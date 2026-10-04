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
        sleep(20)
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.SYSTEM_ACTIVE, self.BGM_Download_Req)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.SYSTEM_ACTIVE.value ,"UA Status != System Active" 

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
 
    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("UA_System_Active_GetStatus")
    def test_fota_caseid_1981956(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.SYSTEM_ACTIVE.value ,"UA Status != System Active" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.GetStatus)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.SYSTEM_ACTIVE.value

    @pytest.mark.V_1_4
    @pytest.mark.full      
    @allure.title("UA_System_Active_StartDownload")
    def test_fota_caseid_1981955(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.SYSTEM_ACTIVE.value ,"UA Status != System Active" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartDownload, self.BGM_Download_Req, retry=False)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) != 0
        
    @pytest.mark.V_1_4
    @pytest.mark.full  
    @allure.title("UA_System_Active_CancleDownload")
    def test_fota_caseid_1981954(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.SYSTEM_ACTIVE.value ,"UA Status != System Active" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelDownload)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) != 0

    @pytest.mark.V_1_4
    @pytest.mark.full  
    @allure.title("UA_System_Active_StartUpdate")
    def test_fota_caseid_1981953(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.SYSTEM_ACTIVE.value ,"UA Status != System Active" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) != 0
    
    @pytest.mark.V_1_4
    @pytest.mark.full   
    @allure.title("UA_System_Active_Active")
    def test_fota_caseid_1981952(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.SYSTEM_ACTIVE.value ,"UA Status != System Active" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.Activate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 0
        time.sleep(180) #BGM UA 切面时长约 140s
    
    @pytest.mark.V_1_4
    @pytest.mark.full      
    @allure.title("UA_System_Active_Rollback")
    def test_fota_caseid_1981951(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.SYSTEM_ACTIVE.value ,"UA Status != System Active" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.Rollback)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) != 0 #BGM UA暂无回滚，暂不做要求
        time.sleep(300) #BGM UA 回滚时长约 250s
    
    @pytest.mark.V_1_4
    @pytest.mark.sanity            
    @allure.title("UA_System_Active_CancelUpdate")
    def test_fota_caseid_1981950(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.SYSTEM_ACTIVE.value ,"UA Status != System Active" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 0

    @pytest.mark.V_1_4
    @pytest.mark.smoke  
    @allure.title("UA_System_Active_FinishUpdate")
    def test_fota_caseid_1981949(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.SYSTEM_ACTIVE.value ,"UA Status != System Active" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.FinishUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 0

    @pytest.mark.V_1_4
    @pytest.mark.full  
    @allure.title("UA_System_Active_PreUpdate")
    def test_fota_caseid_1981948(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.SYSTEM_ACTIVE.value ,"UA Status != System Active" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.PreUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) != 0

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("UA_超时_System_Active")
    def test_fota_caseid_1981937(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.SYSTEM_ACTIVE.value ,"UA Status != System Active" 
        assert self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.Status, target_status=0, timeout=5600) # System_Active 超时时间5400s
        
    @pytest.mark.V_2_0
    @pytest.mark.sanity
    @allure.title("UA_System Active_Rescue")
    def test_fota_caseid_1986919(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.SYSTEM_ACTIVE.value ,"UA Status != System Active" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.Rescue)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.READY_TO_INSTALL.value ,"UA Status != READY_TO_INSTALL"
        assert self.ssh.check_ua_package(DOMAIN.BGM), "No UA package was detected"