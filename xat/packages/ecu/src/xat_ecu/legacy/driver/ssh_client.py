# -*- coding: utf-8 -*-
"""
@File        : ssh_client.py
@Author      : jinhui.zhao@jiduauto.com
@Time        : 2022/03/07 4:01 PM
@Description : ssh basic function

"""
import socket
import time
from time import sleep
import threading
import re
import paramiko
import sys
import os
from xat_ecu.legacy.common.logger import logger

project_root = __import__("xat_ecu.resources", fromlist=["LEGACY_ROOT"]).LEGACY_ROOT.as_posix()


class SSHClient(object):
    def __init__(
        self,
        hostname,
        port=22,
        username='root',
        password=None,
        private_key=None,
        timeout=60,
        max_retry_time=300,
    ):
        """
        Constructor of SSHClient.

        :param hostname: hostname address of remote devices
        :param port: ssh service port, default is 22
        :param username: user name of remote device, default is 'root'
        :param password: password of remote device
        :param private_key: private key of remote device
        :param timeout: timeout of paramiko
        :param max_retry_time: max retry time for ssh, default is 300s
        """
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.private_key = private_key
        self.max_retry_time = max_retry_time
        self.timeout = timeout
        self.is_closed = False
        self.client = None
        self.transport = None
        self.connect()

    def __del__(self):
        """
        Close the connection created previously, if not closed by user.

        :return:
        """
        if not self.is_closed:
            self.client.close()

    def connect(self):
        """
        Connect to host.

        :return:
        """
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if not self.password:
            logger.info('Connect to %s' % self.hostname)
            self.client.connect(
                self.hostname,
                self.port,
                username=self.username,
                key_filename=self.private_key,
                timeout=self.timeout,
            )
        else:
            logger.info('Connect to %s' % self.hostname)
            self.client.connect(
                self.hostname,
                self.port,
                username=self.username,
                password=self.password,
                timeout=self.timeout,
            )

    def is_connected(self):
        """
        Get connection status.

        :return: True or False
        """
        try:
            return self.client.get_transport().is_active()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_client.py")
            logger.error('Exception: %s' % str(e))
            return False

    def is_alive(self):
        """
        Check whether socket is connected.

        :return: True or False
        """
        try:
            self.exec_cmd('\r')
            return True
        except (socket.error, EOFError):
            return False

    def re_connect(self):
        """
        Reconnect ssh server.

        :return: the result of reConnection
        """
        wait_time = 1
        sum_time = 0
        while not self.is_connected():
            if sum_time >= self.max_retry_time:
                logger.debug('max_retry_time = ' + str(self.max_retry_time))
                logger.debug(
                    'SSH retry time has amount to ' + str(sum_time) + ', give up'
                )
                raise SSHFailException('SSH still fail after retry')
            try:
                self.connect()
            except paramiko.ssh_exception.SSHException as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_client.py")
                logger.error('SSH connect exception: ' + str(e))
                logger.debug('Sleep ' + str(wait_time) + 's before retry...')
            time.sleep(wait_time)
            sum_time = sum_time + wait_time
            wait_time = wait_time * 2
        return True

    def close(self):
        """
        Close the connection.

        :return:
        """
        self.client.close()
        self.is_closed = True

    def _exec(self, cmd):
        """
        Execute command in remote server, return stdin, stdout and stderr directly,
        without waiting for the command to complete.

        :param cmd: str, the command to be run, like 'ls -l'
        :return: a tuple containing (stdin, stdout, stderr)
        """
        logger.debug('Executing ' + cmd + ' on host ' + self.hostname)

        if not self.re_connect():
            logger.error('Cannot ssh to host ' + self.hostname)
            return None, None, None

        stdin, stdout, stderr = self.client.exec_command(cmd, get_pty=False)

        logger.debug('Function exec_command returns')
        return stdin, stdout, stderr

    def exec_cmd(self, cmd, timeout=60, wait_time=1.0):
        """
        Execute command in remote server, return until the command completes.
        :param timeout: avoid hangs, give the timeout param, default is 60s
        :param cmd: cmd str, such as 'ls -l'
        :return: A tuple containing stdout and stderr
        """
        try:
            _, stdout, stderr = self._exec(cmd)
        except SSHFailException as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_client.py")
            logger.error(
                'Cannot ssh to host %s in exec_cmd, err: %s' % (self.hostname, e)
            )
            raise SSHFailException
        timeout = timeout
        time.sleep(wait_time)
        for t in range(0, timeout + 5, 5):
            if not stdout.channel.eof_received and not stdout.channel.closed:
                logger.info("Wait {} seconds, no response with cmd:{}".format(t, cmd))
                time.sleep(5)
            else:
                break
        else:
            logger.error(
                "It seems process hangs due to execute:{}, please help check".format(
                    cmd
                )
            )
            try:
                # If get unhand except, it may be that dut is rebooted with uds hard reset
                self.client.exec_command("ls")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_client.py")
                logger.error(e)
                self.re_connect()
            else:
                raise SSHFailException

        # Due to sometimes it will meet errors when decode bytes to str, so add the errors parameters equals replace
        # That means when decode throw a error, it will replace the un-decode bytes to fff
        out_btyes = stdout.read()
        err_bytes = stderr.read()
        out = ''
        err = ''
        try:
            out = out_btyes.decode(errors='ignore').strip()
            err = err_bytes.decode(errors='ignore').strip()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_client.py")
            logger.error("----" + "*" * 10 + "----")
            logger.error("It meet error when try to decode output message to str")
            logger.error("output is {}".format(out))
            logger.error("error is {}".format(err))
        return out, err

    # def sudo_exec_cmd(self, cmd, sudo_password=None, timeout=60, wait_time=1.0):
    #     """
    #     Execute cmd in remote server with sudo mode, return until the cmd complete.

    #     :param cmd: str, such as 'ls -l'
    #     :param sudo_password: sudo password
    #     :param timeout: avoid hangs, give the timeout param, default is 60s
    #     :return: A tuple containing stdout and stderr
    #     """
    #     if not sudo_password:
    #         sudo_password = self.password
    #     try:
    #         # stdin, stdout, stderr = self._exec("sudo -k -s -p '' %s" % cmd)  会没有返回值
    #         stdin, stdout, stderr = self._exec("sudo -k -s -p ''")
    #         stdin.write(sudo_password + "\n")
    #         stdin.flush()
    #         stdin.write(cmd + "\n")
    #         stdout.flush()  # stdout 没有想要的返回值

    #     except SSHFailException as e:
    #         logger.error(
    #             'Cannot ssh to host %s in sudo_exec_cmd, err: %s' % (self.hostname, e)
    #         )
    #         raise SSHFailException

    #     time.sleep(wait_time)
    #     for t in range(0, timeout + 5, 5):
    #         if not stdout.channel.eof_received and not stdout.channel.closed:
    #             logger.info("Wait {} seconds, no response with cmd:{}".format(t, cmd))
    #             time.sleep(5)
    #         else:
    #             break
    #     else:
    #         logger.error(
    #             "It seems process hangs due to execute:{}, please help check".format(
    #                 cmd
    #             )
    #         )
    #         try:
    #             # If get unhand except, it may be that dut is rebooted with uds hard reset
    #             self.client.exec_command("ls")
    #         except Exception as e:
    #             logger.error(e)
    #             self.re_connect()
    #         else:
    #             logger.info("Close the stdout and stderr channel")
    #             stdout.channel.close()
    #             stderr.channel.close()
    #     # Due to sometimes it will meet errors when decode bytes to str, so add the errors parameters equals replace
    #     # That means when decode throw a error, it will replace the un-decode bytes to fff
    #     out_btyes = stdout.read()
    #     err_bytes = stderr.read()
    #     out = ''
    #     err = ''
    #     try:
    #         out = out_btyes.decode(errors='ignore').strip()
    #         err = err_bytes.decode(errors='ignore').strip()
    #     except Exception as e:
    #         logger.error("----" + "*" * 10 + "----")
    #         logger.error("It meet error when try to decode output message to str")
    #         logger.error("output is {}".format(out))
    #         logger.error("error is {}".format(err))

    #     return out, err

    def sudo_exec_cmd(
        self,
        cmd: str,
        sudo_password=None,
        timeout=60,
        wait_time=1.0,
        end_str=('# ', '$ ', '? ', '% '),
    ):
        # 为了显示输出，将invoke_shell 封装
        if not sudo_password:
            sudo_password = self.password

        sudo_invoke_shell = self.client.invoke_shell()
        sleep(0.1)

        sudo_cmd = "sudo -k -s -p ''" + '\n'
        sudo_invoke_shell.send(sudo_cmd)
        sleep(0.1)
        sudo_invoke_shell.send(sudo_password + "\n")
        sleep(0.1)
        buffer = sudo_invoke_shell.recv(1024 * 4).decode()
        # logger.info(buffer)

        if cmd.endswith('\n'):
            sudo_invoke_shell.send(cmd)
        else:
            sudo_invoke_shell.send(cmd + '\n')

        res = self.__recv(sudo_invoke_shell, end_str, timeout)

        # 去掉开头的命令   和  结尾的 @jidu-bgm-mars1:
        res_list = res.split("\n")

        outmsg = ""
        for res_str in res_list[1:]:
            if ("@jidu-bgm-mars1:" not in res_str) and ("#" not in res_str):
                outmsg += res_str + "\n"
        outmsg = outmsg.strip("\r\n")
        # logger.info(outmsg)
        sudo_invoke_shell.close()
        errmsg = ""  # 统一化适配,这里没有实际意义，如果有errmsg也在res里

        return outmsg, errmsg

    def __recv(self, channel, end_str, timeout) -> str:
        result = ''
        out_str = ''
        max_wait_time = timeout * 1000
        channel.settimeout(0.05)
        while max_wait_time > 0:
            try:
                out = channel.recv(1024 * 1024).decode()

                if not out or out == '':
                    continue
                out_str = out_str + out
                # logger.info(out_str)
                match, result = self.__match(out_str, end_str)
                if match is True:
                    return result.strip()
                else:
                    max_wait_time -= 50
            except socket.timeout:
                max_wait_time -= 50

        raise Exception('recv data timeout')

    def __match(self, out_str: str, end_str: list) -> (bool, str):
        result = out_str
        for it in end_str:
            if result.endswith(it):
                return True, result
        return False, result

    class interactive_ssh(threading.Thread):
        def __init__(
            self, client, cmd, callbak, timeout=300, password=None, if_string=True
        ):
            threading.Thread.__init__(self)
            self.loop = True
            self.local_time = None
            self.cmd = cmd
            self.callbak = callbak
            self.timeout = timeout
            self.password = password
            self.client = client
            self.if_string = if_string

        def stop_loop(self):
            self.loop = False

        def if_running(self):
            if self.loop:
                return True
            return False

        def reset_timeout(self):
            self.local_time = time.time()

        @staticmethod
        def get_all_buffer(chan_shell, type_str):
            ret_str = b''
            if getattr(chan_shell, type_str + '_ready'):
                while True:
                    try:
                        ret_str += getattr(chan_shell, type_str)(1024)
                    except socket.timeout as e:
                        break
                    finally:
                        pass
            return ret_str

        def run(self):
            chan_shell = self.client.invoke_shell(width=200)
            if self.password:
                chan_shell.sendall('sudo su\n' + self.password + '\n')
                time.sleep(1)
            while True:
                if chan_shell.send_ready():
                    chan_shell.sendall(self.cmd + "\n")
                    break
            # chan_shell.exec_command(bytes(cmd, 'utf-8'))
            chan_shell.setblocking(0)
            out_str = b''
            err_str = b''
            self.local_time = time.time()
            all_start = b''
            only_once = True
            while time.time() < self.local_time + self.timeout:
                if not self.loop:
                    break
                err_temp = self.get_all_buffer(chan_shell, 'recv_stderr')
                out_temp = self.get_all_buffer(chan_shell, 'recv')
                if only_once:
                    all_start += out_temp
                    all_split = re.split(
                        rb'[^\r\n]{1}' + bytes(self.cmd, encoding='utf-8') + rb'\r\n',
                        all_start,
                        1,
                    )
                    if len(all_split) <= 1:
                        time.sleep(2)
                        continue
                    else:
                        out_temp = all_split[1]
                        all_start = all_split[0]
                        only_once = False
                    # if re.search(bytes(self.cmd,encoding='utf-8')+b'\r\n', all_start) != None:
                    #     out_temp = all_start.split(bytes(self.cmd,encoding='utf-8')+b'\r\n', 1)[1]
                    #     all_start = all_start.split(bytes(self.cmd,encoding='utf-8')+b'\r\n', 1)[0]
                    #     only_once = False
                    # else:
                    #     time.sleep(2)
                    #     continue
                if out_temp or err_temp:
                    try:
                        if self.if_string:
                            err_temp = err_temp.decode(errors='ignore')
                            out_temp = out_temp.decode(errors='ignore')
                        self.callbak((self.cmd, err_temp, out_temp))
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/ssh_client.py")
                        logger.error(str(e))
                time.sleep(1)
            else:
                logger.error("timeout for cmd:" + self.cmd)
                self.stop_loop()
            chan_shell.close()
            logger.info("stopped about cmd:" + self.cmd)

    def start_interactive_cmd(
        self, cmd, callbak, timeout=300, password=None, if_string=True
    ):
        interactive_t = self.interactive_ssh(
            self.client, cmd, callbak, timeout, password, if_string
        )
        interactive_t.start()
        return interactive_t

    @staticmethod
    def stop_interactive_cmd(interactive_t):
        interactive_t.stop_loop()
        time.sleep(3)

    def is_proc_exist(self, pid):
        """
        Check if a process exist in remote server.

        :param pid: int, PID of the process in remote server
        :return: True if process exists, false otherwise
        """
        stdout, stderr = self.exec_cmd('ps -ef | grep %s | grep -v grep' % pid)
        i = 0
        for line in stdout:
            logger.debug('... ' + line.strip('\n'))
            i += 1

        if i > 0:
            return True
        else:
            return False

    def is_file_contain(self, file_path, target_str):
        """
        Check if target_str is contained in a file at remote_path in remote host.

        :param file_path: path of file in remote server
        :param target_str: string to be searched
        :return:
            on error: return False
            on success: return True
        """
        stdout, stderr = self.exec_cmd('cat %s | grep %s' % (file_path, target_str))
        i = 0
        for line in stdout:
            logger.debug('... ' + line.strip('\n'))
            i += 1

        if i > 0:
            return True
        else:
            return False

    def kill_process(self, pid):
        """
        Kill a process in remote host.

        :param pid: int, PID of the process in remote server
        :return: None
        """
        logger.info('Killing process with pid %s' % str(pid))
        self.exec_cmd('kill -9 ' + pid)

    def tar_folder(self, tar_folder, tar_file):
        """
        Tar and zip folder as a tar.gz file.

        :param tar_folder: target folder which need to tar
        :param tar_file: new generated tar.gz file
        :return:
            on error: return False
            on success: return tar.gz file
        """
        cmd = 'tar -Pzcvf %s %s --warning=no-file-changed' % (tar_file, tar_folder)
        stdout, stderr = self.exec_cmd(cmd)
        if stderr:
            logger.error('tar_folder failed: %s' % stderr)
            return False
        else:
            return True

    def fetch_file(self, remote_path, local_path):
        """
        Fetch file with path remote_path on remote server and save to local_path.

        :param remote_path: str, path of the file to be fetched in remote server
        :param local_path: str, path of the file to be stored in local host
        :return: True
        """
        ftp = self.client.open_sftp()
        ftp.get(remote_path, local_path)
        ftp.close()
        logger.info('fetch %s to local %s' % (remote_path, local_path))
        return True

    def put_file(self, local_path, remote_path):
        """
        Put file with path remote_path on remote server and save to local_path.

        :param local_path: str, path of the file to be stored in local host
        :param remote_path: str, path of the file to be fetched in remote server
        :return: True
        """
        ftp = self.client.open_sftp()
        ftp.put(local_path, remote_path)
        ftp.close()
        return True


class SSHFailException(Exception):
    """
    An SSH fail even having retried to ssh to the server
    """

    def __init__(self, value='SSH Fail'):
        self.value = value

    def __str__(self):
        return repr(self.value)


if __name__ == '__main__':
    ssh = SSHClient("172.18.128.73", username="root", password=__import__("os").environ.get('XAT_CREDENTIAL_ECU__DRIVER_SSH_CLIENT_PY_PASSWORD', ""))
    ssh.invoke_shell()
    outmsg, errmsg = ssh.exec_cmd("pwd;ls -l")
    print(outmsg)
