#!/usr/bin/python3

import threading
import time
import socket
import sys
import os
import json
project_path = os.path.join(os.path.realpath(__file__).split("soa_partner")[0], 'soa_partner')
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger

DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class BgmFotaMasterServer():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.current_status = ""
        self.status_args = {
            "status": {
                "taskId": int(time.time()),
                "state": 1,  # idle
                "errorCode": 0
            }
        }
        self.task_info_args = {
                "out":{
                    "version":"abcd",
                    "updateTime":30000,
                    "releaseNoteUrl": "http://faselkjf",
                    "updateTitle":"v0.4",
                    "updatePackageTotalSize": 1223,
                    "publishTime": "2022-03-22",
                    "termsOfService": "flkjhehf",
                    "sucessMessage": "success",
                    "failMessageAvailable": "fail occur",
                    "failMessageNotAvailable": "fail not show"
                    }
                }
            
        self.start_download_response_args = {"out": 0}
        
        self.start_update_response_args = {"out": 0}
        
        self.download_process_args = {
            "downloadProgress":{
                "taskId": self.status_args.get("status").get("taskId"),
                "state": 0,  # download_running
                "progress": 0,
                "downloadSpeed": 11,
                "leftTime": 1000,
                "errorCode": 0
            }
        }

        self.update_process_args = {
            "updateProgress": {
                "taskId": self.status_args.get("status").get("taskId"),
                "state": 0,  # running
                "progress": 0,
                "leftTime": 1000,
                "errorCode": 0
            }
        }
        self.stop_loop = False
        self.download_process_loop = False
        self.update_process_loop = False

    def status_periodic_send(self, interval=1):
        while not self.stop_loop:
            event = {
            "action":"event",
            "function": "UpdateStatusEvent",
            "args": json.dumps(self.status_args)
            }
            try:
                self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
            except BrokenPipeError as e:
                logger.error(f"fota master send periodic status failure with broken pipe: {str(e)}")
            # logger.info("sending {}".format(json.daumps(event)))
            time.sleep(interval)

    def listening(self):
        while not self.stop_loop:
            logger.info("in fota master listen loop")
            # recv_data = recv_data_from(self.tcp_socket)
            recv_data = self.tcp_socket.recv(BUFFER_SIZE)
            if len(recv_data) == 0:
                break
            recv_data_json = json.loads(recv_data.decode('utf-8'))
            logger.info(recv_data_json)
            if recv_data_json.get("function") == "GetTaskInfo":
                logger.info("receiving GetTaskInfo from client")
                self.current_status = "GetTaskInfo"
                self.on_get_task_info()
            if recv_data_json.get("function") == "StartDownload":
                logger.info("receiving StartDownload from client")
                self.current_status = "StartDownload"
                self.on_start_download()
            if recv_data_json.get("function") == "StartUpdate":
                logger.info("receiving StartUpdate from client")
                self.current_status = "StartUpdate"
                self.on_start_update()
            if recv_data_json.get("function") == "CancelFota":
                logger.info("receiving CancelFota from client")
                self.current_status = "CancelFota"
                self.on_cancel_fota()
                

    def on_get_task_info(self):
        resp = {
            "action": "response",
            "function": "GetTaskInfo",
            "result": json.dumps(self.task_info_args)
        }
        logger.info(json.dumps(resp))
        time.sleep(0.2)
        try:
            self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"fota master send get_task_info response with broken pipe: {str(e)}")

    def on_start_download(self):
        # args = {
        #         "out":{
        #             "errorCode": 0
        #         }
        #     }
        resp = {
            "action": "response",
            "function": "StartDownload",
            "result": json.dumps(self.start_download_response_args)
        }
        logger.info(json.dumps(resp))
        try:
            self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"fota master send start_download response with broken pipe: {str(e)}")

    def on_cancel_fota(self):
        args = {
                "out":{
                    "errorCode": 0
                }
            }
        resp = {
            "action": "response",
            "function": "CancelFota",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        try:
            self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"fota master send cancel fota response with broken pipe: {str(e)}")

    def on_start_update(self):
        
        resp = {
            "action": "response",
            "function": "StartUpdate",
            "result": json.dumps(self.start_update_response_args)
        }
        logger.info(json.dumps(resp))
        try:
            self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"fota master send start_update response with broken pipe: {str(e)}")

    def start_listening(self):
        self.listening_thread = threading.Thread(name="FotaMasterServerListening", target=self.listening,)
        self.listening_thread.start()

    def start(self):
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/bgm_fota_master_server.py")
            logger.error(str(e))
        self.start_sending_status()
        self.start_listening()

    def start_sending_status(self):
        self.status_thread = threading.Thread(name="FotaMasterStatusSending", target=self.status_periodic_send,)
        self.status_thread.start()

    def update_status_event(self, taskid=None, state=None, errorCode=None):
        if taskid:
            self.status_args["status"]["taskId"] = taskid
        if state:
            self.status_args["status"]["state"] = state
        if errorCode:
            self.status_args["status"]["errorCode"] = errorCode
    
    def download_process_periodic_send(self, step=1, interval=1):
        while self.download_process_loop and not self.stop_loop:
            event = {
            "action":"event",
            "function": "UpdateDownloadProcessEvent",
            "args": json.dumps(self.download_process_args)
            }
            try:
                self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
            except BrokenPipeError as e:
                logger.error(f"fota master send periodic download process failure with broken pipe: {str(e)}")
            # logger.info("sending {}".format(json.dumps(event)))
            if self.download_process_args.get("downloadProgress").get("progress") < 100:
                self.download_process_args["downloadProgress"]["progress"] += step
            elif self.download_process_args.get("downloadProgress").get("progress") == 100:
                self.download_process_args["downloadProgress"]["state"] = 1
            time.sleep(interval)

    def update_process_periodic_send(self, step=1, interval=1):
        while self.update_process_loop and not self.stop_loop:
            event = {
            "action":"event",
            "function": "UpdateUpdateProcessEvent",
            "args": json.dumps(self.update_process_args)
            }
            try:
                self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
            except BrokenPipeError as e:
                logger.error(f"fota master send periodic update process failure with broken pipe: {str(e)}")
            # logger.info("sending {}".format(json.dumps(event)))
            if self.update_process_args.get("updateProgress").get("progress") < 100:
                self.update_process_args["updateProgress"]["progress"] += step
            elif self.update_process_args.get("updateProgress").get("progress") == 100:
                self.update_process_args["updateProgress"]["state"] = 1
            time.sleep(interval)
    
    def start_sending_download_process(self, step):
        self.download_process_loop = True
        self.download_thread = threading.Thread(name="FotaMasterDownloadProcessSending", target=self.download_process_periodic_send,args=(step,))
        self.download_thread.start()

    def start_sending_update_process(self, step):
        self.update_process_loop = True
        self.update_thread = threading.Thread(name="FotaMasterUpdateProcessSending", target=self.update_process_periodic_send,args=(step,))
        self.update_thread.start()

    def stop_sending_download_process(self):
        self.download_process_loop = False
        time.sleep(1)
        self.download_thread.join()

    def stop_sending_update_process(self):
        self.update_process_loop = False
        time.sleep(1)
        self.update_thread.join()
    
    def distroy(self):
        self.stop_loop = True
        time.sleep(2)
        # self.listening_thread.join()
        self.status_thread.join()
        
        logger.info("distory bgm fota master server")
        self.tcp_socket.close()
    
