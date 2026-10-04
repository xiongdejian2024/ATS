#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_alrm_ctrl_abc.py
@Author      : xiangyue.li@jiduauto.com
@Time        : 2023/11/9 11:30
@Description: BGM车控车设车辆防盗功能
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
from xat_ecu.legacy.common.data_handle import *


@allure.feature("车控车设")
@allure.story("车辆防盗")
class TestAlrmCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(
            ["CentralLockService_client", "CTDService_client", "TailGateService_client"]
        )
        sleep(2)
        self.sd_tester.write_ccp(
            ccp={
                94: 0x80,
                98: 0x2,
                97: 0x2,
                10: 0x2,
                481: 0x4,
                578: 0x4,
                142: 0x83,  # 解闭锁相关
                64: 3,  # With Alarm Using Vehicle Horn 即siren，警报器
                543: 1,  # Without Battery Backed-Up Sounder 即BBS
                66: 1,  # Without inclination sensor 即IS倾斜传感器
                65: 1,  # Without Interior Motion Sensor 即内部运动传感器
                1: 0xA3,  # 适用配置了舒适泊车模式的车型，对应设防准备时间 30s
                69: 1,  # Re-trig次数，一个报警周期30s鸣笛停止10s
                70: 1,  # 无被动设防
                13: 4,  # 动力类型Battery electric vehicle，上切Active或Driving可解防
            }
        )

    def before_each_func(self, ecu):
        pass

    def after_each_func(self, ecu):
        self.io.set_hood_sts(HoodSts.Close)
        self.io.set_five_door_sts(Door.close)
        pass

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    def set_centrllock_to_lock(self):
        self.mix.set_all_seats_present_sts(seat_pres_sts=SeatPresSts.NoPres)
        self.io.set_five_door_sts(Door.close)
        # 设置bodycan上五个电动门均关闭
        self.bus_comm.set_door_opener_sts(DoorOpenerSts.FullClsd)
        self.io.trigger_all_doors_outswitch(OutSwitchPressSts.NoPress)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        sleep(1)
        cen_lock_sts = self.bus_comm.get_central_lock_sts()
        if cen_lock_sts == 1:
            logger.info(f"当前的中控锁状态为UnLock,需要先落锁再执行后续操作")
            self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
            sleep(1)
            cen_lock_sts = self.bus_comm.get_central_lock_sts()
            if cen_lock_sts == 3:
                logger.info(f"当前的中控锁状态是否为Lock,闭锁成功")
            else:
                logger.info(f"当前的中控锁状态仍为UnLock,RKE闭锁失败")
        else:
            logger.info(f"当前的中控锁状态为Lock,不需要先落锁,可以直接执行后续操作")

    def check_indicator_lamp_flash(self, indcr_sts: IndcrSts, timeout=10):
        result_ori = self.bus_comm.get_active_indicator_lamp_req_data(timeout)
        logger.info("result_original {}".format(result_ori))
        result_1 = get_signal_times_interval(result_ori, indcr_sts.value)
        logger.info("result_1(信号值为3):{}".format(result_1))
        if result_1[0] > 17 and result_1[0] < 23:
            assert True
        else:
            assert False

        result_2 = get_signal_times_interval(result_ori, 0)
        logger.info("result_2(信号值为0):{}".format(result_2))
        if result_2[0] > 17 and result_2[0] < 23:
            assert True
        else:
            assert False

    def alrm_notactive(self):
        try:
            self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        except:
            self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)

    def Armd(self):
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        
    def Actv(self):
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        
    def Disarmd(self):
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
                              
    @allure.title("激活防盗后解锁进入Disarm")
    @pytest.mark.sanity
    def test_caseid_1979846(self):
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        sleep(30)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr, sys_sts=SysDefenSts.Actv, alm_src=AlmSrc.DriDoor
        )
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)

    @allure.title("防盗激活后_诊断切写_Active")
    @pytest.mark.sanity
    def test_caseid_1979834(self):
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        sleep(30)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr, sys_sts=SysDefenSts.Actv, alm_src=AlmSrc.DriDoor
        )
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        
    @allure.title("Normal_Inactive_主驾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979881(self):
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr, sys_sts=SysDefenSts.Actv, alm_src=AlmSrc.DriDoor
        )

    @allure.title("Normal_Inactive_副驾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979875(self):
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.PassDoor,
        )

    @allure.title("Normal_Inactive_左后门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979869(self):
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReleDoor,
        )

    @allure.title("Normal_Inactive_右后门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979863(self):
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReriDoor,
        )

    @allure.title("Normal_Inactive_尾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1983728(self):
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Tailgate,
        )
        
    @allure.title("Normal_Abandoned_主驾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979883(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr, sys_sts=SysDefenSts.Actv, alm_src=AlmSrc.DriDoor
        )
        
    @allure.title("Normal_Abandoned_副驾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979877(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.PassDoor,
        )
        
    @allure.title("Normal_Abandoned_右后门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979865(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReriDoor,
        )

    @allure.title("Normal_Abandoned_左后门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979871(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReleDoor,
        )
        
    @allure.title("Normal_Abandoned_尾门触发防盗")        
    @pytest.mark.smoke
    def test_caseid_1979853(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Tailgate
        )
        
    @allure.title("Normal_Abandoned_前舱盖触发防盗")        
    @pytest.mark.full
    def test_caseid_1979859(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_hood_sts(HoodSts.Open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Hood
        )
        
    @allure.title("Dyno_Inactive_主驾门触发防盗")
    @pytest.mark.full
    def test_caseid_1979880(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.INACTIVE)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr, sys_sts=SysDefenSts.Actv, alm_src=AlmSrc.DriDoor
        )

    @allure.title("Dyno_Inactive_副驾门触发防盗")
    @pytest.mark.full
    def test_caseid_1979874(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.INACTIVE)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.PassDoor,
        )

    @allure.title("Dyno_Inactive_左后门触发防盗")
    @pytest.mark.full
    def test_caseid_1979868(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.INACTIVE)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReleDoor,
        )

    @allure.title("Dyno_Inactive_右后门触发防盗")
    @pytest.mark.full
    def test_caseid_1979862(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.INACTIVE)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReriDoor,
        )

    @allure.title("Dyno_Inactive_尾门触发防盗")
    @pytest.mark.full
    def test_caseid_1979850(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.INACTIVE)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Tailgate,
        )

    @allure.title("Dyno_Inactive_前舱盖触发防盗")        
    @pytest.mark.full
    def test_caseid_1979856(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.INACTIVE)
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_hood_sts(HoodSts.Open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Hood
        )
        
    @allure.title("Dyno_Abandoned_主驾门触发防盗")
    @pytest.mark.full
    def test_caseid_1979884(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.ABANDONED)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr, sys_sts=SysDefenSts.Actv, alm_src=AlmSrc.DriDoor
        )
        
    @allure.title("Dyno_Abandoned_副驾门触发防盗")
    @pytest.mark.full
    def test_caseid_1979878(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.ABANDONED)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.PassDoor,
        )

    @allure.title("Dyno_Abandoned_左后门触发防盗")
    @pytest.mark.full
    def test_caseid_1979872(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.ABANDONED)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReleDoor,
        )

    @allure.title("Dyno_Abandoned_右后门触发防盗")
    @pytest.mark.full
    def test_caseid_1979866(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.ABANDONED)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReriDoor,
        )
              
    @allure.title("Dyno_Abandoned_尾门触发防盗")        
    @pytest.mark.full
    def test_caseid_1979854(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.ABANDONED)
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Tailgate
        )

    @allure.title("Dyno_Abandoned_前舱盖触发防盗")        
    @pytest.mark.full
    def test_caseid_1979860(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.ABANDONED)
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_hood_sts(HoodSts.Open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Hood
        )
        
    @allure.title("Crash_Inactive_副驾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979876(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.INACTIVE)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.PassDoor,
        )
        
    @allure.title("Crash_Inactive_左后门触发防盗")
    @pytest.mark.full
    def test_caseid_1979870(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.INACTIVE)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReleDoor,
        )

    @allure.title("Crash_Inactive_右后门触发防盗")
    @pytest.mark.full
    def test_caseid_1979864(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.INACTIVE)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReriDoor,
        )

    @allure.title("Crash_Inactive_主驾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979882(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.INACTIVE)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr, sys_sts=SysDefenSts.Actv, alm_src=AlmSrc.DriDoor
        )
                
    @allure.title("Crash_Inactive_尾门触发防盗")        
    @pytest.mark.full
    def test_caseid_1979852(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.INACTIVE)
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Tailgate
        )


    @allure.title("诊断切写Normal change to Factory")        
    @pytest.mark.sanity
    def test_caseid_1979840(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.set_centrllock_to_lock()
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        self.sd_tester.send_data_and_check(0x1002,"2ed13402",'7f2e31')
#7f是否定响应  2e:写DID服务  22:条件不满足

    @allure.title("诊断切写Crash change to Dyno")        
    @pytest.mark.full
    def test_caseid_1979829(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.INACTIVE)
        self.set_centrllock_to_lock()
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)

    @allure.title("诊断切写Crash change to Normal")        
    @pytest.mark.sanity
    def test_caseid_1979832(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.INACTIVE)
        self.set_centrllock_to_lock()
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL,usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)

    @allure.title("Crash_Abandoned_主驾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979885(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.ABANDONED)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr, sys_sts=SysDefenSts.Actv, alm_src=AlmSrc.DriDoor
        )

    @allure.title("Crash_Abandoned_副驾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979879(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.ABANDONED)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.PassDoor,
        )
                
    @allure.title("Crash_Abandoned_左后门触发防盗")
    @pytest.mark.full
    def test_caseid_1979873(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.ABANDONED)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReleDoor,
        )

    @allure.title("Crash_Abandoned_右后门触发防盗")
    @pytest.mark.full
    def test_caseid_1979867(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.ABANDONED)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReriDoor,
        )

    @allure.title("Crash_Abandoned_尾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979855(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.ABANDONED)
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Tailgate,
        )
                        
    @allure.title("Active结束后进入Arm")
    @pytest.mark.smoke
    def test_caseid_1979845(self):
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()

        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)

    @allure.title("Arm解锁进入Disarm")
    @pytest.mark.smoke
    def test_caseid_1979847(self):
        self.mix.set_common_precontion()
        self.set_centrllock_to_lock()
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)

    @allure.title("Disarm闭锁进入Arm")
    @pytest.mark.smoke
    def test_caseid_1979848(self):
        self.mix.set_common_precontion()
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
     
    @allure.title("Re_Trig_车辆防盗Normal_Abandoned_主驾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979826(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.DriDoor
        )
        self.io.set_door(Drvr=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.DriDoor
        )

    @allure.title("Re_Trig_车辆防盗Normal_Abandoned_副驾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979820(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.PassDoor
        )
        self.io.set_door(Pass=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.PassDoor
        )

        
    @allure.title("Re_Trig_车辆防盗Normal_Abandoned_前舱盖触发防盗")
    @pytest.mark.full
    def test_caseid_1979802(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_hood_sts(HoodSts.Open)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "HoodSts", 1)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Hood
        )
        self.io.set_hood_sts(HoodSts.Close)
        self.io.set_hood_sts(HoodSts.Open)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "HoodSts", 1)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Hood
        )
        
    @allure.title("Re_Trig_车辆防盗Normal_Abandoned_尾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979796(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Tailgate
        )
        self.io.set_door(Trunk=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Tailgate
        )

        
    @allure.title("Re_Trig_车辆防盗Normal_Abandoned_左后门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979814(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReleDoor
        )
        self.io.set_door(LeRe=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReleDoor
        )
               
    @allure.title("Re_Trig_车辆防盗Normal_Abandoned_右后门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979808(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReriDoor
        )
        self.io.set_door(RiRe=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReriDoor
        )

    @allure.title("Re_Trig_车辆防盗Normal_Inactive_主驾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979824(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.DriDoor
        )
        self.io.set_door(Drvr=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.DriDoor
        )
                      
    @allure.title("Re_Trig_车辆防盗Normal_Inactive_副驾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979818(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.PassDoor
        )
        self.io.set_door(Pass=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.PassDoor
        )

    @allure.title("Re_Trig_车辆防盗Normal_Inactive_前舱盖触发防盗")
    @pytest.mark.full
    def test_caseid_1979800(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_hood_sts(HoodSts.Open)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "HoodSts", 1)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Hood
        )
        self.io.set_hood_sts(HoodSts.Close)
        self.io.set_hood_sts(HoodSts.Open)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "HoodSts", 1)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Hood
        )

    @allure.title("Re_Trig_车辆防盗Normal_Inactive_左后门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979812(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReleDoor
        )
        self.io.set_door(LeRe=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReleDoor
        )

                
    @allure.title("Re_Trig_车辆防盗Normal_Inactive_右后门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979806(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReriDoor
        )
        self.io.set_door(RiRe=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReriDoor
        )

                
    @allure.title("Re_Trig_车辆防盗Normal_Inactive_尾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979794(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Tailgate
        )
        self.io.set_door(Trunk=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Tailgate
        )
        
    @allure.title("Re_Trig_车辆防盗Dyno_Inactive_主驾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979823(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.INACTIVE,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.DriDoor
        )
        self.io.set_door(Drvr=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.DriDoor
        )
                      
    @allure.title("Re_Trig_车辆防盗Dyno_Inactive_副驾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979817(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.INACTIVE,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.PassDoor
        )
        self.io.set_door(Pass=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.PassDoor
        )

    @allure.title("Re_Trig_车辆防盗Dyno_Inactive_前舱盖触发防盗")
    @pytest.mark.full
    def test_caseid_1979799(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.INACTIVE,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_hood_sts(HoodSts.Open)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "HoodSts", 1)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Hood
        )
        self.io.set_hood_sts(HoodSts.Close)
        self.io.set_hood_sts(HoodSts.Open)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "HoodSts", 1)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Hood
        )

    @allure.title("Re_Trig_车辆防盗Dyno_Inactive_左后门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979811(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.INACTIVE,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReleDoor
        )
        self.io.set_door(LeRe=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReleDoor
        )
                
    @allure.title("Re_Trig_车辆防盗Dyno_Inactive_右后门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979805(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.INACTIVE,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReriDoor
        )
        self.io.set_door(RiRe=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReriDoor
        )
        
    @allure.title("Re_Trig_车辆防盗Dyno_Inactive_尾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979793(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.INACTIVE,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Tailgate
        )
        self.io.set_door(Trunk=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Tailgate
        )
        
    @allure.title("Re_Trig_车辆防盗Dyno_Abandoned_主驾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979827(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.ABANDONED,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.DriDoor
        )
        self.io.set_door(Drvr=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.DriDoor
        )

    @allure.title("Re_Trig_车辆防盗Dyno_Abandoned_副驾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979821(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.ABANDONED,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.PassDoor
        )
        self.io.set_door(Pass=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.PassDoor
        )
        
    @allure.title("Re_Trig_车辆防盗Dyno_Abandoned_前舱盖触发防盗")
    @pytest.mark.full
    def test_caseid_1979803(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.ABANDONED,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_hood_sts(HoodSts.Open)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "HoodSts", 1)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Hood
        )
        self.io.set_hood_sts(HoodSts.Close)
        self.io.set_hood_sts(HoodSts.Open)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "HoodSts", 1)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Hood
        )
        
    @allure.title("Re_Trig_车辆防盗Dyno_Abandoned_尾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979797(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.ABANDONED,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Tailgate
        )
        self.io.set_door(Trunk=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Tailgate
        )

    @allure.title("Re_Trig_车辆防盗Dyno_Abandoned_左后门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979815(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.ABANDONED,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReleDoor
        )
        self.io.set_door(LeRe=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReleDoor
        )
               
    @allure.title("Re_Trig_车辆防盗Dyno_Abandoned_右后门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979809(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.ABANDONED,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReriDoor
        )
        self.io.set_door(RiRe=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReriDoor
        )
        
    @allure.title("Re_Trig_车辆防盗Crash_Abandoned_主驾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979828(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.ABANDONED,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.DriDoor
        )
        self.io.set_door(Drvr=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.DriDoor
        )

    @allure.title("Re_Trig_车辆防盗Crash_Abandoned_副驾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979822(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.ABANDONED,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.PassDoor
        )
        self.io.set_door(Pass=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.PassDoor
        )
        
    @allure.title("Re_Trig_车辆防盗Crash_Abandoned_前舱盖触发防盗")
    @pytest.mark.full
    def test_caseid_1979804(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.ABANDONED,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_hood_sts(HoodSts.Open)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "HoodSts", 1)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Hood
        )
        self.io.set_hood_sts(HoodSts.Close)
        self.io.set_hood_sts(HoodSts.Open)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "HoodSts", 1)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Hood
        )
        
    @allure.title("Re_Trig_车辆防盗Crash_Abandoned_尾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979798(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.ABANDONED,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Tailgate
        )
        self.io.set_door(Trunk=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Tailgate
        )

    @allure.title("Re_Trig_车辆防盗Crash_Abandoned_左后门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979816(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.ABANDONED,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReleDoor
        )
        self.io.set_door(LeRe=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReleDoor
        )
               
    @allure.title("Re_Trig_车辆防盗Crash_Abandoned_右后门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979810(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.ABANDONED,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReriDoor
        )
        self.io.set_door(RiRe=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReriDoor
        )

    @allure.title("Re_Trig_车辆防盗Crash_Inactive_主驾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979825(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.INACTIVE,ccp={69:0x02})
        self.set_centrllock_to_lock()
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        sleep(30)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.DriDoor
        )
        self.io.set_door(Drvr=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.DriDoor
        )

                      
    @allure.title("Re_Trig_车辆防盗Crash_Inactive_副驾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979819(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.INACTIVE,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.PassDoor
        )
        self.io.set_door(Pass=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.PassDoor
        )

    @allure.title("Re_Trig_车辆防盗Crash_Inactive_前舱盖触发防盗")
    @pytest.mark.full
    def test_caseid_1979801(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.INACTIVE,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_hood_sts(HoodSts.Open)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "HoodSts", 1)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Hood
        )
        self.io.set_hood_sts(HoodSts.Close)
        self.io.set_hood_sts(HoodSts.Open)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "HoodSts", 1)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Hood
        )

    @allure.title("Re_Trig_车辆防盗Crash_Inactive_左后门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979813(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.INACTIVE,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReleDoor
        )
        self.io.set_door(LeRe=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReleDoor
        )
                
    @allure.title("Re_Trig_车辆防盗Crash_Inactive_右后门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979807(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.INACTIVE,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReriDoor
        )
        self.io.set_door(RiRe=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.ReriDoor
        )
        
    @allure.title("Re_Trig_车辆防盗Crash_Inactive_尾门触发防盗")
    @pytest.mark.smoke
    def test_caseid_1979795(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.INACTIVE,ccp={69:0x02})
        self.set_centrllock_to_lock()
        sleep(30)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Tailgate
        )
        self.io.set_door(Trunk=Door.open)
        sleep(10)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.check_indicator_lamp_flash(IndcrSts.LeAndRiOn)
        self.soa.get_alrm_info(
            sys_fault=SysFault.NoFailr,
            sys_sts=SysDefenSts.Actv,
            alm_src=AlmSrc.Tailgate
        )

    @allure.title("自动泊车请求外部锁车和完全防护请求")        
    @pytest.mark.full
    def test_caseid_1982701(self):
        self.mix.set_common_precontion(ccp={142 : 0x83})
        self.io.set_five_door_sts(Door.close)
        self.soa.hmi_set_door_close_lock(LockCmd.LockCompleteArm, LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        
    @allure.title("自动泊车无锁车请求_防盗状态保持不变")        
    @pytest.mark.full
    def test_caseid_1982697(self):
        self.Armd()
        self.sd_tester.write_ccp({142 : 0x83})
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        self.Actv()
        self.sd_tester.write_ccp({142 : 0x83})
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        self.Disarmd()
        self.sd_tester.write_ccp({142 : 0x83})

    @allure.title("休眠唤醒_防盗状态")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1989369(self):
        self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal3,ccp={75:0x02})
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        
    @allure.title("io重启_防盗状态")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994498(self):
        self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal3,ccp={75:0x02})
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        self.io.io_reset_bgm()
        sleep(15)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        
    @allure.title("诊断重启_防盗状态")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994499(self):
        self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal3,ccp={75:0x02})
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)

    @allure.title("防盗状态存储")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1989094(self):
        self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal3,ccp={75:0x02})
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        sleep(15)
        self.io.io_reset_bgm()
        sleep(15)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        sleep(15)
        self.io.io_reset_bgm()
        sleep(15)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        sleep(15)
        self.io.io_reset_bgm()
        sleep(15)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        
    @allure.title("电动门Ajar状态延时0.2s防止误报警")
    @pytest.mark.smoke
    def test_caseid_1989472(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        
    @allure.title("416B_主驾门触发源")
    @pytest.mark.smoke
    def test_caseid_1987629(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        sleep(3)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        sleep(3)
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X6B],recv=[0x62, 0x41, 0X6B,0x06])
        self.io.set_door(Drvr=Door.close)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)#恢复
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        
    @allure.title("416B_副驾门触发源")
    @pytest.mark.full
    def test_caseid_1982019(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        sleep(3)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        sleep(30)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        sleep(3)
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X6B],recv=[0x62, 0x41, 0X6B,0x07])
        self.io.set_door(Pass=Door.close)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)#恢复
        self.bus_comm.check_alrm_sts_req(AlrmSts.Disarmd)
        
    @allure.title("416B_左后门触发源")
    @pytest.mark.full
    def test_caseid_1989095(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        sleep(3)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        sleep(30)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        sleep(3)
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X6B],recv=[0x62, 0x41, 0X6B,0x08])
        self.io.set_door(LeRe=Door.close)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)#恢复
        
    @allure.title("416B_右后门触发源")
    @pytest.mark.full
    def test_caseid_1989290(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        sleep(3)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        sleep(30)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        sleep(3)
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X6B],recv=[0x62, 0x41, 0X6B,0x09])
        self.io.set_door(RiRe=Door.close)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)#恢复
        
    @allure.title("416B_尾门触发源")
    @pytest.mark.smoke
    def test_caseid_1989471(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        sleep(3)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        sleep(30)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Actv)
        sleep(3)
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X6B],recv=[0x62, 0x41, 0X6B,0x05])
        self.io.set_door(RiRe=Door.close)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)#恢复