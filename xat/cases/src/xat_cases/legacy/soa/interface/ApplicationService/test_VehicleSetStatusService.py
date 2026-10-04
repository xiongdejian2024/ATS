"""
@File        : test_VehicleSetStatusService.py
@Author      : tao.cheng_ext@jiduatuo.com
@Time        : 2023/06/5 18:00 PM
@Description : Test SOA for VehicleSetStatusService
"""

import pytest
import allure
from time import sleep
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *

FOTAMASTERSERVICE_SERVER = "FotaMasterService_server"
COCKPITPERCEPTION_SERVICE_CLIENT = "cockpit_perception_service_server"

def is_sublist(main_list, sublist):
    if len(main_list) < len(sublist):
        return False
    for i in range(len(main_list) - len(sublist) + 1):
        if main_list[i:i+len(sublist)] == sublist:
            return True
    return False

@allure.feature("SOA服务接口")
@allure.story("BGM应用/VehicleSetStatusService")
class TestVehicleSetStatusService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([
            ("VehicleSetStatusService", "client"),("InteractiveService","server"),
            ("cockpit_perception_service","server"),("VehicleModeService", "client"),("OuterRearViewService", "client"),
            ("CTDService", "client"),("KeyService", "client"),("SeatService", "client"),("HighVoltageService","client")])
        self.partner.method_default_timeout = 2 #veset服务注册事件较多，可以延时
        self.sd_tester.tester_present()

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.set_nopeople_incar()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        sleep(1)
        self.ipdu.set(self.ipdu.cem_lin6.CemCem_Lin6Fr02, "BattSnsrStReq", 1)
        self.ipdu.send_pdu("cem_lin6", 0x06, [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": False}, timeout=2)
        sleep(1)
        self.seat_belt_status(0,0,0,0,0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.ipdu.set_vehspd(0)
        sleep(0.5)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.partner.empty_all(1)


    def after_each_func(self, ecu):
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": False})
        sleep(1)
        self.ipdu.resume_all_bus_send() 
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.partner.stop_operators()
        self.sd_tester.stop_tester_present()
        self.io.trunk_door_outswitch_unpressed()
        super().after_class(self, ecu)
  
    def set_gear_P_speed_0(self):
        '''P档 车速为0'''
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd',  0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24',  0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06', 0)
        sleep(1)

    def five_door_open(self):
        self.io.drvr_door_open()
        self.io.pass_door_open()
        self.io.rire_door_open()
        self.io.lere_door_open()
        self.io.trunk_door_open()
        sleep(1)

    def five_door_close(self):
        self.io.pass_door_close()
        self.io.drvr_door_close()
        self.io.lere_door_close()
        self.io.rire_door_close()
        self.io.trunk_door_close()
        sleep(1)

    def Shift_Gear(self, X):
        """0代表P挡 2代表N挡 3代表D挡 1代表R挡"""
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', X)
        sleep(1)

    def set_four_seat_occupt(self,A,B,C,D):
        """设置副驾 左后 后中 后右 1/2代表占位 0 代表未占位"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts_0_SRSBackBoneSignalIPdu04', A)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe_0_SRSBackBoneSignalIPdu04', B)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecMid_0_SRSBackBoneSignalIPdu04', C)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecRi_0_SRSBackBoneSignalIPdu04', D)
        sleep(1)
    
    def seat_belt_status(self,A,B,C,D,E):
        """设置主驾 副驾 左后 后中 后右 1代表已系 0 代表未系"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', A)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04', B)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecLeBltLockSt1', C)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecLeBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecMidBltLockSt1', D)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecMidBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecRiBltLockSt1', E)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecRiBltLockSts', 0)
        sleep(1)
        
    def ck_powerOutletDelay_warning_and_resp(self,delaySts,delayTimeLeft,modeStsSet,lastSetTime,reason):
        '''工作状态delaySts,  延时剩余时间delayTimeLeft, 类型modeStsS, 最后一次设置时间lastSetTime, 退出原因reason'''
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"PowerOutletDelayInfo",{"sts": 
                                                {"delaySts":delaySts, "delayTimeLeft":delayTimeLeft ,"modeStsSet":modeStsSet ,"lastSetTime":lastSetTime ,"reason":reason }})
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetPowerOutletDelayInfo", {}, 
                                                {"out": {"delaySts":delaySts, "delayTimeLeft":delayTimeLeft ,"modeStsSet":modeStsSet ,"lastSetTime":lastSetTime ,"reason":reason }})
      
    def ck_ipdu_signal(self, period1, period2, period3):
        #3s后RlyPwrCmdProxyReq = 0
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        a = self.bgm_eth_inter.get_signal_values("UsgModKeeperReq")
        b = self.bgm_eth_inter.get_signal_values("HVActvForProxy")
        c = self.bgm_eth_inter.get_signal_values("RlyPwrCmdProxyReq")
        if (is_sublist(a,[0,1,0,0,1,0]) or is_sublist(a,[0,1,0,1,0])) and (is_sublist(b,[1])) and (is_sublist(c,[1,0])):
            pass
        else:
            assert 0 == 1
        # self.bgm_eth_inter.ck_period_time("UsgModKeeperReq", period1)
        # self.bgm_eth_inter.ck_period_time("RlyPwrCmdProxyReq", period3)
        # self.bgm_eth_inter.ck_period_time("HVActvForProxy", period2)


    @allure.title("获取和通知维持上电基础能力_儿童座有人_触发不能闭锁") 
    @pytest.mark.full
    def test_caseid_1988903(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(0x1)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(0,0,0,0,0)
        self.Shift_Gear(0) #P档
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                            {"firstLeftExist":False,"firstRightExist":False,"errorCode":0}})
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{"seatStsSecondLeft":{"installSts":False,"occupySts":False},
                                                    "seatStsSecondRight":{"installSts":False,"occupySts":False}}})
        self.sd_tester.enter_default_session()
        sleep(1)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": 2})
        sleep(3)#无人判断需要3S
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,'VehModMngtGlbSafe1UsgModSts', 2)#不闭锁保持2convenie
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(0,0,0,0,0)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)

        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp",
                                         {"cmd":{"modeSts": 0,"source":"PetMode"}})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        self.partner.empty_all(1)
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{"seatStsSecondLeft":{"installSts":False,"occupySts":False},
                                                    "seatStsSecondRight":{"installSts":True,"occupySts":True}}})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp",
                                         {"cmd":{"modeSts": 1,"source":"PetMode"}})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        self.dk.set_cenlock_sts(3)
        sleep(2)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 19.0)
        sleep(1)
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT,"getAlarmInfo",{},{"out":{"sysSts":0}})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,'VehModMngtGlbSafe1UsgModSts', 2)#不闭锁保持2convenie
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(1)    
        self.bgm_eth_inter.ck_signal_values("MobDevCenLockReq", [])  #不下发闭锁
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 20.0)
        self.dk.set_cenlock_sts(1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)#保持关闭
        self.partner.empty_all(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp",
                                         {"cmd":{"modeSts": 1,"source":"PetMode"}})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        self.five_door_open()
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{"seatStsSecondLeft":{"installSts":False,"occupySts":False},
                                                    "seatStsSecondRight":{"installSts":False,"occupySts":False}}})
        self.five_door_close()
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.dk.send_nfc_cmd()
        sleep(3)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 11)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp",
                                         {"cmd":{"modeSts": 0,"source":"PetMode"}})
        sleep(2)#晚点校验闭锁设防
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortBaseFunctionSts",{},{"out":
                                                        {"modeSts":0,"reason":1,"source":"PetMode"}})#宠物模式
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
        self.bgm_eth_inter.ck_signal_values("MobDevCenLockReq", [2,0])  

    @allure.title("获取和通知维持上电_儿童座有人_触发不能闭锁") 
    @pytest.mark.full
    def test_caseid_1988916(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(0x1)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(0,0,0,0,0)
        self.Shift_Gear(0) #P档
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                            {"firstLeftExist":False,"firstRightExist":False,"errorCode":0}})
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{"seatStsSecondLeft":{"installSts":False,"occupySts":False},
                                                    "seatStsSecondRight":{"installSts":False,"occupySts":False}}})
        self.sd_tester.enter_default_session()
        sleep(1)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": 2})
        sleep(3)#无人判断需要3S
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,'VehModMngtGlbSafe1UsgModSts', 2)#不闭锁保持2convenie
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(0,0,0,0,0)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)

        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp",
                                         {"cmd":{"modeSts": 0,"source":"PetMode"}})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        self.partner.empty_all(1)
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{"seatStsSecondLeft":{"installSts":False,"occupySts":False},
                                                    "seatStsSecondRight":{"installSts":True,"occupySts":True}}})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        self.dk.set_cenlock_sts(3)
        sleep(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 19.0)
        sleep(1)
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT,"getAlarmInfo",{},{"out":{"sysSts":0}})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,'VehModMngtGlbSafe1UsgModSts', 2)#不闭锁保持2convenie
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 20.0)
        self.dk.set_cenlock_sts(1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)#保持关闭
        self.partner.empty_all(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        self.five_door_open()
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{"seatStsSecondLeft":{"installSts":False,"occupySts":False},
                                                    "seatStsSecondRight":{"installSts":False,"occupySts":False}}})
        self.five_door_close()
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.dk.send_nfc_cmd()
        sleep(3)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 11)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)#晚点校验闭锁设防
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},{"out":{"modeSts":0,"reason":1}})
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
        self.bgm_eth_inter.ck_signal_values("MobDevCenLockReq", [2,0])  
        
    @allure.title("设置Convenience模式_2S计时器超时后的处理") 
    @pytest.mark.full
    def test_caseid_1983937(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(3)
        self.io.driver_seat_notpresent()
        self.seat_belt_status(1,1,1,1,1)#等新版本后将此次设置为已系
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.partner.empty_all(1)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT,"SetConvenienceForAppAction",{"time": 1})
        sleep(2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 1)
        self.sd_tester.enter_default_session()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT,"SetConvenienceForAppAction",{"time": 1})
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetUsageModeUp", {"mode": 2})
        sleep(60)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetUsageModeUp", {"mode": 1})

    @allure.title("设置Convenience模式_正常情况遍历") 
    @pytest.mark.full
    def test_caseid_1983938(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(3)
        self.io.driver_seat_notpresent()
        self.seat_belt_status(1,1,1,1,1)#等新版本后将此次设置为已系
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.set_four_seat_occupt(1,1,1,1)
        self.partner.empty_all(1)
        self.sd_tester.enter_default_session()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT,"SetConvenienceForAppAction",{"time": 3})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        sleep(150)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        sleep(28)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        sleep(4)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 1)
        
    @allure.title("设置Convenience模式_2S内连续调用后的处理") 
    @pytest.mark.full
    def test_caseid_1983969(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(3)
        self.io.driver_seat_notpresent()
        self.seat_belt_status(1,1,1,1,1)#等新版本后将此次设置为已系
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.set_four_seat_occupt(0,0,0,0)
        self.partner.empty_all(1)
        self.sd_tester.enter_default_session()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT,"SetConvenienceForAppAction",{"time": 2})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT,"SetConvenienceForAppAction",{"time": 1})
        sleep(50)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        sleep(12)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 1)
        
    @allure.title("设置Convenience模式_使用者模式改变导致的计时器结束") 
    @pytest.mark.full
    def test_caseid_1983955(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(3)
        self.io.driver_seat_notpresent()
        self.seat_belt_status(0,0,0,0,0)#等新版本后将此次设置为已系
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.set_four_seat_occupt(0,0,0,0)
        self.partner.empty_all(1)
        self.sd_tester.enter_default_session()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT,"SetConvenienceForAppAction",{"time": 1})
        sleep(50)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": 1})#下切使用者模式
        sleep(12)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 1)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT,"SetConvenienceForAppAction",{"time": 1})
        sleep(50)
        self.sd_tester.change_usage_mode(13) #上切使用者模式为13
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                               'VehModMngtGlbSafe1UsgModSts', 13)
        sleep(12)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                               'VehModMngtGlbSafe1UsgModSts', 13)
        
    @allure.title("设置Convenience模式_四门解锁且主踩刹车导致的计时器结束") 
    @pytest.mark.full
    def test_caseid_1983952(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(3)
        self.io.driver_seat_notpresent()
        self.seat_belt_status(1,1,1,1,1)#等新版本后将此次设置为已系
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                        {"firstLeftExist":False,"firstRightExist":False,"errorCode":0}})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.set_four_seat_occupt(0,0,0,0)
        self.partner.empty_all(1)
        self.sd_tester.enter_default_session()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,'VehModMngtGlbSafe1UsgModSts', 1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT,"SetConvenienceForAppAction",{"time": 1})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,'VehModMngtGlbSafe1UsgModSts', 2)
        sleep(50)
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1) #解锁踩刹车
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        sleep(12)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,'VehModMngtGlbSafe1UsgModSts', 2)
        self.sd_tester.change_usage_mode(1)
        self.dk.set_cenlock_sts(3)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,'VehModMngtGlbSafe1UsgModSts', 1)
        sleep(1)
        self.sd_tester.enter_default_session()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT,"SetConvenienceForAppAction",{"time": 1})
        sleep(2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 2)
        sleep(48)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 2)
        self.dk.set_cenlock_sts(1)#仅解锁不打断计时器
        sleep(12)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,'VehModMngtGlbSafe1UsgModSts', 1)
        
    @allure.title("设置Convenience模式_四门解锁且主驾座椅占位导致的计时器结束") 
    @pytest.mark.full
    def test_caseid_1984143(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(3)
        self.io.driver_seat_notpresent()
        self.seat_belt_status(1,1,1,1,1)#等新版本后将此次设置为已系
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.set_four_seat_occupt(0,0,0,0)
        self.partner.empty_all(1)
        self.sd_tester.enter_default_session()
        sleep(2)
        self.dk.set_cenlock_sts(3)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT,"SetConvenienceForAppAction",{"time": 1})
        sleep(0.1)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        sleep(50)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        self.dk.set_cenlock_sts(1) #仅解锁
        sleep(12)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 1)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT,"SetConvenienceForAppAction",{"time": 1})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        sleep(50)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1) #仅踩刹车
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0) #恢复刹车
        sleep(9)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 1)
        
    @allure.title("设置Convenience模式_座椅占位以及单个条件导致的计时器结束") 
    @pytest.mark.full
    def test_caseid_1983951(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(3)
        self.io.driver_seat_notpresent()
        self.seat_belt_status(1,1,1,1,1)#等新版本后将此次设置为已系
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.set_four_seat_occupt(0,0,0,0)
        self.partner.empty_all(1)
        self.sd_tester.enter_default_session()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT,"SetConvenienceForAppAction",{"time": 1})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        sleep(50)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        self.dk.set_cenlock_sts(1)
        self.io.driver_seat_present()#主驾占位
        sleep(12)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        self.io.driver_seat_notpresent()#主驾不占位

    @allure.title("设置Convenience模式_四门解锁且其余四座占位导致的计时器结束") 
    @pytest.mark.full
    def test_caseid_1984664(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(3)
        self.io.driver_seat_notpresent()
        self.seat_belt_status(1,1,1,1,1)#等新版本后将此次设置为已系
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.set_four_seat_occupt(0,0,0,0)
        self.partner.empty_all(1)
        self.sd_tester.enter_default_session()
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 1)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        sleep(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT,"SetConvenienceForAppAction",{"time": 1})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        sleep(50)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        self.dk.set_cenlock_sts(1)
        self.set_four_seat_occupt(1,1,1,1)#其余四座占位
        sleep(12)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 1)
        
    @allure.title("设置Convenience模式_四门解锁且任意门打开引起的计时器结束导致的不能下切") 
    @pytest.mark.full
    def test_caseid_1983940(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(3)
        self.io.driver_seat_notpresent()
        self.seat_belt_status(1,1,1,1,1)#等新版本后将此次设置为已系
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.set_four_seat_occupt(1,1,1,1)
        self.partner.empty_all(1)
        self.sd_tester.enter_default_session()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT,"SetConvenienceForAppAction",{"time": 1})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        sleep(50)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        self.dk.set_cenlock_sts(1)
        self.io.drvr_door_open() #主驾门打开
        sleep(7)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        self.partner.empty_all(2)
        self.io.drvr_door_close() #主驾门关闭

    @allure.title("设置Convenience模式_四门解锁且其余副驾门打开引起的计时器结束导致的不能下切") 
    @pytest.mark.full
    def test_caseid_1984665(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(3)
        self.io.driver_seat_notpresent()
        self.seat_belt_status(1,1,1,1,1)#等新版本后将此次设置为已系
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.set_four_seat_occupt(1,1,1,1)
        self.partner.empty_all(1)
        self.sd_tester.enter_default_session()        
        self.dk.set_cenlock_sts(3)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT,"SetConvenienceForAppAction",{"time": 1})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        sleep(50)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        self.dk.set_cenlock_sts(1)
        self.io.pass_door_open() #副驾门打开
        sleep(12)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        self.io.pass_door_close() #副驾门关闭

    @allure.title("设置Convenience模式_五门打开前提条件不满足不能调用") 
    @pytest.mark.full
    def test_caseid_1984155(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(3)
        self.io.driver_seat_notpresent()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetOccupiedValidity",
                                                {"seats": [0]},{"out": [{"value": {"seatId": 0, "status": 0}},
                                                    ]})
        self.seat_belt_status(1,1,1,1,1)#等新版本后将此次设置为已系
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        sleep(1)
        self.partner.empty_all(1)
        self.dk.set_cenlock_sts(1)
        self.sd_tester.enter_default_session()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT,"SetConvenienceForAppAction",{"time": 1})
        
        sleep(2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        self.five_door_open() #五门打开
        sleep(5)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                    'VehModMngtGlbSafe1UsgModSts', 2)
        sleep(57)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                    'VehModMngtGlbSafe1UsgModSts', 2)
    
    @allure.title("设置Convenience模式_解锁踩刹车条件下不能调用") 
    @pytest.mark.full
    def test_caseid_1984156(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(3)
        self.io.driver_seat_notpresent()
        self.seat_belt_status(1,1,1,1,1)#等新版本后将此次设置为已系
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.partner.empty_all(1)
        self.dk.set_cenlock_sts(1)
        self.sd_tester.enter_default_session()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT,"SetConvenienceForAppAction",{"time": 1})
        sleep(2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                    'VehModMngtGlbSafe1UsgModSts', 2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        sleep(5)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                    'VehModMngtGlbSafe1UsgModSts', 2)
        sleep(57)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                    'VehModMngtGlbSafe1UsgModSts', 2)

    @allure.title("设置Convenience模式_占位条件不满足不能调用") 
    @pytest.mark.full
    def test_caseid_1983936(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(3)
        self.io.driver_seat_notpresent()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetOccupiedValidity",
                                                {"seats": [0]},{"out": [{"value": {"seatId": 0, "status": 0}},
                                                    ]})
        self.seat_belt_status(1,1,1,1,1)#等新版本后将此次设置为已系
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        sleep(1)
        self.partner.empty_all(1)
        for usagemode in [0,2,11,13]:
            self.sd_tester.change_usage_mode(usagemode)
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT,"SetConvenienceForAppAction",{"time": 1})
            sleep(5)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', usagemode)
            sleep(58)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', usagemode)
        self.sd_tester.change_usage_mode(1)
        self.dk.set_cenlock_sts(1)
        self.partner.send_request_and_ck_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyId", {},
                                              {"out": [{"trigger": 3}]})
        self.sd_tester.enter_default_session()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT,"SetConvenienceForAppAction",{"time": 1})
        sleep(2)
        self.io.driver_seat_present() #主驾占位
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetOccupiedValidity",
                                                {"seats": [0]},{"out": [{"value": {"seatId": 0, "status": 1}},
                                                    ]})
        sleep(5)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                    'VehModMngtGlbSafe1UsgModSts', 2)
        sleep(57)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                    'VehModMngtGlbSafe1UsgModSts', 2)
        
    @allure.title("遍历_获取和通知维持上电模式状态_计时器内来回切换")
    @pytest.mark.sanity
    def test_caseid_1984266(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.sd_tester.change_usage_mode(2)
        self.five_door_open()
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(0,0,0,0,0)
        self.set_gear_P_speed_0()
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        sleep(1)
        #2s内无条件变化
        for i in range(10):
            logger.info(f"第{i}次压测")
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
            sleep(0.2)
            self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",{"sts":{"modeSts":1,"reason":0}})
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
            self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",{"sts":{"modeSts":0,"reason":1}})

    @allure.title("VehicleSetStatusService重启上电默认值")
    @pytest.mark.full
    def test_caseid_1984585(self):
        #2s内无条件变化
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.sd_tester.change_usage_mode(1)
        self.five_door_open()
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(0,0,0,0,0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 0.0)
        self.set_gear_P_speed_0()
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetMaintenanceMode", {"isOn": False})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": False})

        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT, "NotifyMaintenanceMode", {"mode": False})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT, "NotifyWashModeSts", {"sts": False})
        #当前为默认状态,重启后不会发送通知,且不影响功能
        # self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",{"sts":{"modeSts":0,"reason":0}})

    @allure.title("遍历_获取和通知维持上电模式状态_客户主动关闭")
    @pytest.mark.sanity
    def test_caseid_1983203(self):
        #2s内无条件变化
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.sd_tester.change_usage_mode(2)
        self.five_door_open()
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(0,0,0,0,0)
        self.set_gear_P_speed_0()
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        sleep(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",{"sts":{"modeSts":1,"reason":0}})
        sleep(3)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",{"sts":{"modeSts":0,"reason":1}})
        sleep(2)
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},{"out":{"modeSts":0,"reason":1}})
        sleep(3)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        sleep(3)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})#主动掉关
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",{"sts":{"modeSts":0,"reason":1}})
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 19.0)
        sleep(2)
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},{"out":{"modeSts":0,"reason":1}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT,"getAlarmInfo",{},{"out":{"sysSts":0}})
        
    @allure.title("通过服务使信号PrkgCmftModTiCtrl=0时reason=6")
    @pytest.mark.sanity
    def test_caseid_1985788(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.sd_tester.change_usage_mode(2)
        #车辆模式不为normal时，不能闭锁设防
        self.five_door_close()
        self.dk.set_cenlock_sts(0x1)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(0,0,0,0,0)
        self.set_gear_P_speed_0()
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        sleep(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.empty_all(3)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetConvenienceModeDuration",
                                                 {"duration": 0})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",{"sts":{"modeSts":0,"reason":6}},timeout=1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        
    @allure.title("通过服务使信号PrkgCmftModTiCtrl=非255和0时不能打开")
    @pytest.mark.smoke
    def test_caseid_1986265(self):
        info = random.randint(1, 255)
        info1 =random.randint(1, 255)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.sd_tester.change_usage_mode(2)
        #车辆模式不为normal时，不能闭锁设防
        self.five_door_close()
        self.dk.set_cenlock_sts(0x1)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(0,0,0,0,0)
        self.set_gear_P_speed_0()
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        sleep(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp",
                                         {"cmd":{"modeSts": 0,"source":"PetMode"}})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        self.partner.empty_all(3)
        logger.info(f"请求入参为{info}")
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetConvenienceModeDuration",
                                                 {"duration": info})
        self.partner.ck_no_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts")
        self.partner.ck_no_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortBaseFunctionSts")
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',info)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        sleep(1) #开启后改变值，不影响维持上电关闭
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        self.partner.empty_all()
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetConvenienceModeDuration",
                                                 {"duration": info1})
        self.partner.ck_no_specific_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",{"sts":{"modeSts":0}})
        self.partner.ck_no_specific_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortBaseFunctionSts",{"sts":{"modeSts":0}})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',info1)
        
    @allure.title("信号PrkgCmftModTiCtrl=255时只能开启维持上电")
    @pytest.mark.sanity
    def test_caseid_1985778(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.sd_tester.change_usage_mode(2)
        #车辆模式不为normal时，不能闭锁设防
        self.five_door_close()
        self.dk.set_cenlock_sts(0x1)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(0,0,0,0,0)
        self.set_gear_P_speed_0()
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        sleep(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        self.partner.empty_all(3)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp",
                                         {"cmd":{"modeSts": 1,"source":"PetMode"}})
        sleep(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp",
                                         {"cmd":{"modeSts": 0,"source":"PetMode"}})
        self.partner.empty_all(3)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetConvenienceModeDuration",
                                                 {"duration": 255})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",{"sts":{"modeSts":1,"reason":0}})
        self.partner.ck_no_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortBaseFunctionSts",timeout=5)
        
    @allure.title("维持上电打开情况下打开宠物模式的现象")
    @pytest.mark.sanity
    def test_caseid_1985961(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.sd_tester.change_usage_mode(2)
        #车辆模式不为normal时，不能闭锁设防
        self.five_door_close()
        self.dk.set_cenlock_sts(0x1)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(0,0,0,0,0)
        self.set_gear_P_speed_0()
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 20.0)
        self.partner.empty_all(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp",
                                         {"cmd":{"modeSts": 0,"source":"PetMode"}})
        self.partner.empty_all(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",{"sts":{"modeSts":1,"reason":0}})
        self.partner.empty_all(3)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp",
                                         {"cmd":{"modeSts": 1,"source":"PetMode"}})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        self.partner.ck_no_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortBaseFunctionSts")
        
    @allure.title("宠物模式打开情况下开启维持上电")
    @pytest.mark.sanity
    def test_caseid_1985865(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.sd_tester.change_usage_mode(2)
        #车辆模式不为normal时，不能闭锁设防
        self.five_door_close()
        self.dk.set_cenlock_sts(0x1)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(0,0,0,0,0)
        self.set_gear_P_speed_0()
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 20.0)
        self.partner.empty_all(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp",
                                         {"cmd":{"modeSts": 1,"source":"PetMode"}})
        self.partner.empty_all(3)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",{"sts":{"modeSts":1,"reason":0}})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortBaseFunctionSts",{"sts":{"modeSts":0,"reason":6}})

    @allure.title("设置维修模式_开")
    @pytest.mark.sanity
    def test_caseid_105611(self):
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetMaintenanceMode", {"isOn": False})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetMaintenanceMode", {"isOn": True})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT, "NotifyMaintenanceMode", {"mode": True})
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetMaintenanceMode", {}, {"out": True})

    @allure.title("设置维修模式_关")
    @pytest.mark.sanity
    def test_caseid_105617(self):
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetMaintenanceMode", {"isOn": True})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetMaintenanceMode", {"isOn": False})

        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT, "NotifyMaintenanceMode", {"mode": False})
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetMaintenanceMode", {}, {"out": False})

    @allure.title("所有情况都能进去")
    @pytest.mark.sanity
    def test_caseid_1959999(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06', 3000)
        sleep(1)
        for X in [0,1,2,11,13]:
            self.sd_tester.change_usage_mode(X)
            sleep(1)
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True})
            sleep(1)
            self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": True})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": False})

    @allure.title("V1.3_D或R挡车速大于15kph，洗车模式应该退出")
    @pytest.mark.sanity
    def test_caseid_1959927(self):
        self.sd_tester.change_usage_mode(11)
        sleep(1)
        for X in [1,3]:
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True})
            sleep(1)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', X)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06', 3)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06', 3000)
            sleep(1)
            self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT, "NotifyWashModeSts", {"sts": False})
            self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False})
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06', 0)
            sleep(2)
            self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False})

    @allure.title("V1.3_P挡车速大于15kph,洗车模式不应该退出")
    @pytest.mark.full
    def test_caseid_1959926(self):
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 0)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT, "NotifyWashModeSts", {"sts": True})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06', 10.0)
        sleep(1)
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": True})

    @allure.title("V1.3_P档下_设置洗车模式_开关")
    @pytest.mark.full
    def test_caseid_1959925_1959924(self):
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 0)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT, "NotifyWashModeSts", {"sts": True})
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": True})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": False})
        sleep(1)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT, "NotifyWashModeSts", {"sts": False})
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False})
        
    @allure.title("100度电池_服务启动1min后_没有调用SetParkingComfortMode不能上报事件")
    @pytest.mark.full
    def test_caseid_1985698(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:1,966:0,962:0,966:0})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.set_four_seat_occupt(0,0,0,0) #其余四座不占位
        self.seat_belt_status(1,0,0,0,0)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        sleep(6)
        for sigin2 in [10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', sigin2)
            sleep(1) 
        self.partner.empty_all(2)
        outputEnergy1=self.partner.send_request_and_return_resp(HIGHVOLTAGE_SERVICE_CLIENT,
                                                                "GetPowerConsumptionInfo", {},timeout=2)["out"]['outputEnergy']
        logger.info(f"服务连接后6-10S内设置Eout={outputEnergy1}")
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        self.partner.ck_no_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",timeout=50)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 70.0)
        self.partner.ck_no_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",timeout=10)
        
    @allure.title("100度电池__调用SetParkingComfortMode失败不能上报事件")
    @pytest.mark.full
    def test_caseid_1985699(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:1,966:0,962:0,966:0})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.set_four_seat_occupt(0,0,0,0) #其余四座不占位
        self.seat_belt_status(1,0,0,0,0)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        sleep(6)
        for sigin2 in [10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', sigin2)
            sleep(1) 
        self.partner.empty_all(2)
        outputEnergy1=self.partner.send_request_and_return_resp(HIGHVOLTAGE_SERVICE_CLIENT,
                                                                "GetPowerConsumptionInfo", {},timeout=2)["out"]['outputEnergy']
        logger.info(f"服务连接后6-10S内设置Eout={outputEnergy1}")
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 19.0)
        sleep(1) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_no_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",timeout=5)
        
    @allure.title("100度电池_服务启动1min后_调用SetParkingComfortMode关闭时_显示上一次时长")
    @pytest.mark.full
    def test_caseid_1985700(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:1,966:0,962:0,966:0})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 27.41)
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.set_four_seat_occupt(0,0,0,0) #其余四座不占位
        self.seat_belt_status(1,0,0,0,0)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        sleep(6)
        for sigin2 in [100.0,200.0,30.0,40.0,110.0,120.0,501.0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', sigin2)
            sleep(1) 
        self.partner.empty_all(2)
        outputEnergy1=self.partner.send_request_and_return_resp(HIGHVOLTAGE_SERVICE_CLIENT,
                                                                "GetPowerConsumptionInfo", {},timeout=2)["out"]['outputEnergy']
        logger.info(f"服务连接后6-10S内设置Eout={outputEnergy1}")
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":422,"displayLeftTime":2}})
        self.partner.empty_all(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":0,"reason":1,"leftTime":422,"displayLeftTime":2}})
        sleep(50)#服务连接66秒
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":422,"displayLeftTime":12}})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":0,"reason":1,"leftTime":422,"displayLeftTime":12}})
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},
                                              {"out":{"modeSts":0,"reason":1,"leftTime":422,"displayLeftTime":12}})
        
    @allure.title("100度电池_电量极限值导致leftTime=0_displayLeftTime赋值3")
    @pytest.mark.smoke
    def test_caseid_1985714(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:1,966:0,962:0,966:0})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 27.4)
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.set_four_seat_occupt(0,0,0,0) #其余四座不占位
        self.seat_belt_status(1,0,0,0,0)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        sleep(6)
        for sigin2 in [10.0,20.0,30.0,40.0,51.0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', sigin2)
            sleep(1) 
        self.partner.empty_all(2)
        outputEnergy1=self.partner.send_request_and_return_resp(HIGHVOLTAGE_SERVICE_CLIENT,
                                                                "GetPowerConsumptionInfo", {},timeout=2)["out"]['outputEnergy']
        logger.info(f"服务连接后6-10S内设置Eout={outputEnergy1}")
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":422,"displayLeftTime":2}})
        sleep(2)#15S时
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        sleep(40)#55S时
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 20.0)
        sleep(5)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 19.4)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":0,"reason":2,"leftTime":11,"displayLeftTime":3}},timeout=2) 
        
    @allure.title("100度电池_锁车自动关窗配置未打开时_维持上电_刷卡锁车")
    @pytest.mark.full
    def test_caseid_1985723(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 26)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 26)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 26)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 26)
        sleep(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 4, "value": 0}]})
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:1,966:0,962:0,966:0})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.set_four_seat_occupt(0,0,0,0) #其余四座不占位
        self.seat_belt_status(1,0,0,0,0)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        sleep(6)
        for sigin2 in [10.0,20.0,30.0,40.0,51.0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', sigin2)
            sleep(1) 
        self.partner.empty_all(3)
        outputEnergy1=self.partner.send_request_and_return_resp(HIGHVOLTAGE_SERVICE_CLIENT,
                                                                "GetPowerConsumptionInfo", {},timeout=2)["out"]['outputEnergy']
        logger.info(f"服务连接后6-10S内设置Eout={outputEnergy1}")
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":4251,"displayLeftTime":2}})
        sleep(2)#15S时
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(2)
        self.dk.send_nfc_cmd()
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('MirrOpenClsReq', [1, 1, 1, 0])
        self.bgm_eth_inter.ck_signal_values('DrvrAsscSysIndcrReq', [0,3,3, 0])
        self.bgm_eth_inter.ck_signal_values('WinOpenDrvrReq', [])
        self.bgm_eth_inter.ck_signal_values('WinOpenPassReq', [])
        self.bgm_eth_inter.ck_signal_values('WinOpenReLeReq', [])
        self.bgm_eth_inter.ck_signal_values('WinOpenReRiReq', [])
        self.dk.ck_cenlock_sts(3)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 11)
        sleep(30)#至少45S了
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":1417,"displayLeftTime":28}},timeout=31)
        
    @allure.title("100度电池_锁车自动关窗配置打开时_维持上电_刷卡锁车")
    @pytest.mark.smoke
    def test_caseid_1985722(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr', 26)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass', 26)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe', 26)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi', 26)
        sleep(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 4, "value": 1}]})
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:1,966:0,962:0,966:0})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.set_four_seat_occupt(0,0,0,0) #其余四座不占位
        self.seat_belt_status(1,0,0,0,0)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        sleep(6)
        for sigin2 in [10.0,20.0,30.0,40.0,51.0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', sigin2)
            sleep(1) 
        self.partner.empty_all(2)
        outputEnergy1=self.partner.send_request_and_return_resp(HIGHVOLTAGE_SERVICE_CLIENT,
                                                                "GetPowerConsumptionInfo", {},timeout=2)["out"]['outputEnergy']
        logger.info(f"服务连接后6-10S内设置Eout={outputEnergy1}")
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":4251,"displayLeftTime":2}})
        sleep(2)#15S时
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(2)
        self.dk.send_nfc_cmd()
        sleep(4) #这里停止太快，导致没有拿到数据0
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('MirrOpenClsReq', [1, 1, 1, 0])
        self.bgm_eth_inter.ck_signal_values('DrvrAsscSysIndcrReq', [0,3,3, 0])
        self.bgm_eth_inter.ck_signal_values('WinOpenDrvrReq', [0,1, 1, 1, 0,0,1, 1, 1, 0])
        self.bgm_eth_inter.ck_signal_values('WinOpenPassReq', [0,1, 1, 1, 0,0,1, 1, 1, 0])
        self.bgm_eth_inter.ck_signal_values('WinOpenReLeReq', [0,1, 1, 1, 0,0,1, 1, 1, 0])
        self.bgm_eth_inter.ck_signal_values('WinOpenReRiReq', [0,1, 1, 1, 0,0,1, 1, 1, 0])
        self.dk.ck_cenlock_sts(3)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 11)
        sleep(30)#至少45S了
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":1417,"displayLeftTime":28}},timeout=31)
        
    @allure.title("100度电池_服务启动1min内_displayLeftTime都是2_1min后跳变")
    @pytest.mark.full
    def test_caseid_1985715(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:1,966:0,962:0,966:0})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.set_four_seat_occupt(0,0,0,0) #其余四座不占位
        self.seat_belt_status(1,0,0,0,0)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        sleep(6)
        for sigin2 in [10.0,20.0,30.0,40.0,51.0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', sigin2)
            sleep(1) 
        self.partner.empty_all(2)
        outputEnergy1=self.partner.send_request_and_return_resp(HIGHVOLTAGE_SERVICE_CLIENT,
                                                                "GetPowerConsumptionInfo", {},timeout=2)["out"]['outputEnergy']
        logger.info(f"服务连接后6-10S内设置Eout={outputEnergy1}")
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":4251,"displayLeftTime":2}})
        sleep(2)#15S时
        sleep(40)#60时
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},
                                              {"out":{"modeSts":1,"reason":0,"leftTime":4251,"displayLeftTime":2}})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":1417,"displayLeftTime":28}},timeout=31)
        
    @allure.title("100度电池___剩余时长显示_电量小于19.4时的反应")
    @pytest.mark.full
    def test_caseid_1985838(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:1,966:0,962:0,966:0})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.set_four_seat_occupt(0,0,0,0) #其余四座不占位
        self.seat_belt_status(1,0,0,0,0)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        sleep(6)
        for sigin2 in [10.0,20.0,30.0,40.0,51.0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', sigin2)
            sleep(1) 
        self.partner.empty_all(2) #13S
        outputEnergy1=self.partner.send_request_and_return_resp(HIGHVOLTAGE_SERVICE_CLIENT,
                                                                "GetPowerConsumptionInfo", {},timeout=2)["out"]['outputEnergy']
        logger.info(f"服务连接后6-10S内设置Eout={outputEnergy1}")
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":4251,"displayLeftTime":2}})
        sleep(27)#40S时
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 0)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                        {"sts":{"modeSts":0,"reason":2,"leftTime":4251,"displayLeftTime":2}})
        sleep(22) #60秒
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        sleep(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                        {"sts":{"modeSts":1,"reason":0,"leftTime":0,"displayLeftTime":3}})
        
    @allure.title("100度电池___剩余时长显示_1min内调用打开_1min后随时调用随时显示时间")
    @pytest.mark.full
    def test_caseid_1985725(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:1,966:0,962:0,966:0})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.set_four_seat_occupt(0,0,0,0) #其余四座不占位
        self.seat_belt_status(1,0,0,0,0)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        sleep(6)
        for sigin2 in [10.0,20.0,30.0,40.0,51.0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', sigin2)
            sleep(1) 
        self.partner.empty_all(2)
        outputEnergy1=self.partner.send_request_and_return_resp(HIGHVOLTAGE_SERVICE_CLIENT,
                                                                "GetPowerConsumptionInfo", {},timeout=2)["out"]['outputEnergy']
        logger.info(f"服务连接后6-10S内设置Eout={outputEnergy1}")
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":4251,"displayLeftTime":2}})
        sleep(2)#15S时
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 90.4)
        sleep(5)#20时时获取到的是上一次的event
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},
                                              {"out":{"modeSts":1,"reason":0,"leftTime":4251,"displayLeftTime":2}})#9S后进行第一个计算
        sleep(35)#55时 应该时电量=90.4的值3692
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},
                                              {"out":{"modeSts":1,"reason":0,"leftTime":3745,"displayLeftTime":2}})
        sleep(1) #56S时调用关闭,防止卡在60s先走计算逻辑了
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":0,"reason":1,"leftTime":3745,"displayLeftTime":2}})
        self.partner.empty_all()
        self.partner.ck_no_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",timeout=5)
        sleep(5) #大于1min调用打开
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":1248,"displayLeftTime":25}})
        
    @allure.title("100度电池__剩余时长显示_1min内调用打开_1min后必须跳转至正常时间")
    @pytest.mark.smoke
    def test_caseid_1985724(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:1,966:0,962:0,966:0})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.set_four_seat_occupt(0,0,0,0) #其余四座不占位
        self.seat_belt_status(1,0,0,0,0)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        sleep(6)
        for sigin2 in [10.0,20.0,30.0,40.0,51.0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', sigin2)
            sleep(1) 
        self.partner.empty_all(2)
        outputEnergy1=self.partner.send_request_and_return_resp(HIGHVOLTAGE_SERVICE_CLIENT,
                                                                "GetPowerConsumptionInfo", {},timeout=2)["out"]['outputEnergy']
        logger.info(f"服务连接后6-10S内设置Eout={outputEnergy1}")
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":4251,"displayLeftTime":2}})
        sleep(2)#15S时
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 90.4)
        sleep(5)#20时时获取到的是上一次的event
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},
                                              {"out":{"modeSts":1,"reason":0,"leftTime":4251,"displayLeftTime":2}})
        sleep(35)#55时 应该时电量=90.4的值3692
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},
                                              {"out":{"modeSts":1,"reason":0,"leftTime":3745,"displayLeftTime":2}})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":1248,"displayLeftTime":25}},timeout=10)
        
    @allure.title("100度电池__剩余时长显示__1min后表显示6h且卡10min上升")
    @pytest.mark.full
    def test_caseid_1986129(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:1,966:0,962:0,966:0})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 61.4)
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.set_four_seat_occupt(0,0,0,0) #其余四座不占位
        self.seat_belt_status(1,0,0,0,0)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 0,"source":"PetMode"}})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0) #E最初为1或0
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        sleep(6) #服务连接6s后
        for sigin2 in [10.0,20.0,30.0,40.0,101.0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', sigin2)
            sleep(1) 
        self.partner.empty_all(2)
        outputEnergy1=self.partner.send_request_and_return_resp(HIGHVOLTAGE_SERVICE_CLIENT,
                                                                "GetPowerConsumptionInfo", {},timeout=2)["out"]['outputEnergy']
        logger.info(f"服务连接后13S内设置Eout={outputEnergy1}") #   E30S=51
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        sleep(2)#服务连接15S时
        sleep(46)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":369,"displayLeftTime":11}}) #理论上60的时候准确拿到
        sleep(25)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 62.5)
        sleep(6)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":379,"displayLeftTime":11}}) #理论上60的时候准确拿到
        
    @allure.title("100度电池__剩余时长显示__P取最小值300w")
    @pytest.mark.full
    def test_caseid_1986131(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:1,966:0,962:0,966:0})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.set_four_seat_occupt(0,0,0,0) #其余四座不占位
        self.seat_belt_status(1,0,0,0,0)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 0,"source":"PetMode"}})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0) #E最初为1或0
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        sleep(6) #服务连接6s后
        for sigin2 in [5.0,6.0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', sigin2)
            sleep(1) 
        self.partner.empty_all(2)
        outputEnergy1=self.partner.send_request_and_return_resp(HIGHVOLTAGE_SERVICE_CLIENT,
                                                                "GetPowerConsumptionInfo", {},timeout=2)["out"]['outputEnergy']
        logger.info(f"服务连接后13S内设置Eout={outputEnergy1}") #   E30S=51
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        sleep(2)#服务连接15S时
        sleep(46)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":14171,"displayLeftTime":29}}) #理论上60的时候准确拿到
        
    @allure.title("100度电池__剩余时长显示__1min后表显=30min且直线上升到6h")
    @pytest.mark.full
    def test_caseid_1986130(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:1,966:0,962:0,966:0})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 23.8)
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.set_four_seat_occupt(0,0,0,0) #其余四座不占位
        self.seat_belt_status(1,0,0,0,0)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 0,"source":"PetMode"}})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0) #E最初为1或0
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        sleep(6) #服务连接6s后
        for sigin2 in [10.0,20.0,30.0,40.0,101.0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', sigin2)
            sleep(1) 
        self.partner.empty_all(2)
        outputEnergy1=self.partner.send_request_and_return_resp(HIGHVOLTAGE_SERVICE_CLIENT,
                                                                "GetPowerConsumptionInfo", {},timeout=2)["out"]['outputEnergy']
        logger.info(f"服务连接后13S内设置Eout={outputEnergy1}") #   E30S=51
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        sleep(2)#服务连接15S时
        sleep(46)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":39,"displayLeftTime":5}}) #理论上60的时候准确拿到
        sleep(25)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 61.4)
        sleep(6)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":369,"displayLeftTime":11}}) #理论上90的时候准确拿到
        
    @allure.title("100度电池__剩余时长显示__1min后卡上升条件20min")
    @pytest.mark.full
    def test_caseid_1986128(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:1,966:0,962:0,966:0})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.set_four_seat_occupt(0,0,0,0) #其余四座不占位
        self.seat_belt_status(1,0,0,0,0)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 0,"source":"PetMode"}})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0) #E最初为1或0
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        sleep(6) #服务连接6s后
        for sigin2 in [10.0,20.0,30.0,40.0,101.0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', sigin2)
            sleep(1) 
        self.partner.empty_all(2)
        outputEnergy1=self.partner.send_request_and_return_resp(HIGHVOLTAGE_SERVICE_CLIENT,
                                                                "GetPowerConsumptionInfo", {},timeout=2)["out"]['outputEnergy']
        logger.info(f"服务连接后13S内设置Eout={outputEnergy1}") #   E30S=51
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":4251,"displayLeftTime":2}})
        sleep(2)#服务连接15S时
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 70.4)
        sleep(40)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":448,"displayLeftTime":12}},timeout=6) #理论上60S的时候准确拿到
        sleep(25)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 77.3)
        sleep(6)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":509,"displayLeftTime":13}}) #理论上120S的时候准确拿到
        
    @allure.title("100度电池__剩余时长显示_30s到120内E变化_1min后卡下降条件30min")
    @pytest.mark.full
    def test_caseid_1986125(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:1,966:0,962:0,966:0})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.set_four_seat_occupt(0,0,0,0) #其余四座不占位
        self.seat_belt_status(1,0,0,0,0)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 0,"source":"PetMode"}})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0) #E最初为1或0
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        sleep(6) #服务连接6s后
        for sigin2 in [10.0,20.0,30.0,40.0,51.0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', sigin2)
            sleep(1) 
        self.partner.empty_all(2)
        outputEnergy1=self.partner.send_request_and_return_resp(HIGHVOLTAGE_SERVICE_CLIENT,
                                                                "GetPowerConsumptionInfo", {},timeout=2)["out"]['outputEnergy']
        logger.info(f"服务连接后13S内设置Eout={outputEnergy1}") #   E30S=51
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":4251,"displayLeftTime":2}})
        sleep(2)#服务连接15S时
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 70.4)
        sleep(5)#服务连接20时时获取到的是最初电量的event
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},
                                              {"out":{"modeSts":1,"reason":0,"leftTime":4251,"displayLeftTime":2}})
        sleep(15)#服务连接35时将E改变为101
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 101.0) #E60S=101
        sleep(20)#55时 应该时电量=70.4的值2637
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},
                                              {"out":{"modeSts":1,"reason":0,"leftTime":2690,"displayLeftTime":2}})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":448,"displayLeftTime":12}},timeout=6) #理论上60S的时候准确拿到
        # 以下为1min后的变化
        sleep(32)#服务连接90S后
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":897,"displayLeftTime":19}}) #理论上90s的时候准确拿到
        sleep(25)#服务连接115S后
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 66.44)
        sleep(6)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":826,"displayLeftTime":19}}) #下降条件810min
        
        
    @allure.title("100度电池_剩余时长显示_电量连续边界值向下跳变")
    @pytest.mark.full
    def test_caseid_1985729(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:1,966:0,962:0,966:0})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 86.4)
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.set_four_seat_occupt(0,0,0,0) #其余四座不占位
        self.seat_belt_status(1,0,0,0,0)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        sleep(7) #避免上电后Get不到数据
        for sigin2 in [10.0,41.0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', sigin2)
            sleep(1) 
        self.partner.empty_all(2)
        outputEnergy1=self.partner.send_request_and_return_resp(HIGHVOLTAGE_SERVICE_CLIENT,
                                                                "GetPowerConsumptionInfo", {},timeout=2)["out"]['outputEnergy']
        logger.info(f"服务连接后6-10S内设置Eout=60*{outputEnergy1}=2400")
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":3534,"displayLeftTime":2}})
        sleep(2)#15S时
        sleep(45)#60S时
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":1473,"displayLeftTime":29}},timeout=10) #65S时
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 84.5)
        sleep(25)#90S时上报24
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":1431,"displayLeftTime":29}},timeout=10) #95S时
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 53.2)
        sleep(25)#120S时上报12
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":743,"displayLeftTime":17}},timeout=10) #125S时
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 36.8)
        sleep(25)#150S时上报6
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":382,"displayLeftTime":11}},timeout=10) #155S时
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 23.1)
        sleep(25)#180S时上报1
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":81,"displayLeftTime":6}},timeout=10) #185S时
        
    @allure.title("100度电池_剩余时长显示_电量连续边界值向上跳变")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1985732(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:1,966:0,962:0,966:0})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 23.1)
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.set_four_seat_occupt(0,0,0,0) #其余四座不占位
        self.seat_belt_status(1,0,0,0,0)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        sleep(7)
        for sigin2 in [10.0,41.0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', sigin2)
            sleep(1) 
        self.partner.empty_all(2)
        outputEnergy1=self.partner.send_request_and_return_resp(HIGHVOLTAGE_SERVICE_CLIENT,
                                                                "GetPowerConsumptionInfo", {},timeout=2)["out"]['outputEnergy']
        logger.info(f"服务连接后6-10S内设置Eout=60*{outputEnergy1}=2400")
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":195,"displayLeftTime":2}})
        sleep(2)#15S时
        sleep(45)#60S时
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":81,"displayLeftTime":6}},timeout=10) #65S时
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 36.8)
        sleep(25)#90S时上报24
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":382,"displayLeftTime":11}},timeout=10) #95S时
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 53.2)
        sleep(25)#120S时上报12
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":743,"displayLeftTime":17}},timeout=10) #125S时
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 84.5)
        sleep(25)#150S时上报6
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":1431,"displayLeftTime":28}},timeout=10) #155S时
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 87.3)
        sleep(25)#180S时上报1
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":1492,"displayLeftTime":29}},timeout=10) #185S时
        
    @allure.title("100度电池_剩余时长显示_电量不满足时应立即退出")
    @pytest.mark.full
    def test_caseid_1985741(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:1,966:0,962:0,966:0})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 23.1)
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.set_four_seat_occupt(0,0,0,0) #其余四座不占位
        self.seat_belt_status(1,0,0,0,0)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        sleep(6)
        for sigin2 in [10.0,41.0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', sigin2)
            sleep(1) 
        self.partner.empty_all(2)
        outputEnergy1=self.partner.send_request_and_return_resp(HIGHVOLTAGE_SERVICE_CLIENT,
                                                                "GetPowerConsumptionInfo", {},timeout=2)["out"]['outputEnergy']
        logger.info(f"服务连接后6-10S内设置Eout=60*{outputEnergy1}=2400")
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":195,"displayLeftTime":2}})
        sleep(45)#55时
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":81,"displayLeftTime":6}},timeout=10) #65S时
        sleep(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 19.4)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":0,"reason":2,"leftTime":81,"displayLeftTime":6}},timeout=1) #65S时
        
    @allure.title("100度电池_剩余时长显示_其他条件不满足时应立即退出")
    @pytest.mark.full
    def test_caseid_1985765(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:1,966:0,962:0,966:0})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 23.1)
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.set_four_seat_occupt(0,0,0,0) #其余四座不占位
        self.seat_belt_status(1,0,0,0,0)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        sleep(6)
        for sigin2 in [10.0,41.0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', sigin2)
            sleep(1) 
        self.partner.empty_all(2)
        outputEnergy1=self.partner.send_request_and_return_resp(HIGHVOLTAGE_SERVICE_CLIENT,
                                                                "GetPowerConsumptionInfo", {},timeout=2)["out"]['outputEnergy']
        logger.info(f"服务连接后6-10S内设置Eout=60*{outputEnergy1}=2400")
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":195,"displayLeftTime":2}})
        sleep(2)#15S时
        sleep(45)#60S时
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":81,"displayLeftTime":6}},timeout=10) #65S时
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)
        self.partner.empty_all(8)
        self.partner.ck_no_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts")
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":0,"reason":6,"leftTime":81,"displayLeftTime":6}},timeout=3) #65S时
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        
    @allure.title("100度电池_剩余时长显示_3min内的显示变化")
    @pytest.mark.full
    def test_caseid_1985728(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:1,966:0,962:0,966:0})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.set_four_seat_occupt(0,0,0,0) #其余四座不占位
        self.seat_belt_status(1,0,0,0,0)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        sleep(6)
        for sigin2 in [10.0,20.0,30.0,40.0,51.0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', sigin2)
            sleep(1) 
        self.partner.empty_all(2)
        outputEnergy1=self.partner.send_request_and_return_resp(HIGHVOLTAGE_SERVICE_CLIENT,
                                                                "GetPowerConsumptionInfo", {},timeout=2)["out"]['outputEnergy']
        logger.info(f"服务连接后6-10S内设置Eout={outputEnergy1}")
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":4251,"displayLeftTime":2}})
        sleep(2)#15S时
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 90.4)
        sleep(5)#20时时获取到的是上一次的event
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},
                                              {"out":{"modeSts":1,"reason":0,"leftTime":4251,"displayLeftTime":2}})
        sleep(35)#55时 应该时电量=90.4的值3692
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},
                                              {"out":{"modeSts":1,"reason":0,"leftTime":3745,"displayLeftTime":2}})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":1248,"displayLeftTime":25}},timeout=10) #65S拿到
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 110.1) #增量为60
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 50.4)
        sleep(55) #120时
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":462,"displayLeftTime":12}},timeout=10) #125S拿到
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 22.4)
        sleep(55) #180时
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":45,"displayLeftTime":5}},timeout=10) #185S拿到
        
        
    @allure.title("100度电池___剩余时长显示_来回充电，需要正确显示")
    @pytest.mark.full
    def test_caseid_1985726(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:1,966:0,962:0,966:0})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.set_four_seat_occupt(0,0,0,0) #其余四座不占位
        self.seat_belt_status(1,0,0,0,0)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        sleep(6)
        for sigin2 in [10.0,20.0,30.0,40.0,51.0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', sigin2)
            sleep(1) 
        self.partner.empty_all(2)
        outputEnergy1=self.partner.send_request_and_return_resp(HIGHVOLTAGE_SERVICE_CLIENT,
                                                                "GetPowerConsumptionInfo", {},timeout=2)["out"]['outputEnergy']
        logger.info(f"服务连接后6-10S内设置Eout={outputEnergy1}")
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15) 
        sleep(1)
        self.partner.ck_no_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts")
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":4251,"displayLeftTime":1}})
        sleep(2)#15S时
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 90.4)
        sleep(5)#20时时获取到的是上一次的event
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},
                                              {"out":{"modeSts":1,"reason":0,"leftTime":4251,"displayLeftTime":1}})
        sleep(35)#55时 应该时电量=90.4的值3692
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},
                                              {"out":{"modeSts":1,"reason":0,"leftTime":3745,"displayLeftTime":1}})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":1248,"displayLeftTime":1}},timeout=10)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":1248,"displayLeftTime":25}},timeout=1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15) 
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":1248,"displayLeftTime":1}},timeout=1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":1248,"displayLeftTime":25}},timeout=1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":0,"reason":1,"leftTime":1248,"displayLeftTime":25}},timeout=1)
        

    @allure.title("100度电池_服务启动2min后_调用SetParkingComfortMode关闭时_使用上次的P")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1985709(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950:1,966:0,962:0,966:0})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 27.4)
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.set_four_seat_occupt(0,0,0,0) #其余四座不占位
        self.seat_belt_status(1,0,0,0,0)
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', 1.0)
        sleep(6)
        for sigin2 in [10.0,20.0,30.0,40.0,51.0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr16, 'DispBattEgyOut', sigin2)
            sleep(1) 
        self.partner.empty_all(2)
        outputEnergy1=self.partner.send_request_and_return_resp(HIGHVOLTAGE_SERVICE_CLIENT,
                                                                "GetPowerConsumptionInfo", {},timeout=2)["out"]['outputEnergy']
        logger.info(f"服务连接后6-10S内设置Eout={outputEnergy1}")
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":422,"displayLeftTime":2}})
        self.partner.empty_all(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":0,"reason":1,"leftTime":422,"displayLeftTime":2}})
        sleep(50)#服务连接66秒
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":141,"displayLeftTime":7}})
        sleep(60)#服务连接126秒 P保持lastValue=500
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 22.4)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",
                                  {"sts":{"modeSts":1,"reason":0,"leftTime":53,"displayLeftTime":5}},timeout=32)
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},
                                              {"out":{"modeSts":1,"reason":0,"leftTime":53,"displayLeftTime":5}})

    @allure.title("V1.3_车辆模式不为normal或者使用者模式为abonded，洗车模式应该退出")
    @pytest.mark.full
    def test_caseid_1959928(self):
        def info(X):
            return False if X == 0 else True
        def result(Y):
            return True if Y == 0 else False
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 0)
        sleep(1)
        for X1 in [0,2,11,13,1]:
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True})
            sleep(1)
            self.sd_tester.change_usage_mode(X1)
            sleep(1)
            self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": info(X1)})
        for Y1 in [1,2,3,5,0]:
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True})
            sleep(1)
            self.sd_tester.change_car_mode(Y1)
            sleep(1)
            self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": result(Y1)})

    @allure.title("设置维持上电模式_电池SOC不满足")
    @pytest.mark.smoke
    def test_caseid_1985165(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        self.Shift_Gear(0) #P档
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        #电量等于低于20%无法调用
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 20.0)
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        
    @allure.title("获取和通知维持上电模式状态_默认值")
    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_1980607(self):
        self.ipdu.pause_all_bus_send()
        self.nucapp.bgm_power_off()
        sleep(2)
        self.nucapp.bgm_power_on()
        sleep(20)
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},{"out":{"modeSts":0,"reason":0}})
        self.ipdu.resume_all_bus_send() 

    @allure.title("设置Convenience模式_默认值及入参0无限制") 
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_1983941(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(3)
        self.io.driver_seat_notpresent()
        self.seat_belt_status(1,1,1,1,1)#等新版本后将此次设置为已系
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.set_four_seat_occupt(1,1,1,1)
        self.partner.empty_all(1)
        self.sd_tester.enter_default_session()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT,"SetConvenienceForAppAction",{"time": 1})
        sleep(50)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        sleep(11)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 1)
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        sleep(1)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 1)

    @allure.title("设置维修模式_下电记忆")
    @pytest.mark.restart
    @pytest.mark.smoke
    def test_caseid_105615(self):
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetMaintenanceMode", {"isOn": False})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetMaintenanceMode", {"isOn": True})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT, "NotifyMaintenanceMode", {"mode": True})
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT, "NotifyMaintenanceMode", {"mode": True},timeout=3)
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetMaintenanceMode", {}, {"out": True})

    @allure.title("设置洗车模式_总线校验")
    @pytest.mark.full
    def test_caseid_1988800(self):
        for cmd in [True,False]:
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": cmd})
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr21, 'WashModeSts', int(cmd))

    @allure.title("设置洗车模式_下电不记忆")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1959998(self):
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True})
        self.ipdu.pause_all_bus_send()
        sleep(2)
        self.nucapp.bgm_power_off()
        sleep(2)
        self.nucapp.bgm_power_on()
        sleep(20)
        self.ipdu.resume_all_bus_send()
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False})  
    
    #宠物模式
    @allure.title("设置维持上电基础能力_遍历")
    @pytest.mark.sanity
    def test_caseid_1985126(self):
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},{"out":{"modeSts":0}})
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        #车辆模式不满足无法调用
        self.set_gear_P_speed_0()
        for carmode1 in [1,2,3,5]:
            logger.info(f"切换车辆模式为{carmode1}")
            self.sd_tester.change_car_mode(carmode1)
            sleep(0.5) #车辆模式不为narmal
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 1,"source":"PetMode"}})
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        self.sd_tester.change_car_mode(0)
        #正常设置打开或关闭
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        self.Shift_Gear(0) #P档
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 1,"source":"PetMode"}})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 0,"source":"PetMode"}})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        #档位条件不满足无法调用
        for gear in [1,2,3]:
            logger.info(f"切换档位为{gear}")
            self.Shift_Gear(gear)
            sleep(0.5) #车辆模式不为narmal
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 1,"source":"PetMode"}})
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        self.Shift_Gear(0)
        #电量低于20%无法调用
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 19.0)
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 1,"source":"PetMode"}})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        self.sd_tester.change_usage_mode(2)
        for carmode1 in [1,2,3,5]:
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
            sleep(1)
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 1,"source":"PetMode"}})
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
            self.Shift_Gear(0) #开启后，车辆模式不满足
            logger.info(f"切换车辆模式为{carmode1}")
            self.sd_tester.change_car_mode(carmode1)
            sleep(0.5) #车辆模式不为narmal
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
            self.sd_tester.change_car_mode(0)
            self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortBaseFunctionSts",{},{"out":
                                                        {"modeSts":0,"reason":4,"source":"PetMode"}})
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
            sleep(1)
             #开启后，电池SOC不满足
            self.partner.empty_all(0.5)
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 1,"source":"PetMode"}})
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 19.0)
            sleep(1)
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
            sleep(1)#恢复后继续不满足
            self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortBaseFunctionSts",{},{"out":
                                                        {"modeSts":0,"reason":2,"source":"PetMode"}})
        self.sd_tester.change_usage_mode(11)
        for gear in [1,2,3]:
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 1,"source":"PetMode"}})
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
            logger.info(f"切换档位为{gear}")
            self.Shift_Gear(gear)
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
            self.Shift_Gear(0)
            sleep(1)
            self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortBaseFunctionSts",{},{"out":
                                                        {"modeSts":0,"reason":3,"source":"PetMode"}})
        
    @allure.title("获取和通知维持上电基础能力_默认值")
    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_1985133(self):
        self.ipdu.pause_all_bus_send()
        self.nucapp.bgm_power_off()
        sleep(2)
        self.nucapp.bgm_power_on()
        sleep(20)
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortBaseFunctionSts",{},{"out":
                                                            {"modeSts":0,"reason":0,"source":"PetMode"}})
        self.ipdu.resume_all_bus_send() 
    
    @allure.title("遍历_获取和通知维持上电基础能力状态_客户主动关闭")
    @pytest.mark.sanity
    def test_caseid_1985134(self):
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},{"out":{"modeSts":0}})
        #2s内无条件变化
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.sd_tester.change_usage_mode(2)
        self.five_door_open()
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(0,0,0,0,0)
        self.set_gear_P_speed_0()
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        sleep(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 1,"source":"PetMode"}})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortBaseFunctionSts",{"sts":
                                                                            {"modeSts":1,"reason":0,"source":"PetMode"}})
        sleep(3)
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 0,"source":"PetMode"}})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortBaseFunctionSts",{"sts":
                                                                            {"modeSts":0,"reason":1,"source":"PetMode"}})
        sleep(2)
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortBaseFunctionSts",{},{"out":
                                                           {"modeSts":0,"reason":1,"source":"PetMode"}})
        sleep(3)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 1,"source":"PetMode"}})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        sleep(3)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 0,"source":"PetMode"}})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortBaseFunctionSts",{"sts":
                                                                           {"modeSts":0,"reason":1,"source":"PetMode"}})
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 19.0)
        sleep(2)
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortBaseFunctionSts",{},{"out":
                                                           {"modeSts":0,"reason":1,"source":"PetMode"}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT,"getAlarmInfo",{},{"out":{"sysSts":0}})
        
    @allure.title("遍历_获取和通知维持上电基础能力状态_计时器内来回切换")
    @pytest.mark.sanity
    def test_caseid_1985135(self):
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},{"out":{"modeSts":0}})
        #2s内无条件变化
        for i in range(10):
            logger.info(f"第{i}次压测")
            self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
            self.five_door_close()
            self.dk.set_cenlock_sts(1)
            self.sd_tester.change_usage_mode(2)
            self.five_door_open()
            self.io.driver_seat_notpresent()
            self.set_four_seat_occupt(0,0,0,0)
            self.seat_belt_status(0,0,0,0,0)
            self.set_gear_P_speed_0()
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
            sleep(1)
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 1,"source":"PetMode"}})
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
            self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortBaseFunctionSts",{"sts":
                                                                            {"modeSts":1,"reason":0,"source":"PetMode"}})
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 0,"source":"PetMode"}})
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
            self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortBaseFunctionSts",{"sts":
                                                                            {"modeSts":0,"reason":1,"source":"PetMode"}})
            
    @allure.title("设置维持上电模式_遍历")
    @pytest.mark.sanity
    def test_caseid_1980580(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        #车辆模式不满足无法调用
        for carmode1 in [1,2,3,5]:
            logger.info(f"切换车辆模式为{carmode1}")
            self.sd_tester.change_car_mode(carmode1)
            sleep(0.5) #车辆模式不为narmal
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        self.sd_tester.change_car_mode(0)
        #正常设置打开或关闭
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        self.Shift_Gear(0) #P档
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        #档位条件不满足无法调用
        for gear in [1,2,3]:
            logger.info(f"切换档位为{gear}")
            self.Shift_Gear(gear)
            sleep(0.5) #车辆模式不为narmal
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        self.Shift_Gear(0)
        #电量低于20%无法调用
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 19.0)
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        for carmode1 in [1,2,3,5]:
            self.sd_tester.change_usage_mode(2)
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
            sleep(1)
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
            self.Shift_Gear(0) #开启后，车辆模式不满足
            logger.info(f"切换车辆模式为{carmode1}")
            self.sd_tester.change_car_mode(carmode1)
            sleep(0.5) #车辆模式不为narmal
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
            self.sd_tester.change_car_mode(0)
            self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},{"out":{"modeSts":0,"reason":4}})
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
            sleep(1)
             #开启后，电池SOC不满足
            self.partner.empty_all(0.5)
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 19.0)
            sleep(1)
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
            sleep(1)#恢复后继续不满足
            self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},{"out":{"modeSts":0,"reason":2}})
        for gear in [1,2,3]:
            self.sd_tester.change_usage_mode(11)
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
            logger.info(f"切换档位为{gear}")
            self.Shift_Gear(gear)
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
            self.Shift_Gear(0)
            sleep(1)
            self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},{"out":{"modeSts":0,"reason":3}})
    
    @allure.title("维持上电模式状态打开时无法设置维持上电基础能力")
    @pytest.mark.smoke
    def test_caseid_1985137(self):
        #2s内无条件变化
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.sd_tester.change_usage_mode(2)
        self.five_door_open()
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(0,0,0,0,0)
        self.set_gear_P_speed_0()
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        sleep(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 0,"source":"PetMode"}})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        self.partner.empty_all(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 1,"source":"PetMode"}})
        self.partner.ck_no_event(VEHICLESETSTATUS_CLIENT, "ParkingComfortBaseFunctionSts")
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        self.partner.empty_all()
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 1,"source":"PetMode"}})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortBaseFunctionSts",{"sts":
                                                                            {"modeSts":1,"reason":0,"source":"PetMode"}})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        self.partner.empty_all()
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 0,"source":"PetMode"}})
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortBaseFunctionSts",{"sts":{"modeSts":0,"reason":1,"source":"PetMode"}})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        self.partner.ck_no_event(VEHICLESETSTATUS_CLIENT, "ParkingComfortMode")
        
    #12延迟上电   
    @allure.title("12V电源延时状态默认值")
    @pytest.mark.sanity
    def test_caseid_1984911(self):
        """删除s2s的数据库，一般用于测试默认配置"""
        self.bgmcli.type_commands("rm -f /data/SOAApp/SOAApp.db3", alias="1")
        self.bgmcli.type_commands("sync", alias="1")
        self.bgmcli.type_commands("ls -l /data/SOAApp", alias="1")
        sleep(0.5)
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        sleep(1)
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetPowerOutletDelayInfo", {}, 
                                                {"out": {"delaySts":0, "delayTimeLeft":0xFFFF, "modeStsSet":0,
                                                       "lastSetTime" : 0xFFFF, "reason" :0}})
        
    @allure.title("12v电源延时状态_OFF_Standby")
    @pytest.mark.sanity
    def test_caseid_1984954(self):
        self.sd_tester.change_usage_mode(0)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})
        self.ck_powerOutletDelay_warning_and_resp(1, 1, 1, 1, 0)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 1, 1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":2}})
        self.ck_powerOutletDelay_warning_and_resp(1, 0xFFFF, 2, 1, 0)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
    @allure.title("12v电源延时状态_Standby_Standby")
    @pytest.mark.full
    def test_caseid_1984970(self):
        self.sd_tester.change_usage_mode(0)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})
        self.ck_powerOutletDelay_warning_and_resp(1, 1, 1, 1, 0)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        self.ck_powerOutletDelay_warning_and_resp(1, 0xFFFF, 2, 1, 0)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})
        self.ck_powerOutletDelay_warning_and_resp(1, 1, 1, 1, 0)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
    @allure.title("12v电源延时状态_Standby(kTimerMode)_Keeping_OFF(定时器到期)")
    @pytest.mark.full
    def test_caseid_1984982(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 0.0)
        sleep(2)
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)

        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
        self.ck_powerOutletDelay_warning_and_resp(1, 2, 1, 2, 0)
        #进入keeping
        self.sd_tester.change_usage_mode(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        for i in [0,1]:
            logger.info(f"i = {i}")
            if i == 0:
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
                sleep(0.5)
            else:
                self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
                sleep(0.5)
                self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
                # self.partner.empty_all(0.5)
                self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.0)
                sleep(0.5)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
                
            self.ck_powerOutletDelay_warning_and_resp(2, 2, 1, 2, 0)
            sleep(65)
            
            self.ck_powerOutletDelay_warning_and_resp(2, 1, 1, 2, 0)
            sleep(60)
            
            self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 3)
                
        self.ck_ipdu_signal(0.2, 1, 0.5)
    
    @allure.title("12v电源延时状态_keeing状态下行PDU周期校验")
    @pytest.mark.sanity
    def test_caseid_1985373(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 0.0)
        sleep(2)
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)

        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
        self.ck_powerOutletDelay_warning_and_resp(1, 2, 1, 2, 0)
        #进入keeping
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        self.bgm_eth_inter.start_bgm_tcpdump()
                
        self.ck_powerOutletDelay_warning_and_resp(2, 2, 1, 2, 0)
        sleep(5)   
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time("UsgModKeeperReq", 0.2)
        self.bgm_eth_inter.ck_period_time("RlyPwrCmdProxyReq", 0.5,permit_fail_times=2) #同一帧被校验到2次
        self.bgm_eth_inter.ck_period_time("HVActvForProxy", 1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
              
    @allure.title("12v电源延时状态_Standby(kKeepMode)_Keeping_OFF(用户触发)")
    @pytest.mark.full
    def test_caseid_1984983(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 0.0)
        sleep(2)
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        self.ck_powerOutletDelay_warning_and_resp(1, 0xFFFF, 2, 2, 0)
        #进入keeping
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.change_usage_mode(1)
        for i in [0,1]:
            logger.info(f"i = {i}")
            if i == 0:
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
                sleep(0.5)
            else:
                self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
                sleep(0.5)
                self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
                #self.partner.empty_all(0.5)
                self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
                self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.0) #不存在开始
                sleep(0.1)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
                sleep(0.5)
                
            self.ck_powerOutletDelay_warning_and_resp(2, 0xFFFF, 2, 2, 0)
            self.partner.empty_all(0.5)
            sleep(65)
            self.partner.ck_no_event(VEHICLESETSTATUS_CLIENT, "PowerOutletDelayInfo")
            
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
            self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 1)
            
        self.ck_ipdu_signal(0.2, 1, 0.5)
              
    @allure.title("12电源延时状态_Standby(kTimerMode)_Keeping_OFF(用户触发)")
    @pytest.mark.full
    def test_caseid_1984984(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 0.0)
        sleep(2)
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
        
        self.ck_powerOutletDelay_warning_and_resp(1, 2, 1, 2, 0)
        #进入keeping
        self.sd_tester.change_usage_mode(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        for i in [0,1]:
            logger.info(f"i = {i}")
            if i == 0:
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
                sleep(0.5)
            else:
                self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
                self.partner.empty_all(0.5)
                self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
                self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.0)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
                sleep(0.5)
               
            self.ck_powerOutletDelay_warning_and_resp(2, 2, 1, 2, 0)
            sleep(65)
            self.ck_powerOutletDelay_warning_and_resp(2, 1, 1, 2, 0)
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
            self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 1)
            
        self.ck_ipdu_signal(0.2, 1, 0.5)
          
    @allure.title("12v电源延时状态_Standby(kKeepMode)_Keeping_OFF(退出条件触发)")
    @pytest.mark.full
    def test_caseid_1984986(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 0.0)
        sleep(2)
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)

        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})

        #进入keeping-OFF组合1
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        sleep(0.5)
        self.sd_tester.change_usage_mode(13)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 4)
        
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        #进入keeping-OFF组合2
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)
        #需要等待10s吗
        sleep(10)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 5)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        #进入keeping-OFF组合3
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        self.sd_tester.change_usage_mode(0)
        #需要等待10s吗
        sleep(10)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 5)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        #进入keeping-OFF组合4
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 9.0)
        sleep(0.5)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 2)
        
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        #进入keeping-OFF组合5 
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.0)
        self.sd_tester.change_usage_mode(13)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 4)
        
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        #进入keeping-OFF组合6
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)
        #需要等待10s吗
        sleep(10)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 5)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        #进入keeping-OFF组合7
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        self.sd_tester.change_usage_mode(0)
        #需要等待10s吗
        sleep(10)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 5)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        #进入keeping-OFF组合8
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 9.0)
        sleep(0.5)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 2)
        
        self.ck_ipdu_signal(0.2, 1, 0.5)

                    
    @allure.title("12v电源延时状态_Standby(kTimerMode)_Keeping_OFF(退出条件触发)")
    @pytest.mark.full
    def test_caseid_1984987(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 0.0)
        sleep(2)
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)

        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})
        sleep(0.5)
        #进入keeping-OFF组合1
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        sleep(1) #这里会偶现不会进入keeping
        self.sd_tester.change_usage_mode(13)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 1, 4)
        
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})
        #进入keeping-OFF组合2
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)
        #需要等待10s吗
        sleep(10)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 1, 5)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})
        #进入keeping-OFF组合3
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        self.sd_tester.change_usage_mode(0)
        #需要等待10s吗
        sleep(10)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 1, 5)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})
        #进入keeping-OFF组合4
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 9.0)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 1, 2)
        
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.0)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})
        #进入keeping-OFF组合5 
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_usage_mode(13)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 1, 4)
        
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})
        #进入keeping-OFF组合6
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)
        #需要等待10s吗
        sleep(10)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 1, 5)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
  
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})
        #进入keeping-OFF组合7
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.0)
        self.sd_tester.change_usage_mode(0)
        #需要等待10s吗
        sleep(10)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 1, 5)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})
        #进入keeping-OFF组合8
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 9.0)
        sleep(0.5)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 1, 2)
     
        self.ck_ipdu_signal(0.2, 1, 0.5)
                    
                    
    @allure.title("12v电源延时状态_Standby(kKeepMode)_Keeping_不满足进入条件保持Stanby状态_OFF")
    @pytest.mark.full
    def test_caseid_1985031(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 0.0)
        sleep(2)
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)#防止上一个case干扰
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        self.partner.empty_all(0.5)
        
        self.sd_tester.change_usage_mode(1)

        sleep(0.5)
        self.partner.ck_no_event(VEHICLESETSTATUS_CLIENT,"PowerOutletDelayInfo")                                      
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetPowerOutletDelayInfo", {}, 
                                                {"out": {"delaySts":1, "delayTimeLeft":0xFFFF ,"modeStsSet":2 ,"lastSetTime":2 ,"reason":0 }})

    @allure.title("12v电源延时状态_Standby(kKeepMode)_Keeping_OFF(退出条件不满足保持当前状态)")
    @pytest.mark.full
    def test_caseid_1985032(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 11.0)
        sleep(2)
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)

        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})

        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        sleep(0.5)
        self.ck_powerOutletDelay_warning_and_resp(2, 0xFFFF, 2, 2, 0)
        
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.partner.ck_no_event(VEHICLESETSTATUS_CLIENT,"PowerOutletDelayInfo")                                      
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetPowerOutletDelayInfo", {}, 
                                                {"out":  {"delaySts":2, "delayTimeLeft":0xFFFF,"modeStsSet":2,"lastSetTime":2 ,"reason":0 }})
        
    @allure.title("12电源延时状态_Standby(kTimerMode)_Keeping_Stop_OFF(定时器到期)")
    @pytest.mark.full
    def test_caseid_1985049(self):
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)

        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
        sleep(0.5)
        #进入keeping
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        sleep(0.5)
        self.ck_powerOutletDelay_warning_and_resp(2, 2, 1, 2, 0)
        sleep(5)
        #进入stop
        for i in [0 ,1]:
            logger.info(f"i = {i}")
            if i == 0:
                self.sd_tester.change_usage_mode(2)
            else :
                self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
                self.partner.empty_all(0.5)
                self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
                sleep(0.5)
                self.sd_tester.change_usage_mode(1)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
                sleep(0.5)
                self.sd_tester.change_usage_mode(11)
            self.ck_powerOutletDelay_warning_and_resp(3, 2, 1, 2, 0)
            sleep(65)
            self.ck_powerOutletDelay_warning_and_resp(3, 1, 1, 2, 0)
            sleep(65)
            self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 3)
        #usagemode离开 inactive  RlyPwrCmdProxyReq就失效了，可以不用下发0    
        #self.ck_ipdu_signal(0.2, 1, 0.5)
    
    @allure.title("12v电源延时状态_Standby(kKeepMode)_Keeping_Stop_OFF(用户触发)")
    @pytest.mark.full
    def test_caseid_1985051(self):
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        #进入keeping
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        sleep(5)
        #进入stop
        for i in [0 ,1]:
            logger.info(f"i = {i}")
            if i == 0:
                self.sd_tester.change_usage_mode(2)
            else :
                self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
                sleep(0.5)
                self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
                self.partner.empty_all(0.5)
                self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
                self.sd_tester.change_usage_mode(1)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
                sleep(0.5)
                self.sd_tester.change_usage_mode(11)
        
            self.ck_powerOutletDelay_warning_and_resp(3, 0xFFFF, 2, 2, 0)
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
            self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 1)
        #usagemode离开 inactive  RlyPwrCmdProxyReq就失效了，可以不用下发0  
        #self.ck_ipdu_signal(0.2, 1, 0.5)

    @allure.title("12电源延时状态_Standby(kTimerMode)_Keeping_Stop_OFF(用户触发)")
    @pytest.mark.full
    def test_caseid_1985052(self):
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)

        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        sleep(0.5)
        #进入stop
        for i in [0 ,1]:
            if i == 0:
                self.sd_tester.change_usage_mode(2)
            else :
                self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
                sleep(0.5)
                self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
                self.sd_tester.change_usage_mode(1)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
                sleep(0.5)
                self.sd_tester.change_usage_mode(11)
           
            self.ck_powerOutletDelay_warning_and_resp(3, 2, 1, 2, 0)
            sleep(65)
            
            self.ck_powerOutletDelay_warning_and_resp(3, 1, 1, 2, 0)
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
           
            self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 1)
            
    @allure.title("12电源延时状态_Standby(kTimerMode)_Keeping_Stop_OFF(用户重新设置模式)")
    @pytest.mark.smoke
    def test_caseid_1985053(self):
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)

        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
        #进入keeping
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        sleep(0.5)
        #进入stop
        self.sd_tester.change_usage_mode(2)
        self.ck_powerOutletDelay_warning_and_resp(3, 2, 1, 2, 0)
        
        sleep(30)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
    
        self.ck_powerOutletDelay_warning_and_resp(3, 0xFFFF, 2, 2, 0)
        self.partner.empty_all(0.5)
        sleep(65)
        self.partner.ck_no_event(VEHICLESETSTATUS_CLIENT, "PowerOutletDelayInfo")
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetPowerOutletDelayInfo", {}, 
                                                {"out":{"delaySts":3, "delayTimeLeft":0xFFFF ,"modeStsSet":2 ,"lastSetTime":2 ,"reason":0 }}) 
         
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 1)
          
    @allure.title("12电源延时状态_Standby(kTimerMode)_Keeping_Stop_Stop(时长更新)")
    @pytest.mark.sanity
    def test_caseid_1985055(self):
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)

        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
        #进入keeping
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        sleep(0.5)
        #进入stop
        self.sd_tester.change_usage_mode(11)
        
        self.ck_powerOutletDelay_warning_and_resp(3, 2, 1, 2, 0)
        sleep(65)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
        sleep(65)
        self.ck_powerOutletDelay_warning_and_resp(3, 1, 1, 2, 0)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 1)
        
    @allure.title("12v电源延时状态_Standby(kKeepMode)_Keeping_Stop_Stop(用户重新设置模式)")
    @pytest.mark.smoke
    def test_caseid_1985057(self):
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)

        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        #进入keeping
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 24)
        sleep(0.5)
        #进入stop
        self.sd_tester.change_usage_mode(2)
        self.ck_powerOutletDelay_warning_and_resp(3, 0xFFFF, 2, 2, 0)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
        sleep(65)
        self.ck_powerOutletDelay_warning_and_resp(3, 1, 1, 2, 0)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 1)
        
    @allure.title("12v电源延时状态_Standby(kKeepMode)_Keeping_Stop_OFF(退出条件触发)")
    @pytest.mark.sanity
    def test_caseid_1985061(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 0.0)
        sleep(2)
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)

        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        sleep(0.5)
        #进入keeping-OFF组合
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 24)
        sleep(0.5)
        self.sd_tester.change_usage_mode(2)
        sleep(0.5)
        self.sd_tester.change_usage_mode(13)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 4)
        
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        #进入keeping-OFF组合2
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        sleep(0.5)
        self.sd_tester.change_usage_mode(11)
        sleep(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)
        #需要等待10s吗
        sleep(10)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 5)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        #进入keeping-OFF组合3
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        sleep(0.5)
        self.sd_tester.change_usage_mode(2)
        sleep(0.5)
        self.sd_tester.change_usage_mode(0)
        #需要等待10s吗
        sleep(10)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 5)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        #进入keeping-OFF组合4
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        sleep(0.5)
        self.sd_tester.change_usage_mode(11)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 9.0)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 2)
        
    @allure.title("12v电源延时状态_Standby(kTimerMode)_Keeping_Stop_OFF(退出条件触发)")
    @pytest.mark.sanity
    def test_caseid_1985062(self):
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})
        sleep(0.5)
        #进入keeping-OFF组合1
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.0)
        sleep(0.5)
        self.sd_tester.change_usage_mode(2)
        sleep(0.5)
        self.sd_tester.change_usage_mode(13)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 1, 4)
        
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})
        #进入keeping-OFF组合2
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.0)
        sleep(0.5)
        self.sd_tester.change_usage_mode(11)
        sleep(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)
        #需要等待10s吗
        sleep(10)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 1, 5)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})
        #进入keeping-OFF组合3
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.0)
        sleep(0.5)
        self.sd_tester.change_usage_mode(2)
        sleep(0.5)
        self.sd_tester.change_usage_mode(0)
        #需要等待10s吗
        sleep(10)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 1, 5)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})
        #进入keeping-OFF组合4
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.0)
        sleep(0.5)
        self.sd_tester.change_usage_mode(11)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 9.0)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 1, 2)
        
    @allure.title("12v电源延时状态_Standby(kKeepMode)_Keeping_Stop_Keeping")
    @pytest.mark.sanity
    def test_caseid_1985063(self):
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        #进入keeping
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        sleep(0.5)
        #进入stop
        self.sd_tester.change_usage_mode(2)
        self.bgm_eth_inter.start_bgm_tcpdump()
        #进入keeping
        self.sd_tester.change_usage_mode(1)
        self.ck_powerOutletDelay_warning_and_resp(2, 0xFFFF, 2, 2, 0)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        a = self.bgm_eth_inter.get_signal_values("UsgModKeeperReq")
        b = self.bgm_eth_inter.get_signal_values("HVActvForProxy")
        c = self.bgm_eth_inter.get_signal_values("RlyPwrCmdProxyReq")
        assert 1 in a
        assert 1 in b
        assert 1 in c
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 1)
        
    @allure.title("12v电源延时状态_Standby(kTimerMode)_Keeping_Stop_Keeping")
    @pytest.mark.sanity
    def test_caseid_1985064(self):
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})
        sleep(0.5)
        #进入keeping
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.0)
        sleep(0.5)
        self.sd_tester.change_usage_mode(11)
        sleep(0.5)
        #进入keeping
        self.sd_tester.change_usage_mode(1)
      
        self.ck_powerOutletDelay_warning_and_resp(2, 1, 1, 1, 0)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
       
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 1, 1) 
    
    @allure.title("12v电源延时状态_断电保持")
    @pytest.mark.sanity
    def test_caseid_1985065(self):
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}},timeout=3)#遇到之前有重启了
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}},timeout=3)
        sleep(0.5)
        self.ck_powerOutletDelay_warning_and_resp(1, 1, 1, 1, 0) 
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetPowerOutletDelayInfo", {}, 
                                                {"out":{"delaySts":1, "delayTimeLeft":1 ,"modeStsSet":1 ,"lastSetTime":1 ,"reason":0 }})
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}},timeout=3)
        sleep(0.5)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 1, 1) 
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetPowerOutletDelayInfo", {}, 
                                                {"out":{"delaySts":0, "delayTimeLeft":0xFFFF ,"modeStsSet":0,"lastSetTime":1,"reason":0 }})
        
    @allure.title("12v电源延时状态_Standby(kKeepMode)_Keeping_OFF(Reason1,2,3,4,5同时满足)")
    @pytest.mark.sanity
    def test_caseid_1985066(self):
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        sleep(0.5)
        #进入keeping
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
       
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)
        self.sd_tester.change_usage_mode(0)
        sleep(62)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 9.0)

        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 2, 1) 
        
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
         
        
    @allure.title("12v电源延时状态_Standby(kTimerMode)_Keeping_OFF(Reason2,3同时满足)")
    @pytest.mark.sanity
    def test_caseid_1985108(self):
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})
        sleep(0.5)
        #进入keeping
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        sleep(0.5)
        self.ck_powerOutletDelay_warning_and_resp(2, 1, 1, 1, 0) 
        
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 9.0)
        sleep(65)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 1, 2) 
    
    @allure.title("12v电源延时状态_Standby(kKeepMode)_Keeping_OFF(Reason4,5同时满足)")
    @pytest.mark.sanity
    def test_caseid_1985109(self):
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        sleep(0.5)
        #进入keeping
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        sleep(2)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)
        sleep(10)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 1, 4)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
    
    @allure.title(" 12v电源延时状态_断电保持_keeping需恢复到Stop状态")
    @pytest.mark.sanity
    def test_caseid_1985110(self):
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 9.0)
        sleep(2)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        #进入keeping
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        sleep(2)
        self.ck_powerOutletDelay_warning_and_resp(2, 0xFFFF, 2, 1, 0)
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT)
        self.sd_tester.change_usage_mode(2)
        self.ck_powerOutletDelay_warning_and_resp(3, 0xFFFF, 2, 1, 0)
        
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        sleep(2)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        #进入keeping
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        sleep(2)
        self.ck_powerOutletDelay_warning_and_resp(2, 0xFFFF, 2, 1, 0)
        self.restart_bgm_and_connect_service(VEHICLESETSTATUS_CLIENT,pause_all_bus=True, resume_all_bus=False)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"PowerOutletDelayInfo",{"sts": 
                                                {"delaySts":3, "delayTimeLeft":0xFFFF ,"modeStsSet":2 ,"lastSetTime":1 ,"reason":0}},timeout=5)
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"PowerOutletDelayInfo",{"sts": 
                                                {"delaySts":2, "delayTimeLeft":0xFFFF ,"modeStsSet":2 ,"lastSetTime":1 ,"reason":0}},timeout=5)
        
    @allure.title("12v电源延时状态_反向用例_OFF状态下VMM=Convince无法进入Stop")
    @pytest.mark.sanity
    def test_caseid_1985111(self):
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay",{"req":{"modeSts":0,"time":0}})
        self.partner.empty_all(0.5)
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_no_event(VEHICLESETSTATUS_CLIENT,"PowerOutletDelayInfo")
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        
    @allure.title("12v电源延时状态_反向用例_Standby无法通过满足退出条件进入OFF")
    @pytest.mark.sanity
    def test_caseid_1985112(self):
        #usage=13 确保不能从stanby跳keeping
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})
        self.partner.empty_all(0.5)
        self.sd_tester.change_usage_mode(13)
        self.partner.ck_no_event(VEHICLESETSTATUS_CLIENT,"PowerOutletDelayInfo")
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetPowerOutletDelayInfo", {}, 
                                                {"out": {"delaySts":1, "delayTimeLeft":1 ,"modeStsSet":1 ,"lastSetTime":1 ,"reason":0 }})

    @allure.title("12v电源延时状态_Standby(kKeepMode)_Keeping_Keeping_OFF(用户触发)")
    @pytest.mark.sanity
    def test_caseid_1985114(self):
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
        #进入keeping
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})

        self.ck_powerOutletDelay_warning_and_resp(2, 1, 1, 1, 0)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        
    @allure.title("12电源延时状态_Standby(kTimerMode)_Keeping_Keeping_OFF(用户触发)")
    @pytest.mark.smoke
    def test_caseid_1985115(self):
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
        #进入keeping
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":2,"time":1}})
       
        self.ck_powerOutletDelay_warning_and_resp(2, 0xFFFF, 2, 2, 0)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
    
    @allure.title("12v电源延时状态_Standby(kTimerMode)_Keeping_OFF(定时器多次启停、打断)")
    @pytest.mark.sanity
    def test_caseid_1985157(self):
        #需要满足dcdc条件，否则进入后里面满足退出条件，退出keeping状态
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":0,"time":0}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":2}})
        #进入keeping
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 24)
        sleep(0.5)
        sleep(65)
        self.ck_powerOutletDelay_warning_and_resp(2, 1, 1, 2, 0)
        self.partner.empty_all(0.5)
        sleep(30)
        self.partner.ck_no_event(VEHICLESETSTATUS_CLIENT,"PowerOutletDelayInfo")
        
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetPowerOutletDelay", {"req":{"modeSts":1,"time":1}})
        self.ck_powerOutletDelay_warning_and_resp(2, 1, 1, 1, 0)
        self.partner.ck_no_event(VEHICLESETSTATUS_CLIENT,"PowerOutletDelayInfo")
        sleep(40)
        self.partner.ck_no_event(VEHICLESETSTATUS_CLIENT,"PowerOutletDelayInfo")
        sleep(25)
        self.ck_powerOutletDelay_warning_and_resp(0, 0xFFFF, 0, 1, 3)
        
    @allure.title("出厂默认值PrkgCmftModTiCtrl=255时只能开启维持上电")
    @pytest.mark.sanity
    def test_caseid_1985779(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.sd_tester.change_usage_mode(2)
        #车辆模式不为normal时，不能闭锁设防
        self.five_door_close()
        self.dk.set_cenlock_sts(0x1)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(0,0,0,0,0)
        self.set_gear_P_speed_0()
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        # 删除数据库
        self.del_s2s_db()
        sleep(2)
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        self.partner.empty_all(4)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetConvenienceModeDuration",{"duration": 255})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",{"sts":{"modeSts":1,"reason":0}})
        self.partner.ck_no_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortBaseFunctionSts",timeout=5)
    
    ######################################################################################################################################################## 
