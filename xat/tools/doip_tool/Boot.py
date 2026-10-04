# -*- coding: utf-8 -*-
import asyncio
import os
import sys
import threading

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "thirdpartylib"))

from utils.doip import DOIP
from vbfparser.vbfparser import *
from log.logger import MyLogger
import time


class Boot(DOIP):

    def __init__(self):
        self.logger = MyLogger("Boot")
        loggerfile = os.path.join(os.path.dirname(__file__), "log", f"log_Boot_{time.strftime('%Y%m%d%H%M%S')}.log")
        log_level = "DEBUG"  # "CRITICAL", "FATAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"
        self.logger.start_logging(log_level, loggerfile)

        auto_reconnect_tcp = True   # tcp 是否自动重连
        super(Boot, self).__init__(self.logger.logger, auto_reconnect_tcp)

        # logical
        self.logger.info("connect target ecu")
        self.conn_logical()
        # function
        self.logger.info("connect other ecu for functional addressing")
        self.conn_function()
        self.cycle_tester_present_flag = True  # 默认发送3e 80
        time.sleep(0.05)
        #threading.Thread(target=self.cycle_tester_present).start()

    def enter_boot(self):
        """
        BOOT进入
        @return:
        """
        while 1:
            self.read_data_by_identifier(0XF186)
            pl = self.get_read_did_payload()
            if pl == "62f18602":
                #self.cycle_tester_present_flag = False
                break
            else :
                self.session_control(2, enable_resp=True, func_addr=True)
                time.sleep(15)
                self.conn_logical()
                time.sleep(3)

    def cycle_tester_present(self, func_addr=True):
        """
        Functional addressing, Tester present
        @param func_addr: True: Functional addressing; False: Logical addressing
        @return:
        """
        while self.cycle_tester_present_flag:
            try:
                self.tester_present(enable_resp=True, func_addr=func_addr)
            except TimeoutError:
                print("Tester present response timeout error")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/doip_tool/Boot.py")
                print(f"Tester present response exception {e}")
            time.sleep(3)

if __name__ == '__main__':
    flasher = Boot()
    flasher.enter_boot()
