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
from src.bgm_hv_service_server import HighVoltageServiceServer
from src.lowvoltageservice_server import LowVoltageServiceServer
from src.chassis_serice_server import ChassisServiceServer
from src.vehicle_mode_service_server import VehicleModeServiceServer
from src.bgm_mcu_inter_comm_server import BgmMcuInterCommService
from src.doorservice_server import DoorServiceServer
from src.windowservice_server import WindowServiceServer
from src.tcam_netstat_service import TcamNetStatService


DEFAULT_PORT = 6789
MESSAGE_LENGTH_BYTES = 4
BUFFER_SIZE = 1024 * 1024


class S2sSim:
    def __init__(self, proxy_init=False) -> None:
        logger.info('Start partner operator...')
        self.s2s_sim_operator = SOAOperator("s2s_sim_op", DEFAULT_PORT)
        self.proxy_sim_operator = SOAOperator("proxy_sim_op",DEFAULT_PORT+1000) if proxy_init else None
        self.start_operators()
        time.sleep(2)
        self.start_skeleton_and_proxy()
        self.initiate_server_clients_controller()


    def initiate_server_clients_controller(self):
        logger.info("start init server client")
        logger.info(self.s2s_sim_operator_cnn_info)
        self.hv_voltage_service_server = HighVoltageServiceServer(tuple(self.s2s_sim_operator_cnn_info["HighVoltageService_server"]))
        self.lv_management_service_server = LowVoltageServiceServer(tuple(self.s2s_sim_operator_cnn_info["LowVoltageService_server"]))
        self.chassis_service_server = ChassisServiceServer(tuple(self.s2s_sim_operator_cnn_info["ChassisService_server"]))
        self.vehicle_mode_service_server = VehicleModeServiceServer(tuple(self.s2s_sim_operator_cnn_info["VehicleModeService_server"]))
        self.bgm_mcu_inter_comm_server = BgmMcuInterCommService(tuple(self.s2s_sim_operator_cnn_info["InterCommService_server"]))
        self.doorservice_server = DoorServiceServer(tuple(self.s2s_sim_operator_cnn_info["DoorService_server"]))
        self.windowservice_server = WindowServiceServer(tuple(self.s2s_sim_operator_cnn_info["WindowService_server"]))
        # self.tcam_netstat_service = TcamNetStatService(tuple(self.s2s_sim_operator_cnn_info["NetStatService_server"]))



    def start_skeleton_and_proxy(self):
        logger.info("start skeleton & proxy...")
        self.s2s_sim_operator_cfg = {"ChassisService": {"role": "server", "name": "ChassisService"},
                                     "HighVoltageService": {"role": "server", "name": "HighVoltageService"},
                                     "LowVoltageService": {"role": "server", "name": "LowVoltageService"},
                                     "VehicleModeService": {"role": "server", "name": "VehicleModeService"},
                                     "InterCommService": {"role": "server", "name": "InterCommService"},
                                     "DoorService": {"role": "server", "name": "DoorService"},
                                     "WindowService": {"role": "server", "name": "WindowService"}
                                     }
        # self.s2s_sim_operator_cfg = {"ChassisService": {"role": "server", "name": "ChassisService"},
        #                              "HighVoltageService": {"role": "server", "name": "HighVoltageService"},
        #                              "LowVoltageService": {"role": "server", "name": "LowVoltageService"},
        #                              "VehicleModeService": {"role": "server", "name": "VehicleModeService"},
        #                              "InterCommService": {"role": "server", "name": "InterCommService"},
        #                              "NetStatService": {"role": "server", "name": "NetStatService"}}
        # self.s2s_sim_operator_cfg = {"HighVoltageService": {"role": "server", "name": "HighVoltageService"}}
        self.s2s_sim_operator_cnn_info = self.start_and_get_socket_info(self.s2s_sim_operator_cfg, self.s2s_sim_operator)
        time.sleep(5)
        if self.proxy_sim_operator:
            self.proxy_sim_operator_cfg = {"ChassisService": {"role": "client", "name": "ChassisService"}, 
                                     "HighVoltageService": {"role": "client", "name": "HighVoltageService"}, 
                                     "LowVoltageService": {"role": "client", "name": "LowVoltageService"}}
            self.proxy_sim_operator_cnn_info = self.start_and_get_socket_info(self.proxy_sim_operator_cfg, self.proxy_sim_operator)
        time.sleep(5)


    def start_operators(self):
        if self.s2s_sim_operator:
            self.s2s_sim_operator.run_operator()
        if self.proxy_sim_operator:
            self.proxy_sim_operator.run_operator()
    
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
        self.bgm_sim_operator.stop_operator()
        if self.cdc_sim_operator:
            # self.reset_operator(self.cdc_sim_operator)
            self.cdc_sim_operator.stop_operator()

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

    def test_fota_s2ssim(self):
        fota_sim = S2sSim(False)
        fota_sim.hv_voltage_service_server.start()
        fota_sim.lv_management_service_server.start()
        fota_sim.chassis_service_server.start()
        fota_sim.vehicle_mode_service_server.start()
        fota_sim.bgm_mcu_inter_comm_server.start()
        fota_sim.doorservice_server.start()
        fota_sim.windowservice_server.start()
        # fota_sim.tcam_netstat_service.start()

        # fota_sim.vehicle_mode_service_server.carmode = 2   #  factory

        # time.sleep(5)
        fota_sim.vehicle_mode_service_server.event_args_dict = {"UpdateNotifyUsageModEvent": {"mode": 2}}  # Convience
        # fota_sim.vehicle_mode_service_server.event_args_dict = {"UpdateNotifyUsageModEvent": {"mode": 13}}  # DRIVING

        exit_flag = None
        while not exit_flag:
            if fota_sim.bgm_mcu_inter_comm_server.fota_status == 2 or fota_sim.bgm_mcu_inter_comm_server.fota_status is None:
                fota_sim.hv_voltage_service_server.hv_flag = True
            elif fota_sim.bgm_mcu_inter_comm_server.fota_status > 2:
            # elif fota_sim.bgm_mcu_inter_comm_server.fota_status > 5:
                fota_sim.hv_voltage_service_server.hv_flag = False
                exit_flag = True
            time.sleep(0.1)

if __name__ == "__main__":
    fota_s2ssim = S2sSim()
    fota_s2ssim.test_fota_s2ssim()
