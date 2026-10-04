#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_CentralLockService.py
@Time         :2023/04/08 17:20:31
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

# from test_case.soa.case_helper.partner_const import *
from xat_cases.legacy.bgm.VehicleControl.case_helper.common_lib_bgm import *

NotifyTi = 1
KEY_MATCH_INFO = {
    1: [2, 3, 4, 5, 6, 8, 0xA, 0xB],
    2: [2, 3, 4, 5, 6, 0xA, 0xB],
    3: [3, 6, 0xA],
    4: [4, 6, 0xB],
    6: [8],
    7: [8],
    8: [8],
}

KEY_SERVICE_CLIENT = "KeyService_client"
CENTRALLOCK_SERVICE_CLIENT = "CentralLockService_client"
TAILGATESERVICE_CLIENT = "TailGateService_client"
DOOR_SERVICE_CLIENT = "DoorService_client"


@allure.feature("车身网关测试/整车控制")
@allure.story("锁控制")
class TestCentralLockCtrl(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        partner_process_check()
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass(
            [
                ("CentralLockService", "client"),
                ("KeyService", "client"),
                ("DoorService", "client"),
                ("TailGateService", "client"),
                ("VehicleModeService", "client"),
            ]
        )
        self.ipdu.start_all_time_control()
        self.busapp.start_all_cyclic_msg()
        sleep(2)
        self.partner.send_method_request(
            KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 5, "value": 0}]}
        )
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.diagnostic_client_sim_start()

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
        # self.sd_tester = Sd_Tester(**self.tc_config)
        # self.sd_tester.update_serverdoipid(0x1002)
        # self.sd_tester.diagnostic_client_sim_start()
        self.sd_tester.change_car_mode(0)
        sleep(1)
        self.set_centrllock_pre_condition()
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgta_0_bcmvddmbackbonesignalipdu06_value(
            0
        )
        # self.sd_tester.diagnostic_client_sim_close()
        self.ipdu.reset_check_results()
        if ecu.get("testresult") != "Pass":
            logger.info("case失败，需等待5s让环境恢复")
            sleep(5)
        else:
            sleep(3)  # 避免防玩
        super().after_each_func(ecu, start=False)

    def ck_LockActTriggerSource(self, src_id, timeout=1.0):
        self.partner.ck_s2s_event(
            CENTRALLOCK_SERVICE_CLIENT,
            "LockActTriggerSource",
            {"sourceId": src_id},
            timeout,
        )
        self.partner.send_request_and_ck_resp(
            CENTRALLOCK_SERVICE_CLIENT, "GetLockActTriggerSource", {}, {"out": src_id}
        )

    def ck_CentralLockStatusInfo(self, lock_sts, trigger_srcid, timeout=1):
        info1 = {"sts": lock_sts, "triggerId": trigger_srcid, "updateEve": True}
        info0 = {"sts": lock_sts, "triggerId": trigger_srcid, "updateEve": False}
        self.partner.ck_s2s_event(
            CENTRALLOCK_SERVICE_CLIENT,
            "NotifyCentralLockSysInfo",
            {"info": info1},
            timeout,
        )
        self.partner.send_request_and_ck_resp(
            CENTRALLOCK_SERVICE_CLIENT, "GetCentralLockSysInfo", {}, {"out": info1}
        )

        self.partner.ck_s2s_event(
            CENTRALLOCK_SERVICE_CLIENT,
            "NotifyCentralLockSysInfo",
            {"info": info0},
            timeout=1,
        )
        self.partner.send_request_and_ck_resp(
            CENTRALLOCK_SERVICE_CLIENT, "GetCentralLockSysInfo", {}, {"out": info0}
        )

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
        # sleep(1)
        # self.dk.send_walk_away_lock_cmd()
        # sleep(1)
        # self.dk.ck_cenlock_sts(3)

    def check_four_door_lock_request_start(self, sts):
        target_msg = self.ipdu.bodycan.CemBodyFr01
        self.ipdu.check_multiple_signals_thread_start(
            [
                (target_msg, "DoorDrvrLockCmd", sts),
                (target_msg, "DoorPassLockCmd", sts),
                (target_msg, "DoorLeReLockCmd", sts),
                (target_msg, "DoorRiReLockCmd", sts),
            ],
            5,
        )

    def check_four_door_lock_request_stop(self):
        return self.ipdu.check_multiple_signals_thread_stop(message_name="CemBodyFr01")

    @allure.title("设置整车上锁解锁_HMI解锁")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1791290?projectId=46"
    )
    @pytest.mark.mcu_test
    @pytest.mark.smoke
    def test_caseid_115514(self):
        self.dk.set_cenlock_sts(0x3)
        sleep(1)
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 2}
        )
        self.dk.ck_four_door_lock_cmd(1)
        sleep(1)
        self.dk.ck_cenlock_sts(0x1, 0x3)
        sleep(3)

    @allure.title("中控锁系统状态_车速自动闭锁成功")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1572080?projectId=46"
    )
    @pytest.mark.mcu_test
    @pytest.mark.smoke
    def test_caseid_110369(self):
        # 设置中控锁unlock
        # self.dk.set_cenlock_sts(1)
        # self.partner.event_list[CENTRALLOCK_SERVICE_CLIENT] = []
        self.partner.empty_all()
        sleep(0.5)
        # 设置usgmod为drving
        self.sd_tester.change_usage_mode(0xD)
        # 设置主驾占位
        self.dk.set_drvr_seat_present()
        # 设置四门锁解锁状态
        self.dk.set_four_door_unlock()
        # self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgtqf_0_bcmvddmbackbonesignalipdu06_genqf1_accurdata()
        self.ipdu.set_vehspd(0.0)
        self.dk.set_door_opener_sts(1, 1)
        self.dk.set_door_opener_sts(2, 1)
        self.dk.set_door_opener_sts(3, 1)
        self.dk.set_door_opener_sts(4, 1)
        self.dk.set_door_opener_sts(5, 1)
        # 设置车速超过7km/h
        self.ipdu.set_vehspd(7.0)
        sleep(1)
        # 检查中控锁状态及闭锁源
        self.ck_CentralLockStatusInfo(3, 4)
        sleep(5)

    @allure.title("中控锁系统状态_8_Crash解锁成功")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1791289?projectId=46"
    )
    @pytest.mark.mcu_test
    @pytest.mark.smoke
    def test_caseid_115515(self):
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_car_mode(0x3)
        self.dk.ck_cenlock_sts(0x1, 0x8)
        sleep(3)

    @allure.title("645007 v4 KV闭锁_钥匙区域在车外左前门区域_可闭锁")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1819367?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_1898289(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])
        self.dk.press_door_outswitch(4, 3)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 3),
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsTrigSrc", 2),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("498582 v16 KV解锁_钥匙遗留车内可解锁")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1791298?projectId=46"
    )
    @pytest.mark.mcu_test
    @pytest.mark.smoke
    def test_caseid_114312(self):
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])  #  车内有钥匙遗留
        self.dk.press_door_outswitch(4, 0.5)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 1),
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsTrigSrc", 2),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("设置整车上锁解锁_RKE闭锁")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1791284?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_115519(self):
        self.dk.set_cenlock_sts(0x1)
        sleep(1)
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 0}
        )
        self.dk.ck_four_door_lock_cmd(2)
        sleep(1)
        self.dk.ck_cenlock_sts(0x3, 0x1)
        sleep(3)

    @allure.title("设置整车上锁解锁_RKE解锁")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1819047?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_114603(self):
        self.dk.set_cenlock_sts(0x3)
        sleep(1)
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 0}
        )
        self.dk.ck_four_door_lock_cmd(1)
        sleep(1)
        self.dk.ck_cenlock_sts(0x1, 0x1)
        sleep(3)

    @allure.title("中控锁系统状态_NFC解锁")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1819379?projectId=46"
    )
    @pytest.mark.mcu_test
    @pytest.mark.smoke
    def test_caseid_115511(self):
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
        sleep(3)

    @allure.title("中控锁系统状态_12_NFC闭锁")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1791283?projectId=46"
    )
    @pytest.mark.mcu_test
    @pytest.mark.smoke
    def test_caseid_114308(self):
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

    # @allure.title("设置整车上锁解锁_Telm_远控闭锁")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/1819289?projectId=46"
    # )
    # @pytest.mark.debug
    # def test_caseid_1819289(self):
    #     # 设置整车上锁
    #     self.dk.set_cenlock_sts(0x1)
    #     sleep(1)
    #     # 调用锁服务设置为Telm闭锁
    #     self.partner.send_method_request(
    #         CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 1}
    #     )
    #     # 检查四门锁指令
    #     self.dk.ck_four_door_lock_cmd(2)
    #     sleep(1)
    #     # 检查中控状态及闭锁源
    #     self.dk.ck_cenlock_sts(0x3, 0x7)
    #     sleep(3)

    @allure.title("设置整车上锁解锁_Telm_远控解锁")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1819304?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_114348(self):
        self.dk.set_cenlock_sts(0x3)
        sleep(1)
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 1}
        )
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.ck_cenlock_sts(0x1, 0x7)
        sleep(3)

    @allure.title("设置整车上锁解锁_Telm_远控关门且闭锁_主驾门open")
    @pytest.mark.smoke
    # @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_caseid_114362(self):
        # self.restart_bgm_and_connect_service("CentralLockService_client")
        self.dk.set_cenlock_sts(0x1)
        sleep(1)
        # 设置开启右前门
        self.dk.set_door_sts([0, 1, 0, 0, 0])
        self.dk.set_door_opener_sts(1, 5, 1, 1, 1)
        time.sleep(1)
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 2, "source": 1}
        )
        self.dk.ck_door_opener_cmd(2, 2)
        sleep(1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.set_four_door_lock()
        self.dk.ck_cenlock_sts(0x3, 0x7)

    @allure.title("设置整车上锁解锁_Apprch_近车解锁")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1819038?projectId=46"
    )
    @pytest.mark.mcu_test
    @pytest.mark.smoke
    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    def test_caseid_114602(self):
        # 调用寻钥匙指令
        self.partner.send_method_request(
            "KeyService_client", "SetConfigInfo", {"infos": [{"key": 1, "value": 1}]}
        )
        # 设置中控上锁
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        sleep(0.5)
        # 调用离车闭锁请求
        self.dk.send_approach_unlock_cmd()
        # 检查中控锁状态为解锁，解锁源为Apprch
        self.dk.ck_cenlock_sts(0x1, 0x9)
        sleep(3)

    @allure.title("中控锁系统状态_Apprch_离车落锁")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1572092?projectId=46"
    )
    @pytest.mark.mcu_test
    @pytest.mark.smoke
    def test_caseid_115524(self):
        self.partner.send_method_request(
            "KeyService_client", "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]}
        )
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        sleep(0.5)
        self.dk.send_walk_away_lock_cmd()
        self.dk.ck_cenlock_sts(0x3, 0x9)
        sleep(3)

    @allure.title("494582 v13 中央闭锁Abandoned模式RKE闭锁成功")
    @pytest.mark.full
    def test_caseid_119270(self):
        self.dk.set_cenlock_sts(0x1)
        self.sd_tester.change_usage_mode(0x0)
        time.sleep(1)
        self.dk.send_rke_lock()
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.set_four_door_lock()
        self.dk.ck_cenlock_sts(0x3, 0x1)

    @allure.title("494582 v13 中央闭锁_右前门开RKE仅闭锁状态监测")
    @pytest.mark.full
    def test_caseid_119273(self):
        self.dk.set_cenlock_sts(0x1)
        self.sd_tester.change_usage_mode(0x2)
        self.dk.set_drvr_seat_present()
        self.dk.set_door_sts([0, 1, 0, 0, 0])  # 右前门开启
        time.sleep(1)
        self.dk.send_rke_lock()
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("494582 v13 中央闭锁_右后门开RKE仅闭锁状态监测")
    @pytest.mark.mcu_test
    @pytest.mark.sanity
    def test_caseid_119275(self):
        self.dk.set_cenlock_sts(0x1)
        self.sd_tester.change_usage_mode(0x2)
        self.dk.set_drvr_seat_present()
        self.dk.set_door_sts([0, 0, 0, 1, 0])  # 右后门开启
        time.sleep(1)
        self.dk.send_rke_lock()
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("RKE闭锁_五门全开仅闭锁")
    @pytest.mark.sanity
    def test_caseid_119276(self):
        self.dk.set_cenlock_sts(0x1)
        self.sd_tester.change_usage_mode(0x2)
        self.dk.set_drvr_seat_present()
        self.dk.set_door_sts([1, 1, 1, 1, 1])  # 五门全开
        time.sleep(2)
        self.dk.send_rke_lock()
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("494582 v13 中央闭锁_Drving模式主驾占座RKE闭锁")
    @pytest.mark.sanity
    def test_caseid_119143(self):
        self.dk.set_cenlock_sts(0x1)
        self.sd_tester.change_usage_mode(0xD)
        self.dk.send_rke_lock()
        self.dk.ck_rke_resp(1, 1, "UsageModeFail", exec_type=3)
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("494582 v13 中央闭锁_Active模式主驾占座RKE闭锁")
    @pytest.mark.sanity
    def test_caseid_119144(self):
        self.dk.set_cenlock_sts(0x1)
        self.sd_tester.change_usage_mode(11)
        self.dk.set_drvr_seat_present()
        time.sleep(1)
        self.dk.send_rke_lock()
        self.dk.ck_rke_resp(1, 1, "UsageModeFail", exec_type=3)
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("494582 v13 中央闭锁_左前门开RKE仅闭锁状态监测")
    @pytest.mark.full
    def test_caseid_119272(self):
        self.dk.set_cenlock_sts(0x1)
        self.sd_tester.change_usage_mode(0x2)
        self.dk.set_drvr_seat_present()
        self.dk.set_door_sts([1, 0, 0, 0, 0])  # 右前门开启
        time.sleep(1)
        self.dk.send_rke_lock()
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("494582 v13 中央闭锁_左后门开RKE仅闭锁状态监测")
    @pytest.mark.full
    def test_caseid_119274(self):
        self.dk.set_cenlock_sts(0x1)
        self.sd_tester.change_usage_mode(0x2)
        self.dk.set_drvr_seat_present()
        self.dk.set_door_sts([0, 0, 1, 0, 0])  # 左后门开启
        time.sleep(1)
        self.dk.send_rke_lock()
        self.dk.ck_cenlock_sts(0x1)

    @allure.title("中央锁状态同步给用户_open")
    @allure.testcase(
        "https: // jama.jiduauto.com / perspective.req  # /testCases/1572109?projectId=46"
    )
    @pytest.mark.mcu_test
    @pytest.mark.smoke
    def test_caseid_110336(self):
        self.dk.set_cenlock_sts(0x1)  # 中控锁解锁
        self.io.hood_door1_open()
        self.io.hood_door2_open()
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "HoodSts", 1)
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr08, "LockgCenStsForUsrFb", 1
        )  # open

    @allure.title("中央锁状态同步给用户_close")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1572108?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_110337(self):
        self.dk.set_cenlock_sts(0x3)
        self.io.hood_door1_close()  # 接地
        self.io.hood_door2_open()  # 悬空 设置引擎盖HoodSts=clsd
        time.sleep(1)
        self.dk.send_rke_unlock()
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_unlock()
        self.dk.ck_cenlock_sts(1)
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr08, "LockgCenStsForUsrFb", 2
        )  # clsd

    @allure.title("中央锁状态同步给用户_lockd")
    @allure.testcase(
        "https: // jama.jiduauto.com / perspective.req  # /testCases/1791296?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_115509(self):
        self.dk.set_cenlock_sts(0x1)
        self.io.hood_door1_close()  # 接地
        self.io.hood_door2_open()  # 悬空 设置引擎盖HoodSts=clsd
        self.sd_tester.change_usage_mode(0x0)  # 防止条件b
        time.sleep(1)
        self.dk.send_rke_lock()
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.set_four_door_lock()
        self.dk.ck_cenlock_sts(3)
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr08, "LockgCenStsForUsrFb", 3
        )  # Lockd

    @allure.title("RKE门锁联动_五门门全开_CONVENIENCE+主驾无占座")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1810273?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_110357(self):
        self.dk.set_cenlock_sts(0x1)
        self.sd_tester.change_usage_mode(0x2)
        self.dk.set_drvr_seat_notpresent()
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        time.sleep(3)
        self.dk.send_rke_close_door_and_lock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_door_opener_cmd(3, 2, 1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        time.sleep(0.5)
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.set_four_door_lock()
        sleep(1)
        self.dk.ck_cenlock_sts(0x3, 0x1)

    @allure.title("Relocking+计时中主驾门open")
    @pytest.mark.sanity
    def test_caseid_115522(self):
        self.dk.send_rke_lock()
        time.sleep(3)
        self.dk.send_rke_unlock()
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_unlock()
        self.dk.ck_cenlock_sts(0x1, 0x1)
        sleep(10)
        self.dk.set_door_sts([0, 1, 0, 0, 0])
        self.dk.set_door_opener_sts(1, 5, 1, 1, 1)
        sleep(20)
        self.dk.ck_cenlock_sts(0x1, 0x1)

    @allure.title("Relocking+重锁计时中同时HMI中控闭锁状态监测")
    @pytest.mark.sanity
    def test_caseid_114305(self):
        self.dk.send_rke_lock()
        time.sleep(3)
        self.dk.send_rke_unlock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_unlock()
        self.dk.ck_cenlock_sts(0x1, 0x1)  # 检查中控锁z
        sleep(10)  # 计时10S开启主驾门
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2}
        )  # HMI闭锁
        sleep(20)  # 正常计时20S后
        self.dk.ck_cenlock_sts(0x3, 0x3)
        sleep(3)

    @allure.title("Telm远控闭锁_Abandone模式下闭锁")
    @pytest.mark.sanity
    def test_caseid_114360(self):
        # 设置整车上锁
        self.dk.set_cenlock_sts(0x1)
        self.sd_tester.change_usage_mode(0x0)
        with allure.step(f"检测当前的Usage Mode是否为Abandoned"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                0,
            )
        sleep(1)
        # 调用锁服务设置为Telm闭锁
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 1}
        )
        # 检查四门锁指令
        self.dk.ck_four_door_lock_cmd(2, 2)
        sleep(1)
        # 检查中控状态及闭锁源
        self.dk.ck_cenlock_sts(0x3, 0x7)
        sleep(3)

    @allure.title("Telm远控闭锁_Inactive模式下闭锁")
    @pytest.mark.sanity
    def test_caseid_1892740(self):
        # 设置整车上锁
        self.dk.set_cenlock_sts(0x1)
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 1}
        )
        self.dk.ck_four_door_lock_cmd(2, 2)
        sleep(1)
        # 检查中控状态及闭锁源
        self.dk.ck_cenlock_sts(0x3, 0x7)
        sleep(3)

    @allure.title("Telm远控闭锁SUCCESS_Active+主驾无占座")
    @pytest.mark.sanity
    def test_caseid_1892741(self):
        # 设置整车上锁
        self.dk.set_cenlock_sts(3)
        self.sd_tester.change_usage_mode(11)
        with allure.step(f"检测当前的Usage Mode是否为Active"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                11,
            )
        self.dk.set_drvr_seat_notpresent()
        sleep(1)
        # 调用锁服务设置为Telm闭锁
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 1}
        )
        self.sd_tester.change_usage_mode(1)
        with allure.step(f"检测当前的Usage Mode是否为Inactive"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr02,
                "VehModMngtGlbSafe1UsgModSts",
                1,
            )  # 闭锁指令发出1.5s内模式下切至 [Inactive] or [Abandoned]才会执行上锁
        # 检查四门锁指令
        self.dk.ck_four_door_lock_cmd(2, 2)
        sleep(1)
        # 检查中控状态及闭锁源
        self.dk.ck_cenlock_sts(0x3, 0x7)
        sleep(3)

    @allure.title("KV闭锁+Abandone模式下_车外后方PE区有有效钥匙0x5_闭锁SUCCESS")
    @pytest.mark.full
    def test_caseid_1898135(self):
        self.sd_tester.change_usage_mode(0)
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(.5)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.press_door_outswitch(4, 2.5)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, 'LockgCenStsLockSt', 3),
            (self.ipdu.backbonefr.CemBackBoneFr06, 'LockgCenStsTrigSrc', 2),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)


    @allure.title("645007 v4 KV闭锁+InActive模式下钥匙遗留车内0x8_闭锁SUCCESS")
    @pytest.mark.full
    def test_caseid_1898137(self):
        self.partner.empty_all(.5)
        self.sd_tester.change_usage_mode(1)
        self.dk.set_cenlock_sts(1)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])
        self.dk.press_door_outswitch(4, 2.5)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, 'LockgCenStsLockSt', 3),
            (self.ipdu.backbonefr.CemBackBoneFr06, 'LockgCenStsTrigSrc', 2),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("KV闭锁+Covenience模式且&&钥匙区域在车外主驾区域0x3_闭锁SUCCESS")
    @pytest.mark.full
    def test_caseid_1898133(self):
        self.partner.empty_all(.5)
        self.sd_tester.change_usage_mode(2)
        self.dk.set_drvr_seat_notpresent()  # 设置主驾无占座
        self.dk.set_cenlock_sts(1)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x3)])
        self.dk.press_door_outswitch(4, 2.5)
        self.sd_tester.change_usage_mode(1)
        sleep(1)  # 等待模式下切
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, 'LockgCenStsLockSt', 3),
            (self.ipdu.backbonefr.CemBackBoneFr06, 'LockgCenStsTrigSrc', 2),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("KV闭锁_钥匙区域在车外右前区域0x4_闭锁SUCCESS")
    @pytest.mark.full
    def test_caseid_1898110(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x4)])
        self.dk.press_door_outswitch(4, 2.5)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, 'LockgCenStsLockSt', 3),
            (self.ipdu.backbonefr.CemBackBoneFr06, 'LockgCenStsTrigSrc', 2),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("KV闭锁_钥匙区域在车外右前区域0x6_闭锁SUCCESS")
    @pytest.mark.full
    def test_caseid_1898109(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])
        self.dk.press_door_outswitch(4, 2.5)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, 'LockgCenStsLockSt', 3),
            (self.ipdu.backbonefr.CemBackBoneFr06, 'LockgCenStsTrigSrc', 2),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("P档自动解锁激活_车内无占位主驾安全带未系&&主驾无人副驾安全带上锁中控不解锁")
    @pytest.mark.sanity
    def test_caseid_1959945(self):
        self.partner.send_method_request(
            DOOR_SERVICE_CLIENT, "SetAutoUnlockTrigger", {"trigger": 0}
        )
        self.dk.set_cenlock_sts(0x3)
        with allure.step(f"设置前置条件:车内无占座主驾安全带未系&&主驾无人，副驾安全带已系"):
            self.io.driver_seat_notpresent()
            self.dk.set_pass_seat_notpresent()
            self.ipdu.set(
                self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 0
            )
            self.ipdu.set(
                self.ipdu.backbonefr.SrsBackBoneFr04,
                "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
                2,
            )
            self.ipdu.set(
                self.ipdu.backbonefr.SrsBackBoneFr04,
                "SeatOccptAtRowSecLe_0_SRSBackBoneSignalIPdu04",
                0,
            )
            self.ipdu.set(
                self.ipdu.backbonefr.SrsBackBoneFr04,
                "SeatOccptAtRowSecRi_0_SRSBackBoneSignalIPdu04",
                0,
            )
            self.ipdu.set(
                self.ipdu.backbonefr.SrsBackBoneFr04,
                "SeatOccptAtRowSecMid_0_SRSBackBoneSignalIPdu04",
                0,
            )
        # 先挂D档再挂P档
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, "GearLvrIndcn", 3)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, "GearLvrIndcn", 0)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 3)
        sleep(5)  # 等待5s计时NVM还是未解锁
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 3)
        sleep(3)
        
    @allure.title("P档自动解锁激活_车内中后排座椅有占座中控解锁")
    @pytest.mark.full
    def test_caseid_119085(self):
        self.partner.send_method_request(
            DOOR_SERVICE_CLIENT, "SetAutoUnlockTrigger", {"trigger": 0}
        )
        self.dk.set_cenlock_sts(0x3)
        # 设置中后排座椅有占座
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecMid_0_SRSBackBoneSignalIPdu04",
            1,
        )
        # 先挂D档再挂P档
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, "GearLvrIndcn", 3)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, "GearLvrIndcn", 0)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 1),
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsTrigSrc", 11),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("P档自动解锁激活_车内副驾座椅有占座中控解锁")
    @pytest.mark.sanity
    def test_caseid_1959947(self):
        self.partner.send_method_request(
            DOOR_SERVICE_CLIENT, "SetAutoUnlockTrigger", {"trigger": 0}
        )
        self.dk.set_cenlock_sts(0x3)
        # 设置副驾座椅有占座
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "PassSeatSts_0_SRSBackBoneSignalIPdu04",
            2,
        )
        # 先挂D档再挂P档
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, "GearLvrIndcn", 3)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, "GearLvrIndcn", 0)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 1),
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsTrigSrc", 11),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("P档自动解锁激活_车内左后排座椅有占座中控解锁")
    @pytest.mark.full
    def test_caseid_1959946(self):
        self.partner.send_method_request(
            DOOR_SERVICE_CLIENT, "SetAutoUnlockTrigger", {"trigger": 0}
        )
        self.dk.set_cenlock_sts(0x3)
        # 设置左后座椅有占座
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecLe_0_SRSBackBoneSignalIPdu04",
            2,
        )
        # 先挂D档再挂P档
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, "GearLvrIndcn", 3)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, "GearLvrIndcn", 0)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 1),
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsTrigSrc", 11),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("NFC锁定转向指示灯可见反馈")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1791304?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_115506(self):
        self.io.hood_door1_close()  # 接地
        self.io.hood_door2_open()  # 悬空 设置引擎盖HoodSts=clsd
        sleep(0.5)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        sleep(0.5)
        self.dk.send_nfc_cmd()
        self.dk.set_four_door_lock()
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, "LockgCenStsForUsrFb", 3)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr02, "ExtrLtgStsTurnIndrRi", 1),
            (self.ipdu.backbonefr.CemBackBoneFr02, "ExtrLtgStsTurnIndrLe", 1),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("Telm锁定转向指示灯可见反馈")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1791288?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_115516(self):
        # 设置整车上锁
        self.dk.set_cenlock_sts(0x1)
        sleep(1)
        self.io.hood_door1_close()  # 接地
        self.io.hood_door2_open()  # 悬空 设置引擎盖HoodSts=clsd
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "HoodSts", 2)
        # 调用锁服务设置为Telm闭锁
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 1}
        )
        sleep(0.5)
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.set_four_door_lock()
        sleep(0.5)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, "LockgCenStsForUsrFb", 3)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr02, "ExtrLtgStsTurnIndrRi", 1),
            (self.ipdu.backbonefr.CemBackBoneFr02, "ExtrLtgStsTurnIndrLe", 1),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("离车闭锁指示灯可见反馈")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1791284?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1791278(self):
        self.io.hood_door1_close()  # 接地
        self.io.hood_door2_open()  # 悬空 设置引擎盖HoodSts=clsd
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "HoodSts", 2)
        sleep(0.5)
        self.partner.send_method_request(
            "KeyService_client", "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]}
        )
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        sleep(0.5)
        self.dk.send_walk_away_lock_cmd()
        self.dk.set_four_door_lock()
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, "LockgCenStsForUsrFb", 3)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr02, "ExtrLtgStsTurnIndrRi", 1),
            (self.ipdu.backbonefr.CemBackBoneFr02, "ExtrLtgStsTurnIndrLe", 1),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("蓝牙锁定指示灯可见反馈")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1791311?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_115501(self):
        self.io.hood_door1_close()  # 接地
        self.io.hood_door2_open()  # 悬空 设置引擎盖HoodSts=clsd
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "HoodSts", 2)
        sleep(0.5)
        self.dk.set_cenlock_sts(0x1)
        sleep(1)
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 0}
        )
        self.dk.ck_four_door_lock_cmd(2)
        self.dk.set_four_door_lock()
        sleep(0.5)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, "LockgCenStsForUsrFb", 3)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr02, "ExtrLtgStsTurnIndrRi", 1),
            (self.ipdu.backbonefr.CemBackBoneFr02, "ExtrLtgStsTurnIndrLe", 1),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("热失控_电池请求中央解锁")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1572089?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_110350(self):
        self.dk.set_cenlock_sts(0x3)
        sleep(0.5)
        # 设置触发热失控
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr18,
            "HvBattLimnIndcn_0_VDDMBackBoneSignalIPdu18",
            128,
        )
        # 设置车速超过22km/h,约6.2m/s
        self.ipdu.set_vehspd(0.27)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 1),
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsTrigSrc", 11),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("热失控_电池请求中央解锁车速V>3km/h中央不解锁")
    @pytest.mark.full
    def test_caseid_1959960(self):
        self.dk.set_cenlock_sts(0x3)
        sleep(0.5)
        # 设置触发热失控
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr18,
            "HvBattLimnIndcn_0_VDDMBackBoneSignalIPdu18",
            128,
        )
        # 设置车速超过22km/h,约6.2m/s
        self.ipdu.set_vehspd(0.28)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 3)
        sleep(3)

    @allure.title("NFC闭锁+RKE解锁+relocking")
    @pytest.mark.Oct
    @pytest.mark.longtime
    @pytest.mark.full
    def test_caseid_1919326(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all()
        sleep(0.5)
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 0}
        )
        self.dk.ck_four_door_lock_cmd(2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 3)
        sleep(0.5)
        self.io.hood_door1_close()  # 接地
        self.io.hood_door2_open()  # 引擎盖open可能影响重锁功能(四门两盖需关闭)
        self.dk.send_rke_unlock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_unlock()
        self.dk.ck_cenlock_sts(0x1, 0x1)
        sleep(0.5)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)
        sleep(30)
        self.dk.ck_cenlock_sts(0x3, 0x5)
        sleep(3)

    @allure.title("RKE闭锁+RKE解锁+relocking")
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1959961(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all()
        sleep(0.5)
        self.dk.send_nfc_cmd()
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 3)
        sleep(0.5)
        self.io.hood_door1_close()  # 接地
        self.io.hood_door2_open()  # 引擎盖open可能影响重锁功能(四门两盖需关闭)
        self.dk.send_rke_unlock()
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_unlock()
        self.dk.ck_cenlock_sts(0x1, 0x1)
        sleep(0.5)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)
        sleep(30)
        self.dk.ck_cenlock_sts(0x3, 0x5)
        sleep(3)

    @allure.title("NFC闭锁+HMI解锁+relocking不执行")
    @pytest.mark.longtime
    @pytest.mark.full
    def test_caseid_1919331(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all()
        sleep(0.5)
        self.dk.send_nfc_cmd()
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 3)
        sleep(0.5)
        self.io.hood_door1_close()  # 接地
        self.io.hood_door2_open()  # 引擎盖open可能影响重锁功能(四门两盖需关闭)
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 2}
        )
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 1)
        sleep(30)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 1)
        sleep(3)

    @allure.title("NFC闭锁+远控解锁+relocking")
    @pytest.mark.longtime
    @pytest.mark.sanity
    def test_caseid_1919329(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all()
        sleep(0.5)
        self.dk.send_nfc_cmd()
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 3)
        sleep(0.5)
        self.io.hood_door1_close()  # 接地
        self.io.hood_door2_open()  # 引擎盖open可能影响重锁功能(四门两盖需关闭)
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 1}
        )
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 1)
        sleep(30)
        self.dk.ck_cenlock_sts(0x3, 0x5)
        sleep(3)

    @allure.title("NFC解锁转向指示灯可见反馈")
    @pytest.mark.sanity
    def test_caseid_115507(self):
        self.io.hood_door1_close()  # 接地
        self.io.hood_door2_open()  # 悬空 设置引擎盖HoodSts=clsd
        sleep(0.5)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.partner.empty_all()
        sleep(0.5)
        self.dk.send_nfc_cmd()
        self.dk.set_four_door_unlock()
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 1)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr02, "ExtrLtgStsTurnIndrRi", 1),
            (self.ipdu.backbonefr.CemBackBoneFr02, "ExtrLtgStsTurnIndrLe", 1),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("远控解锁转向指示灯可见反馈")
    @pytest.mark.sanity
    def test_caseid_115523(self):
        # 设置整车上锁
        self.dk.set_cenlock_sts(0x3)
        sleep(1)
        self.io.hood_door1_close()  # 接地
        self.io.hood_door2_open()  # 悬空 设置引擎盖HoodSts=clsd
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "HoodSts", 2)
        # 调用锁服务设置为Telm闭锁
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 1}
        )
        sleep(0.5)
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_unlock()
        sleep(0.5)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 1)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr02, "ExtrLtgStsTurnIndrRi", 1),
            (self.ipdu.backbonefr.CemBackBoneFr02, "ExtrLtgStsTurnIndrLe", 1),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("RKE解锁指示灯可见反馈")
    @pytest.mark.smoke
    def test_caseid_114597(self):
        self.io.hood_door1_close()  # 接地
        self.io.hood_door2_open()  # 悬空 设置引擎盖HoodSts=clsd
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "HoodSts", 2)
        sleep(0.5)
        self.dk.set_cenlock_sts(0x3)
        sleep(1)
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 0}
        )
        self.dk.ck_four_door_lock_cmd(1)
        self.dk.set_four_door_unlock()
        sleep(0.5)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 1)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr02, "ExtrLtgStsTurnIndrRi", 1),
            (self.ipdu.backbonefr.CemBackBoneFr02, "ExtrLtgStsTurnIndrLe", 1),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("不同CarMode模式下中央锁定行为_Normal(Telm)")
    @pytest.mark.mcu_test
    @pytest.mark.full
    def test_caseid_110365(self):
        # 设置CarMode为Nomal
        self.sd_tester.change_car_mode(0)
        # 设置整车解锁
        self.dk.set_cenlock_sts(0x1)
        sleep(1)
        # 调用锁服务设置为Telm闭锁
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 1}
        )
        # 检查四门锁指令
        self.dk.ck_four_door_lock_cmd(2)
        sleep(1)
        # 检查中控状态及闭锁源
        self.dk.ck_cenlock_sts(0x3, 0x7)
        sleep(3)

    @allure.title("不同CarMode模式下中央锁定行为_Transport（HMI）")
    @pytest.mark.sanity
    def test_caseid_110366(self):
        self.dk.set_cenlock_sts(0x1)
        # 设置CarMode为Transport
        self.sd_tester.change_car_mode(1)
        sleep(1)
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2}
        )
        # 工厂模式闭锁不执行
        self.dk.ck_four_door_lock_cmd(0)
        sleep(1)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 1)
        sleep(3)

    @allure.title("不同CarMode模式下中央锁定行为_Factory(NFC)")
    @pytest.mark.mcu_test
    @pytest.mark.sanity
    def test_caseid_115503(self):
        self.dk.set_cenlock_sts(1)
        # 设置CarMode为Factory
        self.sd_tester.change_car_mode(2)
        sleep(1)
        self.partner.empty_all()
        sleep(0.5)
        self.dk.send_nfc_cmd()
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 1)
        sleep(3)

    @allure.title("不同CarMode模式下中央锁定行为_Crash（Insoth）")
    @pytest.mark.sanity
    def test_caseid_110358(self):
        self.dk.set_cenlock_sts(1)
        # 设置CarMode为Crash
        self.sd_tester.change_car_mode(3)
        sleep(11)
        self.partner.empty_all()
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 3}
        )
        self.partner.ck_s2s_event(
            CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 11}
        )
        self.partner.send_request_and_ck_resp(
            CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 11}
        )
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 3),
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsTrigSrc", 11),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("不同CarMode模式下中央锁定行为_Dyno（Outsoth）")
    @pytest.mark.full
    def test_caseid_110354(self):
        self.dk.set_cenlock_sts(1)
        # 设置CarMode为Dyno
        self.sd_tester.change_car_mode(5)
        sleep(0.5)
        self.partner.empty_all()
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3}
        )
        self.partner.ck_s2s_event(
            CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 10}
        )
        self.partner.send_request_and_ck_resp(
            CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 10}
        )
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 3),
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsTrigSrc", 10),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    # APA 请求内部其它方式闭锁
    @allure.title("被ASM请求锁定_内部锁定")
    @pytest.mark.sanity
    def test_caseid_110364(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 3}
        )
        self.partner.ck_s2s_event(
            CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 11}
        )
        self.partner.send_request_and_ck_resp(
            CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 11}
        )
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 3)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, "LockgCenStsTrigSrc", 11)
        sleep(3)

    @allure.title("被ASM请求解锁解防_内部解锁")
    @pytest.mark.sanity
    def test_caseid_110339(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 3}
        )
        self.partner.ck_s2s_event(
            CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 11}
        )
        self.partner.send_request_and_ck_resp(
            CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 11}
        )
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 1)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, "LockgCenStsTrigSrc", 11)
        sleep(3)

    @allure.title("被ASM请求锁定_外部锁定")
    @pytest.mark.sanity
    def test_caseid_110361(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3}
        )
        self.partner.ck_s2s_event(
            CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 10}
        )
        self.partner.send_request_and_ck_resp(
            CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 10}
        )
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 3)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, "LockgCenStsTrigSrc", 10)
        sleep(3)

    @allure.title("HMI闭锁_尾门解锁")
    @pytest.mark.sanity
    def test_caseid_114599(self):
        # 设置尾门ccp
        self.sd_tester.write_multi_ccp({97: 2, 98: 2})
        self.dk.set_cenlock_sts(0x1)
        sleep(1)
        self.partner.empty_all()
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2}
        )
        self.dk.ck_four_door_lock_cmd(2)
        sleep(1)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 3)
        self.ipdu.set(
            self.ipdu.bodycan.PotBodyFr02, "TrOpenerSts_0_PotBodySignalIPdu02", 9
        )  # 设置尾门全关
        sleep(2)
        self.partner.send_method_request(TAILGATESERVICE_CLIENT, "Open", {})
        self.ipdu.check(
            self.ipdu.bodycan.CemBodyFr02, "TrOpenerReqTrOpenerReq", 1
        )  # 设置调用尾门开启
        self.dk.set_door_opener_sts(0, 0, 0, 0, 5)  # 设置尾门全开
        sleep(1)
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 2
        )  # 中控锁状态为尾门解锁
        sleep(3)

    @allure.title("478749 v13 驻车舒享模式_NFC解锁成功触发源[InsOth]")
    @pytest.mark.sanity
    def test_caseid_1919332(self):
        self.dk.set_cenlock_sts(1)
        self.sd_tester.change_usage_mode(2)
        sleep(.1)
        self.partner.send_method_request(
            "VehicleModeService_client", "SetConvenienceModeDuration", {"duration": 1}
        )
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, "PrkgCmftModTiCtrl", 1)
        self.partner.empty_all(.5)
        self.dk.send_nfc_cmd()
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 3),
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsTrigSrc", 11),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("478749_v17驻车舒享模式_蓝牙闭锁触发源::InOth")
    @pytest.mark.sanity
    def test_caseid_1919336(self):
        self.dk.set_cenlock_sts(1)
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(
            "VehicleModeService_client", "SetConvenienceModeDuration", {"duration": 1}
        )
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, "PrkgCmftModTiCtrl", 1)
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 0}
        )
        self.dk.ck_four_door_lock_cmd(2)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 3),
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsTrigSrc", 11),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("478749_v17驻车舒享模式_蓝牙闭锁触发源::InOth")
    @pytest.mark.sanity
    def test_caseid_1919337(self):
        self.dk.set_cenlock_sts(1)
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(
            "VehicleModeService_client", "SetConvenienceModeDuration", {"duration": 1}
        )
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, "PrkgCmftModTiCtrl", 1)
        # 调用锁服务设置为Telm闭锁
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 1}
        )
        # 检查四门锁指令
        self.dk.ck_four_door_lock_cmd(2)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 3),
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsTrigSrc", 11),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)


    @allure.title("478749 v16 驻车舒享模式_离车落锁成功_中控锁状态+闭锁源信号监测")
    @pytest.mark.full
    def test_caseid_1919334(self):
        self.dk.set_cenlock_sts(1)
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(
            "VehicleModeService_client", "SetConvenienceModeDuration", {"duration": 1}
        )
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, "PrkgCmftModTiCtrl", 1)
        self.partner.send_method_request(
            "KeyService_client", "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]}
        )
        self.dk.send_walk_away_lock_cmd()
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 3),
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsTrigSrc", 11),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("478749 v4 驻车舒享模式 KV(PEPS)闭锁_闭锁源::InsOth")
    @pytest.mark.sanity
    def test_caseid_1919335(self):
        self.dk.set_cenlock_sts(1)
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(
            "VehicleModeService_client", "SetConvenienceModeDuration", {"duration": 1}
        )
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, "PrkgCmftModTiCtrl", 1)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0xA)])
        self.dk.press_door_outswitch(4, 2.5)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 3),
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsTrigSrc", 11),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("478749 v13 驻车舒享模式禁用_NFC解锁成功触发源[NFC]")
    @pytest.mark.sanity
    def test_caseid_1981001(self):
        self.dk.set_cenlock_sts(1)
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(
            "VehicleModeService_client", "SetConvenienceModeDuration", {"duration": 0}
        )
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18, "PrkgCmftModTiCtrl", 0)
        self.dk.send_nfc_cmd()
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 3),
            (self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsTrigSrc", 12),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)


