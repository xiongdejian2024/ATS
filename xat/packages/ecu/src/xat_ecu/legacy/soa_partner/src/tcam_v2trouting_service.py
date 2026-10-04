#!/usr/bin/python3

import socket
import sys
import os
import threading
import json

project_path = os.path.join(os.path.realpath(__file__).split("soa_partner")[0], 'soa_partner')
from xat_ecu.legacy.common.logger import logger

DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000


class TcamV2TRoutingService():
    # TCAM service
    def __init__(self, connect_info):
        self.connect_info = connect_info
        logger.info(self.connect_info)
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stop_loop = False
        self.task_flag = False
        self.pn_flag = False
        self.up_sw_hw_flag = False
        self.traceId = "A55A"

    def listening(self):
        while not self.stop_loop:
            recv_data = self.tcp_socket.recv(BUFFER_SIZE)
            if len(recv_data) == 0:
                break
            recv_data_json = json.loads(recv_data.decode('utf-8'))
            logger.info("receiving data from client : {}".format(recv_data_json))
            if recv_data_json.get("function") == "CallTspApi":
                args_json = recv_data_json.get("args")

                args = json.loads(args_json)
                self.traceId = args.get("traceId")

                payload_list = args.get("payload")
                payload_json = bytes(payload_list).decode('utf-8')
                payload = json.loads(payload_json)
                logger.info("receiving payload from client : {}".format(payload))

                if payload:
                    type = payload.get("type")
                    if type == 1:    #  To TSP   BaseLine
                        self.on_call_tsp_api()
                        self.task_flag = True
                    elif type == 3:   #   Response To TSP    zhen dui type 2
                        self.on_call_tsp_api()
                    elif type == 4:   #   To TSP   SW/HW  Version
                        self.on_call_tsp_api()
                        self.pn_flag = True
                    elif type == 8:   #  up To TSP  Vehicle Status
                        # {"data":{"StateCode":"01F1","taskId":1231},"type":8}  start collect SW/HW Version
                        # {"data":{"StateCode":"01F2","taskId":140},"type":8}   finish collect SW/HW Version
                        # {"data":{"stateCode":"01F3","taskId":140},"type":8}   received manifest
                        statecode = payload.get("data").get("StateCode")
                        self.on_call_tsp_api()
                        if statecode == "01F1":
                            logger.info("Recived -- start collect SW/HW Version")
                        elif statecode == "01F2":
                            logger.info("Recived -- finished UP SW/HW Version")
                            self.up_sw_hw_flag = True
                        elif statecode == "01F3":
                            logger.info("Recived -- received manifest")
                else:
                    logger.error("Receive Unexpected Data")
            elif recv_data_json.get("function") == "GetV2TConnectStatus":
                self.on_GetV2TConnectStatus()


    def start_listening(self):
        self.listening_thread = threading.Thread(name="TcamV2TRoutingService", target=self.listening, )
        self.listening_thread.start()

    def on_call_tsp_api(self):
        '''
                enum CallResult
        {
            @value(0) CALL_SUCCESS, //调用成功
          @value(1) CALL_FAIL, //调用失败,比如云端路由服务回复了错误
          @value(2) CALL_TSP_TIMEOUT,    //等待TSP回复超时
          @value(3) CALL_TSP_SERVICE_TIMEOUT //TSP业务端超时
        };
        '''
        payload = ""
        sequence_payload = list(bytes(payload, encoding='utf-8'))
        args = {
            "out": {
                "result": 0,
                "payload": sequence_payload
            }
        }
        resp = {
            "action": "response",
            "function": "CallTspApi",
            "result": json.dumps(args)
        }
        logger.info(json.dumps(resp))
        try:
            self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(e)


    def on_GetV2TConnectStatus(self):
        V2TConnectStatus = 0
        args = {
            "out": V2TConnectStatus
        }
        resp = {
            "action": "response",
            "function": "GetV2TConnectStatus",
            "result": json.dumps(args)
        }
        logger.info("Send : {}".format(json.dumps(resp)))
        try:
            self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(e)

    def start(self):
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/tcam_v2trouting_service.py")
            logger.error(str(e))
        self.start_listening()

    def distroy(self):
        self.stop_loop = True
