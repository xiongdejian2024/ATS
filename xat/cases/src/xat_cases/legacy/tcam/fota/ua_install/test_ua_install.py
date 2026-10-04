import os
import sys
import pytest
import allure
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
                         ("RtcAlarmService","client")])
        sleep(20)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.back_ua_to(DOMAIN.TCAM, UA_Sts.READY_TO_INSTALL, self.TCAM_Download_Req)  

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        self.sd_tester.routine_ctrl_and_check(TA.TCAM, 0xA100, 0x01, SESSION.DEFAULT, UnLock.L0, '02','7101a1001000')      
        self.soa.ua_back_to_idle(DOMAIN.TCAM)
        super().after_class(self, ecu)

    @pytest.mark.full 
    @allure.title("夜间升级_RTC_SetBookEvent")
    def test_fota_caseid_1985776(self, ecu):
        appiont_time_1 = self.mix.generate_fota_appointment_time(120)
        appiont_time_2 = self.mix.generate_fota_appointment_time(300)
        self.soa.send_request_and_return_resp("RtcAlarmService_client", "SetBookEvent",
                                                    {"bookEventInfo": {"serviceName": "eat",
                                                                        "repeatType": 0,
                                                                        "rtcTime": appiont_time_1,
                                                                        "timerFlag": "eatapple1",
                                                                        "rtcFlag": False,
                                                                        "bookInfo":
                                                                            {"bookType": "1",
                                                                            "repeatType": 0, 
                                                                            "startTime": appiont_time_1,
                                                                            "stopTime": appiont_time_1 + 600}}})["out"]    
        self.soa.send_request_and_return_resp("RtcAlarmService_client", "SetBookEvent",
                                                    {"bookEventInfo": {"serviceName": "eat",
                                                                        "repeatType": 0,
                                                                        "rtcTime": appiont_time_2,
                                                                        "timerFlag": "eatapple2",
                                                                        "rtcFlag": False,
                                                                        "bookInfo":
                                                                            {"bookType": "1",
                                                                            "repeatType": 0, 
                                                                            "startTime": appiont_time_2,
                                                                            "stopTime": appiont_time_2 + 600}}})["out"]    
        self.soa.send_request_and_ck_resp("RtcAlarmService_client", "GetRtcEventInfoList",
                                                   {"serviceName": "eat"}, {
                                                      "out": [{"serviceName": "eat",
                                                                        "repeatType": 0,
                                                                        "rtcTime": appiont_time_1,
                                                                        "timerFlag": "eatapple1",
                                                                        "rtcFlag": False,
                                                                        "bookInfo":
                                                                            {"bookType": "1",
                                                                            "repeatType": 0, 
                                                                            "startTime": appiont_time_1,
                                                                            "stopTime": appiont_time_1 + 600}},
                                                              {"serviceName": "eat",
                                                                        "repeatType": 0,
                                                                        "rtcTime": appiont_time_2,
                                                                        "timerFlag": "eatapple2",
                                                                        "rtcFlag": False,
                                                                        "bookInfo":
                                                                            {"bookType": "1",
                                                                            "repeatType": 0, 
                                                                            "startTime": appiont_time_2,
                                                                            "stopTime": appiont_time_2 + 600}}
                                                              ]}) 

    @pytest.mark.full 
    @allure.title("TCAM_UA_Status_periodic_Installing")
    def test_fota_caseid_1985410(self, ecu):
        self.mix.back_ua_to(DOMAIN.TCAM, UA_Sts.INSTALLING, self.TCAM_Download_Req)  
        assert self.soa.check_ua_event_period(DOMAIN.TCAM, target_period=2.0, epsilon=0.1)

    @pytest.mark.smoke 
    @allure.title("FOTA解密过程_READY_TO_INSTALL")
    def test_fota_caseid_1982980(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.DownloadStatus) == 1 and self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.PreUpdateStatus) == 0
        
    @pytest.mark.smoke 
    @allure.title("FOTA解密过程_READY_TO_INSTALL_PreUpdate_解密成功")
    def test_fota_caseid_1982979(self, ecu):
        self.mix.back_ua_to(DOMAIN.TCAM, UA_Sts.READY_TO_INSTALL, self.TCAM_Download_Req)  
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.PreUpdate)
        assert self.soa.till_ua_event_to(DOMAIN.TCAM, UA_EVENT.PreUpdateStatus, target_status=2, timeout=300)
        
    @pytest.mark.full 
    @allure.title("FOTA解密过程_READY_TO_INSTALL_PreUpdate_解密失败")
    def test_fota_caseid_1982978(self, ecu):
        self.mix.back_ua_to(DOMAIN.TCAM, UA_Sts.READY_TO_INSTALL, self.TCAM_Download_Req)  
        self.ssh.type_commands(DeviceName.TCAM, "rm /mnt/sdcard/Update/ua/*;sync")
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.PreUpdate)
        assert self.soa.till_ua_event_to(DOMAIN.TCAM, UA_EVENT.PreUpdateStatus, target_status=3, timeout=300)
        
    @pytest.mark.smoke 
    @allure.title("TCAM升级_Installing_升级成功")
    def test_fota_caseid_1982976(self, ecu):
        self.mix.back_ua_to(DOMAIN.TCAM, UA_Sts.UPDATE_FINISH, self.TCAM_Download_Req)  
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == 4 and self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.UpdateStatus) == 3
        
    @pytest.mark.full 
    @allure.title("TCAM升级_Installing_升级失败")
    def test_fota_caseid_1982975(self, ecu):
        self.mix.back_ua_to(DOMAIN.TCAM, UA_Sts.UPDATE_FAILED, self.TCAM_Download_Req)  
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == 9
        
    @pytest.mark.smoke 
    @allure.title("退出流程_FinishUptdate")
    def test_fota_caseid_1982974(self, ecu):
        self.mix.back_ua_to(DOMAIN.TCAM, UA_Sts.SYSTEM_ACTIVE, self.TCAM_Download_Req)  
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.FinishUpdate)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == 0 and not self.ssh.check_ua_package(DOMAIN.TCAM)
        
    @pytest.mark.smoke 
    @allure.title("TCAM升级_Installing_强刷BOOT")
    def test_fota_caseid_1985670(self, ecu):
        self.ssh.update_ua_skip(DOMAIN.TCAM, True)
        self.soa.ua_back_to_idle(DOMAIN.TCAM)
        self.mix.back_ua_to(DOMAIN.TCAM, UA_Sts.SYSTEM_ACTIVE, self.TCAM_Download_Req)
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.FinishUpdate)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == 0 
        self.ssh.update_ua_skip(DOMAIN.TCAM, False)
        
    @pytest.mark.smoke 
    @allure.title("FOTA_Mode_进入")
    def test_fota_caseid_1982977(self, ecu):
        # 31 01 A1 00 01
        self.sd_tester.routine_ctrl_and_check(TA.TCAM, 0xA100, 0x01, SESSION.DEFAULT, UnLock.L0, '01','7101a1001000')

    @pytest.mark.smoke 
    @allure.title("FOTA_Mode_退出")
    def test_fota_caseid_1982973(self, ecu):
        # 31 01 A1 00 02
        self.sd_tester.routine_ctrl_and_check(TA.TCAM, 0xA100, 0x01, SESSION.DEFAULT, UnLock.L0, '02','7101a1001000')      

    @pytest.mark.full 
    @allure.title("域控升级Error_Code_TCAM_UA_FotaStateError_030C")
    def test_fota_caseid_1985667(self, ecu):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == UA_Sts.READY_TO_INSTALL.value ,"UA Status != Ready_to_Install"
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.Activate)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.ErrorCode) == UA_ErrorCode.FotaStateError_0x03_0x0C.value
        
    @pytest.mark.full 
    @allure.title("域控升级Error_Code_TCAM_UA_0x03_0x0FDecryption_Error")
    def test_fota_caseid_1985666(self, ecu):
        self.soa.ua_back_to_idle(DOMAIN.TCAM)
        self.soa.send_ua_request(DOMAIN.TCAM, UA_REQUEST.StartDownload, {
            "downloadReq": {
                "fileNumber": 1,
                "fileInformations": [
                    {
                        "pn": "8895036217  B",
                        "version": "6110110140 AC",
                        "size": 186402848,
                        "fileName": "6110110140AC.bin",
                        "url": "https://t-ivs-fota.cdn.bcebos.com/ofm/b7f77f14e1d4272f45f16a14158d81672d171fde/cd49d385-f2f6-611e-d997-049345aabd8f/6110110140AC.bin?responseContentType=application%2Foctet-stream&authorization=bce-auth-v1%2F289a3f3e82b34da4973652d035b59cc3%2F2023-12-25T09%3A57%3A22Z%2F-1%2F%2F27149e8feccdb7c9cff54748aeb788a31b934c47be08c1b5aec0d703bff59c80",
                        "signature": "MEQCIHkHR+ZDVoa3biXgnPHB5Aubqasm/sr/VU5k60zLKAYtAiAwuAIUA3S0qZY0bGGAGH+lsAz0AXZHHF1mgtVyQFWsig==",
                        "keyId": "abc",
                        "encKey": "abc"
                    }
                ],
                "keyInformation": {
                    "keyId": "abc",
                    "encKey": "abc"
                },
                "mode": 0
            }
        })
        assert self.soa.till_ua_event_to(DOMAIN.TCAM, UA_EVENT.Status, target_status=2, timeout=1800)
        self.soa.send_ua_request(DOMAIN.TCAM, ua_request=UA_REQUEST.PreUpdate)
        assert self.soa.till_ua_event_to(DOMAIN.TCAM, UA_EVENT.ErrorCode, target_status=UA_ErrorCode.Decryption_Error_0x03_0x0F.value, timeout=300)
        
    @pytest.mark.smoke 
    @allure.title("车机预约升级-到达 预约时间后-TCAM发送时间到达通知接口")
    def test_fota_caseid_1988200(self, ecu):
        appiont_time = self.mix.generate_fota_appointment_time(120)
        self.soa.send_request_and_return_resp("RtcAlarmService_client", "SetBookEvent",
                                                    {"bookEventInfo": {"serviceName": "fota",
                                                                        "repeatType": 0,
                                                                        "rtcTime": appiont_time,
                                                                        "timerFlag": "flag1",
                                                                        "rtcFlag": False,
                                                                        "bookInfo":
                                                                            {"bookType": "1",
                                                                            "repeatType": 0, 
                                                                            "startTime": appiont_time,
                                                                            "stopTime": appiont_time + 600}}})["out"]   
        time.sleep(130)
        assert self.soa.return_latest_event("RtcAlarmService_client", "NotifyTimeUpEventInfo")['bookEvent']['rtcTime'] == appiont_time
        
if __name__ == "__main__":
    pass