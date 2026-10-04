#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : test_diag_bgm_full_new.py
@time         : 2023/11/26 14:19
@author       : o_jingyuan.chen@external.jiduauto.com
@description  : 
'''


import pytest
import allure
from xat_cases.legacy.bgm.BaseTech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature('BGM BaseTech/诊断功能')
class TestIOControlApp(TestABCBase):
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

    # 后挡风玻璃加热器控制#1（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)Rear Windscreen Heater Control #1_EF99_0x00控制')
    def test_caseid_1981726(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xef99, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xef99, 0x00, SESSION.EXTENDED, UnLock.L0, '', '6fef9900',
                                         check_method=Check_Method.response, recover=False)

    # 控制WMM激活前洗涤（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Activation of Washer Front Safe_420A _0x03控制')
    def test_caseid_1981777(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x420a, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x420a, 0x03, SESSION.EXTENDED, UnLock.L0, '01', '62420a01')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x420a, 0x03, SESSION.EXTENDED, UnLock.L0, '02', '62420a02')

    # 控制WMM激活前洗涤（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Activation of Washer Front Safe_420A_0x00控制')
    def test_caseid_1981776(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x420a, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x420a, 0x00, SESSION.EXTENDED, UnLock.L0, '', '6f420a00',
                                         check_method=Check_Method.response, recover=False)

    # 电池可用Delta电源信号输出状态（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Available Delta Power signal output_40E2_0x00控制')
    def test_caseid_1981788(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x40e2, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x40e2, 0x00, SESSION.EXTENDED, UnLock.L0, '', '6f40e200',
                                         check_method=Check_Method.response, recover=False)

    # 电池可用Delta电源信号输出状态（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Available Delta Power signal output_40E2_0x03控制')  # 测试边界值7FFF
    def test_caseid_1981789(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x40e2, 0x03, SESSION.DEFAULT, UnLock.L0, '7fff', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x40e2, 0x03, SESSION.EXTENDED, UnLock.L0, '7fff', '6240e27fff')

    # B柱左侧门开按钮背光控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_B pillar left door opening button backlight control_4212_0x00控制')
    def test_caseid_1981723(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4212, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4212, 0x00, SESSION.EXTENDED, UnLock.L0, '', '7f2f33',
                                         check_method=Check_Method.response, recover=False)

    # B柱左侧门开按钮背光控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_B pillar left door opening button backlight control_4212_L5_0x00控制')
    def test_caseid_1981722(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4212, 0x00, SESSION.EXTENDED, UnLock.L5, '', '6f421200',
                                         check_method=Check_Method.response, recover=False)

    # B柱左侧门开按钮背光控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_B pillar left door opening button backlight control_4212_0x03控制')
    def test_caseid_1981725(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4212, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4212, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '7f2f33',
                                         check_method=Check_Method.response, recover=False)

    # B柱左侧门开按钮背光控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_B pillar left door opening button backlight control_4212_L5_0x03控制')
    def test_caseid_1981724(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4212, 0x03, SESSION.EXTENDED, UnLock.L5, '00', '62421200')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4212, 0x03, SESSION.EXTENDED, UnLock.L5, '01', '62421201')

    # B柱右侧门开按钮背光控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_B pillar Right door opening button backlight control_4222_0x00控制')
    def test_caseid_1981711(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4222, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4222, 0x00, SESSION.EXTENDED, UnLock.L0, '', '7f2f33',
                                         check_method=Check_Method.response, recover=False)

    # B柱右侧门开按钮背光控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_B pillar Right door opening button backlight control_4222_0x03控制')
    def test_caseid_1981713(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4222, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4222, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '7f2f33',
                                         check_method=Check_Method.response, recover=False)

    # B柱右侧门开按钮背光控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_B pillar Right door opening button backlight control_4222_L5_0x00控制')
    def test_caseid_1981710(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4222, 0x00, SESSION.EXTENDED, UnLock.L5, '', '6f422200',
                                         check_method=Check_Method.response, recover=False)

    # B柱右侧门开按钮背光控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_B pillar Right door opening button backlight control_4222_L5_0x03控制')
    def test_caseid_1981712(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4222, 0x03, SESSION.EXTENDED, UnLock.L5, '00', '62422200')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4222, 0x03, SESSION.EXTENDED, UnLock.L5, '01', '62422201')

    # C柱左侧门开按钮背光控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_C pillar left door opening button backlight control_4213_0x00控制')
    def test_caseid_1981719(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4213, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4213, 0x00, SESSION.EXTENDED, UnLock.L0, '', '7f2f33',
                                         check_method=Check_Method.response, recover=False)

    # C柱左侧门开按钮背光控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_C pillar left door opening button backlight control_4213_L5_0x00控制')
    def test_caseid_1981718(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4213, 0x00, SESSION.EXTENDED, UnLock.L5, '', '6f421300',
                                         check_method=Check_Method.response, recover=False)

    # C柱左侧门开按钮背光控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_C pillar left door opening button backlight control_4213_0x03控制')
    def test_caseid_1981721(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4213, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4213, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '7f2f33',
                                         check_method=Check_Method.response, recover=False)

    # C柱左侧门开按钮背光控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_C pillar left door opening button backlight control_4213_L5_0x03控制')
    def test_caseid_1981720(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4213, 0x03, SESSION.EXTENDED, UnLock.L5, '00', '62421300')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4213, 0x03, SESSION.EXTENDED, UnLock.L5, '01', '62421301')

    # C柱右侧门开按钮背光控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_C pillar Right door opening button backlight control_4223_0x00控制')
    def test_caseid_1981707(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4223, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4223, 0x00, SESSION.EXTENDED, UnLock.L0, '', '7f2f33',
                                         check_method=Check_Method.response, recover=False)

    # C柱右侧门开按钮背光控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_C pillar Right door opening button backlight control_4223_0x03控制')
    def test_caseid_1981709(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4223, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4223, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '7f2f33',
                                         check_method=Check_Method.response, recover=False)

    # C柱右侧门开按钮背光控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_C pillar Right door opening button backlight control_4223_L5_0x00控制')
    def test_caseid_1981706(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4223, 0x00, SESSION.EXTENDED, UnLock.L5, '', '6f422300',
                                         check_method=Check_Method.response, recover=False)

    # C柱右侧门开按钮背光控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_C pillar Right door opening button backlight control_4223_L5_0x03控制')
    def test_caseid_1981708(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4223, 0x03, SESSION.EXTENDED, UnLock.L5, '00', '62422300')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4223, 0x03, SESSION.EXTENDED, UnLock.L5, '01', '62422301')

    # 车辆模式（APP）
    # BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Car Mode_D134_0x00控制')
    def test_caseid_1981741(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xd134, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xd134, 0x00, SESSION.EXTENDED, UnLock.L0, '', '7f2f33',
                                         check_method=Check_Method.response, recover=False)

    # 车辆模式（APP）
    # BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Car Mode_D134_0x03控制')
    def test_caseid_1981743(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xd134, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xd134, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '7f2f33',
                                         check_method=Check_Method.response, recover=False)

    # 车辆模式（APP）
    # BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Car Mode_D134_L11_0x03控制')
    def test_caseid_1981737(self):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        # self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xd134, 0x03, SESSION.EXTENDED, UnLock.L11, '00', '62d13400',
                                         recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xd134, 0x03, SESSION.EMPTY, UnLock.L0, '01', '62d13401',
                                         recover=False)
        # 在03会话安全访问L11下，2F 03控制车辆模式变为其他状态，最后默认2F 00 归还DID IO控制权
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xd134, 0x03, SESSION.EMPTY, UnLock.L0, '02', '62d13402',
                                         recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xd134, 0x03, SESSION.EMPTY, UnLock.L0, '03', '62d13403',
                                         recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xd134, 0x03, SESSION.EMPTY, UnLock.L0, '05', '62d13405')

    # 车辆模式（APP）
    # BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Car Mode_D134_L11_0x00控制')
    def test_caseid_1981736(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xd134, 0x00, SESSION.EXTENDED, UnLock.L11, '', '6fd13400',
                                         check_method=Check_Method.response, recover=False)

    # 车辆模式（APP）
    # BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Car Mode_D134_L3_0x03控制')
    def test_caseid_1981739(self):
        # self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xd134, 0x03, SESSION.EXTENDED, UnLock.L3, '00', '62d13400')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xd134, 0x03, SESSION.EMPTY, UnLock.L0, '01', '62d13401')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xd134, 0x03, SESSION.EMPTY, UnLock.L0, '02', '62d13402')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xd134, 0x03, SESSION.EMPTY, UnLock.L0, '03', '62d13403')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xd134, 0x03, SESSION.EMPTY, UnLock.L0, '05', '62d13405')

    # 车辆模式（APP）
    # BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Car Mode_D134_L3_0x00控制')
    def test_caseid_1981738(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xd134, 0x00, SESSION.EXTENDED, UnLock.L3, '', '6fd13400',
                                         check_method=Check_Method.response, recover=False)

    # 车辆模式（APP）
    # BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Car Mode_D134_L5_0x03控制')
    def test_caseid_1981742(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xd134, 0x03, SESSION.EXTENDED, UnLock.L5, '00', '62d13400')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xd134, 0x03, SESSION.EMPTY, UnLock.L0, '01', '62d13401')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xd134, 0x03, SESSION.EMPTY, UnLock.L0, '02', '62d13402')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xd134, 0x03, SESSION.EMPTY, UnLock.L0, '03', '62d13403')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xd134, 0x03, SESSION.EMPTY, UnLock.L0, '05', '62d13405')

    # 车辆模式（APP）
    # BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Car Mode_D134_L5_0x00控制')
    def test_caseid_1981740(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xd134, 0x00, SESSION.EXTENDED, UnLock.L5, '', '6fd13400',
                                         check_method=Check_Method.response, recover=False)

    # ECM唤醒控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_ECM Wake Up Control_4253_0x00控制')
    def test_caseid_1981766(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4253, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4253, 0x00, SESSION.EXTENDED, UnLock.L0, '', '6f425300',
                                         check_method=Check_Method.response, recover=False)

    # ECM唤醒控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_ECM Wake Up Control_4253_0x03控制')
    def test_caseid_1981767(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4253, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4253, 0x03, SESSION.EXTENDED, UnLock.L0, '01', '62425301')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4253, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '62425300')

    # 低压能量等级替代（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Energy Level Electric Substitution_429D_0x00控制')
    def test_caseid_1981762(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x429d, 0x00, SESSION.DEFAULT, UnLock.L0, '80', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x429d, 0x00, SESSION.EXTENDED, UnLock.L0, '80', '6f429d00',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x429d, 0x00, SESSION.EXTENDED, UnLock.L0, '40', '6f429d00',
                                         check_method=Check_Method.response, recover=False)

    # 低压能量等级替代（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Energy Level Electric Substitution_429D_0x03控制')
    def test_caseid_1981763(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x429d, 0x03, SESSION.DEFAULT, UnLock.L0, 'ff40', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x429d, 0x03, SESSION.EXTENDED, UnLock.L0, 'ff40', '62429dff',
                                         recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x429d, 0x00, SESSION.EXTENDED, UnLock.L0, '80', '6f429d00',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x429d, 0x00, SESSION.EXTENDED, UnLock.L0, '40', '6f429d00',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x429d, 0x03, SESSION.EXTENDED, UnLock.L0, 'f080', '62429df0',
                                         recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x429d, 0x00, SESSION.EXTENDED, UnLock.L0, '80', '6f429d00',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x429d, 0x00, SESSION.EXTENDED, UnLock.L0, '40', '6f429d00',
                                         check_method=Check_Method.response, recover=False)

    # 外灯控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Exterior Lights Control_7022_0x00控制')
    def test_caseid_1981744(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x7022, 0x00, SESSION.DEFAULT, UnLock.L0, '800000', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x7022, 0x00, SESSION.EXTENDED, UnLock.L0, '800000', '6f702200',
                                         check_method=Check_Method.response, recover=False)

    # 外灯控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Exterior Lights Control_7022_0x03控制')
    def test_caseid_1981745(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x7022, 0x03, SESSION.DEFAULT, UnLock.L0, '800000800000', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x7022, 0x03, SESSION.EXTENDED, UnLock.L0, '800000800000',
                                         '62702280', recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x7022, 0x00, SESSION.EXTENDED, UnLock.L0, '800000', '6f702200',
                                         check_method=Check_Method.response, recover=False)

    # 摄像头三角区域加热（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Front Camera Defrost Control_4256_0x00控制')
    def test_caseid_1981702(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4256, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4256, 0x00, SESSION.EXTENDED, UnLock.L0, '', '6f425600',
                                         check_method=Check_Method.response, recover=False)

    # 摄像头三角区域加热（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Front Camera Defrost Control_4256_0x03控制')
    def test_caseid_1981703(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4256, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4256, 0x03, SESSION.EXTENDED, UnLock.L0, '01', '62425601')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4256, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '62425600')

    # 高位刹车灯控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_High Mounted Stop Lamp control_4221_0x00控制')
    def test_caseid_1981714(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4221, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4221, 0x00, SESSION.EXTENDED, UnLock.L0, '', '6f422100',
                                         check_method=Check_Method.response, recover=False)

    # 高位刹车灯控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_High Mounted Stop Lamp control_4221_0x03控制')
    def test_caseid_1981715(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4221, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4221, 0x03, SESSION.EXTENDED, UnLock.L0, '01', '62422101')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4221, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '62422100')

    # 喇叭控制（APP）
    # BGM _MCU
    @pytest.mark.sanity
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Horn Control_41F2 _0x03控制')
    def test_caseid_1981779(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x41f2, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x41f2, 0x03, SESSION.EXTENDED, UnLock.L0, '01', '6241f201')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x41f2, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '6241f200')

    # 喇叭控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Horn Control_41F2_0x00控制')
    def test_caseid_1981778(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x41f2, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x41f2, 0x00, SESSION.EXTENDED, UnLock.L0, '', '6f41f200',
                                         check_method=Check_Method.response, recover=False)

    # 内灯控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_InteriorLight_41E5 _0x00控制')
    def test_caseid_1981784(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x41e5, 0x00, SESSION.DEFAULT, UnLock.L0, '80', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x41e5, 0x00, SESSION.EXTENDED, UnLock.L0, '80', '6f41e500',
                                         check_method=Check_Method.response, recover=False)

    # 内灯控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_InteriorLight_41E5 _0x03控制')
    def test_caseid_1981785(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x41e5, 0x03, SESSION.DEFAULT, UnLock.L0, '64000000000080',
                                         '7f2f7f', check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x41e5, 0x03, SESSION.EXTENDED, UnLock.L0, '64000000000080',
                                         '6241e564', recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x41e5, 0x00, SESSION.EXTENDED, UnLock.L0, '80', '6f41e500',
                                         check_method=Check_Method.response, recover=False)

    # 左右牌照灯（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_License Plate light Control_4217_0x00控制')
    def test_caseid_1981704(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4217, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4217, 0x00, SESSION.EXTENDED, UnLock.L0, '', '6f421700',
                                         check_method=Check_Method.response, recover=False)

    # 左右牌照灯（APP）
    # BGM _MCU
    @pytest.mark.sanity
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_License Plate light Control_4217_0x03控制')
    def test_caseid_1981705(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4217, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4217, 0x03, SESSION.EXTENDED, UnLock.L0, '01', '62421701')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4217, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '62421700')

    # 低压功率等级替代（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Power Level Electric Substitution_429E_0x00控制')
    def test_caseid_1981760(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x429e, 0x00, SESSION.DEFAULT, UnLock.L0, '80', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x429e, 0x00, SESSION.EXTENDED, UnLock.L0, '80', '6f429e00',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x429e, 0x00, SESSION.EXTENDED, UnLock.L0, '40', '6f429e00',
                                         check_method=Check_Method.response, recover=False)

    # 低压功率等级替代（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Power Level Electric Substitution_429E_0x03控制')
    def test_caseid_1981761(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x429e, 0x03, SESSION.DEFAULT, UnLock.L0, 'f080', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x429e, 0x03, SESSION.EXTENDED, UnLock.L0, 'f080', '62429ef0',
                                         recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x429e, 0x00, SESSION.EXTENDED, UnLock.L0, '80', '6f429e00',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x429e, 0x00, SESSION.EXTENDED, UnLock.L0, '40', '6f429e00',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x429e, 0x03, SESSION.EXTENDED, UnLock.L0, 'ff40', '62429eff',
                                         recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x429e, 0x00, SESSION.EXTENDED, UnLock.L0, '80', '6f429e00',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x429e, 0x00, SESSION.EXTENDED, UnLock.L0, '40', '6f429e00',
                                         check_method=Check_Method.response, recover=False)

    # 车辆电源插口控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Power Outlet Control_4110 _0x00控制')
    def test_caseid_1981786(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4110, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4110, 0x00, SESSION.EXTENDED, UnLock.L0, '', '6f411000',
                                         check_method=Check_Method.response, recover=False)

    # 车辆电源插口控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Power Outlet Control_4110 _0x03控制')
    def test_caseid_1981787(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4110, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4110, 0x03, SESSION.EXTENDED, UnLock.L0, '01', '62411001')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4110, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '62411000')

    # ECM唤醒控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Private Unlock Supply Control_4260_0x00控制')
    def test_caseid_1981764(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4260, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4260, 0x00, SESSION.EXTENDED, UnLock.L0, '', '6f426000',
                                         check_method=Check_Method.response, recover=False)

    # ECM唤醒控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Private Unlock Supply Control_4260_0x03控制')
    def test_caseid_1981765(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4260, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4260, 0x03, SESSION.EXTENDED, UnLock.L0, '01', '62426001')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4260, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '62426000')

    # 雨量传感器重新采用（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Rain Sensor ReAdaption_43B8_0x00控制')
    def test_caseid_1981746(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x43b8, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x43b8, 0x00, SESSION.EXTENDED, UnLock.L0, '', '6f43b800',
                                         check_method=Check_Method.response, recover=False)

    # 雨量传感器重新采用（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Rain Sensor ReAdaption_43B8_0x03控制')
    def test_caseid_1981747(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x43b8, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x43b8, 0x03, SESSION.EXTENDED, UnLock.L0, '01', '6243b801')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x43b8, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '6243b800')

    # 后挡风玻璃加热器控制#1（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Rear Windscreen Heater Control #1_EF99_0x03控制')
    def test_caseid_1981727(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xef99, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xef99, 0x03, SESSION.EXTENDED, UnLock.L0, '01', '62ef9901')  # ON
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xef99, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '62ef9900')  # OFF

    # 雨刮单次挂水（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Single Stroke Wiping_4328_0x00控制')
    def test_caseid_1981754(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4328, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4328, 0x00, SESSION.EXTENDED, UnLock.L0, '', '6f432800',
                                         check_method=Check_Method.response, recover=False)

    # 雨刮单次挂水（APP）
    # BGM _MCU
    @pytest.mark.sanity
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Single Stroke Wiping_4328_0x03控制')
    def test_caseid_1981755(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4328, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4328, 0x03, SESSION.EXTENDED, UnLock.L0, '01', '62432801')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4328, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '62432800')

    # 方向盘加热控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Steering Wheel heat control_4220_0x00控制')
    def test_caseid_1981716(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4220, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4220, 0x00, SESSION.EXTENDED, UnLock.L0, '', '6f422000',
                                         check_method=Check_Method.response, recover=False)

    # 方向盘加热控制（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Steering Wheel heat control_4220_0x03控制')
    def test_caseid_1981717(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4220, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4220, 0x03, SESSION.EXTENDED, UnLock.L0, '01', '62422001')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4220, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '62422000')

    # 使用模式（APP）
    # BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Usage Mode_DD0A_0x00控制')
    def test_caseid_1981733(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xdd0a, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xdd0a, 0x00, SESSION.EXTENDED, UnLock.L0, '', '7f2f33',
                                         check_method=Check_Method.response, recover=False)

    # 使用模式（APP）
    # BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Usage Mode_DD0A_0x03控制')
    def test_caseid_1981735(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xdd0a, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xdd0a, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '7f2f33',
                                         check_method=Check_Method.response, recover=False)

    # 使用模式（APP）
    # BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Usage Mode_DD0A_L11_0x00控制')
    def test_caseid_1981728(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xdd0a, 0x00, SESSION.EXTENDED, UnLock.L11, '', '6fdd0a00',
                                         check_method=Check_Method.response, recover=False)

    # 使用模式（APP）
    # BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Usage Mode_DD0A_L11_0x03控制')
    def test_caseid_1981729(self):
        self.bus_comm.set('backbonefr', 'BcmVddmBackBoneFr00', 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xdd0a, 0x03, SESSION.EXTENDED, UnLock.L11, '00', '62dd0a00')
        # 在03会话安全访问L11下，2F 03控制车辆模式变为其他状态，最后默认2F 00 归还DID IO控制权
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xdd0a, 0x03, SESSION.EXTENDED, UnLock.L11, '01', '62dd0a01')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xdd0a, 0x03, SESSION.EXTENDED, UnLock.L11, '02', '62dd0a02')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xdd0a, 0x03, SESSION.EXTENDED, UnLock.L11, '0b', '62dd0a0b')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xdd0a, 0x03, SESSION.EXTENDED, UnLock.L11, '0d', '62dd0a0d')

    # 使用模式（APP）
    # BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Usage Mode_DD0A_L3_0x00控制')
    def test_caseid_1981730(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xdd0a, 0x00, SESSION.EXTENDED, UnLock.L3, '', '6fdd0a00',
                                         check_method=Check_Method.response)

    # 使用模式（APP）
    # BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Usage Mode_DD0A_L3_0x03控制')
    def test_caseid_1981731(self):
        self.bus_comm.set('backbonefr', 'BcmVddmBackBoneFr00', 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xdd0a, 0x03, SESSION.EXTENDED, UnLock.L3, '00', '62dd0a00')
        # 在03会话安全访问L3下，2F 03控制车辆模式变为其他状态，最后默认2F 00 归还DID IO控制权
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xdd0a, 0x03, SESSION.EXTENDED, UnLock.L3, '01', '62dd0a01')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xdd0a, 0x03, SESSION.EXTENDED, UnLock.L3, '02', '62dd0a02')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xdd0a, 0x03, SESSION.EXTENDED, UnLock.L3, '0b', '62dd0a0b')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xdd0a, 0x03, SESSION.EXTENDED, UnLock.L3, '0d', '62dd0a0d')

    # 使用模式（APP）
    # BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Usage Mode_DD0A_L5_0x00控制')
    def test_caseid_1981732(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xdd0a, 0x00, SESSION.EXTENDED, UnLock.L5, '', '6fdd0a00',
                                         check_method=Check_Method.response)

    # 使用模式（APP）
    # BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Usage Mode_DD0A_L5_0x03控制')
    def test_caseid_1981734(self):
        self.bus_comm.set('backbonefr', 'BcmVddmBackBoneFr00', 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xdd0a, 0x03, SESSION.EXTENDED, UnLock.L5, '00', '62dd0a00')
        # 在03会话安全访问L11下，2F 03控制车辆模式变为其他状态，最后默认2F 00 归还DID IO控制权
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xdd0a, 0x03, SESSION.EXTENDED, UnLock.L5, '01', '62dd0a01')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xdd0a, 0x03, SESSION.EXTENDED, UnLock.L5, '02', '62dd0a02')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xdd0a, 0x03, SESSION.EXTENDED, UnLock.L5, '0b', '62dd0a0b')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0xdd0a, 0x03, SESSION.EXTENDED, UnLock.L5, '0d', '62dd0a0d')

    # 控制BGM激活前洗涤继电器（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Washing Supply Control_41E9 _0x00控制')
    def test_caseid_1981780(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x41e9, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x41e9, 0x00, SESSION.EXTENDED, UnLock.L0, '', '6f41e900',
                                         check_method=Check_Method.response, recover=False)

    # 控制BGM激活前洗涤继电器（APP）
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Washing Supply Control_41E9 _0x03控制')
    def test_caseid_1981781(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x41e9, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x41e9, 0x03, SESSION.EXTENDED, UnLock.L0, '01', '6241e901')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x41e9, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '6241e900')

    # IGN电源继电器控制
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_4252_0x00控制')
    def test_caseid_1984792(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4252, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4252, 0x00, SESSION.EXTENDED, UnLock.L0, '', '7f2f33',
                                         check_method=Check_Method.response, recover=False)

    # IGN电源继电器控制
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_4252_L3_0x00控制')
    def test_caseid_1984791(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4252, 0x00, SESSION.EXTENDED, UnLock.L3, '', '624252',
                                         check_in=[0x00, 0x01], recover=False)

    # IGN电源继电器控制
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_4252_0x03控制')
    def test_caseid_1984790(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4252, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4252, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '7f2f33',
                                         check_method=Check_Method.response, recover=False)

    # IGN电源继电器控制
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_4252_L3_0x03控制')
    def test_caseid_1984789(self):
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal2)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4252, 0x03, SESSION.EXTENDED, UnLock.L3, '01', '62425201',
                                         recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4252, 0x03, SESSION.EXTENDED, UnLock.L3, '00', '62425200')

    # IGN扩展继电器控制
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_4250_0x00控制')
    def test_caseid_1984784(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4250, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4250, 0x00, SESSION.EXTENDED, UnLock.L0, '', '6f425000',
                                         check_method=Check_Method.response, recover=False)

    # IGN扩展继电器控制
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_4250_0x03控制')
    def test_caseid_1984783(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4250, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4250, 0x03, SESSION.EXTENDED, UnLock.L0, '01', '62425001',
                                         check_method=Check_Method.read, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4250, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '62425000',
                                         check_method=Check_Method.read)

    # KL15_3继电器控制
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_4254_0x00控制')
    def test_caseid_1984788(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4254, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4254, 0x00, SESSION.EXTENDED, UnLock.L0, '', '7f2f33',
                                         check_method=Check_Method.response, recover=False)

    # KL15_3继电器控制
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_4254_L3_0x00控制')
    def test_caseid_1984787(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4254, 0x00, SESSION.EXTENDED, UnLock.L3, '', '624254',
                                         check_in=[0x00, 0x01], recover=False)

    # KL15_3继电器控制
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_4254_0x03控制')
    def test_caseid_1984786(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4254, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4254, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '7f2f33',
                                         check_method=Check_Method.response, recover=False)

    # KL15_3继电器控制
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_4254_L3_0x03控制')
    def test_caseid_1984785(self):
        # self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal2)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4254, 0x03, SESSION.EXTENDED, UnLock.L3, '01', '62425401',
                                         recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4254, 0x03, SESSION.EXTENDED, UnLock.L3, '00', '62425400')

    # 舒适继电器控制
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_424f_0x00控制')
    def test_caseid_1984782(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x424f, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x424f, 0x00, SESSION.EXTENDED, UnLock.L0, '', '6f424f00',
                                         check_method=Check_Method.response, recover=False)

    # 舒适继电器控制
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_424f_0x03控制')
    def test_caseid_1984781(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x424f, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x424f, 0x03, SESSION.EXTENDED, UnLock.L0, '01', '62424f01',
                                         check_method=Check_Method.read, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x424f, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '62424f00',
                                         check_method=Check_Method.read)

    # 电池节电继电器控制
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_41e8_0x00控制')
    def test_caseid_1984780(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x41e8, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x41e8, 0x00, SESSION.EXTENDED, UnLock.L0, '', '6f41e800',
                                         check_method=Check_Method.response, recover=False)

    # 电池节电继电器控制
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_41e8_0x03控制')
    def test_caseid_1984779(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x41e8, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x41e8, 0x03, SESSION.EXTENDED, UnLock.L0, '01', '6241e801',
                                         check_method=Check_Method.read, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x41e8, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '6241e800',
                                         check_method=Check_Method.read)

    # 燃油泵/碰撞继电器控制
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Fuel Pump / crash relay Control_4310_0x03控制')
    def test_caseid_1981759(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4310, 0x03, SESSION.DEFAULT, UnLock.L0, '00', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4310, 0x03, SESSION.EXTENDED, UnLock.L0, '01', '7f2f33',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4310, 0x03, SESSION.EXTENDED, UnLock.L0, '00', '7f2f33',
                                         check_method=Check_Method.response, recover=False)

    # 燃油泵/碰撞继电器控制
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Fuel Pump / crash relay Control_4310_L3_0x00控制')
    def test_caseid_1981756(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4310, 0x00, SESSION.EXTENDED, UnLock.L3, '', '624310',
                                         check_in=[0x00, 0x01], recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4310, 0x00, SESSION.EXTENDED, UnLock.L3, '', '624310',
                                         check_in=[0x00, 0x01], recover=False)

    # 燃油泵/碰撞继电器控制
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Fuel Pump / crash relay Control_4310_0x00控制')
    def test_caseid_1981757(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4310, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4310, 0x00, SESSION.EXTENDED, UnLock.L0, '', '7f2f33',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4310, 0x00, SESSION.EXTENDED, UnLock.L0, '', '7f2f33',
                                         check_method=Check_Method.response, recover=False)

    # 燃油泵/碰撞继电器控制
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Fuel Pump / crash relay Control_4310_L3_0x03控制')
    def test_caseid_1981758(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4310, 0x03, SESSION.EXTENDED, UnLock.L3, '01', '62431001',
                                         recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4310, 0x03, SESSION.EXTENDED, UnLock.L3, '00', '62431000')

    # 外灯继电器控制
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Exterior Light Relay Control_439F_0x00控制')
    def test_caseid_1981748(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x439f, 0x00, SESSION.DEFAULT, UnLock.L0, '', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x439f, 0x00, SESSION.EXTENDED, UnLock.L0, '80', '6f439f000101',
                                         check_method=Check_Method.response, recover=False)

    # 外灯继电器控制
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Exterior Light Relay Control_439F_0x03控制')
    def test_caseid_1981749(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x439f, 0x03, SESSION.DEFAULT, UnLock.L0, '000080', '7f2f7f',
                                         check_method=Check_Method.response, recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x439f, 0x03, SESSION.EXTENDED, UnLock.L0, '000080', '62439f0001',
                                         recover=False)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x439f, 0x03, SESSION.EXTENDED, UnLock.L0, '000040', '62439f0000',
                                         recover=False)




@allure.feature('BGM BaseTech/诊断功能')
class TestIOControlBoot(TestABCBase):
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
        self.sd_tester.send_request_and_recv_response([0x10,0x02],recv=[0x50,0x02])
        self.sd_tester.send_request_and_recv_response([0x22, 0xf1,0x86], recv=[0x62, 0xf1,0x86,0x02])


    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        logger.info("after_class")
        # with allure.step("恢复环境"):
        #     self.mix.init_boot_per()
        super().after_class(self, ecu)
        self.sd_tester.exit_muc_boot()
        # 退出boot


    #后挡风玻璃加热器控制#1（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)Rear Windscreen Heater Control #1_EF99_0x00控制')
    def test_caseid_1981726_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0xef99,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)

    #控制WMM激活前洗涤（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Activation of Washer Front Safe_420A _0x03控制')
    def test_caseid_1981777_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x420a,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)

    #控制WMM激活前洗涤（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Activation of Washer Front Safe_420A_0x00控制')
    def test_caseid_1981776_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x420a,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)

    #电池可用Delta电源信号输出状态（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Available Delta Power signal output_40E2_0x00控制')
    def test_caseid_1981788_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x40e2,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)

    #电池可用Delta电源信号输出状态（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Available Delta Power signal output_40E2_0x03控制')#测试边界值7FFF
    def test_caseid_1981789_00(self):

        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x40e2,0x03,SESSION.PROGRAMMING,UnLock.L0,'7fff','7f2f11',check_method=Check_Method.response,recover=False)

    #B柱左侧门开按钮背光控制（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_B pillar left door opening button backlight control_4212_0x00控制')
    def test_caseid_1981723_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4212,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)

    # B柱左侧门开按钮背光控制（APP）
    # BGM _MCU


    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_B pillar left door opening button backlight control_4212_0x03控制')
    def test_caseid_1981725_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4212, 0x03, SESSION.PROGRAMMING, UnLock.L0, '00', '7f2f11',
                                         check_method=Check_Method.response, recover=False)

        # B柱右侧门开按钮背光控制（APP）
        # BGM _MCU

    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_B pillar Right door opening button backlight control_4222_0x00控制')
    def test_caseid_1981711_00(self):

        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x4222, 0x00, SESSION.PROGRAMMING, UnLock.L0, '', '7f2f11',
                                         check_method=Check_Method.response, recover=False)



    #B柱右侧门开按钮背光控制（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_B pillar Right door opening button backlight control_4222_0x03控制')
    def test_caseid_1981713_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4222,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)


    #C柱左侧门开按钮背光控制（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_C pillar left door opening button backlight control_4213_0x00控制')
    def test_caseid_1981719_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4213,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)


    #C柱左侧门开按钮背光控制（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_C pillar left door opening button backlight control_4213_0x03控制')
    def test_caseid_1981721_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4213,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)


    #C柱右侧门开按钮背光控制（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_C pillar Right door opening button backlight control_4223_0x00控制')
    def test_caseid_1981707_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4223,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)


    #C柱右侧门开按钮背光控制（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_C pillar Right door opening button backlight control_4223_0x03控制')
    def test_caseid_1981709_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4223,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)


    #车辆模式（APP）
    #BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Car Mode_D134_0x00控制')
    def test_caseid_1981741_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0xd134,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)


    #车辆模式（APP）
    #BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Car Mode_D134_0x03控制')
    def test_caseid_1981743(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0xd134,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)


    #ECM唤醒控制（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_ECM Wake Up Control_4253_0x00控制')
    def test_caseid_1981766_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4253,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)



    #ECM唤醒控制（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_ECM Wake Up Control_4253_0x03控制')
    def test_caseid_1981767_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4253,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)



    #低压能量等级替代（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Energy Level Electric Substitution_429D_0x00控制')
    def test_caseid_1981762_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429d,0x00,SESSION.PROGRAMMING,UnLock.L0,'80','7f2f11',check_method=Check_Method.response,recover=False)


    def test_caseid_1981763_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429d,0x03,SESSION.PROGRAMMING,UnLock.L0,'ff40','7f2f11',check_method=Check_Method.response,recover=False)

    #外灯控制（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Exterior Lights Control_7022_0x00控制')
    def test_caseid_1981744_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x7022,0x00,SESSION.PROGRAMMING,UnLock.L0,'800000','7f2f11',check_method=Check_Method.response,recover=False)


    #外灯控制（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Exterior Lights Control_7022_0x03控制')
    def test_caseid_1981745_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x7022,0x03,SESSION.PROGRAMMING,UnLock.L0,'800000800000','7f2f11',check_method=Check_Method.response,recover=False)


    #摄像头三角区域加热（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Front Camera Defrost Control_4256_0x00控制')
    def test_caseid_1981702_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4256,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)


    #摄像头三角区域加热（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Front Camera Defrost Control_4256_0x03控制')
    def test_caseid_1981703_00(self):

        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4256,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)

    #高位刹车灯控制（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_High Mounted Stop Lamp control_4221_0x00控制')
    def test_caseid_1981714_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4221,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)

    #高位刹车灯控制（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_High Mounted Stop Lamp control_4221_0x03控制')
    def test_caseid_1981715_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4221,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)


    #喇叭控制（APP）
    #BGM _MCU
    @pytest.mark.sanity
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Horn Control_41F2 _0x03控制')
    def test_caseid_1981779_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x41f2,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)


    #喇叭控制（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Horn Control_41F2_0x00控制')
    def test_caseid_1981778_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x41f2,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)


    #内灯控制（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_InteriorLight_41E5 _0x00控制')
    def test_caseid_1981784_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x41e5,0x00,SESSION.PROGRAMMING,UnLock.L0,'80','7f2f11',check_method=Check_Method.response,recover=False)


    #内灯控制（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_InteriorLight_41E5 _0x03控制')
    def test_caseid_1981785_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x41e5,0x03,SESSION.PROGRAMMING,UnLock.L0,'64000000000080','7f2f11',check_method=Check_Method.response,recover=False)

    #左右牌照灯（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_License Plate light Control_4217_0x00控制')
    def test_caseid_1981704_00(self):

        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4217,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)

    #左右牌照灯（APP）
    #BGM _MCU
    @pytest.mark.sanity
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_License Plate light Control_4217_0x03控制')
    def test_caseid_1981705_00(self):

        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4217,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)

    #低压功率等级替代（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Power Level Electric Substitution_429E_0x00控制')
    def test_caseid_1981760_00(self):

        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x00,SESSION.PROGRAMMING,UnLock.L0,'80','7f2f11',check_method=Check_Method.response,recover=False)

    #低压功率等级替代（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Power Level Electric Substitution_429E_0x03控制')
    def test_caseid_1981761_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x429e,0x03,SESSION.PROGRAMMING,UnLock.L0,'f080','7f2f11',check_method=Check_Method.response,recover=False)


    #车辆电源插口控制（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Power Outlet Control_4110 _0x00控制')
    def test_caseid_1981786_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4110,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)

    #车辆电源插口控制（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Power Outlet Control_4110 _0x03控制')
    def test_caseid_1981787_00(self):

        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4110,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)

    #ECM唤醒控制（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Private Unlock Supply Control_4260_0x00控制')
    def test_caseid_1981764_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4260,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)


    #ECM唤醒控制（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Private Unlock Supply Control_4260_0x03控制')
    def test_caseid_1981765_00(self):

        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4260,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)

    #雨量传感器重新采用（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Rain Sensor ReAdaption_43B8_0x00控制')
    def test_caseid_1981746_00(self):

        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x43b8,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)

    #雨量传感器重新采用（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Rain Sensor ReAdaption_43B8_0x03控制')
    def test_caseid_1981747_00(self):

        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x43b8,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)



    #后挡风玻璃加热器控制#1（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Rear Windscreen Heater Control #1_EF99_0x03控制')
    def test_caseid_1981727_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0xef99,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)

    #雨刮单次挂水（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Single Stroke Wiping_4328_0x00控制')
    def test_caseid_1981754_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4328,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)

    #雨刮单次挂水（APP）
    #BGM _MCU
    @pytest.mark.sanity
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Single Stroke Wiping_4328_0x03控制')
    def test_caseid_1981755_00(self):

        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4328,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)

    #方向盘加热控制（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Steering Wheel heat control_4220_0x00控制')
    def test_caseid_1981716_00(self):

        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4220,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)

    #方向盘加热控制（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Steering Wheel heat control_4220_0x03控制')
    def test_caseid_1981717_00(self):

        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4220,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)

    #使用模式（APP）
    #BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Usage Mode_DD0A_0x00控制')
    def test_caseid_1981733_00(self):

        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0xdd0a,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)

    #使用模式（APP）
    #BGM _MCU
    @pytest.mark.smoke
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Usage Mode_DD0A_0x03控制')
    def test_caseid_1981735_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0xdd0a,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)


    #控制BGM激活前洗涤继电器（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Washing Supply Control_41E9 _0x00控制')
    def test_caseid_1981780_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x41e9,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)


    #控制BGM激活前洗涤继电器（APP）
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Washing Supply Control_41E9 _0x03控制')
    def test_caseid_1981781_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x41e9,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)

    #IGN电源继电器控制
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_4252_0x00控制')
    def test_caseid_1984792_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4252,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)


    #IGN电源继电器控制
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_4252_0x03控制')
    def test_caseid_1984790_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4252,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)

    #IGN扩展继电器控制
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_4250_0x00控制')
    def test_caseid_1984784_00(self):

        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4250,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)

    #IGN扩展继电器控制
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_4250_0x03控制')
    def test_caseid_1984783_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4250,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)

    #KL15_3继电器控制
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_4254_0x00控制')
    def test_caseid_1984788_00(self):

        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4254,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)

    #KL15_3继电器控制
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_4254_0x03控制')
    def test_caseid_1984786_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4254,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)

    #舒适继电器控制
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_424f_0x00控制')
    def test_caseid_1984782_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x424f,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)

    #舒适继电器控制
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_424f_0x03控制')
    def test_caseid_1984781_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x424f,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)

    #电池节电继电器控制
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_41e8_0x00控制')
    def test_caseid_1984780_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x41e8,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)

    #电池节电继电器控制
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_VehicleModeManagment_41e8_0x03控制')
    def test_caseid_1984779_00(self):

        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x41e8,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)


    #燃油泵/碰撞继电器控制
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Fuel Pump / crash relay Control_4310_0x03控制')
    def test_caseid_1981759_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4310,0x03,SESSION.PROGRAMMING,UnLock.L0,'00','7f2f11',check_method=Check_Method.response,recover=False)


    #燃油泵/碰撞继电器控制
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Fuel Pump / crash relay Control_4310_0x00控制')
    def test_caseid_1981757_00(self):

        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x4310,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)


    #外灯继电器控制
    #BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Exterior Light Relay Control_439F_0x00控制')
    def test_caseid_1981748_00(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU,0x439f,0x00,SESSION.PROGRAMMING,UnLock.L0,'','7f2f11',check_method=Check_Method.response,recover=False)

    # 外灯继电器控制
    # BGM _MCU
    @pytest.mark.full
    @allure.story('诊断IOControl')
    @allure.title('UDS_IOControl(0x2F)_Exterior Light Relay Control_439F_0x03控制')
    def test_caseid_1981749_00(self):

        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0x439f, 0x03, SESSION.PROGRAMMING, UnLock.L0, '000040', '7f2f11',
                                         check_method=Check_Method.response, recover=False)


#pytest BaseTech/DiagFlash/test_diag_bgm_iocontrol.py::TestIOControlApp::test_caseid_1981742 --disable_partner='true'





#pytest BaseTech/Diagnostics/test_diag_bgm_iocontrol.py::TestIOControlBoot::test_caseid_1981737 --disable_partner='true'
