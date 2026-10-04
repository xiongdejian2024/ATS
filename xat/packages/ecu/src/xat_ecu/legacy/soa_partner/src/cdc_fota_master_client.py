#!/usr/bin/python3

import threading
import time
import socket
import sys
import os
import json
project_path = os.path.join(os.path.realpath(__file__).split("soa_partner")[0], 'soa_partner')
from xat_ecu.legacy.common.logger import logger
from src.socket_recv import *

DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000
MESSAGE_LENGTH_BYTES = 4




class CdcFotaMasterClient():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        logger.info(self.connect_info)
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stop_loop = False
        self.event_list = []
        self.resp_list = []

    
    def listening(self):
        while not self.stop_loop:
            recv_data = self.tcp_socket.recv(BUFFER_SIZE)
            if len(recv_data) == 0:
                break
            recv_data_list = self.handle_socket_data(recv_data)
            # recv_data_json = json.loads(recv_data.decode('utf-8'))
            logger.info("===================================")
            logger.info(recv_data_list)
            logger.info("===================================")
            for items in recv_data_list:
                if items.get("action") == "event":
                    self.event_list.append(items)
                elif items.get("action") == "response":
                    self.resp_list.append(items)
                else:
                    logger.info(f"=========not dentify========={items}")

    def handle_socket_data(self, raw):
        """
        有时会有多个事件上报，需要数据处理成列表
        :param raw: 如 b'{"action":"event","function":"UpdatePressureEvent","args":"{\\"sts\\":{\\"id\\":3,\\"pressure\\":260.8699951171875}}","failtype":""}{"action":"event","function":"UpdateTemperatureEvent","args":"{\\"sts\\":{\\"id\\":3,\\"temperature\\":49}}","failtype":""}'
        :return:
        """
        
        raw_data = raw.decode('utf-8')
        raw_data = raw_data.replace('false', "False")
        raw_data = raw_data.replace('true', "True")
        raw_data = raw_data.replace('null', "None")
        if '}{' not in raw_data:
            return [json.loads(raw_data)]
        else:
            raw_datas = raw_data.replace('}{', '}|{').split('|')
            return [eval(raw) for raw in raw_datas]

    def get_release_note_request(self):
        args = {}
        req = {
            "action":"request",
            "function": "GetTaskInfo",
            "args": json.dumps(args)
        }
        self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
    
    def start_download(self):
        args = {}
        req = {
            "action": "request",
            "function": "StartDownload",
            "args": json.dumps(args)
        }
        self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))

    def start_update(self):
        args = {}
        req = {
            "action": "request",
            "function": "StartUpdate",
            "args": json.dumps(args)
        }
        self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
        
    def get_ConditionCheck(self):
        args = {}
        req = {
            "action": "request",
            "function": "GetConditionCheck",
            "args": json.dumps(args)
        }
        self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
        
    def check_task(self):
        args = {
            "cmd": 0
        }
        req = {
            "action": "request",
            "function": "CheckTask",
            "args": json.dumps(args)
        }
        self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))

    def clear_list(self):
        self.resp_list.clear()
        self.event_list.clear()
        
    def check_event(self, field1 = '', field2 = '', field3 = ''):
        """ 
        {
            "status": {
                "taskId": 0,
                "state": 0,
                "errorCode": 0
            }
        }        
        """
        self.clear_list()
        time.sleep(3)
        retry_count = 1
        while True:
            if len(self.event_list) != 0:
                logger.info(self.event_list)
                event = self.event_list[-1]
                if event.get("function") == "UpdateStatusEvent":
                    args_json = event.get("args")
                    args = json.loads(args_json)
                    return self.get_nested_value(args, field1, field2, field3)
                else:
                    logger.error(f'''Current event 【{event.get("function")}】 not equal 【UpdateStatusEvent】''')
                    time.sleep(3)
            else:
                logger.error(f"No events have been received yet, retry {retry_count} times") 
                logger.info(f"//////////////////{self.event_list}//////////////////////")
                retry_count = retry_count + 1
                if retry_count > 9:
                    return None
                time.sleep(10)    

    def till_status_to(self, target_status, timeout):
        start_time = time.time()
        while True:
            cur_time = time.time()
            if cur_time - start_time > timeout:
                assert False, "Function timed out"
            else:
                curr_status = self.check_event(field1="status", field2="state")
                if curr_status == target_status:
                    return True
                else:
                    time.sleep(3)
                    logger.info(f"Current FOTA Satus is {curr_status}")
                    
    def till_taskid_to(self, target_status, timeout):
        start_time = time.time()
        while True:
            cur_time = time.time()
            if cur_time - start_time > timeout:
                assert False, "Function timed out"
            else:
                curr_status = self.check_event(field1="status", field2="taskId")
                if curr_status == target_status:
                    return True
                else:
                    time.sleep(3)
                    logger.info(f"Current FOTA Taskid is {curr_status}")

    def get_nested_value(self, info_dict, value1, value2, value3):
        if all(v == '' for v in [value1, value2, value3]):
            return info_dict
        elif len(value1) != 0 and len(value2) == 0:
            return info_dict.get(value1)
        elif len(value2) != 0 and len(value3) == 0 and isinstance(info_dict.get(value1), dict):
            return info_dict.get(value1).get(value2)
        elif len(value3) != 0 and isinstance(info_dict.get(value1).get(value2), dict):
            return info_dict.get(value1).get(value2).get(value3)
        
    def start_listening(self):
        self.listening_thread = threading.Thread(name="FotaMasterClientListening", target=self.listening,)
        self.listening_thread.start()

    def start(self):
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/cdc_fota_master_client.py")
            logger.error(str(e))
        self.start_listening()

    
    def distroy(self):
        self.stop_loop = True