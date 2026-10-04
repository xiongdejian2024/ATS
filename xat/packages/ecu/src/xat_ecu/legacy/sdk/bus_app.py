# -*- coding: utf-8 -*-
"""
@File        : bus_app.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022/10/16 10:51 AM
@Description : simulator of can or lin or fr (cyc,single)
@Examples    : example of how to use it
"""
import copy
import uuid
from cmath import log
import os
import subprocess
from re import L
from itertools import cycle
from typing import Union
import sys
import locale
import datetime

from xat_ecu import reporting as allure
import re

from xat_ecu.legacy.common.time_handle import get_time_str_year_month_day
from xat_ecu.legacy.interface.baidu_bos.bos_api import BosApi
from xat_ecu.legacy.interface.nuc_app import exec_shell
from xat_ecu.legacy.interface.youzi.youzi import YouZiClient

current_path = os.path.dirname(os.path.realpath(__file__))
import can
from threading import Thread
import threading

from xat_ecu.legacy.ecu_sim.parse_tn_config import ParseTNConfig
from xat_ecu.legacy.ecu_sim.parse_tb_config import ParseTBConfig
import time
from time import sleep
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.ecu_sim_const import ECUSimConst
from xat_ecu.legacy.sdk.driver.can_lib.socket_can import SocketCan
from xat_ecu.legacy.sdk.driver.toomoss.toomoss_can import ToomossCan
from xat_ecu.legacy.sdk.driver.toomoss.toomoss_lin import ToomossLin
from xat_ecu.legacy.sdk.driver.tosun.tosun_flexray import TosunFlexray
from xat_ecu.legacy.sdk.driver.tosun.tosun_can import TosunCan
from xat_ecu.legacy.sdk.driver.lin_lib.lin import Lin
from xat_ecu.legacy.sdk.driver.toomoss.toomoss_constant import *
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from xat_ecu.legacy.sdk.driver.tosun.tosunbus import TosunBus
from xat_ecu.legacy.sdk.driver.toomoss.toomoss_lin_status import ToomossStatus

# =========== Convenient and fast manual test  ====================================
exit_flag = False
timeout = 100


def send_single_data_directly(can_id, data, channel, bitrate=500000, is_fd=False):
    # Convenient and fast manual test
    can.rc['interface'] = 'socketcan'
    can.rc['channel'] = channel
    can.rc['bitrate'] = bitrate
    can.rc['fd'] = is_fd
    bus = can.interface.Bus()
    msg = can.Message(
        arbitration_id=can_id, data=data, is_extended_id=False, is_fd=is_fd
    )
    bus.send(msg)
    bus.shutdown()


def add_cyclic_msg_with_data(
        can_id, data, cyclic_rate, channel, bitrate=500000, is_fd=False
):
    # Convenient and fast manual test
    """
    Add cyclic message with specific data to bus
    :param can_id: can message id
    :param data: data of can cyclic message
    :param cyclic_rate: Cycle rate of new cyclic message (in seconds)
    """
    can.rc['interface'] = 'socketcan'
    can.rc['channel'] = channel
    can.rc['bitrate'] = bitrate
    can.rc['fd'] = is_fd
    bus = can.interface.Bus()
    msg = can.Message(
        arbitration_id=can_id, data=data, is_extended_id=False, is_fd=is_fd
    )
    while exit_flag is False:
        try:
            bus.send(msg)
        except can.CanError as e:
            logger.error("can.CanError is {}".format(e))
        sleep(cyclic_rate)
    bus.shutdown()


def add_cyclic_msg_with_data_run(
        can_id, data, cyclic_rate, channel, bitrate=500000, is_fd=False
):
    cyclic_msg = Thread(
        target=add_cyclic_msg_with_data,
        args=(can_id, data, cyclic_rate, channel, bitrate, is_fd),
    )
    cyclic_msg.start()


def reset_cyclic_msg_flag():
    global exit_flag
    exit_flag = False


def close_cyclic_msg():
    global exit_flag
    exit_flag = True


def receives(func, channel, wait=100, bustype='socketcan', bitrate=500000):
    global timeout
    timeout = wait
    rx_bus = can.interface.Bus(bustype=bustype, channel=channel, bitrate=bitrate)
    notifier = can.Notifier(rx_bus, [func])

    sleep(timeout)
    # Close Ecu_Sim by stopping notifier and interface_bus
    try:
        notifier.stop()
        rx_bus.socket.close()
        rx_bus.shutdown()
        logger.info('bus close success: {}'.format(channel))
    except AttributeError:
        logger.error('bus close error: {}'.format(channel))


def rx_msg(msg):
    logger.info("msg.arbitration_id is {}".format(msg.arbitration_id))
    logger.info("msg is {}".format(msg))


# ================================================================================================================


