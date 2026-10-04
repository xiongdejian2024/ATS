import os
import sys
import pytest
import allure
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.tcam.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.smoke 
    @allure.title("版本收集_22_F1_86")
    def test_fota_caseid_1982972(self, ecu):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.DEFAULT,'62f18601')
        
    @pytest.mark.smoke 
    @allure.title("版本收集_22_F1_AA")
    def test_fota_caseid_1982971(self, ecu):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF1AA,SESSION.DEFAULT,'62f1aa',check_length=22)

    @pytest.mark.smoke 
    @allure.title("版本收集_22_F1_AE")
    def test_fota_caseid_1982970(self, ecu):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF1AE,SESSION.DEFAULT,'62f1ae',check_length=24)

if __name__ == "__main__":
    pass