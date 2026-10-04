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
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.common.data_handle import *
from xat_ecu.api.common.common import set_bench_vlan9_ip
from xat_ecu.legacy.protocol.ProtocolServerKeywords import ProtocolServerKeywords


@allure.feature("车控车设")
@allure.story("四域重启")
class TestHVAlarmCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["ObtDiagService_client","VehicleSetStatusService_client", 
                         "FotaMasterService_client","VehicleModeService_client",
                         ("CCPMasterService", "client" ,"CcpMasterService")])
        self.taskid = 19160
        set_bench_vlan9_ip('172.16.9.21')
        self.server_mock = ProtocolServerKeywords('doip', '172.16.9.21', 13400)
        self.server_mock.init_middleware()
        self.ssh.type_commands(DeviceName.BGM,"cd /data;cp debug_bak.sh debug.sh",timeout=30)
        self.ssh.type_commands(DeviceName.BGM,"cd /data;chmod 777 debug.sh",timeout=30)
        self.ssh.type_commands(DeviceName.BGM,"cd /data;chmod -R 777 sl",timeout=30)
        self.ssh.type_commands(DeviceName.BGM,"cd /data;/app/bin/swdl -nw 10 1",timeout=30)
        super().before_class(self, ecu)
        logger.info("before_class")
        sleep(2)

    def before_each_func(self, ecu):
        self.mix.back_ccp_status_to_Idle()
        self.tsp.back_vsp_to_Idle()
        self.io.bgm_diag_line_down()
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)
        super().before_each_func(ecu)
        self.io.bgm_diag_line_up()
        logger.info("before_each_func")
        pass

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        logger.info("after_each_func")
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.No)
        self.bus_comm.set_singal("bodycan","SwtlBodyFr02","SteerWhlScLeftButtonLeSteerWhlTouchSwt2",1)
        self.bus_comm.set_singal("bodycan","SwtrBodyFr01","SteerWhlScRightButtonRi",1)
        self.io.bgm_diag_line_up()
        self.ssh.type_commands(DeviceName.BGM,"cd /data;rm debug_script_executed_count")
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

    @allure.title("重启四域ACU执行重启_诊断方式失败处理")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985806?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test0906
    def test_climate_soa_caseid_1985805(self):
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.clear_accept_message_by_domain(source_address=0x0e90, target_address=0x1401)
        self.server_mock.doip_update_service_data_0x8001({
            0x1011: {
                0x27: {
                    0x01: ['6701123456']
                },
                0x10: {
                    0x01: ['5001'],
                    0x03: ['5003']
                },
                0x11: {
                    0x01: ['5101'],
                    0x03: ['5103'],
                    0x81: ['5181'],
                },
                0x14: {
                    0xff: []
                }
            },
        })
        self.io.bgm_diag_line_down()
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
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
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Reseting,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Success,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        logger.info("提示关键信息：{TCAM重启成功}")   
        
        self.server_mock.check_accept_message_count_by_domain(source_address=0x0e90, target_address=0x1401,check_data={"1101": 3})
        sleep(10)

    @allure.title("重启四域BNCM执行重启_诊断方式失败处理")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985806?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test0906
    def test_climate_soa_caseid_1985806(self):
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.clear_accept_message_by_domain(source_address=0x0e90, target_address=0x1023)
        self.server_mock.doip_update_service_data_0x8001({
            0x1011: {
                0x27: {
                    0x01: ['6701123456']
                },
                0x10: {
                    0x01: ['5001'],
                    0x03: ['5003']
                },
                0x11: {
                    0x01: ['5101'],
                    0x03: ['5103'],
                    0x81: ['5181'],
                },
                0x14: {
                    0xff: []
                }
            },
            0x1401: {
                0x11: {
                    0x01: ['5101'],
                    0x03: ['5103'],
                    0x81: ['5181'],
                }
            },
            0x1201: {
                0x11: {
                    0x01: ['5101'],
                    0x03: ['5103'],
                    0x81: ['5181'],
                }
            },
        })
        self.io.bgm_diag_line_down()
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
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
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Reseting,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Success,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        logger.info("提示关键信息：{TCAM重启成功}")  
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Success,autoState=AutoState.Reseting,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)  
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Success,autoState=AutoState.Success,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)  
        logger.info("提示关键信息：{ACU重启成功}") 
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Success,autoState=AutoState.Success,cockpitState=CdcState.Reseting,digitalKeyState=BncmState.Idle)  
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Success,autoState=AutoState.Success,cockpitState=CdcState.Success,digitalKeyState=BncmState.Idle)  
        logger.info("提示关键信息：{CDC重启成功}")   
        
        self.server_mock.check_accept_message_count_by_domain(source_address=0x0e90, target_address=0x1023,check_data={"1101": 3})
        sleep(10)

    @allure.title("重启四域ACU执行重启_诊断方式")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test0906
    def test_climate_soa_caseid_1985793(self):
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.doip_update_service_data_0x8001({
            0x1401: {
                0x27: {
                    0x01: ['6701123456']
                },
                0x10: {
                    0x01: ['5001'],
                    0x03: ['5003']
                },
                0x11: {
                    0x01: ['5101'],
                    0x03: ['5103'],
                    0x81: ['5181'],
                }
            }
        })
        self.io.bgm_diag_line_down()
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
        self.bus_comm.set_singal(bus="propulsioncan", msg="EcmPropComFr10", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.set_epb_sts(sts=3)
        self.bus_comm.set_singal("bodycan","SwtlBodyFr02","SteerWhlScLeftButtonLeSteerWhlTouchSwt2",2)
        self.bus_comm.set_singal("bodycan","SwtrBodyFr01","SteerWhlScRightButtonRi",2)
        sleep(4.5)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Triggering,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle) 
        sleep(5.0)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Fail,autoState=AutoState.Reseting,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Fail,autoState=AutoState.Success,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        
        sleep(10)

    @allure.title("重启四域CDC执行重启_诊断方式")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test0906
    def test_climate_soa_caseid_1985794(self):
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.doip_update_service_data_0x8001({
            0x1201: {
                0x11: {
                    0x01: ['5101'],
                    0x03: ['5103'],
                    0x81: ['5181'],
                }
            },
            0x1023: {
                0x11: {
                    0x01: ['5101'],
                    0x03: ['5103'],
                    0x81: ['5181'],
                }
            },
        })
        self.io.bgm_diag_line_down()
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
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
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Reseting,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Fail,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        logger.info("提示关键信息：{TCAM重启失败}")  
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Fail,autoState=AutoState.Reseting,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)  
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Fail,autoState=AutoState.Fail,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)  
        logger.info("提示关键信息：{ACU重启失败}") 
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Fail,autoState=AutoState.Fail,cockpitState=CdcState.Reseting,digitalKeyState=BncmState.Idle)  
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Fail,autoState=AutoState.Fail,cockpitState=CdcState.Success,digitalKeyState=BncmState.Idle)  
        logger.info("提示关键信息：{CDC重启成功}") 
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Fail,autoState=AutoState.Fail,cockpitState=CdcState.Success,digitalKeyState=BncmState.Reseting)  
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Fail,autoState=AutoState.Fail,cockpitState=CdcState.Success,digitalKeyState=BncmState.Success)  
        logger.info("提示关键信息：{BNCM重启成功}") 
        sleep(10)
  
    @allure.title("重启四域BNCM执行重启_诊断方式")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test0906
    def test_climate_soa_caseid_1985795(self):
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.doip_update_service_data_0x8001({
            0x1023: {
                0x11: {
                    0x01: ['5101'],
                    0x03: ['5103'],
                    0x81: ['5181'],
                }
            },
        })
        self.io.bgm_diag_line_down()
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
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
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Reseting,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Fail,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        logger.info("提示关键信息：{TCAM重启失败}")  
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Fail,autoState=AutoState.Reseting,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)  
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Fail,autoState=AutoState.Fail,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)  
        logger.info("提示关键信息：{ACU重启失败}") 
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Fail,autoState=AutoState.Fail,cockpitState=CdcState.Reseting,digitalKeyState=BncmState.Idle)  
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Fail,autoState=AutoState.Fail,cockpitState=CdcState.Fail,digitalKeyState=BncmState.Idle)  
        logger.info("提示关键信息：{CDC重启失败}") 
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Fail,autoState=AutoState.Fail,cockpitState=CdcState.Fail,digitalKeyState=BncmState.Reseting)  
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Fail,autoState=AutoState.Fail,cockpitState=CdcState.Fail,digitalKeyState=BncmState.Success)  
        logger.info("提示关键信息：{BNCM重启成功}")
        sleep(10)
    
    @allure.title("重启四域BGM执行重启_诊断方式")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test0906
    def test_climate_soa_caseid_1985796(self):
        global bgm_log_awakeup
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
        self.soa.event_check_reset_vehicle_sts(state=MainState.ConditionCheck,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Arbitration,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Idle,notify=Notification.ArbitrationFail,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        
        awakeup_log_last=self.ssh.read_bgm_jetlog()
        bgm_log_awakeup=awakeup_log_last[1]
        key_info = "reboot reason: 1"
        self.chek_key_info_in_awakeup_stage(key_info)
        sleep(10)

    @allure.title("重启四域CDC执行重启_诊断方式失败处理")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985803?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test0906
    def test_climate_soa_caseid_1985808(self):
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.doip_update_service_data_0x8001({
            0x1011: {
                0x27: {
                    0x01: ['6701123456']
                },
                0x10: {
                    0x01: ['5001'],
                    0x03: ['5003']
                },
                0x11: {
                    0x01: ['5101'],
                    0x03: ['5103'],
                    0x81: ['5181'],
                }
            },
            0x1401: {
                0x11: {
                    0x01: ['5101'],
                    0x03: ['5103'],
                    0x81: ['5181'],
                }
            },
            0x1201: {
               
            },
            0x1023: {
                0x11: {
                    0x01: ['5101'],
                    0x03: ['5103'],
                    0x81: ['5181'],
                }
            },
        })
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
                                               telestate=TeleState.Success,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle,timeout=1.0) 
        logger.info("提示关键信息：{TCAM重启成功}")  
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Success,autoState=AutoState.Reseting,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)  
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Success,autoState=AutoState.Success,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)  
        logger.info("提示关键信息：{ACU重启成功}") 
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Success,autoState=AutoState.Success,cockpitState=CdcState.Reseting,digitalKeyState=BncmState.Idle)  
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Success,autoState=AutoState.Success,cockpitState=CdcState.Fail,digitalKeyState=BncmState.Idle)  
        logger.info("提示关键信息：{CDC重启失败}") 
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Success,autoState=AutoState.Success,cockpitState=CdcState.Fail,digitalKeyState=BncmState.Reseting)  
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Success,autoState=AutoState.Success,cockpitState=CdcState.Fail,digitalKeyState=BncmState.Success)  
        logger.info("提示关键信息：{BNCM重启成功}") 
        sleep(10)
    
    @allure.title("重启四域BGM执行重启_诊断方式(成功)")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test0906
    def test_climate_soa_caseid_1985797_1985799_1985800_1985801(self):
        self.server_mock.doip_update_service_data_0x8001({
            0x1011: {
                0x27: {
                    0x01: ['6701123456']
                },
                0x10: {
                    0x01: ['5001'],
                    0x03: ['5003']
                },
                0x11: {
                    0x01: ['5101'],
                    0x03: ['5103'],
                    0x81: ['5181'],
                },
                0x14: {
                    0xff: []
                }
            },
            0x1401: {
                0x11: {
                    0x01: ['5101'],
                    0x03: ['5103'],
                    0x81: ['5181'],
                }
            },
            0x1201: {
                0x11: {
                    0x01: ['5101'],
                    0x03: ['5103'],
                    0x81: ['5181'],
                }
            },
            0x1023: {
                0x11: {
                    0x01: ['5101'],
                    0x03: ['5103'],
                    0x81: ['5181'],
                }
            },
        })
        global bgm_log_awakeup
        self.io.bgm_diag_line_down()
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
        self.soa.event_check_reset_vehicle_sts(state=MainState.ConditionCheck,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Arbitration,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Reseting,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Success,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        logger.info("提示关键信息：{TCAM重启成功}")  
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Success,autoState=AutoState.Reseting,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)  
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Success,autoState=AutoState.Success,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)  
        logger.info("提示关键信息：{ACU重启成功}") 
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Success,autoState=AutoState.Success,cockpitState=CdcState.Reseting,digitalKeyState=BncmState.Idle)  
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Success,autoState=AutoState.Success,cockpitState=CdcState.Success,digitalKeyState=BncmState.Idle)  
        logger.info("提示关键信息：{CDC重启成功}") 
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Success,autoState=AutoState.Success,cockpitState=CdcState.Success,digitalKeyState=BncmState.Reseting)  
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Success,autoState=AutoState.Success,cockpitState=CdcState.Success,digitalKeyState=BncmState.Success)  
        logger.info("提示关键信息：{BNCM重启成功}") 
        awakeup_log_last=self.ssh.read_bgm_jetlog_flag()
        bgm_log_awakeup=awakeup_log_last
        key_info = "save restart flag to false"
        key_info1 = "clear DTC: send 0x14FFFFFF to 1FFF"
        key_info2 = "MainState::kIdle"
        key_info3 = "clean up restart process"
        self.chek_key_info_in_awakeup_stage(key_info)
        self.chek_key_info_in_awakeup_stage(key_info1)
        self.chek_key_info_in_awakeup_stage(key_info2)
        self.chek_key_info_in_awakeup_stage(key_info3)
        sleep(10)

    @allure.title("重启四域TCAM执行重启_诊断方式")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test0906
    def test_climate_soa_caseid_1985792_1989400(self):
        self.server_mock.doip_update_service_data_0x8001({
            0x1011: {
                0x27: {
                    0x01: ['6701123456']
                },
                0x10: {
                    0x01: ['5001'],
                    0x03: ['5003']
                },
                0x11: {
                    0x01: ['5101'],
                    0x03: ['5103'],
                    0x81: ['5181'],
                }
            },
        })
        self.io.bgm_diag_line_down()
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
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
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Reseting,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Success,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)  
        
        sleep(10)
      
    
    @allure.title("重启四域TCAM执行重启_诊断方式失败处理")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test0906
    def test_climate_soa_caseid_1985807(self):
        self.server_mock.clear_mock_data_0x8001()
        global bgm_log_awakeup
        self.io.bgm_diag_line_down()
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
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
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Reseting,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Fail,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)  
        sleep(4.5)
        awakeup_log_last=self.ssh.read_bgm_jetlog_flag()
        bgm_log_awakeup=awakeup_log_last
        key_info = "send cmd to tcam fail"
        self.chek_key_info_in_awakeup_stage(key_info)
        sleep(10)
    
    @allure.title("重启四域TCAM执行重启_诊断方式1001重试次数")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test0906
    def test_climate_soa_caseid_1989401(self):
        self.server_mock.clear_mock_data_0x8001()
        self.io.bgm_diag_line_down()
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
        self.bus_comm.set_singal(bus="propulsioncan", msg="EcmPropComFr10", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.set_epb_sts(sts=3)
        self.bus_comm.set_singal("bodycan","SwtlBodyFr02","SteerWhlScLeftButtonLeSteerWhlTouchSwt2",2)
        self.bus_comm.set_singal("bodycan","SwtrBodyFr01","SteerWhlScRightButtonRi",2)
        self.server_mock.clear_accept_message_by_domain(source_address=0x0e90, target_address=0x1011)
        sleep(4.5)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Triggering,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.ConditionCheck,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.ConditionCheck,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Arbitration,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Reseting,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Fail,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)  
        
        self.server_mock.check_accept_message_count_by_domain(source_address=0x0e90, target_address=0x1011,check_data={"1001": 3})
        sleep(10)
    
    @allure.title("重启四域TCAM执行重启_诊断方式1003重试次数")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test0906
    def test_climate_soa_caseid_1989402(self):
        self.server_mock.clear_mock_data_0x8001()
        self.server_mock.clear_accept_message_by_domain(source_address=0x0e90, target_address=0x1011)
        self.server_mock.doip_update_service_data_0x8001({
            0x1011: {
                0x27: {
                    0x01: ['6701123456']
                },
                0x10: {
                    0x01: ['5001']
                }
            },
        })
        self.io.bgm_diag_line_down()
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
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
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Reseting,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Reseting,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Fail,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)  
        
        self.server_mock.check_accept_message_count_by_domain(source_address=0x0e90, target_address=0x1011,check_data={"1003": 3})
        sleep(10)
    

    @allure.title("四域重启_指令_触发成功")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_1985779(self):
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
        self.soa.send_check_reset_vehicle_sts(state=MainState.Idle,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.bus_comm.set_singal("bodycan","SwtlBodyFr02","SteerWhlScLeftButtonLeSteerWhlTouchSwt2",2)
        self.bus_comm.set_singal("bodycan","SwtrBodyFr01","SteerWhlScRightButtonRi",2)
        sleep(4.5)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Triggering,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.mix.sd_tester.reset_bgm()

    @allure.title("四域重启_指令_按键间隔过长")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_1985780(self):
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
        self.bus_comm.set_singal("bodycan","SwtlBodyFr02","SteerWhlScLeftButtonLeSteerWhlTouchSwt2",2)
        sleep(1.0)
        self.bus_comm.set_singal("bodycan","SwtrBodyFr01","SteerWhlScRightButtonRi",2)
        sleep(4.5)
        self.soa.send_check_reset_vehicle_sts(state=MainState.Idle,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)

    @allure.title("触发四域重启_失败_触发流程不正确")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_1985781(self):
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.No)
        self.soa.send_check_reset_vehicle_sts(state=MainState.Idle,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.bus_comm.set_singal("bodycan","SwtlBodyFr02","SteerWhlScLeftButtonLeSteerWhlTouchSwt2",2)
        self.bus_comm.set_singal("bodycan","SwtrBodyFr01","SteerWhlScRightButtonRi",2)
        sleep(4.5)
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
        self.soa.send_check_reset_vehicle_sts(state=MainState.Idle,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)

    @allure.title("触发四域重启_触发流程中断")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_1985782(self):
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
        self.soa.send_check_reset_vehicle_sts(state=MainState.Idle,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.bus_comm.set_singal("bodycan","SwtlBodyFr02","SteerWhlScLeftButtonLeSteerWhlTouchSwt2",2)
        self.bus_comm.set_singal("bodycan","SwtrBodyFr01","SteerWhlScRightButtonRi",2)
        sleep(2.5)
        self.bus_comm.set_singal("bodycan","SwtlBodyFr02","SteerWhlScLeftButtonLeSteerWhlTouchSwt2",1)
        sleep(4.5)
        self.soa.send_check_reset_vehicle_sts(state=MainState.Idle,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)

    @allure.title("四域重启_指令_触发成功")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_1985783(self):
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
        self.soa.event_check_reset_vehicle_sts(state=MainState.ConditionCheck,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Arbitration,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Idle,notify=Notification.ArbitrationFail,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.mix.sd_tester.reset_bgm()

    @allure.title("四域重启前提条件判断_P档不满足")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_1985784(self):
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
        self.soa.send_check_reset_vehicle_sts(state=MainState.Idle,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.bus_comm.set_singal("bodycan","SwtlBodyFr02","SteerWhlScLeftButtonLeSteerWhlTouchSwt2",2)
        self.bus_comm.set_singal("bodycan","SwtrBodyFr01","SteerWhlScRightButtonRi",2)
        self.bus_comm.set_singal(bus="propulsioncan", msg="EcmPropComFr10", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.bus_comm.set_epb_sts(sts=0)
        sleep(4.5)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Triggering,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)  
        self.soa.event_check_reset_vehicle_sts(state=MainState.ConditionCheck,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Idle,notify=Notification.NotInPark,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.mix.sd_tester.reset_bgm()
    
    @allure.title("重启四域执行失败_仲裁失败")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_1985790(self):
        self.io.bgm_diag_line_up()
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
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
        sleep(4.5)
        self.mix.sd_tester.reset_bgm()

    @allure.title("四域重启前提条件判断_P档不满足(第二次触发)")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_1989381(self):
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
        self.soa.send_check_reset_vehicle_sts(state=MainState.Idle,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.bus_comm.set_singal("bodycan","SwtlBodyFr02","SteerWhlScLeftButtonLeSteerWhlTouchSwt2",2)
        self.bus_comm.set_singal("bodycan","SwtrBodyFr01","SteerWhlScRightButtonRi",2)
        self.bus_comm.set_singal(bus="propulsioncan", msg="EcmPropComFr10", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.bus_comm.set_epb_sts(sts=0)
        sleep(4.5)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Triggering,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)  
        self.soa.event_check_reset_vehicle_sts(state=MainState.ConditionCheck,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Idle,notify=Notification.NotInPark,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.No)
        self.bus_comm.set_singal("bodycan","SwtlBodyFr02","SteerWhlScLeftButtonLeSteerWhlTouchSwt2",1)
        self.bus_comm.set_singal("bodycan","SwtrBodyFr01","SteerWhlScRightButtonRi",1)
        sleep(3.0)
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
        self.bus_comm.set_singal("bodycan","SwtlBodyFr02","SteerWhlScLeftButtonLeSteerWhlTouchSwt2",2)
        self.bus_comm.set_singal("bodycan","SwtrBodyFr01","SteerWhlScRightButtonRi",2)
        sleep(4.5)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Triggering,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)  
        self.soa.event_check_reset_vehicle_sts(state=MainState.ConditionCheck,notify=Notification.Idle,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Idle,notify=Notification.NotInPark,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.mix.sd_tester.reset_bgm()

    @allure.title("四域重启前提条件判断_通过_Usagemode=Driving")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_1985787(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
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
        self.soa.event_check_reset_vehicle_sts(state=MainState.Idle,notify=Notification.ShutDownFail,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.mix.sd_tester.reset_bgm()
    
    @allure.title("重启四域置位flag持久化")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_climate_soa_caseid_1985791(self):
        global bgm_log_awakeup
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
        self.soa.event_check_reset_vehicle_sts(state=MainState.ConditionCheck,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Arbitration,notify=Notification.RestartTriggered,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        self.soa.event_check_reset_vehicle_sts(state=MainState.Idle,notify=Notification.ArbitrationFail,
                                               telestate=TeleState.Idle,autoState=AutoState.Idle,cockpitState=CdcState.Idle,digitalKeyState=BncmState.Idle)
        awakeup_log_last=self.ssh.read_bgm_jetlog_flag()
        bgm_log_awakeup=awakeup_log_last
        key_info = "do restart. save reset flag: true"
        self.chek_key_info_in_awakeup_stage(key_info)
 
    @allure.title("四域重启_工程配置")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.debug
    def test_climate_soa_caseid_0001(self):
        ret = self.ssh.type_commands(DeviceName.BGM,"cat /sys/power/sys_resumed",timeout=30)
        logger.info(f"gggggggggggggggggg, {ret},{type(ret)}")
        if ret == "1":
            self.ssh.type_commands(DeviceName.BGM,"cd /data;cp debug_bak.sh debug.sh;chmod 777 debug.sh;chmod -R 777 sl;/app/bin/swdl -nw 10 1",timeout=30)
            self.mix.sd_tester.reset_bgm()
        else:
            logger.info(f"当前是冷启动 {ret},{type(ret)}")