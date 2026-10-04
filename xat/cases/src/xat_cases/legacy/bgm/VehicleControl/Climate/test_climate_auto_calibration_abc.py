#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : xiangyue.li@jiduauto.com
@Time        : 2023/11/21 11:30
@Description : BGM空调功能
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
@allure.story("空调功能")
class TestSeatCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["VehicleModeService_client","ObtDiagService_client"])
        self.tsp.get_remote_diag_token()
        time.sleep(5)


    def before_each_func(self, ecu):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)


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
        self.bus_comm.centrl_lock_pre_msg_send_ctrl(sts=MsgSendContrl.Start)
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    @pytest.mark.sanity
    def test_caseid_0000001(self):
        diag_request = []
        '''智能标定_接口触发授权标定_远程-10 '''
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(2)
        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.ClimateVent,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.ClimateVent)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.ClimateVent)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x711,resp_id=0x611,
                                                           check_req_data=[0x10, 0x03],send_resp_data=[0x50, 0x03, 0x00, 0x32, 0x01, 0xF4])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x711,resp_id=0x611,
                                                           check_req_data=[0X27,0X05],send_resp_data=[0x67, 0x05, 0x01, 0x02, 0x03])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x711,resp_id=0x611,
                                                           check_req_data=[0X27,0X06],send_resp_data=[0x67, 0x06],check_len=2)
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x711,resp_id=0x611,
                                                           check_req_data=[0X31,0X01,0xDF, 0x20],send_resp_data=[0x71, 0x01,0xDF, 0x20, 0x10])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x711,resp_id=0x611,
                                                           check_req_data=[0X31,0X03,0xDF, 0x20],send_resp_data=[0x71, 0x03,0xDF, 0x20, 0x10,0x00])
        
    @pytest.mark.sanity
    def test_caseid_0000002(self):
        diag_request = []
        '''智能标定_接口触发授权标定_远程-12 '''
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(2)
        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.ClimateVent,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.ClimateVent)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.ClimateVent)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x711,resp_id=0x611,
                                                           check_req_data=[0x10, 0x03],send_resp_data=[0x50, 0x03, 0x00, 0x32, 0x01, 0xF4])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x711,resp_id=0x611,
                                                           check_req_data=[0X27,0X05],send_resp_data=[0x67, 0x05, 0x01, 0x02, 0x03])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x711,resp_id=0x611,
                                                           check_req_data=[0X27,0X06],send_resp_data=[0x67, 0x06],check_len=2)
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x711,resp_id=0x611,
                                                           check_req_data=[0X31,0X01,0xDF, 0x20],send_resp_data=[0x71, 0x01,0xDF, 0x20, 0x12])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x711,resp_id=0x611,
                                                           check_req_data=[0X31,0X03,0xDF, 0x20],send_resp_data=[0x71, 0x03,0xDF, 0x20, 0x10,0x00])
        
    @pytest.mark.sanity
    def test_caseid_0000003(self):
        diag_request = []
        '''智能标定_无需授权_远程_10 '''
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(2)
        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.ClimateVent,source=SourceType.kRemote, isAlloweSkip=True)
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x711,resp_id=0x611,
                                                           check_req_data=[0x10, 0x03],send_resp_data=[0x50, 0x03, 0x00, 0x32, 0x01, 0xF4])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x711,resp_id=0x611,
                                                           check_req_data=[0X27,0X05],send_resp_data=[0x67, 0x05, 0x01, 0x02, 0x03])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x711,resp_id=0x611,
                                                           check_req_data=[0X27,0X06],send_resp_data=[0x67, 0x06],check_len=2)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.ClimateVent)
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x711,resp_id=0x611,
                                                           check_req_data=[0X31,0X01,0xDF, 0x20],send_resp_data=[0x71, 0x01,0xDF, 0x20, 0x10])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x711,resp_id=0x611,
                                                           check_req_data=[0X31,0X03,0xDF, 0x20],send_resp_data=[0x71, 0x03,0xDF, 0x20, 0x10,0x00])

    @pytest.mark.sanity
    def test_caseid_0000004(self):
        diag_request = []
        '''智能标定_无需授权_远程_12 '''
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(2)
        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.ClimateVent,source=SourceType.kRemote, isAlloweSkip=True)
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x711,resp_id=0x611,
                                                           check_req_data=[0x10, 0x03],send_resp_data=[0x50, 0x03, 0x00, 0x32, 0x01, 0xF4])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x711,resp_id=0x611,
                                                           check_req_data=[0X27,0X05],send_resp_data=[0x67, 0x05, 0x01, 0x02, 0x03])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x711,resp_id=0x611,
                                                           check_req_data=[0X27,0X06],send_resp_data=[0x67, 0x06],check_len=2)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.ClimateVent)
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x711,resp_id=0x611,
                                                           check_req_data=[0X31,0X01,0xDF, 0x20],send_resp_data=[0x71, 0x01,0xDF, 0x20, 0x10])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x711,resp_id=0x611,
                                                           check_req_data=[0X31,0X03,0xDF, 0x20],send_resp_data=[0x71, 0x03,0xDF, 0x20, 0x10,0x00])
  