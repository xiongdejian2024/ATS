#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_CarConfigService.py
@Time         :2023/05/13 17:20:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import random
import os
import allure
import pytest
from time import sleep
from xat_cases.legacy.soa.case_helper.test_base import TestBase, write_s2s_json
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.interface.bgm.bgm_env.change_bgm_env import change_bgm_config, recover_bgm_config

default_ccp_list = DataTypeHanding.hexstr_to_inlist(
    "A3018006FD030101A302090304020102858B06010004050203000001048C800C0101010102010202010216010701010100030102028089020301010302736E03010101010101010302020202020A010103820201010102020103010201800202020201800000008182118003010103020102020302800102010102010104010101010101010203010103020101830201020201012902010402038002820103040128030A800104010201020203820402810101020101130301010101010205020101000302020304020202010101020001010101010101010180030A0101040607070A0A07070A0A00000400000201010101010280030301020000000202020102020200010102000000010300000100008100000000000000000000000000000080000000000000000000000100010100000200000080000000008403010100000000020100000000000000000002018001020101010101020103020180018002020101010101050380020601030110000002030100000000000000000000000000000000000000000000000000000002000000000001010301000000000200000000000000000000000000000000000000000000000000010201000000000085040102020201020202040301020201028004030101020201030101010202020101020101010101030000000180020201010202010202020102010302020101010101010101000103010201010502020204010101010301010402010201010101020101010101010100000000000001020301010109030101010202020101030104010401010101010201030105020001010101010101010101010101010101010101010101010202010101010102010101010201000001010401000000010100000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001030202080100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001010201020102020101020101010101010201010201010101010202010201010101020202020202010202010202010201010101020101010102010101000102010101000101010101020202010101020201010101010102020102010101010101010001010101010101020101010101020101010101010101010101010101010101010101020201020101010101010100000101010101010101020101010101010101010202000101010101010202020101010100000000000000000000000000000000000000000000000000000000000000000000020202020202020101010101010101020101010101010202020202010002020101020102020201020001")


def return_EnergyConsumptionData(batteryCapacityMax, cltcFullRange, cltcEnergyComsumption,
                                 wltpFullRange, wltpEnergyComsumption,epaFullRange,epaEnergyComsumption):
    """返回续航能耗属性信息的结构体(字典)"""
    return {'batteryCapacityMax': batteryCapacityMax,
            'cltcFullRange': cltcFullRange,
            'cltcEnergyComsumption': cltcEnergyComsumption,
            'wltpFullRange': wltpFullRange,
            'wltpEnergyComsumption': wltpEnergyComsumption,
            'epaFullRange': epaFullRange,
            'epaEnergyComsumption': epaEnergyComsumption}


