from time import sleep
import pytest
import allure
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check

# from test_case.soa.case_helper.partner_const import VEHICLESETSTATUS_CLIENT

VEHICLESETSTATUS_CLIENT = "VehicleSetStatusService_client"


class CarMode(object):
    NORMAL = 0
    TRANSPORT = 1
    FACTORY = 2
    CRASH = 3
    DYNO = 5


CAR_MODE_MAP = {
    0: "NORMAL",
    1: "TRANSPORT",
    2: "FACTORY",
    3: "CRASH",
    5: "DYNO",
}


@allure.feature("架构基础")
@allure.story("整车模式/洗车模式")
class TestWashMode(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        partner_process_check()
        self.nucapp.bgm_diag_line_up()
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.sd_tester.update_serverdoipid(0x1002)
        time.sleep(0.5)
        self.sd_tester.diagnostic_client_sim_start()
        self.sd_tester.tester_present()
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.s2sbaseclass = S2sBaseClass(
            [("VehicleSetStatusService", "client"), ("VehicleModeService", "client")]
        )

        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()
            self.busapp.start_all_cyclic_msg()

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, "EngSt1WdStsEngSt1WdSts", 0
        )
        # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "VehMtnStVehMtnSt", 3)
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropComFr10, "TrsmParkLockdTrsmParkLockd", 1
        )
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropFr24, "GearLvrIndcn_1_EcmPropSignalIPdu24", 0
        )
        # self.ipdu.set(
        #     self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0
        # )
        # self.ipdu.set(
        #     self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 0
        # )
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06",
            3,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06",
            0.0,
        )
        sleep(1)
        self.s2sbaseclass.send_method_request(
            "VehicleModeService_client",
            "SetCarMode",
            {"mode": 0},
        )
        time.sleep(1)

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)
        self.s2sbaseclass.send_method_request(
            VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": False}
        )
        time.sleep(1)
        # self.s2sbaseclass.send_request_and_ck_resp(
        #     VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False}
        # )

    def after_class(self, ecu):
        # self.s2sbaseclass.send_method_request(
        #     'VehicleModeService_client', "SetUsageModeDown", {"mode": 1}
        # )
        self.s2sbaseclass.send_method_request(
            VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": False}
        )
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False}
        )
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        self.s2sbaseclass.stop_operators()
        self.sd_tester.stop_tester_present()
        self.nucapp.bgm_diag_line_down()
        self.sd_tester.diagnostic_client_sim_close()
        super().after_class(self, ecu)

    # @staticmethod
    def s2s_change_car_mode_and_check_result(self, car_mode, **kwargs):
        """
        通过s2s 切换 car mode
        """
        car_mode_name = CAR_MODE_MAP.get(car_mode)
        logger.info(f"设置car mode 为{car_mode_name}:{car_mode}")
        logger.info(
            f"Step:调用 SetCarMode:(服务:BonnetService;函数名:set:SetCarMode(mode:{car_mode}))"
        )
        self.s2sbaseclass.send_method_request(
            "VehicleModeService_client",
            "SetCarMode",
            {"mode": car_mode},
        )
        logger.info(f"验证切换结果是否为{car_mode_name}:{car_mode}")
        self.check_car_mode_status(expectedmode=car_mode)

    def check_car_mode_status(self, expectedmode, do_assert=True, **kwargs):
        timeout = kwargs.get("timeout", 5)
        msg_signals_obj = kwargs.get("msg_signals_obj", self.ipdu.bodycan.CEMBodyFr12)
        signal_name = kwargs.get(
            "signal_name", "VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12"
        )
        # msg_signals_obj = kwargs.get('msg_signals_obj', self.ipdu.backbonefr.CemBackBoneFr02)
        # signal_name = kwargs.get('signal_name', 'VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02')
        result, realvalue, expectedvalue = self.ipdu.check(
            msg_signals_obj=msg_signals_obj,
            signal_name=signal_name,
            sig_value_name=expectedmode,
            do_assert=do_assert,
            timeout=timeout,
        )
        return result, realvalue, expectedvalue

    def set_lockunlock_change_to_active(self):
        self.ipdu.pause_all_bus_send()
        # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "VehMtnStVehMtnSt", 3)
        # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0
        )
        # self.ipdu.backbonefr_vddmbackbonefr03_gearlvrindcn_gearlvrindcn2_parkindcn()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, "GearLvrIndcn", 0)
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
        self.dk.set_cenlock_sts(0x3)
        sleep(1)
        self.dk.set_cenlock_sts(0x1)
        self.ipdu.pause_all_bus_send()
        self.s2sbaseclass.send_method_request(
            "VehicleModeService_client", "SetUsageModeUp", {"mode": 11}
        )
        time.sleep(1)
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr02,
            "VehModMngtGlbSafe1UsgModSts_0_CEMBackBoneSignalIpdu02",
            "UsgModSts1_UsgModActv",
        )

    # @pytest.mark.smoke
    # @pytest.mark.full
    # def test_speed_enter_washmode_118600(self):
    #     '''
    #     车速满足进入洗车模式
    #     1.FR:36-0-1:VehModMngtGlbSafe1UsgModSts==11 UsgModSts1_UsgModActive
    #     2.FR:57-0-4:VehSpdLgtQf ==3 GenQf1_AccurData
    #     3.FR:57-0-4:VehSpdLgtA == 4m/s
    #     4.PropulsionCAN:0x04B:GearLvrIndcn == 1 GearLvrIndcn2_RvsIndcn
    #     5.PropulsionCAN:0x155:TrsmParkLockdTrsmParkLockd == 1 TrsmParkLock1_ParkEngd
    #     6.调用VehicleSetStatusService::getwashmodests的值为0'''
    #     self.set_lockunlock_change_to_active()
    #     self.ipdu.set(
    #         self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1
    #     )
    #     self.ipdu.set(
    #         self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 1
    #     )
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06',3)
    #     self.ipdu.set(
    #         self.ipdu.backbonefr.BcmVddmBackBoneFr06,
    #         'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06',
    #         4,
    #     )
    #     sleep(1)
    #     self.s2sbaseclass.send_method_request(
    #         VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True}
    #     )
    #     time.sleep(.5)
    #     self.s2sbaseclass.send_request_and_ck_resp(
    #         VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": True}
    #     )

    @pytest.mark.smoke
    @pytest.mark.verify
    @pytest.mark.mcu_test
    def test_speed_enter_washmode_caseid_1943290(self):
        """
        服务进入洗车模式_车速满足1.3
        1.FR:36-0-1:VehModMngtGlbSafe1UsgModSts==11 UsgModSts1_UsgModActive
        2.FR:57-0-4:VehSpdLgtQf ==3 GenQf1_AccurData
        3.FR:57-0-4:VehSpdLgtA == 4m/s
        4.PropulsionCAN:0x04B:GearLvrIndcn == 1 GearLvrIndcn2_RvsIndcn
        5.PropulsionCAN:0x155:TrsmParkLockdTrsmParkLockd == 1 TrsmParkLock1_ParkEngd
        6.调用VehicleSetStatusService::getwashmodests的值为0"""
        # self.set_lockunlock_change_to_active()
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropComFr10, "TrsmParkLockdTrsmParkLockd", 1
        )
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropFr24, "GearLvrIndcn_1_EcmPropSignalIPdu24", 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06",
            3,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06",
            4,
        )
        sleep(1)
        self.s2sbaseclass.send_method_request(
            VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True}
        )
        time.sleep(0.5)
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": True}
        )

    # @pytest.mark.smoke
    # @pytest.mark.full
    # def test_exit_washmode_118596(self):
    #     '''
    #     服务退出洗车模式,关注能不能切到洗车模式再退出
    #     1.FR:36-0-1:VehModMngtGlbSafe1UsgModSts==11 UsgModSts1_UsgModActive
    #     2.FR:57-0-4:VehSpdLgtQf ==3 GenQf1_AccurData
    #     3.FR:57-0-4:VehSpdLgtA == 5m/s
    #     4.PropulsionCAN:0x04B:GearLvrIndcn == 0 GearLvrIndcn2_ParkIndcn
    #     5.PropulsionCAN:0x155:TrsmParkLockdTrsmParkLockd == 1 TrsmParkLock1_ParkEngd
    #     6.调用VehicleSetStatusService::getwashmodests的值为1
    #     '''
    #     self.s2sbaseclass.send_method_request(
    #         VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": False}
    #     )
    #     time.sleep(.5)
    #     self.s2sbaseclass.send_request_and_ck_resp(
    #         VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False}
    #     )

    @pytest.mark.smoke
    @pytest.mark.mcu_test
    def test_exit_washmode_caseid_1943286(self):
        """
        服务退出洗车模式,关注能不能切到洗车模式再退出
        1.FR:36-0-1:VehModMngtGlbSafe1UsgModSts==11 UsgModSts1_UsgModActive
        2.FR:57-0-4:VehSpdLgtQf ==3 GenQf1_AccurData
        3.FR:57-0-4:VehSpdLgtA == 5m/s
        4.PropulsionCAN:0x04B:GearLvrIndcn == 0 GearLvrIndcn2_ParkIndcn
        5.PropulsionCAN:0x155:TrsmParkLockdTrsmParkLockd == 1 TrsmParkLock1_ParkEngd
        6.调用VehicleSetStatusService::getwashmodests的值为1
        """
        # self.set_lockunlock_change_to_active()
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropComFr10, "TrsmParkLockdTrsmParkLockd", 1
        )
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropFr24, "GearLvrIndcn_1_EcmPropSignalIPdu24", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06",
            5.0,
        )
        # self.ipdu.check(self.ipdu.bodycan.CemBodyFr03, 'VehSpdLgtA_4_CemBodySignalIPdu03', 5.0)
        self.s2sbaseclass.send_method_request(
            VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True}
        )
        time.sleep(0.5)
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": True}
        )
        self.s2sbaseclass.send_method_request(
            VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": False}
        )
        time.sleep(0.5)
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False}
        )

    @pytest.mark.sanity
    def test_exit_washmode_caseid_1943284(self):
        """
        仲裁退出洗车模式_服务请求退出1s内再次服务进入
        1.FR:36-0-1:VehModMngtGlbSafe1UsgModSts==11 UsgModSts1_UsgModActive
        2.FR:57-0-4:VehSpdLgtQf ==3 GenQf1_AccurData
        3.FR:57-0-4:VehSpdLgtA == 5m/s
        4.PropulsionCAN:0x04B:GearLvrIndcn == 0 GearLvrIndcn2_ParkIndcn
        5.PropulsionCAN:0x155:TrsmParkLockdTrsmParkLockd == 1 TrsmParkLock1_ParkEngd
        6.调用VehicleSetStatusService::getwashmodests的值为1
        """
        # self.set_lockunlock_change_to_active()
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropComFr10, "TrsmParkLockdTrsmParkLockd", 1
        )
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropFr24, "GearLvrIndcn_1_EcmPropSignalIPdu24", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06",
            5.0,
        )
        # self.ipdu.check(self.ipdu.bodycan.CemBodyFr03, 'VehSpdLgtA_4_CemBodySignalIPdu03', 5.0)
        self.s2sbaseclass.send_method_request(
            VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True}
        )
        time.sleep(0.5)
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": True}
        )
        self.s2sbaseclass.send_method_request(
            VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": False}
        )
        time.sleep(0.5)
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False}
        )
        self.s2sbaseclass.send_method_request(
            VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True}
        )
        time.sleep(0.5)
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": True}
        )

    @pytest.mark.sanity
    def test_exit_washmode_caseid_1943285(self):
        """
        仲裁退出洗车模式_服务请求退出1s内再次服务进入
        1.FR:36-0-1:VehModMngtGlbSafe1UsgModSts==11 UsgModSts1_UsgModActive
        2.FR:57-0-4:VehSpdLgtQf ==3 GenQf1_AccurData
        3.FR:57-0-4:VehSpdLgtA == 5m/s
        4.PropulsionCAN:0x04B:GearLvrIndcn == 0 GearLvrIndcn2_ParkIndcn
        5.PropulsionCAN:0x155:TrsmParkLockdTrsmParkLockd == 1 TrsmParkLock1_ParkEngd
        6.调用VehicleSetStatusService::getwashmodests的值为1
        """
        # self.set_lockunlock_change_to_active()
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropComFr10, "TrsmParkLockdTrsmParkLockd", 1
        )
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropFr24, "GearLvrIndcn_1_EcmPropSignalIPdu24", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06",
            5.0,
        )
        # self.ipdu.check(self.ipdu.bodycan.CemBodyFr03, 'VehSpdLgtA_4_CemBodySignalIPdu03', 5.0)
        self.s2sbaseclass.send_method_request(
            VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True}
        )
        time.sleep(0.5)
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": True}
        )
        self.s2sbaseclass.send_method_request(
            VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": False}
        )
        time.sleep(0.5)
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False}
        )

    # @pytest.mark.smoke
    # @pytest.mark.full
    # def test_gear_enter_washmode_118601(self):
    #     '''
    #     挡位满足设置洗车模式
    #     1.FR:36-0-1:VehModMngtGlbSafe1UsgModSts==11 UsgModSts1_UsgModActive
    #     2.FR:57-0-4:VehSpdLgtQf ==3 GenQf1_AccurData
    #     3.FR:57-0-4:VehSpdLgtA == 5m/s
    #     4.PropulsionCAN:0x04B:GearLvrIndcn == 0 GearLvrIndcn2_ParkIndcn
    #     5.PropulsionCAN:0x155:TrsmParkLockdTrsmParkLockd == 1 TrsmParkLock1_ParkEngd
    #     6.调用VehicleSetStatusService::getwashmodests的值为0
    #     '''
    #     self.set_lockunlock_change_to_active()
    #     self.ipdu.set(
    #         self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1
    #     )
    #     self.ipdu.set(
    #         self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 0
    #     )
    #     self.ipdu.set(
    #         self.ipdu.backbonefr.BcmVddmBackBoneFr06,
    #         'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06',
    #         5.0,
    #     )
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr03, 'VehSpdLgtA_4_CemBodySignalIPdu03', 5.0)
    #     self.s2sbaseclass.send_method_request(
    #         VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True}
    #     )
    #     time.sleep(.5)
    #     self.s2sbaseclass.send_request_and_ck_resp(
    #         VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": True}
    #     )

    @pytest.mark.smoke
    def test_gear_enter_washmode_caseid_1943291(self):
        """
        挡位满足设置洗车模式
        1.FR:36-0-1:VehModMngtGlbSafe1UsgModSts==11 UsgModSts1_UsgModActive
        2.FR:57-0-4:VehSpdLgtQf ==3 GenQf1_AccurData
        3.FR:57-0-4:VehSpdLgtA == 5m/s
        4.PropulsionCAN:0x04B:GearLvrIndcn == 0 GearLvrIndcn2_ParkIndcn
        5.PropulsionCAN:0x155:TrsmParkLockdTrsmParkLockd == 1 TrsmParkLock1_ParkEngd
        6.调用VehicleSetStatusService::getwashmodests的值为0
        """
        # self.set_lockunlock_change_to_active()
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropComFr10, "TrsmParkLockdTrsmParkLockd", 1
        )
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropFr24, "GearLvrIndcn_1_EcmPropSignalIPdu24", 0
        )
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06",
            5.0,
        )
        # self.ipdu.check(self.ipdu.bodycan.CemBodyFr03, 'VehSpdLgtA_4_CemBodySignalIPdu03', 5.0)
        self.s2sbaseclass.send_method_request(
            VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True}
        )
        time.sleep(0.5)
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": True}
        )

    # @pytest.mark.sanity
    # def test_wash_caseid_118592(self):
    #     '''
    #     条件不满足无法进入洗车模式_Usagemode后满足条件仍无法进入
    #     1.FR:36-0-1:VehModMngtGlbSafe1UsgModSts==11 UsgModSts1_UsgModActive
    #     2.FR:57-0-4:VehSpdLgtQf ==3 GenQf1_AccurData
    #     3.FR:57-0-4:VehSpdLgtA == 5m/s
    #     4.PropulsionCAN:0x04B:GearLvrIndcn == 1 GearLvrIndcn2_RvsIndcn
    #     5.PropulsionCAN:0x155:TrsmParkLockdTrsmParkLockd == 1 TrsmParkLock1_ParkEngd
    #     6.调用VehicleSetStatusService::getwashmodests的值为0
    #     '''

    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06',3)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06', 5.0)
    #     self.ipdu.set(
    #         self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1
    #     )
    #     self.ipdu.set(
    #         self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 1
    #     )
    #     self.s2sbaseclass.send_method_request(
    #         VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True}
    #     )
    #     time.sleep(1)
    #     self.s2sbaseclass.send_request_and_ck_resp(
    #         VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False}
    #     )
    #     self.set_lockunlock_change_to_active()
    #     self.s2sbaseclass.ck_s2s_event(VEHICLESETSTATUS_CLIENT, "NotifyWashModeSts", {"sts": False})
    #     self.s2sbaseclass.send_request_and_ck_resp(
    #         VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False}
    #     )

    # @pytest.mark.sanity
    # def test_wash_caseid_118593(self):
    #     '''
    #     条件不满足无法进入洗车模式_Usagemode不满足无法进入
    #     1.FR:36-0-1:VehModMngtGlbSafe1UsgModSts==1 UsgModSts1_UsgModInactive
    #     2.FR:57-0-4:VehSpdLgtQf ==3 GenQf1_AccurData
    #     3.FR:57-0-4:VehSpdLgtA == 5m/s
    #     4.PropulsionCAN:0x04B:GearLvrIndcn == 0 GearLvrIndcn2_ParkIndcn
    #     5.PropulsionCAN:0x155:TrsmParkLockdTrsmParkLockd == 1 TrsmParkLock1_ParkEngd
    #     6.调用VehicleSetStatusService::getwashmodests的值为0
    #     '''
    #     self.s2sbaseclass.send_method_request(
    #         'VehicleModeService_client', "SetUsageModeDown", {"mode": 1}
    #     )
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06',3)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06', 5.0)
    #     self.ipdu.set(
    #         self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1
    #     )
    #     self.ipdu.set(
    #         self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 0
    #     )
    #     self.s2sbaseclass.send_method_request(
    #         VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True}
    #     )
    #     self.s2sbaseclass.ck_s2s_event(VEHICLESETSTATUS_CLIENT, "NotifyWashModeSts", {"sts": False})
    #     self.s2sbaseclass.send_request_and_ck_resp(
    #         VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False}
    #     )

    # @pytest.mark.sanity
    # def test_wash_caseid_118594(self):
    #     '''
    #     条件不满足无法进入洗车模式_挡位和车速不满足
    #     1.FR:36-0-1:VehModMngtGlbSafe1UsgModSts==11 UsgModSts1_UsgModActive
    #     2.FR:57-0-4:VehSpdLgtQf ==3 GenQf1_AccurData
    #     3.FR:57-0-4:VehSpdLgtA == 5m/s
    #     4.PropulsionCAN:0x04B:GearLvrIndcn == 1 GearLvrIndcn2_RvsIndcn
    #     5.PropulsionCAN:0x155:TrsmParkLockdTrsmParkLockd == 1 TrsmParkLock1_ParkEngd
    #     6.调用VehicleSetStatusService::getwashmodests的值为0
    #     '''
    #     self.set_lockunlock_change_to_active()
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06',3)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06', 5.0)
    #     self.ipdu.set(
    #         self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1
    #     )
    #     self.ipdu.set(
    #         self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 1
    #     )
    #     self.s2sbaseclass.send_method_request(
    #         VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True}
    #     )
    #     self.s2sbaseclass.ck_s2s_event(VEHICLESETSTATUS_CLIENT, "NotifyWashModeSts", {"sts": False})
    #     self.s2sbaseclass.send_request_and_ck_resp(
    #         VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False}
    #     )

    # @pytest.mark.sanity
    # def test_wash_caseid_118598(self):
    #     '''
    #     仲裁退出洗车模式_Usagemode不满足_inactive直接退出
    #     1.FR:36-0-1:VehModMngtGlbSafe1UsgModSts==11 UsgModSts1_UsgModActive
    #     2.FR:57-0-4:VehSpdLgtQf ==3 GenQf1_AccurData
    #     3.FR:57-0-4:VehSpdLgtA == 0m/s
    #     4.PropulsionCAN:0x04B:GearLvrIndcn == 0 GearLvrIndcn2_ParkIndcn
    #     5.PropulsionCAN:0x155:TrsmParkLockdTrsmParkLockd == 1 TrsmParkLock1_ParkEngd
    #     6.调用VehicleSetStatusService::getwashmodests的值为1
    #     '''
    #     self.set_lockunlock_change_to_active()
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06',3)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06', 0)
    #     self.ipdu.set(
    #         self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1
    #     )
    #     self.ipdu.set(
    #         self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 0
    #     )
    #     self.s2sbaseclass.send_method_request(
    #         VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True}
    #     )
    #     time.sleep(.5)
    #     self.s2sbaseclass.send_request_and_ck_resp(
    #         VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": True}
    #     )
    #     self.s2sbaseclass.send_method_request(
    #         'VehicleModeService_client', "SetUsageModeDown", {"mode": 1}
    #     )
    #     self.s2sbaseclass.ck_s2s_event(VEHICLESETSTATUS_CLIENT, "NotifyWashModeSts", {"sts": False})
    #     self.s2sbaseclass.send_request_and_ck_resp(
    #         VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False}
    #     )

    @pytest.mark.full
    @pytest.mark.new
    def test_wash_caseid_1943288(self):
        """
        仲裁退出洗车模式_Usagemode不满足_inactive不直接退出
        1.FR:36-0-1:VehModMngtGlbSafe1UsgModSts==11 UsgModSts1_UsgModActive
        2.FR:57-0-4:VehSpdLgtQf ==3 GenQf1_AccurData
        3.FR:57-0-4:VehSpdLgtA == 0m/s
        4.PropulsionCAN:0x04B:GearLvrIndcn == 0 GearLvrIndcn2_ParkIndcn
        5.PropulsionCAN:0x155:TrsmParkLockdTrsmParkLockd == 1 TrsmParkLock1_ParkEngd
        6.调用VehicleSetStatusService::getwashmodests的值为1
        """
        self.sd_tester.change_usage_mode(11)
        # self.set_lockunlock_change_to_active()
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
            self.ipdu.propulsioncan.EcmPropComFr10, "TrsmParkLockdTrsmParkLockd", 1
        )
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropFr24, "GearLvrIndcn_1_EcmPropSignalIPdu24", 0
        )
        self.s2sbaseclass.send_method_request(
            VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True}
        )
        time.sleep(0.5)
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": True}
        )
        self.sd_tester.change_usage_mode(1)
        # self.s2sbaseclass.send_method_request(
        #     'VehicleModeService_client', "SetUsageModeDown", {"mode": 1}
        # )
        # self.s2sbaseclass.ck_s2s_event(VEHICLESETSTATUS_CLIENT, "NotifyWashModeSts", {"sts": False})
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": True}
        )

    @pytest.mark.full
    @pytest.mark.new
    def test_wash_caseid_1943287(self):
        """
        仲裁退出洗车模式_Usagemode不满足_abandon退出
        1.FR:36-0-1:VehModMngtGlbSafe1UsgModSts==11 UsgModSts1_UsgModActive
        2.FR:57-0-4:VehSpdLgtQf ==3 GenQf1_AccurData
        3.FR:57-0-4:VehSpdLgtA == 0m/s
        4.PropulsionCAN:0x04B:GearLvrIndcn == 0 GearLvrIndcn2_ParkIndcn
        5.PropulsionCAN:0x155:TrsmParkLockdTrsmParkLockd == 1 TrsmParkLock1_ParkEngd
        6.调用VehicleSetStatusService::getwashmodests的值为1
        """
        self.sd_tester.change_usage_mode(11)
        # self.set_lockunlock_change_to_active()
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
            self.ipdu.propulsioncan.EcmPropComFr10, "TrsmParkLockdTrsmParkLockd", 1
        )
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropFr24, "GearLvrIndcn_1_EcmPropSignalIPdu24", 0
        )
        self.s2sbaseclass.send_method_request(
            VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True}
        )
        time.sleep(0.5)
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": True}
        )
        self.sd_tester.change_usage_mode(0)
        # self.s2sbaseclass.send_method_request(
        #     'VehicleModeService_client', "SetUsageModeDown", {"mode": 1}
        # )
        self.s2sbaseclass.ck_s2s_event(
            VEHICLESETSTATUS_CLIENT, "NotifyWashModeSts", {"sts": False}
        )
        time.sleep(1)
        self.sd_tester.get_usge_mode()
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False}
        )

    # @pytest.mark.sanity
    # def test_wash_caseid_118599(self):
    #     '''
    #     仲裁退出洗车模式_挡位与车速都不满足
    #     1.FR:36-0-1:VehModMngtGlbSafe1UsgModSts==11 UsgModSts1_UsgModActive
    #     2.FR:57-0-4:VehSpdLgtQf ==3 GenQf1_AccurData
    #     3.FR:57-0-4:VehSpdLgtA == 5m/s
    #     4.PropulsionCAN:0x04B:GearLvrIndcn == 0 GearLvrIndcn2_ParkIndcn
    #     5.PropulsionCAN:0x155:TrsmParkLockdTrsmParkLockd == 1 TrsmParkLock1_ParkEngd
    #     6.调用VehicleSetStatusService::getwashmodests的值为1
    #     '''
    #     self.set_lockunlock_change_to_active()
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06',3)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06', 4)
    #     self.ipdu.set(
    #         self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1
    #     )
    #     self.ipdu.set(
    #         self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 0
    #     )
    #     self.s2sbaseclass.send_method_request(
    #         VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True}
    #     )
    #     time.sleep(.5)
    #     self.s2sbaseclass.send_request_and_ck_resp(
    #         VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {},{"out": True}
    #     )
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06', 5.0)
    #     time.sleep(.5)
    #     # self.ipdu.check(self.ipdu.bodycan.CemBodyFr03, 'VehSpdLgtA_4_CemBodySignalIPdu03', 5)
    #     self.ipdu.set(
    #         self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 1
    #     )
    #     # self.ipdu.check(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 1)
    #     time.sleep(.5)
    #     self.s2sbaseclass.ck_s2s_event(VEHICLESETSTATUS_CLIENT, "NotifyWashModeSts", {"sts": False})
    #     self.s2sbaseclass.send_request_and_ck_resp(
    #         VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {},{"out": False}
    #     )
    #     # self.s2sbaseclass.send_request_and_ck_resp(
    #     #     VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {},{"out": False}
    #     # )

    @pytest.mark.sanity
    @pytest.mark.wt
    @pytest.mark.new
    def test_wash_caseid_1943289(self):
        """
        仲裁退出洗车模式_挡位与车速都不满足
        1.FR:36-0-1:VehModMngtGlbSafe1UsgModSts==11 UsgModSts1_UsgModActive
        2.FR:57-0-4:VehSpdLgtQf ==3 GenQf1_AccurData
        3.FR:57-0-4:VehSpdLgtA == 5m/s
        4.PropulsionCAN:0x04B:GearLvrIndcn == 0 GearLvrIndcn2_ParkIndcn
        5.PropulsionCAN:0x155:TrsmParkLockdTrsmParkLockd == 1 TrsmParkLock1_ParkEngd
        6.调用VehicleSetStatusService::getwashmodests的值为1
        """
        self.sd_tester.change_usage_mode(11)
        # self.set_lockunlock_change_to_active()
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06",
            3,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06",
            4,
        )
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropComFr10, "TrsmParkLockdTrsmParkLockd", 1
        )
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropFr24, "GearLvrIndcn_1_EcmPropSignalIPdu24", 0
        )
        self.s2sbaseclass.send_method_request(
            VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True}
        )
        time.sleep(0.5)
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": True}
        )
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06",
            5.0,
        )
        time.sleep(0.5)
        # self.ipdu.check(self.ipdu.bodycan.CemBodyFr03, 'VehSpdLgtA_4_CemBodySignalIPdu03', 5)
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropFr24, "GearLvrIndcn_1_EcmPropSignalIPdu24", 1
        )
        # self.ipdu.check(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 1)
        time.sleep(0.5)
        self.s2sbaseclass.ck_s2s_event(
            VEHICLESETSTATUS_CLIENT, "NotifyWashModeSts", {"sts": False}
        )
        # time.sleep(10)
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False}
        )
        # self.s2sbaseclass.send_request_and_ck_resp(
        #     VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {},{"out": False}
        # )

    @pytest.mark.full
    @pytest.mark.new
    def test_washmode_caseid_1943281(self):
        """
        仲裁退出洗车模式_进入factory
        1.FR:36-0-1:VehModMngtGlbSafe1UsgModSts==11 UsgModSts1_UsgModActive
        2.FR:57-0-4:VehSpdLgtQf ==3 GenQf1_AccurData
        3.FR:57-0-4:VehSpdLgtA == 4m/s
        4.PropulsionCAN:0x04B:GearLvrIndcn == 1 GearLvrIndcn2_RvsIndcn
        5.PropulsionCAN:0x155:TrsmParkLockdTrsmParkLockd == 1 TrsmParkLock1_ParkEngd
        6.调用VehicleSetStatusService::getwashmodests的值为0"""
        self.sd_tester.change_usage_mode(11)
        # self.set_lockunlock_change_to_active()
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropComFr10, "TrsmParkLockdTrsmParkLockd", 1
        )
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropFr24, "GearLvrIndcn_1_EcmPropSignalIPdu24", 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06",
            3,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06",
            4,
        )
        sleep(1)
        self.s2sbaseclass.send_method_request(
            VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True}
        )
        time.sleep(0.5)
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": True}
        )
        time.sleep(2)
        self.dk.set_central_lock(0x1)
        self.s2s_change_car_mode_and_check_result(CarMode.FACTORY)
        time.sleep(0.5)
        self.s2sbaseclass.ck_s2s_event(
            VEHICLESETSTATUS_CLIENT, "NotifyWashModeSts", {"sts": False}
        )
        time.sleep(0.5)
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False}
        )

    @pytest.mark.full
    @pytest.mark.new
    def test_washmode_caseid_1943280(self):
        """
        仲裁退出洗车模式_进入tramsport
        1.FR:36-0-1:VehModMngtGlbSafe1UsgModSts==11 UsgModSts1_UsgModActive
        2.FR:57-0-4:VehSpdLgtQf ==3 GenQf1_AccurData
        3.FR:57-0-4:VehSpdLgtA == 4m/s
        4.PropulsionCAN:0x04B:GearLvrIndcn == 1 GearLvrIndcn2_RvsIndcn
        5.PropulsionCAN:0x155:TrsmParkLockdTrsmParkLockd == 1 TrsmParkLock1_ParkEngd
        6.调用VehicleSetStatusService::getwashmodests的值为0"""
        # self.set_lockunlock_change_to_active()
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropComFr10, "TrsmParkLockdTrsmParkLockd", 1
        )
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropFr24, "GearLvrIndcn_1_EcmPropSignalIPdu24", 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06",
            3,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06",
            4,
        )
        sleep(1)
        self.s2sbaseclass.send_method_request(
            VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True}
        )
        time.sleep(0.5)
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": True}
        )
        time.sleep(0.5)
        self.s2sbaseclass.send_method_request(
            "VehicleModeService_client",
            "SetCarMode",
            {"mode": 1},
        )
        time.sleep(0.5)
        self.s2sbaseclass.ck_s2s_event(
            VEHICLESETSTATUS_CLIENT, "NotifyWashModeSts", {"sts": False}
        )
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False}
        )

    @pytest.mark.full
    @pytest.mark.new
    def test_washmode_caseid_1943282(self):
        """
        仲裁退出洗车模式_进入dyno
        1.FR:36-0-1:VehModMngtGlbSafe1UsgModSts==11 UsgModSts1_UsgModActive
        2.FR:57-0-4:VehSpdLgtQf ==3 GenQf1_AccurData
        3.FR:57-0-4:VehSpdLgtA == 4m/s
        4.PropulsionCAN:0x04B:GearLvrIndcn == 1 GearLvrIndcn2_RvsIndcn
        5.PropulsionCAN:0x155:TrsmParkLockdTrsmParkLockd == 1 TrsmParkLock1_ParkEngd
        6.调用VehicleSetStatusService::getwashmodests的值为0"""
        self.sd_tester.change_usage_mode(11)
        # self.set_lockunlock_change_to_active()
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropComFr10, "TrsmParkLockdTrsmParkLockd", 1
        )
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropFr24, "GearLvrIndcn_1_EcmPropSignalIPdu24", 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06",
            3,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06",
            4,
        )
        sleep(1)
        self.s2sbaseclass.send_method_request(
            VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True}
        )
        time.sleep(0.5)
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": True}
        )
        time.sleep(0.5)
        self.s2sbaseclass.send_method_request(
            "VehicleModeService_client",
            "SetCarMode",
            {"mode": 5},
        )
        time.sleep(0.5)
        self.s2sbaseclass.ck_s2s_event(
            VEHICLESETSTATUS_CLIENT, "NotifyWashModeSts", {"sts": False}
        )
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False}
        )

    @pytest.mark.full
    @pytest.mark.new
    def test_washmode_caseid_1943283(self):
        """
        仲裁退出洗车模式_进入crash
        1.FR:36-0-1:VehModMngtGlbSafe1UsgModSts==11 UsgModSts1_UsgModActive
        2.FR:57-0-4:VehSpdLgtQf ==3 GenQf1_AccurData
        3.FR:57-0-4:VehSpdLgtA == 4m/s
        4.PropulsionCAN:0x04B:GearLvrIndcn == 1 GearLvrIndcn2_RvsIndcn
        5.PropulsionCAN:0x155:TrsmParkLockdTrsmParkLockd == 1 TrsmParkLock1_ParkEngd
        6.调用VehicleSetStatusService::getwashmodests的值为0"""
        self.sd_tester.change_usage_mode(11)
        # self.set_lockunlock_change_to_active()
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropComFr10, "TrsmParkLockdTrsmParkLockd", 1
        )
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropFr24, "GearLvrIndcn_1_EcmPropSignalIPdu24", 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06",
            3,
        )
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            "VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06",
            4,
        )
        sleep(1)
        self.s2sbaseclass.send_method_request(
            VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True}
        )
        time.sleep(0.5)
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": True}
        )
        time.sleep(0.5)
        self.s2sbaseclass.send_method_request(
            "VehicleModeService_client",
            "SetCarMode",
            {"mode": 5},
        )
        self.sd_tester.change_car_mode(5)
        time.sleep(0.5)
        self.s2sbaseclass.ck_s2s_event(
            VEHICLESETSTATUS_CLIENT, "NotifyWashModeSts", {"sts": False}
        )
        self.s2sbaseclass.send_request_and_ck_resp(
            VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": False}
        )
        self.sd_tester.change_car_mode(0)
