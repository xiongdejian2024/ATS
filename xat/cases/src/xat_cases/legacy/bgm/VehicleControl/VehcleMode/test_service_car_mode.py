# -*- coding: utf-8 -*-
"""
@File        : test_soa_bonnet.py
@Author      : hui.zhao@jiduatuo.com
@Time        : 2023/05/10 15:00 PM
@Description : Test s2s interface about bonnet function
"""

import os
import sys
from time import sleep
import pytest
import allure
from random import randint
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
sys.path.append(os.path.join(os.getcwd(), "../../../.."))

from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.common.logger import logger
# from test_case.soa.case_helper.partner_const import *
from xat_ecu.legacy.sdk.bus_app import BusApp
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *

class CarMode(object):
    NORMAL = 0
    TRANSPORT = 1
    FACTORY = 2
    CRASH = 3
    DYNO = 5

class UsageMode(object):
    INACTIVE = 1
    CONVENIENCE = 2
    ACTIVE = 11
    DRIVING = 13
    ABANDONED = 0
USAGE_MODE_MAP = {
    0: "ABANDONED",
    1: "INACTIVE",
    2: "CONVENIENCE",
    11: "ACTIVE",
    13: "DRIVING",
}
CAR_MODE_MAP = {
    0: "NORMAL",
    1: "TRANSPORT",
    2: "FACTORY",
    3: "CRASH",
    5: "DYNO",
}