@allure.feature("SOA服务接口")
@allure.story("架构基础/CarConfigService")
@pytest.mark.zjb
class TestCarConfigService(TestBase):

    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("CarConfigService", "client")])
        self.partner.method_default_timeout = 2
        self.sd_tester.tester_present()
        self.sd_tester.update_serverdoipid(0x1001)
        self.sd_tester.enter_extended_session()
        sleep(0.5)
        self.sd_tester.security_access_level_l3()
        self.sd_tester.write_vehicleinfo([0x61,0x60,0x11,0x02,0x10,0x60,0x41,0x50])
        sleep(1)
        self.sd_tester.read_data_by_identifier(0xF150)
        self.old_engineering = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 22F150 to get result")[3:]   
        sleep(2)
        self.sd_tester.client_sim.send_data([0x2E, 0xF1, 0x51] +[0x56,0x32,0x2E,0x30,0x2E,0x30]+[0x00]*25 + [0x30])
        sleep(1)
        self.sd_tester.read_data_by_identifier(0xF151)
        self.old_formal = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 22F151 to get result")[3:]
        logger.info(f"==========打印{self.old_engineering}和{self.old_formal}")

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.sd_tester.update_serverdoipid(0x1001)
        self.sd_tester.enter_extended_session()
        sleep(0.5)
        self.sd_tester.security_access_level_l3()
        self.sd_tester.write_vehicleinfo([0x61,0x60,0x11,0x02,0x10,0x60,0x41,0x50])
        sleep(1)
        self.sd_tester.read_data_by_identifier(0xF150)
        self.old_engineering = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 22F150 to get result")[3:]   
        sleep(2)
        self.sd_tester.client_sim.send_data([0x2E, 0xF1, 0x51] +[0x56,0x32,0x2E,0x30,0x2E,0x30]+[0x00]*25 + [0x30])
        sleep(1)
        self.partner.stop_operators()
        self.sd_tester.stop_tester_present()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.io.set_four_door_close()
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.change_usage_mode(1)
        self.tc_vin_list = self.write_vin(self.tc_config['vin'])
        self.write_ccp()
        self.partner.empty_all(3)

    def after_each_func(self, ecu):
        self.sd_tester.update_serverdoipid(0x1002)
        self.tc_vin_list = self.write_vin(self.tc_config['vin'])
        self.write_ccp()
        self.partner.empty_all(1)
        super().after_each_func(ecu, start=False)

    def write_vin(self, vin_str):
        """写入vin码"""
        self.sd_tester.enter_extended_session()
        self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 1003 to get result")
        self.sd_tester.security_access_level_l3()
        self.sd_tester.write_vin(vin_str)
        self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 2EF190 to get result")
        return list(bytes(vin_str, encoding="ascii"))

    def write_ccp(self, ccp_list=default_ccp_list):
        self.sd_tester.write_multi_ccp({index + 1: ccp_list[index] for index in range(1556)})

    def get_ccp(self, count):
        """获取ccp#？的值, ccp1即第0个ccp"""
        return self.sd_tester.read_ccp()[1][count - 1]

    @allure.title("最大标称OBC电流_非0/1/2的情况")
    @pytest.mark.full
    def test_caseid_1988886(self):
        self.sd_tester.write_single_ccp(973, 1)
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetCarPropertyInfo", {},
                                              {"out": {"obcCurrentMax":32}})
        self.partner.empty_all()
        last_value=32
        for ccp973 in [0, 3, 1, 4]:
            self.sd_tester.write_single_ccp(973, ccp973)
            logger.info("打印当前ccp:{}".format({973: ccp973}))
            value = 32 if ccp973 in [1, 2] else -1
            if last_value != value:
                self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "CarPropertyInfo",
                                               {"propertyInfo":{"obcCurrentMax":value}})
            else:
                self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "CarPropertyInfo")                               
            last_value=value  

    @allure.title("最大标称OBC电流")
    @pytest.mark.smoke
    def test_caseid_1988882(self):
        self.sd_tester.write_single_ccp(973, 1)
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetCarPropertyInfo", {},
                                              {"out": {"obcCurrentMax":32}})
        self.partner.empty_all()
        last_value=32
        for ccp973 in [0, 1, 2]:
            self.sd_tester.write_single_ccp(973, ccp973)
            logger.info("写ccp:{}".format({973: ccp973}))
            value = 32 if ccp973 in [1, 2] else -1
            if last_value != value:
                self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "CarPropertyInfo",
                                               {"propertyInfo":{"obcCurrentMax":value}})
            else:
                self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "CarPropertyInfo")                               
            last_value=value  
            
    @allure.title("获取车辆软件Baseline")
    @pytest.mark.sanity
    def test_caseid_104996(self):
        self.restart_bgm_and_connect_service(CARCONFIG_SERVICE_CLIENT)
        self.sd_tester.update_serverdoipid(0x1001)
        self.sd_tester.read_data_by_identifier(0xF150)
        engineering = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 22F150 to get result")[3:]
        engineering_baseline = f"{engineering[0]:02X}{engineering[1]:02X}{engineering[2]:02X}{engineering[3]:02X}" \
                               f"{engineering[4]:02X}" + chr(engineering[5]) + chr(engineering[6]) + chr(engineering[7])
        self.sd_tester.read_data_by_identifier(0xF151)
        formal = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 22F151 to get result")[3:]
        forma2=formal[:-2]
        formal_baseline1 = ''.join([chr(x) for x in forma2]).rstrip(chr(0))
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetVehicleSWBaseline", {},
                                              {"out": {"engineeringBaseline": engineering_baseline,
                                                       "formalBaseline": formal_baseline1}})  
     
    @allure.title("获取和通知车辆软件Baseline")
    @pytest.mark.sanity
    def test_caseid_1986209(self):
        self.sd_tester.update_serverdoipid(0x1001)
        self.sd_tester.enter_extended_session()
        self.sd_tester.security_access_level_l3()
        self.sd_tester.write_vehicleinfo([0x01,0x61,0x60,0x11,0x00,0x60,0x43,0x47])
        sleep(2)
        self.sd_tester.client_sim.send_data([0x2E, 0xF1, 0x51] + [0x00]*32)
        self.partner.empty_all(2)
        self.sd_tester.write_vehicleinfo([0x01,0x62,0x60,0x11,0x00,0x60,0x43,0x48])
        sleep(1)
        self.sd_tester.client_sim.send_data([0x2E, 0xF1, 0x51] + [0x42]*32)
        sleep(1)
        self.sd_tester.update_serverdoipid(0x1001)
        sleep(1)
        self.sd_tester.read_data_by_identifier(0xF150)
        sleep(1)
        engineering = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 22F150 to get result")[3:]
        engineering_baseline = f"{engineering[0]:02X}{engineering[1]:02X}{engineering[2]:02X}{engineering[3]:02X}" \
                               f"{engineering[4]:02X}" + chr(engineering[5]) + chr(engineering[6]) + chr(engineering[7])
        self.sd_tester.read_data_by_identifier(0xF151)
        formal = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 22F151 to get result")[3:]
        formal_baseline1 = ''.join([chr(x) for x in formal])
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "VehicleSWBaseline",
                                           {"info": {"engineeringBaseline": engineering_baseline,
                                                       "formalBaseline": formal_baseline1}})
        
    @allure.title("获取和通知车辆软件Baseline_全0x00或不足32位时主动补0x00截断")
    @pytest.mark.smoke
    def test_caseid_1987931(self):
        self.sd_tester.update_serverdoipid(0x1001)
        self.sd_tester.enter_extended_session()
        sleep(0.5)
        self.sd_tester.security_access_level_l3()
        self.sd_tester.write_vehicleinfo([0x01,0x61,0x60,0x11,0x00,0x60,0x43,0x47])
        sleep(2)
        self.sd_tester.client_sim.send_data([0x2E, 0xF1, 0x51] + [0x41]*32)
        self.partner.empty_all(2)
        self.sd_tester.write_vehicleinfo([0x01,0x62,0x60,0x11,0x00,0x60,0x43,0x48])
        sleep(1)
        self.sd_tester.client_sim.send_data([0x2E, 0xF1, 0x51] + [0x00]*32)
        sleep(1)
        self.sd_tester.update_serverdoipid(0x1001)
        sleep(1)
        self.sd_tester.read_data_by_identifier(0xF150)
        sleep(1)
        engineering = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 22F150 to get result")[3:]
        engineering_baseline = f"{engineering[0]:02X}{engineering[1]:02X}{engineering[2]:02X}{engineering[3]:02X}" \
                               f"{engineering[4]:02X}" + chr(engineering[5]) + chr(engineering[6]) + chr(engineering[7])
        #全0时为空
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "VehicleSWBaseline",
                                           {"info": {"engineeringBaseline": engineering_baseline,
                                                       "formalBaseline": ""}}) 
        sleep(1)
        #字节不足32mcu报NRC 13长度错误，所以只能前后加0x00报文观察是否被截断
        self.sd_tester.client_sim.send_data([0x2E, 0xF1, 0x51] +[0x56,0x32,0x2E,0x30,0x2E,0x30]+[0x00]*25 + [0x30])
        sleep(1)
        self.sd_tester.read_data_by_identifier(0xF151)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "VehicleSWBaseline",
                                           {"info": {"engineeringBaseline": engineering_baseline,
                                                       "formalBaseline": "V2.0.0"}}, fuzz_match=False) 

    @allure.title("获取车辆软件Baseline_空内容参数赋值空")
    @pytest.mark.sanity
    def test_caseid_1986158(self):
        self.sd_tester.update_serverdoipid(0x1001)
        sleep(1)
        self.sd_tester.read_data_by_identifier(0xF150)
        sleep(1)
        engineering = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 22F150 to get result")[3:]
        engineering_baseline = f"{engineering[0]:02X}{engineering[1]:02X}{engineering[2]:02X}{engineering[3]:02X}" \
                               f"{engineering[4]:02X}" + chr(engineering[5]) + chr(engineering[6]) + chr(engineering[7])
        self.sd_tester.read_data_by_identifier(0xF151)
        formal = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 22F151 to get result")[3:]
        new_formal_baseline = formal[:-1]
        formal_baseline = ''.join([chr(x) for x in new_formal_baseline]).rstrip(chr(0))

        logger.info(f"F150的结果为{engineering_baseline}且F151的结果为{formal_baseline}")
        self.bgmcli.type_commands("mv /data/vehicleInfo.json /data/vehicleInfo1.json")
        sleep(2)
        self.kill_s2s_and_reconnect_service(CARCONFIG_SERVICE_CLIENT)
        sleep(2)
        try:
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetVehicleSWBaseline", {},
                                              {"out": {"engineeringBaseline": '',"formalBaseline": ''}})
        except Exception as err:
            self.bgmcli.type_commands("rm /data/vehicleInfo.json")
            sleep(1)
            self.bgmcli.type_commands("mv /data/vehicleInfo1.json /data/vehicleInfo.json")
            assert False
        else:
            self.bgmcli.type_commands("rm /data/vehicleInfo.json")
            sleep(1)
            self.bgmcli.type_commands("mv /data/vehicleInfo1.json /data/vehicleInfo.json")
        sleep(2) #重新改回来
        self.kill_s2s_and_reconnect_service(CARCONFIG_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetVehicleSWBaseline", {},
                                              {"out": {"engineeringBaseline": engineering_baseline,"formalBaseline": formal_baseline}}) #

    @allure.title("车辆配置字信息_Jidu车型")
    @pytest.mark.sanity
    def test_caseid_1724870(self):
        self.sd_tester.write_single_ccp(950, 0)
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950]},
                                              {"out": [{"name": 950, "value": 0}]})
        for ccp950 in [1, 2] + [random.randint(3, 255) for _ in range(3)]:
            self.sd_tester.write_single_ccp(950, ccp950)
            logger.info("写ccp：{}".format({950: ccp950}))
            self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyConfigList",
                                           {"list": [{"name": 950, "value": ccp950}]},
                                           method_args={"names": [950]})

    @allure.title("车辆配置字信息_新旧方向盘")
    @pytest.mark.sanity
    def test_caseid_104986(self):
        self.sd_tester.write_single_ccp(959, 0)
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [959]},
                                              {"out": [{"name": 959, "value": 0}]})
        for ccp959 in [1, 2] + [random.randint(3, 255) for _ in range(3)]:
            self.sd_tester.write_single_ccp(959, ccp959)
            logger.info("写ccp：{}".format({959: ccp959}))
            self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyConfigList",
                                           {"list": [{"name": 959, "value": ccp959}]},
                                           method_args={"names": [959]})

    @allure.title("通知并获取车辆VIN码")
    @pytest.mark.smoke
    def test_caseid_104992(self):
        self.restart_bgm_and_connect_service(CARCONFIG_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CARCONFIG_SERVICE_CLIENT, "NotifyVIN", {"vin": {"vin": self.tc_vin_list}},
                                  fuzz_match=False)
        # 因为partner默认注册event时会发送历史值，多个case运行时是重启会异常发送一次历史数据event
        self.partner.empty_all(1)
        sleep(7)
        # self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyVIN", timeout=7)
        self.partner.ck_s2s_event(CARCONFIG_SERVICE_CLIENT, "NotifyVIN", {"vin": {"vin": self.tc_vin_list}},
                                  fuzz_match=False, timeout=3)

        self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyVIN", timeout=8)
        self.partner.ck_s2s_event(CARCONFIG_SERVICE_CLIENT, "NotifyVIN", {"vin": {"vin": self.tc_vin_list}},
                                  fuzz_match=False, timeout=3)

        self.partner.ck_no_event_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "NotifyVIN", 
                                              {"out": {"vin": self.tc_vin_list}}, timeout=13)

        vin = self.write_vin('11111111111111111')
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyVIN", {"vin": {"vin": vin}}, fuzz_match=False)

        vin = self.write_vin(self.tc_config["vin"])
        self.partner.ck_s2s_event(CARCONFIG_SERVICE_CLIENT, "NotifyVIN", {"vin": {"vin": vin}}, fuzz_match=False)

    @allure.title("通知并获取轮周长")
    @pytest.mark.sanity
    def test_caseid_104988(self):
        ccp18 = self.get_ccp(18)
        self.partner.empty_all(2)
        self.restart_bgm_and_connect_service(CARCONFIG_SERVICE_CLIENT)
        circumference = ccp18 * 5 + 1700
        self.partner.ck_s2s_event(CARCONFIG_SERVICE_CLIENT, "NotifyWheelCircumference",
                                  {"circumference": circumference}, timeout=10)
    
        # self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyWheelCircumference", timeout=8)
        sleep(8)
        self.partner.ck_s2s_event(CARCONFIG_SERVICE_CLIENT, "NotifyWheelCircumference",
                                  {"circumference": circumference}, timeout=3)

        self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyWheelCircumference", timeout=8)
        self.partner.ck_s2s_event(CARCONFIG_SERVICE_CLIENT, "NotifyWheelCircumference",
                                  {"circumference": circumference}, timeout=3)

        self.partner.ck_no_event_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "NotifyWheelCircumference", 
                                              {"out": circumference}, timeout=13)

        self.sd_tester.write_single_ccp(18, 130)
        new_circumference = 130 * 5 + 1700
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyWheelCircumference",
                                       {"circumference": new_circumference})

        self.sd_tester.write_single_ccp(18, ccp18)
        self.partner.ck_s2s_event(CARCONFIG_SERVICE_CLIENT, "NotifyWheelCircumference",
                                  {"circumference": circumference})

    @allure.title("通知车辆配置信息_ccp全部为0xFF")
    @pytest.mark.full
    def test_caseid_104993(self):
        car_config_info = self.partner.send_request_and_return_resp(CARCONFIG_SERVICE_CLIENT, "GetCarConfigInfo", {})[
            "out"]

        origin_ccp_list = self.sd_tester.read_ccp()[1]
        self.sd_tester.write_multi_ccp({x: 0xFF for x in range(1, 1557)})
        exp_info = {"config": [0xFF] * 504,
                    "extendConfig": [0xFF] * 504,
                    "nodeList": [0] * 8,
                    "vin": car_config_info["vin"],
                    "wheelCircum": 4095,
                    "isValid": True
                    }
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyCarConfigInfo",
                                       {"info": exp_info}, fuzz_match=False)

        self.write_ccp(origin_ccp_list)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyCarConfigInfo",
                                       {"info": car_config_info}, fuzz_match=False)

    @allure.title("通知车辆配置信息_config参数变化")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1724869?projectId=46')
    @pytest.mark.full
    def test_caseid_104987(self):
        car_config_info = self.partner.send_request_and_return_resp(CARCONFIG_SERVICE_CLIENT, "GetCarConfigInfo", {})[
            "out"]

        self.sd_tester.write_multi_ccp({x: 0xFF for x in range(1, 505)})
        exp_info = {"config": [0xFF] * 504,
                    "extendConfig": car_config_info["extendConfig"],
                    "nodeList": car_config_info["nodeList"],
                    "vin": car_config_info["vin"],
                    "wheelCircum": 4095,
                    "isValid": True
                    }
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyCarConfigInfo",
                                       {"info": exp_info}, fuzz_match=False)

        self.sd_tester.write_multi_ccp({x: 0x00 for x in range(1, 505)})
        exp_info.update({"config": [0x00] * 504})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyCarConfigInfo",
                                       {"info": exp_info}, fuzz_match=False)

        self.sd_tester.write_multi_ccp({x: car_config_info['config'][x - 1] for x in range(1, 505)})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyCarConfigInfo",
                                       {"info": car_config_info}, fuzz_match=False)

    @allure.title("通知车辆配置信息_extendConfig参数变化")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1724862?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104994(self):
        car_config_info = self.partner.send_request_and_return_resp(CARCONFIG_SERVICE_CLIENT, "GetCarConfigInfo", {})[
            "out"]

        self.sd_tester.write_multi_ccp({x: 0xFF for x in range(505, 1009)})
        exp_info = {"config": car_config_info["config"],
                    "extendConfig": [0xFF] * 504,
                    "nodeList": car_config_info["nodeList"],
                    "vin": car_config_info["vin"],
                    "wheelCircum": car_config_info["wheelCircum"],
                    "isValid": True
                    }
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyCarConfigInfo",
                                       {"info": exp_info}, fuzz_match=False)

        self.sd_tester.write_multi_ccp({x: car_config_info['extendConfig'][x - 505] for x in range(505, 1009)})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyCarConfigInfo",
                                       {"info": car_config_info}, fuzz_match=False)

    @allure.title("通知车辆配置信息_nodeList参数变化")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1724867?projectId=46')
    @pytest.mark.full
    def test_caseid_104989(self):
        car_config_info = self.partner.send_request_and_return_resp(CARCONFIG_SERVICE_CLIENT, "GetCarConfigInfo", {})[
            "out"]

        self.sd_tester.write_multi_ccp({x: 2 for x in range(1301, 1557)})
        exp_info = {"config": car_config_info["config"],
                    "extendConfig": car_config_info["extendConfig"],
                    "nodeList": [0xFFFFFFFF] * 8,
                    "vin": car_config_info["vin"],
                    "wheelCircum": car_config_info["wheelCircum"],
                    "isValid": True
                    }
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyCarConfigInfo",
                                       {"info": exp_info}, fuzz_match=False)

        self.sd_tester.write_multi_ccp({x: 1 for x in range(1301, 1557)})
        exp_info['nodeList'] = [0] * 8
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyCarConfigInfo",
                                       {"info": exp_info}, fuzz_match=False)

        self.sd_tester.write_multi_ccp({x: 0 for x in range(1301, 1557)})
        self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT,
                                 "NotifyCarConfigInfo")  # 关注下到底会不会有event，因为tcp有数据上来，但映射的CarConfigInfo无变化
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetCarConfigInfo", {}, {"out": exp_info})

        ccp_nodelist = {index: random.randint(0, 2) for index in range(1301, 1557)}
        exp_nodelist = [0] * 8
        for i in range(8):
            for j in range(32):
                exp_nodelist[i] += (1 << j if ccp_nodelist[1301 + i * 32 + j] == 2 else 0)
        exp_info['nodeList'] = exp_nodelist
        self.sd_tester.write_multi_ccp(ccp_nodelist)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyCarConfigInfo",
                                       {"info": exp_info}, fuzz_match=False)

    @allure.title("通知车辆配置信息_vin参数变化")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1724865?projectId=46')
    @pytest.mark.full
    def test_caseid_104991(self):
        car_config_info = self.partner.send_request_and_return_resp(CARCONFIG_SERVICE_CLIENT, "GetCarConfigInfo", {})[
            "out"]

        vin = self.write_vin('11111111111111111')
        exp_info = {"config": car_config_info["config"],
                    "extendConfig": car_config_info["extendConfig"],
                    "nodeList": car_config_info["nodeList"],
                    "vin": vin,
                    "wheelCircum": car_config_info["wheelCircum"],
                    "isValid": True
                    }
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyCarConfigInfo",
                                       {"info": exp_info}, fuzz_match=False)

        vin = self.write_vin(self.tc_config["vin"])
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyCarConfigInfo",
                                       {"info": car_config_info}, fuzz_match=False)
        
    @allure.title("续航能耗属性信息_Mars1")
    @pytest.mark.smoke
    def test_caseid_1989258(self):
        self.sd_tester.write_multi_ccp({950: 0, 3: 0, 566: 0, 966: 0,948: 2}) #948不写4进行干扰
        self.del_s2s_db()
        self.restart_bgm_and_connect_service(CARCONFIG_SERVICE_CLIENT)
        self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData")
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT,"GetEnergyConsumptionData",{},
                                              {"out": return_EnergyConsumptionData(0.0, 0, 0.0, 0, 0.0,599, 19.0)}, timeout = 2) #需求认可拿到599和19
        self.sd_tester.write_multi_ccp({950: 1, 3: 129, 566: 16, 966: 0})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(97.68, 720, 13.57, 595, 16.42,599,19.0)})
        self.sd_tester.write_multi_ccp({950: 1, 3: 129, 566: 24, 966: 2})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(96.04, 750, 12.81, 630, 15.24,599,19.0)})
        self.sd_tester.write_multi_ccp({950: 1, 3: 129, 566: 16, 966: 1})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(98.70, 780, 12.65, 650, 15.18,599,19.0)})
        
        self.sd_tester.write_multi_ccp({950: 1, 3: 128, 566: 16, 966: 0})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(97.68, 660, 14.80, 557, 17.54,599,19.0)})
        self.sd_tester.write_multi_ccp({950: 1, 3: 128, 566: 24, 966: 2})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(96.04, 700, 13.72, 588, 16.33,599,19.0)})
        self.sd_tester.write_multi_ccp({950: 1, 3: 128, 566: 16, 966: 1})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(98.70, 700, 14.10, 590, 16.73,599,19.0)})
        
        self.sd_tester.write_multi_ccp({950: 1, 3: 129, 566: 23, 966: 0})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(74.25, 550, 13.5, 452, 16.43,599,19.0)})
        self.sd_tester.write_multi_ccp({950: 1, 3: 129, 566: 25, 966: 2})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(76.50, 600, 12.75, 504, 15.18,599,19.0)})
        self.sd_tester.write_multi_ccp({950: 1, 3: 129, 566: 23, 966: 1})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(74.25, 580, 12.80, 490, 15.15,599,19.0)})
        
        self.sd_tester.write_multi_ccp({950: 0xFF, 3: 0xFF, 566: 0xFF})
        self.partner.ck_no_event_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                             {"out": return_EnergyConsumptionData(74.25, 580, 12.80, 490, 15.15,599,19.0)})
        
    @allure.title("续航能耗属性信息_Venus")
    @pytest.mark.sanity
    def test_caseid_1989259(self):
        self.sd_tester.write_multi_ccp({950: 0, 3: 0, 566: 0, 966: 0,948:4}) #写4进行干扰
        self.del_s2s_db()
        self.restart_bgm_and_connect_service(CARCONFIG_SERVICE_CLIENT)
        self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData")
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT,"GetEnergyConsumptionData",{},
                                              {"out": return_EnergyConsumptionData(0.0, 0, 0.0, 0, 0.0,599, 19.0)}, timeout = 2)
        self.sd_tester.write_multi_ccp({950: 2, 3: 129, 566: 16, 966: 1})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(98.70, 880, 11.22, 730, 13.52,599,19.0)})
        self.sd_tester.write_multi_ccp({950: 2, 3: 129, 566: 24, 966: 1})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(96.04, 880, 10.91, 730, 13.16,599,19.0)})


        self.sd_tester.write_multi_ccp({950: 2, 3: 128, 566: 16, 966: 2})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(98.70, 770, 12.82, 650, 15.18,599,19.0)})
        self.sd_tester.write_multi_ccp({950: 2, 3: 128, 566: 24, 966: 2})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(96.04, 770, 12.48, 650, 14.78,599,19.0)})
        self.sd_tester.write_multi_ccp({950: 2, 3: 129, 566: 23, 966: 2})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(74.25, 660, 11.25, 560, 13.26,599,19.0)})
        self.sd_tester.write_multi_ccp({950: 2, 3: 129, 566: 25, 966: 2})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                       {"data": return_EnergyConsumptionData(76.5, 700, 10.93, 580, 13.19,599,19.0)})
        self.sd_tester.write_multi_ccp({950: 0xFF, 3: 0xFF, 566: 0xFF})
        self.partner.ck_no_event_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData", 
                                             {"out": return_EnergyConsumptionData(76.5, 700, 10.93, 580, 13.19,599,19.0)})
    
    @allure.title("续航能耗属性信息_下电记忆")
    @pytest.mark.full
    def test_caseid_1983486(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 16, 950: 1})
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                              {"out": return_EnergyConsumptionData(97.68, 720, 13.57, 595, 16.42,599,19.0)})
        self.restart_bgm_and_connect_service(CARCONFIG_SERVICE_CLIENT)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, 
                                       "NotifyEnergyConsumptionData",
                                       {"data": return_EnergyConsumptionData(97.68, 720, 13.57, 595, 16.42,599,19.0)})
        self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData")

    @allure.title("车辆配置字信息_弹射控制")
    @pytest.mark.sanity
    def test_caseid_1984760(self):
        self.sd_tester.write_single_ccp(641, 0)
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [641]},
                                              {"out": [{"name": 641, "value": 0}]})
        for ccp641 in [1, 2] + [random.randint(3, 255) for _ in range(3)]:
            self.sd_tester.write_single_ccp(641, ccp641)
            logger.info("写ccp：{}".format({641: ccp641}))
            self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyConfigList",
                                           {"list": [{"name": 641, "value": ccp641}]},
                                           method_args={"names": [641]})
            
    @allure.title("车辆配置字信息_智能方向盘按键类型")
    @pytest.mark.sanity
    def test_caseid_1985653(self):
        self.sd_tester.write_single_ccp(641, 0)
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [970]},
                                              {"out": [{"name": 970, "value": 0}]})
        for ccp970 in [1, 2] + [random.randint(3, 255)]: 
            self.sd_tester.write_single_ccp(970, ccp970)
            logger.info("写ccp：{}".format({970: ccp970}))
            self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyConfigList",
                                           {"list": [{"name": 970, "value": ccp970}]},
                                           method_args={"names": [970]})

    @allure.title("车辆配置字信息_BMS类型")
    @pytest.mark.sanity
    def test_caseid_1984761(self):
        self.sd_tester.write_single_ccp(961, 0)
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [961]},
                                              {"out": [{"name": 961, "value": 0}]})
        for ccp961 in [1, 2] + [random.randint(3, 255)]:
            self.sd_tester.write_single_ccp(961, ccp961)
            logger.info("写ccp：{}".format({961: ccp961}))
            self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyConfigList",
                                           {"list": [{"name": 961, "value": ccp961}]},
                                           method_args={"names": [961]})

    @allure.title("车辆配置字信息_高压系统")
    @pytest.mark.sanity
    def test_caseid_1984762(self):
        ccp1 =[1,2] + [random.randint(3, 255) for _ in range(3)]
        self.sd_tester.write_single_ccp(962, 0)
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [962]},
                                              {"out": [{"name": 962, "value": 0}]})
        lastccp =0 
        for ccp962 in ccp1:
            self.sd_tester.write_single_ccp(962, ccp962)
            logger.info("写ccp：{}".format({962: ccp962}))
            if lastccp != ccp962 :
                self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyConfigList",
                                            {"list": [{"name": 962, "value": ccp962}]},
                                            method_args={"names": [962]})
            else:
                self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyConfigList")
            lastccp =ccp962  
            
    @allure.title("车辆配置字信息_IEMType")
    @pytest.mark.sanity
    def test_caseid_1984763(self):
        self.sd_tester.write_single_ccp(963, 0)
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [963]},
                                              {"out": [{"name": 963, "value": 0}]})
        for ccp963 in [1, 2] + [random.randint(3, 255)]:
            self.sd_tester.write_single_ccp(963, ccp963)
            logger.info("写ccp：{}".format({963: ccp963}))
            self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyConfigList",
                                           {"list": [{"name": 963, "value": ccp963}]},
                                           method_args={"names": [963]})
            
    @allure.title("车辆配置字信息_IPM")
    @pytest.mark.sanity
    def test_caseid_1984764(self):
        self.sd_tester.write_single_ccp(1333, 0)
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [1333]},
                                              {"out": [{"name": 1333, "value": 0}]})
        for ccp1333 in [1, 2] + [random.randint(3, 255)]:
            self.sd_tester.write_single_ccp(1333, ccp1333)
            logger.info("写ccp：{}".format({1333: ccp1333}))
            self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyConfigList",
                                           {"list": [{"name": 1333, "value": ccp1333}]},
                                           method_args={"names": [1333]})
            
    @allure.title("车辆配置字信息_WCTV")
    @pytest.mark.sanity
    def test_caseid_1984765(self):
        self.sd_tester.write_single_ccp(1334, 0)
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [1334]},
                                              {"out": [{"name": 1334, "value": 0}]})
        for ccp1334 in [1, 2] + [random.randint(3, 255)]:
            self.sd_tester.write_single_ccp(1334, ccp1334)
            logger.info("写ccp：{}".format({1334: ccp1334}))
            self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyConfigList",
                                           {"list": [{"name": 1334, "value": ccp1334}]},
                                           method_args={"names": [1334]})
            
    @allure.title("车辆配置字信息_WPC3")
    @pytest.mark.sanity
    def test_caseid_1984766(self):
        self.sd_tester.write_single_ccp(1439, 0)
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [1439]},
                                              {"out": [{"name": 1439, "value": 0}]})
        for ccp1439 in [1, 2] + [random.randint(3, 255)]:
            self.sd_tester.write_single_ccp(1439, ccp1439)
            logger.info("写ccp：{}".format({1439: ccp1439}))
            self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyConfigList",
                                           {"list": [{"name": 1439, "value": ccp1439}]},
                                           method_args={"names": [1439]})
            
    @allure.title("车辆配置字信息_SMB")
    @pytest.mark.smoke
    def test_caseid_1984768(self):
        self.sd_tester.write_single_ccp(1473, 0)
        last_CCP=0
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [1473]},
                                              {"out": [{"name": 1473, "value": 0}]})
        for ccp1473 in [1, 2] + [random.randint(3, 255)]:
            self.sd_tester.write_single_ccp(1473, ccp1473)
            logger.info("写ccp：{}".format({1473: ccp1473}))
            if last_CCP != ccp1473: #防止随机数相同导致拿不到event
                self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyConfigList",
                                           {"list": [{"name": 1473, "value": ccp1473}]},
                                           method_args={"names": [1473]})
            else:
                self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyConfigList")                               
            last_CCP=ccp1473          
            
    @allure.title("最大标称输出功率")
    @pytest.mark.smoke
    def test_caseid_1988521(self):
        self.sd_tester.write_multi_ccp({962: 0, 3: 0})
        sleep(5)
        self.del_s2s_db()
        self.restart_bgm_and_connect_service(CARCONFIG_SERVICE_CLIENT)
        # 删掉数据库，tcp包也不上来的情况下，bgm重启后要发 不发默认值0
        self.partner.ck_no_event_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "CarPropertyInfo", 
                                       {"propertyInfo":{"motorPowerMax":0}})
        
        self.sd_tester.write_multi_ccp({962: 0, 3: 128})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "CarPropertyInfo", 
                                       {"propertyInfo":{"motorPowerMax":400}})
        self.sd_tester.write_multi_ccp({962: 0, 3: 129})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "CarPropertyInfo", 
                                       {"propertyInfo":{"motorPowerMax":200}})
        self.sd_tester.write_multi_ccp({962: 0, 3: 130})
        self.partner.ck_no_event_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "CarPropertyInfo", 
                                              {"out": {"propertyInfo":{"motorPowerMax":200}}})
        self.sd_tester.write_multi_ccp({962: 2, 3: 130})
        self.partner.ck_no_event_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "CarPropertyInfo", 
                                              {"out": {"propertyInfo":{"motorPowerMax":200}}})
        self.sd_tester.write_multi_ccp({962: 2, 3: 128})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "CarPropertyInfo", 
                                       {"propertyInfo":{"motorPowerMax":530}})
        self.sd_tester.write_multi_ccp({962: 2, 3: 129})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "CarPropertyInfo", 
                                       {"propertyInfo":{"motorPowerMax":300}})
        
    @allure.title("BGM重启_最大标称输出功率_非默认值通知")
    @pytest.mark.full
    def test_caseid_1988522(self):
        self.sd_tester.write_multi_ccp({962: 2, 3: 129})
        sleep(5)
        self.del_s2s_db()
        self.restart_bgm_and_connect_service(CARCONFIG_SERVICE_CLIENT)
        self.sd_tester.write_multi_ccp({962: 2, 3: 129})
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "CarPropertyInfo", 
                                       {"propertyInfo":{"motorPowerMax":300}})
        
        
