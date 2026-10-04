#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_peps_baseclass.py
@Time         :2022/11/24 13:56:21
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import allure
import pytest
import time
from time import sleep

from xat_ecu.legacy.sdk.digital_key.digital_key_const import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding, logger
from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.digital_key_s2s import *
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey
from groot2.cloud.biz.digital_key.manager import DigitalKeyManager
from xat_ecu.legacy.sdk.driver.jidutest_io.io.io_system import IOSystem
from xat_ecu.api.common.common import Gear


def format_assert_log(sts_name, current_key, expect_key, mapping={}):
    """格式化assert的打印信息"""
    return f"{time.time()}--当前{sts_name}为{current_key}: {mapping.get(current_key, '')}, 不满足预期{expect_key}: {mapping.get(expect_key, '')}"


class TestDigitalKey(TestBase):
    """数字钥匙测试用例类"""

    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        partner_process_check()

        self.io = IOSystem(self.tc_config)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        # self.tsp = DigitalKeyManager(self.tc_config.get('vid'),
        #                              self.tc_config.get('tel'),
        #                              "jiduapp/0.9.3 (iOS; 16.0; apple; jdcomiphone; iPhone 12; NULL; BF983636-D3F2-4805-90B4-77C3DC75D433; aVBob25l)",
        #                              uid = self.tc_config.get('uid'))
        self.partner = DigitalKeyPartner([("KeyService", "client"),
                                          ("RPAAPAService", "server"),
                                          ("TailGateService", "client"),
                                          ("CentralLockService", "client"),
                                          ("RKECtrlService", "client")
                                          ])
        self.partner.register_callback(RPAAPA_SERVICE_SERVER, self.partner.on_GetAPAStatus)
        self.ipdu.start_all_time_control()
        self.busapp.start_all_cyclic_msg()
        self.doip = Sd_Tester(**self.tc_config)
        self.doip.update_serverdoipid(0x1002)
        self.doip.diagnostic_client_sim_start()

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        logger.info("--------------->基础类test_digital_key_baseclass中after_each_func")
        self.doip.diagnostic_client_sim_close()
        self.dk.stop_listen_dk_bgm_response()
        self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
        self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        logger.info("---------------->基础类test_digital_key_baseclass中:before_each_func")
        logger.info(f"设置EntityKeyWhiteListVersw为{self.dk.last_sync_time_entity}")
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'EntityKeyWhiteListVers', self.dk.last_sync_time_entity)
        logger.info(f"BLESlotKeyWhiteListVers{self.dk.last_sync_time_ble}")
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BLESlotKeyWhiteListVers', self.dk.last_sync_time_ble)

        logger.info("设置车辆为静止状态,测试为0,挡位为P，电子手刹拉起")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3') #设置车辆静止
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0) #车速设为0
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3) # 车速值有效
        self.set_gear_pos(gear=Gear.Park) #设置挡位为P
        # self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd') #设置电子手刹
        # self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn') #挡位设为P挡

        logger.info("设置车内没有检测到钥匙")
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEKeyPrsntStsZone7', 'Validity_NotValid') #设置车内没有检测到钥匙

        logger.info("设置五个座椅没有占位")
        self.dk.set_drvr_seat_notpresent()
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()

        sleep(0.5)
        logger.info("UsageMode 为Abandoned，CarMode为Normal")
        self.set_usage_mode(0)
        self.set_car_mode(0)

        logger.info("重置钥匙信息, 当前任何区域无钥匙")
        self.dk.reset_bncm_digital_keyinfo()

        logger.info("设置初始化的CCP：94: 0x80, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x4, 578: 0x4")
        self.write_ccp({94: 0x80, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x4, 578: 0x4})

        logger.info("先恢复5门关门状态，主驾无人，车门按钮未按下,刹车释放,诊断激活线连接，设置bodycan上五个电动门均关闭")
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.nucapp.bgm_diag_line_up()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        logger.info("清除数字钥匙中接收的数据缓存")
        self.dk.empty_dk_data_queue() #清除数字钥匙中接收的数据缓存
        logger.info("设置PE解锁时对应寻钥匙关闭")
        self.set_config_info(5, 0)

    def after_each_func(self, ecu):
        if ecu.get("testresult") != "Pass":
            logger.info("case失败，需等待10s让环境恢复")
            sleep(10)
        else:
            sleep(3)  # 防止触发解闭锁防玩
        super().after_each_func(ecu, start=False)

    def set_usage_mode(self, mode: int, need_exit=False, auto_ack_tsp_req=True):
        """
        切换usage mode为XX
        :param : 0x0: 'ABANDONED', 0x1: 'INACTIVE', 0x2: 'CONVENIENCE', 0x11: 'ACTIVE', 0x13: 'DRIVING'
        :param : need_exit: 是否退出IO控制
        :return:
        """
        with allure.step(f"设置usage mode: {usage_mode_desc[mode]}"):
            self.doip.change_usage_mode(mode, need_exit)
            sleep(0.5)  # 确保S2S notify给订阅方

    def set_car_mode(self, mode: int):
        """
        切换car mode为XX
        :param : 0x0: 'NORMAL', 0x1: 'TRANSPORT', 0x2: 'FACTORY', 0x3: 'CRASH', 0x5: 'DYNO'
        """
        with allure.step(f"设置usage mode: {car_mode_desc[mode]}"):
            self.doip.change_car_mode(mode)

    def write_ccp(self, ccp_dict: dict):
        """写ccp， 例如{94: 0x80, 98: 0x2, 10: 0x2}"""
        with allure.step(f"配置ccp: {ccp_dict}"):
            self.doip.write_multi_ccp(ccp_dict)
            time.sleep(0.5)

    def set_config_info(self, key, value):
        """
        配置单个数字钥匙approach功能
        :param key: 功能代号         @value(0)     kAutoLockOnLeave;\n
                                     @value(1)     kAutoUnLockOnApproach;\n
                                    @value(2)     kLightOnApproache;\n
                                    @value(3)     kDoorAutoOpenOnUnlock;\n
                                    @value(4)     kWindowAutoCloseOnLock;\n
                                    @value(5)     kSetPEKeySearchDedicateZone       //设置PE解锁时对应寻钥匙的区域
        :param value: 配置生效与否   @value(0)     kConfigOff;\n
                                    @value(1)     kConfigOn;\n
                      离车上锁配置   @value(0)     kAutoLockOnLeaveOff;\n
                                    @value(1)     kOnWithoutAnyDoorClose;\n
                                    @value(2)     kOnWithDriverDoorClose;\n
                                    @value(3)     kOnWithAllDoorClose
        :return:
        """
        key_desc = {0: 'kAutoLockOnLeave', 1: 'kAutoLockOnApproach',
                    2: 'kLightOnApproache', 3: 'kDoorAutoOpenOnUnlock', 4: 'kWindowAutoCloseOnLock',
                    5: 'kSetPEKeySearchDedicateZone'}
        value_desc = {0: 'kConfigOff', 1: 'kConfigOn'}
        walk_away_unlocking_desc = {0: 'kAutoLockOnLeaveOff', 1: 'kOnWithoutAnyDoorClose',
                                    2: 'kOnWithDriverDoorClose', 3: 'kOnWithAllDoorClose'}
        if key == 0:
            desc = f"设置{key_desc[key]} = {walk_away_unlocking_desc[value]}"
        else:
            desc = f"设置{key_desc[key]} = {value_desc[value]}"
        with allure.step(desc):
            args = {'infos': [{"key": key, "value": value}]}
            self.partner.send_method_request("KeyService_client", "SetConfigInfo", args)
            logger.info("SetConfigInfo", args)

    def ck_pnc23(self, sts):
        """校验PNC23 valid: 1 or invalid: 0，当前接口固定使用connectivity CanFd"""
        # self.nm.ck_pnc(23, sts)
        return  # todo: 当前RVS在非Abandoned时都会拉PNC23
        self.dk.can_bus_connectivity.ck_signal(self.ipdu.connectivitycanfd.BgmConnectivityCANNmFr, "PNC23_BGM", sts,
                                               timeout=2)

    def ck_pnc24(self, sts, timeout=2):
        """校验PNC24 valid: 1 or invalid: 0，当前接口固定使用connectivity CanFd"""
        st = time.time()
        while time.time() - st < timeout:
            pdu = self.ipdu.recv_pdu("connectivitycanfd", 0x533, 0.02)  # 快发的周期20ms
            print(pdu)
            if pdu is None:
                continue
            if pdu[3][3] & 1 == sts:
                return True
        else:
            assert f"{timeout}s内PNC24不为{sts}"

    def ck_key_service_unlock_event(self, keyid: list, key_type: int, trigger: int):
        """
        校验S2S_KeyService上报解锁事件
        :param keyid: 指示Key ID，占16个字节
        :param key_type: 钥匙类型
        :param trigger: 指示Key ID更新的事件类型
        :return:
        """
        with allure.step(f"校验有解锁事件上报, keyid: {keyid}, type: {key_type}, trigger: {trigger}"):
            self.partner.ck_s2s_event("KeyService_client", "DigitalKeyId",
                                      {"info": {"keyId": DataTypeHanding.to_bytes(keyid),
                                                "trigger": trigger,
                                                "type": key_type}})

    
    def set_gear_pos(self, gear: Gear):
        prompt_info = f"----------> 设置车辆挡位为:{gear.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', gear.value)
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr07, 'GearLvrIndcn', gear.value)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', gear.value)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 1)

    
    # def update_keyinfos_for_search_all_location(self,find_loc:Union[Location, int], keys: List[KeyInfo]):

    #     # update_keyinfos(self, location: Union[Location, int], keys: List[KeyInfo]):