# -*- coding: utf-8 -*-
"""
@File        : toomoss_can.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022-12-02 09:06
@Description : 
@Examples    :
"""

import sys
import os

import json
import time
import inspect
import threading
from xat_ecu.legacy.common.logger import logger
from ctypes import *
import platform
from time import sleep
from xat_ecu.legacy.sdk.driver.toomoss.sdk.api.python_sat.usb_device import *
from xat_ecu.legacy.sdk.driver.toomoss.toomoss_constant import *
from xat_ecu.legacy.sdk.driver.toomoss.sdk.api.python_sat.usb2can import *
from xat_ecu.legacy.sdk.driver.toomoss.sdk.api.python_sat.usb2canfd import *
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding


class ToomossCan(threading.Thread):
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
        brateconfig=CANConfig_CONSTANT.UTA05XX.bt_500k,
        canconfig=[0, 0, 1, 0, 1],
        nbrateconfig=CANConfig_CONSTANT.UTA05XX.nbt_500k,
        dbrateconfig=CANConfig_CONSTANT.UTA05XX.dbt_2m,
        canfdconfig=[0, 1, 1, 1],
        canfilter=[1, 0, 0, 0, 0, 0, 0],
        ipdu=None,
        is_fd=False,
        dbc_json=None,
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
        self.devhandle = channel[0]
        self.canindex = channel[1]
        self.canfilter = canfilter

        self.canconfig = canconfig
        self.brateconfig = brateconfig

        self.canfdconfig = canfdconfig
        self.nbrateconfig = nbrateconfig
        self.dbrateconfig = dbrateconfig

        self.dbc_json = dbc_json
        self.is_fd = is_fd

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
        self.f = None

        # start toomoss
        self.start_toomoss()

    def run(self):
        """
        Start tasks to transmit each cyclic message read from json file
        :return:
        """
        try:
            # if self.msgs:
            #     for idx, msg in enumerate(self.msgs):
            #         msg_foo = msg                       # For debugging.
            #         msg_task_foo = self.msg_task        # For debugging.

            #         cyclic_msg = can.Message(arbitration_id=msg["Id"],
            #                                  data=[0] * msg["DLC"], is_extended_id=False)
            #         if msg["Id"] in self.msg_task:
            #             raise ValueError
            #         else:
            #             self.msg_task[msg['Id']] = self.bus.send_periodic(
            #                 cyclic_msg, msg['Cycle'] / 1000)
            #     while self.exit_flag is False:
            #         time.sleep(1)
            #     logger.info("{} is stopped".format(self.bus_name))

            # 启动 tx cycle
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

            logger.info("{} is stopped".format(self.bus_name))

        except (AttributeError, OSError) as err:
            error_foo = err  # For debugging.
            logger.error("Toomoss Can run error: {}".format(self.bus_name))
            logger.error(err)

    def tx_cycle(self, msg_obj, msg_cls_obj, crc_sig_groups, lock):
        while self.exit_flag is False:
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
                    data_print = (
                        DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(data)
                    )

                    msg = self.can_msg(
                        arbitration_id=msg_id,
                        dlc=length,
                        data=data,
                        is_extended_id=False,
                    )

                    # lock.acquire()
                    self.send(msg)
                    # lock.release()

                    time_stamp = time.time()
                    trace_log = "[{}] {} TX CanBusMsg: [0x{:0>2X}] [{}]  {}".format(
                        time_stamp, self.bus_name, msg_id, length, data_print
                    )
                    # logger.debug(trace_log)
                    if (self.f is not None) and (not self.f.closed):
                        self.f.write(trace_log)
                        self.f.write("\n")

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
        msgs = self.recv()
        if msgs:
            if update_ipdu:
                for msg in msgs:
                    id = msg[0]
                    time_stamp = msg[1]
                    # length = msg[2]
                    data = msg[3]

                    for message in self.pdu_dict:
                        msg_obj = self.pdu_dict[message]
                        if msg_obj["rx_flag"] is not None:
                            if id == msg_obj["msg_id"]:
                                # if id == 0x114:
                                #     logger.info(msg_obj)
                                msg_obj["pdu_data"] = data
                                msg_obj["time_stamp"] = time_stamp
                                msg_obj["rx_flag"] = True
        return msgs

    def rx_update_ipdu(self):
        tracelog_path = "/root/" + self.bus_name + ".txt"
        with open(tracelog_path, "w") as self.f:
            logger.info(
                "{} CanBus Tracelog path is {}".format(self.bus_name, tracelog_path)
            )
            while self.rx_exit_flag is False:
                self.rx_update()
                sleep(0.001)
            sleep(0.1)

    # def rx_update_ipdu_start(self):
    #     thread = threading.Thread(target=self.rx_update_ipdu, name="ToomossCan rx_update_ipdu", daemon=True,)
    #     thread.start()

    def rx_update_stop(self):
        self.exit_flag = True
        self.rx_exit_flag = True
        sleep(2)

    def add_cyclic_msg(self, can_id, dlc, cyclic_rate):
        """
        Add cyclic message to bus
        :param can_id: can message id
        :param dlc: Data length of new cyclic message to add
        :param cyclic_rate: Cycle rate of new cyclic message (in seconds)
        :return:
        """
        try:
            cyclic_msg = can.Message(
                arbitration_id=can_id, data=[0] * dlc, is_extended_id=False
            )
            # if not hasattr(self, "msg_task"):
            #     self.msg_task = {}
            if can_id in self.msg_task:
                logger.info(
                    "{}(): can_id({:#x}) already being published.".format(
                        inspect.stack()[0].function, can_id
                    )
                )
            else:
                self.msg_task[can_id] = self.bus.send_periodic(cyclic_msg, cyclic_rate)
        except (AttributeError, OSError) as e:
            logger.error(
                'SocketCan add cyclic msg error: \
                {} on {}'.format(
                    hex(can_id), self.channel
                )
            )
            logger.error(e)
        except KeyError:
            logger.error(
                'SocketCan add cyclic msg error: \
                {} already exists on {}'.format(
                    hex(can_id), self.bus_name
                )
            )

    def add_cyclic_msg_with_data(self, can_id, data, cyclic_rate):
        """
        Add cyclic message with specific data to bus
        :param can_id: can message id
        :param data: data of can cyclic message
        :param cyclic_rate: Cycle rate of new cyclic message (in seconds)
        :return:
        """
        try:
            cyclic_msg = can.Message(
                arbitration_id=can_id, data=data, is_extended_id=False
            )
            if can_id in self.msg_task:
                logger.error(
                    "{}(): can_id({:#x}) already being published.".format(
                        inspect.stack()[0].function, can_id
                    )
                )
            else:
                self.msg_task[can_id] = self.bus.send_periodic(cyclic_msg, cyclic_rate)
        except (AttributeError, OSError) as e:
            logger.error(
                'SocketCan add cyclic msg error: \
                {} on {}'.format(
                    hex(can_id), self.channel
                )
            )
            logger.error(e)
        except KeyError:
            logger.error(
                'SocketCan add cyclic msg error: \
                {} already exists on {}'.format(
                    hex(can_id), self.channel
                )
            )

    # Failed
    def add_dual_rate_cyclic_msg(
        self, can_id, dlc, count_rate1, cyclic_rate1, cyclic_rate2
    ):
        """
        Add a dual rate cyclic message to bus.
        This method will send a cyclic message at "cyclic_rate1" for
        "count_rate1" times, then continue to send at "cyclic_rate2"
        :param can_id: can message id
        :param dlc: Data length of new cyclic message to add
        :param count_rate1: Number of times to send at cyclic_rate1
        :param cyclic_rate1: First cycle rate of cyclic message (in seconds)
        :param cyclic_rate2: Second cycle rate of cyclic message (in seconds)
        :return:
        """
        try:
            cyclic_msg = can.Message(
                arbitration_id=can_id, data=[0] * dlc, is_extended_id=False
            )
            if can_id in self.msg_task:
                raise ValueError
            else:
                # self, channel, message, count, initial_period, subsequent_period
                self.msg_task[can_id] = can.interface.MultiRateCyclicSendTask(
                    channel=self.channel,
                    message=cyclic_msg,
                    count=count_rate1,
                    initial_period=cyclic_rate1,
                    subsequent_period=cyclic_rate2,
                )
        except (AttributeError, OSError) as e:
            logger.error(
                'SocketCan add dual rate cyclic msg error: \
                {} on {}'.format(
                    hex(can_id), self.bus_name
                )
            )
            logger.error(e)
        except KeyError:
            logger.error(
                'SocketCan add dual rate cyclic msg error: \
                    {} already exists on {}'.format(
                    hex(can_id), self.bus_name
                )
            )

    def remove_cyclic_msg(self, can_id):
        """
        Remove cyclic message from bus
        :param can_id: can message id
        :return:
        """
        try:
            if can_id not in self.msg_task:
                logger.error('CAN ID %s not in cyclic task list' % can_id)
                return False
            self.msg_task[can_id].stop()
            del self.msg_task[can_id]
            # logger.info(self.msg_task.keys())
        except (AttributeError, OSError) as e:
            logger.error(
                'SocketCan remove cyclic msg error: \
                {} on {}'.format(
                    hex(can_id), self.bus_name
                )
            )
            logger.error(e)
        except KeyError:
            logger.error(
                'SocketCan remove cyclic msg error: \
                {} not found on {}'.format(
                    hex(can_id), self.bus_name
                )
            )

    # change the pause_cyclic_msg function, if can_id is None, will stop all msgs on the channel
    def pause_cyclic_msg(self, can_id=None):
        """
        Pause a cyclic message
        :param can_id: can message id, if None mean all can message id in the chanel bus
        :return:
        """
        try:
            if can_id:
                self.msg_task[can_id].stop()
            else:
                for id in self.msg_task.keys():
                    self.msg_task[id].stop()
        except (AttributeError, OSError) as e:
            logger.error(
                'SocketCan pause cyclic msg error: \
                {} on {}'.format(
                    hex(can_id), self.bus_name
                )
            )
            logger.error(e)
        except KeyError:
            logger.error(
                'SocketCan pause cyclic msg error: \
                {} not found on {}'.format(
                    hex(can_id), self.bus_name
                )
            )

    def resume_cyclic_msg(self, can_id):
        """
        Resume a cyclic message
        :param can_id: can message id, if None mean all can message id in the chanel bus
        :return:
        """
        try:
            if can_id:
                self.msg_task[can_id].start()
            else:
                for id in self.msg_task.keys():
                    self.msg_task[id].start()
        except (AttributeError, OSError) as e:
            logger.error(
                'SocketCan resume cyclic msg error: \
                {} on {}'.format(
                    hex(can_id), self.bus_name
                )
            )
            logger.error(e)
        except KeyError:
            logger.error(
                'SocketCan resume cyclic msg error: \
                {} not found on {}'.format(
                    hex(can_id), self.bus_name
                )
            )

    def modify_cyclic_data(self, can_id, data):
        """
        Modify data of existing running cyclic message
        :param can_id: can message id
        :param data: data of can cyclic message
        :return:
        """
        try:
            msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
            self.msg_task[can_id].modify_data(msg)
            # Wait 40ms after data modification
            time.sleep(0.04)
        except (AttributeError, OSError) as e:
            logger.error(
                'CAN modify data error: \
                {} on {}'.format(
                    hex(can_id), self.bus_name
                )
            )
            logger.error(e)
        except KeyError:
            err_msg = "CAN modify data error: {} not found on {}".format(
                hex(can_id), self.bus_name
            )
            hint1 = "Possibly this msg is an output of CGW."
            hint2 = "Look for this msg on another bus, where it is an input of CGW."
            logger.error(err_msg)
            logger.error(hint1)
            logger.error(hint2)

    def read_single_msg_from_obj(self, msg_obj, timeout=1.0):
        return self.read_single_msg(
            msg_obj.msg_id, wait=msg_obj.msg_cyc, timeout=timeout
        )

    def read_single_msg(self, can_id, wait=0, timeout=0.1, log_error=True):
        """
        Read a message from an can interface
        :param can_id: Can id of message to read
        :param wait: Wait time for new message data to propagate.
        :param timeout: Time before function returns if there is
                no data on bus or message with can_id is not found
        :param log_error: In class BusCmd, the higher layers will log the error, so no need to do it here.
        :return:
        """
        try:
            time.sleep(wait)
            interface_bus = can.interface.Bus(bustype='socketcan', channel=self.channel)
            interface_bus.set_filters([{"can_id": can_id, "can_mask": 0xFFFF}])

            msg = None
            start_time = time.time()

            while msg is None or msg.arbitration_id != can_id:
                msg = interface_bus.recv(timeout=timeout)
                self.timestamp = msg.timestamp
                self.dlc = msg.dlc
                elapsed_time = time.time() - start_time

                # timeout if no messages are read after elapsed time
                if elapsed_time > timeout and msg is None:
                    if log_error:
                        logger.error(
                            "CAN read timeout: {} not found on {}".format(
                                hex(can_id), self.bus_name
                            )
                        )

                    return None
                else:
                    time.sleep(0.001)  # loop timing
            interface_bus.shutdown()
        except AttributeError:
            logger.error(
                "AttributeError: Message {} not on bus {}".format(
                    hex(can_id), self.bus_name
                )
            )

            return None

        return msg

    def write_single_msg(self, can_id, data):
        """
        Write a message to the can interface
        :param can_id: Can id of message to write.
        :param data: list of values being written. Length of message
                should match length of CAN id message defined in dbc file.
        :return:
        """
        try:
            bus = can.interface.Bus(bustype='socketcan', channel=self.channel)
            msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
            bus.send(msg)
            bus.shutdown()
        except AttributeError:
            logger.error(
                'CAN write error: \
                {} on {}'.format(
                    hex(can_id), self.bus_name
                )
            )

    def stop(self):
        """
        Stop each task that is sending cyclic messages.
        :return:
        """
        try:
            # if len(self.msg_task)>0:
            #     for can_id, inst in self.msg_task.items():
            #         inst.stop()
            #     del self.msg_task
            self.rx_exit_flag = True
            self.exit_flag = True
        except AttributeError:
            logger.error('SocketCan stop error: {}'.format(self.bus_name))

    def read_msg_cycle_time(self, msg_obj, wait=0, timeout=1.0):
        # It is forbidden to call multiple processes at the same time
        start_time = 0
        interval_time = 0
        if self.read_single_msg(msg_obj.msg_id, wait=wait, timeout=timeout):
            start_time = self.timestamp
            # logger.info("timestamp1 is {}".format(self.timestamp))
            if self.read_single_msg(msg_obj.msg_id, wait=wait, timeout=timeout):
                interval_time = self.timestamp - start_time
                # logger.info("timestamp2 is {}".format(self.timestamp))
                return interval_time
            else:
                return None
        else:
            return None

    def read_msg_dlc(self, msg_obj, wait=0, timeout=1.0):
        if self.read_single_msg(msg_obj.msg_id, wait=wait, timeout=timeout):
            return self.dlc
        else:
            return None

    # --------------------   toomoss api -----------------------------------
    def toomoss_scandevice(self):
        # Scan device
        devhandles = (c_uint * 20)()
        ret = USB_ScanDevice(byref(devhandles))

        if ret == 0:
            logger.warning("No device connected!")
        else:
            logger.info("Have %d device connected!" % ret)
            for i in range(0, ret):
                logger.info("Connected Device_{} : {}".format(i + 1, devhandles[i]))
                i += 1
        return devhandles

    def toomoss_opendevice(self):
        # param: devhandle  type:c_uint   such as  1409286394
        # Open device
        ret = USB_OpenDevice(self.devhandle)
        logger.info(ret)
        if bool(ret):
            logger.info("Open toomoss device {} success!".format(self.devhandle))
        else:
            logger.info("Open toomoss device {} failed!".format(self.devhandle))

    def toomoss_device_info(self):
        # Get device infomation
        USB2XXXInfo = DEVICE_INFO()
        USB2XXXFunctionString = (c_char * 256)()
        ret = DEV_GetDeviceInfo(
            self.devhandle, byref(USB2XXXInfo), byref(USB2XXXFunctionString)
        )
        if bool(ret):
            logger.debug("USB2XXX device infomation:")
            logger.debug(
                "--Firmware Name: %s" % bytes(USB2XXXInfo.FirmwareName).decode('ascii')
            )
            logger.debug(
                "--Firmware Version: v%d.%d.%d"
                % (
                    (USB2XXXInfo.FirmwareVersion >> 24) & 0xFF,
                    (USB2XXXInfo.FirmwareVersion >> 16) & 0xFF,
                    USB2XXXInfo.FirmwareVersion & 0xFFFF,
                )
            )
            logger.debug(
                "--Hardware Version: v%d.%d.%d"
                % (
                    (USB2XXXInfo.HardwareVersion >> 24) & 0xFF,
                    (USB2XXXInfo.HardwareVersion >> 16) & 0xFF,
                    USB2XXXInfo.HardwareVersion & 0xFFFF,
                )
            )
            logger.debug(
                "--Build Date: %s" % bytes(USB2XXXInfo.BuildDate).decode('ascii')
            )
            toomoss_SerialNumber = ""
            for i in range(0, len(USB2XXXInfo.SerialNumber)):
                toomoss_SerialNumber += "%08X" % USB2XXXInfo.SerialNumber[i]

            logger.debug("--Serial Number: {}".format(toomoss_SerialNumber))
            logger.debug(
                "--Function String: %s"
                % bytes(USB2XXXFunctionString.value).decode('ascii')
            )
        else:
            logger.debug("Get device infomation faild!")
            # exit()

    def toomoss_init_can(self):
        # param: devhandle  type:c_uint   such as  1409286394
        # param: canindex  type:int   such as  0 , 1 , 2
        # 初始化CAN
        CANConfig = CAN_INIT_CONFIG()
        CANConfig.CAN_Mode = self.canconfig[0]  # 1-自发自收模式，0-正常模式
        CANConfig.CAN_ABOM = self.canconfig[1]
        CANConfig.CAN_NART = self.canconfig[2]
        CANConfig.CAN_RFLM = self.canconfig[3]
        CANConfig.CAN_TXFP = self.canconfig[4]

        # 配置波特率,波特率 = 100M/(BRP*(SJW+BS1+BS2))
        CANConfig.CAN_BRP_CFG3 = self.brateconfig["CAN_BRP_CFG3"]
        CANConfig.CAN_BS1_CFG1 = self.brateconfig["CAN_BS1_CFG1"]
        CANConfig.CAN_BS2_CFG2 = self.brateconfig["CAN_BS2_CFG2"]
        CANConfig.CAN_SJW = self.brateconfig["CAN_SJW"]

        ret = CAN_Init(self.devhandle, self.canindex, byref(CANConfig))
        if ret != CAN_SUCCESS:
            logger.warning("Config CAN failed!")
        else:
            logger.info("Config CAN INIT Success!")

    def toomoss_init_canfd(self):
        # param: devhandle  type:c_uint   such as  1409286394
        # param: canindex  type:int   such as  0 , 1 , 2

        # 初始化CAN
        CANConfig = CANFD_INIT_CONFIG()
        CANConfig.Mode = self.canfdconfig[0]  # 1-自发自收模式，0-正常模式
        CANConfig.ISOCRCEnable = self.canfdconfig[1]  # 0-禁止ISO CRC,1-使能ISO CRC
        CANConfig.RetrySend = self.canfdconfig[2]
        CANConfig.ResEnable = self.canfdconfig[3]
        # 配置波特率,波特率 = 40M/(BRP*(1+BS1+BS2))
        CANConfig.NBT_BRP = self.nbrateconfig["NBT_BRP"]
        CANConfig.NBT_SEG1 = self.nbrateconfig["NBT_SEG1"]
        CANConfig.NBT_SEG2 = self.nbrateconfig["NBT_SEG2"]
        CANConfig.NBT_SJW = self.nbrateconfig["NBT_SJW"]

        CANConfig.DBT_BRP = self.dbrateconfig["DBT_BRP"]
        CANConfig.DBT_SEG1 = self.dbrateconfig["DBT_SEG1"]
        CANConfig.DBT_SEG2 = self.dbrateconfig["DBT_SEG2"]
        CANConfig.DBT_SJW = self.dbrateconfig["DBT_SJW"]

        ret = CANFD_Init(self.devhandle, self.canindex, byref(CANConfig))
        if ret != CANFD_SUCCESS:
            logger.warning(
                "Config ({}, {}) failed!".format(self.devhandle, self.canindex)
            )
        else:
            logger.info(
                "Config ({}, {}) Success!".format(self.devhandle, self.canindex)
            )

    def toomoss_canfilter_init(self):
        # 配置过滤器，必须配置，否则可能无法收到数据
        CANFilter = CAN_FILTER_CONFIG()
        CANFilter.Enable = self.canfilter[0]
        CANFilter.ExtFrame = self.canfilter[1]
        CANFilter.FilterIndex = self.canfilter[2]
        CANFilter.FilterMode = self.canfilter[3]
        CANFilter.MASK_IDE = self.canfilter[4]
        CANFilter.MASK_RTR = self.canfilter[5]
        CANFilter.MASK_Std_Ext = self.canfilter[6]
        ret = CAN_Filter_Init(self.devhandle, self.canindex, byref(CANFilter))
        if ret != CANFD_SUCCESS:
            logger.warning(
                "Config CAN_Filter_Init ({}, {}) failed!".format(
                    self.devhandle, self.canindex
                )
            )
        else:
            logger.info(
                "Config CAN_Filter_Init ({}, {}) Success!".format(
                    self.devhandle, self.canindex
                )
            )

    def toomoss_clearmsg(self):
        ret = CAN_ClearMsg(self.devhandle, self.canindex)
        if ret == CAN_SUCCESS:
            logger.info("CAN_ClearMsg Success")
        else:
            logger.info("CAN_ClearMsg Failed")

    def toomoss_startgetmsg(self):
        ret = CAN_StartGetMsg(self.devhandle, self.canindex)
        if ret == CAN_SUCCESS:
            logger.info("CAN_StartGetMsg Success")
        else:
            logger.info("CAN_StartGetMsg Failed")

    def toomoss_stopgetmsg(self):
        ret = CAN_StopGetMsg(self.devhandle, self.canindex)
        if ret == CAN_SUCCESS:
            logger.info("CAN_StopGetMsg Success")
        else:
            logger.info("CAN_StopGetMsg Failed")

    def toomoss_close_device(self):
        # Close device     Toomos does not need to be closed
        ret = USB_CloseDevice(self.devhandle)
        if bool(ret):
            logger.info("Close device success!")
        else:
            logger.warning("Close device faild!")

    # --------------------   toomoss high level api -----------------------------------
    def can_msg(
        self,
        arbitration_id: int,
        dlc: int,
        data: list,
        is_extended_id=False,
        RemoteFlag=0,
        Flags=5,
    ):
        # if self.is_fd:
        #     CanMsg = (CANFD_MSG*1)()
        #     datas = (c_ubyte * 64)(*data)
        #     CanMsg[0].Flags = Flags  # 0 -- can   4 -- canfd    5 -- canfd 加速
        #     CanMsg[0].ID = arbitration_id
        #     CanMsg[0].DLC = dlc
        #     CanMsg[0].Data = datas

        #     return CanMsg[0]

        # else:
        #     if is_extended_id:
        #         ExternFlag = 1
        #     else:
        #         ExternFlag = 0
        #     CanMsg = (CAN_MSG*1)()
        #     datas = (c_ubyte * 8)(*data)
        #     CanMsg[0].ExternFlag = ExternFlag
        #     CanMsg[0].RemoteFlag = RemoteFlag
        #     CanMsg[0].ID = arbitration_id
        #     CanMsg[0].DataLen = dlc
        #     CanMsg[0].Data = datas

        #     return CanMsg[0]

        if self.is_fd:
            CanMsg = (CANFD_MSG * 1)()
            datas = (c_ubyte * 64)(*data)
            # CanMsg[i].ID = i|CANFD_MSG_FLAG_IDE   # 扩展报文
            CanMsg[0].Flags = Flags  # 0 -- can   4 -- canfd    5 -- canfd 加速
            CanMsg[0].ID = arbitration_id
            CanMsg[0].DLC = dlc
            CanMsg[0].Data = datas

            return CanMsg[0]

        else:
            # if is_extended_id:
            #     ExternFlag = 1
            # else:
            #     ExternFlag = 0
            CanMsg = (CANFD_MSG * 1)()
            datas = (c_ubyte * 64)(*data)
            CanMsg[0].Flags = 0
            CanMsg[0].ID = arbitration_id
            CanMsg[0].DLC = dlc
            CanMsg[0].Data = datas

            return CanMsg[0]

    def send(self, CanMsg, count=1):
        # toomoss 发送CAN帧
        msg = byref(CanMsg)
        # Bug  几个toomoss 在一个上位机，单独使用 can OK，单独使用 canfd OK；但 can，canfd一起使用，canfd OK， can大概率不OK
        # if self.is_fd:
        #     SendedNum = CANFD_SendMsg(self.devhandle, self.canindex, msg, count)
        # else:
        #     SendedNum = CAN_SendMsg(self.devhandle, self.canindex, msg, count)

        # New 兼容或改变 flags=0 ----- can     flags=5 -----  canfd 加速

        SendedNum = CANFD_SendMsg(self.devhandle, self.canindex, msg, count)

        if SendedNum >= 0:
            pass
            # logger.debug("Success send frames:%d" % SendedNum)
        else:
            logger.debug("ERROR: Send CAN data failed!")

    def recv(self):
        # 读取CAN数据

        # if self.is_fd:
        #     CanMsgBuffer = (CANFD_MSG*10240)()
        #     CanNum = CANFD_GetMsg(self.devhandle, self.canindex, byref(CanMsgBuffer), 10240)
        # else:
        #     CanMsgBuffer = (CAN_MSG*10240)()
        #     CanNum = CAN_GetMsg(self.devhandle, self.canindex, byref(CanMsgBuffer))

        CanMsgBuffer = (CANFD_MSG * 10240)()
        CanNum = CANFD_GetMsg(self.devhandle, self.canindex, byref(CanMsgBuffer), 10240)

        msgs = []
        if CanNum > 0:
            # logger.debug("CanNum = %d" % CanNum)
            for i in range(0, CanNum):
                id = CanMsgBuffer[i].ID
                time_stamp = CanMsgBuffer[i].TimeStamp
                # logger.debug("CanMsg[%d].ID = %d" % (i, id))
                # logger.debug("CanMsg[%d].TimeStamp = %d" % (i, time_stamp))

                # if self.is_fd:
                #     length = CanMsgBuffer[i].DLC
                # else:
                #     length = CanMsgBuffer[i].DataLen

                length = CanMsgBuffer[i].DLC

                data = []
                data_print = ""
                for j in range(0, length):
                    data_value = CanMsgBuffer[i].Data[j]
                    data.append(data_value)
                    data_print += " {:0>2X}".format(data_value)
                msg = (id, time_stamp, length, data)
                msgs.append(msg)
                trace_log = "[{}] {} RX CanBusMsg: [0x{:0>2X}] [{}]  {}".format(
                    time_stamp, self.bus_name, id, length, data_print
                )
                # logger.info(trace_log)
                if (self.f is not None) and (not self.f.closed):
                    self.f.write(trace_log)
                    self.f.write("\n")
            return msgs
        elif CanNum == 0:
            # logger.debug("No CAN data!")
            return msgs
        else:
            logger.debug("ERROR: Get CAN data error!")

    def start_toomoss(self):
        global is_scaned_toomoss_devices
        if is_scaned_toomoss_devices[0]:
            logger.debug("scaned toomoss devices")
        else:
            self.toomoss_scandevice()
            is_scaned_toomoss_devices[0] = True  # Can only be called once

        global opened_toomoss_devices
        if self.devhandle in opened_toomoss_devices:
            logger.debug("Toomoss {}  已经打开了,无需再次启动".format(self.devhandle))
        else:
            self.toomoss_opendevice()
            self.toomoss_device_info()
            opened_toomoss_devices.append(self.devhandle)

        # if self.is_fd:
        #     self.toomoss_init_canfd()
        # else:
        #     self.toomoss_init_can()
        #     self.toomoss_canfilter_init()

        self.toomoss_init_canfd()


if __name__ == '__main__':
    # Work Path: ecu_simulator/
    # cmd : python3 sdk/driver/toomoss/toomoss_can.py
    can_test = ToomossCan("1", [1392511910, 0])
    can_test.toomoss_startgetmsg()
    msg = can_test.can_msg(0x53F, 8, [0x3F, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
    i = 1
    while i < 20:
        can_test.send(msg)
        i += 1
        sleep(0.1)
    can_test.toomoss_clearmsg()
    sleep(0.01)
    can_test.recv()

    sleep(0.01)
    can_test.recv()

    can_test.toomoss_stopgetmsg()
    # can_test.toomoss_close_device()

    # can_test2 = ToomossCan("2", [1392512057, 1], is_fd=True)
    # msg = can_test2.can_msg(0x53F, 8, [0x3F, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
    # i=1
    # while i < 50:
    #     can_test2.send(msg)
    #     i += 1
    #     sleep(0.1)
    # can_test2.recv()
    # can_test2.toomoss_close_device()
