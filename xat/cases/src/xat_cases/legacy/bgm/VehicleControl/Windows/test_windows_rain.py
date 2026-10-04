#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_windows_rain.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/11/9 11:30
@Description: BGM车控车设窗户下雨直接用例
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
from xat_ecu.api.constants.common import *


@allure.feature("BGM车控车设/车窗功能")
@allure.story("雨天关窗")
@pytest.mark.run(order=1)
class TestWiperCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["CentralLockService_client","WindowService_client","KeyService_client","ResetSOAConfigService_client","WindowAppService_client"])
        sleep(2)

    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.io.set_five_door_sts(Door.close)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=False)
        sleep(0.5)
        self.bus_comm.set_rain_detect_sts(False)
        sleep(1)

    def after_each_func(self, ecu):
        sleep(3)

    def after_class(self, ecu):
        self.soa.stop_get_wiper_switch_sts()
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        

    def trigger_auto_close_wins_by_rain(self,usage_mode:UsageMode = UsageMode.INACTIVE):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=False)
        self.sd_tester.change_usage_mode(usage_mode)
        sleep(0.5)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(1)
        self.bus_comm.wakeup_lin1()
        sleep(1)
        self.bus_comm.set_rain_detect_sts(False)
        sleep(1)
        self.bus_comm.set_rain_detect_sts(True)
        
    def set_windows_pre_condition(self,usage_mode:UsageMode = UsageMode.INACTIVE,car_mode:CarMode = CarMode.NORMAL,lock_sts:CenLockSts = CenLockSts.Unlock):
        self.mix.set_common_precontion(usage_mode=usage_mode,car_mode=car_mode)
        self.io.set_bgm_hardware_condition_to_default()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.bus_comm.set_five_door_opener_sts(door_opener=DoorOpenerSts.FullClsd)  # 设置bodycan上五个电动门均关闭
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)

    @pytest.mark.smoke
    def test_caseid_1980098(self):
        """
        设置雨天自动化关窗功能开启
        """
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=False,time_wait=1)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)


    @pytest.mark.smoke
    def test_caseid_1980097(self):
        """
        "设置雨天自动化关窗功能开启"
        """
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True,time_wait=1)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=False)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=False)

    @pytest.mark.smoke
    @pytest.mark.rain
    def test_caseid_1980025(self):
        """
        触发雨天自动关窗时，如果4窗户全开时，验证BGM是否会直接发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_four_windows_position(pos=WinPos.percent_100,time_wait=1)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)
    
    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1979965(self):
        """
        触发雨天自动关窗时，如果后排16%，其他全开时，验证BGM是否会直接发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_16,pos_rire=WinPos.percent_16)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.smoke
    @pytest.mark.rain
    def test_caseid_1979961(self):
        """
        触发雨天自动关窗时，如果后排96%，其余的打开4%时，验证BGM是否会控制后排车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_4,pos_pass=WinPos.percent_4,pos_lere=WinPos.percent_96,pos_rire=WinPos.percent_96)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_4,pos_pass=WinPos.percent_4,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1980001(self):
        """
        触发雨天自动关窗时，右后16%，其他全关时，验证BGM是否会直接发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.percent_16)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)


    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1980009(self):
        """
        触发雨天自动关窗时，左后全开，其他全关时，验证BGM是否会直接发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.percent_100,pos_rire=WinPos.close)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1979989(self):
        """
        触发雨天自动关窗时，如果左后窗户20%，其余的全开时，验证BGM是否会控制左后车窗降低4%，并且被控车窗在2秒内未下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_100)
        self.trigger_auto_close_wins_by_rain()
        sleep(2)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    
    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1979961(self):
        """
        触发雨天自动关窗时，如果后排96%，其余的打开4%时，验证BGM是否会控制后排车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_4,pos_pass=WinPos.percent_4,pos_lere=WinPos.percent_96,pos_rire=WinPos.percent_96)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        sleep(1.5)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1979937(self):
        """
        触发雨天自动关窗时，如果后排20%，驾驶16%，副驾驶位关时，验证BGM是否会控制后排和驾驶位车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_16,pos_pass=WinPos.close,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_20)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_20,pos_lere=WinPos.percent_24,pos_rire=WinPos.percent_24)
        sleep(1.5)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20,pos_lere=WinPos.percent_24,pos_rire=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1979965(self):
        """
        触发雨天自动关窗时，如果后排20%，其他全开时，验证BGM是否会直接发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_20)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_24,pos_rire=WinPos.percent_24)
        sleep(1.5)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_24,pos_rire=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1979981(self):
        """
        触发雨天自动关窗时，如果副驾驶窗户96%，其余的4%时，验证BGM是否会控制副驾车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_4,pos_pass=WinPos.percent_96,pos_lere=WinPos.percent_4,pos_rire=WinPos.percent_4)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.percent_100)
        sleep(1.5)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_100)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1979985(self):
        """
        触发雨天自动关窗时，如果副驾驶窗户60%，其余的全关时，验证BGM是否会控制副驾车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_60,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.percent_64)
        sleep(1.5)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_64)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    
    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1979977(self):
        """
        触发雨天自动关窗时，如果副驾驶窗户16%，其余的8%时，验证BGM是否会控制副驾车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_8,pos_pass=WinPos.percent_16,pos_lere=WinPos.percent_8,pos_rire=WinPos.percent_8)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.percent_20)
        sleep(1.5)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_20)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)


    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1979973(self):
        """
        触发雨天自动关窗时，如果副驾驶窗户12%，主驾8%，后排12%时，验证BGM是否会控制副驾车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_60,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.percent_64)
        sleep(1.5)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_64)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)


    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1979969(self):
        """
        触发雨天自动关窗时，如果前排窗户16%，其余的全开时，验证BGM是否会控制前排车窗降低4%，并且主驾车窗在2秒内未下降4%时，BGM是否会在2s超时时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_16,pos_pass=WinPos.percent_16,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20)
        sleep(1.5)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)


    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1979953(self):
        """
        触发雨天自动关窗时，如果前排和左后20%，右后全开，验证BGM是否会控制前排和左后车窗降低4%，并且主驾车窗在2秒内未下降4%时，BGM是否会在2s超时时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_100)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_24,pos_pass=WinPos.percent_24,pos_lere=WinPos.percent_24)
        sleep(2)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1979945(self):
        """
        触发雨天自动关窗时，如果前排和左后20%，右后全开时，验证BGM是否会控制前排和左后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_100)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_24,pos_pass=WinPos.percent_24,pos_lere=WinPos.percent_24)
        sleep(1.5)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_24,pos_pass=WinPos.percent_24,pos_lere=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)


    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1979941(self):
        """
        触发雨天自动关窗时，如果前排和右后96%，左后8%时，验证BGM是否会控制前排和右后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_96,pos_pass=WinPos.percent_96,pos_lere=WinPos.percent_8,pos_rire=WinPos.percent_96)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_rire=WinPos.percent_100)
        sleep(1.5)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    
    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1979949(self):
        """
        触发雨天自动关窗时，如果前排和右后20%，左后全开时，验证BGM是否会控制前排和左后车窗降低4%，并且前排和左后在2秒内未下降4%时，BGM是否会在2s超时时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_20)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_24,pos_pass=WinPos.percent_24,pos_rire=WinPos.percent_24)
        sleep(2)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)


    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1979929(self):
        """
        触发雨天自动关窗时，如果前排20%，后排96%时，验证BGM是否会控制所有车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_96,pos_rire=WinPos.percent_96)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_24,pos_pass=WinPos.percent_24,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        sleep(1.5)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_24,pos_pass=WinPos.percent_24,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    
    @pytest.mark.smoke
    @pytest.mark.rain
    def test_caseid_1979933(self):
        """
        触发雨天自动关窗时，如果全部60%时，验证BGM是否会控制所有车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_60,pos_pass=WinPos.percent_60,pos_lere=WinPos.percent_60,pos_rire=WinPos.percent_60)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_64,pos_pass=WinPos.percent_64,pos_lere=WinPos.percent_64,pos_rire=WinPos.percent_64)
        sleep(1.5)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_64,pos_pass=WinPos.percent_64,pos_lere=WinPos.percent_64,pos_rire=WinPos.percent_64)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)


    @pytest.mark.smoke
    @pytest.mark.rain
    def test_caseid_1979993(self):
        """
        触发雨天自动关窗时，如果主驾驶窗户16%，其余的全开时，验证BGM是否会控制主驾车窗降低4%，并且被控车窗在2秒内未下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_16,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_20)
        sleep(1.5)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    
    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1979957(self):
        """
        触发雨天自动关窗时，如果主驾和右后60%，其余的全开时，验证BGM是否会控制主驾和右后车窗降低4%，并且后排车窗在2秒内未下降4%时，BGM是否会在2s超时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_60,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_60)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_64,pos_rire=WinPos.percent_64)
        sleep(1.5)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_64,pos_rire=WinPos.percent_64)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    
    @pytest.mark.smoke
    @pytest.mark.rain
    def test_caseid_1979997(self):
        """
        触发雨天自动关窗时，副驾驾和左后8%，其他全关时，验证BGM是否会直接发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_8,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.percent_8)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1980005(self):
        """
        触发雨天自动关窗时，副驾12%，其他全关时，验证BGM是否会直接发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_12,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    
    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1980021(self):
        """
        触发雨天自动关窗时，前窗户全开,后窗户12%时，验证BGM是否会直接发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_12,pos_rire=WinPos.percent_12)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)
    
    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1980017(self):
        """
        触发雨天自动关窗时，前窗户全关,后窗4%时，验证BGM是否会直接发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.percent_4,pos_rire=WinPos.percent_4)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)
    
    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1980013(self):
        """
        触发雨天自动关窗时，主驾全开，其他全关时，验证BGM是否会直接发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.trigger_auto_close_wins_by_rain()
        sleep(0.5)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

   
    @pytest.mark.full
    @pytest.mark.rain_tcam
    def test_caseid_1980080(self):
        """
        验证有下雨时BGM能否将下雨关窗的结果通知反馈给TCAM,当只有右后窗户未及时关闭(Car Mode=Normal、UsageMode=Abandoned)
        """
        self.set_windows_pre_condition()
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_40,pos_lere=WinPos.percent_80,pos_rire=WinPos.percent_100)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.percent_4)
        sleep(2.8)
        self.bus_comm.check_without_close_win_dueto_rain_req()

    @pytest.mark.full
    @pytest.mark.rain_tcam
    def test_caseid_1980081(self):
        """
        验证有下雨时BGM能否将下雨关窗的结果通知反馈给TCAM,当只有左后窗户未及时关闭(Car Mode=Normal、UsageMode=Abandoned)
        """
        self.set_windows_pre_condition()
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_40,pos_lere=WinPos.percent_80,pos_rire=WinPos.percent_100)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.percent_4,pos_rire=WinPos.close)
        sleep(2.8)
        self.bus_comm.check_without_close_win_dueto_rain_req()


    @pytest.mark.full
    @pytest.mark.rain_tcam
    def test_caseid_1980082(self):
        """
        验证有下雨时BGM能否将下雨关窗的结果通知反馈给TCAM,当只有副驾驶窗户未及时关闭(Car Mode=Normal、UsageMode=Abandoned)
        """
        self.set_windows_pre_condition()
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_40,pos_lere=WinPos.percent_80,pos_rire=WinPos.percent_100)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_4,pos_lere=WinPos.close,pos_rire=WinPos.close)
        sleep(2.8)
        self.bus_comm.check_without_close_win_dueto_rain_req()

    
    @pytest.mark.full
    @pytest.mark.rain_tcam
    def test_caseid_1980083(self):
        """
        验证有下雨时BGM能否将下雨关窗的结果通知反馈给TCAM,当只有主驾驶窗户未及时关闭(Car Mode=Normal、UsageMode=Abandoned)
        """
        self.set_windows_pre_condition()
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_40,pos_lere=WinPos.percent_80,pos_rire=WinPos.percent_100)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_4,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        sleep(2.8)
        self.bus_comm.check_without_close_win_dueto_rain_req()

    @pytest.mark.sanity
    @pytest.mark.rain_tcam
    def test_caseid_1980084(self):
        """
        验证有下雨时BGM能否将下雨关窗的结果通知反馈给TCAM,当4窗户都未及时关闭(Car Mode=Normal、UsageMode=Abandoned)
        """
        self.set_windows_pre_condition()
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_40,pos_lere=WinPos.percent_80,pos_rire=WinPos.percent_100)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_40,pos_lere=WinPos.percent_80,pos_rire=WinPos.percent_100)
        sleep(2.8)
        self.bus_comm.check_without_close_win_dueto_rain_req()


    @pytest.mark.smoke
    @pytest.mark.rain_tcam
    def test_caseid_1980085(self):
        """
        验证有下雨时BGM能否将下雨关窗的结果通知反馈给TCAM,当4窗户都及时关闭(Car Mode=Normal、UsageMode=Abandoned)
        """
        self.set_windows_pre_condition()
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_40,pos_lere=WinPos.percent_80,pos_rire=WinPos.percent_100)
        self.trigger_auto_close_wins_by_rain()
        sleep(2.5)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.check_close_win_dueto_rain_sts(True)
        # self.bus_comm.check_without_close_win_dueto_rain_req()

    
    @pytest.mark.sanity
    @pytest.mark.rain_tcam
    def test_caseid_1980079(self):
        """
        验证有下雨时BGM能否将下雨关窗的结果通知反馈给TCAM,当4窗户都及时关闭(Car Mode=Normal、UsageMode=Inactive)
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_40,pos_lere=WinPos.percent_80,pos_rire=WinPos.percent_100)
        self.trigger_auto_close_wins_by_rain()
        sleep(2.5)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.percent_100)
        self.bus_comm.check_close_win_dueto_rain_sts(True)

    @pytest.mark.full
    @pytest.mark.rain_tcam
    def test_caseid_1980078(self):
        """
        验证有下雨时BGM能否将下雨关窗的结果通知反馈给TCAM,当4窗户都及时关闭(Car Mode=Normal、UsageMode=Convenience)
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_40,pos_lere=WinPos.percent_80,pos_rire=WinPos.percent_100)
        self.trigger_auto_close_wins_by_rain()
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(2.5)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.check_close_win_dueto_rain_sts(True)


    @pytest.mark.full
    @pytest.mark.rain_tcam
    def test_caseid_1980077(self):
        """
        验证有下雨时BGM能否将下雨关窗的结果通知反馈给TCAM,当4窗户都及时关闭(Car Mode=Normal、UsageMode=Active)
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_40,pos_lere=WinPos.percent_80,pos_rire=WinPos.percent_100)
        self.trigger_auto_close_wins_by_rain()
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        sleep(2.5)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.check_close_win_dueto_rain_sts(True)

    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1980096(self):
        """
        模拟下雨时获取下雨自动关窗请求状态以及对应事件上报(Car Mode=Normal、UsageMode=Abandoned)
        """
        self.set_windows_pre_condition(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_four_windows_position(pos=WinPos.percent_100,time_wait=1)
        self.trigger_auto_close_wins_by_rain()
        self.soa.get_and_event_check_rain_auto_close_window_req(sts=RainCloseWinReq.Close)

    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1980089(self):
        """
        模拟下雨时查询是否有下雨通知(Car Mode=Transport、UsageMode=Inactive)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_four_windows_position(pos=WinPos.percent_100,time_wait=1)
        self.trigger_auto_close_wins_by_rain()
        self.soa.event_check_not_rain_auto_close_window_req()

    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1980095(self):
        """
        模拟下雨时获取下雨自动关窗请求状态以及对应事件上报(Car Mode=Normal、UsageMode=Abandoned)
        """
        self.bus_comm.set_four_windows_position(pos=WinPos.percent_100,time_wait=1)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=False)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ABANDONED)
        sleep(0.5)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(1)
        self.bus_comm.wakeup_lin1()
        sleep(1)
        self.bus_comm.set_rain_detect_sts(False)
        sleep(1)
        self.soa.get_rain_auto_close_window_req(sts=RainCloseWinReq.NoRequest)

    @pytest.mark.smoke
    @pytest.mark.rain
    def test_caseid_1980094(self):
        """
        模拟下雨时查询是否有下雨通知(Car Mode=Normal、UsageMode=Abandoned)
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_four_windows_position(pos=WinPos.percent_100,time_wait=1)
        self.trigger_auto_close_wins_by_rain(usage_mode=UsageMode.ABANDONED)
        self.soa.event_check_rain_auto_close_window_req(sts=RainCloseWinReq.Close)

    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1980093(self):
        """
        模拟下雨时查询是否有下雨通知(Car Mode=Normal、UsageMode=Inactive)
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_four_windows_position(pos=WinPos.percent_100,time_wait=1)
        self.trigger_auto_close_wins_by_rain(usage_mode=UsageMode.INACTIVE)
        self.soa.event_check_rain_auto_close_window_req(sts=RainCloseWinReq.Close)

    
    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1980092(self):
        """
        模拟下雨时查询是否有下雨通知(Car Mode=Normal、UsageMode=Convenience)
        """
        self.set_windows_pre_condition(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_four_windows_position(pos=WinPos.percent_100,time_wait=1)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.bus_comm.wakeup_lin1()
        sleep(0.1)
        self.bus_comm.set_rain_detect_sts(False)
        sleep(1)
        self.bus_comm.set_rain_detect_sts(True)
        self.soa.event_check_not_rain_auto_close_window_req()

    
    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1980091(self):
        """
        模拟下雨时查询是否有下雨通知(Car Mode=Normal、UsageMode=Active)
        """
        self.set_windows_pre_condition(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_four_windows_position(pos=WinPos.percent_100,time_wait=1)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.bus_comm.wakeup_lin1()
        sleep(0.1)
        self.bus_comm.set_rain_detect_sts(False)
        sleep(1)
        self.bus_comm.set_rain_detect_sts(True)
        self.soa.event_check_not_rain_auto_close_window_req()

    
    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1980090(self):
        """
        模拟下雨时查询是否有下雨通知(Car Mode=Normal、UsageMode=Driving)
        """
        self.set_windows_pre_condition(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_four_windows_position(pos=WinPos.percent_100,time_wait=1)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.bus_comm.wakeup_lin1()
        sleep(0.1)
        self.bus_comm.set_rain_detect_sts(False)
        sleep(1)
        self.bus_comm.set_rain_detect_sts(True)
        self.soa.event_check_not_rain_auto_close_window_req()

    
    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1980089(self):
        """
        模拟下雨时查询是否有下雨通知(Car Mode=Transport、UsageMode=Inactive)
        """
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.set_windows_pre_condition(car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_four_windows_position(pos=WinPos.percent_100,time_wait=1)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.bus_comm.wakeup_lin1()
        sleep(0.1)
        self.bus_comm.set_rain_detect_sts(False)
        sleep(1)
        self.bus_comm.set_rain_detect_sts(True)
        self.soa.event_check_not_rain_auto_close_window_req()

    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1980088(self):
        """
        模拟下雨时查询是否有下雨通知(Car Mode=Factory、UsageMode=Inactive)
        """
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_four_windows_position(pos=WinPos.percent_100,time_wait=1)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.bus_comm.wakeup_lin1()
        sleep(0.1)
        self.bus_comm.set_rain_detect_sts(False)
        sleep(1)
        self.bus_comm.set_rain_detect_sts(True)
        self.soa.event_check_not_rain_auto_close_window_req()


    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1980087(self):
        """
        模拟下雨时查询是否有下雨通知(Car Mode=Dyno、UsageMode=Inactive)
        """
        self.bus_comm.set_four_windows_position(pos=WinPos.percent_100,time_wait=1)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.bus_comm.wakeup_lin1()
        sleep(0.1)
        self.bus_comm.set_rain_detect_sts(False)
        sleep(1)
        self.bus_comm.set_rain_detect_sts(True)
        self.soa.event_check_not_rain_auto_close_window_req()


    @pytest.mark.full
    @pytest.mark.rain
    def test_caseid_1980086(self):
        """
        模拟下雨时查询是否有下雨通知(Car Mode=Crash、UsageMode=Inactive)
        """
        self.bus_comm.set_four_windows_position(pos=WinPos.percent_100,time_wait=1)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.bus_comm.wakeup_lin1()
        sleep(0.1)
        self.bus_comm.set_rain_detect_sts(False)
        sleep(1)
        self.bus_comm.set_rain_detect_sts(True)
        self.soa.event_check_not_rain_auto_close_window_req()

    @pytest.mark.sanity
    def test_caseid_1991439(self):
        """
        Inactive&naomal 检测到雨天关窗事件，WinFctReq=on,60s后置位off
        """
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.check("infocanfd","BgmInfoCanFdDevFr02","WinFctReq",1)
        sleep(60)
        self.bus_comm.check("infocanfd","BgmInfoCanFdDevFr02","WinFctReq",0)

    @pytest.mark.smoke
    def test_caseid_1991432(self):
        """
        检测到下雨，锁车后自动关窗
        """
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr03",'RainDetected', 1)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    
    @pytest.mark.full
    def test_caseid_1992553(self):
        """
        窗户全开，先通过NFC锁车过程中，在通过远控锁车，窗户正常关闭
        """
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)


    @pytest.mark.full
    def test_caseid_1992555(self):
        """
        窗户全开，先通过雨天自动关窗过程中，在通过NFC锁车，窗户正常关闭
        """
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr03",'RainDetected', 1)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1992556(self):
        """
        窗户全开，先通过雨天自动关窗过程中，在通过远控锁车，窗户正常关闭
        """
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr03",'RainDetected', 1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.sanity
    def test_caseid_1989486(self):
        """
        气候控制打开/关闭
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set("bodycan","CcmBodyFr44","WinAndRoofReqFrmClima",2)
        self.bus_comm.check("infocanfd","BgmInfoCanFdFr22","WinGlbCmd1",2)
        self.bus_comm.set("bodycan","CcmBodyFr44","WinAndRoofReqFrmClima",1)
        self.bus_comm.check("infocanfd","BgmInfoCanFdFr22","WinGlbCmd1",1)
        sleep(0.5)
        self.bus_comm.check("infocanfd","BgmInfoCanFdFr22","WinGlbCmd1",0)