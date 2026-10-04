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
from multiprocessing import Process
from typing import List, Tuple, Optional

global is_connected
is_connected = None
global DeviceHandle
DeviceHandle = c_size_t(0)
DLC_DATA_BYTE_CNT = (0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 16, 20, 24, 32, 48, 64)


class TosunCan(threading.Thread):
    """
    Provide interfaces:
      1. send single message
      2. read single message
    """

    from xat_ecu.legacy.sdk.driver.tosun.libTSCANAPI.TSStructure import (
        TLibFlexray_controller_config,
        TLibTrigger_def,
        TLIBFlexray,
        TLIBCAN,
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
        nbrateconfig=500,
        dbrateconfig=2000,
        ipdu=None,
        is_fd=False,
        dbc_json=None,
        **kwargs
    ):
        """
        Initialize a SocketCan object.
        :param bus_name: bus name, such as 'bodycan', 'ept'
        :param channel: channel interface, such as (1409286394, 0)
        :param brateconfig: brateconfig of socket can, default is CANConfig_CONSTANT.UTA05XX.bt_500k
        :param dbc_json: dbc_json file which defined cyclic message
        """
        threading.Thread.__init__(self, name=bus_name, daemon=True)

        self.bus_name = bus_name  # name of channel, such as 'etp'
        self.channel = channel
        self.dbc_json = dbc_json

        self.nbrateconfig = nbrateconfig
        self.dbrateconfig = dbrateconfig
        self.is_fd = is_fd
        self.callback = kwargs.get('callback')
        self.exit_flag = False  # True means stop sending cyclic messages tasks
        self.msg_task = {}  # Tasks to sending cyclic messages
        self.timestamp = None
        self.dlc = None
        if self.dbc_json is None:
            self.msgs = []
        else:
            with open(self.dbc_json) as data:
                self.msgs = json.load(data)

        # New
        if ipdu:
            self.pdu_dict = ipdu.bus_pdu_dict[self.bus_name]
            self.bus_cls_obj = getattr(ipdu, self.bus_name)
            self.ipdu_instance = ipdu
        else:
            logger.error("没有传入 ipdu 实例 参数")
        self.pause_flag = False
        self.rx_exit_flag = False

        # DeviceHandle = TosunCan.size_t(0)
        if isinstance(self.channel[0], str):
            self.ADeviceSerial = bytes(self.channel[0], encoding="utf-8")
        else:
            self.ADeviceSerial = None
            logger.warning("没有给出同星的设备号, 后续当只有一个同星设备处理")
        # self.AChnIdx = c_int(self.channel[1])
        self.AChnIdx = self.channel[1]
        self.record_time = None

    def initialize(self, AEnableFIFO=True, AEnableTurbe=True, hardtime=False):
        # hardtime ---  True  usb接入时间开始      False  每次connect时间开始
        TosunCan.initialize_lib_tscan(AEnableFIFO, AEnableTurbe, hardtime)

    def scan_device(self):  # 获取 ADeviceSerial
        ADeviceScan = TosunCan.s32(0)
        TosunCan.tscan_scan_devices(ADeviceScan)
        return ADeviceScan.value

    def get_device_info(self, DeviceCount: int = 0):
        AFManufacturer = c_char_p()
        AFProduct = c_char_p()
        AFSerial = c_char_p()
        TosunCan.tscan_get_device_info(
            DeviceCount, AFManufacturer, AFProduct, AFSerial
        )  # 获取设备信息(选择要连接的设备   0)

        return (
            AFManufacturer.value,
            AFProduct.value,
            AFSerial.value,
        )

    def connect(self, ADeviceSerial=b''):  # open 设备 （根据 句柄）
        global DeviceHandle
        if self.ADeviceSerial:
            TosunCan.tsapp_connect(self.ADeviceSerial, DeviceHandle)
        else:
            TosunCan.tsapp_connect(ADeviceSerial, DeviceHandle)

    def disconnect(self):  # close 设备
        TosunCan.tsapp_disconnect_by_handle(DeviceHandle)

    def config_can(self):
        TosunCan.tsapp_configure_baudrate_canfd(
            DeviceHandle,
            self.AChnIdx,
            self.nbrateconfig,
            self.dbrateconfig,
            TosunCan.TLIBCANFDControllerType.lfdtISOCAN,
            TosunCan.TLIBCANFDControllerMode.lfdmNormal,
            True,
        )

    def start_logging(self, filepath="", exe_type=1):
        # 开始保存该同行设备的日志  asc 格式
        if filepath:
            filepath_byte = bytes(filepath, encoding="utf-8")
            TosunCan.tsapp_start_logging(DeviceHandle, filepath_byte, exe_type)
            logger.info(f"开始记录日志 {filepath}")
        else:
            filepath_default = "/root/TosunCan_" + get_time_str_now() + ".asc"
            filepath_default_byte = bytes(filepath_default, encoding="utf-8")
            TosunCan.tsapp_start_logging(DeviceHandle, filepath_default_byte, exe_type)
            logger.info(f"开始记录日志 {filepath_default}")

    def stop_logging(self, exe_type=1):
        # exe_type   要和start_logging  里面的一致
        TosunCan.tsapp_stop_logging(exe_type)
        logger.info(f"停止记录 TosunCan 日志")

    # def stop_flexray(self, ATimeoutMs=1000):  # can lin 没有此接口
    #     tsflexray_stop_net(DeviceHandle, self.AChnIdx, c_int(ATimeoutMs))

    # def start_flexray(self, ATimeoutMs=1000):  # can lin 没有此接口
    #     tsflexray_start_net(DeviceHandle, self.AChnIdx, c_int(ATimeoutMs))

    def flush_rx_buffer(self):
        TosunCan.tsfifo_clear_flexray_receive_buffers(DeviceHandle, self.AChnIdx)

    def run(self):
        try:
            # self.initialize()  # 函数初始化

            # self.current_device = self.scan_device()  # 可以反复调用
            # logger.info("FR current_device is {}".format(self.current_device))
            # self.manufacturer, self.product, self.serial = self.get_device_info()
            # logger.info(
            #     "FR 设备信息： manufacturer is {}, product is {}, serial is {}".format(
            #         self.manufacturer, self.product, self.serial
            #     )
            # )
            global is_connected

            if is_connected:
                logger.info("Tosun can 已经连接")
            else:
                self.initialize()  # 函数初始化
                self.connect()
                is_connected = True
                logger.info("Tosun can 连接成功")
                # self.start_logging()

            self.config_can()


            for message in self.pdu_dict:
                msg_obj = self.pdu_dict[message]
                if msg_obj.get("tx_flag") is not None:
                    if isinstance(message, str):
                        msg_cls_obj = getattr(self.bus_cls_obj, message)
                        crc_sig_groups = msg_cls_obj.sig_group_dataid_dict
                        msg_id = msg_cls_obj.msg_id

                        # lock = threading.Lock()
                        lock = None  # 没有用

                        cycle_msg_thread_obj = self.tx_cycle_start(
                            message, msg_obj, msg_cls_obj, crc_sig_groups, lock
                        )

                        self.msg_task[msg_id] = cycle_msg_thread_obj
                    else:
                        # add_msg  在 self.bus_cls_obj 上不存在的
                        msg_cls_obj = None
                        crc_sig_groups = None
                        msg_id = message

                        # lock = threading.Lock()
                        lock = None  # 没有用

                        cycle_msg_thread_obj = self.tx_cycle_start(
                            message, msg_obj, msg_cls_obj, crc_sig_groups, lock
                        )

                        self.msg_task[msg_id] = cycle_msg_thread_obj

            self.rx_update_ipdu()

        except (AttributeError, OSError) as err:
            error_foo = err  # For debugging.
            logger.error("Tosun Can run error: {}".format(self.bus_name))
            logger.error(err)

    def tx_cycle(self, msg_obj, msg_cls_obj, crc_sig_groups, lock):
        msg_id = msg_obj["msg_id"]

        while self.exit_flag is False:
            # if msg_id == 0x150:
            #     time1 = time.time()

            if not self.pause_flag:
                tx_flag = msg_obj["tx_flag"]
                if tx_flag == True:
                    if crc_sig_groups:  # crc sig group (dataid)
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
                    data = msg_obj["pdu_data"]
                    msg_id = msg_obj["msg_id"]
                    length = msg_obj["msg_length"]
                    cycle_time = msg_obj["msg_cycle"]

                    FFDProperties = 3 if self.is_fd else 0
                    msg = TosunCan.TLIBCANFD(
                        FIdxChn=self.AChnIdx,
                        FDLC=len(data),
                        FIdentifier=msg_id,
                        FProperties=1,
                        FFDProperties=FFDProperties,
                        FData=data,
                    )

                    # lock.acquire()
                    self.send(msg)

                    # if msg_id == 0x150:
                    #     time2 = time.time()
                    #     time3 = time2 - time1
                    #     if time3 >= 0.001:
                    #         logger.info(f"========= {time3} =========")

                    # if msg_id == 0x166:
                    #     logger.info(msg_id)

                    if self.callback:
                        try:
                            self.callback(device_type='tosun_can', msg=msg, msg_id=msg_id, DLC_DATA_BYTE_CNT=DLC_DATA_BYTE_CNT)
                        except Exception as e:
                            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/tosun/tosun_can.py")
                            logger.debug(f'err {str(e)}')
                    if cycle_time: 
                        sleep(cycle_time)
                    else:
                        msg_obj["tx_flag"] = False

                elif tx_flag == False:
                    pre_send = msg_obj.get("pre_send")
                    if pre_send:
                        # 为了立即发送，进行预热
                        sleep(0.001)
                    else:
                        # 非周期msg，挂住
                        sleep(2)

                elif tx_flag == None:
                    logger.info(f"CAN Tx {msg_obj['msg_name']} 停止发送")
                    break

    def tx_cycle_start(self, msg_name, msg_obj, msg_cls_obj, crc_sig_groups, lock):
        # logger.info(msg_name)
        thread = threading.Thread(
            target=self.tx_cycle,
            name=msg_name,
            args=(msg_obj, msg_cls_obj, crc_sig_groups, lock),
            daemon=True,
        )
        thread.start()

        return thread

    def rx_update(self, update_ipdu=True):
        # update self.pdu_dict
        msgs, data_buffer_size = self.recv()
        # logger.info(data_buffer_size)
        if data_buffer_size:
            for i in range(data_buffer_size):
                # if msgs[i].FCCType == 0:  # 确保是正常帧, can 没有这个参数
                id = msgs[i].FIdentifier

                # logger.info(id)
                # if id == 0x157:
                #     logger.info(id)
                # if id == 80:
                #     logger.info(id)

                # Tosun 时间戳
                # time_stamp = msgs[i].FTimeUs
                # 上位机时间戳
                time_stamp = time.time()

                length = DLC_DATA_BYTE_CNT[msgs[i].FDLC]
                data = msgs[i].FData[:length]

                if self.callback:
                    try:
                        self.callback(device_type='tosun_can', msg=msgs[i], msg_id=id, DLC_DATA_BYTE_CNT=DLC_DATA_BYTE_CNT, channel=self.channel)
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/tosun/tosun_can.py")
                        print(f'err {str(e)}')
                if update_ipdu:
                    for message in self.pdu_dict:
                        msg_obj = self.pdu_dict[message]
                        if msg_obj["rx_flag"] is not None:
                            if id == msg_obj["msg_id"]:
                                msg_obj["pdu_data"] = data
                                msg_obj["time_stamp"] = time_stamp
                                msg_obj["rx_flag"] = True
            # [(id, time_stamp, length, data)]
        return msgs

    def rx_update_ipdu(self):
        while self.rx_exit_flag is False:
            self.rx_update()
            sleep(0.001)
        sleep(0.1)

        # while self.rx_exit_flag is False:
        #     self.rx_update()
        #     sleep(0.001)
        # sleep(0.1)

    # def rx_update_ipdu_start(self):
    #     thread = threading.Thread(target=self.rx_update_ipdu, name="SocketCan rx_update_ipdu", daemon=True,)
    #     thread.start()

    def rx_update_stop(self):
        self.exit_flag = True
        self.rx_exit_flag = True
        sleep(2)

    # --------------------   tosun high level api -----------------------------------
    def recv(self, buffer_num=100):
        # 读取fr数据
        can_buffer = (TosunCan.TLIBCANFD * buffer_num)()
        ADataBufferSize = TosunCan.s32(buffer_num)

        TosunCan.tsfifo_receive_canfd_msgs(
            DeviceHandle,
            can_buffer,
            ADataBufferSize,
            self.AChnIdx,
            TosunCan.READ_TX_RX_DEF.ONLY_RX_MESSAGES,
        )
        return can_buffer, ADataBufferSize.value

    def send(self, ACAN):
        # time1 = time.perf_counter()

        TosunCan.tsapp_transmit_canfd_async(DeviceHandle, ACAN)

        # time2 = time.perf_counter() - time1
        # if time2 > 0.001:
        #     logger.info(f"-------------------------{time2}------------------")

    def stop(self):
        """
        Stop each task that is sending cyclic messages.
        :return:
        """
        global is_connected
        try:
            self.rx_exit_flag = True
            self.exit_flag = True
            sleep(0.01)
            if is_connected:
                # self.stop_logging()
                is_connected = False

            # # self.disconnect()  #  关掉设备
            # # tsapp_disconnect_all()    #  关掉所有tosun设备
            logger.info("{} is stopped".format(self.bus_name))

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
        # if slot_id == 20 and cyclecode == 1:
        #     data_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(data)
        #     logger.info(data_print)

        TosunCan.tsapp_transmit_flexray_async(DeviceHandle, fr_tx_frame)
        # result = transmit_async(DeviceHandle, byref(fr_tx_frame))
        # logger.info(result)

        # transmit_sync(DeviceHandle, byref(fr_tx_frame), 1)
        # result = transmit_sync(DeviceHandle, byref(fr_tx_frame), 1)  # 设置超时 1ms
        # logger.info(result)  # 测试接口不行 延迟太高  有点返回 5


if __name__ == '__main__':
    # Work Path: ecu_simulator/
    # cmd : python3 sdk/driver/tosun/tosun_can.py
    # can_sender = TosunCan()
    pass
