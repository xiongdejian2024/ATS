import os
import sys
import pytest
import allure
import yaml
import json
from time import sleep

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
        self.ssh.update_skip_debug([
                                    FOTA_Skip_Debug.cdc_acu_doip_check
                                    ]) 
        set_bench_vlan9_ip(self.tc_config['ecu_mock_cfg']['server_ip'])
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.fota_back_to_idle()
        self.io.bgm_diag_line_down()
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_TASK)
        self.mix.set_factory_ota_condition(display_hv_soc=250,low_volt_power=11.5,local_diag_sts=DiagActLineSts.DisActive)
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x88, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @allure.title("FOTA解密过程_ECM3无法上高压_否定响应") 
    def test_fota_caseid_1982680(self):
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : {"NRC": 0x11}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:factory_build_task => pre_update', timeout=300):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)  
        with self.log_manage.check_jetlog_by_same_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01'], timeout=60):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords='send stack raw data, addr:1630, data::22 f1 86', timeout=60):
            pass

    @allure.title("FOTA解密过程_ECM3无法上高压_回复超时") 
    def test_fota_caseid_1982679(self):
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : {"NRC": "no_reply"}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:factory_build_task => pre_update', timeout=300):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)  
        with self.log_manage.check_jetlog_by_same_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01'], timeout=45):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords='send stack raw data, addr:1630, data::22 f1 86', timeout=60):
            pass

    @allure.title("FOTA解密过程_VBF 验签错误") 
    def test_fota_caseid_1982677(self):
        with open('config/ota_mapping.yaml', 'r') as f:
            mapping = yaml.safe_load(f)
        mapping["ecu"][1]["packages"][0]["sblPkg"][0]["signature"] = "===========================================abc================================================="
        mapping["ecu"][1]["packages"][0]["sblPkg"][0]["keyinfo"] = "===========================================abc================================================="
        mapping = json.dumps(mapping).replace('{', '{ ').replace('}', ' }').replace('"', '\\"')
        self.ssh.type_commands(DeviceName.BGM, f'echo -n "{mapping}" > /update/factory/mapping.json')
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=["Decrypt:ecu decrypt file failed:/update/factory/1160210060AB.bin",
                                                                                   "DecryptPackage:decrypt sbl file failed!"], timeout=600):
            pass
        self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.FACTORY_FAILED.value, 1500)
        assert "'ecuName': 'DDM', 'errorCode': 4" in str(self.soa.get_fota_UpdateErrorInfo())

    @allure.title("FOTA解密过程_ VBF 格式错误") 
    def test_fota_caseid_1982678(self):
        self.ssh.type_commands(DeviceName.BGM, 'mv /update/factory/1160210060AB.bin /update/factory/1160210060AB.txt;sync')
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="DecryptPackage:decrypt sbl file failed!", timeout=600):
            pass
        self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.FACTORY_FAILED.value, 1500)
        assert "'ecuName': 'DDM', 'errorCode': 4" in str(self.soa.get_fota_UpdateErrorInfo())

    @allure.title("FOTA解密过程_VBF 版本错误") 
    def test_fota_caseid_1982676(self):
        self.ssh.type_commands(DeviceName.BGM, 'mv /update/factory/1160210060AB.bin /update/factory/1160210110AB.bin;sync')
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="DecryptPackage:decrypt sbl file failed!", timeout=600):
            pass
        self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.FACTORY_FAILED.value, 1500)
        assert "'ecuName': 'DDM', 'errorCode': 4" in str(self.soa.get_fota_UpdateErrorInfo())

if __name__ == "__main__":
    pass


    




