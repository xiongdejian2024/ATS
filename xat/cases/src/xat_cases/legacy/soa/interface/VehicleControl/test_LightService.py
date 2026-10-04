# -*- coding: utf-8 -*-
"""
@File        : test_soa_Lightservice.py
@Author      : peipei.yang_ext@jiduatuo.com
@Time        : 2023/08/8 15:00 PM
@Description : Test s2s interface about rctalarm function
"""

import pytest
import threading
from time import sleep
from xat_ecu.legacy.sdk.sdk_tools import *

from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_cases.legacy.soa.case_helper.test_base import *
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.soa.case_helper.utils import ck_pdu_period_time, ck_pdu_sporadic
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *



def set_hazard(io,ipdu,open=True):
    sts = ipdu.get_recent_signal_raw_value(ipdu.bodycan.CemBodyFr01, 'IndcrSts')
    if open:
        if sts == 3:
            return
        else:
            io.hazard_light_open()  # 通过双闪开危险报警灯
            sleep(0.2)
            io.hazard_light_close()  # 通过双闪关闭危险报警灯
            ipdu.check(ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3)  # 危险报警灯开
    else:
        if sts != 3:
            return
        else:
            io.hazard_light_open()  # 通过双闪开危险报警灯
            sleep(0.2)
            io.hazard_light_close()  # 通过双闪关闭危险报警灯
            ipdu.check(ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0)  # 危险报警灯关

def Fault(fault, type, zoneid):
    return {"fault": fault, "faultMsg": "","light": {"type": type,"zoneId": zoneid}}


@allure.feature("SOA服务接口")
@allure.story("整车控制/LightService")  # 转向灯
@pytest.mark.turnlamp
class TestLightServiceTurnLamp(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        # self.nucapp.bgm_power_off()
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        # 放在beforecase
        self.bgm_tcpdump = BGM_SSH()
        self.bgm_tcpdump.init_bgm_tcpdump()
        # 启动partner operator
        self.partner = S2sBaseClass([("LightService", "client"),
                                     ("SteerWheelService", "client"),
                                     ("CarConfigService", "client"),
                                     ("LightService", "client_1"),
                                     ])
        self.partner.method_default_timeout = 0.1
        sleep(5)
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        # 检查上位机上是否有其它未关闭的soa_partner进程在运行，如果有，则杀死进程

        self.set_mode_bg = False
        self.turnlamp_on = False   
              
    def before_each_func(self, ecu):
        self.sd_tester.tester_present()
        self.ipdu.set_vehspd(0)  # 车速
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 0)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 0)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 0) 
        sleep(0.5)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 255}}, timeout=0.3)
        sleep(0.2)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampHold", {"flag": 0})
        sleep(0.2)
        set_hazard(self.io, self.ipdu, open=False)
        self.partner.empty_all()
        super().before_each_func(ecu, start=False)

        self.set_mode_bg = False
        self.turnlamp_on = False   
        
    def after_each_func(self, ecu):
        self.sd_tester.stop_tester_present()
        self.ipdu.set_vehspd(0)  # 车速
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 255}}, timeout=0.3)
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 255}}, timeout=0.3)
        sleep(0.2)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampHold", {"flag": 0})
        sleep(0.2)
        set_hazard(self.io, self.ipdu, open=False)
        self.partner.stop_operators()
        # self.nucapp.bgm_power_on()
        super().after_class(self, ecu)

    def set_hazard_button(self, open=True, press_if_sts_is_same=True):
        """
        通过按键打开关闭双闪报警灯。
        @param open (bool, optional): 是否打开双闪，默认为True。
        @param press_if_sts_is_same (bool, optional): 默认如果预期与当前状态相同，仍会再按两次双闪按键，否则不会按。
        """
        sts = self.ipdu.get_recent_signal_raw_value(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts')
        if not press_if_sts_is_same:
            if (sts == 3 and open) or (sts !=3 and not open):
                return
        press_times = 1 if (sts != 3 and open) or (sts == 3 and not open) else 2
    
        for i in range(press_times):
            self.io.hazard_light_open()  
            sleep(0.2)
            self.io.hazard_light_close()  
            sleep(1.2)
            logger.info(f"[set_hazard_button] press {i+1}/{press_times}")
            
        self.hazard_button = open
        logger.info(f"[set_hazard_button] hazard_button status: {open}")
        
    @allure.title("设置转向灯工作模式原子能力压测_Set开左转")
    @pytest.mark.full
    def test_caseid_1988563(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        
        loop_num = 1000
        fail_num_list = []
        for i in range(loop_num):
            logger.info(f"**********************第{i}次开始")
            try:
                self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                                {"lamp": {"mode": 0, "priority": 47}}, timeout=0.3)
                self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                                {"lamp": {"mode": 0, "priority": 255}}, timeout=0.3)
                self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                                {"lamp": {"mode": 1, "priority": 95}}, timeout=0.3)
                # 检查是否能打开左转
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                    {"out": {"mode": 1, "priority": 95}})  
                self.partner.empty_all()
            except AssertionError as e:
                logger.info(f"*****第{i}次失败")
                fail_num_list.append(i)
                logger.info(str(e))

        per = f"{len(fail_num_list)/loop_num * 100:.2f}%"
        msg = f"统计失败率:{len(fail_num_list)}/{loop_num}={per} 第几次失败:{fail_num_list}"
        logger.info(msg)
        assert len(fail_num_list) == 0, f"{msg}"
          
    def set_turnlamp_mode_thread(self, mode, priority, period=0.05, is_check_on=False):
        """
        子线程LightService_client_1设置转向灯模式
        Args:
            mode (int): 转向灯的模式0，1，2，3
            priority (int): 转向灯的优先级
            period (float, optional): 循环检查的间隔时间，默认为0.05秒
            is_check_on (bool, optional): 是否在发送设置后检查转向灯状态，默认为False
        """
        while self.set_mode_bg:  # LightService_client_1
            if not self.turnlamp_on:
                self.partner.send_method_request("LightService_client_1", "SetTurnLampMode",
                                            {"lamp": {"mode": mode, "priority": priority}}, timeout=0.3)
                if is_check_on:
                    self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                        {"out": {"mode": mode, "priority": priority}})
                    self.partner.empty_all()
                    self.turnlamp_on = True
                logger.info("************set_turnlamp_mode_thread**********") 
                sleep(period)
                      
    @allure.title("设置转向灯工作模式原子能力压测_Set关左转")
    @pytest.mark.full
    def test_caseid_1988564(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.set_mode_bg = True
        # 持续周期调用
        t = threading.Thread(target=self.set_turnlamp_mode_thread, args=(1, 111, 0.05, True))
        t.setDaemon(True)
        t.start()

        loop_num = 1000
        fail_num_list = []
        for i in range(loop_num):
            logger.info(f"第[{i}]次开始")
            start_time = time.time()
            try:
                while True:
                    if self.turnlamp_on: 
                        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                                        {"lamp": {"mode": 0, "priority": 95}}, timeout=0.3)
                        # 检查是否能关闭左转
                        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                                {"sts": {"mode": 0, "priority": 255}})
                        self.partner.empty_all()
                        self.turnlamp_on = False
                        break
                    else:
                        if time.time() - start_time > 5:
                            assert False, f"第[{i}]次超时"
                        sleep(0.01)
            except AssertionError as e:
                logger.info(f"第[{i}]次失败")
                fail_num_list.append(i)
                logger.info(str(e))

        self.set_mode_bg = False
        self.turnlamp_on = False
        t.join()
        
        per = f"{len(fail_num_list)/loop_num * 100:.2f}%"
        msg = f"统计失败率:{len(fail_num_list)}/{loop_num}={per} 第几次失败:{fail_num_list}"
        logger.info(msg)
        assert len(fail_num_list) == 0, f"{msg}"

    @allure.title("设置转向灯工作模式原子能力压测_按键关左转")
    @pytest.mark.full
    def test_caseid_1988565(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.set_mode_bg = True
        # 持续周期调用
        t = threading.Thread(target=self.set_turnlamp_mode_thread, args=(1, 111, 0.05, True))
        t.setDaemon(True)
        t.start()
        
        loop_num = 100
        fail_num_list = []        
        for i in range(loop_num):
            try: 
                logger.info(f"第[{i}]次开始")
                start_time = time.time()
                while True:
                    if self.turnlamp_on: 
                        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)  
                        sleep(0.2)
                        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)  # 转向开关短按
                        sleep(0.2)
                        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
                        # 检查是否能关闭左转
                        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                            {"out": {"mode": 0, "priority": 255}})  
                        self.partner.empty_all()
                        self.turnlamp_on = False
                        break
                    else:
                        if time.time() - start_time > 5:
                            assert False, f"第[{i}]次超时"
                        sleep(0.01)
            except AssertionError as e:
                logger.info(f"第[{i}]次失败")
                fail_num_list.append(i)
                logger.info(str(e))
                
        self.set_mode_bg = False
        self.turnlamp_on = False
        t.join()
        
        per = f"{len(fail_num_list)/loop_num * 100:.2f}%"
        msg = f"统计失败率:{len(fail_num_list)}/{loop_num}={per} 第几次失败:{fail_num_list}"
        logger.info(msg)
        assert len(fail_num_list) == 0, f"{msg}"

    @allure.title("通知|获取转向灯工作状态原子能力压测")
    @pytest.mark.full
    def test_caseid_1988566(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # 持续周期调用
        self.set_mode_bg = True
        t = threading.Thread(target=self.set_turnlamp_mode_thread, args=(1, 0x5F, 0.05))
        t.setDaemon(True)
        t.start()
            
        loop_num = 1000
        fail_num_list = []
        for i in range(loop_num):
            logger.info(f"第[{i}]次开始")
            try:
                # 检查左转状态
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                        {"sts": {"mode": 1, "priority": 0x5F}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                    {"out": {"mode": 1, "priority": 0x5F}})  
                
                self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                                {"lamp": {"mode": 0, "priority": 0x5F}}, timeout=0.3)
                self.partner.empty_all()
            except AssertionError as e:
                logger.info(f"第[{i}]次失败")
                fail_num_list.append(i)
                logger.info(str(e))

        self.set_mode_bg = False
        t.join()        
        per = f"{len(fail_num_list)/loop_num * 100:.2f}%"
        msg = f"统计失败率:{len(fail_num_list)}/{loop_num}={per} 第几次失败:{fail_num_list}"
        logger.info(msg)
        assert len(fail_num_list) == 0, f"{msg}"

    @pytest.mark.steer
    @allure.title("设置禁止方向盘回正关转向灯原子能力压测")
    @pytest.mark.full
    def test_caseid_1988778(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3) #方向盘转角状态有效
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)  

        loop_num = 500
        fail_num_list = []
        for i in range(loop_num):
            # 方向盘回正关闭转向灯
            try:
                for flag in [0, 1]:
                    logger.info(f"[SetTurnLampHold][flag:{flag}](0:使能, 1:禁止)[loop:{i}]开始")
                    self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampHold", {"flag": flag})
                
                    # 方向盘短按开左转向
                    self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)  
                    sleep(0.1)
                    self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
                    
                    # 设置方向盘角度
                    self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
                    sleep(0.2)
                    self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.52)
                        
                    # 检查左转向灯
                    if flag == 0:
                        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": flag, "priority": 255}})
                        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                            {"out": {"mode": flag, "priority": 255}})
                        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', flag, timeout=1)
                    else:
                        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                            {"out": {"mode": flag, "priority": 95}})
                        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', flag, timeout=1)
                        
            except AssertionError as e:
                logger.info(f"[SetTurnLampHold][flag:{flag}](0:使能, 1:禁止)[loop:{i}]失败")
                fail_num_list.append(i)
                logger.info(str(e))
 
        per = f"{len(fail_num_list)/loop_num * 100:.2f}%"
        msg = f"统计失败率:{len(fail_num_list)}/{loop_num}={per} 第几次失败:{fail_num_list}"
        logger.info(msg)
        assert len(fail_num_list) == 0, f"{msg}"
        
    @allure.title("接口SetTurnLampHold使能/禁止方向盘回正关转向")
    @pytest.mark.full
    def test_caseid_1988559(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3) #方向盘转角状态有效
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)  
        
        # 方向盘回正关闭转向灯
        for flag in [0, 1]:
            logger.info(f"方向盘回正关左转flag:{flag}（0：使能，1：禁止）")
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampHold", {"flag": flag})
        
            # 方向盘短按开左转向
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)  
            sleep(0.2)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
            sleep(0.1)
            # 设置方向盘角度
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.52)
                
            # 检查左转向灯
            if flag == 0:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": flag, "priority": 255}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                    {"out": {"mode": flag, "priority": 255}})
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', flag, timeout=1)
            else:
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                    {"out": {"mode": flag, "priority": 95}})
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', flag, timeout=1)

    @allure.title("设置转向灯工作模式_独占需求5s超时释放")
    @pytest.mark.full
    def test_caseid_1988579(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        for priority in [0x2F, 0x4F]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                            {"lamp": {"mode": 1, "priority": priority}})
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                    {"sts": {"mode": 1, "priority": priority}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                {"out": {"mode": 1, "priority": priority}})
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  

            logger.info(f"sleep 5s wait to release [{priority}] control.")
            sleep(5)

            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                            {"lamp": {"mode": 0, "priority": 95}})   
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                    {"sts": {"mode": 0, "priority": 255}})     
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                {"out": {"mode": 0, "priority": 255}})
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)

    @allure.title("设置转向灯工作模式_独占需求未超时调用_再超时释放")
    @pytest.mark.full
    def test_caseid_1988580(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        for priority in [0x2F, 0x4F]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                            {"lamp": {"mode": 0, "priority": priority}})
            logger.info(f"sleep 2s wait to recall.")
            sleep(2)
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                            {"lamp": {"mode": 0, "priority": priority}})
            logger.info(f"sleep 3s to check not release.")
            sleep(3)
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                            {"lamp": {"mode": 1, "priority": 0x6F}})   
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                {"out": {"mode": 0, "priority": priority}})
            logger.info(f"sleep 2s to check release [{hex(priority)}] control.")
            sleep(2.1)
            self.partner.empty_all()

            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                            {"lamp": {"mode": 1, "priority": 0x6F}})   
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                    {"sts": {"mode": 1, "priority": 0x6F}})     
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                {"out": {"mode": 1, "priority": 0x6F}})
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
            self.partner.empty_all()

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_MD/MP左转向开到关")
    @pytest.mark.sanity
    def test_caseid_1980120(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # 设置转向灯工作模式:转向灯关闭，优先级为47
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 47}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 获取转向灯工作状态原子能力
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 47}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 47}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 47}, "isSteerHold": False})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)
    
    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态")#6F
    @pytest.mark.smoke
    def test_caseid_1984534(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 111}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 左转
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 111}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 111}})
    
    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_(6F-1-- 6f-0)")
    @pytest.mark.full
    def test_caseid_1984538(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 111}})
        sleep(0.2)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 左转
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 111}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 111}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 111}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 0, "priority": 255}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 0, "priority": 255}})
    
    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_(5F-1-- 6f-2)")
    @pytest.mark.full
    def test_caseid_1984535(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 左转
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 111}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 95}})
    
    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_(5F_1--6f_1--6f_0)")
    @pytest.mark.sanity
    def test_caseid_1984536(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # 设置转向灯工作模式:转向灯关闭，优先级为47
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 左转
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 95}})
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 111}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 95}})
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 111}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 95}})
    
    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_(按键打开双闪--6f_1)")  
    @pytest.mark.sanity
    def test_caseid_1984537(self):
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)  # 转向开关状态
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        set_hazard(self.io, self.ipdu, open=True)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 111}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})
        
    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_MD/MP左转向开再服务调-右转向开-危险报警灯开")  # 被打断
    @pytest.mark.full
    def test_caseid_1980171(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # 设置转向灯工作模式:转向灯关闭，优先级为47
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 47}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 获取转向灯工作状态原子能力--左转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 47}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 47}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 47}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 获取转向灯工作状态原子能力--右转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 2, "priority": 47}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 47}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 47}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)  # 获取转向灯工作状态原子能力--危险报警灯
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_MD/MP左转向开再服务调-危险报警灯-右转向开")  # 被打断
    @pytest.mark.full
    def test_caseid_1980173(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # 设置转向灯工作模式:转向灯关闭，优先级为47
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 47}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 获取转向灯工作状态原子能力--左转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 47}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 47}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 47}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)  # 获取转向灯工作状态原子能力--危险报警灯
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 47}, "isSteerHold": True})
        sleep(0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 获取转向灯工作状态原子能力--右转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 2, "priority": 47}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 47}})

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_MD/MP右转向开到关")
    @pytest.mark.sanity
    def test_caseid_1980121(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # 设置转向灯工作模式:转向灯关闭，优先级为47
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 47}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 2, "priority": 47}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 47}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 47}, "isSteerHold": False})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_MD/MP右转向开再服务调-左转向开-危险报警灯开")  # 被打断
    @pytest.mark.full
    def test_caseid_1980172(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # 设置转向灯工作模式:转向灯关闭，优先级为47
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 47}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 获取转向灯工作状态原子能力--左转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 2, "priority": 47}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 47}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 47}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 获取转向灯工作状态原子能力--右转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 47}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 47}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 47}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)  # 获取转向灯工作状态原子能力--危险报警灯
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_MD/MP右转向开再服务调-危险报警灯-左转向开")  # 被打断
    @pytest.mark.full
    def test_caseid_1980177(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # 设置转向灯工作模式:转向灯关闭，优先级为47
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 47}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 获取转向灯工作状态原子能力--左转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 2, "priority": 47}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 47}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 47}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)  # 获取转向灯工作状态原子能力--右转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 47}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 获取转向灯工作状态原子能力--左转
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 47}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 47}})

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_MD/MP危险报警灯开到关")  # 危险报警灯不管什么方式打开优先级都是0X5F(95)
    @pytest.mark.sanity
    def test_caseid_1980122(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 47}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 3, "priority": 95}})  # 服务调用所以优先级是95需求定的
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 47}, "isSteerHold": False})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_MD/MP危险报警灯开到关--服务调用左转向--调用右转向")  
    def test_caseid_1980178(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 47}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)  # 获取转向灯工作状态原子能力--危险报警灯
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 47}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 获取转向灯工作状态原子能力--左转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 47}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority":47}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 47}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 获取转向灯工作状态原子能力--右转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 2, "priority": 47}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 47}})

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_MD/MP危险报警灯开到关--服务调用右转向--调用左转向")  
    @pytest.mark.full
    def test_caseid_1980180(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 47}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)  # 获取转向灯工作状态原子能力--危险报警灯
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 47}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 获取转向灯工作状态原子能力--右转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 2, "priority": 47}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 47}}, timeout=1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 47}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 获取转向灯工作状态原子能力--左转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 47}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 47}})

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_Game_左转向开到关")
    @pytest.mark.smoke
    def test_caseid_1980123(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 79}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 47}, "isSteerHold": False})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_Game_左转向开--服务调用右转向--危险报警灯开")  
    @pytest.mark.full
    def test_caseid_1980182(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 获取转向灯工作状态原子能力--危险报警灯
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 79}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 获取转向灯工作状态原子能力--左转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 2, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 79}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)  # 获取转向灯工作状态原子能力--右转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_Game_左转向开--服务调用危险报警灯--右转向灯开")  
    @pytest.mark.full
    def test_caseid_1980183(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 获取转向灯工作状态原子能力--危险报警灯
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 79}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)  # 获取转向灯工作状态原子能力--左转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 获取转向灯工作状态原子能力--右转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 2, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 79}})

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_Game_右转向开到关")
    @pytest.mark.sanity
    def test_caseid_1980124(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # 设置转向灯工作模式:转向灯关闭，优先级为47
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 2, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 79}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 47}, "isSteerHold": False})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_Game_右转向开--服务调用左转向--危险报警灯开")  
    @pytest.mark.full
    def test_caseid_1980186(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 获取转向灯工作状态原子能力--危险报警灯
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 2, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 79}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 获取转向灯工作状态原子能力--左转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 79}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)  # 获取转向灯工作状态原子能力--右转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_Game_右转向开--服务调用危险报警灯--左转向灯开") 
    @pytest.mark.full
    def test_caseid_1980185(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # 设置转向灯工作模式:转向灯关闭，优先级为47
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 获取转向灯工作状态原子能力--危险报警灯
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 2, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 79}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)  # 获取转向灯工作状态原子能力--左转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 获取转向灯工作状态原子能力--右转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 79}})

    @allure.title("设置转向灯工作模式_按键0x5F开左转再接口0x2F开左转")  # SOA-28058
    @pytest.mark.full
    def test_caseid_1988896(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)

        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)  
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)  
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
        sleep(0.2)

        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 95}})

        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 47}})
        
        # SOA-28058暂时不修复，注释掉以下步骤
        # sleep(1)      
        # self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
        #                           {"sts": {"mode": 1, "priority": 47}})
        # self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  
        # self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
        #                                 {"out": {"mode": 1, "priority": 47}})

    @allure.title("设置转向灯工作模式_服务设置（1，111）_等待0.5秒_按键关开左转")   # SOA-28163
    @pytest.mark.full
    def test_caseid_1988931(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)

        # 服务接口设置左转（1，111）
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", 
                                             {"lamp": {"mode": 1, "priority": 111}}) #, "isSteerHold": True})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {}, 
                                              {"out": {"mode": 1, "priority": 111}})
        sleep(0.5)
        
        # 方向盘按键关左转
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)  
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)  
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
        sleep(1)  # 延长等待时间1s  SOA-28163
        # 方向盘按键开左转
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)  
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)  
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
        sleep(0.2)

        # 检查转向灯状态
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 95}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                        {"out": {"mode": 1, "priority": 95}})
        
    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_Game_危险报警灯开到关")  # 危险报警灯不管什么方式打开优先级都是0X5F(95)
    @pytest.mark.sanity
    def test_caseid_1980125(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # 设置转向灯工作模式:转向灯关闭，优先级为47
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 47}, "isSteerHold": False})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_Game_危险报警灯开--服务调用左转向开--右转向开")  
    @pytest.mark.full
    def test_caseid_1980187(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                            {"lamp": {"mode": 3, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)  # 获取转向灯工作状态原子能力--危险报警灯
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                    {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                {"out": {"mode": 3, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                            {"lamp": {"mode": 1, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 获取转向灯工作状态原子能力--左转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                    {"sts": {"mode": 1, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                {"out": {"mode": 1, "priority": 79}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                            {"lamp": {"mode": 2, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 获取转向灯工作状态原子能力--右转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                    {"sts": {"mode": 2, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                {"out": {"mode": 2, "priority": 79}})

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_Game_危险报警灯开--服务调用右转向开--左转向开") 
    @pytest.mark.full
    def test_caseid_1980188(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                            {"lamp": {"mode": 3, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)  # 获取转向灯工作状态原子能力--危险报警灯
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                    {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                {"out": {"mode": 3, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                            {"lamp": {"mode": 2, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 获取转向灯工作状态原子能力--左转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                    {"sts": {"mode": 2, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                {"out": {"mode": 2, "priority": 79}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                            {"lamp": {"mode": 1, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 获取转向灯工作状态原子能力--右转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                    {"sts": {"mode": 1, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                {"out": {"mode": 1, "priority": 79}})

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_语音_左转向开到关")
    @pytest.mark.smoke
    def test_caseid_1980126(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 47}, "isSteerHold": False})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_语音_左转向开--服务调用右转向--危险报警灯开")  
    @pytest.mark.sanity
    def test_caseid_1980189(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 获取转向灯工作状态原子能力--危险报警灯
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 获取转向灯工作状态原子能力--左转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 2, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)  # 获取转向灯工作状态原子能力--右转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_语音_左转向开--服务调用危险报警灯--右转向灯开")  
    @pytest.mark.sanity
    def test_caseid_1980190(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 获取转向灯工作状态原子能力--危险报警灯
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)  # 获取转向灯工作状态原子能力--左转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 获取转向灯工作状态原子能力--右转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 2, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 95}})

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_语音_右转向开到关")
    @pytest.mark.smoke
    def test_caseid_1980127(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 2, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 47}, "isSteerHold": False})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_语音_右转向开--服务调用左转向--危险报警灯开") 
    @pytest.mark.sanity
    def test_caseid_1980193(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 获取转向灯工作状态原子能力--危险报警灯
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 2, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 获取转向灯工作状态原子能力--左转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)  # 获取转向灯工作状态原子能力--右转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_语音_右转向开--服务调用危险报警灯--左转向灯开")  
    @pytest.mark.full
    def test_caseid_1980192(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 获取转向灯工作状态原子能力--危险报警灯
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 2, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)  # 获取转向灯工作状态原子能力--左转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                          {"lamp": {"mode": 1, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 获取转向灯工作状态原子能力--右转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 95}})

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_语音_危险报警灯开到关")  # 危险报警灯不管什么方式打开优先级都是0X5F(95)
    @pytest.mark.smoke
    def test_caseid_1980128(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 47}, "isSteerHold": False})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_语音_危险报警灯开--服务调用左转向开--右转向开")
    @pytest.mark.full
    def test_caseid_1980194(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                            {"lamp": {"mode": 3, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)  # 获取转向灯工作状态原子能力--危险报警灯
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                    {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                {"out": {"mode": 3, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                            {"lamp": {"mode": 1, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 获取转向灯工作状态原子能力--左转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                    {"sts": {"mode": 1, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                {"out": {"mode": 1, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                            {"lamp": {"mode": 2, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 获取转向灯工作状态原子能力--右转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                    {"sts": {"mode": 2, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                {"out": {"mode": 2, "priority": 95}})

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_语音_危险报警灯开--服务调用右转向开--左转向开")
    @pytest.mark.sanity
    def test_caseid_1980195(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                            {"lamp": {"mode": 3, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)  # 获取转向灯工作状态原子能力--危险报警灯
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                    {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                {"out": {"mode": 3, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                            {"lamp": {"mode": 2, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 获取转向灯工作状态原子能力--左转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                    {"sts": {"mode": 2, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                {"out": {"mode": 2, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                            {"lamp": {"mode": 1, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 获取转向灯工作状态原子能力--右转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                    {"sts": {"mode": 1, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                {"out": {"mode": 1, "priority": 95}})

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_MD/MP开左转-语音开右转-Game开危险报警灯")
    @pytest.mark.sanity
    def test_caseid_1980199(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 47}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 获取转向灯工作状态原子能力--左转向
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 获取转向灯工作状态原子能力--右转向
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 79}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 获取转向灯工作状态原子能力--右转向

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态&危险报警灯-左转向")  # 服务打开危险报警灯，通过双闪关闭危险报警灯，通过方向盘按键开关打开左转向
    @pytest.mark.smoke
    def test_caseid_1980129(self):
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)  # 转向开关状态
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)  # 释放优先级
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)  # 危险报警灯开
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})
        self.io.hazard_light_open()  # 通过双闪开危险报警灯
        self.io.hazard_light_close()  # 通过双闪关闭危险报警灯
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)  # 转向灯关
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 0, "priority": 255}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 0, "priority": 255}})
        self.partner.send_request_and_return_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [626]})[
            "out"]  # 读取车辆配置字
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)  # 转向开关状态
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 左转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 1, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 95}})
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)  # 转向开关状态

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态&危险报警灯-右转向")  # 服务打开危险报警灯，通过双闪关闭危险报警灯，通过方向盘按键开关打开右转向#老方向盘
    @pytest.mark.full
    def test_caseid_1980130(self):
        self.sd_tester.write_single_ccp(629, 4)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)  # 危险报警灯开
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})
        set_hazard(self.io, self.ipdu, open=False)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)  # 转向灯关
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 0, "priority": 255}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 0, "priority": 255}})
        self.partner.send_request_and_return_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [626]})[
            "out"]  # 读取车辆配置字
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 0)  # 转向开关状态
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 1)  # 转向开关状态
        sleep(1)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 右转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 2, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 255}})
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 0)  # 转向开关状态
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态&危险报警灯-右转向")  # 服务打开危险报警灯，通过双闪关闭危险报警灯，通过方向盘按键开关打开右转向#新方向盘
    @pytest.mark.full
    def test_caseid_1980131(self):
        self.sd_tester.write_single_ccp(629, 6)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)  # 危险报警灯开
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})
        set_hazard(self.io, self.ipdu, open=False)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)  # 转向灯关
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 0, "priority": 255}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 0, "priority": 255}})
        self.partner.send_request_and_return_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [626]})[
            "out"]  # 读取车辆配置字
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 0)  # 转向开关状态
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 1)  # 转向开关状态
        sleep(1)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 右转向
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
                                  {"sts": {"mode": 2, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 95}})

    # @allure.title("SetTurnLampHold_设置禁止方向盘回正关闭左转向灯")  # 请求源MD/MP
    # @pytest.mark.full
    # def test_caseid_10(self):
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     # 设置转向灯工作模式:转向灯关闭，优先级为47
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 0, "priority": 47}})
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SeIndcrStstTurnLampMode",
    #                                      {"lamp": {"mode": 0, "priority": 255}})
    #     # 检查转向灯为关
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)
    #     # 开左转向灯
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 1, "priority": 47}})
    #     # 检查获取通知左转向灯开
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
    #     self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": 1, "priority": 47}})
    #     self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
    #                                           {"out": {"mode": 1, "priority": 47}})
    #     # 禁止方向盘回正关闭转向灯
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampHold", {"flag": 1})
    #     # 设置方向盘角度为10度和0度
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg_0_VDDMBackBoneSignalIPdu02', 14.5)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAgSpd_0_VDDMBackBoneSignalIPdu02', 50)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf_0_VDDMBackBoneSignalIPdu02', 3)
    #     self.partner.send_request_and_ck_resp("SteerWheelService_client", "GetSteerWheelInfo", {},
    #                                           {"out": {"angle": 14.5, "speed": 0.390625, "isvalid": True}},
    #                                           timeout=3)
    #     # 检查转向灯未关闭，左转向灯还开着
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
    #     # 使能转向灯逻辑模块通过判断方向盘转角自动关闭转向灯
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg_0_VDDMBackBoneSignalIPdu02', 0)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAgSpd_0_VDDMBackBoneSignalIPdu02', 0)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf_0_VDDMBackBoneSignalIPdu02', 0)
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampHold", {"flag": 0})
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)
    #
    # @allure.title("SetTurnLampHold_设置禁止方向盘回正关闭右转向灯")  # 请求源MD/MP
    # @pytest.mark.full
    # def test_caseid_11(self):
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     # 设置转向灯工作模式:转向灯关闭，优先级为47
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 0, "priority": 47}})
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
    #                                      {"lamp": {"mode": 0, "priority": 255}})
    #     # 检查转向灯为关
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)
    #     # 开左转向灯
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 2, "priority": 47}})
    #     # 检查获取通知右转向灯开
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)
    #     self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": 2, "priority": 47}})
    #     self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
    #                                           {"out": {"mode": 2, "priority": 47}})
    #     # 禁止方向盘回正关闭转向灯
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampHold", {"flag": 1})
    #     # 设置方向盘角度为10度和0度
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg_0_VDDMBackBoneSignalIPdu02', 14.5)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAgSpd_0_VDDMBackBoneSignalIPdu02', 50)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf_0_VDDMBackBoneSignalIPdu02', 3)
    #     self.partner.send_request_and_ck_resp("SteerWheelService_client", "GetSteerWheelInfo", {},
    #                                           {"out": {"angle": 14.5, "speed": 0.390625, "isvalid": True}},
    #                                           timeout=3)
    #     # 检查转向灯未关闭，右转向灯还开着
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)
    #     # 使能转向灯逻辑模块通过判断方向盘转角自动关闭转向灯
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg_0_VDDMBackBoneSignalIPdu02', 0)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAgSpd_0_VDDMBackBoneSignalIPdu02', 0)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf_0_VDDMBackBoneSignalIPdu02', 0)
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampHold", {"flag": 0})
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)
    #
    # @allure.title("SetTurnLampHold_设置禁止方向盘回正关闭左转向灯")  # 请求源Game
    # @pytest.mark.full
    # def test_caseid_12(self):
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     # 设置转向灯工作模式:转向灯关闭，优先级为47
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
    #                                      {"lamp": {"mode": 0, "priority": 47}})
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
    #                                      {"lamp": {"mode": 0, "priority": 255}})
    #     # 检查转向灯为关
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)
    #     # 开左转向灯
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
    #                                      {"lamp": {"mode": 1, "priority": 79}})
    #     # 检查获取通知左转向灯开
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
    #     self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus",
    #                               {"sts": {"mode": 1, "priority": 79}})
    #     self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
    #                                           {"out": {"mode": 1, "priority": 79}})
    #     # 禁止方向盘回正关闭转向灯
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampHold", {"flag": 1})
    #     # 设置方向盘角度为10度和0度
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg_0_VDDMBackBoneSignalIPdu02', 14.5)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAgSpd_0_VDDMBackBoneSignalIPdu02', 50)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf_0_VDDMBackBoneSignalIPdu02', 3)
    #     self.partner.send_request_and_ck_resp("SteerWheelService_client", "GetSteerWheelInfo", {},
    #                                           {"out": {"angle": 14.5, "speed": 0.390625, "isvalid": True}},
    #                                           timeout=3)
    #     # 检查转向灯未关闭，左转向灯还开着
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
    #     # 使能转向灯逻辑模块通过判断方向盘转角自动关闭转向灯
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg_0_VDDMBackBoneSignalIPdu02', 0)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAgSpd_0_VDDMBackBoneSignalIPdu02', 0)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf_0_VDDMBackBoneSignalIPdu02', 0)
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampHold", {"flag": 0})
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)
    #
    # @allure.title("SetTurnLampHold_设置禁止方向盘回正关闭右转向灯")  # 请求源Game
    # @pytest.mark.full
    # def test_caseid_13(self):
    #     self.sd_tester.change_car_mode(0)
    #     self.sd_tester.change_usage_mode(13)
    #     # 设置转向灯工作模式:转向灯关闭，优先级为47
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 0, "priority": 47}})
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
    #                                      {"lamp": {"mode": 0, "priority": 255}})
    #     # 检查转向灯为关
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)
    #     # 开左转向灯
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 2, "priority": 79}})
    #     # 检查获取通知右转向灯开
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)
    #     self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": 2, "priority": 79}})
    #     self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
    #                                           {"out": {"mode": 2, "priority": 79}})
    #     # 禁止方向盘回正关闭转向灯
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampHold", {"flag": 1})
    #     # 设置方向盘角度为10度和0度
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg_0_VDDMBackBoneSignalIPdu02', 14.5)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAgSpd_0_VDDMBackBoneSignalIPdu02', 50)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf_0_VDDMBackBoneSignalIPdu02', 3)
    #     self.partner.send_request_and_ck_resp("SteerWheelService_client", "GetSteerWheelInfo", {},
    #                                           {"out": {"angle": 14.5, "speed": 0.390625, "isvalid": True}},
    #                                           timeout=3)
    #     # 检查转向灯未关闭，右转向灯还开着
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)
    #     # 使能转向灯逻辑模块通过判断方向盘转角自动关闭转向灯
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg_0_VDDMBackBoneSignalIPdu02', 0)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAgSpd_0_VDDMBackBoneSignalIPdu02', 0)
    #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf_0_VDDMBackBoneSignalIPdu02', 0)
    #     self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampHold", {"flag": 0})
    #     self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_转向灯服务由转角关闭功能_左转向灯")  # 请求源MD/MP
    @pytest.mark.sanity
    def test_caseid_1980134(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3)  # 方向盘转角角度Qf==3(方向盘转角状态有效)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # 开左转向灯
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 47}, "isSteerHold": True})
        # sleep(2)
        # self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        # 检查获取通知左转向灯开
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": 1, "priority": 47}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 47}})
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.52)
        sleep(0.5)
        # 检查转向灯关闭，左转向灯
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": 0, "priority": 255}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 0, "priority": 255}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_转向灯服务由转角关闭功能_左转向灯")  # 请求源Game
    @pytest.mark.sanity
    def test_caseid_1980135(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # 开左转向灯
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 79}, "isSteerHold": True})
        # sleep(2)
        # self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        # 检查获取通知左转向灯开
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": 1, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 79}})
        # 设置方向盘角度
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.52)
        # 检查转向灯未关闭，左转向灯
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": 0, "priority": 255}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 0, "priority": 255}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_转向灯服务由转角关闭功能_左转向灯")  # 请求源语音
    @pytest.mark.full
    def test_caseid_1980136(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # 开左转向灯8
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}, "isSteerHold": True})
        # sleep(2)
        # self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        # 检查获取通知左转向灯开
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": 1, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 95}})
        # 设置方向盘角度
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.52)
        # 检查转向灯未关闭，左转向灯
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": 0, "priority": 255}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 0, "priority": 255}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_转向灯服务由转角关闭功能_右转向灯")  # 请求源MD/MP
    @pytest.mark.full
    def test_caseid_1980137(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # 开右转向灯
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 47}, "isSteerHold": True})
        # sleep(2)
        # self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.8)
        sleep(0.5)
        # 检查获取通知右转向灯开
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": 2, "priority": 47}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 47}})
        # 设置方向盘角度
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.8)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.52)
        # 检查转向灯未关闭，右转向灯
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": 0, "priority": 255}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 0, "priority": 255}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_转向灯服务由转角关闭功能_右转向灯")  # 请求源Game
    @pytest.mark.sanity
    def test_caseid_1980138(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 79}, "isSteerHold": True})
        # sleep(2)
        # self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.8)
        sleep(0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": 2, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 79}})
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.8)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.52)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": 0, "priority": 255}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 0, "priority": 255}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_转向灯服务由转角关闭功能_右转向灯")  # 请求源语音
    @pytest.mark.smoke
    def test_caseid_1980139(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # 开右转向灯8
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 95}, "isSteerHold": True})
        # sleep(2)
        # self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.8)
        sleep(0.5)
        # 检查获取通知右转向灯开
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": 2, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 95}})
        # 设置方向盘角度为10度和0度
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.8)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.52)
        # 检查转向灯未关闭，右转向灯
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": 0, "priority": 255}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 0, "priority": 255}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_转向灯服务由转角关闭功能_右转向灯通过按键开左转向")  # 请求源语音--打断机制
    @pytest.mark.full
    def test_caseid_1980140(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 95}, "isSteerHold": True})
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.8)
        sleep(0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)  # 转向开关状态
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)  
        sleep(0.5)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": 1, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 95}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 左转向

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_转向灯服务由转角关闭功能_右转向-未关闭前服务调用-左转向")  # --打断机制
    @pytest.mark.sanity
    def test_caseid_1980204(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # 开右转向灯
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 95}, "isSteerHold": True})
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.8)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 79}, "isSteerHold": True})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 79}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_转向灯服务由转角关闭功能_右转向-未关闭前服务调用-危险报警灯")  # --打断机制
    @pytest.mark.full
    def test_caseid_1980205(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # 开右转向灯
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 95}, "isSteerHold": True})
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.8)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 79}, "isSteerHold": True})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_转向灯服务由转角关闭功能_左转向灯通过按键开右转向")  # 请求源语音--打断机制  老方向盘
    @pytest.mark.full
    def test_caseid_1980142(self):
        self.sd_tester.write_single_ccp(629, 4)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # 开右转向灯8
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}, "isSteerHold": True})
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 0)  # 转向开关状态
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 1)  # 转向开关状态
        sleep(0.5)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": 2, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 95}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 右转向

    @allure.title("设置转向灯工作模式&获取|通知转向灯工作状态_转向灯服务由转角关闭功能_左转向灯通过按键开右转向")  # 请求源语音--打断机制  新方向盘
    @pytest.mark.full
    def test_caseid_1980143(self):
        self.sd_tester.write_single_ccp(629, 6)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # 开右转向灯8
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}, "isSteerHold": True})
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 0)  # 转向开关状态
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 1)  # 转向开关状态
        sleep(0.5)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": 2, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 95}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 右转向
    
    @allure.title("服务调用0XFF-当前是5F服务调用-用2F服务打断")
    @pytest.mark.sanity
    def test_caseid_1984544(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 左转向
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 47}})
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('DrvrAsscSysIndcrReq', [0, 1])
    
    @allure.title("服务调用0XFF-当前是5F服务调用-用4F服务打断")
    @pytest.mark.full
    def test_caseid_1984545(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 左转向
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 79}})
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('DrvrAsscSysIndcrReq', [0, 1])
    
    @allure.title("服务调用0XFF-当前是5F服务调用-用6F服务打断")#5301下发一次0-1
    @pytest.mark.full
    def test_caseid_1984554(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)  # 左转向
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 95}})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 111}})
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('DrvrAsscSysIndcrReq', [0, 1])
    
    @allure.title("当前是5F语音调用-用5F方向盘按键打断")#左转--打开右转
    @pytest.mark.sanity
    def test_caseid_1984555(self):
        self.sd_tester.write_single_ccp(629, 6)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}})
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 0)  # 转向开关状态
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 1)  # 转向开关状态
        sleep(0.5)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": 2, "priority": 95}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)
    
    @allure.title("2F调用-用0XFF释放")#
    @pytest.mark.full
    def test_caseid_1984557(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 47}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 255}})
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('DrvrAsscSysIndcrReq', [0, 1])
    
    @allure.title("4F调用-用0XFF释放-5F关")#
    @pytest.mark.full
    def test_caseid_1984853(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 79}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 255}})
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 0, "priority": 255}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('DrvrAsscSysIndcrReq', [0, 1, 1, 0])
    
    @allure.title("5F开左转-用4F打断-5F开右转")#
    @pytest.mark.full
    def test_caseid_1984854(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 79}})
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 79}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('DrvrAsscSysIndcrReq', [0, 1])
    
    @allure.title("4F开左转-用4F开危险报警灯-5F关")
    @pytest.mark.full
    def test_caseid_1984877(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 79}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 255}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)
    
    @allure.title("4F开危险报警灯-双闪关 -5F开左转")
    @pytest.mark.full
    def test_caseid_1984878(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)
        set_hazard(self.io, self.ipdu, open=False)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 0, "priority": 255}})
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 95}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
    
    @allure.title("4F开危险报警灯-双闪关-6F开左转")
    @pytest.mark.full
    def test_caseid_1984879(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)
        set_hazard(self.io, self.ipdu, open=False)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 0, "priority": 255}})
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 111}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 111}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
    
    @allure.title("5F开左转-5F开危险报警灯-6F开右转")#
    @pytest.mark.full
    def test_caseid_1984880(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 95}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 111}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 3, "priority": 95}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)
    
    @allure.title("4F开左转-2F开左转-4F开右转")#
    @pytest.mark.full
    def test_caseid_1984881(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 79}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 47}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority":47}})
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 47}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
    
    @allure.title("5F开左转-2F开左转-4F开右转")#
    @pytest.mark.full
    def test_caseid_1984882(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 95}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 47}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority":47}})
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 79}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 47}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
    
    @allure.title("5f开左转-按键开右转")#
    @pytest.mark.sanity
    def test_caseid_1984883(self):
        self.sd_tester.write_single_ccp(629, 4)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # 开左转向灯
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}})
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 0)  # 转向开关状态
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 1)  # 转向开关状态
        sleep(0.5)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": 2, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 2, "priority": 95}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)  # 右转向
    
    @allure.title("5f开左转-按键关左转")#
    @pytest.mark.sanity
    def test_caseid_1984884(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # 开右转向灯
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}})
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.8)
        sleep(0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)  # 转向开关状态
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
        sleep(0.2)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 0, "priority": 255}})
    
    @allure.title("5F开左转-2F开左转-5F开右转")#
    @pytest.mark.full
    def test_caseid_1984885(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 95}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 47}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority":47}})
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 95}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": 1, "priority": 47}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
    
    @allure.title("多次调用转向灯:DrvrAsscSysIndcrReq 与IndcrSts")#
    @pytest.mark.sanity
    def test_caseid_1986249(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}})
        sleep(1)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}})
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 95}})
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}})
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 95}})
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}})
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 95}})
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('DrvrAsscSysIndcrReq', [0, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 3, 3, 1])
    
    @allure.title("多次调用转向灯DrvrAsscSysIndcrReq与IndcrSts变化")#
    @pytest.mark.full
    def test_caseid_1986250(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 95}})
        sleep(0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 1, "priority": 47}})
        sleep(1)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 2, "priority": 47}})
        sleep(1)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 2, timeout=1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 255}})
        sleep(0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 3, "priority": 0}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 3, timeout=1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('DrvrAsscSysIndcrReq', [0, 1, 1, 2, 2, 3])

    def steerwhl_set_turnlamp(self, open_by='method', close_by='button', priority=95, mode=1, isSteerHold=True, check_event=True):
        """
        通过按键或者调用服务打开转向灯，然后通过按键或方向盘回正或接口调用关闭转向
        @param open_by:(method, button) 打开转向灯方式，通过服务接口打开，或方向盘按键打开
        @param close_by:(method, button, angle) 关闭转向灯方式，通过服务接口关闭，或方向盘按键关闭，或方向盘转角回正关闭
        @param priority: 转向灯的优先级
        @param mode: 转向灯的模式
        @param isSteerHold: 方向盘回正是否关闭转向灯
        @param check_event: 打开时是否检查event
        """
        self.partner.empty_all()
        logger.info(f"[steerwhl_set_turnlamp][open_by:{open_by}][close_by:{close_by}][priority:{priority}][mode:{mode}][isSteerHold:{isSteerHold}]")
        if close_by == 'angle': # 方向盘设置角度
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3) #方向盘转角状态有效

        # 开左转向灯
        if open_by == 'method':
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", 
                                            {"lamp": {"mode": mode, "priority": priority}, "isSteerHold": isSteerHold})
            if check_event:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": mode, "priority": priority}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                {"out": {"mode": mode, "priority": priority}})
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', mode, timeout=1)
        elif open_by == 'button':
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampHold", {"flag": int(not isSteerHold)})
            sleep(0.2)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)  
            sleep(0.2)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)  # 转向开关短按
            sleep(0.2)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
            sleep(0.2)
            
        sleep(1)
        
        if close_by == 'button': # 方向盘按键关左转向灯
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)  
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)  # 转向开关短按
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
            sleep(0.5)
        elif close_by == 'angle': # 方向盘回正关左转向灯
            # 设置方向盘角度
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.52)
        elif close_by == 'method': # 服务接口关左转向灯
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", 
                                            {"lamp": {"mode": 0, "priority": priority}, "isSteerHold": isSteerHold})
        sleep(1)    # 等待1秒防止状态跳变
        
        # 检查左转向灯
        if (isSteerHold and close_by == 'angle') or (close_by == 'button') or (close_by == 'method'):
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": 0, "priority": 255}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                {"out": {"mode": 0, "priority": 255}})
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)
        else:
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                                {"out": {"mode": mode, "priority": priority}})
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', mode, timeout=1)
    
    @pytest.mark.steer
    @allure.title("优先级95开左转_方向盘按键关左转_优先级111开左转_方向盘按键关左转")
    @pytest.mark.sanity
    def test_caseid_1988466(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.steerwhl_set_turnlamp(open_by='method', close_by='button', priority=95)
        self.steerwhl_set_turnlamp(open_by='method', close_by='button', priority=111)

    @pytest.mark.steer
    @allure.title("优先级95开左转_方向盘回正关左转_优先级111开左转_方向盘按键关左转")
    @pytest.mark.sanity
    def test_caseid_1988467(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.steerwhl_set_turnlamp(open_by='method', close_by='angle',  priority=95)
        self.steerwhl_set_turnlamp(open_by='method', close_by='button', priority=111)

    @pytest.mark.steer
    @allure.title("优先级95开左转_方向盘按键关左转_优先级111开左转_方向盘回正关左转")
    @pytest.mark.sanity
    def test_caseid_1988468(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.steerwhl_set_turnlamp(open_by='method', close_by='button', priority=95)
        self.steerwhl_set_turnlamp(open_by='method', close_by='angle',  priority=111)

    @pytest.mark.steer
    @allure.title("优先级95开左转_方向盘回正关左转_优先级111开左转_方向盘回正关左转")
    @pytest.mark.sanity
    def test_caseid_1988469(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.steerwhl_set_turnlamp(open_by='method', close_by='angle', priority=95)
        self.steerwhl_set_turnlamp(open_by='method', close_by='angle', priority=111)

    @pytest.mark.steer
    @allure.title("按键回正使能与接口回正使能")
    @pytest.mark.full
    def test_caseid_1988780(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.steerwhl_set_turnlamp(open_by='button', close_by='angle', priority=0x5F, isSteerHold=True)
        self.steerwhl_set_turnlamp(open_by='method', close_by='angle', priority=0x4F, isSteerHold=True)

    @pytest.mark.steer
    @allure.title("按键回正使能与接口回正禁止")
    @pytest.mark.full
    def test_caseid_1988781(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.steerwhl_set_turnlamp(open_by='button', close_by='angle', priority=0x5F, isSteerHold=True)
        self.steerwhl_set_turnlamp(open_by='method', close_by='angle', priority=0x4F, isSteerHold=False)

    @pytest.mark.steer
    @allure.title("按键回正禁止与接口回正使能") # SOA-28058
    @pytest.mark.full
    def test_caseid_1988782(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.steerwhl_set_turnlamp(open_by='button', close_by='angle', priority=0x5F, isSteerHold=False)
        # self.steerwhl_set_turnlamp(open_by='method', close_by='angle', priority=0x5F, isSteerHold=True)  # SOA-28058暂时不修复，注释此步骤

    @pytest.mark.steer
    @allure.title("按键回正禁止与接口回正禁止") # SOA-27733
    @pytest.mark.full
    def test_caseid_1988783(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.steerwhl_set_turnlamp(open_by='button', close_by='angle', priority=0x5F, isSteerHold=False)
        # self.steerwhl_set_turnlamp(open_by='method', close_by='angle', priority=0x5F, isSteerHold=False, check_event=False)  # SOA-28058暂时不修复，注释此步骤

    @pytest.mark.steer
    @allure.title("按键回正使能后接口开按键关")
    @pytest.mark.full
    def test_caseid_1988785(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.steerwhl_set_turnlamp(open_by='button', close_by='angle',  priority=0x5F, isSteerHold=True)
        self.steerwhl_set_turnlamp(open_by='method', close_by='button', priority=0x6F, isSteerHold=False)

    @pytest.mark.steer
    @allure.title("按键回正使能后接口开接口关")
    @pytest.mark.full
    def test_caseid_1988786(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.steerwhl_set_turnlamp(open_by='button', close_by='angle',  priority=0x5F, isSteerHold=True)
        self.steerwhl_set_turnlamp(open_by='method', close_by='method', priority=0x5F, isSteerHold=True)

    @pytest.mark.steer
    @allure.title("按键回正使能后按键开按键关")
    @pytest.mark.full
    def test_caseid_1988787(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.steerwhl_set_turnlamp(open_by='button', close_by='angle',  priority=0x5F, isSteerHold=True)
        self.steerwhl_set_turnlamp(open_by='button', close_by='button', priority=0x5F, isSteerHold=True)

    @pytest.mark.steer
    @allure.title("按键回正使能后按键开回正关") # 即按键回正使能调用两次
    @pytest.mark.full
    def test_caseid_1988788(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13) 
        self.steerwhl_set_turnlamp(open_by='button', close_by='angle', priority=0x5F, isSteerHold=True)
        self.steerwhl_set_turnlamp(open_by='button', close_by='angle', priority=0x5F, isSteerHold=True)

    @pytest.mark.steer
    @allure.title("按键回正使能后按键开接口关")
    @pytest.mark.full
    def test_caseid_1988789(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.steerwhl_set_turnlamp(open_by='button', close_by='angle',  priority=0x5F, isSteerHold=True)
        self.steerwhl_set_turnlamp(open_by='button', close_by='method', priority=0x5F, isSteerHold=True)

    @pytest.mark.steer
    @allure.title("按键回正使能和接口回正禁止同时设置_接口开左转然后回正")
    @pytest.mark.full
    def test_caseid_1988790(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3) 
                    
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampHold", {"flag": 0})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", 
                                        {"lamp": {"mode": 1, "priority": 95}, "isSteerHold": False})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)     
        self.partner.empty_all()
        # 方向盘回正
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.52)
        
        # 检查转向灯没有关闭
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                            {"out": {"mode": 1, "priority": 95}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
           
    @pytest.mark.steer
    @allure.title("按键回正使能和接口回正禁止同时设置_按键开左转然后回正")
    @pytest.mark.full
    def test_caseid_1988791(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3) 
        
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampHold", {"flag": 0})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", 
                                        {"lamp": {"mode": 0, "priority": 95}, "isSteerHold": False})
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)  
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)  # 转向开关短按
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
        sleep(0.2)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)     
        self.partner.empty_all()
        # 方向盘回正
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.52)
        
        # 检查转向灯已关闭
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                            {"out": {"mode": 0, "priority": 255}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1) 

    @pytest.mark.steer
    @allure.title("按键回正禁止和接口回正使能同时设置_按键开左转然后回正")
    @pytest.mark.full
    def test_caseid_1988792(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3) 
        
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampHold", {"flag": 1})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", 
                                        {"lamp": {"mode": 0, "priority": 95}, "isSteerHold": True})
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)  
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)  # 转向开关短按
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
        sleep(0.2)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)     
        self.partner.empty_all()
        # 方向盘回正
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.52)
        sleep(1)
        
        # 检查转向灯没有关闭
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                            {"out": {"mode": 1, "priority": 95}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)
        
    @pytest.mark.steer
    @allure.title("按键回正禁止和接口回正使能同时设置_接口开左转然后回正")
    @pytest.mark.full
    def test_caseid_1988793(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3) 
                    
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampHold", {"flag": 1})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", 
                                        {"lamp": {"mode": 1, "priority": 95}, "isSteerHold": True})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 1, timeout=1)     
        self.partner.empty_all()
        # 方向盘回正
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.52)
        sleep(1)
        
        # 检查转向灯已关闭
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                            {"out": {"mode": 0, "priority": 255}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1) 

    @pytest.mark.steer
    @allure.title("设置转向灯工作模式_重启场景初始状态")
    @pytest.mark.full
    def test_caseid_1988794(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        for mode in [0, 1, 2, 3]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                            {"lamp": {"mode": mode, "priority": 95}}, timeout=0.3)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                            {"out": {"mode": mode, "priority": 0xff if mode == 0 else 95}})    
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT)
            logger.info(f"mode:{mode} restart success.")
            sleep(15)
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": 0, "priority": 0xff}}, timeout=10)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                {"out": {"mode": 0, "priority": 0xff}})    
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', 0, timeout=1)
            

    def set_lever_signal(self, value, start=0, end=0):
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', start) 
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', value) 
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', end) 
        sleep(0.1)
    
    def ck_event_resp_indcrsts(self, mode, priority, check_event=True):
        if check_event:
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", {"sts": {"mode": mode, "priority": priority}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {}, {"out": {"mode": mode, "priority": priority}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', mode, timeout=1) 

    def lever_open_turnlamp(self, mode=1, priority=0x5f):
        self.partner.empty_all()
        open_sig = random.randint(1, 2) if mode == 1 else random.randint(3, 4)
        logger.info(f"[lever_open_turnlamp] open_sig:{open_sig}, mode:{mode}, priority:{priority}")
        
        self.set_lever_signal(open_sig)
        self.ck_event_resp_indcrsts(mode, priority)

    def lever_close_turnlamp(self, cur_mode, exp_mode=0, exp_priority=0xff):
        self.partner.empty_all()
        close_sig = random.randint(1, 2) if cur_mode == 1 else random.randint(3, 4)
        logger.info(f"[lever_close_turnlamp] close_sig:{close_sig}, exp_mode:{exp_mode}, exp_priority:{exp_priority}")
        
        self.set_lever_signal(close_sig)
        check_event = False if cur_mode == exp_mode else True
        self.ck_event_resp_indcrsts(exp_mode, exp_priority, check_event=check_event)
        
    def lever_open_close_turnlamp(self, mode, open_sig=1, close_sig=1):
        if mode == 2 and open_sig == 1:
            open_sig = 3
        if mode == 2 and close_sig == 1:
            close_sig = 3
        logger.info(f"[lever_open_close_turnlamp] mode:{mode}, open_sig:{open_sig}, close_sig:{close_sig}")
        
        self.set_lever_signal(open_sig)
        self.ck_event_resp_indcrsts(mode, 0x5f)

        self.set_lever_signal(close_sig)
        if (mode == 1 and close_sig in [3, 4]) or (mode == 2 and close_sig in [1, 2]):
            exp_mode = 2 if mode == 1 else 1
            exp_priority = 0x5f
        else:
            exp_mode = 0
            exp_priority = 0xff
        self.ck_event_resp_indcrsts(exp_mode, exp_priority)

    @pytest.mark.lever
    @allure.title("转向灯_拨杆激活退出左转")
    @pytest.mark.sanity
    def test_caseid_1989060(self):
        # 非Normal下MCU不能用转向灯，只需要检查MPU下行pdu信号
        for car_mode in [1, 2, 3, 5, 0]:
            logger.info(f"car_mode:{car_mode}")
            self.sd_tester.change_car_mode(car_mode)
            self.sd_tester.change_usage_mode(11)

            self.bgm_eth_inter.start_bgm_tcpdump()
            self.set_lever_signal(1)    # 开左转
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(1)
            self.bgm_eth_inter.ck_signal_values('DrvrAsscSysIndcrReq', [3 if car_mode == 3 else 0, 1])
            if car_mode == 3:
                self.set_hazard_button(open=False)
        
        self.lever_close_turnlamp(cur_mode=1)   # 关左转
        
        for usage_mode in [2, 11, 13]:
            logger.info(f"usage_mode:{usage_mode}")
            self.sd_tester.change_usage_mode(usage_mode)
            self.lever_open_close_turnlamp(1)

        for open_sig in [1, 2]:
            logger.info(f"open_sig:{open_sig}")
            self.lever_open_close_turnlamp(1, open_sig=open_sig)

        for close_sig in [1, 2, 3, 4]:
            logger.info(f"close_sig:{close_sig}")
            self.lever_open_close_turnlamp(1, close_sig=close_sig)

    @pytest.mark.lever
    @allure.title("转向灯_拨杆激活退出左转_前提不满足")
    @pytest.mark.full
    def test_caseid_1989061(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        
        self.set_lever_signal(1)
        self.ck_event_resp_indcrsts(0, 0xff, check_event=False)

    @pytest.mark.lever
    @allure.title("转向灯_拨杆激活退出左转_激活不满足")
    @pytest.mark.full
    def test_caseid_1989062(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)

        self.set_lever_signal(5)
        self.ck_event_resp_indcrsts(0, 0xff, check_event=False)

        self.set_lever_signal(6)
        self.ck_event_resp_indcrsts(0, 0xff, check_event=False)

        # 1->0
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 1) 
        sleep(0.1)
        self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT)
        self.ck_event_resp_indcrsts(0, 0xff, check_event=False)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 0) 
        sleep(0.1)
        self.ck_event_resp_indcrsts(0, 0xff, check_event=False)
        
    @pytest.mark.lever
    @allure.title("转向灯_拨杆激活退出左转_退出不满足")
    @pytest.mark.full
    def test_caseid_1989063(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        
        self.set_lever_signal(1)
        self.ck_event_resp_indcrsts(1, 0x5f)

        self.set_lever_signal(5)
        self.ck_event_resp_indcrsts(1, 0x5f, check_event=False)

        self.set_lever_signal(6)
        self.ck_event_resp_indcrsts(1, 0x5f, check_event=False)

        self.set_lever_signal(1)      # 关左转
        self.ck_event_resp_indcrsts(0, 0xff)
        
        # 重新开左转，检查信号从 1->0 不会关闭左转
        self.set_lever_signal(1, end=1)     
        self.ck_event_resp_indcrsts(1, 0x5f)           
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 0) 
        sleep(0.1)
        self.ck_event_resp_indcrsts(1, 0x5f, check_event=False)     
        
    @pytest.mark.lever
    @allure.title("转向灯_其他方式开左转_拨杆关左转")
    @pytest.mark.full
    def test_caseid_1989064(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)

        # 其他服务开左转拨杆关左转
        for priority in [0x2f, 0x4f, 0x5f, 0x6f]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 0, "priority": 255}})
            sleep(1)
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 1, "priority": priority}})
            sleep(1)
            if priority in [0x2f, 0x4f]:
                self.lever_close_turnlamp(cur_mode=1, exp_mode=1, exp_priority=priority)
            else:
                self.lever_close_turnlamp(cur_mode=1, exp_mode=0, exp_priority=0xff)

        # 按键开左转
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)  
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)  
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
        # 拨杆关左转
        self.lever_close_turnlamp(cur_mode=1, exp_mode=0, exp_priority=0xff)
        
    @pytest.mark.lever
    @allure.title("转向灯_拨杆开左转_其他方式关左转")
    @pytest.mark.full
    def test_caseid_1989065(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3) 

        for priority in [0x2f, 0x4f, 0x5f, 0xff, 0x6f]:
            self.lever_open_turnlamp(mode=1)
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 0, "priority": priority}})
            sleep(1)
            if priority in [0x6f]:
                self.ck_event_resp_indcrsts(1, 0x5f, check_event=False)     
            elif priority in [0x2f, 0x4f]:
                self.ck_event_resp_indcrsts(0, priority)     
                self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 0, "priority": 255}})
                self.ck_event_resp_indcrsts(0, 0xff, check_event=False)     
            else:
                self.ck_event_resp_indcrsts(0, 0xff)     

        # 按键关左转
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)  
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)  
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
        self.ck_event_resp_indcrsts(0, 0xff)     
        
        # 使能回正关左转
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 0, "priority": 0x5f}, "isSteerHold": True})
        self.lever_open_turnlamp(mode=1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.52)
        self.ck_event_resp_indcrsts(0, 0xff)     

        # 禁止回正关左转
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 0, "priority": 0x5f}, "isSteerHold": False})
        self.lever_open_turnlamp(mode=1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.52)
        self.ck_event_resp_indcrsts(0, 0xff)     

    @pytest.mark.lever
    @allure.title("转向灯_拨杆开左转_其他方式开右转")
    @pytest.mark.full
    def test_caseid_1989068(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)

        self.lever_open_turnlamp(mode=1)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 0)  
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 1)  
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 0)
        self.ck_event_resp_indcrsts(2, 0x5f)     

        self.lever_open_turnlamp(mode=1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 2, "priority": 0x6f}})
        self.ck_event_resp_indcrsts(1, 0x5f, check_event=False)     
        
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 2, "priority": 0x5f}})
        self.ck_event_resp_indcrsts(2, 0x5f)     
               
        self.lever_open_turnlamp(mode=1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 2, "priority": 0x2f}})
        self.ck_event_resp_indcrsts(2, 0x2f)     
        
    @pytest.mark.lever
    @allure.title("转向灯_拨杆开左转_服务开双闪")
    @pytest.mark.full
    def test_caseid_1989066(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)

        self.lever_open_turnlamp(mode=1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 3, "priority": 0x5f}})
        self.ck_event_resp_indcrsts(3, 0x5f)     
        self.lever_open_turnlamp(mode=1)

    @pytest.mark.lever
    @allure.title("转向灯_拨杆开左转_按键开双闪")
    @pytest.mark.full
    def test_caseid_1989067(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)

        self.lever_open_turnlamp(mode=1)
        self.set_hazard_button(open=True)
        self.ck_event_resp_indcrsts(3, 0x5f)   
         
        self.set_hazard_button(open=False)
        self.ck_event_resp_indcrsts(1, 0x5f)    
        
        self.set_hazard_button(open=True)
        self.ck_event_resp_indcrsts(3, 0x5f)    
        
        self.lever_open_turnlamp(mode=1)

    @pytest.mark.lever
    @allure.title("转向灯_拨杆开左转_服务开左转")
    @pytest.mark.full
    def test_caseid_1989069(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)

        self.lever_open_turnlamp(mode=1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 1, "priority": 0x5f}})
        sleep(1)
        self.ck_event_resp_indcrsts(1, 0x5f, check_event=False)    
        self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus")

    @pytest.mark.lever
    @allure.title("转向灯_拨杆激活退出右转")
    @pytest.mark.sanity
    def test_caseid_1989075(self):
        # 非Normal下MCU不能用转向灯，只需要检查MPU下行pdu信号
        for car_mode in [1, 2, 3, 5, 0]:
            logger.info(f"car_mode:{car_mode}")
            self.sd_tester.change_car_mode(car_mode)
            self.sd_tester.change_usage_mode(11)

            self.bgm_eth_inter.start_bgm_tcpdump()
            self.set_lever_signal(3)    # 开右转
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(1)
            self.bgm_eth_inter.ck_signal_values('DrvrAsscSysIndcrReq', [3 if car_mode == 3 else 0, 2])
            if car_mode == 3:
                self.set_hazard_button(open=False)
        
        self.lever_close_turnlamp(cur_mode=2)   # 关右转

        for usage_mode in [2, 11, 13]:
            logger.info(f"usage_mode:{usage_mode}")
            self.sd_tester.change_usage_mode(usage_mode)
            self.lever_open_close_turnlamp(2)

        for open_sig in [3, 4]:
            logger.info(f"open_sig:{open_sig}")
            self.lever_open_close_turnlamp(2, open_sig=open_sig)

        for close_sig in [1, 2, 3, 4]:
            logger.info(f"close_sig:{close_sig}")
            self.lever_open_close_turnlamp(2, close_sig=close_sig)


    @pytest.mark.lever
    @allure.title("转向灯_拨杆激活退出右转_前提不满足")
    @pytest.mark.full
    def test_caseid_1989072(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        
        self.set_lever_signal(3)
        self.ck_event_resp_indcrsts(0, 0xff, check_event=False)

    @pytest.mark.lever
    @allure.title("转向灯_拨杆激活退出右转_激活不满足")
    @pytest.mark.full
    def test_caseid_1989076(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)

        self.set_lever_signal(5)
        self.ck_event_resp_indcrsts(0, 0xff, check_event=False)

        self.set_lever_signal(6)
        self.ck_event_resp_indcrsts(0, 0xff, check_event=False)

        # 3->0
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 3) 
        sleep(0.1)
        self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT)
        self.ck_event_resp_indcrsts(0, 0xff, check_event=False)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 0) 
        sleep(0.1)
        self.ck_event_resp_indcrsts(0, 0xff, check_event=False)
        
    @pytest.mark.lever
    @allure.title("转向灯_拨杆激活退出右转_退出不满足")
    @pytest.mark.full
    def test_caseid_1989078(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        
        self.set_lever_signal(3)
        self.ck_event_resp_indcrsts(2, 0x5f)

        self.set_lever_signal(5)
        self.ck_event_resp_indcrsts(2, 0x5f, check_event=False)

        self.set_lever_signal(6)
        self.ck_event_resp_indcrsts(2, 0x5f, check_event=False)

        self.set_lever_signal(4)      # 关右转
        self.ck_event_resp_indcrsts(0, 0xff)
        
        # 重新开右转，检查信号从 3->0 不会关闭右转
        self.set_lever_signal(3, end=1)     
        self.ck_event_resp_indcrsts(2, 0x5f)           
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 0) 
        sleep(0.1)
        self.ck_event_resp_indcrsts(2, 0x5f, check_event=False)     
        
    @pytest.mark.lever
    @allure.title("转向灯_其他方式开右转_拨杆关右转")
    @pytest.mark.full
    def test_caseid_1989070(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)

        # 其他服务开右转拨杆关右转
        for priority in [0x2f, 0x4f, 0x5f, 0x6f]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 0, "priority": 255}})
            sleep(1)
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 2, "priority": priority}})
            sleep(1)
            if priority in [0x2f, 0x4f]:
                self.lever_close_turnlamp(cur_mode=2, exp_mode=2, exp_priority=priority)
            else:
                self.lever_close_turnlamp(cur_mode=2, exp_mode=0, exp_priority=0xff)

        # 按键开右转
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 0)  
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 1)  
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 0)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {}, {"out": {"mode": 2, "priority": 95}})
        sleep(1)
        
        # 拨杆关右转
        self.lever_close_turnlamp(cur_mode=2, exp_mode=0, exp_priority=0xff)
        
    @pytest.mark.lever
    @allure.title("转向灯_拨杆开右转_其他方式关右转")
    @pytest.mark.full
    def test_caseid_1989077(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3) 

        for priority in [0x2f, 0x4f, 0x5f, 0xff, 0x6f]:
            self.lever_open_turnlamp(mode=2)
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 0, "priority": priority}})
            sleep(1)
            if priority in [0x6f]:
                self.ck_event_resp_indcrsts(2, 0x5f, check_event=False)     
            elif priority in [0x2f, 0x4f]:
                self.ck_event_resp_indcrsts(0, priority)     
                self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 0, "priority": 255}})
                self.ck_event_resp_indcrsts(0, 0xff, check_event=False)     
            else:
                self.ck_event_resp_indcrsts(0, 0xff)     

        # 按键关右转
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 0)  
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 1)  
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 0)
        self.ck_event_resp_indcrsts(0, 0xff)     
        
        # 使能回正关右转
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 0, "priority": 0x5f}, "isSteerHold": True})
        self.lever_open_turnlamp(mode=2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.8)
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.52)
        self.ck_event_resp_indcrsts(0, 0xff)     

        # 禁止回正关右转
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 0, "priority": 0x5f}, "isSteerHold": False})
        self.lever_open_turnlamp(mode=2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.8)
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.52)
        self.ck_event_resp_indcrsts(0, 0xff)     

    @pytest.mark.lever
    @allure.title("转向灯_拨杆开右转_其他方式开左转")
    @pytest.mark.full
    def test_caseid_1989074(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)

        self.lever_open_turnlamp(mode=2)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)  
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)  
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
        self.ck_event_resp_indcrsts(1, 0x5f)     

        self.lever_open_turnlamp(mode=2)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 1, "priority": 0x6f}})
        self.ck_event_resp_indcrsts(2, 0x5f, check_event=False)     
        
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 1, "priority": 0x5f}})
        self.ck_event_resp_indcrsts(1, 0x5f)     
               
        self.lever_open_turnlamp(mode=2)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 1, "priority": 0x2f}})
        self.ck_event_resp_indcrsts(1, 0x2f)     
        
    @pytest.mark.lever
    @allure.title("转向灯_拨杆开右转_服务开双闪")
    @pytest.mark.full
    def test_caseid_1989073(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)

        self.lever_open_turnlamp(mode=2)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 3, "priority": 0x5f}})
        self.ck_event_resp_indcrsts(3, 0x5f)     
        self.lever_open_turnlamp(mode=2)

    @pytest.mark.lever
    @allure.title("转向灯_拨杆开右转_按键开双闪")
    @pytest.mark.full
    def test_caseid_1989079(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)

        self.lever_open_turnlamp(mode=2)
        self.set_hazard_button(open=True)
        self.ck_event_resp_indcrsts(3, 0x5f)   
         
        self.set_hazard_button(open=False)
        self.ck_event_resp_indcrsts(2, 0x5f)    
        
        self.set_hazard_button(open=True)
        self.ck_event_resp_indcrsts(3, 0x5f)    
        
        self.lever_open_turnlamp(mode=2)

    @pytest.mark.lever
    @allure.title("转向灯_拨杆开右转_服务开右转")
    @pytest.mark.full
    def test_caseid_1989071(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)

        self.lever_open_turnlamp(mode=2)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 2, "priority": 0x5f}})
        sleep(1)
        self.ck_event_resp_indcrsts(2, 0x5f, check_event=False)    
        self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus")

    @pytest.mark.lever
    @allure.title("转向灯_拨杆开转向_回正角度")
    @pytest.mark.full
    def test_caseid_1989099(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3) 

        self.lever_open_turnlamp(mode=1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.52)
        sleep(0.2)
        self.ck_event_resp_indcrsts(0, 0xff)  
          
        self.lever_open_turnlamp(mode=1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.52)
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.07)
        self.ck_event_resp_indcrsts(1, 0x5f, check_event=False)  

        self.lever_open_turnlamp(mode=2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.8)
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.52)
        sleep(0.2)
        self.ck_event_resp_indcrsts(0, 0xff)  
          
        self.lever_open_turnlamp(mode=2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.52)
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.07)
        self.ck_event_resp_indcrsts(2, 0x5f, check_event=False)  

    @pytest.mark.lever
    @allure.title("转向灯_服务/拨杆/回正/按键")
    @pytest.mark.full
    def test_caseid_1989085(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3) 

        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 1, "priority": 0x5f}})
        sleep(0.5)
        self.lever_close_turnlamp(cur_mode=1, exp_mode=0)
        
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 1, "priority": 0x6f}, "isSteerHold": True})
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.52)
        self.ck_event_resp_indcrsts(0, 0xff)  

        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)  
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 1)  
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
        self.lever_close_turnlamp(cur_mode=1, exp_mode=0)

    @pytest.mark.lever
    @allure.title("转向灯_按键双闪/拨杆/服务")
    @pytest.mark.full
    def test_caseid_1989088(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        
        self.set_hazard_button(open=True)
        self.lever_open_turnlamp(mode=1)
        self.lever_close_turnlamp(cur_mode=1, exp_mode=3, exp_priority=0x5f)

        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", {"lamp": {"mode": 1, "priority": 0x2f}})
        self.ck_event_resp_indcrsts(1, 0x2f)  

    @pytest.mark.lever
    @allure.title("转向灯_拨杆开左转_重启场景")
    @pytest.mark.full
    def test_caseid_1989082(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)

        self.set_lever_signal(1, end=1)
        self.ck_event_resp_indcrsts(1, 0x5f)  
        self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT)
        self.ck_event_resp_indcrsts(0, 0xff)  
        self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", timeout=1)

        self.lever_open_turnlamp(mode=1)
        self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT)
        self.ck_event_resp_indcrsts(0, 0xff)  
        self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", timeout=1)
        

class Light:
    Brake = 0               # 刹车灯
    Eyebrow = 1             # 轮眉灯
    Hazard = 2              # 报警灯
    Daytime = 3             # 日间行车灯
    Fog = 4                 # 雾灯
    HighBeam = 5            # 远光灯
    LowBeam = 6             # 近光灯
    OutLine = 7             # 示廓灯
    Reverse = 8             # 倒车灯
    HeadLamp = 9            # 前大灯
    Steer = 10              # 转向灯
    Position = 11           # 位置灯
    Welcome = 12            # 迎宾灯
    Pixel = 13              # 像素灯
    Didrl = 14              # DIDRL灯
    License = 15            # 牌照灯
    SteerMirror = 16        # 外后视镜灯
    DoorAlarm = 17          # 车门报警灯
    Corner = 18             # 角灯
    Puddle = 19             # 地面照明灯
    
    Blind = 21              # 盲区灯(弯道灯)
    Reading = 22            # 阅读灯
    Background = 23         # 背光灯
    Foot = 24               # 照脚灯
    SmartAmbient = 25       # 智能氛围灯
    Courtesy = 26           # 礼貌灯
    Trunk = 27              # 行李箱灯
    ArmRestBox = 28         # 扶手箱灯
    Roof = 29               # 顶灯
    Side = 30               # 侧灯
    Glove = 31              # 手套箱灯
    Overtake = 32           # 超车灯
    SteerWheel = 33         # 方向盘灯
    AILight = 34            # AI交互灯
    GeneralAmbient = 35     # 普通氛围灯
    AFS = 36                # 自适应前照灯系统(功能激活)
    AHL = 37                # 大灯水平高度调节(功能激活) 
    PositionPattern = 38    # 位置灯图案切换
    LightCross = 39         # 一字眉灯
    LightADS = 40           # ADS灯
    System = 100            # 灯光系统                        
    

class ZoneID:
    AllOrSingle = 0
    FrontLeft = 1
    FrontRight = 2
    RearLeft = 3
    RearRight = 4
    MiddleRear = 5
    ThreeRowLeft = 6        # 阅读灯使用
    ThreeRowRight = 7       # 阅读灯使用
    MiddleThreeRow = 8      # 阅读灯使用
    Front = 9
    Rear = 10
    ThreeRow = 11           # 阅读灯使用
    Left = 12
    Right = 13
    Ring = 14               # 环
    IpLeft = 15             # 仪表左侧
    IpRight = 16            # 仪表右侧
    TweeterLeft = 17        # 可升降扬声器左侧
    TweeterRight = 18       # 可升降扬声器右侧
    ConsoleLeft = 19        # 中控左侧
    ConsoleRight = 20       # 中控右侧
    leftY1Sts = 21          # 左侧AI指示灯LY1
    leftY2Sts = 22          # 左侧AI指示灯LY2
    leftY3Sts = 23          # 左侧AI指示灯LY3
    leftY4Sts = 24          # 左侧AI指示灯LY4
    rightY1Sts = 25         # 右侧AI指示灯LY1
    rightY2Sts = 26         # 右侧AI指示灯LY2
    rightY3Sts = 27         # 右侧AI指示灯LY3
    rightY4Sts = 28         # 右侧AI指示灯LY4
    
    
@allure.feature("SOA服务接口")
@allure.story("整车控制/LightService")
@pytest.mark.light
class TestLightService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("LightService", "client"),
                                     ("CentralLockService", "client"),
                                     ("KeyService", "client"),
                                     ("DoorService", "client"),
                                     ("BonnetService", "client"),
                                     ("TailGateService", "client"),
                                     ("CarConfigService", "client")])
        self.partner.method_default_timeout = 0.1
        
    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.set_nopeople_incar()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1) # MPU侧档位
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)  
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 35, "inhibitSts": False}]}, timeout=0.5)#普通氛围灯不禁用
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 25, "inhibitSts": False}]}, timeout=0.5)#智能氛围灯不禁用
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 0}, timeout=0.5) #外灯模式关闭
        #轮眉灯状态
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntWheelLampLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedFrntWheelLampRi', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReWheelLampLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReWheelLampRi', 0)
        #AI灯状态
        self.ipdu.set(self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, 'StsOfLedLeftAIILY1', 0)
        self.ipdu.set(self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, 'StsOfLedLeftAIILY2', 0)
        self.ipdu.set(self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, 'StsOfLedLeftAIILY3', 0)
        self.ipdu.set(self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, 'StsOfLedLeftAIILY4', 0)
        self.ipdu.set(self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, 'StsOfLedRightAIILY1', 0)
        self.ipdu.set(self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, 'StsOfLedRightAIILY2', 0)
        self.ipdu.set(self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, 'StsOfLedRightAIILY3', 0)
        self.ipdu.set(self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, 'StsOfLedRightAIILY4', 0)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 0)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 0)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'IntrBriSts', 0)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
                                            {"lights": [{"light": {"type": 33, "zoneId": 12}, "mode": 0,
                                                        "brightness": 0,"color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}]}, timeout=0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
                                            {"lights": [{"light": {"type": 33, "zoneId": 13}, "mode": 0,
                                                        "brightness": 0,"color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}]}, timeout=0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
                                            {"lights": [{"light": {"type": 33, "zoneId": 14}, "mode": 0,
                                                        "brightness": 0,"color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}]}, timeout=0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
                                            {"lights": [{"light": {"type": 3, "zoneId": 0}, "mode": 0,
                                                        "brightness": 0,"color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}]}, timeout=0.5)#日间行车灯关闭
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 12, "mode": 0}]}, timeout=0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 13, "mode": 0}]}, timeout=0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 14, "mode": 0}]}, timeout=0.5)
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr10, 'ALM1FailrStsLEDSts',  0)
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr11, 'ALM2FailrStsLEDSts',  0)
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr12, 'ALM3FailrStsLEDSts',  0)
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr13, 'ALM4FailrStsLEDSts',  0)
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr14, 'ALM5FailrStsLEDSts',  0)
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr15, 'ALM6FailrStsLEDSts',  0)
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr16, 'ALM7FailrStsLEDSts',  0)
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr17, 'ALM8FailrStsLEDSts',  0)
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr18, 'ALM9FailrStsLEDSts',  0)
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr19, 'ALM10FailrStsLEDSts',  0)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 0)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi1SteerWhlTouchSwt2', 0)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 0)
        self.ipdu.set_vehspd(0)  # 车速
        sleep(0.5)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.bgmcli.type_commands("ps -ef|grep -i soa|awk '{printf $2\"\\n\"}'|xargs kill -9;ps -ef|grep -i tcpdump")
        self.partner.empty_all(2)
        
    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu, start=False)

    def set_Pixel_signal(self, Le1=0, Ri1=0, Le2=0, Ri2=0):
        logger.info(f"[set_Pixel_signal]设置信号{Le1,Ri1,Le2,Ri2}")
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntLampLe1', Le1)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedFrntLampRi1', Ri1)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReLampLe2', Le2)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReLampRi2', Ri2)
    
    def set_EDF_signal(self, FrntLampMid1=0, ReLampLe1=0, ReLampRi1=0, ReLampMid1=0):
        logger.info(f"[set_EDF_signal]设置信号{FrntLampMid1,ReLampLe1,ReLampRi1,ReLampMid1}")
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntLampMid1', FrntLampMid1)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReLampLe1', ReLampLe1)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReLampRi1',ReLampRi1)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmmBodyExpoFr02, 'StsOfLedReLampMid1', ReLampMid1)
    
    def set_StsOfLEDFrnt_signal(self, LampLe2=0, LampRi2=0):
        logger.info(f"[set_StsOfLEDFrnt_signal]设置信号{LampLe2,LampRi2}")
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntLampLe2', LampLe2)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedFrntLampRi2', LampRi2)
        sleep(1)
    
    def set_WheelLamp_signal(self, FrntWheelLampLe=0, FrntWheelLampRi=0, LedReWheelLampLe=0, ReWheelLampRi=0):
        logger.info(f"[set_WheelLamp_signal]设置信号{FrntWheelLampLe,FrntWheelLampRi,LedReWheelLampLe,ReWheelLampRi}")    
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntWheelLampLe', FrntWheelLampLe)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedFrntWheelLampRi', FrntWheelLampRi)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReWheelLampLe', LedReWheelLampLe)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReWheelLampRi', ReWheelLampRi)
        
    def set_Fault_signal(self, ALM1=0, ALM2=0, ALM3=0, ALM4=0, ALM5=0, ALM6=0, ALM7=0, ALM8=0, ALM9=0, ALM10=0):    
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr10, 'ALM1FailrStsLEDSts',  ALM1)
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr11, 'ALM2FailrStsLEDSts',  ALM2)
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr12, 'ALM3FailrStsLEDSts',  ALM3)
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr13, 'ALM4FailrStsLEDSts',  ALM4)
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr14, 'ALM5FailrStsLEDSts',  ALM5)
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr15, 'ALM6FailrStsLEDSts',  ALM6)
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr16, 'ALM7FailrStsLEDSts',  ALM7)
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr17, 'ALM8FailrStsLEDSts',  ALM8)
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr18, 'ALM9FailrStsLEDSts',  ALM9)
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr19, 'ALM10FailrStsLEDSts',  ALM10)

    @allure.title("后雾灯控制_mode = @value(0)")
    @pytest.mark.sanity
    def test_caseid_1913707(self):
        self.sd_tester.write_multi_ccp({508: 3, 255: 2})
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 0})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 4, "zoneId": 10}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 0)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("FogSetReReq", [0])
    
    @allure.title("后雾灯控制_mode = @value(1)")
    @pytest.mark.full
    def test_caseid_1981775(self):
        self.sd_tester.write_multi_ccp({508: 3, 255: 2})
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3})  # 近光打开
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 4, "zoneId": 10}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("FogSetReReq", [1])

    @allure.title("后雾灯控制_ExtrLtgStsReFog信号从1跳变为0")
    @pytest.mark.full
    def test_caseid_1981889(self):
        self.sd_tester.write_multi_ccp({508: 3, 255: 2})
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 4, "zoneId": 10}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 4, "zoneId": 10}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 0)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("FogSetReReq", [1, 0])

    @allure.title("背光灯亮度控制 &获取内灯背光亮度状态&通知内灯背光亮度状态")
    @pytest.mark.sanity
    def test_caseid_1918466(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        for bright in [1, 7, 15, 0]:
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
                                             {"lights": [{"light": {"type": 23, "zoneId": 0}, "mode": 0,
                                                          "brightness": bright,
                                                          "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11, 'IntrBriSts', bright)
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                "sts": {"light": {"type": 23, "zoneId": 0}, "sts": 1, "brightness": bright,
                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                  {"lights": [{"type": 23, "zoneId": 0}]},
                                                  {"out": [{"light": {"type": 23, "zoneId": 0},"sts": 1,
                                                            "brightness": bright,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.ck_ordered_array('IntrBriLvlCtrlStsIntrBriSts', [bright])
            self.bgm_eth_inter.ck_ordered_array('IntrBriLvlCtrlStsIdPen1', [0])

    @allure.title("普通氛围灯控制_左前车门普通氛围灯")
    @pytest.mark.full
    def test_caseid_111184(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        for b, R, G, B in [(1, 1, 100, 1),(99, 50, 255, 254), (100, 254, 255, 255), (0, 255, 254, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals(
                [(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness', b),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftRed', R),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftGreen', G),
                (self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBlue', B)], timeout=0.5)
    
    @allure.title("普通氛围灯控制_右前车门普通氛围灯")
    @pytest.mark.smoke
    def test_caseid_111104(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        for b, R, G, B in [(1, 50, 80, 100),(50, 100, 200, 50), (55, 150, 255, 254), (99, 195, 254, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 2}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals([(self.ipdu.cem_lin5.CemCem_Lin5Fr04, 'OrdinaryAmbientLightFrontRightBrightness', b),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr04, 'OrdinaryAmbientLightFrontRightRed', R),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr04, 'OrdinaryAmbientLightFrontRightGreen', G),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr04, 'OrdinaryAmbientLightFrontRightBlue', B)], timeout=0.5)
    
    @allure.title("普通氛围灯控制_左后车门普通氛围灯--ALM2")
    @pytest.mark.full
    def test_caseid_111125(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        for b, R, G, B in [(20, 1, 55, 65),(30, 110, 155, 254), (100, 150, 255, 254), (0, 254, 254, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 3}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            self.ipdu.check_multiple_signals([(self.ipdu.cem_lin5.CemCem_Lin5Fr02, 'OrdinaryAmbientLightRearLeftBrightness', b),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr02, 'OrdinaryAmbientLightRearLeftRed', R),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr02, 'OrdinaryAmbientLightRearLeftGreen', G),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr02, 'OrdinaryAmbientLightRearLeftBlue', B)], timeout=0.5)
    
    @allure.title("普通氛围灯控制_右后车门普通氛围灯--ALM3")
    @pytest.mark.full
    def test_caseid_111181(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        for b, R, G, B in [(1, 1, 100, 1),(99, 50, 255, 254), (100, 254, 255, 255), (0, 255, 254, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 4}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]}, timeout=0.2)
            sleep(0.5)
            self.ipdu.check_multiple_signals([(self.ipdu.cem_lin5.CemCem_Lin5Fr03, 'OrdinaryAmbientLightRearRightBrightness', b),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr03, 'OrdinaryAmbientLightRearRightRed', R),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr03, 'OrdinaryAmbientLightRearRightGreen', G),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr03, 'OrdinaryAmbientLightRearRightBlue', B)], timeout=0.5)
    
    @allure.title("普通氛围灯控制_左扬声器普通氛围灯--ALM8")
    @pytest.mark.sanity
    def test_caseid_111179(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        for b, R, G, B in [(20, 1, 55, 65),(30, 110, 155, 254), (100, 150, 255, 254), (0, 254, 254, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 17}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals([(self.ipdu.cem_lin5.CemCem_Lin5Fr08, 'OrdinaryAmbientLightTweeterLeftBrightness', b),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr08, 'OrdinaryAmbientLightTweeterLeftRed', R),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr08, 'OrdinaryAmbientLightTweeterLeftGreen', G),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr08, 'OrdinaryAmbientLightTweeterLeftBlue', B)], timeout=0.5)
    
    @allure.title("普通氛围灯控制_右扬声器普通氛围灯--ALM7")
    @pytest.mark.full
    def test_caseid_111175(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        for b, R, G, B in [(20, 1, 55, 65),(30, 110, 155, 254), (100, 150, 255, 254), (0, 254, 254, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 18}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals([(self.ipdu.cem_lin5.CemCem_Lin5Fr07, 'OrdinaryAmbientLightTweeterRightBrightness', b),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr07, 'OrdinaryAmbientLightTweeterRightRed', R),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr07, 'OrdinaryAmbientLightTweeterRightGreen', G),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr07, 'OrdinaryAmbientLightTweeterRightBlue', B)], timeout=0.5)
    
    @allure.title("普通氛围灯控制_CC左侧普通氛围灯--ALM6")
    @pytest.mark.sanity
    def test_caseid_111126(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        for b, R, G, B in [(20, 1, 55, 65),(30, 110, 155, 254), (100, 150, 255, 254), (0, 254, 254, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 19}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals([(self.ipdu.cem_lin5.CemCem_Lin5Fr06, 'OrdinaryAmbientLightCCLeftBrightness', b),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr06, 'OrdinaryAmbientLightCCLeftRed', R),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr06, 'OrdinaryAmbientLightCCLeftGreen', G),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr06, 'OrdinaryAmbientLightCCLeftBlue', B)], timeout=0.5)
    
    @allure.title("普通氛围灯控制_CC右侧普通氛围灯--ALM5")
    @pytest.mark.sanity
    def test_caseid_111100(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        for b, R, G, B in [(20, 1, 55, 65),(30, 110, 155, 254), (100, 150, 255, 254), (0, 254, 254, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 20}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals([(self.ipdu.cem_lin5.CemCem_Lin5Fr05, 'OrdinaryAmbientLightCCRightBrightness', b),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr05, 'OrdinaryAmbientLightCCRightRed', R),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr05, 'OrdinaryAmbientLightCCRightGreen', G),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr05, 'OrdinaryAmbientLightCCRightBlue', B)], timeout=0.5)
    
    @allure.title("普通氛围灯控制_CC中间右侧普通氛围灯--ALM7")#Venus有此配置
    @pytest.mark.full
    def test_caseid_1984178(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.sd_tester.write_single_ccp(950, 2)
        for b, R, G, B in [(1, 1, 100, 1),(99, 50, 255, 254), (100, 254, 255, 255), (0, 255, 254, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 29}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals([(self.ipdu.cem_lin5.CemCem_Lin5Fr09, 'OrdinaryAmbientLightCCMiddleRightBrightness', b),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr09, 'OrdinaryAmbientLightCCMiddleRightRed', R),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr09, 'OrdinaryAmbientLightCCMiddleRightGreen', G),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr09, 'OrdinaryAmbientLightCCMiddleRightBlue', B)], timeout=0.5)
    
    @allure.title("普通氛围灯控制_CC中间左侧普通氛围灯--ALM8")#Venus有此配置
    @pytest.mark.sanity
    def test_caseid_1984179(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.sd_tester.write_single_ccp(950, 2)
        for b, R, G, B in [(1, 1, 100, 1),(99, 50, 255, 254), (100, 254, 255, 255), (0, 255, 254, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 30}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals([(self.ipdu.cem_lin5.CemCem_Lin5Fr0A, 'OrdinaryAmbientLightCCMiddleLeftBrightness', b),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr0A, 'OrdinaryAmbientLightCCMiddleLeftRed', R),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr0A, 'OrdinaryAmbientLightCCMiddleLeftGreen', G),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr0A, 'OrdinaryAmbientLightCCMiddleLeftBlue', B)], timeout=0.5)
    
    @allure.title("普通氛围灯控制_中控下部普通氛围灯")
    @pytest.mark.full
    def test_caseid_1987249(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        for b, R, G, B in [(1, 1, 100, 1),(99, 50, 255, 254), (100, 254, 255, 255), (0, 255, 254, 0)]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 35, "zoneId": 31}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(0.5)
            self.ipdu.check_multiple_signals([(self.ipdu.cem_lin5.CemCem_Lin5Fr0B, 'OrdinaryAmbientLightCCUnderBrightness', b),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr0B, 'OrdinaryAmbientLightCCUnderRed', R),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr0B, 'OrdinaryAmbientLightCCUnderGreen', G),
                                              (self.ipdu.cem_lin5.CemCem_Lin5Fr0B, 'OrdinaryAmbientLightCCUnderBlue', B)], timeout=0.5)
    ###  ALM1
    @allure.title("普通氛围灯故障状态_左前门普通氛围灯--ALM1(950=1&964=(1|0)&636=1)")
    @pytest.mark.full
    def test_caseid_1987448(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 1, 964: ccp, 636:1})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": ccp}, {"name": 636, "value": 1}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr10, 'ALM1FailrStsLEDSts',  ALM)
                sleep(1)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 1)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_左前门普通氛围灯--ALM1(950=2&964=0&636=1)")
    @pytest.mark.full
    def test_caseid_1987457(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 2, 964: ccp, 636:1})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": ccp}, {"name": 636, "value": 1}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr10, 'ALM1FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 1)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_左前门普通氛围灯--ALM1(950=1&964=0&636=2)")
    @pytest.mark.full
    def test_caseid_1987453(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 1, 964: ccp, 636:2})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": ccp}, {"name": 636, "value": 2}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr10, 'ALM1FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 1)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_左前门普通氛围灯--ALM1(950=2&964=0&636=2)")
    @pytest.mark.full
    def test_caseid_1987456(self):
        for  ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 2, 964: ccp, 636:2})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": ccp}, {"name": 636, "value": 2}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr10, 'ALM1FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 1)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
                      
    ###  ALM2
    @allure.title("普通氛围灯故障状态_左后门普通氛围灯--ALM2(950=1&964=(1|0)&636=1)")
    @pytest.mark.full
    def test_caseid_1987462(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 1, 964: ccp, 636:1})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": ccp}, {"name": 636, "value": 1}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr11, 'ALM2FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 3)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_左后门普通氛围灯--ALM2(950=2&964=0&636=1)")
    @pytest.mark.sanity
    def test_caseid_1987463(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 2, 964: ccp, 636:1})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": ccp}, {"name": 636, "value": 1}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr11, 'ALM2FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM ==1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 3)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_左后门普通氛围灯--ALM2(950=1&964=0&636=2)")
    @pytest.mark.full
    def test_caseid_1987464(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 1, 964: ccp, 636:2})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": ccp}, {"name": 636, "value": 2}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr11, 'ALM2FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 3)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_左后门普通氛围灯--ALM2(950=2&964=0&636=2)")
    @pytest.mark.sanity
    def test_caseid_1987465(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 2, 964: ccp, 636:2})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": ccp}, {"name": 636, "value": 2}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr11, 'ALM2FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 3)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    ###  ALM3
    @allure.title("普通氛围灯故障状态_右后门普通氛围灯--ALM3(950=1&964=(1|0)&636=1)")
    @pytest.mark.sanity
    def test_caseid_1987469(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 1, 964: ccp, 636:1})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": ccp}, {"name": 636, "value": 1}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr12, 'ALM3FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 4)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_右后门普通氛围灯--ALM3(950=2&964=0&636=1)")
    @pytest.mark.full
    def test_caseid_1987470(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 2, 964: ccp, 636:1})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": ccp}, {"name": 636, "value": 1}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr12, 'ALM3FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 4)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_右后门普通氛围灯--ALM3(950=1&964=0&636=2)")
    @pytest.mark.full
    def test_caseid_1987472(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 1, 964: ccp, 636:2})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": ccp}, {"name": 636, "value": 2}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr12, 'ALM3FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 4)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_右后门普通氛围灯--ALM3(950=2&964=0&636=2)")
    @pytest.mark.smoke
    def test_caseid_1987473(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 2, 964: ccp, 636:2})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": ccp}, {"name": 636, "value": 2}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr12, 'ALM3FailrStsLEDSts',  ALM)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 4)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    ###  ALM4
    @allure.title("普通氛围灯故障状态_右前门普通氛围灯--ALM4(950=1&964=(1|0)&636=1)")
    @pytest.mark.full
    def test_caseid_1987476(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 1, 964: ccp, 636:1})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": ccp}, {"name": 636, "value": 1}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr13, 'ALM4FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 2)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_右前门普通氛围灯--ALM4(950=2&964=0&636=1)")
    @pytest.mark.sanity
    def test_caseid_1987477(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 2, 964: ccp, 636:1})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": ccp}, {"name": 636, "value": 1}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr13, 'ALM4FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 2)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_右前门普通氛围灯--ALM4(950=1&964=0&636=2)")
    @pytest.mark.full
    def test_caseid_1987479(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 1, 964: ccp, 636:2})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": ccp}, {"name": 636, "value": 2}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr13, 'ALM4FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 2)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_右前门普通氛围灯--ALM4(950=2&964=0&636=2)")
    @pytest.mark.sanity
    def test_caseid_1987480(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 2, 964: ccp, 636:2})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": ccp}, {"name": 636, "value": 2}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr13, 'ALM4FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 2)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    ###  ALM5
    @allure.title("普通氛围灯故障状态_中控中间右普通氛围灯--ALM5(950=1&964=1&636=(1|2)")
    @pytest.mark.full
    def test_caseid_1987482(self):
        for ccp in [1, 2]:
            self.sd_tester.write_multi_ccp({950: 1, 964: 1, 636: ccp})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": 1}, {"name": 636, "value": ccp}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr14, 'ALM5FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 29)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_中控右侧普通氛围灯--ALM5(950=1&964=0&636=(1|2))")
    @pytest.mark.full
    def test_caseid_1987483(self):
        for ccp in [1, 2]:
            self.sd_tester.write_multi_ccp({950: 1, 964: 0, 636: ccp})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": 0}, {"name": 636, "value": ccp}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr14, 'ALM5FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 20)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_中控右侧普通氛围灯--ALM5(950=2&964=964=(1|0)&636=1)")
    @pytest.mark.full
    def test_caseid_1987484(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 2, 964: ccp, 636: 1})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": ccp}, {"name": 636, "value": 1}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr14, 'ALM5FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 20)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_可升降扬声器右侧普通氛围灯--ALM5(950=2&964=964=(1|0)&636=2)")
    @pytest.mark.full
    def test_caseid_1987485(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 2, 964: ccp, 636: 2})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": ccp}, {"name": 636, "value": 2}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr14, 'ALM5FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 18)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    ###  ALM6
    @allure.title("普通氛围灯故障状态_中控中间左普通氛围灯--ALM6(950=1&964=1&636=(1|2)")
    @pytest.mark.sanity
    def test_caseid_1987490(self):
        for ccp in [1, 2]:
            self.sd_tester.write_multi_ccp({950: 1, 964: 1, 636: ccp})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": 1}, {"name": 636, "value": ccp}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr15, 'ALM6FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 30)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
                    
    @allure.title("普通氛围灯故障状态_中控左侧普通氛围灯--ALM6(950=1&964=0&636=(1|2))")
    @pytest.mark.full
    def test_caseid_1987491(self):
        for ccp in [1, 2]:
            self.sd_tester.write_multi_ccp({950: 1, 964: 0, 636:ccp})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": 0}, {"name": 636, "value": ccp}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr15, 'ALM6FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 19)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_中控中间右普通氛围灯--ALM6(950=2&964=964=(1|0)&636=1)")
    @pytest.mark.sanity
    def test_caseid_1987492(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 2, 964: ccp, 636: 1})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": ccp}, {"name": 636, "value": 1}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr15, 'ALM6FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 29)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_中控右侧普通氛围灯--ALM6(950=2&964=964=(1|0)&636=2)")
    @pytest.mark.full
    def test_caseid_1987495(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 2, 964: ccp, 636: 2})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": ccp}, {"name": 636, "value": 2}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr15, 'ALM6FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 20)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
                    
    ###  ALM7
    @allure.title("普通氛围灯故障状态_中控下部普通氛围灯--ALM7(950=1&964=1&636=(1|2)")
    @pytest.mark.full
    def test_caseid_1987497(self):
        for ccp in [1, 2]:
            self.sd_tester.write_multi_ccp({950: 1, 964: 1, 636: ccp})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": 1}, {"name": 636, "value": ccp}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr16, 'ALM7FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 31)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_可升降扬声器右侧普通氛围灯--ALM7(950=1&964=0&636=(1|2))")
    @pytest.mark.sanity
    def test_caseid_1987499(self):
        for ccp in [2, 1]:
            self.sd_tester.write_multi_ccp({950: 1, 964: 0, 636: ccp})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": 0}, {"name": 636, "value": ccp}]})
            for y in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr16, 'ALM7FailrStsLEDSts',  y)
                sleep(0.5)
                if ccp == 2:
                    if y == 1:
                        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 18)]}, method_name="GetFaultInfo")
                    else:
                        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                        {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_no_event_and_ck_resp(LIGHT_SERVICE_CLIENT, "LightFault", {"out": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_中控中间左普通氛围灯--ALM7(950=2&964=964=(1|0)&636=1)")
    @pytest.mark.full
    def test_caseid_1987501(self):
        self.sd_tester.write_multi_ccp({950: 1, 964: 0, 636:2})
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr16, 'ALM7FailrStsLEDSts',  0)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                        {"out": [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 2, 964: ccp, 636: 1})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": ccp}, {"name": 636, "value": 1}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr16, 'ALM7FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 30)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_中控中间右普通氛围灯--ALM7(950=2&964=964=(1|0)&636=2)")
    @pytest.mark.full
    def test_caseid_1987574(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 2, 964: ccp, 636: 2})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": ccp}, {"name": 636, "value": 2}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr16, 'ALM7FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 29)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    ###  ALM8
    @allure.title("普通氛围灯故障状态_可升降扬声器左侧普通氛围灯--ALM8(950=1&964=0&636=(2-1)")
    @pytest.mark.full
    def test_caseid_1987507(self):
        for ccp in [1, 2]:
            self.sd_tester.write_multi_ccp({950: 1, 964: 0, 636: ccp})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": 0}, {"name": 636, "value": ccp}]})
            for y in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr17, 'ALM8FailrStsLEDSts',  y)
                sleep(0.5)
                if ccp == 2:
                    if y == 1:
                        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 17)]}, method_name="GetFaultInfo")
                    else:
                        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                        {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_no_event_and_ck_resp(LIGHT_SERVICE_CLIENT, "LightFault", {"out": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_可升降扬声器右侧普通氛围灯--ALM8(950=1&964=1&636=(1|2))")
    @pytest.mark.sanity
    def test_caseid_1987508(self):
        for ccp in [1, 2]:
            self.sd_tester.write_multi_ccp({950: 1, 964: 1, 636: ccp})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": 1}, {"name": 636, "value": ccp}]})
            for y in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr17, 'ALM8FailrStsLEDSts',  y)
                sleep(0.5)
                if ccp == 2:
                    if y == 1:
                        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 18)]}, method_name="GetFaultInfo")
                    else:
                        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                        {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_no_event_and_ck_resp(LIGHT_SERVICE_CLIENT, "LightFault", {"out": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_中控中间左普通氛围灯--ALM8(950=2&964=(0|1)&636=2)")
    @pytest.mark.sanity
    def test_caseid_1987509(self):
        for ccp in [0, 1]:
            self.sd_tester.write_multi_ccp({950: 2, 964: ccp, 636: 2})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": ccp}, {"name": 636, "value": 2}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr17, 'ALM8FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 30)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_中控左侧普通氛围灯--ALM8(950=2&964=964=(1|0)&636=1)")
    @pytest.mark.full
    def test_caseid_1987503(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 2, 964: ccp, 636: 1})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": ccp}, {"name": 636, "value": 1}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr17, 'ALM8FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 19)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    ###  ALM9
    @allure.title("普通氛围灯故障状态_可升降扬声器左侧普通氛围灯--ALM9(950=1&964=1&636=(2-1)")
    @pytest.mark.full
    def test_caseid_1987575(self):
        for ccp in [1, 2]:
            self.sd_tester.write_multi_ccp({950: 1, 964: 1, 636: ccp})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": 1}, {"name": 636, "value": ccp}]})
            for y in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr18, 'ALM9FailrStsLEDSts',  y)
                sleep(0.5)
                if ccp == 2:
                    if y == 1:
                        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 17)]}, method_name="GetFaultInfo")
                    else:
                        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                        {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_no_event_and_ck_resp(LIGHT_SERVICE_CLIENT, "LightFault", {"out": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_可升降扬声器左侧普通氛围灯--ALM9(950=1&964=(0-1)&636=2)")
    @pytest.mark.smoke
    def test_caseid_1987576(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 1, 964: ccp, 636:2})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": ccp}, {"name": 636, "value": 2}]})
            for y in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr18, 'ALM9FailrStsLEDSts',  y)
                sleep(0.5)
                if ccp == 1:
                    if y == 1:
                        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 17)]}, method_name="GetFaultInfo")
                    else:
                        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                        {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_no_event_and_ck_resp(LIGHT_SERVICE_CLIENT, "LightFault", {"out": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_可升降扬声器左侧普通氛围灯--ALM9(950=1&964=(1-0)&636=(2-1))")
    @pytest.mark.sanity
    def test_caseid_1987577(self):
        self.sd_tester.write_multi_ccp({950: 1, 964: 1, 636: 2})#964:ALM Type   636:头枕音响
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": 1}, {"name": 636, "value": 2}]})
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr18, 'ALM9FailrStsLEDSts',  1)
        sleep(0.5)
        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                       {"faults": [Fault(1, 35, 17)]}, method_name="GetFaultInfo")
        self.partner.empty_all(0.5)
        self.sd_tester.write_multi_ccp({950: 1, 964: 0, 636: 1})#964:ALM Type   636:头枕音响
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": 0}, {"name": 636, "value": 1}]})
        self.partner.ck_no_event_and_ck_resp(LIGHT_SERVICE_CLIENT, "LightFault", {"out": [Fault(1, 35, 17)]}, method_name="GetFaultInfo")
        self.sd_tester.write_multi_ccp({950: 1, 964: 1, 636: 2})
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr18, 'ALM9FailrStsLEDSts',  0)
        sleep(0.5)
        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                        {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_中控左侧普通氛围灯--ALM9(950=2&964=(1|0)&636=2)")
    @pytest.mark.full
    def test_caseid_1987578(self):
        for ccp in [1, 0]:
            self.sd_tester.write_multi_ccp({950: 2, 964: ccp, 636: 2})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": ccp}, {"name": 636, "value": 2}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr18, 'ALM9FailrStsLEDSts',  ALM)
                sleep(1)
                if ALM == 1:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                    {"faults": [Fault(1, 35, 19)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                    {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_中控左侧普通氛围灯--ALM9(950=2&964=1&636=2-1)")
    @pytest.mark.sanity
    def test_caseid_1987579(self):
        for ccp in [2, 1]:
            self.sd_tester.write_multi_ccp({950: 2, 964: 1, 636: ccp})#964:ALM Type   636:头枕音响
            self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": 1}, {"name": 636, "value": ccp}]})
            for ALM in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr18, 'ALM9FailrStsLEDSts',  ALM)
                sleep(0.5)
                if ccp == 2:
                    if ALM == 1:
                        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                    {"faults": [Fault(1, 35, 19)]}, method_name="GetFaultInfo")
                    else:
                        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                        {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
                else:
                    self.partner.ck_no_event_and_ck_resp(LIGHT_SERVICE_CLIENT, "LightFault", {"out": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_可升降扬声器左侧普通氛围灯--ALM10(950=2&964=0&636=2)")
    @pytest.mark.full
    def test_caseid_1987617(self):
        self.sd_tester.write_multi_ccp({950: 2, 964: 0, 636:2})#964:ALM Type   636:头枕音响
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": 0}, {"name": 636, "value": 2}]})
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr19, 'ALM10FailrStsLEDSts',  1)
        sleep(0.5)
        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                    {"faults": [Fault(1, 35, 17)]}, method_name="GetFaultInfo")
        self.partner.empty_all(0.5)
        self.sd_tester.write_multi_ccp({950: 1, 964: 1, 636: 1})#964:ALM Type   636:头枕音响
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": 1}, {"name": 636, "value": 1}]})
        self.partner.ck_no_event_and_ck_resp(LIGHT_SERVICE_CLIENT, "LightFault", {"out": [Fault(1, 35, 17)]}, method_name="GetFaultInfo")
        self.sd_tester.write_multi_ccp({950: 2, 964: 0, 636:2})#964:ALM Type   636:头枕音响
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": 0}, {"name": 636, "value": 2}]})
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr19, 'ALM10FailrStsLEDSts',  0)
        sleep(1)
        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                        {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_可升降扬声器左侧普通氛围灯--ALM10(950=2&964=1&636=2)")
    @pytest.mark.full
    def test_caseid_1987618(self):
        self.sd_tester.write_multi_ccp({950: 2, 964: 1, 636:2})#964:ALM Type   636:头枕音响
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": 1}, {"name": 636, "value": 2}]})
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr19, 'ALM10FailrStsLEDSts',  1)
        sleep(0.5)
        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                    {"faults": [Fault(1, 35, 17)]}, method_name="GetFaultInfo")
        self.partner.empty_all(0.5)
        self.sd_tester.write_multi_ccp({950: 1, 964: 0, 636: 1})#964:ALM Type   636:头枕音响
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": 0}, {"name": 636, "value": 1}]})
        self.partner.ck_no_event_and_ck_resp(LIGHT_SERVICE_CLIENT, "LightFault", {"out": [Fault(1, 35, 17)]}, method_name="GetFaultInfo")
        self.sd_tester.write_multi_ccp({950: 2, 964: 1, 636:2})#964:ALM Type   636:头枕音响
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": 1}, {"name": 636, "value": 2}]})
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr19, 'ALM10FailrStsLEDSts',  0)
        sleep(1)
        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                        {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_可升降扬声器左侧普通氛围灯--ALM10(950=2&964=0&636=2切换950:1)")
    @pytest.mark.full
    def test_caseid_1987619(self):
        self.sd_tester.write_multi_ccp({950: 2, 964: 0, 636:2})#964:ALM Type   636:头枕音响
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": 0}, {"name": 636, "value": 2}]})
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr19, 'ALM10FailrStsLEDSts',  1)
        sleep(0.5)
        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                    {"faults": [Fault(1, 35, 17)]}, method_name="GetFaultInfo")
        self.partner.empty_all(0.5)
        self.sd_tester.write_multi_ccp({950: 1, 964: 0, 636: 2})#964:ALM Type   636:头枕音响
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": 0}, {"name": 636, "value": 2}]})
        self.partner.ck_no_event_and_ck_resp(LIGHT_SERVICE_CLIENT, "LightFault", {"out": [Fault(1, 35, 17)]}, method_name="GetFaultInfo")
        self.sd_tester.write_multi_ccp({950: 2, 964: 0, 636:2})#964:ALM Type   636:头枕音响
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": 0}, {"name": 636, "value": 2}]})
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr19, 'ALM10FailrStsLEDSts',  0)
        sleep(1)
        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                        {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_可升降扬声器左侧普通氛围灯--ALM10(950=2&964=0&636=2切换964:1)")
    @pytest.mark.full
    def test_caseid_1987621(self):
        self.sd_tester.write_multi_ccp({950: 2, 964: 0, 636:2})#964:ALM Type   636:头枕音响
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": 0}, {"name": 636, "value": 2}]})
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr19, 'ALM10FailrStsLEDSts',  1)
        sleep(0.5)
        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                    {"faults": [Fault(1, 35, 17)]}, method_name="GetFaultInfo")
        self.partner.empty_all(0.5)
        self.sd_tester.write_multi_ccp({950: 1, 964: 1, 636: 2})#964:ALM Type   636:头枕音响
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": 1}, {"name": 636, "value": 2}]})
        self.partner.ck_no_event_and_ck_resp(LIGHT_SERVICE_CLIENT, "LightFault", {"out": [Fault(1, 35, 17)]}, method_name="GetFaultInfo")
        self.sd_tester.write_multi_ccp({950: 2, 964: 0, 636:2})#964:ALM Type   636:头枕音响
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": 0}, {"name": 636, "value": 2}]})
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr19, 'ALM10FailrStsLEDSts',  0)
        sleep(1)
        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                        {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_可升降扬声器左侧普通氛围灯--ALM10(950=2&964=0&636=2切换946:0)")
    @pytest.mark.full
    def test_caseid_1987624(self):
        self.sd_tester.write_multi_ccp({950: 2, 964: 0, 636:2})#964:ALM Type   636:头枕音响
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": 0}, {"name": 636, "value": 2}]})
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr19, 'ALM10FailrStsLEDSts',  1)
        sleep(0.5)
        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                    {"faults": [Fault(1, 35, 17)]}, method_name="GetFaultInfo")
        self.partner.empty_all(0.5)
        self.sd_tester.write_multi_ccp({950: 2, 964: 0, 636: 1})#964:ALM Type   636:头枕音响
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": 0}, {"name": 636, "value": 1}]})
        self.partner.ck_no_event_and_ck_resp(LIGHT_SERVICE_CLIENT, "LightFault", {"out": [Fault(1, 35, 17)]}, method_name="GetFaultInfo")
        self.sd_tester.write_multi_ccp({950: 2, 964: 0, 636:2})#964:ALM Type   636:头枕音响
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": 0}, {"name": 636, "value": 2}]})
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr19, 'ALM10FailrStsLEDSts',  0)
        sleep(0.5)
        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                        {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_可升降扬声器左侧普通氛围灯--ALM10(950=2&964=0&636=2切换946:1)")
    @pytest.mark.full
    def test_caseid_1987625(self):
        self.sd_tester.write_multi_ccp({950: 2, 964: 0, 636:2})#964:ALM Type   636:头枕音响
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": 0}, {"name": 636, "value": 2}]})
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr19, 'ALM10FailrStsLEDSts',  1)
        sleep(0.5)
        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                    {"faults": [Fault(1, 35, 17)]}, method_name="GetFaultInfo")
        self.sd_tester.write_multi_ccp({950: 2, 964: 1, 636: 1})#964:ALM Type   636:头枕音响
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": 1}, {"name": 636, "value": 1}]})
        self.partner.ck_no_event_and_ck_resp(LIGHT_SERVICE_CLIENT, "LightFault", {"out": [Fault(1, 35, 17)]}, method_name="GetFaultInfo")
        self.sd_tester.write_multi_ccp({950: 2, 964: 0, 636:2})#964:ALM Type   636:头枕音响
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 2}, {"name": 964, "value": 0}, {"name": 636, "value": 2}]})
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr19, 'ALM10FailrStsLEDSts',  0)
        sleep(0.5)
        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                        {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_ccp不满足")
    @pytest.mark.full
    def test_caseid_1987634(self):
        self.sd_tester.write_multi_ccp({950: 3, 964: 3, 636:3})#964:ALM Type   636:头枕音响
        self.set_Fault_signal(1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "LightFault")
    
    @allure.title("普通氛围灯故障状态_一个故障存在时再去制造另一个故障")
    @pytest.mark.full
    def test_caseid_1987645(self):
        self.sd_tester.write_multi_ccp({950: 1, 964: 1, 636:1})#964:ALM Type   636:头枕音响
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr10, 'ALM1FailrStsLEDSts',  1)
        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                        {"faults": [Fault(1, 35, 1)]}, method_name="GetFaultInfo")
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr11, 'ALM2FailrStsLEDSts',  1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                    {"faults": [{"fault": 1, "faultMsg": "","light": {"type": 35,"zoneId": 1},
                                                 "fault": 1, "faultMsg": "","light": {"type": 35,"zoneId": 3}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 35, "zoneId": 1},
                                                              "fault": 1, "faultMsg": "","light": {"type": 35,"zoneId": 3}}]})
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr10, 'ALM1FailrStsLEDSts',  0)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                    {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 35,"zoneId": 1},
                                                 "fault": 1, "faultMsg": "","light": {"type": 35,"zoneId": 3}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 0, "faultMsg": "", "light": {"type": 35, "zoneId": 1},
                                                              "fault": 1, "faultMsg": "","light": {"type": 35,"zoneId": 3}}]})
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr11, 'ALM2FailrStsLEDSts',  0)
        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                        {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯故障状态_大灯水平高度调节（AHL）存在故障时再去制造普通氛围灯故障")
    @pytest.mark.full
    def test_caseid_1987697(self):
        # self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLvlgLeStsOfLvlgLe', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLvlgLeStsOfLvlgLe', 2)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsAHL', 2)
        sleep(0.5)
        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                        {"faults": [Fault(1, 37, 0)]}, method_name="GetFaultInfo")
        self.sd_tester.write_multi_ccp({950: 1, 964: 1, 636:1})
        self.partner.send_request_and_ck_resp(CARCONFIG_SERVICE_CLIENT, "GetConfigList", {"names": [950,964,636]},
                                              {"out": [{"name": 950, "value": 1}, {"name": 964, "value": 1}, {"name": 636, "value": 1}]})
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr10, 'ALM1FailrStsLEDSts',  1)
        sleep(0.5)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                    {"faults": [{"fault": 1, "faultMsg": "","light": {"type": 37,"zoneId": 0}},
                                                {"fault": 1, "faultMsg": "","light": {"type": 35,"zoneId": 1}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 37, "zoneId": 0}},
                                                             {"fault": 1, "faultMsg": "","light": {"type": 35,"zoneId": 1}}]})
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLvlgLeStsOfLvlgLe', 0)
        sleep(0.5)
        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                        {"faults": [Fault(1, 35, 1)]}, method_name="GetFaultInfo")
        self.ipdu.set(self.ipdu.cem_lin5.CemCem_Lin5Fr10, 'ALM1FailrStsLEDSts',  0)
        self.partner.ck_event_and_resp(LIGHT_SERVICE_CLIENT, "LightFault", 
                                                        {"faults": [Fault(0, 100, 0)]}, method_name="GetFaultInfo")
    
    @allure.title("普通氛围灯控制_其他信号发LastValue")
    @pytest.mark.full
    def test_caseid_1984180(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 35, "inhibitSts": True}]})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 35, "inhibitSts": False}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
            {"light": {"type": 35, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
                {"brightness": 1, "color": {"cRed": 2, "cGreen": 3, "cBlue": 4}}]}]})
        sleep(0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftRed', 2, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftGreen', 3, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBlue', 4, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr04, 'OrdinaryAmbientLightFrontRightBrightness', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr04, 'OrdinaryAmbientLightFrontRightRed', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr04, 'OrdinaryAmbientLightFrontRightGreen', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr04, 'OrdinaryAmbientLightFrontRightBlue', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr02, 'OrdinaryAmbientLightRearLeftBrightness', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr02, 'OrdinaryAmbientLightRearLeftRed', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr02, 'OrdinaryAmbientLightRearLeftGreen', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr02, 'OrdinaryAmbientLightRearLeftBlue', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr03, 'OrdinaryAmbientLightRearRightBrightness', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr03, 'OrdinaryAmbientLightRearRightRed', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr03, 'OrdinaryAmbientLightRearRightGreen', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr03, 'OrdinaryAmbientLightRearRightBlue', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr08, 'OrdinaryAmbientLightTweeterLeftBrightness', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr08, 'OrdinaryAmbientLightTweeterLeftRed', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr08, 'OrdinaryAmbientLightTweeterLeftGreen', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr08, 'OrdinaryAmbientLightTweeterLeftBlue', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr07, 'OrdinaryAmbientLightTweeterRightBrightness', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr07, 'OrdinaryAmbientLightTweeterRightRed', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr07, 'OrdinaryAmbientLightTweeterRightGreen', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr07, 'OrdinaryAmbientLightTweeterRightBlue', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr06, 'OrdinaryAmbientLightCCLeftBrightness', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr06, 'OrdinaryAmbientLightCCLeftRed', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr06, 'OrdinaryAmbientLightCCLeftGreen', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr06, 'OrdinaryAmbientLightCCLeftBlue', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr05, 'OrdinaryAmbientLightCCRightBrightness', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr05, 'OrdinaryAmbientLightCCRightRed', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr05, 'OrdinaryAmbientLightCCRightGreen', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr05, 'OrdinaryAmbientLightCCRightBlue', 0, timeout=0.5)

    @allure.title("智能氛围灯控制_左前车门智能氛围灯--SALM2_MARS1")#MARS1有35个灯珠
    @pytest.mark.smoke
    def test_caseid_1984191(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.sd_tester.write_single_ccp(950, 1)
        for b, R, G, B in [(20, 1, 55, 65),(30, 110, 155, 254), (100, 150, 255, 254), (0, 254, 254, 0)]:
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 25, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(10)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            for i in range(35):
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightFrontLeft{i}Brightness", [b])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightFrontLeft{i}Red", [R])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightFrontLeft{i}Green", [G])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightFrontLeft{i}Blue", [B])
    
    @allure.title("智能氛围灯控制_左前车门智能氛围灯--SALM2_Venus")#Venus有31个灯珠
    @pytest.mark.full
    def test_caseid_1984192(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.sd_tester.write_single_ccp(950, 2)
        for b, R, G, B in [(20, 1, 55, 65),(30, 110, 155, 254), (100, 150, 255, 254), (0, 254, 254, 0)]:
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 25, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(10)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            for i in range(32):
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightFrontLeft{i}Brightness", [b])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightFrontLeft{i}Red", [R])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightFrontLeft{i}Green", [G])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightFrontLeft{i}Blue", [B])
        
    @allure.title("智能氛围灯控制_右前车门智能氛围灯--SALM5_MARS1")#MARS1有35个灯珠
    @pytest.mark.sanity
    def test_caseid_1984193(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.sd_tester.write_single_ccp(950, 1)
        for b, R, G, B in [(20, 1, 55, 65),(30, 110, 155, 254), (100, 150, 255, 254), (0, 254, 254, 0)]:
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 25, "zoneId": 2}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(10)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            for i in range(35):
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightFrontRight{i}Brightness", [b])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightFrontRight{i}Red", [R])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightFrontRight{i}Green", [G])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightFrontRight{i}Blue", [B])
    
    @allure.title("智能氛围灯控制_右前车门智能氛围灯--SALM5_Venus")#Venus有31个灯珠
    @pytest.mark.full
    def test_caseid_1984195(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.sd_tester.write_single_ccp(950, 2)
        for b, R, G, B in [(20, 1, 55, 65),(30, 110, 155, 254), (100, 150, 255, 254), (0, 254, 254, 0)]:
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 25, "zoneId": 2}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(10)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            for i in range(32):
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightFrontRight{i}Brightness", [b])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightFrontRight{i}Red", [R])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightFrontRight{i}Green", [G])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightFrontRight{i}Blue", [B])
    
    @allure.title("智能氛围灯控制_左后车门智能氛围灯--SALM3")#bug  SOA-23761
    @pytest.mark.sanity
    def test_caseid_1984196(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.sd_tester.write_single_ccp(950, 2)
        for b, R, G, B in [(20, 1, 55, 65),(30, 110, 155, 254), (100, 150, 255, 254), (0, 254, 254, 0)]:
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 25, "zoneId": 3}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(5)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            for i in range(30):
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightRearLeft{i}Brightness", [b])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightRearLeft{i}Red", [R])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightRearLeft{i}Green", [G])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightRearLeft{i}Blue", [B])
    
    @allure.title("智能氛围灯控制_右后车门智能氛围灯--SALM6")
    @pytest.mark.full
    def test_caseid_1984197(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.sd_tester.write_single_ccp(950, 2)
        for b, R, G, B in [(20, 1, 55, 65),(30, 110, 155, 254), (100, 150, 255, 254), (0, 254, 254, 0)]:
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 25, "zoneId": 4}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(5)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            for i in range(30):
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightRearRight{i}Brightness", [b])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightRearRight{i}Red", [R])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightRearRight{i}Green", [G])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightRearRight{i}Blue", [B])
    
    @allure.title("智能氛围灯控制_左侧IP智能氛围灯--SALM1_MARS1")#MARS1有35个灯珠
    @pytest.mark.full
    def test_caseid_1984219(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.sd_tester.write_single_ccp(950, 1)
        for b, R, G, B in [(20, 1, 55, 65),(30, 110, 155, 254), (100, 150, 255, 254), (0, 254, 254, 0)]:
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 25, "zoneId": 15}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(10)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            for i in range(35):
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightIpLeft{i}Brightness", [b])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightIpLeft{i}Red", [R])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightIpLeft{i}Green", [G])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightIpLeft{i}Blue", [B])
    
    @allure.title("智能氛围灯控制_左侧IP智能氛围灯--SALM1_Venus")#Venus有31个灯珠
    @pytest.mark.sanity
    def test_caseid_1984222(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.sd_tester.write_single_ccp(950, 2)
        for b, R, G, B in [(20, 1, 55, 65),(30, 110, 155, 254), (100, 150, 255, 254), (0, 254, 254, 0)]:
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 25, "zoneId": 15}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(10)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            for i in range(32):
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightIpLeft{i}Brightness", [b])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightIpLeft{i}Red", [R])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightIpLeft{i}Green", [G])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightIpLeft{i}Blue", [B])
    
    @allure.title("智能氛围灯控制_右侧IP智能氛围灯--SALM4_MARS1")#MARS1有35个灯珠
    @pytest.mark.full
    def test_caseid_1984223(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.sd_tester.write_single_ccp(950, 1)
        for b, R, G, B in [(20, 1, 55, 65),(30, 110, 155, 254), (100, 150, 255, 254), (0, 254, 254, 0)]:
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 25, "zoneId": 16}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(10)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            for i in range(35):
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightIpRight{i}Brightness", [b])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightIpRight{i}Red", [R])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightIpRight{i}Green", [G])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightIpRight{i}Blue", [B])
    
    @allure.title("智能氛围灯控制_右侧IP智能氛围灯--SALM4_Venus")#Venus有31个灯珠
    @pytest.mark.sanity
    def test_caseid_1984224(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.sd_tester.write_single_ccp(950, 2)
        for b, R, G, B in [(20, 1, 55, 65),(30, 110, 155, 254), (100, 150, 255, 254), (0, 254, 254, 0)]:
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
                {"light": {"type": 25, "zoneId": 16}, "PixelData": [0], "type": 0, "color": [
                    {"brightness": b, "color": {"cRed": R, "cGreen": G, "cBlue": B}}]}]})
            sleep(10)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            for i in range(32):
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightIpRight{i}Brightness", [b])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightIpRight{i}Red", [R])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightIpRight{i}Green", [G])
                self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightIpRight{i}Blue", [B])
    
    @allure.title("智能氛围灯控制_其他信号发LastValue")
    @pytest.mark.full
    def test_caseid_1985851(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 25, "inhibitSts": True}]})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 25, "inhibitSts": False}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
            {"light": {"type": 25, "zoneId": 1}, "PixelData": [0], "type": 0, "color": [
                {"brightness": 1, "color": {"cRed": 2, "cGreen": 3, "cBlue": 4}}]}]})
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
            {"light": {"type": 25, "zoneId": 2}, "PixelData": [0], "type": 0, "color": [
                {"brightness": 40, "color": {"cRed": 100, "cGreen": 254, "cBlue": 255}}]}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        for i in range(35):
            self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightFrontRight{i}Brightness", [40])
            self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightFrontRight{i}Red", [100])
            self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightFrontRight{i}Green", [254])
            self.bgm_eth_inter.ck_signal_values(f"SmartAmbientLightFrontRight{i}Blue", [255])

    @allure.title("查询DRL/TI灯灯组状态&通知DRL/TI灯灯组状态_全部开/故障/关")
    @pytest.mark.sanity
    def test_caseid_111109(self):
        self.set_StsOfLEDFrnt_signal(2,2)
        self.partner.empty_all(1)
        self.set_StsOfLEDFrnt_signal(1,1)
        sleep(1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                        {"sts": {"light": {"type": 14, "zoneId": 1},
                                "sts": 1, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                        {"sts": {"light": {"type": 14, "zoneId": 2},
                                "sts": 1, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 14, "zoneId": 0}]},
                                            {"out": [{"light": {"type": 14, "zoneId": 1}, "sts": 1,
                                                    "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}},
                                                    {"light": {"type": 14, "zoneId": 2}, "sts": 1,
                                                    "brightness": 0,"color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.set_StsOfLEDFrnt_signal(2, 2)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                        {"sts": {"light": {"type": 14, "zoneId": 1},
                                "sts": 2, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                        {"sts": {"light": {"type": 14, "zoneId": 2},
                                "sts": 2, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 14, "zoneId": 0}]},
                                            {"out": [{"light": {"type": 14, "zoneId": 1}, "sts": 2,
                                                    "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}},
                                                    {"light": {"type": 14, "zoneId": 2}, "sts": 2,
                                                    "brightness": 0,"color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.set_StsOfLEDFrnt_signal(0, 0)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                        {"sts": {"light": {"type": 14, "zoneId": 1},
                                "sts": 0, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                        {"sts": {"light": {"type": 14, "zoneId": 2},
                                "sts": 0, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 14, "zoneId": 0}]},
                                            {"out": [{"light": {"type": 14, "zoneId": 1}, "sts": 0,
                                                    "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}},
                                                    {"light": {"type": 14, "zoneId": 2}, "sts": 0,
                                                        "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        
    @allure.title("查询DRL/TI灯灯组状态&通知DRL/TI灯灯组状态")
    @pytest.mark.sanity
    def test_caseid_1983893(self):
        self.set_StsOfLEDFrnt_signal(0, 0)
        # self.partner.empty_all(0.5)
        for Le2 in [1, 2, 3, 0]:
            self.partner.empty_all(0.1)
            self.set_StsOfLEDFrnt_signal(LampLe2=Le2)#左前
            if Le2 in [1, 2, 0]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 14, "zoneId": 1},
                                            "sts": Le2, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 14, "zoneId": 1}]},
                                                {"out": [{"light": {"type": 14, "zoneId": 1}, "sts": Le2, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})  
            else:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 14, "zoneId": 1}]},
                                            {"out": [{"light": {"type": 14, "zoneId": 1}, "sts": 2,
                                                    "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        for Ri2 in [1, 2, 3, 0]:
            self.partner.empty_all(0.1)
            self.set_StsOfLEDFrnt_signal(LampRi2=Ri2)#右前
            if Ri2 in [1, 2, 0]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 14, "zoneId": 2},
                                            "sts": Ri2, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 14, "zoneId": 2}]},
                                                {"out": [{"light": {"type": 14, "zoneId": 2}, "sts": Ri2, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            else:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 14, "zoneId": 2}]},
                                            {"out": [{"light": {"type": 14, "zoneId": 2}, "sts": 2,
                                                    "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
    
    @allure.title("查询DRL/TI灯灯组状态&通知DRL/TI灯灯组状态_默认值")
    @pytest.mark.full
    def test_caseid_1983894(self):
        for sts in [0, 1]:
            self.set_StsOfLEDFrnt_signal(sts, sts)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 14, "zoneId": 0}]},
                                                {"out":[{"light":{"type":14,"zoneId":1},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":14,"zoneId":2},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]}) 
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                            {"sts": {"light": {"type": 14, "zoneId": 1},
                                    "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                            {"sts": {"light": {"type": 14, "zoneId": 2},
                                    "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 14, "zoneId": 0}]},
                                                {"out": [{"light": {"type": 14, "zoneId": 1}, "sts": sts,
                                                        "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}},
                                                        {"light": {"type": 14, "zoneId": 2}, "sts": sts,
                                                        "brightness": 0,"color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.set_StsOfLEDFrnt_signal(0, 0)

    @allure.title("位置灯图案切换")
    @pytest.mark.sanity
    def test_caseid_111209(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 38, "zoneId": 0}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.ipdu.check(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr10, 'SetOfPosnLampScopeReq', 1, timeout=0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 38, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.ipdu.check(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr10, 'SetOfPosnLampScopeReq', 2, timeout=0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('SetOfPosnLampScopeReq', [1, 2])

    @allure.title("查询Pixel像素灯灯组状态&通知Pixel像素灯灯组状态_全部开关")
    @pytest.mark.sanity
    def test_caseid_111145(self):
        self.set_Pixel_signal(0, 0, 0, 0)
        self.partner.empty_all(0.5) 
        self.set_Pixel_signal(1, 1, 1, 1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 13, "zoneId": 1},
                                                                            "sts": 1, "brightness": 0,
                                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 13, "zoneId": 2},
                                                                            "sts": 1, "brightness": 0,
                                                                            "color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 13, "zoneId": 3},
                                                                            "sts": 1, "brightness": 0,
                                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 13, "zoneId": 4},
                                                                            "sts": 1, "brightness": 0,
                                                                            "color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 13, "zoneId": 0}]},
                                            {"out": [{"light": {"type": 13, "zoneId": 1}, "sts": 1,
                                                    "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}},
                                                    {"light": {"type": 13, "zoneId": 2}, "sts": 1,
                                                    "brightness": 0, "color": { "cRed": 0, "cGreen": 0, "cBlue": 0}},
                                                    {"light": {"type": 13, "zoneId": 3}, "sts": 1,
                                                    "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}},
                                                    {"light": {"type": 13, "zoneId": 4}, "sts": 1,
                                                    "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.set_Pixel_signal(0, 0, 0, 0)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 13, "zoneId": 1},
                                                                            "sts": 0, "brightness": 0,
                                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 13, "zoneId": 2},
                                                                            "sts": 0, "brightness": 0,
                                                                            "color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 13, "zoneId": 3},
                                                                            "sts": 0, "brightness": 0,
                                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 13, "zoneId": 4},
                                                                            "sts": 0, "brightness": 0,
                                                                            "color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 13, "zoneId": 0}]},
                                            {"out": [{"light": {"type": 13, "zoneId": 1}, "sts": 0,
                                                    "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}},
                                                    {"light": {"type": 13, "zoneId": 2}, "sts": 0,
                                                    "brightness": 0, "color": { "cRed": 0, "cGreen": 0, "cBlue": 0}},
                                                    {"light": {"type": 13, "zoneId": 3}, "sts": 0,
                                                    "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}},
                                                    {"light": {"type": 13, "zoneId": 4}, "sts": 0,
                                                    "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
    
    @allure.title("查询Pixel像素灯灯组状态&通知Pixel像素灯灯组状态")
    @pytest.mark.full
    def test_caseid_1983885(self):
        self.set_Pixel_signal(0, 0, 0, 0)
        self.partner.empty_all(0.5) 
        for Le in [1, 2, 3, 0]:
            self.set_Pixel_signal(Le1=Le)
            if Le in [3]:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 13, "zoneId": 1}]},
                                              {"out": [{"light": {"type": 13, "zoneId": 1}, "sts": 2,
                                                     "brightness": 0, "color": {"cRed": 0, "cGreen": 0,
                                                                                "cBlue": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 13, "zoneId": 1},
                                                                            "sts": Le, "brightness": 0,
                                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 13, "zoneId": 1}]},
                                              {"out": [{"light": {"type": 13, "zoneId": 1}, "sts": Le,
                                                     "brightness": 0, "color": {"cRed": 0, "cGreen": 0,
                                                                                "cBlue": 0}}]})
        for Ri1 in [1, 2, 3, 0]:
            self.set_Pixel_signal(Ri1=Ri1)
            if Ri1 in [3]:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 13, "zoneId": 2}]},
                                              {"out": [{"light": {"type": 13, "zoneId": 2}, "sts": 2,
                                                     "brightness": 0, "color": {"cRed": 0, "cGreen": 0,
                                                                                "cBlue": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 13, "zoneId": 2},
                                                                            "sts": Ri1, "brightness": 0,
                                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 13, "zoneId": 2}]},
                                              {"out": [{"light": {"type": 13, "zoneId": 2}, "sts": Ri1,
                                                     "brightness": 0, "color": {"cRed": 0, "cGreen": 0,
                                                                                "cBlue": 0}}]})
        for Le2 in [1, 2, 3, 0]:
            self.set_Pixel_signal(Le2=Le2)
            if Le2 in [3]:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 13, "zoneId": 3}]},
                                              {"out": [{"light": {"type": 13, "zoneId": 3}, "sts": 2,
                                                     "brightness": 0, "color": {"cRed": 0, "cGreen": 0,
                                                                                "cBlue": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 13, "zoneId": 3},
                                                                            "sts": Le2, "brightness": 0,
                                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 13, "zoneId": 3}]},
                                              {"out": [{"light": {"type": 13, "zoneId": 3}, "sts": Le2,
                                                     "brightness": 0, "color": {"cRed": 0, "cGreen": 0,
                                                                                "cBlue": 0}}]})
        for Ri2 in [1, 2, 3, 0]:
            self.set_Pixel_signal(Ri2=Ri2)
            if Ri2 in [3]:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 13, "zoneId": 4}]},
                                              {"out": [{"light": {"type": 13, "zoneId": 4}, "sts": 2,
                                                     "brightness": 0, "color": {"cRed": 0, "cGreen": 0,
                                                                                "cBlue": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 13, "zoneId": 4},
                                                                            "sts": Ri2, "brightness": 0,
                                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 13, "zoneId": 4}]},
                                              {"out": [{"light": {"type": 13, "zoneId": 4}, "sts": Ri2,
                                                     "brightness": 0, "color": {"cRed": 0, "cGreen": 0,
                                                                                "cBlue": 0}}]})
    
    @allure.title("查询Pixel像素灯灯组状态&通知Pixel像素灯灯组状态_默认值")
    @pytest.mark.full
    def test_caseid_1983886(self):
        for sts in [0, 1]:
            self.set_Pixel_signal(sts, sts, sts, sts)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 13, "zoneId": 0}]},
                                                {"out":[{"light":{"type":13,"zoneId":1},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":13,"zoneId":2},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":13,"zoneId":3},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":13,"zoneId":4},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]}) 
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 13, "zoneId": 1},
                                            "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 13, "zoneId": 2},
                                            "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 13, "zoneId": 3},
                                            "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 13, "zoneId": 4},
                                            "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 13, "zoneId": 0}]},
                                                {"out":[{"light":{"type":13,"zoneId":1},"sts":sts,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":13,"zoneId":2},"sts":sts,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":13,"zoneId":3},"sts":sts,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":13,"zoneId":4},"sts":sts,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})  
        self.set_Pixel_signal(0, 0, 0, 0)        

    @allure.title("查询AI状态&通知AI状态_左侧")
    @pytest.mark.sanity
    def test_caseid_111235(self):
        for LY1 in [1, 2, 3, 0]:
            self.ipdu.set(self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, 'StsOfLedLeftAIILY1', LY1)
            if LY1 in [1, 2, 0]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                    "sts": {"light": {"type": 34, "zoneId": 21}, "sts": LY1, "brightness": 0,
                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 34, "zoneId": 21}]},
                                                    {"out": [{"light": {"type": 34, "zoneId": 21}, "sts": LY1, "brightness": 0,
                                                                "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            else:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                        {"lights": [{"type": 34, "zoneId":21 }]},
                                            {"out":[{"light":{"type":34,"zoneId":21},"sts": 2,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})
        self.partner.empty_all(0.5)
        for LY2 in [1, 2, 3, 0]:
            self.ipdu.set(self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, 'StsOfLedLeftAIILY2', LY2)
            if LY2 in [1, 2, 0]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                    "sts": {"light": {"type": 34, "zoneId": 22}, "sts": LY2, "brightness": 0,
                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 34, "zoneId": 22}]},
                                                    {"out": [{"light": {"type": 34, "zoneId": 22}, "sts": LY2, "brightness": 0,
                                                                "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            else:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                        {"lights": [{"type": 34, "zoneId":22}]},
                                            {"out":[{"light":{"type":34,"zoneId":22},"sts": 2,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})
        self.partner.empty_all(0.5)
        for LY3 in [1, 2, 3, 0]:
            self.ipdu.set(self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, 'StsOfLedLeftAIILY3', LY3)
            if LY3 in [1, 2, 0]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                    "sts": {"light": {"type": 34, "zoneId": 23}, "sts": LY3, "brightness": 0,
                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 34, "zoneId": 23}]},
                                                    {"out": [{"light": {"type": 34, "zoneId": 23}, "sts": LY3, "brightness": 0,
                                                                "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            else:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                        {"lights": [{"type": 34, "zoneId":23}]},
                                            {"out":[{"light":{"type":34,"zoneId":23},"sts": 2,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})
        self.partner.empty_all(0.5)
        for LY4 in [1, 2, 3, 0]:
            self.ipdu.set(self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, 'StsOfLedLeftAIILY4', LY4)
            if LY4 in [1, 2, 0]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                    "sts": {"light": {"type": 34, "zoneId": 24}, "sts": LY4, "brightness": 0,
                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 34, "zoneId": 24}]},
                                                    {"out": [{"light": {"type": 34, "zoneId": 24}, "sts": LY4, "brightness": 0,
                                                                "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            else:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                        {"lights": [{"type": 34, "zoneId":24}]},
                                            {"out":[{"light":{"type":34,"zoneId":24},"sts": 2,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})
                
    @allure.title("查询AI状态&通知AI状态_右侧")
    @pytest.mark.sanity
    def test_caseid_1984719(self):
        for LY1 in [1, 2, 3, 0]:
            self.ipdu.set(self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, 'StsOfLedRightAIILY1', LY1)
            sleep(0.5)
            if LY1 in [1, 2, 0]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                    "sts": {"light": {"type": 34, "zoneId": 25}, "sts": LY1, "brightness": 0,
                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 34, "zoneId": 25}]},
                                                    {"out": [{"light": {"type": 34, "zoneId": 25}, "sts": LY1, "brightness": 0,
                                                                "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            else:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                        {"lights": [{"type": 34, "zoneId":25}]},
                                            {"out":[{"light":{"type":34,"zoneId":25},"sts": 2,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})
        self.partner.empty_all(0.5)
        for LY2 in [1, 2, 3, 0]:
            self.ipdu.set(self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, 'StsOfLedRightAIILY2', LY2)
            if LY2 in [1, 2, 0]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                    "sts": {"light": {"type": 34, "zoneId": 26}, "sts": LY2, "brightness": 0,
                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 34, "zoneId": 26}]},
                                                    {"out": [{"light": {"type": 34, "zoneId": 26}, "sts": LY2, "brightness": 0,
                                                                "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            else:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                        {"lights": [{"type": 34, "zoneId":26}]},
                                            {"out":[{"light":{"type":34,"zoneId":26},"sts": 2,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})
        for LY3 in [1, 2, 3, 0]:
            self.ipdu.set(self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, 'StsOfLedRightAIILY3', LY3)
            if LY3 in [1, 2, 0]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                    "sts": {"light": {"type": 34, "zoneId": 27}, "sts": LY3, "brightness": 0,
                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 34, "zoneId": 27}]},
                                                    {"out": [{"light": {"type": 34, "zoneId": 27}, "sts": LY3, "brightness": 0,
                                                                "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            else:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                        {"lights": [{"type": 34, "zoneId":27}]},
                                            {"out":[{"light":{"type":34,"zoneId":27},"sts": 2,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})
        for LY4 in [1, 2, 3, 0]:
            self.ipdu.set(self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, 'StsOfLedRightAIILY4', LY4)
            if LY4 in [1, 2, 0]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                    "sts": {"light": {"type": 34, "zoneId": 28}, "sts": LY4, "brightness": 0,
                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 34, "zoneId": 28}]},
                                                    {"out": [{"light": {"type": 34, "zoneId": 28}, "sts": LY4, "brightness": 0,
                                                                "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            else:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                        {"lights": [{"type": 34, "zoneId":28}]},
                                            {"out":[{"light":{"type":34,"zoneId":28},"sts": 2,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})
    
    @allure.title("查询AI状态&通知AI状态_左侧默认值")
    @pytest.mark.full
    def test_caseid_1984724(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        for LY1 in [1, 0]:
            self.ipdu.set(self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, 'StsOfLedLeftAIILY1', LY1)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",{"lights": [{"type": 34, "zoneId": 21}]}, 
                                                        {"out": [{"light": {"type": 34, "zoneId": 21}, "sts": 0, 
                                                                    "brightness": 0,"color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", 
                                      {"sts": {"light": {"type": 34, "zoneId": 21}, 
                                               "sts": LY1, "brightness": 0,"color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}}, timeout=3)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 34, "zoneId": 21}]},
                                                    {"out": [{"light": {"type": 34, "zoneId": 21}, "sts": LY1, "brightness": 0,
                                                                "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        for LY2 in [1, 0]:
            self.ipdu.set(self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, 'StsOfLedLeftAIILY2', LY2)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",{"lights": [{"type": 34, "zoneId": 22}]}, 
                                                        {"out": [{"light": {"type": 34, "zoneId": 22}, "sts": 0, 
                                                                    "brightness": 0,"color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                "sts": {"light": {"type": 34, "zoneId": 22}, "sts": LY2, "brightness": 0,
                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}}, timeout=3)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 34, "zoneId": 22}]},
                                                {"out": [{"light": {"type": 34, "zoneId": 22}, "sts": LY2, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        for LY3 in [1, 0]:
            self.ipdu.set(self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, 'StsOfLedLeftAIILY3', LY3)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",{"lights": [{"type": 34, "zoneId": 23}]}, 
                                                        {"out": [{"light": {"type": 34, "zoneId": 23}, "sts": 0, 
                                                                    "brightness": 0,"color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                "sts": {"light": {"type": 34, "zoneId": 23}, "sts": LY3, "brightness": 0,
                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}}, timeout=3)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 34, "zoneId": 23}]},
                                                {"out": [{"light": {"type": 34, "zoneId": 23}, "sts": LY3, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            
        for LY4 in [1, 0]:
            self.ipdu.set(self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, 'StsOfLedLeftAIILY4', LY4)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",{"lights": [{"type": 34, "zoneId": 24}]}, 
                                                        {"out": [{"light": {"type": 34, "zoneId": 24}, "sts": 0, 
                                                                    "brightness": 0,"color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                "sts": {"light": {"type": 34, "zoneId": 24}, "sts": LY4, "brightness": 0,
                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}}, timeout=3)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 34, "zoneId": 24}]},
                                                {"out": [{"light": {"type": 34, "zoneId": 24}, "sts": LY4, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
    @allure.title("查询AI状态&通知AI状态_右侧默认值")
    @pytest.mark.full
    def test_caseid_1984725(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        for LY1 in [1, 0]:
            self.ipdu.set(self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, 'StsOfLedRightAIILY1', LY1)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",{"lights": [{"type": 34, "zoneId": 25}]}, 
                                                        {"out": [{"light": {"type": 34, "zoneId": 25}, "sts": 0, 
                                                                    "brightness": 0,"color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                "sts": {"light": {"type": 34, "zoneId": 25}, "sts": LY1, "brightness": 0,
                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 34, "zoneId": 25}]},
                                                {"out": [{"light": {"type": 34, "zoneId": 25}, "sts": LY1, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        for LY2 in [1, 0]:
            self.ipdu.set(self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, 'StsOfLedRightAIILY2', LY2)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",{"lights": [{"type": 34, "zoneId": 26}]}, 
                                                        {"out": [{"light": {"type": 34, "zoneId": 26}, "sts": 0, 
                                                                    "brightness": 0,"color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                "sts": {"light": {"type": 34, "zoneId": 26}, "sts": LY2, "brightness": 0,
                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}}, timeout=3)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 34, "zoneId": 26}]},
                                                {"out": [{"light": {"type": 34, "zoneId": 26}, "sts": LY2, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        for LY3 in [1, 0]:
            self.ipdu.set(self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, 'StsOfLedRightAIILY3', LY3)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",{"lights": [{"type": 34, "zoneId": 27}]}, 
                                                        {"out": [{"light": {"type": 34, "zoneId": 27}, "sts": 0, 
                                                                    "brightness": 0,"color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                "sts": {"light": {"type": 34, "zoneId": 27}, "sts": LY3, "brightness": 0,
                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}}, timeout=3)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 34, "zoneId": 27}]},
                                                {"out": [{"light": {"type": 34, "zoneId": 27}, "sts": LY3, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        for LY4 in [1, 0]:
            self.ipdu.set(self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, 'StsOfLedRightAIILY4', LY4)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",{"lights": [{"type": 34, "zoneId": 28}]}, 
                                                        {"out": [{"light": {"type": 34, "zoneId": 28}, "sts": 0, 
                                                                    "brightness": 0,"color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                "sts": {"light": {"type": 34, "zoneId": 28}, "sts": LY4, "brightness": 0,
                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}}, timeout=3)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 34, "zoneId": 28}]},
                                                {"out": [{"light": {"type": 34, "zoneId": 28}, "sts": LY4, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})   
        
    @allure.title("查询一字眉灯灯组状态&通知一字眉灯灯组状态_全部开关")
    @pytest.mark.sanity
    def test_caseid_111222(self):
        self.set_EDF_signal(0, 0, 0, 0)
        self.partner.empty_all(0.5) 
        self.set_EDF_signal(1, 1, 1, 1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 39, "zoneId": 9},
                                                                   "sts": 1, "brightness": 0,
                                                                   "color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 39, "zoneId": 3},
                                                                       "sts": 1, "brightness": 0,
                                                                       "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 39, "zoneId": 4},
                                                                       "sts": 1, "brightness": 0,
                                                                       "color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 39, "zoneId": 5},
                                                                       "sts": 1, "brightness": 0,
                                                                       "color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                            {"lights": [{"type": 39, "zoneId": 0}]},
                                            {"out":[{"light":{"type":39,"zoneId":9},"sts":1,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                    {"light":{"type":39,"zoneId":3},"sts":1,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                    {"light":{"type":39,"zoneId":4},"sts":1,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                    {"light":{"type":39,"zoneId":5},"sts":1,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]}) 
        self.set_EDF_signal(2, 2, 2, 2)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 39, "zoneId": 9},
                                                                   "sts": 2, "brightness": 0,
                                                                   "color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 39, "zoneId": 3},
                                                                       "sts": 2, "brightness": 0,
                                                                       "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 39, "zoneId": 4},
                                                                       "sts": 2, "brightness": 0,
                                                                       "color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 39, "zoneId": 5},
                                                                       "sts": 2, "brightness": 0,
                                                                       "color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                            {"lights": [{"type": 39, "zoneId": 0}]},
                                            {"out":[{"light":{"type":39,"zoneId":9},"sts":2,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                    {"light":{"type":39,"zoneId":3},"sts":2,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                    {"light":{"type":39,"zoneId":4},"sts":2,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                    {"light":{"type":39,"zoneId":5},"sts":2,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]}) 
        self.set_EDF_signal(0, 0, 0, 0)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 39, "zoneId": 9},
                                                                   "sts": 0, "brightness": 0,
                                                                   "color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 39, "zoneId": 3},
                                                                       "sts": 0, "brightness": 0,
                                                                       "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 39, "zoneId": 4},
                                                                       "sts": 0, "brightness": 0,
                                                                       "color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 39, "zoneId": 5},
                                                                       "sts": 0, "brightness": 0,
                                                                       "color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                            {"lights": [{"type": 39, "zoneId": 0}]},
                                            {"out":[{"light":{"type":39,"zoneId":9},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                    {"light":{"type":39,"zoneId":3},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                    {"light":{"type":39,"zoneId":4},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                    {"light":{"type":39,"zoneId":5},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]}) 
    
    @allure.title("查询一字眉灯灯组状态&通知一字眉灯灯组状态")
    @pytest.mark.sanity
    def test_caseid_1983888(self):
        self.set_EDF_signal(0, 0, 0, 0)
        self.partner.empty_all(0.5) 
        for Frnt in [1, 2, 3, 0]:
            self.set_EDF_signal(FrntLampMid1=Frnt)
            if Frnt in [3]:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 39, "zoneId": 9}]},
                                              {"out": [{"light": {"type": 39, "zoneId": 9}, "sts": 2,
                                                     "brightness": 0, "color": {"cRed": 0, "cGreen": 0,
                                                                                "cBlue": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 39, "zoneId": 9},
                                                                            "sts": Frnt, "brightness": 0,
                                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 39, "zoneId": 9}]},
                                              {"out": [{"light": {"type": 39, "zoneId": 9}, "sts": Frnt,
                                                     "brightness": 0, "color": {"cRed": 0, "cGreen": 0,
                                                                                "cBlue": 0}}]})
        for Le1 in [1, 2, 3, 0]:
            self.set_EDF_signal(ReLampLe1=Le1)
            if Le1 in [3]:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 39, "zoneId": 3}]},
                                              {"out": [{"light": {"type": 39, "zoneId": 3}, "sts": 2,
                                                     "brightness": 0, "color": {"cRed": 0, "cGreen": 0,
                                                                                "cBlue": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 39, "zoneId": 3},
                                                                            "sts": Le1, "brightness": 0,
                                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 39, "zoneId": 3}]},
                                              {"out": [{"light": {"type": 39, "zoneId": 3}, "sts": Le1,
                                                     "brightness": 0, "color": {"cRed": 0, "cGreen": 0,
                                                                                "cBlue": 0}}]})
        for Ri1 in [1, 2, 3, 0]:
            self.set_EDF_signal(ReLampRi1=Ri1)
            if Ri1 in [3]:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 39, "zoneId": 4}]},
                                              {"out": [{"light": {"type": 39, "zoneId": 4}, "sts": 2,
                                                     "brightness": 0, "color": {"cRed": 0, "cGreen": 0,
                                                                                "cBlue": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 39, "zoneId": 4},
                                                                            "sts": Ri1, "brightness": 0,
                                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 39, "zoneId": 4}]},
                                              {"out": [{"light": {"type": 39, "zoneId": 4}, "sts": Ri1,
                                                     "brightness": 0, "color": {"cRed": 0, "cGreen": 0,
                                                                                "cBlue": 0}}]})
        for Mid1 in [1, 2, 3, 0]:
            self.set_EDF_signal(ReLampMid1=Mid1)
            if Mid1 in [3]:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 39, "zoneId": 5}]},
                                              {"out": [{"light": {"type": 39, "zoneId": 5}, "sts": 2,
                                                     "brightness": 0, "color": {"cRed": 0, "cGreen": 0,
                                                                                "cBlue": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 39, "zoneId": 5},
                                                                            "sts": Mid1, "brightness": 0,
                                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 39, "zoneId": 5}]},
                                              {"out": [{"light": {"type": 39, "zoneId": 5}, "sts": Mid1,
                                                     "brightness": 0, "color": {"cRed": 0, "cGreen": 0,
                                                                                "cBlue": 0}}]})
    
    @allure.title("查询一字眉灯灯组状态&通知一字眉灯灯组状态_默认值")
    @pytest.mark.full
    def test_caseid_1983891(self):
        for sts in [0, 1]:
            self.set_EDF_signal(sts, sts, sts, sts)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 39, "zoneId": 0}]},
                                                {"out":[{"light":{"type":39,"zoneId":9},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":39,"zoneId":3},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":39,"zoneId":4},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":39,"zoneId":5},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]}, timeout=0.5) 
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 39, "zoneId": 9},
                                                                    "sts": sts, "brightness": 0,
                                                                    "color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}})
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 39, "zoneId": 3},
                                                                        "sts": sts, "brightness": 0,
                                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 39, "zoneId": 4},
                                                                        "sts": sts, "brightness": 0,
                                                                        "color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}})
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 39, "zoneId": 5},
                                                                        "sts": sts, "brightness": 0,
                                                                        "color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 39, "zoneId": 0}]},
                                                {"out":[{"light":{"type":39,"zoneId":9},"sts":sts,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":39,"zoneId":3},"sts":sts,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":39,"zoneId":4},"sts":sts,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":39,"zoneId":5},"sts":sts,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]}, timeout=0.5) 
        self.set_EDF_signal(0, 0, 0, 0)

    @allure.title("阅读灯开关控制_左前阅读灯开")
    @pytest.mark.smoke
    def test_caseid_111107(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 1}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]}, timeout=0.2)
        # self.ipdu.set(self.ipdu.cem_lin3.CemCem_Lin3Fr03, 'ReadLiOpenReqFrontLeft', 1)
        self.ipdu.check(self.ipdu.cem_lin3.CemCem_Lin3Fr03, 'ReadLiOpenReqFrontLeft', 1, timeout=0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('ReadLiOpenReqFrontLeft', [1, 1, 1, 0])
        self.bgm_eth_inter.ck_period_time('ReadLiOpenReqFrontLeft', 0.16, permit_fail_times=1)

    @allure.title("阅读灯开关控制_左前阅读灯关") 
    @pytest.mark.full
    def test_caseid_111111(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 1}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        # self.ipdu.set(self.ipdu.cem_lin3.CemCem_Lin3Fr03, 'ReadLiOpenReqFrontLeft', 0)
        self.ipdu.check(self.ipdu.cem_lin3.CemCem_Lin3Fr03, 'ReadLiOpenReqFrontLeft', 2, timeout=0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('ReadLiOpenReqFrontLeft', [2, 2, 2, 0])
        self.bgm_eth_inter.ck_period_time('ReadLiOpenReqFrontLeft', 0.16, permit_fail_times=1)
        
    @allure.title("阅读灯开关控制_左前打断逻辑")  
    @pytest.mark.full
    def test_caseid_1918547(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 1}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        sleep(0.1)  # 相同忽略
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 1}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        sleep(0.1)  # 设置值不同打断
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 1}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 1}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array('ReadLiOpenReqFrontLeft', [1, 2, 0])
        self.bgm_eth_inter.ck_ordered_array('ReadLiOpenReqFrontRight', [0])
        self.bgm_eth_inter.ck_ordered_array('ReadLiOpenReqSecondRowLeft', [0])
        self.bgm_eth_inter.ck_ordered_array('ReadLiOpenReqSecondRowRight', [0])

    @allure.title("阅读灯开关控制_右前阅读灯开") 
    @pytest.mark.sanity
    def test_caseid_1983180(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 2}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        # self.ipdu.set(self.ipdu.cem_lin3.CemCem_Lin3Fr03, 'ReadLiOpenReqFrontRight', 1)
        self.ipdu.check(self.ipdu.cem_lin3.CemCem_Lin3Fr03, 'ReadLiOpenReqFrontRight', 1, timeout=0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('ReadLiOpenReqFrontRight', [1, 1, 1, 0])
        self.bgm_eth_inter.ck_period_time('ReadLiOpenReqFrontRight', 0.16, permit_fail_times=1)

    @allure.title("阅读灯开关控制_右前阅读灯关") 
    @pytest.mark.full
    def test_caseid_1983181(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 2}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        # self.ipdu.set(self.ipdu.cem_lin3.CemCem_Lin3Fr03, 'ReadLiOpenReqFrontRight', 0)
        self.ipdu.check(self.ipdu.cem_lin3.CemCem_Lin3Fr03, 'ReadLiOpenReqFrontRight', 2, timeout=0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('ReadLiOpenReqFrontRight', [2, 2, 2, 0])
        self.bgm_eth_inter.ck_period_time('ReadLiOpenReqFrontRight', 0.16, permit_fail_times=1)

    @allure.title("阅读灯开关控制_右前打断逻辑")
    @pytest.mark.full
    def test_caseid_1983182(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 2}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        sleep(0.1)  # 相同忽略
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 2}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        sleep(0.1)  # 设置值不同打断
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 2}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 2}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array('ReadLiOpenReqFrontLeft', [0])
        self.bgm_eth_inter.ck_ordered_array('ReadLiOpenReqFrontRight', [1, 2, 0])
        self.bgm_eth_inter.ck_ordered_array('ReadLiOpenReqSecondRowLeft', [0])
        self.bgm_eth_inter.ck_ordered_array('ReadLiOpenReqSecondRowRight', [0])

    @allure.title("阅读灯开关控制_左后阅读灯开")
    @pytest.mark.sanity
    def test_caseid_1983183(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 3}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        # self.ipdu.set(self.ipdu.cem_lin3.CemCem_Lin3Fr03, 'ReadLiOpenReqSecondRowLeft', 1)
        self.ipdu.check(self.ipdu.cem_lin3.CemCem_Lin3Fr03, 'ReadLiOpenReqSecondRowLeft', 1, timeout=0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('ReadLiOpenReqSecondRowLeft', [1, 1, 1, 0])
        self.bgm_eth_inter.ck_period_time('ReadLiOpenReqSecondRowLeft', 0.16, permit_fail_times=1)

    @allure.title("阅读灯开关控制_左后阅读灯关")
    @pytest.mark.full
    def test_caseid_1983184(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 3}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        # self.ipdu.set(self.ipdu.cem_lin3.CemCem_Lin3Fr03, 'ReadLiOpenReqSecondRowLeft', 0)
        self.ipdu.check(self.ipdu.cem_lin3.CemCem_Lin3Fr03, 'ReadLiOpenReqSecondRowLeft', 2, timeout=0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('ReadLiOpenReqSecondRowLeft', [2, 2, 2, 0])
        self.bgm_eth_inter.ck_period_time('ReadLiOpenReqSecondRowLeft', 0.16, permit_fail_times=1)

    @allure.title("阅读灯开关控制_左后打断逻辑")
    @pytest.mark.full
    def test_caseid_1983189(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 3}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        sleep(0.1)  # 相同忽略
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 3}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        sleep(0.1)  # 设置值不同打断
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 3}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 3}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array('ReadLiOpenReqFrontLeft', [0])
        self.bgm_eth_inter.ck_ordered_array('ReadLiOpenReqFrontRight', [0])
        self.bgm_eth_inter.ck_ordered_array('ReadLiOpenReqSecondRowLeft', [1, 2, 0])
        self.bgm_eth_inter.ck_ordered_array('ReadLiOpenReqSecondRowRight', [0])

    @allure.title("阅读灯开关控制_右后阅读灯开")
    @pytest.mark.sanity
    def test_caseid_1983191(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 4}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        # self.ipdu.set(self.ipdu.cem_lin3.CemCem_Lin3Fr03, 'ReadLiOpenReqSecondRowRight', 1)
        self.ipdu.check(self.ipdu.cem_lin3.CemCem_Lin3Fr03, 'ReadLiOpenReqSecondRowRight', 1, timeout=0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('ReadLiOpenReqSecondRowRight', [1, 1, 1, 0])
        self.bgm_eth_inter.ck_period_time('ReadLiOpenReqSecondRowRight', 0.16, permit_fail_times=1)

    @allure.title("阅读灯开关控制_右后阅读灯关")
    @pytest.mark.full
    def test_caseid_1983192(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 4}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        # self.ipdu.set(self.ipdu.cem_lin3.CemCem_Lin3Fr03, 'ReadLiOpenReqSecondRowRight', 0)
        self.ipdu.check(self.ipdu.cem_lin3.CemCem_Lin3Fr03, 'ReadLiOpenReqSecondRowRight', 2, timeout=0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('ReadLiOpenReqSecondRowRight', [2, 2, 2, 0])
        self.bgm_eth_inter.ck_period_time('ReadLiOpenReqSecondRowRight', 0.16, permit_fail_times=1)

    @allure.title("阅读灯开关控制_右后打断逻辑")
    @pytest.mark.full
    def test_caseid_1983193(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 4}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        sleep(0.1)  # 相同忽略
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 4}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        sleep(0.1)  # 设置值不同打断
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 4}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 4}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array('ReadLiOpenReqFrontLeft', [0])
        self.bgm_eth_inter.ck_ordered_array('ReadLiOpenReqFrontRight', [0])
        self.bgm_eth_inter.ck_ordered_array('ReadLiOpenReqSecondRowLeft', [0])
        self.bgm_eth_inter.ck_ordered_array('ReadLiOpenReqSecondRowRight', [1, 2, 0])


    def light_control(self, light_type, zoneid=0, bright=0):
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
                    {"light": {"type": light_type, "zoneId": zoneid}, "mode": 0, "brightness": bright,
                     "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]}, timeout=0.2)
        
    # 照脚灯
    @allure.title("照脚灯控制_brightness为0")
    @pytest.mark.sanity
    def test_caseid_1988970(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.light_control(Light.Foot, bright=0)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_signal_values('FootwellLampSRVReq', [0, 0, 0])
        self.bgm_eth_inter.ck_period_time('FootwellLampSRVReq', 0.1, permit_fail_times=1)

    @allure.title("照脚灯控制_brightness为100")
    @pytest.mark.sanity
    def test_caseid_1988971(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.light_control(Light.Foot, bright=100)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_signal_values('FootwellLampSRVReq', [1, 1, 1])
        self.bgm_eth_inter.ck_period_time('FootwellLampSRVReq', 0.1, permit_fail_times=1)

    @allure.title("照脚灯控制_brightness为非法值")
    @pytest.mark.full
    def test_caseid_1988972(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.light_control(Light.Foot, bright=50)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_signal_values('FootwellLampSRVReq', [])

    @allure.title("照脚灯控制_重启场景")
    @pytest.mark.full
    def test_caseid_1988973(self):
        self.light_control(Light.Foot, bright=100)
        self.partner.empty_all(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.kill_s2s_and_reconnect_service(LIGHT_SERVICE_CLIENT)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('FootwellLampSRVReq', [])

    @allure.title("照脚灯控制_brightness值不同_会打断")
    @pytest.mark.full
    def test_caseid_1988974(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.light_control(Light.Foot, bright=0)
        sleep(0.05)
        self.light_control(Light.Foot, bright=100)
        sleep(0.05)
        self.light_control(Light.Foot, bright=0)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_signal_values('FootwellLampSRVReq', [0, 1, 0, 0, 0])

    @allure.title("照脚灯控制_brightness值相同_不会响应")
    @pytest.mark.full
    def test_caseid_1988975(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.light_control(Light.Foot, bright=100)
        sleep(0.05)
        self.light_control(Light.Foot, bright=100)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_signal_values('FootwellLampSRVReq', [1, 1, 1])

    # ADS灯
    @allure.title("ADS灯控制_分别设置前后左右灯")
    @pytest.mark.sanity
    def test_caseid_1989374(self):
        self.sd_tester.write_single_ccp(950, 2)
        sleep(1)
        for bright in [0, 50, 100]:
            logger.info(f"Front bright:{bright}")
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.light_control(Light.LightADS, zoneid=ZoneID.Front, bright=bright)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
            self.bgm_eth_inter.ck_signal_values('WheelLampFrntRi', [bright, bright, bright])
            self.bgm_eth_inter.ck_signal_values('WheelLampFrntLe', [0, 0, 0])
            self.bgm_eth_inter.ck_signal_values('WheelLampRearLe', [0, 0, 0])
            self.bgm_eth_inter.ck_signal_values('WheelLampRearRi', [0, 0, 0])
            self.bgm_eth_inter.ck_period_time('WheelLampFrntRi', 0.1, permit_fail_times=1)
            
        for bright in [0, 50, 100]:
            logger.info(f"Left bright:{bright}")
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.light_control(Light.LightADS, zoneid=ZoneID.Left, bright=bright)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
            self.bgm_eth_inter.ck_signal_values('WheelLampFrntRi', [100, 100, 100])
            self.bgm_eth_inter.ck_signal_values('WheelLampFrntLe', [bright, bright, bright])
            self.bgm_eth_inter.ck_signal_values('WheelLampRearLe', [0, 0, 0])
            self.bgm_eth_inter.ck_signal_values('WheelLampRearRi', [0, 0, 0])
            self.bgm_eth_inter.ck_period_time('WheelLampFrntLe', 0.1, permit_fail_times=1)

        for bright in [0, 50, 100]:
            logger.info(f"Rear bright:{bright}")
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.light_control(Light.LightADS, zoneid=ZoneID.Rear, bright=bright)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
            self.bgm_eth_inter.ck_signal_values('WheelLampFrntRi', [100, 100, 100])
            self.bgm_eth_inter.ck_signal_values('WheelLampFrntLe', [100, 100, 100])
            self.bgm_eth_inter.ck_signal_values('WheelLampRearLe', [bright, bright, bright])
            self.bgm_eth_inter.ck_signal_values('WheelLampRearRi', [0, 0, 0])
            self.bgm_eth_inter.ck_period_time('WheelLampRearLe', 0.1, permit_fail_times=1)

        for bright in [0, 50, 100]:
            logger.info(f"Right bright:{bright}")
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.light_control(Light.LightADS, zoneid=ZoneID.Right, bright=bright)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
            self.bgm_eth_inter.ck_signal_values('WheelLampFrntRi', [100, 100, 100])
            self.bgm_eth_inter.ck_signal_values('WheelLampFrntLe', [100, 100, 100])
            self.bgm_eth_inter.ck_signal_values('WheelLampRearLe', [100, 100, 100])
            self.bgm_eth_inter.ck_signal_values('WheelLampRearRi', [bright, bright, bright])
            self.bgm_eth_inter.ck_period_time('WheelLampRearRi', 0.1, permit_fail_times=1)
        
    @allure.title("ADS灯控制_同时设置前后左右灯")
    @pytest.mark.sanity
    def test_caseid_1989378(self):
        self.sd_tester.write_single_ccp(950, 2)
        sleep(1)
        for bright in [0, 50, 100]:
            logger.info(f"bright:{bright}")
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.light_control(Light.LightADS, zoneid=ZoneID.AllOrSingle, bright=bright)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
            self.bgm_eth_inter.ck_signal_values('WheelLampFrntLe', [bright, bright, bright])
            self.bgm_eth_inter.ck_signal_values('WheelLampFrntRi', [bright, bright, bright])
            self.bgm_eth_inter.ck_signal_values('WheelLampRearLe', [bright, bright, bright])
            self.bgm_eth_inter.ck_signal_values('WheelLampRearRi', [bright, bright, bright])
            self.bgm_eth_inter.ck_period_time('WheelLampFrntLe', 0.1, permit_fail_times=1)
        
    @allure.title("ADS灯控制_brightness为非法值")
    @pytest.mark.sanity
    def test_caseid_1989379(self):
        self.sd_tester.write_single_ccp(950, 2)
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.light_control(Light.LightADS, zoneid=ZoneID.AllOrSingle, bright=101)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_signal_values('WheelLampFrntLe', [])
        self.bgm_eth_inter.ck_signal_values('WheelLampFrntRi', [])
        self.bgm_eth_inter.ck_signal_values('WheelLampRearLe', [])
        self.bgm_eth_inter.ck_signal_values('WheelLampRearRi', [])

    @allure.title("ADS灯控制_重启场景")
    @pytest.mark.full
    def test_caseid_1989380(self):
        self.sd_tester.write_single_ccp(950, 2)
        sleep(1)
        self.light_control(Light.LightADS, zoneid=ZoneID.AllOrSingle, bright=100)
        self.partner.empty_all(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.kill_s2s_and_reconnect_service(LIGHT_SERVICE_CLIENT)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('WheelLampFrntLe', [])
        self.bgm_eth_inter.ck_signal_values('WheelLampFrntRi', [])
        self.bgm_eth_inter.ck_signal_values('WheelLampRearLe', [])
        self.bgm_eth_inter.ck_signal_values('WheelLampRearRi', [])
        
    @allure.title("ADS灯控制_brightness不同值打断")
    @pytest.mark.full
    def test_caseid_1989381(self):
        self.sd_tester.write_single_ccp(950, 2)
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.light_control(Light.LightADS, zoneid=ZoneID.AllOrSingle, bright=10)
        sleep(0.05)
        self.light_control(Light.LightADS, zoneid=ZoneID.AllOrSingle, bright=90)
        sleep(0.05)
        self.light_control(Light.LightADS, zoneid=ZoneID.Front, bright=30)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_signal_values('WheelLampFrntLe', [10, 90, 90, 90, 90])
        self.bgm_eth_inter.ck_signal_values('WheelLampFrntRi', [10, 90, 30, 30, 30])
        self.bgm_eth_inter.ck_signal_values('WheelLampRearLe', [10, 90, 90, 90, 90])
        self.bgm_eth_inter.ck_signal_values('WheelLampRearRi', [10, 90, 90, 90, 90])
        
    @allure.title("ADS灯控制_brightness相同值打断")
    @pytest.mark.full
    def test_caseid_1989382(self):
        self.sd_tester.write_single_ccp(950, 2)
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.light_control(Light.LightADS, zoneid=ZoneID.AllOrSingle, bright=10)
        sleep(0.05)
        self.light_control(Light.LightADS, zoneid=ZoneID.AllOrSingle, bright=10)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_signal_values('WheelLampFrntLe', [10, 10, 10, 10])
        self.bgm_eth_inter.ck_signal_values('WheelLampFrntRi', [10, 10, 10, 10])
        self.bgm_eth_inter.ck_signal_values('WheelLampRearLe', [10, 10, 10, 10])
        self.bgm_eth_inter.ck_signal_values('WheelLampRearRi', [10, 10, 10, 10])
             
    
    @allure.title("礼貌灯(内灯)控制&获取内灯模式（礼貌灯）&通知内灯模式（礼貌灯）")  # mode = @value(0)
    @pytest.mark.smoke
    def test_caseid_111093(self):
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.empty_all(1)
        self.dk.set_cenlock_sts(1)#LockgCenStsLockSt不为2|3(解锁成功)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2})#LockgCenStsTrigSrc=3
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "InternalLightMode", {"sts": 0})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 0})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [0, 0, 0])
        self.bgm_eth_inter.ck_period_time('IntrLampSelnMod', 0.1)

    @allure.title("礼貌灯(内灯)控制&获取内灯模式（礼貌灯）&通知内灯模式（礼貌灯）")  # mode = @value(1)
    @pytest.mark.sanity
    def test_caseid_111182(self):
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.empty_all(1)
        self.dk.set_cenlock_sts(1)#LockgCenStsLockSt不为2|3(解锁成功)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2})#LockgCenStsTrigSrc=3
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "InternalLightMode", {"sts": 1})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 1})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [1, 1, 1])
        self.bgm_eth_inter.ck_period_time('IntrLampSelnMod', 0.1)

    @allure.title("礼貌灯(内灯)控制&获取内灯模式（礼貌灯）&通知内灯模式（礼貌灯）")  # mode = @value(2)
    @pytest.mark.full
    def test_caseid_1982937(self):
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.empty_all(1)
        self.dk.set_cenlock_sts(1)#LockgCenStsLockSt不为2|3(解锁成功)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2})#LockgCenStsTrigSrc=3
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 2, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "InternalLightMode", {"sts": 2})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 2})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [2, 2, 2])
        self.bgm_eth_inter.ck_period_time('IntrLampSelnMod', 0.1)
    
    @allure.title("礼貌灯(内灯)控制&获取内灯模式(礼貌灯)_不响应接口调用(解闭锁成功触发源_1_RKE闭锁成功)")  #LockgCenStsLockSt=3
    @pytest.mark.full
    def test_caseid_4rr(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.empty_all(1)
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.dk.send_rke_lock()
        info1 = {"sts": 3, "triggerId": 1, "updateEve": True}
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info1})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 2, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 0})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [])
    
    @allure.title("礼貌灯(内灯)控制&获取内灯模式(礼貌灯)_不响应接口调用(解闭锁成功触发源_2_PE长按闭锁成功)")  #LockgCenStsLockSt=3
    @pytest.mark.full
    def test_caseid_b(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.empty_all(1)
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.press_door_outswitch(4, 2.2)
        info1 = {"sts": 3, "triggerId": 2, "updateEve": True}
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info1})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 2, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 0})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [])
    
    @allure.title("礼貌灯(内灯)控制&获取内灯模式(礼貌灯)_(解闭锁成功触发源_3_车内按钮闭锁成功)")  #LockgCenStsLockSt=3
    @pytest.mark.full
    def test_caseid_c(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.empty_all(1)
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2})
        info1 = {"sts": 3, "triggerId": 3, "updateEve": True}
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info1})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 2, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 2})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [2, 2, 2])
        self.bgm_eth_inter.ck_period_time('IntrLampSelnMod', 0.1)
    
    @allure.title("礼貌灯(内灯)控制&获取内灯模式(礼貌灯)_不响应接口调用(解闭锁成功触发源_5_重上锁)")  #LockgCenStsLockSt=3
    @pytest.mark.full
    def test_caseid_d(self):
        logger.info("硬线J3-36接地(内部信号HoodSwt1")
        self.io.set_do_level("hood_ajar_2", True)
        sleep(1)
        logger.info("硬线J3-37接地(内部信号HoodSwt2)")
        self.io.set_do_level("hood_ajar_1", True)
        sleep(1)
        logger.info("Step:使硬线J3-36悬空")
        self.io.set_do_level("hood_ajar_2", False)
        self.dk.set_cenlock_sts(1)
        self.dk.send_rke_lock()
        sleep(1)
        self.dk.send_rke_unlock()
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.empty_all(1)
        sleep(30)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetStatus', {}, {"out": 1})  #获取前舱盖状态 1=关闭 0=打开
        self.partner.send_request_and_ck_resp(TAILGATE_SERVICE_CLIENT, "GetOpenCloseStatusValidity", {}, {"out": {"value": False, "validity": 0}})  #尾门开关状态 false关 true打开
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetOpenCloseStatusValidity", {"doors": [4]},
                                                  {"out": [{"value":{"id":0,"isOpen":False},"isOpenValidity":0},
                                                           {"value":{"id":1,"isOpen":False},"isOpenValidity":0},
                                                           {"value":{"id":2,"isOpen":False},"isOpenValidity":0},
                                                           {"value":{"id":3,"isOpen":False},"isOpenValidity":0}]}) # DoorAll false关
        info1 = {"sts": 3, "triggerId": 5, "updateEve": True}
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info1})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 2, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 0})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [])
    
    @allure.title("礼貌灯(内灯)控制&获取内灯模式(礼貌灯)_不响应接口调用(解闭锁成功触发源_7_远程闭锁成功)")  #LockgCenStsLockSt=3
    @pytest.mark.full
    def test_caseid_e(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.empty_all(1)
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 1})
        info1 = {"sts": 3, "triggerId": 7, "updateEve": True}
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info1})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 2, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 0})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [])
    
    @allure.title("礼貌灯(内灯)控制&获取内灯模式(礼貌灯)_不响应接口调用(解闭锁成功触发源_9_离车自动闭锁成功)")  #LockgCenStsLockSt=3
    @pytest.mark.full
    def test_caseid_f(self):
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.empty_all(1)
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.dk.send_walk_away_lock_cmd()
        info1 = {"sts": 3, "triggerId": 9, "updateEve": True}
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info1})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 2, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 0})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [])
    
    @allure.title("礼貌灯(内灯)控制&获取内灯模式(礼貌灯)_不响应接口调用(解闭锁成功触发源_10_外部的其他方式闭锁成功)")  #LockgCenStsLockSt=3
    @pytest.mark.full
    def test_caseid_g(self):
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.empty_all(1)
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3})
        info1 = {"sts": 3, "triggerId": 10, "updateEve": True}
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info1})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 2, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 0})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [])
    
    @allure.title("礼貌灯(内灯)控制&获取内灯模式(礼貌灯)_不响应接口调用(解闭锁成功触发源_12_NFC闭锁成功)")#LockgCenStsLockSt=3
    @pytest.mark.full
    def test_caseid_h(self):
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.empty_all(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.dk.send_nfc_cmd()
        info1 = {"sts": 3, "triggerId": 12, "updateEve": True}
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info1})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 2, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 0})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [])

    @allure.title("礼貌灯(内灯)控制&获取内灯模式（礼貌灯）_下电记忆")  
    @pytest.mark.full
    def test_caseid_1918809(self):
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.empty_all(1)
        self.dk.set_cenlock_sts(1)#LockgCenStsLockSt不为2|3(解锁成功)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2})#LockgCenStsTrigSrc=3
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "InternalLightMode", {"sts": 1})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 1})

    def light_courtesy_restart_and_check_IntrLampSelnMod(self, mode, del_sdb=False):
        if del_sdb:
            self.del_s2s_db()  # 删除数据库
            self.partner.empty_all()
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.kill_bgm_process()  
            self.partner.wait_for_service_reconnect(LIGHT_SERVICE_CLIENT)
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "InternalLightMode", {"sts": 2}, timeout=5)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=1)
            self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [2, 2, 2])
        else:
            temp = 0 if mode == 2 else mode + 1
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
                {"light": {"type": 26, "zoneId": 0}, "mode": temp, "brightness": 0,
                "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
                
        self.partner.empty_all(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": mode, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "InternalLightMode", {"sts": mode})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": mode})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [mode, mode, mode])
        self.bgm_eth_inter.ck_period_time('IntrLampSelnMod', 0.1)    

        self.partner.empty_all(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.kill_bgm_process()  
        self.partner.wait_for_service_reconnect(LIGHT_SERVICE_CLIENT)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "InternalLightMode", {"sts": mode}, timeout=5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [mode, mode, mode])

    @allure.title("礼貌灯(内灯)控制_模式为0时重启服务检查主动发送的信号值")  
    @pytest.mark.sanity
    def test_caseid_1987952(self):
        self.light_courtesy_restart_and_check_IntrLampSelnMod(0)

    @allure.title("礼貌灯(内灯)控制_模式为1时重启服务检查主动发送的信号值")  
    @pytest.mark.full
    def test_caseid_1987953(self):
        self.light_courtesy_restart_and_check_IntrLampSelnMod(1)

    @allure.title("礼貌灯(内灯)控制_模式为2时重启服务检查主动发送的信号值")  
    @pytest.mark.full
    def test_caseid_1987954(self):
        self.light_courtesy_restart_and_check_IntrLampSelnMod(2)

    @allure.title("礼貌灯(内灯)控制_首次下线后重启检查信号值，再改变礼貌灯模式后重启检查信号值")  
    @pytest.mark.full
    def test_caseid_1987955(self):
        self.light_courtesy_restart_and_check_IntrLampSelnMod(1, del_sdb=True)

    @allure.title("礼貌灯(内灯)控制_在模式为0的报文发送过程中改变模式为1，检查报文是否被打断（不同模式）")  
    @pytest.mark.full
    def test_caseid_1987956(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        sleep(0.1) 
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [0, 1, 1, 1]) 

    @allure.title("礼貌灯(内灯)控制_在模式为2的报文发送过程中再设置模式为2，检查报文是否被打断（相同模式）")  
    @pytest.mark.full
    def test_caseid_1987958(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 2, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        sleep(0.05) 
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 2, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [2, 2, 2, 2]) 

    @allure.title("礼貌灯(内灯)控制_在模式为2的报文过程中设置模式为1，在模式1的报文过程中设置模式为0，检查报文是否多次被打断（多次打断）")  
    @pytest.mark.full
    def test_caseid_1987959(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 2, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        sleep(0.15) 
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        sleep(0.15) 
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=2)
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [2, 2, 1, 1, 0, 0, 0]) 
        
    @allure.title("获取内灯模式（礼貌灯）")  # 首次下线
    @pytest.mark.full
    def test_caseid_1983163(self):
        self.del_s2s_db()  # 删除数据库
        self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 2})
    
    @allure.title("设置外灯模式&获取外灯模式&通知外灯模式")
    @pytest.mark.sanity
    def test_caseid_111218(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 0}, timeout=0.3)
        self.partner.empty_all(0.5)
        for mode in [1, 2, 3, 0]:
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": mode}, timeout=0.3)
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "ExteriorLightMode", {"mode": mode})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetExteriorLightMode",{}, {"out": mode}, timeout=0.3)
            sleep(2)
            if mode ==0:
                self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
                self.bgm_eth_inter.ck_ordered_array('SwtCDCLiLoBeamSw', [0])
                self.bgm_eth_inter.ck_ordered_array('SwtCDCLiPosLampSw', [0])
                self.bgm_eth_inter.ck_ordered_array('SwtCDCLiAutoLampSw', [0])
            elif mode ==1:
                self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
                self.bgm_eth_inter.ck_ordered_array('SwtCDCLiLoBeamSw', [0])
                self.bgm_eth_inter.ck_ordered_array('SwtCDCLiPosLampSw', [0])
                self.bgm_eth_inter.ck_ordered_array('SwtCDCLiAutoLampSw', [1])
            elif mode ==2:
                self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
                self.bgm_eth_inter.ck_ordered_array('SwtCDCLiLoBeamSw', [0])
                self.bgm_eth_inter.ck_ordered_array('SwtCDCLiPosLampSw', [1])
                self.bgm_eth_inter.ck_ordered_array('SwtCDCLiAutoLampSw', [0])
            elif mode ==3:
                self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
                self.bgm_eth_inter.ck_ordered_array('SwtCDCLiLoBeamSw', [1])
                self.bgm_eth_inter.ck_ordered_array('SwtCDCLiPosLampSw', [0])
                self.bgm_eth_inter.ck_ordered_array('SwtCDCLiAutoLampSw', [0])
    
    @allure.title("设置外灯模式&获取外灯模式&通知外灯模式_下电记忆")
    @pytest.mark.full
    def test_caseid_1918804(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 0})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 1})
        self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "ExteriorLightMode", {"mode": 1})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 1})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 0})
    
    @allure.title("设置外灯模式&获取外灯模式&通知外灯模式_首次下线")
    @pytest.mark.full
    def test_caseid_111117(self):
        self.del_s2s_db()  # 删除数据库
        self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetExteriorLightMode", {}, {"out": 1})
    
    @allure.title("设置外灯FollowMeHome时长&获取外灯FollowMeHome时长&通知外灯FollowMeHome时长")
    @pytest.mark.sanity
    def test_caseid_111148(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetFollowMeHomeTime", {"time": 0})
        self.partner.empty_all(0.5)
        for sts in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 0]:
            sleep(0.5)
            logger.info(f"打印当前循环值{sts}")
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetFollowMeHomeTime", {"time": sts})
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "FollowMeHomeTime", {"time": sts})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFollowMeHomeTime", {}, {"out": sts})
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.ck_signal_values('LiHomeSafeReqSts', [sts/10])
            self.bgm_eth_inter.ck_signal_values('LiHomeSafeReqPen', [0])
    
    @allure.title("设置外灯FollowMeHome时长&获取外灯FollowMeHome时长&通知外灯FollowMeHome时长_下电记忆")
    @pytest.mark.full
    def test_caseid_1918802(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetFollowMeHomeTime", {"time": 0})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetFollowMeHomeTime", {"time": 10})
        self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "FollowMeHomeTime", {"time": 10})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFollowMeHomeTime", {}, {"out": 10})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetFollowMeHomeTime", {"time": 0})
    
    @allure.title("设置外灯FollowMeHome时长&获取外灯FollowMeHome时长&通知外灯FollowMeHome时长_首次下线")
    @pytest.mark.full
    def test_caseid_1984157(self):
        self.del_s2s_db()  # 删除数据库
        self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFollowMeHomeTime", {}, {"out": 0})
    
    @allure.title("设置氛围灯功能禁用&获取普通氛围灯功能禁用状态通知普通氛围灯功能禁用状态_禁用")
    @pytest.mark.sanity
    def test_caseid_111116(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 35, "inhibitSts": True}]})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightInhibitSts", {"sts": [{"type": 35, "inhibitSts": True}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetLightInhibitSts", {"type": [35]},
                                              {"out": [{"type": 35, "inhibitSts": True}]})
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr08, 'OrdinaryAmbientLightTweeterLeftRed', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr08, 'OrdinaryAmbientLightTweeterLeftGreen', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr08, 'OrdinaryAmbientLightTweeterLeftBlue', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr04, 'OrdinaryAmbientLightFrontRightBrightness', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr04, 'OrdinaryAmbientLightFrontRightRed', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr04, 'OrdinaryAmbientLightFrontRightGreen', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr04, 'OrdinaryAmbientLightFrontRightBlue', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr02, 'OrdinaryAmbientLightRearLeftBrightness', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr02, 'OrdinaryAmbientLightRearLeftRed', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr02, 'OrdinaryAmbientLightRearLeftGreen', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr02, 'OrdinaryAmbientLightRearLeftBlue', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr03, 'OrdinaryAmbientLightRearRightBrightness', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr03, 'OrdinaryAmbientLightRearRightRed', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr03, 'OrdinaryAmbientLightRearRightGreen', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr03, 'OrdinaryAmbientLightRearRightBlue', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr08, 'OrdinaryAmbientLightTweeterLeftBrightness', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr08, 'OrdinaryAmbientLightTweeterLeftRed', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr08, 'OrdinaryAmbientLightTweeterLeftGreen', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr08, 'OrdinaryAmbientLightTweeterLeftBlue', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr07, 'OrdinaryAmbientLightTweeterRightBrightness', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr07, 'OrdinaryAmbientLightTweeterRightRed', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr07, 'OrdinaryAmbientLightTweeterRightGreen', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr07, 'OrdinaryAmbientLightTweeterRightBlue', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr06, 'OrdinaryAmbientLightCCLeftBrightness', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr06, 'OrdinaryAmbientLightCCLeftRed', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr06, 'OrdinaryAmbientLightCCLeftGreen', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr06, 'OrdinaryAmbientLightCCLeftBlue', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr05, 'OrdinaryAmbientLightCCRightBrightness', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr05, 'OrdinaryAmbientLightCCRightRed', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr05, 'OrdinaryAmbientLightCCRightGreen', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr05, 'OrdinaryAmbientLightCCRightBlue', 0, timeout=0.5)
    
    @allure.title("设置氛围灯功能禁用&获取普通氛围灯功能禁用状态通知普通氛围灯功能禁用状态_未禁用")
    @pytest.mark.full
    def test_caseid_111187(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 35, "inhibitSts": True}]})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 35, "inhibitSts": False}]})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightInhibitSts", {"sts": [{"type": 35, "inhibitSts": False}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetLightInhibitSts", {"type": [35]},
                                              {"out": [{"type": 35, "inhibitSts": False}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
            {"light": {"type": 35, "zoneId": 1}, "PixelData": [0], "type": 0,
             "color": [{"brightness": 50, "color": {"cRed": 255, "cGreen": 255, "cBlue": 255}}]}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
            {"light": {"type": 35, "zoneId": 2}, "PixelData": [0], "type": 0,
             "color": [{"brightness": 50, "color": {"cRed": 255, "cGreen": 255, "cBlue": 255}}]}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
            {"light": {"type": 35, "zoneId": 3}, "PixelData": [0], "type": 0,
             "color": [{"brightness": 50, "color": {"cRed": 255, "cGreen": 255, "cBlue": 255}}]}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
            {"light": {"type": 35, "zoneId": 4}, "PixelData": [0], "type": 0,
             "color": [{"brightness": 50, "color": {"cRed": 255, "cGreen": 255, "cBlue": 255}}]}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
            {"light": {"type": 35, "zoneId": 17}, "PixelData": [0], "type": 0,
             "color": [{"brightness": 50, "color": {"cRed": 255, "cGreen": 255, "cBlue": 255}}]}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
            {"light": {"type": 35, "zoneId": 18}, "PixelData": [0], "type": 0,
             "color": [{"brightness": 50, "color": {"cRed": 255, "cGreen": 255, "cBlue": 255}}]}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
            {"light": {"type": 35, "zoneId": 19}, "PixelData": [0], "type": 0,
             "color": [{"brightness": 50, "color": {"cRed": 255, "cGreen": 255, "cBlue": 255}}]}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
            {"light": {"type": 35, "zoneId": 20}, "PixelData": [0], "type": 0,
             "color": [{"brightness": 50, "color": {"cRed": 255, "cGreen": 255, "cBlue": 255}}]}]})
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness', 50, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr08, 'OrdinaryAmbientLightTweeterLeftRed', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr08, 'OrdinaryAmbientLightTweeterLeftGreen', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr08, 'OrdinaryAmbientLightTweeterLeftBlue', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr04, 'OrdinaryAmbientLightFrontRightBrightness', 50, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr04, 'OrdinaryAmbientLightFrontRightRed', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr04, 'OrdinaryAmbientLightFrontRightGreen', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr04, 'OrdinaryAmbientLightFrontRightBlue', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr02, 'OrdinaryAmbientLightRearLeftBrightness', 50, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr02, 'OrdinaryAmbientLightRearLeftRed', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr02, 'OrdinaryAmbientLightRearLeftGreen', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr02, 'OrdinaryAmbientLightRearLeftBlue', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr03, 'OrdinaryAmbientLightRearRightBrightness', 50, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr03, 'OrdinaryAmbientLightRearRightRed', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr03, 'OrdinaryAmbientLightRearRightGreen', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr03, 'OrdinaryAmbientLightRearRightBlue', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr08, 'OrdinaryAmbientLightTweeterLeftBrightness', 50, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr08, 'OrdinaryAmbientLightTweeterLeftRed', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr08, 'OrdinaryAmbientLightTweeterLeftGreen', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr08, 'OrdinaryAmbientLightTweeterLeftBlue', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr07, 'OrdinaryAmbientLightTweeterRightBrightness', 50, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr07, 'OrdinaryAmbientLightTweeterRightRed', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr07, 'OrdinaryAmbientLightTweeterRightGreen', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr07, 'OrdinaryAmbientLightTweeterRightBlue', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr06, 'OrdinaryAmbientLightCCLeftBrightness', 50, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr06, 'OrdinaryAmbientLightCCLeftRed', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr06, 'OrdinaryAmbientLightCCLeftGreen', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr06, 'OrdinaryAmbientLightCCLeftBlue', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr05, 'OrdinaryAmbientLightCCRightBrightness', 50, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr05, 'OrdinaryAmbientLightCCRightRed', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr05, 'OrdinaryAmbientLightCCRightGreen', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr05, 'OrdinaryAmbientLightCCRightBlue', 255, timeout=0.5)
    
    @allure.title("设置氛围灯功能禁用&获取普通氛围灯功能禁用状态通知普通氛围灯功能禁用状态_未禁用(Venus)")
    @pytest.mark.full
    def test_caseid_1984164(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.sd_tester.write_single_ccp(950, 2)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 35, "inhibitSts": True}]})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 35, "inhibitSts": False}]})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightInhibitSts", {"sts": [{"type": 35, "inhibitSts": False}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetLightInhibitSts", {"type": [35]},
                                              {"out": [{"type": 35, "inhibitSts": False}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
            {"light": {"type": 35, "zoneId": 29}, "PixelData": [0], "type": 0,
             "color": [{"brightness": 50, "color": {"cRed": 255, "cGreen": 255, "cBlue": 255}}]}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
            {"light": {"type": 35, "zoneId": 30}, "PixelData": [0], "type": 0,
             "color": [{"brightness": 50, "color": {"cRed": 255, "cGreen": 255, "cBlue": 255}}]}]})
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr09, 'OrdinaryAmbientLightCCMiddleRightBrightness', 50, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr09, 'OrdinaryAmbientLightCCMiddleRightRed', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr09, 'OrdinaryAmbientLightCCMiddleRightGreen', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr09, 'OrdinaryAmbientLightCCMiddleRightBlue', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr0A, 'OrdinaryAmbientLightCCMiddleLeftBrightness', 50, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr0A, 'OrdinaryAmbientLightCCMiddleLeftRed', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr0A, 'OrdinaryAmbientLightCCMiddleLeftGreen', 255, timeout=0.5)
        self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr0A, 'OrdinaryAmbientLightCCMiddleLeftBlue', 255, timeout=0.5)
    
    @allure.title("设置氛围灯功能禁用&获取普通氛围灯功能禁用状态通知普通氛围灯功能禁用状态_下电记忆")#SOA-2090SOA-20906【BGM】【140AM】启动场景接收到总线信号后，部分event未上
    @pytest.mark.full
    def test_caseid_1984165(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 35, "inhibitSts": False}]})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 35, "inhibitSts": True}]})
        self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightInhibitSts", {"sts": [{"type": 35, "inhibitSts": False}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetLightInhibitSts", {"type": [35]},
                                              {"out": [{"type": 35, "inhibitSts": False}]})
    
    @allure.title("设置氛围灯功能禁用&获取智能氛围灯功能禁用状态通知智能氛围灯功能禁用状态_禁用")
    @pytest.mark.sanity
    def test_caseid_111120(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 25, "inhibitSts": False}]}, timeout=0.5)
        self.partner.empty_all(0.5)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 25, "inhibitSts": True}]}, timeout=0.5)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightInhibitSts", {"sts": [{"type": 25, "inhibitSts": True}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetLightInhibitSts", {"type": [25]},
                                              {"out": [{"type": 25, "inhibitSts": True}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
            {"light": {"type": 25, "zoneId": 1}, "PixelData": [0], "type": 0,
             "color": [{"brightness": 50, "color": {"cRed": 255, "cGreen": 255, "cBlue": 255}}]}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('SmartAmbientLightIpRight0Brightness', [0])
    
    
    @allure.title("设置氛围灯功能禁用&获取智能氛围灯功能禁用状态通知智能氛围灯功能禁用状态_未禁用")
    @pytest.mark.full
    def test_caseid_111135(self):
        self.sd_tester.change_usage_mode(13)
        self.sd_tester.change_car_mode(0)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 25, "inhibitSts": True}]})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 25, "inhibitSts": False}]})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightInhibitSts", {"sts": [{"type": 25, "inhibitSts": False}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetLightInhibitSts", {"type": [25]},
                                              {"out": [{"type": 25, "inhibitSts": False}]})
        file_path, save_name = self.bgmcli.start_bgm_tcpdump()
        data_list = [(6251, 864, 6, 7)]  # （pdu的id，数据长度，信号起始bit未，信号长度）
        for id in [1, 2, 3, 4, 15, 16]:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightShowControlWithLightDevice", {"lights": [
            {"light": {"type": 25, "zoneId": id}, "PixelData": [0], "type": 0,
             "color": [{"brightness": 50, "color": {"cRed": 255, "cGreen": 255, "cBlue": 255}}]}]})
            sleep(0.5)
        res_dict = self.stop_tcpdump_and_copy_and_calculate(save_name, data_list)
        assert len(res_dict[(6251, 864, 6, 7)]) == 6, "当前次数为几"
    
    @allure.title("设置氛围灯功能禁用&获取智能氛围灯功能禁用状态通知智能氛围灯功能禁用状态_下电记忆")
    @pytest.mark.full
    def test_caseid_1984170(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 25, "inhibitSts": False}]})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetAmbientInhibit",
                                         {"ambientInhibit": [{"type": 25, "inhibitSts": True}]})
        self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetLightInhibitSts", {"type": [25]},
                                              {"out": [{"type": 25, "inhibitSts": False}]})

    @allure.title(" CDC断连导致通道阻塞时灯光功能安全")
    @pytest.mark.full
    def test_caseid_1903203(self):
        self.sd_tester.change_usage_mode(13)
        self.sd_tester.change_car_mode(0)
        # 设置外灯模式为关
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 0})
        # 夜晚模式
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawTwliBriRaw_0_RlsmCem_Lin1SignalIPdu01',
                      0)  # SUS光感-1000为白天-0-1000为夜晚;
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawQf_0_RlsmCem_Lin1SignalIPdu01', 3)  # SUS光感QF3
        self.ipdu.set(
            self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'OutdBriSts', 1)
        # 车速为0
        self.ipdu.set_vehspd(0)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "GetLightInhibitSts", {"type": 0})
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "GetLightInhibitSts", {"type": 0})
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "GetLightInhibitSts", {"type": 0})
        sleep(5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 6, "zoneId": 0}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 0})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 6, "zoneId": 0}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "GetLightInhibitSts", {"type": 0})
        sleep(2.9)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 1})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 6, "zoneId": 0}]})

    @allure.title("方向盘灯带控制")  # 左侧L2按键灯光控制
    @pytest.mark.sanity
    def test_caseid_111171(self):
        for brightness, r, g, b in [(1, 254, 255, 0), (99, 1, 254, 255), (100, 0, 255, 254), (0, 255, 0, 1)]:
            self.bgm_eth_inter.start_bgm_tcpdump()
            logger.info(f"打印当前循环值bright={brightness},cRed={r},cGreen={g},cBlue={b}")
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
                                                {"lights": [{"light": {"type": 33, "zoneId": 12}, "mode": 0,
                                                            "brightness": brightness,"color": {"cRed": r, "cGreen": g,"cBlue": b}}]})
            self.ipdu.check_multiple_signals([(self.ipdu.bodycan.BgmBodyFr14, 'SteerWhlSymbolLightCtrlLeBrightness', brightness),
                                                (self.ipdu.bodycan.BgmBodyFr14, 'SteerWhlSymbolLightCtrlLeRed', r),
                                                (self.ipdu.bodycan.BgmBodyFr14, 'SteerWhlSymbolLightCtrlLeGreen', g),
                                                (self.ipdu.bodycan.BgmBodyFr14, 'SteerWhlSymbolLightCtrlLeBlue', b)], timeout=0.5)
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlLeBrightness', [brightness])    
            self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlLeRed', [r])
            self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlLeGreen', [g])
            self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlLeBlue', [b])
    
    @allure.title("方向盘灯带控制")  # 右侧R2按键灯光控制
    @pytest.mark.full
    def test_caseid_111217(self):
        self.partner.empty_all(1)
        for brightness, r, g, b in [(1, 254, 255, 0), (99, 1, 254, 255), (100, 0, 255, 254), (0, 255, 0, 1)]:
            logger.info(f"打印当前循环值bright={brightness},cRed={r},cGreen={g},cBlue={b}")
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
                                                {"lights": [{"light": {"type": 33, "zoneId": 13}, "mode": 0,
                                                            "brightness": brightness,
                                                            "color": {"cRed": r, "cGreen": g,
                                                                    "cBlue": b}}]})
            self.ipdu.check_multiple_signals([(self.ipdu.bodycan.BgmBodyFr14, 'SteerWhlSymbolLightCtrlRiBrightness', brightness),
                                              (self.ipdu.bodycan.BgmBodyFr14, 'SteerWhlSymbolLightCtrlRiRed', r),
                                              (self.ipdu.bodycan.BgmBodyFr14, 'SteerWhlSymbolLightCtrlRiGreen', g),
                                              (self.ipdu.bodycan.BgmBodyFr14, 'SteerWhlSymbolLightCtrlRiBlue', b)], timeout=0.5)
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiBrightness', [brightness])
            self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiRed', [r])
            self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiGreen', [g])
            self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiBlue', [b])

    @allure.title("方向盘灯带控制")  # 长条指示灯L7控制
    @pytest.mark.sanity
    def test_caseid_111224(self):
        self.partner.empty_all(0.5)
        for brightness, r, g, b in [(1, 254, 255, 0), (99, 1, 254, 255), (100, 0, 255, 254), (0, 255, 0, 1)]:
            logger.info(f"打印当前循环值bright={brightness},cRed={r},cGreen={g},cBlue={b}")
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
                                                {"lights": [{"light": {"type": 33, "zoneId": 14}, "mode": 0,
                                                            "brightness": brightness,
                                                            "color": {"cRed": r, "cGreen": g,
                                                                    "cBlue": b}}]})
            self.ipdu.check_multiple_signals([(self.ipdu.bodycan.BgmBodyFr13, 'SteerWhlLightingBarCtrlBrightness', brightness),
                                                (self.ipdu.bodycan.BgmBodyFr13, 'SteerWhlLightingBarCtrlRed', r),
                                                (self.ipdu.bodycan.BgmBodyFr13, 'SteerWhlLightingBarCtrlGreen', g),
                                                (self.ipdu.bodycan.BgmBodyFr13, 'SteerWhlLightingBarCtrlBlue', b)], timeout=0.5)#同时校验四个信号
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlBrightness', [brightness])
            self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlRed', [r])
            self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlGreen', [g])
            self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlBlue', [b])
    
    @allure.title("远光灯控制（仲裁)_超车灯开")
    @pytest.mark.smoke
    def test_caseid_1984259(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3})  # 设置近光灯打开
        # 确保环境正常
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedHiBeamLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedHiBeamRi', 0)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                        {"info": {"cmd": 255, "clientId": 1}}, timeout=0.5)  
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                         {"info": {"cmd": 255, "clientId": 255}}, timeout=0.5)#独占释放 恢复环境
        for id in [6, 4, 5, 3, 2, 1]:
            self.bgm_eth_inter.start_bgm_tcpdump()
            sleep(0.5)
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                            {"info": {"cmd": 1, "clientId": id}}, timeout=0.5)  
            sleep(1)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.ck_signal_values('HiBeamSw', [1, 0])
    
    @pytest.mark.sanity
    @allure.title("通知/获取远光灯开关状态_老方向盘")  # V2.2
    def test_caseid_1989048(self):
        self.sd_tester.write_single_ccp(629, 4)
        sleep(1)
        # SteerWhlTouchSwtLe3信号值长度为2bit, 取值只能是0，1，2，3
        for i in [1, 0, 2]: 
            logger.info(f"SteerWhlTouchSwtLe3:{i}")
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', i)
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": i})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": i})

        for i in [1, 0, 2, 4]:
            logger.info(f"LeverSwtLeLvrSwt2:{i}")
            sts = 2 if i == 4 else i
            self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', i)
            if i == 4:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus")
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": sts})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": sts})
            
        # SteerWhlTouchSwtLe3 != 3 && LeverSwtLeLvrSwt2 = 3
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 3)
        self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus")

        # SteerWhlTouchSwtLe3 = 3 && LeverSwtLeLvrSwt2 != 3
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 4)
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 3)
        self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus")
        
        # SteerWhlTouchSwtLe3 = 3 && LeverSwtLeLvrSwt2 = 3
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 3)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 3})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": 3})        

    @pytest.mark.full
    @allure.title("通知/获取远光灯开关状态_老方向盘_无效值(other状态)")  # V2.2
    def test_caseid_1989049(self):
        self.sd_tester.write_single_ccp(629, 4)
        sleep(1)
        # LeverSwtLeLvrSwt3从无效值(4) → 0,1,2,3
        for i in [0, 1, 2, 3]:
            self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 4)
            sleep(0.1)
            self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', i)
            self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus")
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": 0})

    @pytest.mark.full
    @allure.title("通知/获取远光灯开关状态_老方向盘_拨杆和按键多次赋值") # V2.2
    def test_caseid_1989050(self):
        self.sd_tester.write_single_ccp(629, 4)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": 1})
        
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 1)
        self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus")
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": 1})

        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 2)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 2})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": 2})
        
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 0)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 0})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": 0})

    @pytest.mark.full
    @allure.title("通知/获取远光灯开关状态_老方向盘_重启场景(默认值和非默认值)") # V2.2
    def test_caseid_1989052(self):
        self.sd_tester.write_single_ccp(629, 4)
        sleep(1)
        # 当前状态为0
        sts = 0
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', sts)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', sts)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": sts})
        self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": sts})
        # self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus")  # SOA-29048
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": sts}, timeout=15)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": sts})
        self.partner.empty_all()
        
        # 当前状态为1和3 停止SteerWhlTouchSwtLe3发送
        for sts in [0, 1, 2, 3]:
            logger.info(f"sts:{sts}")
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', sts)
            self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', sts)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": sts})
            self.ipdu.stop_send_pdu('bodycan', 0x268)   # 停止SteerWhlTouchSwtLe3发送
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
            logger.info(f"restart success.")
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 0}, timeout=15)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": 0})
            self.ipdu.resume_bus_send("bodycan")        # 恢复SteerWhlTouchSwtLe3发送
            if sts != 0:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": sts})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": sts})
            self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus")

        # 当前状态为1和3 停止LeverSwtLeLvrSwt3发送
        for sts in [0, 1, 2, 3]:
            logger.info(f"sts:{sts}")
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', sts)
            self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', sts)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": sts})
            self.ipdu.stop_send_pdu('bodycan', 0x1ff)   # 停止LeverSwtLeLvrSwt3发送
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
            logger.info(f"restart success.")
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 0 if sts == 3 else sts}, timeout=15)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": 0 if sts == 3 else sts})
            self.ipdu.resume_bus_send("bodycan")        # 恢复LeverSwtLeLvrSwt3发送
            if sts == 3:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": sts})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": sts})
            self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus")
        
    @pytest.mark.full
    @allure.title("通知/获取远光灯开关状态_老方向盘_重启场景(other状态)") # V2.2
    def test_caseid_1989053(self):
        self.sd_tester.write_single_ccp(629, 4)
        sleep(1)
        # 当前状态为2
        sts = 2
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', sts)  
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', sts)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": sts})

        # other状态 (last value为2)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 4)
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 2)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": sts})
        self.ipdu.stop_send_pdu('bodycan', 0x268)   # 停止SteerWhlTouchSwtLe3发送
        self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 0}, timeout=15)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": 0})
        
        self.ipdu.resume_bus_send("bodycan")        # 恢复SteerWhlTouchSwtLe3发送
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": sts})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": sts})

    @pytest.mark.sanity
    @allure.title("通知/获取远光灯开关状态_新方向盘")  # V2.2
    def test_caseid_1989055(self):
        self.sd_tester.write_single_ccp(629, 6)
        sleep(1)
        # SteerWhlTouchSwtRi1SteerWhlTouchSwt2信号值长度为2bit, 取值只能是0，1，2，3
        for i in [1, 0, 2]: 
            logger.info(f"SteerWhlTouchSwtRi1SteerWhlTouchSwt2:{i}")
            self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi1SteerWhlTouchSwt2', i)
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": i})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": i})

        for i in [1, 0, 2, 4]:
            logger.info(f"LeverSwtLeLvrSwt2:{i}")
            sts = 2 if i == 4 else i
            self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', i)
            if i == 4:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus")
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": sts})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": sts})
            
        # SteerWhlTouchSwtRi1SteerWhlTouchSwt2 != 3 && LeverSwtLeLvrSwt2 = 3
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 3)
        self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus")

        # SteerWhlTouchSwtRi1SteerWhlTouchSwt2 = 3 && LeverSwtLeLvrSwt2 != 3
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 4)
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi1SteerWhlTouchSwt2', 3)
        self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus")
        
        # SteerWhlTouchSwtRi1SteerWhlTouchSwt2 = 3 && LeverSwtLeLvrSwt2 = 3
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 3)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 3})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": 3})        

    @pytest.mark.full
    @allure.title("通知/获取远光灯开关状态_新方向盘_无效值(other状态)")  # V2.2
    def test_caseid_1989056(self):
        self.sd_tester.write_single_ccp(629, 6)
        sleep(1)
        # LeverSwtLeLvrSwt3从无效值(4) → 0,1,2,3
        for i in [0, 1, 2, 3]:
            self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 4)
            sleep(0.1)
            self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', i)
            self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus")
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": 0})

    @pytest.mark.full
    @allure.title("通知/获取远光灯开关状态_新方向盘_拨杆和按键多次赋值") # V2.2
    def test_caseid_1989058(self):
        self.sd_tester.write_single_ccp(629, 6)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi1SteerWhlTouchSwt2', 1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": 1})
        
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 1)
        self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus")
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": 1})

        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi1SteerWhlTouchSwt2', 2)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 2})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": 2})
        
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 0)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 0})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": 0})

    @pytest.mark.full
    @allure.title("通知/获取远光灯开关状态_新方向盘_重启场景(默认值和非默认值)") # V2.2
    def test_caseid_1989059(self):
        self.sd_tester.write_single_ccp(629, 6)
        sleep(1)
        # 当前状态为0
        sts = 0
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi1SteerWhlTouchSwt2', sts)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', sts)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": sts})
        self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": sts})
        # self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus")  # SOA-29048
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": sts}, timeout=15)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": sts})
        self.partner.empty_all()
        
        # 当前状态为1和3 停止SteerWhlTouchSwtRi1SteerWhlTouchSwt2发送
        for sts in [1, 3]:
            self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi1SteerWhlTouchSwt2', sts)
            self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', sts)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": sts})
            self.ipdu.stop_send_pdu('bodycan', 0x271)   # 停止SteerWhlTouchSwtRi1SteerWhlTouchSwt2发送
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 0}, timeout=15)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": 0})
            self.ipdu.resume_bus_send("bodycan")        # 恢复SteerWhlTouchSwtRi1SteerWhlTouchSwt2发送
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": sts})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": sts})
            self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus")

        # 当前状态为1和3 停止LeverSwtLeLvrSwt3发送
        for sts in [1, 3]:
            self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi1SteerWhlTouchSwt2', sts)
            self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', sts)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": sts})
            self.ipdu.stop_send_pdu('bodycan', 0x1ff)   # 停止LeverSwtLeLvrSwt3发送
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 1 if sts == 1 else 0}, timeout=15)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": 1 if sts == 1 else 0})
            self.ipdu.resume_bus_send("bodycan")        # 恢复LeverSwtLeLvrSwt3发送
            if sts == 3:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": sts})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": sts})
            self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus")
        
    @pytest.mark.full
    @allure.title("通知/获取远光灯开关状态_新方向盘_重启场景(other状态)") # V2.2
    def test_caseid_1989054(self):
        self.sd_tester.write_single_ccp(629, 6)
        sleep(1)
        # 当前状态为2
        sts = 2
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi1SteerWhlTouchSwt2', sts)  
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', sts)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": sts})

        # other状态 (last value为2)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 4)
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 2)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": sts})
        self.ipdu.stop_send_pdu('bodycan', 0x271)   # 停止SteerWhlTouchSwtRi1SteerWhlTouchSwt2发送
        self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": 0}, timeout=15)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": 0})
        
        self.ipdu.resume_bus_send("bodycan")        # 恢复SteerWhlTouchSwtRi1SteerWhlTouchSwt2发送
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHighBeamSwitchStatus", {"swtsts": sts})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": sts})
 
    @allure.title("获取远光灯开关按键状态&通知远光灯开关按键状态_BGM首次下线默认配置")
    @pytest.mark.full
    def test_caseid_1984257(self):
        # 删除数据库
        bgmssh = BGM_SSH()
        bgmssh.type_commands("sudo rm -rf /data/s2s_service/s2sdb", root_permission=True)
        sleep(1)
        bgmssh.type_commands("ls -l /data/s2s_service")
        sleep(1)
        self.ipdu.pause_all_bus_send()  # 停掉总线
        self.nucapp.bgm_power_off()
        sleep(7)
        self.partner.empty_all()
        self.nucapp.bgm_power_on()
        self.partner.wait_for_service_reconnect(LIGHT_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamSwitchStatus", {}, {"out": 0})

    @allure.title("设置灯光秀激活状态（外灯)SequenceControl")#参数status=1(True)时,发送三帧1再发三帧0 
    @pytest.mark.smoke
    def test_caseid_1983978(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetLightShowActivateStatus",
                                         {"status": True})  # 设置灯光秀激活状态
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('StaticLightingModeReq', [1, 1, 1, 0, 0, 0])
    
    @allure.title("设置灯光秀激活状态（外灯)SequenceControl")#参数status=0（False）时，发送三帧StaticLightModeReq=2=Off 
    @pytest.mark.full
    def test_caseid_1983979(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetLightShowActivateStatus",
                                         {"status": False})  # 设置灯光秀激活状态
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('StaticLightingModeReq', [2, 2, 2])
        self.bgm_eth_inter.ck_period_time('StaticLightingModeReq', 0.1)
    
    @allure.title("设置灯光秀激活状态（外灯)SequenceControl")#300ms后打断(True-True)  
    @pytest.mark.full
    def test_caseid_1983980(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetLightShowActivateStatus",
                                         {"status": True})  # 设置灯光秀激活状态
        sleep(0.35)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetLightShowActivateStatus",
                                         {"status": True})  # 设置灯光秀激活状态
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('StaticLightingModeReq', [1, 1, 1, 0, 1, 1, 1, 0, 0, 0])
    
    @allure.title("设置灯光秀激活状态（外灯)SequenceControl")#300ms后打断(True-False)  
    @pytest.mark.sanity
    def test_caseid_1983982(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetLightShowActivateStatus",
                                         {"status": True})  # 设置灯光秀激活状态
        sleep(0.35)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetLightShowActivateStatus",
                                         {"status": False})  # 设置灯光秀激活状态
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('StaticLightingModeReq', [1, 1, 1, 0, 2, 2, 2])
    
    @allure.title("设置灯光秀激活状态（外灯)SequenceControl")#300ms内打断  
    @pytest.mark.full
    def test_caseid_1983983(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetLightShowActivateStatus",
                                         {"status": True})  # 设置灯光秀激活状态
        sleep(0.15)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetLightShowActivateStatus",
                                         {"status": True})  # 设置灯光秀激活状态
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('StaticLightingModeReq', [1, 1, 1, 1, 1, 0, 0, 0])

    @allure.title("设置灯光秀激活状态（外灯)SequenceControl")#300ms内打断  
    @pytest.mark.full
    def test_caseid_1983984(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetLightShowActivateStatus",
                                         {"status": True})  # 设置灯光秀激活状态
        sleep(0.15)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetLightShowActivateStatus",
                                         {"status": False})  # 设置灯光秀激活状态
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('StaticLightingModeReq', [1, 1, 2, 2, 2])
    
    @allure.title("设置灯光秀激活状态（外灯)SequenceControl")#打断(False-True) 
    @pytest.mark.sanity
    def test_caseid_1983985(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetLightShowActivateStatus",
                                         {"status": False})  # 设置灯光秀激活状态
        sleep(0.15)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetLightShowActivateStatus",
                                         {"status": True})  # 设置灯光秀激活状态
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('StaticLightingModeReq', [2, 2, 1, 1, 1, 0, 0, 0])
    
    @allure.title("设置灯光秀激活状态（外灯)SequenceControl")#打断(False-False) 
    @pytest.mark.full
    def test_caseid_1983986(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetLightShowActivateStatus",
                                         {"status": False})  # 设置灯光秀激活状态
        sleep(0.15)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetLightShowActivateStatus",
                                         {"status": False})  # 设置灯光秀激活状态
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('StaticLightingModeReq', [2, 2, 2, 2, 2])

    @allure.title("获取ADS灯状态&通知ADS灯状态_kLightOFF")  ##Jidu车型配置信息识别为“Venus判断为ADS灯状态
    @pytest.mark.full
    def test_caseid_1979746(self):
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntWheelLampLe', 1)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedFrntWheelLampRi', 1)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReWheelLampLe', 1)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReWheelLampRi', 1)
        self.partner.empty_all(0.5)
        self.sd_tester.write_single_ccp(950, 2)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntWheelLampLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedFrntWheelLampRi', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReWheelLampLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReWheelLampRi', 0)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
            "sts": {"light": {"type": 40, "zoneId": 12}, "sts": 0, "brightness": 0,
                    "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
            "sts": {"light": {"type": 40, "zoneId": 9}, "sts": 0, "brightness": 0,
                    "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
            "sts": {"light": {"type": 40, "zoneId": 10}, "sts": 0, "brightness": 0,
                    "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
            "sts": {"light": {"type": 40, "zoneId": 13}, "sts": 0, "brightness": 0,
                    "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 40, "zoneId": 12}]},
                                              {"out": [{"light": {"type": 40, "zoneId": 12}, "sts": 0, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 40, "zoneId": 9}]},
                                              {"out": [{"light": {"type": 40, "zoneId": 9}, "sts": 0, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 40, "zoneId": 10}]},
                                              {"out": [{"light": {"type": 40, "zoneId": 10}, "sts": 0, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 40, "zoneId": 13}]},
                                              {"out": [{"light": {"type": 40, "zoneId": 13}, "sts": 0, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})

    @allure.title("获取ADS灯状态&通知ADS灯状态_kLightOn")  ##Jidu车型配置信息识别为“Venus判断为ADS灯状态
    @pytest.mark.full
    def test_caseid_1979747(self):
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntWheelLampLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedFrntWheelLampRi', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReWheelLampLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReWheelLampRi', 0)
        self.partner.empty_all(0.5)
        self.sd_tester.write_single_ccp(950, 2)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntWheelLampLe', 1)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedFrntWheelLampRi', 1)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReWheelLampLe', 1)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReWheelLampRi', 1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
            "sts": {"light": {"type": 40, "zoneId": 12}, "sts": 1, "brightness": 0,
                    "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
            "sts": {"light": {"type": 40, "zoneId": 9}, "sts": 1, "brightness": 0,
                    "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
            "sts": {"light": {"type": 40, "zoneId": 10}, "sts": 1, "brightness": 0,
                    "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
            "sts": {"light": {"type": 40, "zoneId": 13}, "sts": 1, "brightness": 0,
                    "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 40, "zoneId": 12}]},
                                              {"out": [{"light": {"type": 40, "zoneId": 12}, "sts": 1, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 40, "zoneId": 9}]},
                                              {"out": [{"light": {"type": 40, "zoneId": 9}, "sts": 1, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 40, "zoneId": 10}]},
                                              {"out": [{"light": {"type": 40, "zoneId": 10}, "sts": 1, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 40, "zoneId": 13}]},
                                              {"out": [{"light": {"type": 40, "zoneId": 13}, "sts": 1, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})

    @allure.title("获取ADS灯状态&通知ADS灯状态_kLightFault")  ##Jidu车型配置信息识别为“Venus判断为ADS灯状态
    @pytest.mark.smoke
    def test_caseid_1979748(self):
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntWheelLampLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedFrntWheelLampRi', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReWheelLampLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReWheelLampRi', 0)
        self.partner.empty_all(0.5)
        self.sd_tester.write_single_ccp(950, 2)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntWheelLampLe', 2)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedFrntWheelLampRi', 2)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReWheelLampLe', 2)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReWheelLampRi', 2)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
            "sts": {"light": {"type": 40, "zoneId": 12}, "sts": 2, "brightness": 0,
                    "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
            "sts": {"light": {"type": 40, "zoneId": 9}, "sts": 2, "brightness": 0,
                    "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
            "sts": {"light": {"type": 40, "zoneId": 10}, "sts": 2, "brightness": 0,
                    "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
            "sts": {"light": {"type": 40, "zoneId": 13}, "sts": 2, "brightness": 0,
                    "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 40, "zoneId": 12}]},
                                              {"out": [{"light": {"type": 40, "zoneId": 12}, "sts": 2, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 40, "zoneId": 9}]},
                                              {"out": [{"light": {"type": 40, "zoneId": 9}, "sts": 2, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 40, "zoneId": 10}]},
                                              {"out": [{"light": {"type": 40, "zoneId": 10}, "sts": 2, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 40, "zoneId": 13}]},
                                              {"out": [{"light": {"type": 40, "zoneId": 13}, "sts": 2, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})

    @allure.title("获取ADS灯状态&通知ADS灯状态_默认值")  # Venus判断为ADS灯状态
    @pytest.mark.full
    def test_caseid_1988827(self):
        self.sd_tester.write_single_ccp(950, 2)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        for sts in [0, 1]:
            self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntWheelLampLe', sts)
            self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedFrntWheelLampRi', sts)
            self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReWheelLampLe', sts)
            self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReWheelLampRi', sts)
            sleep(0.1)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            for zoneid in [12, 9, 10, 13]:
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                            {"lights": [{"type": 40, "zoneId": zoneid}]},
                                            {"out": [{"light": {"type": 40, "zoneId": zoneid}, "sts": 0, "brightness": 0,
                                                      "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            for zoneid in [12, 9, 10, 13]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                    "sts": {"light": {"type": 40, "zoneId": zoneid}, "sts": sts, "brightness": 0,
                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                            {"lights": [{"type": 40, "zoneId": zoneid}]},
                                            {"out": [{"light": {"type": 40, "zoneId": zoneid}, "sts": sts, "brightness": 0,
                                                      "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
 
    @allure.title("查询轮眉灯状态&通知轮眉灯状态_kLightOff")  
    @pytest.mark.full
    def test_caseid_111134(self):
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntWheelLampLe', 1)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedFrntWheelLampRi', 1)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReWheelLampLe', 1)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReWheelLampRi', 1)
        self.partner.empty_all(0.5)
        self.sd_tester.write_single_ccp(950, 1)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntWheelLampLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedFrntWheelLampRi', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReWheelLampLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReWheelLampRi', 0)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
            "sts": {"light": {"type": 1, "zoneId": 1}, "sts": 0, "brightness": 0,
                    "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
            "sts": {"light": {"type": 1, "zoneId": 2}, "sts": 0, "brightness": 0,
                    "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
            "sts": {"light": {"type": 1, "zoneId": 3}, "sts": 0, "brightness": 0,
                    "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
            "sts": {"light": {"type": 1, "zoneId": 4}, "sts": 0, "brightness": 0,
                    "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 1, "zoneId": 0}]},
                                              {"out": [{"light": {"type": 1, "zoneId": 1}, "sts": 0, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 1, "zoneId": 0}]},
                                              {"out": [{"light": {"type": 1, "zoneId": 2}, "sts": 0, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 1, "zoneId": 0}]},
                                              {"out": [{"light": {"type": 1, "zoneId": 3}, "sts": 0, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 1, "zoneId": 0}]},
                                              {"out": [{"light": {"type": 1, "zoneId": 4}, "sts": 0, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})

    @allure.title("查询轮眉灯状态&通知轮眉灯状态_kLightOn") 
    @pytest.mark.smoke
    def test_caseid_1979744(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        for sts in [1, 2, 0]:
            self.set_WheelLamp_signal(sts, sts, sts, sts)
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                "sts": {"light": {"type": 1, "zoneId": 1}, "sts": sts, "brightness": 0,
                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                "sts": {"light": {"type": 1, "zoneId": 2}, "sts": sts, "brightness": 0,
                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                "sts": {"light": {"type": 1, "zoneId": 3}, "sts": sts, "brightness": 0,
                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                "sts": {"light": {"type": 1, "zoneId": 4}, "sts": sts, "brightness": 0,
                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 1, "zoneId": 0}]},
                                                {"out": [{"light": {"type": 1, "zoneId": 1}, "sts": sts, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 1, "zoneId": 0}]},
                                                {"out": [{"light": {"type": 1, "zoneId": 2}, "sts": sts, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 1, "zoneId": 0}]},
                                                {"out": [{"light": {"type": 1, "zoneId": 3}, "sts": sts, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 1, "zoneId": 0}]},
                                                {"out": [{"light": {"type": 1, "zoneId": 4}, "sts": sts, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})

    @allure.title("查询轮眉灯状态&通知轮眉灯状态_kLightFault")  
    @pytest.mark.full
    def test_caseid_1979745(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntWheelLampLe', 2)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedFrntWheelLampRi', 2)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReWheelLampLe', 2)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReWheelLampRi', 2)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
            "sts": {"light": {"type": 1, "zoneId": 1}, "sts": 2, "brightness": 0,
                    "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
            "sts": {"light": {"type": 1, "zoneId": 2}, "sts": 2, "brightness": 0,
                    "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
            "sts": {"light": {"type": 1, "zoneId": 3}, "sts": 2, "brightness": 0,
                    "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
            "sts": {"light": {"type": 1, "zoneId": 4}, "sts": 2, "brightness": 0,
                    "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 1, "zoneId": 0}]},
                                              {"out": [{"light": {"type": 1, "zoneId": 1}, "sts": 2, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 1, "zoneId": 0}]},
                                              {"out": [{"light": {"type": 1, "zoneId": 2}, "sts": 2, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 1, "zoneId": 0}]},
                                              {"out": [{"light": {"type": 1, "zoneId": 3}, "sts": 2, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 1, "zoneId": 0}]},
                                              {"out": [{"light": {"type": 1, "zoneId": 4}, "sts": 2, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})

    @allure.title("查询轮眉灯状态&通知轮眉灯状态_默认值") 
    @pytest.mark.full
    def test_caseid_1988826(self):
        self.sd_tester.write_single_ccp(950, 1)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        for sts in [1, 0]:
            logger.info(f"sts:{sts}")
            self.set_WheelLamp_signal(sts, sts, sts, sts)
            sleep(0.1)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            for zoneid in range(1, 5):
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                    {"lights": [{"type": 1, "zoneId": zoneid}]},
                                                    {"out": [{"light": {"type": 1, "zoneId": zoneid}, "sts": 0, "brightness": 0,
                                                              "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            for zoneid in range(1, 5):
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                    "sts": {"light": {"type": 1, "zoneId": zoneid}, "sts": sts, "brightness": 0,
                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                    {"lights": [{"type": 1, "zoneId": zoneid}]},
                                                    {"out": [{"light": {"type": 1, "zoneId": zoneid}, "sts": sts, "brightness": 0,
                                                              "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})

@allure.feature("SOA服务接口")
@allure.story("整车控制/LightService")
@pytest.mark.ypp
class TestLightServiceMockMcu(TestBase):

    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21", tcp_down_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("LightService", "client")])
        self.partner.wait_for_service_reconnect(LIGHT_SERVICE_CLIENT)
        
    def after_class(self, ecu):
        try:
            self.partner.stop_operators()
        except Exception as e:
            logger.error(f"{str(e)}")
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 0)#方向盘背光灯功能使能的状态
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr04, 'SwtLiHzrdWarn', 0)#危险报警灯开关按键状态
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFlash', 0)#超车灯状态
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsLoBeam', 0)#近光灯状态
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsAHL', 0)#大灯水平高度调节状态
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReverseLi', 0)#倒车灯状态
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', 0)#制动灯状态
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsDRL', 0)#日间行车灯状态
        #轮眉灯状态
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntWheelLampLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedFrntWheelLampRi', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReWheelLampLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReWheelLampRi', 0)
        #转向灯状态
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)#危险报警灯状态
        #位置灯无故障
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiRe', 0)
        #雾灯无故障
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFrntFogTBD', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', 0)#远光灯无故障
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsAFSTBD', 0)#自适应前照明灯系统无故障
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 0)#白天黑夜状态
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 0)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'IntrBriSts', 0)#内灯背光亮度等级
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt', 0)  # 前位置灯
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiRe', 0)  # 后位置灯
        #Pixel像素灯灯组状态
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntLampLe1', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedFrntLampRi1', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReLampLe2', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReLampRi2', 0)
        #DRL/TI灯灯组状态
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntLampLe2', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedFrntLampRi2', 0)
        #AI灯状态(左侧)
        self.ipdu.set(self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, 'StsOfLedLeftAIILY1', 0)
        self.ipdu.set(self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, 'StsOfLedLeftAIILY2', 0)
        self.ipdu.set(self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, 'StsOfLedLeftAIILY3', 0)
        self.ipdu.set(self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, 'StsOfLedLeftAIILY4', 0)
        #AI灯状态(右侧)
        self.ipdu.set(self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, 'StsOfLedRightAIILY1', 0)
        self.ipdu.set(self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, 'StsOfLedRightAIILY2', 0)
        self.ipdu.set(self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, 'StsOfLedRightAIILY3', 0)
        self.ipdu.set(self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, 'StsOfLedRightAIILY4', 0)
        #一字眉灯灯组状态
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntLampMid1', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReLampLe1', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReLampRi1',0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmmBodyExpoFr02, 'StsOfLedReLampMid1', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1', 0)#carmode信号
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1)#usagemode信号
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06', 0)#车速
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06', 3)#车速
        #照脚灯
        self.bgm_eth_inter.set_signal("StsOfLedFootwellLightFrntLe", 0)
        self.bgm_eth_inter.set_signal("StsOfLedFootwellLightFrntRi", 0)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
                                            {"lights": [{"light": {"type": 33, "zoneId": 12}, "mode": 0,
                                                        "brightness": 0,"color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
                                            {"lights": [{"light": {"type": 33, "zoneId": 13}, "mode": 0,
                                                        "brightness": 0,"color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
                                            {"lights": [{"light": {"type": 33, "zoneId": 14}, "mode": 0,
                                                        "brightness": 0,"color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl",
                                            {"lights": [{"light": {"type": 3, "zoneId": 0}, "mode": 0,
                                                        "brightness": 0,"color": {"cRed": 0, "cGreen": 0,"cBlue": 0}}]})#日间行车灯关闭
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 12, "mode": 0}]}, timeout=0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 13, "mode": 0}]}, timeout=0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 14, "mode": 0}]}, timeout=0.5)
        #阅读灯控制
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 1}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 2}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 3}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 22, "zoneId": 4}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        #礼貌灯内灯
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        #位置灯图案切换
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 38, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        #照脚灯
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 24, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.empty_all(10)

        # 近光灯、雾灯、轮眉灯、AI灯、位置灯、超车灯、倒车灯、制动灯、日间行车灯、转向灯、危险报警灯、Pixel像素灯、一字眉灯、DRL/TI灯、ADS灯
        self.light_dict = {'ExtrLtgStsLoBeam': [self.ipdu.backbonefr.CemBackBoneFr02, Light.LowBeam, ZoneID.AllOrSingle, 0],
                        'ExtrLtgStsFrntFogTBD': [self.ipdu.backbonefr.CemBackBoneFr02, Light.Fog, ZoneID.Front, 0],
                        'ExtrLtgStsReFog': [self.ipdu.backbonefr.CemBackBoneFr02, Light.Fog, ZoneID.Rear, 0],
                        'StsOfLedFrntWheelLampLe': [self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, Light.Eyebrow, ZoneID.FrontLeft, 0],
                        'StsOfLedFrntWheelLampRi': [self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, Light.Eyebrow, ZoneID.FrontRight, 0],
                        'StsOfLedReWheelLampLe': [self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, Light.Eyebrow, ZoneID.RearLeft, 0],
                        'StsOfLedReWheelLampRi': [self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, Light.Eyebrow, ZoneID.RearRight, 0],
                        
                        'StsOfLedLeftAIILY1': [self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, Light.AILight, ZoneID.leftY1Sts, 0],
                        'StsOfLedLeftAIILY2': [self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, Light.AILight, ZoneID.leftY2Sts, 0],
                        'StsOfLedLeftAIILY3': [self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, Light.AILight, ZoneID.leftY3Sts, 0],
                        'StsOfLedLeftAIILY4': [self.ipdu.cem_lin2.AIILLCem_Lin2Fr01, Light.AILight, ZoneID.leftY4Sts, 0],
                        'StsOfLedRightAIILY1': [self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, Light.AILight, ZoneID.rightY1Sts, 0],  
                        'StsOfLedRightAIILY2': [self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, Light.AILight, ZoneID.rightY2Sts, 0],  
                        'StsOfLedRightAIILY3': [self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, Light.AILight, ZoneID.rightY3Sts, 0], 
                        'StsOfLedRightAIILY4': [self.ipdu.cem_lin2.AIILRCem_Lin2Fr01, Light.AILight, ZoneID.rightY4Sts, 0],
                        
                        'ExtrLtgStsPosLiFrnt': [self.ipdu.backbonefr.CemBackBoneFr02, Light.Position, ZoneID.Front, 0],
                        'ExtrLtgStsPosLiRe': [self.ipdu.backbonefr.CemBackBoneFr02, Light.Position, ZoneID.Rear, 0],
                        'ExtrLtgStsFlash': [self.ipdu.backbonefr.CemBackBoneFr02, Light.Overtake, ZoneID.AllOrSingle, 0],
                        'ExtrLtgStsReverseLi': [self.ipdu.backbonefr.CemBackBoneFr02, Light.Reverse, ZoneID.AllOrSingle, 0],
                        'ExtrLtgStsStopLi': [self.ipdu.backbonefr.CemBackBoneFr02, Light.Brake, ZoneID.AllOrSingle, 0],
                        'ExtrLtgStsDRL': [self.ipdu.backbonefr.CemBackBoneFr02, Light.Daytime, ZoneID.AllOrSingle, 0],
                        'ExtrLtgStsTurnIndrLe': [self.ipdu.backbonefr.CemBackBoneFr02, Light.Steer, ZoneID.Left, 0],
                        'ExtrLtgStsTurnIndrRi': [self.ipdu.backbonefr.CemBackBoneFr02, Light.Steer, ZoneID.Right, 0],
                        'IndcrDisp': [self.ipdu.backbonefr.CemBackBoneFr06, Light.Hazard, ZoneID.AllOrSingle, 0],
                        
                        'StsOfLedFrntLampLe1': [self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, Light.Pixel, ZoneID.FrontLeft, 0],
                        'StsOfLedFrntLampRi1': [self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, Light.Pixel, ZoneID.FrontRight, 0],
                        'StsOfLedReLampLe2': [self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, Light.Pixel, ZoneID.RearLeft, 0],
                        'StsOfLedReLampRi2': [self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, Light.Pixel, ZoneID.RearRight, 0],
                        
                        'StsOfLedFrntLampMid1': [self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, Light.LightCross, ZoneID.Front, 0],
                        'StsOfLedReLampLe1': [self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, Light.LightCross, ZoneID.RearLeft, 0],
                        'StsOfLedReLampRi1': [self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, Light.LightCross, ZoneID.RearRight, 0],
                        'StsOfLedReLampMid1': [self.ipdu.bodyexposedcanfd.RcmmBodyExpoFr02, Light.LightCross, ZoneID.MiddleRear, 0],
                        
                        'StsOfLedFrntLampLe2': [self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, Light.Didrl, ZoneID.FrontLeft, 0],
                        'StsOfLedFrntLampRi2': [self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, Light.Didrl, ZoneID.FrontRight, 0],
                        
                        # 'StsOfLedFrntWheelLampLe': [self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, Light.LightADS, ZoneID.Left, 0],
                        # 'StsOfLedFrntWheelLampRi': [self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, Light.LightADS, ZoneID.Front, 0],
                        # 'StsOfLedReWheelLampLe': [self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, Light.LightADS, ZoneID.Rear, 0],
                        # 'StsOfLedReWheelLampRi': [self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, Light.LightADS, ZoneID.Right, 0],
                      }

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                            {"adasInfo": [{"zoneId": 14, "mode": 0}]}, timeout=0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 13, "mode": 0}]}, timeout=0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                         {"info": {"cmd": 0, "clientId": 255}})
        super().after_each_func(ecu)

    def set_usage_mode(self, mode):
        """通过模拟mcu cdd打包总线数据来输入usage mode给到S2S"""
        logger.info(f"设置usage mode: {mode}")
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', mode)

    def set_car_mode(self, mode):
        """通过模拟mcu cdd打包总线数据来输入carmode给到S2S"""
        logger.info(f"设置car mode: {mode}")
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', mode)
    
    def set_ReadLiSts_signal(self, FirstRowLe=0, FirstRowRi=0, SecondRowLe=0, SecondRowRi=0,ThirdRowLe=0, ThirdRowRi=0):
        logger.info(f"设置FirstRowLe--{FirstRowLe}")
        self.ipdu.set(self.ipdu.cem_lin3.OhcCem_Lin3Fr01, 'ReadLiStsFirstRowLe', FirstRowLe)
        self.ipdu.set(self.ipdu.cem_lin3.OhcCem_Lin3Fr01, 'ReadLiStsFirstRowRi', FirstRowRi)
        self.ipdu.set(self.ipdu.cem_lin3.OhcCem_Lin3Fr01, 'ReadLiStsSecondRowLe', SecondRowLe)
        self.ipdu.set(self.ipdu.cem_lin3.OhcCem_Lin3Fr01, 'ReadLiStsSecondRowRi', SecondRowRi)
        self.ipdu.set(self.ipdu.cem_lin3.OhcCem_Lin3Fr01, 'ReadLiStsThirdRowLe', ThirdRowLe)
        self.ipdu.set(self.ipdu.cem_lin3.OhcCem_Lin3Fr01, 'ReadLiStsThirdRowRi',ThirdRowRi)
    
    def ck_signal2(self, signals, min_value, exp_max_value):
        find_max_flag = False  # 有没有找到最大值,最大值左边是递增,最大值右边是递减
        assert signals[0] == min_value
        # assert signals[-1] == 0
        max_value = max(signals)
        assert max_value in [exp_max_value, exp_max_value - 1], f"实际最大值{max_value}不符合预期"
        for i in range(len(signals) - 1):
            if signals[i] == max_value:#如果信号=最大值走下坡
                find_max_flag = True
            if signals[i] == min_value:#如果信号=最小值走上坡
                find_max_flag = False
            if find_max_flag:
                assert signals[i] >= signals[i+1]
            else:
                assert signals[i] < signals[i+1]

    def ck_signal3(self, signals, value1, value2):
        for i in range(len(signals)):
            if i % 2==0 :
                assert signals[i] == value1
            else:
                assert signals[i] == value2#校验闪烁灯效

    @allure.title("获取方向盘背光灯功能使能的状态&通知方向盘背光灯功能使能的状态")
    @pytest.mark.sanity
    def test_caseid_111197(self):
        for dcrIllmn in [1, 0]:
            self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', dcrIllmn)
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifySteerWheelBackLightEnableStatus",
                                      {"isEnable": dcrIllmn})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetSteerWheelBackLightEnableStatus", {},
                                                  {"out": dcrIllmn})

    @allure.title("获取方向盘背光灯功能使能的状态&通知方向盘背光灯功能使能的状态_默认值")
    @pytest.mark.full
    def test_caseid_1981768(self):
        for dcrIllmn in [1, 0]:
            self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', dcrIllmn)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetSteerWheelBackLightEnableStatus", {},
                                                {"out": 0})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifySteerWheelBackLightEnableStatus",
                                    {"isEnable": dcrIllmn})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetSteerWheelBackLightEnableStatus", {},
                                                {"out": dcrIllmn})

    @allure.title("获取危险报警灯开关按键状态 &通知危险报警灯开关按键状态")
    @pytest.mark.sanity
    def test_caseid_111124(self):
        for hzrdWarn in [1, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr04, 'SwtLiHzrdWarn', hzrdWarn)
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHazardLightSwitchStatus", {"swtsts": hzrdWarn})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHazardLightSwitchStatus", {},
                                                  {"out": hzrdWarn})

    @allure.title("获取危险报警灯开关按键状态 &通知危险报警灯开关按键状态_默认值")
    @pytest.mark.full
    def test_caseid_1981769(self):
        for hzrdWarn in [1, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr04, 'SwtLiHzrdWarn', hzrdWarn)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHazardLightSwitchStatus", {},
                                                {"out": 0})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyHazardLightSwitchStatus", {"swtsts": hzrdWarn})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHazardLightSwitchStatus", {},
                                                {"out": hzrdWarn})

    @allure.title("查询超车灯状态&通知超车灯状态")
    @pytest.mark.smoke
    def test_caseid_1918541(self):
        self.partner.empty_all(0.5)
        for sts in [1, 2, 3, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFlash', sts)
            sleep(0.5)
            if sts in [1, 2, 0]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                    "sts": {"light": {"type": 32, "zoneId": 0}, "sts": sts, "brightness": 0,
                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                      {"lights": [{"type": 32, "zoneId": 0}]},
                                                      {"out": [{"light": {"type": 32, "zoneId": 0}, "sts": sts,
                                                                "brightness": 0,
                                                                "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            else:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                      {"lights": [{"type": 32, "zoneId": 0}]},
                                                      {"out": [{"light": {"type": 32, "zoneId": 0}, "sts": 2,
                                                                "brightness": 0,
                                                                "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
                
    @allure.title("查询超车灯状态&通知超车灯状态_默认值")
    @pytest.mark.full
    def test_caseid_1983601(self):
        for sts in [2, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFlash', sts)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 32, "zoneId": 0}]},
                                                {"out": [{"light": {"type": 32, "zoneId": 0}, "sts": 0, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                "sts": {"light": {"type": 32, "zoneId": 0}, "sts": sts, "brightness": 0,
                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                    {"lights": [{"type": 32, "zoneId": 0}]},
                                                    {"out": [{"light": {"type": 32, "zoneId": 0}, "sts": sts,
                                                            "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
    
    @allure.title("查询近光灯状态状态&通知近光灯状态")
    @pytest.mark.sanity
    def test_caseid_1918505(self):
        for sLoBeam in [1, 2, 3, 0]:
            logger.info(f"发送信号: {sLoBeam}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsLoBeam', sLoBeam)
            if sLoBeam in [1, 2, 0]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", 
                                        {"sts": {"light": {"type": 6, "zoneId": 0}, "sts": sLoBeam, "brightness": 0, 
                                                "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",{"lights": [{"type": 6, "zoneId": 0}]}, 
                                                    {"out": [{"light": {"type": 6, "zoneId": 0}, "sts": sLoBeam, 
                                                                "brightness": 0,"color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            else:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",{"lights": [{"type": 6, "zoneId": 0}]}, 
                                                    {"out": [{"light": {"type": 6, "zoneId": 0}, "sts": 2, 
                                                                "brightness": 0,"color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
    
    @allure.title("查询近光灯状态状态&通知近光灯状态_默认值")
    @pytest.mark.full
    def test_caseid_1983949(self):
        for sLoBeam in [1, 0]:
            logger.info(f"发送信号: {sLoBeam}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsLoBeam', sLoBeam)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",{"lights": [{"type": 6, "zoneId": 0}]}, 
                                                        {"out": [{"light": {"type": 6, "zoneId": 0}, "sts": 0, 
                                                                    "brightness": 0,"color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", 
                                            {"sts": {"light": {"type": 6, "zoneId": 0}, "sts": sLoBeam, "brightness": 0, 
                                                    "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",{"lights": [{"type": 6, "zoneId": 0}]}, 
                                                        {"out": [{"light": {"type": 6, "zoneId": 0}, "sts": sLoBeam, 
                                                                    "brightness": 0,"color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})

    def update_light_dict_sts(self, signal_name, sts):
        self.light_dict[signal_name][3] = sts

    def update_light_dict_to_venus(self,):
        # venus车型轮眉灯为ADS灯
        self.light_dict['StsOfLedFrntWheelLampLe'] = [self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, Light.LightADS, ZoneID.Left, 0]
        self.light_dict['StsOfLedFrntWheelLampRi'] = [self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, Light.LightADS, ZoneID.Front, 0]
        self.light_dict['StsOfLedReWheelLampLe'] = [self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, Light.LightADS, ZoneID.Rear, 0]
        self.light_dict['StsOfLedReWheelLampRi'] = [self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, Light.LightADS, ZoneID.Right, 0]

    def set_light_dict_ipdu(self, value=0):
        for i in self.light_dict:
            self.light_dict[i][3] = value
            self.ipdu.set(self.light_dict[i][0], i, self.light_dict[i][3])
        sleep(0.5)
    
    def check_ExteriorLightStatusInfo_event(self, timeout=3):
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "ExteriorLightStatusInfo", {"lightStatusInfo": [
                                {"light": {"type": self.light_dict[i][1], "zoneId": self.light_dict[i][2]}, 
                                 "sts": 1 if i == 'IndcrDisp' and self.light_dict[i][3] == 3 else 0 if i == 'IndcrDisp' and self.light_dict[i][3] != 3 else self.light_dict[i][3], 
                                "brightness": 0,"color": {"cRed": 0, "cGreen": 0, "cBlue": 0}} for i in self.light_dict]}, timeout=timeout)

    @allure.title("通知所有外灯状态_单个灯改变_MarsOne") 
    @pytest.mark.sanity
    def test_caseid_1989118(self):
        # 近光灯、雾灯、轮眉灯、AI灯、位置灯、超车灯、倒车灯、制动灯、日间行车灯、转向灯、危险报警灯、Pixel像素灯、一字眉灯、DRL/TI灯
        for i in self.light_dict:
            self.partner.empty_all()

            if i == 'IndcrDisp':
                self.update_light_dict_sts(i, 3)   
            else:
                self.update_light_dict_sts(i, 1)   

            logger.info(f"signal: {i}, info: {self.light_dict[i]}]")
            self.ipdu.set(self.light_dict[i][0], i, self.light_dict[i][3])
            self.check_ExteriorLightStatusInfo_event()

    @allure.title("通知所有外灯状态_全部外灯改变_MarsOne") 
    @pytest.mark.sanity
    def test_caseid_1989119(self):
        for sts in [1, 0, 2, 3]:
            logger.info(f"sts:{sts}")
            
            for i in self.light_dict:
                self.partner.empty_all()

                if i == 'IndcrDisp':
                    self.update_light_dict_sts(i, 3 if sts == 1 else 1 if sts == 3 else sts)   
                else:
                    self.update_light_dict_sts(i, sts)   
                    
                logger.info(f"signal: {i}, info: {self.light_dict[i]}]")
                self.ipdu.set(self.light_dict[i][0], i, self.light_dict[i][3])

            if sts in [0, 1, 2]:
                self.check_ExteriorLightStatusInfo_event()
            else:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "ExteriorLightStatusInfo")

    @allure.title("通知所有外灯状态_重启场景_默认值和非默认值_MarsOne") 
    @pytest.mark.sanity
    def test_caseid_1989120(self):
        for sts in [1, 0]:
            logger.info(f"sts:{sts}")
            self.set_light_dict_ipdu(sts)
            
            if sts == 1:
                self.update_light_dict_sts('IndcrDisp', 3)  
                self.ipdu.set(self.light_dict['IndcrDisp'][0], 'IndcrDisp', self.light_dict['IndcrDisp'][3])
                
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT)
            logger.info(f"restart success...")
            self.check_ExteriorLightStatusInfo_event(timeout=25)
            if sts == 0:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "ExteriorLightStatusInfo")

    @allure.title("通知所有外灯状态_单个灯改变_Venus") 
    @pytest.mark.sanity
    def test_caseid_1989240(self):
        self.write_ccp_by_tcp({950:2})  
        sleep(1)
        self.update_light_dict_to_venus()

        for i in self.light_dict:
            self.partner.empty_all()

            if i == 'IndcrDisp':
                self.update_light_dict_sts(i, 3)   
            else:
                self.update_light_dict_sts(i, 1) 
                  
            logger.info(f"signal: {i}, info: {self.light_dict[i]}]")                
            self.ipdu.set(self.light_dict[i][0], i, self.light_dict[i][3])
            self.check_ExteriorLightStatusInfo_event()

    @allure.title("通知所有外灯状态_全部外灯改变_Venus") 
    @pytest.mark.sanity
    def test_caseid_1989241(self):
        self.write_ccp_by_tcp({950:2})
        sleep(1)
        self.update_light_dict_to_venus()
        
        for sts in [1, 0, 2, 3]:
            logger.info(f"sts:{sts}")
            
            for i in self.light_dict:
                self.partner.empty_all()

                if i == 'IndcrDisp':
                    self.update_light_dict_sts(i, 3 if sts == 1 else 1 if sts == 3 else sts)   
                else:
                    self.update_light_dict_sts(i, sts)   
                    
                logger.info(f"signal: {i}, info: {self.light_dict[i]}]")
                self.ipdu.set(self.light_dict[i][0], i, self.light_dict[i][3])

            if sts in [0, 1, 2]:
                self.check_ExteriorLightStatusInfo_event()
            else:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "ExteriorLightStatusInfo")

    @allure.title("通知所有外灯状态_重启场景_默认值和非默认值_Venus") 
    @pytest.mark.sanity
    def test_caseid_1989242(self):
        self.write_ccp_by_tcp({950:2})  
        sleep(1)
        self.update_light_dict_to_venus()
        
        for sts in [1, 0]:
            logger.info(f"sts:{sts}")
            self.set_light_dict_ipdu(sts)
            
            if sts == 1:
                self.update_light_dict_sts('IndcrDisp', 3)  
                self.ipdu.set(self.light_dict['IndcrDisp'][0], 'IndcrDisp', self.light_dict['IndcrDisp'][3])
                
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT)
            logger.info(f"restart success...")
            self.check_ExteriorLightStatusInfo_event(timeout=25)
            if sts == 0:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "ExteriorLightStatusInfo")

    # @allure.title("通知所有外灯状态_非外灯状态改变不上报事件") 
    # @pytest.mark.sanity
    # def test_caseid_temp(self):
    #     self.partner.empty_all(0.5)
    #     # 大灯水平高度调节状态
    #     self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsAHL', 1)     
    #     # 内灯背光亮度等级
    #     self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'IntrBriSts', 1)              
    #     # 阅读灯
    #     self.ipdu.set(self.ipdu.cem_lin3.OhcCem_Lin3Fr01, 'ReadLiStsFirstRowLe', 1)
    #     self.ipdu.set(self.ipdu.cem_lin3.OhcCem_Lin3Fr01, 'ReadLiStsFirstRowRi', 1)
    #     self.ipdu.set(self.ipdu.cem_lin3.OhcCem_Lin3Fr01, 'ReadLiStsSecondRowLe', 1)
    #     self.ipdu.set(self.ipdu.cem_lin3.OhcCem_Lin3Fr01, 'ReadLiStsSecondRowRi', 1)
    #     self.ipdu.set(self.ipdu.cem_lin3.OhcCem_Lin3Fr01, 'ReadLiStsThirdRowLe', 1)
    #     self.ipdu.set(self.ipdu.cem_lin3.OhcCem_Lin3Fr01, 'ReadLiStsThirdRowRi', 1)
    #     # 照脚灯
    #     self.bgm_eth_inter.set_signal("StsOfLedFootwellLightFrntLe", 1)
    #     self.bgm_eth_inter.set_signal("StsOfLedFootwellLightFrntRi", 1)
    #     sleep(0.5)
    #     self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "ExteriorLightStatusInfo")

    @allure.title("查询雾灯状态&通知雾灯状态")  # 前后雾灯
    @pytest.mark.smoke
    def test_caseid_1983492(self):
        self.partner.empty_all(0.5)
        for FrntFogTBD in [1, 2, 0, 3]:
            logger.info(f"发送信号: {FrntFogTBD}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFrntFogTBD', FrntFogTBD)  # 前雾灯
            sleep(0.5)
            if FrntFogTBD in [1, 2, 0]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                    "sts": {"light": {"type": 4, "zoneId": 9}, "sts": FrntFogTBD, "brightness": 0,
                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                      {"lights": [{"type": 4, "zoneId": 9}]},
                                                      {"out": [{"light": {"type": 4, "zoneId": 9}, "sts": FrntFogTBD,
                                                                "brightness": 0,
                                                                "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            else:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                      {"lights": [{"type": 4, "zoneId": 9}]},
                                                      {"out": [
                                                          {"light": {"type": 4, "zoneId": 9}, "sts": 0, "brightness": 0,
                                                           "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        for ReFog in [1, 2, 0, 3]:
            logger.info(f"发送信号: {ReFog}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', ReFog)  # 后雾灯
            sleep(0.5)
            if ReFog in [1, 2, 0]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                    "sts": {"light": {"type": 4, "zoneId": 10}, "sts": ReFog, "brightness": 0,
                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                      {"lights": [{"type": 4, "zoneId": 10}]},
                                                      {"out": [{"light": {"type": 4, "zoneId": 10}, "sts": ReFog,
                                                                "brightness": 0,
                                                                "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            else:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                      {"lights": [{"type": 4, "zoneId": 10}]},
                                                      {"out": [{"light": {"type": 4, "zoneId": 10}, "sts": 0,
                                                                "brightness": 0,
                                                                "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})

    @allure.title("查询雾灯状态&通知雾灯状态_默认值")  # 前雾灯
    @pytest.mark.full
    def test_caseid_1983493(self):
        for sts in [1, 0]:
            logger.info(f"sts:{sts}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFrntFogTBD', sts)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 4, "zoneId": 9}]},
                                                {"out": [{"light": {"type": 4, "zoneId": 9}, "sts": 0, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 4, "zoneId": 9},
                                            "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 4, "zoneId": 9}]},
                                                {"out": [{"light": {"type": 4, "zoneId": 9}, "sts": sts, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
    
    @allure.title("查询雾灯状态&通知雾灯状态_默认值")  # 后雾灯
    @pytest.mark.full
    def test_caseid_1983494(self):
        for sts in [1, 0]:
            logger.info(f"sts:{sts}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', sts)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 4, "zoneId": 10}]},
                                                {"out": [{"light": {"type": 4, "zoneId": 10}, "sts": 0, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 4, "zoneId": 10},
                                            "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 4, "zoneId": 10}]},
                                                {"out": [{"light": {"type": 4, "zoneId": 10}, "sts": sts, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
    
    @allure.title("查询位置灯状态&通知位置灯状态")
    @pytest.mark.sanity
    def test_caseid_111180(self):
        last_value = -1     
        dic = {"Frnt": 9, "Re": 10}
        for sig, sts in dic.items():
            for send_value in [1, 2, 3, 0]:
                logger.info(f"发送信号: {send_value},当前灯.{sig}")
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, f'ExtrLtgStsPosLi{sig}', send_value)
                if send_value in [1, 2, 0]:
                    self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 11, "zoneId": sts},
                                        "sts":send_value, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                    self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                        {"lights": [{"type": 11, "zoneId":sts }]},
                                            {"out":[{"light":{"type":11,"zoneId":sts},"sts":send_value,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})
                    last_value = send_value
                else:
                    self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                    self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                        {"lights": [{"type": 11, "zoneId":sts }]},
                                            {"out":[{"light":{"type":11,"zoneId":sts},"sts":last_value,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})
    
    @allure.title("查询位置灯状态&通知位置灯状态_默认值")#前位置灯
    @pytest.mark.full
    def test_caseid_1918533(self):
        for sts in [1, 0]:
            logger.info(f"sts:{sts}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt', sts)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 11, "zoneId": 9}]},
                                                {"out": [{"light": {"type": 11, "zoneId": 9}, "sts": 0, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 11, "zoneId": 9},
                                            "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 11, "zoneId": 9}]},
                                                {"out": [{"light": {"type": 11, "zoneId": 9}, "sts": sts, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
    
    @allure.title("查询位置灯状态&通知位置灯状态_默认值")#后位置灯
    @pytest.mark.full
    def test_caseid_1919345(self):
        for sts in [1, 0]:
            logger.info(f"sts:{sts}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiRe', sts)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 11, "zoneId": 10}]},
                                                {"out": [{"light": {"type": 11, "zoneId": 10}, "sts": 0, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 11, "zoneId": 10},
                                            "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 11, "zoneId": 10}]},
                                                {"out": [{"light": {"type": 11, "zoneId": 10}, "sts": sts, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
    
    @allure.title("查询大灯水平高度调节(功能激活)(AHL)状态&通知大灯水平高度调节(功能激活)(AHL)状态")
    @pytest.mark.sanity
    def test_caseid_1983599(self):
        for sts in [1, 2, 3, 0] :
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsAHL', sts)
            if sts in [1, 2, 0]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 37, "zoneId": 0},
                                            "sts":sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                            {"lights": [{"type": 37, "zoneId": 0}]},
                                                {"out":[{"light":{"type":37,"zoneId":0},"sts":sts,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})
            else:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                        {"lights": [{"type": 37, "zoneId":0 }]},
                                            {"out":[{"light":{"type":37,"zoneId":0},"sts":2,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})
    
    @allure.title("查询大灯水平高度调节(功能激活)(AHL)状态&通知大灯水平高度调节(功能激活)(AHL)状态_默认值")
    @pytest.mark.full
    def test_caseid_1983600(self):
        for sts in [1, 0] :
            logger.info(f"sts:{sts}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsAHL', sts)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 37, "zoneId": 0}]},
                                                {"out": [{"light": {"type": 37, "zoneId": 0}, "sts": 0, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 37, "zoneId": 0},
                                            "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 37, "zoneId": 0}]},
                                                {"out": [{"light": {"type": 37, "zoneId": 0}, "sts": sts, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]}) 

    @allure.title("查询倒车灯状态&通知倒车灯状态")
    @pytest.mark.sanity
    def test_caseid_1918552(self):
        for seli in [1, 2, 3, 0]:
            logger.info(f"发送信号: {seli}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReverseLi', seli)
            if seli in [1, 2, 0]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                    "sts": {"light": {"type": 8, "zoneId": 0}, "sts": seli, "brightness": 0,
                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 8, "zoneId": 0}]},
                                                    {"out": [{"light": {"type": 8, "zoneId": 0}, "sts": seli, "brightness": 0,
                                                                "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            else:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                        {"lights": [{"type": 8, "zoneId":0 }]},
                                            {"out":[{"light":{"type":8,"zoneId":0},"sts":2,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})
    
    @allure.title("查询倒车灯状态&通知倒车灯状态_默认值")
    @pytest.mark.full
    def test_caseid_1919346(self):
        for sts in [1, 0]:
            logger.info(f"sts:{sts}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReverseLi', sts)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 8, "zoneId": 0}]},
                                                {"out": [{"light": {"type": 8, "zoneId": 0}, "sts": 0,
                                                        "brightness": 0, "color": {"cRed": 0, "cGreen": 0,
                                                                                    "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 8, "zoneId": 0},
                                            "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 8, "zoneId": 0}]},
                                                {"out": [{"light": {"type": 8, "zoneId": 0}, "sts": sts, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
    
    @allure.title("查询制动灯状态&通知制动灯状态")
    @pytest.mark.smoke
    def test_caseid_1918550(self):
        for topLi in [1, 2, 3, 0]:
            logger.info(f"发送信号: {topLi}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', topLi)
            if topLi in [1, 2, 0]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                    "sts": {"light": {"type": 0, "zoneId": 0}, "sts": topLi, "brightness": 0,
                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                    {"lights": [{"type": 0, "zoneId": 0}]}, {"out": [
                        {"light": {"type": 0, "zoneId": 0}, "sts": topLi, "brightness": 0,
                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            else:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                        {"lights": [{"type": 0, "zoneId":0 }]},
                                            {"out":[{"light":{"type":0,"zoneId":0},"sts":2,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})
    
    @allure.title("查询制动灯状态&通知制动灯状态_默认值")
    @pytest.mark.full
    def test_caseid_1983602(self):
        for sts in [1, 0]:
            logger.info(f"sts:{sts}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', sts)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 0, "zoneId": 0}]},
                                                {"out": [{"light": {"type": 0, "zoneId": 0}, "sts": 0,
                                                        "brightness": 0, "color": {"cRed": 0, "cGreen": 0,
                                                                                    "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 0, "zoneId": 0},
                                            "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 0, "zoneId": 0}]},
                                                {"out": [{"light": {"type": 0, "zoneId": 0}, "sts": sts, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
    
    @allure.title("查询日间行车灯状态&通知日间行车灯状态 ")
    @pytest.mark.smoke
    def test_caseid_1918511(self):
        for StsDRL in [1, 2, 3, 0]:
            logger.info(f"发送信号: {StsDRL}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsDRL', StsDRL)
            sleep(0.5)
            if StsDRL in [1, 2, 0]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {
                    "sts": {"light": {"type": 3, "zoneId": 0}, "sts": StsDRL, "brightness": 0,
                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                    {"lights": [{"type": 3, "zoneId": 0}]}, {"out": [
                        {"light": {"type": 3, "zoneId": 0}, "sts": StsDRL, "brightness": 0,
                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            else:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                        {"lights": [{"type": 3, "zoneId":0 }]},
                                            {"out":[{"light":{"type":3,"zoneId":0},"sts":2,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})
    
    @allure.title("查询日间行车灯状态&通知日间行车灯状态_默认值")
    @pytest.mark.full
    def test_caseid_1983603(self):
        for sts in [1, 0]:
            logger.info(f"sts:{sts}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsDRL', sts)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 3, "zoneId": 0}]},
                                                {"out": [{"light": {"type": 3, "zoneId": 0}, "sts": 0,
                                                        "brightness": 0, "color": {"cRed": 0, "cGreen": 0,
                                                                                    "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 3, "zoneId": 0},
                                            "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 3, "zoneId": 0}]},
                                                {"out": [{"light": {"type": 3, "zoneId": 0}, "sts": sts, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
    
    @allure.title("查询转向灯状态&通知转向灯状态")
    @pytest.mark.smoke
    def test_caseid_1983607(self):
        last_value = -1     
        dic = {"Le": 12, "Ri": 13}
        for sig, sts in dic.items():
            for send_value in [1, 2, 3, 0]:
                logger.info(f"发送信号: {send_value},当前灯.{sig}")
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, f'ExtrLtgStsTurnIndr{sig}', send_value)
                if send_value in [1, 2, 0]:
                    self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 10, "zoneId": sts},
                                        "sts":send_value, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
                    self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                        {"lights": [{"type": 10, "zoneId":sts }]},
                                            {"out":[{"light":{"type":10,"zoneId":sts},"sts":send_value,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})
                    last_value = send_value
                else:
                    self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
                    self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                        {"lights": [{"type": 10, "zoneId":sts }]},
                                            {"out":[{"light":{"type":10,"zoneId":sts},"sts":last_value,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})
    
    @allure.title("查询转向灯状态&通知转向灯状态_默认值")
    @pytest.mark.full
    def test_caseid_1983610(self):
        for sts in [1, 0]:
            logger.info(f"sts:{sts}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', sts)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', sts)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 10, "zoneId": 0}]},
                                                {"out": [{"light": {"type": 10, "zoneId": 12}, "sts": 0,
                                                        "brightness": 0, "color": {"cRed": 0, "cGreen": 0,
                                                                                    "cBlue": 0}}, {"light": {"type": 10, "zoneId": 12}, "sts": 0,
                                                        "brightness": 0, "color": {"cRed": 0, "cGreen": 0,
                                                                                    "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 10, "zoneId": 12},
                                            "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 10, "zoneId": 12}]},
                                                {"out": [{"light": {"type": 10, "zoneId": 12}, "sts": sts, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 10, "zoneId": 13},
                                            "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 10, "zoneId": 13}]},
                                                {"out": [{"light": {"type": 10, "zoneId": 13}, "sts": sts, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
    
    @allure.title("查询危险报警灯状态&通知危险报警灯状态")
    @pytest.mark.sanity
    def test_caseid_111191(self):
        for Disp in [3, 1, 3, 2, 3, 0]:
            logger.info(f"发送信号: {Disp}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', Disp)
            sleep(0.5) 
            if  Disp in [3]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 2, "zoneId": 0},
                                                                                    "sts": 1, "brightness": 0,
                                                                                    "color": {"cRed": 0, "cGreen": 0,
                                                                                                "cBlue": 0}}})
                self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 2, "zoneId": 0}]},
                                                    {"out": {"light": {"type": 2, "zoneId": 0}, "sts": 1,
                                                            "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            else :
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 2, "zoneId": 0},
                                                                                "sts": 0, "brightness": 0,
                                                                                "color": {"cRed": 0, "cGreen": 0,
                                                                                            "cBlue": 0}}})
                self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 2, "zoneId": 0}]},
                                                    {"out": {"light": {"type": 2, "zoneId": 0}, "sts": 0,
                                                            "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})

    @allure.title("查询危险报警灯状态&通知危险报警灯状态_默认值")
    @pytest.mark.full
    def test_caseid_1983611(self):
        for sts in [3, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', sts) 
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 2, "zoneId": 0}]},
                                                {"out": [{"light": {"type": 2, "zoneId": 0}, "sts": 0, "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            if  sts in [3]:
                    self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 2, "zoneId": 0},
                                                                                        "sts": 1, "brightness": 0,
                                                                                        "color": {"cRed": 0, "cGreen": 0,
                                                                                                    "cBlue": 0}}})
                    self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 2, "zoneId": 0}]},
                                                        {"out": {"light": {"type": 2, "zoneId": 0}, "sts": 1,
                                                                "brightness": 0,
                                                                "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            else :
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 2, "zoneId": 0},
                                                                                "sts": 0, "brightness": 0,
                                                                                "color": {"cRed": 0, "cGreen": 0,
                                                                                            "cBlue": 0}}})
                self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 2, "zoneId": 0}]},
                                                    {"out": {"light": {"type": 2, "zoneId": 0}, "sts": 0,
                                                            "brightness": 0,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
    
    @allure.title("查询阅读灯状态&通知阅读灯状态")
    @pytest.mark.sanity
    def test_caseid_1983637(self):
        self.set_ReadLiSts_signal(0, 0, 0, 0, 0, 0)
        self.partner.empty_all(0.5) 
        for Le in [1, 0]:
            self.set_ReadLiSts_signal(FirstRowLe=Le)
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                  {"sts": {"light": {"type": 22, "zoneId": 1},
                                           "sts": Le, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                              {"lights": [{"type": 22, "zoneId": 1}]},
                                              {"out": [{"light": {"type": 22, "zoneId": 1}, "sts": Le, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})   
        for Ri in [1, 0]:
            self.set_ReadLiSts_signal(FirstRowRi=Ri)
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 22, "zoneId": 2},
                                            "sts": Ri, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 22, "zoneId": 2}]},
                                                {"out": [{"light": {"type": 22, "zoneId": 2}, "sts": Ri, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})   
        for L in [1, 0]:
            self.set_ReadLiSts_signal(SecondRowLe=L)
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 22, "zoneId": 3},
                                            "sts": L, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 22, "zoneId": 3}]},
                                                {"out": [{"light": {"type": 22, "zoneId": 3}, "sts": L, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})   
        for R in [1, 0]:
            self.set_ReadLiSts_signal(SecondRowRi=R)
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 22, "zoneId": 4},
                                            "sts": R, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 22, "zoneId": 4}]},
                                                {"out": [{"light": {"type": 22, "zoneId": 4}, "sts": R, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})   
        for thirdRowLe in [1, 0]:
            self.set_ReadLiSts_signal(ThirdRowLe=thirdRowLe)
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 22, "zoneId": 6},
                                            "sts": thirdRowLe, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 22, "zoneId": 6}]},
                                                {"out": [{"light": {"type": 22, "zoneId": 6}, "sts": thirdRowLe, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})  
        for thirdRowRe in [1, 0]:
            self.set_ReadLiSts_signal(ThirdRowRi=thirdRowRe)
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 22, "zoneId": 7},
                                            "sts": thirdRowRe, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 22, "zoneId": 7}]},
                                                {"out": [{"light": {"type": 22, "zoneId": 7}, "sts": thirdRowRe, "brightness": 0,
                                                        "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})   
    
    @allure.title("查询阅读灯状态&通知阅读灯状态_全部开关")
    @pytest.mark.full
    def test_caseid_1983640(self):
        self.set_ReadLiSts_signal(0, 0, 0, 0, 0, 0)
        self.partner.empty_all(0.5) 
        self.set_ReadLiSts_signal(1, 1, 1, 1, 1, 1)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                {"sts": {"light": {"type": 22, "zoneId": 1},
                                        "sts": 1, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                {"sts": {"light": {"type": 22, "zoneId": 2},
                                        "sts": 1, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                {"sts": {"light": {"type": 22, "zoneId": 3},
                                        "sts": 1, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                {"sts": {"light": {"type": 22, "zoneId": 4},
                                        "sts": 1, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                {"sts": {"light": {"type": 22, "zoneId": 6},
                                        "sts": 1, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                {"sts": {"light": {"type": 22, "zoneId": 7},
                                        "sts": 1, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                            {"lights": [{"type": 22, "zoneId": 0}]},
                                            {"out":[{"light":{"type":22,"zoneId":1},"sts":1,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                    {"light":{"type":22,"zoneId":2},"sts":1,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                    {"light":{"type":22,"zoneId":3},"sts":1,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                    {"light":{"type":22,"zoneId":4},"sts":1,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                    {"light":{"type":22,"zoneId":6},"sts":1,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                    {"light":{"type":22,"zoneId":7},"sts":1,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})   
        self.set_ReadLiSts_signal(0, 0, 0, 0, 0, 0)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                {"sts": {"light": {"type": 22, "zoneId": 1},
                                        "sts": 0, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                {"sts": {"light": {"type": 22, "zoneId": 2},
                                        "sts": 0, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                {"sts": {"light": {"type": 22, "zoneId": 3},
                                        "sts": 0, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                {"sts": {"light": {"type": 22, "zoneId": 4},
                                        "sts": 0, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                {"sts": {"light": {"type": 22, "zoneId": 6},
                                        "sts": 0, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                {"sts": {"light": {"type": 22, "zoneId": 7},
                                        "sts": 0, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                            {"lights": [{"type": 22, "zoneId": 0}]},
                                            {"out":[{"light":{"type":22,"zoneId":1},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                    {"light":{"type":22,"zoneId":2},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                    {"light":{"type":22,"zoneId":3},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                    {"light":{"type":22,"zoneId":4},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                    {"light":{"type":22,"zoneId":6},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                    {"light":{"type":22,"zoneId":7},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]}) 
    
    @allure.title("查询阅读灯状态&通知阅读灯状态_默认值")
    @pytest.mark.full
    def test_caseid_1983641(self):
        for sts in [0, 1]:
            logger.info(f"sts:{sts}")
            self.set_ReadLiSts_signal(sts, sts, sts, sts, sts, sts)  
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 22, "zoneId": 0}]},
                                                {"out":[{"light":{"type":22,"zoneId":1},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":22,"zoneId":2},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":22,"zoneId":3},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":22,"zoneId":4},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":22,"zoneId":6},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":22,"zoneId":7},"sts":0,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})  
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 22, "zoneId": 1},
                                            "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 22, "zoneId": 2},
                                            "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 22, "zoneId": 3},
                                            "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 22, "zoneId": 4},
                                            "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 22, "zoneId": 6},
                                            "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                    {"sts": {"light": {"type": 22, "zoneId": 7},
                                            "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 22, "zoneId": 0}]},
                                                {"out":[{"light":{"type":22,"zoneId":1},"sts":sts,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":22,"zoneId":2},"sts":sts,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":22,"zoneId":3},"sts":sts,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":22,"zoneId":4},"sts":sts,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":22,"zoneId":6},"sts":sts,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}},
                                                        {"light":{"type":22,"zoneId":7},"sts":sts,"brightness":0,"color":{"cRed":0,"cGreen":0,"cBlue":0}}]})   
        self.set_ReadLiSts_signal(0, 0, 0, 0, 0, 0) 

    def ck_event_and_status(self, light, zoneid, sts, ck_event=True):
        if ck_event:
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status",
                                        {"sts": {"light": {"type": light, "zoneId": zoneid},
                                        "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
        else:
            self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "Status")
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": light, "zoneId": zoneid}]},
                                        {"out": [{"light": {"type": light, "zoneId": zoneid}, 
                                        "sts": sts, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})                    

    @allure.title("照脚灯_通知查询状态-左前(zoneId=1)/右前(zoneId=2)")
    @pytest.mark.sanity
    def test_caseid_1988976(self):
        for i in [2, 0, 1, 3]:
            logger.info(f"sts:{i}")
            sts = 1 if i == 3 else i
            ck_event = False if i == 3 else True
            self.partner.empty_all()
            
            self.bgm_eth_inter.set_signal("StsOfLedFootwellLightFrntLe", i, send_pdu_immediately=True)
            sleep(0.5)
            self.bgm_eth_inter.set_signal("StsOfLedFootwellLightFrntRi", i, send_pdu_immediately=True)
            self.ck_event_and_status(Light.Foot, ZoneID.FrontLeft, sts, ck_event)
            self.ck_event_and_status(Light.Foot, ZoneID.FrontRight, sts, ck_event)

    @allure.title("照脚灯_通知查询状态_左前/右前同时查询(zoneId=0)")
    @pytest.mark.full
    def test_caseid_1988977(self):
        self.bgm_eth_inter.set_signal("StsOfLedFootwellLightFrntLe", 1, send_pdu_immediately=True)
        sleep(0.5)
        self.bgm_eth_inter.set_signal("StsOfLedFootwellLightFrntRi", 1, send_pdu_immediately=True)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": Light.Foot, "zoneId": ZoneID.AllOrSingle}]},
                                        {"out": [{"light": {"type": Light.Foot, "zoneId": ZoneID.FrontLeft}, 
                                         "sts": 1, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}},
                                                 {"light": {"type": Light.Foot, "zoneId": ZoneID.FrontRight}, 
                                         "sts": 1, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})       
        
        self.bgm_eth_inter.set_signal("StsOfLedFootwellLightFrntLe", 1, send_pdu_immediately=True)
        sleep(0.5)
        self.bgm_eth_inter.set_signal("StsOfLedFootwellLightFrntRi", 0, send_pdu_immediately=True)
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": Light.Foot, "zoneId": ZoneID.AllOrSingle}]},
                                        {"out": [{"light": {"type": Light.Foot, "zoneId": ZoneID.FrontLeft}, 
                                         "sts": 1, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}},
                                                 {"light": {"type": Light.Foot, "zoneId": ZoneID.FrontRight}, 
                                         "sts": 0, "brightness": 0, "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})   

    @allure.title("照脚灯_通知查询状态_重启场景（默认值和非默认值）")
    @pytest.mark.full
    def test_caseid_1988978(self):
        for i in [0, 1]:
            logger.info(f"sts:{i}")
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT)
            sleep(5)
            self.bgm_eth_inter.set_signal("StsOfLedFootwellLightFrntLe", i, send_pdu_immediately=True)
            sleep(0.5)
            self.bgm_eth_inter.set_signal("StsOfLedFootwellLightFrntRi", i, send_pdu_immediately=True)
            self.ck_event_and_status(Light.Foot, ZoneID.FrontLeft, i)
            self.ck_event_and_status(Light.Foot, ZoneID.FrontRight, i)
    
    @allure.title("查询内灯背光亮度状态&通知内灯背光亮度状态")
    @pytest.mark.sanity
    def test_caseid_1983645(self):
        for sts in [1, 7, 15, 0]:
            logger.info(f"发送信号: {sts}")
            self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'IntrBriSts', sts)
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 23, "zoneId": 0},"brightness": sts,
                                                                                    "color": {"cRed": 0, "cGreen": 0,
                                                                                                "cBlue": 0}}})
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "GetStatus", {"lights": [{"type": 23, "zoneId": 0}]},
                                                    {"out": {"light": {"type": 23, "zoneId": 0}, "brightness": sts,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}})
    
    @allure.title("查询内灯背光亮度状态&通知内灯背光亮度状态_默认值")
    @pytest.mark.full
    def test_caseid_1983165(self):
        for sts in [11, 0]:
            logger.info(f"sts:{sts}")
            self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'IntrBriSts', sts)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 23, "zoneId": 0}]},
                                                {"out": [{"light": {"type": 23, "zoneId": 0}, "sts": 1, "brightness": 11,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
            self.ipdu.resume_all_bus_send()
            sleep(0.5)
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "Status", {"sts": {"light": {"type": 23, "zoneId": 0},"sts": 1, "brightness": sts,
                                                                                        "color": {"cRed": 0, "cGreen": 0,
                                                                                                    "cBlue": 0}}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetStatus",
                                                {"lights": [{"type": 23, "zoneId": 0}]},
                                                {"out": [{"light": {"type": 23, "zoneId": 0}, "sts": 1, "brightness": sts,
                                                            "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
    
    @allure.title("获取近光灯故障状态&通知近光灯故障状态")
    @pytest.mark.smoke
    def test_caseid_111164(self):
        for LoBeam in [2, 1, 2, 3, 0]:
            logger.info(f"发送信号: {LoBeam}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsLoBeam', LoBeam)
            if LoBeam in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 1, "faultMsg": "","light": {"type": 6,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 6, "zoneId": 0}}]})
            elif LoBeam in [3]:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "LightFault")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 6, "zoneId": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [ {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
    
    @allure.title("获取近光灯故障状态&通知近光灯故障状态_默认值")
    @pytest.mark.full
    def test_caseid_1983948(self):
        for LoBeam in [2, 0]:
            logger.info(f"发送信号: {LoBeam}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsLoBeam', LoBeam)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                        {"out": [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
            self.ipdu.resume_all_bus_send()
            if LoBeam in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 1, "faultMsg": "","light": {"type": 6,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 6, "zoneId": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [ {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
    
    @allure.title("获取远光灯故障状态&通知远光灯故障状态")
    @pytest.mark.sanity
    def test_caseid_111228(self):
        for sHiBeam in [2, 1, 2, 3, 0]:
            logger.info(f"发送信号: {sHiBeam}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', sHiBeam)
            if sHiBeam in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 1, "faultMsg": "","light": {"type": 5,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 5, "zoneId": 0}}]})
            elif sHiBeam in [3]:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "LightFault")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 5, "zoneId": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
    
    @allure.title("获取远光灯故障状态&通知远光灯故障状态_默认值")
    @pytest.mark.full
    def test_caseid_1983950(self):
        for sHiBeam in [2, 0]:
            logger.info(f"发送信号: {sHiBeam}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', sHiBeam)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                        {"out": [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
            self.ipdu.resume_all_bus_send()
            if sHiBeam in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 1, "faultMsg": "","light": {"type": 5,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 5, "zoneId": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
    
    @allure.title("获取雾灯故障状态&通知雾灯故障状态_单个雾灯")
    @pytest.mark.sanity
    def test_caseid_111143(self):
        for FogTBD in [2, 1, 2, 3, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFrntFogTBD', FogTBD)
            if FogTBD in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault",
                                  {"faults": [{"fault": 1, "faultMsg": "", "light": {"type": 4, "zoneId": 9}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {}, 
                                              {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 4, "zoneId": 9}}]})
            elif FogTBD in [3]:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "LightFault")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {}, 
                                              {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 4, "zoneId": 9}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [ {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
        for ReFog in [2, 1, 2, 3, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', ReFog)
            if ReFog in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault",
                                  {"faults": [{"fault": 1, "faultMsg": "", "light": {"type": 4, "zoneId": 10}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {}, 
                                              {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 4, "zoneId": 10}}]})
            elif ReFog in [3]:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "LightFault")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {}, 
                                              {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 4, "zoneId": 10}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [ {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
    
    @allure.title("获取雾灯故障状态&通知雾灯故障状态_全部雾灯")
    @pytest.mark.sanity
    def test_caseid_1983953(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFrntFogTBD', 2)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault",
                                  {"faults": [{"fault": 1, "faultMsg": "", "light": {"type": 4, "zoneId": 9}}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 2)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault",
                                  {"faults": [{"fault": 1, "faultMsg": "", "light": {"type": 4, "zoneId": 10}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 4, "zoneId": 9}},
                                                       {"fault": 1, "faultMsg": "","light": {"type": 4, "zoneId": 10}}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFrntFogTBD', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', 0)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [ {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})

    @allure.title("获取雾灯故障状态&通知雾灯故障状态_默认值")
    @pytest.mark.full
    def test_caseid_1983954(self):
        for sts in [2, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFrntFogTBD', sts)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', sts)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                        {"out": [ {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
            self.ipdu.resume_all_bus_send()
            if sts in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", {"faults": 
                                                    [{"fault": 1, "faultMsg": "", "light": {"type": 4, "zoneId": 9}},
                                                     {"fault": 1, "faultMsg": "", "light": {"type": 4, "zoneId": 10}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {}, {"out": 
                                                    [{"fault": 1, "faultMsg": "", "light": {"type": 4, "zoneId": 9}},
                                                     {"fault": 1, "faultMsg": "", "light": {"type": 4, "zoneId": 10}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", {"faults": 
                                                    [{"fault": 0, "faultMsg": "", "light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {}, {"out": 
                                                    [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
    
    @allure.title("获取位置灯故障状态&通知位置灯故障状态")
    @pytest.mark.smoke
    def test_caseid_111144(self):
        for lifrnt in [2, 1, 2, 3, 0]:
            logger.info(f"发送信号: {lifrnt}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt', lifrnt)  # 前位置灯
            if lifrnt in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults":[{"fault": 1, "faultMsg": "","light": {"type": 11,"zoneId": 9}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                      {"out": [{"fault": 1, "faultMsg": "","light": {"type": 11, "zoneId": 9}}]})
            elif lifrnt in [3]:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "LightFault")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {}, 
                                              {"out": [{"fault": 1, "faultMsg": "","light": {"type": 11, "zoneId": 9}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [ {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
        for lire in [2, 1, 2, 3, 0]:
            logger.info(f"发送信号: {lire}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiRe', lire)  # 后位置灯
            sleep(0.5)
            if lire in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault",
                                          {"faults":[{"fault": 1, "faultMsg": "","light": {"type": 11,"zoneId": 10}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                      {"out": [{"fault": 1, "faultMsg": "","light": {"type": 11, "zoneId": 10}}]})
            elif lire in [3]:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "LightFault")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {}, 
                                              {"out": [{"fault": 1, "faultMsg": "","light": {"type": 11, "zoneId": 10}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [ {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt', 2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiRe', 2)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                  {"faults":[{"fault": 1, "faultMsg": "","light": {"type": 11, "zoneId": 9}},
                                             {"fault": 1, "faultMsg": "","light": {"type": 11, "zoneId": 10}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 11, "zoneId": 9}},
                                                       {"fault": 1, "faultMsg": "","light": {"type": 11, "zoneId": 10}}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiRe', 0)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault",
                                  {"faults": [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
    
    @allure.title("获取位置灯故障状态&通知位置灯故障状态_默认值")
    @pytest.mark.full
    def test_caseid_1983974(self):
        for sts in [2, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt', sts)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiRe', sts)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                        {"out": [ {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
            self.ipdu.resume_all_bus_send()
            if sts in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", {"faults": [
                                                    {"fault": 1, "faultMsg": "", "light": {"type": 11, "zoneId": 9}},
                                                    {"fault": 1, "faultMsg": "", "light": {"type": 11, "zoneId": 10}}]})

                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {}, {"out": [
                                                    {"fault": 1, "faultMsg": "", "light": {"type": 11, "zoneId": 9}},
                                                    {"fault": 1, "faultMsg": "", "light": {"type": 11, "zoneId": 10}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [ {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
    
    @allure.title("获取自适应前照灯系统(功能激活)(AFS)故障状态&通知自适应前照灯系统(功能激活)(AFS)故障状态")
    @pytest.mark.smoke
    def test_caseid_1983345(self):
        for AFSTBD in [2, 1, 2, 3, 0]:
            logger.info(f"发送信号: {AFSTBD}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsAFSTBD', AFSTBD)
            if AFSTBD in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 1, "faultMsg": "","light": {"type": 36,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 36, "zoneId": 0}}]})
            elif AFSTBD in [3]:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "LightFault")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 36, "zoneId": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
    
    @allure.title("获取自适应前照灯系统(功能激活)(AFS)故障状态&通知自适应前照灯系统(功能激活)(AFS)故障状态_默认值")
    @pytest.mark.full
    def test_caseid_1983975(self):
        for AFSTBD in [2, 0]:
            logger.info(f"发送信号: {AFSTBD}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsAFSTBD', AFSTBD)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                        {"out": [ {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
            self.ipdu.resume_all_bus_send()
            if AFSTBD in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 1, "faultMsg": "","light": {"type": 36,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 36, "zoneId": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
    
    @allure.title("获取大灯水平高度调节(AHL)故障状态&通知大灯水平高度调节(AHL)故障状态")
    @pytest.mark.sanity
    def test_caseid_111210(self):
        for AHL in [2, 1, 2, 3, 0]:
            logger.info(f"发送信号: {AHL}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsAHL', AHL)
            if AHL in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                      {"faults": [{"fault": 1, "faultMsg": "","light": {"type": 37,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 37, "zoneId": 0}}]})
            elif AHL in [3]:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "LightFault")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 37, "zoneId": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
    
    @allure.title("获取大灯水平高度调节(AHL)故障状态&通知大灯水平高度调节(AHL)故障状态_默认值")
    @pytest.mark.full
    def test_caseid_1983976(self):
        for AHL in [2, 0]:
            logger.info(f"发送信号: {AHL}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsAHL', AHL)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                        {"out": [ {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
            self.ipdu.resume_all_bus_send()
            if AHL in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 1, "faultMsg": "","light": {"type": 37,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 37, "zoneId": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})

    @allure.title("获取超车灯故障状态&通知超车灯故障状态")
    @pytest.mark.smoke
    def test_caseid_1913650(self):
        for Flash in [2, 1, 2, 3, 0]:
            logger.info(f"发送信号: {Flash}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFlash', Flash)
            if Flash in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                  {"faults": [{"fault": 1, "faultMsg": "","light": {"type": 32,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 32, "zoneId": 0}}]})
            elif Flash in [3]:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "LightFault")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 32, "zoneId": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
    
    @allure.title("获取超车灯故障状态&通知超车灯故障状态_默认值")
    @pytest.mark.full
    def test_caseid_1983977(self):
        for Flash in [2, 0]:
            logger.info(f"发送信号: {Flash}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFlash', Flash)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                        {"out": [ {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
            self.ipdu.resume_all_bus_send()
            if Flash in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                    {"faults": [{"fault": 1, "faultMsg": "","light": {"type": 32,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 32, "zoneId": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
    
    @allure.title("获取倒车灯故障状态&通知倒车灯故障状态")
    @pytest.mark.smoke
    def test_caseid_111233(self):
        for seLi in [2, 1, 2, 3, 0]:
            logger.info(f"发送信号: {seLi}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReverseLi', seLi)
            if seLi in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                  {"faults": [{"fault": 1, "faultMsg": "","light": {"type": 8,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 8, "zoneId": 0}}]})
            elif seLi in [3]:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "LightFault")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 8, "zoneId": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
    
    @allure.title("获取倒车灯故障状态&通知倒车灯故障状态_默认值")
    @pytest.mark.full
    def test_caseid_1983987(self):
        for seLi in [2, 0]:
            logger.info(f"发送信号: {seLi}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReverseLi', seLi)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                        {"out": [ {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
            self.ipdu.resume_all_bus_send()
            if seLi in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                    {"faults": [{"fault": 1, "faultMsg": "","light": {"type": 8,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 8, "zoneId": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
    
    @allure.title("获取制动灯故障状态&通知制动灯故障状态")
    @pytest.mark.sanity
    def test_caseid_111113(self):
        for StopLi in [2, 1, 2, 3, 0]:
            logger.info(f"发送信号: {StopLi}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', StopLi)
            if StopLi in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault",
                                  {"faults": [{"fault": 1, "faultMsg": "", "light": {"type": 0, "zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {}, 
                                                      {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 0, "zoneId": 0}}]})
            elif StopLi in [3]:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "LightFault")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {}, 
                                                      {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 0, "zoneId": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
    
    @allure.title("获取制动灯故障状态&通知制动灯故障状态_默认值")
    @pytest.mark.full
    def test_caseid_111140(self):
        for StopLi in [2, 1, 2, 3, 0]:
            logger.info(f"发送信号: {StopLi}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', StopLi)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                        {"out": [ {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
            self.ipdu.resume_all_bus_send()
            if StopLi in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault",
                                    {"faults": [{"fault": 1, "faultMsg": "", "light": {"type": 0, "zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {}, 
                                                        {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 0, "zoneId": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
        
    @allure.title("获取日间行车灯故障状态&通知日间行车灯故障状态")
    @pytest.mark.sanity
    def test_caseid_111178(self):
        for DRL in [2, 1, 2, 3, 0]:
            logger.info(f"发送信号: {DRL}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsDRL', DRL)
            if DRL in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault",
                                  {"faults": [{"fault": 1, "faultMsg": "", "light": {"type": 3, "zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {}, 
                                                      {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 3, "zoneId": 0}}]})
            elif DRL in [3]:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "LightFault")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {}, 
                                                      {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 3, "zoneId": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
    
    @allure.title("获取日间行车灯故障状态&通知日间行车灯故障状态_默认值")
    @pytest.mark.full
    def test_caseid_1913661(self):
        for DRL in [2,  0]:
            logger.info(f"发送信号: {DRL}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsDRL', DRL)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                        {"out": [ {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
            self.ipdu.resume_all_bus_send()
            if DRL in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault",
                                    {"faults": [{"fault": 1, "faultMsg": "", "light": {"type": 3, "zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {}, 
                                                        {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 3, "zoneId": 0}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
    
    @allure.title("获取转向灯故障状态&通知转向灯故障状态")
    @pytest.mark.sanity
    def test_caseid_1983988(self):
        for IndrLe in [2, 1, 2, 3, 0]:
            logger.info(f"发送信号: {IndrLe}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', IndrLe)  # 左转向
            if IndrLe in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults":[{"fault": 1, "faultMsg": "","light": {"type": 10,"zoneId": 12}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                      {"out": [{"fault": 1, "faultMsg": "","light": {"type": 10, "zoneId": 12}}]})
            elif IndrLe in [3]:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "LightFault")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {}, 
                                              {"out": [{"fault": 1, "faultMsg": "","light": {"type": 10, "zoneId": 12}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [ {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
        for IndrRi in [2, 1, 2, 0]:
            logger.info(f"发送信号: {IndrRi}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', IndrRi)  # 右转向
            if IndrRi in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault",
                                          {"faults":[{"fault": 1, "faultMsg": "","light": {"type": 10,"zoneId": 13}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                      {"out": [{"fault": 1, "faultMsg": "","light": {"type": 10, "zoneId": 13}}]})
            elif IndrRi in [3]:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "LightFault")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {}, 
                                              {"out": [{"fault": 1, "faultMsg": "","light": {"type": 10, "zoneId": 13}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [ {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 2)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                  {"faults":[{"fault": 1, "faultMsg": "","light": {"type": 10, "zoneId": 12}},
                                             {"fault": 1, "faultMsg": "","light": {"type": 10, "zoneId": 13}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 10, "zoneId": 12}},
                                                       {"fault": 1, "faultMsg": "","light": {"type": 10, "zoneId": 13}}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', 0)
        self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault",
                                  {"faults": [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
    
    @allure.title("获取转向灯故障状态&通知转向灯故障状态_默认值")
    @pytest.mark.full
    def test_caseid_1983989(self):
        for sts in [2, 0]:
            logger.info(f"发送信号: {sts}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', sts)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', sts)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                        {"out": [ {"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
            self.ipdu.resume_all_bus_send()
            if sts in [2]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                    {"faults":[{"fault": 1, "faultMsg": "","light": {"type": 10, "zoneId": 12}},
                                                {"fault": 1, "faultMsg": "","light": {"type": 10, "zoneId": 13}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                {"out": [{"fault": 1, "faultMsg": "", "light": {"type": 10, "zoneId": 12}},
                                                        {"fault": 1, "faultMsg": "","light": {"type": 10, "zoneId": 13}}]})
            else:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightFault", 
                                          {"faults": [{"fault": 0, "faultMsg": "","light": {"type": 100,"zoneId": 0}}]})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetFaultInfo", {},
                                                    {"out": [{"fault": 0, "faultMsg": "", "light": {"type": 100, "zoneId": 0}}]})
    
    @allure.title("设置左侧L2按键灯ADAS提醒模式_mode=0(夜晚)")#TwliBriSts=0 & ActvnOfIndcrIllmn=0
    @pytest.mark.sanity
    def test_caseid_111206(self):
        for sts in [1, 2, 3, 4, 10, 15, 0]:
            logger.info(f"发送信号: {sts}")
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'IntrBriSts', sts)
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 0)
            self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 0)
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 12, "mode": 0}]})
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            if sts in [1, 0]:
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBrightness", [0])
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeRed", [29])
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeGreen", [18])
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBlue", [27])
            elif sts in [2, 3]:
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBrightness", [0])
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeRed", [22])
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeGreen", [20])
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBlue", [23])
            elif sts in [4, 10, 15]:
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBrightness", [0])
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeRed", [19])
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeGreen", [21])
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBlue", [23])
    
    @allure.title("设置左侧L2按键灯ADAS提醒模式_mode=0(夜晚)")#TwliBriSts=1 & ActvnOfIndcrIllmn=1
    @pytest.mark.full
    def test_caseid_1984027(self):
        for sts in [1, 2, 3, 4, 10, 15, 0]:
            logger.info(f"发送信号: {sts}")
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'IntrBriSts', sts)
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 0)
            self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 1)
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 12, "mode": 0}]})
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            if sts in [1]:
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBrightness", [30])
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeRed", [29])
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeGreen", [18])
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBlue", [27])
            elif sts in [2, 3]:
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBrightness", [65])
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeRed", [22])
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeGreen", [20])
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBlue", [23])
            elif sts in [4, 10, 15]:
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBrightness", [100])
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeRed", [19])
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeGreen", [21])
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBlue", [23])
            elif sts in [0]:
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBrightness", [30])
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeRed", [29])
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeGreen", [18])
                self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBlue", [27])
    
    @allure.title("设置左侧L2按键灯ADAS提醒模式_mode=0(白天)")#TwliBriSts=1 & ActvnOfIndcrIllmn=0
    @pytest.mark.smoke
    def test_caseid_1984028(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 1)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 0)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                            {"adasInfo": [{"zoneId": 12, "mode": 0}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBrightness", [0])
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeRed", [57])
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeGreen", [64])
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBlue", [70])
    
    @allure.title("设置左侧L2按键灯ADAS提醒模式_mode=0(白天)")#TwliBriSts=1 & ActvnOfIndcrIllmn=1 & IntrBriSts=4
    @pytest.mark.full
    def test_caseid_1984029(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 1)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'IntrBriSts', 4)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                            {"adasInfo": [{"zoneId": 12, "mode": 0}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBrightness", [100])
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeRed", [57])
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeGreen", [64])
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBlue", [70])
    
    @allure.title("设置左侧L2按键灯ADAS提醒模式_mode=2(夜晚)")#TwliBriSts=0 & ActvnOfIndcrIllmn=0/1
    @pytest.mark.full
    def test_caseid_1984031(self):
        for sts in [1, 0]:
            logger.info(f"发送信号: {sts}")
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', sts)
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 0)
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 12, "mode": 2}]})
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.get_signal_values("SteerWhlSymbolLightCtrlLeBrightness")
            self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBrightness", [70])
            self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeRed", [4])
            self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeGreen", [5])
            self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBlue", [100])
    
    @allure.title("设置左侧L2按键灯ADAS提醒模式_mode=2(白天)")#TwliBriSts=1 & ActvnOfIndcrIllmn=0/1
    @pytest.mark.sanity
    def test_caseid_1984032(self):
        for sts in [1, 0]:
            logger.info(f"发送信号: {sts}")
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', sts)
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 1)
            # todo 开始抓包
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 12, "mode": 2}]})
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBrightness", [100])
            self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeRed", [18])
            self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeGreen", [15])
            self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBlue", [255])
            
    @allure.title("设置左侧L2按键灯ADAS提醒模式_mode=3(夜晚)")#TwliBriSts=0 & ActvnOfIndcrIllmn=0/1
    @pytest.mark.sanity
    def test_caseid_1984056(self):
        for sts in [1, 0]:
            logger.info(f"发送信号: {sts}")
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', sts)
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 0)
            # todo 开始抓包
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 12, "mode": 3}]})
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBrightness", [70])
            self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeRed", [26])
            self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeGreen", [5])
            self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBlue", [105])
    
    @allure.title("设置左侧L2按键灯ADAS提醒模式_mode=3(白天)")#TwliBriSts=1 & ActvnOfIndcrIllmn=0/1
    @pytest.mark.full
    def test_caseid_1984057(self):
        for sts in [1, 0]:
            logger.info(f"发送信号: {sts}")
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', sts)
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 1)
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 12, "mode": 3}]})
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBrightness", [100])
            self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeRed", [45])
            self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeGreen", [3])
            self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBlue", [255])
    
    @allure.title("设置左侧L2按键灯ADAS提醒模式_mode=4(夜晚)")#TwliBriSts=0 & ActvnOfIndcrIllmn=0
    @pytest.mark.full
    def test_caseid_1984058(self):
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 0)
            self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 0)
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 12, "mode": 4}]})
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            signals = self.bgm_eth_inter.get_signal_values("SteerWhlSymbolLightCtrlLeBrightness")
            logger.info(f"list1111 = {signals}")
            self.ck_signal2(signals, 10, 70)
            self.bgm_eth_inter.ck_ordered_array("SteerWhlSymbolLightCtrlLeRed", [26])
            self.bgm_eth_inter.ck_ordered_array("SteerWhlSymbolLightCtrlLeGreen", [5])
            self.bgm_eth_inter.ck_ordered_array("SteerWhlSymbolLightCtrlLeBlue", [105])
    
    @allure.title("设置左侧L2按键灯ADAS提醒模式_mode=4(夜晚)")#TwliBriSts=0 & ActvnOfIndcrIllmn=1
    @pytest.mark.sanity
    def test_caseid_1984967(self):
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 0)
            self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 1)
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 12, "mode": 4}]})
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            signals = self.bgm_eth_inter.get_signal_values("SteerWhlSymbolLightCtrlLeBrightness")
            logger.info(f"list1111 = {signals}")
            self.ck_signal2(signals, 10, 70)
            self.bgm_eth_inter.ck_ordered_array("SteerWhlSymbolLightCtrlLeRed", [26])
            self.bgm_eth_inter.ck_ordered_array("SteerWhlSymbolLightCtrlLeGreen", [5])
            self.bgm_eth_inter.ck_ordered_array("SteerWhlSymbolLightCtrlLeBlue", [105])

    @allure.title("设置左侧L2按键灯ADAS提醒模式_mode=4(白天)")#TwliBriSts=1 & ActvnOfIndcrIllmn=0
    @pytest.mark.sanity
    def test_caseid_1984059(self):
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 1)
            self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 1)
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 12, "mode": 4}]})
            # sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=3)
            signals = self.bgm_eth_inter.get_signal_values("SteerWhlSymbolLightCtrlLeBrightness")
            logger.info(f"list1111 = {signals}")
            self.ck_signal2(signals, 10, 100)
            self.bgm_eth_inter.ck_ordered_array("SteerWhlSymbolLightCtrlLeRed", [45])
            self.bgm_eth_inter.ck_ordered_array("SteerWhlSymbolLightCtrlLeGreen", [3])
            self.bgm_eth_inter.ck_ordered_array("SteerWhlSymbolLightCtrlLeBlue", [255])
    
    @allure.title("设置左侧L2按键灯ADAS提醒模式_mode=4(白天)")#TwliBriSts=1 & ActvnOfIndcrIllmn=0
    @pytest.mark.full
    def test_caseid_1984985(self):
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 1)
            self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 0)
            self.partner.empty_all(0.5)
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 12, "mode": 4}]})
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            signals = self.bgm_eth_inter.get_signal_values("SteerWhlSymbolLightCtrlLeBrightness")
            logger.info(f"list1111 = {signals}")
            self.ck_signal2(signals, 10, 100)
            self.bgm_eth_inter.ck_ordered_array("SteerWhlSymbolLightCtrlLeRed", [45])
            self.bgm_eth_inter.ck_ordered_array("SteerWhlSymbolLightCtrlLeGreen", [3])
            self.bgm_eth_inter.ck_ordered_array("SteerWhlSymbolLightCtrlLeBlue", [255])
    
    @allure.title("设置左侧L2按键灯ADAS提醒模式_IntrBriSts(信号丢失)_Last Value")
    @pytest.mark.full
    def test_caseid_1984067(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 1)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'IntrBriSts', 4)
        self.partner.empty_all(0.5)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.stop_send_pdu("bodycan", 0x0E0)
        sleep(1)
        logger.info(f"打印{time.time()}")#打印时间
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 12, "mode": 0}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBrightness", [100, 100])
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeRed", [57, 57])
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeGreen", [64, 64])
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBlue", [70, 70])
    
    @allure.title("设置左侧L2按键灯ADAS提醒模式_IntrBriSts(信号丢失)_默认值")
    @pytest.mark.full
    def test_caseid_1984069(self):
        self.partner.empty_all(0.5)
        self.ipdu.stop_send_pdu("bodycan", 0x0E0)
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 12, "mode": 2}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBrightness", [70])
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeRed", [4])
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeGreen", [5])
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBlue", [100])
    
    @allure.title("设置左侧L2按键灯ADAS提醒模式_ActvnOfIndcrIllmn(信号丢失)_Last Value")
    @pytest.mark.full
    def test_caseid_1984070(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 0)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 1)
        self.ipdu.stop_send_pdu("bodycan", 0x230)
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        logger.info(f"打印{time.time()}")#打印时间
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 12, "mode": 3}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBrightness", [70])
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeRed", [26])
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeGreen", [5])
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBlue", [105])
    
    @allure.title("设置左侧L2按键灯ADAS提醒模式_ActvnOfIndcrIllmn(信号丢失)_默认值")
    @pytest.mark.full
    def test_caseid_1984071(self):
        self.ipdu.stop_send_pdu("bodycan", 0x230)
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 12, "mode": 2}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBrightness", [70])
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeRed", [4])
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeGreen", [5])
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBlue", [100])
    
    @allure.title("设置左侧L2按键灯ADAS提醒模式_TwliBriSts(信号丢失)_默认值")
    @pytest.mark.full
    def test_caseid_1984072(self):
        self.ipdu.stop_send_pdu("bodycan", 0x040)
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 12, "mode": 2}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBrightness", [70])
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeRed", [4])
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeGreen", [5])
        self.bgm_eth_inter.ck_signal_values("SteerWhlSymbolLightCtrlLeBlue", [100])
        
    @allure.title("设置L7长条指示灯ADAS提醒模式_mode=0")
    @pytest.mark.smoke
    def test_caseid_111138(self):
        for sts in [1, 0]:
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', sts)
            for Illmn in [1, 0]:
                self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', Illmn)
                self.bgm_eth_inter.start_bgm_tcpdump()
                self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 14, "mode": 0}]})
                sleep(2)
                self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
                self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlBrightness', [0])
                self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlRed', [255])
                self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlGreen', [255])
                self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlBlue', [255])
    
    @allure.title("设置L7长条指示灯ADAS提醒模式_mode=2(夜晚)")
    @pytest.mark.full
    def test_caseid_1984103(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 0)
        for Illmn in [1, 0]:
            self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', Illmn)
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                            {"adasInfo": [{"zoneId": 14, "mode": 2}]})
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlBrightness', [40])
            self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlRed', [6])
            self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlGreen', [0])
            self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlBlue', [28])
    
    @allure.title("设置L7长条指示灯ADAS提醒模式_mode=2(白天)")
    @pytest.mark.sanity
    def test_caseid_1984104(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 1)
        for Illmn in [1, 0]:
            self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', Illmn)
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                            {"adasInfo": [{"zoneId": 14, "mode": 2}]})
            sleep(2)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlBrightness', [40])
            self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlRed', [35])
            self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlGreen', [0])
            self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlBlue', [200])
    
    @allure.title("设置L7长条指示灯ADAS提醒模式_mode=3(夜晚)")
    @pytest.mark.sanity
    def test_caseid_1984105(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 0)
        for Illmn in [1, 0]:
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', Illmn)
            sleep(2)
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                            {"adasInfo": [{"zoneId": 14, "mode": 3}]})
            sleep(3)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            signals =self.bgm_eth_inter.get_signal_values('SteerWhlLightingBarCtrlBrightness')
            logger.info(f"打印抓包出来信号值 = {signals}")
            self.ck_signal2(signals, 10, 39)
            self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlRed', [6])
            self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlGreen', [0])
            self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlBlue', [28])
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                            {"adasInfo": [{"zoneId": 14, "mode": 0}]})
    
    @allure.title("设置L7长条指示灯ADAS提醒模式_mode=3(白天)")
    @pytest.mark.full
    def test_caseid_1984106(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 1)
        for Illmn in [1, 0]:
            self.bgm_eth_inter.start_bgm_tcpdump()
            self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', Illmn)
            sleep(2)
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                            {"adasInfo": [{"zoneId": 14, "mode": 3}]})
            sleep(3)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            signals =self.bgm_eth_inter.get_signal_values('SteerWhlLightingBarCtrlBrightness')
            logger.info(f"打印抓包出来信号值 = {signals}")
            self.ck_signal2(signals, 10, 39)
            self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlRed', [35])
            self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlGreen', [0])
            self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlBlue', [200])
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                            {"adasInfo": [{"zoneId": 14, "mode": 0}]})
    
    @allure.title("设置L7长条指示灯ADAS提醒模式_mode=4(夜晚)")#ActvnOfIndcrIllmn=1&TwliBriSts=0
    @pytest.mark.sanity
    def test_caseid_1984107(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 0)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                        {"adasInfo": [{"zoneId": 14, "mode": 4}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        signals = self.bgm_eth_inter.get_signal_values("SteerWhlLightingBarCtrlBrightness")
        logger.info(f"list1111 = {signals}")
        self.ck_signal3(signals, 0, 100)#闪烁灯效,0-100闪烁
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlRed', [10])
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlGreen', [0])
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlBlue', [0])
    
    @allure.title("设置L7长条指示灯ADAS提醒模式_mode=4(夜晚)")#ActvnOfIndcrIllmn=0&TwliBriSts=0
    @pytest.mark.sanity
    def test_caseid_1984997(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 0)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 0)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                        {"adasInfo": [{"zoneId": 14, "mode": 4}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        signals = self.bgm_eth_inter.get_signal_values("SteerWhlLightingBarCtrlBrightness")
        logger.info(f"list1111 = {signals}")
        self.ck_signal3(signals, 0, 100)#闪烁灯效,0-100闪烁
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlRed', [10])
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlGreen', [0])
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlBlue', [0])
    
    @allure.title("设置L7长条指示灯ADAS提醒模式_mode=4(白天)")#ActvnOfIndcrIllmn=1&TwliBriSts=1
    @pytest.mark.full
    def test_caseid_1984108(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 1)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                        {"adasInfo": [{"zoneId": 14, "mode": 4}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        signals = self.bgm_eth_inter.get_signal_values("SteerWhlLightingBarCtrlBrightness")
        logger.info(f"list1111 = {signals}")
        self.ck_signal3(signals, 0, 100)#闪烁灯效,0-100闪烁
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlRed', [210])
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlGreen', [2])
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlBlue', [5])
    
    @allure.title("设置L7长条指示灯ADAS提醒模式_mode=4(白天)")#ActvnOfIndcrIllmn=0&TwliBriSts=1
    @pytest.mark.full
    def test_caseid_1984998(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 1)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 0)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                        {"adasInfo": [{"zoneId": 14, "mode": 4}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        signals = self.bgm_eth_inter.get_signal_values("SteerWhlLightingBarCtrlBrightness")
        logger.info(f"list1111 = {signals}")
        self.ck_signal3(signals, 0, 100)#闪烁灯效,0-100闪烁
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlRed', [210])
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlGreen', [2])
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlBlue', [5])
    
    @allure.title("设置L7长条指示灯ADAS提醒模式_mode=5(夜晚)")
    @pytest.mark.sanity
    def test_caseid_1984109(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 0)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                        {"adasInfo": [{"zoneId": 14, "mode": 5}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        signals = self.bgm_eth_inter.get_signal_values("SteerWhlLightingBarCtrlBrightness")
        logger.info(f"list1111 = {signals}")
        self.ck_signal3(signals, 0, 100)#闪烁灯效,0-100闪烁
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlRed', [10])
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlGreen', [0])
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlBlue', [0])
    
    @allure.title("设置L7长条指示灯ADAS提醒模式_mode=5(夜晚)")
    @pytest.mark.sanity
    def test_caseid_1984999(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 0)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 0)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                        {"adasInfo": [{"zoneId": 14, "mode": 5}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        signals = self.bgm_eth_inter.get_signal_values("SteerWhlLightingBarCtrlBrightness")
        logger.info(f"list1111 = {signals}")
        self.ck_signal3(signals, 0, 100)#闪烁灯效,0-100闪烁
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlRed', [10])
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlGreen', [0])
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlBlue', [0])
    
    @allure.title("设置L7长条指示灯ADAS提醒模式_mode=5(白天)")
    @pytest.mark.full
    def test_caseid_1984110(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 1)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                        {"adasInfo": [{"zoneId": 14, "mode": 5}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        signals = self.bgm_eth_inter.get_signal_values("SteerWhlLightingBarCtrlBrightness")
        logger.info(f"list1111 = {signals}")
        self.ck_signal3(signals, 0, 100)#闪烁灯效,0-100闪烁
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlRed', [210])
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlGreen', [2])
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlBlue', [5])
    
    @allure.title("设置L7长条指示灯ADAS提醒模式_mode=5(白天)")
    @pytest.mark.full
    def test_caseid_1985000(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 1)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 0)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                        {"adasInfo": [{"zoneId": 14, "mode": 5}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        signals = self.bgm_eth_inter.get_signal_values("SteerWhlLightingBarCtrlBrightness")
        logger.info(f"list1111 = {signals}")
        self.ck_signal3(signals, 0, 100)#闪烁灯效,0-100闪烁
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlRed', [210])
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlGreen', [2])
        self.bgm_eth_inter.ck_ordered_array('SteerWhlLightingBarCtrlBlue', [5])
    
    @allure.title("设置L7长条指示灯ADAS提醒模式_IntrBriSts(信号丢失)_Last Value")
    @pytest.mark.full
    def test_caseid_1984120(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 1)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 1)
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 14, "mode": 2}]})
        sleep(1)
        self.ipdu.stop_send_pdu("bodycan", 0x0E0)
        logger.info(f"打印{time.time()}")#打印时间
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlBrightness', [40, 40])
        self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlRed', [35, 35])
        self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlGreen', [0, 0])
        self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlBlue', [200, 200])
    
    @allure.title("设置L7长条指示灯ADAS提醒模式_IntrBriSts(信号丢失)_默认值")
    @pytest.mark.full
    def test_caseid_1984121(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.stop_send_pdu("bodycan", 0x0E0)
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 14, "mode": 2}]})
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlBrightness', [40])
        self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlRed', [6])
        self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlGreen', [0])
        self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlBlue', [28])
    
    @allure.title("设置L7长条指示灯ADAS提醒模式_ActvnOfIndcrIllmn(信号丢失)_Last Value")
    @pytest.mark.full
    def test_caseid_1984122(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 1)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 1)
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 14, "mode": 2}]})
        sleep(1)
        self.ipdu.stop_send_pdu("bodycan", 0x230)
        logger.info(f"打印{time.time()}")#打印时间
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlBrightness', [40, 40])
        self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlRed', [35, 35])
        self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlGreen', [0, 0])
        self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlBlue', [200, 200])
    
    @allure.title("设置L7长条指示灯ADAS提醒模式_ActvnOfIndcrIllmn(信号丢失)_默认值")
    @pytest.mark.full
    def test_caseid_1984123(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 14, "mode": 2}]})
        sleep(1)
        self.ipdu.stop_send_pdu("bodycan", 0x230)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlBrightness', [40, 40])
        self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlRed', [6, 6])
        self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlGreen', [0, 0])
        self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlBlue', [28, 28])
    
    @allure.title("设置L7长条指示灯ADAS提醒模式_TwliBriSts(信号丢失)_默认值")
    @pytest.mark.full
    def test_caseid_1984124(self):
        self.ipdu.stop_send_pdu("bodycan", 0x040)
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 14, "mode": 2}]})
        sleep(1)
        self.kill_s2s_and_reconnect_service(LIGHT_SERVICE_CLIENT)
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlBrightness', [40, 0])
        self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlRed', [6, 255])
        self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlGreen', [0, 255])
        self.bgm_eth_inter.ck_signal_values('SteerWhlLightingBarCtrlBlue', [28, 255])
    
    @allure.title("设置右侧R2按键灯ADAS提醒模式_mode=0(夜晚)")#TwliBriSts=0 & ActvnOfIndcrIllmn=0
    @pytest.mark.smoke
    def test_caseid_111169(self):
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 0)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 0)
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                            {"adasInfo": [{"zoneId": 13, "mode": 0}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiBrightness', [0])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiRed', [255])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiGreen', [255])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiBlue', [255])
    
    @allure.title("设置右侧R2按键灯ADAS提醒模式_mode=0(夜晚)")#TwliBriSts=0 & ActvnOfIndcrIllmn=1
    @pytest.mark.full
    def test_caseid_1984128(self):
        # todo 开始抓包
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 0)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'IntrBriSts', 3)
        sleep(0.5)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                            {"adasInfo": [{"zoneId": 13, "mode": 0}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiBrightness', [35])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiRed', [255])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiGreen', [255])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiBlue', [255])
    
    @allure.title("设置右侧R2按键灯ADAS提醒模式_mode=1(白天)")#TwliBriSts=1 & ActvnOfIndcrIllmn=0
    @pytest.mark.sanity
    def test_caseid_1984129(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 1)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 0)
        sleep(0.5)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                            {"adasInfo": [{"zoneId": 13, "mode": 0}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiBrightness', [0])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiRed', [255])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiGreen', [255])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiBlue', [255])
    
    @allure.title("设置右侧R2按键灯ADAS提醒模式_mode=1(白天)")#TwliBriSts=1 & ActvnOfIndcrIllmn=1
    @pytest.mark.full
    def test_caseid_1984130(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 1)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 1)
        sleep(0.5)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                            {"adasInfo": [{"zoneId": 13, "mode": 0}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiBrightness', [100])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiRed', [255])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiGreen', [255])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiBlue', [255])
    
    @allure.title("设置右侧R2按键灯ADAS提醒模式_IntrBriSts(信号丢失)_Last Value")
    @pytest.mark.full
    def test_caseid_1984133(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 1)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'IntrBriSts', 4)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.stop_send_pdu("bodycan", 0x0E0)
        sleep(1)
        logger.info(f"打印{time.time()}")#打印时间
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 13, "mode": 0}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiBrightness', [100, 100])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiRed', [255, 255])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiGreen', [255, 255])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiBlue', [255, 255])
    
    @allure.title("设置右侧R2按键灯ADAS提醒模式_IntrBriSts(信号丢失)_默认值")
    @pytest.mark.full
    def test_caseid_1984134(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.stop_send_pdu("bodycan", 0x0E0)
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 13, "mode": 0}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiBrightness', [0, 0])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiRed', [255, 255])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiGreen', [255, 255])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiBlue', [255, 255])
    
    @allure.title("设置右侧R2按键灯ADAS提醒模式_ActvnOfIndcrIllmn(信号丢失)_Last Value")
    @pytest.mark.full
    def test_caseid_1984136(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'TwliBriSts', 0)
        self.ipdu.set(self.ipdu.bodycan.BgmBodyFr01, 'ActvnOfIndcrIllmn', 1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'IntrBriSts', 8)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.stop_send_pdu("bodycan", 0x230)
        sleep(1)
        logger.info(f"打印{time.time()}")#打印时间
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 13, "mode": 0}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiBrightness', [45, 45])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiRed', [255, 255])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiGreen', [255, 255])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiBlue', [255, 255])
    
    @allure.title("设置右侧R2按键灯ADAS提醒模式_ActvnOfIndcrIllmn(信号丢失)_默认值")
    @pytest.mark.full
    def test_caseid_1984139(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.stop_send_pdu("bodycan", 0x230)
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 13, "mode": 0}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiBrightness', [0, 0])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiRed', [255, 255])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiGreen', [255, 255])
        self.bgm_eth_inter.ck_signal_values('SteerWhlSymbolLightCtrlRiBlue', [255, 255])
    
    @allure.title("设置右侧R2按键灯ADAS提醒模式_TwliBriSts(信号丢失)_默认值")
    @pytest.mark.full
    def test_caseid_1984140(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.stop_send_pdu("bodycan", 0x040)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetSteerWhlLampADASMode",
                                                {"adasInfo": [{"zoneId": 13, "mode": 0}]})
        sleep(1)
        self.kill_s2s_and_reconnect_service(LIGHT_SERVICE_CLIENT)
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array('SteerWhlSymbolLightCtrlRiBrightness', [0])
        self.bgm_eth_inter.ck_ordered_array('SteerWhlSymbolLightCtrlRiRed', [255])
        self.bgm_eth_inter.ck_ordered_array('SteerWhlSymbolLightCtrlRiGreen', [255])
        self.bgm_eth_inter.ck_ordered_array('SteerWhlSymbolLightCtrlRiBlue', [255])

    @allure.title("获取远光灯状态&通知远光灯状态")
    @pytest.mark.smoke
    def test_caseid_1984142(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', 0)
        self.partner.empty_all(0.5)
        for sts in [1, 2, 3, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', sts)
            if sts in [1, 2, 0]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "HighBeamStatus", {"sts":{"sts":sts,"clientId":255}})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamStatus", {},
                                                {"out":{"sts": sts,"clientId":255}})
            else:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "HighBeamStatus")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamStatus", {},
                                                {"out":{"sts": 2,"clientId":255}})
    
    @allure.title("获取远光灯状态&通知远光灯状态_默认值")
    @pytest.mark.full
    def test_caseid_1984256(self):
        for sts in [1, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', sts)
            sleep(0.5)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamStatus", {},
                                                {"out":{"sts": 0,"clientId":255}})
            self.ipdu.resume_all_bus_send()
            sleep(0.5)
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "HighBeamStatus", {"sts":{"sts":sts,"clientId":255}})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetHighBeamStatus", {},
                                                {"out":{"sts": sts,"clientId":255}})
    
    @allure.title("获取灯光秀激活状态(外灯)&通知灯光秀激活状态(外灯)")
    @pytest.mark.sanity
    def test_caseid_1984145(self):
        self.ipdu.set(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr10, 'StaticLightingModeEn', 0)
        self.partner.empty_all(0.5)
        for ModeEn in [1, 2, 3, 0]:
            logger.info(f"发送信号: {ModeEn}")
            self.ipdu.set(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr10, 'StaticLightingModeEn', ModeEn)
            if ModeEn in [1, 2, 0]:
                self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightShowActivateStatus",
                                          {"status": ModeEn})
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetLightShowActivateStatus", {},
                                                      {"out": ModeEn})
            else:
                self.partner.ck_no_event(LIGHT_SERVICE_CLIENT, "LightFault")
                self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetLightShowActivateStatus", {},
                                                      {"out": 2})
    
    @allure.title("获取灯光秀激活状态(外灯)&通知灯光秀激活状态(外灯)_默认值")
    @pytest.mark.full
    def test_caseid_1984146(self):
        for sts in [0, 1]:
            logger.info(f"sts:{sts}")
            self.ipdu.set(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr10, 'StaticLightingModeEn', sts)
            self.restart_bgm_and_connect_service(LIGHT_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetLightShowActivateStatus", {},
                                                        {"out": 0})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "LightShowActivateStatus",
                                            {"status": sts})
            self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetLightShowActivateStatus", {},
                                                        {"out": sts})
        self.ipdu.set(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr10, 'StaticLightingModeEn', 0)
    
    @allure.title("远光灯控制（仲裁)_cmd=0-远光灯开")
    @pytest.mark.sanity
    def test_caseid_1984260(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1', 0)#设置carmode
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 13)#设置usagemode
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3})  # 设置近光灯打开
        # 确保环境正常
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedHiBeamLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedHiBeamRi', 0)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                        {"info": {"cmd": 255, "clientId": 1}})  
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                         {"info": {"cmd": 255, "clientId": 255}})#独占释放 恢复环境
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', 1)
        for id in [6, 4, 5, 3, 2, 1]:
            sleep(0.5)
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                            {"info": {"cmd": 0, "clientId": id}})  
            sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=1)
        self.bgm_eth_inter.ck_signal_values('HiBeamSw', [0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2])

    @allure.title("远光灯控制（仲裁)_cmd=0_远光灯关")#AHBC
    @pytest.mark.full
    def test_caseid_1984261(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1', 0)#设置carmode
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 13)#设置usagemode
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3})  # 设置近光灯打开
        # 确保环境正常
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedHiBeamLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedHiBeamRi', 0)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                        {"info": {"cmd": 255, "clientId": 1}})  
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                         {"info": {"cmd": 255, "clientId": 255}})#独占释放 恢复环境
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', 0)
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                        {"info": {"cmd": 0, "clientId": 6}})  
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('HiBeamSw', [])

    @allure.title("远光灯控制（仲裁)_cmd=0_超车灯开")#AVP
    @pytest.mark.full
    def test_caseid_1984273(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1', 0)#设置carmode
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 13)#设置usagemode
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3})  # 设置近光灯打开
        # 确保环境正常
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedHiBeamLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedHiBeamRi', 0)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                        {"info": {"cmd": 255, "clientId": 1}})  
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                         {"info": {"cmd": 255, "clientId": 255}})#独占释放 恢复环境
        
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFlash', 1)
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                        {"info": {"cmd": 0, "clientId": 3}})  
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('HiBeamSw', [0])
        
    @allure.title("远光灯控制（仲裁)_cmd=2_远光灯开")#AHBC
    @pytest.mark.full
    def test_caseid_1984274(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1', 0)#设置carmode
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 13)#设置usagemode
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3})  # 设置近光灯打开
        # 确保环境正常
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedHiBeamLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedHiBeamRi', 0)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                        {"info": {"cmd": 255, "clientId": 1}})  
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                         {"info": {"cmd": 255, "clientId": 255}})#独占释放 恢复环境
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', 1)
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                        {"info": {"cmd": 2, "clientId": 6}})  
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('HiBeamSw', [])
    
    @allure.title("远光灯控制（仲裁)_cmd=2_远光灯关")#AHBC
    @pytest.mark.sanity
    def test_caseid_1984275(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1', 0)#设置carmode
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 13)#设置usagemode
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3})  # 设置近光灯打开
        # 确保环境正常
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedHiBeamLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedHiBeamRi', 0)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                        {"info": {"cmd": 255, "clientId": 1}})  
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                         {"info": {"cmd": 255, "clientId": 255}})#独占释放 恢复环境
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', 0)
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                        {"info": {"cmd": 2, "clientId": 6}})  
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('HiBeamSw', [0, 2])
    
    @allure.title("远光灯控制（仲裁)_cmd=2_超车灯开")#方向盘按键 
    @pytest.mark.full
    def test_caseid_1984276(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1', 0)#设置carmode
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 13)#设置usagemode
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3})  # 设置近光灯打开
        # 确保环境正常
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedHiBeamLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedHiBeamRi', 0)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                        {"info": {"cmd": 255, "clientId": 1}})  
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                         {"info": {"cmd": 255, "clientId": 255}})#独占释放 恢复环境
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFlash', 1)
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                        {"info": {"cmd": 2, "clientId": 2}})  
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('HiBeamSw', [2])
    
    @allure.title("远光灯控制（仲裁)_cmd=2_远光灯故障")#AHBC
    @pytest.mark.full
    def test_caseid_1984280(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1', 0)#设置carmode
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 13)#设置usagemode
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3})  # 设置近光灯打开
        # 确保环境正常
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedHiBeamLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedHiBeamRi', 0)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                        {"info": {"cmd": 255, "clientId": 1}})  
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                         {"info": {"cmd": 255, "clientId": 255}})#独占释放 恢复环境
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', 2)
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                        {"info": {"cmd": 2, "clientId": 6}})  
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('HiBeamSw', [])
    
    @allure.title("远光灯控制（仲裁)_cmd=2_超车灯故障")#方向盘按键 
    @pytest.mark.full
    def test_caseid_1984281(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1', 0)#设置carmode
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 13)#设置usagemode
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetExteriorLightMode", {"mode": 3})  # 设置近光灯打开
        # 确保环境正常
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedHiBeamLe', 0)
        self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedHiBeamRi', 0)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                        {"info": {"cmd": 255, "clientId": 1}})  
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                         {"info": {"cmd": 255, "clientId": 255}})#独占释放 恢复环境
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFlash', 2)
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetHighBeamControl",
                                        {"info": {"cmd": 2, "clientId": 2}})  
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('HiBeamSw', [0, 2])
    
    @allure.title("礼貌灯(内灯)控制&获取内灯模式(礼貌灯)_不响应接口调用(解闭锁成功触发源_1_RKE闭锁成功)")  #LockgCenStsLockSt=2
    @pytest.mark.full
    def test_caseid_a1(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 3)
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 2)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 1)
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 2, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 0})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [])
    
    @allure.title("礼貌灯(内灯)控制&获取内灯模式(礼貌灯)_不响应接口调用(解闭锁成功触发源_2_PE长按闭锁成功)")  #LockgCenStsLockSt=2
    @pytest.mark.full
    def test_caseid_b1(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 3)
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.empty_all(1)
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 2)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 2)
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 2, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 0})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [])
    
    @allure.title("礼貌灯(内灯)控制&获取内灯模式(礼貌灯)_(解闭锁成功触发源_3_车内按钮闭锁成功)")  #LockgCenStsLockSt=2
    @pytest.mark.full
    def test_caseid_c1(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 3)
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.empty_all(1)
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 2)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 3)
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 2, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 2})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [2, 2, 2])
        self.bgm_eth_inter.ck_period_time('IntrLampSelnMod', 0.1)
    
    @allure.title("礼貌灯(内灯)控制&获取内灯模式(礼貌灯)_不响应接口调用(解闭锁成功触发源_5_重上锁)")  #LockgCenStsLockSt=2
    @pytest.mark.full
    def test_caseid_d1(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 3)
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.empty_all(1)
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 2)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 5)
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 2, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 0})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [])
    
    @allure.title("礼貌灯(内灯)控制&获取内灯模式(礼貌灯)_不响应接口调用(解闭锁成功触发源_7_远程闭锁成功)")  #LockgCenStsLockSt=2
    @pytest.mark.full
    def test_caseid_e1(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 3)
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.empty_all(1)
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 2)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 7)
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 2, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 0})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [])
    
    @allure.title("礼貌灯(内灯)控制&获取内灯模式(礼貌灯)_不响应接口调用(解闭锁成功触发源_9_离车自动闭锁成功)")  #LockgCenStsLockSt=2
    @pytest.mark.full
    def test_caseid_f1(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 3)
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.empty_all(1)
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 2)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 9)
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 2, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 0})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [])
    
    @allure.title("礼貌灯(内灯)控制&获取内灯模式(礼貌灯)_不响应接口调用(解闭锁成功触发源_10_外部的其他方式闭锁成功)") #LockgCenStsLockSt=2 
    @pytest.mark.full
    def test_caseid_g1(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 3)
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.empty_all(1)
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 2)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 10)
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 2, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 0})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [])
    
    @allure.title("礼貌灯(内灯)控制&获取内灯模式(礼貌灯)_不响应接口调用(解闭锁成功触发源_12_NFC闭锁成功)")#LockgCenStsLockSt=2
    @pytest.mark.full
    def test_caseid_h1(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 3)
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.empty_all(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt', 2)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 12)
        sleep(1)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "LightControl", {"lights": [
            {"light": {"type": 26, "zoneId": 0}, "mode": 2, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetInternalLightMode", {}, {"out": 0})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('IntrLampSelnMod', [])
