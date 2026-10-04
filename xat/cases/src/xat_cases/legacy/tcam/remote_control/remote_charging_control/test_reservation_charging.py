#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pytest

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("互联服务/远程控制/远控设置预约充电充电")
@allure.story("远控设置预约充电充电")
class TestReservationpCharge(TestABCBase):
    def before_class(self, ecu):
        self.soa.update([ "VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server","SeatService_server", 
                         "HighVoltageService_server","VehicleTimeService_server",'HighVoltageAppService_server'])
        sleep(3)
        self.tsp.set_bench_config(self.tb_config["vid"], self.tb_config["tel"])


    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.io.tcam_kl15_up()
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_ChargingInfo(is_charging = True)

    def after_each_func(self, ecu):
        if ecu.testresult == 'Failure':
            logger.info('用例执行失败')
            sleep(10)
        self.io.tcam_kl15_up()
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_ChargingInfo(is_charging = True)
        time.sleep(1)

    def after_class(self, ecu):
        pass


    @allure.title("远程控制-RVC_远程预约充电_预约充电_CarMode_FACTORY")
    @pytest.mark.sanity
    def test_caseid_1990371(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程预约充电_预约充电_CarMode_TRANSPORT")
    @pytest.mark.sanity
    def test_caseid_1990372(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程预约充电_预约充电_CarMode_CRASH")
    @pytest.mark.sanity
    def test_caseid_1990373(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程预约充电_预约充电_CarMode_DYNO")
    @pytest.mark.sanity
    def test_caseid_1990374(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程预约充电_预约充电_MntnMode_True")
    @pytest.mark.sanity
    def test_caseid_1990375(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_预约充电_fota_UPDATE")
    @pytest.mark.sanity
    def test_caseid_1990376(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_预约充电_fota_ROLLBACK")
    @pytest.mark.sanity
    def test_caseid_1990377(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_预约充电_fota_QUERY")
    @pytest.mark.full
    def test_caseid_1990378(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_预约充电_fota_NEW_TASK")
    @pytest.mark.full
    def test_caseid_1990379(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_预约充电_fota_DOWNLOADING")
    @pytest.mark.full
    def test_caseid_1990380(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_预约充电_fota_ACTIVE")
    @pytest.mark.full
    def test_caseid_1990381(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_预约充电_fota_FAILED_NOT_DRIVING")
    @pytest.mark.full
    def test_caseid_1990382(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_预约充电_fota_SUCCESSFUL")
    @pytest.mark.full
    def test_caseid_1990383(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_fota_status(state=FOTAMasteSts.SUCCESSFUL)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_预约充电_fota_FAILED_DRIVING")
    @pytest.mark.full
    def test_caseid_1990384(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_DRIVING)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_预约充电_GearD")
    @pytest.mark.full
    def test_caseid_1990385(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.s2s_set_gear(Gear.Drv)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_预约充电_插枪状态_True")
    @pytest.mark.full
    def test_caseid_1990386(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_ChargingInfo(isConnect=True)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_预约充电_相同指令_开")
    @pytest.mark.full
    def test_caseid_1990387(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_ChargingInfo(isConnect=True)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  
        sleep(15)

    @allure.title("远程控制-RVC_远程预约充电_预约充电_相同指令_开和关")
    @pytest.mark.full
    def test_caseid_1990388(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_ChargingInfo(isConnect=True)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        execid = self.tsp.rvc_booking_ac_charge(op=-1,chargingfull=True,starttime=starttime,endtime=endtime)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  
        sleep(15)

    @allure.title("远程控制-RVC_远程预约充电_预约充电_不相同指令_开和修改充电SOC")
    @pytest.mark.full
    def test_caseid_1990390(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_ChargingInfo(isConnect=True)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault)
        execid1 = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        execid2 = self.tsp.rvc_charge_soc_settings(max_soc=850)
        # self.soa.check_SetChargeSoc_req_and_feedback_resp(soc=85,timeout=20)
        self.soa.notify_ChargingInfo(tar_soc=85)
        # self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1),f"TCAM远程控制上报到车云的结果校验失败"  
        assert self.tsp.log_search_remote_vehicle_control(execid=execid2),f"TCAM远程控制上报到车云的结果校验失败"  
        sleep(15)

    @allure.title("远程控制-RVC_远程预约充电_预约充电_网络唤醒失败")
    @pytest.mark.sanity
    def test_caseid_1990391(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        assert self.tsp.log_search_remote_vehicle_control("NetwakeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_预约充电_SOA服务启动失败")
    @pytest.mark.sanity
    def test_caseid_1990392(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault)
        self.soa.soa_partner.stop_single_partner("HighVoltageAppService_server")
        time.sleep(10)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        time.sleep(50)
        assert self.tsp.log_search_remote_vehicle_control("SOAFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      
        self.soa.soa_partner.start_single_partner(service="HighVoltageAppService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("HighVoltageAppService_server",timeout=30)    
 

 
    @allure.title("远程控制-RVC_远程预约充电_kBookOff_创建预约充电_reqSts=kBookActive")
    @pytest.mark.smoke
    def test_caseid_1990394(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookOff)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,
                                                               startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程预约充电_kBookOff_创建预约充电_reqSts=kBookDeactive")
    @pytest.mark.smoke
    def test_caseid_1990395(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookOff)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,
                                                               startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程预约充电_kBookOff_创建预约充电_15s内_reqSts=kDefault")
    @pytest.mark.sanity
    def test_caseid_1990396(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookOff)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,
                                                               startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault)
        sleep(10)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程预约充电_kBookOff_创建预约充电_15s内_reqSts=kBookOff")
    @pytest.mark.full
    def test_caseid_1990397(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookOff)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,
                                                               startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookOff)
        sleep(10)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程预约充电_kBookOff_创建预约充电_15s外_reqSts=kBookOff")
    @pytest.mark.full
    def test_caseid_1990398(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookOff)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,
                                                               startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)

        sleep(16)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookOff)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程预约充电_kBookOff_创建预约充电_15s外_reqSts=kDefault")
    @pytest.mark.full
    def test_caseid_1990399(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookOff)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,
                                                               startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)

        sleep(16)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程预约充电_kBookOff_创建预约充电_15s外_reqSts=kBookActive")
    @pytest.mark.full
    def test_caseid_1990400(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookOff)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,
                                                               startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)

        sleep(16)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程预约充电_kBookOff_创建预约充电_15s外_reqSts=kBookDeactive")
    @pytest.mark.full
    def test_caseid_1990401(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookOff)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,
                                                               startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)

        sleep(16)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程预约充电_kBookOff_创建预约充电_15s后不响应")
    @pytest.mark.full
    def test_caseid_1990402(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookOff)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,
                                                               startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)

        sleep(16)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程预约充电_kBookActive_关闭预约充电_reqSts=kDefault_关闭全流程")
    @pytest.mark.sanity
    def test_caseid_1990423(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)

        execid = self.tsp.rvc_booking_ac_charge(op=-1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)

        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCancel,source=DischargeSourceId.kRemoteControl,
                                                               startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程预约充电_kBookActive_关闭预约充电_reqSts=kBookOff")
    @pytest.mark.sanity
    def test_caseid_1990424(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)

        execid = self.tsp.rvc_booking_ac_charge(op=-1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)

        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCancel,source=DischargeSourceId.kRemoteControl,
                                                               startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookOff)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程预约充电_kBookActive_关闭预约充电_15s内_reqSts=kBookActive")
    @pytest.mark.sanity
    def test_caseid_1990425(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)

        execid = self.tsp.rvc_booking_ac_charge(op=-1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)

        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCancel,source=DischargeSourceId.kRemoteControl,
                                                               startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程预约充电_kBookActive_关闭预约充电_15s内_reqSts=kBookDeactive")
    @pytest.mark.full
    def test_caseid_1990426(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)

        execid = self.tsp.rvc_booking_ac_charge(op=-1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)

        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCancel,source=DischargeSourceId.kRemoteControl,
                                                               startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程预约充电_kBookActive_关闭预约充电_15s外_reqSts=kDefault")
    @pytest.mark.full
    def test_caseid_1990427(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)

        execid = self.tsp.rvc_booking_ac_charge(op=-1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)

        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCancel,source=DischargeSourceId.kRemoteControl,
                                                               startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        sleep(19)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程预约充电_kBookActive_关闭预约充电_15s外_reqSts=kBookOff")
    @pytest.mark.full
    def test_caseid_1990428(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)

        execid = self.tsp.rvc_booking_ac_charge(op=-1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)

        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCancel,source=DischargeSourceId.kRemoteControl,
                                                               startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        sleep(15)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookOff)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程预约充电_kBookActive_关闭预约充电_15s外_reqSts=kBookActive")
    @pytest.mark.full
    def test_caseid_1990429(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)

        execid = self.tsp.rvc_booking_ac_charge(op=-1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)

        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCancel,source=DischargeSourceId.kRemoteControl,
                                                               startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        sleep(15)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程预约充电_kBookActive_关闭预约充电_15s外_reqSts=kBookDeactive")
    @pytest.mark.full
    def test_caseid_1990430(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)

        execid = self.tsp.rvc_booking_ac_charge(op=-1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)

        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCancel,source=DischargeSourceId.kRemoteControl,
                                                               startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        sleep(15)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程预约充电_kBookActive_关闭预约充电_15s外_不响应")
    @pytest.mark.full
    def test_caseid_1990431(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)

        execid = self.tsp.rvc_booking_ac_charge(op=-1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)

        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCancel,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        sleep(15)

        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程预约充电_开始时间/结束时间_预约状态为1_全部一致_休眠")
    @pytest.mark.smoke
    def test_caseid_1990538(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,startTime=starttime,endTime=endtime)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程预约充电_开始时间/结束时间_预约状态为1_endTime不相等")
    @pytest.mark.sanity
    def test_caseid_1990539(self, ecu):
        # starttime = int(time.time() + 1)
        # endtime = starttime + 100
        starttime = next_occurrence_timestamp('11:00')
        endtime = next_occurrence_timestamp('23:00')
        notify_endtime = next_occurrence_timestamp('23:10')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)

        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,startTime=starttime,endTime=notify_endtime)
        sleep(10)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程预约充电_开始时间/结束时间_预约状态为1_startTime不相等")
    @pytest.mark.sanity
    def test_caseid_1990540(self, ecu):
        starttime = next_occurrence_timestamp('11:00')
        endtime = next_occurrence_timestamp('23:00')
        notify_starttime = get_timestamp_after_minutes(2*60,starttime)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)

        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,startTime=notify_starttime,endTime=endtime)
        sleep(10)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/结束时间_预约状态为1_全不相等")
    @pytest.mark.sanity
    def test_caseid_1990541(self, ecu):
        starttime = next_occurrence_timestamp('00:00')
        endtime = next_occurrence_timestamp('01:00')
        notify_starttime = get_timestamp_after_minutes(3*60,starttime)
        notify_endtime = get_timestamp_after_minutes(2*60,endtime)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)

        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,startTime=notify_starttime,endTime=notify_endtime)
        sleep(10)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/结束时间_预约状态为1_全相等_充满为止True")
    @pytest.mark.full
    def test_caseid_1990542(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)

        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,startTime=starttime,endTime=endtime,isToTargetSOCStop=True)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/结束时间_预约状态为1_全相等_充满为止False")
    @pytest.mark.full
    def test_caseid_1990543(self, ecu):
        starttime = next_occurrence_timestamp('00:00')
        endtime = next_occurrence_timestamp('01:00')
        # 大于24小时
        notify_starttime = get_timestamp_after_minutes(24*60,starttime)
        notify_endtime = get_timestamp_after_minutes(24*2*60,endtime)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,startTime=notify_starttime,endTime=notify_endtime,isToTargetSOCStop=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/结束时间_预约状态为2_15s外_全部一致")
    @pytest.mark.full
    def test_caseid_1990558(self, ecu):
        starttime = next_occurrence_timestamp('00:00')
        endtime = next_occurrence_timestamp('01:00')
        # 大于24小时
        notify_starttime = get_timestamp_after_minutes(24*60,starttime)
        notify_endtime = get_timestamp_after_minutes(24*2*60,endtime)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        sleep(16)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,startTime=notify_starttime,endTime=notify_endtime)
        sleep(10)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/结束时间_预约状态为2_全相等_充满为止False")
    @pytest.mark.full
    def test_caseid_1990559(self, ecu):
        starttime = next_occurrence_timestamp('00:00')
        endtime = next_occurrence_timestamp('01:00')
        # 大于24小时
        notify_starttime = get_timestamp_after_minutes(24*60, starttime)
        notify_endtime = get_timestamp_after_minutes(24*2*60, endtime)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,startTime=notify_starttime,endTime=notify_endtime)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/结束时间_预约状态为2_全相等_充满为止True")
    @pytest.mark.full
    def test_caseid_1990560(self, ecu):
        starttime = next_occurrence_timestamp('00:00')
        endtime = next_occurrence_timestamp('01:00')
        # 大于24小时
        notify_starttime = get_timestamp_after_minutes(24*60,starttime)
        notify_endtime = get_timestamp_after_minutes(24*60,endtime)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,startTime=notify_starttime,endTime=notify_endtime,isToTargetSOCStop=True)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/结束时间_预约状态为2_全不相等")
    @pytest.mark.sanity
    def test_caseid_1990561(self, ecu):
        starttime = next_occurrence_timestamp('00:00')
        endtime = next_occurrence_timestamp('01:00')
        # 大于24小时
        notify_starttime = get_timestamp_after_minutes(12*60,starttime)
        notify_endtime = get_timestamp_after_minutes(21*60,endtime)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,startTime=notify_starttime,endTime=notify_endtime)
        sleep(15)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/结束时间_预约状态为2_startTime不相等")
    @pytest.mark.sanity
    def test_caseid_1990562(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        notify_starttime = get_timestamp_after_minutes(1*60,starttime)
        notify_endtime = get_timestamp_after_minutes(2*60,endtime)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+120,endTime=endtime+120,repeatType=True,isToTargetSOCStop=False)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,startTime=notify_starttime,endTime=endtime)
        sleep(15)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/结束时间_预约状态为2_endTime不相等")
    @pytest.mark.sanity
    def test_caseid_1990563(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        notify_starttime = get_timestamp_after_minutes(18,starttime)
        notify_endtime = get_timestamp_after_minutes(14,endtime)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+120,endTime=endtime+360,repeatType=True,isToTargetSOCStop=False)
        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,startTime=starttime,endTime=notify_endtime)
        sleep(15)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/结束时间_预约状态为2_全部一致_休眠")
    @pytest.mark.sanity
    def test_caseid_1990564(self, ecu):
        starttime = next_occurrence_timestamp('22:44')
        endtime = next_occurrence_timestamp('23:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)
        self.mix.tcam_network_sleep()

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,startTime=starttime,endTime=endtime)
        sleep(15)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/结束时间_预约状态为1_15s外_全部一致")
    @pytest.mark.full
    def test_caseid_1990565(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)
        self.mix.tcam_network_sleep()

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        sleep(16)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,startTime=starttime,endTime=endtime)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/充满为止_预约状态为1_全相等_全流程休眠")
    @pytest.mark.smoke
    def test_caseid_1990569(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)
        self.mix.tcam_network_sleep()

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=starttime,endTime=endtime,isToTargetSOCStop=True)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/充满为止_预约状态为1_startTime不相等")
    @pytest.mark.full
    def test_caseid_1990570(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        notify_starttime = get_timestamp_after_minutes(11,starttime)
    #     notify_endtime = get_timestamp_after_minutes(14,endtime)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=notify_starttime,endTime=endtime,isToTargetSOCStop=True)
        sleep(10)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/充满为止_预约状态为1_endtime不相等")
    @pytest.mark.full
    def test_caseid_1990571(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        notify_starttime = get_timestamp_after_minutes(18,starttime)
        notify_endtime = get_timestamp_after_minutes(14,endtime)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)

        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=starttime,endTime=notify_endtime,isToTargetSOCStop=True)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/充满为止_预约状态为1_isToTargetSOCStop不相等")
    @pytest.mark.sanity
    def test_caseid_1990572(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)

        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=starttime,endTime=endtime,isToTargetSOCStop=False)
        sleep(15)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/充满为止_预约状态为1_2个时间不相等")
    @pytest.mark.full
    def test_caseid_1990573(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        notify_starttime = get_timestamp_after_minutes(18,starttime)
        notify_endtime = get_timestamp_after_minutes(66,endtime)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)

        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=notify_starttime,endTime=notify_endtime,isToTargetSOCStop=True)
        sleep(15)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/充满为止_预约状态为1_开始和充满为止不相等")
    @pytest.mark.full
    def test_caseid_1990574(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        notify_starttime = get_timestamp_after_minutes(18,starttime)
        notify_endtime = get_timestamp_after_minutes(66,endtime)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)

        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=notify_starttime,endTime=endtime,isToTargetSOCStop=False)
        sleep(15)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/充满为止_预约状态为1_结束和充满为止不相等")
    @pytest.mark.full
    def test_caseid_1990575(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        notify_starttime = get_timestamp_after_minutes(18,starttime)
        notify_endtime = get_timestamp_after_minutes(66,endtime)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)

        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=starttime,endTime=notify_endtime,isToTargetSOCStop=False)
        sleep(15)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/充满为止_预约状态为1_全部不相等")
    @pytest.mark.sanity
    def test_caseid_1990576(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        notify_starttime = get_timestamp_after_minutes(15,starttime)
        notify_endtime = get_timestamp_after_minutes(16,endtime)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)

        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=notify_starttime,endTime=notify_endtime,isToTargetSOCStop=False)
        sleep(15)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/充满为止_预约状态为1_15s后全相等")
    @pytest.mark.full
    def test_caseid_1990577(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        sleep(16)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=starttime,endTime=endtime,isToTargetSOCStop=True)
        
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/充满为止_预约状态为2_15s后全相等")
    @pytest.mark.full
    def test_caseid_1990578(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        sleep(16)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=starttime,endTime=endtime,isToTargetSOCStop=True)
        
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/充满为止_预约状态为2_全部不相等")
    @pytest.mark.sanity
    def test_caseid_1990579(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        notify_starttime = get_timestamp_after_minutes(3,starttime)
        notify_endtime = get_timestamp_after_minutes(3,endtime)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=notify_starttime,endTime=notify_endtime,isToTargetSOCStop=False)
        sleep(16)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/充满为止_预约状态为2_结束和充满为止不相等")
    @pytest.mark.full
    def test_caseid_1990580(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        notify_endtime = get_timestamp_after_minutes(3,endtime)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=starttime,endTime=notify_endtime,isToTargetSOCStop=False)
        sleep(16)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/充满为止_预约状态为2_开始和充满为止不相等")
    @pytest.mark.full
    def test_caseid_1990581(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        notify_starttime = get_timestamp_after_minutes(3,starttime)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=notify_starttime,endTime=endtime,isToTargetSOCStop=False)
        sleep(16)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/充满为止_预约状态为2_2个时间不相等")
    @pytest.mark.full
    def test_caseid_1990582(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        notify_starttime = get_timestamp_after_minutes(12*60,starttime)
        notify_enttime = get_timestamp_after_minutes(6*60,endtime)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=notify_starttime,endTime=notify_enttime,isToTargetSOCStop=True)
        sleep(16)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/充满为止_预约状态为2_isToTargetSOCStop不相等")
    @pytest.mark.sanity
    def test_caseid_1990583(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=starttime,endTime=endtime,isToTargetSOCStop=False)
        sleep(16)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/充满为止_预约状态为2_endTime不相等")
    @pytest.mark.full
    def test_caseid_1990584(self, ecu):
        starttime = next_occurrence_timestamp('08:44')
        endtime = next_occurrence_timestamp('06:53')
        notify_enttime = get_timestamp_after_minutes(5,endtime)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=starttime,endTime=notify_enttime,isToTargetSOCStop=True)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/充满为止_预约状态为2_startTime不相等")
    @pytest.mark.full
    def test_caseid_1990585(self, ecu):
        starttime = next_occurrence_timestamp('05:44')
        endtime = next_occurrence_timestamp('06:53')
        notify_starttime = get_timestamp_after_minutes(12*60,starttime)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime*60,endTime=endtime*60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=notify_starttime,endTime=endtime,isToTargetSOCStop=True)
        sleep(10)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/充满为止_预约状态为2_全相等休眠")
    @pytest.mark.smoke
    def test_caseid_1990586(self, ecu):
        starttime = next_occurrence_timestamp('04:44')
        endtime = next_occurrence_timestamp('05:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime*60,endTime=endtime*60,repeatType=True,isToTargetSOCStop=False)
        self.mix.tcam_network_sleep()

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=starttime,endTime=endtime,isToTargetSOCStop=True)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/结束时间_预约状态为1_全相等休眠")
    @pytest.mark.smoke
    def test_caseid_1990605(self, ecu):
        starttime = next_occurrence_timestamp('03:44')
        endtime = next_occurrence_timestamp('03:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)
        self.mix.tcam_network_sleep()

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=starttime,endTime=endtime,isToTargetSOCStop=False)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/结束时间_预约状态为1_全部一致不休眠")
    @pytest.mark.smoke
    def test_caseid_1990606(self, ecu):
        starttime = next_occurrence_timestamp('02:44')
        endtime = next_occurrence_timestamp('02:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=starttime,endTime=endtime,isToTargetSOCStop=False)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/结束时间_预约状态为2_全部一致_不休眠")
    @pytest.mark.sanity
    def test_caseid_1990609(self, ecu):
        starttime = next_occurrence_timestamp('00:44')
        endtime = next_occurrence_timestamp('01:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=starttime,endTime=endtime,isToTargetSOCStop=False)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/充满为止_预约状态为1_全相等_全流程不休眠")
    @pytest.mark.smoke
    def test_caseid_1990610(self, ecu):
        starttime = next_occurrence_timestamp('23:44')
        endtime = next_occurrence_timestamp('23:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=starttime,endTime=endtime,isToTargetSOCStop=True)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_开始时间/充满为止_预约状态为2_全相等不休眠")
    @pytest.mark.smoke
    def test_caseid_1990611(self, ecu):
        starttime = next_occurrence_timestamp('22:44')
        endtime = next_occurrence_timestamp('22:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=True,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kModify,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=True,repeatType=RepeatType.kDaily,timeout=10)
        
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=starttime,endTime=endtime,isToTargetSOCStop=True)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_创建预约充电_reqSts=kBookActive_时间不相等")
    @pytest.mark.smoke
    def test_caseid_1990623(self, ecu):
        starttime = next_occurrence_timestamp('21:44')
        endtime = next_occurrence_timestamp('21:53')
        notify_starttime = get_timestamp_after_minutes(5,starttime)
        notify_endtime = get_timestamp_after_minutes(5*60,endtime)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookOff,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=notify_starttime,endTime=notify_endtime,isToTargetSOCStop=False) 
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_创建预约充电_reqSts=kBookActive_isToTargetSOCStop不相等")
    @pytest.mark.smoke
    def test_caseid_1990624(self, ecu):
        starttime = next_occurrence_timestamp('20:44')
        endtime = next_occurrence_timestamp('20:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookOff,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,startTime=starttime,endTime=endtime,isToTargetSOCStop=True) 
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程预约充电_kBookDeactive_关闭预约充电_15s外_不响应")
    @pytest.mark.full
    def test_caseid_1990653(self, ecu):
        starttime = next_occurrence_timestamp('19:44')
        endtime = next_occurrence_timestamp('19:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=-1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCancel,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        
        sleep(15)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程预约充电_kBookDeactive_关闭预约充电_15s外_reqSts=kBookDeactive")
    @pytest.mark.full
    def test_caseid_1990654(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=-1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCancel,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        
        sleep(16)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程预约充电_kBookDeactive_关闭预约充电_15s外_reqSts=kBookActive")
    @pytest.mark.full
    def test_caseid_1990655(self, ecu):
        starttime = next_occurrence_timestamp('18:44')
        endtime = next_occurrence_timestamp('18:53')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=-1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCancel,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        
        sleep(16)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程预约充电_kBookDeactive_关闭预约充电_15s外_reqSts=kBookOff")
    @pytest.mark.full
    def test_caseid_1990656(self, ecu):
        starttime = next_occurrence_timestamp('17:12')
        endtime = next_occurrence_timestamp('17:44')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=-1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCancel,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        
        sleep(16)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookOff,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程预约充电_kBookDeactive_关闭预约充电_15s外_reqSts=kDefault")
    @pytest.mark.full
    def test_caseid_1990657(self, ecu):
        starttime = next_occurrence_timestamp('16:00')
        endtime = next_occurrence_timestamp('16:55')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=-1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCancel,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        
        sleep(16)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程预约充电_kBookDeactive_关闭预约充电_15s内_reqSts=kBookDeactive")
    @pytest.mark.full
    def test_caseid_1990658(self, ecu):
        starttime = next_occurrence_timestamp('15:15')
        endtime = next_occurrence_timestamp('15:50')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=-1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCancel,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)

        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)
        sleep(15)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程预约充电_kBookDeactive_关闭预约充电_15s内_reqSts=kBookActive")
    @pytest.mark.sanity
    def test_caseid_1990659(self, ecu):
        starttime = next_occurrence_timestamp('14:14')
        endtime = next_occurrence_timestamp('14:16')

        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=-1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCancel,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)

        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)
        sleep(15)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程预约充电_kBookDeactive_关闭预约充电_reqSts=kBookOff")
    @pytest.mark.sanity
    def test_caseid_1990660(self, ecu):
        starttime = next_occurrence_timestamp('13:15')
        endtime = next_occurrence_timestamp('13:44')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=-1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCancel,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)

        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookOff,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程预约充电_kBookDeactive_关闭预约充电_reqSts=kDefault_关闭全流程")
    @pytest.mark.smoke
    def test_caseid_1990661(self, ecu):
        starttime = next_occurrence_timestamp('12:12')
        endtime = next_occurrence_timestamp('12:15')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=-1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCancel,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)

        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程预约充电_kDefault_关闭预约充电_reqSts=kDefault_关闭全流程")
    @pytest.mark.smoke
    def test_caseid_1990662(self, ecu):
        starttime = next_occurrence_timestamp('11:00')
        endtime = next_occurrence_timestamp('11:10')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=-1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程预约充电_kBookOff_关闭预约充电_reqSts=kDefault_关闭全流程")
    @pytest.mark.smoke
    def test_caseid_1990663(self, ecu):
        starttime = next_occurrence_timestamp('10:00')
        endtime = next_occurrence_timestamp('10:10')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookOff,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=-1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程预约充电_kDefault_创建预约充电_15s后不响应")
    @pytest.mark.full
    def test_caseid_1990664(self, ecu):
        starttime = next_occurrence_timestamp('09:55')
        endtime = next_occurrence_timestamp('10:00')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)

        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        sleep(15)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程预约充电_kDefault_创建预约充电_15s外_reqSts=kBookDeactive")
    @pytest.mark.full
    def test_caseid_1990665(self, ecu):
        starttime = next_occurrence_timestamp('08:43')
        endtime = next_occurrence_timestamp('08:59')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)

        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        sleep(16)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程预约充电_kDefault_创建预约充电_15s外_reqSts=kBookActive")
    @pytest.mark.full
    def test_caseid_1990666(self, ecu):
        starttime = next_occurrence_timestamp('07:53')
        endtime = next_occurrence_timestamp('08:00')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)

        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        sleep(16)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      

    @allure.title("远程控制-RVC_远程预约充电_kDefault_创建预约充电_15s外_reqSts=kDefault")
    @pytest.mark.full
    def test_caseid_1990667(self, ecu):
        starttime = next_occurrence_timestamp('06:40')
        endtime = next_occurrence_timestamp('06:50')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)

        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        sleep(16)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程预约充电_kDefault_创建预约充电_15s外_reqSts=kBookOff")
    @pytest.mark.full
    def test_caseid_1990668(self, ecu):
        starttime = next_occurrence_timestamp('04:14')
        endtime = next_occurrence_timestamp('05:15')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)

        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        sleep(16)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookOff,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程预约充电_kDefault_创建预约充电_15s内_reqSts=kBookOff")
    @pytest.mark.full
    def test_caseid_1990669(self, ecu):
        starttime = next_occurrence_timestamp('03:55')
        endtime = next_occurrence_timestamp('04:00')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)

        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        sleep(4)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookOff,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)
        sleep(10)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程预约充电_kDefault_创建预约充电_15s内_reqSts=kDefault")
    @pytest.mark.sanity
    def test_caseid_1990670(self, ecu):
        starttime = next_occurrence_timestamp('02:22')
        endtime = next_occurrence_timestamp('02:23')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)

        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        sleep(4)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)
        sleep(10)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程预约充电_kDefault_创建预约充电_15s内_reqSts=kBookDeactive")
    @pytest.mark.smoke
    def test_caseid_1990671(self, ecu):
        starttime = next_occurrence_timestamp('01:00')
        endtime = next_occurrence_timestamp('01:10')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)

        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        sleep(4)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookDeactive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远程预约充电_kDefault_创建预约充电_15s内_reqSts=kBookActive")
    @pytest.mark.smoke
    def test_caseid_1990672(self, ecu):
        starttime = next_occurrence_timestamp('15:00')
        endtime = next_occurrence_timestamp('11:00')
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kDefault,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        execid = self.tsp.rvc_booking_ac_charge(op=1,chargingfull=False,starttime=starttime,endtime=endtime)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)

        self.soa.check_SetACBookCharging_req_and_feedback_resp(com_type=BookChargingCommandType.kCreate,source=DischargeSourceId.kRemoteControl,startTime=starttime,endTime=endtime,isToTargetSOCStop=False,repeatType=RepeatType.kDaily,timeout=10)
        sleep(4)
        self.soa.notify_BookChargingInfo(reqSts=ACBookChargingReqSts.kBookActive,source=DischargeSourceId.kRemoteControl,workSts=ACBookChargingWorkSts.kBookStsDefault,startTime=starttime+60,endTime=endtime+60,repeatType=True,isToTargetSOCStop=False)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    