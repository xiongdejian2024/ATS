# -*- coding: utf-8 -*-
"""
@File        : test_uds_bgm_app.py
@Author      : o_wenyu.liang_ext@jiduauto.com
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
from xat_ecu.legacy.sdk.sdk_tools import *

test_count=0

@allure.feature("架构基础/网络架构/诊断")
class TestF18C_F1AE(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.b_cli = DiagTestBase(self.ipdu, self.busapp,self.tc_config)
        self.path = f'./bgm_f18c_stress_log/{time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime(int(time.time())))}_读取f18c_sn号1181复位测试'
        self.is_all_zero = 0
        self.is_all_ffff = 0
        self.is_not_all = 0
        with allure.step("连接BGM"):
            self.b_cli.connect(0x1001)
        with allure.step("读取SN号并保存"):
            self.b_cli.read_data_by_identifier(0xf18c)
            self.f18c_payload = self.b_cli.get_payload()
        # with allure.step("关闭BGM"):
        #     self.b_cli.close()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("Test running ...")
        logger.info("当前测试全零次数{0} 全F次数{1} 非零非F也非初始值次数{2}".format(self.is_all_zero,self.is_all_ffff,self.is_not_all))
        global test_count
        test_count +=1
        with allure.step("开始抓取数据"):
            self.sniff = SniffPacket(iface=self.tc_config['bus']['eth_obd'],save_path=self.path,count=test_count)
            self.sniff.set_save_name(f"第{test_count}次_f18c测试_上位机抓包_")
            self.sniff.start_sniff()
            
    def after_each_func(self, ecu):
        logger.info("Test ending ...")
        logger.info(f"#############1181复位读取SN号测试{test_count}次#############")
        logger.info(f"#############测试全零次数{self.is_all_zero}s#############")
        logger.info(f"#############全F次数{self.is_all_ffff}s#############")
        logger.info(f"#############非零非F也非初始值次数{self.is_not_all}s#############")    
        with allure.step("发送0x1181重启指令"):
            self.b_cli.sd_test.update_serverdoipid(0x1FFF)
            self.b_cli.reset(0x81)
        with allure.step("结束抓取数据"):
            self.sniff.stop_sniff()
        super().after_each_func(ecu)

    def after_class(self, ecu):
        with allure.step("关闭BGM"):
            self.b_cli.close()
       
        super().after_class(self, ecu)

    @pytest.mark.repeat(1000)
    def test_f18c_f1ae(self):
        try:
            with allure.step("读取0xF18C值"):
                self.b_cli.sd_test.update_serverdoipid(0x1001)
                self.b_cli.read_data_by_identifier(0xf18c)
                pl1 = self.b_cli.get_payload()
            with allure.step("判断0xF18C值"):
                if pl1 !=  self.f18c_payload:
                    if pl1 == "62f18c00000000":
                        logger.info("f18c读出全零")
                        self.is_all_zero  = self.is_all_zero + 1
                        raise ValueError
                    elif pl1 == "62f18cffffffff":
                        logger.info("f18c读出全F")
                        self.is_all_ffff = self.is_all_ffff + 1
                        raise ValueError
                    elif pl1!= "62f18c00000000" or pl1!="62f18cffffffff":
                        logger.info("错误值:{}".format(pl1))
                        logger.info("f18c读出既不为全零也不为全F且与上次结果不同")
                        self.is_not_all = self.is_not_all + 1
                        raise ValueError
                    else:
                        logger.info("f18c读出无误")
        except:
            self.b_cli.Get_Bgm_Log(self.path)
            assert False
       
        #assert False
## pytest stress/test_f18c_f1ae.py --tbcfg="bench_config/soa_bench_100.yaml" --disable_partner='true'
## nohup pytest -sv uds/test_f18c_f1ae.py > log/test_f18c_f1ae.txt 2>&1 &