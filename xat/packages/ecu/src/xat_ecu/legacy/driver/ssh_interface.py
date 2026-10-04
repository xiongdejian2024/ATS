# -*- coding: utf-8 -*-
"""
@File        : ssh_interface.py
@Author      : dejian.xiong@jiduauto.com
@Time        : 2023/7/6 上午11:27
@Description : 封装ssh交互接口
@Examples    :
```
command_send(device_name='BGM', cmd="pwd", expect='@', timeout=1)
```
"""
import socket

from typing import Tuple, List

import paramiko
from scp import SCPClient
import time
from base64 import b64decode

from xat_ecu.legacy.common.logger import logger

from xat_ecu.legacy.common.singleton import SingletonMeta
from xat_ecu.legacy.interface.nuc_app import get_obd_ip
from xat_ecu.legacy.common.constant import BGM_CONSTANT, CD_SOC_CONSTANT
from xat_ecu.legacy.common.constant import TCAM_CONSTANT
from xat_ecu.legacy.common.constant import ACU_CONSTANT
from xat_ecu.legacy.common.constant import CDCQ_CONSTANT
from xat_ecu.legacy.common.constant import NAD_CONSTANT

END_OF_CMD = ('$', ' # ', '~#', '~$ ', '~ # ', '# ', '~$', '$ ')

command_run_flag = False
RECONNECT_TIMEOUT = 240


def get_command_run_flag():
    global command_run_flag
    return command_run_flag


def set_command_run_flag(status):
    global command_run_flag
    command_run_flag = status


class BaseClient:
    def __init__(self, host: str, port: int = 22, **kwargs):
        self.host = host
        self.port = port
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.sock = kwargs.get("sock")
        self.dest_addr = kwargs.get("dest_addr")
        self.src_addr = kwargs.get("src_addr")

    def connect(self):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.host, self.port, self.username, self.password, sock=self.sock, timeout=20)
            logger.info(f"SSH连接已建立：{self.host}")
            return client
        except paramiko.AuthenticationException:
            # logger.error("身份验证失败")
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_interface.py")
            raise Exception('身份验证失败')
        except paramiko.SSHException:
            # logger.error("SSH连接错误:")
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_interface.py")
            raise Exception("SSH连接错误")
        except (paramiko.ssh_exception.NoValidConnectionsError, Exception):
            # logger.error("无法连接到主机")
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_interface.py")
            raise Exception(f"无法连接到{self.host}:{self.port}")


class ScpClient(BaseClient):
    def __init__(self, host: str, port: int = 22, **kwargs):
        super().__init__(host, port, **kwargs)
        self.scp_client = self.__get_scp_client()
        self.scp_session = self.__get_scp_session()

    def __get_scp_client(self):
        return self.connect()

    def __get_scp_session(self):
        session = SCPClient(self.scp_client.get_transport())
        return session

    def get(self, local_path, remote_path):
        logger.info(f'download {remote_path} to {local_path} ...')
        try:
            self.scp_session.get(local_path=local_path, remote_path=remote_path)
            logger.info(f'download {remote_path} to {local_path} success')
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_interface.py")
            logger.error(f'download fail, reason: {str(e)}')
        self.close()

    def put(self, local_path, remote_path):
        logger.info(f'upload {local_path} to {remote_path} ...')
        try:
            self.scp_session.put(files=local_path, remote_path=remote_path)
            logger.info(f'upload {local_path} to {remote_path} success')
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_interface.py")
            logger.error(f'upload fail, reason: {str(e)}')
        self.close()

    def close(self):
        self.scp_session.close()
        self.scp_client.close()


