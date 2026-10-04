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
        self.ssh.update_ua_skip(DOMAIN.BGM, allow_same_version_flash=False)
        sleep(20)
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.INSTALLING, self.BGM_Download_Req)
           
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.V_1_4
    @pytest.mark.sanity 
    @allure.title("UA_Installing_GetStatus")
    def test_fota_caseid_1981987(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 3 ,"UA Status != Installing" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.GetStatus)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 3
    
    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("UA_Installing_StartDownload")
    def test_fota_caseid_1981986(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 3 ,"UA Status != Installing" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartDownload, self.BGM_Download_Req, retry=False)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 518
        
    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("UA_Installing_CancleDownload")
    def test_fota_caseid_1981985(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 3 ,"UA Status != Installing" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelDownload)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 518

    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("UA_Installing_StartUpdate")
    def test_fota_caseid_1981984(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 3 ,"UA Status != Installing" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 0
        
    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("UA_Installing_Active")
    def test_fota_caseid_1981983(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 3 ,"UA Status != Installing" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.Activate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 780
        
    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("UA_Installing_Rollback")
    def test_fota_caseid_1981982(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 3 ,"UA Status != Installing" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.Rollback)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 780
                
    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("UA_Installing_CancelUpdate")
    def test_fota_caseid_1981981(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 3 ,"UA Status != Installing" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 0

    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("UA_Installing_FinishUpdate")
    def test_fota_caseid_1981980(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 3 ,"UA Status != Installing" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.FinishUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) ==780
        
    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("UA_Installing_PreUpdate")
    def test_fota_caseid_1981979(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 3 ,"UA Status != Installing" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.PreUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 780

    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("UA_Installing_UpdateSucceed")
    def test_fota_caseid_1981977(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 3 ,"UA Status != Installing" 
        logger.info("Still Downloading")       
        assert self.soa.till_ua_event_to(DOMAIN.BGM, target_status=4, ua_event_field=UA_EVENT.Status, timeout=600)
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("UA_Installing_UpdateFail")
    def test_fota_caseid_1981978(self, ecu):
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.UPDATE_FAILED, self.BGM_Download_Req)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FAILED.value ,"UA Status != Update Fail"             

    @pytest.mark.V_2_0
    @pytest.mark.full 
    @allure.title("UA_Installing_Rescue")
    def test_fota_caseid_1986921(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 3 ,"UA Status != Installing" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.Rescue)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.INSTALLING.value ,"UA Status != INSTALLING"             