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
from xat_cases.legacy.bgm.case_helper.test_fota_bridge import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("AcuModeManagerService","server"),
                         ("UpdateAgentService","server","CDC_UA_Service"),
                         ("V2TRoutingForwarder","client","V2TOTAFotaForwarder")])
        self.ssh.update_skip_debug([FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.before_group_hv_ctl,
                                    FOTA_Skip_Debug.ecm3_down_hv,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.update_precondition_check,
                                    FOTA_Skip_Debug.car_mode_normal
                                    ]) 
        self.mix.set_enter_boot_condition(UsageMode.CONVENIENCE, low_volt_power=14, vehspd=0)
        self.taskid_tmp = 99999
        self.bridgeId = 88888
        self.mix.update_version_debug(self.taskid_tmp,[DOMAIN.BGM]) 

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        self.soa.start_send_ua_response(DOMAIN.CDC)
        self.soa.start_send_ua_event(DOMAIN.CDC, self.soa.pack_ua_event_args(UA_Sts.IDLE))
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50['data']['serialNumber'] = 1
            Task_Info_Type50['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.NEW_TASK.value, 20), "type50 not take effect"
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, self.taskid_tmp)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=20)
        assert self.soa.get_fota_status(MASTER_EVENT.TaskType) == 2        
        self.soa.empty_all()
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.mix.fota_back_to_idle()
        self.sd_tester.reset_bgm()
        self.soa.stop_send_ua_event(DOMAIN.CDC)
        self.soa.stop_send_ua_response(DOMAIN.CDC)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        
    @pytest.mark.smoke
    @allure.title("一键过桥下载_维持唤醒_维持唤醒和不可开车动作")    
    def test_fota_caseid_1987685(self):
        self.bus_comm.set_fota_download_wake_condition(display_hv_soc=900, low_volt_soc=90)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1200), "Not Enter Bridge Trun Download"   
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50_CDC = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50_CDC['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50_CDC['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50_CDC['data']['serialNumber'] = 2
            Task_Info_Type50_CDC['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50_CDC)
        self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=300)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.DOWNLOAD) 
        assert self.mix.check_fota_keep_awake(pnc29=True,
                                        acu_keep_alive=True,
                                        up_inactive=True,
                                        hv_active=True), "Not Send Awake Signal"
        assert self.mix.check_fota_setStartInhibit(startInhibit=True)
        
    @pytest.mark.smoke
    @allure.title("一键过桥下载_Status广播")    
    def test_fota_caseid_1987676(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1200), "Not Enter Bridge Trun Download"   
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50_CDC = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50_CDC['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50_CDC['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50_CDC['data']['serialNumber'] = 2
            Task_Info_Type50_CDC['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50_CDC)
        self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=300)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.DOWNLOAD) 
        assert self.soa.get_fota_status(MASTER_EVENT.SerialNumber) == 2 and self.soa.get_fota_status(MASTER_EVENT.TaskType) == FOTA_TaskType.Bridge.value, "Illegal SerialNumber or TaskType"

    @pytest.mark.full
    @allure.title("一键过桥_pre_download_check_GetStatus不回复")    
    def test_fota_caseid_1987675(self):
        self.soa.stop_send_ua_response(DOMAIN.CDC)
        try:
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1200), "First Update Fail"        
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
                Task_Info_Type50_CDC = copy.deepcopy(self.Task_Info_Type50_CDC)
                Task_Info_Type50_CDC['data']['taskId'] = self.taskid_tmp
                Task_Info_Type50_CDC['data']['bridgeId'] = self.bridgeId
                Task_Info_Type50_CDC['data']['serialNumber'] = 2
                Task_Info_Type50_CDC['data']['currentFotaTask'] = 2
            self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50_CDC)
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=[
                                                                                    #    '"stateCode":"0200"', # DownloadReqTimeOut
                                                                                    '"stateCode":"02F4"',
                                                                                    '"stateCode":"03F7"'], timeout=1800):
                pass     
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value and \
                self.soa.get_fota_status(MASTER_EVENT.SerialNumber) == 2 and \
                self.soa.get_fota_status(MASTER_EVENT.TaskType) == FOTA_TaskType.Bridge.value, "Illegal SerialNumber or TaskType"
        except Exception as e:
            logger.error(f"异常》》{str(e)}")
        finally:
            self.soa.start_send_ua_response(DOMAIN.CDC)

    @pytest.mark.full
    @allure.title("一键过桥_pre_download_check_UA_Activing_Fail")    
    def test_fota_caseid_1987669(self):
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1200), "First Update Fail"        
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.ACTIVATING) 
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50_CDC = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50_CDC['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50_CDC['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50_CDC['data']['serialNumber'] = 2
            Task_Info_Type50_CDC['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50_CDC)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=[
                                                                                #    '"stateCode":"02F5"', # 	Mission Confusion
                                                                                   '"stateCode":"02F4"',
                                                                                   '"stateCode":"03F7"'], timeout=1800):
            pass     
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value and \
               self.soa.get_fota_status(MASTER_EVENT.SerialNumber) == 2 and \
               self.soa.get_fota_status(MASTER_EVENT.TaskType) == FOTA_TaskType.Bridge.value, "Illegal SerialNumber or TaskType"

    @pytest.mark.full
    @allure.title("一键过桥_pre_download_check_UA_Download_Fail")    
    def test_fota_caseid_1987674(self):
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1200), "First Update Fail"        
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.DOWNLOAD) 
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50_CDC = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50_CDC['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50_CDC['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50_CDC['data']['serialNumber'] = 2
            Task_Info_Type50_CDC['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50_CDC)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=[
                                                                                #    '"stateCode":"02F5"', # 	Mission Confusion
                                                                                   '"stateCode":"02F4"',
                                                                                   '"stateCode":"03F7"'], timeout=1800):
            pass     
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value and \
               self.soa.get_fota_status(MASTER_EVENT.SerialNumber) == 2 and \
               self.soa.get_fota_status(MASTER_EVENT.TaskType) == FOTA_TaskType.Bridge.value, "Illegal SerialNumber or TaskType"

    @pytest.mark.full
    @allure.title("一键过桥_pre_download_check_UA_Installing_Fail")    
    def test_fota_caseid_1987672(self):
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1200), "First Update Fail"        
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.INSTALLING) 
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50_CDC = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50_CDC['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50_CDC['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50_CDC['data']['serialNumber'] = 2
            Task_Info_Type50_CDC['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50_CDC)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=[
                                                                                #    '"stateCode":"02F5"', # 	Mission Confusion
                                                                                   '"stateCode":"02F4"',
                                                                                   '"stateCode":"03F7"'], timeout=1800):
            pass     
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value and \
               self.soa.get_fota_status(MASTER_EVENT.SerialNumber) == 2 and \
               self.soa.get_fota_status(MASTER_EVENT.TaskType) == FOTA_TaskType.Bridge.value, "Illegal SerialNumber or TaskType"

    @pytest.mark.full
    @allure.title("一键过桥_pre_download_check_UA_Ready_to_Install_Fail")    
    def test_fota_caseid_1987673(self):
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1200), "First Update Fail"        
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.READY_TO_INSTALL) 
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50_CDC = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50_CDC['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50_CDC['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50_CDC['data']['serialNumber'] = 2
            Task_Info_Type50_CDC['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50_CDC)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=[
                                                                                #    '"stateCode":"02F5"', # 	Mission Confusion
                                                                                   '"stateCode":"02F4"',
                                                                                   '"stateCode":"03F7"'], timeout=1800):
            pass     
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value and \
               self.soa.get_fota_status(MASTER_EVENT.SerialNumber) == 2 and \
               self.soa.get_fota_status(MASTER_EVENT.TaskType) == FOTA_TaskType.Bridge.value, "Illegal SerialNumber or TaskType"

    @pytest.mark.full
    @allure.title("一键过桥_pre_download_check_UA_Rolling_Back_Fail")    
    def test_fota_caseid_1987671(self):
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1200), "First Update Fail"        
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.ROLLING_BACK) 
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50_CDC = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50_CDC['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50_CDC['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50_CDC['data']['serialNumber'] = 2
            Task_Info_Type50_CDC['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50_CDC)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=[
                                                                                #    '"stateCode":"02F5"', # 	Mission Confusion
                                                                                   '"stateCode":"02F4"',
                                                                                   '"stateCode":"03F7"'], timeout=1800):
            pass     
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value and \
               self.soa.get_fota_status(MASTER_EVENT.SerialNumber) == 2 and \
               self.soa.get_fota_status(MASTER_EVENT.TaskType) == FOTA_TaskType.Bridge.value, "Illegal SerialNumber or TaskType"

    @pytest.mark.full
    @allure.title("一键过桥_pre_download_check_UA_System_Active_Fail")    
    def test_fota_caseid_1987667(self):
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1200), "First Update Fail"        
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.SYSTEM_ACTIVE) 
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50_CDC = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50_CDC['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50_CDC['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50_CDC['data']['serialNumber'] = 2
            Task_Info_Type50_CDC['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50_CDC)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=[
                                                                                #    '"stateCode":"02F5"', # 	Mission Confusion
                                                                                   '"stateCode":"02F4"',
                                                                                   '"stateCode":"03F7"'], timeout=1800):
            pass     
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value and \
               self.soa.get_fota_status(MASTER_EVENT.SerialNumber) == 2 and \
               self.soa.get_fota_status(MASTER_EVENT.TaskType) == FOTA_TaskType.Bridge.value, "Illegal SerialNumber or TaskType"

    @pytest.mark.full
    @allure.title("一键过桥_pre_download_check_UA_Update_Failed_Fail")    
    def test_fota_caseid_1987668(self):
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1200), "First Update Fail"        
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.UPDATE_FAILED) 
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50_CDC = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50_CDC['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50_CDC['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50_CDC['data']['serialNumber'] = 2
            Task_Info_Type50_CDC['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50_CDC)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=[
                                                                                #    '"stateCode":"02F5"', # 	Mission Confusion
                                                                                   '"stateCode":"02F4"',
                                                                                   '"stateCode":"03F7"'], timeout=1800):
            pass     
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value and \
               self.soa.get_fota_status(MASTER_EVENT.SerialNumber) == 2 and \
               self.soa.get_fota_status(MASTER_EVENT.TaskType) == FOTA_TaskType.Bridge.value, "Illegal SerialNumber or TaskType"

    @pytest.mark.full
    @allure.title("一键过桥_pre_download_check_UA_Update_Finish_Fail")    
    def test_fota_caseid_1987670(self):
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1200), "First Update Fail"        
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.UPDATE_FINISH) 
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50_CDC = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50_CDC['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50_CDC['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50_CDC['data']['serialNumber'] = 2
            Task_Info_Type50_CDC['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50_CDC)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=[
                                                                                #    '"stateCode":"02F5"', # 	Mission Confusion
                                                                                   '"stateCode":"02F4"',
                                                                                   '"stateCode":"03F7"'], timeout=1800):
            pass     
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value and \
               self.soa.get_fota_status(MASTER_EVENT.SerialNumber) == 2 and \
               self.soa.get_fota_status(MASTER_EVENT.TaskType) == FOTA_TaskType.Bridge.value, "Illegal SerialNumber or TaskType"

    @pytest.mark.smoke
    @allure.title("一键过桥下载_下载完成状态机跳转_Download跳转至Update")    
    def test_fota_caseid_1987677(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1200), "Not Enter Bridge Trun Download"   
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50_CDC = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50_CDC['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50_CDC['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50_CDC['data']['serialNumber'] = 2
            Task_Info_Type50_CDC['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50_CDC)
        self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=300)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.READY_TO_INSTALL) 
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.UPDATE.value, 300), "Not Enter Bridge Trun Update"   

    @pytest.mark.full
    @allure.title("一键过桥下载_维持唤醒_不实时监控大电池电量(电量低不影响流程)")    
    def test_fota_caseid_1987683(self):
        self.bus_comm.set_fota_download_wake_condition(display_hv_soc=89, low_volt_soc=90) #not meet HVSOC > 10%
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1200), "Not Enter Bridge Trun Download"   
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50_CDC = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50_CDC['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50_CDC['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50_CDC['data']['serialNumber'] = 2
            Task_Info_Type50_CDC['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50_CDC)
        self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=300)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords=['DownloadBatteryPowerNotKeep',
                                                                                            '"stateCode":"02F7"'], timeout=120):
            self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.DOWNLOAD)     
        assert self.mix.check_fota_keep_awake(pnc29=True,
                                        acu_keep_alive=True,
                                        up_inactive=True,
                                        hv_active=True), "Not Send Awake Signal"
        assert self.mix.check_fota_setStartInhibit(startInhibit=True)
        
    @pytest.mark.full
    @allure.title("一键过桥下载_维持唤醒_不实时监控小电池电量(电量低不影响流程)")    
    def test_fota_caseid_1987682(self):
        self.bus_comm.set_fota_download_wake_condition(display_hv_soc=900, low_volt_soc=69) #not meet low_volt_soc ＜ 70%
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1200), "Not Enter Bridge Trun Download"   
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50_CDC = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50_CDC['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50_CDC['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50_CDC['data']['serialNumber'] = 2
            Task_Info_Type50_CDC['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50_CDC)
        self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=300)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords=['DownloadBatteryPowerNotKeep',
                                                                                            '"stateCode":"02F6"'], timeout=120):
            self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.DOWNLOAD)     
        assert self.mix.check_fota_keep_awake(pnc29=True,
                                        acu_keep_alive=True,
                                        up_inactive=True,
                                        hv_active=True), "Not Send Awake Signal"
        assert self.mix.check_fota_setStartInhibit(startInhibit=True)
        
    @pytest.mark.full
    @allure.title("一键过桥下载_维持唤醒_不实时监控网络(弱网断网不影响流程)")    
    def test_fota_caseid_1987684(self):
        self.bus_comm.set_fota_download_wake_condition(display_hv_soc=900, low_volt_soc=90)
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1200), "Not Enter Bridge Trun Download"   
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50_CDC = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50_CDC['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50_CDC['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50_CDC['data']['serialNumber'] = 2
            Task_Info_Type50_CDC['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50_CDC)
        self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=300)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords=['"stateCode":"02F8"'], timeout=700):
            self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.DOWNLOAD)     
        assert self.mix.check_fota_keep_awake(pnc29=True,
                                        acu_keep_alive=True,
                                        up_inactive=True,
                                        hv_active=True), "Not Send Awake Signal"
        assert self.mix.check_fota_setStartInhibit(startInhibit=True)
        
    @pytest.mark.full
    @allure.title("一键过桥下载_下载中异常_域控DownloadFinalFail")
    def test_fota_caseid_1987678(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1200), "Not Enter Bridge Trun Download"   
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50_CDC = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50_CDC['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50_CDC['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50_CDC['data']['serialNumber'] = 2
            Task_Info_Type50_CDC['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50_CDC)
        self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=300)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"02F4"',
                                                                                   '"stateCode":"03F7"'], timeout=1800):
            self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC,
                                                            UA_Sts.DOWNLOAD,
                                                            ua_download_sts=UA_DownloadStatus.DOWNLOAD_FINAL_FAILED.value,
                                                            errorCode=UA_ErrorCode.DL_HTTPS_TimeoutError_0x02_0x08.value)   
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value and \
               self.soa.get_fota_status(MASTER_EVENT.SerialNumber) == 2 and \
               self.soa.get_fota_status(MASTER_EVENT.TaskType) == FOTA_TaskType.Bridge.value, "Illegal SerialNumber or TaskType"
               
    @pytest.mark.full
    @allure.title("一键过桥下载_维持唤醒_Download超时2H处理")    
    def test_fota_caseid_1987681(self):
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1200), "Not Enter Bridge Trun Download"   
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50_CDC = copy.deepcopy(self.Task_Info_Type50_CDC)
            Task_Info_Type50_CDC['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50_CDC['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50_CDC['data']['serialNumber'] = 2
            Task_Info_Type50_CDC['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50_CDC)
        self.soa.ck_s2s_req_v20("UpdateAgentService_server_CDC_UA_Service", ["StartDownload"], timeout=300)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"03F7"'], timeout=7900): #超时2h
            self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.DOWNLOAD)  
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value and \
               self.soa.get_fota_status(MASTER_EVENT.SerialNumber) == 2 and \
               self.soa.get_fota_status(MASTER_EVENT.TaskType) == FOTA_TaskType.Bridge.value, "Illegal SerialNumber or TaskType"
        
if __name__ == "__main__":
    pass

    




