'''
Author: tom
Date: 2023-05-12 18:00:41
LastEditors: Do not edit
LastEditTime: 2023-06-16 13:41:58
FilePath: /yangliu_tmp/sat/xat_cases/legacy/bgm/case_helper/fota_case_helper/fota_signal_helper.py
'''

import os
import sys
import time
import binascii
current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path, ".."))
sys.path.append(os.path.join(current_path, "../.."))
sys.path.append(os.path.join(current_path, "../../.."))
sys.path.append(os.path.join(current_path, "../../../.."))
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.logger import logger
# from ecu_simulator.sdk.driver.tosun.libs.libTOSUN import *
from xat_ecu.legacy.sdk.bus_app import BusApp
# from ecu_simulator.sdk.driver.tosun.libs.libTOSUN import *
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.sdk.ecu_simulator_app import Ecu_Sim_App
from xat_ecu.legacy.interface.nuc_app import get_obd_ip
from xat_ecu.legacy.config.path import CONFIG_DIR_PATH
from xat_ecu.legacy.ecu_sim.parse_tb_config import ParseTBConfig


class Fota_Signal_Helper():
    def __init__(self, ipdu, busapp, tc_config):
        self.ipdu=ipdu
        self.busapp=busapp
        self.sd_test = Sd_Tester(**tc_config)
        
    def start_mock_update_precondition(self):
        self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set_vehspd(0)
        time.sleep(1)
        tb_path = os.path.join(CONFIG_DIR_PATH, "willow_bgm_flash_config.yaml")
        tb_config = ParseTBConfig(tb_path).yaml_content
        self.sd_test.diagnostic_client_sim_start()
        time.sleep(2)
        self.sd_test.tester_present()
        time.sleep(2)
        
        self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
        self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
    
    def end_mock_update_precondition(self):
        try:
            self.ipdu.time_control_stop()  
            self.busapp.stop_all_cyclic_msgs()  
            self.sd_test.stop_tester_present()
            time.sleep(0.5)
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info("==================== SdTester Stopped Error ==========================")
            logger.error(e)
            
    def diag_cancel(self):
        self.sd_test.update_serverdoipid(0x1001)       
        self.sd_test.send_data([0x31,0x01,0xA1,0x02])
        time.sleep(0.5)
        
        payload = self.sd_test.return_udsdata_and_check_and_print_response_result()
        result = self.sd_test.check_and_print_response_result()
        
        
        # self.sd_test.close()     
        
    def routing_control(self,routing_did,routing_type,data=None):
        data_send = '31'
        
        if len(hex(routing_type)[2:])%2 == 0:
            data_send = data_send +  hex(routing_type)[2:]
        else:
            data_send = data_send + '0' + hex(routing_type)[2:]
            
        if len(hex(routing_did)[2:])%2 == 0:
            data_send = data_send +  hex(routing_did)[2:]
        else:
            data_send = data_send + '0' + hex(routing_did)[2:]
     
        if data == None:
            pass
        else:                
            hex_data = binascii.b2a_hex(data)
            str_data = str(hex_data,encoding='utf-8')
            data_send = data_send + str_data    
            
    def change_car_mode(self,car_mode):
        '''
        切换 car mode
        @param mode_type: 切换的 模式
                    0 : NORMAL
                    1 : TRANSPORT
                    2 : FACTORY
                    3 : CRASH
                    5 : DYNO
        @param do_assert: 若为True 则表示切换失败则会报错，否则返回切换后的模式
        @return:
        '''
        logger.info(f"==============  Switch carmode --> {car_mode}  ==============")
        self.sd_test.update_serverdoipid(0x1002)
        time.sleep(0.5)
        curr_mode = self.sd_test.change_car_mode(car_mode, do_assert=1)
        logger.info(f"==============  Curr_Car_Mode --> {curr_mode} ===================")
        
    def change_usage_mode(self, usage_mode):
        '''
        切换 usage mode
        @param mode_type:
            /** 废弃 */ @value(0) ABANDONED,
            /** 未激活 */ @value(1) INACTIVE,
            /** 充电 */ @value(2) CONVENIENCE,
            /** 激活 */ @value(11) ACTIVE,
            /** 驾驶 */ @value(13) DRIVING
        @param do_assert: 若为True 则表示切换失败则会报错，否则返回切换后的模式
        @return:
        '''
        logger.info(f"==============  Switch usagemode --> {usage_mode}  ==============")
        self.sd_test.update_serverdoipid(0x1002)
        time.sleep(0.5)
        curr_mode = self.sd_test.change_usage_mode(usage_mode, do_assert=1)
        logger.info(f"==============  Curr_Usage_Mode --> {curr_mode} ===================")
            
    def mock_factory_update_precondition(self, Precondition_List):
        # =========================
        # HV_SOC   
        # Small_Battery_SOC
        # ==========================
        
        # HV_SOC
        if Precondition_List[0] == 1:
            self.ipdu.send_pdu(
                "propulsioncan",
                0x53F,
                [0x3F, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
                cycle_time=0.1,
            )
            self.ipdu.send_pdu(
                "propulsioncan",
                0x131,
                [0x00, 0x00, 0x00, 0x00, 0xFA, 0x05, 0x80, 0x00],
                cycle_time=0.02,
            )

            # self.ipdu.send_pdu(
            #     "propulsioncan",
            #     0x178,
            #     [0x40, 0x00, 0x00, 0x00, 0x00, 0xF3, 0x70, 0x00], 
            #     cycle_time=0.07,
            # ) 
           
                   
               
        # Small_Battery_SOC
        if Precondition_List[1] == 1:
            self.ipdu.cem_lin6_bmscem_lin6fr05_batturaw_0_bmscem_lin6signalipdu05_value(13.75)
     
      
      
                
    def mock_normal_update_precondition(self, Precondition_List):
        # =========================
        # Vehicle_Speed  
        # Gear  
        # HV_SOC 
        # HV_Thermal_Out_Of_Control    
        # Small_Battery_SOC
        # ==========================
        
        # Vehicle_Speed
        if Precondition_List[0] == 1:
            pass
        
        # Gear  挡位 PropulsionCAN  0x4B 00 00 00 01 00 00 00 00 
        #            PropulsionCAN  0x155 00 00 00 00 00 00 00 00  
        if Precondition_List[1] == 1:
            self.ipdu.send_pdu(
                "propulsioncan",
                0x4B,
                [0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00],
                cycle_time=0.10,
            )
            self.ipdu.send_pdu(
                "propulsioncan",
                0x155,
                [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                cycle_time=0.25,
            )
        
        # HV_SOC  HV电池电量 PropulsionCAN  0x131 00 00 00 00 F2 48 00 00   // 96.9%电量
        if Precondition_List[2] == 1:
            self.ipdu.send_pdu(
                "propulsioncan",
                0x53F,
                [0x3F, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
                cycle_time=0.1,
            )
            self.ipdu.send_pdu(
                "propulsioncan",
                0x131,
                [0x00, 0x00, 0x00, 0x00, 0xFA, 0x05, 0x80, 0x00],
                cycle_time=0.02,
            )
            
            #HV_SOC 电量24%
            self.ipdu.send_pdu(
                "propulsioncan",
                0x178,
                [0x40, 0x00, 0x00, 0x00, 0x00, 0xFA, 0x00, 0x00],
                cycle_time=0.07,
            )
            # #HV_SOC 电量80%
            # self.ipdu.send_pdu(
            #     "propulsioncan",
            #     0x178,
            #     [0x40, 0x00, 0x00, 0x00, 0x00, 0xC8, 0x00, 0x00],
            #     cycle_time=0.07,
            # )            
            # #HV_SOC 电量20%
            # self.ipdu.send_pdu(
            #     "propulsioncan",
            #     0x178,
            #     [0x40, 0x00, 0x00, 0x00, 0x00, 0x32, 0x00, 0x00],
            #     cycle_time=0.07,
            # )
            # #HV_SOC 电量19%
            # self.ipdu.send_pdu(
            #     "propulsioncan",
            #     0x178,
            #     [0x40, 0x00, 0x00, 0x00, 0x00, 0x2F, 0x80, 0x00],
            #     cycle_time=0.07,
            # )            
            
                    
            #  self.ipdu.send_pdu(
            #     "propulsioncan",
            #     0x175,
            #     [0xA0, 0x00, 0x00, 0x80, 0x00, 0x00, 0x00, 0x00],
            #     cycle_time=1,
            # )
                     
        # HV_Thermal_Out_Of_Control  电池热失控 PropulsionCAN  0x142 00 00 00 00 00 00 00 00
        if Precondition_List[3] == 1:
            self.ipdu.send_pdu(
                "propulsioncan",
                0x142,
                [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                cycle_time=1,
            )
            
        # Small_Battery_SOC  小电池电量 LIN6 BmsCem_Lin6Fr05_CEM_LIN6(0x06) BattSocRaw_CEM_LIN6
        if Precondition_List[4] == 1:
            self.ipdu.send_pdu(
                "bodycan",
                0x53F,
                [0x3F, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
                cycle_time=1,
            )            
            self.ipdu.cem_lin6_bmscem_lin6fr05_battsocraw_value(90.10)         
            self.ipdu.cem_lin6_bmscem_lin6fr05_batturaw_0_bmscem_lin6signalipdu05_value(13.75)
        
if __name__ == "__main__":
    pass