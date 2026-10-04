# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_goosenecklamp_abc.py
@Time         :9/2/24 6:25 PM
@Author       :yucheng.zhu@jiduauto.com 
@Description  :
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


@allure.feature("车控车设")
@allure.story("内灯功能")
class TestIntrlightCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(
            [
                "LightService_client",
                "CentralLockService_client",
                "DoorService_client",
                "TailGateService_client",
                "WiperService_client",
                "SeatService_client",
                "KeyService_client",
            ]
        )

    def before_each_func(self, ecu):
        try:
            self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        except:
            self.mix.ctrl_lock(LockCmd.UnLock, LockSource.NFC)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL,
            vehmtnst=VehMtnSts.StandStillVal3,ccp={183: 0x84, 950: 0x02}
        )
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_all_seats_present_sts(SeatPresSts.NoPres)
        sleep(.5)

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    @allure.title("座椅鹅颈灯常亮_driving")
    @pytest.mark.sanity
    def test_goosenecklamp_caseid_1900116(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)

    @allure.title("座椅鹅颈灯常亮_active")
    @pytest.mark.sanity
    def test_goosenecklamp_caseid_1992539(self):
        self.mix.set_usage_mode(UsageMode.ACTIVE)
        sleep(1)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)

    @allure.title("座椅鹅颈灯On_inactive_开主驾门")
    @pytest.mark.sanity
    def test_goosenecklamp_caseid_118914(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)

    @allure.title("座椅鹅颈灯On_inactive_开副驾门")
    @pytest.mark.sanity
    def test_goosenecklamp_caseid_1992541(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)

    @allure.title("座椅鹅颈灯On_inactive_开左后门")
    @pytest.mark.sanity
    def test_goosenecklamp_caseid_1992542(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)

    @allure.title("座椅鹅颈灯On_inactive_开右后门")
    @pytest.mark.sanity
    def test_goosenecklamp_caseid_1991452(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)

    @allure.title("座椅鹅颈灯Off_NFC闭锁")
    @pytest.mark.sanity
    def test_goosenecklamp_caseid_118919(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.NFC)
        self.bus_comm.check_goosenecklamp(sts=OnOff.Off)

    @allure.title("座椅鹅颈灯Off_TmrAut闭锁")
    @pytest.mark.full
    @pytest.mark.man
    def test_goosenecklamp_caseid_1992450(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(0.5)
        self.io.set_hood_sts(HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem, timeout=3)
        sleep(30)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)
        self.bus_comm.check_goosenecklamp(sts=OnOff.Off)

    @allure.title("座椅鹅颈灯Off_KeyRem闭锁")
    @pytest.mark.full
    def test_goosenecklamp_caseid_1992451(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_goosenecklamp(sts=OnOff.Off)

    @allure.title("座椅鹅颈灯Off_Keyls闭锁")
    @pytest.mark.full
    @pytest.mark.man
    def test_goosenecklamp_caseid_1992441(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.io.hazard_light_close()
        self.mix.set_lock_unlock_visible_feedback_precondition(LockState.Lock)
        # self.bus_comm.check_turn_indicate_lamp_req(IndcrSts.Off)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=2.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        self.bus_comm.check_goosenecklamp(sts=OnOff.Off)

    @allure.title("座椅鹅颈灯Off_Telm闭锁")
    @pytest.mark.full
    def test_goosenecklamp_caseid_1991994(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.io.set_hood_sts(HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.check_goosenecklamp(sts=OnOff.Off)

    @allure.title("座椅鹅颈灯Off_Apprch闭锁")
    @pytest.mark.full
    def test_goosenecklamp_caseid_1992052(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 1)
        self.soa.hmi_event_check_tailgate_movests(MoveSts.Closed)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.HMI)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)
        sleep(3)  # 等待前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_goosenecklamp(sts=OnOff.Off)

    @allure.title("座椅鹅颈灯Off_OutsOth闭锁")
    @pytest.mark.full
    @pytest.mark.man
    def test_goosenecklamp_caseid_1992049(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.io.hazard_light_close()
        self.mix.set_lock_unlock_visible_feedback_precondition(LockState.Lock)
        # self.bus_comm.check_turn_indicate_lamp_req(IndcrSts.Off)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        self.bus_comm.check_goosenecklamp(sts=OnOff.Off)

    @allure.title("座椅鹅颈灯On_IntrSwt闭锁")
    @pytest.mark.full
    def test_goosenecklamp_caseid_1991443(self):
        self.io.set_door(Drvr=Door.open)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)

    @allure.title("座椅鹅颈灯Off_任意座椅未占用_关闭主驾门")
    @pytest.mark.full
    def test_goosenecklamp_caseid_118915(self):
        self.io.set_door(Drvr=Door.open)
        sleep(0.1)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_goosenecklamp(sts=OnOff.Off)

    @allure.title("座椅鹅颈灯Off_任意座椅未占用_关闭副驾门")
    @pytest.mark.full
    def test_goosenecklamp_caseid_1992540(self):
        self.io.set_door(Pass=Door.open)
        sleep(0.1)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)
        self.io.set_door(Pass=Door.close)
        self.bus_comm.check_goosenecklamp(sts=OnOff.Off)

    @allure.title("座椅鹅颈灯Off_任意座椅未占用_关闭左后门")
    @pytest.mark.full
    def test_goosenecklamp_caseid_1992543(self):
        self.io.set_door(LeRe=Door.open)
        sleep(0.1)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)
        self.io.set_door(LeRe=Door.close)
        self.bus_comm.check_goosenecklamp(sts=OnOff.Off)

    @allure.title("座椅鹅颈灯Off_任意座椅未占用_关闭右后门")
    @pytest.mark.full
    def test_goosenecklamp_caseid_1992544(self):
        self.io.set_door(RiRe=Door.open)
        sleep(0.1)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)
        self.io.set_door(RiRe=Door.close)
        self.bus_comm.check_goosenecklamp(sts=OnOff.Off)

    @allure.title("座椅鹅颈灯Off_主驾占用_关闭主驾门")
    @pytest.mark.full
    def test_goosenecklamp_caseid_1992536(self):
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.io.set_door(Drvr=Door.open)
        sleep(0.1)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)

    @allure.title("座椅鹅颈灯Off_副驾占用_关闭副驾门")
    @pytest.mark.full
    def test_goosenecklamp_caseid_1991379(self):
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        self.io.set_door(Pass=Door.open)
        sleep(0.1)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)
        self.io.set_door(Pass=Door.close)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)

    @allure.title("座椅鹅颈灯Off_左后座位占座_关闭左后门")
    @pytest.mark.full
    def test_goosenecklamp_caseid_1991380(self):
        self.mix.set_seats_present_sts(sec_left=SeatPresSts.Pres)
        self.io.set_door(LeRe=Door.open)
        sleep(0.1)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)
        self.io.set_door(LeRe=Door.close)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)

    @allure.title("座椅鹅颈灯Off_右后座位占座_关闭右后门")
    @pytest.mark.full
    def test_goosenecklamp_caseid_1991384(self):
        self.mix.set_seats_present_sts(sec_right=SeatPresSts.Pres)
        self.io.set_door(RiRe=Door.open)
        sleep(0.1)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)
        self.io.set_door(RiRe=Door.close)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)

    @allure.title("座椅鹅颈灯Off_CarMode = Factory")
    @pytest.mark.full
    def test_goosenecklamp_caseid_118918(self):
        self.mix.set_car_mode(CarMode.FACTORY)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_goosenecklamp(sts=OnOff.Off)

    @allure.title("座椅鹅颈灯Off_CarMode = Transport")
    @pytest.mark.full
    def test_goosenecklamp_caseid_1991941(self):
        self.mix.set_car_mode(CarMode.TRANSPORT)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_goosenecklamp(sts=OnOff.Off)

    @allure.title("座椅鹅颈灯On_开主驾门_掉电重启")
    @pytest.mark.full
    @pytest.mark.man
    def test_goosenecklamp_caseid_1992002(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)
        self.io.io_reset_bgm(times=5)
        sleep(20)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)

    @allure.title("座椅鹅颈灯On_开主驾门_abandon切inactive")
    @pytest.mark.full
    def test_goosenecklamp_caseid_1991939(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.io.set_door(Drvr=Door.open)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.check_goosenecklamp(sts=OnOff.Off)

    @allure.title("CCP不满足_座椅鹅颈灯Off_开副驾门")
    @pytest.mark.full
    def test_goosenecklamp_caseid_1991996(self):
        self.sd_tester.write_ccp(ccp={183: 0x80, 950: 0x02})
        sleep(1)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_goosenecklamp(sts=OnOff.Off)
        self.io.set_door(Pass=Door.close)
        self.sd_tester.write_ccp(ccp={183: 0x84, 950: 0x02})
        sleep(1)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)

    @allure.title("座椅鹅颈灯On_conv_开主驾门切inactive")
    @pytest.mark.full
    def test_goosenecklamp_caseid_1992003(self):
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.check_goosenecklamp(sts=OnOff.On)

    @allure.title("座椅鹅颈灯On_active切inactive")
    @pytest.mark.full
    def test_goosenecklamp_caseid_1992011(self):
        self.mix.set_usage_mode(UsageMode.ACTIVE)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.check_goosenecklamp(sts=OnOff.Off)

