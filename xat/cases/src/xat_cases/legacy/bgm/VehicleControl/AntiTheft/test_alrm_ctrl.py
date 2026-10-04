# -*- coding:utf-8 -*-
"""
@File        : test_alrm_ctrl.py
@Author      : xiangyue.li@jiduatuo.com
@Time        : 2023/07/16 11:00 AM
@Description : BGM车控车设车辆防盗功能
"""

import allure
import pytest
import os
from time import sleep

from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
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


@allure.feature("车身网关测试/整车控制")
@allure.story("防盗")
# @pytest.mark.flaky(reruns=1, reruns_delay=2)
class TestCTDService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        partner_process_check()
        self.partner = S2sBaseClass(
            [("CTDService", "client"), ("CentralLockService", "client"),("FotaMasterService", "client")]
        )
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.ipdu.start_all_time_control()
        self.busapp.start_all_cyclic_msg()
        # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "VehMtnStVehMtnSt", 3)
        # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0
        )
        # self.ipdu.backbonefr_vddmbackbonefr03_gearlvrindcn_gearlvrindcn2_parkindcn()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, "GearLvrIndcn", 0)

        self.sd_tester = Sd_Tester(**self.tc_config)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.diagnostic_client_sim_start()
        self.sd_tester.tester_present()
        self.sd_tester.write_multi_ccp(
            {
                94: 0x80,
                98: 0x2,
                97: 0x2,
                10: 0x2,
                481: 0x4,
                578: 0x4,
                142: 0x83,  # 解闭锁相关
                64: 3,  # With Alarm Using Vehicle Horn 即siren，警报器
                543: 1,  # Without Battery Backed-Up Sounder 即BBS
                66: 1,  # Without inclination sensor 即IS倾斜传感器
                65: 1,  # Without Interior Motion Sensor 即内部运动传感器
                1: 0xA3,  # 适用配置了舒适泊车模式的车型，对应设防准备时间 30s
                69: 1,  # Re-trig次数，一个报警周期30s鸣笛停止10s
                70: 1,  # 无被动设防
                13: 4,  # 动力类型Battery electric vehicle，上切Active或Driving可解防
            }
        )
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

        # self.set_centrllock_to_lock()

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.all_door_close()
        self.ipdu.reset_check_results()
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        try:
            self.sd_tester.change_usage_mode(1)
            self.sd_tester.change_car_mode(0)
            self.dk.stop_listen_dk_bgm_response()
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
        self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        self.partner.stop_operators()
        self.sd_tester.stop_tester_present()
        self.sd_tester.diagnostic_client_sim_close()
        super().after_class(self, ecu)

    def all_door_close(self):
        self.io.pass_door_close()
        self.io.drvr_door_close()
        self.io.lere_door_close()
        self.io.rire_door_close()
        self.io.trunk_door_close()
        self.io.hood_door1_close()
        self.io.hood_door2_open()

    def set_centrllock_to_lock(self):
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
        sleep(1)
        self.partner.send_method_request(
            CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 0}
        )
        self.dk.ck_four_door_lock_cmd(2)
        sleep(1)
        self.dk.ck_cenlock_sts(0x3, 0x1)
        sleep(1)
        # self.dk.send_walk_away_lock_cmd()
        # sleep(1)
        # self.dk.ck_cenlock_sts(3)

    def check_singal_value_duration_time(self):
        result_ori = self.ipdu.check_signal(
            self.ipdu.bodycan.CemBodyFr03, "ActvnOfIndcrIndcrOut"
        )
        logger.info("result_original {}".format(result_ori))
        result_1 = get_signal_times_interval(result_ori, 3)
        logger.info("result_1(信号值为3):{}".format(result_1))
        if result_1[0] > 17 and result_1[0] < 23:
            assert True
        else:
            assert False

        result_2 = get_signal_times_interval(result_ori, 0)
        logger.info("result_2(信号值为0):{}".format(result_2))
        if result_2[0] > 15 and result_2[0] < 25:
            assert True
        else:
            assert False

        self.ipdu.reset_check_results()


    @allure.title("OTA升级防盗状态要处于Disarm状态")
    @pytest.mark.full
    def test_caseid_1979833(self):
        with allure.step(f"Step:模拟车辆OTA升级状态Event:(服务:FotaMasterService;函数名:Status,升级状态 = UPDATE&ROLLBACK"):
            self.partner.send_event_notify("FotaMasterService_client", 'Status', {"Status":{"taskId":123, "state":4, "errorCode":1}})
        with allure.step("检查AlrmStsAlrmSt=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr18,
                "AlrmStsAlrmSt",
                0,
            )        