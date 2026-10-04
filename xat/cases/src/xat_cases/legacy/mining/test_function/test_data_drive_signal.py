
import os
import sys
import time

import pytest
from xat_cases.legacy.bgm.case_helper.test_base import TestBase

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path.split("sat")[0], "sat"))
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *

from xat_ecu.legacy.soa_partner.src.Operator import SOAOperator
from xat_ecu.legacy.soa_partner.src import partner_client
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_ecu.legacy.common.logger import *
from xat_cases.legacy.mining.case_helper.parse_excel import get_signal_testcases_from_excel
from xat_ecu.legacy.soa_partner.src.state import CAN_CONSTANT, UPSTREAM, CASE_RUN
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester


@pytest.mark.full
@pytest.mark.datadrive
class TestMiningSignal(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        """CAN、LIN、FR总线相关资源初始化"""
        self.ipdu.start_all_time_control()
        self.busapp.start_all_cyclic_msg()

        self.sd_tester = Sd_Tester(**self.tc_config)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.diagnostic_client_sim_start()
        self.sd_tester.tester_present()

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.ipdu.reset_check_results()
        self.sd_tester.change_usage_mode(13)

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.sd_tester.stop_tester_present()
        self.sd_tester.diagnostic_client_sim_close()
        """总线相关资源回收"""
        self.ipdu.time_control_stop()
        self.busapp.stop_all_cyclic_msgs()
        super().after_class(self, ecu)
        #
        # """使用模式切换、配置字修改相关资源回收"""
        # sd_test_teardown(self.sd_test)

    @pytest.mark.BackboneFR
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("test_case", get_signal_testcases_from_excel("signal_mining.xlsx", "BackboneFR"),
                             ids=get_signal_testcases_from_excel("signal_mining.xlsx", "BackboneFR", ids=True))
    def test_data_signal_BackboneFR(self, test_case):
        """发送CAN、LIN、FR信号"""
        try:
            logger.info(f"开始发送信号：总线：{test_case.bus_name}, 报文：{test_case.message_id}, "
                        f"信号名：{test_case.signal_name}, 信号值：{test_case.signal_value}")
            send_bus_signals_V2(self.tb_config, self.ipdu, test_case)
            assert True
        except Exception as e:
            assert False

    @pytest.mark.InfoCANFD
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("test_case", get_signal_testcases_from_excel("signal_mining.xlsx", "InfoCANFD"),
                             ids=get_signal_testcases_from_excel("signal_mining.xlsx", "InfoCANFD", ids=True))
    def test_data_signal_InfoCANFD(self, test_case):
        """发送CAN、LIN、FR信号"""
        try:
            logger.info(f"开始发送信号：总线：{test_case.bus_name}, 报文：{test_case.message_id}, "
                        f"信号名：{test_case.signal_name}, 信号值：{test_case.signal_value}")
            send_bus_signals_V2(self.tb_config, self.ipdu, test_case)
            assert True
        except Exception as e:
            assert False

    @pytest.mark.ADCANFD
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("test_case", get_signal_testcases_from_excel("signal_mining.xlsx", "ADCANFD"),
                             ids=get_signal_testcases_from_excel("signal_mining.xlsx", "ADCANFD", ids=True))
    def test_data_signal_ADCANFD(self, test_case):
        """发送CAN、LIN、FR信号"""
        try:
            logger.info(f"开始发送信号：总线：{test_case.bus_name}, 报文：{test_case.message_id}, "
                        f"信号名：{test_case.signal_name}, 信号值：{test_case.signal_value}")
            send_bus_signals_V2(self.tb_config, self.ipdu, test_case)
            assert True
        except Exception as e:
            assert False

    @pytest.mark.PropulsionCAN
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("test_case", get_signal_testcases_from_excel("signal_mining.xlsx", "PropulsionCAN"),
                             ids=get_signal_testcases_from_excel("signal_mining.xlsx", "PropulsionCAN", ids=True))
    def test_data_signal_PropulsionCAN(self, test_case):
        """发送CAN、LIN、FR信号"""
        try:
            logger.info(f"开始发送信号：总线：{test_case.bus_name}, 报文：{test_case.message_id}, "
                        f"信号名：{test_case.signal_name}, 信号值：{test_case.signal_value}")
            send_bus_signals_V2(self.tb_config, self.ipdu, test_case)
            assert True
        except Exception as e:
            assert False

    @pytest.mark.ChassisCAN1
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("test_case", get_signal_testcases_from_excel("signal_mining.xlsx", "ChassisCAN1"),
                             ids=get_signal_testcases_from_excel("signal_mining.xlsx", "ChassisCAN1", ids=True))
    def test_data_signal_ChassisCAN1(self, test_case):
        """发送CAN、LIN、FR信号"""
        try:
            logger.info(f"开始发送信号：总线：{test_case.bus_name}, 报文：{test_case.message_id}, "
                        f"信号名：{test_case.signal_name}, 信号值：{test_case.signal_value}")
            send_bus_signals_V2(self.tb_config, self.ipdu, test_case)
            assert True
        except Exception as e:
            assert False

    @pytest.mark.ChassisCAN2
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("test_case", get_signal_testcases_from_excel("signal_mining.xlsx", "ChassisCAN2"),
                             ids=get_signal_testcases_from_excel("signal_mining.xlsx", "ChassisCAN2", ids=True))
    def test_data_signal_ChassisCAN2(self, test_case):
        """发送CAN、LIN、FR信号"""
        try:
            logger.info(f"开始发送信号：总线：{test_case.bus_name}, 报文：{test_case.message_id}, "
                        f"信号名：{test_case.signal_name}, 信号值：{test_case.signal_value}")
            send_bus_signals_V2(self.tb_config, self.ipdu, test_case)
            assert True
        except Exception as e:
            assert False

    @pytest.mark.PassiveSafetyCAN
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("test_case", get_signal_testcases_from_excel("signal_mining.xlsx", "PassiveSafetyCAN"),
                             ids=get_signal_testcases_from_excel("signal_mining.xlsx", "PassiveSafetyCAN", ids=True))
    def test_data_signal_PassiveSafetyCAN(self, test_case):
        """发送CAN、LIN、FR信号"""
        try:
            logger.info(f"开始发送信号：总线：{test_case.bus_name}, 报文：{test_case.message_id}, "
                        f"信号名：{test_case.signal_name}, 信号值：{test_case.signal_value}")
            send_bus_signals_V2(self.tb_config, self.ipdu, test_case)
            assert True
        except Exception as e:
            assert False

    @pytest.mark.ConnectivityCANFD
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("test_case", get_signal_testcases_from_excel("signal_mining.xlsx", "ConnectivityCANFD"),
                             ids=get_signal_testcases_from_excel("signal_mining.xlsx", "ConnectivityCANFD", ids=True))
    def test_data_signal_ConnectivityCANFD(self, test_case):
        """发送CAN、LIN、FR信号"""
        try:
            logger.info(f"开始发送信号：总线：{test_case.bus_name}, 报文：{test_case.message_id}, "
                        f"信号名：{test_case.signal_name}, 信号值：{test_case.signal_value}")
            send_bus_signals_V2(self.tb_config, self.ipdu, test_case)
            assert True
        except Exception as e:
            assert False

    @pytest.mark.BodyCAN
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("test_case", get_signal_testcases_from_excel("signal_mining.xlsx", "BodyCAN"),
                             ids=get_signal_testcases_from_excel("signal_mining.xlsx", "BodyCAN", ids=True))
    def test_data_signal_BodyCAN(self, test_case):
        """发送CAN、LIN、FR信号"""
        try:
            logger.info(f"开始发送信号：总线：{test_case.bus_name}, 报文：{test_case.message_id}, "
                        f"信号名：{test_case.signal_name}, 信号值：{test_case.signal_value}")
            send_bus_signals_V2(self.tb_config, self.ipdu, test_case)
            assert True
        except Exception as e:
            assert False

    @pytest.mark.BodyExposedCANFD
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("test_case", get_signal_testcases_from_excel("signal_mining.xlsx", "BodyExposedCANFD"),
                             ids=get_signal_testcases_from_excel("signal_mining.xlsx", "BodyExposedCANFD", ids=True))
    def test_data_signal_BodyExposedCANFD(self, test_case):
        """发送CAN、LIN、FR信号"""
        try:
            logger.info(f"开始发送信号：总线：{test_case.bus_name}, 报文：{test_case.message_id}, "
                        f"信号名：{test_case.signal_name}, 信号值：{test_case.signal_value}")
            send_bus_signals_V2(self.tb_config, self.ipdu, test_case)
            assert True
        except Exception as e:
            assert False

    @pytest.mark.CEM_LIN1
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("test_case", get_signal_testcases_from_excel("signal_mining.xlsx", "CEM_LIN1"),
                             ids=get_signal_testcases_from_excel("signal_mining.xlsx", "CEM_LIN1", ids=True))
    def test_data_signal_CEM_LIN1(self, test_case):
        """发送CAN、LIN、FR信号"""
        try:
            logger.info(f"开始发送信号：总线：{test_case.bus_name}, 报文：{test_case.message_id}, "
                        f"信号名：{test_case.signal_name}, 信号值：{test_case.signal_value}")
            send_bus_signals_V2(self.tb_config, self.ipdu, test_case)
            assert True
        except Exception as e:
            assert False

    @pytest.mark.CEM_LIN2
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("test_case", get_signal_testcases_from_excel("signal_mining.xlsx", "CEM_LIN2"),
                             ids=get_signal_testcases_from_excel("signal_mining.xlsx", "CEM_LIN2", ids=True))
    def test_data_signal_CEM_LIN2(self, test_case):
        """发送CAN、LIN、FR信号"""
        try:
            logger.info(f"开始发送信号：总线：{test_case.bus_name}, 报文：{test_case.message_id}, "
                        f"信号名：{test_case.signal_name}, 信号值：{test_case.signal_value}")
            send_bus_signals_V2(self.tb_config, self.ipdu, test_case)
            assert True
        except Exception as e:
            assert False

    @pytest.mark.CEM_LIN3
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("test_case", get_signal_testcases_from_excel("signal_mining.xlsx", "CEM_LIN3"),
                             ids=get_signal_testcases_from_excel("signal_mining.xlsx", "CEM_LIN3", ids=True))
    def test_data_signal_CEM_LIN3(self, test_case):
        """发送CAN、LIN、FR信号"""
        try:
            logger.info(f"开始发送信号：总线：{test_case.bus_name}, 报文：{test_case.message_id}, "
                        f"信号名：{test_case.signal_name}, 信号值：{test_case.signal_value}")
            send_bus_signals_V2(self.tb_config, self.ipdu, test_case)
            assert True
        except Exception as e:
            assert False

    @pytest.mark.CEM_LIN4
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("test_case", get_signal_testcases_from_excel("signal_mining.xlsx", "CEM_LIN4"),
                             ids=get_signal_testcases_from_excel("signal_mining.xlsx", "CEM_LIN4", ids=True))
    def test_data_signal_CEM_LIN4(self, test_case):
        """发送CAN、LIN、FR信号"""
        try:
            logger.info(f"开始发送信号：总线：{test_case.bus_name}, 报文：{test_case.message_id}, "
                        f"信号名：{test_case.signal_name}, 信号值：{test_case.signal_value}")
            send_bus_signals_V2(self.tb_config, self.ipdu, test_case)
            assert True
        except Exception as e:
            assert False

    @pytest.mark.CEM_LIN5
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("test_case", get_signal_testcases_from_excel("signal_mining.xlsx", "CEM_LIN5"),
                             ids=get_signal_testcases_from_excel("signal_mining.xlsx", "CEM_LIN5", ids=True))
    def test_data_signal_CEM_LIN5(self, test_case):
        """发送CAN、LIN、FR信号"""
        try:
            logger.info(f"开始发送信号：总线：{test_case.bus_name}, 报文：{test_case.message_id}, "
                        f"信号名：{test_case.signal_name}, 信号值：{test_case.signal_value}")
            send_bus_signals_V2(self.tb_config, self.ipdu, test_case)
            assert True
        except Exception as e:
            assert False

    @pytest.mark.CEM_LIN6
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("test_case", get_signal_testcases_from_excel("signal_mining.xlsx", "CEM_LIN6"),
                             ids=get_signal_testcases_from_excel("signal_mining.xlsx", "CEM_LIN6", ids=True))
    def test_data_signal_CEM_LIN6(self, test_case):
        """发送CAN、LIN、FR信号"""
        try:
            logger.info(f"开始发送信号：总线：{test_case.bus_name}, 报文：{test_case.message_id}, "
                        f"信号名：{test_case.signal_name}, 信号值：{test_case.signal_value}")
            send_bus_signals_V2(self.tb_config, self.ipdu, test_case)
            assert True
        except Exception as e:
            assert False

    @pytest.mark.CEM_LIN7
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("test_case", get_signal_testcases_from_excel("signal_mining.xlsx", "CEM_LIN7"),
                             ids=get_signal_testcases_from_excel("signal_mining.xlsx", "CEM_LIN7", ids=True))
    def test_data_signal_CEM_LIN7(self, test_case):
        """发送CAN、LIN、FR信号"""
        try:
            logger.info(f"开始发送信号：总线：{test_case.bus_name}, 报文：{test_case.message_id}, "
                        f"信号名：{test_case.signal_name}, 信号值：{test_case.signal_value}")
            send_bus_signals_V2(self.tb_config, self.ipdu, test_case)
            assert True
        except Exception as e:
            assert False


if __name__ == '__main__':
    pytest.main()
