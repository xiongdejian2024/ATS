# -*- coding: utf-8 -*-
"""
@File        : socket_can.py
@Description : The basic interfaces of socket can,
               porting from Alpha2 project
@Examples    :
"""
import can
import json
import time
import inspect
from xat_ecu.legacy.common.logger import logger


class SocketCan:
    """
    Provide interfaces:
      1. send single message
      2. read single message
      3. send cyclic message with modification
         add/remove/pause/resume cyclic msg, modify data
         add_dual_rate_cyclic_msg
    """

    def __init__(self, bus_name, channel, bitrate=500000, dbc_json=None):
        """
        Initialize a SocketCan object.
        :param bus_name: bus name, such as 'body', 'ept'，随意填写
        :param channel: channel interface, such as 'can0', 'can1'
        :param bitrate: bitrate of socket can, default is 500000
        :param dbc_json: dbc_json file which defined cyclic message
        """
        self.bus_name = bus_name    # name of channel, such as 'etp'
        self.channel = channel      # channel name, such as 'can0'
        self.bitrate = bitrate
        self.dbc_json = dbc_json
        can.rc['interface'] = 'socketcan'  # bus type
        can.rc['channel'] = self.channel  # channel
        can.rc['bitrate'] = self.bitrate
        self.bus = can.interface.Bus()
        self.__started = False
        self.msg_task = {}          # Tasks to sending cyclic messages
        if self.dbc_json is None:
            self.msgs = []
        else:
            with open(self.dbc_json) as data:
                self.msgs = json.load(data)

    def start(self):
        """
        Start tasks to transmit each cyclic message read from json file
        :return:
        """
        if self.__started:
            return 
        try:
            if self.msgs:
                for idx, msg in enumerate(self.msgs):
                    msg_foo = msg                       # For debugging.
                    msg_task_foo = self.msg_task        # For debugging.

                    cyclic_msg = can.Message(arbitration_id=msg["Id"],
                                             data=[0] * msg["DLC"], is_extended_id=False)
                    if msg["Id"] in self.msg_task:
                        raise ValueError
                    else:
                        self.msg_task[msg['Id']] = self.bus.send_periodic(
                            cyclic_msg, msg['Cycle'] / 1000)
                    
                    self.__started = True    
        except (AttributeError, OSError) as err:
            error_foo = err                             # For debugging.
            logger.error("SocketCan run task error: {}".format(self.bus_name))
            logger.error(err)

    def add_cyclic_msg(self, can_id, dlc, cyclic_rate):
        """
        Add cyclic message to bus
        :param can_id: can message id
        :param dlc: Data length of new cyclic message to add
        :param cyclic_rate: Cycle rate of new cyclic message (in seconds)
        :return:
        """
        try:
            cyclic_msg = can.Message(arbitration_id=can_id,
                                     data=[0] * dlc, is_extended_id=False)
            if can_id in self.msg_task:
                logger.info(
                    "{}(): can_id({:#x}) already being published.".format(inspect.stack()[0].function, can_id))
            else:
                self.msg_task[can_id] = self.bus.send_periodic(cyclic_msg, cyclic_rate)
        except (AttributeError, OSError) as e:
            logger.error('SocketCan add cyclic msg error: \
                {} on {}'.format(hex(can_id), self.channel))
            logger.error(e)
        except KeyError:
            logger.error('SocketCan add cyclic msg error: \
                {} already exists on {}'.format(hex(can_id), self.bus_name))

    def add_cyclic_msg_with_data(self, can_id, data, cyclic_rate):
        """
        Add cyclic message with specific data to bus
        :param can_id: can message id
        :param data: data of can cyclic message
        :param cyclic_rate: Cycle rate of new cyclic message (in seconds)
        :return:
        """
        try:
            cyclic_msg = can.Message(arbitration_id=can_id, data=data,
                                     is_extended_id=False)
            if can_id in self.msg_task:
                raise ValueError
            else:
                self.msg_task[can_id] = self.bus.send_periodic(cyclic_msg, cyclic_rate)
        except (AttributeError, OSError) as e:
            logger.error('SocketCan add cyclic msg error: \
                {} on {}'.format(hex(can_id), self.channel))
            logger.error(e)
        except KeyError:
            logger.error('SocketCan add cyclic msg error: \
                {} already exists on {}'.format(hex(can_id), self.channel))

    # Failed
    def add_dual_rate_cyclic_msg(self, can_id, dlc, count_rate1,
                                 cyclic_rate1, cyclic_rate2):
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
            cyclic_msg = can.Message(arbitration_id=can_id, data=[0] * dlc,
                                     is_extended_id=False)
            if can_id in self.msg_task:
                raise ValueError
            else:
                # self, channel, message, count, initial_period, subsequent_period
                self.msg_task[can_id] = can.interface.MultiRateCyclicSendTask(
                    channel=self.channel, message=cyclic_msg, count=count_rate1,
                    initial_period=cyclic_rate1, subsequent_period=cyclic_rate2)
        except (AttributeError, OSError) as e:
            logger.error('SocketCan add dual rate cyclic msg error: \
                {} on {}'.format(hex(can_id), self.bus_name))
            logger.error(e)
        except KeyError:
            logger.error(
                'SocketCan add dual rate cyclic msg error: \
                    {} already exists on {}'.format(hex(can_id), self.bus_name))

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
        except (AttributeError, OSError) as e:
            logger.error('SocketCan remove cyclic msg error: \
                {} on {}'.format(hex(can_id), self.bus_name))
            logger.error(e)
        except KeyError:
            logger.error('SocketCan remove cyclic msg error: \
                {} not found on {}'.format(hex(can_id), self.bus_name))
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
            logger.error('SocketCan pause cyclic msg error: \
                {} on {}'.format(hex(can_id), self.bus_name))
            logger.error(e)
        except KeyError:
            logger.error('SocketCan pause cyclic msg error: \
                {} not found on {}'.format(hex(can_id), self.bus_name))

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
            logger.error('SocketCan resume cyclic msg error: \
                {} on {}'.format(hex(can_id), self.bus_name))
            logger.error(e)
        except KeyError:
            logger.error('SocketCan resume cyclic msg error: \
                {} not found on {}'.format(hex(can_id), self.bus_name))

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
            logger.error('CAN modify data error: \
                {} on {}'.format(hex(can_id), self.bus_name))
            logger.error(e)
        except KeyError:
            err_msg = "CAN modify data error: {} not found on {}".format(hex(can_id), self.bus_name)
            hint1 = "Possibly this msg is an output of CGW."
            hint2 = "Look for this msg on another bus, where it is an input of CGW."
            logger.error(err_msg)
            logger.error(hint1)
            logger.error(hint2)

    def read_single_msg_from_obj(self, msg_obj, timeout=1.0):
        return self.read_single_msg(msg_obj.msg_id, wait=msg_obj.msg_cyc, timeout=timeout)

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
            interface_bus.set_filters([{"can_id": can_id, "can_mask": 0xffff}])

            msg = None
            start_time = time.time()

            while msg is None or msg.arbitration_id != can_id:
                msg = interface_bus.recv(timeout=timeout)
                elapsed_time = time.time() - start_time

                # timeout if no messages are read after elapsed time
                if elapsed_time > timeout and msg is None:
                    if log_error:
                        logger.error("CAN read timeout: {} not found on {}".format(hex(can_id), self.bus_name))
                    return None
                else:
                    time.sleep(0.001)
            interface_bus.shutdown()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/socket_can.py")
            logger.error("Error: Message {} not on bus {}. {}".format(hex(can_id), self.bus_name, e))
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
            logger.error('CAN write error: \
                {} on {}'.format(hex(can_id), self.bus_name))

    def write_single_msg_with_msg(self, msg):
        try:
            self.bus.send(msg)
        except AttributeError:
            logger.error('CAN write error: \
                {} on {}'.format(hex(msg.frame_id), self.bus_name))

    def stop(self):
        """
        Stop each task that is sending cyclic messages.
        :return:
        """
        try:
            if not self.__started:
                return 
            if len(self.msg_task)>0:
                for can_id, inst in self.msg_task.items():
                    inst.stop()
                del self.msg_task
            self.bus.shutdown()
            self.__started = False
        except AttributeError:
            logger.error('SocketCan stop task error: {}'.format(self.bus_name))


if __name__ == '__main__':
    pass

