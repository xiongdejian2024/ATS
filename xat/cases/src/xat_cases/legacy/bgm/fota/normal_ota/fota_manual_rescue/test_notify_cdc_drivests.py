import os
import sys
import pytest
import allure
import re
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature("基础架构")
@allure.story("remote_diag")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("AcuModeManagerService","server"),
                         ("RemoteRescueService","client","BGM_RemoteRescueService")])

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa105, 0x01, SESSION.EXTENDED, UnLock.L5, '00', '7101a10510')
       
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.V_2_2
    @pytest.mark.smoke
    @allure.title("关闭维持不可开车状态_重启BGM_检查RemoteRescueService上线")
    def test_remote_rescue_caseid_1995499(self):
        self.tsp.trigger_remote_rescue(rescue_type=RescueType.CloseInhibit)
        assert self.sd_tester.read_f155() == "00"
        assert self.soa.get_Remote_Rescue_DriveSts() == Remote_Rescue_DriveSts.kNormal.value
        self.sd_tester.reset_bgm()
        assert self.soa.get_Remote_Rescue_DriveSts() == Remote_Rescue_DriveSts.kNormal.value
        assert self.soa.check_DriveSts_event_period(target_period=3.0, epsilon=0.1)

    @pytest.mark.V_2_2
    @pytest.mark.smoke
    @allure.title("开启维持不可开车状态_重启BGM_检查RemoteRescueService上线")
    def test_remote_rescue_caseid_1995500(self):
        self.tsp.trigger_remote_rescue(rescue_type=RescueType.OpenInhibit)
        assert self.sd_tester.read_f155() == "01"
        assert self.soa.get_Remote_Rescue_DriveSts() == Remote_Rescue_DriveSts.kInhibit.value
        self.sd_tester.reset_bgm()
        assert self.soa.get_Remote_Rescue_DriveSts() == Remote_Rescue_DriveSts.kInhibit.value
        assert self.soa.check_DriveSts_event_period(target_period=3.0, epsilon=0.1)
        
if __name__ == "__main__":
    pass