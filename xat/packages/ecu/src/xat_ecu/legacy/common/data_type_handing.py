# -*- coding: utf-8 -*-
"""
@File        : common.data_type_handing.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021-12-02 14:59
@Description : data type handing
"""

import sys
import os
from typing import Tuple, Union

from xat_ecu.legacy.common.logger import *
import time
import binascii


def hex_string_to_ascii(hex_string):
    """
    16进制字符串转ascii
    hex_string: "30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30"
    return: 00000000000000000
    """
    hex_list = [int(hex_str, 16) for hex_str in hex_string.split()]
    result_str = ''.join(chr(num) for num in hex_list)
    return result_str


def ascii_to_hex_string(input_str):
    """
    ascii转16进制字符串
    input_str: "00000000000000000"
    return: "30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30"
    """
    ascii_list = [ord(char) for char in input_str]
    hex_string = ' '.join(format(num, '02X') for num in ascii_list)
    return hex_string


# -------  FR  --------------
def slotid_cyclecode_to_msgid(slot_id, cyclecode):
    BaseCycle, CycleRepetition = cyclecode_to_baseCycle(cyclecode)
    msgid = slotid_to_msgid(slot_id, BaseCycle, CycleRepetition)
    return msgid


def slotid_to_msgid(slot_id, BaseCycle, CycleRepetition):
    msgid = (slot_id << 16) + (BaseCycle << 8) + CycleRepetition
    return msgid


def msgid_to_slotid(msgid):
    slot_id = msgid >> 16
    BaseCycle = (msgid >> 8) & 0xFF
    CycleRepetition = msgid & 0xFF
    return slot_id, BaseCycle, CycleRepetition


def cyclecode_to_baseCycle(cyclecode):
    if cyclecode:
        i = 0x7F
        while cyclecode == cyclecode & i:
            i = i >> 1
        BaseCycle = cyclecode & i
        CycleRepetition = i + 1
    else:
        logger.error("Flexray cyclecode is {}    ----- error -----".format(cyclecode))
        BaseCycle = 0
        CycleRepetition = 0
    return BaseCycle, CycleRepetition


def baseCycle_to_cyclecode(BaseCycle, CycleRepetition):
    return BaseCycle + CycleRepetition


# -----------------------------


def str_to_bcd5_ascii3_list(str_data: str):
    # str length is 13
    # bcd5_ascii3 length is 8 bytes
    if len(str_data) == 13:
        s = str_data[:10]
        b = binascii.a2b_hex(s)
        b_list = list(b)
        a_list = list(bytes(str_data[10:13], "ascii"))
        data = b_list + a_list
        return data
    else:
        logger.error("config data error")


def int_to_2_bytes_list(int_data):
    # such as    386 ---->> [0x01, 0x82]
    bytes_list = [int_data >> 8] + [int_data & 0xFF]
    return bytes_list


def int_to_4_bytes_list(int_data):
    # such as    386 ---->> [0x01, 0x82]
    bytes_list = (
            [(int_data >> 24) & 0xFF]
            + [(int_data >> 16) & 0xFF]
            + [(int_data >> 8) & 0xFF]
            + [int_data & 0xFF]
    )
    return bytes_list


