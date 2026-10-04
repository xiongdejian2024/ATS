import os
import sys
import pytest
import allure
import yaml
import json

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.common.common import set_bench_vlan9_ip


@pytest.mark.ecu_mock
@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service")])
        self.ssh.update_ua_skip(DOMAIN.BGM, False)
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        set_bench_vlan9_ip(self.tc_config['ecu_mock_cfg']['server_ip'])
        self.mix.update_version_debug(self.taskid,["DDM"])

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.mix.back_fota_to(FOTAMasteSts.IDLE,taskid=self.taskid)
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM]) 
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @allure.title("上传云端_CanNot Get into FOTAMode(0308)") 
    def test_fota_caseid_1983122(self):
        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                                    FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.before_group_hv_ctl,
                                    FOTA_Skip_Debug.ecm3_down_hv,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ]) 
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0308"'], timeout=300):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

    @allure.title("上传云端_CanNot ShutDown HV(0309)") 
    def test_fota_caseid_1983121(self):
        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                                    FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.before_group_hv_ctl,
                                    FOTA_Skip_Debug.ecm3_down_hv,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ]) 
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0309"'], timeout=300):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

    @allure.title("上传云端_ECU_CANNOT_Leave_FOTAMode(0329)") 
    def test_fota_caseid_1983094(self):
        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                            FOTA_Skip_Debug.baseline,
                            FOTA_Skip_Debug.before_group_1081,
                            FOTA_Skip_Debug.before_group_hv_ctl,
                            FOTA_Skip_Debug.ecm3_down_hv,
                            FOTA_Skip_Debug.fota_mode_requeset_cdc,
                            FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                            FOTA_Skip_Debug.upload_version_from_debug_file,
                            FOTA_Skip_Debug.CDC_UA,
                            FOTA_Skip_Debug.ACU_UA,
                            FOTA_Skip_Debug.version_collect,
                            FOTA_Skip_Debug.cdc_acu_doip_check,
                            FOTA_Skip_Debug.update_precondition_check
                            ]) 
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
        self.diag_mock.doip_sim_start()
        self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x10, 0x00]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:exit_ota => success', timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0329"'], timeout=300):
            pass

    @allure.title("上传云端_ECU_PN_IsNotMatch(032A)") 
    def test_fota_caseid_1983092(self):
        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                                    FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.before_group_hv_ctl,
                                    FOTA_Skip_Debug.ecm3_down_hv,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ]) 
        with open('config/UA_conf.yaml', 'r') as f:
            data = yaml.safe_load(f)
        version_debug = data['Version_Debug_BGM']
        version_debug["data"]["taskId"] = self.taskid
        version_debug["data"]["ecu"][0]["HWPN"] = "8895036214  I"
        config_json = json.dumps(version_debug).replace('{', '{ ').replace('}', ' }').replace('"', '\\"')
        self.ssh.type_commands(DeviceName.BGM, f'echo -n "{config_json}" > /update/version_debug.json')
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:exit_ota => success', timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"032A"'], timeout=300):
            pass

if __name__ == "__main__":
    pass

    




