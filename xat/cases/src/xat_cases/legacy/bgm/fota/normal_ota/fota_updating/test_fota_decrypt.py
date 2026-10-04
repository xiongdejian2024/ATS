import os
import sys
import pytest
import allure
from time import sleep
import random

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
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.start_download,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ]) 
        self.ssh.update_ua_skip(DOMAIN.BGM, False)
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value 
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.mix.back_fota_to(FOTAMasteSts.IDLE, self.taskid)
        assert not self.sd_tester.check_mcu_whether_in_boot(), "Case Finish, but MCU still in boot"
    
    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("FOTA解密过程_解密成功") 
    def test_fota_caseid_1982350(self):  
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)  
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.UPDATE.value      
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='BGM_UA_Service,state:2,download status:1,pre update status:2,errorcode:0', timeout=420):
            pass
    
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("FOTA解密过程_ECM3无法上高压_回复超时 (03 0B)") 
    def test_fota_caseid_1982348(self):  
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                                    FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.ecm3_down_hv,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.start_download,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ]) 
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate) 
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"030B"', timeout=360):
            pass


    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("FOTA解密过程_VBF 验签错误(03 10)") 
    def test_fota_caseid_1982346(self):  
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.READY_TO_INSTALL, self.BGM_Download_Req)
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.PreUpdate)
        time.sleep(60)
        self.ssh.type_commands(DeviceName.BGM, "rm /update/installer/*;sync")
        assert self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.PreUpdateStatus, target_status=3, timeout=300)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == UA_ErrorCode.VBF_Signature_verification_Error_0x03_0x10.value
        
if __name__ == "__main__":
    pass        