#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_steerwheel_ctrl.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/11/21 11:30
@Description: BGM车控车座椅功能
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
@allure.story("后视镜功能")
class TestSeatCtrl(TestABCBase):
    def before_class(self, ecu):
        # logger.info("------------------>复位BGM")
        # self.io.bgm_power_off()
        # sleep(2)
        # self.io.bgm_power_on()
        # time.sleep(15)
        # logger.info("------------------>复位BGM结束")

        self.soa.update(["VehicleModeService_client","ObtDiagService_client","SeatService_client", "cockpit_perception_service_server", "InteractiveService_server","ChassisService_client"])
        self.tsp.get_remote_diag_token()
        time.sleep(5)     



    def before_each_func(self, ecu):
        self.io.bgm_diag_line_down()
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)

        self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionClose)
        sleep(1)

    def after_each_func(self, ecu):
        self.soa.set_auto_calibration(req=calibration_req.kOff,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kScreen, isAlloweSkip=True)
        time.sleep(1)
        self.soa.set_auto_calibration(req=calibration_req.kOff,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kScreen, isAlloweSkip=True)
        time.sleep(1)
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
        time.sleep(0.5)
        pass
    
    def set_nopeople_incar(self):
        self.set_four_Door_open()
        self.io.driver_seat_notpresent()

        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04", 'PassSeatSts', 0)
        self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04", 'SeatOccptAtRowSecLe', 0)
        self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04", 'SeatOccptAtRowSecMid', 0)
        self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04", 'SeatOccptAtRowSecRi', 0)
      
        self.bus_comm.set_singal("backbonefr","SrsBackBoneFr05", 'BltLockStAtDrvrBltLockSt1', 0)        
        self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04", 'BltLockStAtPassBltLockSt1', 0)   
        self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04", 'BltLockStAtRowSecLeBltLockSt1', 0)     
        self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04", 'BltLockStAtRowSecMidBltLockSt1', 0)           
        self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04", 'BltLockStAtRowSecRiBltLockSt1', 0)          
        
        #确保开门3s后无人占座
        sleep(3)               


    def common_diag_communication(self):
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0x10, 0x03],send_resp_data=[0x50, 0x03, 0x00, 0x32, 0x01, 0xF4])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X27,0X05],send_resp_data=[0x67, 0x05, 0x01, 0x02, 0x03])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X27,0X06],send_resp_data=[0x67, 0x06],check_len=2)
        
        

    def common_diag_communication_Passenger(self):
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0x10, 0x03],send_resp_data=[0x50, 0x03, 0x00, 0x32, 0x01, 0xF4])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X27,0X05],send_resp_data=[0x67, 0x05, 0x01, 0x02, 0x03])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X27,0X06],send_resp_data=[0x67, 0x06],check_len=2)
        
        
        
    def set_four_Door_open(self):

        self.io.set_door(Drvr=Door.open)
        self.io.set_door(Pass=Door.open)
        self.io.set_door(LeRe=Door.open)
        self.io.set_door(RiRe=Door.open)
        
    @pytest.mark.sanity
    def test_caseid_0000002(self):
        '''智能标定_接口触发授权标定_远程 '''
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)

        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication()
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
  
  
    @allure.title("语音-授权请求-需授权-授权通过-主驾标定")
    @pytest.mark.full
    def test_caseid_1995879(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park, parklock=ParkLockSts.ParkEngd)
        self.soa.get_gear_level(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kVoicd, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
             
        
    @allure.title("语音-授权请求-无需授权-主驾标定")
    @pytest.mark.full
    def test_caseid_1995880(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kVoicd, isAlloweSkip=True)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)


        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
    @allure.title("屏幕-授权请求-需授权-授权通过-主驾标定")
    @pytest.mark.full
    def test_caseid_1995881(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
    @allure.title("屏幕-授权请求-无需授权-主驾标定")
    @pytest.mark.full
    def test_caseid_1995882(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kScreen, isAlloweSkip=True)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)


        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
    @allure.title("远程-授权请求-需授权-授权通过-主驾标定")
    @pytest.mark.sanity
    def test_caseid_1995903(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
    @allure.title("远程-授权请求-无需授权-主驾标定")
    @pytest.mark.sanity
    def test_caseid_1995904(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=True)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)


        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle) 
        
        
        
        
    @allure.title("远程-标定过程中取消-需要授权-主驾标定")
    @pytest.mark.full
    def test_caseid_1995887(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        
        self.soa.set_auto_calibration(req=calibration_req.kOff,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)

        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kUserCancelRoutine)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
    @allure.title("远程-标定过程中取消-无需授权-主驾标定")
    @pytest.mark.full
    def test_caseid_1995888(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=True)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)


        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        
        self.soa.set_auto_calibration(req=calibration_req.kOff,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)

        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kUserCancelRoutine)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
    @allure.title("远程-授权请求-需授权-取消授权-主驾标定")
    @pytest.mark.full
    def test_caseid_1995902(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kCancelAuthorize)
       
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kAuthorizedFailed)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
    @allure.title("远程-授权请求-需授权-授权超时-主驾标定")
    @pytest.mark.full
    def test_caseid_1995901(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        sleep(32)
       
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kAuthorizedTimeout)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
  
        
    @allure.title("屏幕-判断竞争任务-有高优先级诊断任务-需要授权-主驾标定")    #高优先级和授权，可能有问题  http://172.18.128.177:8080/2024_10_31_17_26_48
    @pytest.mark.full
    @pytest.mark.a1101
    def test_caseid_1995907(self):
        self.io.bgm_diag_line_up()
        sleep(1)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kHighPriorityRunning)
        # self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
    @allure.title("语音-判断竞争任务-有高优先级诊断任务-无需授权-主驾标定")   #http://172.18.128.177:8080/2024_10_31_17_35_34
    @pytest.mark.full
    @pytest.mark.a1101
    def test_caseid_1995906(self):
        self.io.bgm_diag_line_up()
        sleep(1)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kVoicd, isAlloweSkip=True)
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kHighPriorityRunning)

         
    # @allure.title("远程-前提条件判断-车辆N挡-静止-无需授权-超时无重试-主驾标定")  #1104
    # @pytest.mark.full
    # @pytest.mark.a11011
    # def test_caseid_1995900(self):
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Neut)
    #     self.soa.get_gear_level(gear=Gear.Neut)
    #     self.set_nopeople_incar()

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=True)
 
    #     sleep(31)
        
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kCheckPreconditionTimeout)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)      
        
        
        
    # @allure.title("远程-前提条件判断-车辆D挡-静止-需要授权-超时无重试-主驾标定")   #http://172.18.128.177:8080/2024_11_01_11_37_53  待跑
    # @pytest.mark.full
    # @pytest.mark.a11011
    # def test_caseid_1995899(self):   #http://172.18.128.177:8080/2024_11_01_15_34_15
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Drv)
    #     self.soa.get_gear_level(gear=Gear.Drv)
    #     self.set_nopeople_incar()

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        
    #     self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.DriverSeat,text_id=50)


    #     sleep(31)

    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kCheckPreconditionTimeout)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
    # @allure.title("远程-前提条件判断-车辆R挡-静止-无需授权-重试取消-主驾标定")  #正在
    # @pytest.mark.full
    # @pytest.mark.a11012
    # def test_caseid_1995898(self):
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Rvs)
    #     self.soa.get_gear_level(gear=Gear.Rvs)
    #     self.set_nopeople_incar()
    #     sleep(1)

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kScreen, isAlloweSkip=True)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.DriverSeat,text_id=50)
        
    #     sleep(2)      
    #     self.soa.set_Calibration_Retry(req=retry_req.kCancel)  
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kCheckPreconditionFailed)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle) 
        
        
    # @allure.title("前提条件判断-车辆N挡-静止-需要授权-重试取消-主驾标定")
    # @pytest.mark.full
    # @pytest.mark.a11011
    # def test_caseid_1995897(self):
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Neut)
    #     self.soa.get_gear_level(gear=Gear.Neut)
    #     self.set_nopeople_incar()

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        
    #     self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.DriverSeat,text_id=50)

    #     self.soa.set_Calibration_Retry(req=retry_req.kCancel)

    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kCheckPreconditionFailed)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
    # @allure.title("远程-前提条件判断-车辆D挡-静止-需要授权-重试条件满足-主驾标定")  #正在
    # @pytest.mark.full
    # @pytest.mark.a11011
    # def test_caseid_1995896(self):

    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Drv)
    #     self.soa.get_gear_level(gear=Gear.Drv)
    #     self.set_nopeople_incar()

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        
    #     self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.DriverSeat,text_id=50)

    #     # self.sd_tester.send_request_and_recv_response([0x2F, 0xDD, 0X0A ,0x03, 0x02],recv=[0x6F])
    #     self.bus_comm.set_gear_pos(gear=Gear.Park)
    #     self.soa.get_gear_level(gear=Gear.Park)

    #     sleep(1)
    #     self.soa.set_Calibration_Retry(req=retry_req.kRetry)
                
    #     # sleep(15)
    #     self.common_diag_communication()
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
      
        
    # @allure.title("前提条件判断-车辆N挡-静止-无需授权-重试条件满足-主驾标定")
    # @pytest.mark.full
    # @pytest.mark.a11012
    # def test_caseid_1995895(self):
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Neut)
    #     self.soa.get_gear_level(gear=Gear.Neut)
    #     self.set_nopeople_incar()
    #     sleep(1)

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kScreen, isAlloweSkip=True)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.DriverSeat,text_id=50)
      
    #     self.bus_comm.set_gear_pos(gear=Gear.Park)
    #     self.soa.get_gear_level(gear=Gear.Park)  
    #     sleep(1)      
        
    #     self.soa.set_Calibration_Retry(req=retry_req.kRetry) 
    #     sleep(11)
    #     self.common_diag_communication()
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
    # @allure.title(" 远程-前提条件判断-车辆D挡-静止-需要授权-重试条件还不满足-主驾标定")  #1104
    # @pytest.mark.full
    # @pytest.mark.a11011
    # def test_caseid_1995894(self):
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Drv)
    #     self.soa.get_gear_level(gear=Gear.Drv)
    #     self.set_nopeople_incar()

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        
    #     sleep(26)
    #     self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.DriverSeat,text_id=50)


    #     self.soa.set_Calibration_Retry(req=retry_req.kRetry)         
    #     # self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.DriverSeat,text_id=50)  
              
    #     sleep(6)        
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kCheckPreconditionFailed)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
       
       
       
        
    # @allure.title("远程-前提条件判断-车辆R挡-静止-无需授权-重试条件还不满足-主驾标定")
    # @pytest.mark.full
    # @pytest.mark.a11012
    # def test_caseid_1995893(self):

    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Rvs)
    #     self.soa.get_gear_level(gear=Gear.Rvs)
    #     self.set_nopeople_incar()
    #     sleep(1)

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kScreen, isAlloweSkip=True)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.DriverSeat,text_id=50)    
        
    #     self.soa.set_Calibration_Retry(req=retry_req.kRetry) 
    #     sleep(31)
       
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kCheckPreconditionFailed)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
    # @allure.title("远程-前提条件判断-车辆D挡-运动-需要授权-重试条件满足-主驾标定")
    # @pytest.mark.full
    # @pytest.mark.a11012
    # def test_caseid_1995892(self):
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Rvs)
    #     self.soa.get_gear_level(gear=Gear.Rvs)
    #     self.set_nopeople_incar()
    #     sleep(1)

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kScreen, isAlloweSkip=True)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.DriverSeat,text_id=50)    
        
    #     self.soa.set_Calibration_Retry(req=retry_req.kRetry) 
    #     sleep(31)
       
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kCheckPreconditionFailed)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
   
       
    @allure.title("屏幕-判断竞争任务-有低优先级诊断任务-主驾标定")
    @pytest.mark.sanity
    def test_caseid_1995905(self):
        self.io.bgm_diag_line_up()
        time.sleep(1)
        self.io.bgm_diag_line_down()
        time.sleep(1)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
         
 
       
    @allure.title("语音-判断竞争任务-有低优先级诊断任务-主驾标定")
    @pytest.mark.sanity
    @pytest.mark.a1104
    def test_caseid_1996196(self):
        self.io.bgm_diag_line_up()
        time.sleep(1)
        self.io.bgm_diag_line_down()
        time.sleep(3)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kVoicd, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
         
 
        
    @allure.title("远控-判断竞争任务-有低优先级诊断任务-主驾标定")
    @pytest.mark.sanity
    @pytest.mark.a1104
    def test_caseid_1996194(self):
        self.io.bgm_diag_line_up()
        time.sleep(1)
        self.io.bgm_diag_line_down()
        time.sleep(1)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
         
 
        
    @allure.title("远程-标定过程执行前，需等待10s-主驾标定")
    @pytest.mark.sanity
    @pytest.mark.a1113
    def test_caseid_1996081(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(5)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)

        sleep(6)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
 
