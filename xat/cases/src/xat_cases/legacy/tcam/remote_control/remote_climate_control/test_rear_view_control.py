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


@allure.feature("互联服务/远程控制/远程查看喊话")
@allure.story("远程查看喊话")
class TestRearviewControl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update([ "VehicleModeService_server", "FotaMasterService_server", "VehicleTimeService_server",
                         "VehicleSetStatusService_server", "ChassisService_server", "SeatService_server", 
                         "HighVoltageService_server", "ClimateControlService_server", "OuterRearViewService_server",
                         "InteractiveService_server",])
        self.tsp.set_bench_config(self.tb_config["vid"], self.tb_config["tel"])
        time.sleep(60)

    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.io.tcam_kl15_up()
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_PetModeSts(sts=PetModeSts.kUnExpect)
        # self.soa.notify_ViewFault([0,"1",0], [0,"1",1])

        self.soa.notify_ViewFault([0,"1",2])
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusNa, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusNa, validity_right=ValidityLevel.kValid)
        
        time.sleep(1)

    def after_each_func(self, ecu):
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusNa, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusNa, validity_right=ValidityLevel.kValid)
        # self.soa.notify_ViewFault([0,"1",0], [0,"1",1])
        self.soa.notify_PetModeSts(sts=PetModeSts.kUnExpect)
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_ViewFault([0,"1",2])
        time.sleep(20)
        logger.info("等待20s再操作")

    def after_class(self, ecu):
        pass

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_transport")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986928(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail")
    
    @allure.title("远程查看喊话-RVC_远控后视镜折叠_Factory")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986927(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_abandoned")
    @pytest.mark.sanity
    def test_rear_view_control_caseid_1986926(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusFolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusFolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")         

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_inactive")
    @pytest.mark.smoke
    def test_rear_view_control_caseid_1986925(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusFolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusFolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_convience")
    @pytest.mark.smoke
    def test_rear_view_control_caseid_1986924(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_PetModeSts(sts=PetModeSts.kRUN)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusFolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusFolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_active")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986923(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        self.soa.notify_PetModeSts(sts=PetModeSts.kRUN)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusFolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusFolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_宠物kON")
    @pytest.mark.full
    def test_rear_view_control_caseid_1987352(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        self.soa.notify_PetModeSts(sts=PetModeSts.kON)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="PetModeNotRun")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_宠物默认状态")
    @pytest.mark.full
    def test_rear_view_control_caseid_1987353(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        self.soa.notify_PetModeSts(sts=PetModeSts.kUnExpect)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="PetModeNotRun")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_driving")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986922(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        sleep(1)
        self.soa.notify_PetModeSts(sts=PetModeSts.kRUN)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusFolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusFolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_维修模式")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986921(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="MntnMode")      

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_N档")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986920(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Neut)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="ParkFail")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_D档")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986919(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Drv)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="ParkFail")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_R档")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986918(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="ParkFail")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_UPDATE")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986917(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="OTAOngoing")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_ROLLBACK")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986916(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="OTAOngoing") 

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_QUERY")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986915(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusFolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusFolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_NEWTASK")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986914(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusFolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusFolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_DOWNLOADING")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986913(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusFolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusFolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_ACIVE")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986912(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusFolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusFolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_FAILEDNOTDRIVING")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986911(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusFolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusFolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_FAILEDDRIVING")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986910(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_DRIVING)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusFolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusFolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_SUCCESSFUL")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986909(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.SUCCESSFUL)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusFolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusFolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_REACHAPPOINTMENT")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986908(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.REACH_APPOINTMENT)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusFolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusFolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_transport与convience")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986907(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_PetModeSts(sts=PetModeSts.kUnExpect)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_convience与维修模式")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986906(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_PetModeSts(sts=PetModeSts.kON)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="PetModeNotRun")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_维修模式与N档")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986905(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="MntnMode") 

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_N档与UPDATE")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986904(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="ParkFail")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_相同指令")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986903(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        time.sleep(5)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        logger.info("已发送两次远程查看喊话开启请求")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="SysBusy") 

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_SOAFail")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986902(self, ecu):
        self.soa.soa_partner.stop_single_partner("OuterRearViewService_server")
        logger.info("中控锁服务已下线")
        time.sleep(10)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        time.sleep(50)
        assert self.tsp.log_search("SOAFail")
        self.soa.soa_partner.start_single_partner(service="OuterRearViewService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("OuterRearViewService_server",timeout=30)

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_Delayfail")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986901(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_已折叠")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986900(self, ecu):
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusFolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusFolded, validity_right=ValidityLevel.kValid)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_右FaultFold")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986899(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_ViewFault([1,"1",0])
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="FaultFold")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_已故障")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986898(self, ecu):
        self.soa.notify_ViewFault([1,"1",0],[1,"1",1])
        execid = self.tsp.rvc_rear_view_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="FaultFold") 

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_右kFaultTilt")
    @pytest.mark.full
    def test_rear_view_control_caseid_1987371(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_ViewFault([2,"1",0])
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_右kFaultNA")
    @pytest.mark.full
    def test_rear_view_control_caseid_1987370(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_ViewFault([3,"1",0])
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_左FaultFold")
    @pytest.mark.full
    def test_rear_view_control_caseid_1987369(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_ViewFault([1,"1",1])
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="FaultFold")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_左kFaultTilt")
    @pytest.mark.full
    def test_rear_view_control_caseid_1987368(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_ViewFault([2,"1",1])
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_左kFaultNA")
    @pytest.mark.full
    def test_rear_view_control_caseid_1987367(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_ViewFault([3,"1",1])
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_左右FaultFold")
    @pytest.mark.full
    def test_rear_view_control_caseid_1987366(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_ViewFault([1,"1",0],[1,"1",1])
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="FaultFold")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_仅右后视镜折叠")
    @pytest.mark.full
    def test_rear_view_control_caseid_1987365(self, ecu):
        self.soa.notify_OuterRearViewFoldStatus(view_id=ViewId.RearViewRight, value_left=ViewFoldStatus.StatusUnfolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusFolded, validity_right=ValidityLevel.kValid)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远程查看喊话-RVC_远控后视镜折叠_仅左后视镜折叠")
    @pytest.mark.full
    def test_rear_view_control_caseid_1987364(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(view_id=ViewId.RearViewLeft, value_left=ViewFoldStatus.StatusFolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusUnfolded, validity_right=ValidityLevel.kValid)
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_transport")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986897(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        execid = self.tsp.rvc_rear_view_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail")
    
    @allure.title("远程查看喊话-RVC_远控后视镜展开_Factory")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986896(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        execid = self.tsp.rvc_rear_view_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_abandoned")
    @pytest.mark.sanity
    def test_rear_view_control_caseid_1986895(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusUnfolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusUnfolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")         

    @allure.title("远程查看喊话-RVC_远控后视镜展开_inactive")
    @pytest.mark.smoke
    def test_rear_view_control_caseid_1986894(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusUnfolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusUnfolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_convience")
    @pytest.mark.smoke
    def test_rear_view_control_caseid_1986893(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_PetModeSts(sts=PetModeSts.kRUN)
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusUnfolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusUnfolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_宠物kON")
    @pytest.mark.full
    def test_rear_view_control_caseid_1987363(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_PetModeSts(sts=PetModeSts.kON)
        execid = self.tsp.rvc_rear_view_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="PetModeNotRun")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_宠物默认状态")
    @pytest.mark.full
    def test_rear_view_control_caseid_1987362(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_PetModeSts(sts=PetModeSts.kUnExpect)
        execid = self.tsp.rvc_rear_view_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="PetModeNotRun")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_active")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986892(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        self.soa.notify_PetModeSts(sts=PetModeSts.kRUN)
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusUnfolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusUnfolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_driving")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986891(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        sleep(1)
        self.soa.notify_PetModeSts(sts=PetModeSts.kRUN)
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusUnfolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusUnfolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_维修模式")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986890(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        execid = self.tsp.rvc_rear_view_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="MntnMode")      

    @allure.title("远程查看喊话-RVC_远控后视镜展开_N档")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986889(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Neut)
        execid = self.tsp.rvc_rear_view_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="ParkFail")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_D档")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986888(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Drv)
        execid = self.tsp.rvc_rear_view_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="ParkFail")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_R档")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986887(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        execid = self.tsp.rvc_rear_view_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="ParkFail")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_UPDATE")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986886(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_rear_view_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="OTAOngoing")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_ROLLBACK")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986885(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        execid = self.tsp.rvc_rear_view_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="OTAOngoing") 

    @allure.title("远程查看喊话-RVC_远控后视镜展开_QUERY")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986884(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusUnfolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusUnfolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_NEWTASK")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986883(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusUnfolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusUnfolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_DOWNLOADING")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986882(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusUnfolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusUnfolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_ACIVE")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986881(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusUnfolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusUnfolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_FAILEDNOTDRIVING")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986880(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusUnfolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusUnfolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_FAILEDDRIVING")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986879(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_DRIVING)
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusUnfolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusUnfolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_SUCCESSFUL")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986878(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.SUCCESSFUL)
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusUnfolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusUnfolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_REACHAPPOINTMENT")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986877(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.REACH_APPOINTMENT)
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusUnfolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusUnfolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_transport与convience")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986876(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_PetModeSts(sts=PetModeSts.kON)
        execid = self.tsp.rvc_rear_view_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_convience与维修模式")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986875(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_PetModeSts(sts=PetModeSts.kON)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        execid = self.tsp.rvc_rear_view_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="PetModeNotRun")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_维修模式与N档")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986874(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        execid = self.tsp.rvc_rear_view_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="MntnMode") 

    @allure.title("远程查看喊话-RVC_远控后视镜展开_N档与UPDATE")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986873(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_rear_view_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="ParkFail")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_相同指令")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986872(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        time.sleep(5)
        execid1 = self.tsp.rvc_rear_view_control(op=1)
        logger.info("已发送两次远程查看喊话开启请求")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy") 

    @allure.title("远程查看喊话-RVC_远控后视镜展开_SOAFail")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986871(self, ecu):
        self.soa.soa_partner.stop_single_partner("OuterRearViewService_server")
        logger.info("中控锁服务已下线")
        time.sleep(10)
        execid = self.tsp.rvc_rear_view_control(op=1)
        time.sleep(50)
        assert self.tsp.log_search("SOAFail")
        self.soa.soa_partner.start_single_partner(service="OuterRearViewService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("OuterRearViewService_server",timeout=30)

    @allure.title("远程查看喊话-RVC_远控后视镜展开_Delayfail")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986870(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_已展开")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986869(self, ecu):
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusUnfolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusUnfolded, validity_right=ValidityLevel.kValid)
        execid = self.tsp.rvc_rear_view_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @pytest.mark.qw
    @allure.title("远程查看喊话-RVC_远控后视镜展开_右FaultFold")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986868(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_ViewFault([1,"1",0])
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="FaultFold")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_已故障")
    @pytest.mark.full
    def test_rear_view_control_caseid_1986867(self, ecu):
        self.soa.notify_ViewFault([1,"1",0],[1,"1",1])
        execid = self.tsp.rvc_rear_view_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="FaultFold") 

    @pytest.mark.qw
    @allure.title("远程查看喊话-RVC_远控后视镜展开_右kFaultTilt")
    @pytest.mark.full
    def test_rear_view_control_caseid_1987361(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_ViewFault([2,"1",0])
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @pytest.mark.qw
    @allure.title("远程查看喊话-RVC_远控后视镜展开_右kFaultNA")
    @pytest.mark.full
    def test_rear_view_control_caseid_1987360(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_ViewFault([3,"1",0])
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @pytest.mark.qw
    @allure.title("远程查看喊话-RVC_远控后视镜展开_左FaultFold")
    @pytest.mark.full
    def test_rear_view_control_caseid_1987359(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_ViewFault([1,"1",1])
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="FaultFold")

    @pytest.mark.qw
    @allure.title("远程查看喊话-RVC_远控后视镜展开_左kFaultTilt")
    @pytest.mark.full
    def test_rear_view_control_caseid_1987358(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_ViewFault([2,"1",1])
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @pytest.mark.qw
    @allure.title("远程查看喊话-RVC_远控后视镜展开_左kFaultNA")
    @pytest.mark.full
    def test_rear_view_control_caseid_1987357(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_ViewFault([3,"1",1])
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @pytest.mark.qw
    @allure.title("远程查看喊话-RVC_远控后视镜展开_左右FaultFold")
    @pytest.mark.full
    def test_rear_view_control_caseid_1987356(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_ViewFault([1,"1",0],[1,"1",1])
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="FaultFold")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_仅右后视镜展开")
    @pytest.mark.full
    def test_rear_view_control_caseid_1987355(self, ecu):
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        self.soa.notify_OuterRearViewFoldStatus(view_id=ViewId.RearViewLeft,value_left=ViewFoldStatus.StatusFolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusUnfolded, validity_right=ValidityLevel.kValid)
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远程查看喊话-RVC_远控后视镜展开_仅左后视镜展开")
    @pytest.mark.full
    def test_rear_view_control_caseid_1987354(self, ecu):
        self.soa.notify_OuterRearViewFoldStatus(view_id=ViewId.RearViewRight, value_left=ViewFoldStatus.StatusUnfolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusFolded, validity_right=ValidityLevel.kValid)
        execid = self.tsp.rvc_rear_view_control(op=1)
        self.soa.check_Unfold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")
