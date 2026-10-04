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

@pytest.mark.auto_rescue
@pytest.mark.V_2_0
@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("UpdateAgentService","server","CDC_UA_Service")])
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
        time.sleep(10)   

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        self.mix.set_fota_rescue_condition(Gear.Park, HvSysRelaySts.Close, 230)
        self.soa.start_send_ua_response(DOMAIN.CDC)
        self.soa.start_send_ua_event(DOMAIN.CDC, self.soa.pack_ua_event_args(UA_Sts.IDLE))
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.mix.fota_back_to_idle()
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, self.taskid)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        time.sleep(2) # 防止CDC状态切太快
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.READY_TO_INSTALL)
        self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.ACTIVE.value, 100)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "PreUpdate", timeout=180)
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value
                                                          )
        time.sleep(5) #模拟 CDC 在 PREUPDATE_RUNNING 状态，持续一段时间
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                        ua_sts=UA_Sts.INSTALLING,
                                                        ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                        ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                        ua_update_sts=UA_UpdatedStatus.UPDATE_FAILED_TWICE.value,
                                                        errorCode=UA_ErrorCode.UpdateError_0x03_0x16.value
                                                        )
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        try:
            time.sleep(5) #留给OTA Master充足的时间记住CDC UA Status = Idle状态
            self.soa.stop_send_ua_event(DOMAIN.CDC)
            self.soa.stop_send_ua_response(DOMAIN.CDC)
        except Exception as e:
            logger.error(e)        
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.sanity
    @allure.title("Rescue_After_Reset_UA_Idle")    
    def test_fota_caseid_1987118(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:rescue_pre_check => rescue_reset'], timeout=480):
            pass
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "Rescue", timeout=180)
        
    @pytest.mark.full
    @allure.title("Rescue_After_Reset_UA_Finsish_Update_未回到Ready_to_Install")    
    def test_fota_caseid_1987121(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:rescue_pre_check => rescue_reset'], timeout=480):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"1006"'], timeout=600):
            self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.UPDATE_FINISH)
            self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "Rescue", timeout=180)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value, "FOTA Status is not FAILED_NOT_DRIVING"
        
    @pytest.mark.sanity
    @allure.title("Rescue_After_Reset_UA_Finsish_Update_回到Ready_to_Install")    
    def test_fota_caseid_1987122(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:rescue_pre_check => rescue_reset'], timeout=480):
            pass
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.UPDATE_FINISH)
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "Rescue", timeout=180)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.READY_TO_INSTALL)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.QUERY.value, timeout=120), "FOTA Status not Back to QUERY"
        
    @pytest.mark.full
    @allure.title("Rescue_After_Reset_UA_Activiting")    
    def test_fota_caseid_1987125(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:rescue_pre_check => rescue_reset'], timeout=480):
            pass
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.ACTIVATING)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:rescue_domain => failed_not_driving'], timeout=240):
            pass
        self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value, "FOTA Status not Turn to FAILED_NOT_DRIVING"
        
    @pytest.mark.full
    @allure.title("Rescue_After_Reset_UA_Installing")    
    def test_fota_caseid_1987126(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:rescue_pre_check => rescue_reset'], timeout=480):
            pass
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.INSTALLING)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:rescue_domain => failed_not_driving'], timeout=240):
            pass
        self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value, "FOTA Status not Turn to FAILED_NOT_DRIVING"
    
    @pytest.mark.full
    @allure.title("Rescue_After_Reset_链接UA超时")    
    def test_fota_caseid_1987127(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:rescue_pre_check => rescue_reset'], timeout=480):
            pass
        self.soa.stop_send_ua_event(DOMAIN.CDC)
        self.soa.stop_send_ua_response(DOMAIN.CDC)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:rescue_domain => failed_not_driving'], timeout=700):
            pass
        
        self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value, "FOTA Status not Turn to FAILED_NOT_DRIVING"

    @pytest.mark.full
    @allure.title("Rescue_After_Reset_UA_System Active_未回到Idle")    
    def test_fota_caseid_1987123(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:rescue_pre_check => rescue_reset'], timeout=480):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"1006"'], timeout=600):
            self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.SYSTEM_ACTIVE)
            self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "FinishUpdate", timeout=180)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value, "FOTA Status is not FAILED_NOT_DRIVING"
        
    @pytest.mark.sanity
    @allure.title("Rescue_After_Reset_UA_System Active_回到Idle")    
    def test_fota_caseid_1987124(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:rescue_pre_check => rescue_reset'], timeout=480):
            pass
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.SYSTEM_ACTIVE)
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "FinishUpdate", timeout=180)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.QUERY.value, timeout=300), "FOTA Status not Back to QUERY"
        
    @pytest.mark.full
    @allure.title("Rescue_After_Reset_UA_Update_Error_未回到Ready_to_Install")    
    def test_fota_caseid_1987119(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:rescue_pre_check => rescue_reset'], timeout=480):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"1006"'], timeout=600):
            self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.UPDATE_FAILED)
            self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "Rescue", timeout=180)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value, "FOTA Status is not FAILED_NOT_DRIVING"
        
    @pytest.mark.sanity
    @allure.title("Rescue_After_Reset_UA_Update_Error_回到Ready_to_Install")    
    def test_fota_caseid_1987120(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:rescue_pre_check => rescue_reset'], timeout=480):
            pass
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.UPDATE_FAILED)
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "Rescue", timeout=180)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.QUERY.value, timeout=300), "FOTA Status not Back to QUERY"
        
if __name__ == "__main__":
    pass

