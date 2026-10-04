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

@allure.feature("互联服务/远程控制/远程车窗控制")
@allure.story("远程车窗控制")
class TestWindowCtrl(TestABCBase):
    def before_class(self, ecu):

        self.soa.update(["HighVoltageService_server","VehicleModeService_server", "FotaMasterService_server",
                    "VehicleSetStatusService_server", "ChassisService_server", 
                    "VehicleTimeService_server", "SeatService_server",
                    "WindowAppService_server","WindowService_server"])
        self.mix.start_get_request_and_send_response_to_tcam_thread(["VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server","SeatService_server",
                         "HighVoltageService_server", "VehicleTimeService_server",
                          ])
        sleep(30)

    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(1)
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))
        
    def after_each_func(self, ecu):
        if ecu.testresult == 'Failure':
            logger.info('用例执行失败')
            sleep(12)
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        time.sleep(1)

    def after_class(self, ecu):
        self.mix.stop_get_request_and_send_response_to_tcam_thread()

    @allure.title("远程控制-RVC_远程车窗控制_关ABANDONED")
    @pytest.mark.smoke
    def test_close_window_abandoned_caseid_1982466(self, ecu):
        self.io.tcam_kl15_down()
        self.bus_comm.pause_all_bus_send()
        sleep(60)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0) 
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC37,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.resume_all_bus_send() 
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=15)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_关_INACTIVE")
    @pytest.mark.smoke
    def test_close_window_inactive_caseid_1982461(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
            
    @allure.title("远程控制-RVC_远程车窗控制_关_Convenience")
    @pytest.mark.smoke
    def test_close_window_convenience_caseid_1982457(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_关_等待车窗动作完成9.9秒")
    @pytest.mark.sanity
    def test_close_window_waittime_9s_caseid_1982458(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts()
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        time.sleep(9.9)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
    
    @allure.title("远程控制-RVC_远程车窗控制_关_四个车窗状态position=100关窗")
    @pytest.mark.sanity
    def test_close_window_position_100_caseid_1982431(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts()
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_关_四个车窗状态position=0关窗")
    @pytest.mark.sanity
    def test_close_window_position_0_caseid_1982430(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_关_四个车窗状态position=4关窗")
    @pytest.mark.sanity
    def test_close_window_position_4_caseid_1982429(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts(positions = [4,4,4,4])
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_关_四个车窗状态position=16关窗")
    @pytest.mark.sanity
    def test_close_window_position_16_caseid_1982428(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts(positions=[16,16,16,16])
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
                
    @allure.title("远程控制-RVC_远程车窗控制_关_FOTA为Query")
    @pytest.mark.sanity
    def test_close_window_FOTA_Query_caseid_1982436(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
    
    @allure.title("远程控制-RVC_远程车窗控制_关_FOTA为NewTask")
    @pytest.mark.sanity
    def test_close_window_FOTA_NewTask_caseid_1982435(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_关_FOTA为Downloadingk")
    @pytest.mark.sanity
    def test_close_window_FOTA_Downloadingk_caseid_1982434(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_关_FOTA为Active")
    @pytest.mark.sanity
    def test_close_window_FOTA_Active_caseid_1982433(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_关_FOTA为UpdateFailedNotDriving")
    @pytest.mark.sanity
    def test_close_window_FOTA_UpdateFailedNotDriving_caseid_1982432(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_开_ABANDONED")
    @pytest.mark.smoke
    def test_open_window_abandoned_caseid_1982412(self, ecu):
        self.io.tcam_kl15_down()
        self.bus_comm.pause_all_bus_send()
        sleep(60)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_window_control() 
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC37,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.resume_all_bus_send() 
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100},timeout=15)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
    
    @allure.title("远程控制-RVC_远程车窗控制_开_INACTIVE")
    @pytest.mark.smoke
    def test_open_window_inactive_caseid_1982407(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()  
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100},timeout=10)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_开_Convenience")
    @pytest.mark.smoke
    def test_open_window_convenience_caseid_1982406(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()  
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100},timeout=10)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_开_FOTA为Query")
    @pytest.mark.sanity
    def test_open_window_FOTA_Query_caseid_1982385(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)        
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()  
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100},timeout=10)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远程车窗控制_开_FOTA为NewTask")
    @pytest.mark.sanity
    def test_open_window_FOTA_NewTask_caseid_1982384(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)      
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()  
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100},timeout=10)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远程车窗控制_开_FOTA为Downloadingk")
    @pytest.mark.sanity
    def test_open_window_FOTA_Downloadingk_caseid_1982383(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()  
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100},timeout=10)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远程车窗控制_开_FOTA为ACTIVE")
    @pytest.mark.sanity
    def test_open_window_FOTA_ACTIVE_caseid_1982382(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()  
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100},timeout=10)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_开_FOTA为UpdateFailedNotDriving")
    @pytest.mark.sanity
    def test_open_window_FOTA_UpdateFailedNotDriving_caseid_1982381(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)  
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()  
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100},timeout=10)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_开_四个车窗状态position=100开窗")
    @pytest.mark.sanity
    def test_open_window_position_100_caseid_1982380(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()  
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100},timeout=10)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程车窗控制_开_四个车窗状态position=0开窗")
    @pytest.mark.sanity
    def test_open_window_position_0_open_100_caseid_1982379(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()  
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100},timeout=10)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程车窗控制_开_四个车窗状态position=4开窗")
    @pytest.mark.sanity
    def test_open_window_position_4_open_100_caseid_1982378(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts(positions = [4,4,4,4])
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()  
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100},timeout=10)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程车窗控制_开_四个车窗状态position=16开窗")
    @pytest.mark.sanity
    def test_open_window_position_16_open_100_caseid_1982377(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts(positions=[16,16,16,16])
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()  
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100}, timeout=10)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"          
        
    @allure.title("远程控制-RVC_远程车窗控制_开_3个车窗状态position=16开窗")
    @pytest.mark.sanity
    def test_open_window_position_three_16_open_100_caseid_1982376(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts(positions = [16,16,16,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()  
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100}, timeout=10)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程车窗控制_开_2个车窗状态position=16开窗")
    @pytest.mark.sanity
    def test_open_window_position_two_16_open_100_caseid_1982375(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts(positions = [16,16,0,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()  
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100}, timeout=10)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程车窗控制_开_1个车窗状态position=16开窗")
    @pytest.mark.sanity
    def test_open_window_position_one_16_open_100_caseid_1982374(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts(positions = [16,0,0,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()  
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100}, timeout=10)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程车窗控制_开_下发1个车窗position=4开窗")
    @pytest.mark.sanity
    def test_open_window_position_one_4_open_100_caseid_1982373(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=4) 
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":4},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100}, timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [4,100,100,100])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  


    @allure.title("远程控制-RVC_远程车窗控制_开_下发1个车窗position=8开窗")
    @pytest.mark.sanity
    def test_open_window_position_one_8_open_100_caseid_1982372(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=8) 
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":8},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100}, timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [8,100,100,100])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"          

    @allure.title("远程控制-RVC_远程车窗控制_开_下发1个车窗position=12开窗")
    @pytest.mark.sanity
    def test_open_window_position_one_12_open_100_caseid_1982371(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=12) 
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":12},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100}, timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [12,100,100,100])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程车窗控制_开_下发2个车窗position=12开窗")
    @pytest.mark.sanity
    def test_open_window_position_two_12_open_100_caseid_1982369(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=12, win_fr=12) 
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":12},{"id":1,"position":12},{"id":2,"position":100},{"id":3,"position":100}, timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [12,12,100,100])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   
        
    @allure.title("远程控制-RVC_远程车窗控制_开_下发2个车窗position不同开窗")
    @pytest.mark.sanity
    def test_open_window_position_oen_8_two_12_open_100_caseid_1982368(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=8, win_fr=12) 
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":8},{"id":1,"position":12},{"id":2,"position":100},{"id":3,"position":100}, timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [8,12,100,100])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"          
        
    @allure.title("远程控制-RVC_远程车窗控制_开_下发3个车窗position=12开窗")
    @pytest.mark.sanity
    def test_open_window_position_three_12_open_100_caseid_1982367(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=12, win_fr=12, win_rl=12) 
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":12},{"id":1,"position":12},{"id":2,"position":12},{"id":3,"position":100}, timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [12,12,12,100])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
        
    @allure.title("远程控制-RVC_远程车窗控制_开_下发3个车窗position不同开窗")
    @pytest.mark.sanity
    def test_open_window_position_three_different_open_100_caseid_1982366(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=8, win_fr=12, win_rl=16) 
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":8},{"id":1,"position":12},{"id":2,"position":16},{"id":3,"position":100}, timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [8,12,16,100])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程车窗控制_开_下发4个车窗position=12开窗")
    @pytest.mark.sanity
    def test_open_window_position_three_different_open_100_caseid_1982365(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=12, win_fr=12, win_rl=12,win_rr=12) 
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":12},{"id":1,"position":12},{"id":2,"position":12},{"id":3,"position":12}, timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [12,12,12,12])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程车窗控制_开_下发4个车窗position不同开窗")
    @pytest.mark.sanity
    def test_open_window_position_oen_0_four_different_open_100_caseid_1982364(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=4, win_rl=8, win_rr=12) 
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":4},{"id":2,"position":8},{"id":3,"position":12}, timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [0,4,8,12])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程车窗控制_开_下发4个车窗position相同开窗")
    @pytest.mark.sanity
    def test_open_window_position_four_different_open_100_caseid_1982363(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=16, win_fr=16, win_rl=16, win_rr=16) 
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":16},{"id":1,"position":16},{"id":2,"position":16},{"id":3,"position":16}, timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [16,16,16,16])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程车窗控制_开_下发4个车窗position不同开窗")
    @pytest.mark.sanity
    def test_open_window_position_four_different_open_100_caseid_1982362(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=8, win_fr=12, win_rl=16, win_rr=20) 
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":8},{"id":1,"position":12},{"id":2,"position":16},{"id":3,"position":20}, timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [8,12,16,20])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   
        
    @allure.title("远程控制-RVC_远程车窗控制_开_超时时间内NotifyPosition值相同")
    @pytest.mark.sanity
    def test_open_window_position_four_different_open_100_caseid_1982361(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control() 
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100}, timeout=10)
        time.sleep(9)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程车窗控制_开_等待车窗动作完成的时间先发异常再发正常")
    @pytest.mark.sanity
    def test_open_window_position_four_different_open_100_caseid_1982359(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control() 
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100}, timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        time.sleep(2)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      
        
    @allure.title("远程控制-RVC_远程车窗控制_开_等待车窗动作完成的时间先发正常再发异常")
    @pytest.mark.sanity
    def test_open_window_position_four_different_open_100_caseid_1982358(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control() 
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100}, timeout=10)
        self.soa.notify_WindowPosition_sts()
        time.sleep(2)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程车窗控制_ReqFail")
    @pytest.mark.full
    def test_open_window_ReqFail_caseid_1982474(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=-1) 
        assert self.tsp.log_search_remote_vehicle_control("ReqFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"          
    
    @allure.title("远程控制-RVC_远程车窗控制_开_超时时间内NotifyPosition值不相同")
    @pytest.mark.full
    def test_open_window_NotifyPosition_different_caseid_1982360(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        execid = self.tsp.rvc_window_control() 
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100}, timeout=10)
        time.sleep(9)
        self.soa.notify_WindowPosition_sts(positions = [80,80,80,80])
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     
        
    @allure.title("远程控制-RVC_远程车窗控制_关_等待车窗动作完成10.5秒")
    @pytest.mark.full
    def test_close_window_NotifyPosition_10s_waittime_caseid_1982459(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0}, timeout=10)
        time.sleep(10.5)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     

    @allure.title("远程控制-RVC_远程车窗控制_连续二次远程车窗关")
    @pytest.mark.full
    def test_close_window_two_close_caseid_1982472(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts()
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)    
        
    @allure.title("远程控制-RVC_远程车窗控制_关_TRANSPORT")
    @pytest.mark.full
    def test_close_window_CarMode_TRANSPORT_caseid_1982465(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程车窗控制_关_FACTORY")
    @pytest.mark.full
    def test_close_window_CarMode_FACTORY_caseid_1982464(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程车窗控制_关_CRASH")
    @pytest.mark.full
    def test_close_window_CarMode_CRASH_caseid_1982463(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程车窗控制_关_DYNO")
    @pytest.mark.full
    def test_close_window_CarMode_DYNO_caseid_1982462(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     
         
    @allure.title("远程控制-RVC_远程车窗控制_关_Active")
    @pytest.mark.full
    def test_close_window_UsageMode_ACTIVE_caseid_1982456(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程车窗控制_关_Driving")
    @pytest.mark.full
    def test_close_window_UsageMode_DRIVING_caseid_1982455(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程车窗控制_关_FACTORY和Driving")
    @pytest.mark.full
    def test_close_window_FACTORY_UsageMode_DRIVING_caseid_1982454(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程车窗控制_关_GearR")
    @pytest.mark.full
    def test_close_window_Gear_Rvs_caseid_1982453(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程车窗控制_关_Neut")
    @pytest.mark.full
    def test_close_window_Gear_Neut_caseid_1982452(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-VC_远程车窗控制_关_GearD")
    @pytest.mark.full
    def test_close_window_Gear_Drv_caseid_1982451(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程车窗控制_关_GearM")
    @pytest.mark.full
    def test_close_window_Gear_ManMode_caseid_1982450(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程车窗控制_关_GearNA")
    @pytest.mark.full
    def test_close_window_Gear_GearNA_caseid_1982449(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        self.soa.s2s_set_gear(gear=Gear.Resd1)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程车窗控制_关_GearNA和FOAT为UPDATE")
    @pytest.mark.full
    def test_close_window_FOTA_UPDATE_GearNA_caseid_1982448(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.s2s_set_gear(gear=Gear.Resd1)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      

    @allure.title("远程控制-RVC_远程车窗控制_关_Active和GearR")
    @pytest.mark.full
    def test_close_window_UsageMode_ACTIVE_GearR_caseid_1982447(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      

    @allure.title("远程控制-RVC_远程车窗控制_关_Convenience和GearR")
    @pytest.mark.full
    def test_close_window_UsageMode_CONVENIENCE_GearR_caseid_1982446(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程车窗控制_关_Convenience和kSeatFrontLeft")
    @pytest.mark.full
    def test_close_window_UsageMode_CONVENIENCE_kSeatFrontLeft_caseid_1982445(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程车窗控制_关_Convenience和kSeatFrontRight")
    @pytest.mark.full
    def test_close_window_UsageMode_CONVENIENCE_kSeatFrontRight_caseid_1982444(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,1,0,0,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_关_Convenience和kSeatRearLeft")
    @pytest.mark.full
    def test_close_window_UsageMode_CONVENIENCE_kSeatRearLeft_caseid_1982443(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,1,0,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_关_Convenience和kSeatRearMiddle")
    @pytest.mark.full
    def test_close_window_UsageMode_CONVENIENCE_kSeatRearMiddle_caseid_1982442(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,1,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_关_Convenience和kSeatRearRight")
    @pytest.mark.full
    def test_close_window_UsageMode_CONVENIENCE_kSeatRearRight_caseid_1982441(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,1])
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_关_维修模式True")
    @pytest.mark.full
    def test_close_window_mntnmode_True_caseid_1982440(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程车窗控制_关_维修模式True和FOTA为UPDATE")
    @pytest.mark.full
    def test_close_window_mntnmode_True_FOTAM_UPDATE_caseid_1982439(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程车窗控制_关_FOTA为UPDATE")
    @pytest.mark.full
    def test_close_window_FOTAM_UPDATE_caseid_1982438(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程车窗控制_关_FOTA为ROLLBACK")
    @pytest.mark.full
    def test_close_window_FOTAM_ROLLBACK_caseid_1982437(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程车窗控制_关_超时时间内NotifyPosition值相同")
    @pytest.mark.sanity
    def test_close_window_NotifyPosition_same_caseid_1982423(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts()        
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        time.sleep(9)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_关_车窗状态1个车窗position=16关窗")
    @pytest.mark.sanity
    def test_close_window_NotifyPosition16_caseid_1982424(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts(positions = [16,16,16,16])      
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        time.sleep(9)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_关_车窗状态2个车窗position=16关窗")
    @pytest.mark.sanity
    def test_close_window_NotifyPosition16_caseid_1982425(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts(positions = [16,16,0,0])     
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        time.sleep(9)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远程车窗控制_关_车窗状态3个车窗position=16关窗")
    @pytest.mark.sanity
    def test_close_window_NotifyPosition16_caseid_1982426(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts(positions = [16,16,16,0])     
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        time.sleep(9)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_关_四个车窗状态position不同关窗")
    @pytest.mark.sanity
    def test_close_window_NotifyPosition_different_caseid_1982427(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts(positions = [4,8,12,16])    
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        time.sleep(9)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_关_超时时间内NotifyPosition值不同")
    @pytest.mark.sanity
    def test_close_window_NotifyPosition_timeout_different_caseid_1982422(self, ecu):
        # 设置总线通信模式为INACTIVE
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        # 通知车窗位置状态
        self.soa.notify_WindowPosition_sts()
        # 等待0.5秒
        time.sleep(0.5)
        # 控制车窗位置
        execid = self.tsp.rvc_window_control(win_fl=4, win_fr=4, win_rl=4, win_rr=4)
        # 检查是否发送了设置特定车窗位置的请求，并设置超时时间为10秒
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":4},{"id":1,"position":4},{"id":2,"position":4},{"id":3,"position":4},timeout=10)
        # 等待9秒
        time.sleep(9)
        # 通知车窗位置状态，并设置车窗位置为[8,8,8,8]
        self.soa.notify_WindowPosition_sts(positions = [8,8,8,8])
        # 断言日志中是否存在"DelayFail"，如果不存在，则测试失败并抛出异常
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
           
    @allure.title("远程控制-等待车窗动作完成的时间先发异常再发正常状态")
    @pytest.mark.sanity
    def test_close_window_position_4_0_caseid_1982421(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts()
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)  
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        self.soa.notify_WindowPosition_sts(positions = [4,4,4,4])
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程车窗控制_关_等待车窗动作完成的时间先发正常再发异常状态")
    @pytest.mark.sanity
    def test_close_window_position_0_4_caseid_1982420(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts()
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        time.sleep(2)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        time.sleep(2)
        self.soa.notify_WindowPosition_sts(positions = [4,4,4,4])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_关_超时NotifyPosition值相同")
    @pytest.mark.full
    def test_close_window_NotifyPosition_timeout_same_caseid_1982419(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts()        
        time.sleep(2)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        time.sleep(10.5)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_关_超时NotifyPosition值不同")
    @pytest.mark.full
    def test_close_window_NotifyPosition_timeout_different_caseid_1982418(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts()
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=10)
        time.sleep(10.5)
        self.soa.notify_WindowPosition_sts(positions = [80,80,80,80])
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_连续二次远程开车窗")
    @pytest.mark.full
    def test_open_window_two_open_caseid_1982417(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control() 
        execid = self.tsp.rvc_window_control()   
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)   

    @allure.title("远程控制-RVC_远程车窗控制_开_TRANSPORT")
    @pytest.mark.full
    def test_open_window_CarMode_TRANSPORT_caseid_1982411(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程车窗控制_开_FACTORY")
    @pytest.mark.full
    def test_open_window_CarMode_FACTORY_caseid_1982410(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程车窗控制_开_CRASH")
    @pytest.mark.full
    def test_open_window_CarMode_CRASH_caseid_1982409(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程车窗控制_开_DYNO")
    @pytest.mark.full
    def test_open_window_CarMode_DYNO_caseid_1982408(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     
         
    @allure.title("远程控制-RVC_远程车窗控制_开_Active")
    @pytest.mark.full
    def test_open_window_UsageMode_ACTIVE_caseid_1982405(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程车窗控制_开_Driving")
    @pytest.mark.full
    def test_open_window_UsageMode_DRIVING_caseid_1982404(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程车窗控制_开_GearR")
    @pytest.mark.full
    def test_open_window_Gear_Rvs_caseid_1982403(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程车窗控制_开_Neut")
    @pytest.mark.full
    def test_open_window_Gear_Neut_caseid_1982402(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-VC_远程车窗控制_开_GearD")
    @pytest.mark.full
    def test_open_window_Gear_Drv_caseid_1982401(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-VC_远程车窗控制_开_GearM")
    @pytest.mark.full
    def test_open_window_Gear_ManMode_caseid_1982400(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      

    @allure.title("远程控制-RVC_远程车窗控制_开_GearNA")
    @pytest.mark.full
    def test_open_window_Gear_GearNA_caseid_1982399(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        self.soa.s2s_set_gear(gear=Gear.Resd1)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   
        
    @allure.title("远程控制-RVC_远程车窗控制_开_GearNA和FOAT为UPDATE")
    @pytest.mark.full
    def test_open_window_FOTA_UPDATE_GearNA_caseid_1982398(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.s2s_set_gear(gear=Gear.Resd1)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     

    @allure.title("远程控制-RVC_远程车窗控制_开_Active和GearR")
    @pytest.mark.full
    def test_open_window_UsageMode_ACTIVE_GearR_caseid_1982397(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      

    @allure.title("远程控制-RVC_远程车窗控制_开_Convenience和GearR")
    @pytest.mark.full
    def test_open_window_UsageMode_CONVENIENCE_GearR_caseid_1982396(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程车窗控制_开_Convenience和kSeatFrontLeft")
    @pytest.mark.full
    def test_open_window_UsageMode_CONVENIENCE_kSeatFrontLeft_caseid_1982395(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100},timeout=15)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程车窗控制_开_Convenience和kSeatFrontRight")
    @pytest.mark.full
    def test_open_window_UsageMode_CONVENIENCE_kSeatFrontRight_caseid_1982394(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,1,0,0,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100},timeout=15)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_开_Convenience和kSeatRearLeft")
    @pytest.mark.full
    def test_open_window_UsageMode_CONVENIENCE_kSeatRearLeft_caseid_1982393(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,1,0,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100},timeout=15)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程车窗控制_开_Convenience和kSeatRearMiddle")
    @pytest.mark.full
    def test_open_window_UsageMode_CONVENIENCE_kSeatRearMiddle_caseid_1982392(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,1,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100},timeout=15)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程车窗控制_开_Convenience和kSeatRearRight")
    @pytest.mark.full
    def test_open_window_UsageMode_CONVENIENCE_kSeatRearRight_caseid_1982391(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,1])
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100},timeout=15)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程车窗控制_开_GearM和FOTA为UPDATE")
    @pytest.mark.full
    def test_open_window_Gear_ManMode_FOTAM_UPDATE_caseid_1982390(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程车窗控制_开_维修模式True")
    @pytest.mark.full
    def test_open_window_mntnmode_True_caseid_1982389(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程车窗控制_开_维修模式True和FOTA为UPDATE")
    @pytest.mark.full
    def test_open_window_mntnmode_True_FOTAM_UPDATE_caseid_1982388(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程车窗控制_开_FOTA为UPDATE")
    @pytest.mark.full
    def test_open_window_FOTAM_UPDATE_caseid_1982387(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程车窗控制_开_FOTA为ROLLBACK")
    @pytest.mark.full
    def test_open_window_FOTAM_ROLLBACK_caseid_1982386(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control()   
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"          

    @allure.title("远程控制-RVC_远程车窗控制_开_下发1个车窗position=12不同与SetSpecificWindowPosition")
    @pytest.mark.full
    def test_open_window_rvc12_NotifyPosition16_caseid_1982370(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)  
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=12)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":12},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100},timeout=15)
        time.sleep(9)
        self.soa.notify_WindowPosition_sts(positions = [16,100,100,100])
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程车窗控制_开_超时时间内NotifyPosition值相同")
    @pytest.mark.full
    def test_open_window_position_timeout_open_100_caseid_1982357(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control() 
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100}, timeout=10)
        time.sleep(11)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程车窗控制_开_超时NotifyPosition值不相同")
    @pytest.mark.full
    def test_open_window_position_timeout_open_100_caseid_1982356(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_window_control(win_fl=4, win_fr=4, win_rl=4,win_rr=4) 
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":4},{"id":1,"position":4},{"id":2,"position":4},{"id":3,"position":4}, timeout=10)
        time.sleep(11)
        self.soa.notify_WindowPosition_sts(positions = [8,8,8,8])
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      
        
    @allure.title("远程控制-RVC_远程车窗控制_开_SOAFail")
    @pytest.mark.full
    def test_open_window_SOAFail_caseid_1982413(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        self.soa.soa_partner.stop_single_partner("WindowAppService_server")
        time.sleep(10)
        execid = self.tsp.rvc_window_control()   
        time.sleep(50)
        assert self.tsp.log_search_remote_vehicle_control("SOAFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      
        self.soa.soa_partner.start_single_partner(service="WindowAppService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("WindowAppService_server",timeout=30)    

    @allure.title("远程控制-RVC_远程车窗控制_关_SOAFail")
    @pytest.mark.full
    def test_close_window_SOAFail_caseid_1982467(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        self.soa.notify_WindowPosition_sts()
        self.soa.soa_partner.stop_single_partner("WindowAppService_server")
        time.sleep(10)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0,win_rr=0)   
        time.sleep(50)
        assert self.tsp.log_search_remote_vehicle_control("SOAFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      
        self.soa.soa_partner.start_single_partner(service="WindowAppService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("WindowAppService_server",timeout=30)    

    @allure.title("远程控制-RVC_远程车窗控制_开_检查休眠")
    @pytest.mark.sanity
    def test_open_window_inactive_hibernate_caseid_1982471(self, ecu):
        self.io.tcam_kl15_down()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        time.sleep(0.5)
        self.bus_comm.pause_all_bus_send()
        execid = self.tsp.rvc_window_control()   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":100},{"id":1,"position":100},{"id":2,"position":100},{"id":3,"position":100},timeout=15)
        self.soa.notify_WindowPosition_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.mix.check_tcam_sleep(300) == True, 'TCAM远控执行完成之后休眠检查失败' 

    @allure.title("远程控制-RVC_远程车窗控制_关_检查休眠")
    @pytest.mark.sanity
    def test_close_window_inactive_hibernate_caseid_1982460(self, ecu):
        self.io.tcam_kl15_down()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_WindowPosition_sts()
        time.sleep(0.5)
        self.bus_comm.pause_all_bus_send()
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        self.soa.check_SetSpecificWindowPosition_req({"id":0,"position":0},{"id":1,"position":0},{"id":2,"position":0},{"id":3,"position":0},timeout=15)
        self.soa.notify_WindowPosition_sts(positions = [0,0,0,0])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.mix.check_tcam_sleep(300) == True, 'TCAM远控执行完成之后休眠检查失败'
                    
    @allure.title("远程控制-RVC_远程车窗控制_关_ABANDONED_TelmFctReq")
    @pytest.mark.full
    def test_close_window_ABANDONED_wake_up_TelmFctReq_caseid_1982470(self, ecu):
        self.io.tcam_kl15_down()
        self.bus_comm.pause_all_bus_send()
        sleep(60)
        self.mix.tcam_network_sleep()
        self.bus_comm.check_signal_thread_start("connectivitycanfd","TcamConnectivityFr35", "TelmFctReq", timeout=5)
        execid = self.tsp.rvc_window_control(win_fl=0, win_fr=0, win_rl=0, win_rr=0)   
        result_ori_1 = self.bus_comm.check_signal_thread_stop("TelmFctReq",10)
        logger.info(f'监控到的数据： {result_ori_1}')
        result_1 = check_signal_num(result_ori_1,1)
        frame_times = result_1[0]
        duration_time = result_1[1]
        logger.info(f"持续发送{frame_times}帧，持续时间为{duration_time}s")
        assert frame_times==25, f"检查休眠唤醒后TelmFctReq发送失败"
        sleep(10)
        
    @allure.title("远程控制-RVC_远程车窗控制_关_ABANDONED_TelmFctReq")
    @pytest.mark.full
    def test_open_window_ABANDONED_wake_up_TelmFctReq_caseid_1982469(self, ecu):
        self.io.tcam_kl15_down()
        self.bus_comm.pause_all_bus_send()
        sleep(60)
        self.mix.tcam_network_sleep()
        self.bus_comm.check_signal_thread_start("connectivitycanfd","TcamConnectivityFr35", "TelmFctReq", timeout=5)
        execid = self.tsp.rvc_window_control()   
        result_ori_1 = self.bus_comm.check_signal_thread_stop("TelmFctReq",10)
        result_1 = check_signal_num(result_ori_1,1)
        frame_times = result_1[0]
        duration_time = result_1[1]
        logger.info(f"持续发送{frame_times}帧，持续时间为{duration_time}s")
        assert frame_times==25, f"检查休眠唤醒后TelmFctReq发送失败"
        sleep(10)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
# pytest -vs -p no:warnings remote_control/basic_remote_control/test_window.py

