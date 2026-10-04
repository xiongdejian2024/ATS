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
        self.mix.update_version_debug(self.taskid, ["DDM"])
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        set_bench_vlan9_ip(self.tc_config['ecu_mock_cfg']['server_ip'])
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update={"NRC": 0x22})
        self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
        self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])
        self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={})
        self.diag_mock.update_0x37_data(ecu_name="DDM", data={})
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0212": { 1 : [0x10, 0x00]}})
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0301": { 1 : [0x10]}})
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"FF00": { 1 : [0x10]}})
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0205": { 1 : [0x10, 0x00, 0x00, 0x00, 0x00]}})
                    
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @allure.title("升级成功退出_软硬件读取不回应（032A）") 
    def test_fota_caseid_1983078(self):
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
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:exit_ota => success', timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x88, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update={"NRC": "no_reply"})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"032A"'], timeout=600):
            pass
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FAILED_NOT_DRIVING.value, timeout=600)

    @allure.title("升级成功退出_软硬件读取回复否定响应（032A）") 
    def test_fota_caseid_1983077(self):
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
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:exit_ota => success', timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x88, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update={"NRC": 0x11})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"032A"'], timeout=600):
            pass
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FAILED_NOT_DRIVING.value, timeout=600)

    @allure.title("升级成功退出_软硬件读取不对应（032A）") 
    def test_fota_caseid_1983076(self):
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
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE,taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:exit_ota => success', timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x88, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update=[0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x42])
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"032A"'], timeout=600):
            pass
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FAILED_NOT_DRIVING.value, timeout=600)

    @allure.title("升级成功退出_退出FOTA mode失败_回复超时（0329）") 
    def test_fota_caseid_1983075(self):
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
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1401, data::31 01 a1 00 02',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 02',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 02',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 02'
                                                                                   ], timeout=300):
            self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : {"NRC": "no_reply"}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0329"'], timeout=120):
            pass
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FAILED_NOT_DRIVING.value, timeout=600)
    
    @allure.title("升级成功退出_退出FOTA mode失败_回复负响应（0329）") 
    def test_fota_caseid_1983074(self):
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
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1401, data::31 01 a1 00 02',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 02',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 02',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 02'
                                                                                   ], timeout=300):
            self.diag_mock.doip_sim_start()
            self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : {"NRC": 0x11}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0329"'], timeout=120):
            pass
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FAILED_NOT_DRIVING.value, timeout=600)

    @allure.title("升级成功退出_退出FOTA mode失败_回复正相应错误状态（0329）") 
    def test_fota_caseid_1983073(self):
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
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1401, data::31 01 a1 00 02',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 02',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 02',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 02'
                                                                                   ], timeout=300):
            self.diag_mock.doip_sim_start()
            self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x20, 0xff]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0329"'], timeout=120):
            pass
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FAILED_NOT_DRIVING.value, timeout=600)

    @allure.title("升级成功退出_退出FOTA mode失败_ECM回复超时（0329）") 
    def test_fota_caseid_1983072(self):
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
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:exit_ota => success', timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1401, data::31 01 a1 00 02',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 02',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 02',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 02'
                                                                                   ], timeout=300):
            self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : {"NRC": "no_reply"}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0329"'], timeout=120):
            pass
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FAILED_NOT_DRIVING.value, timeout=600)

    @allure.title("升级成功退出_退出FOTA mode失败_ECM回复负响应（0329）") 
    def test_fota_caseid_1983071(self):
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
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:exit_ota => success', timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1401, data::31 01 a1 00 02',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 02',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 02',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 02'
                                                                                   ], timeout=300):
            self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : {"NRC": 0x11}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0329"'], timeout=120):
            pass
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FAILED_NOT_DRIVING.value, timeout=600)

if __name__ == "__main__":
    pass

    