class DataTypeHanding:
    @staticmethod
    def intlist_to_int(intlist: list):
        # [0x00, 0x10]   >>>>   16
        byte_data = bytes(intlist)
        int_data = int.from_bytes(byte_data, byteorder="big", signed=False)
        return int_data

    # @staticmethod
    # def intlist_to_str(intlist: list):
    #     # [0x30, 0x30]   >>>>   '00'
    #     i_str = ""
    #     for i in intlist:
    #         i = chr(i)
    #         i_str += i
    #     return i_str

    @staticmethod
    def int_to_int2list(intdata: int):
        # 0x1001    >>>>    [0x10, 0x01]
        data1 = intdata & 0xFF
        data2 = (intdata >> 8) & 0xFF
        int2list = [data2, data1]
        return int2list

    @staticmethod
    def intlist_to_hexstr(intlist: Union[list, bytes, bytearray]):
        # [0xF1, 0x10]   >>>>    "f110"
        byte_data = bytes(intlist)
        hexstr = byte_data.hex()
        return hexstr

    @staticmethod
    def intlist_to_hexstr_capitalize_and_spaces(intlist: list):
        # [0xF1, 0x10]   >>>>    "F1 10"
        hexstr = DataTypeHanding.intlist_to_hexstr(intlist)
        hexstr_capitalize = hexstr.upper()
        hexstr_capitalize_and_spaces = DataTypeHanding.addstr_into_rawstr(
            hexstr_capitalize, " ", 2
        )
        return hexstr_capitalize_and_spaces

    @staticmethod
    def intlist_to_hexliststr(intlist: list):
        # [34, 241, 158]   >>>>    "[0x22, 0xF1, 0x9E]"
        hexlist = []
        for int_data in intlist:
            hex_data = hex(int_data)
            hexlist.append(hex_data)
        hexliststr = str(hexlist)
        hexliststr = hexliststr.replace("'", '')
        return hexliststr

    @staticmethod
    def addstr_into_rawstr(rawstr: str, addstr: str, length: int):
        # such as   "F110"  " "  1 >>>>    "F1 10"
        rawlist = list(rawstr)
        rawlist_Roundinglen = len(rawlist) // length
        count = 0
        for i in range(rawlist_Roundinglen):
            rawlist.insert((1 + i) * length + count, addstr)
            count += 1
        get_str = "".join(rawlist)
        return get_str

    @staticmethod
    def int_list_to_time(data_int_list):
        if data_int_list[3] >= 16:
            data_int_list[3] -= 16
            data_int_list[2] += 1
        else:
            data_int_list[3] += 8
        time_str = "20%s-%s-%s %s:%s:%s" % (
            data_int_list[0],
            data_int_list[1],
            data_int_list[2],
            data_int_list[3],
            data_int_list[4],
            data_int_list[5],
        )
        time_s = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        time_int = int(time.mktime(time_s))
        return time_int

    @staticmethod
    def get_dtc_list_by_dtc_standard_code(dtc_standard_code):
        int_list = []
        first_c = dtc_standard_code[0]
        first_int = int(dtc_standard_code[1], 16)
        if first_c == "P":
            first_int += 0
        elif first_c == "C":
            first_int += 1 * 4
        elif first_c == "B":
            first_int += 2 * 4
        elif first_c == "U":
            first_int += 3 * 4
        int_list.append(first_int)
        for id in range(2, len(dtc_standard_code)):
            int_list.append(int(dtc_standard_code[id], 16))
        return int_list

    @staticmethod
    def set_dtc_no_by_dtc_standard_code(self, dtc_standard_code):
        """
        @brief : DTC_NO U010087 -> 12648583
        """
        int_list = self.get_dtc_list_by_dtc_standard_code(dtc_standard_code)
        self.dtc_no = self.int_list_to_int(int_list)

    @staticmethod
    def get_int_from_str(data_str, start_byte, length_byte):
        """从十六进制字符串中提取成指定长度数据转成十进制, ('0102030405', 1, 1) --> 2"""
        return int(data_str[start_byte * 2: (start_byte + length_byte) * 2], 16)

    @staticmethod
    def get_signal_from_pdus_by_bit(data_bytes: bytes, start_bit: int, bit_length: int):
        """
        从原始数据中根据起始bit位和长度获取数据
        :param data_bytes: bytes类型的数据
        :param start_bit: 起始bit位
        :param bit_length: 数据bit长度
        :return: int
        """
        bytes_length = len(data_bytes)
        int_data = int.from_bytes(data_bytes, 'big')
        bin_data_str = bin(int_data).replace("0b", "").zfill(bytes_length * 8)
        bin_data_str_r = bin_data_str[::-1]
        return int(bin_data_str_r[start_bit: start_bit + bit_length][::-1], 2)

    @staticmethod
    def hexstr_to_inlist(data_str: str):
        """‘02 10 01’ ---> [0x02, 0x10, 0x01]"""
        data_str = data_str.replace(" ", "")
        res = []
        for i in range(0, len(data_str), 2):
            res.append(int(data_str[i: i + 2], 16))
        return res

    @staticmethod
    def hexstr_to_bytes(data_str: str):
        """十六进制字符串转成bytes格式"""
        return bytes.fromhex(data_str.replace(" ", ""))

    @staticmethod
    def to_bytes(data: Union[bytes, bytearray, str, list]) -> bytes:
        """转换成bytes输出"""
        if isinstance(data, str):
            return DataTypeHanding.hexstr_to_bytes(data)
        elif isinstance(data, bytes):
            return data
        elif isinstance(data, bytearray):
            return bytes(list(data))
        elif isinstance(data, list):
            return bytes(data)
        else:
            raise TypeError("入参类型不支持".format(type(data)))  # todo: 待补充

    @staticmethod
    def to_intlist(data: Union[int], length: Union[None, int] = None) -> list:
        """转换成列表输出"""
        res = []
        if isinstance(data, int):
            while data > 255:
                res.insert(0, data & 0xFF)
                data = data >> 8
            res.insert(0, data)
        if length is None:
            return res
        else:
            if length > len(res):
                res = [0] * (length - len(res)) + res
            else:
                res = res[-length:]
            return res

    @staticmethod
    def to_hexstr(data: Union[bytes, bytearray, str, list]) -> str:
        """转换成十六进制字符串输出(不带空格)"""
        if isinstance(data, str):
            return data.replace(" ", "")
        elif isinstance(data, list) or isinstance(data, bytes) or isinstance(data, bytearray):
            return DataTypeHanding.intlist_to_hexstr(data)
        else:
            raise TypeError("入参类型不支持".format(type(data)))  # todo: 待补充

    @staticmethod
    def to_int(data: Union[bytes, list, int]) -> int:
        """转换成十进制"""
        if isinstance(data, bytes):
            int_data = int.from_bytes(data, byteorder="big", signed=False)
            return int_data
        elif isinstance(data, list):
            return DataTypeHanding.intlist_to_int(data)
        elif isinstance(data, int):
            return data

    @staticmethod
    def is_chinese(data):
        """判断是否是中文"""
        for ch in data:
            if '\u4e00' <= ch <= '\u9fff':
                return True
            else:
                pass
        return False

    @staticmethod
    def is_English_no_spcae(data):
        """判断是否是英文(去掉空格后)"""
        data = data.replace(" ", "")
        if data.isalpha():
            return True
        else:
            return False


if __name__ == "__main__":
    hexstr = DataTypeHanding.intlist_to_hexstr([0xF1, 0x10])
    logger.warning(hexstr)
    hexstrlist = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(
        [0xF1, 0x10, 0x77]
    )
    logger.warning(hexstrlist)

    # intlist = [246,107,234,82,17,117,65,18,150,228,181,160,12,214,212,101]
    # i_str = DataTypeHanding.intlist_to_str(intlist)
    # print(i_str)
    a = DataTypeHanding.hexstr_to_inlist('0040FFFFFFFFFFFF')
    print(a)
