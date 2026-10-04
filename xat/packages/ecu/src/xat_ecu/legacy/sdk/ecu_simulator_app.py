# -*- coding: utf-8 -*-
"""
@File        : ecu_simulator_app.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2023-03-11 23:59
@Description : Ecu_Sim_App simulate the ecu behavior using pcan
"""
    

import os
from typing import Tuple, Union
from xat_ecu.legacy.ecu_sim.parse_tn_config import ParseTNConfig
from xat_ecu.legacy.ecu_sim.parse_tb_config import ParseTBConfig
import time
from time import sleep
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.ecu_sim_const import ECUSimConst
from xat_ecu.legacy.sdk.diagnosis.uds_const import *
from xat_ecu.legacy.sdk.can_lin.ecu_can_lin_simulator import Ecu_Sim
from xat_ecu.legacy.sdk.ethernet.doip_server_sim_odx import Doip_Server_Sim_Odx
from xat_ecu.legacy.common import exception_error
from xat_ecu.legacy.common.error_code import StatusCode
from xat_ecu.legacy.common.exception_error import error_check
from xat_ecu.legacy.utils.utils import struct_pretty


class MockUdsResponseDataInfo:

    def __init__(self):
        self.SID_10 = dict()
        self.SID_11 = dict()
        self.SID_27 = dict()
        self.SID_34: Union[list, dict] = None
        self.SID_36 = dict()
        self.SID_37 = None
        self.BFS = dict()
        self.no_reply = False

    
