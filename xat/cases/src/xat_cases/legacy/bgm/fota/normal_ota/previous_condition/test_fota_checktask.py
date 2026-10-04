import os
import sys
import pytest
import allure
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature("基础架构")
@allure.story("FOTA")
class TestFotaSleep(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("CentralLockService","client")])
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
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ])
        self.ssh.update_ua_skip(DOMAIN.BGM, allow_same_version_flash=False)
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])    

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        cen_lock_sts = self.bus_comm.get_central_lock_sts()
        if cen_lock_sts == 3:
            self.bus_comm.send_nfc_cmd()
            self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.NFC)
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.smoke
    @pytest.mark.V_1_4
    @allure.title("FOTA休眠唤醒") 
    def test_fota_caseid_1979785(self):
        self.mix.fota_back_to_idle()
        try:
            self.mix.network_sleep()
        except Exception as e:
            logger.error(e)
        self.tsp.trigger_vsp_fota(VSP.Repub, task_id=self.taskid)
        time.sleep(60)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="UpdateFotaState:Send FOTA Status:2", timeout=120):
            pass

@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("CentralLockService","client")])
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
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ])
        self.ssh.update_ua_skip(DOMAIN.BGM, allow_same_version_flash=False)
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        cen_lock_sts = self.bus_comm.get_central_lock_sts()
        if cen_lock_sts == 3:
            self.bus_comm.send_nfc_cmd()
            self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.NFC)
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.full
    @pytest.mark.V_1_4
    @allure.title("车机界面触发_Idle") 
    def test_fota_caseid_1979784(self):
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        with allure.step("当前FOTA Status = Idle"):        
            assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status,target_status=FOTAMasteSts.IDLE.value, timeout=30)
        with allure.step("触发check_task，检查是否触发type 10"):
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"type":10', timeout=90):
                sleep(2)
                self.soa.send_fota_request(MASTER_REQUEST.CheckTask, {'cmd': 0}) 

    @pytest.mark.smoke
    @pytest.mark.V_2_0
    @allure.title("车机界面触发_Idle状态下_设置Flag") 
    def test_fota_caseid_1987610(self):
        self.mix.back_fota_to(FOTAMasteSts.SUCCESSFUL, taskid=self.taskid)
        with allure.step("当前FOTA Status = Idle"):        
            assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status,target_status=FOTAMasteSts.IDLE.value, timeout=30)
        with allure.step("触发check_task，检查是否触发type 10"):
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"type":10',
                                                                                       'UpdateFotaState:Send FOTA Status:0, task id:0, error code:0, serial number:1, task type:0'
                                                                                      ], timeout=90):
                sleep(2)
                self.soa.send_fota_request(MASTER_REQUEST.CheckTask, {'cmd': 0}) 


    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("车机界面触发_非Idle") 
    def test_fota_caseid_1979783(self):
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
        with allure.step("当前FOTA Status = Idle, repub task"):
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.IDLE.value
            self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
        with allure.step("当FOTA Status = Query时, 触发check_task，检查是否触发type 10"):
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.QUERY.value
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords='"type":10', timeout=90):
                sleep(2)
                self.soa.send_fota_request(MASTER_REQUEST.CheckTask, {'cmd': 0}) 

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("OTA FOTA任务_云端无任务") 
    def test_fota_caseid_1979772(self):
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.IDLE.value
        self.soa.send_fota_request(MASTER_REQUEST.CheckTask, {'cmd': 0}) 
        assert self.soa.get_fota_status(MASTER_EVENT.TaskId) == 0
        
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("OTA FOTA任务_云端有任务_车端有任务_taskid一致") 
    def test_fota_caseid_1979771(self):
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.IDLE.value
        self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.QUERY.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"code":0,"msg":"not in wait task state"', timeout=120):
            self.tsp.trigger_vsp_fota(VSP.Reset, task_id=self.taskid)
            self.tsp.trigger_vsp_fota(VSP.Repub, task_id=self.taskid)
    
    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("OTA FOTA任务_云端有任务_车端无任务") 
    def test_fota_caseid_1979770(self):
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.IDLE.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"code":1,"msg":"ok"', timeout=120):
            self.tsp.trigger_vsp_fota(VSP.Reset, task_id=self.taskid)
            self.tsp.trigger_vsp_fota(VSP.Repub, task_id=self.taskid)

    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("车辆周期性请求后台获取FOTA任务_Convience_2h_Idle") 
    def test_fota_caseid_1979781(self):
        self.mix.set_car_mode(CarMode.DYNO)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        self.ssh.update_skip_debug([FOTA_Skip_Debug.time_check], allow_sleep=False) 
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords= ['car mode is not NORMAL or FACTORY'], timeout=35):
            pass
        self.mix.set_car_mode(CarMode.NORMAL)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords= ['CheckPreCondition:vehicle mode:'], timeout=60):
            pass
        time.sleep(30) #等待 OTA Master进入init
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords= ['"type":10'], timeout=30):
            self.mix.set_usage_mode(UsageMode.CONVENIENCE)
            
    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("车辆周期性请求后台获取FOTA任务_Driving_2h_Idle") 
    def test_fota_caseid_1979778(self):
        self.mix.set_car_mode(CarMode.DYNO)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        self.ssh.update_skip_debug([FOTA_Skip_Debug.time_check], allow_sleep=False) 
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords= ['car mode is not NORMAL or FACTORY'], timeout=35):
            pass
        self.mix.set_car_mode(CarMode.NORMAL)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords= ['CheckPreCondition:vehicle mode:'], timeout=60):
            pass
        time.sleep(30) #等待 OTA Master进入init
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords= ['"type":10'], timeout=30):
            self.mix.set_usage_mode(UsageMode.DRIVING)
            
    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("车辆周期性请求后台获取FOTA任务_Active_2h_Idle") 
    def test_fota_caseid_1979773(self):
        self.mix.set_car_mode(CarMode.DYNO)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        self.ssh.update_skip_debug([FOTA_Skip_Debug.time_check], allow_sleep=False) 
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords= ['car mode is not NORMAL or FACTORY'], timeout=35):
            pass
        self.mix.set_car_mode(CarMode.NORMAL)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords= ['CheckPreCondition:vehicle mode:'], timeout=60):
            pass
        time.sleep(30) #等待 OTA Master进入init
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords= ['"type":10'], timeout=30):
            self.mix.set_car_mode(CarMode.NORMAL)
            self.mix.set_usage_mode(UsageMode.ACTIVE)   
            
    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("车辆周期性请求后台获取FOTA任务_Inactive_2h_Idle") 
    def test_fota_caseid_1979774(self):
        self.mix.set_car_mode(CarMode.DYNO)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        self.ssh.update_skip_debug([FOTA_Skip_Debug.time_check], allow_sleep=False) 
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords= ['car mode is not NORMAL or FACTORY'], timeout=35):
            pass
        self.mix.set_car_mode(CarMode.NORMAL)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords= ['CheckPreCondition:vehicle mode:'], timeout=60):
            pass
        time.sleep(30) #等待 OTA Master进入init
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords= ['"type":10'], timeout=30):
            self.mix.set_car_mode(CarMode.NORMAL)
            self.mix.set_usage_mode(UsageMode.INACTIVE)  

if __name__ == "__main__":
    pass