# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# """
# @File        : test_rvs.py
# @Author      : hui.zhao@jiduauto.com
# @Time        : 2023/12/1 11:30
# @Description: BGM RVS功能测试
# """

# import os
# import sys
# import pytest
# import allure
# from time import sleep
# import threading
# import math

# sys.path.append(os.getcwd())
# sys.path.append(os.path.join(os.getcwd(), ".."))
# sys.path.append(os.path.join(os.getcwd(), "../.."))
# sys.path.append(os.path.join(os.getcwd(), "../../.."))

# from test_case.abc_demo.case_helper.test_abc_base import TestABCBase
# from sdk_interface.abc_interface import *
# from ecu_simulator.tsp.rvs_client import RvsClient
# from signal_value_mapping import *

# @allure.feature("BGM车云")
# @allure.story("基础数据上报")
# @pytest.mark.order_last
# class TestRVS(TestABCBase):
#     def before_class(self, ecu):
#         self.io.tcam_power_off()
#         sleep(1)
#         self.io.bgm_power_off()
#         self.soa.update(["RemoteCtrlService_server"])
#         sleep(3)
#         self.io.bgm_power_on()
#         sleep(15)
#         self.io.tcam_power_on()
#         sleep(15)
#         self.vid = self.tb_config["vid"]
#         self.rvs_client = RvsClient(vid=self.vid)
#         logger.info("VID: {0}".format(self.vid))
#         sleep(180)

#     def before_each_func(self, ecu):
#         self.bus_comm.recover_extral_light_to_defaul_sts()
#         self.bus_comm.set_extral_light_button_to_defaul_sts()

#     def after_each_func(self, ecu):
#         self.bus_comm.set_singal("bodycan","CcmBodyFr29","FragCh1Id",0)
#         self.bus_comm.set_singal("bodycan","CcmBodyFr29","FragCh2Id",0)
#         self.bus_comm.set_singal("bodycan","CcmBodyFr29","FragCh3Id",0)
#         self.bus_comm.set_singal("bodycan","CcmBodyFr25","FragCh1UseUpWrn",0)
#         self.bus_comm.set_singal("bodycan","CcmBodyFr25","FragCh2UseUpWrn",0)
#         self.bus_comm.set_singal("bodycan","CcmBodyFr25","FragCh3UseUpWrn",0)



#     def after_class(self, ecu):
#         self.soa.stop_soa()
#         sleep(1)
#         self.io.tcam_power_off()
#         sleep(180)
#         self.io.bgm_power_off()
#         sleep(1)
#         self.io.tcam_power_on()
#         sleep(1)
#         self.io.bgm_power_on()
#         sleep(15)




#     @pytest.mark.sanity
#     def test_outview_defrost_caseid_888888(self):
#         '''远程授权启动 '''
#         self.soa.send_event_notify("RemoteCtrlService_server", "RemoteAuthStartModeSts", {"info":{"sts":0,"time":0}})
#         sleep(1)
#         for key in [1,2,3,4,5,0]:
#             self.soa.send_event_notify("RemoteCtrlService_server", "RemoteAuthStartModeSts", {"info":{"sts":key,"time":0}})
#             self.tsp.check_rvs_data_update_new(block=BlockName.BusStatus,keys=["remoteAuthInfo","remoteAuthSts"],target_value=key)



#     @pytest.mark.sanity
#     def test_caseid_999999(self):
#         '''远程电池加热状态 '''
#         self.soa.send_event_notify("RemoteCtrlService_server", "RemoteBatteryHeatingInfo", {"heatInfo":{"modeSts":1,"heatSts":0}})
#         sleep(1)
#         for key in range(0, 4):
#             self.soa.send_event_notify("RemoteCtrlService_server", "RemoteBatteryHeatingInfo", {"heatInfo":{"modeSts":key,"heatSts":0}})
#             self.tsp.check_rvs_data_update_new(block=BlockName.CabinStatus,keys=["remoteBatHeatInfo","modeSts"],target_value=key)
#         sleep(1)
#         self.soa.send_event_notify("RemoteCtrlService_server", "RemoteBatteryHeatingInfo", {"heatInfo":{"modeSts":0,"heatSts":1}})
#         sleep(1)
#         for key in range(0, 4):
#             self.soa.send_event_notify("RemoteCtrlService_server", "RemoteBatteryHeatingInfo", {"heatInfo":{"modeSts":0,"heatSts":key}})
#             self.tsp.check_rvs_data_update_new(block=BlockName.CabinStatus,keys=["remoteBatHeatInfo","heatSts"],target_value=key)
#         sleep(1)
#         self.soa.send_event_notify("RemoteCtrlService_server", "RemoteBatteryHeatingInfo", {"heatInfo":{"modeSts":0,"heatSts":0}})