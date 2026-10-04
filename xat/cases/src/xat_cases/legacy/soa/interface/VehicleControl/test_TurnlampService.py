# -*- coding: utf-8 -*-
"""
@File        : test_turnlamp.py
@Author      : chi.han@jiduatuo.com
@Time        : 2024/9/1 15:00 PM
@Description : Test s2s interface about turnlamp function
"""

import pytest
import random
from time import sleep
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
            
            
class TurnLampControl():
    def __init__(self, partner: S2sBaseClass, ipdu, sd_tester, io):
        self.partner = partner
        self.ipdu = ipdu
        self.sd_tester = sd_tester
        self.io = io

        self.mode_list = [0, 1, 2, 3]
        self.priority_list = [0x2f, 0x4f, 0x5f, 0x6f, 0xff]
        self.open_by_list = ['button', 'method']
        self.close_by_list = ['button', 'method', 'angle']
        self.button_stehold_list = [True, False]
        self.method_stehold_list = [True, False]
        
        self.curr_state = {
            'mode': 0,
            'priority': 255,
            'open_by': 'method',
            'close_by': 'method',
            'btn_stehold': False,
            'mth_stehold': False,
            'service_ctrl': False,
            'ctrl_timeout': 0
            }

        self.turnlamp_states = self.get_turnlamp_states()
        self.hazard_button = False
        self.DIPriority_start = False
        self.DIPriority_flag = False
        self.timer_thread = None
        self.storage_state = None

    def get_turnlamp_states(self,):
        """
        获取所有转向灯状态列表，每个状态是一个字典，包含以下键值对：
        - mode (int): 转向灯模式
        - priority (int): 优先级
        - open_by (str): 打开方式，可选值为 'button' 或 'method'
        - close_by (str): 关闭方式，可选值为 'button'、'method'、'angle'
        - btn_stehold (bool): 按键开转向灯后方向盘回正是否关闭转向灯
        - mth_stehold (bool): 服务开转向灯后方向盘回正是否关闭转向灯
        - service_ctrl (bool): 是否有独占控制权
        - ctrl_timeout (int): 控制超时时间（秒），有独占控制权为5，没有独占控制权为0，
        """
        state_all = []
        for mode in self.mode_list:
            for priority in self.priority_list:
                for open_by in self.open_by_list:
                    for close_by in self.close_by_list:
                        for btn_stehold in self.button_stehold_list:
                            for mth_stehold in self.method_stehold_list:
                                if priority != 0x5f and open_by == 'button':
                                    continue
                                if priority != 0x5f and close_by in ['button', 'angle']:
                                    continue
                                open_by = None if mode == 0 else open_by
                                close_by = None if mode != 0 else close_by
                                btn_stehold = btn_stehold if open_by == 'button' else None
                                mth_stehold = mth_stehold if open_by == 'method' else None
                                service_ctrl = priority < 0x5f and mode != 3
                                ctrl_timeout = 5 if service_ctrl else 0
                                state = {
                                    'mode': mode,
                                    'priority': priority,
                                    'open_by': open_by,
                                    'close_by': close_by,
                                    'btn_stehold': btn_stehold,
                                    'mth_stehold': mth_stehold,
                                    'service_ctrl': service_ctrl,
                                    'ctrl_timeout': ctrl_timeout
                                }
                                state_all.append(state)
        # 去重
        state_set = set()
        state_list = []
        for s in state_all:
            key = tuple(sorted(s.items()))
            if key not in state_set:
                state_list.append(s)
                state_set.add(key)
                logger.info(f"[index:{len(state_list)-1}]{s}")
                
        return state_list

    def set_hazard_button(self, open=True):
        """
        通过按键打开关闭双闪报警灯。
        @param open (bool, optional): 是否打开双闪，默认为True。
        """
        sts = self.ipdu.get_recent_signal_raw_value(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts')
        press_times = 1 if (sts != 3 and open) or (sts == 3 and not open) else 2

        if open:
            self.storage_state = self.curr_state
    
        for i in range(press_times):
            self.io.hazard_light_open()  
            sleep(0.2)
            self.io.hazard_light_close()  
            sleep(1.2)
            logger.info(f"[set_hazard_button] press {i+1}/{press_times}")
            
        self.hazard_button = open
        logger.info(f"[set_hazard_button] hazard_button status: {open}")
        
    def set_turnlamp_by_button(self, open_by, close_by, req_mode, cur_mode):
        """
        通过按键控制转向灯
        @param open_by (str): 打开方式，可选值为'button'
        @param close_by (str): 关闭方式，可选值为'button'
        @param req_mode (int): 请求模式，范围为0~3，分别代表关闭、打开左转、打开右转、打开双闪
        @param cur_mode (int): 当前模式，范围为0~3，分别代表关闭、打开左转、打开右转、打开双闪
        """
        press_num = 0
        directions = {
            'left': {
                'bodycan': self.ipdu.bodycan.SwtlBodyFr01,
                'signal': 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2'},
            'right': {
                'bodycan': self.ipdu.bodycan.SwtrBodyFr01,
                'signal': 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2' }
        }
        
        # 根据当前状态和请求状态，判断按键的操作
        if open_by == 'button':
            if req_mode == 1:  # 左转
                press_num = 1 if cur_mode != 1 else 2
                operate = 'left'
            elif req_mode == 2:  # 右转
                press_num = 1 if cur_mode != 2 else 2
                operate = 'right'
            elif req_mode == 3:  # 打开双闪
                self.set_hazard_button(True)
                return
        elif close_by == 'button' and req_mode == 0:
            if cur_mode == 1 or cur_mode == 2:  # 关闭左右转
                press_num = 1
                operate = 'left' if cur_mode == 1 else 'right'
            elif cur_mode == 0:  # 如果当前为关闭状态（可能是服务关闭，故仍需再按两次）
                press_num = 2
                operate = 'left' 
            elif cur_mode == 3:  # 关闭双闪
                self.set_hazard_button(False)
                return
        else:
            return

        # 执行左转向或右转向按键操作
        for i in range(press_num):
            self.ipdu.set(directions[operate]['bodycan'], directions[operate]['signal'], 0)
            sleep(0.2)
            self.ipdu.set(directions[operate]['bodycan'], directions[operate]['signal'], 1)
            sleep(0.2)
            self.ipdu.set(directions[operate]['bodycan'], directions[operate]['signal'], 0)
            sleep(0.2)
            logger.info(f"[set_turnlamp_by_button][{operate}_num:{i}/{press_num}]")

    
    def goto_turnlamp_state(self, state):
        """
        回到转向灯某个状态
        """
        target_state = copy.deepcopy(state)
        
        priority = target_state['priority']
        mode = target_state['mode']
        open_by = target_state['open_by']
        close_by = target_state['close_by']
        btn_stehold = False if target_state['btn_stehold'] is None else target_state['btn_stehold']
        mth_stehold = False if target_state['mth_stehold'] is None else target_state['mth_stehold']
        self.partner.empty_all()

        if mode != 0: # 方向盘设置角度
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3) 
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
        
        # 停止独占超时
        if self.timer_thread:
            self.timer_thread.cancel()
        self.DIPriority_start = False
        self.DIPriority_flag = False
                
        # 判断如果当前状态与目标状态相同则退出
        if target_state == self.curr_state:
            get_state = self.partner.send_request_and_return_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {})
            if get_state == {"out": {"mode": mode, "priority": priority}}:
                logger.info(f'[GOTO_STATE]:Already in {target_state} True')
                sleep(0.1)
                return True
        
        # 如果当前处于双闪模式，先关闭双闪
        if self.curr_state['mode'] == 3:
            self.set_hazard_button(False)
            
        # 释放当前模式控制权
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", 
                                         {"lamp": {"mode":0, "priority": 255}}, timeout=0.5) 
        sleep(1)
        
        # 设置目标状态
        get_state = self.partner.send_request_and_return_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {})
        if open_by == 'button' or close_by == 'button':
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampHold", {"flag": not btn_stehold}, timeout=0.5)
            # sleep(0.1)
            self.set_turnlamp_by_button(open_by, close_by, mode, get_state['out']['mode'])
        else:
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", 
                                             {"lamp": {"mode": mode, "priority": priority}, 
                                              "isSteerHold": mth_stehold}, timeout=0.5)
                
        if priority < 0x5f:
            sleep(1)

        if mode == 0 and priority >= 0x5f:
            priority = 0xff
        elif mode != 0 and priority == 0xff:
            priority = 0x5f
        elif mode == 3 :  
            priority = 0x5f
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {}, {"out": {"mode": mode, "priority": priority}})
        
        self.curr_state = target_state
        self.curr_state['mode'] = mode
        self.curr_state['priority'] = priority   

        logger.info(f'[GOTO_STATE]:{target_state} True')
        return True

    def timer_handle(self):
        """
        独占控制权的优先级超时后更新DIPriority_flag和curr_state['priority']状态。
        """
        # self.DIPriority_start = False
        self.DIPriority_flag = False
        self.curr_state['priority'] = 0xff
        logger.info(f"[timer_handle] DIPriority_start:{self.DIPriority_start}, DIPriority_flag:{self.DIPriority_flag}")

    def handle_turnlamp(self, req_state):      
        """
        执行转向灯请求
        """
        req_open = req_state['open_by']
        req_close = req_state['close_by']
        req_priority = req_state['priority']
        req_mode = req_state['mode']
        req_btn_stehold = False if req_state['btn_stehold'] is None else req_state['btn_stehold']
        req_mth_stehold = False if req_state['mth_stehold'] is None else req_state['mth_stehold']
        
        self.partner.empty_all()
        if req_mode != 0: # 方向盘设置角度
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrQf', 3) 
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.8)
             
        # 接口开或关转向
        if req_open == 'method' or req_close == 'method':
            if self.DIPriority_start and not self.DIPriority_flag:
                self.DIPriority_start = False
            self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode", 
                                             {"lamp": {"mode": req_mode, "priority": req_priority}, 
                                              "isSteerHold": req_mth_stehold}, timeout=0.5)
            # 如果优先级大于当前优先级并且有独占控制权，取消原来timer线程，新启timer线程
            if req_state['service_ctrl'] and req_priority <= self.curr_state['priority']:
                if self.timer_thread:
                    self.timer_thread.cancel()
                self.DIPriority_start = True
                self.DIPriority_flag = True
                self.timer_thread = threading.Timer(5.0, self.timer_handle)
                self.timer_thread.daemon = True
                self.timer_thread.start()
                logger.info(f"[handle_turnlamp] DIPriority_start:{self.DIPriority_start}, DIPriority_flag:{self.DIPriority_flag}")
            elif req_priority == 0xff or (req_priority <= self.curr_state['priority'] < 0x5f and req_mode == 3):
                if self.timer_thread:
                    self.timer_thread.cancel()
                self.DIPriority_start = False
                self.DIPriority_flag = False
                
        # 按键开或关转向
        elif req_open == 'button' or req_close == 'button':
            if req_open == 'button':
                self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampHold", 
                                                {"flag": not req_btn_stehold}, timeout=0.5)
                sleep(0.2)
            self.set_turnlamp_by_button(req_open, req_close, req_mode, self.curr_state['mode'])
            
        # 回正关转向
        elif req_close == 'angle': 
            if self.curr_state['mode'] == 1:
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.53)
                sleep(0.2)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', 0.52)
            else:
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.53)
                sleep(0.2)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr02, 'SteerWhlSnsrAg', -0.52)                

        return 
            
    def set_turnlamp_state(self, state):
        """
        设置转向灯状态，根据优先级不同等仲裁逻辑判断是否响应请求
        """
        req_state = copy.deepcopy(state)
        handle_start = False
        handle_end = False
        
        req_open = req_state['open_by']
        req_close = req_state['close_by']
        req_priority = req_state['priority']
        req_mode = req_state['mode']
        exp_mode = req_mode
        exp_priority = req_priority
        
        get_state = self.partner.send_request_and_return_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {})
        cur_mode = self.curr_state['mode'] = get_state['out']['mode']
        cur_priority = self.curr_state['priority'] = get_state['out']['priority']
        cur_open = self.curr_state['open_by'] 
        cur_close = self.curr_state['close_by']    
             
        # 判断是否检查event
        if (cur_priority > req_priority) or \
            (cur_priority == req_priority and cur_mode != req_mode) or \
            (req_priority == 0xff and cur_mode != req_mode):
            check_event = True 
        else:
            check_event = False
        logger.info(f"[set_turnlamp_state] current mode:{cur_mode}, current priority:{cur_priority}, hazard_button:{self.hazard_button}, DIPriority_flag:{self.DIPriority_flag}")

        # 处理转向灯请求
        handle_start = self.DIPriority_flag
        self.handle_turnlamp(req_state)
        handle_end = self.DIPriority_flag

        # 检查转向灯预期状态
        # 如果请求mode为3双闪，预期优先级为0x5f
        if req_mode == 3 :  
            exp_priority = 0x5f
            if cur_mode == 3:
                check_event = False
            logger.info(f"[set_turnlamp_state] expect condition 0")   
        # 如果当前为按键开的双闪，服务无法关闭，但服务或按键可以设置左转右转
        if self.hazard_button and req_close == 'method' and req_mode == 0:
            exp_mode = 3
            if cur_mode != 3:
                exp_priority = 0x5f                
            logger.info(f"[set_turnlamp_state] expect condition 1")   
        
        # 如果请求优先级高于或等于当前优先级，并且高于0x5f有独占控制权，等待1s
        if req_priority <= cur_priority and req_priority < 0x5f:
            sleep(1)
            logger.info(f"[set_turnlamp_state] expect condition 2")   
        # 如果请求优先级比当前优先级低，则不执行，优先级和mode仍为当前值
        elif (cur_priority < req_priority < 0xff) and (not (req_mode == 3 and req_open == 'button')):
            exp_priority = cur_priority
            exp_mode = cur_mode
            sleep(1)
            logger.info(f"[set_turnlamp_state] expect condition 3")
        # 如果请求状态为关闭，并且请求优先级高于当前优先级低于0x5f, 预期优先级为0xff
        elif req_mode == 0 and 0x5f <= req_priority <= cur_priority and \
            not (cur_mode == 3 and req_close == 'angle'):
            exp_priority = 0xff
            if cur_priority == 0xff:
                check_event = False
            if self.hazard_button and not (req_close == 'button' and cur_mode ==3):
                # exp_priority = 0x5f 
                exp_mode = 3
                # check_event = True
            logger.info(f"[set_turnlamp_state] expect condition 4")
        # 如果请求优先级为0xff，mode不为0，预期优先级为0x5f
        elif req_priority == 0xff and req_mode != 0:
            exp_priority = 0x5f
            self.DIPriority_start = False
            logger.info(f"[set_turnlamp_state] expect condition 5")
            
        # # 如果请求是关闭双闪，预期状态为开双闪前的状态
        if req_mode == 0 and req_close == 'button' and self.hazard_button:
            exp_priority = self.storage_state['priority']
            exp_mode = self.storage_state['mode']
            logger.info(f"[set_turnlamp_state] expect condition 6")
            
        # 如果关闭方式为方向盘回正关，且当前打开的方式为禁止回正关，或者当前mode为3，则不执行关闭
        if req_close == 'angle' and (self.curr_state['btn_stehold'] is False or \
                                     self.curr_state['mth_stehold'] is False or \
                                     cur_mode == 3): 
            exp_priority = cur_priority
            exp_mode = cur_mode
            check_event = False
            logger.info(f"[set_turnlamp_state] expect condition 7")
        elif req_close == 'angle' and cur_mode != 3 and (self.curr_state['btn_stehold'] is True or \
                                                         self.curr_state['mth_stehold'] is True):
            exp_priority = 0xff
            if cur_priority == 0xff:
                check_event = False
            logger.info(f"[set_turnlamp_state] expect condition 8")
        
        # 如果独占优先级超时(超过5s)
        if self.DIPriority_start and not self.DIPriority_flag:
            if cur_mode == 3 and not self.hazard_button:
                exp_priority = 0x5f
            if (handle_start and handle_end) or req_mode == 0:
                exp_priority = 0xff
            if req_open == 'button' or req_close == 'button': # 按键过程中随时可能出现独占超时，预期可能为0x5f或0xff   
                sleep(0.5) 
                get_state = self.partner.send_request_and_return_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {})
                exp_priority = get_state['out']['priority']
                exp_mode = get_state['out']['mode']
                assert exp_priority in [0x5f, 0xff]
            self.DIPriority_start = False
            logger.info(f"[set_turnlamp_state] expect condition 9")
            
        logger.info(f"[set_turnlamp_state] expect mode:{exp_mode}, expect priority:{exp_priority}, check event:{check_event}")

        # 检查转向灯状态是否符合预期
        if check_event:
            self.partner.ck_s2s_event(LIGHT_SERVICE_CLIENT, "NotifyTurnLampStatus", 
                                      {"sts": {"mode": exp_mode, "priority": exp_priority}})
        self.partner.send_request_and_ck_resp(LIGHT_SERVICE_CLIENT, "GetTurnLampStatus", {},
                                              {"out": {"mode": exp_mode, "priority": exp_priority}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'IndcrSts', exp_mode, timeout=1)
        
        # 更新当前状态
        self.curr_state = req_state
        self.curr_state['mode'] = exp_mode
        self.curr_state['priority'] = exp_priority 

        return


@allure.feature("SOA服务接口")
@allure.story("整车控制/LightService")  # 转向灯
class TestTurnLamp(TestBase):
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
                                     ])
        self.partner.method_default_timeout = 0.1
        sleep(5)
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')

        self.tlc = TurnLampControl(self.partner, self.ipdu, self.sd_tester, self.io)
        self.tl_states = self.tlc.turnlamp_states

    def before_each_func(self, ecu):
        self.sd_tester.tester_present()
        self.ipdu.set_vehspd(0)  # 车速
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', 0)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', 0)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', 0)
        sleep(0.5)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 255}}, timeout=0.3)
        self.tlc.set_hazard_button(open=False)
        self.partner.empty_all()
        super().before_each_func(ecu, start=False)
        
    def after_each_func(self, ecu):
        self.sd_tester.stop_tester_present()
        self.ipdu.set_vehspd(0)  # 车速
        sleep(0.5)
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 255}}, timeout=0.5)
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.partner.send_method_request(LIGHT_SERVICE_CLIENT, "SetTurnLampMode",
                                         {"lamp": {"mode": 0, "priority": 255}}, timeout=0.5)
        self.tlc.set_hazard_button(open=False)
        self.partner.stop_operators()
        # self.nucapp.bgm_power_on()
        super().after_class(self, ecu)
    
    def test_caseid_fuzz1(self):
        """
        遍历测试转向灯每个状态，检查从当前状态切换到下一个状态是否成功。
        """
        curr_states = next_states = self.tl_states
        ret = []
        for index1, curr in enumerate(curr_states):  # [0:7] [7:19] [19:31] [31:]
            for index2, next in enumerate(next_states):
                try:
                    logger.info(f"[TEST_STATE index:{index1}]:{curr}")
                    self.tlc.goto_turnlamp_state(curr)
        
                    sleep(0.25)
                    
                    logger.info(f"[NEXT_STATE index:{index2}]:{next}")
                    self.tlc.set_turnlamp_state(next)
                    
                    logger.info(f"[TEST_STATE index:{index1}] TO [NEXT_STATE index:{index2}] SUCCESS")
                except AssertionError as e:
                    msg = f"[TEST_STATE index:{index1}]:{curr}->[NEXT_STATE index:{index2}]:{next} FAIL, error:{e}"
                    logger.error(msg)
                    ret.append(msg)
                    
        assert len(ret) == 0


    def test_caseid_fuzz2(self):
        """
        随机测试转向灯跳转到下一随机状态是否正确
        """
        ret = []
        loop_num = 100

        for i in range(loop_num):
            try:
                index = random.randint(0, len(self.tl_states)-1)
                state = self.tl_states[index]
                
                logger.info(f"[loop:{i}][NEXT_STATE index{index}]:{state} start...")
                self.tlc.set_turnlamp_state(state)
                logger.info(f"[loop:{i}][NEXT_STATE index{index}]:{state} PASS")
                sleep(1)
                
            except AssertionError as e:
                msg = f"[loop:{i}][NEXT_STATE index{index}]:{state} FAIL, error:{e}"
                logger.error(msg)
                ret.append(msg)
                
        assert len(ret) == 0                

