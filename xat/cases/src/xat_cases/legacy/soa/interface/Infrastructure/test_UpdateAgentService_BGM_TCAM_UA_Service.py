import os
import sys
import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.soa.case_helper.fota_ua import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature("SOA服务接口")
@pytest.mark.wjj
@allure.story("架构基础/UpdateAgentService")
class TestBgmUA(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("UpdateAgentService","client","BGM_UA_Service")])

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.soa.ua_back_to_idle(DOMAIN.BGM)
        assert self.soa.get_ua_status(DOMAIN.BGM, UA_EVENT.Status) == 0, "UA Status != Idle"
           
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
           
    @pytest.mark.smoke
    @allure.title("BGM_UA_Event_Status")
    def test_caseid_1984198(self):
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelUpdate)
        self.soa.ck_s2s_event('UpdateAgentService_client_BGM_UA_Service',"Status",{"status":{"status":0,
                                                                                             "downloadStatus":{"downloadFileSize":0,"totalFileSize":0,"downloadSpeed":0,"status":255},
                                                                                             "preUpdateStatus":{"progress":0,"status":255},
                                                                                             "updateStatus":{"updateFileSize":0,"totalFileSize":0,"status":255},"errorCode":0}})

    @pytest.mark.full
    @allure.title("BGM_UA_Request_GetStatus")
    def test_caseid_1984199(self):
        self.soa.send_ua_request(DOMAIN.BGM, UA_REQUEST.CancelUpdate)
        self.soa.send_request_and_ck_resp(partner_key=f'UpdateAgentService_client_BGM_UA_Service', method_name=UA_REQUEST.GetStatus.name, args={}, ck_info=
            {"out": {
                "status": 0,
                "downloadStatus": {
                    "downloadFileSize": 0,
                    "totalFileSize": 0,
                    "downloadSpeed": 0,
                    "status": 255
                },
                "preUpdateStatus": {
                    "progress": 0,
                    "status": 255
                },
                "updateStatus": {
                    "updateFileSize": 0,
                    "totalFileSize": 0,
                    "status": 255
                },
                "errorCode": 0
                    }})
    
    @pytest.mark.full
    @allure.title("BGM_UA_Request_SuspendDownload")
    def test_caseid_1984200(self):
        self.soa.send_request_and_ck_resp('UpdateAgentService_client_BGM_UA_Service', "SuspendDownload", {}, {'out': 0})

    @pytest.mark.full
    @allure.title("BGM_UA_Request_ResumeDownload")
    def test_caseid_1984201(self):
        self.soa.send_request_and_ck_resp('UpdateAgentService_client_BGM_UA_Service', "ResumeDownload", {}, {'out': 0})

    @pytest.mark.sanity
    @allure.title("BGM_UA_Request_CancelDownload")
    def test_caseid_1984202(self):
        self.soa.send_request_and_ck_resp(partner_key=f'UpdateAgentService_client_BGM_UA_Service', method_name=UA_REQUEST.CancelDownload.name, args={}, ck_info={'out': 0})
        
    @pytest.mark.sanity
    @allure.title("BGM_UA_Request_StartUpdate")
    def test_caseid_1984203(self):
        self.soa.send_request_and_ck_resp(partner_key=f'UpdateAgentService_client_BGM_UA_Service', method_name=UA_REQUEST.StartUpdate.name, args={}, ck_info={'out': 0})

    @pytest.mark.smoke
    @allure.title("BGM_UA_Request_StartDownload")
    def test_caseid_1984207(self):
        self.soa.send_request_and_ck_resp(partner_key=f'UpdateAgentService_client_BGM_UA_Service', method_name=UA_REQUEST.Activate.name, args="BGM_Download_Req", ck_info={'out': 0})
        
    @pytest.mark.sanity
    @allure.title("BGM_UA_Request_Activate")
    def test_caseid_1984205(self):
        self.soa.send_request_and_ck_resp(partner_key=f'UpdateAgentService_client_BGM_UA_Service', method_name=UA_REQUEST.Activate.name, args={}, ck_info={'out': 0})
        
    @pytest.mark.sanity
    @allure.title("BGM_UA_Request_Rollback")
    def test_caseid_1984206(self):
        self.soa.send_request_and_ck_resp(partner_key=f'UpdateAgentService_client_BGM_UA_Service', method_name=UA_REQUEST.Rollback.name, args={}, ck_info={'out': 0})
        
    @pytest.mark.sanity
    @allure.title("BGM_UA_Request_CancelUpdate")
    def test_caseid_1984204(self):
        self.soa.send_request_and_ck_resp(partner_key=f'UpdateAgentService_client_BGM_UA_Service', method_name=UA_REQUEST.CancelUpdate.name, args={}, ck_info={'out': 0})
        
    @pytest.mark.sanity
    @allure.title("BGM_UA_Request_FinishUpdate")
    def test_caseid_1984194(self):
        self.soa.send_request_and_ck_resp(partner_key=f'UpdateAgentService_client_BGM_UA_Service', method_name=UA_REQUEST.FinishUpdate.name, args={}, ck_info={'out': 0})
        
    @pytest.mark.sanity
    @allure.title("BGM_UA_Request_PreUpdate")
    def test_caseid_1984208(self):
        self.soa.send_request_and_ck_resp(partner_key=f'UpdateAgentService_client_BGM_UA_Service', method_name=UA_REQUEST.PreUpdate.name, args={}, ck_info={'out': 255})

    @pytest.mark.sanity
    @allure.title("BGM_UA_Request_Rescue")
    def test_caseid_1985578(self):
        self.soa.send_request_and_ck_resp(partner_key=f'UpdateAgentService_client_BGM_UA_Service', method_name=UA_REQUEST.Rescue.name, args={}, ck_info={'out': 0})
        
