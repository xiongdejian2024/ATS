# -*- coding: utf-8 -*-
"""
@File        : sdk_tools
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/4/11 13:33
@Description :

"""
import os
import re
import subprocess
import time
from hashlib import md5, sha1, sha256
from xat_ecu.legacy.common.logger import *
from xat_ecu.legacy.common.file_handle import *
from scapy.sendrecv import sniff
from scapy.utils import wrpcap,rdpcap
import threading


def exec_shell(command):
    '''
    输入指令，获取返回结果
    @param command:
    @return:
    '''
    try:
        # 执行命令
        logger.info(f"开始执行cmd={command}")
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 等待命令执行完成
        process.wait()
        # 获取命令的输出和错误信息
        output = process.stdout.read()
        error = process.stderr.read()
        # 将输出和错误信息解码为字符串
        output = output.decode(encoding="utf-8")
        error = error.decode(encoding="utf-8")
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/sdk_tools.py")
        output = ""
        error = str(e)
    logger.info(f"执行cmd={command} 结束")
    # 返回命令的输出和错误信息
    result = {"output": output, "error": error}
    logger.debug(result)
    return result


def get_willow_file_path(**kwargs):
    '''
    获取 最近的 willow 文件
    @return:
    '''
    if not ("willow" in current_path.lower() or "testdev" in current_path.lower()):
        return None
    save_num = kwargs.get("save_num", 20)
    # 存放 willow_log 的路径
    willow_log_path = kwargs.get("willow_log_path", "/root/autotest/willow/")
    willow_log_filename_len = kwargs.get("willow_log_filename_len", 36)
    # 查找文件
    cmd = f"cd {willow_log_path};ls -lrt"
    result = exec_shell(cmd)
    data = result["output"]
    error = result["error"]
    try:
        if data:
            output_lis = data.split("\n")
            name_list = [na.split(' ')[-1] for na in output_lis[1:]]
            name_list = [i for i in name_list if i.strip()]
            name_list.reverse()
            logger.info(f"len={len(name_list)} name_list={name_list}")
            # 需要保留的 日志
            save_log_list = []
            for namestr in name_list:
                if namestr.endswith('zip'):
                    continue
                if len(save_log_list) >= save_num:
                    break
                save_log_list.append(namestr)
            logger.info(f"删除多余文件保留最近修改的{save_num}个文件==》{save_log_list}")
            # 删除 文件
            for del_name in name_list:
                if del_name in save_log_list:
                    continue
                path = os.path.join(willow_log_path, del_name)
                logger.info(f"删除的文件为 path={path}")
                cmd = f"rm -rf {path}"
                exec_shell(cmd)
            # 返回最新文件
            willow_file_lis = [namestr for namestr in name_list if len(namestr) == willow_log_filename_len]
            path = os.path.join(willow_log_path, willow_file_lis[0])
            logger.info(f"获取到最新的文件夹path为{path}")
            return path
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/sdk_tools.py")
        logger.error(f"未找到最新 willow 文件 {str(e)}")
    logger.error(f"未找到最新 willow 文件{error}")
    return None


def get_md5(strFilePath):
    '''
    获取当前文件 md5 值
    :param strFilePath:
    :return:
    '''
    mdfive = md5()
    try:
        with open(strFilePath, 'rb') as f:
            mdfive.update(f.read())
        hashMD5 = mdfive.hexdigest().upper()
        return hashMD5
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/sdk_tools.py")
        logger.error(f"获取 {strFilePath}的 md5 失败{str(e)}")
        return None


def get_sha1(strFilePath):
    '''
    获取当前文件 sha1 值
    :param strFilePath:
    :return:
    '''
    sha1Obj = sha1()
    try:
        with open(strFilePath, 'rb') as f:
            sha1Obj.update(f.read())
        hashSHA1 = sha1Obj.hexdigest()
        return hashSHA1
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/sdk_tools.py")
        logger.error(f"获取 {strFilePath}的 sha1 失败{str(e)}")
        return None


