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
        pass

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

    
    @pytest.mark.sanity
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1350904?projectId=46',
        name='RVS case 1350904',
    )
    def test_epb_status_caseid_1981198(self):
        epb_status = {
            # "EpbResd0": 0,
            # "EpbResd1": 1,
            # "EpbResd2": 2,
            3: 3,
            # "EpbResd4": 4,
            5: 5,
            6: 6,
            # "EpbResd7": 7,
            # "EpbResd8": 8,
            9: 9,
            10: 10,
            # "EpbResd11": 11,
            12: 12,
            # "EpbResd13": 13,
            # "EpbResd14": 14,
            # "EpbError": 15,
        }
        self.bus_comm.set_epb_sts(9)
        for key in epb_status:
            self.bus_comm.set_epb_sts(epb_status[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.DrivingStatus, keys=["epb", "status"], target_value=key,sleep_time=15)
            
    
    
    @pytest.mark.sanity
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1493664?projectId=46',
        name='RVS case 109758',
    )
    def test_drvrbelt_status_caseid_109758(self):
        drvrbelt_status = {
            "BeltStatusBeltLocked": BltLockSts.Lock,
            "BeltStatusBeltUnlock": BltLockSts.Unlock,
        }
        self.bus_comm.set_blt_sts(seat_id=SeatId.FrontLeft, blt_flt_sts=BltFltSts.NoFault,
                                      blt_lock_sts=BltLockSts.Unlock)
        sleep(1)
        for key in drvrbelt_status:
            self.bus_comm.set_blt_sts(seat_id=SeatId.FrontLeft, blt_flt_sts=BltFltSts.NoFault,
                                      blt_lock_sts=drvrbelt_status[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.DrivingStatus, keys=["seatBeltStatusInfo", "beltSeatId==0","beltStatus"], target_value=getattr(BeltStatusRvs, key).value)

    @pytest.mark.full
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1493665?projectId=46',
        name='RVS case 109768',
    )
    def test_passbelt_status_caseid_109768(self):
        passbelt_status = {
            "BeltStatusBeltLocked": BltLockSts.Lock,
            "BeltStatusBeltUnlock": BltLockSts.Unlock,
        }
        self.bus_comm.set_blt_sts(seat_id=SeatId.FrontRight, blt_flt_sts=BltFltSts.NoFault,
                                      blt_lock_sts=BltLockSts.Unlock)
        sleep(1)
        for key in passbelt_status:
            self.bus_comm.set_blt_sts(seat_id=SeatId.FrontRight, blt_flt_sts=BltFltSts.NoFault,
                                      blt_lock_sts=passbelt_status[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.DrivingStatus, keys=["seatBeltStatusInfo", "beltSeatId==1","beltStatus"], target_value=getattr(BeltStatusRvs, key).value)

    @pytest.mark.full
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1493666?projectId=46',
        name='RVS case 109729',
    )
    def test_seclebelt_status_caseid_109729(self):
        seclebelt_status = {
            "BeltStatusBeltLocked": BltLockSts.Lock,
            "BeltStatusBeltUnlock": BltLockSts.Unlock,
        }
        self.bus_comm.set_blt_sts(seat_id=SeatId.RearLeft, blt_flt_sts=BltFltSts.NoFault,
                                      blt_lock_sts=BltLockSts.Unlock)
        sleep(1)
        for key in seclebelt_status:
            self.bus_comm.set_blt_sts(seat_id=SeatId.RearLeft, blt_flt_sts=BltFltSts.NoFault,
                                      blt_lock_sts=seclebelt_status[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.DrivingStatus, keys=["seatBeltStatusInfo","beltSeatId==4", "beltStatus"], target_value=getattr(BeltStatusRvs, key).value)

    @pytest.mark.full
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1493667?projectId=46',
        name='RVS case 109725',
    )
    def test_secmidbelt_status_caseid_109725(self):
        secmidbelt_status = {
            "BeltStatusBeltLocked": BltLockSts.Lock,
            "BeltStatusBeltUnlock": BltLockSts.Unlock,
        }
        self.bus_comm.set_blt_sts(seat_id=SeatId.RearMiddle, blt_flt_sts=BltFltSts.NoFault,
                                      blt_lock_sts=BltLockSts.Unlock)
        sleep(1)
        for key in secmidbelt_status:
            self.bus_comm.set_blt_sts(seat_id=SeatId.RearMiddle, blt_flt_sts=BltFltSts.NoFault,
                                      blt_lock_sts=secmidbelt_status[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.DrivingStatus, keys=["seatBeltStatusInfo","beltSeatId==5", "beltStatus"], target_value=getattr(BeltStatusRvs, key).value)

    @pytest.mark.full
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1493668?projectId=46',
        name='RVS case 109808',
    )
    def test_secribelt_status_caseid_109808(self):
        secribelt_status = {
            "BeltStatusBeltLocked": BltLockSts.Lock,
            "BeltStatusBeltUnlock": BltLockSts.Unlock,
        }
        self.bus_comm.set_blt_sts(seat_id=SeatId.RearRight, blt_flt_sts=BltFltSts.NoFault,
                                      blt_lock_sts=BltLockSts.Unlock)
        sleep(1)
        for key in secribelt_status:
            self.bus_comm.set_blt_sts(seat_id=SeatId.RearRight, blt_flt_sts=BltFltSts.NoFault,
                                      blt_lock_sts=secribelt_status[key])
            self.tsp.check_rvs_data_update_new(block=BlockName.DrivingStatus, keys=["seatBeltStatusInfo", "beltSeatId==6","beltStatus"], target_value=getattr(BeltStatusRvs, key).value)


        
    @pytest.mark.sanity
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1493663?projectId=46',
        name='RVS case 1493663',
    )
    def test_brakepedal_status_caseid_109800(self):
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00", 'BrkPedlPsdBrkPedlPsd', 1)
        sleep(1)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00", 'BrkPedlPsdBrkPedlPsd', 0)
        self.tsp.check_rvs_data_update_new(
            BlockName.DrivingStatus,["pedalInfo", "pedalId==1","pressedStatus"],target_value=0
        )
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00", 'BrkPedlPsdBrkPedlPsd', 1)
        self.tsp.check_rvs_data_update_new(
            BlockName.DrivingStatus,keys=["pedalInfo","pedalId==1", "pressedStatus"], target_value=1
        )


    @pytest.mark.full
    def test_accpedal_status_caseid_109722(self):
        self.bus_comm.set_singal("chassiscan2","EcmChas2Fr04",'AccrPedlPsdAccrPedlPsd',0)
        sleep(1)
        self.bus_comm.set_singal("chassiscan2","EcmChas2Fr04",'AccrPedlPsdAccrPedlPsd',1)
        self.tsp.check_rvs_data_update_new(
            BlockName.DrivingStatus,keys=["pedalInfo","pedalId==0", "pressedStatus"], target_value=1
        )
    
    # @pytest.mark.sanity
    # def test_gear_status_caseid_1918795(self):
    #     self.bus_comm.set_gear_pos(gear=Gear.Park)
    #     sleep(1)
    #     self.bus_comm.set_gear_pos(gear=Gear.Rvs)
    #     self.tsp.check_rvs_data_update_new(BlockName.DrivingStatus,keys=["gearLevel"], target_value=1,sleep_time=15)
    #     sleep(1)
    #     self.bus_comm.set_gear_pos(gear=Gear.Neut)
    #     self.tsp.check_rvs_data_update_new(BlockName.DrivingStatus,keys=["gearLevel"], target_value=2,sleep_time=15)
    #     sleep(1)
    #     self.bus_comm.set_gear_pos(gear=Gear.Drv)
    #     self.tsp.check_rvs_data_update_new(BlockName.DrivingStatus,keys=["gearLevel"], target_value=3,sleep_time=15)
    #     sleep(1)
    #     self.bus_comm.set_gear_pos(gear=Gear.Park)
    #     self.tsp.check_rvs_data_update_new(BlockName.DrivingStatus,keys=["gearLevel"], target_value=0,sleep_time=15)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr03", 'GearLvrIndcn', 0)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr18", 'TrsmParkLockdTrsmParkLockd', 0)
    #     sleep(1)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr03",'GearLvrIndcn', 1)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr18", 'TrsmParkLockdTrsmParkLockd', 1)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
    #     self.tsp.check_rvs_data_update_new(BlockName.DrivingStatus,keys=["gearLevel"], target_value=1,sleep_time=15)
    #     sleep(1)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr18", 'TrsmParkLockdTrsmParkLockd', 0)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr03", 'GearLvrIndcn', 3)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
    #     self.tsp.check_rvs_data_update_new(BlockName.DrivingStatus,keys=["gearLevel"], target_value=3,sleep_time=15)
    #     sleep(1)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr18", 'TrsmParkLockdTrsmParkLockd', 1)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr03", 'GearLvrIndcn', 2)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
    #     self.tsp.check_rvs_data_update_new(BlockName.DrivingStatus,keys=["gearLevel"], target_value=2,sleep_time=15)
    #     sleep(1)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr18", 'TrsmParkLockdTrsmParkLockd', 0)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr03", 'GearLvrIndcn', 0)
    #     self.tsp.check_rvs_data_update_new(BlockName.DrivingStatus,keys=["gearLevel"], target_value=0,sleep_time=15)

    @pytest.mark.full
    def test_HodSts_caseid_109793(self):
        HodSts = [0,1,2]
        self.bus_comm.set_singal("cem_lin4","HodDim_Lin1Fr04", 'HandsOnDetectionHandsOnStatus', 1)
        self.bus_comm.set_singal("cem_lin4","HodDim_Lin1Fr04", 'HandsOnDetectionErrorStatus', 2)
        sleep(1)
        for key in HodSts:
            self.bus_comm.set_singal("cem_lin4","HodDim_Lin1Fr04", 'HandsOnDetectionHandsOnStatus',key)
            self.tsp.check_rvs_data_update_new(BlockName.DrivingStatus,keys=["handsOFFStatusInfo","handsOnStatus"], target_value=key)
    
    # @pytest.mark.sanity
    # @allure.testcase(
    #     'https://jama.jiduauto.com/perspective.req#/testCases/1350905?projectId=46',
    #     name='RVS case 1350905',
    # )
    # def test_gear_status_caseid_1918795(self):
    #     self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt",3)
    #     self.sd_tester.update_serverdoipid(0x1002)
    #     time.sleep(3)
    #     for um in [13, 11]:
    #         logger.info(self.sd_tester.change_usage_mode(um))
    #         for i in range(0, 2):
    #             self.bus_comm.set_singal(
    #                 "propulsioncan","EcmPropComFr10",
    #                 'TrsmParkLockdTrsmParkLockd',
    #                 i,
    #             )
    #             for j in range(0, 8):
    #                 self.bus_comm.set_singal(
    #                     "propulsioncan","EcmPropFr24",
    #                     'GearLvrIndcn',
    #                     j,
    #                 )
    #                 logger.info(
    #                     "TrsmParkLockdTrsmParkLockd: {0}, GearLvrIndcn: {1}, um: {2}".format(
    #                         i, j, um
    #                     )
    #                 )
    #                 if j == 0:
    #                     if i in [0, 1]:
    #                         self.tsp.check_rvs_data_update_new(
    #                             BlockName.DrivingStatus,["gearLevel"], "GearLevelP", timeout=5
    #                         )
    #                     # else:
    #                     #     self.tsp.check_rvs_data_update_new(BlockName.DrivingStatus,["gearLevel"], "GearLevelNA")
    #                 elif j == 1:
    #                     if i in [0, 1]:
    #                         self.tsp.check_rvs_data_update_new(
    #                             BlockName.DrivingStatus,["gearLevel"], "GearLevelR", timeout=5
    #                         )
    #                     # else:
    #                     #     self.tsp.check_rvs_data_update_new(BlockName.DrivingStatus,["gearLevel"], "GearLevelNA")
    #                 elif j == 2:
    #                     if i in [0, 1]:
    #                         self.tsp.check_rvs_data_update_new(
    #                             BlockName.DrivingStatus,["gearLevel"], "GearLevelN", timeout=5
    #                         )
    #                     # else:
    #                     #     self.tsp.check_rvs_data_update_new(BlockName.DrivingStatus,["gearLevel"], "GearLevelNA")
    #                 elif j == 3:
    #                     if i in [0, 1]:
    #                         self.tsp.check_rvs_data_update_new(
    #                             BlockName.DrivingStatus,["gearLevel"], "GearLevelD", timeout=5
    #                         )
    #                     # else:
    #                     #     self.tsp.check_rvs_data_update_new(BlockName.DrivingStatus,["gearLevel"], "GearLevelNA")
    #                 elif j == 7:
    #                     if i == 1:
    #                         self.tsp.check_rvs_data_update_new(
    #                             BlockName.DrivingStatus,["gearLevel"], "GearLevelP", timeout=5
    #                         )
  
    #     gear_level = self.rvs_client.get_rvs_data_from_cloud(10106)["gearLevel"]
    #     logger.info(self.sd_tester.change_usage_mode(1))
    #     for m in [1, 3]:
    #         for n in [0, 1]:
    #             self.bus_comm.set_singal(
    #                 "propulsioncan","EcmPropFr24",
    #                 'GearLvrIndcn',
    #                 m,
    #             )
    #             self.bus_comm.set_singal(
    #                 "propulsioncan","EcmPropComFr10",
    #                 'TrsmParkLockdTrsmParkLockd',
    #                 n,
    #             )
    #             self.tsp.check_rvs_data_update_new(BlockName.DrivingStatus,["gearLevel"], gear_level)



    # @pytest.mark.acc
    # @pytest.mark.smoke
    # @allure.testcase(
    #     'https://jama.jiduauto.com/perspective.req#/testCases/1493663?projectId=46',
    #     name='RVS case 1493663',
    # )
    # def test_accpedal_status_caseid_109722(self):
    #     self.ipdu.chassiscan2_ecmchas2fr04_accrpedlpsdaccrpedlpsd_noyes1_no()
    #     self.ipdu.chassiscan2_ecmchas2fr04_accrpedlpsdsts_noyes1_no()
    #     self.tsp.check_rvs_data_update_new(
    #         BlockName.DrivingStatus,["pedalInfo", "pedalId"], "PedalIdPedalAcc", index=0
    #     )
    #     self.tsp.check_rvs_data_update_new(
    #         BlockName.DrivingStatus,["pedalInfo", "pressedStatus"], "PedalReleased", index=0
    #     )
    #     self.ipdu.chassiscan2_ecmchas2fr04_accrpedlpsdaccrpedlpsd_noyes1_no()
    #     self.ipdu.chassiscan2_ecmchas2fr04_accrpedlpsdsts_noyes1_yes()
    #     self.tsp.check_rvs_data_update_new(
    #         BlockName.DrivingStatus,["pedalInfo", "pedalId"], "PedalIdPedalAcc", index=0
    #     )
    #     self.tsp.check_rvs_data_update_new(
    #         BlockName.DrivingStatus,["pedalInfo", "pressedStatus"], "PedalReleased", index=0
    #     )
    #     self.ipdu.chassiscan2_ecmchas2fr04_accrpedlpsdaccrpedlpsd_noyes1_yes()
    #     self.ipdu.chassiscan2_ecmchas2fr04_accrpedlpsdsts_noyes1_yes()
    #     self.tsp.check_rvs_data_update_new(
    #         BlockName.DrivingStatus,["pedalInfo", "pedalId"], "PedalIdPedalAcc", index=0
    #     )
    #     self.tsp.check_rvs_data_update_new(
    #         BlockName.DrivingStatus,["pedalInfo", "pressedStatus"], "PedalPressed", index=0
    #     )
    #     self.ipdu.chassiscan2_ecmchas2fr04_accrpedlpsdaccrpedlpsd_noyes1_yes()
    #     self.ipdu.chassiscan2_ecmchas2fr04_accrpedlpsdsts_noyes1_no()
    #     self.tsp.check_rvs_data_update_new(
    #         BlockName.DrivingStatus,["pedalInfo", "pedalId"], "PedalIdPedalAcc", index=0
    #     )
    #     self.tsp.check_rvs_data_update_new(
    #         BlockName.DrivingStatus,["pedalInfo", "pressedStatus"], "PedalPressed", index=0
    #     )


    # @pytest.mark.acc
    # @pytest.mark.full
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1493663?projectId=46',name='RVS case 1493663',)
    # def test_accpedal_status_caseid_109722(self):
    #     self.bus_comm.set_door_opener_sts(DoorOpenerSts.FullClsd)
    #     self.bus_comm.set_gear_pos(Gear.Drv)
    #     self.mix.set_usage_mode(UsageMode.DRIVING)
    #     self.bus_comm.set_accr_pedl_press_act(isOn.On)
    #     self.bus_comm.set_accr_pedl_press_sts(isOn.On)
    #     self.tsp.check_rvs_data_update_new(block=BlockName.DrivingStatus,keys=["pedalInfo", "pedalId"],target_value="PedalIdPedalAcc")
    #     self.tsp.check_rvs_data_update_new(block=BlockName.DrivingStatus,keys=["pedalInfo", "pressedStatus"],target_value="PedalPressed")