class SshClient(BaseClient):
    def __init__(self, host: str, port: int = 22, **kwargs):
        super().__init__(host, port, **kwargs)
        self.client = self.__get_client()
        self.__get_session()

    def __get_session(self):
        self.session = self.client.invoke_shell(width=200)
        data = ''
        while not data.endswith(END_OF_CMD) or self.session.recv_ready():
            raw_data = self.session.recv(1024)
            decode_raw_data = str(raw_data, encoding='utf-8', errors='ignore').encode('utf-8', 'ignore').decode(
                'utf-8', 'ignore')
            data += decode_raw_data
        logger.info(f'登录{self.host}成功， {data}')
        if 'root' not in data:
            timeout = 10
            logger.info(f'切root账号,超时时间{timeout}s')
            status, ret = self.execute(cmd=f'echo {self.password} | sudo -S whoami;sudo -s', log_print=False,
                                       timeout=timeout)
            if not status:
                logger.warning('root命令切换失败,尝试重新切换')
                self.session.close()
                self.session = self.__get_session()
            else:
                logger.info('root命令切换成功')
        else:
            logger.info(f'当前为root账户无需切换')
        return self.session

    def get_jump_client_connect(self, dest_addr: Tuple[str, int], src_addr: Tuple[str, int], timeout: int = 150):
        start_time = time.time()
        end_time = time.time()
        remainder = timeout
        while end_time - start_time < timeout:
            try:
                self.sock = self.client.get_transport().open_channel(
                    "direct-tcpip", dest_addr=dest_addr, src_addr=src_addr, timeout=5
                )
                logger.info(f'connect {dest_addr} channel success')
                return self.sock
            except paramiko.ssh_exception.SSHException as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_interface.py")
                if 'Timeout opening channel.' in str(e):
                    remainder -= 6
                else:
                    remainder -= 1
                logger.error(
                    f'通过{src_addr}连接{dest_addr}失败, 失败原因: {str(e)}, 等待继续连接, 剩余连接时间{remainder}s')
                time.sleep(1)
                end_time = time.time()
        else:
            raise Exception(f'connect {dest_addr} channel timeout')

    def __get_client(self):
        return self.connect()

    def __check_alive(self):
        self.client.exec_command('pwd', timeout=20)

    def execute(self, cmd, expect=None, unexpect=None, timeout: int = 60, **kwargs) -> Tuple[bool, str]:
        callback = kwargs.get("callback")
        log_print = kwargs.get("log_print")
        is_reconnected = kwargs.get("is_reconnected", True)
        print_raw_data = kwargs.get("print_raw_data", False)
        if log_print:
            log_type = logger.info
        else:
            log_type = logger.debug
        cmd.strip('\r\n') or cmd.strip('\n')
        expect_flag = False  # 该值为False时，超时时间结束后上报结果为True
        if expect is not None:
            expect_flag = True  # 该值为True时，超时时间内如果没有出现期望值，则会上报结果为false
        remove_space_cmd = cmd
        cmd += '\n'
        connect_time = time.time()
        try:
            self.__check_alive()
            self.session.settimeout(timeout)
            self.session.send(cmd)
            log_type(f'命令{remove_space_cmd}开始执行，超时时间为{timeout}s')
            if cmd.startswith("cd /data/;chmod +x tcpdump;/data/tcpdump"):
                set_command_run_flag(True)  # 设置命令开始运行的状态为True
            start_time = time.time()
            buffer = ''
            while not buffer.endswith(END_OF_CMD) or self.session.recv_ready():
                if connect_time > timeout + start_time:
                    logger.error(f'wait for {self.host} terminal return timeout ...')
                    raise paramiko.SSHException
                # 对于打包 压缩等响应较长的命令进行等待
                if not self.session.recv_ready():
                    time.sleep(0.5)
                    self.__check_alive()
                if self.session.recv_ready():
                    raw_data = self.session.recv(1024 * 1024)
                    decode_raw_data = str(raw_data, encoding='utf-8', errors='ignore').encode('utf-8', 'ignore').decode(
                        'utf-8', 'ignore')
                    if print_raw_data:
                        log_type(decode_raw_data)
                    buffer += decode_raw_data
                    if callback:
                        try:
                            callback(decode_raw_data)
                        except Exception as e:
                            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_interface.py")
                            logger.error(f'{str(e)}')
                    # 防止内存消耗过大将buff清空
                    if len(buffer) > 1024 * 1024 * 512:  # 512M
                        buffer = ''
                    if expect is not None and len(expect) > 1:
                        while expect:
                            first_expect = expect[0]
                            logger.info(f'检查{first_expect}是否出现在结果中')
                            if first_expect in decode_raw_data.replace(remove_space_cmd, ''):
                                logger.info(f'期望值{first_expect}已出现')
                                if len(expect) > 0:
                                    expect = expect[1:]
                                    if len(expect) == 0:
                                        logger.info(f'所有关键字检查ok')
                                        return True, buffer
                                else:
                                    break
                            elif len(expect) == 1:
                                break
                            else:
                                break
                    elif expect is not None and len(expect) == 1:
                        logger.info(f'检查{expect[0]}是否出现在结果中')
                        if expect[0] in decode_raw_data.replace(remove_space_cmd, ''):
                            logger.info(f'期望值{expect[0]}已出现')
                            logger.debug(f'{remove_space_cmd} execute success, >>>回显值为: {buffer}<<<')
                            return True, buffer
                    if unexpect:
                        if self.__check_unexpect(unexpect, decode_raw_data, remove_space_cmd):
                            return False, buffer
                end_time = time.time()
                if end_time - start_time > timeout + 2:
                    if expect_flag:
                        if expect is not None and len(expect) >= 1:
                            logger.info(f'未检查到{expect[0]}')
                        logger.error(f'{remove_space_cmd}执行超时，命令退出')
                        return False, buffer
                    if unexpect:
                        logger.info(f'{remove_space_cmd}执行时间已到，命令退出')
                        return True, buffer
                    else:
                        logger.info(f'{remove_space_cmd}执行时间已到，命令退出')
                        return False, buffer
            logger.debug(f'{remove_space_cmd} execute success, >>>回显值为: {buffer}<<<')
            return True, buffer
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_interface.py")
            if is_reconnected:
                logger.info(f'ssh connect error:{str(e)}, 重连中...')
                if hasattr(self.client, "close"):
                    try:
                        self.client.close()
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_interface.py")
                        logger.warning(f"客户端连接关闭报错：{e}")
                if hasattr(self.session, "close"):
                    try:
                        self.session.close()
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_interface.py")
                        logger.warning(f"会话关闭报错：{e}")
                return self.reconnect(cmd, expect, unexpect, timeout, **kwargs)

    @staticmethod
    def __check_unexpect(unexpect, data, remove_space_cmd):
        for target in unexpect:
            if target in data.replace(remove_space_cmd, ''):
                logger.error(f'不期望值{target}出现在结果中,命令退出')
                return True
            else:
                logger.info(f'不期望值{target}目前未出现在结果中,继续检查')

    def close(self):
        try:
            if self.sock:
                self.sock.close()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_interface.py")
            logger.error(f'sock close error, {str(e)}')
        try:
            self.session.close()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_interface.py")
            logger.error(f'session close error, {str(e)}')
        try:
            self.client.close()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_interface.py")
            logger.error(f'client close error, {str(e)}')
        logger.info(f"SSH连接已关闭：{self.host}")

    def reconnect(self, cmd, expect, unexpect, timeout, **kwargs) -> Tuple[bool, str]:
        connect_type = kwargs.get('connect_type')
        start_time = time.time()
        end_time = time.time()
        self.close()
        logger.info(f'正在重连中，重连超时时间为{RECONNECT_TIMEOUT}s')
        if self.dest_addr and self.src_addr:
            self.username, username = decode_encrypt_string(BGM_CONSTANT.BGM_USERNAME), self.username
            self.password, password = decode_encrypt_string(BGM_CONSTANT.BGM_PASSWORD), self.password
        while end_time - start_time < RECONNECT_TIMEOUT:
            # 通过BGM跳板机连接
            if self.dest_addr and self.src_addr:
                # 连接bgm
                try:
                    self.host = get_bgm_hostname(connect_type=connect_type)
                    self.sock = None
                    self.client = self.client_ = self.__get_client()
                except Exception:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_interface.py")
                    logger.info(f'{self.host} {self.port}断开连接, 重连中...')
                    time.sleep(1)
                    end_time = time.time()
                    continue
                try:
                    self.session = self.session_ = self.__get_session()
                except Exception:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_interface.py")
                    logger.info(f'{self.host} {self.port}断开连接, 重连中...')
                    time.sleep(1)
                    end_time = time.time()
                    self.client.close()
                    self.client_.close()
                    logger.info(f'close {self.host}, {self.host} {self.port}断开连接, 重连中...')
                    time.sleep(1)
                    continue
                # 连接目标设备
                try:
                    self.sock = self.get_jump_client_connect(dest_addr=self.dest_addr, src_addr=(self.host, self.port))
                    self.host = self.src_addr[0]
                    self.port = self.src_addr[1]
                    self.username = username
                    self.password = password
                    self.client = self.__get_client()
                except Exception:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_interface.py")
                    logger.info(f'{self.host} {self.port}断开连接, 重连中...')
                    time.sleep(1)
                    # 关闭跳板机，防止ssh连接上限
                    self.session_.close()
                    self.session.close()
                    self.client_.close()
                    self.client.close()
                    end_time = time.time()
                    continue
                try:
                    self.session = self.__get_session()
                except Exception:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_interface.py")
                    logger.info(f'{self.host} {self.port}断开连接, 重连中...')
                    time.sleep(1)
                    self.session_.close()
                    self.session.close()
                    self.client_.close()
                    self.client.close()
                    end_time = time.time()
                    continue
                else:
                    break
            else:
                try:
                    if '169.254' in self.host:
                        self.host = get_bgm_hostname(connect_type=connect_type)
                    self.client = self.__get_client()
                except (socket.timeout, OSError, paramiko.SSHException, Exception):
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_interface.py")
                    logger.info(f'{self.host} {self.port}断开连接, 重连中...')
                    end_time = time.time()
                    time.sleep(2)
                try:
                    self.session = self.__get_session()
                except (socket.timeout, OSError, paramiko.SSHException, Exception):
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_interface.py")
                    logger.info(f'{self.host} {self.port}断开连接, 重连中...')
                    end_time = time.time()
                    if hasattr(self.session, "close"):
                        self.session.close()
                    self.client.close()
                    time.sleep(2)
                else:
                    break

        if end_time - start_time > RECONNECT_TIMEOUT:
            raise Exception(f'ssh连接超时')
        # 遇到重启的命令时 不重新执行命令
        restart_commands = ['shutdown', 'poweroff', 'halt', 'reboot']
        if any(command in cmd for command in restart_commands):
            return True, '\r\n'
        else:
            status, output = self.execute(cmd, expect, unexpect, timeout, **kwargs)
            return status, '\r\n'.join(output.split('\r\n')[:-1])


