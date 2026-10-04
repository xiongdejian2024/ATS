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

    @allure.title("Group升级中_单个普通ECU升级_1002持续否定响应") 
    def test_fota_caseid_1982460(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: {"NRC": 0x22}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=["send stack raw data, addr:1a12, data::10 02",
                                                                                  "send stack raw data, addr:1a12, data::10 02"], timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        # 规避重启之后log检查函数停止执行的问题
        time.sleep(120)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="name:DDM , err code:4 ,",  timeout=800):
            pass

    @allure.title("Group升级中_单个普通ECU升级_1002重试成功") 
    def test_fota_caseid_1982459(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=["send stack raw data, addr:1a12, data::10 02",
                                                                                  "send stack raw data, addr:1a12, data::10 02",
                                                                                  "send stack raw data, addr:1a12, data::22 f1 86"], timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

    @allure.title("Group升级中_单个普通ECU升级_会话检查异常响应超时") 
    def test_fota_caseid_1982458(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x01])
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=["send stack raw data, addr:1a12, data::22 f1 86",
                                                                                   "send stack raw data, addr:1a12, data::22 f1 86"], timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" diag_client:", unexpect_keywords="tx 1a12:22 d0 1c", timeout=10):
            pass

    @allure.title("Group升级中_单个普通ECU升级_会话失败重试进boot后检测失败") 
    def test_fota_caseid_1982457(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x01])
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=["send stack raw data, addr:1a12, data::22 f1 86",
                                                                                   "send stack raw data, addr:1a12, data::22 f1 86"], timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" diag_client:", unexpect_keywords="tx 1a12:22 d0 1c", timeout=10):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="name:DDM , err code:4 ,", timeout=800):
            pass

    @allure.title("Group升级中_单个普通ECU升级_会话失败重试进boot后检测成功") 
    def test_fota_caseid_1982456(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x01])
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=["send stack raw data, addr:1a12, data::22 f1 86",
                                                                                   "send stack raw data, addr:1a12, data::22 f1 86"], timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" diag_client:", keywords="tx 1a12:22 d0 1c", timeout=10):
            self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])

    @allure.title("Group升级中_单个普通ECU升级_获取公钥肯定响应") 
    def test_fota_caseid_1982455(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update=[0x00])
        with self.log_manage.check_jetlog_by_keywords(log_type=" diag_client:", keywords="tx 1a12:27 01", timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        # TODO: check验签类型
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords="send stack raw data, addr:1a12, data::31 01 02 12", timeout=300):
            pass

    @allure.title("Group升级中_单个普通ECU升级_获取公钥否定响应") 
    def test_fota_caseid_1982454(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update={"NRC": 0x22})
        with self.log_manage.check_jetlog_by_keywords(log_type=" diag_client:", keywords="tx 1a12:27 01", timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        # TODO: check验签类型
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords="send stack raw data, addr:1a12, data::31 01 02 12", timeout=300):
            pass

    @allure.title("Group升级中_单个普通ECU升级_2701解锁持续否定响应") 
    def test_fota_caseid_1982453(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update={"NRC": 0x22})
        self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: {"NRC": 0x22}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" diag_client:", keywords=["tx 1a12:27 01", "tx 1a12:27 01"], timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="name:DDM , err code:4 ,", timeout=800):
            pass

    @allure.title("Group升级中_单个普通ECU升级_2701解锁失败重试成功") 
    def test_fota_caseid_1982452(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update={"NRC": 0x22})
        self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce]})
        with self.log_manage.check_jetlog_by_keywords(log_type=" diag_client:", keywords=["tx 1a12:27 01", 
                                                                                          "tx 1a12:27 01",
                                                                                          "tx 1a12:27 02 7d 90 6c"], timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

    @allure.title("Group升级中_单个普通ECU升级_2702解锁Pincode使用") 
    def test_fota_caseid_1982451(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update=[0x00])
        self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce]})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=["seed: a9 19 ce, constant: ff ff ff ff ff",
                                                                                  "seed: a9 19 ce, constant: ff ff ff ff ff"], timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

    @allure.title("Group升级中_单个普通ECU升级_2702解锁持续否定响应") 
    def test_fota_caseid_1982450(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update=[0x00])
        self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: {"NRC": 0x22}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="name:DDM , err code:4 ,", timeout=1400): 
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

    @allure.title("Group升级中_SBL刷写_34请求下载持续否定响应/不响应") 
    def test_fota_caseid_1982449(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update={"NRC": 0x22})
        self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
        self.diag_mock.update_0x34_data(ecu_name="DDM", data={"NRC": 0x22})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="name:DDM , err code:4 ,", timeout=1400): 
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

    @allure.title("Group升级中_SBL刷写_34请求下载异常响应后正响应") 
    def test_fota_caseid_1982448(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update={"NRC": 0x22})
        self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
        self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords="send stack raw data, addr:1a12, start data: 36 01", timeout=1400):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

    @allure.title("Group升级中_SBL刷写_36数据传输持续否定响应") 
    def test_fota_caseid_1982447(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update={"NRC": 0x22})
        self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
        self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])
        self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={2: 0x22})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=["send stack raw data, addr:1a12, start data: 36 02",
                                                                                  "send stack raw data, addr:1a12, start data: 36 02"], timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="name:DDM , err code:4 ,", timeout=800):
            pass

    @allure.title("Group升级中_SBL刷写_36数据传输超时不响应后否定响应") 
    def test_fota_caseid_1982446(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update={"NRC": 0x22})
        self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
        self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])
        self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={2: 0x78})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=["send stack raw data, addr:1a12, start data: 36 02",
                                                                                "send stack raw data, addr:1a12, start data: 36 02"], timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords="send stack raw data, addr:1a12, start data: 36 02", timeout=300):
            self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={2: 0x22})

    @allure.title("Group升级中_SBL刷写_36数据传输重试成功") 
    def test_fota_caseid_1982445(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update={"NRC": 0x22})
        self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
        self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])
        self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={2: 0x22})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=["send stack raw data, addr:1a12, start data: 36 02"], timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords="send stack raw data, addr:1a12, data::37", timeout=300):
            self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={})

    @allure.title("Group升级中_SBL刷写_37退出数据传输持续否定响应") 
    def test_fota_caseid_1982444(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update={"NRC": 0x22})
        self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
        self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])
        self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={})
        self.diag_mock.update_0x37_data(ecu_name="DDM", data={"NRC": 0x22})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=["send stack raw data, addr:1a12, data::37",
                                                                                  "send stack raw data, addr:1a12, data::37"], timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="name:DDM , err code:4 ,", timeout=800): 
            pass

