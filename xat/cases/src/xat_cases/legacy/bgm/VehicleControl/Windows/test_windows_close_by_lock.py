#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_OuterRearView_ctrl.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/11/9 11:30
@Description: BGM车控车设外后视镜功能
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


@allure.feature("BGM车控车设")
@allure.story("车窗功能/锁车自动升窗")
@pytest.mark.run(order=1)
class TestWiperCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["CentralLockService_client","WindowService_client","KeyService_client","ResetSOAConfigService_client","WindowAppService_client","DoorService_client"])
        sleep(2)

    def before_each_func(self, ecu):
        self.bus_comm.ipdu.reset_check_results()
        self.sd_tester.write_ccp({561: 0x2})
        self.io.set_five_door_sts(Door.close)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=False)
        sleep(0.5)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        sleep(1)

    def after_each_func(self, ecu):
        sleep(3)

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    
    def trigger_outside_switch(self,pos:DoorPos):
        if pos.name == "Dirver":
            self.mix.push_door_outer_switch(DoorPos.Dirver, 2)
            self.io.trigger_door_outswitch_sts(Drvr=OutSwitchPressSts.Press)
            time.sleep(2)
            self.io.trigger_door_outswitch_sts(Drvr=OutSwitchPressSts.NoPress)
            self.bus_comm.check_door_opener_req(drv_opener=DoorOpenerReq.Idle, trigger_src=LockTrigerSource.NoTrigSrc)

    def trigger_walk_away_lock(self):
        self.sd_tester.write_ccp(ccp={94:0x80})
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave,value=2)
        sleep(1)
        self.bus_comm.dk.send_walk_away_lock_cmd()

    def set_windows_pre_condition(self,lock_sts:CenLockSts = CenLockSts.Unlock):
        self.mix.set_common_precontion()
        self.io.set_bgm_hardware_condition_to_default()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.bus_comm.set_five_door_opener_sts(door_opener=DoorOpenerSts.FullClsd)  # 设置bodycan上五个电动门均关闭
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)

    def get_window_close_req(self,check_signal,LockSource):
        self.bus_comm.check_signal_thread_start("bodycan","CemBodyFr68", check_signal)  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource)
        result_ori = self.bus_comm.check_signal_thread_stop(check_signal)  
        logger.info(f'获取到的原始数据 {check_signal} 为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))
        assert result[0] !=0

    @pytest.mark.smoke
    def test_caseid_119284(self):
        """
        验证按下车外驾驶位门开关窗户会自动短降
        """
        self.sd_tester.write_ccp({561: 0x2,94:0x02})
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.set_windows_pre_condition(lock_sts=CenLockSts.Lock)
        sleep(1)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.check_windows_short_drop_req(pos_drvr=WinShortDropReq.Open)

    @pytest.mark.smoke
    def test_caseid_1980048(self):
        """
        用蓝牙锁车时，如果副驾车窗处于打开16%位置时，验证BGM是否会控制被控车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_16,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.percent_20)
        sleep(1)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_20)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.close)

    @pytest.mark.smoke
    def test_caseid_1980047(self):
        """
        用远控锁车时，如果左后车窗处于打开20%位置时，验证BGM是否会控制被控车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.sd_tester.write_ccp({561: 0x2})
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.percent_20,pos_rire=WinPos.close)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_24)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.close)
    
    @pytest.mark.smoke
    def test_caseid_1980046(self):
        """
        用蓝牙锁车时，如果右后窗处于打开20%位置时，验证BGM是否会控制被控车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.percent_20)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_rire=WinPos.percent_24)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.close)

    @pytest.mark.smoke
    @pytest.mark.kv
    def test_caseid_119291(self):
        """
        设置锁车自动关窗功能开启，验证主驾驶位置门KV锁车之后会自动落窗（窗户全开）
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close)

    @pytest.mark.full
    @pytest.mark.kv
    def test_caseid_119290(self):
        """
        设置锁车自动关窗功能开启，验证副驾驶位置门KV锁车之后会自动落窗（窗户全开）
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval=2.5)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.close)

    @pytest.mark.full
    @pytest.mark.kv
    def test_caseid_119289(self):
        """
        设置锁车自动关窗功能开启，验证左后位置门KV锁车之后会自动落窗（窗户全开）
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.mix.push_door_outer_switch(pos=DoorPos.RearLeft,time_interval=2.5)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.close)

    @pytest.mark.full
    @pytest.mark.kv
    def test_caseid_119288(self):
        """
        设置锁车自动关窗功能开启，验证右后位置门KV锁车之后会自动落窗（窗户全开）
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.close)

    @pytest.mark.full
    @pytest.mark.kv
    def test_caseid_119287(self):
        """
        设置锁车自动关窗功能关闭，验证KV锁车之后会自动落窗（窗户全开）
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.check_win_without_pos_req(pos_drvr=WinPos.close)

    @pytest.mark.smoke
    @pytest.mark.kv
    def test_caseid_1979954(self):
        """
        按下门外开关锁车时，如果前排窗户16%，左后20%，右后全关时，验证BGM是否会控制前排和左后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_16,pos_pass=WinPos.percent_16,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_20)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_24,pos_rire=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_24,pos_rire=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)


    @pytest.mark.smoke
    @pytest.mark.kv
    def test_caseid_1979970(self):
        """
        按下门外开关锁车时，如果前排窗户16%，其余的全开时，验证BGM是否会控制前排车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_16,pos_pass=WinPos.percent_16,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.smoke
    @pytest.mark.kv
    def test_caseid_1979946(self):
        """
        按下门外开关锁车时，如果前排和左后96%，右后8%时，验证BGM是否会控制前排和左后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_96,pos_pass=WinPos.percent_96,pos_lere=WinPos.percent_96,pos_rire=WinPos.percent_12)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    @pytest.mark.kv
    def test_caseid_1979942(self):
        """
        按下门外开关锁车时，如果前排和右后60%，左后4%时，验证BGM是否会控制前排和右后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_60,pos_pass=WinPos.percent_60,pos_lere=WinPos.percent_4,pos_rire=WinPos.percent_60)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_64,pos_pass=WinPos.percent_64,pos_rire=WinPos.percent_64)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_64,pos_pass=WinPos.percent_64,pos_rire=WinPos.percent_64)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    @pytest.mark.kv
    def test_caseid_1979950(self):
        """
        按下门外开关锁车时，如果前排16%，右后20%，左后全关时，验证BGM是否会控制前排和左后车窗降低4%，并且前排车窗在2秒内未下降4%时，BGM是否会在2s超时时发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_16,pos_pass=WinPos.percent_16,pos_lere=WinPos.close,pos_rire=WinPos.percent_20)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_rire=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_rire=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)


    @pytest.mark.smoke
    @pytest.mark.kv
    def test_caseid_1979934(self):
        """
        按下门外开关锁车时，如果前排16%,后排20%时，验证BGM是否会控制所有车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_16,pos_pass=WinPos.percent_16,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_20)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_24,pos_rire=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_24,pos_rire=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    @pytest.mark.kv
    def test_caseid_1979982(self):
        """
        按下门外开关锁车时，如果主驾驶窗户96%，其余的4%时，验证BGM是否会控制主驾车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_96,pos_pass=WinPos.percent_4,pos_lere=WinPos.percent_4,pos_rire=WinPos.percent_4)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_100)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)


    @pytest.mark.full
    @pytest.mark.kv
    def test_caseid_1979986(self):
        """
        按下门外开关锁车时，如果主驾驶窗户60%，其余的全关时，验证BGM是否会控制主驾车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_60,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_64)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_64)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)


    @pytest.mark.full
    @pytest.mark.kv
    def test_caseid_1979974(self):
        """
        按下门外开关锁车时，如果主驾驶窗户16%，副驾12%，后排16%时，验证BGM是否会控制主驾车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_16,pos_pass=WinPos.percent_12,pos_lere=WinPos.percent_16,pos_rire=WinPos.percent_16)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_20)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    
    @pytest.mark.smoke
    @pytest.mark.kv
    def test_caseid_1979994(self):
        """
        按下门外开关锁车时，如果主驾驶窗户16%，其余的全开时，验证BGM是否会控制主驾车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_16,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_20)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    @pytest.mark.kv
    def test_caseid_1979978(self):
        """
        按下门外开关锁车时，如果主驾驶窗户16%，其余的12%时，验证BGM是否会控制主驾车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_16,pos_pass=WinPos.percent_12,pos_lere=WinPos.percent_12,pos_rire=WinPos.percent_12)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_20)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    
    @pytest.mark.smoke
    @pytest.mark.kv
    def test_caseid_1979930(self):
        """
        按下门外开关锁车时，如果主驾驶96%，副驾驶60%，左右20%，右后16%时，验证BGM是否会控制所有车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_96,pos_pass=WinPos.percent_60,pos_lere=WinPos.percent_24,pos_rire=WinPos.percent_20)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_64,pos_lere=WinPos.percent_28,pos_rire=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_64,pos_lere=WinPos.percent_28,pos_rire=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)


    @pytest.mark.full
    @pytest.mark.kv
    def test_caseid_1979958(self):
        """
        按下门外开关锁车时，如果主驾16%和左后20%，其余的全关时，验证BGM是否会控制主驾和左后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_16,pos_pass=WinPos.close,pos_lere=WinPos.percent_20,pos_rire=WinPos.close)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_20,pos_lere=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20,pos_lere=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)


    @pytest.mark.smoke
    @pytest.mark.kv
    def test_caseid_1980022(self):
        """
        按下门外开关锁车时，如果4窗户开8%时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_8,pos_pass=WinPos.percent_8,pos_lere=WinPos.percent_8,pos_rire=WinPos.percent_8)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    @pytest.mark.kv
    def test_caseid_1980010(self):
        """
        按下门外开关锁车时，副驾4%，其他全关时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_4,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    @pytest.mark.kv
    def test_caseid_1980014(self):
        """
        按下门外开关锁车时，前窗户全开,后窗全关时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)


    @pytest.mark.full
    @pytest.mark.kv
    def test_caseid_1980018(self):
        """
        按下门外开关锁车时，前窗户4%,后窗全关时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_4,pos_pass=WinPos.percent_4,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    @pytest.mark.kv
    def test_caseid_1979998(self):
        """
        按下门外开关锁车时，主驾和右后12%，其他全关时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_12,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.percent_12)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)


    @pytest.mark.full
    @pytest.mark.kv
    def test_caseid_1980006(self):
        """
        按下门外开关锁车时，主驾12%，其他全关时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_12,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)


    @pytest.mark.smoke
    @pytest.mark.kv
    def test_caseid_1979966(self):
        """
        按下门外开关锁车时，如果后排20%，其他全开时，验证BGM是否会控制后排车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_20)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_24,pos_rire=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_24,pos_rire=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)


    @pytest.mark.smoke
    def test_caseid_118126(self):
        """
        设置锁车自动关窗功能开启，验证离车锁车之会自动落窗（窗户全开）
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_four_windows_position(pos=WinPos.percent_100,time_wait=1)
        self.trigger_walk_away_lock()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.smoke
    def test_caseid_1980023(self):
        """
        触发离车落锁时，如果4窗户开4%时，验证BGM是否会直接发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_four_windows_position(pos=WinPos.percent_4,time_wait=1)
        self.trigger_walk_away_lock()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980007(self):
        """
        触发离车落锁时，右后4%，其他全关时，验证BGM是否会直接发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.percent_4)
        self.trigger_walk_away_lock()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.smoke
    def test_caseid_1979991(self):
        """
        触发离车落锁时，主驾和右后全开，其他全关时，验证BGM是否会直接发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.percent_100)
        self.trigger_walk_away_lock()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.smoke
    def test_caseid_1979963(self):
        """
        触发离车落锁时，如果后排60%，其他全开时，验证BGM是否会控制后排车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_60,pos_rire=WinPos.percent_60)
        self.trigger_walk_away_lock()
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_64,pos_rire=WinPos.percent_64)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_64,pos_rire=WinPos.percent_64)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.smoke
    def test_caseid_1979947(self):
        """
        触发离车落锁时，如果前排和左后60%，右后4%时，验证BGM是否会控制前排和左后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_60,pos_pass=WinPos.percent_60,pos_lere=WinPos.percent_60,pos_rire=WinPos.percent_4)
        self.trigger_walk_away_lock()
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_64,pos_pass=WinPos.percent_64,pos_lere=WinPos.percent_64)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_64,pos_pass=WinPos.percent_64,pos_lere=WinPos.percent_64)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.smoke
    def test_caseid_1979931(self):
        """
        触发离车落锁时，如果主驾驶16%，副驾驶20%，左右60%，右后96%时，验证BGM是否会控制所有车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_16,pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_60,pos_rire=WinPos.percent_96)
        self.trigger_walk_away_lock()
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_24,pos_lere=WinPos.percent_64,pos_rire=WinPos.percent_100)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_24,pos_lere=WinPos.percent_64,pos_rire=WinPos.percent_100)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    @pytest.mark.kv
    def test_caseid_1979927(self):
        """
        在门外开关关窗的过程中再发送远控锁车，查看BGM是否会忽略第二次请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        sleep(0.5)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.check_win_without_pos_req(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979926(self):
        """
        在蓝牙锁车关窗的过程中再发送远控关窗，查看BGM是否会忽略第二次请求
        """
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        sleep(1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        self.bus_comm.check_win_without_pos_req(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979925(self):
        """
        在远控关窗的过程中再发送离车自动关窗，查看BGM是否会忽略第二次请求
        """
        self.sd_tester.write_ccp({561: 0x2})
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        sleep(1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        self.bus_comm.check_win_without_pos_req(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979928(self):
        """
        NFC闭锁关窗后再发送离车关窗请求(上次命令执行中)，查看BGM是否会忽略第二次请求
        """
        self.sd_tester.write_ccp({561: 0x2})
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        sleep(1)
        self.trigger_walk_away_lock()
        self.bus_comm.check_win_without_pos_req(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)

    @pytest.mark.smoke
    def test_caseid_1980049(self):
        """
        用远控锁车时，如果主驾车窗处于打开16%位置时，验证BGM是否会控制被控车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.sd_tester.write_ccp({561: 0x2})
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_16,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_20)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close)

    @pytest.mark.smoke
    def test_caseid_1980020(self):
        """
        触发NFC闭锁时，前窗户12%,后窗户16%时，验证BGM是否会直接发出full close服务请求
        """
        self.sd_tester.write_ccp({561: 0x2})
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_12,pos_pass=WinPos.percent_12,pos_lere=WinPos.percent_16,pos_rire=WinPos.percent_16)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.smoke
    def test_caseid_1979995(self):
        """
        触发离车落锁时，主驾和右后全开，其他全关时，验证BGM是否会直接发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.percent_100)
        self.trigger_walk_away_lock()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.smoke
    @pytest.mark.kv
    def test_caseid_1979990(self):
        """
        按下门外开关锁车时，如果左后窗户20%，其余的全开时，验证BGM是否会控制左后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_100)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.smoke
    def test_caseid_1979988(self):
        """
        触发NFC闭锁时，如果右后窗户20%，其余的全开时，验证BGM是否会控制右后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.sd_tester.write_ccp({561: 0x2})
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.smoke
    def test_caseid_1979992(self):
        """
        触发NFC闭锁时，主驾和左后全开，其他全关时，验证BGM是否会直接发出full close服务请求
        """
        self.sd_tester.write_ccp({561: 0x2})
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.close,pos_lere=WinPos.percent_100,pos_rire=WinPos.close)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980059(self):
        """
        用蓝牙锁车时，如果左后车窗处于开4%位置时，验证BGM是否会直接发出full close服务请求
        """
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.percent_4,pos_rire=WinPos.close)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980002(self):
        """
        按下门外开关锁车时，左后16%，其他全关时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.percent_16,pos_rire=WinPos.close)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979962(self):
        """
        按下门外开关锁车时，如果前排窗户96%，其余的打开4%时，验证BGM是否会控制前排车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_96,pos_pass=WinPos.percent_96,pos_lere=WinPos.percent_4,pos_rire=WinPos.percent_4)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    
    @pytest.mark.full
    def test_caseid_1979938(self):
        """
        按下门外开关锁车时，如果后排和副驾驶96%，驾驶位4%时，验证BGM是否会控制后排和副驾车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_4,pos_pass=WinPos.percent_96,pos_lere=WinPos.percent_96,pos_rire=WinPos.percent_96)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_rire=WinPos.percent_100)
        sleep(1)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980062(self):
        """
        用远控锁车时，如果所有车窗处于全关位置时，验证BGM是否会直接发出full close服务请求
        """
        self.sd_tester.write_ccp({561: 0x2})
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_four_windows_position(pos=WinPos.close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980057(self):
        """
        用蓝牙锁车时，如果所有车窗处于开4%位置时，验证BGM是否会直接发出full close服务请求
        """
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_four_windows_position(pos=WinPos.close)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.close)

    @pytest.mark.sanity
    def test_caseid_1980036(self):
        """
        用远控锁车时，如果所有车窗处于打开20%位置时，验证BGM是否会控制被控车窗降低4%，但是被控车窗在2秒内一直未下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.sd_tester.write_ccp({561: 0x2})
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_four_windows_position(pos=WinPos.percent_20)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.percent_24)
        sleep(2)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980019(self):
        """
        触发离车落锁时，前窗户8%,后窗户4%时，验证BGM是否会直接发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_8,pos_pass=WinPos.percent_8,pos_lere=WinPos.percent_4,pos_rire=WinPos.percent_4)
        self.trigger_walk_away_lock()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980015(self):
        """
        触发离车落锁时，前窗户全开,后窗4%时，验证BGM是否会直接发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_4,pos_rire=WinPos.percent_4)
        self.trigger_walk_away_lock()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980011(self):
        """
        触发离车落锁时，副驾全开，其他全关时，验证BGM是否会直接发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.trigger_walk_away_lock()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980003(self):
        """
        触发离车落锁时，右后8%，其他全关时，验证BGM是否会直接发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.percent_8)
        self.trigger_walk_away_lock()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980000(self):
        """
        触发NFC闭锁时，主驾和左后4%，其他全关时，验证BGM是否会直接发出full close服务请求
        """
        self.sd_tester.write_ccp({561: 0x2})
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_4,pos_pass=WinPos.close,pos_lere=WinPos.percent_4,pos_rire=WinPos.close)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979999(self):
        """
        触发离车落锁时，副驾驾和右后4%，其他全关时，验证BGM是否会直接发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_4,pos_lere=WinPos.close,pos_rire=WinPos.percent_4)
        self.trigger_walk_away_lock()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979987(self):
        """
        触发离车落锁时，如果右后窗户20%，其余的全开时，验证BGM是否会控制右后车窗降低4%，并且被控车窗在2秒内未下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_20)
        self.trigger_walk_away_lock()
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.percent_24)
        sleep(2)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979983(self):
        """
        触发离车落锁时，如果右后窗户60%，其余的全关时，验证BGM是否会控制右后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.percent_60)
        self.trigger_walk_away_lock()
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.percent_64)
        sleep(1)
        self.bus_comm.set_windows_position(pos_rire=WinPos.percent_64)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979979(self):
        """
        触发离车落锁时，如果右后窗户96%，其余的全关时，验证BGM是否会控制右后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.percent_96)
        self.trigger_walk_away_lock()
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.percent_100)
        sleep(1)
        self.bus_comm.set_windows_position(pos_rire=WinPos.percent_100)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979976(self):
        """
        触发NFC闭锁时，如果左后窗户20%，其余的12%时，验证BGM是否会控制左后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.sd_tester.write_ccp({561: 0x2})
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_12,pos_pass=WinPos.percent_12,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_12)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979975(self):
        """
        触发离车落锁时，如果右后窗户20%，其余的12%时，验证BGM是否会控制右后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_12,pos_pass=WinPos.percent_12,pos_lere=WinPos.percent_12,pos_rire=WinPos.percent_20)
        self.trigger_walk_away_lock()
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_rire=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    
    @pytest.mark.full
    def test_caseid_1979972(self):
        """
        触发NFC闭锁时，如果左后窗户20%，前排12%，右后16%时，验证BGM是否会控制左后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.sd_tester.write_ccp({561: 0x2})
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_12,pos_pass=WinPos.percent_12,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_16)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979971(self):
        """
        触发离车落锁时，如果右后窗户20%，前排12%，左后16%时，验证BGM是否会控制右后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_12,pos_pass=WinPos.percent_12,pos_lere=WinPos.percent_16,pos_rire=WinPos.percent_20)
        self.trigger_walk_away_lock()
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_rire=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979968(self):
        """
        触发NFC闭锁时，如果前排窗户16%，其余的全开时，验证BGM是否会控制前排车窗降低4%，并且副驾车窗在2秒内未下降4%时，BGM是否会在2s超时时发出full close服务请求
        """
        self.sd_tester.write_ccp({561: 0x2})
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_16,pos_pass=WinPos.percent_16,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20)
        sleep(2)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979967(self):
        """
        触发离车落锁时，如果前排窗户16%，其余的全开时，验证BGM是否会控制前排车窗降低4%，并且主副驾车窗在2秒内未下降4%时，BGM是否会在2s超时时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_16,pos_pass=WinPos.percent_16,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.trigger_walk_away_lock()
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20)
        sleep(2)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979959(self):
        """
        触发离车落锁时，如果后排20%，其余的打开8%时，验证BGM是否会控制后排车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_8,pos_pass=WinPos.percent_8,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_20)
        self.trigger_walk_away_lock()
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_24,pos_rire=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_24,pos_rire=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979955(self):
        """
        触发离车落锁时，如果副驾和右后20%，其余的全8%时，验证BGM是否会控制副驾驾和右后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_20)
        self.trigger_walk_away_lock()
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.percent_24,pos_rire=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_24,pos_rire=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979951(self):
        """
        触发离车落锁时，如果前排和左后96%，右后16%时，验证BGM是否会控制前排和左后车窗降低4%，并且左后车窗在2秒内未下降4%时，BGM是否会在2s超时时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_96,pos_pass=WinPos.percent_96,pos_lere=WinPos.percent_96,pos_rire=WinPos.percent_16)
        self.trigger_walk_away_lock()
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100)
        sleep(2)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    
    @pytest.mark.full
    def test_caseid_1979944(self):
        """
        触发NFC闭锁时，如果前排窗户16%，右后20%，左后全关时，验证BGM是否会控制前排和左后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.sd_tester.write_ccp({561: 0x2})
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_16,pos_pass=WinPos.percent_16,pos_lere=WinPos.close,pos_rire=WinPos.percent_20)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_rire=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_rire=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979943(self):
        """
        触发离车落锁时，如果前排和右后20%，左后全开时，验证BGM是否会控制前排和右后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_20)
        self.trigger_walk_away_lock()
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_24,pos_pass=WinPos.percent_24,pos_rire=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_24,pos_pass=WinPos.percent_24,pos_rire=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979940(self):
        """
        触发NFC闭锁时，如果后排20%，副驾驶16%，驾驶位关时，验证BGM是否会控制前排和左后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.sd_tester.write_ccp({561: 0x2})
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_16,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_20)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_24,pos_rire=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_24,pos_rire=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979939(self):
        """
        触发离车落锁时，如果后排和副驾驶60%，驾驶位开时，验证BGM是否会控制后排和副驾驶车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_60,pos_lere=WinPos.percent_60,pos_rire=WinPos.percent_60)
        self.trigger_walk_away_lock()
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.percent_64,pos_lere=WinPos.percent_64,pos_rire=WinPos.percent_64)
        sleep(1)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_64,pos_lere=WinPos.percent_64,pos_rire=WinPos.percent_64)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979935(self):
        """
        触发离车落锁时，如果后排和驾驶96%，副驾驶位开4%时，验证BGM是否会控制后排和驾驶位车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.set_windows_pre_condition()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_96,pos_pass=WinPos.percent_4,pos_lere=WinPos.percent_96,pos_rire=WinPos.percent_96)
        self.trigger_walk_away_lock()
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_119282(self):
        """
        验证按下车外左后门开关窗户会自动短降,对应儿童锁状态处于关闭状态
        """
        self.sd_tester.write_ccp({561: 0x2})
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_four_windows_position(pos=WinPos.close)
        self.bus_comm.set_singal("bodycan","RldmBodyFr01","DoorLeReLockSts",1,wait_time=0.5)
        self.bus_comm.set("bodycan","RldmBodyFr01","ChdLockLeftSts",2)
        self.mix.push_door_outer_switch(pos=DoorPos.RearLeft,time_interval=0.5)
        self.bus_comm.check_windows_short_drop_req(pos_lere=WinShortDropReq.Open)

    @pytest.mark.full
    def test_caseid_119281(self):
        """
        验证按下车外右后门开关窗户会自动短降,对应儿童锁状态处于关闭状态
        """
        self.sd_tester.write_ccp({561: 0x2})
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_four_windows_position(pos=WinPos.close)
        self.bus_comm.set_singal("bodycan","RrdmBodyFr01","DoorRiReLockSts",1,wait_time=0.5)
        self.bus_comm.set("bodycan","RrdmBodyFr01","ChdLockRightSts",2)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=0.5)
        self.bus_comm.check_windows_short_drop_req(pos_rire=WinShortDropReq.Open)

    @pytest.mark.smoke
    def test_caseid_1980071(self):
        """
        用远控锁车时，如果主驾车窗处于全开位置时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.sd_tester.write_ccp({561: 0x2})
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.get_window_close_req("WinOpenDrvrReq",LockSource.Telm)

    @pytest.mark.smoke
    def test_caseid_1980070(self):
        """
        用蓝牙锁车时，如果副驾车窗处于全开位置时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_100)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.get_window_close_req("WinOpenPassReq",LockSource.RKE)
        # self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        # self.bus_comm.check_windows_position_req(pos_pass=WinPos.close)

    @pytest.mark.smoke
    def test_caseid_1980069(self):
        """
        用远控锁车时，如果左后车窗处于全开位置时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_100)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.get_window_close_req("WinOpenReLeReq",LockSource.Telm)
        # self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        # self.bus_comm.check_windows_position_req(pos_lere=WinPos.close)
        

    @pytest.mark.smoke
    def test_caseid_1980068(self):
        """
        用蓝牙锁车时，如果右后车窗处于全开位置时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_rire=WinPos.percent_100)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.close)

    @pytest.mark.smoke
    def test_caseid_1980067(self):
        """
        用远控锁车时，如果所有车窗处于全开位置时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980066(self):
        """
        用蓝牙锁车时，如果主驾车窗处于全关位置时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980065(self):
        """
        用远控锁车时，如果副驾车窗处于全关位置时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_pass=WinPos.close)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980064(self):
        """
        用蓝牙锁车时，如果左后车窗处于全关位置时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_lere=WinPos.close)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980063(self):
        """
        用远控锁车时，如果右后车窗处于全关位置时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_rire=WinPos.close)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980061(self):
        """
        用蓝牙锁车时，如果主驾车窗处于开4%位置时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_4)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close)

    @pytest.mark.sanity
    def test_caseid_1980060(self):
        """
        用远控锁车时，如果副驾车窗处于开4%位置时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_4)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980058(self):
        """
        用远控锁车时，如果副驾车窗处于开4%位置时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_rire=WinPos.percent_4)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980056(self):
        """
        用远控锁车时，如果主驾车窗处于开8%位置时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_8)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980055(self):
        """
        用蓝牙锁车时，如果副驾车窗处于开8%位置时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_8)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980054(self):
        """
        用蓝牙锁车时，如果左后车窗处于开8%位置时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_8)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980053(self):
        """
        用远控锁车时，如果右后车窗处于开8%位置时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_rire=WinPos.percent_8)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980052(self):
        """
        用蓝牙锁车时，如果所有车窗处于开8%位置时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_8,pos_pass=WinPos.percent_8,pos_lere=WinPos.percent_8,pos_rire=WinPos.percent_8)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980051(self):
        """
        用远控锁车时，如果左后车窗处于开12%位置时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_12)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980050(self):
        """
        用蓝牙锁车时，如果右后车窗处于开12%位置时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_rire=WinPos.percent_12)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980045(self):
        """
        用远控锁车时，如果主驾车窗处于打开20%位置时，验证BGM是否会控制被控车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_24)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close)

    
    @pytest.mark.full
    def test_caseid_1980044(self):
        """
        用蓝牙锁车时，如果副驾车窗处于打开20%位置时，验证BGM是否会控制被控车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_20)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_24)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980043(self):
        """
        用远控锁车时，如果左后车窗处于打开20%位置时，验证BGM是否会控制被控车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_20)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_24)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980042(self):
        """
        用蓝牙锁车时，如果右后窗处于打开20%位置时，验证BGM是否会控制被控车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_rire=WinPos.percent_20)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_rire=WinPos.percent_24)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.close)


    @pytest.mark.smoke
    def test_caseid_1980041(self):
        """
        用远控锁车时，如果全部车窗处于打开20%位置时，验证BGM是否会控制被控车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_20)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_24,pos_pass=WinPos.percent_24,pos_lere=WinPos.percent_24,pos_rire=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_24,pos_pass=WinPos.percent_24,pos_lere=WinPos.percent_24,pos_rire=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980040(self):
        """
        用蓝牙锁车时，如果主驾车窗处于打开20%位置时，验证BGM是否会控制被控车窗降低4%，但是被控车窗在2秒内一直未下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_24)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close)

    @pytest.mark.sanity
    def test_caseid_1980039(self):
        """
        用远控锁车时，如果副驾车窗处于打开20%位置时，验证BGM是否会控制被控车窗降低4%，但是被控车窗在2秒内一直未下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_20)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_24)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980038(self):
        """
        用蓝牙锁车时，如果左后车窗处于打开20%位置时，验证BGM是否会控制被控车窗降低4%，但是被控车窗在2秒内一直未下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_20)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_24)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980037(self):
        """
        用蓝牙锁车时，如果右后车窗处于打开20%位置时，验证BGM是否会控制被控车窗降低4%，但是被控车窗在2秒内一直未下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_rire=WinPos.percent_20)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_rire=WinPos.percent_24)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980035(self):
        """
        用蓝牙锁车时，如果主驾车窗处于打开80%位置时，验证BGM是否会控制被控车窗降低4%，但是被控车窗在2秒内一直未下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_80)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_84)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_84)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980034(self):
        """
        用远控锁车时，如果副驾车窗处于打开80%位置时，验证BGM是否会控制被控车窗降低4%，但是被控车窗在2秒内一直未下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_80)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.percent_84)
        sleep(1)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_84)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.close)
    
    @pytest.mark.full
    def test_caseid_1980033(self):
        """
        用蓝牙锁车时，如果左后车窗处于打开80%位置时，验证BGM是否会控制被控车窗降低4%，但是被控车窗在2秒内一直未下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_80)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_84)
        sleep(1)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_84)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980032(self):
        """
        用远控锁车时，如果右后车窗处于打开80%位置时，验证BGM是否会控制被控车窗降低4%，但是被控车窗在2秒内一直未下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_rire=WinPos.percent_80)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.percent_84)
        sleep(1)
        self.bus_comm.set_windows_position(pos_rire=WinPos.percent_84)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980031(self):
        """
        用蓝牙锁车时，如果全部车窗处于打开80%位置时，验证BGM是否会控制被控车窗降低4%，但是被控车窗在2秒内一直未下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_80,pos_pass=WinPos.percent_80,pos_lere=WinPos.percent_80,pos_rire=WinPos.percent_80)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_84,pos_pass=WinPos.percent_84,pos_lere=WinPos.percent_84,pos_rire=WinPos.percent_84)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_84,pos_pass=WinPos.percent_84,pos_lere=WinPos.percent_84,pos_rire=WinPos.percent_84)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980030(self):
        """
        用蓝牙锁车时，如果主驾车窗处于打开96%位置时，验证BGM是否会控制被控车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_96)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_100)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980029(self):
        """
        用远控锁车时，如果副驾车窗处于打开96%位置时，验证BGM是否会控制被控车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_96)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.percent_100)
        sleep(1)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_100)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980028(self):
        """
        用远控锁车时，如果副驾车窗处于打开96%位置时，验证BGM是否会控制被控车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_96)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.percent_100)
        sleep(1)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_100)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980027(self):
        """
        用远控锁车时，如果右后车窗处于打开96%位置时，验证BGM是否会控制被控车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_rire=WinPos.percent_96)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.percent_100)
        sleep(1)
        self.bus_comm.set_windows_position(pos_rire=WinPos.percent_100)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980026(self):
        """
        用蓝牙锁车时，如果所有车窗处于打开96%位置时，验证BGM是否会控制被控车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在2秒时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_96,pos_pass=WinPos.percent_96,pos_lere=WinPos.percent_96,pos_rire=WinPos.percent_96)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980024(self):
        """
        触发NFC闭锁时，如果4窗户全关时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)


    @pytest.mark.full
    def test_caseid_1980016(self):
        """
        触发NFC闭锁时，前窗户4%,后窗8%时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_4,pos_pass=WinPos.percent_4,pos_lere=WinPos.percent_8,pos_rire=WinPos.percent_8)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980012(self):
        """
        触发NFC闭锁时，主驾4%，其他全关时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_4,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980008(self):
        """
        触发NFC闭锁时，左后4%，其他全关时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.percent_4,pos_rire=WinPos.close)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1980004(self):
        """
        触发NFC闭锁时，左后8%，其他全关时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.percent_8,pos_rire=WinPos.close)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979996(self):
        """
        触发NFC闭锁时，主驾和左后全开，其他全关时，验证BGM是否会直接发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.close,pos_lere=WinPos.percent_100,pos_rire=WinPos.close)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979984(self):
        """
        触发NFC闭锁时，如果左后窗户60%，其余的全关时，验证BGM是否会控制左后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.percent_60,pos_rire=WinPos.close)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_64)
        sleep(1)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_64)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979980(self):
        """
        触发NFC闭锁时，如果左后窗户96%，其余的4%时，验证BGM是否会控制左后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_4,pos_pass=WinPos.percent_4,pos_lere=WinPos.percent_96,pos_rire=WinPos.percent_4)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_100)
        sleep(1)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_100)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.smoke
    def test_caseid_1979964(self):
        """
        触发NFC闭锁时，如果前排窗户60%，其余的全关时，验证BGM是否会控制前排车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_60,pos_pass=WinPos.percent_60,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_64,pos_pass=WinPos.percent_64)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_64,pos_pass=WinPos.percent_64)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979960(self):
        """
        触发NFC闭锁时，如果前排窗户20%，其余的打开8%时，验证BGM是否会控制前排车窗降低4%，并且被控车窗在2秒内下降8%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_8,pos_rire=WinPos.percent_8)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_24,pos_pass=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_24,pos_pass=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979956(self):
        """
        触发NFC闭锁时，如果副驾驾和左后96%，其余的全4%时，验证BGM是否会控制副驾驾和左后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_4,pos_pass=WinPos.percent_96,pos_lere=WinPos.percent_96,pos_rire=WinPos.percent_4)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100)
        sleep(1)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979952(self):
        """
        触发NFC闭锁时，如果前排和左后60%，右后4%，验证BGM是否会控制前排和左后车窗降低4%，并且副驾车窗在2秒内未下降4%时，BGM是否会在2s超时时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_60,pos_pass=WinPos.percent_60,pos_lere=WinPos.percent_60,pos_rire=WinPos.percent_4)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_64,pos_pass=WinPos.percent_64,pos_lere=WinPos.percent_64)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_64,pos_pass=WinPos.percent_64,pos_lere=WinPos.percent_64)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.smoke
    def test_caseid_1979948(self):
        """
        触发NFC闭锁时，如果前排和左后20%，右后全开时，验证BGM是否会控制前排和左后车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_24,pos_pass=WinPos.percent_24,pos_lere=WinPos.percent_24)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_24,pos_pass=WinPos.percent_24,pos_lere=WinPos.percent_24)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1979936(self):
        """
        触发NFC闭锁时，如果后排和驾驶60%，副驾驶位开时，验证BGM是否会控制后排和驾驶位车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_60,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_60,pos_rire=WinPos.percent_60)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_64,pos_lere=WinPos.percent_64,pos_rire=WinPos.percent_64)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_64,pos_lere=WinPos.percent_64,pos_rire=WinPos.percent_64)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)


    @pytest.mark.smoke
    def test_caseid_1979932(self):
        """
        触发NFC闭锁时，如果全部96%时，验证BGM是否会控制所有车窗降低4%，并且被控车窗在2秒内下降4%时，BGM是否会在下降4%时发出full close服务请求
        """
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_96,pos_pass=WinPos.percent_96,pos_lere=WinPos.percent_96,pos_rire=WinPos.percent_96)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_1892739(self):
        """
        验证当主驾驶处于短降状态，锁车后BGM会发出主驾短升请求
        """
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinShortDropReq.Open)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close)

    @pytest.mark.full
    def test_caseid_1892738(self):
        """
        验证按下车外驾驶位门开关窗户会自动短降，并且5s内窗户成功短降，并且门一直打开
        """
        self.sd_tester.write_ccp({561: 0x2,94:0x02})
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.set_windows_pre_condition(lock_sts=CenLockSts.Unlock)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.check_windows_short_drop_req(pos_drvr=WinShortDropReq.Open)
        sleep(3)
        self.bus_comm.check_windows_short_drop_req(pos_drvr=WinShortDropReq.Close)

    @pytest.mark.fail
    @pytest.mark.full
    def test_caseid_119279(self):
        """
        验证Apprch_近车解锁窗户会自动短降
        """
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        sleep(0.5)
        self.bus_comm.dk.send_approach_unlock_cmd()
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.check_windows_short_drop_req(pos_drvr=WinShortDropReq.Open)
        sleep(3)
        self.bus_comm.check_windows_short_drop_req(pos_drvr=WinShortDropReq.Close)

    @pytest.mark.smoke
    def test_caseid_119286(self):
        """
        设置锁车自动关窗功能开启，验证NFC锁车之后会自动落窗（窗户全开）
        """
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_119285(self):
        """
        设置锁车自动关窗功能关闭，验证NFC锁车之后会自动落窗（窗户全开）
        """
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.ukwn)

    @pytest.mark.smoke
    def test_caseid_119280(self):
        """
        验证NFC解锁窗户会自动短降
        """
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        sleep(0.5)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.check("bodycan","CemBodyFr103","ShortDropWinDrvrDoor", 2,timeout=2)
        sleep(3)
        self.bus_comm.check("bodycan","CemBodyFr103","ShortDropWinDrvrDoor", 1, timeout=2)

    @pytest.mark.full
    def test_caseid_118239(self):
        """
        当获4个窗户全关时获取4个窗户的位置(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.get_windows_postion(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)

    @pytest.mark.full
    def test_caseid_118238(self):
        """
        当获4个窗户打开20%时获取4个窗户的位置(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_20)
        self.soa.get_windows_postion(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_20)

    @pytest.mark.full
    def test_caseid_118237(self):
        """
        当获4个窗户全开时获取4个窗户的位置(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.get_windows_postion(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)

    @pytest.mark.full
    def test_caseid_118236(self):
        """
        当获主驾驶窗户全关时获取其窗户的位置(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close)
        self.soa.get_windows_postion(pos_drvr=WinPos.close)

    @pytest.mark.full
    def test_caseid_118235(self):
        """
        当获主驾驶窗户打开20%时获取其窗户的位置(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20)
        self.soa.get_windows_postion(pos_drvr=WinPos.percent_20)

    @pytest.mark.full
    def test_caseid_118234(self):
        """
        当获主驾驶窗户全开时获取其窗户的位置(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100)
        self.soa.get_windows_postion(pos_drvr=WinPos.percent_100)

    @pytest.mark.full
    def test_caseid_118233(self):
        """
        当获副驾驶窗户全关时获取其窗户的位置(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_pass=WinPos.close)
        self.soa.get_windows_postion(pos_pass=WinPos.close)

    @pytest.mark.full
    def test_caseid_118232(self):
        """
        当获副驾驶窗户打开20%时获取其窗户的位置(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_20)
        self.soa.get_windows_postion(pos_pass=WinPos.percent_20)

    @pytest.mark.full
    def test_caseid_118231(self):
        """
        当获副驾驶窗户全开时获取其窗户的位置(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_100)
        self.soa.get_windows_postion(pos_lere=WinPos.percent_100)

    @pytest.mark.full
    def test_caseid_118230(self):
        """
        当获左后窗户全关时获取其窗户的位置(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_lere=WinPos.close)
        self.soa.get_windows_postion(pos_lere=WinPos.close)

    @pytest.mark.full
    def test_caseid_118229(self):
        """
        当获左后窗户打开20%时获取其窗户的位置(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_20)
        self.soa.get_windows_postion(pos_lere=WinPos.percent_20)

    @pytest.mark.full
    def test_caseid_118228(self):
        """
        当获左后窗户全开时获取其窗户的位置(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_lere=WinPos.percent_100)
        self.soa.get_windows_postion(pos_lere=WinPos.percent_100)

    @pytest.mark.full
    def test_caseid_118227(self):
        """
        当获右后窗户全关时获取其窗户的位置(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_rire=WinPos.close)
        self.soa.get_windows_postion(pos_rire=WinPos.close)

    @pytest.mark.full
    def test_caseid_118226(self):
        """
        当获右后窗户打开20%时获取其窗户的位置(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_rire=WinPos.percent_20)
        self.soa.get_windows_postion(pos_rire=WinPos.percent_20)

    @pytest.mark.full
    def test_caseid_118225(self):
        """
        当获右后窗户全开时获取其窗户的位置(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_rire=WinPos.percent_100)
        self.soa.get_windows_postion(pos_rire=WinPos.percent_100)

    @pytest.mark.full
    def test_caseid_118224(self):
        """
        当获4个窗户位置不同时获取4个窗户的位置(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_40,pos_lere=WinPos.percent_80,pos_rire=WinPos.percent_100)
        self.soa.get_windows_postion(pos_drvr=WinPos.close,pos_pass=WinPos.percent_40,pos_lere=WinPos.percent_80,pos_rire=WinPos.percent_100)


    @pytest.mark.full
    def test_caseid_118125(self):
        """
        设置锁车自动关窗功能开启，验证锁车之会自动落窗（窗户只开4%）
        """
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_4,pos_pass=WinPos.percent_4,pos_lere=WinPos.percent_4,pos_rire=WinPos.percent_4)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.trigger_walk_away_lock()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_118124(self):
        """
        设置锁车自动关窗功能开启，验证锁车之会自动落窗（只有主驾驶位窗口开着）
        """
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.trigger_walk_away_lock()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_118123(self):
        """
        设置锁车自动关窗功能开启，验证锁车之会自动落窗（只有副驾驶位窗口开着）
        """
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.trigger_walk_away_lock()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_118122(self):
        """
        设置锁车自动关窗功能开启，验证锁车之会自动落窗（只有左后窗口开着）
        """
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.percent_100,pos_rire=WinPos.close)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.trigger_walk_away_lock()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_118121(self):
        """
        设置锁车自动关窗功能开启，验证锁车之会自动落窗（只有右后窗口开着）
        """
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.trigger_walk_away_lock()
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)

    @pytest.mark.full
    def test_caseid_118120(self):
        """
        设置锁车自动关窗功能关闭，验证锁车之会自动落窗（窗户全开）
        """
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.trigger_walk_away_lock()
        self.bus_comm.check_windows_position_req(pos_drvr = WinPos.ukwn, pos_pass=WinPos.ukwn, pos_lere=WinPos.ukwn, pos_rire=WinPos.ukwn)

    @pytest.mark.full
    def test_caseid_119283(self):
        """
        验证按下车外副驶位门开关窗户会自动短降
        """
        self.sd_tester.write_ccp({561: 0x2,94:0x02})
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.set_windows_pre_condition(lock_sts=CenLockSts.Lock)
        sleep(1)
        self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval=0.5)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        self.bus_comm.check_windows_short_drop_req(pos_pass=WinShortDropReq.Open)