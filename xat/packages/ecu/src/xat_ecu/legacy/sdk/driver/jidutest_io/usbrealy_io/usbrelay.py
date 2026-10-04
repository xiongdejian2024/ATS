# -*- coding: utf-8 -*-
import os
import re
import serial
import time
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.sdk_tools import exec_shell
from typing import Tuple, Union


class USBrelay(object):

    def __init__(self, conifg):
        self.tb_cfg = conifg
        self.io_signal_dict = conifg.get('signal')
        self.usbrelay_map = self.tb_cfg.get("usbrelay")
        self.usbrelay_name = self.get_usbrelay_name()

    def get_usbrelay_name(self):
        '''
        获取继电器名字 前缀
        @return:
        '''
        try:
            results = exec_shell("usbrelay")
            results_str = results["output"]
            result = re.search(r"(\w*)_1=", results_str)
            if result:
                usbrelay_name = result.group(1)
            else:
                usbrelay_name = None
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/jidutest_io/usbrealy_io/usbrelay.py")
            logger.warning(f"获取继电器名字出错，可能出现了乱码，Error：{e}")
            usbrelay_name = ""
        return usbrelay_name

    def usbrelay_cmd(self, num: Union[int, str], on_off: int):
        # on_off:    0 ---- on        1 ---- off
        if self.usbrelay_name or self.usbrelay_name == "":
            if isinstance(num, int):
                usbrelay_cmd = "usbrelay {}_{}={}".format(self.usbrelay_name, num, on_off)
            elif isinstance(num, str):
                usbrelay_cmd = "usbrelay {}={}".format(num, on_off)
            res = exec_shell(usbrelay_cmd)["error"]
            if res == "":
                logger.info("usbrelay cmd success")
            else:
                logger.error("usbrelay cmd res is {}, ----- run failed".format(res))
        else:
            logger.error("No usbrelay is found, and the cmd does not run")

    def usbrelay_cmd_close(self, ur):
        usbrelay_port = None
        if self.usbrelay_map:
            usbrelay_port = self.usbrelay_map.get(ur)
        if usbrelay_port:
            self.usbrelay_cmd(usbrelay_port, 0)
            logger.info("==============  usbrelay_cmd: {} Power on   =============================".format(ur))

    def usbrelay_cmd_open(self, ur):
        usbrelay_port = None
        if self.usbrelay_map:
            usbrelay_port = self.usbrelay_map.get(ur)
        if usbrelay_port:
            self.usbrelay_cmd(usbrelay_port, 1)
            logger.info("==============  usbrelay_cmd: {} Power off   =============================".format(ur))

    def set_do_level(self, io_signal: str, value):
        '''
        默认是断开的
        @param io_signal:
        @param value:
        @return:
        '''
        io_info = self.io_signal_dict.get(io_signal, None)

        channel = io_info.get("channel", None)
        assert channel

        if value:
            usbrelay_cmd = "usbrelay {}={}".format(channel, 1)
        else:
            usbrelay_cmd = "usbrelay {}={}".format(channel, 0)
        res = exec_shell(usbrelay_cmd)["error"]
        if res == "":
            logger.info(f"cmd =={usbrelay_cmd} exc success")
        else:
            logger.error(f"cmd =={usbrelay_cmd} exc failed {res}")
        return 1

    
    def close(self):
        # 统一接口   不可以删除
        pass