@allure.feature("架构基础")
@allure.story("整车模式/车辆模式")
class TestVehicleModeService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        # self.nucapp.bgm_diag_line_up()
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.sd_tester.tester_present()
        self.ipdu.set_vehspd(0.0)
        partner_process_check()
        sleep(1)
        # self.bgm_tcpdump = BgmTcpdump()
        # self.bgm_tcpdump.init_bgm_tcpdump()
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟(数据库周期性报文和调度表)
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        self.s2sbaseclass = S2sBaseClass([("VehicleModeService", "client")])


    def before_each_func(self, ecu):
        super().before_each_func(ecu,start=False)
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 0
        )
        self.ipdu.set_vehspd(0.0)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0
        )
        time.sleep(1)
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client',
            'SetCarMode',
            {"mode": 0},
        )
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr02 ,'VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02','CarModSts1_CarModNorm')
        time.sleep(0.3)
        self.ipdu.check(
             self.ipdu.backbonefr.CemBackBoneFr02 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_0_CEMBackBoneSignalIpdu02',0)
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client',
            'SetUsageModeDown',
            {"mode": 1},)
        time.sleep(1)
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModInActv',
        )        
        time.sleep(1)
        
    def after_each_func(self, ecu):
        self.dk.set_central_lock(0x1)
        super().after_each_func(ecu,start=False)
 
    def after_class(self, ecu):
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client',
            'SetUsageModeDown',
            {"mode": 1},
        )
        time.sleep(1)
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client',
            'SetCarMode',
            {"mode": 0},
        )
        time.sleep(1)
        # self.nucapp.bgm_diag_line_down()
        self.ipdu.time_control_stop()  
        self.busapp.stop_all_cyclic_msgs()  
        self.sd_tester.stop_tester_present()
        self.s2sbaseclass.stop_operators()
        partner_process_check()
        # self.bgm_tcpdump.stop_bgm_tcpdump()
        super().after_class(self, ecu)

    def check_usage_mode_status(self, expectedmode, do_assert=True, **kwargs):
        '''
        校验 usage 状态
        @param expectedmode:
        @param do_assert:
        @param timeout:
        @param kwargs:
        @return:
        '''
        timeout = kwargs.get('timeout', 5)
        msg_signals_obj = kwargs.get('msg_signals_obj', self.ipdu.bodycan.CEMBodyFr12)
        signal_name = kwargs.get(
            'signal_name', 'VehModMngtGlbSafe1UsgModSts_3_CEMBodySignalIPdu12'
        )
        # msg_signals_obj = kwargs.get('msg_signals_obj', self.ipdu.backbonefr.CemBackBoneFr02)
        # signal_name = kwargs.get(
        #     'signal_name', 'VehModMngtGlbSafe1UsgModSts_0_CEMBackBoneSignalIpdu02'
        # )
        # logging.info(msg_signals_obj)
        # logging.info(signal_name)
        result, realvalue, expectedvalue = self.ipdu.check(
            msg_signals_obj=msg_signals_obj,
            signal_name=signal_name,
            sig_value_name=expectedmode,
            do_assert=do_assert,
            timeout=timeout,
        )

        return result, realvalue, expectedvalue

    def partner_change_mode(self, method_name, method_par, **kwargs):
        '''
        通过服务切换 模式
        @param method_name:
        @param method_par:
        @param kwargs:
        @return:
        '''
        try:
            self.s2sbaseclass.send_method_request(
                'VehicleModeService_client',
                method_name,
                method_par,
            )
        except Exception as e:
            logger.error(f"{method_name} 服务调用失败>>{str(e)}")

    # @staticmethod
    def service_change_usage_mode_and_check_result(
        self, usage_mode, do_assert=True, **kwargs
    ):
        '''
        通过s2s 切换 us mode
        '''
        # 先获取下 当前模式
        result, curren_usage_mode, expectedvalue = self.check_usage_mode_status(
            expectedmode=usage_mode, do_assert=False
        )
        curr_usage_mode_name = USAGE_MODE_MAP.get(curren_usage_mode)
        logger.info(f"当前模式为 为{curr_usage_mode_name}:{curren_usage_mode}")
        if curren_usage_mode < usage_mode:
            self.set_lockunlock()
            # self.dk.set_single_digital_key_connect_info(1) #钥匙在车内
            #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
            method_name = "SetUsageModeUp"
        elif curren_usage_mode > usage_mode:
            method_name = "SetUsageModeDown"
        else:
            # 已经是所需要模式，无需切换，直接返回
            return 1, curren_usage_mode, curren_usage_mode
        # 如果切到driving 模式以后 不设置为0 则切不成功
        self.ipdu.backbonefr_vddmbackbonefr00_engst1wdstsengst1wdsts_engst1_ini()
        # 设置 同星信号
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        usage_mode_name = USAGE_MODE_MAP.get(usage_mode)
        logger.info(f"设置usage_mode_name 为{usage_mode_name}:{usage_mode}")
        logger.info(f"Step:调用 {method_name}(mode:{usage_mode}))")

        method_par = {"mode": usage_mode}
        self.partner_change_mode(method_name, method_par)

        logger.info(f"验证切换结果是否为{usage_mode_name}:{usage_mode}")
        result, realvalue, expectedvalue = self.check_usage_mode_status(
            expectedmode=usage_mode, do_assert=False
        )

        string = f" 切换前为{curr_usage_mode_name}，切换后本应为 {USAGE_MODE_MAP.get(usage_mode)} 实际为 {USAGE_MODE_MAP.get(realvalue)}"
        logger.info(string)
        if do_assert and not result:
            string = f" 本应为 {USAGE_MODE_MAP.get(usage_mode)} 实际为 {USAGE_MODE_MAP.get(realvalue)}"
            logger.error(string)
            assert 0, string
        return result, realvalue, expectedvalue

    # def change_usage_mode_driving(self):
    #     # self.dk.set_internal_no_key()
    #     self.set_lock()
    #     self.dk.set_cenlock_sts(0x1)
    #     # self.dk.set_internal_has_key()
    #     self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5)
    #     time.sleep(1)
    #     self.ipdu.check(self.ipdu.bodycan.CEMBodyFr30, 'EngSt1WdStsEngSt1WdSts_1_CEMBodySignalIPdu30',5)
    #     self.check_usage_mode_status(13)
    
    def change_usage_mode_driving(self):
        '''切driving'''
        # self.set_lockunlock()
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        time.sleep(.5)
        # self.ipdu.backbonefr_vddmbackbonefr00_engst1wdstsengst1wdsts_engst1_runngrunng()
        self.check_usage_mode_status(UsageMode.DRIVING)

    # def change_inactive_driving(self):
    #     self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
    #     self.dk.set_cenlock_sts(0x3)
    #     time.sleep(1)
    #     self.dk.set_cenlock_sts(0x1)
    #     self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)

    def reset_bgm(self):
        self.nucapp.bgm_power_off()
        time.sleep(1)
        self.nucapp.bgm_power_on()
        time.sleep(15)
    
    def set_lockunlock(self):
        # self.ipdu.pause_all_bus_send()
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
        # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
        # self.ipdu.backbonefr_vddmbackbonefr03_gearlvrindcn_gearlvrindcn2_parkindcn()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 0)
        self.dk.set_drvr_seat_notpresent()
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        time.sleep(.3)
        self.io.set_four_door_close()
        self.io.trunk_door_close()
        self.io.hood_door1_close()
        time.sleep(.3)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02,'DoorDrvrSts_2_CemBodySignalIPdu02', 2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'DoorPassSts_2_CEMBodySignalIPdu11', 2)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02,'DoorLeReSts_1_CemBodySignalIPdu02', 2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'DoorRiReSts_1_CEMBodySignalIPdu11', 2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'TrSts_2_CEMBodySignalIPdu11', 2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06,'HoodSts', 2)
        self.dk.set_cenlock_sts(0x3)
        sleep(1)
        # self.dk.send_nfc_cmd()
        self.dk.set_cenlock_sts(0x1)
        # self.ipdu.resume_all_bus_send()

    def set_lock(self):
        # self.ipdu.pause_all_bus_send()
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
        time.sleep(.5)
        # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
        # self.ipdu.backbonefr_vddmbackbonefr03_gearlvrindcn_gearlvrindcn2_parkindcn()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 0)
        # self.sd_tester.write_multi_ccp({94: 0x80, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x4, 578: 0x4})
        self.dk.set_drvr_seat_notpresent()
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        time.sleep(.3)
        self.io.set_four_door_close()
        self.io.trunk_door_close()
        self.io.hood_door1_close()
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02,'DoorDrvrSts_2_CemBodySignalIPdu02', 2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'DoorPassSts_2_CEMBodySignalIPdu11', 2)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02,'DoorLeReSts_1_CemBodySignalIPdu02', 2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'DoorRiReSts_1_CEMBodySignalIPdu11', 2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'TrSts_2_CEMBodySignalIPdu11', 2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06,'HoodSts', 2)

        # self.ipdu.check(self.ipdu.propulsioncan.EcmPropComFr10,'TrsmParkLockdTrsmParkLockd', 1)
        time.sleep(.3)
        self.dk.set_cenlock_sts(0x3)
        sleep(1)
        # self.ipdu.resume_all_bus_send()
    
    def set_usage_mode_to_abandoned(self, wait_time=180, do_assert=True, **kwargs):
        '''
        进入 abandoned 模式
        @param wait_time:  关闭四门两盖以后，中控锁上锁后，最长等待时间
        @param do_assert: 为true   进入失败则会报错，为False 则不会报错，返回当前模式
        @param kwargs:
        @return:
        '''
        lin_channel = kwargs.get("lin_channel", "cem_lin6")
        lin_id = kwargs.get("lin_id", 0x06)
        lin_msg = kwargs.get("lin_msg", [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
        logger.info("断开诊断激活线")
        # self.nucapp.bgm_diag_line_down()
        # self.nucapp.bgm_diag_line_down()
        self.nucapp.bgm_power_off()
        time.sleep(3)
        self.nucapp.bgm_power_on()
        time.sleep(20)
        # 2 发送lin 报文 补电
        self.ipdu.set(self.ipdu.cem_lin6.CemCem_Lin6Fr02, "BattSnsrStReq", 1)
        # ipdu.send_pdu("cem_lin6", 0x06, [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
        self.ipdu.send_pdu(lin_channel, lin_id, lin_msg)
        # 3. 四门两盖关闭
        logger.info("关闭四门两盖")
        self.io.drvr_door_close()
        self.io.lere_door_close()
        self.io.pass_door_close()
        self.io.rire_door_close()
        self.io.trunk_door_close()
        self.io.hood_door1_close()
        # 四门两盖是否关闭
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02,'DoorDrvrSts_2_CemBodySignalIPdu02', 2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'DoorPassSts_2_CEMBodySignalIPdu11', 2)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02,'DoorLeReSts_1_CemBodySignalIPdu02', 2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'DoorRiReSts_1_CEMBodySignalIPdu11', 2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'TrSts_2_CEMBodySignalIPdu11', 2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06,'HoodSts', 2)
        # 4. 闭锁
        self.dk.set_cenlock_sts(0x3)
        t1 = time.time()
        # 等待一定时间
        logger.info(f"最长等待{wait_time}秒,让 bgm 进入abandoned 模式，超过时间未进入则退出")
        t1 = time.time()
        realvalue = None
        while time.time() - t1 < wait_time:
            result, realvalue, expectedvalue = self.check_usage_mode_status(expectedmode=UsageMode.ABANDONED,
                                                                            do_assert=False)
            logger.info(f"当前模式为{USAGE_MODE_MAP.get(realvalue)}期望模式为{USAGE_MODE_MAP.get(expectedvalue)}")
            #
            if result:
                # 进入
                logger.info(f"成功进入 abandoned 状态耗时{time.time() - t1}s")
                return True
        else:
            if do_assert:
                assert 0, "进入abandoned  失败"
            return False

    def check_car_mode_status(self, expectedmode, do_assert=True, **kwargs):
            timeout = kwargs.get('timeout', 5)
            msg_signals_obj = kwargs.get('msg_signals_obj', self.ipdu.bodycan.CEMBodyFr12)
            signal_name = kwargs.get('signal_name', 'VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12')
            # msg_signals_obj = kwargs.get('msg_signals_obj', self.ipdu.backbonefr.CemBackBoneFr02)
            # signal_name = kwargs.get('signal_name', 'VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02')
            result, realvalue, expectedvalue = self.ipdu.check(msg_signals_obj=msg_signals_obj,
                                                            signal_name=signal_name,
                                                            sig_value_name=expectedmode,
                                                            do_assert=do_assert, timeout=timeout, )
            return result, realvalue, expectedvalue
    
    # @staticmethod
    def s2s_change_car_mode_and_check_result(self, car_mode, **kwargs):
        '''
        通过s2s 切换 car mode
        '''
        car_mode_name = CAR_MODE_MAP.get(car_mode)
        logger.info(f"设置car mode 为{car_mode_name}:{car_mode}")
        logger.info(
            f"Step:调用 SetCarMode:(服务:BonnetService;函数名:set:SetCarMode(mode:{car_mode}))"
        )
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client',
            'SetCarMode',
            {"mode": car_mode},
        )
        logger.info(f"验证切换结果是否为{car_mode_name}:{car_mode}")
        self.check_car_mode_status(expectedmode=car_mode)
    
    def s2s_change_car_mode_fail_and_check_result(self, car_mode, car_mode1, **kwargs):
        '''
        通过s2s 切换 car mode
        '''
        car_mode_name = CAR_MODE_MAP.get(car_mode)
        car_mode_name1 = CAR_MODE_MAP.get(car_mode1)
        logger.info(f"设置car mode 为{car_mode_name}:{car_mode}")
        logger.info(
            f"Step:调用 SetCarMode:(服务:BonnetService;函数名:set:SetCarMode(mode:{car_mode}))"
        )
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client',
            'SetCarMode',
            {"mode": car_mode},
        )
        logger.info(f"验证切换结果是否为{car_mode_name1}:{car_mode1}")
        self.check_car_mode_status(expectedmode=car_mode1)

    @pytest.mark.smoke
    @pytest.mark.verify
    @pytest.mark.mcu_test
    def test_vehicle_mode_service_caseid_1918590(self):
        '''
        110098
        normal to factory
        '''
        self.dk.set_central_lock(0x1)
        self.s2s_change_car_mode_and_check_result(CarMode.FACTORY)

    @pytest.mark.smoke
    @pytest.mark.mcu_test
    def test_vehicle_mode_service_caseid_1918589(self):
        '''
        normal to transport
        '''
        self.dk.set_central_lock(0x1)
        self.s2s_change_car_mode_and_check_result(CarMode.TRANSPORT)

    @pytest.mark.smoke
    @pytest.mark.mcu_test
    def test_vehicle_mode_service_caseid_1918591(self):
        '''
        normal to factory
        '''
        self.set_lockunlock()
        self.s2s_change_car_mode_fail_and_check_result(CarMode.FACTORY, CarMode.NORMAL)

    # @pytest.mark.xfail
    # @pytest.mark.full
    # def test_vehicle_mode_service_caseid_1740916(self):
    #     '''
    #     crash 不能用服务接口切
    #     '''
    #     self.s2s_change_car_mode_fail_and_check_result(CarMode.CRASH, CarMode.NORMAL)

    @pytest.mark.smoke
    @pytest.mark.mcu_test
    def test_vehicle_mode_service_caseid_1918594(self):
        '''
        normal to dyno
        '''
        self.s2s_change_car_mode_and_check_result(CarMode.DYNO)

    # @pytest.mark.full
    # def test_vehicle_mode_service_caseid_1740918(self):
    #     '''
    #     normal to normal
    #     '''
    #     self.s2s_change_car_mode_and_check_result(CarMode.NORMAL)

    @pytest.mark.smoke
    @pytest.mark.mcu_test
    def test_vehicle_mode_service_caseid_1918584(self):
        '''
        transport to normal
        '''
        self.s2s_change_car_mode_and_check_result(CarMode.TRANSPORT)
        time.sleep(1)
        self.s2s_change_car_mode_and_check_result(CarMode.NORMAL)

    @pytest.mark.smoke
    @pytest.mark.mcu_test
    def test_vehicle_mode_service_caseid_1918596(self):
        '''
        dyno to normal
        '''
        self.s2s_change_car_mode_and_check_result(CarMode.DYNO)
        time.sleep(1)
        self.s2s_change_car_mode_and_check_result(CarMode.NORMAL)

    @pytest.mark.smoke
    @pytest.mark.mcu_test
    def test_vehicle_mode_service_caseid_1918595(self):
        '''
        factory to normal
        '''
        self.dk.set_central_lock(0x1)
        self.s2s_change_car_mode_and_check_result(CarMode.FACTORY)
        time.sleep(1)
        self.s2s_change_car_mode_and_check_result(CarMode.NORMAL)

    @pytest.mark.smoke
    # @pytest.mark.xfail
    @pytest.mark.full
    @pytest.mark.mcu_test
    def test_vehicle_mode_service_caseid_1918587(self):
        """
        不满足条件normal not to transport
        AlrmSts != Disarmed
        """
        self.set_lock()
        sleep(1)
        self.s2s_change_car_mode_fail_and_check_result(CarMode.TRANSPORT, CarMode.NORMAL)

    @pytest.mark.smoke
    def test_vehicle_mode_service_caseid_1918593(self):
        """
        不满足条件normal  to dyno
        AlrmSts != Disarmed
        """
        self.s2s_change_car_mode_and_check_result(CarMode.NORMAL)
        self.set_lock()
        sleep(1)
        self.s2s_change_car_mode_and_check_result(CarMode.DYNO)

    @pytest.mark.smoke
    def test_vehicle_mode_service_caseid_1918634(self):
        '''
        109939
        不满足条件normal to factory
        Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts ==13 UsgModSts1_UsgModDriving
        '''
        # self.change_usage_mode_driving()
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        time.sleep(.5)
        self.check_usage_mode_status(13)
        self.s2s_change_car_mode_fail_and_check_result(CarMode.FACTORY, CarMode.NORMAL)
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 2
        )

    @pytest.mark.smoke
    def test_vehicle_mode_service_caseid_1918635(self):
        '''
        不满足条件normal to dyno
        Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts ==13 UsgModSts1_UsgModDriving
        '''
        # self.change_usage_mode_driving()
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        time.sleep(.5)
        # self.ipdu.set(
        #     self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        # )
        self.check_usage_mode_status(13)
        self.s2s_change_car_mode_and_check_result(CarMode.DYNO)

    @pytest.mark.smoke
    def test_vehicle_mode_service_caseid_1918630(self):
        '''
        110030
        不满足条件normal to transport
        Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts ==13 UsgModSts1_UsgModDriving
        '''  
        # self.change_usage_mode_driving() 
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        time.sleep(.5)
        self.check_usage_mode_status(13)
        self.s2s_change_car_mode_and_check_result(CarMode.TRANSPORT)  
        self.ipdu.check(
             self.ipdu.backbonefr.CemBackBoneFr02 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_0_CEMBackBoneSignalIpdu02',3
         )

    @pytest.mark.full
    def test_vehicle_mode_service_caseid_109937(self):
        '''
        1.Body_CAN:0x0F0:VehModMngtGlbSafe1CarModSts1== 5 CarModSts1_CarModDyno
        2.BodyCAN:0x040:VehMtnStVehMtnSt_VehMtnSt2 == 1 StandStillVal1 || 2 StandStillVal2 ||3 StandStillVal3
        '''  
        self.s2s_change_car_mode_and_check_result(CarMode.DYNO)
        self.io.set_do_level("hazard_switch", True)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr04,'SwtLiHzrdWarn', 1) 
        self.io.set_do_level("hazard_switch", False)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr04,'SwtLiHzrdWarn', 0)
        self.io.set_do_level("hazard_switch", True)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr04,'SwtLiHzrdWarn', 1)
        self.io.set_do_level("hazard_switch", False)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr04,'SwtLiHzrdWarn', 0)
        time.sleep(1)
        self.check_car_mode_status(0)

    @pytest.mark.sanity
    @pytest.mark.mcu_test
    @pytest.mark.nvm
    def test_factory_storage_recovery_caseid_110113(self):
        '''factory存储与恢复'''
        #factory,transport状态需要有钥匙在
        self.dk.set_cenlock_sts(0x1)
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetUsageModeDown", {"mode": 1}
        )
        self.s2s_change_car_mode_and_check_result(CarMode.FACTORY)
        time.sleep(1)
        self.check_car_mode_status(2)
        
        self.reset_bgm()
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr02 ,'VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02','CarModSts1_CarModFcy'
        )

    @pytest.mark.sanity
    @pytest.mark.mcu_test
    @pytest.mark.nvm
    def test_transport_storage_recovery_caseid_110104(self):
        '''transport存储与恢复'''
        self.s2s_change_car_mode_and_check_result(CarMode.TRANSPORT)
        # self.s2sbaseclass.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetCarMode", {},
        #                                       {"out": 3})
        time.sleep(1)
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr02 ,'VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02','CarModSts1_CarModTrnsp'
        )
        
        self.reset_bgm()
        # self.s2sbaseclass.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetCarMode", {},
        #                                       {"out": 3})
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr02 ,'VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02','CarModSts1_CarModTrnsp'
        )
    

    @pytest.mark.sanity
    @pytest.mark.mcu_test
    @pytest.mark.nvm
    def test_dyno_storage_recovery_caseid_110039(self):
        '''dyno存储与恢复'''
        self.s2s_change_car_mode_and_check_result(CarMode.DYNO)
        # self.s2sbaseclass.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetCarMode", {},
        #                                       {"out": 5})
        time.sleep(1)
        self.check_car_mode_status(5)
        self.reset_bgm()
        # self.s2sbaseclass.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetCarMode", {},
        #                                       {"out": 5})
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr02 ,'VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02','CarModSts1_CarModDyno'
        )   


    @pytest.mark.sanity
    @pytest.mark.mcu_test
    def test_factorypaused_storage_recovery_caseid_110026(self):
        '''factorypaused存储与恢复'''
        self.dk.set_central_lock(0x1)
        self.s2s_change_car_mode_and_check_result(CarMode.FACTORY)
        #双击危险报警灯开关
        self.io.set_do_level("hazard_switch", True)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr04,'SwtLiHzrdWarn', 1) 
        self.io.set_do_level("hazard_switch", False)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr04,'SwtLiHzrdWarn', 0)
        self.io.set_do_level("hazard_switch", True)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr04,'SwtLiHzrdWarn', 1)
        self.io.set_do_level("hazard_switch", False)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr04,'SwtLiHzrdWarn', 0)
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 1
        )
        time.sleep(1)
        self.reset_bgm()
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 0
        )

    @pytest.mark.full
    def test_enter_factorypaused_caseid_110150(self):
        '''进入factorypaused'''
        self.dk.set_central_lock(0x1)
        self.s2s_change_car_mode_and_check_result(CarMode.FACTORY)
        #双击危险报警灯开关
        self.io.set_do_level("hazard_switch", True)
        time.sleep(.3)  
        self.io.set_do_level("hazard_switch", False)
        time.sleep(.3)
        self.io.set_do_level("hazard_switch", True)
        time.sleep(.3)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr04,'SwtLiHzrdWarn', 1)
        self.io.set_do_level("hazard_switch", False)
        time.sleep(.3)
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 1
        )

    @pytest.mark.full
    def test_exit_factorypaused_caseid_110042(self):
        '''退出factorypaused'''
        self.s2s_change_car_mode_and_check_result(CarMode.FACTORY)
        #双击危险报警灯开关
        self.io.set_do_level("hazard_switch", True)
        time.sleep(.3)     
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr04,'SwtLiHzrdWarn', 1)
        self.io.set_do_level("hazard_switch", False)
        time.sleep(.3)
        self.io.set_do_level("hazard_switch", True)
        time.sleep(.3)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr04,'SwtLiHzrdWarn', 1)
        self.io.set_do_level("hazard_switch", False)
        time.sleep(.3)
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 1
        )
        #退出
        time.sleep(120)
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 0
        )
    
    @pytest.mark.full
    def test_exit_factorypaused_caseid_109947(self):
        '''Carmode_双击危险开关重新计时Factory Paused Mode'''
        self.s2s_change_car_mode_and_check_result(CarMode.FACTORY)
        #双击危险报警灯开关
        self.io.set_do_level("hazard_switch", True)
        time.sleep(.3)     
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr04,'SwtLiHzrdWarn', 1)
        self.io.set_do_level("hazard_switch", False)
        time.sleep(.3)
        self.io.set_do_level("hazard_switch", True)
        time.sleep(.3)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr04,'SwtLiHzrdWarn', 1)
        self.io.set_do_level("hazard_switch", False)
        time.sleep(.3)
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 1
        )
        #退出
        time.sleep(30)
        self.io.set_do_level("hazard_switch", True)
        time.sleep(.3)     
        # self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr04,'SwtLiHzrdWarn', 1)
        self.io.set_do_level("hazard_switch", False)
        time.sleep(.3)
        self.io.set_do_level("hazard_switch", True)
        time.sleep(.3)
        # self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr04,'SwtLiHzrdWarn', 1)
        self.io.set_do_level("hazard_switch", False)
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 1
        )
        time.sleep(90)
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 1
        )
        time.sleep(30)
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 0
        )


    @pytest.mark.full
    def test_enter_factorypaused_to_factorydriving_caseid_109943(self):
        '''从factorypaused进入factorydriving'''
        self.s2s_change_car_mode_and_check_result(CarMode.FACTORY)
        #双击危险报警灯开关
        self.io.set_do_level("hazard_switch", True)
        time.sleep(.3)     
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr04,'SwtLiHzrdWarn', 1)
        self.io.set_do_level("hazard_switch", False)
        time.sleep(.3)
        self.io.set_do_level("hazard_switch", True)
        time.sleep(.3)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr04,'SwtLiHzrdWarn', 1)
        self.io.set_do_level("hazard_switch", False)
        time.sleep(.3)
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 1
        )
        #进入factorydriving
        self.set_lock()
        self.dk.set_cenlock_sts(0x1)
        time.sleep(1)        
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetUsageModeUp", {"mode": 11}
        )
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5)
        time.sleep(.5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr30, 'EngSt1WdStsEngSt1WdSts_1_CEMBodySignalIPdu30',5)
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 2
        )

    @pytest.mark.full
    def test_carmode_normal_default_caseid_109934(self):
        '''车辆模式默认状态'''
        self.s2s_change_car_mode_and_check_result(CarMode.NORMAL)
        time.sleep(1)
        self.reset_bgm()
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr02 ,'VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02','CarModSts1_CarModNorm'
        )

    @pytest.mark.sanity
    def test_factorydriving_storage_recovery_caseid_109910(self):
        '''factorydriving存储与恢复'''
        self.set_lock()
        self.dk.set_cenlock_sts(0x1)
        time.sleep(1)        
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetUsageModeUp", {"mode": 11}
        )
        self.s2s_change_car_mode_and_check_result(CarMode.FACTORY)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5)
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 2
        )
        time.sleep(1)
        self.reset_bgm()
        self.check_usage_mode_status(13)
        self.check_car_mode_status(0)
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 2
        )

    @pytest.mark.full
    def test_enter_factorydriving_caseid_109962(self):
        '''进factorydriving'''
        self.set_lock()
        self.dk.set_cenlock_sts(0x1)
        time.sleep(1)        
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetUsageModeUp", {"mode": 11}
        )
        self.s2s_change_car_mode_and_check_result(CarMode.FACTORY)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5)
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 2
        )

    @pytest.mark.full
    def test_exit_factorydriving_caseid_109959(self):
        '''退出factorydriving'''
        self.set_lock()
        self.dk.set_cenlock_sts(0x1)
        time.sleep(1)        
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetUsageModeUp", {"mode": 11}
        )
        self.s2s_change_car_mode_and_check_result(CarMode.FACTORY)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr30, 'EngSt1WdStsEngSt1WdSts_1_CEMBodySignalIPdu30',5)
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 2
        )
        #从driving切换到别的模式退出
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0)
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetUsageModeDown", {"mode": 1}
        )
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 0
        )

    @pytest.mark.sanity
    def test_transportdriving_storage_recovery_caseid_109907(self):
        '''transportdriving存储与恢复'''
        self.set_lock()
        self.dk.set_cenlock_sts(0x1)
        time.sleep(1)        
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetUsageModeUp", {"mode": 11}
        )
        self.s2s_change_car_mode_and_check_result(CarMode.TRANSPORT)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5)
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 3
        )   
        time.sleep(1) 
        self.reset_bgm()
        self.check_usage_mode_status(13)
        # self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5)
        # self.ipdu.check(self.ipdu.bodycan.CEMBodyFr30, 'EngSt1WdStsEngSt1WdSts_1_CEMBodySignalIPdu30',5)
        self.check_car_mode_status(0)
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 3
        ) 

    def test_01(self):
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
    @pytest.mark.full
    def test_exit_transportdriving_caseid_110141(self):
        '''退出transportdriving'''
        self.set_lock()
        self.dk.set_cenlock_sts(0x1)
        time.sleep(1)        
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetUsageModeUp", {"mode": 11}
        )
        self.s2s_change_car_mode_and_check_result(CarMode.TRANSPORT)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5)
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 3
        )   
        #退出
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0)
        self.check_usage_mode_status(11)
        self.check_car_mode_status(1)
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 0
        )

    # @pytest.mark.sanity
    # @pytest.mark.mcu_test
    # def test_crash_storage_recovery_1959794(self):
    #     '''crash存储与恢复'''
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 1)
    #     # self.ipdu.backbonefr_srsbackbonefr05_crashstssafests_crashsts2_crash()
    #     time.sleep(1)
    #     self.ipdu.check(
    #         self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12','CarModSts1_CarModCrash'
    #     )
    #     self.reset_bgm()
    #     self.ipdu.check(
    #         self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12','CarModSts1_CarModCrash'
    #     )
    #     #退出crash
    #     self.ipdu.backbonefr_srsbackbonefr05_crashstssafests_crashsts2_nocrash()
    #     # self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 0)
    #     self.ipdu.backbonefr_vddmbackbonefr26_hvsyscrashfb_crashfb_ok()
    #     # self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr26, 'HvSysCrashFb', 3)
    #     # self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'SafetyCrashFb', 3)
    #     self.ipdu.backbonefr_srsbackbonefr02_safetycrashfb_crashfb_ok()
    #     self.s2sbaseclass.send_method_request(
    #         'VehicleModeService_client', "SetUsageModeDown", {"mode": 1}
    #     )
    #     self.check_usage_mode_status(1)
    #     self.dk.set_internal_no_key()
    #     self.set_lock()
    #     self.dk.set_central_lock(0x1)
    #     self.s2sbaseclass.send_method_request(
    #         'VehicleModeService_client', "SetUsageModeUp", {"mode": 2}
    #     )
    #     self.check_usage_mode_status(2)
    #     self.check_car_mode_status(0)
    
    # @pytest.mark.full
    # @pytest.mark.new
    # def test_crash_storage_recovery_110101(self):
    #     '''crash进入_CrashStsSafeSts'''
    #     # self.s2s_change_car_mode_and_check_result(CarMode.CRASH)
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 1)
    #     self.ipdu.check(
    #         self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12','CarModSts1_CarModCrash'
    #     )
    #     #退出crash
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 0)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr26, 'HvSysCrashFb', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'SafetyCrashFb', 3)
    #     self.s2sbaseclass.send_method_request(
    #         'VehicleModeService_client', "SetUsageModeDown", {"mode": 1}
    #     )
    #     self.check_usage_mode_status(1)
    #     self.dk.set_internal_no_key()
    #     self.set_lock()
    #     self.dk.set_central_lock(0x1)
    #     self.s2sbaseclass.send_method_request(
    #         'VehicleModeService_client', "SetUsageModeUp", {"mode": 2}
    #     )
    #     self.check_usage_mode_status(2)
    #     self.check_car_mode_status(0)

