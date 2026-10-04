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
                                    ], allow_sleep=False) 
        self.ssh.update_ua_skip(DOMAIN.BGM, allow_same_version_flash=False, allow_sleep=False)
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM, DOMAIN.TCAM])    
        sleep(20)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("Enter_Download_Status_and_Code")    
    def test_fota_caseid_1983300(self):
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.NEW_TASK.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"02F0"', timeout=120):
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.DOWNLOADING.value

    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("dispatch_task_UA_Idle")    
    def test_fota_caseid_1983279(self):
        self.mix.back_fota_to(FOTAMasteSts.DOWNLOADING, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.DOWNLOADING.value
        assert self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.Status, target_status=UA_Sts.DOWNLOAD.value, timeout=120)

    @pytest.mark.V_1_4
    @pytest.mark.full  
    @allure.title("dispatch_task_BGM_UA_Status_periodic")
    def test_fota_caseid_1983281(self):
        self.soa.ua_back_to_idle(DOMAIN.BGM)
        assert self.soa.check_ua_event_period(DOMAIN.BGM, target_period=2.0, epsilon=0.1)
 
if __name__ == "__main__":
    pass

    




