#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_VehicleControlFaultService.py
@Time         :2023/05/28 17:20:31
@Author       :jishu.duan_ext
@Description  :
"""
import allure
import pytest
from time import sleep
from xat_ecu.legacy.driver.ssh_interface import command_send
from xat_ecu.legacy.common.data_type_handing import logger
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester


@allure.feature("SOA服务接口")
@allure.story("BGM应用/VehicleControlFaultService")
@pytest.mark.jishu
class TestVehicleControlFaultService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        for process_name in ["monitor_em2.sh", "em2", "s2s_service", "service_monitor"]:
            res = command_send(
                device_name="BGM",
                cmd=f"ps -ef |grep app |grep {process_name} |grep -v grep",
                timeout=60,
            )[1]
            pid = res.split()[1]
            command_send(device_name="BGM", cmd=f"kill -9 {pid}")
        sleep(10)
        command_send(device_name="BGM", cmd='su - service_monitor -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;/app/bin/service_monitor  -c /app/etc/service_monitor.json &"', timeout=15)
        
        self.partner = S2sBaseClass(
            [
                ("TyreService", "server"),
                ("VehicleControlFaultService", "client"),
                ("TailGateService", "server"),
                ("SteerWheelService", "server"),
                ("ClimateControlService", "server"),
                ("WiperService", "server"),
                ("SeatService", "server"),
                ("CTDService", "server"),
                ("HighVoltageService", "server"),
                ("LowVoltageService", "server"),
                ("ChassisService", "server"),
                ("DrivingAssistService", "server"),
                ("DoorService", "server"),
                ("ChargeLidService", "server"),
                ("PedalService", "server"),
                ("TailWingService", "server"),
                ("WindowService", "server"),
                ("LightService", "server"),
                ("PassiveSafetyService", "server"),
                ("WirelessPhoneChargingService", "server"),
            ])
        self.partner.method_default_timeout = 0.1
        self.partner.wait_for_service_reconnect(VEHICLECONTROLFAULT_SERVICE_CLIENT)
        
    def after_class(self, ecu):
        self.partner.stop_operators()
        self.bgm_power_off_and_on(self, timeout=1)
        self.nucapp.tcam_power_off()
        sleep(30)
        self.nucapp.tcam_power_on()
        sleep(180)
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.sd_tester.tester_present()
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06",
            3,
        )  # 车速值 3=有效
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06",
            0,
        )  # 车速值给了0 输入浮点数
        sleep(0.5)  # 车速m/s,36km/h对应10m/s 除以0.00391得到2557
        self.clear_all_fault()
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.sd_tester.stop_tester_present()
        super().after_each_func(ecu, start=False)

    def ck_FunctionFaultStatus_and_GetFunctionFaultStatus(
        self, hint, info, info1, timeout=3
    ):
        """校验指定warningMsgList事件,并请求WarningMsgList获取结果"""
        self.partner.ck_s2s_event(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {"infos": [{"functionName": hint, "zoneId": info, "faultId": info1}]},
            timeout=timeout,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "GetFunctionFaultStatus",
            {"function": [{"functionName": hint, "zoneId": info}]},
            {"out": [{"functionName": hint, "zoneId": info, "faultId": info1}]},
        )

    def clear_all_fault(self):
        self.partner.send_event_notify(
            "DoorService_server",
            "DoorFault",
            {"faults": [{"door": 4, "faultMsg": "", "fault": 0}]},
        )
        self.partner.send_event_notify(
            "ClimateControlService_server",
            "ClimateFault",
            {"faults": [{"faultId": 0, "faultMsg": ""}]},
        )
        self.partner.send_event_notify(
            "ClimateControlService_server",
            "coolantLowWarnInfo",
            {"info": {"eMotion": False, "battery": False}},
        )
        self.partner.send_event_notify(
            "SeatService_server",
            "SeatFault",
            {"faults": [{"faultId": 0, "faultMsg": "", "seatId": 12}]},
        )
        self.partner.send_event_notify(
            "TyreService_server",
            "TyreFault",
            {"faults": [{"fault": 0, "faultMsg": "", "type": 4}]},
        )
        self.partner.send_event_notify(
            "WiperService_server",
            "WiperFault",
            {"faults": [{"fault": 0, "faultMsg": "", "wiper": 0}]},
        )
        self.partner.send_event_notify(
            "WiperService_server",
            "HumidityInfo",
            {"faults": [{"fault": 0, "faultMsg": "", "wiper": 0}]},
        )
        self.partner.send_event_notify(
            "WiperService_server",
            "HumidityInfo",
            {"info": {"value": 50.0, "isValid": True}},
        )
        self.partner.send_event_notify(
            "SteerWheelService_server",
            "SteerWheelFault",
            {"faults": [{"fault": 0, "faultMsg": ""}]},
        )
        self.partner.send_event_notify(
            "CTDService_server",
            "alarmInfo",
            {"info": {"sysFault": False, "senFault": False, "intrScanFault": False}},
        )
        self.partner.send_event_notify(
            "HighVoltageService_server", "HighVoltageFault", {"faults": [0]}
        )
        self.partner.send_event_notify(
            "HighVoltageService_server",
            "hvInterLockInfo",
            {"info": {"fault": False, "l1Sts": False, "l2Sts": False, "l3Sts": False}},
        )
        self.partner.send_event_notify(
            "HighVoltageService_server",
            "batteryLowWarnInfo",
            {"info": {"isFirstWarn": False, "isSecondWarn": False}},
        )
        self.partner.send_event_notify(
            "HighVoltageService_server", "HVBatteryFault", {"state": False}
        )
        self.partner.send_event_notify(
            "HighVoltageService_server", "BatteryTemperatureLowState", {"state": False}
        )
        self.partner.send_event_notify(
            "LowVoltageService_server",
            "LVFault",  # 发送无故障
            {"faults": [{"faultId": 0, "faultMsg": ""}]},
        )
        self.partner.send_event_notify("WirelessPhoneChargingService_server",
           "WirelessChargingInfo", {"info":[{"zone": 0, "faults":[{"faultId": 0,"faultMsg":""}]},
                                            {"zone": 1, "faults":[{"faultId": 0,"faultMsg":""}]}]})
        self.partner.send_event_notify(
            "ChassisService_server", "absFailSts", {"sts": False}
        )
        self.partner.send_event_notify(
            "ChassisService_server", "brkRelsWarnReqSts", {"sts": False}
        )
        self.partner.send_event_notify(
            "ChassisService_server", "ChassisFault", {"faults": [0]}
        )
        self.partner.send_event_notify(
            "ChassisService_server", "NotifyBrkFldLvlWarnMsgStatus", {"msg": 0}
        )
        self.partner.send_event_notify(
            "ChassisService_server", "GearFault", {"faults": [0]}
        )
        self.partner.send_event_notify(
            "ChassisService_server", "SuspensionFailureSts",
                                        {"sts": {"value": 0, "validity": 0}}
        )
        self.partner.send_event_notify(
            "DrivingAssistService_server",
            "handOFFSts",
            {"sts": {"onSts": 0, "errSts": 0}},
        )
        self.partner.send_event_notify(
            "ChargeLidService_server",
            "ChargeLidFault",
            {"faults": [{"fault": 0, "faultMsg": ""}]},
        )
        self.partner.send_event_notify(
            "PedalService_server",
            "PedalFault",
            {"faults": [{"faultId": 0, "faultMsg": "", "id": 2}]},
        )
        self.partner.send_event_notify(
            "TailGateService_server",
            "TailGateFault",
            {"faults": [{"fault": 0, "faultMsg": "", "isFault": False}]},
        )
        self.partner.send_event_notify(
            "WindowService_server",
            "WindowFault",
            {"faults": [{"window": 4, "fault": 0, "faultMsg": ""}]},
        )
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}
                ]
            },
        )
        self.partner.send_event_notify(
            "PassiveSafetyService_server",
            "AirbagWarning",
            {"warn": {"isFault": False, "isValid": False}},
        )
        self.partner.empty_all(1)

    @allure.title("通知/获取功能故障状态_童锁故障")
    @pytest.mark.full
    def test_caseid_1979621(self):
        self.partner.send_event_notify(
            "DoorService_server",
            "DoorFault",
            {"faults": [{"door": 4, "faultMsg": "", "fault": 0}]},
        )
        self.partner.empty_all(0.5)

        self.partner.send_event_notify(
            "DoorService_server",
            "DoorFault",  # 左后儿童锁故障
            {"faults": [{"door": 2, "faultMsg": "", "fault": 1}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(3, 7, 11)
        self.partner.send_event_notify(
            "DoorService_server",
            "DoorFault",
            {"faults": [{"door": 2, "faultMsg": "", "fault": 0}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(3, 7, 0)

        self.partner.send_event_notify(
            "DoorService_server",
            "DoorFault",  # 右后儿童锁故障
            {"faults": [{"door": 3, "faultMsg": "", "fault": 1}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(3, 8, 11)
        self.partner.send_event_notify(
            "DoorService_server",
            "DoorFault",
            {"faults": [{"door": 3, "faultMsg": "", "fault": 0}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(3, 8, 0)

        self.partner.send_event_notify(
            "DoorService_server",
            "DoorFault",  # 全部儿童锁故障
            {
                "faults": [
                    {"door": 2, "faultMsg": "", "fault": 1},
                    {"door": 3, "faultMsg": "", "fault": 1},
                ]
            },
        )
        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 3, "zoneId": 7, "faultId": 11},
                    {"functionName": 3, "zoneId": 8, "faultId": 11},
                ]
            },method_args={"function": [{"functionName": 3, "zoneId": 0}]}
        )

        self.partner.send_event_notify(
            "DoorService_server",
            "DoorFault",
            {"faults": [{"door": 4, "faultMsg": "", "fault": 0}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(3, 0, 0)

    @allure.title("通知/获取功能故障状态_热保护")
    @pytest.mark.full
    def test_caseid_1979626(self):
        dic = {(0, 5): (16, 12), (1, 6): (16, 12), (2, 7): (16, 12), (3, 8): (16, 12)}
        for key, value in dic.items():
            logger.info(
                f"key={key}, value={value}, key0={key[0]}, key1={key[1]}, value0={value[0]}, value1={value[1]}"
            )
            self.partner.send_event_notify(
                "DoorService_server",
                "DoorFault",
                {"faults": [{"door": key[0], "faultMsg": "", "fault": value[0]}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(3, key[1], value[1])
            self.partner.send_event_notify(
                "DoorService_server",
                "DoorFault",
                {"faults": [{"door": key[0], "faultMsg": "", "fault": 0}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(3, key[1], 0)
        self.partner.send_event_notify(
            "DoorService_server",
            "DoorFault",
            {
                "faults": [
                    {"door": 0, "faultMsg": "", "fault": 16},
                    {"door": 1, "faultMsg": "", "fault": 16},
                    {"door": 2, "faultMsg": "", "fault": 16},
                    {"door": 3, "faultMsg": "", "fault": 16},
                ]
            },
        )
        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 3, "zoneId": 5, "faultId": 12},
                    {"functionName": 3, "zoneId": 6, "faultId": 12},
                    {"functionName": 3, "zoneId": 7, "faultId": 12},
                    {"functionName": 3, "zoneId": 8, "faultId": 12},
                ]
            },method_args={"function": [{"functionName": 3, "zoneId": 0}]}
        )

        self.partner.send_event_notify(
            "DoorService_server",
            "DoorFault",
            {"faults": [{"door": 4, "faultMsg": "", "fault": 0}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(3, 0, 0)

    @allure.title("通知/获取功能故障状态_车辆横摆角度不正常")
    @pytest.mark.full
    def test_caseid_1979634(self):
        dic = {(0, 5): (17, 13), (1, 6): (17, 13), (2, 7): (17, 13), (3, 8): (17, 13)}
        for key, value in dic.items():
            self.partner.send_event_notify(
                "DoorService_server",
                "DoorFault",
                {"faults": [{"door": key[0], "faultMsg": "", "fault": value[0]}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(3, key[1], value[1])
            self.partner.send_event_notify(
                "DoorService_server",
                "DoorFault",
                {"faults": [{"door": key[0], "faultMsg": "", "fault": 0}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(3, key[1], 0)

        self.partner.send_event_notify(
            "DoorService_server",
            "DoorFault",
            {
                "faults": [
                    {"door": 0, "faultMsg": "", "fault": 17},
                    {"door": 1, "faultMsg": "", "fault": 17},
                    {"door": 2, "faultMsg": "", "fault": 17},
                    {"door": 3, "faultMsg": "", "fault": 17},
                ]
            },
        )
        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 3, "zoneId": 5, "faultId": 13},
                    {"functionName": 3, "zoneId": 6, "faultId": 13},
                    {"functionName": 3, "zoneId": 7, "faultId": 13},
                    {"functionName": 3, "zoneId": 8, "faultId": 13},
                ]
            },method_args={"function": [{"functionName": 3, "zoneId": 0}]})

        self.partner.send_event_notify(
            "DoorService_server",
            "DoorFault",
            {"faults": [{"door": 4, "faultMsg": "", "fault": 0}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(3, 0, 0)

    @allure.title("通知/获取功能故障状态_ 道路倾斜角度不正常")
    @pytest.mark.full
    def test_caseid_1979635(self):
        dic = {(0, 5): (18, 14), (1, 6): (18, 14), (2, 7): (18, 14), (3, 8): (18, 14)}
        for key, value in dic.items():
            self.partner.send_event_notify(
                "DoorService_server",
                "DoorFault",
                {"faults": [{"door": key[0], "faultMsg": "", "fault": value[0]}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(3, key[1], value[1])
            self.partner.send_event_notify(
                "DoorService_server",
                "DoorFault",
                {"faults": [{"door": key[0], "faultMsg": "", "fault": 0}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(3, key[1], 0)
        self.partner.send_event_notify(
            "DoorService_server",
            "DoorFault",
            {
                "faults": [
                    {"door": 0, "faultMsg": "", "fault": 18},
                    {"door": 1, "faultMsg": "", "fault": 18},
                    {"door": 2, "faultMsg": "", "fault": 18},
                    {"door": 3, "faultMsg": "", "fault": 18},
                ]
            },
        )
        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 3, "zoneId": 5, "faultId": 14},
                    {"functionName": 3, "zoneId": 6, "faultId": 14},
                    {"functionName": 3, "zoneId": 7, "faultId": 14},
                    {"functionName": 3, "zoneId": 8, "faultId": 14},
                ]
            },method_args={"function": [{"functionName": 3, "zoneId": 0}]}
        )

        self.partner.send_event_notify(
            "DoorService_server",
            "DoorFault",
            {"faults": [{"door": 4, "faultMsg": "", "fault": 0}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(3, 0, 0)

    @allure.title("通知/获取功能故障状态_霍尔传感器故障")
    @pytest.mark.full
    def test_caseid_1979636(self):
        dic = {(0, 5): (19, 15), (1, 6): (19, 15), (2, 7): (19, 15), (3, 8): (19, 15)}
        for key, value in dic.items():
            self.partner.send_event_notify(
                "DoorService_server",
                "DoorFault",
                {"faults": [{"door": key[0], "faultMsg": "", "fault": value[0]}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(3, key[1], value[1])
            self.partner.send_event_notify(
                "DoorService_server",
                "DoorFault",
                {"faults": [{"door": key[0], "faultMsg": "", "fault": 0}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(3, key[1], 0)

        self.partner.send_event_notify(
            "DoorService_server",
            "DoorFault",
            {
                "faults": [
                    {"door": 0, "faultMsg": "", "fault": 19},
                    {"door": 1, "faultMsg": "", "fault": 19},
                    {"door": 2, "faultMsg": "", "fault": 19},
                    {"door": 3, "faultMsg": "", "fault": 19},
                ]
            },
        )
        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 3, "zoneId": 5, "faultId": 15},
                    {"functionName": 3, "zoneId": 6, "faultId": 15},
                    {"functionName": 3, "zoneId": 7, "faultId": 15},
                    {"functionName": 3, "zoneId": 8, "faultId": 15},
                ]
            },method_args={"function": [{"functionName": 3, "zoneId": 0}]},timeout=10)  

        self.partner.send_event_notify(
            "DoorService_server",
            "DoorFault",
            {"faults": [{"door": 4, "faultMsg": "", "fault": 0}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(3, 0, 0)

    @allure.title("通知/获取功能故障状态_电动门防玩激活")
    @pytest.mark.full
    def test_caseid_1979637(self):
        dic = {(0, 5): (11, 20), (1, 6): (11, 20), (2, 7): (11, 20), (3, 8): (11, 20)}
        for key, value in dic.items():
            self.partner.send_event_notify(
                "DoorService_server",
                "DoorFault",
                {"faults": [{"door": key[0], "faultMsg": "", "fault": value[0]}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(3, key[1], value[1])
            self.partner.send_event_notify(
                "DoorService_server",
                "DoorFault",
                {"faults": [{"door": key[0], "faultMsg": "", "fault": 0}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(3, key[1], 0)

        self.partner.send_event_notify(
            "DoorService_server",
            "DoorFault",
            {
                "faults": [
                    {"door": 0, "faultMsg": "", "fault": 11},
                    {"door": 1, "faultMsg": "", "fault": 11},
                    {"door": 2, "faultMsg": "", "fault": 11},
                    {"door": 3, "faultMsg": "", "fault": 11},
                ]
            },
        )
        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 3, "zoneId": 5, "faultId": 20},
                    {"functionName": 3, "zoneId": 6, "faultId": 20},
                    {"functionName": 3, "zoneId": 7, "faultId": 20},
                    {"functionName": 3, "zoneId": 8, "faultId": 20},
                ]
            },method_args= {"function": [{"functionName": 3, "zoneId": 0}]},timeout=10
        )

        self.partner.send_event_notify(
            "DoorService_server",
            "DoorFault",
            {"faults": [{"door": 4, "faultMsg": "", "fault": 0}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(3, 0, 0)

    @allure.title("通知/获取功能故障状态_轮胎故障")
    @pytest.mark.full
    def test_caseid_1892955(self):
        dic = {1: 60, 2: 61, 4: 62, 5: 63, 6: 64, 7: 65, 3: 66}
        dic1 = {5: 0, 6: 1, 7: 2, 8: 3}
        for zonid, vcid in dic1.items():
            for tyref, typeid in dic.items():
                logger.info(
                    f"当前type.{vcid},当前fault.{tyref},当前zonid.{zonid},当前typeid.{typeid}"
                )
                self.partner.send_event_notify(
                    "TyreService_server",
                    "TyreFault",
                    {"faults": [{"tyre": vcid, "faultMsg": "", "fault": tyref}]},
                )
                self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(
                    11, zonid, typeid
                )
                self.partner.send_event_notify(
                    "TyreService_server",
                    "TyreFault",
                    {"faults": [{"tyre": vcid, "faultMsg": "", "fault": 0}]},
                )
                self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(11, zonid, 0)

        self.partner.send_event_notify(
            "TyreService_server",
            "TyreFault",
            {
                "faults": [
                    {"tyre": 0, "faultMsg": "", "fault": 1},
                    {"tyre": 0, "faultMsg": "", "fault": 2},
                    {"tyre": 0, "faultMsg": "", "fault": 7},
                    {"tyre": 0, "faultMsg": "", "fault": 3},
                    {"tyre": 1, "faultMsg": "", "fault": 1},
                    {"tyre": 1, "faultMsg": "", "fault": 2},
                    {"tyre": 1, "faultMsg": "", "fault": 7},
                    {"tyre": 1, "faultMsg": "", "fault": 3},
                    {"tyre": 2, "faultMsg": "", "fault": 1},
                    {"tyre": 2, "faultMsg": "", "fault": 2},
                    {"tyre": 2, "faultMsg": "", "fault": 7},
                    {"tyre": 2, "faultMsg": "", "fault": 3},
                    {"tyre": 3, "faultMsg": "", "fault": 1},
                    {"tyre": 3, "faultMsg": "", "fault": 2},
                    {"tyre": 3, "faultMsg": "", "fault": 7},
                    {"tyre": 3, "faultMsg": "", "fault": 3},
                ]
            },
        )
        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 11, "zoneId": 5, "faultId": 60},
                    {"functionName": 11, "zoneId": 5, "faultId": 61},
                    {"functionName": 11, "zoneId": 5, "faultId": 65},
                    {"functionName": 11, "zoneId": 5, "faultId": 66},
                    {"functionName": 11, "zoneId": 6, "faultId": 60},
                    {"functionName": 11, "zoneId": 6, "faultId": 61},
                    {"functionName": 11, "zoneId": 6, "faultId": 65},
                    {"functionName": 11, "zoneId": 6, "faultId": 66},
                    {"functionName": 11, "zoneId": 7, "faultId": 60},
                    {"functionName": 11, "zoneId": 7, "faultId": 61},
                    {"functionName": 11, "zoneId": 7, "faultId": 65},
                    {"functionName": 11, "zoneId": 7, "faultId": 66},
                    {"functionName": 11, "zoneId": 8, "faultId": 60},
                    {"functionName": 11, "zoneId": 8, "faultId": 61},
                    {"functionName": 11, "zoneId": 8, "faultId": 65},
                    {"functionName": 11, "zoneId": 8, "faultId": 66},
                ]
            },method_args={"function": [{"functionName": 11, "zoneId": 0}]},timeout=10
        )

        self.partner.send_event_notify(
            "TyreService_server",
            "TyreFault",
            {"faults": [{"tyre": 4, "faultMsg": "", "fault": 0}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(11, 0, 0)

    @allure.title("通知/获取功能故障状态_方向盘故障")
    @pytest.mark.full
    def test_caseid_1892954(self):
        dic = {2: 80, 3: 81, 4: 82, 5: 83, 6: 84, 7: 85, 20: 86}
        for key, value in dic.items():
            self.partner.send_event_notify(
                "SteerWheelService_server",
                "SteerWheelFault",
                {"faults": [{"fault": key, "faultMsg": ""}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(7, 0, value)

        self.partner.send_event_notify(
            "SteerWheelService_server",
            "SteerWheelFault",
            {
                "faults": [
                    {"fault": 2, "faultMsg": ""},
                    {"fault": 3, "faultMsg": ""},
                    {"fault": 4, "faultMsg": ""},
                    {"fault": 5, "faultMsg": ""},
                    {"fault": 6, "faultMsg": ""},
                    {"fault": 7, "faultMsg": ""},
                    {"fault": 20, "faultMsg": ""},
                ]
            },
        )

        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 7, "zoneId": 0, "faultId": 80},
                    {"functionName": 7, "zoneId": 0, "faultId": 81},
                    {"functionName": 7, "zoneId": 0, "faultId": 82},
                    {"functionName": 7, "zoneId": 0, "faultId": 83},
                    {"functionName": 7, "zoneId": 0, "faultId": 84},
                    {"functionName": 7, "zoneId": 0, "faultId": 85},
                    {"functionName": 7, "zoneId": 0, "faultId": 86},]}, 
            method_args={"function": [{"functionName": 7, "zoneId": 0}]},timeout=10)
        self.partner.send_event_notify(
            "SteerWheelService_server",
            "SteerWheelFault",
            {"faults": [{"fault": 0, "faultMsg": ""}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(7, 0, 0)

    @allure.title("通知功能故障状态_遍历空调故障")
    @pytest.mark.sanity
    def test_caseid_1892951(self):
        dic = {
            6: 34,
            12: 35,
            8: 36,
            13: 37,
            7: 38,
            9: 39,
            10: 40,
            11: 41,
            2: 42,
        }
        for key, value in dic.items():
            self.partner.send_event_notify(
                "ClimateControlService_server",
                "ClimateFault",
                {"faults": [{"faultId": key, "faultIdMsg": ""}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(2, 0, value)

        self.partner.send_event_notify(
            "ClimateControlService_server",
            "coolantLowWarnInfo",  # 模拟发送空调，电驱回路冷却液液位低，空调，电驱回路冷却液液位低;
            {"info": {"eMotion": True, "battery": True}},
        )
        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 2, "zoneId": 0, "faultId": 44},
                    {"functionName": 2, "zoneId": 0, "faultId": 45},
                ]
            }, "GetFunctionFaultStatus",method_args ={"function": [{"functionName": 2, "zoneId": 0}]},timeout=10)

    @allure.title("通知/获取功能故障状态_空调系统故障")
    @pytest.mark.sanity
    def test_caseid_1892953(self):
        dic = {
            6: 34,
            12: 35,
            8: 36,
            13: 37,
            7: 38,
            9: 39,
            10: 40,
            11: 41,
            2: 42,
        }
        for key, value in dic.items():
            self.partner.send_event_notify(
                "ClimateControlService_server",
                "ClimateFault",
                {"faults": [{"faultId": key, "faultIdMsg": ""}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(2, 0, value)
            self.partner.send_event_notify(
                "ClimateControlService_server",
                "ClimateFault",
                {"faults": [{"faultId": 0, "faultIdMsg": ""}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(2, 0, 0)

        self.partner.send_event_notify(
            "ClimateControlService_server",
            "ClimateFault",  # 模拟发送空调，电驱回路冷却液液位低，空调，电驱回路冷却液液位低;
            {
                "faults": [
                    {"faultId": 6, "faultIdMsg": ""},
                    {"faultId": 12, "faultIdMsg": ""},
                    {"faultId": 8, "faultIdMsg": ""},
                    {"faultId": 13, "faultIdMsg": ""},
                    {"faultId": 7, "faultIdMsg": ""},
                    {"faultId": 9, "faultIdMsg": ""},
                    {"faultId": 10, "faultIdMsg": ""},
                    {"faultId": 11, "faultIdMsg": ""},
                    {"faultId": 2, "faultIdMsg": ""},
                ]
            },
        )
        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 2, "zoneId": 0, "faultId": 34},
                    {"functionName": 2, "zoneId": 0, "faultId": 35},
                    {"functionName": 2, "zoneId": 0, "faultId": 36},
                    {"functionName": 2, "zoneId": 0, "faultId": 37},
                    {"functionName": 2, "zoneId": 0, "faultId": 38},
                    {"functionName": 2, "zoneId": 0, "faultId": 39},
                    {"functionName": 2, "zoneId": 0, "faultId": 40},
                    {"functionName": 2, "zoneId": 0, "faultId": 41},
                    {"functionName": 2, "zoneId": 0, "faultId": 42},
                ]
            }, method_args={"function": [{"functionName": 2, "zoneId": 0}]},timeout=10)

    @allure.title("通知/获取功能故障状态_空调故障/获取冷却液液位信息")
    @pytest.mark.full
    def test_caseid_1892952(self):
        self.partner.send_event_notify(
            "ClimateControlService_server",
            "coolantLowWarnInfo",  # 模拟发送空调，电驱回路冷却液液位低，空调，电驱回路冷却液液位低;
            {"info": {"eMotion": True, "battery": False}},
        )
        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
             "FunctionFaultStatus",{"infos": [
                    {"functionName": 2, "zoneId": 0, "faultId": 44}
                ]},method_args={"function": [{"functionName": 2, "zoneId": 0}]},timeout=10)
        self.partner.send_event_notify(
            "ClimateControlService_server",
            "coolantLowWarnInfo",  # 模拟发送空调无故障，
            {"info": {"eMotion": False, "battery": False}},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(2, 0, 0)

        self.partner.send_event_notify(
            "ClimateControlService_server",
            "coolantLowWarnInfo",  # 模拟发送空调，电驱回路冷却液液位低，空调，电驱回路冷却液液位低;
            {"info": {"eMotion": True, "battery": True}},
        )
        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 2, "zoneId": 0, "faultId": 44},
                    {"functionName": 2, "zoneId": 0, "faultId": 45},
                ]
            },method_args={"function": [{"functionName": 2, "zoneId": 0}]},timeout=10)
        self.partner.send_event_notify(
            "ClimateControlService_server",
            "coolantLowWarnInfo",  # 模拟发送空调无故障，
            {"info": {"eMotion": False, "battery": False}},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(2, 0, 0)

    @allure.title("通知/获取功能故障状态_座椅故障")
    @pytest.mark.sanity
    def test_caseid_1892950(self):
        dic = {
            (4, 0): (5, 53),
            (5, 0): (5, 54),
            (7, 0): (5, 57),
            (8, 0): (5, 58),
            (4, 1): (6, 53),
            (5, 1): (6, 54),
            (7, 1): (6, 57),
            (8, 1): (6, 58),
        }
        for key, value in dic.items():
            self.partner.send_event_notify(
                "SeatService_server",
                "SeatFault",
                {"faults": [{"faultId": key[0], "faultMsg": "", "seatId": key[1]}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(
                6, value[0], value[1]
            )
            self.partner.send_event_notify(
                "SeatService_server",
                "SeatFault",
                {"faults": [{"faultId": 0, "faultMsg": "", "seatId": key[1]}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(6, value[0], 0)

        self.partner.send_event_notify(
            "SeatService_server",
            "SeatFault",
            {
                "faults": [
                    {"faultId": 4, "faultMsg": "", "seatId": 0},
                    {"faultId": 5, "faultMsg": "", "seatId": 0},
                    {"faultId": 7, "faultMsg": "", "seatId": 0},
                    {"faultId": 8, "faultMsg": "", "seatId": 0},
                    {"faultId": 4, "faultMsg": "", "seatId": 1},
                    {"faultId": 5, "faultMsg": "", "seatId": 1},
                    {"faultId": 7, "faultMsg": "", "seatId": 1},
                    {"faultId": 8, "faultMsg": "", "seatId": 1},
                ]
            },
        )
        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 6, "zoneId": 5, "faultId": 53},
                    {"functionName": 6, "zoneId": 5, "faultId": 54},
                    {"functionName": 6, "zoneId": 5, "faultId": 57},
                    {"functionName": 6, "zoneId": 5, "faultId": 58},
                    {"functionName": 6, "zoneId": 6, "faultId": 54},
                    {"functionName": 6, "zoneId": 6, "faultId": 54},
                    {"functionName": 6, "zoneId": 6, "faultId": 57},
                    {"functionName": 6, "zoneId": 6, "faultId": 58},
                ]
            }, method_args={"function": [{"functionName": 6, "zoneId": 0}]},timeout=10)
        self.partner.send_event_notify(
            "SeatService_server",
            "SeatFault",
            {"faults": [{"faultId": 0, "faultMsg": "", "seatId": 12}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(6, 0, 0)

    @allure.title("通知/获取功能故障状态_雨刮故障")
    @pytest.mark.sanity
    def test_caseid_1892949(self):
        dic = {2: 70, 3: 71, 4: 72, 5: 73}
        for key, value in dic.items():
            self.partner.send_event_notify(
                "WiperService_server",
                "WiperFault",
                {"faults": [{"fault": key, "faultMsg": "", "wiper": 0}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(13, 1, value)
            self.partner.send_event_notify(
                "WiperService_server",
                "WiperFault",
                {"faults": [{"fault": 0, "faultMsg": "", "wiper": 0}]},
            )

        self.partner.send_event_notify(
            "WiperService_server",
            "WiperFault",
            {
                "faults": [
                    {"fault": 2, "faultMsg": "", "wiper": 0},
                    {"fault": 3, "faultMsg": "", "wiper": 0},
                    {"fault": 4, "faultMsg": "", "wiper": 0},
                    {"fault": 5, "faultMsg": "", "wiper": 0},
                ]
            },
        )
        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 13, "zoneId": 1, "faultId": 70},
                    {"functionName": 13, "zoneId": 1, "faultId": 71},
                    {"functionName": 13, "zoneId": 1, "faultId": 72},
                    {"functionName": 13, "zoneId": 1, "faultId": 73},
                ]
            }, method_args={"function": [{"functionName": 13, "zoneId": 1}]},timeout=10)
        self.partner.send_event_notify(
            "WiperService_server",
            "WiperFault",
            {"faults": [{"fault": 0, "faultMsg": "", "wiper": 0}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(13, 1, 0)

    @allure.title("通知/获取功能故障状态_雨刮故障/车内湿度信息 ")
    @pytest.mark.sanity
    def test_caseid_1892948(self):
        self.partner.send_event_notify(
            "WiperService_server",
            "HumidityInfo",
            {"info": {"value": 100.0, "isValid": False}},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(13, 0, 74)
        self.partner.send_event_notify(
            "WiperService_server",
            "HumidityInfo",
            {"info": {"value": 100.0, "isValid": True}},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(13, 1, 0)

    @allure.title("通知/获取功能故障状态_遍历雨刮故障")
    @pytest.mark.sanity
    def test_caseid_1892947(self):
        dic = {2: 70, 3: 71, 4: 72, 5: 73}
        for key, value in dic.items():
            self.partner.send_event_notify(
                "WiperService_server",
                "WiperFault",
                {"faults": [{"fault": key, "faultMsg": "", "wiper": 0}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(13, 1, value)

        self.partner.send_event_notify(
            "WiperService_server",
            "HumidityInfo",
            {"info": {"value": 80.0, "isValid": False}},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(13, 0, 74)

        self.partner.send_event_notify(
            "WiperService_server",
            "WiperFault",
            {"faults": [{"fault": 0, "faultMsg": "", "wiper": 0}]},
        )
        self.partner.send_event_notify(
            "WiperService_server",
            "HumidityInfo",
            {"info": {"value": 100.0, "isValid": True}},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(13, 1, 0)

    @allure.title("通知/获取功能故障_CTD故障")
    @pytest.mark.full
    def test_caseid_1892946(self):  ##注意核对格式
        self.partner.send_event_notify(
            "CTDService_server",
            "alarmInfo",  # 防盗系统故障
            {"info": {"sysFault": True, "senFault": False, "intrScanFault": False}},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(35, 0, 92)

        self.partner.send_event_notify(
            "CTDService_server",
            "alarmInfo",  # 倾斜传感器故障
            {"info": {"sysFault": False, "senFault": True, "intrScanFault": False}},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(35, 0, 90)

        self.partner.send_event_notify(
            "CTDService_server",
            "alarmInfo",  # 入侵传感器存在系统故障
            {"info": {"sysFault": False, "senFault": False, "intrScanFault": True}},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(35, 0, 91)

        self.partner.send_event_notify(
            "CTDService_server",
            "alarmInfo",
            {"info": {"sysFault": True, "senFault": True, "intrScanFault": True}},
        )
        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 35, "zoneId": 0, "faultId": 90},
                    {"functionName": 35, "zoneId": 0, "faultId": 91},
                    {"functionName": 35, "zoneId": 0, "faultId": 92},
                ]
            },method_args={"function": [{"functionName": 35, "zoneId": 0}]},timeout=10)
        self.partner.send_event_notify(
            "CTDService_server",
            "alarmInfo",
            {"info": {"sysFault": False, "senFault": False, "intrScanFault": False}},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(35, 0, 0)

    @allure.title("通知/获取功能故障状态_遍历HighVoltage") 
    @pytest.mark.sanity
    def test_caseid_1892940(self):  # 高压服务全部接口
        dic = {1: 110, 2: 111, 3: 112, 4: 113, 5: 114}
        for key, value in dic.items():
            self.partner.send_event_notify(
                "HighVoltageService_server", "HighVoltageFault", {"faults": [key]}
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(16, 0, value)

        self.partner.send_event_notify(
            "HighVoltageService_server",
            "hvInterLockInfo",  # 发送高压互锁故障
            {"info": {"fault": True, "l1Sts": True, "l2Sts": True, "l3Sts": True}},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(16, 0, 115)
        self.partner.send_event_notify(
            "HighVoltageService_server",
            "batteryLowWarnInfo",
            {"info": {"color": 0, "lowTeLSts": 1, "isFirstWarn": True}},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(16, 0, 117)
        self.partner.send_event_notify(
            "HighVoltageService_server",
            "batteryLowWarnInfo",
            {"info": {"color": 0, "lowTeLSts": 1, "isSecondWarn": True}},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(16, 0, 118)
        self.partner.send_event_notify(
            "HighVoltageService_server", "HVBatteryFault", {"state": True}  # 发送电力电池故障
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(16, 0, 116)

        self.partner.send_event_notify(
            "HighVoltageService_server",
            "BatteryTemperatureLowState",  # 发送电池低温报警
            {"state": True},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(16, 0, 119)
        # 恢复无故障
        self.partner.send_event_notify(
            "HighVoltageService_server", "HighVoltageFault", {"faults": [0]}
        )
        self.partner.send_event_notify(
            "HighVoltageService_server",
            "hvInterLockInfo",
            {"info": {"fault": False, "l1Sts": False, "l2Sts": False, "l3Sts": False}},
        )
        self.partner.send_event_notify(
            "HighVoltageService_server",
            "batteryLowWarnInfo",  # 发送无故障
            {
                "info": {
                    "color": 0,
                    "lowTeLSts": 1,
                    "isFirstWarn": False,
                    " isSecondWarn": False,
                }
            },
        )
        self.partner.send_event_notify(
            "HighVoltageService_server", "HVBatteryFault", {"state": False}  # 发送无故障
        )
        self.partner.send_event_notify(
            "HighVoltageService_server",
            "BatteryTemperatureLowState",  # 发送无故障
            {"state": False},
        )

    @allure.title("通知/获取功能故障状态_HighVoltage/三电系统故障") 
    @pytest.mark.full
    def test_caseid_1892945(self):
        dic = {1: 110, 2: 111, 3: 112, 4: 113, 5: 114}
        for key, value in dic.items():
            self.partner.send_event_notify(
                "HighVoltageService_server", "HighVoltageFault", {"faults": [key]}
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(16, 0, value)
            self.partner.send_event_notify(
                "HighVoltageService_server", "HighVoltageFault", {"faults": [0]}
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(16, 0, 0)

        self.partner.send_event_notify(
            "HighVoltageService_server", "HighVoltageFault", {"faults": [1, 2, 3, 4, 5]}
        )
        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 16, "zoneId": 0, "faultId": 110},
                    {"functionName": 16, "zoneId": 0, "faultId": 111},
                    {"functionName": 16, "zoneId": 0, "faultId": 112},
                    {"functionName": 16, "zoneId": 0, "faultId": 113},
                    {"functionName": 16, "zoneId": 0, "faultId": 114},
                ]
            },method_args={"function": [{"functionName": 16, "zoneId": 0}]},timeout=10)
        self.partner.send_event_notify(
            "HighVoltageService_server", "HighVoltageFault", {"faults": [0]}
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(16, 0, 0)

    @allure.title("通知/获取功能故障状态_HighVoltage/高压互锁状态")
    @pytest.mark.full
    def test_caseid_1892944(self):  # 高压互锁故障#未过
        self.partner.send_event_notify(
            "HighVoltageService_server",
            "hvInterLockInfo",  # 发送高压互锁故障
            {"info": {"fault": True, "l1Sts": True, "l2Sts": True, "l3Sts": True}},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(16, 0, 115)
        self.partner.send_event_notify(
            "HighVoltageService_server",
            "hvInterLockInfo",  # 恢复故障
            {"info": {"fault": False, "l1Sts": False, "l2Sts": False, "l3Sts": False}},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(16, 0, 0)

    @allure.title("通知/获取功能故障状态_HighVoltage/高压电池电量低报警信息")
    @pytest.mark.full
    def test_caseid_1892943(self):
        self.partner.send_event_notify(
            "HighVoltageService_server",
            "batteryLowWarnInfo",
            {"info": {"color": 0, "lowTeLSts": 1, "isFirstWarn": True}},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(16, 0, 117)
        self.partner.send_event_notify(
            "HighVoltageService_server",
            "batteryLowWarnInfo",
            {"info": {"color": 0, "lowTeLSts": 1, "isSecondWarn": True}},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(16, 0, 118)
        self.partner.send_event_notify(
            "HighVoltageService_server",
            "batteryLowWarnInfo",  # 发送无故障
            {
                "info": {
                    "color": 0,
                    "lowTeLSts": 1,
                    "isFirstWarn": False,
                    "isSecondWarn": False,
                }
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(16, 0, 0)

    @allure.title("通知/获取功能故障状态_HighVoltage/高压电池故障状态")
    @pytest.mark.smoke
    def test_caseid_1892942(self):
        self.partner.send_event_notify(
            "HighVoltageService_server", "HVBatteryFault", {"state": True}  # 发送电力电池故障
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(16, 0, 116)
        self.partner.send_event_notify(
            "HighVoltageService_server", "HVBatteryFault", {"state": False}  # 恢复无故障
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(16, 0, 0)

    @allure.title("通知/获取功能故障状态_HighVoltage/电池低温报警状态")
    @pytest.mark.sanity
    def test_caseid_1892941(self):
        self.partner.send_event_notify(
            "HighVoltageService_server",
            "BatteryTemperatureLowState",  # 发送电池低温报警
            {"state": True},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(16, 0, 119)
        self.partner.send_event_notify(
            "HighVoltageService_server",
            "BatteryTemperatureLowState",  # 恢复无故障
            {"state": False},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(16, 0, 0)

    @allure.title("通知/获取功能故障状态_低压系统故障信息")
    @pytest.mark.full
    def test_caseid_1892939(self):
        # 发送驾驶中供电电压高；驾驶中供电电压高；电池继电器故障；电池传感器通信故障；电池传感器通信故障；
        # DCDC通信故障； DCDC硬件故障；DCDC温度异常；小电池电量低；小电池电量低； 低压故障未知
        dic = {
            1: 140,
            2: 141,
            3: 142,
            4: 143,
            5: 144,
            6: 145,
            7: 146,
            8: 147,
            9: 148,
            10: 149,
            11: 150,
        }
        for key, value in dic.items():
            self.partner.send_event_notify(
                "LowVoltageService_server",
                "LVFault",
                {"faults": [{"faultId": key, "faultMsg": ""}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(18, 0, value)

            self.partner.send_event_notify(
                "LowVoltageService_server",
                "LVFault",  # 发送无故障
                {"faults": [{"faultId": 0, "faultMsg": ""}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(18, 0, 0)

        self.partner.send_event_notify(
            "LowVoltageService_server",
            "LVFault",  # 发送无故障
            {
                "faults": [
                    {"faultId": 1, "faultMsg": ""},
                    {"faultId": 2, "faultMsg": ""},
                    {"faultId": 3, "faultMsg": ""},
                    {"faultId": 4, "faultMsg": ""},
                    {"faultId": 5, "faultMsg": ""},
                    {"faultId": 6, "faultMsg": ""},
                    {"faultId": 7, "faultMsg": ""},
                    {"faultId": 8, "faultMsg": ""},
                    {"faultId": 9, "faultMsg": ""},
                    {"faultId": 10, "faultMsg": ""},
                    {"faultId": 11, "faultMsg": ""},
                ]
            },
        )
        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 18, "zoneId": 0, "faultId": 140},
                    {"functionName": 18, "zoneId": 0, "faultId": 141},
                    {"functionName": 18, "zoneId": 0, "faultId": 142},
                    {"functionName": 18, "zoneId": 0, "faultId": 143},
                    {"functionName": 18, "zoneId": 0, "faultId": 144},
                    {"functionName": 18, "zoneId": 0, "faultId": 145},
                    {"functionName": 18, "zoneId": 0, "faultId": 146},
                    {"functionName": 18, "zoneId": 0, "faultId": 147},
                    {"functionName": 18, "zoneId": 0, "faultId": 148},
                    {"functionName": 18, "zoneId": 0, "faultId": 149},
                    {"functionName": 18, "zoneId": 0, "faultId": 150},
                ]
            },method_args={"function": [{"functionName": 18, "zoneId": 0}]},timeout=10)

        self.partner.send_event_notify(
            "LowVoltageService_server",
            "LVFault",  # 发送无故障
            {"faults": [{"faultId": 0, "faultMsg": ""}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(18, 0, 0)

    @allure.title("通知/获取功能故障状态_遍历Chassis故障")
    @pytest.mark.sanity
    def test_caseid_1892931(self):
        self.partner.send_event_notify(
            "ChassisService_server", "absFailSts", {"sts": True}  # 模拟发送ABS故障
        )

        self.partner.send_event_notify(
            "ChassisService_server", "brkRelsWarnReqSts", {"sts": True}
        )
        self.partner.send_event_notify(
            "ChassisService_server", "ChassisFault", {"faults": [1, 3, 4, 5, 6]}
        )

        self.partner.send_event_notify(
            "ChassisService_server", "NotifyBrkFldLvlWarnMsgStatus", {"msg": 1}
        )

        self.partner.send_event_notify(
            "ChassisService_server", "GearFault", {"faults": [1]}
        )

        self.partner.send_event_notify("ChassisService_server", "SuspensionFailureSts",
                                        {"sts": {"value": 1, "validity": 0}})
        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 15, "zoneId": 0, "faultId": 180},
                    {"functionName": 15, "zoneId": 0, "faultId": 181},
                    {"functionName": 15, "zoneId": 0, "faultId": 184},
                    {"functionName": 15, "zoneId": 0, "faultId": 186},
                    {"functionName": 15, "zoneId": 0, "faultId": 187},
                    {"functionName": 15, "zoneId": 0, "faultId": 188},
                    {"functionName": 15, "zoneId": 0, "faultId": 189},
                    {"functionName": 15, "zoneId": 0, "faultId": 190},
                    {"functionName": 15, "zoneId": 0, "faultId": 191},
                    {"functionName": 15, "zoneId": 0, "faultId": 192},
                ]
            },method_args={"function": [{"functionName": 15, "zoneId": 0}]},timeout=10)

    @allure.title("通知/获取功能故障状态_Chassis/ABS失效状态")
    @pytest.mark.sanity
    def test_caseid_1892937(self):  # 模拟ABS无故障
        self.partner.send_event_notify(
            "ChassisService_server", "absFailSts", {"sts": True}  # 模拟发送ABS故障
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(15, 0, 180)

        self.partner.send_event_notify(
            "ChassisService_server", "absFailSts", {"sts": False}  # 恢复无故障
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(15, 0, 0)

    @allure.title("通知/获取功能故障状态_驻车系统故障状态")
    @pytest.mark.full
    def test_casei_1892936(self):  # 模拟驻车系统故障
        self.partner.send_event_notify(
            "ChassisService_server", "brkRelsWarnReqSts", {"sts": True}
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(15, 0, 181)

        self.partner.send_event_notify(
            "ChassisService_server", "brkRelsWarnReqSts", {"sts": False}
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(15, 0, 0)

    @allure.title("通知/获取功能故障状态_ChassisFault")
    @pytest.mark.full
    def test_caseid_1892935(self):  # 模拟车速无效，模拟左前轮轮速失效，模拟右前车轮失效，模拟左后轮车轮失效，模拟右后轮车轮失效
        dic = {1: 188, 3: 189, 4: 190, 5: 191, 6: 192}
        for key, value in dic.items():
            self.partner.send_event_notify(
                "ChassisService_server", "ChassisFault", {"faults": key}
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(15, 0, value)
            self.partner.send_event_notify(
                "ChassisService_server", "ChassisFault", {"faults": [0]}  # 模拟恢复无故障
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(15, 0, 0)

        self.partner.send_event_notify(
            "ChassisService_server", "ChassisFault", {"faults": [1, 3, 4, 5, 6]}
        )
        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 15, "zoneId": 0, "faultId": 188},
                    {"functionName": 15, "zoneId": 0, "faultId": 189},
                    {"functionName": 15, "zoneId": 0, "faultId": 190},
                    {"functionName": 15, "zoneId": 0, "faultId": 191},
                    {"functionName": 15, "zoneId": 0, "faultId": 192},
                ]
            },method_args={"function": [{"functionName": 15, "zoneId": 0}]},timeout=10)
    
        self.partner.send_event_notify(
            "ChassisService_server", "ChassisFault", {"faults": [0]}  # 模拟恢复无故障
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(15, 0, 0)

    @allure.title("通知/获取功能故障_chassis/制动液位报警提示信息状态")
    @pytest.mark.full
    def test_caseid_1892934(self):  # 模拟发送制动液位故障；
        self.partner.send_event_notify(
            "ChassisService_server", "NotifyBrkFldLvlWarnMsgStatus", {"msg": 1}
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(15, 0, 184)

        self.partner.send_event_notify(
            "ChassisService_server", "NotifyBrkFldLvlWarnMsgStatus", {"msg": 0}
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(15, 0, 0)

    @allure.title("通知/获取功能故障状态_Chassis/换挡故障状态")
    @pytest.mark.full
    def test_caseid_1892933(self):  # 模拟发送换档故障；
        self.partner.send_event_notify(
            "ChassisService_server", "GearFault", {"faults": [1]}
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(15, 0, 186)

        self.partner.send_event_notify(
            "ChassisService_server", "GearFault", {"faults": [0]}
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(15, 0, 0)

    @allure.title("通知功能故障状态_Chassis/悬架故障状态")#v1.4接口修改待产品确认
    @pytest.mark.full
    def test_casei_1892932(self):#模拟发送悬架故障
        for sts in [3, 0, 2, 0, 1, 0]:
            self.partner.send_event_notify("ChassisService_server", "SuspensionFailureSts",
                                        {"sts": {"value": sts, "validity": 0}})
            if sts == 0:
                self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(15, 0, 0)
            else:
                self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(15, 0, 187)
        
        for sts in [3, 2, 1]:
            self.partner.send_event_notify("ChassisService_server", "SuspensionFailureSts",
                                        {"sts": {"value": sts, "validity": 0}})
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(15, 0, 187)
        self.partner.send_event_notify("ChassisService_server", "SuspensionFailureSts",
                                        {"sts": {"value": 0, "validity": 0}})
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(15, 0, 0)
        

    @allure.title("通知/获取功能故障状态_handOFFSts")
    @pytest.mark.full
    def test_caseid_1892930(self):  # 模拟发送标定错误，ECU和STW不统一故障；模拟发送系统错误；模拟发送永久错误
        dic = {3: 200, 4: 201, 5: 202}
        for key, value in dic.items():
            self.partner.send_event_notify(
                "DrivingAssistService_server",
                "handOFFSts",
                {"sts": {"onSts": 0, "errSts": key}},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(37, 0, value)
            self.partner.send_event_notify(
                "DrivingAssistService_server",
                "handOFFSts",
                {"sts": {"onSts": 0, "errSts": 0}},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(37, 0, 0)

    @allure.title("通知/获取功能故障状态_ChargeLid")  # 充电盖故障
    @pytest.mark.full
    def test_caseid_1979648(self):
        self.partner.send_event_notify(
            "ChargeLidService_server",
            "ChargeLidFault",
            {"faults": [{"fault": 1, "faultMsg": ""}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(1, 0, 1)

        self.partner.send_event_notify(
            "ChargeLidService_server",
            "ChargeLidFault",
            {"faults": [{"fault": 0, "faultMsg": ""}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(1, 0, 0)

    @allure.title("通知/获取功能故障状态_踏板故障/加速踏板")
    @pytest.mark.sanity
    def test_caseid_1979653(self):
        for i in range(1, 4):
            self.partner.send_event_notify(
                "PedalService_server",
                "PedalFault",
                {"faults": [{"faultId": i, "faultMsg": "", "id": 0}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(4, 0, 1)
            self.partner.send_event_notify(
                "PedalService_server",
                "PedalFault",
                {"faults": [{"faultId": 0, "faultMsg": "", "id": 0}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(4, 0, 0)

        self.partner.send_event_notify(
            "PedalService_server",
            "PedalFault",
            {
                "faults": [
                    {"faultId": 1, "faultMsg": "", "id": 0},
                    {"faultId": 2, "faultMsg": "", "id": 0},
                    {"faultId": 3, "faultMsg": "", "id": 0},
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(4, 0, 1)

        self.partner.send_event_notify(
            "PedalService_server",
            "PedalFault",
            {"faults": [{"faultId": 0, "faultMsg": "", "id": 2}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(4, 0, 0)

    @allure.title("通知/获取功能故障状态_踏板故障/刹车踏板")
    @pytest.mark.full
    def test_caseid_1979652(self):
        for i in range(1, 4):
            self.partner.send_event_notify(
                "PedalService_server",
                "PedalFault",
                {"faults": [{"faultId": i, "faultMsg": "", "id": 1}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(5, 0, 1)
            self.partner.send_event_notify(
                "PedalService_server",
                "PedalFault",
                {"faults": [{"faultId": 0, "faultMsg": "", "id": 1}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(5, 0, 0)

        self.partner.send_event_notify(
            "PedalService_server",
            "PedalFault",
            {
                "faults": [
                    {"faultId": 1, "faultMsg": "", "id": 1},
                    {"faultId": 2, "faultMsg": "", "id": 1},
                    {"faultId": 3, "faultMsg": "", "id": 1},
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(5, 0, 1)

        self.partner.send_event_notify(
            "PedalService_server",
            "PedalFault",
            {"faults": [{"faultId": 0, "faultMsg": "", "id": 2}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(5, 0, 0)

    @allure.title("通知/获取功能故障状态_TailGateFault/尾门故障信息")
    @pytest.mark.full
    def test_caseid_1979651(self):
        self.partner.send_event_notify(
            "TailGateService_server",
            "TailGateFault",
            {"faults": [{"fault": 1, "faultMsg": "", "isFault": True}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(9, 0, 1)
        sleep(1)

        self.partner.send_event_notify(
            "TailGateService_server",
            "TailGateFault",
            {"faults": [{"fault": 0, "faultMsg": "", "isFault": False}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(9, 0, 0)

    @allure.title("通知/获取功能故障状态_TailWingFault/尾翼故障信息")
    @pytest.mark.full
    def test_caseid_1979650(self):
        self.partner.send_event_notify(
            "TailWingService_server",
            "TailWingFault",
            {"faults": [{"fault": 7, "faultMsg": ""}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(10, 0, 1)

        self.partner.send_event_notify(
            "TailWingService_server",
            "TailWingFault",
            {"faults": [{"fault": 0, "faultMsg": ""}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(10, 0, 0)

    @allure.title("通知/获取功能故障状态_WindowFault/车窗故障信息")
    @pytest.mark.full
    def test_caseid_1979649(self):
        dic = {
            0: 5,
            1: 6,
            2: 7,
            3: 8,
        }
        for key, value in dic.items():
            self.partner.send_event_notify(
                "WindowService_server",
                "WindowFault",
                {"faults": [{"window": key, "fault": 3, "faultMsg": ""}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(12, value, 1)
            self.partner.send_event_notify(
                "WindowService_server",
                "WindowFault",
                {"faults": [{"window": key, "fault": 0, "faultMsg": ""}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(12, value, 0)
            self.partner.send_event_notify(
                "WindowService_server",
                "WindowFault",
                {"faults": [{"window": key, "fault": 4, "faultMsg": ""}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(12, value, 1)
            self.partner.send_event_notify(
                "WindowService_server",
                "WindowFault",
                {"faults": [{"window": key, "fault": 0, "faultMsg": ""}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(12, value, 0)

        self.partner.send_event_notify(
            "WindowService_server",
            "WindowFault",
            {
                "faults": [
                    {"window": 0, "fault": 3, "faultMsg": ""},
                    {"window": 1, "fault": 3, "faultMsg": ""},
                    {"window": 2, "fault": 3, "faultMsg": ""},
                    {"window": 3, "fault": 3, "faultMsg": ""},
                    {"window": 0, "fault": 4, "faultMsg": ""},
                    {"window": 1, "fault": 4, "faultMsg": ""},
                    {"window": 2, "fault": 4, "faultMsg": ""},
                    {"window": 3, "fault": 4, "faultMsg": ""},
                ]
            },
        )
        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 12, "zoneId": 5, "faultId": 1},
                    {"functionName": 12, "zoneId": 6, "faultId": 1},
                    {"functionName": 12, "zoneId": 7, "faultId": 1},
                    {"functionName": 12, "zoneId": 8, "faultId": 1},
                ]
            },method_args={"function": [{"functionName": 12, "zoneId": 0}]},timeout=10
        )
        self.partner.send_event_notify(
            "WindowService_server",
            "WindowFault",
            {"faults": [{"window": 4, "fault": 0, "faultMsg": ""}]},
        )

        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(12, 0, 0)

    @allure.title("通知/获取功能故障状态_LightFault/LowBeam近光灯")
    @pytest.mark.full
    def test_caseid_1979690(self):
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 1, "faultMsg": "", "light": {"type": 6, "zoneId": 0}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(20, 0, 1)

        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(20, 0, 0)

    @allure.title("通知/获取功能故障状态_LightFault/HighBeam远光灯")
    @pytest.mark.full
    def test_caseid_1979689(self):
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 1, "faultMsg": "", "light": {"type": 5, "zoneId": 0}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(21, 0, 1)

        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(21, 0, 0)

    @allure.title("通知/获取功能故障状态_LightFault/FogLamp雾灯")  ##case注意
    @pytest.mark.full
    def test_caseid_1979688(self):
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 1, "faultMsg": "", "light": {"type": 4, "zoneId": 9}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(22, 1, 1)
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 0, "faultMsg": "", "light": {"type": 4, "zoneId": 9}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(22, 1, 0)
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 1, "faultMsg": "", "light": {"type": 4, "zoneId": 10}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(22, 2, 1)
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 0, "faultMsg": "", "light": {"type": 4, "zoneId": 10}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(22, 2, 0)
        self.partner.empty_all(0.5)
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 1, "faultMsg": "", "light": {"type": 4, "zoneId": 9}},
                    {"fault": 1, "faultMsg": "", "light": {"type": 4, "zoneId": 10}},
                ]
            },
        )
        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 22, "zoneId": 1, "faultId": 1},
                    {"functionName": 22, "zoneId": 2, "faultId": 1},
                ]
            },method_args={"function": [{"functionName": 22, "zoneId": 0}]},timeout=10)
     
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(22, 0, 0)
        self.partner.empty_all(0.5)

    @allure.title("通知/获取功能故障状态_LightFault/PositionLamp位置灯")  ##case注意
    @pytest.mark.full
    def test_caseid_1979687(self):
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 1, "faultMsg": "", "light": {"type": 11, "zoneId": 9}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(23, 1, 1)
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 0, "faultMsg": "", "light": {"type": 11, "zoneId": 9}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(23, 1, 0)
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 1, "faultMsg": "", "light": {"type": 11, "zoneId": 10}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(23, 2, 1)
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 0, "faultMsg": "", "light": {"type": 11, "zoneId": 10}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(23, 2, 0)

        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 1, "faultMsg": "", "light": {"type": 11, "zoneId": 9}},
                    {"fault": 1, "faultMsg": "", "light": {"type": 11, "zoneId": 10}},
                ]
            },
        )
        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 23, "zoneId": 1, "faultId": 1},
                    {"functionName": 23, "zoneId": 2, "faultId": 1},
                ]
            },method_args={"function": [{"functionName": 23, "zoneId": 0}]},timeout=10
        )
       
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 0, "faultMsg": "", "light": {"type": 11, "zoneId": 9}},
                    {"fault": 1, "faultMsg": "", "light": {"type": 11, "zoneId": 10}},
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(23, 2, 1)
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 0, "faultMsg": "", "light": {"type": 11, "zoneId": 9}},
                    {"fault": 0, "faultMsg": "", "light": {"type": 11, "zoneId": 10}},
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(23, 2, 0)

    @allure.title("通知/获取功能故障状态_LightFault/BrakeLamp刹车灯")
    @pytest.mark.full
    def test_caseid_1979686(self):
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 1, "faultMsg": "", "light": {"type": 0, "zoneId": 0}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(24, 0, 1)

        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(24, 0, 0)

    @allure.title("通知/获取功能故障状态_LightFault/ReverseLamp倒车灯")
 
    @pytest.mark.full
    def test_caseid_1979684(self):
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 1, "faultMsg": "", "light": {"type": 8, "zoneId": 0}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(25, 0, 1)

        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(25, 0, 0)

    @allure.title("通知/获取功能故障状态_LightFault/DaytimeLamp日间行车灯") 
    @pytest.mark.full
    def test_caseid_1979683(self):
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 1, "faultMsg": "", "light": {"type": 3, "zoneId": 0}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(26, 0, 1)

        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(26, 0, 0)

    @allure.title("通知/获取功能故障状态_LightFault/WelcomeLight迎宾灯")
    @pytest.mark.full
    def test_caseid_1979682(self):
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 1, "faultMsg": "", "light": {"type": 12, "zoneId": 0}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(28, 0, 1)

        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(28, 0, 0)

    @allure.title("通知/获取功能故障状态_LightFault/AdaptiveFrontLight自适应前照灯系统(功能激活)")
    @pytest.mark.full
    def test_caseid_1979681(self):
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 1, "faultMsg": "", "light": {"type": 36, "zoneId": 0}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(29, 0, 1)

        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(29, 0, 0)

    @allure.title("通知/获取功能故障状态_LightFault/AutomaticHeadlampLevelf大灯水平高度调节(功能激活)")
    @pytest.mark.full
    def test_caseid_1979680(self):
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 1, "faultMsg": "", "light": {"type": 37, "zoneId": 0}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(30, 0, 1)

        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(30, 0, 0)

    @allure.title("通知/获取功能故障状态_LightFault/TurnLamp转向灯")
    @pytest.mark.full
    def test_caseid_1979678(self):  ####
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 1, "faultMsg": "", "light": {"type": 10, "zoneId": 12}}
                ]
            },
        )
        sleep(1)
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(31, 3, 1)
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 0, "faultMsg": "", "light": {"type": 10, "zoneId": 12}}
                ]
            },
        )
        sleep(1)
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(31, 3, 0)
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 1, "faultMsg": "", "light": {"type": 10, "zoneId": 13}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(31, 4, 1)
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 0, "faultMsg": "", "light": {"type": 10, "zoneId": 13}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(31, 4, 0)
        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 1, "faultMsg": "", "light": {"type": 10, "zoneId": 12}},
                    {"fault": 1, "faultMsg": "", "light": {"type": 10, "zoneId": 13}},
                ]
            },
        )
        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 31, "zoneId": 3, "faultId": 1},
                    {"functionName": 31, "zoneId": 4, "faultId": 1},
                ]
            },method_args={"function": [{"functionName": 31, "zoneId": 0}]},timeout=10
        )

        self.partner.send_event_notify(
            "LightService_server",
            "LightFault",
            {
                "faults": [
                    {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}
                ]
            },
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(31, 0, 0)

    @allure.title("通知/获取功能故障状态_Airbag/安全气囊")
    @pytest.mark.full
    def test_caseid_1979677(self):
        self.partner.send_event_notify(
            "PassiveSafetyService_server",
            "AirbagWarning",
            {"warn": {"isFault": True, "isValid": True}},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(36, 0, 1)

        self.partner.send_event_notify(
            "PassiveSafetyService_server",
            "AirbagWarning",
            {"warn": {"isFault": False, "isValid": False}},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(36, 0, 0)

    @allure.title("通知/获取功能故障状态_SeatFault/座椅故障")
    @pytest.mark.full
    def test_caseid_1979676(self):  ####
        dic = {0: 5, 1: 6, 4: 7, 5: 13, 6: 8}
        for key, value in dic.items():
            self.partner.send_event_notify(
                "SeatService_server",
                "SeatFault",
                {"faults": [{"faultId": 6, "faultMsg": "", "seatId": key}]},
            )
            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(38, value, 1)

            self.partner.send_event_notify(
                "SeatService_server",
                "SeatFault",
                {"faults": [{"faultId": 0, "faultMsg": "", "seatId": 12}]},
            )

            self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(38, 0, 0)

        self.partner.send_event_notify(
            "SeatService_server",
            "SeatFault",
            {
                "faults": [
                    {"faultId": 6, "faultMsg": "", "seatId": 0},
                    {"faultId": 6, "faultMsg": "", "seatId": 1},
                    {"faultId": 6, "faultMsg": "", "seatId": 4},
                    {"faultId": 6, "faultMsg": "", "seatId": 5},
                    {"faultId": 6, "faultMsg": "", "seatId": 6},
                ]
            },
        )

        self.partner.ck_event_and_resp(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "FunctionFaultStatus",
            {
                "infos": [
                    {"functionName": 38, "zoneId": 5, "faultId": 1},
                    {"functionName": 38, "zoneId": 6, "faultId": 1},
                    {"functionName": 38, "zoneId": 7, "faultId": 1},
                    {"functionName": 38, "zoneId": 13, "faultId": 1},
                    {"functionName": 38, "zoneId": 8, "faultId": 1},
                ]
            },method_args={"function": [{"functionName": 38, "zoneId": 0}]},timeout=10
        )
      
        self.partner.send_event_notify(
            "SeatService_server",
            "SeatFault",
            {"faults": [{"faultId": 0, "faultMsg": "", "seatId": 12}]},
        )
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(38, 0, 0)

    @allure.title("通知/获取功能故障状态_无线充电故障_主驾驶")
    @pytest.mark.smoke
    def test_caseid_1985333(self):
        dic ={1 : 160, 3 : 161, 7 :162, 4 :163, 5: 165, 8 : 166, 0 : 0}
        for sts, fault in dic.items():
            self.partner.send_event_notify("WirelessPhoneChargingService_server", "WirelessChargingInfo",
                                            {"info":[{"zone": 0, "faults":[{"faultId": sts,"faultMsg":""}]},
                                                     {"zone": 1,  "faults":[{"faultId": 0,"faultMsg":""}]}]})
            sleep(0.5)
            if sts == 0 :
                   self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(14, 0, fault)
            else:
               self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(14, 5, fault)
               
    @allure.title("通知/获取功能故障状态_无线充电故障_副驾驶")
    @pytest.mark.full
    def test_caseid_1985354(self):
        dic ={1 : 160, 3 : 161, 7 :162, 4 :163, 5: 165, 8 : 166, 0 : 0}
        for sts, fault in dic.items():
            self.partner.send_event_notify("WirelessPhoneChargingService_server", "WirelessChargingInfo",
                                            {"info":[{"zone": 0, "faults":[{"faultId": 0,"faultMsg":""}]},
                                                     {"zone": 1,  "faults":[{"faultId": sts,"faultMsg":""}]}]})
            sleep(0.5)
            if sts == 0 :
                self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(14, 0, fault)
            else:
                self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(14, 6, fault)
               
    @allure.title("通知/获取功能故障状态_无线充电故障_双排")
    @pytest.mark.full
    def test_caseid_1985355(self):
        dic ={1 : 160, 3 : 161, 7 :162, 4 :163, 5: 165, 8 : 166, 0 : 0}
        for sts, fault in dic.items():
            self.partner.send_event_notify("WirelessPhoneChargingService_server", "WirelessChargingInfo",
                                            {"info":[{"zone": 0,  "faults":[{"faultId": sts,"faultMsg":""}]},
                                                     {"zone": 1, "faults":[{"faultId": sts,"faultMsg":""}]}]})
            sleep(0.5)
            if sts == 0 :
               self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(14, 0, fault)
            else:
                self.partner.ck_event_and_resp(VEHICLECONTROLFAULT_SERVICE_CLIENT,"FunctionFaultStatus",
                                                            {"infos": [{"functionName": 14, "zoneId": 5, "faultId": fault},
                                                                        {"functionName": 14, "zoneId": 6, "faultId": fault}]},
                                                            method_args={"function": [{"functionName": 14, "zoneId": 0}]},timeout=10)

    @allure.title("通知/获取功能故障状态_无线充电故障_主副排交叉故障")
    @pytest.mark.full
    def test_caseid_1985365(self):
        self.partner.send_event_notify("WirelessPhoneChargingService_server", "WirelessChargingInfo",
                                            {"info":[{"zone": 0,"faults":[{"faultId": 1,"faultMsg":""}]},
                                                     {"zone": 1, "faults":[{"faultId": 255,"faultMsg":""}]}]})
        self.partner.ck_s2s_event(VEHICLECONTROLFAULT_SERVICE_CLIENT,"FunctionFaultStatus",
                                                            {"infos": [{"functionName": 14, "zoneId": 5, "faultId": 160},
                                                                      {"functionName": 14, "zoneId": 6, "faultId": 0}]})
        self.partner.send_request_and_ck_resp(VEHICLECONTROLFAULT_SERVICE_CLIENT,"GetFunctionFaultStatus",{"function": [{"functionName": 14, "zoneId": 0}]},
                                                                {"out": [{"functionName": 14, "zoneId": 5, "faultId": 160},
                                                                            {"functionName": 14, "zoneId": 6, "faultId": 0}]})
        self.partner.send_event_notify("WirelessPhoneChargingService_server", "WirelessChargingInfo",
                                            {"info":[{"zone": 0, "faults":[{"faultId": 1,"faultMsg":""}]},
                                                     {"zone": 1, "faults":[{"faultId": 8,"faultMsg":""}]}]})
        self.partner.ck_event_and_resp(VEHICLECONTROLFAULT_SERVICE_CLIENT,"FunctionFaultStatus",
                                                            {"infos": [{"functionName": 14, "zoneId": 5, "faultId": 160},
                                                                      {"functionName": 14, "zoneId": 6, "faultId": 166}]},
                                                            method_args={"function": [{"functionName": 14, "zoneId": 0}]},timeout=10)

        self.partner.send_event_notify("WirelessPhoneChargingService_server", "WirelessChargingInfo",
                                            {"info":[{"zone": 0, "faults":[{"faultId": 0,"faultMsg":""}]},
                                                     {"zone": 1, "faults":[{"faultId": 8,"faultMsg":""}]}]})
        self.partner.ck_event_and_resp(VEHICLECONTROLFAULT_SERVICE_CLIENT,"FunctionFaultStatus",
                                                            {"infos": [{"functionName": 14, "zoneId": 5, "faultId": 0},
                                                                      {"functionName": 14, "zoneId": 6, "faultId": 166}]},
                                                            method_args={"function": [{"functionName": 14, "zoneId": 0}]},timeout=10)
        self.partner.send_event_notify("WirelessPhoneChargingService_server", "WirelessChargingInfo",
                                            {"info":[{"zone": 0, "faults":[{"faultId": 0,"faultMsg":""}]},
                                                     {"zone": 1, "faults":[{"faultId": 0,"faultMsg":""}]}]})
        self.ck_FunctionFaultStatus_and_GetFunctionFaultStatus(14, 0, 0)
 
    @allure.title("通知功能故障状态_遍历FunctionType")
    @pytest.mark.smoke
    def test_caseid_104844(self):
        self.partner.send_method_request(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "GetFunctionFaultStatus",
            {"function": [{"functionName": 4, "zoneId": 0}]},
        )
        self.partner.send_method_request(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "GetFunctionFaultStatus",
            {"function": [{"functionName": 19, "zoneId": 0}]},
        )
        sleep(0.5)
        self.partner.send_method_request(
            VEHICLECONTROLFAULT_SERVICE_CLIENT,
            "GetFunctionFaultStatus",
            {"function": [{"functionName": 32, "zoneId": 0}]},
        )
        sleep(0.5)
        for functionName in range(1, 39):
            try:
                self.partner.send_request_and_ck_resp(
                    VEHICLECONTROLFAULT_SERVICE_CLIENT,
                    "GetFunctionFaultStatus",
                    {"function": [{"functionName": functionName, "zoneId": 0}]},
                    {"out": [{"functionName": functionName, "zoneId": 0}]},
                )
                sleep(0.5)
            except Exception as e:
                logger.info(e)
