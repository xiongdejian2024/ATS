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
        self.soa.ua_back_to_idle(DOMAIN.TCAM)
           
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
     
    @pytest.mark.sanity      
    @allure.title("UA_Idle_GetStatus")
    def test_fota_caseid_1980391(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.IDLE.value, "UA Status != Idle"
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.GetStatus)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.IDLE.value, "UA Status != Idle"

    @pytest.mark.full    
    @allure.title("UA_Idle_CancelDownload")
    def test_fota_caseid_1980389(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.IDLE.value, "UA Status != Idle"
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.CancelDownload)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) == 0, "UA Code != 0"
    
    @pytest.mark.full    
    @allure.title("UA_Idle_StartUpdate")
    def test_fota_caseid_1980388(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.IDLE.value, "UA Status != Idle"
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.StartUpdate)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) == 780, "UA Code != 780"
    
    @pytest.mark.full    
    @allure.title("UA_Idle_Activate")
    def test_fota_caseid_1980387(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.IDLE.value, "UA Status != Idle"
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.Activate)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) == 780, "UA Code != 780"
        
    @pytest.mark.full
    @allure.title("UA_Idle_Rollback")
    def test_fota_caseid_1980386(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.IDLE.value, "UA Status != Idle"
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.Rollback)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) == 780, "UA Code != 780"
    
    @pytest.mark.full    
    @allure.title("UA_Idle_CancelUpdate")
    def test_fota_caseid_1980385(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.IDLE.value, "UA Status != Idle"
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.CancelUpdate)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) == 0, "UA Code != 0"
        
    @pytest.mark.full
    @allure.title("UA_Idle_FinishUpdate")
    def test_fota_caseid_1980384(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.IDLE.value, "UA Status != Idle"
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.FinishUpdate)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) == 0, "UA Code != 0"
    
    @pytest.mark.full    
    @allure.title("UA_Idle_PreUpdate")
    def test_fota_caseid_1980383(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.IDLE.value, "UA Status != Idle"
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.PreUpdate)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) == 0, "UA Code != 0"

    @pytest.mark.smoke
    @allure.title("UA_Idle_StartDownload")
    def test_fota_caseid_1980390(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.IDLE.value, "UA Status != Idle"
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.StartDownload, self.TCAM_Download_Req)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) == 0, "UA Code != 0"
        
    @pytest.mark.full
    @allure.title("UA_Idle_Rescue")
    def test_fota_caseid_1987091(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == 0, "UA Status != Idle"
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.Rescue)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == 0, "UA Status != Idle"
        
if __name__ == "__main__":
    pass

    