@allure.feature("SOA服务接口")    
@allure.story("BGM应用/VehicleSetStatusService")   
class TestVehicleSetStatusServiceMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("VehicleSetStatusService", "client"),("VehicleModeService", "client"),
        ("FotaMasterService", "server"),("CTDService", "client"),("ConditionCheckService", "client"),
        ("SeatService", "client"),("PedalService", "client"),("ChassisService", "client"),
        ("HighVoltageService", "client")])
        self.partner.wait_for_service_reconnect(VEHICLESETSTATUS_CLIENT)   

    def after_class(self, ecu):
        try:
            self.partner.stop_operators()
        except Exception as e:
            logger.error(f"{str(e)}")
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu)
        
    @allure.title("设置维持上电关闭时超时") 
    @pytest.mark.sanity
    def test_caseid_1983204(self):
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02,'VehModMngtGlbSafe1UsgModSts', 2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        #重启后，VehicleSet服务需要花一定时间保证服务能真实可用
        sleep(6)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255) #一直都是255
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",{"sts":{"modeSts":1,"reason":0}})
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 19.0)
        sleep(2)
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},{"out":{"modeSts":1,"reason":0}})
        self.partner.empty_all(3)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(2)#超时后始终不回复repsonse
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        sleep(2)
        # self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",{"sts":{"modeSts":1,"reason":0}})
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},{"out":{"modeSts":1,"reason":0}})
        self.partner.empty_all(3)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        sleep(0.5)#超时后内部第二次调用回repsonse
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 19.0)
        sleep(1.5)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        sleep(0.5)
        self.partner.ck_s2s_event(VEHICLESETSTATUS_CLIENT,"ParkingComfortModeSts",{"sts":{"modeSts":0,"reason":2}})
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},{"out":{"modeSts":0,"reason":2}})
        