def decode_encrypt_string(s):
    return b64decode(s).decode()


def get_bgm_hostname(connect_type):
    if connect_type == 'vlan':
        hostname = '172.16.5.1'
    elif connect_type == 'obd':
        hostname = get_obd_ip()
    return hostname


class SessionManager:
    def __init__(self, device_name):
        self.device_name = device_name

    def get_scp_session(self, connect_type):
        if self.device_name == 'BGM':
            self.scp_session = BgmSession().add_scp_session(connect_type)
            return self.scp_session
        elif self.device_name == 'TCAM':
            self.scp_session = TCAMSession().add_scp_session(connect_type)
            return self.scp_session
        elif self.device_name == 'ACU':
            self.scp_session = ACUSession().add_scp_session(connect_type)
            return self.scp_session
        elif self.device_name == 'CDCQ':
            self.scp_session = CDCQSession().add_scp_session(connect_type)
            return self.scp_session
        elif self.device_name == 'NAD':
            self.scp_session = NADSession().add_scp_session(connect_type)
            return self.scp_session
        elif self.device_name == 'CD_SOC':
            self.scp_session = CDSOCSession().add_scp_session(connect_type)
            return self.scp_session
        else:
            raise Exception('device_name not in [BGM, TCAM, ACU, CDCQ, NAD, CD_SOC]')

    def get_session(self, alias, connect_type):
        if self.device_name == 'BGM':
            self.session = BgmSession().add_session(alias, connect_type)
            return self
        elif self.device_name == 'TCAM':
            self.session = TCAMSession().add_session(alias, connect_type)
            return self
        elif self.device_name == 'ACU':
            self.session = ACUSession().add_session(alias, connect_type)
            return self
        elif self.device_name == 'CDCQ':
            self.session = CDCQSession().add_session(alias, connect_type)
            return self
        elif self.device_name == 'NAD':
            self.session = NADSession().add_session(alias, connect_type)
            return self
        elif self.device_name == 'CD_SOC':
            self.session = CDSOCSession().add_session(alias, connect_type)
            return self
        else:
            raise Exception('device_name not in [BGM, TCAM, ACU, CDCQ, NAD, CD_SOC]')

    def execute_command(self, cmd: str, expect: List, unexpect: List, timeout: int, **kwargs) -> Tuple[bool, str]:
        """
        执行命令
        :param cmd: 命令
        :param expect: 期望值
        :param unexpect: 不期望出现的关键字
        :param timeout: 超时时间
        :param kwargs:
        :return: 字符串
        """
        status, terminal_return = self.session.execute(cmd, expect, unexpect, timeout, **kwargs)
        return status, self.handle_terminal_return(terminal_return)

    def close(self):
        self.session.close()

    def handle_terminal_return(self, terminal_print: str) -> str:
        """
        去掉开头和结尾 只显示命令的返回
        :param terminal_print: 终端打印
        :return: 字符串
        """
        return '\n'.join(terminal_print.split('\r\n')[1:-1])


