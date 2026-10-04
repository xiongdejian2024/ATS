# -*- coding: utf-8 -*-
"""
@File        : tosunbus.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2023-08-17 18:06
@Description : tosun_flexray tosun_can new  混合 小程序版本
@Examples    :
"""

import sys
import os
import re
from pathlib import Path

from xat_ecu.legacy.common.file_handle import parent_dir

current_path = os.path.dirname(os.path.realpath(__file__))
import json
import time
import inspect
import socket
import threading
from xat_ecu.legacy.common.logger import logger
from ctypes import *
import platform
from time import sleep
import subprocess
from subprocess import Popen
from signal import signal
import signal
import struct

from xat_ecu.legacy.sdk.driver.tosun.get_fr_config import *
from xat_ecu.legacy.sdk.driver.tosun.libTSCANAPI import *
# from ecu_simulator.sdk.driver.tosun.libTSCANAPI.TSEnumdefine import *
# from ecu_simulator.sdk.driver.tosun.libTSCANAPI.TSCommon import (
#     size_t,
#     s32,
# )

from xat_ecu.legacy.common.data_type_handing import *
from xat_ecu.legacy.common.time_handle import *
import multiprocessing
from multiprocessing import shared_memory
from multiprocessing.managers import SharedMemoryManager
from multiprocessing import Process, Value, Manager
from typing import List, Tuple, Optional
from copy import deepcopy


def get_device_info(DeviceCount: int = 0):
    AFManufacturer = c_char_p()
    AFProduct = c_char_p()
    AFSerial = c_char_p()
    tscan_get_device_info(
        DeviceCount, AFManufacturer, AFProduct, AFSerial
    )  # DeviceCount 获取设备信息(选择要连接的设备   0)

    return (
        AFManufacturer.value,
        AFProduct.value,
        AFSerial.value,
    )

def get_device_name():
    device_name_info = {}
    initialize_lib_tscan(True, True, False)  # 函数初始化

    # scan tosun 设备
    ADeviceScan = s32(0)
    tscan_scan_devices(ADeviceScan)

    logger.info(f"FR current_device num is {ADeviceScan.value}")

    if ADeviceScan.value > 0:
        for i in range(ADeviceScan.value):
            manufacturer, product, serial = get_device_info(i)
            logger.info(
                f"FR 设备信息 {i+1}： manufacturer is {manufacturer}, product is {product}, serial is {serial}"
            )
            product = product.split()[-1]
            if product in ["TC1034", "TC1018"]:
                device_name_info[product] = serial
            else:
                logger.error("获得的Tosun设备不符合期望")
    else:
        logger.info("没有发现 FR 设备")

    finalize_lib_tscan()

    return device_name_info

class TLIBFlexrayHW(Structure):
    _pack_ = 1
    _fields_ = [("FHWIdx", c_int32),
                ("StopNet",c_int32),
                ("LogFlag",c_int32),
                ("AMsg", TLIBFlexray),
    ]
    def __str__(self):
        return str(self.FHWIdx) +"  "+str(self.AMsg)
PLIBFlexrayHW = POINTER(TLIBFlexrayHW)   

class TLIBCANFDHW(Structure):
    _pack_ = 1
    _fields_ = [("FHWIdx", c_int32),
                ("CyclicTime",c_float),
                ("LogFlag",c_int32),
                ("AMsg", TLIBCANFD),
    ]
    def __str__(self):
        return str(self.FHWIdx) +"  "+str(self.AMsg)
PLIBCANFDHW = POINTER(TLIBCANFDHW) 

