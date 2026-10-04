"""
@File        : test_cdd_function.py
@Author      : xiaoqiang.hu@jiduauto.com
@Time        : 2024/10/23 15:12
@Description : cdd 打包的相关用例

"""
import pytest
import allure
from scapy.all import *
from datetime import datetime
from xat_ecu.legacy.common.logger import logger
from xat_cases.dp2.cd_soc.case_helper.test_abc_base import TestABCBase
from framework.automotive.utils.data_type import EcuInfo
# from ecu_simulator.interface.cd_soc.cd_soc_ssh import CD_SOC_SSH


@allure.feature("MCU 基础平台/CDD打包功能")
@allure.story("CDD功能用例")
class TestCddFunction(TestABCBase):
    # @staticmethod
    # def change_bench_config(ecu:EcuInfo) -> EcuInfo:
    #     ecu.domain.single_bgm = True
    #     ecu.domain.two_domain = False
    #     ecu.tc_config["dut_ecu"] = ["BGM"]
    #     return ecu

    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.dut_name = "CCUMCUCD"
        # self.cd_soc_ssh = CD_SOC_SSH(ecu)
        # self.cd_soc_ssh._init_cd_soc_tcpdump()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.smoke
    @allure.title("100331_CCUCDMCU_Chassis2canFD通道_BCU2数据上传")
    def test_caseid_100331(self):

        channel_name = "chassis2canfd"
        send_node_name = "BCU2"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100330_CCUCDMCU_Chassis2canFD通道_IEM数据上传")
    def test_caseid_100330(self):

        channel_name = "chassis2canfd"
        send_node_name = "IEM"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100329_CCUCDMCU_Chassis2canFD通道_MGM数据上传")
    def test_caseid_100329(self):

        channel_name = "chassis2canfd"
        send_node_name = "MGM"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100328_CCUCDMCU_Chassis2canFD通道_PSCM2数据上传")
    def test_caseid_100328(self):
        
        channel_name = "chassis2canfd"
        send_node_name = "PSCM2"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100327_CCUCDMCU_Chassis2canFD通道_VCU数据上传")
    def test_caseid_100327(self):
        
        channel_name = "chassis2canfd"
        send_node_name = "VCU"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100343_CCUCDMCU_InfoCANFD通道_BNCM数据上传")
    def test_caseid_100343(self):
        
        channel_name = "infocanfd"
        send_node_name = "BNCM"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100342_CCUCDMCU_InfoCANFD通道_CD数据上传")
    def test_caseid_100342(self):
        
        channel_name = "infocanfd"
        send_node_name = "CD"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100341_CCUCDMCU_InfoCANFD通道_DRF数据上传")
    def test_caseid_100341(self):
        
        channel_name = "infocanfd"
        send_node_name = "DRF"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100340_CCUCDMCU_InfoCANFD通道_ETCM数据上传")
    def test_caseid_100340(self):
        
        channel_name = "infocanfd"
        send_node_name = "ETCM"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100339_CCUCDMCU_InfoCANFD通道_NKR数据上传")
    def test_caseid_100339(self):
        
        channel_name = "infocanfd"
        send_node_name = "NKR"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100338_CCUCDMCU_InfoCANFD通道_TPM数据上传")
    def test_caseid_100338(self):
        
        channel_name = "infocanfd"
        send_node_name = "TPM"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100337_CCUCDMCU_InfoCANFD通道_WPC2数据上传")
    def test_caseid_100337(self):
        
        channel_name = "infocanfd"
        send_node_name = "WPC2"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100336_CCUCDMCU_InfoCANFD通道_WPC3数据上传")
    def test_caseid_100336(self):
        
        channel_name = "infocanfd"
        send_node_name = "WPC3"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100326_CCUCDMCU_PropulsionCANFD通道_BCU1数据上传")
    def test_caseid_100326(self):
        
        channel_name = "propulsioncanfd"
        send_node_name = "BCU1"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100325_CCUCDMCU_PropulsionCANFD通道_BCU2数据上传")
    def test_caseid_100325(self):
        
        channel_name = "propulsioncanfd"
        send_node_name = "BCU2"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100324_CCUCDMCU_PropulsionCANFD通道_BECM数据上传")
    def test_caseid_100324(self):
        
        channel_name = "propulsioncanfd"
        send_node_name = "BECM"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100323_CCUCDMCU_PropulsionCANFD通道_CCUMCUAD数据上传")
    def test_caseid_100323(self):
        
        channel_name = "propulsioncanfd"
        send_node_name = "CCUMCUAD"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100322_CCUCDMCU_PropulsionCANFD通道_EGSM数据上传")
    def test_caseid_100322(self):
        
        channel_name = "propulsioncanfd"
        send_node_name = "EGSM"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100321_CCUCDMCU_PropulsionCANFD通道_IEM数据上传")
    def test_caseid_100321(self):
        
        channel_name = "propulsioncanfd"
        send_node_name = "IEM"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100320_CCUCDMCU_PropulsionCANFD通道_MGM数据上传")
    def test_caseid_100320(self):
        
        channel_name = "propulsioncanfd"
        send_node_name = "MGM"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100319_CCUCDMCU_PropulsionCANFD通道_ODP数据上传")
    def test_caseid_100319(self):
        
        channel_name = "propulsioncanfd"
        send_node_name = "ODP"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100318_CCUCDMCU_PropulsionCANFD通道_SRS数据上传")
    def test_caseid_100318(self):
        
        channel_name = "propulsioncanfd"
        send_node_name = "SRS"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100317_CCUCDMCU_PropulsionCANFD通道_VCU数据上传")
    def test_caseid_100317(self):
        
        channel_name = "propulsioncanfd"
        send_node_name = "VCU"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100335_CCUCDMCU_PublicCANFD通道_CCUMCUAD数据上传")
    def test_caseid_100335(self):
        
        channel_name = "publiccanfd"
        send_node_name = "CCUMCUAD"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100334_CCUCDMCU_PublicCANFD通道_LCUL数据上传")
    def test_caseid_100334(self):
        
        channel_name = "publiccanfd"
        send_node_name = "LCUL"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100333_CCUCDMCU_PublicCANFD通道_LCUR数据上传")
    def test_caseid_100333(self):
        
        channel_name = "publiccanfd"
        send_node_name = "LCUR"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100332_CCUCDMCU_PublicCANFD通道_VCU数据上传")
    def test_caseid_100332(self):
        
        channel_name = "publiccanfd"
        send_node_name = "VCU"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.sanity
    @allure.title("100316_校验打包数据内容结束符为0xFE")
    def test_caseid_100316(self, do_assert=True):
        
        packet_list, data_list = self.mix.send_all_node(tcpdump_time=10)
        ret_code = self.mix.check_udp_end_string(packet_list)
        if do_assert:
            assert ret_code, "结束符号不对！"

    @pytest.mark.sanity
    @allure.title("100312_校验打包数据长度<=1400byte")
    def test_caseid_100312(self, do_assert=True):
        
        packet_list, data_list = self.mix.send_all_node(tcpdump_time=10)
        ret_code = self.mix.check_udp_packet_len(packet_list)
        if do_assert:
            assert ret_code, "打包数据长度不对！"

    @pytest.mark.sanity
    @allure.title("100311_校验UDP报文IP及端口")
    def test_caseid_100311(self, do_assert=True):
        
        packet_list, data_list = self.mix.send_all_node(tcpdump_time=10)
        ret_code = self.mix.check_udp_packet_ip_port(packet_list)
        if do_assert:
            assert ret_code, "UDP报文IP和端口不对！"

    @pytest.mark.sanity
    @allure.title("100314_校验打包数据全局时钟格式")
    def test_caseid_100314(self, do_assert=True):
        
        packet_list, data_list = self.mix.send_all_node(tcpdump_time=10)
        ret_code = self.mix.check_udp_packet_global_timestamp(data_list)
        if do_assert:
            assert ret_code, "打包数据全局时钟格式不对！"

    @pytest.mark.sanity
    @allure.title("100315_校验打包数据报文长度一致")
    def test_caseid_100315(self, do_assert=True):
        
        packet_list, data_list = self.mix.send_all_node(tcpdump_time=10)
        ret_code = self.mix.check_udp_packet_msglen(data_list)
        if do_assert:
            assert ret_code, "打包数据报文长度不对！"

    @pytest.mark.sanity
    @allure.title("100313_校验打包数据报文内容一致")
    def test_caseid_100313(self, do_assert=True):

        errno_list = []
        
        packet_list, data_list = self.mix.send_all_node(tcpdump_time=10)
        #按照ID进行分类
        # id 分类
        data_info_dict = {}
        for item in data_list:
            if item.get("channel_name").lower() != "backbonefr":
                item_id = item.get("msg_id")
            else:
                item_id = (item.get("msg_id"), item.get("msg_base_cycle"), item.get("msg_repetition"))
            #将相同ID的报文内容，添加到同一个列表中，在字典中{ID:["","",""]}
            if item_id in data_info_dict:
                data_info_dict[item_id].append(item.get("msg_content"))
            else:
                data_info_dict[item_id] = [item.get("msg_content")]

        # 获取当前脚本的绝对路径
        current_script_path = os.path.abspath(__file__)
        # 获取当前脚本所在的目录（子目录）
        current_directory = os.path.dirname(current_script_path) 
        # 获取父目录的路径
        parent_directory = os.path.dirname(current_directory)
        parent_directory = os.path.dirname(parent_directory)
        parent_directory = os.path.dirname(parent_directory)
        # can asc文件路径
        can_asc_file_path = os.path.join(parent_directory, 'Can.asc')
        can_msg_list = self.mix.read_asc_file(can_asc_file_path)
        if len(can_msg_list) != 0:
            can_msg_list = can_msg_list[-100:]
            can_error_list = self.mix.check_udp_packet_msgcontent(can_msg_list,data_info_dict)
            errno_list.extend(can_error_list)
        else:
            logger.error("can asc file is empty")
        # lin asc文件路径
        lin_asc_file_path = os.path.join(parent_directory, 'Lin.asc')
        if os.path.exists(lin_asc_file_path):
            lin_msg_list = self.mix.read_asc_file(lin_asc_file_path)
            if len(lin_msg_list) != 0:
                lin_msg_list = lin_msg_list[-100:]
                lin_error_list = self.mix.check_udp_packet_msgcontent(lin_msg_list,data_info_dict)
                errno_list.extend(lin_error_list)
            else:
                logger.info("lin asc file is empty")
        else:
            logger.info("lin asc file is not exist")

        ret_code = True if not errno_list else False
        if do_assert:
            assert ret_code, "打包数据报文内容不对！"

    # @pytest.mark.sanity 不满足测试条件，CDD打包的全局时钟未同步
    # @allure.title("100275_打包周期稳定性_报文时间戳与全局时钟<=10ms")
    # def test_caseid_100275(self, do_assert=True):

    #     "发送一帧CAN报文，解析仿真报文的时间戳与全局时钟的时间戳在10ms范围内"
        
    #     packet_list, data_list = self.mix.send_special_msg("发送一帧报文")
    #     ret_code = self.mix.check_can_udp_timestamp(packet_list)
    #     if do_assert:
    #         assert ret_code, "CAN和UDP报文时间差>10ms!"

    @pytest.mark.sanity
    @allure.title("100310_打包周期稳定性_UDP报文时间戳差值小于10ms")
    def test_caseid_100310(self, do_assert=True):

        "仿真大量的CAN数据，确保10ms内每包数据达到1400bytes"

        packet_list, data_list = self.mix.send_all_node(tcpdump_time=60)
        ret_code = self.mix.check_udp_cycle(packet_list, test_type ="udp_timediff<10ms")
        if do_assert:
            assert ret_code, "UDP报文之间时间差>=10ms！"

    @pytest.mark.sanity
    @allure.title("100309_打包周期稳定性_UDP报文时间戳差值等于10ms")
    def test_caseid_100309(self, do_assert=True):

        "仿真少量的CAN数据，确保10ms内有数据且每包数据小于1400bytes"
        
        packet_list, data_list = self.mix.send_special_msg("不仿真报文")
        ret_code = self.mix.check_udp_cycle(packet_list, test_type ="udp_timediff=10ms")
        if do_assert:
            assert ret_code, "UDP打包周期稳定性不符合要求,UDP报文之间时间差!=10ms！"

    @pytest.mark.sanity
    @allure.title("100273_校验打包数据中毫秒时间戳差值<=10ms")
    def test_caseid_100273(self, do_assert=True):

        "仿真大量报文，解析UDP报文中打包数据的毫秒时间戳差值<=10ms"
        
        packet_list, data_list = self.mix.send_all_node(tcpdump_time=10)
        ret_code = self.mix.check_udp_packet_mstimestamp(data_list, test_type ="mstimestamp_timediff<=10ms")
        if do_assert:
            assert ret_code, "打包数据中毫秒时间戳差值>10ms！"
