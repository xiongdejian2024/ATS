#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :sdtest.py
@Time         :2023/10/31 10:00
@Author       :quan.sun@jiduauto.com
@Description  :诊断仪能力模拟 实现接口
"""
from xat_ecu.api.interfaces.dp2.interface import CommonSdTest


class SdTest(CommonSdTest):
    def write_data_by_identifier(self, did: int, data: str):
        '''
        写入did
        @param did: type:int     such as :  0xF15A
        @param data: type:str     such as :  "123456789"
        @return:
        '''
        return self.sd_tester.read_data_by_identifier(did, data)

    def read_data_by_identifier(self, did: int):
        '''
        读取did
        @param did: type:int     such as :  0xF15A
        @return:
        '''
        return self.sd_tester.read_data_by_identifier(did)

    def send_data(self, data: list):
        '''
        发送数据  列表里面需要是整型
        @param data: such as [0x10, 0x03]
        @return:
        '''
        return self.sd_tester.send_data(data)

    def return_udsdata_and_check_and_print_response_result(self, diagnostic_action="Diagnostic Action"):
        '''
        发送诊断请求后，用来接收响应的
        返回一个列表 如 [0x71,0x01,0x02, 0x05,0x10,0x00,0x00,0x00,0x00,]
        @param diagnostic_action: 用来描述当前动作的
        @return:
        '''
        return self.sd_tester.return_udsdata_and_check_and_print_response_result(diagnostic_action)
