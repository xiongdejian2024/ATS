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
        self.ssh.update_skip_debug([
                                    FOTA_Skip_Debug.cdc_acu_doip_check
                                    ]) 
        self.ssh.update_ua_skip(DOMAIN.BGM, False)
        set_bench_vlan9_ip(self.tc_config['ecu_mock_cfg']['server_ip'])
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        self.mix.set_car_mode(car_mode=CarMode.FACTORY)
        self.ssh.copy_factory_packages()
        self.ssh.clear_fota_cache()
        self.sd_tester.reset_bgm()
        self.mix.set_factory_ota_condition(display_hv_soc=250,low_volt_power=11.5,local_diag_sts=DiagActLineSts.DisActive)
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x88, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.io.tcam_power_on()
        self.ssh.clear_fota_cache()
        self.mix.fota_back_to_idle()
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.mix.fota_back_to_idle()
        assert self.soa.get_fota_status(master_event_field=MASTER_EVENT.Status) == 0
        self.io.tcam_power_on()

    @pytest.mark.V_2_2	
    @pytest.mark.full     
    @allure.title("V2.2_Pre_Update检查Doip ACU/CDC 连接失败") 
    def test_fota_caseid_1995498(self):
        try:    
            self.ssh.type_commands(DeviceName.BGM, 'rm -rf /update/skip_debug;sync')
            self.sd_tester.reset_bgm()
            with self.log_manage.check_jetlog_by_keywords(log_type=' fota: ', keywords='ChangeState:factory_build_task => pre_update', timeout=400):
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            with self.log_manage.check_jetlog_by_same_keywords(equal=True,log_type='-E "fota: | obt:"', keywords=['CheckDomainsDoIpConnectionCb:result:0,session:1,addr:',
                                                                                                                'CheckDomainsDoIpConnectionCb:result:0,session:1,addr:',
                                                                                                                'CheckDomainsDoIpConnectionCb:result:0,session:1,addr:',
                                                                                                                'CheckDomainsDoIpConnectionCb:result:0,session:1,addr:',#220AG版本还是超时，需优化至4次 待版本合入
                                                                                                                'send stack raw data, addr:1001, data::31 01 a1 00 01'
                                                                                                                ], timeout=80):
                pass
        finally:
            self.ssh.update_skip_debug([FOTA_Skip_Debug.cdc_acu_doip_check])    
            
    # @pytest.mark.V_2_2	
    @pytest.mark.full
    @allure.title("V2.2_Pre_Update检查Doip TCAM连接失败") 
    def test_fota_caseid_1995497(self):
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=' fota: ', keywords='CheckDomainsDoIpConnection:addr:1011', timeout=400):
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        self.io.tcam_power_off()
        with self.log_manage.check_jetlog_by_keywords(log_type=' fota: ', keywords='factory_build_task => pre_update', timeout=400):
            pass
        with self.log_manage.check_jetlog_by_same_keywords(equal=True,log_type='-E "fota: | obt:"', keywords=['CheckDomainsDoIpConnectionCb:result:0,session:1,addr:1011',
                                                                                                            'CheckDomainsDoIpConnectionCb:result:0,session:1,addr:1011',
                                                                                                            'CheckDomainsDoIpConnectionCb:result:0,session:1,addr:1011',
                                                                                                            'CheckDomainsDoIpConnectionCb:result:0,session:1,addr:1011',
                                                                                                            'send stack raw data, addr:1001, data::31 01 a1 00 01'
                                                                                                            ], timeout=75):
            pass

    @pytest.mark.V_2_2	
    @pytest.mark.full     
    @allure.title("V2.2_Pre_Update 进FOTA MODE_ACU进入FOTAMODE失败") 
    def test_fota_caseid_1995496(self):
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        sleep(90) #等待版本收集完成
        with self.log_manage.check_jetlog_by_same_keywords(equal=True,log_type='-E "fota: | obt:"', keywords=['send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                                            'send stack raw data, addr:1401, data::31 01 a1 00 01',             
                                                                                                            'send stack raw data, addr:1002, data::2e f1 53 04'
                                                                                                            ], timeout=60):
            pass

    @pytest.mark.V_2_2	
    @pytest.mark.full     
    @allure.title("V2.2_Pre_Update 进FOTA MODE_CDC进入FOTAMODE失败") 
    def test_fota_caseid_1995495(self):
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        sleep(90) #等待版本收集完成
        with self.log_manage.check_jetlog_by_same_keywords(equal=True,log_type='-E "fota: | obt:"', keywords=['send stack raw data, addr:1201, data::31 01 a1 00 01',
                                                                                                            'send stack raw data, addr:1201, data::31 01 a1 00 01',             
                                                                                                            'send stack raw data, addr:1002, data::2e f1 53 04'
                                                                                                            ], timeout=60):
            pass
 
    @pytest.mark.V_2_2	
    @pytest.mark.full     
    @allure.title("V2.2_Pre_Update 进FOTA MODE_TCAM进入FOTAMODE失败") 
    def test_fota_caseid_1995494(self):
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        sleep(90) #等待版本收集完成
        self.io.tcam_power_off()
        with self.log_manage.check_jetlog_by_same_keywords(equal=True,log_type='-E "fota: | obt:"', keywords=['send stack raw data, addr:1011, data::31 01 a1 00 01',
                                                                                                            'send stack raw data, addr:1011, data::31 01 a1 00 01',             
                                                                                                            'send stack raw data, addr:1002, data::2e f1 53 04'
                                                                                                            ], timeout=100):
            pass
        
    @allure.title("OTA mode及升级开始流程_进入FOTA mode失败_回复超时") 
    def test_fota_caseid_1982687(self):
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        sleep(120) #等待版本收集完成
        with self.log_manage.check_jetlog_by_same_keywords(log_type='-E "fota: | obt:"', keywords=['send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'ChangeState:pre_update => pkg_decryption'
                                                                                   ], timeout=90):
            self.diag_mock.doip_sim_start()
            self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : {"NRC": "no_reply"}}})

    @allure.title("OTA mode及升级开始流程_进入FOTA mode失败_回复NRC") 
    def test_fota_caseid_1982689(self):
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        sleep(120) #等待版本收集完成
        with self.log_manage.check_jetlog_by_same_keywords(log_type='-E "fota: | obt:"', keywords=['send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'ChangeState:pre_update => pkg_decryption'
                                                                                   ], timeout=90):
            self.diag_mock.doip_sim_start()
            self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : {"NRC": 0x11}}})

    @allure.title("OTA mode及升级开始流程_进入FOTA mode失败_肯定响应状态error") 
    def test_fota_caseid_1982688(self):
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        sleep(120) #等待版本收集完成
        with self.log_manage.check_jetlog_by_same_keywords(log_type='-E "fota: | obt:"', keywords=['send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'ChangeState:pre_update => pkg_decryption'
                                                                                   ], timeout=90):
            self.diag_mock.doip_sim_start()
            self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x20, 0xff]}})

    @allure.title("OTA mode及升级开始流程_ECM3 下高压失败_大电池SoC < 20%") 
    def test_fota_caseid_1982686(self):
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x02]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:factory_build_task => pre_update', timeout=600):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        self.diag_mock.doip_sim_start()
        self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x10, 0x00]}})
        with self.log_manage.check_jetlog_by_same_keywords(log_type='-E "fota: | obt:"', keywords=['send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                                'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                                'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                                'send stack raw data, addr:1630, data::31 01 42 89 01'], timeout=65):
            pass     

    @allure.title("OTA mode及升级开始流程_ECM3 下高压失败_下高压超时") 
    def test_fota_caseid_1982685(self):
        self.diag_mock.doip_sim_start()
        self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x10, 0x00]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x03]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:factory_build_task => pre_update', timeout=600):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_same_keywords(log_type='-E "fota: | obt:"', keywords=['send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                                'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                                'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                                'send stack raw data, addr:1630, data::31 01 42 89 01'], timeout=50):
            pass     

    @allure.title("OTA mode及升级开始流程_ECM3 下高压失败_VMM处于driving") 
    def test_fota_caseid_1982684(self):
        self.diag_mock.doip_sim_start()
        self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x10, 0x00]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x04]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:factory_build_task => pre_update', timeout=600):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_same_keywords(log_type='-E "fota: | obt:"', keywords=['send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                                'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                                'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                                'send stack raw data, addr:1630, data::31 01 42 89 01'], timeout=65):
            pass   

    @allure.title("OTA mode及升级开始流程_ECM3 下高压失败_处于下高压过程中") 
    def test_fota_caseid_1982683(self):
        self.diag_mock.doip_sim_start()
        self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x10, 0x00]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x78]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:factory_build_task => pre_update', timeout=600):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_same_keywords(log_type='-E "fota: | obt:"', keywords=['send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                                'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                                'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                                'send stack raw data, addr:1630, data::31 01 42 89 01'], timeout=50):
            pass  

    @allure.title("OTA mode及升级开始流程_ECM3 下高压失败_回复否定响应") 
    def test_fota_caseid_1982682(self):
        self.diag_mock.doip_sim_start()
        self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x10, 0x00]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : {"NRC": 0x11}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:factory_build_task => pre_update', timeout=600):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_same_keywords(log_type='-E "fota: | obt:"', keywords=['send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                                'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                                'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                                'send stack raw data, addr:1630, data::31 01 42 89 01'], timeout=50):
            pass  

    @allure.title("OTA mode及升级开始流程_ECM3 下高压失败_回复超时") 
    def test_fota_caseid_1982681(self):
        self.diag_mock.doip_sim_start()
        self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x10, 0x00]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : {"NRC": "no_reply"}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:factory_build_task => pre_update', timeout=600):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_same_keywords(log_type='-E "fota: | obt:"', keywords=['send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                                'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                                'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                                'send stack raw data, addr:1630, data::31 01 42 89 01'], timeout=50):
            pass  
if __name__ == "__main__":
    pass

    




