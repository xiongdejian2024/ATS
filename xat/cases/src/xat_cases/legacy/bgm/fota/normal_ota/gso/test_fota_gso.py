import os
import sys
import pytest
import allure
from time import sleep
import random
import copy
import json
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
        self.soa.update([
            ("FotaMasterService","client"),
            ("UpdateAgentService","client","BGM_UA_Service"),
            ("V2TRoutingForwarder","client","V2TOTAFotaForwarder"),
            ("UpdateAgentService","server","CDC_UA_Service")
            ])
        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                                    FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.before_group_hv_ctl,
                                    FOTA_Skip_Debug.ecm3_down_hv,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.start_download,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ], allow_sleep=False) 
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])
        self.taskid_tmp = 99999 #赋值个平台不存在的taskid

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        self.soa.start_send_ua_response(DOMAIN.CDC)
        self.soa.start_send_ua_event(DOMAIN.CDC, self.soa.pack_ua_event_args(UA_Sts.IDLE))
        self.soa.empty_all()
                            
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.mix.fota_back_to_idle()
        self.soa.stop_send_ua_event(DOMAIN.CDC)
        self.soa.stop_send_ua_response(DOMAIN.CDC)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.sd_tester.write_ccp({948: 0x00})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({948: 0x00})  # 检查写入的ccp
            
    @pytest.mark.V_2_2
    @pytest.mark.full
    @allure.title("GSO_判断出口信息_无DownloadNetType_UA_StartDownload参数downloadNetworkMode_CCP#948=00") 
    def test_fota_caseid_1996885(self):  
        self.sd_tester.write_ccp({948: 0x00})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({948: 0x00})  # 检查写入的ccp
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data'].pop("downloadNetType")
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        UA_downloadNetworkMode = json.loads(self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=60)['args'])['downloadReq']['downloadNetworkMode']
        assert UA_downloadNetworkMode == 1
        
    @pytest.mark.V_2_2
    @pytest.mark.full
    @allure.title("GSO_判断出口信息_无DownloadNetType_UA_StartDownload参数downloadNetworkMode_CCP#948≠00") 
    def test_fota_caseid_1996886(self):  
        self.sd_tester.write_ccp({948: 0x03})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({948: 0x03})  # 检查写入的ccp
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data'].pop("downloadNetType")
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        UA_downloadNetworkMode = json.loads(self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=60)['args'])['downloadReq']['downloadNetworkMode']
        assert UA_downloadNetworkMode == 2
    
    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @allure.title("GSO_判断出口信息_DownloadNetType=1_UA_StartDownload参数downloadNetworkMode_CCP#948=00") 
    def test_fota_caseid_1996887(self):  
        self.sd_tester.write_ccp({948: 0x00})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({948: 0x00})  # 检查写入的ccp
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']["downloadNetType"] = 1
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        UA_downloadNetworkMode = json.loads(self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=60)['args'])['downloadReq']['downloadNetworkMode']
        assert UA_downloadNetworkMode == 1
        
    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @allure.title("GSO_判断出口信息_DownloadNetType=1_UA_StartDownload参数downloadNetworkMode_CCP#948≠00") 
    def test_fota_caseid_1996888(self):  
        self.sd_tester.write_ccp({948: 0x03})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({948: 0x03})  # 检查写入的ccp
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']["downloadNetType"] = 1
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        UA_downloadNetworkMode = json.loads(self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=60)['args'])['downloadReq']['downloadNetworkMode']
        assert UA_downloadNetworkMode == 2                          
    
    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @allure.title("GSO_判断出口信息_DownloadNetType=2_UA_StartDownload参数downloadNetworkMode_CCP#948=00") 
    def test_fota_caseid_1996889(self):  
        self.sd_tester.write_ccp({948: 0x00})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({948: 0x00})  # 检查写入的ccp
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']["downloadNetType"] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        UA_downloadNetworkMode = json.loads(self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=60)['args'])['downloadReq']['downloadNetworkMode']
        assert UA_downloadNetworkMode == 2
        
    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @allure.title("GSO_判断出口信息_DownloadNetType=2_UA_StartDownload参数downloadNetworkMode_CCP#948≠00") 
    def test_fota_caseid_1996890(self):  
        self.sd_tester.write_ccp({948: 0x03})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({948: 0x03})  # 检查写入的ccp
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']["downloadNetType"] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        UA_downloadNetworkMode = json.loads(self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=60)['args'])['downloadReq']['downloadNetworkMode']
        assert UA_downloadNetworkMode == 2        

    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @allure.title("GSO_判断出口信息_DownloadNetType=3_UA_StartDownload参数downloadNetworkMode_CCP#948=00") 
    def test_fota_caseid_1996891(self):  
        self.sd_tester.write_ccp({948: 0x00})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({948: 0x00})  # 检查写入的ccp
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']["downloadNetType"] = 3
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        UA_downloadNetworkMode = json.loads(self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=60)['args'])['downloadReq']['downloadNetworkMode']
        assert UA_downloadNetworkMode == 1
        
    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @allure.title("GSO_判断出口信息_DownloadNetType=3_UA_StartDownload参数downloadNetworkMode_CCP#948≠00") 
    def test_fota_caseid_1996892(self):  
        self.sd_tester.write_ccp({948: 0x03})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({948: 0x03})  # 检查写入的ccp
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']["downloadNetType"] = 3
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        UA_downloadNetworkMode = json.loads(self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=60)['args'])['downloadReq']['downloadNetworkMode']
        assert UA_downloadNetworkMode == 1                    

    @pytest.mark.V_2_2
    @pytest.mark.full
    @allure.title("GSO_判断出口信息_无DownloadNetType_下载非域控ECU_CCP#948=00") 
    def test_fota_caseid_1996898(self):  
        self.sd_tester.write_ccp({948: 0x00})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({948: 0x00})  # 检查写入的ccp
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50_NKR)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data'].pop("downloadNetType")
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords=['"stateCode":"02FA"'], timeout=70):
            assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status,target_status=FOTAMasteSts.ACTIVE.value, timeout=60)        
        
    @pytest.mark.V_2_2
    @pytest.mark.full
    @allure.title("GSO_判断出口信息_无DownloadNetType_下载非域控ECU_CCP#948≠00") 
    def test_fota_caseid_1996896(self):  
        self.sd_tester.write_ccp({948: 0x03})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({948: 0x03})  # 检查写入的ccp
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50_NKR)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data'].pop("downloadNetType")
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"02FA"'], timeout=70):
            time.sleep(60)
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.DOWNLOADING.value, "FOTA Status is not DOWNLOADING"

    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @allure.title("GSO_判断出口信息_DownloadNetType=1_下载非域控ECU_CCP#948=00") 
    def test_fota_caseid_1996900(self):  
        self.sd_tester.write_ccp({948: 0x00})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({948: 0x00})  # 检查写入的ccp
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50_NKR)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']["downloadNetType"] = 1
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords=['"stateCode":"02FA"'], timeout=70):
            assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status,target_status=FOTAMasteSts.ACTIVE.value, timeout=60)        
        
    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @allure.title("GSO_判断出口信息_DownloadNetType=1_下载非域控ECU_CCP#948≠00") 
    def test_fota_caseid_1996893(self):  
        self.sd_tester.write_ccp({948: 0x03})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({948: 0x03})  # 检查写入的ccp
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50_NKR)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']["downloadNetType"] = 1
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"02FA"'], timeout=70):
            time.sleep(60)
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.DOWNLOADING.value, "FOTA Status is not DOWNLOADING"

    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @allure.title("GSO_判断出口信息_DownloadNetType=2_下载非域控ECU_CCP#948=00") 
    def test_fota_caseid_1996894(self):  
        self.sd_tester.write_ccp({948: 0x00})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({948: 0x00})  # 检查写入的ccp
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50_NKR)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']["downloadNetType"] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"02FA"'], timeout=70):
            time.sleep(60)
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.DOWNLOADING.value, "FOTA Status is not DOWNLOADING"     
        
    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @allure.title("GSO_判断出口信息_DownloadNetType=2_下载非域控ECU_CCP#948≠00") 
    def test_fota_caseid_1996895(self):  
        self.sd_tester.write_ccp({948: 0x03})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({948: 0x03})  # 检查写入的ccp
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50_NKR)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']["downloadNetType"] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"02FA"'], timeout=70):
            time.sleep(60)
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.DOWNLOADING.value, "FOTA Status is not DOWNLOADING"

    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @allure.title("GSO_判断出口信息_DownloadNetType=3_下载非域控ECU_CCP#948=00") 
    def test_fota_caseid_1996897(self):  
        self.sd_tester.write_ccp({948: 0x00})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({948: 0x00})  # 检查写入的ccp
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50_NKR)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']["downloadNetType"] = 3
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords=['"stateCode":"02FA"'], timeout=70):
            assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status,target_status=FOTAMasteSts.ACTIVE.value, timeout=60)        
        
    @pytest.mark.V_2_2
    @pytest.mark.sanity
    @allure.title("GSO_判断出口信息_DownloadNetType=3_下载非域控ECU_CCP#948≠00") 
    def test_fota_caseid_1996899(self):  
        self.sd_tester.write_ccp({948: 0x03})
        self.sd_tester.reset_bgm()
        assert self.sd_tester.check_ccp_value({948: 0x03})  # 检查写入的ccp
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50_NKR)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']["downloadNetType"] = 3
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords=['"stateCode":"02FA"'], timeout=70):
            assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status,target_status=FOTAMasteSts.ACTIVE.value, timeout=60)        
                        
if __name__ == "__main__":
    pass

    




