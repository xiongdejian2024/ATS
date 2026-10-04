#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :ssh.py
@Time         :2023/10/31 10:00
@Author       :quan.sun@jiduauto.com
@Description  :ssh通信能力模拟 实现接口
"""
from xat_ecu import reporting as allure
import time
import re
import requests

from dateutil import parser
from xat_ecu.legacy.common.file_handle import ecu_simulator_abspath
from xat_ecu.legacy.interface.nuc_app import exec_shell

from xat_ecu.api import CommonSsh
from xat_ecu.legacy.driver.ssh_interface import file_download
from xat_ecu.api.constants.common import *
from xat_ecu.legacy.common.logger import *


class Ssh(CommonSsh):
    def type_commands(self, device_name: DeviceName, commands: str, timeout: int = 60) -> str:
        return self.device_dict[device_name.value].type_commands(commands=commands, timeout=timeout)
    def get_version(self, device_name: DeviceName):
        device_cmd = {
            # DeviceName.BGM.value: 'ls',
            DeviceName.TCAM.value: 'ls',
            DeviceName.ACU.value: 'ls',
            DeviceName.CDCQ.value: 'ls',
        }
        with allure.step(f"获取{device_name.value}版本号"):
            pass
        return self.type_commands(device_name=device_name, commands=device_cmd[device_name.value])

    def update_skip_debug(self, debug_list: list, allow_sleep: bool = True):
        if not debug_list:
            self.type_commands(DeviceName.BGM, f'echo -n "[]" > /update/skip_debug')
            time.sleep(0.5)
            self.type_commands(DeviceName.BGM, '''rm /update/state-backup.pb;rm /update/state.pb;rm /update/update_agent_persist.json;sync;ps -ef|grep -E "ua|install|fota|obt|arb"|grep app|awk -F " " '{print $2}'|xargs kill -9;sync''')
            if allow_sleep:
                time.sleep(10)
        else:
            debug_str = str(debug_list).replace('\'', '\\"').replace(',', ',\n')
            self.type_commands(DeviceName.BGM, f'echo -e "{debug_str}" > /update/skip_debug')
            time.sleep(0.5)
            self.type_commands(DeviceName.BGM, '''rm /update/state-backup.pb;rm /update/state.pb;rm /update/update_agent_persist.json;sync;ps -ef|grep -E "ua|install|fota|obt|arb"|grep app|awk -F " " '{print $2}'|xargs kill -9;sync''')
            if allow_sleep:
                time.sleep(20)

    def update_version_debug_cdc(self, task_id: int):
        logger.info("========================================================")
        logger.info("Current domain controller: CDC ")
        logger.info("========================================================")
        self.type_commands(DeviceName.BGM, f'echo -n "{VERSION_DEBUG_1}" > /update/version_debug.json')
        time.sleep(0.2)
        self.type_commands(DeviceName.BGM, f'echo -n "6608010818  F" >> /update/version_debug.json')
        time.sleep(0.2)
        self.type_commands(DeviceName.BGM, f'echo -n "{VERSION_DEBUG_2_CDC}" >> /update/version_debug.json')
        time.sleep(0.2)
        self.type_commands(DeviceName.BGM, f'echo -n "{task_id}" >> /update/version_debug.json')
        time.sleep(0.2)
        self.type_commands(DeviceName.BGM, f'echo -n "{VERSION_DEBUG_BACK}" >> /update/version_debug.json')
        time.sleep(0.2)

    def update_ua_skip(self, domain_name: DOMAIN, allow_same_version_flash: bool, flash_rate: int = 0, allow_sleep: bool = True):
        path = ""
        device = None
        cleanup_command = ""
        ua_skip_list = []
        if domain_name.value == 0:
            path = '/update/ua_skip'
            device = DeviceName.BGM
            cleanup_command = '''rm /update/state.pb /update/state-backup.pb; sync; ps -ef|grep -E "fota|ua"|grep app|awk '{print $2}'|xargs sudo kill -9'''
        elif domain_name.value == 1:
            path = '/mnt/sdcard/Update/ua_skip'
            device = DeviceName.TCAM
            cleanup_command = '''rm /mnt/sdcard/Update/update_agent_persist*;ps -ef|grep -E "ua|logcat"|grep app|awk -F " " '{print $1}'|xargs kill -9'''
            if flash_rate:
                ua_skip_list.append(f"{flash_rate}_flash_rate")
        else:
            logger.error(f"Not Support {domain_name}")
            return
        if allow_same_version_flash:
            ua_skip_list.append("allow_same_version_flash")
        ua_skip_str = str(ua_skip_list).replace('\'', '\\"')
        self.type_commands(device, f'echo "{ua_skip_str}" > {path}')
        self.type_commands(device, cleanup_command)
        if allow_sleep:
            time.sleep(20)

    def set_airplane_mode(self, sts: isOn):
        logger.info(f"======================= 转换飞行模式为 {sts.value} =======================")
        command = f'echo -en "at+cfun={1 if not sts.value else 0}\\r\\n" > /dev/smd8'
        self.type_commands(DeviceName.TCAM, command, timeout=5)
        time.sleep(3)
        # echo -en "at+cfun=1\\r\\n" > /dev/smd8 命令概率不生效，递归保证一定能开启/关闭飞行模式
        if sts.value and any(interface in self.type_commands(DeviceName.TCAM, 'ifconfig') for interface in ['rmnet_data1', 'rmnet_data0']):
            self.set_airplane_mode(isOn.On)
        elif not sts.value and all(interface not in self.type_commands(DeviceName.TCAM, 'ifconfig') for interface in ['rmnet_data1', 'rmnet_data0']):
            self.set_airplane_mode(isOn.Off)
        else:
            return True

    def set_cell_band(self, band: Cell_band):
        logger.info(f"======================= set Cellular {band.name} band =======================")
        command = f'cat /dev/smd8 & echo -en "at+gtact={band.value}\\r\\n" > /dev/smd8;sleep 3;cat /dev/smd8 & echo -en "at+gtact={band.value}\\r\\n" > /dev/smd8'
        self.type_commands(DeviceName.TCAM, command, timeout=5)
        time.sleep(5)

    def chk_net_channel(self):
        logger.info(f"======================= check rmnet_data 网卡生成结果 =======================")
        return self.type_commands(DeviceName.TCAM, "ifconfig | grep rmnet_data | awk '{print $1}'", timeout=5).split('\n')

    def tcam_ping_net(self, rmnet_data, ping_time):
        # times =time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())
        logger.info(f"======================= 指定tcam 网卡 执行ping操作 =======================")
        commands = f"ping -I {rmnet_data} 8.8.8.8 -c {ping_time}"
        return self.type_commands(DeviceName.TCAM, commands)

    def bgm_ping_net(self, chanel= "eth0.32", ping_time=4):
        logger.info(f"======================= 指定bgm 网卡 eth0.32 执行ping操作 =======================")
        commands = f"ping -I {chanel} www.baidu.com -c {ping_time}"
        return self.type_commands(DeviceName.BGM, commands)

    def bgm_ping_tcam(self, ping_time):
        logger.info(f"======================= 执行 bgm ping tcam 操作 =======================")
        commands = f"ping 172.16.5.31 -c {ping_time}"
        return self.type_commands(DeviceName.BGM, commands)

    def clear_fota_cache(self):
        logger.info("======================= clear fota cache =======================")
        self.type_commands(DeviceName.BGM, '''rm /update/state.pb /update/state-backup.pb; sync; ps -ef|grep fota|grep app|awk '{print $2}'|xargs sudo kill -9''')
        time.sleep(30)

    def ssh_reboot_bgm(self):
        logger.info("======================= reboot bgm =======================")
        self.type_commands(DeviceName.BGM, "cp /app/etc/reboot.sh /tmp/jiduer && chmod +x /tmp/jiduer/reboot.sh && runuser -l powerMgr -c '/tmp/jiduer/reboot.sh'")
        time.sleep(30)

    def init_bgm_tcpdump(self, local_path=None, bgm_path='/data/', **kwargs):
        """
        先推包到tmp 下，然后解压到 bgm_path 路径下
        @param local_path: 工具路径 如 /root/dbg-utils.tar.bz2
        @param bgm_path: 最后解压到那个路径下，建议 data 下
        @param kwargs:
        @return:
        """
        self.bgm_ssh.init_bgm_tcpdump(local_path, bgm_path, **kwargs)

    def delete_bgm_tcpdump_file(self, bgm_log_name="*.pcap", path='/update/'):
        """
        删除 bgm 内部 tcpdump 文件
        @param bgm_log_name: 要删除的w
        @param path: 文件所在路径
        @param kwargs:
        @return:
        """
        self.bgm_ssh.delete_bgm_tcpdump_file(bgm_log_name, path)

    def scp_bgm_log_to_local(self, bgm_log_name, log_path='/root/bgm_log/bgm_log', save_log_name=None, del_flag=False):
        """
         把 bgm 的日志 拉取到本地
        @param bgm_log_name:  拉取的是单个文件，或者压缩包，不能是文件夹
        @param log_path: 保存到本地的文件路径
        @param save_log_name: 保存到本地的文件名称 会加上时间戳
        @param del_flag: 是否删除原文件
        @return: 返回 文件全路径
        """
        file_path=self.bgm_ssh.scp_bgm_log_to_local(bgm_log_name, log_path, save_log_name, del_flag)
        return file_path

    def scp_local_file_to_bgm(self, local_path, bgm_path='/tmp/'):
        """
        把 本地 文件推送到bgm tmp 下
        @param local_path:  上位机的路径  如 "/root/bgm_log/"
        @param bgm_path:
        @return: file_path
        """
        self.bgm_ssh.scp_local_file_to_bgm(local_path, bgm_path)

    def start_bgm_tcpdump(self, name="bgm_", iface="eth0.5", **kwargs):
        """
        开启 bgm 内部抓包
        @param name:  抓包存储 文件名 ，最后会加上时间
        @param kwargs:
        @return: file_path, save_name
        """
        file_path, save_name=self.bgm_ssh.start_bgm_tcpdump(name, iface, **kwargs)
        return file_path, save_name

    def stop_bgm_tcpdump(self):
        """
        停止 bgm 内部抓包
        @return:
        """
        self.bgm_ssh.stop_bgm_tcpdump()

    def get_bgm_uptime(self):
        """
        获取 bgm 重启后的时间
        @return:
        """
        try:
            string_ = self.bgm_ssh.get_uptime()

            string_data = string_.split('0 users')[0].strip().split('up')[-1].strip()
            if "day" in string_data:
                string = string_data.replace("days", '').replace("day", '')
                # string = string_data.replace("day", '')
                string_lis = [item.strip() for item in string.split(',') if item.strip()]
                tim1 = int(string_lis[0]) * 24 * 60
                string_lis2 = string_lis[1].split(":")
                # 重启后运行时间
                tim2 = int(string_lis2[0]) * 60 + int(string_lis2[1])
                tim = tim1 + tim2
            elif 'min' in string_data:
                string = string_data.replace("min", '')
                string1 = string.split(',')[0]
                string_lis = string1.split('up')[-1].strip().split(":")
                # 重启后运行时间
                tim = int(string_lis[0])

            else:
                string1 = string_data.split(',')[0]
                string_lis = string1.split(":")
                # 重启后运行时间
                tim = int(string_lis[0]) * 60 + int(string_lis[1])
            print(f"bgm 重启后运行时间为:{tim}分钟")
            return tim
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/ssh.py")
            logger.error(f"获取bgm uptime失败{str(e)}")
            return 0

    def copy_factory_packages(self):
        logger.info("======================= copy_factory_packages =======================")
        self.type_commands(DeviceName.BGM, "cp /data/factory_bak/* /update/factory/;sync")

    def add_state_file(self):
        logger.info("======================= add_state_file =======================")
        self.type_commands(DeviceName.BGM, "cp /data/state_bak/* /update/;sync")

    def rm_factory_packages(self):
        logger.info("======================= rm_factory_packages =======================")
        self.type_commands(DeviceName.BGM, "rm -rf /update/factory/*;sync")

    def rm_ua_packages(self, domain_name:DOMAIN):
        logger.info(f"======================= rm {domain_name} bin packages =======================")
        if domain_name.value == 0:
            self.type_commands(DeviceName.BGM, "rm -rf /update/ua/* /update/installer/*;sync")
        elif domain_name.value == 1:
            self.type_commands(DeviceName.TCAM, "rm /mnt/sdcard/Update/update.zip;sync")

    def get_bgm_l7_constant(self):
        bgm_l7_key=self.bgm_ssh.get_l7_key()
        logger.info(f'获取到BGM L7 KEY:{bgm_l7_key}')
        return self.bgm_ssh.get_l7_key()

    def get_tcam_l7_constant(self):
        tcam_l7_key=self.tcam_ssh.get_L7()
        logger.info(f'获取到TCAM L7 KEY:{tcam_l7_key}')
        return self.tcam_ssh.get_L7()

    def check_file_existence(self, device_name:DeviceName, path:str, filename:str):
        logger.info(f"======================= Check whether {filename} is in {path} =======================")
        result = self.type_commands(device_name, f"stat {path}/{filename} && echo 'File exists' || echo 'File does not exist'")
        return "File exists" in result

    def check_ua_package(self, domain_name: DOMAIN):
        filename = "*.bin"
        if domain_name.value == 0:
            path = "/update/ua"
            device_name = DeviceName.BGM
        elif domain_name.value == 1:
            path = "/mnt/sdcard/Update/ua"
            device_name = DeviceName.TCAM
        else:
            logger.error(f"Not supported {domain_name}")
            return False
        return self.check_file_existence(device_name=device_name, path=path, filename=filename)

    def set_network_mode(self, network_mode: Network_Mode):
        logger.info(f"======================= set Network Mode: {network_mode} =======================")
        if network_mode.name == 'Fourth_Generation':
            self.type_commands(DeviceName.TCAM, '''cat /dev/smd8 & echo -en "at+gtact=2\r\n" > /dev/smd8''')
        elif network_mode.name == 'Fifth_Generation':
            self.type_commands(DeviceName.TCAM, '''cat /dev/smd8 & echo -en "at+gtact=14\r\n" > /dev/smd8''')
        else:
            logger.error(f"Worng network mode: {network_mode} was given")

    def exec(self, cmd, bgm_ip=None):
        ret = self.type_commands(DeviceName.TCAM, commands=cmd)
        return ret.replace('\r\n', '\n')

    def get_log(self, device_name:DeviceName, local_path:str = '/', file_needed:str = '*', save_log_name:str = 'log.tar.gz', del_flag:bool = False):
        logger.info(f"======================= get {device_name} log =======================")
        if device_name == DeviceName.BGM:
            self.type_commands(DeviceName.BGM, f'tar -zcvf /log/bgm_log.tar.gz /log/{file_needed}',timeout=600)
            self.scp_bgm_log_to_local(bgm_log_name='/log/bgm_log.tar.gz', log_path=local_path, save_log_name=f"bgm_{save_log_name}", del_flag=del_flag)
        else:
            logger.error("Just Support BGM now")

    def clear_log(self, device_name:DeviceName):
        if device_name == DeviceName.BGM:
            self.type_commands(DeviceName.BGM, 'rm -rf /log/*')
        else:
            logger.error("Just Support BGM now")

    def get_domian_last_boot(self, domain_name:DOMAIN):
        if domain_name == DOMAIN.BGM:
            return self.type_commands(DeviceName.BGM, '/app/bin/swdl -nr 8')
        elif domain_name == DOMAIN.TCAM:
            boot_info = self.type_commands(DeviceName.TCAM, 'cd /usr/bin/;updatetool -g')
            match = re.search(r'lastboot\s+=\s+(\w+)', boot_info)
            if match:
                return match.group(1)
        else:
            logger.error(f"Wrong domian name: {domain_name}")

    def get_bgm_jetlog_msg_s2s_bst_names(self, timeout=60):
        '''
        获取 bgm /log 下面所有 jetlog_messages  jetlog_s2s,jetlog_bts 的名字

        @return:[jetlog_messages],[jetlog_s2s],[jetlog_bts]
        '''
        #
        commands = 'ls /log'
        ret_msg = self.type_commands(DeviceName.BGM, commands=commands, timeout=timeout)
        if ret_msg.strip():
            string_list = [item.split(' ') for item in ret_msg.replace('\t', ' ').split('\n')]
            data_lis = []
            for item_lis in string_list:
                lis = [item.strip() for item in item_lis if item.strip()]
                if lis:
                    data_lis.extend(lis)
            jetlog_messages = [item for item in data_lis if item.startswith('jetlog_messages')]
            jetlog_messages.sort()
            logger.info(f"jetlog_messages_names={jetlog_messages}")

            jetlog_s2s = [item for item in data_lis if item.startswith('jetlog_s2s')]
            jetlog_s2s.sort()
            logger.info(f"jetlog_s2s={jetlog_s2s}")

            jetlog_bts = [item for item in data_lis if item.startswith('jetlog_bts')]
            jetlog_bts.sort()
            logger.info(f"jetlog_bts={jetlog_bts}")

            return jetlog_messages, jetlog_s2s, jetlog_bts
        else:
            logger.warning("未获取到bgm的 jetlog_messages")
            return [], [], []

    def get_log_from_bgm(self, log_name=None, save_path='/root/bgm_log', tar_bgm_path='/update/', log_type=None,
                timeout=600):
        '''
        获取 bgm的日志 ：
            可以获取单个文件 单个文件只能获取这三种类型的【jetlog_bts,jetlog_s2s,jetlog_messages】需要传递全名 带后缀
            获取多个文件 会打包到  tar_bgm_path 路径下
        @param log_name: 单个文件名称，或者为None，如为None 则打包 log_type 类型的数据
        @param save_path: 本地保存的位置
        @param tar_bgm_path: 在bgm内部打包的位置，最好不要在 log下，log满的时候无法存储
        @param log_type: 拉取日志的类型 【jetlog_bts,jetlog_s2s,jetlog_messages，None】
        @param timeout:超时时间
        @return:
        '''

        if not os.path.exists(save_path):
            os.mkdir(save_path)
        otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))
        if log_name is None:
            # 打包所有的 jetlog_messages
            # tar -zcvf /update/BGMlog.tar.gz /log/*
            # 拼接地址
            if log_type == "jetlog_bts":
                tar_log_name = 'BGM_jetlog_bts.tar.gz'
                tar_name = 'jetlog_bts*'
            elif log_type == "jetlog_messages":
                tar_log_name = 'BGM_jetlog_message.tar.gz'
                tar_name = 'jetlog_messages*'
            elif log_type == "jetlog_s2s":
                tar_log_name = 'BGM_jetlog_s2s.tar.gz'
                tar_name = 'jetlog_s2s*'
            elif log_type == "coredump":
                tar_log_name = 'BGM_coredump.tar.gz'
                tar_name = 'coredump*'
            else:
                tar_log_name = 'BGM_LOG.tar.gz'
                tar_name = '*'

            bgm_log = os.path.join(tar_bgm_path, tar_log_name)
            commands = f'tar -zcvf {bgm_log} /log/{tar_name}'
            # 打包日志
            logger.info(f"开始打包的bgm的{log_type if log_type is not None else '所有'} 日志")
            ret_msg = self.type_commands(DeviceName.BGM, commands=commands, timeout=timeout)
            logger.info(f"打包的bgm的{log_type if log_type is not None else '所有'} 日志完成")
            save_path = os.path.join(save_path, f'{otherStyleTime}_{tar_log_name}')
        else:
            if not (log_name.startswith('jetlog_bts') or log_name.startswith('jetlog_s2s') or log_name.startswith(
                    'jetlog_messages')):
                string = "单个日志只能拉取这三种类型的【jetlog_bts,jetlog_s2s,jetlog_messages】"
                logger.error(string)
                assert 0, string
            bgm_log = f"/log/{log_name}"
            save_path = os.path.join(save_path, f'{otherStyleTime}_{log_name}')
        # 下载日志
        logger.info(f"开始拉取的bgm的{log_type} ")
        file_download(device_name='BGM', local_path=save_path, remote_path=bgm_log, connect_type='obd')
        logger.info(f"拉取的bgm的{log_type}保存路径为{save_path}")
        # 删除 打包日志
        if log_name is None:
            commands = f'rm -rf {bgm_log}'
            ret_msg = self.type_commands(DeviceName.BGM, commands=commands, timeout=60)
            logger.info(f"清除bgm内部打包 {bgm_log}日志")
        # 返回拉出日志的 路径
        return save_path

    def get_bgm_log(self, save_path='/root/bgm_log', tar_bgm_path='/update/', timeout=600):
        '''
        拉取 bgm的 所有日志
        @param save_path: 本地保存的地址
        @param tar_bgm_path: 在bgm内部打包的位置，最好不要在 log下，log满的时候无法存储
        @param timeout:
        @return:
        '''
        return self.get_log_from_bgm(log_name=None, save_path=save_path, tar_bgm_path=tar_bgm_path, timeout=timeout,
                            log_type=None)

    def get_bgm_jetlog_bts(self, log_name=None, save_path='/root/bgm_log', tar_bgm_path='/update/', timeout=600):
        '''
        拉取 bgm的 jetlog_bts
           拉取单个文件
        @param log_name: 为 None 拉取所有的jetlog_bts 日志，传单个文件则拉取单个文件
        @param save_path: 本地保存的地址
        @param tar_bgm_path: 在bgm内部打包的位置，最好不要在 log下，log满的时候无法存储
        @param timeout:
        @return:
        '''
        return self.get_log_from_bgm(log_name=log_name, save_path=save_path, tar_bgm_path=tar_bgm_path, timeout=timeout,
                            log_type='jetlog_bts')

    def get_bgm_jetlog_s2s(self, log_name=None, save_path='/root/bgm_log', tar_bgm_path='/update/', timeout=600):
        '''
        拉取 bgm的 jetlog_s2s
           拉取单个文件
        @param log_name: 为 None 拉取所有的jetlog_bts 日志，传单个文件则拉取单个文件
        @param save_path: 本地保存的地址
        @param tar_bgm_path: 在bgm内部打包的位置，最好不要在 log下，log满的时候无法存储
        @param timeout:
        @return:
        '''
        return self.get_log_from_bgm(log_name=log_name, save_path=save_path, tar_bgm_path=tar_bgm_path, timeout=timeout,
                            log_type='jetlog_s2s')

    def get_bgm_jetlog_messages(self, log_name=None, save_path='/root/bgm_log', tar_bgm_path='/update/',
                                timeout=600):
        '''
        拉取 bgm的 jetlog_messages
           拉取单个文件
        @param log_name: 为 None 拉取所有的jetlog_bts 日志，传单个文件则拉取单个文件
        @param save_path: 本地保存的地址
        @param tar_bgm_path: 在bgm内部打包的位置，最好不要在 log下，log满的时候无法存储
        @param timeout:
        @return:
        '''
        return self.get_log_from_bgm(log_name=log_name, save_path=save_path, tar_bgm_path=tar_bgm_path, timeout=timeout,
                            log_type='jetlog_messages')

    def get_bgm_coredump_names(self):
        '''
           获取 文件名称
           @return: [（file_name, create_time）, (), .......]
        '''
        return self.bgm_ssh.get_bgm_coredump()

    def get_bgm_coredump(self, dump_file_name=None, save_path='/root/bgm_log', tar_bgm_path='/update/',
                         timeout=10 * 60):
        '''
        拉取 coredump 文件到 本地 save_path 下
        @param dump_file_name:  coredump  可以为单个文件;为 None 的时候，表示拉取所有的coredump 文件
        @param save_path: 本地保存的位置
        @param tar_bgm_path: 在bgm内部打包的位置，最好不要在 log下，log满的时候无法存储
        @return: 本地保存路径
        '''

        # 取单个文件 单个文件的名字
        log_time = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime(time.time()))
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        commands = f"ls /log"
        ret_msg = self.type_commands(DeviceName.BGM, commands=commands, timeout=timeout)
        if "coredump" not in ret_msg:
            return None

        bgm_log_path = os.path.join(tar_bgm_path, 'bgm_coredump.tar.gz')
        if dump_file_name is None:
            commands = f"cd /log/coredump/;tar -zcvf {bgm_log_path} ./*"
        else:
            if isinstance(dump_file_name, list):
                dump_file_name_string = ' '.join(dump_file_name)
            else:
                dump_file_name_string = dump_file_name
            commands = f"cd /log/coredump/;tar -zcvf {bgm_log_path} ./{dump_file_name_string}"

        logger.info(f">>>>>>>>>>>>>>>>开始打包 bgm coredump 日志 需要一定时间<<<<<<<<<<<<<<<<<<<<")
        t = time.time()
        self.type_commands(DeviceName.BGM, commands=commands, timeout=timeout)

        logger.info(f"打包 bgm coredump 日志 结束{time.time() - t}秒")
        # 日志特别大 需要压缩，单个也需要压缩
        name = f"{log_time}_bgm_coredump.tar.gz"
        logger.info(f"{dump_file_name}对应的 压缩包为{name}")

        local_path = os.path.join(save_path, name)
        t1 = time.time()
        file_download(device_name='BGM', local_path=local_path, remote_path=bgm_log_path, connect_type='obd')
        logger.info(f"拉取文件耗时{time.time() - t1}秒")
        if dump_file_name is None:
            commands = f'rm -rf {bgm_log_path}'
            ret_msg = self.type_commands(DeviceName.BGM, commands=commands, timeout=60)
            logger.info(f"清除bgm内部打包 {bgm_log_path}日志")
        return local_path

    def clear_bgm_coredump(self, timeout=10):
        '''
        清除bgm 下的所有 coredump
        @return:
        '''
        commands = f"rm -rf /log/coredump/"
        ret_msg = self.type_commands(DeviceName.BGM, commands=commands, timeout=timeout)

    def clear_bgm_all_log(self):
        '''
        清除所有报告 需要重启
        @return:
        '''
        self.bgm_ssh.clear_log()

    def get_bgm_jetlog_msg_or_s2s_or_bst_del_names(self, log_list: list, log_type: str):
        '''
        获取 删除的日志名称
        @param log_list:
        @param log_type:["jetlog_bts", "jetlog_messages", "jetlog_s2s"]
        @return:
        '''

        if log_type not in ["jetlog_bts", "jetlog_messages", "jetlog_s2s"]:
            assert 0, f"""log_type 的取值范围为{["jetlog_bts", "jetlog_messages", "jetlog_s2s"]}"""
        # 清理 jetlog_messages
        rm_list1 = []
        rm_list2 = []
        for item in log_list:
            if item == log_type:
                continue
            #  jetlog_messages11_20210101080002_c9aae5e2519d4fe490dad2019c668360.zst
            if len(item) > len(f"{log_type}11_20210101080002"):
                rm_list1.append(item)
            else:
                rm_list2.append(item)
        rm_dict = {}
        for item in rm_list2:
            index_string = item.replace(log_type, '').replace('.zst', '')
            try:
                index = int(index_string)
                rm_dict[index] = item
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/ssh.py")
                logger.error(f"{item}名字格式不符合要求需要处理")
        max_index = max(list(rm_dict.keys()))
        max_item = rm_dict.get(max_index)
        if max_item in rm_list2:
            rm_list2.remove(max_item)
        rm_list = rm_list2 + rm_list1[:-1]
        logger.info(f"需要删除的日志名称为{rm_list}")
        return rm_list

    def clear_bgm_log_no_need_reset(self, timeout=10):
        '''
        清除bgm的 日志 不需要重启bgm
        @param timeout:
        @return:
        '''

        jetlog_messages, jetlog_s2s, jetlog_bts = self.get_bgm_jetlog_msg_s2s_bst_names()
        if jetlog_messages:
            jetlog_messages_list = self.get_bgm_jetlog_msg_or_s2s_or_bst_del_names(jetlog_messages, 'jetlog_messages')
            del_log = ' '.join(jetlog_messages_list)
            # 删除
            commands = f"rm -rf /log/{del_log}"
            ret_msg = self.type_commands(DeviceName.BGM, commands=commands, timeout=timeout)

            jetlog_s2s_list = self.get_bgm_jetlog_msg_or_s2s_or_bst_del_names(jetlog_s2s, 'jetlog_s2s')
            del_log = ' '.join(jetlog_s2s_list)
            commands = f"rm -rf /log/{del_log}"
            ret_msg = self.type_commands(DeviceName.BGM, commands=commands, timeout=timeout)

            jetlog_bts_list = self.get_bgm_jetlog_msg_or_s2s_or_bst_del_names(jetlog_bts, 'jetlog_bts')
            del_log = ' '.join(jetlog_bts_list)
            commands = f"rm -rf /log/{del_log}"
            ret_msg = self.type_commands(DeviceName.BGM, commands=commands, timeout=timeout)

            # 删除 coredump
            ret_msg = self.clear_bgm_coredump()
        else:
            logger.error("日志不存在，无法清除")
            assert 0, '日志不存在，无法清除'

    def get_ping(self, ip=None, num=4, root_permission=False):
        """
        看 tcam 是否 ping 通 该 ip
        @param ip: 需要ping的 ip
        @param num: 尝试几次
        @return: True or False
        """
        return self.bgm_ssh.get_ping(ip=ip, num=num, root_permission=root_permission)

    def get_arping(self, ip=None, num=4):
        """
        看 在bgm里是否能arping通
        @param ip: 需要arping的 ip
        @param num: 尝试几次
        @return: True or False
        """
        if ip is None:
            ip = "www.baidu.com"
        cmd = f'arping {ip} -c {num}'
        # 初始化ssh
        # self.ssh = Ssh(domain=self.domain)
        String = self.type_commands(DeviceName.BGM,cmd)
        logger.info(f"获取的 bgm 的{cmd}的结果为 {String}")
        send_count = re.findall("Sent (.*?) probes",String)[0]
        recive_count = re.findall("Received (.*?) response",String)[0]
        if send_count != recive_count:
            #发送数据数量和接受数据数量不一致
            return False
        else:
            return True

    def retry_ping_mul_times(self, ip=None, num=4, retry=2, root_permission=False):
        """
        若失败则重试 ping 几次
        @param ip: 每次 ping 的 对象
        @param num: 每次 ping 4
        @param retry: 若失败 则 再次尝试2轮，每轮ping 4次
        @return: True or False
        """
        return self.bgm_ssh.retry_ping_mul_times(self, ip=None, num=4, retry=2, root_permission=False)

    def read_bgm_jetlog(self):
        ret = self.type_commands(DeviceName.BGM, "cd /log;/app/bin/zstdcat jetlog_messages |grep -E 'PWIMP|PWMGR'",
                                 timeout=60)
        shu = ret.rfind("power mode: 1 PowerOFF")
        pos = ret.rfind("SOC_SFGPIO_3 value")
        if shu == -1 or pos == -1:
            logger.info("日志分页，需要进行拼接查询")
            # 说明日志分页了，获取前一个日志 重新查询
            pre_log_name = self.get_bgm_second2last_jetlog_messages_name()
            pre_ret = self.type_commands(DeviceName.BGM,
                                         f"cd /log;/app/bin/zstdcat {pre_log_name} |grep -E 'PWIMP|PWMGR'",
                                         timeout=80)
            # 两个日志拼接一起，再查询
            ret = pre_ret + '\n'+"拼接处"+ '\n' + ret
            logger.info(f"拼接的日志为={ret}")
            shu = ret.rfind("power mode: 1 PowerOFF")
            pos = ret.rfind("SOC_SFGPIO_3 value")
        else:
            # 如果 需要日志不存在，则需要延长时间，等日志落盘
            awakeup_log_last = ret[pos - 1:]
            # 能获取日志 说明一定是启动了，最后一定会有 power mode: 2 PowerON
            if "power mode: 2 PowerON" not in awakeup_log_last:
                # 需要日志不存在，则加延时 等待日志落盘
                logger.info(f"********* power mode: 2 PowerON 不在日中，日志未完全落盘，延时一段时间再取")
                time.sleep(20)
                ret = self.type_commands(DeviceName.BGM,
                                         "cd /log;/app/bin/zstdcat jetlog_messages |grep -E 'PWIMP|PWMGR'",
                                         timeout=60)
                shu = ret.rfind("power mode: 1 PowerOFF")
                pos = ret.rfind("SOC_SFGPIO_3 value")


        sleep_log_last = ret[shu - 1:]
        awakeup_log_last = ret[pos - 1:]
        logger.info("**************************")
        logger.info(sleep_log_last)
        logger.info(awakeup_log_last)
        return sleep_log_last, awakeup_log_last
    
    def read_auto_jetlog(self):
        ret = self.type_commands(DeviceName.BGM, "cd /log;/app/bin/zstdcat jetlog_messages |grep -E 'CALI_|RM_DIAG|diag_client_log'",
                                 timeout=60)
        shu = ret.rfind("tx 1002:10 03")
        pos = ret.rfind("obt_diag_proxy.cpp")
        if shu == -1 or pos == -1:
            logger.info("日志分页，需要进行拼接查询")
            # 说明日志分页了，获取前一个日志 重新查询
            pre_log_name = self.get_bgm_second2last_jetlog_messages_name()
            pre_ret = self.type_commands(DeviceName.BGM,
                                         f"cd /log;/app/bin/zstdcat {pre_log_name} |grep -E 'CALI_|RM_DIAG|diag_client_log'",
                                         timeout=80)
            # 两个日志拼接一起，再查询
            ret = pre_ret + '\n'+"拼接处"+ '\n' + ret
            logger.info(f"拼接的日志为={ret}")
            shu = ret.rfind("tx 1002:10 03")
            pos = ret.rfind("obt_diag_proxy.cpp")
        else:
            # 如果 需要日志不存在，则需要延长时间，等日志落盘
            awakeup_log_last = ret[pos - 1:]
            # 能获取日志 说明一定是启动了，最后一定会有 power mode: 2 PowerON
            if "标定流程结束" not in awakeup_log_last:
                # 需要日志不存在，则加延时 等待日志落盘
                logger.info(f"********* power mode: 2 PowerON 不在日中，日志未完全落盘，延时一段时间再取")
                time.sleep(20)
                ret = self.type_commands(DeviceName.BGM,
                                         "cd /log;/app/bin/zstdcat jetlog_messages |grep -E 'CALI_|RM_DIAG|diag_client_log'",
                                         timeout=60)
                shu = ret.rfind("tx 1002:10 03")
                pos = ret.rfind("obt_diag_proxy.cpp")


        sleep_log_last = ret[shu - 1:]
        awakeup_log_last = ret[pos - 1:]
        logger.info("**************************")
        logger.info(sleep_log_last)
        logger.info("###########################")
        logger.info(awakeup_log_last)
        return sleep_log_last, awakeup_log_last

    def get_bgm_second2last_jetlog_messages_name(self):
        '''
        日志分层的时候 防止日志取不全，获取倒数第二个日志的名字
        @param log_type: 默认是 jetlog_messages
        @return: 日志名字 jetlog_messages808_20241005091818_31ed136b2ff8467a98e90c4cda2ca443.zst
        '''
        log_type="jetlog_messages"
        log_string = self.type_commands(DeviceName.BGM, "cd /log;ls", timeout=20)
        # 所有 jetlog_messages* 的名字 除去jetlog_messages文件
        lis=[]
        log_string_list=log_string.replace("\t", ' ').split("\n")

        for item in log_string_list:
            if log_type in item :
                item_list=item.split(" ")
                for it in item_list:
                    if log_type in it and it.strip() and len(it) > len(log_type):
                        lis.append(it.strip())

        logger.info(f"jetlog_messages* 个数={len(lis)}={lis}")
        log_name_dict={}
        # 做映射，索引和名字
        for item in lis:
            logger.info(f"item={item}")
            index=item.split("_")[1][len('messages'):]
            log_name_dict[int(index)]=item
        # log_name_dict = {int(item.split("_")[1][len('messages'):]): item for item in lis}
        # 获取所有索引，并按大小排序
        index_list = list(log_name_dict.keys())
        index_list.sort()
        logger.info(f"index_list 个数为{len(index_list)}={index_list}")

        log_name = log_name_dict.get(index_list[-2])
        logger.info(f"获取的前一个日志的文件名字为{log_name}")
        return log_name

    def ccp_skip_debug(self, debug_list: list, allow_sleep: bool = True):
        if not debug_list:
            self.type_commands(DeviceName.BGM, f'echo -n "[]" > /update/ccp_skip_debug')
            time.sleep(0.5)
        else:
            debug_str = str(debug_list).replace('\'', '\\"').replace(',', ',\n')
            self.type_commands(DeviceName.BGM, f'echo -e "{debug_str}" > /update/ccp_skip_debug')
            time.sleep(0.5)

    def rm_ccp_persist(self):
        logger.info("======================= clear ccp cache =======================")
        self.type_commands(DeviceName.BGM, '''rm -rf /data/fod/ccp_persist.json;sync''')
        time.sleep(2)

    def check_metric_data(self, command: str, ip, *args):
        data = self.tcam_ssh.exec(command, ip)
        for i in range(len(args)):
            assert args[i] in data, 'metric_data采集失败'

    def check_vlan_conn(self,bgm_ip, vlan_ip, mac_address):
        data = self.tcam_ssh.exec(cmd="ip neigh show", bgm_ip=bgm_ip)
        # vlan_ip = "172.16.9.1"
        with allure.step(f"查看BGM SOC {vlan_ip}的配置"):
            success = []
            for i in data.split('\n'):
                if i.split(' ')[0] == vlan_ip:
                    if i.split(' ')[-2] == mac_address and i.split(' ')[-1] == 'PERMANENT':
                        allure.attach("{0}".format(i), f"BGM SOC ip {vlan_ip}的配置信息查询")
                        allure.attach("OK", f"ip地址为{vlan_ip}的静态ARP配置")
                        success.append(vlan_ip)
                    else:
                        allure.attach("Failed", f"ip地址为{vlan_ip}的静态ARP配置")
                    break
                else:
                    continue
            if not success:
                allure.attach("暂未查询到", f"BGM SOC ip {vlan_ip}的配置信息查询")
        assert success == [vlan_ip],f"BGM SOC的{vlan_ip}的配置信息错误"

    def update_mcu_switch(self, obd_iface="enx207bd23db624", software_path=None, **kwargs):
        ## 推包 安波福的Switch软件是禁止PC访问Switch的，所以如果在他们的软件下，
        ## 要使用PC访问Switch或者刷软件都要打开后门，上下电后后门失效需要重新打开
        script_path = os.path.join(f"{ecu_simulator_abspath}", 'scripts')
        open_obd = kwargs.get('open_obd', True)
        if software_path is None:
            software_path = "BGM_Switch_FW_JIDU_for_MCUTest_V1.0.bin"

        if open_obd:
            openobdrmu_path = os.path.join(script_path, "openobdrmu")
            self.scp_local_file_to_bgm(openobdrmu_path)
            openobdrmush_path = os.path.join(script_path, "openobdrmu.sh")
            self.scp_local_file_to_bgm(openobdrmush_path)
            self.type_commands(DeviceName.BGM, "cd /tmp/;chmod 777 openobdrmu.sh;./openobdrmu.sh")

        # 查找obd网卡
        for retry_count in range(3):
            cmd_obd_number = f"cd %s;chmod 777 *;./DownloadImage -li | grep %s" % (script_path, obd_iface)
            logger.info(f"cmd_obd_number={cmd_obd_number}")
            output = exec_shell(command=cmd_obd_number).get('output')
            logger.info(f"output={output}")
            if output:
                    iface_number = output.split('.')[0]
                # for retry_count in range(3):
                    ret = os.system(f'cd {script_path};sudo ./fw_download.sh {iface_number} {software_path} 01 0')
                    if ret != 0:
                        logger.error(f"升级失败, 等待 5分钟 开始重试{retry_count+1}  ")
                        time.sleep(5*60)
                        continue
                    else:
                        break
        else:
            assert False, "升级失败"

    def rescue_ua_skip(self):
        debug_list = ["debug_inhibit_timeout"]
        debug_str = str(debug_list).replace('\'', '\\"').replace(',', ',\n')
        self.type_commands(DeviceName.BGM, f'echo -e "{debug_str}" > /update/ua_skip')
        time.sleep(0.5)

    def read_bgm_jetlog_flag(self):
        ret = self.type_commands(DeviceName.BGM,"cd /log;/app/bin/zstdcat jetlog_messages |grep -E 'restart status|DMC_RESTART'",timeout=30)
        flag = ret.rfind('{"mainState":1,"notification":0,"telematicsState":0,"autoDrivingState":0,"cockpitState":0,"digitalKeyState":0}')
        awakeup_log_last = ret[flag - 1 :]
        logger.info("**************************")
        logger.info(awakeup_log_last)
        return awakeup_log_last

    def update_skip_debug_nokill(self, debug_list: list):
        if not debug_list:
            self.type_commands(DeviceName.BGM, f'echo -n "[]" > /update/skip_debug')
            time.sleep(0.5)
        else:
            debug_str = str(debug_list).replace('\'', '\\"').replace(',', ',\n')
            self.type_commands(DeviceName.BGM, f'echo -e "{debug_str}" > /update/skip_debug')
            time.sleep(0.5)

    def get_tcam_uptime(self):
        """
        获取 tcam 重启后的时间
        @return:
        """
        try:
            string_ = self.tcam_ssh.type_commands('uptime', timeout=10)

            string_data = string_.split('0 users')[0].strip().split('up')[-1].strip()
            if "day" in string_data:
                string = string_data.replace("days", '').replace("day", '')
                # string = string_data.replace("day", '')
                string_lis = [item.strip() for item in string.split(',') if item.strip()]
                tim1 = int(string_lis[0]) * 24 * 60
                string_lis2 = string_lis[1].split(":")
                # 重启后运行时间
                tim2 = int(string_lis2[0]) * 60 + int(string_lis2[1])
                tim = tim1 + tim2
            elif 'min' in string_data:
                string = string_data.replace("min", '')
                string1 = string.split(',')[0]
                string_lis = string1.split('up')[-1].strip().split(":")
                # 重启后运行时间
                tim = int(string_lis[0])

            else:
                string1 = string_data.split(',')[0]
                string_lis = string1.split(":")
                # 重启后运行时间
                tim = int(string_lis[0]) * 60 + int(string_lis[1])
            logger.info(f"TCAM 重启后运行时间为:{tim}分钟")
            return tim
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/ssh.py")
            logger.error(f"获取bgm uptime失败{str(e)}")
            return 0

    def kill_bgm_process(self, process: BgmApp):
        """
        在bgm内kill指定进程
        @param process: 进程名
        @return:
        """
        is_running, pid = self.is_bgm_process_running(process)
        if is_running:
            self.bgm_ssh.type_commands(f"kill -9 {pid}", timeout=1, alias="1")

    def rerun_bgm_process(self, process: BgmApp):
        """
        在bgm内重启指定进程，仅用于SIL环境，HIL中em2会主动拉
        @param process: 进程名
        @return:
        """
        self.kill_bgm_process(process)
        self.run_bgm_process(process)

    def is_bgm_process_running(self, process: BgmApp):
        """
        在bgm域控内判断指定进程是否运行
        @param process: 进程名
        @return: (bool: 是否在运行, pid)
        """
        res = self.bgm_ssh.type_commands(f"ps -ef |grep app |grep {process.name} |grep -v grep", timeout=1, alias="1")
        if res == "":
            return False, None
        else:
            return True, res.split()[1]

    def run_bgm_process(self, process: BgmApp):
        """
        在bgm内重启指定进程，仅用于SIL环境，HIL中em2会主动拉
        @param process: 进程名
        @return:
        """
        is_running, pid = self.is_bgm_process_running(process)
        if is_running:
            logger.info(f"{process.name}进程运行中, pid:{pid}")
            return

        if process == BgmApp.s2s_service:
            self.bgm_ssh.type_commands(commands='su -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;nohup /app/bin/s2s_service &"', timeout=1, alias="1")
        elif process == BgmApp.em2:
            self.bgm_ssh.type_commands(commands='su -c "source /app/etc/bgm_app_env.sh; nohup /app/bin/em2 &"', timeout=1, alias="1")
        elif process == BgmApp.jetlogd:
            self.bgm_ssh.type_commands(commands='su -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;nohup /app/bin/jetlogd &"', timeout=1, alias="1")
        elif process == BgmApp.service_monitor:
            self.bgm_ssh.type_commands(commands='su -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;nohup /app/bin/service_monitor -c /app/etc/service_monitor.json &"', timeout=1, alias="1")

    def del_s2s_db(self):
        """
        删除s2s的数据库，一般用于测试默认配置
        @return:
        """
        self.bgm_ssh.type_commands("rm -f /data/s2s_service/s2s_service.db3", timeout=2, alias="1")
        self.bgm_ssh.type_commands("sync", timeout=2, alias="1")
        self.bgm_ssh.type_commands("ls -l /data/s2s_service/", timeout=2, alias="1")

    def del_SOAAPP_db(self):
        """
        删除SOAAPP的数据库，一般用于测试默认配置
        @return:
        """
        self.bgm_ssh.type_commands("rm -f /data/SOAApp/SOAApp.db3", alias="1")
        self.bgm_ssh.type_commands("sync", alias="1")
        self.bgm_ssh.type_commands("ls -l /data/SOAApp/", alias="1")

    def verify_time_synchronization(self, device_name: DeviceName, time_diff=2):
        """
        获取域控时间，判断是否时间同步
        @return:
        """
        # 获取域控当前UTC时间
        cmd = "date"
        tcam_utc_str = self.type_commands(device_name, cmd)
        tcam_utc = parser.parse(tcam_utc_str, fuzzy=True)
        logger.info(f"域控当前UTC时间: {tcam_utc}")

        # 获取当前UTC时间
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        logger.info(f"当前UTC时间: {now_utc}")

        # 判断域控时间与当前时间是否相差不超过time_diff秒
        is_time_synchronized = abs(tcam_utc - now_utc).seconds <= time_diff
        logger.info(f"域控时间与当前时间误差: {abs(tcam_utc - now_utc).seconds}秒，允许最大误差{time_diff}秒")
        assert is_time_synchronized, f"域控时间与当前时间相差超过{time_diff}秒"

    def download_factory_package_to_bgm(self, package_url: str):
        self.type_commands(DeviceName.BGM, "rm -rf /data/factory_package/*")
        response = requests.get(package_url)
        with open("FactoryPackage.zip", 'wb') as fn:
            fn.write(response.content)
        self.scp_local_file_to_bgm("FactoryPackage.zip")
        self.type_commands(DeviceName.BGM, "unzip /tmp/FactoryPackage.zip -d /data/factory_package/")

    def ask_simo_message(self, msg):
        self.cdca_adb.check_connect_status()
        cmd = f'/update/adb shell am broadcast -a com.jidu.voice.jdbroadcast --es test_type "dealAsr" --es test_asr "{msg}" --ei index 0'
        self.cdca_adb.type_commands(cmd)
        cmd = f'/update/adb shell input tap 2462 526'
        ret = self.cdca_adb.type_commands(cmd)
        return ret
