#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_four_domain_restart.py
@Author      : shulin.zheng@jiduauto.com
@Time        : 2024/07/02 11:30
@Description : 四域重启
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
# from test_case.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_cases.legacy.bgm.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.common.data_handle import *
from xat_ecu.api.common.common import set_bench_vlan9_ip
from xat_ecu.legacy.protocol.ProtocolServerKeywords import ProtocolServerKeywords


@allure.feature("车控车设")
@allure.story("四域重启")
class TestHVAlarmCtrl(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update(["ObtDiagService_client","VehicleSetStatusService_client", "FotaMasterService_client",
                         "VehicleModeService_client",
                         ("V2TRoutingForwarder","client","V2TCcpForwarder"),
                         ("CCPMasterService", "client" ,"CcpMasterService")])
        self.ssh.ccp_skip_debug([Ccp_Skip_Debug.skip_verify,
                                 Ccp_Skip_Debug.skip_acu,
                                 Ccp_Skip_Debug.skip_cdc])
        self.ssh.type_commands(DeviceName.BGM,"cd /data;cp debug_bak.sh debug.sh",timeout=30)
        self.ssh.type_commands(DeviceName.BGM,"cd /data;chmod 777 debug.sh",timeout=30)
        self.ssh.type_commands(DeviceName.BGM,"cd /data;chmod -R 777 sl",timeout=30)
        self.ssh.type_commands(DeviceName.BGM,"cd /data;/app/bin/swdl -nw 10 1",timeout=30)
        logger.info("before_class")
        sleep(2)
        logger.info(self.taskid)
       
    def before_each_func(self, ecu):
        self.bus_comm.set_vehmtn()

        logger.info("before_each_func")
        # self.mix.sd_tester.reset_bgm()
        pass

    def after_each_func(self, ecu):
        logger.info("after_each_func")
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.No)
        self.bus_comm.set_singal(bus="propulsioncan", msg="EcmPropComFr10", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.set_epb_sts(sts=3)
        self.bus_comm.set_singal("bodycan","SwtlBodyFr02","SteerWhlScLeftButtonLeSteerWhlTouchSwt2",1)
        self.bus_comm.set_singal("bodycan","SwtrBodyFr01","SteerWhlScRightButtonRi",1)
        self.io.bgm_diag_line_up()
        self.ssh.type_commands(DeviceName.BGM,"cd /data;rm debug_script_executed_count")
        self.mix.sd_tester.reset_bgm()
        pass

    def after_class(self, ecu):
        self.server_mock.doip_sock_obj.tcp_server_sock.stop()
        self.ssh.type_commands(DeviceName.BGM,"cd /data;/app/bin/swdl -nw 10 0",timeout=30)
        super().after_class(self, ecu)
        logger.info("after_class")
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
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
        
    def chek_key_info_in_sleep_stage(self,key_info):
        global bgm_log_goto_sleep  
        logger.info("Check INFO:{}".format(key_info))
        check_result= self.find_info_from_log("sleep",key_info)
        if check_result:
            logger.info("查询到关键信息：{}".format(key_info))
            assert True
        else:
            logger.info("未能查询到关键信息：{}".format(key_info))
            assert False

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
    
    @allure.title("四域重启前提条件判断_通过_Usagemode=Driving")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_climate_soa_caseid_1985787(self):
        self.io.set_five_door_sts(Door.close)
        self.io.set_hood_sts(HoodSts.Close)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(0.3)
        self.bus_comm.check_usage_mode_status(UsageMode.DRIVING)
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
        self.soa.send_check_reset_vehicle_sts(state=MainState.Idle,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.io.bgm_diag_line_up()
        self.bus_comm.set_singal(bus="propulsioncan", msg="EcmPropComFr10", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.set_epb_sts(sts=3)
        self.bus_comm.set_singal("bodycan","SwtlBodyFr02","SteerWhlScLeftButtonLeSteerWhlTouchSwt2",2)
        self.bus_comm.set_singal("bodycan","SwtrBodyFr01","SteerWhlScRightButtonRi",2)
        sleep(4.5)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Triggering,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.ConditionCheck,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.ConditionCheck,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Arbitration,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Idle,notify=Notification.ArbitrationFail,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        
    @allure.title("重启四域TCAM执行重启_CAN方式")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985802?projectId=46"
    )
    @pytest.mark.full
    def test_climate_soa_caseid_1985802(self):
        self.io.bgm_diag_line_down()
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
        self.bus_comm.set_singal(bus="propulsioncan", msg="EcmPropComFr10", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.set_epb_sts(sts=3)
        self.bus_comm.set_singal("bodycan","SwtlBodyFr02","SteerWhlScLeftButtonLeSteerWhlTouchSwt2",2)
        self.bus_comm.set_singal("bodycan","SwtrBodyFr01","SteerWhlScRightButtonRi",2)
        sleep(4.5)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Triggering,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle,timeout=1.0)
        self.soa.event_check_reset_vehicle_sts(state=MainState.ConditionCheck,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle,timeout=1.0)
        check_list_1 = [
                    (self.bus_comm.ipdu.connectivitycanfd.BgmConnectivityFr22,'BGMMPUCtrlTCAMByte0',82,),
                    (self.bus_comm.ipdu.connectivitycanfd.BgmConnectivityFr22,'BGMMPUCtrlTCAMByte1',1,),
                    (self.bus_comm.ipdu.connectivitycanfd.BgmConnectivityFr22,'BGMMPUCtrlTCAM_UB',1,),
                ]
        check_list_2 = [
                    (self.bus_comm.ipdu.connectivitycanfd.BgmConnectivityFr22,'BGMMPUCtrlTCAMByte0',82,),
                    (self.bus_comm.ipdu.connectivitycanfd.BgmConnectivityFr22,'BGMMPUCtrlTCAMByte1',2,),
                    (self.bus_comm.ipdu.connectivitycanfd.BgmConnectivityFr22,'BGMMPUCtrlTCAM_UB',1,),
                ]
        check_list_3 = [
                    (self.bus_comm.ipdu.connectivitycanfd.BgmConnectivityFr22,'BGMMPUCtrlTCAMByte0',82,),
                    (self.bus_comm.ipdu.connectivitycanfd.BgmConnectivityFr22,'BGMMPUCtrlTCAMByte1',3,),
                    (self.bus_comm.ipdu.connectivitycanfd.BgmConnectivityFr22,'BGMMPUCtrlTCAM_UB',1,),
                ]
        self.bus_comm.ipdu.check_multiple_signals(check_list_1)
        self.bus_comm.ipdu.check_multiple_signals(check_list_2)
        self.bus_comm.ipdu.check_multiple_signals(check_list_3)

    @allure.title("重启四域ACU执行重启_CAN方式")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985803?projectId=46"
    )
    @pytest.mark.full
    def test_climate_soa_caseid_1985803(self):
        self.io.bgm_diag_line_down()
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
        self.bus_comm.set_singal(bus="propulsioncan", msg="EcmPropComFr10", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.set_epb_sts(sts=3)
        self.bus_comm.set_singal("bodycan","SwtlBodyFr02","SteerWhlScLeftButtonLeSteerWhlTouchSwt2",2)
        self.bus_comm.set_singal("bodycan","SwtrBodyFr01","SteerWhlScRightButtonRi",2)
        sleep(4.5)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Triggering,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle,timeout=0.0)
        self.soa.event_check_reset_vehicle_sts(state=MainState.ConditionCheck,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle,timeout=1.0)
        self.soa.event_check_reset_vehicle_sts(state=MainState.ConditionCheck,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle,timeout=1.0)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Arbitration,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle,timeout=1.0)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle,timeout=1.0)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Reseting,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle,timeout=1.0)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Fail,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle,timeout=1.0) 
        check_list_1 = [
                    (self.bus_comm.ipdu.adcanfd.BgmADCANFDFr31,'BGMMPUCtrlACUByte0',82,),
                    (self.bus_comm.ipdu.adcanfd.BgmADCANFDFr31,'BGMMPUCtrlACUByte1',1,),
                    (self.bus_comm.ipdu.adcanfd.BgmADCANFDFr31,'BGMMPUCtrlACU_UB',1,),
                ]
        check_list_2 = [
                    (self.bus_comm.ipdu.adcanfd.BgmADCANFDFr31,'BGMMPUCtrlACUByte0',82,),
                    (self.bus_comm.ipdu.adcanfd.BgmADCANFDFr31,'BGMMPUCtrlACUByte1',2,),
                    (self.bus_comm.ipdu.adcanfd.BgmADCANFDFr31,'BGMMPUCtrlACU_UB',1,),
                ]
        check_list_3 = [
                    (self.bus_comm.ipdu.adcanfd.BgmADCANFDFr31,'BGMMPUCtrlACUByte0',82,),
                    (self.bus_comm.ipdu.adcanfd.BgmADCANFDFr31,'BGMMPUCtrlACUByte1',3,),
                    (self.bus_comm.ipdu.adcanfd.BgmADCANFDFr31,'BGMMPUCtrlACU_UB',1,),
                ]
        self.bus_comm.ipdu.check_multiple_signals(check_list_1)
        self.bus_comm.ipdu.check_multiple_signals(check_list_2)
        self.bus_comm.ipdu.check_multiple_signals(check_list_3)
    
    @allure.title("重启四域CDC执行重启_CAN方式")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985803?projectId=46"
    )
    @pytest.mark.full
    def test_climate_soa_caseid_1985804(self):
        self.io.bgm_diag_line_down()
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
        self.bus_comm.set_singal(bus="propulsioncan", msg="EcmPropComFr10", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.set_epb_sts(sts=3)
        self.bus_comm.set_singal("bodycan","SwtlBodyFr02","SteerWhlScLeftButtonLeSteerWhlTouchSwt2",2)
        self.bus_comm.set_singal("bodycan","SwtrBodyFr01","SteerWhlScRightButtonRi",2)
        sleep(4.5)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Triggering,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle,timeout=1.0)
        self.soa.event_check_reset_vehicle_sts(state=MainState.ConditionCheck,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle,timeout=1.0)
        self.soa.event_check_reset_vehicle_sts(state=MainState.ConditionCheck,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle,timeout=1.0)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Arbitration,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle,timeout=1.0)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle,timeout=1.0)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Reseting,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle,timeout=1.0)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Fail,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle,timeout=1.0)
        sleep(4.0) 
        check_list_1 = [
                    (self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr24,'BGMMPUCtrlCDCByte0',82,),
                    (self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr24,'BGMMPUCtrlCDCByte1',1,),
                    (self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr24,'BGMMPUCtrlCDC_UB',1,),
                ]
        check_list_2 = [
                    (self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr24,'BGMMPUCtrlCDCByte0',82,),
                    (self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr24,'BGMMPUCtrlCDCByte1',2,),
                    (self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr24,'BGMMPUCtrlCDC_UB',1,),
                ]
        check_list_3 = [
                    (self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr24,'BGMMPUCtrlCDCByte0',82,),
                    (self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr24,'BGMMPUCtrlCDCByte1',3,),
                    (self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr24,'BGMMPUCtrlCDC_UB',1,),
                ]
        self.bus_comm.ipdu.check_multiple_signals(check_list_1)
        self.bus_comm.ipdu.check_multiple_signals(check_list_2)
        self.bus_comm.ipdu.check_multiple_signals(check_list_3)

    @allure.title("四域重启前提条件判断_FOTA条件不满足")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_climate_soa_caseid_1985785(self):
        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                                    FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.before_group_hv_ctl,
                                    FOTA_Skip_Debug.ecm3_down_hv,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.start_download,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ]) 
        self.ssh.update_ua_skip(DOMAIN.BGM, False)
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])
        self.io.bgm_diag_line_down()
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value 
        time.sleep(2)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)  
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.UPDATE.value, 240)
        time.sleep(30)
        #FOTA update
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
        self.soa.send_check_reset_vehicle_sts(state=MainState.Idle,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.bus_comm.set_singal(bus="propulsioncan", msg="EcmPropComFr10", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.set_epb_sts(sts=3)
        self.bus_comm.set_singal("bodycan","SwtlBodyFr02","SteerWhlScLeftButtonLeSteerWhlTouchSwt2",2)
        self.bus_comm.set_singal("bodycan","SwtrBodyFr01","SteerWhlScRightButtonRi",2)
        sleep(4.5)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Triggering,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)  
        self.soa.event_check_reset_vehicle_sts(state=MainState.ConditionCheck,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Idle,notify=Notification.Updating,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)

    @allure.title("四域重启前提条件判断_FOD条件不满足")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_climate_soa_caseid_1985786(self):
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
        self.fod_bench_config['preCheckUserIn']=1
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.ACTIVING.value,timeout=180)
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
        self.soa.send_check_reset_vehicle_sts(state=MainState.Idle,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.bus_comm.set_singal(bus="propulsioncan", msg="EcmPropComFr10", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.set_epb_sts(sts=3)
        self.bus_comm.set_singal("bodycan","SwtlBodyFr02","SteerWhlScLeftButtonLeSteerWhlTouchSwt2",2)
        self.bus_comm.set_singal("bodycan","SwtrBodyFr01","SteerWhlScRightButtonRi",2)
        sleep(4.5)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Triggering,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)  
        self.soa.event_check_reset_vehicle_sts(state=MainState.ConditionCheck,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Idle,notify=Notification.Updating,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)

    