#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_steerwheel_ctrl.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/11/21 11:30
@Description: BGM车控车方向盘功能
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
class TestSteerWheelCtrl(TestABCBase):
    
    def before_class(self, ecu):
        # logger.info("------------------>复位BGM")
        # self.io.bgm_power_off()
        # sleep(2)
        # self.io.bgm_power_on()
        # time.sleep(15)
        # logger.info("------------------>复位BGM结束")
        self.soa.update(["SteerWheelService_client"])
        sleep(2)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4})
        self.bus_comm.set_Hv_sys_relay_sts(HvSysRelaySts.Close)


    def before_each_func(self, ecu):
        # self.mix.set_dtc_precontion()
        # self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.sd_tester.send_request_and_recv_response([0x19, 0x02, 0x09])    #确认下是否有方向盘DTC
        self.bus_comm.set_steerwheel_PwrAllwd(PwrAllwd_val=90)
        pass

    def after_each_func(self, ecu):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        # self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Off)
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x71])
        sleep(.2)
        self.sd_tester.send_request_and_recv_response([0x31, 0x02, 0X20 ,0x0C],recv=[0x71])
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)

        pass

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    # @allure.title("Normal模式手动控制方向盘加热打开_1档")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    # )
    # @pytest.mark.smoke
    # def test_caseid_1960106(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
    #     self.soa.hmi_set_steer_wheel_heat_level(HeatLevel.Low,source=SourceId.HMI)
    #     self.bus_comm.check_steerwheel_heat_req(
    #         lev_sts=HeatLevel.Low, avl_sts=AvlSts.On)
    #     self.soa.event_check_steer_wheel_heat_level(HeatLevel.Low)
    #     self.soa.get_steer_wheel_heat_level(HeatLevel.Low)

    @allure.title("Dyno模式手动控制方向盘加热打开_1档")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2359979?projectId=46")
    @pytest.mark.full
    # @pytest.mark.a99
    def test_caseid_1982018(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO)
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)

    @allure.title("Dyno模式手动控制方向盘加热打开_2档")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2359909?projectId=46")
    @pytest.mark.full
    # @pytest.mark.a99
    def test_caseid_1960128(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO)
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Mid,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Mid)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Mid, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Mid,source=SourceId.HMI)

    @allure.title("Dyno模式手动控制方向盘加热打开_3档")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2359935?projectId=46")
    @pytest.mark.full
    # @pytest.mark.a99
    def test_caseid_1960129(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO)
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.High,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.High, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.High,source=SourceId.HMI)
        
        
        
    @allure.title("454327 使用模式切至Abandoned，无法调节方向盘")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.smoke
    @pytest.mark.edit
    def test_caseid_1985290(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH,usage_mode=UsageMode.ABANDONED)
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x71])
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=False)
        
    @allure.title("Dyno模式车速大于5km/h，无法手动调节方向盘")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1112
    def test_caseid_1960134(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO,usage_mode=UsageMode.DRIVING,veh_spd=0x9ff)   #10km/h
        # self.mix.set_common_precontion(car_mode=CarMode.NORMAL,usage_mode=UsageMode.CONVENIENCE,veh_spd=10)
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=False)

