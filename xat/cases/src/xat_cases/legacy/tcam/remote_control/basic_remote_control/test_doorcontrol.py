#!/usr/bin/env python
# -*- coding: utf-8 -*-

import allure
import pytest
import threading
import itertools


from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.common import *

@allure.feature("互联服务/远程控制/远程解闭锁")
@allure.story("远程解闭锁")
class TestRvcDoorControl(TestABCBase):
    lock = threading.Lock()
    SetDoorCloseLock_req_num = 0
    door_code_id = {
            DoorCode.All_door : DoorId.kDoorAll,
            DoorCode.driver_door_control : DoorId.kDoorFrontLeft,
            DoorCode.passenger_door_control : DoorId.kDoorFrontRight,
            DoorCode.rear_left_door_control : DoorId.kDoorRearLeft,
            DoorCode.rear_right_door_control : DoorId.kDoorRearRight
        }
    def before_class(self, ecu):
        self.soa.update(["VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server",
                         "DoorService_server", "SeatService_server", "CentralLockService_server",
                         "HighVoltageService_server", "VehicleTimeService_server",
                         "KeyService_server","EntryService_server", "TailGateService_server","RemoteCtrlService_client",('CdcTtsService','server','cdc_a_ttsservice',600)])
        # self.mix.start_get_request_and_send_response_to_tcam_thread(["VehicleModeService_server", "FotaMasterService_server",
        #                  "VehicleSetStatusService_server", "ChassisService_server",
        #                  "DoorService_server", "SeatService_server", "CentralLockService_server",
        #                  "HighVoltageService_server", "VehicleTimeService_server",
        #                  "KeyService_server", "TailGateService_server"],ignore_func=['GetOpenCloseStatus','TailGateService_GetStatus'])
        sleep(30)

    def before_each_func(self, ecu):
        self.error_msg = ""
        self.error = False
        self.SetDoorCloseLock_req_num = 0
        self.soa.empty_all()
        self.soa.set_tcam_rvc_common_preconditions()
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.send_Alldoor_close()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))
        
    def after_each_func(self, ecu):
        if ecu.testresult == 'Failure':
            logger.info('用例执行失败')
            sleep(40)
        if '1990897' in ecu.testname and ecu.testresult == 'Failure':
            self.soa.soa_partner.start_single_partner(service="DoorService",role="server")
            self.soa.soa_partner.empty_all()
            self.soa.soa_partner.wait_for_service_reconnect("DoorService_server",timeout=30)   
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.ipdu.reset_check_results()
        sleep(1)

    def after_class(self, ecu):
        # self.mix.stop_get_request_and_send_response_to_tcam_thread()
        pass
    
    def set_door_sts(self,doorid:DoorId, sts:DoorStatus):
        if sts == DoorStatus.kClosed:
            isopen = False
        else:
            isopen = True
        if doorid == DoorId.kDoorFrontLeft:
            self.soa.notify_FrntLeftDoorSts(isopen,sts=sts)
        elif doorid == DoorId.kDoorFrontRight:
            self.soa.notify_FrntRightDoorSts(isopen,sts=sts)
        elif doorid == DoorId.kDoorRearLeft:
            self.soa.notify_RearLeftDoorSts(isopen,sts=sts)
        elif doorid == DoorId.kDoorRearRight:
            self.soa.notify_RearRightDoorSts(isopen,sts=sts)
        elif doorid == DoorId.kDoorAll:
            self.soa.notify_FrntLeftDoorSts(isopen,sts=sts)
            self.soa.notify_FrntRightDoorSts(isopen,sts=sts)
            self.soa.notify_RearRightDoorSts(isopen,sts=sts)
            self.soa.notify_RearLeftDoorSts(isopen,sts=sts)

    def normal_process_open(self, door_code:DoorCode, lock_sts:LockStatus, userInVehicleStatus:bool = True):
        execid = self.tsp.rvc_door_control(door_code=door_code)
        if lock_sts != LockStatus.Unlocked and self.SetDoorCloseLock_req_num == 0:
            with self.lock:
                try:
                    self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock,timeout=10)
                except AssertionError as e:
                    self.error = True
                    self.error_msg = '未获取到SetDoorCloseLock请求'
                    logger.info('未获取到SetDoorCloseLock请求')
                self.soa.notify_LockStatus(LockStatus.Unlocked)
                try:
                    self.soa.check_NotifyRVCLockInfo_event(timeout=10)
                except AssertionError as e:
                    self.error = True
                    self.error_msg = '未获取到NotifyRVCLockInfo请求'
                    logger.info('未获取到NotifyRVCLockInfo请求')
                self.SetDoorCloseLock_req_num = 1

        if userInVehicleStatus == True:
            Scene = VehicleInsideOutside.VehicleInSide
        else:
            Scene = VehicleInsideOutside.VehicleOutSide
        try:
            doors_pos_dict = {}
            if door_code == DoorCode.All_door:
                for doorid in self.door_code_id.values():
                    if doorid != DoorId.kDoorAll:
                        doors_pos_dict[doorid] = 5
            else:
                doors_pos_dict[self.door_code_id[door_code]] = 5
            with self.lock:
                self.soa.check_DoorService_SetPosition_req_and_feedback_resp(doors_pos_dict,scene=Scene,timeout=10)

        except AssertionError as e:
            self.error = True
            self.error_msg = '未获取到DoorService_SetPosition请求'
            logger.info('未获取到DoorService_SetPosition请求')
        self.set_door_sts(self.door_code_id[door_code], sts=DoorStatus.kOpened)
        try:
            assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        except AssertionError as e:
            self.error = True
            self.error_msg = f'云端查询错误 execid:{execid}'

    def normal_process_close(self, door_code:DoorCode,userInVehicleStatus:bool = True):
        execid = self.tsp.rvc_door_control(door_code=door_code,op=2)
        if door_code == DoorCode.All_door:
            with self.lock:
                if userInVehicleStatus == True:
                    self.soa.check_Play2_req(app='RVC',txt='关门请当心',param='{"isLoopPlay":False,"priority":1,"streamType":6,"zone":0}',timeout=10)
                else:
                    self.soa.check_Play2_req(app='RVC',txt='关门请当心',param='{"isLoopPlay":False,"priority":1,"streamType":6,"zone":3}',timeout=10)

        try:
            doors = [self.door_code_id[door_code]]
            with self.lock:
                self.soa.check_DoorService_Close_req_and_feedback_resp(doors=doors,timeout=10)
        except AssertionError as e:
            self.error = True
            self.error_msg = '未获取到DoorService_Close_req请求'
            logger.info('未获取到DoorService_Close_req请求')
        self.set_door_sts(self.door_code_id[door_code], sts=DoorStatus.kClosed)
        try:
            assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        except AssertionError as e:
            self.error = True
            self.error_msg = '云端查询错误'

    def normal_process_close_error(self, door_code:DoorCode,userInVehicleStatus:bool = True):
        execid = self.tsp.rvc_door_control(door_code=door_code,op=2)
        if door_code == DoorCode.All_door:
            with self.lock:
                if userInVehicleStatus == True:
                    self.soa.check_Play2_req(app='RVC',txt='关门请当心',param='{"isLoopPlay":False,"priority":1,"streamType":6,"zone":0}',timeout=10)
                else:
                    self.soa.check_Play2_req(app='RVC',txt='关门请当心',param='{"isLoopPlay":False,"priority":1,"streamType":6,"zone":3}',timeout=10)

        try:
            doors = [self.door_code_id[door_code]]
            with self.lock:
                self.soa.check_DoorService_Close_req_and_feedback_resp(doors=doors,timeout=10)
        except AssertionError as e:
            self.error = True
            self.error_msg = '未获取到DoorService_Close_req请求'
            logger.info('未获取到DoorService_Close_req请求')
        return execid

    def normal_process_open_error(self, door_code:DoorCode, lock_sts:LockStatus, userInVehicleStatus:bool = True, lock_error=False):
        """
        触发开门的一半动作
        door_code:那个门, 必须传
        userInVehicleStatus: 是否有人
        lock_sts: 当前锁的状态
        lock_error: 触发解锁失败流程检测
        """
        execid = self.tsp.rvc_door_control(door_code=door_code)
        if lock_sts != LockStatus.Unlocked and self.SetDoorCloseLock_req_num == 0:
            with self.lock:
                try:
                    self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock,timeout=10)
                except AssertionError as e:
                    self.error = True
                    self.error_msg = '未获取到SetDoorCloseLock请求'
                    logger.info('未获取到SetDoorCloseLock请求')
                if not lock_error:
                    self.soa.notify_LockStatus(LockStatus.Unlocked)
                else:
                    try:
                        assert self.tsp.log_search_remote_vehicle_control("UnlockFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
                    except AssertionError as e:
                        self.error = True
                        self.error_msg = '云端查询错误'
                        return execid
                try:
                    self.soa.check_NotifyRVCLockInfo_event(timeout=10)
                except AssertionError as e:
                    self.error = True
                    self.error_msg = '未获取到NotifyRVCLockInfo请求'
                    logger.info('未获取到NotifyRVCLockInfo请求')
                self.SetDoorCloseLock_req_num = 1

        if userInVehicleStatus == True:
            Scene = VehicleInsideOutside.VehicleInSide
        else:
            Scene = VehicleInsideOutside.VehicleOutSide
        try:
            doors_pos_dict = {}
            if door_code == DoorCode.All_door:
                for doorid in self.door_code_id.values():
                    if doorid != DoorId.kDoorAll:
                        doors_pos_dict[doorid] = 5
            else:
                doors_pos_dict[self.door_code_id[door_code]] = 5
            with self.lock:
                self.soa.check_DoorService_SetPosition_req_and_feedback_resp(doors_pos_dict,scene=Scene,timeout=10)

        except AssertionError as e:
            self.error = True
            self.error_msg = '未获取到DoorService_SetPosition请求'
            logger.info('未获取到DoorService_SetPosition请求')
        return execid


    def carmode_fail(self,error_carmode: CarMode = CarMode.TRANSPORT):
        self.soa.s2s_set_car_mode(car_mode=error_carmode)
        for i in DoorCode:
            sleep(0.5)
            execid = self.tsp.rvc_door_control(i)
            assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    def usagemode_fail(self,error_usagemode: UsageMode = UsageMode.ACTIVE):
        self.soa.s2s_set_usage_mode(usage_mode=error_usagemode)
        for i in DoorCode:
            sleep(0.5)
            execid = self.tsp.rvc_door_control(i)
            assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    def gear_fail(self,error_gear: Gear = Gear.Rvs):
        self.soa.s2s_set_gear(gear=error_gear)
        for i in DoorCode:
            sleep(0.5)
            execid = self.tsp.rvc_door_control(i)
            assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 


    @allure.title("电动门控制-RVC_电动门控制_前提条件验证_车辆模式_TRANSPORT")
    @pytest.mark.smoke
    def test_caseid_1990697(self):
        self.carmode_fail(CarMode.TRANSPORT)

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证_车辆模式_FACTORY")
    @pytest.mark.full
    def test_caseid_1990698(self):
        self.carmode_fail(CarMode.FACTORY)

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证_车辆模式_CRASH")
    @pytest.mark.full
    def test_caseid_1990699(self):
        self.carmode_fail(CarMode.CRASH)

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证_车辆模式_DYNO")
    @pytest.mark.full
    def test_caseid_1990700(self):
        self.carmode_fail(CarMode.DYNO)

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证_使用模式_ACTIVE")
    @pytest.mark.smoke
    def test_caseid_1990701(self):
        self.usagemode_fail(UsageMode.ACTIVE)

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证_使用模式_DRIVING")
    @pytest.mark.full
    def test_caseid_1990702(self):
        self.usagemode_fail(UsageMode.DRIVING)

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证_使用模式_CONVENIENCE")
    @pytest.mark.sanity
    def test_caseid_1990703(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        for i in DoorCode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.normal_process_open(i,LockStatus.Unlocked)
            assert not self.error, self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证_维修模式_True")
    @pytest.mark.smoke
    def test_caseid_1990704(self):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(1)
        for i in DoorCode:
            sleep(0.5)
            execid = self.tsp.rvc_door_control(i)
            assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证_挡位_Rvs")
    @pytest.mark.smoke
    def test_caseid_1990705(self):
        self.gear_fail(Gear.Rvs)

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证_挡位_Neut")
    @pytest.mark.full
    def test_caseid_1990706(self):
        self.gear_fail(Gear.Neut)

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证_挡位_Drv")
    @pytest.mark.sanity
    def test_caseid_1990707(self):
        self.gear_fail(Gear.Drv)

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证_挡位_ManMode")
    @pytest.mark.full
    def test_caseid_1990708(self):
        self.gear_fail(Gear.ManMode)

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证_挡位_Resd1")
    @pytest.mark.full
    def test_caseid_1990709(self):
        self.soa.s2s_set_gear(gear=Gear.Resd1)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        for i in DoorCode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.normal_process_open(i,LockStatus.Unlocked)
            assert not self.error, self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证_挡位_Resd2")
    @pytest.mark.full
    def test_caseid_1990710(self):
        self.gear_fail(Gear.Resd2)

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证_挡位_Undefd")
    @pytest.mark.full
    def test_caseid_1990711(self):
        self.gear_fail(Gear.Undefd)

    @allure.title("远程解解锁-RVC_电动门控制_前提条件验证_OTA状态_UPDATE")
    @pytest.mark.smoke
    def test_caseid_1990712(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        sleep(0.5)
        for i in DoorCode:
            execid = self.tsp.rvc_door_control(i)
            assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程解解锁-RVC_电动门控制_前提条件验证_OTA状态_ROLLBACK")
    @pytest.mark.sanity
    def test_caseid_1990713(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        sleep(0.5)
        for i in DoorCode:
            execid = self.tsp.rvc_door_control(i)
            assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证__OTA状态_QUERY")
    @pytest.mark.full
    def test_caseid_1990714(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        sleep(0.5)
        for i in DoorCode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.normal_process_open(i,LockStatus.Unlocked)
            assert not self.error, self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证_OTA状态_NEW_TASK")
    @pytest.mark.full
    def test_caseid_1990715(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        sleep(0.5)
        for i in DoorCode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.normal_process_open(i,LockStatus.Unlocked)
            assert not self.error, self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证_OTA状态_DOWNLOADING")
    @pytest.mark.sanity
    def test_caseid_1990716(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        sleep(0.5)
        for i in DoorCode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.normal_process_open(i,LockStatus.Unlocked)
            assert not self.error, self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证_OTA状态_FAILED_NOT_DRIVING")
    @pytest.mark.full
    def test_caseid_1990717(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        sleep(0.5)
        for i in DoorCode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.normal_process_open(i,LockStatus.Unlocked)
            assert not self.error, self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证__OTA状态_FAILED_DRIVING")
    @pytest.mark.full
    def test_caseid_1990718(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_DRIVING)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        sleep(0.5)
        for i in DoorCode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.normal_process_open(i,LockStatus.Unlocked)
            assert not self.error, self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证__OTA状态_REACH_APPOINTMENT")
    @pytest.mark.full
    def test_caseid_1990719(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.REACH_APPOINTMENT)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        sleep(0.5)
        for i in DoorCode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.normal_process_open(i,LockStatus.Unlocked)
            assert not self.error, self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证__OTA状态_REMOTE_UPDATE")
    @pytest.mark.full
    def test_caseid_1990720(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.REMOTE_UPDATE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        sleep(0.5)
        for i in DoorCode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.normal_process_open(i,LockStatus.Unlocked)
            assert not self.error, self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证__OTA状态_FACTORY_TASK")
    @pytest.mark.full
    def test_caseid_1990721(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.FACTORY_TASK)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        sleep(0.5)
        for i in DoorCode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.normal_process_open(i,LockStatus.Unlocked)
            assert not self.error, self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证__OTA状态_FACTORY_UPDATE")
    @pytest.mark.full
    def test_caseid_1990722(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.FACTORY_UPDATE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        sleep(0.5)
        for i in DoorCode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)

            self.normal_process_open(i,LockStatus.Unlocked)
            assert not self.error, self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证__OTA状态_FACTORY_SUCCESSFUL")
    @pytest.mark.full
    def test_caseid_1990723(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.FACTORY_SUCCESSFUL)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        sleep(0.5)
        for i in DoorCode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.normal_process_open(i,LockStatus.Unlocked)
            assert not self.error, self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证__OTA状态_FACTORY_FAILED")
    @pytest.mark.full
    def test_caseid_1990724(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.FACTORY_FAILED)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        sleep(0.5)
        for i in DoorCode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.normal_process_open(i,LockStatus.Unlocked)
            assert not self.error, self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_前提条件验证__OTA状态_RESCUE")
    @pytest.mark.full
    def test_caseid_1990725(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.RESCUE)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        sleep(0.5)
        for i in DoorCode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.normal_process_open(i,LockStatus.Unlocked)
            assert not self.error, self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_前提条件优先级_OTA状态&挡位")
    @pytest.mark.full
    def test_caseid_1990726(self):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        self.gear_fail(Gear.Rvs)

    @allure.title("电动门控制-RVC_电动门控制_前提条件优先级_维修模式&挡位")
    @pytest.mark.full
    def test_caseid_1990727(self):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        sleep(0.5)
        for i in DoorCode:
            execid = self.tsp.rvc_door_control(i)
            assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("电动门控制-RVC_电动门控制_前提条件优先级_维修模式&使用模式")
    @pytest.mark.full
    def test_caseid_1990728(self):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.usagemode_fail(UsageMode.ACTIVE)

    @allure.title("电动门控制-RVC_电动门控制_前提条件优先级_车辆模式&使用模式")
    @pytest.mark.full
    def test_caseid_1990729(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.carmode_fail(CarMode.TRANSPORT)

    @allure.title("电动门控制-RVC_电动门控制_无效前提条件_插枪状态")
    @pytest.mark.sanity
    def test_caseid_1990730(self):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        sleep(0.5)
        for i in DoorCode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.normal_process_open(i,LockStatus.Unlocked)
            assert not self.error, self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_网络管理_唤醒失败")
    @pytest.mark.smoke
    def test_caseid_1990731(self):
        self.mix.tcam_network_sleep()
        for i in DoorCode:
            execid = self.tsp.rvc_door_control(i)
            assert self.tsp.log_search_remote_vehicle_control("NetwakeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("电动门控制-RVC_电动门控制_主驾车门开条缝_网络管理_PNC检查_ABANDONED")
    @pytest.mark.smoke
    def test_caseid_1990732(self):
        self.soa.notify_LockStatus(LockStatus.AllLocked)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_door_control(DoorCode.driver_door_control)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(LockStatus.Unlocked)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.set_door_sts(self.door_code_id[DoorCode.driver_door_control], sts=DoorStatus.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        # self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.no_valid,timeout=50)

    @allure.title("电动门控制-RVC_电动门控制_副驾车门开条缝_网络管理_PNC检查_ABANDONED")
    @pytest.mark.smoke
    def test_caseid_1990733(self):
        self.soa.notify_LockStatus(LockStatus.AllLocked)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_door_control(DoorCode.passenger_door_control)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(LockStatus.Unlocked)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.set_door_sts(self.door_code_id[DoorCode.passenger_door_control], sts=DoorStatus.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        # self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.no_valid,timeout=50)

    @allure.title("电动门控制-RVC_电动门控制_左后车门开条缝_网络管理_PNC检查_ABANDONED")
    @pytest.mark.smoke
    def test_caseid_1990734(self):
        self.soa.notify_LockStatus(LockStatus.AllLocked)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_door_control(DoorCode.rear_left_door_control)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(LockStatus.Unlocked)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.set_door_sts(self.door_code_id[DoorCode.rear_left_door_control], sts=DoorStatus.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        # self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.no_valid,timeout=50)

    @allure.title("电动门控制-RVC_电动门控制_右后车门开条缝_网络管理_PNC检查_ABANDONED")
    @pytest.mark.smoke
    def test_caseid_1990735(self):
        self.soa.notify_LockStatus(LockStatus.AllLocked)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_door_control(DoorCode.rear_left_door_control)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(LockStatus.Unlocked)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.set_door_sts(self.door_code_id[DoorCode.rear_left_door_control], sts=DoorStatus.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        # self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.no_valid,timeout=50)

    @allure.title("电动门控制-RVC_电动门控制_主驾车门开条缝_网络管理_PNC检查_INACTIVE")
    @pytest.mark.sanity
    def test_caseid_1990736(self):
        self.soa.notify_LockStatus(LockStatus.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        execid = self.tsp.rvc_door_control(DoorCode.driver_door_control)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_LockStatus(LockStatus.Unlocked)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.set_door_sts(self.door_code_id[DoorCode.driver_door_control], sts=DoorStatus.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_副驾车门开条缝_网络管理_PNC检查_INACTIVE")
    @pytest.mark.full
    def test_caseid_1990737(self):
        self.soa.notify_LockStatus(LockStatus.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        execid = self.tsp.rvc_door_control(DoorCode.passenger_door_control)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_LockStatus(LockStatus.Unlocked)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.set_door_sts(self.door_code_id[DoorCode.passenger_door_control], sts=DoorStatus.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_左后车门开条缝_网络管理_PNC检查_INACTIVE")
    @pytest.mark.full
    def test_caseid_1990738(self):
        self.soa.notify_LockStatus(LockStatus.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        execid = self.tsp.rvc_door_control(DoorCode.rear_left_door_control)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_LockStatus(LockStatus.Unlocked)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.set_door_sts(self.door_code_id[DoorCode.rear_left_door_control], sts=DoorStatus.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_右后车门开条缝_网络管理_PNC检查_INACTIVE")
    @pytest.mark.full
    def test_caseid_1990739(self):
        self.soa.notify_LockStatus(LockStatus.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        execid = self.tsp.rvc_door_control(DoorCode.rear_right_door_control)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_LockStatus(LockStatus.Unlocked)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.set_door_sts(self.door_code_id[DoorCode.rear_right_door_control], sts=DoorStatus.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_主驾车门开条缝_网络管理_PNC检查_CONVENIENCE")
    @pytest.mark.sanity
    def test_caseid_1990740(self):
        self.soa.notify_LockStatus(LockStatus.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        execid = self.tsp.rvc_door_control(DoorCode.driver_door_control)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.no_valid,timeout=3)
        self.soa.notify_LockStatus(LockStatus.Unlocked)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.set_door_sts(self.door_code_id[DoorCode.driver_door_control], sts=DoorStatus.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_副驾车门开条缝_网络管理_PNC检查_CONVENIENCE")
    @pytest.mark.full
    def test_caseid_1990741(self):
        self.soa.notify_LockStatus(LockStatus.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        execid = self.tsp.rvc_door_control(DoorCode.passenger_door_control)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.no_valid,timeout=3)
        self.soa.notify_LockStatus(LockStatus.Unlocked)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.set_door_sts(self.door_code_id[DoorCode.passenger_door_control], sts=DoorStatus.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_左后车门开条缝_网络管理_PNC检查_CONVENIENCE")
    @pytest.mark.full
    def test_caseid_1990742(self):
        self.soa.notify_LockStatus(LockStatus.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        execid = self.tsp.rvc_door_control(DoorCode.rear_left_door_control)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.no_valid,timeout=3)
        self.soa.notify_LockStatus(LockStatus.Unlocked)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.set_door_sts(self.door_code_id[DoorCode.rear_left_door_control], sts=DoorStatus.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_右后车门开条缝_网络管理_PNC检查_CONVENIENCE")
    @pytest.mark.full
    def test_caseid_1990743(self):
        self.soa.notify_LockStatus(LockStatus.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        execid = self.tsp.rvc_door_control(DoorCode.rear_right_door_control)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.no_valid,timeout=3)
        self.soa.notify_LockStatus(LockStatus.Unlocked)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.set_door_sts(self.door_code_id[DoorCode.rear_right_door_control], sts=DoorStatus.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_一键四门开条缝_网络管理_PNC检查_ABANDONED")
    @pytest.mark.smoke
    def test_caseid_1990744(self):
        self.soa.notify_LockStatus(LockStatus.AllLocked)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_door_control(DoorCode.All_door)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_LockStatus(LockStatus.Unlocked)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.set_door_sts(self.door_code_id[DoorCode.All_door], sts=DoorStatus.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        # self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.no_valid,timeout=50)

    @allure.title("电动门控制-RVC_电动门控制_一键四门开条缝_网络管理_PNC检查_INACTIVE")
    @pytest.mark.sanity
    def test_caseid_1990745(self):
        self.soa.notify_LockStatus(LockStatus.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        execid = self.tsp.rvc_door_control(DoorCode.All_door)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_LockStatus(LockStatus.Unlocked)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.set_door_sts(self.door_code_id[DoorCode.All_door], sts=DoorStatus.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        # self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.no_valid,timeout=50)

    @allure.title("电动门控制-RVC_电动门控制_一键四门开条缝_网络管理_PNC检查_CONVENIENCE")
    @pytest.mark.sanity
    def test_caseid_1990746(self):
        self.soa.notify_LockStatus(LockStatus.AllLocked)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        execid = self.tsp.rvc_door_control(DoorCode.All_door)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.no_valid,timeout=3)
        self.soa.notify_LockStatus(LockStatus.Unlocked)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.set_door_sts(self.door_code_id[DoorCode.All_door], sts=DoorStatus.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        # self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.no_valid,timeout=50)

    @allure.title("电动门控制-RVC_电动门控制_相同指令下发_主驾门开与主驾门开")
    @allure.issue('https://jira.jiduauto.com/browse/SOA-29276?filter=-2')
    @pytest.mark.smoke
    def test_caseid_1990747(self):
        self.set_door_sts(DoorId.kDoorAll,DoorStatus.kClosed)
        sleep(0.5)
        execid = self.tsp.rvc_door_control(DoorCode.driver_door_control)
        execid = self.tsp.rvc_door_control(DoorCode.driver_door_control)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)

    @allure.title("电动门控制-RVC_电动门控制_相同指令下发_主驾门开与主驾门关")
    @pytest.mark.full
    def test_caseid_1990748(self):
        self.set_door_sts(DoorId.kDoorAll,DoorStatus.kClosed)
        sleep(0.5)
        execid = self.tsp.rvc_door_control(DoorCode.driver_door_control)
        execid = self.tsp.rvc_door_control(DoorCode.driver_door_control,2)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)

    @allure.title("电动门控制-RVC_电动门控制_相同指令下发_主驾门关与主驾门关")
    @pytest.mark.full
    def test_caseid_1990749(self):
        self.set_door_sts(DoorId.kDoorAll,DoorStatus.kOpened)
        sleep(0.5)
        execid = self.tsp.rvc_door_control(DoorCode.driver_door_control,2)
        execid = self.tsp.rvc_door_control(DoorCode.driver_door_control,2)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)

    @allure.title("电动门控制-RVC_电动门控制_相同指令下发_副驾门关与副驾门关")
    @pytest.mark.smoke
    def test_caseid_1990750(self):
        self.set_door_sts(DoorId.kDoorAll,DoorStatus.kOpened)
        sleep(0.5)
        execid = self.tsp.rvc_door_control(DoorCode.passenger_door_control,2)
        execid = self.tsp.rvc_door_control(DoorCode.passenger_door_control,2)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)

    @allure.title("电动门控制-RVC_电动门控制_相同指令下发_副驾门开与副驾门关")
    @pytest.mark.full
    def test_caseid_1990751(self):
        self.set_door_sts(DoorId.kDoorAll,DoorStatus.kClosed)
        sleep(0.5)
        execid = self.tsp.rvc_door_control(DoorCode.passenger_door_control)
        execid = self.tsp.rvc_door_control(DoorCode.passenger_door_control,2)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)

    @allure.title("电动门控制-RVC_电动门控制_相同指令下发_主驾门开与主驾门开")
    @pytest.mark.full
    def test_caseid_1990752(self):
        self.set_door_sts(DoorId.kDoorAll,DoorStatus.kClosed)
        sleep(0.5)
        execid = self.tsp.rvc_door_control(DoorCode.passenger_door_control)
        execid = self.tsp.rvc_door_control(DoorCode.passenger_door_control)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)

    @allure.title("电动门控制-RVC_电动门控制_相同指令下发_左后门开与左后门开")
    @pytest.mark.smoke
    def test_caseid_1990753(self):
        self.set_door_sts(DoorId.kDoorAll,DoorStatus.kClosed)
        sleep(0.5)
        execid = self.tsp.rvc_door_control(DoorCode.rear_left_door_control)
        execid = self.tsp.rvc_door_control(DoorCode.rear_left_door_control)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)

    @allure.title("电动门控制-RVC_电动门控制_相同指令下发_左后门关与左后门开")
    @pytest.mark.full
    def test_caseid_1990754(self):
        self.set_door_sts(DoorId.kDoorAll,DoorStatus.kOpened)
        sleep(0.5)
        execid = self.tsp.rvc_door_control(DoorCode.rear_left_door_control,2)
        execid = self.tsp.rvc_door_control(DoorCode.rear_left_door_control)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)

    @allure.title("电动门控制-RVC_电动门控制_相同指令下发_左后门关与左后门关")
    @pytest.mark.full
    def test_caseid_1990755(self):
        self.set_door_sts(DoorId.kDoorAll,DoorStatus.kOpened)
        sleep(0.5)
        execid = self.tsp.rvc_door_control(DoorCode.rear_left_door_control,2)
        execid = self.tsp.rvc_door_control(DoorCode.rear_left_door_control,2)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)

    @allure.title("电动门控制-RVC_电动门控制_相同指令下发_右后门关与右后门关")
    @pytest.mark.smoke
    def test_caseid_1990756(self):
        self.set_door_sts(DoorId.kDoorAll,DoorStatus.kOpened)
        sleep(0.5)
        execid = self.tsp.rvc_door_control(DoorCode.rear_right_door_control,2)
        execid = self.tsp.rvc_door_control(DoorCode.rear_right_door_control,2)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)

    @allure.title("电动门控制-RVC_电动门控制_相同指令下发_右后门开与右后门关")
    @pytest.mark.full
    def test_caseid_1990757(self):
        self.set_door_sts(DoorId.kDoorAll,DoorStatus.kClosed)
        sleep(0.5)
        execid = self.tsp.rvc_door_control(DoorCode.rear_right_door_control)
        execid = self.tsp.rvc_door_control(DoorCode.rear_right_door_control,2)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)

    @allure.title("电动门控制-RVC_电动门控制_相同指令下发_右后门开与右后门开")
    @pytest.mark.full
    def test_caseid_1990758(self):
        self.set_door_sts(DoorId.kDoorAll,DoorStatus.kClosed)
        sleep(0.5)
        execid = self.tsp.rvc_door_control(DoorCode.rear_right_door_control)
        execid = self.tsp.rvc_door_control(DoorCode.rear_right_door_control)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)

    @allure.title("电动门控制-RVC_电动门控制_相同指令下发_一键四门开与一键四门开")
    @pytest.mark.smoke
    def test_caseid_1990759(self):
        self.set_door_sts(DoorId.kDoorAll,DoorStatus.kClosed)
        sleep(0.5)
        execid = self.tsp.rvc_door_control(DoorCode.All_door)
        execid = self.tsp.rvc_door_control(DoorCode.All_door)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)

    @allure.title("电动门控制-RVC_电动门控制_相同指令下发_一键四门关与一键四门开")
    @pytest.mark.full
    def test_caseid_1990760(self):
        self.set_door_sts(DoorId.kDoorAll,DoorStatus.kOpened)
        sleep(0.5)
        execid = self.tsp.rvc_door_control(DoorCode.All_door,2)
        execid = self.tsp.rvc_door_control(DoorCode.All_door)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)

    @allure.title("电动门控制-RVC_电动门控制_相同指令下发_一键四门关与一键四门关")
    @pytest.mark.full
    def test_caseid_1990761(self):
        self.set_door_sts(DoorId.kDoorAll,DoorStatus.kOpened)
        sleep(0.5)
        execid = self.tsp.rvc_door_control(DoorCode.All_door,2)
        execid = self.tsp.rvc_door_control(DoorCode.All_door,2)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_车内有人_单个门开与关门闭锁")
    @pytest.mark.smoke
    def test_caseid_1990762(self):
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        for doorcode in DoorCode:
            # 1. 设置基础状态
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kOpened)
            if doorcode == DoorCode.All_door:
                continue
            # 2. 启动线程，执行主驾门开流程
            t1 = threading.Thread(target=self.normal_process_open, args=(doorcode,LockStatus.Unlocked,True))
            t1.start()
            # 3. 同步监控关门闭锁指令
            execid = self.tsp.rvc_lock_control(3)
            self.soa.check_Play2_req(app='RVC',txt='关门请当心',param='{"isLoopPlay":False,"priority":1,"streamType":6,"zone":0}',timeout=10)
            self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Hmi,find_key_type=FindKeyType.NoReq,timeout=10)	
            sleep(10)
            assert self.tsp.log_search_remote_vehicle_control("DoorCloseFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"        
            t1.join()
            self.SetDoorCloseLock_req_num = 0
            assert not self.error, self.error_msg
            self.soa.empty_all()

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_车内有人_一键四门开与关门闭锁")
    @pytest.mark.smoke
    def test_caseid_1990763(self):
        # 1. 设置基础状态
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kOpened)
        # 2. 启动线程，执行主驾门开流程
        t1 = threading.Thread(target=self.normal_process_open, args=(DoorCode.All_door,LockStatus.Unlocked,True))
        t1.start()
        # 3. 同步监控关门闭锁指令
        execid = self.tsp.rvc_lock_control(3)
        self.soa.check_Play2_req(app='RVC',txt='关门请当心',param='{"isLoopPlay":False,"priority":1,"streamType":6,"zone":0}',timeout=10)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Hmi,find_key_type=FindKeyType.NoReq,timeout=10)	
        sleep(10)
        assert self.tsp.log_search_remote_vehicle_control("DoorCloseFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"        
        t1.join()
        assert not self.error, self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_车内有人_单个门开与远程解锁")
    @pytest.mark.smoke
    def test_caseid_1990764(self):
        # 1. 设置基础状态
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        for doorcode in DoorCode:
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kClosed)
            if doorcode == DoorCode.All_door:
                continue
            # 2. 启动线程，执行主驾门开流程
            t1 = threading.Thread(target=self.normal_process_open, args=(doorcode,LockStatus.AllLocked,True))
            t1.start()
            # 3. 同步监控远程解锁指令
            execid = self.tsp.rvc_lock_control(1)
            # self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, timeout=20)  # 无法同时检测
            self.soa.check_NotifyRVCLockInfo_event(timeout=20)
            assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
            t1.join()
            self.SetDoorCloseLock_req_num = 0
            assert not self.error, self.error_msg
            self.soa.empty_all()

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_车内有人_单个门开与远程闭锁")
    @pytest.mark.smoke
    def test_caseid_1990765(self):
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        for doorcode in DoorCode:
            # 1. 设置基础状态
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kClosed)
            if doorcode == DoorCode.All_door:
                continue
            # 2. 启动线程，执行主驾门开流程
            t1 = threading.Thread(target=self.normal_process_open, args=(doorcode,LockStatus.Unlocked,True))
            t1.start()
            # 3. 同步监控远程闭锁指令
            execid = self.tsp.rvc_lock_control(2)
            self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi, find_key_type=FindKeyType.NoReq, timeout=10)
            assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
            t1.join()
            self.SetDoorCloseLock_req_num = 0
            assert not self.error, self.error_msg
            self.soa.empty_all()

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_车内有人_单个门关与远程关门闭锁")
    @pytest.mark.smoke
    def test_caseid_1990766(self):
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        for doorcode in DoorCode:
            # 1. 设置基础状态
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kOpened)
            if doorcode == DoorCode.All_door:
                continue
            # 2. 启动线程，执行主驾门开流程
            t1 = threading.Thread(target=self.normal_process_close, args=(doorcode,False))
            t1.start()
            # 3. 同步监控远程关门闭锁指令
            execid = self.tsp.rvc_lock_control(3)
            self.soa.check_Play2_req(app='RVC',txt='关门请当心',param='{"isLoopPlay":False,"priority":1,"streamType":6,"zone":0}',timeout=10)
            self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Hmi,find_key_type=FindKeyType.NoReq,timeout=10)	
            self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
            assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    
            t1.join()
            self.SetDoorCloseLock_req_num = 0
            assert not self.error, self.error_msg
            self.soa.empty_all()

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_车内有人_一键四门开与远程闭锁")
    @pytest.mark.smoke
    def test_caseid_1990767(self):
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        # 1. 设置基础状态
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kClosed)

        # 2. 启动线程，执行主驾门开流程
        t1 = threading.Thread(target=self.normal_process_open, args=(DoorCode.All_door,LockStatus.Unlocked,True))
        t1.start()
        # 3. 同步监控远程闭锁指令
        execid = self.tsp.rvc_lock_control(2)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi, find_key_type=FindKeyType.NoReq, timeout=10)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        t1.join()
        assert not self.error, self.error_msg
        self.soa.empty_all()

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_车内有人_一键四门开与远程解锁")
    @pytest.mark.smoke
    def test_caseid_1990768(self):
        # 1. 设置基础状态
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kClosed)

        # 2. 启动线程，执行主驾门开流程
        t1 = threading.Thread(target=self.normal_process_open, args=(DoorCode.All_door,LockStatus.AllLocked,True))
        t1.start()
        # 3. 同步监控远程解锁指令
        execid = self.tsp.rvc_lock_control(1)
        # self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, timeout=20)  # 无法同时检测
        self.soa.check_NotifyRVCLockInfo_event(timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
        t1.join()
        assert not self.error, self.error_msg
        self.soa.empty_all()

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_车内有人_一键四门关与关门闭锁")
    @pytest.mark.smoke
    def test_caseid_1990769(self):
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        # 1. 设置基础状态
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kOpened)

        # 2. 启动线程，执行主驾门开流程
        t1 = threading.Thread(target=self.normal_process_close, args=(DoorCode.All_door,True))
        t1.start()
        # 3. 同步监控远程关门闭锁指令
        execid = self.tsp.rvc_lock_control(3)
        self.soa.check_Play2_req(app='RVC',txt='关门请当心',param='{"isLoopPlay":False,"priority":1,"streamType":6,"zone":0}',timeout=10)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Hmi,find_key_type=FindKeyType.NoReq,timeout=10)	
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    
        t1.join()
        assert not self.error, self.error_msg
        self.soa.empty_all()

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_车内无人_单个门开与关门闭锁")
    @pytest.mark.full
    def test_caseid_1990770(self):
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
        for doorcode in DoorCode:
            # 1. 设置基础状态
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kClosed)
            if doorcode == DoorCode.All_door:
                continue
            # 2. 启动线程，执行主驾门开流程
            t1 = threading.Thread(target=self.normal_process_open, args=(doorcode,LockStatus.Unlocked,False))
            t1.start()
            # 3. 同步监控关门闭锁指令
            execid = self.tsp.rvc_lock_control(3)
            self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)	
            sleep(10)
            assert self.tsp.log_search_remote_vehicle_control("DoorCloseFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"        
            t1.join()
            self.SetDoorCloseLock_req_num = 0
            assert not self.error, self.error_msg
            self.soa.empty_all()

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_车内无人_单个门开与远程解锁")
    @pytest.mark.full
    def test_caseid_1990771(self):
        # 1. 设置基础状态
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
        for doorcode in DoorCode:
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kClosed)
            if doorcode == DoorCode.All_door:
                continue
            # 2. 启动线程，执行主驾门开流程
            t1 = threading.Thread(target=self.normal_process_open, args=(doorcode,LockStatus.AllLocked,False))
            t1.start()
            # 3. 同步监控远程解锁指令
            execid = self.tsp.rvc_lock_control(1)
            # self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, timeout=20)  # 无法同时检测
            self.soa.check_NotifyRVCLockInfo_event(timeout=20)
            assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
            t1.join()
            self.SetDoorCloseLock_req_num = 0
            assert not self.error, self.error_msg
            self.soa.empty_all()

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_车内无人_单个门开与远程闭锁")
    @pytest.mark.full
    def test_caseid_1990772(self):
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
        for doorcode in DoorCode:
            # 1. 设置基础状态
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kClosed)
            if doorcode == DoorCode.All_door:
                continue
            # 2. 启动线程，执行主驾门开流程
            t1 = threading.Thread(target=self.normal_process_open, args=(doorcode,LockStatus.Unlocked,False))
            t1.start()
            # 3. 同步监控远程闭锁指令
            execid = self.tsp.rvc_lock_control(2)
            self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=10)
            assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
            t1.join()
            self.SetDoorCloseLock_req_num = 0
            assert not self.error, self.error_msg
            self.soa.empty_all()

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_车内无人_单个门关与远程关门闭锁")
    @pytest.mark.full
    def test_caseid_1990773(self):
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
        for doorcode in DoorCode:
            # 1. 设置基础状态
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kOpened)
            if doorcode == DoorCode.All_door:
                continue
            # 2. 启动线程，执行主驾门开流程
            t1 = threading.Thread(target=self.normal_process_close, args=(doorcode,False))
            t1.start()
            # 3. 同步监控远程关门闭锁指令
            execid = self.tsp.rvc_lock_control(3)
            self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)	
            self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
            assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    
            t1.join()
            self.SetDoorCloseLock_req_num = 0
            assert not self.error, self.error_msg
            self.soa.empty_all()

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_车内无人_一键四门开与关门闭锁")
    @pytest.mark.sanity
    def test_caseid_1990774(self):
        # 1. 设置基础状态
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
        self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kClosed)
        # 2. 启动线程，执行主驾门开流程
        t1 = threading.Thread(target=self.normal_process_open, args=(DoorCode.All_door,LockStatus.Unlocked,False))
        t1.start()
        # 3. 同步监控关门闭锁指令
        execid = self.tsp.rvc_lock_control(3)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.AllDoorCloseAndLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)	
        sleep(10)
        assert self.tsp.log_search_remote_vehicle_control("DoorCloseFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"        
        t1.join()
        assert not self.error, self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_车内无人_一键四门开与远程闭锁")
    @pytest.mark.full
    def test_caseid_1990775(self):
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
        # 1. 设置基础状态
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kClosed)

        # 2. 启动线程，执行主驾门开流程
        t1 = threading.Thread(target=self.normal_process_open, args=(DoorCode.All_door,LockStatus.Unlocked,False))
        t1.start()
        # 3. 同步监控远程闭锁指令
        execid = self.tsp.rvc_lock_control(2)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=10)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        t1.join()
        assert not self.error, self.error_msg
        self.soa.empty_all()

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_车内无人_一键四门开与远程解锁")
    @pytest.mark.full
    def test_caseid_1990776(self):
        # 1. 设置基础状态
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kClosed)

        # 2. 启动线程，执行主驾门开流程
        t1 = threading.Thread(target=self.normal_process_open, args=(DoorCode.All_door,LockStatus.AllLocked,False))
        t1.start()
        # 3. 同步监控远程解锁指令
        execid = self.tsp.rvc_lock_control(1)
        # self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, timeout=20)  # 无法同时检测
        self.soa.check_NotifyRVCLockInfo_event(timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
        t1.join()
        assert not self.error, self.error_msg
        self.soa.empty_all()

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_车内无人_一键四门关与关门闭锁")
    @pytest.mark.full
    def test_caseid_1990777(self):
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
        # 1. 设置基础状态
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kOpened)

        # 2. 启动线程，执行主驾门开流程
        t1 = threading.Thread(target=self.normal_process_close, args=(DoorCode.All_door,False))
        t1.start()
        # 3. 同步监控远程关门闭锁指令
        execid = self.tsp.rvc_lock_control(3)
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=10)	
        self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    
        t1.join()
        assert not self.error, self.error_msg
        self.soa.empty_all()

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_闭锁状态_车内无人_任意车门开的排列组合")
    @pytest.mark.smoke
    def test_caseid_1990778(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        thread_list = []
        two_combinations = list(itertools.combinations(four_doorcode, 2))
        three_combinations = list(itertools.combinations(four_doorcode, 3))
        combinations = two_combinations + three_combinations + [four_doorcode]
        for combination in combinations:
            logger.info(f'测试的组合是{combination}')
            # 1. 设置基础状态
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_LockStatus(lock_sts=LockStatus.Undef)
            self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kClosed)
            # 2. 启动线程，执行主驾门开流程
            for doorcode in combination:
                t1 = threading.Thread(target=self.normal_process_open, args=(doorcode,LockStatus.Undef,False))
                t1.start()
                thread_list.append(t1)
                sleep(1)
            for thread in thread_list:
                thread.join()
            self.SetDoorCloseLock_req_num = 0
            assert not self.error,self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_闭锁状态_车内有人_任意车门开的排列组合")
    @pytest.mark.sanity
    def test_caseid_1990779(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        thread_list = []
        two_combinations = list(itertools.combinations(four_doorcode, 2))
        three_combinations = list(itertools.combinations(four_doorcode, 3))
        combinations = two_combinations + three_combinations + [four_doorcode]
        for combination in combinations:
            logger.info(f'测试的组合是{combination}')
            # 1. 设置基础状态
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kClosed)
            # 2. 启动线程，执行主驾门开流程
            for doorcode in combination:
                t1 = threading.Thread(target=self.normal_process_open, args=(doorcode,LockStatus.AllLocked,True))
                t1.start()
                thread_list.append(t1)
                sleep(1)
            for thread in thread_list:
                thread.join()
            self.SetDoorCloseLock_req_num = 0
            assert not self.error,self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_闭锁状态_车内有人_一键四门开与任意数量单门开")
    @pytest.mark.full
    def test_caseid_1990780(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        thread_list = []
        one_combinations = list(itertools.combinations(four_doorcode, 1))
        two_combinations = list(itertools.combinations(four_doorcode, 2))
        three_combinations = list(itertools.combinations(four_doorcode, 3))
        combinations = one_combinations+ two_combinations + three_combinations + [four_doorcode]
        for combination in combinations:
            logger.info(f'测试的组合是{combination}')
            # 1. 设置基础状态
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kClosed)
            # 2. 启动线程
            t1 = threading.Thread(target=self.normal_process_open, args=(DoorCode.All_door,LockStatus.AllLocked,True))
            t1.start()
            thread_list.append(t1)
            sleep(1)
            for doorcode in combination:
                t1 = threading.Thread(target=self.normal_process_open, args=(doorcode,LockStatus.AllLocked,True))
                t1.start()
                thread_list.append(t1)
                sleep(1)
            for thread in thread_list:
                thread.join()
            self.SetDoorCloseLock_req_num = 0
            assert not self.error,self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_闭锁状态_车内无人_一键四门开与任意数量单门开")
    @pytest.mark.full
    def test_caseid_1990781(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        thread_list = []
        one_combinations = list(itertools.combinations(four_doorcode, 1))
        two_combinations = list(itertools.combinations(four_doorcode, 2))
        three_combinations = list(itertools.combinations(four_doorcode, 3))
        combinations = one_combinations+ two_combinations + three_combinations + [four_doorcode]
        for combination in combinations:
            logger.info(f'测试的组合是{combination}')
            # 1. 设置基础状态
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kClosed)
            # 2. 启动线程
            t1 = threading.Thread(target=self.normal_process_open, args=(DoorCode.All_door,LockStatus.AllLocked,False))
            t1.start()
            thread_list.append(t1)
            sleep(1)
            for doorcode in combination:
                t1 = threading.Thread(target=self.normal_process_open, args=(doorcode,LockStatus.AllLocked,False))
                t1.start()
                thread_list.append(t1)
                sleep(1)
            for thread in thread_list:
                thread.join()
            self.SetDoorCloseLock_req_num = 0
            assert not self.error,self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_解锁状态_车内无人_任意车门开的排列组合")
    @pytest.mark.smoke
    def test_caseid_1990782(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        thread_list = []
        two_combinations = list(itertools.combinations(four_doorcode, 2))
        three_combinations = list(itertools.combinations(four_doorcode, 3))
        combinations = two_combinations + three_combinations + [four_doorcode]
        for combination in combinations:
            logger.info(f'测试的组合是{combination}')
            # 1. 设置基础状态
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kClosed)
            # 2. 启动线程，执行主驾门开流程
            for doorcode in combination:
                t1 = threading.Thread(target=self.normal_process_open, args=(doorcode,LockStatus.Unlocked,False))
                t1.start()
                thread_list.append(t1)
                sleep(1)
            for thread in thread_list:
                thread.join()
            self.SetDoorCloseLock_req_num = 0
            assert not self.error,self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_解锁状态_车内有人_任意车门开的排列组合")
    @pytest.mark.full
    def test_caseid_1990783(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        thread_list = []
        two_combinations = list(itertools.combinations(four_doorcode, 2))
        three_combinations = list(itertools.combinations(four_doorcode, 3))
        combinations = two_combinations + three_combinations + [four_doorcode]
        for combination in combinations:
            logger.info(f'测试的组合是{combination}')
            # 1. 设置基础状态
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kClosed)
            # 2. 启动线程，执行主驾门开流程
            for doorcode in combination:
                t1 = threading.Thread(target=self.normal_process_open, args=(doorcode,LockStatus.Unlocked,True))
                t1.start()
                thread_list.append(t1)
                sleep(1)
            for thread in thread_list:
                thread.join()
            self.SetDoorCloseLock_req_num = 0
            assert not self.error,self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_解锁状态_车内无人_任意车门关的排列组合")
    @pytest.mark.full
    def test_caseid_1990784(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取组合列表
        thread_list = []
        two_combinations = list(itertools.combinations(four_doorcode, 2))
        three_combinations = list(itertools.combinations(four_doorcode, 3))
        combinations = two_combinations + three_combinations + [four_doorcode]
        for combination in combinations:
            logger.info(f'测试的组合是{combination}')
            # 1. 设置基础状态
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kOpened)
            # 2. 启动线程
            for doorcode in combination:
                t1 = threading.Thread(target=self.normal_process_close, args=(doorcode,False))
                t1.start()
                thread_list.append(t1)
                sleep(1)
            for thread in thread_list:
                thread.join()
            self.SetDoorCloseLock_req_num = 0
            assert not self.error,self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_解锁状态_车内有人_任意车门关的排列组合")
    @pytest.mark.full
    def test_caseid_1990785(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取组合列表
        thread_list = []
        two_combinations = list(itertools.combinations(four_doorcode, 2))
        three_combinations = list(itertools.combinations(four_doorcode, 3))
        combinations = two_combinations + three_combinations + [four_doorcode]
        for combination in combinations:
            logger.info(f'测试的组合是{combination}')
            # 1. 设置基础状态
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kOpened)
            # 2. 启动线程
            for doorcode in combination:
                t1 = threading.Thread(target=self.normal_process_close, args=(doorcode,True))
                t1.start()
                thread_list.append(t1)
                sleep(1)
            for thread in thread_list:
                thread.join()
            self.SetDoorCloseLock_req_num = 0
            assert not self.error,self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_解锁状态_任意车门关与开的排列组合")
    @pytest.mark.full
    def test_caseid_1990786(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取组合列表 q
        thread_list = []
        # 1. 设置基础状态
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kClosed)
        # 2. 启动线程
        for i,doorcode in enumerate(four_doorcode):
            if i == 0:
                t1 = threading.Thread(target=self.normal_process_open, args=(doorcode,LockStatus.Unlocked,False))
                t1.start()
                thread_list.append(t1)
                sleep(1)
            else:
                t1 = threading.Thread(target=self.normal_process_close, args=(doorcode,False))
                t1.start()
                thread_list.append(t1)
                sleep(1)
        for thread in thread_list:
            thread.join()
        self.SetDoorCloseLock_req_num = 0
        assert not self.error,self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_解锁状态_一键四门开与任意数量单门开")
    @pytest.mark.smoke
    def test_caseid_1990787(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        thread_list = []
        one_combinations = list(itertools.combinations(four_doorcode, 1))
        two_combinations = list(itertools.combinations(four_doorcode, 2))
        three_combinations = list(itertools.combinations(four_doorcode, 3))
        combinations = one_combinations+ two_combinations + three_combinations + [four_doorcode]
        for combination in combinations:
            logger.info(f'测试的组合是{combination}')
            # 1. 设置基础状态
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            self.set_door_sts(doorid=DoorId.kDoorAll,sts=DoorStatus.kClosed)
            # 2. 启动线程
            t1 = threading.Thread(target=self.normal_process_open, args=(DoorCode.All_door,LockStatus.Unlocked,False))
            t1.start()
            thread_list.append(t1)
            sleep(1)
            for doorcode in combination:
                t1 = threading.Thread(target=self.normal_process_open, args=(doorcode,LockStatus.Unlocked,False))
                t1.start()
                thread_list.append(t1)
                sleep(1)
            for thread in thread_list:
                thread.join()
            self.SetDoorCloseLock_req_num = 0
            assert not self.error,self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_解锁状态_一键四门开与任意数量单门关_关闭车门")
    @pytest.mark.full
    def test_caseid_1990788(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        thread_list = []
        one_combinations = list(itertools.combinations(four_doorcode, 1))
        two_combinations = list(itertools.combinations(four_doorcode, 2))
        three_combinations = list(itertools.combinations(four_doorcode, 3))
        combinations = one_combinations+ two_combinations + three_combinations + [four_doorcode]
        for combination in combinations:
            logger.info(f'测试的组合是{combination}')
            # 1. 设置基础状态
            four_error_num = len(combination)
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            for doorcode in combination:
                t1 = threading.Thread(target=self.normal_process_close, args=(doorcode,True))
                t1.start()
                thread_list.append(t1)
                sleep(1)
            four_execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)
            for thread in thread_list:
                thread.join()
            assert self.tsp.log_search_remote_vehicle_control(f"{four_error_num}DoorNotOpened",execid=four_execid),f"TCAM远程控制上报到车云的结果校验失败"
            self.SetDoorCloseLock_req_num = 0
            assert not self.error,self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_解锁状态_一键四门关与任意数量单门关")
    @pytest.mark.full
    def test_caseid_1990790(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        thread_list = []
        one_combinations = list(itertools.combinations(four_doorcode, 1))
        two_combinations = list(itertools.combinations(four_doorcode, 2))
        three_combinations = list(itertools.combinations(four_doorcode, 3))
        combinations = one_combinations+ two_combinations + three_combinations + [four_doorcode]
        for combination in combinations:
            logger.info(f'测试的组合是{combination}')
            # 1. 设置基础状态
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            t1 = threading.Thread(target=self.normal_process_close, args=(DoorCode.All_door,True))
            t1.start()
            thread_list.append(t1)
            sleep(1)
            for doorcode in combination:
                t1 = threading.Thread(target=self.normal_process_close, args=(doorcode,True))
                t1.start()
                thread_list.append(t1)
                sleep(1)
            for thread in thread_list:
                thread.join()
            self.SetDoorCloseLock_req_num = 0
            assert not self.error,self.error_msg

    @allure.title("电动门控制-RVC_电动门控制_不相同指令下发_解锁状态_一键四门关与任意数量单门开_对应车门开")
    @pytest.mark.full
    def test_caseid_1990792(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        thread_list = []
        one_combinations = list(itertools.combinations(four_doorcode, 1))
        two_combinations = list(itertools.combinations(four_doorcode, 2))
        three_combinations = list(itertools.combinations(four_doorcode, 3))
        combinations = one_combinations+ two_combinations + three_combinations + [four_doorcode]
        for combination in combinations:
            logger.info(f'测试的组合是{combination}')
            # 1. 设置基础状态
            four_error_num = len(combination)
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            for doorcode in combination:
                t1 = threading.Thread(target=self.normal_process_open, args=(doorcode,LockStatus.Unlocked,True))
                t1.start()
                thread_list.append(t1)
                sleep(1)
            four_execid = self.normal_process_close_error(DoorCode.All_door,True)
            for thread in thread_list:
                thread.join()
            assert self.tsp.log_search_remote_vehicle_control(f"{four_error_num}DoorNotClosed",execid=four_execid),f"TCAM远程控制上报到车云的结果校验失败"
            self.SetDoorCloseLock_req_num = 0
            assert not self.error,self.error_msg


    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内无人_单车门开_kOpened")
    @pytest.mark.smoke
    def test_caseid_1990793(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.FourDoorLockedTailUnlocked)
            execid = self.normal_process_open_error(doorcode,LockStatus.FourDoorLockedTailUnlocked,False)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kOpened)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内无人_单车门开_kHover")
    @pytest.mark.sanity
    def test_caseid_1990794(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            execid = self.normal_process_open_error(doorcode,LockStatus.AllLocked,False)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kHover)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内无人_单车门开_门异常_kFaultPlayProtectionActive")
    @pytest.mark.full
    def test_caseid_1990795(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Undef)
            execid = self.normal_process_open_error(doorcode,LockStatus.Undef,False)
            self.soa.notify_DoorFault({self.door_code_id[doorcode]: DoorfFultSts.FaultPlayProtectionActive})
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"PlayProtcn",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内无人_单车门开_门异常_kThermalProtection")
    @pytest.mark.full
    def test_caseid_1990796(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            execid = self.normal_process_open_error(doorcode,LockStatus.AllLocked,False)
            self.soa.notify_DoorFault({self.door_code_id[doorcode]: DoorfFultSts.ThermalProtection})
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"ThermProtcn",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内无人_单车门开_门异常_kRollAngleAbnormal")
    @pytest.mark.full
    def test_caseid_1990797(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            execid = self.normal_process_open_error(doorcode,LockStatus.AllLocked,False)
            self.soa.notify_DoorFault({self.door_code_id[doorcode]: DoorfFultSts.RollAngleAbnormal})
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"RollAgAbnorm",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内无人_单车门开_门异常_kRoadInclinationAbnormal")
    @pytest.mark.full
    def test_caseid_1990798(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            execid = self.normal_process_open_error(doorcode,LockStatus.AllLocked,False)
            self.soa.notify_DoorFault({self.door_code_id[doorcode]: DoorfFultSts.RoadInclinationAbnormal})
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"RoadInclnAbnorm",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内无人_单车门开_门异常_kHallSensorsError")
    @pytest.mark.smoke
    def test_caseid_1990799(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            execid = self.normal_process_open_error(doorcode,LockStatus.AllLocked,False)
            self.soa.notify_DoorFault({self.door_code_id[doorcode]: DoorfFultSts.HallSensorsError})
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"HallSnsrErr",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内无人_单车门开_开门超时_Closing")
    @pytest.mark.full
    def test_caseid_1990800(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            execid = self.normal_process_open_error(doorcode,LockStatus.AllLocked,False)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kClosing)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"DoorClosing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内无人_单车门开_开门超时_kClosed")
    @pytest.mark.full
    def test_caseid_1990801(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            execid = self.normal_process_open_error(doorcode,LockStatus.AllLocked,False)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kClosed)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"DoorClosed",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内无人_单车门开_开门超时_kLocked")
    @pytest.mark.full
    def test_caseid_1990802(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            execid = self.normal_process_open_error(doorcode,LockStatus.AllLocked,False)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kLocked)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"DoorLocked",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内无人_单车门开_开门超时_kUnlocked")
    @pytest.mark.full
    def test_caseid_1990803(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            execid = self.normal_process_open_error(doorcode,LockStatus.AllLocked,False)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kUnlocked)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"DoorUnlocked",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内无人_单车门开_开门超时_kOpening")
    @pytest.mark.full
    def test_caseid_1990804(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            execid = self.normal_process_open_error(doorcode,LockStatus.AllLocked,False)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kOpening)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"DoorOpening",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内无人_单车门开_开门超时_kClosingBreak")
    @pytest.mark.full
    def test_caseid_1990806(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            execid = self.normal_process_open_error(doorcode,LockStatus.AllLocked,False)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kClosingBreak)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"DoorClosingBreak",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内无人_单车门开_开门超时_kOpeningBreak")
    @pytest.mark.full
    def test_caseid_1990807(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            execid = self.normal_process_open_error(doorcode,LockStatus.AllLocked,False)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kOpeningBreak)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"DoorOpeningBreak",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内无人_单车门开_开门超时_HalfClosed")
    @pytest.mark.full
    def test_caseid_1990808(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            execid = self.normal_process_open_error(doorcode,LockStatus.AllLocked,False)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kHalfClosed)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"DoorHalfClosed",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内无人_单车门开_开门超时_HalfClosed")
    @pytest.mark.smoke
    def test_caseid_1990809(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            execid = self.normal_process_open_error(doorcode,LockStatus.AllLocked,False,True)
            self.SetDoorCloseLock_req_num = 0

    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内有人_单车门开_kOpened")
    @pytest.mark.smoke
    def test_caseid_1990810(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            execid = self.normal_process_open_error(doorcode,LockStatus.AllLocked,True)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kOpened)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内无人_单车门开_非对应门异常_成功")
    @pytest.mark.full
    def test_caseid_1990811(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            execid = self.normal_process_open_error(doorcode,LockStatus.AllLocked,False)
            # 取出不等于当前门的值
            result = next((value for key, value in self.door_code_id.items() if key != doorcode), None)
            self.soa.notify_DoorFault({result: DoorfFultSts.RoadInclinationAbnormal})

            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kOpened)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内无人_单车门开_非对应门异常_超时")
    @pytest.mark.full
    def test_caseid_1990812(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            execid = self.normal_process_open_error(doorcode,LockStatus.AllLocked,False)
            # 取出不等于当前门的值
            result = next((value for key, value in self.door_code_id.items() if key != doorcode), None)
            self.soa.notify_DoorFault({result: DoorfFultSts.RoadInclinationAbnormal})

            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kOpening)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"DoorOpening",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内无人_单车门开_非对应门异常_对应门异常")
    @pytest.mark.full
    def test_caseid_1990813(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            execid = self.normal_process_open_error(doorcode,LockStatus.AllLocked,False)
            # 取出不等于当前门的值
            result = next((value for key, value in self.door_code_id.items() if key != doorcode), None)
            self.soa.notify_DoorFault({result: DoorfFultSts.HallSensorsError,self.door_code_id[doorcode]: DoorfFultSts.HallSensorsError})

            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"HallSnsrErr",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内无人_单车门开_多门异常后对应门开")
    @pytest.mark.full
    def test_caseid_1990814(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
            execid = self.normal_process_open_error(doorcode,LockStatus.AllLocked,False)
            # 取出不等于当前门的值
            result = next((value for key, value in self.door_code_id.items() if key != doorcode), None)
            self.soa.notify_DoorFault({result: DoorfFultSts.HallSensorsError,self.door_code_id[doorcode]: DoorfFultSts.HallSensorsError})
            sleep(8)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kOpened)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"HallSnsrErr",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内无人_单车门开_kOpened")
    @pytest.mark.smoke
    def test_caseid_1990815(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            execid = self.normal_process_open_error(doorcode,LockStatus.Unlocked,False)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kOpened)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_单车门开_kOpened")
    @pytest.mark.sanity
    def test_caseid_1990816(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            execid = self.normal_process_open_error(doorcode,LockStatus.Unlocked,True)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kOpened)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_单车门关_kClosed")
    @pytest.mark.smoke
    def test_caseid_1990817(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            execid = self.normal_process_close_error(doorcode,True)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kClosed)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_单车门关_kClosed")
    @pytest.mark.full
    def test_caseid_1990819(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            execid = self.normal_process_close_error(doorcode,True)
            # 取非对应门
            result = next((value for key, value in self.door_code_id.items() if key != doorcode), None)
            self.soa.notify_DoorFault({result: DoorfFultSts.HallSensorsError,})

            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kClosed)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_单车门关_门故障_kFaultPlayProtectionActive")
    @pytest.mark.smoke
    def test_caseid_1990820(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            execid = self.normal_process_close_error(doorcode,True)

            self.soa.notify_DoorFault({self.door_code_id[doorcode]: DoorfFultSts.FaultPlayProtectionActive,})

            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"PlayProtcn",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_单车门关_门故障_kThermalProtection")
    @pytest.mark.full
    def test_caseid_1990821(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            execid = self.normal_process_close_error(doorcode,True)

            self.soa.notify_DoorFault({self.door_code_id[doorcode]: DoorfFultSts.ThermalProtection,})

            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"ThermProtcn",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_单车门关_门故障_RollAgAbnorm")
    @pytest.mark.full
    def test_caseid_1990822(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            execid = self.normal_process_close_error(doorcode,True)

            self.soa.notify_DoorFault({self.door_code_id[doorcode]: DoorfFultSts.RollAngleAbnormal,})

            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"RollAgAbnorm",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_单车门关_门故障_kRoadInclinationAbnormal")
    @pytest.mark.full
    def test_caseid_1990823(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            execid = self.normal_process_close_error(doorcode,True)

            self.soa.notify_DoorFault({self.door_code_id[doorcode]: DoorfFultSts.RoadInclinationAbnormal,})

            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"RoadInclnAbnorm",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_单车门关_门故障_kHallSensorsError")
    @pytest.mark.full
    def test_caseid_1990824(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            execid = self.normal_process_close_error(doorcode,True)

            self.soa.notify_DoorFault({self.door_code_id[doorcode]: DoorfFultSts.HallSensorsError,})

            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"HallSnsrErr",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_单车门关_门错误_kCloseDoorFail")
    @pytest.mark.smoke
    def test_caseid_1990825(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            execid = self.normal_process_close_error(doorcode,True)
            self.soa.notify_NotifyLockWarning()
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"DoorAgSmall",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_单车门关_门故障后门错误")
    @pytest.mark.full
    def test_caseid_1990826(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            execid = self.normal_process_close_error(doorcode,True)

            self.soa.notify_DoorFault({self.door_code_id[doorcode]: DoorfFultSts.FaultPlayProtectionActive,})
            sleep(2)
            self.soa.notify_NotifyLockWarning()
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"PlayProtcn",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_单车门关_门故障后门错误")
    @pytest.mark.full
    def test_caseid_1990827(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            execid = self.normal_process_close_error(doorcode,True)
            self.soa.notify_NotifyLockWarning()
            
            sleep(2)
            self.soa.notify_DoorFault({self.door_code_id[doorcode]: DoorfFultSts.FaultPlayProtectionActive,})
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"DoorAgSmall",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_单车门关_关门超时_Opened")
    @allure.issue('https://jira.jiduauto.com/browse/SOA-29356?filter=-2')
    @pytest.mark.smoke
    def test_caseid_1990828(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            execid = self.normal_process_close_error(doorcode,True)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kOpened)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"DoorOpened",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_单车门关_关门超时_Closing")
    @pytest.mark.full
    def test_caseid_1990829(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            execid = self.normal_process_close_error(doorcode,True)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kClosing)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"DoorClosing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_单车门关_关门超时_kLocked")
    @pytest.mark.full
    def test_caseid_1990830(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            execid = self.normal_process_close_error(doorcode,True)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kLocked)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"DoorLocked",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_单车门关_关门超时_kUnlocked")
    @pytest.mark.full
    def test_caseid_1990831(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            execid = self.normal_process_close_error(doorcode,True)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kUnlocked)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"DoorUnlocked",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_单车门关_关门超时_Opening")
    @pytest.mark.full
    def test_caseid_1990832(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            execid = self.normal_process_close_error(doorcode,True)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kOpening)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"DoorOpening",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_单车门关_关门超时_Hover")
    @allure.issue('https://jira.jiduauto.com/browse/SOA-29356?filter=-2')
    @pytest.mark.full
    def test_caseid_1990833(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            execid = self.normal_process_close_error(doorcode,True)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kHover)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"DoorHover",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_单车门关_关门超时_OpeningBreak")
    @pytest.mark.full
    def test_caseid_1990834(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            execid = self.normal_process_close_error(doorcode,True)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kOpeningBreak)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"DoorOpeningBreak",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_单车门关_关门超时_HalfClosed")
    @pytest.mark.full
    def test_caseid_1990835(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            execid = self.normal_process_close_error(doorcode,True)
            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kHalfClosed)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"DoorHalfClosed",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_单车门关_关门超时_非对应门报故障_HalfClosed")
    @pytest.mark.full
    def test_caseid_1990836(self):
        four_doorcode = [DoorCode.driver_door_control,DoorCode.passenger_door_control,DoorCode.rear_left_door_control,DoorCode.rear_right_door_control]
        # 获取2个门开时的组合列表
        for doorcode in four_doorcode:
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
            execid = self.normal_process_close_error(doorcode,True)
            # 取出不等于当前门的值
            result = next((value for key, value in self.door_code_id.items() if key != doorcode), None)
            self.soa.notify_DoorFault({result: DoorfFultSts.FaultPlayProtectionActive})

            self.set_door_sts(self.door_code_id[doorcode], DoorStatus.kHalfClosed)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"DoorHalfClosed",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_一键四门开_kOpened")
    @pytest.mark.smoke
    def test_caseid_1990838(self):
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)

        self.set_door_sts(self.door_code_id[DoorCode.All_door], DoorStatus.kOpened)
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_一键四门开_kHover")
    @pytest.mark.full
    def test_caseid_1990839(self):
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)

        self.set_door_sts(self.door_code_id[DoorCode.All_door], DoorStatus.kHover)
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_一键四门开_一门异常_kFaultPlayProtectionActive")
    @pytest.mark.smoke
    def test_caseid_1990840(self):
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.FaultPlayProtectionActive,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"PlayProtcn",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_一键四门开_一门异常_kThermalProtection")
    @pytest.mark.full
    def test_caseid_1990841(self):
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.ThermalProtection,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"ThermProtcn",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_一键四门开_一门异常_kRollAngleAbnormal")
    @pytest.mark.full
    def test_caseid_1990842(self):
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.RollAngleAbnormal,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"RollAgAbnorm",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_一键四门开_一门异常_kRoadInclinationAbnormal")
    @pytest.mark.full
    def test_caseid_1990843(self):
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.RoadInclinationAbnormal,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"RoadInclnAbnorm",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_一键四门开_一门异常_kHallSensorsError")
    @pytest.mark.full
    def test_caseid_1990844(self):
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)
        self.soa.notify_DoorFault({DoorId.kDoorRearRight: DoorfFultSts.HallSensorsError,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorFrontLeft: DoorfFultSts.OK,})
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"HallSnsrErr",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_一键四门开_两门异常_异常自动排列组合")
    @pytest.mark.full
    def test_caseid_1990845(self):
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)
        self.soa.notify_DoorFault({DoorId.kDoorRearRight: DoorfFultSts.HallSensorsError,DoorId.kDoorFrontLeft: DoorfFultSts.RoadInclinationAbnormal,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorFrontLeft: DoorfFultSts.OK,})
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"HallSnsrErr",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_一键四门开_三门异常_异常自动排列组合")
    @pytest.mark.full
    def test_caseid_1990846(self):
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)
        self.soa.notify_DoorFault({DoorId.kDoorRearLeft: DoorfFultSts.HallSensorsError,DoorId.kDoorFrontLeft: DoorfFultSts.RoadInclinationAbnormal,DoorId.kDoorFrontLeft: DoorfFultSts.RollAngleAbnormal,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"HallSnsrErr",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_一键四门开_四门异常_异常自动排列组合")
    @pytest.mark.sanity
    def test_caseid_1990847(self):
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)
        self.soa.notify_DoorFault({DoorId.kDoorRearLeft: DoorfFultSts.HallSensorsError,DoorId.kDoorFrontLeft: DoorfFultSts.RoadInclinationAbnormal,DoorId.kDoorFrontLeft: DoorfFultSts.RollAngleAbnormal,DoorId.kDoorRearRight: DoorfFultSts.RoadInclinationAbnormal,})
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"HallSnsrErr",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_一键四门开_任意一门超时_Closing")
    @pytest.mark.sanity
    def test_caseid_1990848(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 1))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kClosing)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kOpened)

            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"1DoorNotOpened",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_一键四门开_任意一门超时_kClosed")
    @pytest.mark.sanity
    def test_caseid_1990849(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 1))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kClosed)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kOpened)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"1DoorNotOpened",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_一键四门开_任意一门超时_kLocked")
    @pytest.mark.full
    def test_caseid_1990850(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 1))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kLocked)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kOpened)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"1DoorNotOpened",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_一键四门开_任意一门超时_kUnlocked")
    @pytest.mark.full
    def test_caseid_1990851(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 1))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kUnlocked)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kOpened)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"1DoorNotOpened",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_一键四门开_任意一门超时_kOpening")
    @pytest.mark.full
    def test_caseid_1990852(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 1))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kOpening)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kOpened)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"1DoorNotOpened",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_一键四门开_任意一门超时_kHover")
    @pytest.mark.full
    def test_caseid_1990853(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 1))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kHover)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kOpened)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_一键四门开_任意一门超时_kClosingBreak")
    @pytest.mark.full
    def test_caseid_1990854(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 1))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kClosingBreak)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kOpened)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"1DoorNotOpened",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_一键四门开_任意一门超时_kOpeningBreak")
    @pytest.mark.full
    def test_caseid_1990855(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 1))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kOpeningBreak)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kOpened)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"1DoorNotOpened",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_一键四门开_任意一门超时_kHalfClosed")
    @pytest.mark.full
    def test_caseid_1990856(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 1))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kHalfClosed)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kOpened)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"1DoorNotOpened",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_一键四门开_任意两门超时")
    @pytest.mark.full
    def test_caseid_1990857(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 2))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kHalfClosed)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kOpened)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"2DoorNotOpened",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_一键四门开_任意三门超时")
    @pytest.mark.full
    def test_caseid_1990858(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 3))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kHalfClosed)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kOpened)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"3DoorNotOpened",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内有人_一键四门开_四门超时")
    @pytest.mark.smoke
    def test_caseid_1990859(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 4))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kHalfClosed)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kOpened)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"4DoorNotOpened",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_解锁状态_车内无人_一键四门开_kOpened")
    @pytest.mark.sanity
    def test_caseid_1990860(self):
        # 获取2个门开时的组合列表
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Unlocked,False)
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内有人_一键四门开_kOpened")
    @pytest.mark.smoke
    def test_caseid_1990861(self):
        # 获取2个门开时的组合列表
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.FourDoorLockedTailUnlocked)

        execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.FourDoorLockedTailUnlocked,True)
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_闭锁状态_车内无人_一键四门开_kOpened")
    @pytest.mark.sanity
    def test_caseid_1990862(self):
        # 获取2个门开时的组合列表
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Undef)

        execid = self.normal_process_open_error(DoorCode.All_door,LockStatus.Undef,False)
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_ kClosed")
    @pytest.mark.smoke
    def test_caseid_1990863(self):
        # 获取2个门开时的组合列表
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_close_error(DoorCode.All_door,True)
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kClosed)
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_一门异常_kFaultPlayProtectionActive")
    @pytest.mark.full
    def test_caseid_1990864(self):
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_close_error(DoorCode.All_door,True)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.FaultPlayProtectionActive,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"PlayProtcn",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_一门异常_kThermalProtection")
    @pytest.mark.smoke
    def test_caseid_1990865(self):
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_close_error(DoorCode.All_door,True)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.ThermalProtection,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"ThermProtcn",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_一门异常_kRollAngleAbnormal")
    @pytest.mark.full
    def test_caseid_1990866(self):
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_close_error(DoorCode.All_door,True)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.RollAngleAbnormal,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"RollAgAbnorm",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_一门异常_kRoadInclinationAbnormal")
    @pytest.mark.full
    def test_caseid_1990867(self):
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_close_error(DoorCode.All_door,True)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.RoadInclinationAbnormal,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"RoadInclnAbnorm",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_一门异常_kHallSensorsError")
    @pytest.mark.full
    def test_caseid_1990868(self):
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_close_error(DoorCode.All_door,True)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.HallSensorsError,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"HallSnsrErr",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_一门异常_两门异常_异常自动排列组合")
    @pytest.mark.full
    def test_caseid_1990869(self):
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_close_error(DoorCode.All_door,True)
        self.soa.notify_DoorFault({DoorId.kDoorFrontRight: DoorfFultSts.HallSensorsError,DoorId.kDoorFrontLeft: DoorfFultSts.RoadInclinationAbnormal,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"HallSnsrErr",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_一门异常_两门异常_异常自动排列组合")
    @pytest.mark.full
    def test_caseid_1990870(self):
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_close_error(DoorCode.All_door,True)
        self.soa.notify_DoorFault({DoorId.kDoorRearLeft: DoorfFultSts.HallSensorsError,DoorId.kDoorFrontLeft: DoorfFultSts.RoadInclinationAbnormal,DoorId.kDoorFrontLeft: DoorfFultSts.RollAngleAbnormal,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"HallSnsrErr",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_一门异常_四门异常_异常自动排列组合")
    @pytest.mark.full
    def test_caseid_1990871(self):
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_close_error(DoorCode.All_door,True)
        self.soa.notify_DoorFault({DoorId.kDoorRearLeft: DoorfFultSts.HallSensorsError,DoorId.kDoorFrontLeft: DoorfFultSts.RoadInclinationAbnormal,DoorId.kDoorFrontLeft: DoorfFultSts.RollAngleAbnormal,DoorId.kDoorRearRight: DoorfFultSts.RoadInclinationAbnormal,})
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"HallSnsrErr",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_关门超时_任意一门超时_kOpened")
    @pytest.mark.smoke
    def test_caseid_1990872(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 1))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_close_error(DoorCode.All_door,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kOpened)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kClosed)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"1DoorNotClosed",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_关门超时_任意一门超时_kClosing")
    @pytest.mark.full
    def test_caseid_1990873(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 1))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_close_error(DoorCode.All_door,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kClosing)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kClosed)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"1DoorNotClosed",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_关门超时_任意一门超时_kLocked")
    @pytest.mark.full
    def test_caseid_1990874(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 1))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_close_error(DoorCode.All_door,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kLocked)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kClosed)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"1DoorNotClosed",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_关门超时_任意一门超时_kUnlocked")
    @pytest.mark.full
    def test_caseid_1990875(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 1))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_close_error(DoorCode.All_door,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kUnlocked)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kClosed)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"1DoorNotClosed",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_关门超时_任意一门超时_kOpening")
    @pytest.mark.full
    def test_caseid_1990876(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 1))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_close_error(DoorCode.All_door,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kOpening)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kClosed)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"1DoorNotClosed",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_关门超时_任意一门超时_kHover")
    @pytest.mark.full
    def test_caseid_1990877(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 1))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_close_error(DoorCode.All_door,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kHover)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kClosed)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"1DoorNotClosed",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_关门超时_任意一门超时_kClosingBreak")
    @pytest.mark.full
    def test_caseid_1990878(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 1))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_close_error(DoorCode.All_door,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kClosingBreak)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kClosed)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"1DoorNotClosed",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_关门超时_任意一门超时_kOpeningBreak")
    @pytest.mark.full
    def test_caseid_1990879(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 1))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_close_error(DoorCode.All_door,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kOpeningBreak)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kClosed)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"1DoorNotClosed",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_关门超时_任意一门超时_kHalfClosed")
    @pytest.mark.full
    def test_caseid_1990880(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 1))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_close_error(DoorCode.All_door,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kHalfClosed)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kClosed)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"1DoorNotClosed",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_关门超时_任意两门超时")
    @pytest.mark.full
    def test_caseid_1990881(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 2))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_close_error(DoorCode.All_door,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kHalfClosed)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kClosed)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"2DoorNotClosed",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_关门超时_任意三门超时")
    @pytest.mark.full
    def test_caseid_1990882(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 3))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_close_error(DoorCode.All_door,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kClosing)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kClosed)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"3DoorNotClosed",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_关门超时_四门超时")
    @pytest.mark.smoke
    def test_caseid_1990883(self):
        four_doorcode = [DoorId.kDoorFrontLeft,DoorId.kDoorFrontRight,DoorId.kDoorRearLeft,DoorId.kDoorRearRight]
        # 获取2个门开时的组合列表

        one_combinations = list(itertools.combinations(four_doorcode, 4))
        for combination in one_combinations:
            qufan_combination = [i for i in four_doorcode if i not in combination]
            self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
            self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
            self.soa.notify_NotifyLockWarning(LockWarn.Idle)
            self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
            self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

            execid = self.normal_process_close_error(DoorCode.All_door,True)
            for doorid in combination:
                self.set_door_sts(doorid, DoorStatus.kClosing)
            for doorid in qufan_combination:
                self.set_door_sts(doorid, DoorStatus.kClosed)
            self.SetDoorCloseLock_req_num = 0
            assert self.tsp.log_search_remote_vehicle_control(f"4DoorNotClosed",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_关门警告")
    @pytest.mark.smoke
    def test_caseid_1990884(self):
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_close_error(DoorCode.All_door,True)
        self.soa.notify_NotifyLockWarning()
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"DoorAgSmall",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_门故障后门错误")
    @pytest.mark.full
    def test_caseid_1990885(self):
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_close_error(DoorCode.All_door,True)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.FaultPlayProtectionActive,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        sleep(1)
        self.soa.notify_NotifyLockWarning()
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"PlayProtcn",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内有人_一键四门关_门故障后门错误")
    @pytest.mark.full
    def test_caseid_1990886(self):
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_close_error(DoorCode.All_door,True)
        self.soa.notify_NotifyLockWarning()
        sleep(1)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.FaultPlayProtectionActive,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"DoorAgSmall",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_车内无人_一键四门关_ kClosed")
    @pytest.mark.smoke
    def test_caseid_1990887(self):
        self.set_door_sts(DoorId.kDoorAll, DoorStatus.kOpened)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=False)
        self.soa.notify_NotifyLockWarning(LockWarn.Idle)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.OK,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)

        execid = self.normal_process_close_error(DoorCode.All_door,False)
        self.soa.notify_NotifyLockWarning()
        sleep(1)
        self.soa.notify_DoorFault({DoorId.kDoorFrontLeft: DoorfFultSts.FaultPlayProtectionActive,DoorId.kDoorFrontRight: DoorfFultSts.OK,DoorId.kDoorRearLeft: DoorfFultSts.OK,DoorId.kDoorRearRight: DoorfFultSts.OK,})
        self.SetDoorCloseLock_req_num = 0
        assert self.tsp.log_search_remote_vehicle_control(f"DoorAgSmall",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("电动门控制-RVC_电动门控制_网络唤醒验证_NetWakeFail")
    @pytest.mark.full
    def test_caseid_1990896(self):
        for i in DoorCode:
            self.mix.tcam_network_sleep()
            execid = self.tsp.rvc_door_control(i)
            assert self.tsp.log_search_remote_vehicle_control("NetwakeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
            sleep(40)

    @allure.title("电动门控制-RVC_电动门控制_SOA服务调用失败")
    @pytest.mark.full
    def test_caseid_1990897(self):
        self.soa.soa_partner.stop_single_partner("DoorService_server")
        time.sleep(10)
        for i in DoorCode:
            execid = self.tsp.rvc_door_control(i)
            assert self.tsp.log_search_remote_vehicle_control("SOAFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
            sleep(40)
        self.soa.soa_partner.start_single_partner(service="DoorService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("DoorService_server",timeout=30)     