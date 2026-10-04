# -*- coding: utf-8 -*-
"""
@File        : socket_can.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021-05-07 09:06
@Description : The basic interfaces of socket can,
               porting from Alpha2 project
@Examples    :
"""
import can
import json
import time
from time import sleep
import inspect
import threading
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding


class SocketCan(threading.Thread):
    """
    Provide interfaces:
      1. send single message
      2. read single message
      3. send cyclic message with modification
         add/remove/pause/resume cyclic msg, modify data
         add_dual_rate_cyclic_msg
    """

    def __init__(
            self, bus_name, channel, bitrate=500000, ipdu=None, is_fd=False, dbc_json=None, **kwargs
    ):
        """
        Initialize a SocketCan object.
        :param bus_name: bus name, such as 'bodycan', 'ept'
        :param channel: channel interface, such as 'can0', 'can1'
        :param bitrate: bitrate of socket can, default is 500000
        :param dbc_json: dbc_json file which defined cyclic message
        """
        threading.Thread.__init__(self, name=bus_name)
        self.bus_name = bus_name  # name of channel, such as 'etp'
        self.channel = channel  # channel name, such as 'can0'
        self.bitrate = bitrate
        self.dbc_json = dbc_json
        self.is_fd = is_fd
        can.rc['interface'] = 'socketcan'
        can.rc['channel'] = self.channel
        can.rc['bitrate'] = self.bitrate
        can.rc['fd'] = self.is_fd
        self.bus = can.interface.Bus(receive_own_messages=True)
        self.notifier = can.Notifier(self.bus, [])
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

            self.notifier.add_listener(self.rx_update)

            while self.rx_exit_flag is False:
                sleep(5)
            self.notifier.stop()
            self.bus.shutdown()

            logger.info("{} is stopped".format(self.bus_name))

        except (AttributeError, OSError) as err:
            error_foo = err  # For debugging.
            logger.error("SocketCan run error: {}".format(self.bus_name))
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

                    msg = can.Message(
                        arbitration_id=msg_id,
                        data=data,
                        is_fd=self.is_fd,
                        is_extended_id=False,
                        bitrate_switch=self.is_fd,
                    )
                    # lock.acquire()
                    self.bus.send(msg, timeout=0.1)
                    # if msg_id == 0x176 or 0x166:
                    #     self.bus.send(msg, timeout=0.1)
                    # else:
                    #     break
                    # lock.release()

                    # time_stamp = time.time() - self.record_time
                    time_stamp = time.time()
                    # trace_log = "[{:<7f}] {} TX CanBusMsg: [0x{:0>3X}] [{}]  {}".format(
                    #     time_stamp, self.bus_name, msg_id, length, data_print
                    # )
                    # logger.info(trace_log)

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

    def rx_update(self, msg):
        # update self.pdu_dict
        # while self.rx_exit_flag is False:
        # msg = self.bus.recv(timeout=1)
        if msg:
            # self.listener.on_message_received(msg)
            id = msg.arbitration_id

            # Pcan 时间戳
            time_stamp = msg.timestamp
            # 上位机时间戳
            # time_stamp = time.time()

            length = msg.dlc
            data = list(msg.data)
            # if update_ipdu:
            for message in self.pdu_dict:
                msg_obj = self.pdu_dict[message]
                if msg_obj["rx_flag"] is not None:
                    if id == msg_obj["msg_id"]:
                        msg_obj["pdu_data"] = data
                        msg_obj["time_stamp"] = time_stamp
                        msg_obj["rx_flag"] = True
                # msg = [(id, time_stamp, length, data)]
            # return msg

    # def rx_update_ipdu(self):

    #     while self.rx_exit_flag is False:
    #         self.rx_update()
    #         # sleep(0.0001)
    #     sleep(0.1)

    # def rx_update_ipdu_start(self):
    #     thread = threading.Thread(target=self.rx_update_ipdu, name="SocketCan rx_update_ipdu", daemon=True,)
    #     thread.start()
    def start_log(self):
        self.listener_asc = can.Logger(f"{self.bus_name}.asc")
        self.notifier.add_listener(self.listener_asc)

    def stop_log(self):
        self.notifier.remove_listener(self.listener_asc)
        self.listener_asc.stop()

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
            pass

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
            # self.listener.stop()
            # self.bus.shutdown()
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


if __name__ == '__main__':
    pass
