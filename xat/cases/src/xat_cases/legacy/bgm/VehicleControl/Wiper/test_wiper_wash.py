#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_wiper_mode_abc.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/11/9 11:30
@Description: BGM车控车设外后视镜功能
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
from xat_ecu.api.constants.common import *


@allure.feature("BGM车控车设/雨刮功能")
@allure.story("雨刮洗涤")
class TestWiperCtrl(TestABCBase):
    def before_class(self, ecu):
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0x06],recv=[0x62, 0xF1, 0x06])
        self.ccp_original_value = recv_data_list[3:1556 + 3]
        self.soa.update(["WiperService_client"])
        sleep(2)
        self.soa.start_get_wiper_switch_sts()
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)

    def before_each_func(self, ecu):
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        sleep(1)
        self.bus_comm.ipdu.reset_check_results()
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.Off)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.hmi_set_wiper_mode(WiperPos.Front, WiperMode.Off)
        sleep(1)
        
    def after_each_func(self, ecu):
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.io.set_door(Drvr=Door.close)
        try:
            self.bus_comm.set_wiper_lever_status(value=0)
        except Exception as e:
            logger.info(f"----------> after_each_func Error{str(e)}")
            pass

    def after_class(self, ecu):
        self.sd_tester.write_ccp_value(self.ccp_original_value)
        self.soa.stop_get_wiper_switch_sts()
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    def check_three_sigle(self):
        self.bus_comm.check_signal_thread_start("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe")  
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        result_ori = self.bus_comm.check_signal_thread_stop('WshrLvrPosnSafe')  
        logger.info(f'获取到的原始数据WshrLvrPosnSafe为{result_ori}')
        result = get_signal_times_interval(result_ori, 2)
        logger.info("期望值的统计结果:{}".format(result))
        return result
    
    @pytest.mark.smoke
    def test_caseid_1989622(self):
        """
        convience&nomal 雨刮洗涤激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.smoke
    def test_caseid_1989624(self):
        """
        convience&dyno 雨刮洗涤激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.smoke
    def test_caseid_1989625(self):
        """
        driving&dyno 雨刮洗涤激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.smoke
    def test_caseid_1989626(self):
        """
        driving&nomal 雨刮洗涤激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.smoke
    def test_caseid_1989633(self):
        """
        active&dyno 雨刮洗涤激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.smoke
    def test_caseid_1989634(self):
        """
        active&nomal 雨刮洗涤激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.sanity
    def test_caseid_1989635(self):
        """
        Convience&Crash 雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.sanity
    def test_caseid_1989636(self):
        """
        Convience&Factory 雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.sanity
    def test_caseid_1989637(self):
        """
        Convience&Transport 雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.sanity
    def test_caseid_1989638(self):
        """
        driving&Crash 雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.sanity
    def test_caseid_1989639(self):
        """
        driving&Transport 雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.sanity
    def test_caseid_1989640(self):
        """
        driving&Factory 雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.sanity
    def test_caseid_1989642(self):
        """
        active&Crash 雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.sanity
    def test_caseid_1989643(self):
        """
        acitve&Factory 雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.sanity
    def test_caseid_1989644(self):
        """
        active&Transport 雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.full
    def test_caseid_1989649(self):
        """
        Inactive&Nomal 雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.full
    def test_caseid_1989650(self):
        """
        Inactive&dyno 雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.full
    def test_caseid_1989652(self):
        """
        abandoned&dyno 雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.full
    def test_caseid_1989653(self):
        """
        abandoned&nomal 雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.sanity
    def test_caseid_1989654(self):
        """
        driving&nomal 长按雨刮洗涤按键，雨刮洗涤激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
        sleep(9)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
        sleep(3)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.sanity
    def test_caseid_1989655(self):
        """
        driving&dyno 长按雨刮洗涤按键，雨刮洗涤激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
        sleep(9)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
        sleep(3)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.sanity
    def test_caseid_1989656(self):
        """
        convience&nomal 长按雨刮洗涤按键，雨刮洗涤激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
        sleep(9)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
        sleep(3)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.sanity
    def test_caseid_1989657(self):
        """
        convience&dyno 长按雨刮洗涤按键，雨刮洗涤激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
        sleep(9)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
        sleep(3)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.sanity
    def test_caseid_1989658(self):
        """
        active&nomal 长按雨刮洗涤按键，雨刮洗涤激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
        sleep(9)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
        sleep(3)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.sanity
    def test_caseid_1989659(self):
        """
        active&dyno 长按雨刮洗涤按键，雨刮洗涤激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
        sleep(9)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
        sleep(3)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.full
    def test_caseid_1989660(self):
        """
        driving&crash carmode不满足 长按雨刮洗涤按键，雨刮洗涤ActvnOfWshrFrntSafe无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(9)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(3)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.full
    def test_caseid_1989661(self):
        """
        driving&factory carmode不满足 长按雨刮洗涤按键，雨刮洗涤ActvnOfWshrFrntSafe无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(9)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(3)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.full
    def test_caseid_1989662(self):
        """
        driving&Transoprt carmode不满足 长按雨刮洗涤按键，雨刮洗涤ActvnOfWshrFrntSafe无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(9)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(3)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.full
    def test_caseid_1989664(self):
        """
        convience&Transoprt carmode不满足 长按雨刮洗涤按键，雨刮洗涤ActvnOfWshrFrntSafe无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(9)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(3)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.full
    def test_caseid_1989665(self):
        """
        convience&factory carmode不满足 长按雨刮洗涤按键，雨刮洗涤ActvnOfWshrFrntSafe无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(9)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(3)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.full
    def test_caseid_1989666(self):
        """
        convience&crash carmode不满足 长按雨刮洗涤按键，雨刮洗涤ActvnOfWshrFrntSafe无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(9)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(3)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.full
    def test_caseid_1989667(self):
        """
        active&crash carmode不满足 长按雨刮洗涤按键，雨刮洗涤ActvnOfWshrFrntSafe无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(9)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(3)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.full
    def test_caseid_1989668(self):
        """
        active&factory carmode不满足 长按雨刮洗涤按键，雨刮洗涤ActvnOfWshrFrntSafe无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(9)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(3)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.full
    def test_caseid_1989669(self):
        """
        active&Transoprt  carmode不满足 长按雨刮洗涤按键，雨刮洗涤ActvnOfWshrFrntSafe无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(9)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(3)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.full
    def test_caseid_1989670(self):
        """
        Inactive&Nomal usagemode不满足 长按雨刮洗涤按键，雨刮洗涤ActvnOfWshrFrntSafe无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(9)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(3)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.full
    def test_caseid_1989671(self):
        """
        inactive&dyno  usagemode不满足 长按雨刮洗涤按键，雨刮洗涤ActvnOfWshrFrntSafe无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(9)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(3)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.full
    def test_caseid_1989672(self):
        """
        abandoned&dyno usagemode不满足 长按雨刮洗涤按键，雨刮洗涤ActvnOfWshrFrntSafe无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(9)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(3)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.full
    def test_caseid_1989673(self):
        """
        abandoned&normal  usagemode不满足 长按雨刮洗涤按键，雨刮洗涤ActvnOfWshrFrntSafe无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(9)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(3)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)

    @pytest.mark.sanity
    def test_caseid_1989700(self):
        """
        driving&nomal 雨刮洗涤激活超过11s后自动关闭
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.1)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.On)
        sleep(9)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.On)
        sleep(3)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)

    @pytest.mark.sanity
    def test_caseid_1989701(self):
        """
        driving&dyno 雨刮洗涤激活超过11s后自动关闭
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.1)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.On)
        sleep(9)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.On)
        sleep(3)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)

    @pytest.mark.sanity
    def test_caseid_1989702(self):
        """
        active&nomal 雨刮洗涤激活超过11s后自动关闭
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.1)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.On)
        sleep(9)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.On)
        sleep(3)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)

    @pytest.mark.sanity
    def test_caseid_1989703(self):
        """
        active&dyno 雨刮洗涤激活超过11s后自动关闭
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.1)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.On)
        sleep(9)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.On)
        sleep(3)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)

    @pytest.mark.sanity
    def test_caseid_1989704(self):
        """
        convience&dyno 雨刮洗涤激活超过11s后自动关闭
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.1)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.On)
        sleep(9)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.On)
        sleep(3)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)

    @pytest.mark.sanity
    def test_caseid_1989705(self):
        """
        convience&nomal 雨刮洗涤激活超过11s后自动关闭
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.1)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.On)
        sleep(9)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.On)
        sleep(3)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)

    @pytest.mark.full   
    def test_caseid_1989708(self):
        """
        driving&crash carode不满足，雨刮洗涤无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.1)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(9)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(3)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)

    @pytest.mark.full   
    def test_caseid_1989711(self):
        """
        driving&factory carode不满足，雨刮洗涤无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.1)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(9)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(3)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)


    @pytest.mark.full   
    def test_caseid_1989711(self):
        """
        driving&factory carode不满足，雨刮洗涤无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.1)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(9)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(3)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)

    @pytest.mark.full   
    def test_caseid_1989712(self):
        """
        driving&Transport carode不满足，雨刮洗涤无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.1)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(9)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(3)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)

    @pytest.mark.full   
    def test_caseid_1989713(self):
        """
        active&Transport carode不满足，雨刮洗涤无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.1)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(9)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(3)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)

    
    @pytest.mark.full   
    def test_caseid_1989714(self):
        """
        active&factory carode不满足，雨刮洗涤无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.1)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(9)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(3)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)


    @pytest.mark.full   
    def test_caseid_1989715(self):
        """
        active&crash carode不满足，雨刮洗涤无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.1)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(9)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(3)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)


    @pytest.mark.full   
    def test_caseid_1989716(self):
        """
        convience&crash carode不满足，雨刮洗涤无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.1)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(9)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(3)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)


    @pytest.mark.full   
    def test_caseid_1989717(self):
        """
        convience&factory carode不满足，雨刮洗涤无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.1)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(9)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(3)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)

    @pytest.mark.full   
    def test_caseid_1989718(self):
        """
        Conviecne&Transport carode不满足，雨刮洗涤无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.1)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(9)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(3)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)

    @pytest.mark.full   
    def test_caseid_1989719(self):
        """
        Inactive&Nomal usagemode 不满足，雨刮洗涤无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.1)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(9)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(3)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)

    @pytest.mark.full   
    def test_caseid_1989719(self):
        """
        Inactive&Nomal usagemode 不满足，雨刮洗涤无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.1)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(9)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(3)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)


    @pytest.mark.full   
    def test_caseid_1989720(self):
        """
        Inactive&dyno usagemode 不满足，雨刮洗涤无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.1)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(9)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(3)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)


    @pytest.mark.full   
    def test_caseid_1989721(self):
        """
        abandonded&Nomal usagemode 不满足，雨刮洗涤无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.1)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(9)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(3)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)


    
    @pytest.mark.full   
    def test_caseid_1989722(self):
        """
        abandoned&dyno usagemode 不满足，雨刮洗涤无法激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.1)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(9)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        sleep(3)
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)

    @pytest.mark.smoke
    def test_caseid_1992580(self):
        """
        convience&normal 激活雨刮洗涤超过0.3s后，检查WshrLvrPosnSafe信号值
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",2)
        assert self.check_three_sigle()[0] !=0

    @pytest.mark.full
    def test_caseid_1992579(self):
        """
        convience&dyno 激活雨刮洗涤超过0.3s后，检查WshrLvrPosnSafe信号值
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",2)
        assert self.check_three_sigle()[0] !=0

    @pytest.mark.smoke
    def test_caseid_1992578(self):
        """
        active&normal 激活雨刮洗涤超过0.3s后，检查WshrLvrPosnSafe信号值
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",2)
        assert self.check_three_sigle()[0] !=0


    @pytest.mark.full
    def test_caseid_1992577(self):
        """
        active&dyno 激活雨刮洗涤超过0.3s后，检查WshrLvrPosnSafe信号值
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",2)
        assert self.check_three_sigle()[0] !=0

    @pytest.mark.smoke
    def test_caseid_1992576(self):
        """
        driving&normal 激活雨刮洗涤超过0.3s后，检查WshrLvrPosnSafe信号值
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",2)
        assert self.check_three_sigle()[0] !=0


    @pytest.mark.full
    def test_caseid_1992575(self):
        """
        driving&dyno 激活雨刮洗涤超过0.3s后，检查WshrLvrPosnSafe信号值
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",2)
        assert self.check_three_sigle()[0] !=0


    @pytest.mark.smoke
    def test_caseid_1992574(self):
        """
        convience&normal 激活雨刮洗涤在未超过0.3s前关闭雨刮洗涤，检查WshrLvrPosnSafe是否为2
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.2)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",2)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",2)

    @pytest.mark.full
    def test_caseid_1992573(self):
        """
        convience&dyno 激活雨刮洗涤在未超过0.3s前关闭雨刮洗涤，检查WshrLvrPosnSafe是否为2
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.2)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",2)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",2)

    @pytest.mark.smoke
    def test_caseid_1992572(self):
        """
        active&normal 激活雨刮洗涤在未超过0.3s前关闭雨刮洗涤，检查WshrLvrPosnSafe是否为2
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.2)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",2)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",2)

    @pytest.mark.full
    def test_caseid_1992571(self):
        """
        active&dyno 激活雨刮洗涤在未超过0.3s前关闭雨刮洗涤，检查WshrLvrPosnSafe是否为2
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        sleep(0.2)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",2)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",2)

    @pytest.mark.smoke
    def test_caseid_1992570(self):
        """
        driving&normal 激活雨刮洗涤在未超过0.3s前关闭雨刮洗涤，检查WshrLvrPosnSafe是否为2
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",2)
        sleep(0.2)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",2)

    @pytest.mark.full
    def test_caseid_1992569(self):
        """
        driving&dyno 激活雨刮洗涤在未超过0.3s前关闭雨刮洗涤，检查WshrLvrPosnSafe是否为2
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.On)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",2)
        sleep(0.2)
        self.soa.hmi_set_wiper_wash_func(pos=WiperPos.Front,sts=isOn.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",2)

    @pytest.mark.sanity
    def test_caseid_1992581(self):
        """
        雨刮维修激活时，无法打开雨刮洗涤
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.On)
        self.soa.get_wiper_wash_sts(WiperPos.Front, isOn.Off)


    @pytest.mark.v210
    @pytest.mark.smoke
    def test_caseid_1993135(self):
        """
        Vnus880v，雨刮洗液液位为高液位，当车速车速大于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x02,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)  
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=6)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)

    @pytest.mark.v210
    @pytest.mark.smoke
    def test_caseid_1993134(self):
        """
        Vnus880v，雨刮洗液液位为高液位，当车速车速小于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x02,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)  
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=2)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)
    
    @pytest.mark.v210
    @pytest.mark.smoke
    def test_caseid_1993133(self):
        """
        Vnus880v，雨刮洗液液位为低液位，当车速车速大于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x02,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=6)
        
    @pytest.mark.v210
    @pytest.mark.smoke
    def test_caseid_1993132(self):
        """
        Vnus880v，雨刮洗液液位为低液位，当车速车速小于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x02,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=2)

    @pytest.mark.v210
    @pytest.mark.smoke
    def test_caseid_1993131(self):
        """
        Mars800v，雨刮洗涤液位为低液位，当车速车速大于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x01,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=6)

    @pytest.mark.v210
    @pytest.mark.smoke
    def test_caseid_1993130(self):
        """
        Mars800v，雨刮洗涤液位为低液位，当车速车速小于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x01,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=2)


    @pytest.mark.v210
    @pytest.mark.smoke
    def test_caseid_1993129(self):
        """
        Mars800v，雨刮洗涤液位为高液位，当车速车速大于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x01,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=6)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)

    @pytest.mark.v210
    @pytest.mark.smoke
    def test_caseid_1993128(self):
        """
        Mars800v，雨刮洗涤液位为高液位，当车速车速小于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x01,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=2)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1993127(self):
        """
        Vnus880v，BGM断电上电雨刮洗液液位为低液位，当车速车速大于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x02,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=6)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=31)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1993126(self):
        """
        Vnus880v，BGM断电上电雨刮洗液液位为低液位，当车速车速小于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x02,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=2)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=3)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)
        sleep(15)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1993125(self):
        """
        Vnus880v，BGM断电上电雨刮洗液液位为高液位，当车速车速大于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x02,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=31)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=6)

    @pytest.mark.v210
    @pytest.mark.sanity
    @pytest.mark.nvm
    def test_caseid_1993124(self):
        """
        Vnus880v，BGM断电上电雨刮洗液液位为高液位，当车速车速小于0.1km/h，检测雨刮洗涤低液位信号号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x02,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=2)
        sleep(15)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1993123(self):
        """
       Mars800v，BGM断电上电雨刮洗涤液位为高液位，当车速车速大于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x01,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=31)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=6)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1993122(self):
        """
       Mars800v，BGM断电上电雨刮洗涤液位为高液位，当车速车速小于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x01,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=2)
        sleep(15)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1993121(self):
        """
       Mars800v，BGM断电上电雨刮洗涤液位为低液位，当车速车速大于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x01,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=6)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=31)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1993120(self):
        """
       Mars800v，BGM断电上电雨刮洗涤液位为低液位，当车速车速小于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x01,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=2)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=3)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)
        sleep(15)

    ##########################################################################################################################################################################
    @pytest.mark.v210
    @pytest.mark.sanity
    @pytest.mark.nvm
    def test_caseid_1993119(self):
        """
        Vnus880v，BGM复位雨刮洗液液位为低液位，当车速车速大于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x02,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=6)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'1181')
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=31)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)
        sleep(15)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1993118(self):
        """
        Vnus880v，BGM复位雨刮洗液液位为低液位，当车速车速小于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x02,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=2)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'1181')
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=3)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)
        sleep(15)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1993117(self):
        """
        Vnus880v，BGM复位雨刮洗液液位为高液位，当车速车速大于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x02,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'1181')
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=31)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=6)
        sleep(15)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1993116(self):
        """
        Vnus880v，BGM复位雨刮洗液液位为高液位，当车速车速小于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x02,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'1181')
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=2)
        sleep(15)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1993115(self):
        """
       Mars800v，BGM复位雨刮洗涤液位为高液位，当车速车速大于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x01,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'1181')
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=31)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=6)
        sleep(15)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1993114(self):
        """
       Mars800v，BGM复位雨刮洗涤液位为高液位，当车速车速小于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x01,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'1181')
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=2)
        sleep(15)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1993113(self):
        """
       Mars800v，BGM复位雨刮洗涤液位为低液位，当车速车速大于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x01,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=6)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'1181')
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=31)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)
        sleep(15)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1993112(self):
        """
       Mars800v，BGM复位雨刮洗涤液位为低液位，当车速车速小于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x01,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=2)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'1181')
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=3)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)
        sleep(15)

    #--------------------------------------------------------------------------------------------------------------------------------
    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1993103(self):
        """
        反向用例Vnus880v，雨刮洗液液位为高液位，当车速车速大于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x01,950:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)  
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1993102(self):
        """
        反向用例 Vnus880v，雨刮洗液液位为高液位，当车速车速小于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x01,950:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)  
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)
    
    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1993101(self):
        """
        反向用例Vnus880v，雨刮洗液液位为低液位，当车速车速大于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x01,950:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)
        

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1993100(self):
        """
        反向用例Vnus880v，雨刮洗液液位为低液位，当车速车速小于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x01,950:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1993099(self):
        """
        反向用例Mars800v，雨刮洗涤液位为低液位，当车速车速大于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x01,950:0x01})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1993098(self):
        """
        反向用例Mars800v，雨刮洗涤液位为低液位，当车速车速小于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x01,950:0x01})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1993097(self):
        """
        反向用例Mars800v，雨刮洗涤液位为高液位，当车速车速大于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x01,950:0x01})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1993096(self):
        """
        反向用例Mars800v，雨刮洗涤液位为高液位，当车速车速小于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x01,950:0x01})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @pytest.mark.v210
    @pytest.mark.network_sleep
    @pytest.mark.full
    def test_caseid_1993111(self):
        """
        Vnus880v，BGM休眠唤醒雨刮洗液液位为低液位，当车速车速大于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x02,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=6)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.mix.network_sleep()
        self.io.set_door(Drvr=Door.open)
        self.sd_tester.sd_tester.tester_present()
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=31)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.io.tcam_kl15_up()
        sleep(5)  # 诊断激活线5s钟变为连接状态

    @pytest.mark.v210
    @pytest.mark.network_sleep
    @pytest.mark.full
    def test_caseid_1993110(self):
        """
        Vnus880v，BGM休眠唤醒雨刮洗液液位为低液位，当车速车速小于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x02,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=2)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.mix.network_sleep()
        self.io.set_door(Drvr=Door.open)
        self.sd_tester.sd_tester.tester_present()
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=3)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.io.tcam_kl15_up()
        sleep(5)  # 诊断激活线5s钟变为连接状态
        
    @pytest.mark.v210
    @pytest.mark.network_sleep
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1993109(self):
        """
        Vnus880v，BGM休眠唤醒雨刮洗液液位为高液位，当车速车速大于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x02,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.mix.network_sleep()
        self.io.set_door(Drvr=Door.open)
        self.sd_tester.sd_tester.tester_present()
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=31)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=6)
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.io.tcam_kl15_up()
        sleep(5)  # 诊断激活线5s钟变为连接状态

    @pytest.mark.v210
    @pytest.mark.network_sleep
    @pytest.mark.full
    def test_caseid_1993108(self):
        """
        Vnus880v，BGM休眠唤醒雨刮洗液液位为高液位，当车速车速小于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x02,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.mix.network_sleep()
        self.io.set_door(Drvr=Door.open)
        self.sd_tester.sd_tester.tester_present()
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=2)
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.io.tcam_kl15_up()
        sleep(5)  # 诊断激活线5s钟变为连接状态

    @pytest.mark.v210
    @pytest.mark.network_sleep
    @pytest.mark.full
    def test_caseid_1993107(self):
        """
       Mars800v，BGM休眠唤醒雨刮洗涤液位为高液位，当车速车速大于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x01,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.mix.network_sleep()
        self.io.set_door(Drvr=Door.open)
        self.sd_tester.sd_tester.tester_present()
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=31)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=6)
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.io.tcam_kl15_up()
        sleep(5)  # 诊断激活线5s钟变为连接状态

    @pytest.mark.v210
    @pytest.mark.network_sleep
    @pytest.mark.full
    def test_caseid_1993106(self):
        """
       Mars800v，BGM休眠唤醒雨刮洗涤液位为高液位，当车速车速小于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x01,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.mix.network_sleep()
        self.io.set_door(Drvr=Door.open)
        self.sd_tester.sd_tester.tester_present()
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=2)
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.io.tcam_kl15_up()
        sleep(5)  # 诊断激活线5s钟变为连接状态

    @pytest.mark.v210
    @pytest.mark.network_sleep
    @pytest.mark.full
    def test_caseid_1993105(self):
        """
       Mars800v，BGM休眠唤醒雨刮洗涤液位为低液位，当车速车速大于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x01,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=6)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.mix.network_sleep()
        self.io.set_door(Drvr=Door.open)
        self.sd_tester.sd_tester.tester_present()
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=31)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=25)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=6)
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.io.tcam_kl15_up()
        sleep(5)  # 诊断激活线5s钟变为连接状态

    @pytest.mark.v210
    @pytest.mark.network_sleep
    @pytest.mark.full
    def test_caseid_1993104(self):
        """
       Mars800v，BGM休眠唤醒雨刮洗涤液位为低液位，当车速车速小于0.1km/h，检测雨刮洗涤低液位信号
        """
        self.sd_tester.write_ccp({501:0x02,950:0x01,962:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=3)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.io.set_wiper_washing_open()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=2)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.mix.network_sleep()
        self.io.set_door(Drvr=Door.open)
        self.sd_tester.sd_tester.tester_present()
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=0)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=3)
        self.io.set_wiper_washing_close()
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=1,sleep_time=1)
        self.bus_comm.check_WshrFldTankStsToHMI(expect_value=0,sleep_time=2)
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.io.tcam_kl15_up()
        sleep(5)  # 诊断激活线5s钟变为连接状态
        
    @pytest.mark.v220
    @pytest.mark.aa2
    @pytest.mark.smoke
    def test_caseid_1995578(self):
        """
        convience&normal 雨刮拨杆长按雨刮洗涤激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.aa2
    @pytest.mark.sanity
    def test_caseid_1995577(self):
        """
        convience&dyno 雨刮拨杆长按雨刮洗涤激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=3)
        self.bus_comm.check_wiper_wash_active_status(value=1)


    @pytest.mark.v220
    @pytest.mark.aa2
    @pytest.mark.smoke
    def test_caseid_1995576(self):
        """
        driving&normal 雨刮拨杆长按雨刮洗涤激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=3)
        self.bus_comm.check_wiper_wash_active_status(value=1)


    @pytest.mark.v220
    @pytest.mark.aa2
    @pytest.mark.sanity
    def test_caseid_1995575(self):
        """
        driving&dyno 雨刮拨杆长按雨刮洗涤激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=3)
        self.bus_comm.check_wiper_wash_active_status(value=1)


    @pytest.mark.v220
    @pytest.mark.aa2
    @pytest.mark.smoke
    def test_caseid_1995574(self):
        """
        active&normal 雨刮拨杆长按雨刮洗涤激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=3)
        self.bus_comm.check_wiper_wash_active_status(value=1)


    @pytest.mark.v220
    @pytest.mark.aa2
    @pytest.mark.sanity
    def test_caseid_1995573(self):
        """
        active&dyno 雨刮拨杆长按雨刮洗涤激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995572(self):
        """
        convience&crash 雨刮拨杆长按雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.CRASH)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995571(self):
        """
        convience&factory 雨刮拨杆长按雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.FACTORY)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995570(self):
        """
        convience&transport 雨刮拨杆长按雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995569(self):
        """
        driving&crash 雨刮拨杆长按雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.CRASH)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995568(self):
        """
        drivingfactory 雨刮拨杆长按雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.FACTORY)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995567(self):
        """
        driving&transport 雨刮拨杆长按雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995566(self):
        """
        active&crash 雨刮拨杆长按雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.CRASH)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995565(self):
        """
        active&factory 雨刮拨杆长按雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.FACTORY)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995564(self):
        """
        active&transport 雨刮拨杆长按雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995563(self):
        """
        inactive&normal 雨刮拨杆长按雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995562(self):
        """
        inactive&dyno 雨刮拨杆长按雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995561(self):
        """
        abandoned&normal 雨刮拨杆长按雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995560(self):
        """
        abandoned&dyno 雨刮拨杆长按雨刮洗涤禁用
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)