################  开始副驾
  
    @allure.title("语音-授权请求-需授权-授权通过-副驾标定")   
    @pytest.mark.full
    @pytest.mark.a1106
    def test_caseid_1995850(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park, parklock=ParkLockSts.ParkEngd)
        self.soa.get_gear_level(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kVoicd, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
    @pytest.mark.full
    @pytest.mark.a1106
    def test_caseid_1995851(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kVoicd, isAlloweSkip=True)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)


        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
  
    @allure.title("语音-授权请求-无需授权-副驾标定")
    @pytest.mark.full
    @pytest.mark.a1106
    def test_caseid_1995851(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
    @allure.title("屏幕-授权请求-无需授权-副驾标定")
    @pytest.mark.full
    @pytest.mark.a1106
    def test_caseid_1995853(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kScreen, isAlloweSkip=True)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)


        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
    @allure.title("远程-授权请求-需授权-授权通过-副驾标定")
    @pytest.mark.sanity
    @pytest.mark.a1106
    def test_caseid_1995874(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
    @allure.title("远程-授权请求-无需授权-副驾标定")
    @pytest.mark.sanity
    @pytest.mark.a1106
    def test_caseid_1995875(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=True)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)


        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle) 
        
        
        
        
    @allure.title("远程-标定过程中取消-需要授权-副驾标定")
    @pytest.mark.full
    @pytest.mark.a1106
    def test_caseid_1995858(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        
        self.soa.set_auto_calibration(req=calibration_req.kOff,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)

        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kUserCancelRoutine)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
    @allure.title("远程-标定过程中取消-无需授权-副驾标定")
    @pytest.mark.full
    @pytest.mark.a1106
    def test_caseid_1995859(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=True)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)


        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        
        self.soa.set_auto_calibration(req=calibration_req.kOff,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)

        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kUserCancelRoutine)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
    @allure.title("远程-授权请求-需授权-取消授权-副驾标定")
    @pytest.mark.full
    @pytest.mark.a1106
    def test_caseid_1995873(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kCancelAuthorize)
       
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kAuthorizedFailed)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
    @allure.title("远程-授权请求-需授权-授权超时-副驾标定")
    @pytest.mark.full
    @pytest.mark.a1106
    def test_caseid_1995872(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        sleep(32)
       
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kAuthorizedTimeout)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
  
        
    @allure.title("屏幕-判断竞争任务-有高优先级诊断任务-需要授权-副驾标定")    #高优先级和授权，可能有问题  http://172.18.128.177:8080/2024_10_31_17_26_48
    @pytest.mark.full
    @pytest.mark.a11061
    def test_caseid_1995878(self):
        self.io.bgm_diag_line_up()
        sleep(1)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kHighPriorityRunning)
        # self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
    @allure.title("语音-判断竞争任务-有高优先级诊断任务-无需授权-副驾标定")   #http://172.18.128.177:8080/2024_10_31_17_35_34
    @pytest.mark.full
    @pytest.mark.a11061
    def test_caseid_1995877(self):
        self.io.bgm_diag_line_up()
        sleep(1)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kVoicd, isAlloweSkip=True)
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kHighPriorityRunning)

         
    # @allure.title("远程-前提条件判断-车辆N挡-静止-无需授权-超时无重试-副驾标定")  #1104
    # @pytest.mark.full
    # @pytest.mark.a1106
    # def test_caseid_1995871(self):
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Neut)
    #     self.soa.get_gear_level(gear=Gear.Neut)
    #     self.set_nopeople_incar()

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=True)
 
    #     sleep(31)
        
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kCheckPreconditionTimeout)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)      
        
        
        
    # @allure.title("远程-前提条件判断-车辆D挡-静止-需要授权-超时无重试-副驾标定")   #http://172.18.128.177:8080/2024_11_01_11_37_53  待跑
    # @pytest.mark.full
    # @pytest.mark.a1106
    # def test_caseid_1995870(self):   #http://172.18.128.177:8080/2024_11_01_15_34_15
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Drv)
    #     self.soa.get_gear_level(gear=Gear.Drv)
    #     self.set_nopeople_incar()

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        
    #     self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.PassengerSeat,text_id=51)


    #     sleep(31)

    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kCheckPreconditionTimeout)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
    # @allure.title("远程-前提条件判断-车辆R挡-静止-无需授权-重试取消-副驾标定")  #正在
    # @pytest.mark.full
    # @pytest.mark.a1106
    # def test_caseid_1995869(self):
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Rvs)
    #     self.soa.get_gear_level(gear=Gear.Rvs)
    #     self.set_nopeople_incar()
    #     sleep(1)

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kScreen, isAlloweSkip=True)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.PassengerSeat,text_id=51)
        
    #     sleep(2)      
    #     self.soa.set_Calibration_Retry(req=retry_req.kCancel)  
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kCheckPreconditionFailed)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle) 
        
        
    # @allure.title("前提条件判断-车辆N挡-静止-需要授权-重试取消-副驾标定")
    # @pytest.mark.full
    # @pytest.mark.a1106
    # def test_caseid_1995868(self):
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Neut)
    #     self.soa.get_gear_level(gear=Gear.Neut)
    #     self.set_nopeople_incar()

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        
    #     self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.PassengerSeat,text_id=51)

    #     self.soa.set_Calibration_Retry(req=retry_req.kCancel)

    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kCheckPreconditionFailed)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
    # @allure.title("远程-前提条件判断-车辆D挡-静止-需要授权-重试条件满足-副驾标定")  #正在
    # @pytest.mark.full
    # @pytest.mark.a1106
    # def test_caseid_1995867(self):

    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Drv)
    #     self.soa.get_gear_level(gear=Gear.Drv)
    #     self.set_nopeople_incar()

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        
    #     self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.PassengerSeat,text_id=51)

    #     # self.sd_tester.send_request_and_recv_response([0x2F, 0xDD, 0X0A ,0x03, 0x02],recv=[0x6F])
    #     self.bus_comm.set_gear_pos(gear=Gear.Park)
    #     self.soa.get_gear_level(gear=Gear.Park)

    #     sleep(1)
    #     self.soa.set_Calibration_Retry(req=retry_req.kRetry)
                
    #     # sleep(15)
    #     self.common_diag_communication_Passenger()
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
      
        
    # @allure.title("前提条件判断-车辆N挡-静止-无需授权-重试条件满足-副驾标定")
    # @pytest.mark.full
    # @pytest.mark.a1106
    # def test_caseid_1995866(self):
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Neut)
    #     self.soa.get_gear_level(gear=Gear.Neut)
    #     self.set_nopeople_incar()
    #     sleep(1)

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kScreen, isAlloweSkip=True)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.PassengerSeat,text_id=51)
      
    #     self.bus_comm.set_gear_pos(gear=Gear.Park)
    #     self.soa.get_gear_level(gear=Gear.Park)  
    #     sleep(1)      
        
    #     self.soa.set_Calibration_Retry(req=retry_req.kRetry) 
    #     sleep(11)
    #     self.common_diag_communication_Passenger()
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
    # @allure.title(" 远程-前提条件判断-车辆D挡-静止-需要授权-重试条件还不满足-副驾标定")  #1104
    # @pytest.mark.full
    # @pytest.mark.a1106
    # def test_caseid_1995865(self):
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Drv)
    #     self.soa.get_gear_level(gear=Gear.Drv)
    #     self.set_nopeople_incar()

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        
    #     sleep(26)
    #     self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.PassengerSeat,text_id=51)


    #     self.soa.set_Calibration_Retry(req=retry_req.kRetry)         
    #     # self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.PassengerSeat,text_id=51)  
              
    #     sleep(6)        
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kCheckPreconditionFailed)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
       
       
       
        
    # @allure.title("远程-前提条件判断-车辆R挡-静止-无需授权-重试条件还不满足-副驾标定")
    # @pytest.mark.full
    # @pytest.mark.a1106
    # def test_caseid_1995864(self):

    #     # self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Rvs)
    #     self.soa.get_gear_level(gear=Gear.Rvs)
    #     self.set_nopeople_incar()
    #     sleep(1)

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kScreen, isAlloweSkip=True)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.PassengerSeat,text_id=51)    
        
    #     self.soa.set_Calibration_Retry(req=retry_req.kRetry) 
    #     sleep(31)
       
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kCheckPreconditionFailed)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
    # @allure.title("远程-前提条件判断-车辆D挡-运动-需要授权-重试条件满足-副驾标定")
    # @pytest.mark.full
    # @pytest.mark.a1106
    # def test_caseid_1995863(self):
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Rvs)
    #     self.soa.get_gear_level(gear=Gear.Rvs)
    #     self.set_nopeople_incar()
    #     sleep(1)

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kScreen, isAlloweSkip=True)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.PassengerSeat,text_id=51)    
        
    #     self.soa.set_Calibration_Retry(req=retry_req.kRetry) 
    #     sleep(31)
       
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kCheckPreconditionFailed)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
   
       
    @allure.title("屏幕-判断竞争任务-有低优先级诊断任务-副驾标定")
    @pytest.mark.sanity
    @pytest.mark.a1106
    def test_caseid_1995876(self):
        self.io.bgm_diag_line_up()
        time.sleep(1)
        self.io.bgm_diag_line_down()
        time.sleep(1)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
         
 
       
    @allure.title("语音-判断竞争任务-有低优先级诊断任务-副驾标定")
    @pytest.mark.sanity
    @pytest.mark.a1106
    def test_caseid_1996193(self):
        self.io.bgm_diag_line_up()
        time.sleep(1)
        self.io.bgm_diag_line_down()
        time.sleep(3)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kVoicd, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
         
 
        
    @allure.title("远控-判断竞争任务-有低优先级诊断任务-副驾标定")
    @pytest.mark.sanity
    @pytest.mark.a1106
    def test_caseid_1996191(self):
        self.io.bgm_diag_line_up()
        time.sleep(1)
        self.io.bgm_diag_line_down()
        time.sleep(1)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
         
 
        
    @allure.title("远程-标定过程执行前，需等待10s-副驾标定")
    @pytest.mark.sanity
    @pytest.mark.a1113
    def test_caseid_1996068(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(5)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)

        sleep(6)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
   

