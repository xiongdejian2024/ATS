import os
import sys
import pytest
import allure
import copy

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_fota_bridge import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.common import set_bench_vlan9_ip

@pytest.mark.ecu_mock
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
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.update_precondition_check,
                                    FOTA_Skip_Debug.car_mode_normal
                                    ])
        set_bench_vlan9_ip(self.tc_config['ecu_mock_cfg']['server_ip'])
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
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : [0x10, 0x01]}})
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=20)
        assert self.soa.get_fota_status(MASTER_EVENT.TaskType) == 2
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.mix.fota_back_to_idle()
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        
    @pytest.mark.fota
    @allure.title("OTA mode及升级开始流程_ECM3 下高压失败_下高压超时 (03 09)")    
    def test_fota_caseid_1987656(self):
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1800), "Not Enter Bridge Trun Download"
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x03]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50['data']['serialNumber'] = 2
            Task_Info_Type50['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.DOWNLOADING.value, 300), "Not Trun to DOWNLOADING"        
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.UPDATE.value, 300), "Fail Trun to UPDATE"
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01'], timeout=1200):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0309"', timeout=600):
            pass  
        
    @allure.title("OTA mode及升级开始流程_ECM3 下高压失败_VMM处于driving (03 09)") 
    def test_fota_caseid_1987655(self):
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1800), "Not Enter Bridge Trun Download"
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x04]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50['data']['serialNumber'] = 2
            Task_Info_Type50['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.DOWNLOADING.value, 300), "Not Trun to DOWNLOADING"        
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.UPDATE.value, 300), "Fail Trun to UPDATE"
        with self.log_manage.check_jetlog_by_keywords(log_type='-E " fota:| obt:"', keywords=['send stack raw data, addr:1630, data::31 01 42 89 01', '"stateCode":"0309"'], timeout=1200):
            pass

    @allure.title("OTA mode及升级开始流程_ECM3 下高压失败_回复否定响应 (03 09)") 
    def test_fota_caseid_1987657(self):
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1800), "Not Enter Bridge Trun Download"
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : {"NRC": 0x11}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50['data']['serialNumber'] = 2
            Task_Info_Type50['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.DOWNLOADING.value, 300), "Not Trun to DOWNLOADING"        
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.UPDATE.value, 300), "Fail Trun to UPDATE"
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01'], timeout=1200):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0309"', timeout=600):
            pass
        
    @allure.title("FOTA解密过程_ECM3无法上高压_否定响应 (03 0B)") 
    def test_fota_caseid_1987654(self):
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1800), "Not Enter Bridge Trun Download"
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : {"NRC": 0x11}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50['data']['serialNumber'] = 2
            Task_Info_Type50['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.DOWNLOADING.value, 300), "Not Trun to DOWNLOADING"        
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.UPDATE.value, 300), "Fail Trun to UPDATE"
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01'], timeout=1200):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"030B"', timeout=600):
            pass
        
    @allure.title("FOTA解密过程_ECM3无法上高压_回复超时 (03 0B)") 
    def test_fota_caseid_1987653(self):
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1800), "Not Enter Bridge Trun Download"
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : {"NRC": "no_reply"}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50['data']['serialNumber'] = 2
            Task_Info_Type50['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.DOWNLOADING.value, 300), "Not Trun to DOWNLOADING"        
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.UPDATE.value, 300), "Fail Trun to UPDATE"
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01'], timeout=1200):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"030B"', timeout=600):
            pass

    @allure.title("一键过桥_ECM3 下高压失败_回复超时 (03 09)")    
    def test_fota_caseid_1987658(self):
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1800), "Not Enter Bridge Trun Download"
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : {"NRC": "no_reply"}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50['data']['serialNumber'] = 2
            Task_Info_Type50['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.DOWNLOADING.value, 300), "Not Trun to DOWNLOADING"        
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.UPDATE.value, 300), "Fail Trun to UPDATE"
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01'], timeout=1200):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0309"', timeout=600):
            pass

    @allure.title("一键过桥_ECM3 下高压失败_处于下高压过程中 (03 09)") 
    def test_fota_caseid_1987659(self):
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1800), "Not Enter Bridge Trun Download"
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x78]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50['data']['serialNumber'] = 2
            Task_Info_Type50['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.DOWNLOADING.value, 300), "Not Trun to DOWNLOADING"        
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.UPDATE.value, 300), "Fail Trun to UPDATE"
        with self.log_manage.check_jetlog_by_keywords(log_type='-E " fota:| obt:"', keywords=['send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                              'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                              'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                              'send stack raw data, addr:1630, data::31 01 42 89 01', 
                                                                                              '"stateCode":"0309"'], timeout=1200):
            pass

    @allure.title("一键过桥_ECM3 下高压失败_大电池SoC < 20% (03 09)") 
    def test_fota_caseid_1987660(self):
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 1800), "Not Enter Bridge Trun Download"
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x02]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="collect_version => wait_task_info", timeout=300):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50['data']['serialNumber'] = 2
            Task_Info_Type50['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.DOWNLOADING.value, 300), "Not Trun to DOWNLOADING"        
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.UPDATE.value, 300), "Fail Trun to UPDATE"
        with self.log_manage.check_jetlog_by_keywords(log_type='-E " fota:| obt:"', keywords=['send stack raw data, addr:1630, data::31 01 42 89 01', '"stateCode":"0309"'], timeout=1200):
            pass

