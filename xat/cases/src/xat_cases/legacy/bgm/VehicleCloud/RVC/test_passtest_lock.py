#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_passtest_lock.py
@Time         :2024/07/22 16:55:31
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

CENTRALLOCK_SERVICE_CLIENT = "CentralLockService_client"
KEY_SERVICE_CLIENT = "KeyService_client"

@allure.feature("远程控制/远控两域联调测试/远控尾门")
@allure.story("远控尾门")
class TestRvcTailgate(TestBase):
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
        self.dk.set_drvr_seat_notpresent()
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
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

    @allure.title("远程控制成功率压力测试")
    @pytest.mark.sanity
    def test_caseid_1984973(self):
         # 设置整车上锁
        self.dk.set_cenlock_sts(0x1)
        self.sd_tester.change_usage_mode(0x1)
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