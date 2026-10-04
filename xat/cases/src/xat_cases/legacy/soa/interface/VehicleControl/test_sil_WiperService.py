#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :test_soa_heat.py
@time         :8/27/24 11:23
@author       :dejian.xiong@jiduauto.com
@description  :
"""
from xat_cases.legacy.soa.case_helper.test_abc_sil_base import *
from xat_ecu.api.abc_interface import *


def find_value_change(items, exp_value):
    """校验信号跳变为期望值时的时间戳"""
    for i in range(1, len(items)):
        if items[i-1][2] != exp_value and items[i][2] == exp_value:
            return float(items[i][1])
    assert False, f"遍历完未找到跳变为{exp_value}的情况"


@allure.feature("SOA服务接口")
@allure.story("整车控制/WiperService")
class WiperServiceMockMcu(TestSoaAbcSILBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([WIPER_SERVICE_CLIENT, LOWVLORAGE_SERVICE_CLIENT, VEHICLEMODESERVICE_CLIENT
                         ])
        self.mock_mcu.start_run()
        self.soa.wait_for_service_reconnect(WIPER_SERVICE_CLIENT)
        self.soa.wait_for_service_reconnect(LOWVLORAGE_SERVICE_CLIENT)
        self.soa.wait_for_service_reconnect(VEHICLEMODESERVICE_CLIENT)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.bus_comm.set_steer_wheel_touch_switch_sts(SteerWhlTouchSwtPos.Left3, SteerWhlTouchSwtSts.NotAvailble)  # !3即雨刮开关按键无故障      BGM收的，不带cdd_
        self.bus_comm.set("cem_lin1", "RlsmCem_Lin1Fr01", 'TwliBriRawQf', 3) #舱外光亮度原始数据传感器无故障
        self.bus_comm.cdd_set_wiper_washer_fluid_low(OnOff.On)   # BGM发的 
        self.bus_comm.cdd_set_rain_sensor_error(OnOff.Off)
        self.bus_comm.cdd_set_wiper_sys_fault(OnOff.Off)
        self.bus_comm.cdd_set_wiper_position(OnOff.Off, OnOff.Off)
        self.bus_comm.cdd_set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.cdd_set_car_mode(CarMode.NORMAL)
        self.bus_comm.set_vehspd(0)
        self.soa.empty_all(0.5)
        logger.info(f"case开始运行")

    def after_each_func(self, ecu):
        logger.info(f"case结束运行")
        self.mock_mcu.stop_tcpdump()
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)
    
    @pytest.mark.full
    @allure.title("设置雨刮模式_mode=6时前置条件不满足置为False计时器逻辑")
    def test_caseid_1985559(self):   # 原HIL用例
        self.bus_comm.set("cem_lin1", "CemCem_Lin1Fr06", 'WiprInPrkgPosnLo', 1)
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInWipgArFromWMM', 1)
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInPrkgPosnLoFromWMM', 0)
        self.mock_mcu.write_ccp({401: 2, 503: 2})
        self.mock_mcu.write_ccp({401: 2, 503: 6})
        self.bus_comm.cdd_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_vehspd(1.9)
        self.soa.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMode",
                                            {"wipers": [{"id": 0, "mode": 6}]})
        self.mock_mcu.start_tcpdump()
        sleep(1)  # 期望抓到6，如果不等待直接设置下面的信号会导致直接抓到0，抓不到6
        # self.mock_mcu.start_bgm_tcpdump()
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInWipgArFromWMM', 0)#雨刮位置为0
        sleep(0.1)
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.cem_lin1.WmmCem_Lin1Fr01, 'WiprInPrkgPosnLoFromWMM', 1)
        self.soa.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperPosition", {"wipers": 0},
                                            {"out": 0}, timeout=2)
        self.soa.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 0, "isOn": True})
        sleep(2)
        self.soa.ck_s2s_event(WIPER_SERVICE_CLIENT, "NotifyWiperInhibitStatus",
                                      {"inhibit": {"id": 0, "MoveInhibit": False, "WashInhibit": False}})
        sleep(3)
        self.mock_mcu.stop_tcpdump()
        # self.mock_mcu.stop_tcpdump_and_parse_signal()
        items = self.mock_mcu.get_signal_items('FrntWiprSelnModFrntWiprSelnMod')
        t1 = find_value_change(items, 0)
        t2 = find_value_change(items, 6)
        assert 1.8 < t2 - t1 < 2.5
    
    @allure.title("通知/获取低压继电器状态tcp_默认值")
    @pytest.mark.full
    def test_caseid_1981489(self):
        self.mock_mcu.start_tcpdump()
        # self.mix.kill_s2s_and_reconnect_service(VEHICLEMODESERVICE_CLIENT)
        sleep(50)
        try:
            self.soa.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, 
                                            "getLVRelaySts", 
                                            {}, 
                                            {"out": {"kl15RlySts":0,"battSaverRlySts": False, "pwrOutletRlySts": False, 
                                                    "kl15ExtRlySts": False, "kl15_3RlySts": False}},timeout=5)
        except Exception as e:
            print(e)
        self.mock_mcu.stop_tcpdump()
    
    @allure.title("MOCKMCU_获取和通知低压电池状态_遍历") 
    @pytest.mark.full
    def test_caseid_1983974(self):
        self.mock_mcu.set_signal("BattSoc2Sts", 0, send_pdu_immediately=True)
        sleep(1)
        for sigin in [1,2,3,0]:
            self.mock_mcu.set_signal("BattSoc2Sts", sigin, send_pdu_immediately=True)
            self.soa.ck_event_and_resp(LOWVLORAGE_SERVICE_CLIENT, "BatteryStatus", {"status":{"calculatedStatus":sigin}})
        for sigin1 in [100.0,0]:
            self.mock_mcu.set_signal("BattSocRaw2", sigin1, send_pdu_immediately=True)
            self.soa.ck_event_and_resp(LOWVLORAGE_SERVICE_CLIENT,"BatteryStatus",{"status":{"calculatedSoc":sigin1}})
        for sigin2 in [100.0,0]:
            self.mock_mcu.set_signal("BattSohRaw2", sigin2, send_pdu_immediately=True)
            self.soa.ck_event_and_resp(LOWVLORAGE_SERVICE_CLIENT,"BatteryStatus",{"status":{"calculatedSoh":sigin2}})

    @pytest.mark.notify_wiper_mode
    @pytest.mark.smoke
    @allure.title("获取雨刮单刮模式&通知雨刮单刮模式 ")
    def test_caseid_1979718(self): # 原mock mcu用例
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WiprMotFrntLvrCmdSafeLvrInSnglStrokePos', 0)
        self.soa.empty_all(0.5)
        for OneshotSts in [1, 0]:
            self.bus_comm.ipdu.set(self.bus_comm.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WiprMotFrntLvrCmdSafeLvrInSnglStrokePos', OneshotSts)
            self.soa.ck_s2s_event(WIPER_SERVICE_CLIENT, "WiperOneshotSts",
                                      {"info": {"id": 0, "sts": OneshotSts}})
            self.soa.send_request_and_ck_resp(WIPER_SERVICE_CLIENT, "GetWiperOneshotSts", {"wipers": [0]},
                                                  {"out": [{"id": 0, "sts": OneshotSts}]})
        
    def test_caseid_123456(self):
        self.soa.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 2, "isOn": True})
        sleep(1)
        self.soa.send_method_request(WIPER_SERVICE_CLIENT, "SetWiperMoveInhibit", {"wipers": 3, "isOn": True})
        sleep(6)
