import os
import sys
import pytest
import allure
from time import sleep
import random

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("V2TRoutingForwarder","client","V2TOTAFotaForwarder"),
                         ("CentralLockService","client"),
                         ("TailGateService","client"),
                         ("AcuModeManagerService","server"),
                         ("RtcAlarmService","client"),
                         ("ChassisService","client")])
        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                                    FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.before_group_hv_ctl,
                                    FOTA_Skip_Debug.ecm3_down_hv,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check
                                    ]) 
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])
        self.ssh.update_ua_skip(DOMAIN.BGM,False)
        

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value 
        self.soa.send_fota_request(MASTER_REQUEST.CancelAppointment, args={"taskId":self.taskid})
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == 0, "Appiontment Information Exist"  #当前无预约事件
                    
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
    
    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("进入RemoteUpdate条件_wait_hmi") 
    def test_fota_caseid_1984888(self):
        self.mix.set_fota_RemoteUpdate_condition(UsageMode.INACTIVE, LockCmd.Lock)
        self.soa.trigger_fota_type90(self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Status ≠ REMOTE_UPDATE"
        
    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("进入RemoteUpdate条件_wait_clock") 
    def test_fota_caseid_1984887(self):
        appoint_time = self.mix.generate_fota_appointment_time()
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args={"taskId":self.taskid, "time":appoint_time})
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == appoint_time, "No scheduled events are currently available"
        self.mix.set_fota_RemoteUpdate_condition(UsageMode.INACTIVE, LockCmd.Lock)
        self.soa.trigger_fota_type90(self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Status ≠ REMOTE_UPDATE"
        
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("进入RemoteUpdate条件_taskid_wait_hmi") 
    def test_fota_caseid_1984886(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0430', timeout=60):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.trigger_fota_type90(random.randint(0, self.taskid))
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("进入RemoteUpdate条件_taskid_wait_clock") 
    def test_fota_caseid_1984885(self):
        appoint_time = self.mix.generate_fota_appointment_time()
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args={"taskId":self.taskid, "time":appoint_time})
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == appoint_time, "No scheduled events are currently available"
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0430', timeout=10):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.trigger_fota_type90(random.randint(0, self.taskid))
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("进入RemoteUpdate条件_status_Idle") 
    def test_fota_caseid_1984884(self):
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.IDLE.value, "FOTA Status ≠ Idle"
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='event EVENT_REMOTE_UPDATE discarded', timeout=10):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.trigger_fota_type90(self.taskid)
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("进入RemoteUpdate条件_status_Query") 
    
    def test_fota_caseid_1984883(self):
        self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status, wait=False) == FOTAMasteSts.QUERY.value, "FOTA Status ≠ QUERY"
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='event EVENT_REMOTE_UPDATE discarded', timeout=10):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.trigger_fota_type90(self.taskid)
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("进入RemoteUpdate条件_status_New_Task") 
    def test_fota_caseid_1984882(self):
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.NEW_TASK.value, "FOTA Status ≠ NEW_TASK"
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='event EVENT_REMOTE_UPDATE discarded', timeout=10):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.trigger_fota_type90(self.taskid)
        
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("进入RemoteUpdate条件_status_Download") 
    def test_fota_caseid_1984881(self):
        self.mix.back_fota_to(FOTAMasteSts.DOWNLOADING, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.DOWNLOADING.value, "FOTA Status ≠ DOWNLOADING"
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='event EVENT_REMOTE_UPDATE discarded', timeout=10):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.trigger_fota_type90(self.taskid)
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("进入RemoteUpdate条件_status_ReachAppointment") 
    def test_fota_caseid_1984877(self):
        self.mix.back_fota_to(FOTAMasteSts.REACH_APPOINTMENT, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REACH_APPOINTMENT.value, "FOTA Status ≠ REACH_APPOINTMENT"
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0431', timeout=10):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.trigger_fota_type90(self.taskid)
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("进入RemoteUpdate条件_status_Update") 
    def test_fota_caseid_1984880(self):
        self.mix.back_fota_to(FOTAMasteSts.UPDATE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.UPDATE.value, "FOTA Status ≠ UPDATE"
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='event EVENT_REMOTE_UPDATE discarded', timeout=10):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.trigger_fota_type90(self.taskid)
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("进入RemoteUpdate条件_status_Failed_Can_Not_Driving") 
    def test_fota_caseid_1984879(self):
        self.mix.back_fota_to(FOTAMasteSts.FAILED_NOT_DRIVING, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value, "FOTA Status ≠ FAILED_NOT_DRIVING"
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='event EVENT_REMOTE_UPDATE discarded', timeout=10):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.trigger_fota_type90(self.taskid)
            
    # @pytest.mark.V_1_4
    # @pytest.mark.full
    # @allure.title("进入RemoteUpdate条件_status_Failed_Can_Driving") 
    # def test_fota_caseid_1984878(self):
    #     self.mix.back_fota_to(FOTAMasteSts.FAILED_DRIVING, taskid=self.taskid)
    #     assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_DRIVING.value, "FOTA Status ≠ FAILED_DRIVING"
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='event EVENT_REMOTE_UPDATE discarded', timeout=10):
    #         time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
    #         self.soa.trigger_fota_type90(self.taskid)
    
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("进入RemoteUpdate条件_status_Remote_Update") 
    def test_fota_caseid_1984932(self):
        self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Status ≠ REMOTE_UPDATE"
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0431', timeout=10):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.trigger_fota_type90(self.taskid)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("进入RemoteUpdate条件_车内是否有人_LockStatus=1(Unlock)") 
    def test_fota_caseid_1984876(self):      
        self.mix.set_fota_RemoteUpdate_condition(UsageMode.INACTIVE, LockCmd.UnLock)
        assert self.soa.send_request_and_ck_resp('CentralLockService_client', 'GetLockStatus', {}, {"out":1}), "LockStatus ≠ 1 (Unlock)"
        self.soa.trigger_fota_type90(self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "FOTA Status ≠ ACTIVE"
        
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("进入RemoteUpdate条件_车内是否有人_LockStatus=2(四门上锁尾门解锁)") 
    def test_fota_caseid_1984875(self):      
        self.mix.set_fota_RemoteUpdate_condition(UsageMode.INACTIVE, LockCmd.Lock)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        assert self.soa.send_request_and_ck_resp('CentralLockService_client', 'GetLockStatus', {}, {"out":2}), "LockStatus ≠ 2 (四门上锁尾门解锁)"
        self.soa.trigger_fota_type90(self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "FOTA Status ≠ ACTIVE"
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("进入RemoteUpdate条件_车内是否有人_ABANDONED") 
    def test_fota_caseid_1984873(self):      
        self.mix.set_fota_RemoteUpdate_condition(UsageMode.ABANDONED, LockCmd.Lock)
        time.sleep(10)
        self.soa.trigger_fota_type90(self.taskid)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.ACTIVE.value, 300), "FOTA Status ≠ ACTIVE"
        
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("进入RemoteUpdate条件_车内是否有人_CONVENIENCE") 
    def test_fota_caseid_1984872(self):      
        self.mix.set_fota_RemoteUpdate_condition(UsageMode.CONVENIENCE, LockCmd.Lock)
        time.sleep(10)
        self.soa.trigger_fota_type90(self.taskid)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.ACTIVE.value, 300), "FOTA Status ≠ ACTIVE"

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("进入RemoteUpdate条件_车内是否有人_ACTIVE") 
    def test_fota_caseid_1984871(self):      
        self.mix.set_fota_RemoteUpdate_condition(UsageMode.ACTIVE, LockCmd.Lock)
        time.sleep(10)
        self.soa.trigger_fota_type90(self.taskid)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.ACTIVE.value, 300), "FOTA Status ≠ ACTIVE"

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("进入RemoteUpdate条件_车内是否有人_DRIVING") 
    def test_fota_caseid_1984870(self):      
        self.mix.set_fota_RemoteUpdate_condition(UsageMode.DRIVING, LockCmd.Lock)
        time.sleep(10)
        self.soa.trigger_fota_type90(self.taskid)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.ACTIVE.value, 300), "FOTA Status ≠ ACTIVE"
        
    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("RemoteUpdate状态") 
    def test_fota_caseid_1984869(self):    
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"04F5', timeout=600):
            self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, taskid=self.taskid)  
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("RemoteUpdate状态_SetFirstCheckResult_0420") 
    def test_fota_caseid_1984867(self):    
        self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, taskid=self.taskid)  
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0420', timeout=20):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.SetFirstCheckResult,args={"sts":{"errorCode":FirstCheck_ErrorCode.FirstCheck_HVSOCLow_0x04_0x20.value}})

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("RemoteUpdate状态_SetFirstCheckResult_0421") 
    def test_fota_caseid_1984866(self):    
        self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, taskid=self.taskid)  
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0421', timeout=20):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.SetFirstCheckResult,args={"sts":{"errorCode":FirstCheck_ErrorCode.FirstCheck_NotInPark_0x04_0x21.value}})
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("RemoteUpdate状态_SetFirstCheckResult_0422") 
    def test_fota_caseid_1984865(self):    
        self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, taskid=self.taskid)  
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0422', timeout=20):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.SetFirstCheckResult,args={"sts":{"errorCode":FirstCheck_ErrorCode.FirstCheck_VehicleSpeed_0x04_0x22.value}})

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("RemoteUpdate状态_SetFirstCheckResult_0423") 
    def test_fota_caseid_1984864(self):    
        self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, taskid=self.taskid)  
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0423', timeout=20):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.SetFirstCheckResult,args={"sts":{"errorCode":FirstCheck_ErrorCode.UserChoosePause_0x04_0x23.value}})

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("RemoteUpdate状态_终极校验_仲裁不通过") 
    def test_fota_caseid_1984863(self):    
        self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, taskid=self.taskid)  
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.Active)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"040C', timeout=20):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "FOTA Status ≠ ACTIVE"      

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("RemoteUpdate状态_终极校验_Vehicle speed value != 0") 
    def test_fota_caseid_1984862(self):    
        self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, taskid=self.taskid)  
        self.mix.set_normal_fota_update_condition(vehspd=100, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0402', timeout=20):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "FOTA Status ≠ ACTIVE"      

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("RemoteUpdate状态_终极校验_HVSOC小于25%") 
    def test_fota_caseid_1984861(self):    
        self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, taskid=self.taskid)  
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=240, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0404', timeout=20):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "FOTA Status ≠ ACTIVE"      

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("RemoteUpdate状态_终极校验_热失控") 
    def test_fota_caseid_1984860(self):    
        self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, taskid=self.taskid)  
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=True, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0405', timeout=20):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "FOTA Status ≠ ACTIVE"      

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("RemoteUpdate状态_终极校验_smallBatterySoc小于70") 
    def test_fota_caseid_1984859(self):    
        self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, taskid=self.taskid)  
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=69, local_diag_sts=DiagActLineSts.DisActive)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0406', timeout=20):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "FOTA Status ≠ ACTIVE"      

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("RemoteUpdate状态_终极校验_GearLevelSts不为Park") 
    def test_fota_caseid_1984858(self):    
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Undefd, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
        self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, taskid=self.taskid)  
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0403', timeout=20):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "FOTA Status ≠ ACTIVE"      

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("RemoteUpdate状态下重启") 
    def test_fota_caseid_1984843(self):    
        self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, taskid=self.taskid)  
        self.sd_tester.reset_bgm()
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "FOTA Status ≠ ACTIVE"      
        
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("RemoteUpdate状态下diag_cancel") 
    def test_fota_caseid_1984842(self):    
        self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, taskid=self.taskid)  
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Status ≠ REMOTE_UPDATE"
        self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 60), "FOTA Status ≠ IDLE"
        
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("RemoteUpdate状态下vsp_cancel") 
    def test_fota_caseid_1984935(self):    
        self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, taskid=self.taskid)  
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Status ≠ REMOTE_UPDATE"
        self.tsp.trigger_vsp_fota(VSP.Cancel, self.taskid)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 60), "FOTA Status ≠ IDLE"
    
    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("仲裁及其他异常_无预约信息开始手机OTA_SetFirstCheckResult") 
    def test_fota_caseid_1984857(self):    
        self.mix.set_fota_RemoteUpdate_condition(UsageMode.INACTIVE, LockCmd.Lock)
        self.soa.trigger_fota_type90(self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Status ≠ REMOTE_UPDATE"
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"04F6"', timeout=20):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.SetFirstCheckResult,args={"sts":{"errorCode":FirstCheck_ErrorCode.UserChoosePause_0x04_0x23.value}})
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "FOTA Status ≠ ACTIVE"      
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == 0, "Appiontment Information Exist"        

    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("仲裁及其他异常_无预约信息开始手机OTA_终极校验条件不通过") 
    def test_fota_caseid_1984856(self):    
        self.mix.set_fota_RemoteUpdate_condition(UsageMode.INACTIVE, LockCmd.Lock)
        self.soa.trigger_fota_type90(self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Status ≠ REMOTE_UPDATE"
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Undefd, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.Active)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"04F6"', timeout=20):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "FOTA Status ≠ ACTIVE"      
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == 0, "Appiontment Information Exist"        
        
    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("仲裁及其他异常_预约信息开始手机OTA_SetFirstCheckResult") 
    def test_fota_caseid_1984855(self):    
        appoint_time = self.mix.generate_fota_appointment_time()
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args={"taskId":self.taskid, "time":appoint_time})
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == appoint_time, "No scheduled events are currently available"
        self.mix.set_fota_RemoteUpdate_condition(UsageMode.INACTIVE, LockCmd.Lock)
        self.soa.trigger_fota_type90(self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Status ≠ REMOTE_UPDATE"
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"04F6"', timeout=20):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.SetFirstCheckResult,args={"sts":{"errorCode":FirstCheck_ErrorCode.UserChoosePause_0x04_0x23.value}})
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "FOTA Status ≠ ACTIVE"      
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == appoint_time, "Appiontment Information Exist"  
        
    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("仲裁及其他异常_预约信息开始手机OTA_终极校验条件不通过") 
    def test_fota_caseid_1984854(self):    
        appoint_time = self.mix.generate_fota_appointment_time()
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args={"taskId":self.taskid, "time":appoint_time})
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == appoint_time, "No scheduled events are currently available"
        self.mix.set_fota_RemoteUpdate_condition(UsageMode.INACTIVE, LockCmd.Lock)
        self.soa.trigger_fota_type90(self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Status ≠ REMOTE_UPDATE"
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.Active)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"04F6"', timeout=20):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "FOTA Status ≠ ACTIVE"
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == appoint_time, "Appiontment Information Exist"  

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("仲裁及其他异常_预约时间到达后收到手机OTA消息_Reachappoint") 
    def test_fota_caseid_1984853(self):    
        appoint_time = self.mix.generate_fota_appointment_time(120)
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args={"taskId":self.taskid, "time":appoint_time})
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == appoint_time, "No scheduled events are currently available"
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.REACH_APPOINTMENT.value, 180), "FOTA Status ≠ REACH_APPOINTMENT"
        self.mix.set_fota_RemoteUpdate_condition(UsageMode.INACTIVE, LockCmd.Lock)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0431"', timeout=20):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.trigger_fota_type90(self.taskid)
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("仲裁及其他异常_预约时间到达后收到手机OTA消息_Update") 
    def test_fota_caseid_1984852(self):    
        self.mix.back_fota_to(FOTAMasteSts.UPDATE, taskid=self.taskid)  
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.UPDATE.value, "FOTA Status ≠ UPDATE"
        self.mix.set_fota_RemoteUpdate_condition(UsageMode.INACTIVE, LockCmd.Lock)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='event EVENT_REMOTE_UPDATE discarded', timeout=20):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.trigger_fota_type90(self.taskid)

    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("仲裁及其他异常_有预约信息用户车机立即升级_SetFirstCheckResult") 
    def test_fota_caseid_1984851(self):    
        appoint_time = self.mix.generate_fota_appointment_time()
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args={"taskId":self.taskid, "time":appoint_time})
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == appoint_time, "No scheduled events are currently available"
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0423"', timeout=20):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.SetFirstCheckResult,args={"sts":{"errorCode":FirstCheck_ErrorCode.UserChoosePause_0x04_0x23.value}})
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "FOTA Status ≠ ACTIVE"      
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == appoint_time, "Appiontment Information not Exist"
        
    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("仲裁及其他异常_有预约信息用户车机立即升级_终极校验条件不通过") 
    def test_fota_caseid_1984936(self):    
        appoint_time = self.mix.generate_fota_appointment_time()
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args={"taskId":self.taskid, "time":appoint_time})
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == appoint_time, "No scheduled events are currently available"
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.Active)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"040C"', timeout=20):
            time.sleep(2) #statecode发送太快, 需要sleep 2s等log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "FOTA Status ≠ ACTIVE"      
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == appoint_time, "Appiontment Information not Exist"
    
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("仲裁及其他异常_在APPFOTA状态下(有预约信息)收到SetAppointment") 
    def test_fota_caseid_1984850(self):    
        appoint_time_A = self.mix.generate_fota_appointment_time()
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args={"taskId":self.taskid, "time":appoint_time_A})
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == appoint_time_A, "No scheduled events are currently available"
        self.mix.set_fota_RemoteUpdate_condition(UsageMode.INACTIVE, LockCmd.Lock)
        self.soa.trigger_fota_type90(self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Status ≠ REMOTE_UPDATE"
        appoint_time_B = random.randint(appoint_time_A + 60, appoint_time_A + 60000)
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args={"taskId":self.taskid, "time":appoint_time_B})
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == appoint_time_A, "appoint_time_A is Changed"

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("仲裁及其他异常_在APPFOTA状态下(无预约信息)收到SetAppointment") 
    def test_fota_caseid_1984849(self): 
        self.mix.set_fota_RemoteUpdate_condition(UsageMode.INACTIVE, LockCmd.Lock)
        self.soa.trigger_fota_type90(self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Status ≠ REMOTE_UPDATE"   
        appoint_time_A = self.mix.generate_fota_appointment_time()
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args={"taskId":self.taskid, "time":appoint_time_A})
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == 0, "Appiontment Information Exist"
        
    # @pytest.mark.V_1_4
    # @pytest.mark.full
    # @allure.title("仲裁及其他异常_手机升级触发时预约时间到达且升级未开始(SetFirstCheckResult)") 
    # def test_fota_caseid_1984847(self): 
    #     appoint_time_A = self.mix.generate_fota_appointment_time(120)
    #     self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args={"taskId":self.taskid, "time":appoint_time_A})
    #     assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == appoint_time_A, "No scheduled events are currently available"
    #     time.sleep(2)
    #     real_appiontment_time = self.soa.get_fota_notifybookinfolist(NotifyBookInfoListEVENT.startTime)
    #     sleep(real_appiontment_time - 90)
    #     self.mix.set_fota_RemoteUpdate_condition(UsageMode.INACTIVE, LockCmd.Lock)
    #     self.soa.trigger_fota_type90(self.taskid)
    #     assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Status ≠ REMOTE_UPDATE"
    #     self.mix.return_when_reach_target_time(real_appiontment_time + 10, 2) #预约有效期600s
    #     self.soa.send_fota_request(MASTER_REQUEST.SetFirstCheckResult,args={"sts":{"errorCode":FirstCheck_ErrorCode.UserChoosePause_0x04_0x23.value}})
    #     assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "FOTA Status ≠ REACH_APPOINTMENT"      
    #     assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == 0, "Appiontment Information Exist"
        
    # @pytest.mark.V_1_4
    # @pytest.mark.full
    # @allure.title("仲裁及其他异常_手机升级触发时预约时间到达且升级未开始(终极校验条件不通过)") 
    # def test_fota_caseid_1984846(self): 
    #     appoint_time_A = self.mix.generate_fota_appointment_time(120)
    #     self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args={"taskId":self.taskid, "time":appoint_time_A})
    #     assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == appoint_time_A, "No scheduled events are currently available"
    #     real_appiontment_time = self.soa.get_fota_notifybookinfolist(NotifyBookInfoListEVENT.startTime)
    #     sleep(real_appiontment_time - 90)
    #     self.mix.set_fota_RemoteUpdate_condition(UsageMode.INACTIVE, LockCmd.Lock)
    #     self.soa.trigger_fota_type90(self.taskid)
    #     assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Status ≠ REMOTE_UPDATE"
    #     self.mix.return_when_reach_target_time(real_appiontment_time + 10, 2) #预约有效期600s
    #     self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.Active)
    #     self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
    #     assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.ACTIVE.value, 300)
    #     assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == 0, "Appiontment Information Exist"

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("仲裁及其他异常_在有预约信息的APPFOTA状态下收到cancelAppointment") 
    def test_fota_caseid_1984845(self):
        appoint_time_A = self.mix.generate_fota_appointment_time()
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args={"taskId":self.taskid, "time":appoint_time_A})
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == appoint_time_A, "No scheduled events are currently available"
        self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, taskid=self.taskid), "FOTA Status ≠ REMOTE_UPDATE"
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Status ≠ REMOTE_UPDATE"
        self.soa.send_fota_request(MASTER_REQUEST.CancelAppointment, {"taskId":self.taskid})
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == appoint_time_A, "No scheduled events are currently available"
        self.soa.send_fota_request(MASTER_REQUEST.SetFirstCheckResult,args={"sts":{"errorCode":FirstCheck_ErrorCode.UserChoosePause_0x04_0x23.value}})
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "FOTA Status ≠ ACTIVE"  
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == appoint_time_A, "No scheduled events are currently available"

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("仲裁及其他异常_在无预约信息的APPFOTA状态下收到cancelAppointment") 
    def test_fota_caseid_1984844(self):
        self.soa.send_fota_request(MASTER_REQUEST.CancelAppointment, {"taskId":self.taskid})
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == 0, "Appiontment Information Exist"
        self.soa.send_fota_request(MASTER_REQUEST.SetFirstCheckResult,args={"sts":{"errorCode":FirstCheck_ErrorCode.UserChoosePause_0x04_0x23.value}})
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "FOTA Status ≠ ACTIVE"  
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == 0, "Appiontment Information Exist"

    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("RemoteUpdate状态_超时_04F6(ReturnActive)") 
    def test_fota_caseid_1984937(self):
        self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, taskid=self.taskid), "FOTA Status ≠ REMOTE_UPDATE"
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Status ≠ REMOTE_UPDATE"
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"04F6"', timeout=320):
            pass

    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("RemoteUpdate状态_维持唤醒+超时_0435(APPFOTATimeOUT)") 
    def test_fota_caseid_1984868(self):
        self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, taskid=self.taskid), "FOTA Status ≠ REMOTE_UPDATE"
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Status ≠ REMOTE_UPDATE"
        assert self.mix.check_fota_keep_awake(pnc29=True, acu_keep_alive=True, up_inactive=True)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0435"', timeout=320):
            pass
        assert self.mix.check_fota_keep_awake(pnc29=False, acu_keep_alive=False, up_inactive=False)

    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("仲裁及其他异常_手机升级触发时预约时间到达") 
    def test_fota_caseid_1984848(self):
        appoint_time_A = self.mix.generate_fota_appointment_time()
        self.soa.send_fota_request(MASTER_REQUEST.SetAppointment, args={"taskId":self.taskid, "time":appoint_time_A})
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == appoint_time_A, "No scheduled events are currently available"
        self.mix.back_fota_to(FOTAMasteSts.UPDATE, taskid=self.taskid), "FOTA Status ≠ UPDATE"
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1800)
        assert self.soa.send_fota_request(MASTER_REQUEST.GetAppointment, args={"taskId":self.taskid}) == 0, "Appiontment Information Exist"

if __name__ == "__main__":
    pass

    




