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

@pytest.mark.V_2_0
@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("AcuModeManagerService","server"),
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
                                    FOTA_Skip_Debug.CDC_UA,
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
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.mix.fota_back_to_idle()
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.full
    @allure.title("一键过桥_解密阶段_小ECU解密错误_030F_Decryption_Error")    
    def test_fota_caseid_1987647(self):
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1200), "Not Enter Bridge Trun Download"   
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50_NKR = copy.deepcopy(self.Task_Info_Type50_NKR)
            Task_Info_Type50_NKR['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50_NKR['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50_NKR['data']['serialNumber'] = 2
            Task_Info_Type50_NKR['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50_NKR)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.UPDATE.value, 300), "Not Enter Bridge Trun UPDATE"   
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"030F"', # Decryption_Error
                                                                                   '"stateCode":"03F7"'], timeout=300):
            assert self.ssh.check_file_existence(DeviceName.BGM, path="/update/fota", filename="*.bin")
            self.ssh.type_commands(DeviceName.BGM, "rm -rf /update/fota/*;sync")  
            assert not self.ssh.check_file_existence(DeviceName.BGM, path="/update/fota", filename="*.bin")
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value and \
               self.soa.get_fota_status(MASTER_EVENT.SerialNumber) == 2 and \
               self.soa.get_fota_status(MASTER_EVENT.TaskType) == FOTA_TaskType.Bridge.value, "Illegal SerialNumber or TaskType"
        self.mix.update_version_debug_bridge(task_id=self.taskid)

    @pytest.mark.full
    @allure.title("一键过桥_解密阶段_域控解密版本错误_030F_Decryption_Error")    
    def test_fota_caseid_1987648(self):
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1800), "Not Enter Bridge Trun Download"  
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50['data']['serialNumber'] = 2
            Task_Info_Type50['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50) 
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.UPDATE.value, 300), "Not Enter Bridge Trun UPDATE"   
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"030F"', # Decryption_Error
                                                                                   '"stateCode":"0330"'], timeout=300):
            self.ssh.rm_ua_packages(DOMAIN.BGM)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.FAILED_NOT_DRIVING.value, 300)
        assert self.soa.get_fota_status(MASTER_EVENT.SerialNumber) == 2 and \
               self.soa.get_fota_status(MASTER_EVENT.TaskType) == FOTA_TaskType.Bridge.value, "Illegal SerialNumber or TaskType"

if __name__ == "__main__":
    pass

    




