#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_nfc_learning_abc.py
@Time         :2023/1/31 17:54:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import os
import sys

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ""))
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))

from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass_abc import *
from xat_ecu.api.abc_interface import *
func = ["NFCLearningUpLinkReq"]

@allure.feature("互联服务")
@allure.story("数字钥匙和账号/NFC学卡")
class TestDigitalKeyWhiteListConTrol(TestDigitalKeyBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.soa.set_maintenanceMode(maintenanceMode=False)

    def after_class(self, ecu):
        super().after_class(self, ecu)
    
    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu)
        self.bus_comm.dk.empty_dk_data_queue()
        sleep(2)
    
    def after_each_func(self, ecu):
        """每个测试用例后置步骤"""
        super().after_each_func(ecu)
        sleep(2)

    
    @allure.title("远程NFC学卡_学卡失败_UsageModeFail_Inactive")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111932?projectId=46')
    @pytest.mark.full
    def test_caseid_111932(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(2)
        req_feedback = self.nfc_learning()
        execid = req_feedback["data"]["execId"]
        sleep(1)
        self.bus_comm.dk.ck_bgm_not_send_cmd("条件不满足，BGM不应发送指令给BNCM", self.bus_comm.dk.dk_data_queue_tsp)
        target = func + [f"{execid}"]+[f"ErrCode:16"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # self.tsp.check_digital_key_result(func="NFCLearning",keys=[self.tc_config.get('vid'), execid,"ExecId", "ErrCode"],target_value={"errCode":16})



    @allure.title("远程NFC学卡_学卡失败_当前钥匙已在白名单_Convenience")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111945?projectId=46')
    @pytest.mark.full
    def test_caseid_111945(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(2)
        self.bus_comm.dk.empty_dk_data_queue()
        req_feedback = self.nfc_learning()
        execid = req_feedback["data"]["execId"]
        sleep(1)
        self.bus_comm.dk.ck_nfc_learning_req()
        sleep(2)
        self.bus_comm.dk.send_nfc_learning_resp(3)
        target = func + [f"{execid}"]+[f"ErrCode:3"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # self.tsp.check_digital_key_result(func="NFCLearning",keys=[self.tc_config.get('vid'), execid,"ExecId", "ErrCode"],target_value={"errCode":3})
    
    @allure.title("远程NFC学卡_学卡失败_UsageModeFail_Abandoned")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111935?projectId=46')
    @pytest.mark.full
    def test_caseid_111935(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        req_feedback = self.nfc_learning()
        execid = req_feedback["data"]["execId"]
        sleep(1)
        self.bus_comm.dk.ck_bgm_not_send_cmd("条件不满足，BGM不应发送指令给BNCM", self.bus_comm.dk.dk_data_queue_tsp)
        target = func + [f"{execid}"]+[f"ErrCode:16"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # self.tsp.check_digital_key_result(func="NFCLearning",keys=[self.tc_config.get('vid'), execid,"ExecId", "ErrCode"],target_value={"errCode":16})

    @allure.title("远程NFC学卡_学卡失败_UsageModeFail_Active")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111941?projectId=46')
    @pytest.mark.full
    def test_caseid_111941(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        sleep(2)
        req_feedback = self.nfc_learning()
        execid = req_feedback["data"]["execId"]
        sleep(1)
        self.bus_comm.dk.ck_bgm_not_send_cmd("条件不满足，BGM不应发送指令给BNCM", self.bus_comm.dk.dk_data_queue_tsp)
        target = func + [f"{execid}"]+[f"ErrCode:16"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # self.tsp.check_digital_key_result(func="NFCLearning",keys=[self.tc_config.get('vid'), execid,"ExecId", "ErrCode"],target_value={"errCode":16})

    @allure.title("远程NFC学卡_学卡失败_UsageModeFail_Driving+GearD")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111938?projectId=46')
    @pytest.mark.full
    def test_caseid_111938(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        sleep(2)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        req_feedback = self.nfc_learning()
        execid = req_feedback["data"]["execId"]
        sleep(1)
        self.bus_comm.dk.ck_bgm_not_send_cmd("条件不满足，BGM不应发送指令给BNCM", self.bus_comm.dk.dk_data_queue_tsp)
        target = func + [f"{execid}"]+[f"ErrCode:16"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # self.tsp.check_digital_key_result(func="NFCLearning",keys=[self.tc_config.get('vid'), execid,"ExecId", "ErrCode"],target_value={"errCode":16})


    @allure.title("远程NFC学卡_学卡失败_UsageModeFail_Driving+GearN")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111951?projectId=46')
    @pytest.mark.full
    def test_caseid_111951(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        sleep(2)
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        req_feedback = self.nfc_learning()
        execid = req_feedback["data"]["execId"]
        sleep(1)
        self.bus_comm.dk.ck_bgm_not_send_cmd("条件不满足，BGM不应发送指令给BNCM", self.bus_comm.dk.dk_data_queue_tsp)
        target = func + [f"{execid}"]+[f"ErrCode:16"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # self.tsp.check_digital_key_result(func="NFCLearning",keys=[self.tc_config.get('vid'), execid,"ExecId", "ErrCode"],target_value={"errCode":16})

    @allure.title("远程NFC学卡_学卡失败_UsageModeFail_Driving+GearR")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111946?projectId=46')
    @pytest.mark.full
    @pytest.mark.s2s_prebuild
    def test_caseid_111946(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        sleep(2)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        req_feedback = self.nfc_learning()
        execid = req_feedback["data"]["execId"]
        sleep(1)
        self.bus_comm.dk.ck_bgm_not_send_cmd("条件不满足，BGM不应发送指令给BNCM", self.bus_comm.dk.dk_data_queue_tsp)
        target = func + [f"{execid}"]+[f"ErrCode:16"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # self.tsp.check_digital_key_result(func="NFCLearning",keys=[self.tc_config.get('vid'), execid,"ExecId", "ErrCode"],target_value={"errCode":16})

    
    @allure.title("远程NFC学卡_学卡失败_当前钥匙已在白名单_Driving+GearP")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111937?projectId=46')
    @pytest.mark.full
    def test_caseid_111937(self):  # todo: 性能过不了
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        sleep(2)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        req_feedback = self.nfc_learning()
        execid = req_feedback["data"]["execId"]
        sleep(1)
        self.bus_comm.dk.ck_nfc_learning_req()
        sleep(2)
        self.bus_comm.dk.send_nfc_learning_resp(3)
        target = func + [f"{execid}"]+[f"ErrCode:3"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # self.tsp.check_digital_key_result(func="NFCLearning",keys=[self.tc_config.get('vid'), execid,"ExecId", "ErrCode"],target_value={"errCode":3})

    @allure.title("远程NFC学卡_学卡失败_未检测到卡片_Convenience")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111952?projectId=46')
    @pytest.mark.full
    def test_caseid_111952(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(2)
        req_feedback = self.nfc_learning()
        execid = req_feedback["data"]["execId"]
        sleep(1)
        self.bus_comm.dk.ck_nfc_learning_req()
        sleep(2)
        self.bus_comm.dk.send_nfc_learning_resp(1)
        target = func + [f"{execid}"]+[f"ErrCode:1"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # self.tsp.check_digital_key_result(func="NFCLearning",keys=[self.tc_config.get('vid'), execid,"ExecId", "ErrCode"],target_value={"errCode":1})

    @allure.title("远程NFC学卡_学卡失败_未检测到卡片_Driving+GearP")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111940?projectId=46')
    @pytest.mark.full
    def test_caseid_111940(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        sleep(2)
        self.bus_comm.dk.set_chassis_service_gear("GearP")
        req_feedback = self.nfc_learning()
        execid = req_feedback["data"]["execId"]
        sleep(1)
        self.bus_comm.dk.ck_nfc_learning_req()
        sleep(2)
        self.bus_comm.dk.send_nfc_learning_resp(1)
        target = func + [f"{execid}"]+[f"ErrCode:1"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # self.tsp.check_digital_key_result(func="NFCLearning",keys=[self.tc_config.get('vid'), execid,"ExecId", "ErrCode"],target_value={"errCode":1})

    @allure.title("远程NFC学卡_学卡失败_检测到无效卡_Convenience")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111934?projectId=46')
    @pytest.mark.full
    def test_caseid_111934(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(2)
        req_feedback = self.nfc_learning()
        execid = req_feedback["data"]["execId"]
        sleep(1)
        self.bus_comm.dk.ck_nfc_learning_req()
        sleep(2)
        self.bus_comm.dk.send_nfc_learning_resp(2)
        target = func + [f"{execid}"]+[f"ErrCode:2"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # self.tsp.check_digital_key_result(func="NFCLearning",keys=[self.tc_config.get('vid'), execid,"ExecId", "ErrCode"],target_value={"errCode":2})

    @allure.title("远程NFC学卡_学卡失败_检测到无效卡_Driving+GearP")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111936?projectId=46')
    @pytest.mark.full
    def test_caseid_111936(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        sleep(2)
        self.bus_comm.dk.set_chassis_service_gear("GearP")
        req_feedback = self.nfc_learning()
        execid = req_feedback["data"]["execId"]
        sleep(1)
        self.bus_comm.dk.ck_nfc_learning_req()
        sleep(2)
        self.bus_comm.dk.send_nfc_learning_resp(2)
        target = func + [f"{execid}"]+[f"ErrCode:2"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # self.tsp.check_digital_key_result(func="NFCLearning",keys=[self.tc_config.get('vid'), execid,"ExecId", "ErrCode"],target_value={"errCode":2})

    @allure.title("远程NFC学卡_学卡失败_添加失败_Convenience")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111950?projectId=46')
    @pytest.mark.full
    def test_caseid_111950(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(2)
        req_feedback = self.nfc_learning()
        execid = req_feedback["data"]["execId"]
        sleep(1)
        self.bus_comm.dk.ck_nfc_learning_req()
        sleep(2)
        self.bus_comm.dk.send_nfc_learning_resp(5)
        target = func + [f"{execid}"]+[f"ErrCode:5"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # self.tsp.check_digital_key_result(func="NFCLearning",keys=[self.tc_config.get('vid'), execid,"ExecId", "ErrCode"],target_value={"errCode":5})

    @allure.title("远程NFC学卡_学卡失败_添加失败_Driving+GearP")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111947?projectId=46')
    @pytest.mark.full
    def test_caseid_111947(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        sleep(2)
        self.bus_comm.dk.set_chassis_service_gear("GearP")
        req_feedback = self.nfc_learning()
        execid = req_feedback["data"]["execId"]
        sleep(1)
        self.bus_comm.dk.ck_nfc_learning_req()
        sleep(2)
        self.bus_comm.dk.send_nfc_learning_resp(5)
        target = func + [f"{execid}"]+[f"ErrCode:5"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # self.tsp.check_digital_key_result(func="NFCLearning",keys=[self.tc_config.get('vid'), execid,"ExecId", "ErrCode"],target_value={"errCode":5})

    @allure.title("远程NFC学卡_学卡失败_相同指令执行中_Convenience")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111943?projectId=46')
    @pytest.mark.full_fail
    def test_caseid_111943(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.nfc_learning() 
        self.bus_comm.dk.ck_nfc_learning_req()
        req_feedback = self.nfc_learning()
        execid = req_feedback["data"]["execId"]
        target = func + [f"{execid}"]+[f"ErrCode:17"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # self.tsp.check_digital_key_result(func="NFCLearning",keys=[self.tc_config.get('vid'), execid,"ExecId", "ErrCode"],target_value={"errCode":17})

    @allure.title("远程NFC学卡_学卡失败_超时_Convenience")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111948?projectId=46')
    @pytest.mark.full_fail
    def test_caseid_111948(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(2)
        req_feedback = self.nfc_learning()
        execid = req_feedback["data"]["execId"]
        sleep(1)
        self.bus_comm.dk.ck_nfc_learning_req()
        target = func + [f"{execid}"]+[f"ErrCode:18"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # sleep(10)
        # self.tsp.check_digital_key_result(func="NFCLearning",keys=[self.tc_config.get('vid'), execid,"ExecId", "ErrCode"],target_value={"errCode":18})

    @allure.title("远程NFC学卡_学卡失败_超时_Driving+GearP")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111949?projectId=46')
    @pytest.mark.full_fail
    def test_caseid_111949(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        sleep(2)
        self.bus_comm.dk.set_chassis_service_gear("GearP")
        sleep(1)
        req_feedback = self.nfc_learning()
        execid = req_feedback["data"]["execId"]
        sleep(1)
        self.bus_comm.dk.ck_nfc_learning_req()
        target = func + [f"{execid}"]+[f"ErrCode:18"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # sleep(10)

        # self.tsp.check_digital_key_result(func="NFCLearning",keys=[self.tc_config.get('vid'), execid,"ExecId", "ErrCode"],target_value={"errCode":18})

    @allure.title("远程NFC学卡_学卡失败_钥匙非本车卡_Convenience")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111939?projectId=46')
    @pytest.mark.full
    def test_caseid_111939(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(2)
        req_feedback = self.nfc_learning()
        execid = req_feedback["data"]["execId"]
        sleep(1)
        self.bus_comm.dk.ck_nfc_learning_req()
        sleep(2)
        self.bus_comm.dk.send_nfc_learning_resp(4)
        target = func + [f"{execid}"]+[f"ErrCode:4"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # todo: 查看云端日志err = 4，errMsg=''，CardID=''
        # self.tsp.check_digital_key_result(func="NFCLearning",keys=[self.tc_config.get('vid'), execid,"ExecId", "ErrCode"],target_value={"errCode":4})

    @allure.title("远程NFC学卡_学卡失败_钥匙非本车卡_Driving+GearP")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111942?projectId=46')
    @pytest.mark.full
    def test_caseid_111942(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        sleep(2)
        self.bus_comm.dk.set_chassis_service_gear("GearP")
        sleep(1)
        req_feedback = self.nfc_learning()
        execid = req_feedback["data"]["execId"]
        sleep(1)
        self.bus_comm.dk.ck_nfc_learning_req()
        sleep(2)
        self.bus_comm.dk.send_nfc_learning_resp(4)
        target = func + [f"{execid}"]+[f"ErrCode:4"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # self.tsp.check_digital_key_result(func="NFCLearning",keys=[self.tc_config.get('vid'), execid,"ExecId", "ErrCode"],target_value={"errCode":4})
        # todo: 查看云端日志err = 4，errMsg=''，CardID=''

    @allure.title("远程NFC学卡_学卡成功_Convenience")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111931?projectId=46')
    @pytest.mark.smoke
    @pytest.mark.s2s_prebuild
    def test_caseid_111931(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(1.5)
        self.bus_comm.dk.empty_dk_data_queue()
        req_feedback = self.nfc_learning()
        execid = req_feedback["data"]["execId"]
        sleep(1)
        self.bus_comm.dk.ck_nfc_learning_req()
        self.bus_comm.dk.send_nfc_learning_resp(0, key_id4)
        target = func + [f"{execid}"]+[f"ErrCode:0"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # self.tsp.check_digital_key_result(func="NFCLearning",keys=[self.tc_config.get('vid'),"NFCLearningUpLinkReq", execid,"ErrCode","ErrMsg","CardId"],target_value={"errCode":0})

    @allure.title("远程NFC学卡_学卡成功_Driving+GearP")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111944?projectId=46')
    @pytest.mark.smoke
    def test_caseid_111944(self):
        # self.bus_comm.dk.set_chassis_service_gear("GearP")
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        sleep(1.5)
        self.bus_comm.dk.empty_dk_data_queue()
        req_feedback = self.nfc_learning()
        execid = req_feedback["data"]["execId"]
        sleep(1)
        self.bus_comm.dk.ck_nfc_learning_req()
        self.bus_comm.dk.send_nfc_learning_resp(0, key_id4)
        target = func + [f"{execid}"]+[f"ErrCode:0"]
        assert self.tsp.check_digital_key_result_log(target_value=target),f'SOC主动同步白名单失败'
        # self.tsp.check_digital_key_result(func="NFCLearning",keys=[self.tc_config.get('vid'),"NFCLearningUpLinkReq", execid,"ErrCode","ErrMsg","CardId"],target_value={"errCode":0})
        # todo: 查看云端日志err = 0，errMsg=''，CardID=000102030405060708090A0B0C0D0E0F

    @allure.title("远程NFC学卡_学卡结果重传机制_BGM掉电不会丢失")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111933?projectId=46')
    @pytest.mark.full
    def test_caseid_111933(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(1.5)
        self.bus_comm.dk.empty_dk_data_queue()
        req_feedback = self.nfc_learning()
        execid = req_feedback["data"]["execId"]
        target = func + [f"{execid}"]+[f"ErrCode:0"]
        sleep(1)
        self.bus_comm.dk.ck_nfc_learning_req()
        # self.nucapp.tcam_power_off()
        self.bus_comm.dk.send_nfc_learning_resp(0, key_id4)
        # 此时云端无上报日志
        # sleep(10)
        self.io.io_reset_bgm()
        sleep(15)  # 等tcam完全起来并恢复与云端通信
        assert self.tsp.check_digital_key_result_log(target_value=target,num=45),f'SOC主动同步白名单失败'
        # self.tsp.check_digital_key_result(func="NFCLearning",keys=[self.tc_config.get('vid'),"NFCLearningUpLinkReq", execid,"ErrCode","ErrMsg","CardId"],target_value={"errCode":0})
    
