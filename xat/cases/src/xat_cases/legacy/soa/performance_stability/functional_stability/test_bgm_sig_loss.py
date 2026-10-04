# -*- coding: utf-8 -*-
"""
@File        : test_bgm_sig_loss.py
@Author      : lei.tao@jiduatuo.com
@Time        : 2023/05/10 15:00 PM
@Description : S2S上行信号和下行信号丢失率稳定性
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
from datetime import datetime
from xat_ecu.legacy.sdk.sdk_tools import *
coredumplis = []

g_res_dict = {
    "success": {
    },
    "fail": {
    },
}

g_res_dict_up = {
    "success": {
    },
    "fail": {
    },
}

@allure.feature("性能稳定性")
@allure.story("业务稳定性/上下行信号丢失率")
@pytest.mark.soa
class TestBGM_CPU(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        os.system("ps -ef | grep tcpreplay| awk '{print $2}' | xargs kill -9")


        # 启动partner operator
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
            # ("NetStatService", "client"),
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
        self.partner = S2sBaseClass(list(set(s2s_sever_lis + lis)), logger_flag=1)
        sleep(2)

        self.lin_channel_list = ["cem_lin1", "cem_lin2", "cem_lin3", "cem_lin4", "cem_lin5", "cem_lin6"]
        # can 通道
        self.can_channel_list = [
            "bodycan","propulsioncan",
            "chassiscan1", "chassiscan2", "passivesafetycan",
            "diagnosticcan", "infocanfd", "adcanfd", "bodyalmcanfd1", "connectivitycanfd",
            "bodyexposedcanfd", "bodyalmcanfd2"
        ]
        self.fr_channel_list = ['backbonefr']

        fun_lis = [
            # self.gaoya_request,  # 8
            # self.vehicleset_request,  # 4
            # self.chassis_request,  # 12
            # self.climate_request,  # 4
            # self.shieldwindow_request,  # 4
            # self.window_request,  # 4
            # self.outerview_request,  # 4
            # self.tailgate_request,  # 4
            self.send_request,  # 12
            self.send_request1,  # 40
            self.send_request2,  # 50
            #    self.send_request2,  # 50

            #    self.send_request3
        ]
        self.run_flag = True
        self.time_delay = 1

        for fun in fun_lis:
            t = threading.Thread(target=fun)
            t.setDaemon(True)
            t.start()

        self.run_flag = False

        self.bgm_ssh = BGM_SSH()
        self.bgm_ssh.init_bgm_tcpdump()
        # cmd = "ps -ef | grep top| awk '{print $2}' | xargs kill -9"
        # self.bgm_ssh.type_commands(cmd, timeout=10)
        # self.bgm_ssh.delete_bgm_tcpdump_file(bgm_log_name="cpu1.txt")
        # global coredumplis
        # self.coredump_lis = self.bgm_ssh.get_bgm_coredump()
        # coredumplis = self.coredump_lis
        # logger.error(f"第一次获取的 coredump 文件=====>>{self.coredump_lis} ")
        self.time_delay = 0.15
        os.system("""ps -ef|grep -i tail|awk '{printf $2"\n"}'|xargs kill -9;ps -ef|grep -i tail""")
        
      
    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.all_channel = self.lin_channel_list + self.can_channel_list + self.fr_channel_list
        for name in self.all_channel:
            self.ipdu.set_random_signal_thread_start(name, 50, interval_time=1)

    def after_each_func(self, ecu):
        self.ipdu.set_random_signal_thread_all_stop()
        cmd = "ps -ef | grep top| awk '{print $2}' | xargs kill -9"
        self.bgm_ssh.type_commands(cmd, timeout=10)
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        os.system("ps -ef | grep tcpreplay| awk '{print $2}' | xargs kill -9")
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
            # self.send_NetStatService()  # 4
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
            # self.send_NetStatService()
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
        return

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
                if line.strip().endswith("s2s_ser+"):
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

    def start_thread(self):

        with ThreadPoolExecutor(max_workers=9) as pool:
            # 向线程池提交一个task, 方法1会作为action()函数的参数
            # future1 = pool.submit(self.gaoya_request)
            # 向线程池再提交一个task, 方法2会作为action()函数的参数
            # future2 = pool.submit(self.vehicleset_request)
            # future3 = pool.submit(self.chassis_request)
            # future4 = pool.submit(self.climate_request)
            # future5 = pool.submit(self.shieldwindow_request)

            future6 = pool.submit(self.window_request)
            future7 = pool.submit(self.outerview_request)
            future8 = pool.submit(self.tailgate_request)
            future9 = pool.submit(self.send_request1)

            # def get_result(future):
            #     print(future.result())

            # 为future1添加线程完成的回调函数
            # future1.add_done_callback(get_result)
            # # 为future2添加线程完成的回调函数
            # future2.add_done_callback(get_result)
            # future3.add_done_callback(get_result)
            # future4.add_done_callback(get_result)
            # future5.add_done_callback(get_result)

            # future6.add_done_callback(get_result)
            # future7.add_done_callback(get_result)
            # future8.add_done_callback(get_result)
            # future9.add_done_callback(get_result)

    def tosun_check(self, can_bus, can_id, data, timeout=5):
        file = os.path.join(project_root, "test_case/soa/Can.asc")
        with open(file, "r") as fd:
            date_str = fd.readlines()[0].replace('date ', '').replace('\n', '')
            timestamp = time.mktime(time.strptime(date_str, "%a %b %d %H:%M:%S %Y"))
        
        cmd = f'tail -F {file}|grep "{data}"|grep " {can_id}  "'
        logger.info(f"cmd==>>>{cmd}")
        t0 = time.time()
        # 获取命令的输出和错误信息
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while time.time() - t0 <= timeout:
            line = process.stdout.readline().decode(encoding="utf-8").strip()
            logger.info(f"line==>>{line}")
            if data in line:
                end_time = float(line.split(" ")[0])
                self.time1 = float(timestamp) + float(end_time) + float(28800)
                logger.info(f"end_time=={end_time}")
                process.terminate()
                process.wait()
                logger.info("执行成功，程序退出")
                break
        else:
            logger.info(f"超时{timeout}s，程序退出")
            self.time1 = None

    def candump_check(self, can_bus, can_id, data, timeout=5):
        """
        通过candump命令来获取帧报文发生跳变时刻的时间戳，捕获到的时间戳保存在全局变量 end_time 中，捕获失败 end_time 为None
        can_bus: 例如can4
        can_id：帧报文ID
        """
        file = os.path.join(project_root, "test_case/soa/Can.asc")
        cmd = f'tail -F {file}|grep {can_bus}|grep {can_id}'
        logger.info(f"cmd==>>>{cmd}")
        t0 = time.time()
        # 获取命令的输出和错误信息
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while process.poll() is None:
            line = process.stdout.readline().decode(encoding="utf-8").strip()
            logger.info(f"line==>>{line}")
            if data in line:
                end_time = float(line.split(" ")[0][1:-1])
                self.time1 = end_time
                logger.info(f"end_time=={end_time}")
                process.terminate()
                process.wait()
                logger.info("执行成功，程序退出")
            elif time.time() - t0 > timeout:
                process.terminate()
                process.wait()
                logger.info(f"超时{timeout}s，程序退出")
                self.time1 = None
                break

    def check_send_method(self, server_name, method_name, parm1, parm2, can_name, can_id, data1, data2):
        global g_res_dict
        self.time1 = None
        try:
            th1 = threading.Thread(target=self.tosun_check, args=(can_name, can_id, data2))
            th1.setDaemon(True)
            th1.start()
            self.partner.send_method_request(server_name, method_name, parm1)
            self.partner.empty_all(1)
            t = time.time()
            self.partner.send_method_request(server_name, method_name, parm2)
            th1.join()
        except KeyboardInterrupt:
            if th1.is_alive():
                os.kill(th1.ident, th1.SIGTERM)
        if self.time1:
            with allure.step(f"{data1}-->>{data2} 获取成功，时间差为>>>{self.time1 - t}s"):
                logger.info(f"{data1}-->>{data2} 获取成功，时间差为>>>{self.time1 - t}s")
            if method_name in self.res_dict["success"]:
                self.res_dict["success"][method_name].append((f"{data1}-->>{data2}", self.time1 - t))
            else:
                self.res_dict["success"][method_name] = [(f"{data1}-->>{data2}", self.time1 - t)]

            if method_name in g_res_dict["success"]:
                g_res_dict["success"][method_name].append((f"{data1}-->>{data2}", self.time1 - t))
            else:
                g_res_dict["success"][method_name] = [(f"{data1}-->>{data2}", self.time1 - t)]
        else:
            with allure.step(f"{data1}-->>{data2} 获取失败"):
                logger.info(f"{data1}-->>{data2} 获取失败")
            if method_name in g_res_dict["fail"]:
                g_res_dict["fail"][method_name].append((f"{data1}-->>{data2}"))
            else:
                g_res_dict["fail"][method_name] = [(f"{data1}-->>{data2}")]
            if method_name in self.res_dict["fail"]:
                self.res_dict["fail"][method_name].append((f"{data1}-->>{data2}"))
            else:
                self.res_dict["fail"][method_name] = [(f"{data1}-->>{data2}")]


        self.time1 = None
        try:
            th2 = threading.Thread(target=self.tosun_check, args=(can_name, can_id, data1))
            th2.setDaemon(True)
            th2.start()
            self.partner.send_method_request(server_name, method_name, parm2)
            self.partner.empty_all(1)
            t2 = time.time()
            self.partner.send_method_request(server_name, method_name, parm1)
            th2.join()
        except KeyboardInterrupt:
            if th2.is_alive():
                os.kill(th2.ident, th2.SIGTERM)
        if self.time1:
            with allure.step(f"{data2}-->>{data1} 获取成功，时间差为>>>{self.time1 - t2}s"):
                logger.info(f"{data2}-->>{data1} 获取成功，时间差为>>>{self.time1 - t2}s")
            if method_name in self.res_dict["success"]:
                self.res_dict["success"][method_name].append((f"{data2}-->>{data1}", self.time1 - t))
            else:
                self.res_dict["success"][method_name] = [(f"{data2}-->>{data1}", self.time1 - t)]
            if method_name in g_res_dict["success"]:
                g_res_dict["success"][method_name].append((f"{data2}-->>{data1}", self.time1 - t))
            else:
                g_res_dict["success"][method_name] = [(f"{data2}-->>{data1}", self.time1 - t)]
        else:
            with allure.step(f"{data2}-->>{data1} 获取失败"):
                logger.info(f"{data2}-->>{data1} 获取失败")
            if method_name in g_res_dict["fail"]:
                g_res_dict["fail"][method_name].append((f"{data2}-->>{data1}"))
            else:
                g_res_dict["fail"][method_name] = [(f"{data2}-->>{data1}")]
            if method_name in self.res_dict["fail"]:
                self.res_dict["fail"][method_name].append((f"{data2}-->>{data1}"))
            else:
                self.res_dict["fail"][method_name] = [(f"{data2}-->>{data1}")]
            return

    def check_xiaxing(self):
        #桌椅加热
        server_name = SEAT_SERVICE_CLIENT
        method_name = "SetHeatingLevel"
        parm1 = {"params": [{"id": 0, "uint8Info": 3}]}
        parm2 = {"params": [{"id": 0, "uint8Info": 2}]}
        can_name = '1'  # tosun bodycan通道1
        can_id = "357"  # 桌椅id 357
        data1 = "00 00 00 00 03"
        data2 = "00 00 00 00 02"
        self.check_send_method(server_name, method_name, parm1, parm2, can_name, can_id, data1, data2)

    def check_send_msg(self, obj, sig_name, value1, value2, server_name, method_name, parm1, parm2):
        '''
        校验 发送 信号 收取event
        @param obj:
        @param sig_name:
        @param value1:
        @param value2:
        @param server_name:
        @param method_name:
        @param parm1:
        @param parm2:
        @return:
        '''
        self.ipdu.set(obj, sig_name, value1)  # 20ms
        self.partner.empty_all(0.2)
        self.ipdu.set(obj, sig_name, value2)  # 20ms
        global g_res_dict_up
        time1 = time.time()
        try:
            otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))
            logger.info(f"otherStyleTime>>{otherStyleTime} ")
            self.partner.ck_s2s_event(server_name, method_name, parm2)  # event
            time2 = time.time()
            with allure.step(f"{value1}-->>{value2} 获取成功，时间差为>>>{time2 - time1}s"):
                logger.info(f"{value1}-->>{value2} 获取成功，时间差为>>>{time2 - time1}s")
            if sig_name in self.res_dict_up["success"]:
                self.res_dict_up["success"][sig_name].append((f"{value1}-->>{value2}", time2 - time1))
            else:
                self.res_dict_up["success"][sig_name] = [(f"{value1}-->>{value2}", time2 - time1)]

            if sig_name in g_res_dict_up["success"]:

                g_res_dict_up["success"][sig_name].append((f"{value1}-->>{value2}", time2 - time1))
            else:

                g_res_dict_up["success"][sig_name] = [(f"{value1}-->>{value2}", time2 - time1)]
        except Exception as e:
            with allure.step(f"{value1}-->>{value2} 获取失败{str(e)}"):
                logger.info(f"{value1}-->>{value2} 获取失败{str(e)}")
            if sig_name in g_res_dict_up["fail"]:
                g_res_dict_up["fail"][sig_name].append((f"{value1}-->>{value2}"))
            else:
                g_res_dict_up["fail"][sig_name] = [(f"{value1}-->>{value2}")]

            if sig_name in self.res_dict_up["fail"]:
                self.res_dict_up["fail"][sig_name].append((f"{value1}-->>{value2}"))

            else:
                self.res_dict_up["fail"][sig_name] = [(f"{value1}-->>{value2}")]


        self.ipdu.set(obj, sig_name, value2)
        self.partner.empty_all(0.2)
        self.ipdu.set(obj, sig_name, value1)  # 20ms
        time1 = time.time()
        try:
            self.partner.ck_s2s_event(server_name, method_name, parm1)  # event
            time2 = time.time()
            with allure.step(f"{value2}-->>{value1} 获取成功，时间差为>>>{time2 - time1}s"):
                logger.info(f"{value2}-->>{value1} 获取成功，时间差为>>>{time2 - time1}s")

            if sig_name in self.res_dict_up["success"]:
                self.res_dict_up["success"][sig_name].append((f"{value2}-->>{value1}", time2 - time1))
            else:
                self.res_dict_up["success"][sig_name] = [(f"{value2}-->>{value1}", time2 - time1)]

            if sig_name in g_res_dict_up["success"]:
                g_res_dict_up["success"][sig_name].append((f"{value2}-->>{value1}", time2 - time1))
            else:
                g_res_dict_up["success"][sig_name] = [(f"{value2}-->>{value1}", time2 - time1)]
        except Exception as e:
            with allure.step(f"{value2}-->>{value1} 获取失败{str(e)}"):
                logger.info(f"{value2}-->>{value1} 获取失败{str(e)}")
            if sig_name in g_res_dict_up["fail"]:
                g_res_dict_up["fail"][sig_name].append((f"{value2}-->>{value1}"))
            else:
                g_res_dict_up["fail"][sig_name] = [(f"{value2}-->>{value1}")]

            if sig_name in self.res_dict["fail"]:
                self.res_dict_up["fail"][sig_name].append((f"{value2}-->>{value1}"))
            else:
                self.res_dict_up["fail"][sig_name] = [(f"{value2}-->>{value1}")]


    def check_shangxing(self):

        obj = self.ipdu.propulsioncan.BecmPropFr01
        sig_name = 'HvSysRlyStsHvSysRlySts'
        value1 = 0
        value2 = 2
        server_name = "HighVoltageService_client"
        method_name = 'hvActiveSts'
        parm1 = {"sts": 0}
        parm2 = {"sts": 2}
        self.check_send_msg(obj, sig_name, value1, value2, server_name, method_name, parm1, parm2)

        obj = self.ipdu.backbonefr.VddmBackBoneFr16
        sig_name = 'ChrgnOrDisChrgnStsFb'
        value1 = 0
        value2 = 10
        server_name = "HighVoltageService_client"
        method_name = 'ChargingInfo'
        parm1 = {"info": {"chargingState": 0}}
        parm2 = {"info": {"chargingState": 10}}
        self.check_send_msg(obj, sig_name, value1, value2, server_name, method_name, parm1, parm2)

        obj = self.ipdu.bodycan.PdmBodyFr01
        sig_name = 'MirrFoldStsAtPass_0_PdmBodySignalIPdu01'
        value1 = 0
        value2 = 2
        server_name = "OuterRearViewService_client"
        method_name = 'OuterRearViewFoldStatus'
        parm1 = {"status": [{"id": 0, "value": 0}]}
        parm2 = {"status": [{"id": 0, "value": 2}]}
        self.check_send_msg(obj, sig_name, value1, value2, server_name, method_name, parm1, parm2)

        obj = self.ipdu.bodycan.RldmBodyFr02
        sig_name = 'WinSwtStsAtReLe'
        value1 = 0
        value2 = 4
        server_name = "WindowService_client"
        method_name = 'NotifyWindowSwitchStatus'
        parm1 = {"info": {"zone": 5, "sts": 0}}
        parm2 = {"info": {"zone": 5, "sts": 4}}
        self.check_send_msg(obj, sig_name, value1, value2, server_name, method_name, parm1, parm2)

        obj = self.ipdu.bodycan.PdmBodyFr01
        sig_name = 'WinSwtStsAtPass'
        value1 = 0
        value2 = 5
        server_name = "WindowService_client"
        method_name = 'NotifyWindowSwitchStatus'
        parm1 = {"info": {"zone": 4, "sts": 0}}
        parm2 = {"info": {"zone": 4, "sts": 5}}
        self.check_send_msg(obj, sig_name, value1, value2, server_name, method_name, parm1, parm2)

    def count_success(self, data, type_string="下行"):
        '''
        统计成功率
        @param data:
        @param type_string:
        @return:
        '''
        try:
            if data["success"]:
                success = sum([len(i) for i in list(data["success"].values())])
            else:
                success = 0
            if data["fail"]:
                fail = sum([len(i) for i in list(data["fail"].values())])
            else:
                fail = 0

            string = f"{type_string}成功{success}次 失败{fail}次，成功率{(success) / (success + fail) * 100}%"
            with allure.step(string):
                logger.info(string)
            for name, info in data["success"].items():
                count1 = len(info)
                count2 = len(data["fail"].get(name, []))
                string = f"=======>>>{name} 成功{count1}次 失败{count2}次，成功率{(count1) / (count2 + count1) * 100}%"
                with allure.step(string):
                    logger.info(string)
        except Exception as e:
            logger.error(f"统计成功率失败>>{str(e)}")

    def test_caseid_1983931(self):
        sleep(5)

    @pytest.mark.repeat(100)
    @pytest.mark.pressure
    def test_caseid_1983932(self):

        global g_res_dict
        global g_res_dict_up

        self.res_dict = {
            "success": {
            },
            "fail": {
            },
        }

        self.res_dict_up = {
            "success": {
            },
            "fail": {
            },
        }

        tcpdump_time = time.time()
        while time.time() - tcpdump_time < 5*60:
            logger.info("开始下行数据测试")
            self.check_xiaxing()
            logger.info("开始上行数据测试")
            self.check_shangxing()
            if len(self.res_dict['fail']) or len(self.res_dict_up['fail']):
                break

        self.count_success(self.res_dict, )
        self.count_success(self.res_dict_up, "上行")

        self.count_success(g_res_dict, "所有下行")
        self.count_success(g_res_dict_up, "所有上行")

        self.bgm_ssh.stop_bgm_tcpdump()

        if len(self.res_dict['fail']) or len(self.res_dict_up['fail']):
            local_path = os.path.dirname(os.path.abspath(__file__))
            self.bgm_ssh.get_log(local_path)

        logger.info(f"self.res_dict=>>>{self.res_dict}")
        logger.info(f"self.res_dict_up=>>>{self.res_dict_up}")
        assert (not len(self.res_dict['fail'])) and (not len(self.res_dict_up['fail']))

# pytest test_performance/test_bgm_sig_loss.py --maxfail=1
# nohup  pytest test_performance/test_bgm_sig_loss.py --maxfail=1 > pressure0901.txt 2>&1 &
