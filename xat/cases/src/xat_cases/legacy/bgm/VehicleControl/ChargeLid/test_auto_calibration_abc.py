#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_service_stayconvenience_mode_abc.py
@Author      : heng.wang@jiduauto.com
@Time        : 2024/1/26 13:20
@Description: BGMusagmode驻车舒享服务相关抽象接口用例
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
@allure.story("整车模式/使用模式")
class TestUsageMode(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["VehicleModeService_client", "ObtDiagService_client","KeyService_client"])
        self.tsp.get_remote_diag_token()
        self.sd_tester.write_ccp(ccp={973: 2})
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        time.sleep(5)

    def before_each_func(self, ecu):
        self.io.bgm_diag_line_down()
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionClose)
        self.bus_comm.set_vehmtn()
        self.bus_comm.set_vehspd()
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr18", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        time.sleep(1)
        self.bus_comm.set_dtc_pre()
        self.bus_comm.set_batterylow_mode(DCChrgnHndlSts=DCChrgnHndlSts.Disconnected, DispHvBattLvlOfChrg=80.0)
        self.bus_comm.set_charging_sts(ChargingSts.Default)
        self.bus_comm.set_singal(bus="propulsioncan", msg="EcmPropComFr10", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.set_dcdc_battary_act_sts_on_can(DcDcActvd=DcDcActvd.ConversionToLVSide)
        self.bus_comm.set_dispbattegyout(DispBattEgyOut=40.0)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=True)
        self.sd_tester.stop_tester_present()
        pass

    def after_each_func(self, ecu):
        self.soa.set_auto_calibration(req=calibration_req.kOff ,source=SourceType.kScreen, isAlloweSkip=False)
        time.sleep(0.5)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.io.set_five_door_sts(sts=Door.close)
        self.io.driver_seat_notpresent()
        self.bus_comm.set_secle_seat_notpresent()
        self.bus_comm.set_pass_seat_notpresent()
        self.io.hazard_light_close()
        self.io.bgm_diag_line_up()
        pass

    def after_class(self, ecu):
        time.sleep(0.5)

    def find_info_from_log(self, phase, key_word):
        global bgm_log_goto_sleep
        global bgm_log_awakeup
        if phase == "sleep":
            if bgm_log_goto_sleep.find(key_word) != -1:
                return True
            else:
                return False
        elif phase == "awakeup":
            if bgm_log_awakeup.find(key_word) != -1:
                return True
            else:
                return False
        else:
            logger.error("输入的'phase'参数不正确，请重新输入")
            return False
    def chek_key_info_in_awakeup_stage(self,key_info):  
        global bgm_log_awakeup
        logger.info("Check INFO:{}".format(key_info))
        check_result= self.find_info_from_log("awakeup",key_info)
        if check_result:
            logger.info("查询到关键信息：{}".format(key_info))
            assert True
        else:
            logger.info("未能查询到关键信息：{}".format(key_info))
            assert False

    @pytest.mark.smoke
    @allure.title("智能标定_端到端_远程诊断")
    def test_remote_diag_caseid_1990800(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:1 para:{"code":0}','sig 1 remote session is open:true'],timeout=20):    
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen,session_time_out=600) 
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SendDiagCmd_cali)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
        self.bus_comm.check_ChrgLidManvgDCorAcDc_CalReq2(Req2=Inact.Active)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=True)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Active)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        self.soa.get_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        time.sleep(5)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=False)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Inactive)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)

    @pytest.mark.sanity
    def test_caseid_1990799(self):
        '''智能标定_接口触发非授权标定_远程 '''
        self.soa.set_auto_calibration(source=SourceType.kRemote, isAlloweSkip=True)
        self.bus_comm.check_ChrgLidManvgDCorAcDc_CalReq2(Req2=Inact.Active)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=True)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Active)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        self.soa.get_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        time.sleep(5)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=False)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Inactive)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
    
    @pytest.mark.sanity
    def test_caseid_1990798(self):
        '''智能标定_接口触发授权标定_远程 '''
        self.soa.set_auto_calibration(source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
        self.bus_comm.check_ChrgLidManvgDCorAcDc_CalReq2(Req2=Inact.Active)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=True)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Active)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        self.soa.get_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        time.sleep(5)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=False)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Inactive)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
    
    @pytest.mark.full
    def test_caseid_1990797(self):
        '''智能标定_接口触发非授权标定_屏幕 '''
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=True)
        self.bus_comm.check_ChrgLidManvgDCorAcDc_CalReq2(Req2=Inact.Active)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=True)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Active)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        self.soa.get_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        time.sleep(5)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=False)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Inactive)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
    
    @pytest.mark.full
    def test_caseid_1990796(self):
        '''智能标定_接口触发授权标定_屏幕 '''
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
        self.bus_comm.check_ChrgLidManvgDCorAcDc_CalReq2(Req2=Inact.Active)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=True)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Active)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        self.soa.get_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        time.sleep(5)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=False)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Inactive)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
    
    @pytest.mark.full
    def test_caseid_1990795(self):
        '''智能标定_接口触发非授权标定_语音 '''
        self.soa.set_auto_calibration(source=SourceType.kVoicd, isAlloweSkip=True)
        self.bus_comm.check_ChrgLidManvgDCorAcDc_CalReq2(Req2=Inact.Active)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=True)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Active)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        self.soa.get_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        time.sleep(5)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=False)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Inactive)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
    
    @pytest.mark.full
    def test_caseid_1990794(self):
        '''智能标定_接口触发授权标定_语音 '''
        self.soa.set_auto_calibration(source=SourceType.kVoicd, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
        self.bus_comm.check_ChrgLidManvgDCorAcDc_CalReq2(Req2=Inact.Active)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=True)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Active)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        self.soa.get_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        time.sleep(5)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=False)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Inactive)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
    
    @pytest.mark.full
    def test_caseid_1990793(self):
        '''智能标定_存在竞争业务 '''
        self.io.bgm_diag_line_up()
        time.sleep(1)
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kHighPriorityRunning)
    
    @pytest.mark.full
    def test_caseid_1990792(self):
        '''智能标定_存在低优先级竞争业务 '''
        self.io.bgm_diag_line_up()
        time.sleep(1)
        self.io.bgm_diag_line_down()
        time.sleep(1)
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
        self.bus_comm.check_ChrgLidManvgDCorAcDc_CalReq2(Req2=Inact.Active)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=True)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Active)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        self.soa.get_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        time.sleep(5)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=False)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Inactive)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
    
    @pytest.mark.full
    def test_caseid_1990791(self):
        '''智能标定_授权超时 '''
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization)
        time.sleep(30)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kAuthorizedTimeout)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
    
    @pytest.mark.full
    def test_caseid_1990790(self):
        '''智能标定_取消授权 '''
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kCancelAuthorize)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kAuthorizedFailed)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)

    @pytest.mark.full
    def test_caseid_1990789(self):
        '''智能标定_标定前提条件不满足_非P档 '''
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
        self.soa.event_check_Calibration_Status_Info(text_id=21, status=calibration_status.kCheckPreconditionFailed)
    
    @pytest.mark.full
    def test_caseid_1990788(self):
        '''智能标定_标定前提条件不满足_插枪 '''
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
        self.soa.event_check_Calibration_Status_Info(text_id=21, status=calibration_status.kCheckPreconditionFailed)
    
    @pytest.mark.full
    def test_caseid_1990787(self):
        '''智能标定_标定前提条件不满足后超时尝试 '''
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
        self.soa.event_check_Calibration_Status_Info(text_id=21, status=calibration_status.kCheckPreconditionFailed)
        time.sleep(30)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kCheckPreconditionTimeout)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
    
    @pytest.mark.full
    def test_caseid_1990786(self):
        '''智能标定_标定前提条件不满足后超时尝试 '''
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
        self.soa.event_check_Calibration_Status_Info(text_id=21, status=calibration_status.kCheckPreconditionFailed)
        self.soa.set_Calibration_Retry(req=retry_req.kCancel)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kCheckPreconditionFailed)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
    
    @pytest.mark.full
    def test_caseid_1990785(self):
        '''智能标定_标定前提条件不满足后重试满足条件 '''
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
        self.soa.event_check_Calibration_Status_Info(text_id=21, status=calibration_status.kCheckPreconditionFailed)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        time.sleep(1)
        self.soa.set_Calibration_Retry(req=retry_req.kRetry)
        self.bus_comm.check_ChrgLidManvgDCorAcDc_CalReq2(Req2=Inact.Active)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=True)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Active)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        self.soa.get_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        time.sleep(5)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=False)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Inactive)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
    
    @pytest.mark.full
    def test_caseid_1990784(self):
        '''智能标定_标定失败 '''
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
        self.bus_comm.check_ChrgLidManvgDCorAcDc_CalReq2(Req2=Inact.Active)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=True)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Active)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        self.soa.get_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        time.sleep(15)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kRoutineFailed)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
    
    @pytest.mark.full
    def test_caseid_1990783(self):
        '''智能标定_标定中主动取消 '''
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
        self.bus_comm.check_ChrgLidManvgDCorAcDc_CalReq2(Req2=Inact.Active)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=True)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Active)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        self.soa.get_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        self.soa.set_auto_calibration(req=calibration_req.kOff ,source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kUserCancelRoutine)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)

    @allure.title(" 智能标定_日志确认标定失败")
    @pytest.mark.full
    @pytest.mark.test1125
    def test_remote_diag_caseid_1990781(self):
        global bgm_log_awakeup
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:1 para:{"code":0}','sig 1 remote session is open:true'],timeout=20):    
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen,session_time_out=600) 
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SendDiagCmd_cali)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
        self.bus_comm.check_ChrgLidManvgDCorAcDc_CalReq2(Req2=Inact.Active)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=True)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Active)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        self.soa.get_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        time.sleep(15)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kRoutineFailed)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        sleep_log_last, awakeup_log_last=self.ssh.read_auto_jetlog()
        bgm_log_awakeup=sleep_log_last
        logger.info("%%%%%%%%%%%%%%%%%%%%%%%%%%")
        logger.info(bgm_log_awakeup)
        key_info = "rx 1002:71 01 20 31 10"
        self.chek_key_info_in_awakeup_stage(key_info)
        key_info1 = "0x31, 0x03, 0x20, 0x31"
        self.chek_key_info_in_awakeup_stage(key_info1)
        sleep(10)

    @allure.title(" 智能标定_日志确认标定成功")
    @pytest.mark.full
    @pytest.mark.test1125
    def test_remote_diag_caseid_1990782(self):
        global bgm_log_awakeup
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:1 para:{"code":0}','sig 1 remote session is open:true'],timeout=20):    
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen,session_time_out=600) 
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SendDiagCmd_cali)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
        self.bus_comm.check_ChrgLidManvgDCorAcDc_CalReq2(Req2=Inact.Active)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=True)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Active)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        self.soa.get_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        time.sleep(5)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=False)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Inactive)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        sleep_log_last, awakeup_log_last=self.ssh.read_auto_jetlog()
        bgm_log_awakeup=sleep_log_last
        logger.info("%%%%%%%%%%%%%%%%%%%%%%%%%%")
        logger.info(bgm_log_awakeup)
        key_info = "触发源:RemoteDiag"
        self.chek_key_info_in_awakeup_stage(key_info)
        key_info1 = "功能名称：充电口盖标定"
        self.chek_key_info_in_awakeup_stage(key_info1)
        key_info2 = "用户授权成功"
        self.chek_key_info_in_awakeup_stage(key_info2)
        key_info3 = "前置条件检查通过"
        self.chek_key_info_in_awakeup_stage(key_info3)
        key_info4 = "标定成功"
        self.chek_key_info_in_awakeup_stage(key_info4)
        sleep(10)

    @allure.title(" 智能标定_日志确认标定成功（远程日志）")
    @pytest.mark.full
    @pytest.mark.test1125
    def test_remote_diag_caseid_1995676(self):
        global bgm_log_awakeup
        with self.log_manage.check_jetlog_by_keywords(log_type=" LUA_", keywords=['cmd:1 para:{"code":0}','sig 1 remote session is open:true'],timeout=20):    
            self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionOpen,session_time_out=600) 
        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SendDiagCmd_cali)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
        self.bus_comm.check_ChrgLidManvgDCorAcDc_CalReq2(Req2=Inact.Active)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=True)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Active)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        self.soa.get_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        time.sleep(5)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=False)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Inactive)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        sleep_log_last, awakeup_log_last=self.ssh.read_auto_jetlog()
        bgm_log_awakeup=sleep_log_last
        logger.info("%%%%%%%%%%%%%%%%%%%%%%%%%%")
        logger.info(bgm_log_awakeup)
        key_info = "[39,5]"
        self.chek_key_info_in_awakeup_stage(key_info)
        key_info1 = "[39,6]"
        self.chek_key_info_in_awakeup_stage(key_info1)
        key_info2 = "[113,3,32,49,16,1]"
        self.chek_key_info_in_awakeup_stage(key_info2)
        key_info3 = "[49,3,32,49]"
        self.chek_key_info_in_awakeup_stage(key_info3)
        sleep(10)

    @allure.title(" 智能标定_存在高优先级竞争业务_无需授权")
    @pytest.mark.full
    @pytest.mark.test1125
    def test_caseid_1995760(self):
        '''智能标定_存在竞争业务 '''
        self.io.bgm_diag_line_up()
        time.sleep(1)
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=True)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kHighPriorityRunning)
    
    @allure.title(" 智能标定_标定前提条件不满足_N档_无需授权")
    @pytest.mark.full
    @pytest.mark.test1125
    def test_caseid_1995761(self):
        '''智能标定_标定前提条件不满足_非P档 '''
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=True)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning)
        self.soa.event_check_Calibration_Status_Info(text_id=21, status=calibration_status.kCheckPreconditionFailed)
    
    @allure.title(" 智能标定_标定前提条件不满足_D档_无需授权")
    @pytest.mark.full
    @pytest.mark.test1125
    def test_caseid_1995762(self):
        '''智能标定_标定前提条件不满足_非P档 '''
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
        self.soa.event_check_Calibration_Status_Info(text_id=21, status=calibration_status.kCheckPreconditionFailed)
    
    @allure.title(" 智能标定_标定前提条件不满足_N挡_无需授权_重试取消")
    @pytest.mark.full
    @pytest.mark.test1125
    def test_caseid_1995819(self):
        '''智能标定_标定前提条件不满足_非P档 '''
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=True)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning)
        self.soa.set_Calibration_Retry(req=retry_req.kRetry)
        self.soa.set_auto_calibration(req=calibration_req.kOff ,source=SourceType.kScreen, isAlloweSkip=True)
        self.soa.event_check_Calibration_Status_Info(text_id=21, status=calibration_status.kCheckPreconditionFailed)
        
    @allure.title(" 智能标定_标定前提条件不满足_N挡_无需授权_重试满足条件")
    @pytest.mark.full
    @pytest.mark.test1125
    def test_caseid_1995820(self):
        '''智能标定_标定前提条件不满足_非P档 '''
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=True)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning)
        self.soa.event_check_Calibration_Status_Info(text_id=21, status=calibration_status.kCheckPreconditionFailed)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        time.sleep(1)
        self.soa.set_Calibration_Retry(req=retry_req.kRetry)
        self.bus_comm.check_ChrgLidManvgDCorAcDc_CalReq2(Req2=Inact.Active)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=True)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Active)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        self.soa.get_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        time.sleep(5)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=False)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Inactive)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)

    @allure.title(" 智能标定_标定前提条件不满足_D挡_需要授权_重试条件还不满足")
    @pytest.mark.full
    @pytest.mark.test1125
    def test_caseid_1995828(self):
        '''智能标定_标定前提条件不满足_非P档 '''
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
        self.soa.event_check_Calibration_Status_Info(text_id=21, status=calibration_status.kCheckPreconditionFailed)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        time.sleep(1)
        self.soa.set_Calibration_Retry(req=retry_req.kRetry)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)

    @allure.title(" 智能标定_标定前提条件不满足_R挡运动_无需授权_重试条件还不满足")
    @pytest.mark.full
    @pytest.mark.test1126
    def test_caseid_1995829(self):
        '''智能标定_标定前提条件不满足_非P档 '''
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=True)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning)
        self.soa.event_check_Calibration_Status_Info(text_id=21, status=calibration_status.kCheckPreconditionFailed)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        time.sleep(1)
        self.soa.set_Calibration_Retry(req=retry_req.kRetry)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        

    @allure.title(" 智能标定_标定前提条件不满足_D挡运动_需要授权_重试条件满足")
    @pytest.mark.full
    @pytest.mark.test1126
    def test_caseid_1995830(self):
        '''智能标定_标定前提条件不满足_非P档 '''
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning)
        self.soa.event_check_Calibration_Status_Info(text_id=21, status=calibration_status.kCheckPreconditionFailed)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.sd_tester.stop_tester_present()
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        time.sleep(1)
        self.bus_comm.lin_send_pwm(lin_bus=LinChannel.LIN2)
        self.soa.set_Calibration_Retry(req=retry_req.kRetry)
        self.bus_comm.check_ChrgLidManvgDCorAcDc_CalReq2(Req2=Inact.Active)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=True)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Active)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        self.soa.get_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        time.sleep(5)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=False)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Inactive)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        self.sd_tester.sd_tester.tester_present()


    @allure.title(" 智能标定_标定前提条件不满足_R挡运动_需要授权_重试条件满足")
    @pytest.mark.full
    @pytest.mark.test1126
    def test_caseid_1995831(self):
        '''智能标定_标定前提条件不满足_非P档 '''
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning)
        self.soa.event_check_Calibration_Status_Info(text_id=21, status=calibration_status.kCheckPreconditionFailed)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.sd_tester.stop_tester_present()
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        time.sleep(1)
        self.soa.set_Calibration_Retry(req=retry_req.kRetry)
        self.bus_comm.check_ChrgLidManvgDCorAcDc_CalReq2(Req2=Inact.Active)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=True)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Active)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        self.soa.get_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        time.sleep(5)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=False)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Inactive)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        self.sd_tester.sd_tester.tester_present()

    @allure.title(" 智能标定_标定前提条件不满足_N挡运动_无需授权_重试条件满足")
    @pytest.mark.full
    @pytest.mark.test1126
    def test_caseid_1995832(self):
        '''智能标定_标定前提条件不满足_非P档 '''
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=True)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning)
        self.soa.event_check_Calibration_Status_Info(text_id=21, status=calibration_status.kCheckPreconditionFailed)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        time.sleep(1)
        self.soa.set_Calibration_Retry(req=retry_req.kRetry)
        self.bus_comm.check_ChrgLidManvgDCorAcDc_CalReq2(Req2=Inact.Active)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=True)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Active)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        self.soa.get_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        time.sleep(5)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=False)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Inactive)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)

    @allure.title(" 智能标定_标定前提条件不满足_插交流枪_无需认证_重试满足条件")
    @pytest.mark.full
    @pytest.mark.test1126
    def test_caseid_1995833(self):
        '''智能标定_标定前提条件不满足_非P档 '''
        self.bus_comm.set_onbd_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=True)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning)
        self.soa.event_check_Calibration_Status_Info(text_id=21, status=calibration_status.kCheckPreconditionFailed)
        self.bus_comm.set_onbd_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        time.sleep(1)
        self.soa.set_Calibration_Retry(req=retry_req.kRetry)
        self.bus_comm.check_ChrgLidManvgDCorAcDc_CalReq2(Req2=Inact.Active)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=True)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Active)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        self.soa.get_Calibration_Status_Info(status=calibration_status.kCalibrationRunning)
        time.sleep(5)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalRqrdFb(CalRqrdFb=False)
        self.bus_comm.set_ChrgLidManvgDCorAcDc_CalActvSts2(ActvSts2=Inact.Inactive)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)

    @allure.title(" 智能标定_标定前提条件不满足_插交流_超时未重试")
    @pytest.mark.full
    @pytest.mark.test1126
    def test_caseid_1995834(self):
        '''智能标定_标定前提条件不满足_非P档 '''
        self.bus_comm.set_onbd_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=True)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning)
        self.soa.event_check_Calibration_Status_Info(text_id=21, status=calibration_status.kCheckPreconditionFailed)
        self.soa.set_Calibration_Retry(req=retry_req.kCancel)
        self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kCheckPreconditionFailed)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)

    @allure.title(" 智能标定_标定前提条件不满足_插直流枪_无需认证_重试条件还不满足")
    @pytest.mark.full
    @pytest.mark.test1126
    def test_caseid_1995835(self):
        '''智能标定_标定前提条件不满足_非P档 '''
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.soa.set_auto_calibration(source=SourceType.kScreen, isAlloweSkip=True)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning)
        self.soa.event_check_Calibration_Status_Info(text_id=21, status=calibration_status.kCheckPreconditionFailed)
        time.sleep(1)
        self.soa.set_Calibration_Retry(req=retry_req.kRetry)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        