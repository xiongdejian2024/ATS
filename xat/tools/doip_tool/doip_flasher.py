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


class DoIPFlasher(DOIP):

    def __init__(self, file, key_info):
        self.logger = MyLogger("DoIPFlasher")
        loggerfile = os.path.join(os.path.dirname(__file__), "log", f"log_flasher_{time.strftime('%Y%m%d%H%M%S')}.log")
        log_level = "DEBUG"  # "CRITICAL", "FATAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"
        self.logger.start_logging(log_level, loggerfile)

        auto_reconnect_tcp = True   # tcp 是否自动重连
        super(DoIPFlasher, self).__init__(self.logger.logger, auto_reconnect_tcp)
        self.key_info = key_info
        self.vbf = VBFParser(file)
        # logical
        self.logger.info("connect target ecu")
        self.conn_logical()
        # function
        self.logger.info("connect other ecu for functional addressing")
        self.conn_function()
        self.cycle_tester_present_flag = True  # 默认发送3e 80
        time.sleep(0.05)
        threading.Thread(target=self.cycle_tester_present).start()

    def flash(self):
        """
        诊断刷写流程
        @return:
        """
        try:
            # Functional addressing, Check Program Pre-Condition
            self.logger.info("Functional addressing, Check Program Pre-Condition")
            self.routing_control(0x0206, 1, func_addr=True)

            # Functional addressing, Enter Program Mode
            self.logger.info("Functional addressing, Enter Program Mode")
            self.session_control(2, enable_resp=True, func_addr=True)

            # Confirm Program Mode
            self.logger.info("Confirm Program Mode")
            self.session_control(2)

            # Diagnostic Session Check
            self.logger.info("Diagnostic Session Check: ReadDataByIdentifier 0xF186")
            self.read_data_by_identifier(0xF186)

            # Information Check
            self.logger.info("Information Check: ReadDataByIdentifier 0xED20")
            self.read_data_by_identifier(0xED20)

            # Unlock for Download
            self.logger.info("Unlock Precessing")
            self.unlock_process(1)

            # Erase Memory
            self.logger.info(f"Erase Memory: 3101FF00")
            self.routing_control(0xFF00, 1)

            # Request Download
            self.logger.info("Request Download")
            self.request_download()

            # Transfer Data
            self.logger.info("Transfer Data")
            asyncio.run(self.async_transfer_data())

            # Request Transfer Exit
            self.logger.info("Request Transfer Exit")
            self.request_transfer_exit()

            # Verify Authenticity
            self.logger.info("Verify Authenticity: 31010208")
            self.routing_control(0x0208, 1, self.key_info.encode("utf-8"))
            resp = self.get_routine_payload()
            if resp != "710102081000":
                raise Exception(f"0x0208 response error status: {resp}")

            # # Verify Software Integrity
            self.logger.info("Verify Software Integrity: 31010205")
            self.routing_control(0x0205, 1)

            # Functional addressing, Hardware Reset
            self.logger.info("Functional addressing, Hardware Reset")
            self.ecu_reset(1, enable_resp=True, func_addr=True)
            self.logger.info(f"Flash success!")
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/doip_tool/doip_flasher.py")
            self.logger.info(f"Flash failed with error info: {e}")
        finally:
            self.cycle_tester_present_flag = False

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
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/doip_tool/doip_flasher.py")
                print(f"Tester present response exception {e}")
            time.sleep(3)

    async def async_transfer_data(self):
        index_total = 1
        index = 1
        transfer_flag = True
        async for block in self.vbf.read_all_block():
            for i in range(1, 4):
                try:
                    self.transfer_data(sequence_number=index, data=block)
                    transfer_flag = True
                    self.logger.debug(f"第{index_total}次传包，包长度{len(block)}，传输成功")
                    break
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/doip_tool/doip_flasher.py")
                    self.logger.debug(f"transfer data failed with error {e}")
                    self.logger.debug(f"第{index_total}次传包，包长度{len(block)}，第{i}次传输失败")
                    transfer_flag = False
            if not transfer_flag:
                raise Exception(f"第{index_total}次传包失败")
            else:
                index = index + 1 if index < 255 else 0
                index_total += 1


if __name__ == '__main__':
    key_info = __import__("os").environ['XAT_CREDENTIAL_SCAN_E8146FF8408C2F6B4C3B']
    flasher = DoIPFlasher(r'C:\VBF\6160110050ZAF.VBF', key_info)
    flasher.flash()
