"""
Author: liu.yang
Date: 2022-11-29 01:25:33
LastEditTime: 2023-05-10 13:45:33
FilePath: /yangliu/sat/xat_ecu/legacy/interface/bgm/bgm_ssh.py
Description: A utility class for ssh into bgm
"""
import os, sys
import base64
import pexpect
import json
from pathlib import Path

current_path = os.path.dirname(os.path.realpath(__file__))

from xat_ecu.legacy.sdk.ecu_sim_const import ECUSimConst
from xat_ecu.legacy.common.singleton import SingletonMeta
from xat_ecu.legacy.driver.ssh_interface import command_send, file_download, file_upload,  get_command_run_flag, set_command_run_flag
from xat_ecu.legacy.common.constant import BGM_CONSTANT
from xat_ecu.legacy.driver.ssh_client import *
from xat_ecu.legacy.interface.nuc_app import *
from xat_ecu.legacy.common.file_handle import parent_dir
import re
import datetime

soa_partner_path = Path(parent_dir) / "soa_partner"


class BGM_SSH:
    def __init__(self, hostname=None, connect_type='obd'):
        self.BGM = 'BGM'
        self.connect_type = connect_type

    @staticmethod
    def update_hostname():
        return get_obd_ip()

        # 自定义输入的命令

    def type_commands(self, commands, output=False, root_permission=True, timeout=60, **kwargs):
        ct = kwargs.get('connect_type')
        if ct is not None:
            connect_type = ct
        else:
            connect_type = self.connect_type
        status, outmsg = command_send(device_name=self.BGM, cmd=commands, timeout=timeout, connect_type=connect_type,
                                      **kwargs)
        logger.info(f'{commands}执行结果为:{outmsg}')
        return outmsg

    def get_uptime(self):
        # bgm 启动时间
        cmd = "uptime"
        data = self.type_commands(cmd)
        return data

    def get_build_date_utc(self):
        cmd = "cat /app/etc/build.prop | grep sys.build.date.utc| awk -F'=' '{print $2}'"
        data = self.type_commands(cmd)
        return data

    def get_version(self):
        cmd = "cat /app/etc/build.prop"
        data = self.type_commands(cmd)

        release = ''
        soa_version = ''
        jidl_version = ''
        bootes_version = ''
        version_release = None
        for i in data.split('\n'):
            i = i.strip()
            # if 'sys.build.version.release' in i:
            #     version_release = i.split('=')[-1]
            if 'sys.build.soa.version' in i:
                soa_version = i.split('=')[-1]
            if 'sys.build.jidl.version' in i:
                jidl_version = i.split('/')[-1]
            if 'sys.build.version.swpn' in i:
                release = i.split('=')[-1]
                version_release = f"v{release[-3]}.{release[-2]}.{release[-1]}"
                logger.debug(f"version_release:{version_release}")
            if 'sys.build.version.ver' in i:
                if len(i.split('=')[-1]) == 2:
                    release = release + ' ' + i.split('=')[-1]
                elif len(i.split('=')[-1]) == 3:
                    release = release + i.split('=')[-1]
                else:
                    exit('版本信息命名错误')
            if "sys.build.bootes.version" in i:
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

        # 得到BGM tprop的信息，aeskey、aesiv、cmac等
        # get_tprop()[0] ：tprop全部信息
        # get_tprop()[1] ：aeskey
        # get_tprop()[2] ：aesiv
        # get_tprop()[3] ：cmac

    def get_tprop(self, timeout=10):
        cmd1 = "export JIDU_APP_LOG_PATH=/log/;\
        export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib;\
        export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib/soa;\
        export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib/proxy;\
        export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/service/em;\
        export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/service/prop;\
        export ENV_APP_PATH=/app/;\
        export ENV_APP_INFO=/app/etc/AppInfo.json;\
        export ENV_SOA_CONFIG_PATH=/app/etc/soaconfig/;\
        export ENV_CONFIG_PATH=/app/etc/;cd /app/bin/; ./tprop get"
        cmd2 = "cd /app/bin/; ./prop.sh get"

        result = self.get_version()['build_version'][7:10]
        if result == "065":
            cmd = cmd1
        else:
            cmd = cmd2
        try:
            str1 = self.type_commands(cmd)
        except TimeoutError:
            root = pexpect.spawn(f"ssh root@172.16.5.1 '{cmd} > /log/salt'")
            if root.expect('password') == 0:
                root.sendline('mars1bgm')
            time.sleep(timeout)
            root.sendcontrol('c')
            str1 = self.type_commands("cat /log/salt")
        idx_asekey = str1.find('aeskey:')
        idx_aesiv = str1.find('aesiv:')
        idx_cmac = str1.find('cmac:')
        idx_init = str1.find("Init Proxy")
        aes_str = str1[idx_asekey + 9: idx_aesiv]
        iv_str = str1[idx_aesiv + 8: idx_cmac]
        cmac_str = str1[idx_cmac + 7: idx_init]
        return str1, aes_str, iv_str, cmac_str

    def clear_log(self):
        self.type_commands(commands="rm -rf /log/*")
        logger.info(f"清除BGM全部的log啦~")

    def clear_coredump(self, hours):
        self.type_commands(commands=f'find /log/coredump/ -name "*.core" -mmin +{hours * 60} -delete')
        logger.info(f"清除{hours}小时前的coredump文件")

    def get_log(self, my_local='/root', timeout=600):
        log_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(time.time()))
        cmd = 'cd /log;rm -f bgm_log.tar.gz;rm -f tcam_log.tar.gz;tar -cvf bgm_log.tar.gz ./*'
        self.type_commands(commands=cmd, timeout=timeout)
        file_download(device_name=self.BGM, remote_path='/log/bgm_log.tar.gz',
                      local_path=f'{my_local}/bgm_log_{log_time}.tar.gz')
        logger.info(f"bgm_log_{log_time}.tar.gz已经全部取到 {my_local} 路径下啦0")

    def get_salt_info(self, username=None, root_pwd=None, cmd=None):
        self.type_commands(commands='cd /tmp/jiduer/;export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib')
        self.type_commands(commands='chmod 777 ./soa_api_test')
        result = self.type_commands(commands='./soa_api_test')
        return result

    def get_prop(self):
        result = self.get_version()['build_version']
        result.strip(' ') or result.rstrip(' ')
        file_upload(device_name=self.BGM,
                    local_path=parent_dir + '/interface/bgm/soa_api_test',
                    remote_path='/tmp/')
        ret_str = self.type_commands(
            "cd /tmp/;chmod +x soa_api_test;export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib;./soa_api_test")
        logger.info(f"执行soa_api_test后输出的数据:\n{ret_str}")
        idx_vid = ret_str.find('mVid:')
        aes_hex = ret_str.find('aes_hex')
        idx_root_key = ret_str.find('Root key:')
        idx_l7_key = ret_str.find('L7 key:')
        idx_asekey = ret_str.find('Aeskey:')
        idx_aesiv = ret_str.find('AesIv:')
        idx_cmac = ret_str.find('CMAC:')
        vid = ret_str[idx_vid + 7: aes_hex]
        root = ret_str[idx_root_key + 11: idx_l7_key]
        l7 = ret_str[idx_l7_key + 9: idx_asekey]
        aes_str = ret_str[idx_asekey + 9: idx_aesiv]
        iv_str = ret_str[idx_aesiv + 8: idx_cmac]
        cmac_str = ret_str[idx_cmac + 7:]
        return vid, root, l7, aes_str, iv_str, cmac_str

    def get_set_salt(self):
        vid, root, l7, aes_str, iv_str, cmac_str = self.get_prop()
        aes_str_2 = aes_str.split()
        aes_key = getkey(aes_str_2)
        iv_str_2 = iv_str.split()
        iv_key = getkey(iv_str_2)
        cmac_str_2 = cmac_str.split()
        cmac_key = getkey(cmac_str_2)
        result = {"aes_key": aes_key, "aes_iv": iv_key, "cmac_key": cmac_key}
        logger.info(result)

        if (
                isinstance(aes_key, str)
                and isinstance(iv_key, str)
                and isinstance(cmac_key, str)
        ):
            if len(aes_key) >= 32 and len(iv_key) >= 32 and len(iv_key) >= 32:
                bootes_version = self.get_bootes_version()
                if bootes_version:
                    # bootes
                    salt_path = (
                        f"{soa_partner_path}/BootesRelease/out/x86/conf/salt.json"
                    )
                else:
                    # apus
                    salt_path = "./salt.json"
                with open(salt_path, mode="w", encoding="utf-8") as f:
                    json.dump(result, f, indent=4)
            else:
                logger.error("获取的 aes_key,aes_iv,cmac_key 长度不对, 不去更新 salt.json")
        else:
            logger.error("get salt 失败或 为None, 不去更新 salt.json")

        return result

    def get_vid(self):
        vid, root, l7, aes_str, iv_str, cmac_str = self.get_prop()
        vid_2 = vid.split()
        vid_key = getkey(vid_2)
        return vid_key

    def get_root_key(self):
        vid, root, l7, aes_str, iv_str, cmac_str = self.get_prop()
        root_2 = root.split()
        root_key = getkey(root_2)
        return root_key

    def get_l7_key(self):
        """
        获取L7接口信息
        """
        vid, root, l7, aes_str, iv_str, cmac_str = self.get_prop()
        l7_2 = l7.split()
        l7_key = getkey(l7_2)
        return l7_key

    def get_aes_key(self):
        vid, root, l7, aes_str, iv_str, cmac_str = self.get_prop()
        aes_str_2 = aes_str.split()
        aes_key = getkey(aes_str_2)
        return aes_key

    def get_aes_iv(self):
        vid, root, l7, aes_str, iv_str, cmac_str = self.get_prop()
        iv_str_2 = iv_str.split()
        iv_key = getkey(iv_str_2)
        return iv_key

    def get_cmac_key(self):
        vid, root, l7, aes_str, iv_str, cmac_str = self.get_prop()
        cmac_str_2 = cmac_str.split()
        cmac_key = getkey(cmac_str_2)
        return cmac_key

    def get_soa_jidl_name(self):
        result = self.get_version()
        return result.get("soa_name")

    def get_bootes_version(self):
        result = self.get_version()
        return result.get("bootes_version")

    def get_surface(self, cmd=None, root_permission=False):
        """
        获取 bgm 的切面
        @return:
        """
        if cmd is None:
            # cmd = "/app/bin/swdl -nr 8"
            cmd = "cat /proc/cmdline | awk -F 'apppart=' {'print $2'} | awk -F ' ' {'print $1'}"
        res = self.type_commands(cmd, root_permission=root_permission)
        logger.info(f"获取的 bgm 的当前切面为 {res}")
        return "A" if res == "0" else "B"

    def get_date_time_and_check(self, cmd=None, error_scop=5, time_diff=8, root_permission=False):
        """
        获取bgm 的系统时间，并校验是否和当前时间一致
        @param cmd:
        @param error_scop: 误差范围 单位为秒
        @param time_diff: 时差 相差 8 个小时
        @return:
        """

        if cmd is None:
            cmd = "date"
        res = self.type_commands(cmd, root_permission=root_permission)
        logger.info(f"根据{cmd}指令 获取的 bgm 时间为 {res}")
        result, time_str = self.get_time(
            res, error_scop=error_scop, time_diff=time_diff
        )
        return result, time_str

    def get_time(self, data_str, error_scop=20, time_diff=8):
        """
        @param data_str:  'Fri Mar  3 04:54:11 UTC 2023'
        @param error_scop:  误差范围 单位为秒
        @param time_diff:  时差 相差 8 个小时
        @return:
        """
        month_dict = {
            "Jan": "1月",
            "Feb": "2月",
            "Mar": "3月",
            "Apr": "4月",
            "May": "5月",
            "Jun": "6月",
            "Jul": "7月",
            "Aug": "8月",
            "Sept": "9月",
            "Oct": "10月",
            "Nov": "11月",
            "Dec": "12月",
        }
        week_dict = {
            "Mon": "星期一",
            "Tue": "星期二",
            "Wed": "星期三",
            "Thur": "星期四",
            "Fri": "星期五",
            "Sat": "星期六",
            "Sun": "星期日",
        }
        lis = data_str.replace("  ", " ").split(' ')
        month = month_dict.get(lis[1], lis[1])
        week = week_dict.get(lis[0], lis[0])
        date_str = lis[2]
        time_str = lis[3]
        year_str = lis[5]
        string = year_str + "-" + month[:1] + "-" + date_str + " " + time_str
        UTC_FORMAT = "%Y-%m-%d %H:%M:%S"
        utc_time = datetime.datetime.strptime(string, UTC_FORMAT)
        local_time = utc_time + datetime.timedelta(hours=time_diff)
        # logger.info(f'bgm 系统时间为{local_time} {week}')
        data_sj = time.strptime(
            local_time.strftime(UTC_FORMAT), "%Y-%m-%d %H:%M:%S"
        )  # 定义格式
        time_int = int(time.mktime(data_sj))
        current_time = time.time()
        print(time_int, current_time)
        logger.info(f'bgm 系统时间为{local_time} 对应的时间戳为{time_int},当前时间戳为{current_time}')
        temp = current_time - time_int
        if temp > error_scop:
            logger.info(f'bgm 系统时间和当前时间相差{temp}秒，')
            return False, string
        return True, string

    def get_ping(self, ip=None, num=4, root_permission=False):
        """
        看 tcam 是否 ping 通 该 ip
        @param ip: 需要ping的 ip
        @param num: 尝试几次
        @return:
        """
        if ip is None:
            ip = "www.baidu.com"
        cmd = f'ping {ip} -c {num}'
        String = self.type_commands(cmd, root_permission=root_permission)
        logger.info(f"获取的 bgm 的{cmd}的结果为 {String}")
        # . 匹配任意字符，除了换行符
        # + 匹配1个或多个的表达式
        # ? 匹配0个或1个由前面的正则表达式定义的片段，非贪婪方式
        # 查找丢失的 数据包
        regular = re.findall(f"received,(.+?)packet loss, time", String)
        if regular:
            value = regular[0].strip()
            logger.info(f"bgm  ping {ip} {num}次，丢包率为 {value}")
            if value == "100%":
                # 未ping 通
                return False
            else:
                return True
        return False

    def retry_ping_mul_times(self, ip=None, num=4, retry=2, root_permission=False):
        """
        若失败则重试 ping 几次
        @param ip: 每次 ping 的 对象
        @param num: 每次 ping 4
        @param retry: 若失败 则 再次尝试2轮，每轮ping 4次
        @return:
        """

        res = self.get_ping(ip=ip, num=num, root_permission=root_permission)
        while retry and not res:
            logger.info(f"第{retry}次尝试ping {str(ip)}")
            res = self.get_ping(ip=ip, num=num)
            retry -= 1
        return res

    def get_ping_baidu(self, num=4, retry=2, root_permission=False):
        """
        ping 百度
        @param num: 每次 ping 4
        @param retry: 若失败 则 再次尝试2轮，每轮ping 4次
        @return:
        """
        return self.retry_ping_mul_times(ip="www.baidu.com", num=num, retry=retry, root_permission=root_permission)

    def get_ping_8888(self, num=4, retry=2, root_permission=False):
        """
        ping 8.8.8.8
        @param num: 每次 ping 4
        @param retry: 若失败 则 再次尝试2轮，每轮ping 4次
        @return:
        """
        return self.retry_ping_mul_times(ip="8.8.8.8", num=num, retry=retry, root_permission=root_permission)

    def get_updata_factory_bin_files(self):
        """
        查询 bgm里面 update/factory 下的 bin 文件
        @return:
        """
        try:
            logger.info("查询 bgm里面 update/factory 下的 bin 文件")
            # cmd = "cd ./factory/; ls" # 1. 版本
            cmd = "cd /update/factory/; ls"  # 1.1
            bin_files = self.type_commands(cmd)
            logger.info(f"获取的 bin 文件为bin_files={bin_files}")
            if bin_files:
                # bin_files_list = bin_files.split('\n')
                ls = [i.split(' ') for i in bin_files.split('\n')]
                res = []
                dd = [res.extend(i) for i in ls]
                bin_files_list = [i.replace('\r', '') for i in res if i]
            else:
                bin_files_list = []
            logger.info(f"获取的 bin 文件为 个数为{len(bin_files_list)},{bin_files_list}")
            return bin_files_list
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/bgm/bgm_ssh.py")
            logger.error(str(e))
            return []

    def remove_updata_factory_bin_files(self):
        """
        删除 bgm里面 update/factory 下的 bin 文件
        @return:
        """
        try:
            logger.info("开始 删除 bgm里面 update/factory 下的 bin 文件")
            # cmd = "rm -rf /home/root/factory/*" # 1.0 版本
            cmd = "rm -rf /update/factory/*"  # 1.1
            String = self.type_commands(cmd)

            # 获取下 是否删除
            bin_files = self.get_updata_factory_bin_files()
            if bin_files:
                logger.error(" 删除 bgm里面 update/factory 下的 bin 文件失败！！！")
                return 0
            else:
                logger.info(" 删除 bgm里面 update/factory 下的 bin 文件成功 ！！！")
                return 1

        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/bgm/bgm_ssh.py")
            logger.error(str(e))
            return 0

    def get_ts_security(self):
        cmd = "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib;\
                export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib/soa;\
                export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib/proxy;\
                export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/service/em;\
                export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/service/prop;\
                export ENV_APP_PATH=/app/;\
                export ENV_APP_INFO=/app/etc/AppInfo.json;\
                export ENV_SOA_CONFIG_PATH=/app/etc/soaconfig/;\
                export ENV_CONFIG_PATH=/app/etc/;\
                export UDSDOIP_CONFIG_PATH=/app/bin/udsconfig/;\
                export UDSDOIP_DATA_PATH=/data/uds/;\
                export BOOTES_HOME_DIR=/app/etc;"
        self.type_commands(commands=cmd)
        cmd = "/app/bin/ts_security -m test1 -d 0123456 | head -3 | tail -1"
        out = self.type_commands(commands=cmd)
        return out

    def init_bgm_tcpdump(self, local_path=None, bgm_path='/data/', **kwargs):
        """
        先推包到tmp 下，然后解压到 bgm_path 路径下
        @param local_path: 工具路径 如 /root/dbg-utils.tar.bz2
        @param bgm_path: 最后解压到那个路径下，建议 data 下
        @param kwargs:
        @return:
        """
        # if "tcpdump" in self.type_commands(f'ls {bgm_path}', timeout=2):
        #     logger.info(f"{bgm_path}tcpdump已存在")
        #     return
        # if "dbg-utils" in self.type_commands(f'ls {bgm_path}', timeout=2):
        #     logger.info(f"{bgm_path}dbg-utils已存在")
        # else:
        if local_path is None:
            local_path = os.path.join(os.path.dirname(__file__), 'dbg-utils.tar.bz2')
        # 推送 工具到 bgm 内 tmp 下
        connect_type = kwargs.get('connect_type', 'vlan')
        if "dbg-utils.tar.bz2" not in self.type_commands('ls /tmp/', timeout=2):
            logger.info(f"推送 debug 工具{local_path}到bgm tmp 下面")
            self.scp_local_file_to_bgm(local_path=local_path, bgm_path='/tmp/', connect_type=connect_type)

        logger.info(f"解压 工具 到bgm {bgm_path}下面")
        cmd = kwargs.get('cmd', f'tar xjf /tmp/dbg-utils.tar.bz2 -C {bgm_path}')
        logger.info("开始===》》》解压包")
        self.type_commands(commands=cmd)
        logger.info("解压包===》》》完成")
        self.type_commands("cd /data;cp dbg-utils/bin/tcpdump ./;chmod +x tcpdump", timeout=2)

    def delete_bgm_tcpdump_file(self, bgm_log_name="*.pcap", path='/update/'):
        """
        删除 bgm 内部 tcpdump 文件
        @param bgm_log_name: 要删除的w
        @param path: 文件所在路径
        @param kwargs:
        @return:
        """
        if bgm_log_name.endswith('pcap'):
            pass
        elif bgm_log_name.endswith('*'):
            pass
        else:
            bgm_log_name = bgm_log_name + "*"
        file_path = os.path.join(path, bgm_log_name)
        cmd = f"rm -f {file_path}"
        logger.info(f"删除bgm  {file_path}")
        self.type_commands(commands=cmd, timeout=5)
        logger.info(f"删除bgm  {file_path} 成功")

    def scp_bgm_log_to_local(self, bgm_log_name, log_path='/root/bgm_log', save_log_name=None, del_flag=False,
                             **kwargs):
        """
         把 bgm 的日志 拉取到本地
        @param bgm_log_name:  拉取的是单个文件，或者压缩包，不能是文件夹
        @param log_path: 保存到本地的文件路径
        @param save_log_name: 保存到本地的文件名称 会加上时间戳
        @param del_flag: 是否删除原文件
        @return:
        """
        # 取单个文件 单个文件的名字
        bgm_log_path = kwargs.get("path", "/update")
        connect_type = kwargs.get('connect_type', 'vlan')

        log_time = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime(time.time()))
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        logger.info(f"获取单个文件名字为{save_log_name}")
        if save_log_name is None:
            save_log_name = bgm_log_name

        name = f"{log_time}_{save_log_name}"
        logger.info(f"获取单个文件名字为{name}")

        file_path = os.path.join(log_path, name)
        logger.info(f"生成的文件路径为==》》{file_path}")

        full_path = os.path.join(bgm_log_path, bgm_log_name)
        file_download(device_name=self.BGM, remote_path=f'{full_path}', local_path=file_path, connect_type=connect_type)
        logger.info(f"bgm 的日志 已经取出，路径为==》》》{file_path}")
        if del_flag:
            remote_path = os.path.join(bgm_log_path, bgm_log_name)
            cmd = f"rm -f {remote_path}"
            logger.info(f"删除bgm  {remote_path}")
            self.type_commands(commands=cmd, timeout=5)
            logger.info(f"删除bgm  {remote_path} 成功")
        return file_path

    def scp_local_file_to_bgm(self, local_path, bgm_path='/tmp/', connect_type="vlan"):
        """
        把 本地 文件推送到bgm tmp 下
        @param local_path:  上位机的路径  如 "/root/bgm_log/"
        @param bgm_path:
        @param connect_type:
        @return:
        """
        self.type_commands("ls")  # 超时60s，可以防止重启后直接调用file_upload，未进行等待重连ssh，直接判ssh连接失败
        file_upload(device_name=self.BGM, local_path=local_path, remote_path='/tmp/', connect_type=connect_type)
        if bgm_path not in ["/tmp/", "/tmp"]:
            name = [i for i in local_path.split('/') if i.split()][-1]
            if os.path.isdir(local_path):
                cmd = f"mv -r /tmp/{name} {bgm_path}"
            else:
                cmd = f"mv /tmp/{name} {bgm_path}"
            try:
                logger.info(f"从bgm /tmp下移动文件{name}或者文件夹到bgm {bgm_path}下")
                self.type_commands(commands=cmd)
                logger.info(f"从bgm /tmp下移动文件{name}或者文件夹到bgm {bgm_path}下完成 ")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/bgm/bgm_ssh.py")
                logger.error(f"从bgm /tmp下移动文件{name}或者文件夹到bgm {bgm_path}下失败 {str(e)}")

    def tar_debug_utils(self, **kwargs):
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

    def start_bgm_tcpdump(self, name="bgm_", iface="eth0.5", **kwargs):
        """
        开启 bgm 内部抓包
        @param name:  抓包存储 文件名 ，最后会加上时间
        @param kwargs:
        @return:
        """
        # 抓包指令
        cmd = kwargs.get('cmd', None)
        # 保存路径，默认保存在bgm 里面的 /log 下
        path = kwargs.get("path", "/update")
        # 抓包长度
        eth_len = kwargs.get("eth_len", 0)
        otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))
        save_name = f"{name}{otherStyleTime}.pcap"
        file_path = os.path.join(path, save_name)
        # 抓包 指令
        if cmd is None:
            #     cmd = f'export PATH=$PATH:/data/dbg-utils/bin:/data/dbg-utils/usr/bin;tcpdump -i {iface} -w {file_path}'
            _path = str(__import__("pathlib").Path(__file__).resolve().parent)
            connect_type = kwargs.get('connect_type', 'vlan')
            self.push_file_to_bgm_data(os.path.join(_path, "tcpdump"), connect_type=connect_type)
            cmd = f'cd /data/;chmod +x tcpdump;/data/tcpdump -i {iface} -vvv -w {file_path}'
            if eth_len:
                cmd += f" -s {eth_len}"
        # 检查包是否存在，如果不存在，或者大小异常，则重新推送tcpdump至bgm内
        if "tcpdump" not in self.type_commands('ls /data/', timeout=2):
            logger.info(f"/data/目录下 没有找到tcpdump文件，重新推送tcpdump至bgm内")
            self.init_bgm_tcpdump()  # 开启抓包前，推送tcpdump至bgm内
        else:
            if "5.6M" not in self.type_commands('du -sh /data/tcpdump', timeout=2):
                logger.info(f" /data/目录下的tcpdump文件大小异常，重新推送tcpdump至bgm内")
                self.init_bgm_tcpdump()
            else:
                logger.info(f"tcpdump 已在/data/目录下，且大小5.6M")
        set_command_run_flag(False)  # 将命令执行状态置为 False
        t = threading.Thread(target=self.__start_bgm_tcpdump, args=(cmd,))
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

    def stop_bgm_tcpdump(self):
        """
        停止 bgm 内部抓包
        @return:
        """
        cmd = "\x03"
        logger.info(f"停止 ====》》》bgm 内部 tcpdump 抓包 cmd={cmd}")
        try:
            self.type_commands(commands=cmd, timeout=5)
            logger.info(f"停止 ====》》》bgm 内部 tcpdump 抓包 成功！！")
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/bgm/bgm_ssh.py")
            logger.error(f"停止 ====》》》bgm 内部 tcpdump 抓包失败 {str(e)}！！")

    def __start_bgm_tcpdump(self, cmd):
        """
        开启bgm 内部抓包
        @param cmd:
        @return:
        """
        logger.info(f"开启====》》》 bgm 内tcpdump抓包{cmd}")
        self.type_commands(cmd)

    def scp_bgm_file_to_local(self, bgm_file_pah, local_path, hostname=None, timeout=60, del_flag=False, **kwargs):
        '''
        拉取 bgm 的文件到本地
        @param bgm_file_pah:
        @param local_path:
        @param hostname:
        @return:
        '''
        # 有时候需要通过obd 获取ip
        connect_type = kwargs.get('connect_type', 'vlan')
        logger.info(f"生成的文件路径为==》》{local_path}")
        file_download(device_name=self.BGM, local_path=local_path, remote_path=bgm_file_pah, connect_type=connect_type)
        logger.info(f"bgm 的日志 已经取出，路径为==》》》{local_path}")

        if del_flag:
            # remote_path = os.path.join(bgm_log_path, bgm_log_name)
            cmd = f"rm -f {bgm_file_pah}"
            logger.info(f"删除bgm  {bgm_file_pah}")
            self.type_commands(commands=cmd, timeout=5)
            logger.info(f"删除bgm  {bgm_file_pah} 成功")

    def copy_coredump(self, dump_file, bench_tmp_path, hostname=None, timeout=10 * 60):
        '''
        拉取 coredump 文件到 本地 bench_tmp_path 下

        @param dump_file:  coredump  可以为单个文件;为 None 的时候，表示拉取所有的coredump 文件
        @param bench_tmp_path:
        @param hostname:
        @return:
        '''

        # 取单个文件 单个文件的名字
        log_time = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime(time.time()))
        if not os.path.exists(bench_tmp_path):
            os.makedirs(bench_tmp_path)
        if dump_file is None:
            #
            cmd = f"cd /log/coredump/;rm -f bgm_coredump.tar.gz;rm -f tcam_log.tar.gz;tar -zcvf bgm_coredump.tar.gz ./*"
        else:
            cmd = f"cd /log/coredump/;rm -f bgm_coredump.tar.gz;rm -f tcam_log.tar.gz;tar -zcvf bgm_coredump.tar.gz ./{dump_file}"

        logger.info(f">>>>>>>>>>>>>>>>开始打包 bgm coredump 日志 需要一定时间<<<<<<<<<<<<<<<<<<<<")
        t = time.time()
        self.type_commands(commands=cmd, timeout=timeout)
        logger.info(f"打包 bgm coredump 日志 结束{time.time() - t}秒")
        # 日志特别大 需要压缩，单个也需要压缩
        bgm_file_pah = f'/log/coredump/bgm_coredump.tar.gz'
        name = f"{log_time}_bgm_coredump.tar.gz"
        logger.info(f"{dump_file}对应的 压缩包为{name}")
        local_path = os.path.join(bench_tmp_path, name)
        t1 = time.time()
        self.scp_bgm_file_to_local(bgm_file_pah, local_path, hostname=hostname)
        logger.info(f"拉取文件耗时{time.time() - t1}秒")

    def get_bgm_coredump(self):
        '''
        获取 文件名称
        @return: [（file_name, create_time）, (), .......]
        '''
        #
        result_lis = []
        UTC_FORMAT = "%Y-%m-%d %H:%M:%S"
        # 先判断 有没有coredump 文件夹

        cmd = 'ls  /log'
        ret_value = self.type_commands(cmd)
        if 'coredump' not in ret_value:
            return result_lis

        cmd = 'cd  /log/coredump;ls --full-time'
        ret_list = self.type_commands(cmd)
        if not ret_list:
            logger.warning("获取coredump 文件 异常")
            return result_lis
        logger.info(f"获取coredump===》》》{ret_list}")
        lis = [item for item in ret_list.split('\n')[1:] if item]

        for item in lis:
            item_lis = item.split(' ')
            name = item_lis[-1].replace('\r', "")
            creat_time = item_lis[-4] + " " + item_lis[-3].split('.')[0]
            utc_time = datetime.datetime.strptime(creat_time, UTC_FORMAT)
            local_time = utc_time + datetime.timedelta(hours=8)
            result_lis.append((name, str(local_time)))
        return result_lis

    def get_cpu_idle(self, times=1, delay_time=1, hostname=None, **kwargs):
        '''
        获取 bgm总体cpu idle数值，获取单个则是瞬时值，可以获取多次取平均值
        @param times:  获取几次
        @param delay_time:  间隔多久获取一次
        @param hostname:
        @param kwargs:
        @return:
        '''
        # 指定 那种方式获取，为1 则是如果有多次取值，则直接在bgm 里面取完退出；为0 则是每取一次后退出，重新再进去取值
        get_type = kwargs.get("get_type", 1)
        if get_type:
            # 一次 直接获取够次数 再出来
            cmd = f"top -d {delay_time} -n {times}" + " | grep Cpu | awk '{print $8}'"
            logger.info(f"执行指令===》》》{cmd}")
            timeout = times * delay_time + 20
            # 获取 文件名称
            bgm_cpu = self.type_commands(cmd, timeout=timeout)
            logger.info(f"bgm CPU空闲率={bgm_cpu}")

            cpu_infos = [float(i) for i in bgm_cpu.split("\n") if i.strip()]

            aver_cpu = sum(cpu_infos) / len(cpu_infos)
            aver_cpu = round(aver_cpu, 2)
            temp = round(100 - aver_cpu, 2)
            logger.info(f"bgm CPU空闲率={aver_cpu},使用率为={temp}")
            # 返回平均使用率，和 每次获取的空闲率
            return aver_cpu
        else:
            # 每次获取一次，循环获取
            cmd = "top  -n 1 | grep Cpu | awk '{print $8}'"
            logger.info(f"执行指令===》》》{cmd}")
            cpu_infos = []
            timeout = delay_time + 20
            for i in range(times):
                # 获取 文件名称
                bgm_cpu = self.type_commands(cmd, timeout=timeout)
                logger.info(f"bgm CPU空闲率={bgm_cpu}")
                cpu = bgm_cpu.replace("\n", "").strip()
                if cpu:
                    cpu_infos.append(float(cpu))
                time.sleep(delay_time)

            aver_cpu = sum(cpu_infos) / len(cpu_infos)
            temp = round(100 - aver_cpu, 2)
            logger.info(f"bgm CPU空闲率={aver_cpu},使用率为={temp}")
            # 返回平均使用率，和 每次获取的空闲率
            return aver_cpu

    def get_cpu_and_men_used(self, process_name="s2s_ser+", times=1, delay_time=1, hostname=None, **kwargs):
        '''
        获取 返回bgm中给定进程的cpu占用和 内存占用，获取单个则是瞬时值，可以获取多次取平均值
        @param times:  获取几次
        @param delay_time:  间隔多久获取一次
        @param hostname:
        @param kwargs:
        @return      %CPU   %MEM   RES
        '''

        # PID  USER      PR  NI    VIRT     RES    SHR    S  %CPU   %MEM     TIME+      COMMAND
        # 331  s2s_ser+  20   0    3458336  83800  20676  S   5.6   9.6     149:36.03     s2s_service

        # 指定 那种方式获取，为1 则是如果有多次取值，则直接在bgm 里面取完退出；为0 则是每取一次后退出，重新再进去取值
        get_type = kwargs.get("get_type", 1)
        if get_type:
            # 一次 直接获取够次数 再出来
            cmd = f"top -d {delay_time} -n {times} | grep {process_name}"
            logger.info(f"执行指令===》》》{cmd}")
            timeout = times * delay_time + 20
            # 获取 文件名称
            bgm_cpu = self.type_commands(cmd, timeout=timeout)
            logger.info(f"bgm {process_name}进程 ={bgm_cpu}")
            data = bgm_cpu.split('\n')
            logger.info(f"bgm 的s2s data ===>>> {data}")
            cpu_infos = []
            for item in data:
                if not item.strip():
                    continue
                a = [i.strip() for i in item.split(' ') if i.strip()]
                logger.info(f"bgm s2s  ===>>> {a}")
                cpu_infos.append((int(a[6]), float(a[9]), float(a[10])))
            res_v = int(sum([item[0] for item in cpu_infos]) / len(cpu_infos))
            cpu_v = round(sum([item[1] for item in cpu_infos]) / len(cpu_infos), 2)
            MEM_v = round(sum([item[2] for item in cpu_infos]) / len(cpu_infos), 2)
            logger.info(f"台架上 {process_name} CPU 平均值={cpu_v},使用空间平均值={res_v}")
            # 返回服务的 cpu 使用率 ，内存占用率，以及内存使用大小 单位kb
            return cpu_v, MEM_v, res_v
        else:
            # 每次获取一次，循环获取
            cmd = f"top  -n 1 | grep {process_name}"
            logger.info(f"执行指令===》》》{cmd}")
            cpu_infos = []
            timeout = delay_time + 20
            for i in range(times):
                # 获取 文件名称
                bgm_cpu = self.type_commands(cmd, timeout=timeout)
                logger.info(f"bgm {process_name}进程 ={bgm_cpu}")
                cpu = bgm_cpu.replace("\n", "").strip()
                if cpu:
                    a = [i for i in cpu.split(' ') if i.strip()]
                    cpu_infos.append((int(a[6]), float(a[9]), float(a[10])))
                time.sleep(delay_time)
            res_v = int(sum([item[0] for item in cpu_infos]) / len(cpu_infos))
            cpu_v = round(sum([item[1] for item in cpu_infos]) / len(cpu_infos), 2)
            MEM_v = round(sum([item[2] for item in cpu_infos]) / len(cpu_infos), 2)

            logger.info(f"台架上 {process_name} CPU 平均值={cpu_v},使用空间平均值={res_v}")
            # 返回服务的 cpu 使用率 ，内存占用率，以及内存使用大小 单位kb
            return cpu_v, MEM_v, res_v

    def flash_bgm_mpu(self, version, version_software):
        '''
        单独刷写 bgm_mpu
        @param version: 版本号：例如v1.0 v1.1 v1.3
        @param version_software: 软件版本版本号 例如 RD
        '''
        try:
            username = base64.b64decode(ECUSimConst.SOA_PUBLIC.encode()).decode()
            password = base64.b64decode(ECUSimConst.SOA_PUBLIC_PD.encode()).decode()

            dir_path = version + "_" + version_software
            if not os.path.isdir(dir_path):
                os.mkdir(dir_path)
            files = ['flash.bin', 'flash_a1.bin', 'imx8dxl-mars1-bgm-fit.itb', 'rootfs.img.bz2', 'appfs.img.bz2',
                     'mem-snapshotA.img.bz2', 'mem-snapshotB.img.bz2', 'version.txt']
            if version == 'v1.0.0':
                download_url = f"https://repo.jidudev.com/artifactory/BGMSoftware/Release/v1.0.0/6160110100{version_software}/6160110100{version_software}.zip!/image/"
            elif version == 'v1.1.0':
                download_url = f"https://repo.jidudev.com/artifactory/BGMSoftware/Release/v1.1.0/6160110110{version_software}/6160110110{version_software}.zip!/image/"
            elif version == 'v1.3.0':
                download_url = f"https://repo.jidudev.com/artifactory/BGMSoftware/Release/v1.3.0/6160110130{version_software}/6160110130{version_software}.zip!/image/"
            else:
                logger.info("version不存在 请检查一下输入的version是否正确")
                assert False, 'version不存在 请检查一下输入的version是否正确'

            logger.info("开始下载刷写mpu的文件")
            for file in files:
                file_path = f'./{dir_path}/{file}'
                if os.path.isfile(file_path):
                    logger.info("Path: {} is exit, need not to download".format(file_path))
                else:
                    logger.info(f"开始下载{file}")
                    download_cmd = "curl -u {0}:{1} -o {2} {3} ".format(username, password, file_path,
                                                                        download_url + file)
                    os.system(download_cmd)

            res = []
            for path in os.listdir(dir_path):
                if os.path.isfile(os.path.join(dir_path, path)):
                    res.append(path)
            logger.info("文件下载完成 开始推送mpu刷写包")
            for i in res:
                logger.info(i)
                self.scp_local_file_to_bgm(f'./{dir_path}/{i}', '/update/')
            logger.info("文件下载完成 开始推送刷写工具")
            self.scp_local_file_to_bgm(parent_dir + '/interface/bgm/dd_update_bgm_s2d.sh',
                                       '/update/')
            logger.info("执行dd_update_bgm_s2d.sh 开始刷写mpu")
            cmd = 'cd /update ; chmod 777 dd_update_bgm_s2d.sh ; ./dd_update_bgm_s2d.sh'
            outmsg = self.type_commands(cmd, timeout=1800)
            logger.info(outmsg)
            if 'dd update Success' in outmsg:
                logger.info('mpu刷写成功')
            elif 'dd update Failed' in outmsg:
                logger.info('mpu刷写失败')
                assert False, 'dd update Failed,mpu刷写失败'
            else:
                logger.info('未知错误,mpu刷写失败')
                assert False, '未知错误,mpu刷写失败'

            logger.info("刷写完成 读取版本号校验")
            result = self.get_version()
            if version == 'v1.0.0':
                assert result['build_version'] == f'6160110100 {version_software}', '刷写完成但读取版本号校验与预期刷写版本不一致'
                logger.info(f"刷写完成 版本号一致:{result['build_version']}")
            elif version == 'v1.1.0':
                assert result['build_version'] == f'6160110110 {version_software}', '刷写完成但读取版本号校验与预期刷写版本不一致'
                logger.info(f"刷写完成 版本号一致:{result['build_version']}")
            elif version == 'v1.3.0':
                assert result['build_version'] == f'6160110130 {version_software}', '刷写完成但读取版本号校验与预期刷写版本不一致'
                logger.info(f"刷写完成 版本号一致:{result['build_version']}")
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/bgm/bgm_ssh.py")
            logger.info(f"ERROR:{e}")
            assert False

    def delete_debug_script_executed_count(self):
        # 删除计数文件，否则计数到20 debug 文件会丢失
        cdm = "rm /data/debug_script_executed_count"
        self.type_commands(cdm)

    def create_bgm_uatest_file(self):
        '''
        在bgm 里面创建 uatest 文件
        @return:
        '''
        cmd_exe = "ls /data/"
        string = self.type_commands(cmd_exe)
        if "uatest" not in string:
            cmd_exe = "mkdir /data/uatest"
            self.type_commands(cmd_exe)

    def set_bgm_sync(self):
        '''
        同步一下
        @return:
        '''
        cmd = "sync"
        self.type_commands(cmd)

    def push_file_to_bgm_data(self, file_path, bgm_path="/data/", **kwargs):
        '''
        把文件推送到 bgm 的 bgm_path 路径下
        @param file_path:
        @param bgm_path:
        @return:
        '''
        # 最多尝试推送次数，默认三次
        retry_times = kwargs.get("retry_times", 3)
        file_name = os.path.basename(file_path)
        # if file_path is None:
        #     file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'config/{file_name}')

        for i in range(retry_times):
            connect_type = kwargs.get('connect_type', 'vlan')
            self.scp_local_file_to_bgm(file_path, bgm_path=bgm_path, connect_type=connect_type)
            # 判断是否有 文件
            cmd = f"ls {bgm_path}"
            ret = self.type_commands(cmd)
            name_List = ret.split()
            logger.warning(f"name_List=》》{name_List}")
            if file_name not in name_List:
                if i == 2:
                    assert 0, f"{file_name} 未上传成功"
                time.sleep(1)
            else:
                return

    def push_debug_file_to_bgm_data(self, debug_path=None, bgm_path="/data/", ):
        '''
        把 debug.sh 文件 推送到 bgm 的data 路径下
        @return:
        '''
        if debug_path is None:
            debug_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      'bgm_env/config/mcu_update_config/debug.sh')
        logger.info(f"local_path=====》》{debug_path} ")
        self.push_file_to_bgm_data(debug_path, bgm_path)

    def push_bgm_app_env_file_to_bgm_data(self, bgm_app_env_path=None, bgm_path="/data/", ):
        '''
        把 bgm_app_env.sh 文件 推送到 bgm 的data 路径下
        @return:
        '''
        if bgm_app_env_path is None:
            bgm_app_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                            'bgm_env/config/mcu_update_config/bgm_app_env.sh')
        logger.info(f"local_path=====》》{bgm_app_env_path} ")
        self.push_file_to_bgm_data(bgm_app_env_path, bgm_path)

    def push_app_info_json_file_to_bgm_data(self, app_info_json_path=None, bgm_path="/data/etc/", ):
        '''
        把 app_info.json 文件 推送到 bgm 的 /data/etc/ 路径下
        @return:
        '''

        if app_info_json_path is None:
            app_info_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                              'bgm_env/config/mcu_update_config/app_info.json')
        logger.info(f"local_path=====》》{app_info_json_path} ")
        self.push_file_to_bgm_data(app_info_json_path, bgm_path)

    def push_ua_files_to_bgm_data(self, version_release, bgm_path="/data/uatest/"):
        '''
         libua_service.so  ua_client_app  ua_server_app
         ua相关动态库与app：libua_service.so、ua_client_app、ua_server_app拷贝到bgm中/data/uatest/目录下，
         修改文件权限”chmod 777 /data/uatest/*"

        @param bgm_path:
        @return:
        '''

        # 判断uatest 文件是否存在
        ua_files_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(ua_files_path, 'bgm_env/config/mcu_update_config/')
        files = [f[1:] for f in os.listdir(path) if f.startswith("v")]
        files.sort()
        files.reverse()
        logger.info(f"获取的到 配置文件版本号有{files}，当前bgm的 版本号为{version_release}")
        if version_release is None:
            version_release = "v" + files[0]
            logger.info(f"未获取到版本号，则用最新的配置{version_release}")

            libua_service_path = os.path.join(ua_files_path,
                                              f'bgm_env/config/mcu_update_config/{version_release}/libua_service.so')
            ua_client_app_path = os.path.join(ua_files_path,
                                              f'bgm_env/config/mcu_update_config/{version_release}/ua_client_app')
            ua_server_app_path = os.path.join(ua_files_path,
                                              f'bgm_env/config/mcu_update_config/{version_release}/ua_server_app')
        else:
            if version_release < 140:
                libua_service_path = os.path.join(ua_files_path,
                                                  'bgm_env/config/mcu_update_config/v130/libua_service.so')
                ua_client_app_path = os.path.join(ua_files_path, 'bgm_env/config/mcu_update_config/v130/ua_client_app')
                ua_server_app_path = os.path.join(ua_files_path, 'bgm_env/config/mcu_update_config/v130/ua_server_app')
            else:
                # 获取路径下所有文件
                version_release = "v" + str(version_release).zfill(3)
                # version_release='v140'
                logger.info(f"采用的配置文件版本为{version_release}")
                libua_service_path = os.path.join(ua_files_path,
                                                  f'bgm_env/config/mcu_update_config/{version_release}/libua_service.so')
                ua_client_app_path = os.path.join(ua_files_path,
                                                  f'bgm_env/config/mcu_update_config/{version_release}/ua_client_app')
                ua_server_app_path = os.path.join(ua_files_path,
                                                  f'bgm_env/config/mcu_update_config/{version_release}/ua_server_app')

        logger.info(f"local_path=====》》{ua_files_path} ")
        cmd_exe = "ls /data/uatest/"
        string = self.type_commands(cmd_exe)
        if "libua_service.so" not in string:
            self.push_file_to_bgm_data(libua_service_path, bgm_path)
        if "ua_client_app" not in string:
            self.push_file_to_bgm_data(ua_client_app_path, bgm_path)
        if "ua_server_app" not in string:
            self.push_file_to_bgm_data(ua_server_app_path, bgm_path)
        # ”chmod 777 /data/uatest/*"
        cmd_exe = "chmod 777 /data/uatest/*"
        self.type_commands(cmd_exe)

    def push_ua_file_info_json_to_bgm_data(self, app_info_json_path=None, bgm_path="/data/jiarui/"):
        '''
        把 ua_file_info.json 文件 推送到 bgm /data/jiarui/
        @return:
        '''
        cmd_exe = "ls /data/"
        string = self.type_commands(cmd_exe)
        if "jiarui" not in string:
            cmd_exe = "mkdir /data/jiarui"
            self.type_commands(cmd_exe)

        if app_info_json_path is None:
            app_info_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                              'bgm_env/config/mcu_update_config/ua_file_info.json')
        logger.info(f"local_path=====》》{app_info_json_path} ")
        self.push_file_to_bgm_data(app_info_json_path, bgm_path)

    def set_bgm_start_type(self, start_type=0, **kwargs):
        '''
         # 切换 启动模式
         冷启动” /app/bin/swdl -nw 10 0“。
         热启动指令：/app/bin/swdl -nw 10 1
        @param start_type:
        @param kwargs:
        @return:
        '''

        if not isinstance(start_type, int):
            assert 0, "start_type 为整形，0或者1"

        retry_times = kwargs.get("retry_times", 4)
        get_cmd = "cat /sys/power/sys_resumed"
        set_cdm = f" /app/bin/swdl -nw 10 {start_type}"
        ret_value = 0 if start_type else 1
        for i in range(retry_times):
            ret = self.type_commands(commands=get_cmd).strip()
            logger.info(f"执行指令{get_cmd}》》》{ret}")
            if ret and int(ret[0]) == ret_value:
                logger.info(f"已经是{ret_value}模式")
                return
            else:
                # 切模式
                self.type_commands(set_cdm)
                if i == 3:
                    logger.info(f"尝试{retry_times}切模式失败")
                    # assert 0, f"尝试{retry_times}切模式失败"

    def set_bgm_hot_start(self):
        '''
        切换bgm 热启动
        @return:
        '''
        self.set_bgm_start_type(0)

    def set_bgm_cold_start(self):
        '''
        切换 冷启动
        @return:
        '''
        self.set_bgm_start_type(1)

    def get_jetlogs(self, save_path='.', mintime=0, maxtime=209912312460):
        '''
        根据所填时间范围 拉取对应时间段的jetlogs mintime最小时间 maxtime最大时间 时间格式年月日小时分钟 例如2023-11-13-15-21 就是202311131521
        @return:
        '''
        if not os.path.isdir(save_path):
            os.mkdir(save_path)
        outmsg = self.type_commands('ls /log/jetlog_*')
        jetlog_messages = outmsg.split('\n')
        logger.info("开始下载jetlog_*到本地")
        for jetfile in jetlog_messages:
            result = re.findall(r"/log/jetlog_[a-zA-Z0-9_-]+.zst$", jetfile)
            for file in result:
                file_time = int(file.split("_")[2][0:12])
                if int(file_time) in range(mintime, maxtime):
                    file_download(device_name=self.BGM, local_path=save_path, remote_path=file)
        logger.info("jetlog_*全部下载到本地，开始打包")
        now_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))
        result = os.system(f"tar -cvzf {save_path}/bgm_jetlogs_{now_time}.tar.gz  {save_path}/jetlog_*")
        if not result:
            logger.info(f"jetlog_*打包成功 生成bgm_jetlog_{now_time}.tar.gz ，删除jelog_*")
            os.system(f"rm -rf ./{save_path}/jetlog_*")

    def check_bgm_start_type(self, nucapp):
        i = 3
        while i > 0:
            data = self.type_commands("cat /sys/power/sys_resumed")
            if data == "1":
                logger.info("BGM是镜像启动的")
                break
            else:
                logger.info("BGM是非镜像启动的")
                self.type_commands("/app/bin/swdl -nw 10 0")
                nucapp.bgm_power_off()
                sleep(1)
                nucapp.bgm_power_on()
                sleep(10)
                logger.info("恢复BGM镜像启动")
                i -= 1
        else:
            logger.error("BGM切换镜像启动失败，请手动检测")


def getkey(str1):
    key1 = ''
    for item in str1:
        if len(item) == 2:
            key1 = key1 + item
        if len(item) == 1:
            key1 = key1 + "0"
            key1 = key1 + item
    return key1


if __name__ == '__main__':
    # print(BGM_SSH().get_tprop()[2])
    # print(time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(time.time())))
    print(BGM_SSH().get_set_salt())
