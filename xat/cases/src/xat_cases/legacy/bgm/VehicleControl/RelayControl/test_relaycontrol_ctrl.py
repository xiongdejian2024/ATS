#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_relaycontrol_ctrl.py
@Time         :2023/07/24 17:20:31
@Author       :hui.zhao@jiduauto.com
@Description  :
"""
import allure
import pytest
import time
from time import sleep
from xat_ecu.legacy.sdk.digital_key.digital_key_const import *
from xat_ecu.legacy.common.data_type_handing import logger
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey
from xat_ecu.legacy.soa_partner.src.base_partner import S2sBaseClass
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check

# from test_case.bgm.case_helper.partner_const import *
from xat_cases.legacy.bgm.VehicleControl.case_helper.common_lib_bgm import *
from xat_cases.legacy.bgm.VehicleControl.case_helper.parse_excel_bgm import *
from xat_ecu.legacy.interface.nuc_app import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey


def set_bgm_diag_active_line(status):
    if status == "conntected":
        cmd_set = f"usbrelay 1_3=1"
    elif status == "disconntected":
        cmd_set = f"usbrelay 1_3=0"

    exec_shell(cmd_set)
    sleep(2)

    cmd_get = f"usbrelay"
    exec_result = exec_shell(cmd_get)
    # logger.info(exec_result)

    if status == "conntected":
        if exec_result["output"].find("1_3=1") != -1:
            logger.info("BGM诊断激活线连接成功")
            return True
        else:
            return False

    elif status == "disconntected":
        if exec_result["output"].find("1_3=0") != -1:
            logger.info("BGM诊断激活线断开成功")
            return True
        else:
            return False


@allure.feature("车身网关测试/整车控制")
@allure.story("Relay Control")
class TestRelayContolCtrl(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.ipdu.start_all_time_control()
        self.nucapp.bgm_diag_line_up()
        self.busapp.start_all_cyclic_msg()
        self.sd_tester.diagnostic_client_sim_start()
        # self.partner = S2sBaseClass([("VehicleModeService", "client")])
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.sd_tester.tester_present()
        sleep(0.5)
        self.sd_tester.update_serverdoipid(0x1002)
        sleep(0.5)
        # 启动parete operator
        self.partner = S2sBaseClass([("VehicleModeService", "client")])
        sleep(2)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        sleep(0.1)

    def after_each_func(self, ecu):
        self.sd_tester.change_car_mode(0)
        sleep(0.1)
        self.sd_tester.change_usage_mode(0)
        sleep(0.1)
        self.ipdu.reset_check_results()
        sleep(0.1)
        logger.info("诊断激活线连接")
        self.nucapp.bgm_diag_line_up()
        sleep(15)
        super().after_each_func(ecu)

    def after_class(self, ecu):
        try:
            self.sd_tester.change_usage_mode(1)
            self.sd_tester.change_car_mode(0)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        self.ipdu.time_control_stop()  # 停止数据模拟(数据库周期性报文和调度表)
        self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动,总线开始收发报文
        self.nucapp.bgm_diag_line_down()
        sleep(0.5)
        self.sd_tester.stop_tester_present()
        sleep(0.5)
        self.sd_tester.diagnostic_client_sim_close()
        sleep(0.5)
        logger.info("诊断激活线连接")
        self.nucapp.bgm_diag_line_up()
        sleep(15)
        super().after_class(self, ecu)

    def set_lock(self):
        self.ipdu.pause_all_bus_send()
        # # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "VehMtnStVehMtnSt", 3)
        # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0
        )
        # self.ipdu.backbonefr_vddmbackbonefr03_gearlvrindcn_gearlvrindcn2_parkindcn()
        self.ipdu.set(self.ipdu.backbonefr.vddmbackbonefr03, "gearlvrindcn", 0)
        self.dk.set_drvr_seat_notpresent()
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        time.sleep(0.3)
        self.io.set_four_door_close()
        self.io.trunk_door_close()
        self.io.hood_door1_close()
        time.sleep(0.3)
        
    @allure.title("KL15_1 Fotastaus_update")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.smoke
    def test_relaycontrol_caseid_118336(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Inactive
            self.sd_tester.change_usage_mode(1)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:FOAT状态由00切换为04update"):
            self.sd_tester.update_serverdoipid(0x1002)
            sleep(0.5)
            # 三级 27 解锁
            self.sd_tester.security_access_level_l3()
            logger.info("诊断指令22F15304")
            self.sd_tester.client_sim.send_data([0x22, 0xF1, 0x53, 0x04])
            sleep(10)

        with allure.step(f"检测是否RlyPwrDistbnCmd1WdIgnRlyCmd=1"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr14, "RlyPwrDistbnCmd1WdIgnRlyCmd", 1
            )

    @allure.title("case KL15_2 Fota_update")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    # @pytest.mark.smoke
    # def test_relaycontrol_caseid_118357(self):
    #     with allure.step(f"Step:设置初始条件"):
    #         # UsageMode 设置为Abandoned
    #         self.sd_tester.change_usage_mode(0)
    #         sleep(0.5)
    #         # 诊断激活线断开
    #         logger.info("诊断激活线断开")
    #         self.nucapp.bgm_diag_line_down()

    #     with allure.step(f"Step:usgmod由00abandoned切换为01inactive"):
    #         self.sd_tester.change_usage_mode(1)
    #         sleep(10)

    #     with allure.step(f"Step:FOAT状态由00切换为04update"):
    #         self.sd_tester.update_serverdoipid(0x1002)
    #         sleep(0.1)
    #         # 三级 27 解锁
    #         self.sd_tester.security_access_level_l3()
    #         logger.info("诊断指令22F15304")
    #         self.sd_tester.client_sim.send_data([0x22, 0xF1, 0x53, 0x04])
    #         sleep(10)

    #     with allure.step(f"检测当前的Usage Mode是否为Inactive"):
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr02,
    #             "VehModMngtGlbSafe1UsgModSts",
    #             1,
    #         )
    #         sleep(0.5)

    #     with allure.step(f"检测是否RlyPwrDistbnCmd1WdIgnRlyExtCmd=1"):
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr15,
    #             "RlyPwrDistbnCmd1WdIgnRlyExtCmd",
    #             1,
    #         )

    # @allure.title("case KL15_3 Fota_update")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    # )
    # @pytest.mark.smoke
    # def test_relaycontrol_caseid_118383(self):
    #     with allure.step(f"Step:设置初始条件"):
    #         # UsageMode 设置为Abandoned
    #         self.sd_tester.change_usage_mode(0)
    #         sleep(0.5)
    #         # 诊断激活线断开
    #         logger.info("诊断激活线断开")
    #         self.nucapp.bgm_diag_line_down()

    #     with allure.step(f"Step:usgmod由00abandoned切换为01inactive"):
    #         self.sd_tester.change_usage_mode(1)
    #         sleep(10)

    #     with allure.step(f"Step:FOAT状态由00切换为04update"):
    #         self.sd_tester.update_serverdoipid(0x1002)
    #         sleep(0.1)
    #         # 三级 27 解锁
    #         self.sd_tester.security_access_level_l3()
    #         logger.info("诊断指令22F15304")
    #         self.sd_tester.client_sim.send_data([0x22, 0xF1, 0x53, 0x04])
    #         sleep(10)

    #     with allure.step(f"检测当前的Usage Mode是否为Inactive"):
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr02,
    #             "VehModMngtGlbSafe1UsgModSts",
    #             1,
    #         )
    #         sleep(0.5)

    #     with allure.step(f"检测是否IgnRly3Cmd=1"):
    #         self.ipdu.check(self.ipdu.adcanfd.BgmADCANFDFr30, "IgnRly3Cmd", 1)

    # @allure.title("case KL15_3 OFF")
    # @allure.testcase(
    #     'https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46'
    # )
    # @pytest.mark.smoke
    # @pytest.mark.full
    # def test_relaycontrol_caseid_0000029(self):
    #     with allure.step(f"Step:设置初始条件"):
    #         # 诊断激活线断开
    #         logger.info("诊断激活线断开")
    #         self.nucapp.bgm_diag_line_down()
    #         # LidarPowerReq_on
    #         # self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr05, 'LidarPowerReq', 1)
    #         # sleep(2)

    #     with allure.step(f"Step:设置LidarPowerReq=0"):
    #         self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr05, 'LidarPowerReq', 0)
    #         sleep(0.2)

    #     # with allure.step(f"Step:诊断激活线断开"):
    #     #     logger.info("诊断激活线断开")
    #     #     set_bgm_diag_active_line("disconntected")
    #     #     sleep(10)

    #     # with allure.step(f"Step:等待6分钟"):
    #     #     logger.info("等待6分钟")
    #     #     sleep(360)

    #     with allure.step(f"Step:FOTA状态由00切换为00Idle"):
    #         self.sd_tester.update_serverdoipid(0x1002)
    #         sleep(0.1)
    #         # 三级 27 解锁
    #         self.sd_tester.security_access_level_l3()
    #         logger.info("诊断指令22F15300")
    #         self.sd_tester.client_sim.send_data([0x22, 0xF1, 0x53, 0x00])
    #         sleep(10)

    #     with allure.step(f"检测是否IgnRly3Cmd=0"):
    #         self.ipdu.check(
    #             self.ipdu.adcanfd.BgmADCANFDFr30, 'IgnRly3Cmd', 0
    #         )

    #     sleep(5)

    @allure.title("case Climate relay EngSt1WdStsEngSt1WdSts_2")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.smoke
    def test_relaycontrol_caseid_118438(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Driving
            self.sd_tester.change_usage_mode(13)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:usgmod由13driving切换为01inactive"):
            self.sd_tester.change_usage_mode(1)
            sleep(10)

        with allure.step(f"Step:设置EngSt1WdStsEngSt1WdSts=2"):
            self.ipdu.set(
                self.ipdu.propulsioncan.EcmPropFr24, "EngSt1WdStsEngSt1WdSts", 2
            )
            sleep(0.5)

        with allure.step(f"检测当前的Usage Mode是否为Inactive"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                1,
            )
            sleep(0.5)

        with allure.step(f"Step:诊断控制"):
            self.sd_tester.update_serverdoipid(0x1002)
            sleep(0.1)
            # 三级 27 解锁
            self.sd_tester.security_access_level_l3()
            logger.info("诊断指令2F432E0301")
            self.sd_tester.client_sim.send_data([0x2F, 0x43, 0x2E, 0x03, 0x01])
            sleep(10)

        with allure.step(f"检测是否ClimRlyCmd=1"):
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr04, "ClimRlyCmd", 1)

    @allure.title("case Climate_relay 诊断_on")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.sanity
    def test_relaycontrol_caseid_118474(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Abandoned
            self.sd_tester.change_usage_mode(0)
            sleep(0.5)
            # CarMode 设置为Crash
            self.sd_tester.change_car_mode(3)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:usgmod由13driving切换为01inactive"):
            self.sd_tester.change_usage_mode(1)
            sleep(10)

        with allure.step(f"Step:carmod由03crash切换为00normal"):
            self.sd_tester.change_car_mode(0)
            sleep(10)

        with allure.step(f"Step:诊断激活线连接"):
            logger.info("诊断激活线连接")
            self.nucapp.bgm_diag_line_up()
            sleep(0.5)

        with allure.step(f"检测当前的Usage Mode是否为Inactive"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                1,
            )
            sleep(0.5)

        with allure.step(f"检测当前的Car Mode是否为Normal"):
            expectedvalue = self.ipdu.get_recent_signal_raw_value(
                self.ipdu.bodycan.CEMBodyFr12,
                "VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12",
            )
            assert expectedvalue == 0
            sleep(0.5)

        with allure.step(f"检测是否ClimRlyCmd=1"):
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr04, "ClimRlyCmd", 1)

    @allure.title("case Climate_relay Carmode_crash")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.sanity
    def test_relaycontrol_caseid_118484(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Abandoned
            self.sd_tester.change_usage_mode(0)
            sleep(0.5)
            # CarMode 设置为Normal
            self.sd_tester.change_car_mode(0)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:carmod由00normal切换为03crash"):
            self.sd_tester.change_car_mode(3)
            sleep(10)

        with allure.step(f"检测当前的Car Mode是否为Crash"):
            expectedvalue = self.ipdu.get_recent_signal_raw_value(
                self.ipdu.bodycan.CEMBodyFr12,
                "VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12",
            )
            assert expectedvalue == 3
            sleep(0.5)

        with allure.step(f"检测是否ClimRlyCmd=0"):
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr04, "ClimRlyCmd", 0)

    @allure.title("case Climate_relay Usagemode_abandoned")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.sanity
    def test_relaycontrol_caseid_118485(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Inactive
            self.sd_tester.change_usage_mode(1)
            sleep(0.5)
            # CarMode 设置为Normal
            self.sd_tester.change_car_mode(0)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:usgmod由01inactive切换为00abandoned"):
            self.sd_tester.change_usage_mode(0)
            sleep(10)

        with allure.step(f"检测当前的Usage Mode是否为abandoned"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                0,
            )
            sleep(0.5)

        with allure.step(f"检测是否ClimRlyCmd=0"):
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr04, "ClimRlyCmd", 0)

    @allure.title("case Climate_relay DiagcComActv_off && RlyCrashForClimaReq_off")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.longtime
    @pytest.mark.full
    def test_relaycontrol_caseid_118494(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Abandoned
            self.sd_tester.change_usage_mode(0)
            sleep(0.5)
            # 诊断激活线连接
            logger.info("诊断激活线连接")
            self.nucapp.bgm_diag_line_up()

        with allure.step(f"Step:诊断激活线断开"):
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()
            sleep(0.5)

        with allure.step(f"Step:等待6分钟"):
            logger.info("等待6分钟")
            sleep(360)

        with allure.step(f"Step:设置RlyCrashForClimaReq=0"):
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr08, "RlyCrashForClimaReq", 0)
            sleep(0.5)

        with allure.step(f"检测是否ClimRlyCmd=0"):
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr04, "ClimRlyCmd", 0)

    @allure.title("Batterysaver_调用服务 SetBatterySaverConnect")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.sanity
    def test_relaycontrol_caseid_113142(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Abandoned
            self.sd_tester.change_usage_mode(0)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:usgmod由00abandoned切换为01inactive"):
            self.sd_tester.change_usage_mode(1)
            sleep(10)

        with allure.step(f"调用SetBatterySaverConnect"):
            self.partner.send_method_request(
                "VehicleModeService_client", "SetBatterySaverConnect", {"mode": 1}
            )

        with allure.step(f"检测当前的Usage Mode是否为Inactive"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                1,
            )
            sleep(0.5)

        with allure.step(f"检测是否RlyPwrDistbnCmd1WdBattSaveCmd=1"):
            self.ipdu.check(
                self.ipdu.infocanfd.BgmInfoCanFdFr18, "RlyPwrDistbnCmd1WdBattSaveCmd", 1
            )

    @allure.title("case Climate_relay carmode下切_normal RlyCrashForClimaReq_on")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.smoke
    def test_relaycontrol_caseid_118457(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为inactive
            self.sd_tester.change_usage_mode(1)
            sleep(0.5)
            # CarMode 设置为Crash
            self.sd_tester.change_car_mode(3)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:设置RlyCrashForClimaReq=1"):
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr08, "RlyCrashForClimaReq", 1)
            sleep(0.5)

        with allure.step(f"Step:carmod由03crash切换为00normal"):
            self.sd_tester.change_car_mode(0)
            sleep(10)

        with allure.step(f"检测当前的Car Mode是否为Normal"):
            expectedvalue = self.ipdu.get_recent_signal_raw_value(
                self.ipdu.bodycan.CEMBodyFr12,
                "VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12",
            )
            assert expectedvalue == 0
            sleep(0.5)

        with allure.step(f"检测是否ClimRlyCmd=1"):
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr04, "ClimRlyCmd", 1)

    @allure.title("case Climate_relay usagemode上切_inactive RlyCrashForClimaReq_on")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.sanity
    def test_relaycontrol_caseid_118461(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为abandoned
            self.sd_tester.change_usage_mode(0)
            sleep(0.5)
            # CarMode 设置为Normal
            self.sd_tester.change_car_mode(0)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:设置RlyCrashForClimaReq=1"):
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr08, "RlyCrashForClimaReq", 1)
            sleep(0.5)

        with allure.step(f"Step:usgmod由00abandoned切换为01inactive"):
            self.sd_tester.change_usage_mode(1)
            sleep(10)

        with allure.step(f"检测当前的Usage Mode是否为Inactive"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                1,
            )
            sleep(0.5)

        with allure.step(f"检测是否ClimRlyCmd=1"):
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr04, "ClimRlyCmd", 1)

    @allure.title("case Climate_relay carmode下切_normal DiagcComActv_on")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.smoke
    def test_relaycontrol_caseid_118466(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为inactive
            self.sd_tester.change_usage_mode(1)
            sleep(0.5)
            # CarMode 设置为Crash
            self.sd_tester.change_car_mode(3)
            sleep(0.5)
            # 诊断激活线连接
            logger.info("诊断激活线连接")
            self.nucapp.bgm_diag_line_up()

        with allure.step(f"Step:carmod由03crash切换为00normal"):
            self.sd_tester.change_car_mode(0)
            sleep(10)

        with allure.step(f"检测当前的Car Mode是否为Normal"):
            expectedvalue = self.ipdu.get_recent_signal_raw_value(
                self.ipdu.bodycan.CEMBodyFr12,
                "VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12",
            )
            assert expectedvalue == 0
            sleep(0.5)

        with allure.step(f"检测是否ClimRlyCmd=1"):
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr04, "ClimRlyCmd", 1)

    @allure.title("case Climate_relay usagemode上切_inactive DiagcComActv_on")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.sanity
    def test_relaycontrol_caseid_118470(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为abandoned
            self.sd_tester.change_usage_mode(0)
            sleep(0.5)
            # CarMode 设置为normal
            self.sd_tester.change_car_mode(0)
            sleep(0.5)
            # 诊断激活线连接
            logger.info("诊断激活线连接")
            self.nucapp.bgm_diag_line_up()

        with allure.step(f"Step:usgmod由00abandoned切换为01inactive"):
            self.sd_tester.change_usage_mode(1)
            sleep(10)

        with allure.step(f"检测当前的Usage Mode是否为Inactive"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                1,
            )
            sleep(0.5)

        with allure.step(f"检测是否ClimRlyCmd=1"):
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr04, "ClimRlyCmd", 1)

    @allure.title("case Climate relay ClimRlyCmd_off")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.smoke
    def test_relaycontrol_caseid_118495(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Abandoned
            self.sd_tester.change_usage_mode(0)
            sleep(0.5)
            # CarMode 设置为Crash
            self.sd_tester.change_car_mode(3)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:usgmod由00abandoned切换为01inactive"):
            self.sd_tester.change_usage_mode(1)
            sleep(10)

        with allure.step(f"Step:carmod由03crash切换为00normal"):
            self.sd_tester.change_car_mode(0)
            sleep(10)

        with allure.step(f"Step:设置RlyCrashForClimaReq=1"):
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr08, "RlyCrashForClimaReq", 1)
            sleep(0.5)

        with allure.step(f"检测当前的Usage Mode是否为Inactive"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                1,
            )
            sleep(0.5)

        with allure.step(f"检测当前的Car Mode是否为Normal"):
            expectedvalue = self.ipdu.get_recent_signal_raw_value(
                self.ipdu.bodycan.CEMBodyFr12,
                "VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12",
            )
            assert expectedvalue == 0
            sleep(0.5)

        with allure.step(f"检测是否ClimRlyCmd=1"):
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr04, "ClimRlyCmd", 1)

        with allure.step(f"Step:诊断控制"):
            self.sd_tester.update_serverdoipid(0x1002)
            sleep(0.1)
            # 三级 27 解锁
            self.sd_tester.security_access_level_l3()
            logger.info("诊断指令2F432E0300")
            self.sd_tester.client_sim.send_data([0x2F, 0x43, 0x2E, 0x03, 0x00])
            sleep(10)

        with allure.step(f"检测是否ClimRlyCmd=0"):
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr04, "ClimRlyCmd", 0)

    @allure.title("KL15_1 诊断_on Usagemode_上切inactive")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.smoke
    def test_relaycontrol_caseid_118339(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Abandoned
            self.sd_tester.change_usage_mode(0)
            sleep(1)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:诊断激活线连接"):
            logger.info("诊断激活线连接")
            self.nucapp.bgm_diag_line_up()
            sleep(0.5)

        with allure.step(f"Step:usgmod由00abandoned切换为01inactive"):
            self.sd_tester.change_usage_mode(1)
            sleep(10)

        with allure.step(f"检测当前的Usage Mode是否为Inactive"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                1,
            )
            sleep(0.5)

        with allure.step(f"检测是否RlyPwrDistbnCmd1WdIgnRlyCmd=1"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr14, "RlyPwrDistbnCmd1WdIgnRlyCmd", 1
            )
        sleep(5)

    @allure.title("case Batterysaver_usagemode_上切Active")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.full
    def test_relaycontrol_caseid_113162(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Inactive
            self.sd_tester.change_usage_mode(1)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:usgmod由01inactive切换为11active"):
            self.sd_tester.change_usage_mode(11)
            sleep(10)

        with allure.step(f"检测当前的Usage Mode是否为Active"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                11,
            )
            sleep(0.5)

        with allure.step(f"检测是否RlyPwrDistbnCmd1WdBattSaveCmd=1"):
            self.ipdu.check(
                self.ipdu.infocanfd.BgmInfoCanFdFr18, "RlyPwrDistbnCmd1WdBattSaveCmd", 1
            )
        sleep(3)

    @allure.title("KL15_1 specialcase")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.full
    def test_relaycontrol_caseid_118346(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Driving
            self.sd_tester.change_usage_mode(13)
            sleep(0.5)
            # 诊断激活线连接
            logger.info("诊断激活线连接")
            self.nucapp.bgm_diag_line_up()

        with allure.step(f"Step:usgmod由13Driving切换为02convenience"):
            self.sd_tester.change_usage_mode(2)

        with allure.step(f"检测是否RlyPwrDistbnCmd1WdIgnRlyCmd=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr14, "RlyPwrDistbnCmd1WdIgnRlyCmd", 0
            )
            sleep(1)

        with allure.step(f"检测是否RlyPwrDistbnCmd1WdIgnRlyCmd=1"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr14, "RlyPwrDistbnCmd1WdIgnRlyCmd", 1
            )

        sleep(3)

    @allure.title("KL15_1 诊断_on Usagemode_上切convenience")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.full
    def test_relaycontrol_caseid_118343(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Abandoned
            self.sd_tester.change_usage_mode(0)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:诊断激活线连接"):
            logger.info("诊断激活线连接")
            self.nucapp.bgm_diag_line_up()
            sleep(0.5)

        with allure.step(f"Step:usgmod由00abandoned切换为02convenience"):
            self.sd_tester.change_usage_mode(2)
            sleep(10)

        with allure.step(f"检测当前的Usage Mode是否为convenience"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                2,
            )
            sleep(0.5)

        with allure.step(f"检测是否RlyPwrDistbnCmd1WdIgnRlyCmd=1"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr14, "RlyPwrDistbnCmd1WdIgnRlyCmd", 1
            )
        sleep(3)

    @allure.title("case KL15_3 LidarPowerReq_on_convenience")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.full
    def test_relaycontrol_caseid_118370(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Abandoned
            self.sd_tester.change_usage_mode(0)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:usgmod由00abandoned切换为02convenience"):
            self.sd_tester.change_usage_mode(2)
            sleep(10)

        with allure.step(f"Step:设置LidarPowerReq=1"):
            self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr05, "LidarPowerReq", 1)
            sleep(0.5)

        with allure.step(f"检测当前的Usage Mode是否为convenience"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                2,
            )
            sleep(0.5)

        with allure.step(f"检测是否IgnRly3Cmd=1"):
            self.ipdu.check(self.ipdu.adcanfd.BgmADCANFDFr30, "IgnRly3Cmd", 1)

        sleep(3)

    @allure.title("case KL15_3 LidarPowerReq_on_avtive")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.full
    def test_relaycontrol_caseid_118372(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Abandoned
            self.sd_tester.change_usage_mode(0)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:usgmod由00abandoned切换为0Bactive"):
            self.sd_tester.change_usage_mode(11)
            sleep(10)

        with allure.step(f"Step:设置LidarPowerReq=1"):
            self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr05, "LidarPowerReq", 1)
            sleep(0.5)

        with allure.step(f"检测当前的Usage Mode是否为active"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                11,
            )
            sleep(0.5)

        with allure.step(f"检测是否IgnRly3Cmd=1"):
            self.ipdu.check(self.ipdu.adcanfd.BgmADCANFDFr30, "IgnRly3Cmd", 1)

        sleep(3)

    @allure.title("case KL15_3 LidarPowerReq_on_driving")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.full
    def test_relaycontrol_caseid_118374(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Abandoned
            self.sd_tester.change_usage_mode(0)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:usgmod由00abandoned切换为0Ddriving"):
            self.sd_tester.change_usage_mode(13)
            sleep(10)

        with allure.step(f"Step:设置LidarPowerReq=1"):
            self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr05, "LidarPowerReq", 1)
            sleep(0.5)

        with allure.step(f"检测当前的Usage Mode是否为driving"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                13,
            )
            sleep(0.5)

        with allure.step(f"检测是否IgnRly3Cmd=1"):
            self.ipdu.check(self.ipdu.adcanfd.BgmADCANFDFr30, "IgnRly3Cmd", 1)

        sleep(3)

    @allure.title("case KL15_3 诊断_on convenience")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.full
    def test_relaycontrol_caseid_118378(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Abandoned
            self.sd_tester.change_usage_mode(0)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:usgmod由00abandoned切换为02convenience"):
            self.sd_tester.change_usage_mode(2)
            sleep(0.5)

        with allure.step(f"Step:诊断激活线连接"):
            logger.info("诊断激活线连接")
            self.nucapp.bgm_diag_line_up()
            sleep(10)

        with allure.step(f"检测当前的Usage Mode是否为convenience"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                2,
            )
            sleep(0.5)

        with allure.step(f"检测是否IgnRly3Cmd=1"):
            self.ipdu.check(self.ipdu.adcanfd.BgmADCANFDFr30, "IgnRly3Cmd", 1)

        sleep(3)

    @allure.title("case KL15_3 诊断_on active")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.full
    def test_relaycontrol_caseid_118380(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Abandoned
            self.sd_tester.change_usage_mode(0)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:usgmod由00abandoned切换为0Bactive"):
            self.sd_tester.change_usage_mode(11)
            sleep(0.5)

        with allure.step(f"Step:诊断激活线连接"):
            logger.info("诊断激活线连接")
            self.nucapp.bgm_diag_line_up()
            sleep(10)

        with allure.step(f"检测当前的Usage Mode是否为active"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                11,
            )
            sleep(0.5)

        with allure.step(f"检测是否IgnRly3Cmd=1"):
            self.ipdu.check(self.ipdu.adcanfd.BgmADCANFDFr30, "IgnRly3Cmd", 1)

        sleep(3)

    @allure.title("case KL15_3 诊断_on driving")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.full
    def test_relaycontrol_caseid_118382(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Abandoned
            self.sd_tester.change_usage_mode(0)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:usgmod由00abandoned切换为0Ddriving"):
            self.sd_tester.change_usage_mode(13)
            sleep(0.5)

        with allure.step(f"Step:诊断激活线连接"):
            logger.info("诊断激活线连接")
            self.nucapp.bgm_diag_line_up()
            sleep(10)

        with allure.step(f"检测当前的Usage Mode是否为driving"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                13,
            )
            sleep(0.5)

        with allure.step(f"检测是否IgnRly3Cmd=1"):
            self.ipdu.check(self.ipdu.adcanfd.BgmADCANFDFr30, "IgnRly3Cmd", 1)

        sleep(3)

    @allure.title("case Power outlet supply Usagemode_convenience")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.smoke
    def test_relaycontrol_caseid_118412(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Inactive
            self.sd_tester.change_usage_mode(1)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:usgmod由01inactive切换为02convenience"):
            self.sd_tester.change_usage_mode(2)
            sleep(10)

        with allure.step(f"检测当前的Usage Mode是否为convenience"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                2,
            )
            sleep(0.5)

        with allure.step(f"检测是否IgnRly3Cmd=1"):
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, "RlyPwrCmd", 1)

        sleep(3)

    @allure.title("case Power outlet supply Usagemode_active")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.full
    def test_relaycontrol_caseid_118413(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Inactive
            self.sd_tester.change_usage_mode(1)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:usgmod由01inactive切换为0Bactive"):
            self.sd_tester.change_usage_mode(11)
            sleep(10)

        with allure.step(f"检测当前的Usage Mode是否为active"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                11,
            )
            sleep(0.5)

        with allure.step(f"检测是否IgnRly3Cmd=1"):
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, "RlyPwrCmd", 1)

        sleep(3)

    @allure.title("case Power outlet supply Usagemode_driving")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.full
    def test_relaycontrol_caseid_118414(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Inactive
            self.sd_tester.change_usage_mode(1)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:usgmod由01inactive切换为0Ddriving"):
            self.sd_tester.change_usage_mode(13)
            sleep(10)

        with allure.step(f"检测当前的Usage Mode是否为driving"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                13,
            )
            sleep(0.5)

        with allure.step(f"检测是否IgnRly3Cmd=1"):
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, "RlyPwrCmd", 1)

        sleep(3)

    @allure.title("case Climate relay EngSt1WdStsEngSt1WdSts_3_abandoned")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.full
    def test_relaycontrol_caseid_118439(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为abandoned
            self.sd_tester.change_usage_mode(0)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:设置EngSt1WdStsEngSt1WdSts=3"):
            self.ipdu.set(
                self.ipdu.propulsioncan.EcmPropFr24, "EngSt1WdStsEngSt1WdSts", 3
            )
            sleep(0.5)

        with allure.step(f"检测当前的Usage Mode是否为abandoned"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                0,
            )
            sleep(0.5)

        with allure.step(f"Step:诊断控制"):
            self.sd_tester.update_serverdoipid(0x1002)
            sleep(0.1)
            # 三级 27 解锁
            self.sd_tester.security_access_level_l3()
            logger.info("诊断指令2F432E0301")
            self.sd_tester.client_sim.send_data([0x2F, 0x43, 0x2E, 0x03, 0x01])
            sleep(10)

        with allure.step(f"检测是否ClimRlyCmd=1"):
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr04, "ClimRlyCmd", 1)

    @allure.title("case Climate relay EngSt1WdStsEngSt1WdSts_2_inactive")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.full
    def test_relaycontrol_caseid_118440(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为inactive
            self.sd_tester.change_usage_mode(1)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:设置EngSt1WdStsEngSt1WdSts=2"):
            self.ipdu.set(
                self.ipdu.propulsioncan.EcmPropFr24, "EngSt1WdStsEngSt1WdSts", 2
            )
            sleep(0.5)

        with allure.step(f"检测当前的Usage Mode是否为Inactive"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                1,
            )
            sleep(0.5)

        with allure.step(f"Step:诊断控制"):
            self.sd_tester.update_serverdoipid(0x1002)
            sleep(0.1)
            # 三级 27 解锁
            self.sd_tester.security_access_level_l3()
            logger.info("诊断指令2F432E0301")
            self.sd_tester.client_sim.send_data([0x2F, 0x43, 0x2E, 0x03, 0x01])
            sleep(10)

        with allure.step(f"检测是否ClimRlyCmd=1"):
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr04, "ClimRlyCmd", 1)

    @allure.title("case Climate relay EngSt1WdStsEngSt1WdSts_3_inactive")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.full
    def test_relaycontrol_caseid_118441(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为inactive
            self.sd_tester.change_usage_mode(1)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:设置EngSt1WdStsEngSt1WdSts=3"):
            self.ipdu.set(
                self.ipdu.propulsioncan.EcmPropFr24, "EngSt1WdStsEngSt1WdSts", 3
            )
            sleep(0.5)

        with allure.step(f"检测当前的Usage Mode是否为Inactive"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                1,
            )
            sleep(0.5)

        with allure.step(f"Step:诊断控制"):
            self.sd_tester.update_serverdoipid(0x1002)
            sleep(0.1)
            # 三级 27 解锁
            self.sd_tester.security_access_level_l3()
            logger.info("诊断指令2F432E0301")
            self.sd_tester.client_sim.send_data([0x2F, 0x43, 0x2E, 0x03, 0x01])
            sleep(10)

        with allure.step(f"检测是否ClimRlyCmd=1"):
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr04, "ClimRlyCmd", 1)

    @allure.title("case Climate relay EngSt1WdStsEngSt1WdSts_2_convenience")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.full
    def test_relaycontrol_caseid_118442(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为convenience
            self.sd_tester.change_usage_mode(2)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:设置EngSt1WdStsEngSt1WdSts=2"):
            self.ipdu.set(
                self.ipdu.propulsioncan.EcmPropFr24, "EngSt1WdStsEngSt1WdSts", 2
            )
            sleep(0.5)

        with allure.step(f"检测当前的Usage Mode是否为convenience"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                2,
            )
            sleep(0.5)

        with allure.step(f"Step:诊断控制"):
            self.sd_tester.update_serverdoipid(0x1002)
            sleep(0.1)
            # 三级 27 解锁
            self.sd_tester.security_access_level_l3()
            logger.info("诊断指令2F432E0301")
            self.sd_tester.client_sim.send_data([0x2F, 0x43, 0x2E, 0x03, 0x01])
            sleep(10)

        with allure.step(f"检测是否ClimRlyCmd=1"):
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr04, "ClimRlyCmd", 1)

    @allure.title("case Climate relay EngSt1WdStsEngSt1WdSts_3_convenience")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.full
    def test_relaycontrol_caseid_118443(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为convenience
            self.sd_tester.change_usage_mode(2)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:设置EngSt1WdStsEngSt1WdSts=3"):
            self.ipdu.set(
                self.ipdu.propulsioncan.EcmPropFr24, "EngSt1WdStsEngSt1WdSts", 3
            )
            sleep(0.5)

        with allure.step(f"检测当前的Usage Mode是否为convenience"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                2,
            )
            sleep(0.5)

        with allure.step(f"Step:诊断控制"):
            self.sd_tester.update_serverdoipid(0x1002)
            sleep(0.1)
            # 三级 27 解锁
            self.sd_tester.security_access_level_l3()
            logger.info("诊断指令2F432E0301")
            self.sd_tester.client_sim.send_data([0x2F, 0x43, 0x2E, 0x03, 0x01])
            sleep(10)

        with allure.step(f"检测是否ClimRlyCmd=1"):
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr04, "ClimRlyCmd", 1)

    @allure.title("case Climate relay EngSt1WdStsEngSt1WdSts_2_active")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.full
    def test_relaycontrol_caseid_118444(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为active
            self.sd_tester.change_usage_mode(11)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:设置EngSt1WdStsEngSt1WdSts=2"):
            self.ipdu.set(
                self.ipdu.propulsioncan.EcmPropFr24, "EngSt1WdStsEngSt1WdSts", 2
            )
            sleep(0.5)

        with allure.step(f"检测当前的Usage Mode是否为active"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                11,
            )
            sleep(0.5)

        with allure.step(f"Step:诊断控制"):
            self.sd_tester.update_serverdoipid(0x1002)
            sleep(0.1)
            # 三级 27 解锁
            self.sd_tester.security_access_level_l3()
            logger.info("诊断指令2F432E0301")
            self.sd_tester.client_sim.send_data([0x2F, 0x43, 0x2E, 0x03, 0x01])
            sleep(10)

        with allure.step(f"检测是否ClimRlyCmd=1"):
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr04, "ClimRlyCmd", 1)

    @allure.title("case Climate relay EngSt1WdStsEngSt1WdSts_3_active")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1683107?projectId=46"
    )
    @pytest.mark.full
    def test_relaycontrol_caseid_118445(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为active
            self.sd_tester.change_usage_mode(11)
            sleep(0.5)
            # 诊断激活线断开
            logger.info("诊断激活线断开")
            self.nucapp.bgm_diag_line_down()

        with allure.step(f"Step:设置EngSt1WdStsEngSt1WdSts=3"):
            self.ipdu.set(
                self.ipdu.propulsioncan.EcmPropFr24, "EngSt1WdStsEngSt1WdSts", 3
            )
            sleep(0.5)

        with allure.step(f"检测当前的Usage Mode是否为active"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                11,
            )
            sleep(0.5)

        with allure.step(f"Step:诊断控制"):
            self.sd_tester.update_serverdoipid(0x1002)
            sleep(0.1)
            # 三级 27 解锁
            self.sd_tester.security_access_level_l3()
            logger.info("诊断指令2F432E0301")
            self.sd_tester.client_sim.send_data([0x2F, 0x43, 0x2E, 0x03, 0x01])
            sleep(10)

        with allure.step(f"检测是否ClimRlyCmd=1"):
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr04, "ClimRlyCmd", 1)
