#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
import time
import pytest
import allure
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.common import *

@allure.feature("远程控制/远控两域联调测试/远控电动门")
@allure.story("远控电动门")
class TestRvcLock(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["DoorService_client",
                         "CentralLockService_client",
                         "VehicleSetStatusService_client",
                         "SeatService_client"])

    def before_each_func(self, ecu):
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,
                                       vehmtnst=VehMtnSts.StandStillVal2)
        self.mix.set_all_seats_present_sts(seat_pres_sts=SeatPresSts.NoPres)
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd,
                                          pass_opener=DoorOpenerSts.FullClsd,
                                          lere_opener=DoorOpenerSts.FullClsd,
                                          rire_opener=DoorOpenerSts.FullClsd,
                                          tr_opener=DoorOpenerSts.FullClsd)
        
    def after_each_func(self, ecu):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,
                                       vehmtnst=VehMtnSts.StandStillVal2)
        self.mix.set_all_seats_present_sts(seat_pres_sts=SeatPresSts.NoPres)
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd,
                                          pass_opener=DoorOpenerSts.FullClsd,
                                          lere_opener=DoorOpenerSts.FullClsd,
                                          rire_opener=DoorOpenerSts.FullClsd,
                                          tr_opener=DoorOpenerSts.FullClsd)
        if ecu.testresult == 'Failure':
            logger.info('用例执行失败')
            sleep(12)
        self.io.bgm_diag_line_up()
        logger.info(f'连接诊断激活线')
        self.io.tcam_kl15_up()
        sleep(10)
        self.bus_comm.resume_all_bus_send()
   
    def after_class(self, ecu):
        pass

    @allure.title("RVC_远控开启左前门")
    @pytest.mark.smoke
    def test_caseid_1999108(self):
        execid=self.tsp.rvc_door_control(door_code=DoorCode.driver_door_control,op=1,position=100)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Dirver,position=101,door_trigsrc=DoorTrigerSource.NoTrigSrc,timeout=10)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, isopen=False, doormovests=DoorMoveStatus.Opened, antipinch=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控开启右后门")
    @pytest.mark.smoke
    def test_caseid_1999109(self):
        execid=self.tsp.rvc_door_control(door_code=DoorCode.rear_right_door_control,op=1,position=100)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.RearRight,position=101,door_trigsrc=DoorTrigerSource.NoTrigSrc,timeout=10)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullOpend)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, isopen=False, doormovests=DoorMoveStatus.Opened, antipinch=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控开启右前门")
    @pytest.mark.smoke
    def test_caseid_1999110(self):
        execid=self.tsp.rvc_door_control(door_code=DoorCode.passenger_door_control,op=1,position=100)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Pass,position=101,door_trigsrc=DoorTrigerSource.NoTrigSrc,timeout=10)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntRightDoorSts, isopen=False, doormovests=DoorMoveStatus.Opened, antipinch=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控开启左后门")
    @pytest.mark.smoke
    def test_caseid_1999111(self):
        execid=self.tsp.rvc_door_control(door_code=DoorCode.rear_left_door_control,op=1,position=100)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.RearLeft,position=101,door_trigsrc=DoorTrigerSource.NoTrigSrc,timeout=10)
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullOpend)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearLeftDoorSts, isopen=False, doormovests=DoorMoveStatus.Opened, antipinch=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控一键开所有门")
    @pytest.mark.sanity
    def test_caseid_1999112(self):
        execid=self.tsp.rvc_door_control(door_code=DoorCode.All_door,op=1,position=100)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Dirver,position=100,door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend,pass_opener=DoorOpenerSts.FullOpend,lere_opener=DoorOpenerSts.FullOpend,rire_opener=DoorOpenerSts.FullOpend)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.All, isopen=False, doormovests=DoorMoveStatus.Opened, antipinch=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控一键开所有门关")
    @pytest.mark.sanity
    def test_caseid_1999113(self):
        self.io.set_five_door_sts(Door.open)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend,pass_opener=DoorOpenerSts.FullOpend,lere_opener=DoorOpenerSts.FullOpend,rire_opener=DoorOpenerSts.FullOpend)
        sleep(5)
        execid=self.tsp.rvc_door_control(door_code=DoorCode.All_door,op=2,position=0)
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver,door_req=DoorOpenerReq.Close,door_trigsrc=DoorTrigerSource.HMI)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd,pass_opener=DoorOpenerSts.FullClsd,lere_opener=DoorOpenerSts.FullClsd,rire_opener=DoorOpenerSts.FullClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.All, isopen=False, doormovests=DoorMoveStatus.Closed, antipinch=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控关左前门")
    @pytest.mark.sanity
    def test_caseid_1999114(self):
        self.io.set_five_door_sts(Door.open)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
        sleep(5)
        execid=self.tsp.rvc_door_control(door_code=DoorCode.driver_door_control,op=2,position=0)
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver,door_req=DoorOpenerReq.Close,door_trigsrc=DoorTrigerSource.HMI)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, isopen=False, doormovests=DoorMoveStatus.Closed, antipinch=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控关右前门")
    @pytest.mark.sanity
    def test_caseid_1999115(self):
        self.io.set_five_door_sts(Door.open)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
        sleep(5)
        execid=self.tsp.rvc_door_control(door_code=DoorCode.passenger_door_control,op=2,position=0)
        self.bus_comm.check_door_opener_req_and_trigsrc(pass_opener=DoorPos.Pass,door_req=DoorOpenerReq.Close,door_trigsrc=DoorTrigerSource.HMI)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntRightDoorSts, isopen=False, doormovests=DoorMoveStatus.Closed, antipinch=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控关左后门")
    @pytest.mark.sanity
    def test_caseid_1999116(self):
        self.io.set_five_door_sts(Door.open)
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullOpend)
        sleep(5)
        execid=self.tsp.rvc_door_control(door_code=DoorCode.rear_left_door_control,op=2,position=0)
        self.bus_comm.check_door_opener_req_and_trigsrc(lere_opener=DoorPos.RearLeft,door_req=DoorOpenerReq.Close,door_trigsrc=DoorTrigerSource.HMI)
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearLeftDoorSts, isopen=False, doormovests=DoorMoveStatus.Closed, antipinch=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控开启左后门")
    @pytest.mark.sanity
    def test_caseid_1999117(self):
        self.io.set_five_door_sts(Door.open)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullOpend)
        sleep(5)
        execid=self.tsp.rvc_door_control(door_code=DoorCode.rear_right_door_control,op=2,position=0)
        self.bus_comm.check_door_opener_req_and_trigsrc(rire_opener=DoorPos.RearRight,door_req=DoorOpenerReq.Close,door_trigsrc=DoorTrigerSource.HMI)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, isopen=False, doormovests=DoorMoveStatus.Closed, antipinch=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"