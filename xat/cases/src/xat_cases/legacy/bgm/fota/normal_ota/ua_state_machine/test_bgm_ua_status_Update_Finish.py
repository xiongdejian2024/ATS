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
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.UPDATE_FINISH, self.BGM_Download_Req)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FINISH.value ,"UA Status != Update Finish" 

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
 
    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("UA_Update_Finish_GetStatus")
    def test_fota_caseid_1981976(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FINISH.value ,"UA Status != Update Finish" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.GetStatus)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FINISH.value

    @pytest.mark.V_1_4
    @pytest.mark.full      
    @allure.title("UA_Update_Finish_StartDownload")
    def test_fota_caseid_1981975(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FINISH.value ,"UA Status != Update Finish" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartDownload, self.BGM_Download_Req, retry=False)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) != 0
        
    @pytest.mark.V_1_4
    @pytest.mark.full  
    @allure.title("UA_Update_Finish_CancleDownload")
    def test_fota_caseid_1981974(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FINISH.value ,"UA Status != Update Finish" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelDownload)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) != 0

    @pytest.mark.V_1_4
    @pytest.mark.full  
    @allure.title("UA_Update_Finish_StartUpdate")
    def test_fota_caseid_1981973(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FINISH.value ,"UA Status != Update Finish" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 0
    
    @pytest.mark.V_1_4
    @pytest.mark.smoke    
    @allure.title("UA_Update_Finish_Active")
    def test_fota_caseid_1981972(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FINISH.value ,"UA Status != Update Finish" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.Activate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 0
        time.sleep(180) #BGM UA 切面时长约 140s
    
    @pytest.mark.V_1_4
    @pytest.mark.full      
    @allure.title("UA_Update_Finish_Rollback")
    def test_fota_caseid_1981971(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FINISH.value ,"UA Status != Update Finish" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.Rollback)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) != 0
        time.sleep(300) #BGM UA 回滚时长约 250s
    
    @pytest.mark.V_1_4
    @pytest.mark.sanity            
    @allure.title("UA_Update_Finish_CancelUpdate")
    def test_fota_caseid_1981970(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FINISH.value ,"UA Status != Update Finish" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 0

    @pytest.mark.V_1_4
    @pytest.mark.full  
    @allure.title("UA_Update_Finish_FinishUpdate")
    def test_fota_caseid_1981969(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FINISH.value ,"UA Status != Update Finish" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.FinishUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) != 0

    @pytest.mark.V_1_4
    @pytest.mark.full  
    @allure.title("UA_Update_Finish_PreUpdate")
    def test_fota_caseid_1981968(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FINISH.value ,"UA Status != Update Finish" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.PreUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) != 0
        
    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("UA_Activating_ResetSucceed")
    def test_fota_caseid_1985017(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FINISH.value ,"UA Status != Update Finish"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.Activate)
        assert self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.Status, target_status=6, timeout=180)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("UA_超时_Update_Finish")
    def test_fota_caseid_1981938(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FINISH.value ,"UA Status != Update Finish"
        assert self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.Status, target_status=6, timeout=5400) # Update_Finish 超时时间4800s

    @pytest.mark.V_2_0
    @pytest.mark.sanity
    @allure.title("UA_Update Finish_Rescue")
    def test_fota_caseid_1986920(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FINISH.value ,"UA Status != Update Finish"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.Rescue)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.READY_TO_INSTALL.value ,"UA Status != READY_TO_INSTALL" 
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.PreUpdateStatus) == 2 ,"UA Status != READY_TO_INSTALL" 
        # assert self.ssh.check_ua_package(DOMAIN.BGM)