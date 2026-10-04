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
from xat_cases.legacy.tcam.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("UpdateAgentService","client","TCAM_UA_Service"),
                         "CallService_client"])
        sleep(20)
        self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal3)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.back_ua_to(DOMAIN.TCAM, UA_Sts.DOWNLOAD, self.TCAM_Download_Req)  

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.ssh.set_airplane_mode(isOn.Off)

    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.ssh.set_network_mode(Network_Mode.Fifth_Generation)

    @pytest.mark.sanity      
    @allure.title("分布式下载基本策略_TCAM_UA_4G")
    def test_fota_caseid_1982965(self, ecu):
        self.ssh.set_network_mode(Network_Mode.Fourth_Generation)
        assert self.soa.check_whether_ua_download(DOMAIN.TCAM)

    @pytest.mark.sanity      
    @allure.title("分布式下载基本策略_TCAM_UA_5G")
    def test_fota_caseid_1982964(self, ecu):
        self.ssh.set_network_mode(Network_Mode.Fifth_Generation)
        assert self.soa.check_whether_ua_download(DOMAIN.TCAM)

    @pytest.mark.fota      
    @pytest.mark.sanity      
    @allure.title("分布式下载基本策略_TCAM_UA_飞行模式")
    def test_fota_caseid_1985409(self, ecu):
        self.ssh.set_airplane_mode(isOn.On)
        assert not self.soa.check_whether_ua_download(DOMAIN.TCAM)
        self.ssh.set_airplane_mode(isOn.Off)

    # @pytest.mark.full  
    # @allure.title("TCAM_UA_Status_periodic_idle")
    # def test_fota_caseid_1985411(self, ecu):
    #     self.soa.ua_back_to_idle(DOMAIN.TCAM)
    #     assert self.soa.check_ua_event_period(DOMAIN.TCAM, target_period=2.0, epsilon=0.1)
              
    # @pytest.mark.full 
    # @allure.title("TCAM_UA_Status_periodic_download")
    # def test_fota_caseid_1982967(self, ecu):
    #     assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.DOWNLOAD.value, "UA Status != Download" 
    #     assert self.soa.check_ua_event_period(DOMAIN.TCAM, target_period=2.0, epsilon=0.1)
        
    @pytest.mark.full 
    @allure.title("域控下载Error_Code_TCAM_UA_0000_None")
    def test_fota_caseid_1982961(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.DOWNLOAD.value, "UA Status != Download" 
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) == UA_ErrorCode.None_0x00_0x00.value
    
    @pytest.mark.full 
    @allure.title("域控下载Error_Code_TCAM_UA_0206_FotaStateError")
    def test_fota_caseid_1982960(self, ecu):
        assert self.soa.till_ua_event_to(DOMAIN.TCAM, UA_EVENT.Status, target_status=2, timeout=1800)
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.CancelDownload)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) == UA_ErrorCode.FotaStateError_0x02_0x06.value
        
    @pytest.mark.full 
    @allure.title("域控下载Error_Code_TCAM_UA_0224_PayLoadError")
    def test_fota_caseid_1982958(self, ecu):
        self.soa.ua_back_to_idle(DOMAIN.TCAM)
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.StartDownload, {"downloadReq": {}})
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) == UA_ErrorCode.PayLoadError_0x02_0x24.value
        
    @pytest.mark.full 
    @allure.title("域控下载Error_Code_TCAM_UA_0222_FileSecurityCheck_Error")
    def test_fota_caseid_1982953(self, ecu):
        self.soa.ua_back_to_idle(DOMAIN.TCAM)
        TCAM_Download_Req = copy.deepcopy(self.TCAM_Download_Req)
        TCAM_Download_Req["downloadReq"]["fileInformations"][0]["signature"] = "123"
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.StartDownload, TCAM_Download_Req)
        assert self.soa.till_ua_event_to(DOMAIN.TCAM, UA_EVENT.ErrorCode, target_status=UA_ErrorCode.FileSecurityCheck_Error_0x02_0x22.value, timeout=1800)
    
    @pytest.mark.full 
    @allure.title("分布式下载基本策略_TCAM_UA_XCALL模式")
    def test_fota_caseid_1985672(self, ecu):
        self.soa.ua_back_to_idle(DOMAIN.TCAM)
        self.mix.back_ua_to(DOMAIN.TCAM, UA_Sts.DOWNLOAD, self.TCAM_Download_Req)
        for _ in range(5):
            sleep(10)
            logger.info(f"以{eCallReqSource.kCDC.name}的方式触发ecall")
            try:
                self.soa.send_request_and_ck_resp(
                    "CallService_client",
                    'SetECallMode',
                    {"Cmd": eCallOperCmd.kSTART_ECALL.value, "Src": eCallReqSource.kCDC.value},
                    {"out": True}
                )
            except AssertionError as e:
                logger.error(f"点击SOS失败, 原因:{str(e)}")
                assert False, str(e)
            sleep(4)
            self.soa.confirm_call_sos()
            # 接通后15s挂断
            sleep(15)
            
            # 挂断
            try:
                self.soa.send_request_and_ck_resp(
                    "CallService_client",
                    'SetECallMode',
                    {"Cmd": eCallOperCmd.kHANG_UP_ECALL.value, "Src": eCallReqSource.kCDC.value},
                    {"out": True}
                )
            except AssertionError as e:
                logger.error(f"挂断SOS失败, 原因:{str(e)}")
                assert False, str(e)
            else:
                logger.info("挂断成功")
        assert self.soa.till_ua_event_to(DOMAIN.TCAM, UA_EVENT.Status, target_status=2, timeout=1800)
        self.mix.back_ua_to(DOMAIN.TCAM, UA_Sts.UPDATE_FINISH, self.TCAM_Download_Req)

    @pytest.mark.full 
    @allure.title("域控下载Error_Code_TCAM_UA_0225_File-Size_Error")
    def test_fota_caseid_1982949(self, ecu):
        self.soa.ua_back_to_idle(DOMAIN.TCAM)
        TCAM_Download_Req = copy.deepcopy(self.TCAM_Download_Req)
        TCAM_Download_Req["downloadReq"]["fileInformations"][0]["size"] = 1234567890
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.StartDownload, TCAM_Download_Req)
        assert self.soa.till_ua_event_to(DOMAIN.TCAM, UA_EVENT.ErrorCode, target_status=UA_ErrorCode.File_Size_Error_0x02_0x25.value, timeout=180)
        
if __name__ == "__main__":
    pass