class BgmSession(metaclass=SingletonMeta):
    def __init__(self):
        self.sessions = {}
        self.scp_sessions = {}
        self.device_config_dict = {
            "hostname": decode_encrypt_string(BGM_CONSTANT.BGM_HOSTNAME),
            "port": int(decode_encrypt_string(BGM_CONSTANT.BGM_PORT)),
            "username": decode_encrypt_string(BGM_CONSTANT.BGM_USERNAME),
            "password": decode_encrypt_string(BGM_CONSTANT.BGM_PASSWORD),
        }

    def add_session(self, alias: str, connect_type: str) -> SshClient:
        """
        添加一个连接的session，如果不存在会创建一个连接保存在session中，如果存在会用已有session进行连接
        :param alias: 窗口别名
        :param connect_type: obd或者vlan连接
        :return: SshClient连接对象
        """
        if (alias, connect_type) in self.sessions.keys():
            return self.sessions.get((alias, connect_type))
        else:
            if connect_type == 'vlan':
                host = self.device_config_dict.get('hostname')
            else:
                host = get_bgm_hostname(connect_type)
            port = self.device_config_dict.get('port')
            username = self.device_config_dict.get('username')
            password = self.device_config_dict.get('password')
            ssh_obj = SshClient(host=host, port=port, username=username, password=password)
            self.sessions[(alias, connect_type)] = ssh_obj
            return ssh_obj

    def add_scp_session(self, connect_type: str) -> ScpClient:
        """
        添加一个scp session
        :param connect_type: obd或者vlan连接
        :return:
        """
        if connect_type == 'vlan':
            host = self.device_config_dict.get('hostname')
        else:
            host = get_bgm_hostname(connect_type)
        port = self.device_config_dict.get('port')
        username = self.device_config_dict.get('username')
        password = self.device_config_dict.get('password')
        scp_obj = ScpClient(host=host, port=port, username=username, password=password)
        return scp_obj

    def remove_session(self, alias: str, connect_type: str):
        if (alias, connect_type) in self.sessions:
            self.sessions[(alias, connect_type)].close()
            del self.sessions[(alias, connect_type)]


