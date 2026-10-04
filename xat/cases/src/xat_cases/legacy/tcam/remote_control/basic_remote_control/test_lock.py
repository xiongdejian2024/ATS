#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import time
import pytest
import allure
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.common import *

@allure.feature("互联服务/远程控制/远程解闭锁")
@allure.story("远程解闭锁")
class TestRvcLock(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server",
                         "DoorService_server", "SeatService_server", "CentralLockService_server",
                         "HighVoltageService_server", "VehicleTimeService_server",
                         "KeyService_server", "TailGateService_server","RemoteCtrlService_client",('CdcTtsService','server','cdc_a_ttsservice',600)])
        self.mix.start_get_request_and_send_response_to_tcam_thread(["VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server",
                         "DoorService_server", "SeatService_server", "CentralLockService_server",
                         "HighVoltageService_server", "VehicleTimeService_server",
                         "KeyService_server", "TailGateService_server"],ignore_func=['GetOpenCloseStatus','TailGateService_GetStatus'])
        sleep(30)

    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.soa.set_tcam_rvc_common_preconditions()
        self.soa.send_Alldoor_close()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))
        
    def after_each_func(self, ecu):
        if ecu.testresult == 'Failure':
            logger.info('用例执行失败')
            sleep(12)
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.ipdu.reset_check_results()
        self.tsp.set_bench_config(vid=self.tc_config['vid'],tel=self.tc_config['tel'])
        self.mix.default_func_param(['GetLockStatus'])
        sleep(1)

   
    def after_class(self, ecu):
        self.mix.stop_get_request_and_send_response_to_tcam_thread()
    

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_超时时间后五门关闭")
    @pytest.mark.full
    def test_doorlock_LockStatus_caseid_1982173(self):
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control(keywords='StartOK',execid=execid,flage=0)
        sleep(12)
        self.soa.send_Alldoor_close()
        self.tsp.check_async_log_search_result_from_remote_vehicle_control("DelayFail",execid=execid,flage=2),f"TCAM远程控制上报到车云的结果校验失败"
    
    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_尾门状态为kClosing")
    @pytest.mark.full
    def test_doorlock_LockStatus_FourDoorLockedTailUnlocked_caseid_1982174(self):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control(keywords='StartOK',execid=execid,flage=0)
        sleep(11)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosing)
        self.soa.notify_TailGateService_OpenCloseStatus()
        self.tsp.check_async_log_search_result_from_remote_vehicle_control("DoorCloseFail",execid=execid,flage=2),f"TCAM远程控制上报到车云的结果校验失败"
     
    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_尾门状态为kHalfClosed")
    @pytest.mark.full
    def test_doorlock_TailGateSts_kHalfClosed_caseid_1982175(self):         
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kHalfClosed)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)	
        time.sleep(13)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("DoorCloseFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_尾门状态为 kOpeningBreak")
    @pytest.mark.full
    def test_doorlock_TailGateSts_kOpeningBreak_caseid_1982176(self):       
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpeningBreak)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)	
        time.sleep(13)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("DoorCloseFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_尾门状态为 kClosingBreak")
    @pytest.mark.full
    def test_doorlock_TailGateSts_kClosingBreak_caseid_1982177(self):       
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosingBreak)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)	
        time.sleep(13)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        assert self.tsp.log_search_remote_vehicle_control("DoorCloseFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_尾门状态为 kOpened")
    @pytest.mark.full
    def test_doorlock_TailGateSts_kOpened_caseid_1982178(self):       
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)	
        time.sleep(13)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        assert self.tsp.log_search_remote_vehicle_control("DoorCloseFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_INACTIVE")
    @pytest.mark.smoke
    def test_unlock_inactive_caseid_1982266(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=15)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.check_NotifyRVCLockInfo_event(timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
    
    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_闭锁")
    @pytest.mark.sanity
    def test_unlock_inactive_caseid_1982265(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=15)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.check_NotifyRVCLockInfo_event(timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=15)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_ABANDONED")
    @pytest.mark.smoke
    def test_unlock_abandoned_caseid_1982273(self):
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.mix.tcam_network_sleep()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=20)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=20)
        execid = self.tsp.rvc_lock_control(1)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.check_NotifyRVCLockInfo_event(timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,timeout=1)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,timeout=1)

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_Convenience")
    @pytest.mark.smoke
    def test_unlock_convenience_caseid_1982264(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.check_NotifyRVCLockInfo_event(timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_FOTA为Query")
    @pytest.mark.sanity
    def test_unlock_FOTA_Query_caseid_1982243(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.check_NotifyRVCLockInfo_event(timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_FOTA为NewTask")
    @pytest.mark.sanity
    def test_unlock_FOTA_NewTask_caseid_1982242(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.check_NotifyRVCLockInfo_event(timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_FOTA为Downloadingk")
    @pytest.mark.sanity
    def test_unlock_FOTA_Downloadingk_caseid_1982241(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.check_NotifyRVCLockInfo_event(timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_FOTA为Active")
    @pytest.mark.sanity
    def test_unlock_FOTA_Active_caseid_1982240(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.check_NotifyRVCLockInfo_event(timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_等待锁执行9.9秒")
    @pytest.mark.sanity
    def test_unlock_tiem_9s_inactive_caseid_1982272(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        time.sleep(9)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.check_NotifyRVCLockInfo_event(timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_FOTA为UpdateFailedNotDriving")
    @pytest.mark.sanity
    def test_unlock_FOTA_UpdateFailedNotDriving_caseid_1982239(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)  
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.check_NotifyRVCLockInfo_event(timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     

    @allure.title("远程控制-RVC_远程四门解闭锁_连续二次远程解锁")
    @pytest.mark.full
    def test_unlock_two_unlock_caseid_1982278(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid1 = self.tsp.rvc_lock_control(1)
        execid2 = self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid2),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(13)  # 需要等待第一个指令结束

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_TRANSPORT")
    @pytest.mark.full
    def test_unlock_CarMode_TRANSPORT_caseid_1982271(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_FACTORY")
    @pytest.mark.full
    def test_unlock_CarMode_FACTORY_caseid_1982270(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_CRASH")
    @pytest.mark.full
    def test_unlock_CarMode_CRASH_caseid_1982269(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_DYNO")
    @pytest.mark.full
    def test_unlock_CarMode_DYNO_caseid_1982268(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_TRANSPORT和Active")
    @pytest.mark.full
    def test_unlock_CarMode_TRANSPORT_UsageMode_ACTIVE_caseid_1982267(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_Active")
    @pytest.mark.full
    def test_unlock_UsageMode_ACTIVE_caseid_1982263(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_Driving")
    @pytest.mark.full
    def test_unlock_UsageMode_DRIVING_caseid_1982262(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_ Active和GearD")
    @pytest.mark.full
    def test_unlock_UsageMode_ACTIVE_Gear_Drv_caseid_1982261(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_GearR")
    @pytest.mark.full
    def test_unlock_Gear_Rvs_caseid_1982260(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"              

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_GearN")
    @pytest.mark.full
    def test_unlock_Gear_Neut_caseid_1982259(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_GearD")
    @pytest.mark.full
    def test_unlock_Gear_Drv_caseid_1982258(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_GearM")
    @pytest.mark.full
    def test_unlock_Gear_ManMode_caseid_1982257(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_GearM到GearNA")
    @pytest.mark.full
    def test_unlock_Gear_ManMode_Resd1_caseid_1982256(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(1)
        self.soa.s2s_set_gear(gear=Gear.Resd1)
        execid = self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_GearNA和UPDATE")
    @pytest.mark.full
    def test_unlock_Gear_ManMode_Resd1_caseid_1982255(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.s2s_set_gear(gear=Gear.Resd1)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"            

    @allure.title("远程解解锁-RVC_远程四门解闭锁_解锁_inactive和kSeatFrontLeft")
    @pytest.mark.full
    def test_unlock_usagdemode_inactive_kSeatFrontLeft_caseid_1982254(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=15)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.check_NotifyRVCLockInfo_event(timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程解解锁-RVC_远程四门解闭锁_解锁_Convenience和kSeatFrontLeft")
    @pytest.mark.full
    def test_unlock_usagdemode_Convenience_kSeatFrontLeft_caseid_1982253(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=15)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.check_NotifyRVCLockInfo_event(timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程解解锁-RVC_远程四门解闭锁_解锁_Convenience和kSeatFrontRight")
    @pytest.mark.full
    def test_unlock_usagdemode_Convenience_kSeatFrontRight_caseid_1982252(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,1,0,0,0])
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=15)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.check_NotifyRVCLockInfo_event(timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程解解锁-RVC_远程四门解闭锁_解锁_ Convenience和 kSeatRearLeft")
    @pytest.mark.full
    def test_unlock_usagdemode_Convenience_kSeatRearLeft_caseid_1982251(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,1,0,0])
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=15)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.check_NotifyRVCLockInfo_event(timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程解解锁-RVC_远程四门解闭锁_解锁_ Convenience和 kSeatRearMiddle")
    @pytest.mark.full
    def test_unlock_usagdemode_Convenience_kSeatRearMiddle_caseid_1982250(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,1,0])
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=15)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.check_NotifyRVCLockInfo_event(timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程解解锁-RVC_远程四门解闭锁_解锁_ Convenience和kSeatRearRight")
    @pytest.mark.full
    def test_unlock_usagdemode_Convenience_SeatRearRight_caseid_1982249(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,1])
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=15)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.check_NotifyRVCLockInfo_event(timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_GearM和UPDATE")
    @pytest.mark.full
    def test_unlock_Gear_ManMode_Resd1_caseid_1982248(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     

    @allure.title("远程解解锁-RVC_远程四门解闭锁_解锁_维修模式True")
    @pytest.mark.full
    def test_unlock_mntnmode_True_caseid_1982247(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程解解锁-RVC_远程四门解闭锁_解锁_维修模式True和FOTA为UPDATE")
    @pytest.mark.full
    def test_unlock_mntnmode_True_FOTA_UPDATE_caseid_1982246(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"         
          
    @allure.title("远程解解锁-RVC_远程四门解闭锁_解锁_FOTA为UPDATE")
    @pytest.mark.full
    def test_unlock_FOTA_UPDATE_caseid_1982245(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程解解锁-RVC_远程四门解闭锁_解锁_FOTA为ROLLBACK")
    @pytest.mark.full
    def test_unlock_FOTA_ROLLBACK_caseid_1982244(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程解解锁-RVC_远程四门解闭锁_解锁_超时时间内kAllLocked")
    @pytest.mark.full
    def test_unlock_LockStatus_Unlocked_caseid_1982238(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=15)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        time.sleep(9)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程解解锁-RVC_远程四门解闭锁_解锁_超时kAllLocked")
    @pytest.mark.full
    def test_unlock_LockStatus_tiemout_AllLocked_caseid_1982237(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        time.sleep(11)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    
        
    @allure.title("远程解解锁-RVC_远程四门解闭锁_解锁_超时kFourDoorLockedTailUnlocked")
    @pytest.mark.full
    def test_unlock_LockStatus_tiemout_FourDoorLockedTailUnlocked_caseid_1982236(self):
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        time.sleep(11)
        self.soa.notify_LockStatus(lock_sts=LockStatus.FourDoorLockedTailUnlocked)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程解解锁-RVC_远程四门解闭锁_解锁_超时kUnlocked")
    @pytest.mark.full
    def test_unlock_LockStatus_tiemout_Unlocked_caseid_1982235(self):
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(1)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        time.sleep(11)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    
                          
    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁_ABANDONED")
    @pytest.mark.smoke
    def test_lock_usagdemode_abandoned_caseid_1982340(self):
        self.io.tcam_kl15_down()  
        self.bus_comm.pause_all_bus_send() 
        sleep(180)
        self.mix.tcam_network_sleep()
        self.soa.send_Alldoor_close()
        time.sleep(1)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        execid = self.tsp.rvc_lock_control(2)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.response_to_GetOpenCloseStatus_req()
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,timeout=1)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,timeout=1)        

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_INACTIVE")
    @pytest.mark.smoke
    def test_lock_usagdemode_inactive_caseid_1982335(self):
        self.soa.send_Alldoor_close()
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        self.soa.notify_VehicleInsidePersonSts()
        # # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=15)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_CONVENIENCE")
    @pytest.mark.smoke
    def test_lock_usagdemode_convenience_caseid_1982331(self):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      

    @allure.title("远程解闭锁- RVC_远程四门解闭锁_闭锁_INACTIVE 等待锁执行时间9.9秒")
    @pytest.mark.sanity
    def test_lock_time_9s_caseid_1982332(self):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=10)
        time.sleep(9.9)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      
        
    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁_FOTA为Query")
    @pytest.mark.sanity
    def test_lock_FOTA_Query_caseid_1982308(self):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁_FOTA为NewTask")
    @pytest.mark.sanity
    def test_lock_FOTA_NewTask_caseid_1982307(self):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        time.sleep(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁_FOTA为Downloadingk")
    @pytest.mark.sanity
    def test_lock_FOTA_Downloadingk_caseid_1982306(self,):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        time.sleep(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁_FOTA为Active")
    @pytest.mark.sanity
    def test_lock_FOTA_Active_caseid_1982305(self):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        time.sleep(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"          

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁_FOTA为UpdateFailedNotDriving")
    @pytest.mark.sanity
    def test_lock_FOTA_UpdateFailedNotDriving_caseid_1982304(self):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)
        time.sleep(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       


    @allure.title("远程控制-RVC_远程四门解闭锁_连续二次远程闭锁")
    @pytest.mark.full
    def test_lock_two_lock_caseid_1982345(self):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(1)
        execid1 = self.tsp.rvc_lock_control()
        execid2 = self.tsp.rvc_lock_control()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid2),f"TCAM远程控制上报到车云的结果校验失败"   
        sleep(13)    

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁_NetWakeFail")
    @pytest.mark.full
    @allure.issue(url=r'https://jira.jiduauto.com/browse/SOA-22274?filter=-3',name='SOA-22274')
    def test_lock_two_lock_caseid_1982344(self):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_lock_control(2)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.ABANDONED)
        self.soa.s2s_set_usage_mode(UsageMode.ABANDONED)
        assert self.tsp.log_search_remote_vehicle_control("NetWakeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   
        sleep(13)    

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁_TRANSPORT")
    @pytest.mark.full
    def test_lock_CarMode_TRANSPORT_caseid_1982339(self):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁_FACTORY")
    @pytest.mark.full
    def test_lock_CarMode_FACTORY_caseid_1982338(self):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁_CRASH")
    @pytest.mark.full
    def test_lock_CarMode_CRASH_caseid_1982337(self):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁_DYNO")
    @pytest.mark.full
    def test_lock_CarMode_DYNO_caseid_1982336(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_INACTIVE 等待锁执行时间11秒")
    @pytest.mark.full
    def test_lock_timeout_11s_caseid_1982333(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp(door_id=[4],timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=15)
        time.sleep(11)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"         

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁_Active")
    @pytest.mark.full
    def test_lock_UsageMode_ACTIVE_caseid_1982330(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁_Driving")
    @pytest.mark.full
    def test_lock_UsageMode_DRIVING_caseid_1982329(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁_GearR")
    @pytest.mark.full
    def test_lock_Gear_Rvs_caseid_1982328(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"              

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁_GearN")
    @pytest.mark.full
    def test_lock_Gear_Neut_caseid_1982327(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁_GearD")
    @pytest.mark.full
    def test_lock_Gear_Drv_caseid_1982326(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁_GearM")
    @pytest.mark.full
    def test_lock_Gear_ManMode_caseid_1982325(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁_GearR到GearNA")
    @pytest.mark.full
    def test_lock_Gear_Rvs_Resd1_caseid_1982324(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(1)
        self.soa.s2s_set_gear(gear=Gear.Resd1)
        execid = self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     
        
    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_inactive和kSeatFrontLeft")
    @pytest.mark.full
    def test_lock_usagdemode_inactive_kSeatFrontLeft_caseid_1982322(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        time.sleep(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_Convenience和kSeatFrontLeft")
    @pytest.mark.full
    def test_lock_usagdemode_Convenience_kSeatFrontLeft_caseid_1982321(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        time.sleep(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_Convenience和kSeatFrontRight")
    @pytest.mark.full
    def test_lock_usagdemode_Convenience_kSeatFrontRight_caseid_1982320(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,1,0,0,0])
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        time.sleep(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_ Convenience和 kSeatRearLeft")
    @pytest.mark.full
    def test_lock_usagdemode_Convenience_kSeatRearLeft_caseid_1982319(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,1,0,0])
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        time.sleep(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_ Convenience和 kSeatRearMiddle")
    @pytest.mark.full
    def test_lock_usagdemode_Convenience_kSeatRearMiddle_caseid_1982318(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,1,0])
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        time.sleep(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_ Convenience和kSeatRearRight")
    @pytest.mark.full
    def test_lock_usagdemode_Convenience_SeatRearRight_caseid_1982317(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,1])
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        time.sleep(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_维修模式True")
    @pytest.mark.full
    def test_lock_mntnmode_True_caseid_1982316(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_维修模式True和FOTA为UPDATE")
    @pytest.mark.full
    def test_lock_mntnmode_True_FOTA_UPDATE_caseid_1982315(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"         
        
    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_GearR为UPDATE")
    @pytest.mark.full
    def test_lock_Gear_Rvs_FOTA_UPDATE_caseid_1982314(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_GearN为UPDATE")
    @pytest.mark.full
    def test_lock_Gear_Neut_FOTA_UPDATE_caseid_1982313(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_GearD为UPDATE")
    @pytest.mark.full
    def test_lock_Gear_Drv_FOTA_UPDATE_caseid_1982312(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_GearM为UPDATE")
    @pytest.mark.full
    def test_lock_Gear_ManMode_FOTA_UPDATE_caseid_1982311(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_FOTA为UPDATE")
    @pytest.mark.full
    def test_lock_FOTA_UPDATE_caseid_1982310(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_FOTA为ROLLBACK")
    @pytest.mark.full
    def test_lock_FOTA_ROLLBACK_caseid_1982309(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_左前门状态为TRUE")
    @pytest.mark.full
    def test_lock_open_kDoorFrontLeft_caseid_1982303(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        assert self.tsp.log_search_remote_vehicle_control("AnyDoorOpenFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_右前门状态为TRUE")
    @pytest.mark.full
    def test_lock_open_kDoorFrontRight_caseid_1982302(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_FrntRightDoorSts(isopen=True,sts=DoorStatus.kOpened)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp(open_close_status={'1':True}, door_id=[4])
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(status=TailGateSts.kClosed,timeout=10)
        assert self.tsp.log_search_remote_vehicle_control("AnyDoorOpenFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_左后门状态为TRUE")
    @pytest.mark.full
    def test_lock_open_kDoorRearLeft_caseid_1982301(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_RearLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp(open_close_status={'2':True}, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(status=TailGateSts.kClosed,timeout=10)
        assert self.tsp.log_search_remote_vehicle_control("AnyDoorOpenFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_右后门状态为TRUE")
    @pytest.mark.full
    def test_lock_open_kDoorRearRight_caseid_1982300(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_RearRightDoorSts(isopen=True,sts=DoorStatus.kOpened)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp(open_close_status={'3':True}, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(status=TailGateSts.kClosed,timeout=10)
        assert self.tsp.log_search_remote_vehicle_control("AnyDoorOpenFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       
        
    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_左前门、右前门状态为TRUE")
    @pytest.mark.full
    def test_lock_open_kDoorFrontLeft_kDoorFrontRight_caseid_1982299(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_FrntRightDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp(open_close_status={'0':True,'1':True}, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(status=TailGateSts.kClosed,timeout=10)
        assert self.tsp.log_search_remote_vehicle_control("AnyDoorOpenFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_左前门、左后门状态为TRUE")
    @pytest.mark.full
    def test_lock_open_kDoorFrontLeft_kDoorRearLeft_caseid_1982298(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_RearLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp(open_close_status={'0':True,'2':True}, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(status=TailGateSts.kClosed,timeout=10)
        assert self.tsp.log_search_remote_vehicle_control("AnyDoorOpenFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_左前门、右后门状态为TRUE")
    @pytest.mark.full
    def test_lock_open_kDoorFrontLeft_kDoorRearRight_caseid_1982297(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_RearRightDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp(open_close_status={'0':True,'4':True}, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(status=TailGateSts.kClosed,timeout=10)
        assert self.tsp.log_search_remote_vehicle_control("AnyDoorOpenFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       
                        
    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_左前门、右前门、左后门状态为TRUE")
    @pytest.mark.full
    def test_lock_open_kDoorFrontLeft_kDoorRearRight_caseid_1982296(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_RearLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.soa.notify_FrntRightDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp(open_close_status={'0':True,'1':True,'2':True}, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(status=TailGateSts.kClosed,timeout=10)
        assert self.tsp.log_search_remote_vehicle_control("AnyDoorOpenFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_四门状态为开")
    @pytest.mark.full
    def test_lock_open_AllDoor_caseid_1982295(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.send_Alldoor_open()
        self.soa.notify_TailGateService_Status(TailGateSts.kClosed)
        self.soa.notify_TailGateService_OpenCloseStatus()
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({ "0": True,"1": True,"2": True,"3": True }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(status=TailGateSts.kClosed,timeout=10)
        assert self.tsp.log_search_remote_vehicle_control("AnyDoorOpenFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_五门状态为开")
    @pytest.mark.full
    def test_lock_open_AllDoor_TailGateSts_kOpened_caseid_1982294(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.send_Alldoor_open()
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp(open_close_status={ "0": True,"1": True,"2": True,"3": True }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(status=TailGateSts.kOpened,timeout=10)
        assert self.tsp.log_search_remote_vehicle_control("AnyDoorOpenFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_左前门和尾门状态为开")
    @pytest.mark.full
    def test_lock_open_kDoorFrontLeft_TailGateSts_kOpened_caseid_1982293(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.send_Alldoor_close()
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.soa.notify_TailGateService_OpenCloseStatus(isopen=True)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp(open_close_status={"0": True,}, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(status=TailGateSts.kOpened,timeout=10)
        assert self.tsp.log_search_remote_vehicle_control("AnyDoorOpenFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_尾门状态为 kOpening")
    @pytest.mark.full
    def test_lock_TailGateSts_kOpening_caseid_1982292(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.send_Alldoor_close()
        self.soa.notify_TailGateService_OpenCloseStatus(isopen=True)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpening)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosing,timeout=10)
        assert self.tsp.log_search_remote_vehicle_control("AnyDoorOpenFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_尾门状态为 kHover")
    @pytest.mark.full
    def test_lock_TailGateSts_kHover_caseid_1982291(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.send_Alldoor_close()
        self.soa.notify_TailGateService_OpenCloseStatus(isopen=True)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kHover)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kHover,timeout=10)
        assert self.tsp.log_search_remote_vehicle_control("AnyDoorOpenFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_尾门状态为 kOpened")
    @pytest.mark.full
    def test_lock_TailGateSts_kOpened_caseid_1982290(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.send_Alldoor_close()
        self.soa.notify_TailGateService_OpenCloseStatus(isopen=True)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kOpened,timeout=10)
        assert self.tsp.log_search_remote_vehicle_control("AnyDoorOpenFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_尾门状态为 kClosingBreak")
    @pytest.mark.full
    def test_lock_TailGateSts_kClosingBreak_caseid_1982289(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.send_Alldoor_close()
        self.soa.notify_TailGateService_OpenCloseStatus(isopen=True)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosingBreak)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosingBreak,timeout=10)
        assert self.tsp.log_search_remote_vehicle_control("AnyDoorOpenFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_尾门状态为 kOpeningBreak")
    @pytest.mark.full
    def test_lock_TailGateSts_kOpeningBreak_caseid_1982288(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.send_Alldoor_close()
        self.soa.notify_TailGateService_OpenCloseStatus(isopen=True)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpeningBreak)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kOpeningBreak,timeout=10)
        assert self.tsp.log_search_remote_vehicle_control("AnyDoorOpenFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       
        
    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_尾门状态为kHalfClosed")
    @pytest.mark.full
    def test_lock_TailGateSts_kHalfClosed_caseid_1982287(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.send_Alldoor_close()
        self.soa.notify_TailGateService_OpenCloseStatus(isopen=True)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kHalfClosed)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kHalfClosed,timeout=10)
        assert self.tsp.log_search_remote_vehicle_control("AnyDoorOpenFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_尾门状态为kClosing")
    @pytest.mark.full
    def test_lock_TailGateSts_kClosing_caseid_1982286(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.send_Alldoor_close()
        self.soa.notify_TailGateService_OpenCloseStatus(isopen=True)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kClosing)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosing,timeout=10)
        assert self.tsp.log_search_remote_vehicle_control("AnyDoorOpenFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      
        
    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_超时时间内kFourDoorLockedTailUnlocked")
    @pytest.mark.full
    # @allure.issue(url=r'https://jira.jiduauto.com/browse/SOA-23132?filter=-2',name='SOA-23132')
    def test_lock_LockStatus_FourDoorLockedTailUnlocked_caseid_1982285(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        time.sleep(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.FourDoorLockedTailUnlocked}})
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=15)
        time.sleep(3)
        self.soa.notify_LockStatus(lock_sts=LockStatus.FourDoorLockedTailUnlocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_超时时间内kUnlocked")
    @pytest.mark.full
    def test_lock_LockStatus_Unlocked_caseid_1982284(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        time.sleep(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=15)
        time.sleep(9)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_超时kAllLocked")
    @pytest.mark.full
    def test_lock_LockStatus_tiemout_AllLocked_caseid_1982283(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        time.sleep(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=15)
        time.sleep(12)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    
        
    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_超时kFourDoorLockedTailUnlocked")
    @pytest.mark.full
    def test_lock_LockStatus_tiemout_FourDoorLockedTailUnlocked_caseid_1982282(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        time.sleep(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.FourDoorLockedTailUnlocked}})
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=15)
        time.sleep(12)
        self.soa.notify_LockStatus(lock_sts=LockStatus.FourDoorLockedTailUnlocked)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_超时kUnlocked")
    @pytest.mark.full
    def test_lock_LockStatus_tiemout_Unlocked_caseid_1982281(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        time.sleep(1)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=15)
        time.sleep(11)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_ INACTIVE 等待锁状态时先传错误再传正常状态")
    @pytest.mark.sanity
    def test_lock_LockStatus_Unlocked_AllLocked_caseid_1982280(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.AllLocked}})
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=15)
        time.sleep(1)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        time.sleep(1)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_ INACTIVE等待锁状态时先传正常再传错误状态")
    @pytest.mark.sanity
    def test_lock_LockStatus_AllLocked_Unlocked_caseid_1982279(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=15)
        time.sleep(1)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        time.sleep(3)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_ABANDONED")
    @pytest.mark.smoke
    def test_doorlock_ABANDONED_caseid_1982230(self):
        self.io.tcam_kl15_down()  
        self.bus_comm.pause_all_bus_send() 
        sleep(180)
        self.mix.tcam_network_sleep()
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        time.sleep(1)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=20)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=20)        
        execid = self.tsp.rvc_lock_control(3)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,timeout=0.5)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,timeout=0.5)  
    
    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_车内有人")
    @pytest.mark.smoke
    def test_doorlock_ABANDONED_caseid_1987429(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.check_Play2_req(app='RVC',txt='关门请当心',param='{"isLoopPlay":False,"priority":1,"streamType":6,"zone":0}',timeout=10)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Hmi,find_key_type=FindKeyType.NoReq,timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_INACTIVE")
    @pytest.mark.smoke
    def test_doorlock_INACTIVE_caseid_1982225(self):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_VehicleInsidePersonSts()
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_Convenience")
    @pytest.mark.smoke
    def test_doorlock_Convenience_caseid_1982221(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"        

    @allure.title("远程控制-RVC_远程四门解闭锁联动关门_闭锁联动关门_FOTA为Query")
    @pytest.mark.sanity
    def test_doorlock_FOTA_Query_caseid_1982199(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程四门解闭锁联动关门_闭锁联动关门_FOTA为NewTask")
    @pytest.mark.sanity
    def test_doorlock_FOTA_NewTask_caseid_1982198(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程四门解闭锁联动关门_闭锁联动关门_FOTA为Downloadingk")
    @pytest.mark.sanity
    def test_doorlock_FOTA_Downloadingk_caseid_1982197(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程四门解闭锁联动关门_闭锁联动关门_FOTA为Active")
    @pytest.mark.sanity
    def test_doorlock_FOTA_Active_caseid_1982196(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   
        
    @allure.title("远程控制-RVC_远程四门解闭锁联动关门_闭锁联动关门_FOTA为UpdateFailedNotDriving")
    @pytest.mark.sanity
    def test_doorlock_FOTA_UpdateFailedNotDriving_caseid_1982195(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)  
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   
        
    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_等待锁执行11.9秒")
    @pytest.mark.sanity
    def test_doorlock_LockSts_AllLocked_caseid_1982224(self):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        time.sleep(11)  # 时间存在误差。
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_TRANSPORT")
    @pytest.mark.full
    def test_doorlock_CarMode_TRANSPORT_caseid_1982229(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_FACTORY")
    @pytest.mark.full
    def test_doorlock_CarMode_FACTORY_caseid_1982228(self):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_CRASH")
    @pytest.mark.full
    def test_doorlock_CarMode_CRASH_caseid_1982227(self,):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_DYNO")
    @pytest.mark.full
    def test_doorlock_CarMode_DYNO_caseid_1982226(self):       
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_Active")
    @pytest.mark.full
    def test_doorlock_UsageMode_ACTIVE_caseid_1982219(self, ecu):       
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_Driving")
    @pytest.mark.full
    def test_doorlock_UsageMode_DRIVING_caseid_1982218(self):       
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_Active和GearD")
    @pytest.mark.full
    def test_doorlock_UsageMode_ACTIVE_Gear_Drv_caseid_1982217(self):
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    		

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_GearR")
    @pytest.mark.full
    def test_doorlock_Gear_Rvs_caseid_1982216(self):      
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"              

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_GearN")
    @pytest.mark.full
    def test_doorlock_Gear_Neut_caseid_1982215(self):       
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_GearD")
    @pytest.mark.full
    def test_doorlock_Gear_Drv_caseid_1982214(self):       
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_GearM")
    @pytest.mark.full
    def test_doorlock_Gear_ManMode_caseid_1982213(self):       
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_GearM到GearNA")
    @pytest.mark.full
    def test_doorlock_Gear_Rvs_Resd1_caseid_1982212(self):       
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.s2s_set_gear(gear=Gear.Resd1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_GearNA和UPDATE")
    @pytest.mark.full
    def test_doorlock_Gear_ManMode_Resd1_caseid_1982211(self):
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.s2s_set_gear(gear=Gear.Resd1)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_inactive和kSeatFrontLeft")
    @pytest.mark.sanity
    def test_doorlock_usagdemode_inactive_kSeatFrontLeft_caseid_1982210(self):       
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=15)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_Convenience和kSeatFrontLeft")
    @pytest.mark.full
    def test_doorlock_usagdemode_Convenience_kSeatFrontLeft_caseid_1982209(self):       
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=15)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_Convenience和kSeatFrontRight")
    @pytest.mark.full
    def test_doorlock_usagdemode_Convenience_kSeatFrontRight_caseid_1982208(self):       
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,1,0,0,0])
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=15)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_ Convenience和 kSeatRearLeft")
    @pytest.mark.full
    def test_doorlock_usagdemode_Convenience_kSeatRearLeft_caseid_1982207(self):       
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,1,0,0])
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=15)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_ Convenience和 kSeatRearMiddle")
    @pytest.mark.full
    def test_doorlock_usagdemode_Convenience_kSeatRearMiddle_caseid_1982206(self):       
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,1,0])
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=15)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_ Convenience和kSeatRearRight")
    @pytest.mark.full
    def test_doorlock_usagdemode_Convenience_SeatRearRight_caseid_1982205(self):       
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,1])
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        # assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=15)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_GearM到GearNA")
    @pytest.mark.full
    def test_unlock_Gear_ManMode_Resd1_caseid_1982204(self):
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(1)
        self.soa.s2s_set_gear(gear=Gear.Resd1)
        execid = self.tsp.rvc_lock_control(3)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_维修模式True")
    @pytest.mark.full
    def test_doorlock_mntnmode_True_caseid_1982203(self):       
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_维修模式True和FOTA为UPDATE")
    @pytest.mark.full
    def test_doorlock_mntnmode_True_FOTA_UPDATE_caseid_1982202(self):       
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"            

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_FOTA为UPDATE")
    @pytest.mark.full
    def test_doorlock_FOTA_UPDATE_caseid_1982201(self):       
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_FOTA为ROLLBACK")
    @pytest.mark.full
    def test_doorlock_FOTA_ROLLBACK_caseid_1982200(self):       
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_超时时间内kUnlocked")
    @pytest.mark.full
    def test_doorlock_LockSts_Unlocked_caseid_1982194(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        time.sleep(4)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_超时kAllLocked")
    @pytest.mark.full
    def test_doorlock_LockSts_kAllLocked_caseid_1982193(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        time.sleep(13)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_超时kFourDoorLockedTailUnlocked")
    @pytest.mark.full
    def test_doorlock_LockSts_Unlocked_caseid_1982192(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        time.sleep(13)
        self.soa.notify_LockStatus(lock_sts=LockSts.FourDoorLockedTailUnlocked)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     	

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_超时左前门状态为TRUE")
    @pytest.mark.full
    def test_lock_open_kDoorFrontLeft_caseid_1982191(self):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        time.sleep(12)
        assert self.tsp.log_search_remote_vehicle_control("DoorCloseFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"        

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_超时右前门状态为TRUE")
    @pytest.mark.full
    def test_doorlock_open_kDoorFrontRight_caseid_1982190(self):       
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)	
        self.soa.notify_FrntRightDoorSts(isopen=True, sts=DoorStatus.kOpened)
        time.sleep(13)
        assert self.tsp.log_search_remote_vehicle_control("DoorCloseFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_左后门状态为TRUE")
    @pytest.mark.full
    def test_doorlock_open_kDoorRearLeft_caseid_1982189(self, ecu):       
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)	
        self.soa.notify_RearLeftDoorSts(isopen=True, sts=DoorStatus.kOpened)
        time.sleep(13)
        assert self.tsp.log_search_remote_vehicle_control("DoorCloseFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"        

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_超时右后门状态为TRUE")
    @pytest.mark.full
    def test_doorlock_open_kDoorRearRight_caseid_1982188(self):       
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)	
        self.soa.notify_RearRightDoorSts(isopen=True, sts=DoorStatus.kOpened)
        time.sleep(13)
        assert self.tsp.log_search_remote_vehicle_control("DoorCloseFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"        
        
    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_超时左前门、右前门状态为TRUE")
    @pytest.mark.full
    def test_doorlock_open_kDoorFrontLeft_kDoorFrontRight_caseid_1982187(self):       
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)	
        self.soa.notify_FrntLeftDoorSts(isopen=True, sts=DoorStatus.kOpened)
        self.soa.notify_FrntRightDoorSts(isopen=True, sts=DoorStatus.kOpened) 
        time.sleep(13)
        assert self.tsp.log_search_remote_vehicle_control("DoorCloseFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"        

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_左前门、左后门状态为TRUE")
    @pytest.mark.full
    def test_doorlock_open_kDoorFrontLeft_kDoorRearLeft_caseid_1982186(self):       
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)	
        self.soa.notify_FrntLeftDoorSts(isopen=True, sts=DoorStatus.kOpened)
        self.soa.notify_RearLeftDoorSts(isopen=True, sts=DoorStatus.kOpened)
        time.sleep(13)
        assert self.tsp.log_search_remote_vehicle_control("DoorCloseFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_超时左前门、右后门状态为TRUE")
    @pytest.mark.full
    def test_doorlock_open_kDoorFrontLeft_kDoorRearRight_caseid_1982185(self):       
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)	
        self.soa.notify_FrntLeftDoorSts(isopen=True, sts=DoorStatus.kOpened) 
        self.soa.notify_RearRightDoorSts(isopen=True, sts=DoorStatus.kOpened) 
        time.sleep(13)
        assert self.tsp.log_search_remote_vehicle_control("DoorCloseFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     
                        
    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_左前门、右前门、左后门状态为TRUE")
    @pytest.mark.full
    def test_doorlock_open_kDoorFrontLeft_kDoorRearRight_caseid_1982184(self):       
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)	
        self.soa.notify_FrntLeftDoorSts(isopen=True, sts=DoorStatus.kOpened) 
        self.soa.notify_FrntRightDoorSts(isopen=True, sts=DoorStatus.kOpened) 
        self.soa.notify_RearLeftDoorSts(isopen=True, sts=DoorStatus.kOpened) 
        time.sleep(13)
        assert self.tsp.log_search_remote_vehicle_control("DoorCloseFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     
  
    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_四门状态为开")
    @pytest.mark.full
    def test_doorlock_open_AllDoor_caseid_1982183(self):       
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True, sts=DoorStatus.kOpened) 
        self.soa.notify_FrntRightDoorSts(isopen=True, sts=DoorStatus.kOpened) 
        self.soa.notify_RearLeftDoorSts(isopen=True, sts=DoorStatus.kOpened) 
        self.soa.notify_RearRightDoorSts(isopen=True, sts=DoorStatus.kOpened) 
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)	
        time.sleep(13)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("DoorCloseFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_超时四门和尾门状态为开")
    @pytest.mark.full
    def test_doorlock_open_AllDoor_TailGateSts_kOpened_caseid_1982182(self):       
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True, sts=DoorStatus.kOpened) 
        self.soa.notify_FrntRightDoorSts(isopen=True, sts=DoorStatus.kOpened) 
        self.soa.notify_RearLeftDoorSts(isopen=True, sts=DoorStatus.kOpened) 
        self.soa.notify_RearRightDoorSts(isopen=True, sts=DoorStatus.kOpened) 
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)	
        time.sleep(13)
        assert self.tsp.log_search_remote_vehicle_control("DoorCloseFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_左前门和尾门状态为开")
    @pytest.mark.full
    def test_doorlock_open_kDoorFrontLeft_TailGateSts_kOpened_caseid_1982181(self):       
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True, sts=DoorStatus.kOpened)  
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpened)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)	
        time.sleep(13)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("DoorCloseFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_尾门状态为 kOpening")
    @pytest.mark.full
    def test_doorlock_TailGateSts_kOpening_caseid_1982180(self):       
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kOpening)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)	
        time.sleep(13)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("DoorCloseFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_尾门状态为 kHover")
    @pytest.mark.full
    def test_doorlock_TailGateSts_kHover_caseid_1982179(self):       
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_TailGateService_Status(tailgate_sts=TailGateSts.kHover)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)	
        time.sleep(13)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("DoorCloseFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_超时时间内kFourDoorLockedTailUnlocked")
    @pytest.mark.sanity
    def test_doorlock_CONVENIENCE_LockStatus_FourDoorLockedTailUnlocked_caseid_1982222(self):     
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)	
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=15)
        time.sleep(2)
        self.soa.notify_LockStatus(lock_sts=LockStatus.FourDoorLockedTailUnlocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_超时时间内kFourDoorLockedTailUnlocked")
    @pytest.mark.sanity
    def test_doorlock_CONVENIENCE_LockStatus_FourDoorLockedTailUnlocked_caseid_1982220(self):  
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)     
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,0])
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=15)
        time.sleep(2)
        self.soa.notify_LockStatus(lock_sts=LockStatus.FourDoorLockedTailUnlocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁联动关门_SOAFail")
    @pytest.mark.full
    def test_doorlock_SOAFail_caseid_1982231(self):       
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        time.sleep(0.5)
        self.soa.soa_partner.stop_single_partner("CentralLockService_server")
        time.sleep(10)
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        time.sleep(50)
        assert self.tsp.log_search_remote_vehicle_control("SOAFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      
        self.soa.soa_partner.start_single_partner(service="CentralLockService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("CentralLockService_server",timeout=30)     

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_SOAFail")
    @pytest.mark.full
    def test_unlock_SOAFail_caseid_1982274(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(0.5)
        self.soa.soa_partner.stop_single_partner("CentralLockService_server")
        time.sleep(10)
        execid = self.tsp.rvc_lock_control(1)
        time.sleep(51)
        assert self.tsp.log_search_remote_vehicle_control("SOAFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      
        self.soa.soa_partner.start_single_partner(service="CentralLockService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("CentralLockService_server",timeout=30) 

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_SOAFail")
    @pytest.mark.full
    def test_lock_SOAFail_caseid_1982341(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.soa_partner.stop_single_partner("CentralLockService_server")
        time.sleep(10)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        time.sleep(51)
        assert self.tsp.log_search_remote_vehicle_control("SOAFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      
        self.soa.soa_partner.start_single_partner(service="CentralLockService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("CentralLockService_server",timeout=30) 

    @allure.title("远程解闭锁-RVC_远程四门解闭锁_闭锁_检查休眠")
    @pytest.mark.sanity
    def test_lock_usagdemode_inactive_hibernate_caseid_1982334(self):
        self.io.tcam_kl15_down()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.bus_comm.pause_all_bus_send()
        execid = self.tsp.rvc_lock_control(2)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_VehicleInsidePersonSts()
        # self.soa.check_GetOpenCloseStatus_req_and_feedback_resp({"0": False,"1": False,"2": False,"3": False }, door_id=[4],timeout=10)
        # self.soa.check_TailGateService_GetStatus_req_and_feedback_resp(TailGateSts.kClosed,timeout=10)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=15)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.pause_all_bus_send()
        assert self.mix.check_tcam_sleep(180) == True, 'TCAM远控执行完成之后休眠检查失败'

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁联动关门_休眠")
    @pytest.mark.sanity
    def test_doorlock_INACTIVE_hibernate_caseid_1982223(self):
        self.io.tcam_kl15_down()
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        time.sleep(1)
        self.bus_comm.pause_all_bus_send()
        execid = self.tsp.rvc_lock_control(3)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.pause_all_bus_send()
        assert self.mix.check_tcam_sleep(180) == True, 'TCAM远控执行完成之后休眠检查失败'
              
    @allure.title("远程控制-远程控制-RVC_远程四门解闭锁_闭锁_ABANDONED_TelmFctReq")
    @pytest.mark.full
    def test_lock_usagdemode_abandoned_wake_up_TelmFctReq_caseid_1982343(self, ecu):
        self.io.tcam_kl15_down()  
        self.bus_comm.pause_all_bus_send() 
        sleep(180)
        self.mix.tcam_network_sleep()
        self.bus_comm.check_signal_thread_start("connectivitycanfd","TcamConnectivityFr35", "TelmFctReq", timeout=5)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.notify_VehicleInsidePersonSts()
        result_ori_1 = self.bus_comm.check_signal_thread_stop("TelmFctReq",10)
        logger.info(f'监控到的数据： {result_ori_1}')
        result_1 = check_signal_num(result_ori_1,1)
        frame_times = result_1[0]
        duration_time = result_1[1]
        logger.info(f"持续发送{frame_times}帧，持续时间为{duration_time}s")
        assert frame_times==25, f"检查休眠唤醒后TelmFctReq发送失败"
        sleep(12)

    @allure.title("远程控制-远程控制-RVC_远程四门解闭锁_解锁_ABANDONED_TelmFctReq")
    @pytest.mark.full
    def test_unlock_usagdemode_abandoned_wake_up_TelmFctReq_caseid_1982342(self):
        self.soa.notify_LockStatus(LockStatus.AllLocked)
        self.io.tcam_kl15_down()  
        self.bus_comm.pause_all_bus_send() 
        sleep(180)
        self.mix.tcam_network_sleep()
        self.bus_comm.check_signal_thread_start("connectivitycanfd","TcamConnectivityFr35", "TelmFctReq", timeout=5)
        execid = self.tsp.rvc_lock_control(1)
        result_ori_1 = self.bus_comm.check_signal_thread_stop("TelmFctReq",10)
        logger.info(f'监控到的数据： {result_ori_1}')
        result_1 = check_signal_num(result_ori_1,1)
        frame_times = result_1[0]
        duration_time = result_1[1]
        logger.info(f"持续发送{frame_times}帧，持续时间为{duration_time}s")
        assert frame_times==25, f"检查休眠唤醒后TelmFctReq发送失败"
        sleep(12)

    @allure.title("远程控制-RVC_远程四门解闭锁_不同用户的连续二次远程闭锁")
    @pytest.mark.full
    def test_caseid_1987109(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid1 = self.tsp.rvc_lock_control(2)
        self.tsp.set_bench_config(vid=self.tc_config['vid'],tel='18501735541')
        execid2 = self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid2,num=50),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(13)  # 需要等待第一个指令结束

    @allure.title("远程控制-RVC_远程四门解闭锁_不同用户的闭锁后解锁")
    @pytest.mark.full
    def test_caseid_1987110(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid1 = self.tsp.rvc_lock_control(2)
        self.tsp.set_bench_config(vid=self.tc_config['vid'],tel='18501735541')
        execid2 = self.tsp.rvc_lock_control(1)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid2),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(13)  # 需要等待第一个指令结束

    @allure.title("远程控制-RVC_远程四门解闭锁_不同用户的解锁后闭锁")
    @pytest.mark.full
    def test_caseid_1987111(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        time.sleep(1)
        execid1 = self.tsp.rvc_lock_control(1)
        self.tsp.set_bench_config(vid=self.tc_config['vid'],tel='18501735541')
        execid2 = self.tsp.rvc_lock_control(2)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid2),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(13)  # 需要等待第一个指令结束

    @allure.title("远程控制-RVC_远程四门解闭锁_闭锁_车内有人")
    @pytest.mark.smoke
    def test_lock_usagdemode_abandoned_caseid_1987430(self):
        self.soa.send_Alldoor_close()
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        time.sleep(1)
        execid = self.tsp.rvc_lock_control(2)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi, find_key_type=FindKeyType.NoReq, timeout=10)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_车内有人")
    @pytest.mark.sanity
    def test_caseid_1987431(self):
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        execid = self.tsp.rvc_lock_control(1)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.check_NotifyRVCLockInfo_event(timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程四门解闭锁_解锁_车内无人_ABANDONED")
    @pytest.mark.sanity
    def test_caseid_1987432(self):
        self.io.tcam_kl15_down()  
        self.bus_comm.pause_all_bus_send() 
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        sleep(180)  
        self.mix.tcam_network_sleep()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=20)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=20)
        execid = self.tsp.rvc_lock_control(1)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_VehicleInsidePersonSts()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.check_NotifyRVCLockInfo_event(timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,timeout=1)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,timeout=1)

# pytest -vs -p no:warnings remote_control/basic_remote_control/test_lock.py
