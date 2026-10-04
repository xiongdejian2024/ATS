#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import time
import threading
import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.interface import *


@allure.feature("互联服务/远程控制/远控稳定性控制")
@allure.story("远控稳定性控制")
class TestRCRepeat(TestABCBase):
    def before_class(self, ecu):
        self.tsp.set_bench_config(self.tb_config["Vehicle_vid"], self.tb_config["tel"])


    def before_each_func(self, ecu):
        pass

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        pass

    # @pytest.mark.repeat(20)
    @allure.title("远控实车-RVC_远控打开极速制冷")
    @pytest.mark.stress_test
    def test_rvc_climate_control_caseid_1990673(self, ecu):
        self.mix.vehicle_sleep()
        logger.info("已休眠")
        execid = self.tsp.rvc_cold_down(1)
        time.sleep(5)
        result = self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        logger.info("极速制冷开启结果：{}".format(result))
        time.sleep(60)
        execid1 = self.tsp.rvc_cold_down(-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert result
        self.mix.vehicle_sleep()

    # @pytest.mark.repeat(20)
    @allure.title("远控实车-RVC_远控打开极速制热")
    @pytest.mark.stress_test
    def test_rvc_climate_control_caseid_1990674(self, ecu):
        self.mix.vehicle_sleep()
        logger.info("已休眠")
        execid = self.tsp.rvc_heat_up(1)
        time.sleep(5)
        result = self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        logger.info("极速制热开启结果：{}".format(result))
        execid = self.tsp.rvc_cold_down(1)
        time.sleep(60)
        execid1 = self.tsp.rvc_cold_down(-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert result
        self.mix.vehicle_sleep()

    # @pytest.mark.repeat(20)
    @allure.title("远控实车-RVC_远控打开除霜")
    @pytest.mark.stress_test
    def test_rvc_climate_control_caseid_1987073(self, ecu):
        self.mix.vehicle_sleep()
        logger.info("已休眠")
        execid = self.tsp.rvc_defrost_control(1)
        time.sleep(5)
        result = self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        logger.info("除霜开启结果：{}".format(result))
        execid = self.tsp.rvc_cold_down(1)
        time.sleep(60)
        execid1 = self.tsp.rvc_cold_down(-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert result
        self.mix.vehicle_sleep()

    # @pytest.mark.repeat(20)
    @allure.title("远控实车-RVC_远控打开方向盘加热")
    @pytest.mark.stress_test
    def test_rvc_climate_control_caseid_1987074(self, ecu):
        self.mix.vehicle_sleep()
        logger.info("已休眠")
        execid = self.tsp.rvc_steering_wheel_heat(1)
        time.sleep(5)
        result = self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        logger.info("方向盘加热开启结果：{}".format(result))
        execid = self.tsp.rvc_cold_down(1)
        time.sleep(60)
        execid = self.tsp.rvc_cold_down(-1)
        execid1 = self.tsp.rvc_steering_wheel_heat(-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert result
        self.mix.vehicle_sleep()

    # @pytest.mark.repeat(20)
    @allure.title("远控实车-RVC_远控打开主驾座椅加热")
    @pytest.mark.stress_test
    def test_rvc_climate_control_caseid_1987075(self, ecu):
        self.mix.vehicle_sleep()
        logger.info("已休眠")
        execid = self.tsp.rvc_driver_seat_heat(1)
        time.sleep(5)
        result = self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        logger.info("主驾座椅加热开启结果：{}".format(result))
        execid = self.tsp.rvc_cold_down(1)
        time.sleep(60)
        execid = self.tsp.rvc_cold_down(-1)
        execid1 = self.tsp.rvc_driver_seat_heat(-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert result
        self.mix.vehicle_sleep()

    # @pytest.mark.repeat(20)
    @allure.title("远控实车-RVC_远控打开空调")
    @pytest.mark.stress_test
    def test_rvc_climate_control_caseid_1987076(self, ecu):
        self.mix.vehicle_sleep()
        logger.info("已休眠")
        execid = self.tsp.rvc_ac_control(1,220)
        time.sleep(5)
        result = self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        logger.info("空调开启结果：{}".format(result))
        time.sleep(60)
        execid1 = self.tsp.rvc_ac_control(-1,220)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert result
        self.mix.vehicle_sleep()

    # @pytest.mark.repeat(20)
    @allure.title("远控实车-RVC_远控打开副驾座椅加热")
    @pytest.mark.stress_test
    def test_rvc_climate_control_caseid_1987077(self, ecu):
        self.mix.vehicle_sleep()
        logger.info("已休眠")
        execid = self.tsp.rvc_passenger_seat_heat(1)
        time.sleep(5)
        result = self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        logger.info("副驾座椅加热开启结果：{}".format(result))
        execid = self.tsp.rvc_cold_down(1)
        time.sleep(60)
        execid = self.tsp.rvc_cold_down(-1)
        execid1 = self.tsp.rvc_passenger_seat_heat(-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert result
        self.mix.vehicle_sleep()

    # @pytest.mark.repeat(20)
    @allure.title("远控实车-RVC_远控打开左后座椅加热")
    @pytest.mark.stress_test
    def test_rvc_climate_control_caseid_1987078(self, ecu):
        self.mix.vehicle_sleep()
        logger.info("已休眠")
        execid = self.tsp.rvc_rearleft_seat_heat(1)
        time.sleep(5)
        result = self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        logger.info("左后座椅加热开启结果：{}".format(result))
        execid = self.tsp.rvc_cold_down(1)
        time.sleep(60)
        execid = self.tsp.rvc_cold_down(-1)
        execid1 = self.tsp.rvc_rearleft_seat_heat(-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert result
        self.mix.vehicle_sleep()

    # @pytest.mark.repeat(20)
    @allure.title("远控实车-RVC_远控打开右后座椅加热")
    @pytest.mark.stress_test
    def test_rvc_climate_control_caseid_1987079(self, ecu):
        self.mix.vehicle_sleep()
        logger.info("已休眠")
        execid = self.tsp.rvc_rearright_seat_heat(1)
        time.sleep(5)
        result = self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        logger.info("右后座椅加热开启结果：{}".format(result))
        execid = self.tsp.rvc_cold_down(1)
        time.sleep(60)
        execid = self.tsp.rvc_cold_down(-1)
        execid1 = self.tsp.rvc_rearright_seat_heat(-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert result
        self.mix.vehicle_sleep()

    # @pytest.mark.repeat(20)
    @allure.title("远控实车-RVC_远控打开主驾座椅通风")
    @pytest.mark.stress_test
    def test_rvc_climate_control_caseid_1987080(self, ecu):
        self.mix.vehicle_sleep()
        logger.info("已休眠")
        execid = self.tsp.rvc_driver_seat_vent(1)
        time.sleep(5)
        result = self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        logger.info("主驾座椅通风开启结果：{}".format(result))
        time.sleep(60)
        execid1 = self.tsp.rvc_driver_seat_vent(-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert result
        self.mix.vehicle_sleep()

    # @pytest.mark.repeat(20)
    @allure.title("远控实车-RVC_远控打开副驾座椅通风")
    @pytest.mark.stress_test
    def test_rvc_climate_control_caseid_1987081(self, ecu):
        self.mix.vehicle_sleep()
        logger.info("已休眠")
        execid = self.tsp.rvc_passenger_seat_vent(1)
        time.sleep(5)
        result = self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        logger.info("副驾座椅通风开启结果：{}".format(result))
        time.sleep(60)
        execid1 = self.tsp.rvc_passenger_seat_vent(-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert result
        self.mix.vehicle_sleep()

    # @pytest.mark.repeat(20)
    @allure.title("远控实车-RVC_远控打开左后座椅通风")
    @pytest.mark.stress_test
    def test_rvc_climate_control_caseid_1987082(self, ecu):
        self.mix.vehicle_sleep()
        logger.info("已休眠")
        execid = self.tsp.rvc_rear_left_seat_vent(1)
        time.sleep(5)
        result = self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        logger.info("左后座椅通风开启结果：{}".format(result))
        time.sleep(60)
        execid1 = self.tsp.rvc_rear_left_seat_vent(-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert result
        self.mix.vehicle_sleep()

    # @pytest.mark.repeat(20)
    @allure.title("远控实车-RVC_远控打开右后座椅通风")
    @pytest.mark.stress_test
    def test_rvc_climate_control_caseid_1987083(self, ecu):
        self.mix.vehicle_sleep()
        logger.info("已休眠")
        execid = self.tsp.rvc_rear_right_seat_vent(1)
        time.sleep(5)
        result = self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        logger.info("右后座椅通风开启结果：{}".format(result))
        time.sleep(60)
        execid1 = self.tsp.rvc_rear_right_seat_vent(-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert result
        self.mix.vehicle_sleep()

    @pytest.mark.repeat(40)
    @allure.title("远控实车-RVC_远控一键备车")
    @pytest.mark.stress_test
    def test_rvc_climate_control_caseid_1987910(self, ecu):
        self.mix.vehicle_sleep()
        logger.info("已休眠")
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [1,2,3,4,5,6])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2(op=1)
        execid1 = execid0 + "&&&conditionalAcControl"
        execid2 = execid0 + "&&&driverSeatVent"
        execid3 = execid0 + "&&&passengerSeatVent"
        execid4 = execid0 + "&&&rearLeftSeatVent"
        execid5 = execid0 + "&&&rearRightSeatVent"
        execid6 = execid0 + "&&&driverSeatHeat"
        execid7 = execid0 + "&&&passengerSeatHeat"
        execid8 = execid0 + "&&&rearLeftSeatHeat"
        execid9 = execid0 + "&&&rearRightSeatHeat"
        execidx = execid0 + "&&&steeringWheelHeat"
        time.sleep(5)
        result1 = self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        result2 = self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success")
        result3 = self.tsp.log_search_remote_vehicle_control(execid=execid3, keywords="Success")
        result4 = self.tsp.log_search_remote_vehicle_control(execid=execid4, keywords="Success")
        result5 = self.tsp.log_search_remote_vehicle_control(execid=execid5, keywords="Success")
        result5 = self.tsp.log_search_remote_vehicle_control(execid=execid5, keywords="Success")
        result6 = self.tsp.log_search_remote_vehicle_control(execid=execid6, keywords="Success")
        result7 = self.tsp.log_search_remote_vehicle_control(execid=execid7, keywords="Success")
        result8 = self.tsp.log_search_remote_vehicle_control(execid=execid8, keywords="Success")
        result9 = self.tsp.log_search_remote_vehicle_control(execid=execid9, keywords="Success")
        resultx = self.tsp.log_search_remote_vehicle_control(execid=execidx, keywords="Success")
        time.sleep(60)
        execid2 = self.tsp.rvc_one_click_smart_cockpit_2(op=-1)
        execid3 = execid2 + "&&&conditionalAcControl"
        assert self.tsp.log_search_remote_vehicle_control(execid=execid3, keywords="Success")
        assert result1&result2&result3&result4&result5&result6&result7&result8&result9&resultx
        time.sleep(60)
        self.mix.vehicle_sleep()

    # @pytest.mark.repeat(20)
    @allure.title("远控实车-RVC_远控后视镜折叠展开")
    @pytest.mark.stress_test
    def test_rvc_climate_control_caseid_1987084(self, ecu):
        self.mix.vehicle_sleep()
        logger.info("已休眠")
        execid = self.tsp.rvc_rear_view_control(op=1)
        time.sleep(5)
        result = self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        logger.info("后视镜展开结果：{}".format(result))
        time.sleep(60)
        execid1 = self.tsp.rvc_rear_view_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert result
        self.mix.vehicle_sleep()