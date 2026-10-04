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
from xat_ecu.legacy.soa_partner.src.base_partner import S2sBaseClass
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check

# from ecu_simulator.sdk.digital_key.digital_key_const import *

# from ecu_simulator.sdk.digital_key.digital_key_const import *
from xat_ecu.legacy.common.data_type_handing import logger
from xat_cases.legacy.bgm.case_helper.test_base import TestBase

# from ecu_simulator.sdk.digital_key.digital_key_class import DigitalKey
from xat_ecu.legacy.soa_partner.src.base_partner import S2sBaseClass
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check

# from test_case.soa.case_helper.partner_const import *
from xat_cases.legacy.bgm.VehicleControl.case_helper.common_lib_bgm import *


@allure.feature("网络管理")
@allure.story("网络PNC路由测试")
class TestExample(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.sd_tester.diagnostic_client_sim_start()
        self.partner = S2sBaseClass(
            [
                ("VehicleModeService", "client"),
                ("OuterRearViewService", "client"),
                ("VehicleSetStatusService", "client"),
                ("CentralLockService", "client")
            ]
        )
        self.sd_tester.tester_present()
        sleep(0.5)
        self.sd_tester.update_serverdoipid(0x1002)

        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.ipdu.reset_check_results()
        self.sd_tester.change_car_mode(0, do_assert=1)
        # Code Location

    def after_each_func(self, ecu):
        # Code Location
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        # Code Location
        try:
            self.sd_tester.change_usage_mode(1)
            self.sd_tester.change_car_mode(0)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        self.sd_tester.stop_tester_present()
        sleep(0.5)
        self.sd_tester.diagnostic_client_sim_close()
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        super().after_class(self, ecu)

    def start_thread_check_signal(self, msg_obj, signal, observe_time):
        self.ipdu.check_signal(msg_obj, signal, observe_time)

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
        
    def check_multiple_signal_event_thread(
        self, msg, singal, base_value, targe_value, change_times, duration
    ):
        result = self.ipdu.check_event(
            msg, singal, base_value, targe_value, timeout=duration
        )
        logger.info(
            "\033[0;35;40mResult:{}:{} change from {} to {} happened {} times\033[0m".format(
                msg, singal, base_value, targe_value, result
            )
        )
        if result >= change_times:
            assert True
            logger.info("\033[0;35;40m{}获取值大于{}\033[0m".format(singal, change_times))
        else:
            assert False
        self.ipdu.reset_check_results()

    # @allure.title("屏幕按钮点击外后视镜折叠")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    # )
    # @pytest.mark.smoke
    # @pytest.mark.verify
    # @allure.title("屏幕按钮点击外后视镜折叠")
    # def test_caseid_1960051(self):
    #     with allure.step("设置初始化条件"):
    #         self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, "MirrFoldStsAtDrvr", 1)  # 展开
    #         self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, "MirrFoldStsAtPass", 1)
    #         #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
    #         self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
    #         sleep(2)
    #         # 设置:Carmode 设置为Normal;
    #         self.sd_tester.change_car_mode(0, do_assert=1)
    #         sleep(0.5)
    #         # 设置:Usage 设置为02 Convenience;
    #         self.sd_tester.change_usage_mode(2, do_assert=1)
    #         sleep(0.5)
    #         self.ipdu.reset_check_results()
    #     with allure.step(f"Step:设置车速为0"):
    #         self.ipdu.set_vehspd(0)
    #         sleep(1)
    #     with allure.step("仿真洗车模式未打开"):
    #         self.partner.send_method_request(
    #             "VehicleSetStatusService_client", "SetWashMode", {"isOn": False}
    #         )
    #         sleep(1)

    #     self.ipdu.check_thread_start(
    #         self.ipdu.bodycan.CEMBodyFr13, "ExtrMirrFoldHmiReq", 1, timeout=2
    #     )
    #     with allure.step("设置后视镜折叠"):
    #         self.partner.send_method_request(
    #             "OuterRearViewService_client",
    #             "Fold",
    #             {"views": [2], "isAutoUnFold": False},
    #         )  # 0 左后视镜 1 右后视镜  2 所有后视镜

    #     with allure.step(f"监测总线:Bodycan：ExtrMirrFoldHmiReq"):
    #         result = self.ipdu.check_thread_stop("ExtrMirrFoldHmiReq", timeout=5)
    #         logger.info("result {}".format(result))
    #         if result == None:
    #             assert False
    #         else:
    #             assert result[0]
    #         self.ipdu.reset_check_results()
    #     sleep(1)

    # @allure.title("后视镜在展开的情况下下翻")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    # )
    # @pytest.mark.smoke
    # @allure.title("后视镜在展开的情况下下翻")
    # def test_caseid_1960096(self):
    #     with allure.step("设置初始化条件"):
    #         self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, "MirrFoldStsAtDrvr", 1)
    #         self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, "MirrFoldStsAtPass", 1)
    #         #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
    #         self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
    #         sleep(2)
    #         # 设置:Carmode 设置为Normal;
    #         self.sd_tester.change_car_mode(0, do_assert=1)
    #         sleep(0.5)
    #         # 设置:Usage 设置为02 Convenience;
    #         self.sd_tester.change_usage_mode(2, do_assert=1)
    #         sleep(0.5)
    #         self.ipdu.reset_check_results()
    #     with allure.step(f"Step:设置车速为0"):
    #         self.ipdu.set_vehspd(0)
    #         sleep(1)
    #     with allure.step("仿真洗车模式未打开"):
    #         self.partner.send_method_request(
    #             "VehicleSetStatusService_client", "SetWashMode", {"isOn": False}
    #         )
    #         sleep(1)
    #     with allure.step("设置前置条件：后视镜未下翻"):
    #         self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, "PassExtrMirrAdjHmiReq", 0)
    #         self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, "DrvrExtrMirrAdjHmiReq", 0)
    #         sleep(2)
    #     with allure.step("调用接口StartAdjustViewMirror调节后视镜向下:"):
    #         self.partner.send_method_request(
    #             "OuterRearViewService_client",
    #             "StartAdjustViewMirror",
    #             {"params": [{"id": 2, "direction": 5}]},
    #         )
    #         sleep(1)
    #     with allure.step("检测后视镜是否下翻"):
    #         self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, "DrvrExtrMirrAdjHmiReq", 2)
    #         self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, "PassExtrMirrAdjHmiReq", 2)

    # @allure.title("后视镜在折叠的情况下下翻")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    # )
    # @pytest.mark.full
    # def test_caseid_1960095(self):
    #     with allure.step("设置初始化条件"):
    #         self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, "MirrFoldStsAtDrvr", 2)
    #         self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, "MirrFoldStsAtPass", 2)
    #         sleep(2)
    #         #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
    #         self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
    #         sleep(2)
    #         # 设置:Carmode 设置为Normal;
    #         self.sd_tester.change_car_mode(0, do_assert=1)
    #         sleep(0.5)
    #         # 设置:Usage 设置为02 Convenience;
    #         self.sd_tester.change_usage_mode(2, do_assert=1)
    #         sleep(0.5)
    #         self.ipdu.reset_check_results()
    #     with allure.step(f"Step:设置车速为0"):
    #         self.ipdu.set_vehspd(0)
    #         sleep(1)
    #     with allure.step("仿真洗车模式未打开"):
    #         self.partner.send_method_request(
    #             "VehicleSetStatusService_client", "SetWashMode", {"isOn": False}
    #         )
    #         sleep(1)
    #     with allure.step("设置前置条件：后视镜未下翻"):
    #         self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, "PassExtrMirrAdjHmiReq", 0)
    #         self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, "DrvrExtrMirrAdjHmiReq", 0)
    #         sleep(2)
    #     with allure.step("调用接口StartAdjustViewMirror调节后视镜向下:"):
    #         self.partner.send_method_request(
    #             "OuterRearViewService_client",
    #             "StartAdjustViewMirror",
    #             {"params": [{"id": 2, "direction": 5}]},
    #         )
    #         sleep(1)
    #     with allure.step("检测后视镜是否下翻"):
    #         self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, "DrvrExtrMirrAdjHmiReq", 2)
    #         self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, "PassExtrMirrAdjHmiReq", 2)

    # @allure.title("左后视镜向上调节")
    # @allure.testcase(
    #     'https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46'
    #     )
    # @pytest.mark.smoke
    # @pytest.mark.sanity
    # @pytest.mark.full
    # @allure.title("左后视镜向上调节")
    # def test_caseid_1960094(self):
    #     with allure.step("设置初始化条件"):
    #         self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, "DrvrExtrMirrAdjHmiReq", 0)
    #         # 设置:Carmode 设置为Normal;
    #         self.sd_tester.change_car_mode(0, do_assert=1)
    #         sleep(0.5)
    #         # 设置:Usage 设置为02 Convenience;
    #         self.sd_tester.change_usage_mode(2, do_assert=1)
    #         sleep(0.5)
    #         self.ipdu.reset_check_results()
    #     with allure.step(f"Step:设置车速为0"):
    #         self.ipdu.set_vehspd(0)
    #         sleep(1)
    #     with allure.step("仿真洗车模式未打开"):
    #         self.partner.send_method_request("VehicleSetStatusService_client", "SetWashMode", {"isOn": False})
    #         sleep(1)

    #     self.ipdu.check_thread_start(
    #         self.ipdu.bodycan.CEMBodyFr13, 'DrvrExtrMirrAdjHmiReq', 1, timeout=2
    #     )

    #     with allure.step("调用接口StartAdjustViewMirror调节左后视镜向上:"):
    #         self.partner.send_method_request("OuterRearViewService_client", "StartAdjustViewMirror", {"params": [{"id":2,"direction":2}]})
    #         sleep(1)

    #     with allure.step(f"监测总线:Bodycan：DrvrExtrMirrAdjHmiReq"):
    #         result = self.ipdu.check_thread_stop('DrvrExtrMirrAdjHmiReq', timeout=5)
    #         logger.info("result {}".format(result))
    #         if result == None:
    #             assert False
    #         else:
    #             assert result[0]
    #         self.ipdu.reset_check_results()
    #     sleep(1)

    # @allure.title("左后视镜向左调节")
    # @allure.testcase(
    #     'https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46'
    #     )
    # @pytest.mark.smoke
    # @pytest.mark.sanity
    # @pytest.mark.full
    # @allure.title("左后视镜向左调节")
    # def test_caseid_1960093(self):
    #     with allure.step("设置初始化条件"):
    #         self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, "DrvrExtrMirrAdjHmiReq", 0)
    #         # 设置:Carmode 设置为Normal;
    #         self.sd_tester.change_car_mode(0, do_assert=1)
    #         sleep(0.5)
    #         # 设置:Usage 设置为02 Convenience;
    #         self.sd_tester.change_usage_mode(2, do_assert=1)
    #         sleep(0.5)
    #         self.ipdu.reset_check_results()
    #     with allure.step(f"Step:设置车速为0"):
    #         self.ipdu.set_vehspd(0)
    #         sleep(1)
    #     with allure.step("仿真洗车模式未打开"):
    #         self.partner.send_method_request("VehicleSetStatusService_client", "SetWashMode", {"isOn": False})
    #         sleep(1)

    #     self.ipdu.check_thread_start(
    #         self.ipdu.bodycan.CEMBodyFr13, 'DrvrExtrMirrAdjHmiReq', 3, timeout=2
    #     )

    #     with allure.step("调用接口StartAdjustViewMirror调节左后视镜向左:"):
    #         self.partner.send_method_request("OuterRearViewService_client", "StartAdjustViewMirror", {"params": [{"id":2,"direction":1}]})
    #         sleep(1)

    #     with allure.step(f"监测总线:Bodycan：DrvrExtrMirrAdjHmiReq"):
    #         result = self.ipdu.check_thread_stop('DrvrExtrMirrAdjHmiReq', timeout=5)
    #         logger.info("result {}".format(result))
    #         if result == None:
    #             assert False
    #         else:
    #             assert result[0]
    #         self.ipdu.reset_check_results()
    #     sleep(1)

    # @allure.title("左后视镜向下调节")
    # @allure.testcase(
    #     'https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46'
    #     )
    # @pytest.mark.smoke
    # @pytest.mark.sanity
    # @pytest.mark.full
    # @allure.title("左后视镜向下调节")
    # def test_caseid_1960092(self):
    #     with allure.step("设置初始化条件"):
    #         self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, "DrvrExtrMirrAdjHmiReq", 0)
    #         # 设置:Carmode 设置为Normal;
    #         self.sd_tester.change_car_mode(0, do_assert=1)
    #         sleep(0.5)
    #         # 设置:Usage 设置为02 Convenience;
    #         self.sd_tester.change_usage_mode(2, do_assert=1)
    #         sleep(0.5)
    #         self.ipdu.reset_check_results()
    #     with allure.step(f"Step:设置车速为0"):
    #         self.ipdu.set_vehspd(0)
    #         sleep(1)
    #     with allure.step("仿真洗车模式未打开"):
    #         self.partner.send_method_request("VehicleSetStatusService_client", "SetWashMode", {"isOn": False})
    #         sleep(1)

    #     self.ipdu.check_thread_start(
    #         self.ipdu.bodycan.CEMBodyFr13, 'DrvrExtrMirrAdjHmiReq', 2, timeout=2
    #     )

    #     with allure.step("调用接口StartAdjustViewMirror调节左后视镜向下:"):
    #         self.partner.send_method_request("OuterRearViewService_client", "StartAdjustViewMirror", {"params": [{"id":2,"direction":5}]})
    #         sleep(1)

    #     with allure.step(f"监测总线:Bodycan：DrvrExtrMirrAdjHmiReq"):
    #         result = self.ipdu.check_thread_stop('DrvrExtrMirrAdjHmiReq', timeout=5)
    #         logger.info("result {}".format(result))
    #         if result == None:
    #             assert False
    #         else:
    #             assert result[0]
    #         self.ipdu.reset_check_results()
    #     sleep(1)

    # @allure.title("左后视镜向右调节")
    # @allure.testcase(
    #     'https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46'
    #     )
    # @pytest.mark.smoke
    # @pytest.mark.sanity
    # @pytest.mark.full
    # @allure.title("左后视镜向右调节")
    # def test_caseid_1960091(self):
    #     with allure.step("设置初始化条件"):
    #         self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, "DrvrExtrMirrAdjHmiReq", 0)
    #         # 设置:Carmode 设置为Normal;
    #         self.sd_tester.change_car_mode(0, do_assert=1)
    #         sleep(0.5)
    #         # 设置:Usage 设置为02 Convenience;
    #         self.sd_tester.change_usage_mode(2, do_assert=1)
    #         sleep(0.5)
    #         self.ipdu.reset_check_results()
    #     with allure.step(f"Step:设置车速为0"):
    #         self.ipdu.set_vehspd(0)
    #         sleep(1)
    #     with allure.step("仿真洗车模式未打开"):
    #         self.partner.send_method_request("VehicleSetStatusService_client", "SetWashMode", {"isOn": False})
    #         sleep(1)

    #     self.ipdu.check_thread_start(
    #         self.ipdu.bodycan.CEMBodyFr13, 'DrvrExtrMirrAdjHmiReq', 4, timeout=2
    #     )

    #     with allure.step("调用接口StartAdjustViewMirror调节左后视镜向右:"):
    #         self.partner.send_method_request("OuterRearViewService_client", "StartAdjustViewMirror", {"params": [{"id":2,"direction":4}]})
    #         sleep(1)

    #     with allure.step(f"监测总线:Bodycan：DrvrExtrMirrAdjHmiReq"):
    #         result = self.ipdu.check_thread_stop('DrvrExtrMirrAdjHmiReq', timeout=5)
    #         logger.info("result {}".format(result))
    #         if result == None:
    #             assert False
    #         else:
    #             assert result[0]
    #         self.ipdu.reset_check_results()
    #     sleep(1)

    # @allure.title("右后视镜向上调节")
    # @allure.testcase(
    #     'https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46'
    #     )
    # @pytest.mark.smoke
    # @pytest.mark.sanity
    # @pytest.mark.full
    # def test_caseid_1960090(self):
    #     with allure.step("设置初始化条件"):
    #         self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, "PassExtrMirrAdjHmiReq", 0)
    #         # 设置:Carmode 设置为Normal;
    #         self.sd_tester.change_car_mode(0, do_assert=1)
    #         sleep(0.5)
    #         # 设置:Usage 设置为02 Convenience;
    #         self.sd_tester.change_usage_mode(2, do_assert=1)
    #         sleep(0.5)
    #         self.ipdu.reset_check_results()
    #     with allure.step(f"Step:设置车速为0"):
    #         self.ipdu.set_vehspd(0)
    #         sleep(1)
    #     with allure.step("仿真洗车模式未打开"):
    #         self.partner.send_method_request("VehicleSetStatusService_client", "SetWashMode", {"isOn": False})
    #         sleep(1)

    #     self.ipdu.check_thread_start(
    #         self.ipdu.bodycan.CEMBodyFr13, 'PassExtrMirrAdjHmiReq', 1, timeout=2
    #     )

    #     with allure.step("调用接口StartAdjustViewMirror调节右后视镜向上:"):
    #         self.partner.send_method_request("OuterRearViewService_client", "StartAdjustViewMirror", {"params": [{"id":2,"direction":2}]})
    #         sleep(1)

    #     with allure.step(f"监测总线:Bodycan：PassExtrMirrAdjHmiReq"):
    #         result = self.ipdu.check_thread_stop('PassExtrMirrAdjHmiReq', timeout=5)
    #         logger.info("result {}".format(result))
    #         if result == None:
    #             assert False
    #         else:
    #             assert result[0]
    #         self.ipdu.reset_check_results()
    #     sleep(1)

    # @allure.title("右后视镜向左调节")
    # @allure.testcase(
    #     'https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46'
    #     )
    # @pytest.mark.smoke
    # @pytest.mark.sanity
    # @pytest.mark.full
    # def test_caseid_1960089(self):
    #     with allure.step("设置初始化条件"):
    #         self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, "PassExtrMirrAdjHmiReq", 0)
    #         # 设置:Carmode 设置为Normal;
    #         self.sd_tester.change_car_mode(0, do_assert=1)
    #         sleep(0.5)
    #         # 设置:Usage 设置为02 Convenience;
    #         self.sd_tester.change_usage_mode(2, do_assert=1)
    #         sleep(0.5)
    #         self.ipdu.reset_check_results()
    #     with allure.step(f"Step:设置车速为0"):
    #         self.ipdu.set_vehspd(0)
    #         sleep(1)
    #     with allure.step("仿真洗车模式未打开"):
    #         self.partner.send_method_request("VehicleSetStatusService_client", "SetWashMode", {"isOn": False})
    #         sleep(1)

    #     self.ipdu.check_thread_start(
    #         self.ipdu.bodycan.CEMBodyFr13, 'PassExtrMirrAdjHmiReq', 3, timeout=2
    #     )

    #     with allure.step("调用接口StartAdjustViewMirror调节右后视镜向左:"):
    #         self.partner.send_method_request("OuterRearViewService_client", "StartAdjustViewMirror", {"params": [{"id":2,"direction":1}]})
    #         sleep(1)

    #     with allure.step(f"监测总线:Bodycan：PassExtrMirrAdjHmiReq"):
    #         result = self.ipdu.check_thread_stop('PassExtrMirrAdjHmiReq', timeout=5)
    #         logger.info("result {}".format(result))
    #         if result == None:
    #             assert False
    #         else:
    #             assert result[0]
    #         self.ipdu.reset_check_results()
    #     sleep(1)

    # @allure.title("右后视镜向下调节")
    # @allure.testcase(
    #     'https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46'
    #     )
    # @pytest.mark.smoke
    # @pytest.mark.sanity
    # @pytest.mark.full
    # def test_caseid_1960088(self):
    #     with allure.step("设置初始化条件"):
    #         self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, "PassExtrMirrAdjHmiReq", 0)
    #         # 设置:Carmode 设置为Normal;
    #         self.sd_tester.change_car_mode(0, do_assert=1)
    #         sleep(0.5)
    #         # 设置:Usage 设置为02 Convenience;
    #         self.sd_tester.change_usage_mode(2, do_assert=1)
    #         sleep(0.5)
    #         self.ipdu.reset_check_results()
    #     with allure.step(f"Step:设置车速为0"):
    #         self.ipdu.set_vehspd(0)
    #         sleep(1)
    #     with allure.step("仿真洗车模式未打开"):
    #         self.partner.send_method_request("VehicleSetStatusService_client", "SetWashMode", {"isOn": False})
    #         sleep(1)

    #     self.ipdu.check_thread_start(
    #         self.ipdu.bodycan.CEMBodyFr13, 'PassExtrMirrAdjHmiReq', 2, timeout=2
    #     )

    #     with allure.step("调用接口StartAdjustViewMirror调节右后视镜向下:"):
    #         self.partner.send_method_request("OuterRearViewService_client", "StartAdjustViewMirror", {"params": [{"id":2,"direction":5}]})
    #         sleep(1)

    #     with allure.step(f"监测总线:Bodycan：PassExtrMirrAdjHmiReq"):
    #         result = self.ipdu.check_thread_stop('PassExtrMirrAdjHmiReq', timeout=5)
    #         logger.info("result {}".format(result))
    #         if result == None:
    #             assert False
    #         else:
    #             assert result[0]
    #         self.ipdu.reset_check_results()
    #     sleep(1)

    # @allure.title("右后视镜向右调节")
    # @allure.testcase(
    #     'https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46'
    #     )
    # @pytest.mark.smoke
    # @pytest.mark.sanity
    # @pytest.mark.full
    # @allure.title("右后视镜向右调节")
    # def test_caseid_1960087(self):
    #     with allure.step("设置初始化条件"):
    #         self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, "PassExtrMirrAdjHmiReq", 0)
    #         # 设置:Carmode 设置为Normal;
    #         self.sd_tester.change_car_mode(0, do_assert=1)
    #         sleep(0.5)
    #         # 设置:Usage 设置为02 Convenience;
    #         self.sd_tester.change_usage_mode(2, do_assert=1)
    #         sleep(0.5)
    #         self.ipdu.reset_check_results()
    #     with allure.step(f"Step:设置车速为0"):
    #         self.ipdu.set_vehspd(0)
    #         sleep(1)
    #     with allure.step("仿真洗车模式未打开"):
    #         self.partner.send_method_request("VehicleSetStatusService_client", "SetWashMode", {"isOn": False})
    #         sleep(1)

    #     self.ipdu.check_thread_start(
    #         self.ipdu.bodycan.CEMBodyFr13, 'PassExtrMirrAdjHmiReq', 4, timeout=2
    #     )

    #     with allure.step("调用接口StartAdjustViewMirror调节右后视镜向右:"):
    #         self.partner.send_method_request("OuterRearViewService_client", "StartAdjustViewMirror", {"params": [{"id":2,"direction":4}]})
    #         sleep(1)

    #     with allure.step(f"监测总线:Bodycan：PassExtrMirrAdjHmiReq"):
    #         result = self.ipdu.check_thread_stop('PassExtrMirrAdjHmiReq', timeout=5)
    #         logger.info("result {}".format(result))
    #         if result == None:
    #             assert False
    #         else:
    #             assert result[0]
    #         self.ipdu.reset_check_results()
    #     sleep(1)

    @allure.title("屏幕按钮点击外后视镜展开")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46"
    )
    @pytest.mark.smoke
    @allure.title("屏幕按钮点击外后视镜展开")
    def test_caseid_1960051(self):
        with allure.step("设置初始化条件"):
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, "MirrFoldStsAtDrvr", 0)  # 折叠
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, "MirrFoldStsAtPass", 0)
            #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)

            # 设置:Carmode 设置为Normal;
            self.sd_tester.change_car_mode(0, do_assert=1)

            # 设置:Usage 设置为02 Convenience;
            self.sd_tester.change_usage_mode(2, do_assert=1)

            self.ipdu.reset_check_results()
        with allure.step(f"Step:设置车速为0"):
            self.ipdu.set_vehspd(0)

        with allure.step("仿真洗车模式未打开"):
            self.partner.send_method_request(
                "VehicleSetStatusService_client", "SetWashMode", {"isOn": False}
            )

        self.ipdu.check_thread_start(
            self.ipdu.bodycan.CEMBodyFr13, "ExtrMirrFoldHmiReq", 0, timeout=2
        )
        with allure.step("设置后视镜展开"):
            self.partner.send_method_request(
                "OuterRearViewService_client",
                "UnFold",
                {"views": [2], "isAutoUnFold": False},
            )  # 0 左后视镜 1 右后视镜  2 所有后视镜

        with allure.step(f"监测总线:Bodycan：ExtrMirrFoldHmiReq"):
            result = self.ipdu.check_thread_stop("ExtrMirrFoldHmiReq", timeout=5)
            logger.info("result {}".format(result))
            if result == None:
                assert False
            else:
                assert result[0]
            self.ipdu.reset_check_results()

    @allure.title("Normal_Driving模式打开后视镜加热")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46'
        )
    @pytest.mark.smoke
    def test_caseid_1960097(self):
        with allure.step("设置初始化条件"):
            #使用模式 Usage Mode=13 driving
            self.sd_tester.change_usage_mode(13)
            #车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 5, 13: 4})
        with allure.step("设置后视镜加热"):
            self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',1,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        with allure.step(f"Step:查看信号MirrDefrstAtDrvSts"):
            logger.info("查看信号MirrDefrstAtDrvSts" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'MirrDefrstAtDrvSts',1,timeout=2)
            self.ipdu.check_thread_stop('MirrDefrstAtDrvSts', timeout=5)
        with allure.step(f"Step:查看信号MirrDefrstAtPassSts"):
            logger.info("查看信号MirrDefrstAtPassSts" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'MirrDefrstAtPassSts',1,timeout=2)
            self.ipdu.check_thread_stop('MirrDefrstAtPassSts', timeout=5)

        self.ipdu.reset_check_results() 
        
    @allure.title("Normal_Driving模式关闭后视镜加热")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46'
        )
    @pytest.mark.smoke
    def test_caseid_1960098(self):
        with allure.step("设置初始化条件"):
            #使用模式 Usage Mode=13 driving
            self.sd_tester.change_usage_mode(13)

            #车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            self.sd_tester.write_multi_ccp({182: 5, 13: 4})
        with allure.step("设置后视镜加热"):
            self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        with allure.step(f"Step:查看信号MirrDefrstAtDrvSts"):
            logger.info("查看信号MirrDefrstAtDrvSts" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'MirrDefrstAtDrvSts',0,timeout=2)
            self.ipdu.check_thread_stop('MirrDefrstAtDrvSts', timeout=5)
        with allure.step(f"Step:查看信号MirrDefrstAtPassSts"):
            logger.info("查看信号MirrDefrstAtPassSts" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'MirrDefrstAtPassSts',0,timeout=2)
            self.ipdu.check_thread_stop('MirrDefrstAtPassSts', timeout=5)

        self.ipdu.reset_check_results() 
        
    @allure.title("Crash_Convenience模式后视镜无法加热")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46'
        )
    @pytest.mark.smoke
    def test_caseid_1960101(self):
        with allure.step("设置初始化条件"):
            #使用模式 Usage Mode=02 convenience
            self.sd_tester.change_usage_mode(2)

            #车辆模式Car Mode == 03 Crash
            self.sd_tester.change_car_mode(3)
            self.sd_tester.write_multi_ccp({182: 5, 13: 4})
        with allure.step("设置后视镜加热"):
            self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        with allure.step(f"Step:查看信号MirrDefrstAtDrvSts"):
            logger.info("查看信号MirrDefrstAtDrvSts" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'MirrDefrstAtDrvSts',0,timeout=2)
            self.ipdu.check_thread_stop('MirrDefrstAtDrvSts', timeout=5)
        with allure.step(f"Step:查看信号MirrDefrstAtPassSts"):
            logger.info("查看信号MirrDefrstAtPassSts" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'MirrDefrstAtPassSts',0,timeout=2)
            self.ipdu.check_thread_stop('MirrDefrstAtPassSts', timeout=5)

        self.ipdu.reset_check_results() 
        
    @allure.title("Transport_Convenience模式后视镜无法加热")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46'
        )
    @pytest.mark.sanity
    def test_caseid_1960102(self):
        with allure.step("设置初始化条件"):
            #使用模式 Usage Mode=02 convenience
            self.sd_tester.change_usage_mode(2)

            #车辆模式Car Mode == 01 Transport
            self.sd_tester.change_car_mode(1)
            self.sd_tester.write_multi_ccp({182: 5, 13: 4})
        with allure.step("设置后视镜加热"):
            self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        with allure.step(f"Step:查看信号MirrDefrstAtDrvSts"):
            logger.info("查看信号MirrDefrstAtDrvSts" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'MirrDefrstAtDrvSts',0,timeout=2)
            self.ipdu.check_thread_stop('MirrDefrstAtDrvSts', timeout=5)
        with allure.step(f"Step:查看信号MirrDefrstAtPassSts"):
            logger.info("查看信号MirrDefrstAtPassSts" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'MirrDefrstAtPassSts',0,timeout=2)
            self.ipdu.check_thread_stop('MirrDefrstAtPassSts', timeout=5)

        self.ipdu.reset_check_results() 
        
    @allure.title("Factory_Convenience模式后视镜无法加热")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46'
        )
    @pytest.mark.full
    def test_caseid_1960103(self):
        with allure.step("设置初始化条件"):
            #使用模式 Usage Mode=02 convenience
            self.sd_tester.change_usage_mode(2)

            #车辆模式Car Mode == 02 Factory
            self.sd_tester.change_car_mode(2)
            self.sd_tester.write_multi_ccp({182: 5, 13: 4})
        with allure.step("设置后视镜加热"):
            self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',0,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        with allure.step(f"Step:查看信号MirrDefrstAtDrvSts"):
            logger.info("查看信号MirrDefrstAtDrvSts" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'MirrDefrstAtDrvSts',0,timeout=2)
            self.ipdu.check_thread_stop('MirrDefrstAtDrvSts', timeout=5)
        with allure.step(f"Step:查看信号MirrDefrstAtPassSts"):
            logger.info("查看信号MirrDefrstAtPassSts" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'MirrDefrstAtPassSts',0,timeout=2)
            self.ipdu.check_thread_stop('MirrDefrstAtPassSts', timeout=5)

        self.ipdu.reset_check_results() 
        
    @allure.title("Dyno_Driving模式打开后视镜加热")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1892743?projectId=46'
        )
    @pytest.mark.full
    @allure.title("Dyno_Driving模式打开后视镜加热")
    def test_caseid_1960099(self):
        with allure.step("设置初始化条件"):
            #车辆模式Car Mode == 00 Normal
            self.sd_tester.change_car_mode(0)
            #使用模式 Usage Mode=02 convenience
            self.sd_tester.change_usage_mode(2)
            #车辆模式Car Mode == 05 Dyno
            self.sd_tester.change_car_mode(5)
            #使用模式 Usage Mode=13 driving
            self.sd_tester.change_usage_mode(13)
            self.sd_tester.write_multi_ccp({182: 5, 13: 4})
        with allure.step("设置后视镜加热"):
            self.partner.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        with allure.step(f"Step:查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe"):
            logger.info("查看信号CemBackBoneFr19:0x180:HmiDefrstrElecStsRe" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'HmiDefrstrElecStsRe',1,timeout=2)
            self.ipdu.check_thread_stop('HmiDefrstrElecStsRe', timeout=5)
        with allure.step(f"Step:查看信号MirrDefrstAtDrvSts"):
            logger.info("查看信号MirrDefrstAtDrvSts" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'MirrDefrstAtDrvSts',1,timeout=2)
            self.ipdu.check_thread_stop('MirrDefrstAtDrvSts', timeout=5)
        with allure.step(f"Step:查看信号MirrDefrstAtPassSts"):
            logger.info("查看信号MirrDefrstAtPassSts" )
            self.ipdu.check_thread_start(self.ipdu.backbonefr.CemBackBoneFr19,'MirrDefrstAtPassSts',1,timeout=2)
            self.ipdu.check_thread_stop('MirrDefrstAtPassSts', timeout=5)
