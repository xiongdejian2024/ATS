#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_rvs.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/12/1 11:30
@Description: BGM RVS功能测试
"""

import os
import sys
import pytest
import allure
from time import sleep
import threading
import math

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.tsp.rvs_client import RvsClient
from signal_value_mapping import *

@allure.feature("BGM车云")
@allure.story("基础数据上报")
@pytest.mark.order_last
class TestRVS(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["ClimateControlService_client","CentralLockService_client","TailWingService_client","SteerWheelService_client","TyreService_client","ChargeLidService_client","OuterRearViewService_client","ShieldWindowService_client","VehicleModeService_client","VehicleSetStatusService_client"])
        sleep(3)
        self.vid = self.tb_config["vid"]
        self.rvs_client = RvsClient(vid=self.vid)
        logger.info("VID: {0}".format(self.vid))
        sleep(2)

    def before_each_func(self, ecu):
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_extral_light_button_to_defaul_sts()

    def after_each_func(self, ecu):
        self.bus_comm.set_singal("bodycan","CcmBodyFr29","FragCh1Id",0)
        self.bus_comm.set_singal("bodycan","CcmBodyFr29","FragCh2Id",0)
        self.bus_comm.set_singal("bodycan","CcmBodyFr29","FragCh3Id",0)
        self.bus_comm.set_singal("bodycan","CcmBodyFr25","FragCh1UseUpWrn",0)
        self.bus_comm.set_singal("bodycan","CcmBodyFr25","FragCh2UseUpWrn",0)
        self.bus_comm.set_singal("bodycan","CcmBodyFr25","FragCh3UseUpWrn",0)



    def after_class(self, ecu):
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        self.sd_tester.write_ccp({225: 7, 226: 7}) 
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass


    @pytest.mark.smoke
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196790?projectId=46',
        name='RVS Case 112825',
    )
    def test_drive_seat_heating_level_caseid_112825(self):
        drive_seat_heating_level = {
            "0": HeatVentiLvl.Off,
            "1": HeatVentiLvl.Level1,
            "2": HeatVentiLvl.Level2,
            "3": HeatVentiLvl.Level3,
        }
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft, level=HeatVentiLvl.Level3)
        sleep(0.5)
        for key in drive_seat_heating_level:
            self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft, level=drive_seat_heating_level[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus, keys=["seatHeatVent","id==0","status", "heatLevel"], target_value=int(key),sleep_time=15
            )

    @pytest.mark.smoke
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196788?projectId=46',
        name='RVS Case 112827',
    )
    def test_drive_seat_heating_status_caseid_112827(self):
        drive_seat_heating_status = {
            # "HeatVentNone": HeatVentiSts.None_,
            "HeatVentOn": HeatVentiSts.On,
            "HeatVentOff": HeatVentiSts.Off,
            "HeatVentError": HeatVentiSts.Error,
            "HeatVentFunctionLimit": HeatVentiSts.Functionallimit,
            "HeatVentEnergyLimit": HeatVentiSts.Energylimit,
        }
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        sleep(0.5)
        for key in drive_seat_heating_status:
            self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=drive_seat_heating_status[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus, keys=["seatHeatVent","id==0", "status", "heatWorkStatus"], target_value=getattr(HeatVentWorkStatusRvs, key).value
            )

    @pytest.mark.sanity
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196794?projectId=46',
        name='RVS Case 1918407',
    )
    def test_drive_seat_vent_level_caseid_1918407(self):
        " 触发条件问题"
        drive_seat_vent_level = {
            "0": HeatVentiLvl.Off,
            "1": HeatVentiLvl.Level1,
            "2": HeatVentiLvl.Level2,
            "3": HeatVentiLvl.Level3,
        }
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontLeft, level=HeatVentiLvl.Level3)
        sleep(1)
        for key in drive_seat_vent_level:
            self.bus_comm.set_seat_venti_level(pos=SeatId.FrontLeft, level=drive_seat_vent_level[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus, keys=["seatHeatVent","id==0","status", "ventLevel"], target_value=int(key)
            )

    @pytest.mark.sanity
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196792?projectId=46',
        name='RVS Case 112823',
    )
    def test_drive_seat_vent_status_caseid_112823(self):
        drive_seat_vent_status = {
            "HeatVentNone": HeatVentiSts.None_,
            "HeatVentOn": HeatVentiSts.On,
            "HeatVentOff": HeatVentiSts.Off,
            "HeatVentError": HeatVentiSts.Error,
            "HeatVentFunctionLimit": HeatVentiSts.Functionallimit,
            "HeatVentEnergyLimit": HeatVentiSts.Energylimit,
        }
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        sleep(1)
        for key in drive_seat_vent_status:
            self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=drive_seat_vent_status[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus, keys=["seatHeatVent","id==0", "status", "ventWorkStatus"], target_value=getattr(HeatVentWorkStatusRvs, key).value
            )

    @pytest.mark.smoke
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196791?projectId=46',
        name='RVS Case 112824',
    )
    def test_pass_seat_heating_level_caseid_112824(self):
        pass_seat_heating_level = {
            "0": HeatVentiLvl.Off,
            "1": HeatVentiLvl.Level1,
            "2": HeatVentiLvl.Level2,
            "3": HeatVentiLvl.Level3,
        }
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontRight, level=HeatVentiLvl.Level3)
        sleep(1)
        for key in pass_seat_heating_level:
            self.bus_comm.set_seat_heat_level(pos=SeatId.FrontRight, level=pass_seat_heating_level[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus, keys=["seatHeatVent","id==1", "status", "heatLevel"], target_value=int(key)
            )

    @pytest.mark.smoke
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196789?projectId=46',
        name='RVS Case 112826',
    )
    def test_pass_seat_heating_status_caseid_112826(self):
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.Off)
        sleep(2)
        pass_seat_heating_status = {
            "HeatVentNone": HeatVentiSts.None_,
            "HeatVentOn": HeatVentiSts.On,
            "HeatVentOff": HeatVentiSts.Off,
            "HeatVentError": HeatVentiSts.Error,
            "HeatVentFunctionLimit": HeatVentiSts.Functionallimit,
            "HeatVentEnergyLimit": HeatVentiSts.Energylimit,
        }
        for key in pass_seat_heating_status:
            self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRight, sts=pass_seat_heating_status[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus, keys=["seatHeatVent","id==1", "status", "heatWorkStatus"], target_value=getattr(HeatVentWorkStatusRvs, key).value
            )

    @pytest.mark.sanity
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196795?projectId=46',
        name='RVS Case 112820',
    )
    def test_pass_seat_vent_level_caseid_112820(self):
        pass_seat_vent_level = {
            "0": HeatVentiLvl.Off,
            "1": HeatVentiLvl.Level1,
            "2": HeatVentiLvl.Level2,
            "3": HeatVentiLvl.Level3,
        }
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontRight, level=HeatVentiLvl.Level3)
        sleep(1)
        for key in pass_seat_vent_level:
            self.bus_comm.set_seat_venti_level(pos=SeatId.FrontRight, level=pass_seat_vent_level[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus, keys=["seatHeatVent","id==1", "status", "ventLevel"], target_value=int(key)
            )

    @pytest.mark.sanity
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1196793?projectId=46',
        name='RVS Case 112822',
    )
    def test_pass_seat_vent_status_caseid_112822(self):
        pass_seat_vent_status = {
            "HeatVentNone": HeatVentiSts.None_,
            "HeatVentOn": HeatVentiSts.On,
            "HeatVentOff": HeatVentiSts.Off,
            "HeatVentError": HeatVentiSts.Error,
            "HeatVentFunctionLimit": HeatVentiSts.Functionallimit,
            "HeatVentEnergyLimit": HeatVentiSts.Energylimit,
        }
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.Off)
        sleep(1)
        for key in pass_seat_vent_status:
            self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontRight, sts=pass_seat_vent_status[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus, keys=["seatHeatVent","id==1", "status", "ventWorkStatus"], target_value=getattr(HeatVentWorkStatusRvs, key).value
            )

    @pytest.mark.smoke
    def test_tempDriver_caseid_112832(self):
        self.soa.hmi_set_climate_temperature(zone=ClimateZone.FirstRowLeft,value=0.0)
        sleep(1)
        for tempDriver_value in range(16,29,1):
            logger.info("---------------->{tempDriver_value}") 
            begin_time = time.time()
            self.soa.hmi_set_climate_temperature(zone=ClimateZone.FirstRowLeft,value=float(tempDriver_value))
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["climate","climateInfo","targetTemperature"],target_value=float(tempDriver_value),begin_time=begin_time
            )

    
    # @pytest.mark.sanity
    # @pytest.mark.fail
    # def test_steer_wheel_heating_level_caseid_112828(self):
    #     steer_wheel_heating_level = {
    #         "SteerWheelHeatOff":HeatLevel.Off,
    #         "SteerWheelHeatLow":HeatLevel.Low,
    #         "SteerWheelHeatMedium":HeatLevel.Mid,
    #         "SteerWheelHeatHigh":HeatLevel.High,
    #     }
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
    #     self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4})
    #     self.bus_comm.set_Hv_sys_relay_sts(HvSysRelaySts.Close)
    #     self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.High,source=SourceId.HMI)
    #     sleep(1)
    #     for key in steer_wheel_heating_level:
    #         self.soa.hmi_set_steer_wheel_heat_level(level=steer_wheel_heating_level[key],source=SourceId.HMI)
    #         self.tsp.check_rvs_data_update_new(
    #             block=BlockName.CabinStatus,keys=["steerWheel","level"],target_value=getattr(SteerWheelHeatLevelRvs, key).value,sleep_time=15
    #         )

    @pytest.mark.full
    def test_pm25_status_caseid_1983457(self):
        self.bus_comm.set_climate_pm25_sts(int_pm25_sts=PM25Sts.Complete)
        sleep(1)
        pm25_status={
            "SensorInitial":PM25Sts.Initial,
            "SensorCollecting":PM25Sts.Collecting,
            "SensorComplete":PM25Sts.Complete,
            "SensorError":PM25Sts.Error,
        }
        for key in pm25_status:
            self.bus_comm.set_climate_pm25_sts(int_pm25_sts=pm25_status[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["climate","pm25","status"],target_value=getattr(SensorWorkStatusRvs, key).value
            )
    
    @pytest.mark.full
    def test_pm25_level_caseid_1983458_1983035(self):
        pm25_level = {
            "PmLevel1":PM25Level.Level1,
            "PmLevel2":PM25Level.Level2,
            "PmLevel3":PM25Level.Level3,
            "PmLevel4":PM25Level.Level4,
            "PmLevel5":PM25Level.Level5,
            "PmLevel6":PM25Level.Level6,
            "PmLevelReserved":PM25Level.Reserved,
            "PmLevelInvalid":PM25Level.Invalid,
        }
        self.bus_comm.set_climate_pm25_sts(int_pm25_sts = PM25Sts.Complete)
        self.bus_comm.set_climate_pm25_level(int_pm25_level=PM25Level.Invalid)
        sleep(1)
        for key in pm25_level:
            self.bus_comm.set_climate_pm25_level(int_pm25_level=pm25_level[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["climate","pm25","level"],target_value=getattr(PM25LevelRvs, key).value
            )

    @pytest.mark.full
    def test_pm25_value_caseid_118672_1983036(self):
        self.bus_comm.set_climate_pm25_sts(int_pm25_sts = PM25Sts.Complete)
        self.bus_comm.set_climate_pm25_value(int_pm25_val=0)
        sleep(1)
        for pm25_value in range(10,100,10):
            logger.info("---------------->{pm25_value}")
            self.bus_comm.set_climate_pm25_value(int_pm25_val=int(pm25_value))
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["climate","pm25","value"],target_value=int(pm25_value),timeout=8
            )
    
    @pytest.mark.sanity
    def test_climate_status_caseid_112833(self):
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        sleep(2)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(6)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        begin_time = time.time()-1
        self.tsp.check_rvs_data_update_new(
            block=BlockName.CabinStatus,keys=["climate","climateInfo","climateStatus"],target_value=1,begin_time=begin_time,
        )
        sleep(1)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.Off)
        self.soa.hmi_set_climate_ac_sts(sts=False)
        begin_time = time.time()-1
        self.tsp.check_rvs_data_update_new(
            block=BlockName.CabinStatus,keys=["climate","climateInfo","climateStatus"],target_value=0,begin_time=begin_time,
        )

    
    @pytest.mark.sanity
    def test_defrost_caseid_109648_1983033(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_defrost_mode(mode=False)
        sleep(1)
        self.soa.hmi_set_climate_defrost_mode(mode=True)
        self.tsp.check_rvs_data_update_new(
                 block=BlockName.CabinStatus,keys=["defrostStatus","fastDefrostMode"],target_value=1
            )
        
    @pytest.mark.sanity
    def test_fragrance_type_caseid_112375(self):
        fragrance_type = {
            "FragranceChannel1":FragChannel.Channel1,
            "FragranceChannel2":FragChannel.Channel2,
            "FragranceChannel3":FragChannel.Channel3,
            "FragranceChannel4":FragChannel.Channel4,
            "FragranceChannel5":FragChannel.Channel5,
        }
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        for key in fragrance_type:
            self.soa.hmi_set_fragrance_sts(channel=fragrance_type[key],ratio=100,level=FragLevel.Level1)
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.CabinStatus,keys=["climate","fragrance","channel"],target_value=getattr(FragranceChannelRvs, key).value
            )


    @pytest.mark.sanity
    def test_channelId_caseid_112376(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        for signal_value in [12,24,36]:
            self.bus_comm.set_singal("bodycan","CcmBodyFr29","FragCh1Id",signal_value)
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.CabinStatus,keys=["climate","fragrance","channelId"],target_value=[signal_value,0,0])
                
            
    
    @pytest.mark.full
    def test_channelId_caseid_109717(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        for signal_value in [12,24,36]:
            self.bus_comm.set_singal("bodycan","CcmBodyFr29","FragCh2Id",signal_value)
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.CabinStatus,keys=["climate","fragrance","channelId"],target_value=[0,signal_value,0]
                )
            


    @pytest.mark.full
    def test_channelId_caseid_112816(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        for signal_value in [12,24,36]:
            self.bus_comm.set_singal("bodycan","CcmBodyFr29","FragCh3Id",signal_value)
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.CabinStatus,keys=["climate","fragrance","channelId"],target_value=[0,0,signal_value])

    # @pytest.mark.sanity
    # @pytest.mark.fail
    # def test_steer_wheel_heating_status_caseid_1983034(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
    #     self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4})
    #     self.bus_comm.set_Hv_sys_relay_sts(HvSysRelaySts.Close)
    #     self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
    #     sleep(1)
    #     self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.CabinStatus,keys=["steerWheel","status"],target_value=2,sleep_time=15
    #         )
    #     sleep(3)
    #     self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.CabinStatus,keys=["steerWheel","status"],target_value=1,sleep_time=15
    #         )
    
    @pytest.mark.full
    def test_FrangranceUseup_channel1_caseid_112819(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.bus_comm.set_singal("bodycan","CcmBodyFr25","FragCh1UseUpWrn",1)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["climate","fragrance","isUseUp"],target_value=[1,0,0]
            )
        

    @pytest.mark.full
    def test_FrangranceUseup_channel2_caseid_112818(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.bus_comm.set_singal("bodycan","CcmBodyFr25","FragCh2UseUpWrn",1)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["climate","fragrance","isUseUp"],target_value=[0,1,0]
            )
        

    @pytest.mark.full
    def test_FrangranceUseup_channel3_caseid_112817(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.bus_comm.set_singal("bodycan","CcmBodyFr25","FragCh3UseUpWrn",1)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["climate","fragrance","isUseUp"],target_value=[0,0,1]
            )
    


    @pytest.mark.full
    def test_fragrance_level_caseid_112374(self):
        fragrance_level = {
            "FragranceValueNoWarn":FragLevel.LevelOff,
            "FragranceValueLevel1":FragLevel.Level1,
            "FragranceValueLevel2":FragLevel.Level2,
            "FragranceValueLevel3":FragLevel.Level3
        }
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.AllZone, sts=isOn.On)
        self.soa.hmi_set_climate_ac_sts(sts=True)
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100,level=FragLevel.Level1)
        sleep(1)
        for key in fragrance_level:
            self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel1,ratio=100,level=fragrance_level[key])
            begin_time = time.time()
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.CabinStatus,keys=["climate","fragrance","level"], target_value=getattr(FragranceLevelRvs, key).value,begin_time = begin_time
            )  
    
    @pytest.mark.full
    def test_DriverAirLeftVent_caseid_1918796(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft, on=isOn.Off)
        sleep(1.5)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft, on=isOn.On)
        self.tsp.check_rvs_data_update_new(block=BlockName.CabinStatus,keys=["outletSystemStatus","driverVentStatus","isLeftOpen"],target_value=1)
        sleep(1)
        self.soa.hmi_set_climate_ac_sts(sts=False, timeout=0.5)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRowLeftLeft, sts=isOn.On)
        sleep(1.5)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftLeft, on=isOn.Off)
        self.tsp.check_rvs_data_update_new(block=BlockName.CabinStatus,keys=["outletSystemStatus","driverVentStatus","isLeftOpen"],target_value=0)


    @pytest.mark.full
    def test_DriverAirRightVent_caseid_1988131(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftRight, on=isOn.Off)
        sleep(1.5)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftRight, on=isOn.On)
        self.tsp.check_rvs_data_update_new(block=BlockName.CabinStatus,keys=["outletSystemStatus","driverVentStatus","isRightOpen"],target_value=1)
        sleep(1)
        self.soa.hmi_set_climate_ac_sts(sts=False, timeout=0.5)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftRight, on=isOn.On)
        sleep(1.5)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowLeftRight, on=isOn.Off)
        self.tsp.check_rvs_data_update_new(block=BlockName.CabinStatus,keys=["outletSystemStatus","driverVentStatus","isRightOpen"],target_value=0)

    



    @pytest.mark.full
    def test_PassAirLeftVent_caseid_1918798(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowRightLeft, on=isOn.Off)
        sleep(1.5)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowRightLeft, on=isOn.On)
        self.tsp.check_rvs_data_update_new(block=BlockName.CabinStatus,keys=["outletSystemStatus","passengerVentStatus","isLeftOpen"],target_value=1)
        sleep(1)
        self.soa.hmi_set_climate_ac_sts(sts=False, timeout=0.5)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowRightLeft, on=isOn.On)
        sleep(1.5)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowRightLeft, on=isOn.Off)
        self.tsp.check_rvs_data_update_new(block=BlockName.CabinStatus,keys=["outletSystemStatus","passengerVentStatus","isLeftOpen"],target_value=0)


    @pytest.mark.full
    def test_PassAirRightVent_caseid_1988132(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
        self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowRightRight, on=isOn.Off)
        sleep(1.5)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowRightRight, on=isOn.On)
        self.tsp.check_rvs_data_update_new(block=BlockName.CabinStatus,keys=["outletSystemStatus","passengerVentStatus","isRightOpen"],target_value=1)
        sleep(1)
        self.soa.hmi_set_climate_ac_sts(sts=False, timeout=0.5)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowRightRight, on=isOn.On)
        sleep(1.5)
        self.soa.hmi_set_climate_vent_sts(zone=ClimateZone.FirstRowRightRight, on=isOn.Off)
        self.tsp.check_rvs_data_update_new(block=BlockName.CabinStatus,keys=["outletSystemStatus","passengerVentStatus","isRightOpen"],target_value=0)

    


    @pytest.mark.full
    def test_ClimateFault_caseid_109827(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_singal("bodycan","CcmBodyFr21", 'RemClimaWarn',0)
        sleep(1)
        self.bus_comm.set_singal("bodycan","CcmBodyFr21", 'RemClimaWarn',2)
        self.tsp.check_rvs_data_update_new(block=BlockName.CabinStatus,keys=["climate","climateInfo","faultInfo","faultId"],target_value=7)
        sleep(1)
        self.bus_comm.set_singal("bodycan","CcmBodyFr21", 'RemClimaWarn',0)
        sleep(1)
        self.bus_comm.set_singal("bodycan","CcmBodyFr21", 'RemClimaWarn',8)
        self.tsp.check_rvs_data_update_new(block=BlockName.CabinStatus,keys=["climate","climateInfo","faultInfo","faultId"],target_value=13)
        sleep(1)
        self.bus_comm.set_singal("bodycan","CcmBodyFr21", 'RemClimaWarn',2)
        sleep(1)
        self.bus_comm.set_singal("bodycan","CcmBodyFr21", 'RemClimaWarn',0)
        self.tsp.check_rvs_data_update_new(block=BlockName.CabinStatus,keys=["climate","climateInfo","faultInfo","faultId"],target_value=0)


    @pytest.mark.full
    def test_Fragrance_Channel_caseid_116047(self):
        Fragrance_Channel={
            "0":FragChannel.NoReq,
            "1":FragChannel.Channel1,
            "2":FragChannel.Channel2,
            "3":FragChannel.Channel3,
            "4":FragChannel.Channel4,
            "5":FragChannel.Channel5,
        }
        self.soa.hmi_set_fragrance_sts(channel=FragChannel.Channel2,ratio=100.0,level=FragLevel.Level1)
        sleep(1)
        for key in Fragrance_Channel:
            self.soa.hmi_set_fragrance_sts(channel=Fragrance_Channel[key],ratio=100.0,level=FragLevel.Level1)
            self.tsp.check_rvs_data_update_new(
                 block=BlockName.CabinStatus,keys=["climate","fragrance","channel"], target_value=int(key))
            

    @pytest.mark.full
    def test_CoolingHeatingStatus_caseid_118696(self):
        self.bus_comm.set_singal("bodycan","CcmBodyFr11", 'ClimaCmptSts',1)
        sleep(1)
        self.bus_comm.set_singal("bodycan","CcmBodyFr11", 'ClimaCmptSts',0)
        self.tsp.check_rvs_data_update_new(block=BlockName.CabinStatus,keys=["climate","coolingHeatingStatus"], target_value=0)
        sleep(1)
        self.bus_comm.set_singal("bodycan","CcmBodyFr11", 'ClimaCmptSts',1)
        self.tsp.check_rvs_data_update_new(block=BlockName.CabinStatus,keys=["climate","coolingHeatingStatus"], target_value=1)
        sleep(1)
        self.bus_comm.set_singal("bodycan","CcmBodyFr11", 'ClimaCmptSts',2)
        self.tsp.check_rvs_data_update_new(block=BlockName.CabinStatus,keys=["climate","coolingHeatingStatus"], target_value=2)
        sleep(1)
        self.bus_comm.set_singal("bodycan","CcmBodyFr11", 'ClimaCmptSts',3)
        self.tsp.check_rvs_data_update_new(block=BlockName.CabinStatus,keys=["climate","coolingHeatingStatus"], target_value=3)
            
    
    
    @pytest.mark.sanity
    def test_RowSecLe_vent_status_caseid_1986520(self):
        RowSecLe_vent_status = {
            "HeatVentNone": HeatVentiSts.None_,
            "HeatVentOn": HeatVentiSts.On,
            "HeatVentOff": HeatVentiSts.Off,
            "HeatVentError": HeatVentiSts.Error,
            "HeatVentFunctionLimit": HeatVentiSts.Functionallimit,
            "HeatVentEnergyLimit": HeatVentiSts.Energylimit,
        }
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearLeft, sts=HeatVentiSts.Off)
        sleep(1)
        for key in RowSecLe_vent_status:
            self.bus_comm.set_seat_venti_sts(pos=SeatId.RearLeft, sts=RowSecLe_vent_status[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus, keys=["seatHeatVent","id==4", "status", "ventWorkStatus"], target_value=getattr(HeatVentWorkStatusRvs, key).value
            )
    
    
    @pytest.mark.sanity
    def test_RowSecLe_vent_level_caseid_1986519(self):
        RowSecLe_vent_level = {
            "0": HeatVentiLvl.Off,
            "1": HeatVentiLvl.Level1,
            "2": HeatVentiLvl.Level2,
            "3": HeatVentiLvl.Level3,
        }
        self.bus_comm.set_seat_venti_level(pos=SeatId.RearLeft, level=HeatVentiLvl.Level3)
        sleep(1)
        for key in RowSecLe_vent_level:
            self.bus_comm.set_seat_venti_level(pos=SeatId.RearLeft, level=RowSecLe_vent_level[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus, keys=["seatHeatVent","id==4", "status", "ventLevel"], target_value=int(key)
            )

    @pytest.mark.sanity
    def test_RowSecRi_vent_status_caseid_1986518(self):
        RowSecRi_vent_status = {
            "HeatVentNone": HeatVentiSts.None_,
            "HeatVentOn": HeatVentiSts.On,
            "HeatVentOff": HeatVentiSts.Off,
            "HeatVentError": HeatVentiSts.Error,
            "HeatVentFunctionLimit": HeatVentiSts.Functionallimit,
            "HeatVentEnergyLimit": HeatVentiSts.Energylimit,
        }
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearRight, sts=HeatVentiSts.Off)
        sleep(1)
        for key in RowSecRi_vent_status:
            self.bus_comm.set_seat_venti_sts(pos=SeatId.RearRight, sts=RowSecRi_vent_status[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus, keys=["seatHeatVent","id==6", "status", "ventWorkStatus"], target_value=getattr(HeatVentWorkStatusRvs, key).value
            )

    @pytest.mark.sanity
    def test_RowSecRi_vent_level_caseid_1986517(self):
        RowSecRi_vent_level = {
            "0": HeatVentiLvl.Off,
            "1": HeatVentiLvl.Level1,
            "2": HeatVentiLvl.Level2,
            "3": HeatVentiLvl.Level3,
        }
        self.bus_comm.set_seat_venti_level(pos=SeatId.RearRight, level=HeatVentiLvl.Level3)
        sleep(1)
        for key in RowSecRi_vent_level:
            self.bus_comm.set_seat_venti_level(pos=SeatId.RearRight, level=RowSecRi_vent_level[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus, keys=["seatHeatVent","id==6", "status", "ventLevel"], target_value=int(key)
            )


    @pytest.mark.sanity
    def test_RowSecLe_seat_heating_status_caseid_1988540(self):
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearLeft, sts=HeatVentiSts.Off)
        sleep(2)
        RowSecLe_seat_heating_status = {
            "HeatVentNone": HeatVentiSts.None_,
            "HeatVentOn": HeatVentiSts.On,
            "HeatVentOff": HeatVentiSts.Off,
            "HeatVentError": HeatVentiSts.Error,
            "HeatVentFunctionLimit": HeatVentiSts.Functionallimit,
            "HeatVentEnergyLimit": HeatVentiSts.Energylimit,
        }
        for key in RowSecLe_seat_heating_status:
            self.bus_comm.set_seat_heat_sts(pos=SeatId.RearLeft, sts=RowSecLe_seat_heating_status[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus, keys=["seatHeatVent","id==4", "status", "heatWorkStatus"], target_value=getattr(HeatVentWorkStatusRvs, key).value
            )

    @pytest.mark.sanity
    def test_RowSecLe_seat_heating_level_caseid_1988542(self):
        RowSecLe_seat_heating_level = {
            "0": HeatVentiLvl.Off,
            "1": HeatVentiLvl.Level1,
            "2": HeatVentiLvl.Level2,
            "3": HeatVentiLvl.Level3,
        }
        self.bus_comm.set_seat_heat_level(pos=SeatId.RearLeft, level=HeatVentiLvl.Level3)
        sleep(0.5)
        for key in RowSecLe_seat_heating_level:
            self.bus_comm.set_seat_heat_level(pos=SeatId.RearLeft, level=RowSecLe_seat_heating_level[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus, keys=["seatHeatVent","id==4","status", "heatLevel"], target_value=int(key)
            )
    

    @pytest.mark.sanity
    def test_RowSecRi_seat_heating_status_caseid_1988541(self):
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearRight, sts=HeatVentiSts.Off)
        sleep(2)
        RowSecRi_seat_heating_status = {
            "HeatVentNone": HeatVentiSts.None_,
            "HeatVentOn": HeatVentiSts.On,
            "HeatVentOff": HeatVentiSts.Off,
            "HeatVentError": HeatVentiSts.Error,
            "HeatVentFunctionLimit": HeatVentiSts.Functionallimit,
            "HeatVentEnergyLimit": HeatVentiSts.Energylimit,
        }
        for key in RowSecRi_seat_heating_status:
            self.bus_comm.set_seat_heat_sts(pos=SeatId.RearRight, sts=RowSecRi_seat_heating_status[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus, keys=["seatHeatVent","id==6", "status", "heatWorkStatus"], target_value=getattr(HeatVentWorkStatusRvs, key).value
            )


    @pytest.mark.sanity
    def test_RowSecRi_seat_heating_level_caseid_1988543(self):
        RowSecRi_seat_heating_level = {
            "0": HeatVentiLvl.Off,
            "1": HeatVentiLvl.Level1,
            "2": HeatVentiLvl.Level2,
            "3": HeatVentiLvl.Level3,
        }
        self.bus_comm.set_seat_heat_level(pos=SeatId.RearRight, level=HeatVentiLvl.Level3)
        sleep(0.5)
        for key in RowSecRi_seat_heating_level:
            self.bus_comm.set_seat_heat_level(pos=SeatId.RearRight, level=RowSecRi_seat_heating_level[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus, keys=["seatHeatVent","id==6","status", "heatLevel"], target_value=int(key)
            )
    

    @pytest.mark.sanity
    def test_passenger_tempdriver_caseid_112831(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_singal("bodycan","CcmBodyFr08",'CmptmtTFrntCmptmtTFrnt',0.0)
        self.bus_comm.set_singal("bodycan","CcmBodyFr08",'CmptmtTFrntQf', 3)
        self.soa.hmi_set_climate_ac_sts(sts=True, timeout=0.5)
        for key in range(760,800,10): 
            self.bus_comm.set_singal("bodycan","CcmBodyFr08",'CmptmtTFrntCmptmtTFrnt',key)
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["climate","temperature"],target_value=key*0.1-60,timeout=10
            )

    @pytest.mark.full
    def test_Driver_Occupied_caseid_1918439(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_singal("chassiscan2","VddmChas2Fr17", "DrvrSeatSts", 0)
        sleep(2)
        self.io.driver_seat_present()
        self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["seatInfo","id==0","occupied"],target_value=1,timeout=10
            )
        sleep(1)
        self.io.driver_seat_notpresent()
        self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["seatInfo","id==0","occupied"],target_value=0,timeout=10
            )


    @pytest.mark.full
    def test_Driver_treatedOccupied_caseid_1983042(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_singal("chassiscan2","VddmChas2Fr17", "DrvrSeatSts", 0)
        sleep(2)
        self.io.driver_seat_present()
        self.bus_comm.set_blt_sts(seat_id=SeatId.FrontLeft, blt_flt_sts=BltFltSts.NoFault,
                                      blt_lock_sts=BltLockSts.Lock)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00", 'BrkPedlPsdBrkPedlPsd', 1)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["seatInfo","id==0","treatedOccupied"],target_value=1,timeout=10
            )
        sleep(1)
        self.io.driver_seat_notpresent()
        self.bus_comm.set_blt_sts(seat_id=SeatId.FrontLeft, blt_flt_sts=BltFltSts.NoFault,
                                      blt_lock_sts=BltLockSts.Unlock)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00", 'BrkPedlPsdBrkPedlPsd', 0)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["seatInfo","id==0","treatedOccupied"],target_value=0,timeout=10
            )

    @pytest.mark.full
    def test_pass_treatedOccupied_caseid_1983041(self):
        self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04", "PassSeatSts",0)
        sleep(1)
        self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04", "PassSeatSts",2)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["seatInfo","id==1","treatedOccupied"],target_value=1,timeout=10
            )
        self.bus_comm.set_blt_sts(seat_id=SeatId.FrontRight, blt_flt_sts=BltFltSts.NoFault,
                                      blt_lock_sts=BltLockSts.Lock)
        sleep(1)
        self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04", "PassSeatSts",0)
        self.bus_comm.set_blt_sts(seat_id=SeatId.FrontRight, blt_flt_sts=BltFltSts.NoFault,
                                      blt_lock_sts=BltLockSts.Unlock)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["seatInfo","id==1","treatedOccupied"],target_value=0,timeout=10
            )   
    
    

    @pytest.mark.full
    def test_RowSecLe_treatedOccupied_caseid_1983040(self):
        self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04", "SeatOccptAtRowSecLe",0)
        sleep(1)
        self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04", "SeatOccptAtRowSecLe",2)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["seatInfo","id==4","treatedOccupied"],target_value=1,timeout=10
            )
        self.bus_comm.set_blt_sts(seat_id=SeatId.RearLeft, blt_flt_sts=BltFltSts.NoFault,
                                      blt_lock_sts=BltLockSts.Lock)
        sleep(1)
        self.bus_comm.set_blt_sts(seat_id=SeatId.RearLeft, blt_flt_sts=BltFltSts.NoFault,
                                      blt_lock_sts=BltLockSts.Unlock)
        self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04", "SeatOccptAtRowSecLe",0)    
        self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["seatInfo","id==4","treatedOccupied"],target_value=0,timeout=10
            ) 
   
    
    @pytest.mark.full
    def test_RowSecMid_treatedOccupied_caseid_1983039(self):
        self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04", "SeatOccptAtRowSecMid",0)
        sleep(1)
        self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04", "SeatOccptAtRowSecMid",2)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["seatInfo","id==5","treatedOccupied"],target_value=1,timeout=10
            )
        self.bus_comm.set_blt_sts(seat_id=SeatId.RearMiddle, blt_flt_sts=BltFltSts.NoFault,
                                      blt_lock_sts=BltLockSts.Lock)
        sleep(1)
        self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04", "SeatOccptAtRowSecMid",0)
        self.bus_comm.set_blt_sts(seat_id=SeatId.RearMiddle, blt_flt_sts=BltFltSts.NoFault,
                                      blt_lock_sts=BltLockSts.Unlock)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["seatInfo","id==5","treatedOccupied"],target_value=0,timeout=10
            )   
    
    
    @pytest.mark.full
    def test_RowSecRi_treatedOccupied_caseid_1983038(self):
        self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04", "SeatOccptAtRowSecRi",0)
        sleep(1)
        self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04", "SeatOccptAtRowSecRi",2)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["seatInfo","id==6","treatedOccupied"],target_value=1,timeout=10
            )
        self.bus_comm.set_blt_sts(seat_id=SeatId.RearRight, blt_flt_sts=BltFltSts.NoFault,
                                      blt_lock_sts=BltLockSts.Lock)
        sleep(1)
        self.bus_comm.set_blt_sts(seat_id=SeatId.RearRight, blt_flt_sts=BltFltSts.NoFault,
                                      blt_lock_sts=BltLockSts.Unlock)
        self.bus_comm.set_singal("backbonefr","SrsBackBoneFr04", "SeatOccptAtRowSecRi",0)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["seatInfo","id==6","treatedOccupied"],target_value=0,timeout=10
            )
    
    
    
    
    # @pytest.mark.sanity
    # def test_outview_defrost_caseid_112830(self):
    #     '''后视镜加热开启后会联动后窗电加热开启 '''
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
    #     self.sd_tester.write_multi_ccp({182:0x3,13:0x4})
    #     self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
    #     self.bus_comm.set_singal("bodycan","PdmBodyFr03", 'AmbTRawAtPassSideQly',3)
    #     self.bus_comm.set_singal("bodycan","PdmBodyFr03", 'AmbTRawAtPassSideAmbTVal',0)
    #     self.bus_comm.set_singal("bodycan","DdmBodyFr02", "MirrDefrstAtDrvSts",2) 
    #     self.bus_comm.set_singal("bodycan","PdmBodyFr03", "MirrDefrstAtPassSts",2)
    #     # self.bus_comm.set_singal("bodycan","CcmBodyFr08",'CmptmtTFrntCmptmtTFrnt',0.0)
    #     # self.bus_comm.set_singal("bodycan","CcmBodyFr08",'CmptmtTFrntQf', 3)
    #     sleep(2)
    #     self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
    #     self.bus_comm.set_singal("bodycan","PdmBodyFr03", 'AmbTRawAtPassSideQly',3)
    #     self.bus_comm.set_singal("bodycan","PdmBodyFr03", 'AmbTRawAtPassSideAmbTVal',320.0)
    #     # self.bus_comm.set_singal("bodycan","CcmBodyFr08",'CmptmtTFrntCmptmtTFrnt',650.0)
    #     self.bus_comm.set_singal("bodycan","DdmBodyFr02", "MirrDefrstAtDrvSts",1) 
    #     self.bus_comm.set_singal("bodycan","PdmBodyFr03", "MirrDefrstAtPassSts",1)
    #     self.soa.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
    #     sleep(6)
    #     with allure.step("设置后视镜加热"):
    #     self.soa.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
        # sleep(5)
        # self.tsp.check_rvs_data_update_new(
        #          block=BlockName.CabinStatus,keys=["defrostStatus","viewSwitchInfo","status"],target_value=1,sleep_time=15
        #     )
        # sleep(2)
        # self.soa.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
        # self.tsp.check_rvs_data_update_new(
        #          block=BlockName.CabinStatus,keys=["defrostStatus","viewSwitchInfo","status"],target_value=0,sleep_time=15
        #     )
        


    # @pytest.mark.sanity
    # def test_shieldWindow_defrost_caseid_116063(self):
    #     '''后视镜加热开启后会联动后窗电加热开启 '''
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
    #     self.sd_tester.write_multi_ccp({182:0x3,13:0x4})
    #     self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.Off)
    #     self.bus_comm.set_singal("bodycan","PdmBodyFr03", 'AmbTRawAtPassSideQly',0)
    #     self.bus_comm.set_singal("bodycan","PdmBodyFr03", 'AmbTRawAtPassSideAmbTVal',0)
    #     self.bus_comm.set_singal("bodycan","DdmBodyFr02", "MirrDefrstAtDrvSts",2) 
    #     self.bus_comm.set_singal("bodycan","PdmBodyFr03", "MirrDefrstAtPassSts",2)
    #     # self.bus_comm.set_singal("bodycan","CcmBodyFr08",'CmptmtTFrntCmptmtTFrnt',0.0)
    #     # self.bus_comm.set_singal("bodycan","CcmBodyFr08",'CmptmtTFrntQf', 3)
    #     sleep(2)
    #     self.soa.hmi_set_climate_power_sts(zone=ClimateZone.FirstRow, sts=isOn.On)
    #     self.bus_comm.set_singal("bodycan","PdmBodyFr03", 'AmbTRawAtPassSideQly',3)
    #     self.bus_comm.set_singal("bodycan","PdmBodyFr03", 'AmbTRawAtPassSideAmbTVal',10.0)
    #     # self.bus_comm.set_singal("bodycan","CcmBodyFr08",'CmptmtTFrntCmptmtTFrnt',650.0)
    #     self.bus_comm.set_singal("bodycan","DdmBodyFr02", "MirrDefrstAtDrvSts",1) 
    #     self.bus_comm.set_singal("bodycan","PdmBodyFr03", "MirrDefrstAtPassSts",1)
    #     self.soa.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
    #     sleep(6)
    #     # with allure.step("设置后视镜加热"):
    #     self.soa.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": True}]})
    #     self.tsp.check_rvs_data_update_new(
    #              block=BlockName.CabinStatus,keys=["defrostStatus","shieldWindow","windowId==2","ventWorkStatus"],target_value=1,sleep_time=15
    #         )
    #     sleep(2)
    #     self.soa.send_method_request("OuterRearViewService_client", "SetHeat", {"params": [{"id": 2, "isOn": False}]})
    #     self.tsp.check_rvs_data_update_new(
    #              block=BlockName.CabinStatus,keys=["defrostStatus","shieldWindow","windowId==2","ventWorkStatus"],target_value=0,sleep_time=15
    #         )
        

    @pytest.mark.full
    @pytest.mark.v210
    def test_fragrance_left_caseid_1990895(self):
        self.bus_comm.set_singal("bodycan","CcmBodyFr60", "AirFragCh1AvlTi", 180)
        self.bus_comm.set_singal("bodycan","CcmBodyFr60", "AirFragCh2AvlTi", 0)
        self.bus_comm.set_singal("bodycan","CcmBodyFr60", "AirFragCh3AvlTi", 0)
        sleep(10)
        for key in [150,100,0]:
            self.bus_comm.set_singal("bodycan","CcmBodyFr60", "AirFragCh1AvlTi", key)
            # sleep(10)
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["climate","fragrance","leftTime"],target_value=[key,0,0,0,0]
            )


    @pytest.mark.full
    @pytest.mark.v210
    def test_fragrance_left_caseid_1990894(self):
        self.bus_comm.set_singal("bodycan","CcmBodyFr60", "AirFragCh1AvlTi", 0)
        self.bus_comm.set_singal("bodycan","CcmBodyFr60", "AirFragCh2AvlTi", 180)
        self.bus_comm.set_singal("bodycan","CcmBodyFr60", "AirFragCh3AvlTi", 0)
        sleep(10)
        for key in [150,100,0]:
            self.bus_comm.set_singal("bodycan","CcmBodyFr60", "AirFragCh2AvlTi", key)
            # sleep(10)
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["climate","fragrance","leftTime"],target_value=[0,key,0,0,0]
            )

    @pytest.mark.sanity
    @pytest.mark.v210
    def test_fragrance_left_caseid_1990893(self):
        self.bus_comm.set_singal("bodycan","CcmBodyFr60", "AirFragCh1AvlTi", 0)
        self.bus_comm.set_singal("bodycan","CcmBodyFr60", "AirFragCh2AvlTi", 0)
        self.bus_comm.set_singal("bodycan","CcmBodyFr60", "AirFragCh3AvlTi", 180)
        sleep(10)
        for key in [150,100,0]:
            self.bus_comm.set_singal("bodycan","CcmBodyFr60", "AirFragCh3AvlTi", key)
            # sleep(10)
            self.tsp.check_rvs_data_update_new(
                block=BlockName.CabinStatus,keys=["climate","fragrance","leftTime"],target_value=[0,0,key,0,0]
            )