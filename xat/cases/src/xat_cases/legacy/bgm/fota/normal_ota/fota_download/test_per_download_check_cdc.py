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

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        self.soa.start_send_ua_response(DOMAIN.CDC)
        self.soa.start_send_ua_event(DOMAIN.CDC, self.soa.pack_ua_event_args(UA_Sts.IDLE))
        self.mix.fota_back_to_idle()
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, self.taskid)
        self.soa.empty_all()
        self.bus_comm.set_fota_download_wake_condition(display_hv_soc=900, low_volt_soc=90)
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.soa.stop_send_ua_event(DOMAIN.CDC)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("per_download_check_GetStatus不回复")    
    def test_fota_caseid_1983299(self):
        self.soa.stop_send_ua_response(DOMAIN.CDC)
        time.sleep(5)
        # with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords= ['"stateCode":"0226"', '"stateCode":"02F4"'], timeout=120):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords= '"stateCode":"02F4"', timeout=900):
            sleep(2)
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "GetStatus", timeout=300)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("per_download_check_UA_Download_Succeed")    
    def test_fota_caseid_1983297(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.DOWNLOAD)
        sleep(3)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        sleep(10) # 模拟正常流程
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "CancelDownload", timeout=60)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        sleep(10) # 模拟正常流程
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartDownload", timeout=120)
        self.soa.stop_send_ua_response(DOMAIN.CDC)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("per_download_check_UA_Ready_to_Install_Succeed")    
    def test_fota_caseid_1983296(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.READY_TO_INSTALL)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        sleep(10) # 模拟正常流程
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "CancelUpdate", timeout=60)
        sleep(10) # 模拟正常流程
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartDownload", timeout=120)
        self.soa.stop_send_ua_response(DOMAIN.CDC)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("per_download_check_UA_Installing_Succeed")    
    def test_fota_caseid_1983295(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.INSTALLING)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        sleep(10) # 模拟正常流程
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "CancelUpdate", timeout=60)
        sleep(10) # 模拟正常流程
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartDownload", timeout=120)
        self.soa.stop_send_ua_response(DOMAIN.CDC)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("per_download_check_UA_Rolling_Back_Succeed")    
    def test_fota_caseid_1983294(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.ROLLING_BACK)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        sleep(10) # 模拟正常流程
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "CancelUpdate", timeout=60)
        sleep(10) # 模拟正常流程
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartDownload", timeout=120)
        self.soa.stop_send_ua_response(DOMAIN.CDC)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("per_download_check_UA_Update_Finish_Succeed")    
    def test_fota_caseid_1983293(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.UPDATE_FINISH)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        sleep(10) # 模拟正常流程
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "CancelUpdate", timeout=60)
        sleep(10) # 模拟正常流程
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartDownload", timeout=120)
        self.soa.stop_send_ua_response(DOMAIN.CDC)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("per_download_check_UA_Activing_Succeed")    
    def test_fota_caseid_1983292(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.ACTIVATING)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        sleep(10) # 模拟正常流程
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "CancelUpdate", timeout=60)
        sleep(10) # 模拟正常流程
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartDownload", timeout=120)
        self.soa.stop_send_ua_response(DOMAIN.CDC)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("per_download_check_UA_Update_Failed_Succeed")    
    def test_fota_caseid_1983291(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.UPDATE_FAILED)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        sleep(10) # 模拟正常流程
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "CancelUpdate", timeout=60)
        sleep(10) # 模拟正常流程
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartDownload", timeout=120)
        self.soa.stop_send_ua_response(DOMAIN.CDC)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("per_download_check_UA_System_Active_Succeed")    
    def test_fota_caseid_1983290(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.SYSTEM_ACTIVE)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        sleep(10) # 模拟正常流程
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "FinishUpdate", timeout=60)
        sleep(10) # 模拟正常流程
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartDownload", timeout=120)
        self.soa.stop_send_ua_response(DOMAIN.CDC)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("per_download_check_UA_Download_Fail")    
    def test_fota_caseid_1983289(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.DOWNLOAD)
        sleep(3)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        sleep(10) # 模拟正常流程
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "CancelDownload", timeout=60)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords= ['"stateCode":"0205"', '"stateCode":"02F4"'], timeout=900):
            pass
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120), "UA_Download_Fail之后FOTAMaster未回到IDLE"
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.stop_send_ua_response(DOMAIN.CDC)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("per_download_check_UA_Ready_to_Install_Fail")    
    def test_fota_caseid_1983288(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.READY_TO_INSTALL)
        sleep(3)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        sleep(10) # 模拟正常流程
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "CancelUpdate", timeout=60)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords= ['"stateCode":"0205"', '"stateCode":"02F4"'], timeout=900):
            pass
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120), "UA_Download_Fail之后FOTAMaster未回到IDLE"
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.stop_send_ua_response(DOMAIN.CDC)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("per_download_check_UA_Installing_Fail")    
    def test_fota_caseid_1983287(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.INSTALLING)
        sleep(3)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        sleep(10) # 模拟正常流程
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "CancelUpdate", timeout=60)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords= ['"stateCode":"0205"', '"stateCode":"02F4"'], timeout=900):
            pass
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120), "UA_Download_Fail之后FOTAMaster未回到IDLE"
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.stop_send_ua_response(DOMAIN.CDC)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("per_download_check_UA_Rolling_Back_Fail")    
    def test_fota_caseid_1983286(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.ROLLING_BACK)
        sleep(3)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        sleep(10) # 模拟正常流程
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "CancelUpdate", timeout=60)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords= ['"stateCode":"0205"', '"stateCode":"02F4"'], timeout=900):
            pass
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120), "UA_Download_Fail之后FOTAMaster未回到IDLE"
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.stop_send_ua_response(DOMAIN.CDC)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("per_download_check_UA_Update_Finish_Fail")    
    def test_fota_caseid_1983285(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.UPDATE_FINISH)
        sleep(3)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        sleep(10) # 模拟正常流程
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "CancelUpdate", timeout=60)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords= ['"stateCode":"0205"', '"stateCode":"02F4"'], timeout=900):
            pass
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120), "UA_Download_Fail之后FOTAMaster未回到IDLE"
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.stop_send_ua_response(DOMAIN.CDC)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("per_download_check_UA_Activing_Fail")    
    def test_fota_caseid_1983284(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.ACTIVATING)
        sleep(3)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        sleep(10) # 模拟正常流程
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "CancelUpdate", timeout=60)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords= ['"stateCode":"0205"', '"stateCode":"02F4"'], timeout=900):
            pass
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120), "UA_Download_Fail之后FOTAMaster未回到IDLE"
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.stop_send_ua_response(DOMAIN.CDC)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("per_download_check_UA_Update_Failed_Fail")    
    def test_fota_caseid_1983283(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.UPDATE_FAILED)
        sleep(3)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        sleep(10) # 模拟正常流程
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "CancelUpdate", timeout=60)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords= ['"stateCode":"0205"', '"stateCode":"02F4"'], timeout=900):
            pass
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120), "UA_Download_Fail之后FOTAMaster未回到IDLE"
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.stop_send_ua_response(DOMAIN.CDC)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("per_download_check_UA_System_Active_Fail")    
    def test_fota_caseid_1983282(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.SYSTEM_ACTIVE)
        sleep(3)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        sleep(10) # 模拟正常流程
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "FinishUpdate", timeout=60)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords= ['"stateCode":"0205"', '"stateCode":"02F4"'], timeout=900):
            pass
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120), "UA_Download_Fail之后FOTAMaster未回到IDLE"
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.stop_send_ua_response(DOMAIN.CDC)

if __name__ == "__main__":
    pass

    




