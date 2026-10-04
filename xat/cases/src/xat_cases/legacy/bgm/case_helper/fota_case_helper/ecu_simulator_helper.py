'''
Author: tom
Date: 2023-06-02 11:33:03
LastEditors: Do not edit
LastEditTime: 2023-06-08 19:16:14
FilePath: /sat/xat_cases/legacy/bgm/case_helper/fota_case_helper/ecu_simulator_helper.py
'''

import os
import sys
import time

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path, ".."))
sys.path.append(os.path.join(current_path, "../.."))
sys.path.append(os.path.join(current_path, "../../.."))
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_ecu.legacy.sdk.ecu_simulator_app import Ecu_Sim_App
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.common.file_handle import FileHandle
from xat_ecu.legacy.common.time_handle import *
from xat_ecu.legacy.sdk.s2spdu.signal2service_combination_and_send_pdu import S2sCombinationSendPdu
parent_dir = FileHandle.get_parent_dir()

class Ecu_Simulator_Helper:
    def __init__(self, ipdu, busapp):
        self.ipdu=ipdu
        self.busapp=busapp
        self.ecudiagsim=None

    def all_ecu_start(self):
        self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
        self.busapp.start_all_cyclic_msg()  
        self.ecudiagsim = Ecu_Sim_App(**self.tc_config)
        self.ecudiagsim.all_ecu_start()

    def all_ecu_close(self):
        self.ecudiagsim.all_ecu_close()
        self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
        self.busapp.stop_all_cyclic_msgs()   
        
    def pause_all_bus_send(self):
        self.ipdu.pause_all_bus_send()            
        
if __name__ == "__main__":
    pass