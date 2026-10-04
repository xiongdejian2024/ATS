#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_

"""
@Time: 2023/01/17 13:45  
@Author: lei.tao
@File: logmanager.py
@Software: PyCharm
@Description: 台架日志管理器
@Example:
"""
import concurrent.futures
import logging
import sys
import threading
import time
import os
import re
import base64
import subprocess
from pathlib import Path
from threading import Thread, Event
from six.moves import queue
from xat_ecu import reporting as allure
from xat_ecu.legacy.common.singleton import SingletonMeta
from xat_ecu.legacy.common.time_handle import get_time_str_year_month_day
from xat_ecu.legacy.driver.ssh_interface import command_send, close_command
from xat_ecu.legacy.interface.baidu_bos.bos_api import BosApi
from xat_ecu.legacy.interface.youzi.youzi import YouZiClient

project_root = __import__("xat_ecu.resources", fromlist=["LEGACY_ROOT"]).LEGACY_ROOT.as_posix()
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.file_handle import ecu_simulator_abspath
from xat_ecu.legacy.interface.nuc_app import exec_shell
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.common.constant import *
from xat_ecu.legacy.driver.ssh_client import *
from xat_ecu.legacy.interface.nuc_app import *

partner_log_path = Path(ecu_simulator_abspath) / 'soa_partner' / 'BootesRelease' / 'out' / 'x86' / 'log'


def mk_folder(log_path="/home/"):
    """
    程序开始运行时创建日志文件
    """
    pwd = os.getcwd().split('/')[-1]
    fold = pwd

    if pwd == "bgm":
        bgm = os.path.join(log_path, "BGM", s_timestamp(), fold)
        if not os.path.exists(bgm):
            os.makedirs(bgm)
        return bgm, "bgm"
    elif pwd == "tcam":
        tcam = os.path.join(log_path, "TCAM", s_timestamp(), fold)
        if not os.path.exists(tcam):
            os.makedirs(tcam)
        return tcam, "tcam"
    elif pwd == "soa":
        soa = os.path.join(log_path, "SOA", s_timestamp(), fold)
        if not os.path.exists(soa):
            os.makedirs(soa)
        return soa, "soa"
    else:
        logger.error("Working directory error!!")
        exit()


def get_device_name():
    device_name = os.getcwd().split('/')[-1].upper()
    if device_name == 'SOA':
        device_name = 'BGM'
    if device_name == 'BASETECH':
        device_name = 'BGM'
    if device_name == 'MINING':
        device_name = 'BGM'
    if device_name == 'MCU':
        device_name = 'BGM'
    if device_name not in ['BGM', 'TCAM']:
        logger.warning(f"device_name: {device_name} not in ['BGM', 'TCAM'], setting default BGM")
        return 'BGM'
    return device_name


def device_log_cmd_mapping():
    mapping_info = {
        "BGM": "/app/bin/logcat -F",
        "TCAM": "/oemapp/bin/logcat -F"
    }
    return mapping_info


def s_timestamp():
    """
    获取时间戳, 格式: 年月日
    :return: str
    """
    return time.strftime("%Y%m%d", time.localtime())


def timestamp():
    """
    获取函数运行时的时间戳, 格式: 年月日时分秒
    :return: str
    """
    return time.strftime("%Y%m%d_%H%M%S", time.localtime())


def generate_file_name_by_testcase(case_name, path='/root/test_case_log'):
    """
    根据用例名称生成log文件
    :param case_name: 用例名称 name
    :param path: 用例名称 name
    :return: log name
    """
    log = f"{case_name}"
    log_path = os.path.join(path, log)
    if not os.path.exists(log_path):
        os.mknod(log_path)
    return log_path


def generate_file_name(method, path):
    """
    根据函数名生成log文件
    :param method: function name
    :return: log name
    """
    stamp = timestamp()
    pattern = r"\W"
    log = re.sub(pattern=pattern, repl="_", string=method) + "_" + stamp + ".log"
    log_path = os.path.join(path, log)
    if not os.path.exists(log_path):
        os.mknod(log_path)
    return log_path


def new_log(folder):
    """
    :param folder:
    :return:返回文件
    """
    # 列举folder目录下的所有文件，结果以列表形式返回。
    lists = os.listdir(folder)
    new_lists = {}
    for key in lists:
        data = ''.join(os.path.splitext(key)[0].split('_')[-2:])
        new_lists.update({key: data})
    max_key = max(new_lists.items(), key=operator.itemgetter(1))[0]

    # 获取最新文件的绝对路径
    file_new = os.path.join(folder, max_key)
    return file_new