class TosunBusD(threading.Thread):
    # class TosunFlexray(Process):
    """
    Provide interfaces:
      1. send single message
      2. read single message
      3. send cyclic message with modification
         add/remove/pause/resume cyclic msg, modify data
         add_dual_rate_cyclic_msg
    """

    def __init__(
            self,
            bus_name: list,
            channel: dict,
            mock_msg_id_list=None,
            ipdu=None,
            dbc_json=None,
            fibex_path=r'',
            dut_ecu=["BGM"],
            device_name_info={"TC1034": "E7CB383B263B8955", "TC1018": "609C84C2E4BAF720"},
            issavelog=0,   # 默认保存日志
    ):
        """
        Initialize a SocketCan object.
        :param bus_name: bus name, such as 'bodycan', 'ept'
        :param channel: channel interface, such as (1409286394, 0)
        :param brateconfig: brateconfig of socket can, default is CANConfig_CONSTANT.UTA05XX.bt_500k
        :param dbc_json: dbc_json file which defined cyclic message
        """
        threading.Thread.__init__(self, name="TosunBus", daemon=True)
        # Process.__init__(self, name=bus_name, daemon=True)
        self.issavelog = issavelog 
        self.stopnet = 0
        self.channel = channel
        self.canchannel_to_canbus = {}
        for canbus_name, canbus_info in self.channel.items():
            if "can" in canbus_name:
                self.canchannel_to_canbus[self.channel[canbus_name][1]] = canbus_name

        self.dbc_json = dbc_json

        self.bus_name_list = bus_name
        self.exit_flag = False  # True means stop sending cyclic messages tasks

        if self.dbc_json is None:
            self.msgs = []
        else:
            with open(self.dbc_json) as data:
                self.msgs = json.load(data)

        # New
        if ipdu:
            self.ipdu_instance = ipdu
            self.bus_pdu_dict = ipdu.bus_pdu_dict
        else:
            logger.error("没有传入 ipdu 实例 参数")
        self.pause_flag = False
        self.rx_exit_flag = False

        self.f = None

        self.fibex = fibex_path

        self.mock_msg_id_list = mock_msg_id_list

        self.cyc = None

        # device_name_info = get_device_name()

        if "backbonefr" in self.channel:
            self.host = '127.0.0.1'
            self.port = 8001
            self.ini_path = "./configfr.ini"
            self.tosun_serial = device_name_info.get("TC1034")
            self.taskset = "taskset -c 2,3"
        else:
            self.host = '127.0.0.1'
            self.port = 8003
            self.ini_path = "./configcan.ini"
            self.tosun_serial = device_name_info.get("TC1018")
            self.taskset = "taskset -c 0,1"

        self.client_socket = None
        self.p = None

        self.TC1018 = None
        self.TC1034 = None
        self.logpath = None

        # 生成同星配置
        if device_name_info:
            device_serials = []
            msg_infos_list = []

            i = -1
            for device_name, device_serial in device_name_info.items():
                i += 1
                device_serials.append(device_serial)
                if device_name == "TC1034":
                    self.TC1034 = i
                    self.logpath = "./FlexRay.asc"
                elif device_name == "TC1018":
                    self.TC1018 = i
                    self.logpath = "./Can.asc"
            
            for busname in bus_name:
                tx_msg_obj_list = get_tx_msg_name_list(getattr(self.ipdu_instance,busname), dut_ecu)
                pdu_dict = self.bus_pdu_dict[busname]
                if busname == "backbonefr":
                    HWidx = self.TC1034
                    msg_infos = get_fr_msg_info_list(tx_msg_obj_list, pdu_dict, busname, HWidx, self.channel.get(busname)[1])
                else:
                    HWidx = self.TC1018
                    msg_infos = get_can_msg_info_list(tx_msg_obj_list, pdu_dict, busname, HWidx, self.channel.get(busname)[1])
                msg_infos_list.append(msg_infos)
            write_config(msg_infos_list, tosun_serial=self.tosun_serial, file_path=self.ini_path, FlexRayDSTPORT=self.port, isSaveLog= 0 if self.issavelog else 1)

        else:
            logger.error("没有发现同星设备")

    def fr_tx_cycle(self):
        # 每隔100ms检查是否Fr 需要恢复发送

        while self.rx_exit_flag is False:
            if self.ipdu_instance.fr_resume_flag is True:
                self.stopnet = 0
                # VddmBackboneNmFr01
                pdu_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                slot_id = 2
                cyclecode = baseCycle_to_cyclecode(0, 4)
                length = 32
                self.fr_send(
                    slot_id=slot_id,
                    cyclecode=cyclecode,
                    data=pdu_data,
                    dlc=length,
                )
                self.ipdu_instance.fr_resume_flag = None
            elif self.ipdu_instance.fr_resume_flag is False:
                self.stopnet = 1
                # VddmBackboneNmFr01
                pdu_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                slot_id = 2
                cyclecode = baseCycle_to_cyclecode(0, 4)
                length = 32
                self.fr_send(
                    slot_id=slot_id,
                    cyclecode=cyclecode,
                    data=pdu_data,
                    dlc=length,
                )
                self.ipdu_instance.fr_resume_flag = None
                
            sleep(0.1)       

    def fr_tx_cycle_start(self):
        thread = threading.Thread(
            target=self.fr_tx_cycle,
            name="tosun_fr_tx",
            daemon=True,
        )
        thread.start()

        return thread  

    def can_tx_cycle(self):
        # 每隔1ms检查是否有哪些can报文需要发送
        # msg_id = msg_obj["msg_id"]

        while self.exit_flag is False:
            # if msg_id == 0x150:
            #     time1 = time.time()
            #     time1 = time.time()
            if not self.pause_flag:
                for busname, pdu_dict in self.bus_pdu_dict.items():
                    if "can" in busname and busname in self.bus_name_list:
                        for msg_name, msg_dict in pdu_dict.items():
                            tx_change = msg_dict.get("tx_change")
                            tx_flag = msg_dict["tx_flag"]
                            if tx_flag == True and tx_change == True:
                                # if crc_sig_groups:  # crc sig group (dataid)
                                #     for sig_group in crc_sig_groups:
                                #         self.ipdu_instance.set_crc_count(
                                #             msg_cls_obj,
                                #             sig_group,
                                #             do_cntr=getattr(msg_cls_obj, (sig_group + "_cntr"))
                                #             if hasattr(msg_cls_obj, (sig_group + "_cntr"))
                                #             else None,
                                #             do_crc=getattr(msg_cls_obj, (sig_group + "_crc"))
                                #             if hasattr(msg_cls_obj, (sig_group + "_crc"))
                                #             else None,
                                #         )
                                data = msg_dict["pdu_data"]
                                msg_id = msg_dict["msg_id"]
                                length = msg_dict["msg_length"]
                                cycle_time = msg_dict["msg_cycle"]
                                if cycle_time is None:
                                    cycle_time = 0
                                
                                # lock.acquire()
                                # logger.info(msg_id)
                                msg_dict["tx_change"] = None
                                self.can_send(busname, data, msg_id, cycle_time)
                                

                                # if msg_id == 0x150:
                                #     time2 = time.time()
                                #     time3 = time2 - time1
                                #     if time3 >= 0.001:
                                #         logger.info(f"========= {time3} =========")

                                # if msg_id == 0x166:
                                #     logger.info(msg_id)
                            elif tx_flag == False and tx_change == True:
                                data = msg_dict["pdu_data"]
                                msg_id = msg_dict["msg_id"]
                                length = msg_dict["msg_length"]
                                cycle_time = -1
                                
                                # lock.acquire()
                                # logger.info(msg_id)
                                msg_dict["tx_change"] = None
                                self.can_send(busname, data, msg_id, cycle_time)
            sleep(0.001)


    def can_tx_cycle_start(self):
        # logger.info(msg_name)
        thread = threading.Thread(
            target=self.can_tx_cycle,
            name="tosun_can_tx",
            daemon=True,
        )
        thread.start()

        return thread

    def run(self):
        """
        Start tasks to transmit each cyclic message read from json file
        :return:
        """
        try:
            # create a socket object
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # 查看默认发送接收缓冲区大小
            recv_buff = self.client_socket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
            send_buff = self.client_socket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
            print(f'默认接收缓冲区大小：{recv_buff}。默认发送缓冲区大小：{send_buff}')

            # self.client_socket_fr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # self.client_socket_can = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # cmd = "/root/quansun_clear/ecu-simulator/xat_ecu/legacy/sdk/driver/tosun/libTSCANAPI/linux/IniMap"
            # cmd = f"{self.taskset} ../../venv/lib/python3.8/site-packages/xat_ecu/legacy/sdk/driver/tosun/libTSCANAPI/linux/IniMap {self.ini_path} {self.logpath}"   # cpu 亲和性
            cmd = f"{Path(parent_dir) / f'sdk/driver/tosun/libTSCANAPI/linux/IniMap {self.ini_path} {self.logpath}'}"
            self.p = Popen(cmd, shell=True, close_fds=True, preexec_fn=os.setsid)
            # self.p = Popen([cmd], stdout=subprocess.PIPE)
            sleep(1)
            logger.info(f"=======================  Tosun {self.tosun_serial} start success ======================")

            # connection to host on the port.
            self.client_socket.bind((self.host, self.port))
            # self.client_socket_fr.bind((self.host, self.port))
            # self.client_socket_can.bind(('127.0.0.1', 8003))

            # if self.TC1018 is not None:
            #     self.can_tx_cycle_start()

            # if self.TC1034 is not None:
            #     self.fr_tx_cycle_start()

            # self.rx_update_ipdu()
            
            sleep(1)

        except (AttributeError, OSError) as err:
            error_foo = err  # For debugging.
            logger.error("Tosun run error: {}".format("Tosun Bus"))
            logger.error(err)

    def start_log(self):
        """
        0为log启动，1为暂停
        """
        self.issavelog = 0
        data = [0x3F, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        msg_id = 0x53F
        cycle_time = 0
        for busname in self.channel:
            if "backbonefr" == busname:
                # VddmBackboneNmFr01
                pdu_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                slot_id = 131076
                cyclecode = baseCycle_to_cyclecode(0, 4)
                length = 32
                self.fr_send(
                    slot_id=slot_id,
                    cyclecode=cyclecode,
                    data=pdu_data,
                    dlc=length,
                )
            elif "can" in busname:
                self.can_send(busname, data, msg_id, cycle_time)

    def stop_log(self):
        """
        0为log启动，1为暂停
        """
        self.issavelog = 1
        data = [0x3F, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        msg_id = 0x53F
        cycle_time = 0
        for busname in self.channel:
            if "backbonefr" == busname:
                # VddmBackboneNmFr01
                pdu_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                slot_id = 2
                cyclecode = baseCycle_to_cyclecode(0, 4)
                length = 32
                self.fr_send(
                    slot_id=slot_id,
                    cyclecode=cyclecode,
                    data=pdu_data,
                    dlc=length,
                )
            elif "can" in busname:
                self.can_send(busname, data, msg_id, cycle_time)
 
    def stop_IniMap(self):
        if self.p:
            self.pid = self.p.pid
            try:
                self.p.terminate()
                self.p.wait()
                os.killpg(self.pid, signal.SIGKILL)

                # 获取当前目录下的所有文件
                files = os.listdir()
                # 定义要匹配的文件名模式
                pattern = r'^config.*\.ini$'
                # 遍历文件列表
                for file in files:
                    # 使用正则表达式匹配文件名
                    if re.match(pattern, file):
                        # 删除符合条件的文件
                        os.remove(file)

            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/tosun/tosunbus_d.py")
                logger.warning("Stop Tosun IniMap Error : {}".format(e))
        else:
            logger.warning("IniMap 没有启动，不需要去关闭")

    def fr_rx_update(self, Msg, busname="backbonefr"):
        # update self.bus_pdu_dict
        time_stamp = Msg.FTimeUs
        fdir = Msg.FDir
        # flag = Msg.FFrameFlags
        slot_id = Msg.FSlotId
        length = Msg.FActualPayloadLength
        # crc = Msg.FFrameCRC
        cycle = Msg.FCycleNumber
        data = list(Msg.FData[:length])

        BaseCycle = None
        CycleRepetition = None
        msg_id = None
        for msg_name, msg_dict in self.bus_pdu_dict.get(busname).items():
            # msg_cls_obj = getattr(bus_cls_obj, msg_name)   # 频繁会卡住
            if msg_dict.get("msg_slotid") == slot_id:
                BaseCycle = msg_dict.get("msg_base_cycle")
                CycleRepetition = msg_dict.get("msg_repetition")
                remainder = cycle % CycleRepetition
                if remainder == BaseCycle:
                    msg_id = msg_dict.get("msg_id")
                    tx_change = msg_dict.get("tx_change")
                    tx_flag = msg_dict.get("tx_flag")
                    # logger.info(f"tx_change is {tx_change}")
                    # logger.info(f"tx_flag is {tx_flag}")

                    # if msg_id == 327938:
                    #     if self.cyc is None:
                    #         self.cyc = cycle
                    #     else:
                    #         cccyc = cycle - self.cyc
                    #         if cccyc < 0:
                    #             cccyc = 64 + cccyc
                    #         if cccyc == 2:
                    #             self.cyc = cycle
                    #         else:
                    #             logger.error(f"{cycle} - {self.cyc} = {cccyc} ")
                    #             # logger.error(
                    #             #     f"  -------------   {AFlexRay.contents.FCycleNumber}"
                    #             # )
                    #             self.cyc = cycle

                    # if msg_id == 3604481:
                    #     if self.cyc is None:
                    #         self.cyc = cycle
                    #     else:
                    #         cccyc = cycle - self.cyc
                    #         if cccyc < 0:
                    #             cccyc = 64 + cccyc
                    #         if cccyc == 1:
                    #             self.cyc = cycle
                    #         else:
                    #             logger.error(f"{cycle} - {self.cyc} = {cccyc} ")
                    #             # logger.error(
                    #             #     f"  -------------   {Msg.FCycleNumber}"
                    #             # )
                    #             self.cyc = cycle

                    # 打印某个报文
                    # elif msg_id == 3604481:
                    #     data = msg_dict["pdu_data"]
                    #     data_print = (
                    #         DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(
                    #             data
                    #         )
                    #     )
                    #     # logger.debug("FlexrayMsg[{}].Data = {}".format(i, data_print))
                    #     trace_log = "[{}] {}  {}  FlexrayMsg: id[{}] [{}  {}/{}] [cycele:{}]  [{}]  {}".format(
                    #         time_stamp,
                    #         bus_name,
                    #         fdir,
                    #         msg_id,
                    #         slot_id,
                    #         BaseCycle,
                    #         CycleRepetition,
                    #         cycle,
                    #         length,
                    #         data_print,
                    #     )
                    #     logger.info(trace_log)

                    if fdir == 1:
                        fdir = "TX"
                        # msg_cls_obj = getattr(bus_cls_obj, msg_name)
                        # crc_sig_groups = msg_cls_obj.sig_group_dataid_dict
                        if not self.pause_flag:
                            # if crc_sig_groups or msg_dict.get("tx_change"):
                            if tx_change:
                                # # logger.info(Msg)
                                # if crc_sig_groups:  # 判断是否需要 e2e 或 是否需要正常更新值
                                #     # 判断是否需要 e2e, 处于对linux性能考虑，这里做e2e, 不在下面pre_tx 里做
                                #     for sig_group in crc_sig_groups:
                                #         self.ipdu_instance.set_crc_count(
                                #             msg_cls_obj,
                                #             sig_group,
                                #             do_cntr=getattr(
                                #                 msg_cls_obj, (sig_group + "_cntr")
                                #             )
                                #             if hasattr(
                                #                 msg_cls_obj, (sig_group + "_cntr")
                                #             )
                                #             else None,
                                #             do_crc=getattr(
                                #                 msg_cls_obj, (sig_group + "_crc")
                                #             )
                                #             if hasattr(
                                #                 msg_cls_obj, (sig_group + "_crc")
                                #             )
                                #             else None,
                                #         )

                                msg_dict["tx_change"] = None

                                pdu_data = msg_dict["pdu_data"]

                                if msg_dict.get("tx_flag") is True:
                                    self.stopnet = 0
                                elif msg_dict.get("tx_flag") is False:
                                    self.stopnet = 1

                                cyclecode = baseCycle_to_cyclecode(
                                    BaseCycle, CycleRepetition
                                )
                                self.fr_send(
                                    slot_id=slot_id,
                                    cyclecode=cyclecode,
                                    data=pdu_data,
                                    dlc=length,
                                )

                    elif fdir == 0:
                        fdir = "RX"
                        if msg_dict["rx_flag"] is not None:
                            msg_dict["pdu_data"] = data
                            msg_dict["time_stamp"] = time_stamp
                            msg_dict["rx_flag"] = True

                    # else:
                    #     # RX ---- fdir == 0      TX ----  fdir == 1
                    #     logger.info("fdir is {}".format(fdir))
                    #     logger.error("Fdir 不符合预期")
                    break
                else:
                    BaseCycle = None
                    CycleRepetition = None
                    msg_id = None

    def can_rx_update(self, Msg, busname="connectivitycanfd"):
        # update self.bus_pdu_dict

        msg_id = Msg.FIdentifier

        # Tosun 时间戳
        time_stamp = Msg.FTimeUs
        # # 上位机时间戳
        # time_stamp = time.time()

        length = Msg.FDLC
        length = DLC_DATA_BYTE_CNT[length] 
        data = Msg.FData[:length]
        for message, msg_dict in self.bus_pdu_dict.get(busname).items():
            if msg_dict["rx_flag"] is not None:
                if msg_id == msg_dict["msg_id"]:
                    msg_dict["pdu_data"] = data
                    msg_dict["time_stamp"] = time_stamp
                    msg_dict["rx_flag"] = True

    def rx_update_ipdu(self):
        while self.rx_exit_flag is False:
            Msg, bus_type = self.recv_new()
            if bus_type == 0 :
                self.fr_rx_update(Msg)
            else:
                canbus_name = self.canchannel_to_canbus.get(Msg.FIdxChn)
                if canbus_name not in ["diagnosticcan", None]:
                    self.can_rx_update(Msg, canbus_name)
                else:
                    logger.warning(f"收到错误报文：{Msg}")
            # logger.info(Msg)
            # sleep(0.0005)
        sleep(0.2)

    # def rx_update_ipdu_start(self):
    #     thread = threading.Thread(
    #         target=self.rx_update_ipdu, name="Tosun Flexray rx_update_ipdu"
    #     )
    #     thread.start()

    def rx_update_stop(self):
        # self.rx_exit_flag.value += 1

        self.rx_exit_flag = True

    # --------------------   tosun high level api -----------------------------------
    def recv_new(self):
        # 读取fr/can数据
        # Receive no more than 1024 bytes
        msg, addr = self.client_socket.recvfrom(1024)
        if(len(msg) >= 312):   # 现在是 314
            Msg_HW = cast(msg, PLIBFlexrayHW).contents
            Msg = Msg_HW.AMsg
            bus_type = 0   # fr
            logger.info(Msg)

            # bus_chn =  Msg.FIdxChn
            time_stamp = Msg.FTimeUs
            fdir = Msg.FDir
            # flag = Msg.FFrameFlags
            slot_id = Msg.FSlotId
            length = Msg.FActualPayloadLength
            # crc = Msg.FFrameCRC
            cycle = Msg.FCycleNumber
            data = list(Msg.FData[:length])

            msg_id = slotid_cyclecode_to_msgid(slot_id, cycle)
            # logger.info([msg_id, time_stamp, length, data])
            return (msg_id, time_stamp, length, data), bus_type

            # if Msg.FSlotId == 47:
            #     cycle = Msg.FCycleNumber
            #     if self.cyc is None:
            #         self.cyc = cycle
            #     else:
            #         cccyc = cycle - self.cyc
            #         if cccyc < 0:
            #             cccyc = 64 + cccyc
            #         if cccyc == 1:
            #             self.cyc = cycle
            #         else:
            #             logger.info(f"{cycle} - {self.cyc} = {cccyc} ")
            #             # logger.error(
            #             #     f"  -------------   {AFlexRay.contents.FCycleNumber}"
            #             # )
            #             self.cyc = cycle


        elif (len(msg) >= 88):   # 现在是 92
        # else:
            Msg_HW = cast(msg, PLIBCANFDHW).contents
            Msg = Msg_HW.AMsg
            bus_type = 1  # can
            # logger.info(Msg)

            msg_id = Msg.FIdentifier
            time_stamp = Msg.FTimeUs
            # logger.info(time_stamp)
            length = Msg.FDLC
            length = DLC_DATA_BYTE_CNT[length] 
            # logger.info(length)
            data = Msg.FData[:length]
            bus_chn = Msg.FIdxChn
            # logger.info([msg_id, time_stamp, length, data])
            return (msg_id, time_stamp, length, data, bus_chn), bus_type
        else:
            logger.error("非期望长度报文")
            Msg = None
            bus_type = None
        # Msg.FData[0] = 0xf1
        # logger.info(Msg)
        return Msg, bus_type

    def fr_send(
            self,
            slot_id: int,
            cyclecode: int,
            data: List[int],
            IdxChn=0,
            ChannelMask=1,
            # ChannelMask=7,
            dlc=32,
    ):  # #ChannelMask=3 两通道    ChannelMask=1 通道A   ChannelMask=7 把buffer发完，不跳帧
        fr_tx_frame = TLIBFlexray()
        fr_tx_frame.FIdxChn = IdxChn
        fr_tx_frame.FSlotId = slot_id
        fr_tx_frame.FCycleNumber = cyclecode
        fr_tx_frame.FChannelMask = ChannelMask
        fr_tx_frame.FActualPayloadLength = dlc

        for index in range(dlc):
            try:
                fr_tx_frame.FData[index] = data[index]
            except IndexError:
                fr_tx_frame.FData[index] = 0

        fr_tx_frame_HW = TLIBFlexrayHW()
        fr_tx_frame_HW.FHWIdx = self.TC1034
        fr_tx_frame_HW.StopNet = self.stopnet
        fr_tx_frame_HW.LogFlag = self.issavelog
        fr_tx_frame_HW.AMsg = fr_tx_frame
        # logger.info(fr_tx_frame_HW)

        self.client_socket.sendto(fr_tx_frame_HW, (self.host, self.port - 1))
        # self.client_socket_fr.sendto(fr_tx_frame_HW, ("127.0.0.1",8000))
    
    def can_send(
            self,
            busname: str,
            data: list,
            msg_id: int,
            cycle_time=None,
    ):  
        
        # data = msg_obj["pdu_data"]
        # msg_id = msg_obj["msg_id"]
        # length = msg_obj["msg_length"]
        # cycle_time = msg_obj["msg_cycle"]

        AChnIdx = self.channel.get(busname)[1]
        FFDProperties = 3 if "canfd" in busname else 0
        can_tx_frame = TLIBCANFD(
            FIdxChn=AChnIdx,
            FDLC=len(data),
            FIdentifier=msg_id,
            FProperties=1,
            FFDProperties=FFDProperties,
            FData=data,
        )

        can_tx_frame_HW = TLIBCANFDHW()
        can_tx_frame_HW.FHWIdx = self.TC1018
        if cycle_time is None:
            cycle_time = 0
        can_tx_frame_HW.CyclicTime = cycle_time
        can_tx_frame_HW.LogFlag = self.issavelog
        can_tx_frame_HW.AMsg = can_tx_frame
        # logger.info(can_tx_frame_HW)

        self.client_socket.sendto(can_tx_frame_HW, (self.host, self.port - 1))
        # self.client_socket_can.sendto(can_tx_frame_HW, ("127.0.0.1",8002))

    def stop(self):
        """
        Stop each task that is sending cyclic messages.
        :return:
        """
        try:
            # self.rx_exit_ flag.value += 1

            self.rx_exit_flag = True
            self.exit_flag = True
            sleep(0.2)
            self.client_socket.close()
            # self.client_socket_fr.close()
            # self.client_socket_can.close()
            self.stop_IniMap()
        except AttributeError:
            logger.error('Tosun Flexray stop error: {}'.format("Tosun Bus"))

   

if __name__ == '__main__':
    # Work Path: 
    # cmd : 
    def get_device_info1(DeviceCount: int = 0):
        AFManufacturer = c_char_p()
        AFProduct = c_char_p()
        AFSerial = c_char_p()
        tscan_get_device_info(
            DeviceCount, AFManufacturer, AFProduct, AFSerial
        )  # DeviceCount 获取设备信息(选择要连接的设备   0)

        return (
            AFManufacturer.value,
            AFProduct.value,
            AFSerial.value,
        )


    initialize_lib_tscan(True, True, False)  # 函数初始化

    # scan tosun 设备
    ADeviceScan = s32(0)
    tscan_scan_devices(ADeviceScan)

    print(f"FR current_device num is {ADeviceScan.value}")

    if ADeviceScan.value > 0:
        for i in range(ADeviceScan.value):
            manufacturer, product, serial = get_device_info1(i)
            print(
                f"FR 设备信息 {i+1}： manufacturer is {manufacturer}, product is {product}, serial is {serial}"
            )
    else:
        print("没有发现 FR 设备")

    finalize_lib_tscan()