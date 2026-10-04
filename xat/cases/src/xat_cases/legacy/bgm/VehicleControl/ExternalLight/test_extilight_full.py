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
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
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
        partner_process_check()  # 检查上位机上是否有其它未关闭的soa_partner进程在运行,如果有,则杀死进程
        sleep(1)
        self.bgm_tcpdump = BGM_SSH()#导入tcp抓取模块
        self.bgm_tcpdump.init_bgm_tcpdump()
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.nucapp.bgm_diag_line_up()  # 诊断激活线连接
        self.partner = S2sBaseClass([("LightService", "client"), ("KeyService", "client")])
        sleep(2)
        self.ipdu.start_all_time_control()  # 启动数据模拟(数据库周期性报文和调度表)
        self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动,总线开始收发报文
        
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
        self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动,停止在总线收发报文
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
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 0)
            
            self.sd_tester.change_car_mode(0)
            self.sd_tester.change_usage_mode(1)
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
        global start_get_service_flag
        start_get_service_flag=0
        """检查双闪如果打开手动关闭"""
        result, realvalue, expectedvalue = self.ipdu.check(getattr(getattr(self.ipdu, 'bodycan'), 'CemBodyFr03'),
                                                        'ActvnOfIndcrIndcrOut_1_CemBodySignalIPdu03', 3,
                                                        do_assert=False)
        if result == True:
            # self.io.hazard_light_open()
            self.io.set_do_level("hazard_switch", True)
            logger.info("\033[0;33;40mHWL开关按下\033[0m")
            sleep(0.1)
            # self.io.hazard_light_close()
            self.io.set_do_level("hazard_switch", False)
            logger.info("\033[0;33;40mHWL开关释放\033[0m")
        else:
            pass
            logger.info("\033[0;33;40m检测到HWL关\033[0m")
        self.sd_tester.change_usage_mode(1)
        logger.info("\033[0;33;40m使用模式切回Inactive成功\033[0m")
        self.sd_tester.change_car_mode(0)
        logger.info("\033[0;33;40m车辆模式切回Normal成功\033[0m")
        super().after_each_func(ecu, start=False)

    def bgm_sleep_and_awake(self):
        pass  # todo

    def get_result(self): #后台启动1s周期,获取刹车灯禁用状态不关心实际返回值
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
        # start_get_service_flag=0 关 ##需要暂时停止造成通信阻塞,置0
        #start_get_service_flag=1 开  ##恢复通讯继续调用,置1,下两行配套使用
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
        self.mode = mode#请求打开的模式
        A = self.partner.send_request_and_return_resp(
            LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}
        )["out"]#获取当前的灯模式

        if A != mode:#如果当前的模式不等于请求的模式
            logger.info("\033[0;35;40m当前外灯模式不等设置值,开始切换模式\033[0m")
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
            logger.info("\033[0;35;40m当前外灯模式等于设置值,重新设置当前模式\033[0m")
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
        )  # 车速0,QF值3;
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06',
            0,
        )  # 车速0,QF值3;
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06',
            3,
        )  # 车速0,QF值3;
        self.ipdu.set(
            self.ipdu.backbonefr.BbmVcuBackBoneFr05,
            'VehSpdLgtForBkpVehSpdLgtQf_1_BbmVcuBackBoneSignalIPdu05',
            3,
        )  # 车速0,QF值3;

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
                                            64: 3,  # With Alarm Using Vehicle Horn 即siren,警报器
                                            543: 1,  # Without Battery Backed-Up Sounder 即BBS
                                            66: 1,  # Without inclination sensor 即IS倾斜传感器
                                            65: 1,  # Without Interior Motion Sensor 即内部运动传感器
                                            1: 0xA3,  # 适用配置了舒适泊车模式的车型,对应设防准备时间 30s
                                            69: 1,  # Re-trig次数,一个报警周期30s鸣笛停止10s
                                            70: 1,  # 无被动设防
                                            13: 4,  # 动力类型Battery electric vehicle,上切Active或Driving可解防
                                            })
        with allure.step("五门关闭"):
            self.io.init_bgm_HW()  # 用例开启始前都先恢复5门关门状态,主驾无人,车门按钮未按下
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
    
    # @pytest.mark.full
    # @pytest.mark.parametrize("carmode,usagmode",[(3,2),(3,13),(3,11),(1,2),(1,13),(1,11),(2,2),(2,13),(2,11),(0,13),(0,2),(0,11)],
    #                          ids=['113409','113406','113398','113366','113362','113358','113325','113323','113313','113270','113263','113255'])
    # def test_caseid_lowbeam_manual(self,carmode, usagmode):
    #     '''手动开启和关闭近光灯'''
    #     # allure.dynamic.title(
    #     #     "当Carmode:{}, Usagemode:{}手动开启和关闭近光灯".format(carmode, usagmode)
    #     # )
    #     with allure.step("确保近光off档"):
    #         self.sd_tester.change_car_mode(carmode)
    #         self.sd_tester.change_usage_mode(usagmode)
    #         sleep(2)
    #         self.chk_fr_carmod_usgmod(carmod=carmode, usgmod=usagmode)
    #         self.Night_mode()
    #         self.Sped_0()
    #         self.Lobeam_off()
    #     with allure.step("大灯近光档使S2Sservice到MCU信号SwtCDCLi.LoBeamSw==on"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #     with allure.step("检查近光激活状态"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("MPU到MCU信号SwtCDCLi.LoBeamSw == off"):    
    #         self.req_event_get_ExtiLight_mode(mode=0)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    
    # @pytest.mark.full
    # @pytest.mark.parametrize("carmode,usagmode",[(3,13),(3,11),(2,13),(2,11),(1,13),(1,11),(0,13),(0,11)],
    #                          ids=['113619','113618','113616','113615','113614','113613','113612','113611'])
    # def test_caseid_open_hibeam(self,carmode,usagmode):
    #     '''手动近光和闪光开启然后请求开远光'''
    #     # allure.dynamic.title(
    #     #     "当Carmode:{}, Usagemode:{}手动近光和闪光开启然后请求开远光".format(carmode, usagmode)
    #     # )
    #     with allure.step("大灯近光档使S2Sservice到MCU信号SwtCDCLi.LoBeamSw==on"):
    #         self.sd_tester.change_car_mode(carmode)
    #         self.sd_tester.change_usage_mode(usagmode)
    #         self.chk_fr_carmod_usgmod(carmod=carmode, usgmod=usagmode)
    #         self.Night_mode()
    #         self.Sped_0()
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #     with allure.step("检查近光激活状态"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("打开闪光灯"):    
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)#短按打开闪光,是否需要恢复为0
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
    #         )
    #         logger.info("\033[0;32;40m方控超车成功\033[0m")
    #         self.chk_HB_flash_on()
    #     with allure.step("打开远光灯"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 2)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 2}
    #         )
    #     with allure.step("按键恢复0"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 0)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 0}
    #         )
    #     with allure.step("检测远光开启"):
    #         self.chk_HB_ON()

    # @pytest.mark.full
    # @pytest.mark.parametrize("carmode,usagmode",[(3,13),(3,11),(2,13),(2,11),(1,13),(1,11),(0,13),(0,11)],
    #                          ids=['113637','113636','113635','113634','113633','113632','113631','113630'])
    # def test_caseid_close_hibeam(self,carmode,usagmode):
    #     '''闪光未激活手动近光远光开手动关闭远光'''
    #     # allure.dynamic.title(
    #     #     "当Carmode:{}, Usagemode:{}闪光未激活手动近光远光开手动关闭远光".format(carmode, usagmode)
    #     # )
    #     with allure.step("大灯近光档使S2Sservice到MCU信号SwtCDCLi.LoBeamSw==on"):
    #         self.sd_tester.change_car_mode(carmode)
    #         self.sd_tester.change_usage_mode(usagmode)
    #         self.chk_fr_carmod_usgmod(carmod=carmode, usgmod=usagmode)
    #         self.Night_mode()
    #         self.Sped_0()
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #     with allure.step("检查近光激活状态"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #         self.chk_HB_flash_off()#检查闪光未激活
    #     with allure.step("打开远光灯"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 2)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 2}
    #         )
    #     with allure.step("按键恢复0"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 0)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 0}
    #         )
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

    # @pytest.mark.full
    # @pytest.mark.parametrize("carmode,usagmode",[(2,1),(5,2),(2,13),(5,1),(3,13),(0,2),(2,11),(2,2),(3,1),(0,13),(3,2),(5,11),(3,11),(0,1),(5,13),(0,11)],
    #                          ids=['111372','111331','115061','115034','115005','115002','114913','114902','114890','114871','114868','114850','114803','114783','114742','114729'])
    # def test_caseid_open_hwl(self,carmode,usagmode):
    #     '''按压一次HWL开关激活HWL'''
    #     # allure.dynamic.title(
    #     #     "当Carmode:{}, Usagemode:{}按压一次HWL开关激活HWL".format(carmode, usagmode)
    #     # )
    #     # self.sd_tester.write_single_ccp(629, 4)
    #     self.sd_tester.change_car_mode(carmode)
    #     self.sd_tester.change_usage_mode(usagmode)
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
    #     for num in range(3):
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 3)
    #         sleep(.4)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)

    # @pytest.mark.full
    # @pytest.mark.parametrize("carmode,usagmode",[(3,13),(3,11),(2,13),(2,11),(1,13),(1,11),(0,13),(0,11)],
    #                          ids=['113629','113628','113627','113626','113625','113624','113623','113622'] ) 
    # def test_caseid_auto_hibeam(self,carmode,usagmode):
    #     '''自动近光和闪光开启然后请求开远光'''
    #     self.sd_tester.change_car_mode(carmode)
    #     self.sd_tester.change_usage_mode(usagmode)
    #     with allure.step("设置夜晚模式"):
    #         self.Night_mode()
    #     with allure.step("自动近光打开"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("闪光打开"):
    #         self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
    #         self.partner.ck_s2s_event(
    #             LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
    #         )
    #         logger.info("\033[0;32;40m方控超车成功\033[0m")
    #         self.chk_HB_flash_on()
    #     with allure.step("请求打开远光"):
    #         self.req_event_HB_mode(cmd_value=2, hbid_value=3, hbsts_prty=3)
    #         logger.info("\033[0;32;40m语音打开远光调用成功\033[0m")
    #         self.chk_HB_ON()

    # @pytest.mark.full
    # @pytest.mark.parametrize("carmode,usagmode",[(2,2),(1,11),(0,11),(1,1),(5,11),(2,13),(0,1),(5,1),(3,2),(3,1),
    #                                              (3,11),(2,11),(1,2),(5,2),(1,13),(5,13),(3,13),(0,13),(0,2),(2,1)],
    #                          ids=['115260','115244','115242','115236','115235','115234','115229','115227','115222','115221',
    #                               '115219','115212','115207','115203','115202','115196','115182','115178','115153','115152'])
    # def test_caseid_brkped_safety(self,carmode,usagmode):
    #     "踩刹车点亮刹车灯后刹车信号Qf !=3 超过200ms"
    #     self.sd_tester.change_car_mode(carmode)
    #     self.sd_tester.change_usage_mode(usagmode)
    #     logger.info("读cpuload----------------------------------")
    #     self.sd_tester.client_sim.send_data([0x22, 0xDB, 0x02])
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_On')
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 2)#Qf !=3 超过200ms
    #     time.sleep(.3)
    #     # LED刹车灯
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp', 'OnOff1_Off')
    #     #中央刹车灯
    #     self.ipdu.check(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr01, 'ActnOfLedStopLampMid', 'OnOff1_Off')
    #     #刹车灯状态
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', 'DevSts4_Off')

    # @pytest.mark.full
    # @pytest.mark.parametrize("carmode,usagmode1,usagmode2",[(3,13,1),(1,13,1),(2,13,1),(0,13,1),(3,2,1),(1,2,1),(2,2,1),(0,2,1),(3,11,1),(1,11,1),(2,11,1),(0,11,1)],
    #                          ids=['113423','113384','113344','113299','113430','113394','113354','113309','113427','113388','113351','113301'])
    # def test_caseid_lowbeam_handoff_inactive(self,carmode,usagmode1,usagmode2):
    #     '''
    #     手动点亮的近光Driving变为Inactive熄灭
    #     手动点亮的近光Convenience变为Inactive熄灭
    #     手动点亮的近光Active变为Inactive熄灭
    #     '''
    #     self.sd_tester.change_car_mode(carmode)
    #     self.sd_tester.change_usage_mode(usagmode1)
    #     #开近光
    #     self.req_event_get_ExtiLight_mode(mode=3)
    #     with allure.step("检查近光激活状态"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     self.sd_tester.change_usage_mode(usagmode2)
    #     with allure.step("下切active近光熄灭"):
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)


    # @pytest.mark.full
    # @pytest.mark.parametrize("carmode,usagmode",[(2,11),(2,13),(0,13),(0,2),(1,11),(3,2),(3,13),(1,2),(2,2),(1,13),(3,11),(0,11)],
    #                          ids=['114899','114888','114869','114867','114858','114842','114809','114789','114784','114759','114731','113435'])
    # def test_caseid_auto_lowbeam_night(self,carmode,usagmode):
    #     '''自动近光夜晚被点亮'''
    #     with allure.step("normal driving mode 确保近光off档"):
    #         self.sd_tester.change_car_mode(carmode)
    #         self.sd_tester.change_usage_mode(usagmode)
    #     self.Night_mode()
    #     self.Sped_0()
    #     self.Lobeam_off()
    #     with allure.step("近光Auto档"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @pytest.mark.full
    # @pytest.mark.parametrize("carmode,usagmode",[(3,13),(1,11),(0,13),(1,2),(2,13),(3,11),(2,11),(1,13),(2,2),(0,2),(3,2),(0,11)],
    #                          ids=['115022','114915','114876','114870','114849','114844','114828','114819','114792','114769','114757','113436'])
    # def test_caseid_auto_lowbeam_day(self,carmode,usagmode):
    #     '''自动近光白天未被点亮'''
    #     with allure.step("normal driving mode 确保近光off档"):
    #         self.sd_tester.change_car_mode(carmode)
    #         self.sd_tester.change_usage_mode(usagmode)
    #         self.Sped_0()
    #         self.Lobeam_off()
    #     with allure.step("切到白天"):
    #         self.Day_mode()
    #     with allure.step("近光Auto未点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @pytest.mark.full
    # @pytest.mark.parametrize("carmode,usagmode",[(3,13),(3,2),(3,11),(2,2),(0,2),(1,2),(2,11),(1,13),(1,11),(2,13),(0,13),(0,11)],
    #                          ids=['115015','114990','114986','114914','114901','114895','114874','114856','114847','114839','114786','113441'])
    # def test_caseid_autolowbeam_day_to_night(self,carmode,usagmode):
    #     '''自动近光白天切夜晚被点亮'''
    #     file_path, save_name = self.bgm_tcpdump.start_bgm_tcpdump()
    #     with allure.step("normal convenience mode 确保近光off档"):
    #         self.sd_tester.change_car_mode(carmode)
    #         self.sd_tester.change_usage_mode(usagmode)
    #         self.Sped_0()
    #         self.Lobeam_off()
    #     with allure.step("切到白天"):
    #         self.Day_mode()
    #     with allure.step("近光Auto未点亮"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    #     with allure.step("夜晚"):
    #         self.Night_mode()
    #         sleep(0.2)
    #     with allure.step("近光点亮"):
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     self.bgm_tcpdump.stop_bgm_tcpdump()
    #     file_path=self.bgm_tcpdump.scp_bgm_log_to_local(bgm_log_name=save_name)
    #     self.bgm_tcpdump.delete_bgm_tcpdump_file(bgm_log_name='*.pcap')

    # @pytest.mark.full
    # @pytest.mark.parametrize("carmode,usagmode",[(3,11),(3,13),(3,2),(0,2),(2,11),(0,13),(2,13),(2,2),(1,11),(1,2),(1,13),(0,11)],
    #                          ids=['111391','115069','114846','114843','114838','114836','114832','114829','114826','114821','114806','113442'])
    # def test_caseid_114869(self,carmode,usagmode):
    #     '''自动近光夜晚切白天熄灭'''
    #     self.sd_tester.change_car_mode(carmode)
    #     self.sd_tester.change_usage_mode(usagmode)
    #     self.LoBeamoff_Night_Sped0()
    #     with allure.step("近光Auto档"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("白天近光熄灭"):
    #         self.Day_mode()
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    
    # @pytest.mark.full
    # @pytest.mark.parametrize("carmode,usagmode",[(3,11),(3,2),(3,13),(2,11),(2,2),(2,13),(0,11),(0,2),(0,13),(1,11),(1,2),(1,13)],
    #                          ids=['114772','114762','114911','114761','114813','111385','114891','114745','114854','114831','114834','114782'])
    # def test_caseid_auto_to_manual(self,carmode,usagmode):
    #     '''夜晚自动切手动近光继续被点亮'''
    #     with allure.step("确保近光off档"):
    #         self.sd_tester.change_car_mode(carmode)
    #         self.sd_tester.change_usage_mode(usagmode)
    #         self.LoBeamoff_Night_Sped0()
    #     with allure.step("近光Auto档"):
    #         self.req_event_get_ExtiLight_mode(mode=1)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     with allure.step("近光OFF档"):
    #         self.req_event_get_ExtiLight_mode(mode=3)
    #         self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    # @pytest.mark.full
    # @pytest.mark.parametrize("carmode,usagmode1,usagmode2",[(3,1,13),(2,1,13),(0,1,13),(1,1,13),(3,1,2),(2,1,2),(0,1,2),(1,1,2),(3,0,2),(2,0,2),(0,0,2),(1,0,2),
    #                                              (3,1,11),(2,1,11),(0,1,11),(1,1,11),(3,0,11),(2,0,11),(0,0,11),(1,0,11)],
    #                          ids=['114811','114815','114752','114778','114861','114754','114882','14765','114756','114800','114860','114886',
    #                               '114808','114884','114767','114758','114878','114763','114797','114880'])
    # def test_caseid_lowbeam_usagmode(self,carmode,usagmode1,usagmode2):
    #     '''
    #     手动开关打开Inactive变为Driving点亮近光
    #     手动开关打开Inactive变为Convenience点亮近光
    #     手动开关打开Abandoned变为Convenience点亮近光
    #     手动开关打开Inactive变为Active点亮近光
    #     手动开关打开Abandoned变为Active点亮近光
    #     '''
    #     self.sd_tester.change_car_mode(carmode)
    #     self.sd_tester.change_usage_mode(usagmode1)
    #     #手动打开近光灯
    #     self.req_event_get_ExtiLight_mode(mode=3)
    #     self.sd_tester.change_usage_mode(usagmode2)
    #     self.chk_CanBus_LB_sts(Actn=1, Extr=1)

    #用例有问题待分析   
    def test_caseid_hibeam_manual(self):
        '''远光激活手动打闪光后远光失活'''
        with allure.step("normal driving旧方向盘近光关"):
            self.sd_tester.write_single_ccp(629, 4)
            sleep(2)
            self.sd_tester.change_car_mode(0)
            self.sd_tester.change_usage_mode(13)
            self.LoBeamoff_Night_Sped0()
            self.Hibeam_off()
        with allure.step("按键超车闪"):
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
            self.partner.ck_s2s_event(
                LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1}
            )
            logger.info("\033[0;32;40m方控超车成功\033[0m")
            self.chk_HB_flash_on()
        with allure.step("释放按键超车关"):
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 0)
            self.partner.ck_s2s_event(
                LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 0}
            )
            logger.info("\033[0;32;40m方控释放成功\033[0m")
            self.chk_HB_flash_off()
            # set_no_crc
    
    # 113509,113506,1113505与该用例合并为一个case
    # @pytest.mark.parametrize("usagmode",[(2),(11),(13)],ids=['113497','113496','113495'])
    # def test_caseid_bgm_reset_openlowbeam(self,usagmode):
    #     '''近光开电源复位近光600ms内打开并保持'''
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(usagmode)
    #     self.req_event_get_ExtiLight_mode(mode=3)
    #     self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     self.nucapp.bgm_power_off()
    #     time.sleep(1)
    #     self.nucapp.bgm_power_on()
    #     sleep(.6)
    #     self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     sleep(3)
    #     with allure.step("MPU到MCU信号SwtCDCLi.LoBeamSw == off"):    
    #         self.req_event_get_ExtiLight_mode(mode=0)
    #         self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @pytest.mark.parametrize("usagmode",[(2),(11),(13)],ids=['113503','113502','113499'])
    # def test_caseid_bgm_reset_closelowbeam(self,usagmode):
    #     '''近光关电源复位近光600ms内打开并保持'''
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(usagmode)
    #     self.req_event_get_ExtiLight_mode(mode=0)
    #     self.chk_CanBus_LB_sts(Actn=0, Extr=0)
    #     #重启mcu,mcu回51 01
    #     self.sd_tester.send_data([0x11,0x01])
    #     sleep(.6)
    #     self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     sleep(3)
    #     self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    
    # @pytest.mark.parametrize("usagmode",[(2),(11),(13)],ids=['113514','113512','113510'])
    # def test_caseid_bgm_reset_autolowbeam_day(self,usagmode):
    #     '''夜晚AUTO近光开电源复位(MCU重启)近光重新打开后切换白天'''
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(usagmode)
    #     self.Night_mode()
    #     self.Sped_0()
    #     self.req_event_get_ExtiLight_mode(mode=1)
    #     self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     #重启mcu,mcu回51 01
    #     self.sd_tester.send_data([0x11,0x01])
    #     sleep(.6)
    #     self.chk_CanBus_LB_sts(Actn=1, Extr=1)
    #     sleep(2)
    #     self.Day_mode()
    #     self.chk_CanBus_LB_sts(Actn=0, Extr=0)

    # @pytest.mark.parametrize("carmode",[(0),(3),(5)],ids=['114983','114768','114956'])
    # def test_caseid_hwl_auto_ebl(self,carmode):
    #     '''自动紧急制动以低速制动时制动灯(EBL)请求点亮HWL后按压HWL开关关闭HWL'''
    #     self.sd_tester.write_single_ccp(114, 2)
    #     self.sd_tester.change_car_mode(carmode)
    #     self.sd_tester.change_usage_mode(13)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
    #     #踩刹车
    #     # self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'BrkLiOnReqSts', 'ReqSts1_Reqd')
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EmgyBrkLiReqEmgyBrk', 'EblReq_EmgyBrkgInProgsAtSpdLo')
    #     #危险报警灯闪烁
    #     for num in range(3):
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 3)
    #         sleep(.4)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #     #按压HWL开关关闭HWL
    #     self.io.set_do_level("hazard_switch", True)
    #     logger.info("\033[0;35;40mHWL开关已释放\033[0m")
    #     sleep(0.2)
    #     # self.io.set_do_level("hazard_switch", False)
    #     # logger.info("\033[0;33;40mHWL已关闭\033[0m")
    #     self.ipdu.check(
    #                     self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 3
    #                     )
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)

    # @pytest.mark.parametrize("carmode",[(0),(3),(5)],ids=['115096','114979','114962'])
    # def test_caseid_hwl_ebl(self,carmode):
    #     '''紧急制动以低速制动时制动灯(EBL)请求点亮HWL后按压HWL开关关闭HWL'''
    #     self.sd_tester.write_single_ccp(114, 2)
    #     self.sd_tester.change_car_mode(carmode)
    #     self.sd_tester.change_usage_mode(13)
    #     #踩刹车
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'BrkLiOnReqSts', 'ReqSts1_Reqd')
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EmgyBrkLiReqEmgyBrk', 'EblReq_EmgyBrkgInProgsAtSpdLo')
    #     #危险报警灯闪烁
    #     for num in range(3):
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 3)
    #         sleep(.4)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #     #按压HWL开关关闭HWL
    #     self.io.set_do_level("hazard_switch", True)
    #     logger.info("\033[0;35;40mHWL开关已释放\033[0m")
    #     sleep(0.2)
    #     # self.io.set_do_level("hazard_switch", False)
    #     # logger.info("\033[0;33;40mHWL已关闭\033[0m")
    #     self.ipdu.check(
    #                     self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts_1_CemBodyExpoSignalIPdu51', 3
    #                     )
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    
    #跑不通，需要台架手动
    # def test_caseid_hwl_locking(self):
    #     '''闭锁hwl闪烁一次,解锁hwl闪烁两次'''
    #     self.io.init_bgm_HW()  # 用例开启始前都先恢复5门关门状态，主驾无人，车门按钮未按下
    #     self.io.hood_door1_close()#37接地
    #     self.io.hood_door2_open()#36悬空
    #     with allure.step("设置整车锁解锁"):
    #         self.dk.set_cenlock_sts(0x1)
    #         for num in range(2):
    #             self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 3)
    #         sleep(.4)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #     with allure.step("设置整车锁上锁"):
    #         self.dk.set_cenlock_sts(0x3)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 3)
    #         sleep(.4)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    #     self.dk.set_cenlock_sts(0x1)

    #防盗关失活HWL与该用例合并为1个用例
    # @pytest.mark.parametrize("carmode,usagmode",[(3,0),(3,1),(5,0),(5,1),(0,0),(0,1)],ids=['114952','114927','115078','114760','115055','1912472'])
    # def test_caseid_alrm_open_hwl(self,carmode,usagmode):
    #     '''防盗请求HWL(Inactive abandon下触发防盗 Factroy transport不能闭锁)'''
    #     self.sd_tester.change_car_mode(carmode)
    #     self.sd_tester.change_usage_mode(usagmode)
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
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #     self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)

    # @pytest.mark.parametrize("carmode,usagmode",[(5,2)],ids=['115086'])
    # def test_caseid_hwl_by_crash(self,carmode,usagmode):
    #     '''碰撞事件激活HWL'''
    #     self.sd_tester.change_car_mode(carmode)
    #     self.sd_tester.change_usage_mode(usagmode)
    #     self.sd_tester.change_car_mode(3)
    #     # self.ipdu.set(
    #     #         self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashPed', 'Boolean_TRUE')
    #     for num in range(3):
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 3)
    #         sleep(.4)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)

    # @pytest.mark.parametrize("carmode,usagmode",[(5,2)],ids=['115086'])
    # def test_caseid_hwl_by_crash(self,carmode,usagmode):
    #     '''碰撞事件激活HWL'''
    #     self.sd_tester.change_car_mode(carmode)
    #     self.sd_tester.change_usage_mode(usagmode)
    #     self.ipdu.set(
    #             self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashPed', 'Boolean_TRUE')
    #     for num in range(3):
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_On'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 3)
    #         sleep(.4)
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 'DevSts4_Off'),
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
    # def test_caseid_turnlight(self):
    #     self.sd_tester.change_usage_mode(13)
    #     self.sd_tester.change_car_mode(0)
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 0, "priority": 47}})
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
    #                                      {"lamp": {"mode": 0, "priority": 255}})
    #     # 检查转向灯为关
    #     # self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts_2_CemBodySignalIPdu01', 0)

    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 1, "priority": 47}})
    #     # 检查获取通知左转向灯开
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts_2_CemBodySignalIPdu01', 1)

    #     self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
    #                                           {"out": {"mode": 1, "priority": 47}})
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampHold", {"flag": 0})
    #     # 设置方向盘角度为10度和0度
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAgSpd_0_VDDMBackBoneSignalIPdu02', 46)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAgSpd_0_VDDMBackBoneSignalIPdu02', 29)

    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts_2_CemBodySignalIPdu01', 1)

    # def test_01(self):
    #     #新方向盘
    #     self.sd_tester.write_single_ccp(629, 6)
    #     #老方向盘

    # @pytest.mark.parametrize("carmode,usagmode",[(2,2),(1,11),(0,11),(1,1),(5,11),(2,13),(0,1),(5,1),(3,2),(3,1),
    #                                              (3,11),(2,11),(1,2),(5,2),(1,13),(5,13),(3,13),(0,13),(0,2),(2,1)],
    #                          ids=['115260','115244','115242','115236','115235','115234','115229','115227','115222','115221',
    #                               '115219','115212','115207','115203','115202','115196','115182','115178','115153','115152'])
    # def test_02(self,carmode,usagmode):
    #     self.sd_tester.change_car_mode(carmode)
    #     self.sd_tester.change_usage_mode(usagmode)
    #     logger.info("读cpuload----------------------------------")
    #     self.sd_tester.client_sim.send_data([0x22, 0xDB, 0x02])
    #     self.partner.send_request_and_return_resp(
    #         LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}
    #     )["out"]
    #     self.sd_tester.client_sim.send_data([0x22, 0xDB, 0x02])
    # def test_caseid_