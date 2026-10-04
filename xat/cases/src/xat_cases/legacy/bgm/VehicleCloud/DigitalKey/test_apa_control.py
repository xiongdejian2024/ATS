# -*- coding: utf-8 -*-
"""
@File        : test_rke.py
@Author      : jiabin.zhu@jiduatuo.com
@Time        : 2022/10/23 18:00 PM
@Description : description about this file
@Examples    : example of how to use it
"""
from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass_abc import *


@allure.feature("互联服务")
@allure.story("数字钥匙和账号/其他/APA控制")
class TestDigitalAPAControl(TestDigitalKeyBase):

    @allure.title("APA控制_超时")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/XXXXX?projectId=46')
    @pytest.mark.full
    def test_caseid_109797(self):
        self.soa.send_event_notify("RPAAPAService_server", "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": 3}})
        self.bus_comm.dk.send_apa_cmd(4, "0102030405060708")
        sleep(45)
        self.soa.ck_s2s_req("RPAAPAService_server", "SetPARemoteStatus",
                                {"paReq": 4, "handleUid": 0x0102030405060708})
        self.bus_comm.dk.ck_vehicle_control_resp(6)

    @allure.title("APA控制_成功")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/XXXXX?projectId=46')
    @pytest.mark.smoke
    def test_caseid_109794(self):
        self.soa.send_event_notify("RPAAPAService_server", "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": 3}})
      
        self.bus_comm.dk.send_apa_cmd(4, "0000000000000002")
        sleep(2)
        self.soa.ck_s2s_req("RPAAPAService_server", "SetPARemoteStatus",
                                {"paReq": 4, "handleUid": 2})
        self.soa.send_event_notify("RPAAPAService_server","NotifyPASetResponse", {"paSetResponse": 2})
        self.bus_comm.dk.ck_vehicle_control_resp(0)


    @allure.title("APA控制_失败")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/XXXXX?projectId=46')
    @pytest.mark.full
    def test_caseid_109802(self):
        self.soa.send_event_notify("RPAAPAService_server", "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": 3}})
        self.bus_comm.dk.send_apa_cmd(4, "0102030405060708")
        sleep(2)
        self.soa.ck_s2s_req("RPAAPAService_server", "SetPARemoteStatus",
                                {"paReq": 4, "handleUid": 0x0102030405060708})
        self.soa.send_event_notify("RPAAPAService_server",
                                       "NotifyPASetResponse", {"paSetResponse": 1})
        self.bus_comm.dk.ck_vehicle_control_resp(7)

    @allure.title("APA控制_超时_ACU响应NO_RESPONSE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/XXXXX?projectId=46')
    @pytest.mark.full
    def test_caseid_109809(self):
        self.soa.send_event_notify("RPAAPAService_server", "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": 3}})
        self.bus_comm.dk.send_apa_cmd(4, "0000000000000002")
        sleep(2)
        self.soa.ck_s2s_req("RPAAPAService_server", "SetPARemoteStatus",
                                {"paReq": 4, "handleUid": 2})
        self.soa.send_event_notify("RPAAPAService_server",
                                       "NotifyPASetResponse", {"paSetResponse": 0})
        sleep(3)
        self.bus_comm.dk.ck_bgm_not_send_cmd("BGM不应该发送车控结果报文", self.bus_comm.dk.dk_data_queue_vehicle_control)
        sleep(45)
        self.bus_comm.dk.ck_vehicle_control_resp(6)


