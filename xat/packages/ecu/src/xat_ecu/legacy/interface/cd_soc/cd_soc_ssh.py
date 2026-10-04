#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :cd_soc_ssh.py
@Time         :2024/10/29 14:07
@Author       :dejian.xiong@jiduauto.com
@Description  :
"""
import os
import threading
import time

from xat_ecu.legacy.common.file_handle import ecu_simulator_abspath
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.driver.ssh_interface import command_send, file_download, file_upload, set_command_run_flag, \
    get_command_run_flag


class CD_SOC_SSH:
    def __init__(self, connect_type='vlan'):
        self.CD_SOC = 'CD_SOC'
        self.connect_type = connect_type

    def type_commands(self, commands, timeout=60, **kwargs):
        ct = kwargs.get('connect_type')
        if ct is not None:
            connect_type = ct
        else:
            connect_type = self.connect_type
        status, outmsg = command_send(
            device_name=self.CD_SOC,
            cmd=commands,
            timeout=timeout,
            connect_type=connect_type,
            **kwargs)
        logger.info(f'{commands}执行结果为:{outmsg}')
        return outmsg
    
    def _init_cd_soc_tcpdump(self, local_path=None, cd_soc_path='/data/', **kwargs):
        """
        先推包到tmp 下，然后解压到 cd_soc_path 路径下
        @param local_path: 工具路径 如 /root/dbg-utils.tar.bz2
        @param cd_soc_path: 最后解压到那个路径下，建议 data 下
        @param kwargs:
        @return:
        """
        if local_path is None:
            local_path = os.path.join(os.path.dirname(__file__), 'dbg-utils.tar.bz2')
        # 推送 工具到 cd_soc 内 tmp 下
        connect_type = kwargs.get('connect_type', 'vlan')
        if "dbg-utils.tar.bz2" not in self.type_commands('ls /tmp/', timeout=2):
            logger.info(f"推送 debug 工具{local_path}到cd_soc tmp 下面")
            self.scp_local_file_to_cd_soc(local_path=local_path, cd_soc_path='/tmp/', connect_type=connect_type)

        logger.info(f"解压 工具 到cd_soc {cd_soc_path}下面")
        cmd = kwargs.get('cmd', f'tar xjf /tmp/dbg-utils.tar.bz2 -C {cd_soc_path}')
        logger.info("开始===》》》解压包")
        self.type_commands(commands=cmd)
        logger.info("解压包===》》》完成")
        self.type_commands("cd /data;cp dbg-utils/bin/tcpdump ./;chmod +x tcpdump", timeout=2)

    def delete_cd_soc_tcpdump_file(self, cd_soc_log_name="*.pcap", path='/update/', **kwargs):
        """
        删除 cd_soc 内部 tcpdump 文件
        @param cd_soc_log_name: 要删除的w
        @param path: 文件所在路径
        @param kwargs:
        @return:
        """
        if cd_soc_log_name.endswith('pcap'):
            pass
        elif cd_soc_log_name.endswith('*'):
            pass
        else:
            cd_soc_log_name = cd_soc_log_name + "*"
        file_path = os.path.join(path, cd_soc_log_name)
        cmd = f"rm -f {file_path}"
        logger.info(f"删除cd_soc  {file_path}")
        self.type_commands(commands=cmd, timeout=5, **kwargs)
        logger.info(f"删除cd_soc  {file_path} 成功")
    
    def push_file_to_cd_soc_data(self, file_path, cd_soc_path="/data/", **kwargs):
        '''
        把文件推送到 cd_soc 的 cd_soc_path 路径下
        @param file_path:
        @param cd_soc_path:
        @return:
        '''
        # 最多尝试推送次数，默认三次
        retry_times = kwargs.get("retry_times", 3)
        file_name = os.path.basename(file_path)

        for i in range(retry_times):
            connect_type = kwargs.get('connect_type', 'vlan')
            self.scp_local_file_to_cd_soc(file_path, cd_soc_path=cd_soc_path, connect_type=connect_type)
            # 判断是否有 文件
            cmd = f"ls {cd_soc_path}"
            ret = self.type_commands(cmd)
            name_list = ret.split()
            logger.warning(f"name_List=》》{name_list}")
            if file_name not in name_list:
                if i == 2:
                    assert 0, f"{file_name} 未上传成功"
                time.sleep(1)
            else:
                return
    
    def scp_cd_soc_log_to_local(self, cd_soc_log_name, log_path='/root/cd_soc_log', save_log_name=None, del_flag=False,
                             **kwargs):
        """
         把 cd_soc 的日志 拉取到本地
        @param cd_soc_log_name:  拉取的是单个文件，或者压缩包，不能是文件夹
        @param log_path: 保存到本地的文件路径
        @param save_log_name: 保存到本地的文件名称 会加上时间戳
        @param del_flag: 是否删除原文件
        @return:
        """
        # 取单个文件 单个文件的名字
        cd_soc_log_path = kwargs.get("path", "/update")
        connect_type = kwargs.get('connect_type', 'vlan')

        log_time = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime(time.time()))
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        logger.info(f"获取单个文件名字为{save_log_name}")
        if save_log_name is None:
            save_log_name = cd_soc_log_name

        name = f"{log_time}_{save_log_name}"
        logger.info(f"获取单个文件名字为{name}")

        file_path = os.path.join(log_path, name)
        logger.info(f"生成的文件路径为==》》{file_path}")

        full_path = os.path.join(cd_soc_log_path, cd_soc_log_name)
        file_download(device_name=self.CD_SOC, remote_path=f'{full_path}', local_path=file_path, connect_type=connect_type)
        logger.info(f"cd_soc 的日志 已经取出，路径为==》》》{file_path}")
        if del_flag:
            remote_path = os.path.join(cd_soc_log_path, cd_soc_log_name)
            cmd = f"rm -f {remote_path}"
            logger.info(f"删除cd_soc  {remote_path}")
            self.type_commands(commands=cmd, timeout=5)
            logger.info(f"删除cd_soc  {remote_path} 成功")
        return file_path

    def scp_local_file_to_cd_soc(self, local_path, cd_soc_path='/tmp/', **kwargs):
        """
        把 本地 文件推送到cd_soc tmp 下
        @param local_path:  上位机的路径  如 "/root/cd_soc_log/"
        @param cd_soc_path:
        @param connect_type:
        @return:
        """
        self.type_commands("ls")  # 超时60s，可以防止重启后直接调用file_upload，未进行等待重连ssh，直接判ssh连接失败
        connect_type = kwargs.get('connect_type', 'vlan')
        file_upload(device_name=self.CD_SOC, local_path=local_path, remote_path='/tmp/', connect_type=connect_type)
        if cd_soc_path not in ["/tmp/", "/tmp"]:
            name = [i for i in local_path.split('/') if i.split()][-1]
            if os.path.isdir(local_path):
                cmd = f"mv -r /tmp/{name} {cd_soc_path}"
            else:
                cmd = f"mv /tmp/{name} {cd_soc_path}"
            try:
                logger.info(f"从cd_soc /tmp下移动文件{name}或者文件夹到cd_soc {cd_soc_path}下")
                self.type_commands(commands=cmd)
                logger.info(f"从cd_soc /tmp下移动文件{name}或者文件夹到cd_soc {cd_soc_path}下完成 ")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/cd_soc/cd_soc_ssh.py")
                logger.error(f"从cd_soc /tmp下移动文件{name}或者文件夹到cd_soc {cd_soc_path}下失败 {str(e)}")
    def _tar_debug_utils(self, **kwargs):
        """
        解压工具包
        首先把工具包推到 tmp 目录下，其他目录不一定有权限
        把工具包解压到 data 下面 （重启不会丢失，在tmp下重启会丢失，在update下访问不到）
        @param kwargs:
        @return:
        """
        cmd = kwargs.get('cmd', 'tar xjf /tmp/dbg-utils.tar.bz2 -C /data/')
        logger.info("开始===》》》解压包")
        self.type_commands(commands=cmd)
        logger.info("解压包===》》》完成")

    def start_cd_soc_tcpdump(self, name="cd_soc_", iface="eth0.5", **kwargs):
        """
        开启 cd_soc 内部抓包
        @param name:  抓包存储 文件名 ，最后会加上时间
        @param kwargs:
        @return:
        """
        # 抓包指令
        cmd = kwargs.get('cmd', None)
        # 保存路径，默认保存在cd_soc 里面的 /log 下
        path = kwargs.get("path", "/update")
        # 抓包长度
        eth_len = kwargs.get("eth_len", 0)
        otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))
        save_name = f"{name}{otherStyleTime}.pcap"
        file_path = os.path.join(path, save_name)
        # 抓包 指令
        if cmd is None:
            _path = os.path.join(ecu_simulator_abspath, "interface/cd_soc")
            #connect_type = kwargs.get('connect_type', 'vlan')
            #self.push_file_to_cd_soc_data(os.path.join(_path, "tcpdump"), connect_type=connect_type)
            cmd = f'cd /data/;tcpdump -i {iface} -vvv -w {file_path}'
            if eth_len:
                cmd += f" -s {eth_len}"
        # 检查包是否存在，如果不存在，或者大小异常，则重新推送tcpdump至cd_soc内
        #if "tcpdump" not in self.type_commands('ls /data/', timeout=2):
        #    logger.info(f"/data/目录下 没有找到tcpdump文件，重新推送tcpdump至cd_soc内")
        #    self._init_cd_soc_tcpdump()  # 开启抓包前，推送tcpdump至cd_soc内
        #else:
        #    if "5.6M" not in self.type_commands('du -sh /data/tcpdump', timeout=2):
        #        logger.info(f" /data/目录下的tcpdump文件大小异常，重新推送tcpdump至cd_soc内")
        #        self._init_cd_soc_tcpdump()
        #    else:
        #        logger.info(f"tcpdump 已在/data/目录下，且大小5.6M")
        set_command_run_flag(False)  # 将命令执行状态置为 False
        t = threading.Thread(target=self.__start_cd_soc_tcpdump, args=(cmd,))
        t.setDaemon(True)
        t.start()
        start_run_timeout = kwargs.get('start_run_timeout', 10)
        start_time = time.time()
        while (time.time() - start_time) < start_run_timeout:  # 阻塞，直到命令开始真正执行或者10秒超时
            if get_command_run_flag() is True:
                break
            else:
                time.sleep(0.2)
        time.sleep(1)
        # 返回 保存路径,和 文件名称
        return file_path, save_name

    def stop_cd_soc_tcpdump(self):
        """
        停止 cd_soc 内部抓包
        @return:
        """
        cmd = "\x03"
        logger.info(f"停止 ====》》》cd_soc 内部 tcpdump 抓包 cmd={cmd}")
        try:
            self.type_commands(commands=cmd, timeout=5)
            logger.info(f"停止 ====》》》cd_soc 内部 tcpdump 抓包 成功！！")
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/cd_soc/cd_soc_ssh.py")
            logger.error(f"停止 ====》》》cd_soc 内部 tcpdump 抓包失败 {str(e)}！！")

    def __start_cd_soc_tcpdump(self, cmd):
        """
        开启cd_soc 内部抓包
        @param cmd:
        @return:
        """
        logger.info(f"开启====》》》 cd_soc 内tcpdump抓包{cmd}")
        self.type_commands(cmd)

    def scp_cd_soc_file_to_local(self, cd_soc_file_pah, local_path, del_flag=False, **kwargs):
        '''
        拉取 cd_soc 的文件到本地
        @param cd_soc_file_pah:
        @param local_path:
        @return:
        '''
        # 有时候需要通过obd 获取ip
        connect_type = kwargs.get('connect_type', 'vlan')
        logger.info(f"生成的文件路径为==》》{local_path}")
        file_download(device_name=self.CD_SOC, local_path=local_path, remote_path=cd_soc_file_pah, connect_type=connect_type)
        logger.info(f"cd_soc 的日志 已经取出，路径为==》》》{local_path}")

        if del_flag:
            cmd = f"rm -f {cd_soc_file_pah}"
            logger.info(f"删除cd_soc  {cd_soc_file_pah}")
            self.type_commands(commands=cmd, timeout=5)
            logger.info(f"删除cd_soc  {cd_soc_file_pah} 成功")

    def get_version(self):
        cmd = "cat /mnt/etc/build.prop"
        data = self.type_commands(cmd)

        release = ''
        soa_version = ''
        jidl_version = ''
        bootes_version = ''
        version_release = None
        for i in data.split('\n'):
            i = i.strip()
            if 'ro.build.soa_carina_version' in i:
                soa_version = i.split('/')[-1]
            if 'ro.build.idl_version' in i:
                jidl_version = i.split('/')[-1]
            if 'ro.build.sw_part_number' in i:
                release = i.split('=')[-1]
                version_release = f"v{release[7]}.{release[8]}.{release[9]}"
                logger.debug(f"version_release:{version_release}")
            if "ro.build.soa_bootes_version" in i:
                bootes_version = i.split('=')[-1]

        if soa_version:
            soa_name = "SOA_" + soa_version + soa_version + jidl_version
        else:
            soa_name = "SOA_" + bootes_version + bootes_version + jidl_version
        soa_name = soa_name.replace(".", "_").strip()

        result = {
            "soa_name": soa_name,
            "soa_version": soa_version,
            "jidl_version": jidl_version,
            "bootes_version": bootes_version,
            "build_version": release,
            "version_release": version_release
        }
        return result
