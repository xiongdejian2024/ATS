# -*- coding: utf-8 -*-

import os
import sys
import time
import json
project_path = os.path.join(os.path.realpath(__file__).split("soa_partner")[0], 'soa_partner')
from xat_ecu.legacy.common.logger import logger

DEFAULT_PORT = 6789
MESSAGE_LENGTH_BYTES = 4
BUFFER_SIZE = 1024 * 1024
MESSAGE_LENGTH_BYTES_FMT = '%08x'

def recv_data_from(tcp_socket, timeout=0.5):
    '''
        MESSAGE_LENGTH_BYTES_FMT = '%08x'
        byte_len = MESSAGE_LENGTH_BYTES_FMT % len(json.dumps(resp))
        conn.sendall(bytes(byte_len + json.dumps(resp), encoding='utf-8'))
    '''
    recv_data = b''
    try:
        msg_len_bcd = tcp_socket.recv(MESSAGE_LENGTH_BYTES * 2)
        logger.info(msg_len_bcd)
        if len(msg_len_bcd) == 0:
            return recv_data
        msg_len = int(msg_len_bcd.decode('utf-8'), 16)
        curr_time = time.time()
        while msg_len > len(recv_data):
            if time.time() - curr_time > timeout:
                recv_data = b''  # 超时直接舍弃
                break
            data = tcp_socket.recv(BUFFER_SIZE)
            recv_data += data
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/socket_recv.py")
        logger.error(str(e))
    return recv_data

def send_data_to(conn, data):
    byte_len = MESSAGE_LENGTH_BYTES_FMT % len(json.dumps(data))
    conn.sendall(bytes(byte_len + json.dumps(data), encoding='utf-8'))