###############################################  副驾标定 ################################################################
  
        
  
    @allure.title("屏幕-授权请求-需授权-授权通过-副驾标定")
    @pytest.mark.full
    @pytest.mark.a1106
    def test_caseid_1995852(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kScreen, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
      
    @allure.title("远程-标定过程中失败（Zero-Position Calibration StartRoutine失败得到NRC，retry失败）-需要授权-副驾")
    @pytest.mark.sanity
    @pytest.mark.a1106
    def test_caseid_1996080(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x7F, 0x31,0x12])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x7F, 0x31,0x12])
        
        self.common_diag_communication_Passenger()
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x7F, 0x31,0x22])

        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kRoutineFailed)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
          
          
        
    @allure.title("远程-标定过程中成功（Zero-Position Calibration StartRoutine失败得到NRC后，retry成功）-需要授权-副驾标定")
    @pytest.mark.sanity
    @pytest.mark.a1106
    def test_caseid_1996079(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x7F, 0x31,0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x7F, 0x31,0x22])
        
        self.common_diag_communication_Passenger()
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
    @allure.title("远程-标定过程中失败（Zero-Position Calibration StartRoutine失败，retry失败）-需要授权-副驾标定")
    @pytest.mark.sanity
    @pytest.mark.a1106
    def test_caseid_1996078(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0X71,0X01,0x20, 0x97, 0x20])
        
        # self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
        #                                                    check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0X71,0X01,0x20, 0x97, 0x20])
        self.common_diag_communication_Passenger()
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x7F, 0x31,0x22])

        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kRoutineFailed)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
          

        
    @allure.title("远程-标定过程中成功（Zero-Position Calibration StartRoutine得到响应码22后，retry成功）-需要授权-副驾标定")
    @pytest.mark.sanity
    @pytest.mark.a1106
    def test_caseid_1996077(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0X71,0X01,0x20, 0x97, 0x20])
        
        # self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
        #                                                    check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0X71,0X01,0x20, 0x97, 0x20])
        
        self.common_diag_communication_Passenger()
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
    @allure.title("远程-标定过程中成功（On-Demand Self-Test StartRoutine失败后，retry成功）-需要授权-副驾标定")
    @pytest.mark.sanity
    @pytest.mark.a1106
    def test_caseid_1996076(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x7F, 0x31, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x7F, 0x31, 0x22])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0X71,0X01,0x02, 0x0A,0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
    @allure.title("远程-标定31 03 20 97，收到NRC继续请求；再次得到21跳出loop，执行读取故障码后retry Zero-Position Calibration StartRoutine-需要授权-副驾标定")
    @pytest.mark.sanity
    @pytest.mark.a1106
    def test_caseid_1996074(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x7F, 0x31,0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x7F, 0x31,0x22])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x21])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X19,0X02,0x2F],send_resp_data=[0x59])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X22,0XFD,0x08],send_resp_data=[0x62, 0xFD,0x08])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
    @allure.title("远程-标定31 03 20 97，收到21跳出loop，执行读取故障码后retry Zero-Position Calibration StartRoutine-需要授权-副驾标定")
    @pytest.mark.sanity
    @pytest.mark.a1106
    def test_caseid_1996072(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x21])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X19,0X02,0x2F],send_resp_data=[0x59])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X22,0XFD,0x08],send_resp_data=[0x62, 0xFD,0x08])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
    @allure.title("远程-标定31 03 02 0A，收到NRC继续请求；再次得到21跳出loop，执行读取故障码后retry On-Demand Self-Test StartRoutine-需要授权-副驾标定") 
    @pytest.mark.sanity
    @pytest.mark.a1106
    def test_caseid_1996071(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x7F, 0x31,0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x7F, 0x31,0x22])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0X71,0X03,0x02, 0x0A, 0x21])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X19,0X02,0x2F],send_resp_data=[0x59])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X22,0XFD,0x08],send_resp_data=[0x62, 0xFD,0x08])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
    @allure.title("远程-标定31 03 02 0A，收到21跳出loop，执行读取故障码后retry On-Demand Self-Test StartRoutine-需要授权-副驾标定")
    @pytest.mark.sanity
    @pytest.mark.a1106
    def test_caseid_1996069(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x21])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X19,0X02,0x2F],send_resp_data=[0x59])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X22,0XFD,0x08],send_resp_data=[0x62, 0xFD,0x08])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
    @allure.title("远程-标定31 03 02 0A，收到NRC继续请求；再次得到21跳出loop，执行读取故障码后retry On-Demand Self-Test StartRoutine-需要授权-副驾标定")
    @pytest.mark.sanity
    @pytest.mark.a1106
    def test_caseid_1996071(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x22])
        

        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0X71,0X03,0x02, 0x0A, 0x21])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X19,0X02,0x2F],send_resp_data=[0x59])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X22,0XFD,0x08],send_resp_data=[0x62, 0xFD,0x08])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
        
    @allure.title("远程-标定过程中成功（On-Demand Self-Test StartRoutine失败后，retry失败）-需要授权-副驾标定")
    @pytest.mark.sanity
    @pytest.mark.a1106
    def test_caseid_1996075(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x7F, 0x31,0x12])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x7F, 0x31,0x12]) 
        
 
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x7F, 0x31,0x22])    
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x7F, 0x31,0x22])
              
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kRoutineFailed)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
        
    # @allure.title("远程-前提条件判断-车辆D挡-静止-需要授权-重试条件满足-副驾标定")
    # @pytest.mark.full
    # @pytest.mark.a1106
    # def test_caseid_1995867(self):

    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Drv)
    #     self.soa.get_gear_level(gear=Gear.Drv)
    #     self.set_nopeople_incar()

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
    #     self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.PassengerSeat,text_id=51)

    #     # self.sd_tester.send_request_and_recv_response([0x2F, 0xDD, 0X0A ,0x03, 0x02],recv=[0x6F])
    #     self.bus_comm.set_gear_pos(gear=Gear.Park)
    #     self.soa.get_gear_level(gear=Gear.Park)
    #     sleep(1)
    #     self.soa.set_Calibration_Retry(req=retry_req.kRetry)

        
    #     sleep(11)
    #     self.common_diag_communication_Passenger()
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        


        
        
    # @allure.title("远程-前提条件判断-车辆R挡-运动-需要授权-重试条件满足-副驾标定")
    # @pytest.mark.full
    # @pytest.mark.a1106
    # def test_caseid_1995862(self):

    #     self.bus_comm.set_vehmtn(VehMtnSts.BackwVal1)
    #     self.bus_comm.set_gear_pos(gear=Gear.Drv)
    #     self.soa.get_gear_level(gear=Gear.Drv)
    #     self.set_nopeople_incar()

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
    #     self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.PassengerSeat,text_id=51)

    #     # self.sd_tester.send_request_and_recv_response([0x2F, 0xDD, 0X0A ,0x03, 0x02],recv=[0x6F])
    #     self.bus_comm.set_gear_pos(gear=Gear.Park)
    #     self.soa.get_gear_level(gear=Gear.Park)
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
    #     self.soa.set_Calibration_Retry(req=retry_req.kRetry)
        
    #     sleep(11)
    #     self.common_diag_communication_Passenger()
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
    # @allure.title("远程-前提条件判断-车辆N挡-运动-无需授权-重试条件满足-副驾标定")
    # @pytest.mark.full
    # @pytest.mark.a1106
    # def test_caseid_1995861(self):
    #     self.bus_comm.set_vehmtn(VehMtnSts.FwdVal1)
    #     self.bus_comm.set_gear_pos(gear=Gear.Neut)
    #     self.soa.get_gear_level(gear=Gear.Neut)
    #     self.set_nopeople_incar()

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=True)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.PassengerSeat,text_id=51)


    #     self.bus_comm.set_gear_pos(gear=Gear.Park)
    #     self.soa.get_gear_level(gear=Gear.Park)
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.soa.set_Calibration_Retry(req=retry_req.kRetry)
        
    #     sleep(11)
    #     self.common_diag_communication_Passenger()
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        

       
    # @allure.title("远程-副驾座椅标定-前提条件判断-车辆P档静止-副驾座椅占位-副驾标定")
    # @pytest.mark.full
    # @pytest.mark.a1106
    # def test_caseid_1995860(self):
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Park)
    #     self.soa.get_gear_level(gear=Gear.Park)
    #     self.set_nopeople_incar()
    #     self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04", 'BltLockStAtPassBltLockSt1', 1) 
    #     self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04", 'PassSeatSts', 1)                           

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=True)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.PassengerSeat,text_id=51)

    #     sleep(31)
        
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kCheckPreconditionTimeout)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
    # @allure.title("远程-标定过程中5分钟超时-无需授权-副驾标定")   用例删除
    # @pytest.mark.full
    # @pytest.mark.a1106
    # def test_caseid_1995857(self):
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Park)
    #     self.set_nopeople_incar()

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=True)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)


    #     sleep(11)
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0x10, 0x03],send_resp_data=[0x7F, 0x10, 0x22])
    #     sleep(60*5)
        
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kRoutingTimeout)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)      
        
        
        
    # @allure.title("远程-标定31 03 20 97，收到22继续请求；超时跳出loop，执行读取故障码后retry Zero-Position Calibration StartRoutine-需要授权-副驾标定")
    # @pytest.mark.full
    # @pytest.mark.a1106
    # def test_caseid_1996073(self):   #半自动化用
    #     count = 0
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Park)
    #     self.set_nopeople_incar()

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
    #     self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

    #     sleep(11)
    #     self.common_diag_communication_Passenger()
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x22])
        
    #     while (count < 53):
    #             sleep(1)
    #             self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x22])
    #             count = count + 1        
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x22])
        
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X19,0X02,0x2F],send_resp_data=[0x59])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X22,0XFD,0x08],send_resp_data=[0x62, 0xFD,0x08])  
        
           
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
       
    @allure.title("远控-判断竞争任务-有高优先级诊断任务-无需授权(不需要判断优先级)-主驾标定")
    @pytest.mark.full
    @pytest.mark.a1107 
    def test_caseid_1996195(self):
        self.io.bgm_diag_line_up()
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=True)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)


        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)     
 
 
        
       
    @allure.title("远控-判断竞争任务-有高优先级诊断任务-无需授权(不需要判断优先级)-副驾标定")
    @pytest.mark.full
    @pytest.mark.a1107 
    def test_caseid_1996192(self):
        self.io.bgm_diag_line_up()
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=True)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)


        sleep(11)
        self.common_diag_communication_Passenger()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)     
 
 
 #########################################  补漏的
 
