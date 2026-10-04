#!/usr/bin/python3

import threading
import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class AccountServer:
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.accountsts = {
            "uid": 0x0102030405060708,
            "token": __import__("os").environ.get('XAT_CREDENTIAL_ECU__SOA_PARTNER_SRC_ACCOUNT_SERVER_PY_TOKEN', "")
            }
        self.loginsts = 1
        time.sleep(5)
        self.start()

    def account_event_send(self):
        event = {
        "action":"event",
        "function": "UpdateNotifyAccountStsEvent",
        "args": json.dumps({"logInSts": self.loginsts, "sts": self.accountsts})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"AccountServer:NotifyAccountSts send periodic status failure with broken pipe: {str(e)}")

    def account_response(self):
        while True:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                logger.info("Received request: {}".format(req))
                if req["function"] == "getAccountSts":
                    logger.info("getAccountSts: {}".format(req))
                    resp = {
                        "action": "response",
                        "function": "getAccountSts",
                        "result": json.dumps({"out": self.accountsts})
                    }
                    logger.info("Send response: {}".format(json.dumps(resp)))
                    self.tcp_socket.sendall(bytes(json.dumps(resp), encoding='utf-8'))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/account_server.py")
                continue

    def start_account_response(self):
        self.account_response_thread = threading.Thread(name="Account_Response", target=self.account_response, )
        self.account_response_thread.start()

    def stop_account_response(self):
        self.account_response_thread.join()

    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        # pass
        try:
            self.tcp_socket.connect(self.connect_info)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/account_server.py")
            logger.error(str(e))
        logger.info("Satrt to send response of Account service")
    
    def start_response(self):
        self.start_account_response()

    def stop_response(self):
        self.stop_account_response()
        logger.info("Stop Account service")