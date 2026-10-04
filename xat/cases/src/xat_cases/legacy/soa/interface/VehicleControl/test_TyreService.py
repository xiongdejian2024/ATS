#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_TyreService.py
@Time         :2023/04/08 17:20:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import allure
import pytest
import math
from time import sleep
from random import randint
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import *


class MockMcuCddTyre:
    def __init__(self, ipdu):
        self.ipdu = ipdu
        self.tyre_msg_map = {0: 'LeFrntTireMsg', 1: 'RiFrntTireMsg', 2: 'LeReTireMsg', 3: 'RiReTireMsg'}
        self.sensor0_temp = 0
        self.sensor1_temp = 0
        self.sensor2_temp = 0
        self.sensor3_temp = 0
        self.sensor0_pressure = 0
        self.sensor1_pressure = 0
        self.sensor2_pressure = 0
        self.sensor3_pressure = 0
        self.sensor_pressure_map = {0: self.sensor0_pressure, 1: self.sensor1_pressure,
                                    3: self.sensor3_pressure, 2: self.sensor2_pressure}
        self.sensor_temp_map = {0: self.sensor0_temp, 1: self.sensor1_temp,
                                3: self.sensor3_temp, 2: self.sensor2_temp}

    def set_pressure(self, tyre_id, pressure):
        """
        设置指定轮胎的胎压
        @param tyre_id: 0:左前，1右前，3:右后，2：左后
        @param pressure: hex的胎压数据，乘1.373后为服务接口中的数据
        """
        logger.info(f"设置tyre{tyre_id}={pressure}kpa")
        hex_pressure = math.ceil(pressure / 1.373)
        if tyre_id == 0:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, 'LeFrntTireMsgP',(hex_pressure))
            self.sensor0_pressure = hex_pressure * 1.373
        elif tyre_id == 1:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, 'RiFrntTireMsgP',(hex_pressure))
            self.sensor1_pressure = hex_pressure * 1.373
        elif tyre_id == 2:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, 'LeReTireMsgP',(hex_pressure))
            self.sensor2_pressure = hex_pressure * 1.373
        elif tyre_id == 3:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, 'RiReTireMsgP',(hex_pressure))
            self.sensor3_pressure = hex_pressure * 1.373
        self.sensor_pressure_map = {0: self.sensor0_pressure, 1: self.sensor1_pressure,
                                    3: self.sensor3_pressure, 2: self.sensor2_pressure}

    def set_temperature(self, tyre_id, temperature):
        """
        设置指定轮胎的胎压
        @param tyre_id: 0:左前，1右前，3:右后，2：左后
        @param temperature: 换算后的真实胎温
        """
        logger.info(f"设置tyre{tyre_id}={temperature}摄氏度")
        if tyre_id == 0:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, 'LeFrntTireMsgT',(temperature + 50))
            self.sensor0_temp = temperature
        elif tyre_id == 1:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, 'RiFrntTireMsgT',(temperature + 50))
            self.sensor1_temp = temperature
        elif tyre_id == 2:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, 'LeReTireMsgT',(temperature + 50))
            self.sensor2_temp = temperature
        elif tyre_id == 3:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, 'RiReTireMsgT',(temperature + 50))
            self.sensor3_temp = temperature
        self.sensor_temp_map = {0: self.sensor0_temp, 1: self.sensor1_temp,
                                3: self.sensor3_temp, 2: self.sensor2_temp}

    def set_PWarnFlg(self, tyre_id, PWarnFlg):
        """
        设置指定轮胎的胎压低告警状态
        @param tyre_id: 0:左前，1右前，3:右后，2：左后
        @param PWarnFlg: 0：Normal, 1: lowpressure， 2：highpressure, 3: reverse
        """
        logger.info(f"设置tyre{tyre_id}::PWarnFlg={PWarnFlg}")
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, f'{self.tyre_msg_map[tyre_id]}PWarnFlg', PWarnFlg)

    def set_TWarnFlg(self, tyre_id, TWarnFlg):
        """
        设置指定轮胎的胎温高告警状态
        @param tyre_id: 0:左前，1右前，3:右后，2：左后
        @param TWarnFlg: 0：Normal, 1: warnning
        """
        logger.info(f"设置tyre{tyre_id}::TWarnFlg={TWarnFlg}")
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, f'{self.tyre_msg_map[tyre_id]}TWarnFlg', TWarnFlg)

    def set_BattLoSt(self, tyre_id, BattLoSt):
        """
        设置指定轮胎的低电量状态
        @param tyre_id: 0:左前，1右前，3:右后，2：左后
        @param BattLoSt: 0：Normal, 1: warning
        """
        logger.info(f"设置tyre{tyre_id}::BattLoSt={BattLoSt}")
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, f'{self.tyre_msg_map[tyre_id]}BattLoSt', BattLoSt)

    def set_FastLoseWarnFlg(self, tyre_id, FastLoseWarnFlg):
        """
        设置指定轮胎的快速漏气状态
        @param tyre_id: 0:左前，1右前，3:右后，2：左后
        @param FastLoseWarnFlg: 0：Normal, 1: warning
        """
        logger.info(f"设置tyre{tyre_id}::FastLoseWarnFlg={FastLoseWarnFlg}")
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, f'{self.tyre_msg_map[tyre_id]}FastLoseWarnFlg',
                      FastLoseWarnFlg)

    def set_MsgOldFlg(self, tyre_id, MsgOldFlg):
        """
        设置指定轮胎的胎压
        @param tyre_id: 0:左前，1右前，3:右后，2：左后
        @param MsgOldFlg: 0：Normal, 1: warning
        """
        logger.info(f"设置tyre{tyre_id}::MsgOldFlg={MsgOldFlg}")
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, f'{self.tyre_msg_map[tyre_id]}MsgOldFlg', MsgOldFlg)

    def set_SysWarnFlg(self, tyre_id, SysWarnFlg):
        """
        设置指定轮胎的胎压
        @param tyre_id: 0:左前，1右前，3:右后，2：左后
        @param SysWarnFlg: 0：Normal, 1: warning
        """
        logger.info(f"设置tyre{tyre_id}::SysWarnFlg={SysWarnFlg}")
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, f'{self.tyre_msg_map[tyre_id]}SysWarnFlg', SysWarnFlg)


