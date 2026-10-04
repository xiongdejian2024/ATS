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
        self.soa.update(["ClimateControlService_client","CentralLockService_client","TailWingService_client","SteerWheelService_client","TyreService_client","ChargeLidService_client","OuterRearViewService_client","ShieldWindowService_client","VehicleModeService_client","VehicleSetStatusService_client","HighVoltageService_client"])
        sleep(3)
        self.vid = self.tb_config["vid"]
        self.rvs_client = RvsClient(vid=self.vid)
        logger.info("VID: {0}".format(self.vid))
        sleep(2)

    def before_each_func(self, ecu):
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_extral_light_button_to_defaul_sts()

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        self.sd_tester.write_ccp({225: 7, 226: 7}) 
        self.sd_tester.write_multi_ccp({950:1})
        self.sd_tester.write_multi_ccp({962:0})
        self.sd_tester.write_multi_ccp({973:2})
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass



    @pytest.mark.sanity
    @pytest.mark.fail
    def test_charggun_status_caseid_1918998(self):
        charggun_status = {
            "PsDisconnected":DCChrgnHndlSts.Disconnected,
            "PsConnectedWithoutPower":DCChrgnHndlSts.ConnectedWithoutPower,
            "PsConnectedWithPower":DCChrgnHndlSts.ConnectedWithPower,
        }
        self.bus_comm.set_dc_chrg_handle_sts(DCChrgnHndlSts.ConnectedWithPower)
        sleep(2)
        for key in charggun_status:
            self.bus_comm.set_dc_chrg_handle_sts(sts=charggun_status[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","pluggerStatus"],target_value=getattr(PluggerStatusRvs, key).value
            )    

    
    @pytest.mark.sanity
    @pytest.mark.fail
    def test_charging_status_caseid_1918982(self):
        charging_status = {
            "CsNoCharging":ChargingSts.NoCharging,
            "CsDCCharging":ChargingSts.DCCharging,
            "CsSuperCharging":ChargingSts.SuperCharging,
            "CsDCChargingEnd":ChargingSts.DCChargingEnd,
        }
        self.bus_comm.set_charging_sts(ChargingSts.DCCharging)
        sleep(1)
        for key in charging_status:
            self.bus_comm.set_charging_sts(sts=charging_status[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","chargingStatus"],target_value=getattr(ChargeStatusRvs, key).value,timeout=12
            )
      

    

    @pytest.mark.full
    def test_chrglid_status_caseid_118674_109789(self):
        self.bus_comm.set_chrglid_pos(0)
        sleep(5)
        self.bus_comm.set_chrglid_pos(100)
        self.tsp.check_rvs_data_update_new(
        block=BlockName.EicCharging,keys=["charging","lidStatus"],target_value=0
        )
        self.bus_comm.set_chrglid_pos(0)
        self.tsp.check_rvs_data_update_new(
        block=BlockName.EicCharging,keys=["charging","lidStatus"],target_value=2
        )


    @pytest.mark.full
    def test_charg_maxcurrent_caseid_118665_1987847(self):
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr31","DCChrgrIMax",0)
        sleep(1)
        for signal_value in [1633.4, 1634.5, 1635.6,1637.7]:
            self.bus_comm.set_singal("propulsioncan","BecmPropFr31","DCChrgrIMax",signal_value)
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","equipmentInfo","maxCurrent"],target_value=signal_value,timeout=12
            )



    # @pytest.mark.full
    # def test_charg_actualcurrent_caseid_118664_1987848(self):
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr13",'HvBattChrgnPwrCns1',5)
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr22","ChrgEquipIDc",0)
    #     sleep(1)
    #     for signal_value in [10.0]:
    #         self.bus_comm.set_singal("propulsioncan","BecmPropFr22","ChrgEquipIDc",signal_value)
    #         self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","equipmentInfo","actualCurrent"],target_value=signal_value,timeout=12
    #         )


    @allure.title("获取和通知动力电池充电电压_400V_800V")
    @pytest.mark.full
    def test_charg_voltage_caseid_118668_118669(self):
        # self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        # self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        # self.bus_comm.set_singal("propulsioncan","BecmPropFr01","HvBattUDc",0)
        # sleep(1)
        # for signal_value in [220, 224, 880,884]:
        #     self.bus_comm.set_singal("propulsioncan","BecmPropFr01","HvBattUDc",signal_value)
        #     self.tsp.check_rvs_data_update_new(
        #         block=BlockName.EicCharging,keys=["batteryInfo","voltage"],target_value=signal_value*0.25,timeout=12
        #     )
        # sleep(1)
        self.sd_tester.write_multi_ccp({950:2}) #Venus
        self.sd_tester.write_multi_ccp({962:2}) #800V
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr01", 'HvBattUDc800', 10.0)
        sleep(1)
        for signal_value in [220,224,880,884,4092]:
            self.bus_comm.set_singal("propulsioncan","BecmPropFr01", 'HvBattUDc800', signal_value)
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["batteryInfo","voltage"],target_value=signal_value*0.25,timeout=15
            )
        sleep(1)
        self.sd_tester.write_multi_ccp({950:1})
        self.sd_tester.write_multi_ccp({962:0})

        
    
    
    # @pytest.mark.full
    # @pytest.mark.fail
    # def test_equipment_type_caseid_1983037_116052(self):
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr02","JIDUChgrFlg",2)
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","equipmentInfo","type"],target_value=[7,1]
    #         )
    #     self.bus_comm.set_singal("connectivitycanfd","BncmBsrmConnectivityFr03","ChrgrPileInfo",0)
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","equipmentInfo","type"],target_value=[7,1],timeout=12,sleep_time=15
    #         )
    
    # @pytest.mark.sanity
    # def test_charg_InputPower_caseid_1919008(self):
    #     self.sd_tester.write_ccp(ccp={962: 0x00})
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr02","JIDUChgrFlg",2)
    #     self.bus_comm.set_singal("connectivitycanfd","BncmBsrmConnectivityFr03","ChrgrPileInfo",0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr01","HvBattUDc",0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr22","ChrgEquipIDc",0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr13",'HvBattChrgnPwrCns1',0)
    #     sleep(1)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr13",'HvBattChrgnPwrCns1',5)
    #     for vol in [280]:
    #         for cur in [10]:
    #             self.bus_comm.set_singal("propulsioncan","BecmPropFr01","HvBattUDc",vol)
    #             self.bus_comm.set_singal("propulsioncan","BecmPropFr22","ChrgEquipIDc",cur)
    #             self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","chargerInputPower"],target_value=(vol)*0.25*(cur),timeout=12
    #         )

    @pytest.mark.sanity
    def test_charg_targetsoc_caseid_118663(self):
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb",0)
        sleep(1)
        for signal_value in [100,110,800,1000]:
            self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb",signal_value)
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","chargeTargetSoc"],target_value=signal_value*0.1,timeout=12
            )

    
    @pytest.mark.full
    @pytest.mark.fail
    def test_totalChargeEnergy_caseid_118661_118660(self):
        self.sd_tester.write_ccp(ccp={566: 0x10})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr16","TotChrgEgy",500)
        sleep(1)
        for signal_value in [10000,10100,80000,80100]:
            self.bus_comm.set_singal("propulsioncan","BecmPropFr16","TotChrgEgy",signal_value)
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","totalChargeEgy"],target_value=signal_value,timeout=15)


    @pytest.mark.full
    def test_remainChargingTime_caseid_118673(self):
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr21","HvBattChrgnTiEstimd",0)
        sleep(1)
        for signal_value in [60,50]:
            self.bus_comm.set_singal("propulsioncan","BecmPropFr21","HvBattChrgnTiEstimd",signal_value)
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","remainChargingTime"],target_value=signal_value,timeout=12
            )

    
    @pytest.mark.full
    def test_chrglid_pos_caseid_109424(self):
        self.bus_comm.set_chrglid_pos(0)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        self.tsp.check_rvs_data_update_new(
        block=BlockName.EicCharging,keys=["charging","chargingLidPos"],target_value=(100),timeout=12
        )
        self.bus_comm.set_chrglid_pos(0)
        self.tsp.check_rvs_data_update_new(
        block=BlockName.EicCharging,keys=["charging","chargingLidPos"],target_value=(0),timeout=12
        )

    

    # @pytest.mark.sanity
    # def test_chrgegythistime_caseid_112351(self):
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.NoCharging)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr16","TotChrgEgy",0)
    #     sleep(2)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr16","TotChrgEgy",10000)
    #     sleep(30)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.DCChargingEnd)
    #     sleep(5)
    #     self.tsp.check_rvs_data_update_new(
    #              block=BlockName.EicCharging,keys=["charging","chargeEgyThisTime"],target_value=10000,timeout=12
    #         )


    # @pytest.mark.sanity
    # @pytest.mark.fail
    # def test_chargTime_caseid_112353(self):
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.NoCharging)
    #     sleep(2)
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
    #     utc_timestamp = time.time()
    #     sleep(5)
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","recentChargeStartTime"],target_value=utc_timestamp*1000,timeout=12,target_value_buffer=1000)
    #     sleep(10)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.DCChargingEnd)
    #     utc_timestamp =time.time()
    #     sleep(5)
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","recentChargeEndTime"],target_value=utc_timestamp*1000,timeout=12,target_value_buffer=1000)


    @pytest.mark.sanity
    def test_charg_booktime_caseid_1985410(self):
        self.bus_comm.set_singal("propulsioncan","BecmPropFr33","RemoteBookStrtTiChrgnTmrChrgnTmrhour",24)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr33","RemoteBookStrtTiChrgnTmrChrgnTmrmin",60)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr33","RemoteBookStopTiChrgnTmrChrgnTmrhour",24)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr33","RemoteBookStopTiChrgnTmrChrgnTmrmin",60)
        sleep(1)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr32","ChrgPilBookChrgn",1)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr33","RemoteBookStrtTiChrgnTmrChrgnTmrmin",30)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr33","RemoteBookStopTiChrgnTmrChrgnTmrhour",20)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr33","RemoteBookStopTiChrgnTmrChrgnTmrmin",10)
        for signal_value in [11,13,15]:
            self.bus_comm.set_singal("propulsioncan","BecmPropFr33","RemoteBookStrtTiChrgnTmrChrgnTmrhour",signal_value)
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging", "bookInfo", "startHour"],target_value=signal_value,timeout=12
            )

    
    # @pytest.mark.sanity
    # @allure.testcase(
    #     'https://jama.jiduauto.com/perspective.req#/testCases/1350998?projectId=46',
    #     name='RVS case 1981197',
    # )
    # def test_chargbook_status_caseid_1981197(self):
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr32", 'ChrgPilBookChrgn',0)
    #     sleep(10)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr32", 'ChrgPilBookChrgn',1)
    #     self.tsp.check_rvs_data_update_new(
    #         BlockName.EicCharging,keys=["charging", "bookInfo", "bookStatus"], target_value=1,timeout=12)
        # self.bus_comm.set_singal("propulsioncan","BecmPropFr32", 'ChrgPilBookChrgn',0)
        # self.tsp.check_rvs_data_update_new(
        #     BlockName.EicCharging,keys=["charging", "bookInfo", "bookStatus"], target_value=0,sleep_time=15)


    # @pytest.mark.sanity
    # def test_targetRange_caseid_1986515(self):
    #     self.sd_tester.write_multi_ccp({3: 129, 566: 25,950:1,962:0})
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.NoCharging)
    #     # self.bus_comm.set_singal("propulsioncan","BecmPropFr04", 'HvBattEgyCdn', 90.0)
    #     # self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13", 'BookChrgnTarValFb', 90.0)
    #     # self.soa.send_method_request("HighVoltageService_client", "SetRange",
    #     #                                     {"infos": {"type": 0, "CLTCRange": 100, "estimatedRange": 999}})
    #     # sleep(2)
    #     # self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
    #     # self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
    #     self.bus_comm.set_singal("propulsioncan","EcmPropFr04", 'DispHvBattLvlOfChrg', 100.0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr04", 'HvBattEgyCdn', 100.0)
    #     self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13", 'BookChrgnTarValFb', 100.0)
    #     self.soa.send_method_request("HighVoltageService_client", "SetAveragePowerConsume", {"power":50})
    #     self.soa.send_method_request("HighVoltageService_client", "SetRange",
    #                                         {"infos": {"type": 0, "CLTCRange": 100, "estimatedRange": 999}})
    #     sleep(2)
    #     self.soa.send_method_request("HighVoltageService_client", "SetRange",
    #                                         {"infos": {"type": 0, "CLTCRange": 999, "estimatedRange": 999}})
    #     self.tsp.check_rvs_data_update_new(
    #         BlockName.EicCharging,keys=["charging", "chargeTargetMileage"], target_value=770,timeout=12,sleep_time=15)
    #     sleep(2)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr04", 'HvBattEgyCdn', 0.0)
    #     self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13", 'BookChrgnTarValFb', 0.0)
    #     self.soa.send_method_request("HighVoltageService_client", "SetRange",
    #                                         {"infos": {"type": 0, "CLTCRange":0, "estimatedRange": 999}})
    #     self.tsp.check_rvs_data_update_new(
    #         BlockName.EicCharging,keys=["charging", "chargeTargetMileage"], target_value=0,timeout=12,sleep_time=15)



    @pytest.mark.sanity
    def test_incMileageThisTime_caseid_1986514(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16,950: 1,966:1})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_charging_sts(sts=ChargingSts.NoCharging)
        # self.bus_comm.set_singal("propulsioncan","BecmPropFr04","HvBattEgyCdn",100.0)
        # self.bus_comm.set_singal("propulsioncan","EcmPropFr04", 'DispHvBattLvlOfChrg', 10.0) 
        sleep(1)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr04","HvBattEgyCdn",100.0)
        self.bus_comm.set_singal("propulsioncan","EcmPropFr04", 'DispHvBattLvlOfChrg', 10.0)
        sleep(5) 
        for key in [20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0]:
            self.bus_comm.set_singal("propulsioncan","EcmPropFr04", 'DispHvBattLvlOfChrg', key)   
            self.tsp.check_rvs_data_update_new(
                BlockName.EicCharging,keys=["charging", "incMileageThisTime"], target_value=key*0.01*780,timeout=14)

    @pytest.mark.full
    def test_current_caseid_118670(self):
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_charging_sts(sts=ChargingSts.NoCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'HvBattIDc1', 0.0)
        sleep(2)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        current= [-1638.0,10.0,11.0,1638.6]
        for key in current:
            self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'HvBattIDc1', key)
            self.tsp.check_rvs_data_update_new(
                    BlockName.EicCharging,keys=["batteryInfo", "current"], target_value=key,timeout=15,target_value_buffer=0.1)


    @pytest.mark.full
    def test_charg_maxcurrent_caseid_1987847(self):
        '''不用满足1A精度组包 '''
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr31","DCChrgrIMax",0)
        sleep(1)
        for signal_value in [1637.0,1637.5,1638.7]:
            self.bus_comm.set_singal("propulsioncan","BecmPropFr31","DCChrgrIMax",signal_value)
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","equipmentInfo","maxCurrent"],target_value=signal_value,timeout=12
            )


    @pytest.mark.full
    def test_charg_voltage_caseid_1987846(self):
        '''不用满足1V精度组包 '''
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr01","HvBattUDc",0)
        sleep(1)
        for signal_value in [220,222,880,882]:
            self.bus_comm.set_singal("propulsioncan","BecmPropFr01","HvBattUDc",signal_value)
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["batteryInfo","voltage"],target_value=signal_value*0.25,timeout=14
            )

    # @pytest.mark.full
    # def test_batteryReqCurrent_caseid_1987844(self):
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
    #     self.bus_comm.set_singal("propulsioncan","EcmPropXEVFr16",'HvBattChrgnILim',20)
    #     for key in [0,21.0,819.1]:
    #         self.bus_comm.set_singal("propulsioncan","EcmPropXEVFr16",'HvBattChrgnILim',key)
    #         self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","batteryReqCurrent"],target_value=key,timeout=12,sleep_time=20
    #         )

    @pytest.mark.full
    def test_isCharging_caseid_1987843(self):
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.NoCharging)
        sleep(2)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","isCharging"],target_value=True,timeout=12
            )
        sleep(2)
        self.bus_comm.set_charging_sts(sts=ChargingSts.NoCharging)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","isCharging"],target_value=False,timeout=12
            )  
    
    

    @pytest.mark.full
    def test_isConnect_caseid_1987842(self):
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(2)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","isConnect"],target_value=True,timeout=12
            )
        sleep(2)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","isConnect"],target_value=False,timeout=12
            )
    
    
    
    # @pytest.mark.sanity
    # def test_Temperature_caseid_1987841(self):
    #     '''电池显示温度 '''
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMin',0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMax',0)
    #     for key in [-256.0,20.0,39.9,40.0,41.0,255.9]:
    #         self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMin',key)
    #         self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","chargingSlowRemind","temperature"],target_value=key,timeout=15,sleep_time=30)
        # sleep(2)
        # for key in [40.0,41.0,255.9]:
        #     self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMin',30.0)
        #     self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMax',key)
        #     self.tsp.check_rvs_data_update_new(
        #         block=BlockName.EicCharging,keys=["charging","chargingSlowRemind","temperature"],target_value=key,timeout=15,sleep_time=25)
    
    
    # @pytest.mark.sanity
    # def test_ChargingSlowRemind_caseid_1987840_1987833(self):
    #     '''从0开始跳变 '''
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr13",'HvBattChrgnPwrCns1',5)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMin',0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMax',0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr22","ChrgEquipIDc",0)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr28",'HvBattILim',0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr31","DCChrgrIMax",0)
    #     self.bus_comm.set_SOC_display_value(79.0)
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.NoCharging)
    #     sleep(1)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr22","ChrgEquipIDc",10.0)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr28",'HvBattILim',30.0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr31","DCChrgrIMax",30.0)
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMin',19.0)
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","chargingSlowRemind","reason"],target_value=[1],timeout=12,sleep_time=20)
    #     sleep(5)
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","chargingSlowRemind","reason"],target_value=[3,1],timeout=12,sleep_time=20)
    #     self.bus_comm.set_SOC_display_value(80.0)
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","chargingSlowRemind","reason"],target_value=[3,2,1],timeout=12,sleep_time=20)
    #     sleep(1)
    #     self.bus_comm.set_SOC_display_value(70.0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMin',20.0)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr28",'HvBattILim',20.0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr31","DCChrgrIMax",150.0)
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","chargingSlowRemind","reason"],target_value=[0],timeout=12,sleep_time=20)

        

    # @pytest.mark.full
    # def test_ChargingSlowRemind_caseid_1987839_1987838_1987837(self):
    #     '''从1,2,3开始跳变 '''
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr13",'HvBattChrgnPwrCns1',5)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMin',0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMax',0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr22","ChrgEquipIDc",0)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr28",'HvBattILim',0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr31","DCChrgrIMax",0)
    #     self.bus_comm.set_SOC_display_value(79.0)
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.NoCharging)
    #     sleep(1)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr22","ChrgEquipIDc",10.0)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr28",'HvBattILim',30.0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr31","DCChrgrIMax",30.0)
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMin',19.0)
    #     sleep(2)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMin',20.0)
    #     sleep(2)
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","chargingSlowRemind","reason"],target_value=[3],timeout=12,sleep_time=20)
    #     sleep(1)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr28",'HvBattILim',20.0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr31","DCChrgrIMax",150.0)
    #     self.bus_comm.set_SOC_display_value(80.0)
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","chargingSlowRemind","reason"],target_value=[2],timeout=12,sleep_time=20)
        
    #     sleep(1)
    #     self.bus_comm.set_SOC_display_value(79.0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMin',19.0)
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","chargingSlowRemind","reason"],target_value=[1],timeout=12,sleep_time=20)
    #     sleep(1)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMin',20.0)
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","chargingSlowRemind","reason"],target_value=[0],timeout=12,sleep_time=20)     
    
    
    
    
    
    
    # @pytest.mark.full
    # def test_calculatedSoc_caseid_118658(self):
    #     self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
    #     self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.FACTORY, car_mode_sub=0)
    #     self.bus_comm.set_battsocraw2_less_value(battsocraw2=65)
    #     self.tsp.check_rvs_data_update_new(
    #         BlockName.EicCharging,keys=["batteryInfo", "calculatedSoc"], target_value=0,sleep_time=15)

    # @pytest.mark.full
    # def test_calculatedSoh_caseid_118659(self):
    #     self.mix.set_usage_mode(UsageMode.INACTIVE)
    #     self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr07","BattSOHLAMRaw",0.0)
    #     self.bus_comm.check_singal("connectivitycanfd","BgmConnectivityFr06","BattSohRaw2",0.0)
    #     self.tsp.check_rvs_data_update_new(
    #         BlockName.EicCharging,keys=["batteryInfo", "calculatedSoh"], target_value=0,sleep_time=15)
        

        
        # self.set("propulsioncan","BecmPropFr32", 'ChrgPilBookChrgn', 'ChrgPilBookChrgn_Reserve')
        # self.tsp.check_rvs_data_update_new(
        #     BlockName.EicCharging,["charging", "bookInfo", "bookStatus"], "ChargingBookStatusBookOff"
        # )

        # self.set("propulsioncan","BecmPropFr32", 'ChrgPilBookChrgn', 'ChrgPilBookChrgn_On')
        # self.tsp.check_rvs_data_update_new(
        #     BlockName.EicCharging,["charging", "bookInfo", "bookStatus"], "ChargingBookStatusBookOn"
        # )

        # self.set("propulsioncan","BecmPropFr32", 'ChrgPilBookChrgn', 'ChrgPilBookChrgn_Default')
        # self.tsp.check_rvs_data_update_new(
        #     BlockName.EicCharging,["charging", "bookInfo", "bookStatus"], "ChargingBookStatusBookOn"
        # )



    # @pytest.mark.sanity
    # def test_chargspd_caseid_190190(self):
    #     self.mix.set_usage_mode(UsageMode.CONVENIENCE)
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
    #     for signal_value in [300,200,100]:
    #         self.bus_comm.set_singal("ChassisCAN1","EcmChas1Fr29","ChrgnSpd",signal_value)
    #         self.tsp.check_rvs_data_update_new(
    #              block=BlockName.EicCharging,keys=["charging","chargingSpeed"],target_value=signal_value
    #             )
    

    # @pytest.mark.addenergy
    # @pytest.mark.xfail
    # @allure.testcase(
    #     'https://jama.jiduauto.com/perspective.req#/testCases/1350952?projectId=46',
    #     name='RVS case 1350952',
    # )
    # def test_chrgegythistime_caseid_1350952(self):
    #     self.ipdu.propulsioncan_becmpropfr16_totchrgegy_value(51)
    #     self.ipdu.backbonefr_vddmbackbonefr16_chrgnordischrgnstsfb_chrgnsts2_dccharging()
    #     time.sleep(30)
    #     self.ipdu.propulsioncan_becmpropfr16_totchrgegy_value(1050)
    #     self.ipdu.backbonefr_vddmbackbonefr16_chrgnordischrgnstsfb_chrgnsts2_dcchargingend()
    #     self.tsp.check_rvs_data_update_new(BlockName.EicCharging,["charging", "chargeEgyThisTime"], 999)


    # @pytest.mark.sanity
    # def test_fullChargingRemind_caseid_1987845(self):
    #     self.sd_tester.write_multi_ccp({3: 129, 566: 25,950:1,962:0})
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr16", 'ChrgnOrDisChrgnStsFb', 0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr03", 'HvBattChrgnCmpl', 0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr16", 'TotChrgEgy', 2000)
    #     sleep(3)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr03", 'HvBattChrgnCmpl', 1)
    #     sleep(1)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr03", 'HvBattChrgnCmpl', 0)
    #     sleep(1)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr16", 'ChrgnOrDisChrgnStsFb', 15)
    #     sleep(1)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr16", 'TotChrgEgy', 3000)
    #     sleep(1)
    #     self.tsp.check_rvs_data_update_new(block=BlockName.EicCharging,keys=["fullChargingRemind", "remind"],target_value=False)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr16", 'TotChrgEgy', 4000)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr16", 'TotChrgEgy', 112000)
    #     self.tsp.check_rvs_data_update_new(block=BlockName.EicCharging,keys=["fullChargingRemind", "remind"],target_value=True) 



    # @pytest.mark.sanity
    # def test_acdcType_caseid_1990885(self):
    #     self.sd_tester.write_multi_ccp({973:2}) # 支持交直流  
    #     self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',0)        
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0) 
    #     sleep(1)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',1)
    #     self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',8)
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","acdcType"],target_value=1,timeout=12,sleep_time=20
    #         )
    #     sleep(1)
    #     self.sd_tester.write_multi_ccp({973:1}) # 支持交流
    #     self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',5)        
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0)
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","acdcType"],target_value=2,timeout=12,sleep_time=20
    #         )
        # self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',0)        
        # self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0) 
        # sleep(2)
        # self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',1)        
        # self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',1)
        # self.tsp.check_rvs_data_update_new(
        #         block=BlockName.EicCharging,keys=["charging","acdcType"],target_value=3,timeout=12,sleep_time=20
        #     )



    # @allure.title("获取和通知充电信息_新75度设置百公里电耗为0_充电速度_CLTC工况")#200
    # @pytest.mark.full
    # def test_caseid_660660(self):
    #     self.sd_tester.write_multi_ccp({3: 129, 566: 25,950:1,962:0})
    #     sleep(3)
    #     self.soa.send_method_request("HighVoltageService_client", "SetRange",
    #                                      {"infos": {"type": 0, "CLTCRange": 999, "estimatedRange": 999}})
    #     #12.75kWh/100km
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.NoCharging)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr13", 'HvBattChrgnPwrCns1', 0)
    #     # self.partner.empty_all(1)
    #     # self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
    #     #                                        {"out": {"cltcEnergyComsumption":12.75}})
    #     sleep(1)
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
    #     self.soa.send_method_request("HighVoltageService_client", "SetAveragePowerConsume", {"power":12.75})
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr13", 'HvBattChrgnPwrCns1', 100000.0)
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","chargingSpeed"],target_value=784,timeout=12,sleep_time=20
    #         )
    #     self.soa.send_method_request("HighVoltageService_client", "SetRange",
    #                                      {"infos": {"type": 1, "CLTCRange": 999, "estimatedRange": 999}})
    #     self.soa.send_method_request("HighVoltageService_client", "SetAveragePowerConsume", {"power": 0})
    #     sleep(1)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr13", 'HvBattChrgnPwrCns1', 110000.0)
    #     sleep(1)
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","chargingSpeed"],target_value=1500,timeout=12,sleep_time=20
    #         )


    # @pytest.mark.sanity
    # @pytest.mark.v210
    # def test_charggun_caseid_1990884(self):
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0)
    #     self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',0)        
    #     sleep(1)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0)
    #     self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',10)        
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","pluggerStatus"],target_value=7
    #         )
    #     sleep(1)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0)
    #     self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',4) 
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","pluggerStatus"],target_value=8
    #         )
    #     sleep(1)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0)
    #     self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',5) 
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","pluggerStatus"],target_value=9
    #         )
    #     sleep(1)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0)
    #     self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',6) 
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","pluggerStatus"],target_value=10
    #         )
    #     sleep(1)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0)
    #     self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',7) 
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","pluggerStatus"],target_value=11
    #         )
        


    @pytest.mark.sanity
    @pytest.mark.v210
    def test_isDischarging_caseid_1990886(self):
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr16", 'ChrgnOrDisChrgnStsFb',0)
        sleep(1)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr16", 'ChrgnOrDisChrgnStsFb',8)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","isDischarging"],target_value=True
            )
        sleep(1)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr16", 'ChrgnOrDisChrgnStsFb',15)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","isDischarging"],target_value=False
            )
        


    @allure.title("获取和通知动力电池充电功率")
    @pytest.mark.full
    def test_caseid_118666(self):
        self.sd_tester.write_multi_ccp({950:2})
        self.sd_tester.write_multi_ccp({962:2})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr12", 'HvBattChrgnPwrCns800', 100.0)
        sleep(1)
        for signal_value in [0,1000,4095]:
            self.bus_comm.set_singal("propulsioncan","BecmPropFr12", 'HvBattChrgnPwrCns800', signal_value)
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","chargingPower"],target_value=signal_value*100,timeout=15
            )
        sleep(1)
        self.sd_tester.write_multi_ccp({950:1})
        self.sd_tester.write_multi_ccp({962:0})

    
    @allure.title("动力电池电压满足0.25V精度组包")
    @pytest.mark.full
    @pytest.mark.v210
    def test_charg_voltage_caseid_1993534(self):
        '''满足0.25V精度组包 '''
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr01","HvBattUDc",0)
        sleep(1)
        for signal_value in [240,241,400,401]:
            self.bus_comm.set_singal("propulsioncan","BecmPropFr01","HvBattUDc",signal_value)
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["batteryInfo","voltage"],target_value=signal_value*0.25,timeout=14) 



    @allure.title("获取和通知动力电池充电功率")
    @pytest.mark.sanity
    @pytest.mark.v220
    def test_caseid_1995974(self):
        self.sd_tester.write_multi_ccp({950:2})
        self.sd_tester.write_multi_ccp({962:2})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.ACCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr12", 'HvBattChrgnPwrCns800', 100.0)
        sleep(1)
        for signal_value in [0,1000,4095]:
            self.bus_comm.set_singal("propulsioncan","BecmPropFr12", 'HvBattChrgnPwrCns800', signal_value)
            self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","chargingPower"],target_value=signal_value*100,timeout=15
            )
        sleep(1)
        self.sd_tester.write_multi_ccp({950:1})
        self.sd_tester.write_multi_ccp({962:0})   

    
