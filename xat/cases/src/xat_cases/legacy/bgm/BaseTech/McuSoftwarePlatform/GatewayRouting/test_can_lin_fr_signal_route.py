# -*- coding: utf-8 -*-
"""
@File        : test_can_lin_fr_signal_route.py
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/11/22 11:36
@Description :

"""

import os
import sys
import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.BaseTech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from framework.automotive.utils.data_type import EcuInfo
from xat_ecu.legacy.common.logger import logger

@pytest.mark.mcu_test
@allure.feature("MCU 基础平台/信号路由")
@allure.story("CAN LIN FR 信号路由")
@pytest.mark.last
class TestCanLinFRSignalRoute(TestABCBase):
    @staticmethod
    def change_bench_config(ecu: EcuInfo) -> EcuInfo:
        """子类重写该接口，自定义台架类型为单域、两域或者四域"""
        ecu.domain.single_bgm=True
        ecu.domain.two_domain=None
        ecu.tc_config['dut_ecu']=["BGM"]
        return ecu
    
    def before_class(self, ecu):
        logger.info("before_class")
        super().before_class(self, ecu)
        self.io.tcam_power_off()
        sleep(30)
        self.mix.set_usage_mode(UsageMode.DRIVING)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("before_each_func")
        self.excel_path = "BaseTech/config_data/signal_routing_communication/"

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        logger.info("after_each_func")

    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.io.tcam_power_on()
        logger.info("tcam 上电 延时3min ")
        sleep(3*60)
        

    @allure.link(
        'https://ms.jiduprod.com/#/track/case/edit/abf46d66-751c-4d37-99a9-1ee6096473d9?projectId=7cf5bac0-7cee-4b73-882b-f53fd8ff859d',
        name="周期信号路由"
    )
    @pytest.mark.smoke
    @pytest.mark.long_time
    @pytest.mark.timeout(60 * 15)
    def test_cycle_route_caseid_1984460(self):
        """
        """
        self.sd_tester.get_mcu_cpuload()
        self.mix.check_signal_route_items(excel_path=self.excel_path, select_cond='cycle')

    @allure.link(
        'https://ms.jiduprod.com/#/track/case/edit/6b9e3e59-e2d8-446d-9994-d12223def3d8?projectId=7cf5bac0-7cee-4b73-882b-f53fd8ff859d',
        name="非周期信号路由"
    )
    @pytest.mark.smoke
    @pytest.mark.timeout(60 * 20)
    def test_event_route_caseid_1984461(self):
        """
        """
        self.sd_tester.get_mcu_cpuload()
        self.mix.check_signal_route_items(excel_path=self.excel_path, select_cond='event')

    @allure.link(
        'https://ms.jiduprod.com/#/track/case/edit/37048096-f7f6-4ce3-b7a1-be03ba728921?projectId=7cf5bac0-7cee-4b73-882b-f53fd8ff859d',
        name="带有UB位的信号路由_UB位不置1"
    )
    @pytest.mark.smoke
    @pytest.mark.long_time
    @pytest.mark.timeout(60 * 45)
    def test_ub_route_caseid_1984464(self):
        """
        """
        self.sd_tester.get_mcu_cpuload()
        self.mix.check_signal_route_items(excel_path=self.excel_path, select_cond='ub')

    @pytest.mark.smoke
    def test_cycle_route_caseid_1987086(self):
        """
        新方向盘信号
        """        
        self.sd_tester.write_ccp(ccp={629: 0x04})
        self.bus_comm.set('bodycan', 'SwtlBodyFr01','SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)
        sleep(1)
        self.bus_comm.check('adcanfd', 'BgmADCANFDFr30', 'SteerWhlTouchTurnLightSwtLeSteerWhlTouchTurnLightSwtLe',1)
        self.bus_comm.check('passivesafetycan', 'BgmPassSafeCANFr01', 'SteerWhlTouchTurnLightSwtLeSteerWhlTouchTurnLightSwtLe', 1)

        self.bus_comm.set('bodycan', 'SwtrBodyFr01','SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 1)
        sleep(1)
        self.bus_comm.check('adcanfd', 'BgmADCANFDFr30', 'SteerWhlTouchTurnLightSwtRiSteerWhlTouchTurnLightSwtLe',1)
        self.bus_comm.check('passivesafetycan', 'BgmPassSafeCANFr01', 'SteerWhlTouchTurnLightSwtRiSteerWhlTouchTurnLightSwtLe', 1)

    @pytest.mark.smoke
    def test_cycle_route_caseid_1987087(self):
        """
        新方向盘信号
        """
        self.sd_tester.write_ccp(ccp={629: 0x06})
        self.bus_comm.set('bodycan', 'SwtlBodyFr01','SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 2)
        sleep(1)
        self.bus_comm.check('adcanfd', 'BgmADCANFDFr30', 'SteerWhlTouchTurnLightSwtLeSteerWhlTouchTurnLightSwtLe',2)
        self.bus_comm.check('passivesafetycan', 'BgmPassSafeCANFr01', 'SteerWhlTouchTurnLightSwtLeSteerWhlTouchTurnLightSwtLe', 2)

        self.bus_comm.set('bodycan', 'SwtlBodyFr02','SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 2)
        sleep(1)
        self.bus_comm.check('adcanfd', 'BgmADCANFDFr30', 'SteerWhlTouchTurnLightSwtRiSteerWhlTouchTurnLightSwtLe',2)
        self.bus_comm.check('passivesafetycan', 'BgmPassSafeCANFr01', 'SteerWhlTouchTurnLightSwtRiSteerWhlTouchTurnLightSwtLe', 2)

if __name__ == '__main__':
    # pytest basic_platform/signal_route/can_lin_fr/test_can_lin_fr_signal_route.py
    # pytest 00ltg/test_can_lin_fr_signal_route.py
    pass
