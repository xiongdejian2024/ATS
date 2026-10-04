# -*- coding: utf-8 -*-
"""
@File        : tosun_flexray.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2023-08-17 18:06
@Description : tosun_flexray new  小程序版本
@Examples    :
"""

import sys
import os

from xat_ecu.legacy.sdk.driver.tosun.libTSCANAPI import TLIBFlexray

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

from xat_ecu.legacy.sdk.driver.tosun.libTSCANAPI import *
from xat_ecu.legacy.sdk.driver.tosun.libTSCANAPI.TSEnumdefine import *
from xat_ecu.legacy.sdk.driver.tosun.libTSCANAPI.TSCommon import (
    size_t,
    s32,
)

from xat_ecu.legacy.common.data_type_handing import *
from xat_ecu.legacy.common.time_handle import *
import multiprocessing
from multiprocessing import shared_memory
from multiprocessing.managers import SharedMemoryManager
from multiprocessing import Process, Value, Manager
from typing import List, Tuple, Optional
from copy import deepcopy


class TLIBFlexrayHW(Structure):
    _pack_ = 1
    _fields_ = [("FHWIdx", c_int32),
                ("AMsg", TLIBFlexray),
    ]
    def __str__(self):
        return str(self.FHWIdx) +"  "+str(self.AMsg)
PLIBFlexrayHW = POINTER(TLIBFlexrayHW) 

