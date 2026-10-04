# -*- coding: utf-8 -*-
"""
@File        : toomoss_lin.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022-12-09 18:06
@Description : 
@Examples    :
"""
import uuid
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
from collections import deque, OrderedDict, defaultdict

from xat_ecu.legacy.sdk.driver.toomoss.sdk.api.python_sat.usb_device import *
from xat_ecu.legacy.sdk.driver.toomoss.toomoss_constant import *
from xat_ecu.legacy.sdk.driver.toomoss.sdk.api.python_sat.usb2lin_ex import *
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from xat_ecu.legacy.sdk.driver.toomoss.sdk.api.python_sat.usb2pwm import PWM_CONFIG, PWM_Init, PWM_SUCCESS, PWM2_Stop
from xat_ecu.legacy.sdk.driver.toomoss.sdk.api.python_sat.usb2pwm import PWM_CAP_Stop, PWM_CAP_DATA, PWM_CAP_GetData, \
    PWM_CAP_Init, PWM2_Start, PWM2_Init
from xat_ecu.legacy.common import exception_error
from xat_ecu.legacy.common.error_code import StatusCode
from xat_ecu.legacy.common.exception_error import error_check
from xat_ecu.legacy.common.error_callback import error_callback
from xat_ecu.legacy.sdk.driver.toomoss.toomoss_lin_status import ToomossStatus


def get_toomoss_device():
    devhandles = (c_uint * 20)()
    ret = USB_ScanDevice(byref(devhandles))

    if ret == 0:
        # logger.warning("No device connected!")
        logger.warning("没有发现LIN设备连接")
    else:
        logger.info("Have %d device connected!" % ret)
        for i in range(0, ret):
            logger.info("Connected Device_{} : {}".format(i + 1, devhandles[i]))
            i += 1
    return devhandles


