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

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
           
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
           
    @pytest.mark.V_1_4
    @pytest.mark.full 
    @allure.title("上传云端/升级阶段_FotaStateError(030C)")
    def test_fota_caseid_1983114(self, ecu):
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.READY_TO_INSTALL, self.BGM_Download_Req)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 2 ,"UA Status != Ready_to_Install"    
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.PreUpdateStatus) == 0, "PreUpdateStatus != 0"
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartUpdate)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.ErrorCode) == UA_ErrorCode.FotaStateError_0x03_0x0C.value, "UA ErrorCode != FotaStateError_0x03_0x0C"
        
if __name__ == "__main__":
    pass

    




