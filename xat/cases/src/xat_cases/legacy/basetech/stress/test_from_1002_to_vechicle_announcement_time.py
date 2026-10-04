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
from xat_cases.legacy.bgm.case_helper.diag_case_helper.DiagTestBase import SniffPacket
from xat_ecu.legacy.sdk.driver.ethernet_lib.udp_brocaster_socket import *
from xat_ecu.legacy.sdk.driver.ethernet_lib.udp_socket import udp_socket_client
from xat_ecu.legacy.sdk.sdk_tools import *
import numpy as np


test_count=0

class TestBgm(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.all_time= []
        self.b_cli = DiagTestBase(self.ipdu, self.busapp,self.tc_config)
        self.path = f'./bgm_1002_vehicle_announcement_stress_log/{time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime(int(time.time())))}_功能寻址下获取1002进boot后第一条车辆公告发出时间'

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("Test running ...")
        global test_count
        test_count += 1
        with allure.step("开始抓取数据"):
            self.sniff = SniffPacket(iface=self.tc_config['bus']['eth_obd'],save_path=self.path,count=test_count)        
            self.sniff.set_save_name(f"第{test_count}次_1002_vehicle_announcement_测试_上位机抓包_")
            self.sniff.start_sniff()
        with allure.step(f"2.连接BGM:0x1002"):
            self.b_cli.connect(0x1002)    

    def after_each_func(self, ecu):
        logger.info("Test ending ...")
        logger.info(f"#############功能寻址下获取1002进boot后第一条车辆公告发出时间测试{test_count}次#############")
        logger.info(f"#############平均发出车辆公告时间{np.mean(self.all_time)}s#############")
        logger.info(f"#############最大发出车辆公告时间{np.max(self.all_time)}s#############")
        logger.info(f"#############最小发出车辆公告时间{np.min(self.all_time)}s#############") 
        with allure.step("7.读取当前会话"):
            self.b_cli.connect(0x1002)
            self.b_cli.read_data_by_identifier(0xf186)
            pl = self.b_cli.get_payload()
        with allure.step("8.退出boot"):
            self.b_cli.session_control(1)
            self.b_cli.close()
        with allure.step("9.结束抓取数据"):
            self.sniff.stop_sniff()
        with allure.step("11.检查是否在boot下"):
            assert pl == '62f18602' , "不在boot下"
        super().after_each_func(ecu)
       
    def after_class(self, ecu):
        super().after_class(self, ecu)
    
    @pytest.mark.vechicle_announcement
    @pytest.mark.repeat(10)
    @allure.title("功能寻址下获取1002进boot后第一条车辆公告发出时间")
    def test_from_1002_to_vechicle_announcement_time(self):
            try:
                with allure.step("3.检查是否在App下"):
                    self.b_cli.read_data_by_identifier(0xf186)
                    pl = self.b_cli.get_payload()
                    assert pl == '62f18601' , "不在app下"
                with allure.step("4.发送1002"):
                    before = time.time()
                    self.b_cli.sd_test.update_serverdoipid(0x1FFF)
                    self.b_cli.sd_test.send_data([0x10,0x02])
                    self.b_cli.close()
                    time.sleep(1)
                with allure.step("5.获取1002进boot后第一条车辆公告发出时间"):
                    after = self.b_cli.catch_announcenent()
                with allure.step("6.判断间隔时间是否在15s内"):
                    interval = after - before
                    self.all_time.append(interval)
                    logger.info("本次测试:功能寻址下获取1002进boot后第一条车辆公告发出时间:{}s".format(interval))
                    #assert interval <= 15
                    if interval > 15:
                        raise ValueError
            except:
                self.b_cli.close()
                self.b_cli.Get_Bgm_Log(self.path)
                assert False
                
         
#cd /root/wenyu.liang/sat/xat_cases/legacy/basetech/bgm
#pytest stress/test_from_1002_to_vechicle_announcement_time.py --tbcfg="bench_config/soa_bench_100.yaml"
#pytest stress -m vechicle_announcement --tbcfg="bench_config/soa_bench_100.yaml"