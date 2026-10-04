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
           
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
     
    @pytest.mark.full      
    @allure.title("UA_Idle_CancelUpdate")
    def test_fota_caseid_1982774(self, ecu):
        self.soa.ua_back_to_idle(DOMAIN.TCAM)
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.CancelUpdate)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.IDLE.value
        
    @pytest.mark.full      
    @allure.title("UA_Idle_CancelDownload")
    def test_fota_caseid_1982776(self, ecu):
        self.soa.ua_back_to_idle(DOMAIN.TCAM)
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.CancelDownload)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.IDLE.value
        
    @pytest.mark.sanity      
    @allure.title("UA_Download_CancelDownload")
    def test_fota_caseid_1982775(self, ecu):
        self.mix.back_ua_to(DOMAIN.TCAM, UA_Sts.DOWNLOAD, self.TCAM_Download_Req)
        time.sleep(10) #等待包生成
        assert self.ssh.check_ua_package(DOMAIN.TCAM), "No UA package was detected"
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.CancelDownload)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.IDLE.value and not self.ssh.check_ua_package(DOMAIN.TCAM)
        
    @pytest.mark.sanity      
    @allure.title("UA_Ready_to_install_CancelUpdate_PreUpdateStatus=0")
    def test_fota_caseid_1982773(self, ecu):
        self.mix.back_ua_to(DOMAIN.TCAM, UA_Sts.READY_TO_INSTALL, self.TCAM_Download_Req)
        assert self.ssh.check_ua_package(DOMAIN.TCAM), "No UA package was detected"
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.CancelUpdate)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.IDLE.value and not self.ssh.check_ua_package(DOMAIN.TCAM)
        
    @pytest.mark.sanity      
    @allure.title("UA_Ready_to_install_CancelUpdate_PreUpdateStatus=1")
    def test_fota_caseid_1984377(self, ecu):
        self.mix.back_ua_to(DOMAIN.TCAM, UA_Sts.READY_TO_INSTALL, self.TCAM_Download_Req)
        self.soa.send_ua_request(DOMAIN.TCAM, ua_request=UA_REQUEST.PreUpdate)
        assert self.soa.till_ua_event_to(DOMAIN.TCAM, UA_EVENT.PreUpdateStatus, target_status=1, timeout=3)
        assert self.ssh.check_ua_package(DOMAIN.TCAM), "No UA package was detected"
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.CancelUpdate)
        assert self.soa.till_ua_event_to(DOMAIN.TCAM, UA_EVENT.Status, target_status=UA_Sts.IDLE.value, timeout=300)
        assert not self.ssh.check_ua_package(DOMAIN.TCAM)
        
    @pytest.mark.sanity      
    @allure.title("UA_Ready_to_install_CancelUpdate_PreUpdateStatus=2")
    def test_fota_caseid_1984378(self, ecu):
        self.mix.back_ua_to(DOMAIN.TCAM, UA_Sts.READY_TO_INSTALL, self.TCAM_Download_Req)
        self.soa.send_ua_request(DOMAIN.TCAM, ua_request=UA_REQUEST.PreUpdate)
        assert self.soa.till_ua_event_to(DOMAIN.TCAM, UA_EVENT.PreUpdateStatus, target_status=2, timeout=300)
        assert self.ssh.check_ua_package(DOMAIN.TCAM), "No UA package was detected"
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.CancelUpdate)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.IDLE.value and not self.ssh.check_ua_package(DOMAIN.TCAM)
        
    @pytest.mark.sanity      
    @allure.title("UA_Update_Finish_CancelUpdate")
    def test_fota_caseid_1982772(self, ecu):
        self.mix.back_ua_to(DOMAIN.TCAM, UA_Sts.UPDATE_FAILED, self.TCAM_Download_Req)
        assert self.ssh.check_ua_package(DOMAIN.TCAM), "No UA package was detected"
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.CancelUpdate)
        assert self.soa.till_ua_event_to(DOMAIN.TCAM, UA_EVENT.Status, target_status=UA_Sts.IDLE.value, timeout=30) and not self.ssh.check_ua_package(DOMAIN.TCAM)
        
    @pytest.mark.sanity      
    @allure.title("UA_System_Active_CancelUpdate")
    def test_fota_caseid_1982771(self, ecu):
        self.mix.back_ua_to(DOMAIN.TCAM, UA_Sts.SYSTEM_ACTIVE, self.TCAM_Download_Req)
        assert self.ssh.check_ua_package(DOMAIN.TCAM), "No UA package was detected"
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.CancelUpdate)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.IDLE.value and not self.ssh.check_ua_package(DOMAIN.TCAM)
        
    @pytest.mark.sanity      
    @allure.title("UA_Update_Failed_CancelUpdate")
    def test_fota_caseid_1982769(self, ecu):
        self.mix.back_ua_to(DOMAIN.TCAM, UA_Sts.UPDATE_FAILED, self.TCAM_Download_Req)
        assert self.ssh.check_ua_package(DOMAIN.TCAM), "No UA package was detected"
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.CancelUpdate)
        assert self.soa.till_ua_event_to(DOMAIN.TCAM, UA_EVENT.Status, target_status=UA_Sts.IDLE.value, timeout=30) and not self.ssh.check_ua_package(DOMAIN.TCAM)
        
    @pytest.mark.full      
    @allure.title("UA_Download_Fail_CancelDownload")
    def test_fota_caseid_1985521(self, ecu):
        self.soa.ua_back_to_idle(DOMAIN.TCAM)
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.StartDownload, {"downloadReq": {}})
        assert self.soa.till_ua_event_to(DOMAIN.TCAM, UA_EVENT.DownloadStatus, target_status=3, timeout=3)
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.CancelDownload)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.IDLE.value

if __name__ == "__main__":
    pass

    




