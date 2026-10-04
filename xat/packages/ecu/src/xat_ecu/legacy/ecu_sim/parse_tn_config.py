# -*- coding: utf-8 -*-
"""
@File        : parse_tc_config.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021-03-28 09:20
@Description : Parase test_network.yaml configuration file
"""


import yaml
from copy import deepcopy
from xat_ecu.legacy.common.logger import logger


class ParseTNConfig(object):
    def __init__(self, tnconfig):
        self.tnconfig = tnconfig
        self.yaml_content = self.get_yaml()
        self.ecu_map_id = self.get_config_parse("ecu_map_id")
        self.all_ecu_list = self.get_all_ecu_list()

    def get_yaml(self):
        with open(self.tnconfig, 'rb') as f:
            yaml_content = list(yaml.safe_load_all(f))
        return yaml_content[0]

    def get_config_parse(self, *args):
        """
        :param args: the element path, such as: exec_node, mac, firefox
        :return: return sub elements
        """
        tmp_cfg = deepcopy(self.yaml_content)
        for para in args:
            tmp_cfg = tmp_cfg[para]
        return tmp_cfg

    def get_all_ecu_list(self):
        return [ecu for ecu in self.ecu_map_id]

    def get_ecu_doip(self, ecu):
        return self.ecu_map_id[ecu][0]

    def get_ecu_from_doip_id(self, doip_id: int):
        '''
        :param doip_id  type:int   such as 0x1001
        '''
        for ecu, ecuinfo in self.ecu_map_id.items():
            if ecuinfo[0] == doip_id:
                return ecu
        logger.error("doip id [{}] 在整车mapping 没有找到".format(doip_id))

    def get_can_req_id(self, ecu):
        return self.ecu_map_id[ecu][1]

    def get_can_res_id(self, ecu):
        return self.ecu_map_id[ecu][2]

    def get_lin_id(self, ecu):
        return self.ecu_map_id[ecu][3]

    def get_fr_id(self, ecu):
        return self.ecu_map_id[ecu][4]

    def get_eth_dig_ip(self, ecu):
        return self.ecu_map_id[ecu][5]

    def get_eth_dds_ip(self, ecu):
        return self.ecu_map_id[ecu][6]

    def get_gw_can(self):
        return self.yaml_content.get("gw_can")

    def get_gateway_ip(self):
        return self.yaml_content.get("gateway_ip")

    def get_positive_data(self):
        return self.yaml_content.get("positive_data")

    def get_dtc_code_table(self):
        return self.yaml_content.get("dtc_code_table")

    def get_dtc_snapshot_table(self):
        return self.yaml_content.get("dtc_snapshot_table")

    def get_dtc_code_table(self):
        return self.yaml_content.get("dtc_code_table")

    def get_routine_control_table(self):
        return self.yaml_content.get("routine_control_table")

    def get_vehicle_topology(self):
        return self.yaml_content.get("vehicle_topology")

    def get_bus_type(self):
        return self.yaml_content.get("bus_type")

    def get_can_or_lin(self, ecu):
        bus = self.get_bus(ecu)
        if "lin" in bus:
            return "lin"
        else:
            return "can"

    def get_channel(self, ecu):
        bus = self.get_bus(ecu)
        return self.get_config_parse("pcan")[bus]

    def get_channel_by_bus(self, bus):
        return self.get_config_parse("pcan")[bus]


if __name__ == '__main__':
    from sys import argv

    f = argv[1]
    print(f)
    tn_cfg = ParseTNConfig(f)
    print(tn_cfg.get_config_parse("can"))