class TCAMSession(metaclass=SingletonMeta):
    def __init__(self):
        self.sessions = {}
        self.scp_sessions = {}
        self.device_config_dict = {
            "host": decode_encrypt_string(TCAM_CONSTANT.TCAM_HOSTNAME),
            "port": int(decode_encrypt_string(TCAM_CONSTANT.TCAM_PORT)),
            "username": decode_encrypt_string(TCAM_CONSTANT.TCAM_USERNAME),
            "password": decode_encrypt_string(TCAM_CONSTANT.TCAM_PASSWORD),
        }

    def add_session(self, alias: str, connect_type: str) -> SshClient:
        """
        添加一个连接的session，如果不存在会创建一个连接保存在session中，如果存在会用已有session进行连接
        :param alias: 窗口别名
        :param connect_type: 连接方式，支持obd和vlan
        :return: SshClient连接对象
        """
        if (alias, connect_type) in self.sessions.keys():
            return self.sessions.get((alias, connect_type))
        else:
            host = self.device_config_dict.get('host')
            port = self.device_config_dict.get('port')
            username = self.device_config_dict.get('username')
            password = self.device_config_dict.get('password')
            if connect_type == 'obd':
                src_addr = (get_bgm_hostname(connect_type), port)
                dest_addr = (host, port)
                sock = BgmSession().add_session(f'TCAM_{alias}', connect_type).get_jump_client_connect(
                    dest_addr=dest_addr, src_addr=src_addr
                )
                ssh_obj = SshClient(host=host, port=port, username=username, password=password, sock=sock,
                                    dest_addr=dest_addr, src_addr=src_addr)
            else:
                ssh_obj = SshClient(host=host, port=port, username=username, password=password)
            self.sessions[(alias, connect_type)] = ssh_obj
            return ssh_obj

    def add_scp_session(self, connect_type: str) -> ScpClient:
        """
        添加一个连接的session，如果不存在会创建一个连接保存在session中，如果存在会用已有session进行连接
        :return: SshClient连接对象
        """
        host = self.device_config_dict.get('host')
        port = self.device_config_dict.get('port')
        username = self.device_config_dict.get('username')
        password = self.device_config_dict.get('password')
        if connect_type == 'obd':
            src_addr = (get_bgm_hostname(connect_type), port)
            dest_addr = (host, port)
            BgmSession().remove_session('TCAM_scp', connect_type)
            sock = BgmSession().add_session('TCAM_scp', connect_type).get_jump_client_connect(
                dest_addr=dest_addr, src_addr=src_addr
            )
            scp_obj = ScpClient(host=host, port=port, username=username, password=password, sock=sock,
                                dest_addr=dest_addr, src_addr=src_addr)
        else:
            scp_obj = ScpClient(host=host, port=port, username=username, password=password)
        return scp_obj

    def remove_session(self, alias: str, connect_type: str):
        if (alias, connect_type) in self.sessions:
            self.sessions[(alias, connect_type)].close()
            del self.sessions[(alias, connect_type)]


class ACUSession(metaclass=SingletonMeta):
    def __init__(self):
        self.sessions = {}
        self.scp_sessions = {}
        self.device_config_dict = {
            "host": decode_encrypt_string(ACU_CONSTANT.ACU_HOSTNAME),
            "port": int(decode_encrypt_string(ACU_CONSTANT.ACU_PORT)),
            "username": decode_encrypt_string(ACU_CONSTANT.ACU_USERNAME),
            "password": decode_encrypt_string(ACU_CONSTANT.ACU_PASSWORD),
        }

    def add_session(self, alias: str, connect_type: str) -> SshClient:
        """
        添加一个连接的session，如果不存在会创建一个连接保存在session中，如果存在会用已有session进行连接
        :param alias: 窗口别名
        :param connect_type: 连接方式，支持obd和vlan
        :return: SshClient连接对象
        """
        if (alias, connect_type) in self.sessions.keys():
            return self.sessions.get((alias, connect_type))
        else:
            host = self.device_config_dict.get('host')
            port = self.device_config_dict.get('port')
            username = self.device_config_dict.get('username')
            password = self.device_config_dict.get('password')
            if connect_type == "obd":
                src_addr = (get_bgm_hostname(connect_type), port)
                dest_addr = (host, port)
                sock = BgmSession().add_session(f'ACU_{alias}', connect_type).get_jump_client_connect(
                    dest_addr=dest_addr, src_addr=src_addr
                )
                ssh_obj = SshClient(host=host, port=port, username=username, password=password, sock=sock,
                                    dest_addr=dest_addr, src_addr=src_addr)
            else:
                ssh_obj = SshClient(host=host, port=port, username=username, password=password)
            self.sessions[(alias, connect_type)] = ssh_obj
            return ssh_obj

    def add_scp_session(self, connect_type: str) -> ScpClient:
        """
        添加一个连接的session，如果不存在会创建一个连接保存在session中，如果存在会用已有session进行连接
        :return: SshClient连接对象
        """
        host = self.device_config_dict.get('host')
        port = self.device_config_dict.get('port')
        username = self.device_config_dict.get('username')
        password = self.device_config_dict.get('password')
        if connect_type == "obd":
            src_addr = (get_bgm_hostname(connect_type), port)
            dest_addr = (host, port)
            BgmSession().remove_session('ACU_scp', connect_type)
            sock = BgmSession().add_session('ACU_scp', connect_type).get_jump_client_connect(
                dest_addr=dest_addr, src_addr=src_addr
            )
            scp_obj = ScpClient(host=host, port=port, username=username, password=password, sock=sock,
                                dest_addr=dest_addr, src_addr=src_addr)
        else:
            scp_obj = ScpClient(host=host, port=port, username=username, password=password)
        return scp_obj

    def remove_session(self, alias: str, connect_type: str):
        if (alias, connect_type) in self.sessions:
            self.sessions[(alias, connect_type)].close()
            del self.sessions[(alias, connect_type)]


