# -*- coding: utf-8 -*-
"""
@File        : parse_tb_config.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021-04-28 09:20
@Description : Parase test_network.yaml configuration file
"""


import yaml


class ParseTBConfig(object):
    def __init__(self, tbconfig):
        self.tbconfig = tbconfig
        self.yaml_content = self.get_yaml()

    def get_yaml(self):
        with open(self.tbconfig, 'rb') as f:
            yaml_content = __import__("xat_ecu.resources", fromlist=["resolve_environment"]).resolve_environment(list(yaml.safe_load_all(f)))
        return yaml_content[0]

    def get_usbrelay(self):
        return self.yaml_content.get("usbrelay")

    def get_bus(self):
        return self.yaml_content.get("bus")

    def get_eth_obd(self):
        bus = self.get_bus()
        eth_obd = bus.get("eth_obd")
        return eth_obd