@allure.feature("SOA服务接口")
@allure.story("整车控制/TyreService")
@pytest.mark.wjj
class TestTyreService(TestBase):

    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.mockmcu = MockMcuCddTyre(self.ipdu)
        self.partner = S2sBaseClass([TYRE_SERVICE_CLIENT])
        self.partner.wait_for_service_reconnect(TYRE_SERVICE_CLIENT)

    def after_class(self, ecu):
        try:
            self.partner.stop_operators()
        except Exception as e:
            logger.error(f"{str(e)}")
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        for i in range(4):
            self.mockmcu.set_temperature(i, 25)
            self.mockmcu.set_pressure(i, 260.0)
            self.mockmcu.set_PWarnFlg(i, 0)
            self.mockmcu.set_TWarnFlg(i, 0)
            self.mockmcu.set_FastLoseWarnFlg(i, 0)
            self.mockmcu.set_MsgOldFlg(i, 0)
            self.mockmcu.set_SysWarnFlg(i, 0)
            self.mockmcu.set_BattLoSt(i, 0)
        self.partner.empty_all(1)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def ck_faultinfo(self, fault_info, tyre_id, timeout=3):
        """校验轮胎故障信息"""
        self.partner.ck_s2s_event(TYRE_SERVICE_CLIENT, "TyreFault", {"faults": fault_info}, timeout=timeout)
        self.partner.send_request_and_ck_resp(TYRE_SERVICE_CLIENT, "GetFaultInfo", {}, {"out": fault_info})
        if tyre_id == 4:
            tyre_infos = [{"id": i,
                           "pressure": self.mockmcu.sensor_pressure_map[i],
                           "temperature": self.mockmcu.sensor_temp_map[i],
                           "fault": [fault_info[0]['fault']]} for i in range(4)]
        else:
            tyre_infos = [{"id": tyre_id,
                           "pressure": self.mockmcu.sensor_pressure_map[tyre_id],
                           "temperature": self.mockmcu.sensor_temp_map[tyre_id],
                           "fault": [x["fault"] for x in fault_info]}
                          ]
        self.partner.send_request_and_ck_resp(TYRE_SERVICE_CLIENT, "GetTyreInfo", {"tyres": [tyre_id]},
                                              {"out": tyre_infos})             
                
    @allure.title("获取左前胎胎压信息_kTyreFrontLeft_AllTyrePressureinfo")
    @allure.title("获取右前胎胎压信息_kTyreFrontRight_AllTyrePressureinfo")
    @allure.title("获取左后胎胎压信息_kTyreRearLeft_AllTyrePressureinfo")
    @allure.title("获取右后胎胎压信息_kTyreRearRight_AllTyrePressureinfo")
    @pytest.mark.sanity
    def test_caseid_1985295_1985297_1985299_1985300(self):
        for tyre_id in range(4):#位置
            for p in [1, 100, 200, 350.115]:
                logger.info(f'现在胎压信息到{p},现在轮胎遍历到{tyre_id}')
                self.partner.empty_all()
                self.mockmcu.set_pressure(tyre_id, p)
                self.partner.ck_s2s_event(TYRE_SERVICE_CLIENT, "AllTyrePressure", 
                                {"infos": [{"id": tyre_id, "pressure": eval(f"self.mockmcu.sensor{tyre_id}_pressure")}]})
                self.partner.send_request_and_ck_resp(TYRE_SERVICE_CLIENT, "GetPressure", {"tyres":[tyre_id]}, {"out": 
                                            [{"id": tyre_id, "pressure": eval(f"self.mockmcu.sensor{tyre_id}_pressure")}]})

    @allure.title("获取全部胎压信息_kTyreRearRight_AllTyrePressureinfo")
    @pytest.mark.full
    def test_caseid_1985302(self):
        datas = set()
        for _ in range(11):
            datas.add((randint(0, 3), randint(1, 350)))
        for data in datas:
            tyre_id, p = data
            self.mockmcu.set_pressure(tyre_id, p)
            logger.info(f'现在遍历到{tyre_id, p}')
            self.partner.send_request_and_ck_resp(TYRE_SERVICE_CLIENT, "GetPressure", {"tyres":[4]},
                                                  {"out": 
                                            [{"id": 0, "pressure": self.mockmcu.sensor0_pressure},
                                             {"id": 1, "pressure": self.mockmcu.sensor1_pressure},
                                             {"id": 2, "pressure": self.mockmcu.sensor2_pressure},
                                             {"id": 3, "pressure": self.mockmcu.sensor3_pressure}]})
                
    @allure.title("获取左前胎胎温信息_kTyreFrontLeft_AllTyreTemperature")
    @allure.title("获取右前胎胎温信息_kTyreFrontRight_AllTyreTemperature")
    @allure.title("获取左后胎胎温信息_kTyreRearLeft_AllTyreTemperature")
    @allure.title("获取右后胎胎温信息_kTyreRearRight_AllTyreTemperature")
    @pytest.mark.sanity
    def test_caseid_1985303_1985304_1985305_1985306(self):
        for t in [-49, 100, 205]:#胎温
                logger.info(f'现在遍历到{t}')
                self.mockmcu.set_temperature(0, t)
                self.mockmcu.set_temperature(1, t)
                self.mockmcu.set_temperature(2, t)
                self.mockmcu.set_temperature(3, t)
                self.partner.ck_s2s_event(TYRE_SERVICE_CLIENT, "AllTyreTemperature", 
                                      {"infos": [{"id": 0, "temperature": t},
                                                 {"id": 1, "temperature": t},
                                                 {"id": 2, "temperature": t},
                                                 {"id": 3, "temperature": t}]},timeout=5)
                for tyre_id in range(5):#位置
                    if tyre_id !=4 :
                        self.partner.send_request_and_ck_resp(TYRE_SERVICE_CLIENT, "GetTemperature", {"tyres":[tyre_id]}, {"out": 
                                                [{"id": tyre_id, "temperature": t}]})
                    else:
                        self.partner.send_request_and_ck_resp(TYRE_SERVICE_CLIENT, "GetTemperature", {"tyres":[tyre_id]}, {"out": 
                                                [{"id": 0, "temperature": t},{"id": 1, "temperature": t},{"id": 2, "temperature": t},{"id": 3, "temperature": t}]})
    @allure.title("获取全部胎温信息")
    @pytest.mark.smoke
    def test_caseid_1985307(self):
        datas = set()
        for _ in range(11):
            datas.add((randint(0, 3), randint(-49, 205)))
        for data in datas:
            tyre_id, t = data
            self.mockmcu.set_temperature(tyre_id, t)
            logger.info(f'现在遍历到{tyre_id, t}')
            self.partner.send_request_and_ck_resp(TYRE_SERVICE_CLIENT, "GetTemperature", {"tyres":[4]},
                                                  {"out": 
                                            [{"id": 0, "temperature": self.mockmcu.sensor0_temp},
                                             {"id": 1, "temperature": self.mockmcu.sensor1_temp},
                                             {"id": 2, "temperature": self.mockmcu.sensor2_temp},
                                             {"id": 3, "temperature": self.mockmcu.sensor3_temp}]},timeout=3)


    @allure.title("获取轮胎故障信息_左前轮故障产生恢复")
    @allure.title("获取轮胎故障信息_右前轮故障产生恢复")
    @allure.title("获取轮胎故障信息_左后轮故障产生恢复")
    @allure.title("获取轮胎故障信息_右后轮故障产生恢复")
    @pytest.mark.sanity
    def test_caseid_109234_109231_109235_109241(self):
        for tyre_id in range(4):
            # 注入msgold
            self.mockmcu.set_MsgOldFlg(tyre_id, 1)
            self.ck_faultinfo([{"fault": 7, "faultMsg": "", "tyre": tyre_id}], tyre_id=tyre_id)

            # msgold恢复，连续两包恢复，无故障
            self.mockmcu.set_MsgOldFlg(tyre_id, 0)
            self.ck_faultinfo([{"fault": 0, "faultMsg": "", "tyre": 4}], tyre_id=tyre_id)

            # 注入胎温高故障，60s后报故障
            self.mockmcu.set_TWarnFlg(tyre_id, 1)
            self.ck_faultinfo([{"fault": 3, "faultMsg": "", "tyre": tyre_id}], tyre_id=tyre_id)

            # 产生快速漏气，24s报故障
            self.mockmcu.set_FastLoseWarnFlg(tyre_id, 1)
            self.ck_faultinfo([{"fault": 3, "faultMsg": "", "tyre": tyre_id},
                               {"fault": 4, "faultMsg": "", "tyre": tyre_id}], tyre_id=tyre_id)

            # 注入低压故障，10s报
            self.mockmcu.set_PWarnFlg(tyre_id, 1)
            self.ck_faultinfo([{"fault": 3, "faultMsg": "", "tyre": tyre_id},
                               {"fault": 4, "faultMsg": "", "tyre": tyre_id},
                               {"fault": 1, "faultMsg": "", "tyre": tyre_id}], tyre_id=tyre_id)
            # 注入低电量故障,10s报
            self.mockmcu.set_BattLoSt(tyre_id, 1)
            self.ck_faultinfo([{"fault": 3, "faultMsg": "", "tyre": tyre_id},
                               {"fault": 4, "faultMsg": "", "tyre": tyre_id},
                               {"fault": 1, "faultMsg": "", "tyre": tyre_id},
                               {"fault": 6, "faultMsg": "", "tyre": tyre_id}], tyre_id=tyre_id)

            # 快速漏气恢复
            self.mockmcu.set_FastLoseWarnFlg(tyre_id, 0)
            self.ck_faultinfo([{"fault": 1, "faultMsg": "", "tyre": tyre_id},
                               {"fault": 6, "faultMsg": "", "tyre": tyre_id},
                               {"fault": 3, "faultMsg": "", "tyre": tyre_id}], tyre_id=tyre_id)

            # 电量故障恢复,连续两包恢复
            self.mockmcu.set_BattLoSt(tyre_id, 0)
            self.ck_faultinfo([{"fault": 1, "faultMsg": "", "tyre": tyre_id},
                               {"fault": 3, "faultMsg": "", "tyre": tyre_id}], tyre_id=tyre_id)

            # 温度故障恢复，低压故障立即恢复，需要连续两包，因为数据跳变过大
            self.mockmcu.set_PWarnFlg(tyre_id, 0)
            self.mockmcu.set_TWarnFlg(tyre_id, 0)
            self.ck_faultinfo([{"fault": 0, "faultMsg": "", "tyre": 4}], tyre_id=tyre_id)

    @allure.title("监测胎压系统故障")
    @pytest.mark.smoke
    def test_caseid_109237(self):
        for i in range(4):
            self.mockmcu.set_SysWarnFlg(i, 1)
        self.ck_faultinfo([{"fault": 5, "faultMsg": "", "tyre": 0},
                           {"fault": 5, "faultMsg": "", "tyre": 1},
                           {"fault": 5, "faultMsg": "", "tyre": 2},
                           {"fault": 5, "faultMsg": "", "tyre": 3}], 4)

        for i in range(4):
            self.mockmcu.set_SysWarnFlg(i, 0)
        self.ck_faultinfo([{"fault": 0, "faultMsg": "", "tyre": 4}], 4)

    @allure.title("获取轮胎故障信息_左前低压故障产生恢复")
    @allure.title("获取轮胎故障信息_右前低压故障产生恢复")
    @allure.title("获取轮胎故障信息_左后低压故障产生恢复")
    @allure.title("获取轮胎故障信息_右后低压故障产生恢复")
    @pytest.mark.full
    def test_caseid_1959964_1959965_1959966_1959967(self):
        for tyre_id in range(4):
            self.mockmcu.set_PWarnFlg(tyre_id, 1)
            self.ck_faultinfo([{"fault": 1, "faultMsg": "", "tyre": tyre_id}], tyre_id=tyre_id)
            self.mockmcu.set_PWarnFlg(tyre_id, 2)
            self.ck_faultinfo([{"fault": 2, "faultMsg": "", "tyre": tyre_id}], tyre_id=tyre_id)
            self.mockmcu.set_PWarnFlg(tyre_id, 0)
            self.ck_faultinfo([{"fault": 0, "faultMsg": "", "tyre": 4}], tyre_id=tyre_id)
            self.mockmcu.set_PWarnFlg(tyre_id, 2)
            self.ck_faultinfo([{"fault": 2, "faultMsg": "", "tyre": tyre_id}], tyre_id=tyre_id)
            self.mockmcu.set_PWarnFlg(tyre_id, 3)
            self.ck_faultinfo([{"fault": 0, "faultMsg": "", "tyre": 4}], tyre_id=tyre_id)

    @allure.title("通知全量胎压信息")
    @pytest.mark.smoke
    def test_caseid_1982936(self):
        for i in range(4):
            self.mockmcu.set_temperature(i, 0)
            self.mockmcu.set_pressure(i, 0)
        self.partner.empty_all(1)
        for data in [(0, 1), (1, 100), (2, 350.115), (3, 350.115)]:
            logger.info(f'发信号')
            self.mockmcu.set_pressure(*data)
            logger.info(f'重启起来')
            self.partner.ck_s2s_event(TYRE_SERVICE_CLIENT, "AllTyrePressure", 
                                    {"infos": [{"id": 0, "pressure": self.mockmcu.sensor0_pressure},
                                                {"id": 1, "pressure": self.mockmcu.sensor1_pressure},
                                                {"id": 2, "pressure": self.mockmcu.sensor2_pressure},
                                                {"id": 3, "pressure": self.mockmcu.sensor3_pressure}]})
        self.restart_bgm_and_connect_service(TYRE_SERVICE_CLIENT)
        self.partner.ck_s2s_event(TYRE_SERVICE_CLIENT, "AllTyrePressure", 
                                  {"infos": [{"id": 0, "pressure": self.mockmcu.sensor0_pressure},
                                             {"id": 1, "pressure": self.mockmcu.sensor1_pressure},
                                             {"id": 2, "pressure": self.mockmcu.sensor2_pressure},
                                             {"id": 3, "pressure": self.mockmcu.sensor3_pressure}]}, timeout=7)
        self.mockmcu.set_pressure(0, 350.115)
        self.mockmcu.set_pressure(1, 350.115)
        self.partner.ck_s2s_event(TYRE_SERVICE_CLIENT, "AllTyrePressure", 
                                  {"infos": [{"id": 0, "pressure": self.mockmcu.sensor0_pressure},
                                             {"id": 1, "pressure": self.mockmcu.sensor1_pressure},
                                             {"id": 2, "pressure": self.mockmcu.sensor2_pressure},
                                             {"id": 3, "pressure": self.mockmcu.sensor3_pressure}]})
        self.restart_bgm_and_connect_service(TYRE_SERVICE_CLIENT)
        self.partner.ck_s2s_event(TYRE_SERVICE_CLIENT, "AllTyrePressure", 
                                  {"infos": [{"id": 0, "pressure": self.mockmcu.sensor0_pressure},
                                             {"id": 1, "pressure": self.mockmcu.sensor1_pressure},
                                             {"id": 2, "pressure": self.mockmcu.sensor2_pressure},
                                             {"id": 3, "pressure": self.mockmcu.sensor3_pressure}]}, timeout=7)

    @allure.title("通知全量胎温信息")
    @pytest.mark.smoke
    def test_caseid_1982929(self):
        for i in range(4):
            self.mockmcu.set_temperature(i, 0)
            self.mockmcu.set_pressure(i, 0)
        self.partner.empty_all(1)

        for data in [(0, 20), (1, -49), (2, 205), (3, 70)]:
            self.mockmcu.set_temperature(*data)
            self.partner.ck_s2s_event(TYRE_SERVICE_CLIENT, "AllTyreTemperature", 
                                      {"infos": [{"id": 0, "temperature": self.mockmcu.sensor0_temp},
                                                 {"id": 1, "temperature": self.mockmcu.sensor1_temp},
                                                 {"id": 2, "temperature": self.mockmcu.sensor2_temp},
                                                 {"id": 3, "temperature": self.mockmcu.sensor3_temp}]})
        self.restart_bgm_and_connect_service(TYRE_SERVICE_CLIENT)
        self.partner.ck_s2s_event(TYRE_SERVICE_CLIENT, "AllTyreTemperature", 
                                  {"infos": [{"id": 0, "temperature": self.mockmcu.sensor0_temp},
                                             {"id": 1, "temperature": self.mockmcu.sensor1_temp},
                                             {"id": 2, "temperature": self.mockmcu.sensor2_temp},
                                             {"id": 3, "temperature": self.mockmcu.sensor3_temp}]}, timeout=7)
        self.mockmcu.set_temperature(0, 205)
        self.mockmcu.set_temperature(1, 205)
        self.mockmcu.set_temperature(3, 205)
        self.partner.ck_s2s_event(TYRE_SERVICE_CLIENT, "AllTyreTemperature", 
                                  {"infos": [{"id": 0, "temperature": self.mockmcu.sensor0_temp},
                                             {"id": 1, "temperature": self.mockmcu.sensor1_temp},
                                             {"id": 2, "temperature": self.mockmcu.sensor2_temp},
                                             {"id": 3, "temperature": self.mockmcu.sensor3_temp}]})
        self.restart_bgm_and_connect_service(TYRE_SERVICE_CLIENT)
        self.partner.ck_s2s_event(TYRE_SERVICE_CLIENT, "AllTyreTemperature", 
                                  {"infos": [{"id": 0, "temperature": self.mockmcu.sensor0_temp},
                                             {"id": 1, "temperature": self.mockmcu.sensor1_temp},
                                             {"id": 2, "temperature": self.mockmcu.sensor2_temp},
                                             {"id": 3, "temperature": self.mockmcu.sensor3_temp}]}, timeout=7)

    @allure.title("获取/通知胎压信息_初始值")
    @pytest.mark.full
    def test_caseid_1988605(self):
        self.ipdu.reset_dpu_data()#将所有信号置为初始值
        self.restart_bgm_and_connect_service(TYRE_SERVICE_CLIENT)
        sleep(5)
        self.partner.ck_s2s_event(TYRE_SERVICE_CLIENT, "AllTyrePressure", 
                                    {"infos": [{"id": 0, "pressure": 350.115},
                                                {"id": 1, "pressure": 350.115},
                                                {"id": 2, "pressure": 350.115},
                                                {"id": 3, "pressure": 350.115}]},timeout=5)
        self.partner.send_request_and_ck_resp(TYRE_SERVICE_CLIENT, "GetPressure", {"tyres":4}, 
                                              {"out": [{"id": 0, "pressure": 350.115},
                                                       {"id": 1, "pressure": 350.115},
                                                       {"id": 2, "pressure": 350.115},
                                                       {"id": 3, "pressure": 350.115}]})
        
    @allure.title("获取/通知胎温信息_初始值")
    @pytest.mark.full
    def test_caseid_1988606(self):
        self.ipdu.reset_dpu_data()#将所有信号置为初始值
        self.restart_bgm_and_connect_service(TYRE_SERVICE_CLIENT)
        sleep(5)
        self.partner.ck_s2s_event(TYRE_SERVICE_CLIENT, "AllTyreTemperature", 
                                      {"infos": [{"id": 0, "temperature": 205},
                                                 {"id": 1, "temperature": 205},
                                                 {"id": 2, "temperature": 205},
                                                 {"id": 3, "temperature": 205}]},timeout=5)
        self.partner.send_request_and_ck_resp(TYRE_SERVICE_CLIENT, "GetTemperature", {"tyres":4}, 
                                              {"out":[{"id": 0, "temperature": 205},
                                                      {"id": 1, "temperature": 205},
                                                      {"id": 2, "temperature": 205},
                                                      {"id": 3, "temperature": 205}]})
        
    @allure.title("获取/通知轮胎故障信息/获取轮胎相关信息_初始值")
    @pytest.mark.full
    def test_caseid_1988607(self):
        self.ipdu.reset_dpu_data()#将所有信号置为初始值
        self.restart_bgm_and_connect_service(TYRE_SERVICE_CLIENT)
        logger.info("启动成功了")
        sleep(5)
        self.partner.ck_s2s_event(TYRE_SERVICE_CLIENT, "TyreFault", {"faults": [{"fault":0,"faultMsg":"","tyre":4}]},timeout=5)
        self.partner.send_request_and_ck_resp(TYRE_SERVICE_CLIENT, "GetFaultInfo", {}, {"out":[{"fault":0,"faultMsg":"","tyre":4}]})
        self.partner.send_request_and_ck_resp(TYRE_SERVICE_CLIENT, "GetTyreInfo", {"tyres": [4]},
                                              {"out": [{"id":0,"pressure":350.115,"temperature":205,"fault":[0]},
                                                       {"id":1,"pressure":350.115,"temperature":205,"fault":[0]},
                                                       {"id":2,"pressure":350.115,"temperature":205,"fault":[0]},
                                                       {"id":3,"pressure":350.115,"temperature":205,"fault":[0]}]}) 