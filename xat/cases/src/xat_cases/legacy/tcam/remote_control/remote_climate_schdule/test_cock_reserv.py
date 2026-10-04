#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import time
from threading import *
import pytest
import allure
import json

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("互联服务/远程控制/远控座舱预约")
@allure.story("远控座舱预约")
class TestCockReserv(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["HighVoltageService_server", "VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server", "RtcAlarmService_client",
                         "ClimateControlService_server", "CentralLockService_server", "InteractiveService_server",
                         "VehicleTimeService_server", "SteerWheelService_server", "SeatService_server"])
        sleep(8)
    
    def before_each_func(self, ecu):
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.empty_all()
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        sleep(1)
        self.soa.notify_ClimateFault()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Default)
        self.soa.notify_RemotePowerStatus(RemoteClimateStatus.Off)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = False)
        self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off,vent_work_sts=HeatVentWorkStatus.Off)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off,vent_work_sts=HeatVentWorkStatus.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off,vent_work_sts=HeatVentWorkStatus.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off,vent_work_sts=HeatVentWorkStatus.Off)
        self.soa.notify_SteerHeatAvailiable(availiable=SteerHeatAvailiable.On)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))
        sleep(20)

    def after_each_func(self, ecu):
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        sleep(1)
        pass

    def after_class(self, ecu):
        pass


    @pytest.mark.full
    @allure.title("远控座舱预约- RVC_远控座舱预约_transport")
    def test_cock_reserv_CM_1_caseid_1982160(self):
        self.soa.s2s_set_car_mode(CarMode.TRANSPORT)
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd()
            assert self.tsp.log_SubscribeTaskResp_search(keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("远控座舱预约- RVC_远控座舱预约_factory")
    def test_cock_reserv_CM_2_caseid_1982159(self):
        self.soa.s2s_set_car_mode(CarMode.FACTORY)
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd()
            assert self.tsp.log_SubscribeTaskResp_search(keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_维修模式MntnMode")
    def test_cock_reserv_VSS_true_caseid_1982158(self):
        self.soa.s2s_set_mntnmode(True)
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=10, appointment_minute=30, cyclesType=4, appointWeekday="1111111")
            assert self.tsp.log_SubscribeTaskResp_search(keywords="MntnMode"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_FOTAUPdate")
    def test_cock_reserv_FOTA_up_caseid_1982157(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=10, appointment_minute=30, cyclesType=4, appointWeekday="1111111")
            assert self.tsp.log_SubscribeTaskResp_search(keywords="OTAOngoing"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_FOTARollback")
    def test_cock_reserv_FOTA_roll_caseid_1982156(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=10, appointment_minute=30, cyclesType=4, appointWeekday="1111111")
            assert self.tsp.log_SubscribeTaskResp_search(keywords="OTAOngoing"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_CARmode维修模式")
    def test_cock_reserv_CM_VSS_caseid_1982155(self):
        self.soa.s2s_set_car_mode(CarMode.TRANSPORT)
        self.soa.s2s_set_mntnmode(True)
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=10, appointment_minute=30, cyclesType=4, appointWeekday="1111111")
            assert self.tsp.log_SubscribeTaskResp_search(keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_CARmodeFOTA")
    def test_cock_reserv_CM_VSS_caseid_1982154(self):
        self.soa.s2s_set_car_mode(CarMode.TRANSPORT)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=10, appointment_minute=30, cyclesType=4, appointWeekday="1111111")
            assert self.tsp.log_SubscribeTaskResp_search(keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_维修模式FOTA")
    def test_cock_reserv_VSS_FOTA_caseid_1982153(self):
        self.soa.s2s_set_mntnmode(True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=10, appointment_minute=30, cyclesType=4, appointWeekday="1111111")
            assert self.tsp.log_SubscribeTaskResp_search(keywords="MntnMode"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_abandoned设置单次0点")
    def test_cock_reserv_UM_abdn_caseid_1982152(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=0, appointment_minute=0)
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_abandoned取消单次0点")
    def test_cock_reserv_UM_abdn_caseid_1982151(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            task_time=self.tsp.rvc_taskCmd(fixed=True, appointment_hour=0, appointment_minute=0)[1]
            sleep(30)
            self.tsp.cancel_cock_reserv_task(task_time=task_time)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_abandoned修改单次4点")
    def test_cock_reserv_UM_abdn_caseid_1982150(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=4, appointment_minute=0)
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_abandoned修改单次12点")
    def test_cock_reserv_UM_abdn_caseid_1982149(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=12, appointment_minute=0)
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"     
    
    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_abandoned修改单次16点")
    def test_cock_reserv_UM_abdn_caseid_1982148(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=16, appointment_minute=0)
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败" 
    
    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_abandoned设置每日0点")
    def test_cock_reserv_UM_abdn_caseid_1982147(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=0, appointment_minute=0, cyclesType=4, appointWeekday="1111111")
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败" 

    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_abandoned修改每日4点")
    def test_cock_reserv_UM_abdn_caseid_1982146(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=4, appointment_minute=0, cyclesType=4, appointWeekday="1111111")
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败" 

    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_abandoned修改每日12点")
    def test_cock_reserv_UM_abdn_caseid_1982145(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=12, appointment_minute=0, cyclesType=4, appointWeekday="1111111")
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败" 

    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_abandoned修改每日16点")
    def test_cock_reserv_UM_abdn_caseid_1982144(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=16, appointment_minute=0, cyclesType=4, appointWeekday="1111111")
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"  

    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_abandoned设置每一至周五0点")
    def test_cock_reserv_UM_abdn_caseid_1982143(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=0, appointment_minute=0, cyclesType=4, appointWeekday="1111100")
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_abandoned设置每一至周五4点")
    def test_cock_reserv_UM_abdn_caseid_1982142(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=4, appointment_minute=0, cyclesType=4, appointWeekday="1111100")
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_abandoned设置每一至周五12点")
    def test_cock_reserv_UM_abdn_caseid_1982141(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=12, appointment_minute=0, cyclesType=4, appointWeekday="1111100")
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_abandoned设置每一至周五16点")
    def test_cock_reserv_UM_abdn_caseid_1982140(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=16, appointment_minute=0, cyclesType=4, appointWeekday="1111100")
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_abandoned设置每周一/周三/周日0点")
    def test_cock_reserv_UM_abdn_caseid_1982139(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=0, appointment_minute=0, cyclesType=4, appointWeekday="1010100")
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_abandoned设置每周一/周三/周日4点")
    def test_cock_reserv_UM_abdn_caseid_1982138(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=4, appointment_minute=0, cyclesType=4, appointWeekday="1010100")
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_abandoned设置每周一/周三/周日12点")
    def test_cock_reserv_UM_abdn_caseid_1982137(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=12, appointment_minute=0, cyclesType=4, appointWeekday="1010100")
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_abandoned设置每周一/周三/周日16点")
    def test_cock_reserv_UM_abdn_caseid_1982136(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=16, appointment_minute=0, cyclesType=4, appointWeekday="1010100")
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_abandoned设置每周一/周三/周日23点59分")
    def test_cock_reserv_UM_abdn_caseid_1982135(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=23, appointment_minute=59, cyclesType=4, appointWeekday="1010100")
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_abandoned设置每周一/周日0点")
    def test_cock_reserv_UM_abdn_caseid_1982134(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=0, appointment_minute=0, cyclesType=4, appointWeekday="1000001")
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_abandoned设置每周一/周日4点")
    def test_cock_reserv_UM_abdn_caseid_1982133(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=4, appointment_minute=0, cyclesType=4, appointWeekday="1000001")
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_abandoned设置每周一/周日12点")
    def test_cock_reserv_UM_abdn_caseid_1982132(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=12, appointment_minute=0, cyclesType=4, appointWeekday="1000001")
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_abandoned设置每周一/周日16点")
    def test_cock_reserv_UM_abdn_caseid_1982131(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=16, appointment_minute=0, cyclesType=4, appointWeekday="1000001")
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_inactive设置每周一/周三/周日12点")
    def test_cock_reserv_UM_inac_caseid_1982130(self):
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=12, appointment_minute=0, cyclesType=4, appointWeekday="1010001")
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_convience设置每周一/周三/周日12点")
    def test_cock_reserv_UM_inac_caseid_1982129(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=12, appointment_minute=0, cyclesType=4, appointWeekday="1010001")
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_active设置每周一/周三/周日12点")
    def test_cock_reserv_UM_inac_caseid_1982128(self):
        self.soa.s2s_set_usage_mode(UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.ACTIVE)
        sleep(1)
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=12, appointment_minute=0, cyclesType=4, appointWeekday="1010001")
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_driving设置每周一/周三/周日12点")
    def test_cock_reserv_UM_inac_caseid_1982127(self):
        self.soa.s2s_set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.DRIVING)
        sleep(1)
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(fixed=True, appointment_hour=12, appointment_minute=0, cyclesType=4, appointWeekday="1010001")
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.smoke
    @allure.title("RVC_座舱预约执行_预约单次整流程")
    def test_cock_reserv_UM_aban_caseid_1982126(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约"):
            task_time=self.tsp.rvc_taskCmd(appointment_minute=60)[0]
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
            self.mix.wait_appoint_until_excut_time(task_time=task_time)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            self.soa.set_ac_seat_steer_heating_start_success() 
            time_start=time.time()
            sleep(25)
            self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
        with allure.step('等待预约时间结束,校验远控预约执行结果'):    
            self.mix.chk_rvc_threads(target=self.soa.soa_partner.ck_s2s_req, args=[("ClimateControlService_server", "RemoteOff", None, 1800), 
                                                                                   ("SteerWheelService_server", "SetHeat", {"status": 0, "source": 2}, 1800),
                                                                                   ("SeatService_server", "SetHeatingLevel", {"params": [{"id": 0, "uint8Info": 0}], "source": 2}, 1800)])
            assert time.time() - time_start > 1790
        
    @pytest.mark.sanity
    @allure.title("RVC_座舱预约执行_当前时间8点42分，设置单次9点任务")
    def test_cock_reserv_caseid_1982125(self):
        with allure.step("下发远控预约"):
            task_time = self.tsp.rvc_taskCmd(appointment_minute=18)[0]
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
            self.mix.wait_appoint_until_excut_time(task_time=task_time)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req(timeout=20)
            sleep(1)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_SetRemoteClimateSwitchToHVDelay_req(timeout=20)
            self.soa.re_chek_hv_cli_seat_steer_driv_pseng_request()

    @pytest.mark.full
    @allure.title("RVC_座舱预约执行_当前时间8点44分，设置单次9点预约任务")
    def test_cock_reserv_caseid_1982124(self):
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(appointment_minute=16)
            self.soa.check_SetRemoteClimateSwitchToHV_req(timeout=20)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_SetRemoteClimateSwitchToHVDelay_req(timeout=20)
            self.soa.re_chek_hv_cli_seat_steer_driv_pseng_request()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
            
    @pytest.mark.full
    @allure.title("RVC_座舱预约执行_当前时间8点59分，设置单次9点预约任务")
    def test_cock_reserv_caseid_1982123(self):
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(appointment_minute=1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req(timeout=20)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_SetRemoteClimateSwitchToHVDelay_req(timeout=20)
            self.soa.re_chek_hv_cli_seat_steer_driv_pseng_request()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_座舱预约执行_当前时间9点0分，设置单次9点预约任务")
    def test_cock_reserv_caseid_1982122(self):
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(appointment_minute=0)
            self.soa.check_no_hv_cli_seat_steer_driv_pseng_req()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_座舱预约执行_当前时间10点，设置单次9点预约任务")
    def test_cock_reserv_caseid_1982121(self):
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(appointment_minute=1380)
            self.soa.check_no_hv_cli_seat_steer_driv_pseng_req()
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_座舱预约执行_当前时间7点，设置每日9点预约任务")
    def test_cock_reserv_caseid_1982120(self):
        with allure.step("下发远控预约"):
            task_time=self.tsp.rvc_taskCmd(appointment_minute=62, cyclesType=4, appointWeekday="1111111")[0]
            appointment_time = task_time - datetime.timedelta(minutes=45) 
            self.mix.wait_appoint_until_excut_time(appointment_time)
            self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x509, TCAMPNC.PNC30, NMSts.valid, timeout=20)

    # @pytest.mark.full
    # @allure.title("RVC_座舱预约执行_当前时间周一上午7点，设置任务为每周二9点")
    # def test_cock_reserv_caseid_1982119(self):
    #     with allure.step("下发远控预约"):
    #         task_time=self.tsp.rvc_taskCmd(appointment_minute=62, cyclesType=4, appointWeekday="0100000")[0]
    #         appointment_time = task_time - datetime.timedelta(minutes=45) 
    #         self.mix.wait_appoint_until_excut_time(appointment_time)
    #         self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x509, TCAMPNC.PNC30, NMSts.valid, timeout=20)
    
    # @pytest.mark.full
    # @allure.title("RVC_座舱预约执行_当前时间为周一上午10点，设置任务为每周一至周五上午9点")
    # def test_cock_reserv_caseid_1982118(self):
    #     with allure.step("下发远控预约"):
    #         task_time=self.tsp.rvc_taskCmd(appointment_minute=62, cyclesType=4, appointWeekday="1111100")[0]
    #         appointment_time = task_time - datetime.timedelta(minutes=45) 
    #         self.mix.wait_appoint_until_excut_time(appointment_time)
    #         self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x509, TCAMPNC.PNC30, NMSts.valid, timeout=20)
    
    # @pytest.mark.full
    # @allure.title("RVC_座舱预约执行_当前时间为周五上午10点，设置任务为每周一至周五上午9点")
    # def test_cock_reserv_caseid_1982117(self):
    #     with allure.step("下发远控预约"):
    #         task_time=self.tsp.rvc_taskCmd(appointment_minute=62, cyclesType=4, appointWeekday="1111100")[0]
    #         appointment_time = task_time - datetime.timedelta(minutes=45) 
    #         self.mix.wait_appoint_until_excut_time(appointment_time)
    #         self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x509, TCAMPNC.PNC30, NMSts.valid, timeout=20)
    
    @pytest.mark.sanity
    @allure.title("RVC_座舱预约执行_用户上车")
    def test_cock_reserv_caseid_1982116(self):
        with allure.step("下发远控预约"):
            self.tsp.rvc_taskCmd(appointment_minute=15)
            self.soa.set_ac_seat_steer_heating_start_success() 
            sleep(25)
            self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
            self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
            self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetTemperatureAndOn", 20, None)
            
    @pytest.mark.full
    @allure.title("RVC_座舱预约执行_预约任务上报")
    def test_cock_reserv_caseid_1982115(self):
        with allure.step("下发远控预约"):
            task_time = self.tsp.rvc_taskCmd(fixed=True, appointment_hour=9, appointment_minute=0, cyclesType=4, appointWeekday="1111100")[1]
            self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
            self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
            result = self.tsp.log_SubscribeTaskUpload_search(keywords="useVehicleTime")
            self.mix.chk_rvc_cock_reserv_taskupload(task_time=task_time, message=result[1])
            assert result[0], f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_座舱预约执行_无预约任务上报")
    def test_cock_reserv_caseid_1982114(self):
        with allure.step("下发远控预约再取消"):
            task_time = self.tsp.rvc_taskCmd(appointment_minute=20)[1]
            sleep(10)
            self.tsp.cancel_cock_reserv_task(task_time=task_time)
            self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
            self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", seconds=30), f"取消TCAM远程座舱预约后，上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_座舱预约执行_重启TCAM")
    def test_cock_reserv_caseid_1982113(self):
        with allure.step("下发远控预约再取消"):
            task_time = self.tsp.rvc_taskCmd(appointment_minute=20)[1]
            sleep(10)
            self.tsp.cancel_cock_reserv_task(task_time=task_time)
            self.ssh.type_commands(DeviceName.TCAM, "reboot -f", timeout=5)
            sleep(180)
            self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
            self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
            assert self.tsp.log_SubscribeTaskResp_search(fuzz_match="msg=SubscribeTask|SubscribeTaskUpload finsh",detail="uploadReq=execId", keywords="OperateUserId不能为0", seconds=220), f"取消TCAM远程座舱预约后，上报到车云的结果校验失败"


    # @pytest.mark.full
    # @allure.title("RVC_远控座舱预约_连续下发两次远控预约指令")
    # def test_cock_reserv_caseid_1982112(self):
    #     with allure.step("同时下发两次远控预约"):
    #         Thread(target=self.tsp.rvc_taskCmd).start()
    #         Thread(target=self.tsp.rvc_taskCmd).start()
    #         assert self.tsp.log_SubscribeTaskResp_search(keywords="SysBusy"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    # @pytest.mark.full
    # @allure.title("RVC_远控座舱预约_8点45分时下发TSP下发立即开启预约空调任务")
    # def test_cock_reserv_caseid_1982111(self):
    #     with allure.step("下发远控预约"):
    #         task_time=self.tsp.rvc_taskCmd(appointment_minute=18)[0] 
    #         self.mix.wait_appoint_until_excut_time(task_time)
    #         self.tsp.rvc_taskCmd(appointment_minute=0, driver_level=-1, passenger_level=-1)
    #         assert self.tsp.log_SubscribeTaskResp_search(keywords="SysBusy"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    # @pytest.mark.full
    # @allure.title("RVC_远控座舱预约_8点45分时下发远控座舱预约")
    # def test_cock_reserv_caseid_1982110(self):
    #     with allure.step("下发远控预约"):
    #         task_time=self.tsp.rvc_taskCmd(appointment_minute=18)[0] 
    #         self.mix.wait_appoint_until_excut_time(task_time)
    #         self.tsp.rvc_taskCmd(appointment_minute=0)
    #         assert self.tsp.log_SubscribeTaskResp_search(keywords="SysBusy"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    # @pytest.mark.full
    # @allure.title("RVC_远控座舱预约_8点45分时下发远控开启座椅加热")
    # def test_cock_reserv_caseid_1982109(self):
    #     with allure.step("下发远控预约"):
    #         task_time=self.tsp.rvc_taskCmd(appointment_minute=18)[0] 
    #         self.mix.wait_appoint_until_excut_time(task_time)
    #         self.tsp.rvc_taskCmd(appointment_minute=0, steering_level=-1)
    #         assert self.tsp.log_SubscribeTaskResp_search(keywords="SysBusy"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    # @pytest.mark.full
    # @allure.title("RVC_远控座舱预约_8点45分时下发TSP下发立即开启预约方向盘加热任务")
    # def test_cock_reserv_caseid_1982108(self):
    #     with allure.step("下发远控预约"):
    #         task_time=self.tsp.rvc_taskCmd(appointment_minute=18)[0] 
    #         self.mix.wait_appoint_until_excut_time(task_time)
    #         self.tsp.rvc_taskCmd(appointment_minute=0, driver_level=-1, passenger_level=-1)
    #         assert self.tsp.log_SubscribeTaskResp_search(keywords="SysBusy"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_开启空调后，设置立即执行预约")
    def test_cock_reserv_caseid_1982107(self):
        with allure.step("开启空调后，设置立即执行预约"):
            self.tsp.rvc_taskCmd(appointment_minute=15, temp=200, driver_level=-1, passenger_level=-1, steering_level=-1)
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=20)
            sleep(1)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_RemoteOn_req(timeout=20)
            self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=20,timeout=20)
            self.soa.notify_RemotePowerStatus(RemoteClimateStatus.On)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.tsp.rvc_taskCmd(appointment_minute=15, temp=220, driver_level=-1, passenger_level=-1, steering_level=-1)
            self.soa.chk_hv_delay_cli_seat_steer_driv_pseng_req(ac=True, temp=22)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_远控开启座椅加热一档，设置立即执行预约")
    def test_cock_reserv_caseid_1982106(self):
        with allure.step("开启座椅加热一档后，设置立即执行预约"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=20)
            sleep(1)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
            self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, driver_level=3, passenger_level=3, steering_level=-1)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20) 
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"      
    
    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_TSP下发立即开启预约方向盘加热任务二档，设置立即执行预约")
    def test_cock_reserv_caseid_1982105(self):
        with allure.step("开启方向盘二档后，设置立即执行预约"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, driver_level=-1, passenger_level=-1)
            self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.Low)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, driver_level=-1, passenger_level=-1, steering_level=3)
            self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=10)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId")

    @pytest.mark.full
    @allure.title("RVC_远控座舱预约_远控关闭空调")
    def test_cock_reserv_caseid_1982104(self):
        with allure.step("执行预约后，远控关闭空调"):
            task_time=self.tsp.rvc_taskCmd(appointment_minute=15)[0]
            self.soa.set_ac_seat_steer_heating_start_success()
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            execid = self.tsp.rvc_ac_control(-1,230)
        with allure.step('校验远控关闭空调执行结果'):         
            self.soa.check_RemoteOff_req(timeout=5)
            self.soa.notify_RemotePowerStatus(RemoteClimateStatus.Off)
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        with allure.step('等待时间至用户上车时间,校验远控预约执行结果'):         
            self.mix.wait_appoint_until_use_time(task_time)
            self.soa.chk_ac_seat_steer_driv_pseng_off_req(ac_off=True, timeout=90)
    
    @pytest.mark.sanity
    @allure.title("RVC_远控座舱预约_远控调节温度")
    def test_cock_reserv_caseid_1982103(self):
        with allure.step("执行预约后，远控调节空调温度至LO"):
            self.tsp.rvc_taskCmd(appointment_minute=15)
            self.soa.set_ac_seat_steer_heating_start_success()
            time_start=time.time()
            sleep(25)
            self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            execid=self.tsp.rvc_ac_control(1,160)
            self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=16, timeout=20)
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        with allure.step('等待预约时间结束,校验远控预约执行结果'):    
            self.mix.chk_rvc_threads(target=self.soa.soa_partner.ck_s2s_req, args=[("ClimateControlService_server", "RemoteOff", None, 1800), 
                                                                                   ("SteerWheelService_server", "SetHeat", {"status": 0, "source": 2}, 1800),
                                                                                   ("SeatService_server", "SetHeatingLevel", {"params": [{"id": 0, "uint8Info": 0}], "source": 2}, 1800)])
            assert time.time() - time_start > 1790
    
    @pytest.mark.sanity
    @allure.title("RVC_远控座舱预约_远控关闭座椅加热")
    def test_cock_reserv_caseid_1982102(self):
        with allure.step("执行预约后，远控关闭主副驾座椅加热"):
            task_time=self.tsp.rvc_taskCmd(appointment_minute=15)[0]
            self.soa.set_ac_seat_steer_heating_start_success()
            self.tsp.rvc_driver_seat_heat(level=-1)
            self.tsp.rvc_passenger_seat_heat(level=-1)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Off, timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Off, timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Off)
            self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Off)
            assert self.tsp.log_search("Success")
        with allure.step('等待时间至用户上车时间,校验远控预约执行结果'):         
            self.mix.wait_appoint_until_use_time(task_time)
            self.soa.chk_ac_seat_steer_driv_pseng_off_req(seat_off=True, timeout=90)
    
    @pytest.mark.sanity
    @allure.title("RVC_远控座舱预约_远控座椅加热一档")
    def test_cock_reserv_caseid_1982101(self):
        with allure.step("执行预约后，远控开启主副驾座椅一档"):
            task_time=self.tsp.rvc_taskCmd(appointment_minute=15)[0]
            self.soa.set_ac_seat_steer_heating_start_success()
            self.tsp.rvc_driver_seat_heat(level=2)
            self.tsp.rvc_passenger_seat_heat(level=2)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Mid, timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Mid, timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid)
            self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid)
            assert self.tsp.log_search("Success")
        with allure.step('等待时间至用户上车时间,校验远控预约执行结果'):         
            self.mix.wait_appoint_until_use_time(task_time)
            self.soa.chk_ac_seat_steer_driv_pseng_off_req(timeout=90)
    
    @pytest.mark.sanity
    @allure.title("RVC_远控座舱预约_远控关闭方向盘")
    def test_cock_reserv_caseid_1982100(self):
        with allure.step("执行预约后，远控关闭方向盘"):
            task_time=self.tsp.rvc_taskCmd(appointment_minute=15)[0]
            self.soa.set_ac_seat_steer_heating_start_success()
            self.tsp.rvc_steering_wheel_heat(level=-1)
        with allure.step('校验远控关闭方向盘执行结果'):         
            self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Off, timeout=3)
            self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
            assert self.tsp.log_search("Success")
        with allure.step('等待时间至用户上车时间,校验远控预约执行结果'):         
            self.mix.wait_appoint_until_use_time(task_time)
            self.soa.chk_ac_seat_steer_driv_pseng_off_req(steer_off=True, timeout=90)
    
    @pytest.mark.sanity
    @allure.title("RVC_远控座舱预约_远控方向盘加热一档")
    def test_cock_reserv_caseid_1982099(self):
        with allure.step("执行预约后，远控开启方向盘加热任务一档"):
            task_time=self.tsp.rvc_taskCmd(appointment_minute=15)[0]
            self.soa.set_ac_seat_steer_heating_start_success()
            self.tsp.rvc_steering_wheel_heat(level=2)
        with allure.step('校验远控方向盘执行结果'):         
            self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Mid, timeout=3)
            self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
            assert self.tsp.log_search("Success")
        with allure.step('等待时间至用户上车时间,校验远控预约执行结果'):         
            self.mix.wait_appoint_until_use_time(task_time)
            self.soa.chk_ac_seat_steer_driv_pseng_off_req(timeout=90)
    
    @pytest.mark.sanity
    @allure.title("RVC_远控座舱预约_远控关闭空调与座椅加热")
    def test_cock_reserv_caseid_1982098(self):
        with allure.step("执行预约后，远控关闭空调与座椅加热"):
            task_time=self.tsp.rvc_taskCmd(appointment_minute=15)[0]
            self.soa.set_ac_seat_steer_heating_start_success()
            self.tsp.rvc_ac_control(-1,230)
            self.tsp.rvc_driver_seat_heat(level=-1)
            self.tsp.rvc_passenger_seat_heat(level=-1)
        with allure.step('校验远控关闭空调与座椅加热执行结果'):
            self.soa.check_RemoteOff_req(timeout=5)
            self.soa.notify_RemotePowerStatus(RemoteClimateStatus.Off)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Off, timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Off, timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Off)
            self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Off)
            assert self.tsp.log_search("Success")         
        with allure.step('等待时间至用户上车时间,校验远控预约执行结果'):         
            self.mix.wait_appoint_until_use_time(task_time)
            self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Off, timeout=80)
            self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
    
    @pytest.mark.sanity
    @allure.title("RVC_远控座舱预约_远控关闭空调与方向盘加热")
    def test_cock_reserv_caseid_1982097(self):
        with allure.step("执行预约后，远控关闭空调与方向盘加热"):
            task_time=self.tsp.rvc_taskCmd(appointment_minute=15)[0]
            self.soa.set_ac_seat_steer_heating_start_success()
            self.tsp.rvc_ac_control(-1,230)
            self.tsp.rvc_steering_wheel_heat(level=-1)
        with allure.step('校验远控关闭空调与方向盘加热执行结果'):
            self.soa.check_RemoteOff_req(timeout=5)
            self.soa.notify_RemotePowerStatus(RemoteClimateStatus.Off)
            self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Off, timeout=5)
            self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
            assert self.tsp.log_search("Success")         
        with allure.step('等待时间至用户上车时间,校验远控预约执行结果'):         
            self.mix.wait_appoint_until_use_time(task_time)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Off, timeout=80)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Off, timeout=80)
            self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off)
            self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off)
    
    @pytest.mark.sanity
    @allure.title("RVC_远控座舱预约_远控关闭座椅与方向盘加热")
    def test_cock_reserv_caseid_1982096(self):
        with allure.step("执行预约后，远控关闭座椅与方向盘加热"):
            task_time=self.tsp.rvc_taskCmd(appointment_minute=15)[0]
            self.soa.set_ac_seat_steer_heating_start_success()
            self.tsp.rvc_driver_seat_heat(level=-1)
            self.tsp.rvc_passenger_seat_heat(level=-1)
            self.tsp.rvc_steering_wheel_heat(level=-1)
        with allure.step('校验远控关闭座椅与方向盘加热执行结果'):
            self.soa.chk_ac_seat_steer_driv_pseng_off_req(ac_off=True)
            assert self.tsp.log_search("Success")         
        with allure.step('等待时间至用户上车时间,校验远控预约执行结果'):         
            self.mix.wait_appoint_until_use_time(task_time)
            self.soa.check_RemoteOff_req(timeout=90)
            self.soa.notify_RemotePowerStatus(RemoteClimateStatus.Off)
    
    @pytest.mark.sanity
    @allure.title("RVC_远控座舱预约_远控关闭空调、方向盘及座椅")
    def test_cock_reserv_caseid_1982095(self):
        with allure.step("执行预约后，远控关闭空调、座椅与方向盘加热"):
            task_time=self.tsp.rvc_taskCmd(appointment_minute=15)[0]
            self.soa.set_ac_seat_steer_heating_start_success()
            self.tsp.rvc_ac_control(-1,230)
            self.tsp.rvc_driver_seat_heat(level=-1)
            self.tsp.rvc_passenger_seat_heat(level=-1)
            self.tsp.rvc_steering_wheel_heat(level=-1)
        with allure.step('校验远控关闭空调、座椅与方向盘加热执行结果'):
            self.soa.chk_ac_seat_steer_driv_pseng_off_req()
            assert self.tsp.log_search("Success")         
        with allure.step('等待时间至用户上车时间,校验远控预约执行结果'):         
            self.mix.wait_appoint_until_use_time(task_time)
            sleep(5)
            self.soa.chk_no_ac_seat_steer_off_req()

    # @pytest.mark.sanity
    # @allure.title("RVC_远控座舱预约_温度维持，预约空调打断")
    # def test_cock_reserv_caseid_1982094(self):
    #     self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
    #     self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
    #     with allure.step("执行远控闭锁，温度维持开启"):
    #         self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.Unlocked,trigger_id=TriggerSourceId.NoTriggerSource)
    #         self.soa.notify_SetClimateTempMaintainSts(data="1")
    #         sleep(5)
    #         self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked,trigger_id=TriggerSourceId.Telematices)
    #         self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,keep_time=30,timeout=120)
    #         logger.info("已发送高压请求")
    #         self.soa.check_RemoteOn_req(timeout=20)
    #         self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=0,timeout=20)
    #         self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
    #         self.soa.check_RemoteOn_req(timeout=20)
    #         self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=0,timeout=20)
    #         self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
    #     with allure.step("下发可立即执行的预约任务"):
    #         self.tsp.rvc_taskCmd(appointment_minute=15)
    #         assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    #         self.soa.check_SetRemoteClimateSwitchToHVDelay_req(timeout=20)
    #         self.soa.check_RemoteOn_req(timeout=10)
    #         self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=23, timeout=10)

    @pytest.mark.sanity
    @allure.title("RVC_座舱预约执行_设置单次立即执行的预约空调与方向盘")
    def test_cock_reserv_caseid_1982093(self):
        with allure.step("设置单次立即执行的预约空调与方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, driver_level=-1, passenger_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req(timeout=20)
            self.soa.check_RemoteOn_req(timeout=5)
            sleep(1)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_RemoteOn_req(timeout=5)
            self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=23, timeout=10)
            self.soa.check_SteerWheelService_SetHeat_req(heat_level=HeatLevel.Low, timeout=10)
            self.soa.notify_RemotePowerStatus(RemoteClimateStatus.On)
            self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        
    @pytest.mark.sanity
    @allure.title("RVC_座舱预约执行_设置单次立即执行的预约空调与主副座椅")
    def test_cock_reserv_caseid_1982092(self):
        with allure.step("设置单次立即执行的预约空调与主副座椅"):
            self.tsp.rvc_taskCmd(appointment_minute=15, steering_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req(timeout=20)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_SetRemoteClimateSwitchToHVDelay_req(timeout=20)
            self.soa.check_RemoteOn_req(timeout=5)
            self.soa.check_SeatService_SetHeatingLevel_req(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=10)
            self.soa.check_SeatService_SetHeatingLevel_req(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=10)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_座舱预约执行_设置单次立即执行的预约方向盘与主副座椅加热")
    def test_cock_reserv_caseid_1982091(self):
        with allure.step("设置单次立即执行的预约方向盘与主副座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req(timeout=20)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_SetRemoteClimateSwitchToHVDelay_req(timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=10)
            self.soa.check_SeatService_SetHeatingLevel_req(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=10)
            self.soa.check_SteerWheelService_SetHeat_req(heat_level=HeatLevel.Low, timeout=10)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_座舱预约执行_设置单次立即执行的预约空调与主驾座椅")
    def test_cock_reserv_caseid_1982090(self):
        with allure.step("设置单次立即执行的预约空调与主座椅"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, steering_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req(timeout=20)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_SetRemoteClimateSwitchToHVDelay_req(timeout=20)
            self.soa.check_RemoteOn_req(timeout=5)
            self.soa.check_SeatService_SetHeatingLevel_req(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=10)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_座舱预约执行_设置单次立即执行的预约方向盘与主驾座椅")
    def test_cock_reserv_caseid_1982089(self):
        with allure.step("设置单次立即执行的预约方向盘与主副座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req(timeout=20)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_SetRemoteClimateSwitchToHVDelay_req(timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=10)
            self.soa.check_SteerWheelService_SetHeat_req(heat_level=HeatLevel.Low, timeout=10)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_远控座舱预约_convience预约执行")
    def test_cock_reserv_caseid_1982088(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.tsp.rvc_taskCmd(appointment_minute=15)
        self.soa.chk_rvc_inacti_to_conve()
        assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_transport")
    def test_cock_reserv_caseid_1982087(self):
        self.soa.s2s_set_car_mode(CarMode.TRANSPORT)
        self.bus_comm.set_car_mode_to_tcam(CarMode.TRANSPORT)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_factory")
    def test_cock_reserv_caseid_1982086(self):
        self.soa.s2s_set_car_mode(CarMode.FACTORY)
        self.bus_comm.set_car_mode_to_tcam(CarMode.FACTORY)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.smoke
    @allure.title("RVC_TSP下发立即开启预约空调任务_abandoned")
    def test_cock_reserv_caseid_1982085(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            self.soa.remote_climate_open_susccess_when_inactive(temp=23, timeout=20)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
    
    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约空调任务_abandoned15自动关闭")
    def test_cock_reserv_caseid_1982084(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约空调"):
            task_time=self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)[0]
            self.mix.chk_rvc_cock_reserv_pnc()
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            self.soa.remote_climate_open_susccess_when_inactive(temp=23, timeout=10)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.mix.wait_appoint_until_use_time(task_time)
            self.soa.check_RemoteOff_req(timeout=60)
            self.soa.notify_RemotePowerStatus(RemoteClimateStatus.Off)
    
    # @pytest.mark.full
    # # 单域台架环境暂无法实现此用例
    # @allure.title("RVC_TSP下发立即开启预约空调任务_abandoned未上切")
    # def test_cock_reserv_caseid_1982083(self):
    #     self.soa.s2s_set_usage_mode(UsageMode.ABANDONED)
    #     self.bus_comm.set_usage_mode_to_tcam(UsageMode.ABANDONED)
    #     self.bus_comm.pause_all_bus_send()
    #     sleep(60)
    #     with allure.step("下发远控预约空调"):
    #         self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
    #         self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x509, TCAMPNC.PNC30, NMSts.valid, timeout=20)
    #         self.soa.remote_climate_open_susccess_when_inactive(temp=23, timeout=10)
    #         sleep(30)
    #         assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="NetwakeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约空调任务_abandoned高压失败")
    def test_cock_reserv_caseid_1982082(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            self.soa.check_SetRemoteClimateSwitchToHV_req(timeout=5)
            self.soa.remote_climate_check_tcam_request(temp=23, timeout=5)
            sleep(30)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="RemClimaHvStrtFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约空调任务_空调开启失败")
    def test_cock_reserv_caseid_1982081(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            self.soa.check_SetRemoteClimateSwitchToHV_req(timeout=10)
            self.soa.remote_climate_check_tcam_request(temp=23, timeout=10)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.remote_climate_check_tcam_request(temp=23, timeout=5)
            sleep(30)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="DelayFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.smoke
    @allure.title("RVC_TSP下发立即开启预约空调任务_inactive")
    def test_cock_reserv_caseid_1982080(self):
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.remote_climate_open_susccess_when_inactive(temp=23, timeout=10)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_inactive22.5℃")
    def test_cock_reserv_caseid_1982079(self):
        with allure.step("下发远控预约空调"):
            self.soa.notify_RemotePowerStatus(sts=RemoteClimateStatus.On)
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            self.soa.remote_climate_check_tcam_request(temp=23, timeout=5)
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_inactiveLo")
    def test_cock_reserv_caseid_1982078(self):
        with allure.step("下发远控预约空调"):
            self.soa.notify_RemotePowerStatus(sts=RemoteClimateStatus.On)
            self.tsp.rvc_taskCmd(appointment_minute=15, temp=160, passenger_level=-1, driver_level=-1, steering_level=-1)
            self.soa.remote_climate_check_tcam_request(temp=16, timeout=5)
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_inactiveHI")
    def test_cock_reserv_caseid_1982077(self):
        with allure.step("下发远控预约空调"):
            self.soa.notify_RemotePowerStatus(sts=RemoteClimateStatus.On)
            self.tsp.rvc_taskCmd(appointment_minute=15, temp=280, passenger_level=-1, driver_level=-1, steering_level=-1)
            self.soa.remote_climate_check_tcam_request(temp=28, timeout=5)
    
    @pytest.mark.smoke
    @allure.title("RVC_TSP下发立即开启预约空调任务_convience")
    def test_cock_reserv_caseid_1982076(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft, temp=23, timeout=10)
            self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_convience22.5℃")
    def test_cock_reserv_caseid_1982075(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        with allure.step("下发远控预约空调"):
            self.soa.notify_RemotePowerStatus(sts=RemoteClimateStatus.On)
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft, temp=23, timeout=5)
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_convienceLo")
    def test_cock_reserv_caseid_1982074(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        with allure.step("下发远控预约空调"):
            self.soa.notify_RemotePowerStatus(sts=RemoteClimateStatus.On)
            self.tsp.rvc_taskCmd(appointment_minute=15, temp=160, passenger_level=-1, driver_level=-1, steering_level=-1)
            self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft, temp=16, timeout=5)

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_convienceHI")
    def test_cock_reserv_caseid_1982073(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        with allure.step("下发远控预约空调"):
            self.soa.notify_RemotePowerStatus(sts=RemoteClimateStatus.On)
            self.tsp.rvc_taskCmd(appointment_minute=15, temp=280, passenger_level=-1, driver_level=-1, steering_level=-1)
            self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft, temp=28, timeout=5)
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_convience空调开启失败")
    def test_cock_reserv_caseid_1982072(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft, temp=23, timeout=5)
            sleep(30)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="DelayFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_convience主驾占座")
    def test_cock_reserv_caseid_1982071(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_convience副驾占座")
    def test_cock_reserv_caseid_1982070(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,1,0,0,0])
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_convience左后座椅占座")
    def test_cock_reserv_caseid_1982069(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,1,0,0])
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_convience右后座椅占座")
    def test_cock_reserv_caseid_1982068(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,1])
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_convience中后座椅占座")
    def test_cock_reserv_caseid_1982067(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,1,0])
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_convience主驾与副驾占座")
    def test_cock_reserv_caseid_1982066(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,0,0,0])
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_convience主驾与左后座椅占座")
    def test_cock_reserv_caseid_1982065(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,1,0,0])
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_convience主驾与右后座椅占座")
    def test_cock_reserv_caseid_1982064(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,1])
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_convience主驾与中后座椅占座")
    def test_cock_reserv_caseid_1982063(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,1,0])
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_convience三座占座")
    def test_cock_reserv_caseid_1982062(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,0,0,1])
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_convience四座占座")
    def test_cock_reserv_caseid_1982061(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,0,1])
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_convience全部占座")
    def test_cock_reserv_caseid_1982060(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约空调任务_active")
    def test_cock_reserv_caseid_1982059(self):
        self.soa.s2s_set_usage_mode(UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.ACTIVE)
        sleep(1)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约空调任务_driving")
    def test_cock_reserv_caseid_1982058(self):
        self.soa.s2s_set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.DRIVING)
        sleep(1)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约空调任务_维修模式")
    def test_cock_reserv_caseid_1982057(self):
        self.soa.s2s_set_mntnmode(True)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="MntnMode"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约空调任务_N档")
    def test_cock_reserv_caseid_1982056(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.s2s_set_gear(Gear.Neut)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft, temp=23, timeout=10)
            self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约空调任务_FOTAUPDATE")
    def test_cock_reserv_caseid_1982055(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="OTAOngoing"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约空调任务_FOTAROLLBACK")
    def test_cock_reserv_caseid_1982054(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="OTAOngoing"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_transport与active")
    def test_cock_reserv_caseid_1982053(self):
        self.soa.s2s_set_car_mode(CarMode.TRANSPORT)
        self.soa.s2s_set_usage_mode(UsageMode.ACTIVE)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_transport与driving")
    def test_cock_reserv_caseid_1982052(self):
        self.soa.s2s_set_car_mode(CarMode.TRANSPORT)
        self.soa.s2s_set_usage_mode(UsageMode.DRIVING)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_Factory与active")
    def test_cock_reserv_caseid_1982051(self):
        self.soa.s2s_set_car_mode(CarMode.FACTORY)
        self.soa.s2s_set_usage_mode(UsageMode.ACTIVE)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_Factory与driving")
    def test_cock_reserv_caseid_1982050(self):
        self.soa.s2s_set_car_mode(CarMode.FACTORY)
        self.soa.s2s_set_usage_mode(UsageMode.DRIVING)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_transport与N档")
    def test_cock_reserv_caseid_1982049(self):
        self.soa.s2s_set_car_mode(CarMode.TRANSPORT)
        self.soa.s2s_set_gear(Gear.Neut)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_Factory与N档")
    def test_cock_reserv_caseid_1982048(self):
        self.soa.s2s_set_car_mode(CarMode.FACTORY)
        self.soa.s2s_set_gear(Gear.Neut)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_active与维修模式")
    def test_cock_reserv_caseid_1982047(self):
        self.soa.s2s_set_usage_mode(UsageMode.ACTIVE)
        self.soa.s2s_set_mntnmode(True)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="MntnMode"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_drving与维修模式")
    def test_cock_reserv_caseid_1982046(self):
        self.soa.s2s_set_usage_mode(UsageMode.DRIVING)
        self.soa.s2s_set_mntnmode(True)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="MntnMode"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_active与N档")
    def test_cock_reserv_caseid_1982045(self):
        self.soa.s2s_set_usage_mode(UsageMode.ACTIVE)
        self.soa.s2s_set_gear(Gear.Neut)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_drving与N档")
    def test_cock_reserv_caseid_1982044(self):
        self.soa.s2s_set_usage_mode(UsageMode.DRIVING)
        self.soa.s2s_set_gear(Gear.Neut)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_维修模式与N档")
    def test_cock_reserv_caseid_1982043(self):
        self.soa.s2s_set_mntnmode(True)
        self.soa.s2s_set_gear(Gear.Neut)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="MntnMode"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_维修模式与FOTA")
    def test_cock_reserv_caseid_1982042(self):
        self.soa.s2s_set_mntnmode(True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="MntnMode"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_N档与FOTA")
    def test_cock_reserv_caseid_1982041(self):
        self.soa.s2s_set_gear(Gear.Neut)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="OTAOngoing"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约空调任务_高压faultId7")
    def test_cock_reserv_caseid_1982040(self):
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req(timeout=20)
            self.soa.check_RemoteOn_req(timeout=5)
            self.soa.notify_ClimateFault(fault_id=FaultId.FaultBatteryLow)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="BatteryLow"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约空调任务_用户上车")
    def test_cock_reserv_caseid_1982039(self):
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            self.soa.remote_climate_open_susccess_when_inactive(temp=23, timeout=10)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
            self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
            self.soa.ck_no_req("ClimateControlService_server", "RemoteOff",1800)   

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约空调任务_inactivefaultId7")
    def test_cock_reserv_caseid_1982038(self):
        with allure.step("下发远控预约空调"):
            task_time=self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)[0]
            self.soa.remote_climate_open_susccess_when_inactive(temp=23, timeout=10)
            self.soa.notify_ClimateFault(fault_id=FaultId.FaultBatteryLow)
            self.mix.wait_appoint_until_use_time(task_time)
            self.soa.ck_no_req("ClimateControlService_server", "SetTemperatureAndOn", timeout=5)
    
    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约空调任务_inactivefaultId13")
    def test_cock_reserv_caseid_1982037(self):
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, passenger_level=-1, driver_level=-1, steering_level=-1)
            self.soa.remote_climate_open_susccess_when_inactive(temp=23, timeout=10)
            self.soa.notify_ClimateFault(fault_id=FaultId.FaultActivationLimited)
            self.soa.ck_no_req("ClimateControlService_server", "SetTemperatureAndOn", timeout=899)
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_transport")
    def test_cock_reserv_caseid_1982036(self):
        self.soa.s2s_set_car_mode(CarMode.TRANSPORT)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_factory")
    def test_cock_reserv_caseid_1982035(self):
        self.soa.s2s_set_car_mode(CarMode.FACTORY)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.smoke
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_abandoned")
    def test_cock_reserv_caseid_1982034(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=10)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_SetRemoteClimateSwitchToHVDelay_req(timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
            self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_abandoned15自动关闭")
    def test_cock_reserv_caseid_1982033(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控主副驾座椅加热"):
            task_time=self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)[0]
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=10)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_SetRemoteClimateSwitchToHVDelay_req(timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
            self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
            self.mix.wait_appoint_until_use_time(task_time)
            Thread(target=self.soa.check_SeatService_SetHeatingLevel_req,args=(SeatId.FrontLeft, HeatLevel.Off, "timeout=80")).start()
            Thread(target=self.soa.check_SeatService_SetHeatingLevel_req,args=(SeatId.FrontRight, HeatLevel.Off, "timeout=80")).start()
    
    # @pytest.mark.full
    # # 单域台架环境暂无法实现此用例
    # @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_未上切abandoned")
    # def test_cock_reserv_caseid_1982032(self):
    #     self.soa.s2s_set_usage_mode(UsageMode.ABANDONED)
    #     self.bus_comm.set_usage_mode_to_tcam(UsageMode.ABANDONED)
    #     # self.io.tcam_kl15_down()
    #     self.bus_comm.pause_all_bus_send()
    #     sleep(60)
    #     with allure.step("下发远控主副驾座椅加热"):
    #         self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
    #         self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x509, TCAMPNC.PNC30, NMSts.valid, timeout=20)
    #         self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=10)
    #         self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
    #         self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
    #         self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
    #         self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
    #         self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
    #         self.soa.notify_SeatHeatVentStatus(id=SeatId.FrontLeft, heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
    #         self.soa.notify_SeatHeatVentStatus(id=SeatId.FrontRight, heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
    #         sleep(30)
    #         assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="NetwakeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_abandoned高压失败")
    def test_cock_reserv_caseid_1982031(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req(timeout=10)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
            sleep(30)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="RemClimaHvStrtFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_主驾座椅加热开启失败")
    def test_cock_reserv_caseid_1982030(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=10)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_SetRemoteClimateSwitchToHVDelay_req(timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
            sleep(30)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="DelayFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.smoke
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_inactive加热3档")
    def test_cock_reserv_caseid_1982029(self):
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, driver_level=3, passenger_level=3, steering_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=10)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_SetRemoteClimateSwitchToHVDelay_req(timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
            self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_inactive加热2档")
    def test_cock_reserv_caseid_1982028(self):
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, driver_level=2, passenger_level=2, steering_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=10)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Mid, timeout=20)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_SetRemoteClimateSwitchToHVDelay_req(timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Mid, timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Mid, timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid)
            self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_inactive加热1档")
    def test_cock_reserv_caseid_1982027(self):
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=10)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_SetRemoteClimateSwitchToHVDelay_req(timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
            self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_inactive15自动关闭")
    def test_cock_reserv_caseid_1982026(self):
        with allure.step("下发远控主副驾座椅加热"):
            task_time=self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)[0]
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=10)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_SetRemoteClimateSwitchToHVDelay_req(timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
            self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
            sleep(300)
            self.tsp.rvc_driver_seat_heat(level=3)
            self.tsp.rvc_passenger_seat_heat(level=3)
            self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
            self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
            assert self.tsp.log_SubscribeTaskResp_search(fuzz_match="msg=sendCmd|vehicleReportHandleFinish",detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
            self.mix.wait_appoint_until_use_time(task_time)
            Thread(target=self.soa.check_SeatService_SetHeatingLevel_req,args=(SeatId.FrontLeft, HeatLevel.Off, "timeout=80")).start()
            Thread(target=self.soa.check_SeatService_SetHeatingLevel_req,args=(SeatId.FrontRight, HeatLevel.Off, "timeout=80")).start()
    
    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_inactive高压失败")
    def test_cock_reserv_caseid_1982025(self):
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req(timeout=5)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
            sleep(30)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="RemClimaHvStrtFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_inactive主驾座椅加热开启失败")
    def test_cock_reserv_caseid_1982024(self):
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=10)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
            sleep(30)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="DelayFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_inactive主驾座椅加热开启")
    def test_cock_reserv_caseid_1982023(self):
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, driver_level=3, passenger_level=3, steering_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=10)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
            self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.smoke
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_convience加热3档")
    def test_cock_reserv_caseid_1982022(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, driver_level=3, passenger_level=3, steering_level=-1)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
            self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_convience加热2档")
    def test_cock_reserv_caseid_1982021(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, driver_level=2, passenger_level=2, steering_level=-1)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Mid, timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Mid, timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid)
            self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_convience加热1档")
    def test_cock_reserv_caseid_1982020(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
            self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_convience主驾座椅加热开启失败")
    def test_cock_reserv_caseid_1982019(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
            sleep(30)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="DelayFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_convience主驾座椅通风开启")
    def test_cock_reserv_caseid_1982018(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=HeatLevel.Low)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            sleep(30)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="DelayFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
       
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_主驾座椅加热开启")
    def test_cock_reserv_caseid_1982017(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_用户上车维持")
    def test_cock_reserv_caseid_1982016(self):
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, driver_level=3, passenger_level=-1, steering_level=-1)
            sleep(1)
            self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
            self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
            self.soa.check_SeatService_SetHeatingLevel_req(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=10)
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_convience主驾占座")
    def test_cock_reserv_caseid_1982015(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_convience副驾占座")
    def test_cock_reserv_caseid_1982014(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,1,0,0,0])
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_convience左后座椅占座")
    def test_cock_reserv_caseid_1982013(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,1,0,0])
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_convience右后座椅占座")
    def test_cock_reserv_caseid_1982012(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,1])
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_convience中后座椅占座")
    def test_cock_reserv_caseid_1982011(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,1,0])
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_convience主驾与副驾占座")
    def test_cock_reserv_caseid_1982010(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,0,0,0])
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_convience主驾与左后座椅占座")
    def test_cock_reserv_caseid_1982009(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,1,0,0])
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_convience主驾与右后座椅占座")
    def test_cock_reserv_caseid_1982008(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,1])
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_convience主驾与中后座椅占座")
    def test_cock_reserv_caseid_1982007(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,1,0])
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_convience三座占座")
    def test_cock_reserv_caseid_1982006(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,0,0,1])
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_convience四座占座")
    def test_cock_reserv_caseid_1982005(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,0,1])
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_convience全部占座")
    def test_cock_reserv_caseid_1982004(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_active")
    def test_cock_reserv_caseid_1982003(self):
        self.soa.s2s_set_usage_mode(UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.ACTIVE)
        sleep(1)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_driving")
    def test_cock_reserv_caseid_1982002(self):
        self.soa.s2s_set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.DRIVING)
        sleep(1)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_维修模式")
    def test_cock_reserv_caseid_1982001(self):
        self.soa.s2s_set_mntnmode(True)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="MntnMode"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("VC_TSP下发立即开启预约主副驾座椅加热任务_N档")
    def test_cock_reserv_caseid_1982000(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.s2s_set_gear(Gear.Neut)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
            self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_FOTAUPDATE")
    def test_cock_reserv_caseid_1981999(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="OTAOngoing"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_FOTAROLLBACK")
    def test_cock_reserv_caseid_1981998(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="OTAOngoing"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_transport与active")
    def test_cock_reserv_caseid_1981997(self):
        self.soa.s2s_set_car_mode(CarMode.TRANSPORT)
        self.soa.s2s_set_usage_mode(UsageMode.ACTIVE)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_transport与driving")
    def test_cock_reserv_caseid_1981996(self):
        self.soa.s2s_set_car_mode(CarMode.TRANSPORT)
        self.soa.s2s_set_usage_mode(UsageMode.DRIVING)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_Factory与active")
    def test_cock_reserv_caseid_1981995(self):
        self.soa.s2s_set_car_mode(CarMode.FACTORY)
        self.soa.s2s_set_usage_mode(UsageMode.ACTIVE)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_Factory与driving")
    def test_cock_reserv_caseid_1981994(self):
        self.soa.s2s_set_car_mode(CarMode.FACTORY)
        self.soa.s2s_set_usage_mode(UsageMode.DRIVING)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_transport与N档")
    def test_cock_reserv_caseid_1981993(self):
        self.soa.s2s_set_car_mode(CarMode.TRANSPORT)
        self.soa.s2s_set_gear(Gear.Neut)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_Factory与N档")
    def test_cock_reserv_caseid_1981992(self):
        self.soa.s2s_set_car_mode(CarMode.FACTORY)
        self.soa.s2s_set_gear(Gear.Neut)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_active与维修模式")
    def test_cock_reserv_caseid_1981991(self):
        self.soa.s2s_set_usage_mode(UsageMode.ACTIVE)
        self.soa.s2s_set_mntnmode(True)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="MntnMode"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_drving与维修模式")
    def test_cock_reserv_caseid_1981990(self):
        self.soa.s2s_set_usage_mode(UsageMode.DRIVING)
        self.soa.s2s_set_mntnmode(True)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="MntnMode"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_active与N档")
    def test_cock_reserv_caseid_1981989(self):
        self.soa.s2s_set_usage_mode(UsageMode.ACTIVE)
        self.soa.s2s_set_gear(Gear.Neut)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_drving与N档")
    def test_cock_reserv_caseid_1981988(self):
        self.soa.s2s_set_usage_mode(UsageMode.DRIVING)
        self.soa.s2s_set_gear(Gear.Neut)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_维修模式与N档")
    def test_cock_reserv_caseid_1981987(self):
        self.soa.s2s_set_mntnmode(True)
        self.soa.s2s_set_gear(Gear.Neut)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="MntnMode"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_维修模式与FOTA")
    def test_cock_reserv_caseid_1981986(self):
        self.soa.s2s_set_mntnmode(True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="MntnMode"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_N档与FOTA")
    def test_cock_reserv_caseid_1981985(self):
        self.soa.s2s_set_gear(Gear.Neut)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, steering_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="OTAOngoing"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_高压faultId7")
    def test_cock_reserv_caseid_1981984(self):
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, driver_level=3, passenger_level=3, steering_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=10)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20)
            self.soa.notify_ClimateFault(fault_id=FaultId.FaultBatteryLow)
            sleep(30)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="BatteryLow"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约主副驾座椅加热任务_inactivefaultId7")
    def test_cock_reserv_caseid_1981983(self):
        with allure.step("下发远控主副驾座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, driver_level=3, passenger_level=3, steering_level=-1)
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=10)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
            self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
            self.soa.notify_ClimateFault(fault_id=FaultId.FaultBatteryLow)
            threads = [Thread(target=self.soa.soa_partner.ck_no_req, args=("SeatService_server", "SetHeatingLevel", 899, {"params": [{"id": i, "uint8Info": 0}]})) for i in [0, 1]]
            [t.start() for t in threads]; [t.join() for t in threads]

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约空调任务_inactivefaultId13")
    def test_cock_reserv_caseid_1981982(self):
        with allure.step("下发远控预约空调"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, driver_level=3, passenger_level=3, steering_level=-1)
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=10)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
            self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
            self.soa.notify_ClimateFault(fault_id=FaultId.FaultActivationLimited)
            threads = [Thread(target=self.soa.soa_partner.ck_no_req, args=("SeatService_server", "SetHeatingLevel", 899, {"params": [{"id": i, "uint8Info": 0}]})) for i in [0, 1]]
            [t.start() for t in threads]; [t.join() for t in threads]
            
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_transport")
    def test_cock_reserv_caseid_1981981(self):
        self.soa.s2s_set_car_mode(CarMode.TRANSPORT)
        self.bus_comm.set_car_mode_to_tcam(CarMode.TRANSPORT)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_factory")
    def test_cock_reserv_caseid_1981980(self):
        self.soa.s2s_set_car_mode(CarMode.FACTORY)
        self.bus_comm.set_car_mode_to_tcam(CarMode.FACTORY)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.smoke
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_abandoned")
    def test_cock_reserv_caseid_1981979(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.Low)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
    
    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_abandoned15自动关闭")
    def test_cock_reserv_caseid_1981978(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约方向盘"):
            task_time=self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)[0]
            self.mix.chk_rvc_cock_reserv_pnc()
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.Low)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.mix.wait_appoint_until_use_time(task_time)
            self.soa.check_SteerWheelService_SetHeat_req(heat_level=HeatLevel.Off, timeout=80)
            self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
    
    # @pytest.mark.full
    # # 单域台架环境暂无法实现此用例
    # @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_未上切abandoned")
    # def test_cock_reserv_caseid_1981977(self):
    #     self.soa.s2s_set_usage_mode(UsageMode.ABANDONED)
    #     self.bus_comm.set_usage_mode_to_tcam(UsageMode.ABANDONED)
    #     self.bus_comm.pause_all_bus_send()
    #     sleep(60)
    #     with allure.step("下发远控预约方向盘"):
    #         self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
    #         self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x509, TCAMPNC.PNC30, NMSts.valid, timeout=20)
    #         self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.Low)
    #         sleep(30)
    #         assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="NetwakeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_abandoned高压失败")
    def test_cock_reserv_caseid_1981976(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            self.soa.check_SetRemoteClimateSwitchToHV_req(timeout=20)
            self.soa.check_SteerWheelService_SetHeat_req(heat_level=HeatLevel.Low, timeout=5)
            sleep(30)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="RemClimaHvStrtFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_方向盘加热开启失败")
    def test_cock_reserv_caseid_1981975(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            self.soa.check_SetRemoteClimateSwitchToHV_req(timeout=5)
            self.soa.check_SteerWheelService_SetHeat_req(heat_level=HeatLevel.Low, timeout=5)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_SteerWheelService_SetHeat_req(heat_level=HeatLevel.Low, timeout=5)
            sleep(30)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="DelayFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.smoke
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_inactive加热3档")
    def test_cock_reserv_caseid_1981974(self):
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1, steering_level=3)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.High)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_inactive加热2档")
    def test_cock_reserv_caseid_1981973(self):
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1, steering_level=2)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.Mid)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_inactive加热1档")
    def test_cock_reserv_caseid_1981972(self):
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.Low)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_inactive15自动关闭")
    def test_cock_reserv_caseid_1981971(self):
        with allure.step("下发远控预约方向盘"):
            task_time=self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1, steering_level=3)[0]
            self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.High)
            sleep(300)
            self.tsp.rvc_steering_wheel_heat(level=1)
            self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Low, timeout=20)
            self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
            assert self.tsp.log_search("Success"), f"TCAM远程座舱执行结果上报到车云的结果校验失败"
            self.mix.wait_appoint_until_use_time(task_time)
            self.soa.check_SteerWheelService_SetHeat_req(heat_level=HeatLevel.Off, timeout=80)
    
    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_inactive高压失败")
    def test_cock_reserv_caseid_1981970(self):
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req(timeout=5)
            self.soa.check_SteerWheelService_SetHeat_req(heat_level=HeatLevel.Low, timeout=5)
            sleep(30)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="RemClimaHvStrtFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_inactive方向盘加热开启失败")
    def test_cock_reserv_caseid_1981969(self):
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=10)
            self.soa.check_SteerWheelService_SetHeat_req(heat_level=HeatLevel.Low, timeout=5)
            self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.On)
            self.soa.check_SteerWheelService_SetHeat_req(heat_level=HeatLevel.Low, timeout=5)
            sleep(30)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="DelayFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_inactive方向盘加热开启")
    def test_cock_reserv_caseid_1981968(self):
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.smoke
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_convience加热3档")
    def test_cock_reserv_caseid_1981967(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1, steering_level=3)
            self.soa.check_SteerWheelService_SetHeat_req(heat_level=HeatLevel.High, timeout=5)
            self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_convience加热2档")
    def test_cock_reserv_caseid_1981966(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1, steering_level=2)
            self.soa.check_SteerWheelService_SetHeat_req(heat_level=HeatLevel.Mid, timeout=5)
            self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_convience加热1档")
    def test_cock_reserv_caseid_1981965(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            self.soa.check_SteerWheelService_SetHeat_req(heat_level=HeatLevel.Low, timeout=5)
            self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_convience方向盘加热开启失败")
    def test_cock_reserv_caseid_1981964(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            self.soa.check_SteerWheelService_SetHeat_req(heat_level=HeatLevel.Low, timeout=5)
            sleep(30)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="DelayFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_convience方向盘加热开启")
    def test_cock_reserv_caseid_1981963(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1, steering_level=3)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
       
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_用户上车维持")
    def test_cock_reserv_caseid_1981962(self):
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            sleep(1)
            self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
            self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
            self.soa.check_SteerWheelService_SetHeat_req(heat_level=HeatLevel.Low, timeout=10)
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_convience主驾占座")
    def test_cock_reserv_caseid_1981961(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_convience副驾占座")
    def test_cock_reserv_caseid_1981960(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,1,0,0,0])
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_convience左后座椅占座")
    def test_cock_reserv_caseid_1981959(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,1,0,0])
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_convience右后座椅占座")
    def test_cock_reserv_caseid_1981958(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,1])
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_convience中后座椅占座")
    def test_cock_reserv_caseid_1981957(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,1,0])
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_convience主驾与副驾占座")
    def test_cock_reserv_caseid_1981956(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,0,0,0])
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_convience主驾与左后座椅占座")
    def test_cock_reserv_caseid_1981955(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,1,0,0])
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_convience主驾与右后座椅占座")
    def test_cock_reserv_caseid_1981954(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,1])
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_convience主驾与中后座椅占座")
    def test_cock_reserv_caseid_1981953(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,1,0])
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_convience三座占座")
    def test_cock_reserv_caseid_1981952(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,0,0,1])
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_convience四座占座")
    def test_cock_reserv_caseid_1981951(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,0,1])
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_convience全部占座")
    def test_cock_reserv_caseid_1981950(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_active")
    def test_cock_reserv_caseid_1981949(self):
        self.soa.s2s_set_usage_mode(UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.ACTIVE)
        sleep(1)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_driving")
    def test_cock_reserv_caseid_1981948(self):
        self.soa.s2s_set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.DRIVING)
        sleep(1)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_维修模式")
    def test_cock_reserv_caseid_1981947(self):
        self.soa.s2s_set_mntnmode(True)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="MntnMode"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_N档")
    def test_cock_reserv_caseid_1981946(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.s2s_set_gear(Gear.Neut)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            self.soa.check_SteerWheelService_SetHeat_req(heat_level=HeatLevel.Low, timeout=5)
            self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_FOTAUPDATE")
    def test_cock_reserv_caseid_1981945(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="OTAOngoing"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.sanity
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_FOTAROLLBACK")
    def test_cock_reserv_caseid_1981944(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="OTAOngoing"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_transport与active")
    def test_cock_reserv_caseid_1981943(self):
        self.soa.s2s_set_car_mode(CarMode.TRANSPORT)
        self.soa.s2s_set_usage_mode(UsageMode.ACTIVE)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_transport与driving")
    def test_cock_reserv_caseid_1981942(self):
        self.soa.s2s_set_car_mode(CarMode.TRANSPORT)
        self.soa.s2s_set_usage_mode(UsageMode.DRIVING)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_Factory与active")
    def test_cock_reserv_caseid_1981941(self):
        self.soa.s2s_set_car_mode(CarMode.FACTORY)
        self.soa.s2s_set_usage_mode(UsageMode.ACTIVE)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_Factory与driving")
    def test_cock_reserv_caseid_1981940(self):
        self.soa.s2s_set_car_mode(CarMode.FACTORY)
        self.soa.s2s_set_usage_mode(UsageMode.DRIVING)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_transport与N档")
    def test_cock_reserv_caseid_1981939(self):
        self.soa.s2s_set_car_mode(CarMode.TRANSPORT)
        self.soa.s2s_set_gear(Gear.Neut)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_Factory与N档")
    def test_cock_reserv_caseid_1981938(self):
        self.soa.s2s_set_car_mode(CarMode.FACTORY)
        self.soa.s2s_set_gear(Gear.Neut)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="CarModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_active与维修模式")
    def test_cock_reserv_caseid_1981937(self):
        self.soa.s2s_set_usage_mode(UsageMode.ACTIVE)
        self.soa.s2s_set_mntnmode(True)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="MntnMode"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_drving与维修模式")
    def test_cock_reserv_caseid_1981936(self):
        self.soa.s2s_set_usage_mode(UsageMode.DRIVING)
        self.soa.s2s_set_mntnmode(True)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="MntnMode"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_active与N档")
    def test_cock_reserv_caseid_1981935(self):
        self.soa.s2s_set_usage_mode(UsageMode.ACTIVE)
        self.soa.s2s_set_gear(Gear.Neut)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_drving与N档")
    def test_cock_reserv_caseid_1981934(self):
        self.soa.s2s_set_usage_mode(UsageMode.DRIVING)
        self.soa.s2s_set_gear(Gear.Neut)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_维修模式与N档")
    def test_cock_reserv_caseid_1981933(self):
        self.soa.s2s_set_mntnmode(True)
        self.soa.s2s_set_gear(Gear.Neut)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="MntnMode"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_维修模式与FOTA")
    def test_cock_reserv_caseid_1981932(self):
        self.soa.s2s_set_mntnmode(True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="MntnMode"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_N档与FOTA")
    def test_cock_reserv_caseid_1981931(self):
        self.soa.s2s_set_gear(Gear.Neut)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="OTAOngoing"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_高压faultId7")
    def test_cock_reserv_caseid_1981930(self):
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req(timeout=20)
            self.soa.check_SteerWheelService_SetHeat_req(heat_level=HeatLevel.Low, timeout=5)
            self.soa.notify_ClimateFault(fault_id=FaultId.FaultBatteryLow)
            sleep(30)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="BatteryLow"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_TelmFctReq")
    def test_cock_reserv_caseid_1981929(self):
        self.soa.s2s_set_usage_mode(UsageMode.ABANDONED)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.ABANDONED)
        sleep(1)
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            self.bus_comm.check("connectivitycanfd", "TcamConnectivityFr35", "TelmFctReq", 1, timeout=10)

    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任务_inactivefaultId7")
    def test_cock_reserv_caseid_1981928(self):
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.Low)
            self.soa.notify_ClimateFault(fault_id=FaultId.FaultBatteryLow)
            self.soa.soa_partner.ck_no_req("SteerWheelService_server", "SetHeat", 1800, {"status": HeatLevel.Off})
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任_inactivefaultId13")
    def test_cock_reserv_caseid_1981927(self):
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.Low)
            self.soa.notify_ClimateFault(fault_id=FaultId.FaultActivationLimited)
            self.soa.soa_partner.ck_no_req("SteerWheelService_server", "SetHeat", 1800, {"status": HeatLevel.Off})
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任_inactivekError")
    def test_cock_reserv_caseid_1981926(self):
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.Low)
            self.soa.notify_SteerHeatAvailiable(availiable=SteerHeatAvailiable.Error)
            self.soa.soa_partner.ck_no_req("SteerWheelService_server", "SetHeat", 1800, {"status": HeatLevel.Off})
    
    @pytest.mark.full
    @allure.title("RVC_TSP下发立即开启预约方向盘加热任_inactivekENERGY_LIMIT")
    def test_cock_reserv_caseid_1981925(self):
        with allure.step("下发远控预约方向盘"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, passenger_level=-1, driver_level=-1)
            self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.Low)
            self.soa.notify_SteerHeatAvailiable(availiable=SteerHeatAvailiable.Energy_Limit)
            self.soa.soa_partner.ck_no_req("SteerWheelService_server", "SetHeat", 1800, {"status": HeatLevel.Off})

    @pytest.mark.xin
    @pytest.mark.full
    @allure.title("RVC_交流预约充电_休眠重启休眠唤醒")
    def test_cock_reserv_caseid_1982109(self):
        self.soa.send_SetBookEvent_req(ser_name="HighVoltageAppService",sch_time=960)
        time.sleep(10)
        self.mix.tcam_network_sleep()
        logger.info("TCAM休眠")
        self.io.tcam_power_off()
        time.sleep(60)
        self.io.tcam_power_on()
        logger.info("TCAM唤醒")
        time.sleep(480)
        self.mix.tcam_network_sleep()
        logger.info("TCAM休眠")
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=300)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC23,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyTimeUpEventInfo_event(service_name="HighVoltageAppService", timeout=20)

    @pytest.mark.full
    @allure.title("RVC_交流预约充电_休眠唤醒")
    def test_cock_reserv_caseid_1982110(self):
        self.soa.send_SetBookEvent_req(ser_name="HighVoltageAppService",sch_time=300)
        self.mix.tcam_network_sleep()
        logger.info("TCAM休眠")
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=300)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC23,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyTimeUpEventInfo_event(service_name="HighVoltageAppService", timeout=20)

    @pytest.mark.sanity
    @allure.title("RVC_远程预约_预约全部功能")
    def test_cock_reserv_caseid_1982111(self):
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=1,driver_level=-1,passenger_level=-1,RearLeft_level=1,RearRight_level=1,steering_level=1,DriverVent_level=1,PassengerVent_level=1,RearLeftVent_level=-1,RearRightVent_level=-1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30, timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=23,timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Low, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=VentLevel.Low, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=HeatLevel.Low, timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")