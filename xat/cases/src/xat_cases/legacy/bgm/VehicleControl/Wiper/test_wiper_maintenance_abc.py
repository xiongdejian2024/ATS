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
@allure.story("雨刮维修位置")
class TestWiperCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["WiperService_client","VehicleSetStatusService_client"])
        sleep(2)
        self.soa.start_get_wiper_switch_sts()

    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.bus_comm.set_vehspd_gear(vehspd=0.0) 
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.Off)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.hmi_set_wiper_mode(WiperPos.Front, WiperMode.Off)
        sleep(1)
        self.bus_comm.ipdu.rx_flag_reset_all()
        
    def after_each_func(self, ecu):
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble)
        try:
            self.bus_comm.set_wiper_lever_status(value=0)
        except Exception as e:
            logger.info(f"----------> after_each_func Error{str(e)}")

    def after_class(self, ecu):
        self.soa.stop_get_wiper_switch_sts()
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
    
    def wiper_maintenance_receive_signal(self,active=1):
        if active == 1:
            self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprPosnForSrvReq",1)
            self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        else:
            self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprPosnForSrvReq",0)
            self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)

    def rain_sensor_status(self,status="on"):
        if status == "on":
            self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
            self.bus_comm.check("backbonefr","CemBackBoneFr08","RainSnsrStsToHMI",1)
        else:
            self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
            self.bus_comm.check("backbonefr","CemBackBoneFr08","RainSnsrStsToHMI",0)

    @pytest.mark.smoke
    def test_caseid_1989836(self):
        """
        Conviecne&normal 雨刮洗涤激活，雨刮挡位关闭，收到雨刮维修激活请求
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",0)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)
       
    @pytest.mark.sanity
    def test_caseid_1989837(self):
        """
        Conviecne&Dyno 雨刮洗涤激活，雨刮挡位关闭，收到雨刮维修激活请求
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",0)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)

    @pytest.mark.sanity
    def test_caseid_1989838(self):
        """
        acitve&Dyno 雨刮洗涤激活，雨刮挡位关闭，收到雨刮维修激活请求
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",0)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)

        
    @pytest.mark.smoke
    def test_caseid_1989839(self):
        """
        acitve&Normal 雨刮洗涤激活，雨刮挡位关闭，收到雨刮维修激活请求
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",0)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)

    @pytest.mark.smoke
    def test_caseid_1989840(self):
        """
        driving&Nomal 雨刮洗涤激活，雨刮挡位关闭，收到雨刮维修激活请求
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",0)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)

    @pytest.mark.sanity
    def test_caseid_1989841(self):
        """
        driving&dyno 雨刮洗涤激活，雨刮挡位关闭，收到雨刮维修激活请求
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",0)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)


    @pytest.mark.sanity
    def test_caseid_1989845(self):
        """
        driving&dyno 雨刮维修激活，雨刮洗涤开启，雨刮维修退出
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.On)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
      
    @pytest.mark.smoke
    def test_caseid_1989868(self):
        """
        driving&Nomal 雨刮维修激活，雨刮洗涤开启，雨刮维修退出
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.On)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)


    @pytest.mark.sanity
    def test_caseid_1989869(self):
        """
        active&dyno 雨刮维修激活，雨刮洗涤开启，雨刮维修退出
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.On)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
      
    @pytest.mark.smoke
    def test_caseid_1989870(self):
        """
        active&normal 雨刮维修激活，雨刮洗涤开启，雨刮维修退出
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.On)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)

    @pytest.mark.smoke
    def test_caseid_1989871(self):
        """
        convience&normal 雨刮维修激活，雨刮洗涤开启，雨刮维修退出
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.On)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)

    @pytest.mark.sanity
    def test_caseid_1989872(self):
        """
        convience&dyno 雨刮维修激活，雨刮洗涤开启，雨刮维修退出
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.On)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)

    @pytest.mark.smoke
    def test_caseid_1989873(self):
        """
        convience&nomal 雨刮为off档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.sanity
    def test_caseid_1989874(self):
        """
        convience&dyno 雨刮为off档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.full
    def test_caseid_1989875(self):
        """
        convience&Transport 雨刮为off档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.full
    def test_caseid_1989876(self):
        """
        convience&factory 雨刮为off档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.full
    def test_caseid_1989877(self):
        """
        convience&Crash 雨刮为off档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.smoke
    def test_caseid_1989880(self):
        """
        driving&nomal 雨刮为off档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.sanity
    def test_caseid_1989878(self):
        """
        driving&dyno 雨刮为off档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.full
    def test_caseid_1989882(self):
        """
        driving&Transport 雨刮为off档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.full
    def test_caseid_1989881(self):
        """
        driving&factory 雨刮为off档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.full
    def test_caseid_1989879(self):
        """
        driving&Crash 雨刮为off档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.smoke
    def test_caseid_1989884(self):
        """
        active&nomal 雨刮为off档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
   

    @pytest.mark.sanity
    def test_caseid_1989887(self):
        """
        active&dyno 雨刮为off档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.full
    def test_caseid_1989883(self):
        """
        active&Transport 雨刮为off档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.full
    def test_caseid_1989885(self):
        """
        active&factory 雨刮为off档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.full
    def test_caseid_1989886(self):
        """
        active&Crash 雨刮为off档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)


    @pytest.mark.smoke
    def test_caseid_1989892(self):
        """
        inactive&nomal 雨刮为off档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.sanity
    def test_caseid_1989888(self):
        """
        inactive&dyno 雨刮为off档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.full
    def test_caseid_1989889(self):
        """
        inactive&Transport 雨刮为off档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.full
    def test_caseid_1989890(self):
        """
        inactive&factory 雨刮为off档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.full
    def test_caseid_1989891(self):
        """
        inactive&Crash 雨刮为off档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)


    @pytest.mark.smoke
    def test_caseid_1989908(self):
        """
        inactive&nomal 雨刮为auto档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        # self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.sanity
    def test_caseid_1989912(self):
        """
        inactive&dyno 雨刮为auto档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        # self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.full
    def test_caseid_1989909(self):
        """
        inactive&Transport 雨刮为auto档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        # self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.full
    def test_caseid_1989911(self):
        """
        inactive&factory 雨刮为auto档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        # self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.full
    def test_caseid_1989910(self):
        """
        inactive&Crash 雨刮为auto档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        # self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.smoke
    def test_caseid_1989905(self):
        """
        convience&nomal 雨刮为auto档，雨刮洗涤关闭，雨刮维修激活，雨传感器停用，退出维修位置，雨传感器启用且雨刮挡位为auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.rain_sensor_status(status="off")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.rain_sensor_status(status="on")
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.sanity
    def test_caseid_1989907(self):
        """
        convience&dyno 雨刮为auto档，雨刮洗涤关闭，雨刮维修激活，雨传感器停用，退出维修位置，雨传感器启用且雨刮挡位为auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.rain_sensor_status(status="off")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.rain_sensor_status(status="on")
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.full
    def test_caseid_1989906(self):
        """
        convience&Transport 雨刮为auto档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        # self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.full
    def test_caseid_1989904(self):
        """
        convience&factory 雨刮为auto档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        # self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.full
    def test_caseid_1989903(self):
        """
        convience&Crash 雨刮为auto档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        # self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.smoke
    def test_caseid_1989898(self):
        """
        driving&nomal 雨刮为auto档，雨刮洗涤关闭，雨刮维修激活，雨传感器停用，退出维修位置，雨传感器启用且雨刮挡位为auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.rain_sensor_status(status="off")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.rain_sensor_status(status="on")
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.sanity
    def test_caseid_1989900(self):
        """
        driving&dyno 雨刮为auto档，雨刮洗涤关闭，雨刮维修激活，雨传感器停用，退出维修位置，雨传感器启用且雨刮挡位为auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.rain_sensor_status(status="off")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.rain_sensor_status(status="on")
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.full
    def test_caseid_1989899(self):
        """
        driving&Transport 雨刮为auto档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        # self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.full
    def test_caseid_1989901(self):
        """
        driving&factory 雨刮为auto档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        # self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.full
    def test_caseid_1989902(self):
        """
        driving&Crash 雨刮为auto档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        # self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.smoke
    def test_caseid_1989897(self):
        """
        active&nomal 雨刮为auto档，雨刮洗涤关闭，雨刮维修激活，雨传感器停用，退出维修位置，雨传感器启用且雨刮挡位为auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.rain_sensor_status(status="off")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.rain_sensor_status(status="on")
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.sanity
    def test_caseid_1989893(self):
        """
        active&dyno 雨刮为auto档，雨刮洗涤关闭，雨刮维修激活，雨传感器停用，退出维修位置，雨传感器启用且雨刮挡位为auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.rain_sensor_status(status="off")
        self.bus_comm.check("backbonefr","CemBackBoneFr08","RainSnsrStsToHMI",0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.rain_sensor_status(status="on")
        self.bus_comm.check("backbonefr","CemBackBoneFr08","RainSnsrStsToHMI",1)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.full
    def test_caseid_1989894(self):
        """
        active&Transport 雨刮为auto档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        # self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.full
    def test_caseid_1989895(self):
        """
        active&factory 雨刮为auto档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        # self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.full
    def test_caseid_1989896(self):
        """
        active&Crash 雨刮为auto档，雨刮洗涤关闭，雨刮维修激活，雨刮维修退出后，雨刮保持auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",2)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        
    #========================================================================================================================
    @pytest.mark.full
    def test_caseid_1989913(self):
        """
        convience&normal 雨刮洗涤关闭，雨刮模式为1档，雨刮维修激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1989923(self):
        """
        convience&normal 雨刮洗涤关闭，雨刮模式为2档，雨刮维修激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.full
    def test_caseid_1989926(self):
        """
        convience&normal 雨刮洗涤关闭，雨刮模式为3档，雨刮维修激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1989927(self):
        """
        convience&normal 雨刮洗涤关闭，雨刮模式为4档，雨刮维修激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.full
    def test_caseid_1989928(self):
        """
        convience&normal 雨刮洗涤关闭，雨刮模式为单刮，雨刮维修激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)

    @pytest.mark.full
    def test_caseid_1989930(self):
        """
        driving&normal 雨刮洗涤关闭，雨刮模式为1档，雨刮维修激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1989931(self):
        """
        driving&normal 雨刮洗涤关闭，雨刮模式为2档，雨刮维修激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.full
    def test_caseid_1989932(self):
        """
        driving&normal 雨刮洗涤关闭，雨刮模式为3档，雨刮维修激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1989929(self):
        """
        driving&normal 雨刮洗涤关闭，雨刮模式为4档，雨刮维修激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.full
    def test_caseid_1989933(self):
        """
        driving&normal 雨刮洗涤关闭，雨刮模式为单刮，雨刮维修激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)

    @pytest.mark.full
    def test_caseid_1989937(self):
        """
        active&normal 雨刮洗涤关闭，雨刮模式为1档，雨刮维修激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1989936(self):
        """
        active&normal 雨刮洗涤关闭，雨刮模式为2档，雨刮维修激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.full
    def test_caseid_1989938(self):
        """
        active&normal 雨刮洗涤关闭，雨刮模式为3档，雨刮维修激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1989934(self):
        """
        active&normal 雨刮洗涤关闭，雨刮模式为4档，雨刮维修激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.full
    def test_caseid_1989935(self):
        """
        active&normal 雨刮洗涤关闭，雨刮模式为单刮，雨刮维修激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)


    @pytest.mark.full
    def test_caseid_1989939(self):
        """
        inactive&normal 雨刮洗涤关闭，雨刮模式为1档，雨刮维修激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1989943(self):
        """
        inactive&normal 雨刮洗涤关闭，雨刮模式为2档，雨刮维修激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.full
    def test_caseid_1989940(self):
        """
        inactive&normal 雨刮洗涤关闭，雨刮模式为3档，雨刮维修激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1989941(self):
        """
        inactive&normal 雨刮洗涤关闭，雨刮模式为4档，雨刮维修激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.full
    def test_caseid_1989942(self):
        """
        inactive&normal 雨刮洗涤关闭，雨刮模式为单刮，雨刮维修激活
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",1)
        sleep(1)
        self.bus_comm.check("backbonefr","CemBackBoneFr15","WiprInPosnForSrv",0)

    
    @pytest.mark.sanity
    def test_caseid_1989944(self):
        """
        convience&normal 雨刮维修激活后，雨刮由off档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
      
    
    @pytest.mark.sanity
    def test_caseid_1989949(self):
        """
        convience&normal 雨刮维修激活后，雨刮由off档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.sanity
    def test_caseid_1989950(self):
        """
        convience&normal 雨刮维修激活后，雨刮由off档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.sanity
    def test_caseid_1989951(self):
        """
        convience&normal 雨刮维修激活后，雨刮由off档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.sanity
    def test_caseid_1989953(self):
        """
        convience&normal 雨刮维修激活后，雨刮由off档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.sanity
    def test_caseid_1989954(self):
        """
        active&normal 雨刮维修激活后，雨刮由off档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.sanity
    def test_caseid_1989955(self):
        """
        active&normal 雨刮维修激活后，雨刮由off档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)


    @pytest.mark.sanity
    def test_caseid_1989956(self):
        """
        active&normal 雨刮维修激活后，雨刮由off档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.sanity
    def test_caseid_1989957(self):
        """
        active&normal 雨刮维修激活后，雨刮由off档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.sanity
    def test_caseid_1989958(self):
        """
        active&normal 雨刮维修激活后，雨刮由off档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)


    @pytest.mark.sanity
    def test_caseid_1989959(self):
        """
        driving&normal 雨刮维修激活后，雨刮由off档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.sanity
    def test_caseid_1989960(self):
        """
        driving&normal 雨刮维修激活后，雨刮由off档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)


    @pytest.mark.sanity
    def test_caseid_1989961(self):
        """
        driving&normal 雨刮维修激活后，雨刮由off档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.sanity
    def test_caseid_1989962(self):
        """
        driving&normal 雨刮维修激活后，雨刮由off档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.sanity
    def test_caseid_1989963(self):
        """
        driving&normal 雨刮维修激活后，雨刮由off档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.sanity
    def test_caseid_1989964(self):
        """
        inactive&normal 雨刮维修激活后，雨刮由off档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.sanity
    def test_caseid_1989965(self):
        """
        inactive&normal 雨刮维修激活后，雨刮由off档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)


    @pytest.mark.sanity
    def test_caseid_1989966(self):
        """
        inactive&normal 雨刮维修激活后，雨刮由off档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.sanity
    def test_caseid_1989967(self):
        """
        inactive&normal 雨刮维修激活后，雨刮由off档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.sanity
    def test_caseid_1989968(self):
        """
        inactive&normal 雨刮维修激活后，雨刮由off档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)
    

    @pytest.mark.sanity
    def test_caseid_1990038(self):
        """
        convience&normal 雨刮维修激活后，雨刮由auto档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
      
    
    @pytest.mark.sanity
    def test_caseid_1990036(self):
        """
        convience&normal 雨刮维修激活后，雨刮由auto档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.sanity
    def test_caseid_1990035(self):
        """
        convience&normal 雨刮维修激活后，雨刮由auto档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.sanity
    def test_caseid_1990037(self):
        """
        convience&normal 雨刮维修激活后，雨刮由auto档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.sanity
    def test_caseid_1990039(self):
        """
        convience&normal 雨刮维修激活后，雨刮由auto档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.sanity
    def test_caseid_1990031(self):
        """
        active&normal 雨刮维修激活后，雨刮由auto档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.sanity
    def test_caseid_1990030(self):
        """
        active&normal 雨刮维修激活后，雨刮由auto档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)


    @pytest.mark.sanity
    def test_caseid_1990034(self):
        """
        active&normal 雨刮维修激活后，雨刮由auto档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.sanity
    def test_caseid_1990032(self):
        """
        active&normal 雨刮维修激活后，雨刮由auto档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.sanity
    def test_caseid_1990033(self):
        """
        acitve&normal 雨刮维修激活后，雨刮由auto档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)


    @pytest.mark.sanity
    def test_caseid_1990024(self):
        """
        driving&normal 雨刮维修激活后，雨刮由auto档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.sanity
    def test_caseid_1990025(self):
        """
        driving&normal 雨刮维修激活后，雨刮由auto档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)


    @pytest.mark.sanity
    def test_caseid_1990027(self):
        """
        driving&normal 雨刮维修激活后，雨刮由auto档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.sanity
    def test_caseid_1990028(self):
        """
        driving&normal 雨刮维修激活后，雨刮由auto档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.sanity
    def test_caseid_1990026(self):
        """
        driving&normal 雨刮维修激活后，雨刮由auto档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.sanity
    def test_caseid_1990018(self):
        """
        inactive&normal 雨刮维修激活后，雨刮由auto档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.sanity
    def test_caseid_1990017(self):
        """
        inactive&normal 雨刮维修激活后，雨刮由auto档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)

    @pytest.mark.sanity
    def test_caseid_1990021(self):
        """
        inactive&normal 雨刮维修激活后，雨刮由auto档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.sanity
    def test_caseid_1990019(self):
        """
        inactive&normal 雨刮维修激活后，雨刮由auto档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)


    @pytest.mark.sanity
    def test_caseid_1990020(self):
        """
        inactive&normal 雨刮维修激活后，雨刮由auto档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.full
    def test_caseid_1990040(self):
        """
        convience&dyno 雨刮维修激活后，雨刮由off档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
      
    
    @pytest.mark.full
    def test_caseid_1990041(self):
        """
        convience&dyno 雨刮维修激活后，雨刮由off档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1990042(self):
        """
        convience&dyno 雨刮维修激活后，雨刮由off档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.full
    def test_caseid_1990043(self):
        """
        convience&dyno 雨刮维修激活后，雨刮由off档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1990044(self):
        """
        convience&dyno 雨刮维修激活后，雨刮由off档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.full
    def test_caseid_1990045(self):
        """
        active&dyno 雨刮维修激活后，雨刮由off档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1990046(self):
        """
        active&dyno 雨刮维修激活后，雨刮由off档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)


    @pytest.mark.full
    def test_caseid_1990047(self):
        """
        active&dyno 雨刮维修激活后，雨刮由off档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1990048(self):
        """
        active&dyno 雨刮维修激活后，雨刮由off档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.full
    def test_caseid_1990049(self):
        """
        active&dyno 雨刮维修激活后，雨刮由off档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)


    @pytest.mark.full
    def test_caseid_1990050(self):
        """
        driving&dyno 雨刮维修激活后，雨刮由off档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1990051(self):
        """
        driving&dyno 雨刮维修激活后，雨刮由off档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)


    @pytest.mark.full
    def test_caseid_1990052(self):
        """
        driving&dyno 雨刮维修激活后，雨刮由off档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1990053(self):
        """
        driving&dyno 雨刮维修激活后，雨刮由off档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.full
    def test_caseid_1990054(self):
        """
        driving&dyno 雨刮维修激活后，雨刮由off档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.full
    def test_caseid_1990055(self):
        """
        inactive&dyno 雨刮维修激活后，雨刮由off档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1990056(self):
        """
        inactive&dyno 雨刮维修激活后，雨刮由off档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)


    @pytest.mark.full
    def test_caseid_1990057(self):
        """
        inactive&dyno 雨刮维修激活后，雨刮由off档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.full
    def test_caseid_1990058(self):
        """
        inactive&dyno 雨刮维修激活后，雨刮由off档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1990059(self):
        """
        inactive&dyno 雨刮维修激活后，雨刮由off档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.full
    def test_caseid_1990060(self):
        """
        convience&factory 雨刮维修激活后，雨刮由off档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
      
    
    @pytest.mark.full
    def test_caseid_1990061(self):
        """
        convience&factory 雨刮维修激活后，雨刮由off档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1990062(self):
        """
        convience&factory 雨刮维修激活后，雨刮由off档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.full
    def test_caseid_1990063(self):
        """
        convience&factory 雨刮维修激活后，雨刮由off档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1990064(self):
        """
        convience&factory 雨刮维修激活后，雨刮由off档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.full
    def test_caseid_1990065(self):
        """
        active&factory 雨刮维修激活后，雨刮由off档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1990066(self):
        """
        active&factory 雨刮维修激活后，雨刮由off档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)


    @pytest.mark.full
    def test_caseid_1990067(self):
        """
        active&factory 雨刮维修激活后，雨刮由off档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1990068(self):
        """
        active&factory 雨刮维修激活后，雨刮由off档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.full
    def test_caseid_1990069(self):
        """
        active&factory 雨刮维修激活后，雨刮由off档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)


    @pytest.mark.full
    def test_caseid_1990070(self):
        """
        driving&factory 雨刮维修激活后，雨刮由off档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1990071(self):
        """
        driving&factory 雨刮维修激活后，雨刮由off档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)


    @pytest.mark.full
    def test_caseid_1990072(self):
        """
        driving&factory 雨刮维修激活后，雨刮由off档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1990073(self):
        """
        driving&factory 雨刮维修激活后，雨刮由off档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.full
    def test_caseid_1990074(self):
        """
        driving&factory 雨刮维修激活后，雨刮由off档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.full
    def test_caseid_1990075(self):
        """
        inactive&factory 雨刮维修激活后，雨刮由off档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1990076(self):
        """
        inactive&factory 雨刮维修激活后，雨刮由off档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)


    @pytest.mark.full
    def test_caseid_1990077(self):
        """
        inactive&factory 雨刮维修激活后，雨刮由off档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.full
    def test_caseid_1990078(self):
        """
        inactive&factory 雨刮维修激活后，雨刮由off档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1990079(self):
        """
        inactive&factory 雨刮维修激活后，雨刮由off档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)
    
    @pytest.mark.full
    def test_caseid_1990085(self):
        """
        convience&crash 雨刮维修激活后，雨刮由off档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
      
    
    @pytest.mark.full
    def test_caseid_1990086(self):
        """
        convience&crash 雨刮维修激活后，雨刮由off档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1990087(self):
        """
        convience&crash 雨刮维修激活后，雨刮由off档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.full
    def test_caseid_1990088(self):
        """
        convience&crash 雨刮维修激活后，雨刮由off档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1990089(self):
        """
        convience&crash 雨刮维修激活后，雨刮由off档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.full
    def test_caseid_1990090(self):
        """
        active&crash 雨刮维修激活后，雨刮由off档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1990091(self):
        """
        active&crash 雨刮维修激活后，雨刮由off档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)


    @pytest.mark.full
    def test_caseid_1990092(self):
        """
        active&crash 雨刮维修激活后，雨刮由off档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1990093(self):
        """
        active&crash 雨刮维修激活后，雨刮由off档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.full
    def test_caseid_1990094(self):
        """
        active&crash 雨刮维修激活后，雨刮由off档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)


    @pytest.mark.full
    def test_caseid_1990095(self):
        """
        driving&crash 雨刮维修激活后，雨刮由off档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1990096(self):
        """
        driving&crash 雨刮维修激活后，雨刮由off档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)


    @pytest.mark.full
    def test_caseid_1990097(self):
        """
        driving&crash 雨刮维修激活后，雨刮由off档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1990098(self):
        """
        driving&crash 雨刮维修激活后，雨刮由off档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.full
    def test_caseid_1990099(self):
        """
        driving&crash 雨刮维修激活后，雨刮由off档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.full
    def test_caseid_1990100(self):
        """
        inactive&crash 雨刮维修激活后，雨刮由off档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1990101(self):
        """
        inactive&crash 雨刮维修激活后，雨刮由off档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)


    @pytest.mark.full
    def test_caseid_1990102(self):
        """
        inactive&crash 雨刮维修激活后，雨刮由off档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.full
    def test_caseid_1990103(self):
        """
        inactive&crash 雨刮维修激活后，雨刮由off档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1990104(self):
        """
        inactive&crash 雨刮维修激活后，雨刮由off档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)


    @pytest.mark.full
    def test_caseid_1990107(self):
        """
        convience&transport 雨刮维修激活后，雨刮由off档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
      
    
    @pytest.mark.full
    def test_caseid_1990108(self):
        """
        convience&transport 雨刮维修激活后，雨刮由off档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1990109(self):
        """
        convience&transport 雨刮维修激活后，雨刮由off档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.full
    def test_caseid_1990110(self):
        """
        convience&transport 雨刮维修激活后，雨刮由off档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1990111(self):
        """
        convience&transport 雨刮维修激活后，雨刮由off档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.full
    def test_caseid_1990112(self):
        """
        active&transport 雨刮维修激活后，雨刮由off档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1990113(self):
        """
        active&transport 雨刮维修激活后，雨刮由off档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)


    @pytest.mark.full
    def test_caseid_1990114(self):
        """
        active&transport 雨刮维修激活后，雨刮由off档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1990115(self):
        """
        active&transport 雨刮维修激活后，雨刮由off档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.full
    def test_caseid_1990116(self):
        """
        active&transport 雨刮维修激活后，雨刮由off档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)


    @pytest.mark.full
    def test_caseid_1990117(self):
        """
        driving&transport 雨刮维修激活后，雨刮由off档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1990118(self):
        """
        driving&transport 雨刮维修激活后，雨刮由off档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)


    @pytest.mark.full
    def test_caseid_1990119(self):
        """
        driving&transport 雨刮维修激活后，雨刮由off档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1990120(self):
        """
        driving&transport 雨刮维修激活后，雨刮由off档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.full
    def test_caseid_1990121(self):
        """
        driving&transport 雨刮维修激活后，雨刮由off档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.full
    def test_caseid_1990122(self):
        """
        inactive&transport 雨刮维修激活后，雨刮由off档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1990123(self):
        """
        inactive&transport 雨刮维修激活后，雨刮由off档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)


    @pytest.mark.full
    def test_caseid_1990124(self):
        """
        inactive&transport 雨刮维修激活后，雨刮由off档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.full
    def test_caseid_1990125(self):
        """
        inactive&transport 雨刮维修激活后，雨刮由off档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1990126(self):
        """
        inactive&transport 雨刮维修激活后，雨刮由off档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.full
    def test_caseid_1990147(self):
        """
        convience&dyno 雨刮维修激活后，雨刮由auto档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
      
    
    @pytest.mark.full
    def test_caseid_1990145(self):
        """
        convience&dyno 雨刮维修激活后，雨刮由auto档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1990144(self):
        """
        convience&dyno 雨刮维修激活后，雨刮由auto档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.full
    def test_caseid_1990146(self):
        """
        convience&dyno 雨刮维修激活后，雨刮由auto档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)   
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1990148(self):
        """
        convience&dyno 雨刮维修激活后，雨刮由auto档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.full
    def test_caseid_1990140(self):
        """
        active&dyno 雨刮维修激活后，雨刮由auto档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1990139(self):
        """
        active&dyno 雨刮维修激活后，雨刮由auto档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)


    @pytest.mark.full
    def test_caseid_1990143(self):
        """
        active&dyno 雨刮维修激活后，雨刮由auto档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1990141(self):
        """
        active&dyno 雨刮维修激活后，雨刮由auto档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.full
    def test_caseid_1990142(self):
        """
        acitve&dyno 雨刮维修激活后，雨刮由auto档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)


    @pytest.mark.full
    def test_caseid_1990134(self):
        """
        driving&dyno 雨刮维修激活后，雨刮由auto档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1990135(self):
        """
        driving&dyno 雨刮维修激活后，雨刮由auto档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)


    @pytest.mark.full
    def test_caseid_1990137(self):
        """
        driving&dyno 雨刮维修激活后，雨刮由auto档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.full
    def test_caseid_1990138(self):
        """
        driving&dyno 雨刮维修激活后，雨刮由auto档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.full
    def test_caseid_1990136(self):
        """
        driving&dyno 雨刮维修激活后，雨刮由auto档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.full
    def test_caseid_1990130(self):
        """
        inactive&dyno 雨刮维修激活后，雨刮由auto档切换雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.full
    def test_caseid_1990129(self):
        """
        inactive&dyno 雨刮维修激活后，雨刮由auto档切换雨刮模式为单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)

    @pytest.mark.full
    def test_caseid_1990133(self):
        """
        inactive&dyno 雨刮维修激活后，雨刮由auto档切换雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.full
    def test_caseid_1990131(self):
        """
        inactive&dyno 雨刮维修激活后，雨刮由auto档切换雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO,ccp={503:0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)


    @pytest.mark.full
    def test_caseid_1990132(self):
        """
        inactive&dyno 雨刮维修激活后，雨刮由auto档切换雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=0)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.sanity
    def test_wiper_ctrl_caseid_1981072(self):
        """
        "进入雨刮维修位置，BGM复位之后继续维持在维修模式"
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503:0x2,401: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check_wiper_maintain_ser_pos_req(MaintainPosReq.On)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.soa.get_wiper_maintaince_pos(isOn.On)

    @pytest.mark.sanity
    def test_wiper_ctrl_caseid_1981073(self):
        """
        "雨刮不在维修位置，BGM复位之后雨刮不在维修位置"
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503:0x2,401: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.bus_comm.check_wiper_maintain_ser_pos_req(MaintainPosReq.Off)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.soa.get_wiper_maintaince_pos(isOn.Off)  

    @pytest.mark.sanity
    def test_wiper_ctrl_caseid_1981202(self):
        """
        "雨刮维修位置NVM记忆"
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503:0x2,401: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.soa.get_wiper_maintaince_pos(sts=isOn.On)
        self.bus_comm.check_wiper_maintain_ser_pos_req(MaintainPosReq.On)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        sleep(15)
        self.soa.get_wiper_maintaince_pos(sts=isOn.On)

        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.get_wiper_maintaince_pos(sts=isOn.Off)
        self.bus_comm.check_wiper_maintain_ser_pos_req(MaintainPosReq.Off)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        sleep(15)
        self.soa.get_wiper_maintaince_pos(sts=isOn.Off)
        sleep(10)

    @pytest.mark.sanity
    def test_caseid_1990250(self):
        """
        driving&normal雨刮为off档，雨刮维修激活，进入洗车模式，雨刮维修退出
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wash_mode(sts=isOn.On)
        self.soa.get_wiper_maintaince_pos(isOn.Off)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)

    @pytest.mark.sanity
    def test_caseid_1990251(self):
        """
        convience&normal雨刮为off档，雨刮维修激活，进入洗车模式，雨刮维修退出
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wash_mode(sts=isOn.On)
        self.soa.get_wiper_maintaince_pos(isOn.Off)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)

    @pytest.mark.sanity
    def test_caseid_1990252(self):
        """
        active&normal雨刮为off档，雨刮维修激活，进入洗车模式，雨刮维修退出
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wash_mode(sts=isOn.On)
        self.soa.get_wiper_maintaince_pos(isOn.Off)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)

    @pytest.mark.sanity
    def test_caseid_1990253(self):
        """
        inactive&normal雨刮为off档，雨刮维修激活，进入洗车模式，雨刮维修退出
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={503: 0x2})
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr67","WiprFrntSrvModReq",1)
        sleep(0.7)
        self.wiper_maintenance_receive_signal(active=1)
        self.soa.hmi_set_wash_mode(sts=isOn.On)
        self.soa.get_wiper_maintaince_pos(isOn.Off)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)

    @pytest.mark.v220
    @pytest.mark.smoke
    def test_caseid_1995615(self):
        """
        convience&normal 雨刮拨杆单刮进维修
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintenance_mode_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintenance_mode_signal("deactive")
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check_single_wiper_status(value=0)
        
    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995614(self):
        """
        convience&dyno 雨刮拨杆单刮进维修
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintenance_mode_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintenance_mode_signal("deactive")
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.smoke
    def test_caseid_1995613(self):
        """
        active&normal 雨刮拨杆单刮进维修
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintenance_mode_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintenance_mode_signal("deactive")
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check_single_wiper_status(value=0)
        
    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995612(self):
        """
        active&dyno 雨刮拨杆单刮进维修
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintenance_mode_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintenance_mode_signal("deactive")
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.smoke
    def test_caseid_1995611(self):
        """
        driving&normal 雨刮拨杆单刮进维修
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintenance_mode_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintenance_mode_signal("deactive")
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check_single_wiper_status(value=0)
        
    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995610(self):
        """
        driving&dyno 雨刮拨杆单刮进维修
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintenance_mode_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintenance_mode_signal("deactive")
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995609(self):
        """
        convience&normal 雨刮拨杆洗涤进维修
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=2)
        sleep(1)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintenance_mode_signal("active")
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintenance_mode_signal("deactive")
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995608(self):
        """
        convience&dyno 雨刮拨杆洗涤进维修
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=2)
        sleep(1)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintenance_mode_signal("active")
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintenance_mode_signal("deactive")
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995607(self):
        """
        active&normal 雨刮拨杆洗涤进维修
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=2)
        sleep(1)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintenance_mode_signal("active")
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintenance_mode_signal("deactive")
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995606(self):
        """
        active&dyno 雨刮拨杆洗涤进维修
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=2)
        sleep(1)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintenance_mode_signal("active")
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintenance_mode_signal("deactive")
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995605(self):
        """
        driving&normal 雨刮拨杆洗涤进维修
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=2)
        sleep(1)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintenance_mode_signal("active")
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintenance_mode_signal("deactive")
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995604(self):
        """
        driving&dyno 雨刮拨杆洗涤进维修
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=2)
        sleep(1)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintenance_mode_signal("active")
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintenance_mode_signal("deactive")
        self.soa.get_wiper_wash_sts(WiperPos.Front,isOn.Off)
        self.bus_comm.check_wiper_wash_active_status(value=1)