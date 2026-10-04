import os
import time

from scapy.all import *
from socket import *
import subprocess
from xat_ecu.legacy.common.logger import logger

# 直接命令行抓包或者实时获取包
class SniffPacket_process: 
    """进程抓包"""
    def __init__(self, **kwargs):
        # 所抓网口 名字
        self.iface = kwargs.get("iface", None)
        # 保存路径
        self.save_path = kwargs.get("save_path", '/root/mock_mpu_cdd_dump')
        # 保存名字
        self.save_name = kwargs.get("save_name", 'mcu_to_cdd_dump')
        self.pcap_file_name = None
        self.start_file_name = None
        self.file_path = None
        self.t_start = None
    
    def set_iface(self,iface):
        self.iface = iface

    def set_save_path(self, save_path):
        self.save_path = save_path

    def set_save_name(self, save_name):
        self.save_name = save_name
        
    def sniff_start_process(self):
        """启动抓包进程并保存数据包到文件"""
        self.t_start = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))
        self.file_path = os.path.join(self.save_path, self.save_name)
        self.start_file_name = os.path.join(self.file_path, self.t_start + '.pcap')
        logger.info(f"抓pacp包的名称：{self.start_file_name}")
        self.pcap_file_name = self.start_file_name

        # 确保保存路径存在
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)

        # 设置抓包命令，这里可以根据需要调整抓包大小和其他参数
        tcpdump_command = f'tcpdump -i {self.iface} -w {self.start_file_name} -s 0'  # -s 0 表示捕获数据包完整内容

        try:
            # 启动tcpdump进程
            self.tcpdump_process = subprocess.Popen(tcpdump_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info(f"抓包开始，等待一段时间以确保抓包进程已启动...")
            time.sleep(2)  # 等待一段时间，确保tcpdump已经启动并开始抓包
        except subprocess.CalledProcessError as e:
            logger.error(f"启动tcpdump进程失败: {e}")
        except Exception as e:
            logger.exception(f"发生未预期的错误: {e}")

    def stop_sniff_process(self):
        """停止抓包进程"""
        if hasattr(self, 'tcpdump_process') and self.tcpdump_process.poll() is None:
            try:
                self.tcpdump_process.terminate()  # 终止tcpdump进程
                # t_stop = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))
                # 等待tcpdump进程终止
                try:
                    # 等待一段时间（可选）
                    self.tcpdump_process.wait(timeout=5)  # 等待5秒
                except subprocess.TimeoutExpired:
                    logger.info("tcpdump 没有在5秒内响应 SIGTERM，现在发送 SIGKILL")
                    self.tcpdump_process.kill()
                # stop_file_name = os.path.join(self.file_path, self.t_start + '_' + t_stop + '.pcap')
                # self.__rename_file(self.start_file_name, stop_file_name)
                # self.pcap_file_name = stop_file_name
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/Internal_ETH/tools/mock_mpu_cdd.py")
                logger.error(f"停止tcpdump进程失败: {e}")
            finally:
                time.sleep(2)
                # 确保抓包进程已停止
                subprocess.Popen("ps -ef | grep tcpdump| awk '{print $2}' | xargs kill -9",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                logger.info("停止抓包进程成功")
        else:
            logger.warning("tcpdump进程已不存在或已停止")
        
    def __rename_file(self, old_name, new_name):
        try:
            os.rename(old_name, new_name)
            logger.info(f"文件 {old_name} 重命名为 {new_name} 成功")
        except OSError as e:
            logger.error(f"文件 {old_name} 重命名为 {new_name} 失败: {e.strerror}")
    

# 数据包进行解析
class PcapParseUdpInfo():
    """解析pcap文件，将上下行udp payload解析出来"""
    def __init__(self, udp_up_mcu_ip="172.16.5.2", udp_up_mcu_port=30502, udp_down_mpu_ip="172.16.5.1", udp_down_mpu_port=30502):
        self.frame_obj_dict = {}
        self.udp_up_mcu_ip = udp_up_mcu_ip
        self.udp_up_mcu_port = udp_up_mcu_port
        self.udp_down_mpu_ip = udp_down_mpu_ip
        self.udp_down_mpu_port = udp_down_mpu_port
        self.up_payload = {}
        self.tcp_packet_list = []
        self.data_error_packet_dict = []
        self.time_error_packet_dict = []
        self.index = 1
    def parse_pcap_file(self, pcap_file, timeout=0.01):
        """
        解析pcap文件，将上下行UDP payload解析出来
        
        Args:
            pcap_file (str): pcap文件路径
            timeout (float, optional): 时间阈值，用于检测超时包。默认为0.01秒。
        
        Returns:
            None: 该函数没有返回值，而是将解析的数据保存在实例的属性中，包括
                - self.up_payload: 字典，保存上行UDP payload的hex字符串
                - self.tcp_packet_list: 列表，保存UdpPacket对象，表示解析出的UDP数据包信息
                - self.time_error_packet_dict: 列表，保存超时的UdpPacket对象
        
        """
        pkt = rdpcap(pcap_file)
        i = 0
        t1 = 0
        for data in pkt:
            if 'UDP' in data:
                if "Raw" not in data:
                    continue
                hex_string = ''.join(hex(b)[2:].zfill(2) for b in data["Raw"].load)
                if (data["IP"].src == self.udp_up_mcu_ip and data["UDP"].sport == self.udp_up_mcu_port):
                # if (data["IP"].src == self.udp_up_mcu_ip and data["UDP"].sport == self.udp_up_mcu_port and
                #         data["IP"].dst == self.udp_down_mpu_ip and data["UDP"].dport == self.udp_down_mpu_port):
                    # 上行tcp数据包
                    i = i + 1
                    curr_tcp_info = UdpPacket(i, data.time, data["IP"].src, data["IP"].dst, data["UDP"].sport,
                                            data["UDP"].dport, hex_string, len(self.up_payload), int(len(hex_string)) // 2,
                                            False)
                    t2 = data.time
                    if t1 != 0 and t2 - t1 > timeout:
                        self.time_error_packet_dict.append(curr_tcp_info)
                    self.up_payload[i] = hex_string
                    self.tcp_packet_list.append(curr_tcp_info)
                    t1 = t2       

    def parse_signal_info(self):
        """
        解析pcap解出来的上下行payload中指定的数据帧。
        
        Args:
            frames (str): pcap解出来的上下行payload。
        
        Returns:
            Tuple[List[FrameObj], int]: 返回一个元组，第一个元素为FrameObj类型的列表，包含解析出来的数据帧；
                                            第二个元素为解析出来的数据帧数量。
        
        """
        for i in self.tcp_packet_list[:-1]:
            frames = i.payload
            frames_bytes_len = len(frames) // 2
            if not frames:
                continue  # 如果payload或frames为空，返回空列表
            if frames_bytes_len > 1400:
                self.data_error_packet_dict.append(i)
                logger.warning(f"------------------数据包序号为：{i} 长度异常---------------------")
                # print(f"数据包长度异常大于1400，解析结束，共解析出{len(self.frame_obj_dict)}个数据帧")
                continue
            if frames[-2:] != 'fe':
                self.data_error_packet_dict.append(i)
                logger.warning(f"------------------数据包序号为：{i} 内容尾部异常---------------------")
                # print(f"数据包尾部异常，解析结束，共解析出{len(self.frame_obj_dict)}个数据帧")
                continue
            start = 12
            end = 14
            g_timestamp = self.__hex_to_decimal_timestamp(frames[:start])
            while end < len(frames):
                f = FrameObj()
                f.g_timestamp = g_timestamp
                f.channel = int(frames[start:end], 16)
                start = end    
                if f.channel == 254:
                    logger.info("------------------数据解析完毕---------------------")
                elif f.channel == 1:
                    id_length = 4
                elif 2 <= f.channel <= 12:
                    id_length = 2
                elif 41 <= f.channel <= 47:
                    id_length = 1
                else:
                    self.data_error_packet_dict.append(i)
                    logger.warning(f"------------------数据包序号为：{i} f.channel={f.channel}异常---------------------")
                    break  # 跳过当前数据包，继续解析下一个

                f.channel = self.__get_channel(f.channel)
                end = start + id_length * 2
                if end > len(frames):
                    break  # 防止索引越界
                
                f.message_id = f"0x{frames[start:end]}"
                start = end
                
                end = start + 2 * 2
                if end > len(frames):
                    break  # 防止索引越界
                
                f.timestamp = f.g_timestamp * 10 ** 4 + int(frames[start:end], 16)
                start = end
                
                end = start + 2
                if end > len(frames):
                    break  # 防止索引越界
                
                f.message_length = int(frames[start:end], 16)
                start = end
                
                end = start + f.message_length * 2
                if end > len(frames):
                    self.data_error_packet_dict.append(i)
                    logger.warning(f"------------------数据包序号为：{i} 数据包长度不足，数据解析异常---------------------")
                    break  # 数据长度不够，终止解析

                f.message_data = frames[start:end]
                f.index = self.index
                self.frame_obj_dict[self.index] = f
                self.index += 1
                start = end
                end = end + 2   
        return len(self.frame_obj_dict)
    def __hex_to_decimal_timestamp(self, hex_timestamp):
        # 确保输入是16进制字符串，并且长度为12（6个字节，每个字节2位16进制数）
        if len(hex_timestamp) != 12:
            raise ValueError("Invalid hex timestamp length, must be 12 characters")

        # 转换为16进制字节数组
        bytes_timestamp = bytes.fromhex(hex_timestamp)

        # 提取并转换为十进制
        year = bytes_timestamp[0]  # 年份后两位
        month = bytes_timestamp[1]  # 月份
        day = bytes_timestamp[2]  # 日期
        hour = bytes_timestamp[3]  # 小时
        minute = bytes_timestamp[4]  # 分钟
        second = bytes_timestamp[5]  # 秒
        timestamp = year * 10 ** 10 + month * 10 ** 8 + day * 10 ** 6 + hour * 10 ** 4 + minute * 10 ** 2 + second

        # 返回结果
        return timestamp
    def __get_channel(self, target_value):
        channel_dict = {
            "bodycan": 9,
            "propulsioncan": 4,
            "chassiscan1": 5,
            "chassiscan2": 6,
            "passivesafetycan": 7,
            "diagnosticcan": None,
            "infocanfd": 2,
            "bodyexposedcanfd": 10,
            "adcanfd": 3,
            "connectivitycanfd": 8,
            "bodyalmcanfd1": 11,
            "bodyalmcanfd2": 12,
            "cem_lin1": 41,
            "cem_lin2": 42,
            "cem_lin3": 43,
            "cem_lin4": 44,
            "cem_lin5": 45,
            "cem_lin6": 46,
            "backbonefr": 1
            }
        for key, value in channel_dict.items():
            if value == target_value:
                return key


class FrameObj:
    """解析数据帧的属性信息"""
    def __init__(self):
        self.index = 0
        self.channel = 0
        self.message_id = ""
        self.message_length = ""
        self.timestamp = 0
        self.g_timestamp = 0
        self.message_data = 0

    def __repr__(self):
        return f"index: {self.index}, 全局时间戳: {self.g_timestamp},channel: {self.channel}, 信号id:{self.message_id}, " \
               f"信号长度:{self.message_length}, 毫秒时间戳:{self.timestamp}, 信号内容:{self.message_data}"


class UdpPacket:
    """解析以太网数据包的属性信息"""
    def __init__(self, index, timestamp, ip_src, ip_dst, tcp_port_src, tcp_port_dst, payload,
                 payload_start, payload_length, downstream=True):
        self.index = index
        self.timestamp = timestamp
        self.ip_src = ip_src
        self.ip_dst = ip_dst
        self.tcp_port_src = tcp_port_src
        self.tcp_port_dst = tcp_port_dst
        self.payload = payload
        self.payload_start = payload_start  # 在总数据包中的起始字节
        self.payload_length = payload_length  # 该以太网帧的data的字节长度
        self.downstream = downstream

    def __repr__(self):
        detail = f"报文序号：{self.index}, 时间戳：{self.timestamp}, 起始位置:{self.payload_start}, " \
                 f"报文长度：{self.payload_length}, 报文内容：{self.payload}"
        return detail


if __name__ == '__main__':
    # frame = "18060d092f0502048002e8080a0200000000000008021002e8108e8e8e8e00000000000000000000000008005002e820ff0000000000500000000000000000000000000000000000000000000000000008019002e8083116f64b4000000008012002e808feb000010180c00008034002e808000002001000400004053f02e90800000000000000002a2802ec087f000000000000000200e102ed08a0001c002300000008023002ed08000000000000000002026002ed10000000fd00400004004001000021000008021f02ed08200000000000000002032002ed08000000000080000002021002ed100020000053b4b7044000002f3e00000008026002ed400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002020102ed08801c11550000000008030002ed08000000000060000002005002ed08000000000481c08008020002ee080000002ca800000008015a02ee080000000000002000fe"
    # a = PcapParseUdpInfo()
    # print(f"解析结果：{a.parse_signal_info(frame)}")
    # # a.parse_signal_info(frame)

    s = SniffPacket_process()
    s.set_iface("enx68da73ad3be6")
    s.sniff_start_process()
    time.sleep(0.5)
    s.stop_sniff_process()
    a = PcapParseUdpInfo()
    a.parse_pcap_file(s.pcap_file_name)
    # for i in a.up_payload:
    # print(a.up_payload)
    b = a.parse_signal_info()
    
    print(f"aaaaaaaaaaaaa{a.tcp_packet_list}")
    print(f"%%%%%%%%{a.frame_obj_dict},长度{len(a.frame_obj_dict)}")
    print("---------------------------------------/n")
    print(f"异常的包：{a.data_error_packet_dict}")
    print(f"时差的包：{a.time_error_packet_dict}")

