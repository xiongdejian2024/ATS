#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_comfortable_access.py
@Time         :2024/1/16
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
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.sdk.sdk_tools import *

global_list1 = []
global_list2 = []
global_list3 = []
@allure.feature("性能稳定性")
@allure.story("业务稳定性/启动场景压测-舒适进出")
@pytest.mark.soa
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
                                     ("SeatService", "client"),
                                     DOOR_SERVICE_CLIENT
                                     ])
        self.sd_tester.write_single_ccp(950, 1)
        # 配置PE寻钥匙区域2
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 5, "value": 0}]})

        self.curr_drvr_height = 0.0
        self.curr_drvr_back_angle = 0.0
        self.curr_drvr_longitudinal = 0.0
        self.curr_drvr_cushion = 0.0
        self.curr_steer_angle = 0.0  # -3~3
        self.curr_steer_length = 0.0  # -25~30

        self.user0 = {"uid": "00000000",
                      "keyId": ["101112131415161718191a1b1c1d1e3f"],  # key_id4
                      "isEnable": True,
                      "drive_seat_position": {"backAngle": 20,
                                              "longitudinalPosition": 30.0,
                                              "verticalPosition": 40.0,
                                              "LegrestVerticalPosition": 8.0},
                      "drive_steer_position": {"angle": 3.0,
                                               "length": 30.0},
                      "easy_seat_position": {"backAngle": 60,
                                             "longitudinalPosition": 35.0,
                                             "verticalPosition": 35.0,
                                             "LegrestVerticalPosition": 60.0},
                      "easy_steer_position": {"angle": 2.0,
                                              "length": -10.0}
                      }

        self.user1 = {"uid": "12345678",
                      "keyId": ["000102030405060708090a0b0c0d0e0f"],  # key_id1
                      "isEnable": True,
                      "drive_seat_position": {"backAngle": 40,
                                              "longitudinalPosition": 20.0,
                                              "verticalPosition": 10.0,
                                              "LegrestVerticalPosition": 70.0},
                      "drive_steer_position": {"angle": 2.7,
                                               "length": 22.0},
                      "easy_seat_position": {"backAngle": 55,
                                             "longitudinalPosition": 45.0,
                                             "verticalPosition": 24.0,
                                             "LegrestVerticalPosition": 15.0},
                      "easy_steer_position": {"angle": 1.0,
                                              "length": 15.0}
                      }

        self.user2 = {"uid": "87654321",
                      "keyId": ["101112131415161718191a1b1c1d1e1f"],  # key_id2
                      "isEnable": False,
                      "drive_seat_position": {"backAngle": 40,
                                              "longitudinalPosition": 7.0,
                                              "verticalPosition": 80.0,
                                              "LegrestVerticalPosition": 90.0},
                      "drive_steer_position": {"angle": 1.5,
                                               "length": 19.0},
                      "easy_seat_position": {"backAngle": 10,
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
        
        global global_list1
        global global_list2
        global global_list3
        if len(global_list1)==0:
            global_list1 = [0]
        if len(global_list2)==0:
            global_list2 = [0]
        if len(global_list3)==0:
            global_list3 = [0]
        average_value1 = sum(global_list1) / len(global_list1)
        average_value2 = sum(global_list2) / len(global_list2)
        average_value3 = sum(global_list3) / len(global_list3)
        logger.info(f"global_list1 ={global_list1},average_value1 = {average_value1}")
        logger.info(f"global_list2 ={global_list2},average_value2 = {average_value2}")
        logger.info(f"global_list3 ={global_list3},average_value3 = {average_value3}")

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
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1) # MPU侧档位
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
                                              {"out": 1})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetUidKeyIdAccountInfo",
                                              {"infos": [{"keyId": self.user0['keyId'],
                                                          "uid": self.user0['uid']},
                                                         {"keyId": self.user1['keyId'],
                                                          "uid": self.user1['uid']},
                                                         {"keyId": self.user2['keyId'],
                                                          "uid": self.user2['uid']},
                                                         ]
                                               }, {"out": 1})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetCurrentLoginStatus",
                                              {"sts": {"uid": self.user0['uid']}}, {"out": 1})
        self.partner.send_method_request(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": False})

        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)  # 刹车踏板未踩下
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 1)  # 座椅可调前置条件
        self.set_drvr_belt_unlock()  # 安全带未系
        self.dk.set_cenlock_sts(3)  # 整车闭锁

        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosFrntHeiQF', 3)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatPosPercSeatPosSldQF', 3)

        self.set_drvr_height(20.0)  # 高度和靠背角度是一个电机，先高度，再角度
        self.set_drvr_back_angle(100.0)

        self.set_drvr_longitudinal(20.0)  # 前后和坐垫高度是一个电机，先前后，再坐垫高度
        self.set_drvr_cushion(20.0)

        self.set_steer_position(0.0, 0.0)  # 角度和长度是一个电机，先角度，再高度
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])  # 踩刹车寻钥匙可以找到钥匙
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, 'StopMoveDirection', 
                                         {"id": 0, "part": 0, "direction": 0})
        self.partner.empty_all(10)

    def after_each_func(self, ecu):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)  # 刹车踏板未踩下
        super().after_each_func(ecu, start=False)

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
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'BackRestAdjmtRowFirstDrvr', 2, timeout=1)
                self.set_drvr_back_angle(exp_angle)
        elif self.curr_drvr_back_angle - exp_angle > 2:
            if control_enable:
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'BackRestAdjmtRowFirstDrvr', 1, timeout=1)
                self.set_drvr_back_angle(exp_angle)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'BackRestAdjmtRowFirstDrvr', 0, timeout=1.5)

    def ck_seat_height_control(self, exp_height, control_enable):
        """校验座椅高度控制"""
        if exp_height - self.curr_drvr_height > 2:  # 百分比增大>>100%，座椅上Up
            if control_enable:
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatHeiAdjmtRowFirstDrvr', 1, timeout=7) # 启动后8s如果没有控制则说明控制失败或性能不足
                self.set_drvr_height(exp_height)
        elif self.curr_drvr_height - exp_height > 2:
            if control_enable:
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatHeiAdjmtRowFirstDrvr', 2, timeout=7)
                self.set_drvr_height(exp_height)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatHeiAdjmtRowFirstDrvr', 0, timeout=7)

    def ck_seat_longitudinal_control(self, exp_longitudinal, control_enable):
        """校验座椅前后控制"""
        if exp_longitudinal - self.curr_drvr_longitudinal > 2:  # 百分比增大>>100%，座椅前Forward
            if control_enable:
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstDrvr', 1, timeout=7)
                self.set_drvr_longitudinal(exp_longitudinal)
        elif self.curr_drvr_longitudinal - exp_longitudinal > 2:
            if control_enable:
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstDrvr', 2, timeout=7)
                self.set_drvr_longitudinal(exp_longitudinal)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstDrvr', 0, timeout=7)

    def ck_seat_cushion_control(self, exp_cushion, control_enable):
        """校验座椅坐垫/腿托控制"""
        if exp_cushion - self.curr_drvr_cushion > 3:  # 百分比增大>>100%，坐垫上Up
            if control_enable:
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatCushTiltAdjmtRowFirstDrvr', 1, timeout=1)
                self.set_drvr_cushion(exp_cushion)
        elif self.curr_drvr_cushion - exp_cushion > 3:
            if control_enable:
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatCushTiltAdjmtRowFirstDrvr', 2, timeout=1)
                self.set_drvr_cushion(exp_cushion)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatCushTiltAdjmtRowFirstDrvr', 0, timeout=1.5)

    def ck_steer_angle_control(self, exp_angle, control_enable):
        """
        校验方向盘角度控制
        @param exp_angle: 预期控制角度，float
        @param control_enable: 是否控制，舒适进出可能不控制
        """
        if abs(self.curr_steer_angle - exp_angle) > 0.13 and control_enable:  # 至少差0.13(对应总线值13)才会触发控制
            if self.curr_steer_angle > exp_angle:  # 角度增加>>-3，Up
                self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtUpSts', 1, timeout=1)
            else:
                self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtDwnSts', 1, timeout=1)
            self.set_steer_position(angle=exp_angle)
        self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtUpSts', 0, timeout=1.5)
        self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtDwnSts', 0, timeout=1)

    def ck_steer_length_control(self, exp_length, control_enable):
        """
        校验方向盘长度控制
        @param exp_length: 预期控制长度，float
        @param control_enable: 是否控制，舒适进出可能不控制
        """
        if abs(self.curr_steer_length - exp_length) > 1.3 and control_enable:  # 应该至少差1.3(对应总线值差13)才会触发控制
            if self.curr_steer_length < exp_length:  # 长度增加>>30，Backward   
                self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtBackSts', 1, timeout=1)
            else:
                self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 1, timeout=1)
            self.set_steer_position(length=exp_length)
        self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtUpSts', 0, timeout=1.5)
        self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr06, 'SteerAdjSwtFwdSts', 0, timeout=1)

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
            angle_can_signal = round((angle + 3.3375) / 0.0125)
            self.ipdu.set(self.ipdu.cem_lin4.AswmCem_Lin4Fr02, 'SteerWhlPosnAng', angle_can_signal)
            self.curr_steer_angle = angle
            hint += f"设置方向盘角度{angle}--总线值{angle_can_signal}"
        if length is not None:
            length_can_signal = round((length + 27.8) / 0.1)
            self.ipdu.set(self.ipdu.cem_lin4.AswmCem_Lin4Fr02, 'SteerWhlPosnX', length_can_signal)
            self.curr_steer_length = length
            hint += f" 设置方向盘长度{length}--总线值{length_can_signal}"
        logger.info(hint)

    def set_drvr_belt_unlock(self):
        """设置主驾安全带未系"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', 0)

    @allure.title("启动场景NFC解锁触发舒适进入_压测100次")
    @pytest.mark.sanity
    @pytest.mark.repeat(100)
    def test_caseid_1984003(self):
        self.dk.set_chassis_service_gear("GearP")
        self.ipdu.pause_all_bus_send()
        self.bgm_power_off_and_on()
        self.ipdu.resume_all_bus_send()
        self.partner.empty_all(1)
        try:
            self.dk.ck_cenlock_sts(3)
        except Exception as e:
            logger.info(f"锁状态没有存住，但不影响本件测试")
            return
        self.dk.send_nfc_cmd(key_id1)
        self.ck_control(self.user1, 7)
        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                              {"out": 7})

    @allure.title("启动场景RKE解锁触发舒适进入_压测100次")
    @pytest.mark.sanity
    @pytest.mark.repeat(100)
    def test_caseid_1984004(self):
        self.dk.set_chassis_service_gear("GearP")
        self.ipdu.pause_all_bus_send()
        self.bgm_power_off_and_on()
        self.ipdu.resume_all_bus_send()
        self.partner.empty_all(1)
        try:
            self.dk.ck_cenlock_sts(3)
        except Exception as e:
            logger.info(f"锁状态没有存住，但不影响本件测试")
            return
        self.dk.send_rke_unlock(key_id=key_id1)
        self.dk.ck_cenlock_sts(1,timeout =7)
        self.ck_control(self.user1, 7)

        self.partner.wait_for_service_reconnect(ERGONOMICS_SERVICE_CLIENT, timeout=5)
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "GetModeInhibitSts", {}, {"out": False})
        self.partner.send_request_and_ck_resp(ERGONOMICS_SERVICE_CLIENT, "SetModeInhibit", {"isInhibit": True},
                                            {"out": 7})
       
    @allure.title("启动场景NFC解锁触发舒适进入_7s内可控压测")
    @pytest.mark.sanity
    @pytest.mark.repeat(100)
    def test_caseid_1988838(self):
        global global_list1
        self.dk.set_chassis_service_gear("GearP")
        self.bgm_power_off_and_on(timeout=0)
        self.ipdu.check_PNC("connectivitycanfd", 0x533, 'PNC25_BGM', 1, timeout=1)
        t1 = time.time()
        try:
            self.dk.ck_cenlock_sts(3)
        except Exception as e:
            logger.info(f"锁状态没有存住，但不影响本件测试")
            return
        self.dk.send_nfc_cmd(key_id1)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstDrvr', 1, timeout=20)
        t2 = time.time()
        t = t2 - t1
        global_list1.append(t)
        logger.info(f"t1 = {t1},t2 = {t2},t = {t},")
        assert t < 7.1
        
    @allure.title("启动场景RKE解锁触发舒适进入_7s内可控压测")
    @pytest.mark.sanity
    @pytest.mark.repeat(100)
    def test_caseid_1988839(self):
        global global_list2
        self.dk.set_chassis_service_gear("GearP")
        self.bgm_power_off_and_on(timeout=0)
        self.ipdu.check_PNC("connectivitycanfd", 0x533, 'PNC25_BGM', 1, timeout=1)
        t1 = time.time()
        try:
            self.dk.ck_cenlock_sts(3)
        except Exception as e:
            logger.info(f"锁状态没有存住，但不影响本件测试")
            return
        self.dk.send_rke_unlock(key_id=key_id1)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstDrvr', 1, timeout=20)
        t2 = time.time()
        t = t2 - t1
        global_list2.append(t)
        logger.info(f"t1 = {t1},t2 = {t2},t = {t},")
        assert t < 7.1
        
    @allure.title("启动场景PE解锁触发舒适进入_7s内可控压测")
    @pytest.mark.sanity
    @pytest.mark.repeat(100)
    def test_caseid_1988894(self):
        global global_list3
        self.dk.set_chassis_service_gear("GearP")
        self.bgm_power_off_and_on(timeout=0)
        self.ipdu.check_PNC("connectivitycanfd", 0x533, 'PNC25_BGM', 1, timeout=1)
        t1 = time.time()
        try:
            self.dk.ck_cenlock_sts(3)
        except Exception as e:
            logger.info(f"锁状态没有存住，但不影响本件测试")
            return
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.press_door_outswitch(4, 0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstDrvr', 1, timeout=20)
        t2 = time.time()
        t = t2 - t1
        global_list3.append(t)
        logger.info(f"t1 = {t1},t2 = {t2},t = {t},")
        assert t < 7.1