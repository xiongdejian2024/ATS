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
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("UpdateAgentService","server","CDC_UA_Service"),
                         ("AcuModeManagerService","server")])
        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                                    FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.before_group_hv_ctl,
                                    FOTA_Skip_Debug.ecm3_down_hv,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.update_precondition_check,
                                    FOTA_Skip_Debug.cdc_acu_doip_check
                                    ], allow_sleep=False) 
        self.mix.update_version_debug(self.taskid,[DOMAIN.CDC])    

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        self.soa.start_send_ua_response(DOMAIN.CDC)
        self.soa.start_send_ua_event(DOMAIN.CDC, self.soa.pack_ua_event_args(UA_Sts.IDLE))
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.empty_all()
        self.ssh.clear_fota_cache()
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, self.taskid)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        time.sleep(10) # 模拟正常流程
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.DOWNLOAD)
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.soa.stop_send_ua_event(DOMAIN.CDC)
        self.soa.stop_send_ua_response(DOMAIN.CDC)
        self.ssh.set_airplane_mode(isOn.Off)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.ssh.set_airplane_mode(isOn.Off)

    @pytest.mark.sanity
    @allure.title("诊断_OTA Cancel_Download_唤醒")    
    def test_fota_caseid_1982938(self):
        self.sd_tester.diag_cancel()
        self.mix.check_fota_keep_awake(pnc29=True, acu_keep_alive=True, up_inactive=False)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("诊断_OTA Cancel_Download_UA_Download_Succeed")    
    def test_fota_caseid_1982937(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0505"', timeout=600):
            sleep(2)
            self.sd_tester.diag_cancel()
            self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "CancelDownload")
            sleep(10) # 模拟正常流程
            self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120), "DiagCancel之后FOTAMaster未回到IDLE"

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("诊断_OTA Cancel_Download_UA_Download_Fail")    
    def test_fota_caseid_1982936(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0504"', timeout=600):
            sleep(2)
            self.sd_tester.diag_cancel()
            self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["CancelDownload"] * 2, timeout=300), "Not Meet 2 times"
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120), "DiagCancel之后FOTAMaster未回到IDLE"

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("诊断_OTA Cancel_Active_UA_System_Active_Succeed")    
    def test_fota_caseid_1982923(self):
        sleep(10)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.READY_TO_INSTALL)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.ACTIVE.value, timeout=120), "FOTA Status ≠ ACTIVE"
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.SYSTEM_ACTIVE)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0505"', timeout=600):
            sleep(2)
            self.sd_tester.diag_cancel()
            self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "FinishUpdate")
            sleep(10) # 模拟正常流程
            self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120), "DiagCancel之后FOTAMaster未回到IDLE"
        assert self.soa.till_fota_event_to(MASTER_EVENT.TaskId, target_status=0, timeout=120)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("诊断_OTA Cancel_Active_UA_System_Active_Fail")    
    def test_fota_caseid_1982922(self):
        sleep(10)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.READY_TO_INSTALL)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.ACTIVE.value, timeout=120), "FOTA Status ≠ ACTIVE"
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.SYSTEM_ACTIVE)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0504"', timeout=600):
            sleep(2)
            self.sd_tester.diag_cancel()
            self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["FinishUpdate"] * 2, timeout=300), "Not Meet 2 times"

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("ERROR_CODE重试_05_04(DiagTool_CancelFota_Fail)")    
    def test_fota_caseid_1979765(self):
        self.ssh.set_airplane_mode(isOn.On)
        with self.log_manage.check_jetlog_by_same_keywords(log_type=" fota:", keywords=['"stateCode":"0504"',
                                                                                   '"stateCode":"0504"',
                                                                                   '"stateCode":"0504"',
                                                                                   '"stateCode":"0504"'
                                                                                   ], timeout=600):
            sleep(2)
            self.sd_tester.diag_cancel()
        self.ssh.set_airplane_mode(isOn.Off)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("ERROR_CODE重试_05_05(DiagTool_CancelFota_Complete)")    
    def test_fota_caseid_1979764(self):
        self.ssh.set_airplane_mode(isOn.On)
        with self.log_manage.check_jetlog_by_same_keywords(log_type=" fota:", keywords=['"stateCode":"0505"',
                                                                                   '"stateCode":"0505"',
                                                                                   '"stateCode":"0505"',
                                                                                   '"stateCode":"0505"'
                                                                                   ], timeout=600):
            sleep(2)
            self.sd_tester.diag_cancel()
            sleep(10) # 模拟正常流程
            self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120), "DiagCancel之后FOTAMaster未回到IDLE"
        self.ssh.set_airplane_mode(isOn.Off)

if __name__ == "__main__":
    pass

    




