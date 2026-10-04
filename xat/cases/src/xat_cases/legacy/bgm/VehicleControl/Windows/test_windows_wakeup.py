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


@allure.feature("车控车设")
@allure.story("后视镜功能")
@pytest.mark.run(order=1)
class TestWiperCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["WindowService_client","WindowAppService_client","KeyService_client","CentralLockService_client"])
        sleep(2)

    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        sleep(1.5)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=False)
        sleep(0.5)
        self.bus_comm.set_rain_detect_sts(False)
        sleep(1)
        
        
    def after_each_func(self, ecu):
        self.io.set_door(Drvr=Door.close)
        sleep(3)
        self.bus_comm.set_rain_detect_sts(False)

    def after_class(self, ecu):
        self.soa.stop_get_wiper_switch_sts()
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        
    def set_windows_signal_ub_false(self,drvr_pos,pass_pos,lere_pos,rire_pos):
        self.bus_comm.set("bodycan", "DdmBodyFr04", 'WinPosnStsAtDrvr',drvr_pos,ub_flag=False)
        self.bus_comm.set("bodycan", "PdmBodyFr01", 'WinPosnStsAtPass',pass_pos,ub_flag=False)
        self.bus_comm.set("bodycan", "RldmBodyFr01", 'WinPosnStsAtReLe',lere_pos,ub_flag=False)
        self.bus_comm.set("bodycan", "RrdmBodyFr01", 'WinPosnStsAtReRi',rire_pos,ub_flag=False)

    def wakeup(self):
        sleep(0.5)
        logger.info(f'连接诊断激活线')
        self.io.bgm_diag_line_up()
        self.io.tcam_kl15_up()
        sleep(35)  # 等待日志打印完整，否则日志获取不全
        self.sd_tester.sd_tester.tester_present()
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.check_four_door_and_tailgate_hood_sts(Door.close, DoorPos.All)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)

    # @pytest.mark.full
    # def test_caseid_1988218(self):
    #     """
    #     锁车自动关窗记忆-整车休眠后，锁车自动关窗
    #     """
    #     self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
    #     self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
    #     self.mix.network_sleep()
    #     self.wakeup()
    #     sleep(30)
    #     self.bus_comm.check_multiple_signals_thread_start([("bodycan",'CemBodyFr68','WinOpenDrvrReq',1), ("bodycan",'CemBodyFr68','WinOpenPassReq',1), ("bodycan",'CemBodyFr68','WinOpenReLeReq',1), ("bodycan",'CemBodyFr68','WinOpenReRiReq',1)],timeout=15)
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
    #     sleep(0.5)
    #     self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
    #     # sleep(3)
    #     # self.bus_comm.set_vehspd_gear(vehspd=3.0)
    #     # self.bus_comm.check_windows_position_req(pos_pass=WinPos.percent_20)
    #     # sleep(1)
    #     # self.bus_comm.set_windows_position(pos_pass=WinPos.percent_20)
    #     result = self.bus_comm.check_multiple_signals_thread_stop("CemBodyFr68")
    #     logger.info(f'获取到的原始数据为{result}')
    #     assert result


    @pytest.mark.full
    def test_caseid_1994579(self):
        """
        锁车自动关窗记忆-诊断复位后，锁车自动关窗
        """
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        sleep(30)
        self.bus_comm.check_multiple_signals_thread_start([("bodycan",'CemBodyFr68','WinOpenDrvrReq',1), ("bodycan",'CemBodyFr68','WinOpenPassReq',1), ("bodycan",'CemBodyFr68','WinOpenReLeReq',1), ("bodycan",'CemBodyFr68','WinOpenReRiReq',1)],timeout=15)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        result = self.bus_comm.check_multiple_signals_thread_stop("CemBodyFr68")
        logger.info(f'获取到的原始数据为{result}')
        assert result

    @pytest.mark.full
    def test_caseid_1994580(self):
        """
        锁车自动关窗记忆-断电上电后，锁车自动关窗
        """
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        sleep(15)
        self.bus_comm.check_multiple_signals_thread_start([("bodycan",'CemBodyFr68','WinOpenDrvrReq',1), ("bodycan",'CemBodyFr68','WinOpenPassReq',1), ("bodycan",'CemBodyFr68','WinOpenReLeReq',1), ("bodycan",'CemBodyFr68','WinOpenReRiReq',1)],timeout=15)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Lock)
        result = self.bus_comm.check_multiple_signals_thread_stop("CemBodyFr68")
        logger.info(f'获取到的原始数据为{result}')
        assert result


    @pytest.mark.full
    def test_caseid_1993185(self):
        """
        雨天关窗记忆，4个窗户全开，BGM复位后，检测到下雨，自动关窗
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.sd_tester.reset_bgm()
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_rain_detect_sts(True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)

    # @pytest.mark.full
    # def test_caseid_1993186(self):
    #     """
    #     雨天关窗记忆，4个窗户全开，BGM断电上电，检测到下雨，自动关窗
    #     """
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
    #     self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
    #     self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
    #     self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
    #     self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
    #     self.io.bgm_power_off()
    #     self.io.bgm_power_on()
    #     sleep(30)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
    #     self.bus_comm.check_multiple_signals_thread_start([("bodycan",'CemBodyFr68','WinOpenDrvrReq',1), ("bodycan",'CemBodyFr68','WinOpenPassReq',1), ("bodycan",'CemBodyFr68','WinOpenReLeReq',1), ("bodycan",'CemBodyFr68','WinOpenReRiReq',1)],timeout=15)
    #     self.bus_comm.set_vehspd_gear(vehspd=3.0)
    #     sleep(1.5)
    #     self.bus_comm.set_rain_detect_sts(True)
    #     self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
    #     result = self.bus_comm.check_multiple_signals_thread_stop("CemBodyFr68")
    #     logger.info(f'获取到的原始数据为{result}')
    #     assert result

    @pytest.mark.full
    def test_caseid_1993183(self):
        """
        雨天关窗记忆，4个窗户全开，休眠唤醒后,设置4个窗户为全关且UB位为0，检测到下雨，自动关窗
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.close,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.mix.network_sleep()
        self.wakeup()
        # sleep(30)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.set_windows_signal_ub_false(1,1,1,1)
        self.bus_comm.set_rain_detect_sts(True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)

    @pytest.mark.full
    def test_caseid_1993182(self):
        """
        雨天关窗记忆，副驾窗户为位置，左后窗户为关闭，其余窗户全开，休眠唤醒后，检测到下雨，自动关窗
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.close,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.mix.network_sleep()
        self.wakeup()
        # sleep(30)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_rain_detect_sts(True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)

    @pytest.mark.full
    def test_caseid_1993181(self):
        """
        雨天关窗记忆，左后和右后窗户关闭，其余窗户全开，休眠唤醒后，检测到下雨，自动关窗
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.mix.network_sleep()
        self.wakeup()
        # sleep(30)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_rain_detect_sts(True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)


    @pytest.mark.full
    def test_caseid_1988226(self):
        """
        雨天关窗记忆，设置4个窗户状态为未知，休眠唤醒后，检测到下雨，4个窗户状态为未知
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.mix.network_sleep()
        self.wakeup()
        # sleep(30)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_rain_detect_sts(True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)


    @pytest.mark.full
    def test_caseid_1988225(self):
        """
        雨天关窗记忆，设置4个窗户状态为全关，休眠唤醒后，设置四个窗户为全开，检测到下雨，自动关窗
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.mix.network_sleep()
        self.wakeup()
        # sleep(30)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
    
    @pytest.mark.full
    def test_caseid_1988224(self):
        """
        雨天关窗记忆，4个窗户全开，休眠唤醒后,设置4个窗户为未知且UB位为0，检测到下雨，自动关窗
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.mix.network_sleep()
        self.wakeup()
        # sleep(30)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.set_windows_signal_ub_false(0,0,0,0)
        self.bus_comm.set_rain_detect_sts(True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
    
    
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1988219(self):
        """
        雨天关窗记忆，4个窗户全开，休眠唤醒后，检测到下雨，自动关窗
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.mix.network_sleep()
        self.wakeup()
        # sleep(30)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_rain_detect_sts(True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)

    

    

   

    