"""
@File        : signal2service_Combination_and_send_pdu.py
@Author      : quan.sun@jiduauto.com
@Time        : 2022/04/04 19:12
@Description :
@Examples    :
"""

'''
全局时钟:
    年(1byte)
    月(1byte)
    日(1byte)
    分(1byte)
    秒(1byte)
		
repeat
	总线编号(1byte??)
	报文ID(
		LIN(1byte)
		CAN/CANFD (2byte)
		FlexRay(4byte))
	毫秒时间戳(2byte)
	报文长度(1byte)
	原始报文数据
	
结束符:
0xFE
'''

import os
import sys
import argparse
from collections import deque


current_path = os.path.dirname(os.path.realpath(__file__))
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.file_handle import FileHandle
from xat_ecu.legacy.common.time_handle import *
from xat_ecu.legacy.sdk.s2spdu.PDU_Const import *
from xat_ecu.legacy.common.data_type_handing import *
import threading
from threading import Thread
from xat_ecu.legacy.sdk.driver.udp_socket import UdpSocketClient
PDU_SEND_DATA_LIST_LEN = 10000


class S2sCombinationSendPdu:
    def __init__(self, bus_pdu_dict,address=("127.0.0.1", 30502)):
        if isinstance(bus_pdu_dict, ISignalIPdu):
            self.bus_pdu_dict = bus_pdu_dict.bus_pdu_dict
            self.ipdu_instance = bus_pdu_dict
        else:
            self.bus_pdu_dict = bus_pdu_dict
            self.ipdu_instance = None
        del_bus = []
        for bus in self.bus_pdu_dict.keys():
            if not hasattr(BUSID, bus.upper()):
                del_bus.append(bus)
        for bus in del_bus:
            del self.bus_pdu_dict[bus]
        self.pdu_list = deque(maxlen=PDU_SEND_DATA_LIST_LEN)
        self.sendpdu = UdpSocketClient(1, "UDP Socket tx", address=address)
        self.continuous_combinationpdu_flag = None
        self.sendpdu_flag = None
        self.lock = threading.Lock()

    def continuous_combinationpdu_start(self):
        self.continuous_combinationpdu_flag = True
        time_thrading = Thread(target=self.continuous_combinationpdu, name="Continuous_Combinationpdu")
        time_thrading.setDaemon(True)
        time_thrading.start()

    def continuous_combinationpdu_stop(self):
        self.continuous_combinationpdu_flag = False
        sleep(0.1)

    def continuous_combinationpdu(self):
        sleep(1)    # Wait for 1s to update the signals before sending
        global_clock_list, global_time = get_6_list_datetime_and_current_time()
        pdu_date = []
        msg_data_lists = []
        while self.continuous_combinationpdu_flag:
            # if (time.time() - global_time) < 0.01:
            #     global_time, global_clock_list, pdu_date, msg_data_lists = self.combinationpdu(global_time, global_clock_list, pdu_date, msg_data_lists)
            # if (time.time() - global_time) >= 0.01:
            #     if msg_data_lists:
            #         self.lock.acquire()
            #         pdu_date = pdu_date + msg_data_lists + [PDUConst.MSG_END]
            #         self.pdu_list.append(pdu_date)
            #         global_clock_list, global_time = get_6_list_datetime_and_current_time()
            #         pdu_date = []
            #         msg_data_lists = []
            #         self.lock.release()
            # sleep(.001)
            global_time, global_clock_list, pdu_date, msg_data_lists = self.combinationpdu(global_time,
                                                                                           global_clock_list, pdu_date,
                                                                                           msg_data_lists)
            sleep(0.01)

    def combinationpdu(self, global_time, global_clock_list=[], pdu_date=[], msg_data_lists=[]):
        for bus in self.bus_pdu_dict.keys():
            bus_cls_obj = getattr(self.ipdu_instance, bus)
            for message in self.bus_pdu_dict[bus]:
                msg_obj = self.bus_pdu_dict[bus][message]
                # if msg_obj.get("tx_flag"):
                if msg_obj.get("tx_change"):
                    msg_obj["tx_change"] = None  # 还原标志位
                    if pdu_date == []:
                        global_clock_list, global_time = get_6_list_datetime_and_current_time()
                        pdu_date = global_clock_list
                    busid = [getattr(BUSID, bus.upper())]
                    message_id = msg_obj.get("msg_id")

                    # 判断计算count crc

                    msg_cls_obj = getattr(bus_cls_obj, message)
                    if hasattr(msg_cls_obj, "sig_group_dataid_dict"):
                        crc_sig_groups = msg_cls_obj.sig_group_dataid_dict
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

                    if busid[0] > 40:
                        message_id = [message_id]
                    elif busid[0] == 1:
                        message_id = int_to_4_bytes_list(message_id)
                    else:
                        message_id = int_to_2_bytes_list(message_id)
                    # if message_id <= 0x7FF:
                    #     message_id = int_to_2_bytes_list(message_id)
                    # else:
                    #     message_id = int_to_4_bytes_list(message_id)
                    relative_time = int((time.time() - int(global_time))*1000)
                    relative_time = int_to_2_bytes_list(relative_time)
                    message_length = [msg_obj.get("msg_length")]
                    msg_pdu = msg_obj.get("pdu_data")
                    msg_data_list = busid + message_id + relative_time + message_length + msg_pdu

                    if len(msg_data_lists + msg_data_list) < 1393:
                        msg_data_lists += msg_data_list
                    elif len(msg_data_lists + msg_data_list) > 1393:
                        pdu_date = pdu_date + msg_data_lists + [PDUConst.MSG_END]
                        self.lock.acquire()
                        self.pdu_list.append(pdu_date)
                        self.lock.release()
                        global_clock_list, global_time = get_6_list_datetime_and_current_time()
                        pdu_date = []
                        msg_data_lists = msg_data_list
                    elif len(msg_data_lists) == 1393:
                        msg_data_lists += msg_data_list
                        pdu_date = pdu_date + msg_data_lists + [PDUConst.MSG_END]
                        self.lock.acquire()
                        self.pdu_list.append(pdu_date)
                        self.lock.release()
                        global_clock_list, global_time = get_6_list_datetime_and_current_time()
                        pdu_date = []
                        msg_data_lists = []
        return global_time, global_clock_list, pdu_date, msg_data_lists

    def s2ssendpdu_start(self, tar_address=("127.0.0.1", 30502)):
        self.sendpdu_flag = True
        time_thrading = Thread(target=self.s2ssendpdu, name="s2ssendpdu", args=(tar_address,))
        time_thrading.setDaemon(True)
        time_thrading.start()

    def s2ssendpdu(self, tar_address=("127.0.0.1", 30502)):

        # debug  Receive
        # self.sendpdu.setup_data_callback(self.sendpdu.print_rx_data)
        # self.sendpdu.start()

        while self.sendpdu_flag:
            try:
                self.lock.acquire()
                if self.pdu_list:
                    # print(len(self.pdu_list))
                    udp_data = self.pdu_list.popleft()   # 需要去取第一个 to do
                    self.lock.release()
                    self.sendpdu.send(udp_data, tar_address)
                    # print("www")
                else:
                    self.lock.release()
                    sleep(0.01)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/s2spdu/signal2service_combination_and_send_pdu.py")
                logger.warning(e)
                self.lock.release()

    def s2ssendpdu_stop(self):
        self.sendpdu.close()
        self.sendpdu_flag = False



if __name__ == "__main__":
    # Work Path: sat/

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--cls_path', choices=("Default"), help='can lin fr cls_path', default=" ecu_simulator/sdk/data/can_lin_fr_cls/v_0_5_5")
    # Default is All
    args = argparser.parse_args()

    ipdu = ISignalIPdu(args.cls_path)
    s2scombinationpdu = S2sCombinationSendPdu(ipdu.bus_pdu_dict)
    s2scombinationpdu.s2ssendpdu_start()
    s2scombinationpdu.sendpdu.send([0x02,0x02^0xFF,0x80,0x01,0x00,0x00,0x00,0x06,0x0E,0x80,0x00,0x05,0x10,0x01],("127.0.0.1", 30502))
    sleep(30)

    s2scombinationpdu.s2ssendpdu_stop

