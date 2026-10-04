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
from xat_cases.dp2.lcu.case_helper.test_abc_base import TestABCBase
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
        # self.cd_soc_ssh = CD_SOC_SSH(ecu)
        # self.cd_soc_ssh._init_cd_soc_tcpdump()
        self.dut_name = "LCUL"
        self.src_ip = "172.16.5.1"

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.smoke
    @allure.title("100291_LCUL_DPOD_LCULCANFD1通道_MsgID校验")
    def test_caseid_100291(self):

        channel_name = "lcu_l_canfd1"
        send_node_name = "DPOD"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100290_LCUL_DRMFL_LCULCANFD1通道_MsgID校验")
    def test_caseid_100290(self):

        channel_name = "lcu_l_canfd1"
        send_node_name = "DRMFL"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100289_LCUL_DRMRL_LCULCANFD1通道_MsgID校验")
    def test_caseid_100289(self):

        channel_name = "lcu_l_canfd1"
        send_node_name = "DRMRL"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100288_LCUL_ETC_LCULCANFD1通道_MsgID校验")
    def test_caseid_100288(self):
        
        channel_name = "lcu_l_canfd1"
        send_node_name = "ETC"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100287_LCUL_LPOD_LCULCANFD1通道_MsgID校验")
    def test_caseid_100287(self):
        
        channel_name = "lcu_l_canfd1"
        send_node_name = "LPOD"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100281_LCUL_BMSF_LCULCANFD2通道_MsgID校验")
    def test_caseid_100281(self):
        
        channel_name = "lcu_l_canfd2"
        send_node_name = "BMSF"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100280_LCUL_CRCM_LCULCANFD2通道_MsgID校验")
    def test_caseid_100280(self):
        
        channel_name = "lcu_l_canfd2"
        send_node_name = "CRCM"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100279_LCUL_EPM_LCULCANFD2通道_MsgID校验")
    def test_caseid_100279(self):
        
        channel_name = "lcu_l_canfd2"
        send_node_name = "EPM"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100278_LCUL_ETC_LCULCANFD2通道_MsgID校验")
    def test_caseid_100278(self):
        
        channel_name = "lcu_l_canfd2"
        send_node_name = "ETC"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100277_LCUL_PNG1_LCULCANFD2通道_MsgID校验")
    def test_caseid_100277(self):
        
        channel_name = "lcu_l_canfd2"
        send_node_name = "PNG1"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100276_LCUL_RML_LCULCANFD2通道_MsgID校验")
    def test_caseid_100276(self):
        
        channel_name = "lcu_l_canfd2"
        send_node_name = "RML"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100275_LCUL_SWTL_LCULCANFD2通道_MsgID校验")
    def test_caseid_100275(self):
        
        channel_name = "lcu_l_canfd2"
        send_node_name = "SWTL"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100274_LCUL_SWTR_LCULCANFD2通道_MsgID校验")
    def test_caseid_100274(self):
        
        channel_name = "lcu_l_canfd2"
        send_node_name = "SWTR"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100273_LCUL_TRM_LCULCANFD2通道_MsgID校验")
    def test_caseid_100273(self):
        
        channel_name = "lcu_l_canfd2"
        send_node_name = "TRM"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100263_LCUL_ETC_LCULCANFD3通道_MsgID校验")
    def test_caseid_100263(self):
        
        channel_name = "lcu_l_canfd3"
        send_node_name = "ETC"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100262_LCUL_HCML_LCULCANFD3通道_MsgID校验")
    def test_caseid_100262(self):
        
        channel_name = "lcu_l_canfd3"
        send_node_name = "HCML"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100261_LCUL_HCMR_LCULCANFD3通道_MsgID校验")
    def test_caseid_100261(self):
        
        channel_name = "lcu_l_canfd3"
        send_node_name = "HCMR"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100260_LCUL_LCUR_LCULCANFD3通道_MsgID校验")
    def test_caseid_100260(self):
        
        channel_name = "lcu_l_canfd3"
        send_node_name = "LCUR"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100259_LCUL_RCML_LCULCANFD3通道_MsgID校验")
    def test_caseid_100259(self):
        
        channel_name = "lcu_l_canfd3"
        send_node_name = "RCML"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100258_LCUL_RCMR_LCULCANFD3通道_MsgID校验")
    def test_caseid_100258(self):
        
        channel_name = "lcu_l_canfd3"
        send_node_name = "RCMR"

        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name)

    @pytest.mark.smoke
    @allure.title("100251_LCUL_LCULLIN1通道_MsgID校验")
    def test_caseid_100251(self):
        
        channel_name = "lcu_l_lin1"
        send_node_name = None
        un_packet_id_list = [22,23,18,19,20,13,15,10,12,1,2]
        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name, un_packet_id_list=un_packet_id_list)

    @pytest.mark.smoke
    @allure.title("100250_LCUL_LCULLIN2通道_MsgID校验")
    def test_caseid_100250(self):
        
        channel_name = "lcu_l_lin2"
        send_node_name = None
        un_packet_id_list = [19,20,16,17,10,11,3,4,0,1]
        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name, un_packet_id_list=un_packet_id_list)

    @pytest.mark.smoke
    @allure.title("100249_LCUL_LCULLIN3通道_MsgID校验")
    def test_caseid_100249(self):
        
        channel_name = "lcu_l_lin3"
        send_node_name = None
        un_packet_id_list = []
        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name, un_packet_id_list=un_packet_id_list)

    @pytest.mark.smoke
    @allure.title("100248_LCUL_LCULLIN4通道_MsgID校验")
    def test_caseid_100248(self):
        
        channel_name = "lcu_l_lin4"
        send_node_name = None
        un_packet_id_list = []
        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name, un_packet_id_list=un_packet_id_list)

    @pytest.mark.smoke
    @allure.title("100247_LCUL_LCULALMLIN1通道_MsgID校验")
    def test_caseid_100247(self):
        
        channel_name = "lcu_l_alm_lin1"
        send_node_name = None
        un_packet_id_list = [1,2,3,4,5,6,7,8,9,10]
        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name, un_packet_id_list=un_packet_id_list)

    @pytest.mark.smoke
    @allure.title("100246_LCUL_LCULALMLIN2通道_MsgID校验")
    def test_caseid_100246(self):
        
        channel_name = "lcu_l_alm_lin2"
        send_node_name = None
        un_packet_id_list = [1,2,3,4,5,6,7,8,9,10]
        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name, un_packet_id_list=un_packet_id_list)

    @pytest.mark.smoke
    @allure.title("100245_LCUL_LCULALMLIN3通道_MsgID校验")
    def test_caseid_100245(self):
        
        channel_name = "lcu_l_alm_lin3"
        send_node_name = None
        un_packet_id_list = [1,2,3,4,5,6,7,8,9,10]
        self.mix.check_packet_msg_id(self.dut_name, channel_name, send_node_name, un_packet_id_list=un_packet_id_list)

    @pytest.mark.sanity
    @allure.title("100181_LCUL_UDP结束符0xFE")
    def test_caseid_100181(self, do_assert=True):
        
        packet_list, data_list = self.mix.send_all_node(tcpdump_time=10,src_ip = self.src_ip)
        ret_code = self.mix.check_udp_end_string(packet_list)
        if do_assert:
            assert ret_code, "结束符号不对！"

    @pytest.mark.sanity
    @allure.title("100183_LCUL_UDPPayload长度小于或等于1400字节")
    def test_caseid_100183(self, do_assert=True):
        
        packet_list, data_list = self.mix.send_all_node(tcpdump_time=10,src_ip = self.src_ip)
        ret_code = self.mix.check_udp_packet_len(packet_list)
        if do_assert:
            assert ret_code, "UDPPayload长度不对！"

    @pytest.mark.sanity
    @allure.title("100195_LCUL_UDP报文IP和端口")
    def test_caseid_100195(self, do_assert=True):
        
        packet_list, data_list = self.mix.send_all_node(tcpdump_time=10,src_ip = self.src_ip)
        ret_code = self.mix.check_udp_packet_ip_port(packet_list)
        if do_assert:
            assert ret_code, "UDP报文IP和端口不对！"

    @pytest.mark.sanity
    @allure.title("100197_LCUL_UDP报文全局时钟格式")
    def test_caseid_100197(self, do_assert=True):
        
        packet_list, data_list = self.mix.send_all_node(tcpdump_time=10,src_ip = self.src_ip)
        ret_code = self.mix.check_udp_packet_global_timestamp(data_list)
        if do_assert:
            assert ret_code, "打包数据全局时钟格式不对！"

    @pytest.mark.sanity
    @allure.title("100185_LCUL_打包数据msg长度是否一致")
    def test_caseid_100185(self, do_assert=True):
        
        packet_list, data_list = self.mix.send_all_node(tcpdump_time=10,src_ip = self.src_ip)
        ret_code = self.mix.check_udp_packet_msglen(data_list)
        if do_assert:
            assert ret_code, "打包数据报文长度不对！"

    @pytest.mark.sanity
    @allure.title("100187_LCUL_打包数据msg内容是否一致")
    def test_caseid_100187(self, do_assert=True):

        error_list = []
        
        packet_list, data_list = self.mix.send_all_node(tcpdump_time=30)
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
            error_list.extend(can_error_list)
        else:
            logger.error("can asc file is empty")
        # lin asc文件路径
        lin_asc_file_path = os.path.join(parent_directory, 'Lin.asc')
        if os.path.exists(lin_asc_file_path):
            lin_msg_list = self.mix.read_asc_file(lin_asc_file_path)
            if len(lin_msg_list) != 0:
                lin_msg_list = lin_msg_list[-100:]
                lin_error_list = self.mix.check_udp_packet_msgcontent(lin_msg_list,data_info_dict)
                error_list.extend(lin_error_list)
            else:
                logger.error("lin asc file is empty")
        else:
            logger.error("lin asc file is not exist")

        ret_code = True if not error_list else False
        if do_assert:
            assert ret_code, "打包数据报文内容不对！"

    @pytest.mark.sanity
    @allure.title("100179_LCUL_报文时间戳与全局时钟<=10ms")
    def test_caseid_100179(self, do_assert=True):

        "发送一帧CAN报文，解析仿真报文的时间戳与全局时钟的时间戳在10ms范围内"
        
        packet_list, data_list = self.mix.send_special_msg("发送一帧报文")
        ret_code = self.mix.check_can_udp_timestamp(packet_list)
        if do_assert:
            assert ret_code, "CAN和UDP报文时间差>10ms!"

    @pytest.mark.sanity
    @allure.title("100191_LCUL_打包周期稳定性_UDP报文时间戳差值小于10ms")
    def test_caseid_100191(self, do_assert=True):

        "仿真大量的CAN数据，确保10ms内每包数据达到1400bytes"

        packet_list, data_list = self.mix.send_all_node(tcpdump_time=60,src_ip = self.src_ip)
        ret_code = self.mix.check_udp_cycle(packet_list, test_type ="udp_timediff<10ms")
        if do_assert:
            assert ret_code, "UDP报文之间时间差>=10ms！"

    @pytest.mark.sanity
    @allure.title("100193_LCUL_打包周期稳定性_UDP报文时间戳差值等于10ms")
    def test_caseid_100193(self, do_assert=True):

        "仿真少量的CAN数据，确保10ms内有数据且每包数据小于1400bytes"
        
        packet_list, data_list = self.mix.send_special_msg("不仿真报文")
        ret_code = self.mix.check_udp_cycle(packet_list, test_type ="udp_timediff=10ms")
        if do_assert:
            assert ret_code, "UDP打包周期稳定性不符合要求,UDP报文之间时间差!=10ms！"

    @pytest.mark.sanity
    @allure.title("100189_LCUL_打包数据中毫秒时间戳差值<=10ms")
    def test_caseid_100189(self, do_assert=True):

        "仿真大量报文，解析UDP报文中同一帧报文的毫秒时间戳差值<=10ms"
        
        packet_list, data_list = self.mix.send_all_node(tcpdump_time=10,src_ip = self.src_ip)
        ret_code = self.mix.check_udp_packet_mstimestamp(data_list, test_type ="mstimestamp_timediff<=10ms")
        if do_assert:
            assert ret_code, "打包数据中毫秒时间戳差值>10ms！"
