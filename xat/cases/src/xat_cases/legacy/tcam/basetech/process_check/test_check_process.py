#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_

"""
@File: test_check_process.py
@Time: 2022/7/10 10:08
@Author: lei.tao
@Software: PyCharm
@Description: 冒烟测试用例
@Examples: 检查TCAM进程是否正常启动
"""

import allure
import os
import sys
import pytest

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH
from xat_ecu.legacy.driver.ssh_client import SSHFailException, SSHClient
from xat_ecu.legacy.common.logger import logger


def con(process=None):  
    """ 
    param process : 进程
    """
    logger.info(f"检查进程{process}")
    try:
        stdout1 = TCAM_SSH().exec(f"ps -ef | grep {process}", ip)

        with allure.step(f"查看进程 {process}"):
            allure.attach("{0}".format(stdout1), f"进程 {process} 的stdout")
            # allure.attach("{0}".format(stderr1), f"进程 {process} 的stderr")

        stdout2 = TCAM_SSH().exec("ps -ef | grep " + process + " | grep -v grep | awk '{print $2}'", ip)
        if stdout2 != "":
            with allure.step(f"查看进程 {process} 是否启动"):
                allure.attach("{0}".format("启动成功"), f"进程 {process}")
            with allure.step(f"查看进程 {process} 的PID"):
                allure.attach("{0}".format(stdout2), f"进程 {process} 的PID")

        else:
            with allure.step(f"查看进程 {process} 是否启动"):
                allure.attach("{0}".format("启动失败"), f"进程 {process}")

        assert stdout2 != "", f"【TCAM】进程{process}启动失败"

    except SSHFailException as e:
        print(f'The server connect failed with error {e}')
        raise SSHFailException


# @pytest.mark.smoke
# @allure.feature("架构基础")
# @allure.story("EM")
# class Test_process(TestBase):
#     def before_class(self, ecu):
#         super().before_class(self, ecu)
#         global ip
#         ip = self.tc_config.get('gateway_ip')

#     def before_each_func(self, ecu):
#         super().before_each_func(ecu)

#     def after_each_func(self, ecu):
#         super().after_each_func(ecu)

#     def after_class(self, ecu):
#         # os.system("ps -ef|grep -i ssh|awk '{printf $2" + ' "\\n" ' + "}'|xargs kill -9 ; ps -ef|grep -i ssh")
#         # logger.debug("清除所有ssh进程")
#         super().after_class(self, ecu)

#     @allure.title("校验进程: jetlogd")
#     def test01_caseid_1196477(self):
#         """
#         校验进程: jetlogd 是否正常启动
#         """
#         con(process="jetlogd")

#     @allure.title("校验进程:gnss_location")
#     def test02_caseid_1196478(self):
#         """
#         校验进程: gnss_location 是否正常启动
#         """
#         con(process="gnss_location")

#     @allure.title("校验进程: service_monitor")
#     def test03_caseid_1196479(self):
#         """
#         校验进程: service_monitor 是否正常启动
#         """
#         con(process="service_monitor")

#     @allure.title("校验进程: sshd")
#     def test04_caseid_1196480(self):
#         """
#         校验进程: sshd 是否正常启动
#         """
#         con(process="sshd")

#     @allure.title("校验进程: phc2sys")
#     def test05_caseid_1196471(self):
#         """
#         校验进程: phc2sys 是否正常启动
#         """
#         con(process="phc2sys")

#     @allure.title("校验进程: em2")
#     def test06_caseid_1196472(self):
#         """
#         校验进程: em2 是否正常启动
#         """
#         con(process="/oemapp/bin/em2")
    
#     @allure.title("校验进程: ptp4l")
#     def test07_caseid_1196473(self):
#         """
#         校验进程: ptp4l 是否正常启动
#         """
#         con(process="ptp4l")

#     @allure.title("校验进程: prop")
#     def test08_caseid_1196474(self):
#         """
#         校验进程: prop 是否正常启动
#         """
#         con(process="prop")

