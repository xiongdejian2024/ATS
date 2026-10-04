'''
Author: liu.yang
Date: 2022-11-29 05:25:45
LastEditTime: 2023-05-10 17:17:45
FilePath: /yangliu/sat/xat_ecu/legacy/interface/tcam/tcam_ssh.py
Description: A utility class for ssh into tcam
'''
import os
import sys
import base64
import json
from pathlib import Path

current_path = os.path.dirname(os.path.realpath(__file__))
from xat_ecu.legacy.common.singleton import SingletonMeta
from xat_ecu.legacy.driver.ssh_interface import command_send, file_download, file_upload
from xat_ecu.legacy.driver.ssh_client import *
from xat_ecu.legacy.interface.nuc_app import *
from xat_ecu.legacy.common.file_handle import parent_dir
from xat_ecu.legacy.common import exception_error
import re
import datetime

soa_partner_path = Path(parent_dir) / "soa_partner"


class TCAM_SSH:
    def __init__(self, connect_type='vlan'):
        self.TCAM = 'TCAM'
        self.connect_type = connect_type

    def type_commands(self, commands, output=False, root_permission=True, timeout=60, **kwargs):
        ct = kwargs.get('connect_type')
        if ct is not None:
            connect_type = ct
            kwargs.pop('connect_type')
        else:
            connect_type = self.connect_type
        status, outmsg = command_send(device_name=self.TCAM, cmd=commands, timeout=timeout, connect_type=connect_type, **kwargs)
        logger.info(f"输入{commands}后返回的结果为:\n{outmsg}")
        return outmsg

    # 得到TCAM的版本信息
    def get_version(self):
        return self.type_commands(commands="cat /oemapp/etc/versions.txt")

    def get_build_date_utc(self):
        cmd = "cat /oemapp/etc/build.prop | grep sys.build.date.utc| awk -F'=' '{print $2}'"
        data = self.type_commands(cmd)
        return data

    # 清除TCAM的所有log
    def clear_log(self):
        self.type_commands(commands="cd /mnt/sdcard/;rm -rf /mnt/sdcard/log/*")

    def clear_coredump(self, hours):
        self.type_commands(commands=f'find /mnt/sdcard/coredump/ -name "*.core" -mmin +{hours * 60} -delete')
        logger.info(f"清除{hours}小时前的coredump文件")

    def get_log(self, my_local='.', needed_log="/mnt/sdcard/log", timeout=600, connect_type="vlan"):
        self.type_commands(
            commands=f"cd /mnt/sdcard/;"
                     f"rm -f /mnt/sdcard/log/tcam_soa.tar.gz;rm -f /mnt/sdcard/log/tcam_log.gz;sync;"
                     f"tar -cvf /mnt/sdcard/log/tcam_log.gz {needed_log}",
            timeout=timeout,
            connect_type=connect_type
        )
        log_time = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime(time.time()))
        file_download(device_name=self.TCAM,
                      remote_path='/mnt/sdcard/log/tcam_log.gz',
                      local_path=f'{my_local}/tcam_log_{log_time}.gz',
                      connect_type=connect_type)

    def exec(self, cmd, bgm_ip=None):
        """
        通过BGM连接TCAM
        cmd: 执行的命令
        bgm_ip:
        为空时获取默认的bgm_ip
        不为空时可以设置为继承TestBase时传的obd_ip,也可以自己输入正确的bgm_ip
        """
        ret = self.type_commands(commands=cmd)
        return ret.replace('\r\n', '\n')

    def get_ICCID(self, timeout=2):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                ret = self.type_commands(commands='cat /dev/smd8 & echo -en "AT+ICCID\\r\\n" > /dev/smd8', expect='OK',
                                         timeout=1)
                if ret is not None:
                    ICCID = re.findall(r'ICCID: (\d+)', ret)
                    if ICCID:
                        return ICCID[0]
                raise exception_error.CmdExecuteError(f'未获取到ICCID, 返回值为{ret}')
            except exception_error.CmdExecuteError:
                time.sleep(0.5)

    def get_surface(self, cmd=None):
        '''
        获取 tcam 的切面
        @return:
        '''
        if cmd is None:
            cmd = "updatetool -g |grep lastboot"
        ret_hex = self.type_commands(cmd)
        logger.info(f"获取的 tcam 的当前切面为 {ret_hex}面")
        # . 匹配任意字符，除了换行符
        # + 匹配1个或多个的表达式
        # ? 匹配0个或1个由前面的正则表达式定义的片段，非贪婪方式
        # 查找丢失的 数据包
        regular = re.findall(f"lastboot          = (.+?)", ret_hex)
        if regular:
            value = regular[0].strip()
            return value
        return ""

    def get_date_time_and_check(self, cmd=None, error_scop=20, time_diff=8):
        '''

        @param cmd:
        @param error_scop: 误差范围 单位为秒
        @param time_diff: 时差 相差 8 个小时
        @return:
        '''

        if cmd is None:
            cmd = "date"
        res = self.type_commands(cmd)
        logger.info(f"获取的 tcam 的当前时间为 {res}")
        temp = """\r\n~ # date;cd /mnt/sdcard/\r\n(.+)\r\n/mnt/sdcard #"""
        regular = re.findall(temp, res)
        if regular:
            value = regular[0].strip()
        else:
            value = ""
        logger.info(f"获取的tcam 的时间 {value}")
        result, time_str = self.get_time(
            value, error_scop=error_scop, time_diff=time_diff
        )
        return result, time_str

    def get_time(self, data_str, error_scop=20, time_diff=8):
        '''
        @param data_str:  'Fri Mar  3 04:54:11 UTC 2023'
        @param error_scop:  误差范围 单位为秒
        @param time_diff:  时差 相差 8 个小时
        @return:
        '''
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
        logger.info(f'tcam 系统时间为{local_time} {week}')
        data_sj = time.strptime(
            local_time.strftime(UTC_FORMAT), "%Y-%m-%d %H:%M:%S"
        )  # 定义格式
        time_int = int(time.mktime(data_sj))
        current_time = time.time()
        print(time_int, current_time)
        logger.info(f'tcam 系统时间为{string} 对应的时间戳为{time_int},当前时间戳为{current_time}')
        temp = current_time - time_int
        if temp > error_scop:
            logger.info(f'tcam 系统时间和当前时间相差{temp}秒，')
            return False, string
        return True, string

    def get_ping(self, ip=None, num=4):
        '''
        看 tcam 是否 ping 通 该 ip
        @param ip: 需要ping的 ip
        @param num: 尝试几次
        @return:
        '''
        if ip is None:
            ip = "www.baidu.com"
        cmd = f'ping {ip} -c {num}'
        String = self.type_commands(cmd)
        logger.info(f"获取的 tcam 的{cmd}的结果为 {String}")
        # . 匹配任意字符，除了换行符
        # + 匹配1个或多个的表达式
        # ? 匹配0个或1个由前面的正则表达式定义的片段，非贪婪方式
        # 查找丢失的 数据包
        regular = re.findall(f"received,(.+?)packet loss, time", String)
        if regular:
            value = regular[0].strip()
            logger.info(f"tcam  ping {ip} {num}次，丢包率为 {value}")
            if value == "100%":
                # 未ping 通
                return False
            else:
                return True
        return False

    def retry_ping_mul_times(self, ip=None, num=4, retry=2):
        '''
        若失败则重试 ping 几次
        @param ip: 每次 ping 的 对象
        @param num: 每次 ping 4
        @param retry: 若失败 则 再次尝试2轮，每轮ping 4次
        @return:
        '''

        res = self.get_ping(ip=ip, num=num)
        while retry and not res:
            logger.info(f"第{retry}次尝试ping {str(ip)}")
            res = self.get_ping(ip=ip, num=num)
            retry -= 1
        return res

    def get_ping_baidu(self, num=4, retry=2):
        '''
        ping 百度
        @param num: 每次 ping 4
        @param retry: 若失败 则 再次尝试2轮，每轮ping 4次
        @return:
        '''
        return self.retry_ping_mul_times(ip="www.baidu.com", num=num, retry=retry)

    def get_ping_8888(self, num=4, retry=2):
        '''
        ping 8.8.8.8
        @param num: 每次 ping 4
        @param retry: 若失败 则 再次尝试2轮，每轮ping 4次
        @return:
        '''
        return self.retry_ping_mul_times(ip="8.8.8.8", num=num, retry=retry)

    def get_L7(self):
        file_upload(device_name=self.TCAM,local_path=parent_dir + '/interface/tcam/tcam_seco_api_test',remote_path='/oemdata/')
        file_upload(device_name=self.TCAM,local_path=parent_dir + '/interface/tcam/run_tcam_seco_api_test.sh',remote_path='/oemdata/')
        outmsg = self.type_commands(commands="cd /oemdata/;chmod +x run_tcam_seco_api_test.sh; chmod +x tcam_seco_api_test;./run_tcam_seco_api_test.sh")
        outmsg_list = outmsg.split('\n')
        for i in outmsg_list:
            if 'L7 key' in i:
                L7_index = outmsg_list.index(i)
                # logger.info('L7_index={} index_type={}'.format(L7_index,type(L7_index)))
                break
        L7_index = L7_index + 1
        L7_key = outmsg_list[L7_index].replace(' ','')
        return L7_key

    def get_ts_security(self):
        cmd = "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/oemapp/lib/bootes;\
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/lib;\
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/oemapp/lib;\
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/oemapp/lib/soa;\
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/oemapp/lib/proxy;\
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/oemapp/service/em;\
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/oemapp/service/prop;\
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/umdp/lib/"
        self.type_commands(commands=cmd)
        cmd = "/oemapp/bin/ts_security -m test1 -d 0123456 | head -7 | tail -1"
        out = self.type_commands(commands=cmd)
        return out

    def get_bootes_version(self):
        result = self.get_soa_jidl_name()
        return result.get("bootes_version")

    def get_prop(self):
        result = self.get_soa_jidl_name()['build_version']
        result.strip(' ') or result.rstrip(' ')
        file_upload(device_name=self.TCAM,
                    local_path=parent_dir + '/interface/tcam/soa_api_test',
                    remote_path='/mnt/sdcard/')
        self.type_commands(
            "cd /mnt/sdcard/;chmod +x soa_api_test;export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/oemapp/lib;export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/umdp/lib/;./soa_api_test")
        json_data = self.type_commands("cat /mnt/sdcard/tcam_seco_api_result.json")

        logger.info("从域控TCAM获取到的用于信息加密的密钥：" + json_data)
        dict_salt = json.loads(json_data + "}")
        return dict_salt.get('aes_key', None), dict_salt.get('aes_iv', None), dict_salt.get('cmac_key', None)

    def get_set_salt(self):
        aes_str, iv_str, cmac_str = self.get_prop()
        result = {"aes_key": aes_str, "aes_iv": iv_str, "cmac_key": cmac_str}
        logger.info(f"生成的上位机秘钥：{result}")

        if (
                isinstance(aes_str, str)
                and isinstance(iv_str, str)
                and isinstance(cmac_str, str)
        ):
            if len(aes_str) >= 32 and len(iv_str) >= 32 and len(cmac_str) >= 32:
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

    def get_soa_jidl_name(self):
        cmd = 'cat /oemapp/etc/build.prop'
        data = self.type_commands(cmd)

        release = ''
        soa_version = ''
        jidl_version = ''
        bootes_version = ''
        for i in data.split('\n'):
            i = i.strip()
            if 'sys.build.soa.version' in i:
                soa_version = i.split('=')[-1]
            if 'sys.build.jidl.version' in i:
                jidl_version = i.split('/')[-1]
            if 'sys.build.version.swpn' in i:
                release = i.split('=')[-1]
            if 'sys.build.version.ver' in i:
                if len(i.split('=')[-1]) == 2:
                    release = release + ' ' + i.split('=')[-1]
                elif len(i.split('=')[-1]) == 3:
                    release = release + i.split('=')[-1]
                else:
                    exit('版本信息命名错误')
            if "sys.build.bootes.version" in i:
                bootes_version = i.split(' ')[0].split('=')[-1]
            if "sys.build.carina.version" in i:
                bootes_version = i.split(' ')[0].split('=')[-1]

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
        }
        return result


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
    TCAM_SSH().clear_log()
    TCAM_SSH().get_log()