def get_sha256(strFilePath):  # 计算sha256
    '''
     获取当前文件 sha256 值
    :param strFilePath:
    :return:
    '''
    sha256Obj = sha256()  # Get the hash algorithm.
    try:
        with open(strFilePath, 'rb') as f:
            sha256Obj.update(f.read())  # Hash the data.
        hashSHA256 = sha256Obj.hexdigest()  # Get he hash value.
        return hashSHA256
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/sdk_tools.py")
        logger.error(f"获取 {strFilePath}的sha256失败{str(e)}")
        return None


class SniffPacket(object):

    def __init__(self, **kwargs):
        # 停止抓包标志位
        self.sniff_flag = False
        # 所抓网口 名字
        self.iface = kwargs.get("iface", None)
        # 是否保存
        self.save_enable = kwargs.get("save_enable", True)
        # 保存路径
        self.save_path = kwargs.get("save_path", '/root/obd_doip_dump')
        # 保存名字
        self.save_name = kwargs.get("save_name", 'obd_doip_')
        # 回调函数
        self.callback = None
        # self.file_path 全路径
        self.file_path = kwargs.get("file_path", '')

    def set_iface(self, iface):
        '''
        设置抓包网口 设置网口的名字，或者ip 优选网卡名字
        @param iface:
        @return:
        '''
        self.iface = iface

    def set_save_path(self, save_path):
        '''
        设置保存 路径
        @param save_path:
        @return:
        '''
        self.save_path = save_path

    def set_save_name(self, save_name):
        '''
        设置保存 名字
        @param save_name:
        @return:
        '''
        self.save_name = save_name

    def start_sniff(self, **kwargs):
        '''
        开启抓包线程
        @param kwargs:
        @return:
        '''
        if self.sniff_flag:
            self.sniff_flag = False

        t = threading.Thread(target=self.__sniff_func)
        t.setDaemon(True)
        t.start()

    def get_network_card_name_by_ip(self, ip_str="169.254.1.200", **kwargs):
        '''
        根据ip 获取 网卡名字
        @param ip_str:
        @return:
        '''
        import subprocess
        import socket
        import fcntl
        import struct

        phy_cmd = 'ls /sys/class/net/ | grep -v "`ls /sys/devices/virtual/net/`"'
        try:
            ret = subprocess.getoutput(phy_cmd)
            list_phy = ret.split('\n')
            logger.info(f"获取的网卡的名字》》》{str(list_phy)}")
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/sdk_tools.py")
            list_phy = []
            logger.info(f"获取网卡失败》》》{str(e)}")
            pass

        for ifname in list_phy:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', bytes(ifname[:15], 'utf-8')))
                ip = socket.inet_ntoa(inet[20:24])

                logger.info(f"获取到该网卡{ifname}的ip为{ip}")
                if ip == ip_str:
                    return ifname
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/sdk_tools.py")
                logger.warning(f"未获取到该网卡{ifname}的ip")
        logger.error(f"未获取到该网卡{list_phy}的ip,影响doip 报文抓包，不影响测试功能")
        return None

    def __sniff_func(self):
        '''
            count:抓取报的数量，设置为0时则一直捕获
            store:保存抓取的数据包或者丢弃，1保存，0丢弃
            offline:从pcap文件中读取数据包，而不进行嗅探，默认为None
            prn:为每个数据包定义一个回调函数，通常使用lambda表达式来写回调函数
            filter:过滤规则，可以在里面定义winreshark里面的过滤语法，使用 Berkeley Packet Filter (BPF)语法，
            L2socket:使用给定的L2socket
            timeout:在给定的事件后停止嗅探，默认为None
            opened_socket:对指定的对象使用.recv进行读取
            stop_filter:定义一个函数，决定在抓到指定的数据之后停止
            iface:指定抓包的网卡,不指定则代表所有网卡
        @return:
        '''
        # 判断 是不是ip  如果是ip 则获取ip 对应的 网卡名字
        p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        if p.match(self.iface):
            self.iface = self.get_network_card_name_by_ip(self.iface)

        logger.info(f"开始抓取{self.iface}网口的以太报文！")
        recv_packet = sniff(count=0,
                            store=1,
                            offline=None,
                            prn=None,
                            filter=None,
                            L2socket=None,
                            timeout=None,
                            opened_socket=None,
                            stop_filter=self.stop_filter,
                            iface=self.iface)

        # 保存 文件
        if self.save_enable:
            otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))
            try:
                save_name = f"{self.save_name}{otherStyleTime}.pcap"
                if not os.path.exists(self.save_path):
                    os.makedirs(self.save_path)
                if not self.file_path:
                    self.file_path = os.path.join(self.save_path, save_name)
                logger.info(f"保存obd口抓包文件路径为===>>>{self.file_path}")
                wrpcap(self.file_path, recv_packet)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/sdk_tools.py")
                wrpcap(f"doip_{otherStyleTime}.pcap", recv_packet)
                logger.error(f"{str(e)}")

    def stop_filter(self, packet):
        '''
        过滤数据
        @param packet:
        @return:
        '''
        if self.callback:
            self.callback(packet)
        return self.sniff_flag

    def stop_sniff(self):
        '''
        停止抓包
        @return:
        '''
        self.sniff_flag = True

    def set_callback(self, fun):
        '''
        设置回调函数
        @param fun:
        @return:
        '''
        self.callback = fun


