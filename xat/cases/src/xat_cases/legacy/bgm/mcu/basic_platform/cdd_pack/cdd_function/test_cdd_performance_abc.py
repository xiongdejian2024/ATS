"""
@File        : test_cdd_function.py
@Author      : O_daidi.liang@external.jiduauto.com
@Time        : 2023/10/31 15:12
@Description : cdd 打包的相关用例

"""

from asyncio import sleep
import pytest
import allure
from xat_cases.legacy.basetech.case_helper.test_abc_base import TestABCBase
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from datetime import datetime
import random
import time
from xat_ecu.legacy.common.logger import logger
from framework.automotive.utils.data_type import EcuInfo

global pecket_loss_list
pecket_loss_list = []


@pytest.mark.mcu_test
@allure.feature("MCU 基础平台/CDD打包功能")
@allure.story("CDD功能用例")
class TestCddFunction(TestABCBase):
    @staticmethod
    def change_bench_config(ecu:EcuInfo) -> EcuInfo:
        ecu.domain.single_bgm = True
        ecu.domain.two_domain = False
        ecu.tc_config["dut_ecu"] = ["BGM"]
        return ecu
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.bgm_tcpdump = BGM_SSH()
        BGM_SSH().init_bgm_tcpdump()#推送tcpdump抓包工具，并初始化抓包工具

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

        with allure.step(f"IO控制TCAM下电"):
            self.io.tcam_power_off()
            time.sleep(30)

    def after_each_func(self, ecu):
        # Code Location
        super().after_each_func(ecu)

    def after_class(self, ecu):
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.bus_comm.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
            self.bus_comm.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        # 删除bgm 内部所有的pcap 包，必须要有的
        self.bgm_tcpdump.delete_bgm_tcpdump_file()
        super().after_class(self, ecu)
        self.bus_comm.ipdu.lin1_reset_wakeup()
        logger.info(f"pecket_loss_list== {pecket_loss_list}")

    def print_log(self, data: str):
        '''
        打印日志
        @param data:
        @return:
        '''
        with allure.step(data):
            logger.info(data)

    def check_packet_loss_rate(self, channel_name, send_node_name, tcpdump_time=10, **kwargs):
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
        self.print_log(f"不可以打包的id有{len(un_packet_id_list)}个》》》{un_packet_id_list}")

        # 开启bgm内部抓包
        bgm_tcpdump_file_path, save_name = self.bgm_tcpdump.start_bgm_tcpdump(iface="eth0")

        time.sleep(tcpdump_time)
        # 获取  通道所有信息
        bus_send_recv_dict = self.mix.get_bus_send_recv_info(channel_name=channel_name)
        # 获取非周期发送的收据
        other_send_lis1, bgm_send_lis = self.mix.get_bus_send_msg_info(data_dic=bus_send_recv_dict,
                                                                             send_nodes=send_node_name,
                                                                             send_type="spontaneous")
        # bgm 节点 非周期发送的
        logger.info(f"bgm_send_lis={other_send_lis1}")
        # 去除不可以打包的

        if str(channel_name).lower() != "backbonefr":
            other_send_lis = [item for item in other_send_lis1 if
                              item.get("msg_id") not in un_packet_id_list]

            bmg_send_msg_id_set_all = set([item.get("msg_id") for item in bgm_send_lis if item.get("msg_id")])
        else:
            other_send_lis = [item for item in other_send_lis1 if
                              (item.get("msg_id"), item.get("msg_base_cycle"),
                               item.get("msg_repetition")) not in un_packet_id_list]

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

        un_cycle_send_msg_dict = {}
        if send_msg_id_set_all:
            # 获取长度
            un_cycle_send_msg_id_len_list = set(
                [(item.get("msg_id"), item.get("msg_length")) for item in other_send_lis if item.get("msg_id")])
            # 发送 非周期数据,f发送三轮
            with allure.step("发送非周期数据，每个发送10帧"):
                for index_1 in range(10):
                    string = f"第{index_1}轮非周期发送报文"
                    with allure.step(string):
                        for index_2, item in enumerate(un_cycle_send_msg_id_len_list):
                            msg_id = item[0]
                            msg_len = item[1]
                            send_msg_lis = [random.randint(0, 255) for _ in range(msg_len)]
                            # 存放发送数据列表
                            msg_string = bytes(send_msg_lis).hex().upper()
                            if msg_id in un_cycle_send_msg_dict:
                                un_cycle_send_msg_dict[msg_id].append(msg_string)
                            else:
                                un_cycle_send_msg_dict[msg_id] = [msg_string]
                            self.bus_comm.ipdu.send_pdu(channel_name, msg_id, send_msg_lis)
                            string = f"第{index_2}个非周期发送id为{hex(msg_id)}，内容为{msg_string}"
                            self.print_log(string)
                            time.sleep(0.1)
        else:
            string = f"在{channel_name}通道上 {send_node_name_log} 没有周期发送的数据"
            self.print_log(string)

        # 获取周期 通信的数据,
        other_cyc_send_lis1, bgm_cyc_send_lis1 = self.mix.get_bus_send_msg_info(data_dic=bus_send_recv_dict,
                                                                                      send_nodes=send_node_name,
                                                                                      send_type="cyclic")

        # 获取周期 发送id
        if str(channel_name).lower() != "backbonefr":
            other_cyc_send_lis = [item for item in other_cyc_send_lis1 if item.get("msg_id") not in un_packet_id_list]

            bgm_cyc_send_lis = [item for item in bgm_cyc_send_lis1 if item.get("msg_id") not in un_packet_id_list]

            cycle_send_msg_id_set = set([item.get("msg_id") for item in other_cyc_send_lis])
        else:
            other_cyc_send_lis = [item for item in other_cyc_send_lis1 if
                                  ((item.get("msg_id"), item.get("msg_base_cycle"),
                                    item.get("msg_repetition"))) not in un_packet_id_list]

            bgm_cyc_send_lis = [item for item in bgm_cyc_send_lis1 if
                                ((item.get("msg_id"), item.get("msg_base_cycle"),
                                  item.get("msg_repetition"))) not in un_packet_id_list]

            cycle_send_msg_id_set = set(
                [(item.get("msg_id"), item.get("msg_base_cycle"), item.get("msg_repetition")) for item in
                 other_cyc_send_lis])
        logger.info(f"other_cyc_send_lis={other_cyc_send_lis}")
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

        # pacp_file_path=""
        # 解析 pcap包，生成对应的数据
        data_list, packet_list = self.mix.parse_pdu_msg(pacp_file_path, proto='UDP')
        # data_list, packet_list = self.cdd_parse.parse_pdu_msg("/root/bgm_log/cdd011701.pcap", proto='UDP')
        # id 分类
        data_info_dict = {}
        for item in data_list:
            get_channel_name = item.get("channel_name")
            if get_channel_name != channel_name:
                continue
            if str(channel_name).lower() != "backbonefr":
                item_id = item.get("msg_id")
            else:
                item_id = (item.get("msg_id"), item.get("msg_base_cycle"), item.get("msg_repetition"))
            if item_id in data_info_dict:
                data_info_dict[item_id].append(item)
            else:
                data_info_dict[item_id] = [item]
        logger.info(f"fdata_info_dict={data_info_dict}")
        # 对发送的id 进行便利
        bgm_cycl_send_err = {}
        # BGM 周期发送的
        with allure.step(f"BGM 周期发送的报文{len(bgm_cyc_send_lis)}个"):
            try:
                for item in bgm_cyc_send_lis:

                    if str(channel_name).lower() != "backbonefr":
                        item_id = item.get("msg_id")
                    else:
                        item_id = (item.get("msg_id"), item.get("msg_base_cycle"), item.get("msg_repetition"))

                    item_msg_cycle = item.get("msg_cycle")

                    item_msg_list = data_info_dict.get(item_id)

                    data = f"id 为{hex(item_id) if isinstance(item_id, int) else item_id} 报文 {len(item_msg_list)}个，周期=={item_msg_cycle} "
                    lissss = []
                    with allure.step(data):

                        for ltg in range(1, len(item_msg_list)):
                            timestamp0 = str(item_msg_list[ltg - 1]["timestamp"])
                            ms_timestamp0 = item_msg_list[ltg - 1]["ms_timestamp"]
                            time_stamp0 = int(
                                time.mktime(time.strptime(timestamp0, '%Y-%m-%d %H:%M:%S')) * 1000) + ms_timestamp0

                            timestamp1 = str(item_msg_list[ltg]["timestamp"])
                            ms_timestamp1 = item_msg_list[ltg]["ms_timestamp"]

                            # self.print_log(str(timestamp))
                            time_stamp1 = int(
                                time.mktime(time.strptime(timestamp1, '%Y-%m-%d %H:%M:%S')) * 1000) + ms_timestamp1
                            temp = time_stamp1 - time_stamp0
                            lissss.append(temp)
                            # string = f" {len(item_msg_list)}个 temp=={temp}  时间=={timestamp1}  timestamp={time_stamp1} ms_timestamp={ms_timestamp1}"
                            # self.print_log(string)
                        lissss.sort()
                        lissss.reverse()
                    data = f"周期》》{list(set(lissss))}"
                    with allure.step(data):
                        pass

                    timestamp1 = str(item_msg_list[0]["timestamp"])
                    ms_timestamp1 = item_msg_list[0]["ms_timestamp"]
                    # self.print_log(str(timestamp))
                    time_stamp1 = int(
                        time.mktime(time.strptime(timestamp1, '%Y-%m-%d %H:%M:%S')) * 1000) + ms_timestamp1
                    string = f" {len(item_msg_list)}个 msg_id=={hex(item_id) if isinstance(item_id, int) else item_id}  周期=={item_msg_cycle}  timestamp={timestamp1} ms_timestamp={ms_timestamp1}"
                    self.print_log(string)

                    timestamp = str(item_msg_list[-1]["timestamp"])
                    ms_timestamp = item_msg_list[-1]["ms_timestamp"]
                    # string = f"{len(item_msg_list)}个 msg_id=={hex(item_id)if isinstance(item_id,int) else item_id}  周期=={item_msg_cycle}  timestamp={timestamp} ms_timestamp={ms_timestamp}"
                    # self.print_log(string)
                    time_stamp2 = int(time.mktime(time.strptime(timestamp, '%Y-%m-%d %H:%M:%S')) * 1000) + ms_timestamp

                    # self.print_log(string)

                    tmp = time_stamp2 - time_stamp1
                    # 按计算应该收到帧数
                    expet_recv_frams = tmp / (item_msg_cycle * 1000)
                    # 实际收到的帧数
                    act_recv = len(item_msg_list)
                    string = f"时间差为{tmp}，本应为{round(expet_recv_frams)}帧数据，实际为{act_recv}个"
                    self.print_log(string)
                    if round(expet_recv_frams) - act_recv > expet_recv_frams * 0.0001:
                        string = f"》》》ERROR 》》》 BGM 周期=={item_msg_cycle}ms 发送id为{hex(item_id) if isinstance(item_id, int) else item_id}的报文，在时间差为{tmp}ms，本应为{round(expet_recv_frams)}帧数据，实际为{act_recv}个"
                        bgm_cycl_send_err[item_id] = string
                        pecket_loss_list.append(
                            f"{channel_name}_BGM周期发送_{item_id}的丢包率为：{round((expet_recv_frams - act_recv) / expet_recv_frams, 4) * 100}%")
            except Exception as e:
                logger.info(f"err>{str(e)}")
                logger.info(f"err >> item_id={item_id}  item_msg_list={item_msg_list}")
                assert 0,str(e)
                # break

        send_cycl_to_bgm_err = {}
        # 周期发送给bgm的
        with allure.step(f"周期发送给BGM的报文{len(other_cyc_send_lis)}个"):
            for item in other_cyc_send_lis:
                # item_id = item.get("msg_id")
                if str(channel_name).lower() != "backbonefr":
                    item_id = item.get("msg_id")
                else:
                    item_id = (item.get("msg_id"), item.get("msg_base_cycle"), item.get("msg_repetition"))
                item_msg_cycle = item.get("msg_cycle")
                logger.info(f"item_id={item_id} ")
                item_msg_list = data_info_dict.get(item_id)
                timestamp1 = str(item_msg_list[0]["timestamp"])
                ms_timestamp1 = item_msg_list[0]["ms_timestamp"]
                # self.print_log(str(timestamp))
                time_stamp1 = int(time.mktime(time.strptime(timestamp1, '%Y-%m-%d %H:%M:%S')) * 1000) + ms_timestamp1
                string = f" {len(item_msg_list)}个 msg_id=={hex(item_id) if isinstance(item_id, int) else item_id}  周期=={item_msg_cycle}  timestamp={timestamp1} ms_timestamp={ms_timestamp1}"
                self.print_log(string)

                timestamp = str(item_msg_list[-1]["timestamp"])
                ms_timestamp = item_msg_list[-1]["ms_timestamp"]
                string = f"{len(item_msg_list)}个 msg_id=={hex(item_id) if isinstance(item_id, int) else item_id}  周期=={item_msg_cycle}  timestamp={timestamp} ms_timestamp={ms_timestamp}"
                self.print_log(string)
                time_stamp2 = int(time.mktime(time.strptime(timestamp, '%Y-%m-%d %H:%M:%S')) * 1000) + ms_timestamp

                self.print_log(string)

                tmp = time_stamp2 - time_stamp1
                # 按计算应该收到帧数
                expet_recv_frams = tmp / (item_msg_cycle * 1000)
                # 实际收到的帧数
                act_recv = len(item_msg_list)
                string = f"时间差为{tmp}，本应为{round(expet_recv_frams)}帧数据，实际为{act_recv}个"
                self.print_log(string)
                if round(expet_recv_frams) - act_recv > expet_recv_frams * 0.0001:
                    string = f"》》》ERROR 》》》 周期为{item_msg_cycle} ms 发送给 BGM 的 id为{hex(item_id) if isinstance(item_id, int) else item_id}的报文，在时间差为{tmp}ms，本应为{round(expet_recv_frams)}帧数据，实际为{act_recv}个"
                    send_cycl_to_bgm_err[item_id] = string
                    pecket_loss_list.append(
                        f"{channel_name}_{send_node_name}_周期发送给BGM_{item_id}的丢包率为：{round((expet_recv_frams - act_recv) / expet_recv_frams, 4) * 100}%")

                # break

        send_uncycl_to_bgm_err = {}
        # 非周期发送给 bgm的
        with allure.step(f"非周期发送给BGM的报文{len(other_send_lis)}个"):
            for item in other_send_lis:
                item_id = item.get("msg_id")
                recv_item_msg_list = [str(msg_data["msg"]).upper() for msg_data in data_info_dict.get(item_id)]
                send_item_msg_lis = un_cycle_send_msg_dict.get(item_id)
                not_recv = [msg for msg in send_item_msg_lis if msg not in recv_item_msg_list]
                if not_recv:
                    send_uncycl_to_bgm_err[item_id] = []
                    for msg in not_recv:
                        string = f"》》》ERROR》》》id为{hex(item_id)}非周期发送的{msg}报文，未收到"
                        send_uncycl_to_bgm_err[item_id].append(string)
                        self.print_log(string)
                else:

                    if recv_item_msg_list != send_item_msg_lis:
                        send_uncycl_to_bgm_err[item_id] = []
                        string = f"》》》ERROR》》》id为{hex(item_id)} 非周期发送的{len(send_item_msg_lis)}帧，接收{len(recv_item_msg_list)}帧 接收的时序不对，先发送的位先打包！"
                        send_uncycl_to_bgm_err[item_id].append(string)
                    else:
                        string = f"id为{hex(item_id)} 非周期发送的{len(send_item_msg_lis)}帧，接收{len(recv_item_msg_list)}帧，内容个数都正常"
                    self.print_log(string)

        # 判断 结果
        # 判断 bgm 周期发送的
        if bgm_cycl_send_err:
            header_string = f"》》》ERROR》》》BGM 周期发送的报文{len(bgm_cyc_send_lis)}个,失败{len(list(bgm_cycl_send_err.keys()))}"
            with allure.step(header_string):
                for msg_id, err_info in bgm_cycl_send_err.items():
                    self.print_log(err_info)

        # 判断  周期发送给 bgm
        if send_cycl_to_bgm_err:
            header_string = f"》》》ERROR》》》 周期发送给BGM的报文{len(bgm_cyc_send_lis)}个,失败{len(list(send_cycl_to_bgm_err.keys()))}"
            with allure.step(header_string):
                for msg_id, err_info in send_cycl_to_bgm_err.items():
                    self.print_log(err_info)

        # 判断非周期发送给BGM 的
        if send_uncycl_to_bgm_err:
            header_string = f"》》》ERROR》》》 非周期发送给BGM的报文{len(other_send_lis)}个,失败{len(list(send_uncycl_to_bgm_err.keys()))}"
            with allure.step(header_string):
                for msg_id, err_info_list in send_uncycl_to_bgm_err.items():
                    with allure.step(f"id 为{hex(msg_id)}非周期发送给BGM的报文{len(err_info_list)}个"):
                        for err_string in err_info_list:
                            self.print_log(err_string)

        assert not send_uncycl_to_bgm_err and not bgm_cycl_send_err and not send_cycl_to_bgm_err, "存在丢帧"

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_bodycan_ccm_caseid_1984744(self):
        """
        发送body can上CCM节点信息
        """
        channel_name = "bodycan"
        send_node_name = "CCM"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_bodycan_SMB_caseid_1986951(self):
        """
        发送body can上SMB节点信息
        """
        channel_name = "bodycan"
        send_node_name = "SMB"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_bodycan_ddm_caseid_1984726(self):
        """
        发送body can上DDM节点信息
        """
        channel_name = "bodycan"
        send_node_name = "DDM"
        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_bodycan_dpod_caseid_1984717(self):
        """
        发送body can上DPOD节点信息
        """
        channel_name = "bodycan"
        send_node_name = "DPOD"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_bodycan_etcm_caseid_1984711(self):
        """
        发送body can上ETCM节点信息
        """
        channel_name = "bodycan"
        send_node_name = "ETCM"
        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_bodycan_ipm_caseid_1984724(self):
        """
        发送body can上IPM节点信息
        """
        channel_name = "bodycan"
        send_node_name = "IPM"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_bodycan_lpod_caseid_1984730(self):
        """
        发送body can上LPOD节点信息
        """
        channel_name = "bodycan"
        send_node_name = "LPOD"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_bodycan_pdm_caseid_1984722(self):
        """
        发送body can上PDM节点信息
        """
        channel_name = "bodycan"
        send_node_name = "PDM"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_bodycan_pot_caseid_1984706(self):
        """
        发送body can上POT节点信息
        """
        channel_name = "bodycan"
        send_node_name = "POT"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_bodycan_ppod_caseid_1984710(self):
        """
        发送body can上PPOD节点信息
        """
        channel_name = "bodycan"
        send_node_name = "PPOD"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_bodycan_rldm_caseid_1984715(self):
        """
        发送body can上RLDM节点信息
        """
        channel_name = "bodycan"
        send_node_name = "RLDM"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_bodycan_rpod_caseid_1984703(self):
        """
        发送body can上RPOD节点信息
        """
        channel_name = "bodycan"
        send_node_name = "RPOD"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_bodycan_rrdm_caseid_1984732(self):
        """
        发送body can上RRDM节点信息
        """
        channel_name = "bodycan"
        send_node_name = "RRDM"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_bodycan_smd_caseid_1984731(self):
        """
        发送body can上SMD节点信息
        """
        channel_name = "bodycan"
        send_node_name = "SMD"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_bodycan_smp_caseid_1984712(self):
        """
        发送body can上SMP节点信息
        """
        channel_name = "bodycan"
        send_node_name = "SMP"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_bodycan_swtl_caseid_1984697(self):
        """
        发送body can上SWTL节点信息
        """
        channel_name = "bodycan"
        send_node_name = "SWTL"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_bodycan_swtr_caseid_1984727(self):
        """
        发送body can上SWTR节点信息
        """
        channel_name = "bodycan"
        send_node_name = "SWTR"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_infocanfd_cdc_caseid_1984696(self):
        """
        发送infocanfd can上CDC节点信息
        """
        channel_name = "infocanfd"
        send_node_name = "CDC"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_adcanfd_acu_caseid_1984695(self):
        """
        发送adcanfd can上ACU节点信息
        """
        channel_name = "adcanfd"
        send_node_name = "ACU"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_propulsioncan_becm1_caseid_1984704(self):
        """
        发送propulsioncan can上BECM1节点信息
        """
        channel_name = "propulsioncan"
        send_node_name = "BECM1"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_propulsioncan_ecm_caseid_1984733(self):
        """
        发送propulsioncan can上ECM节点信息
        """
        channel_name = "propulsioncan"
        send_node_name = "ECM"
        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_propulsioncan_egsm_caseid_1984705(self):
        """
        发送propulsioncan can上EGSM节点信息
        """
        channel_name = "propulsioncan"
        send_node_name = "EGSM"
        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_propulsioncan_hvcm_caseid_1984700(self):
        """
        发送propulsioncan can上HVCM节点信息
        """
        channel_name = "propulsioncan"
        send_node_name = "HVCM"
        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_propulsioncan_iem_caseid_1984714(self):
        """
        发送propulsioncan can上IEM节点信息
        """
        channel_name = "propulsioncan"
        send_node_name = "IEM"
        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_propulsioncan_srs_caseid_1984691(self):
        """
        发送propulsioncan can上srs节点信息
        """
        channel_name = "propulsioncan"
        send_node_name = "SRS"
        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_propulsioncan_mgm_caseid_1984694(self):
        """
        发送propulsioncan can上MGM节点信息
        """
        channel_name = "propulsioncan"
        send_node_name = "MGM"
        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_propulsioncan_vddm_caseid_1984701(self):
        """
        发送propulsioncan can上VDDM节点信息
        """
        channel_name = "propulsioncan"
        send_node_name = "VDDM"
        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_chassiscan1_acu_caseid_1984725(self):
        """
        发送chassiscan1 can上ACU节点信息
        """
        channel_name = "chassiscan1"
        send_node_name = "ACU"
        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_chassiscan1_ecm_caseid_1984699(self):
        """
        发送chassiscan1 can上ECM节点信息
        """
        channel_name = "chassiscan1"
        send_node_name = "ECM"
        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_chassiscan1_pscm1_caseid_1984708(self):
        """
        发送chassiscan1 can上PSCM1节点信息
        """
        channel_name = "chassiscan1"
        send_node_name = "PSCM1"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_chassiscan1_sas_caseid_1984721(self):
        """
        发送chassiscan1 can上SAS节点信息
        """
        channel_name = "chassiscan1"
        send_node_name = "SAS"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_chassiscan1_vddm_caseid_1984690(self):
        """
        发送chassiscan1 can上VDDM节点信息
        """
        channel_name = "chassiscan1"
        send_node_name = "VDDM"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_chassiscan2_bbm_caseid_1984716(self):
        """
        发送chassiscan2 can上BBM节点信息
        """
        channel_name = "chassiscan2"
        send_node_name = "BBM"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_chassiscan2_ecm_caseid_1984693(self):
        """
        发送chassiscan2 can上ECM节点信息
        """
        channel_name = "chassiscan2"
        send_node_name = "ECM"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_chassiscan2_sum1_caseid_1984720(self):
        """
        发送chassiscan2 can上SUM1节点信息
        """
        channel_name = "chassiscan2"
        send_node_name = "SUM1"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_chassiscan2_vddm_caseid_1984729(self):
        """
        发送chassiscan2 can上VDDM节点信息
        """
        channel_name = "chassiscan2"
        send_node_name = "VDDM"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_passivesafetycan_rml_caseid_1984713(self):
        """
        发送passivesafetycan can上RML节点信息
        """
        channel_name = "passivesafetycan"
        send_node_name = "RML"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_passivesafetycan_srs_caseid_1984689(self):
        """
        发送passivesafetycan can上SRS节点信息
        """
        channel_name = "passivesafetycan"
        send_node_name = "SRS"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_connectivitycanfd_bncm_caseid_1984709(self):
        """
        发送connectivitycanfd can上BNCM节点信息
        """
        channel_name = "connectivitycanfd"
        send_node_name = "BNCM"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_connectivitycanfd_drmfl_caseid_1984698(self):
        """
        发送connectivitycanfd can上DRMFL节点信息
        """
        channel_name = "connectivitycanfd"
        send_node_name = "DRMFL"
        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_connectivitycanfd_drmfr_caseid_1984718(self):
        """
        发送connectivitycanfd can上DRMFR节点信息
        """
        channel_name = "connectivitycanfd"
        send_node_name = "DRMFR"
        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_connectivitycanfd_drmrl_caseid_1984738(self):
        """
        发送connectivitycanfd can上DRMRL节点信息
        """
        channel_name = "connectivitycanfd"
        send_node_name = "DRMRL"
        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_connectivitycanfd_drmrr_caseid_1984741(self):
        """
        发送connectivitycanfd can上DRMRR节点信息
        """
        channel_name = "connectivitycanfd"
        send_node_name = "DRMRR"
        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_connectivitycanfd_nkr_caseid_1984745(self):
        """
        发送connectivitycanfd can上NKR节点信息
        """
        channel_name = "connectivitycanfd"
        send_node_name = "NKR"
        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_connectivitycanfd_tcam_caseid_1984737(self):
        """
        发送connectivitycanfd can上NKR节点信息
        """
        channel_name = "connectivitycanfd"
        send_node_name = "TCAM"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_connectivitycanfd_wpc_caseid_1984736(self):
        """
        发送connectivitycanfd can上WPC节点信息
        """
        channel_name = "connectivitycanfd"
        send_node_name = "WPC"

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_connectivitycanfd_WPC3_caseid_1986952(self):
        """
        发送connectivitycanfd can上WPC3节点信息
        """
        channel_name = "connectivitycanfd"
        send_node_name = "WPC3"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_bodyexposedcanfd_hcml_caseid_1984740(self):
        """
        发送bodyexposedcanfd can上HCML节点信息
        """
        channel_name = "bodyexposedcanfd"
        send_node_name = "HCML"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_bodyexposedcanfd_hcmr_caseid_1984743(self):
        """
        发送bodyexposedcanfd can上HCMR节点信息
        """
        channel_name = "bodyexposedcanfd"
        send_node_name = "HCMR"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_bodyexposedcanfd_rcml_caseid_1984739(self):
        """
        发送bodyexposedcanfd can上RCML节点信息
        """
        channel_name = "bodyexposedcanfd"
        send_node_name = "RCML"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_bodyexposedcanfd_rcmm_caseid_1984735(self):
        """
        发送bodyexposedcanfd can上RCMM节点信息
        """
        channel_name = "bodyexposedcanfd"
        send_node_name = "RCMM"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_bodyexposedcanfd_rcmr_caseid_1984734(self):
        """
        发送bodyexposedcanfd can上RCMR节点信息
        """
        channel_name = "bodyexposedcanfd"
        send_node_name = "RCMR"

        self.check_packet_loss_rate(channel_name, send_node_name)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_fr_caseid_1984719(self):
        """
        发送fr上所有节点信息
        """
        channel_name = "backbonefr"
        send_node_name = None
        un_packet_id_list = [(66, 0, 1), (68, 0, 1), (69, 0, 1), (70, 0, 1), (74, 0, 1), (75, 0, 1), (76, 0, 1),
                             (81, 0, 1), (82, 0, 1), (87, 0, 1), (88, 0, 1), (89, 0, 1), (90, 0, 1), (91, 0, 1),
                             (92, 0, 1), (93, 0, 1), (94, 0, 1), (107, 0, 64), (120, 0, 64), (121, 0, 64), (123, 0, 64),
                             (128, 0, 64), (127, 0, 64)]
        self.check_packet_loss_rate(channel_name, send_node_name, un_packet_id_list=un_packet_id_list)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_cem_lin1_caseid_1984728(self):
        """
        发送cem_lin1上所有节点信息
        """
        # 唤醒lin1
        self.bus_comm.ipdu.lin1_wakeup()
        channel_name = "cem_lin1"
        send_node_name = None
        un_packet_id_list = [20, 22, 18, 32, 24, 34, 8, 25, 40, 61]
        self.check_packet_loss_rate(channel_name, send_node_name, un_packet_id_list=un_packet_id_list)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_cem_lin2_caseid_1984707(self):
        """
        发送cem_lin2上所有节点信息
        """
        channel_name = "cem_lin2"
        send_node_name = None
        un_packet_id_list = [33, 34, 35, 37, 38, 48, 49, 53, 2, 61]
        self.check_packet_loss_rate(channel_name, send_node_name, un_packet_id_list=un_packet_id_list)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_cem_lin3_caseid_1984702(self):
        """
        发送cem_lin3上所有节点信息
        """
        channel_name = "cem_lin3"
        send_node_name = None
        un_packet_id_list = [23, 10, 25, 27, 24, 26, 61]
        self.check_packet_loss_rate(channel_name, send_node_name, un_packet_id_list=un_packet_id_list)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_cem_lin4_caseid_1984692(self):
        """
        发送cem_lin4上所有节点信息
        """
        channel_name = "cem_lin4"
        send_node_name = None
        un_packet_id_list = [47, 20, 33, 7, 8, 22, 35, 36, 61]
        self.check_packet_loss_rate(channel_name, send_node_name, un_packet_id_list=un_packet_id_list)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_cem_lin5_caseid_1984723(self):
        """
        发送cem_lin5上所有节点信息
        """
        channel_name = "cem_lin5"
        send_node_name = None
        un_packet_id_list = [61]
        self.check_packet_loss_rate(channel_name, send_node_name, un_packet_id_list=un_packet_id_list)

    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46',
        name='fr Pdu Case 228479',
    )
    @pytest.mark.sanity
    def test_cem_lin6_caseid_1984742(self):
        """
        发送cem_lin6上所有节点信息
        """
        channel_name = "cem_lin6"
        send_node_name = None
        un_packet_id_list = [33, 34, 35, 10, 14, 15, 5, 12, 17, 21, 61]
        self.check_packet_loss_rate(channel_name, send_node_name, un_packet_id_list=un_packet_id_list)


if __name__ == "__main__":
    pytest.main()
