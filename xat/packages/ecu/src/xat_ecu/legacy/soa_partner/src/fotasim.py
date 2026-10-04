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
from src.socket_recv import *
from src.bgm_fota_master_server import BgmFotaMasterServer
from src.bgm_ua_client import BgmFotaUaClient
from src.cdc_fota_master_client import CdcFotaMasterClient
from src.tcam_v2trouting_service import TcamV2TRoutingService
from src.bgm_v2trouting_client import BgmV2TRoutingClient
from src.tcam_v2t_routing_forwarder_client import TcamV2TRoutingForwarderClient
from src.bgm_v2t_routing_forwarder_service import BgmV2TRoutingForwarderService
from src.tcam_task_exec_forwarder_client import TcamTaskExecForwarderClient
from src.bgm_task_exec_forwarder_service import BgmVTaskExecForwarderService
from src.tcam_task_exec_service import TcamTaskExecServiceService
from src.bgm_task_exec_client import BgmTaskExecServiceClient
from src.acu_ua_server import AcuUaServer
from src.cdc_ua_server import CdcUaServer
from src.vehicle_mode_client import VehicleModeServiceClient


DEFAULT_PORT = 7000
MESSAGE_LENGTH_BYTES = 4
BUFFER_SIZE = 1024 * 1024


class FotaSim:
    def __init__(self, bgm_master=True, cdc_ua=False, tcam=True, acu=False, other=False):
        logger.info('Start partner operator...')
        self.bgm_sim_operator = SOAOperator("bgm_sim_op", DEFAULT_PORT) if bgm_master else None
        self.cdc_sim_operator = SOAOperator("cdc_sim_op",DEFAULT_PORT+1000) if cdc_ua else None
        self.tcam_sim_operator = SOAOperator("tcam_sim_op", DEFAULT_PORT + 2000) if tcam else None
        self.acu_sim_operator = SOAOperator("acu_sim_op", DEFAULT_PORT + 3000) if acu else None
        self.other_sim_operator = SOAOperator("other_sim_op", DEFAULT_PORT + 4000) if other else None
        # self.diag_client = DoIP_Client('192.168.43.117', 0x0E80, '192.168.43.160', 0x0E02)  # currently hard coding
        self.start_operators()
        time.sleep(2)
        self.start_skeleton_and_proxy()
        self.initiate_server_clients_controller()
        # self.init_doip_client()

    # def init_doip_client(self):
    #     config = dict(udsoncan.configs.default_client_config)
    #     self.diag_client._configs = config
    #     self.diag_client.connect()

    def initiate_server_clients_controller(self):
        logger.info("start init server client")
        # logger.info("========================{}==============================".format(self.bgm_sim_operator_cnn_info))
        self.fota_master_server = BgmFotaMasterServer(tuple(self.bgm_sim_operator_cnn_info["FotaMasterService_server"])) if self.bgm_sim_operator else None
        self.bgm_v2t_routing_forwarder_service = BgmV2TRoutingForwarderService(
            tuple(self.bgm_sim_operator_cnn_info["V2TRoutingForwarder_server"])) if self.bgm_sim_operator else None
        self.bgm_task_exec_forwarder_service = BgmVTaskExecForwarderService(
            tuple(self.bgm_sim_operator_cnn_info["TaskExecForwarder_server"])) if self.bgm_sim_operator else None
        # self.v2trouting_client = BgmV2TRoutingClient(tuple(self.bgm_sim_operator_cnn_info["V2TRoutingService_client"])) if self.bgm_sim_operator else None
        # self.hv_service_server = BgmHvServer(tuple(self.bgm_sim_operator_cnn_info["HighVoltageService_server"]))
        # self.fota_ua_server = CdcUaServer(tuple(self.cdc_sim_operator_cnn_info["UpdateAgentService_server"])) if self.cdc_sim_operator else None
        # time.sleep(5)
        # self.fota_ua_client = BgmFotaUaClient(tuple(self.bgm_sim_operator_cnn_info["UpdateAgentService_client"]))
        # time.sleep(2)
        logger.info("========================{}==============================".format(self.cdc_sim_operator_cnn_info))
        self.fota_master_client = CdcFotaMasterClient(tuple(self.cdc_sim_operator_cnn_info["FotaMasterService_client"])) if self.cdc_sim_operator else None
        self.cdc_ua_server = CdcUaServer(
            tuple(self.cdc_sim_operator_cnn_info["UpdateAgentService_server"])) if self.cdc_sim_operator else None
        # time.sleep(2)
        # self.hv_service_client = CdcHvClient(tuple(self.cdc_sim_operator_cnn_info["HighVoltageService_client"])) if self.cdc_sim_operator else None
        # logger.info("========================{}==============================".format(self.tcam_sim_operator_cnn_info))
        self.v2trouting_server = TcamV2TRoutingService(
            tuple(self.tcam_sim_operator_cnn_info["V2TRoutingService_server"])) if self.tcam_sim_operator else None
        self.tcam_task_exec_service = TcamTaskExecServiceService(
            tuple(self.tcam_sim_operator_cnn_info["TaskExecService_server"])) if self.tcam_sim_operator else None
        self.tcam_v2t_routing_forwarder_client = TcamV2TRoutingForwarderClient(
            tuple(self.tcam_sim_operator_cnn_info["V2TRoutingForwarder_client"])) if self.tcam_sim_operator else None
        self.tcam_task_exec_forwarder_client = TcamTaskExecForwarderClient(
            tuple(self.tcam_sim_operator_cnn_info["TaskExecForwarder_client"])) if self.tcam_sim_operator else None

        # logger.info("========================{}==============================".format(self.acu_sim_operator_cnn_info))
        # self.v2trouting_client = BgmV2TRoutingClient(
        #     tuple(self.acu_sim_operator_cnn_info["V2TRoutingService_client"])) if self.acu_sim_operator else None
        # self.bgm_task_exec_client = BgmTaskExecServiceClient(
        #     tuple(self.acu_sim_operator_cnn_info["TaskExecService_client"])) if self.acu_sim_operator else None
        self.acu_ua_server = AcuUaServer(
            tuple(self.acu_sim_operator_cnn_info["UpdateAgentService_server"])) if self.acu_sim_operator else None
        self.other_server = VehicleModeServiceClient(
            tuple(self.other_sim_operator_cnn_info["VehicleModeService_client"])) if self.other_sim_operator else None

    def start_skeleton_and_proxy(self):
        logger.info("start skeleton & proxy...")
        if self.bgm_sim_operator:
            self.bgm_sim_operator_cfg = {"V2TRoutingForwarder": {"role": "server", "name": "V2TRoutingForwarder"},
                                         "FotaMasterService": {"role": "server", "name": "FotaMasterService"},
                                         "TaskExecForwarder": {"role": "server", "name": "TaskExecForwarder"}
                                         }

            #  "HighVoltageService": "server"} } # start skeleton first
            self.bgm_sim_operator_cnn_info = self.start_and_get_socket_info(self.bgm_sim_operator_cfg, self.bgm_sim_operator)
        time.sleep(2)
        if self.cdc_sim_operator:
            # self.cdc_sim_operator_cfg = {"UpdateAgentService": "server", "FotaMasterService": "client", "HighVoltageService": "client"}
            self.cdc_sim_operator_cfg = {"FotaMasterService": {"role": "client", "name": "FotaMasterService"},
                                         "UpdateAgentService": {"role": "server", "name": "CDC_UA_Service"}
                                         }
            self.cdc_sim_operator_cnn_info = self.start_and_get_socket_info(self.cdc_sim_operator_cfg, self.cdc_sim_operator)
        # time.sleep(2)
        # self.bgm_sim_operator_cfg = {"FotaMasterService": "server", "HighVoltageService": "server", "UpdateAgentService": "client"}  # start skeleton & proxy
        # self.bgm_sim_operator_cnn_info = self.start_and_get_socket_info(self.bgm_sim_operator_cfg, self.bgm_sim_operator)
        # logger.info(self.bgm_sim_operator_cnn_info)
        time.sleep(2)
        if self.tcam_sim_operator:
            self.tcam_sim_operator_cfg = {"V2TRoutingService": {"role": "server", "name": "V2TRoutingService"},
                                          "TaskExecService": {"role": "server", "name": "TaskExecEngineService"},
                                          "V2TRoutingForwarder": {"role": "client", "name": "V2TOTAFotaForwarder"},
                                          "TaskExecForwarder": {"role": "client", "name": "TaskExecOTAFotaForwarder"}
                                          }
            self.tcam_sim_operator_cnn_info = self.start_and_get_socket_info(self.tcam_sim_operator_cfg, self.tcam_sim_operator)
        time.sleep(2)

        if self.acu_sim_operator:
            # self.acu_sim_operator_cfg = {"V2TRoutingService": {"role": "client", "name": "V2TRoutingService"},
            #                              "TaskExecService": {"role": "client", "name": "TaskExecService"}
            #                              }
            self.acu_sim_operator_cfg = {"UpdateAgentService": {"role": "server", "name": "ACU_UA_Service"}
                                         }
            self.acu_sim_operator_cnn_info = self.start_and_get_socket_info(self.acu_sim_operator_cfg, self.acu_sim_operator)
        time.sleep(2)
        
        if self.other_sim_operator:
            self.other_sim_operator_cfg = {"VehicleModeService": {"role": "client", "name": "VehicleModeService"}}
            self.other_sim_operator_cnn_info = self.start_and_get_socket_info(self.other_sim_operator_cfg, self.other_sim_operator)
        time.sleep(2)



    def start_operators(self):
        if self.bgm_sim_operator:
            self.bgm_sim_operator.run_operator()
        if self.cdc_sim_operator:
            self.cdc_sim_operator.run_operator()
        if self.tcam_sim_operator:
            self.tcam_sim_operator.run_operator()
        if self.acu_sim_operator:
            self.acu_sim_operator.run_operator()
        if self.other_sim_operator:
            self.other_sim_operator.run_operator()
    
    def start_and_get_socket_info(self, cfg, operator_obj):
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect(('127.0.0.1', operator_obj.operator_port))
        req = {
            "action": "request",
            "function": "get_current_service_list",
            "args": None
        }
        send_data_to(tcp_socket, req)
        # tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
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
        # tcp_socket.sendall(bytes(json.dumps(req), encoding='utf-8'))
        recv_data = recv_data_from(tcp_socket)
        resp = json.loads(recv_data.decode("utf-8"))
        result = json.loads(resp['result'])
        logger.info(result)
        tcp_socket.close()
        # connect_info = tuple(result[f'{service}_{role}'])
        return result

    def kill_operators(self):
        # self.reset_operator(self.bgm_sim_operator)
        if self.bgm_sim_operator:
            self.bgm_sim_operator.stop_operator()
        if self.cdc_sim_operator:
            # self.reset_operator(self.cdc_sim_operator)
            self.cdc_sim_operator.stop_operator()
        if self.tcam_sim_operator:
            self.tcam_sim_operator.stop_operator()
        if self.acu_sim_operator:
            self.acu_sim_operator.stop_operator()

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
    fota_sim = FotaSim(True)
    # logger.info('Initiate fota master server...')
    # bgm_fota_master = BgmFotaMasterServer()
    # bgm_fota_master.start()
    # logger.info('Initiate fota ua client')
    # bgm_ua_client = BgmFotaUaClient()
    # time.sleep(8)