def get_signal_value(data_lis, start_bit, bit_len, layout_format="Motorola MSB", **kwargs):
    '''
    根据信号 长度 起始位 获取的信号的值
    :param data_lis: 数据列表
    :param start_bit: 信号起始位
    :param bit_len: 信号长度
    :param layout_format: 格式
    :param kwargs:  十进制数
    :return:
    '''
    layout_format = layout_format.lower().replace(" ", '').strip()

    if isinstance(data_lis, str):
        data_lis = [int(data_lis[i:i + 2], 16) for i in range(0, len(data_lis), 2)]

    if layout_format == "motorolamsb":
        # 转化为 10进制
        data_lis = [bin(i)[2:].zfill(8) for i in data_lis]
        div = start_bit // 8
        # 开始字节
        start_byte = data_lis[div]
        # 当前字节 可取最大长度
        current_byte_max_len = start_bit - div * 8 + 1

        if bit_len <= current_byte_max_len:
            star_pos = -current_byte_max_len
            end_pos = -(current_byte_max_len - bit_len)
            if end_pos:
                data = start_byte[star_pos:end_pos]
            else:
                data = start_byte[star_pos:]
        else:
            star_pos = -current_byte_max_len
            data = start_byte[star_pos:]
            left_bit = bit_len - current_byte_max_len
            num, left = divmod(left_bit, 8)
            for i in range(div + 1, div + num + 1):
                data += data_lis[i]
            if left:
                last_byte = data_lis[div + num + 1][-8:-(8 - left)]
                data += last_byte
        logger.info(f"data》》》{data}")
        return int(data,2)

    elif layout_format == "motorolalsb":

        pass
    elif layout_format == "opaque":
        pass
    else:
        pass



