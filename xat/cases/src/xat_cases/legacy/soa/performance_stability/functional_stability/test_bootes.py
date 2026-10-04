#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_bootes.py
@Time         :2023/09/20 09:45:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import allure
import pytest
from time import sleep
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check


@allure.feature("中间件测试")
@allure.story("功能测试/注册event是否发送历史数据")
class TestBootes(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([DOOR_SERVICE_CLIENT, 
                                     WTI_SERVICE_CLIENT,
                                     ("DoorService", "client_1")
                                     ])
        sleep(2)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.io.drvr_door_close()
        self.io.pass_door_close()
        self.io.lere_door_close()
        self.io.rire_door_close()
        self.partner.empty_all()

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)

    @allure.title("单个event注册_使用服务端配置_默认发送")
    @pytest.mark.smoke
    def test_caseid_1985093(self):
        self.partner.unregister_event(DOOR_SERVICE_CLIENT)
        self.partner.empty_all(1)

        self.partner.register_event(DOOR_SERVICE_CLIENT, [{"FrntLeftDoorSts": {"history_config":0}}])
        sleep(1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts", {"sts": {"openCloseSts": {"isOpen": 0}}})

    @allure.title("单个event注册_使用服务端配置_配置不发送")
    @pytest.mark.smoke
    def test_caseid_1985094(self):
        self.partner.unregister_event(WTI_SERVICE_CLIENT)
        self.partner.empty_all(1)

        self.partner.register_event(WTI_SERVICE_CLIENT, [{"WarningMsgList": {"history_config":0}}])
        sleep(1)
        assert self.partner.partner_infos[WTI_SERVICE_CLIENT].event_queue.qsize() == 0

    @allure.title("单个event注册_要历史数据")
    @pytest.mark.smoke
    def test_caseid_1985095(self):
        self.partner.unregister_event(DOOR_SERVICE_CLIENT)
        self.partner.empty_all(1)

        self.partner.register_event(DOOR_SERVICE_CLIENT, [{"FrntLeftDoorSts": {"history_config":1}}])
        sleep(1)
        assert self.partner.partner_infos[DOOR_SERVICE_CLIENT].event_queue.qsize() == 1
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts", {"sts": {"openCloseSts": {"isOpen": 0}}})

    @allure.title("单个event注册_不要历史数据")
    @pytest.mark.smoke
    def test_caseid_1985096(self):
        self.partner.unregister_event(DOOR_SERVICE_CLIENT)
        self.partner.empty_all(1)

        self.partner.register_event(DOOR_SERVICE_CLIENT, [{"FrntLeftDoorSts": {"history_config":2}}])
        sleep(1)
        assert self.partner.partner_infos[DOOR_SERVICE_CLIENT].event_queue.qsize()==0

    @allure.title("批量注册_全部使用服务端配置_默认发送")
    @pytest.mark.smoke
    def test_caseid_1985097(self):
        self.partner.unregister_event(DOOR_SERVICE_CLIENT)
        self.partner.empty_all(1)

        self.partner.register_event(DOOR_SERVICE_CLIENT, [{"all": {"history_config":0}}])
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts", {}, timeout=0.2)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntRightDoorSts", {})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearLeftDoorSts", {})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearRightDoorSts", {})

    @allure.title("批量注册_全部使用服务端配置_配置不发送")
    @pytest.mark.smoke
    def test_caseid_1985098(self):
        self.partner.unregister_event(WTI_SERVICE_CLIENT)
        self.partner.empty_all(1)

        self.partner.register_event(WTI_SERVICE_CLIENT, [{"all": {"history_config":0}}])
        assert self.partner.partner_infos[WTI_SERVICE_CLIENT].event_queue.qsize() == 0
    
    @allure.title("批量注册_全部要历史数据")
    @pytest.mark.smoke
    def test_caseid_1985099(self):
        self.partner.unregister_event(DOOR_SERVICE_CLIENT)
        self.partner.empty_all(1)

        self.partner.register_event(DOOR_SERVICE_CLIENT, [{"all": {"history_config":1}}])
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts", {}, timeout=0.2)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntRightDoorSts", {})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearLeftDoorSts", {})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearRightDoorSts", {})

    @allure.title("批量注册_全部不要历史数据")
    @pytest.mark.smoke
    def test_caseid_1985100(self):
        self.partner.unregister_event(DOOR_SERVICE_CLIENT)
        self.partner.empty_all(1)

        self.partner.register_event(DOOR_SERVICE_CLIENT, [{"all": {"history_config":2}}])
        sleep(1)
        assert self.partner.partner_infos[DOOR_SERVICE_CLIENT].event_queue.qsize() == 0

    @allure.title("批量注册_部分接口使用服务端配置、部分接口要历史数据、部分接口不要历史数据")
    @pytest.mark.smoke
    def test_caseid_1985101(self):
        self.partner.unregister_event(DOOR_SERVICE_CLIENT)
        self.partner.empty_all(1)

        self.partner.register_event(DOOR_SERVICE_CLIENT, [{"FrntLeftDoorSts": {"history_config":0}}, 
                                                          {"FrntRightDoorSts": {"history_config":0}},
                                                           {"RearLeftDoorSts": {"history_config":1}},
                                                           {"RearRightDoorSts": {"history_config":2}}])
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts", {}, timeout=0.2)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntRightDoorSts", {})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearLeftDoorSts", {})
        assert self.partner.partner_infos[DOOR_SERVICE_CLIENT].event_queue.qsize() == 0

    @allure.title("单个event反注册")
    @pytest.mark.smoke
    def test_caseid_1985102(self):
        self.partner.register_event(DOOR_SERVICE_CLIENT, [{"all": 0}])
        self.partner.empty_all(1)

        self.partner.unregister_event(DOOR_SERVICE_CLIENT, ["FrntLeftDoorSts"])
        self.io.drvr_door_open()
        self.io.pass_door_open()
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts")
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntRightDoorSts", {"sts": {"openCloseSts": {"isOpen": 1}}}, timeout=0.2)

    @allure.title("批量反注册")
    @pytest.mark.smoke
    def test_caseid_1985103(self):
        self.partner.register_event(DOOR_SERVICE_CLIENT, [{"all": 0}])
        self.partner.empty_all(1)

        self.partner.unregister_event(DOOR_SERVICE_CLIENT, ["FrntLeftDoorSts", "FrntRightDoorSts"])
        self.io.drvr_door_open()
        self.io.pass_door_open()
        self.io.lere_door_open()
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts")
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "FrntRightDoorSts")
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearLeftDoorSts", {"sts": {"openCloseSts": {"isOpen": 1}}}, timeout=0.2)

    @allure.title("client1注册event1需要历史数据，client2注册event1不需要历史数据")
    @pytest.mark.smoke
    def test_caseid_1985104(self):
        self.partner.unregister_event(DOOR_SERVICE_CLIENT, ["all"])
        self.partner.unregister_event("DoorService_client_1", ["all"])
        self.partner.empty_all(1)

        self.partner.register_event(DOOR_SERVICE_CLIENT, [{"FrntLeftDoorSts": {"history_config":1}}])
        self.partner.register_event("DoorService_client_1", [{"FrntLeftDoorSts": {"history_config":2}}])
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts", {}, timeout=0.2)
        self.partner.ck_no_event("DoorService_client_1", "FrntLeftDoorSts")

        self.io.drvr_door_open()
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts", {}, timeout=0.2)
        self.partner.ck_s2s_event("DoorService_client_1", "FrntLeftDoorSts", {}, timeout=0.2)

    @allure.title("重复注册")
    @pytest.mark.smoke
    def test_caseid_1985105(self):
        self.partner.unregister_event(DOOR_SERVICE_CLIENT, ["all"])
        self.partner.empty_all(1)

        self.partner.register_event(DOOR_SERVICE_CLIENT, [{"FrntLeftDoorSts": {"history_config":2}}])
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts")

        self.partner.register_event(DOOR_SERVICE_CLIENT, [{"FrntLeftDoorSts": {"history_config":1}}])
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts")
        
        self.partner.register_event(DOOR_SERVICE_CLIENT, [{"FrntLeftDoorSts": {"history_config":0}}])
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts")
    
    @allure.title("重复反注册")
    @pytest.mark.smoke
    def test_caseid_1985106(self):
        self.partner.register_event(DOOR_SERVICE_CLIENT)
        self.partner.empty_all(1)

        self.partner.unregister_event(DOOR_SERVICE_CLIENT, ["FrntLeftDoorSts"])
        self.partner.unregister_event(DOOR_SERVICE_CLIENT, ["FrntLeftDoorSts"])
        sleep(0.5)
        self.io.drvr_door_open()
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts")

    @allure.title("反注册后重新注册压测_100次")
    @pytest.mark.sanity
    def test_caseid_1985107(self):
        for _ in range(100):
            self.io.drvr_door_close()
            self.partner.unregister_event(DOOR_SERVICE_CLIENT, ["all"])
            self.partner.empty_all(0.1)
            self.partner.register_event(DOOR_SERVICE_CLIENT, [{"FrntLeftDoorSts": {"history_config":1}}])
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts", {}, timeout=0.1)
            self.io.drvr_door_open()
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts", {}, timeout=0.1)
        assert self.partner.partner_infos[DOOR_SERVICE_CLIENT].event_queue.qsize() == 0