@allure.feature("SOA服务接口")
@pytest.mark.wjj
@allure.story("架构基础/UpdateAgentService")
class TestTcamUA(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("UpdateAgentService","client","TCAM_UA_Service")])

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.soa.ua_back_to_idle(DOMAIN.TCAM)
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == 0, "UA Status != Idle"
           
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
 
    @pytest.mark.smoke
    @allure.title("TCAM_UA_Event_Status")
    def test_caseid_1984209(self):
        self.soa.ck_s2s_event('UpdateAgentService_client_TCAM_UA_Service',"Status",{"status":{"status":0,
                                                                                             "downloadStatus":{"downloadFileSize":0,"totalFileSize":0,"downloadSpeed":0,"status":255},
                                                                                             "preUpdateStatus":{"progress":0,"status":255},
                                                                                             "updateStatus":{"updateFileSize":0,"totalFileSize":0,"status":255},"errorCode":0}})         

    @pytest.mark.sanity
    @allure.title("TCAM_UA_Request_GetStatus")
    def test_caseid_1984210(self):
        self.soa.send_request_and_ck_resp(partner_key=f'UpdateAgentService_client_TCAM_UA_Service', method_name=UA_REQUEST.GetStatus.name, args={}, ck_info=
            {"out": {
                "status": 0,
                "downloadStatus": {
                    "downloadFileSize": 0,
                    "totalFileSize": 0,
                    "downloadSpeed": 0,
                    "status": 255
                },
                "preUpdateStatus": {
                    "progress": 0,
                    "status": 255
                },
                "updateStatus": {
                    "updateFileSize": 0,
                    "totalFileSize": 0,
                    "status": 255
                },
                "errorCode": 0
                    }})
        
    @pytest.mark.sanity
    @allure.title("TCAM_UA_Request_SuspendDownload")
    def test_caseid_1984220(self):
        self.soa.send_request_and_ck_resp('UpdateAgentService_client_TCAM_UA_Service', "SuspendDownload", {}, {'out': 0})

    @pytest.mark.sanity
    @allure.title("TCAM_UA_Request_ResumeDownload")
    def test_caseid_1984221(self):
        self.soa.send_request_and_ck_resp('UpdateAgentService_client_TCAM_UA_Service', "ResumeDownload", {}, {'out': 0})
        
    @pytest.mark.full
    @allure.title("TCAM_UA_Request_CancelDownload")
    def test_caseid_1984211(self):
        self.soa.send_request_and_ck_resp(partner_key=f'UpdateAgentService_client_TCAM_UA_Service', method_name=UA_REQUEST.CancelDownload.name, args={}, ck_info={'out': 0})
        
    @pytest.mark.full
    @allure.title("TCAM_UA_Request_StartUpdate")
    def test_caseid_1984212(self):
        self.soa.send_request_and_ck_resp(partner_key=f'UpdateAgentService_client_TCAM_UA_Service', method_name=UA_REQUEST.StartUpdate.name, args={}, ck_info={'out': 0})

    @pytest.mark.full
    @allure.title("TCAM_UA_Request_StartDownload")
    def test_caseid_1984213(self):
        assert self.soa.get_ua_status(DOMAIN.TCAM, UA_EVENT.Status) == 0, "UA Status != Idle"
        self.soa.send_request_and_ck_resp(partner_key=f'UpdateAgentService_client_TCAM_UA_Service', method_name=UA_REQUEST.Activate.name, args="TCAM_Download_Req", ck_info={'out': 0})
        
    @pytest.mark.full
    @allure.title("TCAM_UA_Request_Activate")
    def test_caseid_1984214(self):
        self.soa.send_request_and_ck_resp(partner_key=f'UpdateAgentService_client_TCAM_UA_Service', method_name=UA_REQUEST.Activate.name, args={}, ck_info={'out': 0})
        
    @pytest.mark.full
    @allure.title("TCAM_UA_Request_Rollback")
    def test_caseid_1984215(self):
        self.soa.send_request_and_ck_resp(partner_key=f'UpdateAgentService_client_TCAM_UA_Service', method_name=UA_REQUEST.Rollback.name, args={}, ck_info={'out': 0})
        
    @pytest.mark.full
    @allure.title("TCAM_UA_Request_CancelUpdate")
    def test_caseid_1984216(self):
        self.soa.send_request_and_ck_resp(partner_key=f'UpdateAgentService_client_TCAM_UA_Service', method_name=UA_REQUEST.CancelUpdate.name, args={}, ck_info={'out': 0})
        
    @pytest.mark.sanity
    @allure.title("TCAM_UA_Request_FinishUpdate")
    def test_caseid_1984217(self):
        self.soa.send_request_and_ck_resp(partner_key=f'UpdateAgentService_client_TCAM_UA_Service', method_name=UA_REQUEST.FinishUpdate.name, args={}, ck_info={'out': 0})
        
    @pytest.mark.full
    @allure.title("TCAM_UA_Request_PreUpdate")
    def test_caseid_1984218(self):
        self.soa.send_request_and_ck_resp(partner_key=f'UpdateAgentService_client_TCAM_UA_Service', method_name=UA_REQUEST.PreUpdate.name, args={}, ck_info={'out': 255})
        
    @pytest.mark.full
    @allure.title("TCAM_UA_Request_Rescue")
    def test_caseid_1985579(self):
        self.soa.send_request_and_ck_resp(partner_key=f'UpdateAgentService_client_TCAM_UA_Service', method_name=UA_REQUEST.Rescue.name, args={}, ck_info={'out': 0})

        

    





