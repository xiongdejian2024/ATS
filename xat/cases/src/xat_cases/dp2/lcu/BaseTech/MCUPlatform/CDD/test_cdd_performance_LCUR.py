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
        self.dut_name = "LCUR"
        self.src_ip = "172.12.5.2"

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)
        

    @pytest.mark.full
    @allure.title("100232_LCUR_DRMFR_LCURCANFD1通道_丢包率测试")
    def test_caseid_100232(self):

        channel_name = "lcu_r_canfd1"
        send_node_name = "DRMFR"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100231_LCUR_DRMRR_LCURCANFD1通道_丢包率测试")
    def test_caseid_100231(self):

        channel_name = "lcu_r_canfd1"
        send_node_name = "DRMRR"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100230_LCUR_ETC_LCURCANFD1通道_丢包率测试")
    def test_caseid_100230(self):

        channel_name = "lcu_r_canfd1"
        send_node_name = "ETC"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100229_LCUR_PPOD_LCURCANFD1通道_丢包率测试")
    def test_caseid_100229(self):

        channel_name = "lcu_r_canfd1"
        send_node_name = "PPOD"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100228_LCUR_RPOD_LCURCANFD1通道_丢包率测试")
    def test_caseid_100228(self):

        channel_name = "lcu_r_canfd1"
        send_node_name = "RPOD"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100225_LCUR_BMSR_LCURCANFD2通道_丢包率测试")
    def test_caseid_100225(self):

        channel_name = "lcu_r_canfd2"
        send_node_name = "BMSR"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100224_LCUR_ETC_LCURCANFD2通道_丢包率测试")
    def test_caseid_100224(self):

        channel_name = "lcu_r_canfd2"
        send_node_name = "ETC"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100217_LCUR_ETC_LCURCANFD3通道_丢包率测试")
    def test_caseid_100217(self):

        channel_name = "lcu_r_canfd3"
        send_node_name = "ETC"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100216_LCUR_HCML_LCURCANFD3通道_丢包率测试")
    def test_caseid_100216(self):

        channel_name = "lcu_r_canfd3"
        send_node_name = "HCML"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100215_LCUR_HCMR_LCURCANFD3通道_丢包率测试")
    def test_caseid_100215(self):

        channel_name = "lcu_r_canfd3"
        send_node_name = "HCMR"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100214_LCUR_LCUL_LCURCANFD3通道_丢包率测试")
    def test_caseid_100214(self):

        channel_name = "lcu_r_canfd3"
        send_node_name = "LCUL"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100213_LCUR_RCML_LCURCANFD3通道_丢包率测试")
    def test_caseid_100213(self):

        channel_name = "lcu_r_canfd3"
        send_node_name = "RCML"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100212_LCUR_RCMR_LCURCANFD3通道_丢包率测试")
    def test_caseid_100212(self):

        channel_name = "lcu_r_canfd3"
        send_node_name = "RCMR"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name,src_ip=self.src_ip)

    @pytest.mark.full
    @allure.title("100204_LCUR_LCURLIN1通道_丢包率测试")
    def test_caseid_100204(self):
        
        channel_name = "lcu_r_lin1"
        send_node_name = None
        un_packet_id_list = [0,1,3,4,6,7,9,10,12,13,15,16,18,19]

        self.mix.check_packet_loss_rate(channel_name, send_node_name,src_ip=self.src_ip, un_packet_id_list=un_packet_id_list)

    @pytest.mark.full
    @allure.title("100203_LCUR_LCURLIN2通道_丢包率测试")
    def test_caseid_100203(self):
        
        channel_name = "lcu_r_lin2"
        send_node_name = None
        un_packet_id_list = [0,1,3,4,6,7,11,12,14,15,17,18]

        self.mix.check_packet_loss_rate(channel_name, send_node_name,src_ip=self.src_ip, un_packet_id_list=un_packet_id_list)

    @pytest.mark.full
    @allure.title("100202_LCUR_LCURLIN3通道_丢包率测试")
    def test_caseid_100202(self):
        
        channel_name = "lcu_r_lin3"
        send_node_name = None
        un_packet_id_list = [0,1,4,5,7,8,12,13]

        self.mix.check_packet_loss_rate(channel_name, send_node_name,src_ip=self.src_ip, un_packet_id_list=un_packet_id_list)

    @pytest.mark.full
    @allure.title("100201_LCUR_LCURLIN4通道_丢包率测试")
    def test_caseid_100201(self):
        
        channel_name = "lcu_r_lin4"
        send_node_name = None
        un_packet_id_list = [0,1,5,6,12,13,15,16,18,19]

        self.mix.check_packet_loss_rate(channel_name, send_node_name,src_ip=self.src_ip, un_packet_id_list=un_packet_id_list)

    @pytest.mark.full
    @allure.title("100200_LCUR_LCURALMLIN1通道_丢包率测试")
    def test_caseid_100200(self):
        
        channel_name = "lcu_r_alm_lin1"
        send_node_name = None
        un_packet_id_list = [1,2,3,4,5,6,7,8,9,10]

        self.mix.check_packet_loss_rate(channel_name, send_node_name,src_ip=self.src_ip, un_packet_id_list=un_packet_id_list)

    @pytest.mark.full
    @allure.title("100199_LCUR_LCURALMLIN2通道_丢包率测试")
    def test_caseid_100199(self):
        
        channel_name = "lcu_r_alm_lin2"
        send_node_name = None
        un_packet_id_list = [1,2,3,4,5,6,7,8,9,10]

        self.mix.check_packet_loss_rate(channel_name, send_node_name,src_ip=self.src_ip, un_packet_id_list=un_packet_id_list)

    @pytest.mark.full
    @allure.title("100198_LCUR_LCURALMLIN3通道_丢包率测试")
    def test_caseid_100198(self):
        
        channel_name = "lcu_r_alm_lin3"
        send_node_name = None
        un_packet_id_list = [1,2,3,4,5,6,7,8,9,10]

        self.mix.check_packet_loss_rate(channel_name, send_node_name,src_ip=self.src_ip, un_packet_id_list=un_packet_id_list)
