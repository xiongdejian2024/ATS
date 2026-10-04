#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: serial_client.py
@Time: 2022/6/19 13:00
@Author: lei.tao
@Software: PyCharm
@Description: serial串口驱动类的封装，通过串口执行命令，获取串口输出
@Examples:
"""

import datetime
import io
import os
import re
import sys
import threading
import time
from serial import Serial, SerialException
from serial.tools.list_ports import comports

project_root = __import__("xat_ecu.resources", fromlist=["LEGACY_ROOT"]).LEGACY_ROOT.as_posix()

from xat_ecu.legacy.common.logger import logger


def get_device_name():
    """
    Get device name/path of the USB connection
    :return: string
        Full path of device e.g  on linux systems /dev/ttyUSBx or
        on window COMx
    """

    plist = list(comports())
    if len(plist) <= 0:
        logger.info("没有发现连接的端口")
        sys.exit("请先连接串口")
    elif len(plist) == 1:
        plist_0 = list(plist[0])
        serialname = plist_0[0]
        ser = Serial(serialname, 115200, timeout=1)
        logger.info(f"已连接成功，可用端口>>>{ser.name}")
        return ser.name
    else:
        i = 0
        comAttr = []
        port_list = []
        while i < len(plist):
            comAttr.append(list(plist[i]))
            i = i + 1
        logger.info(f"所有已连接的串口列表为{comAttr}, 请选择端口")
        for attr in comAttr:
            port_list.append(attr[0])

        while True:
            _port = input("Enter your serial port: ")
            if _port in port_list:
                break
            else:
                logger.error("Error!!! Please input correct serial port! Please try again!")
                continue

        return _port


class BaseSerial:
    tx_encoding = 'utf-8'
    rx_encoding = 'utf-8'
    READ_TIMEOUT = 0.5
    login_account = "jiduer"
    login_password = __import__("os").environ.get('XAT_CREDENTIAL_ECU__DRIVER_SERIAL_CLIENT_PY_LOGIN_PASSWORD', "")

    def __init__(self, *args, **kwargs):
        """初始化函数
        kwargs:
        * tx_encoding: 串口写入之前是否选择编码。UTF-8: 对字符串进行utf-8编码; None: 输入的是bytes, 不用编码, 这个值必须根据实际收发的数据类型设置正确
        * rx_encoding: 对串口返回的数据进行解码。UTF-8: 使用utf-8解码; None: 不解码
        * timeout: 串口读的超时设置
        * logfile: 用来记录整个串口操作期间的串口输出
        """
        self.args = args
        self.kwargs = kwargs
        timeout = kwargs.get('timeout', self.READ_TIMEOUT)
        rx_encoding = kwargs.get('rx_encoding', self.rx_encoding)
        tx_encoding = kwargs.get('tx_encoding', self.tx_encoding)
        self.account = kwargs.get('account', self.login_account)
        self.password = kwargs.get('password', self.login_password)
        log_file = kwargs.get('logfile', None)
        is_check_login = kwargs.get('is_check_login', True)
        auto_start = kwargs.get('auto_start', True)

        if log_file:
            self.logfile = log_file
            if self.rx_encoding is None:
                self.fout = open(log_file, 'ab')
            else:
                self.fout = open(log_file, 'a', encoding='utf-8')
        else:
            self.logfile = self.fout = None
        if "logfile" in kwargs:
            del kwargs['logfile']  # Serial中kwargs没有定义logfile参数
        if "is_check_login" in kwargs:
            del kwargs['is_check_login']
        if "auto_start" in kwargs:
            del kwargs['auto_start']
        self.set_rx_encoding(rx_encoding)
        self.set_tx_encoding(tx_encoding)

        self.read_lock = threading.RLock()
        self.receiver_thread = None
        self.hook = None
        kwargs['timeout'] = min(timeout, self.READ_TIMEOUT)


        self.check_mark = False
        self.alive = True
        if auto_start:
            self.start_serial()
        if is_check_login:
            self._is_check_login()

    def _is_check_login(self):
        tmp_recv = []
        while True:
            recv = self.serial.readlines()
            tmp_recv.extend(recv)
            if len(recv) >= 1:
                if "ogin" in recv[-1].decode().strip():
                    logger.info("发送账户名jiduer 1")
                    self.serial.write(self.account.encode())
                    time.sleep(0.1)

                if "assword" in recv[-1].decode().strip():
                    logger.info("发送密码bgm@Axzfr778 2")
                    self.serial.write(self.password.encode())
                    time.sleep(0.1)

                # elif ':~$' in recv[-1].decode().strip():
                elif recv[-1].decode().endswith(
                        ('$', ' # ', '~#', '~$ ', '~ # ', '# ', '~$', '$ ')):
                    break
                elif str(recv[-1]).find("heart beat") != -1:
                    break
            else:
                self.serial.write("\r\n".encode('utf-8'))

    def start_serial(self, port=None):
        if port is None:
            port = get_device_name()
        self.clear_buffer()
        self.serial = Serial(*self.args, port=port, **self.kwargs)
        self.start()

    def read_log(self, file_obj, timeout):
        last_time = 0
        recv = []
        while last_time * 0.1 < timeout:
            time.sleep(0.1)
            try:
                recv = self.serial.readlines()
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/serial_client.py")
                if str(e).find("port that is not open") == -1:
                    logger.info("Error info:{}".format(e))
                pass
            if recv == []:
                pass
            else:
                file_obj.write(str(recv))
            last_time = last_time + 1

    def get_file_path(self):
        return self.logfile

    def begin_check(self):
        """设置开始检查串口输出标志

        :rtype: None
        """
        self.check_mark = True

    def end_check(self):
        """设置停止检查串口输出标志

        :rtype: bool
        """
        self.check_mark = False

    def last_buffer(self, clear=True):

        """获取缓冲区内容

        :param bool clear: 是否清空缓冲区内容

        :rtype: str
        :return: 缓冲区内容
        """
        res = self.buff.getvalue()

        if clear:
            self.clear_buffer()

        return res

    def clear_buffer(self):
        """清空缓冲区内容

        :rtype: None
        """
        if self.rx_encoding is None:
            self.buff = io.BytesIO()
        else:
            self.buff = io.StringIO()

    def expect_sync(self, cmd, pattern, timeout):
        """通过串口执行命令，直到匹配的关键字出现，或者超时退出。
        无论是否匹配成功，都会清空缓冲区，为执行下次命令恢复环境。

        :param str cmd: 需执行的串口命令
        :param str pattern: 正则表达式，用于匹配输出关键字。如果为None，则执行命令后直接返回成功。
        :param int timeout: 如果在超时时间内没有匹配到输出关键字，则强制退出

        :rtype: (bool, str)
        :return: 是否匹配到关键字，串口输出内容
        """
        ret = False
        res = ""

        # 这个标志告诉reader线程开始积聚数据来匹配
        self.check_mark = True
        if cmd is not None:
            try:
                self.serial.write(cmd)

            except Exception as ex:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/serial_client.py")
                self.handle_conn_error(ex)

        if pattern is None:
            ret, res = True, ""

        # need to expect pattern
        cur = datetime.datetime.now()
        while self.alive:
            # 每隔100ms读取一次
            time.sleep(0.1)

            res = self.buff.getvalue()

            if pattern and re.search(pattern, res, re.DOTALL):
                ret = True
                break

            interval = datetime.datetime.now() - cur
            if interval.total_seconds() > timeout:
                break

        # ensure no queue of input anymore
        self.check_mark = False

        with self.read_lock:
            self.clear_buffer()

        return ret, res

    def expect_async(self, cmd, pattern, last):
        """通过串口执行命令，等待一段时间后退出，但是不会清空缓冲区，为后续可能的匹配所用。

        :param str cmd: 需执行的串口命令
        :param str pattern: 占位符，不使用。
        :param float last: 等待时间。

        :rtype: None
        """

        # 这个标志告诉reader线程开始积聚数据来匹配
        self.check_mark = True
        if cmd is not None:
            self.serial.write(cmd)

        time.sleep(float(last))
        self.check_mark = False

    def send(self, command, pattern=None, timeout=10, sync=True):
        """朝串口发送命令
        向串口发送指令，同时根据指定的模式pattern来观察串口的输出是否是期望的值。

        :param str/bytes/list command: 命令，可以是str/bytes/list, list会当做二进制字节流拼接成bytes进行发送
        :param str pattern: 要匹配的串口输出
        :param int timeout: 超时设置，最多等这么多时间
        :param bool sync: 同步执行命令或异步执行命令

        :rtype: (bool, str)
        :return: 返回真假值和串口输出
        """

        self.clear_buffer()
        if command is None or len(command) == 0:
            cmd = None
        elif isinstance(command, str):
            # cmd = (command + "\r").encode(encoding=self.tx_encoding)
            cmd = command.encode(encoding=self.tx_encoding)
        elif isinstance(command, list):
            cmd = bytes(command)
        else:  # bytes
            cmd = command
        logger.info(f"串口发送命令{command}, 超时时间为{timeout}s")
        if pattern:
            logger.info(f"要匹配的串口输出为{pattern}")
        if sync:
            self.expect_sync(cmd, pattern, timeout)
        else:
            threading.Thread(target=self.expect_async, args=(cmd, pattern, timeout)).start()
            return True, ""

    def receive_data(self):
        """获取串口所有输出"""

        while self.alive:
            # read all that is there or wait for one byte
            try:
                # data = self.serial.read_until()
                data = self.serial.read_all()

            except SerialException as ex:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/serial_client.py")
                logger.error("Read from serial port failed")
                logger.error(ex)

            else:
                if len(data) == 0:
                    continue
                if self.rx_encoding is None:
                    output = data
                else:
                    output = data.decode(self.rx_encoding, errors='ignore')

                with self.read_lock:
                    if self.check_mark:
                        self.buff.write(output)
                if self.fout:
                    self.fout.write(output)
                    self.fout.flush()

                return output

    def start(self):
        """start worker threads
        Start worker threads for reading/sending data from/to serial port
        """
        self.alive = True

        self.receiver_thread = threading.Thread(target=self.receive_data, name='rx')
        self.receiver_thread.daemon = True
        self.receiver_thread.start()

    def stop(self):
        """Stop worker threads"""
        self.alive = False
        self.receiver_thread.join()

    def close(self):
        """Close serial port"""
        if self.alive is True:
            self.stop()
        if self.fout:
            self.fout.close()
        try:
            self.serial.close()
        except SerialException as ex:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/serial_client.py")
            self.handle_conn_error(ex)
        logger.info(f"stop serial")

    def set_rx_encoding(self, encoding, errors='replace'):
        """set encoding for received data"""
        self.rx_encoding = encoding

    def set_tx_encoding(self, encoding, errors='replace'):
        """set encoding for transmitted data"""
        self.tx_encoding = encoding

    def handle_conn_error(self, error=None):
        """
        Serial port error
        :param error: port exceptions
        """
        # close the connection and forward the exception
        logger.error("Serial connection exception: {}".format(str(error)))
        self.close()
        if isinstance(error, Exception):
            raise error  # pylint: disable=E0702


if __name__ == "__main__":
    # port = get_device_name()
    # print(port)
    com = BaseSerial(baudrate=921600, timeout=0.1, is_check_login=False)
    com.start_serial()
    # print(com)
    # com.send('sys --hbmOff', timeout=int(10))
    com.send('sys --update 10', pattern='CCCCC', timeout=int(10))
    qq = com.receive_data()
    print(qq)
    # print("ip地址：" + str(qq))
    com.close()