# class TosunFlexray:
class TosunFlexray(threading.Thread):
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
            bus_name,
            channel: list,
            mock_msg_id_list=None,
            ipdu=None,
            dbc_json=None,
            fibex_path=r'',
            ARxTx=READ_TX_RX_DEF.TX_RX_MESSAGES,
            ADataBufferSize=100
    ):
        """
        Initialize a SocketCan object.
        :param bus_name: bus name, such as 'bodycan', 'ept'
        :param channel: channel interface, such as (1409286394, 0)
        :param brateconfig: brateconfig of socket can, default is CANConfig_CONSTANT.UTA05XX.bt_500k
        :param dbc_json: dbc_json file which defined cyclic message
        """
        threading.Thread.__init__(self, name=bus_name, daemon=True)
        # Process.__init__(self, name=bus_name, daemon=True)
        self.bus_name = bus_name  # name of channel, such as 'etp'
        self.channel = channel
        self.dbc_json = dbc_json

        self.exit_flag = False  # True means stop sending cyclic messages tasks
        self.msg_task = {}  # Tasks to sending cyclic messages
        self.timestamp = None
        self.dlc = None
        if self.dbc_json is None:
            self.msgs = []
        else:
            with open(self.dbc_json) as data:
                self.msgs = json.load(data)

        # self.shm_fr = shared_memory.SharedMemory(ipdu.shm_main.name)

        # New
        if ipdu:
            self.pdu_dict = ipdu.bus_pdu_dict[self.bus_name]
            self.bus_cls_obj = getattr(ipdu, self.bus_name)
            self.ipdu_instance = ipdu
        else:
            logger.error("没有传入 ipdu 实例 参数")
        self.pause_flag = False
        self.rx_exit_flag = False
        # self.rx_exit_flag = Value("i", 0)
        self.f = None

        self.fibex = fibex_path
        self.ADeviceHandle = size_t(0)

        if isinstance(self.channel[0], str):
            self.ADeviceSerial = bytes(self.channel[0], encoding="utf-8")
        else:
            self.ADeviceSerial = None
            logger.warning("没有给出同星的设备号, 后续当只有一个同星设备处理")
        self.AChnIdx = c_int(self.channel[1])

        self.ARxTx = ARxTx
        self.ADataBufferSize_raw = ADataBufferSize
        self.ADataBufferSize = c_int(ADataBufferSize)
        self.ACount = c_int(0)

        self.mock_msg_id_list = mock_msg_id_list

        self.cyc = None

        self.host = '127.0.0.1'
        self.port = 8001
        self.client_socket = None
        self.p = None

    def initialize(self, AEnableFIFO=True, AEnableTurbe=True, hardtime=False):
        # hardtime ---  True  usb接入时间开始      False  每次connect时间开始
        initialize_lib_tscan(AEnableFIFO, AEnableTurbe, hardtime)

    def scan_device(self):  # 获取 ADeviceSerial
        ADeviceScan = s32(0)
        tscan_scan_devices(ADeviceScan)
        return ADeviceScan.value

    def get_device_info(self, DeviceCount: int = 0):
        AFManufacturer = c_char_p()
        AFProduct = c_char_p()
        AFSerial = c_char_p()
        tscan_get_device_info(
            DeviceCount, AFManufacturer, AFProduct, AFSerial
        )  # 获取设备信息(选择要连接的设备   0)

        return (
            AFManufacturer.value,
            AFProduct.value,
            AFSerial.value,
        )

    def connect(self, ADeviceSerial=b''):  # open 设备 （根据 序列号）
        # logger.info(f"self.ADeviceSerial is {self.ADeviceSerial}")
        if self.ADeviceSerial:
            tsapp_connect(self.ADeviceSerial, self.ADeviceHandle)
        else:
            tsapp_connect(ADeviceSerial, self.ADeviceHandle)

    def disconnect(self):  # close 设备
        tsapp_disconnect_by_handle(self.ADeviceHandle)

    def stop_flexray(self, ATimeoutMs=1000):  # 停止 FR
        tsflexray_stop_net(
            self.ADeviceHandle, self.AChnIdx, c_int(ATimeoutMs)
        )

    def start_flexray(self, ATimeoutMs=1000):  # 启动 FR
        tsflexray_start_net(
            self.ADeviceHandle, self.AChnIdx, c_int(ATimeoutMs)
        )

    def flush_rx_buffer(self):
        tsfifo_clear_flexray_receive_buffers(
            self.ADeviceHandle, self.AChnIdx
        )

    def start_logging(self, filepath="", exe_type=0):
        # 开始保存该同行设备的日志  asc 格式
        if filepath:
            filepath_byte = bytes(filepath, encoding="utf-8")
            tsapp_start_logging(
                self.ADeviceHandle, filepath_byte, exe_type
            )
            logger.info(f"开始记录日志 {filepath}")
        else:
            filepath_default = "/root/TosunFlexray_" + get_time_str_now() + ".asc"
            filepath_default_byte = bytes(filepath_default, encoding="utf-8")
            tsapp_start_logging(
                self.ADeviceHandle, filepath_default_byte, exe_type
            )
            logger.info(f"开始记录日志 {filepath_default}")

    def stop_logging(self, exe_type=0):
        # exe_type   要和start_logging  里面的一致
        tsapp_stop_logging(exe_type)
        logger.info(f"停止记录 TosunFlexray 日志")

    def fr_filter(self, slot_id, base_cycle, rep_cycle):
        # 接口，未验证
        tsfifo_add_flexray_pass_filter(
            self.ADeviceHandle, self.AChnIdx, slot_id, base_cycle, rep_cycle
        )

    def config_by_manual(
            self,
            trigger_lists: list,
            is_open_a=True,
            is_open_b=True,
            wakeup_chn=0,
            enable100_a=True,
            enable100_b=True,
            is_show_nullframe=False,
            is_Bridging=False,
            ATimeoutMs=1000,
    ):
        # trigger_slot_id_cycle_code    type： list      [(trigger_slot_id, cycle_code，config_byte)]
        # is_Bridging  桥接 内部短接
        ANodeIndex = self.AChnIdx
        AFrameNumLength = [32] * len(trigger_lists)
        AFrameLengthArray = (c_int * len(trigger_lists))(*AFrameNumLength)
        AFrameNum = len(trigger_lists)

        self.fr_config = TLibFlexray_controller_config(
            is_open_a=is_open_a,
            is_open_b=is_open_b,
            wakeup_chn=wakeup_chn,
            enable100_a=enable100_a,
            enable100_b=enable100_b,
            is_show_nullframe=is_show_nullframe,
            is_Bridging=is_Bridging,
        )

        i = 0
        self.fr_trigger = (TLibTrigger_def * len(trigger_lists))()
        for trigger_list in trigger_lists:
            trigger_slot_id = trigger_list[0]
            cycle_code = trigger_list[1]
            config_byte = trigger_list[2]

            self.fr_trigger[i].frame_idx = i
            self.fr_trigger[i].slot_id = trigger_slot_id
            self.fr_trigger[i].cycle_code = cycle_code
            self.fr_trigger[i].config_byte = config_byte
            self.fr_trigger[i].recv = 0
            i += 1

        tsflexray_set_controller_frametrigger(
            self.ADeviceHandle,
            ANodeIndex,
            self.fr_config,
            AFrameLengthArray,
            AFrameNum,
            self.fr_trigger,
            AFrameNum,
            ATimeoutMs,
        )

    def on_rx_tx_flexray(self, obj, AFlexRay):
        # 使用同星回调
        time_stamp = AFlexRay.contents.FTimeUs
        fdir = AFlexRay.contents.FDir
        # flag = AFlexRay.contents.FFrameFlags
        slot_id = AFlexRay.contents.FSlotId
        length = AFlexRay.contents.FActualPayloadLength
        # crc = AFlexRay.contents.FFrameCRC
        cycle = AFlexRay.contents.FCycleNumber
        data = list(AFlexRay.contents.FData[:length])

        # # fifo RX
        # time_stamp = AFlexRay.FTimeUs
        # fdir = AFlexRay.FDir
        # # flag = AFlexRay.FFrameFlags
        # slot_id = AFlexRay.FSlotId
        # length = AFlexRay.FActualPayloadLength
        # # crc = AFlexRay.FFrameCRC
        # cycle = AFlexRay.FCycleNumber
        # data = list(AFlexRay.FData[:length])

        BaseCycle = None
        CycleRepetition = None
        msg_id = None
        for msg_name, msg_dict in self.pdu_dict.items():
            # msg_cls_obj = getattr(self.bus_cls_obj, msg_name)   # 频繁会卡住
            if msg_dict.get("msg_slotid") == slot_id:
                BaseCycle = msg_dict.get("msg_base_cycle")
                CycleRepetition = msg_dict.get("msg_repetition")
                remainder = cycle % CycleRepetition
                if remainder == BaseCycle:
                    msg_id = msg_dict.get("msg_id")

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
                    #             #     f"  -------------   {AFlexRay.contents.FCycleNumber}"
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
                    #         self.bus_name,
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
                        msg_cls_obj = getattr(self.bus_cls_obj, msg_name)
                        crc_sig_groups = msg_cls_obj.sig_group_dataid_dict
                        if not self.pause_flag:
                            if crc_sig_groups or msg_dict.get("tx_change"):
                                if crc_sig_groups:  # 判断是否需要 e2e 或 是否需要正常更新值
                                    # 判断是否需要 e2e, 处于对linux性能考虑，这里做e2e, 不在下面pre_tx 里做
                                    for sig_group in crc_sig_groups:
                                        self.ipdu_instance.set_crc_count(
                                            msg_cls_obj,
                                            sig_group,
                                            do_cntr=getattr(
                                                msg_cls_obj, (sig_group + "_cntr")
                                            )
                                            if hasattr(
                                                msg_cls_obj, (sig_group + "_cntr")
                                            )
                                            else None,
                                            do_crc=getattr(
                                                msg_cls_obj, (sig_group + "_crc")
                                            )
                                            if hasattr(
                                                msg_cls_obj, (sig_group + "_crc")
                                            )
                                            else None,
                                        )

                                pdu_data = msg_dict["pdu_data"]
                                cyclecode = baseCycle_to_cyclecode(
                                    BaseCycle, CycleRepetition
                                )
                                self.update(
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

                            # fr_obj = getattr(self.ipdu_instance, msg_name)
                            # self.ipdu_instance.put_shm(fr_obj, msg_dict, 2)  # main 进程更新

                    # else:
                    #     # RX ---- fdir == 0      TX ----  fdir == 1
                    #     logger.info("fdir is {}".format(fdir))
                    #     logger.error("Fdir 不符合预期")
                    break
                else:
                    BaseCycle = None
                    CycleRepetition = None
                    msg_id = None

        # data_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(data)
        # # logger.debug("FlexrayMsg.Data = {}".format(data_print))
        # trace_log = (
        #     "[{}] {}  {}  FlexrayMsg: id[{}] [{}  {}/{}] [cycele:{}]  [{}]  {}".format(
        #         time_stamp,
        #         self.bus_name,
        #         fdir,
        #         msg_id,
        #         slot_id,
        #         BaseCycle,
        #         CycleRepetition,
        #         cycle,
        #         length,
        #         data_print,
        #     )
        # )
        # # logger.info(trace_log)

        # if (self.f is not None) and (not self.f.closed):
        #     self.f.write(trace_log)
        #     self.f.write("\n")

    def pre_tx_flexray(self, obj, AFlexRay):
        # 调用 update 函数后，才会回调此函数
        slot_id = AFlexRay.contents.FSlotId
        length = AFlexRay.contents.FActualPayloadLength
        cycle = AFlexRay.contents.FCycleNumber
        # data = list(AFlexRay.contents.FData[:length])
        for msg_name, msg_dict in self.pdu_dict.items():
            # msg_cls_obj = getattr(self.bus_cls_obj, msg_name)   # 频繁会卡住
            if msg_dict.get("msg_slotid") == slot_id:
                BaseCycle = msg_dict.get("msg_base_cycle")
                CycleRepetition = msg_dict.get("msg_repetition")
                remainder = cycle % CycleRepetition
                if remainder == BaseCycle:
                    msg_id = msg_dict.get("msg_id")

                    # msg_cls_obj = getattr(self.bus_cls_obj, msg_name)
                    # crc_sig_groups = msg_cls_obj.sig_group_dataid_dict

                    # if crc_sig_groups:  # 判断是否需要 e2e, 这里做e2e, linux 负载高耗时会增加 ，会有问题， 导致接口丢帧
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

                    pdu_data = msg_dict["pdu_data"]
                    if length:
                        for index in range(length):
                            try:
                                AFlexRay.contents.FData[index] = pdu_data[index]
                            except IndexError:
                                AFlexRay.contents.FData[index] = 0
                    if msg_dict.get("tx_change") == True:
                        msg_dict["tx_change"] = False

                    # fr_obj = getattr(self.ipdu_instance, msg_name)
                    # self.ipdu_instance.put_shm(fr_obj, msg_dict, 2)  # main 进程更新

    def get_data_pre_send(self, slot_id, cycle):
        for msg_name, msg_dict in self.pdu_dict.items():
            if msg_dict.get("tx_flag"):
                if msg_dict.get("msg_slotid") == slot_id:
                    BaseCycle = msg_dict.get("msg_base_cycle")
                    CycleRepetition = msg_dict.get("msg_repetition")
                    remainder = cycle % CycleRepetition
                    if remainder == BaseCycle:  # 找到对应报文
                        msg_cls_obj = getattr(self.bus_cls_obj, msg_name)
                        crc_sig_groups = msg_cls_obj.sig_group_dataid_dict
                        # cycle_time = msg_cls_obj.msg_cycle
                        if crc_sig_groups:  # 判断是否需要 e2e
                            if not self.pause_flag:
                                for sig_group in crc_sig_groups:
                                    self.ipdu_instance.set_crc_count(
                                        msg_cls_obj,
                                        sig_group,
                                        do_cntr=getattr(
                                            msg_cls_obj, (sig_group + "_cntr")
                                        )
                                        if hasattr(msg_cls_obj, (sig_group + "_cntr"))
                                        else None,
                                        do_crc=getattr(
                                            msg_cls_obj, (sig_group + "_crc")
                                        )
                                        if hasattr(msg_cls_obj, (sig_group + "_crc"))
                                        else None,
                                    )
                                dlc = msg_dict.get("msg_length")
                                data = msg_dict.get("pdu_data")
                                return dlc, data

    def get_send_flexraytrigger_lists(self, mock_msg_id_list):
        send_trigger_lists = []

        # set冷启动报文config  默认放list第一个
        for msg_id in mock_msg_id_list:
            if msg_id in (131076, 196612, 262148):
                slot_id, BaseCycle, CycleRepetition = msgid_to_slotid(msg_id)
                cyclecode = baseCycle_to_cyclecode(BaseCycle, CycleRepetition)
                flexraytrigger_cfg = (slot_id, cyclecode, 0x33)
                send_trigger_lists.append(flexraytrigger_cfg)

        # set 普通报文config
        for msg_id in mock_msg_id_list:
            if msg_id not in (131076, 196612, 262148):
                slot_id, BaseCycle, CycleRepetition = msgid_to_slotid(msg_id)
                cyclecode = baseCycle_to_cyclecode(BaseCycle, CycleRepetition)
                flexraytrigger_cfg = (slot_id, cyclecode, 0x03)
                send_trigger_lists.append(flexraytrigger_cfg)

        return send_trigger_lists

    def run(self):
        """
        Start tasks to transmit each cyclic message read from json file
        :return:
        """
        try:
            # create a socket object
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # cmd = "/root/quansun_clear/ecu-simulator/xat_ecu/legacy/sdk/driver/tosun/libTSCANAPI/linux/IniMap"
            cmd = "../../venv/lib/python3.8/site-packages/xat_ecu/legacy/sdk/driver/tosun/libTSCANAPI/linux/IniMap"
            self.p = Popen(cmd, shell=True, close_fds=True, preexec_fn=os.setsid)  
            # self.p = Popen([cmd], stdout=subprocess.PIPE)
            logger.info("===============  FR start success =============")
            # sleep(2)

            # connection to host on the port.
            self.client_socket.bind((self.host, self.port))

            self.rx_update_ipdu()

            sleep(1)

        except (AttributeError, OSError) as err:
            error_foo = err  # For debugging.
            logger.error("Tosun Flexray run error: {}".format(self.bus_name))
            logger.error(err)
    
        

    def stop_IniMap(self):
        if self.p:
            self.pid = self.p.pid
            try:
                self.p.terminate()
                self.p.wait()
                os.killpg(self.pid, signal.SIGKILL)
                os.remove("./config1.ini")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/tosun/tosun_flexray.py")
                logger.warning("Stop SOA Tosun IniMap Error : {}".format(e))
        else:
            logger.warning("IniMap 没有启动，不需要去关闭")

    def rx_update(self, Msg):
        # update self.pdu_dict
        # 使用同星回调
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
        for msg_name, msg_dict in self.pdu_dict.items():
            # msg_cls_obj = getattr(self.bus_cls_obj, msg_name)   # 频繁会卡住
            if msg_dict.get("msg_slotid") == slot_id:
                BaseCycle = msg_dict.get("msg_base_cycle")
                CycleRepetition = msg_dict.get("msg_repetition")
                remainder = cycle % CycleRepetition
                if remainder == BaseCycle:
                    msg_id = msg_dict.get("msg_id")

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
                    #         self.bus_name,
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
                        # msg_cls_obj = getattr(self.bus_cls_obj, msg_name)
                        # crc_sig_groups = msg_cls_obj.sig_group_dataid_dict
                        if not self.pause_flag:
                            # if crc_sig_groups or msg_dict.get("tx_change"):
                            if msg_dict.get("tx_change"):
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
                                
                                pdu_data = msg_dict["pdu_data"]

                                cyclecode = baseCycle_to_cyclecode(
                                    BaseCycle, CycleRepetition
                                )
                                self.send(
                                    slot_id=slot_id,
                                    cyclecode=cyclecode,
                                    data=pdu_data,
                                    dlc=length,
                                )

                                if msg_dict.get("tx_change") is True:
                                    msg_dict["tx_change"] = False
                    elif fdir == 0:
                        fdir = "RX"
                        if msg_dict["rx_flag"] is not None:
                            msg_dict["pdu_data"] = data
                            msg_dict["time_stamp"] = time_stamp
                            msg_dict["rx_flag"] = True

                            # fr_obj = getattr(self.ipdu_instance, msg_name)
                            # self.ipdu_instance.put_shm(fr_obj, msg_dict, 2)  # main 进程更新

                    # else:
                    #     # RX ---- fdir == 0      TX ----  fdir == 1
                    #     logger.info("fdir is {}".format(fdir))
                    #     logger.error("Fdir 不符合预期")
                    break
                else:
                    BaseCycle = None
                    CycleRepetition = None
                    msg_id = None


    def rx_update_ipdu(self):
        while self.rx_exit_flag is False:
            Msg = self.recv_new()
            self.rx_update(Msg)
            # logger.info(Msg)
            # sleep(0.0005)
        sleep(0.2)

        # while self.rx_exit_flag.value == 0:
        #     AFlexRay = self.recv_new()

        #     # # time1 = time.time()
        #     # for msg_name, msg_info in self.pdu_dict.items():
        #     #     fr_obj = getattr(self.ipdu_instance, msg_name)
        #     #     self.ipdu_instance.fetch_shm(fr_obj, msg_info, 1)  #  1  fr_pre 需要更新

        #     # # time2 = time.time()
        #     # # time3 = time2 - time1
        #     # # logger.info(f"=============={time3}====================")

        #     sleep(0.0005)
        # sleep(0.1)

    def rx_update_ipdu_start(self):
        thread = threading.Thread(
            target=self.rx_update_ipdu, name="Tosun Flexray rx_update_ipdu"
        )
        thread.start()

    def rx_update_stop(self):
        # self.rx_exit_flag.value += 1

        self.rx_exit_flag = True

    # --------------------   tosun high level api -----------------------------------
    def recv_new(self):
        # 读取fr数据
        # Receive no more than 1024 bytes
        msg, addr = self.client_socket.recvfrom(1024)
        if(len(msg) >= 302):
            Msg_HW = cast(msg, PLIBFlexrayHW).contents
            Msg = Msg_HW.AMsg
        # print(Msg)
        # elif(len(msg) == 88):
        #     Msg = cast(msg, PLIBCANFDHW).contents
        #     print(Msg)
        # Msg = cast(msg, PFlexray).contents
        # logger.info(Msg)

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
        #             print(f"{cycle} - {self.cyc} = {cccyc} ")
        #             # logger.error(
        #             #     f"  -------------   {AFlexRay.contents.FCycleNumber}"
        #             # )
        #             self.cyc = cycle

            # print(Msg.FCycleNumber)
        # print(Msg)

        # Msg.FData[0] = 0xf1
        return Msg

    def recv(self, buffer_num=1000):
        # 读取fr数据
        fr_buffer = (TLIBFlexray * buffer_num)()
        ADataBufferSize = c_int(buffer_num)
        msgs = []
        tsfifo_receive_flexray_msgs(
            self.ADeviceHandle,
            fr_buffer,
            ADataBufferSize,
            self.AChnIdx,
            self.ARxTx,
        )
        # self.fr_recv()
        BufferSize = ADataBufferSize.value
        # logger.info(BufferSize)
        for i in range(BufferSize):
            time_stamp = fr_buffer[i].FTimeUs
            fdir = fr_buffer[i].FDir
            # flag = fr_buffer[i].FFrameFlags
            slot_id = fr_buffer[i].FSlotId
            length = fr_buffer[i].FActualPayloadLength
            # crc = fr_buffer[i].FFrameCRC
            cycle = fr_buffer[i].FCycleNumber
            data = list(fr_buffer[i].FData[:length])

            BaseCycle = None
            CycleRepetition = None
            msg_id = None
            for msg_name, msg_dict in self.pdu_dict.items():
                # msg_cls_obj = getattr(self.bus_cls_obj, msg_name)   # 频繁会卡住
                if msg_dict.get("msg_slotid") == slot_id:
                    BaseCycle = msg_dict.get("msg_base_cycle")
                    CycleRepetition = msg_dict.get("msg_repetition")
                    remainder = cycle % CycleRepetition
                    if remainder == BaseCycle:
                        msg_id = msg_dict.get("msg_id")
                        break
                    else:
                        BaseCycle = None
                        CycleRepetition = None
                        msg_id = None

            if fdir == 1:
                fdir = "TX"
            elif fdir == 0:
                fdir = "RX"
            else:
                logger.error("Fdir 不符合预期")

            fr_msg = (
                msg_id,
                time_stamp,
                length,
                data,
                fdir,
                slot_id,
                BaseCycle,
                CycleRepetition,
            )
            msgs.append(fr_msg)

            # data_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(data)
            # # logger.debug("FlexrayMsg[{}].Data = {}".format(i, data_print))
            # trace_log = "[{}] {}  {}  FlexrayMsg: id[{}] [{}  {}/{}] [cycele:{}]  [{}]  {}".format(
            #     time_stamp,
            #     self.bus_name,
            #     fdir,
            #     msg_id,
            #     slot_id,
            #     BaseCycle,
            #     CycleRepetition,
            #     cycle,
            #     length,
            #     data_print,
            # )
            # # logger.info(trace_log)

            # if (self.f is not None) and (not self.f.closed):
            #     self.f.write(trace_log)
            #     self.f.write("\n")
        return msgs

    def send(
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
        fr_tx_frame_HW.FHWIdx = 0
        fr_tx_frame_HW.AMsg = fr_tx_frame

        self.client_socket.sendto(fr_tx_frame_HW, ("127.0.0.1",8000))
        # sleep(0.001)
        # self.client_socket.sendto(fr_tx_frame,("127.0.0.1",8000))
        # sleep(0.001)
        # self.client_socket.sendto(fr_tx_frame,("127.0.0.1",8000))


    def stop(self):
        """
        Stop each task that is sending cyclic messages.
        :return:
        """
        try:
            # self.rx_exit_ flag.value += 1

            self.rx_exit_flag = True
            self.exit_flag = True
            sleep(0.1)
            self.client_socket.close()
            self.stop_IniMap()

            # for msg_name in self.pdu_dict:
            #     fr_obj = getattr(self.ipdu_instance, msg_name)
            #     fr_obj.close()

            # logger.info("开始释放内存")
            # self.ipdu_instance.smm.shutdown()
            # logger.info("释放内存完毕")
            # # self.shm_fr.close()
            # # self.shm_fr.unlink()

        except AttributeError:
            logger.error('Tosun Flexray stop error: {}'.format(self.bus_name))

    def update(
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

        tsapp_transmit_flexray_async(self.ADeviceHandle, fr_tx_frame)
   


if __name__ == '__main__':
    # Work Path: ecu_simulator/sdk/driver/tosun/jidutest_flexray/flexray/libTOSUN/linux
    # cmd : python3 ../../../../tosun_flexray.py
    # [1,2,11,12,22,33,33,33,33,44,55,66,67,77,78,79,1,2,11,12,22,33,33,33,33,44,55,66,67,1,1]
    fr_test = TosunFlexray("1", [0])

    fr_test.start()

    sleep(2)
    fr_test.send(
        131076,
        32,
        [
            4,
            2,
            11,
            12,
            22,
            33,
            33,
            33,
            33,
            44,
            55,
            66,
            67,
            77,
            78,
            79,
            1,
            2,
            11,
            12,
            22,
            33,
            33,
            33,
            33,
            44,
            55,
            66,
            67,
            1,
            1,
        ],
    )
    sleep(2)
    fr_test.fr_bus.update(
        slot_id=51,
        cyclecode=5,
        data=[
            0,
            2,
            11,
            12,
            22,
            33,
            33,
            33,
            33,
            44,
            55,
            66,
            67,
            77,
            78,
            79,
            1,
            2,
            11,
            12,
            22,
            33,
            33,
            33,
            33,
            44,
            55,
            66,
            67,
            1,
            1,
        ],
    )
    sleep(5)

    # fr_print = Printer()
    # fr_notifier = Notifier(fr_test.fr_bus, fr_print)

    # fr_test.fr_bus.update(slot_id=2, cyclecode=4, data=[1,2,11,12,22,33,33,33,33,44,55,66,67,77,78,79,1,2,11,12,22,33,33,33,33,44,55,66,67,1,1])

    # sleep(10)

    fr_test.stop()
