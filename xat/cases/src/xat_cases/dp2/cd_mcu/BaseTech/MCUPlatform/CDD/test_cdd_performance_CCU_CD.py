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
from xat_cases.dp2.cd_soc.case_helper.test_abc_base import TestABCBase


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
        self.dut_name = "CCUMCUCD"
        self.src_ip_LCUL = "172.12.5.1"
        self.src_ip_LCUR = "172.12.5.2"

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)
        

    @pytest.mark.full
    @allure.title("100305_CCUCDMCU_InfoCANFD通道_BNCM接收帧数统计")
    def test_caseid_100305(self):

        channel_name = "infocanfd"
        send_node_name = "BNCM"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100304_CCUCDMCU_InfoCANFD通道_CD接收帧数统计")
    def test_caseid_100304(self):

        channel_name = "infocanfd"
        send_node_name = "CD"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100303_CCUCDMCU_InfoCANFD通道_DRF接收帧数统计")
    def test_caseid_100303(self):

        channel_name = "infocanfd"
        send_node_name = "DRF"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100302_CCUCDMCU_InfoCANFD通道_ETCM接收帧数统计")
    def test_caseid_100302(self):

        channel_name = "infocanfd"
        send_node_name = "ETCM"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100301_CCUCDMCU_InfoCANFD通道_NKR接收帧数统计")
    def test_caseid_100301(self):

        channel_name = "infocanfd"
        send_node_name = "NKR"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100300_CCUCDMCU_InfoCANFD通道_TPM接收帧数统计")
    def test_caseid_100300(self):

        channel_name = "infocanfd"
        send_node_name = "TPM"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100299_CCUCDMCU_InfoCANFD通道_WPC2接收帧数统计")
    def test_caseid_100299(self):

        channel_name = "infocanfd"
        send_node_name = "WPC2"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100298_CCUCDMCU_InfoCANFD通道_WPC3接收帧数统计")
    def test_caseid_100298(self):

        channel_name = "infocanfd"
        send_node_name = "WPC3"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100293_CCUCDMCU_Chassis2CANFD通道_BCU2_接收帧数统计")
    def test_caseid_100293(self):

        channel_name = "chassis2canfd"
        send_node_name = "BCU2"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100292_CCUCDMCU_Chassis2CANFD通道_IEM_接收帧数统计")
    def test_caseid_100292(self):

        channel_name = "chassis2canfd"
        send_node_name = "IEM"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100291_CCUCDMCU_Chassis2CANFD通道_MGM_接收帧数统计")
    def test_caseid_100291(self):

        channel_name = "chassis2canfd"
        send_node_name = "MGM"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100290_CCUCDMCU_Chassis2CANFD通道_PSCM2_接收帧数统计")
    def test_caseid_100290(self):

        channel_name = "chassis2canfd"
        send_node_name = "PSCM2"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100289_CCUCDMCU_Chassis2CANFD通道_VCU_接收帧数统计")
    def test_caseid_100289(self):

        channel_name = "chassis2canfd"
        send_node_name = "VCU"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100288_CCUCDMCU_PropulsionCANFD通道_BCU1_接收帧数统计")
    def test_caseid_100288(self):

        channel_name = "propulsioncanfd"
        send_node_name = "BCU1"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100287_CCUCDMCU_PropulsionCANFD通道_BCU2_接收帧数统计")
    def test_caseid_100287(self):

        channel_name = "propulsioncanfd"
        send_node_name = "BCU2"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100286_CCUCDMCU_PropulsionCANFD通道_BECM_接收帧数统计")
    def test_caseid_100286(self):

        channel_name = "propulsioncanfd"
        send_node_name = "BECM"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100285_CCUCDMCU_PropulsionCANFD通道_CCUMCUAD_接收帧数统计")
    def test_caseid_100285(self):

        channel_name = "propulsioncanfd"
        send_node_name = "CCUMCUAD"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100284_CCUCDMCU_PropulsionCANFD通道_EGSM_接收帧数统计")
    def test_caseid_100284(self):

        channel_name = "propulsioncanfd"
        send_node_name = "EGSM"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100283_CCUCDMCU_PropulsionCANFD通道_IEM_接收帧数统计")
    def test_caseid_100283(self):

        channel_name = "propulsioncanfd"
        send_node_name = "IEM"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100282_CCUCDMCU_PropulsionCANFD通道_MGM_接收帧数统计")
    def test_caseid_100282(self):

        channel_name = "propulsioncanfd"
        send_node_name = "MGM"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100281_CCUCDMCU_PropulsionCANFD通道_ODP_接收帧数统计")
    def test_caseid_100281(self):

        channel_name = "propulsioncanfd"
        send_node_name = "ODP"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100280_CCUCDMCU_PropulsionCANFD通道_SRS_接收帧数统计")
    def test_caseid_100280(self):

        channel_name = "propulsioncanfd"
        send_node_name = "SRS"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100279_CCUCDMCU_PropulsionCANFD通道_VCU_接收帧数统计")
    def test_caseid_100279(self):

        channel_name = "propulsioncanfd"
        send_node_name = "VCU"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100297_CCUCDMCU_PublicCANFD通道_CCUMCUAD_接收帧数统计")
    def test_caseid_100297(self):

        channel_name = "publiccanfd"
        send_node_name = "CCUMCUAD"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100296_CCUCDMCU_PublicCANFD通道_LCUL_接收帧数统计")
    def test_caseid_100296(self):

        channel_name = "publiccanfd"
        send_node_name = "LCUL"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100295_CCUCDMCU_PublicCANFD通道_LCUR_接收帧数统计")
    def test_caseid_100295(self):

        channel_name = "publiccanfd"
        send_node_name = "LCUR"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)

    @pytest.mark.full
    @allure.title("100294_CCUCDMCU_PublicCANFD通道_VCU_接收帧数统计")
    def test_caseid_100294(self):

        channel_name = "publiccanfd"
        send_node_name = "VCU"

        self.mix.check_packet_loss_rate(self.dut_name, channel_name, send_node_name)
