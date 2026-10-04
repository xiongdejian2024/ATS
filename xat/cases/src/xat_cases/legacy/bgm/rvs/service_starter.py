
import sys
import os
import socket
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.soa_partner.src.socket_recv import *
from xat_ecu.legacy.soa_partner.src.wti_server import WTI
from xat_ecu.legacy.soa_partner.src.wti_autodrive_server import WTI_Autodrive
from xat_ecu.legacy.soa_partner.src.avp_server import AVPServer
from xat_ecu.legacy.soa_partner.src.rpaapa_server import RPAAPAServer
from xat_ecu.legacy.soa_partner.src.central_lock_client import CentralLockClient
from xat_ecu.legacy.soa_partner.src.tyre_server import TyreServer
from xat_ecu.legacy.soa_partner.src.account_server import AccountServer
from xat_ecu.legacy.soa_partner.src.navi_server import NaviServer
from xat_ecu.legacy.soa_partner.src.remotectrl_server import RemoteCtrlServer
from xat_ecu.legacy.soa_partner.src.key_server import KeyServer
from xat_ecu.legacy.soa_partner.src.rtc_server import RtcAlarmServer
from xat_ecu.legacy.soa_partner.src.high_voltage_client import HighVoltageClient
from xat_ecu.legacy.soa_partner.src.sentrymode_server import SentryModeServer
from xat_ecu.legacy.soa_partner.src.cdc_wtiservice_cross_domain import CDCWTI
from xat_ecu.legacy.soa_partner.src.Operator import SOAOperator
import json

DEFAULT_PORT = 6789
MESSAGE_LENGTH_BYTES = 4
BUFFER_SIZE = 1024 * 1024

class Service_Starter:
    def __init__(self) -> None:
        logger.info('Start partner operator...')
        self.wti_operator = SOAOperator("wti_op", DEFAULT_PORT)
        logger.info("Here to start server operator")
        self.list_wti_telltalenode = [{"name": "TelltaleChargingGunConnected", "state": "1"}]
        self.list_wti_warningmsgnode = [{"name": "MsgThermalOutOfControl", "info": "1"}]
        self.list_wti_autodrive_telltalenode = [{"name": "TelltaleAEBandFCWYellow", "state": "1"}]
        self.list_wti_autodrive_warningmsgnode = [{"name": "MsgAPAWorkingSts", "info": "41"}]
        self.list_wti_cdc_warningmsgnode = [{"id": "CDCWTIMsgAvasFunctionOn", "data": "1"}]
        self.start_server_operator()
        time.sleep(1)
        self.start_server_skeleton_and_proxy()
        time.sleep(1)
        self.initiate_server_controller()
        time.sleep(1)


    def initiate_server_controller(self):
        logger.info("start init server")
        self.wti_server = WTI(tuple(self.wti_operator_cnn_info["WTIService_server"]), self.list_wti_warningmsgnode,\
            self.list_wti_telltalenode)
        self.wti_autodrive_server = WTI_Autodrive(tuple(self.wti_operator_cnn_info["WTIAutoDriveService_server"]),\
            self.list_wti_autodrive_telltalenode, self.list_wti_autodrive_warningmsgnode)
        self.avp_server = AVPServer(tuple(self.wti_operator_cnn_info["AVPService_server"]))
        self.rpaapa_server = RPAAPAServer(tuple(self.wti_operator_cnn_info["RPAAPAService_server"]))
        self.cental_lock_client = CentralLockClient(tuple(self.wti_operator_cnn_info["CentralLockService_client"]))
        self.tyre_server = TyreServer(tuple(self.wti_operator_cnn_info["TyreService_server"]))
        self.account_server = AccountServer(tuple(self.wti_operator_cnn_info["AccountService_server"]))
        self.rtc_server = RtcAlarmServer(tuple(self.wti_operator_cnn_info["RtcAlarmService_server"]))
        self.highvoltage_client = HighVoltageClient(tuple(self.wti_operator_cnn_info["HighVoltageService_client"]))
        self.navi_server = NaviServer(tuple(self.wti_operator_cnn_info["NaviService_server"]))
        self.remotectrl_server = RemoteCtrlServer(tuple(self.wti_operator_cnn_info["RemoteCtrlService_server"]))
        self.key_server = KeyServer(tuple(self.wti_operator_cnn_info["KeyService_server"]))
        self.sentry_server = SentryModeServer(tuple(self.wti_operator_cnn_info["SentryModeService_server"]))
        self.wti_cdc_server = CDCWTI(tuple(self.wti_operator_cnn_info["cdc_wtiservice_crossdomain_server"]),\
            self.list_wti_cdc_warningmsgnode)
        logger.info("Init server successfully!")
    
    def start_server_skeleton_and_proxy(self):
        logger.info("start server skeleton & proxy...")
        self.wti_operator_cfg = {"WTIService": {"role": "server", "name": "WTIService"},
                                 "WTIAutoDriveService": {"role": "server","name": "WTIAutoDriveService"},
                                 "AVPService": {"role": "server","name": "AVPService"},
                                 "RPAAPAService": {"role": "server","name": "RPAAPAService"},
                                 "CentralLockService": {"role": "client", "name": "CentralLockService"},
                                 "TyreService": {"role": "server", "name": "TyreService"},
                                 "RtcAlarmService": {"role": "server", "name": "RtcAlarmService"},
                                 "HighVoltageService": {"role": "client", "name": "HighVoltageService"},
                                 "AccountService": {"role": "server", "name": "AccountService"},
                                 "NaviService": {"role": "server", "name": "NaviService"},
                                 "RemoteCtrlService": {"role": "server", "name": "RemoteCtrlService"},
                                 "KeyService": {"role": "server", "name": "KeyService"},
                                 "SentryModeService": {"role": "server", "name": "SentryModeService"},
                                 "cdc_wtiservice_crossdomain": {"role": "server", "name": "cdc_wtiservice_crossdomain"}
                                 }
        self.wti_operator_cnn_info = self.start_and_get_socket_info(self.wti_operator_cfg,
                                                                        self.wti_operator)
        logger.info("start server skeleton & proxy... successfully!")

    def start_server_operator(self):
        logger.info("Start server operator-----------------------")
        if self.wti_operator:
            self.wti_operator.run_operator()

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
        self.wti_operator.stop_operator()

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