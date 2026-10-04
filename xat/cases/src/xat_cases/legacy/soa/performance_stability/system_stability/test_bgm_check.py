# -*- coding: utf-8 -*-
"""
@File        : test_bgm_check.py
@Author      : lei.tao@jiduatuo.com
@Time        : 2023/05/10 15:00 PM
@Description : 检测S2S的内存和CPU消耗
"""
import multiprocessing
import os
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import pytest
import allure

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.bus_app import BusApp
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_cases.legacy.soa.case_helper.config.prebuild_prev import *

coredumplis = []

@allure.feature("性能稳定性")
@allure.story("系统稳定性/内存占用&CPU消耗")
@pytest.mark.soa
class TestBGM_CPU(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        os.system("ps -ef | grep tcpreplay| awk '{print $2}' | xargs kill -9")

        # # 启动partner operator
        s2s_sever_lis = [
            ("BonnetService", "client"),
            ("VehicleModeService", "client"),
            ("BlueToothService", "client"),
            ("CarConfigService", "client"),
            ("CentralLockService", "client"),
            ("KeyService", "client"),
            ("ChargeLidService", "client"),
            ("VehicleSetStatusService", "client"),
            ("ChassisService", "client"),
            ("ClimateControlService", "client"),
            ("CTDService", "client"),
            ("DoorService", "client"),
            ("DrivingAssistService", "client"),

            ("EntryService", "client"),
            ("CentralLockService", "client"),
            ("KeyService", "client"),
            ("AVPService", "server"),
            ("RPAAPAService", "server"),
            ("HornService", "client"),
            ("DoorService", "client"),
            ("PedalService", "client"),

            ("HornService", "client"),
            ("InnerRearViewService", "client"),
            ("KeyService", "client"),
            ("NetStatService", "client"),
            ("OuterRearViewService", "client"),
            ("PassiveSafetyService", "client"),
            ("PedalService", "client"),

            ("EntryService", "client"),
            ("LightService", "client"),
            ("WiperService", "client"),
            ("ChassisService", "client"),
            ("HighVoltageService", "client"),
            ("DoorService", "client"),
            ("SeatService", "client"),
            ("SteerWheelService", "client"),
            ("ClimateControlService", "client"),
            ("ShieldWindowService", "client"),

            ("CentralLockService", "client"),
            ("KeyService", "client"),
            ("AVPService", "server"),
            ("RPAAPAService", "server"),
            ("HornService", "client"),
            ("ResetSOAConfigService", "client"),

            ("WTIService", "client"),
            ("EntryService", "client"),
            ("CentralLockService", "client"),
            ("ChassisService", "client"),

        ]

        lis = [
            ("HighVoltageService", "client"), ("TailGateService", "client"), ("CentralLockService", "client"),
            ("VehicleSetStatusService", "client"),
            ("ChassisService", "client"), ("DoorService", "client"), ("WindowService", "client"),
            ("SteerWheelService", "client"),
            ("ClimateControlService", "client"), ("ShieldWindowService", "client"), ("ChargeLidService", "client"),
            ("OuterRearViewService", "client"),
            ("TailGateService", "client"), ("ConditionCheckService", "client"), ("WindowAppService", "client"),
            ("TailWingService", "client"),
            ("CarConfigService", "client"), ("VehicleModeService", "client"),
            ("WirelessPhoneChargingService", "client"), ("WiperService", "client"),
            ("SeatService", "client")]
        self.partner = S2sBaseClass(list(set(s2s_sever_lis + lis)))
        self.partner.method_default_timeout = 100 # 高负债压测对接口性能不做要求
        self.run_flag = False
        self.bgm_ssh = BGM_SSH()
        try:
            self.sd_tester.send_data([0x11, 0x81])

        except Exception as e:
            logger.warning(f"重启失败==》》{str(e)}")
        time.sleep(40)


        cmd = "ps -ef | grep top| awk '{print $2}' | xargs kill -9"
        self.bgm_ssh.type_commands(cmd, timeout=10)
        self.bgm_ssh.delete_bgm_tcpdump_file(bgm_log_name="cpu1.txt")
        global coredumplis
        self.coredump_lis = self.bgm_ssh.get_bgm_coredump()
        coredumplis = self.coredump_lis
        logger.error(f"第一次获取的 coredump 文件=====》》{self.coredump_lis} ")
        self.time_delay = 0.15

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        # change_bgm_config(self.bgmcli, self.sd_tester)

    def after_each_func(self, ecu):
        # recover_bgm_config(self.bgmcli, self.sd_tester)
        cmd = "ps -ef | grep top| awk '{print $2}' | xargs kill -9"
        self.bgm_ssh.type_commands(cmd, timeout=10)
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        os.system("ps -ef | grep tcpreplay| awk '{print $2}' | xargs kill -9")
        self.partner.stop_operators()
        partner_process_check()
        super().after_class(self, ecu)

    def send_request(self):
        # 12
        while self.run_flag:
            self.send_EntryService()  # 8
            self.send_DrivingAssistService()  # 1
            self.send_DoorService()  # 1
            self.send_CTDService()  # 1
            self.send_ClimateControlService()  # 1

    def send_request1(self):
        # 40
        while self.run_flag:
            self.send_ChassisService()  # 14
            self.send_VehicleSetStatusService_ChargeLidService()  # 3
            self.send_CarConfigService()  # 6
            self.send_InnerRearViewService()  # 2
            self.send_HornService()  # 1
            self.send_NetStatService()  # 4
            self.send_OuterRearViewService()  # 9
            self.send_seat()  # 4

    def send_request2(self):
        # 50
        while self.run_flag:
            self.send_PassiveSafetyService()  # 2
            self.send_ResetSOAConfigService()  # 28
            self.send_VehicleModeService()  # 10
            self.send_CentralLockService()  # 6
            self.send_KeyService()  # 4

    def send_request3(self):
        while self.run_flag:
            self.send_HornService()
            self.send_NetStatService()
            self.send_OuterRearViewService()
            self.send_PassiveSafetyService()
            self.send_ResetSOAConfigService()
            self.send_seat()

    def send_seat(self):

        self.partner.send_method_request(
            "SEAT_SERVICE_CLIENT",
            'StopMoveDirection',
            {"id": 0, "part": random.randint(0, 3), "direction": random.randint(0, 3)},
        )
        self.partner.send_method_request(
            "SEAT_SERVICE_CLIENT",
            'StopMoveDirection',
            {"id": 0, "part": random.randint(0, 3), "direction": random.randint(0, 3)},
        )
        self.partner.send_method_request(
            "SEAT_SERVICE_CLIENT",
            'StopMoveDirection',
            {"id": 0, "part": random.randint(0, 3), "direction": random.randint(0, 3)},
        )

        self.partner.send_method_request(
            "SEAT_SERVICE_CLIENT",
            'StopMoveDirection',
            {"id": 0, "part": random.randint(0, 3), "direction": random.randint(0, 3)},
        )

    def send_ResetSOAConfigService(self):
        LIGHT_SERVICE_CLIENT = "LightService_client"
        WIPER_SERVICE_CLIENT = "WiperService_client"
        SEAT_SERVICE_CLIENT = "SeatService_client"
        STEERWHEEL_SERVICE_CLIENT = "SteerWheelService_client"
        KEY_SERVICE_CLIENT = "KeyService_client"
        CLIAMTECONTROL_SERVICE_CLIENT = "ClimateControlService_client"
        SHIELDWINDOW_SERVICE_CLIENT = "ShieldWindowService_client"
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": random.randint(0, 3)})
        # 设置后雾灯打开
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
                                         {"lights": [{"light": {"type": 4, "zoneId": 10}, "mode": 1}]})
        # 设置雨刮档位调节关闭
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": 0, "mode": 0})
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 0},
                                                                                         {"key": 1, "value": 0}]})
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingLevel",
                                         {"params": [{"id": 0, "uint8Info": 1},
                                                     {"id": 1, "uint8Info": 1},
                                                     {"id": 4, "uint8Info": 1},
                                                     {"id": 6, "uint8Info": 1}]})

        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetMassageConf",
                                         {"params": [{"id": 0, "conf": {"isOn": True, "type": 1, "intensity": 0}},
                                                     {"id": 1, "conf": {"isOn": True, "type": 1, "intensity": 0}}]})

        # 设置方向盘加热打开
        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 1})
        # 设置前排空调总开关-关闭
        self.partner.send_method_request(CLIAMTECONTROL_SERVICE_CLIENT, "Off", {"zoneId": 1})

        self.partner.send_method_request(STEERWHEEL_SERVICE_CLIENT, "SetHeat", {"status": 0})
        # 设置前排空调总开关-关闭
        self.partner.send_method_request(CLIAMTECONTROL_SERVICE_CLIENT, "Off", {"zoneId": 0})

        self.partner.send_method_request(CLIAMTECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId": 1, "speed": 0})
        self.partner.send_method_request(CLIAMTECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1})
        # 设置主驾、副驾、后排吹风模式 zoneid 3,4,2， mode 0
        self.partner.send_method_request(CLIAMTECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId": 3, "mode": 0})

        self.partner.send_method_request(CLIAMTECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId": 4, "mode": 0})

        self.partner.send_method_request(CLIAMTECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId": 2, "mode": 0})

        # 设置前挡风玻璃除雾-打开
        self.partner.send_method_request(CLIAMTECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.partner.send_method_request(CLIAMTECONTROL_SERVICE_CLIENT, "GetFastDefrostMode", {})
        # 设置后挡风玻璃除雾-Id=@value(2) kShieldWindowRear status=@value(1) kHeatStatusOn
        self.partner.send_method_request(SHIELDWINDOW_SERVICE_CLIENT, "SetHeat", {"heat": {"id": 2, "status": 1}})

        self.partner.send_method_request(SHIELDWINDOW_SERVICE_CLIENT, "SetHeat",
                                         {"heat": {"id": random.randint(0, 2), "status": random.randint(0, 2)}})

        # 设置PM2.5一键过滤 On
        self.partner.send_method_request(CLIAMTECONTROL_SERVICE_CLIENT, "SetPM25", {"on": True})
        self.partner.send_method_request(CLIAMTECONTROL_SERVICE_CLIENT, "GetPM25", {}, )
        # 设置PM2.5自动 On
        self.partner.send_method_request(CLIAMTECONTROL_SERVICE_CLIENT, "SetPM25Auto", {"isOn": True, "sourceId": 2})
        self.partner.send_method_request(CLIAMTECONTROL_SERVICE_CLIENT, "GetPM25Auto", {}, )
        # 设置清除异味=True
        self.partner.send_method_request(CLIAMTECONTROL_SERVICE_CLIENT, "SetCockpitCleanMode", {"on": True})
        # 设置后排空调控开关-on
        self.partner.send_method_request(CLIAMTECONTROL_SERVICE_CLIENT, "Off", {"zoneId": 2})
        self.partner.send_method_request(CLIAMTECONTROL_SERVICE_CLIENT, "Off", {"zoneId": 0})
        self.partner.send_method_request(CLIAMTECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {})

    def send_PedalService(self):
        ENTRY_SERVICE_CLIENT = "PedalService_client"
        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "GetPedalFault", "", )
        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "GetPedalFault", "", )

    def send_PassiveSafetyService(self):
        ENTRY_SERVICE_CLIENT = "PassiveSafetyService_client"
        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "GetAirbagWarning", {}, )
        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "GetPedestrianProtectionWarning", "", )

        pass

    def send_OuterRearViewService(self):
        ENTRY_SERVICE_CLIENT = "OuterRearViewService_client"
        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "SetMirrorAngleTarget",
                                         {"params": [{"viewId": 1, "horizontalAngle": random.randint(0, 100),
                                                      "verticalAngle": random.randint(0, 100)}]})
        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "SetMirrorAngleTarget",
                                         {"params": [{"viewId": 0, "horizontalAngle": 100, "verticalAngle": 100}]})

        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "SetMirrorAngleTarget",
                                         {"params": [{"viewId": 1, "horizontalAngle": 1, "verticalAngle": 100}]})

        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "SetMirrorAngleTarget",
                                         {"params": [{"viewId": 1, "horizontalAngle": 100, "verticalAngle": 1}]})

        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "SetMirrorAngleTarget",
                                         {"params": [{"viewId": 2, "horizontalAngle": 100, "verticalAngle": 100}]})
        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "SetMirrorAngleTarget",
                                         {"params": [
                                             {"viewId": random.randint(0, 2), "horizontalAngle": random.randint(0, 100),
                                              "verticalAngle": random.randint(0, 100)}]})
        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, 'GetMirrorAngle', {"views": [random.randint(0, 2)]})

        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, 'GetHeat', {"views": [1]})

        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, 'GetHeat', {"views": [0]}, )

    def send_NetStatService(self):

        self.partner.send_method_request(
            'NetStatService_client',
            'SetNetResidentSts',
            args={"is_5G": True},

        )
        self.partner.send_method_request(
            'NetStatService_client',
            'SetNetResidentSts',
            args={"is_5G": False},
        )
        self.partner.send_method_request(
            'NetStatService_client',
            'GetIccid',
            args={},
        )
        self.partner.send_method_request(
            'NetStatService_client',
            'GetNetSts',
            args={},
        )

    def send_KeyService(self):
        KEY_SERVICE_CLIENT = "KeyService_client"
        self.partner.send_method_request(KEY_SERVICE_CLIENT, 'SetCarLocalTraceRequest', {"carLoctrReq": 0})
        self.partner.send_method_request(KEY_SERVICE_CLIENT, 'SetCarLocalTraceRequest', {"carLoctrReq": 1})
        self.partner.send_method_request(KEY_SERVICE_CLIENT, 'SetCarLocalTraceRequest', {"carLoctrReq": 2})
        self.partner.send_method_request(KEY_SERVICE_CLIENT, 'SetCarLocalTraceRequest', {"carLoctrReq": 3})

    def send_InnerRearViewService(self):
        self.partner.send_method_request("InnerRearViewService_client", "SetAutoBlindingProof", {"isOn": True})
        self.partner.send_method_request("InnerRearViewService_client", "SetAutoBlindingProof", {"isOn": False})

    def send_HornService(self):
        self.partner.send_method_request(
            'HornService_client',
            'GetStatus',
            args={},
        )

    def send_EntryService(self):
        self.partner.send_method_request("KeyService_client", "SetConfigInfo",
                                         {"infos": [{"key": 0, "value": random.randint(0, 3)}]})
        self.partner.send_method_request("CentralLockService_client", "SetDoorCloseLock", {"cmd": 1, "source": 1})

        self.partner.send_method_request("CentralLockService_client", "SetDoorCloseLock", {"cmd": 0, "source": 1})

        self.partner.send_method_request("KeyService_client", "SetConfigInfo",
                                         {"infos": [{"key": 0, "value": random.randint(0, 3)}]})

        self.partner.send_method_request("CentralLockService_client", "SetDoorCloseLock",
                                         {"cmd": random.randint(0, 3), "source": 3})

        self.partner.send_event_notify("AVPService_server", "NotifyAVPStatus", {"sts": {"havpSubSatus": 8}})

        self.partner.send_event_notify("RPAAPAService_server", "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": 3}})

        self.partner.send_method_request("CentralLockService_client", "SetDoorCloseLock", {"cmd": 1, "source": 2})

    def send_DrivingAssistService(self):
        ENTRY_SERVICE_CLIENT = "DrivingAssistService_client"
        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "SetDistanceBackup",
                                         {"distance": random.randint(0, 10002)})

    def send_DoorService(self):
        self.partner.send_method_request(
            'DoorService_client',
            'SetPosition',
            {"doors": [{"id": random.randint(0, 3), "pos": random.randint(0, 3)}]},
        )

    def send_CTDService(self):
        self.partner.send_method_request("CTDService_client", "getAlarmInfo", {}, )

    def send_ClimateControlService(self):
        self.partner.send_method_request(
            'ClimateControlService_client',
            'SetFragranceType',
            args={'fragrance': [{'channel': 1, 'ratio': random.randint(0, 100)}]},
        )

    def send_ChassisService(self):
        self.partner.send_method_request('ChassisService_client', "getABSActInfo", {})

        self.partner.send_method_request('ChassisService_client', "getABSFailSts", {})

        self.partner.send_method_request('ChassisService_client', "getIndicatorLightReqSts", {})
        self.partner.send_method_request('ChassisService_client', "GetGear", {})

        self.partner.send_method_request('ChassisService_client', "GetSuspFailrStatus", {})
        self.partner.send_method_request('ChassisService_client', "getDisplayReqSts", {})
        self.partner.send_method_request('ChassisService_client', "GetTorqueMode", {})
        self.partner.send_method_request('ChassisService_client', "GetGearFault", {})

        self.partner.send_method_request('ChassisService_client', "GetSteerErrorReqStatus", {})

        self.partner.send_method_request('ChassisService_client', "GetWheelSpeed", {})
        self.partner.send_method_request('ChassisService_client', "GetSpeed", {})
        self.partner.send_method_request('ChassisService_client', "getVehReadySts", {})
        self.partner.send_method_request('ChassisService_client', "GetEGSMVirtualShiftReq", {})
        self.partner.send_method_request('ChassisService_client', "getVehReadySts", {})

    def send_VehicleSetStatusService_ChargeLidService(self):
        VEHICLESETSTATUS_CLIENT = "VehicleSetStatusService_client"
        CHARGELID_SERVICE_CLIENT = "ChargeLidService_client"
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": False})
        self.partner.send_method_request(CHARGELID_SERVICE_CLIENT, "Open", {})
        self.partner.send_method_request(CHARGELID_SERVICE_CLIENT, "Close", {})

    def send_CarConfigService(self):
        CARCONFIG_SERVICE_CLIENT = "CarConfigService_client"

        self.partner.send_method_request(CARCONFIG_SERVICE_CLIENT, "GetVIN", {})

        self.partner.send_method_request(CARCONFIG_SERVICE_CLIENT, "GetWheelCircumference", {})

        self.partner.send_method_request(CARCONFIG_SERVICE_CLIENT, "GetVehicleSWBaseline", {})

        self.partner.send_method_request(CARCONFIG_SERVICE_CLIENT, "GetCltcPowerConsumption", {})

        self.partner.send_method_request(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {})

        self.partner.send_method_request(CARCONFIG_SERVICE_CLIENT, "GetCarConfigInfo", {})

    def send_CentralLockService(self):
        CENTRALLOCK_SERVICE_CLIENT = "CentralLockService_client"
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "GetLockActTriggerSource", {})

        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "GetCentralLockSysInfo", {})

        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "GetLockStatus", {})

        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {})

        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "GetCenLckUpdEve", {})
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "GetCentralLockReminder", {})

    def send_VehicleModeService(self):
        self.partner.send_method_request(
            'VehicleModeService_client',
            "SetUsageModeUp",
            {"mode": 11},
        )
        self.partner.send_method_request(
            'VehicleModeService_client',
            "SetUsageModeUp",
            {"mode": 13},
        )

        self.partner.send_method_request(
            'VehicleModeService_client',
            "SetUsageModeDown",
            {"mode": 11},
        )

        self.partner.send_method_request(
            'VehicleModeService_client',
            "SetUsageModeDown",
            {"mode": 1},
        )

        self.partner.send_method_request(
            'BonnetService_client',
            'GetOpenCloseStatus',
            args={},
        )

        self.partner.send_method_request(
            'BonnetService_client',
            'GetStatus',
            args={}
        )

        self.partner.send_method_request(
            'BlueToothService_client',
            'SetBLEVehData',
            {"data": [random.randint(0, 9) for i in range(random.randint(1, 4095))]},
        )
        self.partner.send_method_request(
            'BlueToothService_client',
            'GetMobDevSts',
            args={},
        )

        self.partner.send_method_request(
            'BlueToothService_client',
            'GetConStsForAVP',
            args={},
        )

    def gaoya_request(self):
        """发送request请求"""
        while self.run_flag:
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetBatteryHeating",
                                             {"type": 5, "on": False, "value": 0})
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetEnergyRecoveryLevel", {"level": 2})
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetEnergyRecoveryCmd", {"isOn": False})
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetAveragePowerConsume", {"power": 90.0})
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetBatteryHeating",
                                             {"type": 5, "on": True, "value": -40})
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetEnergyRecoveryLevel", {"level": 1})
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetEnergyRecoveryCmd", {"isOn": True})
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetAveragePowerConsume", {"power": 50.0})
            sleep(self.time_delay)

    def vehicleset_request(self):
        """发送request请求"""
        while self.run_flag:
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetMaintenanceMode", {"isOn": False})
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": False})
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetMaintenanceMode", {"isOn": True})
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True})
            sleep(self.time_delay)

    def chassis_request(self):
        """发送request请求"""

        while self.run_flag:
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetHDC", {"on": False})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetTorqueMode", {"mode": 2})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetTorqueMode", {"mode": 1})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetSuspensionLevel", {"level": 2})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "EPBOperation", {"operate": 0})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetAutoHold", {"on": False})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetHDC", {"on": True})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetTorqueMode", {"mode": 0})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetTorqueMode", {"mode": 2})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetSuspensionLevel", {"level": 3})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "EPBOperation", {"operate": 1})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetAutoHold", {"on": True})
            sleep(self.time_delay)

    def Door_request(self):
        """发送request请求"""
        while self.run_flag:
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition',
                                             {"doors": [{"id": 0, "pos": 0}, {"id": 1, "pos": 10},
                                                        {"id": 2, "pos": 0}, {"id": 3, "pos": 10}]})
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPositionMax', {"doors": [{"id": 0, "pos": 10},
                                                                                               {"id": 1, "pos": 10},
                                                                                               {"id": 2, "pos": 10},
                                                                                               {"id": 3, "pos": 10}]})
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition',
                                             {"doors": [{"id": 0, "pos": 50}, {"id": 1, "pos": 50},
                                                        {"id": 2, "pos": 50}, {"id": 3, "pos": 50}]})
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPositionMax', {"doors": [{"id": 0, "pos": 100},
                                                                                               {"id": 1, "pos": 100},
                                                                                               {"id": 2, "pos": 100},
                                                                                               {"id": 3, "pos": 100}]})
            sleep(self.time_delay)

    def climate_request(self):
        """发送request请求"""
        while self.run_flag:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperature',
                                             {"zoneId": 3, "value": 25.5})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetFragranceType',
                                             {'fragrance': [{'channel': 1, 'ratio': 30}]})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperature',
                                             {"zoneId": 3, "value": 22.5})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetFragranceType',
                                             {'fragrance': [{'channel': 1, 'ratio': 100}]})
            sleep(self.time_delay)

    def shieldwindow_request(self):
        """发送request请求"""
        while self.run_flag:
            self.partner.send_method_request(SHIELDWINDOW_SERVICE_CLIENT, "SetHeat", {"heat": {"id": 2, "status": 0}})
            self.partner.send_method_request(SHIELDWINDOW_SERVICE_CLIENT, "SetHeat",
                                             {"heat": {"id": 1, "status": 0}})
            self.partner.send_method_request(SHIELDWINDOW_SERVICE_CLIENT, "SetHeat",
                                             {"heat": {"id": 1, "status": 1}})
            self.partner.send_method_request(SHIELDWINDOW_SERVICE_CLIENT, "SetHeat", {"heat": {"id": 2, "status": 1}})
            sleep(self.time_delay)

    def window_request(self):
        """发送request请求"""
        while self.run_flag:
            self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "Close", {"windows": [0, 1, 2, 3]})
            self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition",
                                             {"windows": [{"id": 0, "position": 20},
                                                          {"id": 1, "position": 20},
                                                          {"id": 2, "position": 20},
                                                          {"id": 3, "position": 20}]})
            self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "Open", {"windows": [0, 1, 2, 3]})
            self.partner.send_method_request(WINDOW_SERVICE_CLIENT, "SetPosition",
                                             {"windows": [{"id": 0, "position": 50},
                                                          {"id": 1, "position": 50},
                                                          {"id": 2, "position": 50},
                                                          {"id": 3, "position": 50}]})
            sleep(self.time_delay)

    def outerview_request(self):
        """发送request请求"""
        while self.run_flag:
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {
                "params": [{"viewId": 1, "horizontalAngle": 50, "verticalAngle": 100}]})
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, 'SetAutoFoldUnfold',
                                             {"params": [{"id": 2, "isOn": False}]})
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, "SetMirrorAngleTarget", {
                "params": [{"viewId": 1, "horizontalAngle": 100, "verticalAngle": 100}]})
            self.partner.send_method_request(OUTERREARVIEW_SERVICE_CLIENT, 'SetAutoFoldUnfold',
                                             {"params": [{"id": 2, "isOn": True}]})
            sleep(self.time_delay)

    def tailgate_request(self):
        """发送request请求"""
        while self.run_flag:
            self.partner.send_method_request(TAILGATE_SERVICE_CLIENT, "SetTailGate", {"cmd": 1})
            self.partner.send_method_request(TAILGATE_SERVICE_CLIENT, "SetTailGate", {"cmd": 0})
            self.partner.send_method_request(TAILGATE_SERVICE_CLIENT, "Open", {})
            self.partner.send_method_request(TAILGATE_SERVICE_CLIENT, "Close", {})
            sleep(self.time_delay)

    def process_pcap(self):
        sf = SniffPacket()
        name =sf.get_network_card_name_by_ip()
        # current_working_dir = os.getcwd()
        # local_path = os.path.join(os.getcwd(), 'case_helper/config/1.1Udp_unvlan_revise_mac_revise_ip.pcap')
        local_path = '/root/test_data/1.1Udp_unvlan_revise_mac_revise_ip.pcap'
        cmd=f"sudo tcpreplay -i {name} -l 10000 {local_path}"
        print(f"执行的指令为={cmd}")
        with allure.step(cmd):
            pass
        os.system(cmd)

    def hander_top(self, bgm_cpu_file):
        result_lis = []
        with open(bgm_cpu_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                if "s2s_service" in line:
                    result = [i.strip() for i in line.strip().split(' ') if i.strip()]
                    cpu = float(result[8])
                    MEM = float(result[9])
                    res = float(result[5])

                    result_lis.append((cpu, MEM, res))

                    logger.info(f"cpu==>>{cpu},MEM==>>{MEM},RES==>>{res / 1024}")

        lis = [i[0] for i in result_lis]
        lis_max = max(lis)
        lis_v = round(sum(lis) / len(lis), 2)
        lis_min = min(lis)

        with allure.step(f"cpu 最大值==>>{lis_max} 平均值==>>{lis_v} 最小值==>>{lis_min}"):
            logger.info(f"cpu 最大值==>>{lis_max}")
            logger.info(f"cpu 平均值==>>{lis_v}")
            logger.info(f"cpu 最小值==>>{lis_min}")

        lis = [i[1] for i in result_lis]
        lis_max = max(lis)
        lis_v = round(sum(lis) / len(lis), 2)
        lis_min = min(lis)
        with allure.step(f"MEM 最大值==>>{lis_max} 平均值==>>{lis_v} 最小值==>>{lis_min}"):

            logger.info(f"MEM 最大值==>>{lis_max}")
            logger.info(f"MEM 平均值==>>{lis_v}")
            logger.info(f"MEM 最小值==>>{lis_min}")

        lis = [i[2] for i in result_lis]
        lis_max = max(lis) / 1024
        lis_v = round(sum(lis) / len(lis), 2) / 1024
        lis_min = min(lis) / 1024
        with allure.step(f"RES 最大值==>>{lis_max} 平均值==>>{lis_v} 最小值==>>{lis_min}"):

            logger.info(f"RES 最大值==>>{lis_max}")
            logger.info(f"RES 平均值==>>{lis_v}")
            logger.info(f"RES 最小值==>>{lis_min}")

    def test_caseid_1983934_1983935(self):

        lin_channel_list = ["cem_lin1", "cem_lin2", "cem_lin3", "cem_lin4", "cem_lin5", "cem_lin6"]
        # can 通道
        can_channel_list = ["bodycan", "propulsioncan", "chassiscan1", "chassiscan2", "passivesafetycan",
                            "diagnosticcan", "infocanfd", "adcanfd", "bodyalmcanfd1", "connectivitycanfd",
                            "bodyexposedcanfd", "bodyalmcanfd2"
                            ]
        fr_channel_list = ['backbonefr']
        all_channel = lin_channel_list + can_channel_list + fr_channel_list
        # todo 通道信号随机变化
        for name in all_channel:
            self.ipdu.set_random_signal_thread_start(name, 100, interval_time=1)

        # todo 数据回放， 需要先修改
        process1 = multiprocessing.Process(target=self.process_pcap)
        process1.daemon = True
        process1.start()
        # 发送请求 method
        fun_lis = [self.gaoya_request,  # 8
                   self.vehicleset_request,  # 4
                   self.chassis_request,  # 12
                   self.climate_request,  # 4
                   self.shieldwindow_request,  # 4
                   self.window_request,  # 4
                   self.outerview_request,  # 4
                   self.tailgate_request,  # 4
                   self.send_request,  # 12
                   self.send_request1,  # 40
                   self.send_request2,  # 50
                   ]
        self.run_flag = True
        # 周期
        self.time_delay = 1
        for fun in fun_lis:
            t = threading.Thread(target=fun)
            t.setDaemon(True)
            t.start()
        # time.sleep(5000)
        # cmd = "top -b > /log/cpu1.txt&"
        # 在bgm 内部执行top 指令重定向到文件
        cmd = "(top -b | grep s2s) > /log/cpu1.txt&"
        bgm_cpu = self.bgm_ssh.type_commands(cmd, timeout=10)
        global coredumplis

        time.sleep(5)
        t = time.time()
        # todo 运行时间根据需要修改
        timeout= 60*60
        while time.time() - t < timeout:
            coredump_lis = self.bgm_ssh.get_bgm_coredump()
            if len(coredump_lis) != len(coredumplis):
                coredumplis = coredump_lis
                logger.info(f"获取 coredump 文件==》》{coredump_lis}")
                with allure.step(f"获取 coredump 文件==》》{coredump_lis}"):
                    # self.bgm_ssh.get_log('/root/ltg01/sat/xat_cases/legacy/bgm/00ltg/log')
                    pass

            sleep(10)
        # 停止执行  top 指令
        cmd = "ps -ef | grep top| awk '{print $2}' | xargs kill -9"
        self.bgm_ssh.type_commands(cmd, timeout=10)
        self.ipdu.set_random_signal_thread_all_stop()
        # 拉取top的日志
        try:
            local_path = os.path.dirname(__file__)
            bgm_cpu_file = self.bgm_ssh.scp_bgm_log_to_local("cpu1.txt",log_path=local_path,save_log_name=None,path="/log")
            # 处理数据
            self.hander_top(bgm_cpu_file)

        except Exception as e:
            logger.error(f"失败==》》{str(e)}")

# pytest test_performance/test_bgm_check_cpu.py
