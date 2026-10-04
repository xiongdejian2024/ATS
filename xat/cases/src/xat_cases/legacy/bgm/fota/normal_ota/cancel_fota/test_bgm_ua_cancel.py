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
           
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
     
        
    @pytest.mark.V_1_4
    @pytest.mark.sanity      
    @allure.title("UA_Download_CancelDownload")
    def test_fota_caseid_1982913(self, ecu):
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.DOWNLOAD, self.BGM_Download_Req)
        assert self.ssh.check_ua_package(DOMAIN.BGM), "No UA package was detected"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelDownload)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.IDLE.value and not self.ssh.check_ua_package(DOMAIN.BGM)
        
    @pytest.mark.V_1_4
    @pytest.mark.sanity      
    @allure.title("UA_Ready_to_install_CancelUpdate_PreUpdateStatus=0")
    def test_fota_caseid_1982911(self, ecu):
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.READY_TO_INSTALL, self.BGM_Download_Req)
        assert self.ssh.check_ua_package(DOMAIN.BGM), "No UA package was detected"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.IDLE.value and not self.ssh.check_ua_package(DOMAIN.BGM)
        
    @pytest.mark.V_1_4
    @pytest.mark.sanity      
    @allure.title("UA_Ready_to_install_CancelUpdate_PreUpdateStatus=1")
    def test_fota_caseid_1984606(self, ecu):
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.READY_TO_INSTALL, self.BGM_Download_Req)
        self.soa.send_ua_request(DOMAIN.BGM, ua_request=UA_REQUEST.PreUpdate)
        assert self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.PreUpdateStatus, target_status=1, timeout=3)
        assert self.ssh.check_ua_package(DOMAIN.BGM), "No UA package was detected"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelUpdate)
        assert self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.Status, target_status=UA_Sts.IDLE.value, timeout=300)
        sleep(2)
        assert not self.ssh.check_ua_package(DOMAIN.BGM)
        
    @pytest.mark.V_1_4
    @pytest.mark.sanity      
    @allure.title("UA_Ready_to_install_CancelUpdate_PreUpdateStatus=2")
    def test_fota_caseid_1984607(self, ecu):
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.READY_TO_INSTALL, self.BGM_Download_Req)
        self.soa.send_ua_request(DOMAIN.BGM, ua_request=UA_REQUEST.PreUpdate)
        assert self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.PreUpdateStatus, target_status=2, timeout=600) #BGM解密最慢可能需要 7-8 min
        assert self.ssh.check_ua_package(DOMAIN.BGM), "No UA package was detected"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.IDLE.value and not self.ssh.check_ua_package(DOMAIN.BGM)

    @pytest.mark.V_1_4
    @pytest.mark.sanity      
    @allure.title("UA_Update_Finish_CancelUpdate")
    def test_fota_caseid_1982910(self, ecu):
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.UPDATE_FINISH, self.BGM_Download_Req)
        assert self.ssh.check_ua_package(DOMAIN.BGM), "No UA package was detected"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.IDLE.value and not self.ssh.check_ua_package(DOMAIN.BGM)
        
    @pytest.mark.V_1_4
    @pytest.mark.sanity      
    @allure.title("UA_System_Active_CancelUpdate")
    def test_fota_caseid_1982909(self, ecu):
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.SYSTEM_ACTIVE, self.BGM_Download_Req)
        assert self.ssh.check_ua_package(DOMAIN.BGM), "No UA package was detected"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.IDLE.value and not self.ssh.check_ua_package(DOMAIN.BGM)

    @pytest.mark.V_1_4
    @pytest.mark.sanity      
    @allure.title("UA_Update_Failed_CancelUpdate")
    def test_fota_caseid_1982907(self, ecu):
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.UPDATE_FAILED, self.BGM_Download_Req)
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.IDLE.value and not self.ssh.check_ua_package(DOMAIN.BGM)
        
    @pytest.mark.V_1_4
    @pytest.mark.sanity      
    @allure.title("UA_Download_Fail_CancelDownload")
    def test_fota_caseid_1984605(self, ecu):
        self.soa.ua_back_to_idle(DOMAIN.BGM)
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartDownload, {"downloadReq": {}})
        assert self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.DownloadStatus, target_status=3, timeout=3)
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelDownload)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.IDLE.value and not self.ssh.check_ua_package(DOMAIN.BGM)

    @pytest.mark.V_1_4
    @pytest.mark.full      
    @allure.title("UA_Idle_CancelDownload")
    def test_fota_caseid_1982914(self, ecu):
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.IDLE)
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelDownload)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.IDLE.value
        
    @pytest.mark.V_1_4
    @pytest.mark.full      
    @allure.title("UA_Idle_CancelDownload")
    def test_fota_caseid_1982912(self, ecu):
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.IDLE)
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.IDLE.value

if __name__ == "__main__":
    pass

    




