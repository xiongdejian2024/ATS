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
        self.ssh.update_ua_skip(DOMAIN.BGM, True)
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])
        self.mix.set_enter_boot_condition(UsageMode.CONVENIENCE, low_volt_power=14, vehspd=0)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value 
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.ssh.set_airplane_mode(isOn.Off)
        
    def after_class(self, ecu):
        super().after_class(self, ecu) 
        self.mix.back_fota_to(FOTAMasteSts.IDLE, self.taskid)
        assert not self.sd_tester.check_mcu_whether_in_boot(), "Case Finish, but MCU still in boot"
        self.ssh.set_airplane_mode(isOn.Off)
        
    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("域控刷写_BGM 升级_BLT 低版本") 
    def test_fota_caseid_1982327(self):  
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)  
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.UPDATE.value 
        # with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:upgrade_manage => domain_pre_upgrade',timeout=420):
        #     pass
        with self.log_manage.check_jetlog_by_keywords(log_type='-E "fota: |UAS"', keywords=['entry ==>> install_boot_success_state',
                                                                                    'installing_soc ==> installing_mcu',
                                                                                    '==>> installing switch state',
                                                                                    '==>> update_finish_state',
                                                                                    '==>> activating_soc_state',
                                                                                    '"stateCode":"03F6"'],timeout=1200):
            pass
        
    
    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("域控刷写_BGM 升级_BLT 高版本") 
    def test_fota_caseid_1982326(self): 
        self.ssh.update_ua_skip(DOMAIN.BGM, False) 
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value 
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)  
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.UPDATE.value 
        # with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:upgrade_manage => domain_pre_upgrade',
        #                                                                              'notify door is available'],timeout=420):
        #     pass
        with self.log_manage.check_jetlog_by_keywords(log_type='-E "fota: |UAS"', keywords=['installing_soc ==> installing_mcu',
                                                                                    '==>> installing switch state',
                                                                                    '==>> update_finish_state',
                                                                                    '==>> activating_soc_state',
                                                                                    '"stateCode":"03F6"'],timeout=1200):
            pass      

    
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("ERROR_CODE重试_03_F6(Update Complete)") 
    def test_fota_caseid_1979768(self):  
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)  
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.UPDATE.value 
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"03F4"',
                                                                                   '"stateCode":"03F9"',
                                                                                   '"stateCode":"03F6"'
                                                                                   ], timeout=1200):
            time.sleep(2) #等待log manage启动
            self.ssh.set_airplane_mode(isOn.On)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"03F6"'
                                                                                   ], timeout=20):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"03F6"'
                                                                                   ], timeout=20):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"03F6"'
                                                                                   ], timeout=20):
            pass
        self.ssh.set_airplane_mode(isOn.Off)       
        
        
    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("域控刷写_CDC/ACU/TCAM 升级成功") 
    def test_fota_caseid_1982322(self):  
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)  
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.UPDATE.value 
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"03F6"'],timeout=900):
            pass  
 

    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("FOTA升级过程HMI交互_升级进度") 
    def test_fota_caseid_1982304(self):  
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)  
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.UPDATE.value 
        assert not (self.soa.get_fota_UpdateProcess(MASTER_UpdateProcess_EVENT.progress) == -1)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"03F6"'],timeout=900):
            pass  
               
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端code_StartUpdate(03F0)/VehicleinUpdate(03F4)") 
    def test_fota_caseid_1983124(self): 
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"03F0"',
                                                                                   '"stateCode":"03F4"'], timeout=900):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)     
@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota_DDM(TestABCBase):
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
        self.ssh.update_ua_skip(DOMAIN.BGM, True)
        self.mix.update_version_debug(self.taskid,["DDM"])
        self.mix.set_enter_boot_condition(UsageMode.CONVENIENCE, low_volt_power=14, vehspd=0)

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
    @pytest.mark.full
    @allure.title("常规OTA_非域控ECU刷写失败处理_0328") 
    def test_fota_caseid_1994895(self):  
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)  
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0328"'],timeout=900):
            pass        
