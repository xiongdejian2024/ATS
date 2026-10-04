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
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.READY_TO_INSTALL, self.BGM_Download_Req)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.PreUpdateStatus) == 0, "PreUpdateStatus != 0"
           
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.V_1_4
    @pytest.mark.sanity 
    @allure.title("UA_Ready_to_Install_GetStatus")
    def test_fota_caseid_1981997(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 2 ,"UA Status != Ready_to_Install" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.GetStatus)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 2
        
    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("UA_Ready_to_Install_StartDownload")
    def test_fota_caseid_1981996(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 2 ,"UA Status != Ready_to_Install"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartDownload, self.BGM_Download_Req, retry=False)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 0       
    
    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("UA_Ready_to_Install_CancelDownload")
    def test_fota_caseid_1981995(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 2 ,"UA Status != Ready_to_Install"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelDownload)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 518

    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("UA_Ready_to_Install_StartUpdate_preUpdateStatus!=2")
    def test_fota_caseid_1981994(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 2 ,"UA Status != Ready_to_Install"    
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.PreUpdateStatus) == 0, "PreUpdateStatus != 0"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 780
        
    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("UA_Ready_to_Install_Activate")
    def test_fota_caseid_1981992(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 2 ,"UA Status != Ready_to_Install"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.Activate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 780
        
    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("UA_Ready_to_Install_Rollback")
    def test_fota_caseid_1981991(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 2 ,"UA Status != Ready_to_Install"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.Rollback)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 780
                
    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("UA_Ready_to_Install_FinishUpdate")
    def test_fota_caseid_1981989(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 2 ,"UA Status != Ready_to_Install"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.FinishUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) ==780

    @pytest.mark.V_1_4
    @pytest.mark.sanity 
    @allure.title("UA_Ready_to_Install_CancelUpdate")
    def test_fota_caseid_1981990(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 2 ,"UA Status != Ready_to_Install"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 0
        
    @pytest.mark.V_1_4
    @pytest.mark.smoke 
    @allure.title("UA_Ready_to_Install_PreUpdate")
    def test_fota_caseid_1981988(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 2 ,"UA Status != Ready_to_Install"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.PreUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 0
        
    @pytest.mark.V_1_4
    @pytest.mark.smoke 
    @allure.title("UA_Ready_to_Install_StartUpdate_preUpdateStatus==2")
    def test_fota_caseid_1981993(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 2 ,"UA Status != Ready_to_Install"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.PreUpdate)
        assert self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.PreUpdateStatus, 2, timeout=600), "PreUpdateStatus != 2"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartUpdate)
        assert self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.Status, 3, timeout=10), "UA Status != Installing"
            
    @pytest.mark.V_2_0
    @pytest.mark.full 
    @allure.title("UA_Ready to Install_Rescue")
    def test_fota_caseid_1986922(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 2 ,"UA Status != Ready_to_Install"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.Rescue)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 2 ,"UA Status != Ready_to_Install"
        assert self.ssh.check_ua_package(DOMAIN.BGM)
            