def check_pdu(data_list, file_path, **kwargs):
    '''
    校验 pdu的 指定bit 位的值，是否在改包出现

    :param data_list: [(pdu_id，length,start_bit,length_bit,value),(pdu_id，length,start_bit,length_bit,value)]
    :param file_path:
    :param kwargs:  True/False , {(5953, 1, 1, 2, 3): True}
    :return:
    '''
    src_ip = kwargs.get("src_ip", "172.16.5.1")
    des_ip = kwargs.get("des_ip", "172.16.5.2")
    #
    proto = kwargs.get("proto", None)
    # 处理下 tcp 或者udp
    if proto is None:
        proto_str = None
    elif proto.lower() == "udp":
        proto_str = "11"
    else:
        proto_str = "06"
    # 处理ip
    ip_str = bytes([int(i) for i in src_ip.split('.')]).hex() + bytes([int(i) for i in des_ip.split('.')]).hex()
    # 处理返回值
    res_dict = dict(zip(data_list, [False] * len(data_list)))
    read_data = rdpcap(file_path)
    for i in range(len(read_data)):
        line = bytes(read_data[i]).hex()
        if ip_str in line:
            # ip 方向对，再判断那种报文
            if proto_str and line[46:48] != proto_str:
                continue
            # 解析 数据
            for data in data_list:
                if res_dict[data]:
                    continue
                pdu_id = data[0]
                length = data[1]
                start_bit = data[2]
                length_bit = data[3]
                except_value = data[4]
                if isinstance(pdu_id, int):
                    pdu_id_str = hex(pdu_id)[2:].zfill(8)
                else:
                    pdu_id_str = pdu_id.zfill(8)
                if isinstance(length, int):
                    length_str = hex(length)[2:].zfill(8)
                else:
                    length_str = length.zfill(8)

                string = pdu_id_str + length_str
                # print("line", line)
                if string in line:
                    data_info = line.split(string)[1][:length * 2]
                    new_data = get_signal_value(data_info, start_bit, length_bit)
                    if new_data == except_value:
                        res_dict[data] = True
        else:
            continue
    logger.info(f"res_dict》》》{res_dict}")
    return all(list(res_dict.values())), res_dict


def get_pdu_value_and_time(data_list, file_path, **kwargs):
    '''
    获取 pdu的 指定bit 位的值，以及该条报文的时间，和对应pcap 包 对应行数
    :param data_list: [(pdu_id，length,start_bit,length_bit),(pdu_id，length,start_bit,length_bit)]
    :param file_path: pcap 包的路径
    :param kwargs:
    :return:{(5953, 1, 1, 2): [(14942, '2023-08-23 15:39:33', 3), (15042, '2023-08-23 15:39:33', 3)]}
    '''
    src_ip = kwargs.get("src_ip", "172.16.5.1")
    des_ip = kwargs.get("des_ip", "172.16.5.2")
    #
    proto = kwargs.get("proto", None)
    # 处理下 tcp 或者udp
    if proto is None:
        proto_str = None
    elif proto.lower() == "udp":
        proto_str = "11"
    else:
        proto_str = "06"
    # 处理ip
    ip_str = bytes([int(i) for i in src_ip.split('.')]).hex() + bytes([int(i) for i in des_ip.split('.')]).hex()
    # 处理返回值
    res_dict = {}

    read_data = rdpcap(file_path)
    for index in range(len(read_data)):
        line_data = read_data[index]
        data_time = float(line_data.time)
        line = bytes(line_data).hex()
        if ip_str in line:
            # ip 方向对，再判断那种报文
            if proto_str and line[46:48] != proto_str:
                continue
            # 解析 数据
            for data in data_list:
                pdu_id = data[0]
                length = data[1]
                start_bit = data[2]
                length_bit = data[3]
                if isinstance(pdu_id, int):
                    pdu_id_str = hex(pdu_id)[2:].zfill(8)
                else:
                    pdu_id_str = pdu_id.zfill(8)
                if isinstance(length, int):
                    length_str = hex(length)[2:].zfill(8)
                else:
                    length_str = length.zfill(8)
                string = pdu_id_str + length_str
                # print("line", line)
                if string in line:
                    data_info = line.split(string)[1][:length * 2]
                    new_data = get_signal_value(data_info, start_bit, length_bit)
                    if data in res_dict:
                        res_dict[data].append((index, new_data, data_time))
                    else:
                        res_dict[data] = [(index, new_data, data_time)]

        else:
            continue
    logger.info(f"res_dict》》》{res_dict}")
    return res_dict
