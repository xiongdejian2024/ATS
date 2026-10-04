#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_InterCommService.py
@Time         :2023/09/24 09:52:31
@Author       :jishu.duan_ext
@Description  :
"""
import pytest
import allure
from random import randint
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.sdk.digital_key.digital_key_const import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_cases.legacy.soa.case_helper.test_base import *
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding, logger
from xat_ecu.legacy.interface.bgm.bgm_env.change_bgm_env import *


@allure.feature("SOA服务接口")
@allure.story("内部通信服务/InterCommService")
class TestInterCommService(TestBase):

    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu, enable_inter_service=True)
        self.partner = S2sBaseClass([("InterCommService", "client", "BGM_InterCommService"),
                                     ("VehicleSetStatusService", "client"),
                                     ("DoorService", "client")])
        self.partner.wait_for_service_reconnect(INTERCOMM_SERVICE_CLIENT)

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.nucapp.bgm_diag_line_up()
        super().after_each_func(ecu, start=False)
        
    def kill_app_process(self, xy = None):
        if xy is None:
            for process_name in ["monitor_em2.sh", "em2", "s2s_service"]:
                res = command_send(
                    device_name="BGM",
                    cmd=f"ps -ef |grep app |grep {process_name} |grep -v grep",
                    timeout=60,
                )[1]
                pid = res.split()[1]
                command_send(device_name="BGM", cmd=f"kill -9 {pid}")
        else:
            for process_name in ["monitor_em2.sh", "em2", "s2s_service", xy]:
                res = command_send(
                    device_name="BGM",
                    cmd=f"ps -ef |grep app |grep {process_name} |grep -v grep",
                    timeout=60,
                )[1]
                pid = res.split()[1]
                command_send(device_name="BGM", cmd=f"kill -9 {pid}")
            sleep(10)

    @allure.title("SetUtcTimeInfo")
    @pytest.mark.full
    def test_caseid_1984026(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, 'SetUtcTimeInfo',
                                         {"info": {"UTCTime": 101525559,
                                                   "UTCTimeBcd": 0x20240117010102,
                                                   "TimeZone": 23,
                                                   "GlobalTime": 1234567}})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_signal_values("UTCTimeEth", [101525559])
        self.bgm_eth_inter.ck_signal_values("UTCTimeBcdEth", [0x20240117010102])
        self.bgm_eth_inter.ck_signal_values("TimeZoneEth", [23])
        self.bgm_eth_inter.ck_signal_values("GlobalTimeEth",[1234567]) 
        
    @allure.title("GetUtcTime_NotifyUtcTime")
    @pytest.mark.full
    def test_caseid_1984045(self):
        flag = True
        try:
            self.kill_app_process()
            self.bgm_eth_inter.start_bgm_tcpdump(port =30501)
            self.bgmcli.type_commands('su - s2s_service -c "source /app/etc/bgm_app_env.sh load_env;umask 0007; /app/bin/s2s_service"', alias="1", timeout=5)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=100)
            a=len(self.bgm_eth_inter.get_signal_values("UTCTimeEthUp"))
            res1 = self.partner.send_request_and_return_resp(INTERCOMM_SERVICE_CLIENT, 'GetUtcTime', {})['out']
            res2 = self.partner.return_latest_event(INTERCOMM_SERVICE_CLIENT, 'NotifyUtcTime')['time']
            logger.info(f"res2..................................{res2}")
            logger.info(f"打印................{a}")
            assert res1 == res2
            assert 55< a <65
        except:
            flag = False
        self.restart_bgm_and_connect_service(INTERCOMM_SERVICE_CLIENT) 
        sleep(5)
        assert flag

    @allure.title("SetEnterBootmodeSts")
    @pytest.mark.sanity
    def test_caseid_1984047(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        for mode in [True, False]:
            self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, 'SetEnterBootmodeSts',
                                             {"isEnterBootmode": mode})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values("ECUsEthCommSts", [1, 0])
        
    @allure.title("SetFotaSts_参数遍历")
    @pytest.mark.smoke
    def test_caseid_1981087(self):
        flag = True
        try:
            self.kill_app_process("fota")
            self.bgmcli.type_commands('su - s2s_service -c "source /app/etc/bgm_app_env.sh load_env;umask 0007; /app/bin/s2s_service"', alias="1", timeout=5)
            self.partner.wait_for_service_reconnect(INTERCOMM_SERVICE_CLIENT)
            self.bgm_eth_inter.start_bgm_tcpdump()
            sleep(2)
            for sts in range(7):
                logger.info(f"当前参数.{sts}")
                self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, 'SetFotaSts', {"sts": sts})
                sleep(0.7)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
            self.bgm_eth_inter.ck_ordered_array("FOTAStatus", [0,1,2,3,4,5,6])
        except:
            flag = False
        self.restart_bgm_and_connect_service(INTERCOMM_SERVICE_CLIENT) 
        sleep(15)
        assert flag

    @allure.title("SetFotaSts_服务启动无初始值")
    @pytest.mark.full
    def test_caseid_1984313(self):
        flag = True
        try:
            self.kill_app_process("fota")
            self.bgmcli.type_commands('su - s2s_service -c "source /app/etc/bgm_app_env.sh load_env;umask 0007; /app/bin/s2s_service"', alias="1", timeout=5)
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
            self.bgm_eth_inter.ck_signal_values("FOTAStatus", [])
        except:
            flag = False
        self.restart_bgm_and_connect_service(INTERCOMM_SERVICE_CLIENT) 
        sleep(15)
        assert flag

    @allure.title("SetVFCReqXXX")
    @pytest.mark.smoke
    def test_caseid_1983994(self):
        flag = True
        try:
            self.kill_app_process("arbitrateMgr")
            self.bgmcli.type_commands('su - s2s_service -c "source /app/etc/bgm_app_env.sh load_env;umask 0007; /app/bin/s2s_service"', alias="1", timeout=5)
            self.bgm_eth_inter.start_bgm_tcpdump()
            for sigset in ['SetVFCReqInfotainmentPush', 'SetVFCReqLocking', 'SetVFCReqExteriorLighting',
                            'SetVFCReqPowerClosures', 'SetVFCReqPostClimatisation', 'SetVFCReqVisibility',
                            'SetVFCReqSettingsComfort', 'SetVFCReqRemoteKeyFunctionality', 'SetVFCReqSettingsProfile',
                            'SetVFCReqSettingsVehicle', 'SetVFCReqIPWakeup', 'SetVFCReqFunctionmarket',
                            'SetVFCReqPropulsionStart', 'SetVFCReqChargingHV', 'SetVFCReqChargingLVInit',
                            'SetVFCReqImmobilizer', 'SetVFCReqParkingDrivingClimatization',
                            'SetVFCReqTelematicsConnectivity', 'SetVFCReqTrailerCaravanFunctions',
                            'SetVFCReqLifeDetection', 'SetVFCReqVisualAssist', 'SetVFCReqVehicleDriving',
                            'SetVFCReqVehicleModeManagement', 'SetVFCReqDiagnostic', 'SetVFCReqGlobalShortDuration',
                            'SetVFCReqInfotainmentPoll', 'SetVFCReqInteriorLighting', 'SetVFCReqAlarm', 'SetVFCReqBrake',
                            'SetVFCReqHVBatteryThermalEventWarning', 'SetVFCReqHVEngergyStorage',
                            'SetVFCReqPowertrainParkingClimatization', 'SetVFCReqDoorOpenWarning', 'SetVFCReqWindows',
                            'SetVFCReqSeatComFortFunctions', 'SetVFCReqBodyPreClimatisation',
                            'SetVFCReqExteriorLightsHazard', 'SetVFCReqCrash', 'SetVFCReqPassiveSafety',
                            'SetVFCReqBackboneFlexray']:
                self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, sigset,
                                                {"isEnable": True, 'actDurTime': 10})
                sleep(0.2)
                self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, sigset,
                                                {"isEnable": False, 'actDurTime': 0})
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=10)
            for isE in ["VFCReqInfotainmentPush", "VFCReqLocking", "VFCReqExteriorLighting", "VFCReqPowerClosures","VFCReqPostClimatisation","VFCReqVisibility","VFCReqSettingsComfort",
            "VFCReqRemoteKeyFunctionality", "VFCReqSettingsProfile", "VFCReqSettingsVehicle", "VFCReqIPWakeup", "VFCReqFunctionmarket", "VFCReqPropulsionStart", "VFCReqChargingHV",
            "VFCReqChargingLVInit", "VFCReqImmobilizer", "VFCReqParkingDrivingClimatization", "VFCReqTelematicsConnectivity", "VFCReqTrailerCaravanFunctions", "VFCReqLifeDetection",
            "VFCReqVisualAssist", "VFCReqVehicleDriving", "VFCReqVehicleModeManagement", "VFCReqDiagnostic", "VFCReqGlobalShortDuration", "VFCReqInfotainmentPoll", "VFCReqInteriorLighting",
            "VFCReqAlarm", "VFCReqBrake", "VFCReqHVBatteryThermalEventWarning", "VFCReqHVEngergyStorage", "VFCReqPowertrainParkingClimatization", "VFCReqDoorOpenWarning",
            "VFCReqWindows", "VFCReqSeatComFortFunctions", "VFCReqBodyPreClimatisation", "VFCReqExteriorLightsHazard", "VFCReqCrash", "VFCReqPassiveSafety", "VFCReqBackboneFlexray"]:
                self.bgm_eth_inter.ck_ordered_array(isE, [1, 0])
            for actD in ["ActDurTimeInfotainmentPush", "ActDurTimeLocking", "ActDurTimeExteriorLighting", "ActDurTimePowerClosures", "ActDurTimePostClimatisation", "ActDurTimeVisibilit",
            "ActDurTimeSettingsComfort", "ActDurTimeRemoteKeyFunctionality", "ActDurTimeSettingsProfile", "ActDurTimeSettingsVehicle", "ActDurTimeIPWakeup", "ActDurTimeFunctionmarket",
            "ActDurTimePropulsionStart", "ActDurTimeChargingHV", "ActDurTimeChargingLVInit", "ActDurTimeImmobilizer", "ActDurTimeParkingDrivingClimatization", "ActDurTimeTelematicsConnectivity",
            "ActDurTimeTrailerCaravanFunctions", "ActDurTimeLifeDetection", "ActDurTimeVisualAssist", "ActDurTimeVehicleDriving", "ActDurTimeVehicleModeManagement", "ActDurTimeDiagnostic",
            "ActDurTimeGlobalShortDuration", "ActDurTimeInfotainmentPoll", "ActDurTimeInteriorLighting", "ActDurTimeAlarm", "ActDurTimeBrake", "ActDurTimeHVBatteryThermalEventWarning", 
            "ActDurTimeHVEngergyStorage", "ActDurTimePowertrainParkingClimatization", "ActDurTimeDoorOpenWarning", "ActDurTimeWindows", "ActDurTimeSeatComFortFunctions", "ActDurTimeBodyPreClimatisation",
            "ActDurTimeExteriorLightsHazard", "ActDurTimeCrash", "ActDurTimePassiveSafety", "ActDurTimeBackboneFlexray"]:
                self.bgm_eth_inter.ck_ordered_array(actD, [10, 0])
        except:
            flag = False
        self.restart_bgm_and_connect_service(INTERCOMM_SERVICE_CLIENT) 
        sleep(15)
        assert flag       

    @allure.title("设置洗车模式")
    @pytest.mark.sanity
    def test_caseid_1984074(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        for mode in [True, False]:
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": mode})
            self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": mode}) 
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values("WashModeSts", [1, 0])

    @allure.title("设置雨天关窗功能_服务初始化无默认值")
    @pytest.mark.full
    def test_caseid_1984715(self): 
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.kill_s2s_and_reconnect_service(INTERCOMM_SERVICE_CLIENT)  
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=10)
        # self.bgm_eth_inter.ck_signal_values("SetRainAutoClsWin", [0])
        # 对该设置参数isOn进行非易失存储记忆，每次服务启动后，调用一次Intercomm::SetRainAutoCloseWindowS2S接口
        val = self.bgm_eth_inter.get_signal_values("SetRainAutoClsWin") 
        assert val in [[0], [1]]
        
    @allure.title("设置雨天关窗功能_遍历on/off")
    @pytest.mark.sanity
    def test_caseid_1984075(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        for mode in [True, False]:
            self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, 'SetRainAutoCloseWindowS2S',
                                             {"isOn": mode})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values("SetRainAutoClsWin", [1, 0])
        
    @allure.title("设置闭锁提示_遍历参数")
    @pytest.mark.smoke
    def test_caseid_1984089(self):
        sleep(1)
        for mode in range(5):
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, 'SetLockReminder',
                                                {"reminder": mode})
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
            self.bgm_eth_inter.ck_signal_values("ReminderWhileLock", [mode,mode,mode,0])
            self.bgm_eth_inter.ck_period_time("ReminderWhileLock", 0.2 ,deviation=0.4)
        
    @allure.title("设置闭锁提示_校验报文打断逻辑")
    @pytest.mark.full
    def test_caseid_1984090(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, 'SetLockReminder',
                                             {"reminder": 4})
        sleep(0.1)
        self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, 'SetLockReminder',
                                             {"reminder": 4})
        sleep(1)
        self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, 'SetLockReminder',
                                             {"reminder": 3})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values("ReminderWhileLock", [4, 4, 4, 0, 3, 3, 3, 0])
        
    @allure.title("SetDiagnosticExtConnect_遍历参数")
    @pytest.mark.sanity
    def test_caseid_1984119(self):
        flag = True
        try:
            self.kill_app_process("arbitrateMgr")
            self.bgmcli.type_commands('su - s2s_service -c "source /app/etc/bgm_app_env.sh load_env;umask 0007; /app/bin/s2s_service"', alias="1", timeout=5)
            self.nucapp.bgm_diag_line_down()
            sleep(1)
            self.bgm_eth_inter.start_bgm_tcpdump()
            for mode in [1, 0]:
                self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, 'SetDiagnosticConnectStatus',
                                                {"connectStatus": mode, "connectActive": mode})
            self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, 'SetDiagnosticConnectStatus',
                                                {"connectStatus": 0, "connectActive": 1})    
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
            self.bgm_eth_inter.ck_signal_values("DiagcExtCom", [1, 0, 0])
            self.bgm_eth_inter.ck_signal_values("DiagcComActv", [1, 0, 1])
            self.nucapp.bgm_diag_line_up()
        except:
            flag = False
        self.restart_bgm_and_connect_service(INTERCOMM_SERVICE_CLIENT) 
        sleep(5)
        assert flag  
          
    @allure.title("SetIpcSlvKeepAlive")
    @pytest.mark.sanity
    def test_caseid_1984126(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, 'SetIpcSlvKeepAlive',
                                             {"time": 10})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values("IpcSlvKeepAlive", [10])
        
    @allure.title("设置踩刹车自动关门功能禁用状态_遍历参数")
    @pytest.mark.smoke
    def test_caseid_1984127(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for sts in [True, False]:
            self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, 'SetBrakeCloseDoorInhibitStatus',
                                             {"isInhibit": sts})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_ordered_array('BrakeCloseDoorInhibitStatus', [1, 0])      

    @allure.title("设置踩刹车自动关门功能禁用状态_服务启动初始值")
    @pytest.mark.full
    def test_caseid_1984137(self):
        self.kill_s2s_and_reconnect_service(INTERCOMM_SERVICE_CLIENT)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=10)
        self.bgm_eth_inter.ck_ordered_array('BrakeCloseDoorInhibitStatus', [0])
        self.bgm_eth_inter.ck_period_time('BrakeCloseDoorInhibitStatus', 1, deviation=0.4)
        
    @allure.title("设置P档迎宾功能_遍历参数")
    @pytest.mark.smoke
    def test_caseid_1984177(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        for sts in [True, False]:
            self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, "SetCourtesyLightStsGearP", {"sts": sts})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('IfPThenIsOrNotCourtesy', [1, 0])
        
    @allure.title("SetLvSocCalibInfo")
    @pytest.mark.full
    def test_caseid_1984289(self):
        list=[randint(0x0, 0xF) for i in range(1024)]
        logger.info(f"打印list={list}")
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(5)
        self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, 'SetLvSocCalibInfo',
              {"info": {"calibType": 10, "calibSubType": 10, "calibData":list}})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('LvSocCalibType', [10])
        self.bgm_eth_inter.ck_signal_values('LvSocCalibSubType', [10])
        self.bgm_eth_inter.ck_signal_values('LvSocCalibData', [DataTypeHanding.to_int(list)])

    @allure.title("DiagnosticActivationLineStatus/GetDiagnosticActivationLineStatus_未激活")
    @pytest.mark.sanity
    def test_caseid_1984166(self): 
        self.nucapp.bgm_diag_line_up()
        self.bgm_eth_inter.start_bgm_tcpdump(port =30501)
        sleep(1)
        logger.info("断开诊断激活线1*************************************************************")
        self.nucapp.bgm_diag_line_down()
        self.partner.ck_s2s_event(INTERCOMM_SERVICE_CLIENT, "DiagnosticActivationLineStatus", {"status": 0})
        self.partner.send_request_and_ck_resp(INTERCOMM_SERVICE_CLIENT, 'GetDiagnosticActivationLineStatus', {}, {"out": 0})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_ordered_array('ActivationLineStatus', [0])
        
    @allure.title("DiagnosticActivationLineStatus/GetDiagnosticActivationLineStatus_激活")
    @pytest.mark.full
    def test_caseid_1984167(self):
        logger.info("断开诊断激活线1*************************************************************") 
        self.nucapp.bgm_diag_line_down()
        self.bgm_eth_inter.start_bgm_tcpdump(port =30501)
        self.nucapp.bgm_diag_line_up()
        self.partner.ck_s2s_event(INTERCOMM_SERVICE_CLIENT, "DiagnosticActivationLineStatus", {"status": 1})
        self.partner.send_request_and_ck_resp(INTERCOMM_SERVICE_CLIENT, 'GetDiagnosticActivationLineStatus', {}, {"out": 1})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_ordered_array('ActivationLineStatus', [1])
        
    @allure.title("BGMPartNum/GetBGMPartNum")
    @pytest.mark.sanity
    def test_caseid_1984173(self):
        self.bgm_eth_inter.start_bgm_tcpdump(port =30501)
        sleep(1)
        self.kill_s2s_and_reconnect_service(INTERCOMM_SERVICE_CLIENT)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=10)    
        string_hex = hex(self.bgm_eth_inter.get_signal_values("SerialNumber")[0])[2:].zfill(8)
        list0 = [int(string_hex[i:i+2], 16)for i in range(0, len(string_hex), 2)]
        string_hex = hex(self.bgm_eth_inter.get_signal_values("CoreAssemblyPN")[0])[2:].zfill(16)
        list1 = [int(string_hex[i:i+2], 16)for i in range(0, len(string_hex), 2)]
        string_hex = hex(self.bgm_eth_inter.get_signal_values("DeliveryAssemblyPN")[0])[2:].zfill(16)
        list3 = [int(string_hex[i:i+2], 16)for i in range(0, len(string_hex), 2)]
        string_hex = hex(self.bgm_eth_inter.get_signal_values("PBLPN")[0])[2:].zfill(16)
        list2= [int(string_hex[i:i+2], 16)for i in range(0, len(string_hex), 2)]   
        SerialNumber = list(reversed(list0))
        PBLPN = list(reversed(list2))
        CoreAssemblyPN = list (reversed(list1))
        DeliveryAssemblyPN = list (reversed(list3))
        logger.info(f"当前PBLPN的值。。。。。。。。。。。。。。。。。。。。.{PBLPN},.{CoreAssemblyPN}")
        res1 = self.partner.send_request_and_return_resp(INTERCOMM_SERVICE_CLIENT, 'GetBGMPartNum', {})['out']
        res2 = self.partner.ck_s2s_event(INTERCOMM_SERVICE_CLIENT, 'NotifyBGMPartNum', {})['num']
        assert CoreAssemblyPN == res2.get("coreAssemPN")
        assert DeliveryAssemblyPN == res2.get("deliveryAssemPN")
        assert SerialNumber == res2.get("serialNum")
        assert PBLPN == res2.get("versionPBLPN")
        assert res1 == res2

    @allure.title("TcpConnStateInfo/GetTcpConnStateInfo_遍历参数")
    @pytest.mark.sanity
    def test_caseid_1984290(self):
        flag = True
        try:
            self.update_bgm_s2s_json({"mcuIpTcp":"172.16.5.5"},partner_key=INTERCOMM_SERVICE_CLIENT)  
            logger.info({f'修改错误s2s文件'})    
            self.partner.ck_s2s_event(INTERCOMM_SERVICE_CLIENT, "TcpConnStateInfo", {"tcpType":2,"tcpState":1})
            self.partner.send_request_and_ck_resp(INTERCOMM_SERVICE_CLIENT, "GetTcpConnStateInfo",{"tcpType":2}, {"out":1})
        except:
            flag = False
        self.update_bgm_s2s_json({"mcuIpTcp":"172.16.5.2"},partner_key=INTERCOMM_SERVICE_CLIENT) 
        logger.info({f'修改正确s2s文件'})
        self.partner.ck_s2s_event(INTERCOMM_SERVICE_CLIENT, "TcpConnStateInfo", {"tcpType":2,"tcpState":3})
        self.partner.send_request_and_ck_resp(INTERCOMM_SERVICE_CLIENT, "GetTcpConnStateInfo",{"tcpType":2}, {"out":3})
        assert flag
        
    @allure.title("设置域控重启_TCAM")
    @pytest.mark.smoke
    def test_caseid_1984712(self):  
        self.bgm_eth_inter.start_bgm_tcpdump()  
        sleep(1)
        self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, "SetDomainControllerReset", {"domain": [2]})
        self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, "SetDomainControllerReset", {"domain": [2]})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=10)
        for digit in range(8):
            if digit == 0:
                self.bgm_eth_inter.ck_signal_values(f'BGMMPUCtrlTCAMByte{digit}', [82, 82, 82, 82, 82, 82, 82, 82, 82])
            elif digit == 1:
                self.bgm_eth_inter.ck_signal_values(f'BGMMPUCtrlTCAMByte{digit}', [1, 2, 3, 1, 2, 3, 1, 2, 3])
            else:
                self.bgm_eth_inter.ck_signal_values(f'BGMMPUCtrlTCAMByte{digit}', [0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    @allure.title("设置域控重启_CDC")
    @pytest.mark.full
    def test_caseid_1984711(self):  
        self.bgm_eth_inter.start_bgm_tcpdump()  
        sleep(1)
        self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, "SetDomainControllerReset", {"domain": [1]})
        self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, "SetDomainControllerReset", {"domain": [1]})
        sleep(5)
        self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, "SetDomainControllerReset", {"domain": [1,2]})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=10)
        for digit in range(8):
            if digit == 0:
                self.bgm_eth_inter.ck_signal_values(f'BGMMPUCtrlCDCByte{digit}', [82, 82, 82, 82, 82, 82, 82, 82, 82,
                                                                                  82, 82, 82, 82, 82, 82, 82, 82, 82])
                self.bgm_eth_inter.ck_signal_values(f'BGMMPUCtrlTCAMByte{digit}', [82, 82, 82, 82, 82, 82, 82, 82, 82])
            elif digit == 1:
                self.bgm_eth_inter.ck_signal_values(f'BGMMPUCtrlCDCByte{digit}', [1, 2, 3, 1, 2, 3, 1, 2, 3,
                                                                                  1, 2, 3, 1, 2, 3, 1, 2, 3])
                self.bgm_eth_inter.ck_signal_values(f'BGMMPUCtrlTCAMByte{digit}', [1, 2, 3, 1, 2, 3, 1, 2, 3])      
            else:
                self.bgm_eth_inter.ck_signal_values(f'BGMMPUCtrlCDCByte{digit}', [0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                                  0, 0, 0, 0, 0, 0, 0, 0, 0])
                self.bgm_eth_inter.ck_signal_values(f'BGMMPUCtrlTCAMByte{digit}', [0, 0, 0, 0, 0, 0, 0, 0, 0])
        
    @allure.title("设置域控重启_ACU")
    @pytest.mark.full
    def test_caseid_1984704(self):  
        self.bgm_eth_inter.start_bgm_tcpdump()  
        sleep(1)
        self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, "SetDomainControllerReset", {"domain": [0]})
        self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, "SetDomainControllerReset", {"domain": [0,1]})
        sleep(7)
        self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, "SetDomainControllerReset", {"domain": [0,1,2]})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=10)
        for digit in range(8):
            if digit == 0:
                self.bgm_eth_inter.ck_signal_values(f'BGMMPUCtrlACUByte{digit}', [82, 82, 82, 82, 82, 82, 82, 82, 82,
                                                                                  82, 82, 82, 82, 82, 82, 82, 82, 82])
                self.bgm_eth_inter.ck_signal_values(f'BGMMPUCtrlCDCByte{digit}', [82, 82, 82, 82, 82, 82, 82, 82, 82,
                                                                                  82, 82, 82, 82, 82, 82, 82, 82, 82])
                self.bgm_eth_inter.ck_signal_values(f'BGMMPUCtrlTCAMByte{digit}', [82, 82, 82, 82, 82, 82, 82, 82, 82])
            elif digit == 1:
                self.bgm_eth_inter.ck_signal_values(f'BGMMPUCtrlACUByte{digit}', [1, 2, 3, 1, 2, 3, 1, 2, 3,
                                                                                  1, 2, 3, 1, 2, 3, 1, 2, 3])
                self.bgm_eth_inter.ck_signal_values(f'BGMMPUCtrlCDCByte{digit}', [1, 2, 3, 1, 2, 3, 1, 2, 3,
                                                                                  1, 2, 3, 1, 2, 3, 1, 2, 3])
                self.bgm_eth_inter.ck_signal_values(f'BGMMPUCtrlTCAMByte{digit}', [1, 2, 3, 1, 2, 3, 1, 2, 3])  
            else:
                self.bgm_eth_inter.ck_signal_values(f'BGMMPUCtrlACUByte{digit}', [0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                                  0, 0, 0, 0, 0, 0, 0, 0, 0])
                self.bgm_eth_inter.ck_signal_values(f'BGMMPUCtrlCDCByte{digit}', [0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                                  0, 0, 0, 0, 0, 0, 0, 0, 0])
                self.bgm_eth_inter.ck_signal_values(f'BGMMPUCtrlTCAMByte{digit}', [0, 0, 0, 0, 0, 0, 0, 0, 0])   

    @allure.title("设置域控重启_信号路由检查")
    @pytest.mark.full
    def test_caseid_1988825(self):  
        self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, "SetDomainControllerReset", {"domain": [0]})
        self.ipdu.check_multiple_signals([(self.ipdu.adcanfd.BgmADCANFDFr31, 'BGMMPUCtrlACUByte0', 0x52),
                                          (self.ipdu.adcanfd.BgmADCANFDFr31, 'BGMMPUCtrlACUByte1', 0x01),
                                          (self.ipdu.adcanfd.BgmADCANFDFr31, 'BGMMPUCtrlACUByte2', 0),
                                          (self.ipdu.adcanfd.BgmADCANFDFr31, 'BGMMPUCtrlACUByte3', 0),
                                          (self.ipdu.adcanfd.BgmADCANFDFr31, 'BGMMPUCtrlACUByte4', 0),
                                          (self.ipdu.adcanfd.BgmADCANFDFr31, 'BGMMPUCtrlACUByte5', 0),
                                          (self.ipdu.adcanfd.BgmADCANFDFr31, 'BGMMPUCtrlACUByte6', 0),
                                          (self.ipdu.adcanfd.BgmADCANFDFr31, 'BGMMPUCtrlACUByte7', 0)], timeout=0.5)
        
        self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, "SetDomainControllerReset", {"domain": [1]})
        self.ipdu.check_multiple_signals([(self.ipdu.infocanfd.BgmInfoCanFdFr24, 'BGMMPUCtrlCDCByte0', 0x52),
                                          (self.ipdu.infocanfd.BgmInfoCanFdFr24, 'BGMMPUCtrlCDCByte1', 0x01),
                                          (self.ipdu.infocanfd.BgmInfoCanFdFr24, 'BGMMPUCtrlCDCByte2', 0),
                                          (self.ipdu.infocanfd.BgmInfoCanFdFr24, 'BGMMPUCtrlCDCByte3', 0),
                                          (self.ipdu.infocanfd.BgmInfoCanFdFr24, 'BGMMPUCtrlCDCByte4', 0),
                                          (self.ipdu.infocanfd.BgmInfoCanFdFr24, 'BGMMPUCtrlCDCByte5', 0),
                                          (self.ipdu.infocanfd.BgmInfoCanFdFr24, 'BGMMPUCtrlCDCByte6', 0),
                                          (self.ipdu.infocanfd.BgmInfoCanFdFr24, 'BGMMPUCtrlCDCByte7', 0)], timeout=0.5)

        self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, "SetDomainControllerReset", {"domain": [2]})
        self.ipdu.check_multiple_signals([(self.ipdu.connectivitycanfd.BgmConnectivityFr22, 'BGMMPUCtrlTCAMByte0', 0x52),
                                          (self.ipdu.connectivitycanfd.BgmConnectivityFr22, 'BGMMPUCtrlTCAMByte1', 0x01),
                                          (self.ipdu.connectivitycanfd.BgmConnectivityFr22, 'BGMMPUCtrlTCAMByte2', 0),
                                          (self.ipdu.connectivitycanfd.BgmConnectivityFr22, 'BGMMPUCtrlTCAMByte3', 0),
                                          (self.ipdu.connectivitycanfd.BgmConnectivityFr22, 'BGMMPUCtrlTCAMByte4', 0),
                                          (self.ipdu.connectivitycanfd.BgmConnectivityFr22, 'BGMMPUCtrlTCAMByte5', 0),
                                          (self.ipdu.connectivitycanfd.BgmConnectivityFr22, 'BGMMPUCtrlTCAMByte6', 0),
                                          (self.ipdu.connectivitycanfd.BgmConnectivityFr22, 'BGMMPUCtrlTCAMByte7', 0)], timeout=0.5)
            

@allure.feature("SOA服务接口")
@allure.story("内部通信服务/InterCommService")
@pytest.mark.mock_tcp    
class TestInterCommServiceMockMcu(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu, tcp_down_mcu_ip="172.16.5.21", enable_inter_service=True)
        self.partner = S2sBaseClass(
            [("InterCommService", "client", "BGM_InterCommService"),
                                     ("VehicleSetStatusService", "client"),
                                     ("DoorService", "client")])
        self.partner.wait_for_service_reconnect(INTERCOMM_SERVICE_CLIENT)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
    
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.partner.empty_all()
            
    @allure.title("DiagnosticObdCANStatus/GetDiagnosticObdCANStatus_未激活")
    @pytest.mark.full
    def test_caseid_1984174(self): 
        self.bgm_eth_inter.set_signal("ObdCANStatus", 1, send_pdu_immediately=True)
        sleep(1)
        self.bgm_eth_inter.set_signal("ObdCANStatus", 0, send_pdu_immediately=True)
        sleep(1)
        self.partner.ck_s2s_event(INTERCOMM_SERVICE_CLIENT, "DiagnosticObdCANStatus", {"status": 0})
        self.partner.send_request_and_ck_resp(INTERCOMM_SERVICE_CLIENT, 'GetDiagnosticObdCANStatus', {}, {"out": 0})
          
    @allure.title("DiagnosticObdCANStatus/GetDiagnosticObdCANStatus_激活")
    @pytest.mark.sanity
    def test_caseid_1984175(self): 
        self.bgm_eth_inter.set_signal("ObdCANStatus", 0, send_pdu_immediately=True)
        sleep(1)
        self.bgm_eth_inter.set_signal("ObdCANStatus", 1, send_pdu_immediately=True)
        sleep(1)
        self.partner.ck_s2s_event(INTERCOMM_SERVICE_CLIENT, "DiagnosticObdCANStatus", {"status": 1})
        self.partner.send_request_and_ck_resp(INTERCOMM_SERVICE_CLIENT, 'GetDiagnosticObdCANStatus', {}, {"out": 1})
            
    @allure.title("GetMcuRebootSts/McuRebootSts")  
    @pytest.mark.full
    def test_caseid_1984013(self):
        self.bgm_eth_inter.set_signal("RebootIndicateEth", 1, send_pdu_immediately=True)
        sleep(0.5)
        self.partner.ck_s2s_event(INTERCOMM_SERVICE_CLIENT, 'McuRebootSts', {"isRebooting": True})
        self.partner.send_request_and_ck_resp(INTERCOMM_SERVICE_CLIENT, "GetMcuRebootSts",{}, {"out": True})
        self.bgm_eth_inter.set_signal("RebootIndicateEth", 0, send_pdu_immediately=True)
        sleep(3)
        self.partner.ck_s2s_event(INTERCOMM_SERVICE_CLIENT, 'McuRebootSts', {"isRebooting": False})
        self.partner.send_request_and_ck_resp(INTERCOMM_SERVICE_CLIENT, "GetMcuRebootSts",{}, {"out": False})
    
    @allure.title("ShutdownPrepare/GetShutdownPrepare")
    @pytest.mark.sanity
    def test_caseid_1984291(self): 
        self.bgm_eth_inter.set_signal("IpcVucShutdownReq", 0, send_pdu_immediately=True)
        self.partner.ck_s2s_event(INTERCOMM_SERVICE_CLIENT, "ShutdownPrepare", {"reserveData": 0})
        self.partner.send_request_and_ck_resp(INTERCOMM_SERVICE_CLIENT, 'GetShutdownPrepare', {}, {"out": 0})
        sleep(1)
        self.bgm_eth_inter.set_signal("IpcVucShutdownReq", 1, send_pdu_immediately=True)
        sleep(1)
        self.partner.ck_s2s_event(INTERCOMM_SERVICE_CLIENT, "ShutdownPrepare", {"reserveData": 1})
        self.partner.send_request_and_ck_resp(INTERCOMM_SERVICE_CLIENT, 'GetShutdownPrepare', {}, {"out": 1})
        
    @allure.title("NotifyLvSocUploadInfo/GetLvSocUploadInfo")
    @pytest.mark.sanity
    def test_caseid_1984287(self): 
        self.bgm_eth_inter.start_bgm_tcpdump()  
        sleep(2)
        self.bgm_eth_inter.set_signal("LvSocUpBlockNum", 255)
        self.bgm_eth_inter.set_signal("LvSocUpBlockIndex", 10)
        self.bgm_eth_inter.set_signal("LvSocUpData", DataTypeHanding.to_int([0xFF] + [0] * 1023), send_pdu_immediately=True)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.partner.ck_event_and_resp(INTERCOMM_SERVICE_CLIENT, "NotifyLvSocUploadInfo", {"info": {"upBlockNum":255, "upBlockIndex": 10, "upData": [0xFF] + [0] * 1023}}, fuzz_match=False)

@allure.feature("SOA服务接口")   
@allure.story("内部通信服务/InterCommService")
@pytest.mark.mockmcu
class TestInterCommServcieMockMcu(TestBase):

    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21", enable_inter_service=True)
        self.partner = S2sBaseClass([("InterCommService", "client", "BGM_InterCommService")])
        self.partner.wait_for_service_reconnect(INTERCOMM_SERVICE_CLIENT)
        
    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu)            
        self.partner.empty_all()

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        sleep(10)
    
    @allure.title("设置P档迎宾功能_Inactive")
    @pytest.mark.full
    def test_caseid_1984233(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 11)
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1)
        self.kill_s2s_and_reconnect_service(INTERCOMM_SERVICE_CLIENT)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=10)
        self.bgm_eth_inter.ck_signal_values('IfPThenIsOrNotCourtesy', [])
        
    @allure.title("设置P档迎宾功能_Abandon")
    @pytest.mark.full
    def test_caseid_1984231(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 11)
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 0)
        self.kill_s2s_and_reconnect_service(INTERCOMM_SERVICE_CLIENT)
        sleep(5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 11)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('IfPThenIsOrNotCourtesy', [1])
        
    @allure.title("设置P档迎宾功能_Driving")
    @pytest.mark.full
    def test_caseid_1984230(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 11)
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 13)
        self.kill_s2s_and_reconnect_service(INTERCOMM_SERVICE_CLIENT)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('IfPThenIsOrNotCourtesy', [1, 1])
    
    @allure.title("设置P档迎宾功能_Active")
    @pytest.mark.full
    def test_caseid_1984226(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1)
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 11)
        self.kill_s2s_and_reconnect_service(INTERCOMM_SERVICE_CLIENT) 
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('IfPThenIsOrNotCourtesy', [1, 1 ])
        
    @allure.title("设置P档迎宾功能_convenience")
    @pytest.mark.sanity
    def test_caseid_1984225(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1)
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 2)
        self.kill_s2s_and_reconnect_service(INTERCOMM_SERVICE_CLIENT)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('IfPThenIsOrNotCourtesy', [1, 1])