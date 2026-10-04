import os
import sys
import pytest
import allure

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
        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                                    FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ]) 
        self.ssh.update_ua_skip(DOMAIN.BGM, False)
        self.mix.update_version_debug(self.taskid,["DDM"])
        set_bench_vlan9_ip(self.tc_config['ecu_mock_cfg']['server_ip'])

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.mix.back_fota_to(FOTAMasteSts.IDLE, self.taskid)
        assert not self.sd_tester.check_mcu_whether_in_boot(), "Case Finish, but MCU still in boot"

    @allure.title("FOTA解密过程_ECM3无法上高压_否定响应 (03 0B)") 
    def test_fota_caseid_1982349(self):
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value 
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : {"NRC": 0x11}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01'], timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"030B"', timeout=600):
             pass


