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
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.soa.stop_send_ua_event(DOMAIN.CDC)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("dispatch_task_状态未切download")
    def test_fota_caseid_1983270(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"] * 2, timeout=120), "Not Meet 2 times"
        self.soa.stop_send_ua_response(DOMAIN.CDC)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("dispatch_task_不回复StartDownload_同一上电周期")
    def test_fota_caseid_1983269(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        self.soa.stop_send_ua_response(DOMAIN.CDC)
        self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["GetStatus"] * 3, timeout=600), "Not Meet 3 times"

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("dispatch_task_不回复StartDownload_三个上电周期")
    def test_fota_caseid_1983268(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        self.soa.stop_send_ua_response(DOMAIN.CDC)
        for _ in range(3):
            self.sd_tester.reset_bgm()
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"02F4"', timeout=900):
            pass


if __name__ == "__main__":
    pass

    




