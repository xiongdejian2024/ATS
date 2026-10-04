
'''
Author: liu.yang
Date: 2023-02-01 19:05:06
LastEditors: Do not edit
LastEditTime: 2023-06-06 13:48:49
FilePath: /sat/xat_cases/legacy/bgm/case_helper/fota_case_helper/domain_helper.py
'''
import os
import sys
import socket
import json
import time
current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path, ".."))
sys.path.append(os.path.join(current_path, "../.."))
sys.path.append(os.path.join(current_path, "../../.."))
sys.path.append(os.path.join(current_path, "../../../.."))
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
project_path = os.path.join(os.path.realpath(__file__).split("soa_partner")[0], 'soa_partner')
sys.path.append(project_path)
from xat_ecu.legacy.soa_partner.src.Operator import SOAOperator
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.soa_partner.src.socket_recv import *
from xat_ecu.legacy.soa_partner.src.cdc_fota_master_client import CdcFotaMasterClient
from xat_ecu.legacy.soa_partner.src.acu_ua_server import AcuUaServer
from xat_ecu.legacy.soa_partner.src.cdc_ua_server import CdcUaServer
from xat_ecu.legacy.soa_partner.src.bgm_ua_client import BgmFotaUaClient
from xat_ecu.legacy.soa_partner.src.tcam_v2trouting_service import TcamV2TRoutingService

DEFAULT_PORT = 7000
MESSAGE_LENGTH_BYTES = 4
BUFFER_SIZE = 1024 * 1024

class Domain_Helper:
    # 封装CDC UA Client\Server端，ACU UA Server端, V2t Server端
    def __init__(self, cdc=False, acu=False, v2t = False, bgm = False):
        logger.info('Start partner operator...')
        self.cdc_sim_operator = SOAOperator("cdc_sim_op", DEFAULT_PORT + 1000) if cdc else None
        self.acu_sim_operator = SOAOperator("acu_sim_op", DEFAULT_PORT + 3000) if acu else None
        self.v2t_sim_operator = SOAOperator("v2t_sim_op", DEFAULT_PORT + 5000) if v2t else None
        self.bgm_sim_operator = SOAOperator("bgm_sim_op", DEFAULT_PORT + 7000) if bgm else None
        self.start_operators()
        time.sleep(2)
        self.start_skeleton_and_proxy()
        self.initiate_server_clients_controller()

    def initiate_server_clients_controller(self):
        logger.info("start init server client")
        # logger.info("========================{}==============================".format(self.cdc_sim_operator_cnn_info))
        self.fota_master_client = CdcFotaMasterClient(
            tuple(self.cdc_sim_operator_cnn_info["FotaMasterService_client"])) if self.cdc_sim_operator else None
        self.cdc_ua_server = CdcUaServer(
            tuple(self.cdc_sim_operator_cnn_info["UpdateAgentService_server"])) if self.cdc_sim_operator else None
        self.acu_ua_server = AcuUaServer(
            tuple(self.acu_sim_operator_cnn_info["UpdateAgentService_server"])) if self.acu_sim_operator else None
        self.v2t_server = TcamV2TRoutingService(
            tuple(self.v2t_sim_operator_cnn_info["V2TRoutingService_server"])) if self.v2t_sim_operator else None
        self.bgm_ua_client = BgmFotaUaClient(
            tuple(self.bgm_sim_operator_cnn_info["UpdateAgentService_client"])) if self.bgm_sim_operator else None
            
    def start_skeleton_and_proxy(self):
        logger.info("start skeleton & proxy...")
        if self.cdc_sim_operator:
            self.cdc_sim_operator_cfg = {"FotaMasterService": {"role": "client", "name": "FotaMasterService"},
                                         "UpdateAgentService": {"role": "server", "name": "CDC_UA_Service"}
                                         }
            self.cdc_sim_operator_cnn_info = self.start_and_get_socket_info(self.cdc_sim_operator_cfg, self.cdc_sim_operator)
        time.sleep(2)
        if self.acu_sim_operator:
            self.acu_sim_operator_cfg = {"UpdateAgentService": {"role": "server", "name": "ACU_UA_Service"}
                                         }
            self.acu_sim_operator_cnn_info = self.start_and_get_socket_info(self.acu_sim_operator_cfg, self.acu_sim_operator)
        time.sleep(2)
        if self.v2t_sim_operator:
            self.v2t_sim_operator_cfg = {"V2TRoutingService": {"role": "server", "name": "V2TRoutingService"}
                                         }
            self.v2t_sim_operator_cnn_info = self.start_and_get_socket_info(self.v2t_sim_operator_cfg, self.v2t_sim_operator)
        time.sleep(2)
        if self.bgm_sim_operator:
            self.bgm_sim_operator_cfg = {"UpdateAgentService": {"role": "client", "name": "BGM_UA_Service"}
                                         }
            self.bgm_sim_operator_cnn_info = self.start_and_get_socket_info(self.bgm_sim_operator_cfg, self.bgm_sim_operator)
        time.sleep(2)
        

    def start_operators(self):
        if self.cdc_sim_operator:
            self.cdc_sim_operator.run_operator()
        if self.acu_sim_operator:
            self.acu_sim_operator.run_operator()
        if self.v2t_sim_operator:
            self.v2t_sim_operator.run_operator()
        if self.bgm_sim_operator:
            self.bgm_sim_operator.run_operator()
        
    def start_and_get_socket_info(self, cfg, operator_obj):
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect(('127.0.0.1', operator_obj.operator_port))
        req = {
            "action": "request",
            "function": "get_current_service_list",
            "args": None
        }
        send_data_to(tcp_socket, req)
        recv_data = recv_data_from(tcp_socket)
        resp = json.loads(recv_data.decode("utf-8"))
        result = json.loads(resp['result'])
        logger.info(result.keys())

        req = {
            "action": "request",
            "function": "start_config",
            "args": json.dumps(cfg)
        }
        send_data_to(tcp_socket, req)
        recv_data = recv_data_from(tcp_socket)
        resp = json.loads(recv_data.decode("utf-8"))
        result = json.loads(resp['result'])
        logger.info(result)
        tcp_socket.close()
        return result

    def kill_operators(self):
        if self.cdc_sim_operator:
            self.cdc_sim_operator.stop_operator()
        if self.acu_sim_operator:
            self.acu_sim_operator.stop_operator()
        if self.v2t_sim_operator:
            self.v2t_sim_operator.stop_operator()
        if self.bgm_sim_operator:
            self.bgm_sim_operator.stop_operator()

    def reset_operator(self, operator_obj):
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect(('127.0.0.1', operator_obj.operator_port))
        req = {
            "action": "request",
            "function": "reset",
            "args": None
        }
        tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
        recv_data = recv_data_from(tcp_socket)
        resp = json.loads(recv_data.decode("utf-8"))
        result = json.loads(resp['result'])
        logger.info(f'operator for {operator_obj.name} close result: {result}')
        tcp_socket.close()

        
if __name__ == "__main__":
    pass