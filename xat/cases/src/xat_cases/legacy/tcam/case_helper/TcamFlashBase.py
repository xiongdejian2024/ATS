# -*- coding: utf-8 -*-
"""
@File        : test_uds_bgm_app.py
@Author      : o_wenyu.liang_ext@jiduauto.com
@Time        : 2022/11/17
@Description :
"""

import time

from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester


class FlashTestBase:
    def __init__(self, tc_config):
        self.tc_config = tc_config
        self.logical_address = ''
        self.payload = ''
        self.ecu_name = ''
        self.sd_test = None

        self.connect(0x1011, ecu_name="TCAM")
        time.sleep(2)

    def connect(self, logical_address, ecu_name='BGM', do_3E_80=True):
        self.ecu_name = ecu_name
        self.sd_test = Sd_Tester(**self.tc_config)
        self.sd_test.update_serverdoipid(logical_address, ecu=self.ecu_name)
        time.sleep(1)
        self.logical_address = logical_address
        logger.info("当前逻辑地址:{}".format(hex(self.logical_address)))
        time.sleep(0.5)
        logger.info("==================== SdTester started ==========================")
        self.sd_test.diagnostic_client_sim_start()
        if do_3E_80:
            self.sd_test.tester_present()
        time.sleep(0.5)

    def close(self, do_close_3E_80=True):
        if do_close_3E_80:
            self.sd_test.stop_tester_present()
            time.sleep(1)
        self.sd_test.diagnostic_client_sim_close()
        time.sleep(0.5)
        logger.info("==================== SdTester stopped ==========================")

    def send_data(self, data, do_assert=True):
        if isinstance(data, int):
            data_str = hex(data)[2:].replace(' ', "")
            data_list = [int(data_str[i:i + 2], 16) for i in range(0, len(data_str), 2)]
            self.sd_test.send_data(data_list)
        elif isinstance(data, list):
            self.sd_test.send_data(data)
        elif isinstance(data, str):
            data_list = [int(data[i:i + 2], 16) for i in range(0, len(data), 2)]
            self.sd_test.send_data(data_list)
        self.payload = self.sd_test.return_udsdata_and_check_and_print_response_result()
        result = self.sd_test.check_and_print_response_result()

        if not do_assert:
            pass
        else:
            if not result or result is None:
                raise ValueError

    def get_payload(self):
        data_str_list = []
        for elemnt in self.payload:
            if len(hex(elemnt)[2:]) == 1:
                elemnt = '0' + hex(elemnt)[2:]
            else:
                elemnt = hex(elemnt)[2:]
            data_str_list.append(elemnt)

        data_str = "".join(data_str_list)
        return data_str

    def Flash_Tcam(self, keyinfo, file_url, standard=True, check_data=None):
        try:
            self.sd_test.upgrade_ecu(keyinfo, file_url, standard=standard, check_data=check_data)
        except Exception as e:
            self.reset_wait(360)
            assert False

    def reset_wait(self, wait_time):
        t = time.time()
        while time.time() - t < wait_time:
            try:
                self.read_data_by_identifier(0xf186, False)
                if self.get_payload()[0:2] == '62':
                    logger.info(f"重启后延时{time.time() - t}s  读取到诊断响应:{self.get_payload()}")
                    break
                time.sleep(2)
            except Exception as e:
                logger.info(f"重启后延时{time.time() - t}s未读取到诊断响应》》{str(e)}")

    def read_data_by_identifier(self, did, do_assert=True):
        data = '22'
        if len(hex(did)[2:]) % 2 == 0:
            data = data + hex(did)[2:]
        else:
            data = data + '0' + hex(did)[2:]
        self.send_data(data, do_assert)
