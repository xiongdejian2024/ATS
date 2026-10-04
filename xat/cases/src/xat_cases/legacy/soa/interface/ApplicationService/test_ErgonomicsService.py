#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_ErgonomicsService.py
@Time         :2023/10/31 17:52:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import time
import allure
import pytest
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.sdk.sdk_tools import *


@allure.feature("SOA服务接口")
@allure.story("BGM应用/ErgonomicsService")
@pytest.mark.zjb
class TestErgonomicsService(TestBase):

    def generate_struct(self, user):
        """生成jidl所需结构体"""
        return {"uid": user['uid'],
                "isEnable": user['isEnable'],
                "position": [{"mode": 1,
                              "targetSeat": [{"id": 0,
                                              "position": user['drive_seat_position']}],
                              "targetSteer": user['drive_steer_position']},
                             {"mode": 7,
                              "targetSeat": [{"id": 0,
                                              "position": user['easy_seat_position']}],
                              "targetSteer": user['easy_steer_position']}
                             ]
                }

    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("CentralLockService", "client"),
                                     ("KeyService", "client"),
                                     ("ErgonomicsService", "client"),
                                     ("PedalService", "client"),
                                     ("ChassisService", "client"),
                                     ("SeatService", "client")
                                     ])
        self.partner.method_default_timeout = 0.1
        self.sd_tester.write_single_ccp(950, 1)
        self.vehicle_type = 1
        # 配置PE寻钥匙区域2
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 5, "value": 0}]})

        self.curr_drvr_height = 0.0
        # self.curr_drvr_back_angle = 120
        self.curr_drvr_back_angle = 0.0
        self.curr_drvr_longitudinal = 0.0
        self.curr_drvr_cushion = 0.0
        self.curr_steer_angle = 0.0  # -3~3
        self.curr_steer_length = 0.0  # -25~30

        self.user0 = {"uid": "00000000",
                      "keyId": ["101112131415161718191a1b1c1d1e3f"],  # key_id4
                      "isEnable": True,

                      "drive_seat_position": {"backAngle": 104,
                                              "longitudinalPosition": 30.0,
                                              "verticalPosition": 40.0,
                                              "LegrestVerticalPosition": 8.0},
                      #不能设置为30？
                    #   "drive_steer_position": {"angle": 3.0,
                    #                            "length": 30.0},
                        "drive_steer_position": {"angle": 3.0,
                                               "length": 25.0},

                      "easy_seat_position": {"backAngle": 160,
                                             "longitudinalPosition": 35.0,
                                             "verticalPosition": 35.0,
                                             "LegrestVerticalPosition": 60.0},
                      "easy_steer_position": {"angle": 2.0,
                                              "length": -10.0}
                      }

        self.user1 = {"uid": "12345678",
                      "keyId": ["000102030405060708090a0b0c0d0e0f"],  # key_id1
                      "isEnable": True,
                      "drive_seat_position": {"backAngle": 110,
                                              "longitudinalPosition": 20.0,
                                              "verticalPosition": 10.0,
                                              "LegrestVerticalPosition": 70.0},
                      "drive_steer_position": {"angle": 2.7,
                                               "length": 22.0},
                      "easy_seat_position": {"backAngle": 160,
                                             "longitudinalPosition": 45.0,
                                             "verticalPosition": 24.0,
                                             "LegrestVerticalPosition": 15.0},
                      "easy_steer_position": {"angle": 1.0,
                                              "length": 15.0}
                      }

        self.user2 = {"uid": "87654321",
                      "keyId": ["101112131415161718191a1b1c1d1e1f"],  # key_id2
                      "isEnable": False,
                      "drive_seat_position": {"backAngle": 120,
                                              "longitudinalPosition": 7.0,
                                              "verticalPosition": 80.0,
                                              "LegrestVerticalPosition": 90.0},
                      "drive_steer_position": {"angle": 1.5,
                                               "length": 19.0},
                      "easy_seat_position": {"backAngle": 135,
                                             "longitudinalPosition": 20.0,
                                             "verticalPosition": 40.0,
                                             "LegrestVerticalPosition": 65.0},
                      "easy_steer_position": {"angle": -2.2,
                                              "length": -15.0}
                      }

        self.user_default = {"uid": "11111111",  # 默认用户无uid和keyid
                             "keyId": ["101112131415161718191a1b1c1d1e1f"],  # key_id2
                             "isEnable": True,
                             "drive_seat_position": {"backAngle": 115,
                                                     "longitudinalPosition": 18.5,
                                                     "verticalPosition": 42.3,
                                                     "LegrestVerticalPosition": 49.1},
                             "drive_steer_position": {"angle": 0.0,
                                                      "length": 0.0},
                             "easy_seat_position": {"backAngle": 115,
                                                    "longitudinalPosition": 14.7,
                                                    "verticalPosition": 0.0,
                                                    "LegrestVerticalPosition": 49.1},
                             "easy_steer_position": {"angle": 0.0,
                                                     "length": -25.0}
                             }

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.set_nopeople_incar()
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set_vehspd(0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.sd_tester.write_multi_ccp({94: 0x80, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x4, 578: 0x4})
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下

        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetUidAccountPosition",
                                              {"infos": [self.generate_struct(self.user0),
                                                         self.generate_struct(self.user1),
                                                         self.generate_struct(self.user2)
                                                         ]},
                                              {"out": 1}, timeout=0.5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetUidKeyIdAccountInfo",
                                              {"infos": [{"keyId": self.user0['keyId'],
                                                          "uid": self.user0['uid']},
                                                         {"keyId": self.user1['keyId'],
                                                          "uid": self.user1['uid']},
                                                         {"keyId": self.user2['keyId'],
                                                          "uid": self.user2['uid']},
                                                         ]
                                               }, {"out": 1}, timeout=0.5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetCurrentLoginStatus",
                                              {"sts": {"uid": self.user0['uid']}}, {"out": 1}, timeout=0.5)
        self.partner.send_method_request(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": False})

        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)  # 刹车踏板未踩下
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 1)  # 座椅可调前置条件
        self.set_drvr_belt_unlock()  # 安全带未系
        self.dk.set_cenlock_sts(3)  # 整车闭锁

        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', 3)

        self.set_drvr_height(20.0)  # 高度和靠背角度是一个电机，先高度，再角度
        # self.set_drvr_back_angle(20.0)
        self.set_drvr_back_angle(120.0)
        self.set_drvr_longitudinal(20.0)  # 前后和坐垫高度是一个电机，先前后，再坐垫高度
        self.set_drvr_cushion(20.0)

        self.set_steer_position(0.0, 0.0)  # 角度和长度是一个电机，先角度，再高度
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])  # 踩刹车寻钥匙可以找到钥匙
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StopMoveDirection', 
                                         {"id": 0, "part": 0, "direction": 0},timeout=0.5)
        #保证闭锁状态被存住
        self.partner.empty_all(15)

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)  # 刹车踏板未踩下
        super().after_each_func(ecu, start=False)

    def restart_bgm_and_wait_for_keyService(self):
        sleep(3)  # 防止闭锁没有成功存到NVM
        self.restart_bgm_and_connect_service(KEY_SERVICE_CLIENT)
        # self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "NotifyDigitalKeyServiceStatus", {"isEnable": True})

    def set_gear(self, gear):
        """设置档位"""
        map = {"GearP": 0, "GearN": 2, "GearR": 1, "GearD": 3}
        self.dk.set_chassis_service_gear(gear)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetGear", {}, {"out": map[gear]}, timeout=1.5)

    def ck_control(self, user, mode=0, enable=None):
        """
        根据输入的用户和进入的模式来校验方向盘和座椅控制是否正常
        @param user: 用户信息，self.user1等
        @param mode: 1：驾驶模式，7：舒适模式，0：无模式请求
        @param enable: 是否进行控制
        """
        exp_seat_position = user["drive_seat_position"] if mode == 1 else user["easy_seat_position"]
        exp_steer_position = user["drive_steer_position"] if mode == 1 else user["easy_steer_position"]
        if enable is None:
            if mode == 1:  # 驾驶模式，一定能控制
                enable = True
            elif mode == 0:
                enable = False
            else:
                enable = user['isEnable']
        else:
            enable = False
        self.ck_seat_height_control(exp_seat_position['verticalPosition'], enable)
        self.ck_seat_longitudinal_control(exp_seat_position['longitudinalPosition'], enable)
        self.ck_seat_back_angle_control(exp_seat_position['backAngle'], enable)
        self.ck_seat_cushion_control(exp_seat_position['LegrestVerticalPosition'], enable)
        self.ck_steer_angle_control(exp_steer_position['angle'], enable)
        self.ck_steer_length_control(exp_steer_position['length'], enable)

    def ck_seat_back_angle_control(self, exp_angle, control_enable):
        """校验座椅靠背角度控制"""
        if exp_angle - self.curr_drvr_back_angle > 2:  # 角度增加>>180，靠背向后Backward
            if control_enable:
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'BackRestAdjmtRowFirstDrvr', 2, timeout=1.5)
                self.set_drvr_back_angle(exp_angle)
        elif self.curr_drvr_back_angle - exp_angle > 2:
            if control_enable:
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'BackRestAdjmtRowFirstDrvr', 1, timeout=1.5)
                self.set_drvr_back_angle(exp_angle)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'BackRestAdjmtRowFirstDrvr', 0, timeout=1.5)

    def ck_seat_height_control(self, exp_height, control_enable):
        """校验座椅高度控制"""
        if exp_height - self.curr_drvr_height > 2:  # 百分比增大>>100%，座椅上Up
            if control_enable:
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatHeiAdjmtRowFirstDrvr', 1, timeout=1.5)
                self.set_drvr_height(exp_height)
        elif self.curr_drvr_height - exp_height > 2:
            if control_enable:
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatHeiAdjmtRowFirstDrvr', 2, timeout=1.5)
                self.set_drvr_height(exp_height)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatHeiAdjmtRowFirstDrvr', 0, timeout=1.5)

    def ck_seat_longitudinal_control(self, exp_longitudinal, control_enable):
        """校验座椅前后控制"""
        if exp_longitudinal - self.curr_drvr_longitudinal > 2:  # 百分比增大>>100%，座椅前Forward
            if control_enable:
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstDrvr', 1, timeout=1.5)
                self.set_drvr_longitudinal(exp_longitudinal)
        elif self.curr_drvr_longitudinal - exp_longitudinal > 2:
            if control_enable:
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstDrvr', 2, timeout=1.5)
                self.set_drvr_longitudinal(exp_longitudinal)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstDrvr', 0, timeout=1.5)

    def ck_seat_cushion_control(self, exp_cushion, control_enable):
        """校验座椅坐垫/腿托控制"""
        if exp_cushion - self.curr_drvr_cushion > 3:  # 百分比增大>>100%，坐垫上Up
            if control_enable:
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatCushTiltAdjmtRowFirstDrvr', 1, timeout=1.5)
                self.set_drvr_cushion(exp_cushion)
        elif self.curr_drvr_cushion - exp_cushion > 3:
            if control_enable:
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatCushTiltAdjmtRowFirstDrvr', 2, timeout=1.5)
                self.set_drvr_cushion(exp_cushion)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatCushTiltAdjmtRowFirstDrvr', 0, timeout=1.5)

    def ck_steer_angle_control(self, exp_angle, control_enable):
        """
        校验方向盘角度控制
        @param exp_angle: 预期控制角度，float
        @param control_enable: 是否控制，舒适进出可能不控制
        """
        if control_enable:
            if (self.vehicle_type == 1 and abs(self.curr_steer_angle - exp_angle) > 0.1625) or (self.vehicle_type == 2 and abs(self.curr_steer_angle - exp_angle) > 0.1603):
                # Marsone至少差0.1625(对应总线值13),Venus至少差0.1603(对应总线值7)才会触发控制
                if self.curr_steer_angle > exp_angle:  # 角度增加>>-3，Up
                    self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtUpSts', 1, timeout=1.5)
                else:
                    self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtDwnSts', 1, timeout=1.5)
                self.set_steer_position(angle=exp_angle)
        self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtUpSts', 0, timeout=1.5)
        self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtDwnSts', 0, timeout=1.5)

    def ck_steer_length_control(self, exp_length, control_enable):
        """
        校验方向盘长度控制
        @param exp_length: 预期控制长度，float
        @param control_enable: 是否控制，舒适进出可能不控制
        """
        if control_enable:
            if (self.vehicle_type == 1 and abs(self.curr_steer_length - exp_length) > 1.3) or (self.vehicle_type == 2 and abs(self.curr_steer_length - exp_length) > 1.2):
                # Marsone至少差1.3(对应总线值13),Venus至少差1.2(对应总线值6)才会触发控制
                if self.curr_steer_length < exp_length:  # 长度增加>>30，Backward   
                    self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 1, timeout=1.5)
                else:
                    self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 1, timeout=1.5)
                self.set_steer_position(length=exp_length)
        self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 0, timeout=1.5)
        self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 0, timeout=1.5)

    def set_drvr_cushion(self, perc):
        """设置主驾腿托位置"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiPerc', perc)
        self.curr_drvr_cushion = perc

    def set_drvr_longitudinal(self, perc):
        """设置主驾前后位置"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldPerc', perc)
        self.curr_drvr_longitudinal = perc

    def set_drvr_back_angle(self, perc):
        """设置主驾靠背角度"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'SeatBackAngleRowFirstDrvr_0_SmdBodySignalIPdu01', perc)
        self.curr_drvr_back_angle = perc

    def set_drvr_height(self, perc):
        """设置主驾高度位置"""
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiPerc', perc)
        self.curr_drvr_height = perc

    def set_steer_position(self, angle: float = None, length: float = None):
        """
        设置方向盘角度和长度, 根据SteerWheelPositionChanged接口定义的转换为int类型给到总线上
        @param angle: 方向盘角度
        @param length: 方向盘长度
        """
        hint = ''
        if angle is not None:
            if self.vehicle_type == 1:
                self.angle_can_signal = round((angle + 3.3375) / 0.0125)
            else:
                self.angle_can_signal = round((angle + 3.3664) / 0.0229)
            self.ipdu.set(self.ipdu.cem_lin4.AswmCem_Lin4Fr02, 'SteerWhlPosnAng', self.angle_can_signal)
            self.curr_steer_angle = angle
            hint += f"设置方向盘角度{angle}--总线值{self.angle_can_signal}"
        if length is not None:
            if self.vehicle_type == 1:
                self.length_can_signal = round((length + 27.8) / 0.1)
            else:
                self.length_can_signal = round((length + 28) / 0.2)
            self.ipdu.set(self.ipdu.cem_lin4.AswmCem_Lin4Fr02, 'SteerWhlPosnX', self.length_can_signal)
            self.curr_steer_length = length
            hint += f" 设置方向盘长度{length}--总线值{self.length_can_signal}"
        logger.info(hint)

    def set_drvr_belt_lock(self):
        """设置主驾安全带已系"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', 1)

    def set_drvr_belt_unlock(self):
        """设置主驾安全带未系"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', 0)

    @allure.title("每次调用SetModeInhibit均触发ModeInhibitSts")
    @pytest.mark.sanity
    def test_caseid_1979850(self):
        self.partner.send_method_request(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True})
        self.partner.ck_s2s_event(ERGONOMICS_SERVICE_CLIENT, "ModeInhibitSts", {"sts": True})
        self.partner.send_method_request(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True})
        self.partner.ck_s2s_event(ERGONOMICS_SERVICE_CLIENT, "ModeInhibitSts", {"sts": True})
        self.partner.send_method_request(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": False})
        self.partner.ck_s2s_event(ERGONOMICS_SERVICE_CLIENT, "ModeInhibitSts", {"sts": False})

    @allure.title("解锁->解锁_SetModeInhibit_原mode为0_NoRequest_返回out=0")
    @pytest.mark.full
    def test_caseid_1979864(self):
        self.dk.set_cenlock_sts(1)
        sleep(5)
        self.restart_bgm_and_connect_service(CENTRALLOCK_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", 
                                  {"info": {"sts": 1}})
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=2)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 0}, cycle_time=1)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": True})

        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": False},
                                              {"out": 0}, cycle_time=1)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})

    @allure.title("启动后5s内蓝牙解锁进入驾驶模式_舒适模式未打开_执行控制_SetModeInhibit返回out=1")
    @pytest.mark.smoke
    def test_caseid_1979867(self):
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        assert self.partner.partner_infos[ERGONOMICS_SERVICE_CLIENT].service_status == "OFFLINE"
        self.dk.send_rke_unlock(key_id=key_id2)
        self.ck_control(self.user2, 1)

        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 1})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": True})

        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": False},
                                              {"out": 0}, cycle_time=1)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})

    @allure.title("启动后5s内蓝牙解锁进入舒适模式_执行控制_keyid匹配到uid_非上一个用户_SetModeInhibit返回out=7")
    @pytest.mark.smoke
    def test_caseid_1979875(self):
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        assert self.partner.partner_infos[ERGONOMICS_SERVICE_CLIENT].service_status == "OFFLINE"
        self.dk.send_rke_unlock(key_id=key_id1)
        self.ck_control(self.user1, 7)

        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})

        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 7})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": True})

        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": False},
                                              {"out": 0}, cycle_time=1)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})

    @allure.title("启动后5s内蓝牙解锁进入舒适模式_执行控制_keyid匹配到uid_上一个用户_SetModeInhibit返回out=7")
    @pytest.mark.sanity
    def test_caseid_1979886(self):
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        assert self.partner.partner_infos[ERGONOMICS_SERVICE_CLIENT].service_status == "OFFLINE"
        self.dk.send_rke_unlock(key_id=key_id4)
        self.ck_control(self.user0, 7)

        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 7})

    @allure.title("启动后5s内近车解锁进入舒适模式_执行控制_keyid未匹配到uid_使用上一个用户信息")
    @pytest.mark.sanity
    def test_caseid_1979876(self):
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        assert self.partner.partner_infos[ERGONOMICS_SERVICE_CLIENT].service_status == "OFFLINE"
        self.dk.send_approach_unlock_cmd(key_id=key_id3)
        self.ck_control(self.user0, 7)

        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 7})

    @allure.title("GetModeInhibitSts_服务启动默认值False")
    @pytest.mark.sanity
    def test_caseid_1979877(self):
        self.restart_bgm_and_connect_service(ERGONOMICS_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})

    @allure.title("启动后5s内不给刹车/UM数据_蓝牙解锁不会控制_5s超时服务上线")
    @pytest.mark.full
    def test_caseid_1979880(self):
        self.ipdu.pause_bus_send("backbonefr")
        sleep(1)
        self.bgm_power_off_and_on(timeout=3)
        self.partner.empty_all()
        self.partner.wait_for_service_reconnect(KEY_SERVICE_CLIENT)
        self.set_gear("GearP")

        self.dk.send_rke_unlock(key_id1)
        self.ck_control(self.user1, 0, enable=False)
        assert self.partner.partner_infos[ERGONOMICS_SERVICE_CLIENT].service_status == "OFFLINE"
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})

        self.ipdu.resume_bus_send("backbonefr")
        sleep(1)
        self.ck_control(self.user1, 0, enable=False)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 0}, cycle_time=1)

    @allure.title("启动后5s内不给档位数据_蓝牙解锁不会控制_5s超时服务上线_获取到档位数据后不再控制")
    @pytest.mark.full
    def test_caseid_1979881(self):
        self.ipdu.pause_bus_send("propulsioncan")
        sleep(1)
        self.bgm_power_off_and_on(timeout=3)
        self.partner.empty_all()
        self.partner.wait_for_service_reconnect(KEY_SERVICE_CLIENT)

        self.dk.send_rke_unlock(key_id1)
        self.ck_control(self.user1, 0, enable=False)
        assert self.partner.partner_infos[ERGONOMICS_SERVICE_CLIENT].service_status == "OFFLINE"
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})

        self.ipdu.resume_bus_send("propulsioncan")
        self.dk.set_chassis_service_gear("GearP")
        sleep(1)
        self.ck_control(self.user1, 0, enable=False)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 0}, cycle_time=1)

    @allure.title("启动后5s内不触发解锁事件_5s超时服务上线_蓝牙解锁会控制")
    @pytest.mark.sanity
    def test_caseid_1979882(self):
        self.restart_bgm_and_connect_service(ERGONOMICS_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
        self.set_gear("GearP")

        self.dk.send_rke_unlock(key_id1)
        self.ck_control(self.user1, 7)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 7})

    @allure.title("启动后5s内远控解锁_按历史用户进入舒适模式并控制_踩刹车进入驾驶模式并控制_主驾安全带解开&档位从D到P进入舒适模式并控制")
    @pytest.mark.sanity
    def test_caseid_1979883(self):
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 1})
        self.ck_control(self.user0, 7)

        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=1)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": False},
                                              {"out": 7})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ck_control(self.user0, 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)

        self.set_drvr_belt_unlock()
        self.sd_tester.change_usage_mode(13)
        self.set_gear("GearD")

        self.sd_tester.change_usage_mode(2)
        self.set_gear("GearP")
        self.ck_control(self.user0, 7)

    @allure.title("启动后5s内远控解锁_按历史用户(isEnable=False)进入驾驶模式并控制_主驾安全带解开&档位从D到P进入舒适模式并控制_踩刹车进驾驶模式并控制")
    @pytest.mark.full
    def test_caseid_1980054(self):
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetCurrentLoginStatus",
                                              {"sts": {"uid": self.user2['uid']}}, {"out": 1})
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 1} ,timeout = 0.5)
        self.ck_control(self.user2, 1)

        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": False},
                                              {"out": 1})
        self.set_drvr_belt_unlock()
        self.sd_tester.change_usage_mode(13)
        self.set_gear("GearD")

        self.sd_tester.change_usage_mode(2)
        self.set_gear("GearP")
        self.ck_control(self.user2, 0)

    @allure.title("启动后5s内内部其他方式解锁进入中间态_5s超时服务上线按历史用户进入舒适模式但不控制_踩刹车进入驾驶模式并控制_主驾安全带解开&档位从D到P进入舒适模式并控制")
    @pytest.mark.full
    def test_caseid_1979884(self):
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 3})
        assert self.partner.partner_infos[ERGONOMICS_SERVICE_CLIENT].service_status == "OFFLINE"
        self.ck_control(self.user0, 0)

        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": False},
                                              {"out": 0}, cycle_time=1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ck_control(self.user0, 1)

        self.set_drvr_belt_unlock()
        self.sd_tester.change_usage_mode(13)
        self.set_gear("GearD")

        self.sd_tester.change_usage_mode(2)
        self.set_gear("GearP")
        self.ck_control(self.user0, 7)
    
    @allure.title("解锁状态(triggresrc=11)下重启BGM_调用SetModeInhibit返回No_req")
    @pytest.mark.full
    def test_caseid_1983352(self):
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 3})
        self.dk.ck_cenlock_sts(1, 11)
        sleep(3)
        self.restart_bgm_and_connect_service(KEY_SERVICE_CLIENT)
        self.set_gear("GearP")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ck_control(self.user0, 0)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 0}, cycle_time=1)
        
    @allure.title("解锁状态(nfc解锁)下重启BGM_服务启动前调用SetModeInhibit返回No_req")
    @pytest.mark.full
    def test_caseid_1985197(self):
        self.dk.set_cenlock_sts(1)
        sleep(3)
        #KEY服务上线后，5s舒适进出服务才能上线
        self.restart_bgm_and_connect_service(KEY_SERVICE_CLIENT)
        self.set_gear("GearP")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ck_control(self.user0, 0)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 0}, cycle_time=1)
        
    @allure.title("解锁状态(triggresrc=11)下重启BGM_服务启动后调用SetModeInhibit返回No_req")
    @pytest.mark.full
    def test_caseid_1985198(self):
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 3})
        self.dk.ck_cenlock_sts(1)
        sleep(3)
        self.restart_bgm_and_connect_service(ERGONOMICS_SERVICE_CLIENT)
        self.set_gear("GearP")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ck_control(self.user0, 0)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 0}, cycle_time=1)
        
    @allure.title("解锁状态(nfc解锁)下重启BGM_服务启动后调用SetModeInhibit返回No_req")
    @pytest.mark.full
    def test_caseid_1985199(self):
        self.dk.set_cenlock_sts(1)
        sleep(3)
        self.restart_bgm_and_connect_service(ERGONOMICS_SERVICE_CLIENT)
        self.set_gear("GearP")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ck_control(self.user0, 0)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 0}, cycle_time=1)

    @allure.title("启动后5s内nfc解锁进入舒适模式_执行控制")
    @pytest.mark.sanity
    def test_caseid_1979885(self):
        sleep(3)
        self.dk.set_chassis_service_gear("GearP")
        self.bgm_power_off_and_on()
        self.partner.empty_all(1)
        self.dk.send_nfc_cmd(key_id1)
        self.partner.wait_for_service_reconnect(CENTRALLOCK_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", 
                                  {"info": {"sts": 1, "triggerId": 12, "updateEve": False}})
        self.ck_control(self.user1, 7)
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=2)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 7})

    @allure.title("启动后5s内nfc解锁进入驾驶模式_舒适模式未打开_执行控制")
    @pytest.mark.sanity
    def test_caseid_1980008(self):
        sleep(3)
        self.dk.set_chassis_service_gear("GearP")
        self.bgm_power_off_and_on()
        self.partner.empty_all(1)
        self.dk.send_nfc_cmd(key_id2)
        self.partner.wait_for_service_reconnect(CENTRALLOCK_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", 
                                  {"info": {"sts": 1, "triggerId": 12, "updateEve": False}})
        self.ck_control(self.user2, 1)
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=2)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 1})

    @allure.title("启动后5s内车外按钮解锁进入舒适模式_执行控制_keyid匹配到uid_非上一个用户_SetModeInhibit返回out=7")
    @pytest.mark.sanity
    def test_caseid_1979889(self):
        sleep(3)
        self.dk.set_chassis_service_gear("GearP")
        self.bgm_power_off_and_on()
        self.partner.empty_all(1)
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.press_door_outswitch(4, 0.5)
        self.partner.wait_for_service_reconnect(CENTRALLOCK_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", 
                                  {"info": {"sts": 1, "triggerId": 2, "updateEve": False}})
        self.ck_control(self.user1, 7)
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 7})

    @allure.title("启动后5s内内部解锁不会控制_5s超时服务上线")
    @pytest.mark.smoke
    def test_caseid_1979899(self):
        self.restart_bgm_and_connect_service(KEY_SERVICE_CLIENT)
        self.set_gear("GearP")
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 2},timeout=0.5)
        self.ck_control(self.user0, 0)
        assert self.partner.partner_infos[ERGONOMICS_SERVICE_CLIENT].service_status == "OFFLINE"
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 7})

    @allure.title("启动5s后Crash解锁进入中间态_5s超时服务上线")
    @pytest.mark.full
    def test_caseid_1979901(self):
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        self.sd_tester.change_car_mode(0x3)
        try:
            self.ck_control(self.user0, 0)

            self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
            self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
            self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                                {"out": 0}, cycle_time=1)
        except Exception as e:
            logger.error(e)
            sleep(10)
            raise e
        else:
            sleep(10)  # 10s内无法闭锁，下个case可能fail

    @allure.title("trunlock等待服务上线后再PE unlock进入舒适模式")
    @pytest.mark.full
    def test_caseid_1979956(self):
        sleep(3)
        self.dk.set_chassis_service_gear("GearP")
        self.bgm_power_off_and_on()
        self.partner.empty_all(1)
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 2)])
        self.dk.press_door_outswitch(5, 0.5)
        self.dk.ck_cenlock_sts(2)
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=15)
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.press_door_outswitch(4, 1.5)
        self.ck_control(self.user1, 7)

        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 7})

    @allure.title("启动后5s内远控解锁_按历史用户进入舒适模式并控制_服务上线后_RKE重复解锁(另一个用户)会触发舒适进入")
    @pytest.mark.full
    def test_caseid_1979982(self):
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 1})
        self.ck_control(self.user0, 7)

        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": False},
                                              {"out": 7})

        self.dk.send_rke_unlock(key_id1)
        self.ck_control(self.user1, 7)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 7})

    @allure.title("启动后5s内蓝牙解锁进入驾驶模式_Active_执行控制_上一个用户")
    @pytest.mark.sanity
    def test_caseid_1979902(self):
        self.sd_tester.change_usage_mode(0xD)
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearN")
        sleep(1)  # Driving重启后是Active，但是KeyService把解锁指令给到rke的时候可能还没拿到Usagemode 11，因此rke是请求的默认值abandon来判断的，此时会报UasgeModeFail
        self.dk.send_nfc_cmd(key_id=key_id4)
        assert self.partner.partner_infos[ERGONOMICS_SERVICE_CLIENT].service_status == "OFFLINE"
        self.ck_control(self.user0, 1)

        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 1})

    @allure.title(
        "启动后5s内蓝牙解锁进入驾驶模式_Active_执行控制_非上一个用户")  # R档需要Active或Driving才能进，和此处Active一样，属于重复case
    @pytest.mark.full
    def test_caseid_1979903(self):
        self.sd_tester.change_usage_mode(0xD)
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        sleep(1)
        self.dk.send_nfc_cmd(key_id=key_id1)
        assert self.partner.partner_infos[ERGONOMICS_SERVICE_CLIENT].service_status == "OFFLINE"
        #SOA-28237
        self.ck_control(self.user1, 7)

        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 7})

    @allure.title("启动后5s内蓝牙解锁(刹车踩下)进入驾驶模式_执行控制")
    @pytest.mark.smoke
    def test_caseid_1979904(self):
        self.restart_bgm_and_wait_for_keyService()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                    {"status": {"value": 1, "validity": 0}})
        self.set_gear("GearP")
        assert self.partner.partner_infos[ERGONOMICS_SERVICE_CLIENT].service_status == "OFFLINE"
        self.dk.send_rke_unlock(key_id=key_id1)
        self.ck_control(self.user1, 1)

        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 1})

    @allure.title("启动后5s内蓝牙解锁(N档)进入驾驶模式_执行控制")
    @pytest.mark.full
    def test_caseid_1979905(self):
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearN")
        assert self.partner.partner_infos[ERGONOMICS_SERVICE_CLIENT].service_status == "OFFLINE"
        self.dk.send_nfc_cmd(key_id=key_id1)
        self.ck_control(self.user1, 1)

        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 1})

    #5s后解锁不会起定时钥匙id变化或锁状态变化哪个先来就先进行控制，执行位置调节，所以会导致重启后，一开始有两次位置调节
    #时间间隔100ms左右，不会影响功能
    @allure.title("启动5s后_服务上线cdc连接但未禁用_触发解锁事件_进入舒适模式_再次触发解锁事件(另一个uid)_进入舒适模式")
    @pytest.mark.sanity
    @pytest.mark.failed
    def test_caseid_1979911(self):
        self.restart_bgm_and_connect_service(ERGONOMICS_SERVICE_CLIENT)
        self.set_gear("GearP")
        self.dk.send_rke_unlock(key_id=key_id1)
        self.ck_control(self.user1, 7)

        self.dk.set_cenlock_sts(3)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetCurrentLoginStatus",
                                              {"sts": {"uid": '12345678'}}, {"out": 1})

        sleep(2)
        self.dk.send_rke_unlock(key_id=key_id4)
        self.ck_control(self.user0, 7)

    @allure.title("启动5s后_服务上线cdc连接但未禁用_触发解锁事件_进入驾驶模式_再次触发解锁事件(另一个uid)_进入舒适模式")
    @pytest.mark.full
    def test_caseid_1979913(self):
        self.restart_bgm_and_connect_service(ERGONOMICS_SERVICE_CLIENT)
        self.set_gear("GearP")
        self.dk.send_rke_unlock(key_id=key_id2)
        self.ck_control(self.user2, 1)

        self.dk.set_cenlock_sts(3)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetCurrentLoginStatus",
                                              {"sts": {"uid": '87654321'}}, {"out": 1})

        sleep(2)
        self.dk.send_rke_unlock(key_id=key_id4)
        self.ck_control(self.user0, 7)

    @allure.title("启动5s后_服务上线cdc连接但未禁用_触发解锁事件_进入舒适模式_再次触发解锁事件(同一个uid)_进入舒适模式")
    @pytest.mark.full
    def test_caseid_1979917(self):
        self.restart_bgm_and_connect_service(ERGONOMICS_SERVICE_CLIENT)
        self.set_gear("GearP")
        self.dk.send_rke_unlock(key_id=key_id1)
        self.ck_control(self.user1, 7)

        self.dk.set_cenlock_sts(3)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetCurrentLoginStatus",
                                              {"sts": {"uid": '12345678'}}, {"out": 1})

        sleep(2)
        self.dk.send_rke_unlock(key_id=key_id1)
        self.ck_control(self.user1, 7)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 7})

    @allure.title("启动5s后_服务上线cdc连接并禁用_触发解锁事件_进入舒适模式但不控制")
    @pytest.mark.smoke
    def test_caseid_1979924(self):
        self.restart_bgm_and_connect_service(ERGONOMICS_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 0}, cycle_time=1)
        self.set_gear("GearP")
        self.dk.send_rke_unlock(key_id=key_id1)
        self.ck_control(self.user1, 7, enable=False)

    @allure.title("启动5s后_服务上线cdc连接并禁用_触发解锁事件_进入驾驶模式但不控制")
    @pytest.mark.sanity
    def test_caseid_1979925(self):
        self.restart_bgm_and_connect_service(ERGONOMICS_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 0}, cycle_time=1)
        self.set_gear("GearP")
        self.dk.send_rke_unlock(key_id=key_id2)
        self.ck_control(self.user2, 1, enable=False)

    @allure.title("启动后5s内解锁进入舒适模式_执行控制_服务上线cdc连接并禁用_再次触发解锁事件(另一个uid)_进入舒适模式但不控制")
    @pytest.mark.full
    def test_caseid_1979926(self):
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        self.dk.send_rke_unlock(key_id=key_id1)
        self.ck_control(self.user1, 7)
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 7})
        self.dk.set_cenlock_sts(3)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetCurrentLoginStatus",
                                              {"sts": {"uid": '12345678'}}, {"out": 1})
        sleep(1)
        self.dk.send_rke_unlock(key_id=key_id4)
        self.ck_control(self.user0, 7, enable=False)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": False},
                                              {"out": 0}, cycle_time=1)

    @allure.title("启动后5s内解锁进入舒适模式_执行控制_服务上线cdc连接并禁用_踩刹车进入驾驶模式但不控制")
    @pytest.mark.full
    def test_caseid_1979927(self):
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        self.dk.send_rke_unlock(key_id=key_id1)
        self.ck_control(self.user1, 7)
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 7})
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                    {"status": {"value": 1, "validity": 0}})
        self.ck_control(self.user1, 1, enable=False)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": False},
                                              {"out": 0}, cycle_time=1)

    @allure.title(
        "启动后5s内解锁进入驾驶模式_执行控制_服务上线cdc连接并禁用_档位P&主驾安全带系上到解开进入舒适模式但不控制")
    @pytest.mark.full
    def test_caseid_1979929(self):
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                    {"status": {"value": 1, "validity": 0}})
        self.dk.send_rke_unlock(key_id=key_id1)
        self.ck_control(self.user1, 1)

        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                    {"status": {"value": 0, "validity": 0}})

        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 1})

        self.set_drvr_belt_lock()
        sleep(1)
        self.set_drvr_belt_unlock()
        sleep(1)
        self.ck_control(self.user1, 7, enable=False)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": False},
                                              {"out": 0}, cycle_time=1)

    @allure.title("启动后5s内解锁进入驾驶模式_执行控制_档位P&主驾安全带系上到解开_进入舒适模式并控制")
    @pytest.mark.full
    def test_caseid_1979930(self):
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                    {"status": {"value": 1, "validity": 0}})
        self.dk.send_rke_unlock(key_id=key_id1)
        self.ck_control(self.user1, 1)

        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                    {"status": {"value": 0, "validity": 0}})

        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.set_drvr_belt_lock()
        sleep(1)
        self.sd_tester.change_usage_mode(13)
        self.set_gear("GearD")

        self.sd_tester.change_usage_mode(2)  # 安全带系着的情况下，档位从非P到P不会切舒适模式控制
        self.set_gear("GearP")
        self.ck_control(self.user1, 7, enable=False)

        self.set_drvr_belt_unlock()
        sleep(1)
        self.ck_control(self.user1, 7)

    @allure.title("启动后5s内解锁进入驾驶模式_执行控制_主驾安全带解开&档位从D到P_进入舒适模式并控制")
    @pytest.mark.full
    def test_caseid_1979934(self):
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                    {"status": {"value": 1, "validity": 0}})
        self.dk.send_rke_unlock(key_id=key_id1)
        self.ck_control(self.user1, 1)

        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                    {"status": {"value": 0, "validity": 0}})
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)

        self.set_drvr_belt_unlock()
        self.sd_tester.change_usage_mode(13)
        self.set_gear("GearD")

        self.sd_tester.change_usage_mode(2)
        self.set_gear("GearP")
        self.ck_control(self.user1, 7)

    @allure.title("启动后5s内解锁进入驾驶模式_执行控制_主驾安全带解开&档位从R到P_进入舒适模式并控制")
    @pytest.mark.full
    def test_caseid_1979936(self):
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                    {"status": {"value": 1, "validity": 0}})
        self.dk.send_rke_unlock(key_id=key_id1)
        self.ck_control(self.user1, 1)

        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                    {"status": {"value": 0, "validity": 0}})
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)

        self.set_drvr_belt_unlock()
        self.sd_tester.change_usage_mode(13)
        self.set_gear("GearR")

        self.sd_tester.change_usage_mode(2)
        self.set_gear("GearP")
        self.ck_control(self.user1, 7)

    @allure.title("启动后5s内解锁进入驾驶模式_执行控制_主驾安全带解开&档位从N到P_进入舒适模式并控制")
    @pytest.mark.full
    def test_caseid_1979937(self):
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                    {"status": {"value": 1, "validity": 0}})
        self.dk.send_rke_unlock(key_id=key_id1)
        self.ck_control(self.user1, 1)

        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                    {"status": {"value": 0, "validity": 0}})
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)

        self.set_gear("GearN")
        self.set_gear("GearP")
        self.ck_control(self.user1, 7)

    @allure.title("启动后5s内解锁进入驾驶模式_执行控制_主驾安全带解开&档位从NA到P_进入舒适模式并控制")
    @pytest.mark.full
    def test_caseid_1979938(self):
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                    {"status": {"value": 1, "validity": 0}})
        self.dk.send_rke_unlock(key_id=key_id1)
        self.ck_control(self.user1, 1)

        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                    {"status": {"value": 0, "validity": 0}})
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)

        self.ipdu.propulsioncan_ecmpropfr24_gearlvrindcn_1_ecmpropsignalipdu24_gearlvrindcn2_manmodeindcn()
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "Gear", {"gear": 5})

        self.set_gear("GearP")
        self.ck_control(self.user1, 7)

    @allure.title("启动后5s内解锁进入舒适模式_执行控制_服务上线cdc连接但不禁用_踩刹车进入驾驶模式并控制")
    @pytest.mark.sanity
    def test_caseid_1979939(self):
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        self.dk.send_rke_unlock(key_id=key_id1)
        self.ck_control(self.user1, 7)
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)

        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                    {"status": {"value": 1, "validity": 0}})
        self.ck_control(self.user1, 1)

    @allure.title("启动后5s内解锁进入舒适模式_执行控制_服务上线cdc连接但不禁用_P档切D档进入驾驶模式并控制")
    @pytest.mark.full
    def test_caseid_1979942(self):
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        self.dk.send_rke_unlock(key_id=key_id1)
        self.ck_control(self.user1, 7)
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)

        self.sd_tester.change_usage_mode(0xD)
        self.set_gear("GearD")
        self.ck_control(self.user1, 1)

    @allure.title("启动后5s内解锁进入舒适模式_执行控制_服务上线cdc连接但不禁用_P档切N档进入驾驶模式并控制")
    @pytest.mark.full
    def test_caseid_1979943(self):
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        self.dk.send_rke_unlock(key_id=key_id1)
        self.ck_control(self.user1, 7)
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)

        self.set_gear("GearN")
        self.ck_control(self.user1, 1)

    @allure.title("启动后5s内解锁进入舒适模式_执行控制_服务上线cdc连接但不禁用_P档切R档进入驾驶模式并控制")
    @pytest.mark.full
    def test_caseid_1979944(self):
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        self.dk.send_rke_unlock(key_id=key_id1)
        self.ck_control(self.user1, 7)
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)

        self.sd_tester.change_usage_mode(0xD)
        self.set_gear("GearR")
        self.ck_control(self.user1, 1)

    @allure.title("启动后5s内解锁进入舒适模式_执行控制_服务上线cdc连接但不禁用_P档切NA档不进入驾驶模式")
    @pytest.mark.full
    def test_caseid_1979945(self):
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        self.dk.send_rke_unlock(key_id=key_id1)
        self.ck_control(self.user1, 7)
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)

        self.ipdu.propulsioncan_ecmpropfr24_gearlvrindcn_1_ecmpropsignalipdu24_gearlvrindcn2_manmodeindcn()
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "Gear", {"gear": 5})
        self.ck_control(self.user1, 1, enable=False)

    @allure.title("更新账户位置信息_删除用户_重启生效")
    @pytest.mark.sanity
    def test_caseid_1979946(self):
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetUidAccountPosition",
                                              {"infos": [self.generate_struct(self.user0),
                                                         self.generate_struct(self.user2)
                                                         ]},
                                              {"out": 1}, timeout=0.5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetUidKeyIdAccountInfo",
                                              {"infos": [{"keyId": self.user0['keyId'],
                                                          "uid": self.user0['uid']},
                                                         {"keyId": self.user2['keyId'],
                                                          "uid": self.user2['uid']},
                                                         ]
                                               }, {"out": 1}, timeout=0.5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetCurrentLoginStatus",
                                              {"sts": {"uid": self.user0['uid']}}, {"out": 1}, timeout=0.2)

        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        self.dk.send_rke_unlock(key_id=key_id1)
        self.ck_control(self.user0, 7)

    @allure.title("更新账户位置信息_更新座椅位置_下电记忆")
    @pytest.mark.sanity
    def test_caseid_1980029(self):
        self.user01 = {"uid": "00000000",
                       "keyId": ["101112131415161718191a1b1c1d1e3f"],  # key_id4
                       "isEnable": True,
                       "drive_seat_position": {"backAngle": 30,
                                               "longitudinalPosition": 31.0,
                                               "verticalPosition": 45.0,
                                               "LegrestVerticalPosition": 18.0},
                       "drive_steer_position": {"angle": 2.0,
                                                "length": 20.0},
                       "easy_seat_position": {"backAngle": 30,
                                              "longitudinalPosition": 75.0,
                                              "verticalPosition": 85.0,
                                              "LegrestVerticalPosition": 60.0},
                       "easy_steer_position": {"angle": 1.0,
                                               "length": -20.0}
                       }
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetUidAccountPosition",
                                              {"infos": [self.generate_struct(self.user01),
                                                         self.generate_struct(self.user1),
                                                         self.generate_struct(self.user2)
                                                         ]},
                                              {"out": 1}, timeout=0.5)
        
        sleep(3)
        self.dk.set_chassis_service_gear("GearP")
        self.bgm_power_off_and_on()
        self.partner.empty_all(1)
        self.dk.send_nfc_cmd(key_id=key_id4)
        self.partner.wait_for_service_reconnect(CENTRALLOCK_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", 
                                  {"info": {"sts": 1, "triggerId": 12, "updateEve": False}})
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT)
        self.ck_control(self.user01, 7)

    @allure.title("更新账户位置信息_uid找不到用户信息_使用历史用户信息_当前上电周期即生效_下电记忆")
    @pytest.mark.full
    def test_caseid_1979949(self):
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetUidAccountPosition",
                                              {"infos": [self.generate_struct(self.user0),
                                                         self.generate_struct(self.user2)
                                                         ]},
                                              {"out": 1}, timeout=0.5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetCurrentLoginStatus",
                                              {"sts": {"uid": self.user0['uid']}}, {"out": 1}, timeout=0.2)
        self.set_gear("GearP")
        self.dk.send_nfc_cmd(key_id=key_id1)
        self.ck_control(self.user0, 7)  # 解锁会主动切换当前用户，但是数据库找不到，因此数据库变成默认用户

        self.dk.set_cenlock_sts(3)
        sleep(20)
        self.bgm_power_off_and_on()
        self.partner.empty_all(1)
        self.dk.send_nfc_cmd(key_id=key_id1)
        self.partner.wait_for_service_reconnect(CENTRALLOCK_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", 
                                  {"info": {"sts": 1, "triggerId": 12, "updateEve": False}})
        self.ck_control(self.user_default, 7)

    @allure.title(
        "更新账户位置信息_当前用户和历史用户均位置信息找不到_使用默认用户位置信息_重启生效")
    @pytest.mark.full
    def test_caseid_1979963(self):
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetUidAccountPosition",
                                              {"infos": [self.generate_struct(self.user0),
                                                         self.generate_struct(self.user2)
                                                         ]},
                                              {"out": 1}, timeout=0.5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetCurrentLoginStatus",
                                              {"sts": {"uid": "99999999"}}, {"out": 1}, timeout=0.2)
        self.partner.send_method_request(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": False})
        self.restart_bgm_and_wait_for_keyService()

        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                    {"status": {"value": 1, "validity": 0}})
        self.set_gear("GearP")
        self.dk.send_rke_unlock(key_id=key_id1)
        self.ck_control(self.user_default, 1)
    
    @allure.title("SetModeInhibit调用禁用_再取消禁用_BGM继续执行舒适进出")
    @pytest.mark.sanity
    def test_caseid_1980532(self):
        self.restart_bgm_and_wait_for_keyService()
        #重启场景对挡位性能无要求，保证挡位信号发送成功
        sleep(2)
        self.set_gear("GearP")
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 0}, cycle_time=1)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": False},
                                              {"out": 0}, cycle_time=1)
        self.dk.send_rke_unlock(key_id=key_id2)
        self.ck_control(self.user2, 1)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 1})
        
    @allure.title("蓝牙状态为迎宾_解锁休眠到解锁唤醒场景")
    @pytest.mark.full
    def test_caseid_1984753(self):
        self.dk.send_rke_unlock(key_id1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {'infos': [{"key": 2, "value": 1}]})
        self.partner.empty_all(1)
        self.dk.send_approach_light_cmd(key_type=3, key_id=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
        sleep(1)
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyId",
                                  {"info": {"type": 3, "trigger": 1,
                                            "keyId": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}})
        sleep(5)
        self.restart_bgm_and_connect_service(CENTRALLOCK_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", 
                                  {"info": {"sts": 1}})
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 0}, cycle_time=1)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": True})

        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": False},
                                              {"out": 0}, cycle_time=1)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})

    @allure.title("启动后5s内蓝牙解锁进入舒适进出_非上一个用户_Active_P挡_刹车未踩下")
    @pytest.mark.sanity
    def test_caseid_1988982(self):
        self.sd_tester.change_usage_mode(0xD)
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        self.dk.send_nfc_cmd(key_id=key_id1)
        assert self.partner.partner_infos[ERGONOMICS_SERVICE_CLIENT].service_status == "OFFLINE"
        
        self.ck_control(self.user1, 7)

        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 7})
        
    @allure.title("启动后5s内蓝牙解锁进入舒适进出_上一个用户_Active_P挡_刹车未踩下")
    @pytest.mark.sanity
    def test_caseid_1988983(self):
        self.sd_tester.change_usage_mode(0xD)
        self.restart_bgm_and_wait_for_keyService()
        self.set_gear("GearP")
        self.dk.send_nfc_cmd(key_id=key_id4)
        assert self.partner.partner_infos[ERGONOMICS_SERVICE_CLIENT].service_status == "OFFLINE"
        
        self.ck_control(self.user0, 7)
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 7})
        