#     @allure.title("校验进程: CertificateMgr")
#     def test09_caseid_1196475(self):
#         """
#         校验进程: CertificateMgr 是否正常启动
#         """
#         con(process="CertificateMgr")

#     @allure.title("校验进程: v2trouter")
#     def test10_caseid_1196476(self):
#         """
#         校验进程: v2trouter 是否正常启动
#         """
#         con(process="v2trouter")
        
#     @allure.title("校验进程: gb32960_service")
#     def test11_caseid_1196477(self):
#         """
#         校验进程: gb32960_service 是否正常启动
#         """
#         con(process="gb32960_service")
    
#     @allure.title("校验进程:  CellNetworkManager ")
#     def test12_caseid_1196478(self):
#         """
#         校验进程: CellNetworkManager 是否正常启动
#         """
#         con(process="CellNetworkManager")   
        
#     @allure.title("校验进程:  diagd_iautosar ")
#     def test13_caseid_1196479(self):
#         """
#         校验进程: diagd_iautosar 是否正常启动
#         """
#         con(process="diagd_iautosar")   

#     @allure.title("校验进程:  xcall_service ")
#     def test14_caseid_1196480(self):
#         """
#         校验进程: xcall_service 是否正常启动
#         """
#         con(process="xcall_service")   
        
#     @allure.title("校验进程:  prop ")
#     def test15_caseid_1196481(self):
#         """
#         校验进程: prop 是否正常启动
#         """
#         con(process="prop")    

#     @allure.title("校验进程:  config_service ")
#     def test16_caseid_1196482(self):
#         """
#         校验进程: config_service 是否正常启动
#         """
#         con(process="config_service")  
    
#     @allure.title("校验进程:   rvc  ")
#     def test17_caseid_1196483(self):
#         """
#         校验进程:  rvc  是否正常启动
#         """
#         con(process="rvc")   
        
#     @allure.title("校验进程: ua_server_app  ")
#     def test18_caseid_1196484(self):
#         """
#         校验进程:  ua_server_app 是否正常启动
#         """
#         con(process="ua_server_app") 

#     @allure.title("校验进程: misc ")
#     def test20_caseid_1196486(self):
#         """
#         校验进程:  misc 是否正常启动
#         """
#         con(process="misc")  
         
#     @allure.title("校验进程: rtc ")
#     def test21_caseid_1196487(self):
#         """
#         校验进程:  rtc 是否正常启动
#         """
#         con(process="rtc")      

#     @allure.title("校验进程: vehicle_data_mining_engine")
#     def test22_caseid_1196488(self):
#         """
#         校验进程: vehicle_data_mining_engine 是否正常启动
#         """
#         con(process="vehicle_data_mining_engine")  
        
#     @allure.title("校验进程: remote_log")
#     def test23_caseid_1196489(self):
#         """
#         校验进程: remote_log 是否正常启动
#         """
#         con(process="remote_log")     
    
#     # GB版本去掉了    
#     # @allure.title("校验进程: monitor_agent")
#     # def test24_caseid_1196490(self):
#     #     """
#     #     校验进程: monitor_agent是否正常启动
#     #     """
#     #     con(process="monitor_agent")     
    
#     # GB版本去掉了
#     # @allure.title("校验进程: sys_monitor")
#     # def test25_caseid_1196491(self):
#     #     """
#     #     校验进程: sys_monitor 是否正常启动
#     #     """
#     #     con(process="sys_monitor") 
           
#     @allure.title("校验进程: network_manager")
#     def test25_caseid_1196491(self):
#         """
#         校验进程: network_manager 是否正常启动
#         """
#         con(process="network_manager")                        



# if __name__ == '__main__':
#     pytest.main(['-vs', 'test_check_process.py'])
# # pytest -vs -p no:warnings process_check/test_check_process.py::Test_process::test25_caseid_1196491