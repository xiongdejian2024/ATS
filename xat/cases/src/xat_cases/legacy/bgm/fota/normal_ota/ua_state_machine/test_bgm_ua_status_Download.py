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
        self.ssh.set_airplane_mode(isOn.On)
        sleep(20)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.DOWNLOAD, self.BGM_Download_Req)
           
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.ssh.set_airplane_mode(isOn.Off)
 
    @pytest.mark.V_1_4
    @pytest.mark.sanity 
    @allure.title("UA_Download_GetStatus")
    def test_fota_caseid_1982007(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 1 ,"UA Status != Downloading" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.GetStatus)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 1
        
    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("UA_Download_StartDownload")
    def test_fota_caseid_1982006(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 1 ,"UA Status != Downloading" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartDownload, self.BGM_Download_Req)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 0       
        
    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("UA_Download_CancelUpdate")
    def test_fota_caseid_1982001(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 1 ,"UA Status != Downloading" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) != 0

    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("UA_Download_StartUpdate")
    def test_fota_caseid_1982004(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 1 ,"UA Status != Downloading" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) != 0
        
    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("UA_Download_Activate")
    def test_fota_caseid_1982003(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 1 ,"UA Status != Downloading" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.Activate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) != 0
        
    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("UA_Download_Rollback")
    def test_fota_caseid_1982002(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 1 ,"UA Status != Downloading" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.Rollback)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) != 0
        
    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("UA_Download_FinishUpdate")
    def test_fota_caseid_1982000(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 1 ,"UA Status != Downloading" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.FinishUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) != 0
        
    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("UA_Download_PreUpdate")
    def test_fota_caseid_1981999(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 1 ,"UA Status != Downloading" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.PreUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) != 0
        
    @pytest.mark.V_1_4
    @pytest.mark.sanity 
    @allure.title("UA_Download_CancelDownload")
    def test_fota_caseid_1982005(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 1 ,"UA Status != Downloading" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelDownload)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 0
    
    @pytest.mark.V_1_4
    @pytest.mark.smoke 
    @allure.title("UA_Download_Download_Complete")
    def test_fota_caseid_1981998(self, ecu):
        self.ssh.set_airplane_mode(isOn.Off)
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.DOWNLOAD, self.BGM_Download_Req)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 1 ,"UA Status != Downloading" 
        logger.info("Still Downloading, first wait 3 min")
        time.sleep(180)
        assert self.soa.till_ua_event_to(DOMAIN.BGM, target_status=2, ua_event_field=UA_EVENT.Status, timeout=600)

    @pytest.mark.V_2_0
    @pytest.mark.full 
    @allure.title("UA_Downloading_Rescue")
    def test_fota_caseid_1986923(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 1 ,"UA Status != Downloading" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.Rescue)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 1 ,"UA Status != Downloading" 
            
            