@allure.feature("SOA服务接口")
@allure.story("架构基础/CarConfigService")
@pytest.mark.zjb
class TestSpecificCarConfigService(TestBase):
    """针对需要修改BGM S2S配置的测试用例，单独新增一个类"""

    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        change_bgm_config(nucapp=self.nucapp)
        self.partner = S2sBaseClass([("CarConfigService", "client")])
        self.partner.method_default_timeout = 2
        self.partner.wait_for_service_reconnect(CARCONFIG_SERVICE_CLIENT)
        self.sd_tester.tester_present()

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.partner.stop_operators()
        self.sd_tester.stop_tester_present()
        recover_bgm_config()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.partner.empty_all(5)

    def after_each_func(self, ecu):
        self.update_bgm_s2s_json({}, partner_key=CARCONFIG_SERVICE_CLIENT) # 修改/data/app/s2s.json中30506端口改为30501
        self.sd_tester.update_serverdoipid(0x1002)
        self.write_vin(self.tc_config['vin'])
        self.write_ccp()
        super().after_each_func(ecu, start=False)

    def write_vin(self, vin_str):
        """写入vin码"""
        self.sd_tester.enter_extended_session()
        self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 1003 to get result")
        self.sd_tester.security_access_level_l3()
        self.sd_tester.write_vin(vin_str)
        self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 2EF190 to get result")
        return list(bytes(vin_str, encoding="ascii"))

    def write_ccp(self, ccp_list=default_ccp_list):
        self.sd_tester.write_multi_ccp({index + 1: ccp_list[index] for index in range(1556)})

    def get_ccp(self, count):
        """获取ccp#？的值, ccp1即第0个ccp"""
        return self.sd_tester.read_ccp()[1][count - 1]

    @allure.title("车辆配置信息_先使用记忆值_再根据mcu数据触发event")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1724871(self):
        car_config_info = self.partner.send_request_and_return_resp(CARCONFIG_SERVICE_CLIENT, "GetCarConfigInfo", {})[
            "out"]
        self.update_bgm_s2s_json({"tcpResClientPort": 30506,
                                  "tcpResServerPort": 30506}, partner_key=CARCONFIG_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CARCONFIG_SERVICE_CLIENT, "NotifyCarConfigInfo",
                                  {"info": car_config_info}, timeout=5, fuzz_match=False)

        vin = self.write_vin('11111111111111111')
        self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyCarConfigInfo")

        self.update_bgm_s2s_json({}, partner_key=CARCONFIG_SERVICE_CLIENT)
        sleep(8)
        event = self.partner.return_latest_event(CARCONFIG_SERVICE_CLIENT, "NotifyCarConfigInfo")
        car_config_info['vin'] = vin
        assert car_config_info == event['info']
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetCarConfigInfo", {},
                                              {"out": car_config_info})

    @allure.title("车辆配置信息_启动后使用记忆值")
    @pytest.mark.full
    def test_caseid_104985(self):
        car_config_info = self.partner.send_request_and_return_resp(CARCONFIG_SERVICE_CLIENT, "GetCarConfigInfo", {})[
            "out"]

        vin = self.write_vin('11111111111111111')
        car_config_info['vin'] = vin
        self.partner.ck_s2s_event(CARCONFIG_SERVICE_CLIENT, "NotifyCarConfigInfo",
                                  {"info": car_config_info}, fuzz_match=False)

        self.sd_tester.write_multi_ccp({x: 0x1 for x in range(1, 1557)})
        exp_info = {"config": [0x1] * 504,
                    "extendConfig": [0x1] * 504,
                    "nodeList": [0] * 8,
                    "vin": vin,
                    "wheelCircum": 1705,
                    "isValid": True
                    }
        self.partner.ck_s2s_event(CARCONFIG_SERVICE_CLIENT, "NotifyCarConfigInfo",
                                  {"info": exp_info}, fuzz_match=False)

        self.update_bgm_s2s_json({"tcpResClientPort": 30506,
                                  "tcpResServerPort": 30506}, partner_key=CARCONFIG_SERVICE_CLIENT)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, "NotifyCarConfigInfo",
                                       {"info": exp_info}, timeout=5, fuzz_match=False)

    @allure.title("通知车辆VIN码_先使用记忆值_再根据mcu数据触发event")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1979615(self):
        ori_vin = self.partner.send_request_and_return_resp(CARCONFIG_SERVICE_CLIENT, "GetVIN", {})[
            "out"]
        self.update_bgm_s2s_json({"tcpResClientPort": 30506,
                                  "tcpResServerPort": 30506}, partner_key=CARCONFIG_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CARCONFIG_SERVICE_CLIENT, "NotifyVIN",
                                  {"vin": ori_vin}, timeout=5, fuzz_match=False)

        vin = self.write_vin('11111111111111111')
        self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyVIN")

        self.update_bgm_s2s_json({}, partner_key=CARCONFIG_SERVICE_CLIENT)
        sleep(35)
        event1 = self.partner.return_latest_event(CARCONFIG_SERVICE_CLIENT, "NotifyVIN")
        event2 = self.partner.return_latest_event(CARCONFIG_SERVICE_CLIENT, "NotifyVIN")
        event3 = self.partner.return_latest_event(CARCONFIG_SERVICE_CLIENT, "NotifyVIN")

        assert event1 == event2 == event3 == {"vin": {"vin": vin}}

    @allure.title("车辆配置信息_首次启动默认值")
    @pytest.mark.full
    def test_caseid_104995(self):
        self.del_s2s_db()
        self.update_bgm_s2s_json({"tcpResClientPort": 30506,
                                  "tcpResServerPort": 30506}, partner_key=CARCONFIG_SERVICE_CLIENT)
        sleep(8)
        self.partner.ck_no_event_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "NotifyCarConfigInfo", 
                                              {"out": {"config": [0xFF] * 504,
                                                       "extendConfig": [0xFF] * 504,
                                                       "nodeList": [0xFFFFFFFF] * 8,
                                                       "vin": [0xFF] * 17,
                                                       "wheelCircum": 0xFFFF,
                                                       "isValid": False
                                                       }})

    @allure.title("最大标称OBC电流_默认值")
    @pytest.mark.full
    def test_caseid_1988930(self):
        self.sd_tester.write_single_ccp(973, 1)
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetCarPropertyInfo", {},
                                              {"out": {"obcCurrentMax":32}})
        self.del_s2s_db()
        self.update_bgm_s2s_json({"tcpResClientPort": 30506,
                                  "tcpResServerPort": 30506}, partner_key=CARCONFIG_SERVICE_CLIENT)
        sleep(8)
        self.partner.ck_no_event_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "CarPropertyInfo", 
                                       {"propertyInfo":{"obcCurrentMax":-1}})     
    
    @allure.title("车辆配置字信息_首次启动默认值_记忆tcp数据")
    @pytest.mark.full
    def test_caseid_1979631(self):
        self.sd_tester.write_multi_ccp({x: 0x1 for x in range(1, 1557)})
        self.del_s2s_db()
        self.update_bgm_s2s_json({"tcpResClientPort": 30506,
                                  "tcpResServerPort": 30506}, partner_key=CARCONFIG_SERVICE_CLIENT)
        self.partner.ck_no_event_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "NotifyConfigList", 
                                             {"out": [{"name": x,"value": 255} for x in range(1, 1557)]},
                                             method_args={"names": [x for x in range(1, 1557)]},timeout=2)
        
        self.update_bgm_s2s_json({}, partner_key=CARCONFIG_SERVICE_CLIENT)
        sleep(8)
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", 
                                              {"names": [x for x in range(1, 1557)]}, 
                                              {"out": [{"name": x,"value": 1} for x in range(1, 1557)]},timeout=2)
        
        self.update_bgm_s2s_json({"tcpResClientPort": 30506,
                                  "tcpResServerPort": 30506}, partner_key=CARCONFIG_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", 
                                              {"names": [x for x in range(1, 1557)]}, 
                                              {"out": [{"name": x,"value": 1} for x in range(1, 1557)]},timeout=2)

    @allure.title("续航能耗属性信息_先使用记忆值_再根据mcu数据触发event")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1983487(self):  # V1.4新增接口 
        self.sd_tester.write_multi_ccp({3: 129, 566: 16, 950: 2})
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                              {"out":return_EnergyConsumptionData(98.69999694824219,880,11.220000267028809,730,13.520000457763672,599,19.0)})
        
        self.update_bgm_s2s_json({"tcpResClientPort": 30506,
                                  "tcpResServerPort": 30506}, partner_key=CARCONFIG_SERVICE_CLIENT)
        self.partner.ck_event_and_resp(CARCONFIG_SERVICE_CLIENT, 
                                                       "NotifyEnergyConsumptionData",
                                                       {"data":return_EnergyConsumptionData(98.69999694824219,880,11.220000267028809,730,13.520000457763672,599,19.0)})
        
        self.sd_tester.write_multi_ccp({3: 129, 566: 16, 950: 1,966:0})
        self.update_bgm_s2s_json({}, partner_key=CARCONFIG_SERVICE_CLIENT)
        sleep(8)
        event1 = self.partner.return_latest_event(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData")
        assert ck_data(event1, {"data": return_EnergyConsumptionData(97.68, 720, 13.57, 595, 16.42,599,19.0)})
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetEnergyConsumptionData", {},
                                              {"out": return_EnergyConsumptionData(97.68, 720, 13.57, 595, 16.42,599,19.0)})    
    
    @allure.title("获取续航能耗属性信息_首次下线默认值")
    @pytest.mark.full
    def test_caseid_1983480(self):  # V1.4新增接口
        # 该case放最下面，否则删数据库后，不重启BGM无法生成新数据库，也就无记忆值，block其他几个case
        self.del_s2s_db()
        self.partner.empty_all()
        self.update_bgm_s2s_json({"tcpResClientPort": 30506,
                                  "tcpResServerPort": 30506}, partner_key=CARCONFIG_SERVICE_CLIENT)
        sleep(8)  # 服务上线后要等待加载数据库，等待Service Run End
        self.partner.ck_no_event_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "NotifyEnergyConsumptionData",
                                             {"out": return_EnergyConsumptionData(0.0, 0, 0.0, 0, 0.0,599,19.0)})
    