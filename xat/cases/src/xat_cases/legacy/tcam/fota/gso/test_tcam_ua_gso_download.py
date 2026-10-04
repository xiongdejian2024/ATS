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
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","TCAM_UA_Service")])
        sleep(10)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.back_ua_to(DOMAIN.TCAM, UA_Sts.IDLE, self.TCAM_Download_Req)
        self.TCAM_Download_Req_Tmp = copy.deepcopy(self.TCAM_Download_Req)
        # self.mix.set_wifi_mode(isOn.Off) #关闭wifi
           
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
                
    def after_class(self, ecu):
        super().after_class(self, ecu)
        # self.mix.set_wifi_mode(isOn.Off) #关闭wifi
 
    @pytest.mark.V_2_2
    @pytest.mark.full 
    @allure.title("GSO_UA_StartDownload_无downloadNetworkMode")
    def test_fota_caseid_1990891(self, ecu):
        self.TCAM_Download_Req_Tmp['downloadReq'].pop('downloadNetworkMode')  
        with self.log_manage.check_jetlog_by_keywords(log_type="UAS", keywords=['downloadnetworkmode: 0'], timeout=30):
            self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.StartDownload, self.TCAM_Download_Req_Tmp)
        assert self.soa.check_whether_ua_download(DOMAIN.TCAM)
        # self.mix.set_wifi_mode(isOn.On) #打开wifi
        # assert self.soa.check_whether_ua_download(DOMAIN.TCAM)
        assert self.soa.till_ua_event_to(DOMAIN.TCAM, UA_EVENT.Status, target_status=UA_Sts.READY_TO_INSTALL.value, timeout=1200)
        
    @pytest.mark.V_2_2
    @pytest.mark.sanity 
    @allure.title("GSO_UA_StartDownload_downloadNetworkMode=1")
    def test_fota_caseid_1990889(self, ecu):
        self.TCAM_Download_Req_Tmp['downloadReq']['downloadNetworkMode'] = 1
        with self.log_manage.check_jetlog_by_keywords(log_type="UAS", keywords=['downloadnetworkmode: 1'], timeout=30):
            self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.StartDownload, self.TCAM_Download_Req_Tmp)
        assert self.soa.check_whether_ua_download(DOMAIN.TCAM)
        # self.mix.set_wifi_mode(isOn.On) #打开wifi
        # assert self.soa.check_whether_ua_download(DOMAIN.TCAM)
        assert self.soa.till_ua_event_to(DOMAIN.TCAM, UA_EVENT.Status, target_status=UA_Sts.READY_TO_INSTALL.value, timeout=1200)        
        
    @pytest.mark.V_2_2
    @pytest.mark.sanity 
    @allure.title("GSO_UA_StartDownload_downloadNetworkMode=2")
    def test_fota_caseid_1990890(self, ecu):
        self.TCAM_Download_Req_Tmp['downloadReq']['downloadNetworkMode'] = 2
        with self.log_manage.check_jetlog_by_keywords(log_type="UAS", keywords=['downloadnetworkmode: 2'], timeout=30):
            self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.StartDownload, self.TCAM_Download_Req_Tmp)
        assert not self.soa.check_whether_ua_download(DOMAIN.TCAM)
        # self.mix.set_wifi_mode(isOn.On) #打开wifi
        # assert self.soa.check_whether_ua_download(DOMAIN.TCAM)
        # assert self.soa.till_ua_event_to(DOMAIN.TCAM, UA_EVENT.Status, target_status=UA_Sts .READY_TO_INSTALL.value, timeout=1200)        
        
    @pytest.mark.V_2_2
    @pytest.mark.sanity 
    @allure.title("GSO_UA_下载断点续传_downloadNetworkMode=1_wifi_重启")
    def test_fota_caseid_1990893(self, ecu):
        # self.mix.set_wifi_mode(isOn.On) #打开wifi
        self.TCAM_Download_Req_Tmp['downloadReq']['downloadNetworkMode'] = 1
        with self.log_manage.check_jetlog_by_keywords(log_type="UAS", keywords=['downloadnetworkmode: 1'], timeout=30):
            self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.StartDownload, self.TCAM_Download_Req_Tmp)
        assert self.soa.check_whether_ua_download(DOMAIN.TCAM)
        # assert self.soa.check_whether_ua_download(DOMAIN.TCAM)
        self.sd_tester.reset_tcam()
        assert self.soa.check_whether_ua_download(DOMAIN.TCAM)
        assert self.soa.till_ua_event_to(DOMAIN.TCAM, UA_EVENT.Status, target_status=UA_Sts .READY_TO_INSTALL.value, timeout=1200)        
        
    @pytest.mark.V_2_2
    @pytest.mark.sanity 
    @allure.title("GSO_UA_下载断点续传_downloadNetworkMode=1_5g_重启")
    def test_fota_caseid_1990892(self, ecu):
        self.TCAM_Download_Req_Tmp['downloadReq']['downloadNetworkMode'] = 1
        with self.log_manage.check_jetlog_by_keywords(log_type="UAS", keywords=['downloadnetworkmode: 1'], timeout=30):
            self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.StartDownload, self.TCAM_Download_Req_Tmp)
        assert self.soa.check_whether_ua_download(DOMAIN.TCAM)
        # assert self.soa.check_whether_ua_download(DOMAIN.TCAM)
        self.sd_tester.reset_tcam()
        assert self.soa.check_whether_ua_download(DOMAIN.TCAM)
        assert self.soa.till_ua_event_to(DOMAIN.TCAM, UA_EVENT.Status, target_status=UA_Sts .READY_TO_INSTALL.value, timeout=1200)        
        
    @pytest.mark.V_2_2
    @pytest.mark.sanity 
    @allure.title("GSO_UA_下载断点续传_downloadNetworkMode=2_wifi_重启")
    def test_fota_caseid_1990894(self, ecu):
        # self.mix.set_wifi_mode(isOn.On) #打开wifi
        self.TCAM_Download_Req_Tmp['downloadReq']['downloadNetworkMode'] = 2
        with self.log_manage.check_jetlog_by_keywords(log_type="UAS", keywords=['downloadnetworkmode: 2'], timeout=30):
            self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.StartDownload, self.TCAM_Download_Req_Tmp)
        # assert self.soa.check_whether_ua_download(DOMAIN.TCAM)
        self.sd_tester.reset_tcam()
        # assert self.soa.check_whether_ua_download(DOMAIN.TCAM)
        # assert self.soa.till_ua_event_to(DOMAIN.TCAM, UA_EVENT.Status, target_status=UA_Sts .READY_TO_INSTALL.value, timeout=1200)        
        
    @pytest.mark.V_2_2
    @pytest.mark.sanity 
    @allure.title("GSO_UA_下载断点续传_downloadNetworkMode=2_断连wifi")
    def test_fota_caseid_1990895(self, ecu):
        # self.mix.set_wifi_mode(isOn.On) #打开wifi
        self.TCAM_Download_Req_Tmp['downloadReq']['downloadNetworkMode'] = 2
        with self.log_manage.check_jetlog_by_keywords(log_type="UAS", keywords=['downloadnetworkmode: 2'], timeout=30):
            self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.StartDownload, self.TCAM_Download_Req_Tmp)
        # assert self.soa.check_whether_ua_download(DOMAIN.TCAM)
        # self.mix.set_wifi_mode(isOn.Off) #关闭wifi
        # assert not self.soa.check_whether_ua_download(DOMAIN.TCAM)
        # self.mix.set_wifi_mode(isOn.On) #打开wifi
        # assert self.soa.check_whether_ua_download(DOMAIN.TCAM)
        # assert self.soa.till_ua_event_to(DOMAIN.TCAM, UA_EVENT.Status, target_status=UA_Sts .READY_TO_INSTALL.value, timeout=1200)        

            
            