###############################full用例################################################
    @pytest.mark.full
    def test_carmode_transport_to_dyno_caseid_115741(self):
        '''transport to dyno'''
        self.s2s_change_car_mode_and_check_result(CarMode.TRANSPORT)
        time.sleep(1)
        self.s2s_change_car_mode_and_check_result(CarMode.DYNO)
        

    @pytest.mark.full
    def test_transport_driving_caseid_110160(self):
        '''transport driving'''
        self.set_lock()
        self.dk.set_cenlock_sts(0x1)
        time.sleep(1)        
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetUsageModeUp", {"mode": 11}
        )
        self.s2s_change_car_mode_and_check_result(CarMode.TRANSPORT)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5)
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 3
        )
        
    @pytest.mark.full
    def test_dyno_to_transport_caseid_109915(self):
        '''dyno not to transport'''
        self.s2s_change_car_mode_and_check_result(CarMode.DYNO)
        time.sleep(1)
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client',
            'SetCarMode',
            {"mode": 1},
        )
        self.ipdu.check(
             self.ipdu.backbonefr.CemBackBoneFr02 ,'VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02','CarModSts1_CarModDyno'
         )
        
    @pytest.mark.full
    def test_transport_to_factory_caseid_109946(self):
        '''transport to factory'''
        self.s2s_change_car_mode_and_check_result(CarMode.TRANSPORT)
        time.sleep(1)
        self.s2s_change_car_mode_and_check_result(CarMode.FACTORY)
    
    @pytest.mark.full
    # @pytest.mark.xfail
    def test_dyno_to_factory_caseid_110005(self):
        '''dyno to factory'''
        self.s2s_change_car_mode_and_check_result(CarMode.DYNO)
        time.sleep(1)
        self.s2s_change_car_mode_fail_and_check_result(CarMode.FACTORY, CarMode.DYNO)

    @pytest.mark.full
    def test_factory_to_dyno_caseid_110019(self):
        '''factory to dyno'''
        self.s2s_change_car_mode_and_check_result(CarMode.FACTORY)
        time.sleep(1)
        self.s2s_change_car_mode_and_check_result(CarMode.DYNO)

    @pytest.mark.full
    def test_factory_to_transport_caseid_110086(self):
        '''factory to transport'''
        self.s2s_change_car_mode_and_check_result(CarMode.FACTORY)
        time.sleep(1)
        self.s2s_change_car_mode_and_check_result(CarMode.TRANSPORT)

