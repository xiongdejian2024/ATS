#!/usr/bin/python3

from collections.abc import Callable, Iterable, Mapping
import sys
import os
from typing import Any
sys.path.append(os.getcwd())
import socket
from xat_ecu.legacy.soa_partner.src.socket_recv import *
from xat_ecu.legacy.soa_partner.src.high_voltage_server import HighVoltageServer
from xat_ecu.legacy.soa_partner.src.vehicle_mode_service_server import VehicleModeServiceServer
from xat_ecu.legacy.soa_partner.src.chassis_serice_server import ChassisServiceServer
from xat_ecu.legacy.soa_partner.src.doorservice_server import DoorServiceServer
from xat_ecu.legacy.soa_partner.src.seatservice_server import SeatServiceServer
from xat_ecu.legacy.soa_partner.src.fota_master_server import FotaMasterServer
from xat_ecu.legacy.soa_partner.src.vehicle_setstatus_server import VehicleSetStatusServer
from xat_ecu.legacy.soa_partner.src.tailgate_server import TailGateServer
from xat_ecu.legacy.soa_partner.src.central_lock_server import CentralLockServer
from xat_ecu.legacy.soa_partner.src.steerwheel_server import SteerWheelServer
from xat_ecu.legacy.soa_partner.src.climate_control_server import ClimateControlServer
from xat_ecu.legacy.soa_partner.src.shield_window_server import ShieldWindowServer
from xat_ecu.legacy.soa_partner.src.outer_rearview_server import OuterRearviewServer
from xat_ecu.legacy.soa_partner.src.Operator import SOAOperator
from threading import Thread


DEFAULT_PORT = 6789
MESSAGE_LENGTH_BYTES = 4
BUFFER_SIZE = 1024 * 1024

class RVCHelper:
    def __init__(self) -> None:
        logger.info('Start partner operator...')
        self.rvc_operator = SOAOperator("rvc_op", DEFAULT_PORT)
        logger.info("Here to start server operator")
        self.start_server_operator()
        time.sleep(2)
        self.start_server_skeleton_and_proxy()
        time.sleep(5)
        self.initiate_server_controller()
        time.sleep(5)

    def initiate_server_controller(self):
        logger.info("Init server")
        self.high_voltage_server = HighVoltageServer(tuple(self.rvc_operator_cnn_info["HighVoltageService_server"]))
        self.vehicle_mode_server = VehicleModeServiceServer(tuple(self.rvc_operator_cnn_info["VehicleModeService_server"]))
        self.door_server = DoorServiceServer(tuple(self.rvc_operator_cnn_info["DoorService_server"]))
        self.seat_server = SeatServiceServer(tuple(self.rvc_operator_cnn_info["SeatService_server"]))
        self.fota_master_server = FotaMasterServer(tuple(self.rvc_operator_cnn_info["FotaMasterService_server"]))
        self.vehicle_setstatus_server = VehicleSetStatusServer(tuple(self.rvc_operator_cnn_info["VehicleSetStatusService_server"]))
        self.chassis_server = ChassisServiceServer(tuple(self.rvc_operator_cnn_info["ChassisService_server"]))
        self.tailgate_server = TailGateServer(tuple(self.rvc_operator_cnn_info["TailGateService_server"]))
        self.central_lock_server = CentralLockServer(tuple(self.rvc_operator_cnn_info["CentralLockService_server"]))
        self.steer_wheel_server = SteerWheelServer(tuple(self.rvc_operator_cnn_info["SteerWheelService_server"]))
        self.climate_control_server = ClimateControlServer(tuple(self.rvc_operator_cnn_info["ClimateControlService_server"]))
        self.shield_window_server =  ShieldWindowServer(tuple(self.rvc_operator_cnn_info["ShieldWindowService_server"]))
        self.outer_rearview_server = OuterRearviewServer(tuple(self.rvc_operator_cnn_info["OuterRearViewService_server"]))
        logger.info("Init server successfully!")

    def start_server_skeleton_and_proxy(self):
        logger.info("Start server")
        self.rvc_operator_cfg = {"HighVoltageService": {"role": "server","name": "HighVoltageService"},
                                          "VehicleModeService": {"role": "server","name": "VehicleModeService"},
                                          "DoorService": {"role": "server", "name": "DoorService"},
                                          "SeatService": {"role": "server", "name": "SeatService"},
                                          "FotaMasterService": {"role": "server", "name": "FotaMasterService"},
                                          "VehicleSetStatusService": {"role": "server", "name": "VehicleSetStatusService"},
                                          "ChassisService": {"role": "server", "name": "ChassisService"},
                                          "TailGateService": {"role": "server", "name": "TailGateService"},
                                          "CentralLockService": {"role": "server", "name": "CentralLockService"},
                                          "SteerWheelService": {"role": "server", "name": "SteerWheelService"},
                                          "ClimateControlService": {"role": "server", "name": "ClimateControlService"},
                                          "ShieldWindowService": {"role": "server", "name": "ShieldWindowService"},
                                          "OuterRearViewService": {"role": "server", "name": "OuterRearViewService"}
                                          }
        self.rvc_operator_cnn_info = self.start_and_get_socket_info(self.rvc_operator_cfg,
                                                                        self.rvc_operator)
        logger.info("start server skeleton & proxy... successfully!")

    def start_server_operator(self):
        logger.info("Start server operator-----------------------")
        if self.rvc_operator:
            self.rvc_operator.run_operator()

    def start_and_get_socket_info(self, cfg, operator_obj):
        logger.info("start_and_get_socket_info-----------------------")
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
        tcp_socket.close()
        # connect_info = tuple(result[f'{service}_{role}'])
        logger.info("Get the socket info: {}".format(result))
        return result

    def kill_operators(self):
        logger.info("Here to stop operator!!")
        self.rvc_operator.stop_operator()

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

    def stop_all(self):
        self.kill_operators()

class CheckThreading(Thread):
    def __init__(self, func, args=()):
        super(CheckThreading,self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        Thread.join(self)
        logger.info("Get the result: {0}".format(self.result))
        try:
            return self.result
        except Exception:
            return None