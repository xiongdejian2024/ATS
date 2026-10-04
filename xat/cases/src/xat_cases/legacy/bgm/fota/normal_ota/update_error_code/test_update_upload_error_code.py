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
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.READY_TO_INSTALL)
        self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.ACTIVE.value, 100)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "PreUpdate", timeout=180)
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_RUNNING.value,
                                                          )
        time.sleep(5) #模拟 CDC 在 PREUPDATE_RUNNING 状态，持续一段时间
        
        
        # self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
        #                                                   ua_sts=UA_Sts.READY_TO_INSTALL,
        #                                                   ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
        #                                                   ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
        #                                                   )
        # self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        # self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.UPDATE_FINISH)
        # self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "Activate", timeout=300)
        # self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.SYSTEM_ACTIVE)
        # self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "FinishUpdate", timeout=300)
        # self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        time.sleep(5) #留给OTA Master充足的时间记住CDC UA Status = Idle状态
        self.soa.stop_send_ua_event(DOMAIN.CDC)
        self.soa.stop_send_ua_response(DOMAIN.CDC)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("域控刷写_CDC/ACU/TCAM 升级_Update finish 1min切状态超时")    
    def test_fota_caseid_1982313(self):
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          )
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.INSTALLING)
        time.sleep(10) #等待10S后检查关键字
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.UPDATE_FINISH)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='CDC_UA_Servicenot ACTIVATING after Activate 1min', timeout=70):
            pass #70S 内检查到切面超时的log

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_DomainECUUpdateTimeout(0327)")    
    def test_fota_caseid_1983097(self):
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          )
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.INSTALLING)
        time.sleep(3300) #等待55min后检查关键字
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0327"', timeout=400):
            pass    
 
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("域控刷写_CDC/ACU/TCAM 升级_域控升级超时>60min")    
    def test_fota_caseid_1982312(self):
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          )
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.INSTALLING)
        time.sleep(3300) #等待55min后检查关键字
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0327"',
                                                                                   'ChangeState:exit_ota => failed'], timeout=500):
            pass 
        
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_透传/升级阶段_VBFFormat_Error(030E)")    
    def test_fota_caseid_1985310(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"030E"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.VBFFormat_Error_0x03_0x0E.value
                                                            )
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_透传/升级阶段_Decryption_Error(030F)")    
    def test_fota_caseid_1985314(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"030F"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.Decryption_Error_0x03_0x0F.value
                                                            )
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("FOTA解密过程_切状态超1min解密失败(03 0F)")    
    def test_fota_caseid_1982344(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"030F"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.Decryption_Error_0x03_0x0F.value
                                                            )
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_透传/升级阶段_VBF_Signature verification_Error(0310)")    
    def test_fota_caseid_1985306(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0310"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.VBF_Signature_verification_Error_0x03_0x10.value
                                                            )
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_透传/升级阶段_VBF Version Error(0311)")    
    def test_fota_caseid_1985298(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0311"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.VBFVersionError_0x03_0x11.value
                                                            )
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_透传/升级阶段_DeletePackage error(0305)")    
    def test_fota_caseid_1985313(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0305"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.DeletePackage_Error_0x03_0x05.value
                                                            )
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_透传/升级阶段_ChangState Error(0306)")    
    def test_fota_caseid_1985307(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0306"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.ChangState_Error_0x03_0x06.value
                                                            )
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_透传/升级阶段_CanNotCancel(0307)")    
    def test_fota_caseid_1985304(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0307"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.CanNotCancel_0x03_0x07.value
                                                            )
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_透传/升级阶段_CancelError(031A)")    
    def test_fota_caseid_1985301(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"031A"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.CancelError_0x03_0x1A.value
                                                            )
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_透传/升级阶段_Reset Condition Error(031B)")    
    def test_fota_caseid_1985303(self):
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          )
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"031B"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.Reset_Condition_Error_0x03_0x1B.value
                                                            )
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_透传/升级阶段_Reset Error(031C)")    
    def test_fota_caseid_1985297(self):
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          )
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"031C"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.Reset_Error_0x03_0x1C.value
                                                            )
    
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("域控刷写_CDC/ACU/TCAM 升级_Activating SOA链接超时10min(03 1C)")    
    def test_fota_caseid_1982307(self):
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          )
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"031C"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.Reset_Error_0x03_0x1C.value
                                                            )
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("域控刷写_CDC/ACU/TCAM 升级_Activating 超时10min(03 1C)")    
    def test_fota_caseid_1982308(self):
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          )
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"031C"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.Reset_Error_0x03_0x1C.value
                                                            )
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("域控刷写_CDC/ACU/TCAM 升级_Activating 失败(03 1C)")    
    def test_fota_caseid_1982309(self):
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          )
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"031C"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.Reset_Error_0x03_0x1C.value
                                                            )

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_透传/升级阶段_Insufficient Resources(0312)")    
    def test_fota_caseid_1985305(self):
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          )
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0312"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.Insufficient_Resourcesr_0x03_0x12.value
                                                            )
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_透传/升级阶段_Software Call failed(0313)")    
    def test_fota_caseid_1985322(self):
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          )
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0313"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.Software_Call_failed_0x03_0x13.value
                                                            )
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_透传/升级阶段_Software Incompatibility(0314)")    
    def test_fota_caseid_1985311(self):
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          )
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0314"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.Software_Incompatibility_0x03_0x14.value
                                                            )
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_透传/升级阶段_DifferentialBaseline Error(0315)")    
    def test_fota_caseid_1985312(self):
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          )
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0315"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.Differential_Baseline_Error_0x03_0x15.value
                                                            )
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_透传/升级阶段_UpdateError(0316)")    
    def test_fota_caseid_1985308(self):
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          )
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0316"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.UpdateError_0x03_0x16.value
                                                            )
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("域控刷写_CDC/ACU/TCAM 升级_Readt to install 1min切状态超时(0316)")    
    def test_fota_caseid_1982314(self):
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          )
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0316"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.UpdateError_0x03_0x16.value
                                                            )
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("域控刷写_CDC/ACU/TCAM 升级失败(03 16)")    
    def test_fota_caseid_1982310(self):
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          )
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0316"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.UpdateError_0x03_0x16.value
                                                            )  
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_透传/升级阶段_IntegratedFailed(0317)")    
    def test_fota_caseid_1985309(self):
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          )
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0317"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.IntegratedFailed_0x03_0x17.value
                                                            )
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_透传/升级阶段_RollBackError(0318)")    
    def test_fota_caseid_1985323(self):
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          )
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0318"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.RollBackError_0x03_0x18.value
                                                            )
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_透传/升级阶段_Permission Error(0319)")    
    def test_fota_caseid_1985299(self):
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          )
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0319"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.Permission_Error_0x03_0x19.value
                                                            )
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_透传/升级阶段_FotaStateError(030C)")    
    def test_fota_caseid_1985300(self):
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          )
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"030C"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.FotaStateError_0x03_0x0C.value
                                                            )
            
    # @pytest.mark.V_1_4
    # @pytest.mark.full
    # @allure.title("域控刷写_CDC/ACU/TCAM 升级_UA状态为installing(03 0C)")    
    # def test_fota_caseid_1982319(self):
    #     self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
    #                                                       ua_sts=UA_Sts.READY_TO_INSTALL,
    #                                                       ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
    #                                                       ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
    #                                                       )
    #     self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"030C"', timeout=120):
    #         time.sleep(2) #等待log manage启动
    #         self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
    #                                                         ua_sts=UA_Sts.READY_TO_INSTALL,
    #                                                         ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
    #                                                         ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
    #                                                         errorCode=UA_ErrorCode.FotaStateError_0x03_0x0C.value
    #                                                         )
            
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("上传云端_透传_CallFunctionTimeOut(032C)")    
    def test_fota_caseid_1985302(self):
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                          )
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "StartUpdate", timeout=180)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"032C"', timeout=120):
            time.sleep(2) #等待log manage启动
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                            ua_sts=UA_Sts.READY_TO_INSTALL,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                            ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_FAILED.value,
                                                            errorCode=UA_ErrorCode.CallFunctionTimeOut_0x03_0x2C.value
                                                            )
            
            
if __name__ == "__main__":
    pass

    




