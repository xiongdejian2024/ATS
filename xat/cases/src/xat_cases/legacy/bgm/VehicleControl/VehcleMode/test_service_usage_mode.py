import os
import sys
import time
import pytest
import allure
from random import randint
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.sdk.bus_app import BusApp
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
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
@allure.story("整车模式/使用模式")
# @pytest.mark.flaky(reruns=3, reruns_delay=2)
class TestUsageMode(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        partner_process_check()
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)       
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.sd_tester.tester_present()
        self.ipdu.set_vehspd(0.0)
        sleep(1)
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟(数据库周期性报文和调度表)
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        # #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        # # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 1)
        self.s2sbaseclass = S2sBaseClass(
            [
                ("VehicleModeService", "client"), ('TailGateService' ,'client'), ('LightService' ,'client')
            ]
        )
        time.sleep(5)
        # self.nucapp.bgm_diag_line_down()

    def before_each_func(self,ecu):
        super().before_each_func(ecu, start=False)
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06',3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0)
        time.sleep(1)
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client',
            'SetUsageModeDown',
            {"mode": 1},
        )
        time.sleep(1)
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModInActv',
        )
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client',
            'SetCarMode',
            {"mode": 0},
        )
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr02 ,'VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02','CarModSts1_CarModNorm')
        time.sleep(1)
        self.ipdu.check(
             self.ipdu.backbonefr.CemBackBoneFr02 ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_0_CEMBackBoneSignalIpdu02',0)

    def after_each_func(self,ecu):
        super().after_each_func(ecu, start=True)
        # self.dk.set_central_lock(0x1)
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client',
            'SetCarMode',
            {"mode": 0},
        )
        time.sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr29, 'DCChrgnHndlSts', 0)
        self.io.drvr_door_close()
        self.io.pass_door_close()
        self.io.lere_door_close()
        self.io.rire_door_close()
        self.io.driver_seat_notpresent()
        self.io.set_do_level("hazard_switch", False)
        self.ipdu.resume_all_bus_send()
        
        

    def after_class(self, ecu):
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetUsageModeDown", {"mode": 1}
        )
        self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
        self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        self.s2sbaseclass.stop_operators()
        partner_process_check()
        self.nucapp.bgm_diag_line_up()
        super().after_class(self, ecu)
    
    def set_lock(self):
        # self.ipdu.pause_all_bus_send()
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 1)
        time.sleep(.5)
        # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 1)
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
    
    def gearAuto(self, gear_status=True):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr10, 'DrvrDesDirDrvrDesDir', 3)
        if gear_status == True:
            self.ipdu.set(self.ipdu.chassiscan1.AcuChas1Fr04, 'GearAutoShiftReq1', 3)
            self.ipdu.set(self.ipdu.chassiscan1.AcuChas1Fr04, 'GearAutoShiftReqSts1', 0)
            self.ipdu.set(self.ipdu.chassiscan1.AcuChas1Fr04, 'GearAutoShiftReqSts1', 1)
        else:
            self.ipdu.set(self.ipdu.chassiscan1.AcuChas1Fr04, 'GearAutoShiftReq1', 0)
            self.ipdu.set(self.ipdu.chassiscan1.AcuChas1Fr04, 'GearAutoShiftReqSts1', 0)
    
    def gearCdc(self, gear_status=True):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr10, 'DrvrDesDirDrvrDesDir', 3)
        if gear_status == True:
            self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr12, 'CDCDrvrGearShiftDirReq1UpDTipAut_0_CdcInfoCanFdSignalIPdu12', 0)
            self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr12, 'CDCDrvrGearShiftDirReq1UpTipAut_0_CdcInfoCanFdSignalIPdu12', 0)
            self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr12, 'CDCDrvrGearShiftDirReq1UpDTipAut_0_CdcInfoCanFdSignalIPdu12', 1)
            self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr12, 'CDCDrvrGearShiftDirReq1UpTipAut_0_CdcInfoCanFdSignalIPdu12', 1)
        else:
            self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr12, 'CDCDrvrGearShiftDirReq1UpDTipAut_0_CdcInfoCanFdSignalIPdu12', 0)
            self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr12, 'CDCDrvrGearShiftDirReq1UpTipAut_0_CdcInfoCanFdSignalIPdu12', 0)
        
    def gear(self, gear_status=True):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr10, 'DrvrDesDirDrvrDesDir', 3)
        if gear_status == True:
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr09, 'DrvrGearShiftDirReq1UpUpTipAut', 0)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr09, 'DrvrGearShiftDirReq1UpUpTipAut', 1)
        else:
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr09, 'DrvrGearShiftDirReq1UpUpTipAut', 0)
        
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
        result, realvalue, expectedvalue = self.ipdu.check(
            msg_signals_obj=msg_signals_obj,
            signal_name=signal_name,
            sig_value_name=expectedmode,
            do_assert=do_assert,
            timeout=timeout,
        )

        return result, realvalue, expectedvalue
    
    def check_car_mode_exhibition_and_exit(self, exhibition=True, do_assert=True, **kwargs):
        '''
        exhibition 为 True 校验 当前模式，验当前是展车模式，
        exhibition 为 False 校验 当前模式，验当前是非展车模式，
        @return: 返回 True 是展车模式，False 不是展车模式
        '''
        ipdu = kwargs.get('ipdu', self.ipdu)
        if ipdu:
            ipdu.set(
                ipdu.backbonefr.BcmVddmBackBoneFr00,
                'EpbStsEpbSts',
                3,
            )
            time.sleep(1)
        if exhibition:
            ck_info = {'out': {'isOpen': True, 'isValid': True}}
        else:
            ck_info = {'out': {'isOpen': False, 'isValid': True}}

        method_name = 'GetExhibitionModeSts'
        ret = self.s2sbaseclass.send_request_and_ck_resp(
            'VehicleModeService_client',
            method_name,
            {}, ck_info=ck_info
        )
        logger.info(f"VehicleModeService ck_info={ck_info}       ret={ret}")
        if exhibition:
            logger.info(F"当前为  {'展车模式' if ret else '非展车模式'}")
        else:
            logger.info(F"当前为  {'展车模式' if not ret else '非展车模式'}")
        if ret:
            return True
        else:
            return False
    
    def check_car_mode_exhibition(self, exhibition=True, do_assert=True, **kwargs):
        '''
        exhibition 为 True 校验 当前模式，验当前是展车模式，
        exhibition 为 False 校验 当前模式，验当前是非展车模式，
        @return: 返回 True 是展车模式，False 不是展车模式
        '''
        ipdu = kwargs.get('ipdu', self.ipdu)
        if ipdu:
            ipdu.set(
                ipdu.backbonefr.BcmVddmBackBoneFr00,
                'EpbStsEpbSts',
                3,
            )
            time.sleep(1)
        if exhibition:
            ck_info = {'out': {'isOpen': True, 'isValid': True}}
        else:
            ck_info = {'out': {'isOpen': False, 'isValid': True}}

        method_name = 'GetExhibitionModeSts'
        ret = self.s2sbaseclass.send_request_and_ck_resp(
            'VehicleModeService_client',
            method_name,
            {}, ck_info=ck_info
        )
        logger.info(f"VehicleModeService ck_info={ck_info}       ret={ret}")
        if exhibition:
            logger.info(F"当前为  {'展车模式' if ret else '非展车模式'}")
        else:
            logger.info(F"当前为  {'展车模式' if not ret else '非展车模式'}")

        if do_assert and not ret:
            assert 0, "模式不匹配"
        if ret:
            return True
        else:
            return False
    
    def set_car_mode_to_unexhibition(self, **kwargs):
        '''
        服务退出展车模式
        @return:
        '''
        ipdu = kwargs.get('ipdu', self.ipdu)
        if ipdu:
            ipdu.set(
                ipdu.backbonefr.BcmVddmBackBoneFr00,
                'EpbStsEpbSts',
                3,
            )
            time.sleep(1)
        method_name = "SetExhibitionMode"
        method_par = {"isOpen": False}
        self.partner_change_mode(method_name, method_par)
        # 校验 非展车模式
        ret = self.check_car_mode_exhibition(exhibition=False)
        return ret

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

    def set_lockunlock(self):
        # self.ipdu.pause_all_bus_send()
        time.sleep(.3)
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 1)
        # # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 1)
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
        # self.dk.set_cenlock_sts(0x1)
        # sleep(1)
        # self.dk.send_nfc_cmd()
        self.dk.set_cenlock_sts(0x3)
        sleep(1)
        self.dk.set_cenlock_sts(0x1)
        time.sleep(.3)
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
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02,'DoorDrvrSts_2_CemBodySignalIPdu02', 2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'DoorPassSts_2_CEMBodySignalIPdu11', 2)
        # self.ipdu.check_bus_recv_message('bodycan')
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02,'DoorLeReSts_1_CemBodySignalIPdu02', 2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'DoorRiReSts_1_CEMBodySignalIPdu11', 2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'TrSts_2_CEMBodySignalIPdu11', 2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06,'HoodSts', 2)
        # 4. 闭锁
        self.dk.set_cenlock_sts(0x3)
        time.sleep(1)
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
            # #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
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

    def reset_bgm(self):
        self.nucapp.bgm_power_off()
        time.sleep(1)
        self.nucapp.bgm_power_on()
        time.sleep(15)

    def change_usage_driving(self):
        '''切driving'''
        # self.set_lockunlock()
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        time.sleep(.5)
        # self.ipdu.backbonefr_vddmbackbonefr00_engst1wdstsengst1wdsts_engst1_runngrunng()
        self.check_usage_mode_status(UsageMode.DRIVING)
    
    def set_PtActvnReq(self, up_type):
        '''
        触发PtActvnReq置位
        up_type:0 gear, 1 geatAuto, 2 gearCdc ,3 setusagemodeup = 13, 4 setusagemodewithoutkey = 2
        '''
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'FOTAStatus', 0)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'StartInhibitSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'ImobEngSts1', 2)
        if up_type == 0:
            self.gear(True)
            time.sleep(0.7)
        elif up_type == 1:
            self.gearAuto(True)
            time.sleep(0.7)
        elif up_type == 2:
            self.gearCdc(True)    
        elif up_type == 3:
            self.s2sbaseclass.send_method_request('VehicleModeService_client', "SetUsageModeUp", {"mode": 13})
        elif up_type == 4:
            self.s2sbaseclass.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",{"mode": 2})
        time.sleep(0.3)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4)
        time.sleep(5)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr25, 'PtActvnReq1WdPtActvnReq', 1)


    # def test_01(self):
    #     self.dk.set_internal_has_key()
    #     self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr03, 'KeyReadStsToVMMNFCNFCKeyPrsnt', 3)
        # time.sleep(121)
        # self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr03, 'KeyReadStsToVMMNFCNFCKeyPrsnt', 3)


    # @pytest.mark.sanity
    # def test_inactive_storage_recovery_109942(self):
    #     '''inactive存储与恢复'''
    #     self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
    #     time.sleep(.7)
    #     self.reset_bgm()
    #     # self.s2sbaseclass.send_request_and_return_resp('VehicleModeService_client', "GetUsageMode", {})["out"]
    #     self.ipdu.check(
    #         self.ipdu.connectivitycanfd.VgmConnFr01,
    #         'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
    #         'UsgModSts1_UsgModInActv',
    #     )


    # @pytest.mark.sanity
    # def test_convenience_storage_recovery_109979(self):
    #     '''convenience存储与恢复'''
    #     self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
    #     time.sleep(1)
    #     self.ipdu.check(
    #         self.ipdu.backbonefr.CemBackBoneFr02,
    #         'VehModMngtGlbSafe1UsgModSts_0_CEMBackBoneSignalIpdu02',
    #         'UsgModSts1_UsgModCnvinc',
    #     )
    #     self.reset_bgm()
    #     self.ipdu.check(
    #         self.ipdu.backbonefr.CemBackBoneFr02,
    #         'VehModMngtGlbSafe1UsgModSts_0_CEMBackBoneSignalIpdu02',
    #         'UsgModSts1_UsgModCnvinc',
    #     )
    
    # @pytest.mark.sanity
    # def test_convenience_storage_recovery_1943277(self):
    #     '''convenience存储与恢复'''
    #     self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
    #     time.sleep(1)
    #     self.reset_bgm()
    #     self.ipdu.check(
    #         self.ipdu.connectivitycanfd.VgmConnFr01,
    #         'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
    #         'UsgModSts1_UsgModCnvinc',
    #     )

    # @pytest.mark.sanity
    # def test_active_norun_storage_recovery_110014(self):
    #     '''active存储与恢复'''
    #     self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
    #     time.sleep(1)
    #     self.reset_bgm()
    #     self.ipdu.check(
    #         self.ipdu.connectivitycanfd.VgmConnFr01,
    #         'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
    #         'UsgModSts1_UsgModActv',
    #     )
       

    @pytest.mark.sanity
    @pytest.mark.mcu_test
    def test_active_runn_storage_recovery_caseid_110155(self):
        '''active run 存储与恢复'''
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        time.sleep(1)
        self.reset_bgm()
        self.check_usage_mode_status(11)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        time.sleep(.3)
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModDrvg',
        )

    @pytest.mark.sanity
    @pytest.mark.mcu_test
    def test_driving_norun_storage_recovery_caseid_110049(self):
        '''driving norun 存储与恢复'''
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.check_usage_mode_status(13)
        time.sleep(1)
        self.reset_bgm()
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0
        )
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModActv',
        )

    @pytest.mark.sanity
    @pytest.mark.mcu_test
    @pytest.mark.nvm
    def test_driving_runn_storage_recovery_caseid_109990(self):
        '''driving running存储与恢复'''
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.check_usage_mode_status(13)
        time.sleep(1)
        self.reset_bgm()
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModDrvg',
        )

    # @pytest.mark.sanity
    # def test_abandon_storage_recovery_110016(self):
    #     '''abandon存储恢复'''
    #     self.set_usage_mode_to_abandoned()
    #     time.sleep(1)
    #     self.reset_bgm()
    #     self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr01, 'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01', 'UsgModSts1_UsgModAbdnd')

    @pytest.mark.sanity
    def test_inactive_to_convenice_caseid_110020(self):
        '''主驾门打开'''
        self.set_lockunlock()
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.io.drvr_door_open()
        time.sleep(.3)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02,'DoorDrvrSts_2_CemBodySignalIPdu02',1)
        time.sleep(6)
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModCnvinc',
        )

    @pytest.mark.sanity
    def test_inactive_to_convenice_caseid_110066(self):
        '''副驾门打开'''
        self.set_lockunlock()
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.io.pass_door_open()
        time.sleep(0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'DoorPassSts_2_CEMBodySignalIPdu11',1)
        time.sleep(6)
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModCnvinc',
        )

    @pytest.mark.sanity
    def test_inactive_to_convenice_caseid_115740(self):
        '''左后门打开'''
        self.set_lockunlock()
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.io.lere_door_open()
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02,'DoorLeReSts_1_CemBodySignalIPdu02',1)
        time.sleep(6)
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModCnvinc',
        )

    @pytest.mark.sanity
    def test_inactive_to_convenice_caseid_109944(self):
        '''右后门打开'''
        self.set_lockunlock()
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.io.rire_door_open()
        time.sleep(0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'DoorRiReSts_1_CEMBodySignalIPdu11',1)
        time.sleep(6)
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModCnvinc',
        )
