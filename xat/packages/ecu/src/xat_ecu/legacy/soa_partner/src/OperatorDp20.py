#!/usr/bin/python3


import os
from signal import signal
import signal
import sys
import subprocess
import socket
import json
import time
project_path = "/root/1022"
from xat_ecu.legacy.soa_partner.src.Const import *
from xat_ecu.legacy.common.logger import logger

bootesflag = True   # 现在只有 bootes 版本了
MESSAGE_LENGTH_BYTES_FMT = '%08x'
MESSAGE_LENGTH_BYTES = 4


def send_data_to(conn, data):
    byte_len = MESSAGE_LENGTH_BYTES_FMT % len(json.dumps(data))
    conn.sendall(bytes(byte_len + json.dumps(data), encoding='utf-8'))


def recv_data_from(conn):
    recv_data = b''
    msg_len_bcd = conn.recv(MESSAGE_LENGTH_BYTES * 2)
    msg_len = int(msg_len_bcd.decode('utf-8'), 16)
    while msg_len > len(recv_data):
        data = conn.recv(BUFFER_SIZE)
        recv_data += data
    return recv_data


class SOAOperator():
    def __init__(self, name=None, operator_port=DEFAULT_PORT):
        self.operator_port = operator_port
        self.pid = None
        self.name = name
        self.tcp_socket = None

    def run_operator(self, domin='tcam'):
        if bootesflag:
            project_path = "/opt"
            projectpath = project_path + "/partnerEnv"
            idl_path = projectpath + '/utils/partner'
            apus_path = os.path.join(projectpath, 'pc_linux_x86_64')
            soa_partner_path = os.path.join(projectpath, 'utils', 'bin', 'soa_partner')
            start_cmd = f'{soa_partner_path} -r {idl_path} -s {apus_path} run -d acu -p {self.operator_port}'
            logger.info(start_cmd)
            # cd /root/1022/partnerEnv/utils  ./bin/soa_partner -r partner/ -s ../pc_linux_x86_64 run -p 16789 -d tcam

        self.process = subprocess.Popen(start_cmd, shell=True, close_fds=True, preexec_fn=os.setsid)
        self.pid = self.process.pid

    def stop_operator(self):
        try:
            if self.tcp_socket is not None:
                self.tcp_socket.close()
            self.process.terminate()
            self.process.wait()
            os.killpg(self.pid, signal.SIGINT)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/OperatorDp20.py")
            logger.warning("Stop SOA operator Error : {}".format(e))

    def create_socket(self):
        """与operator代理建链"""
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.connect(('127.0.0.1', self.operator_port))

    def send_request(self, function, args=None, print_result=True):
        """向operator代理发送请求"""
        try:
            send_data_to(self.tcp_socket, {
                "action": "request",
                "function": function,
                "args": args
            })
            recv_data = recv_data_from(self.tcp_socket)
            resp = json.loads(recv_data.decode("utf-8"))
            result = json.loads(resp['result'])
            if print_result:
                logger.info(f"{function}-->{result}")
            return result
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/OperatorDp20.py")
            logger.error(f"发送失败，当前存在问题{e}")

