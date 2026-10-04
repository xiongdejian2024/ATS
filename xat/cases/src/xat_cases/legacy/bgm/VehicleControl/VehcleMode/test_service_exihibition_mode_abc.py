#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_service_exhibiton_mode_abc.py
@Author      : heng.wang@jiduauto.com
@Time        : 2024/1/29 13:20
@Description: BGM展车模式服务相关抽象接口用例
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
@allure.story("整车模式/展车模式")
class TestUsageMode(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["VehicleModeService_client"])
        time.sleep(5)

    def before_each_func(self, ecu):
        self.bus_comm.set_vehmtn()
        self.bus_comm.set_vehspd()
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr18", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        self.bus_comm.set_epb_sts(sts=3)
        time.sleep(1)
        self.mix.set_and_check_exhibition_mode(status=False)
        self.bus_comm.set_dtc_pre()
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        
        pass

    def after_each_func(self, ecu):
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.io.set_five_door_sts(sts=Door.close)
        self.io.driver_seat_notpresent()
        self.bus_comm.set_secle_seat_notpresent()
        self.bus_comm.set_pass_seat_notpresent()
        self.io.hazard_light_close()
        self.io.bgm_diag_line_up()
        self.io.tcam_kl15_up()
        pass

    def after_class(self, ecu):
        self.mix.set_and_check_exhibition_mode(status=False)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)


    # ---------------------------->展车模式<---------------------------------------------
    @pytest.mark.smoke
    @pytest.mark.mcu_test
    def test_service_exhibition_mode_caseid_113335(self):
        "服务切换 展车模式"
        self.mix.set_and_check_exhibition_mode(status=True)
    
    @pytest.mark.smoke
    @pytest.mark.mcu_test
    def test_service_exhibition_mode_caseid_113332(self):
        "服务切换 非展车模式"
        self.mix.set_and_check_exhibition_mode(status=True)
        self.mix.set_and_check_exhibition_mode(status=False)
    
    @pytest.mark.sanity
    @pytest.mark.single_bgm
    @pytest.mark.nvm
    def test_service_exhibition_mode_caseid_113302(self):
        "bgm休眠唤醒保持展车模式"
        self.mix.set_and_check_exhibition_mode(status=True)
        self.mix.network_sleep()
        self.io.bgm_diag_line_up()
        self.bus_comm.resume_all_bus_send()
        time.sleep(20)
        self.mix.check_exhibition_mode(status=True)
    
    @pytest.mark.sanity
    @pytest.mark.nvm
    def test_service_exhibition_mode_caseid_113300(self):
        "bgm上下电保持展车模式"
        self.mix.set_and_check_exhibition_mode(status=True)
        time.sleep(1)
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(20)
        self.mix.check_exhibition_mode(status=True)
    
    @pytest.mark.full
    def test_service_exhibition_mode_caseid_113311(self):
        "EPB状态非AllAppld下无法进入展车模式_服务进入"
        self.bus_comm.set_epb_sts(sts=0)
        time.sleep(1)
        self.soa.set_exhibition_mode(is_open=True)
        self.mix.check_exhibition_mode(status=False)
    
    @pytest.mark.full
    def test_service_exhibition_mode_caseid_113320(self):
        "driving下无法进入展车模式_服务进入"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.soa.set_exhibition_mode(is_open=True)
        self.mix.check_exhibition_mode(status=False)
    
    @pytest.mark.full
    def test_service_exhibition_mode_caseid_113240(self):
        "驾驶请求中可切展车模式"
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.mix.set_PtActvnReq(up_type=UpType.SetUsageModeUp)
        self.mix.set_and_check_exhibition_mode(status=True)
    
    @pytest.mark.full
    @pytest.mark.longtime
    def test_service_exhibition_mode_caseid_113248(self):
        "展车模式存储_上下电压测1000次"
        self.mix.set_and_check_exhibition_mode(status=True)
        count = 0 
        while count <1000:
            self.io.bgm_power_off()
            time.sleep(10)
            self.io.bgm_power_on()
            time.sleep(20)
            count +=1
        time.sleep(20)
        self.mix.check_exhibition_mode(status=True)
    
    @pytest.mark.full
    @pytest.mark.longtime
    def test_service_exhibition_mode_caseid_113257(self):
        "展车模式功能_动力禁止_动力请求无效"
        self.mix.set_and_check_exhibition_mode(status=True)
        self.bus_comm.check_singal(bus="infocanfd", msg="BgmInfoCanFdDevFr02", signal="StartInhibitSts", value=1)
        self.mix.set_and_check_exhibition_mode(status=False)
        self.bus_comm.check_singal(bus="infocanfd", msg="BgmInfoCanFdDevFr02", signal="StartInhibitSts", value=0)
    
    @pytest.mark.full
    def test_service_exhibition_mode_caseid_113256(self):
        "输出展车模式状态报文E2E校验"
        self.mix.set_and_check_exhibition_mode(status=True)
        captured_msgdata = self.bus_comm.recv_pdu('infocanfd','BgmInfoCanFdFr22',timeout=5)
        logger.info(f'---------------->接收方收到的数据是{captured_msgdata}')
        self.bus_comm.check_crc_from_pdu('infocanfd', 'BgmInfoCanFdFr22', 'ExhibitionModeStsExhibitionModeSts',captured_msgdata[-1])
        captured_msgdata_1 = self.bus_comm.recv_pdu('propulsioncan','BgmPropulsionFr01',timeout=5)
        logger.info(f'---------------->接收方收到的数据是{captured_msgdata_1}')
        self.bus_comm.check_crc_from_pdu('propulsioncan', 'BgmPropulsionFr01', 'ExhibitionModeStsExhibitionModeSts',captured_msgdata_1[-1])
        self.mix.set_and_check_exhibition_mode(status=False)
        captured_msgdata_2 = self.bus_comm.recv_pdu('infocanfd','BgmInfoCanFdFr22',timeout=5)
        logger.info(f'---------------->接收方收到的数据是{captured_msgdata_2}')
        self.bus_comm.check_crc_from_pdu('infocanfd', 'BgmInfoCanFdFr22', 'ExhibitionModeStsExhibitionModeSts',captured_msgdata_2[-1])
        captured_msgdata_3 = self.bus_comm.recv_pdu('propulsioncan','BgmPropulsionFr01',timeout=5)
        logger.info(f'---------------->接收方收到的数据是{captured_msgdata_3}')
        self.bus_comm.check_crc_from_pdu('propulsioncan', 'BgmPropulsionFr01', 'ExhibitionModeStsExhibitionModeSts',captured_msgdata_3[-1])
    
    @pytest.mark.full
    @pytest.mark.nvm
    def test_service_exhibition_mode_caseid_1994577(self):
        "展车模式存储_诊断重启"
        self.mix.set_and_check_exhibition_mode(status=True)
        time.sleep(1)
        self.sd_tester.reset_bgm()
        self.mix.check_exhibition_mode(status=True)
    
    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993212(self):
        '''禁止启动时_服务不触发PtActvnReq1WdPtActvnReq置位'''
        self.bus_comm.set_driving_preconditions(engSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake, imobengsts1=ImobSts.ImobMtn)
        self.mix.set_and_check_exhibition_mode(status=True)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.bus_comm.trigger_gear_by_auto()
        self.bus_comm.check_DrvrStrtReq(StrtReq=StrtReq.Reqd)
        self.bus_comm.check_PtActvnReq(PtActvnReq=PtActvnReq1.NoPtActvnReq)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993211(self):
        '''	禁止启动时_远程泊车不触发PtActvnReq1WdPtActvnReq置位'''
        self.bus_comm.set_driving_preconditions(engSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake, imobengsts1=ImobSts.ImobMtn)
        self.mix.set_and_check_exhibition_mode(status=True)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.soa.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",{"mode": 2})
        self.bus_comm.check_RemPrkgSts(RemPrkgSts=RemPrkgSts.PrkgAssiSysRemPrkgSts_Remoteparkactive)
        self.bus_comm.check_PtActvnReq(PtActvnReq=PtActvnReq1.NoPtActvnReq)

    
    
    


   


    