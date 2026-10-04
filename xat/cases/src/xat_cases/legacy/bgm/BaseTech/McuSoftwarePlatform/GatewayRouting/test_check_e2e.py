import csv
import os
import sys
import pytest, xlrd
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.common.common import *


@pytest.mark.mcu_test
@pytest.mark.smoke
class TestE2E(TestABCBase):
    def before_class(self, ecu):
        self.sd_tester.update_serverdoipid(0x1002)
        # 读取ccp  方便后面进行恢复
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0x06],                                                                    recv=[0x62, 0xF1, 0x06])
        self.ccp_original_value = recv_data_list[3:1556 + 3]
        self.sd_tester.write_ccp(ccp={950: 0x01, 962: 0x02})  # mars1 800v
        self.mix.set_common_precontion(
            usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL
        )

    def before_each_func(self, ecu):
        pass

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        self.sd_tester.write_ccp_value(self.ccp_original_value)
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.error(f"----------> after_class Error{str(e)}")


    @allure.title("校验bgm 发出的e2e 是否正确")
    def test_check_e2e_caseid_1985896(self):
        excel_path = "mcu/config_data/check_e2e/"
        self.data_list = self.mix.read_check_e2e_excel(excel_path)
        self.mix.check_e2e_func(self.data_list)
