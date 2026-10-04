import os
import sys
import pytest
import allure
import re
import json
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature("基础架构")
@allure.story("remote_diag")
class Test_Remote_Rescue(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa105, 0x01, SESSION.EXTENDED, UnLock.L5, '00', '7101a10510')
       
    def after_class(self, ecu):
        super().after_class(self, ecu)
        

    @pytest.mark.smoke
    @allure.title("诊断DID_F1_55_获取维持不可开车状态_当前不可开车Flag未置位")
    def test_remote_rescue_caseid_1988008(self):
        self.tsp.trigger_remote_rescue(rescue_type=RescueType.CloseInhibit)
        sleep(1)#等待写入完成
        vehicleInfo_arg = self.ssh.type_commands(DeviceName.BGM, "cat /data/vehicleInfo.json")
        vehicleInfo_arg = vehicleInfo_arg.replace('\n', '') + '}'  # type_commands函数cat /data/vehicleInfo.json读取结果不完整，会少一个闭合的花括号}
        vehicleInfo_Value = json.loads(vehicleInfo_arg)
        F155_Value = "0" + str(vehicleInfo_Value['F155'][0])
        assert self.sd_tester.read_f155() == F155_Value

    @pytest.mark.sanity
    @allure.title("诊断DID_F1_55_获取维持不可开车状态_当前不可开车Flag默认值")
    def test_remote_rescue_caseid_1988007(self):
        # self.ssh.type_commands(DeviceName.BGM, "rm -rf /data/vehicleInfo.json;sync")
        self.sd_tester.reset_bgm()
        assert self.sd_tester.read_f155() == "00"

    @pytest.mark.smoke
    @allure.title("诊断DID_F1_55_获取维持不可开车状态_当前不可开车Flag已置位")
    def test_remote_rescue_caseid_1988009(self):
        self.tsp.trigger_remote_rescue(rescue_type=RescueType.OpenInhibit)
        sleep(1)#等待写入完成
        vehicleInfo_arg = self.ssh.type_commands(DeviceName.BGM, "cat /data/vehicleInfo.json")
        vehicleInfo_arg = vehicleInfo_arg.replace('\n', '') + '}'  # type_commands函数cat /data/vehicleInfo.json读取结果不完整，会少一个闭合的花括号}
        vehicleInfo_Value = json.loads(vehicleInfo_arg)
        F155_Value = "0" + str(vehicleInfo_Value['F155'][0])
        assert self.sd_tester.read_f155() == F155_Value
        self.tsp.trigger_remote_rescue(rescue_type=RescueType.CloseInhibit)

    @pytest.mark.smoke
    @allure.title("诊断RID_A1_05_解除维持不可开车_当前不可开车Flag未置位")
    def test_remote_rescue_caseid_1988010(self):
        self.tsp.trigger_remote_rescue(rescue_type=RescueType.CloseInhibit)
        self.sd_tester.read_f155() == "00"
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa105, 0x01, SESSION.EXTENDED, UnLock.L5, '00', '7101a10510')

    @pytest.mark.smoke
    @allure.title("诊断RID_A1_05_解除维持不可开车_当前不可开车Flag已置位")
    def test_remote_rescue_caseid_1988011(self):
        self.tsp.trigger_remote_rescue(rescue_type=RescueType.OpenInhibit)
        self.sd_tester.read_f155() == "01"
        with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords='data: {"cmd":1,"cmdDetail":{"inhibitControl":1,"resetControl":0},"responseCode":"50F1",', timeout=60):
            self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa105, 0x01, SESSION.EXTENDED, UnLock.L5, '00', '7101a10510')
            self.mix.check_remoteRescue_wakeup_and_Inhibit(pnc29=False,acu_keep_alive=False,up_inactive=False,hv_active=False,startInhibit=False)
        self.sd_tester.read_f155() == "00"
        
if __name__ == "__main__":
    pass