#-------------------------------------------------------------------------------------
    @pytest.mark.sanity
    def test_inactive_to_convenice_caseid_109971(self):
        '''主驾占位'''
        self.set_lockunlock()
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        time.sleep(0.3)
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        # self.nucapp.driver_seat_present() 
        self.io.driver_seat_present()
        time.sleep(.3)
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr10, 'DrvrSeatSts', 2)
        time.sleep(6)
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModCnvinc',
        )

    @pytest.mark.sanity
    @pytest.mark.mcu_test
    def test_inactive_to_convenice_caseid_109930(self):
        '''刹车踏板踩下'''
        self.set_lockunlock()
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        # self.ipdu.check(self.ipdu.chassiscan1.VddmChas1Fr10,'BrkPedlPsdBrkPedlPsd', 1)
        time.sleep(6)
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModCnvinc',
        )

    @pytest.mark.sanity
    def test_driving_to_convenience_caseid_109994(self):
        '''driving 下切convenience 主驾门打开'''
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        time.sleep(1)
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 1)
        # self.ipdu.set(
        #     self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0
        # )
        self.io.drvr_door_open()
        time.sleep(.3)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02,'DoorDrvrSts_2_CemBodySignalIPdu02',1)
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModCnvinc',
        )

    @pytest.mark.sanity
    @pytest.mark.fail
    def test_driving_to_convenience_caseid_109996(self):
        '''左后门打开，主驾无占位'''
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.check_usage_mode_status(13)
        self.io.lere_door_open()
        self.io.driver_seat_notpresent()
        time.sleep(.3)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts_1_CemBodySignalIPdu02', 1)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr12, 'DrvrSeatSts', 1)
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModCnvinc',
        )


    @pytest.mark.sanity
    @pytest.mark.fail
    def test_driving_to_convenience_caseid_110127(self):
        '''右后门打开，主驾无占位'''
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.ipdu.backbonefr_vddmbackbonefr00_engst1wdstsengst1wdsts_engst1_runngrunng()
        time.sleep(.5)
        self.ipdu.backbonefr_vddmbackbonefr00_engst1wdstsengst1wdsts_engst1_runngrunng()
        self.check_usage_mode_status(UsageMode.DRIVING)
        self.io.rire_door_open()
        self.io.driver_seat_notpresent()
        time.sleep(.3)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr12, 'DrvrSeatSts', 1)
        # self.s2sbaseclass.send_request_and_return_resp('VehicleModeService_client', "GetUsageMode", {})["out"]
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModCnvinc',
        )

    @pytest.mark.sanity 
    @pytest.mark.full
    @pytest.mark.fail
    def test_driving_to_convenience_caseid_109922(self):
        '''副驾门打开，主驾无占位'''
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        time.sleep(.5)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.check_usage_mode_status(UsageMode.DRIVING)
        self.io.pass_door_open()
        self.io.driver_seat_notpresent()
        time.sleep(1)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr12, 'DrvrSeatSts', 1)
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModCnvinc',
        )

    @pytest.mark.sanity
    def test_convenience_to_inactive_caseid_110152(self):
        '''外部锁车'''
        self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
        self.set_lock()
        self.check_usage_mode_status(1)

    @pytest.mark.sanity
    def test_active_to_inactive_caseid_1912991(self):
        '''外部锁车110125'''
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        time.sleep(0.2)
        # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 1)
        self.set_lock()
        self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr12, 'LockgCenStsLockSt_2_VgmConnSignalIPdu12', 3, 2)
        time.sleep(0.5)
        self.check_usage_mode_status(1)
        
    @pytest.mark.sanity 
    @pytest.mark.full
    def test_active_to_inactive_caseid_1912990(self):
        '''高压下电'''
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        time.sleep(1)
        self.s2sbaseclass.send_method_request('VehicleModeService_client', "setHVOffSts", {"isOff":True})
        # self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1)
        self.check_usage_mode_status(1)

    @pytest.mark.sanity
    def test_convenience_to_inactive_caseid_110126(self):
        '''外部上锁'''
        self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
        self.set_lock()
        time.sleep(1)
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModInActv',
        )

    @pytest.mark.sanity
    # @pytest.mark.full
    @pytest.mark.longtime
    def test_convenience_to_inactive_caseid_110112(self):
        '''离车超时,座椅车门无变化需要等待15分钟'''
        self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        time.sleep(1)
        self.io.drvr_door_close()
        self.io.pass_door_close()
        self.io.lere_door_close()
        self.io.rire_door_close()
        self.io.trunk_door_close()
        self.io.hood_door1_close()
        time.sleep(900)
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModInActv',
        )


    @pytest.mark.sanity
    def test_inactive_to_active_caseid_1912992(self):
        '''长按危险警报灯开关同时踩下刹车超过15s'''
        # self.dk.set_internal_has_key()
        # return
        time.sleep(15)
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.set_lockunlock()
        self.dk.set_internal_has_key()
        time.sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.io.set_do_level("hazard_switch", True)  
        time.sleep(1)  
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr04,'SwtLiHzrdWarn', 1) 
        # self.ipdu.check(self.ipdu.chassiscan1.VddmChas1Fr10,'BrkPedlPsdBrkPedlPsd', 1)
        time.sleep(15)
        # self.s2sbaseclass.send_request_and_return_resp('VehicleModeService_client', "GetUsageMode", {})["out"]
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModActv',
        )
        self.dk.set_internal_no_key()

    # #该用例ms找不到
    # @pytest.mark.sanity
    # def test_abandon_to_inactive_1912995(self):
    #     '''用户携带钥匙接近'''
    #     self.set_usage_mode_to_abandoned()
    #     self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'UsgModChgReqFromBLE', 1)
    #     time.sleep(1)
    #     self.ipdu.check(
    #         self.ipdu.connectivitycanfd.VgmConnFr01,
    #         'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
    #         'UsgModSts1_UsgModInActv',
    #     )
    #     #钥匙
    #     self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'UsgModChgReqFromBLE', 0)
    #     # ConnectivityCANFD:0x198:UsgModChgReqFromBLE_ReqSts1 == 1 ReqSts1_Reqd

    @pytest.mark.sanity
    def test_active_to_inactive_caseid_115742(self):
        '''长按危险警报灯开关同时踩下刹车超过15s'''
        # self.set_lockunlock()
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.io.set_do_level("hazard_switch", True)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr04,'SwtLiHzrdWarn', 1) 
        # self.ipdu.check(self.ipdu.chassiscan1.VddmChas1Fr10,'BrkPedlPsdBrkPedlPsd', 1)
        # self.s2sbaseclass.send_request_and_return_resp('VehicleModeService_client', "GetUsageMode", {})["out"]
        time.sleep(15)
        self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr01, 'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01', 'UsgModSts1_UsgModInActv')

    # @pytest.mark.sanity
    # def test_abandon_to_inactive_1912997(self):
    #     '''主驾内门开按钮请求,内门间隔时间要短'''
    #     self.set_usage_mode_to_abandoned()
    #     self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'DoorDrvrOpenReqInsdSwt1', 1)
    #     self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrOpenReqInsdSwt2', 1)
    #     time.sleep(1)
    #     # self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr38, 'DoorLeReOpenReqInsdLogic_0_CemBackBoneSignalIPdu38', 1)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts_0_CEMBackBoneSignalIpdu02', 'UsgModSts1_UsgModInActv')

    # @pytest.mark.sanity
    # def test_abandon_to_inactive_doordrvropen_1912999(self):
    #     '''abandon_to_inactive 主驾门打开'''
    #     self.set_usage_mode_to_abandoned()
    #     self.io.drvr_door_open()
    #     time.sleep(.3)
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr02,'DoorDrvrSts_2_CemBodySignalIPdu02',1)
    #     # self.s2sbaseclass.send_request_and_return_resp('VehicleModeService_client', "GetUsageMode", {})["out"]
    #     self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr01, 'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01', 'UsgModSts1_UsgModInActv')
    
    # @pytest.mark.sanity
    # def test_abandon_to_inactive_doordrvropen_1912996(self):
    #     '''abandon_to_inactive 主驾外门按钮打开'''
    #     self.set_usage_mode_to_abandoned()
    #     self.io.drvr_door_outswitch_unpressed()
    #     self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrOpenReqOutdSwt2', 2)
    #     self.io.drvr_door_outswitch_pressed()
    #     self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrOpenReqOutdSwt2', 1)
    #     time.sleep(.3)
    #     self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr01, 'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01', 'UsgModSts1_UsgModInActv')
    #     self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrOpenReqOutdSwt2', 2)
    #     self.io.drvr_door_outswitch_unpressed()

    # @pytest.mark.smoke
    # @pytest.mark.full
    # @pytest.mark.sanity
    #台架不能io控制电压
    # def test_abandon_to_inactive_lin6_110131(self):
    #     '''abandon_to_inactive 有低压蓄电池补电需求'''
    #     self.set_usage_mode_to_abandoned()
    #     self.setvol(10)
    #     time.sleep(1)
    #     self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr01, 'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01', 'UsgModSts1_UsgModInActv')

    # @pytest.mark.sanity
    # def test_abandon_to_inactive_doordrvropen_1912998(self):
    #     '''abandon_to_inactive 收到制动踏板开关请求'''
    #     self.set_usage_mode_to_abandoned()
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
    #     time.sleep(1)
    #     self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr01, 'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01', 'UsgModSts1_UsgModInActv')
    
    # @pytest.mark.full
    # def test_abandon_to_inactive_doordrvropen_1978204(self):
    #     '''abandon_to_inactive ClimaOvrHeatPrtSts'''
    #     self.set_usage_mode_to_abandoned()
    #     self.ipdu.set(self.ipdu.bodycan.CcmBodyFr34, 'ClimaOvrHeatPrtSts', 'OnOff1_On')
    #     time.sleep(1)
    #     self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr01, 'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01', 'UsgModSts1_UsgModInActv')
    
    @pytest.mark.sanity
    def test_convenience_to_active_hazard_caseid_1912993(self):
        '''convenience_to_active 长按危险警报灯开关同时踩下刹车超过15s'''
        self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
        self.set_lockunlock()
        self.dk.set_internal_has_key()
        self.io.set_do_level("hazard_switch", True)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr04,'SwtLiHzrdWarn', 1) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        time.sleep(.5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        # self.ipdu.check(self.ipdu.chassiscan1.VddmChas1Fr10,'BrkPedlPsdBrkPedlPsd', 1)
        time.sleep(15)
        self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr01, 'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01', 'UsgModSts1_UsgModActv')
        self.dk.set_internal_no_key()

