#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         : test_pedestrian_safety_ctrl.py
@Time         : 2023/05/17 08:07:44
@Author       : xiangyue.li@jiduauto.com
"""
import allure
import pytest
from time import sleep
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey
from xat_cases.legacy.bgm.case_helper.bgm_case_helper.common_interface import *


@pytest.mark.full
@allure.feature("车设车控")
@allure.story("BGM/test_safety_ctrl")
class TestSafetyCtrl(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        partner_process_check()
        self.partner = S2sBaseClass([("PassiveSafetyService", "client")])
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.ipdu.start_all_time_control()
        self.busapp.start_all_cyclic_msg()
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.diagnostic_client_sim_start()
        sleep(2)
        self.sd_tester.tester_present()
        self.com_lib = CommonInterface(
            self.tc_config,
            self.ipdu,
            self.busapp,
            self.nucapp,
            self.dk,
            self.io,
            self.sd_tester,
            self.partner,
        )

        # 设置整车碰撞状态、行人保护及安全气囊为默认值
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, "RecOfImpctCrashFrnt", 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, "RecOfImpctCrashRe", 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, "RecOfImpctCrashRollovr", 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, "RecOfImpctCrashSideLe", 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, "RecOfImpctCrashSideRi", 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, "PedProtnMsgReqForImpct", 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, "RestrntSysLampReq", 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, "RestrntSysMsgReq", 0)

    def after_class(self, ecu):
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.stop_tester_present()
        self.sd_tester.diagnostic_client_sim_close()
        self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
        self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        self.sd_tester.change_car_mode(0)

    def after_each_func(self, ecu):
        try:
            self.sd_tester.change_usage_mode(1)
            self.sd_tester.change_car_mode(0)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        super().after_each_func(ecu, start=False)

    # 1101待上库
    @pytest.mark.smoke
    @pytest.mark.verify
    @allure.title("GID-454515_被动安全_整车碰撞信号通知及恢复状态监测")
    def test_caseid_1980624(self):
        """
        获取/通知碰撞状态TRUE OR FALSE
            1.BackboneFR::SRS::SRSBackboneSignalIPdu02::RecOfImpctCrashFrnt FrontCrash::前碰撞状态
            2.BackboneFR::SRS::SRSBackboneSignalIPdu02::RecOfImpctCrashRe RearCrash::后碰撞状态
            3.BackboneFR::SRS::SRSBackboneSignalIPdu02::RecOfImpctCrashSideRi RightCrash::右碰撞状态
            4.BackboneFR::SRS::SRSBackboneSignalIPdu02::RecOfImpctCrashSideLe LeftCrash::左碰撞状态
            5.BackboneFR::SRS::SRSBackboneSignalIPdu02::RecOfImpctCrashRollovr RollOverCrash::倾翻状态
        """
        self.partner.empty_all(1)
        with allure.step("设置整车碰撞状态激活,然后check S2S 通知碰撞状态后获取碰撞状态是否一致为True"):
            self.com_lib.set_signal_and_check(
                set_signal_parameter=[
                    ("backbonefr.SrsBackBoneFr02", "RecOfImpctCrashFrnt", 1),
                    ("backbonefr.SrsBackBoneFr02", "RecOfImpctCrashRe", 1),
                    ("backbonefr.SrsBackBoneFr02", "RecOfImpctCrashRollovr", 1),
                    ("backbonefr.SrsBackBoneFr02", "RecOfImpctCrashSideLe", 1),
                    ("backbonefr.SrsBackBoneFr02", "RecOfImpctCrashSideRi", 1),
                ],
                check_s2s_event_parameter=(
                    PASSIVESAFETY_SERVICE_CLIENT,
                    "NotifyVehicleCrashStatus",
                    {
                        "crash": {
                            "RollOverCrash": True,
                            "FrontCrash": True,
                            "RearCrash": True,
                            "LeftCrash": True,
                            "RightCrash": True,
                        }
                    },
                ),
                check_service_response=(
                    PASSIVESAFETY_SERVICE_CLIENT,
                    "GetVehicleCrashStatus",
                    {},
                    {
                        "out": [
                            {
                                "RollOverCrash": True,
                                "FrontCrash": True,
                                "RearCrash": True,
                                "LeftCrash": True,
                                "RightCrash": True,
                            }
                        ]
                    },
                ),
            )
        self.partner.empty_all(1)
        with allure.step("设置整车碰撞状态恢复,然后check S2S 碰撞状态是否恢复默认值"):
            self.com_lib.set_signal_and_check(
                set_signal_parameter=[
                    ("backbonefr.SrsBackBoneFr02", "RecOfImpctCrashFrnt", 0),
                    ("backbonefr.SrsBackBoneFr02", "RecOfImpctCrashRe", 0),
                    ("backbonefr.SrsBackBoneFr02", "RecOfImpctCrashRollovr", 0),
                    ("backbonefr.SrsBackBoneFr02", "RecOfImpctCrashSideLe", 0),
                    ("backbonefr.SrsBackBoneFr02", "RecOfImpctCrashSideRi", 0),
                ],
                check_s2s_event_parameter=(
                    PASSIVESAFETY_SERVICE_CLIENT,
                    "NotifyVehicleCrashStatus",
                    {
                        "crash": {
                            "RollOverCrash": False,
                            "FrontCrash": False,
                            "RearCrash": False,
                            "LeftCrash": False,
                            "RightCrash": False,
                        }
                    },
                ),
                check_service_response=(
                    PASSIVESAFETY_SERVICE_CLIENT,
                    "GetVehicleCrashStatus",
                    {},
                    {
                        "out": [
                            {
                                "RollOverCrash": False,
                                "FrontCrash": False,
                                "RearCrash": False,
                                "LeftCrash": False,
                                "RightCrash": False,
                            }
                        ]
                    },
                ),
            )
        sleep(3)

    @pytest.mark.smoke
    @allure.title("GID-453605_被动安全_行人保护故障提示获取及通知状态监测")
    def test_caseid_1980628(self):
        """
        获取/通知行人保护状态 On OR Off,系统故障:isSysFault,系统故障有效性:isValid
        1.行人保护故障指示为默认值:BackboneFR::SRS::SRSBackboneSignalIPdu02::PedProtnMsgReqForFlt==0::NotVld1
        2.PedProtnMsgReqForFlt==1 参数isSysFault==0:False 参数isValid==1:True
        3.PedProtnMsgReqForFlt==2 参数isSysFault==1:True 参数isValid==1:True
        4.PedProtnMsgReqForFlt==0 0R 3 参数isSysFault 首次接收为默认值0 参数isValid==0:False
        """
        self.partner.empty_all(0.5)
        with allure.step(
            "校验PedProtnMsgReqForFlt==2::On 对应参数isSysFault==1:True 参数isValid==1:True"
        ):
            self.com_lib.set_signal_and_check(
                set_signal_parameter=(
                    "backbonefr.SrsBackBoneFr02",
                    "PedProtnMsgReqForFlt",
                    2,
                ),
                check_s2s_event_parameter=(
                    PASSIVESAFETY_SERVICE_CLIENT,
                    "PedestrianProtectionWarning",
                    {"warn": {"isSysFault": True, "isValid": True}},
                ),
                check_service_response=(
                    PASSIVESAFETY_SERVICE_CLIENT,
                    "GetPedestrianProtectionWarning",
                    {},
                    {"out": {"isSysFault": True, "isValid": True}},
                ),
            )
        self.partner.empty_all(0.5)
        with allure.step(
            "校验PedProtnMsgReqForFlt==1 对应参数isSysFault==0:False 参数isValid==1:True"
        ):
            self.com_lib.set_signal_and_check(
                set_signal_parameter=(
                    "backbonefr.SrsBackBoneFr02",
                    "PedProtnMsgReqForFlt",
                    1,
                ),
                check_s2s_event_parameter=(
                    PASSIVESAFETY_SERVICE_CLIENT,
                    "PedestrianProtectionWarning",
                    {"warn": {"isSysFault": False, "isValid": True}},
                ),
                check_service_response=(
                    PASSIVESAFETY_SERVICE_CLIENT,
                    "GetPedestrianProtectionWarning",
                    {},
                    {"out": {"isSysFault": False, "isValid": True}},
                ),
            )
        self.partner.empty_all(0.5)
        with allure.step(
            "校验PedProtnMsgReqForFlt==0 0R 3 对应参数isSysFault 首次接收为默认值0 参数isValid==0:False"
        ):
            self.com_lib.set_signal_and_check(
                set_signal_parameter=(
                    "backbonefr.SrsBackBoneFr02",
                    "PedProtnMsgReqForFlt",
                    0,
                ),
                check_s2s_event_parameter=(
                    PASSIVESAFETY_SERVICE_CLIENT,
                    "PedestrianProtectionWarning",
                    {"warn": {"isSysFault": False, "isValid": False}},
                ),
                check_service_response=(
                    PASSIVESAFETY_SERVICE_CLIENT,
                    "GetPedestrianProtectionWarning",
                    {},
                    {"out": {"isSysFault": False, "isValid": False}},
                ),
            )

        sleep(5)

    @pytest.mark.smoke
    @allure.title("GID-453605_被动安全_行人保护系统提示获取及通知状态监测")
    def test_caseid_1980633(self):
        """
        获取/通知行人保护系统提示 On OR Off,碰撞报警:isImpactWarning
        1.通知行人保护系统提示为默认值：BackboneFR::SRS::SRSBackboneSignalIPdu02::PedProtnMsgReqForImpct==0::off
        2.碰撞报警:isImpactWarning对应PedProtnMsgReqForImpct
        """
        self.partner.empty_all(1)
        with allure.step(
            "校验行人保护系统提示状态PedProtnMsgReqForImpct==1:On 对应isImpactWarning==True"
        ):
            self.com_lib.set_signal_and_check(
                set_signal_parameter=(
                    "backbonefr.SrsBackBoneFr02",
                    "PedProtnMsgReqForImpct",
                    1,
                ),
                check_s2s_event_parameter=(
                    PASSIVESAFETY_SERVICE_CLIENT,
                    "PedestrianProtectionWarning",
                    {"warn": {"isImpactWarning": True}},
                    "timeout=3",
                ),
                check_service_response=(
                    PASSIVESAFETY_SERVICE_CLIENT,
                    "GetPedestrianProtectionWarning",
                    {},
                    {"out": {"isImpactWarning": True}},
                    "timeout=3",
                ),
            )
        with allure.step(
            "校验行人保护系统提示状态PedProtnMsgReqForImpct==0:Off 对应isImpactWarning==False"
        ):
            self.com_lib.set_signal_and_check(
                set_signal_parameter=(
                    "backbonefr.SrsBackBoneFr02",
                    "PedProtnMsgReqForImpct",
                    0,
                ),
                check_s2s_event_parameter=(
                    PASSIVESAFETY_SERVICE_CLIENT,
                    "PedestrianProtectionWarning",
                    {"warn": {"isImpactWarning": False}},
                    "timeout=3",
                ),
                check_service_response=(
                    PASSIVESAFETY_SERVICE_CLIENT,
                    "GetPedestrianProtectionWarning",
                    {},
                    {"out": {"isImpactWarning": False}},
                    "timeout=3",
                ),
            )

        sleep(3)

    @allure.title("GID-451557_被动安全_InActive模式下获取和通知安全气囊故障状态及告警灯状态")
    @pytest.mark.smoke
    def test_caseid_1980998(self):
        """
        获取/通知行人保护系统提示 On OR Off,碰撞报警:isImpactWarning
        1.troubleLightStatus::气囊故障灯@value(0)::kLampOff（Default）,@value(1)::kUnknown,@value(2)::kLampFlash,@value(3)::kLampOn
        2.isFault::气囊故障状态（文言提示）	0 = FALSE（无故障）（Defalut）1 = TRUE（有故障）
        3.isValid::气囊故障状态有效性（文言提示）	0 = FALSE,1 = TRUE（Defalut）
        5.气囊故障灯::troubleLightStatus==BackboneFR::SRS::SRSBackboneSignalIPdu02::RestrntSysLampReq
        6.RestrntSysMsgReq== 0  OR 3 = NoYesCrit1_NotVld1 OR NoYesCrit1_NotVld2对应气囊故障状态::isFault::Last Value（若首次接收，为默认值）对应气囊故障状态有效性::isValid==FALSE
        7.RestrntSysMsgReq== 1 = OnOffCrit1_Off	对应气囊故障状态::isFault==FALSE对应气囊故障状态有效性::isValid==TRUE
        8.RestrntSysMsgReq== 2 = OnOffCrit1_On	对应气囊故障状态::isFault==TRUE对应气囊故障状态有效性::isValid==TRUE
        """
        self.partner.empty_all(1)
        with allure.step("设置前置条件：UsgMode==2"):
            self.sd_tester.change_usage_mode(1)
        with allure.step("监控安全气囊无故障&&故障灯关闭获取后通知"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, "RestrntSysLampReq", 0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, "RestrntSysMsgReq", 1)
            self.partner.ck_s2s_event(
                PASSIVESAFETY_SERVICE_CLIENT,
                "AirbagWarning",
                {"warn": {"troubleLightStatus": 0, "isFault": False, "isValid": True}},
                timeout=3,
            )
            self.partner.send_request_and_ck_resp(
                PASSIVESAFETY_SERVICE_CLIENT,
                "GetAirbagWarning",
                {},
                {"out": {"troubleLightStatus": 0, "isFault": False, "isValid": True}},
                timeout=3,
            )
        with allure.step("监控安全气囊无故障&&故障灯关闭首次获取默认值isFault::Last Value（若首次接收，为默认值）	"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, "RestrntSysLampReq", 0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, "RestrntSysMsgReq", 3)
            self.partner.ck_s2s_event(
                PASSIVESAFETY_SERVICE_CLIENT,
                "AirbagWarning",
                {"warn": {"troubleLightStatus": 0, "isFault": False, "isValid": False}},
                timeout=3,
            )
            self.partner.send_request_and_ck_resp(
                PASSIVESAFETY_SERVICE_CLIENT,
                "GetAirbagWarning",
                {},
                {"out": {"troubleLightStatus": 0, "isFault": False, "isValid": False}},
                timeout=3,
            )
        sleep(3)

    @allure.title("GID-451557_被动安全_Covenience模式下获取和通知安全气囊故障状态及告警灯状态")
    @pytest.mark.smoke
    def test_caseid_1980997(self):
        self.partner.empty_all(1)
        with allure.step("设置前置条件：UsgMode==2"):
            self.sd_tester.change_usage_mode(2)
        with allure.step("监控安全气囊无故障&&故障灯关闭"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, "RestrntSysLampReq", 2)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, "RestrntSysMsgReq", 2)
            self.partner.ck_s2s_event(
                PASSIVESAFETY_SERVICE_CLIENT,
                "AirbagWarning",
                {"warn": {"troubleLightStatus": 2, "isFault": True, "isValid": True}},
                timeout=5,
            )
            self.partner.send_request_and_ck_resp(
                PASSIVESAFETY_SERVICE_CLIENT,
                "GetAirbagWarning",
                {},
                {"out": {"troubleLightStatus": 2, "isFault": True, "isValid": True}},
                timeout=5,
            )
        with allure.step("监控安全气囊故障恢复默认值，isFault::Last Value（若首次接收，为默认值）"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, "RestrntSysLampReq", 0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, "RestrntSysMsgReq", 0)
            self.partner.ck_s2s_event(
                PASSIVESAFETY_SERVICE_CLIENT,
                "AirbagWarning",
                {"warn": {"troubleLightStatus": 0, "isFault": True, "isValid": False}},
                timeout=5,
            )
            self.partner.send_request_and_ck_resp(
                PASSIVESAFETY_SERVICE_CLIENT,
                "GetAirbagWarning",
                {},
                {"out": {"troubleLightStatus": 0, "isFault": True, "isValid": False}},
                timeout=5,
            )
        sleep(2)

    @allure.title("GID-451557_被动安全_Drving模式下安全气囊故障灯5S计时器状态监测")
    @pytest.mark.smoke
    def test_caseid_1980999(self):
        """
        如果5s计时内，VehModMngtGlbSafe1UsgModSts维持在Active/Driving，参数troubleLightStatus =@value(0)kLampOff；
        参数troubleLightStatus = 信号RestrntSysLampReq
        """
        self.partner.empty_all(1)
        with allure.step("设置前置条件：UsgMode==2"):
            self.sd_tester.change_usage_mode(2)
            sleep(1)
        with allure.step("监控5S计时器内气囊报警灯Off状态"):
            self.sd_tester.change_usage_mode(13)
            sleep(1)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, "RestrntSysLampReq", 2)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, "RestrntSysMsgReq", 2)
            self.partner.ck_s2s_event(
                PASSIVESAFETY_SERVICE_CLIENT,
                "AirbagWarning",
                {"warn": {"troubleLightStatus": 0, "isFault": True, "isValid": True}},
                timeout=5,
            )
            self.partner.send_request_and_ck_resp(
                PASSIVESAFETY_SERVICE_CLIENT,
                "GetAirbagWarning",
                {},
                {"out": {"troubleLightStatus": 0, "isFault": True, "isValid": True}},
                timeout=5,
            )
        with allure.step("计时器超过5S安全气囊故障灯正常告警"):
            sleep(4)
            self.partner.ck_s2s_event(
                PASSIVESAFETY_SERVICE_CLIENT,
                "AirbagWarning",
                {"warn": {"troubleLightStatus": 2, "isFault": True, "isValid": True}},
                timeout=5,
            )
            self.partner.send_request_and_ck_resp(
                PASSIVESAFETY_SERVICE_CLIENT,
                "GetAirbagWarning",
                {},
                {"out": {"troubleLightStatus": 2, "isFault": True, "isValid": True}},
                timeout=5,
            )
            sleep(2)