@allure.feature("SOA服务接口")
@allure.story("BGM应用/VehicleSetStatusService")
class TestVehicleSetStatusServiceFota(TestBase):
    
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu, enable_inter_service=True)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        for process_name in ["monitor_em2.sh", "em2", "fota/fota", "service_monitor"]:
            res = command_send(
                device_name="BGM",
                cmd=f"ps -ef |grep app |grep {process_name} |grep -v grep",
                timeout=60,
            )[1]
            pid = res.split()[1]
            command_send(device_name="BGM", cmd=f"kill -9 {pid}")
        sleep(2)
        command_send(device_name="BGM", cmd='su - service_monitor -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;/app/bin/service_monitor  -c /app/etc/service_monitor.json &"', timeout=15)
        self.partner = S2sBaseClass([
            ("VehicleSetStatusService", "client"),("VehicleModeService", "client"),("FotaMasterService", "server"),
            ("CTDService", "client"),("KeyService", "client"),("SeatService", "client"),("HighVoltageService","client")])
        self.partner.wait_for_service_reconnect(FOTAMASTER_SERVICE_SERVER)
        self.sd_tester.tester_present()

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.sd_tester.stop_tester_present()
        self.partner.stop_operators()
        self.nucapp.bgm_power_off()
        sleep(3)
        self.nucapp.bgm_power_on()
        sleep(10)
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.partner.empty_all(1)
        self.sd_tester.change_car_mode(0)

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send() 
        super().after_each_func(ecu, start=False)
        
    def Shift_Gear(self, X):
        """0代表P挡 2代表N挡 3代表D挡 1代表R挡"""
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', X)
        sleep(1)
        
    def five_door_close(self):
        self.io.pass_door_close()
        self.io.drvr_door_close()
        self.io.lere_door_close()
        self.io.rire_door_close()
        self.io.trunk_door_close()
        
    def set_four_seat_occupt(self,A,B,C,D):
        """设置副驾 左后 后中 后右 1/2代表占位 0 代表未占位"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts', A)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe', B)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecMid', C)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecRi', D)
        sleep(1)
    
    def seat_belt_status(self,A,B,C,D,E):
        """设置主驾 副驾 左后 后中 后右 1代表已系 0 代表未系"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', A)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1', B)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecLeBltLockSt1', C)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecLeBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecMidBltLockSt1', D)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecMidBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecRiBltLockSt1', E)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecRiBltLockSts', 0)
        sleep(1)
        
    @allure.title("遍历_获取和通知维持上电基础能力_不同原因退出导致的闭锁设防")
    @pytest.mark.sanity
    def test_caseid_1985132(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.sd_tester.enter_default_session()
        #车辆模式不为normal时，不能闭锁设防
        for carmode in [1,2,5]:
            self.five_door_close()
            self.dk.set_cenlock_sts(0x1)
            self.io.driver_seat_notpresent()
            self.set_four_seat_occupt(0,0,0,0)
            self.Shift_Gear(0) #非P档
            self.seat_belt_status(0,0,0,0,0)
            self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": 2})
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 0,"source":"PetMode"}})
            sleep(1)
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 1,"source":"PetMode"}})
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
            sleep(1)
            self.dk.send_nfc_cmd()
            sleep(2)
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": carmode})
            sleep(1)
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
            sleep(1)
            self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT,"getAlarmInfo",{},{"out":{"sysSts":0}})
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": 0})
            sleep(1)
        #挡位不为P档时，不能闭锁设防
        for gear in range(1,4):
            self.five_door_close()
            self.dk.set_cenlock_sts(0x1)
            self.io.driver_seat_notpresent()
            self.set_four_seat_occupt(0,0,0,0)
            self.Shift_Gear(0) #非P档
            self.seat_belt_status(0,0,0,0,0)
            self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": 11})
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
            sleep(1)
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 1,"source":"PetMode"}})
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
            sleep(1)
            self.dk.send_nfc_cmd()
            sleep(2)
            self.Shift_Gear(gear) #非P档
            sleep(1)
            self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortBaseFunctionSts",{},{"out":
                                                            {"modeSts":0,"reason":3,"source":"PetMode"}})
            sleep(1)
            self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT,"getAlarmInfo",{},{"out":{"sysSts":0}})
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": 0})
            sleep(1)
        #情况6因电量、fota退出导致的闭锁设防
        self.five_door_close()
        self.dk.set_cenlock_sts(0x1)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(0,0,0,0,0)
        self.Shift_Gear(0) #非P档
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": 0})
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": 2})
        self.Shift_Gear(0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        sleep(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 1,"source":"PetMode"}})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        sleep(1)
        self.dk.send_nfc_cmd()
        sleep(2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 11)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 19.0)
        sleep(1)
        self.partner.send_event_notify(FOTAMASTERSERVICE_SERVER, "Status",{"status": {"taskId":0, "state":5, "errorCode":0}})
        sleep(1)
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortBaseFunctionSts",{},{"out":
                                                            {"modeSts":0,"reason":2,"source":"PetMode"}})
        sleep(1)
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT,"getAlarmInfo",{},{"out":{"sysSts":1}})
        #车辆模式变为crash时不能上锁
        self.sd_tester.tester_present()
        self.five_door_close()
        self.Shift_Gear(0)
        self.dk.set_cenlock_sts(0x1)
        sleep(1)
        self.sd_tester.change_usage_mode(2)
        self.five_door_close()
        self.dk.set_cenlock_sts(0x1)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(0,0,0,0,0)
        self.partner.send_event_notify(FOTAMASTERSERVICE_SERVER, "Status",{"status": {"taskId":0, "state":0, "errorCode":0}})
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        sleep(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 1,"source":"PetMode"}})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        sleep(1)
        self.dk.send_nfc_cmd()
        sleep(2)
        self.dk.ck_cenlock_sts(3)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 11)
        self.sd_tester.change_car_mode(3)
        sleep(3)#服务无法切crash，只能通过检测中控锁状态为1来判断未上锁
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt_1_CEMBodySignalIPdu13',1)
        self.sd_tester.stop_tester_present()
        sleep(1)
        
    @allure.title("设置维持上电模式_遍历FOTA")
    @pytest.mark.full
    def test_caseid_1987130(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        #fota状态不满足无法调用
        self.partner.send_event_notify(FOTAMASTERSERVICE_SERVER, "Status",{"status": {"taskId":0, "state":5, "errorCode":0}})
        sleep(0.5) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        self.partner.send_event_notify(FOTAMASTERSERVICE_SERVER, "Status",{"status": {"taskId":0, "state":0, "errorCode":0}})
        
    @allure.title("遍历_获取和通知维持上电模式状态_不同原因退出导致的闭锁设防")
    @pytest.mark.sanity
    def test_caseid_1983178(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.sd_tester.enter_default_session()
        self.partner.send_event_notify(FOTAMASTERSERVICE_SERVER, "Status",{"status": {"taskId":0, "state":0, "errorCode":0}})
        #车辆模式不为normal时，不能闭锁设防
        for carmode in [1,2,5]:
            self.five_door_close()
            self.dk.set_cenlock_sts(0x1)
            self.io.driver_seat_notpresent()
            self.set_four_seat_occupt(0,0,0,0)
            self.seat_belt_status(0,0,0,0,0)
            self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": 2})
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": 0})
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
            sleep(1)
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
            sleep(1)
            self.dk.send_nfc_cmd()
            sleep(2)
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": carmode})
            sleep(1)
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
            sleep(1)
            self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT,"getAlarmInfo",{},{"out":{"sysSts":0}})
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": 0})
            sleep(1)
        #挡位不为P档时，不能闭锁设防
        for gear in range(1,4):
            self.five_door_close()
            self.dk.set_cenlock_sts(0x1)
            self.io.driver_seat_notpresent()
            self.set_four_seat_occupt(0,0,0,0)
            self.seat_belt_status(0,0,0,0,0)
            self.Shift_Gear(0) #P档
            self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": 11})
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
            sleep(1)
            self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
            sleep(1)
            self.dk.send_nfc_cmd()
            sleep(2)
            self.Shift_Gear(gear) #非P档
            sleep(1)
            self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},{"out":{"modeSts":0,"reason":3}})
            sleep(1)
            self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT,"getAlarmInfo",{},{"out":{"sysSts":0}})
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": 0})
            sleep(1)
        #情况6因电量、fota退出导致的闭锁设防
        self.five_door_close()
        self.dk.set_cenlock_sts(0x1)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(0,0,0,0,0)
        self.Shift_Gear(0) #P档
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": 0})
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": 2})
        self.Shift_Gear(0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        sleep(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        sleep(1)
        self.dk.send_nfc_cmd()
        sleep(2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 11)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 19.0)
        sleep(1)
        self.partner.send_event_notify(FOTAMASTERSERVICE_SERVER, "Status",{"status": {"taskId":0, "state":5, "errorCode":0}})
        sleep(1)
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},{"out":{"modeSts":0,"reason":2}})
        sleep(1)
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT,"getAlarmInfo",{},{"out":{"sysSts":1}})
        #车辆模式变为crash时不能上锁
        self.five_door_close()
        self.dk.set_cenlock_sts(0x1)
        sleep(1)
        self.partner.send_event_notify(FOTAMASTERSERVICE_SERVER, "Status",{"status": {"taskId":0, "state":0, "errorCode":0}})
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": 0})
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": 2})
        self.five_door_close()
        self.dk.set_cenlock_sts(0x1)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(0,0,0,0,0)
        self.Shift_Gear(0) #P档
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        sleep(1)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        sleep(1)
        self.dk.send_nfc_cmd()
        sleep(2)
        self.dk.ck_cenlock_sts(3)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 11)
        self.sd_tester.change_car_mode(3)
        sleep(3)#服务无法切crash，只能通过检测中控锁状态为1来判断未上锁
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt',1)
           
    @allure.title("设置维持上电基础能力_Fota更新时退出")
    @pytest.mark.sanity
    def test_caseid_1985131(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.sd_tester.change_car_mode(0)
        #正常设置打开或关闭
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        self.Shift_Gear(0) #P档
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp",{"cmd":{"modeSts": 1,"source":"PetMode"}})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 0,"source":"PetMode"}})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)

        #fota状态不满足无法调用
        self.partner.send_event_notify(FOTAMASTERSERVICE_SERVER, "Status",{"status": {"taskId":0, "state":5, "errorCode":0}})
        sleep(0.5) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 1,"source":"PetMode"}})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        self.partner.send_event_notify(FOTAMASTERSERVICE_SERVER, "Status",{"status": {"taskId":0, "state":0, "errorCode":0}})
        sleep(0.5)
        
        #先调用再设置fota状态
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortBaseFunctionByApp", {"cmd":{"modeSts": 1,"source":"PetMode"}})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        self.partner.send_event_notify(FOTAMASTERSERVICE_SERVER, "Status",{"status": {"taskId":0, "state":5, "errorCode":0}})
        sleep(1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        self.partner.send_event_notify(FOTAMASTERSERVICE_SERVER, "Status",{"status": {"taskId":0, "state":0, "errorCode":0}})
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortBaseFunctionSts",{},{"out":
                                                                {"modeSts":0,"reason":5,"source":"PetMode"}})
        
    @allure.title("设置维持上电_Fota更新时退出")
    @pytest.mark.sanity
    def test_caseid_1985624(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.sd_tester.change_car_mode(0)
        #正常设置打开或关闭
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        self.Shift_Gear(0) #P档
        self.partner.empty_all(0.5)
        self.partner.send_event_notify(FOTAMASTERSERVICE_SERVER, "Status",{"status": {"taskId":0, "state":0, "errorCode":0}})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)

        #fota状态不满足无法调用
        self.partner.send_event_notify(FOTAMASTERSERVICE_SERVER, "Status",{"status": {"taskId":0, "state":5, "errorCode":0}})
        sleep(0.5) 
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        self.partner.send_event_notify(FOTAMASTERSERVICE_SERVER, "Status",{"status": {"taskId":0, "state":0, "errorCode":0}})
        sleep(0.5)
        
        #先调用再设置fota状态
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',255)
        self.partner.send_event_notify(FOTAMASTERSERVICE_SERVER, "Status",{"status": {"taskId":0, "state":5, "errorCode":0}})
        sleep(1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'PrkgCmftModTiCtrl',0)
        self.partner.send_event_notify(FOTAMASTERSERVICE_SERVER, "Status",{"status": {"taskId":0, "state":0, "errorCode":0}})
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT,"GetParkingComfortModeSts",{},{"out":{"modeSts":0,"reason":5}})
    
    