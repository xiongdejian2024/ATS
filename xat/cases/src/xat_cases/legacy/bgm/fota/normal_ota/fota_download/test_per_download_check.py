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
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])    
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
    @allure.title("per_download_check_UA_Idle")    
    def test_fota_caseid_1983298(self):
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.NEW_TASK.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"02F0"', timeout=600):
            sleep(2)
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.DOWNLOADING.value
 
if __name__ == "__main__":
    pass

    




