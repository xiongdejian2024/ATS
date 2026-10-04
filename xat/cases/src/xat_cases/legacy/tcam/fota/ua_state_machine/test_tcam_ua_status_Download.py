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
        self.ssh.set_airplane_mode(isOn.On)
        sleep(20)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.back_ua_to(DOMAIN.TCAM, UA_Sts.DOWNLOAD, self.TCAM_Download_Req)
           
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.ssh.set_airplane_mode(isOn.Off)
 
    @pytest.mark.sanity
    @allure.title("UA_Download_GetStatus")
    def test_fota_caseid_1980382(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.DOWNLOAD.value ,"UA Status != Downloading" 
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.GetStatus)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.DOWNLOAD.value
    
    @pytest.mark.full    
    @allure.title("UA_Download_StartDownload")
    def test_fota_caseid_1980381(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.DOWNLOAD.value ,"UA Status != Downloading" 
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.StartDownload, self.TCAM_Download_Req)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) == 0       
     
    @pytest.mark.sanity   
    @allure.title("UA_Download_CancelUpdate")
    def test_fota_caseid_1980376(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.DOWNLOAD.value ,"UA Status != Downloading" 
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.CancelUpdate)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) != 0

    @pytest.mark.full
    @allure.title("UA_Download_StartUpdate")
    def test_fota_caseid_1980379(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.DOWNLOAD.value ,"UA Status != Downloading" 
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.StartUpdate)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) != 0
    
    @pytest.mark.full    
    @allure.title("UA_Download_Activate")
    def test_fota_caseid_1980378(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.DOWNLOAD.value ,"UA Status != Downloading" 
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.Activate)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) != 0
    
    @pytest.mark.full    
    @allure.title("UA_Download_Rollback")
    def test_fota_caseid_1980377(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.DOWNLOAD.value ,"UA Status != Downloading" 
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.Rollback)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) != 0
     
    @pytest.mark.full   
    @allure.title("UA_Download_FinishUpdate")
    def test_fota_caseid_1980375(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.DOWNLOAD.value ,"UA Status != Downloading" 
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.FinishUpdate)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) != 0
    
    @pytest.mark.full    
    @allure.title("UA_Download_PreUpdate")
    def test_fota_caseid_1980374(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.DOWNLOAD.value ,"UA Status != Downloading" 
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.PreUpdate)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) != 0
    
    @pytest.mark.full    
    @allure.title("UA_Download_CancelDownload")
    def test_fota_caseid_1980380(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.DOWNLOAD.value ,"UA Status != Downloading" 
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.CancelDownload)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) == 0

    @pytest.mark.smoke
    @allure.title("UA_Download_Download_Complete")
    def test_fota_caseid_1980373(self, ecu):
        self.ssh.set_airplane_mode(isOn.Off)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.DOWNLOAD.value ,"UA Status != Downloading" 
        assert self.soa.till_ua_event_to(DOMAIN.TCAM, target_status=2, ua_event_field=UA_EVENT.Status, timeout=1200)
        
    @pytest.mark.full 
    @allure.title("UA_Downloading_Rescue")
    def test_fota_caseid_1987090(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == 1 ,"UA Status != Downloading" 
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.Rescue)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == 1 ,"UA Status != Downloading" 

            
            
