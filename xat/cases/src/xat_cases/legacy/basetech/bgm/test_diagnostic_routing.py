# -*- coding: utf-8 -*-
"""
@File        : diag_example.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022/10/24 18:00 PM
@Description : description about this file
@Examples    : example of how to use it
"""
from cgitb import reset
from dataclasses import dataclass
from doctest import Example
import os,sys
from urllib import response
import pytest
import allure
from time import sleep, time
from threading import Thread

work_path_1 = os.path.join(os.getcwd().split("test_case")[0],'ecu_simulator','ecu_simulator')
sys.path.append(work_path_1)

work_path_2 = os.path.join(os.getcwd().split("sat")[0],'sat')
sys.path.append(work_path_2)

#/root/wenyu.liang/sat/xat_ecu/legacy/ecu_simulator/sdk/bus_app.py
# work_path_3 = os.path.join(os.getcwd().split("test_case")[0],'ecu_simulator','ecu_simulator','sdk')
# sys.path.append(work_path_3)


from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_ecu.legacy.sdk.ecu_simulator_app import Ecu_Sim_App
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
#from sdk.bus_app import *
from xat_ecu.legacy.sdk.bus_app import  add_cyclic_msg_with_data_run

######@pytest.mark.smoke
@allure.feature("UDS")
@allure.story("诊断路由测试")
class TestiagExample(TestBase):
    def before_class(self, ecu):
        super().before_class(self,ecu)
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        #Server
        self.server = Ecu_Sim_App()
        self.server.doip_sim_start()
        self.server.all_ecu_start()

        # Client
        self.client = Sd_Tester()
        self.client.diagnostic_client_sim_start()
        logger.info("==================== SdTester started ==========================")

        sleep(0.1)
        #self.client.tester_present()
        sleep(0.5)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        try:
            #self.client.stop_tester_present()
            sleep(0.5)
            self.client.diagnostic_client_sim_close()
            self.server.doip_sim_close()
            self.server.all_ecu_close()
        except Exception as e:
            logger.info("====================  Stopped Error ==========================")
            logger.error(e)

    def after_class(self, ecu):
        super().after_class(self, ecu)
   
    @allure.title("Signal Frame Routing Test")
    def test_diag_route_example_singal_frame(self):
        """
            单帧路由测试
        """
        #self.client.send_data_to_functional_addressing([0x98,0x12,0x34])
        with allure.step('1.单帧数据发送'):
            self.client.send_data_to_functional_addressing([0x14,0xFF,0xFF,0xFF])
        with allure.step('2.获取单帧数据经过路由后,ecu对其的响应'):
            response = self.client.get_response_dict()
            #print('respinse=',response)
        with allure.step('3.对响应数据进行逻辑判断'):
            for key,value in response.items():
                print('ecu:',key,'response:',value)
                if value == '7F 14 7F':
                    if key == '1001':
                        pass
                        assert True
                    else:
                        print('Error')
                        assert False
                else:
                    assert True
 
    @allure.title("Multi Frame Routing Test")
    def test_diag_route_example_multi_frame(self):
        """
            多帧路由测试
        """
        with allure.step('0.多帧数据发送'):
            data = [0x36,0x01]
            for index in range(2,5):
                if (index%256 > 0) :
                    hex_str = hex(index%256)
                    hex_num = eval(hex_str.replace('0x', ''))
                    data.append(hex_num)
                else:
                    hex_str = hex(index)
                    hex_num = eval(hex_str.replace('0x', ''))      
                    data.append(hex_num)
        
        
        with allure.step('1.多帧数据发送'):
            self.client.update_serverdoipid(0x1001)
            self.client.transfer_data_data(data)

            # self.client.update_serverdoipid(0x1A12)
            # data_list= '2ED01Ca49cb766e25b71fc084de0524ad46442f5a3f847219dc9f729a7e6d76bbc9b14fb7e15d7bd9ffb3f1bcfdc5448154c5bf39492aabc8716f2486c234efc96a614a01b43a923d8cf5401de5115878fe86cfd2e9adfa9f28dc3d090f825cba54e6193aa8a6cdb842eced5b34be4428609312d1783055a1bbb0a740286357e115deb2874b121e5dccfee6f10d059cfc0dc7049de08e518eeeb7564d0a64e483df1768afbca3484a99cb79e12597c89cca1bd4d70ba74606db8bbec10f3b3a9118c4e40d233e6f1bbba5a9038c9cdda644d1e40b6c419535beab8e9a3b73b4251358c012aee2961e1bca3d2abf684a28209b058c0091c857055d5c8826388dd7dffe100010001fc2a8b1665746be6425d05c3d81bf9d03c9115a54b50c4a7dd9ad4ec99429577'
            # data_handle=DataTypeHanding()
            # response_space=data_handle.addstr_into_rawstr(data_list,' ',2)
            # response_hex=data_handle.hexstr_to_inlist(response_space)
            # self.client.write_public_key(response_hex)
            sleep(2)    #休眠两秒，保证获取返回值的时候数据存在
        with allure.step('2.获取多帧数据经过路由后,ecu对其的响应'):
            response = self.client.get_response_dict()
        with allure.step('3.对响应数据进行逻辑判断'):
            if response != {}:
                assert True
                print('True')
            else:
                assert False
                print('False')

if __name__ == "__main__":    
   
    example = TestiagExample()
    example.before_each_func('ecu')
    example.test_diag_route_example_singal_frame()
    #example.test_diag_route_example_multi_frame()
    sleep(10)
    example.after_each_func('ecu')



    

  










