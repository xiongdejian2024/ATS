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
        self.ssh.update_ua_skip(DOMAIN.BGM, True)
        self.mix.update_version_debug(self.taskid, [DOMAIN.BGM])
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        set_bench_vlan9_ip(self.tc_config['ecu_mock_cfg']['server_ip'])
        self.mix.set_car_mode(car_mode=CarMode.FACTORY)
        self.ssh.copy_factory_packages()
        self.ssh.clear_fota_cache()
        self.sd_tester.reset_bgm()
        self.mix.set_factory_ota_condition(display_hv_soc=250,low_volt_power=11.5,local_diag_sts=DiagActLineSts.DisActive)
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x88, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
                    
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.sd_tester.diag_cancel()
        self.mix.fota_back_to_idle()
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.V2_2_0
    @pytest.mark.full
    @allure.title("V2.2_MCU_ECU_UPDATE&&HV_ECU下高压前_检查Doip ACU CDC连接失败") 
    def test_fota_caseid_1995492(self):
        try:
            self.ssh.type_commands(DeviceName.BGM,'rm -rf /update/skip_debug;sync')
            self.sd_tester.reset_bgm()
            self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x88, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
            self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            with self.log_manage.check_jetlog_by_keywords(log_type=' obt:', keywords='send stack raw data, addr:1001, data::31 01 a1 00 01', timeout=600):#等待进入解密进FOTAMODE
                    pass 
            with self.log_manage.check_jetlog_by_same_keywords(equal=True,log_type='fota: ', keywords=['upgrade_manage => hv_ecu_upgrade',
                                                                                                        'CheckDomainsDoIpConnection:addr:1201',
                                                                                                        'CheckDomainsDoIpConnection:addr:1201',
                                                                                                        'CheckDomainsDoIpConnection:addr:1201',
                                                                                                        'CheckDomainsDoIpConnection:addr:1201',
                                                                                                        'CheckDomainsDoIpConnection:addr:1201',
                                                                                                        'CheckECM3Session:'
                                                                                                        ], timeout=120):
                    pass
        finally:
            self.ssh.update_skip_debug([FOTA_Skip_Debug.cdc_acu_doip_check]) 

    @pytest.mark.V2_2_0
    @pytest.mark.full
    @allure.title("V2.2_MCU_ECU_UPDATE&&HV_ECU 功能寻址1082重启后_检查Doip ACU CDC 连接失败") 
    def test_fota_caseid_1995491(self):
        try:
            self.ssh.type_commands(DeviceName.BGM,'rm -rf /update/skip_debug;sync')
            self.sd_tester.reset_bgm()
            self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x88, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
            self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            with self.log_manage.check_jetlog_by_keywords(log_type=' fota:', keywords=['upgrade_manage => hv_ecu_upgrade',
                                                                                    'GetCanEcuAddr:ConnectivityCANFD'], timeout=600):#等待1082重启
                    pass 
            with self.log_manage.check_jetlog_by_same_keywords(equal=True,log_type='" fota:"', keywords=['CheckDomainsDoIpConnectionCb:result:0,session:1,addr:',
                                                                                                        'CheckDomainsDoIpConnectionCb:result:0,session:1,addr:',
                                                                                                        'CheckDomainsDoIpConnectionCb:result:0,session:1,addr:',
                                                                                                        'CheckDomainsDoIpConnectionCb:result:0,session:1,addr:',
                                                                                                        'CheckDomainsDoIpConnectionCb:result:0,session:1,addr:'
                                                                                                        ], timeout=120):
                    pass
        finally:
            self.ssh.update_skip_debug([FOTA_Skip_Debug.cdc_acu_doip_check])     

    @pytest.mark.V2_2_0
    @pytest.mark.full
    @allure.title("V2.2_MCU_ECU_UPDATE&&HV_ECU Group前_通知CDC门不可用等待10S") 
    def test_fota_caseid_1995493(self):
        self.ssh.update_skip_debug_nokill([FOTA_Skip_Debug.cdc_acu_doip_check]) 
        self.sd_tester.reset_bgm()
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x88, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=' fota:', keywords='DomainsDoIpConnectionStsCb:result:1, is factory ota:1', timeout=600):#等待进入解密进FOTAMODE
                pass
        start_time = time.time()
        logger.info("start_time:{}".format(start_time))
        with self.log_manage.check_jetlog_by_keywords(log_type=' fota:', keywords='CheckECM3Session:', timeout=15):#等待进入解密进FOTAMODE
                pass
        end_time = time.time()
        logger.info("end_time:{}".format(end_time))
        assert start_time - end_time < 11
        logger.info("time:{}".format(start_time - end_time))        

    @allure.title("Group升级前动作_Domain/Domain_ECU_ECM3 否定响应") 
    def test_fota_caseid_1982675(self):
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : {"NRC": 0x11}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='factory_build_task => pre_update', timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_same_keywords(equal=True,log_type='" fota:"', keywords=['31 01 40 00 01',
                                                                                                     '7f 31 11',
                                                                                                    '31 01 40 00 01',
                                                                                                    '7f 31 11',
                                                                                                    '31 01 40 00 01',
                                                                                                    '7f 31 11',
                                                                                                    '31 01 40 00 01',
                                                                                                    '7f 31 11',
                                                                                                    'HighVoltageUpCb: failed to up hv',
                                                                                                    'HvUpResult:skipping to check HV Up result'], timeout=50):
            pass 

    @allure.title("Group升级前动作_Domain/Domain_ECU_ECM3 超时") 
    def test_fota_caseid_1982674(self):
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : {"NRC": "no_reply"}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='factory_build_task => pre_update', timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_same_keywords(equal=True,log_type='" fota:"', keywords=['31 01 40 00 01',
                                                                                                    '31 01 40 00 01',
                                                                                                    '31 01 40 00 01',
                                                                                                    '31 01 40 00 01',
                                                                                                    'HighVoltageUpCb: failed to up hv',
                                                                                                    'HvUpResult:skipping to check HV Up result'], timeout=50):
            pass 

    @allure.title("Group升级前动作_Domain/Domain_ECU_ECM3肯定响应状态错误") 
    def test_fota_caseid_1982673(self):
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : [0x10, 0x02]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='factory_build_task => pre_update', timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_same_keywords(equal=True,log_type='" fota:"', keywords=['31 01 40 00 01',
                                                                                                     '71 01 40 00 10 02',
                                                                                                    '31 01 40 00 01',
                                                                                                    '71 01 40 00 10 02',
                                                                                                    '31 01 40 00 01',
                                                                                                    '71 01 40 00 10 02',
                                                                                                    '31 01 40 00 01',
                                                                                                    '71 01 40 00 10 02',
                                                                                                    'HighVoltageUpCb: failed to up hv',
                                                                                                    'HvUpResult:skipping to check HV Up result'], timeout=50):
            pass 

    @allure.title("Group升级前动作_Bgm_mcu_ECM3 大电池SOC<20%") 
    def test_fota_caseid_1982672(self):
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x22_data(ecu_name="ECM3", did="F186", data_info_update=[0x03])
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x02]}})     
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:pre_update => pkg_decryption', timeout=300):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_same_keywords(equal=True,log_type='" fota:"', keywords=['31 01 42 89 01',
                                                                                                    '31 01 42 89 01',
                                                                                                    '31 01 42 89 01',
                                                                                                    '31 01 42 89 01'], timeout=30):
            pass

    @allure.title("Group升级前动作_Bgm_mcu_ECM3 下高压超时") 
    def test_fota_caseid_1982671(self):
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x22_data(ecu_name="ECM3", did="F186", data_info_update=[0x03])
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x03]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:pre_update => pkg_decryption', timeout=300):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_same_keywords(log_type='" fota:"', keywords=['31 01 42 89 01',
                                                                                        '31 01 42 89 01',
                                                                                        '71 01 42 89 10 03',
                                                                                        '31 01 42 89 01',
                                                                                        '31 01 42 89 01'], timeout=30):
            pass

    @allure.title("Group升级前动作_Bgm_mcu_ECM3 VMM处于Driving") 
    def test_fota_caseid_1982670(self):
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x22_data(ecu_name="ECM3", did="F186", data_info_update=[0x03])
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x04]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:pre_update => pkg_decryption', timeout=300):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_same_keywords(log_type='" fota:"', keywords=['31 01 42 89 01',
                                                                                        '31 01 42 89 01',
                                                                                        '71 01 42 89 10 04',
                                                                                        '31 01 42 89 01',
                                                                                        '31 01 42 89 01'], timeout=30):
            pass

    @allure.title("Group升级前动作_Bgm_mcu_ECM3 处于下高压") 
    def test_fota_caseid_1982669(self):
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x22_data(ecu_name="ECM3", did="F186", data_info_update=[0x03])
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : {"NRC": 0x78}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:pre_update => pkg_decryption', timeout=300):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_same_keywords(log_type='" fota:"', keywords=['31 01 42 89 01',
                                                                                        '31 01 42 89 01',
                                                                                        '31 01 42 89 01',
                                                                                        '31 01 42 89 01'], timeout=50):
            pass

    @allure.title("Group升级前动作_Bgm_mcu_ECM3 否定响应") 
    def test_fota_caseid_1982668(self):
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x22_data(ecu_name="ECM3", did="F186", data_info_update=[0x03])
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : {"NRC": 0x22}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:pre_update => pkg_decryption', timeout=300):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_same_keywords(log_type='" fota:"', keywords=['31 01 42 89 01',
                                                                                        '31 01 42 89 01',
                                                                                        '7f 31 22',
                                                                                        '31 01 42 89 01',
                                                                                        '31 01 42 89 01'], timeout=30):
            pass

    @allure.title("Group升级前动作_Bgm_mcu_ECM3 回复超时") 
    def test_fota_caseid_1982667(self):
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x22_data(ecu_name="ECM3", did="F186", data_info_update=[0x03])
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : {"NRC": "no_reply"}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:pre_update => pkg_decryption', timeout=300):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_same_keywords(log_type='" fota:"', keywords=['31 01 42 89 01',
                                                                                        '31 01 42 89 01',
                                                                                        '31 01 42 89 01',
                                                                                        '31 01 42 89 01'], timeout=40):
            pass


if __name__ == "__main__":
    pass





