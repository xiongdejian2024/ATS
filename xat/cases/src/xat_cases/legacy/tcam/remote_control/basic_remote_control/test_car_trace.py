#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import pytest
import allure
import time

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.common import *

@allure.feature("互联服务/远程控制/远程寻车控制")
@allure.story("远程寻车控制")
class TestCarTraceCtrl(TestABCBase):
    def before_class(self, ecu):        
        self.soa.update(["HighVoltageService_server","VehicleModeService_server", "FotaMasterService_server",
                    "VehicleSetStatusService_server", "ChassisService_server", 
                    "VehicleTimeService_server", "SeatService_server",
                   "KeyService_server","LightService_server"])
        self.mix.start_get_request_and_send_response_to_tcam_thread(["HighVoltageService_server","VehicleModeService_server", "FotaMasterService_server",
                    "VehicleSetStatusService_server", "ChassisService_server", 
                    "VehicleTimeService_server", "SeatService_server",
                   "KeyService_server","LightService_server"])
        sleep(30)
        
    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))
        sleep(1)
          
    def after_each_func(self, ecu):
        if ecu.testresult == 'Failure':
            logger.info('用例执行失败')
            sleep(12)
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.ipdu.reset_check_results()


    def after_class(self, ecu):
        self.mix.stop_get_request_and_send_response_to_tcam_thread()


    @allure.title("远程控制-RVC_远程寻车控制_闪灯_等待远程寻车开始时间超时")
    @pytest.mark.full
    def test_OnlyLight_CarLocalTraceActiveStatus_timeout_kFail_caseid_1982652(self):
        execid = self.tsp.rvc_find_vehicle(op=2)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 30)
        time.sleep(12)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_等待远程寻车开始时间超时")
    @pytest.mark.full
    def test_OnlyLight_CarLocalTraceActiveStatus_timeout_kIdle_caseid_1982653(self):
        execid = self.tsp.rvc_find_vehicle(op=1)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 30)
        time.sleep(12)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_等待远程寻车开始时间超时内sts=kSuccess")
    @pytest.mark.sanity
    def test_OnlyLight_CarLocalTraceActiveStatus_timeout_kSuccess_caseid_1982654(self):
        execid = self.tsp.rvc_find_vehicle(op=2)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(11)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   


    @allure.title("远程控制-RVC_远程寻车控制_闪灯_等待远程寻车开始时间超时内sts=kFail")
    @pytest.mark.sanity
    def test_OnlyLight_CarLocalTraceActiveStatus_kFail_caseid_1982655(self):
        execid = self.tsp.rvc_find_vehicle(op=2)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(2)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kFail)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_远程寻车功能超时时间超时内sts=kIdle")
    @pytest.mark.full
    def test_OnlyLight_CarLocalTraceActiveStatus_kSuccess_caseid_1982656(self):
        execid = self.tsp.rvc_find_vehicle(op=2)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(2)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   


    @allure.title("远程控制-RVC_远程寻车控制_闪灯_等待远程寻车开始时间超时sts=kSuccess")
    @pytest.mark.full
    def test_OnlyLight_CarLocalTraceActiveStatus_timeout_kSuccess_caseid_1982657(self):
        execid = self.tsp.rvc_find_vehicle(op=2)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 10)
        time.sleep(11)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_等待远程寻车开始时间超时sts=kFail")
    @pytest.mark.full
    def test_OnlyLight_CarLocalTraceActiveStatus_timeout_kFail_caseid_1982658(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle(op=2)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 10)
        time.sleep(10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kFail)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_等待远程寻车开始时间超时sts=kIdle")
    @pytest.mark.full
    def test_OnlyLight_CarLocalTraceActiveStatus_timeout_kIdle_caseid_1982659(self):
        execid = self.tsp.rvc_find_vehicle(op=2)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 10)
        time.sleep(10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_等待远程寻车开始时间超时内sts=kFail")
    @pytest.mark.full
    def test_OnlyLight_CarLocalTraceActiveStatus_kFail_caseid_1982660(self):
        execid = self.tsp.rvc_find_vehicle(op=2)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 10)
        time.sleep(2)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kFail)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_等待远程寻车开始时间超时内sts=kIdle")
    @pytest.mark.full
    def test_OnlyLight_CarLocalTraceActiveStatus_kIdle_caseid_1982661(self):
        execid = self.tsp.rvc_find_vehicle(op=2)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_寻车等待解闭锁灯提示结束时间超时NotifyTurnLampStatus.sts == kHazard")
    @pytest.mark.full
    def test_OnlyLight_TurnLampMode_timeout_kHazard_caseid_1982662(self):
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kRight)
        execid = self.tsp.rvc_find_vehicle(op=2)
        time.sleep(2.4)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kHazard)
        assert self.tsp.log_search_remote_vehicle_control("ReqPriorLowFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_寻车等待解闭锁灯提示结束时间超时NotifyTurnLampStatus.sts == kRight")
    @pytest.mark.full
    def test_OnlyLight_TurnLampMode_timeout_kRight_caseid_1982663(self):
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kHazard)
        execid = self.tsp.rvc_find_vehicle(op=2)
        time.sleep(2.3)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kRight)
        assert self.tsp.log_search_remote_vehicle_control("ReqPriorLowFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_寻车等待解闭锁灯提示结束时间超时NotifyTurnLampStatus.sts == kLeft")
    @pytest.mark.full
    def test_OnlyLight_TurnLampMode_timeout_kLeft_caseid_1982664(self):
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kHazard)
        execid = self.tsp.rvc_find_vehicle(op=2)
        time.sleep(2.5)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kLeft)
        assert self.tsp.log_search_remote_vehicle_control("ReqPriorLowFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_寻车等待解闭锁灯提示结束时间超时2.6秒")
    @pytest.mark.full
    def test_OnlyLight_TurnLampMode_timeout_kStop_caseid_1982665(self):
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kLeft)
        time.sleep(0.5)
        execid = self.tsp.rvc_find_vehicle(2)
        time.sleep(2.4)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        assert self.tsp.log_search_remote_vehicle_control("ReqPriorLowFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  
    
    @allure.title("远程控制-RVC_远程寻车控制_闪灯_寻车等待解闭锁灯提示结束时间超时内NotifyTurnLampStatus.sts == kHazard")
    @pytest.mark.full
    def test_OnlyLight_TurnLampMode_kHazard_caseid_1982666(self):
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kLeft)
        execid = self.tsp.rvc_find_vehicle(op=2)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kHazard)
        assert self.tsp.log_search_remote_vehicle_control("ReqPriorLowFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_寻车等待解闭锁灯提示结束时间超时内NotifyTurnLampStatus.sts == kRight")
    @pytest.mark.full
    def test_OnlyLight_TurnLampMode_kRight_caseid_1982667(self):
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kLeft)
        execid = self.tsp.rvc_find_vehicle(op=2)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kRight)
        assert self.tsp.log_search_remote_vehicle_control("ReqPriorLowFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_寻车等待解闭锁灯提示结束时间超时内NotifyTurnLampStatus.sts == kLeft")
    @pytest.mark.full
    def test_OnlyLight_TurnLampMode_kLeft_caseid_1982668(self):
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kRight)
        execid = self.tsp.rvc_find_vehicle(op=2)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kLeft)
        assert self.tsp.log_search_remote_vehicle_control("ReqPriorLowFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_FOTA为UpdateFailedNotDriving")
    @pytest.mark.sanity
    def test_OnlyLight_FOTA_UpdateFailedNotDriving_caseid_1982670(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)
        execid = self.tsp.rvc_find_vehicle(2)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(0.5)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程寻车控制_闪灯_FOTA为Active")
    @pytest.mark.sanity
    def test_OnlyLight_FOTA_Active_caseid_1982671(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        execid = self.tsp.rvc_find_vehicle(2)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(0.5)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_FOTA为Downloadingk")
    @pytest.mark.sanity
    def test_OnlyLight_FOTA_Downloadingk_caseid_1982672(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        execid = self.tsp.rvc_find_vehicle(2)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(0.5)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_FOTA为NewTask")
    @pytest.mark.sanity
    def test_OnlyLight_FOTA_NewTask_caseid_1982673(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        execid = self.tsp.rvc_find_vehicle(2)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(0.5)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程寻车控制_闪灯_FOTA为Query")
    @pytest.mark.sanity
    def test_OnlyLight_FOTA_Query_caseid_1982674(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        execid = self.tsp.rvc_find_vehicle(2)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(0.5)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_FOTA为ROLLBACK")
    @pytest.mark.full
    def test_OnlyLight_FOTAM_ROLLBACK_caseid_1982675(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        execid = self.tsp.rvc_find_vehicle(op=2)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_FOTA为UPDATE")
    @pytest.mark.full
    def test_OnlyLight_FOTAM_UPDATE_caseid_1982676(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_find_vehicle(op=2)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_维修模式True和FOTA为UPDATE")
    @pytest.mark.full
    def test_OnlyLight_mntnmode_True_FOTAM_UPDATE_caseid_1982677(self):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_find_vehicle(op=2)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_维修模式True")
    @pytest.mark.full
    def test_OnlyLight_mntnmode_True_caseid_1982678(self):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        execid = self.tsp.rvc_find_vehicle(op=2)
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_CONVENIENCE和kSeatFrontLeft")
    @pytest.mark.full
    def test_OnlyLight_UsageMode_CONVENIENCE_kSeatFrontLeft_caseid_1982683(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle(op=2)
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(0.5)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程寻车控制_闪灯_Convenience和kSeatFrontRight")
    @pytest.mark.full
    def test_OnlyLight_UsageMode_CONVENIENCE_kSeatFrontRight_caseid_1982682(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,1,0,0,0])
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle(op=2)
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(0.5)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远程寻车控制_闪灯_Convenience和kSeatRearLeft")
    @pytest.mark.full
    def test_OnlyLight_UsageMode_CONVENIENCE_kSeatRearLeft_caseid_1982681(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,1,0,0])
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle(op=2)
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(0.5)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远程寻车控制_闪灯_Convenience和kSeatRearMiddle")
    @pytest.mark.full
    def test_OnlyLight_UsageMode_CONVENIENCE_kSeatRearMiddle_caseid_1982680(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,1,0])
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle(op=2)
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(0.5)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_Convenience和kSeatRearRight")
    @pytest.mark.full
    def test_OnlyLight_UsageMode_CONVENIENCE_kSeatRearRight_caseid_1982679(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,1])
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle(op=2)
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(0.5)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_inactive和kSeatFrontLeft")
    @pytest.mark.sanity
    def test_OnlyLight_UsageMode_INACTIVE_kSeatFrontLeft_caseid_1982684(self):
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle(op=2)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(1)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_GearNA和FOTA为UPDATE")
    @pytest.mark.full
    def test_OnlyLight_Gear_Neut_FOTA_UPDATE_caseid_1982685(self):
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle(op=2)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_GearNA")
    @pytest.mark.full
    def test_OnlyLight_Gear_ManMode_caseid_1982686(self):
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(1)
        self.soa.s2s_set_gear(gear=Gear.Resd1)
        execid = self.tsp.rvc_find_vehicle(op=2)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_GearM")
    @pytest.mark.full
    def test_OnlyLight_Gear_ManMode_caseid_1982687(self):
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle(op=2)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_GearD")
    @pytest.mark.sanity
    def test_OnlyLight_Gear_Drv_caseid_1982688(self):
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle(op=2)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_GearN")
    @pytest.mark.full
    def test_OnlyLight_Gear_Neut_caseid_1982689(self):
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle(op=2)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_GearR")
    @pytest.mark.full
    def test_OnlyLight_Gear_Rvs_caseid_1982690(self):
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle(op=2)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_Driving")
    @pytest.mark.sanity
    def test_OnlyLight_UsageMode_DRIVING_caseid_1982691(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle(op=2)
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_Active")
    @pytest.mark.sanity
    def test_OnlyLight_UsageMode_ACTIVE_caseid_1982692(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle(op=2)
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_Convenience")
    @pytest.mark.smoke
    def test_OnlyLight_Convenience_caseid_1982693(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kLeft)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle(2)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control('StartOK', flage=0,execid=execid)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(0.5)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control("Success", flage=2,execid=execid)

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_INACTIVE")
    @pytest.mark.smoke
    def test_OnlyLight_INACTIVE_caseid_1982694(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kLeft)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle(2)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control('StartOK', flage=0,execid=execid)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(0.5)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control("Success", flage=2,execid=execid)

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_DYNO")
    @pytest.mark.full
    def test_OnlyLight_CarMode_DYNO_caseid_1982695(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle(op=2)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_CRASH")
    @pytest.mark.full
    def test_OnlyLight_CarMode_CRASH_caseid_1982696(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle(op=2)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_FACTORY")
    @pytest.mark.full
    def test_OnlyLight_CarMode_FACTORY_caseid_1982697(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle(op=2)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_TRANSPORT")
    @pytest.mark.full
    def test_OnlyLight_CarMode_TRANSPORT_caseid_1982698(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle(op=2)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_ABANDONED")
    @pytest.mark.smoke
    def test_OnlyLight_ABANDONED_caseid_1982699(self):
        self.io.tcam_kl15_down()  
        self.bus_comm.pause_all_bus_send()  
        sleep(180) # 避免其他case的指令未执行结束导致TCAM依旧保持唤醒
        self.mix.tcam_network_sleep()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        time.sleep(0.5)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC27,signal_value=NMSts.valid,timeout=30)
        execid = self.tsp.rvc_find_vehicle(2)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control('StartOK',flage=0,execid=execid)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(0.5)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control('Success',flage=2,execid=execid)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,timeout=1)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC27,timeout=1)

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_SOAFail")
    @pytest.mark.full
    def test_OnlyLight_SOAFail_caseid_1982700(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.soa_partner.stop_single_partner("KeyService_server")
        time.sleep(10)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        execid = self.tsp.rvc_find_vehicle(op=2)
        time.sleep(5)
        assert self.tsp.log_search_remote_vehicle_control("SOAFail",execid=execid,num=60),f"TCAM远程控制上报到车云的结果校验失败"      
        self.soa.soa_partner.start_single_partner(service="KeyService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("KeyService_server",timeout=30)     

    @allure.title("远程控制-RVC_远程寻车控制_连续二次远程寻车闪灯")
    @pytest.mark.sanity
    def test_OnlyLight_two_OnlyLight_caseid_1982704(self):
        execid1 = self.tsp.rvc_find_vehicle(op=2)
        execid2 = self.tsp.rvc_find_vehicle(op=2)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid2),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)   

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_等待远程寻车开始时间超时sts=sts=kFail")
    @pytest.mark.full
    def test_hornLight_CarLocalTraceActiveStatus_timeout_kFail_caseid_1982705(self):
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        time.sleep(10.6)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(1)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kFail)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail", execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_等待远程寻车开始时间超时sts=kIdle")
    @pytest.mark.full
    def test_hornLight_CarLocalTraceActiveStatus_timeout_kIdle_caseid_1982706(self):
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        time.sleep(10.6)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(1)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail", execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_等待远程寻车开始时间超时sts=kSuccess")
    @pytest.mark.full
    def test_hornLight_CarLocalTraceActiveStatus_timeout_kSuccess_caseid_1982707(self):
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(12)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_等待远程寻车开始时间超时内sts=kFail")
    @pytest.mark.full
    def test_hornLight_CarLocalTraceActiveStatus_kFail_caseid_1982708(self):
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(9)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kFail)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_等待远程寻车开始时间超时内sts=kIdle")
    @pytest.mark.sanity
    def test_hornLight_CarLocalTraceActiveStatus_kSuccess_caseid_1982709(self):
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        time.sleep(5)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(8)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_等待远程寻车开始时间超时后sts=kSuccess")
    @pytest.mark.full
    def test_hornLight_CarLocalTraceActiveStatus_timeout_kSuccess_caseid_1982710(self):
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        time.sleep(11)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_等待远程寻车开始时间超时后sts=kFail")
    @pytest.mark.full
    def test_hornLight_CarLocalTraceActiveStatus_timeout_kFail_caseid_1982711(self):
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        time.sleep(11)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kFail)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_等待远程寻车开始时间超时后sts=kIdle")
    @pytest.mark.full
    def test_hornLight_CarLocalTraceActiveStatus_timeout_kIdle_caseid_1982712(self):
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        time.sleep(11)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_等待远程寻车开始时间超时内sts=kFail")
    @pytest.mark.full
    def test_hornLight_CarLocalTraceActiveStatus_kFail_caseid_1982713(self):
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        time.sleep(2)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kFail)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_等待远程寻车开始时间超时内sts=kIdle")
    @pytest.mark.full
    def test_hornLight_CarLocalTraceActiveStatus_kIdle_caseid_1982714(self):
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        time.sleep(1)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_寻车等待解闭锁灯提示结束时间超时NotifyTurnLampStatus.sts == kHazard")
    @pytest.mark.full
    def test_hornLight_TurnLampMode_timeout_kHazard_caseid_1982715(self):
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kRight)
        execid = self.tsp.rvc_find_vehicle()
        time.sleep(2.6)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kHazard)
        assert self.tsp.log_search_remote_vehicle_control("ReqPriorLowFail",execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_寻车等待解闭锁灯提示结束时间超时NotifyTurnLampStatus.sts == kRight")
    @pytest.mark.full
    def test_hornLight_TurnLampMode_timeout_kRight_caseid_1982716(self):
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kRight)
        execid = self.tsp.rvc_find_vehicle()
        time.sleep(2.6)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kRight)
        assert self.tsp.log_search_remote_vehicle_control("ReqPriorLowFail",execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_寻车等待解闭锁灯提示结束时间超时NotifyTurnLampStatus.sts == kLeft")
    @pytest.mark.full
    def test_hornLight_TurnLampMode_timeout_kLeft_caseid_1982717(self):
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kLeft)
        execid = self.tsp.rvc_find_vehicle()
        time.sleep(2.6)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kLeft)
        assert self.tsp.log_search_remote_vehicle_control("ReqPriorLowFail",execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_寻车等待解闭锁灯提示结束时间超时2.6秒")
    @pytest.mark.full
    def test_hornLight_TurnLampMode_timeout_kStop_caseid_1982718(self):
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kLeft)
        time.sleep(0.5)
        execid = self.tsp.rvc_find_vehicle()
        time.sleep(2.8)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        assert self.tsp.log_search_remote_vehicle_control("ReqPriorLowFail",execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_寻车等待解闭锁灯提示结束时间超时内先发kIdle再发kSuccess")
    @pytest.mark.sanity
    def test_hornLight_CarLoctrActvnSts_kIdle_kSuccess_caseid_1982719(self):
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        time.sleep(1)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        time.sleep(1)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(2)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_寻车等待解闭锁灯提示结束时间超时内NotifyTurnLampStatus.sts == kHazard")
    @pytest.mark.full
    def test_hornLight_TurnLampMode_kHazard_caseid_1982720(self):
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kHazard)
        sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kHazard)
        assert self.tsp.log_search_remote_vehicle_control("ReqPriorLowFail", execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_寻车等待解闭锁灯提示结束时间超时内NotifyTurnLampStatus.sts == kRight")
    @pytest.mark.full
    def test_hornLight_TurnLampMode_kRight_caseid_1982721(self):
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kRight)
        sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kRight)
        assert self.tsp.log_search_remote_vehicle_control("ReqPriorLowFail", execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_等待远程寻车开始时间超时内先发success再发kFail")
    @pytest.mark.sanity
    def test_hornLight_CarLoctrActvnSts_kSuccess_kFail_caseid_1982722(self):
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        time.sleep(1)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(2)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kFail)
        time.sleep(2)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_等待远程寻车开始时间超时内先发kFail再发success")
    @pytest.mark.sanity
    def test_hornLight_CarLoctrActvnSts_kFail_kSuccess_caseid_1982723(self):
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        time.sleep(1)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        time.sleep(2)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kFail)
        time.sleep(2)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(2)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success", execid),f"TCAM远程控制上报到车云的结果校验失败"        

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_寻车等待解闭锁灯提示结束时间超时内NotifyTurnLampStatus.sts == kLeft")
    @pytest.mark.full
    def test_hornLight_TurnLampMode_kLeft_caseid_1982724(self):
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kLeft)
        sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kLeft)
        assert self.tsp.log_search_remote_vehicle_control("ReqPriorLowFail", execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_寻车等待解闭锁灯先发stop再发kHazard")
    @pytest.mark.sanity
    def test_hornLight_TurnLampStatus_stop_kHazard_caseid_1982725(self):
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        time.sleep(1)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kHazard)
        time.sleep(0.5)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制- RVC_远程寻车控制_鸣笛闪灯_寻车等待解闭锁灯先发kHazard再发stop")
    @pytest.mark.sanity
    def test_hornLight_TurnLampStatus_kHazard_waittime_caseid_1982726(self):
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kHazard)
        time.sleep(0.5)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        time.sleep(1)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(0.5)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_寻车等待解闭锁灯先发kRight再发stop")
    @pytest.mark.sanity
    def test_hornLight_TurnLampStatus_kRight_waittime_caseid_1982727(self):
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kRight)
        time.sleep(0.5)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        time.sleep(1.5)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(0.5)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制- RVC_远程寻车控制_鸣笛闪灯_寻车等待解闭锁灯先发kLeft再发stop")
    @pytest.mark.sanity
    def test_hornLight_TurnLampStatus_kLeft_waittime_caseid_1982728(self):
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kLeft)
        time.sleep(0.5)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        time.sleep(1.5)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(0.5)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_寻车等待解闭锁灯提示结束时间超时内2.2秒")
    @pytest.mark.sanity
    def test_hornLight_TurnLampStatus_waittime_2s_caseid_1982729(self):
        execid = self.tsp.rvc_find_vehicle()
        time.sleep(1.9)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_FOTA为UpdateFailedNotDriving")
    @pytest.mark.sanity
    def test_hornLight_FOTA_UpdateFailedNotDriving_caseid_1982730(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_FOTA为Active")
    @pytest.mark.sanity
    def test_hornLight_FOTA_Active_caseid_1982731(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_FOTA为Downloadingk")
    @pytest.mark.sanity
    def test_hornLight_FOTA_Downloadingk_caseid_1982732(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_FOTA为NewTask")
    @pytest.mark.sanity
    def test_hornLight_FOTA_NewTask_caseid_1982733(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid),f"TCAM远程控制上报到车云的结果校验失败" 


    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_FOTA为Query")
    @pytest.mark.sanity
    def test_hornLight_FOTA_Query_caseid_1982734(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid),f"TCAM远程控制上报到车云的结果校验失败" 


    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_FOTA为ROLLBACK")
    @pytest.mark.full
    def test_hornLight_FOTAM_ROLLBACK_caseid_1982735(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_FOTA为UPDATE")
    @pytest.mark.full
    def test_hornLight_FOTAM_UPDATE_caseid_1982736(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid),f"TCAM远程控制上报到车云的结果校验失败"      

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_维修模式True和FOTA为UPDATE")
    @pytest.mark.full
    def test_hornLight_mntnmode_True_FOTAM_UPDATE_caseid_1982737(self):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_维修模式True")
    @pytest.mark.full
    def test_hornLight_mntnmode_True_caseid_1982738(self):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_Convenience和kSeatRearRight")
    @pytest.mark.full
    def test_hornLight_UsageMode_CONVENIENCE_kSeatRearRight_caseid_1982739(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,1])
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid),f"TCAM远程控制上报到车云的结果校验失败"    
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_Convenience和kSeatRearMiddle")
    @pytest.mark.full
    def test_hornLight_UsageMode_CONVENIENCE_kSeatRearMiddle_caseid_1982740(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,1,0])
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid),f"TCAM远程控制上报到车云的结果校验失败"    
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_Convenience和kSeatRearLeft")
    @pytest.mark.full
    def test_hornLight_UsageMode_CONVENIENCE_kSeatRearLeft_caseid_1982741(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,1,0,0])
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid),f"TCAM远程控制上报到车云的结果校验失败"    
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_Convenience和kSeatFrontRight")
    @pytest.mark.full
    def test_hornLight_UsageMode_CONVENIENCE_kSeatFrontRight_caseid_1982742(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,1,0,0,0])
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid),f"TCAM远程控制上报到车云的结果校验失败"    
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_CONVENIENCE和kSeatFrontLeft")
    @pytest.mark.full
    def test_hornLight_UsageMode_CONVENIENCE_kSeatFrontLeft_caseid_1982743(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid),f"TCAM远程控制上报到车云的结果校验失败"    
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_inactive和kSeatFrontLeft")
    @pytest.mark.sanity
    def test_hornLight_UsageMode_INACTIVE_kSeatFrontLeft_caseid_1982744(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(1)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_GearNA和FOTA为UPDATE")
    @pytest.mark.full
    def test_hornLight_Gear_Resd1_FOTA_UPDATE_caseid_1982745(self):
        self.soa.s2s_set_gear(gear=Gear.Resd1)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_GearNA")
    @pytest.mark.full
    def test_hornLight_Gear_ManMode_caseid_1982746(self):
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(1)
        self.soa.s2s_set_gear(gear=Gear.Resd1)
        execid = self.tsp.rvc_find_vehicle()
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid),f"TCAM远程控制上报到车云的结果校验失败"       

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_GearM")
    @pytest.mark.full
    def test_hornLight_Gear_ManMode_caseid_1982747(self):
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_GearD")
    @pytest.mark.full
    def test_hornLight_Gear_Drv_caseid_1982748(self):
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_GearN")
    @pytest.mark.full
    def test_hornLight_Gear_Neut_caseid_1982749(self):
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_GearR")
    @pytest.mark.full
    def test_hornLight_Gear_Rvs_caseid_1982750(self):
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_Driving")
    @pytest.mark.full
    def test_hornLight_UsageMode_DRIVING_caseid_1982751(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_Active")
    @pytest.mark.full
    def test_hornLight_UsageMode_ACTIVE_caseid_1982752(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_Convenience")
    @pytest.mark.smoke
    def test_hornLight_Convenience_caseid_1982753(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(1)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kLeft)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(1)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success", execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_休眠")
    @pytest.mark.sanity
    def test_hornLight_INACTIVE_hibernate_caseid_1982754(self):
        self.io.tcam_kl15_down()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kLeft)
        self.bus_comm.pause_all_bus_send()
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        time.sleep(0.5)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 15)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(0.5)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.mix.check_tcam_sleep(timeout=190) == True, 'TCAM远控执行完成之后休眠检查失败'

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_INACTIVE")
    @pytest.mark.smoke
    def test_hornLight_INACTIVE_caseid_1982755(self):
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kLeft)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        time.sleep(0.5)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 15)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(0.5)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_DYNO")
    @pytest.mark.full
    def test_hornLight_CarMode_DYNO_caseid_1982756(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail", execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_CRASH")
    @pytest.mark.full
    def test_hornLight_CarMode_CRASH_caseid_1982757(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail", execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_FACTORY")
    @pytest.mark.full
    def test_hornLight_CarMode_FACTORY_caseid_1982758(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail", execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_TRANSPORT")
    @pytest.mark.full
    def test_hornLight_CarMode_TRANSPORT_caseid_1982759(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(1)
        execid = self.tsp.rvc_find_vehicle()
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail", execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯ABANDONED")
    @pytest.mark.smoke
    def test_OnlyLight_ABANDONED_caseid_1982760(self):
        self.io.tcam_kl15_down()  
        self.bus_comm.pause_all_bus_send()  
        sleep(180) # 避免其他case的指令未执行结束导致TCAM依旧保持唤醒
        self.mix.tcam_network_sleep()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        time.sleep(0.5)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC27,signal_value=NMSts.valid,timeout=30)
        execid = self.tsp.rvc_find_vehicle()
        self.tsp.check_async_log_search_result_from_remote_vehicle_control('StartOK',execid=execid,flage=0)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetCarLocalTraceRequest_req(carloctr_req=CarLocalTraceReq.kHornLiReq,timeout = 10)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kSuccess)
        time.sleep(0.5)
        self.soa.notify_NotifyCarLoctrActvnSts(cartrace_sts=CarLocalTraceActiveStatus.kIdle)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control('Success',execid=execid,flage=2)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,timeout=1)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC27,timeout=1)


    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_SOAFail")
    @pytest.mark.full
    def test_hornLight_SOAFail_caseid_1982761(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.soa_partner.stop_single_partner("KeyService_server")
        time.sleep(2)
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        execid = self.tsp.rvc_find_vehicle()
        assert self.tsp.log_search_remote_vehicle_control("SOAFail",execid,num=60),f"TCAM远程控制上报到车云的结果校验失败"      
        self.soa.soa_partner.start_single_partner(service="KeyService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("KeyService_server",timeout=30)

    @allure.title("远程控制-RVC_远程寻车控制_闪灯_ABANDONED_TelmFctReq")
    @pytest.mark.full
    def test_OnlyLight_ABANDONED_TelmFctReq_caseid_1982762(self):
        self.io.tcam_kl15_down()  
        self.bus_comm.pause_all_bus_send()  
        sleep(180) # 避免其他case的指令未执行结束导致TCAM依旧保持唤醒
        logger.info(f'signal_list : {self.bus_comm.ipdu.get_check_results()}')
        self.mix.tcam_network_sleep()
        self.bus_comm.check_signal_thread_start("connectivitycanfd","TcamConnectivityFr35", "TelmFctReq", timeout=10)
        execid = self.tsp.rvc_find_vehicle(2)
        result_ori_1 = self.bus_comm.check_signal_thread_stop("TelmFctReq",timeout=13)
        logger.info(f'监控到的数据： {result_ori_1}')
        result_1 = check_signal_num(result_ori_1,1)
        frame_times = result_1[0]
        duration_time = result_1[1]
        logger.info(f"持续发送{frame_times}帧，持续时间为{duration_time}s")
        assert frame_times==25, f"检查休眠唤醒后TelmFctReq发送失败"
        sleep(10)

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_ABANDONED_TelmFctReq")
    @pytest.mark.full
    def test_hornLight_ABANDONED_TelmFctReq_caseid_1982763(self):
        self.io.tcam_kl15_down()  
        self.bus_comm.pause_all_bus_send()  
        sleep(180) # 避免其他case的指令未执行结束导致TCAM依旧保持唤醒
        logger.info(f'signal_list : {self.bus_comm.ipdu.get_check_results()}')
        self.mix.tcam_network_sleep()
        self.bus_comm.check_signal_thread_start("connectivitycanfd","TcamConnectivityFr35", "TelmFctReq", timeout=10)
        execid = self.tsp.rvc_find_vehicle()
        result_ori_1 = self.bus_comm.check_signal_thread_stop("TelmFctReq",13)
        logger.info(f'监控到的数据： {result_ori_1}')
        result_1 = check_signal_num(result_ori_1,1)
        frame_times = result_1[0]
        duration_time = result_1[1]
        logger.info(f"持续发送{frame_times}帧，持续时间为{duration_time}s")
        assert frame_times==25, f"检查休眠唤醒后TelmFctReq发送失败"
        sleep(10)

    @allure.title("远程控制-RVC_远程寻车控制_鸣笛闪灯_NetWakeFail")
    @pytest.mark.full
    def test_OnlyLight_ABANDONED_caseid_1982764(self):
        self.io.tcam_kl15_down()  
        self.bus_comm.pause_all_bus_send()  
        sleep(180) # 避免其他case的指令未执行结束导致TCAM依旧保持唤醒
        self.mix.tcam_network_sleep()
        self.soa.notify_NotifyTurnLampStatus(priority=0,turnlamp_mode=TurnLampMode.kStop)
        time.sleep(0.5)
        execid = self.tsp.rvc_find_vehicle()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.tsp.log_search_remote_vehicle_control('NetWakeFail',execid=execid)


    @allure.title("远程控制-RVC_远程寻车控制_连续二次远程寻车鸣笛闪灯")
    @pytest.mark.full
    def test_hornLight_two_hornLight_caseid_1982765(self):
        execid1 = self.tsp.rvc_find_vehicle()
        execid2 = self.tsp.rvc_find_vehicle()
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid2),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)

    @allure.title("远程控制-RVC_远程寻车控制_ReqFail")
    @pytest.mark.full
    def test_hornLight_ReqFail_caseid_1982766(self):
        execid = self.tsp.rvc_find_vehicle(op=-1)
        assert self.tsp.log_search_remote_vehicle_control("ReqFail",execid),f"TCAM远程控制上报到车云的结果校验失败"


# pytest -vs -p no:warnings remote_control/basic_remote_control/test_car_trace.py
