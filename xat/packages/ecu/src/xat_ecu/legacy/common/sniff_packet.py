#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : sniff_packet.py
@time         : 2023/12/8 15:54
@author       : wenyu.liang_ext@jiduauto.com
@description  : 
'''
import threading
import time
import os
import subprocess
from xat_ecu.legacy.common.logger import logger
from scapy.sendrecv import sniff
from scapy.utils import wrpcap,rdpcap

class SniffPacket_thread: #线程抓包概率影响性能 刷写压测请用进程抓包
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

    def set_iface(self, iface):
        self.iface = iface

    def set_save_path(self, save_path):
        self.save_path = save_path

    def set_save_name(self, save_name):
        self.save_name = save_name

    def start_sniff(self, **kwargs):
        '''
        开启抓包线程
        @param kwargs:
        @return:
        '''
        t = threading.Thread(target=self.__sniff_func)
        t.setDaemon(True)
        t.start()
        time.sleep(2)

    def __sniff_func(self):
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
                file_path = os.path.join(self.save_path, save_name)
                logger.info(f"保存obd口抓包文件路径为===>>>{file_path}")
                wrpcap(file_path, recv_packet)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/common/sniff_packet.py")
                wrpcap(f"doip_{otherStyleTime}.pcap", recv_packet)
                logger.error(f"{str(e)}")

    def stop_flter(self, packet):
        return self.sniff_flag

    def stop_sniff(self):
        # time.sleep(2)
        self.sniff_flag = True
        time.sleep(2)
        
class SniffPacket_process: #进程抓包
    def __init__(self, **kwargs):
        # 所抓网口 名字
        self.iface = kwargs.get("iface", None)
        # 保存路径
        self.save_path = kwargs.get("save_path", '/root/obd_doip_dump')
        # 保存名字
        self.save_name = kwargs.get("save_name", 'obd_doip_')
        self.p = None
        # self.tcp_dump_log = None
    
    def set_iface(self,iface):
        self.iface = iface

    def set_save_path(self, save_path):
        self.save_path = save_path

    def set_save_name(self, save_name):
        self.save_name = save_name
        
    def sniff_start_proccess(self):
        now_time = time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime(int(time.time())))
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        # file_path = os.path.join(self.save_path,self.save_name)
        # self.p = subprocess.Popen(f'tcpdump -i {self.iface} -w {file_path}.pcap -s 128',shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        file_path = os.path.join(self.save_path, self.save_name) + '.pcap'
        # self.tcp_dump_log = open(file_path, 'w', encoding='utf-8')
        try:
            self.tcpdump_process = subprocess.Popen(f"tcpdump -i {self.iface} -s 128 -w {file_path}", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/common/sniff_packet.py")
            logger.warning(f"tcpdump 命令执行失败：{e}")
            if self.tcpdump_process:
                self.tcpdump_process.terminate()
                self.tcpdump_process.kill()
                self.tcpdump_process = None

        logger.info("抓包开始 等待2s")
        time.sleep(2)
        
    def sniff_stop_process(self):
        logger.info("抓包结束 等待3s")
        time.sleep(3)

        if hasattr(self, 'tcpdump_process') and self.tcpdump_process.poll() is None:
            try:
                self.tcpdump_process.terminate()  # 终止tcpdump进程
                try:
                    # 等待一段时间（可选）
                    self.tcpdump_process.wait(timeout=5)  # 等待5秒
                except subprocess.TimeoutExpired:
                    logger.info("tcpdump 没有在5秒内响应 SIGTERM，现在发送 SIGKILL")
                    self.tcpdump_process.kill()
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/common/sniff_packet.py")
                logger.error(f"停止tcpdump进程失败: {e}")
            finally:
                time.sleep(2)
                # 确保抓包进程已停止
                subprocess.Popen("ps -ef | grep tcpdump| awk '{print $2}' | xargs kill -9",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                logger.info("停止抓包进程成功")
        else:
            logger.warning("tcpdump进程已不存在或已停止")
