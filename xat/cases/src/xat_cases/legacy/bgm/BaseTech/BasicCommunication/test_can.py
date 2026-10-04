"""
@File        : test_can.PY
@Author      : O_daidi.liang@external.jiduauto.com
@Time        : 2024/02/25 15:12
@Description : cdd 打包的相关用例

"""
import subprocess
import pytest
import allure
import pytest
import allure
import re
from xat_cases.legacy.bgm.mcu.case_helper.test_abc_base import TestABCBase 
from xat_ecu.api.common.common import *
from xat_cases.legacy.bgm.mcu.case_helper.mcu_interface import MCU_Interface
from xat_ecu.legacy.sdk.bus_app import BusApp
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.api.abc_interface import *

@pytest.mark.mcu_test
@allure.feature("通讯功能")
@allure.story("can通讯")
class Test_Switch(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # Code Location

    def after_each_func(self, ecu):
        # Code Location
        super().after_each_func(ecu)
       

    def after_class(self, ecu):
        # Code Location
        super().after_class(self, ecu)

    

    # @pytest.mark.can_communicate
    # def test_check_bodycan_app_busoff(self):
    #     self.mix.check_app_busoff_channel_recv_msg("bodycan")

    # @pytest.mark.can_communicate
    # def test_check_propulsioncan_app_busoff(self):
    #     self.mix.check_app_busoff_channel_recv_msg("propulsioncan")

    # @pytest.mark.can_communicate
    # def test_check_chassiscan1_app_busoff(self):
    #     self.mix.check_app_busoff_channel_recv_msg("chassiscan1")

    # @pytest.mark.can_communicate
    # def test_check_chassiscan2_app_busoff(self):
    #     self.mix.check_app_busoff_channel_recv_msg("chassiscan2")

    # @pytest.mark.can_communicate
    # def test_check_passivesafetycan_app_busoff(self):
    #     self.mix.check_app_busoff_channel_recv_msg("passivesafetycan")

    # @pytest.mark.can_communicate
    # def test_check_infocanfd_app_busoff(self):
    #     self.mix.check_app_busoff_channel_recv_msg("infocanfd")

    # @pytest.mark.can_communicate
    # def test_check_bodyexposedcanfd_app_busoff(self):

    #     self.mix.check_app_busoff_channel_recv_msg("bodyexposedcanfd")

    # @pytest.mark.can_communicate
    # def test_check_adcanfd_app_busoff(self):
    #     self.mix.check_app_busoff_channel_recv_msg("adcanfd")
        
    # @pytest.mark.can_communicate
    # def test_check_bodycan_boot_busoff(self):
    #     self.mix.check_boot_busoff_channel_recv_msg("bodycan")

    # @pytest.mark.can_communicate
    # def test_check_passivesafetycan_boot_busoff(self):
    #     self.mix.check_boot_busoff_channel_recv_msg("passivesafetycan")

    # @pytest.mark.can_communicate
    # def test_check_bodyexposedcanfd_boot_busoff(self):
    #     self.mix.check_boot_busoff_channel_recv_msg("bodyexposedcanfd")

    @pytest.mark.sanity
    @allure.title("check can send msg id")
    def test_check_send_msg_id_caseid_1984972(self):
        for channel_name in ["bodycan","propulsioncan","chassiscan1","chassiscan2","passivesafetycan","infocanfd","bodyexposedcanfd","adcanfd","connectivitycanfd"]:
            bus_send_recv_dict = self.mix.get_bus_send_recv_info(ipdu=self.bus_comm.ipdu, channel_name=channel_name)
            tx_cicle_data = [i for i in bus_send_recv_dict["tx_nodes"]["cyclic"]["BGM"]]
            tx_spontaneous_data = [i for i in bus_send_recv_dict["tx_nodes"]["spontaneous"]["BGM"]]
            #发送周期性数据
            send_error_msg_list = []

            for i in tx_cicle_data:
                recv_msg_data, time_stamp = self.bus_comm.recv_msg_by_id_func(channel_name,i["msg_id"])
                if recv_msg_data == None:
                    send_error_msg_list.append(channel_name + str(i))
                logger.info(f"999999999999999999999 {channel_name} {recv_msg_data},{time_stamp}")
            assert not(len(send_error_msg_list)),f"存在 {send_error_msg_list} msg id 未发送出去"

    @pytest.mark.sanity
    @allure.title("check can send msg length")
    def test_check_send_msg_lenth_caseid_1984970(self):
        for channel_name in ["bodycan","propulsioncan","chassiscan1","chassiscan2","passivesafetycan","infocanfd","bodyexposedcanfd","adcanfd","connectivitycanfd"]:
            bus_send_recv_dict = self.mix.get_bus_send_recv_info(ipdu=self.bus_comm.ipdu, channel_name=channel_name)
            tx_cicle_data = [i for i in bus_send_recv_dict["tx_nodes"]["cyclic"]["BGM"]]
            tx_spontaneous_data = [i for i in bus_send_recv_dict["tx_nodes"]["spontaneous"]["BGM"]]
            #发送周期性数据
            send_error_msg_lenth_list = []
            for i in tx_cicle_data:
                recv_msg_data, time_stamp = self.bus_comm.recv_msg_by_id_func(channel_name,i["msg_id"])
                if len(recv_msg_data) != i["msg_length"]:
                    send_error_msg_lenth_list.append(channel_name + str(i))
            assert not(len(send_error_msg_lenth_list)),f"存在 {send_error_msg_lenth_list} msg id 未发送出去"


        
        
    
    