# # # 新用例 # # # # # # # #
# # # 新用例 # # # # # # # # 

    @allure.title("Normal模式手动控制方向盘加热打开_1档")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.smoke
    # @pytest.mark.a99
    def test_caseid_1960106(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)   #待请确认
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4, 0x959:0x1}) 
        # self.bus_comm.set_steerwheel_PwrAllwd(PwrAllwd_val=0)
        # sleep(12)
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        # assert False

    @allure.title("CCP#13=0x4_在normal和Convenience，手动设置U型方向盘加热等级为1档时，对应的功率（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.smoke
    # @pytest.mark.a99
    def test_caseid_1992955(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4, 0x959:0x1}) 
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
  
        
    @allure.title("CCCP#13=0x4_在normal和Convenience下，手动设置U型方向盘加热等级为OFF（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.smoke
    # @pytest.mark.a99
    def test_caseid_1992951(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4, 0x959:0x1}) 
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        
        
        
    @allure.title("配置CCP#186=0x2，电车有U型方向盘加热功能")
    @pytest.mark.smoke
    # @pytest.mark.a99
    def test_caseid_1992924(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4, 0x959:0x1}) 
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        
        
    @allure.title("CCP#13=0x4_在normal和Convenience，手动设置O型方向盘加热等级为1档时，对应的功率（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.smoke
    # @pytest.mark.a99
    def test_caseid_1992765(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4, 0x959:0x2}) 
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
  
        
    @allure.title("CCP#13=0x4_在normal和Convenience下，手动设置O型方向盘加热等级为OFF（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.smoke
    # @pytest.mark.a99
    def test_caseid_1992761(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4, 0x959:0x2}) 
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        
        
    # @allure.title("CCP#13=0x4_在normal和INACTIVE，远程设置U型方向盘加热等级为1档时，对应的功率（CCP#959=0x01）")     
    # @pytest.mark.smoke
    # # @pytest.mark.a99
    # def test_caseid_1992891(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
    #     self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4, 0x959:0x1}) 
    #     self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
    #     self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
    #     self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
    @allure.title("CCP#13=0x4_在normal和INACTIVE，远程设置U型方向盘加热等级为1档时，对应的功率（CCP#959=0x01）")  
    @pytest.mark.smoke
    # @pytest.mark.a99
    def test_caseid_1992619(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4, 0x959:0x1}) 
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.High)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.High, DesPwr_sts=DesPwr.High_power)
        
        
    # @allure.title("CCP#13=0x4_在normal和INACTIVE下，远程设置U型方向盘加热等级为OFF（CCP#959=0x01）")
    # @pytest.mark.smoke
    # # @pytest.mark.a99
    # def test_caseid_1992885(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
    #     self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4, 0x959:0x1}) 
    #     self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Off)
    #     self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
    #     self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        
        
        
    # @allure.title("CCP#13=0x4_在normal和INACTIVE下，远程设置O型方向盘加热等级为OFF（CCP#959=0x02）")
    # @pytest.mark.smoke
    # # @pytest.mark.a99
    # def test_caseid_1992695(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
    #     self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4, 0x959:0x2}) 
    #     self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Off)
    #     self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
    #     self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        
        
    @allure.title("U型方向盘_状态切换：ON state_OFF state_本地加热（CCP#13=0x4）")
    @pytest.mark.smoke
    # @pytest.mark.a99
    def test_caseid_1992828(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4, 0x959:0x1}) 
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(lev_sts=HeatLevel.Off, avl_sts=AvlSts.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        
  
############# 0913###################
        
        
    @allure.title("CCP#13=0x04_在Normal和convenience，调节电车U型方向盘（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    # @pytest.mark.a0913
    def test_caseid_1992807(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, veh_spd=0)
        self.sd_tester.write_ccp(ccp={0x959:0x1}) 
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=True)
        
        
    @allure.title("反例_CCP#13=0x04_在CRASH和convenience，调节电车U型方向盘不成功（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    # @pytest.mark.a0913
    def test_caseid_1992796(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.CONVENIENCE, veh_spd=0)
        self.sd_tester.write_ccp(ccp={0x959:0x1}) 
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=False)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=False)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=False)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=False)
        
        
      ############################ 0917
    @allure.title("CCP#13=0x04_在transport和inactive，调节电车U型方向盘（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992802(self):
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.INACTIVE, veh_spd=0, ccp={0x959:0x1})
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=True)
        
        
    @allure.title("CCP#13=0x04_在transport和inactive，调节电车O型方向盘（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992613(self):
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.INACTIVE, veh_spd=0, ccp={0x959:0x2})
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=True)

    @allure.title("CCP#13=0x04_在transport和convenience，调节电车U型方向盘（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992803(self):
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.CONVENIENCE, veh_spd=0, ccp={0x959:0x1})
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=True)
        
    @allure.title("CCP#13=0x04_在transport和convenience，调节电车O型方向盘（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992614(self):
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.CONVENIENCE, veh_spd=0, ccp={0x959:0x2})
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=True)
    
      
    @allure.title("CCP#13=0x04_在Normal和inactive，调节电车U型方向盘（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992806(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, veh_spd=0, ccp={0x959:0x1})
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=True)
       
       
        
    @allure.title("CCP#13=0x04_在Normal和inactive，调节电车O型方向盘（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992617(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, veh_spd=0, ccp={0x959:0x2})
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=True)
        
        
    @allure.title("CCP#13=0x04_在Normal和drving，调节电车U型方向盘（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992804(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, veh_spd=0, ccp={0x959:0x1})
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=True)
        
        
    @allure.title("CCP#13=0x04_在Normal和drving，调节电车O型方向盘（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992615(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, veh_spd=0, ccp={0x959:0x2})
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=True)
        
        
    @allure.title("CCP#13=0x04_在Normal和convenience，调节电车U型方向盘（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992807(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, veh_spd=0, ccp={0x959:0x1})
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=True)
        
        
    @allure.title("CCP#13=0x04_在Normal和convenience，调节电车O型方向盘（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992618(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, veh_spd=0, ccp={0x959:0x2})
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=True)
        
        
    @allure.title("CCP#13=0x04_在Normal和active，调节电车U型方向盘（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992805(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, veh_spd=0, ccp={0x959:0x1})
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=True)
        
        
    @allure.title("CCP#13=0x04_在Normal和active，调节电车O型方向盘（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992616(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, veh_spd=0, ccp={0x959:0x2})
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=True)
        
        
    @allure.title("CCP#13=0x04_在factory和inactive，调节电车U型方向盘（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.full
    @pytest.mark.a0917
    def test_caseid_1992800(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.INACTIVE, veh_spd=0, ccp={0x959:0x1})
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=True)
        
        
    @allure.title("CCP#13=0x04_在factory和inactive，调节电车O型方向盘（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992611(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.INACTIVE, veh_spd=0, ccp={0x959:0x2})
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=True)
        
        
    @allure.title("CCP#13=0x04_在factory和convenience，调节电车U型方向盘（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.full
    @pytest.mark.a0917
    def test_caseid_1992801(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.CONVENIENCE, veh_spd=0, ccp={0x959:0x1})
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=True)
        
        
    @allure.title("CCP#13=0x04_在factory和convenience，调节电车O型方向盘（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.full
    @pytest.mark.a0917
    def test_caseid_1992612(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.CONVENIENCE, veh_spd=0, ccp={0x959:0x2})
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=True)
        
        
    @allure.title("CCP#13=0x04_在Dyno和inactive，调节电车U型方向盘（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992799(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.INACTIVE, veh_spd=0, ccp={0x959:0x1})
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=True)
        
        
    @allure.title("CCP#13=0x04_在Dyno和inactive，调节电车O型方向盘（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992610(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.INACTIVE, veh_spd=0, ccp={0x959:0x2})
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=True)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=True)
        
        
    @allure.title("反例_CCP#13=0x04_在transport和abandone，调节电车U型方向盘不成功（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992794(self):
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.ABANDONED, veh_spd=0, ccp={0x959:0x1})
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x71])
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=False)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=False)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=False)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=False)
        self.sd_tester.send_request_and_recv_response([0x31, 0x02, 0X20 ,0x0C],recv=[0x71])
        
        
    @allure.title("反例_CCP#13=0x04_在transport和abandone，调节电车O型方向盘不成功（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992605(self):
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.ABANDONED, veh_spd=0, ccp={0x959:0x2})
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x71])
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=False)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=False)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=False)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=False)
        self.sd_tester.send_request_and_recv_response([0x31, 0x02, 0X20 ,0x0C],recv=[0x71])
        
        
    @allure.title("反例_CCP#13=0x04_在Normal和convenience，调节电车U型方向盘请求忽略_PwrLvlElecMai（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.full
    @pytest.mark.a0917
    def test_caseid_1992797(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, veh_spd=0, ccp={0x959:0x1})
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E ,0x03, 0x00, 0X40],recv=[0x6F,0x42,0x9E])
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.NotInhb)
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E ,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E])
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        
    @allure.title("反例_CCP#13=0x04_在Normal和convenience，调节电车O型方向盘请求忽略_PwrLvlElecMai（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.full
    @pytest.mark.a1112
    def test_caseid_1992608(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, veh_spd=0, ccp={0x959:0x2})
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E ,0x03, 0x00, 0X40],recv=[0x6F,0x42,0x9E])
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.NotInhb)
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E ,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E])
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E ,0x03, 0x00, 0X40],recv=[0x6F,0x42,0x9E])  #恢复初始值
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.NotInhb)
        
        
    @allure.title("反例_CCP#13=0x04_在Normal和convenience，调节电车O型方向盘请求忽略_EngyLvlElecMai=1（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1112
    def test_caseid_1992609(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, veh_spd=0, ccp={0x959:0x2})
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9D ,0x03, 0x00, 0X40],recv=[0x6F,0x42,0x9D])
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.NotInhb)
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9D ,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9D])
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9D ,0x03, 0x00, 0X40],recv=[0x6F,0x42,0x9D])
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.NotInhb)
        
        
    @allure.title("反例_CCP#13=0x04_在nomal和abandone，调节电车U型方向盘不成功（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992795(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED, veh_spd=0, ccp={0x959:0x1})
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x71])
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        self.sd_tester.send_request_and_recv_response([0x31, 0x02, 0X20 ,0x0C],recv=[0x71])        
        
        
        
    @allure.title("反例_CCP#13=0x04_在nomal和abandone，调节电车O型方向盘不成功（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.full
    @pytest.mark.a0917
    def test_caseid_1992606(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED, veh_spd=0, ccp={0x959:0x2})
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x71])
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        self.sd_tester.send_request_and_recv_response([0x31, 0x02, 0X20 ,0x0C],recv=[0x71])        
        
    @allure.title("反例_CCP#13=0x04_在nomal和abandone，调节电车O型方向盘不成功_车速超过5km/h（CCP#959=0x02）")   #暂时不上传
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1112
    def test_caseid_1992602(self):  
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, veh_spd=0x9ff, ccp={0x959:0x2})
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        
    @allure.title("反例_CCP#13=0x04_在factory和abandone，调节电车U型方向盘不成功（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.full
    @pytest.mark.a0917
    def test_caseid_1992793(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.ABANDONED, veh_spd=0, ccp={0x959:0x1})
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x71])
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        self.sd_tester.send_request_and_recv_response([0x31, 0x02, 0X20 ,0x0C],recv=[0x71])        
        
    @allure.title("反例_CCP#13=0x04_在factory和abandone，调节电车O型方向盘不成功（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.full
    @pytest.mark.a0917
    def test_caseid_1992604(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.ABANDONED, veh_spd=0, ccp={0x959:0x2})
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x71])
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        self.sd_tester.send_request_and_recv_response([0x31, 0x02, 0X20 ,0x0C],recv=[0x71])        
        
        
    @allure.title("反例_CCP#13=0x04_在Dyno和abandone，调节电车U型方向盘不成功（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.full
    @pytest.mark.a0917
    def test_caseid_1992792(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.ABANDONED, veh_spd=0, ccp={0x959:0x1})
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x71])
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        self.sd_tester.send_request_and_recv_response([0x31, 0x02, 0X20 ,0x0C],recv=[0x71])        
        
        
    @allure.title("反例_CCP#13=0x04_在Dyno和abandone，调节电车O型方向盘不成功（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.full
    @pytest.mark.a0917
    def test_caseid_1992603(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.ABANDONED, veh_spd=0, ccp={0x959:0x2})
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x71])
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        self.sd_tester.send_request_and_recv_response([0x31, 0x02, 0X20 ,0x0C],recv=[0x71])        
        
        
    @allure.title("反例_CCP#13=0x04_在CRASH和convenience，调节电车U型方向盘不成功（CCP#959=0x01））")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992796(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.CONVENIENCE, veh_spd=0, ccp={0x959:0x1})
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x71])
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        self.sd_tester.send_request_and_recv_response([0x31, 0x02, 0X20 ,0x0C],recv=[0x71])
        
        
    @allure.title("反例_CCP#13=0x04_在CRASH和convenience，调节电车O型方向盘不成功（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992607(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.ABANDONED, veh_spd=0, ccp={0x959:0x2})
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x71])
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        self.sd_tester.send_request_and_recv_response([0x31, 0x02, 0X20 ,0x0C],recv=[0x71])


    @allure.title("CCP#13=0x4_在normal和Inactive下，远程设置U型方向盘加热等级为3档时，对应的功率（CCP#959=0x01）")  
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992876(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x1})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.High)
        sleep(.1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.High, DesPwr_sts=DesPwr.High_power)
         
        
        
    @allure.title("CCP#13=0x4_在normal和Inactive下，远程设置U型方向盘加热等级为2档时，对应的功率（CCP#959=0x01）")  
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992877(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x1})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Mid)
        sleep(.1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Mid)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Mid, DesPwr_sts=DesPwr.Mid_power)
        
        
    @allure.title("CCP#13=0x4_在normal和Inactive下，远程设置U型方向盘加热等级为1档时，对应的功率（CCP#959=0x01）")  
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992878(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x1})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        sleep(.1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)



    @allure.title("CCP#13=0x4_在normal和Inactive下，远程设置O型方向盘加热等级为3档时，对应的功率（CCP#959=0x02）")  
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992686(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x1})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.High)
        sleep(.1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.High, DesPwr_sts=DesPwr.High_power)
         
        
        
    @allure.title("CCP#13=0x4_在normal和Inactive下，远程设置O型方向盘加热等级为2档时，对应的功率（CCP#959=0x02）")  
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992687(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x1})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Mid)
        sleep(.1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Mid)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Mid, DesPwr_sts=DesPwr.Mid_power)
        
        
    @allure.title("CCP#13=0x4_在normal和Inactive下，远程设置O型方向盘加热等级为1档时，对应的功率（CCP#959=0x02）")  
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992688(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x1})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        sleep(.1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        
    @allure.title("CCP#13=0x4_在normal和Inactive下，远程设置O型方向盘加热等级为1档时，对应的功率（CCP#959=0x00）")  
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992683(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x0})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        sleep(.1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)     #第一次执行到这儿（跑到这儿38条）
        
        
        
        
        
    @allure.title("CCP#13=0x4_在normal和Driving下，手动设置U型方向盘加热等级为3档时，对应的功率（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992940(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={186: 0x02, 13: 0x4, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.High,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.High, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.High,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.High, DesPwr_sts=DesPwr.High_power)
        
        
    @allure.title("CCP#13=0x4_在normal和Driving下，手动设置U型方向盘加热等级为2档时，对应的功率（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992941(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={186: 0x02, 13: 0x4, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Mid,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Mid)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Mid, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Mid,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Mid, DesPwr_sts=DesPwr.Mid_power)
        
        
    @allure.title("CCP#13=0x4_在normal和Driving下，手动设置U型方向盘加热等级为1档时，对应的功率（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992942(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={186: 0x02, 13: 0x4, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        
        
    @allure.title("CCP#13=0x4_在normal和Driving下，手动设置U型方向盘加热等级为1档时，对应的功率（CCP#959=0x00）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992939(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={186: 0x02, 13: 0x4, 0x959:0x0})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        
        



    @allure.title("CCP#13=0x4_在normal和Driving下，手动设置O型方向盘加热等级为3档时，对应的功率（CCP#959=0x02））")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992750(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={186: 0x02, 13: 0x4, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.High,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.High, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.High,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.High, DesPwr_sts=DesPwr.High_power)
        
        
    @allure.title("CCP#13=0x4_在normal和Driving下，手动设置O型方向盘加热等级为2档时，对应的功率（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992751(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={186: 0x02, 13: 0x4, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Mid,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Mid)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Mid, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Mid,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Mid, DesPwr_sts=DesPwr.Mid_power)
        
        
    @allure.title("CCP#13=0x4_在normal和Driving下，手动设置O型方向盘加热等级为1档时，对应的功率（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992752(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={186: 0x02, 13: 0x4, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        
        
    @allure.title("CCP#13=0x4_在normal和Driving下，手动设置O型方向盘加热等级为1档时，对应的功率（CCP#959=0x00）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992749(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={186: 0x02, 13: 0x4, 0x959:0x0})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        
    @allure.title("CCP#13=0x4_在normal和Convenience下，手动设置U型方向盘加热等级为3档时，对应的功率（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992953(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x4, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.High,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.High, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.High,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.High, DesPwr_sts=DesPwr.High_power)
        
        
    @allure.title("CCP#13=0x4_在normal和Convenience下，手动设置U型方向盘加热等级为2档时，对应的功率（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992954(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x4, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Mid,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Mid)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Mid, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Mid,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Mid, DesPwr_sts=DesPwr.Mid_power)
        
        
    @allure.title("CCP#13=0x4_在normal和Convenience下，手动设置U型方向盘加热等级为1档时，对应的功率（CCP#959=0x00）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992952(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x4, 0x959:0x0})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        
    @allure.title("CCP#13=0x4_在normal和Convenience下，手动设置O型方向盘加热等级为3档时，对应的功率（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992763(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x4, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.High,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.High, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.High,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.High, DesPwr_sts=DesPwr.High_power)
        
        
    @allure.title("CCP#13=0x4_在normal和Convenience下，手动设置O型方向盘加热等级为2档时，对应的功率（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992764(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x4, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Mid,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Mid)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Mid, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Mid,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Mid, DesPwr_sts=DesPwr.Mid_power)
        
        
    @allure.title("CCP#13=0x4_在normal和Convenience，手动设置U型方向盘加热等级为1档时，对应的功率（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.smoke
    @pytest.mark.a0917
    def test_caseid_1992955(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x4, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        
    @allure.title("CCP#13=0x4_在normal和Convenience，手动设置O型方向盘加热等级为1档时，对应的功率（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.smoke
    @pytest.mark.a0917
    def test_caseid_1992765(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x4, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
               




    @allure.title("CCP#13=0x3_在normal和Inactive下，远程设置U型方向盘加热等级为3档时，对应的功率（CCP#959=0x01）")  
    @pytest.mark.full
    @pytest.mark.a0917
    def test_caseid_1992902(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x3, 0x959:0x1})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.High)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.High, DesPwr_sts=DesPwr.High_power)
         
        
        
    @allure.title("CCP#13=0x3_在normal和Inactive下，远程设置U型方向盘加热等级为2档时，对应的功率（CCP#959=0x01）")  
    @pytest.mark.full
    @pytest.mark.a0917
    def test_caseid_1992903(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x3, 0x959:0x1})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Mid)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Mid)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Mid, DesPwr_sts=DesPwr.Mid_power)
        
        
    @allure.title("CCP#13=0x3_在normal和Inactive下，远程设置U型方向盘加热等级为1档时，对应的功率（CCP#959=0x01）")  
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992904(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x3, 0x959:0x1})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
    @allure.title("CCP#13=0x3_在normal和Inactive下，远程设置U型方向盘加热等级为1档时，对应的功率（CCP#959=0x00）")  
    @pytest.mark.full
    @pytest.mark.a0917
    def test_caseid_1992899(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x3, 0x959:0x0})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)



    @allure.title("CCP#13=0x3_在normal和Inactive下，远程设置O型方向盘加热等级为3档时，对应的功率（CCP#959=0x02）")  
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992712(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x3, 0x959:0x2})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.High)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.High, DesPwr_sts=DesPwr.High_power)
         
        
        
    @allure.title("CCP#13=0x3_在normal和Inactive下，远程设置O型方向盘加热等级为2档时，对应的功率（CCP#959=0x02）")  
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992713(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x3, 0x959:0x2})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Mid)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Mid)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Mid, DesPwr_sts=DesPwr.Mid_power)
        
        
    @allure.title("CCP#13=0x3_在normal和Inactive下，远程设置O型方向盘加热等级为1档时，对应的功率（CCP#959=0x02）")  
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992714(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x3, 0x959:0x2})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)


    @allure.title("CCP#13=0x3_在normal和Active下，手动设置U型方向盘加热等级为3档时，对应的功率（CCP#959=0x01））")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992965(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x3, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.High,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.High, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.High,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.High, DesPwr_sts=DesPwr.High_power)    #第二次跑到这  23个
        
        
        
        
        
        
    @allure.title("CCP#13=0x3_在normal和Active下，手动设置U型方向盘加热等级为2档时，对应的功率（CCP#959=0x01））")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992966(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x3, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Mid,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Mid)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Mid, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Mid,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Mid, DesPwr_sts=DesPwr.Mid_power)
        
        
    @allure.title("CCP#13=0x3_在normal和Active下，手动设置U型方向盘加热等级为1档时，对应的功率（CCP#959=0x01））")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992967(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x3, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
    @allure.title("CCP#13=0x3_在normal和Active下，手动设置U型方向盘加热等级为1档时，对应的功率（CCP#959=0x00））")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992964(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x3, 0x959:0x0})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        

    @allure.title("CCP#13=0x3_在normal和Active下，手动设置O型方向盘加热等级为3档时，对应的功率（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992775(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x3, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.High,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.High, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.High,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.High, DesPwr_sts=DesPwr.High_power)
        
        
    @allure.title("CCP#13=0x3_在normal和Active下，手动设置O型方向盘加热等级为2档时，对应的功率（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992776(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x3, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Mid,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Mid)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Mid, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Mid,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Mid, DesPwr_sts=DesPwr.Mid_power)
        
        
    @allure.title("CCP#13=0x3_在normal和Active下，手动设置O型方向盘加热等级为1档时，对应的功率（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992777(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x3, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)



    @allure.title("CCP#13=0x2_在Dyno和Convenience下，手动设置U型方向盘加热等级为3档时，对应的功率（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.full
    @pytest.mark.a0917
    def test_caseid_1992978(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x2, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.High,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.High, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.High,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.High, DesPwr_sts=DesPwr.High_power)
        
        
    @allure.title("CCP#13=0x2_在Dyno和Convenience下，手动设置U型方向盘加热等级为2档时，对应的功率（CCP#959=0x01）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.full
    @pytest.mark.a0917
    def test_caseid_1992979(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x2, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Mid,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Mid)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Mid, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Mid,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Mid, DesPwr_sts=DesPwr.Mid_power)
        
        
    @allure.title("CCP#13=0x2_在Dyno和Convenience下，手动设置U型方向盘加热等级为1档时，对应的功率（CCP#959=0x00）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.full
    @pytest.mark.a0917
    def test_caseid_1992977(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x2, 0x959:0x0})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        

    @allure.title("CCP#13=0x2_在Dyno和Convenience下，手动设置O型方向盘加热等级为3档时，对应的功率（CCP#959=0x02）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992788(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x2, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.High,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.High, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.High,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.High, DesPwr_sts=DesPwr.High_power)
        
        
    @allure.title("CCP#13=0x2_在Dyno和Convenience下，手动设置O型方向盘加热等级为2档时，对应的功率（CCP#959=0x02）")    ##单个pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992789(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x2, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Mid,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Mid)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Mid, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Mid,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Mid, DesPwr_sts=DesPwr.Mid_power)
        
        
    @allure.title("CCP#13=0x2_在Dyno和Convenience下，手动设置O型方向盘加热等级为1档时，对应的功率（CCP#959=0x02）")          ##单个pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992787(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x2, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        
        
    @allure.title("CCP#13=0x2_在Dyno和Convenience，手动设置U型方向盘加热等级为1档时，对应的功率（CCP#959=0x01）")            ##单个pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992980(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x2, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        
    @allure.title("CCP#13=0x2_在Dyno和Convenience，手动设置O型方向盘加热等级为1档时，对应的功率（CCP#959=0x02）")           ##单个pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a0917
    def test_caseid_1992990(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x2, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)   #第三次跑到这   14个
        
        
        
##################################### 1005 #########################################

    @allure.title("CCP#13=0x2_在Dyno和Convenience下，手动设置U型方向盘加热等级为OFF（CCP#959=0x01）")   #方向盘加热等级为OFF
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1005
    def test_caseid_1992976(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x2, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        
        
    @allure.title("CCP#13=0x3_在normal和Active下，手动设置U型方向盘加热等级为OFF（CCP#959=0x01）")   #方向盘加热等级为OFF
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1005
    def test_caseid_1992963(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, ccp={186: 0x02, 13: 0x3, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        
        
    @allure.title("CCP#13=0x4_在normal和Driving下，手动设置U型方向盘加热等级为OFF（CCP#959=0x01）")   #方向盘加热等级为OFF
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1005
    def test_caseid_1992938(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={186: 0x02, 13: 0x4, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        

    @allure.title("CCP#13=0x3_在normal和Inactive下，远程设置U型方向盘加热等级为OFF（CCP#959=0x01）")  
    @pytest.mark.sanity
    @pytest.mark.a1005
    def test_caseid_1992898(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x3, 0x959:0x1})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Off)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        
        
    @allure.title("CCP#13=0x4_在normal和Inactive下，远程设置U型方向盘加热等级为OFF（CCP#959=0x01）")  
    @pytest.mark.sanity
    @pytest.mark.a1005
    def test_caseid_1992872(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x1})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Off)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        


    @allure.title("CCP#13=0x2_在Dyno和Convenience下，手动设置O型方向盘加热等级为OFF（CCP#959=0x02）")   #方向盘加热等级为OFF
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1005
    def test_caseid_1992786(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x2, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        
        
    @allure.title("CCP#13=0x3_在normal和Active下，手动设置O型方向盘加热等级为OFF（CCP#959=0x02）")   #方向盘加热等级为OFF
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1005
    def test_caseid_1992773(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, ccp={186: 0x02, 13: 0x3, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        
        
    @allure.title("CCP#13=0x4_在normal和Driving下，手动设置O型方向盘加热等级为OFF（CCP#959=0x02）")   #方向盘加热等级为OFF
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1005
    def test_caseid_1992748(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={186: 0x02, 13: 0x4, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        

    @allure.title("CCP#13=0x3_在normal和Inactive下，远程设置O型方向盘加热等级为OFF（CCP#959=0x02）")  
    @pytest.mark.sanity
    @pytest.mark.a1005
    def test_caseid_1992708(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x3, 0x959:0x2})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Off)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        
        
    @allure.title("CCP#13=0x4_在normal和Inactive下，远程设置O型方向盘加热等级为OFF（CCP#959=0x02）")  
    @pytest.mark.sanity
    @pytest.mark.a1005
    def test_caseid_1992682(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x2})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Off)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        
        
        
    @allure.title("CCP#13=0x2_在Dyno和Convenience下，手动设置U型方向盘加热等级为OFF（CCP#959=0x01）")   ##SteerWhlHeatgOnReq==0x0
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.full
    @pytest.mark.a1005
    def test_caseid_1992973(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x2, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        
        
    @allure.title("CCP#13=0x3_在normal和Active，当SteerWhlHeatgOnReq==0x0 Off，U型方向盘停止加热")   ##SteerWhlHeatgOnReq==0x0
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1005
    def test_caseid_1992961(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, ccp={186: 0x02, 13: 0x3, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        
        
    @allure.title("CCP#13=0x4_在normal和Convenience，当SteerWhlHeatgOnReq==0x0 Off，U型方向盘停止加热")   ##SteerWhlHeatgOnReq==0x0
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1005
    def test_caseid_1992948(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x4, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        
        
        
    @allure.title("CCP#13=0x4 _在normal和Driving，当SteerWhlHeatgOnReq==0x0 Off，U型方向盘停止加热")   ##SteerWhlHeatgOnReq==0x0
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1005
    def test_caseid_1992936(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={186: 0x02, 13: 0x4, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        
        
    @allure.title("CCP#13=0x3_在normal和Inactive，当SteerWhlHeatgOnReq==0x0 Off，U型方向盘停止加热")   ##SteerWhlHeatgOnReq==0x0
    @pytest.mark.full
    @pytest.mark.a0917
    def test_caseid_1992897(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x3, 0x959:0x1})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Off)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        
        
        
    @allure.title("CCP#13=0x4 _在normal和Active，当SteerWhlHeatgOnReq==0x0 Off，U型方向盘停止加热")   ##SteerWhlHeatgOnReq==0x0
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1005
    def test_caseid_1992871(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        
        
        
        
    @allure.title("CCP#13=0x2_在Dyno和Convenience，当SteerWhlHeatgOnReq==0x0 Off，O型方向盘停止加热")   ##SteerWhlHeatgOnReq==0x0
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1005
    def test_caseid_1992783(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x2, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        
        
    @allure.title("CCP#13=0x3_在normal和Active，当SteerWhlHeatgOnReq==0x0 Off，O型方向盘停止加热")   ##SteerWhlHeatgOnReq==0x0
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1005
    def test_caseid_1992771(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, ccp={186: 0x02, 13: 0x3, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        
        
    @allure.title("CCP#13=0x4_在normal和Convenience，当SteerWhlHeatgOnReq==0x0 Off，O型方向盘停止加热")   ##SteerWhlHeatgOnReq==0x0
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1005
    def test_caseid_1992758(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x4, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        
        
        
    @allure.title("CCP#13=0x4 _在normal和Driving，当SteerWhlHeatgOnReq==0x0 Off，O型方向盘停止加热")   ##SteerWhlHeatgOnReq==0x0
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1005
    def test_caseid_1992746(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={186: 0x02, 13: 0x4, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        
        
    @allure.title("CCP#13=0x3_在normal和Inactive，当SteerWhlHeatgOnReq==0x0 Off，O型方向盘停止加热")   ##SteerWhlHeatgOnReq==0x0
    @pytest.mark.sanity
    @pytest.mark.a1005
    def test_caseid_1992707(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x3, 0x959:0x2})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Off)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)
        
        
        
    @allure.title("CCP#13=0x4 _在normal和Active，当SteerWhlHeatgOnReq==0x0 Off，O型方向盘停止加热")   ##SteerWhlHeatgOnReq==0x0
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1005
    def test_caseid_1992681(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Off, DesPwr_sts=DesPwr.Off_power)     #######已上传1008
   
# # ###################### 1006 ########################     
    @allure.title("CCP#13=0x4_在normal和Inactive下，远程设置U型方向盘加热等级为1档时，对应的功率（CCP#959=0x00）")   #对应的功率 
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992873(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x0})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        
    @allure.title("CCP#13=0x3_在normal和Inactive下，远程设置O型方向盘加热等级为1档时，对应的功率（CCP#959=0x00）")   #对应的功率 
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992709(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x3, 0x959:0x0})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        
    @allure.title("CCP#13=0x2_在Dyno和Convenience，手动设置O型方向盘加热等级为1档时，对应的功率（CCP#959=0x02")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992790(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x2, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        
    @allure.title("CCP#13=0x3_在normal和Active下，手动设置O型方向盘加热等级为1档时，对应的功率（CCP#959=0x00）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992774(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, ccp={186: 0x02, 13: 0x3, 0x959:0x0})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        
    @allure.title("CCP#13=0x4_在normal和Convenience下，手动设置O型方向盘加热等级为1档时，对应的功率（CCP#959=0x00）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992762(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x4, 0x959:0x0})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        
        
    @allure.title("CCP#13=0x4_Calibratable parameters_U型方向盘")
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992851(self):      
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={ 13: 0x4, 186: 0x02, 0x959:0x1})
        self.sd_tester.security_access_level(UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x22, 0x70, 0X23])
        self.sd_tester.send_request_and_recv_response([0x2E, 0x70, 0X23 ,0x01, 0x2C, 0X01, 0X2C,0X05,0X05,0X20,0X26,0X28],recv=[0x6E,0x70,0x23])
        sleep(1)
        self.sd_tester.send_request_and_recv_response([0x22, 0x70, 0X23],recv=[0x62, 0x70, 0X23 ,0x01, 0x2C, 0X01, 0X2C,0X05,0X05,0X20,0X26,0X28])
        
        
    @allure.title(" CCP#13=0x4_Normal&&Convenience_通过诊断开启U型方向盘加热")
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992849(self):      
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={ 13: 0x4, 186: 0x02, 0x959:0x1})
        self.sd_tester.security_access_level(UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x71])
        sleep(1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x02],recv=[0x71])
        sleep(1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Mid)
        
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x03],recv=[0x71])
        sleep(1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
        
        
    @allure.title("CCP#13=0x4_Dyno&&Convenience_通过诊断开启U型方向盘加热")
    @pytest.mark.full
    @pytest.mark.a1006
    def test_caseid_1992848(self):      
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={ 13: 0x4, 186: 0x02, 0x959:0x1})
        self.sd_tester.security_access_level(UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x71])
        sleep(1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x02],recv=[0x71])
        sleep(1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Mid)
        
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x03],recv=[0x71])
        sleep(1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
        
        
    @allure.title("CCP#13=0x4_Normal&&Driving_通过诊断开启U型方向盘加热")
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992847(self):      
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={ 13: 0x4, 186: 0x02, 0x959:0x1})
        self.sd_tester.security_access_level(UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x71])
        sleep(1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x02],recv=[0x71])
        sleep(1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Mid)
        
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x03],recv=[0x71])
        sleep(1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
        
        
    @allure.title("CCP#13=0x4_Normal&&Inactive_通过诊断开启U型方向盘加热")
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992845(self):      
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={ 13: 0x4, 186: 0x02, 0x959:0x1})
        self.sd_tester.security_access_level(UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x71])
        sleep(1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x02],recv=[0x71])
        sleep(1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Mid)
        
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x03],recv=[0x71])
        sleep(1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
        

        
    @allure.title("配置CCP#186=0x2，电车有O型方向盘加热功能")
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992734(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4, 0x959:0x2}) 
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)


    @allure.title("CCP#13=0x4_Calibratable parameters_O型方向盘")
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992661(self):      
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={ 13: 0x4, 186: 0x02, 0x959:0x2})
        self.sd_tester.security_access_level(UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x22, 0x70, 0X23])
        self.sd_tester.send_request_and_recv_response([0x2E, 0x70, 0X23 ,0x01, 0x2C, 0X01, 0X2C,0X05,0X05,0X20,0X26,0X28],recv=[0x6E,0x70,0x23])
        sleep(1)
        self.sd_tester.send_request_and_recv_response([0x22, 0x70, 0X23],recv=[0x62, 0x70, 0X23 ,0x01, 0x2C, 0X01, 0X2C,0X05,0X05,0X20,0X26,0X28])
        
        
    @allure.title("CCP#13=0x4_Normal&&Convenience_通过诊断开启O型方向盘加热")
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992659(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
        self.sd_tester.write_ccp(ccp={13: 0x4, 186: 0x02, 0x959:0x2}) 
        self.sd_tester.security_access_level(UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20, 0X0C, 0X01],recv=[0x71, 0x01, 0X20, 0X0C])
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20, 0X0C, 0X02],recv=[0x71, 0x01, 0X20, 0X0C])
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Mid)
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20, 0X0C, 0X03],recv=[0x71, 0x01, 0X20, 0X0C])
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
        
        
    @allure.title("CCP#13=0x4_Dyno&&Convenience_通过诊断开启O型方向盘加热")
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992658(self):      
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE, ccp={ 13: 0x4, 186: 0x02, 0x959:0x2})
        self.sd_tester.security_access_level(UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x71])
        sleep(1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x02],recv=[0x71])
        sleep(1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Mid)
        
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x03],recv=[0x71])
        sleep(1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
        
        
        
    @allure.title("CCP#13=0x4_Normal&&Driving_通过诊断开启O型方向盘加热")
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992657(self):      
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={ 13: 0x4, 186: 0x02, 0x959:0x2})
        self.sd_tester.security_access_level(UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x71])
        sleep(1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x02],recv=[0x71])
        sleep(1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Mid)
        
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x03],recv=[0x71])
        sleep(1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
        
        
    @allure.title("CCP#13=0x4_Normal&&Inactive_通过诊断开启O型方向盘加热")
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992655(self):      
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={ 13: 0x4, 186: 0x02, 0x959:0x2})
        self.sd_tester.security_access_level(UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x71])
        sleep(1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x02],recv=[0x71])
        sleep(1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Mid)
        
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x03],recv=[0x71])
        sleep(1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
 
 
    @allure.title("U型方向盘_状态切换：ON state_OFF state_远程加热（CCP#13=0x4）")  
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992822(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x1})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Off)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)


    @allure.title("O型方向盘_状态切换：ON state_OFF state_远程加热（CCP#13=0x4）")  
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992633(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x2})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Off)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)


    @allure.title("U型方向盘_OFF state_唤醒时_本地加热（CCP#13=0x4）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992831(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x4, 0x959:0x1})
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)



    @allure.title("U型方向盘_ON state_接收到On command命令_本地加热（CCP#13=0x4）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992830(self):  
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)


    @allure.title("U型方向盘_OFF state_唤醒时_远程加热（CCP#13=0x4）")  
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992825(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x1})

        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)


    @allure.title("U型方向盘_ON state_接收到On command命令_远程加热（CCP#13=0x4）")  
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992824(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x1})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)



    @allure.title("O型方向盘_OFF state_唤醒时_本地加热（CCP#13=0x4）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992642(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x4, 0x959:0x2})
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        

    @allure.title("O型方向盘_ON state_接收到On command命令_本地加热（CCP#13=0x4）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992641(self):  
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        
        
    @allure.title("O型方向盘_状态切换：ON state_OFF state_本地加热（CCP#13=0x4）")
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992639(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x4, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(lev_sts=HeatLevel.Off, avl_sts=AvlSts.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        
        
    @allure.title("O型方向盘_OFF state_唤醒时_远程加热（CCP#13=0x4）")  
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992636(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x2})

        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        

    @allure.title("O型方向盘_ON state_接收到On command命令_远程加热（CCP#13=0x4）")  
    @pytest.mark.sanity
    @pytest.mark.a1006
    def test_caseid_1992635(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x2})
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        
        
##################################### 待调试
    @allure.title("CCP#13=0x4_在normal和Convenience，当usage mode=Abandoned，U型方向盘停止加热")
    # @pytest.mark.smoke
    @pytest.mark.a991
    def test_caseid_1992950(self):
        self.sd_tester.send_request_and_recv_response([0x10, 0x03],recv=[0x50])
        self.sd_tester.security_access_level(UnLock.L5)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4, 0x959:0x1}) 
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)

        self.sd_tester.send_request_and_recv_response([0x2F, 0xDD, 0X0A ,0x03, 0x00],recv=[0x6F])
        sleep(.2)        
        # self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
    
    
        
        
    # @allure.title("CCP#13=0x4_远程设置U型方向盘远程加热等级为3档时，切换usage mode=Convinience，对应的功率（CCP#959=0x01）")  #加热档位不对
    # # @pytest.mark.smoke
    # @pytest.mark.a99
    # def test_caseid_1992888(self):
    #     self.sd_tester.send_request_and_recv_response([0x10, 0x03],recv=[0x50])
    #     self.sd_tester.security_access_level(UnLock.L5)
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
    #     self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4, 0x959:0x2}) 
    #     self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.High)
    #     self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
    #     self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.High, DesPwr_sts=DesPwr.High_power)
    #     # self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)


    #     self.sd_tester.send_request_and_recv_response([0x2F, 0xDD, 0X0A ,0x03, 0x02],recv=[0x6F])
    #     sleep(.2)
    #     self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.High)
    #     self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.High, DesPwr_sts=DesPwr.High_power)
        
        
        
    # @allure.title("CCP#13=0x4_在normal和INACTIVE，远程设置O型方向盘加热等级为1档时，对应的功率（CCP#959=0x02）")  
    # # @pytest.mark.smoke
    # @pytest.mark.a99
    # def test_caseid_1992701(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
    #     self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4, 0x959:0x2}) 
    #     self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
    #     self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
    #     self.bus_comm.check_steerwheel_DesPower_req(lev_sts=HeatLevel.Low, DesPwr_sts=DesPwr.Low_power)
        
        
        
        
    @allure.title("反例_CCP#13=0x04_在nomal和abandone，调节电车U型方向盘不成功_车速超过5km/h（CCP#959=0x01）")  #暂时不上传
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1112
    def test_caseid_1992791(self):   
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, veh_spd=0x9ff, ccp={0x959:0x1})
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Up, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Up, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Down, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Down, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Forward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Forward, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
        
        self.soa.hmi_set_steer_wheel_adjust_direction(direct=AdjustDirection.Backward, time_wait=.1)
        self.bus_comm.check_steerwheel_direct_req(direct=AdjustDirection.Backward, sts=False)
        self.bus_comm.check_steerwheel_DisAdjMov_req(disAdjMov_req=DisAdjMov.Inhb)
    


        
    @allure.title("反例_car mode=Factory，不支持U型方向盘加热（CCP#959=0x01）")  #不支持
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a10051
    def test_caseid_1992933(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x4, 0x959:0x1}, veh_spd=5)
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)

        
        
    @allure.title("反例_car mode=Transport，不支持U型方向盘加热（CCP#959=0x01）")  #不支持
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a10051
    def test_caseid_1992932(self):
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x4, 0x959:0x1}, veh_spd=5)
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
 
        
        
    @allure.title("反例_usage mode=Abandoned，不支持U型方向盘加热（CCP#959=0x01）")  #不支持
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a10051
    def test_caseid_1992929(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED, ccp={186: 0x02, 13: 0x4, 0x959:0x1}, veh_spd=5)
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
      
        
    @allure.title("反例_car mode=Factory，不支持U型远程方向盘加热（CCP#959=0x01）")  #不支持
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a10051
    def test_caseid_1992865(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.ABANDONED, ccp={186: 0x02, 13: 0x4, 0x959:0x1}, veh_spd=5)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        
        
    @allure.title("反例_usage mode=Convenience，不支持U型远程方向盘加热（CCP#959=0x01）")  
    @pytest.mark.sanity
    @pytest.mark.a10051
    def test_caseid_1992862(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x4, 0x959:0x1}, veh_spd=5)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)

        

    @allure.title("反例_usage mode=Convenience，不支持U型远程方向盘加热（CCP#959=0x01）")  
    @pytest.mark.sanity
    @pytest.mark.a10051
    def test_caseid_1992860(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.ACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x1}, veh_spd=5)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)

        
        
    @allure.title("反例_car mode=Factory，不支持O型方向盘加热（CCP#959=0x02）")  #不支持
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a10051
    def test_caseid_1992743(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x4, 0x959:0x2}, veh_spd=5)
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)

        
        
    @allure.title("反例_car mode=Transport，不支持O型方向盘加热（CCP#959=0x02）")  #不支持
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a10051
    def test_caseid_1992742(self):
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x4, 0x959:0x2}, veh_spd=5)
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)

        
        
    @allure.title("反例_usage mode=Abandoned，不支持O型方向盘加热（CCP#959=0x02）")  #不支持
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a10051
    def test_caseid_1992739(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED, ccp={186: 0x02, 13: 0x4, 0x959:0x2}, veh_spd=5)
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
       
        
    @allure.title("反例_car mode=Transport，不支持O型方向盘加热（CCP#959=0x02）")  #不支持
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a10051
    def test_caseid_1992738(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, ccp={186: 0x02, 13: 0x3, 0x959:0x2}, veh_spd=5)
        self.bus_comm.set_Hv_sys_relay_sts(HvSysRelaySts.Open)
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        
        
    @allure.title("反例_car mode=Factory，不支持O型远程方向盘加热（CCP#959=0x02）")  #不支持
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a10051
    def test_caseid_1992675(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.ABANDONED, ccp={186: 0x02, 13: 0x4, 0x959:0x2}, veh_spd=5)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        
        
    @allure.title("反例_car mode=Transport，不支持O型远程方向盘加热（CCP#959=0x02）")  #不支持
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a10051
    def test_caseid_1992674(self):
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.ABANDONED, ccp={186: 0x02, 13: 0x4, 0x959:0x2}, veh_spd=5)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        
        
    @allure.title("反例_usage mode=Convenience，不支持O型远程方向盘加热（CCP#959=0x02）")  
    @pytest.mark.sanity
    @pytest.mark.a10051
    def test_caseid_1992672(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x4, 0x959:0x2}, veh_spd=5)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        
        
    @allure.title("反例_usage mode=Active，不支持O型远程方向盘加热（CCP#959=0x02）")  
    @pytest.mark.sanity
    @pytest.mark.a10051
    def test_caseid_1992670(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.ACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x2}, veh_spd=5)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        
        
    @allure.title("反例_HvSysRlyStsHvSysRlySts不满足，不支持O型远程方向盘加热（CCP#959=0x02）")  
    @pytest.mark.sanity
    @pytest.mark.a10051
    def test_caseid_1992669(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x2}, veh_spd=5)
        self.bus_comm.set_Hv_sys_relay_sts(HvSysRelaySts.Open)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)

        
        
    @allure.title("反例_car mode=Crash，不支持U型方向盘加热（CCP#959=0x00）")  #不支持
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.full
    @pytest.mark.a10051
    def test_caseid_1992931(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x2, 0x959:0x0}, veh_spd=5)
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)

        
        
    @allure.title("反例_usage mode=inactive，不支持U型方向盘加热（CCP#959=0x01）")  #不支持
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.full
    @pytest.mark.a10051
    def test_caseid_1992930(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x1}, veh_spd=5)
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
      
        
    @allure.title("反例_usage mode=inactive，不支持U型方向盘加热（CCP#959=0x01）")  #不支持
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.full
    @pytest.mark.a10051
    def test_caseid_1992928(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE, ccp={186: 0x02, 13: 0x3, 0x959:0x1}, veh_spd=5)
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        
        
    @allure.title("反例_car mode=Transport，不支持U型远程方向盘加热（CCP#959=0x01）")  
    @pytest.mark.full
    @pytest.mark.a10051
    def test_caseid_1992864(self):
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x1}, veh_spd=5)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        
        
    @allure.title("反例_car mode=Transport，不支持U型远程方向盘加热（CCP#959=0x01）")  
    @pytest.mark.full
    @pytest.mark.a10051
    def test_caseid_1992863(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x2, 0x959:0x0}, veh_spd=5)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        
        
    @allure.title("反例_car mode=Transport，不支持U型远程方向盘加热（CCP#959=0x01）")  
    @pytest.mark.full
    @pytest.mark.a10051
    def test_caseid_1992861(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={186: 0x02, 13: 0x4, 0x959:0x1}, veh_spd=5)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        
        
    @allure.title("反例_HvSysRlyStsHvSysRlySts不满足，不支持U型远程方向盘加热（CCP#959=0x01）")  
    @pytest.mark.full
    @pytest.mark.a10051
    def test_caseid_1992859(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x3, 0x959:0x1}, veh_spd=5)
        self.bus_comm.set_Hv_sys_relay_sts(HvSysRelaySts.Open)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        
        
    @allure.title("反例_car mode=Crash，不支持O型方向盘加热（CCP#959=0x00）")  #不支持
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.full
    @pytest.mark.a10051
    def test_caseid_1992741(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x2, 0x959:0x0}, veh_spd=5)
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        
        
    @allure.title(" 反例_usage mode=inactive，不支持O型方向盘加热（CCP#959=0x02）")  #不支持
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.full
    @pytest.mark.a10051
    def test_caseid_1992740(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x4, 0x959:0x2}, veh_spd=5)
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)       
        
    @allure.title("反例_car mode=Crash，不支持O型远程方向盘加热（CCP#959=0x00）")  
    @pytest.mark.full
    @pytest.mark.a10051
    def test_caseid_1992673(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.INACTIVE, ccp={186: 0x02, 13: 0x2, 0x959:0x0}, veh_spd=5)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        
        
    @allure.title(" 反例_usage mode=Driving，不支持O型远程方向盘加热（CCP#959=0x02）")  
    @pytest.mark.full
    @pytest.mark.a10051
    def test_caseid_1992671(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING, ccp={186: 0x02, 13: 0x4, 0x959:0x2}, veh_spd=5)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        sleep(1)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
    
        
    # @allure.title("反例_CCP#13=0x4_car mode mode不满足，通过诊断方式的O型方向盘加热不能开启")
    # @pytest.mark.sanity
    # @pytest.mark.a1006
    # def test_caseid_1992654(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.INACTIVE)
    #     self.sd_tester.write_ccp(ccp={13: 0x4, 186: 0x02, 0x959:0x1}) 
    #     self.sd_tester.security_access_level(UnLock.L5)
    #     self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20, 0X0C, 0X01],recv=[0x7F, 0x31, 0X22])
    #     self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        
        
    # @allure.title("反例_CCP#13=0x4_Transport&&Convenience_通过诊断开启O型方向盘加热")
    # @pytest.mark.sanity
    # @pytest.mark.a1006
    # def test_caseid_1992653(self):      
    #     self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.CONVENIENCE, ccp={ 13: 0x4, 186: 0x02, 0x959:0x2})
    #     self.sd_tester.security_access_level(UnLock.L5)
    #     self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x7F, 0x31, 0x22])
    #     sleep(1)
    #     self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        
        
        
    # @allure.title("反例_CCP#13=0x4_Crash&&Convenience_通过诊断开启O型方向盘加热")
    # @pytest.mark.full
    # @pytest.mark.a1006
    # def test_caseid_1992652(self):      
    #     self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.CONVENIENCE, ccp={ 13: 0x4, 186: 0x02, 0x959:0x2})
    #     self.sd_tester.security_access_level(UnLock.L5)
    #     self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x7F, 0x31, 0x22])
    #     sleep(1)
    #     self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        
        
    # @allure.title("CCP#13=0x4_温度补偿写入成功_O型方向盘")
    # @pytest.mark.sanity
    # @pytest.mark.a1006
    # def test_caseid_1992651(self):      
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={ 13: 0x4, 186: 0x02, 0x959:0x2})
    #     self.sd_tester.security_access_level(UnLock.L5)
    #     self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X09])
    #     self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0X09 ,0x01],recv=[0x6E,0x41,0x09])
    #     sleep(2)
    #     self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X09],recv=[0x62, 0x41, 0X09 ,0x01])
    #     self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0X09 ,0x09],recv=[0x6E,0x41,0x09])
    #     sleep(2)
    #     self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X09],recv=[0x62, 0x41, 0X09 ,0x09])
    #     self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0X09 ,0x0F],recv=[0x6E,0x41,0x09])
    #     sleep(2)
    #     self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X09],recv=[0x62, 0x41, 0X09 ,0x0F])
    #     self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0X09 ,0x08],recv=[0x6E,0x41,0x09])
    #     sleep(2)
    #     self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X09],recv=[0x62, 0x41, 0X09 ,0x08])
        
        
    # @allure.title("CCP#13=0x4_温度补偿写入失败_O型方向盘")
    # @pytest.mark.sanity
    # @pytest.mark.a1006
    # def test_caseid_1992650(self):      
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={ 13: 0x4, 186: 0x02, 0x959:0x1})
    #     self.sd_tester.security_access_level(UnLock.L5)
    #     self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X09])
    #     self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0X09 ,0x10],recv=[0x6E,0x41,0x09])
    #     sleep(1)
    #     self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X09],recv=[0x62, 0x41, 0X09 ,0x10])
        
        
        
        
    # @allure.title("反例_CCP#13=0x4_car mode mode不满足，通过诊断方式的U型方向盘加热不能开启")
    # @pytest.mark.sanity
    # @pytest.mark.a1006
    # def test_caseid_1992844(self):      
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, ccp={ 13: 0x4, 186: 0x02, 0x959:0x1})
    #     self.sd_tester.security_access_level(UnLock.L5)
    #     self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x7F, 0x31, 0x22])
    #     sleep(1)
    #     self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        
        
    # @allure.title("反例_CCP#13=0x4_Transport&&Convenience_通过诊断开启U型方向盘加热")
    # @pytest.mark.sanity
    # @pytest.mark.a1006
    # def test_caseid_1992843(self):      
    #     self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT, usage_mode=UsageMode.CONVENIENCE, ccp={ 13: 0x4, 186: 0x02, 0x959:0x1})
    #     self.sd_tester.security_access_level(UnLock.L5)
    #     self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x7F, 0x31, 0x22])
    #     sleep(1)
    #     self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        
        
        
    # @allure.title("反例_CCP#13=0x4_Crash&&Convenience_通过诊断开启U型方向盘加热")
    # @pytest.mark.full
    # @pytest.mark.a1006
    # def test_caseid_1992842(self):      
    #     self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.CONVENIENCE, ccp={ 13: 0x4, 186: 0x02, 0x959:0x1})
    #     self.sd_tester.security_access_level(UnLock.L5)
    #     self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0X20 ,0x0C, 0x01],recv=[0x7F, 0x31, 0x22])
    #     sleep(1)
    #     self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        
        
    # @allure.title("CCP#13=0x4_温度补偿写入成功_U型方向盘")
    # @pytest.mark.sanity
    # @pytest.mark.a1006
    # def test_caseid_1992841(self):      
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={ 13: 0x4, 186: 0x02, 0x959:0x1})
    #     self.sd_tester.security_access_level(UnLock.L5)
    #     self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X09])
    #     self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0X09 ,0x01],recv=[0x6E,0x41,0x09])
    #     sleep(1)
    #     self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X09],recv=[0x62, 0x41, 0X09 ,0x01])
        
    #     sleep(1)        
    #     self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0X09 ,0x09],recv=[0x6E,0x41,0x09])
    #     sleep(1)
    #     self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X09],recv=[0x62, 0x41, 0X09 ,0x09])
    #     sleep(1) 
        
    #     self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0X09 ,0x0F],recv=[0x6E,0x41,0x09])
    #     sleep(1)
    #     self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X09],recv=[0x62, 0x41, 0X09 ,0x0F])
    #     sleep(1) 
        
    #     self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0X09 ,0x08],recv=[0x6E,0x41,0x09])
    #     sleep(1)
    #     self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X09],recv=[0x62, 0x41, 0X09 ,0x08])
        
    # @allure.title(" CCP#13=0x4_温度补偿写入失败_U型方向盘")
    # @pytest.mark.sanity
    # @pytest.mark.a1006
    # def test_caseid_1992840(self):      
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={ 13: 0x4, 186: 0x02, 0x959:0x1})
    #     self.sd_tester.security_access_level(UnLock.L5)
    #     self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X09])
    #     self.sd_tester.send_request_and_recv_response([0x2E, 0x41, 0X09 ,0x10],recv=[0x7F,0x2E,0x31])
    #     # sleep(1)
    #     # self.sd_tester.send_request_and_recv_response([0x22, 0x41, 0X09],recv=[0x62, 0x41, 0X09 ,0x10])
   
