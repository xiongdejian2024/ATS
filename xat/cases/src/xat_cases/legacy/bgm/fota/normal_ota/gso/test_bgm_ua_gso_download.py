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
        sleep(10)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.back_ua_to(DOMAIN.BGM, UA_Sts.IDLE, self.BGM_Download_Req)
        self.BGM_Download_Req_Tmp = copy.deepcopy(self.BGM_Download_Req)
        # self.mix.set_wifi_mode(isOn.Off) #关闭wifi
           
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
                
    def after_class(self, ecu):
        super().after_class(self, ecu)
        # self.mix.set_wifi_mode(isOn.Off) #关闭wifi
 
    @pytest.mark.V_2_2
    @pytest.mark.full 
    @allure.title("GSO_UA_StartDownload_无downloadNetworkMode")
    def test_fota_caseid_1996878(self, ecu):
        self.BGM_Download_Req_Tmp['downloadReq'].pop('downloadNetworkMode')  
        with self.log_manage.check_jetlog_by_keywords(log_type="UAS", keywords=['any download rolute is available'], timeout=30):
            self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartDownload, self.BGM_Download_Req_Tmp)
        assert self.soa.check_whether_ua_download(DOMAIN.BGM)
        # self.mix.set_wifi_mode(isOn.On) #打开wifi
        # assert self.soa.check_whether_ua_download(DOMAIN.BGM)
        assert self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.Status, target_status=UA_Sts.READY_TO_INSTALL.value, timeout=900)
        
    @pytest.mark.V_2_2
    @pytest.mark.sanity 
    @allure.title("GSO_UA_StartDownload_downloadNetworkMode=1")
    def test_fota_caseid_1996879(self, ecu):
        self.BGM_Download_Req_Tmp['downloadReq']['downloadNetworkMode'] = 1
        with self.log_manage.check_jetlog_by_keywords(log_type="UAS", keywords=['any download rolute is available'], timeout=30):
            self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartDownload, self.BGM_Download_Req_Tmp)
        assert self.soa.check_whether_ua_download(DOMAIN.BGM)
        # self.mix.set_wifi_mode(isOn.On) #打开wifi
        # assert self.soa.check_whether_ua_download(DOMAIN.BGM)
        assert self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.Status, target_status=UA_Sts.READY_TO_INSTALL.value, timeout=900)        
        
    @pytest.mark.V_2_2
    @pytest.mark.sanity 
    @allure.title("GSO_UA_StartDownload_downloadNetworkMode=2")
    def test_fota_caseid_1996880(self, ecu):
        self.BGM_Download_Req_Tmp['downloadReq']['downloadNetworkMode'] = 2
        with self.log_manage.check_jetlog_by_keywords(log_type="UAS", keywords=['only support wifi download for non-mobile hotspots'], timeout=30):
            self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartDownload, self.BGM_Download_Req_Tmp)
        assert not self.soa.check_whether_ua_download(DOMAIN.BGM)
        # self.mix.set_wifi_mode(isOn.On) #打开wifi
        # assert self.soa.check_whether_ua_download(DOMAIN.BGM)
        # assert self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.Status, target_status=UA_Sts .READY_TO_INSTALL.value, timeout=900)        
        
    @pytest.mark.V_2_2
    @pytest.mark.sanity 
    @allure.title("GSO_UA_下载断点续传_downloadNetworkMode=1_wifi_重启")
    def test_fota_caseid_1996881(self, ecu):
        # self.mix.set_wifi_mode(isOn.On) #打开wifi
        self.BGM_Download_Req_Tmp['downloadReq']['downloadNetworkMode'] = 1
        with self.log_manage.check_jetlog_by_keywords(log_type="UAS", keywords=['any download rolute is available'], timeout=30):
            self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartDownload, self.BGM_Download_Req_Tmp)
        assert self.soa.check_whether_ua_download(DOMAIN.BGM)
        # assert self.soa.check_whether_ua_download(DOMAIN.BGM)
        self.sd_tester.reset_bgm()
        time.sleep(120) #UA上线+恢复至download状态大概耗时2min
        assert self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.Status, target_status=UA_Sts .READY_TO_INSTALL.value, timeout=900)        
        
    @pytest.mark.V_2_2
    @pytest.mark.sanity 
    @allure.title("GSO_UA_下载断点续传_downloadNetworkMode=1_5g_重启")
    def test_fota_caseid_1996882(self, ecu):
        self.BGM_Download_Req_Tmp['downloadReq']['downloadNetworkMode'] = 1
        with self.log_manage.check_jetlog_by_keywords(log_type="UAS", keywords=['any download rolute is available'], timeout=30):
            self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartDownload, self.BGM_Download_Req_Tmp)
        assert self.soa.check_whether_ua_download(DOMAIN.BGM)
        # assert self.soa.check_whether_ua_download(DOMAIN.BGM)
        self.sd_tester.reset_bgm()
        assert self.soa.check_whether_ua_download(DOMAIN.BGM)
        assert self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.Status, target_status=UA_Sts .READY_TO_INSTALL.value, timeout=900)        
        
    @pytest.mark.V_2_2
    @pytest.mark.sanity 
    @allure.title("GSO_UA_下载断点续传_downloadNetworkMode=2_wifi_重启")
    def test_fota_caseid_1996883(self, ecu):
        # self.mix.set_wifi_mode(isOn.On) #打开wifi
        self.BGM_Download_Req_Tmp['downloadReq']['downloadNetworkMode'] = 2
        with self.log_manage.check_jetlog_by_keywords(log_type="UAS", keywords=['only support wifi download for non-mobile hotspots'], timeout=30):
            self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartDownload, self.BGM_Download_Req_Tmp)
        # assert self.soa.check_whether_ua_download(DOMAIN.BGM)
        # self.sd_tester.reset_bgm()
        # assert self.soa.check_whether_ua_download(DOMAIN.BGM)
        # assert self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.Status, target_status=UA_Sts .READY_TO_INSTALL.value, timeout=900)        
        
    @pytest.mark.V_2_2
    @pytest.mark.sanity 
    @allure.title("GSO_UA_下载断点续传_downloadNetworkMode=2_断连wifi")
    def test_fota_caseid_1996884(self, ecu):
        # self.mix.set_wifi_mode(isOn.On) #打开wifi
        self.BGM_Download_Req_Tmp['downloadReq']['downloadNetworkMode'] = 2
        with self.log_manage.check_jetlog_by_keywords(log_type="UAS", keywords=['only support wifi download for non-mobile hotspots'], timeout=30):
            self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.StartDownload, self.BGM_Download_Req_Tmp)
        # assert self.soa.check_whether_ua_download(DOMAIN.BGM)
        # self.mix.set_wifi_mode(isOn.Off) #关闭wifi
        # assert not self.soa.check_whether_ua_download(DOMAIN.BGM)
        # self.mix.set_wifi_mode(isOn.On) #打开wifi
        # assert self.soa.check_whether_ua_download(DOMAIN.BGM)
        # assert self.soa.till_ua_event_to(DOMAIN.BGM, UA_EVENT.Status, target_status=UA_Sts .READY_TO_INSTALL.value, timeout=900)        

            
            
