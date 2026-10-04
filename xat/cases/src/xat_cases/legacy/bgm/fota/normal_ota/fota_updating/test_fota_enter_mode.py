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

    @pytest.mark.V_2_1
    @pytest.mark.smoke
    @allure.title("OTA mode及升级开始流程_升级开始(03 F0/03 F4)") 
    def test_fota_caseid_1989746(self):   
        with self.log_manage.check_jetlog_by_keywords(log_type='-E "fota: | diag_client:| EM2:"', keywords=[ '"stateCode":"03F0"',
                                                                                                            'SetVFCReqDiagnosticCb: VfcType :23 ActState :1',
                                                                                                            'CheckDomainsDoIpConnection:addr:',
                                                                                                            'tx 1001:31 01 a1 00 01',
                                                                                                            'rx 1001:71 01 a1 00 10 00',
                                                                                                            'onTimer:Send 3E 80',
                                                                                                            'notify current mode: fota_mode',
                                                                                                            'tx 1201:31 01 a1 00 01',
                                                                                                            'tx 1011:31 01 a1 00 01',
                                                                                                            'tx 1401:31 01 a1 00 01',
                                                                                                            'tx 1630:31 01 42 89 01',
                                                                                                            '2e f1 53 04',
                                                                                                            'Finish to send 0206 to all ecus'], timeout=900):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.SUCCESSFUL.value, timeout=1200)
    
    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("OTA mode及升级开始流程_升级开始(03 F0/03 F4)") 
    def test_fota_caseid_1982360(self):   
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=[ '03F0',
                                                                                    '31 01 a1 00 01',
                                                                                    '22 f1 86',
                                                                                    '03F4'], timeout=1800):
            time.sleep(2)
            self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
    
    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("OTA mode及升级开始流程_进入FOTA mode失败_回复超时 (03 08)") 
    def test_fota_caseid_1982357(self):  
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                                    FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.before_group_hv_ctl,
                                    FOTA_Skip_Debug.ecm3_down_hv,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.start_download,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ])
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate) 
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0308"', timeout=500):
            pass  
        
    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("OTA mode及升级开始流程_ECM3 下高压失败_回复超时 (03 09)") 
    def test_fota_caseid_1982351(self):  
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                                    FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.start_download,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ])
        self.mix.update_version_debug(self.taskid,[])
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0309"', timeout=500):
            pass
        
        
    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("FOTA 补丁策略_BGM MCU 进入FOTA mode成功") 
    def test_fota_caseid_1982306(self):  
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
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
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate) 
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"03F6"'],timeout=900):
            self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING,do_assert=False)
    
    
    
    
    
        
        