class CDCQSession(metaclass=SingletonMeta):
    def __init__(self):
        self.sessions = {}
        self.scp_sessions = {}
        self.device_config_dict = {
            "host": decode_encrypt_string(CDCQ_CONSTANT.CDCQ_HOSTNAME),
            "port": int(decode_encrypt_string(CDCQ_CONSTANT.CDCQ_PORT)),
            "username": decode_encrypt_string(CDCQ_CONSTANT.CDCQ_USERNAME),
            "password": decode_encrypt_string(CDCQ_CONSTANT.CDCQ_PASSWORD),
        }

    def add_session(self, alias: str, connect_type: str) -> SshClient:
        """
        添加一个连接的session，如果不存在会创建一个连接保存在session中，如果存在会用已有session进行连接
        :param alias: 窗口别名
        :param connect_type: obd或者vlan连接
        :return: SshClient连接对象
        """
        if (alias, connect_type) in self.sessions.keys():
            return self.sessions.get((alias, connect_type))
        else:
            host = self.device_config_dict.get('host')
            port = self.device_config_dict.get('port')
            username = self.device_config_dict.get('username')
            password = self.device_config_dict.get('password')
            if connect_type == "obd":
                src_addr = (get_bgm_hostname(connect_type), port)
                dest_addr = (host, port)
                sock = BgmSession().add_session(f'CDCQ_{alias}', connect_type).get_jump_client_connect(
                    dest_addr=dest_addr, src_addr=src_addr
                )
                ssh_obj = SshClient(host=host, port=port, username=username, password=password, sock=sock,
                                    dest_addr=dest_addr, src_addr=src_addr)
            else:
                ssh_obj = SshClient(host=host, port=port, username=username, password=password)
            self.sessions[(alias, connect_type)] = ssh_obj
            return ssh_obj

    def add_scp_session(self, connect_type: str) -> ScpClient:
        """
        添加一个连接的session，如果不存在会创建一个连接保存在session中，如果存在会用已有session进行连接
        :return: SshClient连接对象
        """
        host = self.device_config_dict.get('host')
        port = self.device_config_dict.get('port')
        username = self.device_config_dict.get('username')
        password = self.device_config_dict.get('password')
        if connect_type == "obd":
            src_addr = (get_bgm_hostname(connect_type), port)
            dest_addr = (host, port)
            BgmSession().remove_session('CDCQ_scp', connect_type)
            sock = BgmSession().add_session('CDCQ_scp', connect_type).get_jump_client_connect(
                dest_addr=dest_addr, src_addr=src_addr
            )
            scp_obj = ScpClient(host=host, port=port, username=username, password=password, sock=sock,
                                dest_addr=dest_addr, src_addr=src_addr)
        else:
            scp_obj = ScpClient(host=host, port=port, username=username, password=password)
        return scp_obj

    def remove_session(self, alias: str, connect_type: str):
        if (alias, connect_type) in self.sessions:
            self.sessions[(alias, connect_type)].close()
            del self.sessions[(alias, connect_type)]