#####处理主驾


        
    @allure.title("远程-标定过程中成功（Zero-Position Calibration StartRoutine失败后，retry成功）-需要授权-主驾标定")
    @pytest.mark.full
    @pytest.mark.a1107
    def test_caseid_1996090(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0X71,0X01,0x20, 0x97, 0x20])
        
        # self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
        #                                                    check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0X71,0X01,0x20, 0x97, 0x20])
        
        self.common_diag_communication()
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
                

        
    @allure.title("远程-标定31 03 02 0A，收到21跳出loop，执行读取故障码后retry On-Demand Self-Test StartRoutine-需要授权-主驾标定")
    @pytest.mark.full
    @pytest.mark.a1107
    def test_caseid_1996082(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x21])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X19,0X02,0x2F],send_resp_data=[0x59])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X22,0XFD,0x08],send_resp_data=[0x62, 0xFD,0x08])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
 
        
    # @allure.title("远程-前提条件判断-车辆R挡-运动-需要授权-重试条件满足-主驾标定")
    # @pytest.mark.full
    # @pytest.mark.a21107
    # def test_caseid_1995891(self):

    #     self.bus_comm.set_vehmtn(VehMtnSts.BackwVal1)
    #     self.bus_comm.set_gear_pos(gear=Gear.Drv)
    #     self.soa.get_gear_level(gear=Gear.Drv)
    #     self.set_nopeople_incar()

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
    #     self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.DriverSeat,text_id=50)

    #     # self.sd_tester.send_request_and_recv_response([0x2F, 0xDD, 0X0A ,0x03, 0x02],recv=[0x6F])
    #     self.bus_comm.set_gear_pos(gear=Gear.Park)
    #     self.soa.get_gear_level(gear=Gear.Park)
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
    #     self.soa.set_Calibration_Retry(req=retry_req.kRetry)
        
    #     sleep(11)
    #     self.common_diag_communication()
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
                
 
        
    # @allure.title("远程-前提条件判断-车辆N挡-运动-无需授权-重试条件满足-主驾标定")
    # @pytest.mark.full
    # @pytest.mark.a21107
    # def test_caseid_1995890(self):
    #     self.bus_comm.set_vehmtn(VehMtnSts.FwdVal1)
    #     self.bus_comm.set_gear_pos(gear=Gear.Neut)
    #     self.soa.get_gear_level(gear=Gear.Neut)
    #     self.set_nopeople_incar()

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=True)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.DriverSeat,text_id=50)


    #     self.bus_comm.set_gear_pos(gear=Gear.Park)
    #     self.soa.get_gear_level(gear=Gear.Park)
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.soa.set_Calibration_Retry(req=retry_req.kRetry)
        
    #     sleep(11)
    #     self.common_diag_communication()
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
       
    # @allure.title("远程-主驾座椅标定-前提条件判断-车辆P档静止-主驾座椅占位-主驾标定")
    # @pytest.mark.full
    # @pytest.mark.a1107
    # def test_caseid_1995889(self):
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Park)
    #     self.soa.get_gear_level(gear=Gear.Park)
    #     self.set_nopeople_incar()
    #     self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)


    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=True)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,functionID=CalibrationFunctionID.DriverSeat,text_id=50)

    #     sleep(31)
        
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kCheckPreconditionTimeout)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
         
       
        
    # @allure.title("远程-标定过程中5分钟超时-无需授权-主驾标定")  用例删除
    # @pytest.mark.full
    # @pytest.mark.a1107
    # def test_caseid_11995886(self):
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Park)
    #     self.soa.get_gear_level(gear=Gear.Park)
    #     self.set_nopeople_incar()

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=True)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)


    #     sleep(11)
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0x10, 0x03],send_resp_data=[0x7F, 0x10, 0x22])
    #     sleep(60*5)
        
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kRoutingTimeout)
    #     self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)      
          
 
        
    @allure.title("远程-标定31 03 02 0A，收到NRC继续请求；再次得到21跳出loop，执行读取故障码后retry On-Demand Self-Test StartRoutine-需要授权-主驾标定") 
    @pytest.mark.full
    @pytest.mark.a1107
    def test_caseid_1996083(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
        # self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x22])
        

        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0X71,0X03,0x02, 0x0A, 0x21])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X19,0X02,0x2F],send_resp_data=[0x59])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X22,0XFD,0x08],send_resp_data=[0x62, 0xFD,0x08])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
    
        
        
    @allure.title("远程-标定31 03 02 0A，收到NRC继续请求；再次得到21跳出loop，执行读取故障码后retry On-Demand Self-Test StartRoutine-需要授权-主驾标定") 
    @pytest.mark.full
    @pytest.mark.a1107
    def test_caseid_1996084(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x7F, 0x31,0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x7F, 0x31,0x22])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0X71,0X03,0x02, 0x0A, 0x21])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X19,0X02,0x2F],send_resp_data=[0x59])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X22,0XFD,0x08],send_resp_data=[0x62, 0xFD,0x08])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
                
        
    @allure.title("远程-标定31 03 20 97，收到21跳出loop，执行读取故障码后retry Zero-Position Calibration StartRoutine-需要授权-主驾标定")
    @pytest.mark.full
    @pytest.mark.a1107
    def test_caseid_1996085(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x21])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X19,0X02,0x2F],send_resp_data=[0x59])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X22,0XFD,0x08],send_resp_data=[0x62, 0xFD,0x08])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
            
        
    @allure.title("远程-标定31 03 02 0A，收到NRC继续请求；再次得到21跳出loop，执行读取故障码后retry On-Demand Self-Test StartRoutine-需要授权-主驾标定") 
    @pytest.mark.full
    @pytest.mark.a1107
    def test_caseid_1996084(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x7F, 0x31,0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x7F, 0x31,0x22])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0X71,0X03,0x02, 0x0A, 0x21])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X19,0X02,0x2F],send_resp_data=[0x59])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X22,0XFD,0x08],send_resp_data=[0x62, 0xFD,0x08])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
   
        
    # @allure.title("远程-标定31 03 20 97，收到22继续请求；超时跳出loop，执行读取故障码后retry Zero-Position Calibration StartRoutine-需要授权-主驾标定")
    # @pytest.mark.full       #半自动化用    测50s超时，counter大于50，结果就是ok的    先注释，测试时候打开
    # @pytest.mark.a11107
    # def test_caseid_1996086(self):
    #     count = 0
    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Park)
    #     self.soa.get_gear_level(gear=Gear.Park)
    #     self.set_nopeople_incar()

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
    #     self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

    #     sleep(11)
    #     self.common_diag_communication()
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x22])
        
    #     while (count < 53):
    #             sleep(1)
    #             self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x22])
    #             count = count + 1        
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #                                                        check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x22])
        
        # self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
        #                                                    check_req_data=[0X19,0X02,0x2F],send_resp_data=[0x59])
        # self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
        #                                                    check_req_data=[0X22,0XFD,0x08],send_resp_data=[0x62, 0xFD,0x08])  
        
           
        # self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
        #                                                    check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        # self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
        #                                                    check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        # self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
        #                                                    check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        # self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
        #                                                    check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        # self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
        #                                                    check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        # self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kRoutingTimeout)
        # # self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.DriverSeat, status=calibration_status.kCalibrationFailed)
        
   
 
   
  
        
    @allure.title("远程-标定31 03 20 97，收到NRC继续请求；再次得到21跳出loop，执行读取故障码后retry Zero-Position Calibration StartRoutine-需要授权-主驾标定")
    @pytest.mark.full
    @pytest.mark.a1107
    def test_caseid_1996087(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x7F, 0x31,0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x7F, 0x31,0x22])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x21])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X19,0X02,0x2F],send_resp_data=[0x59])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X22,0XFD,0x08],send_resp_data=[0x62, 0xFD,0x08])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
    @allure.title("远程-标定过程中成功（On-Demand Self-Test StartRoutine失败后，retry失败）-需要授权-主驾标定")
    @pytest.mark.full
    @pytest.mark.a1107
    def test_caseid_1996088(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x7F, 0x31,0x12])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x7F, 0x31,0x12]) 
        
 
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x7F, 0x31,0x22])    
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x7F, 0x31,0x22])
              
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kRoutineFailed)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
    @allure.title("远程-标定过程中成功（On-Demand Self-Test StartRoutine失败后，retry成功）-需要授权-主驾标定")
    @pytest.mark.full
    @pytest.mark.a1107
    def test_caseid_1996089(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.get_gear_level(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x7F, 0x31, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x7F, 0x31, 0x22])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0X71,0X01,0x02, 0x0A,0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
                    
            
    # @allure.title("远程-标定31 03 02 0A，收到22继续请求；超时跳出loop，执行读取故障码后retry On-Demand Self-Test StartRoutine-需要授权-副驾标定")
    # @pytest.mark.full       #半自动化用    测30s超时，counter大于30，结果就是ok的    先注释，测试时候打开
    # @pytest.mark.a11107
    # def test_caseid_1996070(self):
    #     count = 0

    #     self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
    #     self.bus_comm.set_gear_pos(gear=Gear.Park)
    #     self.soa.get_gear_level(gear=Gear.Park)
    #     self.set_nopeople_incar()

    #     self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.PassengerSeat,source=SourceType.kRemote, isAlloweSkip=False)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.PassengerSeat)
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.PassengerSeat)
    #     self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

    #     sleep(11)
    #     self.common_diag_communication_Passenger()
    #     self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.PassengerSeat)  
              
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x22])
        
    #     while (count < 29):
    #             sleep(1)
    #             self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x22])
    #             count = count + 1        
    #     self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
    #                                                        check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x22])
        
    #     # self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
    #     #                                                    check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
    #     self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.PassengerSeat, errorCode=calibration_error_code.kRoutingTimeout)
    #     # self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.PassengerSeat, status=calibration_status.kRoutingTimeout)
        
         
