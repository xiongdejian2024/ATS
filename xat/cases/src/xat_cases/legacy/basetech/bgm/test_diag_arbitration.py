 # -*- coding: utf-8 -*-
"""
@File        : test_uds_bgm_app.py
@Author      : o_wenyu.liang_ext@jiduauto.com
@Time        : 2022/11/17
@Description :

"""
import time
import pytest
import allure
import sys, os


project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

work_path_2 = os.path.join(os.getcwd().split("sat")[0], 'sat','ecu_simulator','interface')
sys.path.append(work_path_2)

work_path_3 = os.path.join(os.getcwd().split("sat")[0], 'sat','ecu_simulator','driver')
sys.path.append(work_path_3)



from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.case_helper.fota_case_helper.tsp_helper import Tsp_Helper
from xat_cases.legacy.bgm.case_helper.fota_case_helper.fota_operationn import *
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.sdk.ecu_simulator_app import Ecu_Sim_App
from xat_ecu.legacy.interface.nuc_app import get_obd_ip
from xat_ecu.legacy.driver.ssh_client import SSHClient
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.common.logmanagment.logmanager import *


# from ecu_simulator.sdk.get_obd_ip import get_announcement_ip



# @pytest.mark.full
@allure.feature("UDS")
@allure.story("BGM_diag_arbitration测试")
@allure.feature("BGM_diag_arbitration测试")
class TestBgm_diag_arbitration(TestBase):
    def before_class(self, ecu):
        super().before_class(self,ecu)
        self.nucapp.bgm_diag_line_up()
        time.sleep(2)
            
        self.sd_test = Sd_Tester(**self.tc_config)
        self.sd_test.update_serverdoipid(0x1002)
        self.sd_test.diagnostic_client_sim_start()
        logger.info("==================== SdTester started ==========================")
        
        self.sd_test.tester_present()
        
        self.hostname = "172.16.5.1"
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        print("Test running ...")
        
        with allure.step("切换UsageMode为Abandoned"):
            self.sd_test.change_usage_mode(0)
        with allure.step("切换CarMode为Normal"):
            self.sd_test.change_car_mode(0)
            
    def after_each_func(self, ecu):
        print("Test ending ...")
        #self.b_cli.close()
        time.sleep(60)
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.nucapp.bgm_diag_line_down()
        super().after_class(self, ecu)
     
        self.sd_test.stop_tester_present()
        sleep(0.5)
        self.sd_test.diagnostic_client_sim_close()
        logger.info("==================== SdTester stopped ==========================")

    #@pytest.mark.full
    def test_Rvs(self):
        with allure.step("切换UsageMode为Driving"):
            self.sd_test.change_usage_mode(13)
        with allure.step("诊断仲裁:RVS优先级判断"):
            logger.info("开始RVS优先级诊断仲裁判断")
            result = Logmagment(logger=logger).nonblocking_pattern_check('172.16.5.1','bgm',pattern="Received heart beat for remote_vehicle_status:daily version collection",timeout=120)
            if result: 
                with allure.step("RVS赢得仲裁权"):
                    logger.info("RVS赢得仲裁权")
                    assert True
                with allure.step("RVS失败获得得仲裁权"):
                    logger.info("RVS赢得仲裁权")
            else:
                assert False
     
    #@pytest.mark.full
    def test_Diag_Line(self):  
        with allure.step("诊断激活线上电"):
            self.nucapp.bgm_diag_line_up()
        with allure.step("诊断仲裁:诊断激活线优先级判断"):
            logger.info("开始诊断激活线优先级诊断仲裁判断")
            result = Logmagment(logger=logger).nonblocking_pattern_check('172.16.5.1','bgm',pattern="Received heart beat for uds_server:local diag",timeout=10)
            if result: 
                with allure.step("诊断激活线赢得仲裁权"):
                    logger.info("诊断激活线赢得仲裁权")
                    assert True
            else:
                assert False
        with allure.step("诊断激活线下电"):
            self.nucapp.bgm_diag_line_up()
    
    #@pytest.mark.full
    def test_Edr(self):
        with allure.step("切换UsageMode为Convenience"):
            self.sd_test.change_usage_mode(2)
        with allure.step("诊断仲裁:EDR优先级判断"):
            logger.info("开始诊EDR优先级诊断仲裁判断")
            result = Logmagment(logger=logger).nonblocking_pattern_check('172.16.5.1','bgm',pattern="Received heart beat for edr_service:daily version collection", timeout=120)
            if result: 
                with allure.step("EDR赢得仲裁权"):
                    logger.info("EDR赢得仲裁权")
                    assert True
            else:
                assert False
      
    # def test_ETCM(self):
        
    #     bgm_ssh = BGM_SSH(self.hostname)
        
    #     cmd1 = " export ENV_APP_PATH=/app/ "
            
    #     # cmd1 = "export JIDU_APP_LOG_PATH=/log/ \
    #     #         export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/data/test_lib:/app/lib \
    #     #         export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib/soa \
    #     #         export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib/proxy \
    #     #         export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/service/em \
    #     #         export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/service/prop \
    #     #         export ENV_APP_PATH=/app/ \
    #     #         export ENV_APP_INFO=/app/etc/AppInfo.json \
    #     #         export ENV_SOA_CONFIG_PATH=/app/etc/soaconfig/ \
    #     #         export ENV_CONFIG_PATH=/app/etc/ \
    #     #         export UDSDOIP_CONFIG_PATH=/app/bin/udsconfig/ \
    #     #         export UDSDOIP_DATA_PATH=/data/uds/ \
    #     #         export UDSDOIP_LOG_PATH=/log/uds/ \
    #     #         export UDSDOIP_STLOG_LEVEL=warn \
    #     #         export PAVARO_HOME_DIR=/app/etc/soaconfig \
    #     #         export BOOTES_HOME_DIR=/app/etc \
    #     #         export JETCRASH_DMP_DIR=/log/jetcrash/" 
        
    #     # cmd2 = '/app/bin/trigger etc setGearP'
    #     # cmd3 = '/app/bin/trigger etc mockcmd'
    #     # cmd4 = 'ls'
    #     # os.system(cmd1)
    #     outmsg_1 = bgm_ssh.type_commands(cmd1)
    #     # outmsg_2 = bgm_ssh.type_commands(cmd2)
    #     # outmsg_3 = bgm_ssh.type_commands(cmd3)
    #     # outmsg_4 = bgm_ssh.type_commands(cmd4)
    #     # print('outmsg_1=',outmsg_1)
    #     # print('outmsg_2=',outmsg_2)
    #     # print('outmsg_3=',outmsg_3)
    #     # print('outmsg_4=',outmsg_4)
        
    #     # data1 = Logmagment(logger=logger).nonblocking_pattern_check(self.hostname,pattern="remote diag win the arbitration rights", timeout=120)
               
    #     # if data1: 
    #     #     print("第",i,"ETCM赢得仲裁权")
    #     #     assert True
    #     # else:
    #     #     assert False

        
    #     # os.system(cmd1)
    #     # os.system(cmd2)
        # os.system(cmd3)
       
if __name__ == "__main__":
    print("!")
    pass

#cd /root/wenyu.liang/sat/xat_cases/legacy/bgm
#pytest uds/test_diag_arbitration.py::TestBgm_diag_arbitration::test_Rvs --tbcfg="bench_config/soa_bench_005.yaml"  
#pytest uds/test_diag_arbitration.py::TestBgm_diag_arbitration::test_Edr --tbcfg="bench_config/soa_bench_005.yaml"  
#pytest uds/test_diag_arbitration.py::TestBgm_diag_arbitration::test_Diag_Line --tbcfg="bench_config/soa_bench_005.yaml"  
#pytest uds/test_diag_arbitration.py::TestBgm_diag_arbitration::test_ETCM --tbcfg="bench_config/soa_bench_005.yaml"  
#pytest uds/test_diag_arbitration.py  --tbcfg="bench_config/soa_bench_005.yaml"  



