# /*
#  * @Author: lei.song
#  * @Date: 2022-12-05 14:26:52 
#  * @Last Modified by:   lei.song
#  * @Last Modified time: 2022-12-05 14:26:52 
#  */


# -*- coding: utf-8 -*-

import os
from signal import signal
import sys
import time
import threading
# from ecu_simulator.tsp.grpc_client import GrpcClient
from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
import pytest
import allure
import json
from xat_cases.legacy.bgm.rvs.service_starter import Service_Starter
# from rvs.service_starter import Service_Starter

with open('./rvs/data/wti.json','r',encoding='utf8') as f_wti:
    wti_data = json.load(f_wti)
with open('./rvs/data/wtiautodrive.json','r',encoding='utf8') as f_wtiautodrive:
    wti_autodrive_data = json.load(f_wtiautodrive)
with open('./rvs/data/wticdc.json','r',encoding='utf8') as f_wti:
    wti_cdc_data = json.load(f_wti)
wti_telltalenode = wti_data["WTI"]["TelltaleNode"]
wti_warningmsgnode = wti_data["WTI"]["WarningMsgNode"]
wti_autodrive_telltalenode = wti_autodrive_data["WTI"]["TelltaleNode"]
wti_autodrive_warningmsgnode = wti_autodrive_data["WTI"]["WarningMsgNode"]
wti_cdc_warningmsgnode = wti_cdc_data["WTI"]["WarningMsgNode"]
list_wti_telltalenode = []
for wti_t in wti_telltalenode.items():
    list_wti_telltalenode.append(wti_t)
list_wti_warningmsgnode = []
for wti_w in wti_warningmsgnode.items():
    list_wti_warningmsgnode.append(wti_w)
list_wti_autodrive_telltalenode = []
for wti_auto_t in wti_autodrive_telltalenode.items():
    list_wti_autodrive_telltalenode.append(wti_auto_t)
list_wti_autodrive_warningmsgnode = []
for wti_auto_w in wti_autodrive_warningmsgnode.items():
    list_wti_autodrive_warningmsgnode.append(wti_auto_w)
list_wti_cdc_warningmsgnode = []
for wti_cdc_w in wti_cdc_warningmsgnode.items():
    list_wti_cdc_warningmsgnode.append(wti_cdc_w)

class TestWTI(TestBase):
    def before_class(self, bgm):
        super().before_class(self, bgm)
        self.vid = self.tb_config["vid"]
        # self.grpc_message = GrpcClient(self.vid)
        self.wti_op = Service_Starter()
        self.wti_server = self.wti_op.wti_server
        self.wti_auto_server = self.wti_op.wti_autodrive_server
        self.wti_cdc_server = self.wti_op.wti_cdc_server

    def after_class(self, bgm):
        super().after_class
        logger.info("Teardown_class execute finished!")

    def before_each_func(self, bgm):
        super().before_each_func
        pass

    def after_each_func(self, bgm):
        super().after_each_func
        pass
    
    @pytest.mark.normal
    @pytest.mark.parametrize("name, msg", list_wti_telltalenode)
    def skip_test_wti_telltalenode(self, name, msg):
        logger.info("测试wti service telltalenode：{0}, {1}".format(name, msg))
        telltalemnode = {
            "name": "",
            "state": ""
        }
        for key, value in msg.items():
            print("key, value: ", key, value)
            telltalemnode["name"] = key
            for val in value:
                print("val: ", val)
                telltalemnode["state"] = val
                print("telltalemnode: ", telltalemnode)
                self.wti_server.telltalelist = [telltalemnode]
                self.wti_server.telltalelist_event_send()
                time.sleep(1)
                # rcv_data = self.grpc_message.get_report_message_from_http(17001)
                # logger.info("Get wti info: {0}".format(rcv_data))
            

    @pytest.mark.normal
    @pytest.mark.parametrize("name, msg", list_wti_warningmsgnode)
    def skip_test_wti_warningmsgnode(self, name, msg):
        logger.info("测试 wti service warningmsgnode: {0}, {1}".format(name, msg))
        warningmsgnode = {
            "name": "",
            "info": ""
        }
        for key1, value1 in msg.items():
            if "info" in value1.keys():
                warningmsgnode_dict = value1["info"]
            else:
                warningmsgnode_dict = value1
            for key2, value2 in warningmsgnode_dict.items():
                warningmsgnode["name"] = key1
                warningmsgnode["info"] = value2
                logger.info(warningmsgnode)
                self.wti_server.warningmsglist = [warningmsgnode]
                self.wti_server.warningmsglist_event_send()
                time.sleep(1)
                # rcv_data = self.grpc_message.get_report_message_from_http(10701)
                # logger.info("Get wti info: {0}".format(rcv_data))

    @pytest.mark.auto
    @pytest.mark.parametrize("name, msg", list_wti_autodrive_telltalenode)
    def skip_test_wti_autodrive_telltalenode(self, name, msg):
        logger.info("测试wti autodrive service telltalenode：{0}, {1}".format(name, msg))
        telltalemnode = {
            "name": "",
            "state": ""
        }
        for key, value in msg.items():
            telltalemnode["name"] = key
            for val in value:
                telltalemnode["state"] = val
                logger.info(telltalemnode)
                self.wti_server.telltalelist = [telltalemnode]
                self.wti_server.telltalelist_event_send()
                time.sleep(1)
                # rcv_data = self.grpc_message.get_report_message_from_http(17002)
                # logger.info("Get wti info: {0}".format(rcv_data))

    @pytest.mark.auto
    @pytest.mark.parametrize("name, msg", list_wti_autodrive_warningmsgnode)
    def skip_test_wti_autodrive_warningmsgnode(self, name, msg):
        logger.info("测试测试wti autodrive service warningmsgnode: {0}, {1}".format(name, msg))
        warningmsgnode = {
            "name": "",
            "info": ""
        }
        for key1, value1 in msg.items():
            print(key1, value1)
            if "info" in value1.keys():
                warningmsgnode_dict = value1["info"]
            else:
                warningmsgnode_dict = value1
            for key2, value2 in warningmsgnode_dict.items():
                warningmsgnode["name"] = key1
                warningmsgnode["info"] = value2
                logger.info(warningmsgnode)
                self.wti_server.warningmsglist = [warningmsgnode]
                self.wti_server.warningmsglist_event_send()
                time.sleep(1)
                # rcv_data = self.grpc_message.get_report_message_from_http(10702)
                # logger.info("Get wti info: {0}".format(rcv_data))

    @pytest.mark.cdc
    @pytest.mark.parametrize("name, msg", list_wti_cdc_warningmsgnode)
    def skip_test_wti_cdc_warningmsgnode(self, name, msg):
        logger.info("测试测试wti cdc service warningmsgnode: {0}, {1}".format(name, msg))
        warningmsgnode = {
            "id": "",
            "data": ""
        }
        for key1, value1 in msg.items():
            print(key1, value1)
            if "info" in value1.keys():
                warningmsgnode_dict = value1["info"]
            else:
                warningmsgnode_dict = value1
            for key2, value2 in warningmsgnode_dict.items():
                warningmsgnode["id"] = key1
                warningmsgnode["data"] = value2
                self.wti_cdc_server.notifyvalue = [warningmsgnode]
                self.wti_cdc_server.notyfyvalue_event_send()
                time.sleep(1)
                # rcv_data = self.grpc_message.get_report_message_from_http(10702)
                # logger.info("Get wti info: {0}".format(rcv_data))