class NADSession(metaclass=SingletonMeta):
    def __init__(self):
        self.sessions = {}
        self.scp_sessions = {}
        self.device_config_dict = {
            "host": decode_encrypt_string(NAD_CONSTANT.NAD_HOSTNAME),
            "port": int(decode_encrypt_string(NAD_CONSTANT.NAD_PORT)),
            "username": decode_encrypt_string(NAD_CONSTANT.NAD_USERNAME),
            "password": decode_encrypt_string(NAD_CONSTANT.NAD_PASSWORD),
        }

    def add_session(self, alias: str, connect_type: str) -> SshClient:
        """
        添加一个连接的session，如果不存在会创建一个连接保存在session中，如果存在会用已有session进行连接
        :param alias: 窗口别名
        :param connect_type: obd或者vlan连接
        :return: SshClient连接对象
        """
        if (alias, connect_type) in self.sessions.keys():
            return self.sessions.get((alias, connect_type))
        else:
            host = self.device_config_dict.get('host')
            port = self.device_config_dict.get('port')
            username = self.device_config_dict.get('username')
            password = self.device_config_dict.get('password')
            if connect_type == "obd":
                src_addr = (get_bgm_hostname(connect_type), port)
                dest_addr = (host, port)
                sock = BgmSession().add_session(f'NAD_{alias}', connect_type).get_jump_client_connect(
                    dest_addr=dest_addr, src_addr=src_addr
                )
                ssh_obj = SshClient(host=host, port=port, username=username, password=password, sock=sock,
                                    dest_addr=dest_addr, src_addr=src_addr)
            else:
                ssh_obj = SshClient(host=host, port=port, username=username, password=password)
            self.sessions[(alias, connect_type)] = ssh_obj
            return ssh_obj

    def add_scp_session(self, connect_type: str) -> ScpClient:
        """
        添加一个连接的session，如果不存在会创建一个连接保存在session中，如果存在会用已有session进行连接
        :return: SshClient连接对象
        """
        host = self.device_config_dict.get('host')
        port = self.device_config_dict.get('port')
        username = self.device_config_dict.get('username')
        password = self.device_config_dict.get('password')
        if connect_type == "obd":
            src_addr = (get_bgm_hostname(connect_type), port)
            dest_addr = (host, port)
            BgmSession().remove_session('NAD_scp', connect_type)
            sock = BgmSession().add_session('NAD_scp', connect_type).get_jump_client_connect(
                dest_addr=dest_addr, src_addr=src_addr
            )
            scp_obj = ScpClient(host=host, port=port, username=username, password=password, sock=sock,
                                dest_addr=dest_addr, src_addr=src_addr)
        else:
            scp_obj = ScpClient(host=host, port=port, username=username, password=password)
        return scp_obj

    def remove_session(self, alias: str, connect_type: str):
        if (alias, connect_type) in self.sessions:
            self.sessions[(alias, connect_type)].close()
            del self.sessions[(alias, connect_type)]


class CDSOCSession(metaclass=SingletonMeta):
    def __init__(self):
        self.sessions = {}
        self.scp_sessions = {}
        self.device_config_dict = {
            "host": decode_encrypt_string(CD_SOC_CONSTANT.NAD_HOSTNAME),
            "port": int(decode_encrypt_string(CD_SOC_CONSTANT.NAD_PORT)),
            "username": decode_encrypt_string(CD_SOC_CONSTANT.NAD_USERNAME),
            "password": decode_encrypt_string(CD_SOC_CONSTANT.NAD_PASSWORD),
        }

    def add_session(self, alias: str, connect_type: str) -> SshClient:
        """
        添加一个连接的session，如果不存在会创建一个连接保存在session中，如果存在会用已有session进行连接
        :param alias: 窗口别名
        :param connect_type: obd或者vlan连接
        :return: SshClient连接对象
        """
        if (alias, connect_type) in self.sessions.keys():
            return self.sessions.get((alias, connect_type))
        else:
            host = self.device_config_dict.get('host')
            port = self.device_config_dict.get('port')
            username = self.device_config_dict.get('username')
            password = self.device_config_dict.get('password')
            if connect_type == "obd":
                src_addr = (get_bgm_hostname(connect_type), port)
                dest_addr = (host, port)
                sock = BgmSession().add_session(f'cd_soc_{alias}', connect_type).get_jump_client_connect(
                    dest_addr=dest_addr, src_addr=src_addr
                )
                ssh_obj = SshClient(host=host, port=port, username=username, password=password, sock=sock,
                                    dest_addr=dest_addr, src_addr=src_addr)
            else:
                ssh_obj = SshClient(host=host, port=port, username=username, password=password)
            self.sessions[(alias, connect_type)] = ssh_obj
            return ssh_obj

    def add_scp_session(self, connect_type: str) -> ScpClient:
        """
        添加一个连接的session，如果不存在会创建一个连接保存在session中，如果存在会用已有session进行连接
        :return: SshClient连接对象
        """
        host = self.device_config_dict.get('host')
        port = self.device_config_dict.get('port')
        username = self.device_config_dict.get('username')
        password = self.device_config_dict.get('password')
        if connect_type == "obd":
            src_addr = (get_bgm_hostname(connect_type), port)
            dest_addr = (host, port)
            BgmSession().remove_session('cd_soc_scp', connect_type)
            sock = BgmSession().add_session('cd_soc_scp', connect_type).get_jump_client_connect(
                dest_addr=dest_addr, src_addr=src_addr
            )
            scp_obj = ScpClient(host=host, port=port, username=username, password=password, sock=sock,
                                dest_addr=dest_addr, src_addr=src_addr)
        else:
            scp_obj = ScpClient(host=host, port=port, username=username, password=password)
        return scp_obj

    def remove_session(self, alias: str, connect_type: str):
        if (alias, connect_type) in self.sessions:
            self.sessions[(alias, connect_type)].close()
            del self.sessions[(alias, connect_type)]


def close_command(**kwargs):
    device_name = kwargs.get("device_name")
    if device_name is None:
        raise Exception(f'device_name is {device_name}')
    alias = kwargs.get("alias", '')
    connect_type = kwargs.get("connect_type", 'vlan')
    SessionManager(device_name).get_session(alias, connect_type).close()


