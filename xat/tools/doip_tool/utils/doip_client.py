# -*- coding: utf-8 -*-
"""
@File        : doip_client.py
@Author      : yu.zhang0101 & jiankai.zhang
@Time        : 2022/04/13 4:01 PM
@Description : doip basic function

"""

import udsoncan.configs
from doipclient import DoIPClient
from doipclient.connectors import DoIPClientUDSConnector
from udsoncan.client import Client
import logging


class DOIPClient:

    def __init__(self, logger=None):
        self.logger = logger if logger else logging.getLogger("DOIPClient")
        self._doip_client = None
        self._client = None
        self._configs = dict(udsoncan.configs.default_client_config)

    def connect(self, json_config=None, reconnect_tcp=False):
        self._doip_client = DoIPClient(ecu_ip_address=json_config["ecu_ip"],
                                       ecu_logical_address=json_config["ecu_logical_address"],
                                       client_ip_address=json_config["tester_ip"],
                                       client_logical_address=json_config["tester_logical_address"],
                                       reconnect_tcp=reconnect_tcp,
                                       logger=self.logger)
        _connect = DoIPClientUDSConnector(self._doip_client, logger=self.logger)
        try:
            self._client = Client(_connect, request_timeout=2, config=self._configs, logger=self.logger)
            self._client.suppress_positive_response.enabled = json_config["suppress_positive_response"]
            self.logger.info("DoIP connection has established.")
            return self._client
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/doip_tool/utils/doip_client.py")
            self.logger.info('DoIP connection has NOT established.')
            self.logger.info(f'An exception occurred when connecting to {json_config["ecu_ip"]}: ', e)

    def close(self):
        self._doip_client.close()
