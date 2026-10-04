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

@allure.feature("互联服务/远程控制/远程尾门控制")
@allure.story("远程尾门控制")
class TestTailGateCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["HighVoltageService_server","VehicleModeService_server", "FotaMasterService_server",
                    "VehicleSetStatusService_server", "ChassisService_server", 
                    "VehicleTimeService_server", "SeatService_server",
                    "TailGateService_server"])
        self.mix.start_get_request_and_send_response_to_tcam_thread(["VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server","SeatService_server", 
                         "HighVoltageService_server", "VehicleTimeService_server",
                         "TailGateService_server"])
        sleep(20)
        
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


    @allure.title("远程控制-RVC_远控尾门控制_关_INACTIVE")
    @pytest.mark.smoke
    def test_close_tailgate_INACTIVE_caseid_1982572(self, ecu):
        execid = self.tsp.rvc_tailgate_control()
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 15)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_关_INACTIVE")
    @pytest.mark.sanity 
    def test_close_tailgate_INACTIVE_caseid_1982571(self):
        self.io.tcam_kl15_down()
        self.bus_comm.pause_all_bus_send()
        sleep(60)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_tailgate_control()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 15)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        self.soa.s2s_set_usage_mode(UsageMode.ABANDONED)
        self.bus_comm.pause_all_bus_send()  
        assert self.mix.check_tcam_sleep(180 + 60)

    @allure.title("远程控制-RVC_远控尾门控制_关_ABANDONED")
    @pytest.mark.smoke
    def test_close_tailgate_ABANDONED_caseid_1982577(self, ecu):
        self.io.tcam_kl15_down()
        self.bus_comm.pause_all_bus_send()
        sleep(60)
        self.mix.tcam_network_sleep()
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control()
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.resume_all_bus_send()
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 15)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
    
    @allure.title("远程控制-RVC_远控尾门控制_关_Convenience不占座")
    @pytest.mark.smoke
    def test_close_tailgate_Convenience_caseid_1982569(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control()
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远控尾门控制_开_ABANDONED")
    @pytest.mark.smoke
    def test_open_tailgate_ABANDONED_caseid_1982637(self, ecu):
        self.io.tcam_kl15_down()
        self.bus_comm.pause_all_bus_send()
        sleep(60)
        self.mix.tcam_network_sleep()
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control(1) 
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.resume_all_bus_send()
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_开_INACTIVE")
    @pytest.mark.smoke
    def test_open_tailgate_INACTIVE_caseid_1982632(self, ecu):
        execid = self.tsp.rvc_tailgate_control(1) 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_开_Convenience不占座")
    @pytest.mark.smoke
    def test_open_tailgate_Convenience_caseid_1982628(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control(1) 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_翘起_ABANDONED")
    @pytest.mark.smoke
    def test_open_SetPosition_ABANDONED_caseid_1982527(self, ecu):
        self.io.tcam_kl15_down()
        self.bus_comm.pause_all_bus_send()
        sleep(60)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.resume_all_bus_send()
        self.soa.check_TailGateService_SetPosition_req(pos=20,timeout = 15)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_翘起_INACTIVE")
    @pytest.mark.smoke
    def test_open_SetPosition_INACTIVE_caseid_1982522(self, ecu):
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.soa.check_TailGateService_SetPosition_req(pos=20,timeout = 8)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远控尾门控制_翘起_Convenience不占座")
    @pytest.mark.smoke
    def test_open_SetPosition_Convenience_caseid_1982520(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.soa.check_TailGateService_SetPosition_req(pos=20,timeout = 8)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_开_9秒INACTIVE")
    @pytest.mark.sanity
    def test_open_tailgate_waittime_9_caseid_1982631(self, ecu):
        execid = self.tsp.rvc_tailgate_control(1) 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        time.sleep(9)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_开_FOTA为Query")
    @pytest.mark.sanity
    def test_open_tailgate_FOTA_Query_caseid_1982604(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control(1) 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_开_FOTA为NewTask")
    @pytest.mark.sanity
    def test_open_tailgate_FOTA_NewTask_caseid_1982603(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control(1) 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_开_FOTA为Downloadingk")
    @pytest.mark.sanity
    def test_open_tailgate_FOTA_Downloadingk_caseid_1982602(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control(1) 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_开_FOTA为Active")
    @pytest.mark.sanity
    def test_open_tailgate_FOTA_Active_caseid_1982601(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control(1) 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_开_FOTA为UpdateFailedNotDriving")
    @pytest.mark.sanity
    def test_open_tailgate_FOTA_UpdateFailedNotDriving_caseid_1982600(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)        
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control(1) 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_开_Status==kHover等待尾门执行9.5秒")
    @pytest.mark.sanity
    def test_open_tailgate_Status_kHover_caseid_1982595(self, ecu):    
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control(1) 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        time.sleep(9.5)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kHover)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_开等待尾门执行10秒中先发正常再发异常状态")
    @pytest.mark.sanity
    def test_open_tailgate_Status_kOpened_kClosed_caseid_1982592(self, ecu):    
        execid = self.tsp.rvc_tailgate_control(1) 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_开等待尾门执行10秒中先发异常再发正常状态")
    @pytest.mark.sanity
    def test_open_tailgate_Status_kClosed_kOpened_caseid_1982593(self, ecu):    
        execid = self.tsp.rvc_tailgate_control(1) 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_关_FOTA为Query")
    @pytest.mark.sanity
    def test_close_tailgate_FOTA_Query_caseid_1982552(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control() 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_关_FOTA为NewTask")
    @pytest.mark.sanity
    def test_close_tailgate_FOTA_NewTask_caseid_1982551(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control() 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_关_FOTA为Downloadingk")
    @pytest.mark.sanity
    def test_close_tailgate_FOTA_Downloadingk_caseid_1982550(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control() 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_关_FOTA为Active")
    @pytest.mark.sanity
    def test_close_tailgate_FOTA_Active_caseid_1982549(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control() 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_关_FOTA为UpdateFailedNotDriving")
    @pytest.mark.sanity
    def test_close_tailgate_FOTA_UpdateFailedNotDriving_caseid_1982548(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)        
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control() 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_关等待尾门执行10秒中先发正常再发异常状态")
    @pytest.mark.sanity
    def test_close_tailgate_Status_kClosed_kOpened_caseid_1982541(self, ecu):    
        execid = self.tsp.rvc_tailgate_control() 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_关等待尾门执行10秒中先发异常再发正常状态")
    @pytest.mark.sanity
    def test_close_tailgate_Status_kOpened_kClosed_caseid_1982542(self, ecu):    
        execid = self.tsp.rvc_tailgate_control() 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远控尾门控制_关_等待7秒Status==kClosed")
    @pytest.mark.sanity
    def test_close_tailgate_kClosed_wait_7s_caseid_1982539(self, ecu):    
        execid = self.tsp.rvc_tailgate_control() 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        time.sleep(7)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   
   
    @allure.title("远程控制-RVC_远控尾门控制_翘起_FOTA为Query")
    @pytest.mark.sanity
    def test_open_SetPosition_FOTA_Query_caseid_1982501(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.soa.check_TailGateService_SetPosition_req(pos=20, timeout = 8)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)     
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_翘起_FOTA为NewTask")
    @pytest.mark.sanity
    def test_open_SetPosition_FOTA_NewTask_caseid_1982500(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.soa.check_TailGateService_SetPosition_req(pos=20, timeout = 8)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)     
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_翘起_FOTA为Downloadingk")
    @pytest.mark.sanity
    def test_open_SetPosition_FOTA_Downloadingk_caseid_1982499(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.soa.check_TailGateService_SetPosition_req(pos=20, timeout = 8)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)     
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_翘起_FOTA为Active")
    @pytest.mark.sanity
    def test_open_SetPosition_FOTA_Active_caseid_1982498(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.soa.check_TailGateService_SetPosition_req(pos=20, timeout = 8)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)     
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_翘起_FOTA为UpdateFailedNotDriving")
    @pytest.mark.sanity
    def test_open_SetPosition_FOTA_UpdateFailedNotDriving_caseid_1982497(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)        
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.soa.check_TailGateService_SetPosition_req(pos=20, timeout = 8)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)     
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_翘起_Status==kHover")
    @pytest.mark.sanity
    def test_open_SetPosition_Status_kHover_caseid_1982492(self, ecu):   
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)  
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kHover)     
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.soa.check_TailGateService_SetPosition_req(pos=20, timeout = 8)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kHover)     
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_翘起_等待尾门执行时间9.9秒")
    @pytest.mark.sanity
    def test_open_SetPosition_kHover_wait_9s_caseid_1982491(self, ecu):  
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE) 
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)      
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.soa.check_TailGateService_SetPosition_req(pos=20, timeout = 8)
        time.sleep(9.9)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kHover)     
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_翘起_等待尾门执行时间9.9秒")
    @pytest.mark.sanity
    def test_open_SetPosition_kHover_wait_9s_caseid_1982521(self, ecu):  
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE) 
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)      
        time.sleep(1)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.soa.check_TailGateService_SetPosition_req(pos=20, timeout = 8)
        time.sleep(9.2)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)     
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_翘起等待尾门执行10秒中先发异常再发正常状态")
    @pytest.mark.sanity
    def test_open_SetPosition_Status_kClosed_kOpened_caseid_1982489(self, ecu):    
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.soa.check_TailGateService_SetPosition_req(pos=20,timeout = 8)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)  
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)    
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      

    @allure.title("远程控制-RVC_远控尾门控制_连续二次远程尾门开")
    @pytest.mark.full
    def test_open_tailgate_two_open_caseid_1982641(self, ecu):    
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)  
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        execid = self.tsp.rvc_tailgate_control(op=1) 
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
        sleep(10)    
        
    @allure.title("远程控制-RVC_远控尾门控制_开_TRANSPORT")
    @pytest.mark.full
    def test_open_tailgate_CarMode_TRANSPORT_caseid_1982636(self, ecu):    
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)  
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远控尾门控制_开_FACTORY")
    @pytest.mark.full
    def test_open_tailgate_CarMode_FACTORY_caseid_1982635(self, ecu):    
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远控尾门控制_开_CRASH")
    @pytest.mark.full
    def test_open_tailgate_CarMode_CRASH_caseid_1982634(self, ecu):    
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"          
        
    @allure.title("远程控制-RVC_远控尾门控制_开_DYNO")
    @pytest.mark.full
    def test_open_tailgate_CarMode_DYNO_caseid_1982633(self, ecu):    
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"                   
        
    @allure.title("远程控制-RVC_远控尾门控制_开_Convenience_kSeatFrontLeft")
    @pytest.mark.full
    def test_open_tailgate_UsageMode_CONVENIENCE_kSeatFrontLeft_caseid_1982627(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        time.sleep(1)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kHover)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       
        
    @allure.title("远程控制-RVC_远控尾门控制_开_Convenience_kSeatFrontRight")
    @pytest.mark.full
    def test_open_tailgate_UsageMode_CONVENIENCE_kSeatFrontRight_caseid_1982626(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,1,0,0,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        time.sleep(1)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kHover)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       

    @allure.title("远程控制-RVC_远控尾门控制_开_Convenience_kSeatRearLeft")
    @pytest.mark.full
    def test_open_tailgate_UsageMode_CONVENIENCE_kSeatRearLeft_caseid_1982625(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,1,0,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        time.sleep(1)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kHover)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       

    @allure.title("远程控制-RVC_远控尾门控制_开_Convenience_kSeatRearMiddle")
    @pytest.mark.full
    def test_open_tailgate_UsageMode_CONVENIENCE_kSeatRearMiddle_caseid_1982624(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,1,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        time.sleep(1)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kHover)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"         

    @allure.title("远程控制-RVC_远控尾门控制_开_Convenience_kSeatRearRight")
    @pytest.mark.full
    def test_open_tailgate_UsageMode_CONVENIENCE_kSeatRearRight_caseid_1982623(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,1])
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        time.sleep(1)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kHover)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       
                                                                                                            
    @allure.title("远程控制-RVC_远控尾门控制_开_Active")
    @pytest.mark.full
    def test_open_tailgate_UsageMode_ACTIVE_caseid_1982622(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远控尾门控制_开_DRIVING")
    @pytest.mark.full
    def test_open_tailgate_UsageMode_DRIVING_caseid_1982621(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"            

    @allure.title("远程控制-RVC_远控尾门控制_开_TRANSPORT和Active")
    @pytest.mark.full
    def test_open_tailgate_UsageMode_ACTIVE_caseid_1982620(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远控尾门控制_开_Driving和GearR")
    @pytest.mark.full
    def test_open_tailgate_UsageMode_DRIVING_GearR_caseid_1982619(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       
        
    @allure.title("远程控制-RVC_远控尾门控制_开_Driving和GearN")
    @pytest.mark.full
    def test_open_tailgate_UsageMode_DRIVING_Neut_caseid_1982618(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
        
    @allure.title("远程控制-RVC_远控尾门控制_开_Driving和GearD")
    @pytest.mark.full
    def test_open_tailgate_UsageMode_DRIVING_Drv_caseid_1982617(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远控尾门控制_开_Driving和GearM")
    @pytest.mark.full
    def test_open_tailgate_UsageMode_DRIVING_ManMode_caseid_1982616(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"            
        
    @allure.title("远程控制-RVC_远控尾门控制_开_GearR")
    @pytest.mark.full
    def test_open_tailgate_Gear_Rvs_caseid_1982615(self, ecu):    
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     
        
    @allure.title("远程控制-RVC_远控尾门控制_开_GearN")
    @pytest.mark.full
    def test_open_tailgate_Gear_Neut_caseid_1982614(self, ecu):    
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
        
    @allure.title("远程控制-RVC_远控尾门控制_开_GearD")
    @pytest.mark.full
    def test_open_tailgate_Gear_Drv_caseid_1982613(self, ecu):    
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远控尾门控制_开_GearM")
    @pytest.mark.full
    def test_open_tailgate_Gear_ManMode_caseid_1982612(self, ecu):    
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远控尾门控制_开_GearNA")
    @pytest.mark.full
    def test_open_tailgate_Gear_ManMode_Resd1_caseid_1982611(self, ecu):    
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(0.5)
        self.soa.s2s_set_gear(gear=Gear.Resd1)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"         

    @allure.title("远程控制-RVC_远控尾门控制_开_GearNA和FOTA为UPDATE")
    @pytest.mark.full
    def test_open_tailgate_Gear_ManMode_FOTA_UPDATE_caseid_1982609(self, ecu):    
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(0.5)
        self.soa.s2s_set_gear(gear=Gear.Resd1)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"          
        
    @allure.title("远程控制-RVC_远控尾门控制_开_维修模式True")
    @pytest.mark.full
    def test_open_tailgate_mntnmode_True_caseid_1982608(self, ecu):    
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      

    @allure.title("远程控制-RVC_远控尾门控制_开_维修模式True和FOTA为UPDATE")
    @pytest.mark.full
    def test_open_tailgate_mntnmode_True_FOTA_UPDATE_caseid_1982607(self, ecu):    
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"                      

    @allure.title("远程控制-RVC_远控尾门控制_开_FOTA为UPDATE")
    @pytest.mark.full
    def test_open_tailgate_FOTA_UPDATE_caseid_1982606(self, ecu):    
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"            
        
    @allure.title("远程控制-RVC_远控尾门控制_开_FOTA为ROLLBACK")
    @pytest.mark.full
    def test_open_tailgate_FOTA_ROLLBACK_caseid_1982605(self, ecu):    
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     

    @allure.title("远程控制-RVC_远控尾门控制_开_Status==kClosing")
    @pytest.mark.full
    def test_open_tailgate_Status_kClosing_caseid_1982598(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        time.sleep(5)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosing)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远控尾门控制_开_Status==kOpening")
    @pytest.mark.full
    def test_open_tailgate_Status_kOpening_caseid_1982596(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(1) 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpening)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"          

    @allure.title("远程控制- RVC_远控尾门控制_开_Status==kHover等待尾门执行10.5秒")
    @pytest.mark.full
    def test_open_tailgate_Status_kHover_caseid_1982594(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(1) 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        time.sleep(11)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kHover)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"        

    @allure.title("远程控制-RVC_远控尾门控制_开_Status==kClosed")
    @pytest.mark.full
    def test_open_tailgate_Status_kClosed_caseid_1982589(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1) 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"          

    @allure.title("远程控制-RVC_远控尾门控制_开_Status==kOpeningBreak)")
    @pytest.mark.full
    def test_open_tailgate_Status_kOpeningBreak_caseid_1982590(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(1) 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        time,sleep(9)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpeningBreak)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远控尾门控制_开_超时和Status==kOpened")
    @pytest.mark.full
    def test_open_tailgate_Status_timeout_kOpened_caseid_1982588(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(1) 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        time.sleep(11)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远控尾门控制_开_超时和Status==kClosed")
    @pytest.mark.full
    def test_open_tailgate_Status_timeout_kClosed_caseid_1982587(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(1) 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        time.sleep(10.5)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"           
     
    @allure.title("远程控制-RVC_远控尾门控制_开_超时和Status==kOpening")
    @pytest.mark.full
    def test_open_tailgate_Status_timeout_kOpening_caseid_1982586(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(1) 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        time.sleep(10.5)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"           

    @allure.title("远程控制-RVC_远控尾门控制_开_超时Status==kHover")
    @pytest.mark.full
    def test_open_tailgate_Status_timeout_kHover_caseid_1982585(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(1) 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Open, timeout = 10)
        time.sleep(11)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kHover)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"           

    @allure.title("远程控制-RVC_远控尾门控制_连续二次远程尾门关")
    @pytest.mark.full
    def test_close_tailgate_two_close_caseid_1982581(self, ecu):    
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)  
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        execid = self.tsp.rvc_tailgate_control() 
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    
        sleep(10) 

    @allure.title("远程控制-RVC_远控尾门控制_关_TRANSPORT")
    @pytest.mark.full
    def test_close_tailgate_CarMode_TRANSPORT_caseid_1982576(self, ecu):    
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远控尾门控制_关_FACTORY")
    @pytest.mark.full
    def test_close_tailgate_CarMode_FACTORY_caseid_1982575(self, ecu):    
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远控尾门控制_关_CRASH")
    @pytest.mark.full
    def test_close_tailgate_CarMode_CRASH_caseid_1982574(self, ecu):    
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"          
        
    @allure.title("远程控制-RVC_远控尾门控制_关_DYNO")
    @pytest.mark.full
    def test_close_tailgate_CarMode_DYNO_caseid_1982573(self, ecu):    
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"                   

        
    @allure.title("远程控制-RVC_远控尾门控制_关_Convenience_kSeatFrontLeft")
    @pytest.mark.full
    def test_close_tailgate_UsageMode_CONVENIENCE_kSeatFrontLeft_caseid_1982568(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        time.sleep(1)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"           
        
    @allure.title("远程控制-RVC_远控尾门控制_关_Convenience_kSeatFrontRight")
    @pytest.mark.full
    def test_close_tailgate_UsageMode_CONVENIENCE_kSeatFrontRight_caseid_1982567(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,1,0,0,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        time.sleep(1)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_关_Convenience_kSeatRearLeft")
    @pytest.mark.full
    def test_close_tailgate_UsageMode_CONVENIENCE_kSeatRearLeft_caseid_1982566(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,1,0,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        time.sleep(1)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"         

    @allure.title("远程控制-RVC_远控尾门控制_关_Convenience_kSeatRearMiddle")
    @pytest.mark.full
    def test_close_tailgate_UsageMode_CONVENIENCE_kSeatRearMiddle_caseid_1982565(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,1,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        time.sleep(1)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"        

    @allure.title("远程控制-RVC_远控尾门控制_关_Convenience_kSeatRearRight")
    @pytest.mark.full
    def test_close_tailgate_UsageMode_CONVENIENCE_kSeatRearRight_caseid_1982564(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,1])
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        time.sleep(1)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  
                                                                                                            
    @allure.title("远程控制-RVC_远控尾门控制_关_Active")
    @pytest.mark.full
    def test_close_tailgate_UsageMode_ACTIVE_caseid_1982563(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远控尾门控制_关_DRIVING")
    @pytest.mark.full
    def test_close_tailgate_UsageMode_DRIVING_caseid_1982562(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"            

    @allure.title("远程控制-RVC_远控尾门控制_关_GearR")
    @pytest.mark.full
    def test_close_tailgate_Gear_Rvs_caseid_1982561(self, ecu): 
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)   
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     
        
    @allure.title("远程控制-RVC_远控尾门控制_关_GearN")
    @pytest.mark.full
    def test_close_tailgate_Gear_Neut_caseid_1982560(self, ecu):  
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)    
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
        
    @allure.title("远程控制-RVC_远控尾门控制_关_GearD")
    @pytest.mark.full
    def test_close_tailgate_Gear_Drv_caseid_1982559(self, ecu):    
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)  
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远控尾门控制_关_GearM")
    @pytest.mark.full
    def test_close_tailgate_Gear_ManMode_caseid_1982558(self, ecu):    
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)  
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远控尾门控制_关_GearR")
    @pytest.mark.full
    def test_close_tailgate_CONVENIENCE_Gear_Rvs_caseid_1982557(self, ecu): 
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE) 
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)  
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远控尾门控制_关_维修模式True")
    @pytest.mark.full
    def test_close_tailgate_mntnmode_True_caseid_1982556(self, ecu): 
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)   
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_关_维修模式True和FOTA为UPDATE")
    @pytest.mark.full
    def test_close_tailgate_mntnmode_True_FOTAM_UPDATE_caseid_1982555(self, ecu): 
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远控尾门控制_关_FOTA为UPDATE")
    @pytest.mark.full
    def test_close_tailgate_FOTAM_UPDATE_caseid_1982554(self, ecu): 
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      
        
    @allure.title("远程控制-RVC_远控尾门控制_关_FOTA为ROLLBACK")
    @pytest.mark.full
    def test_close_tailgate_FOTAM_ROLLBACK_caseid_1982553(self, ecu): 
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_关_Status==kClosing")
    @pytest.mark.full
    def test_close_tailgate_Status_kClosing_caseid_1982546(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        time.sleep(5)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosing)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"           
        
    @allure.title("远程控制-RVC_远控尾门控制_关_Status==kOpened")
    @pytest.mark.full
    def test_close_tailgate_Status_kOpened_caseid_1982545(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        time.sleep(5)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远控尾门控制_关_Status==kOpening")
    @pytest.mark.full
    def test_close_tailgate_Status_kOpening_caseid_1982544(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpening)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_关_Status==kHover")
    @pytest.mark.full
    def test_close_tailgate_Status_kHover_caseid_1982543(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        time.sleep(9)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kHover)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远控尾门控制_关_Status==kClosingBreak")
    @pytest.mark.full
    def test_close_tailgate_Status_kClosingBreak_caseid_1982540(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosingBreak)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远控尾门控制_关_超时和Status==kOpened")
    @pytest.mark.full
    def test_close_tailgate_Status_timeout_kOpened_caseid_1982538(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        time.sleep(10.5)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   
        
    @allure.title("远程控制-RVC_远控尾门控制_关_超时和Status==kClosed")
    @pytest.mark.full
    def test_close_tailgate_Status_timeout_kClosed_caseid_1982537(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        time.sleep(11)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远控尾门控制_关_超时和Status==kOpening")
    @pytest.mark.full
    def test_close_tailgate_Status_timeout_kOpening_caseid_1982536(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        time.sleep(10.5)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpening)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"         

    @allure.title("远程控制-RVC_远控尾门控制_关_超时Status==kHover")
    @pytest.mark.full
    def test_close_tailgate_Status_timeout_kHover_caseid_1982535(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control() 
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 10)
        time.sleep(10.5)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kHover)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
        
    @allure.title("远程控制-RVC_远控尾门控制_连续二次远程尾门翘起")
    @pytest.mark.full
    def test_open_SetPosition_two_open_caseid_1982531(self, ecu):    
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)  
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
        sleep(10)   
        
    @allure.title("远程控制-RVC_远控尾门控制_翘起_TRANSPORT")
    @pytest.mark.full
    def test_open_SetPosition_CarMode_TRANSPORT_caseid_1982526(self, ecu):    
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远控尾门控制_翘起_FACTORY")
    @pytest.mark.full
    def test_open_SetPosition_CarMode_FACTORY_caseid_1982525(self, ecu):    
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远控尾门控制_翘起_CRASH")
    @pytest.mark.full
    def test_open_SetPosition_CarMode_CRASH_caseid_1982524(self, ecu):    
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"          
        
    @allure.title("远程控制-RVC_远控尾门控制_翘起_DYNO")
    @pytest.mark.full
    def test_open_SetPosition_CarMode_DYNO_caseid_1982523(self, ecu):    
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"                   
   
    @allure.title("远程控制-RVC_远控尾门控制_翘起_Convenience_kSeatFrontLeft")
    @pytest.mark.full
    def test_open_SetPosition_UsageMode_CONVENIENCE_kSeatFrontLeft_caseid_1982519(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
        self.soa.check_TailGateService_SetPosition_req(pos=20, timeout = 8)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)     
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"         
        
    @allure.title("远程控制-RVC_远控尾门控制_翘起_Convenience_kSeatFrontRight")
    @pytest.mark.full
    def test_open_SetPosition_UsageMode_CONVENIENCE_kSeatFrontRight_caseid_1982518(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,1,0,0,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
        self.soa.check_TailGateService_SetPosition_req(pos=20, timeout = 8)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)     
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远控尾门控制_翘起_Convenience_kSeatRearLeft")
    @pytest.mark.full
    def test_open_SetPosition_UsageMode_CONVENIENCE_kSeatRearLeft_caseid_1982517(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,1,0,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
        self.soa.check_TailGateService_SetPosition_req(pos=20, timeout = 8)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)     
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"        

    @allure.title("远程控制-RVC_远控尾门控制_翘起_Convenience_kSeatRearMiddle")
    @pytest.mark.full
    def test_open_SetPosition_UsageMode_CONVENIENCE_kSeatRearMiddle_caseid_1982516(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,1,0])
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
        self.soa.check_TailGateService_SetPosition_req(pos=20, timeout = 8)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)     
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"        

    @allure.title("远程控制-RVC_远控尾门控制_翘起_Convenience_kSeatRearRight")
    @pytest.mark.full
    def test_open_SetPosition_UsageMode_CONVENIENCE_kSeatRearRight_caseid_1982515(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,1])
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
        self.soa.check_TailGateService_SetPosition_req(pos=20, timeout = 8)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)     
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
                                                                                                            
    @allure.title("远程控制-RVC_远控尾门控制_翘起_Active")
    @pytest.mark.full
    def test_open_SetPosition_UsageMode_ACTIVE_caseid_1982514(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远控尾门控制_翘起_DRIVING")
    @pytest.mark.full
    def test_open_SetPosition_UsageMode_DRIVING_caseid_1982513(self, ecu):    
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"            

    @allure.title("远程控制-RVC_远控尾门控制_翘起_GearR")
    @pytest.mark.full
    def test_open_SetPosition_Gear_Rvs_caseid_1982512(self, ecu): 
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)   
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     
        
    @allure.title("远程控制-RVC_远控尾门控制_翘起_GearN")
    @pytest.mark.full
    def test_open_SetPosition_Gear_Neut_caseid_1982511(self, ecu):  
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)    
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
        
    @allure.title("远程控制-RVC_远控尾门控制_翘起_GearD")
    @pytest.mark.full
    def test_open_SetPosition_Gear_Drv_caseid_1982510(self, ecu):    
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)  
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远控尾门控制_翘起_GearM")
    @pytest.mark.full
    def test_open_SetPosition_Gear_ManMode_caseid_1982509(self, ecu):    
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)  
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远控尾门控制_翘起_GearNA")
    @pytest.mark.full
    def test_open_SetPosition_CONVENIENCE_Gear_Rvs_caseid_1982508(self, ecu): 
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)  
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE) 
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_翘起_GearNA和Fota为UPDATE")
    @pytest.mark.full
    def test_open_SetPosition_FOTAM_UPDATE_Gear_Rvs_caseid_1982507(self, ecu): 
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_翘起_ACTIVE和GearR")
    @pytest.mark.full
    def test_open_SetPosition_ACTIVE_Gear_Rvs_caseid_1982506(self, ecu): 
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)   
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远控尾门控制_翘起_维修模式True")
    @pytest.mark.full
    def test_open_SetPosition_mntnmode_True_caseid_1982505(self, ecu): 
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)   
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_翘起_维修模式True和FOTA为UPDATE")
    @pytest.mark.full
    def test_open_SetPosition_mntnmode_True_FOTAM_UPDATE_caseid_1982504(self, ecu): 
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远控尾门控制_翘起_FOTA为UPDATE")
    @pytest.mark.full
    def test_open_SetPosition_FOTAM_UPDATE_caseid_1982503(self, ecu): 
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      
        
    @allure.title("远程控制-RVC_远控尾门控制_翘起_FOTA为ROLLBACK")
    @pytest.mark.full
    def test_open_SetPosition_FOTAM_ROLLBACK_caseid_1982502(self, ecu): 
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       
        
    @allure.title("远程控制-RVC_远控尾门控制_翘起_Status==kClosing")
    @pytest.mark.full
    def test_open_SetPosition_Status_kOpened_caseid_1982495(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.soa.check_TailGateService_SetPosition_req(pos=20,timeout = 10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosing)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远控尾门控制_翘起_Status==kOpening")
    @pytest.mark.full
    def test_open_SetPosition_Status_kOpening_caseid_1982493(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.soa.check_TailGateService_SetPosition_req(pos=20,timeout = 8)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpening)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控尾门控制_翘起_Status==kClosed")
    @pytest.mark.full
    def test_open_SetPosition_Status_kClosed_caseid_1982494(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.soa.check_TailGateService_SetPosition_req(pos=20,timeout = 8)
        time.sleep(5)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   
        
    @allure.title("远程控制-RVC_远控尾门控制_翘起_Status==kOpeningBreak")
    @pytest.mark.full
    def test_open_SetPosition_Status_kOpeningBreak_caseid_1982487(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.soa.check_TailGateService_SetPosition_req(pos=20,timeout = 8)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpeningBreak)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远控尾门控制_翘起_等待尾门执行时间10.5秒")
    @pytest.mark.full
    def test_open_SetPosition_Status_timeout_caseid_1982490(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.soa.check_TailGateService_SetPosition_req(pos=20,timeout = 8)
        time.sleep(11)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远控尾门控制_翘起_等待尾门执行中先发正常再发异常")
    @pytest.mark.sanity
    def test_open_SetPosition_Status_timeout_caseid_1982488(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.soa.check_TailGateService_SetPosition_req(pos=20,timeout=10)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        time.sleep(5)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远控尾门控制_翘起_超时和Status==kOpened")
    @pytest.mark.full
    def test_open_SetPosition_Status_timeout_kOpened_caseid_1982484(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.soa.check_TailGateService_SetPosition_req(pos=20,timeout = 8)
        time.sleep(11)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   
        
    @allure.title("远程控制-RVC_远控尾门控制_翘起_超时和Status==kClosed")
    @pytest.mark.full
    def test_open_SetPosition_Status_timeout_kClosed_caseid_1982483(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.soa.check_TailGateService_SetPosition_req(pos=20,timeout = 8)
        time.sleep(11)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远控尾门控制_翘起_超时和Status==kOpening")
    @pytest.mark.full
    def test_open_SetPosition_Status_timeout_kOpening_caseid_1982482(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.soa.check_TailGateService_SetPosition_req(pos=20,timeout = 8)
        time.sleep(11)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpening)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"         

    @allure.title("远程控制-RVC_远控尾门控制_翘起_超时Status==kHover")
    @pytest.mark.full
    def test_open_SetPosition_Status_timeout_kHover_caseid_1982481(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(0.5)
        execid = self.tsp.rvc_tailgate_control(op=1, position=50) 
        self.soa.check_TailGateService_SetPosition_req(pos=50,timeout = 8)
        time.sleep(11)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kHover)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
        
    @allure.title("远程控制-RVC_远控尾门控制_开_SOAFail")
    @pytest.mark.full
    def test_open_tailgate_SOAFail_caseid_1982599(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        self.soa.soa_partner.stop_single_partner("TailGateService_server")
        time.sleep(10)
        execid = self.tsp.rvc_tailgate_control(1)
        time.sleep(50)
        assert self.tsp.log_search_remote_vehicle_control("SOAFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    
        self.soa.soa_partner.start_single_partner(service="TailGateService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("TailGateService_server",timeout=30)    

    @allure.title("远程控制-RVC_远控尾门控制_开_SOAFail")
    @pytest.mark.full
    def test_close_tailgate_SOAFail_caseid_1982547(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        self.soa.soa_partner.stop_single_partner("TailGateService_server")
        time.sleep(10)
        execid = self.tsp.rvc_tailgate_control()
        time.sleep(50)
        assert self.tsp.log_search_remote_vehicle_control("SOAFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    
        self.soa.soa_partner.start_single_partner(service="TailGateService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("TailGateService_server",timeout=30)  

    @allure.title("远程控制-RVC_远控尾门控制_翘起_SOAFail")
    @pytest.mark.full
    def test_open_SetPosition_SOAFail_caseid_1982496(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        self.soa.soa_partner.stop_single_partner("TailGateService_server")
        time.sleep(10)
        execid = self.tsp.rvc_tailgate_control(1,position=20)
        time.sleep(50)
        assert self.tsp.log_search_remote_vehicle_control("SOAFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    
        self.soa.soa_partner.start_single_partner(service="TailGateService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("TailGateService_server",timeout=30)   

    @allure.title("远程控制-RVC_远控尾门控制_开_ABANDONED_TelmFctReq")
    @pytest.mark.full
    def test_open_tailgate_ABANDONED_wake_up_TelmFctReq_caseid_1982639(self, ecu):
        self.io.tcam_kl15_down()
        self.bus_comm.pause_all_bus_send()
        sleep(60)
        self.mix.tcam_network_sleep()
        self.bus_comm.check_signal_thread_start("connectivitycanfd","TcamConnectivityFr35", "TelmFctReq", timeout=5)
        execid = self.tsp.rvc_tailgate_control(1) 
        result_ori_1 = self.bus_comm.check_signal_thread_stop("TelmFctReq",10)
        logger.info(f'监控到的数据： {result_ori_1}')
        result_1 = check_signal_num(result_ori_1,1)
        frame_times = result_1[0]
        duration_time = result_1[1]
        logger.info(f"持续发送{frame_times}帧，持续时间为{duration_time}s")
        assert frame_times==25, f"检查休眠唤醒后TelmFctReq发送失败"
        sleep(10)

    @allure.title("远程控制-RVC_远控尾门控制_关_ABANDONED_TelmFctReq")
    @pytest.mark.full
    def test_close_tailgate_ABANDONED_wake_up_TelmFctReq_caseid_1982638(self, ecu):
        self.io.tcam_kl15_down()
        self.bus_comm.pause_all_bus_send()
        sleep(60)
        self.mix.tcam_network_sleep()
        self.bus_comm.check_signal_thread_start("connectivitycanfd","TcamConnectivityFr35", "TelmFctReq", timeout=5)
        execid = self.tsp.rvc_tailgate_control() 
        result_ori_1 = self.bus_comm.check_signal_thread_stop("TelmFctReq",10)
        logger.info(f'监控到的数据： {result_ori_1}')
        result_1 = check_signal_num(result_ori_1,1)
        frame_times = result_1[0]
        duration_time = result_1[1]
        logger.info(f"持续发送{frame_times}帧，持续时间为{duration_time}s")
        assert frame_times==25, f"检查休眠唤醒后TelmFctReq发送失败"
        sleep(10)

    @allure.title("远程控制-RVC_远控尾门控制_开_检验休眠")
    @pytest.mark.sanity
    def test_close_tailgate_INACTIVE_hibernate_caseid_1982630(self, ecu):
        self.io.tcam_kl15_down()
        self.bus_comm.pause_all_bus_send()
        execid = self.tsp.rvc_tailgate_control()
        self.soa.check_SetTailGate_req(cmd=TailGateCmd.Close, timeout = 15)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.mix.check_tcam_sleep(180) == True, 'TCAM远控执行完成之后休眠检查失败'
                                                                                                                                                

    @allure.title("远程控制-RVC_远控尾门控制_请求Usagemode上切中Inactive_收到其他远程指令")
    @pytest.mark.full
    def test_close_tailgate_ABANDONED_wake_up_TelmFctReq_caseid_1987906(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        self.mix.tcam_network_sleep()
        self.bus_comm.check_signal_thread_start("connectivitycanfd","TcamConnectivityFr35", "TelmFctReq", timeout=15)
        execid = self.tsp.rvc_tailgate_control() 
        sleep(1)
        self.tsp.rvc_lock_control()
        sleep(3)
        result_ori_1 = self.bus_comm.check_signal_thread_stop("TelmFctReq",10)
        logger.info(f'监控到的数据： {result_ori_1}')
        result_1 = check_signal_num(result_ori_1,1)
        frame_times = result_1[0]
        duration_time = result_1[1]
        logger.info(f"持续发送{frame_times}帧，持续时间为{duration_time}s")
        assert frame_times==50, f"检查休眠唤醒后TelmFctReq发送失败"
        sleep(10)


    @allure.title("远程控制-RVC_远控尾门控制_请求Usagemode上切Inactive超时")
    @pytest.mark.full
    def test_caseid_1987907(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        sleep(5)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        assert self.tsp.log_search_remote_vehicle_control("NetwakeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远控尾门控制_请求Usagemode=Inactive_功能VFC开启")
    @pytest.mark.full
    def test_caseid_1987908(self, ecu):
        self.mix.tcam_network_sleep()
        self.bus_comm.check_signal_thread_start("connectivitycanfd","TcamConnectivityFr35", "TelmFctReq", timeout=10)
        execid = self.tsp.rvc_tailgate_control(op=1, position=20) 
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.tsp.rvc_lock_control()
        sleep(3)
        result_ori_1 = self.bus_comm.check_signal_thread_stop("TelmFctReq",10)
        logger.info(f'监控到的数据： {result_ori_1}')
        result_1 = check_signal_num(result_ori_1,1)
        frame_times = result_1[0]
        duration_time = result_1[1]
        logger.info(f"持续发送{frame_times}帧，持续时间为{duration_time}s")
        assert frame_times==50, f"检查休眠唤醒后TelmFctReq发送失败"                                                                                     
# pytest -vs -p no:warnings remote_control/basic_remote_control/test_tailgate.py