########################################退出Crash mode#####################################
    # @pytest.mark.full
    # def test_exit_crash_mode_110140(self):
    #     '''
    #     1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts==1 UsgModSts1_UsgModInactive
    #     2.BackboneFR:12-6-64:SafetyCrashFb_CrashFb == 3 CrashFb_Ok
    #     3.BackboneFR:49-11-32:HvSysCrashFb_CrashFb == 3 CrashFb_Ok
    #     4.usagemode inactive to convenience
    #     '''
    #     self.change_usage_mode_driving()
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 1)
        
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr26, 'HvSysCrashFb', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'SafetyCrashFb', 3)
    #     self.ipdu.check(
    #         self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12','CarModSts1_CarModCrash'
    #     )
    #     #inactive to convenience
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 0)
    #     self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
    #     time.sleep(1)
    #     self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
    #     self.ipdu.check(self.ipdu.bodycan.CEMBodyFr12, 'VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12', 0)
    
    # @pytest.mark.full
    # def test_exit_crash_mode_110139(self):
    #     '''
    #     1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts== 0 UsgModSts1_UsgModAbandoned
    #     2.BackboneFR:12-6-64:SafetyCrashFb_CrashFb == 3 CrashFb_Ok
    #     3.BackboneFR:49-11-32:HvSysCrashFb_CrashFb == 3 CrashFb_Ok
    #     4.usagemode abandon to active
    #     '''
        
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 1)
        
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr26, 'HvSysCrashFb', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'SafetyCrashFb', 3)
    #     self.ipdu.check(
    #         self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12','CarModSts1_CarModCrash'
    #     )
    #     #退出crash
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 0)
    #     self.set_usage_mode_to_abandoned()
    #     self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
    #     self.ipdu.check(self.ipdu.bodycan.CEMBodyFr12, 'VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12', 0)

    # @pytest.mark.full
    # def test_exit_crash_mode_110130(self):
    #     '''
    #     1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts==1 UsgModSts1_UsgModInactive
    #     2.BackboneFR:12-6-64:SafetyCrashFb_CrashFb == 3 CrashFb_Ok
    #     3.BackboneFR:49-11-32:HvSysCrashFb_CrashFb == 3 CrashFb_Ok
    #     4.Inactive change to Driving
    #     '''
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 1)
        
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr26, 'HvSysCrashFb', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'SafetyCrashFb', 3)
    #     self.ipdu.check(
    #         self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12','CarModSts1_CarModCrash'
    #     )
    #     #退出crash
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 0)
    #     self.change_usage_mode_driving()
    #     self.check_car_mode_status(0)



    # @pytest.mark.full
    # def test_exit_crash_mode_110079(self):
    #     '''
    #     1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts==1 UsgModSts1_UsgModInactive
    #     2.BackboneFR:12-6-64:SafetyCrashFb_CrashFb == 3 CrashFb_Ok
    #     3.BackboneFR:49-11-32:HvSysCrashFb_CrashFb == 3 CrashFb_Ok
    #     4.Usagemode from Abandoned change to Driving
    #     '''
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 1)
        
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr26, 'HvSysCrashFb', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'SafetyCrashFb', 3)
    #     self.ipdu.check(
    #         self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12','CarModSts1_CarModCrash'
    #     )
    #     #退出crash Inactive change to Active
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 0)
    #     self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
    #     time.sleep(1)
    #     self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
    #     self.check_car_mode_status(0)

    # @pytest.mark.full
    # def test_exit_crash_mode_110031(self):
    #     '''
    #     1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts==1 UsgModSts1_UsgModInactive
    #     2.BackboneFR:12-6-64:SafetyCrashFb_CrashFb == 3 CrashFb_Ok
    #     3.BackboneFR:49-11-32:HvSysCrashFb_CrashFb == 3 CrashFb_Ok
    #     4.Usagemode from Abandoned change to Convenience
    #     '''
    #     self.set_usage_mode_to_abandoned()
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr26, 'HvSysCrashFb', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'SafetyCrashFb', 3)
    #     self.ipdu.check(
    #         self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12','CarModSts1_CarModCrash'
    #     )
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 0)
    #     # Abandoned change to Convenience
    #     self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
    #     time.sleep(1)
    #     self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
    #     self.check_car_mode_status(0)
    
    # @pytest.mark.full
    # def test_exit_crash_mode_109987(self):
    #     '''
    #     1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts==1 UsgModSts1_UsgModInactive
    #     2.BackboneFR:12-6-64:SafetyCrashFb_CrashFb == 3 CrashFb_Ok
    #     3.BackboneFR:49-11-32:HvSysCrashFb_CrashFb == 3 CrashFb_Ok
    #     4.Inactive change to Active
    #     '''
    #     self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 1)
        
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr26, 'HvSysCrashFb', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'SafetyCrashFb', 3)
    #     self.ipdu.check(
    #         self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12','CarModSts1_CarModCrash'
    #     )
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 0)
    #     #  Inactive change to Active
    #     self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
    #     time.sleep(1)
    #     self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
    #     self.check_car_mode_status(0)

    # @pytest.mark.full
    # def test_exit_crash_mode_110094(self):
    #     '''
    #     1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts==1 UsgModSts1_UsgModInactive
    #     2.BackboneFR:12-6-64:SafetyCrashFb_CrashFb == 3 CrashFb_Ok
    #     3.BackboneFR:49-11-32:HvSysCrashFb_CrashFb == 3 CrashFb_Ok
    #     4.Inactive change to Active
    #     '''
        
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 1)
        
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr26, 'HvSysCrashFb', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'SafetyCrashFb', 3)
    #     self.ipdu.check(
    #         self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12','CarModSts1_CarModCrash'
    #     )
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 0)
    #     #  Inactive change to Active
    #     self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
    #     time.sleep(1)
    #     self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
    #     self.check_car_mode_status(0)

    # @pytest.mark.full
    # def test_exit_crash_mode_109968(self):
    #     '''
    #     1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts==1 UsgModSts1_UsgModInactive
    #     2.BackboneFR:12-6-64:SafetyCrashFb_CrashFb == 3 CrashFb_Ok
    #     3.BackboneFR:49-11-32:HvSysCrashFb_CrashFb == 3 CrashFb_Ok
    #     4.Usagemode from Inactive change to Driving
    #     '''
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 1)
    #     time.sleep(.5)
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr26, 'HvSysCrashFb', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'SafetyCrashFb', 3)
    #     self.ipdu.check(
    #         self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12','CarModSts1_CarModCrash'
    #     )
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 0)
    #     #  Inactive change to Driving
    #     self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
    #     time.sleep(1)
    #     self.change_usage_mode_driving()
    #     time.sleep(.5)
    #     self.check_car_mode_status(0)

    # @pytest.mark.full
    # def test_exit_crash_mode_109898(self):
    #     '''
    #     1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts==1 UsgModSts1_UsgModInactive
    #     2.BackboneFR:12-6-64:SafetyCrashFb_CrashFb == 3 CrashFb_Ok
    #     3.BackboneFR:49-11-32:HvSysCrashFb_CrashFb == 3 CrashFb_Ok
    #     4.Usagemode from  Inactive change to Convenience
    #     '''
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 1)
        
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr26, 'HvSysCrashFb', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'SafetyCrashFb', 3)
    #     self.ipdu.check(
    #         self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12','CarModSts1_CarModCrash'
    #     )
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 0)
    #     #  Inactive change to Convenience
    #     self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
    #     time.sleep(1)
    #     self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
    #     self.check_car_mode_status(0)

    # @pytest.mark.full
    # def test_exit_crash_mode_109953(self):
    #     '''
    #     1.Body_CAN:0x0F0:VehModMngtGlbSafe1UsgModSts==1 UsgModSts1_UsgModInactive
    #     2.BackboneFR:12-6-64:SafetyCrashFb_CrashFb == 3 CrashFb_Ok
    #     3.BackboneFR:49-11-32:HvSysCrashFb_CrashFb == 3 CrashFb_Ok
    #     4.UDrvrStrtReq == Reqd
    #     '''
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 1)
    #     time.sleep(.5)
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr26, 'HvSysCrashFb', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'SafetyCrashFb', 3)
    #     self.ipdu.check(
    #         self.ipdu.bodycan.CEMBodyFr12 ,'VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12','CarModSts1_CarModCrash'
    #     )
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 0)
    #     #  UDrvrStrtReq == Reqd
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 2)
    #     self.dk.set_internal_has_key()
    #     self.s2sbaseclass.send_method_request('VehicleModeService_client',
    #         'SetUsageModeUp',
    #         {"mode": 13},)
    #     self.check_car_mode_status(0)
    