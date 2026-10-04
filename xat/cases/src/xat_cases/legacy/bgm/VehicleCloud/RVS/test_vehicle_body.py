#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_rvs.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/12/1 11:30
@Description: BGM RVS功能测试
"""

import os
import sys
import pytest
import allure
from time import sleep
import threading
import math

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.tsp.rvs_client import RvsClient
from signal_value_mapping import *
running_flag = False

@allure.feature("BGM车云")
@allure.story("基础数据上报")
@pytest.mark.order_last
class TestRVS(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["ClimateControlService_client","CentralLockService_client","TailWingService_client","SteerWheelService_client","TyreService_client","ChargeLidService_client","OuterRearViewService_client","ShieldWindowService_client","VehicleModeService_client","VehicleSetStatusService_client"])
        self.vid = self.tb_config["vid"]
        self.rvs_client = RvsClient(vid=self.vid)
        logger.info("VID: {0}".format(self.vid))
        sleep(2)

    def before_each_func(self, ecu):
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_extral_light_button_to_defaul_sts()

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        global running_flag
        running_flag = False
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        self.sd_tester.write_ccp({225: 7, 226: 7}) 
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    
    def pre_conditon_for_tire(self):
        self.sd_tester.write_ccp(ccp={225: 4, 226: 4})
        self.bus_comm.set_Hv_sys_relay_sts(HvSysRelaySts.Close)
        self.bus_comm.pause_bus_send_tpms()
        self.tire_sensor_dic = self.bus_comm.tire_sensor_ini()
        self.rolling_counter = 0
        running_flag = True
        self.start_send_tire_data()
        sleep(2)
        self.tire_sensor_dic["FrontLeft"]["send_rf"] = True
        self.tire_sensor_dic["FrontRight"]["send_rf"] = True
        self.tire_sensor_dic["RearRight"]["send_rf"] = True
        self.tire_sensor_dic["RearLeft"]["send_rf"] = True
        self.sd_tester.write_sensor_id(
            [0x11, 0x11, 0x11, 0x11, 0x02, 0x62, 0x86, 0x43, 0x02, 0x62, 0x84, 0xF4, 0x22, 0x22, 0x22, 0x22])
        time.sleep(3)
        self.bus_comm.set_dtc_pre()
        time.sleep(1)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_vehspd_and_qf(vehspd=37.0)
        time.sleep(1)

    def set_pre_condition_for_keep_power(self):
        self.bus_comm.set_vehmtn()
        self.bus_comm.set_vehspd()
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr18", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        time.sleep(1)
        self.bus_comm.set_dtc_pre()
        self.bus_comm.set_batterylow_mode(DCChrgnHndlSts=DCChrgnHndlSts.Disconnected, DispHvBattLvlOfChrg=80.0)
        self.bus_comm.set_singal(bus="propulsioncan", msg="EcmPropComFr10", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        sleep(1)
    
    def after_tire_func(self):
        global running_flag
        try:
            running_flag = False
            self.bus_comm.resume_all_bus_send()
            self.stop_send_tire_data()
            self.sd_tester.write_sensor_id(
                [0x11, 0x11, 0x11, 0x11, 0x02, 0x62, 0x86, 0x43, 0x02, 0x62, 0x84, 0xF4, 0x22, 0x22, 0x22, 0x22])
            self.bus_comm.set_vehspd_gear(vehspd=0.0)
        except Exception as e:
            running_flag = False
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    def generate_and_send_rf_data(self, pos):
        """
        发送胎压数据
        :param pos: FrontLeft：左前；FrontRight：右前；RearRight：右后；RearLeft左后
        :return:
        """
        global running_flag
        st = time.time()
        running_flag = True
        while running_flag:
            logger.info(f"------->开始胎压报文发送")
            sensor = self.tire_sensor_dic[pos]
            while time.time() - st < sensor["cycle_time"]:
                time.sleep(0.1)
            if sensor["send_rf"]:
                for _ in range(sensor["counter_per_pkg"]):
                    rf_data = sensor["tire_id"] + [math.ceil(sensor["pressure"] / 1.373), int(sensor["temp"] + 50),
                                                   sensor["acc"], sensor["factory"], sensor["function"]]
                    self.bus_comm.send_tpms_rf_data(rf_data, self.rolling_counter)
                    self.rolling_counter = (self.rolling_counter + 1) & 0xFF
                    sleep(0.12)
            st = time.time()


    def start_send_tire_data(self, tire_dic: list = ["FrontLeft", "FrontRight", "RearRight", "RearLeft"]):
        """
        启动进程发送胎压数据报文
        :param tire_dic: 需要发送的胎压数据列表
        :return:
        """
        global running_flag
        logger.info(f"------->开始胎压报文发送")
        for key in tire_dic:
            send_data_thread = threading.Thread(target=self.generate_and_send_rf_data, args=(key,),name="start_function")
            send_data_thread.start()
            sleep(.5)


    def stop_send_tire_data(self):
        """
        停止胎压报文发送
        :return:
        """
        global running_flag
        running_flag = False
    
    def after_func_about_tire(self):
        try:
            self.sd_tester.write_sensor_id(
                [0x11, 0x11, 0x11, 0x11, 0x02, 0x62, 0x86, 0x43, 0x02, 0x62, 0x84, 0xF4, 0x22, 0x22, 0x22, 0x22])
            self.bus_comm.set_vehspd_gear(vehspd=0.0)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass


    

    @pytest.mark.smoke
    def test_Drvrdoor_status_caseid_112842_118693(self):
        Drvrdoor_status = {
            "DoorStatusNA": DoorOpenerSts.Ukwn,
            "DoorStatusClosed": DoorOpenerSts.FullClsd,
            "DoorStatusOpened": DoorOpenerSts.FullOpend,
            "UNKNOWN_ENUM_VALUE_DoorStatus_10": DoorOpenerSts.HalfClsd,
            "UNKNOWN_ENUM_VALUE_DoorStatus_8": DoorOpenerSts.MovgInBrkg,
            "UNKNOWN_ENUM_VALUE_DoorStatus_9": DoorOpenerSts.MovgOutBrkg,
            "DoorStatusOpening": DoorOpenerSts.MovgOut,
            "DoorStatusClosing": DoorOpenerSts.MovgIn,
            "DoorStatusHover": DoorOpenerSts.StopDurgOpen,
            "DoorStatusHover": DoorOpenerSts.StopDurgCls,
        }
        self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorOpenerDrvrSts",1)
        self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorDrvrPosn",0)
        self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorDrvrPercPosn",0)
        for key in Drvrdoor_status:
            self.bus_comm.set_door_opener_sts(drv_opener=Drvrdoor_status[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.VehicleBody, keys=["doors", "id==0","status"], target_value=getattr(DoorStatusRvs, key).value)


    @pytest.mark.smoke
    def test_Passdoor_status_caseid_112841_118692(self):
        Passdoor_status = {
            "DoorStatusNA": DoorOpenerSts.Ukwn,
            "DoorStatusClosed": DoorOpenerSts.FullClsd,
            "DoorStatusOpened": DoorOpenerSts.FullOpend,
            "UNKNOWN_ENUM_VALUE_DoorStatus_10": DoorOpenerSts.HalfClsd,
            "UNKNOWN_ENUM_VALUE_DoorStatus_8": DoorOpenerSts.MovgInBrkg,
            "UNKNOWN_ENUM_VALUE_DoorStatus_9": DoorOpenerSts.MovgOutBrkg,
            "DoorStatusOpening": DoorOpenerSts.MovgOut,
            "DoorStatusClosing": DoorOpenerSts.MovgIn,
            "DoorStatusHover": DoorOpenerSts.StopDurgOpen,
            "DoorStatusHover": DoorOpenerSts.StopDurgCls,
        }
        self.bus_comm.set_singal("bodycan","PpodBodyFr01","DoorPassPosn",0)
        self.bus_comm.set_singal("bodycan","PpodBodyFr01","DoorPassPercPosn",0)
        self.bus_comm.set_singal("bodycan","PpodBodyFr01","DoorOpenerPassSts",1)
        for key in Passdoor_status:
            self.bus_comm.set_door_opener_sts(pass_opener=Passdoor_status[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.VehicleBody, keys=["doors","id==1", "status"], target_value=getattr(DoorStatusRvs, key).value)

    @pytest.mark.smoke
    def test_LeRedoor_status_caseid_112840_118691(self):
        LeRedoor_status = {
            "DoorStatusNA": DoorOpenerSts.Ukwn,
            "DoorStatusClosed": DoorOpenerSts.FullClsd,
            "DoorStatusOpened": DoorOpenerSts.FullOpend,
            "UNKNOWN_ENUM_VALUE_DoorStatus_10": DoorOpenerSts.HalfClsd,
            "UNKNOWN_ENUM_VALUE_DoorStatus_8": DoorOpenerSts.MovgInBrkg,
            "UNKNOWN_ENUM_VALUE_DoorStatus_9": DoorOpenerSts.MovgOutBrkg,
            "DoorStatusOpening": DoorOpenerSts.MovgOut,
            "DoorStatusClosing": DoorOpenerSts.MovgIn,
            "DoorStatusHover": DoorOpenerSts.StopDurgOpen,
            "DoorStatusHover": DoorOpenerSts.StopDurgCls,
        }
        self.bus_comm.set_singal("bodycan","LpodBodyFr01","DoorLeRePosn",0)
        self.bus_comm.set_singal("bodycan","LpodBodyFr01","DoorLeRePercPosn",0)
        self.bus_comm.set_singal("bodycan","LpodBodyFr01","DoorOpenerLeReSts",1)
        sleep(1)
        for key in LeRedoor_status:
            self.bus_comm.set_door_opener_sts(lere_opener=LeRedoor_status[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.VehicleBody, keys=["doors","id==2", "status"], target_value=getattr(DoorStatusRvs, key).value)

    @pytest.mark.smoke
    def test_RiRedoor_status_caseid_112839_118690(self):
        RiRedoor_status = {
            "DoorStatusNA": DoorOpenerSts.Ukwn,
            "DoorStatusClosed": DoorOpenerSts.FullClsd,
            "DoorStatusOpened": DoorOpenerSts.FullOpend,
            # "UNKNOWN_ENUM_VALUE_DoorStatus_10": DoorOpenerSts.HalfClsd,
            # "UNKNOWN_ENUM_VALUE_DoorStatus_8": DoorOpenerSts.MovgInBrkg,
            # "UNKNOWN_ENUM_VALUE_DoorStatus_9": DoorOpenerSts.MovgOutBrkg,
            "DoorStatusOpening": DoorOpenerSts.MovgOut,
            "DoorStatusClosing": DoorOpenerSts.MovgIn,
            "DoorStatusHover": DoorOpenerSts.StopDurgOpen,
            "DoorStatusHover": DoorOpenerSts.StopDurgCls,
        }
        self.bus_comm.set_singal("bodycan","RpodBodyFr01","DoorRiRePosn",0)
        self.bus_comm.set_singal("bodycan","RpodBodyFr01","DoorRiRePercPosn",0)
        self.bus_comm.set_singal("bodycan","RpodBodyFr01","DoorOpenerRiReSts",1)
        for key in RiRedoor_status:
            self.bus_comm.set_door_opener_sts(rire_opener=RiRedoor_status[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.VehicleBody, keys=["doors","id==3", "status"], target_value=getattr(DoorStatusRvs, key).value)
    @pytest.mark.smoke
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1350997?projectId=46',
        name='RVS Case 112336',
    )
    def test_tailgate_status_caseid_112336_118689(self):
        tailgate_status = {
            "TgsOpened" :DoorOpenerSts.FullOpend,
            "TgsClosing":DoorOpenerSts.MovgIn,
            "TgsClosed":DoorOpenerSts.FullClsd,
            "TgsOpening":DoorOpenerSts.MovgOut,
            "TgsHover":DoorOpenerSts.StopDurgOpen,
            "TgsNA":DoorOpenerSts.Ukwn,
            # "UNKNOWN_ENUM_VALUE_TailGateStatus_6":DoorOpenerSts.MovgInBrkg,
            # "UNKNOWN_ENUM_VALUE_TailGateStatus_7":DoorOpenerSts.MovgOutBrkg,
            "TgsHover":DoorOpenerSts.StopDurgCls,
        }
        self.bus_comm.set_singal("bodycan",'PotBodyFr02', 'TrOpenerSts', 1)
        for key in tailgate_status:
            begin_time = time.time()
            self.bus_comm.set_tailgate_opener_sts(sts=tailgate_status[key],time_wait=1)
            self.tsp.check_rvs_data_update_new(
                block=BlockName.VehicleBody,keys=["tailGate","status"],target_value=getattr(TailGateStatusRvs, key).value,begin_time=begin_time
            )

    @pytest.mark.smoke
    def test_central_lock_status_caseid_112844(self):
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(3)
        central_lock_status = {
            "ClsUnlock" :LockCmd.UnLock,
            "ClsLocked" :LockCmd.Lock,
        }
        for key in central_lock_status:
            self.mix.ctrl_lock(lock_type=central_lock_status[key],ctrl_type=LockSource.NFC)
            self.tsp.check_rvs_data_update_new(
                block=BlockName.VehicleBody,keys=["centralLock","status"],target_value=getattr(CentralLockStatus, key).value
            )
            sleep(3)
    
    @pytest.mark.sanity
    def test_tailwing_pos_caseid_1918342(self):
        tailwing_pos ={
           "TwpTailWingPosition0" :TailWingPos.P0,
           "TwpTailWingPosition1" :TailWingPos.P1,
           "TwpTailWingPosition2" :TailWingPos.P2,
           "TwpTailWingPosition3":TailWingPos.P3,
           "TwpTailWingPositionNA" :TailWingPos.Reserved,
        #    "UNKNOWN_ENUM_VALUE_TailWingPosition_5" :TailWingPos.Ukwn,   
        }

        for key in tailwing_pos:
            self.bus_comm.set_tailwing_pos(pos=tailwing_pos[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.VehicleBody,keys=["tailWing","position"],target_value=getattr(TailWingPositionRvs, key).value
            )

    @pytest.mark.full
    def test_tailwing_mode_caseid_1983459(self):
        self.sd_tester.write_single_ccp(564, 2)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.mix.set_car_mode(CarMode.NORMAL)
        tailwing_mode = {
            "TwmTailWingModeOff":TailWindMode.Off,
            "TwmTailWingModeOn":TailWindMode.On,
            "TwmTailWingModeAuto":TailWindMode.Auto,
        }
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Auto)
        sleep(1)
        for key in tailwing_mode:
            self.soa.hmi_set_tailwing_mode(mode=tailwing_mode[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.VehicleBody,keys=["tailWing","wingMode"],target_value=getattr(TailWingModeRvs, key).value
            )


    @pytest.mark.full
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196767?projectId=46',
        name='RVS Case 1196767',
    )
    def test_window_status_caseid_116045(self):
        for signal_value in [26, 21, 10, 1]:
            self.bus_comm.set_singal("bodycan","DdmBodyFr04","WinPosnStsAtDrvr",signal_value)
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["windows","id==0", "position"],target_value=(signal_value - 1) * 4)

    
    
    @pytest.mark.full
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196767?projectId=46',
        name='RVS Case 116048',
    )
    def test_window_status_caseid_116048(self):
        for signal_value in [26, 20, 10, 1]:
            self.bus_comm.set_singal("bodycan","PdmBodyFr01","WinPosnStsAtPass",signal_value)
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["windows","id==1","position"],target_value=(signal_value - 1) * 4)

    
    
    @pytest.mark.full
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196767?projectId=46',
        name='RVS Case 1196767',
    )
    def test_window_status_caseid_116064(self):
        for signal_value in [26, 20, 10, 1]:
            self.bus_comm.set_singal("bodycan","RldmBodyFr01","WinPosnStsAtReLe",signal_value)
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["windows", "id==2","position"],target_value=(signal_value - 1) * 4)

    

    
    @pytest.mark.full
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196767?projectId=46',
        name='RVS Case 116044',
    )
    def test_window_status_caseid_116044(self):
        for signal_value in [26, 20, 10, 1]:
            self.bus_comm.set_singal("bodycan","RrdmBodyFr01","WinPosnStsAtReRi",signal_value)
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["windows", "id==3","position"],target_value=(signal_value - 1) * 4)

    
    @pytest.mark.sanity
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196767?projectId=46',
        name='RVS Case 1196767',
    )
    def test_Drvrdoor_position_caseid_112339(self):
        self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorOpenerDrvrSts",1)
        self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorDrvrPosn",0)
        self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorDrvrPercPosn",0)
        sleep(5)
        for signal_value in [26, 20, 10, 1]:
            self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorDrvrPercPosn",signal_value)
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["doors","id==0", "position"],target_value=signal_value)

    @pytest.mark.sanity
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196767?projectId=46',
        name='RVS Case 1985318',
    )
    def test_Passdoor_position_caseid_1985318(self):
        self.bus_comm.set_singal("bodycan","PpodBodyFr01","DoorPassPosn",0)
        self.bus_comm.set_singal("bodycan","PpodBodyFr01","DoorPassPercPosn",0)
        sleep(2)
        for signal_value in [26, 20, 10, 1]:
            self.bus_comm.set_singal("bodycan","PpodBodyFr01","DoorPassPercPosn",signal_value)
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["doors", "id==1","position"],target_value=signal_value)


    @pytest.mark.sanity
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196767?projectId=46',
        name='RVS Case 1985319',
    )
    def test_LeRedoor_position_caseid_1985319(self):
        self.bus_comm.set_singal("bodycan","LpodBodyFr01","DoorLeRePosn",0)
        self.bus_comm.set_singal("bodycan","LpodBodyFr01","DoorLeRePercPosn",0)
        for signal_value in [26, 20, 10, 1]:
            self.bus_comm.set_singal("bodycan","LpodBodyFr01","DoorLeRePercPosn",signal_value)
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["doors", "id==2","position"],target_value=signal_value)


    @pytest.mark.sanity
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196767?projectId=46',
        name='RVS Case 1985320',
    )
    def test_RiRedoor_position_caseid_1985320(self):
        self.bus_comm.set_singal("bodycan","RpodBodyFr01","DoorRiRePosn",0)
        self.bus_comm.set_singal("bodycan","RpodBodyFr01","DoorRiRePercPosn",0)
        for signal_value in [26, 20, 10, 1]:
            self.bus_comm.set_singal("bodycan","RpodBodyFr01","DoorRiRePercPosn",signal_value)
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["doors", "id==3","position"],target_value=signal_value)


    @pytest.mark.sanity
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196767?projectId=46',
        name='RVS Case 112338',
    )
    def test_Drvrdoor_angle_caseid_112338(self):
        for signal_value in [26, 20, 10, 5]:
            self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorDrvrPosn",signal_value)
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["doors", "id==0","curAngle"],target_value=signal_value)


    @pytest.mark.sanity
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196767?projectId=46',
        name='RVS Case 1985315',
    )
    def test_Passdoor_angle_caseid_1985315(self):
        for signal_value in [26, 20, 10, 5]:
            self.bus_comm.set_singal("bodycan","PpodBodyFr01","DoorPassPosn",signal_value)
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["doors", "id==1","curAngle"],target_value=signal_value)

    
    @pytest.mark.sanity
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196767?projectId=46',
        name='RVS Case 1985316',
    )
    def test_LeRedoor_angle_caseid_1985316(self):
        for signal_value in [26, 20, 10, 5]:
            self.bus_comm.set_singal("bodycan","LpodBodyFr01","DoorLeRePosn",signal_value)
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["doors", "id==2","curAngle"],target_value=signal_value)


    @pytest.mark.sanity
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196767?projectId=46',
        name='RVS Case 1985317',
    )
    def test_RiRedoor_angle_caseid_1985317(self):
        for signal_value in [26, 20, 10, 5]:
            self.bus_comm.set_singal("bodycan","RpodBodyFr01","DoorRiRePosn",signal_value)
            self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["doors","id==3", "curAngle"],target_value=signal_value)


    
    @pytest.mark.smoke
    def test_tailgate_position_caseid_112337(self):
        for signal_value in [99, 50, 30, 10]:
            self.bus_comm.set_singal("bodycan","PotBodyFr03","TrOpenPosn",signal_value)
            self.tsp.check_rvs_data_update_new(
                block=BlockName.VehicleBody,keys=["tailGate","position"],target_value=signal_value
            )

    @pytest.mark.sanity
    def test_drive_mirrorfolder_caseid_112357(self):
        drive_mirrorfolder={
        "3":ViewFoldStatus.StatusUnfolding,
        "1":ViewFoldStatus.StatusUnfolded,
        "4":ViewFoldStatus.StatusFolding,
        "2":ViewFoldStatus.StatusFolded,
        }
        self.bus_comm.set_singal("bodycan","DdmBodyFr01","MirrFoldStsAtDrvr",2)
        sleep(1)
        for key in drive_mirrorfolder:
            self.bus_comm.set_rear_view_mode(pos=ViewPos.RearLeft,mode=drive_mirrorfolder[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.VehicleBody,keys=["outerRearView","id==1","foldStatus"],target_value=int(key))
            


    @pytest.mark.sanity
    def test_pass_mirrorfolder_caseid_1988539(self):
        pass_mirrorfolder={
        "3":ViewFoldStatus.StatusUnfolding,
        "1":ViewFoldStatus.StatusUnfolded,
        "4":ViewFoldStatus.StatusFolding,
        "2":ViewFoldStatus.StatusFolded,
        }
        self.bus_comm.set_singal("bodycan","PdmBodyFr01","MirrFoldStsAtPass",2)
        sleep(1)
        for key in pass_mirrorfolder:
            self.bus_comm.set_rear_view_mode(pos=ViewPos.RearRight,mode=pass_mirrorfolder[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.VehicleBody,keys=["outerRearView","id==0","foldStatus"],target_value=int(key))

    @pytest.mark.full
    def test_tailwing_status_caseid_112083(self):
        tailwing_status ={
           "1" :TailWingPos.Shifting,
           "0" :TailWingPos.Ukwn,  
        }
        self.bus_comm.set_tailwing_pos(pos=TailWingPos.P1)
        sleep(2)
        for key in tailwing_status:
            self.bus_comm.set_tailwing_pos(pos=tailwing_status[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.VehicleBody,keys=["tailWing","status"],target_value=int(key)
            )
    @pytest.mark.sanity
    def test_HoodStatus_caseid_1918338(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.io.set_hood_sts(HoodSts.Close)
        sleep(1)
        self.io.set_hood_sts(HoodSts.Open)
        self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["bonnet","status"],target_value=0)
        sleep(1)
        self.io.set_hood_sts(HoodSts.Close)
        self.tsp.check_rvs_data_update_new(block=BlockName.VehicleBody,keys=["bonnet","status"],target_value=1)


    
    # @pytest.mark.chargetime
    # @pytest.mark.sanity
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1350948?projectId=46', name='RVS case 1350948')
    # def test_chargtime_caseid_1350948(self):
    #     time_satrt = int(time.time()*1000)
    #     logger.info("Charge start time: {0}".format(time_satrt))
    #     self.ipdu.backbonefr_vddmbackbonefr16_chrgnordischrgnstsfb_chrgnsts2_dccharging()
    #     time.sleep(30)
    #     self.ipdu.backbonefr_vddmbackbonefr16_chrgnordischrgnstsfb_chrgnsts2_dcchargingend()
    #     time_end = int(time.time()*1000)
    #     logger.info("Charge end time: {0}".format(time_end))
    #     time.sleep(5)
    #     assert self.rvs_client.get_rvs_data_from_cloud(10107)["charging"]["recentChargeStartTime"] - time_satrt < 2000
    #     assert time_end - self.rvs_client.get_rvs_data_from_cloud(10107)["charging"]["recentChargeEndTime"] < 2000

    

    # # # Not Ready
    # # def test_lowbattsoc(self):
    # #     for low_batt_soc in [0, 123, 432, 243, 111, 333, 471, 500, 511]:
    # #         self.ipdu.propulsioncan_becmpropfr01_hvbattudc_value(voltage)
    # #         ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 10107)
    # #         batt_info = self.protoparse.get_charging_info(ble_bytes).batteryInfo
    # #         logger.info("Get chargpower status: {0}".format(batt_info))
    # #         assert round(batt_info.voltage,2) == voltage*0.25

    # @pytest.mark.sanity
    # @allure.testcase(
    #     'https://jama.jiduauto.com/perspective.req#/testCases/1350942?projectId=46',
    #     name='RVS case 1350942',
    # )
    # def test_drive_mirrorfolder_caseid_112357(self):
    #     mirror_folder_sts = [
    #         "VfsStatusNa",
    #         "VfsStatusUnfolded",
    #         "VfsStatusFolded",
    #         "VfsStatusUnfolding",
    #         "VfsStatusFolding",
    #         "VfsStatusHover",
    #     ]
    #     for value in range(4, -1, -1):
    #         self.bus_comm.set_singal(
    #             "bodycan","DdmBodyFr01",
    #             "MirrFoldStsAtDrvr",
    #             value,
    #         )
    #         self.tsp.check_rvs_data_update_new(
    #             BlockName.VehicleBody,["outerRearView", "id"], 1, index=1
    #         )
    #         self.tsp.check_rvs_data_update_new(
    #             BlockName.VehicleBody,
    #             ["outerRearView", "foldStatus"],
    #             mirror_folder_sts[value],
    #             index=1,
    #         )
    #     for value in range(4, -1, -1):
    #         self.bus_comm.set_singal(
    #             "bodycan","PdmBodyFr01",
    #             'MirrFoldStsAtPass',
    #             value,
    #         )
    #         self.tsp.check_rvs_data_update_new(
    #             BlockName.VehicleBody,["outerRearView", "id"], 0, index=0
    #         )
    #         self.tsp.check_rvs_data_update_new(
    #             BlockName.VehicleBody,
    #             ["outerRearView", "foldStatus"],
    #             mirror_folder_sts[value],
    #             index=0,
    #         )

    # @pytest.mark.tyre
    # @pytest.mark.sanity
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359760?projectId=46', name='RVS case 1359760')
    # def test_block_10103_tyre_pressure_fl_caseid_1359760(self):
    #     tyre_pressure = {"id": 0, "pressure": 200}
    #     pres = 1
    #     while pres < 350.115:
    #         tyre_pressure["pressure"] = pres
    #         self.tyre_server.pressure_info = tyre_pressure
    #         self.tyre_server.tyrepress_event_send()
    #         self.tsp.check_rvs_data_update_new(BlockName.VehicleBody,["tire", "id"], "TyreFrontLeft", index=0)
    #         self.tsp.check_rvs_data_update_new(BlockName.VehicleBody,["tire", "pressure"], pres, index=0)
    #         pres = round(pres + 35.1, 1)

    # @pytest.mark.tyre
    # @pytest.mark.sanity
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359761?projectId=46', name='RVS case 1359761')
    # def test_block_10103_tyre_pressure_fr_caseid_1359761(self):
    #     tyre_pressure = {"id": 1, "pressure": 200}
    #     pres = 1
    #     while pres < 350.115:
    #         tyre_pressure["pressure"] = pres
    #         self.tyre_server.pressure_info = tyre_pressure
    #         self.tyre_server.tyrepress_event_send()
    #         self.tsp.check_rvs_data_update_new(BlockName.VehicleBody,["tire", "id"], "TyreFrontRight", index=1)
    #         self.tsp.check_rvs_data_update_new(BlockName.VehicleBody,["tire", "pressure"], pres, index=1)
    #         pres = round(pres + 35.1, 1)

    # @pytest.mark.tyre
    # @pytest.mark.sanity
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359762?projectId=46', name='RVS case 1359762')
    # def test_block_10103_tyre_pressure_rl_caseid_1359762(self):
    #     tyre_pressure = {"id": 2, "pressure": 200}
    #     pres = 1
    #     while pres < 350.115:
    #         tyre_pressure["pressure"] = pres
    #         self.tyre_server.pressure_info = tyre_pressure
    #         self.tyre_server.tyrepress_event_send()
    #         self.tsp.check_rvs_data_update_new(BlockName.VehicleBody,["tire", "id"], "TyreRearLeft", index=2)
    #         self.tsp.check_rvs_data_update_new(BlockName.VehicleBody,["tire", "pressure"], pres, index=2)
    #         pres = round(pres + 35.1, 1)

    # @pytest.mark.tyre
    # @pytest.mark.sanity
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359763?projectId=46', name='RVS case 1359763')
    # def test_block_10103_tyre_pressure_rr_caseid_1359763(self):
    #     tyre_pressure = {"id": 3, "pressure": 200}
    #     pres = 1
    #     while pres < 350.115:
    #         tyre_pressure["pressure"] = pres
    #         self.tyre_server.pressure_info = tyre_pressure
    #         self.tyre_server.tyrepress_event_send()
    #         self.tsp.check_rvs_data_update_new(BlockName.VehicleBody,["tire", "id"], "TyreRearRight", index=3)
    #         self.tsp.check_rvs_data_update_new(BlockName.VehicleBody,["tire", "pressure"], pres, index=3)
    #         pres = round(pres + 35.1, 1)

    # @pytest.mark.tyre
    # @pytest.mark.sanity
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359764?projectId=46', name='RVS case 1359764')
    # def test_block_10103_tyre_temperature_fl_caseid_1359764(self):
    #     tyre_temp = {"id": 0, "temperature": 200}
    #     temp = 1
    #     while temp < 206:
    #         tyre_temp["temperature"] = temp
    #         self.tyre_server.temp_info = tyre_temp
    #         self.tyre_server.tyretemp_event_send()
    #         self.tsp.check_rvs_data_update_new(BlockName.VehicleBody,["tire", "id"], "TyreFrontLeft", index=0)
    #         self.tsp.check_rvs_data_update_new(BlockName.VehicleBody,["tire", "temperature"], temp, index=0)
    #         temp = temp + 17

    # @pytest.mark.tyre
    # @pytest.mark.sanity
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359765?projectId=46', name='RVS case 1359765')
    # def test_block_10103_tyre_temperature_fr_caseid_1359765(self):
    #     tyre_temp = {"id": 1, "temperature": 200}
    #     temp = 1
    #     while temp < 206:
    #         tyre_temp["temperature"] = temp
    #         self.tyre_server.temp_info = tyre_temp
    #         self.tyre_server.tyretemp_event_send()
    #         self.tsp.check_rvs_data_update_new(BlockName.VehicleBody,["tire", "id"], "TyreFrontRight", index=1)
    #         self.tsp.check_rvs_data_update_new(BlockName.VehicleBody,["tire", "temperature"], temp, index=1)
    #         temp = temp + 21

    # @pytest.mark.tyre
    # @pytest.mark.sanity
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359766?projectId=46', name='RVS case 1359766')
    # def test_block_10103_tyre_temperature_rl_caseid_1359766(self):
    #     tyre_temp = {"id": 2, "temperature": 200}
    #     temp = 1
    #     while temp < 206:
    #         tyre_temp["temperature"] = temp
    #         self.tyre_server.temp_info = tyre_temp
    #         self.tyre_server.tyretemp_event_send()
    #         self.tsp.check_rvs_data_update_new(BlockName.VehicleBody,["tire", "id"], "TyreRearLeft", index=2)
    #         self.tsp.check_rvs_data_update_new(BlockName.VehicleBody,["tire", "temperature"], temp, index=2)
    #         temp = temp + 13

    # @pytest.mark.tyre
    # @pytest.mark.sanity
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359767?projectId=46', name='RVS case 1359767')
    # def test_block_10103_tyre_temperature_rr_caseid_1359767(self):
    #     tyre_temp = {"id": 3, "temperature": 200}
    #     temp = 1
    #     while temp < 206:
    #         tyre_temp["temperature"] = temp
    #         self.tyre_server.temp_info = tyre_temp
    #         self.tyre_server.tyretemp_event_send()
    #         self.tsp.check_rvs_data_update_new(BlockName.VehicleBody,["tire", "id"], "TyreRearRight", index=3)
    #         self.tsp.check_rvs_data_update_new(BlockName.VehicleBody,["tire", "temperature"], temp, index=3)
    #         temp = temp + 11


    

   
    

