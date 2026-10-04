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
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("UpdateAgentService","server","CDC_UA_Service")])
        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                                    FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.before_group_hv_ctl,
                                    FOTA_Skip_Debug.ecm3_down_hv,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.update_precondition_check,
                                    FOTA_Skip_Debug.cdc_acu_doip_check
                                    ], allow_sleep=False) 
        self.mix.update_version_debug(self.taskid,[DOMAIN.CDC])    

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        self.soa.start_send_ua_response(DOMAIN.CDC)
        self.soa.start_send_ua_event(DOMAIN.CDC, self.soa.pack_ua_event_args(UA_Sts.IDLE))
        self.mix.fota_back_to_idle()
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, self.taskid)
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        time.sleep(5) #留给OTA Master充足的时间记住CDC UA Status = Idle状态
        self.soa.stop_send_ua_event(DOMAIN.CDC)
        self.soa.stop_send_ua_response(DOMAIN.CDC)
        self.ssh.set_airplane_mode(sts=isOn.Off)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.ssh.set_airplane_mode(sts=isOn.Off)
            
    @pytest.mark.full
    @allure.title("下载上报OTA_Master_Code_0208_DL-HTTPS-TimeoutError")    
    def test_fota_caseid_1983230(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0208"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC,
                                                            UA_Sts.DOWNLOAD,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_FINAL_FAILED.value,
                                                            errorCode=UA_ErrorCode.DL_HTTPS_TimeoutError_0x02_0x08.value)
            
    @pytest.mark.full
    @allure.title("下载上报OTA_Master_Code_0209_DL_TLS_Error")    
    def test_fota_caseid_1983229(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0209"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC,
                                                            UA_Sts.DOWNLOAD,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_FINAL_FAILED.value,
                                                            errorCode=UA_ErrorCode.DL_TLS_Error_0x02_0x09.value)
            
    @pytest.mark.full
    @allure.title("下载上报OTA_Master_Code_020A_DL_File_Change")    
    def test_fota_caseid_1983228(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"020A"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC,
                                                            UA_Sts.DOWNLOAD,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_FINAL_FAILED.value,
                                                            errorCode=UA_ErrorCode.DL_File_Change_0x02_0x0A.value)
            
    @pytest.mark.full
    @allure.title("下载上报OTA_Master_Code_020B_DNS_Error")    
    def test_fota_caseid_1983227(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"020B"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC,
                                                            UA_Sts.DOWNLOAD,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_FINAL_FAILED.value,
                                                            errorCode=UA_ErrorCode.DNS_Error_0x02_0x0B.value)

    @pytest.mark.full
    @allure.title("下载上报OTA_Master_Code_020C_Https_ResponseErrorCode")    
    def test_fota_caseid_1983226(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"020C"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC,
                                                            UA_Sts.DOWNLOAD,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_FINAL_FAILED.value,
                                                            errorCode=UA_ErrorCode.Service_Unavailable_0x02_0x0C.value)
            
    @pytest.mark.full
    @allure.title("下载上报OTA_Master_Code_020D_Https_ResponseErrorCode")    
    def test_fota_caseid_1983225(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"020D"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC,
                                                            UA_Sts.DOWNLOAD,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_FINAL_FAILED.value,
                                                            errorCode=UA_ErrorCode.Not_Found_0x02_0x0D.value)
            
    @pytest.mark.full
    @allure.title("下载上报OTA_Master_Code_0221_DownloadGeneralError")    
    def test_fota_caseid_1983224(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0221"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC,
                                                            UA_Sts.DOWNLOAD,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_FINAL_FAILED.value,
                                                            errorCode=UA_ErrorCode.General_Error_0x02_0x21.value)

    @pytest.mark.full
    @allure.title("下载上报OTA_Master_Code_0222_File_SecurityCheck_Failed")    
    def test_fota_caseid_1983223(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0222"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC,
                                                            UA_Sts.DOWNLOAD,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_FINAL_FAILED.value,
                                                            errorCode=UA_ErrorCode.FileSecurityCheck_Error_0x02_0x22.value)
    @pytest.mark.full
    @allure.title("下载上报OTA_Master_Code_0224_SOAPayloadError")    
    def test_fota_caseid_1983221(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0224"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC,
                                                            UA_Sts.DOWNLOAD,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_FINAL_FAILED.value,
                                                            errorCode=UA_ErrorCode.PayLoadError_0x02_0x24.value)
            
    @pytest.mark.full
    @allure.title("下载上报OTA_Master_Code_0225_File-Size Error")    
    def test_fota_caseid_1983220(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0225"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC,
                                                            UA_Sts.DOWNLOAD,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_FINAL_FAILED.value,
                                                            errorCode=UA_ErrorCode.File_Size_Error_0x02_0x25.value)

    @pytest.mark.fota
    @pytest.mark.full
    @allure.title("ERROR_CODE重试_02_F4(Download Failed)")    
    def test_fota_caseid_1979769(self):
        with self.log_manage.check_jetlog_by_same_keywords(log_type=" fota:", keywords=[
                                                                                   '"stateCode":"02F4"',
                                                                                   '"stateCode":"02F4"',
                                                                                   '"stateCode":"02F4"'
                                                                                   ], timeout=120):
            time.sleep(2) #等待log manage启动
            self.ssh.set_airplane_mode(isOn.On)
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC,
                                                            UA_Sts.DOWNLOAD,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_FINAL_FAILED.value,
                                                            errorCode=UA_ErrorCode.File_Size_Error_0x02_0x25.value)
        self.ssh.set_airplane_mode(isOn.Off)

@allure.feature("基础架构")
@allure.story("FOTA")
class TestFotaNormal(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service")])
        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                                    FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.before_group_hv_ctl,
                                    FOTA_Skip_Debug.ecm3_down_hv,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.update_precondition_check,
                                    FOTA_Skip_Debug.cdc_acu_doip_check
                                    ], allow_sleep=False) 
        self.mix.update_version_debug(self.taskid,["DDM"])    

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, self.taskid)
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("下载上报OTA_Master_Code_02F0_Download Package Start")    
    def test_fota_caseid_1983232(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"02F0"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.mix.back_fota_to(FOTAMasteSts.ACTIVE, self.taskid)
    
    @pytest.mark.smoke
    @allure.title("下载上报OTA_Master_Code_02F1_Download Package")    
    def test_fota_caseid_1983233(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"02F1"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.mix.back_fota_to(FOTAMasteSts.ACTIVE, self.taskid)
            
    @pytest.mark.smoke
    @allure.title("下载上报OTA_Master_Code_02F2_Download Complete")    
    def test_fota_caseid_1983231(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"02F2"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.mix.back_fota_to(FOTAMasteSts.ACTIVE, self.taskid)
                
if __name__ == "__main__":
    pass

    




