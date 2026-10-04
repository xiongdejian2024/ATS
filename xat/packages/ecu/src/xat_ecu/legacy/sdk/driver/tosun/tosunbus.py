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
import psutil
from pathlib import Path
from psutil import TimeoutExpired
from xat_ecu.legacy.common import exception_error

from xat_ecu.legacy.common.file_handle import parent_dir
from interface.nuc_app import exec_shell
from xat_ecu.legacy.common import exception_error
from xat_ecu.legacy.common.error_code import StatusCode
from xat_ecu.legacy.common.exception_error import error_check
from xat_ecu.legacy.common.error_callback import error_callback

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
from subprocess import Popen, PIPE
from signal import signal
import signal
import struct
import glob

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

    # logger.info(f"FR current_device num is {ADeviceScan.value}")
    logger.info(f"扫描得到同星设备数量是：{ADeviceScan.value}")

    if ADeviceScan.value > 0:
        for i in range(ADeviceScan.value):
            manufacturer, product, serial = get_device_info(i)
            logger.info(
                f"同星设备信息 {i + 1}： manufacturer is {manufacturer}, product is {product}, serial is {serial}"
            )
            product = product.split()[-1]
            if "TC1034" in product.decode():
                device_name_info["TC1034"] = serial.decode()
            elif "TC1018" in product.decode():
                device_name_info["TC1018"] = serial.decode()
            else:
                logger.error("获得的Tosun设备不符合期望")
    else:
        logger.info("没有发现 FR 设备")

    finalize_lib_tscan()

    return device_name_info


class TLIBFlexrayHW(Structure):
    _pack_ = 1
    _fields_ = [("FHWIdx", c_int32),
                ("StopNet", c_int32),
                ("LogFlag", c_int32),
                ("AMsg", TLIBFlexray),
                ]

    def __str__(self):
        return str(self.FHWIdx) + "  " + str(self.AMsg)


PLIBFlexrayHW = POINTER(TLIBFlexrayHW)


class TLIBCANFDHW(Structure):
    _pack_ = 1
    _fields_ = [("FHWIdx", c_int32),
                ("CyclicTime", c_float),
                ("LogFlag", c_int32),
                ("AMsg", TLIBCANFD),
                ]

    def __str__(self):
        return str(self.FHWIdx) + "  " + str(self.AMsg)


PLIBCANFDHW = POINTER(TLIBCANFDHW)


# ======================= socket 筛选报文新增 ======================================================
	# u32 AMsgID;
	# u8 AMsgType;
	# u8 AChnIdx;
	# u8 AComKey;
	# u8 ARes1;
class TPASSMSGINFO(Structure):
    _pack_ = 1
    _fields_ = [("AMsgID", c_int32),
                ("AMsgType",c_uint8),
                ("AChnIdx",c_uint8),
                ("AComKey", c_uint8),
                ("ARes1", c_uint8),
    ]

PPASSMSGINFO = POINTER(TPASSMSGINFO)
# =============================================================================


