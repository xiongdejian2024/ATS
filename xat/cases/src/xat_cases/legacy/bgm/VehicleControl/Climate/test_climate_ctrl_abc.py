#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_climate_ctrl_abc.py
@Author      : xiangyue.li@jiduauto.com
@Time        : 2023/12/7 11:30
@Description : BGM空调功能
"""

import os
import sys
import pytest
import allure
from time import sleep


sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("车控车设")
@allure.story("空调功能")
class TestClimateCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["ClimateControlService_client", "OuterRearViewService_client", "ResetSOAConfigService_client"])
        sleep(2)

    def before_each_func(self, ecu):
        self.climate_precondition()
        pass

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    def climate_precondition(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)

    def ecm_precondition(self):
        self.bus_comm.set_singal("bodycan", "CcmBodyFr21", "ResrvdSigForECM2", 0)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.set_singal("bodycan", "CcmBodyFr25", "FrntHvacBlowerSts", 1)

    def notwindmode(self):
        try:
            self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Face)
            self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Auto)
            self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)
        except:
            assert True

    def autostatus(self):
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRow,mode=AirWindMode.Face)
        
    def defrostoff(self):
        self.bus_comm.check_HmiDefrstMaxReq(sts=OnOff.Off)
        return False
    
    @allure.title("联动_Auto模式_关闭Auto模式_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109081(self):
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.FaceDefrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("联动_Auto模式_设置副驾吹面_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109358(self):
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)   
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.FaceDefrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Face)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)
		
    @allure.title("联动_OFF_打开副驾吹脚_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108769(self):
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.FaceDefrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)
		
    @allure.title("联动_OFF_打开Auto模式_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108879(self):
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)
		
    @allure.title("联动_手动模式_打开Auto模式_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_116156(self):
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)

    @allure.title("联动_手动模式_打开Auto模式_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_108194(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow,sts=isOn.Off)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)
        		
    @allure.title("联动_前除霜除雾_打开Auto模式_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115867(self):
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.get_climate_mode(mode=ClimateMode.kDefrost)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)
                                    
    @allure.title("联动_OFF_打开前除霜除雾_风量")
    @pytest.mark.smoke_1
    def test_climate_soa_caseid_109306(self):
        self.soa.hmi_set_climate_windspeed(
            zone=ClimateZone.AllZone, speed=WindSpeed.kLvlMan5
        )
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_windspeed_sts_req(
            pos=SeatVenPos.Front, speed=SeatVenSpeed.LvlMan9
        )

    @allure.title("联动_OFF_打开前除霜除雾_香氛")
    @pytest.mark.full
    def test_climate_soa_caseid_109165(self):
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_climate_fragrance_req(taste=FragChannel.Channel1,level=FragLevel.Level2,ch1_ratio=100.0)

    @allure.title("联动_OFF_打开前除霜除雾_温度不同步")
    @pytest.mark.full
    def test_climate_soa_caseid_108821(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=25.0)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.get_climate_sync_mode(sts=False)
        self.soa.get_climate_sys_sts(temp_dri=23.0,temp_pass=24.0,temp_sec_row=25.0)

    @allure.title("联动_OFF_调节风量_AC状态_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_109177(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=False, timeout=0.5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windspeed(
            zone=ClimateZone.AllZone, speed=WindSpeed.kLvlMan3
        )
        self.soa.get_climate_ac_sts(sts=False)

    @allure.title("联动_手动模式_调节风量_AC状态_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_108156(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True, timeout=0.5)
        self.soa.hmi_set_climate_windspeed(
            zone=ClimateZone.AllZone, speed=WindSpeed.kLvlMan3
        )
        self.soa.hmi_set_climate_windspeed(
            zone=ClimateZone.AllZone, speed=WindSpeed.kLvlMan5
        )
        self.soa.get_climate_ac_sts(sts=1)

    @allure.title("联动_OFF_打开Auto模式_内外循环模式_Auto循环")
    @pytest.mark.smoke
    def test_climate_soa_caseid_115471(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone, sts=True)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_打开Auto模式_内外循环模式_外循环")
    @pytest.mark.smoke
    def test_climate_soa_caseid_115469(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone, sts=True)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_打开Auto模式_内外循环模式_内循环")
    @pytest.mark.smoke
    def test_climate_soa_caseid_108760(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone, sts=True)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_调节风量_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_109331(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

#v2.0以前CR：
    # @allure.title("初始化默认_前后排风速_OFF状态")
    # @pytest.mark.full
    # def test_climate_soa_caseid_109706(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
    #     self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
    #     self.io.io_reset_bgm()
    #     sleep(15)
    #     self.bus_comm.check_windspeed_sts_req(
    #         pos=SeatVenPos.All, speed=SeatVenSpeed.Off
    #     )

    # @allure.title("初始化默认_香氛信息")
    # @pytest.mark.smoke
    # def test_climate_soa_caseid_109705(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
    #     self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)

    #     self.io.io_reset_bgm()
    #     sleep(15)
    #     self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.All,speed=SeatVenSpeed.Off)

    # @allure.title("初始化默认_前后排风速_Auto状态")
    # @pytest.mark.full
    # def test_climate_soa_caseid_109704(self):
    #     self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone, sts=True)
    #     self.io.io_reset_bgm()
    #     sleep(15)
    #     self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front, speed=SeatVenSpeed.LvlAutNorm)

    @allure.title("出厂化设置_香氛类型")
    @pytest.mark.sanity
    def test_climate_soa_caseid_109701(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_reset_config_sts()
        sleep(10)
        self.bus_comm.check_climate_fragrance_req(taste=FragChannel.NoReq,level=FragLevel.LevelOff)

    @allure.title("初始化默认_调节温度_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_1988707(self):
        self.soa.hmi_set_reset_config_sts()
        sleep(15)
        self.bus_comm.check_climate_temp_req(zone=ClimateZone.AllZone, value=22.0)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft, value=25.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight, value=25.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow, value=25.0)
        self.bus_comm.check_climate_temp_req(zone=ClimateZone.AllZone, value=25.0)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)

    @allure.title("出厂化设置_吹风模式")
    @pytest.mark.sanity
    def test_climate_soa_caseid_109699(self):
        self.soa.hmi_set_reset_config_sts()
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)
        self.soa.get_windmode_sts(zone=ClimateZone.SecondRow, mode=AirWindMode.Auto)
        self.soa.get_windmode_sts(zone=ClimateZone.FirstRowLeft, mode=AirWindMode.Auto)
        self.soa.get_windmode_sts(zone=ClimateZone.FirstRowRight, mode=AirWindMode.Auto)
        
    @allure.title("联动_手动模式_调节风量_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108159(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft, on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_手动模式_温度同步设置_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108144(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft, on=isOn.On)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_sync_sts(sts=True)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_手动模式_前出风口风向调节_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108108(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft, on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_angle_sts(pos=ClimateZone.FirstRowLeftLeft,side=OutletSide.Left,hori_ang=10,ver_ang=15)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )
        
    @allure.title("联动_手动模式_后出风口风向调节_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108143(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft, on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_angle_sts(pos=ClimateZone.SecondRowLeftLeft,side=OutletSide.Left,hori_ang=10,ver_ang=15)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )
                     
    @allure.title("联动_手动模式_打开Auto模式_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_116151(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_windspeed(
            zone=ClimateZone.FirstRowLeft, speed=WindSpeed.kLvlMan3
        )
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone, sts=True)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_手动模式_打开Auto模式_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_108154(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(
            zone=ClimateZone.FirstRowLeft, speed=WindSpeed.kLvlMan3
        )
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone, sts=True)
        self.bus_comm.check_windspeed_sts_req(
            pos=SeatVenPos.Front, speed=SeatVenSpeed.LvlAutNorm
        )

    @allure.title("联动_OFF_打开Auto模式_风量")
    @pytest.mark.smoke
    def test_climate_soa_caseid_108717(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(
            zone=ClimateZone.FirstRowLeft, speed=WindSpeed.kLvlMan3
        )
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone, sts=True)
        self.bus_comm.check_windspeed_sts_req(
            pos=SeatVenPos.Front, speed=SeatVenSpeed.LvlAutNorm
        )

    @allure.title("联动_OFF_AC设置_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108883(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow, on=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_ac_sts(sts=True, timeout=0.5)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_Auto模式_AC设置_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108850(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow, on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_ac_sts(sts=False, timeout=0.5)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_OFF_打开Auto循环_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109328(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow, on=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_OFF_打开Auto循环_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109328(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow, on=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_OFF_打开Auto循环_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109328(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow, on=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_OFF_打开外循环_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108814(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow, on=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )       

    @allure.title("联动_OFF_打开内循环_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108834(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow, on=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_OFF_打开Auto模式_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108746(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow, on=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_OFF_调节后排温度_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109262(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow, on=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=23.0)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_Auto模式_调节主驾温度_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108786(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow, on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone, sts=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_Auto模式_调节后排温度_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108784(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow, on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone, sts=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=23.0)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_Auto模式_调节风量_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108836(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow, on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_OFF_调节风量_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109130(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow, on=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_OFF_调节主驾温度_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108859(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow, on=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_OFF_调节副驾温度_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109018(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow, on=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=23.0)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_手动模式_打开前除霜除雾_温度不同步")
    @pytest.mark.full
    def test_climate_soa_caseid_108821(self):
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=25.0)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.get_climate_sync_mode(sts=False)
        self.bus_comm.check_climate_temp_req(zone=ClimateZone.FirstRowLeft, value=23.0)
        self.bus_comm.check_climate_temp_req(zone=ClimateZone.FirstRowRight, value=24.0)
        self.bus_comm.check_climate_temp_req(zone=ClimateZone.SecondRow, value=25.0)
        
    @allure.title("联动_手动模式_后出风口风向调节_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108090(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.SecondRow, on=isOn.On)
        self.soa.hmi_set_climate_angle_sts(pos=ClimateZone.SecondRow,side=OutletSide.Left,hori_ang=20,ver_ang=25)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_angle_sts(pos=ClimateZone.SecondRow,side=OutletSide.Left,hori_ang=45,ver_ang=35)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)


    @allure.title("联动_手动模式_前出风口风向调节_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108121(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.SecondRow, on=isOn.On)
        self.soa.hmi_set_climate_angle_sts(pos=ClimateZone.FirstRow,side=OutletSide.Left,hori_ang=20,ver_ang=25)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_angle_sts(pos=ClimateZone.FirstRow,side=OutletSide.Left,hori_ang=45,ver_ang=35)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)

    @allure.title("联动_Auto模式_前出风口风向调节_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108462(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_angle_sts(pos=ClimateZone.FirstRowLeftLeft,side=OutletSide.Left,hori_ang=10,ver_ang=15)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_angle_sts(pos=ClimateZone.FirstRowLeftLeft,side=OutletSide.Left,hori_ang=40,ver_ang=30)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutNorm)

    @allure.title("联动_Auto模式_前出风口风向调节_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108511(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft, on=isOn.On)
        self.soa.hmi_set_climate_angle_sts(pos=ClimateZone.FirstRowLeftLeft,side=OutletSide.Left,hori_ang=10,ver_ang=15)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_Auto模式_后出风口风向调节_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108417(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.SecondRowLeftLeft, on=isOn.On)
        self.soa.hmi_set_climate_angle_sts(pos=ClimateZone.SecondRowLeftLeft,side=OutletSide.Left,hori_ang=10,ver_ang=15)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_Auto模式_前出风口风向调节_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_108485(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoNormal)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft, on=isOn.On)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutNorm)
        
    @allure.title("联动_Auto模式_后出风口风向调节_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108510(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_angle_sts(pos=ClimateZone.FirstRowLeftLeft,side=OutletSide.Left,hori_ang=10,ver_ang=15)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_angle_sts(pos=ClimateZone.FirstRowLeftLeft,side=OutletSide.Left,hori_ang=40,ver_ang=30)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutNorm)

    @allure.title("联动_手动模式_打开内循环_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108119(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.5)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=WindSpeed.kLvlMan3)

    @allure.title("联动_手动模式_打开外循环_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_116073(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)

    @allure.title("联动_手动模式_调节主驾温度_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108141(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.On)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.AllZone,value=23.0)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.AllZone,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.5)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)

    @allure.title("联动_手动模式_AC设置_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_113207(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)  
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)
        
    @allure.title("联动_手动模式_香氛功能请求_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108142(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel2,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)        
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        
    @allure.title("联动_手动模式_香氛功能请求_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_116176(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel2,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)        
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_手动模式_AC设置_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108167(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow, on=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=False,timeout=0.5)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)  
        self.soa.hmi_set_climate_ac_sts(sts=True,timeout=0.5)      
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)

    @allure.title("联动_手动模式_AC设置_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_108166(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)  
        self.soa.hmi_set_climate_ac_sts(sts=True,timeout=0.5)      
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)
        
    @allure.title("联动_手动模式_AC设置_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_116153(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow, on=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=False,timeout=0.5)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)  
        self.soa.hmi_set_climate_ac_sts(sts=True,timeout=0.5)      
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_手动模式_调节后排温度_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_116106(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.AllZone,value=23.0)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=23.5)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_手动模式_调节后排温度_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108185(self):
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=23.5)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)

    @allure.title("联动_手动模式_打开Auto模式_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108133(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft, on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_手动模式_关闭总开关_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108130(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft, on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_手动模式_设置主驾吹脚_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115656(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_手动模式_设置副驾吹脚_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115658(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)
              
    @allure.title("联动_手动模式_关闭总开关_香氛")
    @pytest.mark.full
    def test_climate_soa_caseid_1991946(self):
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.bus_comm.check_climate_fragrance_req(taste=FragChannel.Channel1,level=FragLevel.Level2,ch1_ratio=100.0)
                       
    @allure.title("联动_Auto模式_前出风口开关_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108449(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.Off)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutNorm)

    @allure.title("联动_Auto模式_打开前除霜除雾_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_108459(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.AllZone, on=isOn.Off)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=23.0)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.SecondRow, on=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)
        
    @allure.title("联动_Auto模式_后出风口开关_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108484(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.SecondRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.SecondRowLeftLeft,on=isOn.Off)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutNorm)

    @allure.title("联动_Auto模式_后出风口开关_AC状态_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_118949(self):
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.AllZone,on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.SecondRowLeftLeft,on=isOn.Off)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)
        
    @allure.title("联动_Auto模式_香氛功能请求_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108488(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.AllZone,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutNorm)


    @allure.title("联动_Auto模式_香氛功能请求_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_108431(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False,timeout=0.5)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.AllZone,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("联动_Auto模式_设置副驾吹脚_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_108668(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)
        
    @allure.title("联动_Auto模式_设置副驾吹面_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_108697(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)

    @allure.title("联动_Auto模式_设置主驾吹面_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_108718(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)

    @allure.title("联动_Auto模式_设置主驾吹脚_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_109228(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)
        
    @allure.title("联动_Auto模式_设置主驾吹窗_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_108846(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)
                             
    @allure.title("联动_Auto模式_关闭后排开关_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108534(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutNorm)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Rear,speed=SeatVenSpeed.Off)

    @allure.title("联动_Auto模式_调节主驾温度_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108650(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.AllZone,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.5)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutNorm)

    @allure.title("联动_Auto模式_调节副驾温度_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108708(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.AllZone,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=23.0)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=23.5)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutNorm)

    @allure.title("联动_Auto模式_关闭Auto模式_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_108785(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False,timeout=0.5)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)

    @allure.title("联动_Auto模式_AC设置_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_109158(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)

    @allure.title("联动_Auto模式_打开内循环_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_109187(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)

    @allure.title("联动_Auto模式_打开外循环_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_109313(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)

    @allure.title("联动_Auto模式_打开Auto循环_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_109106(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("联动_Auto模式_打开内循环_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_109187(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)
        
    @allure.title("联动_Auto模式_AC设置_电源状态_后排关闭 ")
    @pytest.mark.full
    def test_climate_soa_caseid_109158(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)
                       
    @allure.title("联动_Auto模式_关闭Auto模式_风量")
    @pytest.mark.smoke
    def test_climate_soa_caseid_108693(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoNormal)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)
        
    @allure.title("联动_Auto模式_AC设置_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108793(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_ac_sts(sts=False,timeout=0.5)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)

    @allure.title("联动_Auto模式_前出风口风向调节_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108440(self):
        self.climate_precondition()
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.AllZone,on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_angle_sts(pos=ClimateZone.FirstRowLeftLeft,side=OutletSide.Left,hori_ang=10,ver_ang=15)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)

    @allure.title("联动_Auto模式_后出风口风向调节_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108416(self):
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.AllZone,on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_angle_sts(pos=ClimateZone.SecondRowLeftLeft,side=OutletSide.Left,hori_ang=10,ver_ang=15)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)        

    @allure.title("联动_Auto模式_AC设置_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109255(self):
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_ac_sts(sts=False,timeout=0.5)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.FaceDefrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("联动_Auto模式_关闭总开关_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108837(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.AllZone,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.Off)

    @allure.title("联动_Auto模式_设置后排吹脚_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108905(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Auto)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Foot)

    @allure.title("联动_Auto模式_调节后排温度_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108949(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Auto)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=23.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=23.5)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)

    @allure.title("联动_Auto模式_设置主驾吹面_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108960(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Face)

    @allure.title("联动_Auto模式_设置主驾吹脚_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109046(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Foot)

    @allure.title("联动_Auto模式_设置副驾吹面_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109101(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Face)

    @allure.title("联动_Auto模式_设置副驾吹脚_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109107(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)

    @allure.title("联动_Auto模式_设置主驾吹窗_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109248(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Defrst)

    @allure.title("联动_Auto模式_设置后排吹面_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109361(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)
        
    @allure.title("联动_Auto模式_打开内循环_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108988(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("联动_Auto模式_打开内循环_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109060(self):
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.FaceDefrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("联动_Auto模式_打开外循环_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109254(self):
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.FaceDefrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("联动_Auto模式_打开Auto循环_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109369(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)

    @allure.title("联动_Auto模式_打开外循环_Auto模式 ")
    @pytest.mark.full
    def test_climate_soa_caseid_109007(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)

    @allure.title("联动_Auto模式_温度同步设置_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108712(self):
        self.climate_precondition()
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_sync_sts(sts=True)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)
        
    @allure.title("联动_Auto模式_关闭总开关_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109135(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.DrvrLeft,sts=AirVentReqSts.On)

    @allure.title("联动_Auto模式_关闭总开关_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108493(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.DrvrLeft,sts=AirVentReqSts.On)
        
    @allure.title("联动_Auto模式_关闭总开关_温度同步")
    @pytest.mark.full
    def test_climate_soa_caseid_109024(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=24.0)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.get_climate_sys_sts(temp_dri=24.0,temp_pass=24.0,temp_sec_row=24.0)

    @allure.title("联动_OFF_打开总开关_温度同步")
    @pytest.mark.full
    def test_climate_soa_caseid_108989(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_sync_sts(sts=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=24.0)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.get_climate_sync_mode(sts=True)
        self.soa.get_climate_sys_sts(temp_dri=24.0,temp_pass=24.0,temp_sec_row=24.0)

    @allure.title("联动_OFF_打开总开关_温度不同步")
    @pytest.mark.full
    def test_climate_soa_caseid_108775(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_sync_sts(sts=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=25.0)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.get_climate_sync_mode(sts=False)
        self.soa.get_climate_sys_sts(temp_dri=23.0,temp_pass=24.0,temp_sec_row=25.0)

    @allure.title("联动_OFF_打开后排开关_温度同步")
    @pytest.mark.full
    def test_climate_soa_caseid_108931(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_sync_sts(sts=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=24.0)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.get_climate_sync_mode(sts=True)
        self.soa.get_climate_sys_sts(temp_dri=24.0,temp_pass=24.0,temp_sec_row=24.0)

    @allure.title("联动_Auto模式_温度同步设置_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109173(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_sync_sts(sts=True)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)
    
    @allure.title("联动_前除霜除雾_温度同步设置_AC状态_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_115767(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_前除霜除雾_温度同步设置_AC状态_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_118697(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_sync_sts(sts=True)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_前除霜除雾_温度同步设置_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118699(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_sync_sts(sts=True)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_前除霜除雾_温度同步设置_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118698(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_sync_sts(sts=True)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_前除霜除雾_温度同步设置_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115984(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)        
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_sync_sts(sts=True)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("联动_前除霜除雾_温度同步设置_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_118700(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_sync_sts(sts=False)       
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_sync_sts(sts=True)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)

    @allure.title("联动_Auto模式_打开Auto循环_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109198(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_前除霜除雾_AC设置_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115793(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_ac_sts(sts=False,timeout=0.5)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("联动_前除霜除雾_AC设置_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_115904(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_ac_sts(sts=False,timeout=0.5)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Rear,speed=SeatVenSpeed.Off)

    @allure.title("联动_前除霜除雾_AC设置_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115782(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_ac_sts(sts=False,timeout=0.5)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)

    @allure.title("联动_前除霜除雾_AC设置_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115892(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_ac_sts(sts=False,timeout=0.5)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_前除霜除雾_AC设置_AC状态")
    @pytest.mark.full
    def test_climate_soa_caseid_113218(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_ac_sts(sts=False,timeout=0.5)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_前除霜除雾_调节风量_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_114624(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3,timeout=0.5)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)
        
    @allure.title("联动_前除霜除雾_调节风量_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_115769(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5,timeout=0.5)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)

    # @allure.title("联动_前除霜除雾_AC设置_Auto模式")
    # @pytest.mark.full
    # def test_climate_soa_caseid_115782(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
    #     self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
    #     self.soa.hmi_set_climate_defrost_mode(mode=True)
    #     self.soa.hmi_set_climate_ac_sts(sts=False)
    #     self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5,timeout=0.5)
    #     self.soa.get_climate_sys_sts(power_sts_first_row=False,power_sts_sec_row=False)

    @allure.title("联动_前除霜除雾_关闭总开关_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115795(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_ac_sts(sts=False)

    @allure.title("联动_前除霜除雾_调节风量_AC状态_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_115820(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5,timeout=0.5)
        self.soa.hmi_set_climate_ac_sts(sts=True)

    @allure.title("联动_前除霜除雾_打开内循环_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115822(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_前除霜除雾_调节风量_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_115810(self):
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)

    @allure.title("联动_前除霜除雾_打开外循环_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118534(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_前除霜除雾_打开外循环_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_116002(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_AC设置_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_109298(self):
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_ac_sts(sts=True,timeout=0.5)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)

    @allure.title("联动_OFF_打开外循环_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115424(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)

    @allure.title("联动_OFF_打开Auto循环_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115167(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_打开Auto循环_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_108825(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_打开内循环_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115186(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("联动_OFF_打开内循环_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115180(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("联动_OFF_打开内循环_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115165(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_打开总开关_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115192(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)

    @allure.title("联动_OFF_打开总开关_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_108940(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("联动_OFF_打开外循环_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115423(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)

    @allure.title("联动_OFF_打开外循环_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115424(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_前除霜除雾_AC设置_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118450(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_前除霜除雾_AC设置_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118451(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_AC设置_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_109151(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_AC设置_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115475(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)

    @allure.title("联动_OFF_AC设置_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115474(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("联动_前除霜除雾_打开内循环_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118530(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_前除霜除雾_打开内循环_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118529(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_前除霜除雾_打开外循环_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118533(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_打开外循环_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_109354(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)

    @allure.title("联动_OFF_打开内循环_AC状态")
    @pytest.mark.full
    def test_climate_soa_caseid_109324(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True,timeout=0.5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)

    @allure.title("联动_OFF_打开外循环_AC状态")
    @pytest.mark.full
    def test_climate_soa_caseid_108733(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True,timeout=0.5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)

    @allure.title("联动_OFF_打开内循环_电源状态")
    @pytest.mark.full
    def test_climate_soa_caseid_109324(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.get_climate_sys_sts(power_sts_first_row=False,power_sts_sec_row=False)

    @allure.title("联动_OFF_打开外循环_电源状态")
    @pytest.mark.full
    def test_climate_soa_caseid_108796(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.get_climate_sys_sts(power_sts_first_row=False,power_sts_sec_row=False)


    @allure.title("联动_OFF_打开Auto循环_电源状态")
    @pytest.mark.full
    def test_climate_soa_caseid_109043(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.get_climate_sys_sts(power_sts_first_row=False,power_sts_sec_row=False)

    @allure.title("联动_前除霜除雾_打开主驾吹窗_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115774(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.get_climate_mode(mode=ClimateMode.kDefrost)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.soa.get_climate_mode(mode=ClimateMode.kDefrost)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Defrst)

    @allure.title("联动_前除霜除雾_打开内循环_AC状态_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_116028(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_前除霜除雾_香氛功能请求_AC状态_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_115799(self):
        self.soa.hmi_set_climate_ac_sts(sts=False,timeout=0.5)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_手动模式_设置主驾吹窗_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115669(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Defrst)

    @allure.title("联动_手动模式_设置副驾吹面_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115682(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Defrst)

    @allure.title("联动_手动模式_打开Auto循环_温度同步")
    @pytest.mark.full
    def test_climate_soa_caseid_1991944(self):
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft, value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight, value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow, value=24.0)
        self.soa.hmi_set_climate_sync_sts(sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.get_climate_sync_mode(sts=True)
        self.soa.get_climate_sys_sts(temp_dri=24.0,temp_pass=24.0,temp_sec_row=24.0)
        
    @allure.title("联动_手动模式_设置后排吹脚_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115691(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Foot)

    @allure.title("联动_手动模式_设置主驾吹面_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115736(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Face)

    @allure.title("联动_手动模式_设置主驾吹脚_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115696(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Foot)

    @allure.title("联动_手动模式_设置后排吹面_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115706(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("联动_手动模式_设置副驾吹脚_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115708(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)

    @allure.title("联动_手动模式_打开内循环_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_108091(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality,timeout=0.5)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation,timeout=0.5)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("联动_手动模式_打开Auto循环_风量")
    @pytest.mark.smoke
    def test_climate_soa_caseid_116175(self):
        self.climate_precondition()
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality,timeout=0.5)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)
        
    @allure.title("联动_手动模式_打开内循环_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_108092(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation,timeout=0.5)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)

    @allure.title("联动_手动模式_关闭总开关_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_108095(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation,timeout=0.5)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("联动_手动模式_后出风口风向调节_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108095(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation,timeout=0.5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("联动_手动模式_打开后排开关_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_108106(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality,timeout=0.5)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_打开总开关_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115180(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_打开后排开关_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109171(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_OFF_打开总开关_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109160(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_OFF_打开Auto循环_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115179(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_Auto模式_设置副驾吹面_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109309(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_手动模式_设置副驾吹面_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115723(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftRight,on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.DrvrRight, sts=AirVentReqSts.On)

    @allure.title("联动_手动模式_设置后排吹面_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115722(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.DrvrRight, sts=AirVentReqSts.On)

    @allure.title("联动_手动模式_设置后排吹脚_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115719(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.SecondRow,on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.SecRow, sts=AirVentReqSts.On)

    @allure.title("联动_手动模式_设置主驾吹脚_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115714(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_手动模式_打开后排开关_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_116091(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_前除霜除雾_关闭总开关_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115842(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.SecondRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.SecRow, sts=AirVentReqSts.On)

    @allure.title("联动_手动模式_打开后排开关_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_116084(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_手动模式_关闭后排开关_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115829(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.AllZone,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3,time_wait=0.5)

    @allure.title("联动_手动模式_关闭后排开关_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_116016(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.AllZone,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_前除霜除雾_关闭主驾吹窗_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115816(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftRight,on=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.DrvrRight, sts=AirVentReqSts.On)

    @allure.title("联动_手动模式_设置主驾吹窗_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115738(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowRightRight,on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.AllZone,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.PassRight, sts=AirVentReqSts.On)

    @allure.title("联动_手动模式_设置主驾吹脚_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115728(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowRightLeft,on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.AllZone,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.PassLeft, sts=AirVentReqSts.On)

    @allure.title("联动_手动模式_设置后排吹面_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115727(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.AllZone,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)        
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("联动_Auto模式_设置后排吹面_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108734(self):
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)   
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.FaceDefrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("联动_手动模式_设置后排吹脚_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115724(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.AllZone,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)        
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Foot)

    @allure.title("联动_手动模式_设置副驾吹脚_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115693(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.AllZone,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)        
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)

    @allure.title("联动_手动模式_设置主驾吹面_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115726(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.AllZone,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)        
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Face)


    @allure.title("联动_手动模式_设置主驾吹窗_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115668(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.AllZone,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)        
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Defrst)


    @allure.title("联动_手动模式_设置副驾吹面_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115688(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.AllZone,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)        
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Face)

    @allure.title("联动_前除霜除雾_设置主驾吹面_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115813(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On)

    @allure.title("联动_前除霜除雾_关闭主驾吹窗_AC状态_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_115831(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=False,timeout=0.5)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_前除霜除雾_关闭主驾吹窗_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118554(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_前除霜除雾_关闭主驾吹窗_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118555(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)
        
    @allure.title("联动_前除霜除雾_调节主驾温度_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_115834(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.5)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Rear,speed=SeatVenSpeed.Off)

    @allure.title("联动_前除霜除雾_关闭主驾吹窗_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115835(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3,time_wait=0.5)

    @allure.title("联动_前除霜除雾_调节副驾温度_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_115838(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=23.0)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=23.5)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Rear,speed=SeatVenSpeed.Off)
    
    @allure.title("联动_前除霜除雾_香氛功能请求_Auto模式_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_115855(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)

    @allure.title("联动_前除霜除雾_打开主驾吹窗_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_1991947(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)
        
    @allure.title("联动_前除霜除雾_香氛功能请求_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118819(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_前除霜除雾_打开Auto循环_AC状态_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_115886(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_前除霜除雾_打开外循环_AC状态_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_115900(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_前除霜除雾_打开内循环_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115902(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_前除霜除雾_打开Auto循环_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115792(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_前除霜除雾_打开外循环_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_116018(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_前除霜除雾_打开内循环_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_115920(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Rear,speed=SeatVenSpeed.Off)

    @allure.title("联动_前除霜除雾_打开主驾吹面_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115922(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)

    @allure.title("联动_前除霜除雾_温度同步设置_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_115985(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Rear,speed=SeatVenSpeed.Off)

    @allure.title("联动_前除霜除雾_打开内循环_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115773(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On)

    @allure.title("联动_前除霜除雾_打开外循环_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115794(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.SecondRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.SecRow, sts=AirVentReqSts.On)

    @allure.title("联动_前除霜除雾_温度同步设置_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115883(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_sync_sts(sts=True)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_前除霜除雾_香氛功能请求_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115841(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowRightRight,on=isOn.On)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.PassRight, sts=AirVentReqSts.On)

    @allure.title("联动_前除霜除雾_调节主驾温度_AC状态_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_115992(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.5)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_前除霜除雾_香氛功能请求_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_115994(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Rear,speed=SeatVenSpeed.Off)

    @allure.title("联动_前除霜除雾_调节副驾温度_AC状态_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_115997(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=23.0)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=23.5)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_前除霜除雾_打开副驾吹面_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_116010(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)

    @allure.title("联动_前除霜除雾_打开副驾吹面_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115999(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_手动模式_设置主驾吹面_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115664(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowRightRight,on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.PassRight, sts=AirVentReqSts.On)

    @allure.title("联动_前除霜除雾_打开副驾吹脚_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115950(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_手动模式_设置副驾吹脚_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115665(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowRightLeft,on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.PassLeft, sts=AirVentReqSts.On)

    @allure.title("联动_前除霜除雾_打开后排吹面_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115854(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.SecondRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.SecRow, sts=AirVentReqSts.On)

    @allure.title("联动_前除霜除雾_打开后排吹脚_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115784(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowRightRight,on=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.PassRight, sts=AirVentReqSts.On)

    @allure.title("联动_前除霜除雾_打开后排开关_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115980(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_前除霜除雾_打开Auto模式_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115957(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_前除霜除雾_打开Auto模式_风量")
    @pytest.mark.smoke
    def test_climate_soa_caseid_115897(self):
        self.climate_precondition()
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutNorm)

    @allure.title("联动_前除霜除雾_打开主驾吹脚_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_116012(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)

    @allure.title("联动_前除霜除雾_打开主驾吹脚_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115916(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_手动模式_打开外循环_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_116010(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)

    @allure.title("联动_手动模式_打开前除霜除雾_电源状态")
    @pytest.mark.full
    def test_climate_soa_caseid_116079(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Rear,speed=SeatVenSpeed.Off)

    @allure.title("联动_OFF_打开前除霜除雾_电源状态")
    @pytest.mark.full
    def test_climate_soa_caseid_108761(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)

    @allure.title("联动_手动模式_打开外循环_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_116010(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)

    @allure.title("联动_手动模式_打开Auto循环_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_116085(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)

    @allure.title("联动_手动模式_打开Auto循环_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_116086(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.DrvrLeft,sts=AirVentReqSts.On)

    @allure.title("联动_手动模式_打开前除霜除雾_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108195(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.DrvrLeft,sts=AirVentReqSts.On)

    @allure.title("联动_手动模式_设置主驾吹窗_内外循环模式_内模式")
    @pytest.mark.full
    def test_climate_soa_caseid_119025(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("联动_手动模式_设置副驾吹面_内外循环模式_内模式")
    @pytest.mark.full
    def test_climate_soa_caseid_119029(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)
                        
    @allure.title("联动_手动模式_打开内循环_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_116075(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.DrvrLeft,sts=AirVentReqSts.On)

    @allure.title("联动_手动模式_打开外循环_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108093(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.DrvrLeft,sts=AirVentReqSts.On)

    @allure.title("联动_前除霜除雾_打开主驾吹脚_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_116012(self):
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)

    @allure.title("联动_手动模式_后出风口开关_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_116102(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.AllZone,on=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.SecondRowLeftLeft,on=isOn.Off)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("联动_手动模式_前出风口开关_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108196(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.Off)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.DrvrLeft,sts=AirVentReqSts.Off)
        
    @allure.title("联动_手动模式_后出风口开关_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_116071(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.SecondRowLeftLeft,on=isOn.Off)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.SecRow,sts=AirVentReqSts.Off)

    @allure.title("联动_前除霜除雾_打开主驾吹脚_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_116012(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)

    @allure.title("联动_手动模式_调节风量_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_116104(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)

    @allure.title("联动_手动模式_前出风口开关_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_116126(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.Off)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)

    @allure.title("联动_手动模式_调节副驾温度_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_116148(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("联动_手动模式_调节主驾温度_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108187(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=24.0)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_手动模式_调节副驾温度_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_116149(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrRight, sts=AirVentReqSts.On
        )

    @allure.title("联动_手动模式_温度同步设置_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_116152(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_sync_sts(sts=True)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)


    @allure.title("联动_手动模式_关闭总开关_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_116163(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)

    @allure.title("联动_前除霜除雾_关闭主驾吹窗_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_118556(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)
        self.soa.get_climate_sys_sts(power_sts_sec_row=False)

    @allure.title("联动_前除霜除雾_关闭主驾吹窗_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_115919(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Rear,speed=SeatVenSpeed.Off)

    @allure.title("联动_前除霜除雾_打开后排开关_Auto模式_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_118580(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.All,speed=SeatVenSpeed.LvlAutNorm)

    @allure.title("联动_前除霜除雾_打开Auto循环_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115864(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_前除霜除雾_调节风量_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115772(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftRight, on=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.DrvrRight, sts=AirVentReqSts.On)

    @allure.title("联动_前除霜除雾_打开Auto循环_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_118544(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)

    @allure.title("联动_前除霜除雾_打开外循环_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_118535(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)

    @allure.title("联动_前除霜除雾_打开外循环_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_115945(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)

    @allure.title("联动_前除霜除雾_打开内循环_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115932(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("联动_前除霜除雾_打开Auto循环_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115791(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("联动_前除霜除雾_打开内循环_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_118531(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)

    @allure.title("联动_前除霜除雾_调节主驾温度_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_118712(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Rear,speed=SeatVenSpeed.Off)

    @allure.title("联动_前除霜除雾_调节主驾温度_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115909(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_前除霜除雾_调节副驾温度_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_118716(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=23.0)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Rear,speed=SeatVenSpeed.Off)

    @allure.title("联动_OFF_调节副驾温度_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_115435(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("联动_OFF_调节后排温度_电源状态")
    @pytest.mark.full
    def test_climate_soa_caseid_109211(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=25.0)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("联动_OFF_调节主驾温度_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_109305(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("联动_OFF_调节主驾温度_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_115431(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)

    @allure.title("联动_OFF_调节副驾温度_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_108713(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)

    @allure.title("联动_前除霜除雾_香氛功能请求_Auto模式_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_118818(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)

        
    @allure.title("联动_前除霜除雾_香氛功能请求_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_118821(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Rear,speed=SeatVenSpeed.Off)


    @allure.title("联动_Auto模式_打开前除霜除雾_电源状态_后排开启 ")
    @pytest.mark.full
    def test_climate_soa_caseid_118940(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=23.0)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)
   
    @allure.title("联动_Auto模式_关闭Auto模式_Auto模式")
    @pytest.mark.smoke
    def test_climate_soa_caseid_109379(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoNormal)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)

    @allure.title("联动_Auto模式_关闭Auto模式_AC状态")
    @pytest.mark.smoke
    def test_climate_soa_caseid_108941(self):
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)
        self.soa.hmi_set_acinhibit_sts(sts=True)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)

    @allure.title("联动_Auto模式_打开前除霜除雾_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108461(self):
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        sleep(1)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Defrst)
        
    @allure.title("联动_前除霜除雾_调节主驾温度_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115931(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_前除霜除雾_调节后排温度_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_116008(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=23.0)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_OFF_打开后排吹脚_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109264(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Foot)

    @allure.title("联动_OFF_打开主驾吹脚_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108929(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Foot)

    @allure.title("联动_OFF_打开后排吹面_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108946(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)


    @allure.title("联动_前除霜除雾_调节后排温度_Auto模式_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_118718(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)

    @allure.title("联动_OFF_打开Auto模式_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109250(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutNorm)

    @allure.title("联动_OFF_打开Auto模式_温度同步")
    @pytest.mark.full
    def test_climate_soa_caseid_109127(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_sync_sts(sts=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=24.0)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_sync_mode(sts=True)
        self.soa.get_climate_sys_sts(temp_dri=24.0,temp_pass=24.0,temp_sec_row=24.0)

    @allure.title("联动_OFF_打开主驾吹窗_温度同步")
    @pytest.mark.full
    def test_climate_soa_caseid_109084(self):
        self.soa.hmi_set_climate_sync_sts(sts=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=24.0)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.soa.get_climate_sync_mode(sts=True)
        self.soa.get_climate_sys_sts(temp_dri=24.0,temp_pass=24.0,temp_sec_row=24.0)

    @allure.title("联动_OFF_打开副驾吹脚_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109204(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)

    @allure.title("联动_OFF_香氛功能请求_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109202(self):
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel2,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.DrvrLeft,sts=AirVentReqSts.On)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.DrvrRight,sts=AirVentReqSts.On)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.PassLeft,sts=AirVentReqSts.On)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.PassRight,sts=AirVentReqSts.On)

    @allure.title("联动_OFF_打开后排吹脚_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_109382(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("联动_OFF_打开主驾吹脚_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_108833(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)

    @allure.title("联动_OFF_打开主驾吹窗_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_109161(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)

    @allure.title("联动_OFF_打开总开关_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_109162(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)

    @allure.title("联动_OFF_打开副驾吹脚_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_109272(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)

    @allure.title("联动_OFF_香氛功能请求_温度不同步")
    @pytest.mark.full
    def test_climate_soa_caseid_108809(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=25.0)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.soa.get_climate_sync_mode(sts=False)
        self.soa.get_climate_sys_sts(temp_dri=23.0,temp_pass=24.0,temp_sec_row=25.0)

    @allure.title("联动_OFF_香氛功能请求_AC状态")
    @pytest.mark.full
    def test_climate_soa_caseid_108805(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)

    @allure.title("联动_OFF_打开Auto模式_温度不同步")
    @pytest.mark.full
    def test_climate_soa_caseid_109059(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=25.0)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_sync_mode(sts=False)
        self.soa.get_climate_sys_sts(temp_dri=23.0,temp_pass=24.0,temp_sec_row=25.0)

    @allure.title("联动_OFF_AC设置_温度不同步")
    @pytest.mark.full
    def test_climate_soa_caseid_108903(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.get_climate_sync_mode(sts=False)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=25.0)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.soa.get_climate_sync_mode(sts=False)

    @allure.title("联动_OFF_打开内循环_温度不同步")
    @pytest.mark.full
    def test_climate_soa_caseid_109119(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=25.0)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.get_climate_sync_mode(sts=False)
        self.soa.get_climate_sys_sts(temp_dri=23.0,temp_pass=24.0,temp_sec_row=25.0)

    @allure.title("联动_OFF_打开Auto循环_温度不同步")
    @pytest.mark.full
    def test_climate_soa_caseid_108756(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=25.0)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.get_climate_sync_mode(sts=False)
        self.soa.get_climate_sys_sts(temp_dri=23.0,temp_pass=24.0,temp_sec_row=25.0)

    @allure.title("联动_OFF_打开外循环_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109196(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)

    @allure.title("联动_OFF_调节主驾温度_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_108909(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone, sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft, value=23.0)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)

    @allure.title("联动_OFF_调节副驾温度_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_109380(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone, sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight, value=24.0)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)
        
    @allure.title("联动_OFF_打开内循环_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_109371(self):
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)    
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.All,speed=SeatVenSpeed.Off)

    @allure.title("联动_OFF_打开Auto循环_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_109008(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)    
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.All,speed=SeatVenSpeed.Off)

    @allure.title("联动_OFF_打开外循环_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_109031(self):
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)    
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.All,speed=SeatVenSpeed.Off)

    @allure.title("联动_OFF_打开总开关_Auto模式_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_109193(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)

    @allure.title("联动_OFF_打开后排开关_Auto模式_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_108926(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)

    @allure.title("联动_OFF_调节后排温度_Auto模式_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_109153(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow, value=25.0)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)
    
    @allure.title("联动_OFF_调节后排温度_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115438(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow, value=25.0)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_调节主驾温度_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115430(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft, value=25.0)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_调节主驾温度_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_109002(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft, value=25.0)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("联动_OFF_调节主驾温度_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115429(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft, value=25.0)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)

    @allure.title("联动_OFF_调节主驾温度_AC状态")
    @pytest.mark.full
    def test_climate_soa_caseid_109148(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.5)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_OFF_调节副驾温度_AC状态")
    @pytest.mark.full
    def test_climate_soa_caseid_108840(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=23.0)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=23.5)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_OFF_调节副驾温度_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115434(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight, value=24.0)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_调节副驾温度_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115433(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight, value=24.0)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)

    @allure.title("联动_OFF_调节副驾温度_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_109094(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight, value=25.0)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("联动_OFF_调节后排温度_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115437(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow, value=25.0)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)

    @allure.title("联动_OFF_调节后排温度_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_109000(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow, value=25.0)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("联动_OFF_打开内循环_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109122(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("联动_OFF_打开Auto循环_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109273(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)
        
    @allure.title("联动_OFF_AC设置_Auto模式_Auto关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_108981(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("联动_OFF_调节风量_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115427(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_调节风量_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_109267(self):
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)

    @allure.title("联动_OFF_调节风量_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115426(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)

    @allure.title("联动_OFF_打开后排开关_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_108896(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("联动_OFF_打开后排开关_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115159(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)

    @allure.title("联动_OFF_打开后排开关_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115157(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_调节风量_AC状态_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_115425(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_OFF_打开总开关_AC状态_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_115176(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_OFF_AC设置_AC状态")
    @pytest.mark.full
    def test_climate_soa_caseid_108874(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=False,timeout=0.5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_ac_sts(sts=True,timeout=0.5)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_OFF_打开总开关_AC状态_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_109296(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)

    @allure.title("联动_OFF_打开后排开关_AC状态_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_109366(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=25.0)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.get_climate_sync_mode(sts=False)
        self.soa.get_climate_sys_sts(temp_dri=23.0,temp_pass=24.0,temp_sec_row=25.0)

    @allure.title("联动_OFF_打开后排开关_AC状态_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_115176(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_OFF_AC设置_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_115473(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("联动_OFF_打开总开关_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_115163(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("联动_OFF_打开总开关_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_109260(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("联动_OFF_调节风量_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_115428(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("联动_OFF_打开后排吹面_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108946(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("联动_OFF_打开主驾吹面_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108843(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Face)

    @allure.title("联动_OFF_打开后排吹面_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109147(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_OFF_打开副驾吹面_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108943(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_OFF_打开主驾吹面_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108886(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_OFF_香氛功能请求_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108932(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("联动_OFF_香氛功能请求_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_108865(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.All,speed=SeatVenSpeed.Off)

    @allure.title("联动_OFF_香氛功能请求_电源状态")
    @pytest.mark.full
    def test_climate_soa_caseid_108711(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.soa.get_climate_sys_sts(power_sts_first_row=False,power_sts_sec_row=False)

    @allure.title("联动_OFF_香氛功能请求_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_114606(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)

    @allure.title("联动_OFF_香氛功能请求_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_108912(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("联动_OFF_香氛功能请求_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_114605(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_打开主驾吹脚_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108929(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Foot)

    @allure.title("联动_OFF_打开后排开关_Auto模式_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_108926(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("联动_OFF_调节风量_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108894(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)

    @allure.title("联动_OFF_打开前除霜除雾_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108957(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow, on=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_OFF_打开主驾吹面_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108843(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Face)

    @allure.title("	联动_OFF_调节风量_温度不同步")
    @pytest.mark.full
    def test_climate_soa_caseid_109097(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=25.0)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.get_climate_sync_mode(sts=False)

    @allure.title("联动_OFF_打开主驾吹窗_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_109096(self):
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)

    @allure.title("联动_OFF_打开副驾吹脚_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_109071(self):
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)

    @allure.title("联动_OFF_打开主驾吹窗_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_109022(self):
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)

    @allure.title("联动_OFF_打开主驾吹面_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_108829(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)

    @allure.title("联动_OFF_打开副驾吹面_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_109100(self):
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)

    @allure.title("联动_OFF_打开副驾吹面_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108819(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Face)

    @allure.title("联动_OFF_打开主驾吹窗_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108770(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Defrst)

    @allure.title("联动_OFF_打开主驾吹脚_温度不同步")
    @pytest.mark.full
    def test_climate_soa_caseid_108709(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=25.0)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.soa.get_climate_sync_mode(sts=False)

    @allure.title("联动_OFF_打开副驾吹脚_温度不同步")
    @pytest.mark.full
    def test_climate_soa_caseid_109266(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=25.0)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.get_climate_sync_mode(sts=False)

    @allure.title("联动_OFF_打开后排吹脚_温度不同步")
    @pytest.mark.full
    def test_climate_soa_caseid_108726(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=25.0)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.soa.get_climate_sync_mode(sts=False)

    @allure.title("联动_OFF_打开主驾吹窗_温度不同步")
    @pytest.mark.full
    def test_climate_soa_caseid_109375(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=25.0)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.soa.get_climate_sync_mode(sts=False)

    @allure.title("联动_OFF_打开主驾吹面_温度不同步")
    @pytest.mark.full
    def test_climate_soa_caseid_109210(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=25.0)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.soa.get_climate_sync_mode(sts=False)

    @allure.title("联动_OFF_打开后排吹面_温度不同步")
    @pytest.mark.full
    def test_climate_soa_caseid_108838(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=25.0)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.get_climate_sync_mode(sts=False)

    @allure.title("联动_OFF_打开副驾吹面_温度不同步")
    @pytest.mark.full
    def test_climate_soa_caseid_108995(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=25.0)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.get_climate_sync_mode(sts=False)

    @allure.title("联动_OFF_调节主驾温度_Auto模式_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_108719(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft, value=23.0)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Face)

    @allure.title("联动_OFF_调节主驾温度_温度同步")
    @pytest.mark.full
    def test_climate_soa_caseid_109291(self):
        self.soa.hmi_set_climate_sync_sts(sts=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft, value=24.0)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft, value=24.5)
        self.soa.get_climate_sync_mode(sts=True)
        self.soa.get_climate_sys_sts(temp_dri=24.5,temp_pass=24.5,temp_sec_row=24.5)

    @allure.title("联动_OFF_调节副驾温度_温度同步")
    @pytest.mark.full
    def test_climate_soa_caseid_108773(self):
        self.soa.hmi_set_climate_sync_sts(sts=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft, value=24.0)
        self.soa.get_climate_sys_sts(temp_dri=24.0,temp_pass=24.0,temp_sec_row=24.0)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight, value=24.5)
        self.soa.get_climate_sync_mode(sts=False)
        self.soa.get_climate_sys_sts(temp_dri=24.0,temp_pass=24.5,temp_sec_row=24.0)

    @allure.title("联动_OFF_打开外循环_温度同步")
    @pytest.mark.full
    def test_climate_soa_caseid_108828(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_sync_sts(sts=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft, value=24.0)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.get_climate_sync_mode(sts=True)
        self.soa.get_climate_sys_sts(temp_dri=24.0,temp_pass=24.0,temp_sec_row=24.0)

    @allure.title("联动_OFF_打开Auto循环_温度同步")
    @pytest.mark.full
    def test_climate_soa_caseid_108779(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_sync_sts(sts=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft, value=24.0)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.get_climate_sync_mode(sts=True)
        self.soa.get_climate_sys_sts(temp_dri=24.0,temp_pass=24.0,temp_sec_row=24.0)

    @allure.title("联动_OFF_调节主驾温度_温度不同步")
    @pytest.mark.full
    def test_climate_soa_caseid_109209(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft, value=23.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight, value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow, value=25.0)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft, value=23.5)
        self.soa.get_climate_sync_mode(sts=False)

    @allure.title("联动_OFF_调节副驾温度_Auto模式_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_108667(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight, value=23.0)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Face)

    @allure.title("联动_OFF_调节后排温度_温度不同步")
    @pytest.mark.full
    def test_climate_soa_caseid_108875(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft, value=23.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight, value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow, value=25.0)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow, value=23.5)
        self.soa.get_climate_sync_mode(sts=False)

    @allure.title("联动_Auto模式_温度同步设置_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109088(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_Auto模式_设置主驾吹面_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109087(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_Auto模式_设置后排吹面_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108980(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_Auto模式_打开前除霜除雾_风量")
    @pytest.mark.smoke
    def test_climate_soa_caseid_108508(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)

    @allure.title("联动_Auto模式_打开前除霜除雾_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108429(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)

    @allure.title("联动_手动模式_打开前除霜除雾_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_116109(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        sleep(1)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("联动_手动模式_打开前除霜除雾_风量")
    @pytest.mark.smoke
    def test_climate_soa_caseid_108193(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Rear,speed=SeatVenSpeed.Off)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)#记忆
        
    @allure.title("联动_手动模式_打开前除霜除雾_Auto模式")
    @pytest.mark.smoke
    def test_climate_soa_caseid_108192(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.get_climate_mode(mode=ClimateMode.kDefrost)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)

    @allure.title("联动_手动模式_打开Auto模式_Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108175(self):
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutNorm)

    @allure.title("联动_前除霜除雾_关闭前除霜除雾_温度同步")
    @pytest.mark.sanity
    def test_climate_soa_caseid_115939(self):
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=24.0)
        self.soa.hmi_set_climate_sync_sts(sts=True)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_defrost_mode(mode=False)
        self.soa.get_climate_sys_sts(temp_dri=24.0,temp_pass=24.0,temp_sec_row=24.0)

    @allure.title("联动_前除霜除雾_关闭前除霜除雾_温度不同步")
    @pytest.mark.sanity
    def test_climate_soa_caseid_115915(self):
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=25.0)
        self.soa.hmi_set_climate_sync_sts(sts=False)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_defrost_mode(mode=False)
        self.soa.get_climate_sys_sts(temp_dri=23.0,temp_pass=24.0,temp_sec_row=25.0)

    @allure.title("联动_前除霜除雾_关闭前除霜除雾_香氛")
    @pytest.mark.full
    def test_climate_soa_caseid_115901(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_defrost_mode(mode=False)
        self.bus_comm.check_climate_fragrance_req(taste=FragChannel.Channel1,level=FragLevel.Level2,ch1_ratio=100.0)

    @allure.title("联动_前除霜除雾_关闭前除霜除雾_AC状态_AC关闭")
    @pytest.mark.smoke
    def test_climate_soa_caseid_115806(self):
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_defrost_mode(mode=False)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)
                
    @allure.title("联动_前除霜除雾_关闭前除霜除雾_Auto模式_关闭")
    @pytest.mark.smoke
    def test_climate_soa_caseid_116029(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)

    @allure.title("联动_前除霜除雾_关闭前除霜除雾_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_115888(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_defrost_mode(mode=False)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    # @allure.title("联动_OFF_AC设置_Auto模式_Auto开启")
    # @pytest.mark.full
    # def test_climate_soa_caseid_108858(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
    #     self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
    #     self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=24.0)
    #     self.soa.hmi_set_climate_sync_sts(sts=True)
    #     self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
    #     self.soa.hmi_set_climate_ac_sts(sts=True)
    #     self.soa.get_climate_sync_mode(zone=ClimateZone,sts=True)
    #     self.soa.get_climate_sys_sts(temp_dri=24.0,temp_pass=24.0,temp_sec_row=24.0)

    @allure.title("联动_前除霜除雾_关闭前除霜除雾_Auto模式_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_115456(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.get_climate_mode(mode=ClimateMode.kDefrost)
        self.soa.hmi_set_climate_defrost_mode(mode=False)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Auto)

    @allure.title("联动_OFF_打开后排开关_Auto模式_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_115161(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True,is_wind_mode_auto_sec_row=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)

    @allure.title("联动_OFF_打开总开关_Auto模式_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_115154(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True,is_wind_mode_auto_sec_row=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)

    @allure.title("联动_OFF_打开总开关_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_109300(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)

    @allure.title("联动_OFF_打开后排开关_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_108978(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)

    @allure.title("联动_OFF_调节后排温度_Auto模式_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_115436(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=23.0)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,temp_sec_row=23.0,is_wind_mode_auto_sec_row=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_climate_temp_req(zone=ClimateZone.SecondRow,value=23.0)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)

    @allure.title("联动_OFF_调节主驾温度_Auto模式_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_115420(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,temp_dri=23.0,is_wind_mode_auto_sec_row=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_climate_temp_req(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Auto)
        
    @allure.title("联动_OFF_调节副驾温度_Auto模式_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_115432(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=23.0)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,temp_pass=23.0,is_wind_mode_auto_pass=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_climate_temp_req(zone=ClimateZone.FirstRowRight,value=23.0)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Auto)

    @allure.title("联动_OFF_AC设置_Auto模式_Auto开启")
    @pytest.mark.full
    def test_climate_soa_caseid_115476(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,ac_sts=True,is_wind_mode_auto_dri=True)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Auto)
                
    @allure.title("联动_前除霜除雾_调节副驾温度_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_116021(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=23.0)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("联动_前除霜除雾_调节副驾温度_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118715(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=23.0)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_前除霜除雾_调节副驾温度_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118714(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=23.0)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_前除霜除雾_调节副驾温度_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115844(self):
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("联动_OFF_打开前除霜除雾_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109203(self):
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("联动_OFF_打开后排吹脚_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109397(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.FaceDefrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Foot)

    @allure.title("联动_OFF_打开主驾吹窗_AC状态_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_114633(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_OFF_打开主驾吹窗_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_114631(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)

    @allure.title("联动_OFF_打开主驾吹窗_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_108851(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("联动_OFF_打开主驾吹窗_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_114604(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("联动_OFF_打开主驾吹脚_AC状态_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_114633(self):
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_OFF_打开主驾吹脚_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_114634(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)

    @allure.title("联动_OFF_打开主驾吹脚_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_108947(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("	联动_OFF_打开后排吹脚_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_108992(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("联动_OFF_打开主驾吹面_AC状态_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_114637(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_OFF_打开主驾吹面_AC状态_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_109288(self):
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)

    @allure.title("联动_OFF_打开后排吹面_AC状态_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_108744(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)

    @allure.title("联动_OFF_打开副驾吹面_AC状态_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_108852(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)

    @allure.title("联动_OFF_打开主驾吹窗_AC状态_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_108972(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)

    @allure.title("联动_OFF_打开主驾吹脚_AC状态_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_109041(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)

    @allure.title("	联动_OFF_打开副驾吹脚_AC状态_关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_108913(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)

    @allure.title("联动_OFF_打开主驾吹面_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_114638(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)

    @allure.title("联动_OFF_打开副驾吹脚_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_109010(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("联动_OFF_打开主驾吹面_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_114639(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_打开主驾吹面_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_114640(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("联动_OFF_打开主驾吹面_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_108800(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)

    @allure.title("联动_OFF_打开副驾吹面_电源状态_后排关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_108762(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)

    @allure.title("联动_OFF_打开副驾吹脚_AC状态_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_114641(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_OFF_打开副驾吹脚_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_114642(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)

    @allure.title("联动_OFF_打开副驾吹脚_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_114643(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_打开副驾吹脚_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_114648(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("联动_OFF_打开副驾吹面_AC状态_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_114645(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_OFF_打开副驾吹面_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_114646(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)

    @allure.title("联动_OFF_打开副驾吹面_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_114647(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_打开副驾吹面_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_114644(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("联动_OFF_打开主驾吹脚_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_109156(self):
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)

    @allure.title("联动_OFF_打开后排吹脚_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_109284(self):
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)

    @allure.title("联动_OFF_打开后排吹脚_AC状态_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_114649(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_OFF_打开后排吹脚_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_114650(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)

    @allure.title("联动_OFF_打开后排吹脚_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_114651(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_打开后排吹脚_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_114652(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("联动_OFF_打开后排吹面_AC状态_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_114653(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_OFF_打开后排吹面_内外循环模式_外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_114654(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)

    @allure.title("联动_OFF_打开后排吹面_内外循环模式_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_108731(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("联动_OFF_打开后排吹面_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_114655(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_打开后排吹面_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_114656(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("联动_OFF_打开后排吹面_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_109340(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("联动_前除霜除雾_香氛功能请求_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_115850(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("联动_前除霜除雾_调节风量_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_116023(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("bgm首次上电开启空调")
    @pytest.mark.full
    def test_climate_soa_caseid_1984586(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.io.io_reset_bgm()
        time.sleep(15)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan3)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan3)
    
    @allure.title("OFF进入前除霜除雾_制冷限制")
    @pytest.mark.full
    def test_climate_soa_caseid_115170(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_acinhibit_sts(sts=True)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)

    @allure.title("OFF_制冷限制")
    @pytest.mark.full
    def test_climate_soa_caseid_114717(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)
        self.soa.hmi_set_acinhibit_sts(sts=True)
        sleep(0.1)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)

    @allure.title("OFF进入Auto模式_制冷限制")
    @pytest.mark.full
    def test_climate_soa_caseid_115174(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)
        self.soa.hmi_set_acinhibit_sts(sts=False)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)
        self.soa.hmi_set_acinhibit_sts(sts=True)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)

    @allure.title("手动模式进入Auto模式_制冷限制")
    @pytest.mark.full
    def test_climate_soa_caseid_115189(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(
            zone=ClimateZone.AllZone, speed=WindSpeed.kLvlMan5
        )
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)
        self.soa.hmi_set_acinhibit_sts(sts=True)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)

    @allure.title("Manual→Auto_制冷限制")
    @pytest.mark.full
    def test_climate_soa_caseid_1988703(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)
        self.soa.hmi_set_acinhibit_sts(sts=True)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)
        self.soa.hmi_set_acinhibit_sts(sts=False)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)
        
    @allure.title("Manual→前除霜除雾_制冷限制")
    @pytest.mark.full
    def test_climate_soa_caseid_1988704(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.get_climate_mode(mode=ClimateMode.kDefrost)
        self.soa.hmi_set_acinhibit_sts(sts=True)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)
        self.soa.hmi_set_acinhibit_sts(sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kDefrost)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)
                
    @allure.title("手动模式进入前除霜除雾_制冷限制")
    @pytest.mark.full
    def test_climate_soa_caseid_115191(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windspeed(
            zone=ClimateZone.AllZone, speed=WindSpeed.kLvlMan5
        )
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)
        self.soa.hmi_set_acinhibit_sts(sts=True)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)

    @allure.title("联动_OFF_打开主驾吹脚_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_114636(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("联动_OFF_打开主驾吹面_电源状态_后排开启")
    @pytest.mark.full
    def test_climate_soa_caseid_114604(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("联动_OFF_打开主驾吹脚_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_114635(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_打开主驾吹脚_AC状态_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_114633(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_OFF_打开主驾吹面_AC状态_开启")
    @pytest.mark.full
    def test_climate_soa_caseid_114630(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("联动_OFF_打开主驾吹面_内外循环模式_Auto循环")
    @pytest.mark.full
    def test_climate_soa_caseid_114632(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("联动_OFF_设置后排吹脚_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109076(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_OFF_打开副驾吹脚_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108878(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_OFF_打开主驾吹脚_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108928(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_OFF_打开主驾吹窗_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108984(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("联动_前除霜除雾_关闭前除霜除雾_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_115781(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowRightLeft, on=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_defrost_mode(mode=False)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.PassLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_Auto模式_调节副驾温度_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109411(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftRight, on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=23.0)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.DrvrRight, sts=AirVentReqSts.On)

    @allure.title("联动_Auto模式_设置后排吹脚_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109277(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On)

    @allure.title("联动_Auto模式_设置后排吹脚_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109219(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On)

    @allure.title("联动_Auto模式_设置主驾吹脚_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109222(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On)

    @allure.title("联动_Auto模式_设置主驾吹窗_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109149(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On)
        
    @allure.title("联动_Auto模式_设置副驾吹脚_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109283(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_vent_req(pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On)

    @allure.title("联动_Auto模式_设置主驾吹面_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109280(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.FootFace)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)        
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Face)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Face)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.FootFace)

    @allure.title("联动_Auto模式_关闭总开关_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108939(self):
        self.climate_precondition()
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.notwindmode()

    @allure.title("联动_Auto模式_关闭后排开关_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108499(self):
        self.climate_precondition()
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow,sts=isOn.Off)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)
        
    @allure.title("联动_Auto模式_关闭Auto模式_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108684(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeft, on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False,timeout=0.5)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_Auto模式_设置副驾吹面_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_109233(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)
        
    @allure.title("联动_Auto模式_前出风口开关_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108475(self):
        self.climate_precondition()
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft, on=isOn.Off)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)
        
    @allure.title("联动_Auto模式_后出风口开关_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108521(self):
        self.climate_precondition()
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.AllZone, on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)
        
    @allure.title("联动_Auto模式_设置主驾吹脚_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109093(self):
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("联动_Auto模式_设置副驾吹脚_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108674(self):
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.FaceDefrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)
        
    @allure.title("联动_Auto模式_设置主驾吹窗_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108871(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Defrst)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("联动_Auto模式_调节主驾温度_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108748(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=23.0)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)

    @allure.title("联动_Auto模式_调节副驾温度_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108657(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=23.0)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)

    @allure.title("联动_Auto模式_调节后排温度_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109238(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=23.0)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)

    @allure.title("联动_Auto模式_调节风量_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_109404(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)
        
    @allure.title("联动_Auto模式_香氛功能请求_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_108467(self):
        self.climate_precondition()
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True,timeout=0.5)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Auto)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Auto)
        
    @allure.title("联动_Auto模式_打开Auto循环_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109388(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft, on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_Auto模式_香氛功能请求_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108519(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft, on=isOn.On)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100.0,level=FragLevel.Level2)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel3,ratio=100.0,level=FragLevel.Level2)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("联动_Auto模式_前出风口开关_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108456(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow,on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft,on=isOn.Off)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.Off
        )

    @allure.title("联动_Auto模式_打开前除霜除雾_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108516(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft, on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )
        
    @allure.title("联动_Auto模式_关闭后排开关_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108512(self):
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft, on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )
          
    @allure.title("联动_Auto模式_打开内循环_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_108791(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow, on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    @allure.title("	联动_Auto模式_打开外循环_电动出风口设置")
    @pytest.mark.full
    def test_climate_soa_caseid_109263(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRow, on=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_climate_vent_req(
            pos=AirVentReqPos.DrvrLeft, sts=AirVentReqSts.On
        )

    # @allure.title("联动_OFF_打开Auto循环_Auto模式")
    # @pytest.mark.full
    # def test_climate_soa_caseid_109273(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
    #     self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
    #     self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
    #     self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
    #     self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
    #     self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.Aut)

    @allure.title("泛化记忆_Auto模式_主驾吹风模式记忆当前值_关闭Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_118071(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Front,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_后排吹风模式记忆当前值_关闭Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_118097(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Rear,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_副驾吹风模式记忆当前值_关闭Auto模式")
    @pytest.mark.full
    def test_climate_soa_caseid_118084(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Front,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_主驾吹风模式记忆当前值_关闭AC")
    @pytest.mark.full
    def test_climate_soa_caseid_118070(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Front,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_副驾吹风模式记忆当前值_关闭AC")
    @pytest.mark.full
    def test_climate_soa_caseid_118083(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Front,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_后排吹风模式记忆当前值_关闭AC")
    @pytest.mark.full
    def test_climate_soa_caseid_118096(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Rear,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_副驾吹风模式记忆当前值_关闭后排空调")
    @pytest.mark.full
    def test_climate_soa_caseid_118082(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow,sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Front,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_主驾吹风模式记忆当前值_关闭后排空调")
    @pytest.mark.full
    def test_climate_soa_caseid_118069(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow,sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Front,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_后排吹风模式记忆当前值_关闭后排空调")
    @pytest.mark.full
    def test_climate_soa_caseid_118095(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow,sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Rear,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_主驾吹风模式记忆当前值_调节风量")
    @pytest.mark.full
    def test_climate_soa_caseid_118068(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(
            zone=ClimateZone.AllZone, speed=WindSpeed.kLvlMan5
        )
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Front,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_副驾吹风模式记忆当前值_调节风量")
    @pytest.mark.full
    def test_climate_soa_caseid_118081(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(
            zone=ClimateZone.AllZone, speed=WindSpeed.kLvlMan5
        )
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Front,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_后排吹风模式记忆当前值_调节风量")
    @pytest.mark.full
    def test_climate_soa_caseid_118094(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(
            zone=ClimateZone.AllZone, speed=WindSpeed.kLvlMan5
        )
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Rear,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_后排吹风模式记忆当前值_打开外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118093(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Rear,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_后排吹风模式记忆当前值_打开内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118092(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Rear,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_副驾吹风模式记忆当前值_打开外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118080(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Front,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_副驾吹风模式记忆当前值_打开内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118079(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Front,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_主驾吹风模式记忆当前值_打开外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118067(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Front,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_主驾吹风模式记忆当前值_打开内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118066(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.FaceDefrst)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Front,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_后排吹风模式记忆当前值_设置副驾吹面")
    @pytest.mark.full
    def test_climate_soa_caseid_118091(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Rear,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_副驾吹风模式记忆当前值_设置后排吹面")
    @pytest.mark.full
    def test_climate_soa_caseid_118078(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Front,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_副驾吹风模式记忆当前值_设置后排吹脚")
    @pytest.mark.full
    def test_climate_soa_caseid_118077(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Front,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_后排吹风模式记忆当前值_设置副驾吹脚")
    @pytest.mark.full
    def test_climate_soa_caseid_118090(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Rear,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_后排吹风模式记忆当前值_设置主驾吹面")
    @pytest.mark.full
    def test_climate_soa_caseid_118089(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Rear,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_后排吹风模式记忆当前值_设置主驾吹脚")
    @pytest.mark.full
    def test_climate_soa_caseid_118088(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Rear,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_副驾吹风模式记忆当前值_设置主驾吹脚")
    @pytest.mark.full
    def test_climate_soa_caseid_118076(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Rear,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_副驾吹风模式记忆当前值_设置主驾吹脚")
    @pytest.mark.full
    def test_climate_soa_caseid_118075(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Rear,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_副驾吹风模式记忆当前值_设置主驾吹窗")
    @pytest.mark.full
    def test_climate_soa_caseid_118074(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Rear,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_后排吹风模式记忆当前值_设置主驾吹窗")
    @pytest.mark.full
    def test_climate_soa_caseid_118087(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Rear,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_后排开关记忆OFF_关闭后排空调")
    @pytest.mark.full
    def test_climate_soa_caseid_118007(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoNormal)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)
        
    @allure.title("泛化记忆_Auto模式_后排开关记忆ON_关闭AC")
    @pytest.mark.full
    def test_climate_soa_caseid_118011(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("泛化记忆_Auto模式_后排开关记忆ON_打开内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118012(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("泛化记忆_Auto模式_后排开关记忆ON_打开外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118013(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)
                             
    @allure.title("泛化记忆_Auto模式_主驾吹风模式记忆当前值_设置副驾吹面")
    @pytest.mark.full
    def test_climate_soa_caseid_118062(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Rear,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_主驾吹风模式记忆当前值_设置后排吹面")
    @pytest.mark.full
    def test_climate_soa_caseid_118065(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Front,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_主驾吹风模式记忆当前值_设置后排吹脚")
    @pytest.mark.full
    def test_climate_soa_caseid_118064(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Front,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_主驾吹风模式记忆当前值_设置副驾吹脚")
    @pytest.mark.full
    def test_climate_soa_caseid_118063(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatVenPos.Rear,mode=AirWindMode.Auto)

    @allure.title("泛化记忆_Auto模式_循环模式记忆Auto_设置副驾吹面")
    @pytest.mark.full
    def test_climate_soa_caseid_118045(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("泛化记忆_Auto模式_循环模式记忆Auto_设置后排吹脚")
    @pytest.mark.full
    def test_climate_soa_caseid_118044(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("泛化记忆_Auto模式_循环模式记忆Auto_设置副驾吹脚")
    @pytest.mark.full
    def test_climate_soa_caseid_118043(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("泛化记忆_Auto模式_循环模式记忆Auto_设置主驾吹窗")
    @pytest.mark.full
    def test_climate_soa_caseid_118042(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("泛化记忆_Auto模式_循环模式记忆Auto_设置主驾吹脚")
    @pytest.mark.full
    def test_climate_soa_caseid_118041(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("泛化记忆_Auto模式_循环模式记忆Auto_设置主驾吹面")
    @pytest.mark.full
    def test_climate_soa_caseid_118040(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("泛化记忆_Auto模式_循环模式记忆Auto_设置主驾吹窗")
    @pytest.mark.full
    def test_climate_soa_caseid_118039(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)

    @allure.title("泛化记忆_Auto模式_循环模式记忆Auto_关闭后排空调")
    @pytest.mark.full
    def test_climate_soa_caseid_118036(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("泛化记忆_Auto模式_循环模式记忆设置值_打开外循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118034(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)
        
    @allure.title("泛化记忆_Auto模式_循环模式记忆设置值_内循环")
    @pytest.mark.full
    def test_climate_soa_caseid_118033(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("泛化记忆_Auto模式_风量记忆设置值_调节风量")
    @pytest.mark.full
    def test_climate_soa_caseid_118020(self):
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoNormal)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutNorm)
        
    @allure.title("Auto_Off_Auto联动开空调_风量记忆")
    @pytest.mark.full
    def test_caseid_1988804(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoPlus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlus)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoNormal)#置位

    @allure.title("Manual_Off_On_Manual风量记忆")
    @pytest.mark.full
    def test_caseid_1988803(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.On)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)

    @allure.title("Auto_Off_On_Auto风量记忆")
    @pytest.mark.full
    def test_caseid_1988802(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoPlusPlus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.On)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoNormal)#置位

    @allure.title("Auto_外循环_打开Auto_风量记忆")
    @pytest.mark.full
    def test_caseid_1988801(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoPlusPlus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoNormal)#置位

    @allure.title("Auto_内循环_打开Auto_风量记忆")
    @pytest.mark.full
    def test_caseid_1988800(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoPlusPlus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoNormal)#置位

    @allure.title("Auto_关闭AC_打开Auto_风量记忆")
    @pytest.mark.full
    def test_caseid_1988799(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoPlusPlus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoNormal)#置位

    @allure.title("Auto_关闭Auto_打开Auto_风量记忆")
    @pytest.mark.full
    def test_caseid_1988798(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoPlusPlus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoNormal)#置位
                                               
    @allure.title("泛化记忆_Auto模式_后排开关记忆ON_设置副驾吹面")
    @pytest.mark.full
    def test_climate_soa_caseid_118019(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        sleep(3)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)

    @allure.title("泛化记忆_Auto模式_后排开关记忆ON_设置副驾吹脚")
    @pytest.mark.full
    def test_climate_soa_caseid_118018(self):
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoNormal)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)
        
    @allure.title("泛化记忆_Auto模式_后排开关记忆ON_设置主驾吹窗")
    @pytest.mark.full
    def test_climate_soa_caseid_118017(self):
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoNormal)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)
        
    @allure.title("泛化记忆_Auto模式_后排开关记忆ON_设置主驾吹面")
    @pytest.mark.full
    def test_climate_soa_caseid_118016(self):
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoNormal)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5) 
        
    @allure.title("泛化记忆_Auto模式_后排开关记忆ON_设置主驾吹脚")
    @pytest.mark.full
    def test_climate_soa_caseid_118015(self):
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoNormal)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)

    @allure.title("泛化记忆_Auto模式_后排开关记忆ON_设置后排吹脚")
    @pytest.mark.full
    def test_climate_soa_caseid_118009(self):
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoNormal)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)
                                                                             
    @allure.title("除霜除雾_后排关闭_开门_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_1985161(self):
        self.climate_precondition()
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.io.set_five_door_sts(sts=Door.close)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan4)

    # @allure.title("除霜除雾_开门_风量")
    # @pytest.mark.full
    # def test_climate_soa_caseid_1985160(self):
    #     self.climate_precondition()
    #     self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
    #     self.soa.hmi_set_climate_defrost_mode(mode=True)
    #     self.io.set_five_door_sts(sts=Door.close)
    #     self.io.set_door(Pass=Door.open)
    #     self.bus_comm.check_door_open_mode_req(pos=DoorPos.Pass,mode=isOn.On)
    #     self.soa.get_climate_mode(mode=ClimateMode.kDefrost)
    #     self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan4)
    #     self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Rear,speed=SeatVenSpeed.Off)
        
                
    @allure.title("手动模式_后排关闭_开门_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_1985157(self):
        self.climate_precondition()
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.io.set_five_door_sts(sts=Door.close)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan4)


    # @allure.title("手动模式_开门_风量")
    # @pytest.mark.full
    # def test_climate_soa_caseid_1985156(self):
    #     self.climate_precondition()
    #     self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
    #     self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
    #     self.soa.hmi_set_climate_ac_sts(sts=False)
    #     self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
    #     self.soa.get_climate_mode(mode=ClimateMode.kManual)
    #     self.io.set_five_door_sts(sts=Door.close)
    #     self.io.set_door(Drvr=Door.open)
    #     self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.All,speed=SeatVenSpeed.LvlMan4)
        
    @allure.title("自动模式_后排关闭_开门_风量")
    @pytest.mark.full
    def test_climate_soa_caseid_1985159(self):
        self.climate_precondition()
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.Off)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.io.set_five_door_sts(sts=Door.close)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutMinusMinus)
        self.io.set_five_door_sts(sts=Door.close)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutNorm)
        
    # @allure.title("自动模式_开门_风量")
    # @pytest.mark.full
    # def test_climate_soa_caseid_1985158(self):
    #     self.climate_precondition()
    #     self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
    #     self.io.set_five_door_sts(sts=Door.close)
    #     self.io.set_door(Drvr=Door.open)
    #     self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.All,speed=SeatVenSpeed.LvlAutMinusMinus)
    #     self.io.set_five_door_sts(sts=Door.close)
    #     self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutNorm)
        
    @allure.title("除霜除雾_开门_风量改变")
    @pytest.mark.full
    def test_climate_soa_caseid_1985269(self):
        self.climate_precondition()
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.io.set_five_door_sts(sts=Door.close)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan4)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)
        
    @allure.title("手动模式_开门_风量改变")
    @pytest.mark.full
    def test_climate_soa_caseid_1985271(self):
        self.climate_precondition()
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.io.set_five_door_sts(sts=Door.close)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.All,speed=SeatVenSpeed.LvlMan4)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.All,speed=SeatVenSpeed.LvlMan5)
        
    @allure.title("自动模式_开门_风量改变")
    @pytest.mark.full
    def test_climate_soa_caseid_1985270(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow, sts=isOn.On)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.io.set_five_door_sts(sts=Door.close)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutMinusMinus)
        self.io.set_five_door_sts(sts=Door.close)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutNorm)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutNorm)
        
    @allure.title("内循环_10min倒计时打断")
    @pytest.mark.full
    def test_climate_soa_caseid_1984824(self):
        self.climate_precondition()
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.ecm_precondition()
        self.bus_comm.set_singal("bodycan", "CcmBodyFr21", "ResrvdSigForECM2", 85)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)
        self.bus_comm.set_singal("bodycan", "CcmBodyFr21", "ResrvdSigForECM2", 74)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("内循环_10min倒计时")
    @pytest.mark.full
    def test_climate_soa_caseid_1984823(self):
        self.climate_precondition()
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.ecm_precondition()
        self.bus_comm.set_singal("bodycan", "CcmBodyFr21", "ResrvdSigForECM2", 85)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)
        self.bus_comm.set_singal("bodycan", "CcmBodyFr21", "ResrvdSigForECM2", 74)
        sleep(600)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)
        
    @allure.title("内循环_湿度≥85_除霜除雾")
    @pytest.mark.full
    def test_climate_soa_caseid_1984822(self):
        self.climate_precondition()
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.ecm_precondition()
        self.bus_comm.set_singal("bodycan", "CcmBodyFr21", "ResrvdSigForECM2", 85)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)
        self.soa.hmi_set_climate_defrost_mode(mode=False)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)
        
    @allure.title("内循环_湿度≥85")
    @pytest.mark.full
    def test_climate_soa_caseid_1984821(self):
        self.climate_precondition()
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.ecm_precondition()
        self.bus_comm.set_singal("bodycan", "CcmBodyFr21", "ResrvdSigForECM2", 84)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)
        self.bus_comm.set_singal("bodycan", "CcmBodyFr21", "ResrvdSigForECM2", 85)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)

    @allure.title("AUTO_调节风量10==>14")
    @pytest.mark.full
    def test_climate_soa_caseid_1985825(self):
        self.climate_precondition()
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoMinusMinus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutMinusMinus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoPlusPlus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoNormal)
        
    @allure.title("AUTO_调节风量14==>12")
    @pytest.mark.full
    def test_climate_soa_caseid_1985826(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoPlusPlus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoMinusMinus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutMinusMinus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoNormal)
        
    @allure.title("AUTO_调节风量12==>11_开门降风量")
    @pytest.mark.full
    def test_climate_soa_caseid_1988699(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoMinus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutMinus)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutMinusMinus)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutMinus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoNormal)

    @allure.title("AUTO_调节风量12==>11_开门降风量_手动调节关门")
    @pytest.mark.full
    def test_climate_soa_caseid_1988700(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoMinus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutMinus)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutMinusMinus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoPlusPlus)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoNormal)

    @allure.title("开门降风量_AUTO→除霜除雾")
    @pytest.mark.full
    def test_climate_soa_caseid_1988701(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoPlusPlus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.get_climate_mode(mode=ClimateMode.kDefrost)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan4)
        self.soa.hmi_set_climate_defrost_mode(mode=False)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.io.set_door(Drvr=Door.close)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoNormal)

    @allure.title("开门降风量_Manual→除霜除雾")
    @pytest.mark.full
    def test_climate_soa_caseid_1988702(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlMan5)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.get_climate_mode(mode=ClimateMode.kDefrost)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan4)
        self.soa.hmi_set_climate_defrost_mode(mode=False)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)
        self.io.set_door(Drvr=Door.close)
                                               
    @allure.title("手动_调节风量7==>13_不响应")
    @pytest.mark.full
    def test_climate_soa_caseid_1985830(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlMan7)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoPlus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan7)

    @allure.title("联动_前除霜除雾_关闭前除霜除雾_风量")
    @pytest.mark.smoke
    def test_climate_soa_caseid_115801(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan5)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.hmi_set_climate_defrost_mode(mode=False)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan5)

    @allure.title("出厂化设置_AC状态")
    @pytest.mark.smoke
    def test_climate_soa_caseid_109688(self):
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.soa.reset_soa_config()
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)

    @allure.title("开门降风量_开门后状态机切换不重新执行降风量")
    @pytest.mark.full
    def test_climate_soa_caseid_1991357(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)  
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan9)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoPlusPlus)
        self.io.set_five_door_sts(sts=Door.close)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutMinusMinus)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        self.io.set_five_door_sts(sts=Door.close)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoNormal)#置位
        
    @allure.title("休眠唤醒_后排吹风模式记忆")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994483(self):
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Foot)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Foot)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        sleep(10)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Foot)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        sleep(10)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)

    @allure.title("io重启_副驾吹风模式记忆")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994484(self):
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Face)
        sleep(1)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Face)
        sleep(1)
        self.io.io_reset_bgm()
        sleep(15)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Face)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowRight,mode=AirWindMode.Foot)
        sleep(1)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)
        sleep(1)
        self.io.io_reset_bgm()
        sleep(15)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Pass,mode=AirWindMode.Foot)
        
    @allure.title("诊断重启_主驾吹风模式记忆")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994485(self):
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Defrst)
        sleep(1)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Defrst)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Defrst)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.FirstRowLeft,mode=AirWindMode.Face)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Face)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.Drive,mode=AirWindMode.Face)
        
    @allure.title("休眠唤醒_风量记忆10")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1988811(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoMinusMinus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutMinusMinus)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutMinusMinus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoNormal)#置位

    @allure.title("io重启_风量记忆12")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1988808(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoNormal)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutNorm)
        sleep(3)
        self.io.io_reset_bgm()
        sleep(15)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        sleep(3)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutNorm)

    @allure.title("io重启_风量记忆13_Off")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1988809(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoPlus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlus)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.Off)
        sleep(3)
        self.io.io_reset_bgm()
        sleep(15)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.On)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlus)
        
    @allure.title("诊断重启_风量记忆10")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1988805(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoMinusMinus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutMinusMinus)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutMinusMinus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoNormal)#置位
                        
    @allure.title("休眠唤醒_风量记忆14_Manual")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1988812(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoPlusPlus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan9)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoNormal)#置位

    @allure.title("诊断重启_风量记忆14_Manual")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1988807(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoPlusPlus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan9)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoNormal)#置位

    @allure.title("io重启_风量记忆14_Manual")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1988810(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoPlusPlus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan9)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        sleep(3)
        self.io.io_reset_bgm()
        sleep(15)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoNormal)#置位
        
    @allure.title("休眠唤醒_风量记忆11_Off")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1988813(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoMinus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutMinus)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.Off)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.On)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutMinus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoNormal)#置位

    @allure.title("诊断重启_风量记忆11_Off")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1988806(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoMinus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutMinus)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.Off)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.On)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutMinus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoNormal)#置位
                
    @allure.title("休眠唤醒_循环记忆")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994486(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.AutoWithAirQuality)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.AutWithAirQly)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)

    @allure.title("io重启_循环记忆")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994487(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)
        sleep(3)
        self.io.io_reset_bgm()
        sleep(15)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)
        sleep(3)
        self.io.io_reset_bgm()
        sleep(15)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)
        
    @allure.title("诊断重启_循环记忆")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994488(self):
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.ExternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.OscircFull)
        self.soa.hmi_set_climate_cycle_mode(mode=CycleMode.InternalCirculation)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.bus_comm.check_climate_cycle_req(sts=ClimateCycleReq.RecircFull)
                
    @allure.title("休眠唤醒_AC记忆")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994489(self):
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)        

    @allure.title("io重启_AC记忆")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994490(self):
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)
        sleep(3)
        self.io.io_reset_bgm()
        sleep(15)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)
        sleep(3)
        self.io.io_reset_bgm()
        sleep(15)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)  
        
    @allure.title("诊断重启_AC记忆")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994491(self):
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Auto)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.bus_comm.check_climate_ac_sts(sts=CoolgReq.Off)  
               
    @allure.title("休眠唤醒_Auto记忆")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994492(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        
    @allure.title("io重启_Auto记忆")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994493(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        sleep(3)
        self.io.io_reset_bgm()
        sleep(15)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        sleep(3)
        self.io.io_reset_bgm()
        sleep(15)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
                
    @allure.title("诊断重启_Auto记忆")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994494(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
               
    @allure.title("休眠唤醒_后排空调开关记忆")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994495(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow,sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_sec_row=True)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        sleep(10)
        self.soa.get_climate_sys_sts(power_sts_sec_row=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow,sts=isOn.Off)
        self.soa.get_climate_sys_sts(power_sts_sec_row=False)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        sleep(10)
        self.soa.get_climate_sys_sts(power_sts_sec_row=False)
        
    @allure.title("io重启_后排空调开关记忆")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994496(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow,sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_sec_row=True)
        sleep(3)
        self.io.io_reset_bgm()
        sleep(15)
        self.soa.get_climate_sys_sts(power_sts_sec_row=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow,sts=isOn.Off)
        self.soa.get_climate_sys_sts(power_sts_sec_row=False)
        sleep(3)
        self.io.io_reset_bgm()
        sleep(15)
        self.soa.get_climate_sys_sts(power_sts_sec_row=False)
        
    @allure.title("诊断重启_后排空调开关记忆")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994497(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow,sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_sec_row=True)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        sleep(10)
        self.soa.get_climate_sys_sts(power_sts_sec_row=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow,sts=isOn.Off)
        self.soa.get_climate_sys_sts(power_sts_sec_row=False)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        sleep(10)
        self.soa.get_climate_sys_sts(power_sts_sec_row=False)
                       
    @allure.title("休眠唤醒_空调总开关")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994480(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        sleep(3)
        self.soa.get_climate_sys_sts(power_sts_first_row=False)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        sleep(10)
        self.soa.get_climate_sys_sts(power_sts_first_row=False)

    @allure.title("io重启_空调总开关")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994481(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)
        sleep(3)
        self.io.io_reset_bgm()
        sleep(15)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.soa.get_climate_sys_sts(power_sts_first_row=False)
        sleep(3)
        self.io.io_reset_bgm()
        sleep(15)
        self.soa.get_climate_sys_sts(power_sts_first_row=False)
                               
    @allure.title("诊断重启_空调总开关")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994482(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        sleep(10)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.soa.get_climate_sys_sts(power_sts_first_row=False)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        sleep(10)
        self.soa.get_climate_sys_sts(power_sts_first_row=False)

    @allure.title("ECO节能设置")
    @pytest.mark.smoke
    def test_caseid_115537(self):
        self.soa.set_eco_sts(sts=True)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)
        self.soa.set_eco_sts(sts=False)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)
        
# v2.2CR：
    @allure.title("诊断重启_Off_关闭ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995749(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        self.soa.set_eco_sts(sts=False)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)
        
    @allure.title("休眠唤醒_Off_关闭ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995721(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        self.soa.set_eco_sts(sts=False)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        sleep(5)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)
        
    @allure.title("io重启_Off_关闭ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995727(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        self.soa.set_eco_sts(sts=False)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)
        self.io.io_reset_bgm()
        sleep(15)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)
        
    @allure.title("诊断重启_Off_打开ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995751(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        self.soa.set_eco_sts(sts=True)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        sleep(8)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)
        
    @allure.title("休眠唤醒_Off_打开ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995720(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        self.soa.set_eco_sts(sts=True)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        sleep(8)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        sleep(1)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)
        
    @allure.title("io重启_Off_打开ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995726(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        self.soa.set_eco_sts(sts=True)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)
        self.io.io_reset_bgm()
        sleep(15)
        self.soa.get_climate_mode(mode=ClimateMode.kOFF)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)

    @allure.title("诊断重启_Auto_打开ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995748(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.set_eco_sts(sts=True)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)
        
    @allure.title("休眠唤醒_Auto_打开ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995716(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.set_eco_sts(sts=True)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)    
            
    @allure.title("io重启_Auto_打开ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995722(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.set_eco_sts(sts=True)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)
        self.io.io_reset_bgm()
        sleep(15)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On) 

    @allure.title("诊断重启_Auto_关闭ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995752(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.set_eco_sts(sts=False)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)
        
    @allure.title("休眠唤醒_Auto_关闭ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995718(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.set_eco_sts(sts=False)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)    
            
    @allure.title("io重启_Auto_关闭ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995724(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.set_eco_sts(sts=False)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)
        self.io.io_reset_bgm()
        sleep(15)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off) 

    @allure.title("诊断重启_Manual_关闭ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995750(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.set_eco_sts(sts=False)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)
        
    @allure.title("休眠唤醒_Manual_关闭ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995719(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.set_eco_sts(sts=False)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)
        
    @allure.title("io重启_Manual_关闭ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995725(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.set_eco_sts(sts=False)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)
        self.io.io_reset_bgm()
        sleep(15)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.Off)

    @allure.title("诊断重启_Manual_打开ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995753(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.set_eco_sts(sts=True)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)
        
    @allure.title("休眠唤醒_Manual_打开ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995717(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.set_eco_sts(sts=True)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)
        
    @allure.title("io重启_Manual_打开ECO")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995723(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.set_eco_sts(sts=True)
        sleep(3)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)
        self.io.io_reset_bgm()
        sleep(15)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.bus_comm.check_climate_eco_sts(sts=OnOff.On)
                              
    @allure.title("AUTO_调节风量14==>9_不响应")
    @pytest.mark.full
    def test_climate_soa_caseid_1988797(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoPlusPlus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlMan9)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoNormal)

    @allure.title("Auto_调节风量12==>10")
    @pytest.mark.full
    def test_climate_soa_caseid_1988796(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoNormal)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutNorm)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoMinusMinus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutMinusMinus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoNormal)
    
    @allure.title("Auto_调节风量14==>10")
    @pytest.mark.full
    def test_climate_soa_caseid_1988795(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoPlusPlus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutPlusPlus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoMinusMinus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutMinusMinus)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoNormal)
        
    @allure.title("前除霜除雾_调节风量5==>12_不响应")
    @pytest.mark.full
    def test_climate_soa_caseid_1995754(self):
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.get_climate_mode(mode=ClimateMode.kDefrost)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow, speed=WindSpeed.kLvlAutoPlus)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        
    @allure.title("前除霜除雾→手动_后排空调开启_吹风模式")
    @pytest.mark.full
    def test_climate_soa_caseid_1995758(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windmode_sts(zone=ClimateZone.SecondRow,mode=AirWindMode.Face)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.get_climate_mode(mode=ClimateMode.kDefrost)
        self.soa.hmi_set_climate_defrost_mode(mode=False)
        self.bus_comm.check_climate_windmode_sts_req(pos=SeatPos.RearAll,mode=AirWindMode.Face)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("Off_设置后排温度_后排开关")
    @pytest.mark.full
    def test_climate_soa_caseid_1995755(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.soa.get_climate_sys_sts(power_sts_first_row=False,power_sts_sec_row=False)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=25.0)
        self.bus_comm.check_climate_temp_req(zone=ClimateZone.SecondRow,value=25.0)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)
        self.io.io_reset_bgm()
        sleep(15)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)
        
    @allure.title("Auto_设置后排温度_后排开关")
    @pytest.mark.full
    def test_climate_soa_caseid_1995756(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow,sts=isOn.Off)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=26.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=25.0)
        self.bus_comm.check_climate_temp_req(zone=ClimateZone.SecondRow,value=25.0)
        self.bus_comm.check_climate_temp_req(zone=ClimateZone.FirstRowLeft,value=24.0)
        self.bus_comm.check_climate_temp_req(zone=ClimateZone.FirstRowRight,value=26.0)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)
        self.sd_tester.hard_reset(TA.BGM_SOC)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("Manual_设置后排温度_后排开关")
    @pytest.mark.full
    def test_climate_soa_caseid_1995757(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow,sts=isOn.Off)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowLeft,value=24.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRowRight,value=26.0)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=25.0)
        sleep(1)
        self.bus_comm.check_climate_temp_req(zone=ClimateZone.SecondRow,value=25.0)
        self.bus_comm.check_climate_temp_req(zone=ClimateZone.FirstRowLeft,value=24.0)
        self.bus_comm.check_climate_temp_req(zone=ClimateZone.FirstRowRight,value=26.0)
        sleep(1)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)
        sleep(1)
        self.io.io_reset_bgm()
        sleep(15)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)
                      
    @allure.title("前除霜除雾→自动_后排空调开启_后排温度调节")
    @pytest.mark.full
    def test_climate_soa_caseid_1995759(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone,sts=isOn.Off)
        self.soa.get_climate_sys_sts(power_sts_first_row=False,power_sts_sec_row=False)
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.SecondRow,value=24.0)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.get_climate_mode(mode=ClimateMode.kDefrost)
        self.soa.hmi_set_climate_defrost_mode(mode=False)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.bus_comm.check_climate_temp_req(zone=ClimateZone.SecondRow,value=24.0)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)
        
    @allure.title("前除霜除雾→手动_后排空调关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_1996186(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow,sts=isOn.Off)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.get_climate_mode(mode=ClimateMode.kDefrost)
        self.soa.hmi_set_climate_defrost_mode(mode=False)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)
        
    @allure.title("除霜除雾&Manual_不响应Auto风量")
    @pytest.mark.full
    def test_climate_soa_caseid_1996184(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoNormal)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlAutNorm)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.get_climate_mode(mode=ClimateMode.kDefrost)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoNormal)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan9)
        self.soa.hmi_set_climate_defrost_mode(mode=False)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=False)
        self.soa.get_climate_mode(mode=ClimateMode.kManual)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlMan6)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan6)
        self.soa.hmi_set_climate_windspeed(zone=ClimateZone.FirstRow,speed=WindSpeed.kLvlAutoNormal)
        self.bus_comm.check_windspeed_sts_req(pos=SeatVenPos.Front,speed=SeatVenSpeed.LvlMan6)    
        
    @allure.title("打开Auto退出除霜除雾_后排空调关闭")
    @pytest.mark.full
    def test_climate_soa_caseid_1996187(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow,sts=isOn.Off)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.get_climate_mode(mode=ClimateMode.kDefrost)
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=True)

    @allure.title("关闭前除霜除雾_打开Auto_后排空调联动开启")
    @pytest.mark.full
    def test_climate_soa_caseid_1996185(self):
        self.soa.hmi_set_climate_auto_mode(zone=ClimateZone.AllZone,sts=True)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.SecondRow,sts=isOn.Off)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.soa.get_climate_mode(mode=ClimateMode.kDefrost)
        self.soa.hmi_set_climate_defrost_mode(mode=False)
        self.soa.get_climate_mode(mode=ClimateMode.kAuto)
        self.soa.get_climate_sys_sts(power_sts_first_row=True,power_sts_sec_row=False)
        
    @allure.title("前摄像头加热_Normal_Convenience")
    @pytest.mark.full
    def test_climate_soa_caseid_1983450(self):
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_HmiDefrstMaxReq(sts=OnOff.On)
        self.soa.hmi_set_climate_defrost_mode(mode=False)
        self.bus_comm.check_HmiDefrstMaxReq(sts=OnOff.Off)
        
    @allure.title("前摄像头加热_Normal_Driving")
    @pytest.mark.full
    def test_climate_soa_caseid_1991560(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_HmiDefrstMaxReq(sts=OnOff.On)
        self.soa.hmi_set_climate_defrost_mode(mode=False)
        self.bus_comm.check_HmiDefrstMaxReq(sts=OnOff.Off)
        
    @allure.title("前摄像头不加热_Normal_Inactive")
    @pytest.mark.full
    def test_climate_soa_caseid_1991826(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_HmiDefrstMaxReq(sts=OnOff.Off)
        self.soa.hmi_set_climate_defrost_mode(mode=False)
        self.bus_comm.check_HmiDefrstMaxReq(sts=OnOff.Off)
        
    @allure.title("前摄像头不加热_Normal_Abandone")
    @pytest.mark.full
    def test_climate_soa_caseid_1991826(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_HmiDefrstMaxReq(sts=OnOff.Off)
        self.soa.hmi_set_climate_defrost_mode(mode=False)
        self.bus_comm.check_HmiDefrstMaxReq(sts=OnOff.Off)
        
    @allure.title("前摄像头加热30min停止_Normal_Convenience")
    @pytest.mark.longtime
    def test_climate_soa_caseid_1991564(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_HmiDefrstMaxReq(sts=OnOff.On)
        start_time=time.time()
        for i in range(30):
            if self.defrostoff():
                print(f"除霜在第{i}分钟内关闭")
                break
            if time.time()-start_time>1800:
                print("30分钟到")
                break
        else:
            print("除霜未在30mins内关闭")
            sleep(60)
        
    @allure.title("前摄像头加热30min停止_Normal_Driving")
    @pytest.mark.longtime
    def test_climate_soa_caseid_1991565(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.bus_comm.check_HmiDefrstMaxReq(sts=OnOff.On)
        start_time=time.time()
        for i in range(30):
            if self.defrostoff():
                print(f"除霜在第{i}分钟内关闭")
                break
            if time.time()-start_time>1800:
                print("30分钟到")
                break
        else:
            print("除霜未在30mins内关闭")
            sleep(60)
