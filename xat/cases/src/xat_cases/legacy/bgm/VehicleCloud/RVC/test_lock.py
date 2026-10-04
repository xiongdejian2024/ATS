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

@allure.feature("远程控制/远控两域联调测试/远控解闭锁")
@allure.story("远控解闭锁")
class TestRvcLock(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["DoorService_client",
                         "CentralLockService_client",
                         "KeyService_client",
                         "RemoteCtrlService_client",
                         "VehicleSetStatusService_client",
                         "SeatService_client"])

    def before_each_func(self, ecu):
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,
                                       vehmtnst=VehMtnSts.StandStillVal2)
        self.mix.set_all_seats_present_sts(seat_pres_sts=SeatPresSts.NoPres)
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd,
                                          pass_opener=DoorOpenerSts.FullClsd,
                                          lere_opener=DoorOpenerSts.FullClsd,
                                          rire_opener=DoorOpenerSts.FullClsd,
                                          tr_opener=DoorOpenerSts.FullClsd)
        
    def after_each_func(self, ecu):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,
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

    @allure.title("RVC_远控解锁_ABANDONED")
    @pytest.mark.smoke
    def test_caseid_1991510(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.mix.set_open_close_door_precondition(DoorPos.All,DoorStatus.kOpened)
        sleep(3)
        execid=self.tsp.rvc_lock_control(op=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)
        self.soa.check_lock_status(lock_sts=Locksts.Unlckd)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVClock_Lock_convenience")
    @pytest.mark.smoke
    def test_caseid_1984901(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.mix.set_open_close_door_precondition(DoorPos.All,DoorStatus.kClosed)
        sleep(3)
        execid=self.tsp.rvc_lock_control(op=2)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)
        self.soa.check_lock_status(lock_sts=Locksts.SafeLockd)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVClock_Lock_ClosDoorLock")
    @pytest.mark.smoke
    def test_caseid_1984905(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.mix.set_open_close_door_precondition(DoorPos.All,DoorStatus.kClosed)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.Telm)
        sleep(3)
        execid=self.tsp.rvc_lock_control(3)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)
        self.soa.check_lock_status(lock_sts=Locksts.SafeLockd)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVClock_UnLock_abandoned")
    @pytest.mark.smoke
    def test_caseid_1984900(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.mix.set_open_close_door_precondition(DoorPos.All,DoorStatus.kOpened)
        sleep(3)
        execid=self.tsp.rvc_lock_control(op=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)
        self.soa.check_lock_status(lock_sts=Locksts.Unlckd)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVClock_Lock_Lock")
    @pytest.mark.smoke
    def test_caseid_1984904(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.mix.set_open_close_door_precondition(DoorPos.All,DoorStatus.kClosed)
        sleep(3)
        execid=self.tsp.rvc_lock_control(op=2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)
        self.soa.check_lock_status(lock_sts=Locksts.SafeLockd)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控闭锁联动关门_CONVENIENCE_车内无人")
    @pytest.mark.sanity
    def test_caseid_1991506(self):
        # self.mix.set_open_close_door_precondition(DoorPos.All,DoorStatus.kClosed)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.Telm)
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(3)
        execid=self.tsp.rvc_lock_control(3)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)
        self.soa.check_lock_status(lock_sts=Locksts.SafeLockd)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVClock_UnLock_UnLock")
    @pytest.mark.smoke
    def test_caseid_1984903(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.mix.set_open_close_door_precondition(DoorPos.All,DoorStatus.kOpened)
        sleep(3)
        execid=self.tsp.rvc_lock_control(op=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)
        self.soa.check_lock_status(lock_sts=Locksts.Unlckd)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控闭锁_INACTIVE_车内有人")
    @pytest.mark.smoke
    def test_caseid_1991509(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.mix.set_all_seats_present_sts(seat_pres_sts=SeatPresSts.Pres)
        self.mix.set_open_close_door_precondition(DoorPos.All,DoorStatus.kClosed)
        sleep(3)
        execid=self.tsp.rvc_lock_control(op=2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)
        self.soa.check_lock_status(lock_sts=Locksts.SafeLockd)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVClock_UnLock_Inactive")
    @pytest.mark.smoke
    def test_caseid_1984902(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.mix.set_open_close_door_precondition(DoorPos.All,DoorStatus.kOpened)
        sleep(3)
        execid=self.tsp.rvc_lock_control(op=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)
        self.soa.check_lock_status(lock_sts=Locksts.Unlckd)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控闭锁_INACTIVE_车内无人")
    @pytest.mark.smoke
    def test_caseid_1991508(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.mix.set_open_close_door_precondition(DoorPos.All,DoorStatus.kClosed)
        sleep(3)
        execid=self.tsp.rvc_lock_control(op=2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)
        self.soa.check_lock_status(lock_sts=Locksts.SafeLockd)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控闭锁联动关门_CONVENIENCE_车内有人")
    @pytest.mark.sanity
    def test_caseid_1991507(self):
        # self.mix.set_open_close_door_precondition(DoorPos.All,DoorStatus.kClosed)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.Telm)
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(3)
        execid=self.tsp.rvc_lock_control(3)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)
        self.soa.check_lock_status(lock_sts=Locksts.SafeLockd)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