class NonBlockingStreamReader:
    def __init__(
        self,
        process,
        file_path=None,
        raise_EOF=False,
        print_output=True,
        print_new_line=True,
        auto_kill=False,
        **kwargs,
    ):
        """
        非阻塞式文本流读取器
        :param process: a subprocess instance
        :param file_path: save stream readline to file
        :param raise_EOF: if True, raise an UnexpectedEndOfStream when stream is EOF before kill
        :param print_output: if True, print when readline
        :param print_new_line: if True, skip print old readline
        :param auto_kill: exit when read b''
        :keyword logger: a Logger instance
        :keyword name: use to set self.name, default id(self)
        """
        self._p = process
        # deque数组, 容量自增
        self._q = queue.Queue()
        self._lastline = None
        self.name = kwargs.get("name")
        self.logger = kwargs.get("logger", None)
        if not self.logger:
            self.logger = logging.getLogger(self.__class__.__name__)
        self.file_path = file_path
        if os.path.isfile(self.file_path):
            self._f = open(self.file_path, "a")
        elif os.path.isdir(self.file_path):
            file_name = self.name
            self.file_path = os.path.join(self.file_path, file_name)
            self._f = open(self.file_path, "a")
        else:
            self._f = None
        self.print_output = print_output
        self.print_pattern = None
        self.result_pattern = []

        def _populateQueue(p, queue, kill_event):
            """
            Collect lines from p.stdout and put them in 'queue'.
            """
            while not kill_event.is_set():
                line = p.stdout.readline().decode("utf8", errors="ignore").rstrip()
                if line is not None:
                    queue.put(line)
                    if self.print_output:
                        # print only new line
                        if print_new_line and line == self._lastline:
                            continue
                        self._lastline = line
                        if self.print_pattern:
                            match = re.search(self.print_pattern, line, re.I)
                            if match:
                                self.logger.info(f"[{self.name}]{repr(line)}")
                                self.result_pattern.append(repr(line))
                        else:
                            self.logger.info(f"[{self.name}]{repr(line)}")
                    if line == "":
                        if auto_kill:
                            self.kill()
                    else:
                        try:
                            self._f.write(line + '\n')
                        except:
                            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/common/logmanagment/logmanager.py")
                            self._f.close()
                elif kill_event.is_set():
                    break
                elif raise_EOF:
                    self._f.close()
                    raise UnexpectedEndOfStream
                else:
                    break
            import signal

            self._f.close()
            os.killpg(p.pid, signal.SIGTERM)

            # p.kill()
            # p.terminate()
            # p.wait()

        self._kill_event = Event()
        self._t = Thread(
            target=_populateQueue,
            args=(self._p, self._q, self._kill_event),
            name=f"{self.name}",
        )
        self._t.daemon = True

        try:
            self._t.start()  # start collecting lines from process's stdout
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/common/logmanagment/logmanager.py")
            logger.error(e)

    def set_print_output(self, flag: bool):
        self.print_output = flag

    def set_print_pattern(self, pattern: str, timeout=None):
        self.print_pattern = pattern
        if timeout:
            start = time.time()
            end = 0
            while end < timeout:
                if len(self.result_pattern) == 0:
                    time.sleep(0.01)
                    end = time.time() - start
                else:
                    end = timeout
                    logger.info(f"检测到{pattern}关键字")
                    self.kill()
                    return True
            else:
                self.logger.error("pattern not found in time")
                logger.error(f"{timeout}秒内还未检测到{pattern}关键字")
                return False
        else:
            while True:
                if len(self.result_pattern) != 0:
                    logger.info(f"检测到{pattern}关键字")
                    self.kill()
                    break
                else:
                    time.sleep(0.01)
            return True

    def get_file_path(self):
        return self.file_path

    def readline(self, timeout=None):
        try:
            return self._q.get(block=timeout is not None, timeout=timeout)
        except queue.Empty:
            return None

    def read(self, timeout=0):
        time.sleep(timeout)
        lines = []
        while True:
            line = self.readline()
            if line is None:
                break
            lines.append(line)
        return b"\n".join(lines)

    def kill(self):
        self._kill_event.set()


class UnexpectedEndOfStream(Exception):
    pass