################## 1107
    
    @allure.title("CCP#13=0x4_在normal和Convenience，当usage mode=Abandoned，U型方向盘停止加热")
    @pytest.mark.smoke
    @pytest.mark.a1107
    def test_caseid_1992950(self):
        self.sd_tester.send_request_and_recv_response([0x10, 0x03],recv=[0x50])
        self.sd_tester.security_access_level(UnLock.L5)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
        # self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        # # self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.CONVENIENCE)
        # self.soa.send_method_request( 'VehicleModeService_client', "SetUsageModeUp",{"mode": 2})
        sleep(2)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4, 0x959:0x1}) 
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)

        # self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ABANDONED)
        # self.soa.send_method_request( 'VehicleModeService_client', "SetUsageModeUp",{"mode": 0})
        self.sd_tester.send_request_and_recv_response([0x2F, 0xDD, 0X0A ,0x03, 0x00],recv=[0x6F])
        # self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
        sleep(.2)        
        # self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)    
               
    
    @allure.title("CCP#13=0x2_在Dyno和Convenience，当usage mode=Inactive，U型方向盘停止加热")
    @pytest.mark.full
    @pytest.mark.a1107
    def test_caseid_1992974(self):
        self.sd_tester.send_request_and_recv_response([0x10, 0x03],recv=[0x50])
        self.sd_tester.security_access_level(UnLock.L5)
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE)

        sleep(2)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x2, 0x959:0x1}) 
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)


        self.sd_tester.send_request_and_recv_response([0x2F, 0xDD, 0X0A ,0x03, 0x01],recv=[0x6F])

        sleep(.2)        

        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)    
        
        
    
    @allure.title("CCP#13=0x3_在normal和Active，当usage mode=Inactive，U型方向盘停止加热")
    @pytest.mark.sanity
    @pytest.mark.a1107
    def test_caseid_1992962(self):
        self.sd_tester.send_request_and_recv_response([0x10, 0x03],recv=[0x50])
        self.sd_tester.security_access_level(UnLock.L5)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)

        sleep(2)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x3, 0x959:0x1}) 
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)


        self.sd_tester.send_request_and_recv_response([0x2F, 0xDD, 0X0A ,0x03, 0x01],recv=[0x6F])

        sleep(.2)        

        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)    
        
        
    
    @allure.title("CCP#13=0x4_在normal和Convenience，当usage mode=Inactive，U型方向盘停止加热")
    @pytest.mark.sanity
    @pytest.mark.a1107
    def test_caseid_1992949(self):
        self.sd_tester.send_request_and_recv_response([0x10, 0x03],recv=[0x50])
        self.sd_tester.security_access_level(UnLock.L5)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)

        sleep(2)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4, 0x959:0x1}) 
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)

        self.sd_tester.send_request_and_recv_response([0x2F, 0xDD, 0X0A ,0x03, 0x01],recv=[0x6F])
        sleep(.2)        

        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)    
        
        
    
    @allure.title("CCP#13=0x4 _在normal和Driving，当usage mode=Inactive，U型方向盘停止加热")
    @pytest.mark.sanity
    @pytest.mark.a1107
    def test_caseid_1992937(self):
        self.sd_tester.send_request_and_recv_response([0x10, 0x03],recv=[0x50])
        self.sd_tester.security_access_level(UnLock.L5)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)

        sleep(2)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4, 0x959:0x1}) 
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)

        self.sd_tester.send_request_and_recv_response([0x2F, 0xDD, 0X0A ,0x03, 0x01],recv=[0x6F])
        sleep(.2)        

        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)    
        
        
    
    @allure.title("CCP#13=0x2_在Dyno和Convenience，当usage mode=Abandoned，O型方向盘停止加热")
    @pytest.mark.sanity
    @pytest.mark.a1107
    def test_caseid_1992785(self):
        self.sd_tester.send_request_and_recv_response([0x10, 0x03],recv=[0x50])
        self.sd_tester.security_access_level(UnLock.L5)
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE)

        sleep(2)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x2, 0x959:0x2}) 
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)

        self.sd_tester.send_request_and_recv_response([0x2F, 0xDD, 0X0A ,0x03, 0x00],recv=[0x6F])
        sleep(.2)        

        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)    
        
        
    
    @allure.title("CCP#13=0x2_在Dyno和Convenience，当usage mode=Inactive，O型方向盘停止加热")
    @pytest.mark.sanity
    @pytest.mark.a1107
    def test_caseid_1992784(self):
        self.sd_tester.send_request_and_recv_response([0x10, 0x03],recv=[0x50])
        self.sd_tester.security_access_level(UnLock.L5)
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE)

        sleep(2)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x2, 0x959:0x2}) 
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)

        self.sd_tester.send_request_and_recv_response([0x2F, 0xDD, 0X0A ,0x03, 0x01],recv=[0x6F])
        sleep(.2)        

        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)    
        
        
    
    @allure.title("CCP#13=0x3_在normal和Active，当usage mode=Inactive，O型方向盘停止加热")
    @pytest.mark.sanity
    @pytest.mark.a1107
    def test_caseid_1992772(self):
        self.sd_tester.send_request_and_recv_response([0x10, 0x03],recv=[0x50])
        self.sd_tester.security_access_level(UnLock.L5)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)

        sleep(2)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x3, 0x959:0x2}) 
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)

        self.sd_tester.send_request_and_recv_response([0x2F, 0xDD, 0X0A ,0x03, 0x01],recv=[0x6F])
        sleep(.2)        

        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off) 
        
        
    
    @allure.title("CCP#13=0x4_在normal和Convenience，当usage mode=Abandoned，O型方向盘停止加热")
    @pytest.mark.sanity
    @pytest.mark.a1107
    def test_caseid_1992760(self):
        self.sd_tester.send_request_and_recv_response([0x10, 0x03],recv=[0x50])
        self.sd_tester.security_access_level(UnLock.L5)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)

        sleep(2)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4, 0x959:0x2}) 
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)

        self.sd_tester.send_request_and_recv_response([0x2F, 0xDD, 0X0A ,0x03, 0x00],recv=[0x6F])
        sleep(.2)        

        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off) 
        
        
    
    @allure.title("CCP#13=0x4_在normal和Convenience，当usage mode=Inactive，O型方向盘停止加热")
    @pytest.mark.sanity
    @pytest.mark.a1107
    def test_caseid_1992759(self):
        self.sd_tester.send_request_and_recv_response([0x10, 0x03],recv=[0x50])
        self.sd_tester.security_access_level(UnLock.L5)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)

        sleep(2)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4, 0x959:0x2}) 
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)

        self.sd_tester.send_request_and_recv_response([0x2F, 0xDD, 0X0A ,0x03, 0x01],recv=[0x6F])
        sleep(.2)        

        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off) 
        
        
    
    @allure.title("CCP#13=0x4 _在normal和Driving，当usage mode=Inactive，O型方向盘停止加热")
    @pytest.mark.sanity
    @pytest.mark.a1107
    def test_caseid_1992747(self):
        self.sd_tester.send_request_and_recv_response([0x10, 0x03],recv=[0x50])
        self.sd_tester.security_access_level(UnLock.L5)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)

        sleep(2)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4, 0x959:0x2}) 
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)

        self.sd_tester.send_request_and_recv_response([0x2F, 0xDD, 0X0A ,0x03, 0x01],recv=[0x6F])
        sleep(.2)        

        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off) 
        
          
    @allure.title("U型方向盘_AvlSts=0x2_方向盘不处于加热状态(CCP#13=0x4)")
    @pytest.mark.sanity
    @pytest.mark.a1107
    def test_caseid_1992921(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={13: 0x4, 186: 0x02, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
       
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)      
        
        
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)  
        
        
    @allure.title("O型方向盘_AvlSts=0x2_方向盘不处于加热状态(CCP#13=0x4)")
    @pytest.mark.sanity
    @pytest.mark.a1107
    def test_caseid_1992731(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={13: 0x4, 186: 0x02, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
       
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)      
        
        
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)  
        
        
    @allure.title("O型方向盘_AvlSts=0x1_方向盘处于加热状态(CCP#13=0x4)")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    )
    @pytest.mark.sanity
    @pytest.mark.a1107
    def test_caseid_1992732(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
        self.sd_tester.write_ccp(ccp={13: 0x4, 186: 0x02, 0x959:0x2}) 
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
        
############## 1111

########################### 1108
    @allure.title("O型方向盘_AvlSts=0x1_方向盘处于加热状态(CCP#13=0x4)")
    @pytest.mark.sanity
    @pytest.mark.a1111
    def test_caseid_1992732(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={13: 0x4, 186: 0x02, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
       
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)       
        
        
    @allure.title("U型方向盘_AvlSts=0x1_方向盘处于加热状态(CCP#13=0x4)")
    @pytest.mark.sanity
    @pytest.mark.a1111
    def test_caseid_1992922(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={13: 0x4, 186: 0x02, 0x959:0x1})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
       
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)   

        
    @allure.title("O型方向盘_AvlSts=0x2_方向盘不处于加热状态(CCP#13=0x4)")
    @pytest.mark.sanity
    @pytest.mark.a1111
    def test_caseid_1992731(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={13: 0x4, 186: 0x02, 0x959:0x2})
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
       
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)      
        
        
        self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
        self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)  

 
    # @allure.title("U型方向盘_AvlSts=0x1_方向盘处于加热状态(CCP#13=0x4)")   ##########处理1111
    # @pytest.mark.sanity
    # # @pytest.mark.a99
    # def test_caseid_199100(self):
        
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={ 13: 0x4, 186: 0x02, 0x959:0x1})
    #     self.mix.set_dtc_precontion()
    #     self.sd_tester.security_access_level(UnLock.L5)
    #     self.sd_tester.send_request_and_recv_response([0x22, 0x70, 0X23])
    #     self.sd_tester.send_request_and_recv_response([0x2E, 0x70, 0X23 ,0x00, 0x05, 0X00, 0X05,0X05,0X05,0X20,0X26,0X28],recv=[0x6E,0x70,0x23])
    #     sleep(1)
    #     self.sd_tester.send_request_and_recv_response([0x22, 0x70, 0X23],recv=[0x62, 0x70, 0X23, 0x00, 0x05, 0X00, 0X05,0X05,0X05,0X20,0X26,0X28])
                

    #     self.sd_tester.send_request_and_recv_response([0x14, 0xFF, 0XFF ,0xFF],recv=[0x54])
    #     sleep(1)
    #     self.sd_tester.send_request_and_recv_response([0x19, 0x04, 0XD3, 0x24, 0x47, 0x20],recv=[0x59, 0x04, 0XD3, 0x24, 0x47, 0x00])
        
    #     self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
    #     self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.On, lev_sts=HeatLevel.Low)
    #     self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.HMI)
        
         
    #     self.bus_comm.set_singal("cem_lin4","AswmCem_Lin4Fr01","WhlFailrSts",0x40)
    #     sleep(1)       
    #     # self.sd_tester.send_request_and_recv_response([0x19, 0x04, 0XD3, 0x24, 0x47, 0x20],recv=[0x59, 0x04, 0XD3, 0x24, 0x47, 0x2F])
    #     self.sd_tester.send_request_and_recv_response([0x19, 0x02, 0XFF],recv=[0x59])
    #     sleep(12)
    #     self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
    #     self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI) 

    #     self.bus_comm.set_singal("cem_lin4","AswmCem_Lin4Fr01","WhlFailrSts",0x00)
    #     sleep(1)       
    #     # self.sd_tester.send_request_and_recv_response([0x19, 0x04, 0XD3, 0x24, 0x47, 0x20],recv=[0x59, 0x04, 0XD3, 0x24, 0x47, 0x2F])
    #     self.sd_tester.send_request_and_recv_response([0x19, 0x02, 0XFF],recv=[0x59])   
        
        
        

    # @allure.title("U型方向盘_AvlSts=0x1_方向盘处于加热状态(CCP#13=0x4)")   ##########处理1111
    # @pytest.mark.sanity
    # # @pytest.mark.a99
    # def test_caseid_199101(self):
        

    #     self.mix.set_dtc_precontion()
    #     self.sd_tester.send_request_and_recv_response([0x22, 0x70, 0X23])

        
    #     self.bus_comm.set_singal("cem_lin4","AswmCem_Lin4Fr01","WhlFailrSts",0x40)
    #     sleep(1)       

    #     self.sd_tester.send_request_and_recv_response([0x19, 0x02, 0XFF],recv=[0x59])
        
    #     self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)

    #     sleep(12)
    #     self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Off, lev_sts=HeatLevel.Off)
    #     self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI) 

    #     self.bus_comm.set_singal("cem_lin4","AswmCem_Lin4Fr01","WhlFailrSts",0x00)
    #     sleep(1)       
    #     # self.sd_tester.send_request_and_recv_response([0x19, 0x04, 0XD3, 0x24, 0x47, 0x20],recv=[0x59, 0x04, 0XD3, 0x24, 0x47, 0x2F])
    #     self.sd_tester.send_request_and_recv_response([0x19, 0x02, 0XFF],recv=[0x59])   
        
        
    
    # @allure.title("配置CCP#186=0x1，电车没有U型方向盘加热功能")
    # @pytest.mark.sanity
    # @pytest.mark.a01112
    # def test_caseid_1992925(self):

    #     self.sd_tester.write_ccp({186:0x01})        
    #     sleep(1)
    #     self.sd_tester.send_request_and_recv_response([0x11, 0x01],recv=[0x51])
    #     sleep(5)
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={13: 0x4, 0x959:0x1})

    #     self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
       
    #     self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Non, lev_sts=HeatLevel.Off)
    #     self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
    #     self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        
    #     self.sd_tester.write_ccp({186:0x02})        
    #     sleep(1)
    #     self.sd_tester.send_request_and_recv_response([0x11, 0x01],recv=[0x51])
    #     sleep(15)
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={13: 0x4, 0x959:0x1})   
        
        
    
    # @allure.title("配置CCP#186=0x1，电车没有O型方向盘加热功能")
    # @pytest.mark.sanity
    # @pytest.mark.a01112
    # def test_caseid_1992735(self):

    #     self.sd_tester.write_ccp({186:0x01})        
    #     sleep(1)
    #     self.sd_tester.send_request_and_recv_response([0x11, 0x01],recv=[0x51])
    #     sleep(5)
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={13: 0x4, 0x959:0x2})

    #     self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
       
    #     self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Non, lev_sts=HeatLevel.Off)
    #     self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
    #     self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        
    #     self.sd_tester.write_ccp({186:0x02})        
    #     sleep(1)
    #     self.sd_tester.send_request_and_recv_response([0x11, 0x01],recv=[0x51])
    #     sleep(15)
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={13: 0x4, 0x959:0x1})   
        
        
    
    # @allure.title("U型方向盘_AvlSts=0x0_没有方向盘加热功能(CCP#13=0x4)")
    # @pytest.mark.sanity
    # @pytest.mark.a01112
    # def test_caseid_1992923(self):

    #     self.sd_tester.write_ccp({186:0x01})        
    #     sleep(1)
    #     self.sd_tester.send_request_and_recv_response([0x11, 0x01],recv=[0x51])
    #     sleep(5)
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={13: 0x4, 0x959:0x1})

    #     self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
       
    #     self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Non, lev_sts=HeatLevel.Off)
    #     self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
    #     self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        
    #     self.sd_tester.write_ccp({186:0x02})        
    #     sleep(1)
    #     self.sd_tester.send_request_and_recv_response([0x11, 0x01],recv=[0x51])
    #     sleep(15)
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={13: 0x4, 0x959:0x1})   
        
        
    
    # @allure.title("O型方向盘_AvlSts=0x0_没有方向盘加热功能(CCP#13=0x4)")
    # @pytest.mark.sanity
    # @pytest.mark.a01112
    # def test_caseid_1992733(self):

    #     self.sd_tester.write_ccp({186:0x01})        
    #     sleep(1)
    #     self.sd_tester.send_request_and_recv_response([0x11, 0x01],recv=[0x51])
    #     sleep(5)
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={13: 0x4, 0x959:0x2})

    #     self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
       
    #     self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Non, lev_sts=HeatLevel.Off)
    #     self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
    #     self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
        
    #     self.sd_tester.write_ccp({186:0x02})        
    #     sleep(1)
    #     self.sd_tester.send_request_and_recv_response([0x11, 0x01],recv=[0x51])
    #     sleep(15)
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={13: 0x4, 0x959:0x1})       
        
        
    # @allure.title("CCP#13=0x4_在normal和Driving下，手动设置U型方向盘加热等级为1档时，对应的功率（CCP#959=0x01）")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/114623?projectId=46",
    # )
    # @pytest.mark.sanity
    # @pytest.mark.a01112
    # def test_caseid_1992918(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE, ccp={186: 0x02, 13: 0x4, 0x959:0x1})
    #     self.bus_comm.set_steerwheel_PwrAllwd(PwrAllwd_val=20)
    #     sleep(.2)
    #     self.soa.hmi_set_steer_wheel_heat_level(level=HeatLevel.Low,source=SourceId.HMI)
    #     self.bus_comm.check_steerwheel_heat_req(avl_sts=AvlSts.Energylimit, lev_sts=HeatLevel.Off)
    #     self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.HMI)
    #     self.soa.get_steer_wheel_heat_level(level=HeatLevel.Off,source=SourceId.HMI)
