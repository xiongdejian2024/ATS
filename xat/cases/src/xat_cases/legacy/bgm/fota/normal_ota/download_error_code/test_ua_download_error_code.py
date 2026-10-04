import os
import sys
import pytest
import allure
import copy
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

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
           
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
           
    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("域控下载Error_Code_BGM_UA_0000_None")
    def test_fota_caseid_1983246(self, ecu):
        self.soa.ua_back_to_idle(DOMAIN.BGM)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 0, "UA Status != Idle"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.GetStatus)
        self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.ErrorCode, target_status=UA_ErrorCode.None_0x00_0x00.value, timeout=120)
        
    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("域控下载Error_Code_BGM_UA_0206_FotaStateError")
    def test_fota_caseid_1983245(self, ecu):
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.READY_TO_INSTALL, self.BGM_Download_Req)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 2 ,"UA Status != Ready_to_Install"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelDownload)
        self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.ErrorCode, target_status=UA_ErrorCode.FotaStateError_0x02_0x06.value, timeout=120)

    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("域控下载Error_Code_BGM_UA_0907_安装soc失败")
    def test_fota_caseid_1986144(self, ecu):
        BGM_Download_Req_tmp = copy.deepcopy(self.BGM_Download_Req)
        BGM_Download_Req_tmp['downloadReq']['fileNumber'] = 1
        del BGM_Download_Req_tmp['downloadReq']['fileInformations'][0]
        logger.info(f"BGM_Download_Req_SOC: {BGM_Download_Req_tmp}")
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.READY_TO_INSTALL, BGM_Download_Req_tmp)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 2 ,"UA Status != Ready_to_Install"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.PreUpdate)
        assert self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.PreUpdateStatus, 2, timeout=600), "PreUpdateStatus != 2"
        self.ssh.type_commands(DeviceName.BGM,"rm -rf /update/installer/*;sync")
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartUpdate)
        self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.ErrorCode, target_status=UA_ErrorCode.IntsallSocFailed_0x09_0x07.value, timeout=120)

if __name__ == "__main__":
    pass

    




