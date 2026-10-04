import subprocess
import pytest
import allure
import pytest
import allure
from xat_cases.legacy.bgm.mcu.case_helper.test_abc_base import TestABCBase 
from xat_ecu.api.common.common import *



@allure.feature("通讯功能/以太网通讯")
@allure.story("以太网通讯")
class Test_Switch(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # Code Location

    def after_each_func(self, ecu):
        # Code Location
        super().after_each_func(ecu)
        logger.info("================测试结束 tcam 上电 =================")
        self.io.tcam_power_on()
        time.sleep(3*60)

    def after_class(self, ecu):
        # Code Location
        super().after_class(self, ecu)


    @pytest.mark.sanity
    def test_ping_tcam_success_caseid_1986462(self):
        """
        BGM SOC 启动 3mins后开始检测TCAM的通讯状态
        """
        self.mix.test_check_ping_tcam_success(bgm_wait_time=3*60,tcam_wait_time=2*60,expect_value=2)

    @pytest.mark.sanity
    def test_ping_tcam_fail_caseid_1986463(self):
        """
        BGM SOC 启动 3mins后，断开tcam电源，开始检测TCAM的通讯状态
        """
        #tcam断电8分钟
        self.mix.test_check_ping_tcam_fail(bgm_wait_time=3*60,tcam_wait_time=8*60,expect_value=6,phy_reset_count=1)
        self.io.tcam_power_on()

    @pytest.mark.sanity
    def test_ping_tcam_fail_phy_six_caseid_1986464(self):
        """
        BGM SOC 启动 3mins后，TCAM复位6次失败后上电，开始检测TCAM的通讯状态
        """
        #tcam断电50分钟
        self.mix.test_check_ping_tcam_fail(bgm_wait_time=3*60,tcam_wait_time=50*60,expect_value=36,phy_reset_count=6,phy_quit=1)
        #复位6次失败后，给TCAM上电9分钟
        logger.info("================ tcam 上电 =================")
        self.io.tcam_power_on()
        self.mix.test_check_ping_tcam_success(bgm_wait_time=3*60,tcam_wait_time=9*60,expect_value=6)

    @pytest.mark.sanity
    def test_ping_tcam_fail_phy_two_caseid_1986465(self):
        """
        BGM SOC 启动 3mins后，TCAM2次复位失败后上电再断电，开始检测TCAM的通讯状态
        """   
        #tcam断电15分钟
        self.mix.test_check_ping_tcam_fail(bgm_wait_time=3*60,tcam_wait_time=15*60,expect_value=12,phy_reset_count=2)
        #复位2次失败后，给TCAM上电9分钟
        logger.info("================ tcam 上电 =================")
        self.io.tcam_power_on()
        self.mix.test_check_ping_tcam_success(bgm_wait_time=3*60,tcam_wait_time=9*60,expect_value=6)
        #再次给tcam断电50分钟
        self.mix.test_check_ping_tcam_fail(bgm_wait_time=3*60,tcam_wait_time=50*60,expect_value=36,phy_reset_count=6,phy_quit=1)
    
    