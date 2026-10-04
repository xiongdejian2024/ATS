# -*- coding: utf-8 -*-


import os
import sys
import time
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
import pytest
import allure
import threading
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.bus_app import BusApp
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.bgm.VehicleControl.case_helper.common_lib_bgm import *
from xat_cases.legacy.bgm.VehicleControl.case_helper.parse_excel_bgm import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_cases.legacy.bgm.case_helper.bgm_case_helper.common_interface import *


@allure.feature("网络管理")
@allure.story("网络PNC路由测试")
class TestExample(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        partner_process_check()
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.partner = S2sBaseClass(
            [
                ("CentralLockService", "client"),
                ("KeyService", "client"),
                ("DoorService", "client"),
                ("SteerWheelService", "client"),
            ]
        )
        self.ipdu.start_all_time_control()
        self.busapp.start_all_cyclic_msg()
        sleep(2)
        self.partner.send_method_request(
            "KeyService_client", "SetConfigInfo", {"infos": [{"key": 5, "value": 0}]}
        )
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set_vehspd(0.0)
        sleep(1)
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)

        # 设置高压继电器状态为闭合
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr06,
            "HvSysRlyStsHvSysRlySts",
            1,
        )
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.diagnostic_client_sim_start()
        self.sd_tester.write_multi_ccp({186: 0x2, 13: 0x4})
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

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        try:
            self.sd_tester.change_usage_mode(1)
            self.sd_tester.change_car_mode(0)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        self.dk.stop_listen_dk_bgm_response()
        self.sd_tester.diagnostic_client_sim_close()
        self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
        self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.sd_tester.change_usage_mode(1, do_assert=0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr06, "HvSysRlyStsHvSysRlySts", 1)
        sleep(0.5)

        self.partner.empty_all()
        if self.check_cenlock_sts(0x01)[0] != True:
            self.unlock_by_nfc()

    def after_each_func(self, ecu):
        self.ipdu.set_vehspd(0.0)
        # 设置:Carmode 设置为 Normal;
        self.sd_tester.change_usage_mode(1, do_assert=0)
        sleep(0.5)
        self.ipdu.reset_check_results()
        if ecu.get("testresult") != "Pass":
            logger.info("case失败，需等待5s让环境恢复")
            sleep(5)
        else:
            sleep(3)  # 避免防玩

        super().after_each_func(ecu, start=False)

    def set_centrllock_pre_condition(self):
        self.ipdu.pause_bus_send("chassiscan1")
        self.ipdu.pause_bus_send("chassiscan2")
        self.ipdu.pause_bus_send("passivesafetycan")
        self.ipdu.pause_ecu_send("connectivitycanfd", "DRMFL")
        self.ipdu.pause_ecu_send("connectivitycanfd", "DRMFR")
        self.ipdu.pause_ecu_send("connectivitycanfd", "DRMRL")
        self.ipdu.pause_ecu_send("connectivitycanfd", "DRMRR")
        self.ipdu.pause_ecu_send("connectivitycanfd", "TCAM")
        self.ipdu.stop_send_pdu("connectivitycanfd", 0x10)
        self.ipdu.stop_send_pdu("connectivitycanfd", 0x40)
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        sleep(1)
        self.dk.set_cenlock_sts(0x1)

    def check_cenlock_sts(self, exp_sts):
        return self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr12,
            "LockgCenStsLockSt_2_VgmConnSignalIPdu12",
            exp_sts,
            timeout=3,
            do_assert=False,
        )

    def start_thread_check_signal(self, msg_obj, signal, observe_time):
        self.ipdu.check_signal(msg_obj, signal, observe_time)

    def check_signal_alway_is(self, msg, signal, value, obv_time=5):
        result_ori = self.ipdu.check_signal(msg, signal, timeout=obv_time)
        logger.info("result_original {}".format(result_ori))
        result = check_all_value_is(result_ori, value)
        assert result

    # 中控锁系统状态_NFC解锁"
    def unlock_by_nfc(self):
        self.set_centrllock_pre_condition()
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        sleep(0.5)
        self.dk.send_nfc_cmd()
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 1),
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsTrigSrc", 12),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(1)

    # 中控锁系统状态_NFC闭锁"
    def lock_by_nfc(self):
        self.set_centrllock_pre_condition()
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        sleep(0.5)
        self.dk.send_nfc_cmd()
        # self.ck_CentralLockStatusInfo(3, 12)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 3),
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsTrigSrc", 12),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    # @allure.title("Normal模式手动控制方向盘加热打开_1档")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    #     name="Normal模式手动控制方向盘加热打开_1档",
    # )
    # @pytest.mark.smoke
    # @pytest.mark.verify
    # def test_caseid_1960106(self):
    #     with allure.step("设置初始化条件"):
    #         self.com_lib.set_common_precontion(usage_mode=13)
    #         # self.partner.send_method_request("SteerWheelService_client", "SetHeat", {"status": 0})
    #         # time.sleep(3)

    #     self.com_lib.send_s2s_request_and_check(
    #         ("SteerWheelService", "SetHeat", {"status": 1}),
    #         check_signal_parameter=[
    #             ("backbonefr.CemBackBoneFr19", "SteerWhlHeatgLvlSts", 1),
    #             ("connectivitycanfd.VgmConnFr03", "SteerWhlHeatgAvlSts", 1),
    #         ],
    #         check_service_response=("SteerWheelService", "GetHeat", {}, {"out": {"level":1}}),
    #     )
    #     sleep(3)

    # @allure.title("Normal模式手动控制方向盘加热打开_2档")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/1892742?projectId=46",
    #     name="Normal模式手动控制方向盘加热打开_2档",
    # )
    # @pytest.mark.smoke
    # def test_caseid_1960110(self):
    #     with allure.step("设置初始化条件"):
    #         self.com_lib.set_common_precontion(usage_mode=13)
    #         # self.partner.send_method_request("SteerWheelService_client", "SetHeat", {"status": 0})
    #         # time.sleep(3)

    #     self.com_lib.send_s2s_request_and_check(
    #         ("SteerWheelService", "SetHeat", {"status": 2}),
    #         check_signal_parameter=[
    #             ("backbonefr.CemBackBoneFr19", "SteerWhlHeatgLvlSts", 2),
    #             ("connectivitycanfd.VgmConnFr03", "SteerWhlHeatgAvlSts", 1),
    #         ],
    #         check_service_response=("SteerWheelService", "GetHeat", {}, {"out": {"level":2}}),
    #     )
    #     sleep(3)

    # @allure.title("Normal模式手动控制方向盘加热打开_3档")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46",
    #     name="Normal模式手动控制方向盘加热打开_3档",
    # )
    # @pytest.mark.smoke
    # def test_caseid_1960111(self):
    #     with allure.step("设置初始化条件"):
    #         self.com_lib.set_common_precontion(usage_mode=13)

    #     self.com_lib.send_s2s_request_and_check(
    #         ("SteerWheelService", "SetHeat", {"status": 3}),
    #         check_signal_parameter=[
    #             ("backbonefr.CemBackBoneFr19", "SteerWhlHeatgLvlSts", 3),
    #             ("connectivitycanfd.VgmConnFr03", "SteerWhlHeatgAvlSts", 1),
    #         ],
    #         check_service_response=("SteerWheelService", "GetHeat", {}, {"out": {"level":3}}),
    #     )
    #     sleep(3)

    @allure.title("Normal模式手动控制方向盘加热关闭")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892744?projectId=46",
        name="Normal模式手动控制方向盘加热关闭",
    )
    @pytest.mark.smoke
    def test_caseid_1960112(self):
        with allure.step("设置初始化条件"):
            self.com_lib.set_common_precontion(usage_mode=13)
            self.partner.send_method_request(
                "SteerWheelService_client", "SetHeat", {"status": 3}
            )
            sleep(1)

        self.com_lib.send_s2s_request_and_check(
            ("SteerWheelService", "SetHeat", {"status": 0}),
            check_signal_parameter=[
                ("backbonefr.CemBackBoneFr19", "SteerWhlHeatgLvlSts", 0),
                ("connectivitycanfd.VgmConnFr03", "SteerWhlHeatgAvlSts", 2),
            ],
            check_service_response=("SteerWheelService", "GetHeat", {}, {"out": {"level":0}}),
        )

    @allure.title("Dyno模式调节方向盘（向上）")  # Pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1753869?projectId=46",
        name="调节方向盘",
    )
    @pytest.mark.full
    def test_caseid_1960114(self):
        with allure.step("设置初始化条件"):
            self.com_lib.set_common_precontion(usage_mode=13, car_mode=5)

        self.com_lib.send_s2s_request_and_check(
            ("SteerWheelService_client", "StartMoveDirection", {"direction": 2}),
            check_signal_parameter=[
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtUpSts", 1),
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtDwnSts", 0),
            ],
        )
        sleep(3)

    @allure.title("Dyno模式调节方向盘（向下）")  # Pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1753869?projectId=46",
        name="调节方向盘",
    )
    @pytest.mark.full
    def test_caseid_1960137(self):
        with allure.step("设置初始化条件"):
            self.com_lib.set_common_precontion(usage_mode=13, car_mode=5)

        self.com_lib.send_s2s_request_and_check(
            ("SteerWheelService_client", "StartMoveDirection", {"direction": 5}),
            check_signal_parameter=[
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtDwnSts", 1),
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtUpSts", 0),
            ],
        )
        sleep(3)

    @allure.title("Dyno模式调节方向盘（向前）")  # Pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1753869?projectId=46",
        name="调节方向盘",
    )
    @pytest.mark.full
    def test_caseid_1960135(self):
        with allure.step("设置初始化条件"):
            self.com_lib.set_common_precontion(usage_mode=13, car_mode=5)

        self.com_lib.send_s2s_request_and_check(
            ("SteerWheelService_client", "StartMoveDirection", {"direction": 0}),
            check_signal_parameter=[
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtFwdSts", 1),
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtDwnSts", 0),
            ],
        )
        sleep(3)

    @allure.title("Dyno模式调节方向盘（向后）")  # Pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1753869?projectId=46",
        name="调节方向盘",
    )
    @pytest.mark.full
    def test_caseid_1960136(self):
        with allure.step("设置初始化条件"):
            self.com_lib.set_common_precontion(usage_mode=13, car_mode=5)

        self.com_lib.send_s2s_request_and_check(
            ("SteerWheelService_client", "StartMoveDirection", {"direction": 3}),
            check_signal_parameter=[
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtBackSts", 1),
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtDwnSts", 0),
            ],
        )
        sleep(3)

    @allure.title("Normal模式调节方向盘（向上）")  # Pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1753869?projectId=46",
        name="调节方向盘",
    )
    @pytest.mark.smoke
    def test_caseid_1960121(self):
        with allure.step("设置初始化条件"):
            self.com_lib.set_common_precontion(usage_mode=2)

        self.com_lib.send_s2s_request_and_check(
            ("SteerWheelService_client", "StartMoveDirection", {"direction": 2}),
            check_signal_parameter=[
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtUpSts", 1),
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtDwnSts", 0),
            ],
        )
        sleep(3)

    @allure.title("Normal模式调节方向盘（向下）")  # Pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1753869?projectId=46",
        name="调节方向盘",
    )
    @pytest.mark.smoke
    def test_caseid_1960122(self):
        with allure.step("设置初始化条件"):
            self.com_lib.set_common_precontion(usage_mode=2)

        self.com_lib.send_s2s_request_and_check(
            ("SteerWheelService_client", "StartMoveDirection", {"direction": 5}),
            check_signal_parameter=[
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtDwnSts", 1),
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtUpSts", 0),
            ],
        )
        sleep(3)

    @allure.title("Normal模式调节方向盘（向前）")  # Pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1753869?projectId=46",
        name="调节方向盘",
    )
    @pytest.mark.smoke
    def test_caseid_1960120(self):
        with allure.step("设置初始化条件"):
            self.com_lib.set_common_precontion(usage_mode=2)

        self.com_lib.send_s2s_request_and_check(
            ("SteerWheelService_client", "StartMoveDirection", {"direction": 0}),
            check_signal_parameter=[
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtFwdSts", 1),
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtDwnSts", 0),
            ],
        )
        sleep(3)

    @allure.title("Normal模式调节方向盘（向后）")  # Pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1753869?projectId=46",
        name="调节方向盘",
    )
    @pytest.mark.smoke
    def test_caseid_1960109(self):
        with allure.step("设置初始化条件"):
            self.com_lib.set_common_precontion(usage_mode=2)

        self.com_lib.send_s2s_request_and_check(
            ("SteerWheelService_client", "StartMoveDirection", {"direction": 3}),
            check_signal_parameter=[
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtBackSts", 1),
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtDwnSts", 0),
            ],
        )
        sleep(3)

    @allure.title("Transport模式调节方向盘（向上）")  # Pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1753869?projectId=46",
        name="调节方向盘",
    )
    @pytest.mark.smoke
    def test_caseid_1960127(self):
        with allure.step("设置初始化条件"):
            self.com_lib.set_common_precontion(usage_mode=13, car_mode=1)
        self.com_lib.send_s2s_request_and_check(
            ("SteerWheelService_client", "StartMoveDirection", {"direction": 2}),
            check_signal_parameter=[
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtUpSts", 1),
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtDwnSts", 0),
            ],
        )
        sleep(3)

    @allure.title("Transport模式调节方向盘（向下）")  # Pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1753869?projectId=46",
        name="调节方向盘",
    )
    @pytest.mark.smoke
    def test_caseid_1960115(self):
        with allure.step("设置初始化条件"):
            self.com_lib.set_common_precontion(usage_mode=13, car_mode=1)

        self.com_lib.send_s2s_request_and_check(
            ("SteerWheelService_client", "StartMoveDirection", {"direction": 5}),
            check_signal_parameter=[
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtUpSts", 0),
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtDwnSts", 1),
            ],
        )
        sleep(3)

    @allure.title("Transport模式调节方向盘（向前）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1753869?projectId=46",
        name="调节方向盘",
    )
    @pytest.mark.smoke
    def test_caseid_1960126(self):
        with allure.step("设置初始化条件"):
            self.com_lib.set_common_precontion(usage_mode=13, car_mode=1)
        self.com_lib.send_s2s_request_and_check(
            ("SteerWheelService_client", "StartMoveDirection", {"direction": 0}),
            check_signal_parameter=[
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtFwdSts", 1),
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtDwnSts", 0),
            ],
        )
        sleep(3)

    @allure.title("Transport模式调节方向盘（向后）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1753869?projectId=46",
        name="调节方向盘",
    )
    @pytest.mark.smoke
    def test_caseid_1960125(self):
        with allure.step("设置初始化条件"):
            self.com_lib.set_common_precontion(usage_mode=13, car_mode=1)
        self.com_lib.send_s2s_request_and_check(
            ("SteerWheelService_client", "StartMoveDirection", {"direction": 3}),
            check_signal_parameter=[
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtBackSts", 1),
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtDwnSts", 0),
            ],
        )
        sleep(3)

    @allure.title("Factory模式调节方向盘（向上）")  # Pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1753869?projectId=46",
        name="调节方向盘",
    )
    @pytest.mark.smoke
    def test_caseid_1960131(self):
        with allure.step("设置初始化条件"):
            self.com_lib.set_common_precontion(usage_mode=13, car_mode=2)
        self.com_lib.send_s2s_request_and_check(
            ("SteerWheelService_client", "StartMoveDirection", {"direction": 2}),
            check_signal_parameter=[
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtUpSts", 1),
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtDwnSts", 0),
            ],
        )
        sleep(3)

        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)


    @allure.title("Factory模式调节方向盘（向下）")  # Pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1753869?projectId=46",
        name="调节方向盘",
    )
    @pytest.mark.smoke
    def test_caseid_1960132(self):
        with allure.step("设置初始化条件"):
            self.com_lib.set_common_precontion(usage_mode=13, car_mode=2)
        self.com_lib.send_s2s_request_and_check(
            ("SteerWheelService_client", "StartMoveDirection", {"direction": 5}),
            check_signal_parameter=[
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtDwnSts", 1),
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtUpSts", 0),
            ],
        )
        sleep(3)

    @allure.title("Factory模式调节方向盘（向前）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1753869?projectId=46",
        name="调节方向盘",
    )
    @pytest.mark.smoke
    def test_caseid_1960113(self):
        with allure.step("设置初始化条件"):
            self.com_lib.set_common_precontion(usage_mode=13, car_mode=2)
        self.com_lib.send_s2s_request_and_check(
            ("SteerWheelService_client", "StartMoveDirection", {"direction": 0}),
            check_signal_parameter=[
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtFwdSts", 1),
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtDwnSts", 0),
            ],
        )
        sleep(3)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)


    @allure.title("Factory模式调节方向盘（向后）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1753869?projectId=46",
        name="调节方向盘",
    )
    @pytest.mark.smoke
    def test_caseid_1960130(self):
        with allure.step("设置初始化条件"):
            self.com_lib.set_common_precontion(usage_mode=13, car_mode=2)
        self.com_lib.send_s2s_request_and_check(
            ("SteerWheelService_client", "StartMoveDirection", {"direction": 3}),
            check_signal_parameter=[
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtBackSts", 1),
                ("cem_lin4.CemCem_Lin4Fr06", "SteerAdjSwtDwnSts", 0),
            ],
        )
        sleep(3)

        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)


    @allure.title("Transport模式方向盘加热无法打开")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
        name="Transport模式方向盘加热无法打开",
    )
    @pytest.mark.full
    def test_caseid_1960117(self):
        with allure.step("设置初始化条件"):
            self.com_lib.set_common_precontion(usage_mode=13, car_mode=1)
            self.partner.send_method_request(
                "SteerWheelService_client", "SetHeat", {"status": 0}
            )
            time.sleep(3)

        self.com_lib.send_s2s_request_and_check(
            ("SteerWheelService_client", "SetHeat", {"status": 1}),
            check_signal_parameter=[
                ("backbonefr.CemBackBoneFr19", "SteerWhlHeatgLvlSts", 0),
                ("connectivitycanfd.VgmConnFr03", "SteerWhlHeatgAvlSts", 2),
            ],
            check_service_response=(
                "SteerWheelService_client",
                "GetHeat",
                {},
                {"out": {"level":0}},
            ),
        )
        sleep(3)


    @allure.title("Factory模式方向盘加热无法打开")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
        name="Factory模式方向盘加热无法打开",
    )
    @pytest.mark.full
    def test_caseid_1960118(self):
        with allure.step("设置初始化条件"):
            self.com_lib.set_common_precontion(usage_mode=13, car_mode=2)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr06, "HvSysRlyStsHvSysRlySts", 1)
            self.partner.send_method_request(
                "SteerWheelService_client", "SetHeat", {"status": 0}
            )
            time.sleep(3)

        self.com_lib.send_s2s_request_and_check(
            ("SteerWheelService_client", "SetHeat", {"status": 1}),
            check_signal_parameter=[
                ("backbonefr.CemBackBoneFr19", "SteerWhlHeatgLvlSts", 0),
                ("connectivitycanfd.VgmConnFr03", "SteerWhlHeatgAvlSts", 2),
            ],
            check_service_response=(
                "SteerWheelService_client",
                "GetHeat",
                {},
                {"out": {"level":0}},
            ),
        )
        sleep(3)
        

    # @allure.title("方向盘加热打开后锁车，加热关闭")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    #     name="方向盘加热打开后锁车，加热关闭",
    # )
    # @pytest.mark.smoke
    # def test_caseid_1960107(self):
    #     with allure.step("设置初始化条件"):
    #         self.com_lib.set_common_precontion(usage_mode=2, car_mode=0)
    #         self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr06, "HvSysRlyStsHvSysRlySts", 1)
    #     self.com_lib.send_s2s_request_and_check(
    #         ("SteerWheelService_client", "SetHeat", {"status": 3}),
    #         check_service_response=(
    #             "SteerWheelService_client",
    #             "GetHeat",
    #             {},
    #             {"out": {"level":3}},
    #         ),
    #     )

    #     with allure.step("NFC闭锁"):
    #         self.lock_by_nfc()
    #         time.sleep(1)

    #     with allure.step("检查调用获取GetHeat接口"):
    #         self.partner.send_request_and_ck_resp(
    #             "SteerWheelService_client", "GetHeat", {}, {"out": {"level":0}}, timeout=3
    #         )

    #     with allure.step(f"检测当前是否SteerWhlHeatgLvlSts=0"):
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr19,
    #             "SteerWhlHeatgLvlSts",
    #             0,
    #         )
    #     with allure.step(f"检测当前是否SteerWhlHeatgLvlSts=2"):
    #         self.ipdu.check(
    #             self.ipdu.connectivitycanfd.VgmConnFr03,
    #             "SteerWhlHeatgAvlSts",
    #             2,
    #         )
    #     sleep(3)

    @allure.title("远程控制方向盘加热")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
        name="远程控制方向盘加热",
    )
    @pytest.mark.smoke
    def test_caseid_1960116(self):
        with allure.step("设置初始化条件"):
            self.com_lib.set_common_precontion(usage_mode=0, car_mode=0)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr06, "HvSysRlyStsHvSysRlySts", 1)
            sleep(0.5)
        self.com_lib.send_s2s_request_and_check(
            ("SteerWheelService", "SetHeat", {"status": 3}),
            check_signal_parameter=(
                "bodycan.CEMBodyFr36",
                "TelmSteerWhlHeatgReqLvl",
                3,
            ),
            check_service_response=(
                "SteerWheelService_client",
                "GetHeat",
                {},
                {"out": {"level":0}},
            ),
        )
       