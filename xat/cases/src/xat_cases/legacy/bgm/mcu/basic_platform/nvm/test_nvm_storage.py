# -*- coding: utf-8 -*-
"""
@File        : test_nvm_storage.py
@Author      : huajie.yang@jiduauto.com
@Time        : 2023/10/24 
@Description : Test NVM storage functionality
"""

import os
import sys
import struct
from time import sleep
import pytest
import allure
import random
from xat_ecu.legacy.interface.ecuinterface import EcuInterFace

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
sys.path.append(os.path.join(os.getcwd(), "../../../.."))

from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_cases.legacy.bgm.case_helper.diag_case_helper.DiagTestBase import *
from xat_ecu.legacy.soa_partner.src.base_partner import *

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

@pytest.mark.mcu_test
@pytest.mark.smoke
class TestNvmStora(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        partner_process_check()
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟(数据库周期性报文和调度表)
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        self.nucapp.bgm_diag_line_up()
        self.sd = DiagTestBase(self.ipdu, self.busapp, self.tc_config)
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)

        self.sd_tester.update_serverdoipid(0x1002)
        sleep(0.5)
        self.sd_tester.diagnostic_client_sim_start()
        self.sd_tester.tester_present()
        self.s2sbaseclass = S2sBaseClass(
            [
                ("VehicleModeService", "client"),
                ("LightService", "client"),
                ("KeyService", "client"),
                ("TailWingService", "client"),
                ("CentralLockService", "client"),
                ("LowVoltageService", "client"),
                ("WTIService", "client"),
            ]
        )
        self.ecu_interface = EcuInterFace(
            sd_test=self.sd_tester,
            ipdu=self.ipdu,
            io_obj=self.io,
            dk=self.dk,
            nucapp=self.nucapp,
            cfg=self.tc_config,
        )

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.sd_tester.send_request_and_recv_response([0x22, 0xDB, 0x02])  # 读cpuload
        self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set_vehspd(0.0)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0
        )
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client',
            'SetCarMode',
            {"mode": 0},
        )
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr02,
            'VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02',
            'CarModSts1_CarModNorm',
        )

        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client',
            'SetUsageModeDown',
            {"mode": 1},
        )
        sleep(0.7)
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModInActv',
        )
        sleep(0.7)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client',
            'SetExhibitionMode',
            {"isOpen": False},
        )
        self.ipdu.check(
            self.ipdu.propulsioncan.BgmPropulsionFr01,
            'ExhibitionModeStsExhibitionModeSts_1_BgmPropSignalIPdu01',
            'OnOff1_Off',
        )


    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0
        )       
        self.nucapp.bgm_diag_line_up()

    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client',
            'SetExhibitionMode',
            {"isOpen": False},
        )
        self.ipdu.time_control_stop()
        self.busapp.stop_all_cyclic_msgs()
        self.sd_tester.stop_tester_present()
        sleep(0.5)
        self.sd_tester.diagnostic_client_sim_close()

    def reset_bgm(self):
        self.sd_tester.update_serverdoipid(0x1FFF)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(25)
        self.sd_tester.update_serverdoipid(0x1002)

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
        lin_msg = kwargs.get("lin_msg", [0x0, 0x7C, 0xC8, 0xFF, 0xFF, 0xFF, 0xFF])
        logger.info("断开诊断激活线")
        self.nucapp.bgm_diag_line_down()
        time.sleep(1)
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
        self.ipdu.check(
            self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts_2_CemBodySignalIPdu02', 2
        )
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts_2_CEMBodySignalIPdu11', 2
        )
        self.ipdu.check(
            self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts_1_CemBodySignalIPdu02', 2
        )
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts_1_CEMBodySignalIPdu11', 2
        )
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11, 'TrSts_2_CEMBodySignalIPdu11', 2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'HoodSts', 2)
        # 4. 闭锁
        self.dk.set_cenlock_sts(0x3)
        time.sleep(1)
        t1 = time.time()
        # 等待一定时间
        logger.info(f"最长等待{wait_time}秒,让 bgm 进入abandoned 模式，超过时间未进入则退出")
        t1 = time.time()
        realvalue = None
        while time.time() - t1 < wait_time:
            result, realvalue, expectedvalue = self.check_usage_mode_status(
                expectedmode=0, do_assert=False
            )
            logger.info(f"当前模式为{realvalue}期望模式为{expectedvalue}")
            #
            if result:
                # 进入
                logger.info(f"成功进入 abandoned 状态耗时{time.time() - t1}s")
                return True
        else:
            if do_assert:
                assert 0, "进入abandoned  失败"
            return False

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
            self.set_lock()
            self.dk.set_cenlock_sts(1)
            sleep(1)
            self.ipdu.set(
                self.ipdu.backbonefr.BcmVddmBackBoneFr00,
                'BrkPedlPsdBrkPedlNotPsdSafe',
                1,
            )
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
            self.ipdu.set(
                self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1
            )
            # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
            method_name = "SetUsageModeUp"
        elif curren_usage_mode > usage_mode:
            method_name = "SetUsageModeDown"
        else:
            # 已经是所需要模式，无需切换，直接返回
            return 1, curren_usage_mode, curren_usage_mode
        # 如果切到driving 模式以后 不设置为0 则切不成功
        self.ipdu.backbonefr_vddmbackbonefr00_engst1wdstsengst1wdsts_engst1_ini()
        # 设置 同星信号
        self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
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

    def doip_1002_level(self, level):
        '''1002进入扩展会话过安全等级'''
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.enter_extended_session()
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        self.sd_tester.security_access_level(level)
        self.sd_tester.return_udsdata_and_check_and_print_response_result()

    def doip_1002(self):
        '''1002进入扩展会话过安全等级'''
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.enter_extended_session()
        self.sd_tester.return_udsdata_and_check_and_print_response_result()

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
        result, realvalue, expectedvalue = self.ipdu.check(
            msg_signals_obj=msg_signals_obj,
            signal_name=signal_name,
            sig_value_name=expectedmode,
            do_assert=do_assert,
            timeout=timeout,
        )

        return result, realvalue, expectedvalue

    def set_lock(self):
        '''nfc闭锁'''
        self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.backbonefr_vddmbackbonefr03_gearlvrindcn_gearlvrindcn2_parkindcn()
        # self.sd_tester.write_multi_ccp({94: 0x80, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x4, 578: 0x4})
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
        self.ipdu.check(
            self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts_2_CemBodySignalIPdu02', 2
        )
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts_2_CEMBodySignalIPdu11', 2
        )
        self.ipdu.check(
            self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts_1_CemBodySignalIPdu02', 2
        )
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts_1_CEMBodySignalIPdu11', 2
        )
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11, 'TrSts_2_CEMBodySignalIPdu11', 2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'HoodSts', 2)
        time.sleep(0.3)
        self.dk.set_cenlock_sts(0x3)
        sleep(1)

    @pytest.mark.smoke
    def test_caseid_1984374(self):
        '''Usagemode_本地存储和恢复_Driving_No_Run'''
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.check_usage_mode_status(11)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        time.sleep(1)
        self.reset_bgm()
        self.check_usage_mode_status(13)

    @pytest.mark.smoke
    def test_caseid_1984377(self):
        '''车辆模式的本地存储和恢复_CarModFactory'''
        self.dk.set_cenlock_sts(0x1)
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetCarMode", {"mode": 2}
        )
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr02,
            'VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02',
            'CarModSts1_CarModFcy',
        )
        time.sleep(1)
        self.reset_bgm()
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr02,
            'VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02',
            'CarModSts1_CarModFcy',
        )
    @pytest.mark.sanity
    def test_caseid_1984376(self):
        '''Carmode_车辆模式的本地存储和恢复_FactoryPaused'''
        self.dk.set_central_lock(0x1)
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetCarMode", {"mode": 2}
        )
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr02,
            'VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02',
            'CarModSts1_CarModFcy',
        )
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

    @pytest.mark.smoke
    def test_caseid_1984386(self):
        '''展车模式存储与恢复'''
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client',
            'SetExhibitionMode',
            {"isOpen": True},
        )
        self.s2sbaseclass.send_request_and_ck_resp(
            'VehicleModeService_client',
            "GetExhibitionModeSts",
            {},
            {"out": {"isOpen": True, "isValid": True}},
        )
        self.ipdu.check(
            self.ipdu.propulsioncan.BgmPropulsionFr01,
            'ExhibitionModeStsExhibitionModeSts_1_BgmPropSignalIPdu01',
            'OnOff1_On',
        )
        time.sleep(1)
        self.reset_bgm()
        self.ipdu.check(
            self.ipdu.propulsioncan.BgmPropulsionFr01,
            'ExhibitionModeStsExhibitionModeSts_1_BgmPropSignalIPdu01',
            'OnOff1_On',
        )

    @pytest.mark.smoke
    def test_caseid_1984378(self):
        '''门状态存储'''
        # 四门全关
        self.io.drvr_door_close()
        self.io.pass_door_close()
        self.io.lere_door_close()
        self.io.rire_door_close()
        # 开主驾和左后门
        self.io.drvr_door_open()
        self.io.lere_door_open()
        self.ipdu.check(
            self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts_2_CemBodySignalIPdu02', 1
        )
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts_2_CEMBodySignalIPdu11', 2
        )
        self.ipdu.check(
            self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts_1_CemBodySignalIPdu02', 1
        )
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts_1_CEMBodySignalIPdu11', 2
        )
        self.reset_bgm()
        self.ipdu.check(
            self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts_2_CemBodySignalIPdu02', 1
        )
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts_2_CEMBodySignalIPdu11', 2
        )
        self.ipdu.check(
            self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts_1_CemBodySignalIPdu02', 1
        )
        self.ipdu.check(
            self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts_1_CEMBodySignalIPdu11', 2
        )

    @pytest.mark.smoke
    def test_caseid_1984382(self):
        '''读FOTA状态F153存储'''
        self.doip_1002_level(3)
        logger.info("读FOTA状态值")
        self.sd_tester.send_request_and_recv_response(
            [0x22, 0xF1, 0x53]
        )
        sleep(.1)
        write_f153_list = [random.randint(0, 4)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0xF1, 0x53], write_f153_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("读FOTA状态值")
        self.doip_1002_level(3)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0xF1, 0x53],
            recv=[0x62, 0xF1, 0x53] + write_f153_list,
            do_assert=True,
        )
        sleep(1)
        read_f153_lsit = read_date[3:]
        logger.info("恢复读FOTA状态值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0xF1, 0x53, 0x00]
        )
        if read_f153_lsit != write_f153_list:
            log_string = f"写入读FOTA状态值失败,读取结果本应为{bytes(write_f153_list).hex()}实际为{bytes(read_f153_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.smoke
    def test_caseid_1984385(self):
        '''雨量传感器阈值DID 45A4'''
        self.doip_1002_level(6)
        logger.info("读取雨量传感器阈值")
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x45, 0xA4]
        )
        sleep(.1)
        write_rain_list = [random.randint(0, 15)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0xA4], write_rain_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("读取雨量传感器阈值")
        self.doip_1002_level(6)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x45, 0xA4],
            recv=[0x62, 0x45, 0xA4] + write_rain_list
        )
        sleep(.1)
        read_rain_lsit = read_date[3:]
        logger.info("恢复雨量传感器阈值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0xA4] + local_date[3:]
        )
        if read_rain_lsit != write_rain_list:
            log_string = f"写入雨量传感器阈值失败,读取结果本应为{bytes(write_rain_list).hex()}实际为{bytes(read_rain_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.smoke
    def test_caseid_1984370(self):
        '''认证密钥40DE存储'''
        self.doip_1002_level(6)
        logger.info("读取认证密钥")
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0xDE]
        )
        sleep(.1)
        # 生成随机认证密钥
        write_immokey_list = [random.randint(0, 255) for _ in range(32)]
        logger.info("读取认证密钥")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x40, 0xDE], write_immokey_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("写入随机密钥后，读取认证密钥")
        self.doip_1002_level(6)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0xDE],
            recv=[0x62, 0x40, 0xDE] + write_immokey_list,
            do_assert=True,
        )
        sleep(.1)
        read_immokey_lsit = read_date[3:]
        logger.info("恢复认证密钥")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x40, 0xDE] + local_date[3:]
        )
        if read_immokey_lsit != write_immokey_list:
            log_string = f"认证密钥写入失败,读取结果本应为{bytes(write_immokey_list).hex()}实际为{bytes(read_immokey_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.smoke
    def test_caseid_1984369(self):
        '''认证密钥40DF存储'''
        self.doip_1002_level(6)
        logger.info("读取认证密钥")
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0xDF]
        )
        sleep(.1)
        # 生成随机认证密钥
        write_immokey_list = [random.randint(0, 255) for _ in range(32)]
        logger.info("读取认证密钥")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x40, 0xDF], write_immokey_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("写入随机密钥后，读取认证密钥")
        self.doip_1002_level(6)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0xDF],
            recv=[0x62, 0x40, 0xDF] + write_immokey_list,
            do_assert=True,
        )
        sleep(.1)
        read_immokey_lsit = read_date[3:]
        logger.info("恢复认证密钥")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x40, 0xDF] + local_date[3:]
        )
        if read_immokey_lsit != write_immokey_list:
            log_string = f"认证密钥写入失败,读取结果本应为{bytes(write_immokey_list).hex()}实际为{bytes(read_immokey_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.smoke
    def test_caseid_1984368(self):
        '''认证密钥40E0存储'''
        self.doip_1002_level(6)
        logger.info("读取认证密钥")
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0xE0]
        )
        sleep(.1)
        # 生成随机认证密钥
        write_immokey_list = [random.randint(0, 255) for _ in range(32)]
        logger.info("读取认证密钥")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x40, 0xE0], write_immokey_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("写入随机密钥后，读取认证密钥")
        self.doip_1002_level(6)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0xE0],
            recv=[0x62, 0x40, 0xE0] + write_immokey_list,
            do_assert=True,
        )
        sleep(.1)
        read_immokey_lsit = read_date[3:]
        logger.info("恢复认证密钥")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x40, 0xE0] + local_date[3:]
        )
        if read_immokey_lsit != write_immokey_list:
            log_string = f"认证密钥写入失败,读取结果本应为{bytes(write_immokey_list).hex()}实际为{bytes(read_immokey_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.sanity
    def test_caseid_1984457(self):
        '''40EF闭锁命令记录'''
        self.sd_tester.send_data([0x22, 0x40, 0xEF])
        result1 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        sleep(1)
        self.set_lock()
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr12,
            'LockgCenStsLockSt_2_VgmConnSignalIPdu12',
            3,
        )
        sleep(1)
        self.reset_bgm()
        self.sd_tester.send_data([0x22, 0x40, 0xEF])
        result2 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        if result1 == result2:
            str1 = f'此次闭锁命令未记录'
            logger.info(str1)
            assert 0, str1

    @pytest.mark.sanity
    def test_caseid_1984458(self):
        '''40F0解锁命令记录'''
        self.sd_tester.send_data([0x22, 0x40, 0xF0])
        result1 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        self.sd_tester.change_usage_mode(1)
        self.dk.set_cenlock_sts(0x1)
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr12,
            'LockgCenStsLockSt_2_VgmConnSignalIPdu12',
            1,
        )
        sleep(1)
        self.reset_bgm()
        self.sd_tester.send_data([0x22, 0x40, 0xF0])
        result2 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        if result1 == result2:
            str1 = f'此次解锁命令未记录'
            logger.info(str1)
            assert 0, str1

    @pytest.mark.smoke
    def test_caseid_1984375(self):
        '''Usagemode_本地存储和恢复_Active_No_Run'''
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.check_usage_mode_status(11)
        time.sleep(0.7)
        self.reset_bgm()
        self.check_usage_mode_status(11)

    @pytest.mark.smoke
    def test_caseid_1984373(self):
        '''写CCP车辆配置字F106存储恢复'''
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0xF1, 0x06]
        )
        sleep(.1)
        logger.info("写入ccp")
        self.sd_tester.write_single_ccp(1556, 4)  # 总共1558个byte,后两位是校验位
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("再次读取ccp")
        self.sd_tester.send_data([0x22, 0xF1, 0x06])
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        sleep(.1)
        logger.info("恢复ccp")
        localdate = local_date[-3]
        self.sd_tester.write_single_ccp(1556, localdate)
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        assert result[-3] == 4

    @pytest.mark.smoke
    def test_caseid_1984372(self):
        '''写vin码F190存储恢复'''
        self.doip_1002_level(3)
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0xF1, 0x90]
        )
        sleep(.1)
        write_vin_list = [random.randint(0, 255) for _ in range(17)]
        logger.info("随机写入vin码")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0xF1, 0x90], write_vin_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("再次读取vin码")
        self.doip_1002_level(3)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0xF1, 0x90],
            recv=[0x62, 0xF1, 0x90] + write_vin_list,
            do_assert=True,
        )
        sleep(.1)
        read_vin_lsit = read_date[3:]
        logger.info("恢复vin码")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0xF1, 0x90] + local_date[3:]
        )
        if read_vin_lsit != write_vin_list:
            log_string = f"写入vin码失败,读取结果本应为{bytes(write_vin_list).hex()}实际为{bytes(read_vin_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.sanity
    def test_caseid_1984371(self):
        '''写TPMS 281F存储恢复'''
        self.doip_1002_level(3)
        logger.info("读取TPMS ID")
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x28, 0x1F]
        )
        sleep(.1)
        write_tpmsid_list = [random.randint(0, 255) for _ in range(16)]
        logger.info("随机写入TPMS ID")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x28, 0x1F], write_tpmsid_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("再次读取tpms id")
        self.doip_1002_level(3)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x28, 0x1F],
            recv=[0x62, 0x28, 0x1F] + write_tpmsid_list,
            do_assert=True,
        )
        sleep(.1)
        read_tpmsid_lsit = read_date[3:]
        logger.info("恢复tpmsid")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x28, 0x1F] + local_date[3:]
        )
        if read_tpmsid_lsit != write_tpmsid_list:
            log_string = f"写入tpms id失败,读取结果本应为{bytes(write_tpmsid_list).hex()}实际为{bytes(read_tpmsid_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    # 高风险DID
    @pytest.mark.smoke
    def test_caseid_1984454(self):
        '''电源管理DIDF0F5存储'''
        self.doip_1002_level(3)
        logger.info("读取电源管理值")
        self.sd_tester.send_request_and_recv_response([0x22, 0xF0, 0xF5])
        sleep(.1)
        logger.info("写入电源管理值")
        self.sd_tester.send_request_and_recv_response([0x2E, 0xF0, 0xF5, 0x27, 0x0A, 0X03, 0X05, 0X03, 0x02],do_assert=True)
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("读取电源管理值")
        self.doip_1002_level(3)
        ret_code,read_date=self.sd_tester.send_request_and_recv_response([0x22, 0xF0, 0xF5],do_assert=True)
        sleep(.1)
        logger.info("恢复电源管理值")
        self.sd_tester.send_request_and_recv_response([0x2E, 0xF0, 0xF5, 0x28, 0x0A, 0X03, 0X05, 0X03, 0x02],do_assert=True)
        if read_date[-6] != 39:
            assert 0,"F0F5电源管理值未存储"

    @pytest.mark.sanity
    def test_caseid_1984459(self):
        '''4600内灯亮度值调节'''
        self.doip_1002_level(3)
        logger.info("读取内灯亮度值")
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x46, 0x00]
        )
        sleep(.1)
        logger.info("写入内灯亮度值")
        write_power_list = [random.randint(0, 100) for _ in range(5)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x46, 0x00], write_power_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("读取内灯亮度值")
        self.doip_1002_level(3)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x46, 0x00],
            recv=[0x62, 0x46, 0x00] + write_power_list,
            do_assert=True,
        )
        sleep(.1)
        read_power_lsit = read_date[3:]
        logger.info("恢复内灯亮度值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x46, 0x00] + local_date[3:]
        )
        if read_power_lsit != write_power_list:
            log_string = f"写入内灯亮度值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.smoke
    def test_caseid_1984383_1984384(self):
        '''nfc解闭锁状态存储'''
        self.set_lock()
        sleep(1)
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr12,
            'LockgCenStsLockSt_2_VgmConnSignalIPdu12',
            3,
        )
        logger.info("重启bgm")
        self.reset_bgm()
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr12,
            'LockgCenStsLockSt_2_VgmConnSignalIPdu12',
            3,
        )
        logger.info("nfc解锁")
        self.dk.set_cenlock_sts(0x1)
        sleep(1)
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr12,
            'LockgCenStsLockSt_2_VgmConnSignalIPdu12',
            1,
        )
        logger.info("重启bgm")
        self.reset_bgm()
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr12,
            'LockgCenStsLockSt_2_VgmConnSignalIPdu12',
            1,
        )

    # def test_caseid_1984380(self):
    #     '''靠近解锁锁状态存储'''
    #     self.set_lock()
    #     self.dk.send_approach_unlock_cmd()
    #     self.reset_bgm()
    #     self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr12, 'LockgCenStsLockSt_2_VgmConnSignalIPdu12', 1)

    # @pytest.mark.skip
    # def test_caseid_1984387(self):
    #     '''安全常数D12F存储(需要修改yaml文件中的安全常数)'''
    #     self.dk.set_cenlock_sts(0x1)
    #     self.doip_1002_level(6)
    #     write_vin_string="22 22 22 22 22".strip().replace(" ","").upper()
    #     data_list=[int(write_vin_string[i:i+2],16) for i in range(0,len(write_vin_string),2)]
    #     self.sd_tester.send_data([0x2E, 0xD1, 0x2F]+data_list)
    #     self.reset_bgm()
    #     self.doip_1002_level(6)
    #     self.sd_tester.send_data([0x22, 0xD1, 0x2F])
    #     result = self.sd_tester.return_udsdata_and_check_and_print_response_result()
    #     #恢复
    #     write_vin_string1="FF FF FF FF FF".strip().replace(" ","").upper()
    #     data_list1=[int(write_vin_string1[i:i+2],16) for i in range(0,len(write_vin_string1),2)]
    #     self.sd_tester.send_data([0x2E, 0xD1, 0x2F]+data_list1)
    #     if result[:3]!=[0x62, 0xD1, 0x2F]:
    #         assert 0,"读取安全常数失败"
    #     read_vin_string=bytes(result[3:]).hex().upper()
    #     log_string=f"安全常数写入失败,读取结果本应为{write_vin_string}实际为{read_vin_string}"
    #     logger.info(log_string)
    #     assert read_vin_string ==write_vin_string,log_string

    # 需要8小时等待时间才有记录
    # def test_caseid_100369(self):
    #     '''40E4电力系统故障计数器'''
    #     self.nucapp.bgm_power_off()
    #     time.sleep(1)
    #     self.nucapp.bgm_power_on()
    #     time.sleep(15)
    #     self.sd_tester.send_data([0x22, 0x40, 0xE4])
    #     date1 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
    #     self.sd_tester.write_single_ccp(32, 9)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr05, 'BattURaw_0_BmsCem_Lin6SignalIPdu05', 12.0)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr15, 'FltTDcDc', 0)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'DcDcActvd', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr21, 'FltElecDcDc', 1)
    #     sleep(10)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts', 7)
    #     self.s2sbaseclass.ck_s2s_event(LOWVOLTAGE_SERVICE, "LVFault", {"faults": [{"faultId": 7, "faultMsg": ""}]})
    #     self.s2sbaseclass.send_request_and_ck_resp(LOWVOLTAGE_SERVICE, "GetLVFault", {},
    #                                           {"out": [{"faultId": 7, "faultMsg": ""}]})
    #     self.s2sbaseclass.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList", {"list": [{"name": "Low Voltage Battery",
    #                                                                              "state": "1"}]})
    #     self.s2sbaseclass.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
    #                               {"list": [{"name": "Low Battery Warning1", "info": "2"}]})
    #     self.s2sbaseclass.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
    #                                           {"out": [{"name": "Low Voltage Battery", "state": "1"}]})
    #     self.s2sbaseclass.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
    #                                           {"out": [{"name": "Low Battery Warning1", "info": "2"}]})
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr21, 'FltElecDcDc', 0)
    #     sleep(10)
    #     self.reset_bgm()
    #     self.sd_tester.send_data([0x22, 0x40, 0xE4])
    #     date2 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
    #     if date2[10] != date1[10] + 1:
    #         assert 0,"本次故障未统计"

    @pytest.mark.full
    def test_caseid_1984455(self):
        '''使用模式时间统计convenience存储区间为72-96bit'''
        self.doip_1002_level(3)
        self.sd_tester.send_data([0x22, 0x43, 0x0F])
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        date1 = result[12]
        self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
        self.check_usage_mode_status(2)
        time.sleep(63)  # 需求中需要等待1min才能存储
        self.sd_tester.send_data([0x22, 0x43, 0x0F])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        self.reset_bgm()
        self.sd_tester.send_data([0x22, 0x43, 0x0F])
        result1 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        date2 = result1[12]
        if date2 != date1 + 1:
            assert 0, "usagemode未存储此次时间统计"

    @pytest.mark.smoke
    def test_caseid_1984381(self):
        '''统计usagemode使用次数存储convenience存储区间为144-160bit'''
        self.doip_1002_level(3)
        self.sd_tester.send_data([0x22, 0x43, 0x0E])
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        date1 = result[21]
        self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
        self.check_usage_mode_status(2)
        sleep(11)  # 需求中需要等待10s才能计数
        self.reset_bgm()
        self.sd_tester.send_data([0x22, 0x43, 0x0E])
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        if result[21] != date1 + 2:  # 因为重启的时候超过了10s所以应+2
            assert 0, "usagemode未存储此次切换"

    @pytest.mark.full
    def test_caseid_1984472(self):
        '''4297解锁持续时间'''
        self.doip_1002_level(6)
        logger.info("读取nfc解锁持续时间的值")
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x42, 0x97]
        )
        sleep(.1)
        logger.info("写入nfc解锁持续时间的值")
        write_power_list = [random.randint(0, 255)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x42, 0x97], write_power_list, do_assert=True
        )
        sleep(1)
        logger.info("重启bgm")
        self.reset_bgm()
        logger.info("读取nfc解锁持续时间的值")
        self.doip_1002_level(6)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x42, 0x97],
            recv=[0x62, 0x42, 0x97] + write_power_list,
            do_assert=True,
        )
        sleep(.1)
        read_power_lsit = read_date[3:]
        logger.info("恢复nfc解锁持续时间的值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x42, 0x97, 0xFF], do_assert=True
        )
        if read_power_lsit != write_power_list:
            log_string = f"写入nfc解锁持续时间的值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.full
    def test_caseid_1984473(self):
        '''4532休眠超时充电使能'''
        self.doip_1002_level(3)
        self.sd_tester.send_data([0x22, 0x45, 0x32])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        sleep(.1)
        self.sd_tester.send_data([0x2E, 0x45, 0x32, 0x01])
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.sd_tester.send_data([0x22, 0x45, 0x32])
        date1 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        sleep(.1)
        self.doip_1002_level(3)
        self.sd_tester.send_data([0x2E, 0x45, 0x32, 0x00])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        if date1[-1] != 1:
            assert 0, "本次写入的值未存储"

    @pytest.mark.full
    def test_caseid_1984474(self):
        '''DID4534休眠异常充电电压阈值,
        诊断调查表中DID读出的值应除以10范围在8-16'''
        self.doip_1002_level(3)
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x45, 0x34]
        )
        sleep(.1)
        logger.info("随机写入值")
        write_power_list = [random.randint(80, 160)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0x34], write_power_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.doip_1002_level(3)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x45, 0x34],
            recv=[0x62, 0x45, 0x34] + write_power_list,
            do_assert=True,
        )
        sleep(.1)
        read_power_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0x34] + local_date[3:]
        )
        if read_power_lsit != write_power_list:
            log_string = f"写入值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.full
    def test_caseid_1984475(self):
        '''DID4530休眠低压唤醒充电使能,取值0=Enable 1=Disable'''
        self.doip_1002_level(3)
        self.sd_tester.send_data([0x22, 0x45, 0x30])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        sleep(.1)
        self.sd_tester.send_data([0x2E, 0x45, 0x30, 0x01])
        logger.info("bgm重启")
        sleep(1)
        self.reset_bgm()
        self.sd_tester.send_data([0x22, 0x45, 0x30])
        date1 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        sleep(.1)
        self.doip_1002_level(3)
        self.sd_tester.send_data([0x2E, 0x45, 0x30, 0x00])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        if date1[-1] != 1:
            assert 0, "本次写入的值未存储"

    @pytest.mark.full
    def test_caseid_1984476(self):
        '''
        DID4531休眠低压唤醒充电电压阈值
        取值范围8-16
        '''
        self.doip_1002_level(3)
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x45, 0x31]
        )
        sleep(.1)
        write_power_list = [random.randint(80, 160)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0x31], write_power_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.doip_1002_level(3)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x45, 0x31],
            recv=[0x62, 0x45, 0x31] + write_power_list,
            do_assert=True,
        )
        sleep(.1)
        read_power_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0x31] + local_date[3:]
        )
        if read_power_lsit != write_power_list:
            log_string = f"写入值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.full
    def test_caseid_1984477(self):
        '''DID4533能补电退出SOC阈值'''
        self.doip_1002_level(3)
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x45, 0x33]
        )
        sleep(.1)
        write_power_list = [random.randint(0, 127)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0x33], write_power_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.doip_1002_level(3)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x45, 0x33],
            recv=[0x62, 0x45, 0x33] + write_power_list,
            do_assert=True,
        )
        sleep(.1)
        read_power_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0x33] + local_date[3:]
        )
        if read_power_lsit != write_power_list:
            log_string = f"写入值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    # def test_caseid_666(self):
    #     '''DID42CF只能读'''
    #     self.doip_1002_level(3)
    #     ret_code,local_date = self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0xCF])
    #     write_power_list=[random.randint(0,255) for _ in range(5)]
    #     self.sd_tester.send_request_and_recv_response([0x2E, 0x42, 0xCF],write_power_list,do_assert=False)
    #     logger.info("bgm重启")
    #     sleep(.1)
    #     self.reset_bgm()
    #     self.doip_1002_level(3)
    #     ret_code,read_date=self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0xCF],recv=[0x62, 0x42, 0xCF]+write_power_list,do_assert=False)
    #     read_power_lsit=read_date[3:]
    #     logger.info("恢复值")
    #     self.sd_tester.send_request_and_recv_response([0x2E, 0x42, 0xCF]+local_date[3:])
    #     if read_power_lsit != write_power_list:
    #         log_string=f"写入值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
    #         logger.info(log_string)
    #         assert 0,log_string

    # def test_caseid_777(self):
    #     '''4187运输模式下低电量报警次数统计'''
    #     ret_code,local_date= self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0x87])
    #     sleep(1)
    #     self.s2sbaseclass.send_method_request(
    #         'VehicleModeService_client',
    #         'SetCarMode',
    #         {"mode": 1},
    #     )
    #     # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
    #     # self.sd_tester.change_car_mode(1)
    #     self.ipdu.check(
    #         self.ipdu.backbonefr.CemBackBoneFr02 ,'VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02',1)
    #     self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
    #     self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
    #     self.s2sbaseclass.empty_all(1)
    #     #低电量2级报警
    #     self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.5)
    #     sleep(1)
    #     self.s2sbaseclass.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"High Voltage Battery Low Warning", "info": "2"}]})
    #     self.s2sbaseclass.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"High Voltage Battery Low Telltale", "state": "2"}]})
    #     self.s2sbaseclass.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"High Voltage Battery Low Warning", "info": "2"}]})
    #     sleep(1)
    #     self.s2sbaseclass.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out":[{"name":"High Voltage Battery Low Telltale", "state": "2"}]})
    #     ##低电量1级报警
    #     self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.6)
    #     sleep(1)
    #     self.s2sbaseclass.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"High Voltage Battery Low Warning", "info": "1"}]})
    #     self.s2sbaseclass.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"High Voltage Battery Low Telltale", "state": "1"}]})
    #     self.s2sbaseclass.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"High Voltage Battery Low Warning", "info": "1"}]})
    #     sleep(1)
    #     self.s2sbaseclass.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out":[{"name":"High Voltage Battery Low Telltale", "state": "1"}]})
    #     # ##低电量无报警
    #     # self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
    #     # sleep(1)
    #     # self.s2sbaseclass.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"High Voltage Battery Low Warning", "info": "0"}]})
    #     # self.s2sbaseclass.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"High Voltage Battery Low Telltale", "state": "0"}]})
    #     # self.s2sbaseclass.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"High Voltage Battery Low Warning", "info": "0"}]})
    #     # sleep(1)
    #     # self.s2sbaseclass.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out":[{"name":"High Voltage Battery Low Telltale", "state": "0"}]})
    #     ret_code,local_date1= self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0x87])
    #     # if local_date1 != local_date+2:
    #     #     assert 0,"本次低电量告警未存储"

    @pytest.mark.smoke
    def test_caseid_1984367(self):
        '''408F远程车辆IMMO密钥的读写状态16个byte'''
        self.doip_1002_level(6)
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0x8F]
        )
        sleep(.1)
        write_power_list = [random.randint(0, 255) for _ in range(16)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x40, 0x8F], write_power_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm重启")
        self.sd_tester.stop_tester_present()
        self.reset_bgm()
        self.sd_tester.tester_present()
        self.doip_1002_level(6)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x40, 0x8F],
            recv=[0x62, 0x40, 0x8F] + write_power_list,
            do_assert=True,
        )
        sleep(.1)
        read_power_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x40, 0x8F] + local_date[3:]
        )
        if read_power_lsit != write_power_list:
            log_string = f"写入值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.sanity
    def test_caseid_1984478(self):
        '''诊断写carmode'''
        self.doip_1002_level(3)
        self.ecu_interface.change_car_mode_to_factory()
        sleep(1)
        self.reset_bgm()
        self.sd_tester.send_data([0x22, 0xD1, 0x34])
        date1 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        if date1[-1] != 2:
            assert 0, "此次切换未存储"

    @pytest.mark.smoke
    def test_caseid_1984479(self):
        '''防盗状态'''
        self.set_lock()
        time.sleep(30)
        self.io.drvr_door_open()
        self.ipdu.check(
            self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts_2_CemBodySignalIPdu02', 1
        )
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr18, 'AlrmStsAlrmSt', 2)
        self.reset_bgm()
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr18, 'AlrmStsAlrmSt', 2)
        self.dk.set_central_lock(0x1)

    @pytest.mark.full
    def test_caseid_1984480(self):
        '''4535充电开启SOC阈值'''
        self.doip_1002_level(3)
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x45, 0x35]
        )
        sleep(.1)
        write_power_list = [random.randint(0, 127)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0x35], write_power_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.doip_1002_level(3)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x45, 0x35],
            recv=[0x62, 0x45, 0x35] + write_power_list,
            do_assert=True,
        )
        sleep(.1)
        read_power_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0x35] + local_date[3:]
        )
        if read_power_lsit != write_power_list:
            log_string = f"写入值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.full
    def test_caseid_1984481(self):
        '''42E9中控锁防玩保护'''
        self.doip_1002()
        self.sd_tester.send_data([0x22, 0x42, 0xE9])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        sleep(.1)
        self.sd_tester.send_data([0x2E, 0x42, 0xE9, 0x01])
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.doip_1002()
        self.sd_tester.send_data([0x22, 0x42, 0xE9])
        date1 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        sleep(.1)
        self.sd_tester.send_data([0x2E, 0x42, 0xE9, 0x00])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        if date1[-1] != 1:
            assert 0, "本次写入的值未存储"

    @pytest.mark.full
    def test_caseid_1984486(self):
        '''4109方向盘加热温度补偿'''
        self.doip_1002()
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0x09]
        )
        sleep(1)
        write_power_list = [random.randint(1, 15)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x41, 0x09], write_power_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.doip_1002()
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0x09],
            recv=[0x62, 0x41, 0x09] + write_power_list,
            do_assert=True,
        )
        sleep(1)
        read_power_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x41, 0x09] + local_date[3:]
        )
        if read_power_lsit != write_power_list:
            log_string = f"写入值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.full
    def test_caseid_1984485(self):
        '''4313驱动数量,只有1和2两驱和四驱'''
        self.doip_1002()
        self.sd_tester.send_request_and_recv_response([0x22, 0x43, 0x13])
        sleep(.1)
        self.sd_tester.send_request_and_recv_response([0x2E, 0x43, 0x13, 0x02])
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.doip_1002()
        self.sd_tester.send_data([0x22, 0x43, 0x13])
        date1 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        sleep(.1)
        self.sd_tester.send_request_and_recv_response([0x2E, 0x43, 0x13, 0x01])
        if date1[-1] != 2:
            assert 0, "本次写入的值未存储"

    @pytest.mark.full
    def test_caseid_1984482(self):
        '''7023方向盘加热控制'''
        self.doip_1002_level(3)
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x70, 0x23]
        )
        sleep(.1)
        write_power_list = [
            random.randint(0, 2),
            random.randint(0, 88),
            random.randint(0, 2),
            random.randint(0, 88),
            random.randint(0, 100),
            random.randint(0, 100),
            random.randint(0, 120),
            random.randint(0, 120),
            random.randint(0, 120),
        ]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x70, 0x23], write_power_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.doip_1002_level(3)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x70, 0x23],
            recv=[0x62, 0x70, 0x23] + write_power_list,
            do_assert=True,
        )
        sleep(.1)
        read_power_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x70, 0x23] + local_date[3:]
        )
        if read_power_lsit != write_power_list:
            log_string = f"写入值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.sanity
    def test_caseid_1984483(self):
        '''内灯模式存储'''
        self.ecu_interface.change_usage_mode_to_driving()
        self.s2sbaseclass.send_method_request(
            "LightService_client",
            "LightControl",
            {
                "lights": [
                    {
                        "light": {"type": 26, "zoneId": 0},
                        "mode": 2,
                        "brightness": 0,
                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0},
                    }
                ]
            },
        )
        sleep(1)
        self.s2sbaseclass.send_request_and_ck_resp(
            "LightService_client", "GetInternalLightMode", {}, {"out": 2}
        )
        self.reset_bgm()
        self.s2sbaseclass.send_request_and_ck_resp(
            "LightService_client", "GetInternalLightMode", {}, {"out": 2}
        )

    @pytest.mark.full
    def test_caseid_1984484(self):
        '''EE99喇叭开关触发喇叭的次数和时间'''
        self.doip_1002()
        self.sd_tester.send_data([0x22, 0xEE, 0x99])
        result1 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        self.io.set_do_level("horn_switch", True)  # 打开喇叭
        sleep(3)
        self.io.set_do_level("horn_switch", False)
        self.sd_tester.send_request_and_recv_response([0x22, 0xEE, 0x99])
        sleep(1)
        self.reset_bgm()
        self.sd_tester.send_data([0x22, 0xEE, 0x99])
        result2 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
        if result2[3] != result1[3] + 1:
            assert 0, "本次开关未存储"

    # @pytest.mark.full
    # def test_caseid_1984490(self):
    #     '''4200电动尾翼'''
    #     self.doip_1002_level(3)
    #     ret_code, local_date = self.sd_tester.send_request_and_recv_response(
    #         [0x22, 0x42, 0x00]
    #     )
    #     sleep(.1)
    #     write_power_list = [
    #         random.randint(0, 1),
    #         random.randint(0, 244),
    #         random.randint(0, 1),
    #         random.randint(0, 244),
    #     ]
    #     self.sd_tester.send_request_and_recv_response(
    #         [0x2E, 0x42, 0x00], write_power_list, do_assert=True
    #     )
    #     sleep(1)
    #     logger.info("bgm重启")
    #     self.reset_bgm()
    #     self.doip_1002_level(3)
    #     ret_code, read_date = self.sd_tester.send_request_and_recv_response(
    #         [0x22, 0x42, 0x00],
    #         recv=[0x62, 0x42, 0x00] + write_power_list,
    #         do_assert=True,
    #     )
    #     sleep(.1)
    #     read_power_lsit = read_date[3:]
    #     logger.info("恢复值")
    #     self.sd_tester.send_request_and_recv_response(
    #         [0x2E, 0x42, 0x00] + local_date[3:]
    #     )
    #     if read_power_lsit != write_power_list:
    #         log_string = f"写入电动尾翼值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
    #         logger.info(log_string)
    #         assert 0, log_string

    # def test_caseid_333(self):
    #     '''停车时间存储'''
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0)
    #     sleep(1)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBodyFr68, 'TiDrvgCycOff',)

    @pytest.mark.full
    def test_caseid_1984493(self):
        '''416D室内灯光白天至黑夜计时器存储'''
        self.doip_1002()
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0x6D]
        )
        sleep(.1)
        num = random.randint(0, 10000)
        num_hex = hex(num)[2:].zfill(4)
        write_list = [int(num_hex[i : i + 2], 16) for i in range(0, len(num_hex), 2)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x41, 0x6D], write_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.doip_1002()
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0x6D], recv=[0x62, 0x41, 0x6D] + write_list, do_assert=True
        )
        sleep(.1)
        read_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0x6D, 0x07, 0xD0])
        if read_lsit != write_list:
            log_string = (
                f"写入41F8值失败,读取结果本应为{bytes(write_list).hex()}实际为{bytes(read_lsit).hex()}"
            )
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.full
    def test_caseid_1984494(self):
        '''416E室内灯光黑夜至白天计时器存储'''
        self.doip_1002()
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0x6E])
        sleep(.1)
        num = random.randint(0, 10000)
        num_hex = hex(num)[2:].zfill(4)
        write_list = [int(num_hex[i : i + 2], 16) for i in range(0, len(num_hex), 2)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x41, 0x6E], write_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.doip_1002()
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0x6E], recv=[0x62, 0x41, 0x6E] + write_list, do_assert=True
        )
        sleep(.1)
        read_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0x6E, 0x07, 0xD0])
        if read_lsit != write_list:
            log_string = (
                f"写入416E值失败,读取结果本应为{bytes(write_list).hex()}实际为{bytes(read_lsit).hex()}"
            )
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.full
    def test_caseid_1984491(self):
        '''416F内灯白天至黑夜值'''
        self.doip_1002_level(3)
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0x6F])
        sleep(.1)
        num = random.randint(400, 700)
        num_hex = hex(num)[2:].zfill(4)
        write_list = [int(num_hex[i : i + 2], 16) for i in range(0, len(num_hex), 2)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x41, 0x6F], write_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.doip_1002_level(3)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0x6F], recv=[0x62, 0x41, 0x6F] + write_list, do_assert=True
        )
        sleep(.1)
        read_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0x6F, 0x07, 0xD0])
        if read_lsit != write_list:
            log_string = (
                f"写入值失败,读取结果本应为{bytes(write_list).hex()}实际为{bytes(read_lsit).hex()}"
            )
            logger.info(log_string)
            assert 0, log_string

    @pytest.mark.full
    def test_caseid_1984492(self):
        '''4170内灯黑夜至白天值'''
        self.doip_1002_level(3)
        self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0x70])
        sleep(.1)
        num = random.randint(800, 1300)
        num_hex = hex(num)[2:].zfill(4)
        write_list = [int(num_hex[i : i + 2], 16) for i in range(0, len(num_hex), 2)]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x41, 0x70], write_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm重启")
        self.reset_bgm()
        self.doip_1002_level(3)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x41, 0x70], recv=[0x62, 0x41, 0x70] + write_list, do_assert=True
        )
        sleep(.1)
        read_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0x70, 0x07, 0xD0])
        if read_lsit != write_list:
            log_string = (
                f"写入值失败,读取结果本应为{bytes(write_list).hex()}实际为{bytes(read_lsit).hex()}"
            )
            logger.info(log_string)
            assert 0, log_string

    # def test_caseid_1118(self):
    #     '''40D7动力关闭后需要等待8小时暂时不测'''
    #     self.doip_1002()
    #     self.sd_tester.send_data([0x22,0x40, 0xD7])
    #     self.sd_tester.return_udsdata_and_check_and_print_response_result()
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0)
    #     self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 0)

    #     self.sd_tester.change_usage_mode(0)
    #     self.sd_tester.change_usage_mode(2)
    #     self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattIQuiscAvgRaw', -10)
    #     self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattIQuiscFildLongRaw', -20)
    #     self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr04,'BattIQuiscFildShoRaw', -200)

    #     sleep(1)
    #     self.sd_tester.send_data([0x22,0x40, 0xD7])
    #     self.sd_tester.return_udsdata_and_check_and_print_response_result()

    # def test_caseid_1984489(self):
    #     '''DD01总里程写入的值需要比之前的值大'''
    #     self.doip_1002_level(3)
    #     logger.info("读取总里程")
    #     ret_code,local_date = self.sd_tester.send_request_and_recv_response([0x22, 0xDD, 0x01])
    #     if local_date[-1]!=255:
    #         write_date=local_date[-1]+1
    #         self.sd_tester.send_request_and_recv_response([0x2E, 0xDD, 0x01],write_date,do_assert=False)
    #         logger.info("bgm重启")

    #         self.reset_bgm()
    #         self.doip_1002_level(3)
    #         ret_code,local_date1 = self.sd_tester.send_request_and_recv_response([0x22, 0xDD, 0x01])
    #         if local_date1[:3] == local_date[:3]:
    #             log_string=f"写入值失败,读取结果本应为{bytes(write_date).hex()}实际为{bytes(local_date1).hex()}"
    #             logger.info(log_string)
    #             assert 0,log_string

    # def test_caseid_100374(self):
    #     '''abandon_to_inactive 主驾门打开'''
    #     self.set_usage_mode_to_abandoned()
    #     self.io.drvr_door_open()
    #     time.sleep(.3)
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr02,'DoorDrvrSts_2_CemBodySignalIPdu02',1)
    #     self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr01, 'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01', 'UsgModSts1_UsgModInActv')
    #     self.reset_bgm()
    #     self.check_usage_mode_status(1)

    # def test_usage_mode_caseid_100373(self):
    #     '''1.UsgMode == Abandoned
    #     2.通过[IF: MmedHdPwrMod] 判断娱乐系统有工作需求'''
    #     self.set_usage_mode_to_abandoned()
    #     self.ipdu.set(
    #         self.ipdu.infocanfd.CdcInfoCanFdFr03, 'MmedHdPwrMod', 5
    #     )
    #     self.check_usage_mode_status(1)
    #     self.reset_bgm()
    #     self.check_usage_mode_status(1)
