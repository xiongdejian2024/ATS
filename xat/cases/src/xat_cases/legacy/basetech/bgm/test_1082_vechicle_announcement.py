import time
import pytest
import allure
import sys, os
import socket

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

work_path_2 = os.path.join(os.getcwd().split("sat")[0], 'sat', 'ecu_simulator', 'interface')
sys.path.append(work_path_2)


from xat_cases.legacy.bgm.case_helper.test_base import TestBase
 
from xat_cases.legacy.bgm.NetworkChannel.test_networkChannel import con_bgm
from xat_ecu.legacy.sdk.bus_app import BusApp
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.logger import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_cases.legacy.bgm.case_helper.diag_case_helper.DiagTestBase import *
from xat_ecu.legacy.sdk.driver.ethernet_lib.udp_brocaster_socket import *
from xat_ecu.legacy.sdk.driver.ethernet_lib.udp_socket import udp_socket_client


@allure.feature("架构基础/网络架构/诊断")
class TestBgm(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
            
        with allure.step(f"连接BGM"):
            self.b_cli = DiagTestBase(self.ipdu, self.busapp,self.tc_config)
            # self.b_cli.connect(0x1FFF)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("Test running ...")
        self.b_cli.init_enter_boot_enviroment()
        with allure.step("连接BGM"):
            self.b_cli.connect(0x1FFF)
            time.sleep(5)

    def after_each_func(self, ecu):
        logger.info("Test ending ...")
        with allure.step("关闭BGM连接"):
            self.b_cli.close()
        super().after_each_func(ecu)
       
    def after_class(self, ecu):
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        # with allure.step(f"关闭BGM"):
        #     self.b_cli.close()
        super().after_class(self, ecu)
    
    @pytest.mark.repeat(10)
    def test_1082_vechicle_announcement(self):
        with allure.step("发送1082时间"):
            before = time.time()
            logger.info("发送1082时间:{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        #print("timetime:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            self.b_cli.sd_test.send_data([0x10,0x82])
        #self.b_cli.reset(0x81)
        # self.b_cli.close()
        with allure.step("第一条车辆公告的发出时间"):
            after = self.catch_announcenent()
            interval = after - before
            logger.info("本次测试:1082到第一条车辆公告的发出时间:{}s".format(interval))
        with allure.step("判断间隔时间是否超过17.5s"):
            assert interval < 17.5
        # self.b_cli.connect(0x1FFF)
        
    def catch_announcenent(self):
        bufsize = 1024
        addr = ('', 13400)
        udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpServer.bind(addr)
        logger.info("Waiting for connection....")
        #
        #udpServer.sendto(b'\x02\xfd\x00\x01\x00\x00\x00\x00', ('169.254.255.255', 13400))
        #
        while True:
            data,client_info = udpServer.recvfrom(bufsize)
            # data = data.decode(encoding='ascii')
            if b'\x02\xfd\x00\x04' in data:
                after = time.time()
                ip=client_info[0]
                #print(client_info[0], end=" ")
                logger.info("获取到第一条车辆公告时间:{0} ip:{1}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),ip))
                break
        return after

#cd /root/wenyu.liang/sat/xat_cases/legacy/bgm
#pytest uds/test_1082_vechicle_announcement.py