################ 1128 
        
    @allure.title("远程-标定过程中失败（Zero-Position Calibration StartRoutine失败，retry失败）-需要授权-主驾标定")
    @pytest.mark.sanity
    @pytest.mark.a1128
    def test_caseid_1996091(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0X71,0X01,0x20, 0x97, 0x20])
        
        # self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x728,resp_id=0x628,
        #                                                    check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0X71,0X01,0x20, 0x97, 0x20])
        self.common_diag_communication()
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x7F, 0x31,0x22])

        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kRoutineFailed)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
          
     
    @allure.title("远程-标定过程中失败（Zero-Position Calibration StartRoutine失败得到NRC，retry失败）-需要授权-主驾")
    @pytest.mark.sanity    #1996093
    @pytest.mark.a1128
    def test_caseid_1996093(self):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x7F, 0x31,0x12])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x7F, 0x31,0x12])
        
        self.common_diag_communication()
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x7F, 0x31,0x22])

        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kRoutineFailed)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
          
        
    @allure.title("远程-标定过程中成功（Zero-Position Calibration StartRoutine失败得到NRC后，retry成功）-需要授权-主驾标定")
    @pytest.mark.sanity
    @pytest.mark.a1128
    def test_caseid_1996092(self):      #1996092
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.set_nopeople_incar()

        self.soa.set_auto_calibration(req=calibration_req.KOn,functionID=CalibrationFunctionID.DriverSeat,source=SourceType.kRemote, isAlloweSkip=False)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,functionID=CalibrationFunctionID.DriverSeat)
        self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)

        sleep(11)
        self.common_diag_communication()
        self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,functionID=CalibrationFunctionID.DriverSeat)  
              
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x7F, 0x31,0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x7F, 0x31,0x22])
        
        self.common_diag_communication()
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x20, 0x97],send_resp_data=[0x71, 0x01,0x20, 0x97, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x20, 0x97],send_resp_data=[0x71, 0x03,0x20, 0x97, 0x20])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X01,0x02, 0x0A],send_resp_data=[0x71, 0x01,0x02, 0x0A, 0x22])
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X31,0X03,0x02, 0x0A],send_resp_data=[0x71, 0x03,0x02, 0x0A, 0x20])
        
        self.bus_comm.check_can_lin_diag_req_and_send_resp(bus_name=BusName.bodycan,req_id=0x727,resp_id=0x627,
                                                           check_req_data=[0X10,0X01],send_resp_data=[0x50, 0x01,0x00, 0x31, 0x01, 0xF4])
        
        self.soa.event_check_Calibration_Result_Info(functionID=CalibrationFunctionID.DriverSeat, errorCode=calibration_error_code.kSuccess)
        self.soa.event_check_Calibration_Status_Info(functionID=CalibrationFunctionID.InvalidValue, status=calibration_status.kIdle)
        
        
        
          
                
        