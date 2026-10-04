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
                                    FOTA_Skip_Debug.start_download,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ]) 
        self.ssh.update_ua_skip(DOMAIN.BGM, False)
        set_bench_vlan9_ip(self.tc_config['ecu_mock_cfg']['server_ip'])

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])
        self.mix.back_fota_to(FOTAMasteSts.IDLE, self.taskid)
        assert not self.sd_tester.check_mcu_whether_in_boot(), "Case Finish, but MCU still in boot"

    @allure.title("Group升级前动作_Domain/Domain_ECU_ECM3 否定响应（03 0B）") 
    def test_fota_caseid_1982339(self):
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value 
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : [0x10, 0x01]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords='send stack raw data, addr:1630, data::31 01 40 00 01', timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01'], timeout=1200):
            self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : {"NRC": 0x11}}})
         
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"030B"', timeout=600):
             pass 

    @allure.title("Group升级前动作_Domain/Domain_ECU_ECM3 超时(03 0B)") 
    def test_fota_caseid_1982338(self):
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value 
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : [0x10, 0x01]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords='send stack raw data, addr:1630, data::31 01 40 00 01', timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01'], timeout=1200):
            self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : {"NRC": "no_reply"}}})
         
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"030B"', timeout=600):
             pass  

    @allure.title("Group升级前动作_Domain/Domain_ECU_ECM3肯定响应状态错误（03 0B）") 
    def test_fota_caseid_1982337(self):
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value 
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : [0x10, 0x01]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords='send stack raw data, addr:1630, data::31 01 40 00 01', timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01'], timeout=1200):
            self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : [0x10, 0x03]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"030B"', timeout=600):
             pass 

    @allure.title("Group升级前动作_Bgm_mcu_ECM3 大电池SOC<20%(03 09)") 
    def test_fota_caseid_1982334(self):
        self.mix.update_version_debug(self.taskid,["DDM"])
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value 
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x22_data(ecu_name="ECM3", did="F186", data_info_update=[0x03])
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords='send stack raw data, addr:1630, data::31 01 40 00 01', timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords='send stack raw data, addr:1630, data::31 01 42 89 01', timeout=1200):
            self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x02]}})
        # with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0309"', timeout=600):
        #      pass 

    @allure.title("Group升级前动作_Bgm_mcu_ECM3 下高压超时(03 09)") 
    def test_fota_caseid_1982333(self):
        self.mix.update_version_debug(self.taskid,["DDM"])
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value 
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x22_data(ecu_name="ECM3", did="F186", data_info_update=[0x03])
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords='send stack raw data, addr:1630, data::31 01 40 00 01', timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01'], timeout=1200):
            self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x03]}})
         
        # with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0309"', timeout=600):
        #      pass 

    @allure.title("Group升级前动作_Bgm_mcu_ECM3 VMM处于Driving(03 09)") 
    def test_fota_caseid_1982332(self):
        self.mix.update_version_debug(self.taskid,["DDM"])
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value 
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x22_data(ecu_name="ECM3", did="F186", data_info_update=[0x03])
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords='send stack raw data, addr:1630, data::31 01 40 00 01', timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords='send stack raw data, addr:1630, data::31 01 42 89 01', timeout=1200):
            self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : [0x10, 0x04]}})
         
        # with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0309"', timeout=600):
        #      pass

    @allure.title("Group升级前动作_Bgm_mcu_ECM3 处于下高压(03 09)") 
    def test_fota_caseid_1982331(self):
        self.mix.update_version_debug(self.taskid,["DDM"])
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value 
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x22_data(ecu_name="ECM3", did="F186", data_info_update=[0x03])
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords='send stack raw data, addr:1630, data::31 01 40 00 01', timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01'], timeout=1200):
            self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : {"NRC": 0x78}}})
         
        # with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0309"', timeout=600):
        #      pass

    @allure.title("Group升级前动作_Bgm_mcu_ECM3 否定响应(03 09)") 
    def test_fota_caseid_1982330(self):
        self.mix.update_version_debug(self.taskid,["DDM"])
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value 
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x22_data(ecu_name="ECM3", did="F186", data_info_update=[0x03])
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords='send stack raw data, addr:1630, data::31 01 40 00 01', timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01'], timeout=1200):
            self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : {"NRC": 0x11}}})
        # with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0309"', timeout=600):
        #      pass
        
    @allure.title("Group升级前动作_Bgm_mcu_ECM3 回复超时(03 09)") 
    def test_fota_caseid_1982329(self):
        self.mix.update_version_debug(self.taskid,["DDM"])
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value 
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x22_data(ecu_name="ECM3", did="F186", data_info_update=[0x01])
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords='send stack raw data, addr:1630, data::31 01 40 00 01', timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01'], timeout=1200):
            self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : {"NRC": "no_reply"}}})
        # with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0309"', timeout=600):
        #     pass
                  
        
        
        
        
        
        


