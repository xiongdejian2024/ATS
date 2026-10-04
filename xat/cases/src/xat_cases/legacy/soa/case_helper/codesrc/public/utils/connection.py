#!/usr/bin/python3
# -*- coding=utf-8 -*-
# (C) Copyright Jidu Auto 2023-2023.
# @author: Edison

'''
架构元素：code/public/utils

dependencies:
    python(>=3.5)
    fabric(>=3.0)
    scp(>=0.14.5)
    adb_shell(>=0.4.3)
'''

import os
import stat
from adb_shell import constants
from fabric import Connection
from scp import SCPClient
from adb_shell.adb_device import AdbDeviceTcp
from .log import logger


class RemoteTools(Connection):
    '''
    默认的fabric是基于paramiko的，上传/下载文件是基于sftp协议的，
    当前已支持scp（文件夹传输）
    '''

    def __init__(
        self,
        host,
        user=None,
        port=None,
        config=None,
        gateway=None,
        forward_agent=None,
        connect_timeout=None,
        connect_kwargs=None,
        inline_ssh_env=None,
    ):
        super().__init__(
            host, user, port, config, gateway, forward_agent, connect_timeout, connect_kwargs, inline_ssh_env
        )
        self.scp_client = None

    def check_conn(self):
        try:
            self.run('uname')
            logger.info(f'连接到 {self.host} 成功')
        except Exception as e:
            logger.warning(f'连接到 {self.host} 失败，详细信息：{e}')
            self.open()

    def get(self, *args, **kwargs):
        '''
        下载文件（src：remote，dst：local），举例：
            get(remote_path, local_path=local_path)
        '''
        return self._getdir(*args, **kwargs)

    def put(self, *args, **kwargs):
        '''
        上传文件（src：local，dst：remote），举例：
            put(local_path, remote_path=remote_path)
        @params use_sftp: 如果为True则使用sftp，否则使用scp
        '''
        local_path = args[0]
        if self._is_dir(local_path):
            return self._putdir(*args, **kwargs)

        use_sftp = False
        if 'use_sftp' in kwargs:
            use_sftp = kwargs['use_sftp']

        if use_sftp:
            return super().put(*args, **kwargs)
        self._init_scp()
        return self.scp_client.put(local_path, kwargs['remote_path'])

    def _getdir(self, *args, **kwargs):
        self._init_scp()
        try:
            self.scp_client.get(kwargs['remote_path'], kwargs['local_path'], recursive=True)
        except Exception as e:
            try:
                self._init_scp()
                self.scp_client.get(kwargs['remote_path'], kwargs['local_path'], recursive=True)
            except Exception as e:
                print(f'Warn:{e}')

    def _putdir(self, *args, **kwargs):
        self._init_scp()
        self.scp_client.put(args[0], kwargs['remote_path'], recursive=True)

    def _init_scp(self):
        if self.scp_client is None:
            self.scp_client = SCPClient(self.transport)

    def _is_dir(self, path, remote=False):
        if remote:
            res = self.run(f'test -d {path}', warn=True)
            return res.ok
        return os.path.isdir(path)

    def __del__(self):
        if self.scp_client is not None:
            self.scp_client.close()
        self.close()


class RemoteToolsAdb(AdbDeviceTcp):
    '''
    支持adb操作，示例：
        adb = RemoteToolsAdb(ip, port)
        adb.connect()

        res = adb.shell('ls -l')
        adb.close()
    '''

    def __init__(self, host, port=5555, default_transport_timeout_s=None, banner=None):
        super().__init__(host, port, default_transport_timeout_s, banner)

    def pull(
        self,
        device_path,
        local_path,
        progress_callback=None,
        transport_timeout_s=None,
        read_timeout_s=constants.DEFAULT_READ_TIMEOUT_S,
        recursive=False,
    ):
        '''
        @desp: override
        @param recursive: 是否是文件夹
        '''
        if recursive:
            return self._pull_folder(device_path, local_path)
        return super().pull(device_path, local_path, progress_callback, transport_timeout_s, read_timeout_s)

    def _pull_folder(self, device_path, local_path):
        '''
        @desp：扩展对文件夹拉取的支持
        '''
        local_path = os.path.join(local_path, os.path.basename(device_path))
        if not os.path.exists(local_path):
            os.makedirs(local_path, exist_ok=True)
        for file in self.list(device_path):
            _filename = file.filename.decode()
            if _filename.startswith('.'):
                continue
            _remote_file = f"{device_path}/{_filename}"
            _local_file = os.path.join(local_path, _filename)
            if stat.S_ISDIR(file.mode):
                self._pull_folder(_remote_file, _local_file)
            else:
                super().pull(_remote_file, _local_file)



if __name__ == '__main__':
    # ------------------------------------------------------------------------------------------
    # test fabric
    host = '172.18.128.149'
    port = 22
    user = ''
    passwd = ''

    c = RemoteTools(host=host, user=user, port=port, connect_kwargs={'password': passwd})
    print(c.is_connected)

    c.run('pwd', env={})
    c.check_conn()
    print(c.is_connected)
    c.sudo('chmod a+r /log/ -R', password=passwd)
    local_path = ''
    remote_path = ''

    log_file = []
    if not os.path.exists(local_path):
        os.makedirs(local_path, exist_ok=True)
    for file in str(c.run(f'ls {remote_path}')).split():
        if 'log' in file and file[-1].isdigit() or 'bootes' in file or 'coredump' in file:
            log_file.append(file)
    for f in log_file:
        l_path = os.path.join(local_path, f)
        r_path = remote_path + '/' + f
        c.get(remote_path=r_path, local_path=l_path)
    c.close()
    # c.get(remote_path=remote_path, local_path=local_path)
