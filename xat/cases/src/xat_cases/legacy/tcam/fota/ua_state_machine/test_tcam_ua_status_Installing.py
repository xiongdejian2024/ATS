import os
import sys
import pytest
import allure
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.tcam.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("UpdateAgentService","client","TCAM_UA_Service")])
        sleep(20)
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.back_ua_to(DOMAIN.TCAM, UA_Sts.INSTALLING, self.TCAM_Download_Req)
           
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        self.soa.ua_back_to_idle(DOMAIN.TCAM)
        super().after_class(self, ecu)
 
    @pytest.mark.sanity
    @allure.title("UA_Installing_GetStatus")
    def test_fota_caseid_1980362(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.INSTALLING.value ,"UA Status != Installing" 
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.GetStatus)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.INSTALLING.value 
    
    @pytest.mark.full
    @allure.title("UA_Installing_StartDownload")
    def test_fota_caseid_1980361(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.INSTALLING.value ,"UA Status != Installing" 
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.StartDownload, self.TCAM_Download_Req, retry=False)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) == 518
    
    @pytest.mark.full    
    @allure.title("UA_Installing_CancleDownload")
    def test_fota_caseid_1980360(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.INSTALLING.value ,"UA Status != Installing" 
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.CancelDownload)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) == 518

    @pytest.mark.full
    @allure.title("UA_Installing_StartUpdate")
    def test_fota_caseid_1980359(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.INSTALLING.value ,"UA Status != Installing" 
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.StartUpdate)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) == 0
     
    @pytest.mark.full   
    @allure.title("UA_Installing_Active")
    def test_fota_caseid_1980358(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.INSTALLING.value ,"UA Status != Installing" 
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.Activate)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) == 780
    
    @pytest.mark.full    
    @allure.title("UA_Installing_Rollback")
    def test_fota_caseid_1980357(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.INSTALLING.value ,"UA Status != Installing" 
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.Rollback)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) == 780
    
    @pytest.mark.full            
    @allure.title("UA_Installing_CancelUpdate")
    def test_fota_caseid_1980356(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.INSTALLING.value ,"UA Status != Installing" 
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.CancelUpdate)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) == 0
        
    @pytest.mark.full
    @allure.title("UA_Installing_FinishUpdate")
    def test_fota_caseid_1980355(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.INSTALLING.value ,"UA Status != Installing" 
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.FinishUpdate)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) ==780
    
    @pytest.mark.full    
    @allure.title("UA_Installing_PreUpdate")
    def test_fota_caseid_1980354(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.INSTALLING.value ,"UA Status != Installing" 
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.PreUpdate)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) == 780

    @pytest.mark.smoke
    @allure.title("UA_Installing_UpdateSucceed")
    def test_fota_caseid_1980352(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.INSTALLING.value ,"UA Status != Installing" 
        logger.info("Still Installing")       
        assert self.soa.till_ua_event_to(DOMAIN.TCAM, target_status=4, ua_event_field=UA_EVENT.Status, timeout=600)
        
    @pytest.mark.full
    @allure.title("UA_Installing_UpdateFail")
    def test_fota_caseid_1980353(self, ecu):
        self.mix.back_ua_to(DOMAIN.TCAM, UA_Sts.UPDATE_FAILED, self.TCAM_Download_Req)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.UPDATE_FAILED.value ,"UA Status != Update Fail" 
            
    @pytest.mark.full 
    @allure.title("UA_Installing_Rescue")
    def test_fota_caseid_1987088(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == 3 ,"UA Status != Installing" 
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.Rescue)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.INSTALLING.value ,"UA Status != INSTALLING"   
