#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :ssh.py

@Time         :2023/10/31 10:00

@Author       :quan.sun@jiduauto.com

@Description  :ssh通信能力模拟 抽象接口
"""
from abc import abstractmethod, ABCMeta

from xat_ecu.api.constants.common import *


class AbcSsh(metaclass=ABCMeta):
    @abstractmethod
    def type_commands(self, device_name: DeviceName, commands: str, timeout: int = 60) -> str:
        """
        在对应的设备上执行命令
        
        :param device_name: 连接的设备
        :param commands: 命令
        :param timeout: 超时时间
        :return:
        """
        pass

    @abstractmethod
    def get_version(self, device_name: DeviceName):
        """
        获取版本号
        
        :param device_name: 连接的设备
        :return:
        """

    @abstractmethod
    def update_skip_debug(self, debug_list: list, allow_sleep: bool = True):
        """
        更新BGM /update/skip_debug文件
        
        :param debug_list: debug 字段，例"time_check","wait_hmi"
        :param allow_sleep: 杀完进程后是否允许休眠，默认允许
        :return:
        """

    @abstractmethod
    def update_version_debug_cdc(self, task_id: int):
        """
        更新BGM /update/version_debug文件, mock CDC 升级
        
        :param task_id: FOTA 任务id
        :return:
        """
        
    @abstractmethod
    def update_ua_skip(self, domain_name: DOMAIN, allow_same_version_flash: bool, flash_rate: int = 0, allow_sleep: bool = True):
        """
        更新BGM /update/ua_skip文件
        
        :param domain_name: 枚举类型 : class DOMAIN(BaseEnum): BGM = 0、TCAM = 1、CDC = 2、ACU = 3
        :param allow_same_version_flash: 是否允许同版本强刷
        :param flash_rate: TCAM刷写速率，当domain_name=TCAM且flash_rate不为0时该参数生效，默认值为0
        :param allow_sleep: 杀完进程后是否允许休眠，默认允许
        :return:
        """
        
    def set_airplane_mode(self, sts: isOn):
        """
        设置TCAM的飞行模式
        
        :param sts: 枚举类型 isOn: class isOn(BaseEnum):Off = False、On = True
        :return: None
        :raises keyError: None
        """
    
    @abstractmethod
    def set_cell_band(self, band: Cell_band):
        """
        切换tcam的蜂窝网络制式: SA LTE 制式切换
        
        :param band: 枚举类型 SA = 21 LTE = 2
        """

    @abstractmethod
    def chk_net_channel(self):
        """
        检查tcam网卡生成结果
        
        :return: 
        """

    @abstractmethod
    def tcam_ping_net(self, rmnet_data, ping_time: int):
        """
        指定tcam 网卡 执行ping操作
        
        :param rmnet_data: 生成的网卡名 eg: rmnet_data0 rmnet_data1
        :param ping_time: 指定ping多少时长
        :return: 
        """

    @abstractmethod
    def bgm_ping_net(self, chanel, ping_time):
        """
        指定bgm 网卡 eth0.32 执行ping操作
        
        :param chanel: 指定网卡
        :param ping_time: 指定ping多少时长
        :return: 
        """
    
    @abstractmethod
    def bgm_ping_tcam(self):
        """
        执行 bgm ping tcam 操作
        
        :param ping_time: 指定ping多少时长
        :return: 
        """

    @abstractmethod
    def clear_fota_cache(self):
        """
        清空FOTA、UA缓存、状态文件
        
        :return:
        """
        
    @abstractmethod
    def ssh_reboot_bgm(self):
        """
        命令重启BGM
        
        :return:
        """
        
    @abstractmethod
    def init_bgm_tcpdump(self, local_path=None, bgm_path='/data/', **kwargs):
        """
        先推包到tmp 下，然后解压到 bgm_path 路径下
        
        :param local_path: 工具路径 如 /root/dbg-utils.tar.bz2
        :param bgm_path: 最后解压到那个路径下，建议 data 下
        :param kwargs:
        :return:
        """

    @abstractmethod
    def delete_bgm_tcpdump_file(self, bgm_log_name="*.pcap", path='/log/'):
        """
        删除 bgm 内部 tcpdump 文件

        :param bgm_log_name: 要删除的w
        :param path: 文件所在路径
        :return:
        """

    @abstractmethod
    def scp_bgm_log_to_local(self, bgm_log_name, log_path='/root/bgm_log', save_log_name=None, del_flag=False):
        """
         把 bgm 的日志 拉取到本地

        :param bgm_log_name:  拉取的是单个文件，或者压缩包，不能是文件夹
        :param log_path: 保存到本地的文件路径
        :param save_log_name: 保存到本地的文件名称 会加上时间戳
        :param del_flag: 是否删除原文件
        :return: 返回 文件全路径
        """

    @abstractmethod
    def scp_local_file_to_bgm(self, local_path, bgm_path='/tmp/'):
        """
        把 本地 文件推送到bgm tmp 下

        :param local_path: 上位机的路径  如 "/root/bgm_log/"
        :param bgm_path:
        :return: file_path
        """

    @abstractmethod
    def start_bgm_tcpdump(self, name="bgm_", iface="eth0.5", **kwargs):
        """
        开启 bgm 内部抓包

        :param name: 抓包存储 文件名 ，最后会加上时间
        :param iface:
        :param kwargs:
        :return: file_path, save_name
        """

    @abstractmethod
    def stop_bgm_tcpdump(self):
        """
        停止 bgm 内部抓包

        :return:
        """
    @abstractmethod
    def get_bgm_uptime(self):
        """
        获取 bgm 重启后的时间

        :return:
        """

    @abstractmethod
    def copy_factory_packages(self):
        """
        cp厂内OTA软件包

        :return:
        """
        
    @abstractmethod
    def add_state_file(self):
        """
        替换厂内OTA状态文件

        :return:
        """
        
    @abstractmethod
    def rm_factory_packages(self):
        """
        删除厂内OTA软件包

        :return:
        """
    
    @abstractmethod
    def rm_ua_packages(self, domain_name:DOMAIN):
        """
        删除域控 UA安装包, 制造Update Failed使用

        :param domain_name: 枚举类型 DOMAIN:class DOMAIN(BaseEnum):BGM = 0、TCAM = 1、CDC = 2、ACU = 3
        :return:
        """
        
    @abstractmethod
    def get_bgm_l7_constant(self):
        """
        获取BGM安全等级7安全常数

        :return: str
        """

    @abstractmethod
    def get_tcam_l7_constant(self):
        """
        获取TCAM安全等级7安全常数

        :return: str
        """
        
    @abstractmethod
    def check_file_existence(self, device_name: DeviceName, path: str, filename: str):
        """
        检查某域控某路径下是否有对应的包
        
        :param device_name: 枚举类型 DeviceName: class DeviceName(BaseEnum): BGM = 'BGM' TCAM = 'TCAM' ACU = 'ACU' CDCQ = 'CDCQ'
        :param path: 需要查询的路径
        :param filename: 需要查询的文件名
        :return:
        """
        
    @abstractmethod
    def check_ua_package(self, domain_name: DOMAIN):
        """
        检查某域控UA安装包是否存在
        
        :param domain_name: 枚举类型 DOMAIN: class DOMAIN(BaseEnum): BGM = 0 TCAM = 1 CDC = 2 ACU = 3
        :return:
        """
        
    @abstractmethod
    def set_network_mode(self, network_mode: Network_Mode):
        """
        设置TCAM网络类型
        
        :param network_mode: 枚举类型 Network_Mode: class Network_Mode(BaseEnum): Fourth_Generation = 0 Fifth_Generation = 1
        :return:
        """

    @abstractmethod
    def exec(self, cmd, bgm_ip=None):
        """
        通过BGM连接TCAM

        :param cmd: 执行的命令
        :param bgm_ip:为空时获取默认的bgm_ip 不为空时可以设置为继承TestBase时传的obd_ip,也可以自己输入正确的bgm_ip
        """
        
    @abstractmethod
    def get_log(self, device_name:DeviceName, local_path:str = '/', file_needed:str = '*', save_log_name:str = 'log.tar.gz', del_flag:bool = False):
        """
        打包域控log，并拉取到本地

        :param device_name: 枚举类型 DeviceName: class DeviceName(BaseEnum): BGM = 'BGM' TCAM = 'TCAM' ACU = 'ACU' CDCQ = 'CDCQ'
        :param local_path:需要拉取到的本地路径
        :param file_needed:需要拉取的日志
        :param save_log_name:保存打包的日志名
        :param del_flag:是否需要删除源打包文件
        :return:
        """
        
    @abstractmethod
    def clear_log(self, device_name:DeviceName):
        """
        清空域控log

        :param device_name: 枚举类型 DeviceName: class DeviceName(BaseEnum): BGM = 'BGM' TCAM = 'TCAM' ACU = 'ACU' CDCQ = 'CDCQ'
        :return:
        """
        
    @abstractmethod
    def get_domian_last_boot(self, domain_name:DOMAIN):
        """
        获取域控启动面

        :param domain_name: 枚举类型 DOMAIN: class DOMAIN(BaseEnum): BGM = 0 TCAM = 1 CDC = 2 CU = 3
        :return: last_boot
        """

    @abstractmethod
    def get_bgm_jetlog_msg_s2s_bst_names(self, timeout=60):
        """
        获取 bgm /log 下面所有 jetlog_messages  jetlog_s2s,jetlog_bts 的名字

        @return:[jetlog_messages],[jetlog_s2s],[jetlog_bts]
        """
        #

    @abstractmethod
    def get_log_from_bgm(self, log_name=None, save_path='/root/bgm_log', tar_bgm_path='/update/', log_type=None,
                timeout=600):
        """
        获取 bgm的日志 ： 可以获取单个文件 单个文件只能获取这三种类型的【jetlog_bts,jetlog_s2s,jetlog_messages】需要传递全名 带后缀 获取多个文件 会打包到  tar_bgm_path 路径下
        
        :param log_name: 单个文件名称，或者为None，如为None 则打包 log_type 类型的数据
        :param save_path: 本地保存的位置
        :param tar_bgm_path: 在bgm内部打包的位置，最好不要在 log下，log满的时候无法存储
        :param log_type: 拉取日志的类型 【jetlog_bts,jetlog_s2s,jetlog_messages，None】
        :param timeout:超时时间
        :return:
        """

    @abstractmethod
    def get_bgm_log(self, save_path='/root/bgm_log', tar_bgm_path='/update/', timeout=600):
        """
        拉取 bgm的 所有日志
        
        :param save_path: 本地保存的地址
        :param tar_bgm_path: 在bgm内部打包的位置，最好不要在 log下，log满的时候无法存储
        :param timeout:
        :return:
        """

    @abstractmethod
    def get_bgm_jetlog_bts(self, log_name=None, save_path='/root/bgm_log', tar_bgm_path='/update/', timeout=600):
        """
        拉取 bgm的 jetlog_bts 拉取单个文件

        :param log_name: 为 None 拉取所有的jetlog_bts 日志，传单个文件则拉取单个文件
        :param save_path: 本地保存的地址
        :param tar_bgm_path: 在bgm内部打包的位置，最好不要在 log下，log满的时候无法存储
        :param timeout:
        :return:
        """

    @abstractmethod
    def get_bgm_jetlog_s2s(self, log_name=None, save_path='/root/bgm_log', tar_bgm_path='/update/', timeout=600):
        """
        拉取 bgm的 jetlog_s2s 拉取单个文件

        :param log_name: 为 None 拉取所有的jetlog_bts 日志，传单个文件则拉取单个文件
        :param save_path: 本地保存的地址
        :param tar_bgm_path: 在bgm内部打包的位置，最好不要在 log下，log满的时候无法存储
        :param timeout:
        :return:
        """

    @abstractmethod
    def get_bgm_jetlog_messages(self, log_name=None, save_path='/root/bgm_log', tar_bgm_path='/update/',
                                timeout=600):
        """
        拉取 bgm的 jetlog_messages 拉取单个文件

        :param log_name: 为 None 拉取所有的jetlog_bts 日志，传单个文件则拉取单个文件
        :param save_path: 本地保存的地址
        :param tar_bgm_path: 在bgm内部打包的位置，最好不要在 log下，log满的时候无法存储
        :param timeout:
        :return:
        """

    @abstractmethod
    def get_bgm_coredump_names(self):
        """
           获取 文件名称

           :return: [（file_name, create_time）, (), .......]
        """

    @abstractmethod
    def get_bgm_coredump(self, dump_file_name=None, save_path='/root/bgm_log', tar_bgm_path='/update/',
                         timeout=10 * 60):
        """
        拉取 coredump 文件到 本地 save_path 下

        :param dump_file_name:  coredump  可以为单个文件;为 None 的时候，表示拉取所有的coredump 文件
        :param save_path: 本地保存的位置
        :param tar_bgm_path: 在bgm内部打包的位置，最好不要在 log下，log满的时候无法存储
        :return: 本地保存路径
        """

    @abstractmethod
    def clear_bgm_coredump(self, timeout=10):
        """
        清除bgm 下的所有 coredump

        :return:
        """

    @abstractmethod
    def clear_bgm_all_log(self):
        """
        清除所有报告 需要重启

        :return:
        """

    @abstractmethod
    def get_bgm_jetlog_msg_or_s2s_or_bst_del_names(self, log_list: list, log_type: str):
        """
        获取 删除的日志名称

        :param log_list:
        :param log_type:["jetlog_bts", "jetlog_messages", "jetlog_s2s"]
        :return:
        """

    @abstractmethod
    def clear_bgm_log_no_need_reset(self, timeout=10):
        """
        清除bgm的 日志 不需要重启bgm
        :param timeout:
        :return:
        """
    
    @abstractmethod
    def get_ping(self, ip=None, num=4, root_permission=False):
        """
        看 tcam 是否 ping 通 该 ip
        @param ip: 需要ping的 ip
        @param num: 尝试几次
        @return:
        """
    @abstractmethod   
    def get_arping(self, ip=None, num=4):
        """
        看 在bgm里是否能arping通
        @param ip: 需要arping的 ip
        @param num: 尝试几次
        @return:
        """

    @abstractmethod
    def retry_ping_mul_times(self, ip=None, num=4, retry=2, root_permission=False):
        """
        若失败则重试 ping 几次
        @param ip: 每次 ping 的 对象
        @param num: 每次 ping 4
        @param retry: 若失败 则 再次尝试2轮，每轮ping 4次
        @return:
        """
        
    @abstractmethod
    def rm_ccp_persist(self):
        """
        清除cco持久化文件
        @return:
        """
        
    # @Author:longlong.zhu
    @abstractmethod
    def check_metric_data(self, command: str, ip, *args):
        """
        检查持久化文件是否存在
        @param command: linux命令
        @param ip: TCAM IP
        @param args: 检测是否存在的依据
        @return:
        """
    
    # @Author:longlong.zhu
    @abstractmethod
    def check_vlan_conn(self,bgm_ip, vlan_ip, mac_address):
        """
        检查vlan连接
        @param bgm_ip: bgm的ip地址
        @param vlan_ip: vlan的ip地址
        @param mac_address: mac地址
        @return:
        """

    # @Author:dejian.xiong
    @abstractmethod
    def update_mcu_switch(self, obd_iface: str, software_path: str):
        """
        升级mcu的switch版本
        @param obd_iface: obd网卡
        @param software_path: switch版本路径，默认为工程版本可不传路径
        @return:
        """
    @abstractmethod
    def rescue_ua_skip(self):
        """
        导入手动救援开关"debug_inhibit_timeout"将timeout默认3H 改为5min 

        :return:
        """

    @abstractmethod
    def update_skip_debug_nokill(self, debug_list: list):
        """ 
        仅导入skidebug开关,不杀进程不重启
        
        @return:
        """

    # @Author:lei.song
    @abstractmethod
    def get_tcam_uptime(self):
        """
        获取tcam重启后的时间（单位：分钟）。
        
        Args:
            无
        
        Returns:
            int: tcam重启后的时间，单位：分钟。
        
        Raises:
            无
        """
        """
        获取 tcam 重启后的时间
        @return:
        """
    
    @abstractmethod
    def kill_bgm_process(self, process: BgmApp):
        """
        在bgm内kill指定进程
        @param process: 进程名
        @return:
        """
    
    @abstractmethod
    def rerun_bgm_process(self, process: BgmApp):
        """
        在bgm内重启指定进程，仅用于SIL环境，HIL中em2会主动拉
        @param process: 进程名
        @return:
        """
    
    @abstractmethod
    def is_bgm_process_running(self, process: BgmApp):
        """
        在域控内判断指定进程是否运行
        @param process: 进程名
        @return: (bool: 是否在运行, pid)
        """
    
    @abstractmethod
    def run_bgm_process(self, process: BgmApp):
        """
        在bgm内重启指定进程，仅用于SIL环境，HIL中em2会主动拉
        @param process: 进程名
        @return:
        """
    
    @abstractmethod
    def del_s2s_db(self):
        """
        删除s2s的数据库，一般用于测试默认配置
        @return:
        """
    
    @abstractmethod
    def del_SOAAPP_db(self):
        """
        删除SOAAPP的数据库，一般用于测试默认配置
        @return:
        """

    @abstractmethod
    def verify_time_synchronization(self, device_name: DeviceName, time_diff=2):
        """
        获取域控时间，判断是否时间同步

        Args:
            device_name (DeviceName): 设备名称
            time_diff (int, optional): 时间误差范围，默认为2秒

        Returns:
            None

        Raises:
            AssertionError: 当域控时间与当前时间相差超过time_diff秒时，抛出此异常
        """    
    
    @abstractmethod
    def get_bgm_second2last_jetlog_messages_name(self):
        '''
        日志分层的时候 防止日志取不全，获取倒数第二个日志的名字
        @return: 日志名字 jetlog_messages808_20241005091818_31ed136b2ff8467a98e90c4cda2ca443.zst
        '''

    @abstractmethod
    def download_factory_package_to_bgm(self, package_url: str):
        """
        下载厂内OTA包并解压到BGM
        Args:
            package_url (str): 厂内OTA包下载链接
        Returns:
            None
        """
        pass    
        
