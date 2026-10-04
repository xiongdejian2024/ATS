#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_npc_vfc.py
@Author      : shulin.zheng@jiduauto.com
@Time        : 2023/11/9 11:30
@Description : BGM车控车设VFC
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
@allure.story("VFC")
class TestHVAlarmCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["HighVoltageService_client","CentralLockService_client","SteerWheelService_client",
                         "LightService_client",'ClimateControlService_client',"VehicleModeService_client",
                         "WiperService_client","ChargeLidService_client","TailWingService_client",
                         "KeyService_client","WindowAppService_client","GloveBoxService_client",
                         "OuterRearViewService_client","DoorService_client"])
        sleep(2)

    def before_each_func(self, ecu):
        pass

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
    
    @allure.title("车控车设_VFCPNC16_VMM车辆模式触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_vfc_caseid_1985811(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.mix.set_car_mode(CarMode.DYNO)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 15.0, 3.0)
        self.mix.set_car_mode(CarMode.NORMAL)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 15.0, 3.0)

    @allure.title("车控车设_VFCPNC16_VMM车辆模式触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_vfc_caseid_1989808(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.mix.set_car_mode(CarMode.DYNO)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 15.0, 2.0)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        self.mix.set_car_mode(CarMode.NORMAL)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, NMSts.no_valid, 1.5)
    @allure.title("车控车设_VFCPNC16_EgyLvlElec")
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_vfc_caseid_1985814(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])
        self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])
        self.sd_tester.security_access_level(UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x2F,0x42,0x9D,0x03,0x30,0x00],recv=[0x6F])
        self.bus_comm.check_egylvlelec(mai=3, subtype=0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0, 1.5)
        self.sd_tester.send_request_and_recv_response([0x2F,0x42,0x9D,0x03,0x00,0x00],recv=[0x6F])

    @allure.title("车控车设_VFCPNC16_UsgModMgr_VehNotParkInfoWarn")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_vfc_caseid_1985734(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.bus_comm.set_trsm_park_lockd(TrsmParkLockd=TrsmParkLockd.ParkNotEngd)
        self.bus_comm.check_veh_not_park_info_warn(VehNotParkInfoWarn=VehNotParkInfoWarn.OutofP)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0) 

    @allure.title("车控车设_VFCPNC16_UsgModMgr_StrtMsgToDrvr")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.PNC16
    def test_vfc_caseid_1985733(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.bus_comm.set_strt_msg_to_mod_mngt(StrtMsgToModMngt=StrtMsgToModMngt.PwrUpDly)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.set_strt_req(up_type=UpType.SetUsageModeUp)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.Msg7)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0)

    # @allure.title("车控车设_VFCPNC16_mobMgr_ImobMgrWarnIndcn")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    # )
    # @pytest.mark.full
    # @pytest.mark.PNC16
    # def test_vfc_caseid_1985727(self):
    #     self.mix.clear_pnc(BGMPNC.PNC16)
    #     self.bus_comm.set_strt_msg_to_mod_mngt(StrtMsgToModMngt=StrtMsgToModMngt.PwrUpDly)
    #     self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.CONVENIENCE)
    #     self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
    #     self.mix.set_strt_req(up_type=UpType.SetUsageModeUp)
    #     self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.Msg7)
    #     self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0)

    @allure.title("车控车设_VFCPNC26_ClimaCmd切换")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.PNC26
    def test_vfc_caseid_1985815(self):
        self.mix.clear_pnc(BGMPNC.PNC26)
        self.bus_comm.set_singal("bodycan", "CcmBodyFr27", "EgyDesForClima",96.0)
        self.bus_comm.set_singal("bodycan", "CcmBodyFr25", "ClimaSts",0)
        self.bus_comm.set_battcp_estimd(0.0)
        self.bus_comm.wait_time_and_check_ClimaCmd(mai_new=0, mai_old=1, time=120)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC26, 3.0, 1.0)

    @allure.title("车控车设_VFCPNC26_UsgModSts切换")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC26
    def test_vfc_caseid_1986100(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL,ccp={186: 0x02, 13: 0x4})
        self.mix.clear_pnc(BGMPNC.PNC26)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.set_and_check_steer_wheel_sts(level1=HeatLevel.High,level2=HeatLevel.High)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC26, NMSts.valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC26, 10.0, 3.0)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC26, NMSts.no_valid)
        self.soa.set_and_check_steer_wheel_sts(level1=HeatLevel.Off,level2=HeatLevel.Off)

    @allure.title("车控车设_VFCPNC26_UsgModSts切换")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC26
    def test_vfc_caseid_1986099(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL,ccp={186: 0x02, 13: 0x4})
        self.mix.clear_pnc(BGMPNC.PNC26)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.soa.set_and_check_steer_wheel_sts(level1=HeatLevel.High,level2=HeatLevel.High)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC26, NMSts.no_valid)
        sleep(10)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC26, NMSts.no_valid)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC26, NMSts.valid)
        self.soa.set_and_check_steer_wheel_sts(level1=HeatLevel.Off,level2=HeatLevel.Off)

    @allure.title("车控车设_VFCPNC33_BrkPedlSnsrSt触发120")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC33
    def test_vfc_caseid_1985395(self):
        self.mix.clear_pnc(BGMPNC.PNC33)
        self.io.brake_light_close()
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC33, NMSts.valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC33, 120.0, 5.0)
        self.io.brake_light_open()

    
        
    @allure.title("车控车设_VFCPNC33_BrkPedlSnsrSt触发60")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC33
    def test_vfc_caseid_1985396(self):
        self.mix.clear_pnc(BGMPNC.PNC33)
        self.io.brake_light_close()
        self.io.brake_light_open()
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC33, NMSts.valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC33, 55.0, 5.0)

    @allure.title("479260_PNC29_VFC VehicleDriving UsgModMgr")
    @pytest.mark.smoke
    @pytest.mark.PNC29
    def test_caseid_113196(self):
        self.mix.clear_pnc(BGMPNC.PNC29)
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC29, 20.0, 5.0)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC29, NMSts.no_valid, timeout=30)

    @allure.title("464142_PNC29_VFC VehicleDriving UsgModMgr")
    @pytest.mark.smoke
    @pytest.mark.PNC29
    def test_caseid_1985404(self):
        self.mix.clear_pnc(BGMPNC.PNC29)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC29, 30.0, 2.0)
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC29, 30.0, 2.0)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC29, NMSts.no_valid, timeout=40)
    
    @allure.title("464142_PNC29_VFC VehicleDriving Power Outlet")
    @pytest.mark.smoke
    @pytest.mark.PNC29
    def test_caseid_1985511(self):
        self.mix.clear_pnc(BGMPNC.PNC29)
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 1)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC29, NMSts.no_valid, timeout=3)
        self.soa.set_power_outlet_req(PowerOutLetReq.Off)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 2)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC29, NMSts.no_valid, timeout=3)

    @allure.title("464142_PNC29_VFC VehicleDriving Power Outlet")
    @pytest.mark.smoke
    @pytest.mark.PNC29
    def test_caseid_1985519_1985520(self):
        self.mix.clear_pnc(BGMPNC.PNC29)
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.soa.set_power_outlet_req(PowerOutLetReq.On)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 1)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC29, NMSts.no_valid, timeout=3)
        self.soa.set_power_outlet_req(PowerOutLetReq.Off)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", 2)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC29, NMSts.no_valid, timeout=3)

    @allure.title("车控车设_VFCPNC29_RlyPwrDistbnCmd1WdIgnRlyCmd")
    @pytest.mark.smoke
    @pytest.mark.PNC29
    def test_caseid_1985813(self):
        self.mix.clear_pnc(BGMPNC.PNC29)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC29, NMSts.valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC29, 3.0, 1.0)

    @allure.title("车控车设_VFCPNC29_RlyPwrDistbnCmd1WdBattSaveCmd")
    @pytest.mark.smoke
    @pytest.mark.PNC29
    def test_caseid_1985812(self):
        self.mix.clear_pnc(BGMPNC.PNC29)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC29, NMSts.valid)
    
    @allure.title("车控车设_VFCPNC29_UsageMode")
    @pytest.mark.smoke
    @pytest.mark.PNC29
    def test_caseid_1985740(self):
        self.mix.clear_pnc(BGMPNC.PNC29)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC29, NMSts.no_valid, 60.0)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC29, 15.0, 1.0)
        sleep(10)
           
    @allure.title("车控车设_VFCPNC29_EgyLvlElec")
    @pytest.mark.smoke
    @pytest.mark.PNC29
    def test_caseid_1985739(self):
        self.mix.clear_pnc(BGMPNC.PNC29)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])
        self.sd_tester.security_access_level(UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x2F,0x42,0x9E,0x03,0x51,0x00],recv=[0x6F])
        self.bus_comm.check_pwrlvlelec(mai=5,subtype=1)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC29, 15.0, 1.5)
        self.sd_tester.send_request_and_recv_response([0x2F,0x42,0x9E,0x03,0x00,0x00],recv=[0x6F])

    @allure.title("车控车设_VFCPNC29_PwrLvlElec")
    @pytest.mark.smoke
    @pytest.mark.PNC29
    def test_caseid_1985738(self):
        self.mix.clear_pnc(BGMPNC.PNC29)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])
        self.sd_tester.security_access_level(UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x2F,0x42,0x9D,0x03,0x30,0x00],recv=[0x6F])
        self.bus_comm.check_egylvlelec(mai=3, subtype=0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC29, 15.0, 1.5)
        self.sd_tester.send_request_and_recv_response([0x2F,0x42,0x9D,0x03,0x00,0x00],recv=[0x6F])

    @allure.title("437464_PNC39_Crash_UsgModActv")
    @pytest.mark.smoke
    @pytest.mark.PNC39
    def test_caseid_1985690(self):
        self.mix.clear_pnc(BGMPNC.PNC39)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC39, NMSts.no_valid, 10.0)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC39, 20.0, 5.0)
        self.mix.set_common_precontion(UsageMode.ABANDONED)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC39, NMSts.no_valid, 10.0)
        self.mix.set_car_mode(CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=49)

    @allure.title("437464_PNC39_Crash_UsgModActv")
    @pytest.mark.smoke
    @pytest.mark.PNC39
    def test_caseid_1989810(self):
        self.mix.clear_pnc(BGMPNC.PNC39)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC39, NMSts.no_valid, 10.0)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC39, 20.0, 5.0)
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC39, NMSts.no_valid, 10.0)
        self.mix.set_car_mode(CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=49)

    @allure.title("437464_PNC39_Crash_UsgModActv")
    @pytest.mark.smoke
    @pytest.mark.PNC39
    def test_caseid_1989812(self):
        self.mix.clear_pnc(BGMPNC.PNC39)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC39, NMSts.no_valid, 10.0)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC39, 20.0, 5.0)
        self.mix.set_common_precontion(UsageMode.CONVENIENCE)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC39, NMSts.no_valid, 10.0)
        self.mix.set_car_mode(CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=49)

    @allure.title("437464_PNC39_Crash_UsgModActv")
    @pytest.mark.smoke
    @pytest.mark.PNC39
    def test_caseid_1989815(self):
        self.mix.clear_pnc(BGMPNC.PNC39)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC39, NMSts.no_valid, 10.0)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC39, 20.0, 5.0)
        self.mix.set_common_precontion(UsageMode.CONVENIENCE)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC39, NMSts.no_valid, 10.0)
        self.mix.set_car_mode(CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=49)

    @allure.title("车辆启动HvActvForVehModReq_PNC24置位3s")
    @pytest.mark.smoke
    @pytest.mark.PNC24
    def test_caseid_1985732(self):
        self.mix.clear_pnc(BGMPNC.PNC24)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, 3.0, 1.0)

    @allure.title("车辆启动powertrain_PNC24置位3s")
    @pytest.mark.PNC24
    def test_caseid_1985731(self):
        self.mix.clear_pnc(BGMPNC.PNC24)
        self.bus_comm.set_driving_preconditions(engSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake, imobengsts1=ImobSts.ImobMtn)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.set_strt_req(up_type=UpType.GeatAuto)
        self.bus_comm.check_DrvrStrtReq(StrtReq=StrtReq.Reqd)
        self.bus_comm.check_PtActvnReq(PtActvnReq=PtActvnReq1.PtActvnReq)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC24, 3.0, 1.0)
        