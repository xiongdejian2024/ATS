#!/usr/bin/python3

import socket
import sys
import os
import threading
import json
import time
project_path = os.path.join(os.path.realpath(__file__).split("soa_partner")[0], 'soa_partner')
from xat_ecu.legacy.common.logger import logger

DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class TcamFotaUaClient():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        logger.info(self.connect_info)
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stop_loop = False
        self.resp_list = []
        self.event_list = []

    def listening(self):
        while not self.stop_loop:
            recv_data = self.tcp_socket.recv(BUFFER_SIZE)
            if len(recv_data) == 0:
                    break
            recv_data_json = json.loads(recv_data.decode('utf-8'))
            if recv_data_json.get("action") == "event":
                self.event_list.append(recv_data_json)
            elif recv_data_json.get("action") == "response":
                self.resp_list.append(recv_data_json)
            else:
                logger.info(f"=========not dentify========={recv_data_json}")
                
    def check_response(self, function, value1 = '', value2 = '', value3 = ''):
        """ 
        以 GetStatus 为例：
        {
            "out": {
                "status": 0,
                "downloadStatus": {
                    "downloadFileSize": 0,
                    "totalFileSize": 0,
                    "downloadSpeed": 0,
                    "status": 255
                },
                "preUpdateStatus": {
                    "progress": 0,
                    "status": 255
                },
                "updateStatus": {
                    "updateFileSize": 0,
                    "totalFileSize": 0,
                    "status": 255
                },
                "errorCode": 780
            }
        }
        """
        time.sleep(2.5)
        for resp in self.resp_list:
            if resp.get("function") == function:
                result_json = resp.get("result")
                result = json.loads(result_json)
                return self.get_nested_value(result, value1, value2, value3)
            else:
                logger.error(f"Function 【{function}】 with no response")
                
    def check_event(self, value1 = '', value2 = '', value3 = ''):
        """ 
        {
            "status": {
                "status": 0,
                "downloadStatus": {
                    "downloadFileSize": 0,
                    "totalFileSize": 0,
                    "downloadSpeed": 0,
                    "status": 255
                },
                "preUpdateStatus": {
                    "progress": 0,
                    "status": 255
                },
                "updateStatus": {
                    "updateFileSize": 0,
                    "totalFileSize": 0,
                    "status": 255
                },
                "errorCode": 0
            }
        }
        """
        self.clear_list()
        time.sleep(3)
        retry_count = 1
        while True:
            if len(self.event_list) != 0:
                event = self.event_list[-1]
                if event.get("function") == "UpdateStatusEvent":
                    args_json = event.get("args")
                    args = json.loads(args_json)
                    logger.info("00000000000000000000000000")
                    logger.info(self.event_list)
                    logger.info("99999999999999999999999999")
                    return self.get_nested_value(args, value1, value2, value3)
                else:
                    logger.error(f'''Current event 【{event.get("function")}】 not equal 【UpdateStatusEvent】''')
            else:
                logger.error(f"No events have been received yet, retry {retry_count} times") 
                retry_count = retry_count + 1
                if retry_count > 3:
                    return False
                time.sleep(10)   
                
    def get_nested_value(self, info_dict, value1, value2, value3):
        if all(v == '' for v in [value1, value2, value3]):
            return info_dict
        elif len(value1) != 0 and len(value2) == 0:
            return info_dict.get(value1)
        elif len(value2) != 0 and len(value3) == 0 and isinstance(info_dict.get(value1), dict):
            return info_dict.get(value1).get(value2)
        elif len(value3) != 0 and isinstance(info_dict.get(value1).get(value2), dict):
            return info_dict.get(value1).get(value2).get(value3)

    def till_status_to(self, target_status, timeout):
        start_time = time.time()
        while True:
            cur_time = time.time()
            if cur_time - start_time > timeout:
                assert False, "Function timed out"
            else:        
                curr_status = self.check_event(value1="status", value2="status")
                if curr_status == target_status:
                    return True
                else:
                    time.sleep(3)
                    logger.info(f"Current TCAM UA Satus is {curr_status}")
                
    def till_ua_preUpdateStatus_to(self, target_status, timeout):
        start_time = time.time()
        while True:
            cur_time = time.time()
            if cur_time - start_time > timeout:
                assert False, "Function timed out"
            else:  
                curr_status = self.check_event(value1="status", value2="preUpdateStatus", value3="status")
                if curr_status == target_status:
                    return True
                else:
                    time.sleep(3)
                    logger.info(f"Current UA preUpdateStatus is {curr_status}")
        
    def clear_list(self):
        self.resp_list.clear()
        self.event_list.clear()
    
    def start_listening(self):
        self.listening_thread = threading.Thread(name="UpgradeAgentClientListening", target=self.listening,)
        self.listening_thread.start()

    def start_download(self):
        self.clear_list()
        args = {
            "downloadReq": {
                "fileNumber": 1,
                "fileInformations": [
                    {
                        "pn": "8895036217  A",
                        "version": "6110110130 AH",
                        "size": 179964464,
                        "fileName": "6110110130AH.bin",
                        "url": "https://t-ivs-fota.cdn.bcebos.com/ofm/eab3f1ba59cad58cbe38ca9e287f2dcfeab334d5/697e8cbf-cc2b-c759-d4f7-b24a5a2de4f7/6110110130AH.bin?responseCoe=application%2Foctet-stream&authorization=bce-auth-v1%2F289a3f3e82b34da4973652d035b59cc3%2F2023-11-02T07%3A41%3A04Z%2F-1%2F%2F32a4865210280a21e3683ffed07b4f76397a9e5be097ff1784e13b6614881be7",
                        "signature": "MEUCIAiRsM1qAH5VA459AJHnQpEa6zNbOon0Vi0Z2qT5fgJUAiEA5mRcWnWEWw1y8hRc7swUqAhKF2YeSzDCWN/EIWsDaBQ=",
                        "keyId": "6eb9864c734f402eb6242e3b880b7f69",
                        "encKey": __import__("os").environ['XAT_CREDENTIAL_SCAN_F4A5E792D2F20A933203']
                    }
                ],
                "keyInformation": {
                    "keyId": "6eb9864c734f402eb6242e3b880b7f69",
                    "encKey": __import__("os").environ['XAT_CREDENTIAL_SCAN_F363FF4F5F79C2379513']
                },
                "mode": 0
            }
        }        
        
        # args = {
        #     "downloadReq": {
        #         "fileNumber": 1,
        #         "fileInformations": [
        #             {
        #                 "pn": "8895036217  A",
        #                 "version": "6110110110 HH",
        #                 "size": 177373152,
        #                 "fileName": "6110110110HH.bin",
        #                 "url": "https://t-ivs-fota.cdn.bcebos.com/ofm/23b0dfc791eb0fe1c788c1b260686c5b1c5917fc/1e20d4a5-5dd4-6522-fd2d-0ed9b401426c/6110110110HH.bin?responseContentType=application%2Foctet-stp",
        #                 "signature": "MEYCIQCOADsut2LBtt+41wlwLM5SJmnun1vPQaQtR3J+fPMUGQIhAKZtgRqUo5RFrPRcaEEhS8whK0wqO3RnKemXZMJDmh7x",
        #                 "keyId": "bd33c64503764adbb4205e1c547cc144",
        #                 "encKey": "${XAT_CREDENTIAL_SCAN_5079FDB171B27DAB1DD8}"
        #             }
        #         ],
        #         "keyInformation": {
        #             "keyId": "bd33c64503764adbb4205e1c547cc144",
        #             "encKey": "${XAT_CREDENTIAL_SCAN_5079FDB171B27DAB1DD8}"
        #         },
        #         "mode": 0
        #     }
        # }
        req = {
            "action": "request",
            "function": "StartDownload",
            "args": json.dumps(args)
        }
        self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
        logger.info("【StartDownload】")

    def cancel_download(self):
        self.clear_list()
        args = {}
        req = {
            "action": "request",
            "function": "CancelDownload",
            "args": json.dumps(args)
        }
        self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))

    def get_status(self):
        self.clear_list()
        args = {}
        req = {
            "action": "request",
            "function": "GetStatus",
            "args": json.dumps(args)
        }
        self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
    
    def start_update(self):
        self.clear_list()
        args = {}
        req = {
            "action": "request",
            "function": "StartUpdate",
            "args": json.dumps(args)
        }
        self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
        
    def pre_update(self):
        self.clear_list()
        args = {}
        req = {
            "action": "request",
            "function": "PreUpdate",
            "args": json.dumps(args)
        }
        self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))

    def activate(self):
        self.clear_list()
        args = {}
        req = {
            "action": "request",
            "function": "Activate",
            "args": json.dumps(args)
        }
        self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
        
    def finish_update(self):
        self.clear_list()
        args = {}
        req = {
            "action": "request",
            "function": "FinishUpdate",
            "args": json.dumps(args)
        }
        self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
        
    def cancel_update(self):
        self.clear_list()
        args = {}
        req = {
            "action": "request",
            "function": "CancelUpdate",
            "args": json.dumps(args)
        }
        self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
        logger.info("【CancelUpdate】")
        
    def roll_back(self):
        self.clear_list()
        args = {}
        req = {
            "action": "request",
            "function": "Rollback",
            "args": json.dumps(args)
        }
        self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
        
    def cancel_to_Idle(self):
        self.clear_list()
        args = {}
        while True:
            ua_status = self.check_event("status", "status")
            if ua_status == 0:
                logger.info(f"UA Status is already Idle{self.event_list}")
                break
            elif ua_status == 1:           
                req = {
                    "action": "request",
                    "function": "CancelDownload",
                    "args": json.dumps(args)
                }
                logger.info("UA Status is Downloading, send CancelDownload")
                self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))    
                time.sleep(10)
            elif ua_status == 3:
                logger.info("UA Status is still Installing, wait 60s")
                time.sleep(60)
            elif ua_status == 6:
                self.finish_update()
                time.sleep(60)
            else:
                req = {
                    "action": "request",
                    "function": "CancelUpdate",
                    "args": json.dumps(args)
                }
                logger.info(f"UA Status is {ua_status}, send CancelUpdate")
                self.tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))    
                time.sleep(10)

    def start(self):
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/tcam_ua_client.py")
            logger.error(str(e))
        self.start_listening()
    
    def distroy(self):
        self.stop_loop = True
