#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_digital_key_other_abc.py
@Time         :2024/03/16 22:50:00
@Author       :hui.zhao@jiduauto.com
@Description  :数字钥匙NFC相关功能
"""
import copy
from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass_abc import *
from xat_ecu.api.abc_interface import *


@allure.feature("数字钥匙功能测试")
@allure.story("PEPS_近车自动解锁")
@pytest.mark.run(order=1)
class TestDigitalKeyApproach(TestDigitalKeyBase):
    def before_class(self, ecu):
        super().before_class(self,ecu)
        logger.info("------------------>复位BGM")
        self.io.bgm_power_off()
        sleep(2)
        self.io.bgm_power_on()
        time.sleep(15)
        logger.info("------------------>复位BGM结束")

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb", 0.0)
        sleep(10)
        self.bus_comm.dk.empty_dk_data_queue()
    
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
    
    def after_class(self, ecu):
        return super().after_class(self,ecu)
    

    @allure.title("MaxSoc控制_Success_设置95%_CONVENIENCE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111981?projectId=46')
    @pytest.mark.smoke
    def test_caseid_111981(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.dk.send_rke_maxsoc(950)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.valid,timeout=2)
        self.bus_comm.check_singal("backbonefr","IHUBackBoneFr12", 'LocalBookChrgnTarVal', 950)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb", 95.0)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)
        sleep(5)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.valid)
        sleep(5)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.no_valid)

    
    @allure.title("MaxSoc控制_Success_设置49%_DRIVING")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111981?projectId=46')
    @pytest.mark.smoke
    def test_caseid_111977(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.dk.send_rke_maxsoc(490)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.valid)
        self.bus_comm.check_singal("backbonefr","IHUBackBoneFr12", 'LocalBookChrgnTarVal', 490)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb", 49.0)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)
        sleep(5)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.valid)
        sleep(5)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.no_valid)


    @allure.title(" MaxSoc控制_Success_设置100%_ABANDONED")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111981?projectId=46')
    @pytest.mark.smoke
    def test_caseid_111976(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.dk.send_rke_maxsoc(1000)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.valid)
        self.bus_comm.check_singal("backbonefr","IHUBackBoneFr12", 'LocalBookChrgnTarVal', 1000)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb", 100.0)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)
        sleep(5)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.valid)
        sleep(5)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.no_valid)


    @allure.title("MaxSoc控制_Success_设置90%_ACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111981?projectId=46')
    @pytest.mark.sanity
    def test_caseid_111979(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.dk.send_rke_maxsoc(900)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.valid)
        self.bus_comm.check_singal("backbonefr","IHUBackBoneFr12", 'LocalBookChrgnTarVal', 900)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb", 90.0)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)
        sleep(5)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.valid)
        sleep(5)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.no_valid)

    @allure.title("MaxSoc控制_Success_设置85.5%_INACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111981?projectId=46')
    @pytest.mark.sanity
    def test_caseid_111978(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.dk.send_rke_maxsoc(855)
        self.io.driver_seat_present()
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.valid)
        self.bus_comm.check_singal("backbonefr","IHUBackBoneFr12", 'LocalBookChrgnTarVal', 855)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb", 85.5)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)
        sleep(5)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.valid)
        sleep(5)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.no_valid)

    
    @allure.title("MaxSoc控制_DelayFail_设置80.5%")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111981?projectId=46')
    @pytest.mark.full
    def test_caseid_111980(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.dk.send_rke_maxsoc(805)
        self.io.driver_seat_present()
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.valid)
        self.bus_comm.check_singal("backbonefr","IHUBackBoneFr12", 'LocalBookChrgnTarVal', 805)
        sleep(5)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb", 80.5)
        self.bus_comm.dk.ck_rke_resp(3, 1, "DelayFail", exec_type=3)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.valid)

    
    @allure.title("MaxSoc控制_Busy_设置100%执行中_ABANDONED")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111981?projectId=46')
    @pytest.mark.full
    def test_caseid_111975(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_maxsoc(1000)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        #self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.valid)
        self.bus_comm.check_singal("backbonefr","IHUBackBoneFr12", 'LocalBookChrgnTarVal', 1000)
        self.bus_comm.dk.empty_dk_data_queue()
        sleep(1)
        self.bus_comm.dk.send_rke_maxsoc(1000)
        logger.info("再次发送MaxSoc请求")
        self.bus_comm.dk.ck_rke_resp(3, 1, "SysBusy",exec_type=3)
        sleep(2)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb", 1000)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.valid)


    @allure.title("MaxSoc控制_DelayFail_设置63%")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111981?projectId=46')
    @pytest.mark.full
    def test_caseid_111974(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.dk.send_rke_maxsoc(630)
        self.io.driver_seat_present()
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.valid)
        self.bus_comm.check_singal("backbonefr","IHUBackBoneFr12", 'LocalBookChrgnTarVal', 630)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb", 70.0)
        self.bus_comm.dk.ck_rke_resp(3, 1, "DelayFail", exec_type=3,timeout=6)

    
    @allure.title("掉电之后RKE Max SOC控制")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111981?projectId=46')
    @pytest.mark.full
    def test_caseid_1987542(self):
        logger.info("------------------>复位BGM")
        self.io.io_reset_bgm()
        logger.info("------------------>复位BGM结束")
        sleep(15)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.dk.send_rke_maxsoc(1000)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.valid)
        self.bus_comm.check_singal("backbonefr","IHUBackBoneFr12", 'LocalBookChrgnTarVal', 1000)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb", 100.0)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)
        sleep(5)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.valid)
        sleep(5)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.no_valid)

    @allure.title("休眠之后RKE Max SOC控制")
    @pytest.mark.full
    def test_caseid_1987549(self):
        self.sd_tester.reset_bgm()#重启BGM代替休眠唤醒
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.dk.send_rke_maxsoc(1000)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.valid)
        self.bus_comm.check_singal("backbonefr","IHUBackBoneFr12", 'LocalBookChrgnTarVal', 1000)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb", 100.0)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)
        sleep(5)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.valid)
        sleep(5)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, NMSts.no_valid)
