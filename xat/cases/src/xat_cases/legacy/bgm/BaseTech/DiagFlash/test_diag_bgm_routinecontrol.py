#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : test_diag_bgm_full_new.py
@time         : 2023/11/26 14:19
@author       : o_jingyuan.chen@external.jiduauto.com
@description  :
'''

from distutils.command import sdist
from http.client import ResponseNotReady
import os
import sys
from urllib import response
import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.BaseTech.case_helper.test_abc_base import TestABCBase

from xat_ecu.api.abc_interface import *


@allure.feature('BGM BaseTech/诊断功能/基础诊断')
class TestRoutineControlAPP(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        logger.info("before_class")
        with allure.step("初始化环境"):
            self.mix.init_boot_per()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.sd_tester.update_serverdoipid(0x1002)
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x86])
        if recv_data_list[3] == 0x2:
            self.sd_tester.quit_boot()
        self.sd_tester.update_serverdoipid(0x1001)
        self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        logger.info("after_class")
        with allure.step("恢复环境"):
            self.mix.init_boot_per()
        super().after_class(self, ecu)

    # 1000BaseT1以太网测试模式1
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_1000BaseT1 Ethernet Test Mode 1_A051_0x01控制')
    def test_caseid_1981814(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa051, 0x01, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa051, 0x01, SESSION.EXTENDED, UnLock.L0, '', '7f3133')

    # 1000BaseT1以太网测试模式1
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_1000BaseT1 Ethernet Test Mode 1_L5_A051_0x01控制')
    def test_caseid_1981813(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa051, 0x01, SESSION.EXTENDED, UnLock.L5, '', '7101a05110')

    # 1000BaseT1以太网测试模式2
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_1000BaseT1 Ethernet Test Mode 2_A052_0x01控制')
    def test_caseid_1981812(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa052, 0x01, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa052, 0x01, SESSION.EXTENDED, UnLock.L0, '', '7f3133')

    # 1000BaseT1以太网测试模式2
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_1000BaseT1 Ethernet Test Mode 2_L5_A052_0x01控制')
    def test_caseid_1981811(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa052, 0x01, SESSION.EXTENDED, UnLock.L5, '', '7101a05210')

    # 1000BaseT1以太网测试模式4
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_1000BaseT1 Ethernet Test Mode 4_A054_0x01控制')
    def test_caseid_1981810(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa054, 0x01, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa054, 0x01, SESSION.EXTENDED, UnLock.L0, '', '7f3133')

    # 1000BaseT1以太网测试模式4
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_1000BaseT1 Ethernet Test Mode 4_L5_A054_0x01控制')
    def test_caseid_1981809(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa054, 0x01, SESSION.EXTENDED, UnLock.L5, '', '7101a05410')

    # 1000BaseT1以太网测试模式5
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_1000BaseT1 Ethernet Test Mode 5_A055_0x01控制')
    def test_caseid_1981808(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa055, 0x01, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa055, 0x01, SESSION.EXTENDED, UnLock.L0, '', '7f3133')

    # 1000BaseT1以太网测试模式5
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_1000BaseT1 Ethernet Test Mode 5_L5_A055_0x01控制')
    def test_caseid_1981807(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa055, 0x01, SESSION.EXTENDED, UnLock.L5, '', '7101a05510')

    # 1000BaseT1以太网测试模式6
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_1000BaseT1 Ethernet Test Mode 6_A056_0x01控制')
    def test_caseid_1981806(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa056, 0x01, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa056, 0x01, SESSION.EXTENDED, UnLock.L0, '', '7f3133')

    # 1000BaseT1以太网测试模式6
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_1000BaseT1 Ethernet Test Mode 6_L5_A056_0x01控制')
    def test_caseid_1981805(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa056, 0x01, SESSION.EXTENDED, UnLock.L5, '', '7101a05610')

    # 1000BaseT1以太网测试模式7
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_1000BaseT1 Ethernet Test Mode 7_A057_0x01控制')
    def test_caseid_1981804(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa057, 0x01, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa057, 0x01, SESSION.EXTENDED, UnLock.L0, '', '7f3133')

    # 1000BaseT1以太网测试模式7
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_1000BaseT1 Ethernet Test Mode 7_L5_A057_0x01控制')
    def test_caseid_1981803(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa057, 0x01, SESSION.EXTENDED, UnLock.L5, '', '7101a05710')

    # 100BaseT1以太网测试模式1
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_100BaseT1 Ethernet Test Mode 1_A001_0x01控制')
    def test_caseid_1981799(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa001, 0x01, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa001, 0x01, SESSION.EXTENDED, UnLock.L0, '', '7f3133')

    # 100BaseT1以太网测试模式1
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_100BaseT1 Ethernet Test Mode 1_A001_L5_0x01控制')
    def test_caseid_1981798(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa001, 0x01, SESSION.EXTENDED, UnLock.L5, '', '7101a00110')

    # 100BaseT1以太网测试模式2
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_100BaseT1 Ethernet Test Mode 2_A002_0x01控制')
    def test_caseid_1981797(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa002, 0x01, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa002, 0x01, SESSION.EXTENDED, UnLock.L0, '', '7f3133')

    # 100BaseT1以太网测试模式2
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_100BaseT1 Ethernet Test Mode 2_L5_A002_0x01控制')
    def test_caseid_1981796(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa002, 0x01, SESSION.EXTENDED, UnLock.L5, '', '7101a00210')

    # 100BaseT1以太网测试模式4
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_100BaseT1 Ethernet Test Mode 4_A004_0x01控制')
    def test_caseid_1981795(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa004, 0x01, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa004, 0x01, SESSION.EXTENDED, UnLock.L0, '', '7f3133')

    # 100BaseT1以太网测试模式4
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_100BaseT1 Ethernet Test Mode 4_L5_A004_0x01控制')
    def test_caseid_1981794(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa004, 0x01, SESSION.EXTENDED, UnLock.L5, '', '7101a00410')

    # 100BaseT1以太网测试模式5
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_100BaseT1 Ethernet Test Mode 5_A005_0x01控制')
    def test_caseid_1981793(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa005, 0x01, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa005, 0x01, SESSION.EXTENDED, UnLock.L0, '', '7f3133')

    # 100BaseT1以太网测试模式5
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_100BaseT1 Ethernet Test Mode 5_L5_A005_0x01控制')
    def test_caseid_1981792(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa005, 0x01, SESSION.EXTENDED, UnLock.L5, '', '7101a00510')

    # 报警刷新模式
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Alarm Programming Mode_2025_0x01控制')
    def test_caseid_1981836(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2025, 0x01, SESSION.DEFAULT, UnLock.L0, '11', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2025, 0x01, SESSION.EXTENDED, UnLock.L0, '11', '71012025',
                                              check_in=[0x20, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2025, 0x02, SESSION.EMPTY, UnLock.L0, '', '71022025')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2025, 0x03, SESSION.EMPTY, UnLock.L0, '', '71032025')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2025, 0x01, SESSION.EXTENDED, UnLock.L0, '10', '71012025',
                                              check_in=[0x20, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2025, 0x02, SESSION.EMPTY, UnLock.L0, '', '71022025')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2025, 0x03, SESSION.EMPTY, UnLock.L0, '', '71032025')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2025, 0x01, SESSION.EXTENDED, UnLock.L0, '21', '71012025',
                                              check_in=[0x20, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2025, 0x02, SESSION.EMPTY, UnLock.L0, '', '71022025')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2025, 0x03, SESSION.EMPTY, UnLock.L0, '', '71032025')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2025, 0x01, SESSION.EXTENDED, UnLock.L0, '20', '71012025',
                                              check_in=[0x20, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2025, 0x02, SESSION.EMPTY, UnLock.L0, '', '71022025')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2025, 0x03, SESSION.EMPTY, UnLock.L0, '', '71032025')





    # 允许解锁
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Allow Unlocking_2098_0x01控制')
    def test_caseid_1981791(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2098, 0x01, SESSION.DEFAULT, UnLock.L0, '01', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2098, 0x01, SESSION.EMPTY, UnLock.L0, '00', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2098, 0x01, SESSION.EXTENDED, UnLock.L0, '01', '7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2098, 0x01, SESSION.EMPTY, UnLock.L0, '00', '7f3133')

    # 允许解锁
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Allow Unlocking_L11_2098_0x01控制')
    def test_caseid_1981790(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2098, 0x01, SESSION.EXTENDED, UnLock.L11, '00', '71012098')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2098, 0x01, SESSION.EXTENDED, UnLock.L11, '01', '71012098')

    # 氛围灯-LIN5 ALM自动寻址
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)Ambient Light Modules - LIN5 Cluster (ALM) Auto Addressing_20EB_0x01控制')
    def test_caseid_1981828(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x01, SESSION.DEFAULT, UnLock.L0, '', '710120eb',
                                              check_in=[0x20, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x02, SESSION.EMPTY, UnLock.L0, '', '710220eb')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320eb',
                                              check_length=20)
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x01, SESSION.EXTENDED, UnLock.L0, '', '710120eb',
                                              check_in=[0x20, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x02, SESSION.EMPTY, UnLock.L0, '', '710220eb')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320eb',
                                              check_length=20)



    # 氛围灯-LIN5 ALM自动寻址
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Ambient Light Modules - LIN5 Cluster (ALM) Auto Addressing_20EB_0x03控制')
    def test_caseid_1981826(self):
        self.sd_tester.write_ccp({950: 0x01, 636: 0x01, 964: 0x00})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x01, SESSION.DEFAULT, UnLock.L0, '', '710120eb',
                                              check_in=[0x20, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320eb',
                                              check_length=20)
        self.sd_tester.write_ccp({950: 0x01, 636: 0x01, 964: 0x01})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x01, SESSION.DEFAULT, UnLock.L0, '', '710120eb',
                                              check_in=[0x20, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320eb',
                                              check_length=20)
        self.sd_tester.write_ccp({950: 0x01, 636: 0x02, 964: 0x00})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x01, SESSION.DEFAULT, UnLock.L0, '', '710120eb',
                                              check_in=[0x20, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320eb',
                                              check_length=20)
        self.sd_tester.write_ccp({950: 0x01, 636: 0x02, 964: 0x01})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x01, SESSION.DEFAULT, UnLock.L0, '', '710120eb',
                                              check_in=[0x20, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320eb',
                                              check_length=20)
        self.sd_tester.write_ccp({950: 0x02, 636: 0x01, 964: 0x01})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x01, SESSION.DEFAULT, UnLock.L0, '', '710120eb',
                                              check_in=[0x20, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320eb',
                                              check_length=20)
        self.sd_tester.write_ccp({950: 0x02, 636: 0x01, 964: 0x00})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x01, SESSION.DEFAULT, UnLock.L0, '', '710120eb',
                                              check_in=[0x20, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320eb',
                                              check_length=20)
        self.sd_tester.write_ccp({950: 0x02, 636: 0x02, 964: 0x00})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x01, SESSION.DEFAULT, UnLock.L0, '', '710120eb',
                                              check_in=[0x20, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320eb',
                                              check_length=20)
        self.sd_tester.write_ccp({950: 0x02, 636: 0x02, 964: 0x01})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x01, SESSION.DEFAULT, UnLock.L0, '', '710120eb',
                                              check_in=[0x20, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320eb',
                                              check_length=20)
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x03, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 电池传感器请求
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Battery Sensor Request_2022_0x01控制')
    def test_caseid_1981839(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2022, 0x01, SESSION.DEFAULT, UnLock.L0, '00', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2022, 0x01, SESSION.EXTENDED, UnLock.L0, '00', '71012022',
                                              check_in=[0x20, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2022, 0x02, SESSION.EMPTY, UnLock.L0, '', '71022022')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2022, 0x03, SESSION.EMPTY, UnLock.L0, '', '71032022')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2022, 0x01, SESSION.EXTENDED, UnLock.L0, '01', '71012022',
                                              check_in=[0x20, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2022, 0x02, SESSION.EMPTY, UnLock.L0, '', '71022022')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2022, 0x03, SESSION.EMPTY, UnLock.L0, '', '71032022')





    # 亮度进入配置模式氛围灯-LIN5 ALM 01会话回71，03会话回71
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title(
        'UDS_RoutingControl(0x31)_Brightness Adjustment Mode Ambient Light Modules - LIN5 Cluster (ALM)_20F3_0x01控制')
    def test_caseid_1981819(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x01, SESSION.DEFAULT, UnLock.L0, '010a',
                                              '710120f310')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f310')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x01, SESSION.EXTENDED, UnLock.L0, '010a',
                                              '710120f310')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f310')

    # 亮度进入配置模式氛围灯-LIN5 ALM 一直回78pending
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title(
        'UDS_RoutingControl(0x31)_Brightness Adjustment Mode Ambient Light Modules - LIN5 Cluster (ALM)_20F3_0x03控制')
    def test_caseid_1981818(self):
        self.sd_tester.write_ccp({950: 0x01, 636: 0x01, 964: 0x00})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x01, SESSION.DEFAULT, UnLock.L0, '010a',
                                              '710120f310')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f3',
                                              check_length=30)
        self.sd_tester.write_ccp({950: 0x01, 636: 0x01, 964: 0x01})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x01, SESSION.EXTENDED, UnLock.L0, '010a',
                                              '710120f310')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f310',
                                              check_length=30)
        self.sd_tester.write_ccp({950: 0x01, 636: 0x02, 964: 0x00})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x01, SESSION.DEFAULT, UnLock.L0, '010a',
                                              '710120f310')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f3',
                                              check_length=30)
        self.sd_tester.write_ccp({950: 0x01, 636: 0x02, 964: 0x01})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x01, SESSION.EXTENDED, UnLock.L0, '010a',
                                              '710120f310')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f310',
                                              check_length=30)
        self.sd_tester.write_ccp({950: 0x02, 636: 0x01, 964: 0x00})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x01, SESSION.DEFAULT, UnLock.L0, '010a',
                                              '710120f310')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f3',
                                              check_length=30)
        self.sd_tester.write_ccp({950: 0x02, 636: 0x01, 964: 0x01})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x01, SESSION.EXTENDED, UnLock.L0, '010a',
                                              '710120f310')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f310',
                                              check_length=30)
        self.sd_tester.write_ccp({950: 0x02, 636: 0x02, 964: 0x00})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x01, SESSION.DEFAULT, UnLock.L0, '010a',
                                              '710120f310')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f3',
                                              check_length=30)
        self.sd_tester.write_ccp({950: 0x02, 636: 0x02, 964: 0x01})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x01, SESSION.EXTENDED, UnLock.L0, '010a',
                                              '710120f310')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f310',
                                              check_length=30)
        # self.sd_tester.hard_reset(TA.BGM_MCU)
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x03, SESSION.DEFAULT, UnLock.L0, '', '7f3124')
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x03, SESSION.EXTENDED, UnLock.L0, '', '7f3124')
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x03, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 亮度进入配置模式氛围灯-LIN5 ALM 这个根据CCP字节响应的字节长度也不一样
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title(
        'UDS_RoutingControl(0x31)_Brightness Enter Config Mode Ambient Light Modules - LIN5 Cluster (ALM)_20F1_0x01控制')
    def test_caseid_1981825(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x01, SESSION.DEFAULT, UnLock.L0, 'ffff',
                                              '710120f120')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x02, SESSION.EMPTY, UnLock.L0, '', '710220f120')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f1')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x01, SESSION.EXTENDED, UnLock.L0, 'ffff',
                                              '710120f120')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x02, SESSION.EMPTY, UnLock.L0, '', '710220f120')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f1')



    # 亮度进入配置模式氛围灯-LIN5 ALM
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title(
        'UDS_RoutingControl(0x31)_Brightness Enter Config Mode Ambient Light Modules - LIN5 Cluster (ALM)_20F1_0x03控制')
    def test_caseid_1981823(self):
        self.sd_tester.write_ccp({950: 0x01, 636: 0x01, 964: 0x00})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x01, SESSION.DEFAULT, UnLock.L0, 'ffff',
                                              '710120f120')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f1',
                                              check_length=24)
        self.sd_tester.write_ccp({950: 0x01, 636: 0x01, 964: 0x01})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x01, SESSION.EXTENDED, UnLock.L0, 'ffff',
                                              '710120f120')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f1',
                                              check_length=24)
        self.sd_tester.write_ccp({950: 0x01, 636: 0x02, 964: 0x00})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x01, SESSION.DEFAULT, UnLock.L0, 'ffff',
                                              '710120f120')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f1',
                                              check_length=24)
        self.sd_tester.write_ccp({950: 0x01, 636: 0x02, 964: 0x01})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x01, SESSION.EXTENDED, UnLock.L0, 'ffff',
                                              '710120f120')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f1',
                                              check_length=24)
        self.sd_tester.write_ccp({950: 0x02, 636: 0x01, 964: 0x00})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x01, SESSION.DEFAULT, UnLock.L0, 'ffff',
                                              '710120f120')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f1',
                                              check_length=24)
        self.sd_tester.write_ccp({950: 0x02, 636: 0x01, 964: 0x01})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x01, SESSION.EXTENDED, UnLock.L0, 'ffff',
                                              '710120f120')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f1',
                                              check_length=24)
        self.sd_tester.write_ccp({950: 0x02, 636: 0x02, 964: 0x00})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x01, SESSION.DEFAULT, UnLock.L0, 'ffff',
                                              '710120f120')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f1',
                                              check_length=24)
        self.sd_tester.write_ccp({950: 0x02, 636: 0x02, 964: 0x01})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x01, SESSION.EXTENDED, UnLock.L0, 'ffff',
                                              '710120f120')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f1',
                                              check_length=24)
        # self.sd_tester.hard_reset(TA.BGM_MCU)
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x03, SESSION.DEFAULT, UnLock.L0, '', '7f3124')
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x03, SESSION.EXTENDED, UnLock.L0, '', '7f3124')
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x03, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 亮度进入配置模式氛围灯-LIN5 ALM  3103,回710320f1,需求后面要回9个DID，可是需求也只写了8个DID
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title(
        'UDS_RoutingControl(0x31)_Brightness Exit Config Mode Ambient Light Modules - LIN5 Cluster (ALM)_20F2_0x01控制')
    def test_caseid_1981822(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x01, SESSION.DEFAULT, UnLock.L0, '010a',
                                              '710120f220')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x02, SESSION.EMPTY, UnLock.L0, '', '710220f220')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f220')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x01, SESSION.EXTENDED, UnLock.L0, '010a',
                                              '710120f220')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x02, SESSION.EMPTY, UnLock.L0, '', '710220f220')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f220')



    # 亮度进入配置模式氛围灯-LIN5 ALM
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title(
        'UDS_RoutingControl(0x31)_Brightness Exit Config Mode Ambient Light Modules - LIN5 Cluster (ALM)_20F2_0x03控制')
    def test_caseid_1981820(self):
        self.sd_tester.write_ccp({950: 0x01, 636: 0x01, 964: 0x00})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x01, SESSION.DEFAULT, UnLock.L0, '010a', '710120f2',
                                              check_in=[0x20, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f2',
                                              check_length=24)
        self.sd_tester.write_ccp({950: 0x01, 636: 0x01, 964: 0x01})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x01, SESSION.EXTENDED, UnLock.L0, '010a',
                                              '710120f220')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f2',
                                              check_length=24)
        self.sd_tester.write_ccp({950: 0x01, 636: 0x02, 964: 0x00})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x01, SESSION.DEFAULT, UnLock.L0, '010a', '710120f2',
                                              check_in=[0x20, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f2',
                                              check_length=24)
        self.sd_tester.write_ccp({950: 0x01, 636: 0x02, 964: 0x01})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x01, SESSION.EXTENDED, UnLock.L0, '010a',
                                              '710120f220')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f2',
                                              check_length=24)
        self.sd_tester.write_ccp({950: 0x02, 636: 0x01, 964: 0x00})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x01, SESSION.DEFAULT, UnLock.L0, '010a', '710120f2',
                                              check_in=[0x20, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f2',
                                              check_length=24)
        self.sd_tester.write_ccp({950: 0x02, 636: 0x01, 964: 0x01})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x01, SESSION.EXTENDED, UnLock.L0, '010a',
                                              '710120f220')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f2',
                                              check_length=24)
        self.sd_tester.write_ccp({950: 0x02, 636: 0x02, 964: 0x00})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x01, SESSION.DEFAULT, UnLock.L0, '010a', '710120f2',
                                              check_in=[0x20, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f2',
                                              check_length=24)
        self.sd_tester.write_ccp({950: 0x02, 636: 0x02, 964: 0x01})
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x01, SESSION.EXTENDED, UnLock.L0, '010a',
                                              '710120f220')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x03, SESSION.EMPTY, UnLock.L0, '', '710320f2',
                                              check_length=24)
        # self.sd_tester.hard_reset(TA.BGM_MCU)
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x03, SESSION.DEFAULT, UnLock.L0, '', '7f3124')
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x03, SESSION.EXTENDED, UnLock.L0, '', '7f3124')
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x03, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 充电口盖标定
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Calibarte ChargeLid_2031_0x01控制')
    def test_caseid_1981801(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2031, 0x01, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2031, 0x01, SESSION.EXTENDED, UnLock.L0, '', '7101203110')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2031, 0x03, SESSION.EMPTY, UnLock.L0, '', '7103203110')



    # 取消FOTA任务
    # BGM_SOC
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_CancelFOTATask_A102')
    def test_caseid_1981866(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa102, 0x01, SESSION.DEFAULT, UnLock.L0, '', '7101a1021000')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa102, 0x01, SESSION.EXTENDED, UnLock.L0, '', '7101a1021000')

    # 证书写入
    # BGM_SOC
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Certificate install_8020')
    def test_caseid_1981868(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x8020, 0x01, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x8020, 0x01, SESSION.EXTENDED, UnLock.L0, '', '7f3133')

    # 证书写入
    # BGM_SOC
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Certificate install_L7_8020')
    def test_caseid_1981867(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x8020, 0x01, SESSION.EXTENDED, UnLock.L7, f'{"0" * 4098}',
                                              '71018020', check_length=12)

    # 充电口盖打开/关闭
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_ChargeLid Open/Close_2030_0x01控制')
    def test_caseid_1981802(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2030, 0x01, SESSION.DEFAULT, UnLock.L0, '00', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2030, 0x01, SESSION.EXTENDED, UnLock.L0, '01', '7101203010')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2030, 0x01, SESSION.EXTENDED, UnLock.L0, '00', '7101203010')

    # 检查完整兼容性
    # BGM_SOC,BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Check Complete & Compatible_0205')
    def test_caseid_1981876(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0205, 0x01, SESSION.DEFAULT, UnLock.L0, '','7f3131')

        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0205, 0x01, SESSION.DEFAULT, UnLock.L0, '','7f3131')

        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0205, 0x01, SESSION.EXTENDED, UnLock.L0, '','7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0205, 0x01, SESSION.EXTENDED, UnLock.L0, '', '7f3131')



    # 检查存储器
    # BGM_SOC,BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_check memory_0212')
    def test_caseid_1981874(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0212, 0x01, SESSION.DEFAULT, UnLock.L0,
                                              f'{"0" * 512}', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0212, 0x01, SESSION.DEFAULT, UnLock.L0,
                                              f'{"0" * 512}', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0212, 0x01, SESSION.EXTENDED, UnLock.L0,f'{"0" * 512}', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0212, 0x01, SESSION.EXTENDED, UnLock.L0, f'{"0" * 512}',
                                              '7f3131')



    # 检查刷写先决条件
    # BGM_SOC,BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Check programming pre-conditions_0206')
    def test_caseid_1981877(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0206, 0x01, SESSION.DEFAULT, UnLock.L0, '','71010206')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0206, 0x01, SESSION.DEFAULT, UnLock.L0, '', '71010206')


        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0206, 0x01, SESSION.EXTENDED, UnLock.L0, '','71010206')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0206, 0x01, SESSION.EXTENDED, UnLock.L0, '', '71010206')

    # #滑行模式
    # #BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Coast mode Open/close_2030')
    def test_caseid_1981865(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2030, 0x01, SESSION.DEFAULT, UnLock.L0, '01', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2030, 0x01, SESSION.EMPTY, UnLock.L0, '00', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2030, 0x01, SESSION.EXTENDED, UnLock.L0, '01', '7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2030, 0x01, SESSION.EMPTY, UnLock.L0, '00', '7f3133')

    # #滑行模式
    # #BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Coast mode Open/close_L5_2030')
    def test_caseid_1981864(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2030, 0x01, SESSION.EXTENDED, UnLock.L5, '01', '7101203020')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2030, 0x01, SESSION.EXTENDED, UnLock.L5, '00', '7101203020')

    # #控制普通氛围灯灯带（ALM1-ALM8）的颜色（Red、Green、Blue）和亮度（Brightness）
    # #BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Control all ALMs_2040')
    def test_caseid_1981863(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2040, 0x01, SESSION.DEFAULT, UnLock.L0,
                                              '80ffffff7fffffff7fffffff7fffffff7fffffff7fffffff7fffffff7fffffff',
                                              '7f3131')  # 无效值
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2040, 0x01, SESSION.EMPTY, UnLock.L0,
                                              '0000000000000000000000000000000000000000000000000000000000000000',
                                              '7f3131')  # 最小值
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2040, 0x01, SESSION.EMPTY, UnLock.L0,
                                              '7fffffff7fffffff7fffffff7fffffff7fffffff7fffffff7fffffff7fffffff',
                                              '7f3131')  # 边界值
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2040, 0x01, SESSION.EMPTY, UnLock.L0,
                                              '2233441100000000000000000000000000000000000000000000000011223344',
                                              '7f3131')  # 边界值
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2040, 0x01, SESSION.EXTENDED, UnLock.L0,
                                              '80ffffff7fffffff7fffffff7fffffff7fffffff7fffffff7fffffff7fffffff',
                                              '7f3133')  # 有效值
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2040, 0x01, SESSION.EMPTY, UnLock.L0,
                                              '0000000000000000000000000000000000000000000000000000000000000000',
                                              '7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2040, 0x01, SESSION.EMPTY, UnLock.L0,
                                              '7fffffff7fffffff7fffffff7fffffff7fffffff7fffffff7fffffff7fffffff',
                                              '7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2040, 0x01, SESSION.EMPTY, UnLock.L0,
                                              '2233441100000000000000000000000000000000000000000000000011223344',
                                              '7f3133')  # 边界值

    # #控制普通氛围灯灯带（ALM1-ALM8）的颜色（Red、Green、Blue）和亮度（Brightness）
    # #BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Control all ALMs_L5_2040')
    def test_caseid_1981862(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2040, 0x01, SESSION.EXTENDED, UnLock.L5,
                                              '80ffffff7fffffff7fffffff7fffffff7fffffff7fffffff7fffffff7fffffff',
                                              '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2040, 0x01, SESSION.EXTENDED, UnLock.L5,
                                              '0000000000000000000000000000000000000000000000000000000000000000',
                                              '71012040', check_in=[0x10, 0x11, 0x12])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2040, 0x01, SESSION.EXTENDED, UnLock.L5,
                                              '7fffffff7fffffff7fffffff7fffffff7fffffff7fffffff7fffffff7fffffff',
                                              '71012040', check_in=[0x10, 0x11, 0x12])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2040, 0x01, SESSION.EXTENDED, UnLock.L5,
                                              '2233441100000000000000000000000000000000000000000000000011223344',
                                              '71012040', check_in=[0x10, 0x11, 0x12])

    # #控制智能氛围灯灯带（SALM1-SALM6）的颜色（Red、Green、Blue）和亮度（Brightness）
    # #BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Control all SALMs_2041')
    def test_caseid_1981861(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2041, 0x01, SESSION.DEFAULT, UnLock.L0, f'{"7f" * 816}',
                                              '7f3131')  # 边界值
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2041, 0x01, SESSION.EMPTY, UnLock.L0, f'80{"7f" * 815}',
                                              '7f3131')  # 无效值
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2041, 0x01, SESSION.EMPTY, UnLock.L0,
                                              f'{"01020304112233440000000000000000" * 25}0102030411223344000000000000',
                                              '7f3131')  # 最小值
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2041, 0x01, SESSION.EXTENDED, UnLock.L0, f'{"7f" * 816}',
                                              '7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2041, 0x01, SESSION.EMPTY, UnLock.L0, f'80{"7f" * 815}',
                                              '7f3133')  # 无效值
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2041, 0x01, SESSION.EMPTY, UnLock.L0,
                                              f'{"01020304112233440000000000000000" * 25}0102030411223344000000000000',
                                              '7f3133')  # 最小值

    # 控制智能氛围灯灯带（SALM1-SALM6）的颜色（Red、Green、Blue）和亮度（Brightness）
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Control all SALMs_L5_2041')
    def test_caseid_1981860(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2041, 0x01, SESSION.EXTENDED, UnLock.L5, f'{"7f" * 816}',
                                              '71012041', check_in=[0x10, 0x11, 0x12])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2041, 0x01, SESSION.EMPTY, UnLock.L0, f'80{"7f" * 815}',
                                              '7f3131')  # 无效值
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2041, 0x01, SESSION.EMPTY, UnLock.L0,
                                              f'{"01020304112233440000000000000000" * 51}', '71012041',
                                              check_in=[0x10, 0x11, 0x12])  # 最小值

    # 控制OBD防火墙的状态
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Control OBD Firewall status_A040')
    def test_caseid_1981859(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa040, 0x01, SESSION.DEFAULT, UnLock.L0, '02ff', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa040, 0x01, SESSION.EXTENDED, UnLock.L0, '02ff', '7f3133')

    # 控制OBD防火墙的状态
    # BGM_SOC
    @pytest.mark.sanity
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Control OBD Firewall status_L7_A040')
    def test_caseid_1981858(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa040, 0x01, SESSION.EXTENDED, UnLock.L7, '0100', '7101a040')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa040, 0x01, SESSION.EXTENDED, UnLock.L7, '0200', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa040, 0x01, SESSION.EXTENDED, UnLock.L7, '02ff', '7101a040')

    # #BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_enable SSH_A041')
    def test_caseid_1981849(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa041, 0x01, SESSION.DEFAULT, UnLock.L0, '02', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa041, 0x01, SESSION.EXTENDED, UnLock.L0, '02', '7f3133')

    # #BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_enable SSH_A041_L7')
    def test_caseid_1981848(self):
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa041,0x01,SESSION.EXTENDED,UnLock.L7,'02','7101a041',check_in=[0x10,0x11,0x12])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa041, 0x01, SESSION.EXTENDED, UnLock.L7, '01', '7101a041',
                                              check_in=[0x10, 0x11, 0x12])

    # 擦除存储器
    # BGM_SOC,BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Erase Memory_FF00')
    def test_caseid_1981872(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xff00, 0x01, SESSION.DEFAULT, UnLock.L0,
                                              '0000000000000000', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xff00, 0x01, SESSION.DEFAULT, UnLock.L0,
                                              '0000000000000000', '7f3131')

        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xff00, 0x01, SESSION.EXTENDED, UnLock.L0,
                                              '0000000000000000', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xff00, 0x01, SESSION.EXTENDED, UnLock.L0,
                                              '0000000000000000', '7f3131')



    # 危险警报灯激活
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Hazard Lights Activation_2066_0x01控制')
    def test_caseid_1981833(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2066, 0x01, SESSION.DEFAULT, UnLock.L0, '00', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2066, 0x01, SESSION.EXTENDED, UnLock.L0, '01', '71012066',
                                              check_in=[0x30, 0x31, 0x32])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2066, 0x02, SESSION.EMPTY, UnLock.L0, '', '71022066')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2066, 0x03, SESSION.EMPTY, UnLock.L0, '', '71032066')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2066, 0x01, SESSION.EXTENDED, UnLock.L0, '00', '71012066',
                                              check_in=[0x30, 0x31, 0x32])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2066, 0x02, SESSION.EMPTY, UnLock.L0, '', '71022066')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2066, 0x03, SESSION.EMPTY, UnLock.L0, '', '71032066')





    # AWM初始化学习
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_initilize AWM_2013 _0x01控制')
    def test_caseid_1981816(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2013, 0x01, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2013, 0x01, SESSION.EXTENDED, UnLock.L0, '', '7101201310')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2013, 0x03, SESSION.EMPTY, UnLock.L0, '', '71032013',
                                              check_in=[0x1002, 0x1000])



    # 总线通信控制
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_NetworkCommunicationControl_A101_0x01控制')
    def test_caseid_1981817(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa101, 0x01, SESSION.DEFAULT, UnLock.L0, '0fff',
                                              '7101a1011000')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa101, 0x01, SESSION.EXTENDED, UnLock.L0, '0fff',
                                              '7101a1011000')

    # 私有锁禁用
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Private Locking Deactivation_2015_0x01控制')
    def test_caseid_1981842(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2015, 0x01, SESSION.DEFAULT, UnLock.L0, '00', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2015, 0x01, SESSION.EXTENDED, UnLock.L0, '01', '71012015',
                                              check_in=[0x20, 0x22, 0x21])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2015, 0x02, SESSION.EMPTY, UnLock.L0, '', '71022015')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2015, 0x03, SESSION.EMPTY, UnLock.L0, '', '71032015')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2015, 0x01, SESSION.EXTENDED, UnLock.L0, '00', '71012015',
                                              check_in=[0x20, 0x22, 0x21])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2015, 0x02, SESSION.EMPTY, UnLock.L0, '', '71022015')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2015, 0x03, SESSION.EMPTY, UnLock.L0, '', '71032015')




    # 复位使用模式扩展统计
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Reset Usage Mode Extention Statistics_2071_0x01控制')
    def test_caseid_1981830(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2071, 0x01, SESSION.DEFAULT, UnLock.L0, 'ffffff', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2071, 0x01, SESSION.EXTENDED, UnLock.L0, 'ffffff',
                                              '71012071', check_in=[0x10, 0x11, 0x12])

    # 复位使用模式时间统计
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Reset Usage Mode Time Statistics_2072_0x01控制')
    def test_caseid_1981829(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2072, 0x01, SESSION.DEFAULT, UnLock.L0, 'ff01', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2072, 0x01, SESSION.EXTENDED, UnLock.L0, 'ff01', '71012072',
                                              check_in=[0x10, 0x11, 0x12])

    # 方向盘加热指令
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Steering Wheel Heating Command_200C_0x01控制')
    def test_caseid_1981845(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x200c, 0x01, SESSION.DEFAULT, UnLock.L0, '00', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x200c, 0x01, SESSION.EXTENDED, UnLock.L0, '01', '7101200c',
                                              check_in=[0x20, 0x22, 0x21])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x200c, 0x02, SESSION.EMPTY, UnLock.L0, '', '7102200c')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x200c, 0x03, SESSION.EMPTY, UnLock.L0, '', '7103200c')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x200c, 0x01, SESSION.EXTENDED, UnLock.L0, '02', '7101200c',
                                              check_in=[0x20, 0x22, 0x21])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x200c, 0x02, SESSION.EMPTY, UnLock.L0, '', '7102200c')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x200c, 0x03, SESSION.EMPTY, UnLock.L0, '', '7103200c')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x200c, 0x01, SESSION.EXTENDED, UnLock.L0, '03', '7101200c',
                                              check_in=[0x20, 0x22, 0x21])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x200c, 0x02, SESSION.EMPTY, UnLock.L0, '', '7102200c')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x200c, 0x03, SESSION.EMPTY, UnLock.L0, '', '7103200c')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x200c, 0x01, SESSION.EXTENDED, UnLock.L0, '00', '7101200c',
                                              check_in=[0x20, 0x22, 0x21])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x200c, 0x02, SESSION.EMPTY, UnLock.L0, '', '7102200c')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x200c, 0x03, SESSION.EMPTY, UnLock.L0, '', '7103200c')





    # 传输keyinfo
    # BGM_SOC
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Transfer Key Info_0208')
    def test_caseid_1981870(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0208, 0x01, SESSION.DEFAULT, UnLock.L0, f'{"0" * 688}',
                                              '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0208, 0x01, SESSION.EXTENDED, UnLock.L0, f'{"0" * 688}',
                                              '7f3131')



    # 读取私有ECU零部件/序列号
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Read Private ECUs Part/serial Numbers_0208')
    def test_caseid_1985908(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0208, 0x01, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0208, 0x01, SESSION.EXTENDED, UnLock.L0, '', '71010208',
                                              check_in=[0x20, 0x21, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0208, 0x02, SESSION.EXTENDED, UnLock.L0, '', '71020208')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0208, 0x03, SESSION.EXTENDED, UnLock.L0, '', '71030208')

    # 上传日志
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_upload LOG_EA1D')
    def test_caseid_1981847(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xea1d, 0x01, SESSION.DEFAULT, UnLock.L0, '01', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xea1d, 0x01, SESSION.EXTENDED, UnLock.L0, '01', '7f3133')

    # 上传日志
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_upload LOG_EA1D_L5')
    def test_caseid_1981846(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xea1d, 0x01, SESSION.EXTENDED, UnLock.L5, '01', '7101ea1d',
                                              check_in=[0x10, 0x11, 0x12])

    # 上传SOA service 埋点数据
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_upload SOA service data tracking record_EA29_0x01控制')
    def test_caseid_1981853(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xea29, 0x01, SESSION.DEFAULT, UnLock.L0,
                                              '687474703A2F2F3136392E3235342E302E31323A38303830', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xea29, 0x01, SESSION.EXTENDED, UnLock.L0,
                                              '687474703A2F2F3136392E3235342E302E31323A38303830', '7f3133')

    # 上传SOA service 埋点数据
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_upload SOA service data tracking record_EA29_0x02控制')
    def test_caseid_1981851(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xea29, 0x02, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xea29, 0x02, SESSION.EXTENDED, UnLock.L0, '', '7f3133')

    # 上传SOA service 埋点数据
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_upload SOA service data tracking record_L5_EA29_0x01控制')
    def test_caseid_1981852(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xea29, 0x01, SESSION.EXTENDED, UnLock.L5,
                                              '687474703A2F2F3136392E3235342E302E31323A38303830', '7101ea29',
                                              check_in=[0x20, 0x21, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xea29, 0x02, SESSION.EXTENDED, UnLock.L5, '', '7102ea29')
        # self.sd_tester.reset_0x1181()
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xea29,0x02,SESSION.EXTENDED,UnLock.L5,'','7f3124')


    # 上传埋点数据
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_upload vehicle data tracking record_EA28_0x01控制')
    def test_caseid_1981857(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xea28, 0x01, SESSION.DEFAULT, UnLock.L0,
                                              '687474703A2F2F3136392E3235342E302E31323A38303830', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xea28, 0x01, SESSION.EXTENDED, UnLock.L0,
                                              '687474703A2F2F3136392E3235342E302E31323A38303830', '7f3133')

    # 上传埋点数据
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_upload vehicle data tracking record_EA28_0x02控制')
    def test_caseid_1981855(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xea28, 0x02, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xea28, 0x02, SESSION.EXTENDED, UnLock.L0, '', '7f3133')

    # 上传埋点数据
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_upload vehicle data tracking record_L5_EA28_0x01控制')
    def test_caseid_1981856(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xea28, 0x01, SESSION.EXTENDED, UnLock.L5,
                                              '687474703A2F2F3136392E3235342E302E31323A38303830', '7101ea28',
                                              check_in=[0x20, 0x21, 0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xea28, 0x02, SESSION.EXTENDED, UnLock.L5, '', '7102ea28')


    # 环境切换清数据
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Clear Data for env change_2100_0x01控制')
    def test_caseid_1984747(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2100, 0x01, SESSION.DEFAULT, UnLock.L0, '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2100, 0x01, SESSION.EXTENDED, UnLock.L0, '7f3133')

    # 环境切换清数据
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Clear Data for env change_L5_2100_0x01控制')
    def test_caseid_1984746(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2100, 0x01, SESSION.EXTENDED, UnLock.L5, '', '71012100',
                                              check_in=[0x1000, 0x1100, 0x1200, 0x1001, 0x1101, 0x1201])

@allure.feature('BGM BaseTech/诊断功能/基础诊断')
class TestRoutineControlHardResetMCU(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        logger.info("before_class")
        with allure.step("初始化环境"):
            self.mix.init_boot_per()

        self.sd_tester.hard_reset(TA.BGM_MCU)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # self.sd_tester.update_serverdoipid(0x1002)
        # err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x86])
        # if recv_data_list[3] == 0x2:
        #     self.sd_tester.quit_boot()
        # self.sd_tester.update_serverdoipid(0x1001)
        # self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        logger.info("after_class")
        with allure.step("恢复环境"):
            self.mix.init_boot_per()
        super().after_class(self, ecu)


    # 方向盘加热指令
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Steering Wheel Heating Command_200C_0x03控制')
    def test_caseid_1981843(self):

        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x200c, 0x03, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x200c, 0x03, SESSION.EXTENDED, UnLock.L0, '', '7f3124')

    # 方向盘加热指令
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Steering Wheel Heating Command_200C_0x02控制')
    def test_caseid_1981844(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x200c, 0x02, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x200c, 0x02, SESSION.EXTENDED, UnLock.L0, '', '7f3124')

    # 私有锁禁用 上下电后回正响应
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Private Locking Deactivation_2015_0x02控制')
    def test_caseid_1981841(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2015, 0x02, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2015, 0x02, SESSION.EXTENDED, UnLock.L0, '', '7f3124')

    # AWM初始化学习
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_initilize AWM_2013 _0x03控制')
    def test_caseid_1981815(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2013, 0x03, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2013, 0x03, SESSION.EXTENDED, UnLock.L0, '', '7f3124')

    # 充电口盖标定
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Calibarte ChargeLid_2031 _0x03控制')
    def test_caseid_1981800(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2031, 0x03, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2031, 0x03, SESSION.EXTENDED, UnLock.L0, '', '7f3124')


    # 亮度进入配置模式氛围灯-LIN5 ALM
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title(
        'UDS_RoutingControl(0x31)_Brightness Exit Config Mode Ambient Light Modules - LIN5 Cluster (ALM)_20F2_0x02控制')
    def test_caseid_1981821(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x02, SESSION.DEFAULT, UnLock.L0, '', '7f3124')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x02, SESSION.EXTENDED, UnLock.L0, '', '7f3124')


    # 亮度进入配置模式氛围灯-LIN5 ALM
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title(
        'UDS_RoutingControl(0x31)_Brightness Enter Config Mode Ambient Light Modules - LIN5 Cluster (ALM)_20F1_0x02控制')
    def test_caseid_1981824(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x02, SESSION.DEFAULT, UnLock.L0, '', '7f3124')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x02, SESSION.EXTENDED, UnLock.L0, '', '7f3124')


    # 电池传感器请求
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Battery Sensor Request_2022_0x03控制')
    def test_caseid_1981837(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2022, 0x03, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2022, 0x03, SESSION.EXTENDED, UnLock.L0, '', '7f3124')

    # 电池传感器请求
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Battery Sensor Request_2022_0x02控制')
    def test_caseid_1981838(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2022, 0x02, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2022, 0x02, SESSION.EXTENDED, UnLock.L0, '', '7f3124')



    # 私有锁禁用
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Private Locking Deactivation_2015_0x03控制')
    def test_caseid_1981840(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2015, 0x03, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2015, 0x03, SESSION.EXTENDED, UnLock.L0, '', '7f3124')

    # 危险警报灯激活
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Hazard Lights Activation_2066_0x03控制')
    def test_caseid_1981831(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2066, 0x03, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2066, 0x03, SESSION.EXTENDED, UnLock.L0, '', '7f3124')

    # 危险警报灯激活
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Hazard Lights Activation_2066_0x02控制')
    def test_caseid_1981832(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2066, 0x02, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2066, 0x02, SESSION.EXTENDED, UnLock.L0, '', '7f3124')

    # 报警刷新模式
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Alarm Programming Mode_2025_0x03控制')
    def test_caseid_1981834(self):
        # self.io.io_reset_bgm(times=10)
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU,0x2025,0x01,SESSION.EXTENDED,UnLock.L0,'10','71012025',check_in=[0x20,0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2025, 0x03, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2025, 0x03, SESSION.EXTENDED, UnLock.L0, '', '7f3124')

    # 报警刷新模式  重新上下电后，还是回正响应
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Alarm Programming Mode_2025_0x02控制')
    def test_caseid_1981835(self):
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU,0x2025,0x01,SESSION.EXTENDED,UnLock.L0,'10','71012025',check_in=[0x20,0x22])
        # self.sd_tester.hard_reset(TA.BGM_MCU)
        # self.io.io_reset_bgm(times=10)
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2025, 0x02, SESSION.DEFAULT, UnLock.L0, '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2025, 0x02, SESSION.EXTENDED, UnLock.L0, '',
                                              '7f3124')  # 有问题


    # 亮度进入配置模式氛围灯-LIN5 ALM
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title(
        'UDS_RoutingControl(0x31)_Brightness Enter Config Mode Ambient Light Modules - LIN5 Cluster (ALM)_20F1_0x03控制')
    def test_caseid_1981823_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x03, SESSION.DEFAULT, UnLock.L0, '', '7f3124')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x03, SESSION.EXTENDED, UnLock.L0, '', '7f3124')

    # 亮度进入配置模式氛围灯-LIN5 ALM
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title(
        'UDS_RoutingControl(0x31)_Brightness Exit Config Mode Ambient Light Modules - LIN5 Cluster (ALM)_20F2_0x03控制')
    def test_caseid_1981820_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x03, SESSION.DEFAULT, UnLock.L0, '', '7f3124')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x03, SESSION.EXTENDED, UnLock.L0, '', '7f3124')

    # 亮度进入配置模式氛围灯-LIN5 ALM 一直回78pending
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title(
        'UDS_RoutingControl(0x31)_Brightness Adjustment Mode Ambient Light Modules - LIN5 Cluster (ALM)_20F3_0x03控制')
    def test_caseid_1981818_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x03, SESSION.DEFAULT, UnLock.L0, '', '7f3124')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x03, SESSION.EXTENDED, UnLock.L0, '', '7f3124')

# 禁止开车
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_inhibit drive car_L5_A105_0x01控制')
    def test_caseid_1994867(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa105, 0x01, SESSION.EXTENDED, UnLock.L5, '01', '7101a10510')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa105, 0x01, SESSION.EXTENDED, UnLock.L5, '00', '7101a10510')
        
# 整车FOTA模式
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Vehicle FOTA Mode_A100_0x01控制')
    def test_caseid_1994868(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa100, 0x01, SESSION.EXTENDED, UnLock.L0, '01', '7101a1001000')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa100, 0x01, SESSION.EXTENDED, UnLock.L0, '02', '7101a1001000')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa100, 0x01, SESSION.DEFAULT, UnLock.L0, '01', '7101a1001000')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa100, 0x01, SESSION.DEFAULT, UnLock.L0, '02', '7101a1001000')
        
@allure.feature('BGM BaseTech/诊断功能/基础诊断')
class TestRoutineControlHardResetMPU(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        logger.info("before_class")
        with allure.step("初始化环境"):
            self.mix.init_boot_per()
        self.sd_tester.hard_reset(TA.BGM_SOC)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # self.sd_tester.update_serverdoipid(0x1002)
        # err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x86])
        # if recv_data_list[3] == 0x2:
        #     self.sd_tester.quit_boot()
        # self.sd_tester.update_serverdoipid(0x1001)
        # self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        logger.info("after_class")
        with allure.step("恢复环境"):
            self.mix.init_boot_per()
        super().after_class(self, ecu)

    # 上传埋点数据
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_upload vehicle data tracking record_L5_EA28_0x02控制')
    def test_caseid_1981854(self):

        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xea28, 0x02, SESSION.EXTENDED, UnLock.L5, '', '7102ea2821')

    # 上传SOA service 埋点数据
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_upload SOA service data tracking record_L5_EA29_0x02控制')
    def test_caseid_1981850(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xea29, 0x02, SESSION.EXTENDED, UnLock.L5, '', '7102ea2921')
        
@allure.feature('BGM BaseTech/诊断功能/基础诊断')
class TestRoutineControlBootHardResetMCU(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        logger.info("before_class")
        with allure.step("初始化环境"):
            self.mix.init_boot_per()

        self.sd_tester.hard_reset(TA.BGM_MCU)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.enter_boot()
        self.sd_tester.update_serverdoipid(0x1001)
        self.sd_tester.send_request_and_recv_response([0x10, 0x02], recv=[0x50, 0x02])
        self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x86], recv=[0x62, 0xf1, 0x86, 0x02])


    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        logger.info("after_class")
        # with allure.step("恢复环境"):
        #     self.mix.init_boot_per()
        super().after_class(self, ecu)
        self.sd_tester.exit_muc_boot()
        # 退出boot

    # 私有锁禁用
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Private Locking Deactivation_2015_0x03控制')
    def test_caseid_1981840_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2015, 0x03, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 危险警报灯激活
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Hazard Lights Activation_2066_0x03控制')
    def test_caseid_1981831_00(self):

        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2066, 0x03, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 危险警报灯激活
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Hazard Lights Activation_2066_0x02控制')
    def test_caseid_1981832_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2066, 0x02, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')


    # 报警刷新模式
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Alarm Programming Mode_2025_0x03控制')
    def test_caseid_1981834_00(self):
        # self.io.io_reset_bgm(times=10)
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU,0x2025,0x01,SESSION.EXTENDED,UnLock.L0,'10','71012025',check_in=[0x20,0x22])
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2025, 0x03, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 报警刷新模式  重新上下电后，还是回正响应
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Alarm Programming Mode_2025_0x02控制')
    def test_caseid_1981835_00(self):
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU,0x2025,0x01,SESSION.EXTENDED,UnLock.L0,'10','71012025',check_in=[0x20,0x22])
        # self.sd_tester.hard_reset(TA.BGM_MCU)
        # self.io.io_reset_bgm(times=10)
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2025, 0x02, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 亮度进入配置模式氛围灯-LIN5 ALM
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title(
        'UDS_RoutingControl(0x31)_Brightness Enter Config Mode Ambient Light Modules - LIN5 Cluster (ALM)_20F1_0x03控制')
    def test_caseid_1981823_01(self):

        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x03, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')


    # 亮度进入配置模式氛围灯-LIN5 ALM
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title(
        'UDS_RoutingControl(0x31)_Brightness Exit Config Mode Ambient Light Modules - LIN5 Cluster (ALM)_20F2_0x03控制')
    def test_caseid_1981820_01(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x03, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 亮度进入配置模式氛围灯-LIN5 ALM 一直回78pending
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title(
        'UDS_RoutingControl(0x31)_Brightness Adjustment Mode Ambient Light Modules - LIN5 Cluster (ALM)_20F3_0x03控制')
    def test_caseid_1981818_01(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x03, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

@allure.feature('BGM BaseTech/诊断功能/基础诊断')
class TestRoutineControlBoot(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        logger.info("before_class")
        with allure.step("初始化环境"):
            self.mix.init_boot_per()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.enter_boot()
        self.sd_tester.update_serverdoipid(0x1001)
        self.sd_tester.send_request_and_recv_response([0x10, 0x02], recv=[0x50, 0x02])
        self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x86], recv=[0x62, 0xf1, 0x86, 0x02])


    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        logger.info("after_class")
        # with allure.step("恢复环境"):
        #     self.mix.init_boot_per()
        super().after_class(self, ecu)
        self.sd_tester.exit_muc_boot()
        # 退出boot

    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_1000BaseT1 Ethernet Test Mode 1_A051_0x01控制')
    def test_caseid_1981814_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa051, 0x01, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 1000BaseT1以太网测试模式2
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_1000BaseT1 Ethernet Test Mode 2_A052_0x01控制')
    def test_caseid_1981812_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa052, 0x01, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 1000BaseT1以太网测试模式4
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_1000BaseT1 Ethernet Test Mode 4_A054_0x01控制')
    def test_caseid_1981810_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa054, 0x01, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 1000BaseT1以太网测试模式5
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_1000BaseT1 Ethernet Test Mode 5_A055_0x01控制')
    def test_caseid_1981808_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa055, 0x01, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 1000BaseT1以太网测试模式6
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_1000BaseT1 Ethernet Test Mode 6_A056_0x01控制')
    def test_caseid_1981806_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa056, 0x01, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 1000BaseT1以太网测试模式7
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_1000BaseT1 Ethernet Test Mode 7_A057_0x01控制')
    def test_caseid_1981804_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa057, 0x01, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 100BaseT1以太网测试模式1
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_100BaseT1 Ethernet Test Mode 1_A001_0x01控制')
    def test_caseid_1981799_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa001, 0x01, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 100BaseT1以太网测试模式2
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_100BaseT1 Ethernet Test Mode 2_A002_0x01控制')
    def test_caseid_1981797_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa002, 0x01, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 100BaseT1以太网测试模式4
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_100BaseT1 Ethernet Test Mode 4_A004_0x01控制')
    def test_caseid_1981795_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa004, 0x01, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 100BaseT1以太网测试模式5
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_100BaseT1 Ethernet Test Mode 5_A005_0x01控制')
    def test_caseid_1981793_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa005, 0x01, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 报警刷新模式
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Alarm Programming Mode_2025_0x01控制')
    def test_caseid_1981836_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2025, 0x01, SESSION.PROGRAMMING, UnLock.L0, '11', '7f3131')

    # 允许解锁
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Allow Unlocking_2098_0x01控制')
    def test_caseid_1981791_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2098, 0x01, SESSION.PROGRAMMING, UnLock.L0, '01', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2098, 0x01, SESSION.EMPTY, UnLock.L0, '00', '7f3131')

    # 氛围灯-LIN5 ALM自动寻址
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)Ambient Light Modules - LIN5 Cluster (ALM) Auto Addressing_20EB_0x01控制')
    def test_caseid_1981828_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x01, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 电池传感器请求
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Battery Sensor Request_2022_0x01控制')
    def test_caseid_1981839_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2022, 0x01, SESSION.PROGRAMMING, UnLock.L0, '00', '7f3131')

    # 电池传感器请求
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Battery Sensor Request_2022_0x02控制')
    def test_caseid_1981838_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2022, 0x02, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 电池传感器请求
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Battery Sensor Request_2022_0x03控制')
    def test_caseid_1981837_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2022, 0x03, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 亮度进入配置模式氛围灯-LIN5 ALM 01会话回71，03会话回71
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title(
        'UDS_RoutingControl(0x31)_Brightness Adjustment Mode Ambient Light Modules - LIN5 Cluster (ALM)_20F3_0x01控制')
    def test_caseid_1981819_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f3, 0x01, SESSION.PROGRAMMING, UnLock.L0, '010a',
                                              '7f3131')

    # 亮度进入配置模式氛围灯-LIN5 ALM 这个根据CCP字节响应的字节长度也不一样
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title(
        'UDS_RoutingControl(0x31)_Brightness Enter Config Mode Ambient Light Modules - LIN5 Cluster (ALM)_20F1_0x01控制')
    def test_caseid_1981825_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x01, SESSION.PROGRAMMING, UnLock.L0, 'ffff',
                                              '7f3131')

    # 亮度进入配置模式氛围灯-LIN5 ALM
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title(
        'UDS_RoutingControl(0x31)_Brightness Enter Config Mode Ambient Light Modules - LIN5 Cluster (ALM)_20F1_0x02控制')
    def test_caseid_1981824_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f1, 0x02, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title(
        'UDS_RoutingControl(0x31)_Brightness Exit Config Mode Ambient Light Modules - LIN5 Cluster (ALM)_20F2_0x01控制')
    def test_caseid_1981822_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x01, SESSION.PROGRAMMING, UnLock.L0, '010a',
                                              '7f3131')

    # 亮度进入配置模式氛围灯-LIN5 ALM
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title(
        'UDS_RoutingControl(0x31)_Brightness Exit Config Mode Ambient Light Modules - LIN5 Cluster (ALM)_20F2_0x02控制')
    def test_caseid_1981821_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20f2, 0x02, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 充电口盖标定
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Calibarte ChargeLid_2031_0x01控制')
    def test_caseid_1981801_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2031, 0x01, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 充电口盖标定
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Calibarte ChargeLid_2031 _0x03控制')
    def test_caseid_1981800_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2031, 0x03, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 取消FOTA任务
    # BGM_SOC
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_CancelFOTATask_A102')
    def test_caseid_1981866_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa102, 0x01, SESSION.PROGRAMMING, UnLock.L0, '',
                                              '7101a1021100')
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.DEFAULT,'62f18601')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa102, 0x01, SESSION.PROGRAMMING, UnLock.L0, '',
                                              '7101a1021000')

    # 证书写入
    # BGM_SOC
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Certificate install_8020')
    def test_caseid_1981868_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x8020, 0x01, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 充电口盖打开/关闭
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_ChargeLid Open/Close_2030_0x01控制')
    def test_caseid_1981802_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2030, 0x01, SESSION.PROGRAMMING, UnLock.L0, '00', '7f3131')

    # 检查完整兼容性
    # BGM_SOC,BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Check Complete & Compatible_0205')
    def test_caseid_1981876_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0205, 0x01, SESSION.PROGRAMMING, UnLock.L0,'', '7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0205, 0x01, SESSION.PROGRAMMING, UnLock.L0, '', '7f3133')

    # 检查存储器
    # BGM_SOC,BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_check memory_0212')
    def test_caseid_1981874_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0212, 0x01, SESSION.PROGRAMMING, UnLock.L0,
                                              f'{"0" * 512}', '7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0212, 0x01, SESSION.PROGRAMMING, UnLock.L0,
                                              f'{"0" * 512}', '7f3133')

    # 检查刷写先决条件
    # BGM_SOC,BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Check programming pre-conditions_0206')
    def test_caseid_1981877_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0206, 0x01, SESSION.PROGRAMMING, UnLock.L0,
                                              '', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0206, 0x01, SESSION.PROGRAMMING, UnLock.L0,
                                              '', '7f3131')

    # #滑行模式
    # #BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Coast mode Open/close_2030')
    def test_caseid_1981865_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2030, 0x01, SESSION.PROGRAMMING, UnLock.L0, '01', '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2030, 0x01, SESSION.EMPTY, UnLock.L0, '00', '7f3131')

    # #控制普通氛围灯灯带（ALM1-ALM8）的颜色（Red、Green、Blue）和亮度（Brightness）
    # #BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Control all ALMs_2040')
    def test_caseid_1981863_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2040, 0x01, SESSION.PROGRAMMING, UnLock.L0,
                                              '80ffffff7fffffff7fffffff7fffffff7fffffff7fffffff7fffffff7fffffff',
                                              '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2040, 0x01, SESSION.EMPTY, UnLock.L0,
                                              '0000000000000000000000000000000000000000000000000000000000000000',
                                              '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2040, 0x01, SESSION.EMPTY, UnLock.L0,
                                              '7fffffff7fffffff7fffffff7fffffff7fffffff7fffffff7fffffff7fffffff',
                                              '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2040, 0x01, SESSION.EMPTY, UnLock.L0,
                                              '2233441100000000000000000000000000000000000000000000000011223344',
                                              '7f3131')  # 边界值

    # #控制智能氛围灯灯带（SALM1-SALM6）的颜色（Red、Green、Blue）和亮度（Brightness）
    # #BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Control all SALMs_2041')
    def test_caseid_1981861_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2041, 0x01, SESSION.PROGRAMMING, UnLock.L0, f'{"7f" * 816}',
                                              '7f3131')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2041, 0x01, SESSION.EMPTY, UnLock.L0, f'80{"7f" * 815}',
                                              '7f3131')  # 无效值
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2041, 0x01, SESSION.EMPTY, UnLock.L0,
                                              f'{"01020304112233440000000000000000" * 25}0102030411223344000000000000',
                                              '7f3131')  # 最小值

    # 控制OBD防火墙的状态
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Control OBD Firewall status_A040')
    def test_caseid_1981859_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa040, 0x01, SESSION.PROGRAMMING, UnLock.L0, '02ff',
                                              '7f3131')

    # #BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_enable SSH_A041')
    def test_caseid_1981849_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa041, 0x01, SESSION.PROGRAMMING, UnLock.L0, '02', '7f3131')

    # 擦除存储器
    # BGM_SOC,BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Erase Memory_FF00')
    def test_caseid_1981872_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xff00, 0x01, SESSION.PROGRAMMING, UnLock.L0,
                                              '0000000000000000', '7f3133')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xff00, 0x01, SESSION.PROGRAMMING, UnLock.L0,
                                              '0000000000000000', '7f3133')

    # 危险警报灯激活
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Hazard Lights Activation_2066_0x01控制')
    def test_caseid_1981833_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2066, 0x01, SESSION.PROGRAMMING, UnLock.L0, '00', '7f3131')

    # AWM初始化学习
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_initilize AWM_2013 _0x01控制')
    def test_caseid_1981816_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2013, 0x01, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # AWM初始化学习
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_initilize AWM_2013 _0x03控制')
    def test_caseid_1981815_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2013, 0x03, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 总线通信控制
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_NetworkCommunicationControl_A101_0x01控制')
    def test_caseid_1981817_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xa101, 0x01, SESSION.PROGRAMMING, UnLock.L0, '0fff',
                                              '7f3131')

    # 私有锁禁用
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Private Locking Deactivation_2015_0x01控制')
    def test_caseid_1981842_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2015, 0x01, SESSION.PROGRAMMING, UnLock.L0, '00', '7f3131')

    # 私有锁禁用 上下电后回正响应
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Private Locking Deactivation_2015_0x02控制')
    def test_caseid_1981841_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2015, 0x02, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 复位使用模式扩展统计
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Reset Usage Mode Extention Statistics_2071_0x01控制')
    def test_caseid_1981830_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2071, 0x01, SESSION.PROGRAMMING, UnLock.L0, 'ffffff',
                                              '7f3131')

    # 复位使用模式时间统计
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Reset Usage Mode Time Statistics_2072_0x01控制')
    def test_caseid_1981829_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x2072, 0x01, SESSION.PROGRAMMING, UnLock.L0, 'ff01',
                                              '7f3131')

    # 方向盘加热指令
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Steering Wheel Heating Command_200C_0x01控制')
    def test_caseid_1981845_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x200c, 0x01, SESSION.PROGRAMMING, UnLock.L0, '00', '7f3131')

    # 方向盘加热指令
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Steering Wheel Heating Command_200C_0x02控制')
    def test_caseid_1981844_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x200c, 0x02, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 方向盘加热指令
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Steering Wheel Heating Command_200C_0x03控制')
    def test_caseid_1981843_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x200c, 0x03, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 传输keyinfo
    # BGM_SOC
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Transfer Key Info_0208')
    def test_caseid_1981870_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0208, 0x01, SESSION.PROGRAMMING, UnLock.L0, f'{"0" * 688}',
                                              '7f3133')

    # 读取私有ECU零部件/序列号
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Read Private ECUs Part/serial Numbers_0208')
    def test_caseid_1985908_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0208, 0x01, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 上传日志
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_upload LOG_EA1D')
    def test_caseid_1981847_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xea1d, 0x01, SESSION.PROGRAMMING, UnLock.L0, '01', '7f3131')

    # 上传SOA service 埋点数据
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_upload SOA service data tracking record_EA29_0x01控制')
    def test_caseid_1981853_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xea29, 0x01, SESSION.PROGRAMMING, UnLock.L0,
                                              '687474703A2F2F3136392E3235342E302E31323A38303830', '7f3131')

    # 上传SOA service 埋点数据
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_upload SOA service data tracking record_EA29_0x02控制')
    def test_caseid_1981851_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xea29, 0x02, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 上传埋点数据
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_upload vehicle data tracking record_EA28_0x01控制')
    def test_caseid_1981857_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xea28, 0x01, SESSION.PROGRAMMING, UnLock.L0,
                                              '687474703A2F2F3136392E3235342E302E31323A38303830', '7f3131')

    # 上传埋点数据
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_upload vehicle data tracking record_EA28_0x02控制')
    def test_caseid_1981855_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xea28, 0x02, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')

    # 环境切换清数据
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Clear Data for env change_2100_0x01控制')
    def test_caseid_1984747_00(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x2100, 0x01, SESSION.PROGRAMMING, UnLock.L0, '7f3131')

    # 擦除存储器
    # BGM_SOC,BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Erase Memory_L1_FF00')
    def test_caseid_1981871(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xff00, 0x01, SESSION.PROGRAMMING, UnLock.L1, '0000000000000000',
                                              '7101ff00')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0xff00, 0x01, SESSION.PROGRAMMING, UnLock.L1, '0000000000000000',
                                              '7f3131')


    # 传输keyinfo
    # BGM_SOC
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Transfer Key Info_L1_0208')
    def test_caseid_1981869(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0208, 0x01, SESSION.PROGRAMMING, UnLock.L1, f'{"0" * 688}',
                                              '71010208')


    # 检查存储器
    # BGM_SOC,BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_check memory_L1_0212')
    def test_caseid_1981873(self):
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0x0212,0x01,SESSION.EMPTY,UnLock.L1,f'{"0" * 512}','7f3122')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0212, 0x01, SESSION.PROGRAMMING, UnLock.L1, f'{"0" * 512}',
                                              '71010212')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0212, 0x01, SESSION.PROGRAMMING, UnLock.L1, f'{"0" * 512}',
                                              '71010212')


    # 检查存储器
    # BGM_SOC,BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_check memory_L1_0212')
    def test_caseid_1981873(self):
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0x0212,0x01,SESSION.EMPTY,UnLock.L1,f'{"0" * 512}','7f3122')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0212, 0x01, SESSION.PROGRAMMING, UnLock.L1, f'{"0" * 512}',
                                              '71010212')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0212, 0x01, SESSION.PROGRAMMING, UnLock.L1, f'{"0" * 512}',
                                              '71010212')


    # 检查存储器
    # BGM_SOC,BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_check memory_L1_0212')
    def test_caseid_1981873(self):
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0x0212,0x01,SESSION.EMPTY,UnLock.L1,f'{"0" * 512}','7f3122')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0212, 0x01, SESSION.PROGRAMMING, UnLock.L1, f'{"0" * 512}',
                                              '71010212')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0212, 0x01, SESSION.PROGRAMMING, UnLock.L1, f'{"0" * 512}',
                                              '71010212')

    # 检查完整兼容性
    # BGM_SOC,BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Check Complete & Compatible_L1_0205')
    def test_caseid_1981875(self):
        # self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0x0205,0x01,SESSION.EMPTY,UnLock.L1,'','7f3122')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0208, 0x01, SESSION.PROGRAMMING, UnLock.L1, f'{"0" * 688}',
                                              '71010208')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0x0205, 0x01, SESSION.PROGRAMMING, write_data='',
                                              check_data='71010205')
        # #self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU,0x0205,0x01,SESSION.EMPTY,UnLock.L1,'','7f3122')
        # #self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0x0208,0x01,SESSION.EMPTY,UnLock.L0,f'{"0" * 688}','71010208')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x0205, 0x01, SESSION.PROGRAMMING, UnLock.L1, write_data='',
                                              check_data='71010205')


    # 氛围灯-LIN5 ALM自动寻址
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断RoutineControl-New')
    @allure.title('UDS_RoutingControl(0x31)_Ambient Light Modules - LIN5 Cluster (ALM) Auto Addressing_20EB_0x02控制')
    def test_caseid_1981827(self):
        #     self.sd_tester.hard_reset(TA.BGM_MCU)
        #     self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU,0x20eb,0x02,SESSION.DEFAULT,UnLock.L0,'','7f3124')
        #     self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU,0x20eb,0x02,SESSION.EXTENDED,UnLock.L0,'','7f3124')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0x20eb, 0x02, SESSION.PROGRAMMING, UnLock.L0, '', '7f3131')


#pytest BaseTech/DiagFlash/test_diag_bgm_routinecontrol.py::TestRoutineControlBoot::test_caseid_1981866_00