@pytest.mark.ecu_mock
@pytest.mark.V_2_0
@allure.feature("基础架构")
@allure.story("FOTA")
class TestFotaMode(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("AcuModeManagerService","server"),
                         ("V2TRoutingForwarder","client","V2TOTAFotaForwarder")])
        self.ssh.update_skip_debug([FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.update_precondition_check,
                                    FOTA_Skip_Debug.car_mode_normal
                                    ])
        
        set_bench_vlan9_ip(self.tc_config['ecu_mock_cfg']['server_ip'])
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
        self.diag_mock.doip_sim_start()
        self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x10, 0x01]}})
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=30)
        assert self.soa.get_fota_status(MASTER_EVENT.TaskType) == 2
        
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.mix.fota_back_to_idle()
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        
    @pytest.mark.fota
    @allure.title("一键过桥_进入FOTA mode失败_回复超时 (03 08)") 
    def test_fota_caseid_1987662(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:exit_ota => success', timeout=1200):
            pass
        self.diag_mock.doip_sim_start()
        self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x10, 0x01]}})
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 800), "Not Enter Bridge Trun Download"
        with self.log_manage.check_jetlog_by_same_keywords(log_type='-E "fota: | obt:"', keywords=['send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   '"stateCode":"0308"'
                                                                                   ], timeout=180):
            self.diag_mock.doip_sim_start()
            self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : {"NRC": "no_reply"}}})

    @allure.title("一键过桥_进入FOTA mode失败_回复NRC (03 08)") 
    def test_fota_caseid_1987661(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:exit_ota => success', timeout=1200):
            pass
        self.diag_mock.doip_sim_start()
        self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x10, 0x01]}})
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 800), "Not Enter Bridge Trun Download"
        with self.log_manage.check_jetlog_by_same_keywords(log_type='-E "fota: | obt:"', keywords=['send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   '"stateCode":"0308"'
                                                                                   ], timeout=180):
            self.diag_mock.doip_sim_start()
            self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : {"NRC": 0x11}}})

    @allure.title("一键过桥_进入FOTA mode失败_肯定响应状态error (03 08)") 
    def test_fota_caseid_1987663(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:exit_ota => success', timeout=1200):
            pass
        self.diag_mock.doip_sim_start()
        self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x10, 0x01]}})
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 800), "Not Enter Bridge Trun Download"
        with self.log_manage.check_jetlog_by_same_keywords(log_type='-E "fota: | obt:"', keywords=['send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   '"stateCode":"0308"'
                                                                                   ], timeout=180):
            self.diag_mock.doip_sim_start()
            self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x20, 0xff]}})

               
if __name__ == "__main__":
    pass


    




