# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_ExtiLight_ctrl.py
@Time         :2023/07/21 17:20:31
@Author       :webnlong.xing
@Description  :
"""
import allure,time
import pytest
import copy
import uuid
import threading
from time import sleep
from random import randint
from xat_ecu.legacy.sdk.digital_key.digital_key_const import *
from xat_ecu.legacy.common.data_type_handing import logger, DataTypeHanding
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey
from xat_ecu.legacy.soa_partner.src.base_partner import S2sBaseClass
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
# from test_case.soa.case_helper.partner_const import *
from xat_cases.legacy.bgm.VehicleControl.case_helper.common_lib_bgm import *
# from test_case.tcam.tcam_back.rvcremote.remotectrl import *

start_get_service_flag=1 #后台周期调用get接口1启动0停止
LIGHT_SERVICE_CLIENT = "LightService_client"
KEY_SERVICE_CLIENT = "KeyService_client"
@allure.feature("整车控制")
@allure.story("整车控制/灯控制/外灯控制")
@pytest.mark.full
class TestExtiLightfunction(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        partner_process_check()  # 检查上位机上是否有其它未关闭的soa_partner进程在运行，如果有，则杀死进程
        sleep(1)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.nucapp.bgm_diag_line_up()  # 诊断激活线连接
        self.partner = S2sBaseClass([("LightService", "client"), ("KeyService", "client")])
        sleep(2)
        self.ipdu.start_all_time_control()  # 启动数据模拟(数据库周期性报文和调度表)
        self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.diagnostic_client_sim_start()
        self.sd_tester.tester_present()
        self.vid = self.tb_config["vid"]
        self.tel = self.tb_config["tel"]
        # self.rc = RemoteCtrl(self.vid, self.tel)


    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        try:
            self.sd_tester.change_usage_mode(1)
            self.sd_tester.change_car_mode(0)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
        self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        self.sd_tester.stop_tester_present()
        self.sd_tester.diagnostic_client_sim_close()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        with allure.step("周期调用获取外灯禁用状态启动"):
            receiver_thread = threading.Thread(target=self.get_result,args=()) #周期调获取外灯禁用状态
            receiver_thread.start() #周期调获取外灯禁用状态
            logger.info("\033[0;33;40m开始周期调用检查↑\033[0m")
        with allure.step("使用模式normal inactive"):
            # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
            # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
            # self.ipdu.backbonefr_vddmbackbonefr03_gearlvrindcn_gearlvrindcn2_parkindcn()
            
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 0)
            self.partner.empty_all()  # 清空partner所有缓存数据
            self.ipdu.set(
                self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 0
            )
            self.ipdu.set(
                self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 0
            )
            self.ipdu.set(
                self.ipdu.backbonefr.BcmVddmBackBoneFr06,
                'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06',
                3,
            )
            self.ipdu.set(
                self.ipdu.backbonefr.BcmVddmBackBoneFr06,
                'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06',
                0,
            )
        with allure.step("切到白天"):
            self.ipdu.cem_lin1_rlsmcem_lin1fr01_twlibrirawtwlibriraw_0_rlsmcem_lin1signalipdu01_value(1000)

            sleep(1)
            self.ipdu.cem_lin1_rlsmcem_lin1fr01_twlibrirawqf_0_rlsmcem_lin1signalipdu01_genqf1_accurdata()
            sleep(1)
            self.ipdu.cem_lin1_rlsmcem_lin1fr01_outdbrists_outdbrists_day()
            logger.info("\033[0;35;40m设置RLSM白天模式\033[0m")
        sleep(1)
        with allure.step("外灯设置无故障"):
            """近光OFF"""
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedLoBeamLe', 0
            )  # 设置HCML近光状态0关1开2故障;
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedLoBeamRi', 0
            )  # 设置HHCMR近光状态0关1开2故障;
            logger.info("\033[0;33;40m设置HCM近光状态0关\033[0m")
            """远光OFF"""
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedHiBeamLe', 0
            )  # 设置HCML远光状态0关1开2故障
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedHiBeamRi', 0
            )  # 设置HCMR远光状态0关1开2故障
            logger.info("\033[0;31;40m设置HCM远光状态0关\033[0m")
            """位置灯OFF"""
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLedFrntPosnLampLe', 0
            )
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr04, 'StsOfLedFrntPosnLampRi', 0
            )
            logger.info("\033[0;32;40m设置HCM位置灯状态0关\033[0m")
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedPosnLampLe1', 0
            )
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedPosnLampRi1', 0
            )
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.RcmmBodyExpoFr02, 'StsOfLedPosnLampMid', 0
            )
            logger.info("\033[0;32;40m设置RCM位置灯状态0关\033[0m")
            """后雾灯"""
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReFogLampLe1', 0
            )
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReFogLampRi1', 0
            )
            logger.info("\033[0;33;40m设置RCM后雾灯状态0关\033[0m")
            """转向灯"""
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLedFrntTurnIndcrLe', 0
            )
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr04, 'StsOfLedFrntTurnIndcrRi', 0
            )
            logger.info("\033[0;34;40m设置HCM前转向灯状态0关\033[0m")
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedTurnIndcrLe1', 0
            )
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedTurnIndcrRi1', 0
            )
            logger.info("\033[0;34;40m设置RCM后转向灯状态0关\033[0m")
            """日行灯"""
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLedDaytiRunngLampLe', 0
            )
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr04, 'StsOfLedDaytiRunngLampRi', 0
            )
            logger.info("\033[0;35;40m设置HCM日行灯状态0关\033[0m")
            """灯组"""
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntLampLe1', 0
            )
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntLampLe2', 0
            )
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntLampMid1', 0
            )
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedFrntLampRi1', 0
            )
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedFrntLampRi2', 0
            )
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReLampLe1', 0
            )
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReLampLe2', 0
            )
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReLampRi1', 0
            )
            self.ipdu.set(
                self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReLampRi2', 0
            )
            logger.info("\033[0;36;40m设置灯光秀灯组状态0关\033[0m")
            self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedRvsgLampLe1', 'DevSts4_Off')#左侧倒车灯
            self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedRvsgLampRi1', 'DevSts4_Off')#右侧倒车灯
        with allure.step("按键无触发"):
            """远光灯按键"""
            self.ipdu.set(
                self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 0
            )  # 老方向盘远光按键发0关1超车2远光
            logger.info("\033[0;33;40m老方向盘远光按键发0关\033[0m")
            self.ipdu.set(
                self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi1SteerWhlTouchSwt2', 0
            )  # 新方向盘远光按键发0关1超车2远光
            logger.info("\033[0;33;40m新方向盘远光按键发0关\033[0m")
            """转向灯按键"""
            self.ipdu.bodycan_swtrbodyfr01_steerwhltouchswtri2steerwhltouchswt2_steerwhltouchswt_notavailble()
            logger.info("\033[0;33;40m老方向盘右转按键发0关\033[0m")
            self.ipdu.bodycan_swtlbodyfr01_steerwhltouchswtle2steerwhltouchswt2_steerwhltouchswt_notavailble()
            logger.info("\033[0;33;40m新老方向盘左转按键发0关\033[0m")
            self.ipdu.bodycan_swtlbodyfr02_steerwhltouchswtle1steerwhltouchswt2_steerwhltouchswt_notavailble()
            logger.info("\033[0;33;40m新方向盘右转按键发0关\033[0m")
        with allure.step("检查双闪如果打开手动关闭"):
            result, realvalue, expectedvalue = self.ipdu.check(
                getattr(getattr(self.ipdu, 'bodycan'), 'CemBodyFr03'),
                'ActvnOfIndcrIndcrOut_1_CemBodySignalIPdu03',
                3,
                do_assert=False,
            )
            if result == True:
                # self.io.hazard_light_open()
                self.io.set_do_level("hazard_switch", True)
                logger.info("\033[0;33;40mHWL按键按下\033[0m")
                sleep(0.1)
                # self.io.hazard_light_close()
                self.io.set_do_level("hazard_switch", False)
                logger.info("\033[0;33;40mHWL按键释放\033[0m")
            else:
                pass
                logger.info("\033[0;33;40mHWL未打开什么都不用做\033[0m")

    def after_each_func(self, ecu):
        self.io.drvr_door_close()
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)
        # global start_get_service_flag
        # start_get_service_flag=0
        """检查双闪如果打开手动关闭"""
        result, realvalue, expectedvalue = self.ipdu.check(getattr(getattr(self.ipdu, 'bodycan'), 'CemBodyFr03'),
                                                        'ActvnOfIndcrIndcrOut_1_CemBodySignalIPdu03', 3,
                                                        do_assert=False)
        if result == True:
            self.io.set_do_level("hazard_switch", True)
            logger.info("\033[0;33;40mHWL开关按下\033[0m")
            sleep(0.1)
            self.io.set_do_level("hazard_switch", False)
            
        super().after_each_func(ecu, start=False)

    def bgm_sleep_and_awake(self):
        pass  # todo

    def get_result(self): #后台启动1s周期，获取刹车灯禁用状态不关心实际返回值
        global start_get_service_flag
        while start_get_service_flag == 1:
            self.partner.send_request_and_ck_resp(
                'LightService_client',
                'GetLightInhibitSts',
                args={"type":[0]},
                ck_info={},
                timeout=0.1,
                )
            sleep(1)
        # start_get_service_flag=0 关 ##需要暂时停止造成通信阻塞，置0
        #start_get_service_flag=1 开  ##恢复通讯继续调用，置1，下两行配套使用
        #receiver_thread = threading.Thread(target=self.get_result,args=())
        #receiver_thread.start()
    
    def Night_mode(self):  # 夜晚模式
        self.ipdu.set(
            self.ipdu.cem_lin1.RlsmCem_Lin1Fr01,
            'TwliBriRawTwliBriRaw_0_RlsmCem_Lin1SignalIPdu01',
            0,
        )  # SUS光感-1000为白天-0-1000为夜晚;
        self.ipdu.set(
            self.ipdu.cem_lin1.RlsmCem_Lin1Fr01,
            'TwliBriRawQf_0_RlsmCem_Lin1SignalIPdu01',
            3,
        )  # SUS光感QF3
        self.ipdu.set(
            self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'OutdBriSts', 1
        )
        logger.info("\033[0;35;40m设置RLSM夜晚模式\033[0m")

    def Day_mode(self):  # 白天模式
        self.ipdu.set(
            self.ipdu.cem_lin1.RlsmCem_Lin1Fr01,
            'TwliBriRawTwliBriRaw_0_RlsmCem_Lin1SignalIPdu01',
            1000,
        )  # SUS光感-1000为白天-0-1000为夜晚;
        self.ipdu.set(
            self.ipdu.cem_lin1.RlsmCem_Lin1Fr01,
            'TwliBriRawQf_0_RlsmCem_Lin1SignalIPdu01',
            3,
        )  # SUS光感QF3
        self.ipdu.set(
            self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'OutdBriSts', 2
        )  # 输入控制灯自动打开关闭-0unknow-1夜晚打开-2白天;
        logger.info("\033[0;35;40m设置RLSM白天模式\033[0m")

    def req_event_get_ExtiLight_mode(self, mode):
        self.mode = mode
        A = self.partner.send_request_and_return_resp(
            LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}
        )["out"]
        if A != mode:
            logger.info("\033[0;35;40m当前外灯模式不等设置值，开始切换模式\033[0m")
            self.partner.send_method_request(
                LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": mode}
            )
            logger.info("\033[0;35;40m外灯模式设置成功等待通知返回\033[0m")
            self.partner.ck_s2s_event(
                LIGHT_SERVICE_CLIENT, "ExteriorLightMode", {"mode": mode}
            )
            logger.info("\033[0;35;40m返回通知和预期一致\033[0m")
            self.partner.send_request_and_ck_resp(
                LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": mode}
            )
            logger.info("\033[0;35;40m主动获取到预期外灯模式\033[0m")
        else:
            logger.info("\033[0;35;40m当前外灯模式等于设置值，重新设置当前模式\033[0m")
            self.partner.send_method_request(
                LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": mode}
            )  # 设置近光mode0-OFF/mode1-AUTO/mode2-POS/mode3-LoBeam
            logger.info("\033[0;35;40m外灯模式设置成功无通知等待300ms获取当前模式\033[0m")
            sleep(0.3)
            self.partner.send_request_and_ck_resp(
                LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": mode}
            )  # 获取外灯模式mode0-OFF/mode1-AUTO/mode2-POS/mode3-LoBeam
            logger.info("\033[0;35;40m主动获取到预期外灯模式\033[0m")

    def req_event_HB_mode(self, cmd_value, hbid_value, hbsts_prty):
        logger.info("远光优先级{0}".format(hbid_value))
        self.partner.send_method_request(
            LIGHT_SERVICE_CLIENT,
            "SetHighBeamControl",
            {"info": {"cmd": cmd_value, "clientId": hbid_value}},
        )
        self.partner.ck_s2s_event(
            LIGHT_SERVICE_CLIENT, "HighBeamStatus", {"sts": {"clientId": hbsts_prty}}
        )

    def chk_event_get_HB_sts(self, cmd_value, hbid_value):
        self.partner.ck_s2s_event(
            LIGHT_SERVICE_CLIENT,
            "HighBeamStatus",
            {"sts": {"sts": cmd_value, "clientId": hbid_value}},
        )
        self.partner.send_request_and_ck_resp(
            LIGHT_SERVICE_CLIENT,
            "GetHighBeamStatus",
            {},
            {"out": {'sts': cmd_value, 'clientId': hbid_value}},
        )

    def Lobeam_off(self):
        self.req_event_get_ExtiLight_mode(mode=0)
        sleep(2)
        self.chk_CanBus_LB_sts(Actn=0, Extr=0)
        logger.info("\033[0;35;40m近光关闭成功\033[0m")

    def Sped_0(self):
        self.ipdu.set(
            self.ipdu.backbonefr.BbmVcuBackBoneFr05,
            'VehSpdLgtForBkpVehSpdLgtA_1_BbmVcuBackBoneSignalIPdu05',
            0,
        )  # 车速0，QF值3;
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06',
            0,
        )  # 车速0，QF值3;
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06',
            3,
        )  # 车速0，QF值3;
        self.ipdu.set(
            self.ipdu.backbonefr.BbmVcuBackBoneFr05,
            'VehSpdLgtForBkpVehSpdLgtQf_1_BbmVcuBackBoneSignalIPdu05',
            3,
        )  # 车速0，QF值3;

    def LoBeamoff_Night_Sped0(self):  # 近光关夜晚车速零
        self.Night_mode()
        self.Sped_0()
        self.Lobeam_off()

    def Hibeam_off(self):  # 远光关
        self.req_event_HB_mode(cmd_value=0, hbid_value=1, hbsts_prty=1)
        logger.info("\033[0;32;40m游戏模式占用优先级关远光\033[0m")
        sleep(0.5)
        self.req_event_HB_mode(cmd_value=255, hbid_value=1, hbsts_prty=255)
        logger.info("\033[0;32;40m游戏模式释放优先级\033[0m")
        self.partner.send_request_and_ck_resp(
            LIGHT_SERVICE_CLIENT,
            "GetHighBeamStatus",
            {},
            {"out": {'sts': 0, 'clientId': 255}},
        )
        logger.info("\033[0;32;40m检测到游戏模式优先级已释放\033[0m")
        self.chk_HB_flash_off()
        logger.info("\033[0;32;40m远光关优先级已释放\033[0m")

    def chk_CanBus_LB_sts(self, Actn, Extr):
        self.ipdu.check(
            self.ipdu.bodyexposedcanfd.CemBodyExpoFr50,
            'ActnOfLedLoBeamActnOfLedLoBeam',
            Actn,
        )
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsLoBeam', Extr)

    def chk_CanBus_HB_sts(self, Actn, ExtrHi, ExtrFl):
        self.ipdu.check(
            self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedHiBeam', Actn
        )
        self.ipdu.check(
            self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', ExtrHi
        )
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFlash', ExtrFl)

    def chk_HB_flash_off(self):
        self.chk_CanBus_HB_sts(Actn=0, ExtrHi=0, ExtrFl=0)
        logger.info("\033[0;32;40m超车灯关远光灯关\033[0m")

    def chk_HB_ON(self):
        self.chk_CanBus_HB_sts(Actn=1, ExtrHi=1, ExtrFl=0)
        logger.info("\033[0;32;40m超车灯关远光灯开\033[0m")

    def chk_HB_flash_on(self):
        self.chk_CanBus_HB_sts(Actn=1, ExtrHi=0, ExtrFl=1)
        logger.info("\033[0;32;40m超车灯开远光灯关\033[0m")

    def chk_HB_err(self):
        self.chk_CanBus_HB_sts(Actn=1, ExtrHi=2, ExtrFl=0)
        logger.info("\033[0;32;40m超车灯关远光灯ERR\033[0m")

    def chk_HB_flash_err(self):
        self.chk_CanBus_HB_sts(Actn=1, ExtrHi=0, ExtrFl=2)
        logger.info("\033[0;32;40m超车灯ERR远光灯关\033[0m")

    def chk_fr_carmod_usgmod(self, carmod, usgmod):
        logger.info("\033[0;32;40m开始检测FR总线数据""\033[0m")
        retry_time = 0
        while True:
            retry_time = retry_time + 1
            if retry_time == 5:
                break
            else:
                sleep(1)
                expectedvalue1 = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr02,
                                                                       'VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02')
                logger.info("检查同芯Fr信号信号值为: carmod = {}".format(expectedvalue1))
                expectedvalue2 = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr02,
                                                                       'VehModMngtGlbSafe1UsgModSts_0_CEMBackBoneSignalIpdu02')
                logger.info("检查同芯Fr信号信号值为: usgmod = {}".format(expectedvalue2))
                if expectedvalue1 == carmod and expectedvalue2 == usgmod:
                    logger.info("\033[0;35;40mFR_carmod_usgmod正常\033[0m")
                    break
                else:
                    logger.info("\033[0;35;40mFR_carmod_usgmod异常尝试重新切换先等待两秒\033[0m")
                    sleep(2)
                    if expectedvalue1 != carmod:
                        logger.info("\033[0;35;40m重新切换CarMod\033[0m")
                        self.sd_tester.change_car_mode(carmod)
                    else:
                        logger.info("\033[0;35;40m重新切换UsgMod\033[0m")
                        self.sd_tester.change_usage_mode(usgmod)

    def ctd_func(self):
        with allure.step("修改防盗需要CCP"):
            self.sd_tester.write_multi_ccp({94: 0x80, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x4, 578: 0x4, 142: 0x83,  # 解闭锁相关
                                            64: 3,  # With Alarm Using Vehicle Horn 即siren，警报器
                                            543: 1,  # Without Battery Backed-Up Sounder 即BBS
                                            66: 1,  # Without inclination sensor 即IS倾斜传感器
                                            65: 1,  # Without Interior Motion Sensor 即内部运动传感器
                                            1: 0xA3,  # 适用配置了舒适泊车模式的车型，对应设防准备时间 30s
                                            69: 1,  # Re-trig次数，一个报警周期30s鸣笛停止10s
                                            70: 1,  # 无被动设防
                                            13: 4,  # 动力类型Battery electric vehicle，上切Active或Driving可解防
                                            })
        with allure.step("五门关闭"):
            self.io.init_bgm_HW()  # 用例开启始前都先恢复5门关门状态，主驾无人，车门按钮未按下
            self.io.hood_door1_close()#37接地
            self.io.hood_door2_open()#36悬空
        with allure.step("设置整车锁解锁"):
            self.dk.set_cenlock_sts(0x1)
            self.partner.empty_all()
        with allure.step("设置整车锁上锁"):
            self.dk.set_cenlock_sts(0x3)
        with allure.step("调用定时器等待30s"):
            sleep(35)
        with allure.step("开主驾门触发防盗"):
            self.io.drvr_door_open()

    def check_multiple_signal_event_thread(self,msg,singal,base_value,targe_value,change_times,duration):
        result = self.ipdu.check_event(msg, singal, base_value, targe_value,timeout = duration)
        logger.info("\033[0;35;40mResult:{}:{} change from {} to {} happened {} times\033[0m".format(msg,singal,base_value,targe_value,result))
        if result >= change_times:
            assert True
            logger.info("\033[0;35;40m{}获取值大于{}\033[0m".format(singal,change_times))
        else:
            assert False
        self.ipdu.reset_check_results()

    def hazard_switch_on_off(self):
        self.io.set_do_level("hazard_switch", True)
        logger.info("\033[0;33;40mHWL开关按下\033[0m")
        sleep(0.1)
        self.io.set_do_level("hazard_switch", False)
        logger.info("\033[0;33;40mHWL开关释放\033[0m")

        #################################################################################################################################################################
    # @allure.title("Normal Driving_手动开启近光")
    # @pytest.mark.smoke
    # @pytest.mark.verify
    # @pytest.mark.full
    # def test_caseid_113270_113289(self):
    #     '''手动开启关闭近光'''
    #     with allure.step("normal Driving 确保近光off档"):
    #         self.sd_tester.change_usage_mode(13)
    #         self.Night_mode()
    #         self.Sped_0()
    #         self.Lobeam_off()
    #     with allure.step("大灯近光档使S2Sservice到MCU信号SwtCDCLi.LoBeamSw==on"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("MPU到MCU信号SwtCDCLi.LoBeamSw == off"):
    #         self.req_event_get_ExtiLight_mode(mode=0)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("normal driving手动开启近光Inactive被关闭")
    # @pytest.mark.smoke
    # def test_caseid_113299(self):
    #     with allure.step("normal Driving 确保近光off档"):
    #         self.sd_tester.change_usage_mode(13)
    #         self.Night_mode()
    #         self.Sped_0()
    #         self.Lobeam_off()
    #     with allure.step("大灯近光档使S2Sservice到MCU信号SwtCDCLi.LoBeamSw==on"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("使用模式切到inactive近光关"):
    #         self.sd_tester.change_usage_mode(1)
    #         sleep(1)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Normal Driving mode_手动切自动夜晚继续被点亮")
    # @pytest.mark.smoke
    # def test_caseid_114773_114791(self):
    #     with allure.step("normal Driving 确保近光off档"):
    #         self.sd_tester.change_usage_mode(13)
    #         self.Night_mode()
    #         self.Sped_0()
    #         self.Lobeam_off()
    #     with allure.step("大灯近光档使S2Sservice到MCU信号SwtCDCLi.LoBeamSw==on"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("近光切auto继续点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("白天模式自动挡近光熄灭"):
    #         self.Day_mode()
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("normal driving自动近光白天切夜晚被点亮")
    # @pytest.mark.smoke
    # def test_caseid_114786(self):
    #     with allure.step("normal driving mode 确保近光off档"):
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("白天模式"):
    #         self.Day_mode()
    #     with allure.step("近光Auto档"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    #     with allure.step("夜晚"):
    #         self.Night_mode()
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @allure.title("Normal Driving手动近光切自动近光白天近光熄灭")
    # @pytest.mark.sanity
    # def test_caseid_114791(self): 
    #     with allure.step("normal Driving 确保近光off档"):
    #         self.sd_tester.change_usage_mode(13)
    #         self.Night_mode()
    #         self.Sped_0()
    #         self.Lobeam_off()
    #     with allure.step("大灯近光档使S2Sservice到MCU信号SwtCDCLi.LoBeamSw==on"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("白天模式"):
    #         self.Day_mode()
    #     with allure.step("近光Auto档"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("normal driving白天自动切手动近光被点亮")
    # @pytest.mark.smoke
    # def test_caseid_114795(self):
    #     with allure.step("normal driving mode 确保近光off档"):
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("白天模式"):
    #         self.Day_mode()
    #     with allure.step("近光Auto档"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    #     with allure.step("大灯近光档使S2Sservice到MCU信号SwtCDCLi.LoBeamSw==on"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #     with allure.step("检查近光激活状态"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @pytest.mark.smoke
    # def test_caseid_114799(self):
    #     '''normal driving夜晚自动近光被关闭近光灭'''
    #     with allure.step("normal driving mode 自动近光夜晚点亮"):
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("近光Auto档"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("近光OFF档"):
    #         self.req_event_get_ExtiLight_mode(mode=0)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)


    # @allure.title("normal driving自动近光夜晚切白天熄灭")
    # @pytest.mark.sanity
    # def test_caseid_114836(self):
    #     with allure.step("normal driving mode 确保近光off档"):
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("近光Auto档"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("近光OFF档"):
    #         self.Day_mode()
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @pytest.mark.smoke
    # def test_caseid_114869_114854(self):
    #     '''
    #     自动近光夜晚被点亮
    #     夜晚自动切手动近光继续被点亮
    #     '''   
    #     with allure.step("normal driving mode 确保近光off档"):
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("近光Auto档"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     #自动切手动
    #     self.req_event_get_ExtiLight_mode(mode=3)
    #     self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @allure.title("normal driving自动近光白天未被点亮")
    # @pytest.mark.smoke
    # def test_caseid_114876(self):
    #     with allure.step("normal driving mode 确保近光off档"):
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("切到白天"):
    #         self.Day_mode()
    #     with allure.step("近光Auto未点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)



    # @allure.title("normal driving远光未激活手动打闪光后失活")
    # @pytest.mark.smoke
    # def test_caseid_113563_113543(self):
    #     '''1.BodyCAN:0x0F0 VehModMngtGlbSafe1CarModSts1 == [0]:normal
    #         2.BodyCAN:0x0F0 VehModMngtGlbSafe1UsgModSts == [13]:driving
    #         3.BodyExposedCANFD:0x20A ActnOfLedHiBeam == disable
    #         4.BodyExposedCANFD:0x251 StsOfLedHiBeamLe == off
    #         5.BodyExposedCANFD:0x252 StsOfLedHiBeamRi == off
    #         6.BackboneFR:36-0-1 ExtrLtgStsHiBeam == off'''
    #     with allure.step("normal driving旧方向盘近光关"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #         self.Hibeam_off()
    #     with allure.step("按键超车闪"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
    #         )
    #         logger.info("\033[0;32;40m方控超车成功\033[0m")
    #         self.chk_HB_flash_on()
    #     with allure.step("释放按键超车关"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 0)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 0}
    #         )
    #         logger.info("\033[0;32;40m方控释放成功\033[0m")
    #         self.chk_HB_flash_off()

    # @allure.title("normal driving近光关手动打远光提示不满足条件")
    # @pytest.mark.smoke
    # def test_caseid_113582(self):
    #     with allure.step("normal driving旧方向盘近光关"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #         self.Hibeam_off()
    #     with allure.step("方控超车闪"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
    #         )
    #         logger.info("\033[0;32;40m方控远光按键置1成功\033[0m")
    #         self.chk_HB_flash_on()
    #     sleep(0.6)
    #     with allure.step("方控超车远光提示不满足条件"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 2)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 2}
    #         )
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr38, 'Flash2HighBeamFailFlag', 1
    #         )  # 无法开启远光提示信息1ON/0OFF
    #         logger.info("\033[0;32;40m方控远光按键置2成功\033[0m")
    #         self.chk_HB_flash_off()
    #         logger.info("\033[0;32;40m提示无法开启远光接下来等待500ms\033[0m")
    #         sleep(0.5)
    #     with allure.step("远光提示信息清零"):
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr38, 'Flash2HighBeamFailFlag', 0
    #         )  # 无法开启远光提示信息1ON/0OFF
    #         logger.info("\033[0;32;40m提示信息清除\033[0m")


    # @pytest.mark.smoke
    # def test_caseid_113631(self):
    #     with allure.step("normal driving旧方向盘近光关"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         self.sd_tester.change_usage_mode(13)
    #         self.Night_mode()
    #         self.Sped_0()
    #         self.Lobeam_off()
    #     with allure.step("设置远光关"):
    #         self.Hibeam_off()
    #     with allure.step("打开近光"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("语音开远光"):
    #         self.req_event_HB_mode(cmd_value=2, hbid_value=3, hbsts_prty=3)
    #         logger.info("\033[0;32;40m语音打开远光调用成功\033[0m")
    #         self.chk_HB_ON()
    #     #手动关远光
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
    #                                      {"info": {"cmd": 2, "clientId": 2}})
    #     self.chk_HB_flash_off()
        
    # @pytest.mark.smoke
    # def test_caseid_113254(self):
    #     with allure.step("Normal Driving mode_闪光未激活自动近光开远光开手动关闭远光"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         self.sd_tester.change_usage_mode(13)
    #         self.sd_tester.change_car_mode(0)
    #         self.Night_mode()
    #         self.Sped_0()
    #         self.Lobeam_off()
    #     with allure.step("设置远光关"):
    #         self.Hibeam_off()
    #     with allure.step("打开近光"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("语音开远光"):
    #        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 2)
    #        self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 2})
    #        self.chk_HB_ON()
    #     #手动关远光
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
    #                                      {"info": {"cmd": 2, "clientId": 2}})
    #     self.chk_HB_flash_off()        

    # @allure.title("normal driving远光激活手动超车灯抑制远光后继续亮远光")
    # @pytest.mark.smoke
    # def test_caseid_113604(self):
    #     with allure.step("normal driving旧方向盘近光关"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         self.sd_tester.change_usage_mode(13)
    #         self.Night_mode()
    #         self.Sped_0()
    #         self.Lobeam_off()
    #     with allure.step("设置远光关"):
    #         self.Hibeam_off()
    #     with allure.step("打开近光"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("语音开远光"):
    #         self.req_event_HB_mode(cmd_value=2, hbid_value=3, hbsts_prty=3)
    #         logger.info("\033[0;32;40m语音打开远光调用成功\033[0m")
    #         self.chk_HB_ON()
    #     with allure.step("方控超车灯"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
    #         )
    #         logger.info("\033[0;32;40m方控远光按键置1成功\033[0m")
    #         self.chk_HB_flash_off()
    #     with allure.step("按键释放远光恢复"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 0)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 0}
    #         )
    #         logger.info("\033[0;32;40m方控远光按键释放成功\033[0m")
    #         self.chk_HB_ON()

    # @allure.title("normal driving手动近光开手动开闪光后开远光")
    # @pytest.mark.smoke
    # def test_caseid_113612(self):
    #     with allure.step("normal driving旧方向盘近光关"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("打开近光"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("确保远光关无占用"):
    #         self.Hibeam_off()
    #     with allure.step("方控超车灯"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
    #         )
    #         logger.info("\033[0;32;40m方控远光按键置1成功\033[0m")
    #         self.chk_HB_flash_on()
    #     with allure.step("方控远光"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 2)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 2}
    #         )
    #         logger.info("\033[0;32;40m方控远光按键置2成功\033[0m")
    #     with allure.step("检测远光开启"):
    #         self.chk_HB_ON()

    # @pytest.mark.smoke
    # def test_caseid_113623(self):
    #     '''自动近光和闪光开启然后请求开远光'''
    #     with allure.step("normal driving旧方向盘近光关"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("打开近光"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("确保远光关无占用"):
    #         self.Hibeam_off()
    #     with allure.step("方控超车灯"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
    #         )
    #         logger.info("\033[0;32;40m方控远光按键置1成功\033[0m")
    #         self.chk_HB_flash_on()
    #     with allure.step("方控远光"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 2)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 2}
    #         )
    #         logger.info("\033[0;32;40m方控远光按键置2成功\033[0m")
    #     with allure.step("检测远光开启"):
    #         self.chk_HB_ON()

    # @allure.title("normal driving手动远光开手动关闭远光")
    # @pytest.mark.smoke
    # def test_caseid_113631(self):
    #     with allure.step("normal driving旧方向盘近光关"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("打开近光"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 2)
    #     self.partner.ck_s2s_event(
    #         LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 2}
    #     )
    #     logger.info("\033[0;32;40m方控远光按键置2成功\033[0m")
    #     with allure.step("方控关闭远光"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
    #         )
    #         logger.info("\033[0;32;40m方控远光按键置1成功\033[0m")
    #         self.chk_HB_flash_off()
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 2)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 2}
    #         )
    #         logger.info("\033[0;32;40m方控远光按键置2成功\033[0m")
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 0)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 0}
    #         )
    #         logger.info("\033[0;32;40m方控远光按键置0成功\033[0m")
    #     with allure.step("检测远光关闭"):
    #         self.chk_HB_flash_off()


    # @allure.title("normal driving语音/ANP/AVP/AHBC打开远光")
    # @pytest.mark.smoke
    # def test_caseid_113638(self):
    #     with allure.step("normal driving确保近光off档"):
    #         self.sd_tester.change_car_mode(0)
    #         self.sd_tester.change_usage_mode(13)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=0, usgmod=13)
    #         self.LoBeamoff_Night_Sped0()
    #         sleep(2)
    #     with allure.step("打开近光"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #         sleep(2)
    #     with allure.step("确保远光关无优先级占用"):
    #         self.Hibeam_off()
    #         sleep(1)
    #     with allure.step("语音/ANP/AVP/AHBC打开远光"):
    #         list1 = [3, 4, 5, 6]
    #         for HBID in list1:
    #             logger.info("远光优先级{0}".format(HBID))
    #             self.partner.send_method_request(
    #                 LIGHT_SERVICE_CLIENT,
    #                 "SetHighBeamControl",
    #                 {"info": {"cmd": 2, "clientId": HBID}},
    #             )
    #             self.partner.ck_s2s_event(
    #                 LIGHT_SERVICE_CLIENT, "HighBeamStatus", {"sts": {"clientId": HBID}}
    #             )
    #             with allure.step("检查远光激活"):
    #                 self.chk_HB_ON()
    #             with allure.step("检查当前优先级状态"):
    #                 if HBID == 3 or HBID == 5:
    #                     self.partner.ck_s2s_event(
    #                         LIGHT_SERVICE_CLIENT,
    #                         "HighBeamStatus",
    #                         {"sts": {"sts": 1, "clientId": 255}},
    #                     )
    #                     self.partner.send_request_and_ck_resp(
    #                         LIGHT_SERVICE_CLIENT,
    #                         "GetHighBeamStatus",
    #                         {},
    #                         {"out": {'sts': 1, 'clientId': 255}},
    #                     )
    #                 else:
    #                     self.partner.send_request_and_ck_resp(
    #                         LIGHT_SERVICE_CLIENT,
    #                         "GetHighBeamStatus",
    #                         {},
    #                         {"out": {'sts': 1, 'clientId': HBID}},
    #                     )
    #         with allure.step("恢复环境"):
    #             self.Hibeam_off()

    # @allure.title("normal driving开关'POS'位开启前位置灯")
    # @pytest.mark.smoke
    # def test_caseid_113666_113693(self):
    #     with allure.step("normal driving 近光关"):
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("外灯POS档近光未开启检测前位置灯开启"):
    #         self.req_event_get_ExtiLight_mode(mode=2)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    #         self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedPosnLamp', 1
    #         )
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt', 1
    #         )

    # @allure.title("normal driving激活'LoBeam'时FPL同步点亮")
    # @pytest.mark.smoke
    # def test_caseid_113677(self):
    #     with allure.step("normal driving 近光关"):
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("打开近光"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #         self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedPosnLamp', 1
    #         )
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt', 1
    #         )



    # @allure.title("normal driving激活'LoBeam'时RPL同步点亮")
    # @pytest.mark.smoke
    # def test_caseid_113705(self):
    #     with allure.step("normal driving 近光关"):
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("外灯近光档后位置灯开启"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #         self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedPosnLamp', 1
    #         )
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiRe', 1
    #         )

    # @allure.title("normal driving开关'POS'位改变使用模式关闭前位置灯")
    # @pytest.mark.smoke
    # def test_caseid_113749(self):
    #     with allure.step("normal driving 近光关"):
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("外灯POS档近光未开启检测后位置灯开启"):
    #         self.req_event_get_ExtiLight_mode(mode=2)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    #         self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedPosnLamp', 1
    #         )
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt', 1
    #         )
    #     with allure.step("使用模式下切Inactive前位置灯关闭"):
    #         self.sd_tester.change_usage_mode(1)
    #         self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedPosnLamp', 0
    #         )
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt', 0
    #         )

    # @allure.title("normal driving关闭“LoBeam”时FPL同步关闭")
    # @pytest.mark.smoke
    # def test_caseid_113759(self):
    #     with allure.step("normal driving 近光关"):
    #         self.sd_tester.change_car_mode(0)
    #         self.sd_tester.change_usage_mode(13)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=0, usgmod=13)
    #         self.LoBeamoff_Night_Sped0()
    #         sleep(2)
    #     with allure.step("打开近光"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("检测前位置灯打开"):
    #         self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedPosnLamp', 1
    #         )
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt', 1
    #         )
    #         logger.info("\033[0;35;40m检测到前位置灯已点亮\033[0m")
    #     with allure.step("近光关检测前位置灯关"):
    #         self.req_event_get_ExtiLight_mode(mode=0)
    #         sleep(1)
    #         self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedPosnLamp', 0
    #         )
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt', 0
    #         )
    #         logger.info("\033[0;35;40m检测到前位置灯已关闭\033[0m")

    # @allure.title("normal driving开关'POS'位改变使用模式关闭后位置灯")
    # @pytest.mark.smoke
    # def test_caseid_113779(self):
    #     with allure.step("normal driving 近光关"):
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("外灯POS档近光未开启检测后位置灯开启"):
    #         self.req_event_get_ExtiLight_mode(mode=2)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    #         self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedPosnLamp', 1
    #         )
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiRe', 1
    #         )
    #     with allure.step("使用模式下切Inactive前位置灯关闭"):
    #         self.sd_tester.change_usage_mode(1)
    #         self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedPosnLamp', 0
    #         )
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiRe', 0
    #         )

    # @allure.title("normal driving关闭“LoBeam”时RPL同步关闭")
    # @pytest.mark.smoke
    # def test_caseid_113789(self):
    #     with allure.step("normal driving 近光关"):
    #         self.sd_tester.change_car_mode(0)
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #         sleep(0.5)
    #     with allure.step("打开近光"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("检测后位置灯打开"):
    #         self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedPosnLamp', 1
    #         )
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiRe', 1
    #         )
    #         logger.info("\033[0;35;40m检测到后位置灯已点亮\033[0m")
    #         sleep(0.5)
    #     with allure.step("近光关检测RPL关"):
    #         self.req_event_get_ExtiLight_mode(mode=0)
    #         self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedPosnLamp', 0
    #         )
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiRe', 0
    #         )
    #         logger.info("\033[0;35;40m检测到后位置灯已关闭\033[0m")

   

    # @allure.title("normal driving开关处于'Auto'位置激活FPL")
    # @pytest.mark.smoke
    # def test_caseid_113809(self):
    #     with allure.step("normal driving 近光关"):
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #         self.Day_mode()
    #     with allure.step("外灯Auto档近光未开启检测前位置灯开启"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    #         self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedPosnLamp', 1
    #         )
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt', 1
    #         )


    # @allure.title("normal driving开关处于'Auto'位置开启后位置灯")
    # @pytest.mark.smoke
    # @pytest.mark.position
    # def test_caseid_113821(self):
    #     with allure.step("normal driving 近光关"):
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #         self.Day_mode()
    #     with allure.step("外灯Auto档近光未开启检测后位置灯开启"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    #         self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedPosnLamp', 1
    #         )
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiRe', 1
    #         )

    # @allure.title("后位置灯激活条件_开关处于Auto位置_Factory Active mode")
    # @pytest.mark.smoke
    # def test_caseid_113824(self):
    #     with allure.step("normal driving 近光关"):
    #         self.sd_tester.change_usage_mode(11)
    #         self.sd_tester.change_car_mode(2)
    #         self.LoBeamoff_Night_Sped0()
    #         self.Day_mode()
    #     with allure.step("外灯Auto档近光未开启检测后位置灯开启"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    #         self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedPosnLamp', 1
    #         )
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiRe', 1
    #         )

    # @allure.title("normal convenience开关'Auto'位置改变使用模式到inactive关闭前位置灯")
    # @pytest.mark.full
    # def test_caseid_113842(self):
    #     with allure.step("normal driving 近光关"):
    #         self.sd_tester.change_car_mode(0)
    #         self.sd_tester.change_usage_mode(2)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=0, usgmod=13)
    #         self.LoBeamoff_Night_Sped0()
    #         self.Day_mode()
    #         sleep(2)
    #     with allure.step("外灯Auto档近光未开启检测前位置灯开启"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    #         self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedPosnLamp', 1
    #         )
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt', 1
    #         )
    #     with allure.step("使用模式下切Inactive"):
    #         self.sd_tester.change_usage_mode(1)
    #         self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedPosnLamp', 0
    #         )
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt', 0
    #         )




    # @allure.title("Normal Driving 自动紧急制动(AEB)请求HWL")
    # @pytest.mark.smoke
    # def test_caseid_113312_115079(self):
    #     with allure.step("Normal driving"):
    #         self.sd_tester.change_car_mode(0)
    #         self.sd_tester.change_usage_mode(13)
    #     with allure.step("自动紧急制动触发AEB"):
    #         self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr13, 'AsySftyHWLReq', 1)
    #         logger.info("\033[0;35;40m自动紧急制动触发\033[0m")
    #         self.ipdu.check(
    #                         self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 3
    #                         )
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 3)
    #         sleep(.4)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #         #按压关闭HWL
    #         self.io.set_do_level("hazard_switch", True)
    #         logger.info("\033[0;33;40mHWL按键按下\033[0m")
    #         sleep(0.1)
    #         self.io.set_do_level("hazard_switch", False)
    #         logger.info("\033[0;33;40mHWL按键释放\033[0m")
    #         self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)



    # @pytest.mark.smoke
    # def test_caseid_114871_114753(self):
    #     with allure.step("CCP#629=4 Normal driving"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         self.sd_tester.change_car_mode(0)
    #         self.sd_tester.change_usage_mode(13)
    #     with allure.step("按压危险报警灯开关激活HWL"):
    #         self.io.set_do_level("hazard_switch", True)
    #         logger.info("\033[0;35;40mHWL开关已按下\033[0m")
    #         sleep(0.1)
    #         self.io.set_do_level("hazard_switch", False)
    #         logger.info("\033[0;35;40mHWL开关已释放\033[0m")
    #         sleep(0.1)
    #         self.ipdu.check(
    #                         self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 3
    #                         )

    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 3)
    #         sleep(.4)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #     with allure.step("按压危险报警灯关闭HWL"):
    #         self.io.set_do_level("hazard_switch", True)
    #         logger.info("\033[0;35;40mHWL开关已按下\033[0m")
    #         sleep(0.1)
    #         self.io.set_do_level("hazard_switch", False)
    #         logger.info("\033[0;35;40mHWL开关已释放\033[0m")
    #         sleep(0.1)
    #         self.ipdu.check(
    #                         self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 0
    #                         )
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)


    #############full##################
    ###################################

    # @allure.title("Normal Active_手动开启近光")
    # @pytest.mark.full
    # def test_caseid_113255(self):
    #     with allure.step("normal Active 确保近光off档"):
    #         self.sd_tester.change_car_mode(0)
    #         self.sd_tester.change_usage_mode(11)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=0, usgmod=11)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("大灯近光档使S2Sservice到MCU信号SwtCDCLi.LoBeamSw==on"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #     with allure.step("检查近光激活状态"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @allure.title("Normal Convenience_手动开启近光")
    # @pytest.mark.full
    # def test_caseid_113263(self):
    #     with allure.step("normal convenience 确保近光off档"):
    #         self.sd_tester.change_car_mode(0)
    #         self.sd_tester.change_usage_mode(2)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=0, usgmod=2)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("大灯近光档使S2Sservice到MCU信号SwtCDCLi.LoBeamSw==on"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #     with allure.step("检查近光激活状态"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @allure.title("Factory Active_手动开启近光")
    # @pytest.mark.full
    # def test_caseid_113313(self):
    #     with allure.step("Factory Active 确保近光off档"):
    #         self.sd_tester.change_car_mode(2)
    #         self.sd_tester.change_usage_mode(11)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=2, usgmod=11)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("大灯近光档使S2Sservice到MCU信号SwtCDCLi.LoBeamSw==on"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #     with allure.step("检查近光激活状态"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @allure.title("Factory Convenience_手动开启近光")
    # @pytest.mark.full
    # def test_caseid_113325(self):
    #     with allure.step("Factory convenience 确保近光off档"):
    #         self.sd_tester.change_car_mode(2)
    #         self.sd_tester.change_usage_mode(2)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=2, usgmod=2)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("大灯近光档使S2Sservice到MCU信号SwtCDCLi.LoBeamSw==on"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #     with allure.step("检查近光激活状态"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @allure.title("Factory Driving_手动开启近光")
    # @pytest.mark.full
    # def test_caseid_113323(self):
    #     with allure.step("Factory Driving 确保近光off档"):
    #         self.sd_tester.change_car_mode(2)
    #         self.sd_tester.change_usage_mode(13)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=2, usgmod=13)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("大灯近光档使S2Sservice到MCU信号SwtCDCLi.LoBeamSw==on"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #     with allure.step("检查近光激活状态"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @allure.title("Transport Active_手动开启近光")
    # @pytest.mark.full
    # def test_caseid_113358(self):
    #     with allure.step("Transport Active 确保近光off档"):
    #         self.sd_tester.change_car_mode(1)
    #         self.sd_tester.change_usage_mode(11)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=1, usgmod=11)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("大灯近光档使S2Sservice到MCU信号SwtCDCLi.LoBeamSw==on"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #     with allure.step("检查近光激活状态"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @allure.title("Transport Convenience_手动开启近光")
    # @pytest.mark.full
    # def test_caseid_113366(self):
    #     with allure.step("Transport convenience 确保近光off档"):
    #         self.sd_tester.change_car_mode(1)
    #         self.sd_tester.change_usage_mode(2)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=1, usgmod=2)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("大灯近光档使S2Sservice到MCU信号SwtCDCLi.LoBeamSw==on"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #     with allure.step("检查近光激活状态"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @allure.title("Transport Driving_手动开启近光")
    # @pytest.mark.full
    # def test_caseid_113362(self):
    #     with allure.step("Transport Driving 确保近光off档"):
    #         self.sd_tester.change_car_mode(1)
    #         self.sd_tester.change_usage_mode(13)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=1, usgmod=13)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("大灯近光档使S2Sservice到MCU信号SwtCDCLi.LoBeamSw==on"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #     with allure.step("检查近光激活状态"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @allure.title("Crash Active_手动开启近光")
    # @pytest.mark.full
    # def test_caseid_113398(self):
    #     with allure.step("Crash Active 确保近光off档"):
    #         self.sd_tester.change_car_mode(3)
    #         self.sd_tester.change_usage_mode(11)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=3, usgmod=11)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("大灯近光档使S2Sservice到MCU信号SwtCDCLi.LoBeamSw==on"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #     with allure.step("检查近光激活状态"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @allure.title("Crash Convenience_手动开启近光")
    # @pytest.mark.full
    # def test_caseid_113409(self):
    #     with allure.step("Crash convenience 确保近光off档"):
    #         self.sd_tester.change_car_mode(3)
    #         self.sd_tester.change_usage_mode(2)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=3, usgmod=2)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("大灯近光档使S2Sservice到MCU信号SwtCDCLi.LoBeamSw==on"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #     with allure.step("检查近光激活状态"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @allure.title("Crash Driving_手动开启近光")
    # @pytest.mark.full
    # def test_caseid_113406(self):
    #     with allure.step("Crash Driving 确保近光off档"):
    #         self.sd_tester.change_car_mode(3)
    #         self.sd_tester.change_usage_mode(13)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=3, usgmod=13)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("大灯近光档使S2Sservice到MCU信号SwtCDCLi.LoBeamSw==on"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #     with allure.step("检查近光激活状态"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @allure.title("Normal Active_手动关闭近光")
    # @pytest.mark.full
    # def test_caseid_113274(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113255()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("MPU到MCU信号SwtCDCLi.LoBeamSw == off"):
    #         self.req_event_get_ExtiLight_mode(mode=0)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Normal Convenience_手动关闭近光")
    # @pytest.mark.full
    # def test_caseid_113287(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113263()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("MPU到MCU信号SwtCDCLi.LoBeamSw == off"):
    #         self.req_event_get_ExtiLight_mode(mode=0)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Factory Active_手动关闭近光")
    # @pytest.mark.full
    # def test_caseid_113329(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113313()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("MPU到MCU信号SwtCDCLi.LoBeamSw == off"):
    #         self.req_event_get_ExtiLight_mode(mode=0)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Factory Convenience_手动关闭近光")
    # @pytest.mark.full
    # def test_caseid_113337(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113325()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("MPU到MCU信号SwtCDCLi.LoBeamSw == off"):
    #         self.req_event_get_ExtiLight_mode(mode=0)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Factory Driving_手动关闭近光")
    # @pytest.mark.full
    # def test_caseid_113343(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113323()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("MPU到MCU信号SwtCDCLi.LoBeamSw == off"):
    #         self.req_event_get_ExtiLight_mode(mode=0)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Transport Active_手动关闭近光")
    # @pytest.mark.full
    # def test_caseid_113374(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113358()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("MPU到MCU信号SwtCDCLi.LoBeamSw == off"):
    #         self.req_event_get_ExtiLight_mode(mode=0)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Transport Convenience_手动关闭近光")
    # @pytest.mark.full
    # def test_caseid_113376(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113366()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("MPU到MCU信号SwtCDCLi.LoBeamSw == off"):
    #         self.req_event_get_ExtiLight_mode(mode=0)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Transport Driving_手动关闭近光")
    # @pytest.mark.full
    # def test_caseid_113380(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113362()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("MPU到MCU信号SwtCDCLi.LoBeamSw == off"):
    #         self.req_event_get_ExtiLight_mode(mode=0)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Crash Active_手动关闭近光")
    # @pytest.mark.full
    # def test_caseid_113412(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113398()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("MPU到MCU信号SwtCDCLi.LoBeamSw == off"):
    #         self.req_event_get_ExtiLight_mode(mode=0)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Crash Convenience_手动关闭近光")
    # @pytest.mark.full
    # def test_caseid_113418(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113409()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("MPU到MCU信号SwtCDCLi.LoBeamSw == off"):
    #         self.req_event_get_ExtiLight_mode(mode=0)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Crash Driving_手动关闭近光")
    # @pytest.mark.full
    # def test_caseid_113421(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113406()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("MPU到MCU信号SwtCDCLi.LoBeamSw == off"):
    #         self.req_event_get_ExtiLight_mode(mode=0)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)


    # @allure.title("Normal Active 手动开启近光Inactive被关闭")
    # @pytest.mark.full
    # def test_caseid_113301(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113255()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("usgmod下切Inactive近光熄灭"):
    #         self.sd_tester.change_usage_mode(1)
    #         sleep(0.5)
    #         self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 3})
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Normal Convenience 手动开启近光Inactive被关闭")
    # @pytest.mark.full
    # def test_caseid_113309(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113263()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("usgmod下切Inactive近光熄灭"):
    #         self.sd_tester.change_usage_mode(1)
    #         sleep(0.5)
    #         self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 3})
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Factory Driving 手动开启近光Inactive被关闭")
    # @pytest.mark.full
    # def test_caseid_113344(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113323()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("usgmod下切Inactive近光熄灭"):
    #         self.sd_tester.change_usage_mode(1)
    #         sleep(0.5)
    #         self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 3})
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Factory Active 手动开启近光Inactive被关闭")
    # @pytest.mark.full
    # def test_caseid_113351(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113313()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("usgmod下切Inactive近光熄灭"):
    #         self.sd_tester.change_usage_mode(1)
    #         sleep(0.5)
    #         self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 3})
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Factory Convenience 手动开启近光Inactive被关闭")
    # @pytest.mark.full
    # def test_caseid_113354(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113325()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("usgmod下切Inactive近光熄灭"):
    #         self.sd_tester.change_usage_mode(1)
    #         sleep(0.5)
    #         self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 3})
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Transport Driving 手动开启近光Inactive被关闭")
    # @pytest.mark.full
    # def test_caseid_113344(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113362()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("usgmod下切Inactive近光熄灭"):
    #         self.sd_tester.change_usage_mode(1)
    #         sleep(0.5)
    #         self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 3})
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Transport Active 手动开启近光Inactive被关闭")
    # @pytest.mark.full
    # def test_caseid_113351(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113358()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("usgmod下切Inactive近光熄灭"):
    #         self.sd_tester.change_usage_mode(1)
    #         sleep(0.5)
    #         self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 3})
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Transport Convenience 手动开启近光Inactive被关闭")
    # @pytest.mark.full
    # def test_caseid_113354(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113366()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("usgmod下切Inactive近光熄灭"):
    #         self.sd_tester.change_usage_mode(1)
    #         sleep(0.5)
    #         self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 3})
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Crash Driving 手动开启近光Inactive被关闭")
    # @pytest.mark.full
    # def test_caseid_113344(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113406()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("usgmod下切Inactive近光熄灭"):
    #         self.sd_tester.change_usage_mode(1)
    #         sleep(0.5)
    #         self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 3})
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Crash Active 手动开启近光Inactive被关闭")
    # @pytest.mark.full
    # def test_caseid_113351(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113398()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("usgmod下切Inactive近光熄灭"):
    #         self.sd_tester.change_usage_mode(1)
    #         sleep(0.5)
    #         self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 3})
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Crash Convenience 手动开启近光Inactive被关闭")
    # @pytest.mark.full
    # def test_caseid_113354(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113409()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("usgmod下切Inactive近光熄灭"):
    #         self.sd_tester.change_usage_mode(1)
    #         sleep(0.5)
    #         self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 3})
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Transport Active mode_手动切自动夜晚继续被点亮")
    # @pytest.mark.full
    # def test_caseid_114749(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113358()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("近光切auto继续点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
            


    # @allure.title("Transport Driving mode_手动切自动夜晚继续被点亮")
    # @pytest.mark.full
    # def test_caseid_114802(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113362()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("近光切auto继续点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @allure.title("Normal Convenience mode_手动切自动夜晚继续被点亮")
    # @pytest.mark.full
    # def test_caseid_114814(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113263()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("近光切auto继续点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @allure.title("Transport Covenience mode_手动切自动夜晚继续被点亮")
    # @pytest.mark.full
    # def test_caseid_114863(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113362()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("近光切auto继续点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @allure.title("Crash Convenience mode_手动切自动夜晚继续被点亮")
    # @pytest.mark.full
    # def test_caseid_114864(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113409()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("近光切auto继续点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @allure.title("Factory active mode_手动切自动夜晚继续被点亮")
    # @pytest.mark.full
    # def test_caseid_114865(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113329()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("近光切auto继续点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @allure.title("Factory Driving  mode_手动切自动夜晚继续被点亮")
    # @pytest.mark.full
    # def test_caseid_114872(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113343()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("近光切auto继续点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @allure.title("Normal Active mode_手动切自动夜晚继续被点亮")
    # @pytest.mark.full
    # def test_caseid_114897(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113274()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("近光切auto继续点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @allure.title("Factory Convenience  mode_手动切自动夜晚继续被点亮")
    # @pytest.mark.full
    # def test_caseid_114908(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113337()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("近光切auto继续点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
            
    # @allure.title("Crash driving mode_手动切自动夜晚继续被点亮")
    # @pytest.mark.full
    # def test_caseid_115018(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113406()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("近光切auto继续点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
            
    # @allure.title("Crash active mode_手动切自动夜晚继续被点亮")
    # @pytest.mark.full
    # def test_caseid_115072(self):
    #     with allure.step("先打开近光"):
    #         self.test_caseid_113398()
    #         logger.info("\033[0;35;40m近光点亮成功\033[0m")
    #     with allure.step("近光切auto继续点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @allure.title("normal Convenience自动近光白天未被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114769(self):
    #     with allure.step("normal convenience mode 确保近光off档"):
    #         self.sd_tester.change_car_mode(0)
    #         self.sd_tester.change_usage_mode(2)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=0, usgmod=2)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("切到白天"):
    #         self.Day_mode()
    #     with allure.step("近光Auto未点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("normal Convenience自动近光白天切夜晚被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114901(self):
    #     with allure.step("normal convenience mode 自动近光白天"):
    #         self.test_caseid_114769()
    #     with allure.step("夜晚"):
    #         self.Night_mode()
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("关闭近光"):
    #         self.Lobeam_off()

    # @allure.title("normal Active自动近光白天未被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_113436(self):
    #     with allure.step("normal active mode 确保近光off档"):
    #         self.sd_tester.change_car_mode(0)
    #         self.sd_tester.change_usage_mode(11)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=0, usgmod=11)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("切到白天"):
    #         self.Day_mode()
    #     with allure.step("近光Auto未点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("normal Active自动近光白天切夜晚被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_113441(self):
    #     with allure.step("normal active mode 自动近光白天"):
    #         self.test_caseid_113436()
    #     with allure.step("夜晚"):
    #         self.Night_mode()
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("关闭近光"):
    #         self.Lobeam_off()

    # @allure.title("Transport Driving自动近光白天未被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114819(self):
    #     with allure.step("Transport driving mode 确保近光off档"):
    #         self.sd_tester.change_car_mode(1)
    #         self.sd_tester.change_usage_mode(13)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=1, usgmod=13)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("切到白天"):
    #         self.Day_mode()
    #     with allure.step("近光Auto未点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Transport Driving自动近光白天切夜晚被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114856(self):
    #     with allure.step("Transport driving mode 自动近光白天"):
    #         self.test_caseid_114819()
    #     with allure.step("夜晚"):
    #         self.Night_mode()
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("关闭近光"):
    #         self.Lobeam_off()

    # @allure.title("Trandport Convenience自动近光白天未被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114870(self):
    #     with allure.step("Transport convenience mode 确保近光off档"):
    #         self.sd_tester.change_car_mode(1)
    #         self.sd_tester.change_usage_mode(2)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=1, usgmod=2)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("切到白天"):
    #         self.Day_mode()
    #     with allure.step("近光Auto未点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Transport Convenience自动近光白天切夜晚被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114895(self):
    #     with allure.step("Transport convenience mode 自动近光白天"):
    #         self.test_caseid_114870()
    #     with allure.step("夜晚"):
    #         self.Night_mode()
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("关闭近光"):
    #         self.Lobeam_off()

    # @allure.title("Transport Active自动近光白天未被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114915(self):
    #     with allure.step("Transport active mode 确保近光off档"):
    #         self.sd_tester.change_car_mode(1)
    #         self.sd_tester.change_usage_mode(11)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=1, usgmod=11)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("切到白天"):
    #         self.Day_mode()
    #     with allure.step("近光Auto未点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Transport Active自动近光白天切夜晚被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114847(self):
    #     with allure.step("Transport active mode 自动近光白天"):
    #         self.test_caseid_114915()
    #     with allure.step("夜晚"):
    #         self.Night_mode()
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("关闭近光"):
    #         self.Lobeam_off()

    # @allure.title("Factory Driving自动近光白天未被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114849(self):
    #     with allure.step("Factory driving mode 确保近光off档"):
    #         self.sd_tester.change_car_mode(2)
    #         self.sd_tester.change_usage_mode(13)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=2, usgmod=13)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("切到白天"):
    #         self.Day_mode()
    #     with allure.step("近光Auto未点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Factory Driving自动近光白天切夜晚被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114839(self):
    #     with allure.step("Factory driving mode 自动近光白天"):
    #         self.test_caseid_114849()
    #     with allure.step("夜晚"):
    #         self.Night_mode()
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("关闭近光"):
    #         self.Lobeam_off()

    # @allure.title("Factory Convenience自动近光白天未被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114792(self):
    #     with allure.step("Factory convenience mode 确保近光off档"):
    #         self.sd_tester.change_car_mode(2)
    #         self.sd_tester.change_usage_mode(2)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=2, usgmod=2)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("切到白天"):
    #         self.Day_mode()
    #     with allure.step("近光Auto未点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Factory Convenience自动近光白天切夜晚被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114914(self):
    #     with allure.step("Factory convenience mode 自动近光白天"):
    #         self.test_caseid_114792()
    #     with allure.step("夜晚"):
    #         self.Night_mode()
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("关闭近光"):
    #         self.Lobeam_off()

    # @allure.title("Factory Active自动近光白天未被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114828(self):
    #     with allure.step("Factory active mode 确保近光off档"):
    #         self.sd_tester.change_car_mode(2)
    #         self.sd_tester.change_usage_mode(11)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=2, usgmod=11)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("切到白天"):
    #         self.Day_mode()
    #     with allure.step("近光Auto未点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Factory Active自动近光白天切夜晚被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114874(self):
    #     with allure.step("Factory active mode 自动近光白天"):
    #         self.test_caseid_114828()
    #     with allure.step("夜晚"):
    #         self.Night_mode()
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("关闭近光"):
    #         self.Lobeam_off()

    # @allure.title("Crash Driving自动近光白天未被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_115022(self):
    #     with allure.step("Crash driving mode 确保近光off档"):
    #         self.sd_tester.change_car_mode(3)
    #         self.sd_tester.change_usage_mode(13)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=3, usgmod=13)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("切到白天"):
    #         self.Day_mode()
    #     with allure.step("近光Auto未点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Crash Driving自动近光白天切夜晚被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_115015(self):
    #     with allure.step("Crash driving mode 自动近光白天"):
    #         self.test_caseid_115022()
    #     with allure.step("夜晚"):
    #         self.Night_mode()
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("关闭近光"):
    #         self.Lobeam_off()

    # @allure.title("Crash Convenience自动近光白天未被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114757(self):
    #     with allure.step("Crash convenience mode 确保近光off档"):
    #         self.sd_tester.change_car_mode(3)
    #         self.sd_tester.change_usage_mode(2)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=3, usgmod=2)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("切到白天"):
    #         self.Day_mode()
    #     with allure.step("近光Auto未点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Crash Convenience自动近光白天切夜晚被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114990(self):
    #     with allure.step("Crash convenience mode 自动近光白天"):
    #         self.test_caseid_114757()
    #     with allure.step("夜晚"):
    #         self.Night_mode()
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("关闭近光"):
    #         self.Lobeam_off()

    # @allure.title("Crash Active自动近光白天未被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114844(self):
    #     with allure.step("Crash active mode 确保近光off档"):
    #         self.sd_tester.change_car_mode(3)
    #         self.sd_tester.change_usage_mode(11)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=3, usgmod=11)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("切到白天"):
    #         self.Day_mode()
    #     with allure.step("近光Auto未点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Crash Active自动近光白天切夜晚被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114986(self):
    #     with allure.step("Crash active mode 自动近光白天"):
    #         self.test_caseid_114844()
    #     with allure.step("夜晚"):
    #         self.Night_mode()
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("关闭近光"):
    #         self.Lobeam_off()

    # @allure.title("Crash Active自动近光白天切手动近光被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114885(self):
    #     with allure.step("Crash Active mode 自动近光白天"):
    #         self.test_caseid_114844()
    #     with allure.step("手动近光开"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("关闭近光"):
    #         self.Lobeam_off()

    # @allure.title("Crash Convenience自动近光白天切手动近光被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_115053(self):
    #     with allure.step("Crash convenience mode 自动近光白天"):
    #         self.test_caseid_114757()
    #     with allure.step("手动近光开"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("关闭近光"):
    #         self.Lobeam_off()

    # @allure.title("Crash Driving自动近光白天切手动近光被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_115030(self):
    #     with allure.step("Crash Driving mode 自动近光白天"):
    #         self.test_caseid_115022()
    #     with allure.step("手动近光开"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("关闭近光"):
    #         self.Lobeam_off()

    # @allure.title("Factory Active自动近光白天切手动近光被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114817(self):
    #     with allure.step("Factory Active mode 自动近光白天"):
    #         self.test_caseid_114828()
    #     with allure.step("手动近光开"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("关闭近光"):
    #         self.Lobeam_off()

    # @allure.title("Factory Convenience自动近光白天切手动近光被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_111351(self):
    #     with allure.step("Factory convenience mode 自动近光白天"):
    #         self.test_caseid_114792()
    #     with allure.step("手动近光开"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("关闭近光"):
    #         self.Lobeam_off()

    # @allure.title("Factory Driving自动近光白天切手动近光被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114804(self):
    #     with allure.step("Factory Driving mode 自动近光白天"):
    #         self.test_caseid_114849()
    #     with allure.step("手动近光开"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("关闭近光"):
    #         self.Lobeam_off()

    # @allure.title("Normal Active自动近光白天切手动近光被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114845(self):
    #     with allure.step("Normal Active mode 自动近光白天"):
    #         self.test_caseid_113436()
    #     with allure.step("手动近光开"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("关闭近光"):
    #         self.Lobeam_off()

    # @allure.title("Normal Convenience自动近光白天切手动近光被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114771(self):
    #     with allure.step("Normal convenience mode 自动近光白天"):
    #         self.test_caseid_114769()
    #     with allure.step("手动近光开"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("关闭近光"):
    #         self.Lobeam_off()

    # @allure.title("Transport Active自动近光白天切手动近光被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114793(self):
    #     with allure.step("Transport Active mode 自动近光白天"):
    #         self.test_caseid_114915()
    #     with allure.step("手动近光开"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("关闭近光"):
    #         self.Lobeam_off()

    # @allure.title("Transport Convenience自动近光白天切手动近光被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114851(self):
    #     with allure.step("Transport convenience mode 自动近光白天"):
    #         self.test_caseid_114870()
    #     with allure.step("手动近光开"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("关闭近光"):
    #         self.Lobeam_off()

    # @allure.title("Transport Driving自动近光白天切手动近光被点亮")
    # @pytest.mark.full
    # @pytest.mark.lobeam
    # def test_caseid_114823(self):
    #     with allure.step("Transport Driving mode 自动近光白天"):
    #         self.test_caseid_114819()
    #     with allure.step("手动近光开"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("关闭近光"):
    #         self.Lobeam_off()
           
#################hibeam#################

    # @allure.title("语音打开左转方控打开右转")
    # @pytest.mark.full
    # def test_caseid_XLIFERIGHT(self):
    #     with allure.step("Normal下usgmod为convenience以上"):
    #         for X in [4, 6]:
    #             self.sd_tester.write_single_ccp(629, X)
    #             self.sd_tester.change_car_mode(0)
    #             for Y in [13,11,2]:
    #                 self.sd_tester.change_usage_mode(Y)
    #                 sleep(1)
    #                 self.chk_fr_carmod_usgmod(carmod=0, usgmod=Y)
    #                 self.LoBeamoff_Night_Sped0()
    #                 sleep(2)
    #                 self.req_event_get_ExtiLight_mode(3)
    #                 self.partner.send_method_request(
    #                     LIGHT_SERVICE_CLIENT,
    #                     "SetTurnLampMode",
    #                     {"lamp": {"mode": 1, "priority": 95}},
    #                 )
    #                 sleep(2)
    #                 with allure.step("检查转向灯状态"):
    #                     self.ipdu.check(
    #                         self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 1
    #                         )
    #                     thread_1 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                                 args=(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
    #                                                 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0, 1, 3, 5))
    #                     thread_2 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                                 args=(self.ipdu.backbonefr.CemBackBoneFr02,
    #                                                     'ExtrLtgStsTurnIndrLe', 0, 1, 3, 5))
    #                     thread_3 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                                 args=(self.ipdu.backbonefr.CemBackBoneFr02,
    #                                                     'ExtrLtgStsTurnIndrRi', 0, 0, 0, 5))
    #                     thread_1.start()
    #                     thread_2.start()
    #                     thread_3.start()

    #                     thread_1.join()
    #                     thread_2.join()
    #                     thread_3.join()
    #                 if X == 4:
    #                     #识别旧方向盘
    #                     self.ipdu.bodycan_swtrbodyfr01_steerwhltouchswtri2steerwhltouchswt2_steerwhltouchswt_shortpress()
    #                     logger.info("\033[0;33;40m老方向盘右转按键轻按\033[0m")
    #                     # self.ipdu.bodycan_swtlbodyfr01_steerwhltouchswtle2steerwhltouchswt2_steerwhltouchswt_notavailble()
    #                     # logger.info("\033[0;33;40m新老方向盘左转按键发0关\033[0m")
    #                     sleep(0.5)
    #                     self.ipdu.bodycan_swtrbodyfr01_steerwhltouchswtri2steerwhltouchswt2_steerwhltouchswt_notavailble()
    #                     logger.info("\033[0;33;40m老方向盘右转按键释放\033[0m")
    #                 else:
    #                     self.ipdu.bodycan_swtlbodyfr02_steerwhltouchswtle1steerwhltouchswt2_steerwhltouchswt_shortpress()
    #                     logger.info("\033[0;33;40m新方向盘右转按键轻按\033[0m")
    #                     sleep(0.5)
    #                     self.ipdu.bodycan_swtlbodyfr02_steerwhltouchswtle1steerwhltouchswt2_steerwhltouchswt_notavailble()
    #                     logger.info("\033[0;33;40m新方向盘右转按键释放\033[0m")
    #                 with allure.step("检查转向灯状态"):
    #                     self.ipdu.check(
    #                         self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 2
    #                         )
    #                     thread_1 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                                 args=(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
    #                                                 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0, 2, 3, 5))
    #                     thread_2 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                                 args=(self.ipdu.backbonefr.CemBackBoneFr02,
    #                                                     'ExtrLtgStsTurnIndrLe', 1, 0, 0, 5))
    #                     thread_3 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                                 args=(self.ipdu.backbonefr.CemBackBoneFr02,
    #                                                     'ExtrLtgStsTurnIndrRi', 0, 1, 3, 5))
    #                     thread_1.start()
    #                     thread_2.start()
    #                     thread_3.start()

    #                     thread_1.join()
    #                     thread_2.join()
    #                     thread_3.join()


    # @allure.title("语音打开左转方控关闭左转")
    # @pytest.mark.full
    # def test_caseid_Y991(self):
    #     with allure.step("Normal下usgmod为convenience以上"):
    #         for X in [4]:
    #             self.sd_tester.write_single_ccp(629, X)
    #             self.sd_tester.change_car_mode(0)
    #             for Y in [2]:
    #                 self.sd_tester.change_usage_mode(Y)
    #                 sleep(1)
    #                 self.chk_fr_carmod_usgmod(carmod=0, usgmod=Y)
    #                 self.LoBeamoff_Night_Sped0()
    #                 sleep(2)
    #                 self.req_event_get_ExtiLight_mode(3)
    #                 self.partner.send_method_request(
    #                     LIGHT_SERVICE_CLIENT,
    #                     "SetTurnLampMode",
    #                     {"lamp": {"mode": 1, "priority": 95}},
    #                 )
    #                 sleep(2)
    #                 with allure.step("检查转向灯状态"):
    #                     self.ipdu.check(
    #                         self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 1
    #                         )
    #                     thread_1 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                                 args=(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
    #                                                 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0, 1, 3, 5))
    #                     thread_2 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                                 args=(self.ipdu.backbonefr.CemBackBoneFr02,
    #                                                     'ExtrLtgStsTurnIndrLe', 0, 1, 3, 5))
    #                     thread_3 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                                 args=(self.ipdu.backbonefr.CemBackBoneFr02,
    #                                                     'ExtrLtgStsTurnIndrRi', 0, 0, 0, 5))
    #                     thread_1.start()
    #                     thread_2.start()
    #                     thread_3.start()

    #                     thread_1.join()
    #                     thread_2.join()
    #                     thread_3.join()
    #                     self.ipdu.bodycan_swtlbodyfr01_steerwhltouchswtle2steerwhltouchswt2_steerwhltouchswt_shortpress()
    #                     logger.info("\033[0;33;40m新老方向盘左转按键发0关\033[0m")
    #                     sleep(0.5)
    #                     self.ipdu.bodycan_swtlbodyfr01_steerwhltouchswtle2steerwhltouchswt2_steerwhltouchswt_notavailble()
    #                 with allure.step("检查转向灯状态"):
    #                     self.ipdu.check(
    #                         self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 0
    #                         )
    #                     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
    #                                                 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
    #                     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
    #                                                     'ExtrLtgStsTurnIndrLe', 0)
    #                     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
    #                                                     'ExtrLtgStsTurnIndrRi', 0)
                        
    # @allure.title("语音打开左转方控关闭左转语音打开右转")
    # @pytest.mark.full
    # def test_caseid_Y992(self):
    #     self.test_caseid_Y991()
    #     sleep(10)
    #     self.partner.send_method_request(
    #                     LIGHT_SERVICE_CLIENT,
    #                     "SetTurnLampMode",
    #                     {"lamp": {"mode": 2, "priority": 95}},
    #                 )
    #     with allure.step("检查转向灯状态"):
    #                     # self.ipdu.check(
    #                     #     self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 2
    #                     #     )
    #                     thread_1 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                                 args=(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
    #                                                 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0, 2, 3, 5))
    #                     thread_2 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                                 args=(self.ipdu.backbonefr.CemBackBoneFr02,
    #                                                     'ExtrLtgStsTurnIndrLe', 1, 0, 0, 5))
    #                     thread_3 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                                 args=(self.ipdu.backbonefr.CemBackBoneFr02,
    #                                                     'ExtrLtgStsTurnIndrRi', 0, 1, 3, 5))
    #                     thread_1.start()
    #                     thread_2.start()
    #                     thread_3.start()    

    #                     thread_1.join()
    #                     thread_2.join()
    #                     thread_3.join()

    
    # @allure.title("语音打开右转方控关闭右转")
    # @pytest.mark.full
    # def test_caseid_Y993(self):
    #     with allure.step("Normal下usgmod为convenience以上"):
    #         for X in [4]:
    #             self.sd_tester.write_single_ccp(629, X)
    #             self.sd_tester.change_car_mode(0)
    #             for Y in [2]:
    #                 self.sd_tester.change_usage_mode(Y)
    #                 sleep(1)
    #                 self.chk_fr_carmod_usgmod(carmod=0, usgmod=Y)
    #                 self.LoBeamoff_Night_Sped0()
    #                 sleep(2)
    #                 self.req_event_get_ExtiLight_mode(3)
    #                 self.partner.send_method_request(
    #                     LIGHT_SERVICE_CLIENT,
    #                     "SetTurnLampMode",
    #                     {"lamp": {"mode": 2, "priority": 95}},
    #                 )
    #                 sleep(2)
    #                 with allure.step("检查转向灯状态"):
    #                     self.ipdu.check(
    #                         self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 2
    #                         )
    #                     thread_1 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                                 args=(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
                                                          
    #                                                 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0, 2, 3, 5))
    #                     thread_2 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                                 args=(self.ipdu.backbonefr.CemBackBoneFr02,
    #                                                     'ExtrLtgStsTurnIndrLe', 0, 0, 0, 5))
    #                     thread_3 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                                 args=(self.ipdu.backbonefr.CemBackBoneFr02,
    #                                                     'ExtrLtgStsTurnIndrRi', 0, 1, 3, 5))
    #                     thread_1.start()
    #                     thread_2.start()
    #                     thread_3.start()

    #                     thread_1.join()
    #                     thread_2.join()
    #                     thread_3.join()
    #                     if X == 4:
    #                         #识别旧方向盘
    #                         self.ipdu.bodycan_swtrbodyfr01_steerwhltouchswtri2steerwhltouchswt2_steerwhltouchswt_shortpress()
    #                         logger.info("\033[0;33;40m老方向盘右转按键轻按\033[0m")
    #                         # self.ipdu.bodycan_swtlbodyfr01_steerwhltouchswtle2steerwhltouchswt2_steerwhltouchswt_notavailble()
    #                         # logger.info("\033[0;33;40m新老方向盘左转按键发0关\033[0m")
    #                         sleep(0.5)
    #                         self.ipdu.bodycan_swtrbodyfr01_steerwhltouchswtri2steerwhltouchswt2_steerwhltouchswt_notavailble()
    #                         logger.info("\033[0;33;40m老方向盘右转按键释放\033[0m")
    #                     else:
    #                         self.ipdu.bodycan_swtlbodyfr02_steerwhltouchswtle1steerwhltouchswt2_steerwhltouchswt_shortpress()
    #                         logger.info("\033[0;33;40m新方向盘右转按键轻按\033[0m")
    #                         sleep(0.5)
    #                         self.ipdu.bodycan_swtlbodyfr02_steerwhltouchswtle1steerwhltouchswt2_steerwhltouchswt_notavailble()
    #                         logger.info("\033[0;33;40m新方向盘右转按键释放\033[0m")
    #                 with allure.step("检查转向灯状态"):
    #                     self.ipdu.check(
    #                         self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 0
    #                         )
    #                     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
    #                                                 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
    #                     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
    #                                                     'ExtrLtgStsTurnIndrLe', 0)
    #                     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
    #                                                     'ExtrLtgStsTurnIndrRi', 0)
                        
    # @allure.title("语音打开右转方控关闭右转语音打开左转")
    # @pytest.mark.full
    # def test_caseid_Y994(self):
    #     self.test_caseid_Y993()
    #     sleep(10)
    #     self.partner.send_method_request(
    #                     LIGHT_SERVICE_CLIENT,
    #                     "SetTurnLampMode",
    #                     {"lamp": {"mode": 1, "priority": 95}},
    #                 )
    #     with allure.step("检查转向灯状态"):
    #                     # self.ipdu.check(
    #                     #     self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 2
    #                     #     )
    #                     thread_1 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                                 args=(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
    #                                                 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0, 1, 3, 5))
    #                     thread_2 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                                 args=(self.ipdu.backbonefr.CemBackBoneFr02,
    #                                                     'ExtrLtgStsTurnIndrLe', 1, 0, 3, 5))
    #                     thread_3 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                                 args=(self.ipdu.backbonefr.CemBackBoneFr02,
    #                                                     'ExtrLtgStsTurnIndrRi', 0, 1, 0, 5))
    #                     thread_1.start()
    #                     thread_2.start()
    #                     thread_3.start()    

    #                     thread_1.join()
    #                     thread_2.join()
    #                     thread_3.join()
                        


    # @allure.title("游戏单次调用左转开5秒后方控左转")
    # @allure.testcase('')
    # @pytest.mark.turnlamp
    # def test_caseid_(self):
    #     for X in [0]:
    #     for X in [0]:
    #         self.sd_tester.change_car_mode(X)
    #         for Y in [2]:
    #             logger.info("carmode为{0}, usgmode为{1}".format(X, Y))  # 打印在哪个mode下失败
    #             logger.info("carmode为{0}, usgmode为{1}".format(X, Y))  # 打印在哪个mode下失败
    #             self.sd_tester.change_usage_mode(Y)
    #             self.ipdu.set(
    #                 self.ipdu.bodycan.SwtlBodyFr01,
    #                 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2',
    #                 0,
    #             )
    #             sleep(1)
    #             self.partner.send_method_request(
    #                 LIGHT_SERVICE_CLIENT,
    #                 "SetTurnLampMode",
    #                 {"lamp": {"mode": 0, "priority": 47}},
    #             )
    #             sleep(1)
    #             self.partner.send_method_request(
    #                 LIGHT_SERVICE_CLIENT,
    #                 "SetTurnLampMode",
    #                 {"lamp": {"mode": 0, "priority": 255}},
    #             )
    #             sleep(1)
    #             self.ipdu.set(
    #                 self.ipdu.bodycan.SwtlBodyFr01,
    #                 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2',
    #                 0,
    #             )
    #             sleep(1)
    #             self.partner.send_method_request(
    #                 LIGHT_SERVICE_CLIENT,
    #                 "SetTurnLampMode",
    #                 {"lamp": {"mode": 0, "priority": 47}},
    #             )
    #             sleep(1)
    #             self.partner.send_method_request(
    #                 LIGHT_SERVICE_CLIENT,
    #                 "SetTurnLampMode",
    #                 {"lamp": {"mode": 0, "priority": 255}},
    #             )
    #             sleep(1)
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'IndcrSts', 0)
    #             self.partner.send_method_request(
    #                 LIGHT_SERVICE_CLIENT,
    #                 "SetTurnLampMode",
    #                 {"lamp": {"mode": 2, "priority": 47}},
    #             )
    #             self.partner.ck_s2s_event(
    #                 LIGHT_SERVICE_CLIENT,
    #                 "NotifyTurnLampStatus",
    #                 {"sts": {"mode": 2, "priority": 47}},
    #             )
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'IndcrSts', 2)
    #             self.partner.send_method_request(
    #                 LIGHT_SERVICE_CLIENT,
    #                 "SetTurnLampMode",
    #                 {"lamp": {"mode": 2, "priority": 47}},
    #             )
    #             self.partner.ck_s2s_event(
    #                 LIGHT_SERVICE_CLIENT,
    #                 "NotifyTurnLampStatus",
    #                 {"sts": {"mode": 2, "priority": 47}},
    #             )
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'IndcrSts', 2)
    #             sleep(5)
    #             # self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
    #             #                           {"sts":{"mode":2,"priority":255}}
    #             #                           )
    #             sleep(15)
    #             self.ipdu.set(
    #                 self.ipdu.bodycan.SwtlBodyFr01,
    #                 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2',
    #                 1,
    #             )
    #             sleep(0.2)
    #             self.ipdu.set(
    #                 self.ipdu.bodycan.SwtlBodyFr01,
    #                 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2',
    #                 0,
    #             )
    #             # self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
    #             #                           {"sts":{"mode":1,"priority":95}}
    #             #                           )
    #             # self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
    #             #                           {"sts":{"mode":2,"priority":255}}
    #             #                           )
    #             sleep(15)
    #             self.ipdu.set(
    #                 self.ipdu.bodycan.SwtlBodyFr01,
    #                 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2',
    #                 1,
    #             )
    #             sleep(0.2)
    #             self.ipdu.set(
    #                 self.ipdu.bodycan.SwtlBodyFr01,
    #                 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2',
    #                 0,
    #             )
    #             # self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
    #             #                           {"sts":{"mode":1,"priority":95}}
    #             #                           )
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'IndcrSts', 1)
    #             sleep(2)
    #             self.ipdu.set(
    #                 self.ipdu.bodycan.SwtlBodyFr01,
    #                 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2',
    #                 1,
    #             )
    #             sleep(0.2)
    #             self.ipdu.set(
    #                 self.ipdu.bodycan.SwtlBodyFr01,
    #                 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2',
    #                 0,
    #             )
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'IndcrSts', 0)
    #             sleep(2)
    #             self.ipdu.set(
    #                 self.ipdu.bodycan.SwtlBodyFr01,
    #                 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2',
    #                 1,
    #             )
    #             sleep(0.2)
    #             self.ipdu.set(
    #                 self.ipdu.bodycan.SwtlBodyFr01,
    #                 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2',
    #                 0,
    #             )
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'IndcrSts', 0)

    # # @allure.title("按键危险报警灯开服务开双闪按键关双闪方控开左")
    # # @allure.testcase('')
    # # @pytest.mark.turnlamp1
    # # def test_caseid_(self):
    # #      for X in [0]:
    # #         self.sd_tester.change_car_mode(X)
    # #         for Y in [2]:
    # #             logger.info("carmode为{0}, usgmode为{1}".format(X, Y)) #打印在哪个mode下失败
    # #             self.sd_tester.change_usage_mode(Y)
    # #             self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
    # #             sleep(20)
    # #             self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
    # #                                              {"lamp":{"mode":3,"priority":0}}
    # #                                              )
    # #             sleep(20)
    # #             # self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
    # #             #                                  {"lamp":{"mode":0,"priority":0}}
    # #             #                                  )
    # #             # self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'IndcrSts', 0)
    # #             # self.io.hazard_light_open()
    # #             # sleep(0.1)
    # #             # self.io.hazard_light_close()
    # #             # sleep(5)
    # #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'IndcrSts', 0)
    # #             sleep(10)
    # #             self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)
    # #             sleep(0.2)
    # #             self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
    # #             sleep(5)
    # #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'IndcrSts', 1)

    # @pytest.mark.smoke333
    # def test_caseid_(self):
    #     with allure.step("normal driving mode 确保近光off档"):
    #         self.sd_tester.change_car_mode(0)
    #         self.sd_tester.change_usage_mode(13)
    #         logger.info("\033[0;32;40m诊断切换carmod和usagmod成功\033[0m")
    #         self.req_event_get_ExtiLight_mode(mode=0)
    #         sleep(5)
    #         self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 3)
    #         logger.info("\033[0;32;40m挡位D档\033[0m")
    #         sleep(5)
    #         #     self.LoBeamoff_Night_Sped0()
    #         # with allure.step("大灯近光档使S2Sservice到MCU信号SwtCDCLi.LoBeamSw==on"):
    #         #     self.req_event_get_ExtiLight_mode(mode=3)
    #         # with allure.step("检查近光激活状态"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("MPU到MCU信号SwtCDCLi.LoBeamSw == off"):
    #         self.req_event_get_ExtiLight_mode(mode=0)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    # # @allure.title("按键危险报警灯开服务开双闪按键关双闪方控开左")
    # # @allure.testcase('')
    # # @pytest.mark.turnlamp1
    # # def test_caseid_(self):
    # #      for X in [0]:
    # #         self.sd_tester.change_car_mode(X)
    # #         for Y in [2]:
    # #             logger.info("carmode为{0}, usgmode为{1}".format(X, Y)) #打印在哪个mode下失败
    # #             self.sd_tester.change_usage_mode(Y)
    # #             self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
    # #             sleep(20)
    # #             self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
    # #                                              {"lamp":{"mode":3,"priority":0}}
    # #                                              )
    # #             sleep(20)
    # #             # self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
    # #             #                                  {"lamp":{"mode":0,"priority":0}}
    # #             #                                  )
    # #             # self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'IndcrSts', 0)
    # #             # self.io.hazard_light_open()
    # #             # sleep(0.1)
    # #             # self.io.hazard_light_close()
    # #             # sleep(5)
    # #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'IndcrSts', 0)
    # #             sleep(10)
    # #             self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)
    # #             sleep(0.2)
    # #             self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
    # #             sleep(5)
    # #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'IndcrSts', 1)

    # @pytest.mark.smoke333
    # def test_caseid_(self):
    #     with allure.step("normal driving mode 确保近光off档"):
    #         self.sd_tester.change_car_mode(0)
    #         self.sd_tester.change_usage_mode(13)
    #         logger.info("\033[0;32;40m诊断切换carmod和usagmod成功\033[0m")
    #         self.req_event_get_ExtiLight_mode(mode=0)
    #         sleep(5)
    #         self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 3)
    #         logger.info("\033[0;32;40m挡位D档\033[0m")
    #         sleep(5)
    #         #     self.LoBeamoff_Night_Sped0()
    #         # with allure.step("大灯近光档使S2Sservice到MCU信号SwtCDCLi.LoBeamSw==on"):
    #         #     self.req_event_get_ExtiLight_mode(mode=3)
    #         # with allure.step("检查近光激活状态"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("MPU到MCU信号SwtCDCLi.LoBeamSw == off"):
    #         self.req_event_get_ExtiLight_mode(mode=0)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)


    # @allure.title("安全要求近光与光传感器(RLSM)通信_夜晚模式自动近光CRC正确LIN信号只有一个")
    # @pytest.mark.full
    # def test_caseid_113518(self):
    #     with allure.step("normal Active"):
    #         self.sd_tester.change_car_mode(0)
    #         self.sd_tester.change_usage_mode(11)
    #         logger.info("\033[0;33;40m诊断切换carmod和usagmod成功\033[0m")
    #         sleep(2)
    #     with allure.step("打开自动近光"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.Night_mode()
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("发一次白天状态然后切到unknow"):
    #         self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'OutdBriSts', 2)
    #         logger.info("\033[0;33;40m雨量光传感器白天下发成功\033[0m")
    #         sleep(0.01)
    #         self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'OutdBriSts', 0)
    #     with allure.step("检测到近光还是开状态"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
        
    @allure.title("Dyno Inactive mode 寻车模式请求HWL根据本地配置闪烁3次HWL失活")
    @pytest.mark.full
    def test_caseid_111371(self):
        with allure.step("dyno InActive"):
            self.sd_tester.change_car_mode(0)
            self.sd_tester.change_usage_mode(1)
            logger.info("\033[0;33;40m诊断切换carmod和usagmod成功\033[0m")
            sleep(2)
            self.partner.send_method_request(KEY_SERVICE_CLIENT, 'SetCarLocalTraceRequest', {"carLoctrReq": 2})
            logger.info("\033[0;33;40m寻车模式下发成功\033[0m")
            result = self.ipdu.check_event(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
                                    'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51',0, 3,timeout=5)
            logger.info("result {}".format(result))
            if result == 3:
                assert True
            else:
                assert False
            self.ipdu.reset_check_results()

    # @allure.title("Crash Driving mode 请求点亮刹车灯时触发紧急制动闪烁所有刹车灯")
    # @pytest.mark.full
    # def test_caseid_115410(self):
    #     with allure.step("CCP修改"):
    #         self.sd_tester.write_single_ccp(114, 2)
    #     with allure.step("Crash Driving"):
    #         self.sd_tester.change_car_mode(3)
    #         self.sd_tester.change_usage_mode(13)
    #         logger.info("\033[0;33;40m诊断切换carmod和usagmod成功\033[0m")
    #         sleep(2)
    #     with allure.step("HWL开关关闭双闪"):
    #         self.io.set_do_level("hazard_switch", True)
    #         logger.info("\033[0;35;40mHWL开关已按下\033[0m")
    #         self.io.set_do_level("hazard_switch", False)
    #         logger.info("\033[0;35;40mHWL开关已释放\033[0m")
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'IndcrSts', 0)
    #     with allure.step("踩刹车"):
    #         self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'BrkLiOnReqSts', 'ReqSts1_Reqd')
    #         logger.info("\033[0;35;40m刹车已踩下\033[0m")
    #         self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp',
    #                         'OnOff1_On')
    #         self.ipdu.check(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr01, 'ActnOfLedStopLampMid', 'OnOff1_On')
    #         # 高位刹车灯硬线暂无法检测默认开
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', 1)
    #     with allure.step("激活EBL"):
    #         self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EmgyBrkLiReqEmgyBrk', 'EblReq_EmgyBrkgInProgs')
    #         logger.info("\033[0;35;40mEBL激活\033[0m")
    #     with allure.step("检测刹车灯闪烁"): 
    #         for _ in range(3):
    #             self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_Off')
    #             logger.info("\033[0;35;40m刹车灯熄灭150ms\033[0m")
    #             sleep(0.15)
    #             self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_On')
    #             logger.info("\033[0;35;40m刹车灯点亮150ms\033[0m")
            
    # @allure.title("Crash Driving mode 请求点亮刹车灯时触发紧急制动后解除紧急自动刹车灯不再闪烁")
    # @pytest.mark.full
    # @pytest.mark.debug   #需要更改
    # def test_caseid_115397(self):
    #     with allure.step("先激活EBL"):
    #         self.test_caseid_115410()
    #     with allure.step("检测刹车灯闪烁"):
    #         for _ in range(3):
    #             self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp',
    #                             'OnOff1_Off')
    #             self.ipdu.check(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr01, 'ActnOfLedStopLampMid', 'OnOff1_Off')
    #             # 高位刹车灯硬线暂无法检测默认开
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', 0)
    #             logger.info("\033[0;35;40m刹车灯熄灭150ms\033[0m")
    #             sleep(0.15)
    #             self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp',
    #                             'OnOff1_On')
    #             self.ipdu.check(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr01, 'ActnOfLedStopLampMid', 'OnOff1_On')
    #             # 高位刹车灯硬线暂无法检测默认开
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', 1)
    #             logger.info("\033[0;35;40m刹车灯点亮150ms\033[0m")
            
    # @allure.title("Crash Driving mode 请求点亮刹车灯时触发紧急制动闪烁所有刹车灯")
    # @pytest.mark.full
    # def test_caseid_115410(self):
    #     with allure.step("CCP修改"):
    #         self.sd_tester.write_single_ccp(114, 2)
    #     with allure.step("Normal Driving"):
    #         self.sd_tester.change_car_mode(3)
    #         self.sd_tester.change_usage_mode(13)
    #         logger.info("\033[0;33;40m诊断切换carmod和usagmod成功\033[0m")
    #         sleep(2)
    #     with allure.step("踩刹车"):
    #         self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'BrkLiOnReqSts', 'ReqSts1_Reqd')
    #         logger.info("\033[0;35;40m刹车已踩下\033[0m")
    #         self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp',
    #                         'OnOff1_On')
    #         self.ipdu.check(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr01, 'ActnOfLedStopLampMid', 'OnOff1_On')
    #         # 高位刹车灯硬线暂无法检测默认开
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', 1)
    #     with allure.step("激活EBL"):
    #         self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EmgyBrkLiReqEmgyBrk', 'EblReq_EmgyBrkgInProgs')
    #         logger.info("\033[0;35;40mEBL激活\033[0m")
    #     with allure.step("检测刹车灯闪烁"):   
    #         for _ in range(3):
    #             self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp',
    #                             'OnOff1_Off')
    #             self.ipdu.check(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr01, 'ActnOfLedStopLampMid', 'OnOff1_Off')
    #             # 高位刹车灯硬线暂无法检测默认开
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', 0)
    #             logger.info("\033[0;35;40m刹车灯熄灭150ms\033[0m")
    #             sleep(0.15)
    #             self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp',
    #                             'OnOff1_On')
    #             self.ipdu.check(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr01, 'ActnOfLedStopLampMid', 'OnOff1_On')
    #             # 高位刹车灯硬线暂无法检测默认开
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', 1)
    #             logger.info("\033[0;35;40m刹车灯点亮150ms\033[0m")
                
    # @allure.title("Normal Driving 方控超车游戏模式占用关")
    # @pytest.mark.debug
    # def test_caseid_15333(self):
    #     with allure.step("normal driving旧方向盘近光关"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         sleep(2)
    #         self.sd_tester.change_car_mode(0)
    #         self.sd_tester.change_usage_mode(13)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=0, usgmod=13)
    #         self.LoBeamoff_Night_Sped0()
    #         self.Hibeam_off()
    #     with allure.step("按键超车闪"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
    #         )
    #         logger.info("\033[0;32;40m方控超车成功\033[0m")
    #         self.chk_HB_flash_on()
    #     with allure.step("游戏模式占用关闭超车灯"):
    #         self.req_event_HB_mode(cmd_value=0, hbid_value=1, hbsts_prty=1)
    #         self.chk_HB_flash_off()
        

    # @allure.title("Driving 下近光关CDC断连BGM主动设置外灯Auto")
    # @pytest.mark.debug
    # def test_caseid_113532(self):
    #     global start_get_service_flag
    #     β = [0,1,2,3]
    #     for zhi in β:
    #         self.sd_tester.change_usage_mode(1)
    #         sleep(0.5)
    #         with allure.step("Driving近光关状态"):
    #             self.sd_tester.change_car_mode(zhi)
    #             self.sd_tester.change_usage_mode(13)
    #             logger.info("\033[0;33;40m诊断切换carmod和usagmod成功\033[0m")
    #             sleep(2)
    #             self.chk_fr_carmod_usgmod(carmod=zhi, usgmod=13)
    #             self.LoBeamoff_Night_Sped0()
    #         with allure.step("停止主动获取接口3以上"):
    #             start_get_service_flag=0
    #             logger.info("\033[0;33;40m停止周期调用成功\033[0m")
    #             sleep(5)
    #         with allure.step("检查近光激活状态"):
    #             self.partner.ck_s2s_event(
    #                 LIGHT_SERVICE_CLIENT, "ExteriorLightMode", {"mode": 1}
    #             )
    #             logger.info("\033[0;35;40m返回通知和预期一致\033[0m")
    #             self.partner.send_request_and_ck_resp(
    #                 LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 1}
    #             )
    #             logger.info("\033[0;35;40m主动获取到预期外灯模式\033[0m")
    #             self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #         with allure.step("外灯设置OFF近光关"):
    #             self.req_event_get_ExtiLight_mode(0)
    #             self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    #         with allure.step("CDC继续周期获取"):
    #             start_get_service_flag=1  ##恢复通讯继续调用，置1，下两行配套使用
    #             receiver_thread = threading.Thread(target=self.get_result,args=())
    #             receiver_thread.start()
    #         with allure.step("检查近光off"):
    #             self.partner.send_request_and_ck_resp(
    #                 LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 0}
    #             )
    #             self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Driving 下近光开CDC断连BGM主动设置外灯Auto")
    # @pytest.mark.debug
    # def test_caseid_113534(self):
    #     global start_get_service_flag
    #     β = [0,1,2,3]
    #     for zhi in β:
    #         self.sd_tester.change_usage_mode(1)
    #         sleep(0.5)
    #         with allure.step("Driving近光关状态"):
    #             self.sd_tester.change_car_mode(zhi)
    #             self.sd_tester.change_usage_mode(13)
    #             logger.info("\033[0;33;40m诊断切换carmod和usagmod成功\033[0m")
    #             sleep(2)
    #             self.chk_fr_carmod_usgmod(carmod=zhi, usgmod=13)
    #             self.LoBeamoff_Night_Sped0()
    #         with allure.step("外灯模式近光开"):
    #             self.req_event_get_ExtiLight_mode(3)
    #             self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #         with allure.step("停止主动获取接口3以上"):
    #             start_get_service_flag=0
    #             logger.info("\033[0;33;40m停止周期调用成功\033[0m")
    #             sleep(5)
    #         with allure.step("检查近光激活状态"):
    #             self.partner.ck_s2s_event(
    #                 LIGHT_SERVICE_CLIENT, "ExteriorLightMode", {"mode": 1}
    #             )
    #             logger.info("\033[0;35;40m返回通知和预期一致\033[0m")
    #             self.partner.send_request_and_ck_resp(
    #                 LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 1}
    #             )
    #             logger.info("\033[0;35;40m主动获取到预期外灯模式\033[0m")
    #             self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #         with allure.step("外灯设置OFF近光关"):
    #             self.req_event_get_ExtiLight_mode(0)
    #             self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    #         with allure.step("CDC继续周期获取"):
    #             start_get_service_flag=1  ##恢复通讯继续调用，置1，下两行配套使用
    #             receiver_thread = threading.Thread(target=self.get_result,args=())
    #             receiver_thread.start()
    #         with allure.step("检查近光off"):
    #             self.partner.send_request_and_ck_resp(
    #                 LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 0}
    #             )
    #             self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Active下近光关CDC断连BGM主动设置外灯Auto")
    # @pytest.mark.debug
    # def test_caseid_113531(self):
    #     global start_get_service_flag
    #     β = [0,1,2,3]
    #     for zhi in β:
    #         self.sd_tester.change_usage_mode(1)
    #         sleep(0.5)
    #         with allure.step("Driving近光关状态"):
    #             self.sd_tester.change_car_mode(zhi)
    #             self.sd_tester.change_usage_mode(11)
    #             logger.info("\033[0;33;40m诊断切换carmod和usagmod成功\033[0m")
    #             sleep(2)
    #             self.chk_fr_carmod_usgmod(carmod=zhi, usgmod=11)
    #             self.LoBeamoff_Night_Sped0()
    #         with allure.step("停止主动获取接口3以上"):
    #             start_get_service_flag=0
    #             logger.info("\033[0;33;40m停止周期调用成功\033[0m")
    #             sleep(5)
    #         with allure.step("检查近光激活状态"):
    #             self.partner.ck_s2s_event(
    #                 LIGHT_SERVICE_CLIENT, "ExteriorLightMode", {"mode": 1}
    #             )
    #             logger.info("\033[0;35;40m返回通知和预期一致\033[0m")
    #             self.partner.send_request_and_ck_resp(
    #                 LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 1}
    #             )
    #             logger.info("\033[0;35;40m主动获取到预期外灯模式\033[0m")
    #             self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #         with allure.step("外灯设置OFF近光关"):
    #             self.req_event_get_ExtiLight_mode(0)
    #             self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    #         with allure.step("CDC继续周期获取"):
    #             start_get_service_flag=1  ##恢复通讯继续调用，置1，下两行配套使用
    #             receiver_thread = threading.Thread(target=self.get_result,args=())
    #             receiver_thread.start()
    #         with allure.step("检查近光off"):
    #             self.partner.send_request_and_ck_resp(
    #                 LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 0}
    #             )
    #             self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("Active下近光开CDC断连BGM主动设置外灯Auto")
    # @pytest.mark.debug
    # def test_caseid_113533(self):
    #     global start_get_service_flag
    #     β = [0,1,2,3]
    #     for zhi in β:
    #         self.sd_tester.change_usage_mode(1)
    #         sleep(0.5)
    #         with allure.step("Driving近光关状态"):
    #             self.sd_tester.change_car_mode(zhi)
    #             self.sd_tester.change_usage_mode(11)
    #             logger.info("\033[0;33;40m诊断切换carmod和usagmod成功\033[0m")
    #             sleep(2)
    #             self.chk_fr_carmod_usgmod(carmod=zhi, usgmod=11)
    #             self.LoBeamoff_Night_Sped0()
    #         with allure.step("外灯模式近光开"):
    #             self.req_event_get_ExtiLight_mode(3)
    #             self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #         with allure.step("停止主动获取接口3以上"):
    #             start_get_service_flag=0
    #             logger.info("\033[0;33;40m停止周期调用成功\033[0m")
    #             sleep(5)
    #         with allure.step("检查近光激活状态"):
    #             self.partner.ck_s2s_event(
    #                 LIGHT_SERVICE_CLIENT, "ExteriorLightMode", {"mode": 1}
    #             )
    #             logger.info("\033[0;35;40m返回通知和预期一致\033[0m")
    #             self.partner.send_request_and_ck_resp(
    #                 LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 1}
    #             )
    #             logger.info("\033[0;35;40m主动获取到预期外灯模式\033[0m")
    #             self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #         with allure.step("外灯设置OFF近光关"):
    #             self.req_event_get_ExtiLight_mode(0)
    #             self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    #         with allure.step("CDC继续周期获取"):
    #             start_get_service_flag=1  ##恢复通讯继续调用，置1，下两行配套使用
    #             receiver_thread = threading.Thread(target=self.get_result,args=())
    #             receiver_thread.start()
    #         with allure.step("检查近光off"):
    #             self.partner.send_request_and_ck_resp(
    #                 LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 0}
    #             )
    #             self.chk_CanBus_LB_sts(Actn=0, Extr=0)     

    # @allure.title("convenience下近光开CDC断连BGM保持近光开")
    # @pytest.mark.debug
    # def test_caseid_119142(self):
    #     logger.info("\033[0;33;40mcase执行开始\033[0m")
    #     global start_get_service_flag
    #     β = [0,1,2,3]
    #     for zhi in β:
    #         logger.info("\033[0;33;40m诊断切换usagmod成功\033[0m")
    #         self.sd_tester.change_usage_mode(1)
    #         sleep(0.5)
    #         with allure.step("Driving近光关状态"):
    #             self.sd_tester.change_car_mode(zhi)
    #             self.sd_tester.change_usage_mode(2)
    #             logger.info("\033[0;33;40m诊断切换carmod和usagmod成功\033[0m")
    #             sleep(2)
    #             self.chk_fr_carmod_usgmod(carmod=zhi, usgmod=2)
    #             self.LoBeamoff_Night_Sped0()
    #         with allure.step("外灯模式近光开"):
    #             self.req_event_get_ExtiLight_mode(3)
    #             self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #         with allure.step("停止主动获取接口3以上"):
    #             start_get_service_flag=0
    #             logger.info("\033[0;33;40m停止周期调用成功\033[0m")
    #             sleep(5)
    #         with allure.step("检查近光激活状态"):
    #             self.partner.send_request_and_ck_resp(
    #                 LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 3}
    #             )
    #             logger.info("\033[0;35;40m主动获取到预期外灯模式\033[0m")
    #             self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #         with allure.step("外灯设置OFF近光关"):
    #             self.req_event_get_ExtiLight_mode(0)
    #             self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    #         with allure.step("CDC继续周期获取"):
    #             start_get_service_flag=1  ##恢复通讯继续调用，置1，下两行配套使用
    #             receiver_thread = threading.Thread(target=self.get_result,args=())
    #             receiver_thread.start()
    #         with allure.step("检查近光off"):
    #             self.partner.send_request_and_ck_resp(
    #                 LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 0}
    #             )
    #             self.chk_CanBus_LB_sts(Actn=0, Extr=0) 

    # @allure.title("BGM上电30s内不检测通道阻塞近光灯可控")
    # @pytest.mark.debug
    # def test_caseid_1900118(self):
    #     global start_get_service_flag
    #     with allure.step("停止主动获取接口3以上"):
    #         start_get_service_flag=0
    #         logger.info("\033[0;33;40m停止周期调用成功\033[0m")
    #         sleep(5)
    #     β = [0,1,2,3]
    #     for zhi in β:
    #         sleep(0.5)
    #         with allure.step("切换Carmode"):
    #             self.sd_tester.change_car_mode(zhi)
    #             sleep(0.2)
    #         with allure.step("切换Usgmode"):
    #             self.sd_tester.change_usage_mode(11)
    #             logger.info("\033[0;33;40m诊断切换carmod和usagmod成功\033[0m")
    #             sleep(1)
    #             self.chk_fr_carmod_usgmod(carmod=zhi, usgmod=11)
    #             self.LoBeamoff_Night_Sped0()
    #         with allure.step("BGM下电重新上电"):
    #             self.nucapp.bgm_power_off()
    #             sleep(1)
    #             self.nucapp.bgm_power_on()
    #             sleep(10)
    #         with allure.step("外灯模式近光开"):
    #             self.req_event_get_ExtiLight_mode(3)
    #             self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #         with allure.step("检查近光激活状态"):
    #             self.partner.send_request_and_ck_resp(
    #                 LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 3}
    #             )
    #             logger.info("\033[0;35;40m主动获取到预期外灯模式\033[0m")
    #             self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #         with allure.step("外灯设置OFF近光关"):
    #             self.req_event_get_ExtiLight_mode(0)
    #             self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    #         with allure.step("等待超过服务连接成功30s后"):
    #             sleep(30)
    #             self.partner.send_request_and_ck_resp(
    #                 LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 1}
    #             )
    #             logger.info("\033[0;35;40m主动获取到预期外灯模式AUTO\033[0m")
    #             self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #         with allure.step("关闭近光"):
    #             self.req_event_get_ExtiLight_mode(0)
    #             self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    #         with allure.step("CDC继续周期获取"):
    #             start_get_service_flag=1  ##恢复通讯继续调用，置1，下两行配套使用
    #             receiver_thread = threading.Thread(target=self.get_result,args=())
    #             receiver_thread.start()
    #         with allure.step("检查近光off"):
    #             self.partner.send_request_and_ck_resp(
    #                 LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 0}
    #             )
    #             self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @allure.title("usgmodeERR时CDC断连导致通道阻塞时灯光功能安全主动置auto")
    # @allure.testcase('')
    # @pytest.mark.debug
    # def test_caseid_1900117(self):
    #     pass #暂时拔同星

    # @allure.title("usgmodeERR近光开时CDC断连导致通道阻塞时灯光功能安全主动置auto")
    # @allure.testcase('')
    # @pytest.mark.debug
    # def test_caseid_1900120(self):
    #     pass #暂时拔同星

    # @allure.title("inactive/abandone下近光关CDC断连BGM保持近光关")
    # @allure.testcase('')
    # @pytest.mark.debug
    # def test_caseid_1900121(self):
    #     pass
    
    # @pytest.mark.sanity
    # def test_caseid_113482(self):
    #     '''后雾灯
    #     1.CC#508=[3] CC#255=[2]
    #     2.切换车辆模式CarMod == [0]:normal
    #     3.切换使用模式UsgMod == [13]:Driving
    #     4.SwtCDCLiLoBeamSw == [1]:OnOff1_On使近光激活BodyExposedCANFD:0x20A ActnOfLedLoBeam ==== [1]:ON'''
    #     self.sd_tester.write_multi_ccp({508: 0x3, 255: 0x2})
    #     self.test_caseid_113270()
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT,"LightControl",{"lights":[{"light":{"type":4,"zoneId":10},"mode":1,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})
    #     self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT,"GetStatus",
    #                                           {"lights":[{"type":4,"zoneId":10}]},
    #                                           {"out":[{"light":{"type":4,"zoneId":10},"sts":1,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})        
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedReFogLamp', 'OnOff1_On')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 'DevSts4_On')

    # @pytest.mark.smoke
    # def test_caseid_113389(self):
    #     '''前雾灯已激活通过大屏开关关闭后雾灯'''
    #     self.sd_tester.write_multi_ccp({508: 0x3, 255: 0x2})
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.req_event_get_ExtiLight_mode(mode=3)#近光激活
    #     self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT,"LightControl",{"lights":[{"light":{"type":4,"zoneId":10},
    #                                                                                      "mode":1,"brightness":0,
    #                                                                                      "color":{"cRed":0,"cGreen":0,"cBlue":0}}]})
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedFrntFogLamp', 'OnOff1_On')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 'DevSts4_On')
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
    #                                      {"lights": [{"light": {"type": 4, "zoneId": 10},
    #                                                   "mode": 0, "brightness": 0,
    #                                                   "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedReFogLamp', 'OnOff1_Off')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 'DevSts4_Off')

    # def test_caseid_113417(self):
    #     '''前雾灯已激活通过大屏开关打开后雾灯'''
    #     self.sd_tester.write_multi_ccp({508: 0x3, 255: 0x2})
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.req_event_get_ExtiLight_mode(mode=3)#近光激活
    #     self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT,"LightControl",{"lights":[{"light":{"type":4,"zoneId":10},
    #                                                                                      "mode":1,"brightness":0,
    #                                                                                      "color":{"cRed":0,"cGreen":0,"cBlue":0}}]})
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedReFogLamp', 'OnOff1_On')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 'DevSts4_On')
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
    #                                      {"lights": [{"light": {"type": 4, "zoneId": 10},
    #                                                   "mode": 0, "brightness": 0,
    #                                                   "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedReFogLamp', 'OnOff1_Off')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 'DevSts4_Off')

    # @pytest.mark.smoke
    # def test_caseid_113298(self):
    #     '''紧急制动EBL请求点亮刹车灯后雾灯同步点亮_请求结束熄灭后雾灯'''
    #     self.sd_tester.write_multi_ccp({508: 0x3, 255: 0x2, 114:0x3})
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     # self.req_event_get_ExtiLight_mode(mode=3)#近光激活
    #     # self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)#刹车
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EmgyBrkLiReqEmgyBrk', 'EblReq_EmgyBrkgInProgs')
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedReFogLamp', 'OnOff1_On')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 'DevSts4_On')
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EmgyBrkLiReqEmgyBrk', 'EblReq_EmgyBrkgNotInProgs')#熄灭后雾灯
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedReFogLamp', 'OnOff1_Off')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 'DevSts4_Off')

    # @pytest.mark.smoke
    # def test_caseid_113469(self):
    #     '''近光已激活通过大屏开关关闭后雾灯'''
    #     self.sd_tester.write_multi_ccp({508: 0x3, 255: 0x2})
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.req_event_get_ExtiLight_mode(mode=3)#近光激活
    #     self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     #服务请求打开后雾灯
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT,"LightControl",{"lights":[{"light":{"type":4,"zoneId":10},
    #                                                                                      "mode":1,"brightness":0,
    #                                                                                      "color":{"cRed":0,"cGreen":0,"cBlue":0}}]})
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedReFogLamp', 'OnOff1_On')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 'DevSts4_On')
    #     #服务请求关闭后雾灯
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
    #                                      {"lights": [{"light": {"type": 4, "zoneId": 10},
    #                                                   "mode": 0, "brightness": 0,
    #                                                   "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedReFogLamp', 'OnOff1_Off')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 'DevSts4_Off')

    # @pytest.mark.sanity
    # def test_caseid_113453(self):  
    #     '''1.CC#508=[3] CC#255=[2]
    #         2.切换车辆模式CarMod == [0]:normal
    #         3.切换使用模式UsgMod == [13]:Driving
    #         4.SwtCDCLiLoBeamSw == [1]:OnOff1_On使近光激活BodyExposedCANFD:0x20A ActnOfLedLoBeam ==== [1]:ON
    #         5.BodyExposedCANFD:0x250 StsOfLedReFogLampLe1 == [2]: Err'''
    #     self.sd_tester.write_multi_ccp({508: 0x3, 255: 0x2})
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReFogLampLe1', 1)
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3})
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
    #                                      {"lights": [{"light": {"type": 4, "zoneId": 10},
    #                                                   "mode": 1, "brightness": 0,
    #                                                   "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})

    #     self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReFogLampLe1', 2)
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedReFogLamp', 'OnOff1_On')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 2)
        #当识别到ExtrLtgStsReFog信号从1跳变为0时，服务代理S2S需要发送一帧FogSetReReq=0 = OnOff1_Off的以太网报文
        
    # @pytest.mark.sanity
    # def test_caseid_113316(self):
    #     '''
    #     踩刹车紧急制动EBL请求点亮后雾灯_请求结束熄灭后雾灯
    #     pc:1.CC#508=[3] CC#255=[2] CC#114=[3]
    #     and Hazard Warning
    #     2.BackboneFR:36-0-1 VehModMngtGlbSafe1CarModSts1 == [0]:normal
    #     3.BackboneFR:36-0-1 VehModMngtGlbSafe1UsgModSts == [13]:driving
    #     4.BackboneFR:55-0-1 BrkPedlPsdBrkPedlPsd == [1]:Yes'''
    #     self.sd_tester.write_multi_ccp({508: 0x3, 255: 0x2, 114: 0x3})
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EmgyBrkLiReqEmgyBrk', 'EblReq_EmgyBrkgInProgs')
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedReFogLamp', 'OnOff1_On')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 'DevSts4_On')
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EmgyBrkLiReqEmgyBrk', 'EblReq_EmgyBrkgNotInProgs')
    #     sleep(.5)
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedReFogLamp', 'OnOff1_Off')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 'DevSts4_Off')


    # @pytest.mark.smoke
    # def test_caseid_113413(self):
    #     '''倒车灯
    #     tc-P0:CC#508=[3]，CC#259=[2] Normal Driving mode 挂倒挡点亮倒车灯
    #     pc:1.BackboneFR:36-0-1 VehModMngtGlbSafe1CarModSts1 == [0]:normal
    #     2.BackboneFR:36-0-1 VehModMngtGlbSafe1UsgModSts == [13]:driving'''
    #     self.sd_tester.write_multi_ccp({508: 0x3, 259: 0x2})
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr10, 'DrvrDesDirDrvrDesDir', 'DrvrDesDir1_Rvs')
    #     sleep(.5)
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedRvsgLamp', 'OnOff1_On')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReverseLi', 'DevSts4_On')

    #需要停发倒车信号目前无法停发flexy   
    # @pytest.mark.smoke
    # def test_caseid_113252(self):
    #     '''
    #     倒挡信号丢失超过5秒倒车灯熄灭
    #     pc:1.BackboneFR:36-0-1 VehModMngtGlbSafe1CarModSts1 == [0]:normal
    #     2.BackboneFR:36-0-1 VehModMngtGlbSafe1UsgModSts == [13]:driving
    #     3.收到倒车信息250ms后BackboneFR:50-1-2 DrvrDesDirDrvrDesDir == [2]:DrvrDesDir1_Rvs for ReverseLampTimeout
    #     4.激活LED倒车灯BodyExposedCANFD:0x20A ActnOfLedRvsgLamp  == [1]: On
    #     5.左侧倒车灯状态BodyExposedCANFD:0x250 StsOfLedRvsgLampLe1   == [1]: On
    #     6.右侧倒车灯状态BodyExposedCANFD:0x260 StsOfLedRvsgLampRi1 == [1]: On
    #     7.倒车灯状态BackboneFR:36-0-1 ExtrLtgStsReverseLi == [1]: On'''
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr10, 'DrvrDesDirDrvrDesDir', 'DrvrDesDir1_Rvs')
    #     sleep(.3)
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_On')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReverseLi', 'DevSts4_On')
    #     self.ipdu.stop_send_pdu("", id)  # 停止数据模拟
    #     sleep(5)
    #     self.ipdu.resume_send_pdu("",id )  # 恢复数据模拟
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_Off')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReverseLi', 'DevSts4_Off')

    # @pytest.mark.smoke
    # def test_caseid_115404(self):
    #     '''
    #     tc-P0:CC#114=[2] Normal Driving mode 踩刹车触发紧急制动闪烁所有刹车灯
    #     pc:1.CC#114: EMERGENCY BRAKE LIGHT == [02]: EBL, Flashing Brake Light
    #     and Hazard Warning
    #     2.BackboneFR:36-0-1 VehModMngtGlbSafe1CarModSts1 == [0]:normal
    #     3.BackboneFR:36-0-1 VehModMngtGlbSafe1UsgModSts == [13]:driving
    #     4.BackboneFR:55-0-1 BrkPedlPsdBrkPedlPsd == [1]:Yes
    #     '''
    #     self.sd_tester.write_single_ccp(114, 2)
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.chk_fr_carmod_usgmod(carmod=0,usgmod=13)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_On')
    #     sleep(0.2)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EmgyBrkLiReqEmgyBrk', 1)
    #     with allure.step("检测刹车灯闪烁"):
    #         for _ in range(3):
    #             self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_Off')
    #             sleep(.15)
    #             self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_On')
    #             sleep(.15)
    #     logger.info("\033[0;35;40m取消紧急制动\033[0m")
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EmgyBrkLiReqEmgyBrk', 0)
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_On')

    # @pytest.mark.smoke
    # def test_caseid_115389(self):
    #     '''
    #     踩刹车触发紧急制动后解除紧急自动刹车灯不再闪烁
    #     pc:1.CC#114: EMERGENCY BRAKE LIGHT == [02]: EBL, Flashing Brake Light
    #     and Hazard Warning
    #     2.BackboneFR:36-0-1 VehModMngtGlbSafe1CarModSts1 == [0]:normal
    #     3.BackboneFR:36-0-1 VehModMngtGlbSafe1UsgModSts == [13]:driving
    #     4.BackboneFR:55-0-1 BrkPedlPsdBrkPedlPsd == [1]:Yes
    #     5.BackboneFR:57-1-8 EmgyBrkLiReqEmgyBrk == [1]: In progress
    #     '''
    #     self.sd_tester.write_multi_ccp({114: 0x2})
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EmgyBrkLiReqEmgyBrk', 'EblReq_EmgyBrkgNotInProgs')
    #     #高位刹车灯dbc中不存在，属于硬线输出，ActnOfCenHiMntdStopLamp
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_On')
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr01, 'ActnOfLedStopLampMid', 'OnOff1_On')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', 'DevSts4_On')

    # @pytest.mark.sanity
    # def test_caseid_111347(self):
    #     '''Normal Driving mode 退出紧急制动(AEB)请求信号丢失通过ReqBkp失活HWL'''
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr04, 'AsySftyHWLReqBkp', 1)
    #     self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 3
    #             )#指示HWL激活状态
    #     for i in range(3):
    #         check_list1 = [
    #             (self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 1),
    #             (self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 1),
    #             (self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 1),
    #             (self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 1),    
    #         ]
    #         self.ipdu.check_multiple_signals(check_list1)
    #         sleep(.4)
    #         check_list2 = [
    #             (self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0),
    #             (self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 0),
    #             (self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 0),
    #             (self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0),    
    #         ]
    #         self.ipdu.check_multiple_signals(check_list2)
    #     self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr04, 'AsySftyHWLReqBkp', 2)
    #     time.sleep(1)
    #     check_list3 = [
    #             (self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0),
    #             (self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 0),
    #             (self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 0),
    #             (self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0),    
    #         ]
    #     self.ipdu.check_multiple_signals(check_list3)

    # @pytest.mark.sanity
    # def test_caseid_115136(self):   
    #     '''自动紧急制动(AEB)请求信号丢失通过ReqBkp请求HWL'''  
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr13, 'AsySftyHWLReq', 'AsySftyHWLReq_TurnOn')
    #     self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr04, 'AsySftyHWLReqBkp', 'AsySftyHWLReq_TurnOn')
    #     self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 3
    #             )
    #     for num in range(3):
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 3)
    #         sleep(.4)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 3)

    # #使用功能安全的三个信号无法进入crash模式，driving下无法诊断切crash
    # @pytest.mark.smoke
    # def test_caseid_114910(self):
    #     '''tc-P0:Normal Driving mode 碰撞事件激活HWL'''
    #     # self.sd_tester.change_car_mode(0)
    #     # self.sd_tester.change_usage_mode(13)
    #     #进入crash
    #     # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
    #     # self.sd_tester.change_car_mode(3)
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr26, 'HvSysCrashFb', 0)
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'SafetyCrashFb', 0)
    #     # sleep(1)
    #     self.ipdu.check(
    #         self.ipdu.backbonefr.CemBackBoneFr02 ,'VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02',3)
    #     self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 3
    #             )
    #     for num in range(3):
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 3)
    #         sleep(.4)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 3)
    #     # 退出crash
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 0)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr26, 'HvSysCrashFb', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'SafetyCrashFb', 3)

    

    # @pytest.mark.sanity
    # def test_caseid_1912472(self):
    #     '''Normal Inactive mode 防盗请求HWL'''
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(1)
    #     #触发防盗
    #     self.ctd_func()
    #     self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 3
    #             )
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 3)
    #     for num in range(3):
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 3)
    #         sleep(.4)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #     self.dk.set_cenlock_sts(0x1)
    
    # def test_caseid_115226(self):
    #     '''踩刹车点亮刹车灯后刹车信号校验和不正确超过200ms'''
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
    #     self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
    #     time.sleep(.3)
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_Off')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', 'DevSts4_Off')

    #114999 HzrdLiIndcnReq 为true时，HWL开始闪烁
    #与115104重复
    # @pytest.mark.smoke
    # def test_caseid_115084(self):
    #     '''CCP#153==[02]or[04] Normal Driving mode 后碰撞预警(RCW)请求HWL发送周期大于4s'''
    #     self.sd_tester.write_single_ccp(153, 4)
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr13, 'RcwmLiReq', 0)
    #     self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 3
    #             )
    #     for i in range(15):
    #         print(f'###############################第{i}次循环###########################################')
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #         sleep(.15)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #     sleep(.5)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    
    # @pytest.mark.sanity
    # def test_caseid_113322(self):
    #     '''解除后碰撞预警(RCW)失活HWL'''
    #     self.sd_tester.write_single_ccp(153, 4)
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr13, 'RcwmLiReq', 0)
    #     self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 3
    #             )
    #     self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr13, 'RcwmLiReq', 1)
    #     sleep(.5)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
        
    #与1912475重复
    # @pytest.mark.sanity
    # def test_caseid_115111(self):
    #     '''防盗关失活HWL'''
    #     self.test_caseid_1912472()
    #     self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 0
    #             )
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)

    # @pytest.mark.smoke
    # def test_caseid_115043_115122(self):
    #     '''碰撞后制动(PIB)激活HWL'''
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr19, 'IndcnToDrvrPostImpctCtrl', 1)
    #     self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 3
    #             )
    #     for num in range(3):
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #         sleep(.4)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #     self.io.set_do_level("hazard_switch", True)
    #     logger.info("\033[0;33;40mHWL按键按下\033[0m")
    #     sleep(0.1)
    #     self.io.set_do_level("hazard_switch", False)
    #     logger.info("\033[0;33;40mHWL按键释放\033[0m")
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
        

    # @pytest.mark.sanity
    # def test_caseid_113978(self):
    #     '''转向灯(DI)激活条件_方向改变时手动右转指示'''
    #     for X in [4,6]:
    #         self.sd_tester.write_single_ccp(629, X)
    #         self.sd_tester.change_car_mode(0)
    #         self.sd_tester.change_usage_mode(13)
    #         if X == 4:
    #             #识别旧方向盘
    #             self.ipdu.bodycan_swtrbodyfr01_steerwhltouchswtri2steerwhltouchswt2_steerwhltouchswt_shortpress()
    #             logger.info("\033[0;33;40m老方向盘右转按键轻按\033[0m")
    #             sleep(0.5)
    #             self.ipdu.bodycan_swtrbodyfr01_steerwhltouchswtri2steerwhltouchswt2_steerwhltouchswt_notavailble()
    #             logger.info("\033[0;33;40m老方向盘右转按键释放\033[0m")
    #         else:
    #             self.ipdu.bodycan_swtlbodyfr02_steerwhltouchswtle1steerwhltouchswt2_steerwhltouchswt_shortpress()
    #             logger.info("\033[0;33;40m新方向盘右转按键轻按\033[0m")
    #             sleep(0.5)
    #             self.ipdu.bodycan_swtlbodyfr02_steerwhltouchswtle1steerwhltouchswt2_steerwhltouchswt_notavailble()
    #             logger.info("\033[0;33;40m新方向盘右转按键释放\033[0m")
    #         self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 2
    #         )
    #         for num in range(3):
    #             self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
    #                             'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 2)
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 2)
    #             sleep(.4)
    #             self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
    #                             'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)

    # @pytest.mark.sanity
    # def test_caseid_113956(self):
    #     '''转向灯(DI)激活条件_自动左转指示要求'''
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     with allure.step("检查转向灯状态"):
    #         self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 1
    #         )
    #         thread_1 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                     args=(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
    #                                           'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0, 1, 3, 5))
    #         thread_2 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                     args=(self.ipdu.backbonefr.CemBackBoneFr02,
    #                                           'ExtrLtgStsTurnIndrLe', 0, 1, 3, 5))
    #         thread_3 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                     args=(self.ipdu.backbonefr.CemBackBoneFr02,
    #                                           'ExtrLtgStsTurnIndrRi', 0, 0, 0, 5))
    #         thread_1.start()
    #         thread_2.start()
    #         thread_3.start()
    #         self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
    #                                          {"lamp": {"mode": 1, "priority": 95}})
    #         thread_1.join()
    #         thread_2.join()
    #         thread_3.join()
    #失败与115361重复
    # @pytest.mark.sanity
    # def test_caseid_115178(self):
    #     '''踩刹车点亮刹车灯后刹车信号Qf !=3 超过200ms'''
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.chk_fr_carmod_usgmod(carmod=0,usgmod=13)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_On')
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 2)#Qf !=3 超过200ms
    #     time.sleep(.3)
    #     # self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoCommonFr08, 'BrkPedlSnsrSt_1_CemBodyExpoCommonSignalIPdu08', 'PsdNotPsd2_Psd')
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_Off')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', 'DevSts4_Off')
        # logger.info("\033[0;35;40m取消紧急制动\033[0m")
        # self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EmgyBrkLiReqEmgyBrk', 0)
        # self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_Off')

    # @pytest.mark.sanity
    # def test_caseid_115139(self):
    #     '''E2E正确检测到刹车动作点亮刹车灯'''
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.chk_fr_carmod_usgmod(carmod=0,usgmod=13)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
    #     #高位刹车灯dbc中不存在，属于硬线输出，ActnOfCenHiMntdStopLamp
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_On')
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr01, 'ActnOfLedStopLampMid', 'OnOff1_On')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', 'DevSts4_On')

    # @pytest.mark.sanity
    # def test_caseid_115052(self):
    #     '''E2E正确未再检测到刹车动作关闭刹车灯'''
    #     self.test_caseid_115139()
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_Off')
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr01, 'ActnOfLedStopLampMid', 'OnOff1_Off')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', 'DevSts4_Off')

    # @pytest.mark.smoke
    # def test_caseid_115385(self):
    #     '''请求点亮刹车灯时触发紧急制动后解除紧急自动刹车灯不再闪烁'''
    #     self.sd_tester.write_single_ccp(114, 2)
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'BrkLiOnReqSts', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_Off')
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr01, 'ActnOfLedStopLampMid', 'OnOff1_Off')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', 'DevSts4_Off')
        
    # @allure.title("Normal Driving 自动刹车灯通过VDDM请求点亮刹车灯")
    # @pytest.mark.sanity
    # def test_caseid_115138(self):
    #     '''自动刹车灯通过VDDM请求点亮刹车灯'''
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'BrkLiOnReqSts', 0)
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     with allure.step("VDDM请求点亮刹车灯"):
    #         self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'BrkLiOnReqSts', 1)
    #         self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_On')
    #         self.ipdu.check(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr01, 'ActnOfLedStopLampMid', 'OnOff1_On')
    #         # 高位刹车灯硬线暂无法检测默认开
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', 1)

    # @pytest.mark.smoke
    # def test_caseid_115040(self):
    #     '''寻车模式下按压HWL开关关闭HWL'''
    #     with allure.step('寻车闪灯指令'):
    #         # self.rc.rvc_panic_vehicle(2) # (-1:空闲，1:鸣笛+闪灯，2:仅闪灯)
    #         # self.rc.sendcmd()
    #         self.partner.send_method_request(KEY_SERVICE_CLIENT, 'SetCarLocalTraceRequest', {"carLoctrReq": 2})
    #         logger.info("已发送寻车请求")
    #         # self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr05, 'CarLoctrActvnSts', 2)
    #         self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 3)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 3)
    #         self.io.set_do_level("hazard_switch", True)
    #         logger.info("\033[0;33;40mHWL按键按下\033[0m")
    #         sleep(0.1)
    #         self.io.set_do_level("hazard_switch", False)
    #         logger.info("\033[0;33;40mHWL按键释放\033[0m")
    #         self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)

    # @pytest.mark.smoke
    # def test_caseid_114985(self):
    #     '''寻车模式激活后取消寻车失活HWL'''
    #     self.partner.send_method_request(KEY_SERVICE_CLIENT, 'SetCarLocalTraceRequest', {"carLoctrReq": 2})
    #     logger.info("已发送寻车闪灯请求")
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #     sleep(.4)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #     self.partner.send_method_request(KEY_SERVICE_CLIENT, 'SetCarLocalTraceRequest', {"carLoctrReq": 0})
    #     time.sleep(.5)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)

    # @pytest.mark.smoke
    # def test_caseid_114989(self):
    #     '''寻车模式请求HWL根据本地配置闪烁3次HWL失活'''
    #     self.partner.send_method_request(KEY_SERVICE_CLIENT, 'SetCarLocalTraceRequest', {"carLoctrReq": 2})
    #     logger.info("已发送寻车闪灯请求")
    #     for i in range(3):
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #         sleep(.4)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #     time.sleep(1)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)


    # @pytest.mark.sanity
    # def test_caseid_113322(self):
    #     '''解除后碰撞预警(RCW)失活HWL'''
    #     self.sd_tester.write_single_ccp(153, 4)
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr13, 'RcwmLiReq', 0)
    #     self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 3
    #             )
    #     for i in range(4):
    #         print(f'###############################第{i}次循环###########################################')
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #         sleep(.15)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #     self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr13, 'RcwmLiReq', 1)
    #     sleep(.5)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #失败
    # @allure.title("Normal Driving mode 请求点亮刹车灯时触发紧急制动闪烁所有刹车灯")
    # @pytest.mark.full
    # @pytest.mark.smoke
    # def test_caseid_115392(self):
    #     with allure.step("CCP修改"):
    #         self.sd_tester.write_single_ccp(114, 2)
    #     with allure.step("Normal Driving"):
    #         self.sd_tester.change_car_mode(0)
    #         self.sd_tester.change_usage_mode(13)
    #         logger.info("\033[0;33;40m诊断切换carmod和usagmod成功\033[0m")
    #         sleep(2)
    #     with allure.step("踩刹车"):
    #         self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'BrkLiOnReqSts', 'ReqSts1_Reqd')
    #         logger.info("\033[0;35;40m刹车已踩下\033[0m")
    #         self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp',
    #                         'OnOff1_On')
    #         self.ipdu.check(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr01, 'ActnOfLedStopLampMid', 'OnOff1_On')
    #         # 高位刹车灯硬线暂无法检测默认开
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', 1)
    #     with allure.step("激活EBL"):
    #         self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EmgyBrkLiReqEmgyBrk', 'EblReq_EmgyBrkgInProgs')
    #         # logger.info("\033[0;35;40mEBL激活\033[0m")
    #     with allure.step("检测刹车灯闪烁"):
    #         for _ in range(3):
    #             self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_Off')
    #             logger.info("\033[0;35;40m刹车灯熄灭150ms\033[0m")
    #             sleep(0.15)
    #             self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_On')
    #             logger.info("\033[0;35;40m刹车灯点亮150ms\033[0m")

    # #失败原因看注释，停掉fr上的AsySftyHWLReq，才能使用AsySftyHWLReqBkp控
    # @allure.title("Normal Driving 退出紧急制动(AEB)失活HWL")
    # @pytest.mark.smoke
    # def test_caseid_115049(self):
    #     '''当AsySftyHWLReq丢失后才能使用AsySftyHWLReqBkp作为备份'''
    #     self.sd_tester.change_usage_mode(13)
    #     # self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr04, 'AsySftyHWLReqBkp', 0)
    #     # self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr13, 'AsySftyHWLReq', 2)
    #     with allure.step("Normal driving触发AEB"):
    #         self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr04, 'AsySftyHWLReqBkp', 1)
    #         # self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr13, 'AsySftyHWLReq', 1)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #         sleep(.4)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #     # with allure.step("退出紧急制动"):
    #     #     self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr13, 'AsySftyHWLReq', 2)
    #     #     logger.info("\033[0;35;40m退出自动紧急制动触发\033[0m")
    #     #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 0)
    #     #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
    #     #                     'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
    #     #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    
    
    # @pytest.mark.full
    # def test_caseid_115095(self):
    #     '''电池热失控下退出热失控失活HWL'''
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'HvBattLimnIndcn_0_VDDMBackBoneSignalIPdu18', 128)
    #     for num in range(3):
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 3)
    #         sleep(.4)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)


    # @pytest.mark.smoke
    # def test_caseid_113397(self):
    #     '''电池热失控激活HWL'''
    #     self.test_caseid_115095()
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'HvBattLimnIndcn_0_VDDMBackBoneSignalIPdu18', 0)
    #     time.sleep(.5)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)

    # @pytest.mark.smoke
    # def test_caseid_115036(self):
    #     '''电池热失控下按压HWL开关关闭HWL'''
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'HvBattLimnIndcn_0_VDDMBackBoneSignalIPdu18', 128)
    #     for num in range(3):
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 3)
    #         sleep(.4)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #     self.io.set_do_level("hazard_switch", True)
    #     logger.info("\033[0;33;40mHWL按键按下\033[0m")
    #     sleep(0.1)
    #     self.io.set_do_level("hazard_switch", False)
    #     logger.info("\033[0;33;40mHWL按键释放\033[0m")
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)

    # @pytest.mark.smoke
    # def test_caseid_114750_114983(self):
    #     '''紧急制动以低速制动时制动灯(EBL)请求点亮HWL'''
    #     self.sd_tester.write_single_ccp(114, 2)
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
    #     sleep(.3)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EmgyBrkLiReqEmgyBrk', 2)
    #     self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 3
    #             )
    #     for num in range(3):
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #         sleep(.4)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #     self.io.set_do_level("hazard_switch", True)
    #     logger.info("\033[0;33;40mHWL按键按下\033[0m")
    #     sleep(0.1)
    #     self.io.set_do_level("hazard_switch", False)
    #     logger.info("\033[0;33;40mHWL按键释放\033[0m")
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
        
    # @pytest.mark.smoke
    # def test_caseid_114983(self):
    #     '''紧急制动以低速制动时制动灯(EBL)请求点亮HWL后按压HWL开关关闭HWL'''
    #     self.test_caseid_114750_114983()
    #     self.io.set_do_level("hazard_switch", True)
    #     logger.info("\033[0;33;40mHWL按键按下\033[0m")
    #     sleep(0.1)
    #     self.io.set_do_level("hazard_switch", False)
    #     logger.info("\033[0;33;40mHWL按键释放\033[0m")
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)




    # def test_caseid_114976(self):
    #         '''自动紧急制动以低速制动时制动灯(EBL)请求点亮HWL刹稳后提速到更高速'''
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'BrkLiOnReqSts', 'ReqSts1_Reqd')



    #与114976 114737重复
    # @pytest.mark.sanity
    # def test_caseid_114958(self):
    #     '''紧急制动以低速制动时制动灯(EBL)请求点亮HWL刹稳后车辆提速到更高速度'''
    #     self.test_caseid_114750_114983()
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EmgyBrkLiReqEmgyBrk', 0)
    #     time.sleep(.5)
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    

    # @pytest.mark.smoke
    # def test_caseid_114934(self):
    #     '''tc-P0:Normal Driving mode 退出碰撞后制动(PIB)使HWL失活'''
    #     with allure.step("Normal driving"):
    #         self.sd_tester.change_car_mode(0)
    #         self.sd_tester.change_usage_mode(13)
    #     with allure.step("PIB"):
    #         self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr19, 'IndcnToDrvrPostImpctCtrl', 1)
    #         logger.info("\033[0;35;40m自动紧急制动触发\033[0m")
    #         self.ipdu.check(
    #                         self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 3
    #                         )
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 3)
    #         sleep(.4)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #     #退出碰撞
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr19, 'IndcnToDrvrPostImpctCtrl', 0)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)


    #停发AEB请求信号暂时只能拔flexy
    # def test_caseid_115087(self):
    #     '''自动紧急制动(AEB)请求信号丢失通过ReqBkp请求HWL按压HWL开关关闭HWL'''
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr04, 'AsySftyHWLReqBkp', 1)
    #     self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 3
    #             )#指示HWL激活状态
    #     for i in range(3):
    #         check_list1 = [
    #             (self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 1),
    #             (self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 1),
    #             (self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 1),
    #             (self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 1),    
    #         ]
    #         self.ipdu.check_multiple_signals(check_list1)
    #         sleep(.4)
    #         check_list2 = [
    #             (self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0),
    #             (self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 0),
    #             (self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 0),
    #             (self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0),    
    #         ]
    #         self.ipdu.check_multiple_signals(check_list2)
    #     self.io.set_do_level("hazard_switch", True)
    #     logger.info("\033[0;33;40mHWL按键按下\033[0m")
    #     sleep(0.1)
    #     self.io.set_do_level("hazard_switch", False)
    #     logger.info("\033[0;33;40mHWL按键释放\033[0m")
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)

    # #停发counter暂时只能拔flexy
    # def test_caseid_115217(self): 
    #     '''踩刹车点亮刹车灯后刹车信号计数器停发超过200ms'''
    #     pass
    
    # @pytest.mark.sanity
    # def test_caseid_113750(self):
    #     '''
    #     自动刹车灯通过BBM用作备份请求点亮刹车灯
    #     pc:1.BackboneFR:36-0-1 VehModMngtGlbSafe1CarModSts1 == [0]:normal
    #     2.BackboneFR:36-0-1 VehModMngtGlbSafe1UsgModSts == [13]:driving
    #     '''
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.BbmVcuBackBoneFr05, 'BrkLiOnReqForBkpBrkLiOnReqSts', 'ReqSts1_Reqd')
    #     #高位刹车灯dbc中不存在，属于硬线输出，ActnOfCenHiMntdStopLamp
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_On')
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr01, 'ActnOfLedStopLampMid', 'OnOff1_On')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', 'DevSts4_On')

    # @pytest.mark.sanity
    # def test_caseid_115132(self):
    #     '''退出自动刹车灯通过BBM备份和VDDM请求关闭刹车灯'''
    #     self.test_caseid_115138()
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'BrkLiOnReqSts', 0)
    #     self.ipdu.set(self.ipdu.backbonefr.BbmVcuBackBoneFr05, 'BrkLiOnReqForBkpBrkLiOnReqSts', 'ReqSts1_NotReqd')
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_Off')
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr01, 'ActnOfLedStopLampMid', 'OnOff1_Off')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', 'DevSts4_Off')

    # @pytest.mark.smoke
    # def test_caseid_113331_113413_113346(self):
    #     '''倒挡切前进档倒车灯熄灭'''
    #     self.sd_tester.write_multi_ccp({508: 0x3, 259: 0x2})
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr10, 'DrvrDesDirDrvrDesDir', 'DrvrDesDir1_Rvs')#挂倒挡
    #     sleep(.3)
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedRvsgLamp', 'OnOff1_On')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReverseLi', 'DevSts4_On')
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr10, 'DrvrDesDirDrvrDesDir', 'DrvrDesDir1_Fwd')#前进挡
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedRvsgLamp', 'OnOff1_Off')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReverseLi', 'DevSts4_Off')
    
    # @pytest.mark.smoke
    # def test_caseid_113296_113314(self):
    #     '''倒挡切空档倒车灯熄灭'''
    #     self.sd_tester.write_multi_ccp({508: 0x3, 259: 0x2})
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr10, 'DrvrDesDirDrvrDesDir', 'DrvrDesDir1_Rvs')#挂倒挡
    #     sleep(.3)
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedRvsgLamp', 'OnOff1_On')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReverseLi', 'DevSts4_On')
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr10, 'DrvrDesDirDrvrDesDir', 'DrvrDesDir1_Neut')#空挡
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedRvsgLamp', 'OnOff1_Off')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReverseLi', 'DevSts4_Off')
    
    # @pytest.mark.smoke
    # def test_caseid_113346_113370(self):
    #     '''倒挡切前进档倒车灯熄灭'''
    #     self.sd_tester.write_multi_ccp({508: 0x3, 259: 0x4})
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr10, 'DrvrDesDirDrvrDesDir', 'DrvrDesDir1_Rvs')#挂倒挡
    #     sleep(.3)
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedRvsgLamp', 'OnOff1_On')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReverseLi', 'DevSts4_On')
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr10, 'DrvrDesDirDrvrDesDir', 'DrvrDesDir1_Fwd')#前进挡
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedRvsgLamp', 'OnOff1_Off')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReverseLi', 'DevSts4_Off')
    
    # @pytest.mark.smoke
    # def test_caseid_113314(self):
    #     '''倒挡切空档倒车灯熄灭'''
    #     self.sd_tester.write_multi_ccp({508: 0x3, 259: 0x4})
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr10, 'DrvrDesDirDrvrDesDir', 'DrvrDesDir1_Rvs')#挂倒挡
    #     sleep(.3)
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedRvsgLamp', 'OnOff1_On')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReverseLi', 'DevSts4_On')
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr10, 'DrvrDesDirDrvrDesDir', 'DrvrDesDir1_Neut')#空挡
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedRvsgLamp', 'OnOff1_Off')
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReverseLi', 'DevSts4_Off')

    
    # @allure.title("convenience下近光开CDC断连BGM保持近光开")
    # @pytest.mark.debug
    # def test_caseid_1900119(self):
    #     logger.info("\033[0;33;40mcase执行开始\033[0m")
    #     global start_get_service_flag
    #     β = [0,1,2,3]
    #     for zhi in β:
    #         logger.info("\033[0;33;40m诊断切换usagmod成功\033[0m")
    #         self.sd_tester.change_usage_mode(1)
    #         sleep(0.5)
    #         with allure.step("Driving近光关状态"):
    #             self.sd_tester.change_car_mode(zhi)
    #             self.sd_tester.change_usage_mode(2)
    #             logger.info("\033[0;33;40m诊断切换carmod和usagmod成功\033[0m")
    #             sleep(2)
    #             self.chk_fr_carmod_usgmod(carmod=zhi, usgmod=2)
    #             self.LoBeamoff_Night_Sped0()
    #         with allure.step("外灯模式近光关"):
    #             self.req_event_get_ExtiLight_mode(0)
    #             self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    #         with allure.step("停止主动获取接口3以上"):
    #             start_get_service_flag=0
    #             logger.info("\033[0;33;40m停止周期调用成功\033[0m")
    #             sleep(5)
    #         with allure.step("检查近光激活状态"):
    #             self.partner.send_request_and_ck_resp(
    #                 LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 0}
    #             )
    #             logger.info("\033[0;35;40m主动获取到预期外灯模式\033[0m")
    #             self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    #         with allure.step("外灯设置OFF近光关"):
    #             self.req_event_get_ExtiLight_mode(3)
    #             self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #         with allure.step("CDC继续周期获取"):
    #             start_get_service_flag=1  ##恢复通讯继续调用，置1，下两行配套使用
    #             receiver_thread = threading.Thread(target=self.get_result,args=())
    #             receiver_thread.start()
    #         with allure.step("检查近光off"):
    #             self.partner.send_request_and_ck_resp(
    #                 LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 3}
    #             )
    #             self.chk_CanBus_LB_sts(Actn=1, Extr=1)


    # @pytest.mark.smoke
    # def test_caseid_115104(self):
    #     '''CCP#153==[02]or[04] Normal Driving mode 后碰撞预警(RCW)请求HWL发送周期大于4s'''
    #     self.sd_tester.write_single_ccp(153, 4)
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr13, 'RcwmLiReq', 0)
    #     self.ipdu.check(
    #         self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 3
    #     )
    #     for i in range(15):
    #         print(f'###############################第{i}次循环###########################################')
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #         sleep(.15)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #     sleep(.5)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)


    # @pytest.mark.smoke
    # def test_caseid_113397(self):
    #     '''电池热失控激活HWL'''
    #     self.test_caseid_115095()
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'HvBattLimnIndcn_0_VDDMBackBoneSignalIPdu18', 0)
    #     time.sleep(.5)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)


    # @pytest.mark.smoke
    # def test_caseid_115036(self):
    #     '''电池热失控下按压HWL开关关闭HWL'''
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'HvBattLimnIndcn_0_VDDMBackBoneSignalIPdu18', 128)
    #     for num in range(3):
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 3)
    #         sleep(.4)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #     self.io.set_do_level("hazard_switch", True)
    #     logger.info("\033[0;33;40mHWL按键按下\033[0m")
    #     sleep(0.1)
    #     self.io.set_do_level("hazard_switch", False)
    #     logger.info("\033[0;33;40mHWL按键释放\033[0m")
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)


    # @pytest.mark.smoke
    # def test_caseid_114962(self):
    #     '''紧急制动以低速制动时制动灯(EBL)请求点亮HWL后按压HWL开关关闭HWL'''
    #     self.sd_tester.write_single_ccp(114, 2)
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     # 踩刹车
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'BrkLiOnReqSts', 'ReqSts1_Reqd')
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EmgyBrkLiReqEmgyBrk', 'EblReq_EmgyBrkgInProgsAtSpdLo')
    #     # 危险报警灯闪烁
    #     for num in range(3):
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 3)
    #         sleep(.4)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
        # 按压HWL开关关闭HWL
        # self.io.set_do_level("hazard_switch", True)
        # logger.info("\033[0;35;40mHWL开关已释放\033[0m")
        # sleep(0.2)
        # # self.io.set_do_level("hazard_switch", False)
        # # logger.info("\033[0;33;40mHWL已关闭\033[0m")
        # self.ipdu.check(
        #     self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 3
        # )
        # self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
        # self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
        # self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)


    # @allure.title("normal driving自动近光夜晚切白天熄灭")
    # @pytest.mark.smoke
    # def test_caseid_114836(self):
    #     with allure.step("normal driving mode 确保近光off档"):
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("近光Auto档"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("近光OFF档"):
    #         self.Day_mode()
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)


    # @pytest.mark.smoke
    # def test_caseid_114737(self):
    #     '''紧急制动以低速制动时制动灯(EBL)请求点亮HWL刹稳后车辆提速到更高速度'''
    #     self.sd_tester.write_single_ccp(114, 2)
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'BrkLiOnReqSts', 'ReqSts1_Reqd')
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EmgyBrkLiReqEmgyBrk', 'EblReq_EmgyBrkgInProgsAtSpdLo')
    #     for num in range(3):
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 3)
    #         sleep(.4)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)


    # @pytest.mark.smoke
    # def test_caseid_113978(self):
    #     '''转向灯(DI)激活条件_方向改变时手动右转指示'''
    #     for X in [4, 6]:
    #         self.sd_tester.write_single_ccp(629, X)
    #         self.sd_tester.change_car_mode(0)
    #         self.sd_tester.change_usage_mode(13)
    #         if X == 4:
    #             # 识别旧方向盘
    #             self.ipdu.bodycan_swtrbodyfr01_steerwhltouchswtri2steerwhltouchswt2_steerwhltouchswt_shortpress()
    #             logger.info("\033[0;33;40m老方向盘右转按键轻按\033[0m")
    #             sleep(0.5)
    #             self.ipdu.bodycan_swtrbodyfr01_steerwhltouchswtri2steerwhltouchswt2_steerwhltouchswt_notavailble()
    #             logger.info("\033[0;33;40m老方向盘右转按键释放\033[0m")
    #         else:
    #             self.ipdu.bodycan_swtlbodyfr02_steerwhltouchswtle1steerwhltouchswt2_steerwhltouchswt_shortpress()
    #             logger.info("\033[0;33;40m新方向盘右转按键轻按\033[0m")
    #             sleep(0.5)
    #             self.ipdu.bodycan_swtlbodyfr02_steerwhltouchswtle1steerwhltouchswt2_steerwhltouchswt_notavailble()
    #             logger.info("\033[0;33;40m新方向盘右转按键释放\033[0m")
    #         self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 2
    #         )
    #         for num in range(3):
    #             self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
    #                             'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 2)
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 2)
    #             sleep(.4)
    #             self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
    #                             'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)


    # @pytest.mark.smoke
    # def test_caseid_113956(self):
    #     '''转向灯(DI)激活条件_自动左转指示要求'''
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     with allure.step("检查转向灯状态"):
    #         self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 1
    #         )
    #         thread_1 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                     args=(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
    #                                           'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0, 1, 3, 5))
    #         thread_2 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                     args=(self.ipdu.backbonefr.CemBackBoneFr02,
    #                                           'ExtrLtgStsTurnIndrLe', 0, 1, 3, 5))
    #         thread_3 = threading.Thread(target=self.check_multiple_signal_event_thread,
    #                                     args=(self.ipdu.backbonefr.CemBackBoneFr02,
    #                                           'ExtrLtgStsTurnIndrRi', 0, 0, 0, 5))
    #         thread_1.start()
    #         thread_2.start()
    #         thread_3.start()
    #         self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
    #                                          {"lamp": {"mode": 1, "priority": 95}})
    #         thread_1.join()
    #         thread_2.join()
    #         thread_3.join()


    # @pytest.mark.smoke
    # def test_caseid_113322(self):
    #     '''解除后碰撞预警(RCW)失活HWL'''
    #     self.sd_tester.write_single_ccp(153, 4)
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr13, 'RcwmLiReq', 0)
    #     self.ipdu.check(
    #         self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 3
    #     )
    #     self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr13, 'RcwmLiReq', 1)
    #     sleep(.5)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)


    # @allure.title("normal convenience远光未激活手动打开闪光")
    # @pytest.mark.full
    # @pytest.mark.full
    # def test_caseid_113542(self):
    #     '''1.BodyCAN:0x0F0 VehModMngtGlbSafe1CarModSts1 == [0]:normal
    #         2.BodyCAN:0x0F0 VehModMngtGlbSafe1UsgModSts == [2]:convenience
    #         3.BodyExposedCANFD:0x20A ActnOfLedHiBeam == disable
    #         4.BodyExposedCANFD:0x251 StsOfLedHiBeamLe == off
    #         5.BodyExposedCANFD:0x252 StsOfLedHiBeamRi == off
    #         6.BackboneFR:36-0-1 ExtrLtgStsHiBeam == off'''
    #     with allure.step("normal driving旧方向盘近光关"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         self.sd_tester.change_usage_mode(2)
    #         self.LoBeamoff_Night_Sped0()
    #         self.Hibeam_off()
    #     with allure.step("按键超车闪"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
    #         )
    #         logger.info("\033[0;32;40m方控超车成功\033[0m")
    #         self.chk_HB_flash_on()

    # @pytest.mark.smoke
    # @pytest.mark.highbeam
    # def test_caseid_113254(self):
    #     with allure.step("Normal Driving mode_闪光未激活自动近光开远光开手动关闭远光"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         self.sd_tester.change_usage_mode(13)
    #         self.sd_tester.change_car_mode(0)
    #         self.Night_mode()
    #         self.Sped_0()
    #         self.Hibeam_off()
    #     with allure.step("设置远光关"):
    #         self.Hibeam_off()
    #     with allure.step("打开近光"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("语音开远光"):
    #        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 2)
    #        self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 2})
    #        self.chk_HB_ON()
    #     with allure.step("方控关闭远光"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
    #         )
    #         logger.info("\033[0;32;40m方控远光按键置1成功\033[0m")
    #         self.chk_HB_flash_off()
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 2)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 2}
    #         )
    #         logger.info("\033[0;32;40m方控远光按键置2成功\033[0m")
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 0)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 0}
    #         )
    #         logger.info("\033[0;32;40m方控远光按键置0成功\033[0m")
    #     with allure.step("检测远光关闭"):
    #         self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedHiBeam', 0)
    #         self.ipdu.check(
    #             self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', 0)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFlash', 0)

    # @allure.title("normal convenience远光未激活手动打开闪光")
    # @pytest.mark.full
    # @pytest.mark.full
    # def test_caseid_113562(self):
    #     '''1.BodyCAN:0x0F0 VehModMngtGlbSafe1CarModSts1 == [0]:normal
    #         2.BodyCAN:0x0F0 VehModMngtGlbSafe1UsgModSts == [2]:convenience
    #         3.BodyExposedCANFD:0x20A ActnOfLedHiBeam == disable
    #         4.BodyExposedCANFD:0x251 StsOfLedHiBeamLe == off
    #         5.BodyExposedCANFD:0x252 StsOfLedHiBeamRi == off
    #         6.BackboneFR:36-0-1 ExtrLtgStsHiBeam == off'''
    #     with allure.step("normal driving旧方向盘近光关"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         self.sd_tester.change_usage_mode(2)
    #         self.LoBeamoff_Night_Sped0()
    #         self.Hibeam_off()
    #     with allure.step("按键超车闪"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
    #         )
    #         logger.info("\033[0;32;40m方控超车成功\033[0m")
    #         self.chk_HB_flash_on()
    #     with allure.step("释放按键超车关"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 0)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 0}
    #         )
    #         logger.info("\033[0;32;40m方控释放成功\033[0m")
    #         self.chk_HB_flash_off()

    # @allure.title("normal active远光激活手动打开闪光")
    # @pytest.mark.full
    # def test_caseid_113595(self):
    #     '''1.BodyCAN:0x0F0 VehModMngtGlbSafe1CarModSts1 == [0]:normal
    #         2.BodyCAN:0x0F0 VehModMngtGlbSafe1UsgModSts == [11]:active
    #         3.BodyExposedCANFD:0x20A ActnOfLedHiBeam == enable
    #         4.BodyExposedCANFD:0x251 StsOfLedHiBeamLe == on
    #         5.BodyExposedCANFD:0x252 StsOfLedHiBeamRi == on
    #         6.BackboneFR:36-0-1 ExtrLtgStsHiBeam == on'''
    #     with allure.step("normal driving旧方向盘近光关"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #         self.Hibeam_off()
    #     with allure.step("按键超车闪"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
    #         )
    #         logger.info("\033[0;32;40m方控超车成功\033[0m")
    #         self.chk_HB_flash_on()

    # @allure.title("normal active远光激活手动打开闪光")
    # @pytest.mark.smoke
    # @pytest.mark.highbeam
    # def test_caseid_113596(self):
    #     '''1.BodyCAN:0x0F0 VehModMngtGlbSafe1CarModSts1 == [0]:normal
    #         2.BodyCAN:0x0F0 VehModMngtGlbSafe1UsgModSts == [13]:driving
    #         3.BodyExposedCANFD:0x20A ActnOfLedHiBeam == enable
    #         4.BodyExposedCANFD:0x251 StsOfLedHiBeamLe == on
    #         5.BodyExposedCANFD:0x252 StsOfLedHiBeamRi == on
    #         6.BackboneFR:36-0-1 ExtrLtgStsHiBeam == on'''
    #     with allure.step("normal driving旧方向盘近光关"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         self.LoBeamoff_Night_Sped0()
    #         self.Hibeam_off()
    #     with allure.step("按键超车闪"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
    #         )
    #         logger.info("\033[0;32;40m方控超车成功\033[0m")
    #         self.chk_HB_flash_on()

    # @allure.title("normal active远光未激活手动打开闪光")
    # @pytest.mark.full
    # def test_caseid_113541(self):
    #     '''1.BodyCAN:0x0F0 VehModMngtGlbSafe1CarModSts1 == [0]:normal
    #         2.BodyCAN:0x0F0 VehModMngtGlbSafe1UsgModSts == [11]:active
    #         3.BodyExposedCANFD:0x20A ActnOfLedHiBeam == disable
    #         4.BodyExposedCANFD:0x251 StsOfLedHiBeamLe == off
    #         5.BodyExposedCANFD:0x252 StsOfLedHiBeamRi == off
    #         6.BackboneFR:36-0-1 ExtrLtgStsHiBeam == off'''
    #     with allure.step("normal driving旧方向盘近光关"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         self.sd_tester.change_usage_mode(2)
    #         self.LoBeamoff_Night_Sped0()
    #         self.Hibeam_off()
    #     with allure.step("按键超车闪"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
    #         )
    #         logger.info("\033[0;32;40m方控超车成功\033[0m")
    #         self.chk_HB_flash_on()


    # @allure.title("normal active远光未激活手动打闪光后失活")
    # @pytest.mark.smoke
    # def test_caseid_113561(self):
    #     '''1.BodyCAN:0x0F0 VehModMngtGlbSafe1CarModSts1 == [0]:normal
    #         2.BodyCAN:0x0F0 VehModMngtGlbSafe1UsgModSts == [11]:active
    #         3.BodyExposedCANFD:0x20A ActnOfLedHiBeam == disable
    #         4.BodyExposedCANFD:0x251 StsOfLedHiBeamLe == off
    #         5.BodyExposedCANFD:0x252 StsOfLedHiBeamRi == off
    #         6.BackboneFR:36-0-1 ExtrLtgStsHiBeam == off'''
    #     with allure.step("normal active旧方向盘近光关"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #         self.Hibeam_off()
    #     with allure.step("按键超车闪"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
    #         )
    #         logger.info("\033[0;32;40m方控超车成功\033[0m")
    #         self.chk_HB_flash_on()
    #     with allure.step("释放按键超车关"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 0)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 0}
    #         )
    #         logger.info("\033[0;32;40m方控释放成功\033[0m")
    #         self.chk_HB_flash_off()


    # @allure.title("transport convenience远光未激活手动打开闪光")
    # @pytest.mark.full
    # def test_caseid_113547(self):
    #     '''1.BodyCAN:0x0F0 VehModMngtGlbSafe1CarModSts1 == [1]:transport
    #         2.BodyCAN:0x0F0 VehModMngtGlbSafe1UsgModSts == [2]:convenience
    #         3.BodyExposedCANFD:0x20A ActnOfLedHiBeam == disable
    #         4.BodyExposedCANFD:0x251 StsOfLedHiBeamLe == off
    #         5.BodyExposedCANFD:0x252 StsOfLedHiBeamRi == off
    #         6.BackboneFR:36-0-1 ExtrLtgStsHiBeam == off'''
    #     with allure.step("transport convenience旧方向盘近光关"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         self.sd_tester.change_usage_mode(2)
    #         self.LoBeamoff_Night_Sped0()
    #         self.Hibeam_off()
    #     with allure.step("按键超车闪"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
    #         )
    #         logger.info("\033[0;32;40m方控超车成功\033[0m")
    #         self.chk_HB_flash_on()


    # @allure.title("transport driving远光未激活手动打开闪光")
    # @pytest.mark.full
    # def test_caseid_113548(self):
    #     '''1.BodyCAN:0x0F0 VehModMngtGlbSafe1CarModSts1 == [1]:transport
    #         2.BodyCAN:0x0F0 VehModMngtGlbSafe1UsgModSts == [13]:driving
    #         3.BodyExposedCANFD:0x20A ActnOfLedHiBeam == disable
    #         4.BodyExposedCANFD:0x251 StsOfLedHiBeamLe == off
    #         5.BodyExposedCANFD:0x252 StsOfLedHiBeamRi == off
    #         6.BackboneFR:36-0-1 ExtrLtgStsHiBeam == off'''
    #     with allure.step("transport driving旧方向盘近光关"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         self.sd_tester.change_usage_mode(2)
    #         self.LoBeamoff_Night_Sped0()
    #         self.Hibeam_off()
    #     with allure.step("按键超车闪"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
    #         )
    #         logger.info("\033[0;32;40m方控超车成功\033[0m")
    #         self.chk_HB_flash_on()


    # @allure.title("transport driving远光未激活手动打闪光后失活")
    # @pytest.mark.full
    # def test_caseid_113568(self):
    #     '''1.BodyCAN:0x0F0 VehModMngtGlbSafe1CarModSts1 == [1]:transport
    #         2.BodyCAN:0x0F0 VehModMngtGlbSafe1UsgModSts == [13]:driving
    #         3.BodyExposedCANFD:0x20A ActnOfLedHiBeam == disable
    #         4.BodyExposedCANFD:0x251 StsOfLedHiBeamLe == off
    #         5.BodyExposedCANFD:0x252 StsOfLedHiBeamRi == off
    #         6.BackboneFR:36-0-1 ExtrLtgStsHiBeam == off'''
    #     with allure.step("transport driving旧方向盘近光关"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #         self.Hibeam_off()
    #     with allure.step("按键超车闪"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
    #         )
    #         logger.info("\033[0;32;40m方控超车成功\033[0m")
    #         self.chk_HB_flash_on()
    #     with allure.step("释放按键超车关"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 0)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 0}
    #         )
    #         logger.info("\033[0;32;40m方控释放成功\033[0m")
    #         self.chk_HB_flash_off()


    # @allure.title("transport driving远光激活手动打开闪光")
    # @pytest.mark.full
    # def test_caseid_113598(self):
    #     '''1.BodyCAN:0x0F0 VehModMngtGlbSafe1CarModSts1 == [1]:transport
    #         2.BodyCAN:0x0F0 VehModMngtGlbSafe1UsgModSts == [13]:driving
    #         3.BodyExposedCANFD:0x20A ActnOfLedHiBeam == enable
    #         4.BodyExposedCANFD:0x251 StsOfLedHiBeamLe == on
    #         5.BodyExposedCANFD:0x252 StsOfLedHiBeamRi == on
    #         6.BackboneFR:36-0-1 ExtrLtgStsHiBeam == on'''
    #     with allure.step("transport driving旧方向盘近光关"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         self.sd_tester.change_usage_mode(13)
    #         self.LoBeamoff_Night_Sped0()
    #         self.Hibeam_off()
    #     with allure.step("按键超车闪"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
    #         )
    #         logger.info("\033[0;32;40m方控超车成功\033[0m")
    #         self.chk_HB_flash_on()


    # @allure.title("transport inactive远光激活手动打开闪光")
    # @pytest.mark.full
    # def test_caseid_113564(self):
    #     '''1.BodyCAN:0x0F0 VehModMngtGlbSafe1CarModSts1 == [1]:transport
    #         2.BodyCAN:0x0F0 VehModMngtGlbSafe1UsgModSts == [1]:inactive
    #         3.BodyExposedCANFD:0x20A ActnOfLedHiBeam == disable
    #         4.BodyExposedCANFD:0x251 StsOfLedHiBeamLe == off
    #         5.BodyExposedCANFD:0x252 StsOfLedHiBeamRi == off
    #         6.BackboneFR:36-0-1 ExtrLtgStsHiBeam == off'''
    #     with allure.step("transport driving旧方向盘近光关"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         self.sd_tester.change_usage_mode(1)
    #         self.LoBeamoff_Night_Sped0()
    #         self.Hibeam_off()
    #     with allure.step("按键超车闪"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
    #         )
    #         logger.info("\033[0;32;40m方控超车成功\033[0m")
    #         self.chk_HB_flash_on()
    #     with allure.step("释放按键超车关"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 0)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 0}
    #         )
    #         logger.info("\033[0;32;40m方控释放成功\033[0m")
    #         self.chk_HB_flash_off()


    # @allure.title("transport inactive远光未激活手动打开闪光")
    # @pytest.mark.full
    # def test_caseid_113544(self):
    #     '''1.BodyCAN:0x0F0 VehModMngtGlbSafe1CarModSts1 == [1]:transport
    #         2.BodyCAN:0x0F0 VehModMngtGlbSafe1UsgModSts == [1]:inactive
    #         3.BodyExposedCANFD:0x20A ActnOfLedHiBeam == disable
    #         4.BodyExposedCANFD:0x251 StsOfLedHiBeamLe == off
    #         5.BodyExposedCANFD:0x252 StsOfLedHiBeamRi == off
    #         6.BackboneFR:36-0-1 ExtrLtgStsHiBeam == off'''
    #     with allure.step("transport driving旧方向盘近光关"):
    #         self.sd_tester.write_single_ccp(629, 4)
    #         self.sd_tester.change_usage_mode(1)
    #         self.LoBeamoff_Night_Sped0()
    #         self.Hibeam_off()
    #     with allure.step("按键超车闪"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
    #         )
    #         logger.info("\033[0;32;40m方控超车成功\033[0m")
    #         self.chk_HB_flash_on()


    # @allure.title("normal driving语音/ANP/AVP/AHBC打开远光")
    # @pytest.mark.smoke
    # def test_caseid_113638_113639(self):
    #     with allure.step("normal driving确保近光off档"):
    #         self.sd_tester.change_car_mode(0)
    #         self.sd_tester.change_usage_mode(13)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=0, usgmod=13)
    #         self.LoBeamoff_Night_Sped0()
    #         sleep(2)
    #     with allure.step("打开近光"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #         sleep(2)
    #     with allure.step("确保远光关无优先级占用"):
    #         self.Hibeam_off()
    #         sleep(1)
    #     with allure.step("语音/ANP/AVP/AHBC打开远光"):
    #         list1 = [3, 4, 5, 6]
    #         for HBID in list1:
    #             logger.info("远光优先级{0}".format(HBID))
    #             self.partner.send_method_request(
    #                 LIGHT_SERVICE_CLIENT,
    #                 "SetHighBeamControl",
    #                 {"info": {"cmd": 2, "clientId": HBID}},
    #             )
    #             self.partner.ck_s2s_event(
    #                 LIGHT_SERVICE_CLIENT, "HighBeamStatus", {"sts": {"clientId": HBID}}
    #             )
    #             with allure.step("检查远光激活"):
    #                 self.chk_HB_ON()
    #             with allure.step("检查当前优先级状态"):
    #                 if HBID == 3 or HBID == 5:
    #                     self.partner.ck_s2s_event(
    #                         LIGHT_SERVICE_CLIENT,
    #                         "HighBeamStatus",
    #                         {"sts": {"sts": 1, "clientId": 255}},
    #                     )
    #                     self.partner.send_request_and_ck_resp(
    #                         LIGHT_SERVICE_CLIENT,
    #                         "GetHighBeamStatus",
    #                         {},
    #                         {"out": {'sts': 1, 'clientId': 255}},
    #                     )
    #                 else:
    #                     self.partner.send_request_and_ck_resp(
    #                         LIGHT_SERVICE_CLIENT,
    #                         "GetHighBeamStatus",
    #                         {},
    #                         {"out": {'sts': 1, 'clientId': HBID}},
    #                     )
    #         with allure.step("恢复环境"):
    #             self.Hibeam_off()


    # @allure.title(" Normal Driving mode_闪光未激活自动近光开通过ANP或AHBC激活远光")
    # @pytest.mark.smoke
    # def test_caseid_113647(self):
    #     with allure.step("normal driving确保近光off档"):
    #         self.sd_tester.change_car_mode(0)
    #         self.sd_tester.change_usage_mode(13)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=0, usgmod=13)
    #         self.LoBeamoff_Night_Sped0()
    #         sleep(2)
    #     with allure.step("打开近光"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #         sleep(2)
    #     with allure.step("确保远光关无优先级占用"):
    #         self.Hibeam_off()
    #         sleep(1)
    #     with allure.step("语音/ANP/AVP/AHBC打开远光"):
    #         list1 = [3, 4, 5, 6]
    #         for HBID in list1:
    #             logger.info("远光优先级{0}".format(HBID))
    #             self.partner.send_method_request(
    #                 LIGHT_SERVICE_CLIENT,
    #                 "SetHighBeamControl",
    #                 {"info": {"cmd": 2, "clientId": HBID}},
    #             )
    #             self.partner.ck_s2s_event(
    #                 LIGHT_SERVICE_CLIENT, "HighBeamStatus", {"sts": {"clientId": HBID}}
    #             )
    #             with allure.step("检查远光激活"):
    #                 self.chk_HB_ON()
    #             with allure.step("检查当前优先级状态"):
    #                 if HBID == 3 or HBID == 5:
    #                     self.partner.ck_s2s_event(
    #                         LIGHT_SERVICE_CLIENT,
    #                         "HighBeamStatus",
    #                         {"sts": {"sts": 1, "clientId": 255}},
    #                     )
    #                     self.partner.send_request_and_ck_resp(
    #                         LIGHT_SERVICE_CLIENT,
    #                         "GetHighBeamStatus",
    #                         {},
    #                         {"out": {'sts': 1, 'clientId': 255}},
    #                     )
    #                 else:
    #                     self.partner.send_request_and_ck_resp(
    #                         LIGHT_SERVICE_CLIENT,
    #                         "GetHighBeamStatus",
    #                         {},
    #                         {"out": {'sts': 1, 'clientId': HBID}},
    #                     )
    #         with allure.step("恢复环境"):
    #             self.Hibeam_off()


    # @pytest.mark.smoke
    # def test_caseid_113958(self):
    #     '''转向灯(DI)激活条件_方向改变时手动右转指示'''
    #     for X in [4, 6]:
    #         self.sd_tester.write_single_ccp(629, X)
    #         self.sd_tester.change_car_mode(0)
    #         self.sd_tester.change_usage_mode(13)
    #         if X == 4:
    #             # 识别旧方向盘
    #             self.ipdu.bodycan_swtrbodyfr01_steerwhltouchswtri2steerwhltouchswt2_steerwhltouchswt_longpress()
    #             logger.info("\033[0;33;40m老方向盘右转按键轻按\033[0m")
    #             sleep(0.5)
    #             self.ipdu.bodycan_swtrbodyfr01_steerwhltouchswtri2steerwhltouchswt2_steerwhltouchswt_notavailble()
    #             logger.info("\033[0;33;40m老方向盘右转按键释放\033[0m")
    #         else:
    #             self.ipdu.bodycan_swtlbodyfr02_steerwhltouchswtle1steerwhltouchswt2_steerwhltouchswt_longpress()
    #             logger.info("\033[0;33;40m新方向盘右转按键轻按\033[0m")
    #             sleep(0.5)
    #             self.ipdu.bodycan_swtlbodyfr02_steerwhltouchswtle1steerwhltouchswt2_steerwhltouchswt_notavailble()
    #             logger.info("\033[0;33;40m新方向盘右转按键释放\033[0m")
    #         self.ipdu.check(
    #             self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 2
    #         )
    #         for num in range(3):
    #             self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
    #                             'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 2)
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 2)
    #             sleep(.4)
    #             self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51,
    #                             'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)

    # def test_relay_001(self):
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CEMBodyExpoCommonFr06, 'ExtrLiRlyPwrDwn' ,'Boolean_TRUE')
    #     self.partner.send_method_request(
    #         LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3}
    #     )  # 设置近光mode0-OFF/mode1-AUTO/mode2-POS/mode3-LoBeam
    #     logger.info("\033[0;35;40m外灯模式设置成功无通知等待300ms获取当前模式\033[0m")
    #     sleep(0.3)
    #     self.partner.send_request_and_ck_resp(
    #         LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 3}
    #     )  # 获取外灯模式mode0-OFF/mode1-AUTO/mode2-POS/mode3-LoBeam
    #     logger.info("\033[0;35;40m主动获取到预期外灯模式\033[0m")
    #     time.sleep(60)
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CEMBodyExpoCommonFr06, 'ExtrLiRlyPwrDwn' ,'Boolean_FALSE')
    #     # self.ipdu.pause_all_bus_send()
    #     self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
    #     self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
    #     self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
    #     self.ipdu.backbonefr_vddmbackbonefr03_gearlvrindcn_gearlvrindcn2_parkindcn()
    #     self.dk.set_drvr_seat_notpresent()
    #     self.dk.set_pass_seat_notpresent()
    #     self.dk.set_secle_seat_notpresent()
    #     self.dk.set_secmid_seat_notpresent()
    #     self.dk.set_secri_seat_notpresent()
    #     self.dk.reset_bncm_digital_keyinfo()
    #     self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
    #     time.sleep(.3)
    #     self.io.set_four_door_close()
    #     self.io.trunk_door_close()
    #     self.io.hood_door1_close()
    #     time.sleep(.3)
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr02,'DoorDrvrSts_2_CemBodySignalIPdu02', 2)
    #     self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'DoorPassSts_2_CEMBodySignalIPdu11', 2)
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr02,'DoorLeReSts_1_CemBodySignalIPdu02', 2)
    #     self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'DoorRiReSts_1_CEMBodySignalIPdu11', 2)
    #     self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11,'TrSts_2_CEMBodySignalIPdu11', 2)
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06,'HoodSts', 2)
    #     self.dk.set_cenlock_sts(0x3)
    #     sleep(1)
    #     self.dk.set_cenlock_sts(0x1)
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CEMBodyExpoCommonFr06, 'ExtrLiRlyPwrDwn' ,'Boolean_FALSE')
        # sleep(400)
        # self.ipdu.check(self.ipdu.bodyexposedcanfd.CEMBodyExpoCommonFr06, 'ExtrLiRlyPwrDwn' ,'Boolean_TRUE')

    # @allure.title("Normal Driving mode_信号“VehSpdLgt”E2E校验失败，近光亮")
    # @pytest.mark.full
    # def test_caseid_1987189(self):
    #     '''手动开启关闭近光'''
    #     with allure.step("normal Driving 确保近光off档"):
    #         self.sd_tester.change_car_mode(0)
    #         self.sd_tester.change_usage_mode(13)
    #         self.Lobeam_off()
    #     with allure.step("白天模式"):
    #         self.Day_mode()
    #     with allure.step("近光Auto档"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #     self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06')
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedLoBeamActnOfLedLoBeam', '1')
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActvnOfAhl', '0')