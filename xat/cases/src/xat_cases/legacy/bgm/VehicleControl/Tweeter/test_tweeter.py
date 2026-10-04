"""
@File        : test_tweeter.py
@Author      : xiangyue.li@jiduatuo.com
@Time        : 2024/11/10 15:00 PM
"""

import os
import sys
import pytest
import allure
from time import sleep


sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.soa_partner.src.partner_const import *


@allure.feature("车控车设")
@allure.story("扬声器")
class TestHornCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["HornService_client", "CentralLockService_client","TweeterService_client"])
        sleep(2)

    def before_each_func(self, ecu):
        self.mix.set_common_precontion()
        self.io.set_five_door_sts(Door.close)

    def after_each_func(self, ecu):
        self.mix.set_common_precontion()
        sleep(2)

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    @allure.title("646275_控制扬声器升起")
    @pytest.mark.full
    def test_caseid_1989351(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.set_tweeter_updown(zone_id=TweeterZoneId.AllZone,tweeter_command=TweeterCommand.UP)
        self.bus_comm.check_tweeter_sts(sts=TweeterSts.UP)
        
    @allure.title("646275_控制扬声器降下")
    @pytest.mark.full
    def test_caseid_1989358(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.set_tweeter_updown(zone_id=TweeterZoneId.AllZone,tweeter_command=TweeterCommand.DOWN)
        self.bus_comm.check_tweeter_sts(sts=TweeterSts.DOWN)