########################################################FULL用例######################################################################
    @pytest.mark.full
    @pytest.mark.fail
    def test_abandon_valid_Key_active_caseid_110158(self):
        '''服务代理接口上切UsageMode,UsgModKeeperReq >= Convenience'''
        self.set_usage_mode_to_abandoned()
        self.dk.set_internal_has_key()
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetUsageModeUp", {"mode": 11}
        )
        self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr01, 'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01', 'UsgModSts1_UsgModInActv')

    @pytest.mark.full
    @pytest.mark.fail
    def test_usage_mode_caseid_110034(self):
        '''服务代理接口上切UsageMode'''
        self.set_usage_mode_to_abandoned()
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetUsageModeUp", {"mode": 13}
        )
        self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr01, 'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01', 'UsgModSts1_UsgModInActv')

    @pytest.mark.full
    @pytest.mark.fail
    def test_usage_mode_caseid_110091(self):
        '''服务代理接口上切UsageMode'''
        self.set_usage_mode_to_abandoned()
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetUsageModeUp", {"mode": 1}
        )
        self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr01, 'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01', 'UsgModSts1_UsgModInActv')

    @pytest.mark.full
    @pytest.mark.fail
    def test_usage_mode_caseid_109973(self):
        '''服务代理接口上切UsageMode，usagemode>=convenice'''
        self.set_usage_mode_to_abandoned()
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetUsageModeUp", {"mode": 2}
        )
        self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr01, 'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01', 'UsgModSts1_UsgModInActv')

    # @pytest.mark.xfail
    @pytest.mark.full
    def test_usage_mode_caseid_110085(self):
        '''工厂模式，禁止进入Convenience'''
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client',
            'SetCarMode',
            {"mode": 2},
        )
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetUsageModeUp", {"mode": 2}
        )
        self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr01, 'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01', 'UsgModSts1_UsgModInActv')

    # @pytest.mark.xfail
    @pytest.mark.full
    def test_usage_mode_caseid_110092(self):
        '''运输模式，禁止进入Convenience'''
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client',
            'SetCarMode',
            {"mode": 1},
        )
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetUsageModeUp", {"mode": 2}
        )
        self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr01, 'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01', 'UsgModSts1_UsgModInActv')


    # @pytest.mark.full
    # def test_usage_mode_caseid_110156(self):
    #     '''工厂模式从Inactive超时进入Abandoned_'''
    #     #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
    #     # self.s2sbaseclass.send_method_request(
    #     #     'VehicleModeService_client', "SetUsageModeDown", {"mode": 1}
    #     # )
    #     self.s2sbaseclass.send_method_request(
    #         'VehicleModeService_client',
    #         'SetCarMode',
    #         {"mode": 2},
    #     )
    #     time.sleep(90)
    #     self.check_usage_mode_status(0)

    @pytest.mark.full
    @pytest.mark.fail
    def test_usage_mode_caseid_110100(self):
        '''1.远程泊车场景，触发动力系统启动
        1.PtActvnReq1WdPtActvnReq == True
        2.DrvrStrtReq == False'''
        # if self.check_car_mode_exhibition_and_exit(exhibition=True):
        #     self.set_car_mode_to_unexhibition()
        self.set_PtActvnReq(4)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'ChrgHndlStrtEna', 1)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.check_usage_mode_status(13)
    
    @pytest.mark.full
    @pytest.mark.new
    @pytest.mark.fail
    def test_usage_mode_caseid_110041(self):
        '''1.远程泊车场景，触发动力系统启动
        PrkgAssiSysRemPrkgSts == True'''
        # if self.check_car_mode_exhibition_and_exit(exhibition=True):
        #     self.set_car_mode_to_unexhibition()
        self.set_PtActvnReq(4)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'ChrgHndlStrtEna', 1)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.check_usage_mode_status(13)

    @pytest.mark.full
    @pytest.mark.fail
    def test_usage_mode_caseid_109972(self):
        '''1.PtActvnReq1WdPtActvnReq == True
            2.EngSt1WdSts1 == StrtgInProgs且超时
        '''
        # if self.check_car_mode_exhibition_and_exit(exhibition=True):
        #     self.set_car_mode_to_unexhibition()
        self.set_PtActvnReq(4)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'ChrgHndlStrtEna', 1)
        time.sleep(38)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr25, 'PtActvnReq1WdPtActvnReq', 1)
        time.sleep(2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr25, 'PtActvnReq1WdPtActvnReq', 0)
        

    @pytest.mark.full
    @pytest.mark.fail
    def test_usage_mode_caseid_110008(self):
        '''1.PtActvnReq1WdPtActvnReq == True
        2.EngSt1WdSts1等于RunngRunng或RunngStrtgInProgs或RunngStb'''
        self.set_PtActvnReq(4)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'ChrgHndlStrtEna', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr25, 'PtActvnReq1WdPtActvnReq', 0)
        self.check_usage_mode_status(13)

    @pytest.mark.full
    def test_usage_mode_caseid_110099(self):
        '''P档信号异常，用户下车自动触发EPB'''
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08,'VehParkNotActvd', 0)
        self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_undefd()
        self.io.drvr_door_open()
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08,'VehParkNotActvd', 1)

    @pytest.mark.full
    def test_usage_mode_caseid_110097(self):
        '''从Inactive进入Driving（RPA遥控泊车操作动力系统启动）'''
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.check_usage_mode_status(1)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 6
        )
        time.sleep(.3)
        self.s2sbaseclass.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",
                                         {"mode": 2})
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModDrvg',
        )

    @pytest.mark.full
    def test_usage_mode_caseid_110093(self):
        '''从Inactive进入Driving（本地操作动力系统启动）
        1.使用模式为未激活状态
        2. EngSt1WdSts1 == RunngRunng
        3.DrvrStrtReq = 本地启动请求'''
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.check_usage_mode_status(1)
        self.set_lockunlock()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'FOTAStatus', 0)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'StartInhibitSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'ImobEngSts1', 2)
        self.gearAuto(True)
        time.sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4
        )
        time.sleep(5)
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0
        )
        self.check_usage_mode_status(13)
        self.gearAuto(False)


    # @pytest.mark.full
    # @pytest.mark.xfail
    # def test_usage_mode_caseid_110082(self):
    #     '''从Abandoned进入Inactive收到灯功能触发的状态,反向验证灯触发无法下切abandon'''
    #     self.ipdu.set(
    #         self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsWelcomeTBD', 1
    #     )
    #     self.set_usage_mode_to_abandoned()
    #     self.check_usage_mode_status(0)

    @pytest.mark.full
    def test_usage_mode_caseid_110088(self):
        '''1.使用模式为舒享状态
            2. EngSt1WdSts1 == RunngStb
            3.PrkgAssiSysRemPrkgSts = 有效
        '''
        self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
        self.check_usage_mode_status(2)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 6
        )
        time.sleep(.3)
        self.s2sbaseclass.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",
                                         {"mode": 2})
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModDrvg',
        )

    @pytest.mark.full
    def test_usage_mode_caseid_110087(self):
        '''1.使用模式为舒享状态
            2. EngSt1WdSts1 == RunngStrtgInProgs
            3.PrkgAssiSysRemPrkgSts = 有效 RPA遥控泊车操作动力系统启动'''
        self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
        self.check_usage_mode_status(2)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 7
        )
        self.s2sbaseclass.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",
                                         {"mode": 2})
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModDrvg',
        )

    @pytest.mark.full
    def test_usage_mode_caseid_110103(self):
        '''1.使用模式为驾驶状态
            2.状态EngSt1WdSts3 != RunngStb
            '''
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetUsageModeUp", {"mode": 11}
        )
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModDrvg',
        )
        #动力异常，退出driving
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0
        )
        time.sleep(.5)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0
        )
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModActv',
        )     

    @pytest.mark.full
    def test_usage_mode_caseid_110064(self):
        '''1.使用模式为激活状态
            2.EngSt1WdSts2 == RunngStrtgInProgs
            '''
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 7
        )
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModDrvg',
        )

    # @pytest.mark.full
    # def test_usage_mode_caseid_110068(self):
    #     '''1.使用模式为未激活状态
    #         2.整车设防
    #         3.VehMtnSt == StandStill
    #         4.整车没有Inactive的唤醒源或者保持源持续一段时间 （标定量，默认60s）
    #     '''
    #     #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
    #     self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
    #     self.dk.set_cenlock_sts(0x3)
    #     time.sleep(60)
    #     self.check_usage_mode_status(0)

    @pytest.mark.full   
    def test_usage_mode_caseid_110146(self):
        '''1.使用模式为未激活状态
            2. EngSt1WdSts1 == RunngStrtgInProgs
            3.DrvrStrtReq = 本地启动请求
            '''
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.check_usage_mode_status(1)
        self.set_lockunlock()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'FOTAStatus', 0)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'StartInhibitSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'ImobEngSts1', 2)
        self.gearAuto(True)
        time.sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4
        )
        time.sleep(5)
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 7
        )
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0
        )
        self.check_usage_mode_status(13)
        self.gearAuto(False)

    # @pytest.mark.full
    # def test_usage_mode_caseid_110136(self):
    #     '''1.UsgMode == Abandoned
    #         2.通过[IF: HvOnMaiReq]判断动力系统有高压请求'''
    #     self.set_usage_mode_to_abandoned()
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr09, 'HvEgyLoadFctReq', 1)
    #     self.check_usage_mode_status(1)

    @pytest.mark.full
    def test_usage_mode_caseid_110107(self):
        '''1.使用模式为未激活状态
            2. EngSt1WdSts1 == RunngStb
            3.DrvrStrtReq = 本地启动请求
            '''
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.check_usage_mode_status(1)
        self.set_lockunlock()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'FOTAStatus', 0)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'StartInhibitSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'ImobEngSts1', 2)
        self.gearAuto(True)
        time.sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4
        )
        time.sleep(5)
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 6
        )
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0
        )
        self.check_usage_mode_status(13)
        self.gearAuto(False)

    @pytest.mark.full
    def test_usage_mode_caseid_109982(self):
        '''从Active进入Driving，'''
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        # self.ipdu.set(self.ipdu.bodycan.CEMBodyFr30, 'EngSt1WdStsEngSt1WdSts_1_CEMBodySignalIPdu30', 6)
        # time.sleep(.5)
        # self.ipdu.set(self.ipdu.bodycan.CEMBodyFr30, 'EngSt1WdStsEngSt1WdSts_1_CEMBodySignalIPdu30', 6)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 6
        )
        self.check_usage_mode_status(13)

    @pytest.mark.full
    def test_usage_mode_caseid_109981(self):
        '''从Driving进入Inactive动力异常
        1.使用模式为驾驶状态
        2.无钥匙下切'''
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        
        self.s2sbaseclass.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",
                                         {"mode": 2})
        self.check_usage_mode_status(13)
        self.s2sbaseclass.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",
                                         {"mode": 1})
        time.sleep(1)
        self.check_usage_mode_status(1)
        

    @pytest.mark.full
    def test_usage_mode_caseid_109902(self):
        '''从Active进入Driving'''
        
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.check_usage_mode_status(13)
    
    # @pytest.mark.full
    # def test_usage_mode_caseid_109903(self):
    #     '''1.UsgMode == Abandoned
    #     2.DoorPassOpenReqInsdSwt1==psd and DoorPassOpenReqInsdSwt1==psd
    #     3.通过[IF: DoorPassOpenReqInsdLogic]判断副驾内门开按钮请求'''
    #     self.set_usage_mode_to_abandoned()
    #     self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'DoorPassOpenReqInsdSwt1', 1)
    #     self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassOpenReqInsdSwt2', 1)
    #     time.sleep(.3)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr38, 'DoorPassOpenReqInsdLogic_0_CemBackBoneSignalIPdu38', 1)
    #     self.check_usage_mode_status(1)

    # @pytest.mark.full
    # def test_usage_mode_caseid_109891(self):
    #     '''1.UsgMode == Abandoned
    #     2.通过[IF: DoorRiReOpenReqOutdLogic]判断右后外外门开按钮请求'''
    #     self.set_usage_mode_to_abandoned()
    #     self.io.rire_door_outswitch_unpressed()
    #     self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiReOpenReqOutdSwt2', 2)
    #     self.io.rire_door_outswitch_pressed()
    #     self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiReOpenReqOutdSwt2', 1)
    #     time.sleep(.3)
    #     # expectedvalue = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr38, 'DoorRiReOpenReqOutdLogic')
    #     # assert expectedvalue == 1, "右后门未打开"
    #     self.check_usage_mode_status(1)
    #     self.io.rire_door_outswitch_unpressed()
    #     self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiReOpenReqOutdSwt2', 2)

    #不能实现自动化
    # def test_usage_mode_caseid_110145(self):
    #     '''1.UsgMode == Abandoned
    #         2.通过[IF: HvActvForVehModReq]判断高压系统有工作需求'''
    #     self.set_usage_mode_to_abandoned()
    #     self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr01, 'HvSysRlyStsHvSysRlySts', 0)
    #     self.s2sbaseclass.ck_s2s_event("HighVoltageService_client", "hvActiveSts", {"sts": 0}, timeout=1)
    
    # @pytest.mark.full
    # def test_usage_mode_caseid_110157(self):
    #     '''从Abandoned进入Inactive,HvEgyLoadFctReq高压请求'''
    #     self.set_usage_mode_to_abandoned()
    #     # self.s2sbaseclass.send_method_request('VehicleModeService_client', "setHVOffSts", {"isOff":False})
    #     # expectedvalue = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq')
    #     # assert expectedvalue == 0
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr09, 'HvEgyLoadFctReq', 1)
    #     self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr01, 'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01', 'UsgModSts1_UsgModInActv')
    
    #无法实现，电动门开关按下，门已打开
    # def test_usage_mode_caseid_110135(self):
    #     '''1.UsgMode == Abandoned
    #         2.通过[IF: DoorOpenerXXReq]判断电动门开关请求'''
    #     pass

    #进入abandon后位置灯无法打开，只能反向验证位置灯打开后无法进入abandon
    # def test_usage_mode_caseid_110114(self):
    #     '''1.UsgMode == Abandoned
    #         2.通过[IF: ExtrLtgSts] 判断位置灯处于打开状态'''
    #     self.set_usage_mode_to_abandoned()
    #     pass

    @pytest.mark.full
    def test_usage_mode_caseid_110119(self):
        '''1.使用模式为未激活状态
            2.车内有有效钥匙
            3.实体按键触发手动升档或者降档
            4.制动踏板被踩下'''
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.check_usage_mode_status(1)
        self.set_lockunlock()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'FOTAStatus', 0)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'StartInhibitSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'ImobEngSts1', 2)
        self.gear(True)
        time.sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4
        )
        time.sleep(5)
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0
        )
        self.check_usage_mode_status(13)
        self.gear(False)

    # @pytest.mark.full
    # def test_usage_mode_caseid_110073(self):
    #     '''1.UsgMode == Abandoned
    #         2.通过[IF: SwtLiHzrdWarn] 收到危险警告灯操作请求'''
    #     self.set_usage_mode_to_abandoned()
    #     self.io.hazard_light_open()
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr04, 'SwtLiHzrdWarn', 1)
    #     self.check_usage_mode_status(1)

    # @pytest.mark.full
    # def test_usage_mode_caseid_110062(self):
    #     '''1.UsgMode == Abandoned
    #         2.通过[IF: TelmFctReq] 判断车辆有远程工作需求'''
    #     self.set_usage_mode_to_abandoned()
    #     self.ipdu.set(
    #         self.ipdu.connectivitycanfd.TcamConnectivityFr35, 'TelmFctReq', 1)
    #     self.check_usage_mode_status(1)

    # @pytest.mark.full
    # def test_usage_mode_caseid_110059(self):
    #     '''1.UsgMode == Abandoned
    #         2.通过[IF: DoorLeReSts]判断左后门被打开'''
    #     self.set_usage_mode_to_abandoned()
    #     self.io.lere_door_open()
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'DoorLeReSts', 1)
    #     self.check_usage_mode_status(1)

    @pytest.mark.full
    def test_usage_mode_caseid_110050(self):
        '''从Driving进入Active（动力异常）
        1.使用模式为驾驶状态
        2.状态EngSt1WdSts2 != RunngStrtgInProgs'''
        self.change_usage_driving()
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0
        )
        self.check_usage_mode_status(11)

    # @pytest.mark.full
    # def test_usage_mode_caseid_110028(self):
    #     '''从Inactive进入Abandoned_外部锁车'''
    #     self.service_change_usage_mode_and_check_result(1)
    #     self.dk.set_central_lock(0x3)
    #     #断开诊断激活线
    #     self.nucapp.bgm_diag_line_down()
    #     self.nucapp.bgm_diag_line_down()
    #     self.nucapp.bgm_power_off()
    #     time.sleep(3)
    #     self.nucapp.bgm_power_on()
    #     time.sleep(60)
    #     self.check_usage_mode_status(0)
    #     #恢复诊断激活线
    #     self.nucapp.bgm_diag_line_up()

    # @pytest.mark.full
    # def test_usage_mode_caseid_109890(self):
    #     '''1.UsgMode == Abandoned
    #     2.通过[IF: LockgCenSts]判断车辆锁状态变更'''
    #     self.set_usage_mode_to_abandoned()
    #     self.set_lockunlock()
    #     self.check_usage_mode_status(1)

    # @pytest.mark.full
    # def test_usage_mode_caseid_109905(self):
    #     '''1.UsgMode == Abandoned
    #     2.通过[IF: AlrmSts] 判断车辆防盗报警触发'''
    #     self.set_usage_mode_to_abandoned()
    #     self.dk.set_central_lock(0x3)
    #     self.io.drvr_door_open()
    #     time.sleep(1)
    #     self.check_usage_mode_status(1)

    #无法实现自动化需要用蓝牙开，需实车操作
    # @pytest.mark.full
    # def test_usage_mode_caseid_109911(self):
    #     '''1.UsgMode == Abandoned
    #     2.通过[IF: TrOpenerReq] 收到车辆尾门操作请求'''
    #     self.set_usage_mode_to_abandoned()
    #     self.s2sbaseclass.send_method_request(
    #         'TailGateService_client', "Close", {}
    #     )
    #     self.check_usage_mode_status(1)

    # @pytest.mark.full
    # def test_usage_mode_caseid_109909(self):
    #     '''1.UsgMode == Abandoned
    #     2.通过[IF: DoorPassOpenReqOutdLogic]判断副驾外门开按钮请求'''
    #     self.set_usage_mode_to_abandoned()
    #     self.io.pass_door_outswitch_unpressed()
    #     self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassOpenReqOutdSwt2', 2)
    #     self.io.pass_door_outswitch_pressed()
    #     self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassOpenReqOutdSwt2', 1)
    #     time.sleep(0.3)
    #     self.check_usage_mode_status(1)
    #     self.io.pass_door_outswitch_unpressed()
    #     self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassOpenReqOutdSwt2', 2)

    @pytest.mark.full
    def test_usage_mode_caseid_109904(self):
        '''从Driving进入Convenience（用户插枪）'''
        self.change_usage_driving()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr29, 'DCChrgnHndlSts', 1)
        time.sleep(1)
        self.check_usage_mode_status(2)
        #恢复
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr29, 'DCChrgnHndlSts', 0)

    @pytest.mark.full
    def test_usage_mode_caseid_109906(self):
        '''1.使用模式为未激活状态
            2.车内有有效钥匙
            3.服务接口请求上切到Driving'''
        self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetUsageModeUp", {"mode": 13}
        )
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 1)

    @pytest.mark.full
    def test_usage_mode_caseid_110075(self):
        '''1.PtActvnReq1WdPtActvnReq == True
            2.IMMO认证超时'''
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'FOTAStatus', 0)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'StartInhibitSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'ImobEngSts1', 1)
        self.s2sbaseclass.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",
                                         {"mode": 2})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr25, 'PtActvnReq1WdPtActvnReq', 1)
        time.sleep(2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr25, 'PtActvnReq1WdPtActvnReq', 0)

    # @pytest.mark.full
    # def test_usage_mode_caseid_110149(self):
    #     '''从Inactive进入Abandoned_自行唤醒超时
    #         1.使用模式为未激活状态
    #         2.VehMtnSt == StandStill
    #         3.整车没有Inactive的所有唤醒源或者保持源持续一段时间 （默认3s）'''
    #     self.set_usage_mode_to_abandoned()
    #     self.ipdu.set(
    #         self.ipdu.connectivitycanfd.TcamConnectivityFr35, 'TelmFctReq', 1)
    #     self.check_usage_mode_status(1)
    #     self.ipdu.set(
    #         self.ipdu.connectivitycanfd.TcamConnectivityFr35, 'TelmFctReq', 0)
    #     time.sleep(3)
    #     self.check_usage_mode_status(0)

    # @pytest.mark.full
    def test_usage_mode_caseid_109955(self):
        '''
        1.使用模式为未激活状态
        2.VehMtnSt == StandStill
        3.CarModSts1 != 运输模式
        4.整车没有Inactive保持源的时间大于阈值（默认七分钟）
        '''
        self.self.s2sbaseclass.send_method_request(
            'VehicleModeService_client',
            'SetCarMode',
            {"mode": 5},
        )
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        lin_channel = kwargs.get("lin_channel", "cem_lin6")
        lin_id = kwargs.get("lin_id", 0x06)
        lin_msg = kwargs.get("lin_msg", [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
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
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02,'DoorDrvrSts_2_CemBodySignalIPdu02', 2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'DoorPassSts_2_CEMBodySignalIPdu11', 2)
        # self.ipdu.check_bus_recv_message('bodycan')
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02,'DoorLeReSts_1_CemBodySignalIPdu02', 2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'DoorRiReSts_1_CEMBodySignalIPdu11', 2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'TrSts_2_CEMBodySignalIPdu11', 2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06,'HoodSts', 2)
        # 4. 闭锁
        self.dk.set_cenlock_sts(0x3)
        time.sleep(420)
        self.check_usage_mode_status(0)

    # @pytest.mark.full
    def test_usage_mode_caseid_110148(self,**kwargs):
        '''1.使用模式为未激活状态
            2.VehMtnSt == StandStill
            3.CarModSts1 != 工厂模式
            4.整车没有Inactive保持源的时间大于阈值（默认七分钟）'''
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        lin_channel = kwargs.get("lin_channel", "cem_lin6")
        lin_id = kwargs.get("lin_id", 0x06)
        lin_msg = kwargs.get("lin_msg", [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
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
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02,'DoorDrvrSts_2_CemBodySignalIPdu02', 2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'DoorPassSts_2_CEMBodySignalIPdu11', 2)
        # self.ipdu.check_bus_recv_message('bodycan')
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02,'DoorLeReSts_1_CemBodySignalIPdu02', 2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'DoorRiReSts_1_CEMBodySignalIPdu11', 2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'TrSts_2_CEMBodySignalIPdu11', 2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06,'HoodSts', 2)
        # 4. 闭锁
        self.dk.set_cenlock_sts(0x3)
        time.sleep(420)
        self.check_usage_mode_status(0)


    @pytest.mark.full
    def test_usage_mode_caseid_110121(self):
        '''1.使用模式为舒享状态
            2.车内有有效钥匙
            3.自动换档功能
            4.制动踏板被踩下'''
        self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
        # self.set_lockunlock()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'FOTAStatus', 0)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'StartInhibitSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'ImobEngSts1', 2)
        self.gearAuto(True)
        time.sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4
        )
        time.sleep(5)
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0
        )
        self.check_usage_mode_status(13)
        self.gearAuto(False)
     
    @pytest.mark.full
    def test_usage_mode_caseid_110054(self):
        '''1.使用模式为未激活状态
            2.车内有有效钥匙
            3.服务接口请求上切到Driving'''
        self.set_lockunlock()
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1
        )
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'ImobEngSts1', 2)
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client', "SetUsageModeUp", {"mode": 13}
        )
        time.sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4
        )
        time.sleep(5)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.check_usage_mode_status(13)

    @pytest.mark.full
    def test_usage_mode_caseid_110052(self):
        '''1.使用模式为未激活状态
            2. EngSt1WdSts1 == RunngStrtgInProgs
            3.PrkgAssiSysRemPrkgSts = 有效'''
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 7
        )
        time.sleep(.3)
        self.s2sbaseclass.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",
                                         {"mode": 2})
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModDrvg',
        )

    # @pytest.mark.full   
    # def test_usage_mode_caseid_110051(self,**kwargs):
    #     '''
    #     从Inactive进入Abandoned_超时（工厂模式或运输模式）
    #     1.使用模式为未激活状态
    #     2.VehMtnSt == StandStill
    #     3.CarModSts1 == 运输模式
    #     4.整车没有Inactive保持源的时间大于阈值（默认一分钟）'''
    #     self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
    #     self.s2sbaseclass.send_method_request(
    #         'VehicleModeService_client',
    #         'SetCarMode',
    #         {"mode": 1},
    #     )
    #     lin_channel = kwargs.get("lin_channel", "cem_lin6")
    #     lin_id = kwargs.get("lin_id", 0x06)
    #     lin_msg = kwargs.get("lin_msg", [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
    #     logger.info("断开诊断激活线")
    #     self.nucapp.bgm_diag_line_down()
    #     self.nucapp.bgm_diag_line_down()
    #     self.nucapp.bgm_power_off()
    #     time.sleep(3)
    #     self.nucapp.bgm_power_on()
    #     time.sleep(20)
    #     # 2 发送lin 报文 补电
    #     self.ipdu.set(self.ipdu.cem_lin6.CemCem_Lin6Fr02, "BattSnsrStReq", 1)
    #     # ipdu.send_pdu("cem_lin6", 0x06, [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
    #     self.ipdu.send_pdu(lin_channel, lin_id, lin_msg)
    #     self.dk.set_cenlock_sts(0x3)
    #     time.sleep(60)
    #     self.check_usage_mode_status(0)

    @pytest.mark.full
    def test_usage_mode_caseid_110048(self):
        '''1.使用模式为舒享状态
            2. EngSt1WdSts1 == RunngStrtgInProgs
            3.DrvrStrtReq = 本地启动请求'''
        self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'FOTAStatus', 0)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'StartInhibitSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'ImobEngSts1', 2)
        self.gearAuto(True)
        time.sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4
        )
        time.sleep(5)
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 7
        )
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0
        )
        self.check_usage_mode_status(13)
        self.gearAuto(False)

    # @pytest.mark.full
    # def test_usage_mode_caseid_110046(self):
    #     '''1.UsgMode == Abandoned
    #         2.通过[IF: AlrmSts] 收到车辆解防或者设防状态'''
    #     self.set_usage_mode_to_abandoned()
    #     self.dk.set_central_lock(0x1)
    #     self.check_usage_mode_status(1)

    # @pytest.mark.full
    # def test_usage_mode_caseid_110045(self):
    #     '''1.UsgMode == Abandoned
    #         2.通过[IF: DoorLeReOpenReqOutdLogic]判断左后外门开按钮请求'''
    #     self.set_usage_mode_to_abandoned()
    #     self.io.lere_door_outswitch_unpressed()
    #     self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeReOpenReqOutdSwt2', 2)
    #     self.io.lere_door_outswitch_pressed()
    #     self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeReOpenReqOutdSwt2', 1)
    #     time.sleep(.3)
    #     self.check_usage_mode_status(1)
    #     self.io.lere_door_outswitch_unpressed()
    #     self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeReOpenReqOutdSwt2', 2)


    # @pytest.mark.full   
    # def test_usage_mode_caseid_110043(self):
    #     '''1.UsgMode == Abandoned
    #         2.通过[IF: EpbLampReqSec] 收到EPB备份开关操作请求'''
    #     self.set_usage_mode_to_abandoned()
    #     self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq', 1)
    #     self.check_usage_mode_status(1)
    #     #恢复
    #     self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq', 0)

    @pytest.mark.full
    def test_usage_mode_caseid_110040(self):
        '''1.使用模式非驾驶状态
            2.车辆模式非工厂驾驶模式
            3.变速器驻车锁状态未定义
            4.DriverStartRequest != Req 
            5.车辆处于StandStill
            6.主驾门开'''
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client',
            'SetCarMode',
            {"mode": 1},
        )
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, 'VehParkNotActvd', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 3)
        self.io.drvr_door_open()
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, 'VehParkNotActvd', 1)
        # time.sleep(3)
        # self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, 'VehParkNotActvd', 0)

    @pytest.mark.full
    def test_usage_mode_caseid_109897(self):
        '''
        1.使用模式非驾驶状态
        2.车辆模式非工厂暂停模式
        3.变速器驻车锁状态未定义
        4.DriverStartRequest != Req 
        5.车辆处于StandStill
        6.主驾门开'''
        self.s2sbaseclass.send_method_request(
            'VehicleModeService_client',
            'SetCarMode',
            {"mode": 2},
        )
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, 'VehParkNotActvd', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 3)
        self.io.drvr_door_open()
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, 'VehParkNotActvd', 1)
        # time.sleep(3)
        # self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, 'VehParkNotActvd', 0)

    @pytest.mark.full
    def test_usage_mode_caseid_110132(self):
        '''1.使用模式非驾驶状态
            2.车辆模式非轮毂(dyno)模式
            3.变速器驻车锁状态未定义
            4.DriverStartRequest != Req 
            5.车辆处于StandStill
            6.主驾门开'''
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, 'VehParkNotActvd', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 3)
        self.io.drvr_door_open()
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, 'VehParkNotActvd', 1)
        # time.sleep(3)
        # self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, 'VehParkNotActvd', 0)

    @pytest.mark.full
    def test_usage_mode_caseid_110037(self):
        '''1.使用模式为舒享状态
            2. EngSt1WdSts1 == RunngStb
            3.DrvrStrtReq = 本地启动请求'''
        self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'FOTAStatus', 0)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'StartInhibitSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'ImobEngSts1', 2)
        self.gearAuto(True)
        time.sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4
        )
        time.sleep(5)
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 6
        )
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0
        )
        self.check_usage_mode_status(13)
        self.gearAuto(False)


    # def test_usage_mode_caseid_110033(self):
    #     '''1.UsgMode == Abandoned
    #         2.通过[IF: MobDevAVPReq]判断AVP请求'''

    # @pytest.mark.full  
    # def test_usage_mode_caseid_110032(self):
    #     '''1.UsgMode == Abandoned
    #         2.DoorRiReOpenReqInsdSwt1==psd and DoorRiReOpenReqInsdSwt2 ==psd 注意_UB信号的值也应一致
    #         3.通过[IF: DoorRiReOpenReqInsdLogic]判断右后内门开按钮请求'''
    #     self.set_usage_mode_to_abandoned()
    #     self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'DoorRiReOpenReqInsdSwt1', 1)
    #     self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiReOpenReqInsdSwt2', 1)
    #     time.sleep(1)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr38, 'DoorRiReOpenReqInsdLogic_0_CemBackBoneSignalIPdu38', 1)
    #     self.check_usage_mode_status(1)

    # @pytest.mark.full
    # def test_usage_mode_caseid_110024(self):
    #     '''1.UsgMode == Abandoned
    #         2.通过[IF: EpbLampReq] 收到EPB开关操作请求'''
    #     self.set_usage_mode_to_abandoned()
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq', 1)
    #     self.check_usage_mode_status(1)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq', 0)

    @pytest.mark.full    
    def test_usage_mode_caseid_110021(self):
        '''1.使用模式为舒享状态
            2. EngSt1WdSts1 == RunngRunng
            3.DrvrStrtReq = 本地启动请求'''
        self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'FOTAStatus', 0)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'StartInhibitSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'ImobEngSts1', 2)
        self.gearAuto(True)
        time.sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4
        )
        time.sleep(5)
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0
        )
        self.check_usage_mode_status(13)
        self.gearAuto(False)

    @pytest.mark.full
    def test_usage_mode_caseid_110018(self):
        '''1.使用模式为未激活状态
            2.车内有有效钥匙
            3.自动换档功能
            4.制动踏板被踩下'''
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.set_lockunlock()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'FOTAStatus', 0)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'StartInhibitSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'ImobEngSts1', 2)
        self.gearAuto(True)
        time.sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4
        )
        time.sleep(5)
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0
        )
        self.check_usage_mode_status(13)
        self.gearAuto(False)

    # @pytest.mark.full  
    # def test_usage_mode_caseid_110015(self):
    #     '''1.UsgMode == Abandoned
    #     2.通过[IF: MmedHdPwrMod] 判断娱乐系统有工作需求'''
    #     self.set_usage_mode_to_abandoned()
    #     self.ipdu.set(
    #         self.ipdu.infocanfd.CdcInfoCanFdFr03, 'MmedHdPwrMod', 5
    #     )
    #     self.check_usage_mode_status(1)



    @pytest.mark.full
    def test_usage_mode_caseid_110011(self):
        '''1.使用模式为未激活状态
        2. EngSt1WdSts1 == RunngRunng
        3.PrkgAssiSysRemPrkgSts = 有效'''
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        time.sleep(.3)
        self.s2sbaseclass.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",
                                         {"mode": 2})
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModDrvg',
        )



    @pytest.mark.full
    def test_usage_mode_caseid_110006(self):
        '''1.使用模式为未激活状态
            2.车内有有效钥匙
            3.通过屏幕触发手动升档或者降档
            4.制动踏板被踩下'''
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.check_usage_mode_status(1)
        self.set_lockunlock()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'FOTAStatus', 0)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'StartInhibitSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'ImobEngSts1', 2)
        self.gearCdc(True)
        time.sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4
        )
        time.sleep(5)
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0
        )
        self.check_usage_mode_status(13)
        self.gearCdc(False)

    @pytest.mark.full
    def test_usage_mode_caseid_110044(self):
        '''1.使用模式为舒享状态
            2.车内有有效钥匙
            3.实体按键触发手动升档或者降档
            4.制动踏板被踩下'''
        self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'FOTAStatus', 0)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'StartInhibitSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'ImobEngSts1', 2)
        self.gear(True)
        time.sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4
        )
        time.sleep(5)
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0
        )
        self.check_usage_mode_status(13)
        self.gear(False)
        
    @pytest.mark.full
    def test_usage_mode_caseid_110065(self):
        '''1.使用模式为激活状态
            2.车内有有效钥匙
            3.实体按键触发手动升档或者降档
            4.制动踏板被踩下'''
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'FOTAStatus', 0)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'StartInhibitSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'ImobEngSts1', 2)
        self.gear(True)
        time.sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4
        )
        time.sleep(5)
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0
        )
        self.check_usage_mode_status(13)
        self.gear(False)
    
    @pytest.mark.full
    def test_usage_mode_caseid_110143(self):
        '''1.使用模式为激活状态
            2.车内有有效钥匙
            3.屏幕按键触发手动升档或者降档
            4.制动踏板被踩下'''
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'FOTAStatus', 0)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'StartInhibitSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'ImobEngSts1', 2)
        self.gearCdc(True)
        time.sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4
        )
        time.sleep(5)
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0
        )
        self.check_usage_mode_status(13)
        self.gearCdc(False)

    @pytest.mark.full
    def test_usage_mode_caseid_110151(self):
        '''1.使用模式为舒享状态
            2.车内有有效钥匙
            3.通过屏幕触发手动升档或者降档
            4.制动踏板被踩下'''
        self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'FOTAStatus', 0)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'StartInhibitSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'ImobEngSts1', 2)
        self.gearCdc(True)
        time.sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4
        )
        time.sleep(5)
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0
        )
        self.check_usage_mode_status(13)
        self.gearCdc(False)

    # @pytest.mark.full      
    # def test_usage_mode_caseid_109998(self):
    #     '''1.UsgMode == Abandoned
    #         2.通过[IF: TrSts]判断尾门被打开'''
    #     self.set_usage_mode_to_abandoned()
    #     self.io.trunk_door_open()
    #     self.check_usage_mode_status(1)

    @pytest.mark.full    
    @pytest.mark.fail
    def test_usage_mode_caseid_109995(self):
        '''1.直流充电枪未拔出'''
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr29, 'DCChrgnHndlSts', 1)
        # self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        # self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        # self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        # self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'ChrgHndlStrtEna', 0)
        # self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr09, 'DrvrGearShiftDirReq1UpUpTipAut', 1)
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.check_usage_mode_status(1)
        self.set_lockunlock()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.set_PtActvnReq(1)
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 1
        )
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'ChrgHndlStrtEna', 0)
        # self.ipdu.set(
        #     self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        # )
        # self.ipdu.check(
        #     self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0
        # )
        # self.check_usage_mode_status(13)
        self.gearAuto(False)

    @pytest.mark.full
    @pytest.mark.fail
    def test_usage_mode_caseid_109993(self):
        '''1.使用模式为驾驶状态
        2.状态EngSt1WdSts1 != RunngRunng'''
        self.change_usage_driving()
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 3
        )
        self.check_usage_mode_status(11)

    # @pytest.mark.full
    # def test_usage_mode_caseid_109991(self):
    #     '''1.UsgMode == Abandoned
    #     3.通过[IF: DoorPassSts]判断副驾门被打开'''
    #     self.set_usage_mode_to_abandoned()
    #     self.io.pass_door_open()
    #     time.sleep(0.5)
    #     self.check_usage_mode_status(1)


    # #无法实现自动化
    # def test_usage_mode_caseid_109989(self):
    #     '''1.UsgMode == Abandoned
    #     2.通过[IF: MobDeBtnCarLctrSts]收到寻车指令'''

    # @pytest.mark.full
    # def test_usage_mode_caseid_109986(self):
    #     '''
    #     1.UsgMode == Abandoned
    #     2.DoorLeReOpenReqInsdSwt1==psd and DoorLeReOpenReqInsdSwt2==psd
    #     3.通过[IF: DoorLeReOpenReqInsdLogic]判断左后内门开按钮请求
    #     '''
    #     self.set_usage_mode_to_abandoned()
    #     self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'DoorLeReOpenReqInsdSwt1', 1)
    #     self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeReOpenReqInsdSwt2', 1)
    #     time.sleep(1)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr38, 'DoorLeReOpenReqInsdLogic_0_CemBackBoneSignalIPdu38', 1)
    #     self.check_usage_mode_status(1)



    @pytest.mark.full
    @pytest.mark.fail
    def test_usage_mode_caseid_109985(self):
        '''
        1.使用模式为驾驶状态
        2.EngSt1WdSts1 != RunngStb
        3.下高压
        '''
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        self.change_usage_driving()
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.s2sbaseclass.send_method_request('VehicleModeService_client', "setHVOffSts", {"isOff":True})
        # self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1)
        # time.sleep(305)
        self.check_usage_mode_status(1)

    @pytest.mark.full
    @pytest.mark.longtime
    def test_usage_mode_caseid_109966(self):
        '''
        1.使用模式为驾驶状态
        2.EngSt1WdSts1 != RunngRunng
        3.车辆处于StandStill，且超过超过300s
        '''
        self.change_usage_driving()
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        time.sleep(300)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 2
        )
        self.check_usage_mode_status(1)

    # @pytest.mark.full
    # def test_usage_mode_caseid_109977(self):
    #     '''
    #     1.UsgMode == Abandoned
    #     2.通过[IF: IndcrSts] 收到危险警告灯开关状态（处于打开状态）
    #     '''
    #     self.set_usage_mode_to_abandoned()
    #     self.io.set_do_level("hazard_switch", True)
    #     time.sleep(1)
    #     self.check_usage_mode_status(1)

    # @pytest.mark.full
    # def test_usage_mode_caseid_109976(self):
    #     '''
    #     1.UsgMode == Abandoned
    #     2.通过[IF: PtCoolgPostRunActv] 判断车辆有动力系统热管理工作需求
    #     '''
    #     self.set_usage_mode_to_abandoned()
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'PtCoolgPostRunActv', 1)
    #     self.check_usage_mode_status(1)
    #不能实现自动化
    # def test_usage_mode_caseid_109975(self):
    #     '''
    #     1.UsgMode == Abandoned
    #     2.通过[IF: FOTAStatus]判断FOTA状态
    #     '''


    @pytest.mark.full
    def test_usage_mode_caseid_109960(self):
        '''
        1.DrvrStrtReq] == Reqd
        2.有禁止启动请求,进展车
        '''
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,'EpbStsEpbSts',3)
        self.s2sbaseclass.send_method_request(
                'VehicleModeService_client',
                'SetExhibitionMode',
                {"isOpen": True},
            )
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'FOTAStatus', 0)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'StartInhibitSts', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'ImobEngSts1', 2)
        self.gear(True)
        time.sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4
        )
        time.sleep(5)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0)
        #恢复
        self.s2sbaseclass.send_method_request(
                'VehicleModeService_client',
                'SetExhibitionMode',
                {"isOpen": False},
            )
        
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,'EpbStsEpbSts',0)
        self.gear(False)

    # @pytest.mark.full
    # def test_usage_mode_caseid_109952(self):
    #     '''
    #     1.UsgMode == Abandoned
    #     2.通过[IF: RemHvStrtActvReq]判断互联子系统有高压请求
    #     '''
    #     self.set_usage_mode_to_abandoned()
    #     self.ipdu.set(self.ipdu.connectivitycanfd.TcamConnectivityFr12, 'RemHvStrtActvReq_0_TcamConnectivitySignalIPdu12', 1)
    #     self.check_usage_mode_status(1)

    # @pytest.mark.full
    # def test_usage_mode_caseid_109936(self):
    #     '''
    #     1.UsgMode == Abandoned
    #     2.通过[IF: DrvrGearShiftParkReq]判断P挡按钮被按下
    #     '''
    #     self.set_usage_mode_to_abandoned()
    #     self.ipdu.set(self.ipdu.propulsioncan.EgsmPropFr01, 'DrvrGearShiftParkReq1', 1)
    #     self.check_usage_mode_status(1)

    @pytest.mark.full
    @pytest.mark.fail
    def test_usage_mode_caseid_109935(self):
        '''
        1.使用模式为激活状态
        2.车内有有效钥匙
        3.自动换档功能
        4.制动踏板被踩下
        '''
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.set_PtActvnReq(0)
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0
        )
        self.check_usage_mode_status(13)
        self.gear(False)

    @pytest.mark.full
    @pytest.mark.fail
    def test_usage_mode_caseid_110012(self):
        '''1.使用模式为激活状态
        2.车内有有效钥匙
        3.服务接口请求上切到Driving'''
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.set_PtActvnReq(3)
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0
        )
        self.check_usage_mode_status(13)

    @pytest.mark.full
    def test_usage_mode_caseid_109931(self):
        '''
        1.使用模式为舒享状态
        2. EngSt1WdSts1 == RunngRunng
        3PrkgAssiSysRemPrkgSts = 有效
        '''
        self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        time.sleep(.3)
        self.s2sbaseclass.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",
                                         {"mode": 2})
        self.ipdu.check(
            self.ipdu.connectivitycanfd.VgmConnFr01,
            'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01',
            'UsgModSts1_UsgModDrvg',
        )

    # @pytest.mark.full
    # def test_usage_mode_caseid_109929(self):
    #     '''
    #     1.UsgMode == Abandoned
    #     2.通过[IF: DoorRiReSts]判断右后门被打开
    #     '''
    #     self.set_usage_mode_to_abandoned()
    #     self.io.rire_door_open()
    #     # expectedvalue = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr38, 'DoorRiReOpenReqOutdLogic')
    #     # assert expectedvalue == 1, "右后门未打开"
    #     self.check_usage_mode_status(1)

    @pytest.mark.full
    def test_usage_mode_caseid_109913(self):
        '''
        1.使用模式非驾驶状态
        2.驱动程序启动请求!= Req
        3.车辆处于StandStill4.变速器驻车锁状态 == ParkNotEngd
        5.主驾门关
        '''
        self.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 0)
        self.io.drvr_door_close()
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'DoorDrvrStsWithFacQlyDoorSts', 2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr19, 'VehNotParkInfoWarn', 2)
    
    @pytest.mark.full
    def test_usage_mode_caseid_109895(self):
        '''
        1.使用模式非驾驶状态
        2.驱动程序启动请求!= Req
        3.车辆处于StandStill
        4.变速器驻车锁状态 == ParkNotEngd
        5.主驾门开
        '''
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 0)
        self.io.drvr_door_open()
        time.sleep(.5)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'DoorDrvrStsWithFacQlyDoorSts', 1)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr19, 'VehNotParkInfoWarn', 1)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr25, 'AudWarn', 1)
    
    @pytest.mark.full
    @pytest.mark.fail
    def test_usage_mode_caseid_1980869(self):
        '''从Driving进入Inactive_P档15分钟下切
        1.使用模式为驾驶状态
        2.P档15分钟下切'''
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        
        self.s2sbaseclass.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",
                                         {"mode": 2})
        self.check_usage_mode_status(13)
        time.sleep(880)
        self.check_usage_mode_status(13)
        time.sleep(21)
        self.check_usage_mode_status(1)
    
    @pytest.mark.full
    @pytest.mark.longtime
    def test_usage_mode_caseid_1980868(self):
        '''Driving下切Inactive_泊车后服务下切再上切Driving,P档15分钟不下切
        1.使用模式为驾驶状态
        2.P档15分钟下切'''
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        
        self.s2sbaseclass.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",
                                         {"mode": 2})
        self.check_usage_mode_status(13)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1)
        time.sleep(1)
        self.s2sbaseclass.send_method_request('VehicleModeService_client', "SetUsageModeDown",
                                         {"mode": 1})
        time.sleep(1)
        self.check_usage_mode_status(1)
        self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'FOTAStatus', 0)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'StartInhibitSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'ImobEngSts1', 2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1)
        self.gearAuto(True)
        time.sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4
        )
        time.sleep(5)
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0
        )
        self.check_usage_mode_status(13)
        self.gearAuto(False)
        time.sleep(880)
        self.check_usage_mode_status(13)
        time.sleep(21)
        self.check_usage_mode_status(13)
    
    @pytest.mark.full
    @pytest.mark.longtime
    @pytest.mark.withoutkey
    def test_usage_mode_caseid_1980867(self):
        '''Driving下切Inactive_泊车后开门下切再上切Driving,P档15分钟不下切
        1.使用模式为驾驶状态
        2.P档15分钟下切'''
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        
        self.s2sbaseclass.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",
                                         {"mode": 2})
        self.check_usage_mode_status(13)
        time.sleep(1)
        self.io.drvr_door_open()
        time.sleep(1)
        self.check_usage_mode_status(2)
        self.io.drvr_door_close()
        self.s2sbaseclass.send_method_request('VehicleModeService_client', "SetUsageModeDown",
                                         {"mode": 1})
        time.sleep(1)
        self.check_usage_mode_status(1)
        self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'FOTAStatus', 0)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'StartInhibitSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'ImobEngSts1', 2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1)
        self.gearAuto(True)
        time.sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4
        )
        time.sleep(5)
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0
        )
        self.check_usage_mode_status(13)
        self.gearAuto(False)
        time.sleep(880)
        self.check_usage_mode_status(13)
        time.sleep(21)
        self.check_usage_mode_status(13)
    
    @pytest.mark.full
    @pytest.mark.longtime
    @pytest.mark.withoutkey
    def test_usage_mode_caseid_1980866(self):
        '''Driving下切Inactive_泊车后无钥匙下切再上切Driving,P档15分钟不下切
        1.使用模式为驾驶状态
        2.P档15分钟下切'''
        self.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        
        self.s2sbaseclass.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",
                                         {"mode": 2})
        self.check_usage_mode_status(13)
        time.sleep(1)
        self.s2sbaseclass.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",
                                         {"mode": 1})
        time.sleep(1)
        self.check_usage_mode_status(1)
        self.service_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'FOTAStatus', 0)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'StartInhibitSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'ImobEngSts1', 2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1)
        self.gearAuto(True)
        time.sleep(1)
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4
        )
        time.sleep(5)
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 1
        )
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5
        )
        self.ipdu.check(
            self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'DrvrStrtReq', 0
        )
        self.check_usage_mode_status(13)
        self.gearAuto(False)
        time.sleep(880)
        self.check_usage_mode_status(13)
        time.sleep(21)
        self.check_usage_mode_status(13)