def command_send(**kwargs):
    """
    阻塞式执行ssh连接，发送一个命令，等待返回
    :param kwargs:
        device_name: 设备名称，目前可填写BGM,TCAM,ACU,CDCQ,NAD,CD_SOC，表示会自动登录到BGM,TCAM,ACU,CDCQ,NAD,CD_SOC
        alias: 默认为空，交互式窗口别名，其他地方调用时建议指定别名，不然会与框架默认运行的窗口相互重叠
        expect: str|list，检查期望出现的值，命令返回中如果出现期望值，将会停止
        unexpect: str|list，检查不期望出现的值，命令返回中如果出现期望值，将会停止，如果没有期望值会等到超时时间退出或者终端执行退出
        timeout: int，超时时间，如果期望值一直不出现，等到超时时间时会停止，注意这个停止只是command_send停止，终端打印并不会停止，如果想让终端打印停止(例如tail)，需要发送\x03(ctrl c)或者kill命令
        cmd: str，命令，不输入命令则会报错
        callback: 回调函数，对命令返回的原始终端打印进行处理
        log_print: 对命令返回的原始终端打印是否记录在日志中进行打印
        connect_type: 连接类型，obd或者vlan
    :return: SshClient连接对象
    """
    device_name = kwargs.get("device_name")
    if device_name is None:
        raise Exception(f'device_name is {device_name}')
    alias = kwargs.get("alias", '')
    expect = kwargs.get("expect")
    if expect and isinstance(expect, str):
        expect = [expect]
    elif expect is None or isinstance(expect, List):
        expect = expect
    else:
        raise Exception('expect只能是str或者list')
    unexpect = kwargs.get("unexpect")
    if unexpect and isinstance(unexpect, str):
        unexpect = [unexpect]
    elif unexpect is None or isinstance(unexpect, List):
        unexpect = unexpect
    else:
        raise Exception('unexpect只能是str或者list')
    timeout = kwargs.get("timeout", 60)
    cmd = kwargs.get("cmd")
    if cmd is None:
        raise Exception(f'cmd is {cmd}')
    callback = kwargs.get('callback')
    log_print = kwargs.get('log_print', True)
    connect_type = kwargs.get('connect_type', 'vlan')
    if connect_type not in ["obd", "vlan"]:
        raise Exception(f'connect_type only obd or vlan')
    return SessionManager(device_name).get_session(alias, connect_type).execute_command(
        expect=expect,
        unexpect=unexpect,
        timeout=timeout,
        cmd=cmd,
        callback=callback,
        log_print=log_print,
        connect_type=connect_type
    )


def file_upload(**kwargs):
    """
    上传文件，目前由于权限问题，建议remote_path设置为/tmp
    :param kwargs:
        device_name: 设备名称，目前可填写BGM,TCAM,ACU,CDCQ，表示会自动登录到BGM,TCAM,ACU,CDCQ
        alias: 默认为空
        local_path: str，本地文件路径
        remote_path: str，远程文件路径
        connect_type: 连接类型，obd或者vlan
    :return: ScpClient连接对象
    """
    device_name = kwargs.get("device_name")
    if device_name is None:
        raise Exception(f'device_name is {device_name}')
    local_path = kwargs.get("local_path")
    remote_path = kwargs.get("remote_path")
    connect_type = kwargs.get('connect_type', 'vlan')
    if connect_type not in ["obd", "vlan"]:
        raise Exception(f'connect_type only obd or vlan')
    return SessionManager(device_name).get_scp_session(connect_type).put(
        local_path=local_path,
        remote_path=remote_path
    )


def file_download(**kwargs):
    """
    下载文件
    :param kwargs:
        device_name: 设备名称，目前可填写BGM,TCAM,ACU,CDCQ，表示会自动登录到BGM,TCAM,ACU,CDCQ
        local_path: str，本地文件路径
        remote_path: str，远程文件路径
        connect_type: 连接类型，obd或者vlan
    :return: ScpClient连接对象
    """
    device_name = kwargs.get("device_name")
    if device_name is None:
        raise Exception(f'device_name is {device_name}')
    local_path = kwargs.get("local_path")
    remote_path = kwargs.get("remote_path")
    connect_type = kwargs.get('connect_type', 'obd')
    if connect_type not in ["obd", "vlan"]:
        raise Exception(f'connect_type only obd or vlan')
    return SessionManager(device_name).get_scp_session(connect_type).get(
        local_path=local_path,
        remote_path=remote_path
    )


if __name__ == '__main__':
    # get_obd_ip()
    command_send(device_name='TCAM', cmd="ls")
    # time.sleep(5)
    # status, ret = command_send(device_name='BGM', cmd="tail")
    # print(ret)
    # file_download(device_name='TCAM', local_path='/root/soa_name.txt', remote_path='/tmp/')
    # file_upload(device_name='BGM', local_path='/root/xdj/sat/.uuid', remote_path='/tmp/jiduer/')
    # status, code = command_send(device_name='TCAM', cmd="cd ../")

    # time.sleep(5)
    # command_send(device_name='BGM', alias=2, cmd="ls")
    # print(status)
    # print([code])
