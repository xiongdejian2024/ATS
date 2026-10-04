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
        self.soa.update([("AcuModeManagerService","server")])

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC, 0xa105, 0x01, SESSION.EXTENDED, UnLock.L5, '00', '7101a10510')
       
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.smoke
    @allure.title("关闭维持不可开车_Flag未置位_【51F2】")
    def test_remote_rescue_caseid_1988012(self):
        self.tsp.trigger_remote_rescue(rescue_type=RescueType.CloseInhibit)
        assert self.sd_tester.read_f155() == "00"
        with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords='data: {"cmd":1,"cmdDetail":{"inhibitControl":1,"resetControl":0},"responseCode":"51F2"', timeout=30):
            self.tsp.trigger_remote_rescue(rescue_type=RescueType.CloseInhibit)
        
    @pytest.mark.smoke
    @allure.title("关闭维持不可开车_Flag已置位_【50F1】【51F2】")
    def test_remote_rescue_caseid_1988013(self):
        self.tsp.trigger_remote_rescue(rescue_type=RescueType.OpenInhibit)
        assert self.sd_tester.read_f155() == "01"
        time.sleep(5) #等待5S后关闭，避免刚开启就立即关闭。
        with self.log_manage.check_jetlog_by_same_keywords(log_type=" remote_rescue:", keywords=['data: {"cmd":1,"cmdDetail":{"inhibitControl":1,"resetControl":0},"responseCode":"51F2"',
                                                                                            'data: {"cmd":1,"cmdDetail":{"inhibitControl":1,"resetControl":0},"responseCode":"50F1"'
                                                                                            ], timeout=30):
            self.tsp.trigger_remote_rescue(rescue_type=RescueType.CloseInhibit)
        self.mix.check_fota_keep_awake(log_type=" remote_rescue: ",pnc29=False,acu_keep_alive=False,up_inactive=False,hv_active=False,startInhibit=False)
        assert self.sd_tester.read_f155() == "00"

    @pytest.mark.full
    @allure.title("开启维持不可开车_TimeOut_time=3H&&休眠唤醒")
    def test_remote_rescue_caseid_1988014(self):
        self.tsp.trigger_remote_rescue(rescue_type=RescueType.CloseInhibit)
        assert self.sd_tester.read_f155() == "00"
        self.ssh.rescue_ua_skip() #必需将不可开车关闭后，开关将timeout 3H 改为5min，才能生效
        self.sd_tester.reset_bgm()
        self.tsp.trigger_remote_rescue(rescue_type=RescueType.OpenInhibit)
        assert self.sd_tester.read_f155() == "01"
        time.sleep(305) #等待5min后timeout
        assert self.mix.check_fota_keep_awake(log_type=" remote_rescue: ",pnc29=False,acu_keep_alive=False,up_inactive=False,hv_active=False,startInhibit=False)
        self.sd_tester.reset_bgm() #重启BGM 代替休眠唤醒
        assert self.mix.check_fota_keep_awake(log_type=" remote_rescue: ",pnc29=True,acu_keep_alive=True,up_inactive=True,hv_active=True,startInhibit=True)
        assert self.sd_tester.read_f155() == "01"

    @pytest.mark.sanity
    @allure.title("开启维持不可开车_TimeOut_默认3H【5101】")
    def test_remote_rescue_caseid_1988015(self):
        try:
            self.ssh.type_commands(DeviceName.BGM,'rm -rf /update/ua_skip;sync')
            self.sd_tester.reset_bgm()
            self.tsp.trigger_remote_rescue(rescue_type=RescueType.OpenInhibit)
            assert self.sd_tester.read_f155() == "01"
            time.sleep(10785) #等待3h后timeout
            with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords='data: {"cmd":2,"cmdDetail":{"inhibitControl":2,"resetControl":0},"responseCode":"5101",', timeout=20):
                pass
            assert self.mix.check_fota_keep_awake(log_type=" remote_rescue: ",pnc29=False,acu_keep_alive=False,up_inactive=False,hv_active=False,startInhibit=False)
        finally:
            self.tsp.trigger_remote_rescue(rescue_type=RescueType.OpenInhibit)
            assert self.sd_tester.read_f155() == "01"
            self.tsp.trigger_remote_rescue(rescue_type=RescueType.CloseInhibit)
            assert self.sd_tester.read_f155() == "00"
            self.ssh.rescue_ua_skip() #必需将不可开车关闭后，开关将timeout 3H 改为5min，才能生效
            self.sd_tester.reset_bgm()

    @pytest.mark.full
    @allure.title("开启维持不可开车_维持唤醒&&不可开车_服务链接不上【5001】")
    def test_remote_rescue_caseid_1988016(self):
        try:
            self.soa.soa_partner.stop_single_partner("AcuModeManagerService_server")
            self.tsp.trigger_remote_rescue(rescue_type=RescueType.OpenInhibit)
            assert self.sd_tester.read_f155() == "01"
            with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords='data: {"cmd":2,"cmdDetail":{"inhibitControl":2,"resetControl":0},"responseCode":"5001"', timeout=330):
                pass
            assert self.mix.check_fota_keep_awake(log_type=" remote_rescue: ",pnc29=False,acu_keep_alive=False,up_inactive=False,hv_active=False,startInhibit=False)
        finally:    
            self.soa.update([("AcuModeManagerService","server")])
   
    @pytest.mark.full
    @allure.title("开启维持不可开车_Flag已置位_time重设&&【51F1】")
    def test_remote_rescue_caseid_1988017(self):
        self.tsp.trigger_remote_rescue(rescue_type=RescueType.OpenInhibit)
        assert self.sd_tester.read_f155() == "01"
        time.sleep(120)#等待2min再次下发维持不可开车
        with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords='data: {"cmd":1,"cmdDetail":{"inhibitControl":2,"resetControl":0},"responseCode":"51F1"', timeout=330):
            self.tsp.trigger_remote_rescue(rescue_type=RescueType.OpenInhibit)
        time.sleep(300)#等待5min 检查唤醒还在发送，且还维持在不可开车置位
        assert self.mix.check_fota_keep_awake(log_type=" remote_rescue: ",pnc29=True,acu_keep_alive=True,up_inactive=True,hv_active=True,startInhibit=True)
        assert self.sd_tester.read_f155() == "01"

    @pytest.mark.smoke
    @allure.title("开启维持不可开车_Flag未置位_维持唤醒&&不可开车&&【51F1】")
    def test_remote_rescue_caseid_1988018(self):
        self.tsp.trigger_remote_rescue(rescue_type=RescueType.CloseInhibit)
        assert self.sd_tester.read_f155() == "00"
        with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords='data: {"cmd":1,"cmdDetail":{"inhibitControl":2,"resetControl":0},"responseCode":"51F1"', timeout=330):
            self.tsp.trigger_remote_rescue(rescue_type=RescueType.OpenInhibit)
        assert self.sd_tester.read_f155() == "01"
        assert self.mix.check_fota_keep_awake(log_type=" remote_rescue: ",pnc29=True,acu_keep_alive=True,up_inactive=True,hv_active=True,startInhibit=True)

    @pytest.mark.sanity
    @allure.title("开启维持不可开车_time = 默认3h_【50F1】")
    def test_remote_rescue_caseid_1988019(self):
        try:
            self.ssh.type_commands(DeviceName.BGM,'rm -rf /update/ua_skip;sync')
            self.sd_tester.reset_bgm()
            with self.log_manage.check_jetlog_by_keywords(log_type=" remote_rescue:", keywords=['"timeout":10800000','data: {"cmd":1,"cmdDetail":{"inhibitControl":2,"resetControl":0},"responseCode":"50F1"'], timeout=330):
                self.tsp.trigger_remote_rescue(rescue_type=RescueType.OpenInhibit)
            assert self.sd_tester.read_f155() == "01"
            assert self.mix.check_fota_keep_awake(log_type=" remote_rescue: ",pnc29=True,acu_keep_alive=True,up_inactive=True,hv_active=True,startInhibit=True)
        finally:
            self.tsp.trigger_remote_rescue(rescue_type=RescueType.OpenInhibit)
            assert self.sd_tester.read_f155() == "01"
            self.tsp.trigger_remote_rescue(rescue_type=RescueType.CloseInhibit)
            assert self.sd_tester.read_f155() == "00"
            self.ssh.rescue_ua_skip() #必需将不可开车关闭后，开关将timeout 3H 改为5min，才能生效
            self.sd_tester.reset_bgm()


    @pytest.mark.sanity
    @allure.title("开启维持不可开车_TimeOut_time=3H&&再次下发维持不可开车指令")
    def test_remote_rescue_caseid_1988718(self):
        self.tsp.trigger_remote_rescue(rescue_type=RescueType.CloseInhibit)
        assert self.sd_tester.read_f155() == "00"
        self.ssh.rescue_ua_skip() #必需将不可开车关闭后，开关将timeout 3H 改为5min，才能生效
        self.sd_tester.reset_bgm()
        self.tsp.trigger_remote_rescue(rescue_type=RescueType.OpenInhibit)
        assert self.sd_tester.read_f155() == "01"
        sleep(305)#等待5min检查是否停发唤醒
        assert self.mix.check_fota_keep_awake(log_type=" remote_rescue: ",pnc29=False,acu_keep_alive=False,up_inactive=False,hv_active=False,startInhibit=False)
        self.tsp.trigger_remote_rescue(rescue_type=RescueType.OpenInhibit)
        assert self.sd_tester.read_f155() == "01"
        assert self.mix.check_fota_keep_awake(log_type=" remote_rescue: ",pnc29=True,acu_keep_alive=True,up_inactive=True,hv_active=True,startInhibit=True)

if __name__ == "__main__":
    pass

