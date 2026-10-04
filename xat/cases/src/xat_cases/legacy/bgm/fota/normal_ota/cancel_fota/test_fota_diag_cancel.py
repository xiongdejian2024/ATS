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
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service")])
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
                                    FOTA_Skip_Debug.update_precondition_check
                                    ], allow_sleep=False) 
        self.ssh.update_ua_skip(DOMAIN.BGM, allow_same_version_flash=False, allow_sleep=False)
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])    
        time.sleep(20)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.ssh.set_airplane_mode(isOn.Off)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.ssh.set_airplane_mode(isOn.Off)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("诊断_OTA Cancel_Query")    
    def test_fota_caseid_1982940(self):
        self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.QUERY.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0505"', timeout=120):
            self.sd_tester.diag_cancel()
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120)

    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("诊断_OTA Cancel_Download_停止唤醒")    
    def test_fota_caseid_1982939(self):
        self.mix.update_version_debug(self.taskid,[])  
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.NEW_TASK.value
        self.ssh.set_airplane_mode(isOn.On)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.DOWNLOADING.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0505"', timeout=120):
            self.sd_tester.diag_cancel()
            self.ssh.set_airplane_mode(isOn.Off)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords=['KeepAlive'], timeout=30):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120)
            assert self.soa.till_fota_event_to(MASTER_EVENT.TaskId, target_status=0, timeout=120)
            # assert self.ssh.check_file_existence(DeviceName.BGM, path="/update/fota", filename="*.bin") == False # 检测/update/fota下不存在小ecu bin包  
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])   

    @pytest.mark.V_1_4
    @pytest.mark.sanity      
    @allure.title("诊断_OTA Cancel_UpdateFailedCanNotDriving_Succeed")    
    def test_fota_caseid_1982917(self):
        self.mix.update_version_debug(self.taskid,[]) 
        self.mix.back_fota_to(FOTAMasteSts.FAILED_NOT_DRIVING, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0505"', timeout=120):
            self.sd_tester.diag_cancel()
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=600)
        assert self.soa.till_fota_event_to(MASTER_EVENT.TaskId, target_status=0, timeout=120)
        # assert self.ssh.check_file_existence(DeviceName.BGM, path="/update/fota", filename="*.bin") == False # 检测/update/fota下不存在小ecu bin包
        self.sd_tester.read_bms_did_value(0xF153, "00")
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM]) 

    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("诊断令牌异常 Cancel_Query")    
    def test_fota_caseid_1982915(self):
        self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.QUERY.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0105"', timeout=120):
            sleep(2)
            self.io.bgm_diag_line_up()
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("诊断_OTA Cancel_Idle")    
    def test_fota_caseid_1982941(self):
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0503"', timeout=600):
            sleep(2)
            self.sd_tester.diag_cancel()

    # @pytest.mark.V_1_4
    # @pytest.mark.full
    # @allure.title("诊断_OTA Cancel_UpdateFailedCanDriving_succeed")    
    # def test_fota_caseid_1982921(self):
    #     self.mix.back_fota_to(FOTAMasteSts.FAILED_DRIVING, taskid=self.taskid)
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0505"', timeout=600):
    #         sleep(2)
    #         self.sd_tester.diag_cancel()
    #     assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120)
    #     assert self.soa.till_fota_event_to(MASTER_EVENT.TaskId, target_status=0, timeout=120)
    #     assert self.ssh.check_file_existence(DeviceName.BGM, path="/update/fota", filename="*.bin") == False, "/update/fota下存在小ecu bin包"

if __name__ == "__main__":
    pass

    




