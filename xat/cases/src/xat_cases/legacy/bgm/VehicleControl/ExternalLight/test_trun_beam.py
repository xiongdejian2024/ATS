
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_extilight.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/11/9 11:30
@Description: BGM车控车设外灯
"""

import os
import sys
import pytest
import allure
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("车控车设")
@allure.story("后视镜功能")
class TestExltlightCtrlABC(TestABCBase):
    def before_class(self, ecu):
        self.soa.update([("LightService","client"),("LightService","client_1"),"CentralLockService_client"])
        sleep(2)
        # 检查双闪是否已经打开，如果打开先关闭
        ori_data = self.bus_comm.ipdu.check_signal(self.bus_comm.ipdu.bodycan.CemBodyFr03, 'ActvnOfIndcrIndcrOut', 3)
        check_result = check_signal_value_exist(ori_data, 3)
        if check_result:
            sleep(3)
            self.io.hazard_light_open()
            self.io.hazard_light_close()
            sleep(3)
            self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        else:
            check_result = check_signal_value_exist(ori_data, 1) or check_signal_value_exist(ori_data, 2)
            if check_result:
                self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
                sleep(6)

    def before_each_func(self, ecu):
        self.io.hazard_light_close()
        self.soa.start_get_light_inhibit_sts()
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_extral_light_button_to_defaul_sts()
        #mars1
        # ccp="A3 01 80 06 FD 03 02 01 A3 02 09 03 04 02 01 02 85 8B 06 01 00 04 05 02 03 00 00 02 04 8F 80 0C 01 01 03 01 02 01 82 02 01 02 16 01 07 01 01 01 00 04 01 02 02 85 89 02 02 01 02 09 02 7B 74 03 01 01 01 01 01 01 01 03 01 02 02 02 02 01 02 01 02 01 01 01 01 01 02 02 01 03 01 02 01 80 02 03 02 80 01 80 00 01 00 81 80 11 01 03 04 01 01 01 01 02 01 03 02 81 02 02 01 01 01 01 01 04 01 01 01 01 01 01 01 02 03 01 01 03 02 02 01 83 02 01 01 02 01 01 29 02 01 04 02 03 80 02 81 03 81 04 01 14 01 0A 80 01 01 01 02 01 02 02 03 82 05 02 05 01 02 02 01 01 80 04 01 02 01 01 01 02 02 03 01 01 01 03 02 02 03 04 02 04 02 01 01 01 03 02 0A 02 01 01 01 02 01 01 01 80 81 0A 01 02 04 01 07 07 0A 0A 07 07 0A 0A 00 00 04 00 01 02 02 02 01 01 01 01 80 03 03 01 02 00 00 00 02 02 02 01 02 02 04 02 01 01 02 00 00 00 01 03 00 01 03 00 01 81 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 01 01 00 00 00 00 00 00 00 01 00 01 01 00 00 02 01 00 00 80 00 00 00 00 84 03 01 03 00 00 00 00 02 01 00 00 00 00 00 00 00 00 00 02 01 80 01 02 01 01 01 01 01 02 01 03 02 01 80 01 80 02 02 02 01 01 01 02 05 03 80 01 06 01 03 01 10 01 00 03 03 01 00 00 00 00 00 03 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 00 00 00 00 00 02 01 03 01 00 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 02 01 01 00 00 00 00 02 04 03 02 01 01 01 02 02 02 04 82 01 02 01 01 02 03 02 03 01 01 02 02 01 01 01 01 01 02 02 02 04 01 02 01 01 01 01 01 03 02 00 00 02 80 02 02 02 01 01 02 01 02 02 01 02 03 01 03 02 02 01 01 01 01 01 01 01 01 00 01 04 01 02 01 02 05 02 02 02 04 08 08 08 08 03 02 01 04 02 01 02 02 01 01 01 02 01 01 01 03 01 01 01 00 00 00 00 00 00 01 02 03 01 02 01 10 03 01 01 01 02 02 02 01 01 03 01 04 02 04 01 01 01 01 01 02 03 03 05 05 02 00 01 01 02 01 01 01 01 01 01 01 02 01 01 01 01 01 01 01 01 01 01 01 02 01 02 02 01 01 02 01 01 01 01 01 00 01 04 00 00 00 02 01 00 02 01 01 04 04 00 00 01 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 02 02 05 08 08 02 01 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 01 02 01 02 02 02 02 01 02 02 02 01 01 01 02 01 01 02 02 01 01 02 01 02 02 01 02 01 01 01 01 02 01 01 01 01 02 01 01 01 01 01 02 01 01 01 00 01 01 01 01 01 02 02 02 01 01 01 01 02 01 01 01 01 01 01 02 02 01 02 02 01 01 02 01 01 01 00 01 01 01 01 01 01 01 02 01 01 01 01 01 02 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 02 02 01 01 01 01 02 02 00 00 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 00 01 01 01 01 01 01 02 02 02 01 01 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 02 02 02 02 02 02 01 02 02 02 01 02 02 02 01 01 02 02 01 01 02 02 02 02 01 01 00 02 02 02 02 02 01 02 02 02 01 02 00 01"
        # # ccp="A3 01 81 06 FD 03 01 01 A2 02 09 03 04 02 01 02 85 8B 06 01 00 04 05 02 03 00 00 01 04 8F 80 0C 01 01 01 01 02 01 82 02 01 02 16 01 07 01 01 01 00 03 01 02 02 80 89 02 03 01 01 03 02 73 72 03 01 01 01 01 01 01 01 03 01 02 02 02 02 0A 01 01 02 01 02 01 01 01 02 02 01 03 01 02 01 80 02 03 02 80 01 80 00 00 00 81 80 11 01 03 04 01 01 01 01 02 01 03 02 80 01 02 01 01 01 01 01 04 01 01 01 01 01 01 01 02 03 01 01 03 02 02 01 83 02 01 01 02 01 01 29 02 01 04 02 03 80 02 82 03 03 04 01 14 03 0A 80 01 04 01 02 01 02 02 03 82 05 02 05 01 01 02 01 01 80 04 01 02 01 01 01 02 05 02 01 01 00 03 02 02 03 04 02 02 02 01 01 01 02 00 01 01 01 01 01 01 01 01 01 80 03 0A 01 01 04 06 07 07 0A 0A 07 07 0A 0A 00 00 04 00 00 02 01 01 01 01 01 02 80 03 03 01 02 00 00 00 02 02 02 01 02 02 04 00 01 01 02 00 00 00 01 03 00 00 01 00 00 81 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80 00 00 00 00 00 00 00 00 00 00 01 00 01 01 00 00 02 00 00 00 80 00 00 00 00 84 03 01 01 00 00 00 00 02 01 00 00 00 00 00 00 00 00 00 02 01 80 01 02 01 01 01 01 01 02 01 03 02 01 80 01 80 02 02 01 01 01 01 01 05 03 80 02 06 01 03 01 10 00 00 02 03 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 00 00 00 00 00 02 01 03 01 00 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 03 02 01 00 00 00 00 00 85 04 01 02 02 02 01 02 02 02 04 85 01 02 01 01 02 80 04 03 01 01 02 02 01 03 01 01 01 02 02 02 04 01 02 01 01 01 01 01 03 00 00 00 01 80 02 02 01 01 02 02 01 02 02 02 01 02 01 03 02 02 01 01 01 01 01 01 01 01 00 01 03 01 02 01 01 05 02 03 03 04 01 01 01 01 03 01 01 04 02 01 02 01 01 01 01 02 01 01 01 01 01 01 01 00 00 00 00 00 00 01 02 03 01 02 01 10 03 01 01 01 02 01 02 01 01 03 01 04 01 04 01 01 01 01 01 02 01 03 01 05 02 00 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 02 01 01 01 01 01 02 01 01 01 01 02 06 00 00 01 01 04 01 01 00 00 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 03 02 02 08 01 00 00 01 02 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 02 02 02 02 01 02 02 01 01 02 02 02 02 02 02 02 02 01 02 02 01 02 01 02 02 02 02 01 02 02 02 02 01 02 02 02 02 02 02 01 02 02 01 02 02 01 02 01 01 01 01 02 01 01 01 01 02 01 01 01 00 01 02 01 01 01 00 01 01 01 01 01 02 02 02 01 01 01 02 02 01 01 01 01 01 01 02 02 01 02 02 01 01 01 01 01 01 00 01 01 01 01 01 01 01 02 01 01 01 01 01 02 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 02 02 02 01 01 01 01 02 02 00 00 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 00 01 01 01 01 01 01 02 02 02 01 01 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 02 02 02 02 02 02 02 01 02 02 02 01 02 02 01 01 01 02 02 01 01 02 02 02 02 02 01 00 02 02 02 02 02 01 02 02 02 01 02 00 01"
        # self.sd_tester.write_ccp_value(ccp)
        # self.io.bgm_power_off()
        # self.io.bgm_power_on()
        # sleep(10)
        # 读取ccp  方便后面进行恢复
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0x06],                                                                    recv=[0x62, 0xF1, 0x06])
        self.ccp_original_value = recv_data_list[3:1556 + 3]
        sleep(3)
        # 检查双闪是否已经打开，如果打开先关闭
        ori_data = self.bus_comm.ipdu.check_signal(self.bus_comm.ipdu.bodycan.CemBodyFr03, 'ActvnOfIndcrIndcrOut', 3)
        check_result = check_signal_value_exist(ori_data, 3)
        if check_result:
            sleep(3)
            self.io.hazard_light_open()
            self.io.hazard_light_close()
            sleep(3)
            self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        else:
            check_result = check_signal_value_exist(ori_data, 1) or check_signal_value_exist(ori_data, 2)
            if check_result:
                self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
                sleep(6)


    def after_each_func(self, ecu):
        self.soa.stop_get_light_inhibit_sts()
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)
        sleep(1)
        self.sd_tester.write_ccp_value(self.ccp_original_value)




    def after_class(self, ecu):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)

    def check_turn_lamp_flash_sts(self,act_sts_le:PosnLampSts,act_sts_ri:PosnLampSts,pos:IndcrSts):
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=act_sts_le,act_sts_ri=act_sts_ri,pos_sts=pos)
            self.bus_comm.check_turn_lamp_act_req(sts=pos,act_sts=pos)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=pos,act_sts=IndcrSts.Off)
    
    def check_hwl_lamp_flash_sts(self,flash_time:int,indcrdisp:IndcrSts=None):
        for num in range(flash_time):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos_sts=indcrdisp)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.Off)


    #--------------------------------------------->下面的是转向灯优先级的case<-----------------------------------------------------
    @allure.title("转向灯优先级验证_5S两次下发开启右转向灯_5s后高优先级可被打断")
    @pytest.mark.sanity
    def test_caseid_1985821(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        sleep(6)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)


    @allure.title("转向灯优先级验证_5S两次下发开启左转向灯_转向灯可服务关闭")
    @pytest.mark.sanity
    def test_caseid_1985816(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=255)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("转向灯优先级验证_5S两次下发开启右转向灯_转向灯可服务关闭")
    @pytest.mark.sanity
    def test_caseid_1985819(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=255)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("转向灯(DI)激活条件_自动右转指示要求_Normal Driving mode")
    @pytest.mark.sanity
    def test_caseid_113987(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)

    @allure.title("转向灯(DI)激活条件_自动左转指示要求_Normal Driving mode")
    @pytest.mark.sanity
    def test_caseid_113956(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)

    @allure.title("转向灯(DI)失活条件_失活自动左转指示要求_Normal Driving mode")
    @pytest.mark.smoke
    def test_caseid_114128(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)


    @allure.title("转向灯(DI)激活条件_方向改变时手动右转指示,旧方向盘")
    @pytest.mark.smoke
    def test_caseid_113968(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,ccp={629:4})
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        sleep(10)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
    
    
    @allure.title("转向灯优先级验证_5S两次下发开启左转向灯_高优先级不打断")
    @pytest.mark.sanity
    def test_caseid_1985820(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(6)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)


    @allure.title("转向灯优先级验证_5S两次下发开启左转向灯_转向灯可方向盘关闭")
    @pytest.mark.sanity
    def test_caseid_1985817(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=255)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("转向灯优先级验证_5S两次下发开启右转向灯_转向灯可方向盘关闭")
    @pytest.mark.sanity
    def test_caseid_1985818(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=255)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("转向灯优先级验证_服务开双闪_服务开右转开左转_5s后服务关闭右转_优先级判别")
    @pytest.mark.sanity
    def test_caseid_1985823(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        sleep(6)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("转向灯优先级验证_服务开双闪_按键关闭-按键开启右转_优先级判别")
    @pytest.mark.sanity
    def test_caseid_1985822(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)


    @allure.title("转向灯优先级验证_服务开启关闭双闪_按键开启双闪_服务关闭双闪_优先级判别")
    @pytest.mark.sanity
    def test_caseid_1985824(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=255)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=255)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=255) #按键开启HWL，只能按键关闭，服务会关闭失败
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close() #恢复HWL为关闭状态，防止影响后续case
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("转向灯优先级验证_高优先级关闭_方控右转失效_优先级判别")
    @pytest.mark.sanity
    def test_caseid_1985924(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(6)  #恢复环境

    
    @allure.title("转向灯优先级验证_95服务开右方控关_111服务开方向盘回正_优先级判别")
    @pytest.mark.sanity
    def test_caseid_1992984(self):
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrQf', 3)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.send_method_request("LightService_client","SetTurnLampMode",
                                     {"lamp": {"mode": 2, "priority": 95},"isSteerHold":False})
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.send_method_request("LightService_client","SetTurnLampMode",
                                     {"lamp": {"mode": 2, "priority": 111},"isSteerHold":True})
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.RiOn,act_sts=IndcrSts.RiOn)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', -0.8)
        sleep(2)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', -0.52)
        sleep(2)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("转向灯优先级验证_方控打开关闭-111服务右转开方向盘回正_优先级判别")
    @pytest.mark.sanity
    def test_caseid_1992590(self):
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrQf', 3)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.send_method_request("LightService_client","SetTurnLampMode",
                                     {"lamp": {"mode": 2, "priority": 111},"isSteerHold":True})
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', -0.8)
        sleep(1)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', -0.52)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("转向灯优先级验证_方控打开关闭-111服务左转开方向盘回正_优先级判别")
    @pytest.mark.sanity
    def test_caseid_1992591(self):
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrQf', 3)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.send_method_request("LightService_client","SetTurnLampMode",
                                     {"lamp": {"mode": 1, "priority": 111},"isSteerHold":True})
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.LeOn)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.8)
        sleep(1)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.52)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("转向灯优先级验证_95服务开左方控关_111服务开方向盘回正_优先级判别")
    @pytest.mark.sanity
    def test_caseid_1992986(self):
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrQf', 3)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        sleep(6)
        self.soa.send_method_request("LightService_client","SetTurnLampMode",
                                     {"lamp": {"mode": 1, "priority": 95},"isSteerHold":False})
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.send_method_request("LightService_client","SetTurnLampMode",
                                     {"lamp": {"mode": 1, "priority": 111},"isSteerHold":True})
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.8)
        sleep(2)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.52)
        sleep(2)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("转向灯优先级验证_111服务右开方向盘回正_优先级判别")
    @pytest.mark.sanity
    def test_caseid_1992988(self):
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrQf', 3)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.send_method_request("LightService_client","SetTurnLampMode",
                                     {"lamp": {"mode": 2, "priority": 111},"isSteerHold":True})
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.send_method_request("LightService_client", "SetTurnLampHold", {"flag": 0})
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', -0.8)
        sleep(1)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', -0.52)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("转向灯优先级验证_111服务左开方向盘回正_优先级判别")
    @pytest.mark.sanity
    def test_caseid_1992987(self):
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrQf', 3)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.send_method_request("LightService_client","SetTurnLampMode",
                                     {"lamp": {"mode": 1, "priority": 111},"isSteerHold":True})
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.send_method_request("LightService_client", "SetTurnLampHold", {"flag": 0})
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.8)
        sleep(1)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.52)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title(" 转向灯优先级验证_47服务周期关_95控制开_优先级判别")
    @pytest.mark.sanity
    def test_caseid_1993379(self):
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrQf', 3)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=255)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)
        self.soa.send_method_request("LightService_client_1", "SetTurnLampMode", {"lamp": {"mode":1, "priority": 95}})
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)
        sleep(6)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title(" 转向灯优先级验证_111服务周期开 95控制关_优先级判别")
    @pytest.mark.sanity
    def test_caseid_1993378(self):
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrQf', 3)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.send_method_request("LightService_client_1", "SetTurnLampMode", {"lamp": {"mode":0, "priority": 95}})
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        # 恢复
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=111)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        

    @allure.title("转向灯优先级验证_111服务周期开 按键控制关_优先级判别")
    @pytest.mark.sanity
    def test_caseid_1993377(self):
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrQf', 3)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.send_method_request("LightService_client","SetTurnLampMode",
                                     {"lamp": {"mode": 1, "priority": 111},"isSteerHold":True})
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(0.3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        # 恢复
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=111)
        sleep(0.3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("转向灯(DI)激活条件_手动右转变道指示_Normal Driving mode")
    @pytest.mark.smoke
    def test_caseid_113958(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47) #恢复环境
        sleep(6)  

    @allure.title("转向灯优先级验证_服务开右转_方控开左转_优先级判别")
    @pytest.mark.sanity
    def test_caseid_1985923(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=255)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)


    @allure.title("转向灯(DI)失活条件_DM/MP下失活自动右转指示要求_Normal Driving mode")
    @pytest.mark.smoke
    def test_caseid_114269(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("转向灯(DI)激活条件_方向改变时手动左转指示__Normal Driving mode")
    @pytest.mark.smoke
    def test_caseid_113947(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)

    @allure.title("转向灯（DI）激活过程_手动|主动变道辅助系统 (ALCA)自动|滑动门|自动泊车辅助 （APA）右转指示请求_满足DI激活条件右1转向灯状态信号故障")
    @pytest.mark.sanity
    @pytest.mark.bedug
    def test_caseid_113921(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        sleep(0.3)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearRight,sts=ExtrLtgSts.Err)
        for num in range(3):
            self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 2)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrRi', 2)
            sleep(.4)
            self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrRi', 0)
        for num in range(3):
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 2)
            sleep(.2)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)

    @allure.title("转向灯（DI）激活过程_手动|自动驾驶功能请求自动左转指示_满足DI激活条件左1转向灯状态信号故障")
    @pytest.mark.full
    @pytest.mark.mcu_test
    def test_caseid_113917(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        sleep(0.3)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearLeft,sts=ExtrLtgSts.Err)
        for num in range(3):
            self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 1)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrLe', 2)
            sleep(.4)
            self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrRi', 0)
        for num in range(3):
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 2)
            sleep(.2)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)

    @allure.title("转向灯（DI）激活过程_手动|自动驾驶功能请求自动左转指示_满足DI激活条件左前转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_113916(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        sleep(0.3)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontLeft,sts=ExtrLtgSts.Err)
        for num in range(3):
            self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 1)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrLe', 2)
            sleep(.4)
            self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrRi', 0)
        for num in range(3):
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 2)
            sleep(.2)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)

    @allure.title("转向灯（DI）激活过程_手动|自动驾驶功能请求自动左转指示_满足DI激活条件转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_113915(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        sleep(0.3)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontLeft,sts=ExtrLtgSts.Err)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearLeft,sts=ExtrLtgSts.Err)
        for num in range(3):
            self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 1)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrLe', 2)
            sleep(.4)
            self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrRi', 0)
        for num in range(3):
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 2)
            sleep(.2)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)

    @allure.title("转向灯（DI）激活过程_手动|自动驾驶功能请求自动左转指示_满足DI激活条件转向灯状态信号正常")
    @pytest.mark.full
    def test_caseid_113914(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        sleep(0.3)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)

    @allure.title("转向灯(DI)失活条件_失活变道时手动右转指示_开关状态右侧轻按开时左侧故障Normal Driving mode")
    @pytest.mark.full
    def test_caseid_114158(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(0.3)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.Error)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        for num in range(3):
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 1)
            sleep(.2)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)

    #-------------------------------------------------------------------------------------------------------------------
    
    @allure.title("转向灯(DI)激活条件_方向改变时手动右转指示__Dyno Driving mode")
    @pytest.mark.full
    def test_caseid_113986(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
        
    @allure.title("转向灯(DI)激活条件_方向改变时手动右转指示__Dyno Active mode")
    @pytest.mark.full
    def test_caseid_113985(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")

    @allure.title("转向灯(DI)激活条件_方向改变时手动右转指示__Crash Driving mode")
    @pytest.mark.full
    def test_caseid_113984(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")

    @allure.title("转向灯(DI)激活条件_方向改变时手动右转指示__Crash Active mode")
    @pytest.mark.full
    def test_caseid_113983(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")

    @allure.title("转向灯(DI)激活条件_方向改变时手动右转指示__Factory Driving mode")
    @pytest.mark.full
    def test_caseid_113982(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")

    @allure.title("转向灯(DI)激活条件_方向改变时手动右转指示__Factory Active mode")
    @pytest.mark.full
    def test_caseid_113981(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")

    @allure.title("转向灯(DI)激活条件_方向改变时手动右转指示__Transport Driving mode")
    @pytest.mark.full
    def test_caseid_113980(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")

    @allure.title("转向灯(DI)激活条件_方向改变时手动右转指示__Transport Active mode")
    @pytest.mark.full
    def test_caseid_113979(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")

    @allure.title("转向灯(DI)激活条件_方向改变时手动右转指示__Normal Active mode")
    @pytest.mark.full
    def test_caseid_113977(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")

    @allure.title("转向灯(DI)失活条件_打断变道手动右转指示轻触后松开轻触左_Dyno Driving mode")
    @pytest.mark.full
    def test_caseid_114198(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)
        sleep(5.1)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
        sleep(1)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")

    @allure.title("转向灯(DI)失活条件_打断变道手动右转指示轻触后松开轻触左_Dyno Active mode")
    @pytest.mark.full
    def test_caseid_114197(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)
        sleep(5.1)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
        sleep(1)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
       

    @allure.title("转向灯(DI)失活条件_打断变道手动右转指示轻触后松开轻触左_Crash Driving mode")
    @pytest.mark.full
    def test_caseid_114196(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
        sleep(1)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
       
    @allure.title("转向灯(DI)失活条件_打断变道手动右转指示轻触后松开轻触左_Factory Driving mode")
    @pytest.mark.full
    def test_caseid_114194(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
        sleep(1)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
       
    @allure.title("转向灯(DI)失活条件_打断变道手动右转指示轻触后松开轻触左_Factory Active mode")
    @pytest.mark.full
    def test_caseid_114193(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
        sleep(1)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
       

    @allure.title("转向灯(DI)失活条件_打断变道手动右转指示轻触后松开轻触左_Transport Driving mode")
    @pytest.mark.full
    def test_caseid_114192(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
        sleep(1)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
       
    @allure.title("转向灯(DI)失活条件_打断变道手动右转指示轻触后松开轻触左_Transport Active mode")
    @pytest.mark.full
    def test_caseid_114191(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
        sleep(1)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
       

    @allure.title("转向灯(DI)失活条件_打断变道手动右转指示轻触后松开轻触左_Normal Driving mode")
    @pytest.mark.full
    def test_caseid_114190(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
        sleep(1)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
       

    @allure.title("转向灯(DI)失活条件_打断变道手动右转指示轻触后松开轻触左_Normal Active mode")
    @pytest.mark.full
    def test_caseid_114189(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
        sleep(1)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
       

    @allure.title("转向灯(DI)失活条件_打断变道手动右转指示轻触后松开轻触右_Dyno Driving mode")
    @pytest.mark.full
    def test_caseid_114188(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
        sleep(1)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_right_light_off()
       
    @allure.title("转向灯(DI)失活条件_打断变道手动右转指示轻触后松开轻触右_Dyno Active mode")
    @pytest.mark.full
    def test_caseid_114187(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
        sleep(1)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_right_light_off()
       

    @allure.title("转向灯(DI)失活条件_打断变道手动右转指示轻触后松开轻触右_Factory Driving mode")
    @pytest.mark.full
    def test_caseid_114184(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
        sleep(1)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_right_light_off()
       

    @allure.title("转向灯(DI)失活条件_打断变道手动右转指示轻触后松开轻触右_Factory Active mode")
    @pytest.mark.full
    def test_caseid_114183(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
        sleep(1)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_right_light_off()
       

    @allure.title("转向灯(DI)失活条件_打断变道手动右转指示轻触后松开轻触右_Transport Driving mode")
    @pytest.mark.full
    def test_caseid_114182(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
        sleep(1)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_right_light_off()
       

    @allure.title("转向灯(DI)失活条件_打断变道手动右转指示轻触后松开轻触右_Transport Active mode")
    @pytest.mark.full
    def test_caseid_114181(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
        sleep(1)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_right_light_off()
       

    @allure.title("转向灯(DI)失活条件_打断变道手动右转指示轻触后松开轻触右_Normal Driving mode")
    @pytest.mark.full
    def test_caseid_114180(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
        sleep(1)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_right_light_off()
       

    @allure.title("转向灯(DI)失活条件_打断变道手动右转指示轻触后松开轻触右_Normal Driving mode")
    @pytest.mark.full
    def test_caseid_114180(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
        sleep(1)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_right_light_off()
       

    @allure.title("转向灯(DI)失活条件_打断变道手动右转指示轻触后松开轻触右_Normal Active mode")
    @pytest.mark.full
    def test_caseid_114179(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
        sleep(1)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_right_light_off()
       
    
    @allure.title("SWTL方控左转左打方向盘45°回正到30°以下关闭左转Dyno Driving mode")
    @pytest.mark.full
    def test_caseid_114127(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        sleep(3)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.52)
        self.bus_comm.check_left_light_off()
       

    @allure.title("SWTL方控左转左打方向盘45°回正到30°以下关闭左转Dyno Active mode")
    @pytest.mark.full
    def test_caseid_114126(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        sleep(3)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.52)
        self.bus_comm.check_left_light_off()
       

    @allure.title("SWTL方控左转左打方向盘45°回正到30°以下关闭左转Crash Driving mode")
    @pytest.mark.full
    def test_caseid_114125(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.8)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.52)
        self.bus_comm.check_left_light_off()
       
    
    @allure.title("SWTL方控左转左打方向盘45°回正到30°以下关闭左转Crash Active mode")
    @pytest.mark.full
    def test_caseid_114124(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.8)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.52)
        self.bus_comm.check_left_light_off()
        
    @allure.title("SWTL方控左转左打方向盘45°回正到30°以下关闭左转Factory Driving mode")
    @pytest.mark.full
    def test_caseid_114123(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        sleep(3)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.52)
        self.bus_comm.check_left_light_off()
       

    @allure.title("SWTL方控左转左打方向盘45°回正到30°以下关闭左转Factory Active mode")
    @pytest.mark.full
    def test_caseid_114122(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        sleep(3)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.52)
        self.bus_comm.check_left_light_off()
       
    @allure.title("SWTL方控左转左打方向盘45°回正到30°以下关闭左转Transport Driving mode")
    @pytest.mark.full
    def test_caseid_114121(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        sleep(3)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.52)
        self.bus_comm.check_left_light_off()
       

    @allure.title("SWTL方控左转左打方向盘45°回正到30°以下关闭左转Transport Active mode")
    @pytest.mark.full
    def test_caseid_114120(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        sleep(3)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.52)
        self.bus_comm.check_left_light_off()
       

    @allure.title("SWTL方控左转左打方向盘45°回正到30°以下关闭左转Normal Driving mode")
    @pytest.mark.full
    def test_caseid_114119(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        sleep(3)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.52)
        self.bus_comm.check_left_light_off()
       

    @allure.title("SWTL方控左转左打方向盘45°回正到30°以下关闭左转Normal Active mode")
    @pytest.mark.full
    def test_caseid_114118(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        sleep(3)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.52)
        self.bus_comm.check_left_light_off()
       
    @allure.title("转向灯(DI)失活条件_失活方向改变时手动左转指示松开左轻触右_Normal Driving mode")
    @pytest.mark.full
    def test_caseid_114059(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        sleep(1)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")

    @allure.title("转向灯(DI)失活条件_失活方向改变时手动左转指示松开左轻触右_Dyno Driving mode")
    @pytest.mark.full
    def test_caseid_114067(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        sleep(1)
        self.bus_comm.set("bodycan","SwtrBodyFr01","SteerWhlTouchSwtRi2SteerWhlTouchSwt2",0)
        self.bus_comm.check_left_light_off()

    @allure.title("转向灯(DI)失活条件_失活方向改变时手动左转指示松开左轻触右_Dyno Active mode")
    @pytest.mark.full
    def test_caseid_114066(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        sleep(1)
        self.bus_comm.set("bodycan","SwtrBodyFr01","SteerWhlTouchSwtRi2SteerWhlTouchSwt2",0)
        self.bus_comm.check_left_light_off()

    @allure.title("转向灯(DI)失活条件_失活方向改变时手动左转指示松开左轻触右_Transport Driving mode")
    @pytest.mark.full
    def test_caseid_114061(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        sleep(1)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")

    @allure.title("转向灯(DI)失活条件_失活方向改变时手动左转指示松开左轻触右_Crash Driving mode")
    @pytest.mark.full
    def test_caseid_114065(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
        
    @allure.title("转向灯(DI)失活条件_失活方向改变时手动左转指示松开左轻触右_Factory Driving mode")
    @pytest.mark.full
    def test_caseid_114063(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        sleep(1)
        self.bus_comm.set("bodycan","SwtrBodyFr01","SteerWhlTouchSwtRi2SteerWhlTouchSwt2",0)
        self.bus_comm.check_left_light_off()

    @allure.title("转向灯(DI)失活条件_失活方向改变时手动左转指示松开左轻触右_Factory Active mode")
    @pytest.mark.full
    def test_caseid_114062(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        sleep(1)
        self.bus_comm.set("bodycan","SwtrBodyFr01","SteerWhlTouchSwtRi2SteerWhlTouchSwt2",0)
        self.bus_comm.check_left_light_off()

    @allure.title("转向灯(DI)失活条件_失活方向改变时手动左转指示松开左轻触右_Transport Active mode")
    @pytest.mark.full
    def test_caseid_114060(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        sleep(1)
        self.bus_comm.set("bodycan","SwtrBodyFr01","SteerWhlTouchSwtRi2SteerWhlTouchSwt2",0)
        self.bus_comm.check_left_light_off()

    @allure.title("转向灯(DI)失活条件_失活方向改变时手动左转指示松开左轻触右_Normal Active mode")
    @pytest.mark.full
    def test_caseid_114058(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        sleep(1)
        self.bus_comm.set("bodycan","SwtrBodyFr01","SteerWhlTouchSwtRi2SteerWhlTouchSwt2",0)
        self.bus_comm.check_left_light_off()

    @allure.title("转向灯(DI)失活条件_打断变道手动左转指示轻触后松开轻触左_Dyno Driving mode")
    @pytest.mark.full
    def test_caseid_114047(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        sleep(1)
        self.bus_comm.set("bodycan","SwtlBodyFr01","SteerWhlTouchSwtLe2SteerWhlTouchSwt2",0)
        self.bus_comm.set("bodycan","SwtlBodyFr01","SteerWhlTouchSwtLe2SteerWhlTouchSwt2",1)
        self.bus_comm.check_left_light_off()

    @allure.title("转向灯(DI)失活条件_打断变道手动左转指示轻触后松开轻触左_Dyno Active mode")
    @pytest.mark.full
    def test_caseid_114046(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        sleep(1)
        self.bus_comm.set("bodycan","SwtlBodyFr01","SteerWhlTouchSwtLe2SteerWhlTouchSwt2",0)
        self.bus_comm.set("bodycan","SwtlBodyFr01","SteerWhlTouchSwtLe2SteerWhlTouchSwt2",1)
        self.bus_comm.check_left_light_off()


    @allure.title("转向灯(DI)失活条件_失活变道时手动左转指示_开关状态左侧轻按开时右侧轻按_Dyno Driving mode")
    @pytest.mark.full
    def test_caseid_114015(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        sleep(1)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")


    @allure.title("转向灯(DI)激活条件_变道时手动右转指示时轻触后断开_Crash Driving mode")
    @pytest.mark.full
    def test_caseid_113974(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
        sleep(1)
        self.bus_comm.set("bodycan","SwtrBodyFr01","SteerWhlTouchSwtRi2SteerWhlTouchSwt2",0)
        self.bus_comm.check_right_light_off()


    @allure.title("转向灯(DI)激活条件_手动右转变道指示_car mode is carch and usagemode is driving")
    @pytest.mark.full
    def test_caseid_113964(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")

    @allure.title("转向灯(DI)激活条件_手动右转变道指示_Dyno Active mode")
    @pytest.mark.full
    def test_caseid_113965(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")

    @allure.title("转向灯(DI)激活条件_手动右转变道指示_Factory Driving mode")
    @pytest.mark.full
    def test_caseid_113962(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")

    @allure.title("转向灯(DI)激活条件_手动右转变道指示_Factory Active mode")
    @pytest.mark.full
    def test_caseid_113961(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")

    @allure.title("转向灯(DI)激活条件_手动右转变道指示_Transport Driving mode")
    @pytest.mark.full
    def test_caseid_113960(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")

    @allure.title("转向灯(DI)激活条件_手动右转变道指示_Transport Active mode")
    @pytest.mark.full
    def test_caseid_113959(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")

    @allure.title("转向灯(DI)激活条件_手动右转变道指示_Normal Active mode")
    @pytest.mark.full
    def test_caseid_113957(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")

    @allure.title("转向灯(DI)激活条件_方向改变时手动左转指示__Dyno Driving mode")
    @pytest.mark.full
    def test_caseid_113955(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")

    @allure.title("转向灯(DI)激活条件_方向改变时手动左转指示__Dyno Active mode")
    @pytest.mark.full
    def test_caseid_113954(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")

    @allure.title("转向灯(DI)激活条件_方向改变时手动左转指示__Crash Driving mode")
    @pytest.mark.full
    def test_caseid_113953(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")

    @allure.title("转向灯(DI)激活条件_方向改变时手动左转指示__Factory Driving mode")
    @pytest.mark.full
    def test_caseid_113951(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")

    @allure.title("转向灯(DI)激活条件_方向改变时手动左转指示__Factory Active mode")
    @pytest.mark.full
    def test_caseid_113950(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")

    @allure.title("转向灯(DI)激活条件_方向改变时手动左转指示__Transport Driving mode")
    @pytest.mark.full
    def test_caseid_113949(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")

    @allure.title("转向灯(DI)激活条件_方向改变时手动左转指示__Transport Active mode")
    @pytest.mark.full
    def test_caseid_113948(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")

    @allure.title("转向灯(DI)激活条件_方向改变时手动左转指示__Normal Active mode")
    @pytest.mark.full
    def test_caseid_113946(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
    
    @allure.title("转向灯(DI)激活条件_变道时手动左转指示_Normal Active mode")
    @pytest.mark.full
    def test_caseid_113926(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")

    @allure.title("转向灯（DI）失活过程_手动|主动变道辅助系统 (ALCA)自动|滑动门|自动泊车辅助 （APA）右转指示请求_满足DI失活条件失活转向灯")
    @pytest.mark.full
    def test_caseid_113923(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
        sleep(3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.bus_comm.check_left_light_off()

    @allure.title("转向灯（DI）失活过程_手动|自动驾驶功能请求自动左转指示_满足DI失活条件失活转向灯")
    @pytest.mark.full
    def test_caseid_113922(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        sleep(3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.bus_comm.check_left_light_off()

        
    @allure.title("转向灯（DI）激活过程_手动|主动变道辅助系统 (ALCA)自动|滑动门|自动泊车辅助 （APA）右转指示请求_满足DI激活条件转向灯状态信号正常")
    @pytest.mark.full
    def test_caseid_113918(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")
        
    
    @allure.title("前后转向灯和位置灯RTI|RPL和FTI|FPL混合控制__在右DI时相应侧DRL和Pos")
    @pytest.mark.full
    def test_caseid_113925(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check("bodyexposedcanfd","CemBodyExpoFr50","ActnOfLedDaytiRunngLamp",0)
        self.bus_comm.check("backbonefr","CemBackBoneFr02","ExtrLtgStsDRL",1)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Position)
        self.bus_comm.check("bodyexposedcanfd","CemBodyExpoFr50","ActnOfLedPosnLamp",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr02","ExtrLtgStsPosLiRe",1)
        self.bus_comm.set_turn_right_wheel(wheel="right_old")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="right")
     
        
    @allure.title("前后转向灯和位置灯RTI|RPL和FTI|FPL混合控制__在左DI时相应侧DRL和Pos关闭")
    @pytest.mark.full
    def test_caseid_113924(self):
        self.sd_tester.write_ccp({629:4})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check("bodyexposedcanfd","CemBodyExpoFr50","ActnOfLedDaytiRunngLamp",0)
        self.bus_comm.check("backbonefr","CemBackBoneFr02","ExtrLtgStsDRL",1)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Position)
        self.bus_comm.check("bodyexposedcanfd","CemBodyExpoFr50","ActnOfLedPosnLamp",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr02","ExtrLtgStsPosLiRe",1)
        self.bus_comm.set_turn_right_wheel(wheel="left")
        self.bus_comm.check_wheel_light_on_and_light_off(direction="left")

    
    @allure.title("转向灯(DI)失活条件_失活变道时手动左转指示_开关状态左侧轻按开时右侧故障_Dyno Active mode")
    @pytest.mark.full
    def test_caseid_114014(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(0.3)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.Error)
        for num in range(3):
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 2)
            sleep(.2)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)

    @allure.title("转向灯(DI)失活条件_失活变道时手动左转指示_开关状态左侧轻按开时右侧故障_Dyno Driving mode")
    @pytest.mark.full
    def test_caseid_114017(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(0.3)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.Error)
        for num in range(3):
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 2)
            sleep(.2)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)

    @allure.title("转向灯(DI)失活条件_打断变道手动左转指示轻触后松开轻触左_Crash Driving mode")
    @pytest.mark.full
    def test_caseid_114045(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)

    @allure.title("转向灯(DI)失活条件_打断变道手动左转指示轻触后松开轻触左_Factory Active mode")
    @pytest.mark.full
    def test_caseid_114042(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)

    @allure.title("转向灯(DI)失活条件_打断变道手动左转指示轻触后松开轻触左_Factory Driving mode")
    @pytest.mark.full
    def test_caseid_114043(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)

    @allure.title("转向灯(DI)失活条件_打断变道手动左转指示轻触后松开轻触左_Normal Active mode")
    @pytest.mark.full
    def test_caseid_114038(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("转向灯(DI)失活条件_打断变道手动左转指示轻触后松开轻触左_Normal Driving mode")
    @pytest.mark.full
    def test_caseid_114039(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("转向灯(DI)失活条件_打断变道手动左转指示轻触后松开轻触左_Transport Active mode")
    @pytest.mark.full
    def test_caseid_114040(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("转向灯(DI)失活条件_打断变道手动左转指示轻触后松开轻触左_Transport Driving mode")
    @pytest.mark.full
    def test_caseid_114041(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("转向灯(DI)激活条件_变道时手动右转指示时轻触后断开_Crash Active mode")
    @pytest.mark.full
    def test_caseid_113973(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("转向灯(DI)激活条件_变道时手动右转指示时轻触后断开_Dyno Active mode")
    @pytest.mark.full
    def test_caseid_113975(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("转向灯(DI)激活条件_变道时手动右转指示时轻触后断开_Dyno Driving mode")
    @pytest.mark.full
    def test_caseid_113976(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("转向灯(DI)激活条件_变道时手动右转指示时轻触后断开_Factory Active mode")
    @pytest.mark.full
    def test_caseid_113971(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("转向灯(DI)激活条件_变道时手动右转指示时轻触后断开_Factory Driving mode")
    @pytest.mark.full
    def test_caseid_113972(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("转向灯(DI)激活条件_变道时手动右转指示时轻触后断开_Normal Active mode")
    @pytest.mark.full
    def test_caseid_113967(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("转向灯(DI)激活条件_变道时手动右转指示时轻触后断开_Transport Active mode")
    @pytest.mark.full
    def test_caseid_113969(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("转向灯(DI)激活条件_变道时手动右转指示时轻触后断开_Transport Driving mode")
    @pytest.mark.full
    def test_caseid_113970(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("转向灯(DI)激活条件_手动右转变道指示_Dyno Driving mode")
    @pytest.mark.full
    def test_caseid_113966(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)

    @allure.title("转向灯（DI）激活过程_手动|主动变道辅助系统 (ALCA)自动|滑动门|自动泊车辅助 （APA）右转指示请求_满足")
    @pytest.mark.full
    def test_caseid_113920(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        sleep(0.3)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=ExtrLtgSts.Err)
        for num in range(3):
            self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 2)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrRi', 2)
            sleep(.4)
            self.bus_comm.set_singal("bodyexposedcanfd","CemBodyExpoFr51", 'ActvnOfIndcrIndcrOut_0_CemBodyExpoSignalIPdu51', 0)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr02", 'ExtrLtgStsTurnIndrRi', 0)
        for num in range(3):
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 2)
            sleep(.2)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)
            
    @allure.title("转向灯(DI)激活条件_方向改变时手动右转指示__Normal Driving mode")
    @pytest.mark.smoke
    def test_caseid_113978(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
            
    @allure.title("功能安全_Normal Active mode HCM节点StsOfLedFrntTurnIndcrRi信号丢失，转向灯状态故障")
    @pytest.mark.full
    def test_caseid_1988353(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        # self.bus_comm.stop_send_pdu("bodyexposedcanfd", "HcmrBodyExpoFr04")
        self.bus_comm.pause_bus_send("bodyexposedcanfd")
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "ExtrLtgStsTurnIndrRi", 2)
        self.bus_comm.resume_all_bus_send()
        for num in range(2):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            
    @allure.title("功能安全_Normal Active mode HCM节点StsOfLedFrntTurnIndcrLe 信号丢失，转向灯状态故障")
    @pytest.mark.full
    def test_caseid_1987379(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        # self.bus_comm.pause_bus_send("bodyexposedcanfd")
        self.bus_comm.stop_send_pdu("bodyexposedcanfd","HcmlBodyExpoFr04")
        sleep(.5)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "ExtrLtgStsTurnIndrLe", 2)
        self.bus_comm.resume_all_bus_send()
        for num in range(2):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)

    @allure.title("转向灯在inactive下,通过语音打开右转，转向灯不亮")
    @pytest.mark.full
    def test_caseid_1988415(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
        
    @allure.title("转向灯在inactive下,通过游戏模式打开右转，转向灯不亮")
    @pytest.mark.full
    def test_caseid_1988536(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)  

    @allure.title("转向灯故障状态 StsOfLedTurnIndcrRi1,（右前）,故障")
    @pytest.mark.full
    def test_caseid_1988613(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearRight,sts=PosnLampSts.Error)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On)

    @allure.title("左转激活之后同时轻触左右按键关闭左转")
    @pytest.mark.full
    def test_caseid_1994341(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

    @allure.title("转向灯优先级验证_关闭-方控右转_优先级判别")
    @pytest.mark.sanity
    def test_caseid_1985922(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=255)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=255)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(6)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("按键打开HWL_按键打开左转HWL抑制左转开启_语音关闭左转HWL继续闪烁_语音关闭HWL失败")
    @pytest.mark.full
    @pytest.mark.tb_new
    def test_caseid_1994765(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos=IndcrSts.LeAndRiOn)
        sleep(0.5)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)#语音关闭左转
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)#语音关闭HWL
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=6)

    @allure.title("语音打开HWL_按键打开右转HWL抑制右转开启_语音打开左转左转开启_按键关闭左转所有灯关闭")
    @pytest.mark.full
    @pytest.mark.tb_new
    def test_caseid_1994764(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos=IndcrSts.LeAndRiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=6)

    @allure.title("按键打开左转_语音打开HWL_按键关闭HWL后全部关闭")
    @pytest.mark.full
    @pytest.mark.tb_new
    def test_caseid_1994763(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=6)

    @allure.title("语音打开左转_按键打开HWL_按键开启右转HWL抑制右转开启_语音关闭右转_HWL继续闪")
    @pytest.mark.full
    @pytest.mark.tb_new
    def test_caseid_1994762(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos=IndcrSts.LeAndRiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95) #语音关闭HWL
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos=IndcrSts.LeAndRiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95) #语音关闭右转
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=6)

    @allure.title("按键打开右转_按键打开HWL_按键关闭HWL右转继续开")
    @pytest.mark.full
    @pytest.mark.tb_new
    def test_caseid_1994761(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        # 恢复
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=6)

    @allure.title("语音打开右转_语音打开HWL_按键开启左转HWL抑制左转开启_语音关闭左转所有灯关闭")
    @pytest.mark.full
    @pytest.mark.tb_new
    def test_caseid_1994760(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos=IndcrSts.LeAndRiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=6)
    
    @allure.title("转向灯(DI)失活条件_打断变道手动右转指示轻触后松开轻触左_Crash Active mode")
    @pytest.mark.full
    def test_caseid_114195(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        sleep(6)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        sleep(1)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)

    @allure.title("转向灯故障状态 StsOfLedFrntTurnIndcrLe（左前）,故障")
    @pytest.mark.full
    def test_caseid_1988589(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:4})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
        sleep(6)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontLeft,sts=PosnLampSts.Error)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.LeOn)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.Off)
        self.bus_comm.ipdu.check(self.bus_comm.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 1)
        sleep(.2)
        self.bus_comm.ipdu.check(self.bus_comm.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
        sleep(.2)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.Off)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.Off)

    @allure.title("转向灯故障状态 StsOfLedFrntTurnIndcrRi（右前）,故障")
    @pytest.mark.full
    def test_caseid_1988595(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:4})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
        sleep(6)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=PosnLampSts.Error)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.RiOn,act_sts=IndcrSts.RiOn)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Error)
        self.bus_comm.ipdu.check(self.bus_comm.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 2)
        sleep(.2)
        self.bus_comm.ipdu.check(self.bus_comm.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
        sleep(.2)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.RiOn,act_sts=IndcrSts.Off)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Error)

    @allure.title("转向灯故障状态 StsOfLedTurnIndcrLe1,（左后）,故障")
    @pytest.mark.full
    def test_caseid_1988612(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:4})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
        sleep(6)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearLeft,sts=PosnLampSts.Error)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.LeOn)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.Off)
        self.bus_comm.ipdu.check(self.bus_comm.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 1)
        sleep(.2)
        self.bus_comm.ipdu.check(self.bus_comm.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', 0)
        sleep(.2)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.Off)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.Off)

    @allure.title("功能安全_转向灯按键开关故障反馈_Counter和Checksum值停发超过1s，转向灯开关故障反馈_故障_老方向盘")
    @pytest.mark.full
    def test_caseid_1988720(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.stop_send_pdu('passivesafetycan', 'BgmPassSafeCANFr01')
        sleep(1)
        self.bus_comm.check_singal('backbonefr','CemBackBoneFr29','SysDirIndcnFailr','1')
        self.bus_comm.resume_bus_send('passivesafetycan')
        sleep(1)

    @allure.title("功能安全_转向灯开启需要UB位判别_左转")
    @pytest.mark.full
    def test_caseid_1988722(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set('bodyexposedcanfd','HcmlBodyExpoFr04','StsOfLedFrntTurnIndcrLe',1,ub_flag=True)
        self.bus_comm.set('bodyexposedcanfd','RcmlBodyExpoFr01','StsOfLedTurnIndcrLe1',1,ub_flag=True)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set('bodyexposedcanfd','HcmlBodyExpoFr04','StsOfLedFrntTurnIndcrLe',1,ub_flag=False)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.Off)
        self.bus_comm.set('bodyexposedcanfd','HcmlBodyExpoFr04','StsOfLedFrntTurnIndcrLe',1,ub_flag=True)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)

    @allure.title("功能安全_转向灯开启需要UB位判别_右转")
    @pytest.mark.full
    def test_caseid_1988745(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set('bodyexposedcanfd','HcmrBodyExpoFr04','StsOfLedFrntTurnIndcrRi',1,ub_flag=True)
        self.bus_comm.set('bodyexposedcanfd','RcmrBodyExpoFr01','StsOfLedTurnIndcrRi1',1,ub_flag=True)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set('bodyexposedcanfd','HcmrBodyExpoFr04','StsOfLedFrntTurnIndcrRi',1,ub_flag=False)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Error)
        self.bus_comm.set('bodyexposedcanfd','HcmrBodyExpoFr04','StsOfLedFrntTurnIndcrRi',1,ub_flag=True)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)

    @allure.title("转向灯在Abandoned下,通过游戏模式打开右转，转向灯不亮")
    @pytest.mark.full
    def test_caseid_1988822(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)
        sleep(6)

    @allure.title("转向灯在Abandoned下,通过语音打开右转，转向灯不亮")
    @pytest.mark.full
    def test_caseid_1988823(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)
        sleep(6)

    @allure.title("转向灯在Dyno下,通过语音打开左转转，转向灯不亮")
    @pytest.mark.full
    def test_caseid_1990218(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)
        sleep(6)

    @allure.title("转向灯在Crash下,通过语音打开左转灯，转向灯不亮")
    @pytest.mark.full
    def test_caseid_1990219(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(1)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)
        sleep(6)
    
    @allure.title("转向灯在factory下,通过语音打开右转转，转向灯不亮")
    @pytest.mark.full
    def test_caseid_1990220(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)
        sleep(6)

    @allure.title("转向灯在transport下,通过语音打开左转，转向灯不亮")
    @pytest.mark.full
    def test_caseid_1990221(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)
        sleep(6)

    @allure.title("转向灯在inactive下,通过语音打开左转，转向灯不亮")
    @pytest.mark.full
    def test_caseid_1990222(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)
        sleep(6)

    @allure.title("Normal Driving mode下CCP 629！=04  or 05 or 06无法手动按键开启左转")
    @pytest.mark.full
    def test_caseid_1990223(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:3})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
    
    @allure.title("转向灯在Abandoned下，通过按键打开右转，转向灯不亮")
    @pytest.mark.full
    def test_caseid_1990224(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)

    @allure.title("转向灯在inactive下,通过按键打开左转，转向灯不亮")
    @pytest.mark.full
    def test_caseid_1990225(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)

    @allure.title("功能安全_转向灯按键开关故障反馈_Counter和Checksum值停发超过1s，转向灯开关故障反馈_故障_新方向盘")
    @pytest.mark.full
    def test_caseid_1990862(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:6})
        self.bus_comm.stop_send_pdu('passivesafetycan', 'BgmPassSafeCANFr01')
        sleep(1)
        self.bus_comm.check_singal('backbonefr','CemBackBoneFr29','SysDirIndcnFailr','1')
        self.bus_comm.resume_bus_send('passivesafetycan')
        sleep(1)

    @allure.title("方向盘信号丢失超过3s_盘回正关闭转向灯")
    @pytest.mark.full
    def test_caseid_1994339(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.stop_send_pdu('bodycan', 'SwtrBodyFr01')
        sleep(4)
        self.soa.send_method_request("LightService_client", "SetTurnLampHold", {"flag": 0})
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.8)
        sleep(2)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.52)
        sleep(2)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)
        self.bus_comm.resume_bus_send('bodycan')
        sleep(1)

    @allure.title("轻触左转600ms以内打开左转向灯")
    @pytest.mark.full
    def test_caseid_1994340(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        sleep(.6)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)

    @allure.title("SWTL方控左转右打方向盘45°回正到30°以下不能关闭左转")
    @pytest.mark.full
    def test_caseid_1994342(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        sleep(3)
        self.soa.send_method_request("LightService_client", "SetTurnLampHold", {"flag": 0})
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', -0.8)
        sleep(0.5)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', -0.52)
        sleep(2)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)

    @allure.title("SWTL方控右转左打方向盘45°回正到30°以下不能关闭右转")
    @pytest.mark.full
    def test_caseid_1994343(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        sleep(3)
        self.soa.send_method_request("LightService_client", "SetTurnLampHold", {"flag": 0})
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.8)
        sleep(0.5)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.52)
        sleep(2)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)

    @allure.title("SWTL方控右转右打方向盘45°回正到30°以下关闭右转Transport Convenience mode")
    @pytest.mark.full
    def test_caseid_1994344(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT,ccp={629:4})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        sleep(3)
        self.soa.send_method_request("LightService_client", "SetTurnLampHold", {"flag": 0})
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', -0.8)
        sleep(0.5)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', -0.52)
        sleep(2)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
    
    @allure.title("SWTL方控右转右打方向盘45°回正到30°以下关闭右转Factory Driving mode")
    @pytest.mark.full
    def test_caseid_1994346(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY,ccp={629:4})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        sleep(3)
        self.soa.send_method_request("LightService_client", "SetTurnLampHold", {"flag": 0})
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', -0.8)
        sleep(0.5)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', -0.52)
        sleep(2)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)

    @allure.title("SWTL方控右转右打方向盘45°回正到30°以下关闭右转Dyno Active mode")
    @pytest.mark.full
    def test_caseid_1994347(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={629:4})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        sleep(3)
        self.soa.send_method_request("LightService_client", "SetTurnLampHold", {"flag": 0})
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', -0.8)
        sleep(0.5)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', -0.52)
        sleep(2)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)

    @allure.title("SWTL方控右转右打方向盘45°回正到30°以下关闭右转Normal Convenience mode")
    @pytest.mark.full
    def test_caseid_1994348(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        sleep(3)
        self.soa.send_method_request("LightService_client", "SetTurnLampHold", {"flag": 0})
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', -0.8)
        sleep(0.5)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', -0.52)
        sleep(2)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)

    @allure.title("ccp#629=06_方向改变时手动右转指示")
    @pytest.mark.full
    def test_caseid_1994349(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:0x06})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left1,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)

    @allure.title("Normal Inactive方向改变时不能激活手动右转指示")
    @pytest.mark.full
    def test_caseid_1994351(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={629:0x04})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)

    @allure.title("Normal Abandoned方向改变时不能激活手动右转指示")
    @pytest.mark.full
    def test_caseid_1994352(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL,ccp={629:0x04})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)

    @allure.title("方向改变时手动右转指示__Normal Convenience mode")
    @pytest.mark.full
    def test_caseid_1994353(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={629:0x04})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)

    @allure.title("ccp#629=06_方向改变时手动左转指示")
    @pytest.mark.full
    def test_caseid_1994354(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:0x06})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)

    @allure.title("方向改变时手动左转指示__Normal Convenience mode")
    @pytest.mark.full
    def test_caseid_1994358(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={629:0x04})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)

    @allure.title("转向灯（DI）激活过程_手动|自动驾驶功能请求自动右转指示_满足DI激活条件右转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_1994359(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearRight,sts=ExtrLtgSts.Err)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=ExtrLtgSts.Err)
        sleep(3)
        for num in range(3):
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.RiOn)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Error)
            sleep(.4)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
        for num in range(3):
            self.bus_comm.check_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 2)
            sleep(.2)
            self.bus_comm.check_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearRight,sts=ExtrLtgSts.On)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=ExtrLtgSts.On)

    @allure.title("转向灯（DI）激活过程_手动|自动驾驶功能请求自动右转指示_满足DI激活条件右1转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_1994360(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearRight,sts=ExtrLtgSts.Err)
        sleep(3)
        for num in range(3):
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.RiOn)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Error)
            sleep(.4)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
        for num in range(3):
            self.bus_comm.check_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 2)
            sleep(.2)
            self.bus_comm.check_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearRight,sts=ExtrLtgSts.On)

    @allure.title("转向灯（DI）激活过程_手动|自动驾驶功能请求自动右转指示_满足DI激活条件右前转向灯状态信号故障")
    @pytest.mark.full
    def test_caseid_1994361(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=ExtrLtgSts.Err)
        sleep(3)
        for num in range(3):
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.RiOn)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Error)
            sleep(.4)
            self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
        for num in range(3):
            self.bus_comm.check_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 2)
            sleep(.2)
            self.bus_comm.check_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=ExtrLtgSts.On)

    @allure.title("111周期性开右转_95开左转")
    @pytest.mark.full
    def test_caseid_1994778(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        # 恢复
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
        sleep(6)

    @allure.title("111开左转_等待超过5s_47关闭左转")
    @pytest.mark.full
    def test_caseid_1994779(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        sleep(6)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
        sleep(6)

    @allure.title("111开左转_95关闭左转")
    @pytest.mark.full
    def test_caseid_1994780(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
        sleep(6)

    @allure.title("111开右转_79关闭右转")
    @pytest.mark.full
    def test_caseid_1994781(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
        sleep(6)

    @allure.title("111开左转_47开右转")
    @pytest.mark.full
    def test_caseid_1994782(self):  
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        # 恢复
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
        sleep(6)

    @allure.title("语音开启右转_按键关闭右转")
    @pytest.mark.full
    def test_caseid_1994783(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)

    @allure.title("语音开启右转_按键开启左转")
    @pytest.mark.full
    def test_caseid_1994784(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        # 恢复
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)

    @allure.title("按键开启左转_语音开启右转")
    @pytest.mark.full
    def test_caseid_1994785(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        # 恢复
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)

    @allure.title("语音开启左转_按键关闭左转")
    @pytest.mark.full
    def test_caseid_1994786(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)    

    @allure.title("95周期性开左转_111关闭左转失败")
    @pytest.mark.full
    def test_caseid_1994788(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        sleep(6)

    @allure.title("95周期性开右转_79关闭右转")
    @pytest.mark.full
    def test_caseid_1994789(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
        sleep(6)

    @allure.title("95开左转_等待超过5s_47关闭左转")
    @pytest.mark.full
    def test_caseid_1994790(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        sleep(6)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
        sleep(6)

    @allure.title("95开左转_111开右转失败")
    @pytest.mark.full
    def test_caseid_1994791(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        sleep(6)

    @allure.title("95开右转_79关闭右转")
    @pytest.mark.full
    def test_caseid_1994792(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
        sleep(6)

    @allure.title("95开左转_47开右转")
    @pytest.mark.full
    def test_caseid_1994793(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        sleep(6)

    @allure.title("79周期性开左转_255释放优先级_95开右转")
    @pytest.mark.full
    def test_caseid_1994794(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.Release,priority=255)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        sleep(6)

    @allure.title("79周期性开左转_95关闭左转失败")
    @pytest.mark.full
    def test_caseid_1994795(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        sleep(6)

    @allure.title("79周期性开右转_47关闭右转")
    @pytest.mark.full
    def test_caseid_1994796(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
        sleep(6)

    @allure.title("79开左转_等待超过5s_95关闭左转")
    @pytest.mark.full
    def test_caseid_1994797(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        sleep(6)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
        sleep(6)

    @allure.title("79开左转_111开右转失败")
    @pytest.mark.full
    def test_caseid_1994798(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        sleep(6)

    @allure.title("79开右转_95开左转失败")
    @pytest.mark.full
    def test_caseid_1994799(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        sleep(6)

    @allure.title("79开左转_47开右转")
    @pytest.mark.full
    def test_caseid_1994800(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        sleep(6)

    @allure.title("47周期性开左转_255释放优先级_95开右转")
    @pytest.mark.full
    def test_caseid_1994801(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.Release,priority=255)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        sleep(6)

    @allure.title("47周期性开右转_95关闭右转失败")
    @pytest.mark.full
    def test_caseid_1994802(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        sleep(6)

    @allure.title("47开左转_等待超过5s_79关闭左转")
    @pytest.mark.full
    def test_caseid_1994803(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        sleep(6)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
        sleep(6)
    
    @allure.title("47开左转_111开右转失败")
    @pytest.mark.full
    def test_caseid_1994804(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        sleep(6)

    @allure.title("47开右转_95开左转失败")
    @pytest.mark.full
    def test_caseid_1994805(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        sleep(6)
    
    @allure.title("47开左转_79关闭左转失败")
    @pytest.mark.full
    def test_caseid_1994806(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        sleep(6)

    @allure.title("95周期性开左转_释放优先级_111关闭左转失败")
    @pytest.mark.full
    def test_caseid_1994787(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        sleep(6)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        sleep(6)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("拨杆开右转_右后灯故障")
    @pytest.mark.full
    def test_caseid_1995353(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress2stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearRight,sts=PosnLampSts.Error)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Error)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.RiOn,act_sts=IndcrSts.RiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Error)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.RiOn,act_sts=IndcrSts.Off)
        for num in range(3):
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 2)
            sleep(.2)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)
        # 恢复
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearRight,sts=PosnLampSts.On)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress2stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("拨杆开右转_右前灯故障")
    @pytest.mark.full
    def test_caseid_1995354(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress1stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=PosnLampSts.Error)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Error)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.RiOn,act_sts=IndcrSts.RiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Error)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.RiOn,act_sts=IndcrSts.Off)
        for num in range(3):
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 2)
            sleep(.2)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)
        # 恢复
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontRight,sts=PosnLampSts.On)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress1stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("拨杆开左转_左后灯故障")
    @pytest.mark.full
    def test_caseid_1995355(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress1stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearLeft,sts=PosnLampSts.Error)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.LeOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.Off)
        for num in range(3):
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 1)
            sleep(.2)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)
        # 恢复
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.RearLeft,sts=PosnLampSts.On)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress1stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("拨杆开左转_左前灯故障")
    @pytest.mark.full
    def test_caseid_1995356(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress1stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.LeOn)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontLeft,sts=PosnLampSts.Error)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.LeOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Error,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.Off)
        for num in range(3):
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 1)
            sleep(.2)
            self.bus_comm.set_singal("backbonefr","CemBackBoneFr06", 'IndcrDisp', 0)
        # 恢复
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.FrontLeft,sts=PosnLampSts.On)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress1stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
    
    @allure.title("按键开HWL_拨杆上拨右转闪烁_拨杆上拨双闪闪烁")
    @pytest.mark.sanity
    def test_caseid_1995357(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress2stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress2stGear)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        # 恢复
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("上拨开右转_语音开HWL右转熄灭双闪闪烁_拨杆下拨开左转")
    @pytest.mark.sanity
    def test_caseid_1995358(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress2stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=95)
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress1stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        # 恢复
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("下拨开左转_按键开HWL左转熄灭双闪闪烁_按键关HWL左转闪烁")
    @pytest.mark.sanity
    def test_caseid_1995359(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress1stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.LeOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_hwl_lamp_flash_sts(flash_time=3,indcrdisp=IndcrSts.LeAndRiOn)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.LeOn)
        # 恢复
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("上拨至二档开右转_方向盘回正关闭右转")
    @pytest.mark.full
    def test_caseid_1995365(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrQf', 3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress2stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', -0.8)
        sleep(1)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', -0.52)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("下拨至一档开左转_方向盘回正关闭左转")
    @pytest.mark.full
    def test_caseid_1995366(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrQf', 3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress1stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.8)
        sleep(1)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.52)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("111开右转_拨杆上拨关闭右转")
    @pytest.mark.full
    def test_caseid_1995367(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress2stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("111周期开左转_上拨至一档左转熄灭右转亮")
    @pytest.mark.full
    def test_caseid_1995368(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress1stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        # 恢复
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("111周期开右转_下拨至二档右转熄灭左转亮")
    @pytest.mark.full
    def test_caseid_1995369(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress2stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        # 恢复
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("95开左转_拨杆下拨关闭左转")
    @pytest.mark.sanity
    def test_caseid_1995370(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress2stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("95周期开右转_下拨至一档右转熄灭左转闪烁")
    @pytest.mark.sanity
    def test_caseid_1995371(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress1stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        # 恢复
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("95周期开左转_上拨至二档左转熄灭右转闪烁")
    @pytest.mark.sanity
    def test_caseid_1995372(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress2stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        # 恢复
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("79开右转_5s内拨杆上拨关闭右转失败")
    @pytest.mark.full
    def test_caseid_1995373(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress2stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        # 恢复
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(6)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("79开右转_5s后拨杆上拨关闭右转")
    @pytest.mark.full
    def test_caseid_1995374(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        sleep(6)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress2stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("79周期开右转_上拨至二档右转继续闪烁")
    @pytest.mark.full
    def test_caseid_1995375(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress2stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        # 恢复
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(6)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
    
    @allure.title("79周期开左转_下拨至一档左转继续闪烁")
    @pytest.mark.full
    def test_caseid_1995376(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress1stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        # 恢复
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        sleep(6)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("47开右转_5s后拨杆上拨关闭右转")
    @pytest.mark.full
    def test_caseid_1995377(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        sleep(6)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress1stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("47开左转_5s内拨杆下拨关闭左转失败")
    @pytest.mark.full
    def test_caseid_1995378(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress1stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        # 恢复
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(6)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("47周期开右转_下拨至二档右转继续闪烁")
    @pytest.mark.full
    def test_caseid_1995379(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kRight,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress2stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        # 恢复
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(6)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("47周期开左转_上拨至一档左转继续闪烁")
    @pytest.mark.full
    def test_caseid_1995380(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress1stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        # 恢复
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(6)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("上拨至二档开启右转_111关闭右转失败")
    @pytest.mark.full
    def test_caseid_1995381(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress2stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=111)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        # 恢复
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress2stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("上拨至一档开启右转_95关闭右转_上拨二档右转闪烁")
    @pytest.mark.full
    def test_caseid_1995382(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress1stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress2stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        # 恢复
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress2stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("上拨至一档开启右转_79关闭右转_5s后拨杆上拨二档右转亮")
    @pytest.mark.full
    def test_caseid_1995383(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress1stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
        sleep(6)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress2stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        # 恢复
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress2stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("下拨至二档开启左转_79关闭左转_5s内拨杆下拨一档左转不亮")
    @pytest.mark.full
    def test_caseid_1995384(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress2stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=79)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress1stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
        # 恢复
        sleep(6)

    @allure.title("上拨至二档开启右转_47关闭右转_5s后上拨至一档右转闪烁")
    @pytest.mark.full
    def test_caseid_1995385(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress2stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(6)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress1stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        # 恢复
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress1stGear)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("下拨至一档开启左转_47关闭左转_5s内下拨至二档左转不亮")
    @pytest.mark.full
    def test_caseid_1995386(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress1stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress2stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
        # 恢复
        sleep(6)

    @allure.title("右转向灯闪烁_下拨至二档右转熄灭左转闪烁")
    @pytest.mark.sanity
    def test_caseid_1995387(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress2stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        # 恢复
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress2stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("右转向灯闪烁_上拨至一档右转熄灭")
    @pytest.mark.sanity
    def test_caseid_1995388(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress1stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("左转向灯闪烁_上拨至二档左转熄灭右转闪烁")
    @pytest.mark.sanity
    def test_caseid_1995389(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress2stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        # 恢复
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress1stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("左转向灯闪烁_下拨至一档左转熄灭")
    @pytest.mark.sanity
    def test_caseid_1995390(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress1stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("转向灯熄灭_上拨至二档开启右转_拨杆拨至上拨一档右转熄灭")
    @pytest.mark.smoke
    def test_caseid_1995391(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress2stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress1stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("转向灯熄灭_上拨至一档开启右转_再次上拨至二档右转熄灭")
    @pytest.mark.smoke
    def test_caseid_1995392(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress1stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress2stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("转向灯熄灭_下拨至二档开启左转_拨杆拨至下拨一档左转熄灭")
    @pytest.mark.smoke
    def test_caseid_1995393(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress2stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress1stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("转向灯熄灭_下拨至一档开启左转_下拨至二档左转熄灭")
    @pytest.mark.smoke
    def test_caseid_1995394(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress1stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress2stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
    
    @allure.title("Transport Inactive mode_拨杆开启左转失败")
    @pytest.mark.full
    def test_caseid_1995395(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress1stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Abandoned mode_拨杆开启右转失败")
    @pytest.mark.full
    def test_caseid_1995396(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress1stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Dyno Convenience mode_拨杆开启右转失败")
    @pytest.mark.full
    def test_caseid_1995397(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.UpPress1stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Crash Driving mode_拨杆开启右转失败")
    @pytest.mark.full
    def test_caseid_1995398(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress1stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Factory Active mode_拨杆开启右转失败")
    @pytest.mark.full
    def test_caseid_1995399(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress1stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Transport Convenience mode_拨杆开启右转失败")
    @pytest.mark.full
    def test_caseid_1995400(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress1stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("Normal Driving mode_拨杆开启左转_拨杆关闭左转")
    @pytest.mark.smoke
    def test_caseid_1995401(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress1stGear)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.set_trun_beam_pull_up_down(gear=TurnPressGear.DownPress1stGear)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("SWTL方控右转右打方向盘45°回正到30°以下关闭右转Crash Active mode")
    @pytest.mark.full
    def test_caseid_1994345(self):
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH,ccp={629:4})
        sleep(1)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)
        sleep(3)
        self.soa.send_method_request("LightService_client", "SetTurnLampHold", {"flag": 0})
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', -0.8)
        sleep(0.5)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', -0.52)
        sleep(2)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)

    @allure.title("ccp#629=05_方向改变时手动右转指示")
    @pytest.mark.full
    def test_caseid_1994350(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:0x05})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
        sleep(6)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.LongPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos=IndcrSts.RiOn)

    @allure.title("ccp#629=05_方向改变时手动左转指示")
    @pytest.mark.full
    def test_caseid_1994355(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:0x05})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
        sleep(6)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.LongPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)

    @allure.title("Normal Inactive方向改变时不能激活手动左转指示")
    @pytest.mark.full
    def test_caseid_1994356(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={629:0x04})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)

    @allure.title("Normal Abandoned方向改变时不能激活手动左转指示")
    @pytest.mark.full
    def test_caseid_1994357(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL,ccp={629:0x04})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.Off)
    
    @allure.title("ccp#508！=03时，手动左转不能激活转向灯")
    @pytest.mark.full
    def test_caseid_1994362(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={508:0x04,274:80})
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
    
    @allure.title("ccp#274！=80/81时，自动驾驶功能不能请求自动左转指示")
    @pytest.mark.full
    def test_caseid_1994363(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={508:0x03,274:0x82})
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=47)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
        sleep(6)
        # 恢复ccp
        self.mix.sd_tester.set_ccp({274:0x80})

    @allure.title("ActvnOfIndcr信号E2E校验错误_转向灯关闭失败_ActvnOfIndcr信号E2E校验恢复_转向灯关闭")
    @pytest.mark.full
    def test_caseid_1997070(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.ipdu.set_no_crc(self.bus_comm.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'ActvnOfIndcrIndcrOut')
        # self.bus_comm.ipdu.set_no_crc(self.bus_comm.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2')
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.ipdu.restore_crc(self.bus_comm.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'ActvnOfIndcrIndcrOut')
        # self.bus_comm.ipdu.restore_crc(self.bus_comm.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2')
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("SteerWhlTouchTurnLightSwtLe信号E2E校验错误_转向灯关闭失败_SteerWhlTouchTurnLightSwtLe信号E2E校验恢复_转向灯关闭")
    @pytest.mark.full
    def test_caseid_1997069(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.ipdu.set_no_crc(self.bus_comm.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2')
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=95)
        self.check_turn_lamp_flash_sts(act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos=IndcrSts.LeOn)
        self.bus_comm.ipdu.restore_crc(self.bus_comm.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2')
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        