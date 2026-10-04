#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_charge_pile_open_charge_lid.py
@Time         :2023/1/31 17:54:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import os
import sys
import hashlib
import datetime

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


def get_current_time_info():
    now = datetime.datetime.now()
    year = now.year -2000
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second
    # 打印结果
    print(f"当前时间：{year}年{month}月{day}日 {hour}时{minute}分{second}秒")
    return [year,month,day,hour,minute,second]

@allure.feature("互联服务")
@allure.story("数字钥匙和账号/其他/SE")
class TestEDR(TestABCBase):
    def before_class(self,ecu):
        super().before_class(self, ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        pass
    
    def after_each_func(self, ecu):
        self.io.bgm_diag_line_up()
    
    def test_caseid_100000x(self):
        dia_resp_payload_1_part1 = []
        dia_resp_payload_1_part2 = []
        dia_resp_payload_2_part1 = []
        dia_resp_payload_2_part2 = []
        dia_resp_payload_3_part1 = []
        dia_resp_payload_3_part2 = []
        for i in range(618):
            value = i%255
            dia_resp_payload_1_part1.append(value)
            dia_resp_payload_2_part1.append(value)
            dia_resp_payload_3_part1.append(value)
        
        for i in range(148):
            dia_resp_payload_1_part2.append(i)
            dia_resp_payload_2_part2.append(i)
            dia_resp_payload_3_part2.append(i)

        dia_resp_1 = [0x62,0xFA,0x13]  + dia_resp_payload_1_part1 + get_current_time_info() + dia_resp_payload_1_part2
        sleep(5)
        dia_resp_2 = [0x62,0xFA,0x14]  + dia_resp_payload_2_part1 + get_current_time_info() + dia_resp_payload_2_part2
        sleep(5)
        dia_resp_3 = [0x62,0xFA,0x15]  + dia_resp_payload_3_part1 + get_current_time_info() + dia_resp_payload_3_part2

        logger.info(f"Mock FA13 响应数据:{dia_resp_1}")
        logger.info(f"Mock FA14 响应数据:{dia_resp_2}")
        logger.info(f"Mock FA15 响应数据:{dia_resp_3}")

        self.io.bgm_diag_line_down()
        self.bus_comm.pause_cycle_tx_rx_d()
        sleep(5)
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        sleep(2)
        self.sd_tester.change_usage_mode(UsageMode.CONVENIENCE)
        sleep(2)
        # dia_req_1 = self.bus_comm.recv_fr_msg(fr_id_list=[88],fr_response_id=70,recv_address=0x1C01)
        self.bus_comm.send_fr_msg(send_data=dia_resp_1,send_id=70,recv_id=88,send_address=0x1C01)
        # dia_req_2 = self.bus_comm.recv_fr_msg(fr_id_list=[88],fr_response_id=70,recv_address=0x1C01)
        self.bus_comm.send_fr_msg(send_data=dia_resp_2,send_id=70,recv_id=88,send_address=0x1C01)
        # dia_req_3 = self.bus_comm.recv_fr_msg(fr_id_list=[88],fr_response_id=70,recv_address=0x1C01)
        self.bus_comm.send_fr_msg(send_data=dia_resp_3,send_id=70,recv_id=88,send_address=0x1C01)

        # logger.info(f"dia_req_1:{dia_req_1},dia_req_2:{dia_req_2},dia_req_3:{dia_req_3}")
        # assert dia_req_1 == [0x22,0xFA,0x13] and dia_req_2 == [0x22,0xFA,0x14] and dia_req_3 == [0x22,0xFA,0x15]
    
        # self.bus_comm.send_fr_msg(send_data=dia_resp_2,send_id=70,recv_id=88,send_address=0x1C01)
        # sleep(2)
        # self.bus_comm.send_fr_msg(send_data=dia_resp_3,send_id=70,recv_id=88,send_address=0x1C01)
        # sleep(2)

        # self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        # sleep(10)
        self.io.bgm_diag_line_up()
        self.bus_comm.resume_cycle_tx_rx_d()
        assert False

if __name__ == "__main__":
    get_current_time_info()