class BusApp:
    def __init__(self, ipdu, **cfg):
        '''
        :param ipdu    type: ISignalIPdu 实例
        :param cfg: dict
        cfg = {
        dut_ecu: ["BGM"]
        gateway_ip: "169.254.1.1"

        bus:
          eth_obd: "enx000ec64a8e4c"
          eth_vlan5: "eth0.5"
          eth_vlan9: "eth0.9"
          bodycan: 'can0'
          }
        '''

        tb_default_path = os.path.join(
            os.path.realpath(__file__).split("ecu_simulator")[0],
            "ecu_simulator/config/default_config.yaml",
        )
        tb_default_config = ParseTBConfig(tb_default_path)
        self._ipdu = ipdu
        if cfg:
            self.cfg = cfg
        else:
            self.cfg = tb_default_config.yaml_content

        logger.debug("bus_app cfg: {}".format(self.cfg))

        self.bus_dict = {}
        self.tosun_list = []

        bus_channel = self.cfg.get("bus")
        dut_ecu = self.cfg.get("dut_ecu")
        com_mock_ecu = self.cfg.get("com_mock_ecu")
        gatway_ecu = ECUSimConst.GATEWAY_ECU

        self.tosun_info = self.cfg.get("tosun_info")
        if self.tosun_info:
            tosun_issavelog = self.tosun_info.get("issavelog")
            if tosun_issavelog:
                self.tosun_issavelog = 0
            else:
                self.tosun_issavelog = 1
        else:
            self.tosun_issavelog = 0  # 默认保存日志
        self.veh_type = self.cfg.get("veh_type")
        self.bl_ver = self.cfg.get("bl_ver")
        if self.veh_type and self.bl_ver:
            # self.cls_path = "sdk/data/{}/can_lin_fr_cls/{}".format(self.veh_type, self.bl_ver)
            tn_config_path = "config/{}/{}/ecu_network.yaml".format(
                self.veh_type, self.bl_ver
            )
        else:
            logger.error(
                "Config error : self.veh_type is {}  self.bl_ver is {}".format(
                    self.veh_type, self.bl_ver
                )
            )
        tn_config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))), tn_config_path
        )
        self.tn_config = ParseTNConfig(tn_config_path)
        self.vehicle_topology = self.tn_config.get_vehicle_topology()
        self.bus_type = self.tn_config.get_bus_type()

        lin_bus = self.bus_type.get("lin")
        can_bus = self.bus_type.get("can")
        canfd_bus = self.bus_type.get("canfd")
        fr_bus = self.bus_type.get("fr")

        self.not_on_bench_ecu = []
        self.needful_bus = []
        self.vehicle_topology_no_eth = self.get_no_eth_vehicle_topology()

        self.bus_pdu_dict = ipdu.bus_pdu_dict
        self.pdu_list = []
        self.record_time = time.time()
        self.lin_trace_name = f"Lin.asc"
        self.lin_trace_log = ''
        self.lin_header_status = False
        self.lin_header_time = None
        self.file_exit = True
        self.lock = threading.Lock()
        self.bus_obj = []
        self.pcan_bus_obj = None
        self.stop_flag = True

        self.tosun_busname = []
        self.tosun_channel = {}
        self.tosun_busname_tc1034 = []
        self.tosun_channel_tc1034 = {}

        def generate_asc_log(device_type, **kwargs):
            if self.file_exit:
                return
            if device_type == "toomoss_lin":
                msg = kwargs.get('msg')
                check = kwargs.get('check')
                bus_name = kwargs.get('bus_name')
                with self.lock:
                    if not self.lin_header_status:
                        self.lin_header_time = time.time()
                        locale.setlocale(locale.LC_TIME, "en_US.UTF-8")
                        # 获取asc文件表头时间例如Thu Jul 13 06:23:13.837 PM 2023
                        dt = datetime.datetime.fromtimestamp(self.lin_header_time)
                        formatted_seconds = "{:.3f}".format(dt.second + dt.microsecond / 1000000)
                        formatted_time = dt.strftime("%a %b %d %I:%M:") + formatted_seconds + dt.strftime(" %p %Y")
                        self.lin_trace_log += f"date {formatted_time}\nbase hex  timestamps absolute\n"
                        self.lin_header_status = True
                    time_stamp = time.time() - self.lin_header_time
                    pid = hex(msg[0])[2:]
                    length = msg[2]
                    data = msg[3]
                    self.lin_trace_log += f"   {time_stamp:.6f} L{bus_name[-1]} {pid} Rx {length} {data}  checksum = {check}\n"
            else:
                logger.error('device_type not in tomoss_lin')
                return

        self.generate_asc_log = generate_asc_log
        if com_mock_ecu:
            no_dut_euc = com_mock_ecu  # not work , to do
        else:
            for dutecu in dut_ecu:
                ecubus = self.vehicle_topology_no_eth.get(dutecu)
                self.needful_bus = list(set(self.needful_bus) | set(ecubus))
            no_dut_euc = list(set(self.vehicle_topology.keys()) - set(dut_ecu))

        for ecu_key in no_dut_euc:
            bus_names = self.get_bus_name(ecu_key)
            if bus_names is None:
                break
            for bus_name in bus_names:
                #  For the time being, only one diagnostic bus is supported, and the diagnostic bus is placed in the first of the list
                if bus_name not in self.needful_bus:
                    continue
                self.channel = bus_channel.get(bus_name)

                lin_nad = self.tn_config.get_lin_id(ecu_key)

                if self.channel is None:
                    self.not_on_bench_ecu.append(ecu_key)
                    logger.warning(
                        "{} is not on the bench_config, ECU:{} can not be Simulated".format(
                            bus_name, ecu_key
                        )
                    )
                    break

                ecu_channel = bus_name
                pdu_dict = self.bus_pdu_dict[
                    bus_name
                ]  # self.bus_pdu_dict is given by ipdu.bus_pdu_dict

                if ecu_channel not in self.bus_dict.keys() and ecu_channel not in self.tosun_list:
                    if bus_name in can_bus:
                        if "can" in self.channel:
                            self.bus_dict[ecu_channel] = SocketCan(
                                bus_name, self.channel, bitrate=500000, ipdu=ipdu, callback=generate_asc_log
                            )
                        elif isinstance(self.channel, list):
                            # self.bus_dict[ecu_channel] = ToomossCan(bus_name, self.channel, brateconfig=CANConfig_CONSTANT.UTA05XX.bt_500k, ipdu=ipdu)
                            if isinstance(self.channel[0], int):
                                self.bus_dict[ecu_channel] = ToomossCan(
                                    bus_name,
                                    self.channel,
                                    nbrateconfig=CANConfig_CONSTANT.UTA05XX.nbt_500k,
                                    dbrateconfig=CANConfig_CONSTANT.UTA05XX.dbt_2m,
                                    ipdu=ipdu,
                                    is_fd=False
                                )
                            elif isinstance(self.channel[0], str):

                                # self.bus_dict[ecu_channel] = TosunCan(
                                #     bus_name,
                                #     self.channel,
                                #     nbrateconfig=500,
                                #     dbrateconfig=2000,
                                #     ipdu=ipdu,
                                #     is_fd=False,
                                #     callback=generate_asc_log
                                # )

                                self.tosun_busname.append(bus_name)
                                self.tosun_channel[bus_name] = self.channel
                                self.tosun_list.append(ecu_channel)
                    elif bus_name in canfd_bus:
                        if "can" in self.channel:
                            self.bus_dict[ecu_channel] = SocketCan(
                                bus_name,
                                self.channel,
                                bitrate=500000,
                                ipdu=ipdu,
                                is_fd=True,
                                callback=generate_asc_log
                            )
                        elif isinstance(self.channel, list):
                            if isinstance(self.channel[0], int):
                                self.bus_dict[ecu_channel] = ToomossCan(
                                    bus_name,
                                    self.channel,
                                    nbrateconfig=CANConfig_CONSTANT.UTA05XX.nbt_500k,
                                    dbrateconfig=CANConfig_CONSTANT.UTA05XX.dbt_2m,
                                    ipdu=ipdu,
                                    is_fd=True,
                                )
                            elif isinstance(self.channel[0], str):

                                # self.bus_dict[ecu_channel] = TosunCan(
                                #     bus_name,
                                #     self.channel,
                                #     nbrateconfig=500,
                                #     dbrateconfig=2000,
                                #     ipdu=ipdu,
                                #     is_fd=True,
                                #     callback=generate_asc_log
                                # )

                                self.tosun_busname.append(bus_name)
                                self.tosun_channel[bus_name] = self.channel
                                self.tosun_list.append(ecu_channel)
                    elif bus_name in lin_bus:
                        self.bus_dict[ecu_channel] = ToomossLin(
                            bus_name, self.channel, brate=19200, ipdu=ipdu, callback=generate_asc_log
                        )
                    elif bus_name in fr_bus:  # To Do
                        logger.info(bus_name)
                        # mock_msg_id_list = self.get_mock_msg_id_list(
                        #     dut_ecu, ipdu, bus_name
                        # )

                        # self.bus_dict[ecu_channel] = TosunFlexray(
                        #     bus_name,
                        #     self.channel,
                        #     mock_msg_id_list=mock_msg_id_list,
                        #     ipdu=ipdu,
                        # )

                        self.tosun_busname_tc1034.append(bus_name)
                        self.tosun_channel_tc1034[bus_name] = self.channel
                        self.tosun_list.append(ecu_channel)

                        # logger.info(type(self.bus_dict[ecu_channel].pdu_dict))
                        # logger.info(id(self.bus_dict[ecu_channel].pdu_dict))
                        logger.info("it is fr bus , instance")
                    else:
                        logger.info(
                            "{} is not on the vehicle_topology".format(bus_name)
                        )
        # 检查是否有同星进程，有就清理掉
        res = tosun_process_check()
        if self.tosun_busname:
            tosun_serial = self.tosun_channel.get(self.tosun_busname[0])[0]
            if tosun_serial is None:
                tosun_serial = ""

            # ------  临时处理，满足bodyalmcanfd1，2这个两路can发送报文的需求（这两路没有任何节点报文）；注意：只在有同星can时生效  ------
            if "bodyalmcanfd1" in bus_channel.keys():
                self.tosun_busname.append("bodyalmcanfd1")
                self.tosun_channel["bodyalmcanfd1"] = bus_channel["bodyalmcanfd1"]
            if "bodyalmcanfd2" in bus_channel.keys():
                self.tosun_busname.append("bodyalmcanfd2")
                self.tosun_channel["bodyalmcanfd2"] = bus_channel["bodyalmcanfd2"]
            # ----------------------------------------------------------------------------------------------

            self.bus_dict["tosun_tc1018"] = TosunBus(self.tosun_busname, self.tosun_channel, ipdu=ipdu, dut_ecu=dut_ecu,
                                                     device_name_info={"TC1018": tosun_serial},
                                                     issavelog=self.tosun_issavelog)
        if self.tosun_busname_tc1034:
            tosun_serial_tc1034 = self.tosun_channel_tc1034.get(self.tosun_busname_tc1034[0])[0]
            if tosun_serial_tc1034 is None:
                tosun_serial_tc1034 = ""
            self.bus_dict["tosun_tc1034"] = TosunBus(self.tosun_busname_tc1034, self.tosun_channel_tc1034, ipdu=ipdu,
                                                     dut_ecu=dut_ecu, device_name_info={"TC1034": tosun_serial_tc1034},
                                                     issavelog=self.tosun_issavelog)

    def get_mock_msg_id_list(self, dut_ecu: list, ipdu, bus_name):
        mock_msg_id_list = []
        pdu_dict = ipdu.bus_pdu_dict[bus_name]
        for msg_name, msg_dict in pdu_dict.items():
            if msg_dict["tx_node"] not in dut_ecu:
                mock_msg_id_list.append(msg_dict["msg_id"])
        return mock_msg_id_list

    def get_no_eth_vehicle_topology(self):
        vehicle_topology_no_eht = {}
        for ecukey in self.vehicle_topology.keys():
            ecu_no_eth_bus = []
            for bus in self.vehicle_topology.get(ecukey):
                if "eth_" not in bus:
                    ecu_no_eth_bus.append(bus)
            vehicle_topology_no_eht[ecukey] = ecu_no_eth_bus
        return vehicle_topology_no_eht

    def get_ecu_canid(self, ecu_name):
        ecu_canid = self.vehicle_topology[ecu_name][0]
        return ecu_canid

    def get_bus_name(self, ecu_name):
        bus_name = self.vehicle_topology.get(ecu_name)
        return bus_name

    def get_tosun_tc1018_can_chn(self, bus_name):
        # 只针对 同星 tc1018
        chn = self.tosun_channel.get(bus_name)[1]
        return chn

    # -------------------------------------只针对 同星-----------------------------------------------------------
    def _filter_msg(self, bus_name: str, msg_id, filter_type: int = 1):
        """
        添加过滤器信息到总线应用层
        
        Args:
            bus_name (str): 总线名称
            msg_id (Union[str, int]): 消息ID或消息名称
            filter_type (int, optional): 过滤器类型，默认为1     0 删除指定过滤报文    1 增加过滤报文    2 删除所有过滤报文
        
        Returns:
            None
        
        Raises:
            无
        
        """
        if isinstance(msg_id, str):
            msg_name = msg_id
            bus_obj = getattr(self._ipdu, bus_name)
            msg_signals_obj = getattr(bus_obj, msg_name)
        if self.bus_dict.get(bus_name) is None:
            if bus_name == "backbonefr":
                if isinstance(msg_id, str):
                    msg_slotid = msg_signals_obj.msg_slotid
                else:
                    msg_slotid = msg_id
                self.bus_dict["tosun_tc1034"].fr_filter_info_send(bus_name, msg_slotid, filter_type)
            else:
                if isinstance(msg_id, str):
                    msg_id = msg_signals_obj.msg_id
                else:
                    msg_id = msg_id
                self.bus_dict["tosun_tc1018"].can_filter_info_send(bus_name, msg_id, filter_type)

    def filter_msg(self, bus_name: str, msg_name: str):
        self._filter_msg(bus_name, msg_name)

    def filter_bus(self, bus_name: str):
        self._filter_msg(bus_name, 0)
        logger.info(f"{bus_name} open all msg filter")

    def filter_msg_all(self):
        for bus_name in self.tosun_busname:
            self.filter_bus(bus_name)
        for bus_name in self.tosun_busname_tc1034:
            self.filter_bus(bus_name)

    def cancel_filter_msg(self, bus_name: str, msg_name: str):
        self._filter_msg(bus_name, msg_name, filter_type=0)

    def cancel_filter_bus(self, bus_name: str):
        self._filter_msg(bus_name, 0, filter_type=0)
        logger.info(f"{bus_name} clear all msg filter")

    def cancel_filter_msg_all(self):
        for bus_name in self.tosun_busname:
            self.cancel_filter_bus(bus_name)
        for bus_name in self.tosun_busname_tc1034:
            self.cancel_filter_bus(bus_name)

    def cancel_fr_filter_msg_all(self):
        self.bus_dict["tosun_tc1034"].clear_fr_all_filter()

    def cancel_can_filter_msg_all(self):
        self.bus_dict["tosun_tc1018"].clear_can_all_filter()

    # ------------------------------------------------------------------------------------------------

    def set_accept_lin_data_flag(self, lin_bus, status):
        """
        设置检查lin信号的标志
        @param lin_bus: eg: cem_lin1
        @param status: eg: bool类型，True为开始接收检查数据；False为停止接收lin的检查数据
        """
        lin_obj = self.bus_dict[lin_bus]
        lin_obj.use_schedule_table = status

    def check_lin_schedule_table(self,
                                 lin_bus,
                                 table_name,
                                 allow_offset=60,
                                 specify_time=5,
                                 need_clear_lin_data=False):
        """
        检查lin的调度表
        @param lin_bus: eg: cem_lin1
        @param table_name: 调度表名，eg: Cem_Lin6Schedule01_CEM_LIN6
        @param specify_time: eg: 指定时间内的数据，默认5秒
        @param need_clear_lin_data: eg: 需要清除之前lin bus所接收的数据，默认为True
        @param allow_offset:允许偏差的范围，百分比，如允许50%误差，这里就是：50
        @return:
        """
        table_schedule_data = self._ipdu.get_lin_scheduleTable(lin_bus)
        single_table_schedule_data = table_schedule_data.get(table_name)

        logger.info(f"当前lin的调度表：{[i[2] for i in single_table_schedule_data]}")
        if not single_table_schedule_data:
            logger.error(f"没有发现：{table_name}，在{lin_bus}里面")
            raise AssertionError(f"没有发现：{table_name}，在{lin_bus}里面")

        lin_obj = self.bus_dict[lin_bus]
        if not isinstance(lin_obj, ToomossLin):
            raise AssertionError(f"输入的lin bus错误，请仔细核对。")
        lin_obj.use_schedule_table = True
        if need_clear_lin_data:
            lin_obj.clear_accept_queue_message()
        time.sleep(specify_time)

        match_data_list = []
        try:
            check_data_queue = copy.deepcopy(lin_obj.message_queue)
            logger.info(f"总线接收到的数据pid是：{[i[0] for i in check_data_queue]}")
            schedule_table_pid_list_cycle = cycle(single_table_schedule_data)
            schedule_pid_list = [j[2] for j in single_table_schedule_data]

            for pid_info in check_data_queue:
                if pid_info[0] in schedule_pid_list:
                    match_data_list.append(pid_info)

            if not match_data_list:
                logger.warning(f"接收到的数据中，没有发现匹配调度表的数据。")
                raise

            if len(match_data_list) >= 2:
                logger.info(f"接收到的开始时间：{match_data_list[0][1]},结束时间：{match_data_list[-1][1]}")
            accept_pid_list = [i[0] for i in match_data_list]
            logger.info(f"发现接收数据在调度表中的数据有: {accept_pid_list}")
            record_start_index = []
            for info in single_table_schedule_data:
                if info[2] == accept_pid_list[0]:
                    record_start_index.append(info[0])

            all_match_data = {}
            for index in record_start_index:
                single_match_data_list = []
                check_count = 0
                record_flag = False
                for schedule_message in schedule_table_pid_list_cycle:
                    if schedule_message[0] == index:
                        record_flag = True
                    if record_flag:
                        single_match_data_list.append(schedule_message[2])
                    if len(single_match_data_list) == len(match_data_list):
                        break
                    if check_count >= len(single_table_schedule_data):
                        if not record_flag:
                            break
                    check_count += 1
                if single_match_data_list:
                    all_match_data[index] = single_match_data_list

            if accept_pid_list not in all_match_data.values():
                raise AssertionError(f"接收到的lin数据调度顺序与调度表顺序不匹配")
            start_index = None
            for k, v in all_match_data.items():
                if v == accept_pid_list:
                    start_index = k
                    break
            logger.info(f"找到匹配调度数据的下标为：{start_index}")
            # start_data = check_data_queue.popleft()

            start_data = match_data_list.pop(0)
            check_start_pid = start_data[0]
            check_start_time = start_data[1]
            start_index += 1
            for index, single_pid_data in enumerate(match_data_list):
                for single_data in single_table_schedule_data:
                    if single_data[0] == start_index:
                        if single_data[0] == 0:
                            check_expect_time = single_table_schedule_data[-1][4]
                        else:
                            check_expect_time = single_table_schedule_data[single_data[0] - 1][4]

                        logger.info(f"now timestamp is:{single_pid_data[1]}, before timestamp is:{check_start_time}")
                        sub_time = abs((single_pid_data[1] - check_start_time) / 1000 - check_expect_time)
                        if check_expect_time == 0:
                            logger.warning(f"检查的期望调度时间是：0 秒")
                            raise

                        if (sub_time / check_expect_time) * 100 > allow_offset:
                            logger.warning(
                                f"queue index:{index + 2},check index:{single_data[0]}, pid:{single_pid_data[0]}: "
                                f"Real time interval is:{(single_pid_data[1] - check_start_time) / 1000}, "
                                f"expect times is:{check_expect_time},percentage of error:{(sub_time / check_expect_time) * 100}")
                            raise
                        check_start_time = single_pid_data[1]
                        if single_data[0] == single_table_schedule_data[-1][0]:
                            start_index = 0
                        else:
                            start_index += 1
                        break
        finally:
            lin_obj.use_schedule_table = False
            return match_data_list

    def bus_send(self, bus_name: str, id: int, data: list):
        # 推荐使用 ipdu中的，可以存tracelog
        inst = self.bus_dict[bus_name]
        if isinstance(inst, SocketCan):
            msg = can.Message(
                arbitration_id=id, data=data, is_fd=inst.is_fd, is_extended_id=False
            )
            inst.bus.send(msg)
        elif isinstance(inst, ToomossCan):
            msg = inst.can_msg(
                arbitration_id=id, dlc=len(data), data=data, is_extended_id=False
            )
            inst.send(msg)
        elif isinstance(inst, ToomossLin):
            inst.toomoss_set_salve_msg(pid=id, dlc=len(data), data=data)

    def bus_recv(self, bus_name: str, update_ipdu=False) -> list:
        # 推荐使用 ipdu 中的
        # retrun [(id, time_stamp, length, data)] or None
        inst = self.bus_dict[bus_name]
        msgs = inst.rx_update(update_ipdu=update_ipdu)
        return msgs

    def start_record_trace_log(self, file_rename: str):
        self.delete_status = self.__delete_old_asc_file()
        self.file_rename = file_rename
        self.file_exit = False
        if self.pcan_bus_obj:
            self.pcan_bus_obj.start_log()
        if self.stop_flag:
            if len(self.bus_obj) and self.delete_status:
                for bus_obj in self.bus_obj:
                    bus_obj.stop_log()
                    # time.sleep(2)
                    bus_obj.start_log()
            self.stop_flag = False
        else:
            if len(self.bus_obj) and self.delete_status:
                for bus_obj in self.bus_obj:
                    bus_obj.start_log()
        logger.info("=============== start bus record =======================")

    def stop_record_trace_log(self, is_record_status=True):
        logger.info(f'=============== stop bus record =======================')
        self.file_exit = True
        if self.pcan_bus_obj:
            self.pcan_bus_obj.stop_log()
        if len(self.bus_obj) and self.delete_status:
            for bus_obj in self.bus_obj:
                bus_obj.stop_log()
        time.sleep(0.1)
        self.__save_trace_log_to_asc()
        return self.__zip_trace_log_under_case(is_record_status)

    def __zip_trace_log_under_case(self, is_record_status=True):
        if is_record_status:
            asc_list = self.__get_asc_path()
            asc_zip = f"/root/test_case_log/{self.file_rename}_asc_{uuid.uuid4()}.zip"
            if asc_list and os.path.exists('/root/test_case_log'):
                res = os.system(f"zip -r {asc_zip} *.asc")
                if res == 0:
                    logger.info("zip asc file success")
                else:
                    logger.error(f"zip asc file failed! ret: {res}")
            if os.path.exists(asc_zip):
                # allure.attach.file(asc_zip, '总线报文', 'application/zip', 'zip')
                bos_client = BosApi()
                try:
                    remote_link = bos_client.put_and_get_url(
                        file_path=asc_zip,
                        target_path=f'SOA/allure_report/{get_time_str_year_month_day()}')
                except Exception as e:
                    logger.exception(f"总线报文日志上传bos失败: {e}")
                    allure.attach.file(asc_zip, '总线报文', 'application/zip', 'zip')
                else:
                    allure.attach(remote_link, '总线报文', allure.attachment_type.URI_LIST)
                return asc_zip
            else:
                return None
        else:
            return None

    def __save_trace_log_to_asc(self):
        with open(self.lin_trace_name, 'w') as f:
            f.write(self.lin_trace_log)
            self.lin_trace_log = ''
            self.lin_header_status = False

    def __delete_old_asc_file(self):
        res = os.system('rm -rf *.asc')
        if res == 0:
            logger.info(f'delete asc success')
            return True
        else:
            logger.error(f'delete asc failed, res:{res}, can not start log')
            return False

    def __get_asc_path(self):
        exec_shell('du -h Can.asc')
        exec_shell('du -h FlexRay.asc')
        file_list = os.listdir()
        asc_list = []
        for filename in file_list:
            if filename.endswith('asc'):
                if 'lin' not in filename:
                    asc_list.append(filename)
        return asc_list

    def start_all_cyclic_msg(self):
        for name, inst in self.bus_dict.items():
            if isinstance(inst, SocketCan) and not inst._started._flag:
                inst.start()
                self.pcan_bus_obj = inst
                logger.info(
                    "=============== BUS {} SocketCan STARTING =======================".format(
                        name
                    )
                )
            elif isinstance(inst, ToomossCan):
                inst.start()
                logger.info(
                    "=============== BUS {} ToomossCan STARTING =======================".format(
                        name
                    )
                )
            elif isinstance(inst, ToomossLin):
                inst.start()
                logger.info(
                    "=============== BUS {} ToomossLin STARTING =======================".format(
                        name
                    )
                )
            elif isinstance(inst, TosunBus):
                # sleep(1)
                inst.tosun_inimap_start()
                inst.connect_tosun_by_udp()
                inst.start()
                self.bus_obj.append(inst)
                logger.info(
                    "=============== Tosun BUS {}  STARTING =======================".format(
                        name
                    )
                )
                # sleep(2)

            sleep(0.1)

    def check_tosun_process(self):
        lin_statu_normal = True
        if ToomossStatus.STATUS != 0:
            lin_statu_normal = False
        for name, inst in self.bus_dict.items():
            if isinstance(inst, TosunBus):
                inst.check_tosun_process()
            if isinstance(inst, ToomossLin):
                if not lin_statu_normal:
                    inst.stop()
                    inst.join(20)
                sleep(0.1)

        if not lin_statu_normal:
            for name, inst in self.bus_dict.items():
                if isinstance(inst, ToomossLin):
                    channel = self.cfg.get("bus").get(name)
                    self.bus_dict[name] = ToomossLin(
                        name, channel, brate=19200, ipdu=self._ipdu,
                        callback=self.generate_asc_log
                    )
                    self.bus_dict[name].start()
                    logger.info(
                        "=============== BUS {} ToomossLin STARTING =======================".format(
                            name
                        )
                    )
                    sleep(0.1)

    def check_tosun_trace(self):
        for name, inst in self.bus_dict.items():
            if isinstance(inst, TosunBus):
                inst.check_tosun_trace()

    def stop_all_cyclic_msgs(self):
        tosuncan = None
        for name, inst in self.bus_dict.items():
            if isinstance(inst, SocketCan) and inst._started._flag:
                inst.bus.socket.close()
            elif isinstance(inst, ToomossCan):
                inst.stop()
            elif isinstance(inst, ToomossLin):
                inst.stop()
            elif isinstance(inst, TosunBus):
                inst.stop()
            sleep(0.1)

        logger.info("===================== 检查总线线程是否全部停止 ====================")
        check_flag = None
        for name, inst in self.bus_dict.items():
            try:
                check_start_time = time.time()
                inst.join(20)  # 防止lin等线程没有彻底结束掉
                check_end_time = time.time()
                check_time = check_end_time - check_start_time
                if check_time >= 20:
                    logger.warning(f'{name} thread is not stop, check_time:{check_time}')
                    check_flag = False
                else:
                    logger.info(
                        "=============== BUS {} stop success =======================".format(
                            name
                        )
                    )
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/bus_app.py")
                logger.error(f'{name} thread is not stop, error:{e}')
        if check_flag is not False:
            logger.info("===================== 全部总线线程已停止 ====================")
        else:
            logger.warning("===================== 全部总线线程没有全部停止 ====================")

    def pause_all_cyclic_msgs(self):
        for name, inst in self.bus_dict.items():
            if isinstance(inst, SocketCan) and inst._started._flag:
                inst.pause_flag = True

    def resume_all_cyclic_msgs(self):
        for name, inst in self.bus_dict.items():
            if isinstance(inst, SocketCan) and inst._started._flag:
                inst.pause_flag = False

    def set_new_signal_value_in_captured_msg(
            self,
            cls_signal_obj,
            msg_signals_info: type,
            bmuws_info,
            captured_msg,
            new_signal_value,
            captured_msg_result=True,
            bus_obj_arg=None,
    ):
        if bus_obj_arg is None:
            bus_obj = msg_signals_info.bus_obj
        else:
            bus_obj = bus_obj_arg

        bus_name = bus_obj.bus_name

        if not captured_msg_result:
            return bus_name, bus_obj, msg_signals_info.msg_id, captured_msg

        # Mask (with &= unmask) out the old signal_value, and Or in the new signal_value.
        #
        if bmuws_info is None:
            # All of this signal's bits are in a single-byte.
            captured_msg.data[cls_signal_obj.byte] &= cls_signal_obj.unmask
            captured_msg.data[cls_signal_obj.byte] |= (
                    new_signal_value << cls_signal_obj.shift
            )
        else:
            # Multi-byte or straddling-two-bytes signal.

            # First the actual_signal_value's LSbyte is copied into the signal's LSbyte.
            # Then the actual_signal_value is right-shifted, to prepare for copying its MSbyte.
            #
            if bus_name in self.dbc_obj_dict.keys():
                bmuws_info = reversed(bmuws_info)

            # The new_signal_value's LSbyte goes into the signal's first byte, and next into the signal's last byte.
            """
            The problem is that the shift must be applied to 'new_signal_value' before the mask (otherwise the bits 
            ignored by the mask will be ignored). 
            And, the 'new_signal_value' should be only shifted by the amount of bits actually encoded. 
            """
            for byte, mask, unmask, width, shift in bmuws_info:
                # Clean out the signal's existing content.
                captured_msg.data[byte] &= unmask

                # In the new_signal_value, keep only this signal_byte's bits,
                # and shift to them to the correct bit position in the msg.
                captured_msg.data[byte] |= (new_signal_value << shift) & mask

                # Throw away the LSbyte, so we can process the MSbyte next.
                new_signal_value >>= 8 - shift

        msg_id = msg_signals_info.msg_id

        return bus_name, bus_obj, msg_id, captured_msg

    def write_bus_msg(self, bus_name, bus_obj, msg_id, captured_msg, wait=0.0):
        if bus_name not in self.dbc_obj_dict.keys():
            bus_obj.write_single_msg(msg_id, captured_msg.data, wait=wait)
        else:
            bus_obj.modify_cyclic_data(msg_id, captured_msg.data)

    def send_pwm(self, bus_name: str, RunTimeOfUs=1000, frequency=1000, polarity=0, precision=1000,
                 dutyCycle=250, ) -> tuple:
        """
        bus_name：总线名称，仅支持lin总线
        RunTimeOfUs：发送时间，单位微妙，RunTimeOfUs=0，代表一直输出PWM
        返回结果为元组，如果第一个元素为0，则执行成功，否则为失败，第二个元素为失败描述信息
        """
        if bus_name in self.bus_dict:
            if bus_name.startswith("cem_lin"):
                inst = self.bus_dict[bus_name]
                ret, detail = inst.toomoss_init_pwm_then_start(RunTimeOfUs=RunTimeOfUs, frequency=frequency,
                                                               polarity=polarity, precision=precision,
                                                               dutyCycle=dutyCycle)
                logger.info(f"{ret} ==> {detail}")
                self._stop_cem_lin(bus_name)
                self._start_cem_lin(bus_name)
            else:
                logger.info(f"404  ==> send_pwm 仅支持lin总线!")
        else:
            logger.info(f"404  ==> 总线名称书写有误!")

    def _start_cem_lin(self, lin_name):
        for name, inst in self.bus_dict.items():
            logger.info(f"{name}: {type(inst)}")
            if name == lin_name:
                self.bus_dict[name] = ToomossLin(
                    name, self.cfg.get("bus").get(name), brate=19200, ipdu=self._ipdu, callback=None
                )
                self.bus_dict[name].start()
                logger.info("=============== BUS {} ToomossLin start success =========".format(name))

    def _stop_cem_lin(self, lin_name):
        for name, inst in self.bus_dict.items():
            if isinstance(inst, ToomossLin):
                if name == lin_name:
                    inst.stop()
                    self.bus_dict[name] = None
                    logger.info("=============== BUS {} ToomossLin stop success =======".format(name))


