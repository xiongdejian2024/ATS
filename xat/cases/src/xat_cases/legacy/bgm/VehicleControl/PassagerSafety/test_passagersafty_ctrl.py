# -*- coding: utf-8 -*-
"""
@File        : test_passagersafty_ctrl.py
@Author      : xiangyue.li@jiduauto.com
@Time        : 2023/05/10 15:00 PM
@Description :
"""
import os
import sys

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
sys.path.append(os.path.join(os.getcwd(), "../../../.."))
current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path.split("sat")[0], "sat"))

# from test_case.bgm.case_helper.partner_const import *
import pytest
from time import sleep
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.common.data_type_handing import logger
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_cases.legacy.soa.case_helper.case_tool import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey

SEAT_SERVICE_CLIENT = "SeatService_client"
CHASSIS_SERVICE_CLIENT = "ChassisService_client"


@allure.feature("整车控制乘客安全")
@allure.story("整车控制/PassengerSafety")
class TestPassengerSafety(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        sleep(1)
        partner_process_check()
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass(
            [("SeatService", "client"), ("WTIService", "client"),("ChassisService","client")]
        )
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set_vehspd(0.0)
        sleep(1)
        # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "VehMtnStVehMtnSt", 3)
        # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0
        )

        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文

        sleep(2)
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.sd_tester.update_serverdoipid(0x1002)
        sleep(0.1)
        self.sd_tester.diagnostic_client_sim_start()
        sleep(0.1)
        self.sd_tester.tester_present()
        sleep(1)

    def set_vddm_pre_condition(self):
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
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0
        )
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, "GearLvrIndcn", 0)
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06",
            3,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr00,
            "VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00",
            3,
        )
        self.io.set_four_door_close()
        sleep(1)
        self.partner.empty_all()
        sleep(1)

    def after_each_func(self, ecu):
        self.sd_tester.stop_tester_present()
        sleep(0.5)
        self.io.set_four_door_close()
        try:
            self.sd_tester.change_usage_mode(1)
            sleep(0.5)
            self.sd_tester.change_car_mode(0)
        except Exception as e:
            logger.error(e)
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        try:
            self.sd_tester.change_usage_mode(1)
            self.sd_tester.change_car_mode(0)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        self.sd_tester.diagnostic_client_sim_close()
        self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
        self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，总线开始收发报文
        super().after_class(self, ecu)

    @allure.title("后排安全带报警状态_右后排安全带二级级告警status==3后座椅占位消失安全带状态监测state==1")
    @pytest.mark.full
    def test_caseid_113099(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecRi_0_SRSBackBoneSignalIPdu04",
            2,
        )

        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        # 设置车速v>22km/h
        self.ipdu.set_vehspd(6.3)
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 6, "status": 3}]},
        )
        # 设置右后座椅无占位
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecRi_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 6, "status": 1}]},
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_中后排安全带二级级告警status==3后座椅占位消失安全带状态监测state==1")
    @pytest.mark.full
    def test_caseid_113100(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecMid_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        # 设置车速v>22km/h
        self.ipdu.set_vehspd(6.3)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 5, "status": 3}]},
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecMid_0_SRSBackBoneSignalIPdu04",
            3,
        )
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 5, "status": 1}]},
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_左后排安全带二级级告警status==3后座椅占位消失安全带状态监测state==1")
    @pytest.mark.full
    def test_caseid_113101(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecLe_0_SRSBackBoneSignalIPdu04",
            2,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        # 设置车速v>22km/h
        self.ipdu.set_vehspd(6.3)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 4, "status": 3}]},
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecLe_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 4, "status": 1}]},
        )
        sleep(3)
        
    @allure.title("492245_驾驶员通讯安全机制ASIL A")
    @pytest.mark.full
    def test_caseid_1919207(self):
        self.io.drvr_door_close()
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "DoorDrvrStsWithFacQlyDoorSts", 2)
        self.io.drvr_door_open()
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "DoorDrvrStsWithFacQlyDoorSts", 1)

        
    @allure.title("471557、471555、471474_功能安全_制动踏板踩下驾驶员质量因子监测Qf==3::ASIL B")
    @pytest.mark.smoke
    # BltLockStSafeAtDrvrBltLockStErrSts==0 则  & BltLockStAtDrvrBltLockSt1 ==1
    def test_caseid_1960104(self):
        self.sd_tester.change_usage_mode(13)
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsntQf", 1
        )
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdQf", 3)
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 1
        )
        sleep(0.5)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsnt", 2),
            (self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsntQf", 3),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)
        
    @allure.title("主驾无占座/有占座安全带已系报警监测state==1")
    @pytest.mark.smoke
    def test_caseid_113191(self):
        self.partner.empty_all()
        sleep(0.5)
        # 车内无占座state=1无报警
        self.dk.set_drvr_seat_notpresent()
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [0]},
            {"out": [{"id": 0, "status": 1}]},
        )

        sleep(0.5)
        self.io.driver_seat_present()  # 设置主驾占座
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )  # 安全带无故障
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 1
        )  # 设置主驾安全带已系
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [0]},
            {"out": [{"id": 0, "status": 1}]},
        )
        sleep(3)

    @allure.title("副驾无占座/有占座安全带已系报警监测status==1")
    @pytest.mark.smoke
    def test_caseid_1913510(self):
        self.partner.empty_all()
        sleep(0.5)
        # 车内无占座status=1无报警
        self.dk.set_pass_seat_notpresent()
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [1]},
            {"out": [{"id": 1, "status": 1}]},
        )
        # 设置副驾有占座&&安全带已系
        self.dk.set_pass_seat_present()
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [1]},
            {"out": [{"id": 1, "status": 1}]},
        )
        sleep(3)

    @allure.title("安全带报警状态_convenience模式j&&前排有乘客占位且安全带未系status==2")
    @pytest.mark.smoke
    def test_caseid_1982017(self):
        self.partner.empty_all()
        sleep(0.5)
        # convenience及以上模式下主副驾有占座前排安全带未系设置
        self.sd_tester.change_usage_mode(11)
        sleep(1)
        self.io.driver_seat_present()
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "PassSeatSts_0_SRSBackBoneSignalIPdu04",
            2,
        )
        sleep(0.5)

        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 0
        )
        self.partner.ck_s2s_event(
            SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 0, "warn": 2}
        )

        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.partner.ck_s2s_event(
            SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 1, "warn": 2}
        )

        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 2}]},
        )

        sleep(1)
        self.partner.send_request_and_ck_resp(
            WTI_SERVICE_CLIENT,
            "GetWarningMsgList",
            {},
            {"out": [{"name": "Driver Seat Belt Warning", "info": "1"}]},
        )
        sleep(3)

    @allure.title("前排主驾安全带报警状态_车速大于等于22km/h安全带未系State=3状态监测")
    @pytest.mark.smoke
    def test_caseid_113182(self):
        self.partner.empty_all()
        sleep(0.5)
        # 设置usgmod为drving
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        self.io.driver_seat_present()
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "PassSeatSts_0_SRSBackBoneSignalIPdu04",
            2,
        )
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 0
        )
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(1)
        # 设置车速超过22km/h,约6.2m/s
        self.ipdu.set_vehspd(6.2)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 3}, {"id": 1, "status": 3}]},
        )
        sleep(3)

    @allure.title("前排主驾安全带报警状态_行驶时间50s≤T<80s安全带未系State=3状态监测")
    @pytest.mark.sanity
    def test_caseid_113172(self):
        self.partner.empty_all()
        sleep(0.5)
        # 设置usgmod为drving
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        self.io.driver_seat_present()
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "PassSeatSts_0_SRSBackBoneSignalIPdu04",
            2,
        )
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 0
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        # 设置行驶时间50s≤T<80s
        self.ipdu.set_vehspd(3.6)
        sleep(71)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 3}, {"id": 1, "status": 3}]},
        )
        sleep(3)

    @allure.title("前排安全带报警状态_行驶时间超过80s安全带未系状态监测state==4")
    @pytest.mark.sanity
    def test_caseid_113175(self):
        self.partner.empty_all()
        sleep(0.5)
        # 设置usgmod为drving
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        self.io.driver_seat_present()
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "PassSeatSts_0_SRSBackBoneSignalIPdu04",
            2,
        )
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 0
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set_vehspd(3.6)  # 车速低于22km/h
        # 设置行驶时间T>80s
        sleep(81)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 4}, {"id": 1, "status": 4}]},
        )
        sleep(3)

    @allure.title("前排主驾安全带报警状态_车速大于等于V>=35km/hState=4状态监测")
    @pytest.mark.sanity
    def test_caseid_1959936(self):
        self.partner.empty_all()
        sleep(0.5)
        # 设置usgmod为drving
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        self.io.driver_seat_present()
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "PassSeatSts_0_SRSBackBoneSignalIPdu04",
            2,
        )
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(1)
        # 设置车速V>=35km/h
        self.ipdu.set_vehspd(9.8)
        sleep(2)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 4}, {"id": 1, "status": 4}]},
        )
        sleep(3)
        self.partner.ck_s2s_event("WTIService_client", "TelltaleList", {"list": [{"name": "Seat Belt", "state": "3"}]},timeout=5)
        self.partner.send_request_and_ck_resp("WTIService_client", "GetTelltaleList", {},
                                          {"out": [{"name": "Seat Belt", "state": "3"}]})
        self.ipdu.set_vehspd(0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.partner.ck_s2s_event("WTIService_client", "TelltaleList", {"list": [{"name": "Seat Belt", "state": "0"}]},timeout=5)
        self.partner.send_request_and_ck_resp("WTIService_client", "GetTelltaleList", {},
                                          {"out": [{"name": "Seat Belt", "state": "0"}]})        
        
        
        
        
    @allure.title("前排安全带报警状态_安全带未系二级最终听觉超过95s，安全带告警状态监测state==2")
    @pytest.mark.sanity
    def test_caseid_113177(self):
        self.partner.empty_all()
        sleep(0.5)
        # 设置usgmod为drving
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        self.io.driver_seat_present()
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "PassSeatSts_0_SRSBackBoneSignalIPdu04",
            2,
        )
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(1)
        # 设置车速V>=35km/h
        self.ipdu.set_vehspd(9.8)
        sleep(2)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 4}, {"id": 1, "status": 4}]},
        )
        sleep(95)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 2}, {"id": 1, "status": 2}]},
        )
        sleep(3)

    @allure.title("安全带报警状态_一级告警status==2后安全带已系，告警状态监测state==1")
    @pytest.mark.smoke
    def test_caseid_1959937(self):
        self.partner.empty_all()
        sleep(0.5)
        # convenience模式下主副驾有占座前排安全带未系设置
        self.sd_tester.change_usage_mode(11)
        sleep(0.5)
        self.io.driver_seat_present()
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "PassSeatSts_0_SRSBackBoneSignalIPdu04",
            2,
        )
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 2}, {"id": 1, "status": 2}]},
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 1}, {"id": 1, "status": 1}]},
        )
        sleep(3)

    @allure.title("前排安全带报警状态_进入二级初始听觉安全带系上，安全带告警状态监测state==1")
    @pytest.mark.sanity
    def test_caseid_113152(self):
        self.partner.empty_all()
        sleep(0.5)
        # 设置usgmod为drving
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        self.io.driver_seat_present()
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "PassSeatSts_0_SRSBackBoneSignalIPdu04",
            2,
        )
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 0
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        # 设置车速超过22km/h
        self.ipdu.set_vehspd(7.0)
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 3}, {"id": 1, "status": 3}]},
        )

        # status =3主副驾系上安全带
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 1
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 1}, {"id": 1, "status": 1}]},
        )
        sleep(3)

    @allure.title("前排安全带报警状态_进入二级报警最终听觉后安全带系上，安全带告警状态监测state==1")
    @pytest.mark.sanity
    def test_caseid_113134(self):
        self.partner.empty_all()
        sleep(0.5)
        # 设置usgmod为drving
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        self.io.driver_seat_present()
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "PassSeatSts_0_SRSBackBoneSignalIPdu04",
            2,
        )
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 0
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        # 设置车速超过35km/h
        self.ipdu.set_vehspd(9.8)
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 4}, {"id": 1, "status": 4}]},
        )

        # status =3主副驾系上安全带
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 1
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 1}, {"id": 1, "status": 1}]},
        )
        sleep(3)

    @allure.title("前排安全带报警状态_进入二级初始听觉后UsgMod模式下切state==1")
    @pytest.mark.sanity
    def test_caseid_113136(self):
        self.partner.empty_all()
        sleep(0.5)
        # 设置usgmod为drving
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        self.io.driver_seat_present()
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "PassSeatSts_0_SRSBackBoneSignalIPdu04",
            2,
        )
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 0
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        # 设置车速超过22km/h
        self.ipdu.set_vehspd(7.0)
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 3}, {"id": 1, "status": 3}]},
        )
        sleep(1)
        self.ipdu.set_vehspd(0)
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr00,
            "VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00",
            3,
        )
        sleep(0.5)
        self.sd_tester.change_usage_mode(0x1)
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 1}, {"id": 1, "status": 1}]},
        )
        sleep(3)

    @allure.title("GID-584086_前排安全带报警状态_进入二级初始听觉后前排无占座告警状态监测state==1")
    @pytest.mark.sanity
    def test_caseid_113150(self):
        self.partner.empty_all()
        sleep(0.5)
        # 设置usgmod为drving
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        self.io.driver_seat_present()
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "PassSeatSts_0_SRSBackBoneSignalIPdu04",
            2,
        )
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 0
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        # 设置车速超过22km/h
        self.ipdu.set_vehspd(7.0)
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 3}, {"id": 1, "status": 3}]},
        )
        sleep(1)
        self.ipdu.set_vehspd(0)
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr00,
            "VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00",
            3,
        )
        sleep(0.5)
        # 车辆静止
        self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.sd_tester.change_usage_mode(0x2)
        self.dk.set_drvr_seat_notpresent()
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "PassSeatSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 1}, {"id": 1, "status": 1}]},
        )
        sleep(3)
        
    @allure.title("安全带报警状态_主驾无占座/有占座安全带已系status==1后安全带故障监测state==5")
    @pytest.mark.smoke
    def test_caseid_1959939(self):
        self.partner.empty_all()
        sleep(0.5)
        # 车内无占座state=1无报警
        self.dk.set_drvr_seat_notpresent()
        sleep(0.5)
        self.io.driver_seat_present()  # 设置主驾占座
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )  # 安全带无故障
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 1
        )  # 设置主驾安全带已系
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 1}, {"id": 1, "status": 1}]},
        )
        # 设置主副驾安全带故障&&UsageMode≥Convenience
        self.sd_tester.change_usage_mode(0xB)
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 5}, {"id": 1, "status": 5}]},
        )
        sleep(3)

    @allure.title("安全带报警状态_前排告警状态status==2后安全带故障状态监测status==5")
    @pytest.mark.smoke
    def test_caseid_1959940(self):
        self.partner.empty_all()
        sleep(0.5)
        # convenience及以上模式主副驾有占座前排安全带未系设置
        self.sd_tester.change_usage_mode(0x2)
        sleep(1)
        self.io.driver_seat_present()
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "PassSeatSts_0_SRSBackBoneSignalIPdu04",
            2,
        )
        sleep(0.5)

        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 0
        )
        self.partner.ck_s2s_event(
            SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 0, "warn": 2}
        )

        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 2}, {"id": 1, "status": 2}]},
        )
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 5}, {"id": 1, "status": 5}]},
        )
        sleep(3)

    @allure.title("安全带报警状态_安全带告警状态status==4后安全带故障状态监测status==5")
    @pytest.mark.sanity
    def test_caseid_1959941(self):
        self.partner.empty_all()
        sleep(0.5)
        # 设置usgmod为drving
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        self.io.driver_seat_present()
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "PassSeatSts_0_SRSBackBoneSignalIPdu04",
            2,
        )
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 0
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set_vehspd(9.8)  # 车速V>35km35km/h
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 4}, {"id": 1, "status": 4}]},
        )
        # 设置主副驾a
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 5}, {"id": 1, "status": 5}]},
        )
        sleep(3)

    @allure.title("前排安全带报警状态_安全带告警State=3后安全带故障告警状态监测status==5")
    @pytest.mark.sanity
    def test_caseid_1959942(self):
        self.partner.empty_all()
        sleep(0.5)
        # 设置usgmod为drving
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        self.io.driver_seat_present()
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "PassSeatSts_0_SRSBackBoneSignalIPdu04",
            2,
        )
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 0
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        # 设置车速V>22km/h
        self.ipdu.set_vehspd(6.2)
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 3}, {"id": 1, "status": 3}]},
        )
        #  设置安全带故障
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 5}, {"id": 1, "status": 5}]},
        )
        sleep(3)

    @allure.title("GID-584086_前排安全带报警状态_安全带告警初始听觉state3后车速低于10km/h&&四门任意门状态改变，告警状态检测state==1")
    @pytest.mark.full
    def test_caseid_1959938(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0x2)
        sleep(1)
        self.io.driver_seat_present()
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "PassSeatSts_0_SRSBackBoneSignalIPdu04",
            2,
        )
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 0
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 3)
        # 设置车速V>22km/h
        self.ipdu.set_vehspd(6.2)
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 3}, {"id": 1, "status": 3}]},
        )
        self.ipdu.set_vehspd(2.5)
        self.io.drvr_door_open()
        sleep(3)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 1}, {"id": 1, "status": 1}]},
        )
        
    @allure.title("GID-584086_前排安全带报警状态_state==3超过30s,告警状态监测status==4")
    @pytest.mark.sanity
    def test_caseid_113164(self):
        self.partner.empty_all()
        sleep(0.5)
        # 设置usgmod为drving
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        self.io.driver_seat_present()
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "PassSeatSts_0_SRSBackBoneSignalIPdu04",
            2,
        )
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 0
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        # 设置车速V>22km/h
        self.ipdu.set_vehspd(6.2)
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 3}, {"id": 1, "status": 3}]},
        )
        sleep(35)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 4}, {"id": 1, "status": 4}]},
        )
        sleep(3)
        
    @allure.title("后排安全带报警状态监测_后排左侧座椅无占位告警状态监测state==1")
    @pytest.mark.smoke
    def test_caseid_113131(self):
        self.partner.empty_all()
        sleep(0.5)
        # 车内无占座state=1无报警
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSts_0_SRSBackBoneSignalIPdu04",
            3,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [4]},
            {"out": [{"id": 4, "status": 1}]},
        )

        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {
                "out": [
                    {"id": 4, "status": 1},
                    {"id": 5, "status": 1},
                    {"id": 6, "status": 1},
                ]
            },
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_后排中座椅无占位告警状态监测state==1")
    @pytest.mark.sanity
    def test_caseid_113130(self):
        self.partner.empty_all()
        sleep(0.5)
        # 车内无占座state=1无报警
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecMid_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [5]},
            {"out": [{"id": 5, "status": 1}]},
        )

        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {
                "out": [
                    {"id": 4, "status": 1},
                    {"id": 5, "status": 1},
                    {"id": 6, "status": 1},
                ]
            },
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_后排右侧座椅无占位告警状态监测state==1")
    @pytest.mark.smoke
    def test_caseid_113129(self):
        self.partner.empty_all()
        sleep(0.5)
        # 车内无占座state=1无报警
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecRi_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [6]},
            {"out": [{"id": 6, "status": 1}]},
        )

        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {
                "out": [
                    {"id": 4, "status": 1},
                    {"id": 5, "status": 1},
                    {"id": 6, "status": 1},
                ]
            },
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_后排左侧有占座&&安全带无故障&&安全带已系告警状态监测state==1")
    @pytest.mark.sanity
    def test_caseid_113128(self):
        self.partner.empty_all()
        sleep(0.5)
        # 设置座椅有占座&&安全带无故障&&安全带已系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSts_0_SRSBackBoneSignalIPdu04",
            1,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSt1_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [4]},
            {"out": [{"id": 4, "status": 1}]},
        )

        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {
                "out": [
                    {"id": 4, "status": 1},
                    {"id": 5, "status": 1},
                    {"id": 6, "status": 1},
                ]
            },
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_后排右侧有占座&&安全带无故障&&安全带已系告警状态监测state==1")
    @pytest.mark.sanity
    def test_caseid_113126(self):
        self.partner.empty_all()
        sleep(0.5)
        # 设置座椅有占座&&安全带无故障&&安全带已系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecRi_0_SRSBackBoneSignalIPdu04",
            2,
        )

        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSt1_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {
                "out": [
                    {"id": 4, "status": 1},
                    {"id": 5, "status": 1},
                    {"id": 6, "status": 1},
                ]
            },
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_后排中有占座&&安全带无故障&&安全带已系告警状态监测state==1")
    @pytest.mark.smoke
    def test_caseid_113127(self):
        self.partner.empty_all()
        sleep(0.5)
        # 设置座椅有占座&&安全带无故障&&安全带已系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecMid_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {
                "out": [
                    {"id": 4, "status": 1},
                    {"id": 5, "status": 1},
                    {"id": 6, "status": 1},
                ]
            },
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_convenience模式后排左侧有占座&&安全带无故障&&安全带已系告警状态监测state==2")
    @pytest.mark.smoke
    def test_caseid_113125(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0x2)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecLe_0_SRSBackBoneSignalIPdu04",
            2,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 4, "status": 2}]},
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_convenience及以上模式后排右侧有占座&&安全带无故障&&安全带已系告警状态监测state==2")
    @pytest.mark.smoke
    def test_caseid_113123(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xB)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecRi_0_SRSBackBoneSignalIPdu04",
            2,
        )

        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 6, "status": 2}]},
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_convenience及以上模式后排右侧中间座椅占座&&安全带无故障&&安全带已系告警状态监测state==2")
    @pytest.mark.smoke
    def test_caseid_113124(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecMid_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 5, "status": 2}]},
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_表显车速V>=22km/h中后排安全带未系告警状态监测status==3")
    @pytest.mark.sanity
    def test_caseid_113118(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecMid_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        # 设置车速v>22km/h
        self.ipdu.set_vehspd(6.3)
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 5, "status": 3}]},
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_表显车速V>=22km/h左后排安全带未系告警状态监测status==3")
    @pytest.mark.smoke
    def test_caseid_113119(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecLe_0_SRSBackBoneSignalIPdu04",
            2,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        # 设置车速v>22km/h
        self.ipdu.set_vehspd(6.3)
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 4, "status": 3}]},
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_表显车速V>=22km/h右后排安全带未系告警状态监测status==3")
    @pytest.mark.smoke
    def test_caseid_113117(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecRi_0_SRSBackBoneSignalIPdu04",
            2,
        )

        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        # 设置车速v>22km/h
        self.ipdu.set_vehspd(6.3)
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 6, "status": 3}]},
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_行驶时间T>=50s左后排安全带未系告警状态监测status==3")
    @pytest.mark.sanity
    def test_caseid_113122(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecLe_0_SRSBackBoneSignalIPdu04",
            2,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        # 设置车速v<22km/h
        self.ipdu.set_vehspd(3.0)
        sleep(51)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 4, "status": 3}]},
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_行驶时间T>=50s右后排安全带未系告警状态监测status==3")
    @pytest.mark.sanity
    def test_caseid_113120(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecRi_0_SRSBackBoneSignalIPdu04",
            2,
        )

        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        # 设置车速v<22km/h
        self.ipdu.set_vehspd(3.0)
        sleep(51)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 6, "status": 3}]},
        )
        sleep(3)

    @allure.title("GID-584086_后排安全带报警状态_行驶时间T>=50s中后排安全带未系告警状态监测status==3")
    @pytest.mark.sanity
    def test_caseid_113121(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecMid_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        # 设置车速v>22km/h
        self.ipdu.set_vehspd(6.3)
        sleep(35)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 5, "status": 3}]},
        )
        sleep(3)
                
    @allure.title("后排安全带报警状态监测_中后排安全带二级级告警status==3超过35S告警状态监测state==2")
    @pytest.mark.sanity
    def test_caseid_113115(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecMid_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        # 设置车速v>22km/h
        self.ipdu.set_vehspd(6.3)
        sleep(35)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 5, "status": 2}]},
        )
        sleep(3)

    @allure.title("GID-584086_后排安全带报警状态_左后安全带告警表显车速V<10km/h主驾门开安全带告警状态监测")
    @pytest.mark.full
    def test_caseid_113098(self):
        self.partner.empty_all()
        self.sd_tester.change_usage_mode(2)
        self.sd_tester.change_usage_mode(0xD)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecLe_0_SRSBackBoneSignalIPdu04",
            2,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        # 设置车速v>22km/h
        self.ipdu.set_vehspd(6.3)

        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 4, "status": 3}]},
        )
        # 设置车速v<10km/h
        self.ipdu.set_vehspd(0)
        self.sd_tester.change_usage_mode(2)
        self.sd_tester.change_usage_mode(1)
        self.io.lere_door_close()
        self.io.lere_door_open()
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 4, "status": 1}]},
        )       

    @allure.title("GID-584086_前排安全带报警状态_进入二级报警后车速下降并且车门状态发生改变可见反馈")
    @pytest.mark.full
    def test_caseid_113135(self):
        self.partner.empty_all()
        self.sd_tester.change_usage_mode(2)
        self.io.driver_seat_present()
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "PassSeatSts_0_SRSBackBoneSignalIPdu04",
            2,
        )
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 0
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set_vehspd(7.0)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 3}, {"id": 1, "status": 3}]},
        )
        self.ipdu.set_vehspd(0)
        self.io.lere_door_close()
        self.io.lere_door_open()
        self.sd_tester.change_usage_mode(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 1}, {"id": 1, "status": 1}]},
        )    
        
    @allure.title("后排安全带报警状态监测_左后排安全带二级级告警status==3超过35S告警状态监测state==2")
    @pytest.mark.sanity
    def test_caseid_113116(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecLe_0_SRSBackBoneSignalIPdu04",
            2,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        # 设置车速v>22km/h
        self.ipdu.set_vehspd(6.3)
        sleep(35)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 4, "status": 2}]},
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_右后排安全带二级级告警status==3超过35S告警状态监测state==2")
    @pytest.mark.smoke
    def test_caseid_113114(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecRi_0_SRSBackBoneSignalIPdu04",
            2,
        )

        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        # 设置车速v>22km/h
        self.ipdu.set_vehspd(6.3)
        sleep(35)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 6, "status": 2}]},
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_左后安全带进入一级告警status==2后安全带系上告警status==1")
    @pytest.mark.sanity
    def test_caseid_113107(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0x2)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecLe_0_SRSBackBoneSignalIPdu04",
            2,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 4, "status": 2}]},
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSt1_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 4, "status": 1}]},
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_右后安全带进入一级告警status==2后安全带系上告警状态监测state==1")
    @pytest.mark.smoke
    def test_caseid_113105(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xB)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecRi_0_SRSBackBoneSignalIPdu04",
            2,
        )

        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 6, "status": 2}]},
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSt1_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 6, "status": 1}]},
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_中后安全带进入一级告警status==2后安全带系上告警状态监测state==1")
    @pytest.mark.sanity
    def test_caseid_113106(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecMid_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 5, "status": 2}]},
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSt1_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 5, "status": 1}]},
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_左后安全带进入一级告警status==2后模式下切告警状态监测state==1")
    @pytest.mark.sanity
    def test_caseid_113110(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecMid_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 5, "status": 2}]},
        )
        sleep(0.5)
        # 模式下切至InActiv
        self.sd_tester.change_usage_mode(0x1)
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 5, "status": 1}]},
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_右后安全带进入一级告警status==2后对应座椅无占位告警状态监测state==1")
    @pytest.mark.sanity
    def test_caseid_113108(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xB)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecRi_0_SRSBackBoneSignalIPdu04",
            2,
        )

        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 6, "status": 2}]},
        )
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecRi_0_SRSBackBoneSignalIPdu04",
            3,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 6, "status": 1}]},
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_中后安全带进入一级告警status==2后安全带系上告警状态监测state==1")
    @pytest.mark.sanity
    def test_caseid_113109(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecMid_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 5, "status": 2}]},
        )
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecMid_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 5, "status": 1}]},
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_表显车速V>=22km/h右后排安全带未系告警状态监测status==3")
    @pytest.mark.smoke
    def test_caseid_113117(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecRi_0_SRSBackBoneSignalIPdu04",
            2,
        )

        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        # 设置车速v>22km/h
        self.ipdu.set_vehspd(6.3)
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 6, "status": 3}]},
        )
        sleep(3)
        
    @allure.title("后排安全带报警状态监测_左后安全带一级告警status==2&&UsgMod==Active后安全带故障监测status==5")
    @pytest.mark.smoke
    def test_caseid_113095(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xB)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecLe_0_SRSBackBoneSignalIPdu04",
            2,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 4, "status": 2}]},
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSts_0_SRSBackBoneSignalIPdu04",
            1,
        )
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 4, "status": 5}]},
        )
        sleep(3)

    @allure.title(
        "Driving_后排安全带报警状态_中后安全带告警status==3后安全带故障_告警状态监测SeatBeltWarning.State=5"
    )
    @pytest.mark.sanity
    def test_caseid_113094(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecMid_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        # 设置车速v>22km/h
        self.ipdu.set_vehspd(6.3)
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 5, "status": 3}]},
        )
        # 设置中后排安全带故障
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 5, "status": 5}]},
        )
        sleep(3)

    @allure.title("GID-584086_前排安全带报警状态_安全带告警status==3&&convenience以上模式车辆处于P档前排安全带告警状态监测status==2")
    @pytest.mark.sanity
    def test_caseid_113132(self):
        self.partner.empty_all()
        sleep(0.5)
        # 设置usgmod为drving
        self.sd_tester.change_usage_mode(0xD)
        sleep(1)
        self.io.driver_seat_present()
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "PassSeatSts_0_SRSBackBoneSignalIPdu04",
            2,
        )
        sleep(0.5)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 0
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 3)
        # 设置车速V>22km/h
        self.ipdu.set_vehspd(6.2)
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 3}, {"id": 1, "status": 3}]},
        )
        self.ipdu.set_vehspd(0)
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr00,
            "VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00",
            3,
        )
        sleep(0.5)
        # 车辆静止
        self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.sd_tester.change_usage_mode(0x2)
        # 车辆处于P挡GearLvrIndcn（backbonefr.VddmBackBoneFr03)=0(GearLvrIndcn2_ParkIndcn) and TrsmParkLockd(backbonefr.VddmBackBoneFr18) = 0(TrsmParkLock1_ParkNotEngd)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 0)
        sleep(3)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [3]},
            {"out": [{"id": 0, "status": 2}, {"id": 1, "status": 2}]},
        )
                       
    @allure.title("后排安全带报警状态监测_后排右侧告警状态state==1&&UsgMod=covenience后安全带故障监测status==5")
    @pytest.mark.smoke
    def test_caseid_113093(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0x2)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带已系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecRi_0_SRSBackBoneSignalIPdu04",
            2,
        )

        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSt1_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 6, "status": 1}]},
        )
        # 设置安全带故障
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSts_0_SRSBackBoneSignalIPdu04",
            1,
        )
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 6, "status": 5}]},
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_安全带告警Status==5&&UsgMod<Covenience故障后恢复告警状态监测Status==1")
    @pytest.mark.smoke
    def test_caseid_113092(self):
        """
        1、先设置安全带无告警status==1
        2、再设置后排安全带故障Status==5
        3、最后再设置安全带无故障&&模式小于covenience，监测状态机告警状态status值为1
        """
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0x2)
        sleep(1)
        # 后排左
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSts_0_SRSBackBoneSignalIPdu04",
            1,
        )
        # 后排中
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04",
            1,
        )
        # 后排右
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSts_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {
                "out": [
                    {"id": 4, "status": 5},
                    {"id": 5, "status": 5},
                    {"id": 6, "status": 5},
                ]
            },
        )
        sleep(1)
        # 设置安全带故障恢复
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.sd_tester.change_usage_mode(0x1)
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {
                "out": [
                    {"id": 4, "status": 1},
                    {"id": 5, "status": 1},
                    {"id": 6, "status": 1},
                ]
            },
        )
        sleep(3)


    @allure.title("后排安全带报警状态监测_安全带告警Status==5&&UsgMod=Inactive故障后恢复告警状态监测Status==1")
    @pytest.mark.sanity
    def test_caseid_1959950(self):
        """
        1、先设置安全带无告警status==1
        2、再设置后排安全带故障Status==5
        3、最后再设置安全带无故障&&模式小于convenience，监测状态机告警状态status值为1
        """
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0x2)
        sleep(1)
        # 后排左
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSts_0_SRSBackBoneSignalIPdu04",
            1,
        )
        # 后排中
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04",
            1,
        )
        # 后排右
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSts_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {
                "out": [
                    {"id": 4, "status": 5},
                    {"id": 5, "status": 5},
                    {"id": 6, "status": 5},
                ]
            },
        )
        sleep(1)
        # 设置安全带故障恢复
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.sd_tester.change_usage_mode(0x1)
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {
                "out": [
                    {"id": 4, "status": 1},
                    {"id": 5, "status": 1},
                    {"id": 6, "status": 1},
                ]
            },
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_车辆处于P档UsgMod>=convenience&&右后排安全带未系安全带状态监测status==2")
    @pytest.mark.smoke
    def test_caseid_113111(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0x2)
        # 设置挡位为P档
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, "GearLvrIndcn", 0)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecRi_0_SRSBackBoneSignalIPdu04",
            2,
        )

        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 6, "status": 2}]},
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_车辆处于P档UsgMod>=convenience&&中后排安全带未系安全带状态监测status==2")
    @pytest.mark.sanity
    def test_caseid_113112(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xD)
        # 设置挡位为P档
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, "GearLvrIndcn", 0)
        sleep(1)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecMid_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 5, "status": 2}]},
        )
        sleep(3)

    @allure.title("后排安全带报警状态监测_车辆处于P档UsgMod>=convenience&&左后排安全带未系安全带状态监测status==2")
    @pytest.mark.sanity
    def test_caseid_113113(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xB)
        # 设置挡位为P档
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, "GearLvrIndcn", 0)
        sleep(0.5)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecLe_0_SRSBackBoneSignalIPdu04",
            2,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 4, "status": 2}]},
        )

        sleep(3)

    @allure.title("471557_功能安全_制动踏板信号监测BrkPedlPsdQf==3，刹车踏板认为有效")
    @pytest.mark.smoke
    def test_caseid_1960105(self):
        # 设置usgmod为Active及以上
        self.sd_tester.change_usage_mode(11)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdQf", 0)
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 1
        )
        sleep(0.3)
        self.ipdu.check_signal(
            self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 0
        )
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdQf", 1)
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 1
        )
        sleep(0.3)
        self.ipdu.check_signal(
            self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 0
        )
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdQf", 2)
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 1
        )
        sleep(0.3)
        self.ipdu.check_signal(
            self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 0
        )
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdQf", 3)
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 1
        )
        sleep(0.3)
        self.ipdu.check_signal(
            self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 1
        )
        sleep(3)

    @allure.title("471554_乘客安全_功能安全_避免意外踩踏板")
    @pytest.mark.smoke
    def test_caseid_1960138(self):
        """
        只有安全带扣上，车门锁上的情况下，才考虑加速踏板信号 AccrPedlPsd和刹车踏板信号 BrkPedlPsd
        """
        self.sd_tester.change_usage_mode(13)
        sleep(1)

        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdQf", 3)
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 1
        )
        sleep(0.5)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsnt", 2),
            (self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsntQf", 3),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(1)
        self.io.drvr_door_open()
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr06, "DoorDrvrStsWithFacQlyDoorSts", 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 1
        )  # 安全带有故障
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 0
        )# 安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStSafeAtDrvrBltLockSt1", 0
        )# 安全带未系
        sleep(0.5)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsnt", 1),
            (self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsntQf", 1),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    @allure.title("471555_功能安全_车速V>15km/h驾驶员质量因子监测Qf==3::ASIL B")
    @pytest.mark.smoke
    def test_caseid_1960140(self):
        self.io.drvr_door_open()
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr06, "DoorDrvrStsWithFacQlyDoorSts", 1
        )
        # 设置usgmod为Active及以上
        self.sd_tester.change_usage_mode(13)
        sleep(1)
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsntQf", 1
        )
        sleep(0.5)
        # 设置车速v>15km/h
        self.ipdu.set_vehspd(4.2)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsnt", 2),
            (self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsntQf", 3),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)

    # @allure.title("安全带报警状态_convenience模式&&前排有乘客占位且安全带未系status==2")
    # @pytest.mark.smoke
    # def test_caseid_1982017(self):
    #     self.partner.empty_all()
    #     sleep(0.5)
    #     self.sd_tester.change_usage_mode(0x2)
    #     sleep(1)
    #     # 设置座椅有占座&&安全带无故障&&安全带未系
        # self.dk.set_drvr_seat_present()
        # self.ipdu.backbonefr_srsbackbonefr04_passseatsts_0_srsbackbonesignalipdu04_passseatsts1_occptlrg()
        # self.ipdu.set(
        #     self.ipdu.backbonefr.SrsBackBoneFr04,
        #     "BltLockStAtDrvrBltLockSts_0_SRSBackBoneSignalIPdu04",
        #     0,
        # )
        # self.ipdu.set(
        #     self.ipdu.backbonefr.SrsBackBoneFr04,
        #     "BltLockStAtDrvrBltLockSt1_0_SRSBackBoneSignalIPdu04",
        #     0,
        # )
        # self.ipdu.set(
        #     self.ipdu.backbonefr.SrsBackBoneFr04,
        #     "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04",
        #     0,
        # )
        # self.ipdu.set(
        #     self.ipdu.backbonefr.SrsBackBoneFr04,
        #     "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04",
        #     0,
        # )
    #     sleep(1)
    #     self.partner.send_request_and_ck_resp(
    #         SEAT_SERVICE_CLIENT,
    #         "GetBeltWarning",
    #         {"seats": [7]},
    #         {"out": [{"id": 4, "status": 2}]},
    #     )
    #     sleep(3)
    
    @allure.title("GID-584086_后排安全带报警状态监测_安全带告警Status==5&&UsgMod=convenience故障后恢复告警状态监测Status==1")
    @pytest.mark.sanity
    def test_caseid_1959949(self):
        """
        1、先设置安全带无告警status==1
        2、再设置后排安全带故障Status==5
        3、最后再设置安全带无故障&&模式小于convenience，监测状态机告警状态status值为1
        """
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0x2)
        sleep(1)
        # 后排左
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSts_0_SRSBackBoneSignalIPdu04",
            1,
        )
        # 后排中
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04",
            1,
        )
        # 后排右
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSts_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {
                "out": [
                    {"id": 4, "status": 5},
                    {"id": 5, "status": 5},
                    {"id": 6, "status": 5},
                ]
            },
        )
        sleep(1)
        # 设置安全带故障恢复
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecLeBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecRiBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.sd_tester.change_usage_mode(0x1)
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {
                "out": [
                    {"id": 4, "status": 1},
                    {"id": 5, "status": 1},
                    {"id": 6, "status": 1},
                ]
            },
        )
        sleep(3)
        
    @allure.title("471561_驾驶员在功能安全等级ASIL B信号监测")
    @pytest.mark.sanity
    def test_caseid_1919196(self):
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStSafeAtDrvrBltLockSt1", 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06,"VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06",1.5)
        self.io.drvr_door_close()
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, "DoorDrvrStsWithFacQlyDoorSts", 3),
            (self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsntQf", 2),
        ]
        self.io.drvr_door_open()
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr06, "DoorDrvrStsWithFacQlyDoorSts", 1),
            (self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsntQf", 1),
        ]
        
    @allure.title("492229_驾驶员E2E保护")
    @pytest.mark.full
    def test_caseid_1986706(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsntQf", 0)
        self.ipdu.set_no_crc(self.ipdu.backbonefr.CemBackBoneFr03, 'DrvrPrsntStsDrvrPrsnt')
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdQf", 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 1)
        # self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsntQf", 3)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsnt", 0)
        self.ipdu.set_crc_count(self.ipdu.backbonefr.CemBackBoneFr03, 'DrvrPrsntStsDrvrPrsnt')
        
    @allure.title("492243_车速通讯安全监测")
    @pytest.mark.full
    def test_caseid_1919206(self):
        self.partner.empty_all()
        sleep(0.5)
        self.sd_tester.change_usage_mode(0xD)
        # 设置车速v=5km/h
        self.ipdu.set_vehspd(1.3)
        sleep(1)
        self.io.drvr_door_close()
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "DoorDrvrStsWithFacQlyDoorSts", 2)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStSafeAtDrvrBltLockSt1", 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdQf", 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 1)#yes
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'DrvrPrsntStsDrvrPrsntQf', 3)
        
    @allure.title("456476、471555_功能安全_加速踏板踩下驾驶员质量因子监测Qf==3::ASIL B")
    @pytest.mark.full
    def test_caseid_1960139(self):
        self.sd_tester.change_usage_mode(0xD)
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsntQf", 1
        )
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', 1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdSts', 1)
        self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf')
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsnt", 2),
            (self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsntQf", 3),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)
        
    @allure.title("驾驶员状态优先级")
    @pytest.mark.full
    def test_caseid_1989090(self):
        self.partner.empty_all()
        self.dk.set_drvr_seat_notpresent()
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )  # 安全带无故障
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 0
        )# 安全带未系
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsntQf", 1)

        self.io.drvr_door_close()
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, "DoorDrvrSts", 2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "DoorDrvrStsWithFacQlyDoorSts", 2)
        sleep(1) 
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 1)  # 设置主驾安全带已系
        self.sd_tester.change_usage_mode(0xD)
        self.ipdu.set_vehspd(6.2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsntQf", 3)
        
    @allure.title("门状态安全监测")
    @pytest.mark.full
    def test_caseid_1989091(self):
        self.sd_tester.change_usage_mode(13)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdQf", 3)
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 1
        )
        sleep(0.5)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsnt", 2),
            (self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsntQf", 3),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(1)
        self.io.drvr_door_close()
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "DoorDrvrStsWithFacQlyDoorSts", 2)
        self.io.driver_seat_present()  # 设置主驾占座
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )  # 安全带无故障
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 1
        )  # 设置主驾安全带已系
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'DoorDrvrStsWithFacQlyFacQly', 3)
        sleep(3)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'DoorDrvrStsWithFacQlyDoorSts', 2)
        
    @allure.title("471554_安全带无故障未系_避免意外踩踏板")
    @pytest.mark.full
    def test_caseid_1919198(self):
        self.sd_tester.change_usage_mode(13)
        sleep(1)

        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdQf", 3)
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 1
        )
        sleep(0.5)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsnt", 2),
            (self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsntQf", 3),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(1)
        self.io.drvr_door_open()
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr06, "DoorDrvrStsWithFacQlyDoorSts", 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSts", 0
        )  # 安全带无故障
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStAtDrvrBltLockSt1", 0
        )# 安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr05, "BltLockStSafeAtDrvrBltLockSt1", 0
        )# 安全带未系
        sleep(0.5)
        check_list = [
            (self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsnt", 1),
            (self.ipdu.backbonefr.CemBackBoneFr03, "DrvrPrsntStsDrvrPrsntQf", 1),
        ]
        self.ipdu.check_multiple_signals(check_list)
        self.ipdu.reset_check_results()
        sleep(3)
        
    @allure.title("Convenience_后排安全带报警状态_中后安全带告警status==3后安全带故障_告警状态监测SeatBeltWarning.State=5")
    @pytest.mark.full
    def test_caseid_1919197(self):
        self.sd_tester.change_usage_mode(2)
        # 设置座椅有占座&&安全带无故障&&安全带未系
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "SeatOccptAtRowSecMid_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04",
            0,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSt1_0_SRSBackBoneSignalIPdu04",
            0,
        )
        sleep(0.5)
        # 设置车速v>22km/h
        self.ipdu.set_vehspd(6.3)
        sleep(1)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 5, "status": 3}]},
        )
        # 设置中后排安全带故障
        self.ipdu.set(
            self.ipdu.backbonefr.SrsBackBoneFr04,
            "BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04",
            1,
        )
        sleep(0.5)
        self.partner.send_request_and_ck_resp(
            SEAT_SERVICE_CLIENT,
            "GetBeltWarning",
            {"seats": [7]},
            {"out": [{"id": 5, "status": 5}]},
        )
        sleep(3)