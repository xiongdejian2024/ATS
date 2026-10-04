#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**********************
@File    : SerialOperate.py

**********************

------------------------------------------------------------------
@Time    : 2024/9/24 16:00
@Author  : jiewen.deng
Language: Python 3.9
------------------------------------------------------------------
Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.
"""
import re
import time
import serial
from serial import Timeout
from threading import Thread

from xat_ecu.legacy.utils.utils import *
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.uart.uart_data import *


class SerialOperate(object):

    def __init__(self, port='/dev/USB_LIGHT', baudrate=500000):
        self.port = port
        self.baudrate = baudrate
        self.stop_serial = True
        self.need_handle_diag_flag = False
        self.mock_chip_diag_data = {}
        self.diag_full_data = None
        self.interval_time = 0.00047
        self.chip_data_max_count = 10000
        self.send_thread_flag = False
        self.recv_thread_flag = False
        self.save_serial_data = False
        self.match_data = r"(00e0|00a0\d{2}|0080\d{2}|00c0)\s*"
        self.serial = serial.Serial(port, baudrate, timeout=0.1)
        self.serial.write_buffer_size = 0

    def open_serial(self):
        if not self.serial.isOpen():
            logger.warning(f"串口打开失败，请检查设置！")
            raise AssertionError(f"串口打开失败，请检查设置！")
        logger.info(f"{self.port} 串口已打开...")

    def stop_receive_data(self):
        if not self.serial.isOpen():
            self.serial.close()
        self.stop_serial = True
        self.send_thread_flag = False
        self.recv_thread_flag = False
        self.need_handle_diag_flag = False

    def read_serial_data(self, size=None, expect=r"00a0\d{2}", expect_len=3):
        line = bytearray()
        timeout = Timeout(self.serial._timeout)
        while True:
            c = self.serial.read(1)
            if c:
                line += c
                match_data = re.match(expect, line[-expect_len:].hex().lower())
                if match_data:
                    break
                if size is not None and len(line) >= size:
                    break
            else:
                break
            if timeout.expired():
                break
        return bytes(line)

    def start_receive_data(self):
        if not self.recv_thread_flag:
            self.stop_serial = False
            self.recv_thread_flag = True
            Thread(target=self._handle_receive_data, daemon=True).start()

    def change_mock_diag_data(self, mock_chip_diag_data, start_mock_flag=True):
        """
        模拟灯带故障诊断
        :param mock_chip_diag_data: {"1": 0x00, "2": 0x01, "3":0x02, "4":0x3, "5":0x04, "6":0x7, "7": 0x0, "8":0x0}
                                key为芯片ID，VALUE为故障值（ 0：无故障；1：SALM1U1LEDSts故障；2：SALM1U1VltSts故障；4：SALM1U1TmpSts故障）
        :param start_mock_flag: 开始模拟诊断回复，默认改变完数据后需要模拟回复
        """
        if not isinstance(mock_chip_diag_data, dict):
            raise AssertionError(f"mock数据必须为dict类型。")
        self.mock_chip_diag_data = mock_chip_diag_data
        self.need_handle_diag_flag = start_mock_flag

    def stop_mock_diag_data(self):
        self.need_handle_diag_flag = False

    def handle_serial_data(self, info_data):
        need_list = []
        current_str = ""
        for data in info_data:
            if not data:
                continue
            if data == "00e0":
                current_str = data
            elif data == "00c0":
                current_str = data
            elif len(data) == 6:
                need_list.append(data)
            else:
                if current_str:
                    current_str += data
                    need_list.append(current_str)
                    current_str = ""
        return need_list

    def start_send_data(self):
        if not self.send_thread_flag:
            self.stop_serial = False
            self.send_thread_flag = True
            Thread(target=self._start_send_data, daemon=True).start()

    def _start_send_data(self):
        while not self.stop_serial and self.send_thread_flag:
            if self.need_handle_diag_flag:
                if self.diag_full_data:
                    self.serial.write(self.diag_full_data)
                time.sleep(self.interval_time)
            else:
                time.sleep(1)

    def start_save_serial_data(self):
        self.save_serial_data = True

    def _handle_receive_data(self):
        current_count_index = 0
        while not self.stop_serial and self.recv_thread_flag:
            if self.need_handle_diag_flag:
                data_received = self.read_serial_data(size=1110)
                if data_received:
                    try:
                        if data_received[-2] != 0xa0:
                            if current_count_index == 8:
                                current_count_index = 1
                            else:
                                current_count_index += 1
                            mock_data = self.mock_chip_diag_data.get(str(current_count_index))
                        else:
                            if data_received[-1] == 0 or data_received[-1] > 8:
                                logger.info(f"accept error data:{data_received.hex()}")
                                continue
                            if data_received[-1] == 8:
                                current_count_index = 1
                                mock_data = self.mock_chip_diag_data.get(str(current_count_index))
                            else:
                                current_count_index = data_received[-1] + 1
                                mock_data = self.mock_chip_diag_data.get(str(current_count_index))

                        if mock_data is not None:
                            mock_bytes_data = format(mock_data, '02X')
                            chip_id_tmp = bytes.fromhex(format(current_count_index, '02X'))
                            cul_data = data_received[-3: -1] + chip_id_tmp + bytes.fromhex(mock_bytes_data)
                            crc1 = format(get_crc1_data(cul_data), '02X')
                            crc2 = format(get_crc2_data(cul_data), '02X')
                            self.diag_full_data = bytes.fromhex(mock_bytes_data + crc1 + crc2)
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/uart/SerialOperate.py")
                        logger.warning(f"接收数据错误,原始数据：{data_received.hex()}")
                        continue
            else:
                if self.save_serial_data:
                    data_received = self.read_serial_data(size=800)
                    if self not in UartData.RUN_DATA:
                        UartData.RUN_DATA[self] = deque([data_received], maxlen=self.chip_data_max_count)
                    else:
                        UartData.RUN_DATA[self].append(data_received)

                # temp = re.split(self.match_data, data_received.hex(), flags=re.I)
                # if temp:
                #     need_list = self.handle_serial_data(temp)
                #     if self.need_handle_diag_flag:
                #         for single_data in need_list:
                #             if single_data.startswith('00a0'):
                #                 logger.info(f"串口接收:{single_data}")
                #                 diag_obj = intelligent_parse(bytes.fromhex(single_data))
                #                 mock_data = self.diag_data.get(str(diag_obj.Chip_Id))
                #                 if mock_data:
                #                     single_data = single_data + format(mock_data, '02X')
                #                     crc1 = get_crc1_data(bytes.fromhex(single_data))
                #                     crc2 = get_crc2_data(bytes.fromhex(single_data))
                #                     send_data = bytes.fromhex(format(mock_data, '02X') +
                #                                               format(crc1, '02X') +
                #                                               format(crc2, '02X'))
                #                     self.serial.write(send_data)
                #                     logger.info(f"串口发送:{send_data.hex()}")