def tosun_process_check():
    """
    检查上位机上是否有其它未关闭的tosun进程在运行，如果有，则重载进程
    """
    check_cmd = f"ps -ef | grep IniMap | grep -v grep"
    pi = subprocess.Popen(
        check_cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding='utf-8',
    )
    stdout = pi.stdout.read()
    if stdout:
        logger.info("命令执行结果：\n{}".format(stdout))
        stdout = stdout.split('\n')
        pid_list = []
        for s in stdout:
            if s:
                s = ' '.join(s.split())  # 合并连续的空格
                s = s.split(' ')
                pid_list.append(s[1])
        if len(pid_list):
            kill_pid_str = ''
            for pid in pid_list:
                kill_pid_str += pid
                kill_pid_str += ' '
            check_cmd = f"kill -9 {kill_pid_str}"
            pi = subprocess.Popen(
                check_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                encoding='utf-8',
            )
            time.sleep(1)
            stdout = pi.stdout.read()
            if stdout:
                logger.info("error: {}".format(stdout))
                logger.info("Tosun process kill fail")
                time.sleep(1)
                return False
            else:
                logger.info("Tosun process kill success")
                time.sleep(1)
                return True
    else:
        # logger.info("没有残留的 Tosun 进程")
        return True


if __name__ == "__main__":
    # Work Path: ecu_simulator/
    # Command: python3 sdk/bus_app.py
    add_cyclic_msg_with_data_run(
        0x53F,
        [0x3F, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00],
        0.64,
        "can0",
        bitrate=500000,
    )
    # add_cyclic_msg_with_data_run(0x53F, [0x3F, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00], 0.64, "can1", bitrate=500000, is_fd=True)
    add_cyclic_msg_with_data_run(
        0x53F,
        [0x3F, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00],
        0.64,
        "can2",
        bitrate=500000,
    )
    add_cyclic_msg_with_data_run(
        0x53F,
        [0x3F, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00],
        0.64,
        "can3",
        bitrate=500000,
    )
    # add_cyclic_msg_with_data_run(0x53F, [0x3F, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00], 0.64, "can4", bitrate=500000)
    # add_cyclic_msg_with_data_run(0x53F, [0x3F, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00], 0.64, "can5", bitrate=500000)
    add_cyclic_msg_with_data_run(
        0x53F,
        [0x3F, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00],
        0.64,
        "can1",
        bitrate=500000,
    )
    sleep(2)
    from sdk.i_signal_i_pdu import ISignalIPdu

    cls_path = "sdk/data/mars1/can_lin_fr_cls/v_0_6_5"
    ipdu = ISignalIPdu(cls_path, dut_ecu=["BGM"])
    sleep(0.5)
    busapp = BusApp(ipdu)

    ipdu.start_all_time_control()
    busapp.start_all_cyclic_msg()

    # lin_test = busapp.bus_dict.get("cem_lin4")
    # lin_test5 = busapp.bus_dict.get("cem_lin5")
    # sleep(0.5)
    # i=1
    # while i < 20:
    #     i += 1
    #     lin_test.recv()
    #     lin_test5.recv()
    #     # lin_test.toomoss_set_salve_msg(0x11, 8, [i,0x22,0x33,0x44,0x55,0x66,0x77,0x88])
    #     sleep(0.5)

    # update signal
    sleep(2)
    ipdu.bodycan_ppodbodyfr01_doorpassopenreqoutdswt2_psdnotpsd3_psd()

    ipdu.cem_lin6_awmcem_lin6fr01_actvresplrintfltactrflt2_flt_fault()

    sleep(2)
    result, realvalue, expectedvalue = ipdu.check(
        ipdu.bodycan.CemBodyFr121, 'InteCleanUnpleSmell', 'OnOff1_Off'
    )  # 0x114
    logger.info(
        "result {}, realvalue {}, expectedvalue {}".format(
            result, realvalue, expectedvalue
        )
    )

    sleep(2)
    result, realvalue, expectedvalue = ipdu.check(
        ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrIntFltActrFlt2', 1
    )  # 0x20
    logger.info(
        "result {}, realvalue {}, expectedvalue {}".format(
            result, realvalue, expectedvalue
        )
    )
    # sleep(100)
    ipdu.time_control_stop()
    busapp.stop_all_cyclic_msgs()
    close_cyclic_msg()
