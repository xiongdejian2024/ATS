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
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        pass

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
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

    def set_windows_pre_condition(self):
        self.mix.set_common_precontion()
        self.io.set_bgm_hardware_condition_to_default()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.bus_comm.set_five_door_opener_sts(door_opener=DoorOpenerSts.FullClsd)  # 设置bodycan上五个电动门均关闭
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)

    @allure.title("432965_PNC37_Windows_ClsdDueToRain")
    @pytest.mark.full
    @pytest.mark.windows
    def test_vfc_caseid_1985691(self):
        self.set_windows_pre_condition()
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_40,pos_lere=WinPos.percent_80,pos_rire=WinPos.percent_100)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.percent_4)
        sleep(2.8)
        self.bus_comm.check_without_close_win_dueto_rain_req()
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC37, 5.0, 2.0)

    @allure.title("432965_PNC37_Windows_RainDetected")
    @pytest.mark.full
    @pytest.mark.windows
    def test_vfc_caseid_1985692(self):
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100)
        self.trigger_auto_close_wins_by_rain()
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr03",'RainDetected', 1)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        self.bus_comm.check_four_windows_position_req(pos=WinPos.close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC37, 3.0, 2.0)

    
    
    @allure.title("车控车设_VFCPNC16_激活雨刮_RainSnsrStsToHMI")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_vfc_caseid_1985693(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front,isOn.Off)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check_wiper_rain_sensor(RainSnsrStsToHMI.On)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)

    @allure.title("477143_PNC16_InfotainmentPush WiprWshrMgr_雨刮系统故障")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.PNC16
    @pytest.mark.wiper
    def test_vfc_caseid_1985694(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.sd_tester.write_ccp({401:0x02})
        self.mix.set_dtc_precontion()
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0)
        self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.Rainerror,last_time=3)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",1,timeout=5)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0, 2.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0,timeout=5)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0, 2.0)

    @allure.title("车控车设_VFCPNC16_前洗涤_WshrFldTankStsToHMI")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_vfc_caseid_1985695(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.sd_tester.send_request_and_recv_response([0x10,0x01],recv=[0x50,0x01])
        self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])
        self.sd_tester.security_access_level(UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x2F,0x42,0x0A,0x03,0x01],recv=[0x6F, 0x42, 0X0A])
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        self.sd_tester.send_request_and_recv_response([0x2F,0x42,0x0A,0x03,0x02],recv=[0x6F, 0x42, 0X0A])
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 2.0, 1.5)
        self.sd_tester.send_request_and_recv_response([0x2F,0x42,0x0A,0x00],recv=[0x6F, 0x42, 0X0A])

    @allure.title("车控车设_VFCPNC16_RLSM故障_WiprSysFailrDetdSafe")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_vfc_caseid_1985696(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(10)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WiprMotErrSafe",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr18","WiprSysFailrDetdSafe",2)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WiprMotErrSafe",0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 5.0, 1.5)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)

    @allure.title("车控车设_VFCPNC16_洗涤状态_WshrLvrPosn")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_vfc_caseid_1985697(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front,sts=isOn.Off)
        sleep(2)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front,sts=isOn.On)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0 ,1.5)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front,sts=isOn.Off)

    @allure.title("车控车设_VFCPNC20_RainSensActvn雨刮")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC20
    def test_vfc_caseid_1985698(self):
        self.mix.clear_pnc(BGMPNC.PNC20)
        self.mix.set_common_precontion(UsageMode.DRIVING,ccp={401:0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)  
        sleep(1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC20, 3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)

    @allure.title("474494_PNC37_Windows_ShortDropWinDrvrDoor")
    @pytest.mark.full
    @pytest.mark.PNC37
    def test_vfc_caseid_1989484(self):
        self.sd_tester.write_ccp({561: 0x2,94:0x02})
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.set_windows_pre_condition()
        sleep(1)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        sleep(0.5)
        # self.bus_comm.check_windows_short_drop_req(pos_drvr=WinShortDropReq.Open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC37, 5.0, 2.0)
        # self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        # self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC37, 3.0, 2.0)

    @allure.title("474494_PNC37_Windows_ShortDropWinPassDoor")
    @pytest.mark.full
    @pytest.mark.PNC37
    def test_vfc_caseid_1989485(self):
        self.sd_tester.write_ccp({561: 0x2,94:0x02})
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.set_windows_pre_condition()
        sleep(1)
        self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval=0.5)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        sleep(0.5)
        # self.bus_comm.check_windows_short_drop_req(pos_pass=WinShortDropReq.Open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC37, 5.0, 2.0)
        # self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        # self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC37, 3.0, 2.0)

    @allure.title("474494_PNC37_Windows_ShortDropWinRiReDoor")
    @pytest.mark.full
    @pytest.mark.PNC37
    def test_vfc_caseid_1991425(self):
        self.sd_tester.write_ccp({561: 0x2,94:0x02})
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.set_windows_pre_condition()
        sleep(1)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=0.5)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        sleep(0.5)
        # self.bus_comm.check_windows_short_drop_req(pos_rire=WinShortDropReq.Open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC37, 5.0, 2.0)
        # self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        # self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC37, 3.0, 2.0)

    @allure.title("474494_PNC37_Windows_ShortDropWinLeReDoor")
    @pytest.mark.full
    @pytest.mark.PNC37
    def test_vfc_caseid_1991426(self):
        self.sd_tester.write_ccp({561: 0x2,94:0x02})
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.set_windows_pre_condition()
        sleep(1)
        self.mix.push_door_outer_switch(pos=DoorPos.RearLeft,time_interval=0.5)
        sleep(0.5)
        self.bus_comm.set_5_door_lock_status(CenLockSts.Unlock)
        sleep(0.7)
        # self.bus_comm.check_windows_short_drop_req(pos_lere=WinShortDropReq.Open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC37, 5.0, 2.0)
        # self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        # self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC37, 3.0, 2.0)

    @allure.title("车控车设_VFCPNC20_WiprInPosnForSrv雨刮")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.sanity_1
    @pytest.mark.PNC20
    def test_vfc_caseid_1985700(self):
        self.mix.clear_pnc(BGMPNC.PNC20)
        self.mix.set_common_precontion(UsageMode.DRIVING,ccp={401:0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        sleep(1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC20, 3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)


    @allure.title("车控车设_VFCPNC20_WinDefrstFrnt_激活后除霜")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC20
    def test_vfc_caseid_1985703(self):
        self.mix.clear_pnc(BGMPNC.PNC20)
        self.mix.set_rear_defrost_sts(sts=True)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC20, 3.0)
        self.mix.set_rear_defrost_sts(sts=False)

    @allure.title("477144_PNC20_Visibility WiprWshrMgr_激活雨刮RainSensActvn")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.PNC20
    @pytest.mark.wiper
    def test_vfc_caseid_1985699(self):
        self.mix.clear_pnc(BGMPNC.PNC20)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC20, 3.0,2.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC20, 3.0,2.0)

    # @allure.title("477144_PNC20_Visibility WiprWshrMgr_雨刮位置WipgInfo")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    # )
    # @pytest.mark.full
    # @pytest.mark.PNC20
    # def test_vfc_caseid_1985701(self):
        
    #     self.mix.clear_pnc(BGMPNC.PNC20)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
    #     self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
    #     self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
    #     self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",1)
    #     self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC20, 3.0,2.0)
    #     self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
    #     self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
    #     self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC20, 3.0,2.0)

    