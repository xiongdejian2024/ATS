# -*- coding: utf-8 -*-
"""
@File        : test_horn_ctrl_abc.py
@Author      : xiangyue.li@jiduauto.com
@Time        : 2023/05/10 15:00 PM
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
from xat_ecu.legacy.soa_partner.src.partner_const import *


@allure.feature("车控车设")
@allure.story("喇叭")
class TestHornCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["HornService_client", "CentralLockService_client","KeyService_client","DoorService_client","EntryService_client"])
        sleep(2)

    def before_each_func(self, ecu):
        self.mix.set_common_precontion()
        self.io.set_five_door_sts(Door.close)
        self.io.set_horn_switch_sts(isOn.On)  # 关闭喇叭

    def after_each_func(self, ecu):
        self.mix.set_common_precontion()
        sleep(2)

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    def check_horn_sts_and_req(self, sts: HornStatus, req: isOn):
        self.bus_comm.check_horn_active_req(req=req)
        self.soa.event_check_horn_sts(sts=sts)
        self.soa.get_horn_active_sts(sts=sts)

    @allure.title("470798 v10 远程寻车")
    @pytest.mark.smoke
    def test_caseid_118705(self):
        self.soa.send_method_request('KeyService_client','SetCarLocalTraceRequest',{"carLoctrReq": 1})
        self.bus_comm.check_singal("connectivitycanfd","VgmConnFr05","CarLoctrActvnSts",1)
        for i in range(3):
            self.bus_comm.check_horn_active_req(isOn.On)
            sleep(0.4)
            self.bus_comm.check_horn_active_req(isOn.Off)

    @allure.title("470793 v8 Normal喇叭打开后关闭")
    @pytest.mark.smoke
    def test_caseid_1980865(self):
        self.io.set_horn_switch_sts(isOn.Off)   
        self.check_horn_sts_and_req(sts=HornStatus.On, req=isOn.On)
        sleep(0.2)
        self.io.set_horn_switch_sts(isOn.On)
        self.soa.get_horn_active_sts(HornStatus.Off)
        self.bus_comm.check_horn_active_req(isOn.Off)

    @allure.title("470793 v8 喇叭开关基本功能")
    @pytest.mark.smoke
    def test_caseid_118701(self):
        self.io.set_horn_switch_sts(isOn.Off)   
        self.check_horn_sts_and_req(sts=HornStatus.On, req=isOn.On)
        sleep(0.2)
        self.io.set_horn_switch_sts(isOn.On)
        self.soa.get_horn_active_sts(HornStatus.Off)
        self.bus_comm.check_horn_active_req(isOn.Off)

    @allure.title("喇叭基本功能_abandoned")
    @pytest.mark.full
    def test_caseid_1989265(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.io.set_horn_switch_sts(isOn.Off)   
        self.check_horn_sts_and_req(sts=HornStatus.On, req=isOn.On)
        sleep(0.2)
        self.io.set_horn_switch_sts(isOn.On)
        self.soa.get_horn_active_sts(HornStatus.Off)
        self.bus_comm.check_horn_active_req(isOn.Off)
        
    @allure.title("喇叭基本功能_inactive")
    @pytest.mark.full
    def test_caseid_1989266(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.io.set_horn_switch_sts(isOn.Off)   
        self.check_horn_sts_and_req(sts=HornStatus.On, req=isOn.On)
        sleep(0.2)
        self.io.set_horn_switch_sts(isOn.On)
        self.soa.get_horn_active_sts(HornStatus.Off)
        self.bus_comm.check_horn_active_req(isOn.Off)
        
    @allure.title("喇叭基本功能_convenience")
    @pytest.mark.full
    def test_caseid_1989267(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.io.set_horn_switch_sts(isOn.Off)   
        self.check_horn_sts_and_req(sts=HornStatus.On, req=isOn.On)
        sleep(0.2)
        self.io.set_horn_switch_sts(isOn.On)
        self.soa.get_horn_active_sts(HornStatus.Off)
        self.bus_comm.check_horn_active_req(isOn.Off)

    @allure.title("喇叭基本功能_active")
    @pytest.mark.full
    def test_caseid_1989268(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.io.set_horn_switch_sts(isOn.Off)   
        self.check_horn_sts_and_req(sts=HornStatus.On, req=isOn.On)
        sleep(0.2)
        self.io.set_horn_switch_sts(isOn.On)
        self.soa.get_horn_active_sts(HornStatus.Off)
        self.bus_comm.check_horn_active_req(isOn.Off)
        
    @allure.title("喇叭基本功能_driving")
    @pytest.mark.full
    def test_caseid_1989269(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.io.set_horn_switch_sts(isOn.Off)   
        self.check_horn_sts_and_req(sts=HornStatus.On, req=isOn.On)
        sleep(0.2)
        self.io.set_horn_switch_sts(isOn.On)
        self.soa.get_horn_active_sts(HornStatus.Off)
        self.bus_comm.check_horn_active_req(isOn.Off)
                
    @allure.title("470793 v8 喇叭基本功能_喇叭激活计时器最长30s")
    @pytest.mark.full
    def test_caseid_118702(self):
        self.io.set_horn_switch_sts(isOn.Off)   
        self.check_horn_sts_and_req(sts=HornStatus.On, req=isOn.On)
        sleep(30)
        self.bus_comm.check_horn_active_req(isOn.Off)

    @allure.title("470798 v10 Alarm触发鸣笛")
    @pytest.mark.full
    def test_caseid_118704(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(
            exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem
        )
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        sleep(0.2)  # 声光不同步
        self.soa.get_horn_active_sts(HornStatus.On)
        self.bus_comm.check_horn_active_req(isOn.On)
        sleep(0.4)
        self.bus_comm.check_horn_active_req(isOn.Off)

    @allure.title("470793 v8 喇叭基本功能_normal")
    @pytest.mark.sanity
    def test_caseid_1913518(self):
        self.mix.set_common_precontion()
        self.io.set_horn_switch_sts(isOn.On)
        self.io.set_horn_switch_sts(isOn.Off)   
        self.check_horn_sts_and_req(sts=HornStatus.On, req=isOn.On)
        sleep(0.2)
        self.io.set_horn_switch_sts(isOn.On)
        self.soa.get_horn_active_sts(HornStatus.Off)
        self.bus_comm.check_horn_active_req(isOn.Off)

    @allure.title("470793 v8 喇叭基本功能_crash")
    @pytest.mark.sanity
    def test_caseid_1983526(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)
        self.io.set_horn_switch_sts(isOn.On)
        self.io.set_horn_switch_sts(isOn.Off)   
        self.check_horn_sts_and_req(sts=HornStatus.On, req=isOn.On)
        sleep(0.2)
        self.io.set_horn_switch_sts(isOn.On)
        self.soa.get_horn_active_sts(HornStatus.Off)
        self.bus_comm.check_horn_active_req(isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)

    @allure.title("470793 v8 喇叭基本功能_dyno")
    @pytest.mark.sanity
    def test_caseid_1983527(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO)
        self.io.set_horn_switch_sts(isOn.On)
        self.io.set_horn_switch_sts(isOn.Off)   
        self.check_horn_sts_and_req(sts=HornStatus.On, req=isOn.On)
        sleep(0.2)
        self.io.set_horn_switch_sts(isOn.On)
        self.soa.get_horn_active_sts(HornStatus.Off)
        self.bus_comm.check_horn_active_req(isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)

    @allure.title("470793 v8 喇叭基本功能_transport")
    @pytest.mark.sanity
    def test_caseid_1983528(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_central_lock_event_sts(
            evn_update_sts=True, evn_trigsrc=LockTrigerSource.NFC
        )
        self.bus_comm.check_central_lock_sts(
            exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.NFC
        )
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT)
        self.io.set_horn_switch_sts(isOn.On)
        self.io.set_horn_switch_sts(isOn.Off)   
        self.check_horn_sts_and_req(sts=HornStatus.On, req=isOn.On)
        sleep(0.2)
        self.io.set_horn_switch_sts(isOn.On)
        self.soa.get_horn_active_sts(HornStatus.Off)
        self.bus_comm.check_horn_active_req(isOn.Off)
            

    @allure.title("470793 v8 喇叭基本功能_factory")
    @pytest.mark.sanity
    def test_caseid_1983529(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_central_lock_event_sts(
            evn_update_sts=True, evn_trigsrc=LockTrigerSource.NFC
        )
        self.bus_comm.check_central_lock_sts(
            exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.NFC
        )
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY)
        self.io.set_horn_switch_sts(isOn.On)
        self.io.set_horn_switch_sts(isOn.Off)   
        self.check_horn_sts_and_req(sts=HornStatus.On, req=isOn.On)
        sleep(0.2)
        self.io.set_horn_switch_sts(isOn.On)
        self.soa.get_horn_active_sts(HornStatus.Off)
        self.bus_comm.check_horn_active_req(isOn.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        
    @allure.title("io重启_喇叭打开")
    @pytest.mark.sanity
    @pytest.mark.nvm
    def test_caseid_1985113(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.io.set_horn_switch_sts(isOn.Off)   
        self.check_horn_sts_and_req(sts=HornStatus.On, req=isOn.On)
        sleep(0.2)
        self.io.io_reset_bgm()
        sleep(15)
        self.check_horn_sts_and_req(sts=HornStatus.On, req=isOn.On)
        
    @allure.title("io重启_喇叭关闭")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1985114(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.io.set_horn_switch_sts(isOn.On)   
        self.check_horn_sts_and_req(sts=HornStatus.Off, req=isOn.Off)
        sleep(0.2)
        self.io.io_reset_bgm()
        sleep(15)
        self.check_horn_sts_and_req(sts=HornStatus.Off, req=isOn.Off)
    
    @allure.title("休眠唤醒_喇叭打开")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1985115(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.io.set_horn_switch_sts(isOn.Off)   
        self.check_horn_sts_and_req(sts=HornStatus.On, req=isOn.On)
        sleep(5)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        sleep(5)
        self.io.set_horn_switch_sts(isOn.On)
        self.io.set_horn_switch_sts(isOn.Off)
        self.check_horn_sts_and_req(sts=HornStatus.On, req=isOn.On)
        
    @allure.title("诊断重启_喇叭打开")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994567(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.io.set_horn_switch_sts(isOn.Off)   
        self.check_horn_sts_and_req(sts=HornStatus.On, req=isOn.On)
        sleep(0.2)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        sleep(10)
        self.check_horn_sts_and_req(sts=HornStatus.On, req=isOn.On)
        
    @allure.title("470797 v8 喇叭信号功能优先级_寻车鸣笛过程中触发防盗")
    @pytest.mark.full
    def test_caseid_118703(self):
        self.io.set_horn_switch_sts(isOn.On)
        self.soa.get_horn_active_sts(HornStatus.Off)
        self.bus_comm.check_horn_active_req(isOn.Off)
        self.mix.set_common_precontion()
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        sleep(30)
        self.soa.send_method_request('KeyService_client','SetCarLocalTraceRequest',{"carLoctrReq": 1})
        self.bus_comm.check_singal("connectivitycanfd","VgmConnFr05","CarLoctrActvnSts",1)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.bus_comm.check_horn_active_req(isOn.On)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC) #恢复
        
    @allure.title("470797喇叭信号功能优先级_远程寻车按压喇叭开关信号检测")
    @pytest.mark.full
    def test_caseid_118708(self):
        self.soa.send_method_request('KeyService_client','SetCarLocalTraceRequest',{"carLoctrReq": 1})
        self.bus_comm.check_singal("connectivitycanfd","VgmConnFr05","CarLoctrActvnSts",1)
        for i in range(3):
            self.bus_comm.check_horn_active_req(isOn.On)
            sleep(0.4)
            self.bus_comm.check_horn_active_req(isOn.Off)
        self.io.set_horn_switch_sts(isOn.Off)
        self.soa.get_horn_active_sts(HornStatus.On)
        self.bus_comm.check_horn_active_req(isOn.On)
        
    @allure.title("470797 v8 喇叭信号功能优先级_锁车异常按压喇叭")
    @pytest.mark.full
    def test_caseid_118707(self):
        self.io.set_five_door_sts(Door.close)
        self.mix.set_common_precontion()
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.io.set_door(Drvr=Door.open)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.NFC)
        sleep(1)
        self.bus_comm.set_singal("connectivitycanfd", "NfcrConnFr02", "NFCStatus", 1)
        self.bus_comm.set_singal("connectivitycanfd", "NfcrConnFr02", "NFCStatus", 0)
        sleep(7)
        self.bus_comm.set_door_anti_pnch_sts(Drvr=True)
        self.io.set_horn_switch_sts(isOn.Off)
        self.soa.get_horn_active_sts(HornStatus.On)
        self.bus_comm.check_horn_active_req(isOn.On)
        
    @allure.title("441402 寻车异常未触发鸣笛")
    @pytest.mark.full
    def test_caseid_118706(self):
        self.io.set_horn_switch_sts(isOn.On)
        self.soa.get_horn_active_sts(HornStatus.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.soa.send_method_request('KeyService_client','SetCarLocalTraceRequest',{"carLoctrReq": 3})
        self.bus_comm.check_singal("connectivitycanfd","VgmConnFr05","CarLoctrActvnSts",0)
        self.bus_comm.check_horn_active_req(isOn.Off)