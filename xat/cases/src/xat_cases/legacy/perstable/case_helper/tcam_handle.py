import os
import threading
import re
import time
from threading import Thread

from xat_cases.legacy.perstable.case_helper.Adb import ADB
from xat_cases.legacy.perstable.case_helper.constant import testParameter
from xat_cases.legacy.perstable.case_helper.remote_vehicle import *
from xat_ecu.legacy.common.logger import logger


class TcamLogCollect:
    def __init__(self, **kwargs):
        self.cmd_process = None
        self.tcam_device_id = testParameter.get("tcam_device_id")
        self.tcam_pwd = testParameter.get("tcam_pwd")
        self.subprocess_run(cmd=f'adb -s {self.tcam_device_id} shell root', cmd_input=self.tcam_pwd)

    def copy_tcam_jetlog(self, tcam_log_path):
        """
        parameter: tcam_log_path, the local lath to save
        copy tcam jetlog if that has not existed in local path
        """
        if not os.path.exists(tcam_log_path):
            os.mkdir(tcam_log_path)
        existed_log_files = os.listdir(tcam_log_path)

        try:
            tcam_logs = self.subprocess_run(cmd=f'adb -s {self.tcam_device_id} shell du -sh /mnt/sdcard/log/jetlog_message*',
                                                cmd_input=self.tcam_pwd)[0].split("\n")

            for line in tcam_logs:
                if '20.0M' in line:
                    file_size, file_name = line.split()
                    file = os.path.basename(file_name)
                    if file.startswith("jetlog_messages") and file.endswith("zst"):
                        if file in existed_log_files:
                            continue
                        logger.info(f"开始拉取{file_name}到{tcam_log_path}...")
                        self.subprocess_run(cmd=f'adb -s {self.tcam_device_id} pull {file_name} {tcam_log_path}', timeout=60)
                        time.sleep(1)
        except Exception as e:
            logger.error("Exception: {} found in line {}".format(e, e.__traceback__.tb_lineno))

    def copy_tcam_coredump(self, tcam_log_path):
        logger.info("开始获取tcam coredump 日志")
        res = False
        out = self.subprocess_run(cmd=f'adb -s {self.tcam_device_id} shell ls -lht /mnt/sdcard/log/coredump',
                                     cmd_input=self.tcam_pwd)[0].split("\n")
        if any([True if str(f).startswith("-rw") else False for f in out]):
            self.subprocess_run(cmd='adb -s {} pull /mnt/sdcard/log/coredump {}'.format(self.tcam_device_id,
                                                                                        tcam_log_path), timeout=600)
            res = True
        return res

    def subprocess_run(self, cmd, cmd_input=None, timeout=60):
        """
        执行 cmd 命令
        """
        try:
            if cmd_input is not None:
                # 创建子进程并执行命令
                logger.info(f'创建subprocess子进程并执行命令:{cmd}&&{cmd_input}')
                self.cmd_process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE, shell=True)
                input_context = '{}\n'.format(cmd_input).encode('utf-8')
                self.cmd_process.stdin.write(input_context)
                stdout, stderr = self.cmd_process.communicate(timeout=timeout)
            else:
                self.cmd_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = self.cmd_process.communicate(timeout=timeout)
        except Exception as e:
            self.cmd_process.terminate()
            logger.error(f'执行命令超时，超时信息：{e}')
            return None, None
        else:
            return stdout.decode('utf-8'), stderr.decode()


def tcam_thread_start(tcam_stop_event):
    tcam_threading = Thread(
        target=range_control,
        name="TCAM_Control",
        args=(tcam_stop_event, True, 60, testParameter.get("duration_soa", 12)),
        daemon=True,
    )
    tcam_threading.start()


if __name__ =="__main__":
    tcam = TcamLogCollect()
    tcam.copy_tcam_coredump("/root/cyb/soa_perstab_log/test/")