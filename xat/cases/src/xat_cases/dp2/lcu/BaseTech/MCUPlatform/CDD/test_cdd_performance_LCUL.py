"""
@File        : test_cdd_function.py
@Author      : xiaoqiang.hu@jiduauto.com
@Time        : 2024/10/23 15:12
@Description : cdd 打包的相关用例

"""
import pytest
import allure
import time
from xat_ecu.legacy.common.logger import logger
from xat_cases.dp2.lcu.case_helper.test_abc_base import TestABCBase


@allure.feature("MCU 基础平台/CDD打包功能")
@allure.story("CDD性能用例")
class TestCddPerformance(TestABCBase):
    # @staticmethod
    # def change_bench_config(ecu:EcuInfo) -> EcuInfo:
    #     ecu.domain.single_bgm = True
    #     ecu.domain.two_domain = False
    #     ecu.tc_config["dut_ecu"] = ["BGM"]
    #     return ecu

    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.dut_name = "LCUL"
        self.src_ip = "172.12.5.1"

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)
        

    @pytest.mark.full
    @allure.title("100286_LCUL_DPOD_LCULCANFD1通道_丢包率测试")
    def test_caseid_100286(self):

        channel_name = "lcu_l_canfd1"
        send_node_name = "DPOD"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100285_LCUL_DRMFL_LCULCANFD1通道_丢包率测试")
    def test_caseid_100285(self):

        channel_name = "lcu_l_canfd1"
        send_node_name = "DRMFL"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100284_LCUL_DRMRL_LCULCANFD1通道_丢包率测试")
    def test_caseid_100284(self):

        channel_name = "lcu_l_canfd1"
        send_node_name = "DRMRL"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100283_LCUL_ETC_LCULCANFD1通道_丢包率测试")
    def test_caseid_100283(self):

        channel_name = "lcu_l_canfd1"
        send_node_name = "ETC"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100282_LCUL_LPOD_LCULCANFD1通道_丢包率测试")
    def test_caseid_100282(self):

        channel_name = "lcu_l_canfd1"
        send_node_name = "LPOD"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100272_LCUL_BMSF_LCULCANFD2通道_丢包率测试")
    def test_caseid_100272(self):

        channel_name = "lcu_l_canfd2"
        send_node_name = "BMSF"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100271_LCUL_CRCM_LCULCANFD2通道_丢包率测试")
    def test_caseid_100271(self):

        channel_name = "lcu_l_canfd2"
        send_node_name = "CRCM"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100270_LCUL_EPM_LCULCANFD2通道_丢包率测试")
    def test_caseid_100270(self):

        channel_name = "lcu_l_canfd2"
        send_node_name = "EPM"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100269_LCUL_ETC_LCULCANFD2通道_丢包率测试")
    def test_caseid_100269(self):

        channel_name = "lcu_l_canfd2"
        send_node_name = "ETC"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100268_LCUL_PNG1_LCULCANFD2通道_丢包率测试")
    def test_caseid_100268(self):

        channel_name = "lcu_l_canfd2"
        send_node_name = "PNG1"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100267_LCUL_RML_LCULCANFD2通道_丢包率测试")
    def test_caseid_100267(self):

        channel_name = "lcu_l_canfd2"
        send_node_name = "RML"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100266_LCUL_SWTL_LCULCANFD2通道_丢包率测试")
    def test_caseid_100266(self):

        channel_name = "lcu_l_canfd2"
        send_node_name = "SWTL"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100265_LCUL_SWTR_LCULCANFD2通道_丢包率测试")
    def test_caseid_100265(self):

        channel_name = "lcu_l_canfd2"
        send_node_name = "SWTR"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100264_LCUL_TRM_LCULCANFD2通道_丢包率测试")
    def test_caseid_100264(self):

        channel_name = "lcu_l_canfd2"
        send_node_name = "TRM"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100257_LCUL_ETC_LCULCANFD3通道_丢包率测试")
    def test_caseid_100257(self):

        channel_name = "lcu_l_canfd3"
        send_node_name = "ETC"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100256_LCUL_HCML_LCULCANFD3通道_丢包率测试")
    def test_caseid_100256(self):

        channel_name = "lcu_l_canfd3"
        send_node_name = "HCML"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100255_LCUL_HCMR_LCULCANFD3通道_丢包率测试")
    def test_caseid_100255(self):

        channel_name = "lcu_l_canfd3"
        send_node_name = "HCMR"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100254_LCUL_LCUR_LCULCANFD3通道_丢包率测试")
    def test_caseid_100254(self):

        channel_name = "lcu_l_canfd3"
        send_node_name = "LCUR"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100253_LCUL_RCML_LCULCANFD3通道_丢包率测试")
    def test_caseid_100253(self):

        channel_name = "lcu_l_canfd3"
        send_node_name = "RCML"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100252_LCUL_RCMR_LCULCANFD3通道_丢包率测试")
    def test_caseid_100252(self):

        channel_name = "lcu_l_canfd3"
        send_node_name = "RCMR"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100244_LCUL_LCULLIN1通道_丢包率测试")
    def test_caseid_100244(self):

        channel_name = "lcu_l_lin1"
        send_node_name = None
        un_packet_id_list = [22,23,18,19,20,13,15,10,12,1,2]

        self.mix.check_packet_loss_rate(channel_name, send_node_name,src_ip=self.src_ip,un_packet_id_list=un_packet_id_list)

    @pytest.mark.full
    @allure.title("100243_LCUL_LCULLIN2通道_丢包率测试")
    def test_caseid_100243(self):

        channel_name = "lcu_l_lin2"
        send_node_name = None
        un_packet_id_list = [19,20,16,17,10,11,3,4,0,1]

        self.mix.check_packet_loss_rate(channel_name, send_node_name,src_ip=self.src_ip,un_packet_id_list=un_packet_id_list)

    @pytest.mark.full
    @allure.title("100242_LCUL_LCULLIN3通道_丢包率测试")
    def test_caseid_100242(self):
        
        channel_name = "lcu_l_lin3"
        send_node_name = None
        un_packet_id_list = []

        self.mix.check_packet_loss_rate(channel_name, send_node_name,src_ip=self.src_ip,un_packet_id_list=un_packet_id_list)

    @pytest.mark.full
    @allure.title("100241_LCUL_LCULLIN4通道_丢包率测试")
    def test_caseid_100241(self):
        
        channel_name = "lcu_l_lin4"
        send_node_name = None
        un_packet_id_list = []

        self.mix.check_packet_loss_rate(channel_name, send_node_name,src_ip=self.src_ip,un_packet_id_list=un_packet_id_list)

    @pytest.mark.full
    @allure.title("100240_LCUL_ALMLIN1通道_丢包率测试")
    def test_caseid_100240(self):
        
        channel_name = "lcu_l_alm_lin1"
        send_node_name = None
        un_packet_id_list = [1,2,3,4,5,6,7,8,9,10]

        self.mix.check_packet_loss_rate(channel_name, send_node_name,src_ip=self.src_ip,un_packet_id_list=un_packet_id_list)

    @pytest.mark.full
    @allure.title("100239_LCUL_ALMLIN2通道_丢包率测试")
    def test_caseid_100239(self):
        
        channel_name = "lcu_l_alm_lin2"
        send_node_name = None
        un_packet_id_list = [1,2,3,4,5,6,7,8,9,10]

        self.mix.check_packet_loss_rate(channel_name, send_node_name,src_ip=self.src_ip,un_packet_id_list=un_packet_id_list)

    @pytest.mark.full
    @allure.title("100238_LCUL_ALMLIN3通道_丢包率测试")
    def test_caseid_100238(self):
        
        channel_name = "lcu_l_alm_lin3"
        send_node_name = None
        un_packet_id_list = [1,2,3,4,5,6,7,8,9,10]

        self.mix.check_packet_loss_rate(channel_name, send_node_name,src_ip=self.src_ip,un_packet_id_list=un_packet_id_list)
