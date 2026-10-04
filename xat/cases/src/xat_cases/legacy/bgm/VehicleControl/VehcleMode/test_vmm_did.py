#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_vmm_did.py
@Author      : heng.wang@jiduauto.com
@Time        : 2024/5/31 13:20
@Description: BGMvmmdid相关用例
"""

import os
import sys
import pytest
import allure
import random
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.constants.common import *


@allure.feature("车控车设")
@allure.story("整车模式/使用模式")
class TestUsageMode(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["VehicleModeService_client", "TailGateService_client", "VehicleSetStatusService_client"])
        time.sleep(5)

    def before_each_func(self, ecu):
        self.bus_comm.set_vehmtn()
        self.bus_comm.set_vehspd()
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr18", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        time.sleep(1)
        self.bus_comm.set_dtc_pre()
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        pass

    def after_each_func(self, ecu):
        self.soa.set_hv_off_sts(is_off=False)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.bus_comm.set_strt_msg_to_mod_mngt(StrtMsgToModMngt=StrtMsgToModMngt.NoInhb)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.trigger_gear_by_auto(gear_status=False)
        self.bus_comm.trigger_gear_by_manual(gear_status=False)
        self.bus_comm.trigger_gear_by_cdc(gear_status=False)
        self.bus_comm.set_brake_pedal_function_safe(sts=YesOrNo.No)
        self.io.set_five_door_sts(sts=Door.close)
        self.io.driver_seat_notpresent()
        self.bus_comm.set_secle_seat_notpresent()
        self.bus_comm.set_pass_seat_notpresent()
        self.io.hazard_light_close()
        self.io.bgm_diag_line_up()
        pass

    def after_class(self, ecu):
        self.mix.exit_crash()
        self.mix.set_and_check_exhibition_mode(status=False)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.soa.stop_soa()


    # ---------------------------->vmmdid<---------------------------------------------
    @allure.title("VMM_DID_Carmode_41F8_transport_driving")
    @pytest.mark.full
    def test_caseid_1987976(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x41f8, SESSION.EXTENDED, UnLock.L0, '06', '6e41f8', check_method=Check_Method.response, recover=False)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.TRANSPORT, car_mode_sub=0)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.NORMAL, car_mode_sub=3)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.wait_time_and_check_carmode(car_mode_main_new=CarMode.TRANSPORT,carmode_sub_new=0,car_mode_main_old=CarMode.NORMAL,carmode_sub_old=3)
        #恢复正常切换
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x41f8, SESSION.EXTENDED, UnLock.L0, '00', '6e41f8', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_Carmode_41F8_factory_driving")
    @pytest.mark.full
    def test_caseid_1987975(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x41f8, SESSION.EXTENDED, UnLock.L0, '06', '6e41f8', check_method=Check_Method.response, recover=False)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.FACTORY, car_mode_sub=0)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.NORMAL, car_mode_sub=2)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.wait_time_and_check_carmode(car_mode_main_new=CarMode.FACTORY,carmode_sub_new=0,car_mode_main_old=CarMode.NORMAL,carmode_sub_old=2)
        #恢复正常切换
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x41f8, SESSION.EXTENDED, UnLock.L0, '00', '6e41f8', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_Carmode_4231")
    @pytest.mark.full
    def test_caseid_1987974(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4231, SESSION.EXTENDED, UnLock.L0, '06', '6e4231', check_method=Check_Method.response, recover=False)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.FACTORY, car_mode_sub=0)
        self.io.hazard_light_open()
        time.sleep(0.1)
        self.io.hazard_light_close()
        time.sleep(0.1)
        self.io.hazard_light_open()
        time.sleep(0.1)
        self.io.hazard_light_close()
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.NORMAL, car_mode_sub=1)
        self.bus_comm.wait_time_and_check_carmode(car_mode_main_new=CarMode.FACTORY,carmode_sub_new=0,car_mode_main_old=CarMode.NORMAL,carmode_sub_old=1)
        #恢复正常切换
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x41f8, SESSION.EXTENDED, UnLock.L0, '00', '6e41f8', check_method=Check_Method.response, recover=False)
    
    @allure.title("	VMM_DID_Carmode_4232_Transport")
    @pytest.mark.full
    def test_caseid_1987973(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4232, SESSION.EXTENDED, UnLock.L3, '06', '6e4232', check_method=Check_Method.response, recover=False)
        self.sd_tester.send_request_and_recv_response([0x2F, 0xD1, 0X34, 0X3, 0X1],recv=True,do_assert=True)
        self.bus_comm.wait_time_and_check_carmode(car_mode_main_new=CarMode.TRANSPORT,carmode_sub_new=0,car_mode_main_old=CarMode.NORMAL,carmode_sub_old=0)
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4232, SESSION.EXTENDED, UnLock.L3, '00', '6e4232', check_method=Check_Method.response, recover=False)
        
        
    @allure.title("	VMM_DID_Carmode_4232_Factory")
    @pytest.mark.full
    def test_caseid_1987972(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4232, SESSION.EXTENDED, UnLock.L3, '06', '6e4232', check_method=Check_Method.response, recover=False)
        self.sd_tester.send_request_and_recv_response([0x2F, 0xD1, 0X34, 0X3, 0X2],recv=True,do_assert=True)
        self.bus_comm.wait_time_and_check_carmode(car_mode_main_new=CarMode.FACTORY,carmode_sub_new=0,car_mode_main_old=CarMode.NORMAL,carmode_sub_old=0)    
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4232, SESSION.EXTENDED, UnLock.L3, '00', '6e4232', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_Carmode_43C4_Normal")
    @pytest.mark.sanity
    def test_caseid_1987970(self):
        self.sd_tester.send_carmode_subtype_request_and_check_result_value(carmode_subtype=Carmode_subtype.Normal)
    
    @allure.title("VMM_DID_Carmode_43C4_Factory_Paused")
    @pytest.mark.full
    def test_caseid_1987969(self):
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.FACTORY, car_mode_sub=0)
        self.io.hazard_light_open()
        time.sleep(0.1)
        self.io.hazard_light_close()
        time.sleep(0.1)
        self.io.hazard_light_open()
        time.sleep(0.1)
        self.io.hazard_light_close()
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.NORMAL, car_mode_sub=1)
        self.sd_tester.send_carmode_subtype_request_and_check_result_value(carmode_subtype=Carmode_subtype.Factory_Paused)
    
    @allure.title("VMM_DID_Carmode_43C4_Factory_Driving")
    @pytest.mark.full
    def test_caseid_1987968(self):
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.FACTORY, car_mode_sub=0)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.NORMAL, car_mode_sub=2)
        self.sd_tester.send_carmode_subtype_request_and_check_result_value(carmode_subtype=Carmode_subtype.Factory_Driving)
    
    @allure.title("VMM_DID_Carmode_43C4_Transport_Driving")
    @pytest.mark.full
    def test_caseid_1987967(self):
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.TRANSPORT, car_mode_sub=0)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.NORMAL, car_mode_sub=3)
        self.sd_tester.send_carmode_subtype_request_and_check_result_value(carmode_subtype=Carmode_subtype.Transport_Driving)
    
    @allure.title("VMM_DID_Carmode_43C4_Transport")
    @pytest.mark.sanity
    def test_caseid_1987966(self):
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.TRANSPORT, car_mode_sub=0)
        self.sd_tester.send_carmode_subtype_request_and_check_result_value(carmode_subtype=Carmode_subtype.Transport)
    
    @allure.title("VMM_DID_Carmode_43C4_Factory")
    @pytest.mark.sanity
    def test_caseid_1987965(self):
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.FACTORY, car_mode_sub=0)
        self.sd_tester.send_carmode_subtype_request_and_check_result_value(carmode_subtype=Carmode_subtype.Factory)
    
    @allure.title("VMM_DID_Carmode_43C4_Crash")
    @pytest.mark.sanity
    def test_caseid_1987964(self):
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.Crash)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.CRASH, car_mode_sub=0)
        self.sd_tester.send_carmode_subtype_request_and_check_result_value(carmode_subtype=Carmode_subtype.Crash_1)
        self.mix.exit_crash()
    
    @allure.title("VMM_DID_Carmode_43C4_Dyno_2")
    @pytest.mark.sanity
    def test_caseid_1987963(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4313, SESSION.EXTENDED, UnLock.L0, '01', '6e4313', check_method=Check_Method.response, recover=False)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.DYNO, car_mode_sub=0)
        self.sd_tester.send_carmode_subtype_request_and_check_result_value(carmode_subtype=Carmode_subtype.Dyno_2)
    
    @allure.title("VMM_DID_Carmode_43C4_Dyno_4")
    @pytest.mark.full
    def test_caseid_1987962(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4313, SESSION.EXTENDED, UnLock.L0, '02', '6e4313', check_method=Check_Method.response, recover=False)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.DYNO, car_mode_sub=1)
        self.sd_tester.send_carmode_subtype_request_and_check_result_value(carmode_subtype=Carmode_subtype.Dyno_4)
        #以下是为了恢复成正常的dyno模式设置
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4313, SESSION.EXTENDED, UnLock.L0, '01', '6e4313', check_method=Check_Method.response, recover=False)
    
    #TPMS
    #TPMS_DID__4503
    @allure.title("TPMS_DID__4503")
    @pytest.mark.full
    def test_caseid_1987961(self):
        self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0x03],recv=True,do_assert=True)
    
    @allure.title("TPMS_DID_4504_1")
    @pytest.mark.full
    def test_caseid_1987960(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4504, SESSION.EXTENDED, UnLock.L5, '01', '6e4504', check_method=Check_Method.response, recover=False)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4504, SESSION.EXTENDED, '62450401')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4504, SESSION.EXTENDED, UnLock.L5, '00', '6e4504', check_method=Check_Method.response, recover=False)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4504, SESSION.EXTENDED, '62450400')
    
    @allure.title("TPMS_DID_4504_2")
    @pytest.mark.full
    def test_caseid_1987959(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4504, SESSION.EXTENDED, UnLock.L5, '02', '6e4504', check_method=Check_Method.response, recover=False)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4504, SESSION.EXTENDED, '62450402')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4504, SESSION.EXTENDED, UnLock.L5, '00', '6e4504', check_method=Check_Method.response, recover=False)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4504, SESSION.EXTENDED, '62450400')
    
    @allure.title("TPMS_DID_4504_3")
    @pytest.mark.full
    def test_caseid_1987958(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4504, SESSION.EXTENDED, UnLock.L5, '03', '6e4504', check_method=Check_Method.response, recover=False)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4504, SESSION.EXTENDED, '62450403')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4504, SESSION.EXTENDED, UnLock.L5, '00', '6e4504', check_method=Check_Method.response, recover=False)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4504, SESSION.EXTENDED, '62450400')
    
    @allure.title("TPMS_DID_4504_4")
    @pytest.mark.full
    def test_caseid_1987957(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4504, SESSION.EXTENDED, UnLock.L5, '04', '6e4504', check_method=Check_Method.response, recover=False)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4504, SESSION.EXTENDED, '62450404')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4504, SESSION.EXTENDED, UnLock.L5, '00', '6e4504', check_method=Check_Method.response, recover=False)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4504, SESSION.EXTENDED, '62450400')
    
    #vmm
    @allure.title("VMM_DID_展车模式_B300")
    @pytest.mark.full
    def test_caseid_1987956(self):
        self.bus_comm.set_epb_sts(sts=3)
        self.mix.set_and_check_exhibition_mode(status=True)
        time.sleep(0.3)
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xB300, SESSION.EXTENDED, '62b30011')
        self.mix.set_and_check_exhibition_mode(status=False)
        time.sleep(0.3)
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xB300, SESSION.EXTENDED, '62b30010')
    
    @allure.title("VMM_DID_洗车模式_B301")
    @pytest.mark.full
    def test_caseid_1987955(self):
        self.bus_comm.set_singal(bus="propulsioncan", msg="EcmPropComFr10", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.soa.hmi_set_wash_mode(sts=isOn.On, time_wait=1)
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xB301, SESSION.EXTENDED, '62b30101')
        self.soa.hmi_set_wash_mode(sts=isOn.Off, time_wait=1)
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xB301, SESSION.EXTENDED, '62b30100')
    
    @allure.title("VMM_DID_usagemode_2071")
    @pytest.mark.full
    def test_caseid_1987954(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0X2071, 0x01, SESSION.EXTENDED, UnLock.L0, 'ffffff', '7101207110')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x430E, SESSION.EXTENDED, '62430e000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
    
    @allure.title("VMM_DID_usagemode_2072")
    @pytest.mark.full
    def test_caseid_1987953(self):
        checklist = [0 for _ in range(27)]
        list_0 = [6, 7, 8, 12, 13, 14, 18, 19 ,20, 24, 25, 26]
        self.sd_tester.routine_ctrl_and_check(TA.BGM_MCU, 0X2072, 0x01, SESSION.EXTENDED, UnLock.L0, 'ffff', '7101207210')
        recvcode, list=self.sd_tester.send_request_and_recv_response([0x22, 0x43, 0x0F],recv=True,do_assert=True)
        read_list = list[3:]
        for i in range(len(read_list)):
            if i in list_0:
                read_list[i] = 0
        logging.info(f'sssss{read_list}')
        logging.info(f'wwwww{checklist}')
        self.sd_tester.compare_list(checklist, read_list)
    
    #enerrylevel
    @allure.title("VMM_DID_EnergryLevel_429D_00")
    @pytest.mark.full
    def test_caseid_1987952(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x03, SESSION.EXTENDED, UnLock.L0, '0000', '6f429d0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_egylvlelec(mai=0, subtype=0)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429D, SESSION.EXTENDED, '62429d00')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429d0000', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_EnergryLevel_429D_10")
    @pytest.mark.full
    def test_caseid_1987951(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x03, SESSION.EXTENDED, UnLock.L0, '1000', '6f429d0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_egylvlelec(mai=1, subtype=0)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429D, SESSION.EXTENDED, '62429d10')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429d0010', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_EnergryLevel_429D_11")
    @pytest.mark.full
    def test_caseid_1987950(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x03, SESSION.EXTENDED, UnLock.L0, '1100', '6f429d0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_egylvlelec(mai=1, subtype=1)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429D, SESSION.EXTENDED, '62429d11')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429d0011', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_EnergryLevel_429D_12")
    @pytest.mark.full
    def test_caseid_1987949(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x03, SESSION.EXTENDED, UnLock.L0, '1200', '6f429d0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_egylvlelec(mai=1, subtype=2)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429D, SESSION.EXTENDED, '62429d12')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429d0012', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_EnergryLevel_429D_20")
    @pytest.mark.full
    def test_caseid_1987948(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x03, SESSION.EXTENDED, UnLock.L0, '2000', '6f429d0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_egylvlelec(mai=2, subtype=0)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429D, SESSION.EXTENDED, '62429d20')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429d0020', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_EnergryLevel_429D_21")
    @pytest.mark.full
    def test_caseid_1987947(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x03, SESSION.EXTENDED, UnLock.L0, '2100', '6f429d0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_egylvlelec(mai=2, subtype=1)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429D, SESSION.EXTENDED, '62429d21')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429d0021', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_EnergryLevel_429D_30")
    @pytest.mark.full
    def test_caseid_1987946(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x03, SESSION.EXTENDED, UnLock.L0, '3000', '6f429d0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_egylvlelec(mai=3, subtype=0)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429D, SESSION.EXTENDED, '62429d30')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429d0030', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_EnergryLevel_429D_31")
    @pytest.mark.sanity
    def test_caseid_1987945(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x03, SESSION.EXTENDED, UnLock.L0, '3100', '6f429d0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_egylvlelec(mai=3, subtype=1)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429D, SESSION.EXTENDED, '62429d31')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429d0031', check_method=Check_Method.response, recover=False)

    @allure.title("VMM_DID_EnergryLevel_429D_2F归还")
    @pytest.mark.sanity
    def test_caseid_1987944(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429D, SESSION.EXTENDED, '62429d00')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x03, SESSION.EXTENDED, UnLock.L0, '3100', '6f429d0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_egylvlelec(mai=3, subtype=1)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429D, SESSION.EXTENDED, '62429d31')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429D, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429d0031', check_method=Check_Method.response, recover=False)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429D, SESSION.EXTENDED, '62429d00')
    
    @allure.title("VMM_DID_PowerLevel_429E_DD0C_00")
    @pytest.mark.full
    def test_caseid_1987943(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '0000', '6f429e0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429E, SESSION.EXTENDED, '62429e00')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xDD0C, SESSION.EXTENDED, '62dd0c0f')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e0000', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_PowerLevel_429E_DD0C_0F")
    @pytest.mark.full
    def test_caseid_1987942(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '0f00', '6f429e0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=15)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429E, SESSION.EXTENDED, '62429e0f')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xDD0C, SESSION.EXTENDED, '62dd0c0f')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e000f', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_PowerLevel_429E_DD0C_10")
    @pytest.mark.full
    def test_caseid_1987941(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '1000', '6f429e0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=1, subtype=0)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429E, SESSION.EXTENDED, '62429e10')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xDD0C, SESSION.EXTENDED, '62dd0c10')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e0010', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_PowerLevel_429E_DD0C_11")
    @pytest.mark.full
    def test_caseid_1987940(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '1100', '6f429e0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=1, subtype=1)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429E, SESSION.EXTENDED, '62429e11')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xDD0C, SESSION.EXTENDED, '62dd0c11')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e0011', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_PowerLevel_429E_DD0C_12")
    @pytest.mark.full
    def test_caseid_1987939(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '1200', '6f429e0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=1, subtype=2)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429E, SESSION.EXTENDED, '62429e12')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xDD0C, SESSION.EXTENDED, '62dd0c12')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e0012', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_PowerLevel_429E_DD0C_20")
    @pytest.mark.full
    def test_caseid_1987938(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '2000', '6f429e0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=2, subtype=0)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429E, SESSION.EXTENDED, '62429e20')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xDD0C, SESSION.EXTENDED, '62dd0c20')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e0020', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_PowerLevel_429E_DD0C_21")
    @pytest.mark.full
    def test_caseid_1987937(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '2100', '6f429e0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=2, subtype=1)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429E, SESSION.EXTENDED, '62429e21')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xDD0C, SESSION.EXTENDED, '62dd0c21')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e0021', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_PowerLevel_429E_DD0C_22")
    @pytest.mark.full
    def test_caseid_1987936(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '2200', '6f429e0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=2, subtype=2)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429E, SESSION.EXTENDED, '62429e22')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xDD0C, SESSION.EXTENDED, '62dd0c22')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e0022', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_PowerLevel_429E_DD0C_23")
    @pytest.mark.full
    def test_caseid_1987935(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '2300', '6f429e0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=2, subtype=3)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429E, SESSION.EXTENDED, '62429e23')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xDD0C, SESSION.EXTENDED, '62dd0c23')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e0023', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_PowerLevel_429E_DD0C_24")
    @pytest.mark.full
    def test_caseid_1987934(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '2400', '6f429e0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=2, subtype=4)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429E, SESSION.EXTENDED, '62429e24')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xDD0C, SESSION.EXTENDED, '62dd0c24')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e0024', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_PowerLevel_429E_DD0C_30")
    @pytest.mark.full
    def test_caseid_1987933(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '3000', '6f429e0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=3, subtype=0)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429E, SESSION.EXTENDED, '62429e30')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xDD0C, SESSION.EXTENDED, '62dd0c30')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e0030', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_PowerLevel_429E_DD0C_31")
    @pytest.mark.full
    def test_caseid_1987932(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '3100', '6f429e0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=3, subtype=1)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429E, SESSION.EXTENDED, '62429e31')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xDD0C, SESSION.EXTENDED, '62dd0c31')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e0031', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_PowerLevel_429E_DD0C_40")
    @pytest.mark.full
    def test_caseid_1987931(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '4000', '6f429e0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=4, subtype=0)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429E, SESSION.EXTENDED, '62429e40')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xDD0C, SESSION.EXTENDED, '62dd0c40')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e0040', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_PowerLevel_429E_DD0C_41")
    @pytest.mark.full
    def test_caseid_1987930(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '4100', '6f429e0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=4, subtype=1)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429E, SESSION.EXTENDED, '62429e41')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xDD0C, SESSION.EXTENDED, '62dd0c41')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e0041', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_PowerLevel_429E_DD0C_42")
    @pytest.mark.full
    def test_caseid_1987929(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '4200', '6f429e0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=4, subtype=2)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429E, SESSION.EXTENDED, '62429e42')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xDD0C, SESSION.EXTENDED, '62dd0c42')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e0042', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_PowerLevel_429E_DD0C_43")
    @pytest.mark.full
    def test_caseid_1987928(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '4300', '6f429e0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=4, subtype=3)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429E, SESSION.EXTENDED, '62429e43')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xDD0C, SESSION.EXTENDED, '62dd0c43')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e0043', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_PowerLevel_429E_DD0C_50")
    @pytest.mark.full
    def test_caseid_1987927(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '5000', '6f429e0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=5, subtype=0)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429E, SESSION.EXTENDED, '62429e50')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xDD0C, SESSION.EXTENDED, '62dd0c50')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e0050', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_PowerLevel_429E_DD0C_51")
    @pytest.mark.sanity
    def test_caseid_1987926(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '5100', '6f429e0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=5, subtype=1)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429E, SESSION.EXTENDED, '62429e51')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xDD0C, SESSION.EXTENDED, '62dd0c51')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e0051', check_method=Check_Method.response, recover=False)
    
    @allure.title("VMM_DID_PowerLevel_429E_2F归还")
    @pytest.mark.sanity
    def test_caseid_1987925(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429E, SESSION.EXTENDED, '62429e00')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '5100', '6f429e0300', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=5, subtype=1)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429E, SESSION.EXTENDED, '62429e51')
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e0051', check_method=Check_Method.response, recover=False)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429E, SESSION.EXTENDED, '62429e00')
    
    ##immo
    @pytest.mark.sanity
    def test_caseid_1987924(self):
        '''IMMO_DID_40DE'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        # 生成随机认证密钥
        write_immokey_list = [random.randint(0, 255) for _ in range(32)]
        logger.info("写入认证密钥")
        self.sd_tester.send_request_and_recv_response([0x2E, 0x40, 0xDE], write_immokey_list, do_assert=True)
        sleep(1)
        self.sd_tester.send_request_and_recv_response([0x22, 0x40, 0xDE],recv=[0x62, 0x40, 0xDE] + write_immokey_list,do_assert=True,)
        logger.info("重启bgm")
        self.sd_tester.update_serverdoipid(0x1FFF)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        logger.info("写入随机密钥后，读取认证密钥")
        self.sd_tester.send_request_and_recv_response([0x22, 0x40, 0xDE],recv=[0x62, 0x40, 0xDE] + write_immokey_list,do_assert=True,)
        sleep(.1)
        logger.info("恢复认证密钥")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        self.sd_tester.send_request_and_recv_response([0x2E, 0x40, 0xDE,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55] )
        
    @pytest.mark.sanity
    def test_caseid_1987923(self):
        '''IMMO_DID_40DF'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        # 生成随机认证密钥
        write_immokey_list = [random.randint(0, 255) for _ in range(32)]
        logger.info("写入认证密钥")
        self.sd_tester.send_request_and_recv_response([0x2E, 0x40, 0xDF], write_immokey_list, do_assert=True)
        sleep(1)
        self.sd_tester.send_request_and_recv_response([0x22, 0x40, 0xDF],recv=[0x62, 0x40, 0xDF] + write_immokey_list,do_assert=True,)
        logger.info("重启bgm")
        self.sd_tester.update_serverdoipid(0x1FFF)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        logger.info("写入随机密钥后，读取认证密钥")
        self.sd_tester.send_request_and_recv_response([0x22, 0x40, 0xDF],recv=[0x62, 0x40, 0xDF] + write_immokey_list,do_assert=True,)
        sleep(.1)
        logger.info("恢复认证密钥")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        self.sd_tester.send_request_and_recv_response([0x2E, 0x40, 0xDF,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55] )
    
    @pytest.mark.sanity
    def test_caseid_1987922(self):
        '''IMMO_DID_40E0'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        # 生成随机认证密钥
        write_immokey_list = [random.randint(0, 255) for _ in range(32)]
        logger.info("写入认证密钥")
        self.sd_tester.send_request_and_recv_response([0x2E, 0x40, 0xE0], write_immokey_list, do_assert=True)
        sleep(1)
        self.sd_tester.send_request_and_recv_response([0x22, 0x40, 0xE0],recv=[0x62, 0x40, 0xE0] + write_immokey_list,do_assert=True,)
        logger.info("重启bgm")
        self.sd_tester.update_serverdoipid(0x1FFF)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        logger.info("写入随机密钥后，读取认证密钥")
        self.sd_tester.send_request_and_recv_response([0x22, 0x40, 0xE0],recv=[0x62, 0x40, 0xE0] + write_immokey_list,do_assert=True,)
        sleep(.1)
        logger.info("恢复认证密钥")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        self.sd_tester.send_request_and_recv_response([0x2E, 0x40, 0xE0,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55] )
    
    @pytest.mark.sanity
    def test_caseid_1987921(self):
        '''IMMO_DID_41DE'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        # 生成随机认证密钥
        write_immokey_list = [random.randint(0, 255) for _ in range(16)]
        logger.info("写入认证密钥")
        self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0xDE], write_immokey_list, do_assert=True)
        sleep(1)
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0xDE],recv=[0x62, 0x41, 0xDE] + write_immokey_list,do_assert=True,)
        logger.info("重启bgm")
        self.sd_tester.update_serverdoipid(0x1FFF)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        logger.info("写入随机密钥后，读取认证密钥")
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0xDE],recv=[0x62, 0x41, 0xDE] + write_immokey_list,do_assert=True,)
        sleep(.1)
        logger.info("恢复认证密钥")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0xDE,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55] )
        
    @pytest.mark.sanity
    def test_caseid_1987920(self):
        '''IMMO_DID_41DF'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        # 生成随机认证密钥
        write_immokey_list = [random.randint(0, 255) for _ in range(16)]
        logger.info("写入认证密钥")
        self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0xDF], write_immokey_list, do_assert=True)
        sleep(1)
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0xDF],recv=[0x62, 0x41, 0xDF] + write_immokey_list,do_assert=True,)
        logger.info("重启bgm")
        self.sd_tester.update_serverdoipid(0x1FFF)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        logger.info("写入随机密钥后，读取认证密钥")
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0xDF],recv=[0x62, 0x41, 0xDF] + write_immokey_list,do_assert=True,)
        sleep(.1)
        logger.info("恢复认证密钥")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0xDF,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55] )
    
    @pytest.mark.sanity
    def test_caseid_1987919(self):
        '''IMMO_DID_41E0'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        # 生成随机认证密钥
        write_immokey_list = [random.randint(0, 255) for _ in range(16)]
        logger.info("写入认证密钥")
        self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0xE0], write_immokey_list, do_assert=True)
        sleep(1)
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0xE0],recv=[0x62, 0x41, 0xE0] + write_immokey_list,do_assert=True,)
        logger.info("重启bgm")
        self.sd_tester.update_serverdoipid(0x1FFF)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        logger.info("写入随机密钥后，读取认证密钥")
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0xE0],recv=[0x62, 0x41, 0xE0] + write_immokey_list,do_assert=True,)
        sleep(.1)
        logger.info("恢复认证密钥")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0xE0,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55] )
    
    @pytest.mark.sanity
    def test_caseid_1987918(self):
        '''IMMO_DID_41E1'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        # 生成随机认证密钥
        write_immokey_list = [random.randint(0, 255) for _ in range(16)]
        logger.info("写入认证密钥")
        self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0xE1], write_immokey_list, do_assert=True)
        sleep(1)
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0xE1],recv=[0x62, 0x41, 0xE1] + write_immokey_list,do_assert=True,)
        logger.info("重启bgm")
        self.sd_tester.update_serverdoipid(0x1FFF)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        logger.info("写入随机密钥后，读取认证密钥")
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0xE1],recv=[0x62, 0x41, 0xE1] + write_immokey_list,do_assert=True,)
        sleep(.1)
        logger.info("恢复认证密钥")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0xE1,0x69,0x6D,0x6D,0x6F,0x6B,0x65,0x79,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30] )
    
    @allure.title("IMMO_DID_45A1_01")
    @pytest.mark.full
    def test_caseid_1987917(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x45A1, SESSION.EXTENDED, '6245a101')
    
    @allure.title("IMMO_DID_45A1_02")
    @pytest.mark.full
    def test_caseid_1987916(self):
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeUp',{"mode": 13})
        time.sleep(0.3)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x45A1, SESSION.EXTENDED, '6245a102')
    
    @pytest.mark.full
    def test_caseid_1987915(self):
        '''IMMO_DID_40EE_存储eeprom'''
        yq_list = [0x2, 0x10, 0x0, 0x1, 0x2, 0x2, 0x2]
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.bus_comm.set_driving_preconditions()
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeUp',{"mode": 13})
        time.sleep(3)
        recvcode, read_list=self.sd_tester.send_request_and_recv_response([0x22, 0x40, 0xEE],recv=True,do_assert=True)
        self.sd_tester.compare_list(yq_list, read_list[3:10])
        logger.info("重启bgm")
        self.sd_tester.update_serverdoipid(0x1FFF)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)
        logger.info("重启后再次读取")
        recvcode, read_list1=self.sd_tester.send_request_and_recv_response([0x22, 0x40, 0xEE],recv=True,do_assert=True)
        sleep(.1)
        logger.info("再次比较")
        self.sd_tester.compare_list(yq_list, read_list1[3:10])
    
    @pytest.mark.full
    def test_caseid_1987914(self):
        '''IMMO_DID_40EE_存储ram'''
        yq_list = [0x2, 0x10, 0x0, 0x1, 0x2, 0x1, 0x1]
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.bus_comm.set_driving_preconditions(imobengsts2=ImobSts.ImobImobn, imobengsts3=ImobSts.ImobImobn)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeUp',{"mode": 13})
        time.sleep(1)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(3)
        recvcode, read_list=self.sd_tester.send_request_and_recv_response([0x22, 0x40, 0xEE],recv=True,do_assert=True)
        self.sd_tester.compare_list(yq_list, read_list[3:10])
        logger.info("重启bgm")
        self.sd_tester.update_serverdoipid(0x1FFF)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)
        logger.info("重启后再次读取")
        recvcode, read_list1=self.sd_tester.send_request_and_recv_response([0x22, 0x40, 0xEE],recv=True,do_assert=True)
        sleep(.1)
        logger.info("再次比较")
        self.sd_tester.compare_list(yq_list, read_list1[3:10], is_equal=False)
    
    @pytest.mark.sanity
    def test_caseid_1987913(self):
        '''总里程_DID_DD01'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        recv_code, read_list=self.sd_tester.send_request_and_recv_response([0x22, 0xDD, 0x01],recv=True,do_assert=True)
        write_list, check_list=self.sd_tester.generate_dd01_list(read_list=read_list) 
        logger.info("写入认证密钥")
        self.sd_tester.send_request_and_recv_response([0x2E, 0xDD, 0x01], write_list, do_assert=True)
        sleep(1)
        self.sd_tester.send_request_and_recv_response([0x22, 0xDD, 0x01],recv=[0x62, 0xDD, 0x01] + check_list,do_assert=True,)
        logger.info("重启bgm")
        self.sd_tester.update_serverdoipid(0x1FFF)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)
        logger.info("写入随机密钥后，读取认证密钥")
        self.sd_tester.send_request_and_recv_response([0x22, 0xDD, 0x01],recv=[0x62, 0xDD, 0x01] + check_list,do_assert=True,)
        sleep(.1)
        logger.info("恢复认证密钥")
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x2E, 0xDD, 0x01,0x00,0X00,0X00] )

    