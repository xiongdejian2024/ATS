from libTSCANAPI import *

import socket
import struct
import time
from time import sleep

import subprocess
from subprocess import Popen
import os
import signal


if __name__=="__main__":



    i = 0
    j = 100  # 测试次数
    while i < j:
        print(f"=================第{i+1}次测试开始======================")
        inimap = "/root/quansun/ecu-simulator/xat_ecu/legacy/sdk/driver/tosun/libTSCANAPI/linux/IniMap"
        ini_path = "/root/quansun/ecu-simulator/xat_ecu/legacy/sdk/driver/tosun/libTSCANAPI/linux/can3.ini"
        logpath = "/root/quansun/ecu-simulator/xat_ecu/legacy/sdk/driver/tosun/libTSCANAPI/linux/logcan.asc"

        inimap = "/root/quansun/ecu-simulator/xat_ecu/legacy/sdk/driver/tosun/libTSCANAPI/linux/IniMap"
        fr_ini_path = "/root/quansun/ecu-simulator/xat_ecu/legacy/sdk/driver/tosun/libTSCANAPI/linux/fr3.ini"
        fr_logpath = "/root/quansun/ecu-simulator/xat_ecu/legacy/sdk/driver/tosun/libTSCANAPI/linux/logfr.asc"

        cmd = f"{inimap} {ini_path} {logpath}"
        p = Popen(cmd, shell=True, close_fds=True, preexec_fn=os.setsid)

        cmd_fr = f"{inimap} {fr_ini_path} {fr_logpath}"
        p_fr = Popen(cmd_fr, shell=True, close_fds=True, preexec_fn=os.setsid)
        
        print("打开同星")

        sleep(2)
        pid = p.pid
        pid_fr = p_fr.pid

        p.terminate()
        p.wait()
        os.killpg(pid, signal.SIGKILL)

        p_fr.terminate()
        p_fr.wait()
        os.killpg(pid_fr, signal.SIGKILL)

        print("关闭同星")
        sleep(3)
        i += 1

        print(f"=================第{i}次测试结束======================\n")
        sleep(1)

