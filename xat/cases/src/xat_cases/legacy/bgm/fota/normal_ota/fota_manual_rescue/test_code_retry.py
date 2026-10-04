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
from xat_cases.legacy.bgm.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature("基础架构")
@allure.story("remote_diag")
class Test_Remote_Rescue(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("AcuModeManagerService","server"),
                         ("V2TRoutingForwarder","client","V2TRemoteRescueForwarder")])
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3) 

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.ssh.set_airplane_mode(isOn.Off)
       
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.ssh.set_airplane_mode(isOn.Off)
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa105, 0x01, SESSION.EXTENDED, UnLock.L5, '00', '7101a10510')

    @pytest.mark.full
    @allure.title("Code上报失败重试_51F2")
    def test_remote_rescue_caseid_1987995(self):
        self.tsp.trigger_remote_rescue(rescue_type=RescueType.OpenInhibit)
        self.ssh.set_airplane_mode(isOn.On)
        with self.log_manage.check_jetlog_by_same_keywords(log_type=" remote_rescue:", keywords=['"responseCode":"51F2"',
                                                                                                '"responseCode":"51F2"',
                                                                                                '"responseCode":"51F2"',
                                                                                                '"responseCode":"51F2"',
                                                                                                '"responseCode":"51F2"',
                                                                                                '"responseCode":"51F2"'], timeout=60):
            self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa105, 0x01, SESSION.EXTENDED, UnLock.L5, '00', '7101a10510')
        self.sd_tester.reset_bgm()
        with self.log_manage.check_jetlog_by_same_keywords(log_type=" remote_rescue:", keywords=['"responseCode":"51F2"',
                                                                                                '"responseCode":"51F2"',
                                                                                                '"responseCode":"51F2"',
                                                                                                '"responseCode":"51F2"',
                                                                                                '"responseCode":"51F2"',
                                                                                                '"responseCode":"51F2"'], timeout=60):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords=['"responseCode":"51F2"',
                                                                                            'v2t info not valid'], timeout=60):
            self.ssh.set_airplane_mode(isOn.Off)
            
    @pytest.mark.full
    @allure.title("Code上报失败重试_51F1")
    def test_remote_rescue_caseid_1987996(self):
        try:
            self.ssh.set_airplane_mode(isOn.On)
            self.soa.trigger_remote_rescue_inhibitControl()
            with self.log_manage.check_jetlog_by_same_keywords(log_type=" remote_rescue:", keywords=['"responseCode":"51F1"',
                                                                                                    '"responseCode":"51F1"',
                                                                                                    '"responseCode":"51F1"',
                                                                                                    '"responseCode":"51F1"',
                                                                                                    '"responseCode":"51F1"',
                                                                                                    '"responseCode":"51F1"'], timeout=60):
                pass
        finally:
            self.ssh.set_airplane_mode(isOn.Off)


    @pytest.mark.full
    @allure.title("Code上报失败重试_52F1")
    def test_remote_rescue_caseid_1987994(self):
        self.io.bgm_diag_line_down()
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.bus_comm.set_epb_sts(sts=0)
        self.tsp.trigger_remote_rescue(rescue_type=RescueType.ResetDomain)
        self.ssh.set_airplane_mode(isOn.On)
        with self.log_manage.check_jetlog_by_same_keywords(log_type=" remote_rescue:", keywords=['"responseCode":"52F1"',
                                                                                                '"responseCode":"52F1"',
                                                                                                '"responseCode":"52F1"',
                                                                                                '"responseCode":"52F1"',
                                                                                                '"responseCode":"52F1"',
                                                                                                '"responseCode":"52F1"'], timeout=60):
            pass
        self.sd_tester.reset_bgm()
        with self.log_manage.check_jetlog_by_same_keywords(log_type=" remote_rescue:", keywords=['"responseCode":"52F1"',
                                                                                                '"responseCode":"52F1"',
                                                                                                '"responseCode":"52F1"',
                                                                                                '"responseCode":"52F1"',
                                                                                                '"responseCode":"52F1"',
                                                                                                '"responseCode":"52F1"'], timeout=60):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords=['"responseCode":"52F1"',
                                                                                            'v2t info not valid'], timeout=60):
            self.ssh.set_airplane_mode(isOn.Off)    

    @pytest.mark.full
    @allure.title("无网下_诊断关闭维持不可开车&&重启四域结束code上报")
    def test_remote_rescue_caseid_1995501(self):
        self.io.bgm_diag_line_down()
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.bus_comm.set_epb_sts(sts=0)
        self.tsp.trigger_remote_rescue(rescue_type=RescueType.OpenInhibit)
        self.tsp.trigger_remote_rescue(rescue_type=RescueType.ResetDomain)
        sleep(4) #等待任务串行执行
        self.ssh.set_airplane_mode(isOn.On)
        with self.log_manage.check_jetlog_by_same_keywords(log_type=" remote_rescue:", keywords=['"responseCode":"52F1"',
                                                                                                 '"responseCode":"51F2"',
                                                                                                '"responseCode":"52F1"',
                                                                                                '"responseCode":"51F2"',
                                                                                                '"responseCode":"52F1"',
                                                                                                '"responseCode":"51F2"',
                                                                                                '"responseCode":"52F1"',
                                                                                                '"responseCode":"51F2"',
                                                                                                '"responseCode":"52F1"',
                                                                                                '"responseCode":"51F2"',
                                                                                                '"responseCode":"52F1"'], timeout=60):
            self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa105, 0x01, SESSION.EXTENDED, UnLock.L5, '00', '7101a10510')
        with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords=['"responseCode":"52F1"',
                                                                                            '"responseCode":"51F2"',
                                                                                            'send to cloud succeed'], timeout=60):
            self.ssh.set_airplane_mode(isOn.Off)    
           
if __name__ == "__main__":
    pass
