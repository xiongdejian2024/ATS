#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : test_diag_bgm_rml.py
@time         : 2024/03/08 14:19
@author       : o_jingyuan.chen@external.jiduauto.com
@description  : 
'''

import pytest
import allure

from xat_cases.legacy.basetech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.soa_partner.src.partner_const import *
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check

@allure.feature('BGM BaseTech/诊断功能')
@allure.story('RML诊断功能')
class TestRML(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self,ecu)
        self.sd_tester.update_serverdoipid(0x1510, "RML")
        logger.info("before_class")
        partner_process_check()
        self.soa.update([("ObtDiagService","client")])
        time.sleep(5)
        self.io.bgm_diag_line_down()#拉低诊断激活线、触发RVS
        self.soa.send_method_request(OBTDIAG_SERVICE_CLIENT, "ReadBeltVibInfo", {})
        self.soa.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "NotifyBeltVibInfo",
                                            {"info":{"VibNum":0xffffffff,"ErrorCode":1,"NRC":0}},timeout=5) 
        logger.info("延时375 秒 等待RVS版本收集完成,诊断仲裁idle")
        time.sleep(375)#等待RVS版本收集完成，诊断仲裁idle

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.soa.empty_all()
        if "power_control_type" in ecu.tb_config:
            ecu.tb_config["power_control_type"] = "jydam0801"
        logger.info(f"case开始运行*******************************************************")

    def after_each_func(self, ecu):
        if ecu.get("testresult") != "Pass":
            logger.info("case失败，需等待5s让环境恢复")
            sleep(5)
        else:
            sleep(3)        
        logger.info(f"case结束运行*******************************************************")
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        if "power_control_type" in ecu.tb_config:
            ecu.tb_config["power_control_type"] = "jydam0800"
            self.io.bgm_diag_line_up()
        super().after_class(self, ecu)

    #P2 本地诊断释放诊断仲裁，触发RVS版本收集
    @pytest.mark.full
    @allure.title('RML诊断_诊断仲裁失败_同优先级')
    def test_caseid_1985533(self):
        pass

    @pytest.mark.full
    @allure.title('RML诊断_服务端内部错误')
    def test_caseid_1985524(self):
        self.soa.send_method_request(OBTDIAG_SERVICE_CLIENT, "ReadBeltVibInfo", {})
        self.diag_mock.send_candata(bus_name="passivesafetycan", ecu_name="RML", res_ecu_canid=0x610, data=[0x04, 0x62, 0xD9, 0x00, 0x00, 0x00, 0x00, 0x00])
        self.soa.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "NotifyBeltVibInfo",
                                            {"info":{"VibNum":0xffffffff,"ErrorCode":4,"NRC":0}},timeout=10) 

    @pytest.mark.smoke
    @allure.title('RML诊断_震动累计次数_最小值')
    def test_caseid_1985538(self):
        self.diag_mock.update_0x22_data(ecu_name="RML", did="D900", data_info_update=[0x00, 0x00, 0x00, 0x00])
        time.sleep(1)
        self.soa.send_method_request(OBTDIAG_SERVICE_CLIENT, "ReadBeltVibInfo", {})
        self.soa.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "NotifyBeltVibInfo",
                                            {"info":{"VibNum":0x00000000,"ErrorCode":0,"NRC":0}},timeout=5)   
        
    @pytest.mark.smoke
    @allure.title('RML诊断_震动累计次数_正常值')
    def test_caseid_1985537(self):
        self.soa.send_method_request(OBTDIAG_SERVICE_CLIENT, "ReadBeltVibInfo", {})
        self.diag_mock.update_0x22_data(ecu_name="RML", did="D900", data_info_update=[0x00, 0x00, 0x00, 0x01])
        self.soa.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "NotifyBeltVibInfo",
                                            {"info":{"VibNum":0x00000001,"ErrorCode":0,"NRC":0}},timeout=5) 

    @pytest.mark.smoke
    @allure.title('RML诊断_震动累计次数_最大值')
    def test_caseid_1985536(self):
        self.soa.send_method_request(OBTDIAG_SERVICE_CLIENT, "ReadBeltVibInfo", {})
        self.diag_mock.update_0x22_data(ecu_name="RML", did="D900", data_info_update=[0x00, 0x00, 0x13, 0x88])
        self.soa.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "NotifyBeltVibInfo",
                                            {"info":{"VibNum":0x00001388,"ErrorCode":0,"NRC":0}},timeout=5)   

    @pytest.mark.sanity
    @allure.title('RML诊断_UDS请求回复NRC13')
    def test_caseid_1985531(self):
        self.soa.send_method_request(OBTDIAG_SERVICE_CLIENT, "ReadBeltVibInfo", {})
        self.diag_mock.update_0x22_data(ecu_name="RML", did="D900", data_info_update={"NRC": 0x13})
        self.soa.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "NotifyBeltVibInfo",
                                            {"info":{"VibNum":0xFFFFFFFF,"ErrorCode":3,"NRC":0x13}},timeout=5)   

    @pytest.mark.sanity
    @allure.title('RML诊断_UDS请求回复NRC14')
    def test_caseid_1985530(self):
        self.soa.send_method_request(OBTDIAG_SERVICE_CLIENT, "ReadBeltVibInfo", {})
        self.diag_mock.update_0x22_data(ecu_name="RML", did="D900", data_info_update={"NRC": 0x14})
        self.soa.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "NotifyBeltVibInfo",
                                            {"info":{"VibNum":0xFFFFFFFF,"ErrorCode":3,"NRC":0x14}},timeout=5)   

    @pytest.mark.sanity
    @allure.title('RML诊断_UDS请求回复NRC22')
    def test_caseid_1985529(self):
        self.soa.send_method_request(OBTDIAG_SERVICE_CLIENT, "ReadBeltVibInfo", {})
        self.diag_mock.update_0x22_data(ecu_name="RML", did="D900", data_info_update={"NRC": 0x22})
        self.soa.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "NotifyBeltVibInfo",
                                            {"info":{"VibNum":0xFFFFFFFF,"ErrorCode":3,"NRC":0x22}},timeout=5)   

    @pytest.mark.sanity
    @allure.title('RML诊断_UDS请求回复NRC31')
    def test_caseid_1985528(self):
        self.soa.send_method_request(OBTDIAG_SERVICE_CLIENT, "ReadBeltVibInfo", {})
        self.diag_mock.update_0x22_data(ecu_name="RML", did="D900", data_info_update={"NRC": 0x31})
        self.soa.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "NotifyBeltVibInfo",
                                            {"info":{"VibNum":0xFFFFFFFF,"ErrorCode":3,"NRC":0x31}},timeout=5)   
        
    @pytest.mark.full
    @allure.title('RML诊断_UDS请求回复NRC_只记录最后一次请求的NRC')
    def test_caseid_1985527(self):
        self.diag_mock.update_0x22_data(ecu_name="RML", did="D900", data_info_update={"NRC": 0x78})
        self.soa.send_method_request(OBTDIAG_SERVICE_CLIENT, "ReadBeltVibInfo", {})
        self.diag_mock.update_0x22_data(ecu_name="RML", did="D900", data_info_update={"NRC": 0x78})
        self.diag_mock.update_0x22_data(ecu_name="RML", did="D900", data_info_update={"NRC": 0x22})
        self.soa.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "NotifyBeltVibInfo",
                                            {"info":{"VibNum":0xFFFFFFFF,"ErrorCode":3,"NRC":0x22}},timeout=5)   
        
    @pytest.mark.full
    @allure.title('RML诊断_UDS请求回复NRC78')
    def test_caseid_1985526(self):
        self.diag_mock.update_0x22_data(ecu_name="RML", did="D900", data_info_update={"NRC": 0x78})
        self.soa.send_method_request(OBTDIAG_SERVICE_CLIENT, "ReadBeltVibInfo", {})
        time.sleep(1)
        self.diag_mock.send_candata(bus_name="passivesafetycan", ecu_name="RML", res_ecu_canid=0x610, data=[0x07, 0x62, 0xD9, 0x00, 0x00, 0x00, 0x10, 0x11])
        time.sleep(1)
        self.soa.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "NotifyBeltVibInfo",
                                            {"info":{"VibNum":0x00001011,"ErrorCode":0,"NRC":0}},timeout=10)   

    @pytest.mark.full
    @allure.title('RML诊断_UDS请求回复NRC78_超时')
    def test_caseid_1985525(self):
        self.soa.send_method_request(OBTDIAG_SERVICE_CLIENT, "ReadBeltVibInfo", {})
        self.diag_mock.update_0x22_data(ecu_name="RML", did="D900", data_info_update={"NRC": 0x78})
        self.soa.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "NotifyBeltVibInfo",
                                            {"info":{"VibNum":0xFFFFFFFF,"ErrorCode":2,"NRC":0}},timeout=7)   
        
    #P1
    @pytest.mark.sanity
    @allure.title('RML诊断_UDS请求无回复')
    def test_caseid_1985532(self):
        self.soa.send_method_request(OBTDIAG_SERVICE_CLIENT, "ReadBeltVibInfo", {})
        self.soa.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "NotifyBeltVibInfo",
                                            {"info":{"VibNum":0xffffffff,"ErrorCode":2,"NRC":0}},timeout=15) 
        
        
    #P1 
    @pytest.mark.sanity
    @allure.title('RML诊断_诊断仲裁失败_高优先级打断')
    def test_caseid_1985534(self):
        with self.log_manage.check_jetlog_by_keywords(log_type="ARB_MGR:",keywords='local diag win the arbitration rights'):
            self.diag_mock.all_close()
            self.soa.send_method_request(OBTDIAG_SERVICE_CLIENT, "ReadBeltVibInfo", {})
            self.io.bgm_diag_line_up()#拉起本地诊断
            self.soa.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "NotifyBeltVibInfo",
                                                {"info":{"VibNum":0xffffffff,"ErrorCode":2,"NRC":0}},timeout=10) 
        
    #P2 本地诊断先赢得优先权
    @pytest.mark.full
    @allure.title('RML诊断_诊断仲裁失败_高优先级忽略')
    def test_caseid_1985535(self):
        self.soa.send_method_request(OBTDIAG_SERVICE_CLIENT, "ReadBeltVibInfo", {})
        self.soa.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "NotifyBeltVibInfo",
                                            {"info":{"VibNum":0xffffffff,"ErrorCode":1,"NRC":0}},timeout=5) 

    #pytest BaseTech/Diagnostics/test_diag_bgm_rml.py::TestRML::test_caseid_1985526 --tccfg=config/daignostic_rml_config.yaml
    #pytest BaseTech/Diagnostics/test_diag_bgm_rml.py --tccfg=config/daignostic_rml_config.yaml