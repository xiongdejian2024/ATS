"""
@File         :test_HighVoltage_abc.py
@Time         :2023/04/30 19:07:31
@Author       :tao.cheng_ext@jiduauto.com
@Description  :Test SOA for HighVoltageService
"""
import os
import sys
import pytest
import allure
from time import sleep
from datetime import datetime, timedelta

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.legacy.driver.ssh_interface import command_send
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.common.data_handle import *

@allure.feature("车控车设")
@allure.story("智能补电")
@pytest.mark.test1018
class TestHVdischarge(TestABCBase):
    def before_class(self, ecu):
        self.soa.update([("HighVoltageService", "client"),
                         ("HighVoltageAppService", "client"),
                         ("VehicleTimeService", "client"),
                         ("CarConfigService", "client"),
                         ("WTIService", "client"),
                         ("ChassisService", "client"),
                         ("VehicleSetStatusService", "client")])
        self.bus_comm.set_vehspd_gear(vehspd=0, gear=Gear.Park)
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)
        self.sd_tester.write_single_ccp(973, 2)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        sleep(2)

    def before_each_func(self, ecu):
        self.soa.set_SetACBookCharging_req(type=CommandType.kDefault, source=HV_SourceId.kFota, startTime=0, endTime=0, repeatType=CoolgReq.Off, isToTargetSOCStop=True)
        self.bus_comm.set_BookCharge_SetResponse(BookChargeSetResponse=BookChargeSetResponse.Cancelled)
        pass

    def after_each_func(self, ecu): 
        self.bus_comm.set_BookCharge_SetResponse(BookChargeSetResponse=BookChargeSetResponse.Default)
        self.soa.set_SetACBookCharging_req(type=CommandType.kDefault, source=HV_SourceId.kFota, startTime=0, endTime=0, repeatType=CoolgReq.Off, isToTargetSOCStop=True)
        pass

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    @allure.title("集度桩_充电满覆盖")
    @pytest.mark.parametrize("charging1,charging2",[(ChargingSts.ACCharging,ChargingSts.ACChargingEnd),(ChargingSts.ACCharging,ChargingSts.ChargingCmpl)
                                                    ,(ChargingSts.ACCharging,ChargingSts.ACChargingSuspend),(ChargingSts.DCCharging,ChargingSts.DCChargingEnd)],
                              ids=[1989663,1989674,1989675,1989767])
    @pytest.mark.test1118
    def test_charging01(self, charging1, charging2):
        self.sd_tester.write_ccp(ccp={973: 2})
        self.sd_tester.diag_cancel()
        self.soa.set_SetCharging_req(req=False)
        sleep(2)  # 避免之前的case在充电中，避免初始拔枪导致季度桩丢失
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=True)
        self.soa.set_SetChargeSoc_req(100.0)
        self.bus_comm.set_charging_sts(sts=charging1)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        sleep(2)
        self.bus_comm.set_charging_sts(sts=charging2)
        sleep(2)
        self.bus_comm.set_battery_charger_handle_status(soc_value=87.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        self.bus_comm.set_battery_charger_handle_status(soc_value=85.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpEna)
        

   
    @allure.title("集度桩_充电状态列变（交流）")
    @pytest.mark.parametrize("charging1,charging2",[(ChargingSts.Default,ChargingSts.ACChargingEnd),(ChargingSts.NoCharging,ChargingSts.ACChargingEnd)
                                                    ,(ChargingSts.ChargingCmpl,ChargingSts.ACChargingEnd),(ChargingSts.Heating,ChargingSts.ACChargingEnd)
                                                    ,(ChargingSts.Booking,ChargingSts.ACChargingEnd),(ChargingSts.NoDischarging,ChargingSts.ACChargingEnd)
                                                    ,(ChargingSts.Discharging,ChargingSts.ACChargingEnd),(ChargingSts.DischargingEnd,ChargingSts.ACChargingEnd)
                                                    ,(ChargingSts.DischargingCmpl,ChargingSts.ACChargingEnd),(ChargingSts.Chargingfault,ChargingSts.ACChargingEnd)
                                                    ,(ChargingSts.DischargingFault,ChargingSts.ACChargingEnd),(ChargingSts.ACChrgnFltChrgrSide,ChargingSts.ACChargingEnd)
                                                    ,(ChargingSts.DCCharging,ChargingSts.ACChargingEnd),(ChargingSts.DCChrgnFltVehSide,ChargingSts.ACChargingEnd)
                                                    ,(ChargingSts.DCChrgnFltChrgrSideTempFlt,ChargingSts.ACChargingEnd),(ChargingSts.DCChrgnFltChrgrSideConFlt,ChargingSts.ACChargingEnd)
                                                    ,(ChargingSts.DCChrgnFltChrgrSideHwFlt,ChargingSts.ACChargingEnd),(ChargingSts.DCChrgnFltChrgrSideEmgyFlt,ChargingSts.ACChargingEnd)
                                                    ,(ChargingSts.DCChrgnFltChrgrSideComFlt,ChargingSts.ACChargingEnd),(ChargingSts.SuperCharging,ChargingSts.ACChargingEnd)
                                                    ,(ChargingSts.ACChargingSuspend,ChargingSts.ACChargingEnd),(ChargingSts.DCChargingEnd,ChargingSts.ACChargingEnd)
                                                    ,(ChargingSts.ACChrgnFltVehSide,ChargingSts.ACChargingEnd),(ChargingSts.Boostcharging,ChargingSts.ACChargingEnd)
                                                    ,(ChargingSts.BoostchargingFlt,ChargingSts.ACChargingEnd),(ChargingSts.WirelessCharging,ChargingSts.ACChargingEnd)],
                              ids=[1998941,1998940,1998939,1998938,1998937,1998936,1998935,1998934,1998933,1998932,1998931
                                   ,1998930,1998929,1998928,1998927,1998926,1998925,1998924,1998923,1998922,1998921
                                   ,1998920,1998919,1998918,1998917,1998916])
    @pytest.mark.full
    @pytest.mark.test1117
    def test_charging02(self,charging1, charging2):
        self.sd_tester.write_ccp(ccp={973: 2})
        self.sd_tester.diag_cancel()
        self.soa.set_SetCharging_req(req=False)
        sleep(2)  # 避免之前的case在充电中，避免初始拔枪导致季度桩丢失
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=True)
        self.soa.set_SetChargeSoc_req(100.0)
        self.bus_comm.set_charging_sts(sts=charging1)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        sleep(2)
        self.bus_comm.set_charging_sts(sts=charging2)
        sleep(2)
        self.bus_comm.set_battery_charger_handle_status(soc_value=85.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpEna)
        
    @allure.title("集度桩_进入维修覆盖")
    @pytest.mark.parametrize("charging1,charging2",[(ChargingSts.ACCharging,ChargingSts.ACChargingEnd),(ChargingSts.ACCharging,ChargingSts.ChargingCmpl)
                                                    ,(ChargingSts.ACCharging,ChargingSts.ACChargingSuspend),(ChargingSts.DCCharging,ChargingSts.DCChargingEnd)],
                              ids=[1995664,1995665,1995666,1995667])
    @pytest.mark.full
    @pytest.mark.test1118
    def test_charging03(self, charging1, charging2):
        self.sd_tester.write_ccp(ccp={973: 2})
        self.sd_tester.diag_cancel()
        self.soa.set_SetCharging_req(req=False)
        sleep(2)  # 避免之前的case在充电中，避免初始拔枪导致季度桩丢失
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.soa.set_maintenanceMode(maintenanceMode=True)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=True)
        self.soa.set_SetChargeSoc_req(100.0)
        self.bus_comm.set_charging_sts(sts=charging1)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        sleep(2)
        self.bus_comm.set_charging_sts(sts=charging2)
        sleep(2)
        self.bus_comm.set_battery_charger_handle_status(soc_value=87.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        self.bus_comm.set_battery_charger_handle_status(soc_value=85.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)

    @allure.title("集度桩_未充电满覆盖交流")
    @pytest.mark.parametrize("charging1",[(ChargingSts.ACCharging),(ChargingSts.DCCharging),(ChargingSts.Discharging)],
                              ids=[1995668,1996877,1996901])
    @pytest.mark.full
    @pytest.mark.test1118
    def test_charging04(self, charging1):
        self.sd_tester.write_ccp(ccp={973: 2})
        self.sd_tester.diag_cancel()
        self.soa.set_SetCharging_req(req=False)
        sleep(2)  # 避免之前的case在充电中，避免初始拔枪导致季度桩丢失
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=True)
        self.soa.set_SetChargeSoc_req(100.0)
        self.bus_comm.set_charging_sts(sts=charging1)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        sleep(2)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        sleep(2)
        self.bus_comm.set_battery_charger_handle_status(soc_value=87.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        self.bus_comm.set_battery_charger_handle_status(soc_value=85.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)

    @allure.title("集度桩_未充电满覆盖直流")
    @pytest.mark.parametrize("charging1",[(ChargingSts.Discharging),(ChargingSts.Boostcharging),(ChargingSts.SuperCharging)],
                              ids=[1996902,1996903,1996904])
    @pytest.mark.full
    @pytest.mark.test1118
    def test_charging05(self, charging1):
        self.sd_tester.write_ccp(ccp={973: 2})
        self.sd_tester.diag_cancel()
        self.soa.set_SetCharging_req(req=False)
        sleep(2)  # 避免之前的case在充电中，避免初始拔枪导致季度桩丢失
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=True)
        self.soa.set_SetChargeSoc_req(100.0)
        self.bus_comm.set_charging_sts(sts=charging1)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        sleep(2)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        sleep(2)
        self.bus_comm.set_battery_charger_handle_status(soc_value=87.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        self.bus_comm.set_battery_charger_handle_status(soc_value=85.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)

    @allure.title("集度桩_充电结束（交流目标大于充满）")
    @pytest.mark.full
    @pytest.mark.test1119
    def test_caseid_1992996(self):
        self.sd_tester.write_ccp(ccp={973: 2})
        self.sd_tester.diag_cancel()
        self.soa.set_SetCharging_req(req=False)
        sleep(2)  
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=True)
        self.soa.set_SetChargeSoc_req(100.0)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACCharging)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        sleep(2)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACChargingEnd)
        sleep(5)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=True)
        sleep(2)
        self.bus_comm.check_handle_status(ChrgSoftSwCtrlSt=ChrgSoftSwCtrlSt.OnOffNoReq_NoReq)
        self.bus_comm.set_onbd_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.check_handle_status(ChrgSoftSwCtrlSt=ChrgSoftSwCtrlSt.OnOffNoReq_On)
        
    @allure.title("集度桩_充电结束（交流目标小于充满）")
    @pytest.mark.full
    @pytest.mark.test1119
    def test_caseid_1992997(self):
        self.sd_tester.write_ccp(ccp={973: 2})
        self.sd_tester.diag_cancel()
        self.soa.set_SetCharging_req(req=False)
        sleep(2)  
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=True)
        self.soa.set_SetChargeSoc_req(100.0)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACCharging)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        sleep(2)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACChargingEnd)
        self.soa.set_SetChargeSoc_req(80.0)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=True)
        sleep(2)
        self.bus_comm.check_handle_status(ChrgSoftSwCtrlSt=ChrgSoftSwCtrlSt.OnOffNoReq_NoReq)
        self.bus_comm.set_onbd_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.check_handle_status(ChrgSoftSwCtrlSt=ChrgSoftSwCtrlSt.OnOffNoReq_NoReq)

    @allure.title("集度桩_充电结束（直流目标大于充满）")
    @pytest.mark.full
    @pytest.mark.test1119
    def test_caseid_1992998(self):
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.diag_cancel()
        self.soa.set_SetCharging_req(req=False)
        sleep(2)  
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=True)
        self.soa.set_SetChargeSoc_req(100.0)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        sleep(2)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCChargingEnd)
        sleep(5)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=True)
        sleep(2)
        self.bus_comm.check_handle_status(ChrgSoftSwCtrlSt=ChrgSoftSwCtrlSt.OnOffNoReq_NoReq)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.check_handle_status(ChrgSoftSwCtrlSt=ChrgSoftSwCtrlSt.OnOffNoReq_On)

    @allure.title("集度桩_充电结束（直流目标小于充满）")
    @pytest.mark.full
    @pytest.mark.test1119
    def test_caseid_1992999(self):
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.diag_cancel()
        self.soa.set_SetCharging_req(req=False)
        sleep(2)  
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=True)
        self.soa.set_SetChargeSoc_req(100.0)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        sleep(2)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCChargingEnd)
        self.soa.set_SetChargeSoc_req(80.0)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=True)
        sleep(2)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=True)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)

    @allure.title("非集度桩_充电满覆盖直流")
    @pytest.mark.parametrize("jiduChgrFlg",[0,1,3],
                              ids=[1993187,1993200,1994280])
    @pytest.mark.full
    @pytest.mark.test1118
    def test_charging06(self, jiduChgrFlg):
        self.sd_tester.write_ccp(ccp={973: 2})
        self.sd_tester.diag_cancel()
        self.soa.set_SetCharging_req(req=False)
        sleep(2)  # 避免之前的case在充电中，避免初始拔枪导致季度桩丢失
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=False)
        self.bus_comm.set_JIDUChgrFlg_sts(jiduChgrFlg)
        self.soa.set_SetChargeSoc_req(100.0)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        sleep(2)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCChargingEnd)
        sleep(2)
        self.bus_comm.set_battery_charger_handle_status(soc_value=87.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        self.bus_comm.set_battery_charger_handle_status(soc_value=85.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)

    @allure.title("非集度桩_充电满覆盖交流")
    @pytest.mark.parametrize("jiduChgrFlg,charging1",[(0,ChargingSts.ACChargingEnd),(1,ChargingSts.ChargingCmpl),(3,ChargingSts.ACChargingSuspend)],
                              ids=[1993000,1993001,1993002])
    @pytest.mark.full
    @pytest.mark.test1118
    def test_charging07(self, jiduChgrFlg,charging1):
        self.sd_tester.write_ccp(ccp={973: 2})
        self.sd_tester.diag_cancel()
        self.soa.set_SetCharging_req(req=False)
        sleep(2)  # 避免之前的case在充电中，避免初始拔枪导致季度桩丢失
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=False)
        self.bus_comm.set_JIDUChgrFlg_sts(jiduChgrFlg)
        self.soa.set_SetChargeSoc_req(100.0)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACCharging)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        sleep(2)
        self.bus_comm.set_charging_sts(sts=charging1)
        sleep(2)
        self.bus_comm.set_battery_charger_handle_status(soc_value=87.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        self.bus_comm.set_battery_charger_handle_status(soc_value=85.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)

    @allure.title("接收云端SOC动态修正权重")
    @pytest.mark.full
    @pytest.mark.test1126
    def test_caseid_1993179(self):
        self.sd_tester.write_single_ccp(566, 23)
        self.mix.sd_tester.reset_bgm()
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.check_ResvSupChrgThermSwt_sts(0,0)
        sleep(1)
        self.soa.set_SetCloudBmsStrategyConfig_req(1)
        self.bus_comm.check_ResvSupChrgThermSwt_sts(1,1)
        
    @allure.title("接收云端SOC动态修正权重")
    @pytest.mark.full
    @pytest.mark.test1126
    def test_caseid_1994616(self):
        self.sd_tester.write_single_ccp(566, 23)
        self.mix.sd_tester.reset_bgm()
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.check_ResvSupChrgThermSwt_sts(0,0)
        sleep(1)
        self.soa.set_SetCloudBmsStrategyConfig_req(0)
        self.bus_comm.check_ResvSupChrgThermSwt_sts(0,1)
        sleep(1)
        self.soa.set_SetCloudBmsStrategyConfig_req(1)
        for i in range(7):
            self.bus_comm.check_ResvSupChrgThermSwt_sts(1,1)
             
    @allure.title("接收云端SOC动态修正权重")
    @pytest.mark.full
    @pytest.mark.test1126
    def test_caseid_1993180(self):
        self.sd_tester.write_single_ccp(566, 16)
        self.mix.sd_tester.reset_bgm()
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.check_ResvSupChrgThermSwt_sts(0,0)
        sleep(1)
        self.soa.set_SetCloudBmsStrategyConfig_req(1)
        self.bus_comm.check_ResvSupChrgThermSwt_sts(0,0)

    @allure.title("集度私桩_未插枪_设置预约充电（交流默认值）_设置预约成功")
    @pytest.mark.full
    def test_caseid_1992989_1992991(self):
        self.mix.clean_soa_all()
        self.bus_comm.set_charge_target_soc_value(value=100.0)
        self.bus_comm.set_charging_sts(sts=ChargingSts.Default)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        time1,time2 = self.mix.get_default_time()
        sleep(10)
        self.soa.response_to_GetBookChargingInfo_req(source=HV_SourceId.kDefault,reqSts=ACBookChargingReqSts.kDefault,workSts=ACBookChargingWorkSts.kBookStsDefault,
                                                    startTime=time1, endTime=time2, repeatType=CoolgReq.Off,isToTargetSOCStop=False)
        sleep(1)
        self.soa.response_to_GetDisplayBookChargingInfo_req(type=DisplayBookChargingType.kNoDisplay,startTime=[2236,13,32,24,60,60],endTime=[2236,13,32,24,60,60])
        self.soa.set_GetVehicleTimeInfo_req(3)
        nowtime = (int(datetime.datetime.now().timestamp())//60) * 60
        logger.info(f"nowtime:{nowtime}")
        self.bus_comm.set_JiDUCharging(isAConnect=True, isPrivate=False)
        self.bus_comm.set_charge_target_soc_value(value=100.0)
        self.soa.set_SetACBookCharging_req(type=CommandType.kDefault, source=HV_SourceId.kFota, startTime=nowtime + 5*60, endTime=0, repeatType=CoolgReq.Off, isToTargetSOCStop=True)
        sleep(1)
        self.soa.set_SetACBookCharging_req(type=CommandType.kOn, source=HV_SourceId.kFota, startTime=nowtime + 5*60, endTime=0, repeatType=CoolgReq.Off, isToTargetSOCStop=True)
        sleep(1)
        self.bus_comm.set_BookCharge_SetResponse(BookChargeSetResponse=BookChargeSetResponse.Success)
        self.soa.event_to_BookChargingInfo(source=HV_SourceId.kFota,reqSts=ACBookChargingReqSts.kBookActive,workSts=ACBookChargingWorkSts.kBookStsStandby,
                                                     startTime=nowtime + 5*60, endTime=0, repeatType=CoolgReq.Off,isToTargetSOCStop=True)
        otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(nowtime+5*60))
        aa = [int(item) for item in otherStyleTime.split("_")]
        logger.info(f"aa:{aa}")
        self.soa.response_to_GetDisplayBookChargingInfo_req(type=DisplayBookChargingType.kAC,startTime=aa,endTime=[2236,13,32,24,60,60])
        sleep(1)
        self.bus_comm.check_BookChrgnActvdReq_set_BookChrgnStsFb(1,1)
        self.soa.response_to_GetBookChargingInfo_req(source=HV_SourceId.kFota,reqSts=ACBookChargingReqSts.kBookActive,workSts=ACBookChargingWorkSts.kBookStsCharging,
                                                     startTime=nowtime + 5*60, endTime=0, repeatType=CoolgReq.Off,isToTargetSOCStop=True)
        
    @allure.title("集度私桩_未插枪_取消预约充电（交流）")
    @pytest.mark.full
    def test_caseid_1992990(self):
        self.mix.clean_soa_all()
        self.bus_comm.set_charge_target_soc_value(value=100.0)
        self.bus_comm.set_charging_sts(sts=ChargingSts.Default)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        time1,time2 = self.mix.get_default_time()
        sleep(10)
        self.soa.response_to_GetBookChargingInfo_req(source=HV_SourceId.kDefault,reqSts=ACBookChargingReqSts.kDefault,workSts=ACBookChargingWorkSts.kBookStsDefault,
                                                    startTime=time1, endTime=time2, repeatType=CoolgReq.Off,isToTargetSOCStop=False)
        sleep(1)
        self.soa.response_to_GetDisplayBookChargingInfo_req(type=DisplayBookChargingType.kNoDisplay,startTime=[2236,13,32,24,60,60],endTime=[2236,13,32,24,60,60])
        self.soa.set_GetVehicleTimeInfo_req(3)
        nowtime = (int(datetime.datetime.now().timestamp())//60) * 60
        logger.info(f"nowtime:{nowtime}")
        self.bus_comm.set_JiDUCharging(isAConnect=True, isPrivate=False)
        self.bus_comm.set_charge_target_soc_value(value=100.0)
        self.soa.set_SetACBookCharging_req(type=CommandType.kDefault, source=HV_SourceId.kFota, startTime=nowtime + 5*60, endTime=0, repeatType=CoolgReq.Off, isToTargetSOCStop=True)
        sleep(1)
        self.soa.set_SetACBookCharging_req(type=CommandType.kOn, source=HV_SourceId.kFota, startTime=nowtime + 5*60, endTime=0, repeatType=CoolgReq.Off, isToTargetSOCStop=True)
        sleep(1)
        self.bus_comm.set_BookCharge_SetResponse(BookChargeSetResponse=BookChargeSetResponse.Success)
        self.soa.event_to_BookChargingInfo(source=HV_SourceId.kFota,reqSts=ACBookChargingReqSts.kBookActive,workSts=ACBookChargingWorkSts.kBookStsStandby,
                                                     startTime=nowtime + 5*60, endTime=0, repeatType=CoolgReq.Off,isToTargetSOCStop=True)
        
    @allure.title("集度私桩_预约充电成功_车桩绑定_插交流枪（预约时间未到）")
    @pytest.mark.full
    @pytest.mark.test1128
    def test_caseid_1995236(self):
        self.mix.clean_soa_all()
        self.bus_comm.set_charge_target_soc_value(value=100.0)
        self.bus_comm.set_charging_sts(sts=ChargingSts.Default)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        self.soa.set_GetVehicleTimeInfo_req(3)
        nowtime = (int(datetime.datetime.now().timestamp())//60) * 60
        logger.info(f"nowtime:{nowtime}")
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=True)
        self.bus_comm.set_charge_target_soc_value(value=100.0)
        self.soa.set_SetACBookCharging_req(type=CommandType.kDefault, source=HV_SourceId.kFota, startTime=nowtime + 5*60, endTime=0, repeatType=CoolgReq.Off, isToTargetSOCStop=True)
        sleep(1)
        self.soa.set_SetACBookCharging_req(type=CommandType.kOn, source=HV_SourceId.kFota, startTime=nowtime + 5*60, endTime=0, repeatType=CoolgReq.Off, isToTargetSOCStop=True)
        sleep(1)
        self.bus_comm.set_BookCharge_SetResponse(BookChargeSetResponse=BookChargeSetResponse.Success)
        self.soa.event_to_BookChargingInfo(source=HV_SourceId.kFota,reqSts=ACBookChargingReqSts.kBookActive,workSts=ACBookChargingWorkSts.kBookStsWait,
                                                     startTime=nowtime + 5*60, endTime=0, repeatType=CoolgReq.Off,isToTargetSOCStop=True)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=True)
        self.soa.event_to_BookChargingInfo(source=HV_SourceId.kFota,reqSts=ACBookChargingReqSts.kBookActive,workSts=ACBookChargingWorkSts.kBookStsStandby,
                                                     startTime=nowtime + 5*60, endTime=0, repeatType=CoolgReq.Off,isToTargetSOCStop=True)
        
    @allure.title("集度私桩_预约充电成功_车桩绑定_插交流枪（预约时间到）")
    @pytest.mark.full
    @pytest.mark.test1128
    def test_caseid_1995237(self):
        self.mix.clean_soa_all()
        self.bus_comm.set_charge_target_soc_value(value=100.0)
        self.bus_comm.set_charging_sts(sts=ChargingSts.Default)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        self.soa.set_GetVehicleTimeInfo_req(3)
        nowtime = (int(datetime.datetime.now().timestamp())//60) * 60
        logger.info(f"nowtime:{nowtime}")
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=True)
        self.bus_comm.set_charge_target_soc_value(value=100.0)
        self.soa.set_SetACBookCharging_req(type=CommandType.kDefault, source=HV_SourceId.kFota, startTime=nowtime + 5*60, endTime=0, repeatType=CoolgReq.Off, isToTargetSOCStop=True)
        sleep(1)
        self.soa.set_SetACBookCharging_req(type=CommandType.kOn, source=HV_SourceId.kFota, startTime=nowtime + 5*60, endTime=0, repeatType=CoolgReq.Off, isToTargetSOCStop=True)
        sleep(1)
        self.bus_comm.set_BookCharge_SetResponse(BookChargeSetResponse=BookChargeSetResponse.Success)
        self.soa.event_to_BookChargingInfo(source=HV_SourceId.kFota,reqSts=ACBookChargingReqSts.kBookActive,workSts=ACBookChargingWorkSts.kBookStsWait,
                                                     startTime=nowtime + 5*60, endTime=0, repeatType=CoolgReq.Off,isToTargetSOCStop=True)
        sleep(360)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=True)
        self.soa.event_to_BookChargingInfo(source=HV_SourceId.kFota,reqSts=ACBookChargingReqSts.kBookActive,workSts=ACBookChargingWorkSts.kBookStsCharging,
                                                     startTime=nowtime + 5*60, endTime=0, repeatType=CoolgReq.Off,isToTargetSOCStop=True)
        self.bus_comm.check_BookChrgnActvdReq_set_BookChrgnStsFb(1,1)

    @allure.title("集度私桩_未插枪_预约充电（交流）未到8小时插枪")
    @pytest.mark.full
    @pytest.mark.test1128
    def test_caseid_1999129(self):
        self.mix.clean_soa_all()
        self.bus_comm.set_charge_target_soc_value(value=100.0)
        self.bus_comm.set_charging_sts(sts=ChargingSts.Default)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        time1,time2 = self.mix.get_default_time()
        sleep(10)
        self.soa.response_to_GetBookChargingInfo_req(source=HV_SourceId.kDefault,reqSts=ACBookChargingReqSts.kDefault,workSts=ACBookChargingWorkSts.kBookStsDefault,
                                                    startTime=time1, endTime=time2, repeatType=CoolgReq.Off,isToTargetSOCStop=False)
        sleep(1)
        self.soa.response_to_GetDisplayBookChargingInfo_req(type=DisplayBookChargingType.kNoDisplay,startTime=[2236,13,32,24,60,60],endTime=[2236,13,32,24,60,60])
        self.soa.set_GetVehicleTimeInfo_req(3)
        nowtime = (int(datetime.datetime.now().timestamp())//60) * 60
        logger.info(f"nowtime:{nowtime}")
        self.bus_comm.set_JiDUCharging(isAConnect=False, isPrivate=False)
        self.bus_comm.set_charge_target_soc_value(value=100.0)
        self.soa.set_SetACBookCharging_req(type=CommandType.kDefault, source=HV_SourceId.kFota, startTime=nowtime -7*60*60, endTime=0, repeatType=CoolgReq.Off, isToTargetSOCStop=True)
        sleep(1)
        self.soa.set_SetACBookCharging_req(type=CommandType.kOn, source=HV_SourceId.kFota, startTime=nowtime -7*60*60, endTime=0, repeatType=CoolgReq.Off, isToTargetSOCStop=True)
        sleep(1)
        self.bus_comm.set_BookCharge_SetResponse(BookChargeSetResponse=BookChargeSetResponse.Success)
        self.soa.event_to_BookChargingInfo(source=HV_SourceId.kFota,reqSts=ACBookChargingReqSts.kBookActive,workSts=ACBookChargingWorkSts.kBookStsWait,
                                                     startTime=nowtime -7*60*60+86400, endTime=0, repeatType=CoolgReq.Off,isToTargetSOCStop=True)
        self.bus_comm.set_onbd_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.soa.event_to_BookChargingInfo(source=HV_SourceId.kFota,reqSts=ACBookChargingReqSts.kBookActive,workSts=ACBookChargingWorkSts.kBookStsCharging,
                                                     startTime=nowtime -7*60*60+86400, endTime=0, repeatType=CoolgReq.Off,isToTargetSOCStop=True)
        self.bus_comm.check_BookChrgnActvdReq_set_BookChrgnStsFb(1,1)
        
    @allure.title("集度私桩_未插枪_预约充电（交流）8小时后插枪")
    @pytest.mark.full
    @pytest.mark.test1128
    def test_caseid_1999130(self):
        self.mix.clean_soa_all()
        self.bus_comm.set_charge_target_soc_value(value=100.0)
        self.bus_comm.set_charging_sts(sts=ChargingSts.Default)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        time1,time2 = self.mix.get_default_time()
        sleep(10)
        self.soa.response_to_GetBookChargingInfo_req(source=HV_SourceId.kDefault,reqSts=ACBookChargingReqSts.kDefault,workSts=ACBookChargingWorkSts.kBookStsDefault,
                                                    startTime=time1, endTime=time2, repeatType=CoolgReq.Off,isToTargetSOCStop=False)
        sleep(1)
        self.soa.response_to_GetDisplayBookChargingInfo_req(type=DisplayBookChargingType.kNoDisplay,startTime=[2236,13,32,24,60,60],endTime=[2236,13,32,24,60,60])
        self.soa.set_GetVehicleTimeInfo_req(3)
        nowtime = (int(datetime.datetime.now().timestamp())//60) * 60
        logger.info(f"nowtime:{nowtime}")
        self.bus_comm.set_JiDUCharging(isAConnect=False, isPrivate=False)
        self.bus_comm.set_charge_target_soc_value(value=100.0)
        self.soa.set_SetACBookCharging_req(type=CommandType.kDefault, source=HV_SourceId.kFota, startTime=nowtime + 5*60, endTime=0, repeatType=CoolgReq.Off, isToTargetSOCStop=True)
        sleep(1)
        self.soa.set_SetACBookCharging_req(type=CommandType.kOn, source=HV_SourceId.kFota, startTime=nowtime - 8*60*60, endTime=0, repeatType=CoolgReq.Off, isToTargetSOCStop=True)
        sleep(1)
        self.bus_comm.set_BookCharge_SetResponse(BookChargeSetResponse=BookChargeSetResponse.Success)
        self.bus_comm.set_onbd_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.check_without_BookChrgnActvd_Req(0,timeout=3)

#=================================================================================================================================
@allure.feature("SOA服务接口")
@allure.story("架构基础/HighVoltageService")
@pytest.mark.test1019
class TestHighVoltageServiceFota(TestABCBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
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
        self.soa.update([
            ("ConditionCheckService", "client"),
            ("HighVoltageService", "client"),
            ("HighVoltageAppService", "client"),
            ("VehicleModeService", "client"),
            ("VehicleTimeService", "client"),
            ("SeatService", "client"),
            ("ChassisService", "client"),
            ("FotaMasterService", "server"),
            ("VehicleSetStatusService", "client")])
        self.soa.wait_for_service_reconnect("FotaMasterService_server",timeout=30)
        pass

                         
    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.soa.stop_soa()
        self.io.tcam_power_off()
        sleep(2)
        self.io.tcam_power_on()
        self.io.bgm_power_off()
        sleep(3)
        self.io.bgm_power_on()
        sleep(10)
        pass

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        self.soa.empty_all()
        pass

    def after_each_func(self, ecu):
        pass
        
   
    @allure.title("集度桩_非fota中状态列变")
    @pytest.mark.parametrize("fotaSts,charging",[(FOTAMasteSts.QUERY,ChargingSts.ACChargingEnd),(FOTAMasteSts.DOWNLOADING,ChargingSts.ACChargingEnd)
                                                 ,(FOTAMasteSts.ACTIVE,ChargingSts.ACChargingSuspend),(FOTAMasteSts.FAILED_DRIVING,ChargingSts.ACChargingEnd)
                                                 ,(FOTAMasteSts.REACH_APPOINTMENT,ChargingSts.ACChargingSuspend),(FOTAMasteSts.SUCCESSFUL,ChargingSts.ACChargingEnd)
                                                 ,(FOTAMasteSts.QUERY,ChargingSts.DCChargingEnd),(FOTAMasteSts.DOWNLOADING,ChargingSts.DCChargingEnd)
                                                 ,(FOTAMasteSts.ACTIVE,ChargingSts.DCChargingEnd),(FOTAMasteSts.FAILED_DRIVING,ChargingSts.DCChargingEnd)
                                                 ,(FOTAMasteSts.REACH_APPOINTMENT,ChargingSts.DCChargingEnd),(FOTAMasteSts.SUCCESSFUL,ChargingSts.DCChargingEnd)],
                              ids=[1989920,1990008,1990009,1990010,1990011,1990012,1990013,1990014,1990015,1990016,1990022,1990023])
    @pytest.mark.sanity
    def test_fota1(self,fotaSts,charging): 
        self.sd_tester.write_ccp(ccp={973: 2})
        self.sd_tester.diag_cancel()
        self.soa.set_SetCharging_req(req=False)
        sleep(2)  # 避免之前的case在充电中，避免初始拔枪导致季度桩丢失
        self.soa.notify_fota_status(FOTAMasteSts.IDLE)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=True)
        self.soa.set_SetChargeSoc_req(100.0)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACCharging)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        self.soa.notify_fota_status(fotaSts)
        self.bus_comm.set_charging_sts(sts=charging)
        sleep(1)
        self.bus_comm.set_battery_charger_handle_status(soc_value=87.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        self.bus_comm.set_battery_charger_handle_status(soc_value=85.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpEna)
    
    @allure.title("集度桩交流_fota中状态列变")
    @pytest.mark.parametrize("fotaSts,charging",[(FOTAMasteSts.UPDATE,ChargingSts.ACChargingEnd),(FOTAMasteSts.ROLLBACK,ChargingSts.ChargingCmpl)
                                                 ,(FOTAMasteSts.FAILED_NOT_DRIVING,ChargingSts.ACChargingSuspend),(FOTAMasteSts.FACTORY_UPDATE,ChargingSts.ACChargingEnd)],
                              ids=[1998949,1998948,1998947,1998946])
    @pytest.mark.sanity
    def test_fota9(self,fotaSts,charging): 
        self.sd_tester.write_ccp(ccp={973: 2})
        self.sd_tester.diag_cancel()
        self.soa.set_SetCharging_req(req=False)
        sleep(2)  # 避免之前的case在充电中，避免初始拔枪导致季度桩丢失
        self.soa.notify_fota_status(FOTAMasteSts.IDLE)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=True)
        self.soa.set_SetChargeSoc_req(100.0)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACCharging)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        self.soa.notify_fota_status(fotaSts)
        self.bus_comm.set_charging_sts(sts=charging)
        sleep(1)
        self.bus_comm.set_battery_charger_handle_status(soc_value=87.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        self.bus_comm.set_battery_charger_handle_status(soc_value=85.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        self.bus_comm.check_handle_status(ChrgSoftSwCtrlSt=ChrgSoftSwCtrlSt.OnOffNoReq_NoReq)
        self.soa.notify_fota_status(FOTAMasteSts.IDLE)
        self.bus_comm.check_handle_status(ChrgSoftSwCtrlSt=ChrgSoftSwCtrlSt.OnOffNoReq_On)

    @allure.title("集度桩直流_fota中状态列变")
    @pytest.mark.parametrize("fotaSts,charging",[(FOTAMasteSts.UPDATE,ChargingSts.DCChargingEnd),(FOTAMasteSts.ROLLBACK,ChargingSts.DCChargingEnd)
                                                 ,(FOTAMasteSts.FAILED_NOT_DRIVING,ChargingSts.DCChargingEnd),(FOTAMasteSts.FACTORY_UPDATE,ChargingSts.DCChargingEnd)],
                              ids=[1998945,1998944,1998943,1998942])
    @pytest.mark.sanity
    def test_fota10(self,fotaSts,charging): 
        self.sd_tester.write_ccp(ccp={973: 2})
        self.sd_tester.diag_cancel()
        self.soa.set_SetCharging_req(req=False)
        sleep(2)  # 避免之前的case在充电中，避免初始拔枪导致季度桩丢失
        self.soa.notify_fota_status(FOTAMasteSts.IDLE)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=True)
        self.soa.set_SetChargeSoc_req(100.0)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        self.soa.notify_fota_status(fotaSts)
        self.bus_comm.set_charging_sts(sts=charging)
        sleep(1)
        self.bus_comm.set_battery_charger_handle_status(soc_value=87.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        self.bus_comm.set_battery_charger_handle_status(soc_value=85.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        self.bus_comm.check_handle_status(ChrgSoftSwCtrlSt=ChrgSoftSwCtrlSt.OnOffNoReq_NoReq)
        self.soa.notify_fota_status(FOTAMasteSts.IDLE)
        self.bus_comm.check_handle_status(ChrgSoftSwCtrlSt=ChrgSoftSwCtrlSt.OnOffNoReq_On)

    @allure.title("集度桩直流_fota打断充电fota结束恢复充电")
    @pytest.mark.parametrize("fotaSts,fotaSts1",[(FOTAMasteSts.UPDATE,FOTAMasteSts.SUCCESSFUL),(FOTAMasteSts.ROLLBACK,FOTAMasteSts.SUCCESSFUL)
                                                 ,(FOTAMasteSts.FAILED_NOT_DRIVING,FOTAMasteSts.SUCCESSFUL),(FOTAMasteSts.FACTORY_UPDATE,FOTAMasteSts.SUCCESSFUL)
                                                 ,(FOTAMasteSts.ROLLBACK,FOTAMasteSts.REACH_APPOINTMENT),(FOTAMasteSts.ROLLBACK,FOTAMasteSts.FAILED_DRIVING)
                                                 ,(FOTAMasteSts.ROLLBACK,FOTAMasteSts.IDLE),(FOTAMasteSts.ROLLBACK,FOTAMasteSts.FACTORY_SUCCESSFUL)
                                                 ,(FOTAMasteSts.ROLLBACK,FOTAMasteSts.DOWNLOADING),(FOTAMasteSts.ROLLBACK,FOTAMasteSts.ACTIVE)],
                              ids=[1992596,1992597,1992598,1992599,1992600,1992601,1998966,1998967,1998968,1998969])
    @pytest.mark.sanity
    @pytest.mark.test1126
    def test_fota11(self,fotaSts,fotaSts1): 
        self.sd_tester.write_ccp(ccp={973: 2})
        self.sd_tester.diag_cancel()
        self.soa.set_SetCharging_req(req=False)
        sleep(2)  # 避免之前的case在充电中，避免初始拔枪导致季度桩丢失
        self.soa.notify_fota_status(FOTAMasteSts.IDLE)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=True)
        self.soa.set_SetChargeSoc_req(100.0)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        sleep(2)
        self.soa.notify_fota_status(fotaSts)
        sleep(2)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCChargingEnd)
        sleep(2)
        self.bus_comm.check_handle_status(ChrgSoftSwCtrlSt=ChrgSoftSwCtrlSt.OnOffNoReq_NoReq)
        self.soa.notify_fota_status(fotaSts1)
        self.bus_comm.check_handle_status(ChrgSoftSwCtrlSt=ChrgSoftSwCtrlSt.OnOffNoReq_On)

    @allure.title("集度桩交流_fota打断充电fota结束恢复充电")
    @pytest.mark.parametrize("fotaSts,fotaSts1",[(FOTAMasteSts.ROLLBACK,FOTAMasteSts.IDLE),(FOTAMasteSts.ROLLBACK,FOTAMasteSts.FACTORY_SUCCESSFUL)
                                                 ,(FOTAMasteSts.ROLLBACK,FOTAMasteSts.DOWNLOADING),(FOTAMasteSts.ROLLBACK,FOTAMasteSts.ACTIVE)
                                                 ,(FOTAMasteSts.ROLLBACK,FOTAMasteSts.FAILED_DRIVING),(FOTAMasteSts.ROLLBACK,FOTAMasteSts.REACH_APPOINTMENT)
                                                 ,(FOTAMasteSts.FACTORY_UPDATE,FOTAMasteSts.SUCCESSFUL),(FOTAMasteSts.FAILED_NOT_DRIVING,FOTAMasteSts.SUCCESSFUL)
                                                 ,(FOTAMasteSts.ROLLBACK,FOTAMasteSts.SUCCESSFUL),(FOTAMasteSts.UPDATE,FOTAMasteSts.SUCCESSFUL)],
                              ids=[1998956,1998957,1998958,1998959,1998960,11998961,1998962,1998963,1998964,1998965])
    @pytest.mark.sanity
    @pytest.mark.test1126
    def test_fota12(self,fotaSts,fotaSts1): 
        self.sd_tester.write_ccp(ccp={973: 2})
        self.sd_tester.diag_cancel()
        self.soa.set_SetCharging_req(req=False)
        sleep(2)  # 避免之前的case在充电中，避免初始拔枪导致季度桩丢失
        self.soa.notify_fota_status(FOTAMasteSts.IDLE)
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=True)
        self.soa.set_SetChargeSoc_req(100.0)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACCharging)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        sleep(2)
        self.soa.notify_fota_status(fotaSts)
        sleep(2)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACChargingSuspend)
        sleep(2)
        self.bus_comm.check_handle_status(ChrgSoftSwCtrlSt=ChrgSoftSwCtrlSt.OnOffNoReq_NoReq)
        self.soa.notify_fota_status(fotaSts1)
        self.bus_comm.check_handle_status(ChrgSoftSwCtrlSt=ChrgSoftSwCtrlSt.OnOffNoReq_On)

    @allure.title("预约充电（交流）")
    @pytest.mark.full
    def test_caseid_1995236_1995237(self):
        self.mix.clean_soa_all()
        self.bus_comm.set_charge_target_soc_value(value=100.0)
        self.bus_comm.set_charging_sts(sts=ChargingSts.Default)
        self.bus_comm.set_battery_charger_handle_status(soc_value=90.0,ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
        time1,time2 = self.mix.get_default_time()
        sleep(10)
        self.soa.response_to_GetBookChargingInfo_req(source=HV_SourceId.kDefault,reqSts=ACBookChargingReqSts.kDefault,workSts=ACBookChargingWorkSts.kBookStsDefault,
                                                    startTime=time1, endTime=time2, repeatType=CoolgReq.Off,isToTargetSOCStop=False)
        sleep(1)
        self.soa.response_to_GetDisplayBookChargingInfo_req(type=DisplayBookChargingType.kNoDisplay,startTime=[2236,13,32,24,60,60],endTime=[2236,13,32,24,60,60])
        self.soa.set_GetVehicleTimeInfo_req(3)
        nowtime = (int(datetime.datetime.now().timestamp())//60) * 60
        logger.info(f"nowtime:{nowtime}")
        self.bus_comm.set_JiDUCharging(isAConnect=True, isPrivate=False)
        self.bus_comm.set_charge_target_soc_value(value=100.0)
        self.soa.set_SetACBookCharging_req(type=CommandType.kDefault, source=HV_SourceId.kFota, startTime=nowtime + 5*60, endTime=0, repeatType=CoolgReq.Off, isToTargetSOCStop=True)
        sleep(1)
        self.soa.set_SetACBookCharging_req(type=CommandType.kOn, source=HV_SourceId.kFota, startTime=nowtime + 5*60, endTime=0, repeatType=CoolgReq.Off, isToTargetSOCStop=True)
        sleep(1)
        self.bus_comm.set_BookCharge_SetResponse(BookChargeSetResponse=BookChargeSetResponse.Success)
        self.soa.event_to_BookChargingInfo(source=HV_SourceId.kFota,reqSts=ACBookChargingReqSts.kBookActive,workSts=ACBookChargingWorkSts.kBookStsStandby,
                                                     startTime=nowtime + 5*60, endTime=0, repeatType=CoolgReq.Off,isToTargetSOCStop=True)
        otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(nowtime+5*60))
        aa = [int(item) for item in otherStyleTime.split("_")]
        logger.info(f"aa:{aa}")
        self.soa.response_to_GetDisplayBookChargingInfo_req(type=DisplayBookChargingType.kAC,startTime=aa,endTime=[2236,13,32,24,60,60])
        sleep(1)
        self.bus_comm.check_BookChrgnActvdReq_set_BookChrgnStsFb(1,1)
        self.soa.response_to_GetBookChargingInfo_req(source=HV_SourceId.kFota,reqSts=ACBookChargingReqSts.kBookActive,workSts=ACBookChargingWorkSts.kBookStsCharging,
                                                     startTime=nowtime + 5*60, endTime=0, repeatType=CoolgReq.Off,isToTargetSOCStop=True)
        
    @allure.title("预约充电_结束后预约充电_未开启执行OTA（endTime<Fotastart）")
    @pytest.mark.full
    @pytest.mark.test1128
    def test_caseid_1998950(self):
        self.mix.clean_soa_all()
        time1,time2 = self.mix.get_default_time()
        self.soa.response_to_GetBookChargingInfo_req(source=HV_SourceId.kDefault,reqSts=ACBookChargingReqSts.kDefault,workSts=ACBookChargingWorkSts.kBookStsDefault,
                                                     startTime=time1, endTime=time2, repeatType=CoolgReq.Off,isToTargetSOCStop=False)
        sleep(1)
        self.soa.set_GetVehicleTimeInfo_req(3)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=False)
        sleep(1)
        nowtime = (int(datetime.datetime.now().timestamp())//60) * 60
        logger.info(f"nowtime:{nowtime}")
        self.soa.set_SetACBookCharging_req(type=CommandType.kDefault, source=HV_SourceId.kFota, startTime=nowtime, endTime=0, repeatType=CoolgReq.Off, isToTargetSOCStop=False)
        sleep(1)
        self.soa.set_SetACBookCharging_req(type=CommandType.kOn, source=HV_SourceId.kFota, startTime=nowtime+1*60, endTime=nowtime+6*60, repeatType=CoolgReq.Off, isToTargetSOCStop=False)
        sleep(1)
        self.bus_comm.set_BookCharge_SetResponse(BookChargeSetResponse=BookChargeSetResponse.Success)
        self.soa.response_to_GetBookChargingInfo_req(source=HV_SourceId.kFota,reqSts=ACBookChargingReqSts.kBookActive,workSts=ACBookChargingWorkSts.kBookStsStandby,
                                                     startTime=nowtime +1*60, endTime=nowtime+6*60, repeatType=CoolgReq.Off,isToTargetSOCStop=False)
        otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(nowtime+1*60))
        otherStyleTime1 = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(nowtime+6*60))
        aa = [int(item) for item in otherStyleTime.split("_")]
        bb = [int(item) for item in otherStyleTime1.split("_")]
        logger.info(f"aa:{aa}")
        logger.info(f"bb:{bb}")
        self.soa.response_to_GetDisplayBookChargingInfo_req(type=DisplayBookChargingType.kAC,startTime=aa,endTime=bb)
        sleep(1)
        self.bus_comm.check_BookChrgnActvdReq_set_BookChrgnStsFb(1,1)
        self.soa.response_to_GetBookChargingInfo_req(source=HV_SourceId.kFota,reqSts=ACBookChargingReqSts.kBookActive,workSts=ACBookChargingWorkSts.kBookStsCharging,
                                                     startTime=nowtime + 1*60, endTime=nowtime+6*60, repeatType=CoolgReq.Off,isToTargetSOCStop=False)
        self.bus_comm.check_BookStopTiAchieved_set_BookChrgnStsFb(1,3,timeout=310.0)
        self.soa.response_to_GetBookChargingInfo_req(source=HV_SourceId.kFota,reqSts=ACBookChargingReqSts.kBookActive,workSts=ACBookChargingWorkSts.kBookStsFinish,
                                                     startTime=nowtime + 1*60, endTime=nowtime+6*60, repeatType=CoolgReq.Off,isToTargetSOCStop=False)
        sleep(1)