class Logmagment(metaclass=SingletonMeta):
    def __init__(self, log_path="/root/", **kwargs):
        self.log_path = log_path
        logger = kwargs.get("logger")
        if logger:
            self.logger = logger
        else:
            logging.basicConfig(level=logging.INFO, stream=sys.stdout)
            self.logger = logging.getLogger(self.__class__.__name__)

        self.username_bgm = base64.b64decode(
            BGM_CONSTANT.BGM_USERNAME.encode()
        ).decode()
        self.hostname_bgm = base64.b64decode(
            BGM_CONSTANT.BGM_HOSTNAME.encode()
        ).decode()
        self.password_bgm = base64.b64decode(
            BGM_CONSTANT.BGM_PASSWORD.encode()
        ).decode()
        self.username_tcam = base64.b64decode(
            TCAM_CONSTANT.TCAM_USERNAME.encode()
        ).decode()
        self.hostname_tcam = base64.b64decode(
            TCAM_CONSTANT.TCAM_HOSTNAME.encode()
        ).decode()
        self.password_tcam = base64.b64decode(
            TCAM_CONSTANT.TCAM_PASSWORD.encode()
        ).decode()
        self.callback = kwargs.get('callback')
        self.set_callback(self.callback)
        self.log_info = ''
        self.device_name = get_device_name()
        self.log_file_name = None
        self.current_thread = None
        self.partner_log_exist = False
        self.queue = queue.Queue()

    def mkdir_file(self, method):
        """
        新建日志文件
        :param method:根据函数名生成对应的log文件
        """
        global folder, device
        folder, device = mk_folder(log_path=self.log_path)
        generate_file_name(method, path=folder)

    def start_cmd_log(self, log_cmd, bgm_ip, print_output=False):
        """
        获取台架log持续输出到日志文件
        :param cmd: 台架获取日志的命令
        :param bgm_ip: bgm台架的ip地址
        :return: a NonBlockingStreamReader instance
        """
        self.logger.info("正在执行{}的模块函数".format(device))
        if device == "bgm" or device == "soa":
            self.logger.info("正在获取BGM台架的日志信息")
            line_generator = f"sshpass -p {self.password_bgm} ssh -o StrictHostKeyChecking=no {self.username_bgm}@{bgm_ip} '{log_cmd}' "

        elif device == "tcam":
            self.logger.info("正在获取TCAM台架的日志信息")
            line_generator = f"sshpass -p {self.password_tcam} ssh {self.username_tcam}@{self.hostname_tcam} '{log_cmd}'"

        data = subprocess.Popen(
            line_generator,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            close_fds=True,
            preexec_fn=os.setsid,
        )
        global file
        file = new_log(folder=folder)
        self.logger.info("本次写入日志的文件名: {}".format(file))
        return NonBlockingStreamReader(
            data,
            file_path=self.log_path,
            print_output=print_output,
            name=file,
            logger=self.logger,
        )

    def start_log(self, bgm_ip, dev=None, print_output=False):
        """
        获取台架log持续输出到日志文件
        :param bgm_ip: bgm台架的ip地址
        :param dev:如果device不是bgm或者tcam, 需要写明需要获取log的台架名
        :return: a NonBlockingStreamReader instance
        """
        # 解决sshpass第一次连接失败的
        import pexpect

        cmd = f"ssh root@{bgm_ip} pwd"
        root = pexpect.spawn(cmd)
        try:
            while True:
                index = root.expect(
                    [
                        'Are you sure you want to continue connecting',
                        'password',
                        'update',
                        'Connection refused',
                        'Temporary failure',
                    ]
                )
                if index == 0:
                    root.sendline('yes')
                    self.logger.debug("确认连接BGM")
                elif index == 1:
                    root.sendline('mars1bgm')
                    self.logger.debug("连接BGM成功")
                    break
                elif index == 2:
                    self.logger.debug("连接BGM成功")
                    break
                else:
                    time.sleep(1)
                    root = pexpect.spawn(cmd)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/common/logmanagment/logmanager.py")
            self.logger.error(e)

        self.logger.info("正在执行{}的模块函数".format(device))
        if device == "bgm":
            self.logger.info("正在获取BGM台架的日志信息")
            line_generator = f"sshpass -p {self.password_bgm} ssh {self.username_bgm}@{bgm_ip} 'tail -F /log/jetlog_messages'"

        elif device == "tcam":
            self.logger.info("正在获取TCAM台架的日志信息")
            line_generator = f"sshpass -p {self.password_tcam} ssh {self.username_tcam}@{self.hostname_tcam} 'tail -F /mnt/sdcard/log/jetlog_messages' "

        else:
            self.logger.info(f"工作目录不在bgm或者tcam下, 开始验证获取台架")
            if not dev or dev.lower() == "bgm":
                line_generator = f"sshpass -p {self.password_bgm} ssh {self.username_bgm}@{bgm_ip} 'tail -F /log/jetlog_messages'"
            elif dev.lower() == "tcam":
                line_generator = f"sshpass -p {self.password_tcam} ssh {self.username_tcam}@{self.hostname_tcam} 'tail -F /mnt/sdcard/log/jetlog_messages' "
            else:
                self.logger.error(f"{dev}赋值有误, 只能是bgm获取tcam")
                exit()

        data = subprocess.Popen(
            line_generator,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            close_fds=True,
            preexec_fn=os.setsid,
        )

        global file
        file = new_log(folder=folder)
        self.logger.info("本次写入日志的文件名: {}".format(file))

        return NonBlockingStreamReader(
            data,
            file_path=self.log_path,
            print_output=print_output,
            name=file,
            logger=self.logger,
        )

    def is_alive(self, ip):
        """
        校验台架是否有重启

        """
        import pexpect
        import socket

        if device == "tcam":
            root = pexpect.spawn(
                command=f"ssh {self.username_tcam}@{self.hostname_tcam}", timeout=2
            )
            try:
                p = root.expect(
                    ['password', 'Connection refused', 'No route to host'], timeout=2
                )
                if p == 0:
                    return True
                else:
                    return False
            except (socket.error, pexpect.EOF, pexpect.TIMEOUT, Exception):
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/common/logmanagment/logmanager.py")
                return False

        else:
            root = pexpect.spawn(command=f"ssh {self.username_bgm}@{ip}", timeout=2)
            try:
                p = root.expect(
                    ['password', 'Connection refused', 'No route to host'], timeout=2
                )
                if p == 0:
                    return True
                else:
                    return False
            except (socket.error, pexpect.EOF, pexpect.TIMEOUT, Exception):
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/common/logmanagment/logmanager.py")
                return False

    def start_log_withrestart(
        self, bgm_ip, dev, result: NonBlockingStreamReader, print_out
    ):
        """
        针对有重启现象的台架特殊处理
        Args:
            bgm_ip (_type_): BGM的动态ip

        Returns:
           a NonBlockingStreamReader instance
        """
        i = 1
        while True:
            if self.is_alive(bgm_ip) is True:
                time.sleep(1)
                # logger.info("无重启")
            else:
                # logger.info("台架有重启, 关闭log获取")
                result.kill()
                logger.info("重启后开始获取obd ip")
                while True:
                    if not self.is_alive(bgm_ip):
                        time.sleep(1)
                        # logger.info(f"暂未获取到BGM的ip, 等待1s")
                    else:
                        ip = get_obd_ip()
                        logger.info(f"重启后BGM的ip为{ip}")
                        break
                i += 1
                result = ""
                logger.info(f"台架重启后第{i}次开启log")
                result = self.start_log(ip, dev, print_out)

    def getvaluefromthread(self, ip):
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            to_do = []
            future = executor.submit(self.start_log, ip)
            to_do.append(future)

            for future in concurrent.futures.as_completed(to_do):  # 并发执行
                return future.result()

    def start_log_Thread(self, ip, dev=None, start=True, print_out=False):
        """
        针对BGM/TCAM重启后继续获取台架log持续输出到日志文件

        Args:
            ip (_type_): BGM的动态ip
        """
        result = self.start_log(ip, dev, print_out)
        logger.info("执行本case第1次开启log")
        if start:
            p = Thread(
                target=self.start_log_withrestart, args=(ip, dev, result, print_out)
            )
            p.setDaemon(True)
            p.start()
        return result

    def stop_log(self, bgm_ip, streamReader: NonBlockingStreamReader = None):
        """
        停止读取cmd返回的文本流
        :param streamReader: a NonBlockingStreamReader instance
        :return: log文件绝对路径
        """
        if streamReader:
            streamReader.kill()
            return streamReader.get_file_path()
        os.system(
            "ps -ef|grep -i 'tail -F'| grep -v grep |awk '{printf $2"
            + ' "\\n" '
            + "}'|xargs kill -9"
        )

        if device == "tcam":
            TCAM_SSH().exec(
                cmd="ps -ef|grep 'tail -F'| grep -v grep |awk '{printf $1\"\\n\"}'|xargs kill -9",
                bgm_ip=bgm_ip,
            )
        else:
            BGM_SSH(bgm_ip).type_commands(
                "ps -ef|grep 'tail -F'| grep -v grep |awk '{printf $2\"\\n\"}'|xargs kill -9"
            )

    def nonblocking_pattern_check(
        self, bgm_ip, dev, pattern: str, cmd=None, timeout=None
    ):
        """
        :param bgm_ip: BGM台架IP
        :param pattern: 关键字断言
        :param cmd :查询关键字需要输入的命令
        :param timeout: 查询关键字的超时时间
        :return: 匹配成功返回True, 失败返回False
        """
        streamReader = self.start_log_Thread(bgm_ip, dev, print_out=True)
        if cmd:
            logger.info(f"开始输入台架命令{cmd}")
            if dev.lower() == "tcam":
                TCAM_SSH().exec(cmd=cmd, bgm_ip=bgm_ip)
            elif dev.lower() == "bgm":
                BGM_SSH(bgm_ip).type_commands(commands=cmd)
            else:
                logger.info("请输入需要获取log的台架（bgm或者tcam）")
        data = streamReader.set_print_pattern(pattern=pattern, timeout=timeout)
        self.stop_log(bgm_ip, streamReader)
        return data

    def pattern_check(self, pattern):
        """
        :param pattern: 关键字断言
        :return: 匹配的字符串列表
        :use: 在各功能模块的after_each_func函数中调用
        """
        matches = []
        cmd = f"cat {file} | grep {pattern}"
        data = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()
        for match in data[0].decode().split('\n'):
            self.logger.info(f"command grep {pattern} match: {match}")
            if pattern in match:
                matches.append(match)

        if len(matches) == 0:
            return False, f"匹配失败，没有找到该关键字"
        else:
            assert True, f"匹配成功"
            return True, f"匹配成功", matches

    def set_callback(self, callback: object):
        if callback:
            self.callback = callback
        else:
            self.callback = self.__get_log_raw_data

    def __get_log_raw_data(self, data):
        if data:
            with open(self.log_file_name, 'a') as f:
                f.write(data.encode().decode())

    def record_log_thread(self):
        cmd = device_log_cmd_mapping()[self.device_name]
        while True:
            command_send(device_name=self.device_name,
                         cmd='\x03',
                         alias=f'{self.device_name}_log', log_print=False, timeout=2)
            command_send(
                device_name=self.device_name,
                cmd=cmd,
                alias=f'{self.device_name}_log',
                callback=self.callback,
                log_print=False,
                timeout=1800
            )
            command_send(device_name=self.device_name,
                         cmd='\x03',
                         alias=f'{self.device_name}_log', log_print=False, timeout=2)

    def start_record_log(self, case_name):
        """
        异步录制log
        :params case_name: 用例名称
        :return:None
        """
        self.log_file_name = generate_file_name_by_testcase(case_name=case_name)
        logger.info(f"=============== start {self.log_file_name} record =======================")
        # 保证线程只启动一次
        if self.current_thread and self.current_thread.is_alive():
            pass
        else:
            t = Thread(target=self.record_log_thread, name=f"record_{self.device_name}_log_thread")
            t.setDaemon(True)
            t.start()
            logger.info(f'已开启线程录制{self.device_name}日志， 线程名:{t.name}')
            self.current_thread = t
            time.sleep(3)  # 保证线程完全启动

    def stop_record_log(self):
        """
        停止录制log
        :return:None
        """
        logger.info(f"=============== stop {self.log_file_name} record =======================")
        log_file_name = self.log_file_name.split('/')[-1]
        jetlog_zip = f"/root/test_case_log/{log_file_name}_jetlog_{uuid.uuid4()}.zip"
        if os.path.exists('/root/test_case_log'):
            res = os.system(f"cd /root/test_case_log/;zip -r {jetlog_zip} {log_file_name};rm -rf {log_file_name}")
            if res == 0:
                logger.info("zip jetlog file success")
            else:
                logger.error(f"zip jetlog file failed! ret: {res}")
        if os.path.exists(jetlog_zip):
            # allure.attach.file(jetlog_zip, 'jetlog日志', 'application/zip', 'zip')
            bos_client = BosApi()
            try:
                remote_link = bos_client.put_and_get_url(
                    file_path=jetlog_zip,
                    target_path=f'SOA/allure_report/{get_time_str_year_month_day()}')
            except Exception as e:
                logger.exception(f"jetlog日志上传bos失败: {e}")
                allure.attach.file(jetlog_zip, 'jetlog日志', 'application/zip', 'zip')
            else:
                allure.attach(remote_link, 'jetlog日志', allure.attachment_type.URI_LIST)
            return jetlog_zip
        else:
            return None

    def check_log_by_keywords_start_thread(self,
                                           log_type,
                                           keywords=None,
                                           unexpect_keywords=None,
                                           log_print=False,
                                           device_name=None,
                                           timeout=10):
        """
        通过关键字检查日志，需要配合check_log_by_keywords_stop_thread一起使用
        :params log_type: 日志类型，必选，例如:rvc
        :params keywords: 查询关键字，支持多个关键字查询，必选，列表或者字符串
        :params unexpect_keywords: 查询不期望的关键字，支持多个关键字查询，可选，列表或者字符串
        :params log_print: 设备上的原生日志是否打印，默认不打印
        :params device_name: 设备类型
        :params timeout: 超时时间，如果超时时间之后未查询到关键字会返回False，否则返回True
        :return:None
        """
        if device_name is None:
            device_name = self.device_name
        command_send(device_name=device_name,
                     cmd='\x03',
                     alias=f'{device_name}_check', log_print=log_print, timeout=10)
        t = Thread(target=self.__check_log_by_keywords,
                   args=(log_type, keywords, unexpect_keywords, log_print, timeout, device_name))
        t.start()

    def __check_log_by_keywords(self, log_type, keywords, unexpect_keywords, log_print, timeout, device_name):
        cmd = f'{device_log_cmd_mapping()[self.device_name]} | grep {log_type}'
        status, cmd_ret = command_send(device_name=device_name,
                                       expect=keywords,
                                       unexpect=unexpect_keywords,
                                       cmd=cmd,
                                       timeout=timeout,
                                       log_print=log_print,
                                       alias=f'{device_name}_check')
        command_send(device_name=device_name,
                     cmd='\x03',
                     alias=f'{device_name}_check', log_print=log_print, timeout=2)
        self.queue.put((status, cmd_ret))

    def check_log_by_keywords_stop_thread(self):
        """
        等待返回检查结果，需要配合check_log_by_keywords_start_thread一起使用
        :return:
             status:成功与失败的标志
             ret:日志返回结果
        """
        status, ret = self.queue.get()
        return status, ret

    @staticmethod
    def start_record_soa_partner_log():
        if partner_log_path.exists():
            logger.info(f"=============== start partner log record =======================")
            exec_shell(f'rm -rf {partner_log_path}/*')
        else:
            logger.warning(f"{partner_log_path}不存在 不进行partner log录制")

    @staticmethod
    def stop_record_soa_partner_log():
        partner_log_zip = f"/root/test_case_log/partner_log_{uuid.uuid4()}.zip"
        if partner_log_path.exists():
            res = os.system(f"cd {partner_log_path};rm -rf /root/test_case_log/partner_log*.zip;zip -r {partner_log_zip} ./*")
            if res == 0:
                logger.info("zip partner log success")
            else:
                logger.error(f"zip partner log failed! ret: {res}")
            if os.path.exists(partner_log_zip):
                # allure.attach.file(partner_log_zip, 'soa_partner日志', 'application/zip', 'zip')
                bos_client = BosApi()
                try:
                    remote_link = bos_client.put_and_get_url(
                        file_path=partner_log_zip,
                        target_path=f'SOA/allure_report/{get_time_str_year_month_day()}')
                except Exception as e:
                    logger.exception(f"jetlog日志上传bos失败: {e}")
                    allure.attach.file(partner_log_zip, 'soa_partner日志', 'application/zip', 'zip')
                else:
                    allure.attach(remote_link, 'soa_partner日志', allure.attachment_type.URI_LIST)
                return partner_log_zip
            logger.info(f"=============== stop partner log record =======================")
            return None

        else:
            return None


if __name__ == '__main__':
    l = Logmagment()
    l.check_log_by_keywords_start_thread(log_type='rvc', keywords='xxxx')
    l.check_log_by_keywords_stop_thread()
    # check_log_by_keywords_start_thread(log_type='rvc', keywords='4211633185')
    # time.sleep(10)
    # check_log_by_keywords_stop_thread()
    pass
