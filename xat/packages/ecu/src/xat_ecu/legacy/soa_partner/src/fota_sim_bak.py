#!/usr/bin/python3


import socket
import json
import time
import os
import sys
project_path = os.path.join(os.path.realpath(__file__).split("soa_partner")[0], 'soa_partner')
from src.Const import *
from xat_ecu.legacy.common.logger import logger
from src.Operator import SOAOperator
from src.bgm_fota_master_server import BgmFotaMasterServer
from src.bgm_ua_client import BgmFotaUaClient
from src.cdc_fota_master_client import CdcFotaMasterClient
from src.cdc_ua_server import CdcUaServer
from src.bgm_hv_service_server import BgmHvServer
from src.cdc_hv_service_client import CdcHvClient


class FotaSim:
    def __init__(self, cdc_ua=False) -> None:
        logger.info('Start partner operator...')
        self.bgm_sim_operator = SOAOperator('fota_sim')
        self.cdc_sim_operator = SOAOperator('cdc_ua_sim', DEFAULT_PORT+1000) if cdc_ua else None
        self.start_operators()
        time.sleep(2)
        self.start_skeleton_and_proxy()
        self.initiate_server_clients_controller()



    def initiate_server_clients_controller(self):
        logger.info("start init server client")
        self.fota_master_server = BgmFotaMasterServer(tuple(self.bgm_sim_operator_cnn_info["FotaMasterService_server"]))
        self.hv_service_server = BgmHvServer(tuple(self.bgm_sim_operator_cnn_info["HighVoltageService_server"]))
        self.fota_ua_server = CdcUaServer(tuple(self.cdc_sim_operator_cnn_info["UpdateAgentService_server"])) if self.cdc_sim_operator else None
        time.sleep(5)
        self.fota_ua_client = BgmFotaUaClient(tuple(self.bgm_sim_operator_cnn_info["UpdateAgentService_client"]))
        time.sleep(2)
        self.fota_master_client = CdcFotaMasterClient(tuple(self.cdc_sim_operator_cnn_info["FotaMasterService_client"])) if self.cdc_sim_operator else None
        time.sleep(2)
        self.hv_service_client = CdcHvClient(tuple(self.cdc_sim_operator_cnn_info["HighVoltageService_client"])) if self.cdc_sim_operator else None



    def start_skeleton_and_proxy(self):
        logger.info("start skeleton & proxy...")
        self.bgm_sim_operator_cfg = {"FotaMasterService": "server", "HighVoltageService": "server"}  # start skeleton first
        self.bgm_sim_operator_cnn_info = self.start_and_get_socket_info(self.bgm_sim_operator_cfg, self.bgm_sim_operator)
        time.sleep(2)
        if self.cdc_sim_operator:
            self.cdc_sim_operator_cfg = {"UpdateAgentService": "server", "FotaMasterService": "client", "HighVoltageService": "client"}
            self.cdc_sim_operator_cnn_info = self.start_and_get_socket_info(self.cdc_sim_operator_cfg, self.cdc_sim_operator)
        time.sleep(2)
        self.bgm_sim_operator_cfg = {"FotaMasterService": "server", "HighVoltageService": "server", "UpdateAgentService": "client"}  # start skeleton & proxy
        self.bgm_sim_operator_cnn_info = self.start_and_get_socket_info(self.bgm_sim_operator_cfg, self.bgm_sim_operator)
        logger.info(self.bgm_sim_operator_cnn_info)
        logger.info(self.cdc_sim_operator_cnn_info)
        time.sleep(2)


    def start_operators(self):
        if self.bgm_sim_operator:
            self.bgm_sim_operator.start()
        if self.cdc_sim_operator:
            self.cdc_sim_operator.start()
    
    def start_and_get_socket_info(self, cfg, operator_obj):
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect(('127.0.0.1', operator_obj.start_port))
        req = {
            "action": "request",
            "function": "get_current_service_list",
            "args": None
        }
        tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
        recv_data = tcp_socket.recv(BUFFER_SIZE)
        resp = json.loads(recv_data.decode("utf-8"))
        result = json.loads(resp['result'])
        logger.info(result.keys())

        req = {
            "action": "request",
            "function": "start_config",
            "args": json.dumps(cfg)
        }
        tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
        recv_data = tcp_socket.recv(BUFFER_SIZE)
        resp = json.loads(recv_data.decode("utf-8"))
        result = json.loads(resp['result'])
        logger.info(result)
        tcp_socket.close()
        # connect_info = tuple(result[f'{service}_{role}'])
        return result

    def kill_operators(self):
        self.reset_operator(self.bgm_sim_operator)
        self.bgm_sim_operator.join()
        if self.cdc_sim_operator:
            self.reset_operator(self.cdc_sim_operator)
            self.cdc_sim_operator.join()

    def reset_operator(self, operator_obj):
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect(('127.0.0.1', operator_obj.start_port))
        req = {
            "action": "request",
            "function": "reset",
            "args": None
        }
        tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
        recv_data = tcp_socket.recv(BUFFER_SIZE)
        resp = json.loads(recv_data.decode("utf-8"))
        result = json.loads(resp['result'])
        logger.info(f'operator for {operator_obj.name} close result: {result}')
        tcp_socket.close()

        




if __name__ == "__main__":
    fota_sim = FotaSim(True)
    # logger.info('Initiate fota master server...')
    # bgm_fota_master = BgmFotaMasterServer()
    # bgm_fota_master.start()
    # logger.info('Initiate fota ua client')
    # bgm_ua_client = BgmFotaUaClient()
    # time.sleep(8)

