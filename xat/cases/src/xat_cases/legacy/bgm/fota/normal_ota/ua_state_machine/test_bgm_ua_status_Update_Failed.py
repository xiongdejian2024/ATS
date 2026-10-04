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
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.UPDATE_FAILED, self.BGM_Download_Req)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FAILED.value ,"UA Status != Update_Failed" 

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
 
    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("UA_Uodate_Failed_GetStatus")
    def test_fota_caseid_1981947(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FAILED.value ,"UA Status != Update_Failed" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.GetStatus)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FAILED.value

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("UA_Uodate_Failed_StartDownload")
    def test_fota_caseid_1981946(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FAILED.value ,"UA Status != Update_Failed" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartDownload, self.BGM_Download_Req, retry=False)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) != 0
        
    @pytest.mark.V_1_4
    @pytest.mark.full  
    @allure.title("UA_Uodate_Failed_CancleDownload")
    def test_fota_caseid_1981945(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FAILED.value ,"UA Status != Update_Failed" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelDownload)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) != 0

    @pytest.mark.V_1_4
    @pytest.mark.full  
    @allure.title("UA_Uodate_Failed_StartUpdate")
    def test_fota_caseid_1981944(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FAILED.value ,"UA Status != Update_Failed" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) != 0
    
    @pytest.mark.V_1_4
    @pytest.mark.full  
    @allure.title("UA_Uodate_Failed_Active")
    def test_fota_caseid_1981943(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FAILED.value ,"UA Status != Update_Failed" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.Activate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) != 0
        time.sleep(180) #BGM UA 切面时长约 140s
    
    @pytest.mark.V_1_4
    @pytest.mark.full      
    @allure.title("UA_Uodate_Failed_Rollback")
    def test_fota_caseid_1981942(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FAILED.value ,"UA Status != Update_Failed" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.Rollback)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 0
        time.sleep(300) #BGM UA 回滚时长约 250s
    
    @pytest.mark.V_1_4
    @pytest.mark.sanity            
    @allure.title("UA_Uodate_Failed_CancelUpdate")
    def test_fota_caseid_1981941(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FAILED.value ,"UA Status != Update_Failed" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == 0

    @pytest.mark.V_1_4
    @pytest.mark.full  
    @allure.title("UA_Uodate_Failed_FinishUpdate")
    def test_fota_caseid_1981940(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FAILED.value ,"UA Status != Update_Failed" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.FinishUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) != 0

    @pytest.mark.V_1_4
    @pytest.mark.full  
    @allure.title("UA_Uodate_Failed_PreUpdate")
    def test_fota_caseid_1981939(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FAILED.value ,"UA Status != Update_Failed" 
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.PreUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) != 0
        
    @pytest.mark.V_2_0
    @pytest.mark.sanity
    @allure.title("UA_Update Failed_Rescue")
    def test_fota_caseid_1986918(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.UPDATE_FAILED.value ,"UA Status != Update Finish"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.Rescue)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == UA_Sts.READY_TO_INSTALL.value ,"UA Status != READY_TO_INSTALL" 
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.PreUpdateStatus) == 2 ,"UA Status != READY_TO_INSTALL" 
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.IDLE, self.BGM_Download_Req)