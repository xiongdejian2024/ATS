import os
import sys
import pytest
import allure
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
        self.ssh.update_ua_skip(DOMAIN.BGM, True)
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        set_bench_vlan9_ip(self.tc_config['ecu_mock_cfg']['server_ip'])
        self.mix.set_car_mode(car_mode=CarMode.FACTORY)
        self.ssh.copy_factory_packages()
        self.ssh.clear_fota_cache()
        self.sd_tester.reset_bgm()
        self.mix.set_factory_ota_condition(display_hv_soc=250,low_volt_power=11.5,local_diag_sts=DiagActLineSts.DisActive)
        self.bus_comm.filter_msg_all()
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x88, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update=[0x02, 0x61, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41, 0x12, 0x50, 0x91, 0x00, 0x55, 0x20, 0x41, 0x41])
                    
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.sd_tester.diag_cancel()
        sleep(60) # 等待厂内OTA升级结束
        self.bus_comm.filter_msg_all()
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    def get_f1aa_data_info(self, swpn):
        pairs = zip(*[iter(swpn[:-2])]*2)
        hex_pairs = [('0x' + ''.join(pair)) for pair in pairs]
        new_s = ' ' + swpn[-2:]
        ascii_codes = [hex(ord(c)) for c in new_s]
        res = hex_pairs + ascii_codes
        ver = [int(s, 16) for s in res]
        return ver

    @allure.title("FOTA升级结束_版本校验_读取硬件号失败") 
    def test_fota_caseid_1982642(self):
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
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords="send stack raw data, addr:1a12, data::31 01 02 05", timeout=1000):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="compareEcusVersion:real ecu info, ecu name:DDM ,ecu id:6021, hwpn: ,", timeout=1000):
            self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update={"NRC": 0x22})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="name:DDM , err code:5 ,", timeout=300): 
            pass
        self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FACTORY_FAILED.value, timeout=300)

    @allure.title("FOTA升级结束_版本校验_读取软件号失败") 
    def test_fota_caseid_1982641(self):
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
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords="send stack raw data, addr:1a12, data::31 01 02 05", timeout=1000):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="compareEcusVersion:real ecu info, ecu name:DDM ,ecu id:6021, hwpn:8892362682  A ,swpn:", timeout=1000):
            self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update={"NRC": 0x22})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="name:DDM , err code:5 ,", timeout=300): 
            pass
        self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FACTORY_FAILED.value, timeout=300)

    @allure.title("FOTA升级结束_版本校验_软件硬件号匹配成功") 
    def test_fota_caseid_1982640(self):
        self.mix.set_car_mode(car_mode=CarMode.FACTORY)
        self.ssh.type_commands(DeviceName.BGM, "cp /data/DDM_bak/* /update/factory/;sync")
        self.ssh.clear_fota_cache()
        self.sd_tester.reset_bgm()
        self.mix.set_factory_ota_condition(display_hv_soc=250,low_volt_power=11.5,local_diag_sts=DiagActLineSts.DisActive)
        mapping = self.ssh.type_commands(DeviceName.BGM, "cat /data/vehicleInfo.json")
        mapping = mapping.replace('\n', '') + '}'  # type_commands函数cat /data/vehicleInfo.json读取结果不完整，会少一个闭合的花括号}
        mapping_dict = json.loads(mapping)
        mapping_dict['F150'] = []
        mapping_dict['F151'] = []
        mapping_json = json.dumps(mapping_dict, indent=2)
        self.ssh.type_commands(DeviceName.BGM, f'echo -n "{mapping_json}" > /update/version_debug.json')
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
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        sleep(10)
        jet_log_bgm = self.ssh.type_commands(DeviceName.BGM,
                                    "/app/bin/zstdcat /log/jetlog_messages |grep ' fota:'")
        logger.info(jet_log_bgm)
        baseLineVer, displayVersion = re.findall(r'parseFactoryTaskInfo: baseline:(.*?)\n.*?parseFactoryTaskInfo: display baseline:(.*?)\n', jet_log_bgm, re.S)[0]
        logger.info(f'当前厂内OTA升级包baseLineVer：{baseLineVer}，displayVersion：{displayVersion}' )
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="ChangeState:exit_ota => factory_exit_ota", timeout=1400):
            pass   
        fire_name = self.ssh.type_commands(DeviceName.BGM, 'find /data/DDM_bak/ -type f -name "616021*.bin" -exec basename {} \\;')
        swpn = fire_name.split('.')[0]
        app_ver = self.get_f1aa_data_info(swpn)
        fire_name = self.ssh.type_commands(DeviceName.BGM, 'find /data/DDM_bak/ -type f -name "126021*.bin" -exec basename {} \\;')
        swpn = fire_name.split('.')[0]
        sbl_ver = self.get_f1aa_data_info(swpn)
        new_rsp = app_ver+sbl_ver
        new_rsp.insert(0, 2)
        logger.info(new_rsp)
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AA", data_info_update=[0x88, 0x92, 0x36, 0x26, 0x82, 0x20, 0x20, 0x41])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F1AE", data_info_update=new_rsp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="ChangeState:factory_exit_ota => factory_ota_finish", timeout=300):
            pass
        res = self.ssh.type_commands(DeviceName.BGM, "cat /data/vehicleInfo.json")
        res = res.replace('\n', '') + '}'  # type_commands函数cat /data/vehicleInfo.json读取结果不完整，会少一个闭合的花括号}
        mapping_new = json.loads(res)
        logger.info(mapping_new)
        assert mapping_new["F150"] == self.get_f1aa_data_info(baseLineVer), "刷写结束后baseLineVer不匹配"
        display_ver_lst = [int(hex(ord(c)), 16) for c in displayVersion]
        assert display_ver_lst == mapping_new["F151"][:len(display_ver_lst)], "刷写结束后displayVersion不匹配"
        self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FACTORY_SUCCESSFUL.value, timeout=300)

    @allure.title("FOTA升级结束_退出FOTAMODE（TCAM/ACU/CDC）_否定响应") 
    def test_fota_caseid_1982637(self):
        self.diag_mock.doip_sim_start()
        self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x10, 0x00]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:exit_ota => factory_exit_ota', timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type='-E " fota:| obt:"', keywords=['QuitFotaModeCb:quit_fota_mode_ecu_info, ecu_name:ACU,ecu quit_fota_mode: 0',
                                                                                   'SendRawData:raw data: :[ 31 01 40 00 00 ]'
                                                                                   ], timeout=300):
            self.diag_mock.doip_sim_start()
            self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : {"NRC": 0x22}}})
        self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FACTORY_FAILED.value, timeout=300)

    @allure.title("FOTA升级结束_退出FOTAMODE（TCAM/ACU/CDC）_超时未响应") 
    def test_fota_caseid_1982636(self):
        self.diag_mock.doip_sim_start()
        self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x10, 0x00]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:exit_ota => factory_exit_ota', timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type='-E " fota:| obt:"', keywords=['QuitFotaModeCb:quit_fota_mode_ecu_info, ecu_name:ACU,ecu quit_fota_mode: 0',
                                                                                   'SendRawData:raw data: :[ 31 01 40 00 00 ]'
                                                                                   ], timeout=300):
            self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : {"NRC": "no_reply"}}})
        self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FACTORY_FAILED.value, timeout=300)

    @allure.title("FOTA升级结束_退出FOTAMODE（TCAM/ACU/CDC）_肯定响应error") 
    def test_fota_caseid_1982635(self):
        self.diag_mock.doip_sim_start()
        self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x10, 0x00]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:exit_ota => factory_exit_ota', timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type='-E " fota:| obt:"', keywords=['QuitFotaModeCb:quit_fota_mode_ecu_info, ecu_name:ACU,ecu quit_fota_mode: 0',
                                                                                   'SendRawData:raw data: :[ 31 01 40 00 00 ]'
                                                                                   ], timeout=300):
            self.diag_mock.doip_sim_start()
            self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x20, 0xff]}})
        self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FACTORY_FAILED.value, timeout=300)

    @allure.title("FOTA升级结束_退出FOTAMODE（TCAM/ACU/CDC）_肯定响应") 
    def test_fota_caseid_1982634(self):
        self.diag_mock.doip_sim_start()
        self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x10, 0x00]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:exit_ota => factory_exit_ota', timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='SendRawData:raw data: :[ 31 01 42 89 00 ]', timeout=300):
            self.diag_mock.doip_sim_start()
            self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x10, 0x00]}})
        self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FACTORY_FAILED.value, timeout=300)

    @allure.title("FOTA升级结束_退出FOTAMODE（ECM3）_否定响应") 
    def test_fota_caseid_1982633(self):
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords='send raw data rsp addr:1630, data:71 01 42 89 10 01', timeout=600):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 42 89 00',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 00',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 00',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 00'], timeout=1200):
            self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : {"NRC": 0x11}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords='send stack raw data, addr:1630, data::31 01 40 00 00', timeout=30):
            pass
        self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FACTORY_FAILED.value, timeout=300)

    @allure.title("FOTA升级结束_退出FOTAMODE（ECM3）_超时未响应") 
    def test_fota_caseid_1982632(self):
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords='send raw data rsp addr:1630, data:71 01 42 89 10 01', timeout=600):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 42 89 00',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 00',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 00',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 00'], timeout=1200):
            self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : {"NRC": "no_reply"}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords='send stack raw data, addr:1630, data::31 01 40 00 00', timeout=30):
            pass
        self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FACTORY_FAILED.value, timeout=300)

    @allure.title("FOTA升级结束_退出FOTAMODE（ECM3）_肯定响应") 
    def test_fota_caseid_1982631(self):
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:exit_ota => factory_exit_ota', timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords='send stack raw data, addr:1630, data::31 01 40 00 00', timeout=300):
            pass
        self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FACTORY_FAILED.value, timeout=300)

    @allure.title("FOTA升级结束_恢复高压（ECM3）_否定响应") 
    def test_fota_caseid_1982630(self):
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : [0x10, 0x01]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:exit_ota => factory_exit_ota', timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 42 89 00',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 00',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 00',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 00',
                                                                                  'send stack raw data, addr:1002, data::2e f1 53 00'], timeout=300):
            self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : {"NRC": 0x11}}})
        self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FACTORY_FAILED.value, timeout=300)

    @allure.title("FOTA升级结束_恢复高压（ECM3）_超时不响应") 
    def test_fota_caseid_1982629(self):
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : [0x10, 0x01]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:exit_ota => factory_exit_ota', timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 42 89 00',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 00',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 00',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 00',
                                                                                  'send stack raw data, addr:1002, data::2e f1 53 00'], timeout=300):
            self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : {"NRC": "no_reply"}}})
        self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FACTORY_FAILED.value, timeout=300)

    @allure.title("FOTA升级结束_恢复高压（ECM3）_肯定响应") 
    def test_fota_caseid_1982628(self):
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : [0x10, 0x01]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='ChangeState:exit_ota => factory_exit_ota', timeout=1200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords='send stack raw data, addr:1002, data::2e f1 53 00', timeout=300):
            pass
        self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FACTORY_FAILED.value, timeout=300)

    @allure.title("FOTA升级结束_升级失败")
    def test_fota_caseid_1982625(self):
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='factory_exit_ota => factory_ota_finish',timeout=1600):
            self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.FACTORY_FAILED.value, timeout=1600)
        # assert self.soa.get_fota_UpdateProcess(MASTER_UpdateProcess_EVENT.progress) == 100   SOA-28477偏差通过不同步进度
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords=['onTimer:Send 3E 80',
                                                                                              'SetVFCReqDiagnosticCb: VfcType :23 ActState :2'],timeout=20):
            pass

    @allure.title("FOTA升级结束_雨刮车窗标定成功") 
    def test_fota_caseid_1982621(self):
        self.io.set_five_door_sts(Door.close)
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_FAILED)
        self.bus_comm.cancel_filter_msg_all()
        self.bus_comm.filter_bus(bus_name="bodycan")
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x03: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x05: [0xf7, 0x84, 0x3b], 0x06: []})
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"2046": { 1 : [0x20],  3 : [0x20]}})
        self.diag_mock.update_0x10_data(ecu_name="PDM", session_mode={0x03: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x27_data(ecu_name="PDM", data_info={0x05: [0x5f, 0xb9, 0x02], 0x06: []})
        self.diag_mock.update_0x31_data(ecu_name="PDM", routine_control_data={"2046": { 1 : [0x20],  3 : [0x20]}})
        self.diag_mock.update_0x10_data(ecu_name="RLDM", session_mode={0x03: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x27_data(ecu_name="RLDM", data_info={0x05: [0x5f, 0xfd, 0x74], 0x06: []})
        self.diag_mock.update_0x31_data(ecu_name="RLDM", routine_control_data={"204E": { 1 : [0x20],  3 : [0x20]}})
        self.diag_mock.update_0x10_data(ecu_name="RRDM", session_mode={0x03: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x27_data(ecu_name="RRDM", data_info={0x05: [0xf7, 0x32, 0xf3], 0x06: []})
        self.diag_mock.update_0x31_data(ecu_name="RRDM", routine_control_data={"204E": { 1 : [0x20],  3 : [0x20]}})
        with self.log_manage.check_jetlog_by_keywords(log_type="CALI_DIAGP: ", keywords=['UpdateNotifyEOLCaliInfoEvent:{"Device":0,"Status":3,"ErrorCode":0,"NRC":0}',
                                                                                        'UpdateNotifyEOLCaliInfoEvent:{"Device":1,"Status":3,"ErrorCode":0,"NRC":0}'],timeout=60):
            pass

    @allure.title("FOTA升级结束_雨刮车窗标定4门否定响应") 
    def test_fota_caseid_1982618(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_FAILED)
        self.bus_comm.cancel_filter_msg_all()
        self.bus_comm.filter_bus(bus_name="bodycan")
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x03: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x05: [0xf7, 0x84, 0x3b], 0x06: []})
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"2046": { 1 : {"NRC": 0x22},  3 : {"NRC": 0x22}}})
        with self.log_manage.check_jetlog_by_keywords(log_type="CALI_DIAGP: ", unexpect_keywords=['UpdateNotifyEOLCaliInfoEvent:{"Device":0,"Status":3,"ErrorCode":0,"NRC":0}'],timeout=60):
            pass

    @allure.title("FOTA升级结束_雨刮车窗标定4门超时不响应") 
    def test_fota_caseid_1982617(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_FAILED)
        self.bus_comm.cancel_filter_msg_all()
        self.bus_comm.filter_bus(bus_name="bodycan")
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x03: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x05: [0xf7, 0x84, 0x3b], 0x06: []})
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"2046": { 1 : {"NRC": "no_reply"},  3 : {"NRC": "no_reply"}}})
        with self.log_manage.check_jetlog_by_keywords(log_type="CALI_DIAGP: ", unexpect_keywords=['UpdateNotifyEOLCaliInfoEvent:{"Device":0,"Status":3,"ErrorCode":0,"NRC":0}'],timeout=60):
            pass

    @allure.title("FOTA升级结束_雨刮车窗标定4门肯定响应71 03 20 4E 21") 
    def test_fota_caseid_1982616(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_FAILED)
        self.bus_comm.cancel_filter_msg_all()
        self.bus_comm.filter_bus(bus_name="bodycan")
        self.diag_mock.update_0x10_data(ecu_name="RLDM", session_mode={0x03: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x27_data(ecu_name="RLDM", data_info={0x05: [0xf7, 0x84, 0x3b], 0x06: []})
        self.diag_mock.update_0x31_data(ecu_name="RLDM", routine_control_data={"204E": { 1 : [0x20],  3 : [0x21]}})
        with self.log_manage.check_jetlog_by_keywords(log_type="CALI_DIAGP: ", unexpect_keywords=['UpdateNotifyEOLCaliInfoEvent:{"Device":0,"Status":3,"ErrorCode":0,"NRC":0}'],timeout=60):
            pass

    @allure.title("FOTA升级结束_雨刮车窗标定4门肯定响应71 03 20 4E XX非21/20") 
    def test_fota_caseid_1982615(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_FAILED)
        self.bus_comm.cancel_filter_msg_all()
        self.bus_comm.filter_bus(bus_name="bodycan")
        self.diag_mock.update_0x10_data(ecu_name="RLDM", session_mode={0x03: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x27_data(ecu_name="RLDM", data_info={0x05: [0xf7, 0x84, 0x3b], 0x06: []})
        self.diag_mock.update_0x31_data(ecu_name="RLDM", routine_control_data={"204E": { 1 : [0x20],  3 : [0x23]}})
        with self.log_manage.check_jetlog_by_keywords(log_type="CALI_DIAGP: ", unexpect_keywords=['UpdateNotifyEOLCaliInfoEvent:{"Device":0,"Status":3,"ErrorCode":0,"NRC":0}'],timeout=60):
            pass


if __name__ == "__main__":
    pass





