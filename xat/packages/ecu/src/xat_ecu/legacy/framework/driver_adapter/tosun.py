#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :tosun.py
@Time         :2024/12/6 17:27
@Author       :dejian.xiong@jiduauto.com
@Description  :
"""
import glob
import os
import socket
import subprocess
import time
from pathlib import Path

import psutil

from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.framework.driver_adapter.abc_adapter import ABCAdapter
from xat_ecu.legacy.framework.common.global_config import BASE_DIR
from xat_ecu.legacy.framework.exception.error_code import StatusCode
from xat_ecu.legacy.framework.exception import exception_error
from xat_ecu.legacy.framework.exception.exception_error import error_check
from xat_ecu.legacy.framework.exception.error_callback import error_callback

logger.info = print
logger.error = print


class TosunCanAadpter(ABCAdapter):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.callback = None
        self.ini_path = None
        self.logpath = None
        self.tosun_serial = None
        self.host = "127.0.0.1"
        self.port = 8001

    def _init_ini_config(
            self,
            msg_infos_list: list = [],
            tosun_serial: str = '',
            file_path: str = "./config1.ini",
            port=8001,
            is_save_log=1
    ):
        with open(file_path, "w") as f:
            f.write("[config]")
            f.write("\n")

            f.write("E2EConfig = 1")
            f.write("\n")

            f.write(f"SaveLog = {is_save_log}")
            f.write("\n")

            f.write(f"DeviceSerial = {tosun_serial}")
            f.write("\n")
            f.write("E2ECRCDLL = ./E2ECRCDLL.dll")
            f.write("\n")
            f.write("CRCFunc = crc8_calc")
            f.write("\n")
            f.write("FlexRaySRCIP = 127.0.0.1")
            f.write("\n")
            f.write(f"FlexRaySRCPORT = {port - 1}")
            f.write("\n")
            f.write("FlexRayDSTIP = 127.0.0.1")
            f.write("\n")
            f.write(f"FlexRayDSTPORT = {port}")
            f.write("\n")

            if port == 8003:
                f.write(f"Chn_AIntervalCnt = 0,0,0,0,0,0,0,0,0,0,0,0\n")  # 设置帧间距   单位us
                f.write("\n")

            for msg_infos in msg_infos_list:
                for msg_info in msg_infos:
                    for msginfo in msg_info:
                        if isinstance(msginfo, str):
                            f.write(msginfo)
                            f.write("\n")
                        else:
                            if msginfo:
                                for sig_info in msginfo:
                                    f.write(sig_info)
                                    f.write("\n")
                f.write("\n")

    def _connect_tosun_by_udp(self):
        with error_check(StatusCode.TOSUN_MINI_PROGRAM_CONNECT_ERR, exception_error.TosunError, error_callback):
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 启用端口复用
            self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.client_socket.bind((self.host, self.port))

    def _init_IniMap(self):
        logger.info(" =========  tosun inimap start ==============")
        cmd = f"cd {Path(BASE_DIR) / f'sdk/driver/tosun/libTSCANAPI/linux/;./IniMap {self.ini_path} {self.logpath}'}"
        logger.info(cmd)

        self.p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True,
                                  preexec_fn=os.setsid, text=True)

        start_time = time.time()
        while time.time() - start_time < 2:
            # 检查命令的状态
            if self.p.poll() is None:
                # 执行其他操作，或者等待一段时间
                time.sleep(0.5)
            else:
                break
        time.sleep(0.5)
        if not self.p.returncode:
            logger.info(f"=======================  Tosun {self.tosun_serial} start success ======================")
        else:
            with error_check(StatusCode.TOSUN_MINI_PROGRAM_START_ERR, exception_error.TosunError, error_callback):
                self.p.terminate()
                stdout = self.p.stdout.read()
                stderr = self.p.stderr.read()
                err_msg = f"同星{self.tosun_serial}初始化失败"
                if stdout:
                    err_msg += f"stdout:{stdout}"
                if stderr:
                    err_msg += f"stderr:{stderr}"
                logger.error(err_msg)
                raise

    def _stop_client(self):
        if hasattr(self, 'client_socket') and self.client_socket:
            self.client_socket.close()

    def set_callback(self, callback):
        self.callback = callback

    def start(self):
        self._init_ini_config()
        self._init_IniMap()
        self._connect_tosun_by_udp()

    def stop(self, clear_ini_map=True):
        self._stop_client()
        if self.p:
            try:
                parent_proc = psutil.Process(self.p.pid)
                for child_proc in parent_proc.children(recursive=True):
                    child_proc.kill()
                parent_proc.kill()

                if clear_ini_map:
                    # 使用glob模块查找所有以'config'开头、'.ini'结尾的文件
                    for file in glob.glob('config*.ini'):
                        try:
                            os.remove(file)
                            logger.info(f"Removed INI file: {file}")
                        except OSError as e:
                            logger.warning(f"Failed to remove INI file {file}: {e}")

            except (OSError, subprocess.TimeoutExpired) as e:
                logger.warning("Error stopping Tosun IniMap: {}".format(e))
            except Exception as e:
                logger.exception(f"停止同星IniMap出现异常：原因是{str(e)}")
        else:
            logger.info("IniMap is not running, no need to stop.")

    def send(self, msg):
        self.client_socket.send(msg)
        self.callback(msg)

    def recv(self):
        msg = self.client_socket.recv(1024)
        self.callback(msg)


def print_msg(msg):
    print(msg)


if __name__ == '__main__':
    tc = TosunCanAadpter()
    tc.set_callback(print_msg)
    tc.start()
    tc.recv()
    time.sleep(10)
    tc.stop()

