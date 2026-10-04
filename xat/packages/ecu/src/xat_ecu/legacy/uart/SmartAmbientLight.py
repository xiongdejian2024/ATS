#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**********************
@File    : SmartAmbientLight.py

**********************

------------------------------------------------------------------
@Time    : 2024/10/15 16:00
@Author  : jiewen.deng
Language: Python 3.9
------------------------------------------------------------------
Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.
"""
import json
import re
import os
import time
import copy
from threading import Thread
from collections import defaultdict

from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.uart.uart_data import *
from xat_ecu.legacy.protocol.ProtocolParser import *
from xat_ecu.legacy.uart.SerialOperate import SerialOperate


class SmartAmbientLight(object):

    def __init__(self, ch_port_map: dict):
        """
        :param ch_port_map: {"ch_1": "/dev/ttyUSB1", "ch_2": "/dev/ttyUSB2"}
        """
        self.ch_port_map = ch_port_map
        self.ser_list = []
        json_path = os.path.join(os.path.dirname(__file__), "smart_map_data.json")
        with open(json_path, "r") as data:
            self.smart_map_json_data = json.load(data)

    def stop_uart(self):
        for ser in self.ser_list:
            ser[0].stop_receive_data()

    def start_uart_receive(self):
        for k, port in self.ch_port_map.items():
            ser = SerialOperate(port)
            ser.open_serial()
            ser.start_save_serial_data()
            ser.start_receive_data()
            self.ser_list.append([ser, k])

    def filter_effective_data(self, data_list, map_light_data):
        """
        return: {
                    "8_R": [240, 240, 240],
                    "8_G": [190, 190, 190],
                    "8_B": [20, 20, 20],
                    "8_L": [22, 22, 22],

                    "9_R": [240, 240, 240],
                    "9_G": [190, 190, 190],
                    "9_B": [20, 20, 20],
                    "9_L": [22, 22, 22],

                    "11_R": [240, 240, 240],
                    "11_G": [190, 190, 190],
                    "11_B": [20, 20, 20],
                    "11_L": [22, 22, 22],

                    "33_R": [240, 240, 240],
                    "33_G": [190, 190, 190],
                    "33_B": [20, 20, 20],
                    "33_L": [22, 22, 22],
                }
        """
        map_dict = {}
        for k, info in map_light_data.items():
            for z, x in info.items():
                map_dict[k + "_" + z.split("_")[-1]] = x

        eff_data = defaultdict(list)
        for data in data_list:
            try:
                parse_data = intelligent_parse(data)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/uart/SmartAmbientLight.py")
                logger.warning(f"{data.hex()}\n with:{e}")
                continue
            if not parse_data:
                continue
            effective_flag = False
            try:
                for data_info in parse_data.RunDataInfo:
                    for rgbl_value in data_info.RGBL_INFO:
                        if any([rgbl_value.R_VALUE, rgbl_value.G_VALUE, rgbl_value.B_VALUE, rgbl_value.L_VALUE]):
                            effective_flag = True
                            break
                    if effective_flag:
                        break
                if not effective_flag:
                    continue
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/uart/SmartAmbientLight.py")
                logger.error(f"*******************{data.hex()}\n with:{e}")
                continue

            parse_dict_data = generate_dict_data(parse_data)
            error_data_flag = False
            for info in parse_dict_data["RunDataInfo"]:
                for i, v in enumerate(info["RGBL_INFO"]):
                    if info["Chip_Id"] > 8:
                        error_data_flag = True
                        logger.debug(f"当前错误的原始数据是1：{data.hex()}")
                        break

                    error_data_flag = False
                    pre_value = map_dict.get(str(info["Chip_Id"]) + f"_{i}")
                    if pre_value is None:
                        continue
                    if eff_data.get(f"{pre_value}_R"):
                        eff_data[f"{pre_value}_R"].append(v["R_VALUE"])
                    else:
                        eff_data[f"{pre_value}_R"] = [v["R_VALUE"]]

                    if eff_data.get(f"{pre_value}_G"):
                        eff_data[f"{pre_value}_G"].append(v["G_VALUE"])
                    else:
                        eff_data[f"{pre_value}_G"] = [v["G_VALUE"]]

                    if eff_data.get(f"{pre_value}_B"):
                        eff_data[f"{pre_value}_B"].append(v["B_VALUE"])
                    else:
                        eff_data[f"{pre_value}_B"] = [v["B_VALUE"]]

                    if eff_data.get(f"{pre_value}_L"):
                        eff_data[f"{pre_value}_L"].append(v["L_VALUE"])
                    else:
                        eff_data[f"{pre_value}_L"] = [v["L_VALUE"]]
                if error_data_flag:
                    break
        return eff_data

    def check_smart_ambient_light_data(self,
                                       check_json_path,
                                       vehicle_type="marsone",
                                       ignore_light_list=[181]
                                       ):
        """

        :param check_json_path: 校验的文件路径
        :param vehicle_type: 车型：marsone/venus
        :param ignore_light_list: 需要忽略彻查车灯的数据
        :return:
        """
        with open(check_json_path, "r") as data:
            check_json_data = json.load(data)

        check_light_map = {}
        for info in check_json_data.values():
            for index, sg in enumerate(info):
                for single_frame_data in sg:
                    if single_frame_data["id"] == -1:
                        continue
                    if index % 2 == 0:
                        if str(single_frame_data["id"]) + "_R" not in check_light_map:
                            check_light_map[str(single_frame_data["id"]) + "_R"] = [single_frame_data["RED"]]
                            check_light_map[str(single_frame_data["id"]) + "_G"] = [single_frame_data["GREEN"]]
                            check_light_map[str(single_frame_data["id"]) + "_B"] = [single_frame_data["BLUE"]]
                            check_light_map[str(single_frame_data["id"]) + "_L"] = [single_frame_data["BRIGHTNESS"]]
                        else:
                            if check_light_map[str(single_frame_data["id"]) + "_R"][-1] != single_frame_data["RED"]:
                                check_light_map[str(single_frame_data["id"]) + "_R"].append(single_frame_data["RED"])
                            if check_light_map[str(single_frame_data["id"]) + "_G"][-1] != single_frame_data["GREEN"]:
                                check_light_map[str(single_frame_data["id"]) + "_G"].append(single_frame_data["GREEN"])
                            if check_light_map[str(single_frame_data["id"]) + "_B"][-1] != single_frame_data["BLUE"]:
                                check_light_map[str(single_frame_data["id"]) + "_B"].append(single_frame_data["BLUE"])
                            if check_light_map[str(single_frame_data["id"]) + "_L"][-1] != single_frame_data["BRIGHTNESS"]:
                                check_light_map[str(single_frame_data["id"]) + "_L"].append(single_frame_data["BRIGHTNESS"])

        logger.info(f"待检查的数据：{check_light_map}")
        ch_data = self.smart_map_json_data[vehicle_type]
        for ser in self.ser_list:
            current_data = copy.deepcopy(UartData.RUN_DATA[ser[0]])
            result = self.filter_effective_data(current_data, ch_data[ser[1]])
            logger.info(f"实际的数据：{result}")

            for k, v in result.items():
                ignore_flag = False
                for i in ignore_light_list:
                    if str(k).startswith(str(i)):
                        ignore_flag = True
                        break
                if ignore_flag:
                    continue
                for data in check_light_map.get(k):
                    if data not in v:
                        logger.error(f"{k}：期望的{data}在实际接收的数据中没有发现。")
                        assert False
                    logger.debug(f"{k}：检查到：{data} 已经接收到")

    def clear_story_data(self):
        for ser in self.ser_list:
            UartData.RUN_DATA[ser[0]].clear()
