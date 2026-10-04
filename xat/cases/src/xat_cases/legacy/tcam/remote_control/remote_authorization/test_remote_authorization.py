#!/usr/bin/env python
# -*- coding: utf-8 -*-


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


@allure.feature("互联服务/远程控制/远程授权")
@allure.story("远程授权")
class TestRemoteAuthorization(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server",
                         "DoorService_server", "SeatService_server", "CentralLockService_server",
                         "HighVoltageService_server", "VehicleTimeService_server", "PedalService_server",
                         "KeyService_server", "TailGateService_server", "RemoteCtrlService_client"])
        self.mix.start_get_request_and_send_response_to_tcam_thread(["VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server",
                         "DoorService_server", "SeatService_server", "CentralLockService_server",
                         "HighVoltageService_server", "VehicleTimeService_server", "PedalService_server",
                         "KeyService_server", "TailGateService_server"])
        time.sleep(30)
        self.tsp.set_bench_config(self.tb_config["vid"], self.tb_config["tel"])

    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.io.tcam_kl15_up()
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.send_Alldoor_OpenCloseStatus_close()
        self.soa.send_Alldoor_Status_close()
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        self.soa.notify_BrakePedalStatus(status=PressedStatus.PedalReleased,validity=ValidityLevel.kValid)
        self.soa.send_Alldoor_close()
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,0])
        self.soa.notify_BrakePedalStatus(status=PressedStatus.PedalReleased,validity=ValidityLevel.kValid)
        time.sleep(2)

    def after_each_func(self, ecu):
        if ecu.testresult == 'Failure':
            logger.info('用例执行失败')
            sleep(10)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.send_Alldoor_close()
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,0])
        self.soa.notify_BrakePedalStatus(status=PressedStatus.PedalReleased,validity=ValidityLevel.kValid)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.Telematices)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.Telematices,update_eve=True)
        self.io.tcam_kl15_up()
        time.sleep(2)

        
    def after_class(self, ecu):
        self.mix.stop_get_request_and_send_response_to_tcam_thread()
    

    @allure.title("远程控制-RVC_持久化存储_entry_休眠唤醒")
    @pytest.mark.full
    def test_authorization_caseid_1986490(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        execid = self.tsp.rvc_remote_authorization()
        # 由于已经解锁，故无需发送解锁请求
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)
        self.bus_comm.pause_all_bus_send()
        self.io.tcam_kl15_down()
        self.soa.soa_partner.empty_all()
        time.sleep(60)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)


    @allure.title("远程控制-RVC_entry状态_异常掉电复归_取消授权条件满足_授权条件不满足")
    @pytest.mark.full
    def test_authorization_caseid_1986491(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        execid = self.tsp.rvc_remote_authorization()
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)
        self.soa.soa_partner.empty_all()
        self.ssh.tcam_ssh.type_commands('reboot -f')
        self.soa.wait_for_service_reconnect('RemoteCtrlService_client', timeout=300)
        self.soa.send_Alldoor_close()
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,0])
        self.soa.notify_BrakePedalStatus(status=PressedStatus.PedalReleased,validity=ValidityLevel.kValid)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.Telematices)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.Telematices,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=False,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kDefault,timeout=100)

    @allure.title("远程控制-RVC_entry状态_异常掉电复归_取消授权条件不满足_授权条件不满足")
    @pytest.mark.full
    def test_authorization_caseid_1986492(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        execid = self.tsp.rvc_remote_authorization()
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)
        self.soa.soa_partner.empty_all()
        self.ssh.tcam_ssh.type_commands('reboot -f')
        self.soa.wait_for_service_reconnect('RemoteCtrlService_client', timeout=300)
        self.soa.send_Alldoor_close()
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,0])
        self.soa.notify_BrakePedalStatus(status=PressedStatus.PedalReleased,validity=ValidityLevel.kValid)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.Telematices)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.Unlocked, trigger_id=TriggerSourceId.Telematices,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=100)
        self.mix.default_func_param(['GetLockStatus'])


    @allure.title("远程控制-RVC_entry状态_异常掉电复归_取消授权条件不满足_授权条件满足")
    @pytest.mark.full
    def test_authorization_caseid_1986493(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        execid = self.tsp.rvc_remote_authorization()
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)
        self.soa.soa_partner.empty_all()
        self.ssh.tcam_ssh.type_commands('reboot -f')
        self.soa.wait_for_service_reconnect('RemoteCtrlService_client', timeout=300)
        self.soa.send_Alldoor_open()
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        self.soa.notify_BrakePedalStatus(status=PressedStatus.PedalReleased,validity=ValidityLevel.kValid)
        # self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.Telematices)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.Unlocked, trigger_id=TriggerSourceId.Telematices,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=100)

    @allure.title("远程控制-RVC_ReadyEntry状态_异常掉电复归_取消授权条件不满足_授权条件不满足")
    @pytest.mark.full
    def test_authorization_caseid_1986494(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)
        self.soa.soa_partner.empty_all()
        self.ssh.tcam_ssh.type_commands('reboot -f')
        self.soa.wait_for_service_reconnect('RemoteCtrlService_client', timeout=300)
        self.soa.send_Alldoor_close()
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,0])
        self.soa.notify_BrakePedalStatus(status=PressedStatus.PedalReleased,validity=ValidityLevel.kValid)
        # self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.Telematices)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.Unlocked, trigger_id=TriggerSourceId.Telematices,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=False,timeout=50)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kDefault,timeout=100)

    @allure.title("远程控制-RVC_ReadyEntry状态_异常掉电复归_取消授权条件不满足_授权条件满足")
    @pytest.mark.full
    def test_authorization_caseid_1986495(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)
        self.soa.soa_partner.empty_all()
        self.ssh.tcam_ssh.type_commands('reboot -f')
        self.soa.wait_for_service_reconnect('RemoteCtrlService_client', timeout=300)
        # time.sleep(180)
        # self.soa.check_GetLockStatus_req_and_feedback_resp(lock_status=LockStatus.Unlocked, timeout=20)
        self.soa.send_Alldoor_open()
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,0])
        self.soa.notify_BrakePedalStatus(status=PressedStatus.PedalReleased,validity=ValidityLevel.kValid)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.Telematices)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.Unlocked, trigger_id=TriggerSourceId.Telematices,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=100)
        self.mix.default_func_param(['GetLockStatus'])


    @allure.title("远程控制-RVC_ReadyEntry状态_异常掉电复归_取消授权条件满足")
    @pytest.mark.full
    def test_authorization_caseid_1986496(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)
        self.soa.soa_partner.empty_all()
        self.ssh.tcam_ssh.type_commands('reboot -f')
        self.soa.wait_for_service_reconnect('RemoteCtrlService_client', timeout=300)
        self.soa.send_Alldoor_close()
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,0])
        self.soa.notify_BrakePedalStatus(status=PressedStatus.PedalReleased,validity=ValidityLevel.kValid)
        # self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.Telematices)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.Telematices,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=False,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kDefault,timeout=100)


    @allure.title("远程控制-RVC_远程授权_二次授权")
    @pytest.mark.full
    def test_authorization_caseid_1982883(self, ecu):
        execid1 = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        execid2 = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid2)
        sleep(10)

    @allure.title("远程控制-RVC_远程授权_reqfail")
    @pytest.mark.full
    def test_authorization_caseid_1982882(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)

    @allure.title("远程控制-RVC_远程授权_transport")
    @pytest.mark.sanity
    def test_authorization_caseid_1982881(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid)
    
    @allure.title("远程控制-RVC_远程授权_factory")
    @pytest.mark.full
    def test_authorization_caseid_1982880(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid)

    @allure.title("远程控制-RVC_远程授权_active")
    @pytest.mark.sanity
    def test_authorization_caseid_1982879(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid)

    @allure.title("远程控制-RVC_远程授权_driving")
    @pytest.mark.sanity
    def test_authorization_caseid_1982878(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid)

    @allure.title("远程控制-RVC_远程授权_N档")
    @pytest.mark.sanity
    def test_authorization_caseid_1982877(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Neut)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid)         

    @allure.title("远程控制-RVC_远程授权_D档")
    @pytest.mark.full
    def test_authorization_caseid_1982876(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Drv)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid) 

    @allure.title("远程控制-RVC_远程授权_R档")
    @pytest.mark.full
    def test_authorization_caseid_1982875(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid)        

    @allure.title("远程控制-RVC_远程授权_FOTAUPDATE")
    @pytest.mark.sanity
    def test_authorization_caseid_1982874(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid)

    @allure.title("远程控制-RVC_远程授权_FOTAROLLBACK")
    @pytest.mark.full
    def test_authorization_caseid_1982873(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid)

    @allure.title("远程控制-RVC_远程授权_QUERY")
    @pytest.mark.full
    def test_authorization_caseid_1982872(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("远程控制-RVC_远程授权_NEWTASK")
    @pytest.mark.full
    def test_authorization_caseid_1982871(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("远程控制-RVC_远程授权_DOWNLOADING")
    @pytest.mark.full
    def test_authorization_caseid_1982870(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("远程控制-RVC_远程授权_ACTIVE")
    @pytest.mark.full
    def test_authorization_caseid_1982869(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("远程控制-RVC_远程授权_FAILEDNOTDRIVING")
    @pytest.mark.full
    def test_authorization_caseid_1982868(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("远程控制-RVC_远程授权_FAILEDDRIVING")
    @pytest.mark.full
    def test_authorization_caseid_1982867(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_DRIVING)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("远程控制-RVC_远程授权_SUCCESSFUL")
    @pytest.mark.full
    def test_authorization_caseid_1982866(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.soa.notify_fota_status(state=FOTAMasteSts.SUCCESSFUL)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("远程控制-RVC_远程授权_REACHAPPOINTMENT")
    @pytest.mark.full
    def test_authorization_caseid_1982865(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.soa.notify_fota_status(state=FOTAMasteSts.REACH_APPOINTMENT)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("远程控制-RVC_远程授权_维修模式")
    @pytest.mark.sanity
    def test_authorization_caseid_1982864(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid)

    @allure.title("远程控制-RVC_远程授权_transport与active")
    @pytest.mark.full
    def test_authorization_caseid_1982863(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        execid = self.tsp.rvc_remote_authorization()

        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid)

    @allure.title("远程控制-RVC_远程授权_driving与N档")
    @pytest.mark.full
    def test_authorization_caseid_1982862(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid)
        
    @allure.title("远程控制-RVC_远程授权_N档与FOTAUPDATE")
    @pytest.mark.full
    def test_authorization_caseid_1982861(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid)     

    @allure.title("远程控制-RVC_远程授权_FOTA与维修模式")
    @pytest.mark.full
    def test_authorization_caseid_1982860(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid)
        
    @allure.title("远程控制-RVC_远程授权_abandoned")
    @pytest.mark.smoke
    def test_authorization_caseid_1982859(self, ecu):
        self.io.tcam_kl15_down()
        self.bus_comm.pause_all_bus_send()
        time.sleep(180)
        self.mix.tcam_network_sleep()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC23,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC27,signal_value=NMSts.valid,timeout=30)
        execid = self.tsp.rvc_remote_authorization()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.resume_all_bus_send()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kUnlockWait,timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry, send_time=10, timeout=20)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,timeout=1)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,timeout=1)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC23,timeout=1)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC27,timeout=1)



    @allure.title("远程控制-RVC_远程授权_远控解锁失败")
    @pytest.mark.full
    def test_authorization_caseid_1982858(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control("AuthUnlockFail",execid=execid)
   
    @allure.title("远程控制-RVC_远程授权_abandoned未上切")
    @pytest.mark.full
    def test_authorization_caseid_1982857(self, ecu):
        self.soa.soa_partner.stop_single_partner("CentralLockService_server")
        logger.info("中控锁服务已下线")
        time.sleep(10)
        execid = self.tsp.rvc_remote_authorization()
        time.sleep(50)
        assert self.tsp.log_search_remote_vehicle_control("SOAFail",execid=execid)
        self.soa.soa_partner.start_single_partner(service="CentralLockService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("CentralLockService_server",timeout=30)

    @allure.title("远程控制-RVC_远程授权_inactive")
    @pytest.mark.smoke
    def test_authorization_caseid_1982856(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kUnlockWait,timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry, send_time=10, timeout=20)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("远程控制-RVC_远程授权_convience")
    @pytest.mark.smoke
    def test_authorization_caseid_1982855(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=10)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kUnlockWait,timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry, send_time=10, timeout=20)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("远程控制-RVC_远程授权_主驾车门开启")
    @pytest.mark.sanity
    def test_authorization_caseid_1982854(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        execid = self.tsp.rvc_remote_authorization()
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("远程控制-RVC_远程授权_副驾车门开启")
    @pytest.mark.full
    def test_authorization_caseid_1982853(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_FrntRightDoorSts(isopen=True,sts=DoorStatus.kOpened)
        execid = self.tsp.rvc_remote_authorization()
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("远程控制-RVC_远程授权_左后车门开启")
    @pytest.mark.full
    def test_authorization_caseid_1982852(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_RearLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        execid = self.tsp.rvc_remote_authorization()
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("远程控制-RVC_远程授权_右后车门开启")
    @pytest.mark.full
    def test_authorization_caseid_1982851(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_RearRightDoorSts(isopen=True,sts=DoorStatus.kOpened)
        execid = self.tsp.rvc_remote_authorization()
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("远程控制-RVC_远程授权_主驾与副驾车门开启")
    @pytest.mark.full
    def test_authorization_caseid_1982850(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.soa.notify_FrntRightDoorSts(isopen=True,sts=DoorStatus.kOpened)
        execid = self.tsp.rvc_remote_authorization()
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("远程控制-RVC_远程授权_主驾副驾左后车门开启")
    @pytest.mark.full
    def test_authorization_caseid_1982849(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.soa.notify_FrntRightDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.soa.notify_RearLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        execid = self.tsp.rvc_remote_authorization()
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)
    
    @allure.title("远程控制-RVC_远程授权_四门开启")
    @pytest.mark.full
    def test_authorization_caseid_1982848(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.soa.notify_FrntRightDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.soa.notify_RearLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.soa.notify_RearRightDoorSts(isopen=True,sts=DoorStatus.kOpened)
        execid = self.tsp.rvc_remote_authorization()
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("远程控制-RVC_远程授权_主驾座椅占座")
    @pytest.mark.sanity
    def test_authorization_caseid_1982847(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        execid = self.tsp.rvc_remote_authorization()
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("远程控制-RVC_远程授权_副驾座椅占座")
    @pytest.mark.full
    @allure.issue("https://jira.jiduauto.com/browse/SOA-24398?filter=-2", name="SOA-24398")
    def test_authorization_caseid_1982846(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,1,0,0,0])
        execid = self.tsp.rvc_remote_authorization()
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,timeout=20)
        # time.sleep(120)
        assert self.tsp.log_search_remote_vehicle_control("TimerAuthDelayFail",execid=execid)
    
    @allure.title("远程控制-RVC_远程授权_刹车踏板")
    @pytest.mark.sanity
    def test_authorization_caseid_1982845(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_BrakePedalStatus(status=PressedStatus.PedalPressed,validity=ValidityLevel.kValid)
        execid = self.tsp.rvc_remote_authorization()
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)
    
    @allure.title("远程控制-RVC_远程授权_主驾车门与主驾座椅占座")
    @pytest.mark.full
    def test_authorization_caseid_1982844(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        execid = self.tsp.rvc_remote_authorization()
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("远程控制-RVC_远程授权_主驾车门与刹车踏板")
    @pytest.mark.full
    def test_authorization_caseid_1982843(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.soa.notify_BrakePedalStatus(status=PressedStatus.PedalPressed,validity=ValidityLevel.kValid)
        execid = self.tsp.rvc_remote_authorization()
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("远程控制-RVC_远程授权_主驾座椅与刹车踏板")
    @pytest.mark.full
    def test_authorization_caseid_1982842(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        self.soa.notify_BrakePedalStatus(status=PressedStatus.PedalPressed,validity=ValidityLevel.kValid)
        execid = self.tsp.rvc_remote_authorization()
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("远程控制-RVC_远程授权_门开主驾座椅与刹车踏板")
    @pytest.mark.full
    def test_authorization_caseid_1982841(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.send_Alldoor_open()
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        self.soa.notify_BrakePedalStatus(status=PressedStatus.PedalPressed,validity=ValidityLevel.kValid)
        execid = self.tsp.rvc_remote_authorization()
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("远程控制-RVC_等待授权_未开车门")
    @pytest.mark.sanity
    @allure.issue("https://jira.jiduauto.com/browse/SOA-24398?filter=-2", name="SOA-24398")
    def test_authorization_caseid_1982840(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        execid = self.tsp.rvc_remote_authorization()
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,timeout=20)
        # time.sleep(120)
        assert self.tsp.log_search_remote_vehicle_control("TimerAuthDelayFail",execid=execid)

    @allure.title("远程控制-RVC_等待授权_远控闭锁")
    @pytest.mark.sanity
    def test_authorization_caseid_1982839(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        execid = self.tsp.rvc_remote_authorization()
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,timeout=20)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control("AuthEscLockStartOK",execid=execid,flage=0)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.Lock,lock_req_source=LockReqSource.Talematics,timeout=10)
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.Telematices)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.Telematices,update_eve=True)
        self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control("AuthEscLockSuccess",execid=execid,exectype_num=2,flage=2)

    @allure.title("远程控制-RVC_等待授权_远控闭锁失败")
    @pytest.mark.full
    @allure.issue("https://jira.jiduauto.com/browse/SOA-24400?filter=-2",name="SOA-24400")
    def test_authorization_caseid_1982838(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        execid = self.tsp.rvc_remote_authorization()
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,timeout=20)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.Lock,lock_req_source=LockReqSource.Talematics,timeout=10)
        assert self.tsp.log_search_remote_vehicle_control("AuthEscLockDelayFail",execid=execid,exectype_num=2)

    @allure.title("远程控制-RVC_等待授权_四门锁尾门未锁")
    @pytest.mark.sanity
    def test_authorization_caseid_1982837(self, ecu):
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        execid = self.tsp.rvc_remote_authorization()
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.FourDoorLockedTailUnlocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.Telematices)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.FourDoorLockedTailUnlocked, trigger_id=TriggerSourceId.Telematices,update_eve=True)
        assert self.tsp.log_search_remote_vehicle_control("AuthEsc",execid=execid)

    @allure.title("远程控制-RVC_等待授权_蓝牙闭锁")
    @pytest.mark.sanity
    def test_authorization_caseid_1982836(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kUnlockWait,timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.RemoteKey)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.Telematices,update_eve=True)
        assert self.tsp.log_search_remote_vehicle_control("AuthEsc",execid=execid)
    
    @allure.title("远程控制-RVC_等待授权_车外的按钮闭锁")
    @pytest.mark.full
    def test_authorization_caseid_1982835(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kUnlockWait,timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control("StartOK",execid=execid,flage=0)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.KeyLessPassive)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.KeyLessPassive,update_eve=True)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control("AuthEsc",execid=execid,flage=2)

    @allure.title("远程控制-RVC_等待授权_车内的按钮闭锁")
    @pytest.mark.full
    def test_authorization_caseid_1982834(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kUnlockWait,timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        # self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.InteriorSwitches)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.InteriorSwitches,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,timeout=20)
        # time.sleep(115)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=False,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kDefault,timeout=20)

    @allure.title("远程控制-RVC_等待授权_车速自动落锁")
    @pytest.mark.full
    def test_authorization_caseid_1982833(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kUnlockWait,timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        # self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.SpeedLocking)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.SpeedLocking,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,timeout=20)
        # time.sleep(115)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=False,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kDefault,timeout=20)

    @allure.title("远程控制-RVC_等待授权_自动重锁")
    @pytest.mark.full
    def test_authorization_caseid_1982832(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kUnlockWait,timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control("StartOK",execid=execid,flage=0)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        # self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        # self.soa.empty_all()
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.Relocking)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.Relocking,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,timeout=20)
        # time.sleep(115)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=False,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kDefault,timeout=20)

    @allure.title("远程控制-RVC_等待授权_锁未使用")
    @pytest.mark.full
    def test_authorization_caseid_1982831(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kUnlockWait,timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        # self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.SlamLocking)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.SlamLocking,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,timeout=20)
        # time.sleep(115)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=False,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kDefault,timeout=20)

    @allure.title("远程控制-RVC_等待授权_碰撞解锁")
    @pytest.mark.full
    def test_authorization_caseid_1982830(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kUnlockWait,timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        # self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.CrashUnlock)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.CrashUnlock,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,timeout=20)
        # time.sleep(115)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=False,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kDefault,timeout=20)

    @allure.title("远程控制-RVC_等待授权_离车闭锁")
    @pytest.mark.full
    def test_authorization_caseid_1982829(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kUnlockWait,timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control("StartOK",execid=execid,flage=0)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.Approach)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.Approach,update_eve=True)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control("AuthEsc",execid=execid,flage=2)

    @allure.title("远程控制-RVC_等待授权_外部其他闭锁")
    @pytest.mark.full
    def test_authorization_caseid_1982828(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kUnlockWait,timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control("StartOK",execid=execid,flage=0)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.OutsideOthers)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.OutsideOthers,update_eve=True)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control("AuthEsc",execid=execid,flage=2)

    @allure.title("远程控制-RVC_等待授权_内部其他闭锁")
    @pytest.mark.full
    def test_authorization_caseid_1982827(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        # self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.InsideOthers)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.InsideOthers,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,timeout=20)
        # time.sleep(115)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=False,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kDefault,timeout=20)

    @allure.title("远程控制-RVC_等待授权_NFC")
    @pytest.mark.full
    def test_authorization_caseid_1982826(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control("StartOK",execid=execid,flage=0)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.NFC)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.NFC,update_eve=True)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control("AuthEsc",execid=execid,flage=2)

    @allure.title("远程控制-RVC_取消授权_四门锁尾门未锁")
    @pytest.mark.smoke
    def test_authorization_caseid_1982825(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        self.soa.send_Alldoor_open()
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        self.soa.notify_BrakePedalStatus(status=PressedStatus.PedalPressed,validity=ValidityLevel.kValid)
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.FourDoorLockedTailUnlocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.Approach)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.FourDoorLockedTailUnlocked, trigger_id=TriggerSourceId.Approach,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=False,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kDefault,timeout=20)

    @allure.title("远程控制-RVC_取消授权_远控闭锁")
    @pytest.mark.smoke
    def test_authorization_caseid_1982824(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.Telematices)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.Telematices,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=False,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kDefault,timeout=20)

    @allure.title("远程控制-RVC_取消授权_远控闭锁失败")
    @pytest.mark.full
    def test_authorization_caseid_1982823(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kUnlockWait,timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        self.soa.soa_partner.stop_single_partner("CentralLockService_server")
        logger.info("中控锁服务已下线")
        self.soa.soa_partner.empty_all()
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=False,timeout=200)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kDefault,timeout=200)
        assert self.tsp.log_search_remote_vehicle_control("AuthEscLockFail",execid=execid,exectype_num=2)
        self.soa.soa_partner.start_single_partner(service="CentralLockService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("CentralLockService_server",timeout=30)

    @allure.title("远程控制-RVC_取消授权_蓝牙闭锁")
    @pytest.mark.sanity
    def test_authorization_caseid_1982822(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        self.soa.send_Alldoor_open()
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.RemoteKey)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.RemoteKey,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=False,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kDefault,timeout=20)

    @allure.title("远程控制-RVC_取消授权_车外的按钮闭锁")
    @pytest.mark.full
    def test_authorization_caseid_1982821(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        self.soa.send_Alldoor_open()
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.KeyLessPassive)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.KeyLessPassive,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=False,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kDefault,timeout=20)

    @allure.title("远程控制-RVC_取消授权_车内的按钮闭锁")
    @pytest.mark.full
    def test_authorization_caseid_1982820(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        self.soa.send_Alldoor_open()
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.InteriorSwitches)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.InteriorSwitches,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)

    @allure.title("远程控制-RVC_取消授权_车速自动落锁")
    @pytest.mark.full
    def test_authorization_caseid_1982819(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        self.soa.send_Alldoor_open()
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.SpeedLocking)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.SpeedLocking,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)

    @allure.title("远程控制-RVC_取消授权_自动重锁")
    @pytest.mark.full
    def test_authorization_caseid_1982818(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kUnlockWait,timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        self.soa.send_Alldoor_open()
        time.sleep(5)
        # self.soa.empty_all()
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.Relocking)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.Relocking,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)

    @allure.title("远程控制-RVC_取消授权_锁未使用")
    @pytest.mark.full
    def test_authorization_caseid_1982817(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kUnlockWait,timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        self.soa.send_Alldoor_open()
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.SlamLocking)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.SlamLocking,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)

    @allure.title("远程控制-RVC_取消授权_碰撞解锁")
    @pytest.mark.full
    def test_authorization_caseid_1982816(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        self.soa.send_Alldoor_open()
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.CrashUnlock)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.CrashUnlock,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)

    @allure.title("远程控制-RVC_取消授权_离车闭锁")
    @pytest.mark.full
    def test_authorization_caseid_1982815(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        self.soa.send_Alldoor_open()
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.Approach)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.Approach,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=False,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kDefault,timeout=20)


    @allure.title("远程控制-RVC_取消授权_外部其他闭锁")
    @pytest.mark.full
    def test_authorization_caseid_1982814(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        self.soa.send_Alldoor_open()
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.OutsideOthers)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.OutsideOthers,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=False,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kDefault,timeout=20)

    @allure.title("远程控制-RVC_取消授权_内部其他闭锁")
    @pytest.mark.full
    def test_authorization_caseid_1982813(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        self.soa.send_Alldoor_open()
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.FourDoorLockedTailUnlocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.InsideOthers)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.FourDoorLockedTailUnlocked, trigger_id=TriggerSourceId.InsideOthers,update_eve=True)
        time.sleep(5)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry,timeout=20)
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.Telematices)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.Telematices,update_eve=True)
        time.sleep(5)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=False,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kDefault,timeout=20)

    @allure.title("远程控制-RVC_取消授权_NFC")
    @pytest.mark.full
    def test_authorization_caseid_1982812(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        time.sleep(5)
        self.soa.send_Alldoor_open()
        time.sleep(5)
        # self.soa.notify_LockStatus(lock_sts=LockSts.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.NFC)
        self.soa.notify_NotifyCentralLockSysInfo(sts=LockStatus.AllLocked, trigger_id=TriggerSourceId.NFC,update_eve=True)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=False,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kDefault,timeout=20)

    @allure.title("远程控制-RVC_远程授权_inactive_TelmFctReq")
    @pytest.mark.full
    def test_authorization_caseid_1982809(self, ecu):
        self.io.tcam_kl15_down()  
        self.bus_comm.pause_all_bus_send() 
        sleep(181)
        self.mix.tcam_network_sleep()
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        self.bus_comm.check_signal_thread_start("connectivitycanfd","TcamConnectivityFr35", "TelmFctReq", timeout=10)
        execid = self.tsp.rvc_remote_authorization()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        result_ori_1 = self.bus_comm.check_signal_thread_stop("TelmFctReq",13)
        result_1 = check_signal_num(result_ori_1,1)
        frame_times = result_1[0]
        duration_time = result_1[1]
        logger.info(f"持续发送{frame_times}帧，持续时间为{duration_time}s")
        assert frame_times==25, f"检查休眠唤醒后TelmFctReq发送失败"
        sleep(10)

    @allure.title("远程控制-RVC_远程授权_授权后休眠唤醒")
    @pytest.mark.full
    def test_authorization_caseid_1982808(self, ecu):
        self.io.tcam_kl15_down()  
        self.bus_comm.pause_all_bus_send() 
        sleep(180) 
        self.mix.tcam_network_sleep()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC23,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC27,signal_value=NMSts.valid,timeout=30)
        execid = self.tsp.rvc_remote_authorization()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kUnlockWait,timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,timeout=1)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,timeout=1)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC23,timeout=1)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC27,timeout=1)
        # self.soa.notify_LockStatus(lock_sts=LockStatus.AllLocked)
        # self.soa.notify_LockSuccessTriggerSource(sourceid=TriggerSourceId.Telematices)



    @allure.title("远程控制-RVC_远程授权_16hTCAM重启后远控")
    @pytest.mark.full
    def test_authorization_caseid_1982807(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        execid = self.tsp.rvc_remote_authorization()
        self.soa.check_SetDoorCloseLock_req_and_feedback_resp(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq, timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kUnlockWait,timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockStatus.Unlocked)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control("StartOK",execid=execid,flage=0)
        # self.soa.check_NotifyRemoteAuthStartSts_event(is_valid=True,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry,send_time=2,timeout=20)
        self.soa.notify_BrakePedalStatus(status=PressedStatus.PedalPressed,validity=ValidityLevel.kValid)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control("Success",execid=execid,flage=2)

    @allure.title("远程控制-RVC_远程授权_休眠清空默认值_自动授权条件全满足")
    @pytest.mark.full
    def test_authorization_caseid_1988807(self, ecu):
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        self.soa.send_Alldoor_open()
        self.soa.notify_BrakePedalStatus(status=PressedStatus.PedalPressed,validity=ValidityLevel.kValid)
        self.mix.tcam_network_sleep()
        self.soa.soa_partner.stop_single_partner("DoorService_server")
        self.soa.soa_partner.stop_single_partner("CentralLockService_server")
        self.soa.soa_partner.stop_single_partner("SeatService_server")
        self.soa.soa_partner.stop_single_partner("PedalService_server")
        logger.info("中控锁服务已下线")
        sleep(2)
        self.soa.soa_partner.start_single_partner(service="DoorService",role="server")
        self.soa.soa_partner.start_single_partner(service="CentralLockService",role="server")
        self.soa.soa_partner.start_single_partner(service="SeatService",role="server")
        self.soa.soa_partner.start_single_partner(service="PedalService",role="server")
        self.soa.soa_partner.empty_all()
        sleep(2)
        execid = self.tsp.rvc_remote_authorization()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry, send_time=10, timeout=20)
        self.mix.default_func_param(['GetLockStatus'])


    @allure.title("远程控制-RVC_远程授权_休眠清空默认值_右后门状态为开")
    @pytest.mark.full
    def test_authorization_caseid_1988806(self, ecu):
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_RearRightDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.mix.tcam_network_sleep()
        self.soa.soa_partner.stop_single_partner("DoorService_server")
        self.soa.soa_partner.stop_single_partner("CentralLockService_server")
        logger.info("中控锁服务已下线")
        sleep(2)
        self.soa.soa_partner.start_single_partner(service="DoorService",role="server")
        self.soa.soa_partner.start_single_partner(service="CentralLockService",role="server")
        self.soa.soa_partner.empty_all()
        sleep(2)
        execid = self.tsp.rvc_remote_authorization()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry, send_time=10, timeout=20)
        self.mix.default_func_param(['GetLockStatus'])

    @allure.title("远程控制-RVC_远程授权_休眠清空默认值_左后门状态为开")
    @pytest.mark.full
    def test_authorization_caseid_1988805(self, ecu):
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_RearLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.mix.tcam_network_sleep()
        self.soa.soa_partner.stop_single_partner("DoorService_server")
        self.soa.soa_partner.stop_single_partner("CentralLockService_server")
        logger.info("中控锁服务已下线")
        sleep(2)
        self.soa.soa_partner.start_single_partner(service="DoorService",role="server")
        self.soa.soa_partner.start_single_partner(service="CentralLockService",role="server")
        self.soa.soa_partner.empty_all()
        sleep(2)
        execid = self.tsp.rvc_remote_authorization()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry, send_time=10, timeout=20)
        self.mix.default_func_param(['GetLockStatus'])

    @allure.title("远程控制-RVC_远程授权_休眠清空默认值_副驾门状态为开")
    @pytest.mark.full
    def test_authorization_caseid_1988804(self, ecu):
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_FrntRightDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.mix.tcam_network_sleep()
        self.soa.soa_partner.stop_single_partner("DoorService_server")
        self.soa.soa_partner.stop_single_partner("CentralLockService_server")
        logger.info("中控锁服务已下线")
        sleep(2)
        self.soa.soa_partner.start_single_partner(service="DoorService",role="server")
        self.soa.soa_partner.start_single_partner(service="CentralLockService",role="server")
        self.soa.soa_partner.empty_all()
        sleep(2)
        execid = self.tsp.rvc_remote_authorization()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry, send_time=10, timeout=20)
        self.mix.default_func_param(['GetLockStatus'])

    @allure.title("远程控制-RVC_远程授权_休眠清空默认值_主驾门状态为开")
    @pytest.mark.full
    def test_authorization_caseid_1988803(self, ecu):
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_FrntLeftDoorSts(isopen=True,sts=DoorStatus.kOpened)
        self.mix.tcam_network_sleep()
        self.soa.soa_partner.stop_single_partner("DoorService_server")
        self.soa.soa_partner.stop_single_partner("CentralLockService_server")
        logger.info("中控锁服务已下线")
        sleep(2)
        self.soa.soa_partner.start_single_partner(service="DoorService",role="server")
        self.soa.soa_partner.start_single_partner(service="CentralLockService",role="server")
        self.soa.soa_partner.empty_all()
        sleep(2)
        execid = self.tsp.rvc_remote_authorization()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry, send_time=10, timeout=20)
        self.mix.default_func_param(['GetLockStatus'])


    @allure.title("远程控制-RVC_远程授权_休眠清空默认值_全部车门状态为开")
    @pytest.mark.full
    def test_authorization_caseid_1988802(self, ecu):
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.send_Alldoor_open()
        self.mix.tcam_network_sleep()
        self.soa.soa_partner.stop_single_partner("DoorService_server")
        self.soa.soa_partner.stop_single_partner("CentralLockService_server")
        logger.info("中控锁服务已下线")
        sleep(2)
        self.soa.soa_partner.start_single_partner(service="DoorService",role="server")
        self.soa.soa_partner.start_single_partner(service="CentralLockService",role="server")
        self.soa.soa_partner.empty_all()
        sleep(2)
        execid = self.tsp.rvc_remote_authorization()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry, send_time=10, timeout=20)
        self.mix.default_func_param(['GetLockStatus'])


    @allure.title("远程控制-RVC_远程授权_休眠清空默认值_主驾座椅占座")
    @pytest.mark.full
    def test_authorization_caseid_1988801(self, ecu):
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        self.mix.tcam_network_sleep()
        self.soa.soa_partner.stop_single_partner("SeatService_server")
        self.soa.soa_partner.stop_single_partner("CentralLockService_server")
        logger.info("中控锁服务已下线")
        sleep(2)
        self.soa.soa_partner.start_single_partner(service="SeatService",role="server")
        self.soa.soa_partner.start_single_partner(service="CentralLockService",role="server")
        self.soa.soa_partner.empty_all()
        sleep(2)
        execid = self.tsp.rvc_remote_authorization()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry, send_time=10, timeout=20)
        self.mix.default_func_param(['GetLockStatus'])


    @allure.title("远程控制-RVC_远程授权_休眠清空默认值_刹车踏板")
    @pytest.mark.full
    def test_authorization_caseid_1988800(self, ecu):
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_BrakePedalStatus(status=PressedStatus.PedalPressed,validity=ValidityLevel.kValid)
        self.mix.tcam_network_sleep()
        self.soa.soa_partner.stop_single_partner("PedalService_server")
        self.soa.soa_partner.stop_single_partner("CentralLockService_server")
        logger.info("中控锁服务已下线")
        sleep(2)
        self.soa.soa_partner.start_single_partner(service="PedalService",role="server")
        self.soa.soa_partner.start_single_partner(service="CentralLockService",role="server")
        self.soa.soa_partner.empty_all()
        sleep(2)
        execid = self.tsp.rvc_remote_authorization()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry, send_time=10, timeout=20)
        self.mix.default_func_param(['GetLockStatus'])

    @allure.title("远程控制-RVC_远程授权_锁状态无效_休眠后先发送无效值")
    @pytest.mark.full
    def test_authorization_caseid_1988809(self, ecu):
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        self.soa.send_Alldoor_open()
        self.soa.notify_BrakePedalStatus(status=PressedStatus.PedalPressed,validity=ValidityLevel.kValid)
        self.mix.tcam_network_sleep()
        self.soa.soa_partner.stop_single_partner("DoorService_server")
        self.soa.soa_partner.stop_single_partner("CentralLockService_server")
        self.soa.soa_partner.stop_single_partner("SeatService_server")
        self.soa.soa_partner.stop_single_partner("PedalService_server")
        logger.info("中控锁服务已下线")
        sleep(2)
        self.soa.soa_partner.start_single_partner(service="DoorService",role="server")
        self.soa.soa_partner.start_single_partner(service="CentralLockService",role="server")
        self.soa.soa_partner.start_single_partner(service="SeatService",role="server")
        self.soa.soa_partner.start_single_partner(service="PedalService",role="server")
        self.soa.soa_partner.empty_all()
        sleep(2)
        execid = self.tsp.rvc_remote_authorization()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry, send_time=10, timeout=20)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry, timeout=20)
        self.soa.notify_NotifyCentralLockSysInfo(LockStatus.AllLocked,TriggerSourceId.Telematices, update_eve=False)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kEntry, timeout=20)
        self.soa.notify_NotifyCentralLockSysInfo(LockStatus.AllLocked,TriggerSourceId.Telematices, update_eve=True)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kDefault, timeout=20)
        self.mix.default_func_param(['GetLockStatus'])

    @allure.title("远程控制-RVC_远程授权_锁状态无效_不响应取消授权")
    @pytest.mark.full
    def test_authorization_caseid_1988808(self, ecu):
        self.mix.set_func_param({'GetLockStatus':{'lock_status': LockStatus.Unlocked}})
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_remote_authorization()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetDoorCloseLock_req(cmd=LockCmd.UnLock, lock_req_source=LockReqSource.Talematics,find_key_type=FindKeyType.NoReq,timeout=20)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kUnlockWait,timeout=20)
        self.soa.notify_LockStatus(lock_sts=LockSts.Unlocked)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kReadyEntry, send_time=10, timeout=20)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        self.soa.notify_NotifyCentralLockSysInfo(LockStatus.AllLocked,TriggerSourceId.Telematices, update_eve=False)
        self.soa.check_NotifyRemoteAuthStartModeSts_event(sts=RemoteAuthSts.kDefault, timeout=20)
        self.mix.default_func_param(['GetLockStatus'])