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
                         ("V2TRoutingForwarder","client","V2TOTAFotaForwarder")])
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
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.version_collect
                                    ], allow_sleep=False) 
        self.ssh.update_ua_skip(DOMAIN.BGM, allow_same_version_flash=False, allow_sleep=False)
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])    
        sleep(20)

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
    @pytest.mark.sanity
    @allure.title("云端_OTA Cancel_Query")    
    def test_fota_caseid_1982960(self):
        self.mix.back_fota_to(FOTAMasteSts.QUERY, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.QUERY.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"05F1"', timeout=600):
            self.tsp.trigger_vsp_fota(VSP.Cancel, task_id=self.taskid)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=120)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("云端取消FOTA_当前处于IDLE状态_无需取消")    
    def test_fota_caseid_1993264(self):
        self.mix.fota_back_to_idle()
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.IDLE.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0503"', timeout=600):
            self.soa.trigger_fota_type70(self.taskid)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("云端取消FOTA_当前处于UpdateComplete状态_取消成功")    
    def test_fota_caseid_1993251(self):
        self.mix.back_fota_to(FOTAMasteSts.UPDATE, taskid=self.taskid)
        self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.SUCCESSFUL.value, timeout=1500)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"031A"', timeout=600):
            self.soa.trigger_fota_type70(self.taskid)
    
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("云端取消FOTA_当前处于UpdateFailedNotDriving状态_当前无域控升级任务_成功")    
    def test_fota_caseid_1993246(self):
        self.mix.back_fota_to(FOTAMasteSts.FAILED_NOT_DRIVING, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"05F1"', timeout=600):
            self.soa.trigger_fota_type70(self.taskid)    
              
if __name__ == "__main__":
    pass

    




