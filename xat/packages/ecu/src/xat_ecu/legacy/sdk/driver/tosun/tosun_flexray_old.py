# -*- coding: utf-8 -*-
"""
@File        : tosun_flexray.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2023-01-16 18:06
@Description : 
@Examples    :
"""

import sys
import os

from xat_ecu.legacy.sdk.driver.tosun.libTSCANAPI import TLIBFlexray

current_path = os.path.dirname(os.path.realpath(__file__))
import json
import time
import inspect
import threading
from xat_ecu.legacy.common.logger import logger
from ctypes import *
import platform
from time import sleep

# from ecu_simulator.sdk.driver.tosun.libTSCANAPI import *
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


def on_rx_tx_flexray(AFlexRay):
    # pass
    string = ''
    for index in range(AFlexRay.contents.FActualPayloadLength):
        string += hex(AFlexRay.contents.FData[index]) + ' '
    print(
        AFlexRay.contents.FTimeUs,
        ' ',
        AFlexRay.contents.FSlotId,
        ' ',
        AFlexRay.contents.FCycleNumber,
        ' ',
        ('tx' if AFlexRay.contents.FDir else 'rx'),
        "  ",
        string,
    )


def pre_tx_flexray(AFlexRay):
    print("tx_info")
    AFlexRay.contents.FData[0] = 0xFF


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

    from xat_ecu.legacy.sdk.driver.tosun.libTSCANAPI.TSStructure import (
        TLibFlexray_controller_config,
        TLibTrigger_def,
        TLIBFlexray,
        TLIBCANFD,
        OnTx_RxFUNC_Flexray_WHandle,
    )
    from xat_ecu.legacy.sdk.driver.tosun.libTSCANAPI.TSEnumdefine import (
        READ_TX_RX_DEF,
        TLIBCANFDControllerType,
        TLIBCANFDControllerMode,
    )
    from xat_ecu.legacy.sdk.driver.tosun.libTSCANAPI.TSCAN import (
        initialize_lib_tscan,
        tsapp_connect,
        size_t,
        s32,
        finalize_lib_tscan,
        tscan_scan_devices,
        tscan_get_device_info,
        tsapp_disconnect_by_handle,
        tsflexray_stop_net,
        tsflexray_start_net,
        tsfifo_clear_flexray_receive_buffers,
        tsapp_start_logging,
        tsapp_stop_logging,
        tsflexray_set_controller_frametrigger,
        tsapp_register_pretx_event_flexray_whandle,
        tsapp_register_event_flexray_whandle,
        tsfifo_receive_flexray_msgs,
        tsfifo_receive_canfd_msgs,
        tsapp_transmit_flexray_async,
        tsapp_transmit_canfd_async,
        tsapp_configure_baudrate_canfd,
    )

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
        self.ADeviceHandle = TosunFlexray.size_t(0)

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

    def initialize(self, AEnableFIFO=True, AEnableTurbe=True, hardtime=False):
        # hardtime ---  True  usb接入时间开始      False  每次connect时间开始
        TosunFlexray.initialize_lib_tscan(AEnableFIFO, AEnableTurbe, hardtime)

    def scan_device(self):  # 获取 ADeviceSerial
        ADeviceScan = TosunFlexray.s32(0)
        TosunFlexray.tscan_scan_devices(ADeviceScan)
        return ADeviceScan.value

    def get_device_info(self, DeviceCount: int = 0):
        AFManufacturer = c_char_p()
        AFProduct = c_char_p()
        AFSerial = c_char_p()
        TosunFlexray.tscan_get_device_info(
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
            TosunFlexray.tsapp_connect(self.ADeviceSerial, self.ADeviceHandle)
        else:
            TosunFlexray.tsapp_connect(ADeviceSerial, self.ADeviceHandle)

    def disconnect(self):  # close 设备
        TosunFlexray.tsapp_disconnect_by_handle(self.ADeviceHandle)

    def stop_flexray(self, ATimeoutMs=1000):  # 停止 FR
        TosunFlexray.tsflexray_stop_net(
            self.ADeviceHandle, self.AChnIdx, c_int(ATimeoutMs)
        )

    def start_flexray(self, ATimeoutMs=1000):  # 启动 FR
        TosunFlexray.tsflexray_start_net(
            self.ADeviceHandle, self.AChnIdx, c_int(ATimeoutMs)
        )

    def flush_rx_buffer(self):
        TosunFlexray.tsfifo_clear_flexray_receive_buffers(
            self.ADeviceHandle, self.AChnIdx
        )

    def start_logging(self, filepath="", exe_type=0):
        # 开始保存该同行设备的日志  asc 格式
        if filepath:
            filepath_byte = bytes(filepath, encoding="utf-8")
            TosunFlexray.tsapp_start_logging(
                self.ADeviceHandle, filepath_byte, exe_type
            )
            logger.info(f"开始记录日志 {filepath}")
        else:
            filepath_default = "/root/TosunFlexray_" + get_time_str_now() + ".asc"
            filepath_default_byte = bytes(filepath_default, encoding="utf-8")
            TosunFlexray.tsapp_start_logging(
                self.ADeviceHandle, filepath_default_byte, exe_type
            )
            logger.info(f"开始记录日志 {filepath_default}")

    def stop_logging(self, exe_type=0):
        # exe_type   要和start_logging  里面的一致
        TosunFlexray.tsapp_stop_logging(exe_type)
        logger.info(f"停止记录 TosunFlexray 日志")

    def fr_filter(self, slot_id, base_cycle, rep_cycle):
        # 接口，未验证
        TosunFlexray.tsfifo_add_flexray_pass_filter(
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

        self.fr_config = TosunFlexray.TLibFlexray_controller_config(
            is_open_a=is_open_a,
            is_open_b=is_open_b,
            wakeup_chn=wakeup_chn,
            enable100_a=enable100_a,
            enable100_b=enable100_b,
            is_show_nullframe=is_show_nullframe,
            is_Bridging=is_Bridging,
        )

        i = 0
        self.fr_trigger = (TosunFlexray.TLibTrigger_def * len(trigger_lists))()
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

        TosunFlexray.tsflexray_set_controller_frametrigger(
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

    # def start(self):
    #     """
    #     代替run
    #     Start tasks to transmit each cyclic message read from json file
    #     :return:
    #     """
    #     try:
    #         tracelog_path = "/root/" + self.bus_name + ".txt"
    #         with open(tracelog_path, "w") as self.f:
    #             logger.info(
    #                 "{} FlexrayBus Tracelog path is {}".format(
    #                     self.bus_name, tracelog_path
    #                 )
    #             )
    #             self.start_flexray()
    #             sleep(20)
    #             # self.flush_rx_buffer()
    #     except (AttributeError, OSError) as err:
    #         error_foo = err  # For debugging.
    #         logger.error("Tosun Flexray run error: {}".format(self.bus_name))
    #         logger.error(err)

    def run(self):
        """
        Start tasks to transmit each cyclic message read from json file
        :return:
        """
        try:
            on_flexray = TosunFlexray.OnTx_RxFUNC_Flexray_WHandle(self.on_rx_tx_flexray)
            pre_flexray = TosunFlexray.OnTx_RxFUNC_Flexray_WHandle(self.pre_tx_flexray)
            self.initialize()  # 函数初始化

            # self.current_device = self.scan_device()  # 可以反复调用
            # logger.info("FR current_device is {}".format(self.current_device))
            # self.manufacturer, self.product, self.serial = self.get_device_info()
            # logger.info(
            #     "FR 设备信息： manufacturer is {}, product is {}, serial is {}".format(
            #         self.manufacturer, self.product, self.serial
            #     )
            # )
            # self.interface = self.manufacturer
            # self.fr_buffer = (TLIBFlexray * self.ADataBufferSize_raw)()

            # self.serial = "" # 防止上面的 self.serial 获取有问题， 一个设备 connect ，可以正常下去， 两个及以上会弹 让你选择那个驱动
            # self.connect(self.serial)

            self.connect()

            self.stop_flexray()  # 防止之前没有正常关闭

            # self.start_logging("/root/fleaxray.asc")

            TosunFlexray.tsapp_register_event_flexray_whandle(
                self.ADeviceHandle, on_flexray
            )

            ret = TosunFlexray.tsapp_register_pretx_event_flexray_whandle(
                self.ADeviceHandle, pre_flexray
            )
            # print(ret)

            # 冷启动报文
            # 131076 # VDDM   (2,4,0x33)
            # 196612 # BGM
            # 262148 # CDC
            # self.mock_msg_id_list = None
            if self.mock_msg_id_list is None:
                send_trigger_lists = [
                    (2, 4, 0x33),
                    (51, 5, 0x03),
                ]  # vddm NM trigger 冷启动  固定这个  (2,4,0x33)
                logger.info("没有给fr调度表，使用默认 (2,4,0x33),(51, 5, 0x03)")
            else:
                send_trigger_lists = self.get_send_flexraytrigger_lists(
                    self.mock_msg_id_list
                )
                # send_trigger_lists = send_trigger_lists[:45]   # 测试

                logger.debug(self.mock_msg_id_list)
                logger.debug(send_trigger_lists)
                logger.info(f"mock FR 报文数量： {len(send_trigger_lists)}")
            self.config_by_manual(send_trigger_lists)

            # tracelog_path = "/root/" + self.bus_name + ".txt"
            # with open(tracelog_path, "w") as self.f:
            #     logger.info(
            #         "{} FlexrayBus Tracelog path is {}".format(
            #             self.bus_name, tracelog_path
            #         )
            #     )

            self.start_flexray()

            # # 试用fifo rx
            # self.flush_rx_buffer()
            # self.rx_update_ipdu()

            # sleep(1)
            # self.flush_rx_buffer() 用后获取不到报文了
            while self.exit_flag is False:
                if not self.pause_flag:
                    sleep(1)

            # self.stop_logging()
            self.stop_flexray()
            self.disconnect()  # 关掉设备
            # tsapp_disconnect_all()    #  关掉所有tosun设备

            # for msg_name in self.pdu_dict:
            #     fr_obj = getattr(self.ipdu_instance, msg_name)
            #     fr_obj.close()
            # logger.info("{} is stopped".format(self.bus_name))

            # # 启动 tx cycle
            # for message in self.pdu_dict:
            #     msg_obj = self.pdu_dict[message]
            #     if msg_obj.get("tx_flag"):
            #         msg_cls_obj = getattr(self.bus_cls_obj, message)
            #         crc_sig_groups = msg_cls_obj.sig_group_dataid_dict
            #         cycle_time = msg_cls_obj.msg_cycle
            #         if crc_sig_groups:  # crc sig group (dataid)
            #             self.tx_cycle_start(
            #                 message, msg_obj, msg_cls_obj, crc_sig_groups, cycle_time
            #             )

            # self.rx_update_ipdu_start()
            # self.rx_update_ipdu()

            # # time.sleep(0.1)
            # # self.send(131076, 32, [4,2,11,12,22,33,33,33,33,44,55,66,67,77,78,79,1,2,11,12,22,33,33,33,33,44,55,66,67,1,1])
            # # time.sleep(0.1)
            # # self.send(131076, 32, [6,2,11,12,22,33,33,33,33,44,55,66,67,77,78,79,1,2,11,12,22,33,33,33,33,44,55,66,67,1,1])
            # # self.update(slot_id=51, cyclecode=5, data=[0,2,11,12,22,33,33,33,33,44,55,66,67,77,78,79,1,2,11,12,22,33,33,33,33,44,55,66,67,1,1])

            # logger.info("{} is stopped".format(self.bus_name))

        except (AttributeError, OSError) as err:
            error_foo = err  # For debugging.
            logger.error("Tosun Flexray run error: {}".format(self.bus_name))
            logger.error(err)

    def rx_update(self, update_ipdu=True):
        # update self.pdu_dict
        msgs = self.recv()
        if msgs:
            if update_ipdu:
                for msg in msgs:
                    id = msg[0]
                    time_stamp = msg[1]
                    # length = msg[2]
                    data = msg[3]
                    fdir = msg[4]

                    if fdir == "RX":
                        for message in self.pdu_dict:
                            msg_obj = self.pdu_dict[message]
                            if msg_obj["rx_flag"] is not None:
                                if id == msg_obj["msg_id"]:
                                    msg_obj["pdu_data"] = data
                                    msg_obj["time_stamp"] = time_stamp
                                    msg_obj["rx_flag"] = True
        return msgs

    def rx_update_ipdu(self):
        # tracelog_path = "/root/" + self.bus_name + ".txt"
        # with open(tracelog_path, "w") as self.f:
        #     logger.info(
        #         "{} FlexrayBus Tracelog path is {}".format(self.bus_name, tracelog_path)
        #     )
        #     while self.rx_exit_flag is False:
        #         AFlexRay = self.recv_new()
        #         sleep(0.0005)
        #     sleep(0.1)

        while self.rx_exit_flag is False:
            AFlexRay = self.recv_new()
            # sleep(0.0005)
        sleep(0.1)

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

    def tx_cycle(self, msg_obj, msg_cls_obj, crc_sig_groups, cycle_time):
        while self.exit_flag is False:
            # if crc_sig_groups:  # crc sig group (dataid)

            if not self.pause_flag:
                for sig_group in crc_sig_groups:
                    self.ipdu_instance.set_crc_count(
                        msg_cls_obj,
                        sig_group,
                        do_cntr=getattr(msg_cls_obj, (sig_group + "_cntr"))
                        if hasattr(msg_cls_obj, (sig_group + "_cntr"))
                        else None,
                        do_crc=getattr(msg_cls_obj, (sig_group + "_crc"))
                        if hasattr(msg_cls_obj, (sig_group + "_crc"))
                        else None,
                    )

                self.send(
                    msgid=msg_obj["msg_id"],
                    dlc=msg_obj["msg_length"],
                    data=msg_obj["pdu_data"],
                )

                # if msg_obj["msg_id"] == 1310721:
                #     data_print = (
                #         DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(
                #             msg_obj["pdu_data"]
                #         )
                #     )
                #     # i += 1
                #     logger.info(data_print)
                # # msg_obj["tx_flag"] = False

            sleep(cycle_time)

        # return i
        # start = time.time()
        # end = time.time()
        # logger.info(end - start)
        # logger.info()

    def tx_cycle_start(
            self, msg_name, msg_obj, msg_cls_obj, crc_sig_groups, cycle_time
    ):
        # logger.info(msg_name)
        thread = threading.Thread(
            target=self.tx_cycle,
            name=msg_name,
            args=(msg_obj, msg_cls_obj, crc_sig_groups, cycle_time),
        )
        thread.start()

    # --------------------   tosun high level api -----------------------------------
    def recv_new(self, buffer_num=1000):
        # 读取fr数据
        fr_buffer = (TosunFlexray.TLIBFlexray * buffer_num)()
        ADataBufferSize = c_int(buffer_num)
        msgs = []

        TosunFlexray.tsfifo_receive_flexray_msgs(
            self.ADeviceHandle,
            fr_buffer,
            ADataBufferSize,
            self.AChnIdx,
            self.ARxTx,
        )

        BufferSize = ADataBufferSize.value

        # time1 = time.time()
        # logger.info(f"----------------------{BufferSize}------------------------------")
        for i in range(BufferSize):
            if fr_buffer[i].FCCType == 0:  # 确保是正常帧
                self.on_rx_tx_flexray(None, fr_buffer[i])
        # time2 = time.time() - time1
        # logger.info(
        #     f"============================={time2}================================="
        # )

    def recv(self, buffer_num=1000):
        # 读取fr数据
        fr_buffer = (TosunFlexray.TLIBFlexray * buffer_num)()
        ADataBufferSize = c_int(buffer_num)
        msgs = []
        TosunFlexray.tsfifo_receive_flexray_msgs(
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

    def send(self, msgid: int, dlc: int, data: list):
        slot_id, BaseCycle, CycleRepetition = msgid_to_slotid(msgid)
        cyclecode = baseCycle_to_cyclecode(BaseCycle, CycleRepetition)
        self.update(slot_id=slot_id, cyclecode=cyclecode, data=data, dlc=dlc)

    # def stop(self):
    #     """
    #     Stop each task that is sending cyclic messages.
    #     :return:
    #     """
    #     try:
    #         self.rx_exit_flag = True
    #         self.exit_flag = True
    #         sleep(1)
    #         self.stop_flexray()
    #         # self.disconnect()
    #         tsapp_disconnect_all()
    #         sleep(1)
    #     except AttributeError:
    #         logger.error('Tosun Flexray stop error: {}'.format(self.bus_name))

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
        fr_tx_frame = TosunFlexray.TLIBFlexray()
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
        # if slot_id == 20 and cyclecode == 1:
        #     data_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(data)
        #     logger.info(data_print)

        TosunFlexray.tsapp_transmit_flexray_async(self.ADeviceHandle, fr_tx_frame)
        # result = transmit_async(self.ADeviceHandle, byref(fr_tx_frame))
        # logger.info(result)

        # transmit_sync(self.ADeviceHandle, byref(fr_tx_frame), 1)
        # result = transmit_sync(self.ADeviceHandle, byref(fr_tx_frame), 1)  # 设置超时 1ms
        # logger.info(result)  # 测试接口不行 延迟太高  有点返回 5


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