class ToomossLin(threading.Thread):
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
            brate=19200,
            master_or_slave=LIN_EX_SLAVE,
            ipdu=None,
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
        threading.Thread.__init__(self, name=f"{bus_name}_{bus_name}")
        self.daemon = True
        self.bus_name = bus_name  # name of channel, such as 'etp'
        self.devhandle = channel[0]
        self.linindex = channel[1]
        self.monitor_index = 1
        self.monitor_second = 5
        self.monitor_period = 0.01
        self.brate = brate
        self.master_or_slave = master_or_slave

        self.dbc_json = dbc_json

        self.exit_flag = False  # True means stop sending cyclic messages tasks
        self.msg_task = {}  # Tasks to sending cyclic messages
        self.timestamp = None
        self.dlc = None
        self.callback = kwargs.get('callback')
        self.lock = threading.Lock()
        self.recv_data = None
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
        self.is_first_frame = False
        # start toomoss
        # self.start_toomoss()
        self.use_schedule_table = False
        self.message_queue = deque([], maxlen=10000)
        self.reset_count = 0

    def run(self):
        """
        Start tasks to transmit each cyclic message read from json file
        :return:
        """
        self.start_toomoss()
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

            for message in self.pdu_dict:
                msg_obj = self.pdu_dict[message]
                if msg_obj.get("tx_flag"):
                    self.toomoss_set_salve_msg(
                        pid=msg_obj["msg_id"],
                        dlc=msg_obj["msg_length"],
                        data=msg_obj["pdu_data"],
                    )
                    # logger.info(msg_obj)

                    # msg_cls_obj = getattr(self.bus_cls_obj, message)
                    # crc_sig_groups = msg_cls_obj.sig_group_dataid_dict
                    # cycle_time = msg_cls_obj.msg_cycle
                    # if crc_sig_groups:  # crc sig group (dataid)
                    #     self.tx_cycle_start(
                    #         message, msg_obj, msg_cls_obj, crc_sig_groups, cycle_time
                    #     )

            self.rx_update_ipdu()
            # logger.info("{} is stopped".format(self.bus_name))
            logger.info("{} 线程退出，已经停止。".format(self.bus_name))

        except (AttributeError, OSError) as err:
            error_foo = err  # For debugging.
            # logger.error("Toomoss Lin 运行报错: {}".format(self.bus_name))
            # logger.error(err)
            logger.warning(f"Lin {self.bus_name} 运行报错，得到：{err}")

        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/toomoss/toomoss_lin.py")
            with error_check(StatusCode.TOMOSSLIN_LIN_RUN_ERR, exception_error.ToomossError):
                raise AssertionError(f"Lin运行线程报错：{e}")
        finally:
            global is_scaned_toomoss_devices
            logger.info(f"当前的toomoss被扫描过：{is_scaned_toomoss_devices}")
            is_scaned_toomoss_devices = [None]

            global opened_toomoss_devices
            logger.info(f"当前已经打开过的toomoss devices是：{opened_toomoss_devices}")
            opened_toomoss_devices = []
            self.toomoss_close_device()
            self.message_queue.clear()

    # def tx_cycle(self, msg_obj, msg_cls_obj, crc_sig_groups, cycle_time):
    #     while self.exit_flag is False:
    #         # if crc_sig_groups:  # crc sig group (dataid)

    #         if not self.pause_flag:
    #             for sig_group in crc_sig_groups:
    #                 self.ipdu_instance.set_crc_count(
    #                     msg_cls_obj,
    #                     sig_group,
    #                     do_cntr=getattr(msg_cls_obj, (sig_group + "_cntr"))
    #                     if hasattr(msg_cls_obj, (sig_group + "_cntr"))
    #                     else None,
    #                     do_crc=getattr(msg_cls_obj, (sig_group + "_crc"))
    #                     if hasattr(msg_cls_obj, (sig_group + "_crc"))
    #                     else None,
    #                 )

    #         self.toomoss_set_salve_msg(
    #             pid=msg_obj["msg_id"],
    #             dlc=msg_obj["msg_length"],
    #             data=msg_obj["pdu_data"],
    #         )
    #         # logger.info("msg_id" +  str(msg_obj["msg_id"]) + str(msg_obj["msg_length"]) + str(msg_obj["pdu_data"]))
    #         # msg_obj["tx_flag"] = False

    #         sleep(cycle_time)

    #     # return i
    #     # start = time.time()
    #     # end = time.time()
    #     # logger.info(end - start)
    #     # logger.info()

    # def tx_cycle_start(
    #     self, msg_name, msg_obj, msg_cls_obj, crc_sig_groups, cycle_time
    # ):
    #     # logger.info(msg_name)
    #     thread = threading.Thread(
    #         target=self.tx_cycle,
    #         name=msg_name,
    #         args=(msg_obj, msg_cls_obj, crc_sig_groups, cycle_time),
    #     )
    #     thread.start()

    def toomoss_stop_msg_by_id(self, message_id):
        for message in self.pdu_dict:
            msg_obj = self.pdu_dict[message]
            if message_id == msg_obj["msg_id"]:
                self.pdu_dict[message]["tx_flag"] = False

    def toomoss_start_msg_by_id(self, message_id):
        for message in self.pdu_dict:
            msg_obj = self.pdu_dict[message]
            if message_id == msg_obj["msg_id"]:
                self.toomoss_set_salve_msg(
                    pid=msg_obj["msg_id"],
                    dlc=msg_obj["msg_length"],
                    data=msg_obj["pdu_data"],
                )

    def on_rx_set_tx_lin(self, message):
        msg_obj = self.pdu_dict[message]
        msg_cls_obj = getattr(self.bus_cls_obj, message)
        crc_sig_groups = msg_cls_obj.sig_group_dataid_dict
        # cycle_time = msg_cls_obj.msg_cycle
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
            # if (
            #     hasattr(msg_cls_obj, (sig_group + "_crc"))
            #     and getattr(msg_cls_obj, (sig_group + "_crc")) == False
            # ):
            #     logger.debug("信号组 {} 没有计算crc".format(sig_group))
            # else:
            #     self.ipdu_instance.set_crc_count(
            #         msg_cls_obj,
            #         sig_group,
            #         do_cntr=getattr(msg_cls_obj, (sig_group + "_cntr"))
            #         if hasattr(msg_cls_obj, (sig_group + "_cntr"))
            #         else None,
            #     )

        if not self.pause_flag:
            if msg_obj.get("tx_flag") == False:
                # 暂停发送 lin ，将 lin salve mode 设为  从机接收数据
                self.toomoss_set_salve_msg(
                    pid=msg_obj["msg_id"],
                    dlc=msg_obj["msg_length"],
                    data=msg_obj["pdu_data"],
                    MsgType=LIN_EX_MSG_TYPE_SR,
                )
            elif crc_sig_groups or msg_obj.get("tx_change"):  # 判断是否需要 e2e 或 是否需要正常更新值
                self.toomoss_set_salve_msg(
                    pid=msg_obj["msg_id"],
                    dlc=msg_obj["msg_length"],
                    data=msg_obj["pdu_data"],
                )
                # logger.info(msg_obj["msg_id"])
                # logger.info(msg_obj["pdu_data"])

                if msg_obj.get("tx_change") == True:
                    msg_obj["tx_change"] = False

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
                            # RX message
                            if id == msg_obj["msg_id"]:
                                msg_obj["pdu_data"] = data
                                msg_obj["time_stamp"] = time_stamp
                                msg_obj["rx_flag"] = True
                        else:
                            # TX message
                            if id == msg_obj["msg_id"]:
                                self.on_rx_set_tx_lin(message)
        return msgs

    def rx_update_ipdu(self):
        while self.rx_exit_flag is False:
            if not self.pause_flag:
                self.rx_update()
                sleep(0.01)   # 1ms改为10ms  降低 toomoss lin 暂用上位机的cup负载
            else:
                sleep(1)  # 降低 toomoss lin 占用cpu负载

    def rx_update_ipdu_start(self):
        thread = threading.Thread(
            target=self.rx_update_ipdu, name="ToomossLin rx_update_ipdu"
        )
        thread.start()

    def rx_update_stop(self):
        self.rx_exit_flag = True

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
            logger.error('Lin停止错误: {}'.format(self.bus_name))

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
            # logger.warning("No device connected!")
            logger.warning("没有发现LIN设备连接")
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
        # logger.info(ret)
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

    def toomoss_init_lin_slave(self):
        # param: devhandle  type:c_uint   such as  1409286394
        # param: linindex  type:int   such as  0 , 1 , 2

        # 初始化配置从机LIN
        with self.lock:
            ret = LIN_EX_Init(self.devhandle, self.linindex, self.brate, LIN_EX_SLAVE)
            if ret != LIN_EX_SUCCESS:
                # logger.error(f"Config slave LIN failed!, ret:{ret}")
                logger.debug(f"配置slave lin失败，返回code:{ret}")
                if ret == -2:
                    with error_check(StatusCode.TOMOSSLIN_LIN_EX_USB_WRITE_FAIL_ERR, exception_error.ToomossError, error_callback):
                        raise
                elif ret == -4:
                    with error_check(StatusCode.TOMOSSLIN_LIN_EX_CMD_FAIL_ERR, exception_error.ToomossError):
                        raise
                elif ret == -7:
                    with error_check(StatusCode.TOMOSSLIN_LIN_POWER_ERR, exception_error.ToomossError):
                        raise
                else:
                    raise Exception(f"配置slave LIN {self.linindex}失败!, 返回值:{ret}, 请重新插拔lin")
            else:
                # logger.info("Config slave LIN Success!")
                logger.info("配置lin slave成功")
            time.sleep(0.3)

    def toomoss_set_salve_msg(
            self,
            pid: int,
            dlc: int,
            data: list,
            MsgType=LIN_EX_MSG_TYPE_SW,  # = 3  # 从机发送数据
            CheckType=LIN_EX_CHECK_EXT,
    ):
        # LIN_EX_MSG_TYPE_SR     = 4	# 从机接收数据

        LINMsg = LIN_EX_MSG()
        LINMsg.PID = pid
        LINMsg.MsgType = MsgType
        LINMsg.CheckType = CheckType  # 使用增强型校验
        LINMsg.Data = (c_ubyte * 8)(*data)
        LINMsg.DataLen = dlc

        ret = LIN_EX_SlaveSetIDMode(self.devhandle, self.linindex, byref(LINMsg), 1)
        if ret != LIN_EX_SUCCESS:
            ToomossStatus.STATUS = ret
            # logger.debug(
            #     "ERROR: Set LIN ID Mode failed! Lin device is [{} , {} ]".format(
            #         self.devhandle, self.linindex
            #     )
            # )
            # logger.debug("ERROR: Set_LIN_Mode ret is {}".format(ret))
            logger.warning(f"{self.devhandle}|{self.linindex}设置Lin值错误：{ret}")
        # else:
        #     logger.info("Set LIN ID Mode success!")

    def clear_accept_queue_message(self):
        self.message_queue.clear()

    def toomoss_close_device(self):
        # Close device      Toomos does not need to be closed
        ret = USB_CloseDevice(self.devhandle)
        if bool(ret):
            # logger.info("Close device success!")
            logger.info("关闭设备成功！")
        else:
            # logger.warning("Close device faild!")
            logger.info("关闭设备失败！")

    # --------------------   toomoss high level api -----------------------------------
    def recv(self):
        # 读取Lin数据

        LINOutMsg = (LIN_EX_MSG * 1024)()  # 缓冲区尽量大一点，防止缓冲区溢出，程序异常崩溃
        ret = LIN_EX_SlaveGetData(self.devhandle, self.linindex, LINOutMsg)
        msgs = []
        if ret < LIN_EX_SUCCESS:
            # logger.debug("ERROR: LIN slave read data error!")
            ToomossStatus.STATUS = ret
            logger.warning(f"lin slave读取数据错误,错误码：{ret}")
        elif ret > 0:
            # logger.debug("CanNum = %d" % ret)
            for i in range(ret):
                if not self.is_first_frame:
                    self.is_first_frame = True
                    self.t = time.time() - LINOutMsg[i].Timestamp / 10 ** 3
                    time_stamp = time.time()
                else:
                    # toomoss 获取的时间
                    time_stamp = self.t + LINOutMsg[i].Timestamp / 10 ** 3
                pid = LINOutMsg[i].PID
                # get id
                pid = pid & 0x3F

                # logger.debug("LinMsg[%d].ID = 0x%02X" % (i, pid))
                length = LINOutMsg[i].DataLen
                if length > 8:
                    logger.error(f"lin bus： {self.bus_name} 接收错误，数据长度超过 8")
                    length = 8
                # logger.debug("LinMsg[%d].DataLen = %dX" % (i, length))

                # toomoss 获取的时间
                # time_stamp = LINOutMsg[i].Timestamp
                # 上位机获取的时间
                # time_stamp = time.time()
                # logger.debug("LinMsg[%d].Timestamp = %d" % (i, time_stamp))
                if self.use_schedule_table:
                    self.message_queue.append([pid, LINOutMsg[i].Timestamp])
                data = []
                data_print = ""
                for j in range(0, length):
                    data_value = LINOutMsg[i].Data[j]
                    data.append(data_value)
                    data_print += " {:0>2X}".format(data_value)
                msg = (pid, time_stamp, length, data)
                check = LINOutMsg[i].Check
                msgs.append(msg)
                # logger.debug("LinMsg[{}].Data = {}".format(i, data_print))
                if self.callback:
                    with error_check(StatusCode.TOMOSSLIN_LIN_LOG_WRITE_ERR, exception_error.ToomossError):
                        self.callback(
                            device_type='toomoss_lin', 
                            msg=(pid, LINOutMsg[i].Timestamp, length, data_print), 
                            check=check, bus_name=self.bus_name)

            return msgs

    def check_toomoss_process(self):
        if self.reset_count >= 5:
            logger.info(f"lin重启次数大于5次，不在重启.")
            return
        if ToomossStatus.STATUS != LIN_EX_SUCCESS:
            logger.info(f"当前lin状态码是：{ToomossStatus.STATUS}")
            try:
                self.pause_flag = True
                logger.info(f"暂停lin收发消息.")
                USB_ResetDevice(self.devhandle)
                self.toomoss_close_device()

                global opened_toomoss_devices
                if self.devhandle in opened_toomoss_devices:
                    opened_toomoss_devices.remove(self.devhandle)
                self.start_toomoss()
                self.pause_flag = False
                logger.info(f"已经恢复lin收发消息.")
            finally:
                self.reset_count += 1
                logger.info(f"lin已经重启：{self.reset_count} 次")

    def recv_pdu_d(self):
        """
        诊断lin使用
        
        """
        if self.recv_data:
            msg = self.recv_data.pop(0)
        else:
            msgs = self.recv()
            if msgs:
                if len(msgs) == 1:
                    msg = msgs[0]
                else:
                    self.recv_data = msgs
                    msg = self.recv_data.pop(0)
            else:
                msg = None
        return msg
        
    def pause_cycle_tx_rx(self):
        # 配合性能接口 recv_pdu_d， 释放cpu负载
        self.pause_flag = True

    def resume_cycle_tx_rx(self):
        # 配合性能接口 recv_pdu_d， 释放cpu负载
        self.pause_flag = False

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

        if self.master_or_slave == LIN_EX_SLAVE:
            self.toomoss_init_lin_slave()
            ToomossStatus.STATUS = LIN_EX_SUCCESS

    def toomoss_init_pwm_then_start(self, RunTimeOfUs=1000, frequency=1000, polarity=0, precision=1000, dutyCycle=250,
                                    monitor=False):
        """
        初始化并启动PWM波输出
        :param RunTimeOfUs: 发送时长
        :param frequency： 频率
        :param polarity： 极性
        :param precision： 精度
        :param dutyCycle： 占空比
        :param monitor: 是否监控pwm波的发送
        """

        ret = PWM2_Init(self.devhandle, self.linindex, frequency, polarity, precision, dutyCycle)
        if ret != PWM_SUCCESS:
            logger.info("Initialize pwm faild!")
            return ret, "Initialize pwm faild!"
        else:
            logger.info("Initialize pwm sunccess!")

        ret = PWM2_Start(self.devhandle, self.linindex, RunTimeOfUs)
        if ret != PWM_SUCCESS:
            logger.info("Start pwm faild!")
            return ret, "Start pwm faild!"
        else:
            logger.info("Start pwm sunccess!")
        time.sleep(1)
        ret = PWM2_Stop(self.devhandle, self.linindex)
        if ret != PWM_SUCCESS:
            logger.info("Stop pwm faild!")
            return ret, "Stop pwm faild!"
        else:
            logger.info("Stop pwm sunccess!")
            return ret, "run pwm success"

        if monitor:
            self.tomoss_monitor_pwm()

    def tomoss_monitor_pwm(self):

        # 初始化PWM监控
        TimePrecUs = 10  # PWM监控时间精度，单位为微秒
        ret = PWM_CAP_Init(self.devhandle, self.monitor_index, TimePrecUs)
        if ret != PWM_SUCCESS:
            logger.info("Start pwm sniffer faild!")
            exit()
        else:
            logger.info("Start pwm sniffer sunccess!")
        # 循环获取数据
        for t in range(0, int(self.monitor_second / self.monitor_period)):
            PWMData = PWM_CAP_DATA()
            ret = PWM_CAP_GetData(self.devhandle, self.monitor_index, byref(PWMData))
            if ret != PWM_SUCCESS:
                logger.info("pwm cap data faild!")
            else:
                logger.info(f"HighValue={PWMData.HighValue * TimePrecUs} us")
                logger.info(f"LowValue={PWMData.LowValue * TimePrecUs} us")
                if ((PWMData.HighValue + PWMData.LowValue) > 0) and (PWMData.HighValue < 0xFFFF) \
                        and (PWMData.LowValue < 0xFFFF):
                    pwm_cap_freq = 1000000 / ((PWMData.HighValue + PWMData.LowValue) * TimePrecUs)
                    pwm_cap_duty = (100 * PWMData.HighValue) / (PWMData.HighValue + PWMData.LowValue)
                    logger.info(f"cap freq:{pwm_cap_freq}Hz cap duty:{pwm_cap_duty}%")
                else:
                    logger.info("未检测到PWM信号")
            sleep(self.monitor_period)
        # 停止监控
        PWM_CAP_Stop(self.devhandle, self.monitor_index)


if __name__ == '__main__':
    # Work Path: ecu_simulator/
    # cmd : python3 sdk/driver/toomoss/toomoss_can.py
    lin_test = ToomossLin("1", [1409286394, 0])
    lin_test.toomoss_set_salve_msg(
        0x11, 8, [0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88]
    )

    sleep(0.5)
    i = 1
    while i < 20:
        i += 1
        lin_test.recv()
        lin_test.toomoss_set_salve_msg(
            0x11, 8, [i, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88]
        )
        sleep(0.5)

    lin_test.toomoss_close_device()

    # lin_test2 = ToomossCan("2", [1392512057, 1], is_fd=True)
    # msg = lin_test2.can_msg(0x53F, 8, [0x3F, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
    # i=1
    # while i < 50:
    #     lin_test2.send(msg)
    #     i += 1
    #     sleep(0.1)
    # lin_test2.recv()
    # lin_test2.toomoss_close_device()
