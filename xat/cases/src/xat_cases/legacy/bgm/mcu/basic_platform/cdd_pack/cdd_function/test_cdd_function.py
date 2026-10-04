"""
@File        : test_cdd_function.PY
@Author      : O_daidi.liang@external.jiduauto.com
@Time        : 2023/10/31 15:12
@Description : cdd 打包的相关用例

"""

from asyncio import sleep
import pytest
import allure
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_cases.legacy.bgm.mcu.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.mcu.case_helper.mcu_interface import MCU_Interface
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from datetime import datetime
from xat_ecu.legacy.ecu_sim.parse_tb_config import ParseTBConfig
from xat_ecu.legacy.config.path import CONFIG_DIR_PATH
from xat_ecu.legacy.driver.ssh_client import *
from xat_ecu.legacy.driver.ssh_interface import file_download

@pytest.mark.mcu_test
@allure.feature("MCU 基础平台/CDD打包功能")
@allure.story("CDD功能用例")
class TestCddFunction(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        # Code Location
        tb_path = os.path.join(CONFIG_DIR_PATH, "willow_bgm_flash_config.yaml")
        self.result = None
        self.cpu_load = []
        tb_config = ParseTBConfig(tb_path)
        self.sd_test_tb_config = tb_config.yaml_content
        self.sd_test = Sd_Tester(**self.sd_test_tb_config)
        self.sd_test.diagnostic_client_sim_start()
        self.sd_test.tester_present()
        self.sd_test.update_serverdoipid(0x1002)
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文

            # self.ipdu.pause_all_bus_send()  # 暂停发送
            # self.sd_test_tb_config = self.tc_config

        with allure.step(f"IO控制TCAM下电"):
            self.nucapp.tcam_power_off()
            time.sleep(30)

        self.cdd_parse = MCU_Interface()  # 实例化解析工具的类
        self.bgm_tcpdump = BGM_SSH()  # 实例化
        self.bgm_tcpdump.init_bgm_tcpdump()  # 初始化，只需要执行一次

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # Code Location
        try:
            self.sd_test.send_data([0x22, 0xdb, 0x02])
            self.result = self.sd_test.return_udsdata_and_check_and_print_response_result("发送  22 DB 02")
            self.cpu_load.append(self.result[3:11])
            self.sd_test.send_data([0x22, 0xF1, 0xD5])
            self.result = self.sd_test.return_udsdata_and_check_and_print_response_result("发送  22 F1 D5")
        except Exception as e:
            # self.print_log(e)
            pass

    def after_each_func(self, ecu):
        # Code Location
        super().after_each_func(ecu)

    def after_class(self, ecu):
        # Code Location
        try:
            self.sd_test.stop_tester_present()
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            pass
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        # 删除bgm 内部所有的pcap 包，必须要有的
        self.bgm_tcpdump.delete_bgm_tcpdump_file()
        super().after_class(self, ecu)
        self.ipdu.lin1_reset_wakeup()
        logger.info(f"""CPU load 
                    core0[短周期当前负载平均值：{round(sum([item[0] for item in self.cpu_load]) / len(self.cpu_load), 2)}，
                    短周期峰值负载最大值：{max([item[1] for item in self.cpu_load])},
                    长周期当前负载平均值：{round(sum([item[2] for item in self.cpu_load]) / len(self.cpu_load), 2)},
                    长周期峰值负载最大值：{max([item[3] for item in self.cpu_load])}],
                    core1[短周期当前负载平均值：{round(sum([item[4] for item in self.cpu_load]) / len(self.cpu_load), 2)},
                    短周期峰值负载最大值：{max([item[5] for item in self.cpu_load])},
                    长周期当前负载平均值：{round(sum([item[6] for item in self.cpu_load]) / len(self.cpu_load), 2)},
                    长周期峰值负载最大值：{max([item[7] for item in self.cpu_load])}]"""
                    )
        with allure.step(f"IO控制TCAM上电"):
            self.nucapp.tcam_power_on()
            time.sleep(200)

    def print_log(self, data: str):
        '''
        打印日志
        @param data:
        @return:
        '''
        with allure.step(data):
            logger.info(data)

    def check_bgm_packet_msg_id(self, channel_name, send_node_name, tcpdump_time=10, **kwargs):
        '''
        校验 某个节点的 发送的数据，接收端是否收到
        @param channel_name: 通道   bodycan 等等
        @param send_node_name: 发送节点
        @param recv_node_name: 接收节点
        @param send_type: 发送类型，
        @param tcpdump_time: bgm tcp 抓包时间
        @param do_assert:
        @param kwargs:
        @return:
        '''
        if send_node_name is None:
            send_node_name_log = "所有非BGM节点"
        else:
            send_node_name_log = send_node_name
        # 不能打包的id 列表
        un_packet_id_list = kwargs.get("un_packet_id_list", [])
        self.ipdu.pause_bus_send(channel_name)
        # 开启bgm内部抓包
        bgm_tcpdump_file_path, save_name = self.bgm_tcpdump.start_bgm_tcpdump(iface="eth0")
        # 发送周期数据
        self.ipdu.resume_send_pdu(channel_name, 0x53F)
        # self.ipdu.resume_ecu_send(channel_name, send_node_name)
        # 发送周期数据
        if send_node_name is None:
            self.ipdu.resume_bus_send(channel_name)
        else:
            self.ipdu.resume_ecu_send(channel_name, send_node_name)
        time.sleep(tcpdump_time)
        # 获取  通道所有信息
        bus_send_recv_dict = self.cdd_parse.get_bus_send_recv_info(ipdu=self.ipdu, channel_name=channel_name)
        # 获取非周期发送的收据
        other_send_lis, bgm_send_lis = self.cdd_parse.get_bus_send_msg_info(data_dic=bus_send_recv_dict,
                                                                            send_nodes=send_node_name,
                                                                            send_type="spontaneous")
        # bgm 节点 非周期发送的
        logger.info(f"bgm_send_lis={bgm_send_lis}")
        if str(channel_name).lower() != "backbonefr":
            bmg_send_msg_id_set_all = set([item.get("msg_id") for item in bgm_send_lis if item.get("msg_id")])
        else:
            bmg_send_msg_id_set_all = set(
                [(item.get("msg_id"), item.get("msg_base_cycle"), item.get("msg_repetition")) for item in bgm_send_lis
                 if item.get("msg_id")])

        un_cycle_l0 = list(bmg_send_msg_id_set_all)
        un_cycle_l0.sort()
        self.print_log(
            f"在{channel_name}通道上bgm非周期发送所有数据有{len(un_cycle_l0)}个，id>{un_cycle_l0}")

        # 非bgm 节点 非周期发送的
        logger.info(f"other_send_lis..{other_send_lis}")
        if str(channel_name).lower() != "backbonefr":
            send_msg_id_set_all = set([item.get("msg_id") for item in other_send_lis if item.get("msg_id")])
        else:
            send_msg_id_set_all = set(
                [(item.get("msg_id"), item.get("msg_base_cycle"), item.get("msg_repetition")) for item in other_send_lis
                 if
                 item.get("msg_id")])

        un_cycle_l = list(send_msg_id_set_all)
        un_cycle_l.sort()
        self.print_log(
            f"在{channel_name}通道上{send_node_name_log} 非周期发送所有数据有{len(un_cycle_l)}个，id>{un_cycle_l}")
        #
        if send_msg_id_set_all:
            # 获取长度
            un_cycle_send_msg_id_len_list = set(
                [(item.get("msg_id"), item.get("msg_length")) for item in other_send_lis if item.get("msg_id")])
            # 发送 非周期数据,f发送三轮
            self.print_log("发送非周期数据，每个发送三帧")
            for _ in range(3):
                for item in un_cycle_send_msg_id_len_list:
                    msg_id = item[0]
                    msg_len = item[1]
                    send_msg_lis = [random.randint(0, 255) for _ in range(msg_len)]
                    self.ipdu.send_pdu(channel_name, msg_id, send_msg_lis)
                    time.sleep(0.1)
        else:
            string = f"在{channel_name}通道上 {send_node_name_log} 没有周期发送的数据"
            self.print_log(string)

        # 获取周期 通信的数据,
        other_cyc_send_lis, bgm_cyc_send_lis = self.cdd_parse.get_bus_send_msg_info(data_dic=bus_send_recv_dict,
                                                                                    send_nodes=send_node_name,
                                                                                    send_type="cyclic")
        # 获取周期 发送id
        if str(channel_name).lower() != "backbonefr":
            cycle_send_msg_id_set = set([item.get("msg_id") for item in other_cyc_send_lis])
        else:
            cycle_send_msg_id_set = set(
                [(item.get("msg_id"), item.get("msg_base_cycle"), item.get("msg_repetition")) for item in
                 other_cyc_send_lis])

        cycle_l1 = list(cycle_send_msg_id_set)
        cycle_l1.sort()
        string_log1 = f"在{channel_name}通道上 {send_node_name_log} 周期发送的数据有{len(cycle_l1)}个，id>{cycle_l1}"
        self.print_log(string_log1)
        if not len(cycle_send_msg_id_set):
            string = f"在{channel_name}通道上 {send_node_name_log} 没有周期发送的数据"
            self.print_log(string)

        # 获取bgm 周期发送id
        if str(channel_name).lower() != "backbonefr":
            bgm_cycle_send_msg_id_set = set([item.get("msg_id") for item in bgm_cyc_send_lis])
        else:
            bgm_cycle_send_msg_id_set = set(
                [(item.get("msg_id"), item.get("msg_base_cycle"), item.get("msg_repetition")) for item in
                 bgm_cyc_send_lis])

        cycle_l2 = list(bgm_cycle_send_msg_id_set)
        cycle_l2.sort()
        string_log2 = f"在{channel_name}通道上,BGM本身周期发送的数据有{len(cycle_l2)}个，id>{cycle_l2}"
        self.print_log(string_log2)
        if not len(bgm_cycle_send_msg_id_set):
            string = f"在{channel_name}通道上 BGM没有周期发送的数据"
            self.print_log(string)
        time.sleep(1)
        # 停止抓包,
        self.bgm_tcpdump.stop_bgm_tcpdump()
        # 把 bgm 的日志 拉取到本地，并删除bgm内部的 pcap 包
        pacp_file_path = self.bgm_tcpdump.scp_bgm_log_to_local(bgm_log_name=save_name, del_flag=True)

        # bgm周期发送 + 非bgm 周期发送+ 非周期发送
        send_msg_id_set = set(list(send_msg_id_set_all) + list(cycle_send_msg_id_set) + list(bgm_cycle_send_msg_id_set))
        cycle_l22 = list(send_msg_id_set)
        cycle_l22.sort()
        string = f"在{channel_name}通道上发送报文{len(cycle_l22)}个》》{cycle_l22}"
        self.print_log(string)
        if not len(send_msg_id_set):
            string = f"在{channel_name}通道上 没有报文发送"
            self.print_log(string)
            assert len(send_msg_id_set), string

        # 解析 pcap包，生成对应的数据
        data_list, packet_list = self.cdd_parse.parse_pdu_msg(pacp_file_path, proto='UDP')
        # 校验数据信息
        # 获取结束通道 接收到的msg id
        if str(channel_name).lower() != "backbonefr":
            bgm_recv_msg_id_set = set(
                [item.get("msg_id") for item in data_list if item.get("channel_name") == channel_name])
        else:
            bgm_recv_msg_id_set = set(
                [(item.get("msg_id"), item.get("msg_base_cycle"), item.get("msg_repetition")) for item in data_list if
                 item.get("channel_name") == channel_name])

        bgm_recv_msg_id_lis = list(bgm_recv_msg_id_set)
        bgm_recv_msg_id_lis.sort()
        self.print_log(f"抓包接收{channel_name}通道的报文id有 {len(bgm_recv_msg_id_lis)}个,id>{bgm_recv_msg_id_lis}")
        # 抓包的id  减去发送的id
        duoyu_id_set = bgm_recv_msg_id_set - send_msg_id_set
        duoyu_id_list = list(duoyu_id_set)
        duoyu_id_list.sort()
        self.print_log(
            f"抓包报文去除{send_node_name_log}周期和非周期以及BGM周期发送的id后，多余的id有 {len(duoyu_id_list)}个,id>{duoyu_id_list}")

        # 多余的id 应该是 bgm 非周期发送的报文 bmg_send_msg_id_set_all
        un_kown_id = duoyu_id_set - bmg_send_msg_id_set_all
        un_kown_id_list = list(un_kown_id)
        un_kown_id_list.sort()
        self.print_log(
            f"抓包报文去除所有节点周期和非周期发送的id后，未知分类的id有 {len(un_kown_id_list)}个,id>{un_kown_id_list}")

        # 判断 所有发送的id 是否都被接收，发送id的是接收id的 子集
        # 减去 指定无法打包的id
        packet_id_set = set([item for item in send_msg_id_set if item not in un_packet_id_list])

        recv_value = packet_id_set.issubset(bgm_recv_msg_id_set)
        # 未收到的id为 集合相减
        unrece_ids = packet_id_set - bgm_recv_msg_id_set

        send_l = list(packet_id_set)
        send_l.sort()
        unrece_l = list(unrece_ids)
        unrece_l.sort()
        string_log = f"应该收到的id个数为{len(send_l)}个》{send_l};\n未收到的id个数为{len(unrece_l)}个,id>{unrece_l}"
        self.print_log(string_log)
        assert recv_value, f"未接收到id为：{unrece_ids}"

    def send_all_node(self):
        """
        发送can/lin/fr所有信号并抓取tcp包解析
        return: 解析后的数据
        """
        # 开启bgm内部抓包
        bgm_tcpdump_file_path, save_name = self.bgm_tcpdump.start_bgm_tcpdump(iface="eth0")
        # 发送can/lin/fr 所有报文
        self.ipdu.resume_all_bus_send()
        time.sleep(60)
        # 停止抓包,
        self.bgm_tcpdump.stop_bgm_tcpdump()
        # 把 bgm 的日志 拉取到本地，并删除bgm内部的 pcap 包
        pacp_file_path = self.bgm_tcpdump.scp_bgm_log_to_local(bgm_log_name=save_name, del_flag=True)
        # 解析 pcap包，生成对应的数据
        data_list, packet_list = self.cdd_parse.parse_pdu_msg(pacp_file_path, proto='UDP')
        return packet_list, data_list

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_bodycan_ccm_caseid_1984388(self):
        """
        发送body can上CCM节点信息
        """
        channel_name = "bodycan"
        send_node_name = "CCM"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_bodycan_ddm_caseid_1984438(self):
        """
        发送body can上DDM节点信息
        """
        channel_name = "bodycan"
        send_node_name = "DDM"
        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_bodycan_SMB_caseid_1986950(self):
        """
        发送body can上SMB节点信息
        """
        channel_name = "bodycan"
        send_node_name = "SMB"
        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_bodycan_dpod_caseid_1984437(self):
        """
        发送body can上DPOD节点信息
        """
        channel_name = "bodycan"
        send_node_name = "DPOD"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_bodycan_etcm_caseid_1984436(self):
        """
        发送body can上ETCM节点信息
        """
        channel_name = "bodycan"
        send_node_name = "ETCM"
        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_bodycan_ipm_caseid_1984435(self):
        """
        发送body can上IPM节点信息
        """
        channel_name = "bodycan"
        send_node_name = "IPM"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_bodycan_lpod_caseid_1984434(self):
        """
        发送body can上LPOD节点信息
        """
        channel_name = "bodycan"
        send_node_name = "LPOD"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_bodycan_pdm_caseid_1984433(self):
        """
        发送body can上PDM节点信息
        """
        channel_name = "bodycan"
        send_node_name = "PDM"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_bodycan_pot_caseid_1984432(self):
        """
        发送body can上POT节点信息
        """
        channel_name = "bodycan"
        send_node_name = "POT"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_bodycan_ppod_caseid_1984431(self):
        """
        发送body can上PPOD节点信息
        """
        channel_name = "bodycan"
        send_node_name = "PPOD"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_bodycan_rldm_caseid_1984430(self):
        """
        发送body can上RLDM节点信息
        """
        channel_name = "bodycan"
        send_node_name = "RLDM"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_bodycan_rpod_caseid_1984429(self):
        """
        发送body can上RPOD节点信息
        """
        channel_name = "bodycan"
        send_node_name = "RPOD"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_bodycan_rrdm_caseid_1984428(self):
        """
        发送body can上RRDM节点信息
        """
        channel_name = "bodycan"
        send_node_name = "RRDM"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_bodycan_smd_caseid_1984427(self):
        """
        发送body can上SMD节点信息
        """
        channel_name = "bodycan"
        send_node_name = "SMD"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_bodycan_smp_caseid_1984426(self):
        """
        发送body can上SMP节点信息
        """
        channel_name = "bodycan"
        send_node_name = "SMP"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_bodycan_swtl_caseid_1984425(self):
        """
        发送body can上SWTL节点信息
        """
        channel_name = "bodycan"
        send_node_name = "SWTL"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_bodycan_swtr_caseid_1984424(self):
        """
        发送body can上SWTR节点信息
        """
        channel_name = "bodycan"
        send_node_name = "SWTR"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_infocanfd_cdc_caseid_1984423(self):
        """
        发送infocanfd can上CDC节点信息
        """
        channel_name = "infocanfd"
        send_node_name = "CDC"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_adcanfd_acu_caseid_1984411(self):
        """
        发送adcanfd can上ACU节点信息
        """
        channel_name = "adcanfd"
        send_node_name = "ACU"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_propulsioncan_becm1_caseid_1984410(self):
        """
        发送propulsioncan can上BECM1节点信息
        """
        channel_name = "propulsioncan"
        send_node_name = "BECM1"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_propulsioncan_ecm_caseid_1984409(self):
        """
        发送propulsioncan can上ECM节点信息
        """
        channel_name = "propulsioncan"
        send_node_name = "ECM"
        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_propulsioncan_egsm_caseid_1984408(self):
        """
        发送propulsioncan can上EGSM节点信息
        """
        channel_name = "propulsioncan"
        send_node_name = "EGSM"
        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_propulsioncan_hvcm_caseid_1984407(self):
        """
        发送propulsioncan can上HVCM节点信息
        """
        channel_name = "propulsioncan"
        send_node_name = "HVCM"
        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_propulsioncan_iem_caseid_1984406(self):
        """
        发送propulsioncan can上IEM节点信息
        """
        channel_name = "propulsioncan"
        send_node_name = "IEM"
        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_propulsioncan_srs_caseid_1984404(self):
        """
        发送propulsioncan can上srs节点信息
        """
        channel_name = "propulsioncan"
        send_node_name = "SRS"
        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_propulsioncan_mgm_caseid_1984405(self):
        """
        发送propulsioncan can上MGM节点信息
        """
        channel_name = "propulsioncan"
        send_node_name = "MGM"
        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_propulsioncan_vddm_caseid_1984403(self):
        """
        发送propulsioncan can上VDDM节点信息
        """
        channel_name = "propulsioncan"
        send_node_name = "VDDM"
        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_chassiscan1_acu_caseid_1984422(self):
        """
        发送chassiscan1 can上ACU节点信息
        """
        channel_name = "chassiscan1"
        send_node_name = "ACU"
        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_chassiscan1_ecm_caseid_1984418(self):
        """
        发送chassiscan1 can上ECM节点信息
        """
        channel_name = "chassiscan1"
        send_node_name = "ECM"
        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_chassiscan1_pscm1_caseid_1984421(self):
        """
        发送chassiscan1 can上PSCM1节点信息
        """
        channel_name = "chassiscan1"
        send_node_name = "PSCM1"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_chassiscan1_sas_caseid_1984420(self):
        """
        发送chassiscan1 can上SAS节点信息
        """
        channel_name = "chassiscan1"
        send_node_name = "SAS"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_chassiscan1_vddm_caseid_1984419(self):
        """
        发送chassiscan1 can上VDDM节点信息
        """
        channel_name = "chassiscan1"
        send_node_name = "VDDM"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_chassiscan2_bbm_caseid_1984417(self):
        """
        发送chassiscan2 can上BBM节点信息
        """
        channel_name = "chassiscan2"
        send_node_name = "BBM"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_chassiscan2_ecm_caseid_1984416(self):
        """
        发送chassiscan2 can上ECM节点信息
        """
        channel_name = "chassiscan2"
        send_node_name = "ECM"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_chassiscan2_sum1_caseid_1984415(self):
        """
        发送chassiscan2 can上SUM1节点信息
        """
        channel_name = "chassiscan2"
        send_node_name = "SUM1"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_chassiscan2_vddm_caseid_1984414(self):
        """
        发送chassiscan2 can上VDDM节点信息
        """
        channel_name = "chassiscan2"
        send_node_name = "VDDM"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_passivesafetycan_rml_caseid_1984413(self):
        """
        发送passivesafetycan can上RML节点信息
        """
        channel_name = "passivesafetycan"
        send_node_name = "RML"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_passivesafetycan_srs_caseid_1984412(self):
        """
        发送passivesafetycan can上SRS节点信息
        """
        channel_name = "passivesafetycan"
        send_node_name = "SRS"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_connectivitycanfd_bncm_caseid_1984402(self):
        """
        发送connectivitycanfd can上BNCM节点信息
        """
        channel_name = "connectivitycanfd"
        send_node_name = "BNCM"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_connectivitycanfd_drmfl_caseid_1984401(self):
        """
        发送connectivitycanfd can上DRMFL节点信息
        """
        channel_name = "connectivitycanfd"
        send_node_name = "DRMFL"
        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_connectivitycanfd_drmfr_caseid_1984400(self):
        """
        发送connectivitycanfd can上DRMFR节点信息
        """
        channel_name = "connectivitycanfd"
        send_node_name = "DRMFR"
        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_connectivitycanfd_drmrl_caseid_1984399(self):
        """
        发送connectivitycanfd can上DRMRL节点信息
        """
        channel_name = "connectivitycanfd"
        send_node_name = "DRMRL"
        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_connectivitycanfd_drmrr_caseid_1984398(self):
        """
        发送connectivitycanfd can上DRMRR节点信息
        """
        channel_name = "connectivitycanfd"
        send_node_name = "DRMRR"
        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_connectivitycanfd_nkr_caseid_1984397(self):
        """
        发送connectivitycanfd can上NKR节点信息
        """
        channel_name = "connectivitycanfd"
        send_node_name = "NKR"
        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_connectivitycanfd_tcam_caseid_1984396(self):
        """
        发送connectivitycanfd can上NKR节点信息
        """
        channel_name = "connectivitycanfd"
        send_node_name = "TCAM"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_connectivitycanfd_wpc_caseid_1984395(self):
        """
        发送connectivitycanfd can上WPC节点信息
        """
        channel_name = "connectivitycanfd"
        send_node_name = "WPC"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_connectivitycanfd_wpc3_caseid_1986949(self):
        """
        发送connectivitycanfd can上WPC3节点信息
        """
        channel_name = "connectivitycanfd"
        send_node_name = "WPC3"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_bodyexposedcanfd_hcml_caseid_1984394(self):
        """
        发送bodyexposedcanfd can上HCML节点信息
        """
        channel_name = "bodyexposedcanfd"
        send_node_name = "HCML"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_bodyexposedcanfd_hcmr_caseid_1984393(self):
        """
        发送bodyexposedcanfd can上HCMR节点信息
        """
        channel_name = "bodyexposedcanfd"
        send_node_name = "HCMR"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_bodyexposedcanfd_rcml_caseid_1984392(self):
        """
        发送bodyexposedcanfd can上RCML节点信息
        """
        channel_name = "bodyexposedcanfd"
        send_node_name = "RCML"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_bodyexposedcanfd_rcmm_caseid_1984391(self):
        """
        发送bodyexposedcanfd can上RCMM节点信息
        """
        channel_name = "bodyexposedcanfd"
        send_node_name = "RCMM"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_bodyexposedcanfd_rcmr_caseid_1984390(self):
        """
        发送bodyexposedcanfd can上RCMR节点信息
        """
        channel_name = "bodyexposedcanfd"
        send_node_name = "RCMR"

        self.check_bgm_packet_msg_id(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_fr_caseid_1984439(self):
        """
        发送fr上所有节点信息
        """
        channel_name = "backbonefr"
        send_node_name = None
        un_packet_id_list = [(66, 0, 1), (68, 0, 1), (69, 0, 1), (70, 0, 1), (74, 0, 1), (75, 0, 1), (76, 0, 1),
                             (81, 0, 1), (82, 0, 1), (87, 0, 1), (88, 0, 1), (89, 0, 1), (90, 0, 1), (91, 0, 1),
                             (92, 0, 1), (93, 0, 1), (94, 0, 1), (107, 0, 64), (120, 0, 64), (121, 0, 64), (123, 0, 64),
                             (128, 0, 64)]
        self.check_bgm_packet_msg_id(channel_name, send_node_name, un_packet_id_list=un_packet_id_list)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_cem_lin1_caseid_1984444(self):
        """
        发送cem_lin1上所有节点信息
        """
        # 唤醒lin1
        self.ipdu.lin1_wakeup()
        channel_name = "cem_lin1"
        send_node_name = None
        un_packet_id_list = [20, 22, 18, 32, 24, 34, 8, 25, 40, 61]
        self.check_bgm_packet_msg_id(channel_name, send_node_name, un_packet_id_list=un_packet_id_list)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_cem_lin2_caseid_1984443(self):
        """
        发送cem_lin2上所有节点信息
        """
        channel_name = "cem_lin2"
        send_node_name = None
        un_packet_id_list = [33, 34, 35, 37, 38, 48, 49, 53, 2, 61]
        self.check_bgm_packet_msg_id(channel_name, send_node_name, un_packet_id_list=un_packet_id_list)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_cem_lin3_caseid_1984442(self):
        """
        发送cem_lin3上所有节点信息
        """
        channel_name = "cem_lin3"
        send_node_name = None
        un_packet_id_list = [23, 10, 25, 27, 24, 26, 61]
        self.check_bgm_packet_msg_id(channel_name, send_node_name, un_packet_id_list=un_packet_id_list)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_cem_lin4_caseid_1984441(self):
        """
        发送cem_lin4上所有节点信息
        """
        channel_name = "cem_lin4"
        send_node_name = None
        un_packet_id_list = [47, 20, 33, 7, 8, 22, 35, 36, 61]
        self.check_bgm_packet_msg_id(channel_name, send_node_name, un_packet_id_list=un_packet_id_list)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_cem_lin5_caseid_1984440(self):
        """
        发送cem_lin5上所有节点信息
        """
        channel_name = "cem_lin5"
        send_node_name = None
        un_packet_id_list = [61]
        self.check_bgm_packet_msg_id(channel_name, send_node_name, un_packet_id_list=un_packet_id_list)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_cem_lin6_caseid_1984389(self):
        """
        发送cem_lin6上所有节点信息
        """
        channel_name = "cem_lin6"
        send_node_name = None
        un_packet_id_list = [33, 34, 35, 10, 14, 15, 5, 12, 17, 21, 61]
        self.check_bgm_packet_msg_id(channel_name, send_node_name, un_packet_id_list=un_packet_id_list)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_check_data_end_caseid_1984451(self, do_assert=True):
        """
        检查文件结尾符是否为fe
        """
        # 发送can/lin/fr所有信号并解析
        packet_list, data_list = self.send_all_node()
        ret_code = self.cdd_parse.check_end_string(packet_list)
        if do_assert:
            assert ret_code, "结束符号不对！"

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_check_data_len_caseid_1984452(self, do_assert=True):
        """
        检查报文长度
        """
        # 发送can/lin/fr所有信号并解析
        packet_list, data_list = self.send_all_node()
        # 校验长度
        ret_code = self.cdd_parse.check_pud_len(packet_list)
        if do_assert:
            assert ret_code, "eth 报文长度不对！"

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_check_data_cicle_caseid_1984450(self, do_assert=True):
        """
        检查周期
        """
        # 发送can/lin/fr所有信号并解析
        packet_list, data_list = self.send_all_node()
        # 校验 周期
        ret_code = self.cdd_parse.check_pud_cycle(packet_list)
        if do_assert:
            assert ret_code, "周期不对！"

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.smoke
    def test_download_error_jetlog_message_caseid_1984488(self):
        """
        下载含E s2s 的jetlog_message文件
        """
        self.bgm_tcpdump = BGM_SSH()
        outmsg = BGM_SSH().type_commands("ls /log/jetlog_message*")
        jie_log_list = [j for i in outmsg.split("\n") for j in i.split(" ") if len(j) != 0]
        error_jetlog_message_list = []
        if not os.path.exists("./jet_log"):
            os.mkdir("./jet_log")
        for i in [i for i in jie_log_list[1:] if str(datetime.now()).replace("-", "").split(" ")[0] in i]:
            error_message = BGM_SSH().type_commands(f'/app/bin/zstdcat {i} | grep "E s2sF"')
            logger.info(f"当前错误的数据长度为：{len(error_message)}")
            if (len(error_message) != 0) and (not os.path.exists(f"./{i}")):
                file_download(device_name="BGM", local_path="./jet_log", remote_path=i)
                logger.info(f"E s2s 在文件{i}中")
                error_jetlog_message_list.append(i)
        assert not len(error_jetlog_message_list), "出现 E s2s"

    @pytest.mark.smoke
    def test_check_cdd_pack_cicle_caseid_1984497(self, do_assert=True):
        """
        检查周期
        """
        # 发送can/lin/fr所有信号并解析
        packet_list, data_list = self.send_all_node()
        # 校验 周期
        ret_code = self.check_cdd_pack_cycle(data_list)
        if do_assert:
            assert ret_code, "cdd 打包周期不对！"

    @pytest.mark.smoke
    def test_check_msg_lenth_caseid_1985118(self, do_assert=True):
        """
        检查 msg id lenth
        """
        # 发送can/lin/fr所有信号并解析
        packet_list, data_list = self.send_all_node()
        error_list = []
        for i in data_list:
            if i['msg_id'] == 1343:
                continue
            elif i['msg_id'] == 87 and i['msg_base_cycle'] == 0 and i['msg_repetition'] == 1:
                continue
            else:
                res = self.cdd_parse.get_bus_msgid_info(self.ipdu,i['channel_name'])
                if i['msg_id'] == res[i['msg_id']]['msg_id'] and i['msg_base_cycle'] == res[i['msg_id']]['msg_base_cycle'] and i['msg_repetition'] == res[i['msg_id']]['msg_repetition'] and i['msg_len'] != res[i['msg_id']]["msg_length"]:
                    logger.info(f"pcap行号： {i['packet_index']} ，打包内容 = {i['msg']} ")
                    error_list.append(f"预期 lenth 为：{res[i['msg_id']]}，实际的lenth为：{i['msg_len']}")
        assert not(error_list),f"错误数据为：{error_list}"

    def check_cdd_pack_cycle(self, data_list, min_value=0.0, max_value=10):
        '''
        判断 udp 报文周期
        @param self:
        @param packet_list:
        @param max_value: 10 ms
        @param min_value: 0.8ms
        @return:
        '''
        error_list = []
        erro_value = []
        # 正常的周期计数
        count = 0
        max_cdd_pack_cycle = 0
        for i in range(1, len(data_list)):
            # 时间戳
            timestamp1 = time.mktime(time.strptime(str(data_list[i - 1].get("timestamp")), "%Y-%m-%d %H:%M:%S"))*1000
            timestamp2 = time.mktime(time.strptime(str(data_list[i].get("timestamp")), "%Y-%m-%d %H:%M:%S"))*1000

            t1 = data_list[i - 1].get("ms_timestamp") + timestamp1
            t2 = data_list[i].get("ms_timestamp") + timestamp2
            temp = t2 - t1
            if temp > max_cdd_pack_cycle:
                max_cdd_pack_cycle = temp
                logger.info(f"cdd 最大打包周期为 {max_cdd_pack_cycle} ms")
            if min_value <= temp <= max_value:
                count += 1
                continue
            if temp >= -3:
                continue
            erro_value.append(temp)

            packet_index = data_list[i].get('packet_index')
            packet_time = data_list[i].get('packet_time')
            string = f"在pcap 文件第{packet_index}行,时间为{packet_time}，打包报文周期为{t2 - t1}不在{min_value}秒到{max_value}秒之间"
            logger.error(string)
            logger.error(data_list[i - 1])
            logger.error(f'timestamp1={timestamp1}')
            logger.error(f'timestamp2={timestamp2}')
            logger.error(data_list[i])

            error_list.append(data_list[i])

        erro_value.sort()
        erro_value.reverse()
        logger.error(f"出范围cdd 打包超的周期频率{erro_value}")
        new_dict = self.cdd_parse.get_range_scop(erro_value, max_value)
        new_dict["正常"] = count
        for name, value in new_dict.items():
            new_dict[name] = str(round(value / len(data_list), 4) * 100) + "%"

        if not len(error_list):
            return True
        else:
            logger.error(f"出范围cdd 打包超的周期频率{new_dict}")
            logger.error(f"cdd 打包超出范围的周期为{erro_value}")
            logger.error(
                f"总报文数{len(data_list)},打包报文周期异常的》》{len(error_list)}个，{error_list}"
            )
            return False


if __name__ == "__main__":
    pytest.main()
    # pytest basic_platform/cdd_pack/cdd_function/test_cdd_function.py