class TosunBus(threading.Thread):
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
            issavelog=0,  # 默认保存日志
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
        self.fr_diag_flag = None

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
                tx_msg_obj_list = get_tx_msg_name_list(getattr(self.ipdu_instance, busname), dut_ecu)
                pdu_dict = self.bus_pdu_dict[busname]
                if busname == "backbonefr":
                    HWidx = self.TC1034
                    msg_infos = get_fr_msg_info_list(tx_msg_obj_list, pdu_dict, busname, HWidx,
                                                     self.channel.get(busname)[1])
                else:
                    HWidx = self.TC1018
                    msg_infos = get_can_msg_info_list(tx_msg_obj_list, pdu_dict, busname, HWidx,
                                                      self.channel.get(busname)[1])
                msg_infos_list.append(msg_infos)
            write_config(msg_infos_list, tosun_serial=self.tosun_serial, file_path=self.ini_path,
                         FlexRayDSTPORT=self.port, isSaveLog=0 if self.issavelog else 1)

        else:
            logger.error("没有发现同星设备")

        self.diag_flag = None
        self.cb = None
        self.cb_fr = None
        self.listen_frame_with_0x27 = 0
        self.listen_frame_first_flag_with_0x27 = False

    def fr_tx_cycle(self):
        # 每隔100ms检查是否Fr 需要恢复发送

        while self.rx_exit_flag is False:
            if self.ipdu_instance.fr_resume_flag is True:
                self.stopnet = 0
                # VddmBackboneNmFr01
                pdu_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0]
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
                pdu_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0]
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
                                try:
                                    msg_type = getattr(getattr(self.ipdu_instance, busname), msg_name).msg_type
                                except Exception:
                                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/tosun/tosunbus.py")
                                    msg_type = None
                                self.can_send(busname, data, msg_id, cycle_time, can_type = msg_type)
                                try:
                                    logger.debug(f"{busname}总线已经通过UDP周期：{cycle_time} 发送：{msg_id}：{bytes(data).hex()}")
                                except Exception as e:
                                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/tosun/tosunbus.py")
                                    logger.warning(f"CAN打印日志报错：{e}")
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
                                try:
                                    msg_type = getattr(getattr(self.ipdu_instance, busname), msg_name).msg_type
                                except Exception:
                                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/tosun/tosunbus.py")
                                    msg_type = None
                                self.can_send(busname, data, msg_id, cycle_time, can_type = msg_type)
            else:
                # 释放cpu负载
                sleep(1)
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

    def tosun_inimap_start(self, cycle_send_status: Union[int, str] = 1):
        logger.info(" =========  tosun inimap start ==============")
        cmd = f"{Path(parent_dir) / f'sdk/driver/tosun/libTSCANAPI/linux/IniMap {self.ini_path} {self.logpath}'}"
        # cmd = f"{Path(parent_dir) / f'sdk/driver/tosun/libTSCANAPI/linux/IniMap {self.ini_path} {self.logpath} {cycle_send_status}'}"  # 启动就只打开bus，不发报文
        logger.info(cmd)

        self.p = Popen(cmd, shell=True, stdout=subprocess.PIPE, close_fds=True, preexec_fn=os.setsid, text=True)

        start_time = time.time()
        while time.time() - start_time < 2:
            # 检查命令的状态
            if self.p.poll() is None:
                # 执行其他操作，或者等待一段时间
                time.sleep(0.5)
            else:
                break
        time.sleep(0.5)
        if not self.p.returncode:
            logger.info(f"=======================  Tosun {self.tosun_serial} start success ======================")
        else:
            with error_check(StatusCode.TOSUN_MINI_PROGRAM_START_ERR, exception_error.TosunError, error_callback):
                self.p.terminate()
                logger.error(f"同星{self.tosun_serial}初始化失败，原因是:{self.p.stdout.read()}，请检查同星是否有问题")
                raise
        # sleep(1)

    def connect_tosun_by_udp(self):
        with error_check(StatusCode.TOSUN_MINI_PROGRAM_CONNECT_ERR, exception_error.TosunError, error_callback):
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 启用端口复用
            self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.client_socket.bind((self.host, self.port))
        # try:
        #     self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #     # 启用端口复用
        #     self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #     self.client_socket.bind((self.host, self.port))
        # except (AttributeError, OSError) as err:
        #     raise exception_error.TosunError(f"连接同星小程序失败，原因是:{err}")

    def check_tosun_process(self):
        if self.client_socket:
            check_cmd = f"ps -ef | grep {self.ini_path} | grep -v grep | wc -l"
            result = exec_shell(command=check_cmd)
            stdout = result.get('output')
            if stdout:
                try:
                    ret = stdout.split('\n')[0]
                except IndexError:
                    logger.warning(f"检查同星小程序的命令可能有异常，索引越界")
                else:
                    if int(ret) != 2:
                        logger.error(f"{self.ini_path}进程应该有2个， 实际有{int(ret)}，开始重启同星小程序")
                        # kill_cmd = f"ps -ef | grep {self.ini_path}" + " | grep -v grep | awk '{print $2}' | xargs kill -9"
                        # exec_shell(command=kill_cmd)
                        self.reset()
                        logger.info(f"重启同星小程序成功")
                    # else:
                    #     logger.info(f"{self.ini_path}进程存在")
                    #     filter_channel = {"bodyalmcanfd1", "bodyalmcanfd2", "diagnosticcan", "propulsioncan", "chassiscan1", "chassiscan2"} | self.ipdu_instance.pause_bus_info
                    #     # 休眠场景总线可能为None, 过滤掉暂停总线的通道、需要发唤醒帧和三个默认通道
                    #     check_channel = list(set(list(self.channel.keys())) - filter_channel)
                    #     if check_channel:
                    #         is_active = self.ipdu_instance.check_bus_recv_message(check_channel[0])
                    #         if is_active:
                    #             logger.info(f'当前的检查的通道为：{check_channel[0]}, 总线报文正常输出')
                    #         else:
                    #             logger.info(f'当前的检查的通道为：{check_channel[0]}, 总线报文输出为{is_active}， 开始重启同星小程序')
                    #             kill_cmd = f"ps -ef | grep {self.ini_path}" + " | grep -v grep | awk '{print $2}' | xargs kill -9"
                    #             exec_shell(command=kill_cmd)
                    #             self.reset()
                    #             logger.info(f"重启同星小程序成功")
                    #     else:
                    #         logger.warning('当前可检查的通道数量为空, 可能暂停了所有总线')
            else:
                logger.error(f"未检查到{self.ini_path}进程，开始重启同星小程序")
                self.reset()
                logger.info(f"重启同星小程序成功")
                self.stop_log()

    def check_tosun_trace(self):
        if self.client_socket:
            if not os.path.exists(f'{self.logpath}'):
                logger.warning(f"未检查到{self.logpath}文件，开始重启同星小程序")
                self.reset()
                logger.info(f"重启同星小程序成功")
            else:
                if os.path.getsize(f'{self.logpath}') < 100 * 1024:
                    logger.warning(f"{self.logpath}文件中没有报文数据，开始重启同星小程序")
                    self.reset()
                    logger.info(f"重启同星小程序成功")

    def reset(self):
        # self.pause_flag = True
        # self.client_socket.close()
        self.stop_IniMap(clear_ini_map=False)
        sleep(0.2)
        self.tosun_inimap_start(cycle_send_status='')
        self.stop_log()
        # self.connect_tosun_by_udp()
        # self.pause_flag = False

    def run(self):
        """
        Start tasks to transmit each cyclic message read from json file
        :return:
        """
        try:
            # create a socket object
            # self.client_socket_fr.bind((self.host, self.port))
            # self.client_socket_can.bind(('127.0.0.1', 8003))

            if self.TC1018 is not None:
                self.can_tx_cycle_start()

            if self.TC1034 is not None:
                self.fr_tx_cycle_start()

            self.rx_update_ipdu()

            sleep(1)

            if self.TC1018 is not None:
                logger.info(" =========  TC1018 end ==============")

            if self.TC1034 is not None:
                logger.info(" =========  TC1034 end ==============")

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
                pdu_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0]
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
                pdu_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0]
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

    # def stop_IniMap(self, clear_ini_map=True):
    #     if self.p:
    #         self.pid = self.p.pid
    #         try:
    #             self.p.terminate()
    #             self.p.wait()
    #             os.killpg(self.pid, signal.SIGKILL)
    #             if clear_ini_map:
    #                 # 获取当前目录下的所有文件
    #                 files = os.listdir()
    #                 # 定义要匹配的文件名模式
    #                 pattern = r'^config.*\.ini$'
    #                 # 遍历文件列表
    #                 for file in files:
    #                     # 使用正则表达式匹配文件名
    #                     if re.match(pattern, file):
    #                         # 删除符合条件的文件
    #                         os.remove(file)

    #         except Exception as e:
    #             logger.warning("Stop Tosun IniMap Error : {}".format(e))
    #     else:
    #         logger.warning("IniMap 没有启动，不需要去关闭")

    def stop_IniMap(self, clear_ini_map=True):
        if self.p:
            try:
                # 终止子进程并等待其退出
                # self.p.terminate()
                # self.p.wait(timeout=5)  # 设置超时时间，避免无限等待
                # if self.p.poll() is None:  # 如果进程仍在运行
                #     self.p.kill()  # 强制杀死进程
                parent_proc = psutil.Process(self.p.pid)
                for child_proc in parent_proc.children(recursive=True):
                    child_proc.kill()
                parent_proc.kill()

                if clear_ini_map:
                    # 使用glob模块查找所有以'config'开头、'.ini'结尾的文件
                    for file in glob.glob('config*.ini'):
                        try:
                            os.remove(file)
                            logger.info(f"Removed INI file: {file}")
                        except OSError as e:
                            logger.warning(f"Failed to remove INI file {file}: {e}")

            except (OSError, TimeoutExpired) as e:
                logger.warning("Error stopping Tosun IniMap: {}".format(e))
            except Exception as e:
                logger.exception(f"停止同星IniMap出现异常：原因是{str(e)}")
        else:
            logger.info("IniMap is not running, no need to stop.")

    def set_listen_frame_first_flag_with_0x27(self, flag):
        self.listen_frame_first_flag_with_0x27 = flag

    def set_listen_frame_with_0x27(self, time_value):
        self.listen_frame_with_0x27 = time_value

    def fr_rx_update(self, Msg, busname="backbonefr"):
        # update self.bus_pdu_dict
        try:
            time_stamp = Msg.FTimeUs / 10 ** 6
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

            # 使用sot_id=39来检测BGM发出来的fr帧信号，监听BGM重启后多久后能发出帧数据
            if slot_id == 0x27 and not self.listen_frame_first_flag_with_0x27:
                try:
                    logger.info(f"BGM重启后，监听到Flexray第一帧数据耗时:{float(time.time()-self.listen_frame_with_0x27)}")
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/tosun/tosunbus.py")
                    logger.warning(f"BGM重启后，监听Flexray第一帧数据耗时错误:{e}")
                self.listen_frame_first_flag_with_0x27 = True

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
                                msg_dict["time_stamp"] = time_stamp / 10 ** 6
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
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/tosun/tosunbus.py")
            logger.warning(f"解析报文错误：{e}")

    def can_rx_update(self, Msg, busname="connectivitycanfd"):
        # update self.bus_pdu_dict
        try:
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
                        msg_dict["time_stamp"] = time_stamp / 10 ** 6
                        msg_dict["rx_flag"] = True
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/tosun/tosunbus.py")
            logger.warning(f"解析报文错误：{e}")

    def rx_update_ipdu(self):
        while self.rx_exit_flag is False:
            if not self.pause_flag:
                Msg, bus_type = self.recv_new()
                # logger.info(f"{Msg}")
                if Msg is None:
                    continue

                chn_id = Msg.FIdxChn
                if bus_type == 0:
                    self.fr_rx_update(Msg)
                    # logger.info(f"{Msg}")
                else:
                    canbus_name = self.canchannel_to_canbus.get(chn_id)
                    # if canbus_name not in ["diagnosticcan", None]:
                    if canbus_name not in [None]:
                        self.can_rx_update(Msg, canbus_name)
                    else:
                        logger.warning(f"收到错误报文：{Msg}")
                # logger.info(f"{Msg}")
                # sleep(0.0005)
            else:
                # 释放cpu负载
                sleep(1)
                if self.TC1018 is not None:
                    logger.info(" =========  TC1018 释放cpu负载zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz ==============")

                if self.TC1034 is not None:
                    logger.info(" =========  TC1034 释放cpu负载zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz ==============")
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
    def register_diagcan_callback(self, callback):
        self.cb = callback
        self.diag_flag = True

    def unregister_diagcan_callback(self):
        self.diag_flag = False

    def register_diagfr_callback(self, callback):
        self.cb_fr = callback
        self.fr_diag_flag = True

    def unregister_diagfr_callback(self):
        self.fr_diag_flag = False

    def recv_new(self):
        # 读取fr/can数据
        # Receive no more than 1024 bytes
        msg, addr = self.client_socket.recvfrom(1024)
        try:
            if (len(msg) >= 312):  # 实际 314
                Msg_HW = cast(msg, PLIBFlexrayHW).contents
                Msg = Msg_HW.AMsg
                bus_type = 0  # fr

                if Msg.FSlotId == 47:
                    cycle = Msg.FCycleNumber
                    if self.cyc is None:
                        self.cyc = cycle
                    else:
                        cccyc = cycle - self.cyc
                        if cccyc < 0:
                            cccyc = 64 + cccyc
                        if cccyc == 1:
                            self.cyc = cycle
                        else:
                            logger.debug(f"{cycle} - {self.cyc} = {cccyc} ")
                            # logger.error(
                            #     f"  -------------   {AFlexRay.contents.FCycleNumber}"
                            # )
                            self.cyc = cycle
                if self.fr_diag_flag:
                    if Msg.FSlotId > 64:
                        self.cb_fr(Msg)

            # elif(len(msg) >= 88):
            else:  # 实际 92
                Msg_HW = cast(msg, PLIBCANFDHW).contents
                Msg = Msg_HW.AMsg
                bus_type = 1  # can

                if self.diag_flag:
                    msg_id = Msg.FIdentifier
                    if msg_id >= 0x500:
                        self.cb(Msg)

            # Msg.FData[0] = 0xf1
            # logger.info(Msg)
            return Msg, bus_type
        except Exception as e:
            # logger.error(f"recv_new error: {e}")
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/tosun/tosunbus.py")
            logger.error(f"同星接收到消息和处理报错: {e}")
            return None, None

    def recv(self, bus_chn=None, msgid=None):
        # 读取fr/can 报文数据，配合性能接口 recv_pdu_d，只返回纯接收的报文数据
        # Receive no more than 1024 bytes
        # msgid FR 里暂用slot_id
        # logger.info(bus_chn)
        # logger.info(msgid)
        msg, addr = self.client_socket.recvfrom(1024)
        length = len(msg)
        if length >= 312:  # 实际 314
            Msg_HW = cast(msg, PLIBFlexrayHW).contents
            Msg = Msg_HW.AMsg
            if Msg.FDir == 1:  # TX数据 不要    1 ---- TX    0 ---- RX
                return None
            slot_id = Msg.FSlotId
            if slot_id != msgid:
                return None
            # bus_chn =  Msg.FIdxChn
            time_stamp = Msg.FTimeUs / 10 ** 6
            # flag = Msg.FFrameFlags
            slot_id = Msg.FSlotId
            length = Msg.FActualPayloadLength
            # crc = Msg.FFrameCRC
            cycle = Msg.FCycleNumber
            data = list(Msg.FData[:length])
            msg_id = slot_id  # FR 暂用 slot_id 代替
            # msg_id = slotid_cyclecode_to_msgid(slot_id, cycle)
            # logger.info([msg_id, time_stamp, length, data])
            return (msg_id, time_stamp, length, data)
        elif length >= 88:  # 实际 92
            Msg_HW = cast(msg, PLIBCANFDHW).contents
            Msg = Msg_HW.AMsg
            if Msg.FProperties == 1:  # TX数据 不要    1 ---- TX    0 ---- RX
                return None
            if bus_chn is None:  # 返回所有can数据
                bus_id = Msg.FIdxChn
                msg_id = Msg.FIdentifier
            else:
                bus_id = Msg.FIdxChn
                if bus_id != bus_chn:
                    return None
                msg_id = Msg.FIdentifier
                if msg_id != msgid:
                    return None

            time_stamp = Msg.FTimeUs / 10 ** 6
            # logger.info(time_stamp)
            length = Msg.FDLC
            length = DLC_DATA_BYTE_CNT[length]
            # logger.info(length)
            data = Msg.FData[:length]

            # logger.info([msg_id, time_stamp, length, data])
            return (msg_id, time_stamp, length, data, bus_id)
        else:
            logger.warning(f"收到同星的数据长度不符合期望，收到的数据长度未{length}")
            return None

    def clear_recv_buffer(self, timeout=1):
        """
        清空接收缓冲区,并设置了socket的超时时间
        
        Args:
            timeout (float, optional): 超时时间，默认为1秒。设置socket的超时时间，防止程序因等待接收数据而挂起。
        
        Returns:
            None
        
        """

        # python清空linux  udp socket 缓存，删掉历史缓存
        start_time = time.time() 
        self.client_socket.settimeout(timeout)  # 设置超时为0.1秒
        while time.time() - start_time < timeout:
            try:
                data, addr = self.client_socket.recvfrom(1024)  
                if not data:
                    logger.debug("清理UDP缓存，没有接收到数据,退出循环")
                    break  # 如果没有接收到数据，退出循环
            except socket.timeout:
                # 如果没有在超时期限内接收到数据，则假定缓冲区为空
                logger.debug("清理UDP缓存，超时,退出循环")
                break
        # self.client_socket.settimeout(None) # 取消超时设置  
        logger.info("清理了 UDP 缓存")

    def pause_cycle_tx_rx(self):
        # 配合性能接口 recv_pdu_d， 释放cpu负载
        self.pause_flag = True

    def resume_cycle_tx_rx(self):
        # 配合性能接口 recv_pdu_d， 释放cpu负载
        self.pause_flag = False

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
            can_type=None,
    ):

        # data = msg_obj["pdu_data"]
        # msg_id = msg_obj["msg_id"]
        # length = msg_obj["msg_length"]
        # cycle_time = msg_obj["msg_cycle"]

        AChnIdx = self.channel.get(busname)[1]
        if can_type:
            FFDProperties = 3 if can_type == "can_fd" else 0
        else:
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
    def can_filter_info_send(
            self,
            busname: str,
            msg_id: int,
            filter_type: int,
        ):  

        AChnIdx = self.channel.get(busname)[1] if busname != "can" else 0

        # 总线类型  0：can  1:backbonefr
        if "can" in busname: 
            bustype = 0
        elif "backbonefr" in busname:
            bustype = 1

        can_filter_info_frame = TPASSMSGINFO()
        can_filter_info_frame.AMsgID = msg_id   #id   0 对象是整个bus     xx 对象是单个msg
        can_filter_info_frame.AMsgType = bustype     # 总线类型  0：can  1:backbonefr
        can_filter_info_frame.AChnIdx = AChnIdx      # 通道 
        can_filter_info_frame.AComKey = filter_type   # 0 删除指定过滤报文    1 增加过滤报文    2 删除所有过滤报文

        self.client_socket.sendto(can_filter_info_frame, (self.host, self.port - 1))

    def fr_filter_info_send(
            self,
            busname: str,
            slot_id: int,
            filter_type: int,
        ):  

        AChnIdx = self.channel.get(busname)[1]

        # 总线类型  0：can  1:backbonefr
        if "can" in busname: 
            bustype = 0
        elif "backbonefr" in busname:
            bustype = 1

        fr_filter_info_frame = TPASSMSGINFO()
        fr_filter_info_frame.AMsgID = slot_id   #id   0 对象是整个bus     xx 对象是单个msg    fr对应的是slotid
        fr_filter_info_frame.AMsgType = bustype     # 总线类型  0：can  1:backbonefr
        fr_filter_info_frame.AChnIdx = AChnIdx      # 通道 
        fr_filter_info_frame.AComKey = filter_type   # 0 删除指定过滤报文    1 增加过滤报文    2 删除所有过滤报文

        self.client_socket.sendto(fr_filter_info_frame, (self.host, self.port - 1))
    
    def clear_can_all_filter(self):
        self.can_filter_info_send("can", 0, 2)
    
    def clear_fr_all_filter(self):
        self.fr_filter_info_send("backbonefr", 0, 2)

    def stop(self, clear_ini_map=True):
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
            self.stop_IniMap(clear_ini_map)
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
                f"FR 设备信息 {i + 1}： manufacturer is {manufacturer}, product is {product}, serial is {serial}"
            )
    else:
        print("没有发现 FR 设备")

    finalize_lib_tscan()
