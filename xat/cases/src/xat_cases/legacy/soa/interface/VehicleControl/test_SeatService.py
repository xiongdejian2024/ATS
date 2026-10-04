# -*- coding: utf-8 -*-
"""
@File        : test_soa_heat.py
@Author      : tao.cheng_ext@jiduatuo.com
@Time        : 2023/06/10 15:00 PM
@Description : Test s2s interface about heat function
"""

import os
import sys

from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_cases.legacy.soa.case_helper.parse_excel import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_cases.legacy.soa.case_helper.utils import *

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path.split("sat")[0], "sat"))
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.common.logger import logger

# from test_case.bgm.s2s.case_helper.contants import CAN_CONSTANT, DOWNSTREAM

partner = None
sd_test = None
COCKPITPERCEPTION_SERVICE_CLIENT = "cockpit_perception_service_server"
@allure.feature("SOA服务接口")
@allure.story("整车控制/SeatService")
class TestSeatService(TestBase):
    
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("SeatService", "client"),
                                     ("WTIService", "client"),
                                     ("RPAAPAService", "server"),
                                     ("cockpit_perception_service","server"),
                                     ("InteractiveService","server")
                                     ])
        self.partner.method_default_timeout = 0.1
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.io_obj = self.io.io_obj
        #保持诊断状态
        self.sd_tester.tester_present()
        self.bgm_tcpdump = BGM_SSH()
        self.bgm_tcpdump.init_bgm_tcpdump()
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.set_four_Door_open() 
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        sleep(3)
        self.set_four_Door_close()
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                            {"firstLeftExist":False,"firstRightExist":False,"errorCode":0}})
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{"seatStsSecondLeft":{"installSts":False,"occupySts":False},"seatStsSecondRight":{"installSts":False,"occupySts":False}}})
        self.ipdu.set_vehspd(0)
        self.Shift_Gear(0)
        sleep(0.2)
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)
        self.dk.set_cenlock_sts(0x1)
        self.partner.empty_all(0.5)
        logger.info("case开始运行*************************************************************")
        
    def after_each_func(self, ecu):
        # todo 停止抓包
        logger.info("case结束运行*************************************************************")
        self.ipdu.resume_all_bus_send()
        self.seat_belt_status(1,1,1,1,1)
        super().after_each_func(ecu, start=False)
 
    def after_class(self, ecu):
        self.partner.stop_operators()
        self.sd_tester.stop_tester_present()
        self.bgm_tcpdump.stop_bgm_tcpdump()
        self.bgm_tcpdump.delete_bgm_tcpdump_file(bgm_log_name='*.pcap')
        super().after_class(self, ecu)


    def seat_belt_status(self,A,B,C,D,E):
        """设置主驾 副驾 左后 后中 后右 1代表已系 0 代表未系"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', A)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1', B)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecLeBltLockSt1', C)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecLeBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecMidBltLockSt1', D)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecMidBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecRiBltLockSt1', E)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecRiBltLockSts', 0)
        sleep(1)
    
    def BGM_down_up(self,X,Y,Z):
        """X代表总线停后等待时间 Y代表下电后电等待时间 Z代表上电后电等待时间"""
        sleep(X)
        self.nucapp.bgm_power_off()
        sleep(Y)
        self.nucapp.bgm_power_on()
        sleep(Z)

    def set_drvr_position(self,hei,sld,angle,poshei):
        """设置主驾四个部分位位置0 0 0 180 方便4个调节信号都发1 向上或向前"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiPerc', hei)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldPerc', sld)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'SeatBackAngleRowFirstDrvr', angle)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiPerc', poshei)
        sleep(1)

    def set_drvr_position1(self):
        """设置主驾四个部分位位置0 0 0 180 方便4个调节信号都发1 向上或向前"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiPerc', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldPerc', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'SeatBackAngleRowFirstDrvr', 160)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiPerc', 0)
        sleep(1)

    def set_drvr_position1Valid(self,HeiQF,FrntHeiQF,PosSldQF):
        """设置主驾高度 腿托 前后位置有效性"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiPerc', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldPerc', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'SeatBackAngleRowFirstDrvr', 160)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiPerc', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF', HeiQF)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF', FrntHeiQF)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', PosSldQF)
        sleep(1)

    def set_drvr_position2(self):
        """设置主驾四个部分位位置100 100 100 0 方便4个调节信号都发2 向下或向后"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiPerc', 100.0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldPerc', 100.0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'SeatBackAngleRowFirstDrvr', 104)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiPerc', 100.0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', 3)
        sleep(1)

    def set_drvr_position3(self):
        """设置主驾四个部分位位置1 方便4个调节信号都发1 向上或向前"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiPerc', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldPerc', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'SeatBackAngleRowFirstDrvr', 160)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiPerc', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', 3)
        sleep(1)

    def set_drvr_position4(self):
        """设置主驾四个部分位位置2 方便4个调节信号都发2 向下或向后"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiPerc', 100.0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldPerc', 100.0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'SeatBackAngleRowFirstDrvr', 104)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiPerc', 100.0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', 3)
        sleep(1)

    def set_Pass_position(self,hei,sld,angle,poshei):
        """设置副驾四个部分位位置0 0 0 180 方便4个调节信号都发1 向上或向前"""
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiPerc', hei)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldPerc',  sld)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'SeatBackAngleRowFirstPass', angle)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiPerc', poshei)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiQF', 3)
        sleep(1)
        
    def set_Pass_position1(self):
        """设置副驾四个部分位位置0 0 0 180 方便4个调节信号都发1 向上或向前"""
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiPerc',  0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldPerc',  0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'SeatBackAngleRowFirstPass', 160)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiPerc', 0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiQF', 3)
        sleep(1)

    def set_Pass_position1Valid(self,HeiQF,FrntHeiQF,PosSldQF):
        """设置主驾高度 腿托 前后位置有效性"""
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiPerc',  0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldPerc',  0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'SeatBackAngleRowFirstPass', 160)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiPerc', 0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiQF', HeiQF)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldQF', PosSldQF)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiQF', FrntHeiQF)
        sleep(1)

    def set_Pass_position2(self):
        """设置副驾四个部分位位置100 100 100 0 方便4个调节信号都发2 向下或向后"""
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiPerc',  100.0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldPerc',  100.0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'SeatBackAngleRowFirstPass', 104)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiPerc', 100.0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiQF', 3)
        sleep(1)

    def set_Pass_position3(self):
        """设置副驾四个部分位置1 0 0 0 180 方便4个调节信号都发1 向上或向前"""
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiPerc',  0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldPerc',  0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'SeatBackAngleRowFirstPass', 160)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiPerc', 0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiQF', 3)
        sleep(1)

    def set_Pass_position4(self):
        """设置副驾四个部分位位置2 100 100 100 0方便4个调节信号都发2 向下或向后"""
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiPerc',  100.0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldPerc',  100.0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'SeatBackAngleRowFirstPass', 104)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiPerc', 100.0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiQF', 3)
        sleep(1)

    def set_drvr_frontheiperc(self, perc):
        """设置主驾腿托位置"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiPerc', perc)

    def set_drvr_sldperc(self, perc):
        """设置主驾前后位置"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldPerc', perc)

    def set_drvr_angelperc(self, perc):
        """设置主驾靠背角度"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'SeatBackAngleRowFirstDrvr', perc)

    def set_drvr_heiperc(self, perc):
        """设置主驾高度位置"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiPerc', perc)

    def set_drvr_heipercValid(self, QF):
        """设置主驾高度位置有效性"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF', QF)

    def set_drvr_frontheipercValid(self, QF):
        """设置主驾腿托位置有效性"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF', QF)

    def set_drvr_sldpercValid(self, QF):
        """设置主驾前后位置有效性"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', QF)

    def set_pass_frontheiperc(self, perc):
        """设置副驾腿托位置"""
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiPerc', perc)

    def set_pass_sldperc(self, perc):
        """设置副驾前后位置"""
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldPerc', perc)

    def set_pass_sldpercValid(self, QF):
        """设置副驾前后位置有效性"""
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldQF', QF)

    def set_pass_angelperc(self, perc):
        """设置副驾靠背角度"""
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'SeatBackAngleRowFirstPass', perc)

    def set_pass_heiperc(self, perc):
        """设置副驾高度位置"""
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiPerc', perc)

    def set_pass_heipercValid(self, QF):
        """设置副驾高度位置有效性"""
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiQF', QF)

    def set_pass_frontheipercValid(self, QF):
        """设置副驾腿托位置有效性"""
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiQF', QF)

    def check_drvrseat_adjust(self, DrvrLenthReq, DrvrangelReq, DrvrfrontheighReq, DrvrheighReq):
        """检查主驾前后 靠背 腿托 高度的设置信号"""
        CemBodyFr74 = self.ipdu.bodycan.CemBodyFr74
        self.ipdu.check_multiple_signals([(CemBodyFr74, 'SeatLenAdjmtRowFirstDrvr', DrvrLenthReq),
                                          (CemBodyFr74, 'BackRestAdjmtRowFirstDrvr', DrvrangelReq),
                                          (CemBodyFr74, 'SeatCushTiltAdjmtRowFirstDrvr', DrvrfrontheighReq),
                                          (CemBodyFr74, 'SeatHeiAdjmtRowFirstDrvr', DrvrheighReq)], timeout=1)
        
    def check_Passseat_adjust(self, DrvrLenthReq, DrvrangelReq, DrvrfrontheighReq, DrvrheighReq):
        """检查副驾前后 靠背 腿托 高度的设置信号"""
        CemBodyFr74 = self.ipdu.bodycan.CemBodyFr74
        self.ipdu.check_multiple_signals([(CemBodyFr74, 'SeatLenAdjmtRowFirstPass', DrvrLenthReq),
                                          (CemBodyFr74, 'BackRestAdjmtRowFirstPass', DrvrangelReq),
                                          (CemBodyFr74, 'SeatCushTiltAdjmtRowFirstPass', DrvrfrontheighReq),
                                          (CemBodyFr74, 'SeatHeiAdjmtRowFirstPass', DrvrheighReq)], timeout=1)
        
    def check_drvrseat_heightsld_adjust(self, DrvrLenthReq, DrvrheighReq):
        """检查主驾前后 高度 的设置信号"""
        CemBodyFr74 = self.ipdu.bodycan.CemBodyFr74
        self.ipdu.check_multiple_signals([(CemBodyFr74, 'SeatLenAdjmtRowFirstDrvr', DrvrLenthReq),
                                          (CemBodyFr74, 'SeatHeiAdjmtRowFirstDrvr', DrvrheighReq)], timeout=1)
        
    def check_drvrseat_kaotuituo_adjust(self, DrvrangelReq, DrvrfrontheighReq):
        """检查主驾 靠背 腿托的设置信号"""
        CemBodyFr74 = self.ipdu.bodycan.CemBodyFr74
        self.ipdu.check_multiple_signals([(CemBodyFr74, 'BackRestAdjmtRowFirstDrvr', DrvrangelReq),
                                          (CemBodyFr74, 'SeatCushTiltAdjmtRowFirstDrvr', DrvrfrontheighReq)], timeout=1)
        
    def check_Passseat_heightsld_adjust(self, DrvrLenthReq, DrvrheighReq):
        """检查副驾前后 高度 的设置信号"""
        CemBodyFr74 = self.ipdu.bodycan.CemBodyFr74
        self.ipdu.check_multiple_signals([(CemBodyFr74, 'SeatLenAdjmtRowFirstPass', DrvrLenthReq),
                                          (CemBodyFr74, 'SeatHeiAdjmtRowFirstPass', DrvrheighReq)], timeout=1)
        
    def check_Passseat_kaotuituo_adjust(self, DrvrangelReq, DrvrfrontheighReq):
        """检查副驾 靠背 腿托的设置信号"""
        CemBodyFr74 = self.ipdu.bodycan.CemBodyFr74
        self.ipdu.check_multiple_signals([(CemBodyFr74, 'BackRestAdjmtRowFirstPass', DrvrangelReq),
                                          (CemBodyFr74, 'SeatCushTiltAdjmtRowFirstPass', DrvrfrontheighReq)], timeout=1)
        
    def Shift_Gear(self, X):
        """0代表P挡 2代表N挡 3代表D挡 1代表R挡"""
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', X)
        sleep(1)
        
    def set_four_seat_occupt(self,A,B,C,D):
        """设置副驾 左后 后中 后右 1/2代表占位 0 代表未占位"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts', A)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe', B)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecMid', C)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecRi', D)
        sleep(0.5)

    #设置座椅占位，一次有且只有一个占位
    def set_four_seat_occupt_onlyone(self,seatid):
        if seatid == 0:
            self.io.driver_seat_present()
            self.set_four_seat_occupt(0,0,0,0)
        elif seatid == 1:
            self.io.driver_seat_notpresent()
            self.set_four_seat_occupt(1,0,0,0)
        elif seatid == 2:
            self.io.driver_seat_notpresent()
            self.set_four_seat_occupt(0,1,0,0)
        elif seatid == 3:
            self.io.driver_seat_notpresent()
            self.set_four_seat_occupt(0,0,1,0)
        else:
            self.io.driver_seat_notpresent()
            self.set_four_seat_occupt(0,0,0,1)
    
    
    def check_four_seatoccupt_event(self,X,Y,Z):
        """检查四个座椅占位：副驾 左后 后中 后右 X代表传感器状态(0,1,255) Y代表处理后的状态(0,1) Z代表信号是否丢失(4,0)"""
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatusValidity", {"infos": [{"value": {"seatId": 1, "rawSensorStatus": X, "status": Y}},{"statusValidity": Z},
                                                                                              {"value": {"seatId": 4, "rawSensorStatus": X, "status": Y}},{"statusValidity": Z},
                                                                                              {"value": {"seatId": 5, "rawSensorStatus": X, "status": Y}},{"statusValidity": Z},
                                                                                              {"value": {"seatId": 6, "rawSensorStatus": X, "status": Y}},{"statusValidity": Z}]})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatus", {"infos": [{"seatId": 1, "rawSensorStatus": X, "status": Y},
                                                                                      {"seatId": 4, "rawSensorStatus": X, "status": Y},
                                                                                      {"seatId": 5, "rawSensorStatus": X, "status": Y},
                                                                                      {"seatId": 6, "rawSensorStatus": X, "status": Y}]})
        
    def check_five_seatoccuptLoss_event(self,X,Y,Z):
        """检查四个座椅占位：副驾 左后 后中 后右 X代表传感器状态(0,1,255) Y代表处理后的状态(0,1) Z代表信号是否丢失(4,0)"""
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatusValidity", {"infos": [{"value": {"seatId": 0, "rawSensorStatus": X, "status": Y}},{"statusValidity": Z},
                                                                                              {"value": {"seatId": 1, "rawSensorStatus": X, "status": Y}},{"statusValidity": Z},
                                                                                              {"value": {"seatId": 4, "rawSensorStatus": X, "status": Y}},{"statusValidity": Z},
                                                                                              {"value": {"seatId": 5, "rawSensorStatus": X, "status": Y}},{"statusValidity": Z},
                                                                                              {"value": {"seatId": 6, "rawSensorStatus": X, "status": Y}},{"statusValidity": Z}]})

    
    def seat_NA_status(self,A,B,C,D,E):
        """设置五个座位是否为NA状态：主驾 副驾 左后 后中 后右 1代表NA  0代表不是NA"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', A)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts', B)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecLeBltLockSts', C)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecMidBltLockSts', D)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecRiBltLockSts', E)
        sleep(1)
    
    def check_All_seatOccupt_response(self,X,Y,Z):
        """使用GetOccupiedValidity和GetOccupied检查五个座位占位状态 X代表传感器状态(0,1,255) Y代表处理后的状态(0,1) Z代表信号是否丢失(4,0)"""
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetOccupiedValidity",
                                                {"seats": [12]},{"out": [{"value": {"seatId": 0, "rawSensorStatus": X, "status": Y}},{"statusValidity": Z},
                                                    {"value": {"seatId": 1, "rawSensorStatus": X, "status": Y}},{"statusValidity": Z},
                                                    {"value": {"seatId": 4, "rawSensorStatus": X, "status": Y}},{"statusValidity": Z},
                                                    {"value": {"seatId": 5, "rawSensorStatus": X, "status": Y}},{"statusValidity": Z},
                                                    {"value": {"seatId": 6, "rawSensorStatus": X, "status": Y}},{"statusValidity": Z}]})
        sleep(0.5)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetOccupied", {"seats": [12]},
                                                {"out": [{"seatId": 0, "rawSensorStatus": X, "status": Y},{"seatId": 1, "rawSensorStatus": X, "status": Y},
                                                        {"seatId": 4, "rawSensorStatus": X, "status": Y},{"seatId": 5, "rawSensorStatus": X, "status": Y},
                                                        {"seatId": 6, "rawSensorStatus": X, "status": Y}]})
    def check_DrvrSeatOccupt_event_response(self,X,Y,Z):
        """使用GetOccupiedValidity和GetOccupied和SeatOccupyStatusValidity和SeatOccupyStatus检查主驾
        座位占位状态 X代表传感器状态(0,1,255) Y代表处理后的状态(0,1) Z代表信号是否丢失(4,0)"""
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatusValidity", {"infos": [{"value": {"seatId": 0, "rawSensorStatus": X, "status": Y}},{"statusValidity": Z}]})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatus", {"infos": [{"seatId": 0, "rawSensorStatus": X, "status": Y}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetOccupied", {"seats": [0]},
                                              {"out": [{"seatId": 0, "rawSensorStatus": X, "status": Y}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetOccupiedValidity", {"seats": [0]},
                                              {"out": [{"value": {"seatId": 0, "rawSensorStatus": X, "status": Y}},{"statusValidity": Z}]})
    def check_DrvrSeatOccupt_event(self,X,Y,Z):
        """使用SeatOccupyStatusValidity和SeatOccupyStatus检查主驾座位占位状态 X代表传感器状态(0,1,255) Y代表处理后的状态(0,1) Z代表信号是否丢失(4,0)"""
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatusValidity", {"infos": [{"value": {"seatId": 0, "rawSensorStatus": X, "status": Y}},{"statusValidity": Z}]})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatus", {"infos": [{"seatId": 0, "rawSensorStatus": X, "status": Y}]})

    def set_second_selt_equip(self,X):
        """后排三个座椅装配情况：1代表装配，0代表未装配"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecLeBltLockEquid',
                      X)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockEquid', X)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecRiBltLockEquid', X)

    def set_vehicle_speed(self,X):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', X)
        sleep(1)
    
    def check_all_beltwarning(self,A):
        """检查所有座椅未系报警状态 1代表已系 2代表一级报警 3代表2级报警低 4代表2级报警高 5代表故障"""
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 0, "warn": A})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 1, "warn": A})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 4, "warn": A})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 5, "warn": A})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 6, "warn": A})
        
    def check_all_beltwarningValidity(self,A):
        """检查所有座椅未系报警状态 1代表已系 2代表一级报警 3代表2级报警低 4代表2级报警高 5代表故障"""
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 0, "warn":{"value":A}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 1, "warn":{"value":A}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 4, "warn":{"value":A}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 5, "warn":{"value":A}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 6, "warn":{"value":A}})

    def check_Wti_all_beltwarning_one_event(self):
        """通过 WarningMsgList TelltaleList 来表示所有安全带未系一级报警"""
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list": [{"name": "Driver Seat Belt Warning", "info": "1"}]})                                    
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list":[{"name": "Passenger Seat Belt Warning", "info": "1"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list":[{"name": "Second Row Middle Seat Belt Warning", "info": "1"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list":[{"name": "Second Row Right Seat Belt Warning", "info": "1"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list":[{"name": "Second Row Left Seat Belt Warning", "info": "1"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                                        {"list": [{"name":"Seat Belt", "state": "1"}]})
        
    def check_Wti_all_beltwarning_one_reponse(self):
        """通过GetWarningMsgList WarningMsgList 来表示所有安全带未系一级报警"""
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                        {"out": [{"name": "Driver Seat Belt Warning", "info": "1"},
                                                                 {"name": "Passenger Seat Belt Warning", "info": "1"},
                                                                 {"name": "Second Row Left Seat Belt Warning", "info": "1"},
                                                                 {"name": "Second Row Middle Seat Belt Warning", "info": "1"},
                                                                 {"name": "Second Row Right Seat Belt Warning", "info": "1"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                        {"out": [{"name":"Seat Belt", "state": "1"}]})
        
    def check_Wti_all_beltwarning_two_event(self):
        """通过 WarningMsgList TelltaleList 来表示所有安全带未系二级报警"""
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list": [{"name": "Driver Seat Belt Warning", "info": "2"}]})                                    
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list":[{"name": "Passenger Seat Belt Warning", "info": "2"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list":[{"name": "Second Row Middle Seat Belt Warning", "info": "2"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list":[{"name": "Second Row Right Seat Belt Warning", "info": "2"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list":[{"name": "Second Row Left Seat Belt Warning", "info": "2"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                                        {"list": [{"name":"Seat Belt", "state": "2"}]})
        
    def check_Wti_all_beltwarning_two_reponse(self):
        """通过GetWarningMsgList WarningMsgList 来表示所有安全带未系二级报警"""
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                        {"out": [{"name": "Driver Seat Belt Warning", "info": "2"},
                                                                 {"name": "Passenger Seat Belt Warning", "info": "2"},
                                                                 {"name": "Second Row Left Seat Belt Warning", "info": "2"},
                                                                 {"name": "Second Row Middle Seat Belt Warning", "info": "2"},
                                                                 {"name": "Second Row Right Seat Belt Warning", "info": "2"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                      {"out": [{"name":"Seat Belt", "state": "2"}]})  
    def check_Secondrow_seltwaring_one_event(self):
        """通过BeltWarning 和WarningMsgList 来表示后排安全带未系一级报警"""
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 4, "warn": 2})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 5, "warn": 2})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 6, "warn": 2})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                {"list":[{"name": "Second Row Middle Seat Belt Warning", "info": "1"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list":[{"name": "Second Row Right Seat Belt Warning", "info": "1"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list":[{"name": "Second Row Left Seat Belt Warning", "info": "1"}]})
        
    def check_All_seltwaring_fault_event(self):
        """通过BeltWarning 和WarningMsgList 来表示所有安全带故障报警"""
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 0, "warn": 5})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 1, "warn": 5})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 4, "warn": 5})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 5, "warn": 5})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 6, "warn": 5})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list": [{"name": "Driver Seat Belt Warning", "info": "4"}]})                                    
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list":[{"name": "Passenger Seat Belt Warning", "info": "4"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                {"list":[{"name": "Second Row Middle Seat Belt Warning", "info": "4"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list":[{"name": "Second Row Right Seat Belt Warning", "info": "4"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list":[{"name": "Second Row Left Seat Belt Warning", "info": "4"}]})
        
    def pass_position_stop(self):
        """通过StopMoveDirection 来停止之前未完成的动作"""
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StopMoveDirection',
                                                {"id": 1, "part": 1, "direction": 0})
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StopMoveDirection',
                                                {"id": 1, "part": 0, "direction": 0})
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StopMoveDirection',
                                                {"id": 1, "part": 1, "direction": 2})
    
    def set_four_Door_open(self):
        self.io.drvr_door_open()
        self.io.pass_door_open()
        self.io.lere_door_open()
        self.io.rire_door_open()
    
    #设置一次有且只有一个门开   
    def set_four_Door_open_onlyone(self,doorid):
        if doorid == 0:
            self.set_four_Door_close()
            self.io.drvr_door_open()
        elif doorid == 1:
            self.set_four_Door_close()
            self.io.pass_door_open()
        elif doorid == 2:
            self.set_four_Door_close()
            self.io.lere_door_open()
        elif doorid == 3:
            self.set_four_Door_close()
            self.io.rire_door_open()

    def set_four_Door_close(self):
        self.io.drvr_door_close()
        self.io.pass_door_close()
        self.io.lere_door_close()
        self.io.rire_door_close()

    def set_Drvrseat_condition_allow(self):
        """主驾可调的前提条件:车辆模式正常 车速为0 座椅可调 按键未按下"""
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.sd_tester.change_car_mode(0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatBtnPsd', 0)
        sleep(1)

    def set_Passseat_condition_allow(self):
        """副驾可调的前提条件:车辆模式正常 车速可设置为大于0 副驾按键未按下 """
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 10.0)
        self.sd_tester.change_car_mode(0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 0)
        sleep(1)

    def check_Drvrseat_direction_not_send(self,a=0,b=0,c=0,d=0):
        """四个主驾部位调节的指令都是0"""
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatHeiAdjmtRowFirstDrvr',a, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstDrvr',b, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'BackRestAdjmtRowFirstDrvr',c, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatCushTiltAdjmtRowFirstDrvr', d, timeout=0.5)
        
    def check_Passseat_direction_not_send(self,a=0,b=0,c=0,d=0):
        """四个副驾部位调节的指令都是0"""
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'BackRestAdjmtRowFirstPass', a, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatHeiAdjmtRowFirstPass',b, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstPass',c, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatCushTiltAdjmtRowFirstPass',d, timeout=0.5)
        
    #设置安全带状态 liugang
    def setDefaultSeatbeltStatus(self,seatId):
        if(seatId=="主驾"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts',0)
        elif(seatId=="副驾"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts',0)
        elif(seatId=="前排所有"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts',0)
        elif(seatId=="二排左侧"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecLeBltLockSt1',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecLeBltLockSts',0)
        elif(seatId=="二排中间"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSt1',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSts',0) 
        elif(seatId=="二排右侧"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecRiBltLockSt1',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecRiBltLockSts',0)
        elif(seatId=="二排所有"): 
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecLeBltLockSt1',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecLeBltLockSts',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSt1',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSts',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecRiBltLockSt1',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecRiBltLockSts',0)
        elif(seatId=="所有座椅"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecLeBltLockSt1',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecLeBltLockSts',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSt1',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSts',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecRiBltLockSt1',0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecRiBltLockSts',0)
        sleep(1)
            
    def setSeatbeltStatusValue(self,St1,Sts):
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1',St1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts',Sts)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1',St1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts',Sts)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecLeBltLockSt1',St1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecLeBltLockSts',Sts)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSt1',St1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSts',Sts)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecRiBltLockSt1',St1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecRiBltLockSts',Sts)
        sleep(1)  
    #设置主副驾座椅位置初始化
    def setDefaultSeatPosition(self):
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'SeatBackAngleRowFirstDrvr',0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF',0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF',0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF',0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiPerc',1000)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldPerc',1000)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiPerc',1000)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'SeatBackAngleRowFirstPass',0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiQF',0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldQF',0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiQF',0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiPerc',1000)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldPerc',1000)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiPerc',1000)
        sleep(1)
        
    #设置座椅安全带加热通风状态初始化
    def setSeatHeatVent(self,seatId,status):
        if seatId==("主驾"):
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgLvlSts',status)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentnLvlSts',status)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgAvlSts',status)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentAvlSts',status)   
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingTime",
                                                {"params": [{"id": 0, "uint64Info": 59}]},timeout = 0.5)
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingTime",
                                                    {"params": [{"id": 0, "uint64Info": 59}]},timeout = 0.5)
        elif seatId==("副驾"):
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgLvlSts',status)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentnLvlSts',status)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgAvlSts',status)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentAvlSts',status)
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingTime",
                                            {"params": [{"id": 1, "uint64Info": 59}]},timeout = 0.5)
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingTime",
                                             {"params": [{"id": 1, "uint64Info": 59}]},timeout = 0.5)
        elif seatId==("二排左侧"):
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecLe',status)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecLe',status)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecLe',status)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecLe',status)
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingTime",
                                            {"params": [{"id": 4, "uint64Info": 59}]},timeout = 0.5)
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingTime",
                                             {"params": [{"id": 4, "uint64Info": 59}]},timeout = 0.5)
        elif seatId==("二排右侧"):
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecRi',status)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecRi',status)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecRi',status)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecRi',status)
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingTime",
                                            {"params": [{"id": 6, "uint64Info": 59}]},timeout = 0.5)
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingTime",
                                             {"params": [{"id": 6, "uint64Info": 59}]},timeout = 0.5)
        sleep(1)
    
    #设置加热等级带请求源
    def setHeatLevelSource(self,ID0,ID1,ID4,ID6):
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                    {"params": [{"id": ID0[0], "uint8Info": ID0[1]}],"source":ID0[2]},timeout = 0.5)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                    {"params": [{"id": ID1[0], "uint8Info": ID1[1]}],"source":ID1[2]},timeout = 0.5)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                    {"params": [{"id": ID4[0], "uint8Info": ID4[1]}],"source":ID4[2]},timeout = 0.5)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                    {"params": [{"id": ID6[0], "uint8Info": ID6[1]}],"source":ID6[2]},timeout = 0.5)
        
    #设置通风等级带请求源
    def setVentLevelSource(self,ID0,ID1,ID4,ID6):
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                    {"params": [{"id": ID0[0], "uint8Info": ID0[1]}],"source":ID0[2]},timeout = 0.5)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                    {"params": [{"id": ID1[0], "uint8Info": ID1[1]}],"source":ID1[2]},timeout = 0.5)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                    {"params": [{"id": ID4[0], "uint8Info": ID4[1]}],"source":ID4[2]},timeout = 0.5)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                    {"params": [{"id": ID6[0], "uint8Info": ID6[1]}],"source":ID6[2]},timeout = 0.5)
        
    #设置座椅加热等级
    def setSeatHeatLevel(self,Drvr,Pass,SecLe,SecRi):
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgLvlSts',Drvr)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgLvlSts',Pass)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecLe',SecLe)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecRi',SecRi)
        sleep(0.5)
    
    #设置座椅通风等级   
    def setSeatVentLevel(self,Drvr,Pass,SecLe,SecRi):
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentnLvlSts',Drvr)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentnLvlSts',Pass)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecLe',SecLe)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecRi',SecRi)
        sleep(0.5)
        
    def SetPositionTargetThread(self,time):
        logger.info(f"线程开始")
        sleep(time)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatBtnPsd', 0)

        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 0)
        logger.info(f"线程结束")             
        
    def ckAllSeatbeltStatusNoEvent(self):
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts")
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntRightBeltSts")
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearLeftBeltSts")
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearMiddleBeltSts")
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearRightBeltSts")
        
    def ckAllSeatbeltStatusEvent(self,status):
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts", 
                                  {"status":{"value": status}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightBeltSts", 
                                  {"status":{"value": status}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftBeltSts",
                                  {"status":{"value": status}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearMiddleBeltSts",
                                  {"status":{"value": status}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightBeltSts", 
                                  {"status":{"value": status}})
    
    def ckAllSeatbeltStatusValue(self,value):
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                        {"out": [{"id": 0, "status": value},{"id": 1, "status": value},
                                                {"id": 4, "status": value},{"id": 5, "status": value},
                                                {"id": 6, "status": value}]},timeout = 0.5)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [12]},
                                            {"out": [{"value": {"id": 0, "status": value}},
                                                    {"value": {"id": 1, "status": value}},
                                                    {"value": {"id": 4, "status": value}},
                                                    {"value": {"id": 5, "status": value}},
                                                    {"value": {"id": 6, "status": value}}]},timeout = 0.5)
    #设置加热通风等级
    def setHeatVentingLevel(self,heatlevel,ventLevel):
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                    {"params": [{"id": 0, "uint8Info": heatlevel},
                                                                {"id": 1, "uint8Info": heatlevel},
                                                                {"id": 4, "uint8Info": heatlevel},
                                                                {"id": 6, "uint8Info": heatlevel}]},timeout = 0.5)
        # sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                    {"params": [{"id": 0, "uint8Info": ventLevel},
                                                                {"id": 1, "uint8Info": ventLevel},
                                                                {"id": 4, "uint8Info": ventLevel},
                                                                {"id": 6, "uint8Info": ventLevel}]},timeout = 0.5)
        
    #设置座椅加热通风状态
    def setHeatVentingStatus(self,heatStatus,ventStatus):
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgAvlSts',heatStatus)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentAvlSts',ventStatus) 
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgAvlSts',heatStatus)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentAvlSts',ventStatus)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecLe',heatStatus)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecLe',ventStatus)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecRi',heatStatus)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecRi',ventStatus)
    
    #获取二排左右占位情况，针对儿童座椅需求
    def get_occupied_sec(self,id,sts):
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetOccupied", {"seats": [id]},
                                              {"out": [{"seatId": id, "status": sts}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetOccupiedValidity", {"seats": [id]},
                                              {"out": [{"value": {"seatId": id, "status": sts}}]})
    #通知二排左右占位情况，针对儿童座椅需求
    def notify_occupied_sec(self,id,sts):
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatus", 
                                 {"infos": [{"seatId": id, "status": sts}]})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatusValidity", 
                                  {"infos": [{"value": {"seatId": id, "status": sts}}]})
        
    #设置主驾姿态调节启动场景2s条件
    def set_dri_position_condition(self,QF1,QF2,QF3,backAngleRow):
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF', QF1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF', QF2)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', QF3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'SeatBackAngleRowFirstDrvr', backAngleRow)
        sleep(0.5)
        
    #设置副姿态调节启动场景2s条件
    def set_pass_position_condition(self,QF1,QF2,QF3,backAngleRow):
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiQF', QF1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiQF', QF2)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldQF',QF3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'SeatBackAngleRowFirstPass',backAngleRow)
        sleep(0.5)
        
    #通知和获取主副驾座椅占位情况_带视觉  
    def ck_event_and_resp_SeatOccupyWithCam(self,id,statusWithCam):
        self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "SeatOccupyStatus",
                                        {"infos": [{"seatId": id, "statusWithCam": statusWithCam}]},
                                        "GetOccupied", {"seats": [12]}, timeout = 1)
        self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "SeatOccupyStatusValidity",
                                        {"infos": [{"value": {"seatId": id, "statusWithCam":statusWithCam}}]},
                                        "GetOccupiedValidity",{"seats": [12]},timeout = 1)
        
    #设置座椅无故障
    def set_no_seatFault(self):
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecLeBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecMidBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecRiBltLockSts', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldQF', 3)
        sleep(1)
    
    #设置安全带故障
    def set_seatBeltFault(self,driB,passB,seleB,semidB,seriB,ub_flage=True):
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05,'BltLockStAtDrvrBltLockSts', driB, ub_flag=ub_flage)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtPassBltLockSts', passB, ub_flag=ub_flage)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', seleB, ub_flag=ub_flage)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', semidB, ub_flag=ub_flage)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', seriB, ub_flag=ub_flage)
        sleep(0.5)
        
    #获取校验周期失败次数    
    def return_fail_period_time(self, signal_name: str, period, deviation=0.2):
        """
        用于周期性信号校验，但是考虑插帧场景，允许一定次数失败，返回失败次数
        @param signal_name: 信号名
        @param period: 期望周期, 单位s
        @param deviation: 默认±20%为可接受偏差
        @param permit_fail_times: 允许失败的次数，默认0次
        return: 失败次数
        """
        items = self.bgm_eth_inter.get_signal_items(signal_name)
        fail_timestamps = []
        last_time = None
        for item in items:
            if last_time is None:
                last_time = item[1]
            else:
                if abs(float(item[1]) - float(last_time) - period) / period > deviation:
                    fail_timestamps.append(item[1])
                last_time = item[1]
        logger.info(f"周期校验失败时间戳fail_timestamps=={fail_timestamps}")
        return len(fail_timestamps)
    
    @allure.title("设置座椅通风加热时间_下行PDU校验")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1698204?projectId=46')
    @pytest.mark.full
    @pytest.mark.period
    #调用set接口会下发一帧，导致校验周期非预期
    def test_caseid_1939959(self):
        info1 =['HmiSeatClimaTmrHmiSeatHeatgFirstLeTmr', 'HmiSeatClimaTmrHmiSeatHeatgFirstRiTmr',
                'HmiSeatClimaTmrHmiSeatHeatgSecLeTmr', 'HmiSeatClimaTmrHmiSeatHeatgSecRiTmr']
        info2 =['HmiSeatClimaTmrHmiSeatVentnFirstLeTmr', 'HmiSeatClimaTmrHmiSeatVentnFirstRiTmr',
                'HmiSeatClimaTmrHmiSeatVentnSecLeTmr', 'HmiSeatClimaTmrHmiSeatVentnSecRiTmr']
        self.partner.empty_all(0.5)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingTime",
                                             {"params": [{"id": 0, "uint64Info": 30},{"id": 1, "uint64Info": 30},
                                                         {"id": 4, "uint64Info": 30},{"id": 6, "uint64Info": 30}]})
        self.ipdu.check_multiple_signals(
                                [(self.ipdu.bodycan.CemBodyFr09, info1[0], 30),
                                (self.ipdu.bodycan.CemBodyFr09, info1[1], 30),
                                (self.ipdu.bodycan.CemBodyFr09, info1[2], 30),
                                (self.ipdu.bodycan.CemBodyFr09, info1[3], 30)], timeout=0.5)
        sleep(0.5)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingTime",
                                             {"params": [{"id": 0, "uint64Info": 30},{"id": 1, "uint64Info": 30},
                                                         {"id": 4, "uint64Info": 30},{"id": 6, "uint64Info": 30}]})
        self.ipdu.check_multiple_signals(
                                [(self.ipdu.bodycan.CemBodyFr09, info2[0], 30),
                                (self.ipdu.bodycan.CemBodyFr09, info2[1], 30),
                                (self.ipdu.bodycan.CemBodyFr09, info2[2], 30),
                                (self.ipdu.bodycan.CemBodyFr09, info2[3], 30)], timeout=0.5)
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingTime",
                                             {"params": [{"id": 0, "uint64Info": 20},{"id": 1, "uint64Info": 20},
                                                         {"id": 4, "uint64Info": 20},{"id": 6, "uint64Info": 20}]})
        self.ipdu.check_multiple_signals(
                                [(self.ipdu.bodycan.CemBodyFr09, info1[0], 20),
                                (self.ipdu.bodycan.CemBodyFr09, info1[1], 20),
                                (self.ipdu.bodycan.CemBodyFr09, info1[2], 20),
                                (self.ipdu.bodycan.CemBodyFr09, info1[3], 20)], timeout=0.5)
        sleep(0.5)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingTime",
                                             {"params": [{"id": 0, "uint64Info": 20},{"id": 1, "uint64Info": 20},
                                                         {"id": 4, "uint64Info": 20},{"id": 6, "uint64Info": 20}]})
        self.ipdu.check_multiple_signals(
                                [(self.ipdu.bodycan.CemBodyFr09, info2[0], 20),
                                (self.ipdu.bodycan.CemBodyFr09, info2[1], 20),
                                (self.ipdu.bodycan.CemBodyFr09, info2[2], 20),
                                (self.ipdu.bodycan.CemBodyFr09, info2[3], 20)], timeout=0.5)
        
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaTmrIdPen",[0])
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr09, 'HmiSeatClimaTmrIdPen', 0, timeout=0.5)
        for i in range(4):
            self.bgm_eth_inter.ck_ordered_array(info1[i], [30,20])
            self.bgm_eth_inter.ck_ordered_array(info2[i], [30,20])
            assert self.return_fail_period_time(info1[i],period = 0.5) >= 16
            assert self.return_fail_period_time(info2[i],period = 0.5) >= 16
        #校验周期，规避插帧影响
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        for i in range(4):
            self.bgm_eth_inter.ck_period_time(info1[i],period=0.5)
            self.bgm_eth_inter.ck_period_time(info2[i],period=0.5)
        
    @allure.title("远程座椅加热_下行PDU校验打断")
    @pytest.mark.full
    def test_caseid_1939949(self): 
        info =['TelmSeatDrvHeatClimaLvlSP', 'TelmSeatPassHeatClimaLvlSP',
        'TelmSeatSecLeHeatClimaLvl', 'TelmSeatSecRiHeatClimaLvl']
        self.bgm_eth_inter.start_bgm_tcpdump()
        for ID in [0, 1, 4, 6]:
            for level in [1,2]:
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingLevel",
                                             {"params": [{"id": ID, "uint8Info": level}]})
                sleep(1)
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        for i in range(4):
            self.bgm_eth_inter.ck_signal_values(info[i], [1, 1, 1, 1, 1, 2, 2, 2, 2, 2])   
                 
    @allure.title("远程座椅加热_下行PDU校验设置加热为0时不能打断通风&相同信号值的处理")
    @pytest.mark.full
    def test_caseid_1980503(self):
        info = ["TelmSeatDrvVentnClimaLvl", "TelmSeatPassVentnClimaLvl", "TelmSeatSecLeVentnClimaLvl", "TelmSeatSecRiVentnClimaLvl"]
        for ID in [0, 1, 4, 6]:
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingLevel",
                                                {"params": [{"id": ID, "uint8Info": 1}]})
        for ID in [0, 1, 4, 6]:#100ms内调用两次
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingLevel",
                                                {"params": [{"id": ID, "uint8Info": 1}]})
        self.bgm_eth_inter.start_bgm_tcpdump()
        for ID in [0, 1, 4, 6]:
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingLevel",
                                                {"params": [{"id": ID, "uint8Info": 1}]})
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingLevel",
                                                {"params": [{"id": ID, "uint8Info": 0}]})
            sleep(1)  
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        for i in range(4):
            self.bgm_eth_inter.ck_ordered_array(info[i], [1])
            assert (self.bgm_eth_inter.get_signal_values(info[i])).count(1) == 5
        
    @allure.title("远程座椅通风_下行PDU校验设置通风为0时不能打断加热&相同信号值的处理")
    @pytest.mark.full
    def test_caseid_1980537(self):
        info =['TelmSeatDrvHeatClimaLvlSP', 'TelmSeatPassHeatClimaLvlSP',
        'TelmSeatSecLeHeatClimaLvl', 'TelmSeatSecRiHeatClimaLvl']
        for ID in [0, 1, 4, 6]:
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingLevel",
                                                {"params": [{"id": ID, "uint8Info": 1}]})
        for ID in [0, 1, 4, 6]:#100ms内调用两次
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingLevel",
                                                {"params": [{"id": ID, "uint8Info": 1}]})
        self.bgm_eth_inter.start_bgm_tcpdump()
        for ID in [0, 1, 4, 6]:
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingLevel",
                                                {"params": [{"id": ID, "uint8Info": 1}]})
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingLevel",
                                                {"params": [{"id": ID, "uint8Info": 0}]})
            sleep(1)
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        for i in range(4):
            self.bgm_eth_inter.ck_ordered_array(info[i], [1])
            assert (self.bgm_eth_inter.get_signal_values(info[i])).count(1) == 5

    @allure.title("远程座椅通风_下行PDU校验打断")
    @pytest.mark.smoke
    def test_caseid_1903501(self):
        info = ["TelmSeatDrvVentnClimaLvl", "TelmSeatPassVentnClimaLvl", "TelmSeatSecLeVentnClimaLvl", "TelmSeatSecRiVentnClimaLvl"]
        self.bgm_eth_inter.start_bgm_tcpdump()
        for ID in [0, 1, 4, 6]:
            for level in [1,2]:
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingLevel",
                                             {"params": [{"id": ID, "uint8Info": level}]})
                sleep(1)
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        for i in range(4):
            self.bgm_eth_inter.ck_signal_values(info[i], [1, 1, 1, 1, 1, 2, 2, 2, 2, 2])        

    @allure.title("主驾座椅姿态设置_下行PDU校验")
    @pytest.mark.sanity
    @pytest.mark.period
    def test_caseid_1919348(self):
        info = ["BackRestAdjmtRowFirstDrvr", "SeatHeiAdjmtRowFirstDrvr", "SeatLenAdjmtRowFirstDrvr", "SeatCushTiltAdjmtRowFirstDrvr"]
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatBtnPsd', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'SeatBackAngleRowFirstDrvr', 20)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiPerc',500)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldPerc', 100)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiPerc', 300)
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.empty_all(0.5)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                              {"params": {"id": 0,
                                                          "position": {"backAngle": 10, "longitudinalPosition": 100,
                                                                       "verticalPosition": 20,
                                                                       "LegrestVerticalPosition": 20,
                                                                       "backAngleIsValid": True,
                                                                       "longitudinalIsValid": True,
                                                                       "verticalIsValid": True,
                                                                       "legrestVerticalIsValid": True}}},
                                              {"out": 1})
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array(info[0], [0])
        self.bgm_eth_inter.ck_ordered_array(info[1], [0,2])
        self.bgm_eth_inter.ck_ordered_array(info[2], [0,1])
        self.bgm_eth_inter.ck_ordered_array(info[3], [0])
        for i in range(4):
            assert self.return_fail_period_time(info[i],period = 0.16) >= 1
        #校验周期，规避插帧影响
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        for i in range(4):
            self.bgm_eth_inter.ck_period_time(info[i],period=0.16)
            
    # @allure.title("主驾座椅姿态设置_下行PDU校验_启动场景2s内信号恢复_使用信号值进行控制")
    # @pytest.mark.full
    # def test_caseid_1986141(self):
    #     info = ["BackRestAdjmtRowFirstDrvr", "SeatHeiAdjmtRowFirstDrvr", "SeatLenAdjmtRowFirstDrvr", "SeatCushTiltAdjmtRowFirstDrvr"]
    #     #前置条件
    #     self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatBtnPsd', 0)
    #     self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 1)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
    
    #     #调节主驾位置 
    #     self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', 3)
    #     self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldPerc', 100)
    #     self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF', 3)
    #     self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiPerc', 300)
        
    #     self.ipdu.pause_bus_send("bodycan")
    #     self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT, resume_all_bus=False)
    #     self.bgm_eth_inter.start_bgm_tcpdump()
    #     #重启2s内恢复总线信号
    #     self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', 3)
    #     self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
    #                                           {"params": {"id": 0,
    #                                                       "position": {"backAngle": 10, "longitudinalPosition": 100,
    #                                                                    "verticalPosition": 20,
    #                                                                    "LegrestVerticalPosition": 20,
    #                                                                    "backAngleIsValid": True,
    #                                                                    "longitudinalIsValid": True,
    #                                                                    "verticalIsValid": True,
    #                                                                    "legrestVerticalIsValid": True}}},
    #                                           {"out": 1})
        
    #     sleep(3)
    #     self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
    #     self.bgm_eth_inter.ck_ordered_array(info[0], [0])
    #     self.bgm_eth_inter.ck_ordered_array(info[1], [0,2])
    #     self.bgm_eth_inter.ck_ordered_array(info[2], [0,1])
    #     self.bgm_eth_inter.ck_ordered_array(info[3], [0])
        
    @allure.title("副驾座椅姿态设置_下行PDU校验")
    @pytest.mark.sanity
    @pytest.mark.period
    def test_caseid_1919349(self):
        info = ["BackRestAdjmtRowFirstPass", "SeatHeiAdjmtRowFirstPass", "SeatLenAdjmtRowFirstPass", "SeatCushTiltAdjmtRowFirstPass"]
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 0)
        self.set_pass_angelperc(20.0)
        self.set_pass_heiperc(20.0)
        self.set_pass_heipercValid(3)
        self.set_pass_sldperc(20.0)
        self.set_pass_sldpercValid(3)
        self.set_pass_frontheiperc(20.0)
        self.set_pass_frontheipercValid(3)
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.empty_all(0.5)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                              {"params": {"id": 1,
                                                          "position": {"backAngle": 30, "longitudinalPosition": 100,
                                                                       "verticalPosition": 40,
                                                                       "LegrestVerticalPosition": 50,
                                                                       "backAngleIsValid": True,
                                                                       "longitudinalIsValid": True,
                                                                       "verticalIsValid": True,
                                                                       "legrestVerticalIsValid": True}}},
                                              {"out": 1})
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array(info[0], [0])
        self.bgm_eth_inter.ck_ordered_array(info[1], [0,1])
        self.bgm_eth_inter.ck_ordered_array(info[2], [0,1])
        self.bgm_eth_inter.ck_ordered_array(info[3], [0])
        for i in range(4):
            assert self.return_fail_period_time(info[i],period = 0.16) >= 1
        #校验周期，规避插帧影响
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        for i in range(4):
            self.bgm_eth_inter.ck_period_time(info[i],period=0.16) 
            
    # @allure.title("副驾座椅姿态设置_下行PDU校验_启动场景2s内信号恢复_使用信号值进行控制")
    # @pytest.mark.full
    # def test_caseid_1986143(self):
    #     info = ["BackRestAdjmtRowFirstPass", "SeatHeiAdjmtRowFirstPass", "SeatLenAdjmtRowFirstPass", "SeatCushTiltAdjmtRowFirstPass"]
    #     self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 0)
    #     self.set_pass_heiperc(20.0)
    #     self.set_pass_heipercValid(3)
    #     self.set_pass_sldperc(20.0)
    #     self.set_pass_sldpercValid(3)
    #     sleep(1)
    #     self.ipdu.pause_bus_send("bodycan")
    #     self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT, resume_all_bus=False)
  
    #     self.bgm_eth_inter.start_bgm_tcpdump()
    #     self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 0)
    #     self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiPerc',  0)
        
    #     self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
    #                                           {"params": {"id": 1,
    #                                                       "position": {"backAngle": 30, "longitudinalPosition": 100,
    #                                                                    "verticalPosition": 40,
    #                                                                    "LegrestVerticalPosition": 50,
    #                                                                    "backAngleIsValid": True,
    #                                                                    "longitudinalIsValid": True,
    #                                                                    "verticalIsValid": True,
    #                                                                    "legrestVerticalIsValid": True}}},
    #                                           {"out": 1})
    #     sleep(3)
    #     self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
    #     self.bgm_eth_inter.ck_ordered_array(info[0], [0])
    #     self.bgm_eth_inter.ck_ordered_array(info[1], [0,1])
    #     self.bgm_eth_inter.ck_ordered_array(info[2], [0,1])
    #     self.bgm_eth_inter.ck_ordered_array(info[3], [0])
        
    # @allure.title("副驾座椅姿态设置_下行PDU校验_启动场景2s内信号未恢复_使用默认值进行控制")
    # @pytest.mark.full
    # def test_caseid_1986146(self):
    #     info = ["BackRestAdjmtRowFirstPass", "SeatHeiAdjmtRowFirstPass", "SeatLenAdjmtRowFirstPass", "SeatCushTiltAdjmtRowFirstPass"]
    #     self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 0)
    #     self.set_pass_angelperc(20.0)
    #     self.set_pass_heiperc(20.0)
    #     self.set_pass_heipercValid(3)
    #     self.set_pass_sldperc(20.0)
    #     self.set_pass_sldpercValid(3)
    #     self.set_pass_frontheiperc(20.0)
    #     self.set_pass_frontheipercValid(3)
    #     sleep(1)
    #     self.ipdu.pause_bus_send("bodycan")
    #     self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT, resume_all_bus=False)
    #     self.bgm_eth_inter.start_bgm_tcpdump()
    #     self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
    #                                           {"params": {"id": 1,
    #                                                       "position": {"backAngle": 30, "longitudinalPosition": 100,
    #                                                                    "verticalPosition": 5,
    #                                                                    "LegrestVerticalPosition": 50,
    #                                                                    "backAngleIsValid": True,
    #                                                                    "longitudinalIsValid": True,
    #                                                                    "verticalIsValid": True,
    #                                                                    "legrestVerticalIsValid": True}}},
    #                                           {"out": 1})
    #     sleep(3)
    #     self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
    #     self.bgm_eth_inter.ck_ordered_array(info[0], [0])
    #     self.bgm_eth_inter.ck_ordered_array(info[1], [0,1])
    #     self.bgm_eth_inter.ck_ordered_array(info[2], [0,2])
    #     self.bgm_eth_inter.ck_ordered_array(info[3], [0])
    #     self.ipdu.resume_all_bus_send()
      
    @allure.title("设置主副驾座椅按摩_按摩结束主动发0")
    @pytest.mark.full
    def test_caseid_1919416(self):
        info1 = ["DrvrSeatDispMassgFctOnOff", "DrvrSeatDispMassgFctMassgProg", "DrvrSeatDispMassgFctMassgInten"]
        info2 = ["PassSeatDispMassgFctOnOff", "PassSeatDispMassgFctMassgProg", "PassSeatDispMassgFctMassgInten"]
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrMassgRunng', 1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassMassgRunng', 1)
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetMassageConf",
                                         {"params": [{"id": 0, "conf": {"isOn": True, "type": 1, "intensity": 1}},
                                                     {"id": 1, "conf": {"isOn": True, "type": 2, "intensity": 0}}]})
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrMassgRunng', 0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassMassgRunng', 0)
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array(info1[0], [0])
        self.bgm_eth_inter.ck_ordered_array(info2[0], [0])
        self.bgm_eth_inter.ck_ordered_array(info1[1], [1])
        self.bgm_eth_inter.ck_ordered_array(info2[1], [2])
        self.bgm_eth_inter.ck_ordered_array(info1[2], [1])
        self.bgm_eth_inter.ck_ordered_array(info2[2], [0])
        #校验周期，规避插帧影响
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        for i in range(3):
            self.bgm_eth_inter.ck_period_time(info1[i],period=0.2)
            self.bgm_eth_inter.ck_period_time(info2[i],period=0.2)
        
    @allure.title("获取和通知安全带预紧故障报警")
    @pytest.mark.smoke
    def test_caseid_1892798(self):
        self.ipdu.set(self.ipdu.passivesafetycan.RmlPassSafeCANFrame1, 'MsgReqForRtrctrRvsbLe', 1)
        self.partner.empty_all(0.5) #7台架未接passivecan
        for X in [0,1]:
            self.ipdu.set(self.ipdu.passivesafetycan.RmlPassSafeCANFrame1, 'MsgReqForRtrctrRvsbLe', X)
            sleep(0.5)
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltPretensioningWarning", {"warn": X})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltPretensioningWarning",{},
                                                {"out": X})
        
    @allure.title("设置主驾安全带震动_下行PDU校验")
    @pytest.mark.sanity
    def test_caseid_1903499(self):
        # todo 开始抓包
        file_path, save_name = self.bgm_tcpdump.start_bgm_tcpdump()
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetDriverBeltVibration',
                                         {"duration": 3})
        self.ipdu.check(self.ipdu.passivesafetycan.DmmPassSafeCANFr02, 'DrvrPfmncAlrmReq', 5, timeout=0.5)
        sleep(5)
        # # todo 停止抓包
        self.bgm_tcpdump.stop_bgm_tcpdump()
        # todo 拉取日志 单个日志 不打包
        file_path = self.bgm_tcpdump.scp_bgm_log_to_local(bgm_log_name=save_name)
        # todo 删除所有 pcap 文件
        self.bgm_tcpdump.delete_bgm_tcpdump_file(bgm_log_name='*.pcap')
        data_list = [(30004, 1, 2, 3)]
        #先发5再隔duration=3秒后发送2
        res_dict = get_pdu_value_and_time(data_list, file_path)
        assert res_dict[data_list[0]][0][1] == 5
        assert res_dict[data_list[0]][1][1] == 2
        self.ipdu.check(self.ipdu.passivesafetycan.DmmPassSafeCANFr02, 'DrvrPfmncAlrmReq', 2, timeout=0.5)
        durationtime = res_dict[data_list[0]][1][2]- res_dict[data_list[0]][0][2]
        if abs(durationtime-3) < 0.1:
            pass
        else:
            assert(1 == 0)
            logger.info(f"durationtime=={durationtime}")
        logger.info(f"{res_dict}")

    @allure.title("座椅调节_下行PDU校验_主驾座椅高度/前后调节")
    @pytest.mark.sanity
    def test_caseid_1903500(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01,'DrvrSeatBtnPsd','Boolean_FALSE')
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 'Boolean_TRUE')
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 0, "part": 0, "direction": 3}, timeout=0.2)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 0, "part": 0, "direction": 2}, timeout=0.2)
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SeatLenAdjmtRowFirstDrvr", [0,2])
        self.bgm_eth_inter.ck_signal_values("SeatCushTiltAdjmtRowFirstDrvr", [0])
        self.bgm_eth_inter.ck_signal_values("SeatHeiAdjmtRowFirstDrvr", [0,1])
        self.bgm_eth_inter.ck_signal_values("BackRestAdjmtRowFirstDrvr", [0])
        #校验周期，规避插帧影响
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time("SeatHeiAdjmtRowFirstDrvr",period=0.16)
        self.bgm_eth_inter.ck_period_time("SeatLenAdjmtRowFirstDrvr",period=0.16)
        
    @allure.title("座椅调节_下行PDU校验_副驾座椅高度/前后调节")
    @pytest.mark.full
    def test_caseid_1984870(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 0)
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 1, "part": 0, "direction": 2}, timeout=0.2)
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 1, "part": 0, "direction": 3}, timeout=0.2)
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SeatHeiAdjmtRowFirstPass", [0,1])
        self.bgm_eth_inter.ck_signal_values("BackRestAdjmtRowFirstPass", [0])
        self.bgm_eth_inter.ck_signal_values("SeatLenAdjmtRowFirstPass", [0,2])
        self.bgm_eth_inter.ck_signal_values("SeatCushTiltAdjmtRowFirstPass", [0])
        #校验周期，规避插帧影响
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time("SeatHeiAdjmtRowFirstPass",period=0.16)
        self.bgm_eth_inter.ck_period_time("SeatLenAdjmtRowFirstPass",period=0.16)
        
    @allure.title("座椅调节_下行PDU校验_主驾座椅靠背调节")
    @pytest.mark.smoke
    def test_caseid_1984871(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01,'DrvrSeatBtnPsd','Boolean_FALSE')
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 'Boolean_TRUE')
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 0, "part": 1, "direction": 0}, timeout=0.2)
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 0, "part": 1, "direction": 3}, timeout=0.2)
        
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SeatHeiAdjmtRowFirstDrvr", [0,0])
        self.bgm_eth_inter.ck_signal_values("BackRestAdjmtRowFirstDrvr", [0,1,0,2])
        #校验周期，规避插帧影响
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time("BackRestAdjmtRowFirstDrvr",period=0.16)
    
    @allure.title("座椅调节_下行PDU校验_副驾座椅靠背调节")
    @pytest.mark.full
    def test_caseid_1984872(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 0)
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 1, "part": 1, "direction": 0}, timeout=0.2)
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 1, "part": 1, "direction": 3}, timeout=0.2)
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SeatHeiAdjmtRowFirstPass", [0,0])
        self.bgm_eth_inter.ck_signal_values("BackRestAdjmtRowFirstPass", [0,1,0,2])
        #校验周期，规避插帧影响
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time("BackRestAdjmtRowFirstPass",period=0.16)
        
    @allure.title("座椅调节_下行PDU校验_主驾座椅坐垫（腿托）调节")
    @pytest.mark.smoke
    def test_caseid_1984873(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01,'DrvrSeatBtnPsd','Boolean_FALSE')
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 'Boolean_TRUE')
        sleep(1)

        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 0, "part": 2, "direction": 2}, timeout=0.2)
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 0, "part": 2, "direction": 5}, timeout=0.2)
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SeatLenAdjmtRowFirstDrvr", [0,0])
        self.bgm_eth_inter.ck_signal_values("SeatCushTiltAdjmtRowFirstDrvr", [0,1,0,2])
        #校验周期，规避插帧影响
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time("SeatCushTiltAdjmtRowFirstDrvr",period=0.16)
        
    @allure.title("座椅调节_下行PDU校验_主驾座椅腰托调节")
    @pytest.mark.smoke
    def test_caseid_1984874(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01,'DrvrSeatBtnPsd','Boolean_FALSE')
        sleep(1)

        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                    {"id": 0, "part": 3, "direction": 2}, timeout=0.2)
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                    {"id": 0, "part": 3, "direction": 3}, timeout=0.2)
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("LumHeiAdjmtRowFirstDrvr", [0,1,0])
        self.bgm_eth_inter.ck_signal_values("LumLenAdjmtRowFirstDrvr", [0,0,2])
        #校验周期，规避插帧影响
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time("LumHeiAdjmtRowFirstDrvr",period=0.7)
        self.bgm_eth_inter.ck_period_time("LumLenAdjmtRowFirstDrvr",period=0.7)
        
    @allure.title("座椅调节_下行PDU校验_副驾座椅腰托调节")
    @pytest.mark.full
    def test_caseid_1984875(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 0)
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                    {"id": 1, "part": 3, "direction": 2}, timeout=0.2)
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                    {"id": 1, "part": 3, "direction": 3}, timeout=0.2)
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        self.bgm_eth_inter.ck_signal_values("LumHeiAdjmtRowFirstPass", [0,1,0])
        self.bgm_eth_inter.ck_signal_values("LumLenAdjmtRowFirstPass", [0,0,2])
        #校验周期，规避插帧影响
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time("LumHeiAdjmtRowFirstPass",period=0.7)
        self.bgm_eth_inter.ck_period_time("LumLenAdjmtRowFirstPass",period=0.7)

    @allure.title("座椅调节_无总线通讯时_下行PDU校验主驾都是0")
    @pytest.mark.sanity
    def test_caseid_1980567(self):
        info1 = ["SeatHeiAdjmtRowFirstDrvr", "SeatLenAdjmtRowFirstDrvr", "BackRestAdjmtRowFirstDrvr", "SeatCushTiltAdjmtRowFirstDrvr"]
        info2 = ["LumHeiAdjmtRowFirstDrvr", "LumLenAdjmtRowFirstDrvr"]
        #SOA-28654  偏差接受
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01,'DrvrSeatBtnPsd',0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 1)
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01,'DrvrSeatBtnPsd',1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 0)
        sleep(2)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 0, "part": 0, "direction": 3}, timeout=0.2)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 0, "part": 0, "direction": 2}, timeout=0.2)
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 0, "part": 1, "direction": 0}, timeout=0.2)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 0, "part": 1, "direction": 3}, timeout=0.2)
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 0, "part": 2, "direction": 2}, timeout=0.2)
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 0, "part": 3, "direction": 2}, timeout=0.2)
        #副驾
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 1, "part": 1, "direction": 0}, timeout=0.2)
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 1, "part": 1, "direction": 3}, timeout=0.2)
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SeatHeiAdjmtRowFirstPass", [0,0])
        self.bgm_eth_inter.ck_signal_values("BackRestAdjmtRowFirstPass", [0,1,0,2])
        for i in range(len(info1)):
            self.bgm_eth_inter.ck_signal_values(info1[i], [0])
        #SOA-28344 偏差接受  
        for i in range(len(info2)):
            self.bgm_eth_inter.ck_ordered_array(info2[i], [0])
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01,'DrvrSeatBtnPsd',0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 1)
        
    @pytest.mark.sanity
    @allure.title("设置主驾安全带震动_返回failed和success")
    def test_caseid_1919340(self):
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetDriverBeltVibration",
                                              {"duration": 9}, {"out": 1})
        sleep(1)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetDriverBeltVibration",
                                              {"duration": 3}, {"out": 0})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetDriverBeltVibration",
                                              {"duration": 4}, {"out": 1})
        sleep(3)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetDriverBeltVibration",
                                              {"duration": 2}, {"out": 0})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetDriverBeltVibration",
                                              {"duration": 2}, {"out": 1})
        
    @allure.title("座椅调节_无总线通讯时_下行PDU校验副驾都是0")
    #需要抓包看
    @pytest.mark.sanity
    def test_caseid_1984905(self):
        info2 = ["SeatHeiAdjmtRowFirstPass", "SeatLenAdjmtRowFirstPass", "BackRestAdjmtRowFirstPass", "LumHeiAdjmtRowFirstPass",
                 "LumLenAdjmtRowFirstPass"]
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01,'DrvrSeatBtnPsd',0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd',  1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 1, "part": 0, "direction": 2}, timeout=0.2)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 1, "part": 0, "direction": 3}, timeout=0.2)
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 1, "part": 1, "direction": 0}, timeout=0.2)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 1, "part": 1, "direction": 3}, timeout=0.2)
        sleep(1)
        #主驾
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 0, "part": 0, "direction": 3}, timeout=0.2)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                         {"id": 0, "part": 0, "direction": 2}, timeout=0.2)
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SeatLenAdjmtRowFirstDrvr", [0,2])
        for i in range(len(info2)):
            self.bgm_eth_inter.ck_ordered_array(info2[i], [0])

        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 0) 
             
    @allure.title("遍历_获取和通知座椅系统状态")
    @pytest.mark.smoke
    def test_caseid_1939968(self):
        info = {1: True, 0: False}
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetMassageConf",
                                         {"params": [{"id": 0, "conf": {"isOn": True, "type": 2, "intensity": 3}},
                                                     {"id": 1, "conf": {"isOn": True, "type": 2, "intensity": 3}}]})
        for key, value in info.items():
            logger.info(f"---请求{key}----反馈{value}----")
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd',key)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatInAutMovmt',key)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrMassgRunng',key)
            sleep(1)
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT,"SeatSysStatus", {"id": 0, "status": {"isExtAdjAllowed": value,"isAutoModeOn": value,
                                                            "isMassageRunning": value, "massageType": 2, "massageIntensity": 3}})
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatInAutMovmt',key)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassMassgRunng',key)
            sleep(1)
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT,"SeatSysStatus", {"id": 1, "status": {"isExtAdjAllowed": False,"isAutoModeOn": value,
                                                            "isMassageRunning": value, "massageType": 2, "massageIntensity": 3}})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatSysStatus", {"seats": [12]},
                                                    {"out": [{"id": 0, "status": {"isExtAdjAllowed": value,"isAutoModeOn": value,
                                                            "isMassageRunning": value, "massageType": 2, "massageIntensity": 3}},
                                                            {"id": 1, "status": {"isExtAdjAllowed": False,"isAutoModeOn": value,
                                                            "isMassageRunning": value, "massageType": 2, "massageIntensity": 3}}]})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatSysStatus", {"seats": [3]},
                                                    {"out": [{"id": 0, "status": {"isExtAdjAllowed": value,"isAutoModeOn": value,
                                                            "isMassageRunning": value, "massageType": 2, "massageIntensity": 3}},
                                                            {"id": 1, "status": {"isExtAdjAllowed": False,"isAutoModeOn": value,
                                                            "isMassageRunning": value, "massageType": 2, "massageIntensity": 3}}]})      
        
    @allure.title("遍历_获取和通知座椅开关按键状态")
    @pytest.mark.smoke
    def test_caseid_1919388(self):
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatBtnPsd', 0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatBtnPsd', 1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatSwitchStatus",
                                  {"id": 0, "status": {"isLocalSwitchActivated": True}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatSwitchStatus",
                                  {"id": 1, "status": {"isLocalSwitchActivated": True}})
        list1 = {'DrvrSeatSwtStsDrvrSeatSwtHeiSts': "verticalPositionSwitch",
                 'DrvrSeatSwtStsDrvrSeatSwtHeiFrntSts': "legrestVerticalPositionSwitch",
                 'DrvrSeatSwtStsDrvrSeatSwtSldSts': "longitudinalPositionSwitch",
                 'DrvrSeatSwtStsDrvrSeatSwtInclSts': "backSwitch",
                'DrvrSeatSwtStsDrvrSeatSwtAdjmtOfSpplFctHozlSts': "lumbarLongitudinalPositionSwitch",
                 'DrvrSeatSwtStsDrvrSeatSwtAdjmtOfSpplFctVertSts': "lumbarVerticalPositionSwitch"}
        list2 = {'PassSeatSwtSts2PassSeatSwtHeiSts': "verticalPositionSwitch",
                 'PassSeatSwtSts2PassSeatSwtHeiFrntSts': "legrestVerticalPositionSwitch",
                 'PassSeatSwtSts2PassSeatSwtSldSts': "longitudinalPositionSwitch",
                 'PassSeatSwtSts2PassSeatSwtInclSts': "backSwitch",
                'PassSeatSwtSts2PassSeatSwtAdjmtOfSpplFctHozlSts': "lumbarLongitudinalPositionSwitch",
                 'PassSeatSwtSts2PassSeatSwtAdjmtOfSpplFctVerSts': "lumbarVerticalPositionSwitch"}
        for key1, value1 in list1.items():
            for X in [1, 3, 0, 2]:
                logger.info(f"--信号{key1}--发送值{X}---")
                if X != 3: 
                    self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, key1, X)
                    sleep(1)
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatSwitchStatus",
                                            {"id": 0, "status": {value1: X}})
                else :
                    self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "SeatSwitchStatus")
        for key2,value2 in list2.items():
            for X in [1, 3, 0, 2]:
                if X != 3 :
                    self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, key2, X)
                    sleep(1)
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatSwitchStatus",
                                                    {"id": 1, "status": {value2: X}})
                else :
                    self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "SeatSwitchStatus")
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatSwitchStatus", {"seats": [12]},
                                                    {"out": [{"id": 0,
                                                                "status": {"verticalPositionSwitch": 2,
                                                                        "legrestVerticalPositionSwitch": 2,
                                                                        "longitudinalPositionSwitch": 2,
                                                                        "backSwitch": 2,
                                                                        "isLocalSwitchActivated": True,
                                                                        "lumbarLongitudinalPositionSwitch": 2,
                                                                        "lumbarVerticalPositionSwitch": 2}},
                                                                {"id": 1,
                                                                "status": {"verticalPositionSwitch": 2,
                                                                        "legrestVerticalPositionSwitch": 2,
                                                                        "longitudinalPositionSwitch": 2,
                                                                        "backSwitch": 2,
                                                                        "isLocalSwitchActivated": True,
                                                                        "lumbarLongitudinalPositionSwitch": 2,
                                                                        "lumbarVerticalPositionSwitch": 2}}]})
        
    @allure.title("遍历本地设置所有座椅通风等级时_加热等级为0_下切使用者模式通风等级置0")
    @pytest.mark.sanity
    def test_caseid_1980538(self):
        for X in [2, 11, 13]:
            for Y in range(1, 4):
                self.sd_tester.change_usage_mode(X)
                logger.info(f"使用者模式={X}--通风等级为{Y}")
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                {"params": [{"id": 0, "uint8Info": Y},
                                                            {"id": 1, "uint8Info": Y},
                                                            {"id": 4, "uint8Info": Y},
                                                            {"id": 6, "uint8Info": Y}]},timeout=0.5)
                sleep(1)
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel', {"params":[{"id":0,"uint8Info":Y},
                                                                                                    {"id":1,"uint8Info":Y},
                                                                                                    {"id":4,"uint8Info":Y},
                                                                                                    {"id":6,"uint8Info":Y}]},timeout=0.5)
                self.ipdu.check_multiple_signals(
                                [(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', 0),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', 0),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', 0),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', 0)])
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', Y),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowFirstRi', Y),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecLe', Y),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecRi', Y)])
                #下切使用者模式
                self.sd_tester.change_usage_mode(1)
                self.ipdu.check_multiple_signals(
                                [(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', 0),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', 0),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', 0),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', 0)])
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowFirstRi', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecRi', 0)])
        for X in [2, 11, 13]:
            for Y in range(1, 4):
                self.sd_tester.change_usage_mode(X)
                logger.info(f"使用者模式={X}--通风等级为{Y}")
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                {"params": [{"id": 0, "uint8Info": Y},
                                                            {"id": 1, "uint8Info": Y},
                                                            {"id": 4, "uint8Info": Y},
                                                            {"id": 6, "uint8Info": Y}]},timeout = 0.2)
                sleep(1)
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel', {"params":[{"id":0,"uint8Info":Y},
                                                                                                    {"id":1,"uint8Info":Y},
                                                                                                    {"id":4,"uint8Info":Y},
                                                                                                    {"id":6,"uint8Info":Y}]})
                self.ipdu.check_multiple_signals(
                                [(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', 0),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', 0),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', 0),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', 0)])
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', Y),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowFirstRi', Y),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecLe', Y),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecRi', Y)])
                #下切使用者模式
                self.sd_tester.change_usage_mode(0)
                self.ipdu.check_multiple_signals(
                                [(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', 0),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', 0),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', 0),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', 0)])
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowFirstRi', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecRi', 0)])

    @allure.title("遍历本地设置所有座椅通风加热等级时_下切使用者模式为2后设置不变")
    @pytest.mark.sanity
    def test_caseid_1980502(self):
        for X in [11, 13]:
            for Y in range(1,4):
                self.sd_tester.change_usage_mode(X)
                logger.info(f"使用者模式={X}--加热等级为{Y}")
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                {"params": [{"id": 0, "uint8Info": Y},
                                                            {"id": 1, "uint8Info": Y},
                                                            {"id": 4, "uint8Info": Y},
                                                            {"id": 6, "uint8Info": Y}]},timeout=0.2)
                self.sd_tester.change_usage_mode(2)
                sleep(1)
                self.ipdu.check_multiple_signals(
                                    [(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', Y),
                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', Y),
                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', Y),
                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', Y)])
        for X in [11, 13]:
            for Y in range(1,4):
                self.sd_tester.change_usage_mode(X)
                logger.info(f"使用者模式={X}--通风等级为{Y}")
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel', {"params":[{"id":0,"uint8Info":Y},
                                                                                                    {"id":1,"uint8Info":Y},
                                                                                                    {"id":4,"uint8Info":Y},
                                                                                                    {"id":6,"uint8Info":Y}]},timeout=0.2)
                self.sd_tester.change_usage_mode(2)
                sleep(1)
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', Y),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowFirstRi', Y),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecLe', Y),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecRi', Y)])

    @allure.title("遍历本地设置所有座椅加热等级时_通风等级为0_下切使用者模式加热等级置0")
    @pytest.mark.sanity
    def test_caseid_111084(self):
        for X in [2, 11, 13]:
            for Y in range(1, 4):
                self.sd_tester.change_usage_mode(X)
                logger.info(f"使用者模式={X}--加热等级为{Y}")
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                {"params": [{"id": 0, "uint8Info": Y},
                                                            {"id": 1, "uint8Info": Y},
                                                            {"id": 4, "uint8Info": Y},
                                                            {"id": 6, "uint8Info": Y}]})
                sleep(1)
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel', {"params":[{"id":0,"uint8Info":Y},
                                                                                                    {"id":1,"uint8Info":Y},
                                                                                                    {"id":4,"uint8Info":Y},
                                                                                                    {"id":6,"uint8Info":Y}]})
                self.ipdu.check_multiple_signals(
                                [(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', Y),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', Y),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', Y),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', Y)])
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowFirstRi', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecRi', 0)])
                #下切使用者模式
                self.sd_tester.change_usage_mode(1)
                self.ipdu.check_multiple_signals(
                                [(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', 0),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', 0),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', 0),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', 0)])
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowFirstRi', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecRi', 0)])
        for X in [2, 11, 13]:
            for Y in range(1, 4):
                self.sd_tester.change_usage_mode(X)
                logger.info(f"使用者模式={X}--加热等级为{Y}")
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                {"params": [{"id": 0, "uint8Info": Y},
                                                            {"id": 1, "uint8Info": Y},
                                                            {"id": 4, "uint8Info": Y},
                                                            {"id": 6, "uint8Info": Y}]})
                sleep(1)
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel', {"params":[{"id":0,"uint8Info":Y},
                                                                                                    {"id":1,"uint8Info":Y},
                                                                                                    {"id":4,"uint8Info":Y},
                                                                                                    {"id":6,"uint8Info":Y}]})
                self.ipdu.check_multiple_signals(
                                [(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', Y),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', Y),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', Y),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', Y)])
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowFirstRi', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecRi', 0)])
                #下切使用者模式
                self.sd_tester.change_usage_mode(0)
                self.ipdu.check_multiple_signals(
                                [(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', 0),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', 0),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', 0),
                                (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', 0)])
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowFirstRi', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecRi', 0)])
    
                
    @allure.title("本地设置所有座椅加热等级为0时_座椅通风不能关闭")
    @pytest.mark.sanity
    def test_caseid_111085(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            logger.info(f"使用者模式={X}")
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetAutoHeating',
                                             {"params": [{"id": 0, "isOn": False},
                                                         {"id": 1, "isOn": False},
                                                         {"id": 4, "isOn": False},
                                                         {"id": 6, "isOn": False}]})
            for Y in range(4):
                logger.info(f"设置档位为{Y}")
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                 {"params": [{"id": 0, "uint8Info": Y},
                                                             {"id": 1, "uint8Info": Y},
                                                             {"id": 4, "uint8Info": Y},
                                                             {"id": 6, "uint8Info": Y}]})
                sleep(1)
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                 {"params": [{"id": 0, "uint8Info": 0},
                                                             {"id": 1, "uint8Info": 0},
                                                             {"id": 4, "uint8Info": 0},
                                                             {"id": 6, "uint8Info": 0}]})
                sleep(1)
                self.ipdu.check_multiple_signals(
                    [(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', 0),
                     (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', 0),
                     (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', 0),
                     (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', 0)])
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', Y),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowFirstRi', Y),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecLe', Y),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecRi', Y)])
                
    @allure.title("本地设置所有座椅通风等级为0时_座椅加热不能关闭")
    @pytest.mark.sanity
    def test_caseid_111083(self):
        
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            logger.info(f"使用者模式={X}")
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetAutoHeating',
                                             {"params": [{"id": 0, "isOn": False},
                                                         {"id": 1, "isOn": False},
                                                         {"id": 4, "isOn": False},
                                                         {"id": 6, "isOn": False}]})
            for Y in range(4):
                logger.info(f"设置档位为{Y}")
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                 {"params": [{"id": 0, "uint8Info": Y},
                                                             {"id": 1, "uint8Info": Y},
                                                             {"id": 4, "uint8Info": Y},
                                                             {"id": 6, "uint8Info": Y}]})
                sleep(1)
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                 {"params": [{"id": 0, "uint8Info": 0},
                                                             {"id": 1, "uint8Info": 0},
                                                             {"id": 4, "uint8Info": 0},
                                                             {"id": 6, "uint8Info": 0}]})
                sleep(1)
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowFirstRi', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecRi', 0)])
                self.ipdu.check_multiple_signals(
                    [(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', Y),
                     (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', Y),
                     (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', Y),
                     (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', Y)])

    @allure.title("本地设置单个座椅加热或通风时，其余三座不能被打断")
    @pytest.mark.sanity
    def test_caseid_1980821(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetAutoHeating',
                                            {"params": [{"id": 0, "isOn": False},
                                                        {"id": 1, "isOn": False},
                                                        {"id": 4, "isOn": False},
                                                        {"id": 6, "isOn": False}]})
        for Y in range(4):
            logger.info(f"设置加热档位为{Y}")
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                {"params": [{"id": 0, "uint8Info": Y},
                                                            {"id": 1, "uint8Info": Y},
                                                            {"id": 4, "uint8Info": Y},
                                                            {"id": 6, "uint8Info": Y}]},timeout = 0.2)
            sleep(1)
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                {"params": [{"id": 0, "uint8Info": 1}]},timeout = 0.2)
            sleep(1)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', 1, timeout=0.5)
            self.ipdu.check_multiple_signals(
                [(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', 0),
                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', Y),
                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', Y),
                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', Y)]) 
        for Y in range(4):
            logger.info(f"设置通风档位为{Y}")
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                {"params": [{"id": 0, "uint8Info": Y},
                                                            {"id": 1, "uint8Info": Y},
                                                            {"id": 4, "uint8Info": Y},
                                                            {"id": 6, "uint8Info": Y}]},timeout = 0.2)
            sleep(1)
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                {"params": [{"id": 0, "uint8Info": 2}]})
            sleep(1)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe',2, timeout=0.5)
            self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowFirstRi', Y),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecLe', Y),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecRi', Y)])                               
                
    @allure.title("远程设置所有座椅加热等级_所有档_座椅通风为0")
    @pytest.mark.sanity
    @pytest.mark.failed
    def test_caseid_1939950(self):
        for X in [1,0]:
            for Y in range(1, 4):
                self.sd_tester.change_usage_mode(X)
                logger.info(f"使用者模式={X}--加热等级为{Y}")
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                {"params": [{"id": 0, "uint8Info": Y},
                                                            {"id": 1, "uint8Info": Y}]})
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel', {"params":[{"id":0,"uint8Info":Y},
                                                                                                    {"id":1,"uint8Info":Y}]})
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr48, 'TelmSeatDrvHeatClimaLvl', Y),
                                                    (self.ipdu.bodycan.CemBodyFr48, 'TelmSeatPassHeatClimaLvl', Y),
                                                    (self.ipdu.bodycan.CemBodyFr48, 'TelmSeatDrvVentnClimaLvl', 0),
                                                    (self.ipdu.bodycan.CemBodyFr47, 'TelmSeatPassVentnClimaLvl', 0)])  
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                {"params": [{"id": 4, "uint8Info": Y},
                                                            {"id": 6, "uint8Info": Y}]})
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel', {"params":[{"id":6,"uint8Info":Y}]})
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr47, 'TelmSeatSecRiHeatClimaLvl', Y, timeout=1)
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel', {"params":[{"id":4,"uint8Info":Y}]})
                sleep(2)
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr47, 'TelmSeatSecLeHeatClimaLvl', Y),
                                                    (self.ipdu.bodycan.CemBodyFr47, 'TelmSeatSecLeVentnClimaLvl', 0),
                                                    (self.ipdu.bodycan.CemBodyFr47, 'TelmSeatSecRiVentnClimaLvl', 0),
                                                   ])  

    @allure.title("遍历_获取通风等级_所有情况")
    @pytest.mark.smoke
    def test_caseid_1983351(self):
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentnLvlSts', 1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentnLvlSts', 1)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecLe',1)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecRi',1)
        self.partner.empty_all(0.5)
        for level in range(4):
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentnLvlSts', level)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentnLvlSts', level)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecLe',level)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecRi',level)
            sleep(1)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVentingLevel", {"seats": [3]}, 
                                              {"out": [{"id": 0, "level": level},{"id": 1, "level": level}]})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVentingLevel", {"seats": [7]}, 
                                              {"out": [{"id": 4, "level": level},{"id": 6, "level": level}]})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVentingLevel", {"seats": [12]}, 
                                              {"out": [{"id": 0, "level": level},{"id": 1, "level": level},
                                                       {"id": 4, "level": level},{"id": 6, "level": level}]})
            
    @allure.title("遍历_获取加热等级_所有情况")
    @pytest.mark.smoke
    def test_caseid_105601(self):
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgLvlSts', 1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgLvlSts', 1)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecLe',1)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecRi',1)
        self.partner.empty_all(0.5)
        for level in range(4):
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgLvlSts', level)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgLvlSts', level)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecLe',level)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecRi',level)
            sleep(0.5)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetHeatingLevel", {"seats": [3]}, 
                                              {"out": [{"id": 0, "level": level},{"id": 1, "level": level}]})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetHeatingLevel", {"seats": [7]}, 
                                              {"out": [{"id": 4, "level": level},{"id": 6, "level": level}]})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetHeatingLevel", {"seats": [12]}, 
                                              {"out": [{"id": 0, "level": level},{"id": 1, "level": level},
                                                       {"id": 4, "level": level},{"id": 6, "level": level}]})
                
    @allure.title("获取和通知座椅故障信息_主副驾位置信息错误")
    @pytest.mark.full
    def test_caseid_111319(self):
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecLeBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecMidBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecRiBltLockSts', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldQF', 3)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts', 1)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecLeBltLockSts', 1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecMidBltLockSts', 1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecRiBltLockSts', 1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF', 1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF', 1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', 1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiQF', 1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldQF', 1)
        sleep(1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatFault",
                                  {"faults": [{"faultId": 6, "faultMsg": "", "seatId": 0},
                                              {"faultId": 6, "faultMsg": "", "seatId": 1},
                                              {"faultId": 6, "faultMsg": "", "seatId": 4},
                                              {"faultId": 6, "faultMsg": "", "seatId": 5},
                                              {"faultId": 6, "faultMsg": "", "seatId": 6},
                                              {"faultId": 8, "faultMsg": "", "seatId": 0},
                                              {"faultId": 8, "faultMsg": "", "seatId": 1}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatFault", {}, {"out": [{"faultId": 6, "faultMsg": "", "seatId": 0},
                                              {"faultId": 6, "faultMsg": "", "seatId": 1},
                                              {"faultId": 6, "faultMsg": "", "seatId": 4},
                                              {"faultId": 6, "faultMsg": "", "seatId": 5},
                                              {"faultId": 6, "faultMsg": "", "seatId": 6},
                                              {"faultId": 8, "faultMsg": "", "seatId": 0},
                                              {"faultId": 8, "faultMsg": "", "seatId": 1}]})

        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecLeBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecMidBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecRiBltLockSts', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldQF', 3)
        sleep(1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatFault",
                                          {"faults": [{"faultId": 0, "faultMsg": "", "seatId": 12}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatFault", {},
                                              {"out": [{"faultId": 0, "faultMsg": "", "seatId": 12}]})
                
    @allure.title("远程设置所有座椅通风等级_所有档_座椅加热为0")
    @pytest.mark.sanity
    def test_caseid_1980539(self):
        for X in [1,0]:
            for Y in range(1, 4):
                self.sd_tester.change_usage_mode(X)
                logger.info(f"使用者模式={X}--通风等级为{Y}")
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                {"params": [{"id": 0, "uint8Info": Y},
                                                            {"id": 1, "uint8Info": Y}]})
                sleep(0.1)
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel', {"params":[{"id":0,"uint8Info":Y},
                                                                                                    {"id":1,"uint8Info":Y}]})
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'TelmSeatDrvVentnClimaLvl', Y, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr47, 'TelmSeatPassVentnClimaLvl', Y, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'TelmSeatPassHeatClimaLvl', 0)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'TelmSeatDrvHeatClimaLvl', 0)
                
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                {"params": [{"id": 4, "uint8Info": Y},
                                                            {"id": 6, "uint8Info": Y}]})
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel', {"params":[{"id":4,"uint8Info":Y}]})
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr47, 'TelmSeatSecLeVentnClimaLvl', Y, timeout=1)
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel', {"params":[{"id":6,"uint8Info":Y}]})
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr47, 'TelmSeatSecRiVentnClimaLvl', Y),
                                                    (self.ipdu.bodycan.CemBodyFr47, 'TelmSeatSecRiHeatClimaLvl', 0),
                                                    (self.ipdu.bodycan.CemBodyFr47, 'TelmSeatSecLeHeatClimaLvl', 0),
                                                   ])  
        
    @allure.title("获取和通知所有自动加热通风状态_打开或关闭")
    @pytest.mark.smoke
    def test_caseid_106965(self):
        for type in ["SetAutoHeating","SetAutoVenting"]:
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, type, {"params": [{"id": 0, "isOn": False},
                                                                                                {"id": 1, "isOn": False},
                                                                                                {"id": 4, "isOn": False},
                                                                                                {"id": 6, "isOn": False}]}, timeout=0.2)
        self.partner.empty_all(0.5)
        for status in [True,False]:
            for X in [0,1,4,6]:
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetAutoHeating", {"params": [{"id": 0, "isOn": status},
                                                                                            {"id": 1, "isOn": status},
                                                                                            {"id": 4, "isOn": status},
                                                                                            {"id": 6, "isOn": status}]},timeout = 0.2)
                self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "AutoHeating",{"id": X, "isOn": status})                                      
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetAutoHeating", {"seats": [12]},
                                                {"out": [{"id": 0, "isOn": status}, {"id": 1, "isOn": status},
                                                            {"id": 4, "isOn": status}, {"id": 6, "isOn": status}]})
        for status2 in [True,False]:
            for X in [0,1,4,6]:
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetAutoVenting", {"params": [{"id": 0, "isOn": status2},
                                                                                            {"id": 1, "isOn": status2},
                                                                                            {"id": 4, "isOn": status2},
                                                                                            {"id": 6, "isOn": status2}]}, timeout=0.2)
                self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "AutoVenting",{"id": X, "isOn": status2})                                      
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetAutoVenting", {"seats": [12]},
                                                {"out": [{"id": 0, "isOn": status2}, {"id": 1, "isOn": status2},
                                                            {"id": 4, "isOn": status2}, {"id": 6, "isOn": status2}]})

    @pytest.mark.sanity
    @allure.title("设置主驾安全带震动_返回succes")
    def test_caseid_1919341(self):
        for time1 in range(9):
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetDriverBeltVibration",
                                                  {"duration": time1}, {"out": 0})
            sleep(time1+1)

    @allure.title("获取和通知所有安全带未系报警状态_前排g和后排f所有触发条件")
    @pytest.mark.sanity
    def test_caseid_1892827(self):
        self.set_vehicle_speed(0.0)
        for X in [2,11,13]:
            self.sd_tester.change_usage_mode(X)
            self.io.driver_seat_notpresent()
            self.partner.empty_all(0.5)
            self.io.driver_seat_present()
            self.set_four_seat_occupt(1,1,1,1)
            self.seat_belt_status(0,0,0,0,0)
            #g和f条件1座椅不占位
            self.io.driver_seat_notpresent()
            self.set_four_seat_occupt(0,0,0,0)
            self.check_all_beltwarning(1)
            self.io.driver_seat_present()
            self.set_four_seat_occupt(1,1,1,1)
            #g和f条件2安全带已系
            self.seat_belt_status(1,1,1,1,1)
            self.check_all_beltwarning(1)
            self.seat_belt_status(0,0,0,0,0)
            #g和f条件3使用者模式切为0，1
            for Y in [1,0]:
                logger.info(f"使用者模式从{X}到{Y}")
                self.sd_tester.change_usage_mode(Y)
                self.check_all_beltwarning(1)
                self.sd_tester.change_usage_mode(X)

    @allure.title("获取和通知所有安全带未系报警状态_满足车速_流程图d/e到h到c触发的所有报警状态")
    @pytest.mark.smoke
    def test_caseid_1980401(self):
        self.io.set_four_door_close()
        for X in [2,11,13]: #使用者为1试过不行
            self.sd_tester.change_usage_mode(X)
            for status in ["open","close"]:
                logger.info(f"X={X},status={status}")
                self.Shift_Gear(2)
                self.set_four_seat_occupt(0,0,0,0)
                self.io.driver_seat_notpresent()
                self.partner.empty_all(0.5)
                self.io.driver_seat_present()
                self.set_four_seat_occupt(1,1,1,1)
                self.seat_belt_status(0,0,0,0,0)
                self.partner.empty_all(0.5)
                self.set_vehicle_speed(7.0)
                self.check_all_beltwarning(3)
                #由d到h通过降车速为10以下到任意门打开到无报警
                self.set_vehicle_speed(2.0)
                eval(f"self.set_four_Door_{status}()")
                self.check_all_beltwarning(2)
                sleep(1)
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 0, "status": 2},{"id": 1, "status": 2},{"id": 4, "status": 2},
                                                                 {"id": 5, "status": 2},{"id": 6, "status": 2}]})
            #由d到h通过座椅都无占位到无报警
            self.set_vehicle_speed(7.0)
            self.io.driver_seat_notpresent()
            self.set_four_seat_occupt(0,0,0,0)
            self.check_all_beltwarning(1)
            self.io.driver_seat_present()
            self.set_four_seat_occupt(1,1,1,1)
            #由d到h通过座椅安全带系上到无报警
            self.set_vehicle_speed(7.0)
            self.seat_belt_status(1,1,1,1,1)
            self.check_all_beltwarning(1)
            self.seat_belt_status(0,0,0,0,0)
            #由d到h通过切换使用者模式为1到无报警
            self.set_vehicle_speed(0.0)
            logger.info(f"--当前使用者模式从{X}到1")
            self.sd_tester.change_usage_mode(1)
            self.check_all_beltwarning(1)

    @allure.title("获取和通知所有安全带未系报警状态_流程图前排c到i到c和后排c到h再到c触发的所有报警状态")
    @pytest.mark.smoke
    def test_caseid_1980405(self):
        self.set_vehicle_speed(0.0)
        self.sd_tester.change_usage_mode(2)
        self.set_four_seat_occupt(0,0,0,0)
        self.io.driver_seat_notpresent()
        self.partner.empty_all(0.5)
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(0,0,0,0,0)
        self.check_all_beltwarning(2)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                {"out": [{"id": 0, "status": 2},{"id": 1, "status": 2},{"id": 4, "status": 2},
                                                            {"id": 5, "status": 2},{"id": 6, "status": 2}]})
        #由c到i再到c一级报警
        self.seat_NA_status(1,1,1,1,1)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                {"out": [{"id": 0, "status": 5},{"id": 1, "status": 5},{"id": 4, "status": 5},
                                                            {"id": 5, "status": 5},{"id": 6, "status": 5}]})
        self.seat_NA_status(0,0,0,0,0)
        self.check_all_beltwarning(2)

    @allure.title("获取和通知所有安全带未系报警状态_流程图前排d到m后排d到e触发的所有报警状态")
    @pytest.mark.full
    def test_caseid_1980407(self):
        self.io.set_four_door_close()
        for X in [11,13]: #使用者为1试过不行
            self.sd_tester.change_usage_mode(X)
            self.Shift_Gear(3)
            self.set_four_seat_occupt(0,0,0,0)
            self.io.driver_seat_notpresent()
            self.partner.empty_all(0.5)
            self.io.driver_seat_present()
            self.set_four_seat_occupt(1,1,1,1)
            self.seat_belt_status(0,0,0,0,0)
            self.set_vehicle_speed(6.0)
            self.check_all_beltwarning(3)
            sleep(2)
            #由d到h通过降车速为0挂入P挡
            self.set_vehicle_speed(0.0)
            self.Shift_Gear(0)
            self.check_all_beltwarning(2)
            sleep(1)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                    {"out": [{"id": 0, "status": 2},{"id": 1, "status": 2},{"id": 4, "status": 2},
                                                            {"id": 5, "status": 2},{"id": 6, "status": 2}]})
                
    @allure.title("获取和通知所有安全带未系报警状态_测试3级最终报警能否回到3级最初报警")
    @pytest.mark.full
    def test_caseid_1980409(self):
        self.sd_tester.change_usage_mode(13)
        self.Shift_Gear(3)
        self.set_four_seat_occupt(0,0,0,0)
        self.io.driver_seat_notpresent()
        self.partner.empty_all(0.5)
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,0,0,0)
        self.seat_belt_status(0,0,0,0,0)
        self.set_vehicle_speed(10.0)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                {"out": [{"id": 0, "status": 4},{"id": 1, "status": 4},{"id": 4, "status": 1},
                                                        {"id": 5, "status": 1},{"id": 6, "status": 1}]})
        sleep(2)
        #车速降到22到35之间
        self.set_vehicle_speed(6.0)
        sleep(2)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                {"out": [{"id": 0, "status": 4},{"id": 1, "status": 4},{"id": 4, "status": 1},
                                                        {"id": 5, "status": 1},{"id": 6, "status": 1}]})

    @allure.title("获取和通知所有安全带未系报警状态_a/b到K再到L无报警")
    @pytest.mark.full
    def test_caseid_1892821(self):
        for X in [2,11,13]: #使用者为1试过不行
            self.sd_tester.change_usage_mode(X)
            self.seat_NA_status(0,0,0,0,0)
            self.io.driver_seat_notpresent()
            self.set_four_seat_occupt(0,0,0,0)
            self.partner.empty_all(0.5)
            self.seat_NA_status(1,1,1,1,1)
            self.check_All_seltwaring_fault_event()
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                    {"out": [{"name": "Driver Seat Belt Warning", "info": "4"},
                                                                {"name": "Passenger Seat Belt Warning", "info": "4"},
                                                                {"name": "Second Row Left Seat Belt Warning", "info": "4"},
                                                                {"name": "Second Row Middle Seat Belt Warning", "info": "4"},
                                                                {"name": "Second Row Right Seat Belt Warning", "info": "4"}]})
            self.seat_NA_status(0,0,0,0,0)
            self.check_all_beltwarning(1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                                        {"list": [{"name":"Seat Belt", "state": "0"}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                    {"out": [{"name": "Driver Seat Belt Warning", "info": "0"},
                                                                {"name": "Passenger Seat Belt Warning", "info": "0"},
                                                                {"name": "Second Row Left Seat Belt Warning", "info": "0"},
                                                                {"name": "Second Row Middle Seat Belt Warning", "info": "0"},
                                                                {"name": "Second Row Right Seat Belt Warning", "info": "0"}]})
            
    @allure.title("获取和通知所有安全带未系报警状态_c一级报警及WTI报警")
    @pytest.mark.full
    def test_caseid_1892831(self):
        def info(input):
            if input > 1:
                return 2
            else:
                return 0
        self.io.driver_seat_notpresent()
        self.partner.empty_all(0.5)
        for usgmode in [0,1,2,11,13]:
            self.sd_tester.change_usage_mode(usgmode)
            for ocupt in [1,2]:
                self.io.driver_seat_present()
                logger.info(f"切换使用者模式{usgmode}")
                self.set_four_seat_occupt(ocupt,ocupt,ocupt,ocupt)
                self.seat_belt_status(0,0,0,0,0)
                if usgmode in [0,1
                               ]: #处于0或1使用者模式时，没有通知并且调用结果都是1
                    self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "BeltWarning")
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 0, "status": 1},{"id": 1, "status": 1},{"id": 4, "status": 1},
                                                                 {"id": 5, "status": 1},{"id": 6, "status": 1}]})
                else:
                    self.check_Wti_all_beltwarning_one_event()
                    self.check_all_beltwarning(2)
                    self.check_Wti_all_beltwarning_one_reponse()
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 0, "status": info(usgmode)},{"id": 1, "status": info(usgmode)},{"id": 4, "status": info(usgmode)},
                                                                 {"id": 5, "status": info(usgmode)},{"id": 6, "status": info(usgmode)}]})
                self.seat_belt_status(1,1,1,1,1)

    @allure.title("获取和通知所有安全带未系报警状态_满足车速_流程图d到e到f到d触发的所有报警状态")
    @pytest.mark.full
    def test_caseid_1980390(self):
        self.io.driver_seat_notpresent()
        self.seat_belt_status(1,1,1,1,1)
        self.partner.empty_all(0.5)
        self.sd_tester.change_usage_mode(11) #D挡Driving试过也是ok的
        self.Shift_Gear(2)
        self.io.driver_seat_present()
        self.set_four_seat_occupt(2,2,2,2)
        self.set_vehicle_speed(7.0)
        self.seat_belt_status(0,0,0,0,0)
        #22-35km/h内触发所有座椅二级初级报警
        self.check_all_beltwarning(3)
        self.check_Wti_all_beltwarning_two_event()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                {"out": [{"id": 0, "status": 3},{"id": 1, "status": 3},{"id": 4, "status": 3},
                                                            {"id": 5, "status": 3},{"id": 6, "status": 3}]})
        self.check_Wti_all_beltwarning_two_reponse()
        #大于35km/h触发前排二级最终报警，后排仍是二级初级报警
        self.set_vehicle_speed(10.0)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                {"out": [{"name":"Seat Belt", "state": "3"}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                {"out": [{"id": 0, "status": 4},{"id": 1, "status": 4},{"id": 4, "status": 3},
                                                            {"id": 5, "status": 3},{"id": 6, "status": 3}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{"name": "Driver Seat Belt Warning", "info": "3"},
                                                            {"name": "Passenger Seat Belt Warning", "info": "3"},
                                                            {"name": "Second Row Left Seat Belt Warning", "info": "2"},
                                                            {"name": "Second Row Middle Seat Belt Warning", "info": "2"},
                                                            {"name": "Second Row Right Seat Belt Warning", "info": "2"}]})
        #大于22km/h后等待35S触发后排回到一级报警
        sleep(35)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                {"out": [{"id": 0, "status": 4},{"id": 1, "status": 4},{"id": 4, "status": 2},
                                                            {"id": 5, "status": 2},{"id": 6, "status": 2}]})
        #大于35km/h后等待95S所有安全带都回到一级报警
        sleep(60)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                {"out": [{"id": 0, "status": 2},{"id": 1, "status": 2},{"id": 4, "status": 2},
                                                            {"id": 5, "status": 2},{"id": 6, "status": 2}]})
        #不能再通过d方式进入到二级报警
        sleep(50)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                {"out": [{"id": 0, "status": 2},{"id": 1, "status": 2},{"id": 4, "status": 2},
                                                            {"id": 5, "status": 2},{"id": 6, "status": 2}]})
        self.set_vehicle_speed(0.0)
        
    @allure.title("获取和通知所有安全带未系报警状态_满足时间_流程图d到e到f到j触发的所有报警状态")
    @pytest.mark.full
    def test_caseid_1892833(self):
        self.io.driver_seat_notpresent()
        self.seat_belt_status(1,1,1,1,1)
        self.partner.empty_all(0.5)
        self.sd_tester.change_usage_mode(13) #N挡Active试过也是ok的
        self.Shift_Gear(3)
        self.io.driver_seat_present()
        self.set_four_seat_occupt(2,2,2,2)
        self.seat_belt_status(0,0,0,0,0)
        self.set_vehicle_speed(5.0)
        #50-80S内触发所有座椅二级初级报警
        sleep(51)
        self.check_all_beltwarning(3)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                {"out": [{"id": 0, "status": 3},{"id": 1, "status": 3},{"id": 4, "status": 3},
                                                            {"id": 5, "status": 3},{"id": 6, "status": 3}]})
        self.check_Wti_all_beltwarning_two_event()
        self.check_Wti_all_beltwarning_two_reponse()
        #80到85S内触发前排二级最终报警，后排还是二级初级报警
        sleep(31)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                {"out": [{"name":"Seat Belt", "state": "3"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{"name": "Driver Seat Belt Warning", "info": "3"},
                                                            {"name": "Passenger Seat Belt Warning", "info": "3"},
                                                            {"name": "Second Row Left Seat Belt Warning", "info": "2"},
                                                            {"name": "Second Row Middle Seat Belt Warning", "info": "2"},
                                                            {"name": "Second Row Right Seat Belt Warning", "info": "2"}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                {"out": [{"id": 0, "status": 4},{"id": 1, "status": 4},{"id": 4, "status": 3},
                                                            {"id": 5, "status": 3},{"id": 6, "status": 3}]})
        #85S到175S内前排二级最终报警，后排进入一级报警
        sleep(4)
        self.check_Secondrow_seltwaring_one_event()
        sleep(85)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{"name": "Driver Seat Belt Warning", "info": "3"},
                                                            {"name": "Passenger Seat Belt Warning", "info": "3"},
                                                            {"name": "Second Row Left Seat Belt Warning", "info": "1"},
                                                            {"name": "Second Row Middle Seat Belt Warning", "info": "1"},
                                                            {"name": "Second Row Right Seat Belt Warning", "info": "1"}]})
        #175S后所有都进入一级报警
        sleep(5)
        self.check_Wti_all_beltwarning_one_reponse()
        #225S后不能通过d方式进入到二级报警初级，仍是一级报警
        sleep(50)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                {"out": [{"id": 0, "status": 2},{"id": 1, "status": 2},{"id": 4, "status": 2},
                                                            {"id": 5, "status": 2},{"id": 6, "status": 2}]})
        #故障状态
        self.seat_NA_status(1,1,1,1,1)
        self.check_All_seltwaring_fault_event()
        #故障恢复应该仍是一级报警
        self.seat_NA_status(0,0,0,0,0)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                {"out": [{"id": 0, "status": 2},{"id": 1, "status": 2},{"id": 4, "status": 2},
                                                            {"id": 5, "status": 2},{"id": 6, "status": 2}]})
    
    @allure.title("获取和通知所有安全带未系报警状态_前排d到e到m到d触发的所有报警状态_条件1")
    @pytest.mark.full
    def test_caseid_1984160(self):
        self.io.driver_seat_notpresent()
        self.seat_belt_status(1,1,1,1,1)
        self.partner.empty_all(0.5)
        self.sd_tester.change_usage_mode(13) #N挡Active试过也是ok的
        self.Shift_Gear(3)
        self.io.driver_seat_present()
        self.set_four_seat_occupt(2,2,2,2)
        self.seat_belt_status(0,0,0,0,0)
        # self.set_vehicle_speed(5.0)
        # #50-80S内触发所有座椅二级初级报警  d迁移
        # sleep(51)
        #80到85S内触发前排二级最终报警，后排还是二级初级报警  e迁移
        self.set_vehicle_speed(7.0)
        sleep(31)
        #触发前排迁移m 5个条件
        self.set_vehicle_speed(0.0)
        self.Shift_Gear(0)
        self.check_all_beltwarning(2)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list": [{"name": "Driver Seat Belt Warning", "info": "1"}]})                                    
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list":[{"name": "Passenger Seat Belt Warning", "info": "1"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{"name": "Driver Seat Belt Warning", "info": "1"},
                                                            {"name": "Passenger Seat Belt Warning", "info": "1"},
                                                            ]})
        sleep(90)
        self.Shift_Gear(3)
        self.set_vehicle_speed(7.0)
        sleep(6)   
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 0, "warn": 3})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 1, "warn": 3})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [0,1]},
                                                {"out": [{"id": 0, "status": 3},{"id": 1, "status": 3},
                                                            ]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list": [{"name": "Driver Seat Belt Warning", "info": "2"}]})                                    
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list":[{"name": "Passenger Seat Belt Warning", "info": "2"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{"name": "Driver Seat Belt Warning", "info": "2"},
                                                            {"name": "Passenger Seat Belt Warning", "info": "2"},
                                                            ]})
    @allure.title("获取和通知所有安全带未系报警状态_前排d到e到m到d触发的所有报警状态_条件2")
    @pytest.mark.full
    def test_caseid_1984161(self):     
        self.io.driver_seat_notpresent()
        self.seat_belt_status(1,1,1,1,1)
        self.partner.empty_all(0.5)
        self.sd_tester.change_usage_mode(13) #N挡Active试过也是ok的
        self.Shift_Gear(3)
        self.io.driver_seat_present()
        self.set_four_seat_occupt(2,2,2,2)
        self.seat_belt_status(0,0,0,0,0)
        # self.set_vehicle_speed(5.0)
        # #50-80S内触发所有座椅二级初级报警  d迁移
        # sleep(51)
        self.set_vehicle_speed(7.0)
        #80到85S内触发前排二级最终报警，后排还是二级初级报警  e迁移
        sleep(31)
        
        #触发前排迁移m 5个条件
        self.set_vehicle_speed(0.0)
        self.Shift_Gear(0)
        self.check_all_beltwarning(2)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list": [{"name": "Driver Seat Belt Warning", "info": "1"}]})                                    
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list":[{"name": "Passenger Seat Belt Warning", "info": "1"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{"name": "Driver Seat Belt Warning", "info": "1"},
                                                            {"name": "Passenger Seat Belt Warning", "info": "1"},
                                                            ]})
        self.Shift_Gear(3)
        self.set_vehicle_speed(7.0)
        
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 0, "warn": 3})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 1, "warn": 3})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [0,1]},
                                                {"out": [{"id": 0, "status": 3},{"id": 1, "status": 3},
                                                            ]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list": [{"name": "Driver Seat Belt Warning", "info": "2"}]})                                    
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list":[{"name": "Passenger Seat Belt Warning", "info": "2"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{"name": "Driver Seat Belt Warning", "info": "2"},
                                                            {"name": "Passenger Seat Belt Warning", "info": "2"},
                                                            ]})
    
    @allure.title("获取和通知所有安全带未系报警状态_前排d到e到m到d触发的所有报警状态_条件3")
    @pytest.mark.full
    def test_caseid_1984162(self):
        self.io.driver_seat_notpresent()
        self.seat_belt_status(1,1,1,1,1)
        self.partner.empty_all(0.5)
        self.sd_tester.change_usage_mode(13) #N挡Active试过也是ok的
        self.Shift_Gear(3)
        self.io.driver_seat_present()
        self.set_four_seat_occupt(2,2,2,2)
        self.seat_belt_status(0,0,0,0,0)
        self.set_vehicle_speed(7.0)
        sleep(31)
        
        #触发前排迁移m 5个条件
        self.set_vehicle_speed(0.0)
        self.Shift_Gear(0)
        self.check_all_beltwarning(2)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list": [{"name": "Driver Seat Belt Warning", "info": "1"}]})                                    
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list":[{"name": "Passenger Seat Belt Warning", "info": "1"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{"name": "Driver Seat Belt Warning", "info": "1"},
                                                            {"name": "Passenger Seat Belt Warning", "info": "1"},
                                                            ]})

        self.Shift_Gear(3)
        self.set_vehicle_speed(5.0)
        sleep(51)
        
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 0, "warn": 3})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 1, "warn": 3})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [0,1]},
                                                {"out": [{"id": 0, "status": 3},{"id": 1, "status": 3},
                                                            ]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list": [{"name": "Driver Seat Belt Warning", "info": "2"}]})                                    
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                                        {"list":[{"name": "Passenger Seat Belt Warning", "info": "2"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{"name": "Driver Seat Belt Warning", "info": "2"},
                                                            {"name": "Passenger Seat Belt Warning", "info": "2"},
                                                            ]})
             
    @allure.title("通知和获取安全带装配状态_遍历")
    @pytest.mark.sanity
    def test_caseid_1892805(self):
        self.set_second_selt_equip(0)
        self.partner.empty_all(0.5)
        for State in [1,0]:
            self.set_second_selt_equip(State)
            sleep(0.5)
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltEquipStatus", {"id": 4, "status": State})
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltEquipStatus", {"id": 5, "status": State})
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltEquipStatus", {"id": 6, "status": State})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltEquipStatus", {"seats": [4]},
                                                {"out": [{"id": 4, "uint8Info": State}]})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltEquipStatus", {"seats": [5]},
                                                {"out": [{"id": 5, "uint8Info": State}]})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltEquipStatus", {"seats": [6]},
                                                {"out": [{"id": 6, "uint8Info": State}]})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltEquipStatus", {"seats": [7]},
                                                {"out": [{"id": 4, "uint8Info": State},{"id": 5, "uint8Info": State},{"id": 6, "uint8Info": State}]})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltEquipStatus", {"seats": [12]},
                                                {"out": [{"id": 4, "uint8Info": State}, {"id": 5, "uint8Info": State},
                                                        {"id": 6, "uint8Info": State}]})
             
    @allure.title("获取和通知座椅占位状态_所有座椅传感器占位所有情况")
    @pytest.mark.sanity
    def test_caseid_1980324(self):
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 0) 
        self.seat_belt_status(0,0,0,0,0)
        self.set_four_seat_occupt(0,0,0,0)
        self.partner.empty_all(0.5)
        for X in [1,2]:
            logger.info(f"---发送座椅占位信号为{X}")
            self.io.driver_seat_present()
            self.check_DrvrSeatOccupt_event(1,1,0)
            self.set_four_seat_occupt(X,X,X,X)
            self.check_four_seatoccupt_event(1,1,0)
            self.check_All_seatOccupt_response(1,1,0) 
            #主驾
            self.io.driver_seat_notpresent()
            #2S内
            self.check_DrvrSeatOccupt_event(0,1,0)
            #2S后
            sleep(2)
            self.check_DrvrSeatOccupt_event(0,0,0)
            
            #其余四座
            self.set_four_seat_occupt(0,0,0,0)
            #2S内
            self.check_four_seatoccupt_event(0,1,0)
            #2S后
            sleep(2)
            self.check_four_seatoccupt_event(0,0,0)


    @allure.title("主驾座椅不同部位调节禁用scene4_车速限制")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1751631?projectId=46')
    @pytest.mark.full
    def test_caseid_1919310(self):
        def hei_REQ(direction):
            if direction == 2:
                return 1
            elif direction == 5:
                return 2
            else:
                return 0
        def Len_REQ(direction):
            if direction == 0:
                return 1
            elif direction == 3:
                return 2
            else:
                return 0
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 1.1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatBtnPsd', 0)
        sleep(1)
        for direction in [2, 5]:
            logger.info(f"--腿托方向发送{direction}")
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                             {"id": 0, "part": 2, "direction": direction}, timeout=0.2)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatCushTiltAdjmtRowFirstDrvr', hei_REQ(direction), timeout=0.5)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 1.4)
            sleep(1)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatCushTiltAdjmtRowFirstDrvr', 0, timeout=0.5)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 1.1)
            sleep(1)
        for direction in [0,3,2,5]:
            logger.info(f"--高度-前后方向发送{direction}")
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                             {"id": 0, "part": 0, "direction": direction}, timeout=0.2)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstDrvr',Len_REQ(direction), timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatHeiAdjmtRowFirstDrvr',hei_REQ(direction), timeout=0.5)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 1.4)
            sleep(1)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstDrvr',0, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatHeiAdjmtRowFirstDrvr',0, timeout=0.5)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 1.1)
            sleep(1)
        for direction in [0,3]:
            logger.info(f"--靠背方向发送{direction}")
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                             {"id": 0, "part": 1, "direction": direction}, timeout=0.2)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'BackRestAdjmtRowFirstDrvr',Len_REQ(direction), timeout=0.5)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 1.4)
            sleep(1)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'BackRestAdjmtRowFirstDrvr',0, timeout=0.5)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 1.1)
            sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 1.5)
        sleep(1)
        for path in [0,1,2]: #车速大于5km/h每个接口都无法调用
            for direction in [0,3,2,5]:
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                             {"id": 0, "part": path, "direction": direction}, timeout=0.2)
                logger.info(f"--部位{path}方向发送{direction}")
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatCushTiltAdjmtRowFirstDrvr', 0, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'BackRestAdjmtRowFirstDrvr',0, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstDrvr',0, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatHeiAdjmtRowFirstDrvr',0, timeout=0.5)

    @allure.title("主驾座椅不同部位调节禁用scene1_模式限制")
    @pytest.mark.sanity
    def test_caseid_105563(self):
        def result(part,direction):  #以下列表中的数分别代表前后、高度、靠背、腿托的调节信号  
            if part == 0 :
                if direction ==0:
                    return [1,0,0,0]
                elif direction ==3:
                    return [2,0,0,0]
                elif direction ==2:
                    return [0,1,0,0]
                elif direction ==5:
                    return [0,2,0,0]
            elif part == 1:
                if direction ==0:
                    return [0,0,1,0]
                elif direction ==3:
                    return [0,0,2,0]
                else:
                    return[0,0,0,0]
            elif part == 2 :
                if direction ==2:
                    return [0,0,0,1]
                elif direction ==5:
                    return [0,0,0,2]
                else:
                    return[0,0,0,0]
                 
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 0)
        self.partner.empty_all(0.5)
        self.set_Drvrseat_condition_allow()
        # self.dk.set_cenlock_sts(0x1)
        for path in [0,1,2]:
            for direction1 in [0,2,3,5]: 
                for carmode in [1,2,3]: #校验每个部位每个方向都从车辆模式0切到1、2、3
                    logger.info(f"--部位{path}方向正常发送{direction1}")
                    self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 0, "part": path, "direction": direction1}, timeout=0.2)
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstDrvr',result(path,direction1)[0], timeout=0.5)
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatHeiAdjmtRowFirstDrvr',result(path,direction1)[1], timeout=0.5)
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatCushTiltAdjmtRowFirstDrvr', result(path,direction1)[3], timeout=0.5)
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'BackRestAdjmtRowFirstDrvr',result(path,direction1)[2], timeout=0.5)
                    self.sd_tester.change_car_mode(carmode) #在遍历每个方向时将模式切为非0和5
                    logger.info(f"--部位{path}方向正常发送{direction1}--车辆模式从0切为{carmode}")
                    self.check_Drvrseat_direction_not_send()
                    self.sd_tester.change_car_mode(0)
                    sleep(1)  #http://172.18.128.7:8080/2023_11_25_11_17_36/
        for carmode2 in [1,2,3]:
            for path in [0,1,2]:
                for direction1 in [0,2,3,5]: 
                    self.sd_tester.change_car_mode(carmode) #前提条件为车辆模式1，2，3
                    self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 0, "part": path, "direction": direction1}, timeout=0.2)
                    logger.info(f"--车辆模在{carmode}下-部位{path}发送{direction1}不能下发-")
                    self.check_Drvrseat_direction_not_send()

    @allure.title("遍历_设置所有座椅加热时间_0-59min")
    @pytest.mark.full
    def test_caseid_105741(self):
        info ={0:'HmiSeatClimaTmrHmiSeatHeatgFirstLeTmr', 1:'HmiSeatClimaTmrHmiSeatHeatgFirstRiTmr',
                4:'HmiSeatClimaTmrHmiSeatHeatgSecLeTmr', 6:'HmiSeatClimaTmrHmiSeatHeatgSecRiTmr'}
        for key,value in info.items():
             for Y in [0, 30, 59]:
                logger.info(f"---座椅{key}--请求{Y}--")
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingTime",
                                            {"params": [{"id": key, "uint64Info": Y}]})
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr09, value,Y)

    @allure.title("遍历_设置所有座椅通风时间_0-59min")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1716508?projectId=46')
    @pytest.mark.full
    def test_caseid_1939958(self):
        info ={0:'HmiSeatClimaTmrHmiSeatVentnFirstLeTmr', 1:'HmiSeatClimaTmrHmiSeatVentnFirstRiTmr',
                4:'HmiSeatClimaTmrHmiSeatVentnSecLeTmr', 6:'HmiSeatClimaTmrHmiSeatVentnSecRiTmr'}
        for key,value in info.items():
             for Y in [0, 30, 59]:
                logger.info(f"---座椅{key}--请求{Y}--")
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingTime",
                                            {"params": [{"id": key, "uint64Info": Y}]})
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr09, value,Y)

    @allure.title("主驾座椅姿态设置所有位置_禁用scene1_模式限制")
    @pytest.mark.sanity
    def test_caseid_105483(self):
        positionSet = [{1:{"backAngle": 160, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置高度1向上，水平1向前
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {3:{"backAngle": 104, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置靠背1向前，腿托1向上
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {2:{"backAngle": 104, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置高度2向下，水平2向后
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {4:{"backAngle": 160, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置靠背2向后，腿托2向下
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}]
        self.set_Drvrseat_condition_allow()
        for positionSet1 in positionSet:
            for key,value in positionSet1.items():
                for carmode in [1,2,3]:
                    logger.info(f"--处于主驾位置{key}--准备切换车辆模式为{carmode}")
                    eval(f"self.set_drvr_position{key}()")#包括两个位置方便调用以上四个方向
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                    {"params": {"id": 0,"position": value}},{"out": 1})
                    if key==1 :
                        self.check_drvrseat_heightsld_adjust(1,1)
                    elif key==3 :
                        self.check_drvrseat_kaotuituo_adjust(1,1)
                    elif key==2 :
                        self.check_drvrseat_heightsld_adjust(2,2)
                    elif key==4 :
                        self.check_drvrseat_kaotuituo_adjust(2,2)
                    self.sd_tester.change_car_mode(carmode)
                    self.check_Drvrseat_direction_not_send()
                    self.sd_tester.change_car_mode(0)
        for carmode in [1,2,3]:
            for key,value in positionSet1.items():
                self.sd_tester.change_car_mode(carmode)
                logger.info(f"--处于主驾位置{key}--切换车辆模式为{carmode}")
                eval(f"self.set_drvr_position{key}()")#包括两个位置方便调用以上四个方向
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                    {"params": {"id": 0,"position": value}},{"out": 0})
                self.check_Drvrseat_direction_not_send() 

    @allure.title("副驾座椅姿态设置所有位置_禁用scene1_模式限制")
    @pytest.mark.sanity
    def test_caseid_1980469(self):
        positionSet = [{1:{"backAngle": 160, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置高度1向上，水平1向前
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {3:{"backAngle": 104, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置靠背1向前，腿托1向上
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {2:{"backAngle": 104, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置高度2向下，水平2向后
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {4:{"backAngle": 160, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置靠背2向后，腿托2向下
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}]
        self.set_Drvrseat_condition_allow()
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 0)
        # self.dk.set_cenlock_sts(0x1)
        self.partner.empty_all(0.5)
        for positionSet1 in positionSet:
            for key,value in positionSet1.items():
                for carmode in [1,2,3]:
                    logger.info(f"--处于副驾位置{key}--准备切换车辆模式为{carmode}")
                    eval(f"self.set_Pass_position{key}()")#包括两个位置方便调用以上四个方向
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                    {"params": {"id": 1,"position": value}},{"out": 1})
                    if key==1 :
                        self.check_Passseat_heightsld_adjust(1,1)
                    elif key==3 :
                        self.check_Passseat_kaotuituo_adjust(1,1)
                    elif key==2 :
                        self.check_Passseat_heightsld_adjust(2,2)
                    elif key==4 :
                        self.check_Passseat_kaotuituo_adjust(2,2)
                    self.sd_tester.change_car_mode(carmode)
                    self.check_Passseat_direction_not_send()
                    self.sd_tester.change_car_mode(0)
        for carmode in [1,2,3]:
            for key,value in positionSet1.items():
                self.sd_tester.change_car_mode(carmode)
                logger.info(f"--处于副驾位置{key}--切换车辆模式为{carmode}")
                eval(f"self.set_Pass_position{key}()")#包括两个位置方便调用以上四个方向
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                    {"params": {"id": 1,"position": value}},{"out": 0})
                self.check_Passseat_direction_not_send() 

    @allure.title("副驾座椅姿态设置所有位置_禁用scene2_本地按键按下")
    @pytest.mark.sanity
    def test_caseid_1980470(self):
        positionSet = [{1:{"backAngle": 180, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置高度1向上，水平1向前
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {3:{"backAngle": 0, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置靠背1向前，腿托1向上
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {2:{"backAngle": 0, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置高度2向下，水平2向后
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {4:{"backAngle": 180, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置靠背2向后，腿托2向下
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}]
        self.set_Passseat_condition_allow()
        self.partner.empty_all(0.5)
        for positionSet1 in positionSet:
            for key,value in positionSet1.items():
                    logger.info(f"--处于副驾位置{key}--准备本地按键按下")
                    eval(f"self.set_Pass_position{key}()")#包括两个位置方便调用以上四个方向
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                    {"params": {"id": 1,"position": value}},{"out": 1})
                    if key==1 :
                        self.check_Passseat_heightsld_adjust(1,1)
                    elif key==3 :
                        self.check_Passseat_kaotuituo_adjust(1,1)
                    elif key==2 :
                        self.check_Passseat_heightsld_adjust(2,2)
                    elif key==4 :
                        self.check_Passseat_kaotuituo_adjust(2,2)
                    self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 1)
                    sleep(0.5)
                    self.check_Passseat_direction_not_send()
                    self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 0)
                    sleep(0.5)
        for key,value in positionSet1.items():
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 1)
            sleep(0.5)
            eval(f"self.set_Pass_position{key}()")#包括两个位置方便调用以上四个方向
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                {"params": {"id": 1,"position": value}},{"out": 0})
            self.check_Passseat_direction_not_send() 

    @allure.title("主驾座椅姿态设置所有位置_禁用scene2_本地按键限制")
    @pytest.mark.sanity
    def test_caseid_1980430(self):
        positionSet = [{1:{"backAngle": 180, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置高度1向上，水平1向前
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {3:{"backAngle": 0, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置靠背1向前，腿托1向上
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {2:{"backAngle": 0, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置高度2向下，水平2向后
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {4:{"backAngle": 180, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置靠背2向后，腿托2向下
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}]
        self.set_Drvrseat_condition_allow()
        for positionSet1 in positionSet:
            for key,value in positionSet1.items():
                    logger.info(f"--处于主驾位置{key}--准备按下本地开关")
                    eval(f"self.set_drvr_position{key}()")#包括两个位置方便调用以上四个方向
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                    {"params": {"id": 0,"position": value}},{"out": 1})
                    if key==1 :
                        self.check_drvrseat_heightsld_adjust(1,1)
                    elif key==3 :
                        self.check_drvrseat_kaotuituo_adjust(1,1)
                    elif key==2 :
                        self.check_drvrseat_heightsld_adjust(2,2)
                    elif key==4 :
                        self.check_drvrseat_kaotuituo_adjust(2,2)
                    self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatBtnPsd', 1)
                    sleep(1)
                    self.check_Drvrseat_direction_not_send()
                    self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatBtnPsd', 0)
                    sleep(1)
                    self.check_Drvrseat_direction_not_send()
        for positionSet1 in positionSet:
            for key,value in positionSet1.items():
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatBtnPsd', 1)
                sleep(1)
                logger.info(f"--处于主驾位置{key}--本地按键已按下")
                eval(f"self.set_drvr_position{key}()")#包括两个位置方便调用以上四个方向
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                    {"params": {"id": 0,"position": value}},{"out": 0})
                self.check_Drvrseat_direction_not_send() #http://172.18.128.7:8080/2023_11_27_15_24_49

    @allure.title("主驾座椅姿态设置所有位置_禁用scene3_座椅不可调限制")
    @pytest.mark.sanity
    def test_caseid_1980432(self):
        positionSet = [{1:{"backAngle": 160, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置高度1向上，水平1向前
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {3:{"backAngle": 104, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置靠背1向前，腿托1向上
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {2:{"backAngle": 104, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置高度2向下，水平2向后
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {4:{"backAngle": 160, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置靠背2向后，腿托2向下
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}]
        self.set_Drvrseat_condition_allow()
        for positionSet1 in positionSet:
            for key,value in positionSet1.items():
                    logger.info(f"--处于主驾位置{key}--准备座椅不可调")
                    eval(f"self.set_drvr_position{key}()")#包括两个位置方便调用以上四个方向
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                    {"params": {"id": 0,"position": value}},{"out": 1})
                    if key==1 :
                        self.check_drvrseat_heightsld_adjust(1,1)
                    elif key==3 :
                        self.check_drvrseat_kaotuituo_adjust(1,1)
                    elif key==2 :
                        self.check_drvrseat_heightsld_adjust(2,2)
                    elif key==4 :
                        self.check_drvrseat_kaotuituo_adjust(2,2)
                    self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 0)
                    sleep(1)
                    self.check_Drvrseat_direction_not_send()
                    self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 1)
                    sleep(1)
                    self.check_Drvrseat_direction_not_send()
        for positionSet1 in positionSet:
            for key,value in positionSet1.items():
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 0)
                sleep(1)
                logger.info(f"--处于主驾位置{key}--座椅已经不可调")
                eval(f"self.set_drvr_position{key}()")#包括两个位置方便调用以上四个方向
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                    {"params": {"id": 0,"position": value}},{"out": 0})
                self.check_Drvrseat_direction_not_send() # http://172.18.128.7:8080/2023_11_27_15_42_27

    @allure.title("主驾座椅姿态设置所有位置_禁用scene4_车速限制")
    @pytest.mark.sanity
    def test_caseid_1980434(self):
        positionSet = [{1:{"backAngle": 160, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置高度1向上，水平1向前
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {3:{"backAngle": 104, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置靠背1向前，腿托1向上
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {2:{"backAngle": 104, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置高度2向下，水平2向后
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {4:{"backAngle": 160, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置靠背2向后，腿托2向下
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}]
        self.set_Drvrseat_condition_allow()
        for positionSet1 in positionSet:
            for key,value in positionSet1.items():
                    logger.info(f"--处于主驾位置{key}--准备表显速度大于5")
                    eval(f"self.set_drvr_position{key}()")#包括两个位置方便调用以上四个方向
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                    {"params": {"id": 0,"position": value}},{"out": 1})
                    if key==1 :
                        self.check_drvrseat_heightsld_adjust(1,1)
                    elif key==3 :
                        self.check_drvrseat_kaotuituo_adjust(1,1)
                    elif key==2 :
                        self.check_drvrseat_heightsld_adjust(2,2)
                    elif key==4 :
                        self.check_drvrseat_kaotuituo_adjust(2,2)
                    self.set_vehicle_speed(1.4)
                    self.check_Drvrseat_direction_not_send()
                    self.set_vehicle_speed(1.0)
                    self.check_Drvrseat_direction_not_send()
        for positionSet1 in positionSet:
            for key,value in positionSet1.items():
                self.set_vehicle_speed(1.4)
                logger.info(f"--处于主驾位置{key}--表显车速大于5km/h")
                eval(f"self.set_drvr_position{key}()")#包括两个位置方便调用以上四个方向
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                    {"params": {"id": 0,"position": value}},{"out": 0})
                self.check_Drvrseat_direction_not_send() # http://172.18.128.7:8080/2023_11_27_15_59_39

    @allure.title("主驾座椅姿态设置所有位置_QF不等于3时_无需控制")
    @pytest.mark.sanity
    def test_caseid_1980440(self):
        self.set_Drvrseat_condition_allow()
        self.set_drvr_position1()
        for X in [0,1,2]:
            self.set_drvr_position1Valid(X,X,X) #3个部位无效
            logger.info(f"--3个QF都为{X}")
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                              {"params": {"id": 0,
                                                          "position": {"backAngle": 0, "longitudinalPosition": 100,
                                                                       "verticalPosition": 100,
                                                                       "LegrestVerticalPosition": 100,
                                                                       "backAngleIsValid": True,
                                                                       "longitudinalIsValid": True,
                                                                       "verticalIsValid": True,
                                                                       "legrestVerticalIsValid": True}}},{"out": 1})
            self.check_drvrseat_adjust(0,1,0,0)
        for Y in [0,1,2]:
            self.set_drvr_position1Valid(Y,3,Y) #高度前后无效
            logger.info(f"--高度前后QF都为{Y}")
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                              {"params": {"id": 0,
                                                          "position": {"backAngle": 0, "longitudinalPosition": 100,
                                                                       "verticalPosition": 100,
                                                                       "LegrestVerticalPosition": 100,
                                                                       "backAngleIsValid": True,
                                                                       "longitudinalIsValid": True,
                                                                       "verticalIsValid": True,
                                                                       "legrestVerticalIsValid": True}}},{"out": 1})
            self.check_drvrseat_adjust(0,1,1,0)

    @allure.title("副驾座椅姿态设置所有位置_QF不等于3时_无需控制")
    @pytest.mark.sanity
    def test_caseid_1980476(self):
        self.set_Passseat_condition_allow()
        self.set_Pass_position1()
        for X in [0,1,2]:
            self.set_Pass_position1Valid(X,X,X) #3个部位无效
            logger.info(f"--3个QF都为{X}")
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                              {"params": {"id": 1,
                                                          "position": {"backAngle": 0, "longitudinalPosition": 100,
                                                                       "verticalPosition": 100,
                                                                       "LegrestVerticalPosition": 100,
                                                                       "backAngleIsValid": True,
                                                                       "longitudinalIsValid": True,
                                                                       "verticalIsValid": True,
                                                                       "legrestVerticalIsValid": True}}},{"out": 1})
            self.check_Passseat_adjust(0,1,0,0)
        for Y in [0,1,2]:
            self.set_Pass_position1Valid(Y,3,3) #高度无效
            logger.info(f"--高度QF都为{Y}")
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                              {"params": {"id": 1,
                                                          "position": {"backAngle": 0, "longitudinalPosition": 100,
                                                                       "verticalPosition": 100,
                                                                       "LegrestVerticalPosition": 100,
                                                                       "backAngleIsValid": True,
                                                                       "longitudinalIsValid": True,
                                                                       "verticalIsValid": True,
                                                                       "legrestVerticalIsValid": True}}},{"out": 1})
            self.check_Passseat_adjust(1,1,0,0)#腿托调节无效

    @allure.title("主驾座椅姿态设置所有位置_4个方向调节")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1716361?projectId=46')
    @pytest.mark.sanity
    def test_caseid_1979791(self):
        self.set_Drvrseat_condition_allow()
        self.set_drvr_position1()
        sleep(1)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                              {"params": {"id": 0,
                                                          "position": {"backAngle": 50, "longitudinalPosition": 20,
                                                                       "verticalPosition": 50,
                                                                       "LegrestVerticalPosition": 100,
                                                                       "backAngleIsValid": True,
                                                                       "longitudinalIsValid": True,
                                                                       "verticalIsValid": True,
                                                                       "legrestVerticalIsValid": True}}},
                                              {"out": 1})
        self.check_drvrseat_adjust(1,0,0,1)
        self.set_drvr_heiperc(50.0)
        self.set_drvr_sldperc(20.0)
        sleep(1)
        self.check_drvrseat_adjust(0,1,1,0)
        self.set_drvr_angelperc(50.0)
        self.set_drvr_frontheiperc(100.0)
        sleep(0.5) #http://172.18.128.7:8080/2023_11_27_18_02_03
        self.check_drvrseat_adjust(0,0,0,0)

    @allure.title("副驾座椅姿态设置所有位置_4个方向调节")
    @pytest.mark.sanity
    def test_caseid_1979787(self):
        self.pass_position_stop()
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StopMoveDirection',
                                                {"id": 1, "part": 1, "direction": 0})
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StopMoveDirection',
                                                {"id": 1, "part": 0, "direction": 0})
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StopMoveDirection',
                                                {"id": 1, "part": 1, "direction": 2})
        self.set_Passseat_condition_allow()
        self.set_Pass_position1()
        sleep(1)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                              {"params": {"id": 1,
                                                          "position": {"backAngle": 50, "longitudinalPosition": 20,
                                                                       "verticalPosition": 50,
                                                                       "LegrestVerticalPosition": 100,
                                                                       "backAngleIsValid": True,
                                                                       "longitudinalIsValid": True,
                                                                       "verticalIsValid": True,
                                                                       "legrestVerticalIsValid": True}}},
                                              {"out": 1})
        self.check_Passseat_adjust(1,0,0,1)
        self.set_pass_heiperc(50.0)
        self.set_pass_sldperc(20.0)
        sleep(1)
        self.check_Passseat_adjust(0,1,1,0)
        self.set_pass_angelperc(50.0)
        self.set_pass_frontheiperc(100.0)
        sleep(0.5) 
        self.check_Passseat_adjust(0,0,0,0)

    @allure.title("主驾座椅姿态设置所有位置_两次调用间隔160ms")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1716361?projectId=46')
    @pytest.mark.sanity
    def test_caseid_1980460(self):
        self.set_Drvrseat_condition_allow()
        self.set_drvr_position1()
        sleep(1)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                              {"params": {"id": 0,
                                                          "position": {"backAngle": 50, "longitudinalPosition": 20,
                                                                       "verticalPosition": 50,
                                                                       "LegrestVerticalPosition": 100,
                                                                       "backAngleIsValid": True,
                                                                       "longitudinalIsValid": True,
                                                                       "verticalIsValid": True,
                                                                       "legrestVerticalIsValid": True}}},
                                              {"out": 1})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                              {"params": {"id": 0,
                                                          "position": {"backAngle": 50, "longitudinalPosition": 20,
                                                                       "verticalPosition": 50,
                                                                       "LegrestVerticalPosition": 100,
                                                                       "backAngleIsValid": True,
                                                                       "longitudinalIsValid": True,
                                                                       "verticalIsValid": True,
                                                                       "legrestVerticalIsValid": True}}},
                                              {"out": 1})
        self.check_drvrseat_adjust(1,0,0,1)
        self.set_drvr_heiperc(50.0)
        self.set_drvr_sldperc(20.0)
        sleep(1)
        self.check_drvrseat_adjust(0,1,1,0)
        self.set_drvr_angelperc(50.0)
        self.set_drvr_frontheiperc(100.0)
        sleep(0.5) #http://172.18.128.7:8080/2023_11_27_18_02_03
        self.check_drvrseat_adjust(0,0,0,0)

    @allure.title("副驾座椅姿态设置所有位置_两次调用间隔160ms")
    @pytest.mark.sanity
    def test_caseid_1980484(self):
        self.pass_position_stop()
        self.set_Pass_position1()
        self.set_Passseat_condition_allow()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                              {"params": {"id": 1,
                                                          "position": {"backAngle": 50, "longitudinalPosition": 20,
                                                                       "verticalPosition": 50,
                                                                       "LegrestVerticalPosition": 100,
                                                                       "backAngleIsValid": True,
                                                                       "longitudinalIsValid": True,
                                                                       "verticalIsValid": True,
                                                                       "legrestVerticalIsValid": True}}},
                                              {"out": 1})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                              {"params": {"id": 1,
                                                          "position": {"backAngle": 50, "longitudinalPosition": 20,
                                                                       "verticalPosition": 50,
                                                                       "LegrestVerticalPosition": 100,
                                                                       "backAngleIsValid": True,
                                                                       "longitudinalIsValid": True,
                                                                       "verticalIsValid": True,
                                                                       "legrestVerticalIsValid": True}}},
                                              {"out": 1})
        self.check_Passseat_adjust(1,0,0,1)
        self.set_pass_heiperc(50.0)
        self.set_pass_sldperc(20.0)
        sleep(1)
        self.check_Passseat_adjust(0,1,1,0)
        self.set_pass_angelperc(50.0)
        self.set_pass_frontheiperc(100.0)
        sleep(0.5) 
        self.check_Passseat_adjust(0,0,0,0)
  
    @allure.title("主驾座椅姿态设置所有位置_各个位置超时恢复")
    @pytest.mark.sanity
    def test_caseid_1980448(self):
        positionSet = [{1:{"backAngle": 180, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置高度1向上，水平1向前
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {3:{"backAngle": 0, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置靠背1向前，腿托1向上
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}]
        self.set_Drvrseat_condition_allow()
        for positionSet1 in positionSet:
            for key,value in positionSet1.items():
                    logger.info(f"--处于主驾位置{key}")
                    eval(f"self.set_drvr_position{key}()")#一个固定位置调节四个方向
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                    {"params": {"id": 0,"position": value}},{"out": 1})
                    if key==1 :
                        self.check_drvrseat_heightsld_adjust(1,1)
                        sleep(15)
                        self.check_drvrseat_heightsld_adjust(1,1)
                        sleep(6) #两个都是20s超时
                        self.check_drvrseat_heightsld_adjust(0,0)
                    elif key==3 :
                        self.check_drvrseat_kaotuituo_adjust(1,1)
                        sleep(7)
                        self.check_drvrseat_kaotuituo_adjust(1,1)
                        sleep(4) #坐垫10s超时引起所有超时
                        self.check_Drvrseat_direction_not_send()

    @allure.title("副驾座椅姿态设置所有位置_各个位置超时恢复")
    @pytest.mark.sanity
    def test_caseid_1980478(self):
        positionSet = [{1:{"backAngle": 180, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置高度1向上，水平1向前
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {3:{"backAngle": 0, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置靠背1向前，腿托1向上
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}]
        self.set_Passseat_condition_allow()
        for positionSet1 in positionSet:
            for key,value in positionSet1.items():
                    logger.info(f"--处于副驾位置{key}")
                    eval(f"self.set_Pass_position{key}()")#一个固定位置调节四个方向
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                    {"params": {"id": 1,"position": value}},{"out": 1})
                    if key==1 :
                        self.check_Passseat_heightsld_adjust(1,1)
                        sleep(15)
                        self.check_Passseat_heightsld_adjust(1,1)
                        sleep(6) #两个都是20s超时
                        self.check_Passseat_heightsld_adjust(0,0)
                    elif key==3 :
                        self.check_Passseat_kaotuituo_adjust(1,1)
                        sleep(7)
                        self.check_Passseat_kaotuituo_adjust(1,1)
                        sleep(4) #坐垫10s超时引起所有超时
                        self.check_Passseat_direction_not_send()

    @allure.title("主驾座椅姿态设置所有位置_异常处理_单个方向停止控制")
    @pytest.mark.sanity
    def test_caseid_1980456(self):
        self.set_Drvrseat_condition_allow()
        self.set_drvr_position1()
        sleep(1)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                              {"params": {"id": 0,
                                                          "position": {"backAngle": 50, "longitudinalPosition": 20,
                                                                       "verticalPosition": 50,
                                                                       "LegrestVerticalPosition": 100,
                                                                       "backAngleIsValid": True,
                                                                       "longitudinalIsValid": True,
                                                                       "verticalIsValid": True,
                                                                       "legrestVerticalIsValid": True}}},
                                              {"out": 1})
        self.check_drvrseat_adjust(1,0,0,1)
        self.set_drvr_heiperc(52.0)
        self.set_drvr_sldperc(22.0)
        sleep(1)
        self.check_drvrseat_adjust(0,1,1,0)
        self.set_drvr_angelperc(48.0)
        self.set_drvr_frontheiperc(99.0)
        sleep(0.5) #http://172.18.128.7:8080/2023_11_28_15_05_36
        self.check_drvrseat_adjust(0,0,0,0)

    @allure.title("副驾座椅姿态设置所有位置_异常处理_单个方向停止控制")
    @pytest.mark.sanity
    def test_caseid_1980481(self):
        self.set_Pass_position1()
        self.set_Passseat_condition_allow()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                              {"params": {"id": 1,
                                                          "position": {"backAngle": 50, "longitudinalPosition": 20,
                                                                       "verticalPosition": 50,
                                                                       "LegrestVerticalPosition": 100,
                                                                       "backAngleIsValid": True,
                                                                       "longitudinalIsValid": True,
                                                                       "verticalIsValid": True,
                                                                       "legrestVerticalIsValid": True}}},
                                              {"out": 1})
        self.check_Passseat_adjust(1,0,0,1)
        self.set_pass_heiperc(52.0)
        self.set_pass_sldperc(22.0)
        sleep(1)
        self.check_Passseat_adjust(0,1,1,0)
        self.set_pass_angelperc(48.0)
        self.set_pass_frontheiperc(99.0)
        sleep(0.5) 
        self.check_Passseat_adjust(0,0,0,0)
                    
    @allure.title("主驾座椅姿态设置所有位置_仲裁处理_调用副驾接口或主驾腰托不应该打断")
    @pytest.mark.sanity
    def test_caseid_1980458(self):
        positionSet = [{1:{"backAngle": 180, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置高度1向上，水平1向前
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {3:{"backAngle": 0, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置靠背1向前，腿托1向上
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}]
        self.set_Drvrseat_condition_allow()
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 0)
        sleep(0.5)
        for positionSet1 in positionSet:
            for key,value in positionSet1.items():
                    logger.info(f"--处于主驾位置{key}-")
                    eval(f"self.set_drvr_position{key}()")#同一个位置方便调用以上四个方向
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                    {"params": {"id": 0,"position": value}},{"out": 1})
                    if key==1 :
                        self.check_drvrseat_heightsld_adjust(1,1)
                        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 1, "part": 1, "direction": 0}, timeout=0.2)
                        sleep(0.2)
                        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 0, "part": 3, "direction": 3}, timeout=0.2)
                        sleep(0.2)
                        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StopMoveDirection',
                                                {"id": 1, "part": 1, "direction": 0})
                        self.check_drvrseat_heightsld_adjust(1,1)
                    elif key==3 :
                        self.check_drvrseat_kaotuituo_adjust(1,1)
                        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 1, "part": 1, "direction": 1}, timeout=0.2)
                        sleep(0.2)
                        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 0, "part": 3, "direction": 2}, timeout=0.2)
                        sleep(0.2)
                        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StopMoveDirection',
                                                {"id": 1, "part": 1, "direction": 1})
                        self.check_drvrseat_kaotuituo_adjust(1,1)

    @allure.title("副驾座椅姿态设置所有位置_仲裁处理_调用主驾接口或副驾腰托不应该打断")
    @pytest.mark.sanity
    def test_caseid_1980482(self):
        positionSet = [{1:{"backAngle": 180, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置高度1向上，水平1向前
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {3:{"backAngle": 0, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置靠背1向前，腿托1向上
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}]
        self.set_Passseat_condition_allow()
        sleep(0.5)
        for positionSet1 in positionSet:
            for key,value in positionSet1.items():
                    logger.info(f"--处于副驾位置{key}-")
                    eval(f"self.set_Pass_position{key}()")#同一个位置方便调用以上四个方向
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                    {"params": {"id": 1,"position": value}},{"out": 1})
                    if key==1 :
                        self.check_Passseat_heightsld_adjust(1,1)
                        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 0, "part": 1, "direction": 0}, timeout=0.2)
                        sleep(0.2)
                        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 1, "part": 3, "direction": 3}, timeout=0.2)
                        sleep(0.2)
                        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StopMoveDirection',
                                                {"id": 0, "part": 1, "direction": 0})
                        self.check_Passseat_heightsld_adjust(1,1)
                    elif key==3 :
                        self.check_Passseat_kaotuituo_adjust(1,1)
                        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 0, "part": 1, "direction": 1}, timeout=0.2)
                        sleep(0.2)
                        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 1, "part": 3, "direction": 2}, timeout=0.2)
                        sleep(0.2)
                        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StopMoveDirection',
                                                {"id": 0, "part": 1, "direction": 1})
                        self.check_Passseat_kaotuituo_adjust(1,1)

    @allure.title("主驾座椅姿态设置所有位置_仲裁处理_调用主驾接口应该打断")
    @pytest.mark.sanity
    def test_caseid_1980459(self):
        positionSet = [{1:{"backAngle": 180, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置高度1向上，水平1向前
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {3:{"backAngle": 0, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置靠背1向前，腿托1向上
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {2:{"backAngle": 0, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置高度2向下，水平2向后
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {4:{"backAngle": 180, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置靠背2向后，腿托2向下
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}]
        self.set_Drvrseat_condition_allow()
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 0)
        sleep(0.5)
        for positionSet1 in positionSet:
            for key,value in positionSet1.items():
                    logger.info(f"--处于主驾位置{key}-")
                    eval(f"self.set_drvr_position{key}()")#同一个位置方便调用以上四个方向
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                    {"params": {"id": 0,"position": value}},{"out": 1})
                    if key==1 :
                        self.check_drvrseat_heightsld_adjust(1,1) 
                        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 0, "part": 0, "direction": 0}, timeout=0.2)#调用前后打断
                        self.check_Drvrseat_direction_not_send(a=0,b=1,c=0,d=0)
                        
                    elif key==3 :
                        self.check_drvrseat_kaotuituo_adjust(1,1)
                        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StopMoveDirection',
                                                {"id": 0, "part": 1, "direction": 0})#调用靠背打断
                        self.check_Drvrseat_direction_not_send(a=0,b=0,c=0,d=0)
                    elif key==2 :
                        self.check_drvrseat_heightsld_adjust(2,2)
                        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 0, "part": 1, "direction": 3}, timeout=0.2)#调用靠背打断
                        self.check_Drvrseat_direction_not_send(a=0,b=0,c=2,d=0)
                    elif key==4 :
                        self.check_drvrseat_kaotuituo_adjust(2,2)
                        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StopMoveDirection',
                                                {"id": 0, "part": 2, "direction": 5})#调用腿托打断
                        self.check_Drvrseat_direction_not_send(a=0,b=0,c=0,d=0)

    @allure.title("副驾座椅姿态设置所有位置_仲裁处理_调用副驾接口应该打断")
    @pytest.mark.sanity
    def test_caseid_1980483(self):
        positionSet = [{1:{"backAngle": 180, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置高度1向上，水平1向前
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {3:{"backAngle": 0, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置靠背1向前，腿托1向上
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {2:{"backAngle": 0, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置高度2向下，水平2向后
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {4:{"backAngle": 180, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置靠背2向后，腿托2向下
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}]
        self.set_Passseat_condition_allow()
        for positionSet1 in positionSet:
            for key,value in positionSet1.items():
                    logger.info(f"--处于副驾位置{key}-")
                    eval(f"self.set_Pass_position{key}()")#同一个位置方便调用以上四个方向
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                    {"params": {"id": 1,"position": value}},{"out": 1})
                    if key==1 :
                        self.check_Passseat_heightsld_adjust(1,1) 
                        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 1, "part": 0, "direction": 0}, timeout=0.2)#调用前后打断
                        self.check_Passseat_direction_not_send(a=0,b=0,c=1,d=0)
                    elif key==3 :
                        self.check_Passseat_kaotuituo_adjust(1,1)
                        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StopMoveDirection',
                                                {"id": 1, "part": 1, "direction": 0})#调用靠背打断
                        self.check_Passseat_direction_not_send(a=0,b=0,c=0,d=0)
                    elif key==2 :
                        self.check_Passseat_heightsld_adjust(2,2)
                        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 1, "part": 1, "direction": 3}, timeout=0.2)#调用靠背打断
                        self.check_Passseat_direction_not_send(a=2,b=0,c=0,d=0)
                    elif key==4 :
                        self.check_Passseat_kaotuituo_adjust(2,2)
                        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StopMoveDirection',
                                                {"id": 1, "part": 2, "direction": 5})#调用腿托打断
                        self.check_Passseat_direction_not_send(a=0,b=0,c=0,d=0)

    @allure.title("停止座椅调节_主副驾所有位置都停止调节")
    @pytest.mark.sanity
    def test_caseid_1980466(self):
        list1 = [{0:0},{1:0},{0:1},{1:1},{0:2}]
        list2 = [0,3,2,5]
        self.set_Drvrseat_condition_allow()
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 0)
        for ke in list1:
            for key,value in ke.items():
                for direction1 in list2:
                    logger.info(f"--座椅{key}-部位{value}--指令{direction1}")
                    self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                        {"id": key, "part": value, "direction": direction1}, timeout=0.2)
                    sleep(1)
                    self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StopMoveDirection',
                                                        {"id": key, "part": value, "direction": direction1}, timeout=0.2)
                    if key == 0:
                        self.check_Drvrseat_direction_not_send()
                    if key == 1:
                        self.check_Passseat_direction_not_send()

    @allure.title("副驾座椅不同部位调节禁用scene1_模式限制")
    @pytest.mark.sanity
    def test_caseid_1980414(self):
        def result(part,direction):  #以下列表中的数分别代表前后、高度、靠背、腿托预留的调节信号  
            if part == 0 :
                if direction ==0:
                    return [1,0,0,0]
                elif direction ==3:
                    return [2,0,0,0]
                elif direction ==2:
                    return [0,1,0,0]
                elif direction ==5:
                    return [0,2,0,0]
            elif part == 1:
                if direction ==0:
                    return [0,0,1,0]
                elif direction ==3:
                    return [0,0,2,0]
                else:
                    return[0,0,0,0]
            elif part == 2 :
                if direction ==2:
                    return [0,0,0,1]
                elif direction ==5:
                    return [0,0,0,2]
                else:
                    return[0,0,0,0]
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 1)
        # self.dk.set_cenlock_sts(0x1)
        self.partner.empty_all(0.5)
        for path in [0,1,2]:
            for direction1 in [0,2,3,5]: 
                for carmode in [1,2,3]: #校验每个部位每个方向都从车辆模式0切到1、2、3
                    self.set_Passseat_condition_allow()
                    logger.info(f"--部位{path}方向正常发送{direction1}")
                    self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 1, "part": path, "direction": direction1}, timeout=0.2)
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstPass',result(path,direction1)[0], timeout=0.5)
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatHeiAdjmtRowFirstPass',result(path,direction1)[1], timeout=0.5)
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatCushTiltAdjmtRowFirstPass', result(path,direction1)[3], timeout=0.5)
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'BackRestAdjmtRowFirstPass',result(path,direction1)[2], timeout=0.5)
                    self.sd_tester.change_car_mode(carmode) #在遍历每个方向时将模式切为非0和5
                    logger.info(f"--部位{path}方向正常发送{direction1}--车辆模式从0切为{carmode}")
                    self.check_Passseat_direction_not_send()
                    self.set_vehicle_speed(0.0)
                    self.sd_tester.change_car_mode(0)
                    sleep(1)  
        for carmode2 in [1,2,3]:
            for path in [0,1,2]:
                for direction1 in [0,2,3,5]: 
                    self.set_vehicle_speed(0.0)
                    self.sd_tester.change_car_mode(carmode2) #前提条件为车辆模式1，2，3
                    self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 1, "part": path, "direction": direction1}, timeout=0.2)
                    logger.info(f"--车辆模在{carmode2}下-部位{path}发送{direction1}不能下发-")
                    self.check_Passseat_direction_not_send()

    @allure.title("副驾座椅不同部位调节禁用scene2_本地开关按下限制")
    @pytest.mark.sanity
    def test_caseid_1980415(self):
        def result(part,direction):  #以下列表中的数分别代表前后、高度、靠背、腿托预留的调节信号  
            if part == 0 :
                if direction ==0:
                    return [1,0,0,0]
                elif direction ==3:
                    return [2,0,0,0]
                elif direction ==2:
                    return [0,1,0,0]
                elif direction ==5:
                    return [0,2,0,0]
            elif part == 1:
                if direction ==0:
                    return [0,0,1,0]
                elif direction ==3:
                    return [0,0,2,0]
                else:
                    return[0,0,0,0]
            elif part == 2 :
                if direction ==2:
                    return [0,0,0,1]
                elif direction ==5:
                    return [0,0,0,2]
                else:
                    return[0,0,0,0]
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 1)
        self.partner.empty_all(0.5)
        for path in [0,1,2]:
            for direction1 in [0,2,3,5]: 
                self.set_Passseat_condition_allow()
                logger.info(f"--部位{path}方向正常发送{direction1}")
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                            {"id": 1, "part": path, "direction": direction1}, timeout=0.2)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstPass',result(path,direction1)[0], timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatHeiAdjmtRowFirstPass',result(path,direction1)[1], timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatCushTiltAdjmtRowFirstPass', result(path,direction1)[3], timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'BackRestAdjmtRowFirstPass',result(path,direction1)[2], timeout=0.5)
                self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 1) #遍历每个方向调用时本地开关按下
                sleep(1)
                logger.info(f"--部位{path}方向正常发送{direction1}--本地开关按下")
                self.check_Passseat_direction_not_send()
                self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 0) #遍历每个方向调用时本地开关按下
                sleep(1) 
        for carmode2 in [0,5]:
            for path in [0,1,2]:
                for direction1 in [0,2,3,5]: 
                    self.set_vehicle_speed(0.0)
                    self.sd_tester.change_car_mode(carmode2) #前提条件为车辆模式0，5
                    self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 1) #遍历每个方向调用时本地开关按下
                    sleep(1) #http://172.18.128.7:8080/2023_11_25_14_09_35
                    self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 1, "part": path, "direction": direction1}, timeout=0.2)
                    logger.info(f"--车辆模在{carmode2}下本地开关按下-部位{path}发送{direction1}不能下发-")
                    self.check_Passseat_direction_not_send()

    @allure.title("主驾座椅不同部位调节禁用scene2_本地开关按下限制")
    @pytest.mark.sanity
    def test_caseid_1980411(self):
        def result(part,direction):  #以下列表中的数分别代表前后、高度、靠背、腿托的调节信号  
            if part == 0 :
                if direction ==0:
                    return [1,0,0,0]
                elif direction ==3:
                    return [2,0,0,0]
                elif direction ==2:
                    return [0,1,0,0]
                elif direction ==5:
                    return [0,2,0,0]
            elif part == 1:
                if direction ==0:
                    return [0,0,1,0]
                elif direction ==3:
                    return [0,0,2,0]
                else:
                    return[0,0,0,0]
            elif part == 2 :
                if direction ==2:
                    return [0,0,0,1]
                elif direction ==5:
                    return [0,0,0,2]
                else:
                    return[0,0,0,0]
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 0)
        self.partner.empty_all(0.5)
        self.set_Drvrseat_condition_allow()
        for path in [0,1,2]:
            for direction1 in [0,2,3,5]: 
                    logger.info(f"--部位{path}方向正常发送{direction1}")
                    self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 0, "part": path, "direction": direction1}, timeout=0.2)
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstDrvr',result(path,direction1)[0], timeout=0.5)
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatHeiAdjmtRowFirstDrvr',result(path,direction1)[1], timeout=0.5)
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatCushTiltAdjmtRowFirstDrvr', result(path,direction1)[3], timeout=0.5)
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'BackRestAdjmtRowFirstDrvr',result(path,direction1)[2], timeout=0.5)
                    self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatBtnPsd', 1)
                    sleep(1)
                    logger.info(f"--部位{path}方向正常发送{direction1}--本地开关按下")
                    self.check_Drvrseat_direction_not_send()  #http://172.18.128.7:8080/2023_11_25_13_08_35
                    self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatBtnPsd', 0)
                    sleep(1)  
        for path in [0,1,2]:
            for direction1 in [0,2,3,5]: 
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatBtnPsd', 1)
                sleep(1)
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                            {"id": 0, "part": path, "direction": direction1}, timeout=0.2)
                logger.info(f"--本地开关按下-部位{path}发送{direction1}不能下发-")
                self.check_Drvrseat_direction_not_send()

    @allure.title("主驾座椅不同部位调节禁用scene3_座椅不可调限制")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1751631?projectId=46')
    @pytest.mark.sanity
    def test_caseid_1980412(self):
        def result(part,direction):  #以下列表中的数分别代表前后、高度、靠背、腿托的调节信号  
            if part == 0 :
                if direction ==0:
                    return [1,0,0,0]
                elif direction ==3:
                    return [2,0,0,0]
                elif direction ==2:
                    return [0,1,0,0]
                elif direction ==5:
                    return [0,2,0,0]
            elif part == 1:
                if direction ==0:
                    return [0,0,1,0]
                elif direction ==3:
                    return [0,0,2,0]
                else:
                    return[0,0,0,0]
            elif part == 2 :
                if direction ==2:
                    return [0,0,0,1]
                elif direction ==5:
                    return [0,0,0,2]
                else:
                    return[0,0,0,0]
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 0)
        self.partner.empty_all(0.5)
        self.set_Drvrseat_condition_allow()
        for path in [0,1,2]:
            for direction1 in [0,2,3,5]: 
                    logger.info(f"--部位{path}方向正常发送{direction1}")
                    self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 0, "part": path, "direction": direction1}, timeout=0.2)
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstDrvr',result(path,direction1)[0], timeout=0.5)
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatHeiAdjmtRowFirstDrvr',result(path,direction1)[1], timeout=0.5)
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatCushTiltAdjmtRowFirstDrvr', result(path,direction1)[3], timeout=0.5)
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'BackRestAdjmtRowFirstDrvr',result(path,direction1)[2], timeout=0.5)
                    self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 0)
                    sleep(1)
                    logger.info(f"--部位{path}方向正常发送{direction1}--座椅不可调")
                    self.check_Drvrseat_direction_not_send() #http://172.18.128.7:8080/2023_11_25_13_18_49
                    self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 1)
                    sleep(1)
        for path in [0,1,2]:
            for direction1 in [0,2,3,5]: 
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 0)
                sleep(1)
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                            {"id": 0, "part": path, "direction": direction1}, timeout=0.2)
                logger.info(f"--座椅不可调下-部位{path}发送{direction1}不能下发-")
                self.check_Drvrseat_direction_not_send()

    @allure.title("主驾座椅腰托调节_条件不满足或打断")
    @pytest.mark.sanity
    def test_caseid_1980274(self):
        def hei_REQ(direction):
            if direction == 2:
                return 1
            elif direction == 5:
                return 2
            else:
                return 0
        def Len_REQ(direction):
            if direction == 0:
                return 1
            elif direction == 3:
                return 2
            else:
                return 0
        self.sd_tester.change_car_mode(3) #测试碰撞模式下，腰托依然可调
        for direction1 in [0, 3, 2, 5]:
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0.0)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 1)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatBtnPsd', 1)
            sleep(1)
            logger.info(f"----设置腰托方向{direction1}")
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 0, "part": 3, "direction": direction1}, timeout=0.2)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr54, 'LumHeiAdjmtRowFirstDrvr',0, timeout=1)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr54, 'LumLenAdjmtRowFirstDrvr',0, timeout=1)
        for direction1 in [0, 3, 2, 5]: #测试车速大于5km/h、座椅不可调时腰托也能控制
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 10.0)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 0)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatBtnPsd', 0)
            sleep(1)
            logger.info(f"----设置腰托方向{direction1}")
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 0, "part": 3, "direction": direction1}, timeout=0.2)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr54, 'LumHeiAdjmtRowFirstDrvr',
                                hei_REQ(direction1), timeout=1)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr54, 'LumLenAdjmtRowFirstDrvr',
                                Len_REQ(direction1), timeout=1)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatBtnPsd', 1)
            sleep(1)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr54, 'LumHeiAdjmtRowFirstDrvr',0, timeout=1)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr54, 'LumLenAdjmtRowFirstDrvr',0, timeout=1)

    @allure.title("副驾座椅腰托调节_条件不满足和打断")
    @pytest.mark.sanity
    def test_caseid_1980275(self):
        def hei_REQ(direction):
            if direction == 2:
                return 1
            elif direction == 5:
                return 2
            else:
                return 0
        def Len_REQ(direction):
            if direction == 0:
                return 1
            elif direction == 3:
                return 2
            else:
                return 0
        self.set_Passseat_condition_allow()
        for direction1 in [0, 3, 2, 5]:
            logger.info(f"----设置方向等于={direction1}----")
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 1)
            sleep(1)
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 1, "part": 3, "direction": direction1}, timeout=0.2)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr54, 'LumHeiAdjmtRowFirstPass',0, timeout=1)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr54, 'LumLenAdjmtRowFirstPass',0, timeout=1)
        for direction1 in [0, 3, 2, 5]:
            logger.info(f"----设置方向等于={direction1}----")
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 0)
            sleep(1)
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StartMoveDirection',
                                                {"id": 1, "part": 3, "direction": direction1}, timeout=0.2)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr54, 'LumHeiAdjmtRowFirstPass',
                            hei_REQ(direction1), timeout=1)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr54, 'LumLenAdjmtRowFirstPass',
                            Len_REQ(direction1), timeout=1)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 1)
            sleep(1)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr54, 'LumHeiAdjmtRowFirstPass',0, timeout=1)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr54, 'LumLenAdjmtRowFirstPass',0, timeout=1)

    @allure.title("获取和通知所有自动加热通风状态_打开或关闭下电记忆")
    @pytest.mark.sanity
    @pytest.mark.restart
    def test_caseid_106973(self):
        info = {"SetAutoHeating":"GetAutoHeating","SetAutoVenting":"GetAutoVenting"}
        for status in [True,False]:
            for key,value in info.items():
                logger.info(f"--类型{key}--状态{status}")
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, key, {"params": [{"id": 0, "isOn": status},
                                                                                            {"id": 1, "isOn": status},
                                                                                            {"id": 4, "isOn": status},
                                                                                            {"id": 6, "isOn": status}]}, timeout=1)
            self.ipdu.pause_all_bus_send()
            sleep(2)
            self.nucapp.bgm_power_off()
            sleep(3)
            self.nucapp.bgm_power_on()
            sleep(10)
            self.ipdu.resume_all_bus_send()
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, value, {"seats": [12]},
                                                {"out": [{"id": 0, "isOn": status}, {"id": 1, "isOn": status},
                                                            {"id": 4, "isOn": status}, {"id": 6, "isOn": status}]}, timeout=0.2)
        
    @pytest.mark.restart
    @pytest.mark.sanity
    @allure.title("设置座椅按摩断电重启记忆_遍历")
    def test_caseid_106977(self):
        for id in [0,1]:
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetMassageConf",
                                        {"params": [{"id": id, "conf": {"isOn": True, "type": 2, "intensity": 0}}]})
        self.partner.empty_all(0.5)
        for X in range(8):
            for id1 in [0,1]:
                logger.info(f"--座位{id1}type设置为:{X}")
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetMassageConf",
                                            {"params": [{"id": id1, "conf": {"isOn": True, "type": X}}]})
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrMassgRunng', 1)
                self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassMassgRunng', 1)
                sleep(0.5)#按摩不能为关
                self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "MassageConf",
                                          {"id": id1, "conf": {"isOn": True, "type": X}})
        for index in range(4):
            for id1 in [0,1]:
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetMassageConf",
                                                {"params": [{"id": id1, "conf": {"isOn": True, "type": index,"intensity": index}}]})
            self.ipdu.pause_bus_send("bodycan")
            self.BGM_down_up(2,3,10)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetMassageConf",{"seats": [0,1]},
                                        {"out": [{"id": 0,"conf": {"isOn": False, "type": index, "intensity": index}},
                                                    {"id": 1,"conf": {"isOn": False, "type": index, "intensity": index}}]})
            self.ipdu.resume_bus_send("bodycan")
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrMassgRunng', 1)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassMassgRunng', 1)
            sleep(2)

    @allure.title("获取安全带状态_1.3默认值参数）_默认值")
    @pytest.mark.sanity
    @pytest.mark.restart
    def test_caseid_1919339(self):
        try:
            self.ipdu.pause_bus_send("backbonefr")
            sleep(1)
            self.nucapp.bgm_power_off()
            sleep(3)
            self.nucapp.bgm_power_on()
            sleep(12)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                                  {"out": [{"id": 0, "status": 1}, {"id": 1, "status": 1},
                                                           {"id": 5, "status": 1}, {"id": 4, "status": 1},
                                                           {"id": 6, "status": 1}]})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [0, 1, 4, 5, 6]},
                                                  {"out": [{"id": 0, "status": 1}, {"id": 1, "status": 1},
                                                           {"id": 5, "status": 1}, {"id": 4, "status": 1},
                                                           {"id": 6, "status": 1}]})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [12]},
                                            {"out": [{"value": {"id": 0, "status": 1}, "statusValidity": 0},
                                                      {"value": {"id": 1, "status": 1}, "statusValidity": 0},
                                                      {"value": {"id": 4, "status": 1}, "statusValidity": 0},
                                                      {"value": {"id": 5, "status": 1}, "statusValidity": 0},
                                                      {"value": {"id": 6, "status": 1}, "statusValidity": 0}]})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [0,1,4,5,6]},
                                            {"out": [{"value": {"id": 0, "status": 1}, "statusValidity": 0},
                                                      {"value": {"id": 1, "status": 1}, "statusValidity": 0},
                                                      {"value": {"id": 4, "status": 1}, "statusValidity": 0},
                                                      {"value": {"id": 5, "status": 1}, "statusValidity": 0},
                                                      {"value": {"id": 6, "status": 1}, "statusValidity": 0}]})
        except Exception as error:
            self.ipdu.resume_bus_send("backbonefr")
            assert False, error
        else:
            self.ipdu.resume_bus_send("backbonefr") 

    @allure.title("获取和通知座椅占位状态_初始化后所有座椅其他占位方式触发和恢复")
    @pytest.mark.sanity
    @pytest.mark.restart
    def test_caseid_1980096(self):
        self.ipdu.pause_bus_send("backbonefr")
        self.BGM_down_up(2,3,15)
        self.check_All_seatOccupt_response(255,0,0)
        self.ipdu.resume_bus_send("backbonefr")
        sleep(2)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts' , 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 0) 
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', 0)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyPARemoteStatus",
                                        {"paRemoteStatus": {"paStatus": 0, "lastHandleType": 0, "lastHandleUseatId": 0}})
        sleep(2)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetOccupied", {"seats": [0]},
                                              {"out": [{"seatId": 0, "rawSensorStatus": 0, "status": 0}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetOccupiedValidity", {"seats": [0]},
                                              {"out": [{"value": {"seatId": 0, "rawSensorStatus": 0, "status": 0}},{"statusValidity": 0}]})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 1)
        sleep(0.1)
        self.check_DrvrSeatOccupt_event_response(0,1,0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 0)
        sleep(0.1)
        self.check_DrvrSeatOccupt_event_response(0,0,0)
        for ALLSTATUS in [1,0]:
            logger.info(f"--五个座位占位都发{ALLSTATUS}")
            self.seat_belt_status(ALLSTATUS,ALLSTATUS,ALLSTATUS,ALLSTATUS,ALLSTATUS)
            self.check_four_seatoccupt_event(0,ALLSTATUS,0)
            self.check_All_seatOccupt_response(0,ALLSTATUS,0)

    @allure.title("获取和通知座椅占位状态_所有座椅传感器占位后信号丢失到恢复到未占位")
    @pytest.mark.sanity
    def test_caseid_1980328(self):
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 0) 
        self.seat_belt_status(0,0,0,0,0)
        self.partner.empty_all(1)
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.check_All_seatOccupt_response(1,1,0)
        self.ipdu.pause_bus_send("backbonefr")
        sleep(1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatusValidity", 
                                  {"infos": [{"value": {"seatId": 0, "rawSensorStatus": 1, "status": 1}},{"statusValidity": 4}]})
        sleep(1)
        self.check_five_seatoccuptLoss_event(1,1,4)
        self.check_All_seatOccupt_response(1,1,4)
        self.ipdu.resume_bus_send("backbonefr")
        sleep(2)
        self.check_five_seatoccuptLoss_event(1,1,0)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        #2S内
        self.check_All_seatOccupt_response(0,1,0)
        #2S后
        sleep(2)
        self.check_All_seatOccupt_response(0,0,0)

    @allure.title("获取和通知座椅占位状态_所有座椅传感器未占位后信号丢失到恢复到占位")
    @pytest.mark.sanity
    def test_caseid_1980329(self):
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 0) 
        self.seat_belt_status(0,0,0,0,0)
        self.partner.empty_all(1)
        self.set_four_seat_occupt(0,0,0,0)
        self.check_All_seatOccupt_response(0,0,0)
        self.ipdu.pause_bus_send("backbonefr")
        sleep(1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatusValidity", 
                                  {"infos": [{"value": {"seatId": 0, "rawSensorStatus": 0, "status": 0}},{"statusValidity": 4}]})
        sleep(1)
        self.check_five_seatoccuptLoss_event(0,0,4)
        self.check_All_seatOccupt_response(0,0,4)
        self.ipdu.resume_bus_send("backbonefr")
        sleep(3)
        self.check_five_seatoccuptLoss_event(0,0,0)
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.check_All_seatOccupt_response(1,1,0)

    @allure.title("获取和通知座椅占位状态_所有座椅其他方式占位后信号丢失到恢复")
    @pytest.mark.sanity
    def test_caseid_1980331(self):
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 0) 
        self.seat_belt_status(1,1,1,1,1)
        self.partner.empty_all(1)
        self.check_All_seatOccupt_response(0,1,0)
        self.ipdu.pause_bus_send("backbonefr")
        sleep(1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatusValidity", 
                                  {"infos": [{"value": {"seatId": 0, "rawSensorStatus": 0, "status": 1}},{"statusValidity": 4}]})
        sleep(1)
        self.check_five_seatoccuptLoss_event(0,1,4)
        self.check_All_seatOccupt_response(0,1,4)
        self.ipdu.resume_bus_send("backbonefr")
        sleep(2)
        self.check_five_seatoccuptLoss_event(0,1,0)
        #踩刹车
        self.seat_belt_status(0,1,1,1,1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 1) 
        sleep(0.5)
        self.ipdu.pause_bus_send("backbonefr")
        sleep(1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatusValidity", 
                                  {"infos": [{"value": {"seatId": 0, "rawSensorStatus": 0, "status": 1}},{"statusValidity": 4}]})
        sleep(1)
        self.check_five_seatoccuptLoss_event(0,1,4)
        sleep(0.5)
        self.check_All_seatOccupt_response(0,1,4)
        self.ipdu.resume_bus_send("backbonefr")
        sleep(2)
        self.check_five_seatoccuptLoss_event(0,1,0)

    @allure.title("遍历_获取座椅加热通风时间_下电记忆所有座椅")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_106832(self):
        for X in [0,1,4,6]:
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingTime",
                                            {"params": [{"id": X, "uint64Info": 50}]})
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingTime",
                                            {"params": [{"id": X, "uint64Info": 50}]})
        sleep(1)
        self.ipdu.pause_all_bus_send()
        self.BGM_down_up(2,3,15)
        self.ipdu.resume_all_bus_send()
        sleep(2)
        for Y in ["GetVentingTime","GetHeatingTime"]:
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, Y, {"seats": [3]},
                                                {"out": [{"id":0, "uint64Info": 50},{"id":0, "uint64Info": 50}]})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, Y, {"seats": [7]},
                                                {"out": [{"id":4, "uint64Info": 50},{"id":6, "uint64Info": 50}]})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, Y, {"seats": [12]},
                                                {"out": [{"id":0, "uint64Info": 50},{"id":1, "uint64Info": 50}
                                                            ,{"id":4, "uint64Info": 50},{"id":6, "uint64Info": 50}]})
            
    @allure.title("获取座椅服务所有接口默认值")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_1919343(self):
        self.ipdu.pause_all_bus_send()
        self.BGM_down_up(2,3,10)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltPretensioningWarning",{},
                                              {"out": 0})#安全带预紧
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltEquipStatus",{"seats":[12]},
                                              {"out": [{"id": 4, "uint8Info": 1}, #安全带装配
                                                       {"id": 5, "uint8Info": 1}, {"id": 6, "uint8Info": 1}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning",{"seats":[12]},
                                              {"out": [{"id": 0, "status": 1}, {"id": 1, "status": 1},
                                                       {"id": 5, "status": 1}, {"id": 4, "status": 1},
                                                         {"id": 6, "status": 1}]})#安全带未系
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo",{"seats":[12]},#位置信息
                                              {"out": [{"id": 0, "position": {"backAngle": 0,"longitudinalPosition": 100,
                                            "verticalPosition": 100,"LegrestVerticalPosition": 100, "backAngleIsValid": False,
                                            "longitudinalIsValid": False,  "verticalIsValid": False,"legrestVerticalIsValid": False}},
                                              {"id": 1,"position": {"backAngle": 0, "longitudinalPosition": 100,"verticalPosition": 100,
                                            "LegrestVerticalPosition": 100,"backAngleIsValid": False,"longitudinalIsValid": False, 
                                            "verticalIsValid": False,"legrestVerticalIsValid": False}}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatSwitchStatus",{"seats":[12]},#按键信息
                                              {"out": [{"id": 0, "status": {"verticalPositionSwitch": 0, 
                                            "legrestVerticalPositionSwitch": 0, "longitudinalPositionSwitch": 0,
                                              "backSwitch": 0,  "isLocalSwitchActivated": False,"lumbarLongitudinalPositionSwitch": 0, 
                                              "lumbarVerticalPositionSwitch": 0}},{"id": 1,  "status": {"verticalPositionSwitch": 0,
                                            "legrestVerticalPositionSwitch": 0, "longitudinalPositionSwitch": 0,"backSwitch": 0, 
                                            "isLocalSwitchActivated": False, "lumbarLongitudinalPositionSwitch": 0,
                                            "lumbarVerticalPositionSwitch": 0}}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus",{"seats":[12]},#通风加热状态
                                              {"out": [{"id": 4, "status": {"heatLevel": 0, "heatWorkStatus": 0, 
                                            "ventLevel": 0, "ventWorkStatus": 0}},  {"id": 6, "status": {"heatLevel": 0, 
                                            "heatWorkStatus": 0, "ventLevel": 0, "ventWorkStatus": 0}},{"id": 0, "status": 
                                            {"heatLevel": 0, "heatWorkStatus": 0, "ventLevel": 0, "ventWorkStatus": 0}}, 
                                              {"id": 1, "status": {"heatLevel": 0, "heatWorkStatus": 0, "ventLevel": 0, "ventWorkStatus": 0}}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatSysStatus",{"seats":[12]},
                                              {"out": [{"id": 0, "status": {"isExtAdjAllowed": False,"isAutoModeOn": False, 
                                            "isMassageRunning": False}},
                                            {"id": 1, "status": {"isExtAdjAllowed": False,"isAutoModeOn": False,
                                             "isMassageRunning": False}}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatFault",{},
                                              {"out": [{"faultId": 0, "faultMsg": "", "seatId": 12}]})#系统故障
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                              {"params": {"id": 0,
                                                          "position": {"backAngle": 20, "longitudinalPosition": 100,
                                                                       "verticalPosition": 20,
                                                                       "LegrestVerticalPosition": 20,
                                                                       "backAngleIsValid": True,
                                                                       "longitudinalIsValid": True,
                                                                       "verticalIsValid": True,
                                                                       "legrestVerticalIsValid": True}}},
                                              {"out": 0}) #设置主驾姿态
        self.ipdu.resume_all_bus_send()
        sleep(2)

    @allure.title("获取所有座椅安全带状态_默认值")
    @pytest.mark.full
    def test_caseid_1983390(self): 
        #停止FR总线并停止
        #self.ipdu.pause_bus_send("backbonefr")
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT,pause_all_bus=True, resume_all_bus=False)
        #获取所有座椅安全带状态
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [0,1,4,5,6]},
                                            {"out": [{"value": {"id": 0, "status": 1}, "statusValidity": 0},
                                                    {"value": {"id": 1, "status": 1}, "statusValidity": 0},
                                                    {"value": {"id": 4, "status": 1}, "statusValidity": 0},
                                                    {"value": {"id": 5, "status": 1}, "statusValidity": 0},
                                                    {"value": {"id": 6, "status": 1}, "statusValidity": 0}]},timeout=0.5)
        
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [12]},
                                            {"out": [{"value": {"id": 0, "status": 1}, "statusValidity": 0},
                                                    {"value": {"id": 1, "status": 1}, "statusValidity": 0},
                                                    {"value": {"id": 4, "status": 1}, "statusValidity": 0},
                                                    {"value": {"id": 5, "status": 1}, "statusValidity": 0},
                                                    {"value": {"id": 6, "status": 1}, "statusValidity": 0}]},timeout=0.5)
        self.ipdu.resume_all_bus_send()   
            
    @allure.title("获取主驾座椅安全带状态_安全带状态变更时")
    @pytest.mark.sanity
    def test_caseid_1983395(self): 
        signal1Value = [0,1]
        signal2Value = [0,1]
        self.setDefaultSeatbeltStatus("主驾")
        self.partner.empty_all(0.5)
        
        for i in range(len(signal1Value)):
            for j in range(len(signal2Value)):
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1',signal1Value[i])
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts',signal2Value[j])
                sleep(0.1)
                if i==0 and j==0:
                    self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts ")
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [0]},
                                            {"out": [{"value": {"id": 0, "status": 1}, "statusValidity": 0},
                                                    ]})
                elif i==0 and j==1:
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts",
                                            {"status":{"value": 2, "validity":0}})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [0]},
                                            {"out": [{"value": {"id": 0, "status": 2}, "statusValidity": 0},
                                                    ]})
                elif i==1 and j==0:
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts",
                                            {"status":{"value": 0, "validity":0}})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [0]},
                                            {"out": [{"value": {"id": 0, "status": 0}, "statusValidity": 0},
                                                    ]})
                elif i==1 and j==1:
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts",
                                            {"status":{"value": 2, "validity":0}})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [0]},
                                            {"out": [{"value": {"id": 0, "status": 2}, "statusValidity": 0},
                                                    ]})
        #信号恢复默认值
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1',0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts',0)            

    @allure.title("获取副驾座椅安全带状态_安全带状态变更时")
    @pytest.mark.full
    def test_caseid_1983401(self): 
        signal1Value = [0,1]
        signal2Value = [0,1]
        self.setDefaultSeatbeltStatus("副驾")
        self.partner.empty_all(0.5)
        
        for i in range(len(signal1Value)):
            for j in range(len(signal2Value)):
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1',signal1Value[i])
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts',signal2Value[j])
                sleep(0.1)
                if i==0 and j==0:
                    self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntRightBeltSts ")
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [1]},
                                            {"out": [{"value": {"id": 1, "status": 1}, "statusValidity": 0},
                                                    ]})
                elif i==0 and j==1:
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightBeltSts",
                                            {"status":{"value": 2, "validity":0}})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [1]},
                                            {"out": [{"value": {"id": 1, "status": 2}, "statusValidity": 0},
                                                    ]})
                elif i==1 and j==0:
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightBeltSts",
                                            {"status":{"value": 0, "validity":0}})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [1]},
                                            {"out": [{"value": {"id": 1, "status": 0}, "statusValidity": 0},
                                                    ]})
                elif i==1 and j==1:
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightBeltSts",
                                            {"status":{"value": 2, "validity":0}})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [1]},
                                            {"out": [{"value": {"id": 1, "status": 2}, "statusValidity": 0},
                                                    ]})
        #信号恢复默认值
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1',0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts',0)  
    
    @allure.title("获取二排左侧座椅安全带状态_安全带状态变更时")
    @pytest.mark.full
    def test_caseid_1983402(self): 
        signal1Value = [0,1]
        signal2Value = [0,1]
        self.setDefaultSeatbeltStatus("二排左侧")
        self.partner.empty_all(0.5)
        
        for i in range(len(signal1Value)):
            for j in range(len(signal2Value)):
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecLeBltLockSt1',signal1Value[i])
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecLeBltLockSts',signal2Value[j])
                sleep(0.1)
                if i==0 and j==0:
                    self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearLeftBeltSts ")
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [4]},
                                            {"out": [{"value": {"id": 4, "status": 1}, "statusValidity": 0},
                                                    ]})
                elif i==0 and j==1:
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftBeltSts",
                                            {"status":{"value": 2, "validity":0}})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [4]},
                                            {"out": [{"value": {"id": 4, "status": 2}, "statusValidity": 0},
                                                    ]})
                elif i==1 and j==0:
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftBeltSts",
                                            {"status":{"value": 0, "validity":0}})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [4]},
                                            {"out": [{"value": {"id": 4, "status": 0}, "statusValidity": 0},
                                                    ]})
                elif i==1 and j==1:
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftBeltSts",
                                            {"status":{"value": 2, "validity":0}})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [4]},
                                            {"out": [{"value": {"id": 4, "status": 2}, "statusValidity": 0},
                                                    ]})
        #信号恢复默认值
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecLeBltLockSt1',0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecLeBltLockSts',0) 
       
    @allure.title("获取二排中间座椅安全带状态_安全带状态变更时")
    @pytest.mark.full
    def test_caseid_1983403(self): 
        signal1Value = [0,1]
        signal2Value = [0,1]
        self.setDefaultSeatbeltStatus("二排中间")
        self.partner.empty_all(0.5)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSt1',0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSts',0)
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearMiddleBeltSts")
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [5]},
                                            {"out": [{"value": {"id": 5, "status": 1}, "statusValidity": 0},
                                                    ]})
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSt1',1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSts',0)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearMiddleBeltSts",
                                             {"status":{"value": 0, "validity":0}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [5]},
                                            {"out": [{"value": {"id": 5, "status": 0}, "statusValidity": 0},
                                                    ]})
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSt1',1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSts',1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearMiddleBeltSts",
                                             {"status":{"value": 2, "validity":0}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [5]},
                                            {"out": [{"value": {"id": 5, "status": 2}, "statusValidity": 0},
                                                    ]})
        #信号恢复默认值
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSt1',0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSts',0)
        
    @allure.title("获取二排右侧座椅安全带状态_安全带状态变更时")
    @pytest.mark.full
    def test_caseid_1983404(self): 
        signal1Value = [0,1]
        signal2Value = [0,1]
        self.setDefaultSeatbeltStatus("二排右侧")
        self.partner.empty_all(0.5)
        
        for i in range(len(signal1Value)):
            for j in range(len(signal2Value)):
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecRiBltLockSt1',signal1Value[i])
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecRiBltLockSts',signal2Value[j])
                sleep(0.1)
                if i==0 and j==0:
                    self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearRightBeltSts")
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [6]},
                                            {"out": [{"value": {"id": 6, "status": 1}, "statusValidity": 0},
                                                    ]})
                elif i==0 and j==1:
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightBeltSts",
                                            {"status":{"value": 2, "validity":0}})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [6]},
                                            {"out": [{"value": {"id": 6, "status": 2}, "statusValidity": 0},
                                                    ]})
                elif i==1 and j==0:
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightBeltSts",
                                            {"status":{"value": 0, "validity":0}})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [6]},
                                            {"out": [{"value": {"id": 6, "status": 0}, "statusValidity": 0},
                                                    ]})
                elif i==1 and j==1:
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightBeltSts",
                                            {"status":{"value": 2, "validity":0}})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [6]},
                                            {"out": [{"value": {"id": 6, "status": 2}, "statusValidity": 0},
                                                    ]})
        #信号恢复默认值
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecRiBltLockSt1',0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecRiBltLockSts',0) 
    
    @allure.title("获取所有座椅安全带状态_安全带状态变更时")
    @pytest.mark.full
    def test_caseid_1983405(self): 
        signal1Value = [0,1]
        signal2Value = [0,1]
    
        for i in range(len(signal1Value)):
            for j in range(len(signal2Value)):
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1',signal1Value[i])
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts',signal2Value[j])
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1',signal1Value[i])
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts',signal2Value[j])
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecLeBltLockSt1',signal1Value[i])
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecLeBltLockSts',signal2Value[j])
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSt1',signal1Value[i])
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSts',signal2Value[j])
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecRiBltLockSt1',signal1Value[i])
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecRiBltLockSts',signal2Value[j])
                sleep(1)
                if i==0 and j==0:
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [3]},
                                            {"out": [{"value": {"id": 0, "status": 1}, "statusValidity": 0},
                                                     {"value": {"id": 1, "status": 1}, "statusValidity": 0},
                                                    ]})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [7]},
                                            {"out": [{"value": {"id": 4, "status": 1}, "statusValidity": 0},
                                                     {"value": {"id": 5, "status": 1}, "statusValidity": 0},
                                                     {"value": {"id": 6, "status": 1}, "statusValidity": 0},
                                                    ]})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [12]},
                                            {"out": [{"value": {"id": 0, "status": 1}, "statusValidity": 0},
                                                     {"value": {"id": 1, "status": 1}, "statusValidity": 0},
                                                     {"value": {"id": 4, "status": 1}, "statusValidity": 0},
                                                     {"value": {"id": 5, "status": 1}, "statusValidity": 0},
                                                     {"value": {"id": 6, "status": 1}, "statusValidity": 0},
                                                    ]})
                elif i==0 and j==1:
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [3]},
                                            {"out": [{"value": {"id": 0, "status": 2}, "statusValidity": 0},
                                                     {"value": {"id": 1, "status": 2}, "statusValidity": 0},
                                                    ]})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [7]},
                                            {"out": [{"value": {"id": 4, "status": 2}, "statusValidity": 0},
                                                     {"value": {"id": 5, "status": 2}, "statusValidity": 0},
                                                     {"value": {"id": 6, "status": 2}, "statusValidity": 0},
                                                    ]})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [12]},
                                            {"out": [{"value": {"id": 0, "status": 2}, "statusValidity": 0},
                                                     {"value": {"id": 1, "status": 2}, "statusValidity": 0},
                                                     {"value": {"id": 4, "status": 2}, "statusValidity": 0},
                                                     {"value": {"id": 5, "status": 2}, "statusValidity": 0},
                                                     {"value": {"id": 6, "status": 2}, "statusValidity": 0},
                                                    ]})
                elif i==1 and j==0:
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [3]},
                                            {"out": [{"value": {"id": 0, "status": 0}, "statusValidity": 0},
                                                     {"value": {"id": 1, "status": 0}, "statusValidity": 0},
                                                    ]})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [7]},
                                            {"out": [{"value": {"id": 4, "status": 0}, "statusValidity": 0},
                                                     {"value": {"id": 5, "status": 0}, "statusValidity": 0},
                                                     {"value": {"id": 6, "status": 0}, "statusValidity": 0},
                                                    ]})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [12]},
                                            {"out": [{"value": {"id": 0, "status": 0}, "statusValidity": 0},
                                                     {"value": {"id": 1, "status": 0}, "statusValidity": 0},
                                                     {"value": {"id": 4, "status": 0}, "statusValidity": 0},
                                                     {"value": {"id": 5, "status": 0}, "statusValidity": 0},
                                                     {"value": {"id": 6, "status": 0}, "statusValidity": 0},
                                                    ]})
                elif i==1 and j==1:
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [3]},
                                            {"out": [{"value": {"id": 0, "status": 2}, "statusValidity": 0},
                                                     {"value": {"id": 1, "status": 2}, "statusValidity": 0},
                                                    ]})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [7]},
                                            {"out": [{"value": {"id": 4, "status": 2}, "statusValidity": 0},
                                                     {"value": {"id": 5, "status": 2}, "statusValidity": 0},
                                                     {"value": {"id": 6, "status": 2}, "statusValidity": 0},
                                                    ]})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [12]},
                                            {"out": [{"value": {"id": 0, "status": 2}, "statusValidity": 0},
                                                     {"value": {"id": 1, "status": 2}, "statusValidity": 0},
                                                     {"value": {"id": 4, "status": 2}, "statusValidity": 0},
                                                     {"value": {"id": 5, "status": 2}, "statusValidity": 0},
                                                     {"value": {"id": 6, "status": 2}, "statusValidity": 0},
                                                    ]})
        #信号恢复默认值
        self.setDefaultSeatbeltStatus("所有座椅")
      
    @allure.title("获取所有座椅安全带状态有效性_信号Miss时")
    @pytest.mark.full
    def test_caseid_1983406(self):
        
        self.setDefaultSeatbeltStatus("所有座椅")
        self.partner.empty_all(0.5)
        
        #感觉此处会有问题
        #主驾
        self.ipdu.pause_bus_send("backbonefr")
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [0]},
                                            {"out": [{"value": {"id": 0, "status": 1}, "statusValidity": 0},]})
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts",timeout=0.5)
        self.ipdu.resume_all_bus_send()
        sleep(2)
        
        #副驾
        self.ipdu.pause_bus_send("backbonefr")
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [1]},
                                            {"out": [{"value": {"id": 1, "status": 1}, "statusValidity": 0},]})
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntRightBeltSts",timeout=0.5)
        self.ipdu.resume_all_bus_send()
        sleep(2)
        
        #二排左
        self.ipdu.pause_bus_send("backbonefr")
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [4]},
                                            {"out": [{"value": {"id": 4, "status": 1}, "statusValidity": 0},]})
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearLeftBeltSts",timeout=0.5)
        self.ipdu.resume_all_bus_send()
        sleep(2)
        
        #二排中
        self.ipdu.pause_bus_send("backbonefr")
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [5]},
                                            {"out": [{"value": {"id": 5, "status": 1}, "statusValidity": 0},]})
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearMiddleBeltSts",timeout=0.5)
        self.ipdu.resume_all_bus_send()
        sleep(2)
        
        #二排右
        self.ipdu.pause_bus_send("backbonefr")
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [6]},
                                            {"out": [{"value": {"id": 6, "status": 1}, "statusValidity": 0},]})
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearRightBeltSts",timeout=0.5)
        self.ipdu.resume_all_bus_send()
        sleep(2)
        self.ipdu.pause_bus_send("backbonefr")
        sleep(2)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts",
                                             {"status":{"value": 1, "validity":4}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightBeltSts",
                                             {"status":{"value": 1, "validity":4}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftBeltSts",
                                             {"status":{"value": 1, "validity":4}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearMiddleBeltSts",
                                             {"status":{"value": 1, "validity":4}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightBeltSts",
                                             {"status":{"value": 1, "validity":4}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [0,1,4,5,6]},
                                            {"out": [{"value": {"id": 0, "status": 1}, "statusValidity": 4},
                                                    {"value": {"id": 1, "status": 1}, "statusValidity": 4},
                                                    {"value": {"id": 4, "status": 1}, "statusValidity": 4},
                                                    {"value": {"id": 5, "status": 1}, "statusValidity": 4},
                                                    {"value": {"id": 6, "status": 1}, "statusValidity": 4}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [12]},
                                            {"out": [{"value": {"id": 0, "status": 1}, "statusValidity": 4},
                                                    {"value": {"id": 1, "status": 1}, "statusValidity": 4},
                                                    {"value": {"id": 4, "status": 1}, "statusValidity": 4},
                                                    {"value": {"id": 5, "status": 1}, "statusValidity": 4},
                                                    {"value": {"id": 6, "status": 1}, "statusValidity": 4}]})
        self.ipdu.resume_all_bus_send()
        sleep(1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts",
                                             {"status":{"value": 1, "validity":0}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightBeltSts",
                                             {"status":{"value": 1, "validity":0}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftBeltSts",
                                             {"status":{"value": 1, "validity":0}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearMiddleBeltSts",
                                             {"status":{"value": 1, "validity":0}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightBeltSts",
                                             {"status":{"value": 1, "validity":0}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [0,1,4,5,6]},
                                            {"out": [{"value": {"id": 0, "status": 1}, "statusValidity": 0},
                                                    {"value": {"id": 1, "status": 1}, "statusValidity": 0},
                                                    {"value": {"id": 4, "status": 1}, "statusValidity": 0},
                                                    {"value": {"id": 5, "status": 1}, "statusValidity": 0},
                                                    {"value": {"id": 6, "status": 1}, "statusValidity": 0}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [12]},
                                            {"out": [{"value": {"id": 0, "status": 1}, "statusValidity": 0},
                                                    {"value": {"id": 1, "status": 1}, "statusValidity": 0},
                                                    {"value": {"id": 4, "status": 1}, "statusValidity": 0},
                                                    {"value": {"id": 5, "status": 1}, "statusValidity": 0},
                                                    {"value": {"id": 6, "status": 1}, "statusValidity": 0}]})
        
    @allure.title("获取主副驾座椅位置信息_默认值")
    @pytest.mark.full
    def test_caseid_1983408(self):
        #设置一个非默认值 
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'SeatBackAngleRowFirstDrvr',180)
        self.ipdu.pause_bus_send("backbonefr")
        sleep(1)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT,pause_all_bus=True, resume_all_bus=False)
        #获取所有座椅安全带状态
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo", {"seats": [0,1]},
                                               {"out": [{"id":0,"position":{"backAngle":0, "longitudinalPosition": 100,"verticalPosition": 100,"LegrestVerticalPosition": 100,"backAngleIsValid": 0,"longitudinalIsValid": 0,"verticalIsValid": 0,"legrestVerticalIsValid": 0}},
                                                        {"id":1,"position":{"backAngle":0, "longitudinalPosition": 100,"verticalPosition": 100,"LegrestVerticalPosition": 100,"backAngleIsValid": 0,"longitudinalIsValid": 0,"verticalIsValid": 0,"legrestVerticalIsValid": 0}},
                                                        ]},timeout = 1)
                                                                           
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo", {"seats": [3]},
                                               {"out": [{"id":0,"position":{"backAngle":0, "longitudinalPosition": 100,"verticalPosition": 100,"LegrestVerticalPosition": 100,"backAngleIsValid": 0,"longitudinalIsValid": 0,"verticalIsValid": 0,"legrestVerticalIsValid": 0}},
                                                        {"id":1,"position":{"backAngle":0, "longitudinalPosition": 100,"verticalPosition": 100,"LegrestVerticalPosition": 100,"backAngleIsValid": 0,"longitudinalIsValid": 0,"verticalIsValid": 0,"legrestVerticalIsValid": 0}},
                                                        ]},timeout = 1)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo", {"seats": [12]},
                                               {"out": [{"id":0,"position":{"backAngle":0, "longitudinalPosition": 100,"verticalPosition": 100,"LegrestVerticalPosition": 100,"backAngleIsValid": 0,"longitudinalIsValid": 0,"verticalIsValid": 0,"legrestVerticalIsValid": 0}},
                                                        {"id":1,"position":{"backAngle":0, "longitudinalPosition": 100,"verticalPosition": 100,"LegrestVerticalPosition": 100,"backAngleIsValid": 0,"longitudinalIsValid": 0,"verticalIsValid": 0,"legrestVerticalIsValid": 0}},
                                                        ]},timeout = 1)
        self.ipdu.resume_all_bus_send()   

    @allure.title("获取主驾座椅位置信息_位置信息变更时")
    @pytest.mark.sanity
    def test_caseid_1983437(self): 
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF',3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF',3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF',3)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiPerc',1000)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldPerc',1000)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiPerc',1000)
        sleep(1)
      
        self.setDefaultSeatPosition()
        self.partner.empty_all(0.5)
   
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'SeatBackAngleRowFirstDrvr',0)
        sleep(1)
        # self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatPosition")
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo", {"seats": [0]},
                                            {"out": [{"id":0,"position":{"backAngle":0, "longitudinalPosition": 100,"verticalPosition": 100,"LegrestVerticalPosition": 100,"backAngleIsValid": 1,"longitudinalIsValid": 0,"verticalIsValid": 0,"legrestVerticalIsValid": 0}},
                                                        ]})
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'SeatBackAngleRowFirstDrvr',90)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatPosition",
                                             {"position":{"backAngle": 90, "longitudinalPosition":100,"verticalPosition":100,"LegrestVerticalPosition":100,"backAngleIsValid":1,"longitudinalIsValid":0,"verticalIsValid":0,"legrestVerticalIsValid":0}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo", {"seats": [0]},
                                               {"out": [{"id":0,"position":{"backAngle":90, "longitudinalPosition": 100,"verticalPosition": 100,"LegrestVerticalPosition": 100,"backAngleIsValid": 1,"longitudinalIsValid": 0,"verticalIsValid": 0,"legrestVerticalIsValid": 0}},
                                                        ]})
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'SeatBackAngleRowFirstDrvr',180)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatPosition",
                                             {"position":{"backAngle": 180, "longitudinalPosition":100,"verticalPosition":100,"LegrestVerticalPosition":100,"backAngleIsValid":1,"longitudinalIsValid":0,"verticalIsValid":0,"legrestVerticalIsValid":0}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo", {"seats": [0]},
                                            {"out": [{"id":0,"position":{"backAngle":180, "longitudinalPosition": 100,"verticalPosition": 100,"LegrestVerticalPosition": 100,"backAngleIsValid": 1,"longitudinalIsValid": 0,"verticalIsValid": 0,"legrestVerticalIsValid": 0}},
                                                        ]})
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'SeatBackAngleRowFirstDrvr',0)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatPosition",
                                             {"position":{"backAngle": 0, "longitudinalPosition":100,"verticalPosition":100,"LegrestVerticalPosition":100,"backAngleIsValid":1,"longitudinalIsValid":0,"verticalIsValid":0,"legrestVerticalIsValid":0}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo", {"seats": [0]},
                                            {"out": [{"id":0,"position":{"backAngle":0, "longitudinalPosition": 100,"verticalPosition": 100,"LegrestVerticalPosition": 100,"backAngleIsValid": 1,"longitudinalIsValid": 0,"verticalIsValid": 0,"legrestVerticalIsValid": 0}},
                                                        ]})  
        SignalValue = [0,500,1000]
        for i in range(0,4):
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF',i)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF',i)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF',i)
            if i != 3:
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiPerc',SignalValue[i])
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldPerc',SignalValue[i])
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiPerc',SignalValue[i])
                sleep(0.5)
                self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatPosition")
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo", {"seats": [0]},
                                               {"out": [{"id":0,"position":{"backAngle":0, "longitudinalPosition": 100,"verticalPosition": 100,"LegrestVerticalPosition": 100,"backAngleIsValid": 1,"longitudinalIsValid": 0,"verticalIsValid": 0,"legrestVerticalIsValid": 0}},
                                                        ]})    
            else:
                for j in range(3):
                    self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiPerc',SignalValue[j])
                    self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldPerc',SignalValue[j])
                    self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiPerc',SignalValue[j])
                    sleep(0.5)
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatPosition",
                                                {"position":{"backAngle": 0, "longitudinalPosition":SignalValue[j]*0.1,"verticalPosition":SignalValue[j]*0.1,"LegrestVerticalPosition":SignalValue[j]*0.1,"backAngleIsValid":1,"longitudinalIsValid":1,"verticalIsValid":1,"legrestVerticalIsValid":1}})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo", {"seats": [0]},
                                                {"out": [{"id":0,"position":{"backAngle":0, "longitudinalPosition": SignalValue[j]*0.1,"verticalPosition": SignalValue[j]*0.1,"LegrestVerticalPosition": SignalValue[j]*0.1,"backAngleIsValid": 1,"longitudinalIsValid": 1,"verticalIsValid": 1,"legrestVerticalIsValid": 1}},
                                                        ]})
             
    @allure.title("获取主副驾座椅位置信息_信号Miss时")
    @pytest.mark.full
    def test_caseid_1983604(self): 
        self.setDefaultSeatPosition()
        self.partner.empty_all(0.5)                                         
        self.ipdu.resume_all_bus_send()
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT,pause_all_bus=True, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo", {"seats": [0,1]},
                                            {"out": [{"id":0,"position":{"backAngleIsValid": 0}},
                                                     {"id":1,"position":{"backAngleIsValid": 0}},
                                                        ]},timeout = 1)
        self.ipdu.resume_all_bus_send() 
        sleep(1)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo", {"seats": [0,1]},
                                            {"out": [{"id":0,"position":{"backAngleIsValid": 1}},
                                                     {"id":1,"position":{"backAngleIsValid": 1}},
                                                        ]},timeout = 1)   
        
    @allure.title("获取副驾座椅位置信息_位置信息变更时")
    @pytest.mark.full
    def test_caseid_1983438(self):
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiQF',3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldQF',3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiQF',3)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiPerc',1000)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldPerc',1000)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiPerc',1000)
        sleep(1)
        self.setDefaultSeatPosition()
        self.partner.empty_all(0.5)
       
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'SeatBackAngleRowFirstPass',0)
        # self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatPosition")
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo", {"seats": [1]},
                                            {"out": [{"id":1,"position":{"backAngle":0, "longitudinalPosition": 100,"verticalPosition": 100,"LegrestVerticalPosition": 100,"backAngleIsValid": 1,"longitudinalIsValid": 0,"verticalIsValid": 0,"legrestVerticalIsValid": 0}},
                                                        ]})
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'SeatBackAngleRowFirstPass',90)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatPosition",
                                             {"position":{"backAngle": 90, "longitudinalPosition":100,"verticalPosition":100,"LegrestVerticalPosition":100,"backAngleIsValid":1,"longitudinalIsValid":0,"verticalIsValid":0,"legrestVerticalIsValid":0}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo", {"seats": [1]},
                                               {"out": [{"id":1,"position":{"backAngle":90, "longitudinalPosition": 100,"verticalPosition": 100,"LegrestVerticalPosition": 100,"backAngleIsValid": 1,"longitudinalIsValid": 0,"verticalIsValid": 0,"legrestVerticalIsValid": 0}},
                                                        ]})
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'SeatBackAngleRowFirstPass',180)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatPosition",
                                             {"position":{"backAngle": 180, "longitudinalPosition":100,"verticalPosition":100,"LegrestVerticalPosition":100,"backAngleIsValid":1,"longitudinalIsValid":0,"verticalIsValid":0,"legrestVerticalIsValid":0}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo", {"seats": [1]},
                                            {"out": [{"id":1,"position":{"backAngle":180, "longitudinalPosition": 100,"verticalPosition": 100,"LegrestVerticalPosition": 100,"backAngleIsValid": 1,"longitudinalIsValid": 0,"verticalIsValid": 0,"legrestVerticalIsValid": 0}},
                                                        ]})
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'SeatBackAngleRowFirstPass',0)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatPosition",
                                             {"position":{"backAngle": 0, "longitudinalPosition":100,"verticalPosition":100,"LegrestVerticalPosition":100,"backAngleIsValid":1,"longitudinalIsValid":0,"verticalIsValid":0,"legrestVerticalIsValid":0}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo", {"seats": [1]},
                                            {"out": [{"id":1,"position":{"backAngle":0, "longitudinalPosition": 100,"verticalPosition": 100,"LegrestVerticalPosition": 100,"backAngleIsValid": 1,"longitudinalIsValid": 0,"verticalIsValid": 0,"legrestVerticalIsValid": 0}},
                                                        ]})       

        SignalValue = [0,500,1000]
        for i in range(0,4):
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiQF',i)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldQF',i)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiQF',i)
            if i != 3:
                self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiPerc',SignalValue[i])
                self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldPerc',SignalValue[i])
                self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiPerc',SignalValue[i])
                sleep(0.5)
                self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntRightSeatPosition")
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo", {"seats": [1]},
                                               {"out": [{"id":1,"position":{"backAngle":0, "longitudinalPosition": 100,"verticalPosition": 100,"LegrestVerticalPosition": 100,"backAngleIsValid": 1,"longitudinalIsValid": 0,"verticalIsValid": 0,"legrestVerticalIsValid": 0}},
                                                        ]})    
            else:
                for j in range(3):
                    self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiPerc',SignalValue[j])
                    self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldPerc',SignalValue[j])
                    self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiPerc',SignalValue[j])
                    sleep(0.5)
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatPosition",
                                                {"position":{"backAngle": 0, "longitudinalPosition":SignalValue[j]*0.1,"verticalPosition":SignalValue[j]*0.1,"LegrestVerticalPosition":SignalValue[j]*0.1,"backAngleIsValid":1,"longitudinalIsValid":1,"verticalIsValid":1,"legrestVerticalIsValid":1}})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo", {"seats": [1]},
                                                {"out": [{"id":1,"position":{"backAngle":0, "longitudinalPosition": SignalValue[j]*0.1,"verticalPosition": SignalValue[j]*0.1,"LegrestVerticalPosition": SignalValue[j]*0.1,"backAngleIsValid": 1,"longitudinalIsValid": 1,"verticalIsValid": 1,"legrestVerticalIsValid": 1}},
                                                        ]})   
        
    @allure.title("获取所有座椅位置信息_位置信息变更时")
    @pytest.mark.smoke
    def test_caseid_1983444(self): 
        self.setDefaultSeatPosition()
        self.partner.empty_all(0.5)
        
        backAngleValue = [0,90,180]
        positionSignalValue = [0,500,1000]
        for i in range(len(backAngleValue)):
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'SeatBackAngleRowFirstDrvr',backAngleValue[i])
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'SeatBackAngleRowFirstPass',backAngleValue[i])
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo", {"seats": [3]},
                                            {"out": [{"id":0,"position":{"backAngle":backAngleValue[i], "longitudinalPosition": 100,"verticalPosition": 100,"LegrestVerticalPosition": 100,"backAngleIsValid": 1,"longitudinalIsValid": 0,"verticalIsValid": 0,"legrestVerticalIsValid": 0}},
                                                     {"id":1,"position":{"backAngle":backAngleValue[i], "longitudinalPosition": 100,"verticalPosition": 100,"LegrestVerticalPosition": 100,"backAngleIsValid": 1,"longitudinalIsValid": 0,"verticalIsValid": 0,"legrestVerticalIsValid": 0}},   
                                                        ]})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo", {"seats": [12]},
                                            {"out": [{"id":0,"position":{"backAngle":backAngleValue[i], "longitudinalPosition": 100,"verticalPosition": 100,"LegrestVerticalPosition": 100,"backAngleIsValid": 1,"longitudinalIsValid": 0,"verticalIsValid": 0,"legrestVerticalIsValid": 0}},
                                                     {"id":1,"position":{"backAngle":backAngleValue[i], "longitudinalPosition": 100,"verticalPosition": 100,"LegrestVerticalPosition": 100,"backAngleIsValid": 1,"longitudinalIsValid": 0,"verticalIsValid": 0,"legrestVerticalIsValid": 0}},   
                                                        ]})
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF',3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF',3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF',3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiQF',3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldQF',3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiQF',3)
        
        for i in range(len(positionSignalValue)):
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiPerc',positionSignalValue[i])
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldPerc',positionSignalValue[i])
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiPerc',positionSignalValue[i])
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiPerc',positionSignalValue[i])
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldPerc',positionSignalValue[i])
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiPerc',positionSignalValue[i])
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo", {"seats": [3]},
                                            {"out": [{"id":0,"position":{"backAngle":180, "longitudinalPosition": positionSignalValue[i]*0.1,"verticalPosition": positionSignalValue[i]*0.1,"LegrestVerticalPosition": positionSignalValue[i]*0.1,"backAngleIsValid": 1,"longitudinalIsValid": 1,"verticalIsValid": 1,"legrestVerticalIsValid": 1}},
                                                     {"id":1,"position":{"backAngle":180, "longitudinalPosition": positionSignalValue[i]*0.1,"verticalPosition": positionSignalValue[i]*0.1,"LegrestVerticalPosition": positionSignalValue[i]*0.1,"backAngleIsValid": 1,"longitudinalIsValid": 1,"verticalIsValid": 1,"legrestVerticalIsValid": 1}},   
                                                        ]})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo", {"seats": [12]},
                                            {"out": [{"id":0,"position":{"backAngle":180, "longitudinalPosition": positionSignalValue[i]*0.1,"verticalPosition": positionSignalValue[i]*0.1,"LegrestVerticalPosition": positionSignalValue[i]*0.1,"backAngleIsValid": 1,"longitudinalIsValid": 1,"verticalIsValid": 1,"legrestVerticalIsValid": 1}},
                                                     {"id":1,"position":{"backAngle":180, "longitudinalPosition": positionSignalValue[i]*0.1,"verticalPosition": positionSignalValue[i]*0.1,"LegrestVerticalPosition": positionSignalValue[i]*0.1,"backAngleIsValid": 1,"longitudinalIsValid": 1,"verticalIsValid": 1,"legrestVerticalIsValid": 1}},   
                                                        ]})
    
    @allure.title("获取所有座椅通风加热状态_默认值")
    @pytest.mark.smoke
    def test_caseid_1983445(self): 
        
        #设置非默认值
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgLvlSts',2)
        self.del_s2s_db()  # 删除数据库
        self.del_s2s_db()
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT,resume_all_bus=False)
         
        sleep(30)
        #self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT,pause_all_bus=True, resume_all_bus=False)
        #获取所有座椅安全带状态
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [0,1,4,6]},
                                               {"out": [{"id":0,"status":{"heatLevel":0, "heatTime": 59,"heatWorkStatus": 0,"ventLevel": 0,"ventTime": 59,"ventWorkStatus": 0}},
                                                        {"id":1,"status":{"heatLevel":0, "heatTime": 59,"heatWorkStatus": 0,"ventLevel": 0,"ventTime": 59,"ventWorkStatus": 0}},
                                                        {"id":1,"status":{"heatLevel":0, "heatTime": 59,"heatWorkStatus": 0,"ventLevel": 0,"ventTime": 59,"ventWorkStatus": 0}},
                                                        {"id":1,"status":{"heatLevel":0, "heatTime": 59,"heatWorkStatus": 0,"ventLevel": 0,"ventTime": 59,"ventWorkStatus": 0}},
                                                        ]})
                                                                           
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [3]},
                                               {"out": [{"id":0,"status":{"heatLevel":0, "heatTime": 59,"heatWorkStatus": 0,"ventLevel": 0,"ventTime": 59,"ventWorkStatus": 0}},
                                                        {"id":1,"status":{"heatLevel":0, "heatTime": 59,"heatWorkStatus": 0,"ventLevel": 0,"ventTime": 59,"ventWorkStatus": 0}},
                                                        ]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [7]},
                                               {"out": [{"id":4,"status":{"heatLevel":0, "heatTime": 59,"heatWorkStatus": 0,"ventLevel": 0,"ventTime": 59,"ventWorkStatus": 0}},
                                                        {"id":6,"status":{"heatLevel":0, "heatTime": 59,"heatWorkStatus": 0,"ventLevel": 0,"ventTime": 59,"ventWorkStatus": 0}},
                                                        ]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                               {"out": [{"id":0,"status":{"heatLevel":0, "heatTime": 59,"heatWorkStatus": 0,"ventLevel": 0,"ventTime": 59,"ventWorkStatus": 0}},
                                                        {"id":1,"status":{"heatLevel":0, "heatTime": 59,"heatWorkStatus": 0,"ventLevel": 0,"ventTime": 59,"ventWorkStatus": 0}},
                                                        {"id":4,"status":{"heatLevel":0, "heatTime": 59,"heatWorkStatus": 0,"ventLevel": 0,"ventTime": 59,"ventWorkStatus": 0}},
                                                        {"id":6,"status":{"heatLevel":0, "heatTime": 59,"heatWorkStatus": 0,"ventLevel": 0,"ventTime": 59,"ventWorkStatus": 0}},
                                                        ]})
        self.ipdu.resume_all_bus_send() 
               
    @allure.title("通知主驾座椅通风加热状态_通风加热状态变化时")
    @pytest.mark.sanity
    def test_caseid_1983446(self): 
        timeValue = [0,10,25,40,50,59]
        self.setSeatHeatVent("主驾",0)
        self.partner.empty_all(0.5)
        #测试heatLevel ventLevel
        for i in range(4):
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgLvlSts',i)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentnLvlSts',i)
            if i == 0:
                self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus ")     
            else:
                self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                                {"status":{"heatLevel":i, "ventLevel":i}})   
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [0]},
                                                {"out": [{"id":0,"status":{"heatLevel":i,"ventLevel":i}},
                                                        ]})
        self.setSeatHeatVent("主驾",0)
        self.partner.empty_all(0.5)
        for i in range(7):
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgAvlSts',i)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentAvlSts',i)
            if i == 0:
                self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus ")     
            else:
                self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                                {"status":{"heatWorkStatus": i,"ventWorkStatus": i}})   
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [0]},
                                                {"out": [{"id":0,"status":{"heatWorkStatus": i,"ventWorkStatus": i}},
                                                        ]})
        self.setSeatHeatVent("主驾",0)
        
        #测试Time
        for i in range(len(timeValue)):
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingTime",
                                            {"params": [{"id": 0, "uint64Info": timeValue[i]}]})
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingTime",
                                             {"params": [{"id": 0, "uint64Info": timeValue[i]}]})
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                                {"status":{"heatLevel":0, "heatTime": timeValue[i],"heatWorkStatus": 0,"ventLevel":0,"ventTime": timeValue[i],"ventWorkStatus": 0}})   
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [0]},
                                                {"out": [{"id":0,"status":{"heatLevel":0, "heatTime": timeValue[i],"heatWorkStatus": 0,"ventLevel":0,"ventTime": timeValue[i],"ventWorkStatus": 0}},
                                                        ]})
       
    @allure.title("通知副驾座椅通风加热状态_通风加热状态变化时")
    @pytest.mark.full
    def test_caseid_1983447(self): 
        timeValue = [0,10,25,40,50,59]
        self.setSeatHeatVent("副驾",0)
        self.partner.empty_all(0.5)
        #测试heatLevel ventLevel
        for i in range(4):
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgLvlSts',i)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentnLvlSts',i)
            if i == 0:
                self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus")     
            else:
                self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus",
                                                {"status":{"heatLevel":i,"ventLevel":i,}})   
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [1]},
                                                {"out": [{"id":1,"status":{"heatLevel":i, "ventLevel":i}},
                                                        ]})
        self.setSeatHeatVent("副驾",0)
        self.partner.empty_all(0.5)
        for i in range(7):
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgAvlSts',i)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentAvlSts',i)
            if i == 0:
                self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus")     
            else:
                self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus",
                                                {"status":{"heatWorkStatus": i,"ventWorkStatus": i}})   
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [1]},
                                                {"out": [{"id":1,"status":{"heatWorkStatus": i,"ventWorkStatus": i}},
                                                        ]})
        self.setSeatHeatVent("副驾",0)
        
         #测试Time
        for i in range(len(timeValue)):
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingTime",
                                            {"params": [{"id": 1, "uint64Info": timeValue[i]}]})
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingTime",
                                             {"params": [{"id": 1, "uint64Info": timeValue[i]}]})
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus",
                                                {"status":{"heatLevel":0, "heatTime": timeValue[i],"heatWorkStatus": 0,"ventLevel":0,"ventTime": timeValue[i],"ventWorkStatus": 0}})   
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [1]},
                                                {"out": [{"id":1,"status":{"heatLevel":0, "heatTime": timeValue[i],"heatWorkStatus": 0,"ventLevel":0,"ventTime": timeValue[i],"ventWorkStatus": 0}},
                                                        ]})
    
    @allure.title("通知二排左侧座椅通风加热状态_通风加热状态变化时")
    @pytest.mark.full
    def test_caseid_1983448(self): 
        timeValue = [0,10,25,40,50,59]
        self.setSeatHeatVent("二排左侧",0)
        self.partner.empty_all(0.5)
        #测试heatLevel ventLevel
        for i in range(4):
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecLe',i)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecLe',i)
            sleep(0.5)
            if i == 0:
                self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus")     
            else:
                self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus",
                                                {"status":{"heatLevel":i,"ventLevel":i,}})   
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [4]},
                                                {"out": [{"id":4,"status":{"heatLevel":i,"ventLevel":i,}},
                                                        ]})
        self.setSeatHeatVent("二排左侧",0)
        self.partner.empty_all(0.5)
        for i in range(7):
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecLe',i)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecLe',i)
            sleep(0.5)
            if i == 0:
                self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus")     
            else:
                self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus",
                                               {"status":{"heatWorkStatus": i,"ventWorkStatus": i}})  
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [4]},
                                                {"out": [{"id":4,"status":{"heatWorkStatus": i,"ventWorkStatus": i}},
                                                        ]})
        self.setSeatHeatVent("二排左侧",0)
        
         #测试Time
        for i in range(len(timeValue)):
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingTime",
                                            {"params": [{"id": 4, "uint64Info": timeValue[i]}]})
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingTime",
                                             {"params": [{"id": 4, "uint64Info": timeValue[i]}]})
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus",
                                                {"status":{"heatLevel":0, "heatTime": timeValue[i],"heatWorkStatus": 0,"ventLevel":0,"ventTime": timeValue[i],"ventWorkStatus": 0}})   
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [4]},
                                                {"out": [{"id":4,"status":{"heatLevel":0, "heatTime": timeValue[i],"heatWorkStatus": 0,"ventLevel":0,"ventTime": timeValue[i],"ventWorkStatus": 0}},
                                                        ]})

    @allure.title("通知二排右侧座椅通风加热状态_通风加热状态变化时")
    @pytest.mark.full
    def test_caseid_1983449(self): 
        timeValue = [0,10,25,40,50,59]
        self.setSeatHeatVent("二排右侧",0)
        self.partner.empty_all(0.5)
        #测试heatLevel ventLevel
        for i in range(4):
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecRi',i)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecRi',i)
            sleep(0.5)
            if i == 0:
                self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus")     
            else:
                self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus",
                                                {"status":{"heatLevel":i, "ventLevel":i,}})   
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [6]},
                                                {"out": [{"id":6,"status":{"heatLevel":i, "ventLevel":i}},
                                                        ]})
        self.setSeatHeatVent("二排右侧",0)
        self.partner.empty_all(0.5)
        for i in range(7):
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecRi',i)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecRi',i)
            sleep(0.5)
            if i == 0:
                self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus")     
            else:
                self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus",
                                                {"status":{"heatWorkStatus": i,"ventWorkStatus": i}})   
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [6]},
                                                {"out": [{"id":6,"status":{"heatWorkStatus": i,"ventWorkStatus": i}},
                                                        ]})
        self.setSeatHeatVent("二排右侧",0)
        
         #测试Time
        for i in range(len(timeValue)):
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingTime",
                                            {"params": [{"id": 6, "uint64Info": timeValue[i]}]})
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingTime",
                                             {"params": [{"id": 6, "uint64Info": timeValue[i]}]})
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus",
                                                {"status":{"heatLevel":0, "heatTime": timeValue[i],"heatWorkStatus": 0,"ventLevel":0,"ventTime": timeValue[i],"ventWorkStatus": 0}})   
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [6]},
                                                {"out": [{"id":6,"status":{"heatLevel":0, "heatTime": timeValue[i],"heatWorkStatus": 0,"ventLevel":0,"ventTime": timeValue[i],"ventWorkStatus": 0}},
                                                        ]})

    @allure.title("获取所有座椅通风加热状态_通风加热状态变化时")
    @pytest.mark.smoke
    def test_caseid_1983450(self): 
        timeValue = [0,10,25,40,50,59]
        self.setSeatHeatVent("主驾",0)
        self.setSeatHeatVent("副驾",0)
        self.setSeatHeatVent("二排左侧",0)
        self.setSeatHeatVent("二排右侧",0)
        self.partner.empty_all(0.5)
        #测试heatLevel ventLevel
        for i in range(4):
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgLvlSts',i)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentnLvlSts',i)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgAvlSts',i)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentAvlSts',i)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgLvlSts',i)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentnLvlSts',i)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgAvlSts',i)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentAvlSts',i)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecLe',i)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecLe',i)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecLe',i)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecLe',i)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecRi',i)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecRi',i)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecRi',i)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecRi',i)
            
            sleep(0.5)
            
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [3]},
                                                {"out": [{"id":0,"status":{"heatLevel":i, "heatTime": 59,"heatWorkStatus": i,"ventLevel":i,"ventTime": 59,"ventWorkStatus": i}},
                                                         {"id":1,"status":{"heatLevel":i, "heatTime": 59,"heatWorkStatus": i,"ventLevel":i,"ventTime": 59,"ventWorkStatus": i}},
                                                        ]})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [7]},
                                                {"out": [{"id":4,"status":{"heatLevel":i, "heatTime": 59,"heatWorkStatus": i,"ventLevel":i,"ventTime": 59,"ventWorkStatus": i}},
                                                         {"id":6,"status":{"heatLevel":i, "heatTime": 59,"heatWorkStatus": i,"ventLevel":i,"ventTime": 59,"ventWorkStatus": i}},
                                                        ]})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                                {"out": [{"id":0,"status":{"heatLevel":i, "heatTime": 59,"heatWorkStatus": i,"ventLevel":i,"ventTime": 59,"ventWorkStatus": i}},
                                                         {"id":1,"status":{"heatLevel":i, "heatTime": 59,"heatWorkStatus": i,"ventLevel":i,"ventTime": 59,"ventWorkStatus": i}},
                                                         {"id":4,"status":{"heatLevel":i, "heatTime": 59,"heatWorkStatus": i,"ventLevel":i,"ventTime": 59,"ventWorkStatus": i}},
                                                         {"id":6,"status":{"heatLevel":i, "heatTime": 59,"heatWorkStatus": i,"ventLevel":i,"ventTime": 59,"ventWorkStatus": i}},
                                                        ]})
        self.setSeatHeatVent("主驾",0)
        self.setSeatHeatVent("副驾",0)
        self.setSeatHeatVent("二排左侧",0)
        self.setSeatHeatVent("二排右侧",0)
         #测试Time
        for i in range(len(timeValue)):
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingTime",
                                            {"params": [{"id": 0, "uint64Info": timeValue[i]},
                                                        {"id": 1, "uint64Info": timeValue[i]},
                                                        {"id": 4, "uint64Info": timeValue[i]},
                                                        {"id": 6, "uint64Info": timeValue[i]},
                                                        ]})
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingTime",
                                             {"params": [{"id": 0, "uint64Info": timeValue[i]},
                                                        {"id": 1, "uint64Info": timeValue[i]},
                                                        {"id": 4, "uint64Info": timeValue[i]},
                                                        {"id": 6, "uint64Info": timeValue[i]},
                                                        ]})
            
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                                {"out": [{"id":0,"status":{"heatLevel":0, "heatTime": timeValue[i],"heatWorkStatus": 0,"ventLevel":0,"ventTime": timeValue[i],"ventWorkStatus": 0}},
                                                         {"id":1,"status":{"heatLevel":0, "heatTime": timeValue[i],"heatWorkStatus": 0,"ventLevel":0,"ventTime": timeValue[i],"ventWorkStatus": 0}},
                                                         {"id":4,"status":{"heatLevel":0, "heatTime": timeValue[i],"heatWorkStatus": 0,"ventLevel":0,"ventTime": timeValue[i],"ventWorkStatus": 0}},
                                                         {"id":6,"status":{"heatLevel":0, "heatTime": timeValue[i],"heatWorkStatus": 0,"ventLevel":0,"ventTime": timeValue[i],"ventWorkStatus": 0}},
                                                        ]})   

    @allure.title("获取所有座椅通风加热时间_断电保持")
    @pytest.mark.smoke
    def test_caseid_1983605(self): 
        nonDefaultTime = 10
        defaultTime=59
        self.setSeatHeatVent("主驾",0)
        self.setSeatHeatVent("副驾",0)
        self.setSeatHeatVent("二排左侧",0)
        self.setSeatHeatVent("二排右侧",0)
        self.partner.empty_all(0.5)
        #设置非默认
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingTime",
                                            {"params": [{"id": 0, "uint64Info":nonDefaultTime},
                                                        {"id": 1, "uint64Info": nonDefaultTime},
                                                        {"id": 4, "uint64Info": nonDefaultTime},
                                                        {"id": 6, "uint64Info": nonDefaultTime},
                                                        ]},timeout = 1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingTime",
                                             {"params": [{"id": 0, "uint64Info": nonDefaultTime},
                                                        {"id": 1, "uint64Info": nonDefaultTime},
                                                        {"id": 4, "uint64Info": nonDefaultTime},
                                                        {"id": 6, "uint64Info": nonDefaultTime},
                                                        ]},timeout = 1)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [0,1,4,6]},
                                                {"out": [{"id":0,"status":{"heatLevel":0, "heatTime": 10,"heatWorkStatus": 0,"ventLevel":0,"ventTime": 10,"ventWorkStatus": 0}},
                                                         {"id":1,"status":{"heatLevel":0, "heatTime": 10,"heatWorkStatus": 0,"ventLevel":0,"ventTime": 10,"ventWorkStatus": 0}},
                                                         {"id":4,"status":{"heatLevel":0, "heatTime": 10,"heatWorkStatus": 0,"ventLevel":0,"ventTime": 10,"ventWorkStatus": 0}},
                                                         {"id":6,"status":{"heatLevel":0, "heatTime": 10,"heatWorkStatus": 0,"ventLevel":0,"ventTime": 10,"ventWorkStatus": 0}},
                                                        ]},timeout = 1) 
        #断电重启
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT,pause_all_bus=True, resume_all_bus=True)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [0,1,4,6]},
                                                {"out": [{"id":0,"status":{"heatLevel":0, "heatTime": 10,"heatWorkStatus": 0,"ventLevel":0,"ventTime": 10,"ventWorkStatus": 0}},
                                                         {"id":1,"status":{"heatLevel":0, "heatTime": 10,"heatWorkStatus": 0,"ventLevel":0,"ventTime": 10,"ventWorkStatus": 0}},
                                                         {"id":4,"status":{"heatLevel":0, "heatTime": 10,"heatWorkStatus": 0,"ventLevel":0,"ventTime": 10,"ventWorkStatus": 0}},
                                                         {"id":6,"status":{"heatLevel":0, "heatTime": 10,"heatWorkStatus": 0,"ventLevel":0,"ventTime": 10,"ventWorkStatus": 0}},
                                                        ]},timeout = 1)
        #设置默认
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingTime",
                                            {"params": [{"id": 0, "uint64Info":defaultTime},
                                                        {"id": 1, "uint64Info": defaultTime},
                                                        {"id": 4, "uint64Info": defaultTime},
                                                        {"id": 6, "uint64Info": defaultTime},
                                                        ]},timeout = 1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingTime",
                                             {"params": [{"id": 0, "uint64Info": defaultTime},
                                                        {"id": 1, "uint64Info": defaultTime},
                                                        {"id": 4, "uint64Info": defaultTime},
                                                        {"id": 6, "uint64Info": defaultTime},
                                                        ]},timeout = 1)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [0,1,4,6]},
                                                {"out": [{"id":0,"status":{"heatLevel":0, "heatTime": 59,"heatWorkStatus": 0,"ventLevel":0,"ventTime": 59,"ventWorkStatus": 0}},
                                                         {"id":1,"status":{"heatLevel":0, "heatTime": 59,"heatWorkStatus": 0,"ventLevel":0,"ventTime": 59,"ventWorkStatus": 0}},
                                                         {"id":4,"status":{"heatLevel":0, "heatTime": 59,"heatWorkStatus": 0,"ventLevel":0,"ventTime": 59,"ventWorkStatus": 0}},
                                                         {"id":6,"status":{"heatLevel":0, "heatTime": 59,"heatWorkStatus": 0,"ventLevel":0,"ventTime": 59,"ventWorkStatus": 0}},
                                                        ]},timeout = 2)
        
    @allure.title("所有座椅加热通风时间_首次下线")
    @pytest.mark.full
    def test_caseid_1983451(self): 
        nonDefaultTime = 10
        defaultTime=59
        self.setSeatHeatVent("主驾",0)
        self.setSeatHeatVent("副驾",0)
        self.setSeatHeatVent("二排左侧",0)
        self.setSeatHeatVent("二排右侧",0)
        self.partner.empty_all(0.5)
        #设置非默认
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingTime",
                                            {"params": [{"id": 0, "uint64Info":nonDefaultTime},
                                                        {"id": 1, "uint64Info": nonDefaultTime},
                                                        {"id": 4, "uint64Info": nonDefaultTime},
                                                        {"id": 6, "uint64Info": nonDefaultTime},
                                                        ]})
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingTime",
                                             {"params": [{"id": 0, "uint64Info": nonDefaultTime},
                                                        {"id": 1, "uint64Info": nonDefaultTime},
                                                        {"id": 4, "uint64Info": nonDefaultTime},
                                                        {"id": 6, "uint64Info": nonDefaultTime},
                                                        ]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [0,1,4,6]},
                                                {"out": [{"id":0,"status":{"heatLevel":0, "heatTime": 10,"heatWorkStatus": 0,"ventLevel":0,"ventTime": 10,"ventWorkStatus": 0}},
                                                         {"id":1,"status":{"heatLevel":0, "heatTime": 10,"heatWorkStatus": 0,"ventLevel":0,"ventTime": 10,"ventWorkStatus": 0}},
                                                         {"id":4,"status":{"heatLevel":0, "heatTime": 10,"heatWorkStatus": 0,"ventLevel":0,"ventTime": 10,"ventWorkStatus": 0}},
                                                         {"id":6,"status":{"heatLevel":0, "heatTime": 10,"heatWorkStatus": 0,"ventLevel":0,"ventTime": 10,"ventWorkStatus": 0}},
                                                        ]}) 
        #首次下线
        self.del_s2s_db()  # 删除数据库
        self.del_s2s_db()
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(30)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [0,1,4,6]},
                                                {"out": [{"id":0,"status":{"heatLevel":0, "heatTime": 59,"heatWorkStatus": 0,"ventLevel":0,"ventTime": 59,"ventWorkStatus": 0}},
                                                         {"id":1,"status":{"heatLevel":0, "heatTime": 59,"heatWorkStatus": 0,"ventLevel":0,"ventTime": 59,"ventWorkStatus": 0}},
                                                         {"id":4,"status":{"heatLevel":0, "heatTime": 59,"heatWorkStatus": 0,"ventLevel":0,"ventTime": 59,"ventWorkStatus": 0}},
                                                         {"id":6,"status":{"heatLevel":0, "heatTime": 59,"heatWorkStatus": 0,"ventLevel":0,"ventTime": 59,"ventWorkStatus": 0}},
                                                        ]})

    @allure.title("通知所有安全带状态_SequenceTime")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1983453(self):
        self.io.driver_seat_present()
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', 0)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', 1)
        sleep(1)
        A = self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts", {})["status"]["sequenceTime"]['timestamp']
        B = self.partner.send_request_and_return_resp(SEAT_SERVICE_CLIENT,"GetBeltStatusValidity", {"seats":[0]})["out"][0]['sequenceTime']['timestamp']
        B1 = self.partner.send_request_and_return_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity",
                                                      {"seats": [0]})["out"][0]['sequenceTime']['id']
        logger.info(f"----{B}")
        if A == B:
            assert True
        else:
            assert False
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', 0)
        sleep(1)
        C = self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts", {})["status"]["sequenceTime"][
            "timestamp"]
        if int(C)-int(A) >0:
            assert True
        else:
            assert False
        self.ipdu.pause_all_bus_send()
        self.BGM_down_up(2,3,10)
        self.ipdu.resume_all_bus_send()
        C1 = self.partner.send_request_and_return_resp(SEAT_SERVICE_CLIENT,"GetBeltStatusValidity",
                                                      {"seats":[0]})["out"][0]['sequenceTime']['id']
        C2 = self.partner.send_request_and_return_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity",
                                                       {"seats": [0]})["out"][0]['sequenceTime']['timestamp']

        logger.info(f"比较----{C1}--{C2}--")
        if abs(C1-B1)>0:
            if C2 < B:
                assert True
        else:
            assert False
            
    @allure.title("获取安全带未系报警状态（带功能安全参数）_信号丢失")
    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_1980566(self):
        self.sd_tester.change_usage_mode(2)
        self.Shift_Gear(2)
        self.set_four_seat_occupt(0,0,0,0)
        self.io.driver_seat_notpresent()
        self.partner.empty_all(0.5)
        
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.set_vehicle_speed(7.0)
        self.seat_belt_status(0,0,0,0,0)
        
        self.check_all_beltwarning(3)
        sleep(2)
        #由d到h通过降车速为0挂入P挡
        self.set_vehicle_speed(0.0)
        self.Shift_Gear(0)
        self.check_all_beltwarning(2)
             
        self.ipdu.pause_bus_send("backbonefr")
        sleep(2)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":0, "status": 2}},{"statusValidity":0},
                                                         {"value": {"id":1, "status": 2}},{"statusValidity":0},
                                                         {"value": {"id":4, "status": 2}},{"statusValidity":0},
                                                         {"value": {"id":5, "status": 2}},{"statusValidity":0},
                                                         {"value": {"id":6, "status": 2}},{"statusValidity":0}]})
        self.ipdu.resume_all_bus_send()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":0, "status": 2}},{"statusValidity":0},
                                                         {"value": {"id":1, "status": 2}},{"statusValidity":0},
                                                         {"value": {"id":4, "status": 2}},{"statusValidity":0},
                                                         {"value": {"id":5, "status": 2}},{"statusValidity":0},
                                                         {"value": {"id":6, "status": 2}},{"statusValidity":0}]})
        
    @allure.title("获取安全带未系报警状态（带功能安全参数）_默认值及时间戳变化")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1980561(self):
        self.sd_tester.change_usage_mode(2)
        self.Shift_Gear(3)
        self.set_four_seat_occupt(0,0,0,0)
        self.io.driver_seat_notpresent()
        self.partner.empty_all(0.5)
        #保证只有一个座椅的event上报
        self.io.driver_seat_present()
        self.seat_belt_status(0,0,0,0,0)
        self.set_vehicle_speed(6.0)
        sleep(3)
        A = self.partner.return_latest_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity")["warn"]["sequenceTime"]['timestamp']
        B = self.partner.send_request_and_return_resp(SEAT_SERVICE_CLIENT,"GetBeltWarningValidity", {"seats":[0]})["out"][0]['sequenceTime']['timestamp']
        B1 = self.partner.send_request_and_return_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity",
                                                      {"seats": [0]})["out"][0]['sequenceTime']['id']
        logger.info(f"----{A}----{B}")
        if A == B:
            assert True
        else:
            assert False
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        sleep(1)
        C = self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {})["warn"]["sequenceTime"]['timestamp']
        if int(C)-int(A) >0:
            assert True
        else:
            assert False
        self.ipdu.pause_all_bus_send()
        self.BGM_down_up(2,3,10)
        self.ipdu.resume_all_bus_send()
        C1 = self.partner.send_request_and_return_resp(SEAT_SERVICE_CLIENT,"GetBeltWarningValidity",
                                                      {"seats":[0]})["out"][0]['sequenceTime']['id']
        C2 = self.partner.send_request_and_return_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity",
                                                       {"seats": [0]})["out"][0]['sequenceTime']['timestamp']

        logger.info(f"比较----{C1}--{C2}--")
        if abs(C1-B1)>0:
            if C2 < B:
                assert True
        else:
            assert False
        
    @allure.title("启动场景获取到总线信号后_安全带状态事件发出_安全带未扣")
    @pytest.mark.smoke
    def test_caseid_1984182(self): 
        self.setSeatbeltStatusValue(0,0)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT,pause_all_bus=True, resume_all_bus=False)
        self.ckAllSeatbeltStatusNoEvent()
        self.ipdu.resume_all_bus_send()
        sleep(0.5)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts", 
                                  {"status":{"value": 1,"validity":0}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightBeltSts", 
                                  {"status":{"value": 1,"validity":0}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftBeltSts",
                                  {"status":{"value": 1,"validity":0}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearMiddleBeltSts",
                                  {"status":{"value": 1}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightBeltSts", 
                                  {"status":{"value": 1,"validity":0}})
    
    @allure.title("启动场景获取到总线信号后_安全带状态事件发出_安全带已扣")
    @pytest.mark.full
    def test_caseid_1984183(self): 
        self.setSeatbeltStatusValue(1,0)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT,pause_all_bus=True, resume_all_bus=False)
        self.ckAllSeatbeltStatusNoEvent()
        self.ipdu.resume_all_bus_send()
        sleep(0.5)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts", 
                                  {"status":{"value": 0,"validity":0}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightBeltSts", 
                                  {"status":{"value": 0,"validity":0}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftBeltSts",
                                  {"status":{"value": 0,"validity":0}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearMiddleBeltSts",
                                  {"status":{"value": 0}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightBeltSts", 
                                  {"status":{"value": 0,"validity":0}})

    @allure.title("启动场景获取到总线信号后_座椅占位状态事件发出_未占位")
    @pytest.mark.full
    def test_caseid_1984187(self): 
        self.io.driver_seat_notpresent()
        self.seat_belt_status(0,0,0,0,0)
        self.set_four_seat_occupt(3,3,3,3)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr12, 'DrvrSeatSts', 3)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(1)
        #主驾为硬线信号
        # self.check_DrvrSeatOccupt_event(0,0,0)
        self.check_four_seatoccupt_event(255,0,0)
        
    @allure.title("启动场景获取到总线信号后_座椅占位状态事件发出_已占位")
    @pytest.mark.full
    def test_caseid_1984188(self): 
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr12, 'DrvrSeatSts', 2)
        self.io.driver_seat_present()
        self.seat_belt_status(1,1,1,1,1)
        self.set_four_seat_occupt(2,2,2,2)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(1)
        self.check_DrvrSeatOccupt_event(1,1,0)
        # self.check_four_seatoccupt_event(1,1,0)
                                         
    @allure.title("启动场景获取到总线信号后_通知安全带预紧故障报警_不报警")
    @pytest.mark.full
    def test_caseid_1984227(self):
        self.ipdu.set(self.ipdu.passivesafetycan.RmlPassSafeCANFrame1, 'MsgReqForRtrctrRvsbLe', 0)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltPretensioningWarning", {"warn": 0})                                
                                         
    @allure.title("启动场景获取到总线信号后_通知安全带预紧故障报警_报警")
    @pytest.mark.full
    def test_caseid_1984228(self):
        self.ipdu.set(self.ipdu.passivesafetycan.RmlPassSafeCANFrame1, 'MsgReqForRtrctrRvsbLe', 1)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltPretensioningWarning", {"warn": 1})                                                             
    
    @allure.title("启动场景获取到总线信号后_通知安全带装配状态_装配")
    @pytest.mark.full
    def test_caseid_1984235(self):
        self.set_second_selt_equip(0)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(3)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltEquipStatus", {"id": 6, "status": 0})
        # self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltEquipStatus", {"id": 5, "status": 0})
        # self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltEquipStatus", {"id": 4, "status": 0})
        
    @allure.title("启动场景获取到总线信号后_通知安全带装配状态_未装配")
    @pytest.mark.full
    def test_caseid_1984236(self):
        self.set_second_selt_equip(1)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(1)
        # self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltEquipStatus", {"id": 4, "status": 1})
        # self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltEquipStatus", {"id": 5, "status": 1})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltEquipStatus", {"id": 6, "status": 1})
    
    @allure.title("启动场景获取到总线信号后_通知安全带未系报警状态_kNormal")
    @pytest.mark.full
    def test_caseid_1984248(self):
        #前提条件无乘客占位
        self.sd_tester.change_usage_mode(2)
        self.set_four_seat_occupt(0,0,0,0)
        self.io.driver_seat_notpresent()
        self.set_no_seatFault()
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(5)
        #SOA-22917中澄清可不发
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "BeltWarning")
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity")
    
    @allure.title("启动场景获取到总线信号后_通知安全带未系报警状态_1级报警")
    @pytest.mark.full
    def test_caseid_1984250(self):
        #前提条件无乘客占位
        self.sd_tester.change_usage_mode(13)
        self.set_four_seat_occupt(0,0,0,0)
        self.io.driver_seat_notpresent()
        #一级报警
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(0,0,0,0,0)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(3)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {}) 
        
    @allure.title("启动场景获取到总线信号后_通知座椅位置信息_默认值")
    @pytest.mark.full
    def test_caseid_1984251(self):
        self.setDefaultSeatPosition()
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatPosition",
                                             {"position":{"backAngle": 0, "longitudinalPosition":100,"verticalPosition":100,"LegrestVerticalPosition":100,"backAngleIsValid":1,"longitudinalIsValid":0,"verticalIsValid":0,"legrestVerticalIsValid":0}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatPosition",
                                             {"position":{"backAngle": 0, "longitudinalPosition":100,"verticalPosition":100,"LegrestVerticalPosition":100,"backAngleIsValid":1,"longitudinalIsValid":0,"verticalIsValid":0,"legrestVerticalIsValid":0}})

    @allure.title("启动场景获取到总线信号后_通知座椅位置信息_非默认值")
    @pytest.mark.full
    def test_caseid_1984252(self):
        self.setDefaultSeatPosition()
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'SeatBackAngleRowFirstDrvr',90)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'SeatBackAngleRowFirstPass',90)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatPosition",
                                             {"position":{"backAngle": 90, "longitudinalPosition":100,"verticalPosition":100,"LegrestVerticalPosition":100,"backAngleIsValid":1,"longitudinalIsValid":0,"verticalIsValid":0,"legrestVerticalIsValid":0}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatPosition",
                                             {"position":{"backAngle": 90, "longitudinalPosition":100,"verticalPosition":100,"LegrestVerticalPosition":100,"backAngleIsValid":1,"longitudinalIsValid":0,"verticalIsValid":0,"legrestVerticalIsValid":0}})
        
    @allure.title("启动场景获取到总线信号后_通知座椅开关按键状态_默认值")
    @pytest.mark.full
    def test_caseid_1984263(self):
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatBtnPsd', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatSwtStsDrvrSeatSwtHeiSts', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatSwtStsDrvrSeatSwtHeiFrntSts', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatSwtStsDrvrSeatSwtSldSts', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatSwtStsDrvrSeatSwtInclSts', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatSwtStsDrvrSeatSwtAdjmtOfSpplFctHozlSts', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatSwtStsDrvrSeatSwtAdjmtOfSpplFctVertSts', 0)
        
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatSwtSts2PassSeatSwtHeiSts', 0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatSwtSts2PassSeatSwtHeiFrntSts', 0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatSwtSts2PassSeatSwtSldSts', 0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatSwtSts2PassSeatSwtInclSts', 0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatSwtSts2PassSeatSwtAdjmtOfSpplFctHozlSts', 0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatSwtSts2PassSeatSwtAdjmtOfSpplFctVerSts', 0)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatSwitchStatus",
                                        {"status": {"verticalPositionSwitch": 0,"legrestVerticalPositionSwitch": 0,
                                                             "longitudinalPositionSwitch": 0,"backSwitch": 0,"isLocalSwitchActivated":0,
                                                             "lumbarLongitudinalPositionSwitch": 0,"lumbarVerticalPositionSwitch": 0,}})
        
    @allure.title("启动场景获取到总线信号后_通知座椅开关按键状态_非默认值")
    @pytest.mark.full
    def test_caseid_1984264(self):
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatBtnPsd', 1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatSwtStsDrvrSeatSwtHeiSts', 1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatSwtStsDrvrSeatSwtHeiFrntSts', 1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatSwtStsDrvrSeatSwtSldSts', 1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatSwtStsDrvrSeatSwtInclSts', 1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatSwtStsDrvrSeatSwtAdjmtOfSpplFctHozlSts', 1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatSwtStsDrvrSeatSwtAdjmtOfSpplFctVertSts', 1)
        
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatSwtSts2PassSeatSwtHeiSts', 1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatSwtSts2PassSeatSwtHeiFrntSts', 1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatSwtSts2PassSeatSwtSldSts', 1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatSwtSts2PassSeatSwtInclSts', 1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatSwtSts2PassSeatSwtAdjmtOfSpplFctHozlSts', 1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatSwtSts2PassSeatSwtAdjmtOfSpplFctVerSts', 1)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatSwitchStatus",
                                        {"status": {"verticalPositionSwitch": 1,"legrestVerticalPositionSwitch": 1,
                                                             "longitudinalPositionSwitch": 1,"backSwitch": 1,"isLocalSwitchActivated":1,
                                                             "lumbarLongitudinalPositionSwitch": 1,"lumbarVerticalPositionSwitch": 1,}})
        
    @allure.title("启动场景获取到总线信号后_座椅通风状态_默认值")
    @pytest.mark.full
    def test_caseid_1984278(self):
        self.setSeatHeatVent("主驾",0)
        self.setSeatHeatVent("副驾",0)
        self.setSeatHeatVent("二排左侧",0)
        self.setSeatHeatVent("二排右侧",0)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                                {"status":{"heatTime":59,"ventTime":59,"heatLevel":0,"heatWorkStatus": 0,"ventLevel":0,"ventWorkStatus": 0}}) 
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus",
                                                {"status":{"heatTime":59,"ventTime":59,"heatLevel":0,"heatWorkStatus": 0,"ventLevel":0,"ventWorkStatus": 0}})     
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus",
                                                {"status":{"heatTime":59,"ventTime":59,"heatLevel":0,"heatWorkStatus": 0,"ventLevel":0,"ventWorkStatus": 0}})     
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus",
                                                {"status":{"heatTime":59,"ventTime":59,"heatLevel":0,"heatWorkStatus": 0,"ventLevel":0,"ventWorkStatus": 0}})         

    @allure.title("启动场景获取到总线信号后_座椅通风状态_非默认值")
    @pytest.mark.full
    def test_caseid_1984279(self):
        self.setSeatHeatVent("主驾",1)
        self.setSeatHeatVent("副驾",1)
        self.setSeatHeatVent("二排左侧",1)
        self.setSeatHeatVent("二排右侧",1)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                                {"status":{"heatTime":59,"ventTime":59,"heatLevel":1,"heatWorkStatus": 1,"ventLevel":1,"ventWorkStatus": 1}},timeout=5) 
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus",
                                                {"status":{"heatTime":59,"ventTime":59,"heatLevel":1,"heatWorkStatus": 1,"ventLevel":1,"ventWorkStatus": 1}},timeout=5)   
        #后排信号是非周期性，重启后不会下发  
        self.setSeatHeatVent("二排左侧",1)
        self.setSeatHeatVent("二排右侧",1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus",
                                                {"status":{"heatTime":59,"ventTime":59,"heatLevel":1,"heatWorkStatus": 1,"ventLevel":1,"ventWorkStatus": 1}},timeout=5)     
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus",
                                                {"status":{"heatLevel":1,"heatTime":59,"heatWorkStatus":1,"ventLevel":1,"ventTime":59,"ventWorkStatus":1}},timeout=5)         

    @allure.title("启动场景获取到总线信号后_通知座椅系统状态_默认值")
    @pytest.mark.full
    def test_caseid_1984299(self):
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetMassageConf",
                                         {"params": [{"id": 0, "conf": {"isOn": True, "type": 0, "intensity": 0}},
                                                     {"id": 1, "conf": {"isOn": True, "type": 0, "intensity": 0}}]}, timeout = 0.5)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd',0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatInAutMovmt',0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrMassgRunng',0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatInAutMovmt',0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassMassgRunng',0)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT,"SeatSysStatus", {})
         
    @allure.title("启动场景获取到总线信号后_通知座椅系统状态_非默认值")
    @pytest.mark.full
    def test_caseid_1984301(self):
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetMassageConf",
                                         {"params": [{"id": 0, "conf": {"isOn": True, "type": 0, "intensity": 0}},
                                                     {"id": 1, "conf": {"isOn": True, "type": 0, "intensity": 0}}]})
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd',1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatInAutMovmt',1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrMassgRunng',1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatInAutMovmt',1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassMassgRunng',1)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT,"SeatSysStatus", {})
        
    @allure.title("启动场景获取到总线信号后_通知座椅系统状态_有故障")
    @pytest.mark.full
    def test_caseid_1984302(self):
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts', 1)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecLeBltLockSts', 1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecMidBltLockSts', 1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecRiBltLockSts', 1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF', 1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF', 1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', 1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiQF', 1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldQF', 1)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatFault",
                                  {"faults": [{"faultId": 6, "faultMsg": "", "seatId": 0},
                                              {"faultId": 6, "faultMsg": "", "seatId": 1},
                                              {"faultId": 6, "faultMsg": "", "seatId": 4},
                                              {"faultId": 6, "faultMsg": "", "seatId": 5},
                                              {"faultId": 6, "faultMsg": "", "seatId": 6},
                                              {"faultId": 8, "faultMsg": "", "seatId": 0},
                                              {"faultId": 8, "faultMsg": "", "seatId": 1}]})
        
    @allure.title("启动场景获取到总线信号后_通知座椅系统状态_无故障")
    @pytest.mark.full
    def test_caseid_1984303(self):
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecLeBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecMidBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecRiBltLockSts', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldQF', 3)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatFault",
                                    {"faults": [{"faultId": 0, "faultMsg": "", "seatId": 12}]})
   
    @allure.title("启动场景获取到总线信号后_通知车内有人_非默认值")
    @pytest.mark.full
    def test_caseid_1988601(self):
        self.io.driver_seat_present()
        self.partner.empty_all(0.5)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":True,"userInVehicleStatusWithCam":True}})

    @allure.title("启动场景获取到总线信号后_通知车内有人_默认值")
    @pytest.mark.full
    def test_caseid_1988602(self):
        self.set_nopeople_incar()
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":False,"userInVehicleStatusWithCam":False}})

    @allure.title("信号切换时座椅加热下行PDU校验")
    @pytest.mark.smoke
    def test_caseid_1984528(self):
        oldSignalValue = [0,1,2]
        newSignalValue = [3,4,5]
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            logger.info(f"使用者模式={X}")
            for Y in range(3):
                self.setHeatVentingLevel(1,0)
                sleep(1)
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', 1),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', 1),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', 1),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', 1)])  
              
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgAvlSts', oldSignalValue[Y])
                sleep(0.5)
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgAvlSts', newSignalValue[Y])
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', 0),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', 1),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', 1),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', 1)])
                self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgAvlSts', oldSignalValue[Y])
                sleep(0.5)
                self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgAvlSts', newSignalValue[Y])
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', 0),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', 0),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', 1),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', 1)])
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecLe', oldSignalValue[Y])
                sleep(0.5)
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecLe', newSignalValue[Y])
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', 0),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', 0),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', 0),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', 1)])
                
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecRi', oldSignalValue[Y])
                sleep(0.5)
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecRi', newSignalValue[Y])
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', 0),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', 0),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', 0),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', 0)])            
    @allure.title("信号切换时座椅通风下行PDU校验")
    @pytest.mark.full
    def test_caseid_1984529(self):
        oldSignalValue = [0,1,2]
        newSignalValue = [3,4,5]
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            for Y in range(3):
                self.setHeatVentingLevel(0,1)
                sleep(1)
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', 1),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowFirstRi', 1),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecLe', 1),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecRi', 1)])
        
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentAvlSts', oldSignalValue[Y])
                sleep(0.5)
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentAvlSts', newSignalValue[Y])
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowFirstRi', 1),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecLe', 1),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecRi', 1)])
                self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentAvlSts', oldSignalValue[Y])
                sleep(0.5)
                self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentAvlSts', newSignalValue[Y])
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowFirstRi', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecLe', 1),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecRi', 1)])
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecLe', oldSignalValue[Y])
                sleep(0.5)
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecLe', newSignalValue[Y])
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowFirstRi', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecRi', 1)])
                
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecRi', oldSignalValue[Y])
                sleep(0.5)
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecRi', newSignalValue[Y])
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowFirstRi', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecRi', 0)])#

    @allure.title("座椅加热取消优先级限制_Usagemode上切挡位下发_挡位无变化")
    @pytest.mark.sanity
    def test_caseid_1984580(self): 
        def return_info(value):
            return (value-1) if (value>1) else 3 
        self.partner.empty_all(1) 
        for i in [1,2,3]:
            for j in [2,11,13]:
                self.setHeatVentingLevel(0,1)
                self.sd_tester.change_usage_mode(1)
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                    {"params": [{"id": 0, "uint8Info": i},
                                                {"id": 1, "uint8Info": return_info(i)},
                                                {"id": 4, "uint8Info": i},
                                                {"id": 6, "uint8Info": return_info(i)}]})
                self.sd_tester.change_usage_mode(j)
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', 0),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', 0),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', 0),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', 0)]) 
                sleep(0.5)
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', i),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', return_info(i)),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', i),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', return_info(i))]) 
                
    @allure.title("座椅通风取消优先级限制_Usagemode上切挡位下发_挡位无变化")
    @pytest.mark.full
    def test_caseid_1984582(self): 
        def return_info(value):
            return (value-1) if (value>1) else 3 
        self.partner.empty_all(1) 
        for i in [1,2,3]:
            for j in [2,11,13]:
                self.setHeatVentingLevel(1,0)
                self.sd_tester.change_usage_mode(1)
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                    {"params": [{"id": 0, "uint8Info": i},
                                                {"id": 1, "uint8Info": return_info(i)},
                                                {"id": 4, "uint8Info": i},
                                                {"id": 6, "uint8Info": return_info(i)}]})
                self.sd_tester.change_usage_mode(j)
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowFirstRi', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecRi', 0)])
                sleep(0.5)
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', i),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowFirstRi', return_info(i)),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecLe', i),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecRi', return_info(i))])
                
    @allure.title("座椅加热取消优先级限制_Usagemode上切挡位下发_500ms挡位有变化")
    @pytest.mark.full
    def test_caseid_1984583(self): 
        def return_info(value):
            return (value-1) if (value>1) else 3 
        self.partner.empty_all(1) 
        for i in [1,2,3]:
            for j in [2,11,13]:
                self.setHeatVentingLevel(0,1)
                self.sd_tester.change_usage_mode(1)
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                    {"params": [{"id": 0, "uint8Info": i},
                                                {"id": 1, "uint8Info": return_info(i)},
                                                {"id": 4, "uint8Info": i},
                                                {"id": 6, "uint8Info": return_info(i)}]})
                self.sd_tester.change_usage_mode(j)
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', 0),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', 0),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', 0),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', 0)]) 
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                     {"params": [{"id": 0, "uint8Info": return_info(i)},
                                                {"id": 1, "uint8Info": i},
                                                {"id": 4, "uint8Info": return_info(i)},
                                                {"id": 6, "uint8Info": i}]})
                sleep(0.5)
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', return_info(i)),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', i),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', return_info(i)),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', i)]) 
    
    @allure.title("座椅通风取消优先级限制_Usagemode上切挡位下发_500ms挡位有变化")
    @pytest.mark.full
    def test_caseid_1984934(self): 
        def return_info(value):
            return (value-1) if (value>1) else 3 
        self.partner.empty_all(1) 
        for i in [1,2,3]:
            for j in [2,11,13]:
                self.setHeatVentingLevel(0,1)
                self.sd_tester.change_usage_mode(1)
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                    {"params": [{"id": 0, "uint8Info": i},
                                                {"id": 1, "uint8Info": return_info(i)},
                                                {"id": 4, "uint8Info": i},
                                                {"id": 6, "uint8Info": return_info(i)}]})
                self.sd_tester.change_usage_mode(j)
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowFirstRi', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecLe', 0),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecRi', 0)])
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                     {"params": [{"id": 0, "uint8Info": return_info(i)},
                                                {"id": 1, "uint8Info": i},
                                                {"id": 4, "uint8Info": return_info(i)},
                                                {"id": 6, "uint8Info": i}]})
                sleep(0.5)
                self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', return_info(i)),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowFirstRi', i),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecLe', return_info(i)),
                                                (self.ipdu.bodycan.CemBodyFr01,'HmiSeatClimaHmiSeatVentnForRowSecRi', i)])
    
    #需求中的通风加热 指level，且只有SetHeatingLevel与当前挡位一致时才需有1s等待 SOA-25109      
    @allure.title("座椅加热取消优先级限制_加热状态非0到0")
    @pytest.mark.full
    def test_caseid_1984937(self): 
        for i in [1,2,3]:
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                        {"params": [{"id": 0, "uint8Info": i},
                                                    {"id": 1, "uint8Info": i},
                                                    {"id": 4, "uint8Info": i},
                                                    {"id": 6, "uint8Info": i}]})
            self.setSeatHeatLevel(i,i,i,i)
            sleep(2)
            self.setSeatHeatLevel(0,0,0,0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                            {"out": [{"id":0,"status":{"heatLevel":i}},
                                                        {"id":1,"status":{"heatLevel":i}},
                                                        {"id":4,"status":{"heatLevel":i}},
                                                        {"id":6,"status":{"heatLevel":i}},
                                                    ]},timeout = 0.2)
            
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                            {"status":{"heatLevel":0}})
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus",
                                        {"status":{"heatLevel":0}}) 
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus",
                                        {"status":{"heatLevel":0}}) 
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus",
                                        {"status":{"heatLevel":0}}) 
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                            {"out": [{"id":0,"status":{"heatLevel":0}},
                                                        {"id":1,"status":{"heatLevel":0}},
                                                        {"id":4,"status":{"heatLevel":0}},
                                                        {"id":6,"status":{"heatLevel":0}},
                                                    ]},timeout = 1)
    
    @allure.title("座椅通风取消优先级限制_通风状态非0到0")
    @pytest.mark.full
    def test_caseid_1984938(self): 
        for i in [1,2,3]:
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                        {"params": [{"id": 0, "uint8Info": i},
                                                    {"id": 1, "uint8Info": i},
                                                    {"id": 4, "uint8Info": i},
                                                    {"id": 6, "uint8Info": i}]})
            self.setSeatVentLevel(i,i,i,i)
            sleep(0.5)
            self.setSeatVentLevel(0,0,0,0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                            {"out": [{"id":0,"status":{"ventLevel":i}},
                                                        {"id":1,"status":{"ventLevel":i}},
                                                        {"id":4,"status":{"ventLevel":i}},
                                                        {"id":6,"status":{"ventLevel":i}},
                                                    ]},timeout = 0.2)
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                            {"status":{"ventLevel":0}})
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus",
                                        {"status":{"ventLevel":0}}) 
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus",
                                        {"status":{"ventLevel":0}}) 
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus",
                                        {"status":{"ventLevel":0}}) 
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                            {"out": [{"id":0,"status":{"ventLevel":0}},
                                                        {"id":1,"status":{"ventLevel":0}},
                                                        {"id":4,"status":{"ventLevel":0}},
                                                        {"id":6,"status":{"ventLevel":0}},
                                                    ]},timeout = 1)
                
    @allure.title("座椅加热取消优先级限制_加热状态非0到0到非0")
    @pytest.mark.full
    def test_caseid_1984940(self): 
        def return_info(value):
            return (value-1) if (value>1) else 3 
        for i in [1,2,3]:
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                        {"params": [{"id": 0, "uint8Info": i},
                                                    {"id": 1, "uint8Info": i},
                                                    {"id": 4, "uint8Info": i},
                                                    {"id": 6, "uint8Info": i}]})
           
            self.setSeatHeatLevel(i,i,i,i)
            sleep(0.5)
            self.setSeatHeatLevel(0,0,0,0)
            sleep(0.5)
            self.setSeatHeatLevel(return_info(i),return_info(i),return_info(i),return_info(i))
 
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                            {"status":{"heatLevel":return_info(i)}})
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus",
                                        {"status":{"heatLevel":return_info(i)}}) 
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus",
                                        {"status":{"heatLevel":return_info(i)}}) 
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus",
                                        {"status":{"heatLevel":return_info(i)}}) 
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                            {"out": [{"id":0,"status":{"heatLevel":return_info(i)}},
                                                        {"id":1,"status":{"heatLevel":return_info(i)}},
                                                        {"id":4,"status":{"heatLevel":return_info(i)}},
                                                        {"id":6,"status":{"heatLevel":return_info(i)}},
                                                    ]},timeout = 0.5)
    
    @allure.title("座椅通风取消优先级限制_通风状态非0到0到非0")
    @pytest.mark.full
    def test_caseid_1984941(self): 
        def return_info(value):
            return (value-1) if (value>1) else 3 
        for i in [1,2,3]:
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                        {"params": [{"id": 0, "uint8Info": i},
                                                    {"id": 1, "uint8Info": i},
                                                    {"id": 4, "uint8Info": i},
                                                    {"id": 6, "uint8Info": i}]})
            self.setSeatVentLevel(i,i,i,i)
            sleep(0.5)
            self.setSeatVentLevel(0,0,0,0)
            sleep(0.5)
            self.setSeatVentLevel(return_info(i),return_info(i),return_info(i),return_info(i))

            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                            {"status":{"ventLevel":return_info(i)}})
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus",
                                        {"status":{"ventLevel":return_info(i)}}) 
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus",
                                        {"status":{"ventLevel":return_info(i)}}) 
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus",
                                        {"status":{"ventLevel":return_info(i)}}) 
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                            {"out": [{"id":0,"status":{"ventLevel":return_info(i)}},
                                                        {"id":1,"status":{"ventLevel":return_info(i)}},
                                                        {"id":4,"status":{"ventLevel":return_info(i)}},
                                                        {"id":6,"status":{"ventLevel":return_info(i)}},
                                                    ]},timeout = 1)
    
    @allure.title("座椅加热取消优先级限制_加热状态非0到非0")
    @pytest.mark.full
    def test_caseid_1984942(self): 
        def return_info(value):
            return (value-1) if (value>1) else 3 
        for i in [1,2,3]:
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                        {"params": [{"id": 0, "uint8Info": i},
                                                    {"id": 1, "uint8Info": i},
                                                    {"id": 4, "uint8Info": i},
                                                    {"id": 6, "uint8Info": i}]})
            
            self.setSeatHeatLevel(i,i,i,i)
            sleep(0.5)
            self.setSeatHeatLevel(return_info(i), return_info(i),return_info(i),return_info(i))
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                            {"status":{"heatLevel":return_info(i)}})
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus",
                                        {"status":{"heatLevel":return_info(i)}}) 
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus",
                                        {"status":{"heatLevel":return_info(i)}}) 
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus",
                                        {"status":{"heatLevel":return_info(i)}}) 
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                            {"out": [{"id":0,"status":{"heatLevel":return_info(i)}},
                                                        {"id":1,"status":{"heatLevel":return_info(i)}},
                                                        {"id":4,"status":{"heatLevel":return_info(i)}},
                                                        {"id":6,"status":{"heatLevel":return_info(i)}},
                                                    ]},timeout = 0.5)
                
    @allure.title("座椅通风取消优先级限制_通风状态非0到非0")
    @pytest.mark.full
    def test_caseid_1984943(self): 
        def return_info(value):
            return (value-1) if (value>1) else 3 
        for i in [1,2,3]:
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                        {"params": [{"id": 0, "uint8Info": i},
                                                    {"id": 1, "uint8Info": i},
                                                    {"id": 4, "uint8Info": i},
                                                    {"id": 6, "uint8Info": i}]})
            self.setSeatVentLevel(i,i,i,i)
            sleep(0.5)
            self.setSeatVentLevel(return_info(i),return_info(i),return_info(i),return_info(i))

            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                            {"status":{"ventLevel":return_info(i)}})
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus",
                                        {"status":{"ventLevel":return_info(i)}}) 
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus",
                                        {"status":{"ventLevel":return_info(i)}}) 
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus",
                                        {"status":{"ventLevel":return_info(i)}}) 
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                            {"out": [{"id":0,"status":{"ventLevel":return_info(i)}},
                                                        {"id":1,"status":{"ventLevel":return_info(i)}},
                                                        {"id":4,"status":{"ventLevel":return_info(i)}},
                                                        {"id":6,"status":{"ventLevel":return_info(i)}},
                                                    ]},timeout = 1)

    #车内有人
    @allure.title("车内有人状态判断_默认值")
    @pytest.mark.full
    def test_caseid_1985502(self): 
        #重启前设置车内有人
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts', 1)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVehicleInsidePersonSts", {},
                                            {"out":{"userInVehicleStatus":True,"userInVehicleStatusWithCam":True}}, timeout = 1)                                     
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVehicleInsidePersonSts", {},
                                            {"out":{"userInVehicleStatus":False,"userInVehicleStatusWithCam":False}}, timeout = 1)                                     
        self.ipdu.resume_all_bus_send()
        
    @allure.title("车内有人状态判断_任意座位有人到所有座位无人_门开时")
    @pytest.mark.sanity
    def test_caseid_1985505(self): 
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.set_four_Door_open()
        for i in range(5):
            self.set_four_seat_occupt_onlyone(i)
            logger.info(f"当前信号{i}")
            self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":True}},
                                    "GetVehicleInsidePersonSts", {})
            self.io.driver_seat_notpresent()
            self.set_four_seat_occupt(0,0,0,0)
            self.partner.ck_coming_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":False}},
                                    "GetVehicleInsidePersonSts", {},timeout=3)
                 
    @allure.title("车内有人状态判断_任意座位有人_任意门打开期间任意座位有人")
    @pytest.mark.sanity
    def test_caseid_1985508(self): 
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.set_four_Door_close()
        for i in range(5):
            for j in range(4):
                self.set_four_seat_occupt_onlyone(i)
                self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":True}},
                                    "GetVehicleInsidePersonSts", {})
                self.set_four_Door_open_onlyone(j)
                #门开期间确认无人
                self.io.driver_seat_notpresent()
                self.set_four_seat_occupt(0,0,0,0)
                self.partner.ck_coming_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":False}},
                                    "GetVehicleInsidePersonSts", {},timeout=3)
                self.set_four_Door_close()
    
    @allure.title("车内有人状态判断_任意座位有人_任意门打开到关闭_关闭时无人")
    @pytest.mark.full
    def test_caseid_1985511(self): 
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.set_four_Door_close()
        for i in range(5):
            for j in range(4):
                self.set_four_seat_occupt_onlyone(i)
                self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":True}},
                                    "GetVehicleInsidePersonSts", {})
                self.set_four_Door_open_onlyone(j)
                self.io.driver_seat_notpresent()
                self.set_four_seat_occupt(0,0,0,0)
                #门关后确认无人
                self.set_four_Door_close()
                self.partner.ck_coming_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":False}},
                                    "GetVehicleInsidePersonSts", {},timeout=3)
        
    @allure.title("车内有人状态判断_门开所有座无人_关闭期间任意座有人")
    @pytest.mark.full
    def test_caseid_1985512(self): 
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.set_four_Door_open()
        for i in range(5):
            self.set_four_seat_occupt_onlyone(i)
            self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":True}},
                                    "GetVehicleInsidePersonSts", {})
            self.set_four_Door_close()
            self.io.drvr_door_open()
            self.io.driver_seat_notpresent()
            self.set_four_seat_occupt(0,0,0,0)
            self.partner.ck_coming_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":False}},
                                    "GetVehicleInsidePersonSts", {},timeout=3)
        
    @allure.title("车内有人状态判断_车内有人_所有门关_无法切换到车内无人")
    @pytest.mark.full
    def test_caseid_1985608(self): 
        for i in range(5):
            self.io.driver_seat_notpresent()
            self.set_four_seat_occupt(0,0,0,0)
            self.set_four_Door_close()
            self.partner.empty_all(0.5)
            self.set_four_seat_occupt_onlyone(i)
            logger.info(f"当前信号{i}")
            self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":True}},
                                    "GetVehicleInsidePersonSts", {})
            self.io.driver_seat_notpresent()
            self.set_four_seat_occupt(0,0,0,0)
            self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",timeout=4)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVehicleInsidePersonSts", {},
                                                    {"out":{"userInVehicleStatus":True}})
            self.set_four_Door_close()
            self.io.drvr_door_open()
            self.io.driver_seat_notpresent()
            self.set_four_seat_occupt(0,0,0,0)
            self.partner.ck_coming_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":False}},
                                    "GetVehicleInsidePersonSts", {},timeout=3)      
            
    @allure.title("车内有人状态判断_门开_无占位_3s内变为有占位&门开_无占位_关门_3s内有占位")
    @pytest.mark.full
    def test_caseid_1985616(self): 
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.set_four_Door_open()
        self.io.driver_seat_present()
        self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":True}},
                                    "GetVehicleInsidePersonSts", {})
        self.io.driver_seat_notpresent()
        sleep(1)
        self.io.driver_seat_present()
        sleep(3)
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts")
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVehicleInsidePersonSts", {},
                                                    {"out": {"userInVehicleStatus":True}})
        self.io.driver_seat_notpresent()
        self.partner.ck_coming_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":False}},
                                    "GetVehicleInsidePersonSts", {},timeout=3, deviation=0.3)
        self.set_four_Door_close()   
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts', 2)   
        self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":True}},
                                    "GetVehicleInsidePersonSts", {})
    
    @allure.title("融合视觉的车内有人状态_UserInVehicleStatus为True_视觉感知主副驾无人_errorCode为0")
    @pytest.mark.smoke
    def test_caseid_1985516(self): 
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.set_four_Door_close()
        self.partner.empty_all(1)
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                                                    {"firstLeftExist":False,"firstRightExist":False,"errorCode":0}})
        for i in range(5):
            for j in range(4):
                self.set_four_seat_occupt_onlyone(i)
                logger.info(f"当前信号{i}")
                self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatusWithCam":True}},
                                    "GetVehicleInsidePersonSts", {})
                self.set_four_Door_open_onlyone(j)
                logger.info(f"当前信号{j}")
                #门开期间确认无人
                self.io.driver_seat_notpresent()
                self.set_four_seat_occupt(0,0,0,0)
                self.partner.ck_coming_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatusWithCam":False}},
                                    "GetVehicleInsidePersonSts", {},timeout=3)   
                self.set_four_Door_close()
    
    @allure.title("融合视觉的车内有人状态_UserInVehicleStatus为True_视觉感知主副驾无人_errorCode不为0")
    @pytest.mark.full
    def test_caseid_1985517(self): 
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.set_four_Door_close()
        for k in [1,2,3,4]:
            self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                            {"firstLeftExist":False,"firstRightExist":False,"errorCode":k}})                                                            
            for i in range(5):
                for j in range(4):
                    self.set_four_seat_occupt_onlyone(i)
                    self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatusWithCam":True}},
                                    "GetVehicleInsidePersonSts", {})
                    self.set_four_Door_open_onlyone(j)
                    #门开期间确认无人
                    self.io.driver_seat_notpresent()
                    self.set_four_seat_occupt(0,0,0,0)
                    sleep(1)
                    self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts")
                    sleep(2)
                    self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatusWithCam":False}},
                                    "GetVehicleInsidePersonSts", {})
                    self.set_four_Door_close()
                    
    @allure.title("融合视觉的车内有人状态_UserInVehicleStatus为False_视觉感知主副驾有人")
    @pytest.mark.full
    def test_caseid_1985518(self): 
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                            {"firstLeftExist":False,"firstRightExist":False,"errorCode":0}})         
        for firstLeftExistValue in [False,True]:
            for firstRightExistValue in [False,True]:
                for errorCodeValue in [0,1,2,3,4]:
                    logger.info(f"firstLeftExistValue={firstLeftExistValue},firstRightExistValue={firstRightExistValue},errorCodeValue={errorCodeValue}")
                    self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                            {"firstLeftExist":firstLeftExistValue,"firstRightExist":firstRightExistValue,"errorCode":errorCodeValue}})  
                    if (firstLeftExistValue == 0 and firstRightExistValue == 1 and errorCodeValue == 0) or \
                        (firstLeftExistValue == 1 and firstRightExistValue == 0 and errorCodeValue == 0) or\
                            (firstLeftExistValue == 1 and firstRightExistValue == 1 and errorCodeValue == 0):
                        self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatusWithCam":True}},
                                    "GetVehicleInsidePersonSts", {})
                    elif (firstLeftExistValue == 0 and firstRightExistValue == 1 and errorCodeValue == 1) or \
                         (firstLeftExistValue == 1 and firstRightExistValue == 0 and errorCodeValue == 1) or \
                              (firstLeftExistValue == 1 and firstRightExistValue == 1 and errorCodeValue == 1):
                        self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatusWithCam":False}},
                                    "GetVehicleInsidePersonSts", {})
                    else:self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts")
                        
    @allure.title("融合视觉的车内有人状态_UserInVehicleStatus与视觉感知主副驾有人切换")
    @pytest.mark.full
    def test_caseid_1985519(self):
        self.io.driver_seat_present()
        self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":True}},
                                    "GetVehicleInsidePersonSts", {})
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                            {"firstLeftExist":True,"firstRightExist":False,"errorCode":0}}) 
                
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts")
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVehicleInsidePersonSts", {},
                                                    {"out":{"userInVehicleStatusWithCam":True}})
        self.io.drvr_door_open()
        self.io.driver_seat_notpresent()
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts", timeout=2)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVehicleInsidePersonSts", {},
                                                    {"out":{"userInVehicleStatusWithCam":True}})
        
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                            {"firstLeftExist":False,"firstRightExist":False,"errorCode":1}})         
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts")
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVehicleInsidePersonSts", {},
                                                    {"out":{"userInVehicleStatusWithCam":True}})
        
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                            {"firstLeftExist":False,"firstRightExist":True,"errorCode":0}})         
        self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatusWithCam":True}},
                                    "GetVehicleInsidePersonSts", {})   
        self.io.driver_seat_present()
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                            {"firstLeftExist":False,"firstRightExist":False,"errorCode":1}})         
        self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatusWithCam":True}},
                                    "GetVehicleInsidePersonSts", {})
        
    #座椅通风加热请求源
    @allure.title("座椅通风加热等级_请求源赋值逻辑测试")
    @pytest.mark.sanity
    def test_caseid_1985590(self):
        a, b, c, d = [0,1,2], [1,2,0], [2,0,1], [0,2,1]
        A, B, C, D = [1,2,0], [2,0,1], [0,2,1], [0,1,2]
        for i in [2,0,11,1,13]:
            logger.info(f"i=={i}")
            self.sd_tester.change_usage_mode(i)
            for j in range(3):
                logger.info(f"j=={j}")
                self.setHeatLevelSource([0,0,a[j]], [1,0,b[j]], [4,0,c[j]], [6,0,d[j]])
                sleep(1)
                self.setVentLevelSource([0,0,A[j]], [1,0,B[j]], [4,0,C[j]], [6,0,D[j]])
                sleep(1)
                if i == 2 or i == 11 or i == 13:
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetHeatingLevel", {"seats": [3]}, 
                                                {"out": [{"id": 0, "source": A[j]},{"id": 1, "source": B[j]}]})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetHeatingLevel", {"seats": [7]}, 
                                                {"out": [{"id": 4, "source": C[j]},{"id": 6, "source": D[j]}]})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetHeatingLevel", {"seats": [12]}, 
                                                {"out": [{"id": 0, "source": A[j]},{"id": 1, "source": B[j]},
                                                        {"id": 4, "source": C[j]},{"id": 6, "source": D[j]}]})
                    
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVentingLevel", {"seats": [3]}, 
                                                {"out": [{"id": 0, "source": A[j]},{"id": 1, "source": B[j]}]})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVentingLevel", {"seats": [7]}, 
                                                {"out": [{"id": 4, "source": C[j]},{"id": 6, "source": D[j]}]})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVentingLevel", {"seats": [12]}, 
                                                {"out": [{"id": 0, "source": A[j]},{"id": 1, "source": B[j]},
                                                        {"id": 4, "source": C[j]},{"id": 6, "source": D[j]}]})
                else:
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetHeatingLevel", {"seats": [12]}, 
                                                {"out": [{"id": 0, "source": 0},{"id": 1, "source": 0},
                                                        {"id": 4, "source": 0},{"id": 6, "source": 0}]})  
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVentingLevel", {"seats": [12]}, 
                                                {"out": [{"id": 0, "source": 0},{"id": 1, "source": 0},
                                                        {"id": 4, "source": 0},{"id": 6, "source": 0}]})  
    
    @allure.title("座椅通风加热等级_请求源赋值逻辑测试_BGM重启")
    @pytest.mark.full
    def test_caseid_1985591(self):
        self.sd_tester.change_usage_mode(2)
        self.setHeatLevelSource([0,0,2], [1,0,2], [4,0,2], [6,0,2])
        sleep(1)
        self.setVentLevelSource([0,0,2], [1,0,2], [4,0,2], [6,0,2])
        sleep(1)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetHeatingLevel", {"seats": [12]}, 
                                    {"out": [{"id": 0, "source": 2},{"id": 1, "source": 2},
                                            {"id": 4, "source": 2},{"id": 6, "source": 2}]})
        
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVentingLevel", {"seats": [12]}, 
                                    {"out": [{"id": 0, "source": 2},{"id": 1, "source": 2},
                                            {"id": 4, "source": 2},{"id": 6, "source": 2}]})
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT, pause_all_bus=False)   
        sleep(2)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetHeatingLevel", {"seats": [12]}, 
                                                {"out": [{"id": 0, "source": 0},{"id": 1, "source": 0},
                                                        {"id": 4, "source": 0},{"id": 6, "source": 0}]})  
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVentingLevel", {"seats": [12]}, 
                                                {"out": [{"id": 0, "source": 0},{"id": 1, "source": 0},
                                                        {"id": 4, "source": 0},{"id": 6, "source": 0}]}) 
        sleep(30)
        
    @allure.title("座椅通风加热状态_请求源赋值逻辑测试")
    @pytest.mark.sanity
    def test_caseid_1985592(self):
        a, b, c, d = [0,1,2], [1,2,0], [2,0,1], [0,2,1]
        A, B, C, D = [1,2,0], [2,0,1], [0,1,2], [1,0,2]
        for i in [2,0,11,1,13]:
            logger.info(f"i=={i}")
            self.sd_tester.change_usage_mode(i)
            for j in range(3):
                logger.info(f"j=={j}")
                self.setHeatLevelSource([0,0,a[j]], [1,0,b[j]], [4,0,c[j]], [6,0,d[j]])
                self.partner.empty_all(0.5)
                self.setVentLevelSource([0,0,A[j]], [1,0,B[j]], [4,0,C[j]], [6,0,D[j]])
                if i == 2 or i == 11 or i == 13:
                    logger.info(f"A[j]=={A[j]},B[j]=={B[j]},C[j]=={C[j]},D[j]=={D[j]}")
                    #此处使用ck_s2s_event 防止校验后面时 通知已经发出
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                                {"status":{"source":A[j]}})
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus",
                                                {"status":{"source":B[j]}}) 
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus",
                                                {"status":{"source":C[j]}}) 
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus",
                                                {"status":{"source":D[j]}})    
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                               {"out": [{"id":0,"status":{"source":A[j]}},
                                                        {"id":1,"status":{"source":B[j]}},
                                                        {"id":4,"status":{"source":C[j]}},
                                                        {"id":6,"status":{"source":D[j]}},
                                                        ]})
                else:
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                               {"out": [{"id":0,"status":{"source":0}},
                                                        {"id":1,"status":{"source":0}},
                                                        {"id":4,"status":{"source":0}},
                                                        {"id":6,"status":{"source":0}},
                                                        ]})
                
                self.setVentLevelSource([0,0,A[j]], [1,0,B[j]], [4,0,C[j]], [6,0,D[j]])
                self.partner.empty_all(0.5)
                self.setHeatLevelSource([0,0,a[j]], [1,0,b[j]], [4,0,c[j]], [6,0,d[j]])
                if i == 2 or i == 11 or i == 13:
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                                {"status":{"source":a[j]}})
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus",
                                                {"status":{"source":b[j]}}) 
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus",
                                                {"status":{"source":c[j]}}) 
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus",
                                                {"status":{"source":d[j]}})   
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                               {"out": [{"id":0,"status":{"source":a[j]}},
                                                        {"id":1,"status":{"source":b[j]}},
                                                        {"id":4,"status":{"source":c[j]}},
                                                        {"id":6,"status":{"source":d[j]}},
                                                        ]})
                else:
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                               {"out": [{"id":0,"status":{"source":0}},
                                                        {"id":1,"status":{"source":0}},
                                                        {"id":4,"status":{"source":0}},
                                                        {"id":6,"status":{"source":0}},
                                                        ]})
                    
    @allure.title("座椅通风加热状态_请求源赋值逻辑测试_BGM重启")
    @pytest.mark.full
    def test_caseid_1985593(self):
        self.sd_tester.change_usage_mode(2)
        self.setHeatLevelSource([0,0,0], [1,0,0], [4,0,0], [6,0,0])
        self.partner.empty_all(0.5)
        self.setVentLevelSource([0,0,1], [1,0,1], [4,0,1], [6,0,1])

        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                                {"status":{"source":1}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus",
                                    {"status":{"source":1}}) 
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus",
                                    {"status":{"source":1}}) 
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus",
                                    {"status":{"source":1}})  
        
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                               {"out": [{"id":0,"status":{"source":1}},
                                                        {"id":1,"status":{"source":1}},
                                                        {"id":4,"status":{"source":1}},
                                                        {"id":6,"status":{"source":1}},
                                                        ]})
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT, pause_all_bus=False)   
        sleep(2)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                                {"status":{"source":0}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus",
                                    {"status":{"source":0}}) 
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus",
                                    {"status":{"source":0}}) 
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus",
                                    {"status":{"source":0}}) 
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                               {"out": [{"id":0,"status":{"source":0}},
                                                        {"id":1,"status":{"source":0}},
                                                        {"id":4,"status":{"source":0}},
                                                        {"id":6,"status":{"source":0}},
                                                        ]})   
        
    @allure.title("座椅通风加热_请求源赋值默认值测试")
    @pytest.mark.full
    def test_caseid_1985594(self):
        self.sd_tester.change_usage_mode(2)
        self.setHeatLevelSource([0,0,0], [1,0,0], [4,0,0], [6,0,0])
        self.setVentLevelSource([0,0,0], [1,0,0], [4,0,0], [6,0,0])

        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                    {"params": [{"id": 0, "uint8Info": 0}]},timeout =0.5)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                    {"params": [{"id": 1, "uint8Info": 0}]},timeout =0.5)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                    {"params": [{"id": 4, "uint8Info": 0}]},timeout =0.5)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                    {"params": [{"id": 6, "uint8Info": 0}]},timeout =0.5)

        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                                {"status":{"source":1}})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus",
                                    {"status":{"source":1}}) 
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus",
                                    {"status":{"source":1}}) 
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus",
                                    {"status":{"source":1}})  
        
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                               {"out": [{"id":0,"status":{"source":1}},
                                                        {"id":1,"status":{"source":1}},
                                                        {"id":4,"status":{"source":1}},
                                                        {"id":6,"status":{"source":1}},
                                                        ]},timeout =0.5)

    @allure.title("座椅通风加热请求源_usagemode_下切上切")
    @pytest.mark.full
    def test_caseid_1985703(self):
        for i in [2,11,13]:
            for j in [0,1]:
                for k in [2,11,13]:
                    self.sd_tester.change_usage_mode(i)
                    self.setHeatLevelSource([0,0,0], [1,0,0], [4,0,0], [6,0,0])
                    self.setVentLevelSource([0,0,0], [1,0,0], [4,0,0], [6,0,0])
                    sleep(1)
                    
                    self.setHeatLevelSource([0,0,1], [1,0,1], [4,0,1], [6,0,1])
                    self.setVentLevelSource([0,0,1], [1,0,1], [4,0,1], [6,0,1])
                    sleep(1)
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetHeatingLevel", {"seats": [12]}, 
                                                    {"out": [{"id": 0, "source": 1},{"id": 1, "source": 1},
                                                            {"id": 4, "source": 1},{"id": 6, "source": 1}]})  
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVentingLevel", {"seats": [12]}, 
                                                    {"out": [{"id": 0, "source": 1},{"id": 1, "source": 1},
                                                            {"id": 4, "source": 1},{"id": 6, "source": 1}]}) 
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                                            {"status":{"source":1}})
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus",
                                                {"status":{"source":1}}) 
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus",
                                                {"status":{"source":1}}) 
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus",
                                                {"status":{"source":1}})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                                {"out": [{"id":0,"status":{"source":1}},
                                                            {"id":1,"status":{"source":1}},
                                                            {"id":4,"status":{"source":1}},
                                                            {"id":6,"status":{"source":1}},
                                                            ]})
                    self.sd_tester.change_usage_mode(j)
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetHeatingLevel", {"seats": [12]}, 
                                                    {"out": [{"id": 0, "source": 0},{"id": 1, "source": 0},
                                                            {"id": 4, "source": 0},{"id": 6, "source": 0}]})  
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVentingLevel", {"seats": [12]}, 
                                                    {"out": [{"id": 0, "source": 0},{"id": 1, "source": 0},
                                                            {"id": 4, "source": 0},{"id": 6, "source": 0}]})  
                    
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                                            {"status":{"source":0}})
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus",
                                                {"status":{"source":0}}) 
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus",
                                                {"status":{"source":0}}) 
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus",
                                                {"status":{"source":0}})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                                {"out": [{"id":0,"status":{"source":0}},
                                                            {"id":1,"status":{"source":0}},
                                                            {"id":4,"status":{"source":0}},
                                                            {"id":6,"status":{"source":0}},
                                                            ]})
                    self.sd_tester.change_usage_mode(k)
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetHeatingLevel", {"seats": [12]}, 
                                                    {"out": [{"id": 0, "source": 0},{"id": 1, "source": 0},
                                                            {"id": 4, "source": 0},{"id": 6, "source": 0}]})  
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVentingLevel", {"seats": [12]}, 
                                                    {"out": [{"id": 0, "source": 0},{"id": 1, "source": 0},
                                                            {"id": 4, "source": 0},{"id": 6, "source": 0}]})  
                    
                    self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus")
                    self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus")                         
                    self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus") 
                    self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus") 

                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                                {"out": [{"id":0,"status":{"source":0}},
                                                            {"id":1,"status":{"source":0}},
                                                            {"id":4,"status":{"source":0}},
                                                            {"id":6,"status":{"source":0}},
                                                            ]})
        
    @allure.title("座椅加热状态值非0到0_1s内请求源变化")
    @pytest.mark.smoke
    def test_caseid_1985704(self):
        #SOA-28239 避免前case影响
        self.setHeatVentingStatus(0,0)
        self.sd_tester.change_usage_mode(2)
        #1s延时逻辑 设置值要与挡位值匹配
        self.setHeatLevelSource([0,2,0], [1,2,0], [4,2,0], [6,2,0])
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgLvlSts', 2)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecLe',2)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecRi',2)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgLvlSts', 2)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgLvlSts', 0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgLvlSts', 0)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecLe',0)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecRi',0)

        #1ms调设置加热接口改变source
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                    {"params": [{"id": 0, "uint8Info": 2}],"source":2})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                                            {"status":{"source":2}},timeout=0.2)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                                {"out": [{"id":0,"status":{"heatLevel":2,"source":2}},
                                                         {"id":1,"status":{"heatLevel":2,"source":0}},
                                                         {"id":4,"status":{"heatLevel":2,"source":0}},
                                                         {"id":6,"status":{"heatLevel":2,"source":0}},
                                                        ]},timeout = 0.3)
        sleep(1)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                                {"out": [{"id":0,"status":{"heatLevel":0,"source":2}},
                                                         {"id":1,"status":{"heatLevel":0,"source":0}},
                                                         {"id":4,"status":{"heatLevel":0,"source":0}},
                                                         {"id":6,"status":{"heatLevel":0,"source":0}},
                                                        ]})
 
    @allure.title("座椅通风状态值非0到0_1s内请求源变化")
    @pytest.mark.full
    def test_caseid_1985705(self):
        #SOA-28239 避免前case影响
        self.setHeatVentingStatus(0,0)
        self.sd_tester.change_usage_mode(2)
        self.setVentLevelSource([0,1,0], [1,1,0], [4,1,0], [6,1,0])
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentnLvlSts', 1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentnLvlSts',1)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecLe',1)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecRi', 1)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentnLvlSts', 0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentnLvlSts',0)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecLe',0)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecRi', 0)

        #1ms调设置加热接口改变source
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                    {"params": [{"id": 6, "uint8Info": 1}],"source":1})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus",
                                                            {"status":{"source":1}},timeout=0.2)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                                {"out": [{"id":0,"status":{"ventLevel":1,"source":0}},
                                                         {"id":1,"status":{"ventLevel":1,"source":0}},
                                                         {"id":4,"status":{"ventLevel":1,"source":0}},
                                                         {"id":6,"status":{"ventLevel":1,"source":1}},
                                                        ]},timeout = 0.3)
        sleep(1)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                                {"out": [{"id":0,"status":{"ventLevel":0,"source":0}},
                                                         {"id":1,"status":{"ventLevel":0,"source":0}},
                                                         {"id":4,"status":{"ventLevel":0,"source":0}},
                                                         {"id":6,"status":{"ventLevel":0,"source":1}},
                                                        ]})

    @allure.title("本地座椅_主驾加热的信号重置")
    @pytest.mark.sanity
    def test_caseid_1985986(self):
        self.sd_tester.change_usage_mode(2)
        self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [2,11,13]:
            self.sd_tester.change_usage_mode(mode)
            self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgAvlSts',4)
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgAvlSts',2)
            sleep(0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        #周期发送  
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatHeatgForRowFirstLe",[1,0,1,0,1,0])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatHeatgForRowFirstRi",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatHeatgForRowSecLe",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatHeatgForRowSecRi",[1])
        
    @allure.title("本地座椅_副驾加热的信号重置")
    @pytest.mark.full
    def test_caseid_1985987(self):
        self.sd_tester.change_usage_mode(2)
        self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [2,11,13]:
            self.sd_tester.change_usage_mode(mode)
            self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgAvlSts',4)
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgAvlSts',2)
            sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatHeatgForRowFirstLe",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatHeatgForRowFirstRi",[1,0,1,0,1,0])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatHeatgForRowSecLe",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatHeatgForRowSecRi",[1])
        
    @allure.title("本地座椅_二排左侧加热的信号重置")
    @pytest.mark.full
    def test_caseid_1985988(self):
        self.sd_tester.change_usage_mode(2)
        self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [2,11,13]:
            self.sd_tester.change_usage_mode(mode)
            self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecLe',4)
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecLe',2)
            sleep(0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatHeatgForRowFirstLe",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatHeatgForRowFirstRi",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatHeatgForRowSecLe",[1,0,1,0,1,0])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatHeatgForRowSecRi",[1])
        
    @allure.title("本地座椅_二排右侧加热的信号重置")
    @pytest.mark.full
    def test_caseid_1985989(self):
        self.sd_tester.change_usage_mode(2)
        self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [2,11,13]:
            self.sd_tester.change_usage_mode(mode)
            self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecRi',4)
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecRi',2)
            sleep(0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatHeatgForRowFirstLe",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatHeatgForRowFirstRi",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatHeatgForRowSecLe",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatHeatgForRowSecRi",[1,0,1,0,1,0])
        
    @allure.title("远程座椅_主驾加热的信号重置")
    @pytest.mark.full
    def test_caseid_1985990(self):
        #不需要的条件
        self.setSeatHeatLevel(0,0,0,0)
        
        self.sd_tester.change_usage_mode(1)
        self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [0,1]:
            self.sd_tester.change_usage_mode(mode)
            self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgAvlSts',4)
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgAvlSts',2)
            sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        result = self.bgm_eth_inter.get_signal_values("TelmSeatDrvHeatClimaLvlSP")
        assert result.count(0) == 10
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [0,1,2,11,13]:
            self.sd_tester.change_usage_mode(mode)
            for i in [1,2,3]:
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgLvlSts',i)
                sleep(1)
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgLvlSts',0)
                sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        result = self.bgm_eth_inter.get_signal_values("TelmSeatDrvHeatClimaLvlSP")
        assert result.count(0) == 75

    @allure.title("远程座椅_副驾加热的信号重置")
    @pytest.mark.full
    def test_caseid_1985991(self):
         #不需要的条件
        self.setSeatHeatLevel(1,1,1,1)
        
        self.sd_tester.change_usage_mode(1)
        self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [0,1]:
            self.sd_tester.change_usage_mode(mode)
            self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgAvlSts',4)
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgAvlSts',2)
            sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        result = self.bgm_eth_inter.get_signal_values("TelmSeatPassHeatClimaLvlSP")
        assert result.count(0) == 10
      
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [0,1,2,11,13]:
            self.sd_tester.change_usage_mode(mode)
            for i in [1,2,3]:
                self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgLvlSts',i)
                sleep(1)
                self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgLvlSts',0)
                sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        result = self.bgm_eth_inter.get_signal_values("TelmSeatPassHeatClimaLvlSP")
        assert result.count(0) == 75

    @allure.title("远程座椅_二排左侧加热的信号重置")
    @pytest.mark.full
    def test_caseid_1985992(self):
        #不需要的条件
        self.setSeatHeatLevel(0,0,1,1)
        
        self.sd_tester.change_usage_mode(1)
        self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [0,1]:
            self.sd_tester.change_usage_mode(mode)
            self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecLe',4)
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecLe',2)
            sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        result = self.bgm_eth_inter.get_signal_values("TelmSeatSecLeHeatClimaLvl")
        assert result.count(0) == 10
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [0,1,2,11,13]:
            self.sd_tester.change_usage_mode(mode)
            for i in [1,2,3]:
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecLe',i)
                sleep(1)
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecLe',0)
                sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        result = self.bgm_eth_inter.get_signal_values("TelmSeatSecLeHeatClimaLvl")
        assert result.count(0) == 75

    @allure.title("远程座椅_二排右侧加热的信号重置")
    @pytest.mark.full
    def test_caseid_1985993(self):
        #不需要的条件
        self.setSeatHeatLevel(1,1,1,1)
        
        self.sd_tester.change_usage_mode(1)
        self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [0,1]:
            self.sd_tester.change_usage_mode(mode)
            self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecRi',4)
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecRi',2)
            sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        result = self.bgm_eth_inter.get_signal_values("TelmSeatSecRiHeatClimaLvl")
        assert result.count(0) == 10
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [0,1,2,11,13]:
            self.sd_tester.change_usage_mode(mode)
            for i in [1,2,3]:
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecRi',i)
                sleep(1)
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecRi',0)
                sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        result = self.bgm_eth_inter.get_signal_values("TelmSeatSecRiHeatClimaLvl")
        assert result.count(0) == 75
        
    @allure.title("本地座椅_主驾通风的信号重置")
    @pytest.mark.sanity
    def test_caseid_1985994(self):
        self.sd_tester.change_usage_mode(2)
        self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [2,11,13]:
            self.sd_tester.change_usage_mode(mode)
            self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentAvlSts',4)
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentAvlSts',2)
            sleep(0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        #周期发送  
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatVentnForRowFirstLe",[1,0,1,0,1,0])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatVentnForRowFirstRi",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatVentnForRowSecLe",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatVentnForRowSecRi",[1])
        
    @allure.title("本地座椅_副驾通风的信号重置")
    @pytest.mark.full
    def test_caseid_1985995(self):
        self.sd_tester.change_usage_mode(2)
        self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [2,11,13]:
            self.sd_tester.change_usage_mode(mode)
            self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentAvlSts',4)
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentAvlSts',2)
            sleep(0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatVentnForRowFirstLe",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatVentnForRowFirstRi",[1,0,1,0,1,0])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatVentnForRowSecLe",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatVentnForRowSecRi",[1])
        
    @allure.title("本地座椅_二排左侧通风的信号重置")
    @pytest.mark.full
    def test_caseid_1985996(self):
        self.sd_tester.change_usage_mode(2)
        self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [2,11,13]:
            self.sd_tester.change_usage_mode(mode)
            self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecLe',4)
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecLe',2)
            sleep(0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatVentnForRowFirstLe",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatVentnForRowFirstRi",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatVentnForRowSecLe",[1,0,1,0,1,0])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatVentnForRowSecRi",[1])
        
    @allure.title("本地座椅_二排右侧通风的信号重置")
    @pytest.mark.full
    def test_caseid_1985997(self):
        self.sd_tester.change_usage_mode(2)
        self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [2,11,13]:
            self.sd_tester.change_usage_mode(mode)
            self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecRi',4)
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecRi',2)
            sleep(0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatVentnForRowFirstLe",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatVentnForRowFirstRi",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatVentnForRowSecLe",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatVentnForRowSecRi",[1,0,1,0,1,0])
        
    @allure.title("远程座椅_主驾通风的信号重置")
    @pytest.mark.full
    def test_caseid_1985998(self):
        #不需要的条件
        self.setSeatVentLevel(1,1,1,1)
        
        self.sd_tester.change_usage_mode(1)
        self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [0,1]:
            self.sd_tester.change_usage_mode(mode)
            self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentAvlSts',4)
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentAvlSts',2)
            sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        result = self.bgm_eth_inter.get_signal_values("TelmSeatDrvVentnClimaLvl")
        assert result.count(0) == 10

        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [0,1,2,11,13]:
            self.sd_tester.change_usage_mode(mode)
            for i in [1,2,3]:
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentnLvlSts',i)
                sleep(1)
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentnLvlSts',0)
                sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        result = self.bgm_eth_inter.get_signal_values("TelmSeatDrvVentnClimaLvl")
        assert result.count(0) == 75

    @allure.title("远程座椅_副驾通风的信号重置")
    @pytest.mark.full
    def test_caseid_1985999(self):
        #不需要的条件
        self.setSeatVentLevel(1,1,1,1)
        
        self.sd_tester.change_usage_mode(1)
        self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [0,1]:
            self.sd_tester.change_usage_mode(mode)
            self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentAvlSts',4)
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentAvlSts',2)
            sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        result = self.bgm_eth_inter.get_signal_values("TelmSeatPassVentnClimaLvl")
        assert result.count(0) == 10
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [0,1,2,11,13]:
            self.sd_tester.change_usage_mode(mode)
            for i in [1,2,3]:
                self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentnLvlSts',i)
                sleep(1)
                self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentnLvlSts',0)
                sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        result = self.bgm_eth_inter.get_signal_values("TelmSeatPassVentnClimaLvl")
        assert result.count(0) == 75

    @allure.title("远程座椅_二排左侧通风的信号重置")
    @pytest.mark.full
    def test_caseid_1986000(self):
        #不需要的条件
        self.setSeatVentLevel(1,1,1,1)
        
        self.sd_tester.change_usage_mode(1)
        self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [0,1]:
            self.sd_tester.change_usage_mode(mode)
            self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecLe',4)
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecLe',2)
            sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        result = self.bgm_eth_inter.get_signal_values("TelmSeatSecLeVentnClimaLvl")
        assert result.count(0) == 10
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [0,1,2,11,13]:
            self.sd_tester.change_usage_mode(mode)
            for i in [1,2,3]:
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecLe',i)
                sleep(1)
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecLe',0)
                sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        result = self.bgm_eth_inter.get_signal_values("TelmSeatSecLeVentnClimaLvl")
        assert result.count(0) == 75

    @allure.title("远程座椅_二排右侧通风的信号重置")
    @pytest.mark.full
    def test_caseid_1986001(self):
        #不需要的条件
        self.setSeatVentLevel(1,1,1,1)
        
        self.sd_tester.change_usage_mode(1)
        self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [0,1]:
            self.sd_tester.change_usage_mode(mode)
            self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecRi',4)
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecRi',2)
            sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        result = self.bgm_eth_inter.get_signal_values("TelmSeatSecRiVentnClimaLvl")
        assert result.count(0) == 10
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [0,1,2,11,13]:
            self.sd_tester.change_usage_mode(mode)
            for i in [1,2,3]:
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecRi', i)
                sleep(1)
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecRi', 0)
                sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        result = self.bgm_eth_inter.get_signal_values("TelmSeatSecRiVentnClimaLvl")
        assert result.count(0) == 75
        
    @allure.title("本地座椅_加热的信号重置_非防玩模式")
    @pytest.mark.smoke
    def test_caseid_1986113(self):
        self.sd_tester.change_usage_mode(2)
        self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [2,11,13]:
            self.sd_tester.change_usage_mode(mode)
            #AvlSts从其他值跳变为3(Error)||4(Funcationallimit)||5(Energylimit))HmiSeatClimaHmiSeat=0
            for i in [0,1,2,6,7]:
                self.setHeatVentingStatus(i,0)
                sleep(1)
                self.setHeatVentingStatus(2,0)
                sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatHeatgForRowFirstLe",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatHeatgForRowFirstRi",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatHeatgForRowSecLe",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatHeatgForRowSecRi",[1])
    
    @allure.title("远程座椅_加热的信号重置_非防玩模式")
    @pytest.mark.smoke
    def test_caseid_1986114(self):
        self.sd_tester.change_usage_mode(1)
        #不需要的前提
        self.setSeatHeatLevel(1,1,1,1)
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [0,1]:
            self.sd_tester.change_usage_mode(mode)
            self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(1)
            for i in [0,1,2,3,5,6,7]:
                self.setHeatVentingStatus(i,0)
                sleep(1)
                self.setHeatVentingStatus(2,0)
                sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        self.bgm_eth_inter.ck_ordered_array("TelmSeatDrvHeatClimaLvlSP",[1])
        self.bgm_eth_inter.ck_ordered_array("TelmSeatPassHeatClimaLvlSP",[1])
        self.bgm_eth_inter.ck_ordered_array("TelmSeatSecLeHeatClimaLvl",[1])
        self.bgm_eth_inter.ck_ordered_array("TelmSeatSecRiHeatClimaLvl",[1])
        
    @allure.title("本地座椅_通风的信号重置_非防玩模式")
    @pytest.mark.full
    def test_caseid_1986115(self):
        self.sd_tester.change_usage_mode(2)
        self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [2,11,13]:
            self.sd_tester.change_usage_mode(mode)
            #AvlSts从其他值跳变为3(Error)||4(Funcationallimit)||5(Energylimit))HmiSeatClimaHmiSeat=0
            for i in [0,1,2,6,7]:
                self.setHeatVentingStatus(0,i)
                sleep(1)
                self.setHeatVentingStatus(0,2)
                sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatVentnForRowFirstLe",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatVentnForRowFirstRi",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatVentnForRowSecLe",[1])
        self.bgm_eth_inter.ck_ordered_array("HmiSeatClimaHmiSeatVentnForRowSecRi",[1])
      
    @allure.title("远程座椅_通风的信号重置_非防玩模式")
    @pytest.mark.full
    def test_caseid_1986116(self):
        #不需要的条件
        self.setSeatVentLevel(1,1,1,1)
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [0,1]:
            self.sd_tester.change_usage_mode(mode)
            self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(1)
            for i in [0,1,2,3,5,6,7]:
                self.setHeatVentingStatus(i,0)
                sleep(1)
                self.setHeatVentingStatus(2,0)
                sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        self.bgm_eth_inter.ck_ordered_array("TelmSeatDrvVentnClimaLvl",[1])
        self.bgm_eth_inter.ck_ordered_array("TelmSeatPassVentnClimaLvl",[1])
        self.bgm_eth_inter.ck_ordered_array("TelmSeatSecLeVentnClimaLvl",[1])
        self.bgm_eth_inter.ck_ordered_array("TelmSeatSecRiVentnClimaLvl",[1])
        
    @allure.title("远程座椅_5帧下发周期内_加热的信号重置_最新值与当前值相同_信号跳变打断接口调用")
    @pytest.mark.full
    def test_caseid_1986119(self):
        #不需要的前提
        self.setSeatHeatLevel(1,1,1,1)
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        #方式1
        for mode in [0,1]:
            self.sd_tester.change_usage_mode(mode)
            self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            self.setHeatVentingStatus(4,0)
            sleep(1)
            self.setHeatLevelSource([0,0,1], [1,0,1], [4,0,1], [6,0,1])
            sleep(0.2)
            self.setHeatVentingStatus(2,0)
            sleep(1)
        #方式2    
        for mode in [0,1]:
            self.sd_tester.change_usage_mode(mode)
            for i in [1,2,3]:
                self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
                self.setSeatHeatLevel(i,i,i,i)
                
                self.setHeatLevelSource([0,0,1], [1,0,1], [4,0,1], [6,0,1])
                sleep(0.2)
                self.setSeatHeatLevel(0,0,0,0)
                sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        a = self.bgm_eth_inter.get_signal_values("TelmSeatDrvHeatClimaLvlSP")
        b = self.bgm_eth_inter.get_signal_values("TelmSeatPassHeatClimaLvlSP")
        c = self.bgm_eth_inter.get_signal_values("TelmSeatSecLeHeatClimaLvl")
        d = self.bgm_eth_inter.get_signal_values("TelmSeatSecRiHeatClimaLvl")
        assert a.count(0) == 40 and b.count(0) == 40 and c.count(0) == 40 and d.count(0) == 40
        assert a.count(1) == 40 and b.count(1) == 40 and c.count(1) == 40 and d.count(1) == 40
        
    @allure.title("远程座椅_5帧下发周期内_通风的信号重置_最新值与当前值相同_信号跳变打断接口调用")
    @pytest.mark.full
    def test_caseid_1986120(self):
        #不需要的前提
        self.setSeatVentLevel(1,1,1,1)
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        #方式1
        for mode in [0,1]:
            self.sd_tester.change_usage_mode(mode)
            self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            self.setHeatVentingStatus(0,4)
            sleep(2)
            self.setVentLevelSource([0,0,1], [1,0,1], [4,0,1], [6,0,1])
            sleep(0.2)
            self.setHeatVentingStatus(0,2)
            sleep(1)
        #方式2
        for mode in [0,1]:
            for i in [1,2,3]:
                self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
                self.setSeatVentLevel(i,i,i,i)
                sleep(2)
                self.setVentLevelSource([0,0,1], [1,0,1], [4,0,1], [6,0,1])
                sleep(0.2)
                self.setSeatVentLevel(0,0,0,0)
                sleep(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        a = self.bgm_eth_inter.get_signal_values("TelmSeatDrvVentnClimaLvl")
        b = self.bgm_eth_inter.get_signal_values("TelmSeatPassVentnClimaLvl")
        c = self.bgm_eth_inter.get_signal_values("TelmSeatSecLeVentnClimaLvl")
        d = self.bgm_eth_inter.get_signal_values("TelmSeatSecRiVentnClimaLvl")
        assert a.count(0) == 40 and b.count(0) == 40 and c.count(0) == 40 and d.count(0) == 40
        assert a.count(1) == 40 and b.count(1) == 40 and c.count(1) == 40 and d.count(1) == 40
        
    @allure.title("远程座椅_5帧下发周期内_加热的信号重置_最新值与当前值不同_信号跳变打断接口调用")
    @pytest.mark.full
    def test_caseid_1986121(self):
        #不需要的前提
        self.setSeatHeatLevel(1,1,1,1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        #方式1
        for mode in [0,1]:
            self.sd_tester.change_usage_mode(mode)
            self.setHeatLevelSource([0,0,1], [1,0,1], [4,0,1], [6,0,1])
            self.setHeatVentingStatus(4,0)
            sleep(2)
            self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(0.2)
            self.setHeatVentingStatus(2,0)
            sleep(2)
        #方式2    
        for mode in [0,1]:
            self.sd_tester.change_usage_mode(mode)
            for i in [1,2,3]:
                self.setHeatLevelSource([0,0,1], [1,0,1], [4,0,1], [6,0,1])
                self.setSeatHeatLevel(i,i,i,i)
                sleep(2)
                self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
                sleep(0.2)
                self.setSeatHeatLevel(0,0,0,0)
                sleep(2)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        a = self.bgm_eth_inter.get_signal_values("TelmSeatDrvHeatClimaLvlSP")
        b = self.bgm_eth_inter.get_signal_values("TelmSeatPassHeatClimaLvlSP")
        c = self.bgm_eth_inter.get_signal_values("TelmSeatSecLeHeatClimaLvl")
        d = self.bgm_eth_inter.get_signal_values("TelmSeatSecRiHeatClimaLvl")
        assert a.count(0) == 80 and b.count(0) == 80 and c.count(0) == 80 and d.count(0) == 80
        # assert a.count(1) < 40 and b.count(1) < 40 and c.count(1) < 40 and d.count(1) < 40
        #座椅通风加热的控制信号需要确保间隔500ms
        assert a.count(1) == 40 and b.count(1) == 40 and c.count(1) == 40 and d.count(1) == 40
        
    @allure.title("远程座椅_5帧下发周期内_通风的信号重置_最新值与当前值不同_信号跳变打断接口调用")
    @pytest.mark.full
    def test_caseid_1986122(self):
        #不需要的前提
        self.setSeatVentLevel(1,1,1,1)
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        #方式1
        for mode in [0,1]:
            self.sd_tester.change_usage_mode(mode)
            self.setVentLevelSource([0,0,1], [1,0,1], [4,0,1], [6,0,1])
            self.setHeatVentingStatus(0,4)
            sleep(2)
            self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(0.2)
            self.setHeatVentingStatus(0,2)
            sleep(2)
        #方式2
        for mode in [0,1]:
            for i in [1,2,3]:
                self.setVentLevelSource([0,0,1], [1,0,1], [4,0,1], [6,0,1])
                self.setSeatVentLevel(i,i,i,i)
                sleep(2)
                self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
                sleep(0.2)
                self.setSeatVentLevel(0,0,0,0)
                sleep(2)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        a = self.bgm_eth_inter.get_signal_values("TelmSeatDrvVentnClimaLvl")
        b = self.bgm_eth_inter.get_signal_values("TelmSeatPassVentnClimaLvl")
        c = self.bgm_eth_inter.get_signal_values("TelmSeatSecLeVentnClimaLvl")
        d = self.bgm_eth_inter.get_signal_values("TelmSeatSecRiVentnClimaLvl")
        assert a.count(0) == 80 and b.count(0) == 80 and c.count(0) == 80 and d.count(0) == 80
        assert a.count(1) == 40 and b.count(1) == 40 and c.count(1) == 40 and d.count(1) == 40
        
    @allure.title("远程座椅_5帧下发周期内_加热的信号重置_最新值与当前值相同_接口调用打断信号跳变")
    @pytest.mark.full
    def test_caseid_1986187(self):
        #不需要的前提
        self.setSeatHeatLevel(1,1,1,1)
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        #方式1
        for mode in [0,1]:
            self.sd_tester.change_usage_mode(mode)
            self.setHeatVentingStatus(4,0)
            self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(2)
            self.setHeatVentingStatus(2,0)
            sleep(0.2)
            self.setHeatLevelSource([0,0,1], [1,0,1], [4,0,1], [6,0,1])
            sleep(2)
        #方式2    
        for mode in [0,1]:
            self.sd_tester.change_usage_mode(mode)
            for i in [1,2,3]:
                self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
                self.setSeatHeatLevel(i,i,i,i)
                sleep(2)
                self.setSeatHeatLevel(0,0,0,0)
                sleep(0.2)
                self.setHeatLevelSource([0,0,1], [1,0,1], [4,0,1], [6,0,1])
                sleep(2)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        a = self.bgm_eth_inter.get_signal_values("TelmSeatDrvHeatClimaLvlSP")
        b = self.bgm_eth_inter.get_signal_values("TelmSeatPassHeatClimaLvlSP")
        c = self.bgm_eth_inter.get_signal_values("TelmSeatSecLeHeatClimaLvl")
        d = self.bgm_eth_inter.get_signal_values("TelmSeatSecRiHeatClimaLvl")
        assert a.count(0) <= 70 and b.count(0) <= 70 and c.count(0) <= 70 and d.count(0) <= 70
        assert a.count(1) == 40 and b.count(1) == 40 and c.count(1) == 40 and d.count(1) == 40
        
    @allure.title("远程座椅_5帧下发周期内_通风的信号重置_最新值与当前值相同_接口调用打断信号跳变")
    @pytest.mark.full
    def test_caseid_1986188(self):
        #不需要的前提
        self.setSeatVentLevel(1,1,1,1)
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        #方式1
        for mode in [0,1]:
            self.sd_tester.change_usage_mode(mode)
            self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            self.setHeatVentingStatus(0,4)
            sleep(2)
            
            self.setHeatVentingStatus(0,2)
            sleep(0.2)
            self.setVentLevelSource([0,0,1], [1,0,1], [4,0,1], [6,0,1])
            sleep(2)
        #方式2
        for mode in [0,1]:
            for i in [1,2,3]:
                self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
                self.setSeatVentLevel(i,i,i,i)
                sleep(2)
                self.setSeatVentLevel(0,0,0,0)
                sleep(0.2)
                self.setVentLevelSource([0,0,1], [1,0,1], [4,0,1], [6,0,1])
                sleep(2)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        a = self.bgm_eth_inter.get_signal_values("TelmSeatDrvVentnClimaLvl")
        b = self.bgm_eth_inter.get_signal_values("TelmSeatPassVentnClimaLvl")
        c = self.bgm_eth_inter.get_signal_values("TelmSeatSecLeVentnClimaLvl")
        d = self.bgm_eth_inter.get_signal_values("TelmSeatSecRiVentnClimaLvl")
        assert a.count(0) <= 70 and b.count(0) <= 70 and c.count(0) <= 70 and d.count(0) <= 70
        assert a.count(1) == 40 and b.count(1) == 40 and c.count(1) == 40 and d.count(1) == 40
        
    @allure.title("远程座椅_5帧下发周期内_加热的信号重置_最新值与当前值不同_接口调用打断信号跳变")
    @pytest.mark.full
    def test_caseid_1986189(self):
        #不需要的前提
        self.setSeatHeatLevel(1,1,1,1)
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        #方式1
        for mode in [0,1]:
            self.sd_tester.change_usage_mode(mode)
            self.setHeatLevelSource([0,0,1], [1,0,1], [4,0,1], [6,0,1])
            self.setHeatVentingStatus(4,0)
            sleep(2)
            
            self.setHeatVentingStatus(2,0)
            sleep(0.2)
            self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(2)
        #方式2    
        for mode in [0,1]:
            self.sd_tester.change_usage_mode(mode)
            for i in [1,2,3]:
                self.setHeatLevelSource([0,0,1], [1,0,1], [4,0,1], [6,0,1])
                self.setSeatHeatLevel(i,i,i,i)
                sleep(2)
                self.setSeatHeatLevel(0,0,0,0)
                sleep(0.2)
                self.setHeatLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
                sleep(2)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        a = self.bgm_eth_inter.get_signal_values("TelmSeatDrvHeatClimaLvlSP")
        b = self.bgm_eth_inter.get_signal_values("TelmSeatPassHeatClimaLvlSP")
        c = self.bgm_eth_inter.get_signal_values("TelmSeatSecLeHeatClimaLvl")
        d = self.bgm_eth_inter.get_signal_values("TelmSeatSecRiHeatClimaLvl")
        assert a.count(0) == 80 and b.count(0) == 80 and c.count(0) == 80 and d.count(0) == 80
        assert a.count(1) == 40 and b.count(1) == 40 and c.count(1) == 40 and d.count(1) == 40
        
    @allure.title("远程座椅_5帧下发周期内_通风的信号重置_最新值与当前值不同_接口调用打断信号跳变")
    @pytest.mark.full
    def test_caseid_1986191(self):
        #不需要的前提
        self.setSeatVentLevel(1,1,1,1)
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        #方式1
        for mode in [0,1]:
            self.sd_tester.change_usage_mode(mode)
            self.setVentLevelSource([0,0,1], [1,0,1], [4,0,1], [6,0,1])
            self.setHeatVentingStatus(0,4)
            sleep(2)
            self.setHeatVentingStatus(0,2)
            
            sleep(0.2)
            self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
            sleep(2)
        #方式2
        for mode in [0,1]:
            for i in [1,2,3]:
                self.setVentLevelSource([0,0,1], [1,0,1], [4,0,1], [6,0,1])
                self.setSeatVentLevel(i,i,i,i)
                sleep(2)
                self.setSeatVentLevel(0,0,0,0)
                sleep(0.2)
                self.setVentLevelSource([0,1,1], [1,1,1], [4,1,1], [6,1,1])
                sleep(2)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        a = self.bgm_eth_inter.get_signal_values("TelmSeatDrvVentnClimaLvl")
        b = self.bgm_eth_inter.get_signal_values("TelmSeatPassVentnClimaLvl")
        c = self.bgm_eth_inter.get_signal_values("TelmSeatSecLeVentnClimaLvl")
        d = self.bgm_eth_inter.get_signal_values("TelmSeatSecRiVentnClimaLvl")
        assert a.count(0) == 80 and b.count(0) == 80 and c.count(0) == 80 and d.count(0) == 80
        assert a.count(1) == 40 and b.count(1) == 40 and c.count(1) == 40 and d.count(1) == 40
        
    @allure.title("二排右侧座椅占位状态(status)_带儿童座椅")
    @pytest.mark.sanity
    def test_caseid_1987121(self):
        sts = [[True,False],[False,True],[True,True],[False,True],[True,True],[True,False]]
        #二排右侧无占位
        self.io.drvr_door_open()
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSt1', 0)
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 0)
        
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{"seatStsSecondLeft":{"installSts":True,"occupySts":True},
                                                    "seatStsSecondRight":{"installSts":False,"occupySts":False}}})
        self.get_occupied_sec(6,0)
        self.partner.empty_all(0.5)
        for i in range(6):
            self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                                {"seatSts":{"seatStsSecondLeft":{"installSts":True,"occupySts":True},
                                                            "seatStsSecondRight":{"installSts":sts[i][0],"occupySts":sts[i][1]}}})
            if i in [0,1]:
                self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatus")
                self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatusValidity")
            if i in [2,4]:
                self.notify_occupied_sec(6,1)
                self.get_occupied_sec(6,1)
            if i in [3,5]:
                self.notify_occupied_sec(6,0)
                self.get_occupied_sec(6,0)
            
    @allure.title("二排左侧座椅占位状态(status)_带儿童座椅")
    @pytest.mark.full
    def test_caseid_1987122(self):
        sts = [[True,False],[False,True],[True,True],[False,True],[True,True],[True,False]]
        #二排右侧无占位
        self.io.drvr_door_open()
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSt1', 0)
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 0)
        
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{"seatStsSecondRight":{"installSts":True,"occupySts":True},
                                                    "seatStsSecondLeft":{"installSts":False,"occupySts":False}}})
        self.get_occupied_sec(4,0)
        self.partner.empty_all(0.5)
        for i in range(6):
            self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                                {"seatSts":{"seatStsSecondRight":{"installSts":True,"occupySts":True},
                                                            "seatStsSecondLeft":{"installSts":sts[i][0],"occupySts":sts[i][1]}}})
            if i in [0,1]:
                self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatus")
                self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatusValidity")
            if i in [2,4]:
                self.notify_occupied_sec(4,1)
                self.get_occupied_sec(4,1)
            if i in [3,5]:
                self.notify_occupied_sec(4,0)
                self.get_occupied_sec(4,0)
            
    @allure.title("车内有人状态判断_儿童座椅有人到无人_门开时")
    @pytest.mark.smoke
    def test_caseid_1987123(self):
        sts = [[True,False],[False,True],[True,True],[False,True],[True,True],[True,False]]
        seatid = [["seatStsSecondLeft","seatStsSecondRight"],["seatStsSecondRight","seatStsSecondLeft"]]
        #除儿童座椅外其他座位上无人
        self.set_four_Door_open()
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{"seatStsSecondLeft":{"installSts":False,"occupySts":False},
                                                    "seatStsSecondRight":{"installSts":False,"occupySts":False}}})
        sleep(3)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVehicleInsidePersonSts", {},
                                            {"out":{"userInVehicleStatus":False}})           
        self.partner.empty_all(0.5)

        for i in range(2):
            for j in range(6):
                self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                                    {"seatSts":{seatid[i][0]:{"installSts":False,"occupySts":False},
                                                                seatid[i][1]:{"installSts":sts[j][0],"occupySts":sts[j][1]}}})
                if j in [0,1]:
                    self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts")
                if j in [2,4]:
                    self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":True}},
                                    "GetVehicleInsidePersonSts", {})
                if j in [3,5]:
                    sleep(1)
                    self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts")
                    self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":False}},
                                    "GetVehicleInsidePersonSts", {},timeout = 3)
                                  
    @allure.title("车内有人状态判断_儿童座椅上有人_任意门打开_儿童座椅无人")
    @pytest.mark.full
    def test_caseid_1987124(self):
        seatid = [["seatStsSecondLeft","seatStsSecondRight"],["seatStsSecondRight","seatStsSecondLeft"]]
        #除儿童座椅外其他座位上无人
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.set_four_Door_close()
        
        for i in range(2):
            for j in range(4):
                logger.info(f"i=={i},j=={j}")
                self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{seatid[i][0]:{"installSts":True,"occupySts":True},
                                                    seatid[i][1]:{"installSts":False,"occupySts":False}}})
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVehicleInsidePersonSts", {},
                                            {"out":{"userInVehicleStatus":True}})  
                self.partner.empty_all(0.5)
                self.set_four_Door_open_onlyone(j)
                self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{seatid[i][0]:{"installSts":False,"occupySts":False},
                                                    seatid[i][1]:{"installSts":False,"occupySts":False}}})
                sleep(2)         
                self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts")
                self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":False}},
                                    "GetVehicleInsidePersonSts", {},timeout = 2)
                self.set_four_Door_close()
               
    @allure.title("车内有人状态判断_儿童座椅上有人_任意门打开_门关后确认儿童座椅无人")
    @pytest.mark.full
    def test_caseid_1987125(self):
        seatid = [["seatStsSecondLeft","seatStsSecondRight"],["seatStsSecondRight","seatStsSecondLeft"]]
        #除儿童座椅外其他座位上无人
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.set_four_Door_close()
        
        for i in range(2):
            for j in range(4):
                logger.info(f"i=={i},j=={j}")
                self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{seatid[i][0]:{"installSts":True,"occupySts":True},
                                                    seatid[i][1]:{"installSts":False,"occupySts":False}}})
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVehicleInsidePersonSts", {},
                                            {"out":{"userInVehicleStatus":True}})  
                self.partner.empty_all(0.5)
                self.set_four_Door_open_onlyone(j)
                self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{seatid[i][0]:{"installSts":False,"occupySts":False},
                                                    seatid[i][1]:{"installSts":False,"occupySts":False}}})
                #门关需要耗时
                self.set_four_Door_close()
                sleep(0.5)         
                self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts")
                self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":False}},
                                    "GetVehicleInsidePersonSts", {},timeout = 2)
                
    @allure.title("车内有人状态判断_儿童座椅有人_所有门关_无法切换到儿童座椅无人")
    @pytest.mark.full
    def test_caseid_1987126(self):
        seatid = [["seatStsSecondLeft","seatStsSecondRight"],["seatStsSecondRight","seatStsSecondLeft"]]
        #除儿童座椅外其他座位上无人
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.set_four_Door_close()
        
        for i in range(2):
            logger.info(f"i=={i}")
            self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                    {"seatSts":{seatid[i][0]:{"installSts":True,"occupySts":True},
                                                seatid[i][1]:{"installSts":False,"occupySts":False}}})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVehicleInsidePersonSts", {},
                                        {"out":{"userInVehicleStatus":True}})  
            self.partner.empty_all(0.5)
            self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                    {"seatSts":{seatid[i][0]:{"installSts":False,"occupySts":False},
                                                seatid[i][1]:{"installSts":False,"occupySts":False}}})     
            self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",timeout = 5)
       
    @allure.title("车内有人状态判断_门开_儿童座椅无占位_3s内变为有占位&门开_儿童座椅无占位_关门_3s内有占位")
    @pytest.mark.full
    def test_caseid_1987127(self):
        seatid = [["seatStsSecondLeft","seatStsSecondRight"],["seatStsSecondRight","seatStsSecondLeft"]]
        #除儿童座椅外其他座位上无人
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.set_four_Door_close()
        
        for i in range(2):
            for j in range(4):
                logger.info(f"i=={i},j=={j}")
                self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{seatid[i][0]:{"installSts":True,"occupySts":True},
                                                    seatid[i][1]:{"installSts":False,"occupySts":False}}})
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVehicleInsidePersonSts", {},
                                            {"out":{"userInVehicleStatus":True}})  
                self.partner.empty_all(0.5)
                self.set_four_Door_open_onlyone(j)
                self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{seatid[i][0]:{"installSts":False,"occupySts":False},
                                                    seatid[i][1]:{"installSts":False,"occupySts":False}}})
                sleep(1)
                self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{seatid[i][0]:{"installSts":True,"occupySts":True},
                                                    seatid[i][1]:{"installSts":False,"occupySts":False}}})      
                self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",timeout = 5)
                self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{seatid[i][0]:{"installSts":False,"occupySts":False},
                                                    seatid[i][1]:{"installSts":False,"occupySts":False}}})
                self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":False}},
                                    "GetVehicleInsidePersonSts", {},timeout = 3.5)
                self.set_four_Door_close()
                self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{seatid[i][0]:{"installSts":True,"occupySts":True},
                                                    seatid[i][1]:{"installSts":False,"occupySts":False}}})   
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVehicleInsidePersonSts", {},
                                            {"out":{"userInVehicleStatus":True}},timeout = 1)  
                
    @allure.title("融合视觉的车内有人状态_UserInVehicleStatus为True_视觉感知主副驾无人")
    @pytest.mark.smoke
    def test_caseid_1987128(self):
        seatid = [["seatStsSecondLeft","seatStsSecondRight"],["seatStsSecondRight","seatStsSecondLeft"]]
        #除儿童座椅外其他座位上无人
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.set_four_Door_close()
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                            {"firstLeftExist":False,"firstRightExist":False,"errorCode":0}})
        
        for i in range(2):
            for j in range(4):
                logger.info(f"i=={i},j=={j}")
                self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{seatid[i][0]:{"installSts":True,"occupySts":True},
                                                    seatid[i][1]:{"installSts":False,"occupySts":False}}})
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVehicleInsidePersonSts", {},
                                            {"out":{"userInVehicleStatusWithCam":True}})  
                self.partner.empty_all(0.5)
                self.set_four_Door_open_onlyone(j)
                self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{seatid[i][0]:{"installSts":False,"occupySts":False},
                                                    seatid[i][1]:{"installSts":False,"occupySts":False}}})
                sleep(1)    
                self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",timeout = 1.5)
                self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatusWithCam":False}},
                                    "GetVehicleInsidePersonSts", {},timeout = 2)
                
                self.set_four_Door_close()
                self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{seatid[i][0]:{"installSts":True,"occupySts":True},
                                                    seatid[i][1]:{"installSts":False,"occupySts":False}}})   
                self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatusWithCam":True}},
                                    "GetVehicleInsidePersonSts", {},timeout = 1)
    
    #JBS-38560
    @allure.title("Inactive远程下发打开主副驾座椅加热_切Conve_主副驾座椅加热保持_用户场景")
    @pytest.mark.smoke
    def test_caseid_1987237(self): 
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                    {"params": [{"id": 0, "uint8Info": 1},
                                                {"id": 1, "uint8Info": 2},
                                                {"id": 4, "uint8Info": 3},
                                                {"id": 6, "uint8Info": 2}]})
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgLvlSts',1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgLvlSts',2)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecLe',3)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecRi',2)
        sleep(0.5)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgLvlSts',0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgLvlSts',0)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecLe',0)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecRi',0)
        
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', 1),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', 2),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', 3),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', 2)]) 
        
    @allure.title("Inactive远程下发打开主副驾座椅通风_切Conve_主副驾座椅加热保持_用户场景")
    @pytest.mark.full
    def test_caseid_1987238(self): 
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                    {"params": [{"id": 0, "uint8Info": 2},
                                                {"id": 1, "uint8Info": 1},
                                                {"id": 4, "uint8Info": 3},
                                                {"id": 6, "uint8Info": 2}]})
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentnLvlSts',2)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentnLvlSts',1)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecLe',3)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecRi', 2)
        sleep(0.5)
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentnLvlSts',0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentnLvlSts',0)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecLe',0)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecRi', 0)
        
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstLe', 2),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowFirstRi', 1),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowSecLe', 3),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatVentnForRowSecRi', 2)]) 
        
    @allure.title("启动场景_主驾座椅姿态设置_前置条件满足_2s超时条件不满足_能立马返回success_Mars1")
    @pytest.mark.sanity
    def test_caseid_1987169(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Drvrseat_condition_allow()
        self.set_dri_position_condition(0,0,0,0)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(2)
        self.partner.empty_all()
        t1 = time.time()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 0,
                                                    "position": {"backAngle": 20, "longitudinalPosition": 100,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 1},timeout=2)
        t2 = time.time()
        assert abs(float(t2) - float(t1) ) < 1.5
        
    @allure.title("启动场景_主驾座椅姿态设置_前置条件不满足_2s超时条件满足_能立马返回Fasle_Mars1")
    @pytest.mark.full
    def test_caseid_1987173(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Drvrseat_condition_allow()
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 0)
        self.set_dri_position_condition(3,3,3,100)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(2)
        self.partner.empty_all()
        t1 = time.time()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 0,
                                                    "position": {"backAngle": 20, "longitudinalPosition": 100,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 0},timeout=2)
        t2 = time.time()
        assert abs(float(t2) - float(t1) ) < 1
        
    @allure.title("启动场景_主驾座椅姿态设置_前置条件不满足(0x110信号丢失)_需阻塞2s返回0")
    @pytest.mark.smoke
    def test_caseid_1988055(self):
        #启动后信号为丢失状态DrvrSeatExtAdjAllowd = 0
        msg_id = self.ipdu.get_signal_message("bodycan", "0x110")
        self.set_Drvrseat_condition_allow()
        self.ipdu.stop_send_pdu("bodycan", f"{msg_id}")
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        #确保服务连接
        sleep(2)
        t1 = time.time()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 0,
                                                    "position": {"backAngle": 100, "longitudinalPosition": 100,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                               }}},
                                        {"out": 0},timeout=2.5)
        t2 = time.time()
        # assert abs(float(t2) - float(t1) - 2) / 2 < 0.2
        assert float(t2) - float(t1) > 2
        #非启动场景能立马返回 0
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 0,
                                                    "position": {"backAngle": 20, "longitudinalPosition": 100,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                              }}},
                                        {"out": 0},timeout=0.5)
        self.ipdu.resume_all_bus_send()
        
    @allure.title("启动场景_主驾座椅姿态设置_前置条件不满足(0x110信号值不满足)_不需阻塞2s返回0")
    @pytest.mark.sanity
    def test_caseid_1988056(self):
        self.set_Drvrseat_condition_allow()
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 0)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        #确保服务连接
        sleep(5)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 0,
                                                    "position": {"backAngle": 100, "longitudinalPosition": 100,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                               }}},
                                        {"out": 0},timeout=0.5)
       
        
    @allure.title("启动场景_主驾座椅姿态设置_前置条件不满足(0x110)_条件满足后立马返回1")
    @pytest.mark.sanity
    def test_caseid_1988057(self):
        msg_id = self.ipdu.get_signal_message("bodycan", "0x110")
        self.set_Drvrseat_condition_allow()
        self.ipdu.stop_send_pdu("bodycan", f"{msg_id}")
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT, resume_all_bus=False)
        #确保服务连接
        sleep(5)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 0,
                                                    "position": {"backAngle": 100, "longitudinalPosition": 100,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},timeout=2.2
                                       )
        t1 = time.time()
        #由于位置信号没来，也可能造成阻塞，现状保证启动场景，2s内能控就行
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 1)
        sleep(3)
        result = self.partner.partner_infos[SEAT_SERVICE_CLIENT].resp_queue.get()
        t2 = result["timestamp"]
        out = result["result"]
        out_value = result.get('result')  # 获取'result'键对应的值
        out_value = eval(out_value)['out']
        logger.info(f"result=={result},t1=={t1},t2=={t2},out=={out}")
        assert float(t2) - float(t1) <= 2.2
        assert out_value == 1
        self.ipdu.resume_all_bus_send()
    
    @allure.title("启动场景_主驾座椅姿态设置_前置条件满足(0x069信号丢失)_不需阻塞2s返回1")
    @pytest.mark.full
    def test_caseid_1988058(self):
        #启动后信号为丢失状态DrvrSeatBtnPsd = 0
        msg_id = self.ipdu.get_signal_message("bodycan", "0x069")
        self.set_Drvrseat_condition_allow()
        sleep(0.5)
        self.ipdu.stop_send_pdu("bodycan", f"{msg_id}")
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        #确保服务连接
        sleep(5)
        t1 = time.time()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 0,
                                                    "position": {"backAngle": 100, "longitudinalPosition": 100,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                               }}},
                                        {"out": 1},timeout=2)
        self.ipdu.resume_all_bus_send()
        
    @allure.title("启动场景_主驾座椅姿态设置_前置条件不满足(0x069信号值不满足)_不需阻塞2s返回0")
    @pytest.mark.full
    def test_caseid_1988059(self):
        self.set_Drvrseat_condition_allow()
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatBtnPsd', 1)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        #确保服务连接
        sleep(5)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 0,
                                                    "position": {"backAngle": 100, "longitudinalPosition": 100,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                              }}},
                                        {"out": 0},timeout=0.5)
    
    @allure.title("启动场景_主驾座椅姿态设置_前置条件满足(0x024信号丢失)_不需阻塞2s返回1")
    @pytest.mark.full
    def test_caseid_1988061(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "57-0-4")
        self.set_Drvrseat_condition_allow()
        self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        #确保服务连接
        sleep(2)
        t1 = time.time()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 0,
                                                    "position": {"backAngle": 100, "longitudinalPosition": 100,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                               }}},
                                        {"out": 1},timeout=0.5)
        self.ipdu.resume_all_bus_send()
        
    @allure.title("启动场景_主驾座椅姿态设置_前置条件不满足(0x024信号值不满足)_不需阻塞2s返回0")
    @pytest.mark.full
    def test_caseid_1988062(self):
        self.set_Drvrseat_condition_allow()
        self.set_vehicle_speed(7.0)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        #确保服务连接
        sleep(5)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 0,
                                                    "position": {"backAngle": 100, "longitudinalPosition": 100,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                              }}},
                                        {"out": 0},timeout=0.5)
          
    @allure.title("启动场景_主驾座椅姿态设置2s内超时内条件满足_立马进行控制_Mars1")
    @pytest.mark.sanity
    def test_caseid_1987174(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Drvrseat_condition_allow()
        self.set_drvr_position1()
        #设置座椅当前位置 #四个部分位位置0 0 0 160 方便4个调节信号都发1 向上或向前
        self.set_dri_position_condition(3,3,3,160) 
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(2)
        self.partner.empty_all()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 0,
                                                    "position": {"backAngle": 105, "longitudinalPosition": 20,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 1},timeout=2)
        #2s内首次恢复的信号是什么，就作为能不能进行控制的条件,目的2s内信号如果没来，也会等2s确认执不执行控制，而不是立马使用默认值
        #且由于座椅位置设置的前提条件与2s超时条件信号是同帧，无法测试调用接口后，2s超时信号来的场景，否则接口返回值out=0
        self.check_drvrseat_adjust(1,0,0,1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldPerc', 200)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiPerc', 200)
        sleep(2)
        self.check_drvrseat_adjust(0,1,1,0)
        
    @allure.title("启动场景_主驾座椅姿态设置2s内超时内不满足_不进行控制_Mars1")
    @pytest.mark.full
    def test_caseid_1987175(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Drvrseat_condition_allow()
        self.set_drvr_position1()
        #设置座椅当前位置 #四个部分位位置0 0 0 160 方便4个调节信号都发1 向上或向前
        self.set_dri_position_condition(0,0,0,0) 
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT,pause_all_bus=True)
        sleep(2)
        self.partner.empty_all()
        time1 = time.time()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 0,
                                                    "position": {"backAngle": 20, "longitudinalPosition": 20,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 1},timeout=2)
        
        self.check_drvrseat_adjust(0,0,0,0)
        
    @allure.title("启动场景_主驾座椅姿态设置2s内靠背信号没来_阻塞2s进行控制_Mars1")
    @pytest.mark.sanity
    def test_caseid_1987177(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Drvrseat_condition_allow()
        self.set_drvr_position1()
        #设置座椅当前位置 #四个部分位位置0 0 0 160 方便4个调节信号都发1 向上或向前
        self.set_drvr_position1()
        self.set_dri_position_condition(3,3,3,100)
        self.ipdu.pause_ecu_send('bodycan', 'SmdBodyFr01')
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(2)
        self.partner.empty_all()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 0,
                                                    "position": {"backAngle": 20, "longitudinalPosition": 20,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 1})
        #靠背信号没来_即使其他信号来了_也需要阻塞2s执行控制
        self.check_drvrseat_adjust(0,0,0,0)
        sleep(1)
        self.check_drvrseat_adjust(1,0,0,1)
        self.ipdu.resume_all_bus_send()
        
    @allure.title("非启动场景_主驾座椅姿态设置2s内靠背信号没来_无需阻塞2s进行控制_Mars1")
    @pytest.mark.full
    def test_caseid_1987179(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Drvrseat_condition_allow()
        self.set_drvr_position1()
        #设置座椅当前位置 #四个部分位位置0 0 0 160 方便4个调节信号都发1 向上或向前
        self.set_drvr_position1()
        self.set_dri_position_condition(3,3,3,100)
        self.ipdu.pause_ecu_send('bodycan', 'SmdBodyFr01')
       
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 0,
                                                    "position": {"backAngle": 20, "longitudinalPosition": 20,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 1})
        #靠背信号没来_即使其他信号来了_不需要阻塞2s执行控制
        self.check_drvrseat_adjust(1,0,0,1)
        self.ipdu.resume_all_bus_send()
        
    @allure.title("主驾座椅姿态设置_当前靠背不在范围内_不进行控制_Mars1")
    @pytest.mark.full
    def test_caseid_1987180(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Drvrseat_condition_allow()
        for i in [65,66,164,165]:
            logger.info(f"i=={i}")
            self.set_drvr_position1()
            #设置座椅当前位置 #四个部分位位置0 0 0 160 方便4个调节信号都发1 向上或向前
            self.set_dri_position_condition(3,3,3,i) 
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                            {"params": {"id": 0,
                                                        "position": {"backAngle": 100, "longitudinalPosition": 20,
                                                                    "verticalPosition": 20,
                                                                    "LegrestVerticalPosition": 20,
                                                                    }}},
                                            {"out": 1},timeout=2)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldPerc', 200)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiPerc', 200)
            sleep(2)
            if i == 66:
                self.check_drvrseat_adjust(0,2,1,0)
            elif i == 164:
                self.check_drvrseat_adjust(0,1,1,0)
            else:
                self.check_drvrseat_adjust(0,0,1,0)

    @allure.title("启动场景_副驾座椅姿态设置_前置条件满足_2s超时条件不满足_能立马返回success_Mars1")
    @pytest.mark.full
    def test_caseid_1987181(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Passseat_condition_allow()
        self.set_pass_position_condition(0,0,0,0)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(2)
        self.partner.empty_all()
        t1 = time.time()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 1,
                                                    "position": {"backAngle": 20, "longitudinalPosition": 100,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 1},timeout=2)
        t2 = time.time()
        assert abs(float(t2) - float(t1) ) < 1
        
    @allure.title("启动场景_副驾座椅姿态设置_前置条件不满足_2s超时条件满足_能立马返回Fasle_Mars1")
    @pytest.mark.full
    def test_caseid_1987182(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Passseat_condition_allow()
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 1)
        self.set_pass_position_condition(3,3,3,100)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(2)
        self.partner.empty_all()
        t1 = time.time()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 1,
                                                    "position": {"backAngle": 20, "longitudinalPosition": 100,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 0},timeout=2)
        t2 = time.time()
        assert abs(float(t2) - float(t1) ) < 1
    
    @allure.title("启动场景_副驾座椅姿态设置_前置条件不满足(0x130信号丢失)_不需阻塞2s返回1")
    @pytest.mark.full
    def test_caseid_1988066(self):
        msg_id = self.ipdu.get_signal_message("bodycan", "0x130")
        self.set_Passseat_condition_allow()
        sleep(0.5)
        self.ipdu.stop_send_pdu("bodycan", f"{msg_id}")
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        #确保服务连接
        sleep(5)
        t1 = time.time()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 1,
                                                    "position": {"backAngle": 100, "longitudinalPosition": 100,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                               }}},
                                        {"out": 1},timeout=0.5)
        self.ipdu.resume_all_bus_send()
        
    @allure.title("启动场景_副驾座椅姿态设置_前置条件不满足(0x0130信号值不满足)_不需阻塞2s返回0")
    @pytest.mark.full
    def test_caseid_1988068	(self):
        self.set_Passseat_condition_allow()
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 1)
        sleep(0.5)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        #确保服务连接
        sleep(5)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 0,
                                                    "position": {"backAngle": 100, "longitudinalPosition": 100,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                              }}},
                                        {"out": 0},timeout=0.5)
        
    @allure.title("启动场景_主驾座椅姿态设置2s内超时内条件满足_立马进行控制_Mars1")
    @pytest.mark.smoke
    def test_caseid_1987204(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Passseat_condition_allow()
        self.set_Pass_position1()
        #设置座椅当前位置 #四个部分位位置0 0 0 160 方便4个调节信号都发1 向上或向前
        self.set_pass_position_condition(3,3,3,160) 
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(2)
        self.partner.empty_all()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 1,
                                                    "position": {"backAngle": 105, "longitudinalPosition": 20,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 1},timeout=2)
        #2s内首次恢复的信号是什么，就作为能不能进行控制的条件,目的2s内信号如果没来，也会等2s确认执不执行控制，而不是立马使用默认值
        #且由于座椅位置设置的前提条件与2s超时条件信号是同帧，无法测试调用接口后，2s超时信号来的场景，否则接口返回值out=0
        self.check_Passseat_adjust(1,0,0,1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiPerc',  200)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldPerc',  200)
        sleep(0.5)
        self.check_Passseat_adjust(0,1,1,0)
        
    @allure.title("启动场景_副驾座椅姿态设置2s内超时内不满足_不进行控制_Mars1")
    @pytest.mark.full
    def test_caseid_1987205(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Passseat_condition_allow()
        self.set_Pass_position1()
        #设置座椅当前位置 #四个部分位位置0 0 0 160 方便4个调节信号都发1 向上或向前
        self.set_pass_position_condition(0,0,0,0) 
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT,pause_all_bus=True)
        sleep(2)
        self.partner.empty_all()
        time1 = time.time()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 1,
                                                    "position": {"backAngle": 105, "longitudinalPosition": 20,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 1},timeout=2)
        
        self.check_Passseat_adjust(0,0,0,0)
        
    @allure.title("启动场景_副驾座椅姿态设置2s内靠背信号没来_阻塞2s进行控制_Mars1")
    @pytest.mark.full
    def test_caseid_1987206(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Passseat_condition_allow()
        self.set_Pass_position1()
        #设置座椅当前位置 #四个部分位位置0 0 0 160 方便4个调节信号都发1 向上或向前
        self.set_pass_position_condition(3,3,3,160)
        self.ipdu.pause_ecu_send('bodycan', 'SmdBodyFr01')
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(2)
        self.partner.empty_all()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 1,
                                                    "position": {"backAngle": 20, "longitudinalPosition": 20,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 1})
        #靠背信号没来_即使其他信号来了_也需要阻塞2s执行控制
        self.check_Passseat_adjust(0,0,0,0)
        sleep(1)
        self.check_Passseat_adjust(1,0,0,1)
        self.ipdu.resume_all_bus_send()
        
    @allure.title("非启动场景_副驾座椅姿态设置2s内靠背信号没来_无需阻塞2s进行控制_Mars1")
    @pytest.mark.full
    def test_caseid_1987207(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Passseat_condition_allow()
        self.set_Pass_position1()
        #设置座椅当前位置 #四个部分位位置0 0 0 160 方便4个调节信号都发1 向上或向前
        self.set_pass_position_condition(3,3,3,160)
        self.ipdu.pause_ecu_send('bodycan', 'SmdBodyFr01')
       
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 1,
                                                    "position": {"backAngle": 105, "longitudinalPosition": 20,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 1})
        #靠背信号没来_即使其他信号来了_不需要阻塞2s执行控制
        self.check_Passseat_adjust(1,0,0,1)
        self.ipdu.resume_all_bus_send()
        
    @allure.title("副驾座椅姿态设置_当前靠背不在范围内_不进行控制_Mars1")
    @pytest.mark.full
    def test_caseid_1987208(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Passseat_condition_allow()
        for i in [65,66,164,165]:
            logger.info(f"i=={i}")
            self.set_Pass_position1()
            #设置座椅当前位置 #四个部分位位置0 0 0 160 方便4个调节信号都发1 向上或向前
            self.set_pass_position_condition(3,3,3,i) 
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                            {"params": {"id": 1,
                                                        "position": {"backAngle": 100, "longitudinalPosition": 20,
                                                                    "verticalPosition": 20,
                                                                    "LegrestVerticalPosition": 20,
                                                                    }}},
                                            {"out": 1},timeout=2)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiPerc',  200)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldPerc',  200)
            sleep(2)
            if i == 66:
                self.check_Passseat_adjust(0,2,1,0)
            elif i == 164:
                self.check_Passseat_adjust(0,1,1,0)
            else:
                self.check_Passseat_adjust(0,0,1,0)
        
    @allure.title("启动场景_主驾座椅姿态设置_前置条件满足_2s超时条件不满足_能立马返回success_Vanus")
    @pytest.mark.full
    def test_caseid_1987209(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.set_Drvrseat_condition_allow()
        self.set_dri_position_condition(0,0,0,0)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(2)
        self.partner.empty_all()
        t1 = time.time()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 0,
                                                    "position": {"backAngle": 20, "longitudinalPosition": 100,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 1},timeout=2)
        t2 = time.time()
        assert abs(float(t2) - float(t1) ) < 1
        
    @allure.title("启动场景_主驾座椅姿态设置_前置条件不满足_2s超时条件满足_能立马返回Fasle_Vanus")
    @pytest.mark.full
    def test_caseid_1987210(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.set_Drvrseat_condition_allow()
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 0)
        self.set_dri_position_condition(3,3,3,100)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(2)
        self.partner.empty_all()
        t1 = time.time()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 0,
                                                    "position": {"backAngle": 20, "longitudinalPosition": 100,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 0},timeout=2)
        t2 = time.time()
        assert abs(float(t2) - float(t1) ) < 0.5
    
    @allure.title("启动场景_主驾座椅姿态设置2s内超时内条件满足_立马进行控制_Vanus")
    @pytest.mark.smoke
    def test_caseid_1987211(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.set_Drvrseat_condition_allow()
        self.set_drvr_position1()
        #设置座椅当前位置 #四个部分位位置0 0 0 160 方便4个调节信号都发1 向上或向前
        self.set_dri_position_condition(3,3,3,160) 
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(2)
        self.partner.empty_all()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 0,
                                                    "position": {"backAngle": 105, "longitudinalPosition": 20,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 1},timeout=2)
        #2s内首次恢复的信号是什么，就作为能不能进行控制的条件,目的2s内信号如果没来，也会等2s确认执不执行控制，而不是立马使用默认值
        #且由于座椅位置设置的前提条件与2s超时条件信号是同帧，无法测试调用接口后，2s超时信号来的场景，否则接口返回值out=0
        self.check_drvrseat_adjust(1,0,0,1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldPerc', 200)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiPerc', 200)
        sleep(2)
        self.check_drvrseat_adjust(0,1,1,0)
        
    @allure.title("启动场景_主驾座椅姿态设置2s内超时内不满足_不进行控制_Vanus")
    @pytest.mark.full
    def test_caseid_1987212(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.set_Drvrseat_condition_allow()
        self.set_drvr_position1()
        #设置座椅当前位置 #四个部分位位置0 0 0 160 方便4个调节信号都发1 向上或向前
        self.set_dri_position_condition(0,0,0,0) 
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT,pause_all_bus=True)
        sleep(2)
        self.partner.empty_all()
        time1 = time.time()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 0,
                                                    "position": {"backAngle": 20, "longitudinalPosition": 20,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 1},timeout=2)
        
        self.check_drvrseat_adjust(0,0,0,0)
        
    @allure.title("启动场景_主驾座椅姿态设置2s内靠背信号没来_阻塞2s进行控制_Vanus")
    @pytest.mark.full
    def test_caseid_1987213(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.set_Drvrseat_condition_allow()
        self.set_drvr_position1()
        #设置座椅当前位置 #四个部分位位置0 0 0 160 方便4个调节信号都发1 向上或向前
        self.set_drvr_position1()
        self.set_dri_position_condition(3,3,3,100)
        self.ipdu.pause_ecu_send('bodycan', 'SmdBodyFr01')
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(2)
        self.partner.empty_all()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 0,
                                                    "position": {"backAngle": 20, "longitudinalPosition": 20,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 1})
        #靠背信号没来_即使其他信号来了_也需要阻塞2s执行控制
        self.check_drvrseat_adjust(0,0,0,0)
        sleep(1)
        self.check_drvrseat_adjust(1,0,0,1)
        self.ipdu.resume_all_bus_send()
        
    @allure.title("非启动场景_主驾座椅姿态设置2s内靠背信号没来_无需阻塞2s进行控制_Vanus")
    @pytest.mark.full
    def test_caseid_1987214(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.set_Drvrseat_condition_allow()
        self.set_drvr_position1()
        #设置座椅当前位置 #四个部分位位置0 0 0 160 方便4个调节信号都发1 向上或向前
        self.set_drvr_position1()
        self.set_dri_position_condition(3,3,3,100)
        self.ipdu.pause_ecu_send('bodycan', 'SmdBodyFr01')
       
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 0,
                                                    "position": {"backAngle": 20, "longitudinalPosition": 20,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 1})
        #靠背信号没来_即使其他信号来了_不需要阻塞2s执行控制
        self.check_drvrseat_adjust(1,0,0,1)
        self.ipdu.resume_all_bus_send()
        
    @allure.title("主驾座椅姿态设置_当前靠背不在范围内_不进行控制_Vanus")
    @pytest.mark.full
    def test_caseid_1987215(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.set_Drvrseat_condition_allow()
        for i in [99,100,175,176]:
            logger.info(f"i=={i}")
            self.set_drvr_position1()
            #设置座椅当前位置 #四个部分位位置0 0 0 160 方便4个调节信号都发1 向上或向前
            self.set_dri_position_condition(3,3,3,i) 
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                            {"params": {"id": 0,
                                                        "position": {"backAngle": 120, "longitudinalPosition": 20,
                                                                    "verticalPosition": 20,
                                                                    "LegrestVerticalPosition": 20,
                                                                    }}},
                                            {"out": 1},timeout=2)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldPerc', 200)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiPerc', 200)
            sleep(2)
            if i == 100:
                self.check_drvrseat_adjust(0,2,1,0)
            elif i == 175:
                self.check_drvrseat_adjust(0,1,1,0)
            else:
                self.check_drvrseat_adjust(0,0,1,0)


    @allure.title("启动场景_副驾座椅姿态设置_前置条件满足_2s超时条件不满足_能立马返回success_Vanus")
    @pytest.mark.full
    def test_caseid_1987216(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.set_Passseat_condition_allow()
        self.set_pass_position_condition(0,0,0,0)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(2)
        self.partner.empty_all()
        t1 = time.time()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 1,
                                                    "position": {"backAngle": 20, "longitudinalPosition": 100,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 1},timeout=2)
        t2 = time.time()
        assert abs(float(t2) - float(t1) ) < 1
        
    @allure.title("启动场景_副驾座椅姿态设置_前置条件不满足_2s超时条件满足_能立马返回Fasle_Vanus")
    @pytest.mark.full
    def test_caseid_1987217(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.set_Passseat_condition_allow()
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', 1)
        self.set_pass_position_condition(3,3,3,100)
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(2)
        self.partner.empty_all()
        t1 = time.time()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 1,
                                                    "position": {"backAngle": 20, "longitudinalPosition": 100,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 0},timeout=2)
        t2 = time.time()
        assert abs(float(t2) - float(t1) ) < 0.5
    
    @allure.title("启动场景_主驾座椅姿态设置2s内超时内条件满足_立马进行控制_Vanus")
    @pytest.mark.full
    def test_caseid_1987218(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.set_Passseat_condition_allow()
        self.set_Pass_position1()
        #设置座椅当前位置 #四个部分位位置0 0 0 160 方便4个调节信号都发1 向上或向前
        self.set_pass_position_condition(3,3,3,160) 
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(2)
        self.partner.empty_all()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 1,
                                                    "position": {"backAngle": 105, "longitudinalPosition": 20,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 1},timeout=2)
        #2s内首次恢复的信号是什么，就作为能不能进行控制的条件,目的2s内信号如果没来，也会等2s确认执不执行控制，而不是立马使用默认值
        #且由于座椅位置设置的前提条件与2s超时条件信号是同帧，无法测试调用接口后，2s超时信号来的场景，否则接口返回值out=0
        self.check_Passseat_adjust(1,0,0,1)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiPerc',  200)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldPerc',  200)
        sleep(0.5)
        self.check_Passseat_adjust(0,1,1,0)
        
    @allure.title("启动场景_副驾座椅姿态设置2s内超时内不满足_不进行控制_Vanus")
    @pytest.mark.full
    def test_caseid_1987219(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.set_Passseat_condition_allow()
        self.set_Pass_position1()
        #设置座椅当前位置 #四个部分位位置0 0 0 160 方便4个调节信号都发1 向上或向前
        self.set_pass_position_condition(0,0,0,0) 
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT,pause_all_bus=True)
        sleep(2)
        self.partner.empty_all()
        time1 = time.time()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 1,
                                                    "position": {"backAngle": 105, "longitudinalPosition": 20,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 1},timeout=2)
        
        self.check_Passseat_adjust(0,0,0,0)
        
    @allure.title("启动场景_副驾座椅姿态设置2s内靠背信号没来_阻塞2s进行控制_Vanus")
    @pytest.mark.full
    def test_caseid_1987220(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.set_Passseat_condition_allow()
        self.set_Pass_position1()
        #设置座椅当前位置 #四个部分位位置0 0 0 160 方便4个调节信号都发1 向上或向前
        self.set_pass_position_condition(3,3,3,160)
        self.ipdu.pause_ecu_send('bodycan', 'SmdBodyFr01')
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT)
        sleep(2)
        self.partner.empty_all()
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 1,
                                                    "position": {"backAngle": 20, "longitudinalPosition": 20,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 1})
        #靠背信号没来_即使其他信号来了_也需要阻塞2s执行控制
        self.check_Passseat_adjust(0,0,0,0)
        sleep(1)
        self.check_Passseat_adjust(1,0,0,1)
        self.ipdu.resume_all_bus_send()
        
    @allure.title("非启动场景_副驾座椅姿态设置2s内靠背信号没来_无需阻塞2s进行控制_Vanus")
    @pytest.mark.full
    def test_caseid_1987221(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.set_Passseat_condition_allow()
        self.set_Pass_position1()
        #设置座椅当前位置 #四个部分位位置0 0 0 160 方便4个调节信号都发1 向上或向前
        self.set_pass_position_condition(3,3,3,160)
        self.ipdu.pause_ecu_send('bodycan', 'SmdBodyFr01')
       
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 1,
                                                    "position": {"backAngle": 105, "longitudinalPosition": 20,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 1})
        #靠背信号没来_即使其他信号来了_不需要阻塞2s执行控制
        self.check_Passseat_adjust(1,0,0,1)
        self.ipdu.resume_all_bus_send()
        
    @allure.title("副驾座椅姿态设置_当前靠背不在范围内_不进行控制_Vanus")
    @pytest.mark.full
    def test_caseid_1987222(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.set_Passseat_condition_allow()
        for i in [99,100,175,176]:
            logger.info(f"i=={i}")
            self.set_Pass_position1()
            #设置座椅当前位置 #四个部分位位置0 0 0 160 方便4个调节信号都发1 向上或向前
            self.set_pass_position_condition(3,3,3,i) 
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                            {"params": {"id": 1,
                                                        "position": {"backAngle": 120, "longitudinalPosition": 20,
                                                                    "verticalPosition": 20,
                                                                    "LegrestVerticalPosition": 20,
                                                                    }}},
                                            {"out": 1},timeout=2)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiPerc',  200)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldPerc',  200)
            sleep(2)
            if i == 100:
                self.check_Passseat_adjust(0,2,1,0)
            elif i == 175:
                self.check_Passseat_adjust(0,1,1,0)
            else:
                self.check_Passseat_adjust(0,0,1,0)
        
    @allure.title("启动场景_主副驾座椅姿态设置_配置字不满足条件_不进行控制")
    @pytest.mark.full
    def test_caseid_1987223(self):
        self.sd_tester.write_single_ccp(950, 3)
        self.set_Passseat_condition_allow()
        self.set_Drvrseat_condition_allow()

        #设置座椅当前位置 #四个部分位位置0 0 0 160 方便4个调节信号都发1 向上或向前
      
        self.partner.empty_all()
        #返回值只和前置条件有关，与配置字无关
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 0,
                                                    "position": {"backAngle": 105, "longitudinalPosition": 20,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 1},timeout=2)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                        {"params": {"id": 1,
                                                    "position": {"backAngle": 105, "longitudinalPosition": 20,
                                                                "verticalPosition": 20,
                                                                "LegrestVerticalPosition": 20,
                                                                }}},
                                        {"out": 1},timeout=2)
        self.check_drvrseat_adjust(0,0,0,0)
        self.check_Passseat_adjust(0,0,0,0)
        self.sd_tester.write_single_ccp(950, 1)
        
    @allure.title("车内有人状态_下行PDU校验")
    @pytest.mark.sanity
    def test_caseid_1987242(self): 
        self.set_four_Door_open()
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                            {"firstLeftExist":False,"firstRightExist":False,"errorCode":0}})
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{"seatStsSecondLeft":{"installSts":False,"occupySts":False},"seatStsSecondRight":{"installSts":False,"occupySts":False}}})
        # self.bgm_eth_inter.start_bgm_tcpdump()
        #通过座椅占位控制
        self.io.driver_seat_present()
        self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":True,"userInVehicleStatusWithCam":True}},
                                    "GetVehicleInsidePersonSts", {})
        # self.ipdu.check_multiple_signals(
        #                         [(self.ipdu.connectivitycanfd.BgmConnectivityFr04, "UsrInVehSts", 1),
        #                         (self.ipdu.connectivitycanfd.BgmConnectivityFr04, "UsrInVehStsforDigKey", 1)], timeout=0.5)

        self.io.driver_seat_notpresent()
        sleep(3)
        self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":False,"userInVehicleStatusWithCam":False}},
                                    "GetVehicleInsidePersonSts", {})
        # self.ipdu.check_multiple_signals(
        #                         [(self.ipdu.connectivitycanfd.BgmConnectivityFr04, "UsrInVehSts", 0),
        #                         (self.ipdu.connectivitycanfd.BgmConnectivityFr04, "UsrInVehStsforDigKey", 0)], timeout=0.5)
        #通过视觉控制
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                            {"firstLeftExist":True,"firstRightExist":True,"errorCode":0}})
        self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":False,"userInVehicleStatusWithCam":True}},
                                    "GetVehicleInsidePersonSts", {})
        # self.ipdu.check_multiple_signals(
        #                         [(self.ipdu.connectivitycanfd.BgmConnectivityFr04, "UsrInVehSts", 0),
        #                         (self.ipdu.connectivitycanfd.BgmConnectivityFr04, "UsrInVehStsforDigKey", 1)], timeout=0.5)
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                            {"firstLeftExist":False,"firstRightExist":False,"errorCode":0}})
        self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":False,"userInVehicleStatusWithCam":False}},
                                    "GetVehicleInsidePersonSts", {})
        # self.ipdu.check_multiple_signals(
        #                         [(self.ipdu.connectivitycanfd.BgmConnectivityFr04, "UsrInVehSts", 0),
        #                         (self.ipdu.connectivitycanfd.BgmConnectivityFr04, "UsrInVehStsforDigKey", 0)], timeout=0.5)
        #通过儿童座椅控制
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{"seatStsSecondLeft":{"installSts":True,"occupySts":True},
                                                    "seatStsSecondRight":{"installSts":False,"occupySts":False}}})
        self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":True,"userInVehicleStatusWithCam":True}},
                                    "GetVehicleInsidePersonSts", {})
        # self.ipdu.check_multiple_signals(
        #                         [(self.ipdu.connectivitycanfd.BgmConnectivityFr04, "UsrInVehSts", 1),
        #                         (self.ipdu.connectivitycanfd.BgmConnectivityFr04, "UsrInVehStsforDigKey", 1)], timeout=0.5)
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{"seatStsSecondLeft":{"installSts":False,"occupySts":False},"seatStsSecondRight":{"installSts":False,"occupySts":False}}})
        sleep(3)
        self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":False,"userInVehicleStatusWithCam":False}},
                                    "GetVehicleInsidePersonSts", {})
        # self.ipdu.check_multiple_signals(
        #                         [(self.ipdu.connectivitycanfd.BgmConnectivityFr04, "UsrInVehSts", 0),
        #                         (self.ipdu.connectivitycanfd.BgmConnectivityFr04, "UsrInVehStsforDigKey", 0)], timeout=0.5)
        # sleep(2)
        # self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        # self.bgm_eth_inter.ck_ordered_array("UsrInVehSts", [0,1,0,1,0])
        # self.bgm_eth_inter.ck_ordered_array("UsrInVehStsforDigKey", [0,1,0,1,0,1,0])
        # #存在插帧，一次插帧可能会影响两个的周期
        # self.bgm_eth_inter.ck_period_time("UsrInVehSts", period=0.5, permit_fail_times=12)
        # self.bgm_eth_inter.ck_period_time("UsrInVehStsforDigKey", period=0.5, permit_fail_times=12)
     
    @allure.title("座椅占位视觉融合_默认值")   
    @pytest.mark.full
    def test_caseid_1987243(self): 
        self.restart_bgm_and_connect_service(SEAT_SERVICE_CLIENT,  pause_all_bus=True, resume_all_bus=False)
        sleep(2)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetOccupiedValidity",
                                                {"seats": [12]},{"out": [
                                                    {"value": {"seatId": 0, "statusWithCam": 0}},
                                                    {"value": {"seatId": 1, "statusWithCam": 0}},
                                                    {"value": {"seatId": 4, "statusWithCam": 255}},
                                                    {"value": {"seatId": 5, "statusWithCam": 255}},
                                                    {"value": {"seatId": 6, "statusWithCam": 255}}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetOccupied", {"seats": [12]},
                                                {"out": [{"seatId": 0, "statusWithCam": 0},
                                                        {"seatId": 1, "statusWithCam": 0},
                                                        {"seatId": 4, "statusWithCam": 255},
                                                        {"seatId": 5, "statusWithCam": 255},
                                                        {"seatId": 6, "statusWithCam": 255}]})
        self.ipdu.resume_all_bus_send()
        
    @allure.title("主驾座椅占位视觉融合")
    @pytest.mark.sanity
    def test_caseid_1987244(self): 
        self.set_four_Door_open()
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(0,0,0,0,0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 0) 
        sleep(2)
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                            {"firstLeftExist":False,"firstRightExist":False,"errorCode":0}})
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{"seatStsSecondLeft":{"installSts":False,"occupySts":False},"seatStsSecondRight":{"installSts":False,"occupySts":False}}})
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr04, 'DrvrSeatSts2', 1, timeout=0.5)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.empty_all(3)
        self.io.driver_seat_present()
        self.ck_event_and_resp_SeatOccupyWithCam(0,1)
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr04, 'DrvrSeatSts2', 2, timeout=0.5)
        self.partner.empty_all(0.5)
        self.io.driver_seat_notpresent()
        sleep(2)
        self.ck_event_and_resp_SeatOccupyWithCam(0,0)
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr04, 'DrvrSeatSts2', 1, timeout=0.5)
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                            {"firstLeftExist":True,"firstRightExist":False,"errorCode":0}})
        self.ck_event_and_resp_SeatOccupyWithCam(0,1)
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr04, 'DrvrSeatSts2', 2, timeout=0.5)
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                            {"firstLeftExist":False,"firstRightExist":False,"errorCode":0}})
        self.ck_event_and_resp_SeatOccupyWithCam(0,0)
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr04, 'DrvrSeatSts2', 1, timeout=0.5)
        self.set_four_seat_occupt(1,0,0,0)
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                            {"firstLeftExist":False,"firstRightExist":True,"errorCode":0}})
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr04, 'DrvrSeatSts2', 1, timeout=0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("DrvrSeatSts2",[1,2,1,2,1])
        self.bgm_eth_inter.ck_period_time("DrvrSeatSts2", period=0.5, permit_fail_times=6)
        
    @allure.title("副驾座椅占位视觉融合")
    @pytest.mark.full
    def test_caseid_1987245(self): 
        self.set_four_Door_open()
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(0,0,0,0,0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 0) 
        sleep(2)
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                            {"firstLeftExist":False,"firstRightExist":False,"errorCode":0}})
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{"seatStsSecondLeft":{"installSts":False,"occupySts":False},"seatStsSecondRight":{"installSts":False,"occupySts":False}}})
        self.set_four_seat_occupt(1,0,0,0)
        self.ck_event_and_resp_SeatOccupyWithCam(1,1)
        self.set_four_seat_occupt(0,0,0,0)
        sleep(2)
        self.ck_event_and_resp_SeatOccupyWithCam(1,0)
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                            {"firstLeftExist":False,"firstRightExist":True,"errorCode":0}})
        self.ck_event_and_resp_SeatOccupyWithCam(1,1)
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                            {"firstLeftExist":False,"firstRightExist":False,"errorCode":0}})
        self.ck_event_and_resp_SeatOccupyWithCam(0,0)
        
    @allure.title("安全带信号滤波处理_主驾安全带状态")
    @pytest.mark.sanity
    def test_caseid_1989624(self): 
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05,'BltLockStAtDrvrBltLockSt1', 0, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05,'BltLockStAtDrvrBltLockSts', 0, ub_flag=False)
        self.partner.empty_all(1)  
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05,'BltLockStAtDrvrBltLockSt1', 0, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05,'BltLockStAtDrvrBltLockSts', 1, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts",
                                            {"status":{"value": 2}}, timeout=1, deviation=0.2)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05,'BltLockStAtDrvrBltLockSts', 0, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts",
                                            {"status":{"value": 1}}, timeout=0.5)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05,'BltLockStAtDrvrBltLockSt1', 1, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05,'BltLockStAtDrvrBltLockSts', 0, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts",
                                            {"status":{"value": 0}}, timeout=0.5)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05,'BltLockStAtDrvrBltLockSts', 1, ub_flag=False)
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts" , timeout=0.5)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05,'BltLockStAtDrvrBltLockSts', 0, ub_flag=False)
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts")
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05,'BltLockStAtDrvrBltLockSts', 1, ub_flag=False)
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts" , timeout=0.5)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05,'BltLockStAtDrvrBltLockSt1', 0, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05,'BltLockStAtDrvrBltLockSts', 0, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts",
                                            {"status":{"value": 1}}, timeout=0.5)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05,'BltLockStAtDrvrBltLockSt1', 1, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05,'BltLockStAtDrvrBltLockSts', 1, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "FrntLeftBeltSts",
                                            {"status":{"value": 2}}, timeout=1, deviation=0.2)
        
    @allure.title("安全带信号滤波处理_副驾安全带状态")
    @pytest.mark.full
    def test_caseid_1989625(self): 
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtPassBltLockSt1', 0, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtPassBltLockSts', 0, ub_flag=False)
        self.partner.empty_all(1)  
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtPassBltLockSt1', 0, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtPassBltLockSts', 1, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "FrntRightBeltSts",
                                            {"status":{"value": 2}}, timeout=1, deviation=0.2)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtPassBltLockSts', 0, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "FrntRightBeltSts",
                                            {"status":{"value": 1}}, timeout=0.5)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtPassBltLockSt1', 1, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtPassBltLockSts', 0, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "FrntRightBeltSts",
                                            {"status":{"value": 0}}, timeout=0.5)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtPassBltLockSts', 1, ub_flag=False)
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntRightBeltSts" , timeout=0.5)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtPassBltLockSts', 0, ub_flag=False)
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntRightBeltSts")
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtPassBltLockSts', 1, ub_flag=False)
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntRightBeltSts" , timeout=0.5)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtPassBltLockSt1', 0, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtPassBltLockSts', 0, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "FrntRightBeltSts",
                                            {"status":{"value": 1}}, timeout=0.5)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtPassBltLockSt1', 1, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtPassBltLockSts', 1, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "FrntRightBeltSts",
                                            {"status":{"value": 2}}, timeout=1, deviation=0.2)
        
    @allure.title("安全带信号滤波处理_二排左安全带状态")
    @pytest.mark.full
    def test_caseid_1989626(self): 
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSt1', 0, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 0, ub_flag=False)
        self.partner.empty_all(1)  
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSt1', 0, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 1, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "RearLeftBeltSts",
                                            {"status":{"value": 2}}, timeout=1, deviation=0.2)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 0, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "RearLeftBeltSts",
                                            {"status":{"value": 1}}, timeout=0.5)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSt1', 1, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 0, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "RearLeftBeltSts",
                                            {"status":{"value": 0}}, timeout=0.5)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 1, ub_flag=False)
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearLeftBeltSts" , timeout=0.5)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 0, ub_flag=False)
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearLeftBeltSts")
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 1, ub_flag=False)
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearLeftBeltSts" , timeout=0.5)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSt1', 0, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 0, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "RearLeftBeltSts",
                                            {"status":{"value": 1}}, timeout=0.5)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSt1', 1, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 1, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "RearLeftBeltSts",
                                            {"status":{"value": 2}}, timeout=1, deviation=0.2)
        
    @allure.title("安全带信号滤波处理_二排中安全带状态")
    @pytest.mark.full
    def test_caseid_1989627(self): 
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSt1', 0, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 0, ub_flag=False)
        self.partner.empty_all(1)  
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSt1', 0, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 1, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "RearMiddleBeltSts",
                                            {"status":{"value": 2}}, timeout=1, deviation=0.2)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 0, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "RearMiddleBeltSts",
                                            {"status":{"value": 1}}, timeout=0.5)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSt1', 1, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 0, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "RearMiddleBeltSts",
                                            {"status":{"value": 0}}, timeout=0.5)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 1, ub_flag=False)
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearMiddleBeltSts" , timeout=0.5)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 0, ub_flag=False)
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearMiddleBeltSts")
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 1, ub_flag=False)
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearMiddleBeltSts" , timeout=0.5)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSt1', 0, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 0, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "RearMiddleBeltSts",
                                            {"status":{"value": 1}}, timeout=0.5)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSt1', 1, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 1, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "RearMiddleBeltSts",
                                            {"status":{"value": 2}}, timeout=1, deviation=0.2)
        
    @allure.title("安全带信号滤波处理_二排右安全带状态")
    @pytest.mark.full
    def test_caseid_1989628(self): 
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSt1', 0, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 0, ub_flag=False)
        self.partner.empty_all(1)  
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSt1', 0, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 1, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "RearRightBeltSts",
                                            {"status":{"value": 2}}, timeout=1, deviation=0.2)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 0, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "RearRightBeltSts",
                                            {"status":{"value": 1}}, timeout=0.5)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSt1', 1, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 0, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "RearRightBeltSts",
                                            {"status":{"value": 0}}, timeout=0.5)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 1, ub_flag=False)
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearRightBeltSts" , timeout=0.5)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 0, ub_flag=False)
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearRightBeltSts")
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 1, ub_flag=False)
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "RearRightBeltSts" , timeout=0.5)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSt1', 0, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 0, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "RearRightBeltSts",
                                            {"status":{"value": 1}}, timeout=0.5)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSt1', 1, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 1, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "RearRightBeltSts",
                                            {"status":{"value": 2}}, timeout=1, deviation=0.2)
        
    @allure.title("后排左安全带报警_迁移流程cf_带UB位")
    @pytest.mark.sanity
    def test_caseid_1987732(self): 
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 0)
        sleep(0.5)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(1,1,1,1,1)
        
        self.sd_tester.change_usage_mode(2)
        self.set_four_seat_occupt(0,1,0,0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSt1', 0, ub_flag=False)
        #SOA-29913
        # self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 1, ub_flag=False)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 4, "warn": 2})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 4, "warn":{"value":2}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 4, "status": 2}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":4, "status": 2}}]})
        
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(1,1,1,1,1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 4, "warn": 1})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 4, "warn":{"value":1}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 4, "status": 1}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":4, "status": 1}}]})
        
    @allure.title("后排中安全带报警_迁移流程cf_带UB位")
    @pytest.mark.full
    def test_caseid_1987733(self): 
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 0)
        sleep(0.5)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(1,1,1,1,1)
        
        self.sd_tester.change_usage_mode(2)
        self.set_four_seat_occupt(0,0,1,0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSt1', 0, ub_flag=False)
        # self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 1, ub_flag=False)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 5, "warn": 2})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 5, "warn":{"value":2}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 5, "status": 2}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":5, "status": 2}}]})
        
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(1,1,1,1,1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 5, "warn": 1})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 5, "warn":{"value":1}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 5, "status": 1}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":5, "status": 1}}]})
        
    @allure.title("后排右安全带报警_迁移流程cf_带UB位")
    @pytest.mark.full
    def test_caseid_1987734(self): 
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 0)
        sleep(0.5)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(1,1,1,1,1)
        
        self.sd_tester.change_usage_mode(2)
        self.set_four_seat_occupt(0,0,0,1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSt1', 0, ub_flag=False)
        # self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 1, ub_flag=False)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 6, "warn": 2})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 6, "warn":{"value":2}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 6, "status": 2}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":6, "status": 2}}]})
        
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(1,1,1,1,1)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 6, "warn": 1})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 6, "warn":{"value":1}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 6, "status": 1}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":6, "status": 1}}]})
        
    @allure.title("后排左安全带报警_迁移流程e_带UB位")
    @pytest.mark.full
    def test_caseid_1987735(self): 
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 0)
        sleep(0.5)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(1,1,1,1,1)
        
        self.sd_tester.change_usage_mode(2)
        self.set_four_seat_occupt(0,1,0,0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSt1', 0, ub_flag=False)
        # self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 1, ub_flag=False)
        self.Shift_Gear(2)
        self.set_vehicle_speed(7.0)
        
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 4, "warn": 3})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 4, "warn":{"value":3}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 4, "status": 3}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":4, "status": 3}}]})
        self.Shift_Gear(0)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 4, "warn": 2})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 4, "warn":{"value":2}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 4, "status": 2}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":4, "status": 2}}]})
        
    @allure.title("后排中安全带报警_迁移流程e_带UB位")
    @pytest.mark.full
    def test_caseid_1987744(self): 
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 0)
        sleep(0.5)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(1,1,1,1,1)
        
        self.sd_tester.change_usage_mode(2)
        self.set_four_seat_occupt(0,0,1,0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSt1', 0, ub_flag=False)
        # self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 1, ub_flag=False)
        self.Shift_Gear(2)
        self.set_vehicle_speed(7.0)
        
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 5, "warn": 3})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 5, "warn":{"value":3}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 5, "status": 3}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":5, "status": 3}}]})
        self.Shift_Gear(0)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 5, "warn": 2})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 5, "warn":{"value":2}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 5, "status": 2}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":5, "status": 2}}]})
        
    @allure.title("后排右安全带报警_迁移流程e_带UB位")
    @pytest.mark.full
    def test_caseid_1987745(self): 
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 0)
        sleep(0.5)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(1,1,1,1,1)
        
        self.sd_tester.change_usage_mode(2)
        self.set_four_seat_occupt(0,0,0,1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSt1', 0, ub_flag=False)
        # self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 1, ub_flag=False)
        self.Shift_Gear(2)
        self.set_vehicle_speed(7.0)
        
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 6, "warn": 3})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 6, "warn":{"value":3}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 6, "status": 3}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":6, "status": 3}}]})
        self.Shift_Gear(0)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 6, "warn": 2})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 6, "warn":{"value":2}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 6, "status": 2}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":6, "status": 2}}]})
        
    @allure.title("后排左安全带报警_迁移流程h_带UB位")
    @pytest.mark.full
    def test_caseid_1987746(self): 
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 0)
        sleep(0.5)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(1,1,1,1,1)
        
        self.sd_tester.change_usage_mode(2)
        self.set_four_seat_occupt(0,1,0,0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSt1', 0, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 0, ub_flag=False)

        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 4, "warn": 2})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 4, "warn":{"value":2}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 4, "status": 2}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":4, "status": 2}}]})
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 1, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 4, "warn": 5},timeout=1, deviation=0.3)
        
    @allure.title("后排中安全带报警_迁移流程h_带UB位")
    @pytest.mark.full
    def test_caseid_1987747(self): 
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 0)
        sleep(0.5)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(1,1,1,1,1)
        
        self.sd_tester.change_usage_mode(2)
        self.set_four_seat_occupt(0,0,1,0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSt1', 0, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 0, ub_flag=False)

        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 5, "warn": 2})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 5, "warn":{"value":2}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 5, "status": 2}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":5, "status": 2}}]})
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 1, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 5, "warn": 5},timeout=1, deviation=0.3)
        
    @allure.title("后排右安全带报警_迁移流程h_带UB位")
    @pytest.mark.full
    def test_caseid_1987748(self): 
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 0)
        sleep(0.5)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(1,1,1,1,1)
        
        self.sd_tester.change_usage_mode(2)
        self.set_four_seat_occupt(0,0,0,1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSt1', 0, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 0, ub_flag=False)

        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 6, "warn": 2})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 6, "warn":{"value":2}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 6, "status": 2}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":6, "status": 2}}]})
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 1, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 6, "warn": 5},timeout=1, deviation=0.3)
        
    @allure.title("后排左安全带报警_迁移流程i_带UB位")
    @pytest.mark.full
    def test_caseid_1987749(self): 
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 0)
        sleep(0.5)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(1,1,1,1,1)
        
        self.sd_tester.change_usage_mode(2)
        self.set_four_seat_occupt(0,1,0,0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSt1', 0, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 0, ub_flag=False)
        self.Shift_Gear(2)
        self.set_vehicle_speed(7.0)
        
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 4, "warn": 3})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 4, "warn":{"value":3}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 4, "status": 3}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":4, "status": 3}}]})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 1, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 4, "warn": 5},timeout=1, deviation=0.3)
        
    @allure.title("后排中安全带报警_迁移流程i_带UB位")
    @pytest.mark.full
    def test_caseid_1987750(self): 
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 0)
        sleep(0.5)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(1,1,1,1,1)
        
        self.sd_tester.change_usage_mode(2)
        self.set_four_seat_occupt(0,0,1,0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSt1', 0, ub_flag=False)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 0, ub_flag=False)
        self.Shift_Gear(2)
        self.set_vehicle_speed(7.0)
        
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 5, "warn": 3})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 5, "warn":{"value":3}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 5, "status": 3}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":5, "status": 3}}]})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 1, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 5, "warn": 5},timeout=1, deviation=0.3)
        
    @allure.title("后排右安全带报警_迁移流程i_带UB位")
    @pytest.mark.full
    def test_caseid_1987751(self): 
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 0)
        sleep(0.5)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(1,1,1,1,1)
        
        self.sd_tester.change_usage_mode(2)
        self.set_four_seat_occupt(0,0,0,1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSt1', 0, ub_flag=False)
        # self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 1, ub_flag=False)
        self.Shift_Gear(2)
        self.set_vehicle_speed(7.0)
        
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 6, "warn": 3})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarningValidity", {"id": 6, "warn":{"value":3}})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 6, "status": 3}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":6, "status": 3}}]})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 1, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 6, "warn": 5},timeout=1, deviation=0.3)
    
    @allure.title("后排左安全带报警_迁移流程jk_带UB位")
    @pytest.mark.full
    def test_caseid_1987752(self): 
        self.sd_tester.change_usage_mode(2)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_NA_status(0,0,0,0,0)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 1)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 4, "warn": 5},timeout=1, deviation=0.3)
  
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 4, "status": 5}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":4, "status": 5}}]})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 0, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 4, "warn": 1},timeout=0.5)
        self.seat_NA_status(0,0,0,0,0)
        
    @allure.title("后排中安全带报警_迁移流程jk_带UB位")
    @pytest.mark.full
    def test_caseid_1987753(self): 
        self.sd_tester.change_usage_mode(2)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_NA_status(0,0,0,0,0)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 1)
        
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 5, "warn": 5},timeout=1, deviation=0.3)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 5, "status": 5}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":5, "status": 5}}]})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 0, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 5, "warn": 1},timeout=0.5)
        self.seat_NA_status(0,0,0,0,0)
        
    @allure.title("后排右安全带报警_迁移流程jk_带UB位")
    @pytest.mark.full
    def test_caseid_1987754(self): 
        self.sd_tester.change_usage_mode(2)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_NA_status(0,0,0,0,0)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 1)
        
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 6, "warn": 5},timeout=1, deviation=0.3)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarning", {"seats": [12]},
                                                        {"out": [{"id": 6, "status": 5}]})
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltWarningValidity", {"seats": [12]},
                                                {"out": [{"value": {"id":6, "status": 5}}]})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 0, ub_flag=False)
        self.partner.ck_coming_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 6, "warn": 1},timeout=0.5)
        self.seat_NA_status(0,0,0,0,0)
        
        
    @allure.title("安全带信号滤波处理_安全带故障")
    @pytest.mark.smoke
    def test_caseid_1989629(self): 
        self.set_no_seatFault()
        self.set_seatBeltFault(1, 1, 1, 1, 1, ub_flage=False)
        #set_seatBeltFault有等待0.5s
        self.partner.ck_coming_event_and_resp(SEAT_SERVICE_CLIENT, "SeatFault",
                                  {"faults": [{"faultId": 6, "faultMsg": "", "seatId": 0},
                                              {"faultId": 6, "faultMsg": "", "seatId": 1},
                                              {"faultId": 6, "faultMsg": "", "seatId": 4},
                                              {"faultId": 6, "faultMsg": "", "seatId": 5},
                                              {"faultId": 6, "faultMsg": "", "seatId": 6},
                                              ]}, timeout = 0.5, deviation= 0.3)
        self.set_seatBeltFault(0, 0, 0, 0, 0, ub_flage=False)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatFault", {}, {"out": 
                                            [{"faultId": 0, "faultMsg": "", "seatId": 12}]})
        
    @allure.title("安全带状态仅带UB位变化_无通知上报")
    @pytest.mark.full
    def test_caseid_1987885(self): 
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05,'BltLockStAtDrvrBltLockSt1', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtPassBltLockSt1', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSt1', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSt1', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSt1', 0)
        self.set_seatBeltFault(0,0,0,0,0,True)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                        {"out": [{"id": 0, "status": 1},
                                                 {"id": 1, "status": 1},
                                                 {"id": 4, "status": 1},
                                                 {"id": 5, "status": 1},
                                                 {"id": 6, "status": 1}]})
        self.partner.empty_all(1)
        self.set_seatBeltFault(0,0,0,0,0,False)
        self.ckAllSeatbeltStatusNoEvent()
        self.partner.empty_all(1)
        self.set_seatBeltFault(0,0,0,0,0,True)
        self.ckAllSeatbeltStatusNoEvent()

    @allure.title("安全带故障仅带UB位变化_无通知上报")
    @pytest.mark.full
    def test_caseid_1987886(self): 
        self.set_no_seatFault()
        self.set_seatBeltFault(1,1,1,1,1,True)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatFault", {"seats": [12]},
                                        {"out": [{"faultId": 6, "faultMsg": "", "seatId": 0},
                                              {"faultId": 6, "faultMsg": "", "seatId": 1},
                                              {"faultId": 6, "faultMsg": "", "seatId": 4},
                                              {"faultId": 6, "faultMsg": "", "seatId": 5},
                                              {"faultId": 6, "faultMsg": "", "seatId": 6}
                                              ]})
        self.partner.empty_all(1)
        self.set_seatBeltFault(1,1,1,1,1,False)
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "SeatFault")
        self.partner.empty_all(1)
        self.set_seatBeltFault(1,1,1,1,1,True)
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "SeatFault")
        self.set_no_seatFault()
        
    @allure.title("后排安全带报警仅带UB位变化_无通知上报")
    @pytest.mark.full
    def test_caseid_1987887(self): 
        self.set_seatBeltFault(0,0,0,0,0,True)
        sleep(0.5)
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(1,1,1,1,1)
        
        self.sd_tester.change_usage_mode(2)
        self.set_four_seat_occupt(0,1,1,1)
        self.seat_belt_status(0,0,0,0,0)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 4, "warn": 2})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 5, "warn": 2})
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "BeltWarning", {"id": 6, "warn": 2})
        
        self.partner.empty_all(1)
        self.set_seatBeltFault(0,0,0,0,0,False)
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "BeltWarning")
        self.partner.empty_all(1)
        self.set_seatBeltFault(0,0,0,0,0,True)
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "BeltWarning")
        self.set_four_seat_occupt(0,0,0,0)
        self.seat_belt_status(1,1,1,1,1)
       
    @allure.title("主驾座椅加热_加热状态非0到0_1s内加热状态&通风状态&通风等级变化")
    @pytest.mark.sanity
    def test_caseid_1988581(self): 
        for LvlSts in [1,2,3]:
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgAvlSts',0)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentnLvlSts',0)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentAvlSts',0)
            sleep(0.5)
            for AvlSts in [1,2,3,4,5,6,7,0]:
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                            {"params": [{"id": 0, "uint8Info": LvlSts}]})
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgLvlSts',LvlSts)
                sleep(1)
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgLvlSts',0)
                self.partner.empty_all(0.2)
                #设置加热状态、通风状态、通风等级变化
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgAvlSts',AvlSts)
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentAvlSts',AvlSts)
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentnLvlSts',LvlSts)
                
                logger.info(f"LvlSts = {LvlSts}, AvlSts = {AvlSts}")
                if AvlSts not in [3,4,5]:
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                                    {"status":{"heatWorkStatus":AvlSts,"ventWorkStatus":AvlSts,"ventLevel":LvlSts}})
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                                    {"status":{"heatLevel":0}})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                                    {"out": [{"id":0,"status":{"heatLevel":0,"heatWorkStatus":AvlSts,"ventWorkStatus":AvlSts,"ventLevel":LvlSts}}
                                                            ]},timeout = 1)
                else :
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                                    {"status":{"heatLevel":0}})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                                    {"out": [{"id":0,"status":{"heatLevel":0,"heatWorkStatus":AvlSts,"ventWorkStatus":AvlSts,"ventLevel":LvlSts}}
                                                            ]},timeout = 1)
                    
    @allure.title("副驾座椅加热_加热状态非0到0_1s内source_time变化")
    @pytest.mark.sanity
    def test_caseid_1988582(self): 
        self.sd_tester.change_usage_mode(2)
        for LvlSts in [1,2,3]:
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                    {"params": [{"id": 1}],"source":0})
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingTime",
                                                {"params": [{"id": 1, "uint64Info": 0}]})
            for sourcetime in [1,2,0]:
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                            {"params": [{"id": 0, "uint8Info": LvlSts}]})
                self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgLvlSts',LvlSts)
                sleep(1)
                self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgLvlSts',0)
                self.partner.empty_all(0.2)
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                    {"params": [{"id": 1}],"source":sourcetime})
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetHeatingTime",
                                                {"params": [{"id": 1, "uint64Info": sourcetime}]})
                
                logger.info(f"LvlSts = {LvlSts}, sourcetime = {sourcetime}")
                self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus",
                                                    {"status":{"source":sourcetime,"heatTime":sourcetime}})
                self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus",
                                                {"status":{"heatLevel":0}})
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                                {"out": [{"id":1,"status":{"heatLevel":0}}
                                                        ]},timeout = 1)  
                           
    @allure.title("二排左座椅通风_通风状态非0到0_1s内加热状态&通风状态&加热等级变化")
    @pytest.mark.full
    def test_caseid_1988583(self): 
        for LvlSts in [1,2,3]:
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecLe',0)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecLe',0)
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecLe',0)
            sleep(0.5)
            for AvlSts in [1,2,3,4,5,6,7,0]:
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                            {"params": [{"id": 4, "uint8Info": LvlSts}]})
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecLe',LvlSts)
                sleep(1)
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecLe',0)
                self.partner.empty_all(0.2)
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecLe',AvlSts)
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecLe',LvlSts)
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecLe',AvlSts)
                logger.info(f"LvlSts = {LvlSts}, AvlSts = {AvlSts}")
                if AvlSts not in [3,4,5]:
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus",
                                                    {"status":{"heatWorkStatus":AvlSts,"ventWorkStatus":AvlSts,"heatLevel":LvlSts}})
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus",
                                                    {"status":{"ventLevel":0}})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                                    {"out": [{"id":4,"status":{"heatWorkStatus":AvlSts,"ventWorkStatus":AvlSts,"heatLevel":LvlSts,"ventLevel":0}}
                                                            ]},timeout = 1)
                else :
                    self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearLeftSeatHeatVentStatus",
                                                    {"status":{"heatWorkStatus":AvlSts,"ventWorkStatus":AvlSts,"ventLevel":LvlSts,"ventLevel":0}})
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                                    {"out": [{"id":4,"status":{"heatWorkStatus":AvlSts,"ventWorkStatus":AvlSts,"heatLevel":LvlSts,"ventLevel":0}}
                                                            ]},timeout = 1)
                             
    @allure.title("二排右座椅通风_通风状态非0到0_1s内source_time变化")
    @pytest.mark.full
    def test_caseid_1988585(self): 
        self.sd_tester.change_usage_mode(2)
        for LvlSts in [1,2,3]:
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                    {"params": [{"id": 6}],"source":0})
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingTime",
                                                {"params": [{"id": 6, "uint64Info": 0}]})
            for sourcetime in [1,2,0]:
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                            {"params": [{"id": 0, "uint8Info": LvlSts}]})
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecRi',LvlSts)
                sleep(1)
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecRi',0)
                self.partner.empty_all(0.2)
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                    {"params": [{"id": 6}],"source":sourcetime})
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingTime",
                                                {"params": [{"id": 6, "uint64Info": sourcetime}]})
                logger.info(f"LvlSts = {LvlSts}, sourcetime = {sourcetime}")
                self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus",
                                                    {"status":{"source":sourcetime,"ventTime":sourcetime}})
                self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "RearRightSeatHeatVentStatus",
                                                {"status":{"ventLevel":0}})
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                                {"out": [{"id":6,"status":{"ventLevel":0}}
                                                        ]},timeout = 1)  
                
    #SOA-27307 补充
    @allure.title("副驾座椅加热_加热状态非0到0_1s内不会触发多余event")
    @pytest.mark.full
    def test_caseid_1988578(self): 
        for i in [1,2,3]:
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                        {"params": [{"id": 1, "uint8Info": i}]})
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgLvlSts',i)
            self.partner.empty_all(1)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgLvlSts',0)
            #必须加等待
            sleep(0.2)
            self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus",timeout = 0.5)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                            {"out": [{"id":1,"status":{"heatLevel":i}},
                                                    ]},timeout = 0.2)
            
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatHeatVentStatus",
                                            {"status":{"heatLevel":0}})
            
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                            {"out": [{"id":1,"status":{"heatLevel":0}}
                                                    ]},timeout = 1)
                   
    #SOA-27307 补充
    @allure.title("主驾座椅_通风状态非0到0_1s内不会触发多余event")
    @pytest.mark.sanity
    def test_caseid_1988576(self): 
        for i in [1,2,3]:
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                {"params": [{"id": 0, "uint8Info": i}]})
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentnLvlSts',i)
            self.partner.empty_all(1)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentnLvlSts',0)
            #必须加等待
            sleep(0.2)
            self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",timeout = 0.5)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                            {"out": [{"id":0,"status":{"ventLevel":i}},
                                                    ]},timeout = 0.2)
            
            self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatHeatVentStatus",
                                            {"status":{"ventLevel":0}})
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatHeatVentStatus", {"seats": [12]},
                                            {"out": [{"id":0,"status":{"ventLevel":0}}
                                                    ]},timeout = 1)     
            
    @allure.title("本地座椅加热_信号下发取消插帧_接口调用触发下发")
    @pytest.mark.sanity
    def test_caseid_1988899(self): 
        info = ["HmiSeatClimaHmiSeatHeatgForRowFirstLe","HmiSeatClimaHmiSeatHeatgForRowFirstRi","HmiSeatClimaHmiSeatHeatgForRowSecLe","HmiSeatClimaHmiSeatHeatgForRowSecRi"]
        value = [[0,1,0,1,0,1],[1,2,1,2,1,2],[2,3,2,3,2,3],[3,0,3,0,3,0]]
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [2, 11, 13]:
            self.sd_tester.change_usage_mode(mode)
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                    {"params": [{"id": 0, "uint8Info": 0},{"id": 1, "uint8Info": 1},
                                                                {"id": 4, "uint8Info": 2},{"id": 6, "uint8Info": 3}]},timeout = 0.5)
            sleep(0.5)
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                    {"params": [{"id": 0, "uint8Info": 2},{"id": 1, "uint8Info": 3},
                                                                {"id": 4, "uint8Info": 0},{"id": 6, "uint8Info": 1}]})
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                    {"params": [{"id": 0, "uint8Info": 1},{"id": 1, "uint8Info": 2},
                                                                {"id": 4, "uint8Info": 3},{"id": 6, "uint8Info": 0}]})
            sleep(1)
        sleep(2)  
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()       
        for i in range(4):
            self.bgm_eth_inter.ck_ordered_array(info[i], value[i])
            self.bgm_eth_inter.ck_period_time(info[i],period=0.5)
    
    @allure.title("本地座椅加热_信号下发取消插帧_加热状态信号从4到2触发下发&接口调用触发下发")
    @pytest.mark.full
    def test_caseid_1988900(self): 
        info = ["HmiSeatClimaHmiSeatHeatgForRowFirstLe","HmiSeatClimaHmiSeatHeatgForRowFirstRi","HmiSeatClimaHmiSeatHeatgForRowSecLe","HmiSeatClimaHmiSeatHeatgForRowSecRi"]
        value = [[0],[1,0,1,0,1,0],[2,0,2,0,2,0],[3,0,3,0,3,0]]
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [2]:
            self.sd_tester.change_usage_mode(mode)
            self.setHeatVentingStatus(4,0)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgAvlSts',4)
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                    {"params": [{"id": 0, "uint8Info": 0},{"id": 1, "uint8Info": 1},
                                                                {"id": 4, "uint8Info": 2},{"id": 6, "uint8Info": 3}]},timeout = 0.5)
            sleep(1)
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                    {"params": [{"id": 0, "uint8Info": 2},{"id": 1, "uint8Info": 3},
                                                                {"id": 4, "uint8Info": 0},{"id": 6, "uint8Info": 1}]})
            self.setHeatVentingStatus(2,0)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgAvlSts',2)
            sleep(1)
        sleep(2)  
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()       
        for i in range(1):
            #无法保证下发的值是否在一个周期内，此处重点检验周期
            # self.bgm_eth_inter.ck_ordered_array(info[i], value[i])
            self.bgm_eth_inter.ck_period_time(info[i],period=0.5)
            
    @allure.title("本地座椅加热_信号下发取消插帧_UsageMode下切触发下发")
    @pytest.mark.full
    def test_caseid_1988912(self): 
        info = ["HmiSeatClimaHmiSeatHeatgForRowFirstLe","HmiSeatClimaHmiSeatHeatgForRowFirstRi","HmiSeatClimaHmiSeatHeatgForRowSecLe","HmiSeatClimaHmiSeatHeatgForRowSecRi"]
        value = [[0],[1,0,1,0,1,0,1,0,1,0,1,0],[2,0,2,0,2,0,2,0,2,0,2,0],[3,0,3,0,3,0,3,0,3,0,3,0]]
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode1 in [2, 11, 13]:
            for mode2 in [0,1]:
                self.sd_tester.change_usage_mode(mode1)
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                        {"params": [{"id": 0, "uint8Info": 0},{"id": 1, "uint8Info": 1},
                                                                    {"id": 4, "uint8Info": 2},{"id": 6, "uint8Info": 3}]},timeout = 0.5)
                sleep(0.5)
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                        {"params": [{"id": 0, "uint8Info": 2},{"id": 1, "uint8Info": 3},
                                                                    {"id": 4, "uint8Info": 0},{"id": 6, "uint8Info": 1}]})
                self.sd_tester.change_usage_mode(mode2)
                sleep(1)
        sleep(2)  
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()       
        for i in range(4):
            # self.bgm_eth_inter.ck_ordered_array(info[i], value[i])
            self.bgm_eth_inter.ck_period_time(info[i],period=0.5)
            
    @allure.title("本地座椅通风_信号下发取消插帧_接口调用触发下发")
    @pytest.mark.sanity
    def test_caseid_1988901(self): 
        info = ["HmiSeatClimaHmiSeatVentnForRowFirstLe","HmiSeatClimaHmiSeatVentnForRowFirstRi","HmiSeatClimaHmiSeatVentnForRowSecLe","HmiSeatClimaHmiSeatVentnForRowSecRi"]
        value = [[0,1,0,1,0,1],[1,2,1,2,1,2],[2,3,2,3,2,3],[3,0,3,0,3,0]]
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [2, 11, 13]:
            self.sd_tester.change_usage_mode(mode)
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                    {"params": [{"id": 0, "uint8Info": 0},{"id": 1, "uint8Info": 1},
                                                                {"id": 4, "uint8Info": 2},{"id": 6, "uint8Info": 3}]},timeout = 0.5)
            sleep(0.5)
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                    {"params": [{"id": 0, "uint8Info": 2},{"id": 1, "uint8Info": 3},
                                                                {"id": 4, "uint8Info": 0},{"id": 6, "uint8Info": 1}]})
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                    {"params": [{"id": 0, "uint8Info": 1},{"id": 1, "uint8Info": 2},
                                                                {"id": 4, "uint8Info": 3},{"id": 6, "uint8Info": 0}]})
            sleep(1)
        sleep(2)  
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()       
        for i in range(4):
            self.bgm_eth_inter.ck_ordered_array(info[i], value[i])
            self.bgm_eth_inter.ck_period_time(info[i],period=0.5)
    
    @allure.title("本地座椅通风_信号下发取消插帧_通风状态信号从4到2触发下发&接口调用触发下发")
    @pytest.mark.full
    def test_caseid_1988902(self): 
        info = ["HmiSeatClimaHmiSeatVentnForRowFirstLe","HmiSeatClimaHmiSeatVentnForRowFirstRi","HmiSeatClimaHmiSeatVentnForRowSecLe","HmiSeatClimaHmiSeatVentnForRowSecRi"]
        value = [[0],[1,0,1,0,1,0],[2,0,2,0,2,0],[3,0,3,0,3,0]]
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode in [2, 11, 13]:
            self.sd_tester.change_usage_mode(mode)
            self.setHeatVentingStatus(0,4)
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                    {"params": [{"id": 0, "uint8Info": 0},{"id": 1, "uint8Info": 1},
                                                                {"id": 4, "uint8Info": 2},{"id": 6, "uint8Info": 3}]},timeout = 0.5)
            sleep(0.7)
            self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                    {"params": [{"id": 0, "uint8Info": 2},{"id": 1, "uint8Info": 3},
                                                                {"id": 4, "uint8Info": 0},{"id": 6, "uint8Info": 1}]})
            self.setHeatVentingStatus(0,2)
            sleep(1)
        sleep(2)  
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()       
        for i in range(4):
            # self.bgm_eth_inter.ck_ordered_array(info[i], value[i])
            self.bgm_eth_inter.ck_period_time(info[i],period=0.5)
            
    @allure.title("本地座椅通风_信号下发取消插帧_UsageMode下切触发下发")
    @pytest.mark.full
    def test_caseid_1988913(self): 
        info = ["HmiSeatClimaHmiSeatVentnForRowFirstLe","HmiSeatClimaHmiSeatVentnForRowFirstRi","HmiSeatClimaHmiSeatVentnForRowSecLe","HmiSeatClimaHmiSeatVentnForRowSecRi"]
        value = [[0],[1,0,1,0,1,0,1,0,1,0,1,0],[2,0,2,0,2,0,2,0,2,0,2,0],[3,0,3,0,3,0,3,0,3,0,3,0]]
        self.bgm_eth_inter.start_bgm_tcpdump()
        for mode1 in [2, 11, 13]:
            for mode2 in [0,1]:
                self.sd_tester.change_usage_mode(mode1)
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                        {"params": [{"id": 0, "uint8Info": 0},{"id": 1, "uint8Info": 1},
                                                                    {"id": 4, "uint8Info": 2},{"id": 6, "uint8Info": 3}]},timeout = 0.5)
                sleep(0.5)
                self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                        {"params": [{"id": 0, "uint8Info": 2},{"id": 1, "uint8Info": 3},
                                                                    {"id": 4, "uint8Info": 0},{"id": 6, "uint8Info": 1}]})
                self.sd_tester.change_usage_mode(mode2)
                sleep(1)
        sleep(2)  
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()       
        for i in range(4):
            # self.bgm_eth_inter.ck_ordered_array(info[i], value[i])
            self.bgm_eth_inter.ck_period_time(info[i],period=0.5)
            
    @allure.title("远程座椅加热_信号下发取消插帧_接口调用触发下发")
    @pytest.mark.sanity
    def test_caseid_1988904(self): 
        info = ["TelmSeatDrvHeatClimaLvlSP","TelmSeatPassHeatClimaLvlSP","TelmSeatSecLeHeatClimaLvl","TelmSeatSecRiHeatClimaLvl"]
        value = [[0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,3,3,3,3,3],[3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,0,0,0,0,0]]
        self.bgm_eth_inter.start_bgm_tcpdump()
        
        self.sd_tester.change_usage_mode(0)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                {"params": [{"id": 0, "uint8Info": 0},{"id": 1, "uint8Info": 1},
                                                            {"id": 4, "uint8Info": 2},{"id": 6, "uint8Info": 3}]},timeout = 0.5)
        #周期内设置相同值不下发
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                {"params": [{"id": 0, "uint8Info": 0},{"id": 1, "uint8Info": 1},
                                                            {"id": 4, "uint8Info": 2},{"id": 6, "uint8Info": 3}]})
        #周期外设置相同值下发
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                {"params": [{"id": 0, "uint8Info": 0},{"id": 1, "uint8Info": 1},
                                                            {"id": 4, "uint8Info": 2},{"id": 6, "uint8Info": 3}]})
        sleep(1)
        #如果设置主驾座椅加热挡位为1的时候，500ms计时器是处于超时状态，会先发1并重置500ms计时器，500ms计时器超时后再发2；
        #否则只会发2
        #本次会下发
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                {"params": [{"id": 0, "uint8Info": 2},{"id": 1, "uint8Info": 3},
                                                            {"id": 4, "uint8Info": 0},{"id": 6, "uint8Info": 1}]})
        #本次不会下发
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                {"params": [{"id": 0, "uint8Info": 0},{"id": 1, "uint8Info": 1},
                                                            {"id": 4, "uint8Info": 2},{"id": 6, "uint8Info": 3}]})
        #本次会下发
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                {"params": [{"id": 0, "uint8Info": 1},{"id": 1, "uint8Info": 2},
                                                            {"id": 4, "uint8Info": 3},{"id": 6, "uint8Info": 0}]})
        sleep(2)  
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()       
        for i in range(4):
            self.bgm_eth_inter.ck_signal_values(info[i], value[i])
            self.bgm_eth_inter.ck_period_time(info[i], period=0.1, permit_fail_times=3, deviation=0.5)
           
    @allure.title("远程座椅加热_信号下发取消插帧_加热等级状态信号从其他值跳变为0触发下发")
    @pytest.mark.full
    def test_caseid_1988905(self): 
        info = ["TelmSeatDrvHeatClimaLvlSP","TelmSeatPassHeatClimaLvlSP","TelmSeatSecLeHeatClimaLvl","TelmSeatSecRiHeatClimaLvl"]
        value = [[0,0,0,0,0,2,2,2,2,2,0,0,0,0,0],[1,1,1,1,1,3,3,3,3,3,0,0,0,0,0],[2,2,2,2,2,0,0,0,0,0],[3,3,3,3,3,1,1,1,1,1,0,0,0,0,0]]
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.change_usage_mode(1)
        self.setSeatHeatLevel(1,2,3,1)
        sleep(0.5)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                {"params": [{"id": 0, "uint8Info": 0},{"id": 1, "uint8Info": 1},
                                                            {"id": 4, "uint8Info": 2},{"id": 6, "uint8Info": 3}]},timeout = 0.5)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                {"params": [{"id": 0, "uint8Info": 2},{"id": 1, "uint8Info": 3},
                                                            {"id": 4, "uint8Info": 0},{"id": 6, "uint8Info": 1}]})
        sleep(0.05)
        #当监测到主驾座椅加热等级状态信号DrvrSeatHeatgLvlSts值从其他值跳变为0（OFF）时（此场景下：信号TelmSeatDrvHeatClimaLvlSP=0）
        self.setSeatHeatLevel(0,0,0,0)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()       
        for i in range(4):
            self.bgm_eth_inter.ck_signal_values(info[i], value[i])
            self.bgm_eth_inter.ck_period_time(info[i], period=0.1, permit_fail_times=2)
            
    @allure.title("远程座椅加热_信号下发取消插帧_加热等级状态信号从其他值跳变为0触发下发")
    @pytest.mark.full
    def test_caseid_1988906(self): 
        info = ["TelmSeatDrvHeatClimaLvlSP","TelmSeatPassHeatClimaLvlSP","TelmSeatSecLeHeatClimaLvl","TelmSeatSecRiHeatClimaLvl"]
        value = [[0,0,0,0,0],[1,1,1,1,1,0,0,0,0,0],[2,2,2,2,2,0,0,0,0,0],[3,3,3,3,3,0,0,0,0,0]]
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.change_usage_mode(1)

        self.setHeatVentingStatus(4,0)
        sleep(0.5)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                {"params": [{"id": 0, "uint8Info": 0},{"id": 1, "uint8Info": 1},
                                                            {"id": 4, "uint8Info": 2},{"id": 6, "uint8Info": 3}]},timeout = 0.5)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                {"params": [{"id": 0, "uint8Info": 2},{"id": 1, "uint8Info": 3},
                                                            {"id": 4, "uint8Info": 0},{"id": 6, "uint8Info": 1}]})
        sleep(0.05) #不等会导致 下面设置的信号2比SetHeatingLevel快
        self.setHeatVentingStatus(2,0)
        sleep(2)  
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()       
        for i in range(4):
            self.bgm_eth_inter.ck_signal_values(info[i], value[i])
            self.bgm_eth_inter.ck_period_time(info[i], period=0.1, permit_fail_times=1)
            
    @allure.title("远程座椅加热_信号下发取消插帧_调用座椅通风接口触发下发")
    @pytest.mark.full
    def test_caseid_1988907(self): 
        info = ["TelmSeatDrvHeatClimaLvlSP","TelmSeatPassHeatClimaLvlSP","TelmSeatSecLeHeatClimaLvl","TelmSeatSecRiHeatClimaLvl"]
        value = [[0,0,0,0,0,2,2,2,2,2],[1,1,1,1,1,0,0,0,0,0],[2,2,2,2,2,0,0,0,0,0],[3,3,3,3,3,0,0,0,0,0]]
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                {"params": [{"id": 0, "uint8Info": 0},{"id": 1, "uint8Info": 1},
                                                            {"id": 4, "uint8Info": 2},{"id": 6, "uint8Info": 3}]},timeout = 0.5)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                {"params": [{"id": 0, "uint8Info": 2},{"id": 1, "uint8Info": 3},
                                                            {"id": 4, "uint8Info": 0},{"id": 6, "uint8Info": 1}]})
        #通风设置0的时候 不会打断加热，通风设置非0，会打断加热 ，加热下发0
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                {"params": [{"id": 0, "uint8Info": 0},{"id": 1, "uint8Info": 1},
                                                            {"id": 4, "uint8Info": 2},{"id": 6, "uint8Info": 3}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()       
        for i in range(4):
            self.bgm_eth_inter.ck_signal_values(info[i], value[i])
            self.bgm_eth_inter.ck_period_time(info[i], period=0.1, permit_fail_times=1)
            
    @allure.title("远程座椅通风_信号下发取消插帧_接口调用触发下发")
    @pytest.mark.full
    def test_caseid_1988908(self): 
        info = ["TelmSeatDrvVentnClimaLvl","TelmSeatPassVentnClimaLvl","TelmSeatSecLeVentnClimaLvl","TelmSeatSecRiVentnClimaLvl"]
        value = [[0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,3,3,3,3,3],[3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,0,0,0,0,0]]
        self.bgm_eth_inter.start_bgm_tcpdump()
        
        self.sd_tester.change_usage_mode(0)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                {"params": [{"id": 0, "uint8Info": 0},{"id": 1, "uint8Info": 1},
                                                            {"id": 4, "uint8Info": 2},{"id": 6, "uint8Info": 3}]},timeout = 0.5)
        #周期内设置相同值不下发
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                {"params": [{"id": 0, "uint8Info": 0},{"id": 1, "uint8Info": 1},
                                                            {"id": 4, "uint8Info": 2},{"id": 6, "uint8Info": 3}]})
        #周期外设置相同值下发
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                {"params": [{"id": 0, "uint8Info": 0},{"id": 1, "uint8Info": 1},
                                                            {"id": 4, "uint8Info": 2},{"id": 6, "uint8Info": 3}]})
        sleep(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                {"params": [{"id": 0, "uint8Info": 2},{"id": 1, "uint8Info": 3},
                                                            {"id": 4, "uint8Info": 0},{"id": 6, "uint8Info": 1}]})
        #本次不会下发
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                {"params": [{"id": 0, "uint8Info": 0},{"id": 1, "uint8Info": 1},
                                                            {"id": 4, "uint8Info": 2},{"id": 6, "uint8Info": 3}]})
        #本次会下发
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                {"params": [{"id": 0, "uint8Info": 1},{"id": 1, "uint8Info": 2},
                                                            {"id": 4, "uint8Info": 3},{"id": 6, "uint8Info": 0}]})
        sleep(2)  
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()       
        for i in range(4):
            self.bgm_eth_inter.ck_signal_values(info[i], value[i])
            self.bgm_eth_inter.ck_period_time(info[i], period=0.1, permit_fail_times=3, deviation=0.5)
           
    @allure.title("远程座椅通风_信号下发取消插帧_通风等级状态信号从其他值跳变为0触发下发")
    @pytest.mark.full
    def test_caseid_1988909(self): 
        info = ["TelmSeatDrvVentnClimaLvl","TelmSeatPassVentnClimaLvl","TelmSeatSecLeVentnClimaLvl","TelmSeatSecRiVentnClimaLvl"]
        value = [[0,0,0,0,0,2,2,2,2,2],[1,1,1,1,1,3,3,3,3,3],[2,2,2,2,2,0,0,0,0,0],[3,3,3,3,3,1,1,1,1,1]]
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.change_usage_mode(1)
        self.setSeatHeatLevel(1,2,3,1)
        sleep(0.5)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                {"params": [{"id": 0, "uint8Info": 0},{"id": 1, "uint8Info": 1},
                                                            {"id": 4, "uint8Info": 2},{"id": 6, "uint8Info": 3}]},timeout = 0.5)
        sleep(0.05)
        self.setSeatHeatLevel(0,0,0,0)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                {"params": [{"id": 0, "uint8Info": 2},{"id": 1, "uint8Info": 3},
                                                            {"id": 4, "uint8Info": 0},{"id": 6, "uint8Info": 1}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()       
        for i in range(4):
            self.bgm_eth_inter.ck_signal_values(info[i], value[i])
            self.bgm_eth_inter.ck_period_time(info[i], period=0.1, permit_fail_times=2)
            
    @allure.title("远程座椅通风_信号下发取消插帧_通风状态信号从4跳变为2触发下发")
    @pytest.mark.full
    def test_caseid_1988910(self): 
        info = ["TelmSeatDrvVentnClimaLvl","TelmSeatPassVentnClimaLvl","TelmSeatSecLeVentnClimaLvl","TelmSeatSecRiVentnClimaLvl"]
        value = [[0,0,0,0,0,2,2,2,2,2],[1,1,1,1,1,3,3,3,3,3],[2,2,2,2,2,0,0,0,0,0],[3,3,3,3,3,1,1,1,1,1]]
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.change_usage_mode(1)
        self.setHeatVentingStatus(4,0)
        sleep(0.5)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                {"params": [{"id": 0, "uint8Info": 0},{"id": 1, "uint8Info": 1},
                                                            {"id": 4, "uint8Info": 2},{"id": 6, "uint8Info": 3}]})
        sleep(0.05) 
        self.setHeatVentingStatus(2,0)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                {"params": [{"id": 0, "uint8Info": 2},{"id": 1, "uint8Info": 3},
                                                            {"id": 4, "uint8Info": 0},{"id": 6, "uint8Info": 1}]})
        sleep(2)  
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()       
        for i in range(4):
            self.bgm_eth_inter.ck_signal_values(info[i], value[i])
            self.bgm_eth_inter.ck_period_time(info[i], period=0.1, permit_fail_times=1)
          
    @allure.title("远程座椅通风_信号下发取消插帧_调用座椅加热接口触发下发")
    @pytest.mark.full
    def test_caseid_1988911(self): 
        info = ["TelmSeatDrvVentnClimaLvl","TelmSeatPassVentnClimaLvl","TelmSeatSecLeVentnClimaLvl","TelmSeatSecRiVentnClimaLvl"]
        value = [[0,0,0,0,0,1,1,1,1,1],[1,1,1,1,1,2,2,2,2,2],[2,2,2,2,2,3,3,3,3,3],[3,3,3,3,3,0,0,0,0,0]]
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                {"params": [{"id": 0, "uint8Info": 0},{"id": 1, "uint8Info": 1},
                                                            {"id": 4, "uint8Info": 2},{"id": 6, "uint8Info": 3}]})
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetHeatingLevel',
                                                {"params": [{"id": 0, "uint8Info": 2},{"id": 1, "uint8Info": 3},
                                                            {"id": 4, "uint8Info": 0},{"id": 6, "uint8Info": 1}]})
        
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'SetVentingLevel',
                                                {"params": [{"id": 0, "uint8Info": 1},{"id": 1, "uint8Info": 2},
                                                            {"id": 4, "uint8Info": 3},{"id": 6, "uint8Info": 0}]})
        sleep(2)
        #远程没有覆盖一说，第一次一定能发，只有在500ms内的中间一次会被覆盖，二排右的3能发下来
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()       
        for i in range(4):
            self.bgm_eth_inter.ck_signal_values(info[i], value[i])
            self.bgm_eth_inter.ck_period_time(info[i], period=0.1, permit_fail_times=1)
            
    @allure.title("主驾位置信息_QF有效_无效_有效")
    @pytest.mark.full
    def test_caseid_1989150(self):
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiPerc', 100)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldPerc', 200)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiPerc', 300)
              
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo",{"seats":[0]},#位置信息
                                              {"out": [{"id": 0, "position": {"longitudinalPosition": 20,"verticalPosition": 30,"LegrestVerticalPosition": 10,
                                            "longitudinalIsValid": 1,  "verticalIsValid": 1,"legrestVerticalIsValid": 1}},
                                             ]})
        
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiPerc', 200)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldPerc', 300)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiPerc', 100)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatPosition",
                                             {"position":{"longitudinalPosition":20,"verticalPosition":30,"LegrestVerticalPosition":10,"longitudinalIsValid":0,"verticalIsValid":0,"legrestVerticalIsValid":0}})
        
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', 3)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntLeftSeatPosition",
                                             {"position":{"longitudinalPosition":30,"verticalPosition":10,"LegrestVerticalPosition":20,"longitudinalIsValid":1,"verticalIsValid":1,"legrestVerticalIsValid":1}})
        
    @allure.title("副位置信息_QF有效_无效_有效")
    @pytest.mark.full
    def test_caseid_1989151(self):
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiPerc',  100)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldPerc',  200)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiPerc', 300)
        
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatPositionInfo",{"seats":[1]},#位置信息
                                              {"out": [{"id": 1, "position": {"longitudinalPosition": 20,"verticalPosition": 30,"LegrestVerticalPosition": 10,
                                            "longitudinalIsValid": 1,  "verticalIsValid": 1,"legrestVerticalIsValid": 1}},
                                             ]})
        
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiQF', 0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldQF', 0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiQF', 0)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiPerc',  200)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldPerc',  300)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiPerc', 100)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatPosition",
                                             {"position":{"longitudinalPosition":20,"verticalPosition":30,"LegrestVerticalPosition":10,"longitudinalIsValid":0,"verticalIsValid":0,"legrestVerticalIsValid":0}})
        
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosSldQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr02, 'PassSeatPosPercSeatPosFrntHeiQF', 3)
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "FrntRightSeatPosition",
                                             {"position":{"longitudinalPosition":30,"verticalPosition":10,"LegrestVerticalPosition":20,"longitudinalIsValid":1,"verticalIsValid":1,"legrestVerticalIsValid":1}})
        
    @allure.title("主驾座椅姿态设置_座椅高度差值范围内_Mars")
    @pytest.mark.sanity
    def test_caseid_1989554(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Drvrseat_condition_allow()
        vertical_list = [8, 7.9 ,12, 12.1]
        for i in range(4):
            self.set_drvr_position(10.0, 10.0 ,120, 10.0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                        {"params": {"id": 0,"position": {"backAngle": 120, "longitudinalPosition": 10,"verticalPosition": vertical_list[i],
                        "LegrestVerticalPosition": 10,"backAngleIsValid": True,
                        "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}},{"out": 1})
            if i == 0 or i == 2:
                sleep(1)
                self.check_Drvrseat_direction_not_send() 
            elif i == 1:
                self.check_drvrseat_adjust(0,0,0,2)
                self.set_drvr_position(10.0, 10.0 ,120, 7.9)
            else:
                self.check_drvrseat_adjust(0,0,0,1)
                self.set_drvr_position(10.0, 10.0 ,120, 12.1)
                
    @allure.title("主驾座椅姿态设置_座椅靠背角度差值范围内_Mars")
    @pytest.mark.full
    def test_caseid_1989559(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Drvrseat_condition_allow()
        backAngle_list = [119, 118 ,121, 122]
        for i in range(4):
            self.set_drvr_position(10.0, 10.0 ,120, 10.0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                        {"params": {"id": 0,"position": {"backAngle": backAngle_list[i], "longitudinalPosition": 10,"verticalPosition": 10,
                        "LegrestVerticalPosition": 10,"backAngleIsValid": True,
                        "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}},{"out": 1})
            if i == 0 or i == 2:
                sleep(1)
                self.check_Drvrseat_direction_not_send() 
            elif i == 1:
                self.check_drvrseat_adjust(0,1,0,0)
                self.set_drvr_position(10.0, 10.0 ,118, 10.0)
            else:
                self.check_drvrseat_adjust(0,2,0,0)
                self.set_drvr_position(10.0, 10.0 ,122, 10.0)
    
    @allure.title("主驾座椅姿态设置_座椅前后位置差值范围内_Mars")
    @pytest.mark.full
    def test_caseid_1989560(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Drvrseat_condition_allow()
        longitudinal_list = [8, 7.9 ,12, 12.1]
        for i in range(4):
            self.set_drvr_position(10.0, 10.0 ,120, 10.0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                        {"params": {"id": 0,"position": {"backAngle": 120, "longitudinalPosition": longitudinal_list[i],"verticalPosition": 10,
                        "LegrestVerticalPosition": 10,"backAngleIsValid": True,
                        "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}},{"out": 1})
            if i == 0 or i == 2:
                sleep(1)
                self.check_Drvrseat_direction_not_send() 
            elif i == 1:
                self.check_drvrseat_adjust(2,0,0,0)
                self.set_drvr_position(10.0, 7.9 ,120, 10.0)
            else:
                self.check_drvrseat_adjust(1,0,0,0)
                self.set_drvr_position(10.0, 12.1 ,120, 10.0)     
                
    @allure.title("主驾座椅姿态设置_座椅坐垫高度位置差值范围内_Mars")
    @pytest.mark.full
    def test_caseid_1989561(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Drvrseat_condition_allow()
        LegrestVertical_list = [7, 6.9 ,13, 13.1]
        for i in range(4):
            self.set_drvr_position(10.0, 10.0 ,120, 10.0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                        {"params": {"id": 0,"position": {"backAngle": 120, "longitudinalPosition": 10,"verticalPosition": 10,
                        "LegrestVerticalPosition": LegrestVertical_list[i],"backAngleIsValid": True,
                        "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}},{"out": 1})
            if i == 0 or i == 2:
                sleep(1)
                self.check_Drvrseat_direction_not_send() 
            elif i == 1:
                self.check_drvrseat_adjust(0,0,2,0)
                self.set_drvr_position(6.9, 10.0 ,120, 10.0)
            else:
                self.check_drvrseat_adjust(0,0,1,0)
                self.set_drvr_position(13.1, 10.0 ,120, 10.0)            
    
    @allure.title("主驾座椅姿态设置_座椅高度差值范围内_Venus")
    @pytest.mark.sanity
    def test_caseid_1989562(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.set_Drvrseat_condition_allow()
        vertical_list = [8, 7.9 ,12, 12.1]
        for i in range(4):
            self.set_drvr_position(10.0, 10.0 ,120, 10.0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                        {"params": {"id": 0,"position": {"backAngle": 120, "longitudinalPosition": 10,"verticalPosition": vertical_list[i],
                        "LegrestVerticalPosition": 10,"backAngleIsValid": True,
                        "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}},{"out": 1})
            if i == 0 or i == 2:
                sleep(1)
                self.check_Drvrseat_direction_not_send() 
            elif i == 1:
                self.check_drvrseat_adjust(0,0,0,2)
                self.set_drvr_position(10.0, 10.0 ,120, 7.9)
            else:
                self.check_drvrseat_adjust(0,0,0,1)
                self.set_drvr_position(10.0, 10.0 ,120, 12.1)
                
    @allure.title("主驾座椅姿态设置_座椅前后位置差值范围内_Venus")
    @pytest.mark.full
    def test_caseid_1989563(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.set_Drvrseat_condition_allow()
        backAngle_list = [119, 118 ,121, 122]
        for i in range(4):
            self.set_drvr_position(10.0, 10.0 ,120, 10.0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                        {"params": {"id": 0,"position": {"backAngle": backAngle_list[i], "longitudinalPosition": 10,"verticalPosition": 10,
                        "LegrestVerticalPosition": 10,"backAngleIsValid": True,
                        "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}},{"out": 1})
            if i == 0 or i == 2:
                sleep(1)
                self.check_Drvrseat_direction_not_send() 
            elif i == 1:
                self.check_drvrseat_adjust(0,1,0,0)
                self.set_drvr_position(10.0, 10.0 ,118, 10.0)
            else:
                self.check_drvrseat_adjust(0,2,0,0)
                self.set_drvr_position(10.0, 10.0 ,122, 10.0)
    
    @allure.title("主驾座椅姿态设置_座椅前后位置差值范围内_Venus")
    @pytest.mark.full
    def test_caseid_1989564(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.set_Drvrseat_condition_allow()
        longitudinal_list = [8, 7.9 ,12, 12.1]
        for i in range(4):
            self.set_drvr_position(10.0, 10.0 ,120, 10.0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                        {"params": {"id": 0,"position": {"backAngle": 120, "longitudinalPosition": longitudinal_list[i],"verticalPosition": 10,
                        "LegrestVerticalPosition": 10,"backAngleIsValid": True,
                        "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}},{"out": 1})
            if i == 0 or i == 2:
                sleep(1)
                self.check_Drvrseat_direction_not_send() 
            elif i == 1:
                self.check_drvrseat_adjust(2,0,0,0)
                self.set_drvr_position(10.0, 7.9 ,120, 10.0)
            else:
                self.check_drvrseat_adjust(1,0,0,0)
                self.set_drvr_position(10.0, 12.1 ,120, 10.0)     
                
    @allure.title("主驾座椅姿态设置_座椅坐垫高度位置差值范围内_Venus")
    @pytest.mark.full
    def test_caseid_1989565(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.set_Drvrseat_condition_allow()
        LegrestVertical_list = [6, 5.9 ,14, 14.1]
        for i in range(4):
            self.set_drvr_position(10.0, 10.0 ,120, 10.0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                        {"params": {"id": 0,"position": {"backAngle": 120, "longitudinalPosition": 10,"verticalPosition": 10,
                        "LegrestVerticalPosition": LegrestVertical_list[i],"backAngleIsValid": True,
                        "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}},{"out": 1})
            if i == 0 or i == 2:
                sleep(1)
                self.check_Drvrseat_direction_not_send() 
            elif i == 1:
                self.check_drvrseat_adjust(0,0,2,0)
                self.set_drvr_position(5.9, 10.0 ,120, 10.0)
            else:
                self.check_drvrseat_adjust(0,0,1,0)
                self.set_drvr_position(14.1, 10.0 ,120, 10.0)              
                  
    @allure.title("副驾座椅姿态设置_座椅高度差值范围内_Mars")
    @pytest.mark.sanity
    def test_caseid_1989566(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Passseat_condition_allow()
        vertical_list = [8, 7.9 ,12, 12.1]
        for i in range(4):
            self.set_Pass_position(10.0, 10.0 ,120, 10.0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                        {"params": {"id": 1,"position": {"backAngle": 120, "longitudinalPosition": 10,"verticalPosition": vertical_list[i],
                        "LegrestVerticalPosition": 10,"backAngleIsValid": True,
                        "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}},{"out": 1})
            if i == 0 or i == 2:
                sleep(1)
                self.check_Passseat_direction_not_send() 
            elif i == 1:
                self.check_Passseat_adjust(0,0,0,2)
                self.set_Pass_position(10.0, 10.0 ,120, 7.9)
            else:
                self.check_Passseat_adjust(0,0,0,1)
                self.set_Pass_position(10.0, 10.0 ,120, 12.1)
                
    @allure.title("副驾座椅姿态设置_座椅靠背角度差值范围内_Mars")
    @pytest.mark.full
    def test_caseid_1989568(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Passseat_condition_allow()
        backAngle_list = [119, 118 ,121, 122]
        for i in range(4):
            self.set_Pass_position(10.0, 10.0 ,120, 10.0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                        {"params": {"id": 1,"position": {"backAngle": backAngle_list[i], "longitudinalPosition": 10,"verticalPosition": 10,
                        "LegrestVerticalPosition": 10,"backAngleIsValid": True,
                        "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}},{"out": 1})
            if i == 0 or i == 2:
                sleep(1)
                self.check_Passseat_direction_not_send() 
            elif i == 1:
                self.check_Passseat_adjust(0,1,0,0)
                self.set_Pass_position(10.0, 10.0 ,118, 10.0)
            else:
                self.check_Passseat_adjust(0,2,0,0)
                self.set_Pass_position(10.0, 10.0 ,122, 10.0)
    
    @allure.title("副驾座椅姿态设置_座椅前后位置差值范围内_Mars")
    @pytest.mark.full
    def test_caseid_1989567(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Passseat_condition_allow()
        longitudinal_list = [8, 7.9 ,12, 12.1]
        for i in range(4):
            self.set_Pass_position(10.0, 10.0 ,120, 10.0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                        {"params": {"id": 1,"position": {"backAngle": 120, "longitudinalPosition": longitudinal_list[i],"verticalPosition": 10,
                        "LegrestVerticalPosition": 10,"backAngleIsValid": True,
                        "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}},{"out": 1})
            if i == 0 or i == 2:
                sleep(1)
                self.check_Passseat_direction_not_send() 
            elif i == 1:
                self.check_Passseat_adjust(2,0,0,0)
                self.set_Pass_position(10.0, 7.9 ,120, 10.0)
            else:
                self.check_Passseat_adjust(1,0,0,0)
                self.set_Pass_position(10.0, 12.1 ,120, 10.0)     
                
    @allure.title("副驾座椅姿态设置_座椅坐垫高度位置差值范围内_Mars")
    @pytest.mark.full
    def test_caseid_1989569(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Passseat_condition_allow()
        LegrestVertical_list = [7, 6.9 ,13, 13.1]
        for i in range(4):
            self.set_Pass_position(10.0, 10.0 ,120, 10.0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                        {"params": {"id": 1,"position": {"backAngle": 120, "longitudinalPosition": 10,"verticalPosition": 10,
                        "LegrestVerticalPosition": LegrestVertical_list[i],"backAngleIsValid": True,
                        "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}},{"out": 1})
            if i == 0 or i == 2:
                sleep(1)
                self.check_Passseat_direction_not_send() 
            elif i == 1:
                self.check_Passseat_adjust(0,0,2,0)
                self.set_Pass_position(6.9, 10.0 ,120, 10.0)
            else:
                self.check_Passseat_adjust(0,0,1,0)
                self.set_Pass_position(13.1, 10.0 ,120, 10.0)            
    
    @allure.title("副驾座椅姿态设置_座椅高度差值范围内_Venus")
    @pytest.mark.sanity
    def test_caseid_1989570(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.set_Passseat_condition_allow()
        vertical_list = [8, 7.9 ,12, 12.1]
        for i in range(4):
            self.set_Pass_position(10.0, 10.0 ,120, 10.0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                        {"params": {"id": 1,"position": {"backAngle": 120, "longitudinalPosition": 10,"verticalPosition": vertical_list[i],
                        "LegrestVerticalPosition": 10,"backAngleIsValid": True,
                        "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}},{"out": 1})
            if i == 0 or i == 2:
                sleep(1)
                self.check_Passseat_direction_not_send() 
            elif i == 1:
                self.check_Passseat_adjust(0,0,0,2)
                self.set_Pass_position(10.0, 10.0 ,120, 7.9)
            else:
                self.check_Passseat_adjust(0,0,0,1)
                self.set_Pass_position(10.0, 10.0 ,120, 12.1)
                
    @allure.title("副驾座椅姿态设置_座椅靠背角度差值范围内_Venus")
    @pytest.mark.full
    def test_caseid_1989571(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.set_Passseat_condition_allow()
        backAngle_list = [119, 118 ,121, 122]
        for i in range(4):
            self.set_Pass_position(10.0, 10.0 ,120, 10.0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                        {"params": {"id": 1,"position": {"backAngle": backAngle_list[i], "longitudinalPosition": 10,"verticalPosition": 10,
                        "LegrestVerticalPosition": 10,"backAngleIsValid": True,
                        "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}},{"out": 1})
            if i == 0 or i == 2:
                sleep(1)
                self.check_Passseat_direction_not_send() 
            elif i == 1:
                self.check_Passseat_adjust(0,1,0,0)
                self.set_Pass_position(10.0, 10.0 ,118, 10.0)
            else:
                self.check_Passseat_adjust(0,2,0,0)
                self.set_Pass_position(10.0, 10.0 ,122, 10.0)
    
    @allure.title("副驾座椅姿态设置_座椅前后位置差值范围内_Venus")
    @pytest.mark.full
    def test_caseid_1989572(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.set_Passseat_condition_allow()
        longitudinal_list = [8, 7.9 ,12, 12.1]
        for i in range(4):
            self.set_Pass_position(10.0, 10.0 ,120, 10.0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                        {"params": {"id": 1,"position": {"backAngle": 120, "longitudinalPosition": longitudinal_list[i],"verticalPosition": 10,
                        "LegrestVerticalPosition": 10,"backAngleIsValid": True,
                        "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}},{"out": 1})
            if i == 0 or i == 2:
                sleep(1)
                self.check_Passseat_direction_not_send() 
            elif i == 1:
                self.check_Passseat_adjust(2,0,0,0)
                self.set_Pass_position(10.0, 7.9 ,120, 10.0)
            else:
                self.check_Passseat_adjust(1,0,0,0)
                self.set_Pass_position(10.0, 12.1 ,120, 10.0)     
                
    @allure.title("副驾座椅姿态设置_座椅坐垫高度位置差值范围内_Venus")
    @pytest.mark.full
    def test_caseid_1989573(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.set_Passseat_condition_allow()
        LegrestVertical_list = [7, 5.9 ,13, 14.1]
        for i in range(4):
            self.set_Pass_position(10.0, 10.0 ,120, 10.0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                        {"params": {"id": 1,"position": {"backAngle": 120, "longitudinalPosition": 10,"verticalPosition": 10,
                        "LegrestVerticalPosition": LegrestVertical_list[i],"backAngleIsValid": True,
                        "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}},{"out": 1})
            if i == 0 or i == 2:
                sleep(1)
                self.check_Passseat_direction_not_send() 
            elif i == 1:
                self.check_Passseat_adjust(0,0,2,0)
                self.set_Pass_position(5.9, 10.0 ,120, 10.0)
            else:
                self.check_Passseat_adjust(0,0,1,0)
                self.set_Pass_position(14.1, 10.0 ,120, 10.0)           
                           
    @allure.title("主驾座椅姿态设置所有位置_差值范围内_停止控制_Mars")
    @pytest.mark.sanity
    def test_caseid_1989574(self):
        self.sd_tester.write_single_ccp(950, 1)
        positionSet = [{1:{"backAngle": 180, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置高度1向上，水平1向前
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {3:{"backAngle": 0, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置靠背1向前，腿托1向上
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}]
        self.set_Drvrseat_condition_allow()
        for positionSet1 in positionSet:
            for key,value in positionSet1.items():
                    logger.info(f"--处于主驾位置{key}-")
                    eval(f"self.set_drvr_position{key}()")#同一个位置方便调用以上四个方向
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                    {"params": {"id": 0,"position": value}},{"out": 1})
                    if key==1 :
                        self.check_drvrseat_heightsld_adjust(1,1)
                        self.set_drvr_heiperc(98.0)
                        self.set_drvr_sldperc(98.0)
                        sleep(0.5)
                        self.check_drvrseat_heightsld_adjust(0,0)
                    elif key==3 :
                        self.check_drvrseat_kaotuituo_adjust(1,1)
                        self.set_drvr_angelperc(1.0)
                        self.set_drvr_frontheiperc(97.0)
                        sleep(0.5)
                        self.check_drvrseat_kaotuituo_adjust(0,0)
    
    @allure.title("主驾座椅姿态设置所有位置_差值范围内_停止控制_Venus")
    @pytest.mark.full
    def test_caseid_1989576(self):
        self.sd_tester.write_single_ccp(950, 2)
        positionSet = [{1:{"backAngle": 180, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置高度1向上，水平1向前
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {3:{"backAngle": 0, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置靠背1向前，腿托1向上
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}]
        self.set_Drvrseat_condition_allow()
        for positionSet1 in positionSet:
            for key,value in positionSet1.items():
                    logger.info(f"--处于主驾位置{key}-")
                    eval(f"self.set_drvr_position{key}()")#同一个位置方便调用以上四个方向
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                    {"params": {"id": 0,"position": value}},{"out": 1})
                    if key==1 :
                        self.check_drvrseat_heightsld_adjust(1,1)
                        self.set_drvr_heiperc(98.0)
                        self.set_drvr_sldperc(98.0)
                        sleep(0.5)
                        self.check_drvrseat_heightsld_adjust(0,0)
                    elif key==3 :
                        self.check_drvrseat_kaotuituo_adjust(1,1)
                        self.set_drvr_angelperc(1.0)
                        self.set_drvr_frontheiperc(96.0)
                        sleep(0.5)
                        self.check_drvrseat_kaotuituo_adjust(0,0)
                        
    @allure.title("副驾座椅姿态设置所有位置_差值范围内_停止控制_Mars")
    @pytest.mark.sanity
    def test_caseid_1989577(self):
        self.sd_tester.write_single_ccp(950, 1)
        positionSet = [{1:{"backAngle": 180, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置高度1向上，水平1向前
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {3:{"backAngle": 0, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置靠背1向前，腿托1向上
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}]
        self.set_Passseat_condition_allow()
        for positionSet1 in positionSet:
            for key,value in positionSet1.items():
                    logger.info(f"--处于副驾位置{key}-")
                    eval(f"self.set_Pass_position{key}()")#同一个位置方便调用以上四个方向
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                    {"params": {"id": 1,"position": value}},{"out": 1})
                    if key==1 :
                        self.check_Passseat_heightsld_adjust(1,1)
                        self.set_pass_heiperc(98.0)
                        self.set_pass_sldperc(98.0)
                        sleep(0.5)
                        self.check_Passseat_heightsld_adjust(0,0)
                    elif key==3 :
                        self.check_Passseat_kaotuituo_adjust(1,1)
                        self.set_pass_angelperc(1.0)
                        self.set_pass_frontheiperc(97.0)
                        sleep(0.5)
                        self.check_Passseat_kaotuituo_adjust(0,0)
                        
    @allure.title("副驾座椅姿态设置所有位置_差值范围内_停止控制_Venus")
    @pytest.mark.full
    def test_caseid_1989578(self):
        self.sd_tester.write_single_ccp(950, 2)
        positionSet = [{1:{"backAngle": 180, "longitudinalPosition": 100,"verticalPosition": 100,
                         "LegrestVerticalPosition": 0,"backAngleIsValid": True,# 设置高度1向上，水平1向前
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}},
                      {3:{"backAngle": 0, "longitudinalPosition": 0,"verticalPosition": 0,
                         "LegrestVerticalPosition": 100,"backAngleIsValid": True,# 设置靠背1向前，腿托1向上
                      "longitudinalIsValid": True,"verticalIsValid": True,"legrestVerticalIsValid": True}}]
        self.set_Passseat_condition_allow()
        for positionSet1 in positionSet:
            for key,value in positionSet1.items():
                    logger.info(f"--处于副驾位置{key}-")
                    eval(f"self.set_Pass_position{key}()")#同一个位置方便调用以上四个方向
                    self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "SetPositionTarget",
                                                    {"params": {"id": 1,"position": value}},{"out": 1})
                    if key==1 :
                        self.check_Passseat_heightsld_adjust(1,1)
                        self.set_pass_heiperc(98.0)
                        self.set_pass_sldperc(98.0)
                        sleep(0.5)
                        self.check_Passseat_heightsld_adjust(0,0)
                    elif key==3 :
                        self.check_Passseat_kaotuituo_adjust(1,1)
                        self.set_pass_angelperc(1.0)
                        self.set_pass_frontheiperc(96.0)
                        sleep(0.5)
                        self.check_Passseat_kaotuituo_adjust(0,0)