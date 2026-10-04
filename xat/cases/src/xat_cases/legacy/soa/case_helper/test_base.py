# -*- coding: utf-8 -*-
"""
@File        : common_test_base.py
@Author      : jiabin.zhu@jiduauto.com
@Time        : 2022/7/11 11:33
@Description :
@Examples    :
"""

import os
import sys
import json
from copy import deepcopy
from xat_cases.legacy.common_test_base import (
    CommonTestBase,
    logger,
    partner_process_check,
    sleep,
    EcuInfo, get_class_after_bgm_log, jy_dam0800_check_and_repair, inspect, defunc_process_check
)
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from xat_ecu.legacy.interface.bgm.bgm_env.change_bgm_env import (
    change_bgm_config,
    recover_bgm_config,
)
from xat_ecu.legacy.sdk.s2spdu.signal2service_combination_and_send_pdu import (
    S2sCombinationSendPdu,
)
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.sdk.Internal_ETH.tools.bgm_eth_internal import BgmEthInternal, s2s_json, s2s_path, write_s2s_json


class TestBase(CommonTestBase):
    def after_class_teardown(self, ecu: EcuInfo):
        # 调用子类
        try:
            self.after_class(self, ecu)
            if not ecu.domain.single_tcam and ecu.disable_env is False:
                get_class_after_bgm_log(self.bgmcli, ecu)  # 如果类有失败用例，则拷贝类相关的日志文件
            if "power_control_type" in ecu.tb_config:
                if ecu.tb_config.get("power_control_type") == "jydam0800":
                    jy_dam0800_check_and_repair()
        except AttributeError as e:
            err_msg = f'子类after_class执行失败，原因是:{str(e)}'
            logger.exception(err_msg)
            # 获取错误的描述信息，例如sd_tester，ipdu，partner等
            # AttributeError: type object 'xxxx' has no attribute 'xxx'
            # error_obj = str(e).split('attribute ')[-1]
            if hasattr(self, 'ipdu'):
                self.ipdu.time_control_stop()
            if hasattr(self, 'busapp'):
                self.busapp.stop_all_cyclic_msgs()
            # raise Exception(f'{error_obj}初始化失败，请检查before_class或者before_each_func中{error_obj}初始化是否正常')
        except Exception as e:
            err_msg = f'子类after_class执行失败，原因是:{str(e)}'
            logger.exception(err_msg)
            if hasattr(self, 'ipdu'):
                self.ipdu.time_control_stop()
                self.ipdu.recv_pdu_thread_all_stop()
            if hasattr(self, 'busapp'):
                self.busapp.stop_all_cyclic_msgs()
            # raise Exception(err_msg)
        finally:
            logger.info(inspect.stack()[0].function + ' start!')
            if hasattr(self, 'io'):
                self.io.close()
            if hasattr(self, 'log_manage'):
                self.log_manage.stop_record_soa_partner_log()
            if hasattr(self, 'sd_tester'):
                self.sd_tester.stop_tester_present()
                self.sd_tester.diagnostic_client_sim_close()
            # 检查上位机上是否有其它未关闭的soa_partner进程在运行，如果有，则杀死进程
            partner_process_check()
            # 检查上位机上是否有其它未关闭的defunc进程在运行，如果有，则重载进程
            defunc_process_check()

    def before_class(self, ecu, **kwargs):
        super().before_class(self, ecu)
        partner_process_check()
        self.bgmcli.check_bgm_start_type(self.nucapp)

        # 由基类控制诊断仪启动，并且先读取台架ccp
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.diagnostic_client_sim_start()
        curr_ccp_str, self.tb_ccp_list = self.sd_tester.read_ccp()

        # 启动BGM内部以太网控制器，用于mockmcu收发tcp或解析pacp报文，按需模拟udp报文发送
        self.bgm_eth_inter = BgmEthInternal(ipdu=self.ipdu, nucapp= self.nucapp, 
                                            # veh_type=ecu.tc_config['veh_type'], 
                                            bl_ver=ecu.tc_config['bl_ver'], **kwargs)

        self.ipdu.start_all_time_control(isrealbus=False if self.bgm_eth_inter.mock_mcu_udp else True)
        if not self.bgm_eth_inter.mock_mcu_udp:
            file = os.path.join(os.getcwd(), "tosun_asc_product_time")
            os.system(f"rm {file}")
            self.busapp.start_all_cyclic_msg()

    def after_class(self, ecu):
        # 由基类控制诊断仪关闭，并且需恢复台架ccp
        self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
        if not self.bgm_eth_inter.mock_mcu_udp:
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文

        self.bgm_eth_inter.env_post_process()
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.write_multi_ccp({index + 1: self.tb_ccp_list[index] for index in range(1556)})
        self.sd_tester.stop_tester_present()
        self.sd_tester.diagnostic_client_sim_close()
        super().after_class(self, ecu)

    def before_each_func(self, ecu, start=False):
        if hasattr(self, "partner"):
            self.partner.method_is_timeout = []
        super().before_each_func(ecu, start)

    def after_each_func(self, ecu, start=False):
        self.bgm_eth_inter.bgm_ssh.stop_bgm_tcpdump()
        self.bgm_eth_inter.bgm_ssh.delete_bgm_tcpdump_file(bgm_log_name='*.pcap')
        if hasattr(self, "partner"):
            self.partner.ck_method_timeout()
        super().after_each_func(ecu, start)
    
    def del_s2s_db(self):
        """删除s2s的数据库，一般用于测试默认配置"""
        self.bgmcli.type_commands("rm -f /data/s2s_service/s2s_service.db3", alias="1")
        self.bgmcli.type_commands("sync", alias="1")
        self.bgmcli.type_commands("ls -l /data/s2s_service/", alias="1")

    def del_SOAAPP_db(self):
        """删除SOAAPP的数据库，一般用于测试默认配置"""
        self.bgmcli.type_commands("rm -f /data/SOAApp/SOAApp.db3", alias="1")
        self.bgmcli.type_commands("sync", alias="1")
        self.bgmcli.type_commands("ls -l /data/SOAApp/", alias="1")

    def update_bgm_s2s_json(self, update_info: dict, partner_key=None):
        """
        更新本地s2s.json文件，并同步更新bgm的s2s.json并落盘
        @param update_info: 更新的字段内容
        @param partner_key: 需要重连的partner_key,如不填则不等待服务连接
        """
        write_s2s_json(update_info)
        self.bgmcli.scp_local_file_to_bgm(s2s_path, bgm_path="/data/app/etc/")
        self.bgmcli.type_commands("sync")
        self.bgmcli.type_commands("cat /data/app/etc/s2s.json")
        self.kill_s2s_and_reconnect_service(partner_key)

    def kill_s2s_and_reconnect_service(self, partner_key=None):
        """
        kill S2S进程，等待EM2拉起S2S并等待partner重新连接服务
        @param partner_key: 需要重连的partner_key,如不填则不等待服务连接
        """
        self.kill_bgm_process()
        self.partner.empty_all()
        if partner_key is not None:
            self.partner.wait_for_service_reconnect(partner_key)
    
    def write_ccp_by_tcp(self, new_ccp_map: dict):
        """
        通过仿真tcp数据直接发送ccp给到MPU
        @param new_ccp_map: {ccp_index: ccp_value}, index从1开始
        """
        logger.info(f"修改ccp：{new_ccp_map}")
        new_ccp = deepcopy(self.tb_ccp_list)
        for index, ccp_value in new_ccp_map.items():
            new_ccp[index-1] = ccp_value
        self.bgm_eth_inter.set_signal("CarConfig", DataTypeHanding.to_int(new_ccp), send_pdu_immediately=True)

    def set_nopeople_incar(self):
        self.io.drvr_door_open()
        self.io.driver_seat_notpresent()
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecMid', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecRi', 0)
        #确保开门3s后无人占座
        sleep(3)                                     
        self.io.drvr_door_close()