class Ecu_Sim_App():
    def __init__(self, **cfg):
        '''
            :param cfg: dict
            cfg = {
            dut_ecu: ["BGM"]
            gateway_ip: "169.254.1.1"

            bus:
              eth_obd: "enx000ec64a8e4c"
              eth_vlan5: "eth0.5"
              eth_vlan9: "eth0.9"
              bodycan: 'can0'
              }
        '''

        tb_default_path = os.path.join(os.path.realpath(__file__).split("ecu_simulator")[0], "ecu_simulator/config/default_config.yaml")
        tb_default_config = ParseTBConfig(tb_default_path)

        if cfg:
            self.cfg = cfg
        else:
            self.cfg = tb_default_config.yaml_content

        self.tosun_obj = self.cfg.get("tosun_obj")
        self.tosun_fr_obj = self.cfg.get("tosun_fr_obj")
        self.ecu_dict = {}
        
        bus_channel = self.cfg.get("bus")
        ecu_mock_cfg = self.cfg.get("ecu_mock_cfg")
        dut_ecu = self.cfg.get("dut_ecu")
        sec_con = self.cfg.get("sec_con")
        gatway_ecu = ECUSimConst.GATEWAY_ECU

        self.p_n_res = ecu_mock_cfg.get("p_n_res")
        self.nrc_code = ecu_mock_cfg.get("nrc_code")
        self.diag_mode = ecu_mock_cfg.get("diag_mode")
        self.ecu_name = ecu_mock_cfg.get("ecu_name")
        self.server_doip_id = ecu_mock_cfg.get("server_doip_id")
        self.server_ip = ecu_mock_cfg.get("server_ip")

        self.veh_type = self.cfg.get("veh_type")
        self.bl_ver = self.cfg.get("bl_ver")
        if self.veh_type and self.bl_ver:
            # self.cls_path = "sdk/data/{}/can_lin_fr_cls/{}".format(self.veh_type, self.bl_ver)
            tn_config_path = "config/{}/{}/ecu_network.yaml".format(self.veh_type, self.bl_ver)
        else:
            logger.error("Config error : self.veh_type is {}  self.bl_ver is {}".format(self.veh_type, self.bl_ver))
        tn_config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                                      tn_config_path)
        self.tn_config = ParseTNConfig(tn_config_path)
        self.ecu_map_id = self.tn_config.ecu_map_id
        self.positive_data = self.tn_config.get_positive_data()
        self.dtc_code_table = self.tn_config.get_dtc_code_table()
        self.dtc_snapshot_table = self.tn_config.get_dtc_snapshot_table()
        self.dtc_extended_data_table = self.tn_config.get_dtc_code_table()
        self.routine_control_p_data = self.tn_config.get_routine_control_table()
        self.vehicle_topology = self.tn_config.get_vehicle_topology()
        self.bus_type = self.tn_config.get_bus_type()

        gw_can = self.tn_config.get_gw_can()

        lin_bus = self.bus_type.get("lin")
        can_bus = self.bus_type.get("can")
        canfd_bus = self.bus_type.get("canfd")
        fr_bus = self.bus_type.get("fr")
        self.not_on_bench_ecu = []
        self.needful_bus = []
        self.no_dut_ecu = []
        self.vehicle_topology_no_eth = self.get_no_eth_vehicle_topology()

        if self.diag_mode == "ALL":
            self.doip_sim = Doip_Server_Sim_Odx(server_doip_id=self.server_doip_id, server_ip=self.server_ip,
                                                    server_port=Doip.SERVER_PORT,
                                                    p_n_res=self.p_n_res, data_info=self.positive_data,
                                                    nrc_code=self.nrc_code, ecu_map_id=self.ecu_map_id,
                                                    dtc_code=self.dtc_code_table,  routine_control_p_data=self.routine_control_p_data,
                                                    sec_con=sec_con, mock_uds_data=MockUdsResponseDataInfo())

            if self.ecu_name == "ALL":              # ecu_name = "ALL", p_n_res = True,data_info = []  Fixed together
                for dutecu in dut_ecu:
                    ecubus = self.vehicle_topology_no_eth.get(dutecu)
                    self.needful_bus = list(set(self.needful_bus) | set(ecubus))   #  测试 dut ecu 需要的 bus
                self.no_dut_ecu = list(set(self.vehicle_topology.keys()) - set(dut_ecu))   #  非 dut ecu
                for ecu_key in self.no_dut_ecu:
                    i = 0
                    bus_names = self.get_bus_name(ecu_key)
                    if bus_names is None:
                        # logger.error("{} is error, not in vehicle_topology".format(ecu_key))
                        logger.exception("{} 错误，没有在车辆拓扑中".format(ecu_key))
                        break
                    for bus_name in bus_names:
                        #  For the time being, only one diagnostic bus is supported, and the diagnostic bus is placed in the first of the list
                        if bus_name not in self.needful_bus:
                            if i == 0:
                                self.not_on_bench_ecu.append(ecu_key)  #  self.not_on_bench_ecu   --》不需要模拟的ECU & （台架没法模拟的ECU）
                            break
                        self.dtc_code = self.dtc_code_table.get(ecu_key, None)
                        snapshot_unit_data = self.dtc_snapshot_table.get(ecu_key, None)
                        extended_unit_data = self.dtc_extended_data_table.get(ecu_key, None)
                        self.channel = bus_channel.get(bus_name)
                        self.ecu_canid = self.tn_config.get_can_req_id(ecu_key)
                        res_ecu_canid = self.tn_config.get_can_res_id(ecu_key)
                        if not self.routine_control_p_data.get(ecu_key):
                            self.routine_control_p_data[ecu_key] = {}
                        routine_control_p_data = self.routine_control_p_data.get(ecu_key)
                        lin_nad = self.tn_config.get_lin_id(ecu_key)
                        self.data_info = self.positive_data.get(ecu_key, {})
                        if not self.channel:
                            self.not_on_bench_ecu.append(ecu_key)   #  self.not_on_bench_ecu   （不需要模拟的ECU） &   --》台架没法模拟的ECU
                            # logger.warning("{} is not on the bench_config".format(bus_name))
                            logger.warning("{} 没有在bench_config中".format(bus_name))
                            break
                        if i == 0:
                            ecu_channel = ecu_key
                        else:
                            # ecu_channel = ecu_key + "_" + self.channel
                            # logger.error(" ( > 1 )  num of diagnostic can/lin/fr is Not in line with expectations ")
                            logger.debug("( > 1 ) 数量诊断can/lin/fr不符合预期")
                            break
                        i += 1

                        if bus_name in can_bus:
                            self.ecu_dict[ecu_channel] = Ecu_Sim(tosun_obj=self.tosun_obj, bus_name=bus_name, ecu=ecu_key, ecu_canid=self.ecu_canid, channel=self.channel, res_ecu_canid=res_ecu_canid, lin_nad=lin_nad, bus_type="can",
                                                             p_n_res=self.p_n_res, data_info=self.data_info, nrc_code=self.nrc_code,
                                                             dtc_code=self.dtc_code, snapshot_data=snapshot_unit_data, routine_control_p_data=routine_control_p_data,
                                                             extended_data=extended_unit_data, block_size=Can.block_size, st=Can.st, sec_con=sec_con, mock_uds_data=MockUdsResponseDataInfo())
                        elif bus_name in canfd_bus:
                            self.ecu_dict[ecu_channel] = Ecu_Sim(tosun_obj=self.tosun_obj, bus_name=bus_name, ecu=ecu_key, ecu_canid=self.ecu_canid, channel=self.channel, res_ecu_canid=res_ecu_canid, lin_nad=lin_nad, bus_type="canfd",
                                                             p_n_res=self.p_n_res, data_info=self.data_info, nrc_code=self.nrc_code,
                                                             dtc_code=self.dtc_code, snapshot_data=snapshot_unit_data, routine_control_p_data=routine_control_p_data,
                                                             extended_data=extended_unit_data, block_size=Can.block_size, st=Can.st, sec_con=sec_con, mock_uds_data=MockUdsResponseDataInfo())
                        elif bus_name in lin_bus:
                            self.ecu_dict[ecu_channel] = Ecu_Sim(tosun_obj=self.tosun_obj, bus_name=bus_name, ecu=ecu_key, ecu_canid=self.ecu_canid, channel=self.channel, res_ecu_canid=res_ecu_canid, lin_nad=lin_nad, bus_type="lin",
                                                             p_n_res=self.p_n_res, data_info=self.data_info, nrc_code=self.nrc_code,
                                                             dtc_code=self.dtc_code, snapshot_data=snapshot_unit_data, routine_control_p_data=routine_control_p_data,
                                                             extended_data=extended_unit_data, sec_con=sec_con, mock_uds_data=MockUdsResponseDataInfo())
                        elif bus_name in fr_bus:
                            fr_id = self.tn_config.get_fr_id(ecu_key)
                            self.ecu_dict[ecu_channel] = Ecu_Sim(tosun_obj=self.tosun_fr_obj, bus_name=bus_name,
                                                                 ecu=ecu_key,
                                                                 ecu_canid=self.tn_config.get_ecu_doip(ecu_key), channel=self.channel,
                                                                 res_ecu_canid=fr_id, lin_nad=lin_nad,
                                                                 bus_type="fr",
                                                                 p_n_res=self.p_n_res, data_info=self.data_info,
                                                                 nrc_code=self.nrc_code,
                                                                 dtc_code=self.dtc_code,
                                                                 snapshot_data=snapshot_unit_data,
                                                                 routine_control_p_data=routine_control_p_data,
                                                                 extended_data=extended_unit_data,
                                                                 block_size=Can.block_size, st=Can.st, sec_con=sec_con,
                                                                 mock_uds_data=MockUdsResponseDataInfo())

                            logger.debug(f"模拟的flexray类型ecu:{ecu_key}")
                        else:
                            # logger.warning("{} is not on the vehicle_topology".format(bus_name))
                            logger.warning("{} 没有在车辆拓扑上".format(bus_name))
            else:
                # logger.exception("ecu_name expects ALL,not {}".format(self.ecu_name))
                logger.warning("期望ecu名字是ALL，得到：{}".format(self.ecu_name))

        elif self.diag_mode == "doip":
            self.doip_sim = Doip_Server_Sim_Odx(server_doip_id=self.server_doip_id, server_ip=self.server_ip,
                                                    server_port=Doip.SERVER_PORT,
                                                    p_n_res=self.p_n_res, data_info=self.positive_data,
                                                    nrc_code=self.nrc_code, ecu_map_id=self.ecu_map_id,
                                                    dtc_code=self.dtc_code_table, routine_control_p_data=self.routine_control_p_data,
                                                    sec_con=sec_con, mock_uds_data=MockUdsResponseDataInfo())
            # self.doip_sim = Doip_Server_Sim_Odx(server_doip_id=self.server_doip_id, server_ip=self.server_ip,
            #                                         server_port=Doip.SERVER_PORT
            #                                         )
        else: # 非doip 的单个ECU
            bus_name = self.get_bus_name(self.ecu_name)     # name of ecu, such as 'bodycan'
            if isinstance(bus_name, list):
                bus_name = bus_name[0]           #  There is only one diagnostic can/lin/fr by default
            else:
                # logger.error("{} is not on the vehicle_topology".format(self.ecu_name))
                with error_check(None, exception_error.DOCANError):
                    # logger.error("{} is not on the vehicle_topology".format(self.ecu_name))
                    raise AssertionError("{} 没有在车辆拓扑上".format(self.ecu_name))

            self.dtc_code = self.dtc_code_table.get(self.ecu_name, None)
            snapshot_unit_data = self.dtc_snapshot_table.get(self.ecu_name, None)
            extended_unit_data = self.dtc_extended_data_table.get(self.ecu_name, None)
            self.channel = bus_channel.get(bus_name)
            self.ecu_canid = self.tn_config.get_can_req_id(self.ecu_name)
            res_ecu_canid = self.tn_config.get_can_res_id(self.ecu_name)
            if not self.routine_control_p_data.get(self.ecu_name):
                self.routine_control_p_data[self.ecu_name] = {}
            routine_control_p_data = self.routine_control_p_data.get(self.ecu_name)
            lin_nad = self.tn_config.get_lin_id(self.ecu_name)
            self.data_info = self.positive_data.get(self.ecu_name, {})
            if bus_name in can_bus:
                self.ecu_sim = Ecu_Sim(tosun_obj=self.tosun_obj, bus_name=bus_name, ecu=self.ecu_name, ecu_canid=self.ecu_canid, channel=self.channel,
                                                     res_ecu_canid=res_ecu_canid, lin_nad=lin_nad, bus_type="can",
                                                     p_n_res=self.p_n_res, data_info=self.data_info,
                                                     nrc_code=self.nrc_code, routine_control_p_data=routine_control_p_data,
                                                     dtc_code=self.dtc_code, snapshot_data=snapshot_unit_data,
                                                     extended_data=extended_unit_data, block_size=Can.block_size,
                                                     st=Can.st, sec_con=sec_con, mock_uds_data=MockUdsResponseDataInfo())
            elif bus_name in canfd_bus:
                self.ecu_sim = Ecu_Sim(tosun_obj=self.tosun_obj, bus_name=bus_name, ecu=self.ecu_name, ecu_canid=self.ecu_canid, channel=self.channel,
                                                     res_ecu_canid=res_ecu_canid, lin_nad=lin_nad, bus_type="canfd",
                                                     p_n_res=self.p_n_res, data_info=self.data_info,
                                                     nrc_code=self.nrc_code, routine_control_p_data=routine_control_p_data,
                                                     dtc_code=self.dtc_code, snapshot_data=snapshot_unit_data,
                                                     extended_data=extended_unit_data, block_size=Can.block_size,
                                                     st=Can.st, sec_con=sec_con, mock_uds_data=MockUdsResponseDataInfo())
            elif bus_name in lin_bus:
                self.ecu_sim = Ecu_Sim(tosun_obj=self.tosun_obj, bus_name=bus_name, ecu=self.ecu_name, ecu_canid=self.ecu_canid, channel=self.channel,
                                                     res_ecu_canid=res_ecu_canid, lin_nad=lin_nad, bus_type="lin",
                                                     p_n_res=self.p_n_res, data_info=self.data_info,
                                                     nrc_code=self.nrc_code, routine_control_p_data=routine_control_p_data,
                                                     dtc_code=self.dtc_code, snapshot_data=snapshot_unit_data,
                                                     extended_data=extended_unit_data, sec_con=sec_con, mock_uds_data=MockUdsResponseDataInfo())
            elif bus_name in fr_bus:
                fr_id = self.tn_config.get_fr_id(self.ecu_name)
                self.ecu_sim = Ecu_Sim(tosun_obj=self.tosun_fr_obj, bus_name=bus_name,
                                                     ecu=self.ecu_name,
                                                     ecu_canid=self.tn_config.get_ecu_doip(self.ecu_name), channel=self.channel,
                                                     res_ecu_canid=fr_id, lin_nad=lin_nad,
                                                     bus_type="fr",
                                                     p_n_res=self.p_n_res, data_info=self.data_info,
                                                     nrc_code=self.nrc_code,
                                                     dtc_code=self.dtc_code,
                                                     snapshot_data=snapshot_unit_data,
                                                     routine_control_p_data=routine_control_p_data,
                                                     extended_data=extended_unit_data,
                                                     block_size=Can.block_size, st=Can.st, sec_con=sec_con,
                                                     mock_uds_data=MockUdsResponseDataInfo())
            else:
                # logger.warning("{} is not on the vehicle_topology".format(bus_name))
                logger.warning("{} 没有在车辆拓扑上".format(bus_name))

    def get_no_eth_vehicle_topology(self):
        vehicle_topology_no_eth = {}
        for ecukey in self.vehicle_topology.keys():
            ecu_no_eth_bus = []
            for bus in self.vehicle_topology.get(ecukey):
                if "eth_" not in bus:
                    ecu_no_eth_bus.append(bus)
            vehicle_topology_no_eth[ecukey] = ecu_no_eth_bus
        return vehicle_topology_no_eth
                            
    def get_ecu_canid(self,ecu_name):
        ecu_canid = self.vehicle_topology[ecu_name][0]
        return ecu_canid

    def get_bus_name(self, ecu_name):
        bus_name = self.vehicle_topology.get(ecu_name)
        return bus_name

    # def set_ecu_sim(self,ecu_canid,channel):
    #     ecu_canid = self.ecu_canid
    #     channel = self.channel
    #     self.ecu_sim = Ecu_Sim(ecu_canid,channel)

    def all_start(self):
        if hasattr(self, "doip_sim"):
            self.doip_sim_start()
        # 所有非doip ecu 启动
        if hasattr(self, "ecu_sim"):
            self.ecu_sim_start()
        # 单个ecu启动
        if self.ecu_dict:
            self.all_ecu_start()

    def all_close(self):
        if hasattr(self, "doip_sim"):
            self.doip_sim_close()
        # 所有非doip ecu 启动
        if hasattr(self, "ecu_sim"):
            self.ecu_sim_close()
        # 单个ecu启动
        if self.ecu_dict:
            self.all_ecu_close()

    def ecu_sim_start(self):
        # single ecu
        self.ecu_sim.run()

    def ecu_sim_close(self):
        # single ecu
        self.ecu_sim.close()

    def doip_sim_start(self):
        # single ecu
        self.doip_sim.run()

    def doip_sim_close(self):
        # single ecu
        self.doip_sim.close()

    def send_candata(self, bus_name: str, ecu_name: str, res_ecu_canid: int, data: list):
        '''
        指用于tosun can
        :param bus_name: such as "bodycan"
        :param ecu_name: if it is "can" , ecu_name such as "PLG" , "BCM_F"
                         if it is "lin" , ecu_name such as "SCU_D"
        :param res_ecu_canid: type:int  msg id  such as  0x623
        :param data: type:list   such as  [0x7F, 0x22, 0x78]   
        '''
        
        if self.ecu_dict:
            if self.ecu_dict[ecu_name]:
                self.tosun_obj.can_send(bus_name, data, res_ecu_canid, cycle_time=0)
            else:
                with error_check(StatusCode.DOCAN_ECU_NOT_FOUND_ERR, exception_error.DOCANError):
                    raise AssertionError(f"没有发现ecu:{ecu_name}")
        else:
            logger.error("没有can对象去进行诊断数据")


    def update_0x22_data(self, ecu_name: str, did: str, data_info_update: Union[list, dict, str]):
        '''
        更新 0x22 服务相关数据
        single ecu of all_ecu,    data_info   is dict   
        read_data_by_identifier(SID=0x22) data positive response update
        :param ecu_name: if it is "can" , ecu_name such as "PLG" , "BCM_F"
                         if it is "lin" , ecu_name such as "SCU_D"
        :param did: type:str  such as F1AA
        :data_info_update: one DID Positive/negative response      
            Positive response   type : list or str(str建议不用，需要了解的场景比较多)     such as [0x01]
            Negative response   type : dict   such as {"NRC": 0x22}
        '''
        if hasattr(self, "doip_sim"):
            if self.doip_sim.data_infos.get(ecu_name) and isinstance(self.doip_sim.data_infos.get(ecu_name), dict):
                self.doip_sim.data_infos[ecu_name][did] = data_info_update
            else:
                self.doip_sim.data_infos[ecu_name] = {}
                self.doip_sim.data_infos[ecu_name][did] = data_info_update
        if self.ecu_dict:
            with error_check(StatusCode.DOCAN_ECU_NOT_FOUND_ERR, exception_error.DOCANError):
                self.ecu_dict[ecu_name].data_info[did] = data_info_update
    
    def update_0x31_data(self, ecu_name: str, routine_control_data: dict):
        '''
        更新 0x31 服务相关数据
        :param ecu_name: if it is "can" , ecu_name such as "PLG" , "BCM_F"
                         if it is "lin" , ecu_name such as "SCU_D"
        :param routine_control_data: routine control positive (include rid , routine_type , rsr)    /Negative data ,      type:dict 
                            such as  {"08BA": { 1 : [0x00] , 3 : [0x02]}}    {"08BA":{"NRC": 0x22}}
                            rid: "08BA" is  HV PowerDown 
                            routine_type:  are Fixed
                                        1  ---- "start routine request"
                                        2  ---- "stop rountine request"
                                        3  ---- "request rountine results"   
                            rsr: [0x00],[0x02],[0xA0,0x01] Specific ECU may have different implementation      
        '''
        if hasattr(self, "doip_sim"):
            if self.doip_sim.routine_control_p_datas.get(ecu_name) and isinstance(self.doip_sim.routine_control_p_datas.get(ecu_name), dict):
                self.doip_sim.routine_control_p_datas[ecu_name].update(routine_control_data)
            else:
                self.doip_sim.routine_control_p_datas[ecu_name] = {}
                self.doip_sim.routine_control_p_datas[ecu_name].update(routine_control_data)
        if self.ecu_dict:
            with error_check(StatusCode.DOCAN_ECU_NOT_FOUND_ERR, exception_error.DOCANError):
                self.ecu_dict[ecu_name].routine_control_p_data.update(routine_control_data)

    def update_0x10_data(self, ecu_name: str, session_mode: dict):
        '''
        更新 0x10 切换会话服务相关数据 (只针对物理寻址Mock，功能寻址不需要回复)
        :param ecu_name: if it is "can" , ecu_name such as "PLG" , "BCM_F"
                         if it is "lin" , ecu_name such as "SCU_D"
        :param session_mode: one DID Positive/negative response
            Positive response   type : dict such as {0x01: [0x01, 0x02, 0x03, 0x04], 0x02: [0x01, 0x02, 0x03, 0x04], 0x03: {"NRC": 0x22}}
            发送01会话时，期望返回的肯定响应+后面的值：[0x01, 0x02, 0x03, 0x04]
            发送03会话时，期望返回的肯定响应+后面的值：{"NRC": 0x22}
        '''
        if hasattr(self, "doip_sim"):
            self.doip_sim.mock_uds_data.SID_10 = session_mode

        if self.ecu_dict:
            with error_check(StatusCode.DOCAN_ECU_NOT_FOUND_ERR, exception_error.DOCANError):
                self.ecu_dict[ecu_name].mock_uds_data.SID_10 = session_mode

    def update_0x11_data(self, ecu_name: str, reset_type: Union[int, dict]):
        '''
        更新 0x11 服务相关数据
        :param ecu_name: if it is "can" , ecu_name such as "PLG" , "BCM_F"
                         if it is "lin" , ecu_name such as "SCU_D"
        :param reset_type
            Positive response   type : int  such as 0x01为硬重启
            Negative response   type : dict   such as {"NRC": 0x22}
        '''
        if hasattr(self, "doip_sim"):
            self.doip_sim.mock_uds_data.SID_11 = reset_type

        if self.ecu_dict:
            with error_check(StatusCode.DOCAN_ECU_NOT_FOUND_ERR, exception_error.DOCANError):
                self.ecu_dict[ecu_name].mock_uds_data.SID_11 = reset_type

    def update_0x36_data(self, ecu_name: str, block_sequence_counter_nrc_config: dict):
        '''
        0x36 模拟数据传输 (只针对物理寻址Mock，功能寻址不需要回复)
        :param ecu_name: if it is "can" , ecu_name such as "PLG" , "BCM_F"
                         if it is "lin" , ecu_name such as "SCU_D"
        :param block_sequence_counter_nrc_config: 第几个seq counter回复否定响应配置，如：
        {2: 0x78, 18: 0x11} 表示服务端收到第二个counter回复否定响应0x78，第18个counter回复0x11否定
        响应
        '''
        if hasattr(self, "doip_sim"):
            self.doip_sim.mock_uds_data.SID_36 = block_sequence_counter_nrc_config

        if self.ecu_dict:
            with error_check(StatusCode.DOCAN_ECU_NOT_FOUND_ERR, exception_error.DOCANError):
                self.ecu_dict[ecu_name].mock_uds_data.SID_36 = block_sequence_counter_nrc_config

    def update_0x37_data(self, ecu_name: str, data: dict):
        '''
        更新 请求结束刷写 ECU复位服务相关数据 (只针对物理寻址Mock，功能寻址不需要回复)
        :param ecu_name: if it is "can" , ecu_name such as "PLG" , "BCM_F"
                         if it is "lin" , ecu_name such as "SCU_D"
        :param data: one DID Positive/negative response
            Negative response   type : dict   such as {"NRC": 0x22}
        '''
        if hasattr(self, "doip_sim"):
            self.doip_sim.mock_uds_data.SID_37 = data

        if self.ecu_dict:
            with error_check(StatusCode.DOCAN_ECU_NOT_FOUND_ERR, exception_error.DOCANError):
                self.ecu_dict[ecu_name].mock_uds_data.SID_37 = data

    def update_0x27_data(self, ecu_name: str, data_info: dict):
        '''
        更新 0x27 会话解锁
        :param ecu_name: if it is "can" , ecu_name such as "PLG" , "BCM_F"
                         if it is "lin" , ecu_name such as "SCU_D"
        :param data_info: one DID Positive/negative response
            Positive response   type : int     such as {0x01: [0x01, 0x02, 0x03], 0x02: []} 等级是0x01时
            回复种子：[0x01, 0x02, 0x03], 等级是0x02时直接回复67 02
            Negative response   type : dict   such as {"NRC": 0x22}
        '''
        if hasattr(self, "doip_sim"):
            self.doip_sim.mock_uds_data.SID_27 = data_info

        if self.ecu_dict:
            with error_check(StatusCode.DOCAN_ECU_NOT_FOUND_ERR, exception_error.DOCANError):
                self.ecu_dict[ecu_name].mock_uds_data.SID_27 = data_info

    def update_0x34_data(self, ecu_name: str, data: Union[list, dict]):
        '''
        更新 0x34 请求服务下载 (只针对物理寻址Mock，功能寻址不需要回复)
        :param ecu_name: if it is "can" , ecu_name such as "PLG" , "BCM_F"
                         if it is "lin" , ecu_name such as "SCU_D"
        :param data: one DID Positive/negative response
            Positive response   type : int     such as [0x20, 0x20, 0x20]
            Negative response   type : dict   such as {"NRC": 0x22}
        '''
        if hasattr(self, "doip_sim"):
            self.doip_sim.mock_uds_data.SID_34 = data

        if self.ecu_dict:
            with error_check(StatusCode.DOCAN_ECU_NOT_FOUND_ERR, exception_error.DOCANError):
                self.ecu_dict[ecu_name].mock_uds_data.SID_34 = data

    def multi_ecu_update_data_info(self, ecu_name,  p_data_info_updates, p_n_res_update=True):
        # 旧接口，不建议使用
        for did, p_data_info in p_data_info_updates.items():
            self.single_ecu_sim_update_data_info(ecu_name, did, p_data_info, p_n_res_update)

    def ecu_sim_update_data_info(self, data_info_update, p_n_res_update = True):
        # 旧接口，不建议使用
        # single ecu
        # data_info_update is DID Positive response
        # data_info_update is list
        self.ecu_sim.p_n_res = p_n_res_update
        self.ecu_sim.data_info = data_info_update
    
    def ecu_sim_update_nrc_code(self, nrc_code, p_n_res_update=False):
        # 旧接口，不建议使用
        # single ecu
        # nrc_code is NRC
        # nrc_code is list   such as [0x22]
        self.ecu_sim.p_n_res = p_n_res_update
        self.ecu_sim.nrc_code = nrc_code
    
    def single_ecu_start(self,ecu_name):
        # single ecu of all_ecu
        self.ecu_dict[ecu_name].run()
        # logger.info("start {} ecu sim".format(ecu_name))
        logger.debug(f"已开启ecu：{ecu_name}")

    def multi_ecus_close(self, ecu_list):
        for ecu_name in ecu_list:
            self.single_ecu_close(ecu_name)

    def multi_ecus_start(self, ecu_list):
        for ecu_name in ecu_list:
            self.single_ecu_start(ecu_name)

    def single_ecu_close(self, ecu_name):
        # single ecu of all_ecu
        self.ecu_dict[ecu_name].close()
        # logger.info("close {} ecu sim".format(ecu_name))
        logger.debug(f"已关闭ecu：{ecu_name}")

    def single_ecu_sim_update_data_info(self,ecu_name, did, p_data_info_update, p_n_res_update = True):
        '''
        single ecu of all_ecu,    data_info   is dict   
        read_data_by_identifier(SID=0x22) data positive response update
        :param ecu_name: if it is "can" , ecu_name such as "PLG" , "BCM_F"
                         if it is "lin" , ecu_name such as "SCU_D"
        :p_data_info_update: one DID Positive response      type : list or str      
        ''' 
        self.ecu_dict[ecu_name].p_n_res = p_n_res_update
        self.ecu_dict[ecu_name].data_info[did] = p_data_info_update
            
    def single_ecu_sim_update_dtc_code(self,ecu_name, dtc_code, p_n_res_update = True):
        '''
        single ecu of all_ecu,  
        update DTC
        :param ecu_name: if it is "can" , ecu_name such as "PLG" , "BCM_F"
                         if it is "lin" , ecu_name such as "SCU_D"
        :param dtc_code: such as  {'C16A904': [86, 169, 4, 15] ,'C16AA04': [86, 170, 4, 15]}      type : dict  
        '''
        self.ecu_dict[ecu_name].p_n_res = p_n_res_update
        self.ecu_dict[ecu_name].dtc_code = dtc_code

    def multi_ecus_sim_update_nrc_code(self, ecu_info_list):
        """
        update multi ecus' nrc code
        """
        for info in ecu_info_list:
            self.single_ecu_sim_update_nrc_code(info.get("ecu_name", None), info.get("nrc_code", None), info.get("p_n_res_update", None))

    def single_ecu_sim_update_nrc_code(self,ecu_name, nrc_code, p_n_res_update = False):
        '''
        single ecu of all_ecu
        :param ecu_name: if it is "can" , ecu_name such as "PLG" , "BCM_F"
                         if it is "lin" , ecu_name such as "SCU_D"
        :nrc_code: DID Positive response      type : list     
        '''
        self.ecu_dict[ecu_name].p_n_res = p_n_res_update
        self.ecu_dict[ecu_name].nrc_code = nrc_code
        
    def single_ecu_sim_update_routine_control_p_data(self,ecu_name, routine_control_p_data , p_n_res_update = True):
        '''
        single ecu of all_ecu
        :param ecu_name: if it is "can" , ecu_name such as "PLG" , "BCM_F"
                         if it is "lin" , ecu_name such as "SCU_D"
        :param routine_control_p_data : routine control positive data (include rid , routine_type , rsr)  ,      type:dict 
                            such as  {"08BA": { 1 : [0x00] , 3 : [0x02]}}
                            rid: "08BA" is  HV PowerDown 
                            routine_type:  are Fixed
                                        1  ---- "start routine request"
                                        2  ---- "stop rountine request"
                                        3  ---- "request rountine results"   
                            rsr: [0x00],[0x02],[0xA0,0x01] Specific ECU may have different implementation      
        '''
        self.ecu_dict[ecu_name].p_n_res = p_n_res_update
        self.ecu_dict[ecu_name].routine_control_p_data = routine_control_p_data
        
    def single_ecu_sim_reset(self,ecu_name):
        #Restore to ECU_ sim_ Const configuration
        self.ecu_dict[ecu_name].p_n_res = True
        self.ecu_dict[ecu_name].data_info = self.positive_data[ecu_name]
        self.ecu_dict[ecu_name].dtc_code = self.dtc_code
    
    def all_ecu_sim_reset(self):
        # Restore to ECU_ sim_ Const configuration 
        for ecu_key in self.no_dut_ecu:
            bus_name = self.get_bus_name(ecu_key)[0]
            if ecu_key in self.not_on_bench_ecu:
                # logger.debug("{0} is not on the bench_config or needful, {1} simulator is non-existent, No need to reset ".format(bus_name,ecu_key))
                logger.debug("{0} 没有在bench_config配置文件或者不是需要的, {1} 不需要重置".format(bus_name,ecu_key))
            else:
                self.ecu_dict[ecu_key].p_n_res = True
                self.ecu_dict[ecu_key].data_info = self.positive_data.get(ecu_key, None)
                self.ecu_dict[ecu_key].dtc_code = self.dtc_code_table.get(ecu_key, None)
                self.ecu_dict[ecu_key].nrc_code = self.nrc_code
        # logger.info("reset all ecu sim")
        logger.info("所有的ECU已经重置...")

    def all_ecu_start(self):
        for ecu_key in self.no_dut_ecu:
            bus_name = self.get_bus_name(ecu_key)[0]
            if ecu_key in self.not_on_bench_ecu:
                # logger.info("{0} is not on the bench_config or needful, {1} simulator can not start".format(bus_name, ecu_key))
                logger.debug("{0} 没有在bench_config配置文件或者不是需要的, {1} 没有启动".format(bus_name, ecu_key))
            else:
                self.ecu_dict[ecu_key].run() 
                logger.debug("ecu: "+ ecu_key + ' start!')
        # logger.debug("start all ecu sim")
        logger.info("所有的ECU已经启动...")

    def all_ecu_close(self):
        for ecu_key in self.no_dut_ecu:
            bus_name = self.get_bus_name(ecu_key)[0]
            if ecu_key in self.not_on_bench_ecu:
                # logger.info("{0} is not on the bench_config or needful, {1} simulator is non-existent".format(bus_name, ecu_key))
                logger.debug("{0} 没有在bench_config配置文件或者不是需要的, {1} 没有退出".format(bus_name, ecu_key))
            else:
                self.ecu_dict[ecu_key].close()
        logger.info("所有的ECU已经关闭...")
            
        
