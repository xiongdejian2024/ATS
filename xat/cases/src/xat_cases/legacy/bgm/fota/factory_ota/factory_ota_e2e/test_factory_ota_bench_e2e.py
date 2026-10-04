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

cur_num = 0
@allure.feature("基础架构")
@allure.story("FOTA")
@pytest.mark.stress_test
class TestFota(TestABCBase):
    num = 1 #压测次数
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("CentralLockService","client"),
                         ("TailGateService","client"),
                         ("AcuModeManagerService","server"),
                         ("ChassisService","client")])
        self.mix.back_fota_to(FOTAMasteSts.IDLE, self.taskid)
        self.ssh.update_skip_debug([FOTA_Skip_Debug.factory_ecu_ver_collection])
        self.super_file_name = f"factory_log"
        self.file_name = time.strftime("%m_%d_%H_%H:%M:%S", time.localtime(time.time()))
        self.cur_log_path = ""
        self.start_plane = ""
        log_folder = f"/root/log/{self.super_file_name}"
        os.makedirs(log_folder, exist_ok=True)
        os.makedirs(f"{log_folder}/{self.file_name}", exist_ok=True)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.back_fota_to(FOTAMasteSts.IDLE, self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.IDLE.value, "FOTA Status is not Idle"
        self.mix.set_car_mode(CarMode.FACTORY)  
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @allure.title("E2E_FactoryOTA_Smoke_台架全量刷写")    
    def test_fota_caseid_1983061(self): 
        global cur_num
        cur_num = cur_num + 1
        self.cur_log_path = f"/root/log/{self.super_file_name}/{self.file_name}/{cur_num}"
        os.makedirs(self.cur_log_path, exist_ok=True)
        with allure.step("【Idle】Mock Inactive && Doors Close"):
            self.mix.set_fota_RemoteUpdate_condition(UsageMode.INACTIVE, LockCmd.Lock)
        with allure.step("【Idle】Copy Factory Packages to /update/factory"):
            self.ssh.copy_factory_packages()
        with allure.step("【Idle】Reset BGM"):
            self.sd_tester.reset_bgm()
        with allure.step("【Factory Task】Enter FACTORY_TASK"):
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FACTORY_TASK.value, "FOTA Status is not FACTORY_TASK"
        with allure.step("【Factory Update】StartUpdate"):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with allure.step("【Factory Update】Enter FACTORY_UPDATE"):
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FACTORY_UPDATE.value, "FOTA Status is not FACTORY_UPDATE"
        with allure.step("【Factory Update】Meet All Conditions"):
            self.mix.set_factory_ota_condition(display_hv_soc=260, low_volt_power=14, local_diag_sts=DiagActLineSts.DisActive)
            assert FOTA_ConditionCheck_Code.CR_SUCCESSFUL.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results)
        with allure.step("【Successful】Back to Idle"):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.FACTORY_SUCCESSFUL.value, 1800), "Reach Factory OTA Maximum Timeout: 30min"
        with allure.step("【Successful】Window Calibration"):
            with self.log_manage.check_jetlog_by_keywords(log_type="UpdateNotifyEOLCaliInfoEvent:", 
                                                        keywords= '''UpdateNotifyEOLCaliInfoEvent:{"Device":1,"Status":3,"ErrorCode":0,"NRC":0}''', 
                                                        unexpect_keywords= 'FOTA Status:23',
                                                        timeout=1800):
                pass
        with allure.step("【Successful】Enter FACTORY_SUCCESSFUL"):
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FACTORY_SUCCESSFUL.value, "FOTA Status is not FACTORY_SUCCESSFUL"
        with allure.step("【Successful】Carmode Back to Normal"):
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", 
                                                    keywords='get car mode ret:0 car mode:0',
                                                    unexpect_keywords= 'FOTA Status:23',
                                                    timeout=30):
                    pass
                
    @allure.title("E2E_FactoryOTA_Sanity_台架全量刷写")    
    def test_fota_caseid_1983060(self): 
        global cur_num
        cur_num = cur_num + 1
        self.cur_log_path = f"/root/log/{self.super_file_name}/{self.file_name}/{cur_num}"
        os.makedirs(self.cur_log_path, exist_ok=True)
        with allure.step("【Idle】Check 1.Normal 2.Exist Package"):
            self.mix.set_car_mode(CarMode.NORMAL)
            self.ssh.copy_factory_packages()
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.IDLE.value
            self.mix.set_car_mode(CarMode.FACTORY)
        with allure.step("【Idle】Mock Inactive && Doors Close"):
            self.mix.set_fota_RemoteUpdate_condition(UsageMode.INACTIVE, LockCmd.Lock)
        with allure.step("【Idle】Reset BGM"):
            self.sd_tester.reset_bgm()
        with allure.step("【Factory Task】Enter FACTORY_TASK"):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.FACTORY_TASK.value, 30), "FOTA Status is not FACTORY_TASK"
        with allure.step("【Factory Update】Meet All Conditions"):
            self.mix.set_factory_ota_condition(display_hv_soc=260, low_volt_power=14, local_diag_sts=DiagActLineSts.Active)
        with allure.step("【Factory Update】Steel Wheel > 3s"):
            self.bus_comm.trigger_steer_wheel(time_interval=3.5)
        with allure.step("【Factory Update】Enter FACTORY_UPDATE"):
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FACTORY_UPDATE.value, "FOTA Status is not FACTORY_UPDATE"
            assert FOTA_ConditionCheck_Code.CR_SUCCESSFUL.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results)
        with allure.step("【Successful】Back to Idle"):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.FACTORY_SUCCESSFUL.value, 1800), "Reach Factory OTA Maximum Timeout: 30min"
        with allure.step("【Successful】Window Calibration"):
            with self.log_manage.check_jetlog_by_keywords(log_type="UpdateNotifyEOLCaliInfoEvent:", 
                                                        keywords= '''UpdateNotifyEOLCaliInfoEvent:{"Device":1,"Status":3,"ErrorCode":0,"NRC":0}''', 
                                                        unexpect_keywords= 'FOTA Status:23',
                                                        timeout=1800):
                pass
        with allure.step("【Successful】Enter FACTORY_SUCCESSFUL"):
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FACTORY_SUCCESSFUL.value, "FOTA Status is not FACTORY_SUCCESSFUL"
        with allure.step("【Successful】Carmode Back to Normal"):
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", 
                                                    keywords='get car mode ret:0 car mode:0',
                                                    unexpect_keywords= 'FOTA Status:23',
                                                    timeout=30):
                    pass
   
    @allure.title("E2E_FactoryOTA_Full_台架全量刷写")    
    def test_fota_caseid_1983059(self): 
        global cur_num
        cur_num = cur_num + 1
        self.cur_log_path = f"/root/log/{self.super_file_name}/{self.file_name}/{cur_num}"
        os.makedirs(self.cur_log_path, exist_ok=True)
        with allure.step("【Idle】Mock Inactive && Doors Close"):
            self.mix.set_fota_RemoteUpdate_condition(UsageMode.INACTIVE, LockCmd.Lock)
        with allure.step("【Idle】Reset BGM"):
            self.sd_tester.reset_bgm()
        with allure.step("【Idle】Check When No package, OTA Master Behavior"):
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", 
                                                    keywords='factory_file_suffix is not match',
                                                    unexpect_keywords= 'FOTA Status:23',
                                                    timeout=30):
                    pass            
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.IDLE.value, "FOTA Status is not IDLE"
        with allure.step("【Idle】Copy Factory Packages to /update/factory"):
            self.ssh.copy_factory_packages()
        with allure.step("【Factory Task】Enter FACTORY_TASK"):
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FACTORY_TASK.value, "FOTA Status is not FACTORY_TASK"
        with allure.step("【Factory Update】Not Meet Any Conditions"):
            self.mix.set_factory_ota_condition(display_hv_soc=200, low_volt_power=11, local_diag_sts=DiagActLineSts.Active)
        with allure.step("【Factory Update】Steel Wheel > 3s"):
            self.bus_comm.trigger_steer_wheel(time_interval=3.5)
        with allure.step("【Factory Update】Check ConditionCheck Results, Diag Online"):
            assert FOTA_ConditionCheck_Code.CR_DIAGNOSTIC_ERROR.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results)
        with allure.step("【Factory Update】Check ConditionCheck Results, Diag Offline"):
            self.io.bgm_diag_line_down()
            assert FOTA_ConditionCheck_Code.CR_HV_ERROR.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results) and\
                   FOTA_ConditionCheck_Code.CR_LV_ERROR.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results)
        with allure.step("【Factory Update】Meet All Conditions"):
            self.mix.set_factory_ota_condition(display_hv_soc=260, low_volt_power=14, local_diag_sts=DiagActLineSts.DisActive)
        with allure.step("【Factory Update】Enter FACTORY_UPDATE"):
            assert FOTA_ConditionCheck_Code.CR_SUCCESSFUL.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results)
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FACTORY_UPDATE.value, "FOTA Status is not FACTORY_UPDATE"
        with allure.step("【Successful】Back to Idle"):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.FACTORY_SUCCESSFUL.value, 1800), "Reach Factory OTA Maximum Timeout: 30min"
        with allure.step("【Successful】Window Calibration"):
            with self.log_manage.check_jetlog_by_keywords(log_type="UpdateNotifyEOLCaliInfoEvent:", 
                                                        keywords= '''UpdateNotifyEOLCaliInfoEvent:{"Device":1,"Status":3,"ErrorCode":0,"NRC":0}''', 
                                                        unexpect_keywords= 'FOTA Status:23',
                                                        timeout=1800):
                pass
        with allure.step("【Successful】Enter FACTORY_SUCCESSFUL"):
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FACTORY_SUCCESSFUL.value, "FOTA Status is not FACTORY_SUCCESSFUL"
        with allure.step("【Successful】Carmode Back to Normal"):
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", 
                                                    keywords='get car mode ret:0 car mode:0',
                                                    unexpect_keywords= 'FOTA Status:23',
                                                    timeout=30):
                    pass   
        
if __name__ == "__main__":
    pass



