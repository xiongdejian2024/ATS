#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_EntryService.py
@Time         :2023/04/30 19:07:31
@Author       :peipei.yang_ext@jiduauto.com
@Description  :
"""
import allure
import pytest
from xat_ecu.legacy.sdk.sdk_tools import check_pdu, get_pdu_value_and_time
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.sdk.driver.jidutest_io.io.io_system import IOSystem
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.soa.case_helper.utils import *


COCKPITPERCEPTION_SERVICE_CLIENT = "cockpit_perception_service_server"

def get_signal_changed_timestamp(items, pre_value, changed_value):
    """获取信号跳变为期望值时的时间戳"""
    for i in range(1, len(items)):
        if items[i-1][2] == pre_value and items[i][2] == changed_value:
            return float(items[i][1])
    assert False, f"遍历完未找到跳变为{changed_value}的情况"


@allure.feature("SOA服务接口")
@allure.story("整车控制/WiperService")
@pytest.mark.wiper
class TestWiperService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("WiperService", "client"),
                                     ("VehicleModeService", "client"),
                                     ("CentralLockService", "client"),
                                     ("WindowAppService", "client"),
                                     ("cockpit_perception_service","server"),
                                     ("WindowService", "client"),
                                     ("SeatService", "client"),
                                     ("InteractiveService","server")])
        self.partner.method_default_timeout = 0.1
        self.sd_tester.tester_present()
        self.ipdu.lin1_wakeup()#唤醒lin1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')#车辆静止
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1) # MPU侧档位
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)  
        self.sd_tester.write_multi_ccp({94: 0x80, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x4, 578: 0x4})
        self.sd_tester.change_car_mode(0)
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.io.init_bgm_HW()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.start_mode = 2
        self.end_mode = 2
        self.driver_occupy_flag=False

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        # self.dk.stop_listen_dk_bgm_response() #
        # self.ipdu.lin1_reset_wakeup()#停止唤醒 #
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.set_nopeople_incar()
        self.ipdu.rx_flag_reset_all()
        self.ipdu.set_vehspd(0)
        sleep(1)
        self.sd_tester.change_usage_mode(11)
        self.sd_tester.change_car_mode(0)
        # self.ipdu.lin1_wakeup()#唤醒lin1 #
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)#开关按键无故障
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 0)#拨杆按键无故障
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawQf', 3)#舱外光亮度原始数据传感器无故障
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 0)#洗涤液不足无故障
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'RainSnsrActvnErrToHmi', 0)#雨量传感器无故障
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WiprSysFailrDetdSafe', 0)#雨刮控制系统内部无故障
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'SolarSnsrLeValue', 0)
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'SolarSnsrRiValue', 0)
        #雨刮位置信号需要写入ccp(401,2&503,2)
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInWipgArFromWMM', 0)
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInPrkgPosnLoFromWMM', 1)
        self.partner.empty_all(0.5)

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()  # 恢复所有总线
        self.ipdu.set_vehspd(0)
        # sleep(1) #
        # self.sd_tester.change_usage_mode(1) #
        # self.sd_tester.change_car_mode(0) # 
        # sleep(1) # 
        self.start_mode = 2
        self.end_mode = 2
        super().after_each_func(ecu, start=False)

    @pytest.mark.full
    @allure.title("设置雨刮动作禁用&获取雨刮禁用状态&通知雨刮禁用状态__状态机跳转(超时恢复)")  # PASS
    def test_caseid_111435(self):
        for usage_mode in [1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            # 第一种速度满足,模式满足
            self.ipdu.set_vehspd(0.5)
            sleep(1)
            self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": True})
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus",
                                      {"inhibit": {"id": 0, "MoveInhibit": True, "WashInhibit": False}})
            sleep(1)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperInhibitStatus", {},
                                                  {"out": {"id": 0, "MoveInhibit": True, "WashInhibit": False}})
            sleep(1)  # 超时恢复
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus",
                                      {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperInhibitStatus", {},
                                                  {"out": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
    
    @pytest.mark.full
    @allure.title("设置雨刮动作禁用&获取雨刮禁用状态&通知雨刮禁用状态__雨刮动作禁用调用两次")  # PASS  2秒内调用两次逻辑
    def test_caseid_111442(self):
        def inner_test():
            self.ipdu.set_vehspd(0.5)
            sleep(0.5)
            self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit",
                                             {"wipers": 0, "isOn": True})  # 第一次调用
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus",
                                      {"inhibit": {"id": 0, "MoveInhibit": True, "WashInhibit": False}})  # 通知事件下发
            sleep(1)  # 计时器1s
            self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit",
                                             {"wipers": 0, "isOn": True})  # 第二次调用:重新计时
            sleep(1.1)  # 计时器1.1s
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperInhibitStatus", {},
                                                  {"out": {"id": 0, "MoveInhibit": True, "WashInhibit": False}})
            sleep(1)  # 计时器1s
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus",
                                      {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperInhibitStatus", {},
                                                  {"out": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
    
        for usage_mode in [1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            inner_test()
    
    @pytest.mark.sanity
    @allure.title("设置雨刮动作禁用&获取雨刮禁用状态&通知雨刮禁用状态_状态机跳转(车速大于等于1.944m/s)")  # PASS
    def test_caseid_111434(self):
        for usage_mode in [1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            # 第一种速度满足,模式满足
            self.ipdu.set_vehspd(0.5)
            sleep(1)
            self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit",
                                             {"wipers": 0, "isOn": True})
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus",
                                      {"inhibit": {"id": 0, "MoveInhibit": True, "WashInhibit": False}})
            sleep(1)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperInhibitStatus", {},
                                                  {"out": {"id": 0, "MoveInhibit": True, "WashInhibit": False}})
            self.ipdu.set_vehspd(1.944)
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus",
                                      {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperInhibitStatus", {},
                                                  {"out": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
    
    @pytest.mark.full
    @allure.title("设置雨刮动作禁用&获取雨刮禁用状态&通知雨刮禁用状态__雨刮动作未禁用")  # PASS
    def test_caseid_111440(self):
        def inner_test():
            self.ipdu.set_vehspd(0.5)
            self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperWashInhibit", {"wipers": 0, "isOn": True})
            sleep(1)
            self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperWashInhibit", {"wipers": 0, "isOn": False})
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus",
                                      {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperInhibitStatus", {},
                                                  {"out": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
    
        for usage_mode in [1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            inner_test()
    
    @pytest.mark.sanity
    @allure.title("设置雨刮动作禁用&获取雨刮禁用状态&通知雨刮禁用状态__pdu报文下发")  # PASS
    def test_caseid_1980486(self):
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        def inner_test():
            self.ipdu.set_vehspd(0.5)
            sleep(0.5)
            self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": True})
            self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 0}]})
    
        for usage_mode in [1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            inner_test()
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [0])#校验周期列表里面有0
    
    @pytest.mark.full
    @allure.title("设置雨刮洗涤禁用&获取雨刮禁用状态&通知雨刮禁用状态_状态机跳转(超时恢复)")  # PASS
    def test_caseid_108753(self):
        def inner_test():
            self.ipdu.set_vehspd(0.5)  # 第一种速度满足，模式满足
            sleep(1)
            self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperWashInhibit", {"wipers": 0, "isOn": True})
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus",
                                      {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": True}})
            sleep(1)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperInhibitStatus", {},
                                                  {"out": {"id": 0, "MoveInhibit": False, "WashInhibit": True}})
            sleep(1)  # 超时恢复
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus",
                                      {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperInhibitStatus", {},
                                                  {"out": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
    
        for usage_mode in [1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            inner_test()
    
    @pytest.mark.full
    @allure.title("设置雨刮洗涤禁用&获取雨刮禁用状态&通知雨刮禁用状态_调用两次禁用")  # PASS
    def test_caseid_111443(self):
        def inner_test():
            self.ipdu.set_vehspd(0.5)
            sleep(0.2)
            self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperWashInhibit",
                                             {"wipers": 0, "isOn": True})  # 第一次调用
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus",
                                      {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": True}})  # 通知事件下发
            sleep(1)  # 计时器1s
            self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperWashInhibit",
                                             {"wipers": 0, "isOn": True})  # 第二次调用:重新计时
            sleep(1.1)  # 计时器1.1s
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperInhibitStatus", {},
                                                  {"out": {"id": 0, "MoveInhibit": False, "WashInhibit": True}})
            sleep(1)  # 计时器1s
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus",
                                      {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperInhibitStatus", {},
                                                  {"out": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
    
        for usage_mode in [1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            inner_test()
    
    @pytest.mark.sanity
    @allure.title("设置雨刮洗涤禁用&获取雨刮禁用状态&通知雨刮禁用状态_状态机跳转(车速大于等于1.944m/s)")  # PASS
    def test_caseid_111437(self):
        def inner_test():
            self.ipdu.set_vehspd(0.5)  # 第一种速度满足，模式满足
            sleep(1)
            self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperWashInhibit", {"wipers": 0, "isOn": True})
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus",
                                      {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": True}})  # 通知事件下发
            sleep(1)  # 计时器一秒
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperInhibitStatus", {},
                                                  {"out": {"id": 0, "MoveInhibit": False, "WashInhibit": True}})
            self.ipdu.set_vehspd(1.944)
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus",
                                      {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperInhibitStatus", {},
                                                  {"out": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
    
        for usage_mode in [1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            inner_test()
    
    @pytest.mark.full
    @allure.title("设置雨刮洗涤禁用&获取雨刮禁用状态&通知雨刮禁用状态_ 雨刮洗涤未禁用")  # PASS
    def test_caseid_111441(self):
        def inner_test():
            self.ipdu.set_vehspd(0.5)
            self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperWashInhibit", {"wipers": 0, "isOn": True})
            sleep(1)
            self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperWashInhibit", {"wipers": 0, "isOn": False})
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus",
                                      {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperInhibitStatus", {},
                                                  {"out": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
    
        for usage_mode in [1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            inner_test()
    
    @pytest.mark.sanity
    @allure.title("获取|通知雨刮禁用状态_默认值")
    def test_caseid_1980817(self):
        self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT)
        sleep(5)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperInhibitStatus", {},
                                              {"out": {"id": 0, "MoveInhibit": False, "WashInhibit": False}}, timeout=10)

    @pytest.mark.sanity
    @allure.title("设置雨刮洗涤禁用_获取|通知雨刮禁用状态_pdu报文下发")  # PASS
    def test_caseid_1980492(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        def inner_test():
            self.ipdu.set_vehspd(0.5)
            sleep(0.5)
            self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperWashInhibit", {"wipers": 0, "isOn": True})
            self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 0}]})
    
        for usage_mode in [1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            inner_test()
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_signal_values('WinWshrLvrCmd', [0, 0, 0, 0])
    
    @pytest.mark.smoke
    @allure.title("设置雨刮模式") 
    def test_caseid_1980501(self):
        self.sd_tester.write_single_ccp(401, 2)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set_vehspd(0.5)
        sleep(0.2)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit",
                                         {"wipers": 0, "isOn": False})  # 设置动作为未禁用状态
        for mode in [0, 2, 3, 4, 5, 6, 7]:  # 7为error
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode",
                                             {"wipers": [{"id": 0, "mode": mode}]})
            sleep(5)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [mode])
    
    @pytest.mark.sanity
    @allure.title("设置雨刮模式_单刮")  
    def test_caseid_1898767(self):
        self.sd_tester.write_single_ccp(401, 2)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set_vehspd(0.5)
        sleep(1)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit",
                                         {"wipers": 0, "isOn": False})  # 设置动作为未禁用状态
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 0}]})
        sleep(0.5)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 1}]})
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [0, 1, 0])
        assert self.bgm_eth_inter.get_signal_values('FrntWiprSelnModFrntWiprSelnMod').count(1) == 2
    
    @pytest.mark.full
    @allure.title("设置雨刮模式_首次下线")  
    def test_caseid_1980506(self):
        self.del_s2s_db()  # 删除数据库
        self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT)
        sleep(30)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.write_single_ccp(401, 2)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set_vehspd(0.5)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit",
                                         {"wipers": 0, "isOn": False})  # 设置动作为未禁用状态
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [6])

    @allure.title("设置雨刮模式_下电记忆")  # 最后一次记忆值等于@value(6)todo重启和抓包不能同时
    @pytest.mark.full
    def test_caseid_1980508(self):
        self.sd_tester.write_single_ccp(401, 2)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set_vehspd(0.5)
        sleep(1)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit",
                                         {"wipers": 0, "isOn": False})  # 设置动作为未禁用状态
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 6}]})
        self.kill_s2s_and_reconnect_service(WIPER_SERVICE_CLIENT)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [6])
    
    @allure.title("设置雨刮模式_下电记忆")  # 最后一次记忆值不等于@value(6)重启和抓包不能同时 todo
    @pytest.mark.full
    def test_caseid_1980509(self):
        self.sd_tester.write_single_ccp(401, 2)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set_vehspd(0.5)
        sleep(1)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit",
                                         {"wipers": 0, "isOn": False})  # 设置动作为未禁用状态
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 5}]})
        self.partner.empty_all()
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.kill_s2s_and_reconnect_service(WIPER_SERVICE_CLIENT)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [0])

    @allure.title("设置雨刮模式_外部触发源(RKE解锁成功_四门上锁且尾门上锁)")  # 1 最后一次记忆值等于@value(6)
    @pytest.mark.sanity
    def test_caseid_1980513(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.write_single_ccp(401, 2)
        self.sd_tester.change_usage_mode(2)
        sleep(1)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit",
                                         {"wipers": 0, "isOn": False})  # 设置动作为未禁用状态
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 6}]})
        self.dk.send_rke_unlock()
        self.sd_tester.change_usage_mode(1)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [6])

    @allure.title("设置雨刮模式_外部触发源(RKE解锁成功_四门上锁且尾门上锁)")  # 1 最后一次记忆值不等于@value(6)
    @pytest.mark.full
    def test_caseid_1980514(self):
        self.sd_tester.write_single_ccp(401, 2)
        self.sd_tester.change_usage_mode(2)
        sleep(1)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit",
                                         {"wipers": 0, "isOn": False})  # 设置动作为未禁用状态
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 5}]})
        self.partner.empty_all()
        self.dk.send_rke_unlock()
        self.sd_tester.change_usage_mode(1)
        self.dk.set_cenlock_sts(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=1)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [5, 0])

    @allure.title("设置雨刮模式_外部触发源(PE解锁成功_四门上锁且尾门上锁)")  # 2 最后一次记忆值等于@value(6)
    @pytest.mark.sanity
    def test_caseid_1980515(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.write_single_ccp(401, 2)
        self.sd_tester.change_usage_mode(2)
        sleep(1)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit",
                                         {"wipers": 0, "isOn": False})  # 设置动作为未禁用状态
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 6}]})
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.press_door_outswitch(4, 0.5)
        self.sd_tester.change_usage_mode(1)
        self.dk.set_cenlock_sts(3)
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [6])

    @allure.title("设置雨刮模式_外部触发源(PE解锁成功_四门上锁且尾门上锁)")  # 2 最后一次记忆值不等于@value(6)
    @pytest.mark.full
    def test_caseid_1980516(self):
        self.sd_tester.write_single_ccp(401, 2)
        self.sd_tester.change_usage_mode(1)
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 2}]})
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.press_door_outswitch(4, 2.2)
        info1 = {"sts": 3, "triggerId": 2, "updateEve": True}
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info1})
        sleep(1)
        self.dk.set_cenlock_sts(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=1)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [2, 0])

    @allure.title("设置雨刮模式_外部触发源(远程解锁成功)")  # 7 最后一次记忆值等于@value(6)
    @pytest.mark.sanity
    def test_caseid_1980519(self):
        # self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.write_single_ccp(401, 2)
        self.sd_tester.change_usage_mode(2)
        sleep(1)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit",
                                         {"wipers": 0, "isOn": False})  # 设置动作为未禁用状态
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 6}]})
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.dk.send_nfc_cmd()
        self.sd_tester.change_usage_mode(1)
        self.dk.set_cenlock_sts(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [6])

    @allure.title("设置雨刮模式_外部触发源(远程解锁成功)")  # 7 最后一次记忆值不等于@value(6)
    @pytest.mark.full
    def test_caseid_1980520(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.write_single_ccp(401, 2)
        self.sd_tester.change_usage_mode(2)
        sleep(1)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit",
                                         {"wipers": 0, "isOn": False})  # 设置动作为未禁用状态
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 4}]})
        self.dk.send_nfc_cmd()  # 解锁
        sleep(2)
        self.sd_tester.change_usage_mode(1)
        self.dk.set_cenlock_sts(3)  # 闭锁
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [4, 0])

    @allure.title("设置雨刮模式_外部触发源(近车解锁成功)")  # 9 最后一次记忆值等于@value(6)
    @pytest.mark.full
    def test_caseid_1980521(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.write_single_ccp(401, 2)
        self.sd_tester.change_usage_mode(2)
        sleep(1)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit",
                                         {"wipers": 0, "isOn": False})  # 设置动作为未禁用状态
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 6}]})
        self.dk.send_approach_unlock_cmd()  # 解锁
        self.sd_tester.change_usage_mode(1)
        self.dk.set_cenlock_sts(3)  # 闭锁
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [6])

    @allure.title("设置雨刮模式_外部触发源(近车解锁成功)")  # 9 最后一次记忆值不等于@value(6)
    @pytest.mark.sanity
    def test_caseid_1980522(self):
        # self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.write_single_ccp(401, 2)
        self.sd_tester.change_usage_mode(2)
        sleep(1)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit",
                                         {"wipers": 0, "isOn": False})  # 设置动作为未禁用状态
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 4}]})
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.dk.send_approach_unlock_cmd()  # 解锁
        self.sd_tester.change_usage_mode(1)
        self.dk.set_cenlock_sts(3)  # 闭锁
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [0])

    @allure.title("设置雨刮模式_外部触发源(外部的其他方式闭锁成功)")  # 10 最后一次记忆值等于@value(6)
    @pytest.mark.full
    def test_caseid_1980523(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.write_single_ccp(401, 2)
        self.sd_tester.change_usage_mode(2)
        sleep(1)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit",
                                         {"wipers": 0, "isOn": False})  # 设置动作为未禁用状态
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 6}]})
        self.dk.set_cenlock_sts(1)  # 解锁
        self.sd_tester.change_usage_mode(1)
        self.dk.set_cenlock_sts(3)  # 闭锁
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [6])

    @allure.title("设置雨刮模式_外部触发源(外部的其他方式闭锁成功)")  # 10 最后一次记忆值不等于@value(6)
    @pytest.mark.sanity
    def test_caseid_1980524(self):
        # self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.write_single_ccp(401, 2)
        self.sd_tester.change_usage_mode(2)
        sleep(1)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit",
                                         {"wipers": 0, "isOn": False})  # 设置动作为未禁用状态
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 5}]})
        self.dk.set_cenlock_sts(1)  # 解锁
        self.sd_tester.change_usage_mode(1)
        self.dk.set_cenlock_sts(3)  # 闭锁
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [0])

    @allure.title("设置雨刮模式_外部触发源(sourceId不跳变)")  # 12 最后一次记忆值等于@value(6)
    @pytest.mark.full
    def test_caseid_1980525(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.write_single_ccp(401, 2)
        self.sd_tester.change_usage_mode(2)
        sleep(1)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit",
                                         {"wipers": 0, "isOn": False})  # 设置动作为未禁用状态
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 6}]})
        self.dk.send_nfc_cmd()  # 解锁
        self.sd_tester.change_usage_mode(1)
        self.dk.set_cenlock_sts(3)  # 闭锁
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [6])

    @allure.title("设置雨刮模式_外部触发源(sourceId不跳变)")  # 12 最后一次记忆值不等于@value(6)
    @pytest.mark.sanity
    def test_caseid_1980526(self):
        # self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.write_single_ccp(401, 2)
        self.sd_tester.change_usage_mode(2)
        sleep(1)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit",
                                         {"wipers": 0, "isOn": False})  # 设置动作为未禁用状态
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 2}]})
        self.dk.send_nfc_cmd()  # 解锁
        self.sd_tester.change_usage_mode(1)
        self.dk.set_cenlock_sts(3)  # 闭锁
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [0])

    def set_four_seat_occupt(self,A,B,C,D):
        """设置副驾 左后 后中 后右 1/2代表占位 0 代表未占位"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts', A)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe', B)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecMid', C)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecRi', D)
        sleep(1)

    def seat_belt_status(self,A,B,C,D,E):
        """设置主驾 副驾 左后 后中 后右 1代表已系 0 代表未系"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', A)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1', B)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecLeBltLockSt1', C)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecLeBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSt1', D)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecRiBltLockSt1', E)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecRiBltLockSts', 0)
        sleep(1)

    def ck_event_and_resp_SeatOccupyWithCam(self,id,statusWithCam):
        self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "SeatOccupyStatus",
                                        {"infos": [{"seatId": id, "statusWithCam": statusWithCam}]},
                                        "GetOccupied", {"seats": [12]})
        self.partner.ck_event_and_resp(SEAT_SERVICE_CLIENT, "SeatOccupyStatusValidity",
                                        {"infos": [{"value": {"seatId": id, "statusWithCam":statusWithCam}}]},
                                        "GetOccupiedValidity",{"seats": [12]})
    
    def set_four_Door_open(self):
        self.io.drvr_door_open()
        self.io.pass_door_open()
        self.io.lere_door_open()
        self.io.rire_door_open()

    def set_four_Door_close(self):
        self.io.drvr_door_close()
        self.io.pass_door_close()
        self.io.lere_door_close()
        self.io.rire_door_close()

    def Shift_Gear(self, X):
        """0代表P挡 2代表N挡 3代表D挡 1代表R挡"""
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', X)
        sleep(1)

    def precond_wiper_off(self, door_close=True, driver_occupy=False):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 1)#车辆处于静止状态
        
        # # 雨刮不处于维修模式
        # maintain = self.partner.send_request_and_return_resp(WIPER_SERVICE_CLIENT, "GetWiperMaintainceMode", {})['out']
        # logger.info(f"[precond_wiper_off] maintain: {maintain}")
        # if maintain:
        #     self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMaintainceMode", {'on': False})
        #     self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "MaintainceMode", {"on": 0})
        #     self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMaintainceMode", {}, {"out": 0})
            
        self.io.drvr_door_close() if door_close else self.io.drvr_door_open()

        if self.driver_occupy_flag is False:
            self.io.driver_seat_notpresent()
            self.set_four_seat_occupt(0,0,0,0)#副驾 左后 后中 后右未占位
            self.seat_belt_status(0,0,0,0,0)#主驾 副驾 左后 后中 后右安全带未系
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdBrkPedlPsd", 0) 
            sleep(2)
            self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                                {"firstLeftExist":False,"firstRightExist":False,"errorCode":0}})
            self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                            {"seatSts":{"seatStsSecondLeft":{"installSts":False,"occupySts":False},
                                                        "seatStsSecondRight":{"installSts":False,"occupySts":False}}})
            self.driver_occupy_flag=False

        if driver_occupy:
            self.partner.empty_all(1)
            self.io.driver_seat_present()#io控制 主驾占位
            # sleep(2)
            self.ck_event_and_resp_SeatOccupyWithCam(0,1)#主驾有人
            self.driver_occupy_flag=True
  
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit",
                                         {"wipers": 0, "isOn": False}) 
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", 
                                         {"wipers": [{"id": 0, "mode": self.start_mode}]})
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(0.3)
        
    def trigger_wiper_off_by_driver_occupy_to_not(self, check_evnet=True):
        self.partner.empty_all(1)
        self.io.driver_seat_present()#io控制 主驾占位
        if check_evnet:
            self.ck_event_and_resp_SeatOccupyWithCam(0,1)#主驾有人

        self.partner.empty_all(1)
        self.io.driver_seat_notpresent()#主驾无人
        self.ck_event_and_resp_SeatOccupyWithCam(0,0)#主驾占位无人
        sleep(1)
        self.driver_occupy_flag = False
    
    def trigger_wiper_off_by_door_close_open(self):
        self.io.drvr_door_close()
        sleep(0.2)
        self.io.drvr_door_open() #门关到开
        sleep(1)
    
    def exit_wiper_off_by_set_veh_not_still(self, stop_tcp=True):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 4)#退出条件
        if not stop_tcp:
            return
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', 
                                            [self.start_mode, 0, self.end_mode])

    def exit_wiper_off_by_door_close_and_driver_occupy(self, door_close=True, driver_occupy=True, stop_tcp=True):
        if door_close:
            self.io.drvr_door_close()#主驾门关
        if driver_occupy and not self.driver_occupy_flag:
            self.partner.empty_all(1)
            self.io.driver_seat_present()#io控制主驾占位
            self.ck_event_and_resp_SeatOccupyWithCam(0,1)#主驾有人
            self.driver_occupy_flag = True
        elif driver_occupy is False and self.driver_occupy_flag:
            self.partner.empty_all(1)
            self.io.driver_seat_notpresent()#主驾无人
            self.ck_event_and_resp_SeatOccupyWithCam(0,0)#主驾占位无人
            self.driver_occupy_flag = False
        
        logger.info(f"[exit_wiper_off_by_door_close_and_driver_occupy] door_close, driver_occupy:{self.driver_occupy_flag}")
        if not stop_tcp:
            return
        
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        
        if door_close and driver_occupy:
            check_val = [self.start_mode, 0, self.end_mode]
        else:
            check_val = [self.start_mode, 0]
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', check_val)

    def exit_wiper_off_by_set_wiper_mode(self):
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", 
                                         {"wipers": [{"id": 0, "mode": self.end_mode}]})#退出条件
        sleep(1.5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', 
                                            [self.start_mode, 0, self.end_mode])

    @allure.title("设置雨刮模式_车辆处于静止状态+主驾门从关闭→开启(激活)---车辆处于非静止状态(退出条件)")  
    @pytest.mark.full
    def test_caseid_1987722(self):
        self.precond_wiper_off()
        self.trigger_wiper_off_by_door_close_open()
        self.exit_wiper_off_by_set_veh_not_still()
        
    @allure.title("设置雨刮模式_车辆处于静止状态+主驾门从关闭→开启(激活)---主驾门关闭且主驾有人(退出条件)")  
    @pytest.mark.full
    def test_caseid_1987757(self):
        self.start_mode = 3
        self.end_mode = 3
        self.precond_wiper_off()
        self.trigger_wiper_off_by_door_close_open()
        self.exit_wiper_off_by_door_close_and_driver_occupy()
    
    @allure.title("设置雨刮模式_车辆处于静止状态+主驾门从关闭→开启(激活)---雨刮未处于禁用状态时，用户操作雨刮(退出条件)")  
    @pytest.mark.full
    def test_caseid_1987761(self):
        self.start_mode = 2
        self.end_mode = 5
        self.precond_wiper_off()
        self.trigger_wiper_off_by_door_close_open()
        self.exit_wiper_off_by_set_wiper_mode()
    
    @allure.title("设置雨刮模式_车辆处于静止状态+主驾占位从有人→无人(激活)---车辆处于非静止状态(退出条件)")  
    @pytest.mark.full
    def test_caseid_1987765(self):
        self.precond_wiper_off()
        self.trigger_wiper_off_by_driver_occupy_to_not()
        self.exit_wiper_off_by_set_veh_not_still()
    
    @allure.title("设置雨刮模式_车辆静止门关无人+主驾占位从有人→无人(激活)---主驾门关闭且主驾有人(退出条件)")  
    @pytest.mark.full
    def test_caseid_1987769(self):
        self.start_mode = 4
        self.end_mode = 4
        self.precond_wiper_off(door_close=True)
        self.trigger_wiper_off_by_driver_occupy_to_not()
        self.exit_wiper_off_by_door_close_and_driver_occupy()

    @allure.title("设置雨刮模式_车辆静止门开无人+主驾占位从有人→无人(激活)---主驾门关闭且主驾有人(退出条件)")  
    @pytest.mark.full
    def test_caseid_1988184(self): 
        self.start_mode = 4
        self.end_mode = 4
        self.precond_wiper_off(door_close=False)
        self.trigger_wiper_off_by_driver_occupy_to_not()
        self.exit_wiper_off_by_door_close_and_driver_occupy()

    @allure.title("设置雨刮模式_车辆处于静止状态+主驾占位从有人→无人(激活)---雨刮未处于禁用状态时，用户操作雨刮(退出条件)")  
    @pytest.mark.full
    def test_caseid_1987775(self):
        self.start_mode = 2
        self.end_mode = 6
        self.precond_wiper_off()
        self.trigger_wiper_off_by_driver_occupy_to_not()
        self.exit_wiper_off_by_set_wiper_mode()
    
    @allure.title("设置雨刮模式_车辆处于静止状态+主驾门从关闭→开启(激活)---主驾门关闭(不满足退出条件)")  
    @pytest.mark.full
    def test_caseid_1987811(self):
        self.precond_wiper_off()
        self.trigger_wiper_off_by_door_close_open()
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=True, driver_occupy=False)
    
    @allure.title("设置雨刮模式_车辆处于静止状态+主驾占位有人→无人(激活)---主驾占位有人(不满足退出条件)")  
    @pytest.mark.full
    def test_caseid_1987812(self):
        self.precond_wiper_off(door_close=False, driver_occupy=False)
        self.trigger_wiper_off_by_driver_occupy_to_not()
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=False, driver_occupy=True)

    @allure.title("设置雨刮模式_车辆处于静止状态+主驾门从关闭→开启(激活)---主驾门关闭(维持当前mode)---车辆处于非静止状态(退出条件)")  
    @pytest.mark.full
    def test_caseid_1987814(self):
        self.precond_wiper_off()
        self.trigger_wiper_off_by_door_close_open()
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=True, driver_occupy=False, stop_tcp=False)
        self.exit_wiper_off_by_set_veh_not_still()

    @allure.title("设置雨刮模式_车辆处于静止状态+主驾门从关闭→开启(激活)---主驾门关闭(维持当前mode)---主驾门关闭且主驾有人(退出条件)")  
    @pytest.mark.full
    def test_caseid_1987818(self):
        self.precond_wiper_off()
        self.trigger_wiper_off_by_door_close_open()
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=True, driver_occupy=False, stop_tcp=False)
        self.exit_wiper_off_by_door_close_and_driver_occupy()

    @allure.title("设置雨刮模式_车辆处于静止状态+主驾门从关闭→开启(激活)---主驾门关闭(维持当前mode)---用户操作雨刮(退出条件)")  
    @pytest.mark.full
    def test_caseid_1987838(self):
        self.precond_wiper_off()
        self.trigger_wiper_off_by_door_close_open()
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=True, driver_occupy=False, stop_tcp=False)
        self.exit_wiper_off_by_set_wiper_mode()

    @allure.title("设置雨刮模式_车辆处于静止状态+主驾占位有人→无人(激活)---主驾占位有人(维持当前mode)---车辆处于非静止状态(退出条件)")  
    @pytest.mark.full
    def test_caseid_1987839(self):
        self.precond_wiper_off()
        self.trigger_wiper_off_by_driver_occupy_to_not()
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=False, driver_occupy=True, stop_tcp=False)
        self.exit_wiper_off_by_set_veh_not_still()

    @allure.title("设置雨刮模式_车辆处于静止状态+主驾占位有人→无人(激活)---主驾占位有人(维持当前mode)---主驾门关闭且主驾有人(退出条件)")  
    @pytest.mark.full
    def test_caseid_1987840(self):
        self.precond_wiper_off()
        self.trigger_wiper_off_by_driver_occupy_to_not()
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=False, driver_occupy=True, stop_tcp=False)
        self.exit_wiper_off_by_door_close_and_driver_occupy()

    @allure.title("设置雨刮模式_车辆处于静止状态+主驾占位有人→无人(激活)---主驾占位有人(维持当前mode)---用户操作雨刮(退出条件)")  
    @pytest.mark.full
    def test_caseid_1987841(self):
        self.start_mode = 4
        self.end_mode = 6
        self.precond_wiper_off(door_close=False, driver_occupy=False)
        self.trigger_wiper_off_by_driver_occupy_to_not()
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=False, driver_occupy=True, stop_tcp=False)
        self.exit_wiper_off_by_set_wiper_mode()

    @allure.title("设置雨刮模式_车辆处于静止状态+主驾门从关闭→开启(激活)---改变当前mode值---车辆处于非静止状态(退出条件)")  
    @pytest.mark.full
    def test_caseid_1987842(self):
        self.start_mode = 2
        self.end_mode = 6
        self.precond_wiper_off()
        self.trigger_wiper_off_by_door_close_open()
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", 
                                         {"wipers": [{"id": 0, "mode": self.end_mode}]})
        self.exit_wiper_off_by_set_veh_not_still()

    @allure.title("设置雨刮模式_车辆处于静止状态+主驾占位有人→无人(激活)---改变当前mode值---主驾门关闭且主驾有人(退出条件)")  
    @pytest.mark.full
    def test_caseid_1987843(self):
        self.start_mode = 4
        self.end_mode = 2
        self.precond_wiper_off()
        self.trigger_wiper_off_by_driver_occupy_to_not()
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", 
                                         {"wipers": [{"id": 0, "mode": self.end_mode}]})
        self.exit_wiper_off_by_door_close_and_driver_occupy()

    @allure.title("设置雨刮模式_车辆处于静止状态+主驾占位有人→无人(激活)---改变当前mode值---用户操作雨刮(退出条件)")  
    @pytest.mark.full
    def test_caseid_1987844(self):
        self.start_mode = 6
        self.end_mode = 3
        self.precond_wiper_off()
        self.trigger_wiper_off_by_driver_occupy_to_not()
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", 
                                         {"wipers": [{"id": 0, "mode": self.end_mode}]})
        self.exit_wiper_off_by_set_wiper_mode()

    def set_wiper_move_inhibit(self, is_on: bool, check_event: bool = True):
        """
        设置雨刮动作禁用状态
        """
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": is_on}) 
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperInhibitStatus", {}, {"out": 
                                             {"id": 0, "MoveInhibit": is_on, "WashInhibit": False}})
        if check_event:
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus", {"inhibit": 
                                             {"id": 0, "MoveInhibit": is_on, "WashInhibit": False}})

    @allure.title("主驾无人关雨刮_前置条件都不满足_车辆非静止雨刮处于禁用状态")  
    @pytest.mark.full
    def test_caseid_1987845(self):
        self.precond_wiper_off()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 6)
        
        self.set_wiper_move_inhibit(True)
        sleep(1)
        self.trigger_wiper_off_by_door_close_open()
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=3)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0, self.start_mode])

    @allure.title("主驾无人关雨刮_前置条件不满足_车辆静止雨刮处于禁止状态")  
    @pytest.mark.sanity
    def test_caseid_1989317(self):
        self.precond_wiper_off()
        
        self.set_wiper_move_inhibit(True)
        sleep(1)
        
        self.trigger_wiper_off_by_door_close_open()
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=3)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0, self.start_mode])

    @allure.title("主驾无人关雨刮_前置条件不满足_车辆非静止雨刮不处于禁止状态")  
    @pytest.mark.full
    def test_caseid_1989318(self):
        self.precond_wiper_off()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 6)
        
        self.trigger_wiper_off_by_door_close_open()
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode])
        
    @allure.title("门关无人(前提)_门关到开(激活)_雨刮禁用_车辆非静止(仅功能退出)")  
    @pytest.mark.smoke
    def test_caseid_1989490(self):
        self.precond_wiper_off(door_close=True, driver_occupy=False)
        self.trigger_wiper_off_by_door_close_open()
        self.set_wiper_move_inhibit(True)
        self.exit_wiper_off_by_set_veh_not_still(stop_tcp=False)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=4)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0, self.start_mode])

    @allure.title("门关无人(前提)_门关到开(激活)_雨刮禁用_门关有人(仅功能退出)")  
    @pytest.mark.sanity
    def test_caseid_1989494(self):
        self.precond_wiper_off(door_close=True, driver_occupy=False)
        self.trigger_wiper_off_by_door_close_open()
        self.set_wiper_move_inhibit(True)
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=True, driver_occupy=True, stop_tcp=False)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=4)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0, self.start_mode])

    @allure.title("门关无人(前提)_门关到开(激活)_雨刮禁用_门关无人(不退出)")  
    @pytest.mark.full
    def test_caseid_1989497(self):
        self.precond_wiper_off(door_close=True, driver_occupy=False)
        self.trigger_wiper_off_by_door_close_open()
        self.set_wiper_move_inhibit(True)
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=True, driver_occupy=False, stop_tcp=False)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=4)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0])

    @allure.title("门关无人(前提)_门关到开(激活)_雨刮禁用_门开无人(不退出)")  
    @pytest.mark.full
    def test_caseid_1989498(self):
        self.precond_wiper_off(door_close=True, driver_occupy=False)
        self.trigger_wiper_off_by_door_close_open()
        self.set_wiper_move_inhibit(True)
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=False, driver_occupy=False, stop_tcp=False)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=4)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0])

    @allure.title("门关无人(前提)_门关到开(激活)_雨刮禁用_门开有人(不退出)")  
    @pytest.mark.full
    def test_caseid_1989499(self):
        self.precond_wiper_off(door_close=True, driver_occupy=False)
        self.trigger_wiper_off_by_door_close_open()
        self.set_wiper_move_inhibit(True)
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=False, driver_occupy=True, stop_tcp=False)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=4)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0])

    @allure.title("门开有人(前提)_门关到开(激活)_雨刮禁用_车辆非静止(仅功能退出)")  
    @pytest.mark.sanity
    def test_caseid_1989500(self):
        self.precond_wiper_off(door_close=False, driver_occupy=True)
        self.trigger_wiper_off_by_door_close_open()
        self.set_wiper_move_inhibit(True)
        self.exit_wiper_off_by_set_veh_not_still(stop_tcp=False)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=4)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0, self.start_mode])

    @allure.title("门开有人(前提)_门关到开(激活)_雨刮禁用_门关有人(仅功能退出)")  
    @pytest.mark.full
    def test_caseid_1989501(self):
        self.precond_wiper_off(door_close=False, driver_occupy=True)
        self.trigger_wiper_off_by_door_close_open()
        self.set_wiper_move_inhibit(True)
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=True, driver_occupy=True, stop_tcp=False)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=4)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0, self.start_mode])

    @allure.title("门开有人(前提)_门关到开(激活)_雨刮禁用_门关无人(不退出)")  
    @pytest.mark.full
    def test_caseid_1989502(self):
        self.precond_wiper_off(door_close=False, driver_occupy=True)
        self.trigger_wiper_off_by_door_close_open()
        self.set_wiper_move_inhibit(True)
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=False, driver_occupy=False, stop_tcp=False)
        sleep(0.2)
        self.io.drvr_door_close()
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=4)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0])

    @allure.title("门开有人(前提)_门关到开(激活)_雨刮禁用_门开无人(不退出)")  
    @pytest.mark.full
    def test_caseid_1989503(self):
        self.precond_wiper_off(door_close=False, driver_occupy=True)
        self.trigger_wiper_off_by_door_close_open()
        self.set_wiper_move_inhibit(True)
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=False, driver_occupy=False, stop_tcp=False)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=4)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0])

    @allure.title("门开有人(前提)_门关到开(激活)_雨刮禁用_门开有人(不退出)")  
    @pytest.mark.sanity
    def test_caseid_1989504(self):
        self.precond_wiper_off(door_close=False, driver_occupy=True)
        self.trigger_wiper_off_by_door_close_open()
        self.set_wiper_move_inhibit(True)
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=False, driver_occupy=True, stop_tcp=False)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=4)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0])

    @allure.title("门关有人(前提)_有人到无(激活)_雨刮禁用_车辆非静止(仅功能退出)")  
    @pytest.mark.sanity
    def test_caseid_1989507(self):
        self.precond_wiper_off(door_close=True, driver_occupy=True)
        self.trigger_wiper_off_by_driver_occupy_to_not(check_evnet=False)
        self.set_wiper_move_inhibit(True)
        self.exit_wiper_off_by_set_veh_not_still(stop_tcp=False)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=4)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0, self.start_mode])

    @allure.title("门关有人(前提)_有人到无(激活)_雨刮禁用_门关有人(仅功能退出)")  
    @pytest.mark.smoke
    def test_caseid_1989511(self):
        self.precond_wiper_off(door_close=True, driver_occupy=True)
        self.trigger_wiper_off_by_driver_occupy_to_not(check_evnet=False)
        self.set_wiper_move_inhibit(True)
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=True, driver_occupy=True, stop_tcp=False)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=4)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0, self.start_mode])

    @allure.title("门关有人(前提)_有人到无(激活)_雨刮禁用_门关无人(不退出)")  
    @pytest.mark.full
    def test_caseid_1989508(self):
        self.precond_wiper_off(door_close=True, driver_occupy=True)
        self.trigger_wiper_off_by_driver_occupy_to_not(check_evnet=False)
        self.set_wiper_move_inhibit(True)
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=True, driver_occupy=False, stop_tcp=False)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=4)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0])

    @allure.title("门关有人(前提)_有人到无(激活)_雨刮禁用_门开无人(不退出)")  
    @pytest.mark.full
    def test_caseid_1989509(self):
        self.precond_wiper_off(door_close=True, driver_occupy=True)
        self.trigger_wiper_off_by_driver_occupy_to_not(check_evnet=False)
        self.set_wiper_move_inhibit(True)
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=False, driver_occupy=False, stop_tcp=False)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=4)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0])

    @allure.title("门关有人(前提)_有人到无(激活)_雨刮禁用_门开有人(不退出)")  
    @pytest.mark.full
    def test_caseid_1989510(self):
        self.precond_wiper_off(door_close=True, driver_occupy=True)
        self.trigger_wiper_off_by_driver_occupy_to_not(check_evnet=False)
        self.set_wiper_move_inhibit(True)
        self.io.drvr_door_open()
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=False, driver_occupy=True, stop_tcp=False)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=4)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0])

    @allure.title("门开无人(前提)_有人到无(激活)_雨刮禁用_车辆非静止(仅功能退出)")  
    @pytest.mark.sanity
    def test_caseid_1989513(self):
        self.precond_wiper_off(door_close=False, driver_occupy=False)
        self.trigger_wiper_off_by_driver_occupy_to_not()
        self.set_wiper_move_inhibit(True)
        self.exit_wiper_off_by_set_veh_not_still(stop_tcp=False)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=4)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0, self.start_mode])

    @allure.title("门开无人(前提)_有人到无(激活)_雨刮禁用_门关有人(仅功能退出)")  
    @pytest.mark.sanity
    def test_caseid_1989512(self):
        self.precond_wiper_off(door_close=False, driver_occupy=False)
        self.trigger_wiper_off_by_driver_occupy_to_not()
        self.set_wiper_move_inhibit(True)
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=True, driver_occupy=True, stop_tcp=False)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=4)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0, self.start_mode])

    @allure.title("门开无人(前提)_有人到无(激活)_雨刮禁用_门关无人(不退出)")  
    @pytest.mark.full
    def test_caseid_1989514(self):
        self.precond_wiper_off(door_close=False, driver_occupy=False)
        self.trigger_wiper_off_by_driver_occupy_to_not()
        self.set_wiper_move_inhibit(True)
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=True, driver_occupy=False, stop_tcp=False)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=4)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0])

    @allure.title("门开无人(前提)_有人到无(激活)_雨刮禁用_门开无人(不退出)")  
    @pytest.mark.full
    def test_caseid_1989515(self):
        self.precond_wiper_off(door_close=False, driver_occupy=False)
        self.trigger_wiper_off_by_driver_occupy_to_not()
        self.set_wiper_move_inhibit(True)
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=False, driver_occupy=False, stop_tcp=False)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=4)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0])

    @allure.title("门开无人(前提)_有人到无(激活)_雨刮禁用_门开有人(不退出)")  
    @pytest.mark.full
    def test_caseid_1989516(self):
        self.precond_wiper_off(door_close=False, driver_occupy=False)
        self.trigger_wiper_off_by_driver_occupy_to_not()
        self.set_wiper_move_inhibit(True)
        self.exit_wiper_off_by_door_close_and_driver_occupy(door_close=False, driver_occupy=True, stop_tcp=False)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=4)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0])


    @allure.title("主驾无人关雨刮已激活_雨刮处于维修模式")  
    @pytest.mark.full
    def test_caseid_1989319(self):
        self.precond_wiper_off()
        self.trigger_wiper_off_by_door_close_open()
        
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMaintainceMode", {'on': True})
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "MaintainceMode", {"on": 1})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMaintainceMode", {}, {"out": 1})
        
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0])

    @allure.title("主驾无人关雨刮已激活_雨刮退出禁用状态_2s计时器前处于刮刷")  
    @pytest.mark.full
    def test_caseid_1989320(self):
        self.sd_tester.write_multi_ccp({401: 2, 503: 2})
        self.precond_wiper_off()
        self.trigger_wiper_off_by_door_close_open()
        
        # 雨刮处于刮刷区域退出禁用状态
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInWipgArFromWMM', 0) 
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInPrkgPosnLoFromWMM', 0)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0}, {"out": 1}, timeout=2) # 雨刮处于刮刷区域
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": True})
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus", {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
        sleep(3)

        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(2)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0])
        
    @allure.title("主驾无人关雨刮已激活_雨刮退出禁用状态_2s计时器前处于park")  
    @pytest.mark.full
    def test_caseid_1989321(self):
        self.sd_tester.write_multi_ccp({401: 2, 503: 2})
        self.precond_wiper_off()
        self.trigger_wiper_off_by_door_close_open()
        
        # 雨刮处于park区域退出禁用状态
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInWipgArFromWMM', 0) 
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInPrkgPosnLoFromWMM', 1)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0}, {"out": 0}, timeout=2) # 雨刮处于park区域
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": True})
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus", {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
        sleep(3)

        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(2)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0])        

    @allure.title("主驾无人关雨刮已激活_雨刮退出禁用状态_2s计时器内改变mode值")  
    @pytest.mark.full
    def test_caseid_1989322(self):
        self.sd_tester.write_multi_ccp({401: 2, 503: 2})
        self.precond_wiper_off()
        self.trigger_wiper_off_by_door_close_open()
        
        # 雨刮处于刮刷区域退出禁用状态
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInWipgArFromWMM', 0) 
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInPrkgPosnLoFromWMM', 0)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0}, {"out": 1}, timeout=2) # 雨刮处于刮刷区域
        
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": True})
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus", {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
        sleep(0.5)
        # 改变mode值为4
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 4}]})
        
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(3)
        # self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0, 4])

        items = self.bgm_eth_inter.get_signal_items('FrntWiprSelnModFrntWiprSelnMod')
        t1 = get_signal_changed_timestamp(items, self.start_mode, 0)
        t2 = get_signal_changed_timestamp(items, 0, 4)
        assert 2.8 < t2 - t1 < 4
        
    @allure.title("主驾无人关雨刮已激活_雨刮退出禁用状态_2s计时器内改变雨刮位置")  
    @pytest.mark.full
    def test_caseid_1989323(self):
        self.sd_tester.write_multi_ccp({401: 2, 503: 2})
        self.precond_wiper_off()
        self.trigger_wiper_off_by_door_close_open()
        
        # 雨刮处于刮刷区域退出禁用状态
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInWipgArFromWMM', 0) 
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInPrkgPosnLoFromWMM', 0)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0}, {"out": 1}, timeout=2) # 雨刮处于刮刷区域
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": True})
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus", {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
        sleep(1)
        # 改变mode值为4
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInWipgArFromWMM', 0) 
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInPrkgPosnLoFromWMM', 1)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0}, {"out": 0}, timeout=2) # 雨刮处于park区域
        
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(3)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0])
        
    @allure.title("主驾无人关雨刮已退出_雨刮退出禁用状态_2s计时器前处于刮刷")  
    @pytest.mark.full
    def test_caseid_1989324(self):
        self.sd_tester.write_multi_ccp({401: 2, 503: 2})
        self.precond_wiper_off()
        self.trigger_wiper_off_by_door_close_open()
        self.exit_wiper_off_by_set_veh_not_still()
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        # 雨刮处于刮刷区域退出禁用状态
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInWipgArFromWMM', 0) 
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInPrkgPosnLoFromWMM', 0)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0}, {"out": 1}, timeout=2) # 雨刮处于刮刷区域
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": True})
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus", {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
        sleep(3)

        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(1)
        # self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.end_mode, 0, self.end_mode]) 
        
        items = self.bgm_eth_inter.get_signal_items('FrntWiprSelnModFrntWiprSelnMod')
        t1 = get_signal_changed_timestamp(items, self.end_mode, 0)
        t2 = get_signal_changed_timestamp(items, 0, self.end_mode)
        assert 3.8 < t2 - t1 < 4.3    
        
    @allure.title("主驾无人关雨刮已退出_雨刮退出禁用状态_2s计时器前处于park")  
    @pytest.mark.full
    def test_caseid_1989325(self):
        self.sd_tester.write_multi_ccp({401: 2, 503: 2})
        self.precond_wiper_off()
        self.trigger_wiper_off_by_door_close_open()
        self.exit_wiper_off_by_set_veh_not_still()
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        # 雨刮处于park区域退出禁用状态
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInWipgArFromWMM', 0) 
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInPrkgPosnLoFromWMM', 1)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0}, {"out": 0}, timeout=2) # 雨刮处于park区域
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": True})
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus", {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
        sleep(3)

        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(1)
        # self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.end_mode, 0, self.end_mode]) 
        items = self.bgm_eth_inter.get_signal_items('FrntWiprSelnModFrntWiprSelnMod')
        t1 = get_signal_changed_timestamp(items, self.end_mode, 0)
        t2 = get_signal_changed_timestamp(items, 0, self.end_mode)
        assert 2.0 < t2 - t1 < 2.5    
        
        
        
        
        
        
        
    @allure.title("设置雨刮模式_车辆处于非静止状态+主驾门从关闭→开启 (前置条件不满足，不激活）->再激活")  
    @pytest.mark.full
    def test_caseid_1988186(self):  
        self.precond_wiper_off()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 6)
        self.trigger_wiper_off_by_door_close_open()
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode])

        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.trigger_wiper_off_by_door_close_open()
        self.exit_wiper_off_by_set_veh_not_still()

    @allure.title("设置雨刮模式_重复激活雨刮关闭后退出")  
    @pytest.mark.full
    def test_caseid_1988187(self):  
        self.precond_wiper_off()
        self.trigger_wiper_off_by_door_close_open()
        self.exit_wiper_off_by_set_wiper_mode()

        self.bgm_eth_inter.start_bgm_tcpdump()
        self.trigger_wiper_off_by_driver_occupy_to_not()
        self.exit_wiper_off_by_set_wiper_mode()

    @allure.title("设置雨刮模式_激活雨刮关闭_设置单刮模式（不退出）")  
    @pytest.mark.full
    def test_caseid_1988188(self):  
        self.start_mode = 4
        self.precond_wiper_off()
        self.trigger_wiper_off_by_door_close_open()
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode",  {"wipers": [{"id": 0, "mode": 1}]}) # 服务设置单刮
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod',  [self.start_mode, 0, 1, 0])
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode",  {"wipers": [{"id": 0, "mode": 4}]})
        
        self.precond_wiper_off()
        self.trigger_wiper_off_by_driver_occupy_to_not()
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 1) # 按键触发单刮
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperOneshotSts", {"info": {"id": 0, "sts": 1}})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod',  [self.start_mode, 0, 1, 0])
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode",  {"wipers": [{"id": 0, "mode": 4}]})

        self.precond_wiper_off()
        self.trigger_wiper_off_by_driver_occupy_to_not()
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 0) # 拨杆触发单刮
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 1)
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 0) 
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperOneshotSts", {"info": {"id": 0, "sts": 1}})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod',  [self.start_mode, 0, 1, 0])
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode",  {"wipers": [{"id": 0, "mode": 4}]})

    @allure.title("主驾无人关雨刮已激活_设置单刮模式同时满足退出条件_检查单刮报文不会被打断")  
    @pytest.mark.full
    def test_caseid_1989603(self):  
        ret = False
        self.precond_wiper_off()
        self.trigger_wiper_off_by_driver_occupy_to_not()
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode",  {"wipers": [{"id": 0, "mode": 1}]}) # 服务设置单刮
        sleep(0.15)
        self.exit_wiper_off_by_set_veh_not_still(stop_tcp=False)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod',  [self.start_mode, 0, 1, self.start_mode])
        signal_list = self.bgm_eth_inter.get_signal_items('FrntWiprSelnModFrntWiprSelnMod')
        for i in range(2, len(signal_list)-2):
            if signal_list[i][2] == 1 and signal_list[i+1][2] == 1:
                ret = True
        if not ret:
            assert False, "服务单刮报文被打断"
        
        ret = False
        self.precond_wiper_off()
        self.trigger_wiper_off_by_driver_occupy_to_not()
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 1) # 按键触发单刮
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        sleep(0.05)
        self.io.drvr_door_close()
        self.io.driver_seat_present()
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod',  [self.start_mode, 0, 1, self.start_mode])
        signal_list = self.bgm_eth_inter.get_signal_items('FrntWiprSelnModFrntWiprSelnMod')
        for i in range(2, len(signal_list)-2):
            if signal_list[i][2] == 1 and signal_list[i+1][2] == 1:
                ret = True
        if not ret:
            assert False, "按键单刮报文被打断"

        ret = False
        self.precond_wiper_off()
        self.trigger_wiper_off_by_driver_occupy_to_not()
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 1) # 拨杆触发单刮
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 0) 
        sleep(0.1)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode",  {"wipers": [{"id": 0, "mode": 4}]})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod',  [self.start_mode, 0, 1, 4])
        signal_list = self.bgm_eth_inter.get_signal_items('FrntWiprSelnModFrntWiprSelnMod')
        for i in range(2, len(signal_list)-2):
            if signal_list[i][2] == 1 and signal_list[i+1][2] == 1:
                ret = True
        if not ret:
            assert False, "拨杆单刮报文被打断"

    @allure.title("设置雨刮模式_激活雨刮关闭后退出_重启后检查周期报文")  
    @pytest.mark.full
    def test_caseid_1987880(self):
        self.end_mode = 6
        self.precond_wiper_off()
        self.trigger_wiper_off_by_door_close_open()
        self.exit_wiper_off_by_set_wiper_mode()

        self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.write_single_ccp(401, 2)
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": False}) 

        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.end_mode])

    @allure.title("设置雨刮模式_激活雨刮关闭后退出_启动阶段未收到门和座椅状态检查周期报文")  
    @pytest.mark.full
    def test_caseid_1987881(self):
        self.precond_wiper_off()
        self.trigger_wiper_off_by_door_close_open()
        self.exit_wiper_off_by_set_wiper_mode()
        self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.empty_all()
        self.bgm_eth_inter.start_bgm_tcpdump()
        # self.ipdu.pause_bus_send("bodycan") 

        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [0])
        
    @allure.title("设置雨刮模式_雨刮处于禁用状态_激活触发条件，条件不触发但仍周期发送0的报文")  
    @pytest.mark.full
    def test_caseid_1987882(self):
        self.precond_wiper_off()
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": True})
        self.trigger_wiper_off_by_door_close_open()
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array('FrntWiprSelnModFrntWiprSelnMod', [self.start_mode, 0])
        
    @pytest.mark.smoke
    @allure.title("获取|通知下雨事件 测试")  # PASS
    def test_caseid_108736(self):
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'RainDetected', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'RainDetected', 1)
        sleep(0.1)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "RainStatusRestricted", {"status": 1})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetRainStatusRestricted", {}, {"out": 1})
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'RainDetected', 0)
        sleep(0.1)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "RainStatusRestricted", {"status": 0})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetRainStatusRestricted", {}, {"out": 0})

    @pytest.mark.full
    @allure.title("获取|通知下雨事件_默认值")  
    def test_caseid_1980779(self):
        for ted in [1, 0]:
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'RainDetected', ted)
            self.partner.empty_all(0.5)
            self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT, resume_all_bus=False)            
            sleep(5)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetRainStatusRestricted", {}, {"out": 0}, timeout=10)
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "RainStatusRestricted", {"status": ted}, timeout=1)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetRainStatusRestricted", {}, {"out": ted},
                                                timeout=2)

    @allure.title("设置雨刮维修模式_1")
    @pytest.mark.sanity
    def test_caseid_1980002(self):
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr06, 'GearLvrIndcn', 0)
        sleep(0.2)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMaintainceMode", {'on': True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr67, 'WiprFrntSrvModReq', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("WiprFrntSrvModReq", [1, 1, 1, 0])
    
    @allure.title("设置雨刮维修模式_0")
    @pytest.mark.sanity
    def test_caseid_1984897(self):
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr06, 'GearLvrIndcn', 0)
        sleep(0.2)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMaintainceMode", {'on': False})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr67, 'WiprFrntSrvModReq', 2, timeout=0.5)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 0)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("WiprFrntSrvModReq", [2, 2, 2, 0])

    @allure.title("设置雨刮维修模式_打断逻辑")
    @pytest.mark.full
    def test_caseid_1980555(self):
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr06, 'GearLvrIndcn', 0)
        # ("设置P档")
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMaintainceMode", {'on': False})
        sleep(0.1)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMaintainceMode", {'on': True})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("WiprFrntSrvModReq", [2, 1, 1, 1, 0])

    @pytest.mark.smoke
    @allure.title("获取雨量大小&通知雨量大小")
    def test_caseid_108756(self):
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'RainfallAmnt', 0)
        self.partner.empty_all(0.5)
        for Rain in range(1, 16):
            logger.info(f"打印{Rain}")
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'RainfallAmnt', Rain)
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "Rainlevel", {"level": Rain}, timeout=3)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetRainlevel", {}, {"out": Rain}, timeout=3)

    @pytest.mark.full
    @allure.title("获取雨量大小&通知雨量大小_默认值")
    def test_caseid_1980830(self):
        for Rain in [14, 0]:
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'RainfallAmnt', Rain)
            self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT, resume_all_bus=False)            
            sleep(5)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetRainlevel", {}, {"out": 14}, timeout=10)
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "Rainlevel", {"level": Rain}, timeout=10)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetRainlevel", {}, {"out": Rain}, timeout=2)

    @pytest.mark.sanity
    @allure.title("获取环境光强度信息&通知环境光强度信息")  
    def test_caseid_108739(self):
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawTwliBriRaw', 0)
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawQf', 0)
        self.partner.empty_all(0.5)
        for QF in [0, 1, 2, 3]:
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawQf', QF)
            if QF in [1, 2, 0]:
                QF = False
            else:
                QF = True
            for Raw in [100, 1000, 10000, 16383, 0]:
                self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawTwliBriRaw', Raw)
                logger.info(f'发到{Raw}')
                self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "LightLux", {"lux": Raw})
                self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetRawLightLux", {},
                                                      {"out": {"value": Raw, "isValid": QF}})

    @pytest.mark.full
    @allure.title("获取环境光强度信息&通知环境光强度信息_默认值")
    def test_caseid_1980565(self):
        for Raw in [100, 0]:
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawTwliBriRaw', Raw)
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawQf', 3)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetRawLightLux", {},
                                                {"out": {"value": Raw, "isValid": True}})
            self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetRawLightLux", {},
                                                {"out": {"value": 0, "isValid": False}}, timeout=10)
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "LightLux", {"lux": Raw})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetRawLightLux", {},
                                                {"out": {"value": Raw, "isValid": True}})

    @pytest.mark.sanity
    @allure.title("获取阳光强度&通知阳光强度")
    def test_caseid_108744(self):
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'SolarSnsrLeValue', 1)
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'SolarSnsrRiValue', 1)
        self.partner.empty_all(0.5)
        for LeValue in [5, 100, 254, 255, 0]:
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'SolarSnsrLeValue', LeValue)
            for RiValue in [5, 100, 254, 255, 0]:
                self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'SolarSnsrRiValue', RiValue)
                self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SolarValue",
                                          {"value": {"driverValue": LeValue * 5, "passengerValue": RiValue * 5}})
                self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSolarValue", {},
                                                      {"out": {"driverValue": LeValue * 5,
                                                               "passengerValue": RiValue * 5}})

    @pytest.mark.full
    @allure.title("获取阳光强度&通知阳光强度_默认值")  
    def test_caseid_1980579(self):
        for sts in [254, 0]:
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'SolarSnsrLeValue', sts)
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'SolarSnsrRiValue', sts)
            self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSolarValue", {},
                                                {"out": {"driverValue": 254, "passengerValue": 254}}, timeout=10)
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SolarValue",
                                {"value": {"driverValue": sts* 5, "passengerValue": sts* 5}}, timeout=10)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSolarValue", {},
                                                {"out": {"driverValue": sts* 5, "passengerValue": sts* 5}}, timeout=2)

    @pytest.mark.sanity
    @allure.title("通知/获取雨刮开关状态")  # V2.2
    def test_caseid_1989041(self):
        # SteerWhlTouchSwtRi3信号值长度为2bit, 取值只能是0，1，2，3
        for i in [1, 0, 2]: 
            logger.info(f"SteerWhlTouchSwtRi3:{i}")
            self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', i)
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SwitchStatus", {"status": i, "wipers": 0})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSwitchStatus", {"wipers": 0}, {"out": i})

        for i in [1, 0, 2, 4]:
            logger.info(f"LeverSwtLeLvrSwt3:{i}")
            sts = 2 if i == 4 else i
            self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', i)
            if i == 4:
                self.partner.ck_no_event(WIPER_SERVICE_CLIENT, "SwitchStatus")
            else:
                self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SwitchStatus", {"status": sts, "wipers": 0})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSwitchStatus", {"wipers": 0}, {"out": sts})
            
        # SteerWhlTouchSwtRi3 != 3 && LeverSwtLeLvrSwt3 = 3
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 3)
        self.partner.ck_no_event(WIPER_SERVICE_CLIENT, "SwitchStatus")

        # SteerWhlTouchSwtRi3 = 3 && LeverSwtLeLvrSwt3 != 3
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 4)
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 3)
        self.partner.ck_no_event(WIPER_SERVICE_CLIENT, "SwitchStatus")
        
        # SteerWhlTouchSwtRi3 = 3 && LeverSwtLeLvrSwt3 = 3
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 3)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SwitchStatus", {"status": 3, "wipers": 0})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSwitchStatus", {"wipers": 0}, {"out": 3})
        
    @pytest.mark.full
    @allure.title("通知/获取雨刮开关状态_无效值(other状态)")  # V2.2
    def test_caseid_1989042(self):
        # LeverSwtLeLvrSwt3从无效值(4) → 0,1,2,3
        for i in [0, 1, 2, 3]:
            self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 4)
            sleep(0.1)
            self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', i)
            self.partner.ck_no_event(WIPER_SERVICE_CLIENT, "SwitchStatus")
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSwitchStatus", {"wipers": 0}, {"out": 0})

    @pytest.mark.full
    @allure.title("通知/获取雨刮开关状态_拨杆和按键多次赋值") # V2.2
    def test_caseid_1989043(self):
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 1)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SwitchStatus", {"status": 1, "wipers": 0})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSwitchStatus", {"wipers": 0}, {"out": 1})
        
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 1)
        self.partner.ck_no_event(WIPER_SERVICE_CLIENT, "SwitchStatus")
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSwitchStatus", {"wipers": 0}, {"out": 1})

        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 2)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SwitchStatus", {"status": 2, "wipers": 0})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSwitchStatus", {"wipers": 0}, {"out": 2})
        
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 0)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SwitchStatus", {"status": 0, "wipers": 0})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSwitchStatus", {"wipers": 0}, {"out": 0})
        
    @pytest.mark.full
    @allure.title("通知/获取雨刮故障信息_拨杆故障") # V2.2
    def test_caseid_1989045(self):
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 3)
        self.partner.ck_no_event(WIPER_SERVICE_CLIENT, "WiperFault")
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {}, {"out": [{"fault": 0, "faultMsg": "OK", "wiper": 2}]})
        
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 3)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault", {"faults": [{"fault": 5, "faultMsg": "", "wiper": 0}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {}, {"out": [{"fault": 5, "faultMsg": "", "wiper": 0}]})

    @pytest.mark.full
    @allure.title("通知/获取雨刮开关状态_重启场景(默认值和非默认值)") # V2.2
    def test_caseid_1989046(self):
        # 当前状态为0
        sts = 0
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', sts)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', sts)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSwitchStatus", {"wipers": 0}, {"out": sts})
        self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.ck_no_event(WIPER_SERVICE_CLIENT, "SwitchStatus")
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SwitchStatus", {"status": sts, "wipers": 0}, timeout=15)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSwitchStatus", {"wipers": 0}, {"out": sts})
        self.partner.ck_no_event(WIPER_SERVICE_CLIENT, "SwitchStatus")

        # 当前状态为0~3 停止SteerWhlTouchSwtRi3发送
        for sts in [0, 1, 2, 3]:
            logger.info(f"sts:{sts}")
            self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', sts)
            self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', sts)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSwitchStatus", {"wipers": 0}, {"out": sts})
            self.ipdu.stop_send_pdu('bodycan', 0x271)   # 停止SteerWhlTouchSwtRi3发送
            self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
            logger.info(f"restart success.")
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SwitchStatus", {"status": 0, "wipers": 0}, timeout=15)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSwitchStatus", {"wipers": 0}, {"out": 0})
            self.ipdu.resume_bus_send("bodycan")        # 恢复SteerWhlTouchSwtRi3发送
            if sts != 0:
                self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SwitchStatus", {"status": sts, "wipers": 0})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSwitchStatus", {"wipers": 0}, {"out": sts})
            self.partner.ck_no_event(WIPER_SERVICE_CLIENT, "SwitchStatus")

        # 当前状态为0~3 停止LeverSwtLeLvrSwt3发送
        for sts in [0, 1, 2, 3]:
            self.partner.empty_all()
            logger.info(f"sts:{sts}")
            self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', sts)
            self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', sts)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSwitchStatus", {"wipers": 0}, {"out": sts})
            self.ipdu.stop_send_pdu('bodycan', 0x1ff)   # 停止LeverSwtLeLvrSwt3发送
            self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
            logger.info(f"restart success.")
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SwitchStatus", {"status": 0 if sts == 3 else sts, "wipers": 0}, timeout=15)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSwitchStatus", {"wipers": 0}, {"out": 0 if sts == 3 else sts})
            self.ipdu.resume_bus_send("bodycan")        # 恢复LeverSwtLeLvrSwt3发送
            if sts == 3:
                self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SwitchStatus", {"status": sts, "wipers": 0})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSwitchStatus", {"wipers": 0}, {"out": sts})
            self.partner.ck_no_event(WIPER_SERVICE_CLIENT, "SwitchStatus")
        
    @pytest.mark.full
    @allure.title("通知/获取雨刮开关状态_重启场景(other状态)") # V2.2
    def test_caseid_1989047(self):
        # 当前状态为2
        sts = 2
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', sts)  
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', sts)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSwitchStatus", {"wipers": 0}, {"out": sts})

        # other状态 (last value为2)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 4)
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3', 2)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSwitchStatus", {"wipers": 0}, {"out": sts})
        self.ipdu.stop_send_pdu('bodycan', 0x271)   # 停止SteerWhlTouchSwtRi3发送
        self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SwitchStatus", {"status": 0, "wipers": 0}, timeout=15)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSwitchStatus", {"wipers": 0}, {"out": 0})
        
        self.ipdu.resume_bus_send("bodycan")        # 恢复SteerWhlTouchSwtRi3发送
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SwitchStatus", {"status": sts, "wipers": 0})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSwitchStatus", {"wipers": 0}, {"out": sts})

    @allure.title("启动/停止洗涤") 
    @pytest.mark.sanity
    def test_caseid_1979863(self):
        self.ipdu.set_vehspd(0)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperWashInhibit", {"wipers": 0, "isOn": True})
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetSparyWashing", {"wipers": [{"id": 0, "on": False}]})
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.change_usage_mode(13)
        sleep(2)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus",
                                      {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetSparyWashing", {"wipers": [{"id": 0, "on": True}]})
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetSparyWashing", {"wipers": [{"id": 0, "on": False}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('WinWshrLvrCmd', [1, 0])

    @allure.title("启动/停止洗涤_雨刮洗涤禁用(下发一帧0)")
    @pytest.mark.full 
    def test_caseid_1980592(self):
        self.ipdu.set_vehspd(0)
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperWashInhibit",
                                         {"wipers": 0, "isOn": True})  # 雨刮禁用
        sleep(0.1)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetSparyWashing", {"wipers": [{"id": 0, "on": True}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('WinWshrLvrCmd', [0])

    @pytest.mark.full
    @allure.title("获取雨刮故障信息&通知雨刮故障信息_舱外光亮度原始数据传感器故障")
    def test_caseid_1913764(self):
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawQf', 3)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawQf', 1)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                  {"faults": [{"fault": 3, "faultMsg": "", "wiper": 0}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 3, "faultMsg": "", "wiper": 0}]})
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawQf', 3)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                  {"faults": [{"fault": 0, "faultMsg": "OK", "wiper": 2}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 0, "faultMsg": "OK", "wiper": 2}]})
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawQf', 2)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                  {"faults": [{"fault": 3, "faultMsg": "", "wiper": 0}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 3, "faultMsg": "", "wiper": 0}]})
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawQf', 3)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                  {"faults": [{"fault": 0, "faultMsg": "OK", "wiper": 2}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 0, "faultMsg": "OK", "wiper": 2}]})
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawQf', 0)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                  {"faults": [{"fault": 3, "faultMsg": "", "wiper": 0}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 3, "faultMsg": "", "wiper": 0}]})
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawQf', 3)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                  {"faults": [{"fault": 0, "faultMsg": "OK", "wiper": 2}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 0, "faultMsg": "OK", "wiper": 2}]})

    @pytest.mark.smoke
    @allure.title("获取雨刮故障信息&通知雨刮故障信息_ 雨刮开关/按键故障")
    def test_caseid_1913765(self):
        for SwtRi3 in [3, 1, 3, 2, 3, 0]:
            logger.info(f"打印{SwtRi3}")
            self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', SwtRi3)
            if SwtRi3 in [3]:
                self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                          {"faults": [{"fault": 5, "faultMsg": "", "wiper": 0}]})
                self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                                      {"out": [{"fault": 5, "faultMsg": "", "wiper": 0}]})
            else:
                self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                          {"faults": [{"fault": 0, "faultMsg": "OK", "wiper": 2}]})
                self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                                      {"out": [{"fault": 0, "faultMsg": "OK", "wiper": 2}]})
    
    @pytest.mark.full
    @allure.title("设置雨刮模式_2s计时器positon=@value(0)")
    def test_caseid_1985531(self):
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInWipgArFromWMM', 1)
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInPrkgPosnLoFromWMM', 0)
        self.sd_tester.write_multi_ccp({401: 2, 503: 2})
        self.ipdu.set_vehspd(1.9)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 2}]})
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInWipgArFromWMM', 0)
        sleep(0.1)
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInPrkgPosnLoFromWMM', 1)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0}, {"out": 0}, timeout=2) # 雨刮位置为0
        
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": True})
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus", {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        items = self.bgm_eth_inter.get_signal_items('FrntWiprSelnModFrntWiprSelnMod')
        
        t1 = get_signal_changed_timestamp(items, 2, 0)
        t2 = get_signal_changed_timestamp(items, 0, 2)
        assert 1.5 < t2 - t1 < 2.8
    
    @pytest.mark.full
    @allure.title("设置雨刮模式_2s计时器positon=@value(1)")
    def test_caseid_1985532(self):
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInWipgArFromWMM', 0)
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInPrkgPosnLoFromWMM', 1)
        self.sd_tester.write_multi_ccp({401: 2, 503: 2})
        self.ipdu.set_vehspd(1.9)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode",{"wipers": [{"id": 0, "mode": 2}]})
        self.bgm_eth_inter.start_bgm_tcpdump()

        sleep(0.5)
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInWipgArFromWMM', 0)#雨刮位置为1
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInPrkgPosnLoFromWMM', 0)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0},
                                            {"out": 1}, timeout=2)
        sleep(0.5)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": True})
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus", {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        items = self.bgm_eth_inter.get_signal_items('FrntWiprSelnModFrntWiprSelnMod')

        t1 = get_signal_changed_timestamp(items, 2, 0)
        t2 = get_signal_changed_timestamp(items, 0, 2)
        assert 3.8 < t2 - t1 < 4.2
        
    @pytest.mark.full
    @allure.title("设置雨刮模式_2s计时器内改变mode值")
    def test_caseid_1985533(self):
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInWipgArFromWMM', 0)
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInPrkgPosnLoFromWMM', 0)
        self.sd_tester.write_multi_ccp({401: 2, 503: 2})
        self.ipdu.set_vehspd(1.9)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 2}]})
        sleep(0.5)
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0}, {"out": 1}, timeout=2)
        sleep(0.5)
        
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": True})
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus", {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
        
        sleep(1.5)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 4}]})
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        items = self.bgm_eth_inter.get_signal_items('FrntWiprSelnModFrntWiprSelnMod')

        t1 = get_signal_changed_timestamp(items, 2, 0)
        t2 = get_signal_changed_timestamp(items, 0, 4)
        assert 3.3 < t2 - t1 < 3.7
        
    @pytest.mark.full
    @allure.title("设置雨刮模式_mode=2时雨刮动作禁用从True到False超时后再到True")
    def test_caseid_1985535(self):
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInWipgArFromWMM', 0)
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInPrkgPosnLoFromWMM', 1)
        self.sd_tester.write_multi_ccp({401: 2, 503: 2})
        self.ipdu.set_vehspd(1.9)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode",
                                            {"wipers": [{"id": 0, "mode": 2}]})
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(0.5)
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInWipgArFromWMM', 0)#雨刮位置为1
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInPrkgPosnLoFromWMM', 0)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0},
                                            {"out": 1}, timeout=2)
        sleep(0.5)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": True})#T1
        sleep(2)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus",
                                      {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})#T2
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": True})
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        items = self.bgm_eth_inter.get_signal_items('FrntWiprSelnModFrntWiprSelnMod')

        t1 = get_signal_changed_timestamp(items, 2, 0)
        t2 = get_signal_changed_timestamp(items, 0, 2)
        assert 3.8 < t2 - t1 < 4.2
    
    @pytest.mark.full
    @allure.title("设置雨刮模式_禁用前后设置雨刮位置校验周期报文")
    def test_caseid_1985556(self):
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInWipgArFromWMM', 0)
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInPrkgPosnLoFromWMM', 1)
        self.sd_tester.write_multi_ccp({401: 2, 503: 2})
        self.ipdu.set_vehspd(1.9)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 2}]})
        self.bgm_eth_inter.start_bgm_tcpdump()
        
        sleep(0.5)
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInWipgArFromWMM', 0)#雨刮位置为1
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInPrkgPosnLoFromWMM', 0)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0},  {"out": 1}, timeout=2)
        
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": True})#T1 mode=0
        sleep(2)
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInPrkgPosnLoFromWMM', 1)#雨刮位置为0 #mode=2 T2
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        items = self.bgm_eth_inter.get_signal_items('FrntWiprSelnModFrntWiprSelnMod')
        
        t1 = get_signal_changed_timestamp(items, 2, 0)
        t2 = get_signal_changed_timestamp(items, 0, 2)
        assert 2 < t2 - t1 < 2.3
    
    @pytest.mark.full
    @allure.title("设置雨刮模式_mode=6时前置条件不满足置为False计时器逻辑")
    def test_caseid_1985559(self):
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInWipgArFromWMM', 1)
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInPrkgPosnLoFromWMM', 0)
        self.sd_tester.write_multi_ccp({401: 2, 503: 2})
        self.ipdu.set_vehspd(1.9)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode", {"wipers": [{"id": 0, "mode": 6}]})
        self.bgm_eth_inter.start_bgm_tcpdump()
        
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInWipgArFromWMM', 0)#雨刮位置为0
        sleep(0.1)
        self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInPrkgPosnLoFromWMM', 1)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0}, {"out": 0}, timeout=2)
        
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": True})
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus",{"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        items = self.bgm_eth_inter.get_signal_items('FrntWiprSelnModFrntWiprSelnMod')

        t1 = get_signal_changed_timestamp(items, 6, 0)
        t2 = get_signal_changed_timestamp(items, 0, 6)
        assert 1.8 < t2 - t1 < 2.5
        
@allure.feature("SOA服务接口")
@allure.story("整车控制/WiperService")
@pytest.mark.ypp
class TestWiperServiceMockMcu(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([WIPER_SERVICE_CLIENT])
        sleep(5)

    def after_class(self, ecu):
        try:
            self.partner.stop_operators()
        except Exception as e:
            logger.error(f"{str(e)}")
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)#开关按键无故障
        sleep(0.5)
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawQf', 3)#舱外光亮度原始数据传感器无故障
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 0)#洗涤液不足无故障
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'RainSnsrActvnErrToHmi', 0)#雨量传感器无故障
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WiprSysFailrDetdSafe', 0)#雨刮控制系统内部无故障
        sleep(0.5)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr06, 'WiprInWipgAr', 0)#雨刮位置
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr06, 'WiprInPrkgPosnLo', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1', 0)#carmode信号
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1)#usagemode信号
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06', 0)#车速
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06', 3)#车速
        self.partner.empty_all(1)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def set_usage_mode(self, mode):
        """通过模拟mcu cdd打包总线数据来输入usage mode给到S2S"""
        logger.info(f"设置usage mode: {mode}")
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', mode)
        sleep(0.5)

    def set_car_mode(self, mode):
        """通过模拟mcu cdd打包总线数据来输入carmode给到S2S"""
        logger.info(f"设置car mode: {mode}")
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', mode)
        sleep(0.5)
        
    @pytest.mark.notify_wiper_mode
    @pytest.mark.sanity
    @allure.title("获取|通知雨刮自动模式")
    def test_caseid_1980493(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'RainSensActvn', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'RainSensActvn', 1)
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'WipgAutFrntMod', 0)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperAutoMode",
                                  {"mode": 1, "wiper": 0})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperAutoMode", {"wipers": 0},
                                              {"out": 1}, timeout=1)
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'WipgAutFrntMod', 1)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperAutoMode",
                                  {"mode": 2, "wiper": 0})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperAutoMode", {"wipers": 0},
                                              {"out": 2}, timeout=1)
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'WipgAutFrntMod', 2)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperAutoMode",
                                  {"mode": 3, "wiper": 0})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperAutoMode", {"wipers": 0},
                                              {"out": 3}, timeout=1)
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'WipgAutFrntMod', 3)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperAutoMode",
                                  {"mode": 4, "wiper": 0})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperAutoMode", {"wipers": 0},
                                              {"out": 4}, timeout=1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'RainSensActvn', 0)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperAutoMode",
                                  {"mode": 0, "wiper": 0})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperAutoMode", {"wipers": 0},
                                              {"out": 0}, timeout=1)

    @pytest.mark.notify_wiper_mode
    @pytest.mark.smoke
    @allure.title("获取|通知雨刮自动模式_默认值")
    def test_caseid_1980935(self):
        for RainSensActvn in [1]: # 为默认值0时重启不会上报event，已确认偏差接受
            logger.info(f"RainSensActvn:{RainSensActvn}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'RainSensActvn', RainSensActvn)
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'WipgAutFrntMod', 0)
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperAutoMode",
                                    {"mode": RainSensActvn, "wiper": 0})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperAutoMode", {"wipers": 0},
                                                {"out": RainSensActvn}, timeout=1)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                                {"out": [{"id": 0, "mode": 6 if RainSensActvn == 1 else 0}]})
            self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperAutoMode", {"wipers": 0},
                                                {"out": 0}, timeout=10)
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperAutoMode",
                                    {"mode": RainSensActvn, "wiper": 0}, timeout=5)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperAutoMode", {"wipers": 0},
                                                {"out": RainSensActvn})

    @pytest.mark.notify_wiper_mode
    @pytest.mark.smoke
    @allure.title("获取雨刮单刮模式&通知雨刮单刮模式 ")
    def test_caseid_1979708(self):
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WiprMotFrntLvrCmdSafeLvrInSnglStrokePos', 0)
        self.partner.empty_all(0.5)
        for OneshotSts in [1, 0]:
            self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WiprMotFrntLvrCmdSafeLvrInSnglStrokePos', OneshotSts)
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperOneshotSts",
                                      {"info": {"id": 0, "sts": OneshotSts}})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperOneshotSts", {"wipers": [0]},
                                                  {"out": [{"id": 0, "sts": OneshotSts}]})

    @pytest.mark.notify_wiper_mode
    @pytest.mark.sanity
    @allure.title("获取雨刮单刮模式&通知雨刮单刮模式_默认值")
    def test_caseid_1980547(self):
        for sts in [1, 0]:
            logger.info(f"sts:{sts}")
            self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WiprMotFrntLvrCmdSafeLvrInSnglStrokePos', sts)
            sleep(1)
            self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperOneshotSts", {"wipers": [0]},
                                                {"out": [{"id": 0, "sts": 255}]}, timeout=10)
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperOneshotSts",
                                    {"info": {"id": 0, "sts": sts}})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperOneshotSts", {"wipers": [0]},
                                                {"out": [{"id": 0, "sts": sts}]})

    @pytest.mark.smoke
    @allure.title("获取雨刮位置&通知雨刮位置")
    def test_caseid_108759(self):
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr06, 'WiprInWipgAr', 0)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr06, 'WiprInPrkgPosnLo', 0)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0},
                                              {"out": 1}, timeout=2)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr06, 'WiprInWipgAr', 0)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr06, 'WiprInPrkgPosnLo', 1)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperPosition", {"positon": 0, "wiper": 0}, timeout=2)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0},
                                              {"out": 0}, timeout=2)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr06, 'WiprInWipgAr', 1)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr06, 'WiprInPrkgPosnLo', 0)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperPosition", {"positon": 1, "wiper": 0})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0},
                                              {"out": 1}, timeout=2)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr06, 'WiprInWipgAr', 1)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr06, 'WiprInPrkgPosnLo', 1)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0},
                                              {"out": 1}, timeout=2)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr06, 'WiprInWipgAr', 0)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr06, 'WiprInPrkgPosnLo', 1)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperPosition", {"positon": 0, "wiper": 0})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0},
                                              {"out": 0}, timeout=2)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr06, 'WiprInWipgAr', 0)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr06, 'WiprInPrkgPosnLo', 0)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0},
                                              {"out": 1}, timeout=2)

    @pytest.mark.full
    @allure.title("获取雨刮位置&通知雨刮位置_默认值")
    def test_caseid_1980781(self):
        for sts in [0, 1]:
            self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr06, 'WiprInWipgAr', sts)
            self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr06, 'WiprInPrkgPosnLo', sts)
            sleep(0.2)
            self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0},
                                                {"out": 0}, timeout=10)
            self.ipdu.resume_all_bus_send()
            if sts in [0]:
                self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperPosition", {"positon": 1, "wiper": 0})
                self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0},
                                                    {"out": 1}, timeout=2)
            else:
                self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperPosition", {"positon": 0, "wiper": 0})
                self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0},
                                                    {"out": 0}, timeout=2)

    @pytest.mark.sanity
    @allure.title("获取车内湿度信息&通知车内湿度信息")
    def test_caseid_108758(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr60, 'CmptmtRelHum', 1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'RelHumSnsrQf', 1)
        self.partner.empty_all(0.5)
        for qf in [0, 1]:
            self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'RelHumSnsrQf', qf)
            if qf in [0]:
                qf = False
            else:
                qf = True
            last_hum = 0
            for send_hum in [1, 50, 200, 201, 0]:
                logger.info(f'发到{send_hum}')
                self.ipdu.set(self.ipdu.bodycan.CemBodyFr60, 'CmptmtRelHum', send_hum)
                if send_hum in [1, 50, 200, 0]:
                    new_hum = send_hum
                else:
                    new_hum = last_hum
                if new_hum == last_hum:
                    self.partner.ck_no_event(WIPER_SERVICE_CLIENT, "SteerHeatAvailiable")
                else:
                    self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "HumidityInfo",
                                              {"info": {"value": new_hum * 0.5, "isValid": qf}},
                                              timeout=1)
                    self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetHumidityInfo", {},
                                                          {"out": {"value": new_hum * 0.5, "isValid": qf}}, timeout=1)
                last_hum = new_hum

    @pytest.mark.full
    @allure.title("获取车内湿度信息&通知车内湿度信息_默认值")
    def test_caseid_1980573(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr60, 'CmptmtRelHum', 10)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'RelHumSnsrQf', 0)
        sleep(1)
        self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT, resume_all_bus=False)
        sleep(5)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetHumidityInfo", {},
                                              {"out": {"value": 40.0, "isValid": True}}, timeout=10)
        self.ipdu.resume_all_bus_send()
        try:
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "HumidityInfo",
                                {"info": {"value": 10 * 0.5, "isValid": False}},
                                timeout=4)
        except Exception:
            logger.info("XXXX")
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetHumidityInfo", {},
                                              {"out": {"value": 10*0.5, "isValid": False}}, timeout=1)

    @pytest.mark.sanity
    @allure.title("获取白天黑夜状态&通知白天黑夜状态")
    def test_caseid_108735(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 0)
        self.partner.empty_all(0.5)
        for Sts in [1, 0]:
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', Sts)
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "DayNightStatus", {"status": Sts}, timeout=1)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetDayNightStatus", {},
                                                  {"out": Sts}, timeout=1)

    @pytest.mark.full
    @allure.title("获取白天黑夜状态&通知白天黑夜状态_默认值") 
    def test_caseid_1980576(self):
        for sts in [0, 1]:
            logger.info(f"sts:{sts}")
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', sts)
            sleep(0.5)
            self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetDayNightStatus", {},
                                                {"out": False}, timeout=10)
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "DayNightStatus", {"status": sts})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetDayNightStatus", {},
                                                {"out": sts})

    @pytest.mark.sanity
    @allure.title("获取洗涤状态&通知洗涤状态")
    def test_caseid_1979983(self):
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WshrLvrPosnSafe', 0)
        self.partner.empty_all(0.5)
        for posnsafe in [2, 1, 2, 3, 2, 0]:
            logger.info(f"打印{posnsafe}")
            self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WshrLvrPosnSafe', posnsafe)
            if posnsafe in [0, 1, 3]:
                posnsafe = False
            else:
                posnsafe = True
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SparyWashing", {"info": {"id": 0, "on": posnsafe}})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSparyWashing", {"wipers": [0]},
                                                  {"out": [{"id": 0, "on": posnsafe}]})

    @pytest.mark.full
    @allure.title("获取洗涤状态&通知洗涤状态_默认值")
    def test_caseid_1980600(self):
        for sts in [0, 2]:
            logger.info(f"sts:{sts}")
            on = True if sts == 2 else False
            self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WshrLvrPosnSafe', sts)
            sleep(0.5)
            self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSparyWashing", {"wipers": [0]},
                                                {"out": [{"id": 0, "on": False}]}, timeout=10)
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "SparyWashing", {"info": {"id": 0, "on": on}})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetSparyWashing", {"wipers": [0]},
                                                {"out": [{"id": 0, "on": on}]})

    @pytest.mark.full
    @allure.title("获取雨刮故障信息&通知雨刮故障信息_默认值")
    def test_caseid_1913766(self):
        for sts in [0, 1]:
            logger.info(f"sts:{sts}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', sts)
            self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                                {"out": [{"fault": 0, "faultMsg": "OK", "wiper": 2}]}, timeout=10)
            self.ipdu.resume_all_bus_send()
            fault = [{"fault": 0, "faultMsg": "OK", "wiper": 2}] if sts == 0 else [{"fault": sts, "faultMsg": "", "wiper": 0}]
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault", {"faults": fault})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {}, {"out": fault})

    @pytest.mark.full
    @allure.title("获取雨刮故障信息&通知雨刮故障信息_洗涤液不足")
    def test_caseid_1980610(self):
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 1)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                  {"faults": [{"fault": 1, "faultMsg": "", "wiper": 0}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 1, "faultMsg": "", "wiper": 0}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 0)
        sleep(0.5)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                  {"faults": [{"fault": 0, "faultMsg": "OK", "wiper": 2}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 0, "faultMsg": "OK", "wiper": 2}]})

    @pytest.mark.full
    @allure.title("获取雨刮故障信息&通知雨刮故障信息_雨量传感器故障")
    def test_caseid_108741(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'RainSnsrActvnErrToHmi', 1)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                  {"faults": [{"fault": 2, "faultMsg": "", "wiper": 0}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 2, "faultMsg": "", "wiper": 0}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'RainSnsrActvnErrToHmi', 0)
        sleep(0.5)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                  {"faults": [{"fault": 0, "faultMsg": "OK", "wiper": 2}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 0, "faultMsg": "OK", "wiper": 2}]})

    @pytest.mark.full
    @allure.title("获取雨刮故障信息&通知雨刮故障信息_雨刮控制系统内部故障,导致雨刮无法挂刷")
    def test_caseid_108749(self):
        for Safe in [2, 1, 2, 0]:
            logger.info(f"打印{Safe}")
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WiprSysFailrDetdSafe', Safe)
            if Safe in [2]:
                self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                          {"faults": [{"fault": 4, "faultMsg": "", "wiper": 0}]})
                self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                                      {"out": [{"fault": 4, "faultMsg": "", "wiper": 0}]})
            else:
                self.partner.ck_coming_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                          {"faults": [{"fault": 0, "faultMsg": "OK", "wiper": 2}]}, timeout=0.2, deviation=0)
                self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                                      {"out": [{"fault": 0, "faultMsg": "OK", "wiper": 2}]})

    @pytest.mark.smoke
    @allure.title("获取雨刮故障信息&通知雨刮故障信息_全部故障产生到恢复")
    def test_caseid_1980605(self):
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawQf', 3)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 1)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                  {"faults": [{"fault": 1, "faultMsg": "", "wiper": 0}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 1, "faultMsg": "", "wiper": 0}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'RainSnsrActvnErrToHmi', 1)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                  {"faults": [{"fault": 1, "faultMsg": "", "wiper": 0},
                                              {"fault": 2, "faultMsg": "", "wiper": 0}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 1, "faultMsg": "", "wiper": 0},
                                                       {"fault": 2, "faultMsg": "", "wiper": 0}]})
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawQf', 1)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                  {"faults": [{"fault": 1, "faultMsg": "", "wiper": 0},
                                              {"fault": 2, "faultMsg": "", "wiper": 0},
                                              {"fault": 3, "faultMsg": "", "wiper": 0}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 1, "faultMsg": "", "wiper": 0},
                                                       {"fault": 2, "faultMsg": "", "wiper": 0},
                                                       {"fault": 3, "faultMsg": "", "wiper": 0}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WiprSysFailrDetdSafe', 2)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                  {"faults": [{"fault": 1, "faultMsg": "", "wiper": 0},
                                              {"fault": 2, "faultMsg": "", "wiper": 0},
                                              {"fault": 3, "faultMsg": "", "wiper": 0},
                                              {"fault": 4, "faultMsg": "", "wiper": 0}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 1, "faultMsg": "", "wiper": 0},
                                                       {"fault": 2, "faultMsg": "", "wiper": 0},
                                                       {"fault": 3, "faultMsg": "", "wiper": 0},
                                                       {"fault": 4, "faultMsg": "", "wiper": 0}]})
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 3)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                  {"faults": [{"fault": 1, "faultMsg": "", "wiper": 0},
                                              {"fault": 2, "faultMsg": "", "wiper": 0},
                                              {"fault": 3, "faultMsg": "", "wiper": 0},
                                              {"fault": 4, "faultMsg": "", "wiper": 0},
                                              {"fault": 5, "faultMsg": "", "wiper": 0}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 1, "faultMsg": "", "wiper": 0},
                                                       {"fault": 2, "faultMsg": "", "wiper": 0},
                                                       {"fault": 3, "faultMsg": "", "wiper": 0},
                                                       {"fault": 4, "faultMsg": "", "wiper": 0},
                                                       {"fault": 5, "faultMsg": "", "wiper": 0}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 0)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                  {"faults": [{"fault": 2, "faultMsg": "", "wiper": 0},
                                              {"fault": 3, "faultMsg": "", "wiper": 0},
                                              {"fault": 4, "faultMsg": "", "wiper": 0},
                                              {"fault": 5, "faultMsg": "", "wiper": 0}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 2, "faultMsg": "", "wiper": 0},
                                                       {"fault": 3, "faultMsg": "", "wiper": 0},
                                                       {"fault": 4, "faultMsg": "", "wiper": 0},
                                                       {"fault": 5, "faultMsg": "", "wiper": 0}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'RainSnsrActvnErrToHmi', 0)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                  {"faults": [{"fault": 3, "faultMsg": "", "wiper": 0},
                                              {"fault": 4, "faultMsg": "", "wiper": 0},
                                              {"fault": 5, "faultMsg": "", "wiper": 0}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 3, "faultMsg": "", "wiper": 0},
                                                       {"fault": 4, "faultMsg": "", "wiper": 0},
                                                       {"fault": 5, "faultMsg": "", "wiper": 0}]})
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawQf', 3)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                  {"faults": [{"fault": 4, "faultMsg": "", "wiper": 0},
                                              {"fault": 5, "faultMsg": "", "wiper": 0}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 4, "faultMsg": "", "wiper": 0},
                                                       {"fault": 5, "faultMsg": "", "wiper": 0}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WiprSysFailrDetdSafe', 1)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                  {"faults": [{"fault": 5, "faultMsg": "", "wiper": 0}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 5, "faultMsg": "", "wiper": 0}]})
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 1)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperFault",
                                  {"faults": [{"fault": 0, "faultMsg": "OK", "wiper": 2}]})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 0, "faultMsg": "OK", "wiper": 2}]})

    @pytest.mark.notify_wiper_mode
    @pytest.mark.smoke
    @allure.title("获取|通知雨刮模式(不包含单刮模式)_Mode与信号映射")  
    def test_caseid_1985270(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'WipgInfoWipgSpdInfo', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'RainSensActvn', 0)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                              {"out": [{"id": 0, "mode": 0}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'WipgInfoWipgSpdInfo', 1)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "Mode", {"mode": {"id": 0, "mode": 2}})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                              {"out": [{"id": 0, "mode": 2}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'WipgInfoWipgSpdInfo', 2)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "Mode", {"mode": {"id": 0, "mode": 3}})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                              {"out": [{"id": 0, "mode": 3}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'WipgInfoWipgSpdInfo', 3)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "Mode", {"mode": {"id": 0, "mode": 4}})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                              {"out": [{"id": 0, "mode": 4}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'WipgInfoWipgSpdInfo', 6)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "Mode", {"mode": {"id": 0, "mode": 5}})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                              {"out": [{"id": 0, "mode": 5}]})
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'WipgInfoWipgSpdInfo', 5)
        self.partner.ck_no_event(WIPER_SERVICE_CLIENT, "Mode")
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                              {"out": [{"id": 0, "mode": 5}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'RainSensActvn', 1)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "Mode", {"mode": {"id": 0, "mode": 6}})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                              {"out": [{"id": 0, "mode": 6}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'WipgInfoWipgSpdInfo', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'RainSensActvn', 0)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "Mode", {"mode": {"id": 0, "mode": 0}})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                              {"out": [{"id": 0, "mode": 0}]})

    @pytest.mark.notify_wiper_mode
    @pytest.mark.full
    @allure.title("获取|通知雨刮模式(不包含单刮模式)_默认值")
    def test_caseid_1988396(self):
        self.set_car_mode(0)
        self.set_usage_mode(2)
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": False}) 
        for spdinfo in [2, 0]:
            mode = spdinfo if spdinfo == 0 else spdinfo + 1
            logger.info(f"mode:{mode}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'WipgInfoWipgSpdInfo', spdinfo)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'RainSensActvn', 0) 
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                                {"out": [{"id": 0, "mode": mode}]}) 
            self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                                {"out": [{"id": 0, "mode": 6}]}, timeout=10)
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "Mode", {"mode": {"id": 0, "mode": mode}}, timeout=5)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                                {"out": [{"id": 0, "mode": mode}]})

    @pytest.mark.notify_wiper_mode
    @pytest.mark.sanity
    @allure.title("获取|通知雨刮模式(不包含单刮模式)_前提条件触发_超时退出") 
    def test_caseid_1985271(self):
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": False})  
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'RainSensActvn', 0)
        for car_mode in [0]:
            self.set_car_mode(car_mode)
            for usage_mode in [2]:
                self.set_usage_mode(usage_mode)
                sleep(1)
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'WipgInfoWipgSpdInfo', 1)
                self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                                      {"out": [{"id": 0, "mode": 2}]})

                self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 1)  # 雨刮开关短按
                self.partner.empty_all(0.2)
                self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
                self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "Mode", {"mode": {"id": 0, "mode": 2}}, timeout=0.5)
                
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'WipgInfoWipgSpdInfo', 2)
                sleep(1)
                self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                                      {"out": [{"id": 0, "mode": 3}]})
                
                self.partner.ck_no_event(WIPER_SERVICE_CLIENT, "Mode", timeout=1.5)
                self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "Mode", {"mode": {"id": 0, "mode": 3}}, timeout=1.5)
                self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                                      {"out": [{"id": 0, "mode": 3}]})
                
                #检查Last value mode 
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'WipgInfoWipgSpdInfo', 5)
                self.partner.ck_no_event(WIPER_SERVICE_CLIENT, "Mode")
                self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                                    {"out": [{"id": 0, "mode": 3}]})
 
    @pytest.mark.notify_wiper_mode
    @pytest.mark.sanity
    @allure.title("获取|通知雨刮模式(不包含单刮模式)_前提条件触发_主动退出单刮_检查Mode值") 
    def test_caseid_1988391(self):
        self.set_car_mode(0)
        self.set_usage_mode(11)
        
        # 前提条件模式为4
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": False})  
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'WipgInfoWipgSpdInfo', 3)    
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'RainSensActvn', 0)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                              {"out": [{"id": 0, "mode": 4}]}) 

        # 触发条件：雨刮开关短按
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 1)  
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        # 退出单刮
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WiprMotFrntLvrCmdSafeLvrInSnglStrokePos', 1)
        sleep(0.02)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WiprMotFrntLvrCmdSafeLvrInSnglStrokePos', 0)
        self.partner.empty_all(0.2)
        
        #检查改变后的mode
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'WipgInfoWipgSpdInfo', 1)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "Mode", {"mode": {"id": 0, "mode": 2}})
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                              {"out": [{"id": 0, "mode": 2}]})
                
        # 再次触发条件：雨刮开关短按
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 1)  
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        # 退出单刮
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WiprMotFrntLvrCmdSafeLvrInSnglStrokePos', 1)
        sleep(0.02)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WiprMotFrntLvrCmdSafeLvrInSnglStrokePos', 0)
        self.partner.empty_all(0.5)

        #检查Last value mode 
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'WipgInfoWipgSpdInfo', 7)
        self.partner.ck_no_event(WIPER_SERVICE_CLIENT, "Mode")
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                              {"out": [{"id": 0, "mode": 2}]})
        
    @pytest.mark.notify_wiper_mode       
    @pytest.mark.full
    @allure.title("获取|通知雨刮模式(不包含单刮模式)_增加信号debounce_模式为0时收到RainSensActvn从1到0") 
    def test_caseid_1988393(self):
        self.set_car_mode(0)
        self.set_usage_mode(2)
        
        # 前提条件模式为0
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": False})  
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'WipgInfoWipgSpdInfo', 0)    
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'RainSensActvn', 0)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                              {"out": [{"id": 0, "mode": 0}]}) 
        
        # 触发条件：雨刮开关短按
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 1)  
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        self.partner.empty_all(0.2)
        
        # 退出单刮
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'RainSensActvn', 1)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WiprMotFrntLvrCmdSafeLvrInSnglStrokePos', 1)
        sleep(0.02)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WiprMotFrntLvrCmdSafeLvrInSnglStrokePos', 0)
        sleep(0.02) # 100ms内收到RainSensActvn为0
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'RainSensActvn', 0)
        
        # 实际会收到两次事件mode均为6，一次RainSensActvn改变，一次退出单刮100ms后，不会收到mode为0的事件 
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "Mode", {"mode": {"id": 0, "mode": 0}})
        self.partner.ck_coming_event(WIPER_SERVICE_CLIENT, "Mode", {"mode": {"id": 0, "mode": 0}}, timeout=0.08, deviation=0.05)
        self.partner.ck_no_event(WIPER_SERVICE_CLIENT, "Mode")

    @pytest.mark.notify_wiper_mode       
    @pytest.mark.full
    @allure.title("获取|通知雨刮模式(不包含单刮模式)_增加信号debounce_模式为6时退出单刮前收到RainSensActvn=1") 
    def test_caseid_1988394(self):
        self.set_car_mode(0)
        self.set_usage_mode(2)
        
        # 前提条件模式为0
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": False})  
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'WipgInfoWipgSpdInfo', 0)    
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'RainSensActvn', 1)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                              {"out": [{"id": 0, "mode": 6}]}) 
        
        # 触发条件：雨刮开关短按
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 1)  
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        self.partner.empty_all(0.2)
        
        # 退出单刮
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'RainSensActvn', 0)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WiprMotFrntLvrCmdSafeLvrInSnglStrokePos', 1)
        sleep(0.05)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'RainSensActvn', 1)
        sleep(0.05)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WiprMotFrntLvrCmdSafeLvrInSnglStrokePos', 0)
        logger.info("退出单刮完成")

        # 实际会收到一次事件mode为6:退出单刮，不会收到mode为0的事件 
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "Mode", {"mode": {"id": 0, "mode": 6}}, timeout=0.3)
        self.partner.ck_no_event(WIPER_SERVICE_CLIENT, "Mode")
  
    @pytest.mark.notify_wiper_mode
    @pytest.mark.full
    @allure.title("获取|通知雨刮模式(不包含单刮模式)_增加信号debounce_模式为6时收到RainSensActvn从0到1") 
    def test_caseid_1988398(self):
        self.set_car_mode(0)
        self.set_usage_mode(2)
        
        # 前提条件模式为6
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": False})  
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'WipgInfoWipgSpdInfo', 0)    
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'RainSensActvn', 1)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                              {"out": [{"id": 0, "mode": 6}]}) 
        
        # 触发条件：雨刮开关短按
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 1)  
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        self.partner.empty_all(0.2)
        
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'RainSensActvn', 0)
        # 退出单刮
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WiprMotFrntLvrCmdSafeLvrInSnglStrokePos', 1)
        sleep(0.02)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WiprMotFrntLvrCmdSafeLvrInSnglStrokePos', 0)
        logger.info("退出单刮完成")
        sleep(0.02) # 100ms内收到RainSensActvn为1
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'RainSensActvn', 1)

        # 实际会收到两次事件mode均为6，一次RainSensActvn改变，一次退出单刮100ms后，不会收到mode为0的事件 
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "Mode", {"mode": {"id": 0, "mode": 6}})
        self.partner.ck_coming_event(WIPER_SERVICE_CLIENT, "Mode", {"mode": {"id": 0, "mode": 6}}, timeout=0.08, deviation=0.05)
        self.partner.ck_no_event(WIPER_SERVICE_CLIENT, "Mode")

    @pytest.mark.notify_wiper_mode       
    @pytest.mark.full
    @allure.title("获取|通知雨刮模式(不包含单刮模式)_增加信号debounce_模式为6时退出单刮_再进入special状态再退出") 
    def test_caseid_1988399(self):
        self.set_car_mode(0)
        self.set_usage_mode(2)
        
        # 前提条件模式为6
        self.partner.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": False})  
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'WipgInfoWipgSpdInfo', 0)    
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'RainSensActvn', 1)
        self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMode", {"wipers": [0]},
                                              {"out": [{"id": 0, "mode": 6}]}) 
        
        # 触发条件：雨刮开关短按
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 1)  
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        self.partner.empty_all(0.2)
        
        # 退出单刮
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WiprMotFrntLvrCmdSafeLvrInSnglStrokePos', 1)
        sleep(0.02)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WiprMotFrntLvrCmdSafeLvrInSnglStrokePos', 0)
        sleep(0.02)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "Mode", {"mode": {"id": 0, "mode": 6}}, timeout=0.5)
        
        # 再次触发条件：雨刮开关短按
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 1)  
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3', 0)
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "Mode", {"mode": {"id": 0, "mode": 6}}, timeout=0.5)
        self.partner.empty_all(0.2)

        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'RainSensActvn', 0)
        # 退出单刮
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WiprMotFrntLvrCmdSafeLvrInSnglStrokePos', 1)
        sleep(0.02)
        self.ipdu.set(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WiprMotFrntLvrCmdSafeLvrInSnglStrokePos', 0)
        sleep(0.02)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'RainSensActvn', 1)
        
        # 实际会收到两次事件mode均为6，一次RainSensActvn改变，一次退出单刮100ms后，不会收到mode为0的事件 
        self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "Mode", {"mode": {"id": 0, "mode": 6}})
        self.partner.ck_coming_event(WIPER_SERVICE_CLIENT, "Mode", {"mode": {"id": 0, "mode": 6}}, timeout=0.08, deviation=0.05)
        self.partner.ck_no_event(WIPER_SERVICE_CLIENT, "Mode")

    @pytest.mark.sanity
    @allure.title("获取雨刮维修模式状态&通知雨刮维修模式状态")
    def test_caseid_108750(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', 0)
        self.partner.empty_all(0.2)
        for Srv in [1, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', Srv)
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "MaintainceMode", {"on": Srv})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMaintainceMode", {}, {"out": Srv})

    @pytest.mark.full
    @allure.title("获取雨刮维修模式状态&通知雨刮维修模式状态_默认值")
    def test_caseid_1980834(self):
        for sts in [1, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'WiprInPosnForSrv', sts)
            sleep(0.5)
            self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMaintainceMode", {}, {"out": 0}, timeout=10)
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "MaintainceMode", {"on": sts})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperMaintainceMode", {}, {"out": sts})

    @pytest.mark.sanity
    @allure.title("获取|通知雨刮洗涤液位低")
    def test_caseid_1988408(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', 0)
        self.partner.empty_all(0.5)
        for val in [1, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', val)
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperWashFluidLowStatus", {"isWashFluidLow": val})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperWashFluidLow", {}, {"out": val})

    @pytest.mark.full
    @allure.title("获取|通知雨刮洗涤液位低_默认值") 
    def test_caseid_1988409(self):
        for sts in [0, 1]:
            logger.info(f"sts:{sts}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', sts)
            sleep(0.5)
            self.restart_bgm_and_connect_service(WIPER_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperWashFluidLow", {}, {"out": False}, timeout=10)
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperWashFluidLowStatus", {"isWashFluidLow": sts})
            self.partner.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperWashFluidLow", {}, {"out": sts})