# 37服务重试诊断请求间隔只有十几毫秒，来不及处理，依赖capl脚本验证
    # @allure.title("Group升级中_SBL刷写_37退出数据传输重试成功") 
    # def test_fota_caseid_1982426(self):
    #     self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
    #     self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update={"NRC": 0x22})
    #     self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
    #     self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])
    #     self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={})
    #     self.diag_mock.update_0x37_data(ecu_name="DDM", data={"NRC": 0x22})
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=["send stack raw data, addr:1a12, data::37"], timeout=800):
    #         self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
    #     self.diag_mock.update_0x37_data(ecu_name="DDM", data={})
    #     with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords="send stack raw data, addr:1a12, data::31 01 02 12", timeout=300): 
    #         pass

    @allure.title("Group升级中_SBL刷写_签名验签持续异常响应") 
    def test_fota_caseid_1982425(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update={"NRC": 0x22})
        self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
        self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])
        self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={})
        self.diag_mock.update_0x37_data(ecu_name="DDM", data={})
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0212": { 1 : [0x10, 0x01]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=["send stack raw data, addr:1a12, data::31 01 02 12",
                                                                                  "send stack raw data, addr:1a12, data::31 01 02 12"], timeout=800): 
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="name:DDM , err code:4 ,", timeout=800): 
            pass

    @allure.title("Group升级中_SBL刷写_激活SBL持续异常响应") 
    def test_fota_caseid_1982424(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update={"NRC": 0x22})
        self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
        self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])
        self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={})
        self.diag_mock.update_0x37_data(ecu_name="DDM", data={})
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0212": { 1 : [0x10, 0x00]}})
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0301": { 1 : {"NRC": 0x22}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=["send stack raw data, addr:1a12, data::31 01 03 01",
                                                                                  "send stack raw data, addr:1a12, data::31 01 03 01"], timeout=800): 
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="name:DDM , err code:4 ,", timeout=800): 
            pass

    @allure.title("Group升级中_SBL刷写_激活SBL重试成功") 
    def test_fota_caseid_1982423(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update={"NRC": 0x22})
        self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
        self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])
        self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={})
        self.diag_mock.update_0x37_data(ecu_name="DDM", data={})
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0212": { 1 : [0x10, 0x00]}})
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0301": { 1 : [0x10]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" diag_client:", keywords="tx 1a12:31 01 ff 00", timeout=800): 
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

    @allure.title("Group升级中_其他VBF刷写_擦除内存持续否定响应") 
    def test_fota_caseid_1982422(self):
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update={"NRC": 0x22})
        self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})
        self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])
        self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={})
        self.diag_mock.update_0x37_data(ecu_name="DDM", data={})
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0212": { 1 : [0x10, 0x00]}})
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0301": { 1 : [0x10]}})
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"FF00": { 1 : {"NRC": 0x22}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" diag_client:", keywords=["tx 1a12:31 01 ff 00 00 01 b0 00 00 00 00 40", 
                                                                                          "tx 1a12:31 01 ff 00 00 01 b0 00 00 00 00 40"], timeout=800): 
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="name:DDM , err code:4 ,", timeout=800): 
            pass

    @allure.title("Group升级中_其他VBF刷写_擦除内存重试成功") 
    def test_fota_caseid_1982421(self):
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
        with self.log_manage.check_jetlog_by_keywords(log_type=" diag_client:", keywords="tx 1a12:31 01 ff 00 00 01 b0 00 00 00 00 40", timeout=800): 
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords="send stack raw data, addr:1a12, data::34", timeout=300): 
            pass

    @allure.title("Group升级中_其他VBF刷写_刷写VBF后验签持续否定响应") 
    def test_fota_caseid_1982420(self):
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
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords="send stack raw data, addr:1a12, data::31 01 ff 00", timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="name:DDM , err code:4 ,", timeout=800): 
            self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0212": { 1 : [0x10, 0x01]}})

    @allure.title("Group升级中_Post-Programming流程_完整性校验异常响应") 
    def test_fota_caseid_1982419(self):
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
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0205": { 1 : {"NRC": 0x22}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=["send stack raw data, addr:1a12, data::31 01 02 05",
                                                                                  "send stack raw data, addr:1a12, data::31 01 02 05"], timeout=800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="name:DDM , err code:4 ,", timeout=800): 
            pass

    @allure.title("Group升级中_Post-Programming流程_完整性校验肯定响应") 
    def test_fota_caseid_1982418(self):
        # 更新DDM的SID：10且session_mode：02的回复数据为[0x00, 0x32, 0x01, 0xf4]。此例子的实际回复的数据为：10 02回复50 01 00 32 01 f4
        self.diag_mock.update_0x10_data(ecu_name="DDM", session_mode={0x02: [0x00, 0x32, 0x01, 0xf4]})

        # 更新DDM的SID：22且DID：F186的回复数据为[0x02]。此例子的实际回复的数据为：22 f1 86回复62 f1 86 02
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="F186", data_info_update=[0x02])

        # 更新DDM的SID：22且DID：D01C的回复数据为{"NRC": 0x22}即负响应。此例子的实际回复的数据为：22 d0 1c回复7f 22 22
        self.diag_mock.update_0x22_data(ecu_name="DDM", did="D01C", data_info_update={"NRC": 0x22})

        # 更新DDM的SID：27且为请求安全解锁种子01的回复数据为[0xa9, 0x19, 0xce],发送安全解锁key 02的回复数据为空。此例子的实际回复的数据为：27 01回复67 01 a9 19 ce，27 02回复67 02
        self.diag_mock.update_0x27_data(ecu_name="DDM", data_info={0x01: [0xa9, 0x19, 0xce], 0x02: []})

        # 更新DDM的SID：34的回复数据为[0x20, 0x0f, 0xa2]。此例子的实际回复的数据为：34 ...回复74 20 0f a2
        self.diag_mock.update_0x34_data(ecu_name="DDM", data=[0x20, 0x0f, 0xa2])

        # 更新DDM的SID：36的block_sequence_counter_nrc_config为空代表所有36服务均回复正相应。如果需要回复负响应，例如：block_sequence_counter_nrc_config={2: 0x78, 18: 0x11} 表示
        # DDM收到第二个counter回复否定响应0x78，第18个counter回复0x11否定响应
        self.diag_mock.update_0x36_data(ecu_name="DDM", block_sequence_counter_nrc_config={})

        # 更新DDM的SID：37的回复数据为空。此例子的实际回复的数据为：67
        self.diag_mock.update_0x37_data(ecu_name="DDM", data={})

        # 更新DDM的SID：31且DID：0212的回复数据为{ 1 : [0x10, 0x00]}。此例子的实际回复的数据为：31 01 02 12回复71 01 02 12 10 00
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0212": { 1 : [0x10, 0x00]}})

        # 更新DDM的SID：31且DID：0301的回复数据为{ 1 : [0x10]}。此例子的实际回复的数据为：31 01 03 01回复71 01 03 01 10
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0301": { 1 : [0x10]}})

        # 更新DDM的SID：31且DID：FF00的回复数据为{ 1 : [0x10]}。此例子的实际回复的数据为：31 01 ff 00回复71 01 ff 00 10
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"FF00": { 1 : [0x10]}})

        # 更新DDM的SID：31且DID：0205的回复数据为{ 1 : [0x10, 0x00, 0x00, 0x00, 0x00]}。此例子的实际回复的数据为：31 01 02 05回复71 01 02 05 10 00 00 00 00
        self.diag_mock.update_0x31_data(ecu_name="DDM", routine_control_data={"0205": { 1 : [0x10, 0x00, 0x00, 0x00, 0x00]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=["send stack raw data, addr:1a12, data::31 01 02 05",
                                                                                  "send stack raw data, addr:1a12, data::31 01 02 05"], timeout=800):

            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="name:DDM , err code:4096 ,", timeout=800): 
            pass

if __name__ == "__main__":
    pass





