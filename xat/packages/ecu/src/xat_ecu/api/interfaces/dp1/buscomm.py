#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :buscomm.py
@Time         :2023/12/26 10:00
@Author       :quan.sun@jiduauto.com
@Description  :整车通信能力实现接口
"""
import math
import re
import threading
import time
from time import sleep

from xat_ecu import reporting as allure
from typing import List, Tuple

from xat_ecu.legacy.common import exception_error
from jsonpath_ng import parse as ng_parse
import copy
from xat_ecu.api import (
    CommonBusComm
)

from xat_ecu.legacy.common.data_handle import *
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from xat_ecu.legacy.tsp.proto_parse import ProtoParse
from xat_ecu.api.common import crc8, transferDTCtoBytes, check_signal_value_exist
from xat_ecu.api.constants.common import *


class BusComm(CommonBusComm):

    # ***************************************用户端抽象接口实现***************************************
    def set(self,
            bus_name: str,
            msg_name: str,
            signal_name: str,
            sig_value_name: Union[str, int, float],
            ub_flag=True,
            cycle_time=None):
        bus_obj = getattr(self.ipdu, bus_name)
        msg_signals_obj = getattr(bus_obj, msg_name)
        # msg_id = msg_name
        # self._filter_msg(bus_name, msg_id)
        return self.ipdu.set(msg_signals_obj, signal_name, sig_value_name, ub_flag=ub_flag, cycle_time=cycle_time)

    def check(self,
              bus_name: str,
              msg_name: str,
              signal_name: str,
              sig_value_name: Union[str, int],
              timeout: Union[float, int] = 5,
              do_assert=True,
              check_time=1,
              check_ub=None,):
        bus_obj = getattr(self.ipdu, bus_name)
        msg_signals_obj = getattr(bus_obj, msg_name)
        # self._filter_msg(bus_name, msg_name)
        return self.ipdu.check(msg_signals_obj,
                               signal_name,
                               sig_value_name,
                               timeout,
                               do_assert=do_assert,
                               check_time=check_time,
                               check_ub=check_ub)
    
    def filter_msg(self, bus_name: str, msg_name: str):
        self.bus_app.filter_msg(bus_name, msg_name)

    def filter_bus(self, bus_name: str):
        self.bus_app.filter_bus(bus_name)

    def filter_msg_all(self):
        self.bus_app.filter_msg_all()

    def cancel_filter_msg(self, bus_name: str, msg_name: str):
        self.bus_app.cancel_filter_msg(bus_name, msg_name)

    def cancel_filter_bus(self, bus_name: str):
        self.bus_app.cancel_filter_bus(bus_name)

    def cancel_filter_msg_all(self):
        self.bus_app.cancel_filter_msg_all()

    def cancel_fr_filter_msg_all(self):
        self.bus_app.cancel_fr_filter_msg_all()

    def cancel_can_filter_msg_all(self):
        self.bus_app.cancel_can_filter_msg_all()
    
    # def filter_msg(self, bus_name: str, msg_name: str):
    #     self._filter_msg(bus_name, msg_name)
    
    # # def filter_diag_msg(self, bus_name: str, msg_name: str):
    # #     i = 0x600  #  to do

    # #     self._filter_msg(bus_name, msg_name)

    # def filter_bus(self, bus_name: str):
    #     self._filter_msg(bus_name, 0)

    # def filter_msg_all(self):
    #     for bus_name in self.bus_app.tosun_busname:
    #         self.filter_bus(bus_name)
    #         # if bus_name not in ["bodyalmcanfd1", "bodyalmcanfd2"]:
    #         #     self.filter_bus(bus_name)
    #         #     logger.info(f"{bus_name} filter_msg_all") 
    #     for bus_name in self.bus_app.tosun_busname_tc1034:
    #             self.filter_bus(bus_name)

    # def cancel_filter_msg(self, bus_name: str, msg_name: str):
    #     self._filter_msg(bus_name, msg_name, filter_type=0)

    # def cancel_filter_bus(self, bus_name: str):
    #     # pdu_info = self.ipdu.bus_pdu_dict.get(bus_name)
    #     # for msg_name in pdu_info.keys():
    #     #     self.cancel_filter_msg(bus_name, msg_name)
    #     self._filter_msg(bus_name, 0, filter_type=0)

    # def cancel_filter_msg_all(self):
    #     for bus_name in self.bus_app.tosun_busname:
    #         self.cancel_filter_bus(bus_name)
    #     for bus_name in self.bus_app.tosun_busname_tc1034:
    #         self.cancel_filter_bus(bus_name)

    # def cancel_fr_filter_msg_all(self):
    #     self.bus_app.bus_dict["tosun_tc1034"].clear_fr_all_filter()

    # def cancel_can_filter_msg_all(self):
    #     self.bus_app.bus_dict["tosun_tc1018"].clear_can_all_filter()
    
    def check_sig_from_pdu(self,
                           bus_name: str,
                           msg_name: str,
                           signal_name: str,
                           sig_value_name: Union[str, int],
                           pdu_data: list,
                           do_assert=True):
        bus_obj = getattr(self.ipdu, bus_name)
        msg_signals_obj = getattr(bus_obj, msg_name)
        return self.ipdu.check_sig_from_pdu(msg_signals_obj,
                                            signal_name,
                                            sig_value_name,
                                            pdu_data,
                                            do_assert=do_assert)

    def check_crc_from_pdu(self, bus_name: str, msg_name: str, signal_name: str, pdu_data: list, do_assert=True):
        bus_obj = getattr(self.ipdu, bus_name)
        msg_signals_obj = getattr(bus_obj, msg_name)
        return self.ipdu.check_crc_from_pdu(msg_signals_obj,
                                            signal_name,
                                            pdu_data,
                                            do_assert=do_assert)

    def check_signal_thread_start(
            self,
            bus_name: str,
            msg_name: str,
            signal_name: str,
            timeout: Union[float, int] = 5,
            do_print=False,
    ) -> None:
        bus_obj = getattr(self.ipdu, bus_name)
        msg_signals_obj = getattr(bus_obj, msg_name)
        return self.ipdu.check_signal_thread_start(msg_signals_obj, signal_name, timeout, do_print)

    def check_signal_thread_stop(self, signal_name, timeout=30) -> bool:
        return self.ipdu.check_signal_thread_stop(signal_name, timeout)

    def check_thread_start(
            self,
            bus_name: str,
            msg_name: str,
            signal_name: str,
            sig_value: Union[str, int],
            timeout: Union[float, int] = 5,
            do_assert=False,
            check_time=1,
    ):
        bus_obj = getattr(self.ipdu, bus_name)
        msg_signals_obj = getattr(bus_obj, msg_name)
        return self.ipdu.check_thread_start(msg_signals_obj, signal_name, sig_value, timeout, do_assert, check_time)

    def check_thread_stop(self, signal_name, timeout=30):
        return self.ipdu.check_thread_stop(signal_name, timeout)

    def check_multiple_signals_thread_start(
            self,
            multiple_signals_info: List[Tuple[str, str, str, Union[str, int]]],
            timeout: Union[float, int] = 5,
            do_assert=False,
            check_time=1
    ) -> None:
        multiple_signals_info_new = []
        for bus_name, msg_name, signal_name, signal_value in multiple_signals_info:
            bus_obj = getattr(self.ipdu, bus_name)
            msg_signals_obj = getattr(bus_obj, msg_name)
            multiple_signals_info_new.append([msg_signals_obj, signal_name, signal_value])
        return self.ipdu.check_multiple_signals_thread_start(multiple_signals_info_new, timeout, do_assert, check_time)

    def check_multiple_signals_thread_stop(self, message_name, timeout=30) -> bool:
        return self.ipdu.check_multiple_signals_thread_stop(message_name, timeout)

    def clear_all_bus_buffer(self):
        self.ipdu.rx_flag_reset_all()

    def clear_bus_buffer(self, bus_name):
        self.ipdu.rx_flag_reset_bus(bus_name)

    def clear_bus_id_buffer(self, bus_name, msgid: Union[str, int]):
        '''
        清空总线上 某个id 报文的缓存
        @param bus_name:
        @param msgid:
        @return:
        '''
        self.ipdu.rx_flag_reset_msg(bus_name, msgid)

    def send_pdu_d(self, bus_name: str, msg_id: Union[str, int], data: list, cycle_time=None):
        """
        目前适配了同星的 can和fr

        :param bus_name: 总线名称 sucn as "bodycan"
        :param msg_id: can ID 或 FR slot_id
        :param data: 报文数据 such as [0x11, 0x22, 0x33, 0x44]
        :param cycle_time: can报文循环周期,发单帧可不用填； FR报文的cyclecode, cyclecode = BaseCycle + CycleRepetition
        :returns:
        :raises keyError: ValueError
        """
        if bus_name == "backbonefr":
            if cycle_time is None:
                raise ValueError(
                    "请给FR cycle_time 参数赋值，cycle_time即为cyclecode， cyclecode = BaseCycle + CycleRepetition")
            else:
                self.bus_app.bus_dict["tosun_tc1034"].fr_send(slot_id=msg_id, cyclecode=cycle_time, data=data)
        elif "can" in bus_name:
            self.bus_app.bus_dict["tosun_tc1018"].can_send(bus_name, data, msg_id, cycle_time)

    def pause_cycle_tx_rx_d(self, bus_type="All"):
        # logger.info(f"暂停 {bus_type} cycle_tx_rx")
        if bus_type == "All":
            self.bus_app.bus_dict["tosun_tc1034"].pause_cycle_tx_rx()
            self.bus_app.bus_dict["tosun_tc1018"].pause_cycle_tx_rx()
        elif bus_type == "FR":
            self.bus_app.bus_dict["tosun_tc1034"].pause_cycle_tx_rx()
        elif bus_type == "CAN":
            self.bus_app.bus_dict["tosun_tc1018"].pause_cycle_tx_rx()
        elif bus_type == "LIN":
            pass  # to do
        else:
            logger.warning(f"暂停 bus_type({bus_type}) cycle_tx_rx 失败,输入的bus_type不符合规范")

    def resume_cycle_tx_rx_d(self, bus_type="All"):
        # logger.info(f"恢复 {bus_type} cycle_tx_rx")
        if bus_type == "All":
            self.bus_app.bus_dict["tosun_tc1034"].resume_cycle_tx_rx()
            self.bus_app.bus_dict["tosun_tc1018"].resume_cycle_tx_rx()
        elif bus_type == "FR":
            self.bus_app.bus_dict["tosun_tc1034"].resume_cycle_tx_rx()
        elif bus_type == "CAN":
            self.bus_app.bus_dict["tosun_tc1018"].resume_cycle_tx_rx()
        elif bus_type == "LIN":
            pass  # to do
        else:
            logger.warning(f"恢复 bus_type({bus_type}) cycle_tx_rx 失败, 输入的bus_type不符合规范")

    def send_pdu(
            self, bus_name: str, msg_id: Union[str, int], data: Union[str, list], cycle_time=None
    ):
        '''
        发送总线数据
        @param bus_name: 总线名称
        @param msg_id: 报文id
        @param data: 报文内容，16进制字符串('1001')，或者列表[0x10,0x01]
        @param cycle_time: 周期
        @return:
        '''
        if isinstance(data, str):
            data_string = data.strip().replace(' ', '')
            data = [int(data_string[i:i + 2], 16) for i in range(0, len(data_string), 2)]
        self.ipdu.send_pdu(bus_name, msg_id, data, cycle_time)

    def stop_send_pdu(self, bus_name: str, id: Union[str, int]):
        '''
        # 针对的是 can bus,停止发送报文
        @param bus_name: 名字
        @param id: 报文id
        @return:
        '''
        self.ipdu.stop_send_pdu(bus_name, id)

    def recv_pdu(self, bus_name, id: Union[str, int], timeout=5):
        '''
        接收指定通道指定id的报文
        @param bus_name: 总线名称
        @param id: 报文id
        @param timeout: 接收超时时间
        @return: 返回一个元组 (id, time_stamp, length, data) 或者 None
        '''
        return self.ipdu.recv_pdu(bus_name, id, timeout)

    def pause_ecu_send(self, bus_name: str, ecu_name: str):
        '''
        暂停 bus 发送数据
        @param bus_name: 通道名称
        @return:
        '''
        self.ipdu.pause_ecu_send(bus_name, ecu_name)

    def pause_bus_send(self, bus_name: str):
        '''
        暂停 bus 发送数据
        @param bus_name: 通道名称
        @return:
        '''
        self.ipdu.pause_bus_send(bus_name)

    def pause_all_bus_send(self):
        '''
        暂停所有 通道发送数据
        @return:
        '''
        self.ipdu.pause_all_bus_send()

    def resume_bus_send(self, bus_name: str):
        '''
        继续发送 数据
        #  can bus  需要做2s的等待以确保所有的报文都恢复
        #  FR bus 需要做200ms 的等待以确保所有的报文都恢复
        @param bus_name:
        @return:
        '''
        self.ipdu.resume_bus_send(bus_name)

    def resume_all_bus_send(self):
        '''
        继续发送 数据
        # 目前只针对的是 can bus  ,  需要做2s的等待以确保所有的报文都恢复
        @return:
        '''
        self.ipdu.resume_all_bus_send()

    def resume_send_pdu(self, bus_name: str, id: Union[str, int]):
        '''
        继续发送
        @param bus_name:
        @param id:
        @return:
        '''
        self.ipdu.resume_send_pdu(bus_name, id)

    def wakeup_lin1(self, **kwargs):
        '''
        唤醒 lin 1  用车速唤醒，  维持原来的状态
        要防止 fr 休眠，要先发送can 报文维持
        @param kwargs:
        @return:
        '''
        self.ipdu.lin1_wakeup(**kwargs)

    def recovery_wakeup_lin1_precondition(self, **kwargs):
        '''
        恢复 唤醒 lin1  环境
        @param kwargs:
        @return:
        '''
        self.ipdu.lin1_reset_wakeup(**kwargs)

    def wakeup_lin2(self, **kwargs):
        '''
       非0 一直唤醒
       在 usagemode=0 唤醒 lin 2  仿真发送FR::VDDM::VDDMBackBoneSignalIPdu29::DCChrgnHndlSts=2
       要防止 fr 休眠，要先发送can 报文维持

       sig_value_table = {'OnBdChrgrHndlSts_Disconnected': 0,
       'OnBdChrgrHndlSts_ConnectedWithoutPower': 1,
        'OnBdChrgrHndlSts_PowerAvailableButNotActivated': 2,
        'OnBdChrgrHndlSts_ConnectedWithPower': 3,
        'OnBdChrgrHndlSts_Init': 4, 'OnBdChrgrHndlSts_Fault': 5}

       @param kwargs:
       @return:
       '''
        self.ipdu.lin2_wakeup(**kwargs)

    def recovery_wakeup_lin2_precondition(self, **kwargs):
        '''
        恢复 唤醒 lin2  环境
        @param kwargs:
        @return:
        '''
        self.ipdu.lin2_reset_wakeup(**kwargs)

    def wakeup_lin3(self, partner, dk):
        '''
        长时间唤醒 切模式
        partner = S2sBaseClass([("VehicleModeService", "client")])
        dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        @param kwargs:
        @return:
        '''
        self.ipdu.lin3_wakeup(partner, dk)

    def recovery_wakeup_lin3_precondition(self, partner, dk):
        '''
        partner = S2sBaseClass([("VehicleModeService", "client")])
        dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        @param partner:
        @param dk:
        @return:
        '''
        self.ipdu.lin3_reset_wakeup(partner, dk)

    def wakeup_lin4(self, **kwargs):
        '''
        唤醒 lin 4  用车速唤醒，  维持原来的状态

        要防止 fr 休眠，要先发送can 报文维持
        @param kwargs:
        @return:
        '''
        self.ipdu.lin4_wakeup(**kwargs)

    def recovery_wakeup_lin4_precondition(self, **kwargs):
        '''
        恢复 lin4 唤醒
        @param kwargs:
        @return:
        '''
        self.ipdu.lin4_reset_wakeup(**kwargs)

    def wakeup_lin5(self, **kwargs):
        '''
        唤醒 lin 5

        @param kwargs:
        @return:
        '''
        self.ipdu.lin5_wakeup(**kwargs)

    def recovery_wakeup_lin5_precondition(self, **kwargs):
        '''
        恢复 lin5 唤醒
        @param kwargs:
        @return:
        '''
        self.ipdu.lin5_reset_wakeup(**kwargs)

    def wakeup_lin6(self, **kwargs):
        '''
        唤醒 lin 6

        @param kwargs:
        @return:
        '''
        self.ipdu.lin6_wakeup(**kwargs)

    def recovery_wakeup_lin6_precondition(self, **kwargs):
        '''
        恢复 lin6 唤醒
        @param kwargs:
        @return:
        '''
        self.ipdu.lin6_reset_wakeup(**kwargs)

    def wakeup_all_lin(self, partner, dk):
        '''
        partner = S2sBaseClass([("VehicleModeService", "client")])
        dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)

        唤醒所有lin 通道
        lin1       车速唤醒  或者 driving
        lin2 非0 一直唤醒  driving  或者 在0 下 1、仿真发送FR::VDDM::VDDMBackBoneSignalIPdu29::DCChrgnHndlSts=2
        lin3 非0 一直唤醒  driving 或者  必须切模式
        lin4 非0 一直唤醒  driving  或者 车速唤醒  driving
        lin5
        lin6 非0 一直唤醒  driving 或者 仿真低压LVEEM signal BattSnsrStsReq == 1

        设置车速 和 切换模式 会唤醒所有通道
        @return:
        '''
        self.ipdu.lin_wakeup(partner, dk)

    def recovery_wakeup_all_lin_precondition(self, partner, dk, **kwargs):
        '''
        partner = S2sBaseClass([("VehicleModeService", "client")])
        dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        复位所有lin 通道
        @return:
        '''
        self.ipdu.lin_reset_wakeup(partner, dk)

    def send_nfc_cmd(self, key_id: Union[int, None] = None):
        return self.dk.send_nfc_cmd(key_id=key_id)

    def set_vehspd_gear(self, vehspd: Union[int, float] = 0.0, gear: Union[Gear, None] = None):
        if gear == None:
            with allure.step(f"设置车速为{vehspd}"):
                logger.info(f"设置车速为{vehspd}")
        else:
            with allure.step(f"设置车速为{vehspd},设置挡位为{gear.name}"):
                logger.info(f"设置车速为{vehspd},设置挡位为{gear.name}")
        self.set("backbonefr", "BcmVddmBackBoneFr06", 'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06', vehspd)
        self.set("backbonefr", "BcmVddmBackBoneFr06", 'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06', 3)
        if vehspd > 0 and gear == None:
            self.set_gear_pos(Gear.Drv)
            self.set("backbonefr", "VddmBackBoneFr18", 'TrsmParkLockdTrsmParkLockd', 1)

        elif vehspd == 0 and gear == None:
            self.set_gear_pos(Gear.Park)
            self.set("backbonefr", "VddmBackBoneFr18", 'TrsmParkLockdTrsmParkLockd', 0)

    def set_gear_pos(self, gear: Gear, parklock=ParkLockSts.ParkEngd):
        prompt_info = f"----------> 设置车辆挡位为:{gear.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.set("propulsioncan", "EcmPropFr24", 'GearLvrIndcn', gear.value)
            self.set("chassiscan2", "EcmChas2Fr07", 'GearLvrIndcn', gear.value)
            self.set("backbonefr", "VddmBackBoneFr03", 'GearLvrIndcn', gear.value)
            if parklock is not None:
                self.set("propulsioncan", "EcmPropComFr10", 'TrsmParkLockdTrsmParkLockd', parklock.value)
                self.set("backbonefr","VddmBackBoneFr18", 'TrsmParkLockdTrsmParkLockd', parklock.value)
            expectedvalue0 = self.ipdu.get_recent_signal_raw_value(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn')
            expectedvalue = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn')
            expectedvalue1 = self.ipdu.get_recent_signal_raw_value(self.ipdu.chassiscan2.EcmChas2Fr07, 'GearLvrIndcn')

            logger.info(f"获取实际的propulsioncan总线上的挡位值为:{expectedvalue0}")
            logger.info(f"获取实际的backbonefr总线上的挡位值为:{expectedvalue}")
            logger.info(f"获取实际的chassiscan2总线上的挡位值为:{expectedvalue1}")
            assert expectedvalue == gear.value   
    def check_extr_mirr_adj_req(self, viewPos: ViewPos, req: MirrDirReq, timeout=3):
        if viewPos == ViewPos.RearLeft:
            self.check("bodycan", "CEMBodyFr13", 'DrvrExtrMirrAdjHmiReq', req.value, timeout=timeout)
        elif viewPos == ViewPos.RearRight:
            self.check("bodycan", "CEMBodyFr13", 'PassExtrMirrAdjHmiReq', req.value, timeout=timeout)
        elif viewPos == ViewPos.All:
            self.check("bodycan", "CEMBodyFr13", 'DrvrExtrMirrAdjHmiReq', req.value, timeout=timeout)
            self.check("bodycan", "CEMBodyFr13", 'PassExtrMirrAdjHmiReq', req.value, timeout=timeout)

    def set_windows_position(self, pos_drvr: Union[WinPos, None] = None, pos_pass: Union[WinPos, None] = None,
                             pos_lere: Union[WinPos, None] = None, pos_rire: Union[WinPos, None] = None):
        with allure.step("通过总线模拟窗户的状态"):
            if pos_drvr is not None:
                logger.info(f"--------->模拟主驾窗户状态为{pos_drvr.name}")
                self.set("bodycan", "DdmBodyFr04", 'WinPosnStsAtDrvr', pos_drvr.value)
            if pos_pass is not None:
                logger.info(f"--------->模拟副驾窗户状态为{pos_pass.name}")
                self.set("bodycan", "PdmBodyFr01", 'WinPosnStsAtPass', pos_pass.value)
            if pos_lere is not None:
                logger.info(f"--------->模拟左后窗户状态为{pos_lere.name}")
                self.set("bodycan", "RldmBodyFr01", 'WinPosnStsAtReLe', pos_lere.value)
            if pos_rire is not None:
                logger.info(f"--------->模拟右后窗户状态为{pos_rire.name}")
                self.set("bodycan", "RrdmBodyFr01", 'WinPosnStsAtReRi', pos_rire.value)
    
    def set_four_windows_position(self,pos:WinPos,time_wait: Union[float, int] = 0):
        promt_info = f"--------------->同时设置4个窗户的位置为：{pos.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.set_windows_position(pos_drvr = pos, pos_pass=pos, pos_lere=pos, pos_rire=pos)
        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)
            
    def check_alrm_sts_req(self, alrm_sts: AlrmSts):
        with allure.step(f"检查AlrmStsAlrmSt是否为{alrm_sts.name}"):
            logger.info(f"检查AlrmStsAlrmSt是否为{alrm_sts.name}")
            self.check("backbonefr", "CemBackBoneFr18", 'AlrmStsAlrmSt', alrm_sts.value)

    def check_active_indicator_lamp_req(self, indcr_sts: IndcrSts, timeout=5):
        with allure.step(f"检查闪灯请求信号ActvnOfIndcrIndcrOut是否为{indcr_sts.name}"):
            logger.info(f"检查闪灯请求信号ActvnOfIndcrIndcrOut是否为{indcr_sts.name}")
            self.check("bodycan", "CemBodyFr03", 'ActvnOfIndcrIndcrOut', indcr_sts.value, timeout)

    def get_active_indicator_lamp_req_data(self, timeout=5):
        with allure.step(f"获取闪灯请求信号ActvnOfIndcrIndcrOut{timeout}秒内打原始数据"):
            logger.info(f"获取闪灯请求信号ActvnOfIndcrIndcrOut{timeout}秒内打原始数据")
            return (self.ipdu.check_signal(self.ipdu.bodycan.CemBodyFr03, 'ActvnOfIndcrIndcrOut'))

    def set_door_lock_sts(self, drv_lock: Union[Locksts, None] = None, pass_lock: Union[Locksts, None] = None,
                          lere_lock: Union[Locksts, None] = None, rire_lock: Union[Locksts, None] = None):
        if drv_lock is not None:
            logger.info(f"设置主驾位锁的状态为{drv_lock}")
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'DoorDrvrLockSts', drv_lock.value)
        if pass_lock is not None:
            logger.info(f"设置副驾位锁的状态为{pass_lock}")
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'DoorPassLockSts', pass_lock.value)
        if lere_lock is not None:
            logger.info(f"设置左后锁的状态为{lere_lock}")
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'DoorLeReLockSts', lere_lock.value)
        if rire_lock is not None:
            logger.info(f"设置右后锁的状态为{rire_lock}")
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'DoorRiReLockSts', rire_lock.value)
            
    # def set_four_doors_lock_sts(self, lock_sts: Locksts):
    #     logger.info(f"同时设置4门锁的状态为{lock_sts}")
    #     self.set_door_lock_sts(drv_lock=lock_sts, pass_lock=lock_sts, rire_lock=lock_sts, lere_lock=lock_sts)

    def set_five_door_opener_sts(self, door_opener: DoorOpenerSts):
        logger.info(f"同时设置5门的开关状态为{door_opener.name}")
        self.set_door_opener_sts(drv_opener=door_opener, pass_opener=door_opener, lere_opener=door_opener,
                                 rire_opener=door_opener, tr_opener=door_opener)

    def set_four_door_opener_sts(self, door_opener: DoorOpenerSts):
        logger.info(f"同时设置5门的开关状态为{door_opener.name}")
        self.set_door_opener_sts(drv_opener=door_opener, pass_opener=door_opener, lere_opener=door_opener,
                                 rire_opener=door_opener)

    def set_door_opener_sts(self, drv_opener: Union[DoorOpenerSts, None] = None,
                            pass_opener: Union[DoorOpenerSts, None] = None,
                            lere_opener: Union[DoorOpenerSts, None] = None,
                            rire_opener: Union[DoorOpenerSts, None] = None,
                            tr_opener: Union[DoorOpenerSts, None] = None):
        with allure.step(f"设置五门的开关状态"):
            if drv_opener is not None:
                logger.info(f"设置主驾位门的开关状态为{drv_opener.name}")
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorOpenerDrvrSts_0_DpodBodySignalIPdu01',
                              drv_opener.value)
            if pass_opener is not None:
                logger.info(f"设置副驾驶位门的开关状态为{pass_opener.name}")
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorOpenerPassSts_0_PpodBodySignalIPdu01',
                              pass_opener.value)
            if lere_opener is not None:
                logger.info(f"设置左后门的开关状态为{lere_opener.name}")
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorOpenerLeReSts_0_LpodBodySignalIPdu01',
                              lere_opener.value)
            if rire_opener is not None:
                logger.info(f"设置右后门的开关状态为{rire_opener.name}")
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorOpenerRiReSts_0_RpodBodySignalIPdu01',
                              rire_opener.value)
            if tr_opener is not None:
                logger.info(f"设置尾门的开关状态为{tr_opener.name}")
                self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts_0_PotBodySignalIPdu02', tr_opener.value)

    def check_door_opener_req(self, drv_opener: Union[DoorPos, None] = None,
                              pass_opener: Union[DoorPos, None] = None,
                              lere_opener: Union[DoorPos, None] = None,
                              rire_opener: Union[DoorPos, None] = None,
                              tr_opener: Union[DoorPos, None] = None,
                              door_req: DoorOpenerReq = DoorOpenerReq.Idle,
                              trigger_src: Union[None, LockTrigerSource] = None,
                              timeout: Union[float, int] = 1
                              ):
        target_msg78 = self.ipdu.bodycan.CemBodyFr78
        target_msg79 = self.ipdu.bodycan.CemBodyFr79
        target_msg02 = self.ipdu.bodycan.CemBodyFr02
        with allure.step(f"Check BGM 发出的电动门的开关请求"):
            if drv_opener is not None:
                if trigger_src is not None:
                    logger.info(f"Check主驾位门的开关请求是否为{door_req.name}，触发源是否为{trigger_src.name}")
                    self.ipdu.check_multiple_signals([(target_msg78, 'DoorOpenerDrvrReqDoorOpenerReq2', door_req.value),
                                                      (target_msg78, 'DoorOpenerDrvrReqTrigSrc', trigger_src.value)],
                                                     timeout=timeout)
                else:
                    logger.info(f"Check主驾位门的开关请求是否为{door_req.name}")
                    self.ipdu.check(target_msg78, 'DoorOpenerDrvrReqDoorOpenerReq2', door_req.value, timeout)
            if pass_opener is not None:
                if trigger_src is not None:
                    logger.info(f"Check副驾位门的开关请求是否为{door_req.name}，触发源是否为{trigger_src.name}")
                    self.ipdu.check_multiple_signals([(target_msg79, 'DoorOpenerPassReqDoorOpenerReq2', door_req.value),
                                                      (target_msg79, 'DoorOpenerPassReqTrigSrc', trigger_src.value)],
                                                     timeout=timeout)
                else:
                    logger.info(f"Check副驾位门的开关请求是否为{door_req.name}")
                    self.ipdu.check(target_msg79, 'DoorOpenerPassReqDoorOpenerReq2', door_req.value, timeout)
            if lere_opener is not None:
                if trigger_src is not None:
                    logger.info(f"Check左后门的开关请求是否为{door_req.name}，触发源是否为{trigger_src.name}")
                    self.ipdu.check_multiple_signals([(target_msg78, 'DoorOpenerLeReReqDoorOpenerReq2', door_req.value),
                                                      (target_msg78, 'DoorOpenerLeReReqTrigSrc', trigger_src.value)],
                                                     timeout=timeout)
                else:
                    logger.info(f"Check左后门的开关请求是否为{door_req.name}")
                    self.ipdu.check(target_msg78, 'DoorOpenerLeReReqDoorOpenerReq2', door_req.value, timeout)
            if rire_opener is not None:
                if trigger_src is not None:
                    logger.info(f"Check右后门的开关请求是否为{door_req.name}，触发源是否为{trigger_src.name}")
                    self.ipdu.check_multiple_signals([(target_msg79, 'DoorOpenerRiReReqDoorOpenerReq2', door_req.value),
                                                      (target_msg79, 'DoorOpenerRiReReqTrigSrc', trigger_src.value)],
                                                     timeout=timeout)
                else:
                    logger.info(f"Check右后门的开关请求是否为{door_req.name}")
                    self.ipdu.check(target_msg79, 'DoorOpenerRiReReqDoorOpenerReq2', door_req.value, timeout)
            if tr_opener is not None:
                if trigger_src is not None:
                    logger.info(f"Check尾门的开关请求是否为{door_req.name}，触发源是否为{trigger_src.name}")
                    self.ipdu.check_multiple_signals([(target_msg02, 'TrOpenerReqTrOpenerReq', door_req.value),
                                                      (target_msg02, 'TrOpenerReqTrigSrc', trigger_src.value)],
                                                     timeout=timeout)
                else:
                    logger.info(f"Check尾门的开关请求是否为{door_req.name}")
                    self.ipdu.check(target_msg02, 'TrOpenerReqTrOpenerReq', door_req.value, timeout)

    def check_four_door_opener_req(self, door_req: DoorOpenerReq, trigger_src: Union[None, LockTrigerSource] = None,
                                   timeout: Union[float, int] = 1):
        if trigger_src is not None:
            logger.info(f"同时Check 4门的开关请求是否为{door_req.name}，触发源是否为{trigger_src.name}")
        else:
            logger.info(f"同时Check 4门的开关请求是否为{door_req.name}")

        self.check_door_opener_req(drv_opener=DoorPos.Dirver, pass_opener=DoorPos.Pass, lere_opener=DoorPos.RearLeft,
                                   rire_opener=DoorPos.RearRight,
                                   door_req=door_req, trigger_src=trigger_src)

    # def check_door_opener_move_sts(self, door_pos: DoorPos, door_req: DoorOpenerMoveSts,
    #                                timeout: Union[float, int] = 1):
    #     if door_pos.name == "Dirver":
    #         logger.info(f"Check主驾位门的运动请求是否为{door_req.name}")
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr10, 'DoorOpenerDrvrSts', door_req.value, timeout)
    #     elif door_pos.name == "Pass":
    #         logger.info(f"Check副驾位门的运动请求是否为{door_req.name}")
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr10, 'DoorOpenerPassSts', door_req.value, timeout)
    #     elif door_pos.name == "RearLeft":
    #         logger.info(f"Check左后门的运动请求是否为{door_req.name}")
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr10, 'DoorOpenerLeReSts', door_req.value, timeout)
    #     elif door_pos.name == "RearRight":
    #         logger.info(f"Check右后门的运动请求是否为{door_req.name}")
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr10, 'DoorOpenerRiReSts', door_req.value, timeout)

    def check_central_lock_sts(self, exp_sts: CenLockSts, exp_trigsrc: Union[None, LockTrigerSource] = None, timeout=1):
        if exp_trigsrc is not None:
            hint = f"校验中控锁状态={exp_sts.name} + Trigger={exp_trigsrc.name}"
        else:
            hint = f"校验中控锁状态={exp_sts.name} + 不需要检查触发源"
        with allure.step(hint):
            logger.info(hint)
            # target_msg = self.ipdu.connectivitycanfd.VgmConnFr12
            target_msg = self.ipdu.backbonefr.CemBackBoneFr06   
            if exp_trigsrc is not None:
                return (self.ipdu.check_multiple_signals([(target_msg, 'LockgCenStsLockSt', exp_sts.value),
                                                          (target_msg, 'LockgCenStsTrigSrc', exp_trigsrc.value)],
                                                         timeout=timeout)
                        )
            else:
                return self.ipdu.check(target_msg, 'LockgCenStsLockSt', exp_sts.value, timeout=timeout)

    def get_central_lock_sts(self, timeout=2):
        expectedvalue = self.ipdu.get_recent_signal_raw_value(self.ipdu.connectivitycanfd.VgmConnFr12,
                                                              'LockgCenStsLockSt')
        logger.info("获取中控锁状态为: expectedvalue {}".format(expectedvalue))
        return expectedvalue

    def check_wipg_spd_info(self, wip_spd_info: WipgSpdInfo, timeout=2):
        with allure.step(f"Check 雨刮模式信息是否为{wip_spd_info.name}"):
            logger.info(f"Check 雨刮模式信息是否为{wip_spd_info.name}")
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr07, 'WipgInfoWipgSpdInfo', wip_spd_info.value, timeout)

    def check_wiper_wash_req(self, wash_req: WashReq, timeout=2):
        with allure.step(f"Check 雨刮清洗请求是否为{wash_req.name}"):
            logger.info(f"Check 雨刮清洗请求是否为{wash_req.name}")
            self.ipdu.check(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WshrLvrPosnSafe', wash_req.value, timeout)

    def check_wiper_without_wash_req(self, timeout=5):
        with allure.step(f"Check 在条件不满足的情况下BGM不发送打开雨刮清洗请求"):
            logger.info(f"Check 在条件不满足的情况下BGM不发送打开雨刮清洗请求")
            ori_data = self.ipdu.check_signal(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WshrLvrPosnSafe', timeout)
            logger.info(f"获取{timeout}秒内的WshrLvrPosnSafe原始数据是:{ori_data}")
            check_result = check_all_value_is(ori_data, 1)
            logger.info(f"Check 结果是：{check_result}")
            assert check_result

    def check_wiper_rain_sensor_active_req(self, rain_sensor_act_req: RainSensorAct, timeout=5):
        with allure.step(f"Check 雨量传感器激活请求信号值{rain_sensor_act_req.name}"):
            logger.info(f"Check 雨量传感器激活请求信号值{rain_sensor_act_req.name}")
            self.ipdu.check(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'RainSensActvn', rain_sensor_act_req.value, timeout)

    def check_wiper_without_rain_sensor_active_req(self, timeout=5):
        with allure.step(f"Check 条件不满足的情况下BGM不发生雨量传感器激活请求"):
            logger.info(f"Check 条件不满足的情况下BGM不发生雨量传感器激活请求")
            self.ipdu.check(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'RainSensActvn', RainSensorAct.Off, timeout)

    def set_low_volt_power_supply(self):
        with allure.step(f"设置低压补电开启"):
            logger.info(f"设置低压补电开启")
            self.ipdu.send_pdu("cem_lin6", 0x06, [0x0, 0x7C, 0x00, 0xFF, 0xFF, 0xFF, 0xFF])

    def check_wiper_maintain_ser_pos_req(self, maintain_ser_req: MaintainPosReq, timeout=5):
        with allure.step(f"Check BGM发出的雨刮维修服务位置请求是否为{maintain_ser_req.name}"):
            logger.info(f"Check BGM发出的雨刮维修服务位置请求是否为{maintain_ser_req.name}")
            self.ipdu.check(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'WiprPosnForSrvReq', maintain_ser_req.value, timeout)

    def set_batterylow_mode(self, DCChrgnHndlSts: DCChrgnHndlSts, DispHvBattLvlOfChrg: float):
        with allure.step(f"设置充电枪状态为：{DCChrgnHndlSts.name}"):
                self.set('propulsioncan', 'BecmPropFr15', 'DCChrgnHndlSts', DCChrgnHndlSts.value)
                logger.info(f"设置充电枪状态为：{DCChrgnHndlSts.name}成功")
        with allure.step(f"设置电量低报警信息为:{DispHvBattLvlOfChrg}"):
            self.set('propulsioncan', 'EcmPropFr04', 'DispHvBattLvlOfChrg', DispHvBattLvlOfChrg)
            logger.info(f"设置电量低报警信息为:{DispHvBattLvlOfChrg}成功")

    def set_batter_sensor_hw_failure(self, BattSnsrHwFltRaw: BattSnsrHwFltRaw):
        with allure.step(f"设置电池硬件故障：{BattSnsrHwFltRaw.name}"):
            self.set('cem_lin6', 'BmsCem_Lin6Fr03', 'BattSnsrHwFltRaw', BattSnsrHwFltRaw.value)
            logger.info(f"设置电池硬件故障：{BattSnsrHwFltRaw.name}成功")

    def set_dcdc_battary_act_sts(self, DcDcActvd: DcDcActvd):
        with allure.step(f"设置高压电池为 {DcDcActvd.name} 状态"):
            self.set('backbonefr', 'VddmBackBoneFr08', 'DcDcActvd', DcDcActvd.value)
            logger.info(f"设置高压电池为 {DcDcActvd.name} 状态成功")

    def check_lv_power_supply_error_sts(self, LVPwrSplyErrSts: LVPwrSplyErrSts):
        with allure.step(f"检测低压电池供电 {LVPwrSplyErrSts.name} 情况"):
            self.check('backbonefr', 'CemBackBoneFr06', 'LVPwrSplyErrSts', LVPwrSplyErrSts.value)
            logger.info(f"检测低压电池供电 {LVPwrSplyErrSts.value} 情况成功")

    def set_sys_safty_battery_current(self, BattSftySigSysSaftyBattI: float):
        with allure.step(f"设置电池电流相关的系统安全状态"):
            self.set('cem_lin6', 'BmsCem_Lin6Fr01', 'BattSftySigSysSaftyBattI', BattSftySigSysSaftyBattI)
            logger.info(f"设置电池电流相关的系统安全状态成功")

    def set_sys_safty_battery_voltage(self, BattSftySigSysSaftyBattU: float):
        with allure.step(f"设置电池电压相关的系统安全状态"):
            self.set('cem_lin6', 'BmsCem_Lin6Fr01', 'BattSftySigSysSaftyBattU', BattSftySigSysSaftyBattU)
            logger.info(f"设置电池电压相关的系统安全状态成功")

    def set_engine_sts(self, EngSt1WdStsEngSt1WdSts: EngSt1WdStsEngSt1WdSts):
        with allure.step(f"设置发动机运行状态{EngSt1WdStsEngSt1WdSts.name}"):
            self.set('backbonefr', 'VddmBackBoneFr00', 'EngSt1WdStsEngSt1WdSts', EngSt1WdStsEngSt1WdSts.value)
            logger.info(f"设置发动机运行状态{EngSt1WdStsEngSt1WdSts.name}成功")

    def set_SOC_display_value(self, soc_value: Union[int, float]):
        with allure.step(f"设置高压电池显示的SOC值为{soc_value}"):
            if soc_value != 0:
                self.set('propulsioncan', 'EcmPropFr04', 'DispHvBattLvlOfChrg', soc_value)
                logger.info(f"设置高压电池显示的SOC值为{soc_value}成功")
            else:
                self.set_Hv_sys_relay_sts(sts=HvSysRelaySts.Close)
                self.set('propulsioncan', 'EcmPropFr04', 'DispHvBattLvlOfChrg', soc_value)
                logger.info(f"设置高压电池显示的SOC值为{soc_value}成功")

    def recv_pdu_d(self, bus_name, msg_id: int, tosun_tc1018, bus_chn, timeout=5):
        """
        目前适配了同星的 can和fr

        :param bus_name: 总线名称 sucn as "bodycan"
        :param msg_id: can ID 或 FR slot_id
        :param timeout: to do 暂无效
        :returns: (msg_id, time_stamp, length, data)
        :raises keyError:
        """
        # self._filter_msg(bus_name, msg_id)
        if bus_name == "backbonefr":
            Msg = self.bus_app.bus_dict["tosun_tc1034"].recv(msgid=msg_id)
        else:
            Msg = tosun_tc1018.recv(bus_chn=bus_chn, msgid=msg_id)

        return Msg
    
    def clear_recv_pdu_d_buffer(self, bus_name: str, timeout: float=1.0):
        """
        清除 recv_pdu_d_buffer, 暂只支持同星
        
        :param bus_name: str such as "backbonefr" "bodycan", can bus只需填任一 canbus 即可
        :param timeout: float 单位 秒   清缓存所需时间
        :returns: 
        :raises keyError: 
        """
        if bus_name == "backbonefr":
            Msg = self.bus_app.bus_dict["tosun_tc1034"].clear_recv_buffer(timeout)
        else:
            Msg = self.bus_app.bus_dict["tosun_tc1018"].clear_recv_buffer(timeout)

    def set_HV_SOC_value(self, soc_value: Union[int, float]):
        with allure.step(f"设置高压电池SOC值为{soc_value}"):
            self.set('propulsioncan', 'BecmPropFr03', 'HvBattSoc', soc_value)
            self.set('backbonefr', 'VddmBackBoneFr06', 'DispHvBattLvlOfChrg', soc_value)
            logger.info(f"设置高压电池SOC值为{soc_value}成功")


    def set_DC_charge_port_tmp(self, port: DCChrgnPort, tmp):
        with allure.step(f"设置DC充电口{port.name}温度为{tmp}"):
            self.set('propulsioncan', 'BecmPropFr11', f'DCChrgn{port.value}PortT', tmp)
            logger.info(f"设置DC充电口{port.name}温度为{tmp}成功")

    def check_low_sys_volt_warning(self, ULoWarnULoWarn: ULoWarnULoWarn):
        with allure.step(f"检测低压系统电压告警状态{ULoWarnULoWarn.name}"):
            self.check('backbonefr', 'CemBackBoneFr08', 'ULoWarnULoWarn', ULoWarnULoWarn.value)
            logger.info(f"检测低压系统电压告警状态{ULoWarnULoWarn.name}")

    def set_tailwing_pos(self, pos: TailWingPos):
        with allure.step(f"设置电动尾翼位置信息{pos.name}"):
            logger.info(f"设置电动尾翼位置信息{pos.name}")
            self.set('cem_lin6', 'AwmCem_Lin6Fr01', 'ActvReSplrPosn', pos.value)

    def check_tailwing_pos_req(self, pos: SetTailWingPos):
        with allure.step(f"Check BGM 发出设置尾翼位置请求是否为{pos.name}"):
            logger.info(f"Check BGM 发出设置尾翼位置请求是否为{pos.name}")
            self.check('cem_lin6', 'BgmCem_Lin6Fr01', 'ActvReSplrPosnCmd', pos.value, timeout=5)

    def get_vehicle_speed(self):
        expectedvalue = self.ipdu.get_recent_signal_raw_value(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06,
            'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06',
        )
        veh_spd = expectedvalue * 0.00391
        logger.info(f"获取的车速值为:{veh_spd}")
        return veh_spd

    def check_tailgate_opener_req(self, req: SetTailGatePos):
        with allure.step(f"Check BGM 发出设置尾门位置请求是否为{req.name}"):
            logger.info(f"Check BGM 发出设置尾门位置请求是否为{req.name}")
            self.check('bodycan', 'CemBodyFr02', 'TrOpenerReqTrOpenerReq', req.value)

    def check_steerwheel_heat_req(self, avl_sts: AvlSts, lev_sts: HeatLevel):
        with allure.step(f"Check BGM 方向盘加热相关的信号：功能可用状态{avl_sts.name}, 加热等级{lev_sts.name}"):
            logger.info(f"Check BGM 方向盘加热相关的信号：功能可用状态{avl_sts.name}, 加热等级{lev_sts.name}")
            self.check('connectivitycanfd', 'VgmConnFr03', 'SteerWhlHeatgAvlSts', avl_sts.value)
            self.check('backbonefr', 'CemBackBoneFr19', 'SteerWhlHeatgLvlSts', lev_sts.value)

    def set_Hv_sys_relay_sts(self, sts: HvSysRelaySts):
        with allure.step(f"设置高压继电器开关状态为{sts.name}"):
            logger.info(f"设置高压继电器开关状态为{sts.name}")
            self.set('backbonefr', 'VddmBackBoneFr06', 'HvSysRlyStsHvSysRlySts', sts.value)

    def set_blt_sts(self, seat_id: SeatId, blt_flt_sts: BltFltSts, blt_lock_sts: BltLockSts):
        with allure.step(f"设置{seat_id.name}座椅安全的故障状态为{blt_flt_sts.name},插入状态为{blt_lock_sts.name}"):
            logger.info(f"设置{seat_id.name}座椅安全的故障状态为{blt_flt_sts.name},插入状态为{blt_lock_sts.name}")
            if seat_id.name == "FrontLeft":
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', blt_flt_sts.value)

                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', blt_lock_sts.value)
            elif seat_id.name == "FrontRight":
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtPassBltLockSts', blt_flt_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtPassBltLockSt1', blt_lock_sts.value)
            elif seat_id.name == "FrontRow":
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', blt_flt_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', blt_lock_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtPassBltLockSts', blt_flt_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtPassBltLockSt1', blt_lock_sts.value)
            elif seat_id.name == "RearLeft":
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtRowSecLeBltLockSts', blt_flt_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtRowSecLeBltLockSt1', blt_lock_sts.value)
            elif seat_id.name == "RearMiddle":
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtRowSecMidBltLockSts', blt_flt_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtRowSecMidBltLockSt1', blt_lock_sts.value)
            elif seat_id.name == "RearRight":
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtRowSecRiBltLockSts', blt_flt_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtRowSecRiBltLockSt1', blt_lock_sts.value)
            elif seat_id.name == "RearRow":
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtRowSecLeBltLockSts', blt_flt_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtRowSecLeBltLockSt1', blt_lock_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtRowSecMidBltLockSts', blt_flt_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtRowSecMidBltLockSt1', blt_lock_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtRowSecRiBltLockSts', blt_flt_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtRowSecRiBltLockSt1', blt_lock_sts.value)
            elif seat_id.name == "All":
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', blt_flt_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', blt_lock_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtPassBltLockSts', blt_flt_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtPassBltLockSt1', blt_lock_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtRowSecLeBltLockSts', blt_flt_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtRowSecLeBltLockSt1', blt_lock_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtRowSecMidBltLockSts', blt_flt_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtRowSecMidBltLockSt1', blt_lock_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtRowSecRiBltLockSts', blt_flt_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                              'BltLockStAtRowSecRiBltLockSt1', blt_lock_sts.value)

    def set_seat_occpt_sts(self, seat_id: SeatId, seat_sts: Union[SeatOccptSts,DriverSeatOccptSts]):
        promt_info = f"设置{seat_id.name}座椅占位状态为{seat_sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if seat_id.name == "FrontLeft":
                self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr17,"DrvrSeatSts",seat_sts.value)
            elif seat_id.name == "FrontRight":
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts',seat_sts.value)
            elif seat_id.name == "FrontRow":
                self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr17,"DrvrSeatSts",seat_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts',seat_sts.value)
            elif seat_id.name == "RearLeft":
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe',seat_sts.value)
            elif seat_id.name == "RearMiddle":
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecMid',seat_sts.value)
            elif seat_id.name == "RearRight":
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecRi',seat_sts.value)
            elif seat_id.name == "RearRow":
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe',seat_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecMid',seat_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecRi',seat_sts.value)
            elif seat_id.name == "All":
                self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr17,"DrvrSeatSts",seat_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts',seat_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe',seat_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecMid',seat_sts.value)
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecRi',seat_sts.value)

    def set_usage_mode_to_tcam(self, usage_mode: UsageMode):
        with allure.step(f"模拟BGM通过connectivitycanfd发送UsageMode = {usage_mode.name}"):
            logger.info(f"模拟BGM通过connectivitycanfd发送UsageMode = {usage_mode.name}")
            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr01, "VehModMngtGlbSafe1UsgModSts", usage_mode.value)

    def set_car_mode_to_tcam(self, car_mode: CarMode):
        with allure.step(f"模拟BGM通过connectivitycanfd发送CarMode = {car_mode.name}"):
            logger.info(f"模拟BGM通过connectivitycanfd发送CarMode = {car_mode.name}")
            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr01, "VehModMngtGlbSafe1CarModSts1", car_mode.value)

    def set_night_mode(self,wait_time: Union[float, int] = 0):
        with allure.step(f"设置当前为夜晚模式"):
            logger.info("\033[0;35;40m设置RLSM夜晚模式\033[0m")
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawTwliBriRaw',
                          0)  # SUS光感-1000为白天-0-1000为夜晚;
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawQf', 3)  # SUS光感QF3
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'OutdBriSts', 1)
            sleep(wait_time)

    def set_day_mode(self,wait_time: Union[float, int] = 0):
        with allure.step(f"设置当前为白天模式"):
            logger.info("\033[0;35;40m设置RLSM白天模式\033[0m")
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawTwliBriRaw',
                          1000)  # SUS光感-1000为白天-0-1000为夜晚;
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawQf', 3)  # SUS光感QF3
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'OutdBriSts', 2)  # 输入控制灯自动打开关闭-0unknow-1夜晚打开-2白天;
            sleep(wait_time)

    def set_hvbatt(self,value:int):
        promt_info = f"--------------->设置HvBattLimnIndcn的值模拟热失控状态"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.set_singal("backbonefr", "VddmBackBoneFr18", "HvBattLimnIndcn",value)

    def check_low_beam_sts(self):
        pass

    def check_climate_ac_sts(self, sts: CoolgReq):
        promt_info = f"---------------->开始查看空调AC状态信号BodyCan:0x180:HmiCmptmtCoolgReq是否为{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.check("bodycan", "CEMBodyFr15", 'HmiCmptmtCoolgReq', sts.value)

    def set_vehspd(self, value=0):
        self.ipdu.set_vehspd(value)

    def send_msg_by_id_func(self, bus_name, msg_id, data, **kwargs):
        '''
        发送指定 id 的报文
        @param bus_name: 通道名称
        @param msg_id: msg id
        @param data: 发送数据内容，可以为列表（[0x10,0x01]），或者16进制字符传（1001）
        @return:
        '''
        if isinstance(data, list):
            send_data = data
        else:
            data = str(data).replace(" ", '').strip()
            send_data = [int(data[i:i + 2], 16) for i in range(0, len(data), 2)]

        self.send_pdu_d(bus_name, msg_id, send_data)
        # msg_hex = ' '.join([hex(i)[2:].zfill(2) for i in send_data])
        # logger.info(f"send》》{bus_name} send id={hex(msg_id)},data={msg_hex}")

    def recv_msg_by_id_func(self, bus_name, msg_id, timeout=3, **kwargs):
        '''
        在 当前通道接收指定id的报文，
        @param bus_name: 通道名称
        @param msg_id: id
        @param timeout: 接收超时时间
        @return:
        '''
        try:
            self.pause_cycle_tx_rx_d()
            bus_chn = self.bus_app.get_tosun_tc1018_can_chn(bus_name)
            tosun_tc1018 = self.bus_app.bus_dict["tosun_tc1018"]
            t = time.time()
            while time.time() - t < timeout:
            # while True:
                consecutive_frame_data_info = self.recv_pdu_d(bus_name, msg_id, tosun_tc1018, bus_chn, timeout=0.001)
                if consecutive_frame_data_info:
                    if "can" in bus_name:
                        msg_id = consecutive_frame_data_info[0]
                        recv_msg_id = hex(msg_id)
                        time_stamp = consecutive_frame_data_info[1]
                        recv_msg_data = consecutive_frame_data_info[3]
                        # msg_hex = ' '.join([hex(i)[2:].zfill(2) for i in recv_msg_data]) if recv_msg_data else None
                        # logger.info(f"recv》》{bus_name} recv id={recv_msg_id} data={msg_hex}time_stamp={time_stamp}")
                        if msg_id == 0x7ff and recv_msg_data[:3] == [0x02, 0x3e, 0x80]:
                            continue
                    elif "lin" in bus_name:
                        pass
                    else:
                        # fr 接收报文
                        pass
                    return recv_msg_data, time_stamp
            #
            logger.info(f"通道{bus_name} 接收{timeout}秒后未收到id为{hex(msg_id)}报文！！！")
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/buscomm.py")
            raise e
        finally:
            # self.resume_cycle_tx_rx_d()
            pass
        return None, None

    def recv_diag_request_msg(self, bus_name, request_id=0x712, response_id=0x612, bs=8, st=5, single_frame_len=None,
                              timeout=10):
        '''
        接收 can的请求报文
        @param bus_name: 通道名字
        @param request_id:  请求id
        @param response_id: 响应id
        @param bs: block
        @param st: st_min
        @return:
        '''
        can_single_frame_len = 8
        canfd_single_frame_len = 64

        if bus_name.endswith("canfd"):
            can_type = 1
        else:
            can_type = 0
        # single_frame_len w为 None 表示 can 就是8个字节，canfd 就是64个字节
        if single_frame_len is None:
            if can_type:
                single_frame_len = canfd_single_frame_len
            else:
                single_frame_len = can_single_frame_len
        # can的时候
        if single_frame_len == can_single_frame_len:
            # 接收首帧数据
            recv_first_data, time_stamp = self.recv_msg_by_id_func(bus_name, request_id, timeout=timeout)
            # 判断是不是多帧
            first_byte = recv_first_data[0]
            first_b = first_byte >> 4
            # 判断是否为 单帧，单帧接收完就返回
            if first_b != 1:
                logger.info("接收的数据为单帧")
                recv_msg_len = first_byte
                recv_msg_data = recv_first_data[1:recv_msg_len + 1]
                recv_padding = recv_first_data[recv_msg_len + 1:]
                # 返回 接收的数据，以及填充位置
                string_log = f"接收的数据填充位为{recv_padding} 报文为{recv_msg_data}"
                logger.info(string_log)
                return recv_msg_data, list(set(recv_padding)), time_stamp
        else:
            # 接收首帧数据
            recv_first_data, time_stamp = self.recv_msg_by_id_func(bus_name, request_id, timeout=timeout)
            # 判断是不是多帧
            first_byte = recv_first_data[0]
            if first_byte == 0:
                # canfd 的单帧，8-62个字节
                secod_byte = recv_first_data[1]
                logger.info("接收的数据为单帧")
                recv_msg_len = secod_byte
                recv_msg_data = recv_first_data[2:recv_msg_len + 2]
                recv_padding = recv_first_data[recv_msg_len + 2:]
                # 返回 接收的数据，以及填充位置
                string_log = f"接收的数据填充位为{recv_padding} 报文为{recv_msg_data}"
                logger.info(string_log)
                return recv_msg_data, list(set(recv_padding)), time_stamp
            first_b = first_byte >> 4
            # 判断是否为 单帧，单帧接收完就返回
            if first_b != 1:
                # 0-7个字节
                logger.info("接收的数据为单帧")
                recv_msg_len = first_byte
                recv_msg_data = recv_first_data[1:recv_msg_len + 1]
                recv_padding = recv_first_data[recv_msg_len + 1:]
                # 返回 接收的数据，以及填充位置
                string_log = f"接收的数据填充位为{recv_padding} 报文为{recv_msg_data}"
                logger.info(string_log)
                return recv_msg_data, list(set(recv_padding)), time_stamp

        # 数据为多帧
        logger.info("接收的数据为多帧")
        second_byte = recv_first_data[1]
        # 接收数据 总长度
        recv_msg_len = ((first_byte << 8) & 0x0f00) + second_byte
        # 存放所有的接收报文
        recv_msg_data = []
        # 第一帧报文
        recv_msg_data.extend(recv_first_data[2:])
        # 发送 流控帧
        flow_control_frame_count = 1
        flow_control_frame = [0x30, bs, st, 0, 0, 0, 0, 0]
        self.send_msg_by_id_func(bus_name, response_id, flow_control_frame)
        logger.info(f"bus_name {hex(response_id)}第{flow_control_frame_count}次发送流控帧数据》》{flow_control_frame}")
        # 连续帧头
        consecutive_frame_head = 0x21
        recv_padding = []
        recv_bs_index = 0
        t = time.time()

        while time.time() - t < timeout:
        # while True:
            consecutive_frame_data, time_stamp1 = self.recv_msg_by_id_func(bus_name, request_id)
            if consecutive_frame_data is None:
                continue
            recv_bs_index += 1
            # 判断连续帧是否连续
            recv_consecutive_frame_head = consecutive_frame_data[0]
            if recv_consecutive_frame_head != consecutive_frame_head:
                log_string = f"接收的连续帧头不连续,本应为{hex(consecutive_frame_head)}实际为{hex(recv_consecutive_frame_head)}"
                logger.error(log_string)
                # consecutive_frame_head = recv_consecutive_frame_head + 1
                break
            else:
                consecutive_frame_head += 1
            # 到周期重置
            if consecutive_frame_head > 0x2f:
                consecutive_frame_head = 0x20
            recv_msg_data.extend(consecutive_frame_data[1:])
            if len(recv_msg_data) >= recv_msg_len:
                recv_padding = recv_msg_data[recv_msg_len:]
                recv_msg_data = recv_msg_data[:recv_msg_len]
                break
            # 发送流控帧
            if bs and bs == recv_bs_index:
                flow_control_frame_count+=1
                self.send_msg_by_id_func(bus_name, response_id, flow_control_frame)
                logger.info(f"bus_name {hex(response_id)}第{flow_control_frame_count}次发送流控帧数据》》{flow_control_frame}")
                recv_bs_index = 0

        string_log = f"接收的数据填充位为{recv_padding} 报文为{bytes(recv_msg_data).hex().upper()}"
        logger.info(string_log)
        # 返回 接收的数据，以及填充位置
        return recv_msg_data, list(set(recv_padding)), time_stamp

    def send_diag_request_msg(self, bus_name: str, request_id=0x712, response_id=0x612, send_msg=[],
                              single_frame_len=None,
                              padding=0x00):
        '''
        发送诊断请求
        @param bus_name: 通道名字
        @param request_id:  请求id
        @param response_id: 响应id
        @param bs: block
        @param st: st_min
        @return:
        '''
        # 单帧报文最大长度
        can_single_frame_len = 8
        canfd_single_frame_len = 64

        if bus_name.endswith("canfd"):
            can_type = 0
        else:
            can_type = 1
        # single_frame_len w为 None 表示 can 就是8个字节，canfd 就是64个字节
        if single_frame_len is None:
            if can_type:
                single_frame_len = can_single_frame_len
            else:
                single_frame_len = canfd_single_frame_len
        # 发送数据的 长度，不包含长度字节，纯数据
        send_msg_len = len(send_msg)

        # 判断单帧还是多帧
        if send_msg_len < can_single_frame_len:
            # 长度小于8的 can 和canfd 都是单帧
            # 单帧
            # 有效数据
            first_frame_msg = [send_msg_len] + send_msg
            # 填充数据
            first_frame_padding = [padding] * (single_frame_len - len(first_frame_msg))
            # 完整的首帧数据，单帧数据只有首帧
            first_frame = first_frame_msg + first_frame_padding
            # 发送数据
            self.send_msg_by_id_func(bus_name, request_id, first_frame)
            return time.time()
        elif not can_type and single_frame_len != can_single_frame_len and can_single_frame_len <= send_msg_len < canfd_single_frame_len - 1:
            # canfd 格式
            # 单帧
            # 有效数据
            first_frame_msg = [0, send_msg_len] + send_msg
            # 填充数据
            first_frame_padding = [padding] * (single_frame_len - len(first_frame_msg))
            # 完整的首帧数据，单帧数据只有首帧
            first_frame = first_frame_msg + first_frame_padding
            # 发送数据
            self.send_msg_by_id_func(bus_name, request_id, first_frame)
            return time.time()
        else:
            # 多帧
            multi_head = '1' + hex(send_msg_len)[2:].zfill(3)
            first_frame_msg = send_msg[:single_frame_len - 2]
            first_frame = [int(multi_head[i:i + 2], 16) for i in range(0, len(multi_head), 2)] + first_frame_msg
            left_msg = send_msg[single_frame_len - 2:]
            # 对数据进行分割
            left_msg_list = [left_msg[i:i + single_frame_len - 1] for i in
                             range(0, len(left_msg), single_frame_len - 1)]
            last_msg = left_msg_list[-1]
            # 最后一个不满7个字节则，补充填充位置
            if len(last_msg) < single_frame_len - 1:
                last_msg = last_msg + [padding] * (single_frame_len - 1 - len(last_msg))
                left_msg_list[-1] = last_msg
            # 存放连续帧
            consecutive_frame_list = []
            # 连续帧头
            consecutive_frame_head = 0x21
            for consecutive_frame_msg in left_msg_list:
                consecutive_frame = [consecutive_frame_head] + consecutive_frame_msg
                consecutive_frame_list.append(consecutive_frame)
                consecutive_frame_head += 1
                if consecutive_frame_head > 0x2f:
                    consecutive_frame_head = 0x20

            # 发送首帧数据
            send_time_stamp = time.time()
            self.send_msg_by_id_func(bus_name, request_id, first_frame)
            # 接收流控帧
            recv_flow_control_frame, time_stamp = self.recv_msg_by_id_func(bus_name, response_id)
            first_byte = recv_flow_control_frame[0]
            if first_byte != 0x30:
                logger.error("发送首帧后未收到流控帧或者流控帧收个字节不为0x30")
            recv_bs = recv_flow_control_frame[1]
            recv_stmin = recv_flow_control_frame[2]
            if recv_stmin==0:
                recv_stmin=5
            # 发送连续帧
            for index, msg in enumerate(consecutive_frame_list):
                self.send_msg_by_id_func(bus_name, request_id, msg)
                sleep(recv_stmin / 1000)
                if recv_bs and (index + 1) % recv_bs == 0:
                    recv_flow_control_frame, time_stamp = self.recv_msg_by_id_func(bus_name, response_id)
                    recv_bs = recv_flow_control_frame[1]
                    recv_stmin = recv_flow_control_frame[2]
            return send_time_stamp

    def check_low_beam_act_sts(self, actn_sts: isOn, extr_light_sts: ExtrLtgSts):
        promt_info = f"----------------> Check 近光灯的状态是否ActnOfLedLoBeam:{actn_sts.name},ExtrLtgStsLoBeam:{extr_light_sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedLoBeamActnOfLedLoBeam',
                            actn_sts.value)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsLoBeam', extr_light_sts.value)

    def recover_extral_light_to_defaul_sts(self):
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedLoBeamLe', 0
        )  # 设置HCML近光状态0关1开2故障;
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedLoBeamRi', 0
        )  # 设置HHCMR近光状态0关1开2故障;
        logger.info("\033[0;33;40m设置HCM近光状态0关\033[0m")
        """远光OFF"""
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedHiBeamLe', 0
        )  # 设置HCML远光状态0关1开2故障
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedHiBeamRi', 0
        )  # 设置HCMR远光状态0关1开2故障
        logger.info("\033[0;31;40m设置HCM远光状态0关\033[0m")
        """位置灯OFF"""
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLedFrntPosnLampLe', 0
        )
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr04, 'StsOfLedFrntPosnLampRi', 0
        )
        logger.info("\033[0;32;40m设置HCM位置灯状态0关\033[0m")
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedPosnLampLe1', 0
        )
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedPosnLampRi1', 0
        )
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.RcmmBodyExpoFr02, 'StsOfLedPosnLampMid', 0
        )
        logger.info("\033[0;32;40m设置RCM位置灯状态0关\033[0m")
        """后雾灯"""
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReFogLampLe1', 0
        )
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReFogLampRi1', 0
        )
        logger.info("\033[0;33;40m设置RCM后雾灯状态0关\033[0m")
        """转向灯"""
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLedFrntTurnIndcrLe', 0
        )
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr04, 'StsOfLedFrntTurnIndcrRi', 0
        )
        logger.info("\033[0;34;40m设置HCM前转向灯状态0关\033[0m")
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedTurnIndcrLe1', 0
        )
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedTurnIndcrRi1', 0
        )
        logger.info("\033[0;34;40m设置RCM后转向灯状态0关\033[0m")
        """日行灯"""
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLedDaytiRunngLampLe', 0
        )
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr04, 'StsOfLedDaytiRunngLampRi', 0
        )
        logger.info("\033[0;35;40m设置HCM日行灯状态0关\033[0m")
        """灯组"""
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntLampLe1', 0
        )
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntLampLe2', 0
        )
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedFrntLampMid1', 0
        )
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedFrntLampRi1', 0
        )
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedFrntLampRi2', 0
        )
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReLampLe1', 0
        )
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReLampLe2', 0
        )
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReLampRi1', 0
        )
        self.ipdu.set(
            self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReLampRi2', 0
        )
        logger.info("\033[0;36;40m设置灯光秀灯组状态0关\033[0m")
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedRvsgLampLe1', 'DevSts4_Off')  # 左侧倒车灯
        self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedRvsgLampRi1', 'DevSts4_Off')  # 右侧倒车灯
        sleep(0.5)

    def set_extral_light_button_to_defaul_sts(self):
        self.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.All,sts=SteerWhlTouchSwtSts.NotAvailble)
        sleep(1)
        # self.ipdu.set(
        #     self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3', 0
        # )  # 老方向盘远光按键发0关1超车2远光
        # logger.info("\033[0;33;40m老方向盘远光按键发0关\033[0m")
        # self.ipdu.set(
        #     self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi1SteerWhlTouchSwt2', 0
        # )  # 新方向盘远光按键发0关1超车2远光
        # logger.info("\033[0;33;40m新方向盘远光按键发0关\033[0m")
        # """转向灯按键"""
        # self.ipdu.bodycan_swtrbodyfr01_steerwhltouchswtri2steerwhltouchswt2_steerwhltouchswt_notavailble()
        # logger.info("\033[0;33;40m老方向盘右转按键发0关\033[0m")
        # self.ipdu.bodycan_swtlbodyfr01_steerwhltouchswtle2steerwhltouchswt2_steerwhltouchswt_notavailble()
        # logger.info("\033[0;33;40m新老方向盘左转按键发0关\033[0m")
        # self.ipdu.bodycan_swtlbodyfr02_steerwhltouchswtle1steerwhltouchswt2_steerwhltouchswt_notavailble()
        # logger.info("\033[0;33;40m新方向盘右转按键发0关\033[0m")
        


    def set_door_warning_sts(self,
                             Drvr: Union[bool, None] = None,
                             Pass: Union[bool, None] = None,
                             LeRe: Union[bool, None] = None,
                             RiRe: Union[bool, None] = None
                             ):
        if Drvr is not None:
            with allure.step(f'设置主驾门故障状态为：{Drvr}'):
                logger.info(f'设置主驾门故障状态为：{Drvr}')
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DtcInfDoorDrvrBoolean5', Drvr)
        if Pass is not None:
            with allure.step(f'设置副驾门故障状态为：{Pass}'):
                logger.info(f'设置副驾门故障状态为：{Pass}')
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DtcInfDoorPassBoolean5', Pass)
        if LeRe is not None:
            with allure.step(f'设置左后门故障状态为：{LeRe}'):
                logger.info(f'设置左后门故障状态为：{LeRe}')
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DtcInfDoorLeReBoolean5', LeRe)
        if RiRe is not None:
            with allure.step(f'设置右后门故障状态为：{RiRe}'):
                logger.info(f'设置右后门故障状态为：{RiRe}')
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DtcInfDoorRiReBoolean5', RiRe)

    def set_door_warning_sts(self, warn_sts: Union[bool, None] = None):
        promt_info = f"---------------->同时设置4门的故障状态为{warn_sts}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.set_door_warning_sts(warn_sts, warn_sts, warn_sts, warn_sts)

    def set_door_active_ice_sts(self,
                                Drvr: Union[bool, None] = None,
                                Pass: Union[bool, None] = None,
                                LeRe: Union[bool, None] = None,
                                RiRe: Union[bool, None] = None
                                ):
        if Drvr is not None:
            with allure.step(f'设置主驾门破冰状态为：{Drvr}'):
                logger.info(f'设置主驾门破冰状态为：{Drvr}')
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'IceBreakDoorDrvrActv', Drvr)
        if Pass is not None:
            with allure.step(f'设置副驾门破冰状态为：{Pass}'):
                logger.info(f'设置副驾门破冰状态为：{Pass}')
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'IceBreakDoorPassActv', Pass)
        if LeRe is not None:
            with allure.step(f'设置左后门破冰状态为：{LeRe}'):
                logger.info(f'设置左后门破冰状态为：{LeRe}')
                self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'IceBreakDoorLeReActv', LeRe)
        if RiRe is not None:
            with allure.step(f'设置右后门破冰状态为：{RiRe}'):
                logger.info(f'设置右后门破冰状态为：{RiRe}')
                self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'IceBreakDoorRiReActv', RiRe)

    def set_four_door_active_ice_sts(self, act_ice_sts: Union[bool, None] = None):
        promt_info = f"---------------->同时设置4门的破冰状态为{act_ice_sts}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.set_door_active_ice_sts(act_ice_sts, act_ice_sts, act_ice_sts, act_ice_sts)

    def set_door_radar_sts(self,
                           Drvr: Union[RadarSts, None] = None,
                           Pass: Union[RadarSts, None] = None,
                           LeRe: Union[RadarSts, None] = None,
                           RiRe: Union[RadarSts, None] = None
                           ):
        if Drvr is not None:
            with allure.step(f'设置主驾门雷达故障为：{Drvr.name}'):
                logger.info(f'设置主驾门雷达故障为：{Drvr.name}')
                self.ipdu.set(self.ipdu.connectivitycanfd.DrmflConnectivityFr07, 'RadarDrvrSts', Drvr.value)
        if Pass is not None:
            with allure.step(f'设置副驾门雷达故障为：{Pass.name}'):
                logger.info(f'设置副驾门雷达故障为：{Pass.name}')
                self.ipdu.set(self.ipdu.connectivitycanfd.DrmfrConnectivityFr07, 'RadarPassSts', Pass.value)
        if LeRe is not None:
            with allure.step(f'设置左后门雷达故障为：{LeRe.name}'):
                logger.info(f'设置左后门雷达故障为：{LeRe.name}')
                self.ipdu.set(self.ipdu.connectivitycanfd.DrmrlConnectivityFr07, 'RadarLeReSts', LeRe.value)
        if RiRe is not None:
            with allure.step(f'设置右后门雷达故障为：{RiRe.name}'):
                logger.info(f'设置右后门雷达故障为：{RiRe.name}')
                self.ipdu.set(self.ipdu.connectivitycanfd.DrmrrConnectivityFr07, 'RadarRiReSts', RiRe.value)

    def set_door_radar_sts(self, radar_sts: Union[RadarSts, None] = None):
        promt_info = f"---------------->同时设置4门的雷达故障为{radar_sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.set_door_warning_sts(radar_sts, radar_sts, radar_sts, radar_sts)

    def set_door_anti_pnch_sts(self,
                               Drvr: Union[bool, None] = None,
                               Pass: Union[bool, None] = None,
                               LeRe: Union[bool, None] = None,
                               RiRe: Union[bool, None] = None
                               ):
        if Drvr is not None:
            with allure.step(f'设置主驾门防夹状态为：{Drvr}'):
                logger.info(f'设置主驾门防夹状态为：{Drvr}')
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', Drvr)
        if Pass is not None:
            with allure.step(f'设置副驾门防夹状态为：{Pass}'):
                logger.info(f'设置副驾门防夹状态为：{Pass}')
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassAntiPnch', Pass)
        if LeRe is not None:
            with allure.step(f'设置左后门防夹状态为：{LeRe}'):
                logger.info(f'设置左后门防夹状态为：{LeRe}')
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeReAntiPnch', LeRe)
        if RiRe is not None:
            with allure.step(f'设置右后门防夹状态为：{RiRe}'):
                logger.info(f'设置右后门防夹状态为：{RiRe}')
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiReAntiPnch', RiRe)

    def set_four_door_anti_pnch_sts(self, anti_pnch_sts: Union[bool, None] = None):
        promt_info = f"---------------->同时设置4门的防夹状态为{anti_pnch_sts}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.set_door_anti_pnch_sts(anti_pnch_sts, anti_pnch_sts, anti_pnch_sts, anti_pnch_sts)

    def set_epb_sts(self, sts: int):
        promt_info = f"---------------->EPB状态为{sts}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', sts)
            expectedvalue = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.BcmVddmBackBoneFr00,
                                                                  'EpbStsEpbSts')
            sleep(0.1)
            logger.info("检查EPB状态信号值为: expectedvalue {}".format(expectedvalue))

    def set_pedestrian_protection_fault_sts(self, sts: PedestProtectFltSts):
        promt_info = f"---------------->行人保护故障状态设置为为{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'PedProtnMsgReqForFlt', sts.value)

    def set_pedestrian_protection_warning_sts(self, sts: PedestProtectImpctSts):
        promt_info = f"---------------->行人保护告警状态设置为为{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'PedProtnMsgReqForImpct', sts.value)

    def set_vehicle_crash_sts(self, roll_over_crash: Union[bool, None] = None, front_crash: Union[bool, None] = None,
                              rear_crash: Union[bool, None] = None, left_crash: Union[bool, None] = None,
                              right_crash: Union[bool, None] = None):
        if front_crash is not None:
            logger.info(f"前碰撞状态设置为{front_crash}")
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashFrnt', roll_over_crash)  # 前碰撞状态
        if rear_crash is not None:
            logger.info(f"后碰撞状态设置为{rear_crash}")
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashRe', rear_crash)  # 后碰撞状态
        if left_crash is not None:
            logger.info(f" 左碰撞状态设置为{left_crash}")
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashSideLe', left_crash)  # 左碰撞状态
        if right_crash is not None:
            logger.info(f"右碰撞状态设置为{right_crash}")
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashSideRi', right_crash)  # 右碰撞状态
        if roll_over_crash is not None:
            logger.info(f"倾翻状态设置为{roll_over_crash}")
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RecOfImpctCrashRollovr', roll_over_crash)  # 倾翻状态

    def set_airbagsign_light_active_sts(self, sts: AirbagLampReqSts):
        promt_info = f"---------------->设置安全气囊指示灯激活状态为{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', sts.value)

    def set_airbag_warning_sts(self, sts: AirbagWarningSts):
        promt_info = f"---------------->设置安全气囊提示状态为{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', sts.value)

    def check_intr_light_read_lamp_req(self, zone: ReadLampZone, sts: ReadLampSts):
        promt_info = f"---------------->Check设置阅读灯请求"
        with allure.step(promt_info):
            logger.info(promt_info)
            if zone.name == "FrontLeft":
                logger.info(f"Check 驾驶位阅读灯是否为{sts.name}")
                self.ipdu.check(self.ipdu.cem_lin3.CemCem_Lin3Fr04, "IntrLiGen2RoofRequestIntrLiGen2RoofReqZon1",
                                sts.value)
            if zone.name == "FrontRight":
                logger.info(f"Check 副驾驶阅读灯是否为{sts.name}")
                self.ipdu.check(self.ipdu.cem_lin3.CemCem_Lin3Fr04, "IntrLiGen2RoofRequestIntrLiGen2RoofReqZon2",
                                sts.value)
            if zone.name == "RearLeft":
                logger.info(f"Check 左后阅读灯是否为{sts.name}")
                self.ipdu.check(self.ipdu.cem_lin3.CemCem_Lin3Fr04, "IntrLiGen2RoofRequestIntrLiGen2RoofReqZon3",
                                sts.value)
            if zone.name == "RearRight":
                logger.info(f"Check 右后阅读灯是否为{sts.name}")
                self.ipdu.check(self.ipdu.cem_lin3.CemCem_Lin3Fr04, "IntrLiGen2RoofRequestIntrLiGen2RoofReqZon4",
                                sts.value)

    def check_alm_light_req(self, brightness: Union[int, None] = None, red: Union[int, None] = None,
                            green: Union[int, None] = None, blue: Union[int, None] = None):
        promt_info = f"---------------->Check氛围灯的颜色和亮度"
        with allure.step(promt_info):
            logger.info(promt_info)
            if brightness is not None:
                logger.info(f"Check BGM 发出的控制亮度信号OrdinaryAmbientLightFrontLeftBrightness是否为{brightness}")
                self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBrightness',
                                brightness)
            if red is not None:
                logger.info(f"Check BGM 发出的控制红色像素的信号OrdinaryAmbientLightFrontLeftRed是否为{red}")
                self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftRed', red)
            if green is not None:
                logger.info(f"Check BGM 发出的控制绿色像素的信号OrdinaryAmbientLightFrontLeftGreen是否为{green}")
                self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftGreen', green)
            if blue is not None:
                logger.info(f"Check BGM 发出的控制蓝色像素的信号OrdinaryAmbientLightFrontLeftBlue是否为{blue}")
                self.ipdu.check(self.ipdu.cem_lin5.CemCem_Lin5Fr01, 'OrdinaryAmbientLightFrontLeftBlue', blue)

    def tire_sensor_ini(self, id1='11111111', id2='02628643', id3='026284F4', id4='22222222', pressure: int = 260):
        sensor1 = DataTypeHanding.hexstr_to_inlist(id1)  # 左前
        sensor2 = DataTypeHanding.hexstr_to_inlist(id2)  # 右前
        sensor3 = DataTypeHanding.hexstr_to_inlist(id3)  # 右后
        sensor4 = DataTypeHanding.hexstr_to_inlist(id4)  # 左后
        tire_sensor_dic = {}
        tire_sensor = {
            "tire_id": [],
            "pressure": pressure,
            "calculated_pressure": math.ceil(pressure / 1.373) * 1.373,
            "temp": 52,
            "acc": 36,
            "factory": 0x02,
            "function": 0x85,
            "send_rf": True,
            "cycle_time": 3,
            "counter_per_pkg": 1,
            "rolling_counter": 0
        }

        tire_sensor["tire_id"] = sensor1
        tire_sensor_dic["FrontLeft"] = copy.deepcopy(tire_sensor)
        tire_sensor["tire_id"] = sensor2
        tire_sensor_dic["FrontRight"] = copy.deepcopy(tire_sensor)
        tire_sensor["tire_id"] = sensor3
        tire_sensor_dic["RearRight"] = copy.deepcopy(tire_sensor)
        tire_sensor["tire_id"] = sensor4
        tire_sensor_dic["RearLeft"] = copy.deepcopy(tire_sensor)
        logger.info(f"4个胎压的原始数据是{tire_sensor_dic}")
        return tire_sensor_dic

    def set_tpms_pressure(self, tire_sensor: dict, pos: TirePos = TirePos.All, pressure: Union[int, float] = 260,
                          time_wait: Union[float, int] = 0):
        if pos.name == "All":
            logger.info(f"四轮胎压={pressure}kpa")
            for key in ['FrontLeft', 'FrontRight', 'RearRight', 'RearLeft']:
                calculated_pressure = math.ceil(pressure / 1.373) * 1.373
                tire_sensor[key]["pressure"] = pressure
                tire_sensor[key]["calculated_pressure"] = calculated_pressure
        else:
            logger.info(f"设置{pos.name}={pressure}kpa")
            calculated_pressure = math.ceil(pressure / 1.373) * 1.373
            tire_sensor[pos.name]["pressure"] = pressure
            tire_sensor[pos.name]["calculated_pressure"] = calculated_pressure
        logger.info(
            f"四轮胎压分别为：左前：{tire_sensor['FrontLeft']['pressure']},右前：{tire_sensor['FrontRight']['pressure']}，左后：{tire_sensor['RearRight']['pressure']},右后：{tire_sensor['RearLeft']['pressure']}")
        logger.info(f"等待{time_wait}秒")
        sleep(time_wait)

    def set_tpms_factory(self, tire_sensor: dict, pos: TirePos = TirePos.All, factory: int = 0x02,
                         time_wait: Union[float, int] = 0):
        if pos.name == "All":
            logger.info(f"设置四轮Factory ={factory}kpa")
            for key in ['FrontLeft', 'FrontRight', 'RearRight', 'RearLeft']:
                tire_sensor[key]["factory"] = factory
        else:
            logger.info(f"设置{pos.name}Factory ={factory}")
            tire_sensor[pos.name]["factory"] = factory

        logger.info(
            f"四轮胎压分别为：左前：{tire_sensor['FrontLeft']['factory']},右前：{tire_sensor['FrontRight']['factory']}，左后：{tire_sensor['RearRight']['factory']},右后：{tire_sensor['RearLeft']['factory']}")
        logger.info(f"等待{time_wait}秒")
        sleep(time_wait)

    def set_tpms_temperature(self, tire_sensor: dict, pos: TirePos = TirePos.All, temperature: Union[int, float] = 52,
                             time_wait: Union[float, int] = 0):
        if pos.name == "All":
            logger.info(f"设置四轮温度：{temperature}℃")
            for key in ['FrontLeft', 'FrontRight', 'RearRight', 'RearLeft']:
                tire_sensor[key]["temp"] = temperature
        else:
            logger.info(f"设置{pos.name}温度为：{temperature}℃")
            tire_sensor[pos.name]["temp"] = temperature

        logger.info(
            f"四轮胎压分别为：左前：{tire_sensor['FrontLeft']['temp']},右前：{tire_sensor['FrontRight']['temp']}，左后：{tire_sensor['RearRight']['temp']},右后：{tire_sensor['RearLeft']['temp']}")
        logger.info(f"等待{time_wait}秒")
        sleep(time_wait)

    def check_tire_flag(self, pos: TirePos, flag: SysWarnFlg, status: TireAlarmSts):
        list_flag = [
            ['LeFrntTireMsgSysWarnFlg', 'LeFrntTireMsgPWarnFlg', 'LeFrntTireMsgTWarnFlg', 'LeFrntTireMsgMsgOldFlg',
             'LeFrntTireMsgFastLoseWarnFlg', 'LeFrntTireMsgBattLoSt'],
            ['RiFrntTireMsgSysWarnFlg', 'RiFrntTireMsgPWarnFlg', 'RiFrntTireMsgTWarnFlg', 'RiFrntTireMsgMsgOldFlg',
             'RiFrntTireMsgFastLoseWarnFlg', 'RiFrntTireMsgBattLoSt'],
            ['RiReTireMsgSysWarnFlg', 'RiReTireMsgPWarnFlg', 'RiReTireMsgTWarnFlg', 'RiReTireMsgMsgOldFlg',
             'RiReTireMsgFastLoseWarnFlg', 'RiReTireMsgBattLoSt'],
            ['LeReTireMsgSysWarnFlg', 'LeReTireMsgPWarnFlg', 'LeReTireMsgTWarnFlg', 'LeReTireMsgMsgOldFlg',
             'LeReTireMsgFastLoseWarnFlg', 'LeReTireMsgBattLoSt']]
        if pos.name == "All":
            for i in range(4):
                signal_name = list_flag[i][flag.value]
                promt_info = f"---------------->检测胎压相关信号{signal_name}的信号值是否为{status.name}"
                with allure.step(promt_info):
                    logger.info(promt_info)
                    self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr09, signal_name, status.value)
        else:
            signal_name = list_flag[pos.value - 1][flag.value]
            promt_info = f"---------------->检测胎压相关信号{signal_name}的信号值是否为{status.name}"
            with allure.step(promt_info):
                logger.info(promt_info)
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr09, signal_name, status.value)

    def check_four_tire_flag(self, flag: SysWarnFlg, status: TireAlarmSts):
        logger.info(f"---------------->同时检测4胎压相关信号{flag.name}的信号值是否为{status.name}")
        if flag.value <= 5:
            self.check_tire_flag(TirePos.FrontLeft, flag, status)
            self.check_tire_flag(TirePos.FrontRight, flag, status)
            self.check_tire_flag(TirePos.RearRight, flag, status)
            self.check_tire_flag(TirePos.RearLeft, flag, status)
        else:
            logger.info(f'输入flag{flag}不在定义范围内')

    def pause_bus_send_tpms(self):
        promt_info = f"---------------->停止相关总线发送"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.pause_bus_send("bodyexposedcanfd")
            self.ipdu.pause_bus_send("chassiscan1")
            self.ipdu.pause_bus_send("chassiscan2")
            self.ipdu.pause_bus_send("passivesafetycan")
            self.ipdu.pause_bus_send("infocanfd")
            self.ipdu.pause_bus_send("bodycan")
            self.ipdu.pause_bus_send("propulsioncan")
            self.ipdu.pause_ecu_send('connectivitycanfd', 'DRMFL')
            self.ipdu.pause_ecu_send('connectivitycanfd', 'DRMFR')
            self.ipdu.pause_ecu_send('connectivitycanfd', 'DRMRL')
            self.ipdu.pause_ecu_send('connectivitycanfd', 'DRMRR')
            self.ipdu.pause_ecu_send('connectivitycanfd', 'BNCM')

    def send_tpms_rf_data(self, rf_data, rolling_counter):
        data_part_1 = rf_data + [crc8(rf_data), 0x5E, rolling_counter]
        data_part_2 = [0x00, 0x35, 0x7E, rolling_counter, 0x00, 0x00, 0x00, 0x00]
        logger.info(f"发送消息0x0A:{data_part_1};0x0B:{data_part_2}")
        self.ipdu.send_pdu("connectivitycanfd", 0xA, data_part_1)
        sleep(0.005)
        self.ipdu.send_pdu("connectivitycanfd", 0xB, data_part_2)
        sleep(0.12)

    def set_vehspd_and_qf(self, vehspd: Union[int, float] = 0.0, veh_qf: VehSpdQf = VehSpdQf.AccurData):
        logger.info(f"设置车速为{vehspd}，对应Qf为{veh_qf.name}")
        self.set("backbonefr", "BcmVddmBackBoneFr06", 'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06', vehspd)
        self.set("backbonefr", "BcmVddmBackBoneFr06", 'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06', veh_qf.value)

    def set_vehmtn(self, vehmtnst: VehMtnSts = VehMtnSts.StandStillVal3):
        logger.info(f"设置车辆静止状态{vehmtnst.name}")
        self.set("backbonefr", "BcmVddmBackBoneFr00", 'VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00', vehmtnst.value)

    def set_dtc_pre(self, **kwargs):
        logger.info(f"测试tpmsdtc都前置条件设置")
        lin_channel = kwargs.get("lin_channel", "cem_lin6")
        lin_id = kwargs.get("lin_id", 0x06)
        lin_msg = kwargs.get("lin_msg", [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
        self.ipdu.set(self.ipdu.cem_lin6.CemCem_Lin6Fr02, "BattSnsrStReq", 1)
        self.ipdu.send_pdu(lin_channel, lin_id, lin_msg)
        self.set_dcdc_battary_act_sts(DcDcActvd.ConversionToLVSide)

    def check_climate_cycle_req(self, sts: ClimateCycleReq):
        promt_info = f"---------------->空调循环模式请求是否为{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd_0_CEMBodySignalIPdu14', sts.value)

    def check_windspeed_sts_req(self, pos: SeatVenPos, speed: SeatVenSpeed, time_wait: Union[int, float] = 0):
        promt_info = f"---------------->空调通风请求，check的位置{pos.name}，风速{speed.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "All":
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlFrnt', speed.value)
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlRe', speed.value)
            elif pos.name == "Front":
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlFrnt', speed.value)
            elif pos.name == "Rear":
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlRe', speed.value)
        sleep(time_wait)

    def check_climate_windmode_sts_req(self, pos: SeatPos, mode: AirWindMode, time_wait: Union[int, float] = 0):
        promt_info = f"---------------->Check 空调吹风模式请求，check的位置{pos.name}，风速{mode.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "Drive":
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr46, 'HmiCmptmtAirDistbnFrntLe', mode.value)
            elif pos.name == "Pass":
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr46, 'HmiCmptmtAirDistbnFrntRi', mode.value)
            elif pos.name == "RearAll":
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr46, 'HmiCmptmtAirDistbnRe', mode.value)
        sleep(time_wait)

    def trigger_steer_wheel(self, time_interval: Union[int, float] = 0.5):
        promt_info = f"---------------->方向盘触发左转"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2',
                          'SteerWhlTouchSwt_ShortPress')
            logger.info("\033[0;33;40m老方向盘左转按键轻按\033[0m")
            sleep(time_interval)
            self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2',
                          'SteerWhlTouchSwt_NotAvailble')

    def check_lin_bus_sts(self, lin_channel: LinChannel, sts: BusSendSts, msg_name: Union[str, None] = None,
                          signal_name: Union[str, None] = None, last_time: Union[float, int, None] = None):
        promt_info = f"---------------->检测{lin_channel.name}的状态，期望其为{sts.name}状态"
        with allure.step(promt_info):
            logger.info(promt_info)

            lin_bus_name = "cem_lin" + str(lin_channel.value)
            if sts.name == "Sleep":
                result = self.ipdu.check_bus_recv_message(lin_bus_name)
                logger.info("result_original {}".format(result))
                if result == None:
                    assert True
                else:
                    assert False
            elif sts.name == "Awakeup":
                if signal_name is None:
                    result = self.ipdu.check_bus_recv_message(lin_bus_name)
                    logger.info("result {}".format(result))
                    assert result
                else:
                    logger.info(f"启动进程开始检测总线{lin_channel.name} 是否发出{signal_name}")
                    self.ipdu.check_signal_thread_start(getattr(getattr(self.ipdu, lin_bus_name), msg_name),
                                                        signal_name, timeout=last_time + 1)
                    sleep(last_time + 2)
                    result_ori_1 = self.ipdu.check_signal_thread_stop(signal_name, timeout=2 * last_time)
                    logger.info(f"result_original_1:{signal_name}")

                    if result_ori_1 == None:
                        assert False
                    else:
                        result_1 = calculate_signal_times_and_duration(result_ori_1)
                        frame_times = result_1[0]
                        duration_time = result_1[1]
                        logger.info(f"{signal_name}持续发送{frame_times}帧，持续时间为{duration_time}s")
                        if abs(duration_time - last_time) <= 0.5:
                            assert True
                        else:
                            logger.info("帧发送时间误差大于500ms")
                            assert False

    def check_climate_vent_req(self, pos: AirVentReqPos, sts: AirVentReqSts):
        promt_info = f"---------------->check{pos.name} BGM 发出的出风口开关请求是否为{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)

            if pos.name == "DrvrLeft":
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr13, "HmiAirVentDrvrLeSwtReq", sts.value)

            if pos.name == "DrvrRight":
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr13, "HmiAirVentDrvrRiSwtReq", sts.value)

            if pos.name == "PassLeft":
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr13, "HmiAirVentPassLeSwtReq", sts.value)

            if pos.name == "PassRight":
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr13, "HmiAirVentPassRiSwtReq", sts.value)

            if pos.name == "SecRow                                                                                                                                    ":
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr13, "HmiAirVentSecLeLeSwtReq", sts.value)

            if pos.name == "All":
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr13, "HmiAirVentDrvrLeSwtReq", sts.value)
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr13, "HmiAirVentDrvrRiSwtReq", sts.value)
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr13, "HmiAirVentPassLeSwtReq", sts.value)
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr13, "HmiAirVentPassRiSwtReq", sts.value)
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr13, "HmiAirVentSecLeLeSwtReq", sts.value)

    def check_horn_active_req(self, req: isOn):
        promt_info = f"---------------->Check BGM 发出的喇叭激活请求是否为{req.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr18, 'ActvOfHorn', req.value)

    def set_seat_heat_sts(self, pos: SeatId, sts: HeatVentiSts):
        promt_info = f"---------------->模拟座椅节点返回座椅加热状态"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "FrontLeft":
                logger.info(f"模拟主驾座椅返回加热状态为{sts.name}")
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgAvlSts', sts.value)
            elif pos.name == "FrontRight":
                logger.info(f"模拟副驾座椅返回加热状态为{sts.name}")
                self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgAvlSts', sts.value)
            elif pos.name == "RearLeft":
                logger.info(f"模拟后排左侧座椅返回加热状态为{sts.name}")                        #增加后排座椅放回加热状态
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecLe', sts.value)
            elif pos.name == "RearRight":
                logger.info(f"模拟后排右侧座椅返回加热状态为{sts.name}")                        #增加后排座椅放回加热状态
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecRi', sts.value)
            elif pos.name == "RearRow":
                logger.info(f"模拟后排座椅返回加热状态为{sts.name}")                        #增加后排座椅放回加热状态
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecLe', sts.value)
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecRi', sts.value)


    def set_seat_venti_sts(self, pos: SeatId, sts: HeatVentiSts):
        promt_info = f"---------------->模拟座椅节点返回座椅通风状态"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "FrontLeft":
                logger.info(f"模拟主驾座椅返回通风状态为{sts.name}")
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentAvlSts', sts.value)
            elif pos.name == "FrontRight":
                logger.info(f"模拟副驾座椅返回通风状态为{sts.name}")
                self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentAvlSts', sts.value)
            elif pos.name == "RearLeft":
                logger.info(f"模拟后排左侧座椅返回通风状态为{sts.name}")
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecLe', sts.value)
            elif pos.name == "RearRight":
                logger.info(f"模拟后排右侧座椅返回通风状态为{sts.name}")
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecRi', sts.value)
            elif pos.name == "RearRow":
                logger.info(f"模拟后排座椅返回通风状态为{sts.name}")
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecLe', sts.value)
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecRi', sts.value)

    def set_seat_massg_sts(self, pos: SeatId, sts: isOn):
        promt_info = f"---------------->模拟座椅节点返回座椅按摩状态"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "FrontLeft":
                logger.info(f"模拟主驾座椅返回按摩状态为{sts.name}")
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrMassgRunng_0_SmdBodySignalIPdu04', sts.value)
            elif pos.name == "FrontRight":
                logger.info(f"模拟副驾座椅返回按摩状态为{sts.name}")
                self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassMassgRunng_0_SmpBodySignalIPdu03', sts.value)
            else:
                logger.error(f"暂时不支持{pos.name}座椅设置")

    def set_seat_heat_level(self, pos: SeatId, level: HeatVentiLvl):
        promt_info = f"---------------->模拟座椅节点返回座椅加热等级"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "FrontLeft":
                logger.info(f"模拟主驾座椅返回加热等级为{level.name}")
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgLvlSts', level.value)
            elif pos.name == "FrontRight":
                logger.info(f"模拟副驾座椅返回加热等级为{level.name}")
                self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgLvlSts', level.value)
            elif pos.name == "RearLeft":
                logger.info(f"模拟后排左侧座椅返回加热等级为{level.name}")
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecLe', level.value)
            elif pos.name == "RearRight":
                logger.info(f"模拟后排右侧座椅返回加热等级为{level.name}")
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecRi', level.value)
            elif pos.name == "RearRow":
                logger.info(f"模拟后排座椅返回加热等级为{level.name}")
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecLe', level.value)
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgLvlStsRowSecRi', level.value)

    def set_seat_venti_level(self, pos: SeatId, level: HeatVentiLvl):
        promt_info = f"---------------->模拟座椅节点返回座椅通风等级"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "FrontLeft":
                logger.info(f"模拟主驾座椅返回通风等级为{level.name}")
                self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentnLvlSts', level.value)
            elif pos.name == "FrontRight":
                logger.info(f"模拟副驾座椅返回通风等级为{level.name}")
                self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentnLvlSts', level.value)
            elif pos.name == "RearLeft":
                logger.info(f"模拟后排左侧座椅返回通风等级为{level.name}")
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecLe', level.value)
            elif pos.name == "RearRight":
                logger.info(f"模拟后排右侧座椅返回通风等级为{level.name}")
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecRi', level.value)
            elif pos.name == "RearRow":
                logger.info(f"模拟后排座椅返回通风等级为{level.name}")
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecLe', level.value)
                self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentnLvlStsRowSecRi', level.value)

#o_fan.liu
    def check_seat_heat_req(self, pos: SeatId, level: HeatVentiLvl, source:SourceId):
        promt_info = f"---------------->check BGM发出{pos.name}座椅加热是否为{level.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if source.name == "HMI":
                if pos.name == "FrontLeft":
                    logger.info(f"BGM发出主驾座椅加热是否为{level.name}")
                    self.check('bodycan', 'CemBodyFr01', 'HmiSeatClimaHmiSeatHeatgForRowFirstLe', level.value)
                elif pos.name == "FrontRight":
                    logger.info(f"BGM发出副驾座椅加热是否为{level.name}")
                    self.check('bodycan', 'CemBodyFr01', 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', level.value)
                elif pos.name == "RearLeft":
                    logger.info(f"BGM发出后排左侧座椅加热是否为{level.name}")
                    self.check('bodycan', 'CemBodyFr01', 'HmiSeatClimaHmiSeatHeatgForRowSecLe', level.value)
                elif pos.name == "RearRight":
                    logger.info(f"BGM发出后排右侧座椅加热是否为{level.name}")
                    self.check('bodycan', 'CemBodyFr01', 'HmiSeatClimaHmiSeatHeatgForRowSecRi', level.value)
                elif pos.name == "RearRow":
                    logger.info(f"BGM发出后排座椅加热是否为{level.name}")
                    self.check('bodycan', 'CemBodyFr01', 'HmiSeatClimaHmiSeatHeatgForRowSecLe', level.value)
                    self.check('bodycan', 'CemBodyFr01', 'HmiSeatClimaHmiSeatHeatgForRowSecRi', level.value)
            elif source.name == "Remote":
                if pos.name == "FrontLeft":
                    logger.info(f"BGM发出远程主驾座椅加热是否为{level.name}")
                    self.check('bodycan', 'CemBodyFr48', 'TelmSeatDrvHeatClimaLvl', level.value)  ###########TelmSeatDrvHeatClimaLvl
                elif pos.name == "FrontRight":
                    logger.info(f"BGM发出远程副驾座椅加热是否为{level.name}")
                    self.check('bodycan', 'CemBodyFr47', 'TelmSeatPassHeatClimaLvl', level.value)
                elif pos.name == "RearLeft":
                    logger.info(f"BGM发出远程后排左侧座椅加热是否为{level.name}")
                    self.check('bodycan', 'CemBodyFr47', 'TelmSeatSecLeHeatClimaLvl', level.value)
                elif pos.name == "RearRight":
                    logger.info(f"BGM发出远程后排右侧座椅加热是否为{level.name}")
                    self.check('bodycan', 'CemBodyFr47', 'TelmSeatSecRiHeatClimaLvl', level.value)
                    
#o_fan.liu
    def check_seat_venti_req(self, pos: SeatId, level: HeatVentiLvl, source:SourceId):
        promt_info = f"---------------->check BGM发出{pos.name}座椅通风是否为{level.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if source.name == "HMI":
                if pos.name == "FrontLeft":
                    logger.info(f"BGM发出主驾座椅通风是否为{level.name}")
                    self.check('bodycan', 'CemBodyFr01', 'HmiSeatClimaHmiSeatVentnForRowFirstLe', level.value)
                elif pos.name == "FrontRight":
                    logger.info(f"BGM发出副驾座椅通风是否为{level.name}")
                    self.check('bodycan', 'CemBodyFr01', 'HmiSeatClimaHmiSeatVentnForRowFirstRi', level.value)
                elif pos.name == "RearLeft":
                    logger.info(f"BGM发出后排左侧座椅通风是否为{level.name}")
                    self.check('bodycan', 'CemBodyFr01', 'HmiSeatClimaHmiSeatVentnForRowSecLe', level.value)
                elif pos.name == "RearRight":
                    logger.info(f"BGM发出后排右侧座椅通风是否为{level.name}")
                    self.check('bodycan', 'CemBodyFr01', 'HmiSeatClimaHmiSeatVentnForRowSecRi', level.value)
                elif pos.name == "RearRow":
                    logger.info(f"BGM发出后排座椅通风是否为{level.name}")
                    self.check('bodycan', 'CemBodyFr01', 'HmiSeatClimaHmiSeatVentnForRowSecLe', level.value)
                    self.check('bodycan', 'CemBodyFr01', 'HmiSeatClimaHmiSeatVentnForRowSecRi', level.value)
            elif source.name == "Remote":
                if pos.name == "FrontLeft":
                    logger.info(f"BGM发出远程主驾座椅通风是否为{level.name}")
                    self.check('bodycan', 'CemBodyFr48', 'TelmSeatDrvVentnClimaLvl', level.value)  ###########TelmSeatDrvHeatClimaLvl
                elif pos.name == "FrontRight":
                    logger.info(f"BGM发出远程副驾座椅通风是否为{level.name}")
                    self.check('bodycan', 'CemBodyFr47', 'TelmSeatPassVentnClimaLvl', level.value)
                elif pos.name == "RearLeft":
                    logger.info(f"BGM发出远程后排左侧座椅通风是否为{level.name}")
                    self.check('bodycan', 'CemBodyFr47', 'TelmSeatSecLeVentnClimaLvl', level.value)
                elif pos.name == "RearRight":
                    logger.info(f"BGM发出远程后排右侧座椅通风是否为{level.name}")
                    self.check('bodycan', 'CemBodyFr47', 'TelmSeatSecRiVentnClimaLvl', level.value)
                    
#o_fan.liu
    def check_seat_massg_req(self, pos: SeatId, is_on: bool, type: MassType, level: MassIntensity):    #o_fan.liu  整改ok
        promt_info = f"---------------->check BGM发出座椅按摩请求:{pos.name}座椅按摩开关为{is_on},类型为{type.name}，力度为{level.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "FrontLeft":
                logger.info(f"BGM发出主驾座椅按摩请求:{pos.name}座椅按摩开关为{is_on},类型为{type.name}，力度为{level.name}")
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'DrvrSeatDispMassgFctOnOff', is_on)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'DrvrSeatDispMassgFctMassgProg', type.value)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'DrvrSeatDispMassgFctMassgInten', level.value)
            elif pos.name == "FrontRight":
                logger.info(f"BGM发出副驾座椅按摩请求:{pos.name}座椅按摩开关为{is_on},类型为{type.name}，力度为{level.name}")
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'PassSeatDispMassgFctOnOff', is_on)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'PassSeatDispMassgFctMassgProg', type.value)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'PassSeatDispMassgFctMassgInten', level.value)
            else:
                logger.error(f"暂时不支持{pos.name}座椅进行按摩")

    def check_seat_heat_level_sts(self, pos: SeatId, level: HeatVentiLvl):
        promt_info = f"---------------->check BGM 转发的座椅加热等级请求"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "FrontLeft":
                logger.info(f"BGM转发的座椅加热等级请求是否为{level.name}")
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr14, 'DrvrSeatHeatgLvlSts', level.value)
            elif pos.name == "FrontRight":
                logger.info(f"BGM转发的座椅加热等级请求是否为{level.name}")
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr14, 'PassSeatHeatgLvlSts', level.value)
            elif pos.name == "RearLeft":
                logger.info(f"BGM转发的座椅加热等级请求是否为{level.name}")
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', level.value)
            elif pos.name == "RearRight":
                logger.info(f"BGM转发的座椅加热等级请求是否为{level.name}")
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', level.value)
            elif pos.name == "RearRow":
                logger.info(f"BGM转发的座椅加热等级请求是否为{level.name}")
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecLe', level.value)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'HmiSeatClimaHmiSeatHeatgForRowSecRi', level.value)

    def check_seat_heat_available_sts(self, pos: SeatId, sts: HeatVentiSts):
        promt_info = f"---------------->check BGM 转发的座椅加热可用状态请求"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "FrontLeft":
                logger.info(f"BGM转发的座椅加热可用状态请求是否为{sts.name}")
                self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr14, 'DrvrSeatHeatgAvlSts', sts.value)
            elif pos.name == "FrontRight":
                logger.info(f"BGM转发的座椅加热可用状态请求是否为{sts.name}")
                self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr14, 'PassSeatHeatgAvlSts', sts.value)
            else:
                logger.error(f"暂时不支持{pos.name}座椅")

    def check_seat_venti_available_sts(self, pos: SeatId, sts: HeatVentiSts):
        promt_info = f"---------------->check BGM 转发的座椅通风可用状态请求"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "FrontLeft":
                logger.info(f"BGM转发的座椅通风可用状态请求是否为{sts.name}")
                self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr14, 'DrvrSeatVentAvlSts', sts.value)
            elif pos.name == "FrontRight":
                logger.info(f"BGM转发的座椅通风可用状态请求是否为{sts.name}")
                self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr14, 'PassSeatVentAvlSts', sts.value)
            else:
                logger.error(f"暂时不支持{pos.name}座椅")

    def check_seat_heat_massg_sts(self, pos: SeatId, sts: isOn):
        promt_info = f"---------------->check BGM 转发的座椅按摩状态请求"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "FrontLeft":
                logger.info(f"BGM转发的座椅按摩可用状态请求是否为{sts.name}")
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr16, 'DrvrMassgRunng', sts.value)
            elif pos.name == "FrontRight":
                logger.info(f"BGM转发的座椅按摩可用状态请求是否为{sts.name}")
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr16, 'PassMassgRunng', sts.value)
            else:
                logger.error(f"暂时不支持{pos.name}座椅")
                
    def check_seat_direction_adjust_req(self, pos: SeatId, type: SeatAdjustType,
                                        req: Union[SeatUpDownAdj, SeatForwBackAdj]):
        promt_info = f"---------------->check BGM 转发的{pos.name}座椅{type.name}调节请求是否为{req.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if type.name == "Height":
                if pos.name == "FrontLeft":
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatHeiAdjmtRowFirstDrvr', req.value)
                elif pos.name == "FrontRight":
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatHeiAdjmtRowFirstPass', req.value)
            elif type.name == "Len":
                if pos.name == "FrontLeft":
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstDrvr', req.value)
                elif pos.name == "FrontRight":
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatLenAdjmtRowFirstPass', req.value)
            elif type.name == "Back":
                if pos.name == "FrontLeft":
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'BackRestAdjmtRowFirstDrvr', req.value)
                elif pos.name == "FrontRight":
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'BackRestAdjmtRowFirstPass', req.value)
            elif type.name == "Legrest":
                if pos.name == "FrontLeft":
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatCushTiltAdjmtRowFirstDrvr', req.value)
                elif pos.name == "FrontRight":
                    self.ipdu.check(self.ipdu.bodycan.CemBodyFr74, 'SeatCushTiltAdjmtRowFirstPass', req.value)
            elif type.name == "Lumbar":
                if pos.name == "FrontLeft":
                    if req.name == "Forward" or  req.name == "Backward":
                        self.ipdu.check(self.ipdu.bodycan.CemBodyFr54, 'LumLenAdjmtRowFirstDrvr', req.value)
                    elif req.name == "Down" or  req.name == "Up":
                        self.ipdu.check(self.ipdu.bodycan.CemBodyFr54, 'LumHeiAdjmtRowFirstDrvr', req.value)   
                elif pos.name == "FrontRight":
                    if req.name == "Forward" or  req.name == "Backward":
                        self.ipdu.check(self.ipdu.bodycan.CemBodyFr54, 'LumLenAdjmtRowFirstPass', req.value)
                    elif req.name == "Down" or  req.name == "Up":
                        self.ipdu.check(self.ipdu.bodycan.CemBodyFr54, 'LumHeiAdjmtRowFirstPass', req.value)
                    
    def check_intelligent_charge_wakeup_counter(self, check_times: int = 5):
        promt_info = f"--------------->检查补电次数30S内最大补电3次'CnvnReq 信号最多置1{check_times}次"
        with allure.step(promt_info):
            logger.info(promt_info)
            
            result = self.ipdu.check_event(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 1, timeout=30)
            logger.info(f"result:{result}")
            assert result == check_times

    def set_intelligent_charge_wakeup_sts(self, sts: IPMLoUWakeUpReq):
        promt_info = f"--------------->设置补电请求WakeUp请求为{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.bodycan.IpmBodyFr01, 'IPMLoUWakeUpReq', sts.value)

    def check_low_volt_servse_sts(self, cnv_req: CnvnReq, charg_vol_req: Union[float, int, None] = None):
        if charg_vol_req is not None:
            promt_info = f"--------------->查询BGM智能补电状态是否为{cnv_req.name}和补电电压是否为{charg_vol_req}"
            with allure.step(promt_info):
                logger.info(promt_info)
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', cnv_req.value)
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'ChrgnUReq', charg_vol_req)
        else:
            promt_info = f"--------------->查询BGM智能补电状态是否为{cnv_req.name}"
            with allure.step(promt_info):
                logger.info(promt_info)
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', cnv_req.value)

    def set_battery_stop_intelligent_charge(self, time_wait: Union[float, int] = 3):
        promt_info = f"--------------->设置BattURaw停止补电"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'CnvnAllwd', 0)
            self.ipdu.send_pdu("cem_lin6", 0x06, [0x0, 0x7C, 0xC8, 0xFF, 0xFF, 0xFF, 0xFF])
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 0)
            self.ipdu.set(self.ipdu.bodycan.IpmBodyFr01, 'IPMLoUWakeUpReq', 0)
        logger.info(f"--------------->等待{time_wait}秒")
        sleep(time_wait)

    def set_intelligent_charge_allow_sts(self, sts: CnvnAllwd, time_wait: Union[float, int] = 0):
        promt_info = f"--------------->设置智能补电允许情况{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08, 'CnvnAllwd', sts.value)
        logger.info(f"--------------->等待{time_wait}秒")
        sleep(time_wait)

    def check_rear_view_fold_sts_req(self, req: FoldHmiReq):
        promt_info = f"--------------->Check BGM发出的后视镜展开折叠请求是否为{req.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'ExtrMirrFoldHmiReq', req.value, check_time=3)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'ExtrMirrFoldHmiReq', 0)

    def check_rear_view_autofold_req(self, req: AutoFoldReq):
        promt_info = f"--------------->Check Auto_BGM发出的后视镜展开折叠请求是否为{req.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr92, 'MirrOpenClsReq', req.value, check_time=3)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr92, 'MirrOpenClsReq', 0)
                        
    def set_pass_seat_present(self):
        with allure.step("设置副驾占位"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts', 2)

    def set_pass_seat_notpresent(self):
        with allure.step("设置副驾未占位"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts', 0)

    def set_secle_seat_present(self):
        with allure.step("设置后左占位"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe', 2)

    def set_secle_seat_notpresent(self):
        with allure.step("设置后左未占位"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe', 0)

    def set_secmid_seat_present(self):
        with allure.step("设置后中占位"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecMid', 2)

    def set_secmid_seat_notpresent(self):
        with allure.step("设置后中未占位"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecMid', 0)

    def set_secri_seat_present(self):
        with allure.step("设置后右占位"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecRi', 2)

    def set_secri_seat_notpresent(self):
        with allure.step("设置后右未占位"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecRi', 0)

    def check_usage_mode_status(self, usage_mode: UsageMode, timeout=1):
        logger.info(f"-------->检查UsageMode是否为：{usage_mode.name}")
        timer = 0
        while timer < timeout:
            receive_result = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr02,
                                                                   'VehModMngtGlbSafe1UsgModSts_0_CEMBackBoneSignalIpdu02')
            logger.info(f"-------->通过总线上的信号获取UsageMode值为{receive_result}")
            if receive_result == usage_mode.value:
                logger.info("-------->获取的实际UsageMode和期望的一致")
                assert True
                return
            else:
                sleep(0.1)
                timer = timer + 0.1    
        logger.info("-------->获取的实际UsageMode和期望的不一致")
        assert False

    def check_car_mode_status(self, car_mode_main: CarMode, car_mode_sub: int, timeout=1):
        logger.info(f"-------->检查CarMode是否为：{car_mode_main.name},子模式是否为{car_mode_sub}")
        timer = 0
        while timer < timeout:
            receive_result_main = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr02,
                                                                        'VehModMngtGlbSafe1CarModSts1')
            logger.info(f"-------->通过总线上的信号获取CarMode值为{receive_result_main}")
            receive_result_sub = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr02,
                                                                       'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp')
            logger.info(f"-------->通过总线上的信号获取CarMode 子模式值为{receive_result_sub}")
            if receive_result_main == car_mode_main.value and receive_result_sub == car_mode_sub:
                logger.info("-------->获取的实际CarMode和子模式与期望的一致")
                assert True
                return
            else:
                sleep(0.1)
                timer = timer + 0.1
        logger.info("-------->获取的实际CarMode和子模式与期望的不一致")
        assert False

    def trigger_gear_by_auto(self, gear_status: bool = True):
        promt_info = f"--------------->触发自动挂挡"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr10, 'DrvrDesDirDrvrDesDir', 3)
            if gear_status == True:
                self.ipdu.set(self.ipdu.chassiscan1.AcuChas1Fr04, 'GearAutoShiftReq1', 3)
                self.ipdu.set(self.ipdu.chassiscan1.AcuChas1Fr04, 'GearAutoShiftReqSts1', 0)
                self.ipdu.set(self.ipdu.chassiscan1.AcuChas1Fr04, 'GearAutoShiftReqSts1', 1)
            else:
                self.ipdu.set(self.ipdu.chassiscan1.AcuChas1Fr04, 'GearAutoShiftReq1', 0)
                self.ipdu.set(self.ipdu.chassiscan1.AcuChas1Fr04, 'GearAutoShiftReqSts1', 0)

    def trigger_gear_by_cdc(self, gear_status: bool = True):
        promt_info = f"--------------->触发屏幕挂挡"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr10, 'DrvrDesDirDrvrDesDir', 3)
            if gear_status == True:
                self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr12,
                              'CDCDrvrGearShiftDirReq1UpDTipAut_0_CdcInfoCanFdSignalIPdu12', 0)
                self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr12,
                              'CDCDrvrGearShiftDirReq1UpTipAut_0_CdcInfoCanFdSignalIPdu12', 0)
                self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr12,
                              'CDCDrvrGearShiftDirReq1UpDTipAut_0_CdcInfoCanFdSignalIPdu12', 1)
                self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr12,
                              'CDCDrvrGearShiftDirReq1UpTipAut_0_CdcInfoCanFdSignalIPdu12', 1)
            else:
                self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr12,
                              'CDCDrvrGearShiftDirReq1UpDTipAut_0_CdcInfoCanFdSignalIPdu12', 0)
                self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr12,
                              'CDCDrvrGearShiftDirReq1UpTipAut_0_CdcInfoCanFdSignalIPdu12', 0)

    def trigger_gear_by_manual(self, gear_status: bool = True):
        promt_info = f"--------------->触发手动挂挡"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr10, 'DrvrDesDirDrvrDesDir', 3)
            if gear_status == True:
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr09, 'DrvrGearShiftDirReq1UpUpTipAut', 0)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr09, 'DrvrGearShiftDirReq1UpUpTipAut', 1)
            else:
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr09, 'DrvrGearShiftDirReq1UpUpTipAut', 0)

    def check_four_door_and_tailgate_hood_sts(self, sts: Door,pos:DoorPos = DoorPos.All):
        promt_info = f"--------------->Check {pos.name}门状态是否为{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
         
            if pos.name == "Dirver":
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', sts.value)
            elif pos.name == "Pass":
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', sts.value)
            elif pos.name == "RearLeft":
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', sts.value)
            elif pos.name == "RearRight":
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', sts.value)
            elif pos.name == "Tailgate":
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11, 'TrSts', sts.value)
            elif pos.name == "Hood":
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'HoodSts', sts.value)
            elif pos.name == "All":
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', sts.value)
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', sts.value)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', sts.value)
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', sts.value)
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr11, 'TrSts', sts.value)
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'HoodSts', sts.value)


    def check_climate_fragrance_req(self, taste: FragChannel, level: FragLevel,
                                    ch1_ratio: Union[int, None] = 0, ch2_ratio: Union[int, None] = 0,
                                    ch3_ratio: Union[int, None] = 0,
                                    ch4_ratio: Union[int, None] = 0, ch5_ratio: Union[int, None] = 0):
        promt_info = f"--------------->Check BGM 发出的香氛信息"
        with allure.step(promt_info):
            logger.info(promt_info)

            logger.info(f"--------------->Check BGM发出的请求控制的香氛通道{taste.name}")
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'TelmAirFragTasteReq', taste.value)

            logger.info(
                f"--------------->Check BGM发出的5个香氛通道的香氛比例是[{ch1_ratio},{ch2_ratio},{ch3_ratio},{ch4_ratio},{ch5_ratio}]")
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh1', ch1_ratio)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh2', ch2_ratio)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh3', ch3_ratio)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh4', ch4_ratio)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh5', ch5_ratio)

            logger.info(f"--------------->Check BGM发出的请求控制的香氛等级是{level.name}")
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr46, 'HmiFragraLvlReq', level.value)

    def set_door_open_angle_sts(self, door_pos: DoorId, angle: int, wait_time: Union[float, int] = 0):
        promt_info = f"--------------->设置{door_pos.name}门的开度为{angle}"
        with allure.step(promt_info):
            logger.info(promt_info)

            if door_pos.name == "kDoorFrontLeft":
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrPosn', angle)

            if door_pos.name == "kDoorFrontRight":
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassPosn', angle)

            if door_pos.name == "kDoorRearLeft":
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeRePosn', angle)

            if door_pos.name == "kDoorRearRight":
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiRePosn', angle)

            if door_pos.name == "kDoorAll":
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrPosn', angle)
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassPosn', angle)
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeRePosn', angle)
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiRePosn', angle)

            logger.info(f"--------------->等待{wait_time}秒")
            sleep(wait_time)

    def check_door_trigger_source(self, door_pos: DoorId, trigger_source: DoorOpenSource):
        promt_info = f"--------------->Check{door_pos.name}门操作的触发源是否为{trigger_source.name}"
        with allure.step(promt_info):
            logger.info(promt_info)

            if door_pos.name == "kDoorFrontLeft":
                self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', trigger_source.value)

            if door_pos.name == "kDoorFrontRight":
                self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqTrigSrc', trigger_source.value)

            if door_pos.name == "kDoorRearLeft":
                self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqTrigSrc', trigger_source.value)

            if door_pos.name == "kDoorRearRight":
                self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqTrigSrc', trigger_source.value)

            if door_pos.name == "kDoorAll":
                self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', trigger_source.value)
                self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqTrigSrc', trigger_source.value)
                self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqTrigSrc', trigger_source.value)
                self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqTrigSrc', trigger_source.value)

    def set_climate_pm25_sts(self, int_pm25_sts: PM25Sts):
        promt_info = f"--------------->设置车辆PM2.5状态为{int_pm25_sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'IntPm25StsFrmClima', int_pm25_sts.value)

    def set_climate_pm25_value(self, int_pm25_val: int):
        promt_info = f"--------------->设置车辆PM2.5值为{int_pm25_val}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr02, 'IntPm25VluFrmClima', int_pm25_val)

    def set_climate_pm25_level(self, int_pm25_level: PM25Level):
        promt_info = f"--------------->设置车辆PM2.5等级为{int_pm25_level.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr01, 'IntPm25LvlFrmClima', int_pm25_level.value)

    def set_defrost_sts(self, defrost_sts: isOn):
        promt_info = f"--------------->设置车辆前挡除霜状态为{defrost_sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr11, 'ClimaDefrstSts', defrost_sts.value)

    def set_outer_rearview_defrost_sts(self, mirr_def_sts: MirrrDefrstrSts):
        promt_info = f"--------------->设置车辆外后视镜除霜状态为{mirr_def_sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr11, 'HmiDefrstrElecStsMirrr', mirr_def_sts.value)

    def check_climate_temp_req(self, zone: ClimateZone, value: Union[float, int]):
        promt_info = f"--------------->Check BGM 发出的{zone.name}空调温度为{value}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if zone.name == "FirstRowLeft":
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15, 'HmiCmptmtTSpForRowFirstLe', value)
            if zone.name == "FirstRowRight":
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15, 'HmiCmptmtTSpForRowFirstRi', value)
            if zone.name == "FirstRow":
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15, 'HmiCmptmtTSpForRowFirstLe', value)
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15, 'HmiCmptmtTSpForRowFirstRi', value)
            if zone.name == "SecondRowLeft":
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15, 'HmiCmptmtTSpForRowSecLe', value)
            if zone.name == "SecondRowRight":
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15, 'HmiCmptmtTSpForRowSecRi', value)
            if zone.name == "SecondRow":
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15, 'HmiCmptmtTSpForRowSecLe', value)
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15, 'HmiCmptmtTSpForRowSecRi', value)
            if zone.name == "AllZone":
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15, 'HmiCmptmtTSpForRowFirstLe', value)
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15, 'HmiCmptmtTSpForRowFirstRi', value)
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15, 'HmiCmptmtTSpForRowSecLe', value)
                self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15, 'HmiCmptmtTSpForRowSecRi', value)

    def set_tailgate_opener_sts(self, sts: DoorOpenerSts, time_wait: Union[float, int] = 0):
        promt_info = f"--------------->设置尾门开关的状态为{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', sts.value)

        logger.info(f"等待{time_wait}s")
        sleep(time_wait)

    def get_usage_mode_status(self):
        logger.info(f"-------->返回UsageMode状态")
        receive_result = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr02,
                                                               'VehModMngtGlbSafe1UsgModSts_0_CEMBackBoneSignalIpdu02')
        logger.info(f"-------->通过总线上的信号获取UsageMode值为{receive_result}")
        return receive_result

    def set_charge_target_soc_value(self, value: Union[float, int], time_wait: Union[float, int] = 0):
        promt_info = f"--------------->设置目标充电SOC值为{value}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', value)

        logger.info(f"等待{time_wait}s")
        sleep(time_wait)

    def set_driver_seat_btn_psd_sts(self, sts: bool, time_wait: Union[float, int] = 0):
        promt_info = f"--------------->设置主驾座椅安全带插入状态为{sts}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr01, 'DrvrSeatBtnPsd', sts)

        logger.info(f"等待{time_wait}s")
        sleep(time_wait)

    def set_pass_seat_btn_psd_sts(self, sts: bool, time_wait: Union[float, int] = 0):
        promt_info = f"--------------->设置副驾座椅安全带插入状态为{sts}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr01, 'PassSeatBtnPsd', sts)
        logger.info(f"等待{time_wait}s")
        sleep(time_wait)

    def set_driver_seat_ext_adj_allow_sts(self, sts: bool, time_wait: Union[float, int] = 0):
        promt_info = f"--------------->设置主驾座椅座椅调节允许情况为{sts}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', sts)

        logger.info(f"等待{time_wait}s")
        sleep(time_wait)

    def mock_bgm_send_ccp(self, byte_index_to_change=[], change_to_value=[]):
        """
        在connectivityCANFD上实现CCP报文发送（TCAM）:模拟BGM发送CCP报文，能够修改任意字节并发送

        :param byte_index_to_change: 需要修改CCP的字节序号列表
        :param change_to_value: 需要修改CCP的字节序号对应的值的列表
        """
        self.mock_ccp_flag = False
        ccp_raw_value = self.ccp_raw_value
        ccp_before_can_list = []
        ccp_after_can_list = []
        if len(ccp_raw_value) == 3116:
            logger.info("CCP 初始值长度合法，为1558个字节")
            if not isinstance(byte_index_to_change, list):
                return False, "参数 byte_index_to_change的类型需为列表"
            else:
                for num in byte_index_to_change:
                    if not isinstance(num, int):
                        return False, "字节序号必须是整形"
                    if num > 1008:
                        return False, "字节序号不能大于1008"
            if not isinstance(change_to_value, list):
                return False, "参数 change_to_value的类型需为列表"
            else:
                for value in change_to_value:
                    if not isinstance(value, int):
                        return False, "修改的CCP值必须是整形"
                    if value > 255:
                        return False, "修改的CCP值不能大于255"
            ccp_before_can_raw = ccp_raw_value[0:1008]
            for i in range(72):  # 第一个can id 对应的72个报文
                ccp_before_can_value = ccp_before_can_raw[i * 14:(i + 1) * 14]
                ccp_before_can_value_list = [int(hex(i + 1), 16)]  # 8个字节中的第一个为序号
                for j in range(7):  # 8个字节中的后7个字节
                    value = ccp_before_can_value[j * 2:(j + 1) * 2]  # 第j+2个字节
                    for x, y in zip(byte_index_to_change, change_to_value):
                        if x == i * 7 + (j + 1):
                            ccp_before_can_value_list.append(y)
                            break
                    else:
                        ccp_before_can_value_list.append(int(value, 16))
                else:
                    ccp_before_can_list.append(ccp_before_can_value_list)
            else:
                logger.info("前72个报文中发送修改的报文：")
                num = 0
                for m in ccp_before_can_list:
                    for x in byte_index_to_change:
                        if num * 7 <= x <= (num + 1) * 7:
                            logger.info(f"   {m}")
                    num = num + 1
            ccp_after_can_raw = ccp_raw_value[1008:2016]
            for i in range(72):
                ccp_after_can_value = ccp_after_can_raw[i * 14:(i + 1) * 14]
                ccp_after_can_value_list = [int(hex(i + 1), 16)]  # 8个字节中的第一个为序号
                for j in range(7):  # 8个字节中的后7个字节
                    value = ccp_after_can_value[j * 2:(j + 1) * 2]  # 第j+2个字节
                    for x, y in zip(byte_index_to_change, change_to_value):
                        if x == 504 + i * 7 + (j + 1):
                            ccp_after_can_value_list.append(y)
                            break
                    else:
                        ccp_after_can_value_list.append(int(value, 16))
                else:
                    ccp_after_can_list.append(ccp_after_can_value_list)
            else:
                logger.info("后72个报文中发送修改的报文：")
                num = 0
                for m in ccp_after_can_list:
                    for x in byte_index_to_change:
                        if num * 7 <= x - 504 <= (num + 1) * 7:
                            logger.info(f"   {m}")
                    num = num + 1
            self.mock_ccp_flag = True
            time.sleep(0.5)
            # 新建2个线程，在两个线程内分别向总线connectivitycanfd循环发送报文0x330（before）, 0x400（after）
            self.ipdu.preheat_msg('connectivitycanfd', "VgmConnFr06")
            self.ipdu.preheat_msg('connectivitycanfd', "VgmConnFr11")
            time.sleep(2)
            before_thread = threading.Thread(target=self._mock_bgm_send, args=(0x330, ccp_before_can_list))
            before_thread.setDaemon(True)
            after_thread = threading.Thread(target=self._mock_bgm_send, args=(0x400, ccp_after_can_list))
            after_thread.setDaemon(True)
            before_thread.start()
            after_thread.start()
            return True, "执行成功"
        else:
            logger.info("CCP 初始值不满足1558个字节")
            return False, "CCP 初始值不满足1558个字节"

    def _mock_bgm_send(self, can_id, data_list):
        while self.mock_ccp_flag:
            before = time.time()
            for data in data_list:
                self.ipdu.send_pdu('connectivitycanfd', can_id, data)
                time.sleep(0.08)
            # else:
            #     after = time.time()
            #     logger.info(f"通过{can_id}发送CCP报文耗时{round((after - before), 2)}秒!!")
        else:
            logger.info("停止模拟BGM发送CCP报文")

    def centrl_lock_pre_msg_send_ctrl(self, sts: MsgSendContrl):
        if sts.name == "Pause":
            logger.info("停止chassiscan1,chassiscan2,passivesafetycan 和部分connectivitycanfd 消息发送")
            self.ipdu.pause_bus_send("chassiscan1")
            self.pause_bus_send("chassiscan2")
            self.pause_bus_send("passivesafetycan")
            self.pause_ecu_send("connectivitycanfd", "DRMFL")
            self.pause_ecu_send("connectivitycanfd", "DRMFR")
            self.pause_ecu_send("connectivitycanfd", "DRMRL")
            self.pause_ecu_send("connectivitycanfd", "DRMRR")
            self.pause_ecu_send("connectivitycanfd", "TCAM")
            self.stop_send_pdu("connectivitycanfd", 0x10)
            self.ipdu.stop_send_pdu("connectivitycanfd", 0x40)

        elif sts.name == "Start":
            logger.info("恢复所有消息发送")
            self.ipdu.resume_all_bus_send()

    def check_steer_strength_level_req(self, req: SteerAsscLvl):
        promt_info = f"---------------->Check BGM 发出的方向盘转动的扭矩等级是否为{req.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.backbonefr.IHUBackBoneFr16, 'SteerAsscLvl', req.value)

    def set_rear_view_mode(self, pos: ViewPos, mode: MirrStsTyp):
        promt_info = f"---------------->设置{pos.name}后视镜折叠状态为{mode.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "RearLeft":
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', mode.value)

            elif pos.name == "RearRight":
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', mode.value)

            elif pos.name == "All":
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr', mode.value)
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass', mode.value)

    def set_rear_view_direction(self, pos: ViewPos, direction: MirrDirReq):
        promt_info = f"---------------->设置{pos.name}后视镜方向为{direction.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "RearLeft":
                self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'DrvrExtrMirrAdjHmiReq', direction.value)

            elif pos.name == "RearRight":
                self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'PassExtrMirrAdjHmiReq', direction.value)

            elif pos.name == "All":
                self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'DrvrExtrMirrAdjHmiReq', direction.value)
                self.ipdu.set(self.ipdu.bodycan.CEMBodyFr13, 'PassExtrMirrAdjHmiReq', direction.value)

    def check_climate_angle_req(self, drvr_LeX: int = 0, drvr_LeY: int = 0, pass_LeX: int = 0, pass_LeY: int = 0,
                                drvr_RiX: int = 0, drvr_RiY: int = 0,
                                pass_RiX: int = 0, pass_RiY: int = 0, sec_rowLeX: int = 0, sec_rowLeY: int = 0,
                                sec_rowRiX: int = 0, sec_rowRiY: int = 0):
        promt_info = f"---------------->Check出风口角度请求"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqDrvrLePosX', drvr_LeX)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqDrvrLePosY', drvr_LeY)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqPassLePosX', pass_LeX)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqPassLePosY', pass_LeY)

            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqDrvrRiPosX', drvr_RiX)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqDrvrRiPosY', drvr_RiY)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqPassRiPosX', pass_RiX)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqPassRiPosY', pass_RiY)

            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'HmiReElecAirDirCrtlReqSecRowLePosX', sec_rowLeX)
            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'HmiReElecAirDirCrtlReqSecRowLePosY', sec_rowLeY)
            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'HmiReElecAirDirCrtlReqSecRowRiPosX', sec_rowRiX)
            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'HmiReElecAirDirCrtlReqSecRowRiPosY', sec_rowRiY)

    # def check_door_lock_and_unlock_sts(self, drv_lock: Union[LockStatus, None] = None,
    #                                    pass_lock: Union[LockStatus, None] = None,
    #                                    lere_lock: Union[LockStatus, None] = None,
    #                                    rire_lock: Union[LockStatus, None] = None):
    #     if drv_lock is not None:
    #         logger.info(f"Check BGM 发出主驾位控制锁的请求是否为{drv_lock.name}")
    #         self.ipdu.check(self.ipdu.bodycan.DdmBodyFr04, 'DoorDrvrLockSts', drv_lock.value)
    #     if pass_lock is not None:
    #         logger.info(f"Check BGM 发出副驾位控制锁的请求是否为{pass_lock.name}")
    #         self.ipdu.check(self.ipdu.bodycan.PdmBodyFr01, 'DoorPassLockSts', pass_lock.value)
    #     if lere_lock is not None:
    #         logger.info(f"Check BGM 发出左后控制锁的请求是否为{lere_lock.name}")
    #         self.ipdu.check(self.ipdu.bodycan.RldmBodyFr01, 'DoorLeReLockSts', lere_lock.value)
    #     if rire_lock is not None:
    #         logger.info(f"Check BGM 发出右后控制锁的请求是否为{rire_lock.name}")
    #         self.ipdu.check(self.ipdu.bodycan.RrdmBodyFr01, 'DoorRiReLockSts', rire_lock.value)

    # def set_four_doors_lock_and_unlock_sts(self, lock_sts: LockStatus):
    #     logger.info(f"同时设置4门锁的状态为{lock_sts.name}")
    #     self.set_door_lock_sts(drv_lock=lock_sts, pass_lock=lock_sts, rire_lock=lock_sts, lere_lock=lock_sts)

    def check_lock_sys_sts(self, req: LockSysStsPrmt):
        promt_info = f"---------------->Check BGM 发出的获取中控锁状态提醒是否为{req.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr21, 'LockSysStsPrmt', req.value)

    def check_central_lock_event_sts(self, evn_update_sts: bool, evn_trigsrc: LockTrigerSource):
        promt_info = f"---------------->Check BGM 是否发出锁状态改变事件，期望结果是{evn_update_sts}，期望的触发源是{evn_trigsrc.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsUpdEve', evn_update_sts)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', evn_trigsrc.value)

    def set_low_bean_fault_sts(self, pos: GeneralPos, fault_sts: LampSts):
        promt_info = f"---------------->设置{pos.name}近光灯故障状态{fault_sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "Right":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedLoBeamRi', fault_sts.value)

            elif pos.name == "Left":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedLoBeamLe', fault_sts.value)

            elif pos.name == "All":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedLoBeamRi', fault_sts.value)
                self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedLoBeamLe', fault_sts.value)

    def set_high_bean_fault_sts(self, pos: GeneralPos, fault_sts: LampSts):
        promt_info = f"---------------->设置{pos.name}远光灯故障状态{fault_sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "Right":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedHiBeamRi', fault_sts.value)

            elif pos.name == "Left":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedHiBeamLe', fault_sts.value)

            elif pos.name == "All":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr02, 'StsOfLedHiBeamRi', fault_sts.value)
                self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr02, 'StsOfLedHiBeamLe', fault_sts.value)

    def set_blue_id_type_sts(self, key_id: int, type: BlueType, con_sts: ConnSts):
        promt_info = f"---------------->设置蓝牙的Key_ID为：{key_id},设置蓝牙类型为{type.name},连接状态{con_sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo2KeyIdByte0', key_id)
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo2KeyTyp', type.value)
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo2KeyConnectSts',
                          con_sts.value)

    def set_chrglid_pos(self, sts: int):
        promt_info = f"---------------->仿真获取充电口盖位置百分比为{sts}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcActPosn2', sts)

    def check_chrgild_req(self, req: ChrgLidReq,timeout: Union[float, int] = 30):
        promt_info = f"---------------->Check BGM 发出的控制充电口盖请求是否为{req.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.check(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', req.value,timeout)


    def check_chrgild_sts(self, sts: ChrgLidOpenCloseSts):
        promt_info = f"---------------->Check BGM 发出的充电口盖状态是否为{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr09, 'ChrgLidRearSts', sts.value)

    def set_chrglid_fault(self, fault_type: ChrdLidFaultType, sts: bool = True, time_wait: Union[float, int] = 0):
        promt_info = f"---------------->设置充电口盖故障类型为{fault_type.name},故障状态为{sts}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if fault_type.name == "ElecErr":
                self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcElecErrFb', sts)
            elif fault_type.name == "TempHigh":
                self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTFb', sts)
            elif fault_type.name == "VoltHigh":
                self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverVoltFb', sts)
            elif fault_type.name == "VoltLow":
                self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcUnderVoltFb', sts)
            elif fault_type.name == "All":
                self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcElecErrFb', sts)
                self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTFb', sts)
                self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverVoltFb', sts)
                self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcUnderVoltFb', sts)

        logger.info(f"等待{time_wait}s")
        sleep(time_wait)

    def check_chrglid_fault_sts(self, sts: isOn):
        promt_info = f"---------------->Check BGM 发出的充电口盖故障状态是否为{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr19, 'ChrgLidRearFltSts', sts.value)

    def check_door_open_mode_req(self, pos: DoorPos, mode: isOn):
        promt_info = f"---------------->Check BGM 发出的{pos.name}门的打开模式是否为{mode.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "Dirver":
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetDrvrPwrDoorAutOperMode', mode.value)
            elif pos.name == "Pass":
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetPassPwrDoorAutOperMode', mode.value)
            elif pos.name == "RearLeft":
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetLeRePwrDoorAutOperMode', mode.value)
            elif pos.name == "RearRight":
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetRiRePwrDoorAutOperMode', mode.value)
            elif pos.name == "All":
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetDrvrPwrDoorAutOperMode', mode.value)
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetPassPwrDoorAutOperMode', mode.value)
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetLeRePwrDoorAutOperMode', mode.value)
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetRiRePwrDoorAutOperMode', mode.value)

    def blue_data_preheat_start(self):
        logger.info("Start preheating!!!")
        self.ipdu.preheat_msg("connectivitycanfd", "BncmToBgmCanTpFrame")

    def blue_data_preheat_stop(self):
        logger.info("Stop preheating!!!")
        self.ipdu.remove_preheating("connectivitycanfd", "BncmToBgmCanTpFrame")

    def get_blue_tp_data(self, msg_id=0x31A, fc=[48, 0, 5, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA], timeout=5):
        logger.info("----------------------------> enter bus_com get_blue_tp_data")
        # self.ipdu.send_pdu("connectivitycanfd", 0x33A, fc,cycle_time=0.003)
        
        rev_msg_list=[]
        msg_len = 0
        start = time.time()
        data = []
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", msg_id)
        logger.info("Start to recv can message")
        while time.time() - start < timeout:
            # self.ipdu.rx_flag_reset_msg("connectivitycanfd", msg_id)
            rx_data = self.ipdu.recv_pdu("connectivitycanfd", msg_id, timeout=1)
            if rx_data != None:
                rx_fm = rx_data[3]
                # self.ipdu.send_pdu("connectivitycanfd", 0x33A, fc)
            else:
                continue
            logger.info("Get frame: {}".format(rx_fm))
            if rx_fm[0] == 0:
                data_len = rx_fm[1]
                data = rx_fm[2:data_len + 2]
                rev_msg_list.append(data)
                logger.info("Get single frame: {}".format(data))
                data = []
                break
            elif rx_fm[0] < 32:
                # self.ipdu.send_pdu("connectivitycanfd", 0x33A, fc)
                msg_len = rx_fm[1] + (rx_fm[0] - 16) * 256
                data = rx_fm[2:]
                msg_len = msg_len - 62
                logger.info("Get first frame: {}".format(data))
                continue
            elif rx_fm[0] >= 32:
                if msg_len > 63:
                    # self.ipdu.send_pdu("connectivitycanfd", 0x33A, fc)
                    data = data + rx_fm[1:]
                    msg_len = msg_len - 63
                    logger.info(f"剩余的msg_len:{msg_len}")
                    logger.info("Get continue frame: {}".format(data))
                    continue
                else:
                    data = data + rx_fm[1:1 + msg_len]
                    rev_msg_list.append(data)
                    logger.info("Get last frame: {}".format(data))
                    data = []
                    break
        logger.info("Get CANTP list: {}".format(rev_msg_list))
        self.ipdu.reset_check_results()
        return rev_msg_list

    def check_door_switch_light_sts(self, pos: DoorPos, req: LampSts):
        prompt_info = f"----------> Check BGM 发出的{pos.name}门按键指示灯状态是否为{req.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)

            if pos.name == "Dirver":
                self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightDrvrSwLight', req.value)
            elif pos.name == "Pass":
                self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightPassSwLight', req.value)
            elif pos.name == "RearLeft":
                self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightLeReSwLight', req.value)
            elif pos.name == "RearRight":
                self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightRiReSwLight', req.value)
            elif pos.name == "All":
                self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightDrvrSwLight', req.value)
                self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightPassSwLight', req.value)
                self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightLeReSwLight', req.value)
                self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightRiReSwLight', req.value)

    def check_driver_door_QF_sts(self, sts: FacQlyDoorSts):
        prompt_info = f"----------> Check BGM 发出的驾驶门QF状态是否为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'DoorDrvrStsWithFacQlyDoorSts', sts.value)

    def press_door_inside_switch(self, pos: DoorPos = DoorPos.Dirver, time_interval: Union[int, float] = 3):
        prompt_info = f"触发模拟按{pos.name}门外开关"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if pos.name == "Dirver":
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'DoorDrvrOpenReqInsdSwt1', 1)
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrOpenReqInsdSwt2', 1)
                sleep(time_interval)
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'DoorDrvrOpenReqInsdSwt1', 2)
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrOpenReqInsdSwt2', 2)

            elif pos.name == "Pass":
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'DoorPassOpenReqInsdSwt1', 1)
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassOpenReqInsdSwt2', 1)
                sleep(time_interval)
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'DoorPassOpenReqInsdSwt1', 2)
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassOpenReqInsdSwt2', 2)

            elif pos.name == "RearLeft":
                self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'DoorLeReOpenReqInsdSwt1', 1)
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeReOpenReqInsdSwt2', 1)
                sleep(time_interval)
                self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'DoorLeReOpenReqInsdSwt1', 2)
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeReOpenReqInsdSwt2', 2)

            elif pos.name == "RearRight":
                self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'DoorRiReOpenReqInsdSwt1', 1)
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiReOpenReqInsdSwt2', 1)
                sleep(time_interval)
                self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'DoorRiReOpenReqInsdSwt1', 2)
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiReOpenReqInsdSwt2', 2)

    def set_steer_strength_level(self, level: SteerAsscLvl, time_wait: Union[int, float] = 0):
        prompt_info = f"设置方向盘强度等级为{level.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr06, 'SteerAsscLvlCfmd', level.value)
        logger.info(f"等待{time_wait}s")
        sleep(time_wait)

    def set_dc_chrg_handle_sts(self, sts: DCChrgnHndlSts, time_wait: Union[int, float] = 0):
        with allure.step(f"设置充电枪状态为：{sts.name}"):
            logger.info(f"设置充电枪状态为：{sts.name}")
            self.set('backbonefr', 'VddmBackBoneFr29', 'DCChrgnHndlSts', sts.value)
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15,"DCChrgnHndlSts", sts.value)
        logger.info(f"等待{time_wait}s")
        sleep(time_wait)

    def stop_listen_dk_bgm_response(self):
        self.dk.stop_listen_dk_bgm_response()

    def reset_bncm_digital_keyinfo(self):
        self.dk.reset_bncm_digital_keyinfo()

    def update_keyinfos(self, location: Union[Location, int], keys: List[KeyInfo]):
        self.dk.update_keyinfos(location, keys)

    def send_approach_light_cmd(self, key_type: int = 2, key_id=key_id1):
        self.dk.send_approach_light_cmd(key_type, key_id)

    def send_approach_unlock_cmd(self, key_type: int = 2, key_id=key_id1):
        self.dk.send_approach_unlock_cmd(key_type, key_id)

    def send_walk_away_lock_cmd(self, key_type: int = 2):
        self.dk.send_walk_away_lock_cmd(key_type)

    def press_door_outswitch(self,door_index: int, timeout: Union[int, float]):
        self.dk.press_door_outswitch(door_index,timeout)

    def get_recent_signal_raw_value(self, msg_signals_obj: type, signal_name: str):
        return self.ipdu.get_recent_signal_raw_value(msg_signals_obj, signal_name)

    def lin_send_pwm(self, lin_bus: LinChannel, run_time: int = 1000):
        prompt_info = f"---------->在{lin_bus.name}发送{run_time}微妙 PWM"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            lin_bus_name = "cem_lin" + str(lin_bus.value)
            self.bus_app.send_pwm(bus_name=lin_bus_name, RunTimeOfUs=run_time)

    def check_lin_bus_awakeup_result(self, lin_bus: LinChannel, trig_start, trig_stop, exp_time_dif=0.5):
        logger.info(f"触发开始时间：{trig_start}")
        logger.info(f"触发结束时间：{trig_stop}")
        prompt_info = f"---------->监控{lin_bus.name}的数据"
        lin_bus_name = "cem_lin" + str(lin_bus.value)
        time_1 = 0
        t2 = None
        with allure.step(prompt_info):
            logger.info(prompt_info)
            while time_1 < 20:
                result = self.ipdu.check_bus_recv_message(lin_bus_name)
                if result == None:
                    logger.info(f"Lin报文停止发送的时间为：{t2}")
                    break
                else:
                    t2 = time.time()
                    time_1 = time_1 + 0.01
        if t2 != None:
            logger.info(f"从触发开始到检测到总线上数据的时间间隔是：{t2 - trig_start}")
            logger.info(f"从触发结束到检测到总线上数据的时间间隔是：{t2 - trig_stop}")
            if abs((t2 - trig_start) - 10) < exp_time_dif:
                logger.info(f"帧发送时间误差为{abs((t2 - trig_start) - 10)},小于500ms")
                assert True
            else:
                logger.info(f"帧发送时间误差为{abs((t2 - trig_start) - 10)},大于500ms")
                assert False
        else:
            logger.info("lin通道中的报文一直再发送")
            assert False

    def set_hv_batt_thermy_sts(self, sts: HvBattThermReq, time_wait: Union[int, float] = 0):
        prompt_info = f"---------->设置高压电池状态为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr24, 'LocalHvBattThermReqFb', sts.value)

        logger.info(f"等待{time_wait}s")
        sleep(time_wait)

    def check_PNC(self,
                  bus_name: BusName,
                  msg_id: NMMsgId,
                  pnc_name: Union[BGMPNC, TCAMPNC],
                  signal_value: NMSts,
                  timeout: Union[int, float] = 1,
                  check_time: int = 1):
        step_msg = f'{timeout}s内检查{bus_name.name} {msg_id.name} {pnc_name.name}的值为{signal_value.name}的次数为{check_time}次'
        logger.info(step_msg)
        with allure.step(f'{step_msg}'):
            status, raw_data = self.ipdu.check_PNC(
                bus_name.value,
                msg_id.value,
                pnc_name.value,
                signal_value.value,
                timeout,
                check_time
            )
            err_msg = f'PNC检查失败'
            assert status, err_msg
            return raw_data

    def check_PNC_thread_start(self,
                               bus_name: BusName,
                               msg_id: NMMsgId,
                               pnc_name: Union[BGMPNC, TCAMPNC],
                               signal_value: NMSts,
                               timeout: Union[int, float] = 1,
                               check_time: int = 1):
        step_msg = f'开始{timeout}s内检查{bus_name.name} {msg_id.name} {pnc_name.name}的值为{signal_value.name}的次数为{check_time}次'
        logger.info(step_msg)
        with allure.step(f'{step_msg}'):
            self.ipdu.check_PNC_thread_start(
                bus_name.value,
                msg_id.value,
                pnc_name.value,
                signal_value.value,
                timeout,
                check_time
            )

    def check_PNC_thread_stop(self,
                              bus_name: BusName,
                              msg_id: NMMsgId,
                              pnc_name: Union[BGMPNC, TCAMPNC],
                              timeout: Union[int, float] = 1):
        step_msg = f'结束{timeout}s内检查{bus_name.name} {msg_id.name} {pnc_name.name}'
        logger.info(step_msg)
        with allure.step(f'{step_msg}'):
            status, raw_data = self.ipdu.check_PNC_thread_stop(
                bus_name.value,
                msg_id.value,
                pnc_name.value,
                timeout
            )
            err_msg = f'PNC检查失败'
            assert status, err_msg
            return raw_data

    def set_PNC(self,
                bus_name: BusName,
                msg_id: NMMsgId,
                pnc_name_list: List[Union[BGMPNC, TCAMPNC]],
                pin_value: int = 0,
                frame_type: FrameType = FrameType.quick):
        step_info = f'设置{bus_name.name} 0{msg_id.name} {pnc_name_list}置位为{frame_type.name}帧发送'
        logger.info(step_info)
        with allure.step(step_info):
            pnc_name_list = [i.value for i in pnc_name_list]
            return self.ipdu.set_PNC(bus_name.value, msg_id.value, pnc_name_list, pin_value, frame_type.value)
            return self.ipdu.set_PNC(bus_name.value, msg_id.value, pnc_name.value, signal_value.value, frame_type.value)

    def telm_set_chrglid_sts(self, sts: ChrgLidOpenCloseSts, time_wait: Union[int, float] = 0):
        prompt_info = f"---------->APP远程设置充电枪状态为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.set(self.ipdu.connectivitycanfd.TcamConnectivityFr12, 'RemDCChrgLidTelmReq', sts.value)

        logger.info(f"等待{time_wait}s")
        sleep(time_wait)

    def set_chrglid_sts(self, sts: ChrgLidConnectSts, time_wait: Union[int, float] = 0):
        prompt_info = f"---------->充电枪连接状态为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.set(self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'DCChrgnHndlSts', sts.value)

        logger.info(f"等待{time_wait}s")
        sleep(time_wait)
        
    def set_pos_lamp_sts(self, front_rear:GeneralPos, pos: GeneralPos, sts: PosnLampSts, time_wait: Union[int, float] = 0):
        prompt_info = f"---------->设置{front_rear.name}位置灯{pos.name}侧灯状态为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)

            if front_rear.name =="Front":
                if pos.name == "Left":
                    self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLedFrntPosnLampLe', sts.value)
                elif pos.name == "Right":
                    self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr04, 'StsOfLedFrntPosnLampRi', sts.value)
                elif pos.name == "All":
                    self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLedFrntPosnLampLe', sts.value)
                    self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr04, 'StsOfLedFrntPosnLampRi', sts.value)
            elif front_rear.name =="Rear":
                if pos.name == "Left":
                    self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedPosnLampLe1', sts.value)

                elif pos.name == "Mid":
                    self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmmBodyExpoFr02, 'StsOfLedPosnLampMid', sts.value)

                elif pos.name == "Right":
                    self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedPosnLampRi1', sts.value)

                elif pos.name == "All":
                    self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedPosnLampLe1', sts.value)
                    self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmmBodyExpoFr02, 'StsOfLedPosnLampMid', sts.value)
                    self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedPosnLampRi1', sts.value)
        logger.info(f"等待{time_wait}s")
        sleep(time_wait)

    def set_steerwheel_turn_lamp_sts(self, type: VehType, rotate_direc: RotateDirec, sts: SteerWhlTouchSwt):
        prompt_info = f"---------->设置{type.name}车型，{rotate_direc.name}转状态为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if rotate_direc == "Left":
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', sts.value)

            elif rotate_direc == "Right":
                if type.name == "Old":
                    self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', sts.value)
                else:
                    self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', sts.value)

            elif rotate_direc == "All":
                if type.name == "Old":
                    self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', sts.value)
                    self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2', sts.value)
                else:
                    self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2', sts.value)
                    self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2', sts.value)

    def check_turn_lamp_act_req(self, sts: IndcrSts, act_sts: IndcrSts):
        prompt_info = f"---------->Check 转向灯状态是否为{sts.name}激活状态是否状态为{act_sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts', sts.value)
            self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'ActvnOfIndcrIndcrOut', act_sts.value)

    def set_turn_indcr_lamp_sts(self, pos: LampPos, sts: PosnLampSts, time_wait: Union[int, float] = 0):
        prompt_info = f"---------->设置{pos.name}转向灯状态为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)

            if pos.name == "FrontLeft":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLedFrntTurnIndcrLe', sts.value)

            elif pos.name == "FrontRight":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr04, 'StsOfLedFrntTurnIndcrRi', sts.value)

            elif pos.name == "RearLeft":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedTurnIndcrLe1', sts.value)

            elif pos.name == "RearRight":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedTurnIndcrRi1', sts.value)

            elif pos.name == "All":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLedFrntTurnIndcrLe', sts.value)
                self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr04, 'StsOfLedFrntTurnIndcrRi', sts.value)
                self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedTurnIndcrLe1', sts.value)
                self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedTurnIndcrRi1', sts.value)

        logger.info(f"等待{time_wait}s")
        sleep(time_wait)

    def check_outside_turn_lamp_act_sts(self, pos: GeneralPos, act_sts_le: PosnLampSts, act_sts_ri: PosnLampSts,pos_sts: Union[IndcrSts,None]=None):
        prompt_info = f"---------->检查外部{pos.value}左转向灯开关状态{act_sts_le.value}，右转向灯开关状态{act_sts_ri.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if pos_sts is not None:
                logger.info(f"指示灯状态为{pos_sts.name}")
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'IndcrDisp', pos_sts.value)

            if pos == "Left":
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', act_sts_le.value)
            elif pos == "Right":
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', act_sts_ri.value)
            elif pos == "All":
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrLe', act_sts_le.value)
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsTurnIndrRi', act_sts_ri.value)

    def trigger_call_sos_by_can(self):
        logger.info("通过发送can signal信号crash触发xcll")
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 0)
        time.sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 1)

    def set_fota_download_wake_condition(self, display_hv_soc: Union[int, float], low_volt_soc: Union[int, float]):
        self.set('propulsioncan', 'EcmPropFr04', 'DispHvBattLvlOfChrg', display_hv_soc)
        logger.info(f"成功设置高压电池显示的SOC值为{display_hv_soc}")
        pdu_data_map = {
            50: [0xF4, 0x01, 0xB4, 0x00, 0x00, 0x00, 0x00],
            69: [0xB2, 0x02, 0xB4, 0x00, 0x00, 0x00, 0x00],
            70: [0xBC, 0x02, 0xB4, 0x00, 0x00, 0x00, 0x00],
            71: [0xC6, 0x02, 0xB4, 0x00, 0x00, 0x00, 0x00],
            90: [0x84, 0x03, 0xB4, 0x00, 0x00, 0x00, 0x00]
        }
        if low_volt_soc in pdu_data_map:
            self.ipdu.send_pdu("cem_lin6", 0x06, pdu_data_map[low_volt_soc])
            logger.info(f"成功设置小电池电量SOC值为{low_volt_soc}")
        else:
            logger.error(f"不合法的小电池电量SOC值：{low_volt_soc}，请在 [50, 69, 70, 71, 90] 中进行选择")


    def check_signal_value_and_times(self,bus:str,msg:str,signal:str,value:Union[int,float],times:Union[int,str],timeout:Union[int,float] = 3):
        prompt_info = f"---------->Check 总线{bus}上的信号{signal}({msg})值{value}是否发送了{times}次"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            bus_obj = getattr(self.ipdu, bus)
            msg_signals_obj = getattr(bus_obj, msg)
            result_ori = self.ipdu.check_signal(msg_signals_obj, signal, timeout)
            logger.info("{}秒内获取信号{}所有的值是:{}".format(timeout, signal, result_ori))
            result = get_signal_times_interval(result_ori, value)
            logger.info("期望值的统计结果:{}".format(result))
            if isinstance(times,int):
                assert result[0] == times
            else:
                assert result[0] != 0


    def set_brake_pedal(self,safe:Union[None,YesOrNo] = YesOrNo.Yes,qf:Union[None,ValueQf] = ValueQf.AccurData,sts:Union[None,YesOrNo] = YesOrNo.Yes):
        prompt_info = f"---------->设置刹车踏板相关信号"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if sts is not None:
                logger.info(f"刹车踏板安全校验设为{safe.name}")
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', safe.value)
            if qf is not None:
                logger.info(f"刹车踏板QF设为{qf.name}")
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', qf.value)
            if sts is not None:
                logger.info(f"刹车踏板状态设为{sts.name}")
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', sts.value)


    def set_brake_req_light_on_sts(self,sts:ReqSts):
        prompt_info = f"---------->设置刹车请求点亮灯请求为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'BrkLiOnReqSts', sts.value)


    def set_emergency_brake_req_light_on_sts(self,req:EmgyBrkLiReq):
        prompt_info = f"---------->设置紧急刹车请求点亮灯请求为{req.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EmgyBrkLiReqEmgyBrk', req.value)

    def check_brake_light_act_sts(self,lamp_sts:isOn,mid_lamp_sts:isOn):
        prompt_info = f"---------->设置刹车灯激活状态为{lamp_sts.name},中央刹车灯激活状态为{mid_lamp_sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp',lamp_sts.value)
            self.ipdu.check(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr01, 'ActnOfLedStopLampMid', mid_lamp_sts.value)

    def check_brake_light_sts(self,sts:ExtrLtgSts):
        prompt_info = f"---------->检车刹车灯状态是否为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsStopLi', sts.value)


    def set_brake_lamp_fault_sts(self,pos:GeneralPos,sts:ExtrLtgSts):
        prompt_info = f"---------->设置{pos.name}刹车灯故障状态{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if pos.name == "Left":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01,'StsOfLedStopLampLe1',sts.value)
            elif pos.name == "Right":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, "StsOfLedStopLampRi1",sts.value)
            elif pos.name == "Mid":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmmBodyExpoFr02,"StsOfLedStopLampMid",sts.value)
            elif pos.name == "All":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01,'StsOfLedStopLampLe1',sts.value)
                self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, "StsOfLedStopLampRi1",sts.value)
                self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmmBodyExpoFr02,"StsOfLedStopLampMid",sts.value)

    def set_brake_pedal_sensor_sts(self,sts:BrkPedlSnsrSt):
        prompt_info = f"---------->设置辅助踏板传感器状态{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoCommonFr08, 'BrkPedlSnsr',sts.value)


    def check_rear_fog_sts(self, actn_sts: isOn, extr_light_sts: ExtrLtgSts):
        prompt_info = f"---------->Check后雾灯的状态是否为:ActnOfLedReFogLamp:{actn_sts.name},状态是否为:ExtrLtgStsReFog:{extr_light_sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedReFogLamp', actn_sts.value)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReFog', extr_light_sts.value)

    def set_rear_fog_fault_sts(self,pos:GeneralPos,sts:ExtrLtgSts):
        prompt_info = f"---------->设置{pos.name}后雾灯故障状态{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if pos.name == "Left":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReFogLampLe1', sts.value)
            if pos.name == "Right":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReFogLampRi1', sts.value)
            if pos.name == "All":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReFogLampLe1', sts.value)
                self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedReFogLampRi1', sts.value)


    def check_door_rels_req(self,Drv:Union[DoorRelsReq, None] = None, Pass:Union[DoorRelsReq, None] = None,
                            ReLe:Union[DoorRelsReq, None] = None,RiRe:Union[DoorRelsReq, None] = None,
                            Tr: Union[DoorRelsReq, None] = None):
        with allure.step(f"check五门电释放请求状态"):
            if Drv is not None:
                logger.info(f"Check主驾位门电释放请求状态为{Drv.name}")
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'DoorDrvrRelsReq',Drv.value)
            if Pass is not None:
                logger.info(f"Check副驾驶位门电释放请求状态为{Pass.name}")
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'DoorPassRelsReq',Pass.value)
            if ReLe is not None:
                logger.info(f"Check左后门电释放请求状态为{ReLe.name}")
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'DoorLeReRelsReq',ReLe.value)
            if RiRe is not None:
                logger.info(f"Check右后门电释放请求状态为{RiRe.name}")
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'DoorRiReRelsReq',RiRe.value)
            if Tr is not None:
                logger.info(f"Check尾门电释放请求状态为{Tr.name}")
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr01, 'TrRelsReq', Tr.value)

    
    def set_ble_bus_siginal_veh_body(self,func_module:BleVehicleBody,sub_func:Union[TirePos,DoorId,WindowId,ViewPos,None],value:Union[int,float]):
        if sub_func is not None:
            prompt_info = f"---------->设置蓝牙功能模块：{func_module.name}的{sub_func.name}相关的信号值为{value}"
        else:
            prompt_info = f"---------->设置蓝牙功能模块：{func_module.name}相关的信号值为{value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if func_module.name == "Doors":
                self.set_door_open_angle_sts(door_pos=sub_func,angle=value)
            elif func_module.name == "TailGate":
                self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', value)
            elif func_module.name == "TailWing":
                self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrPosn', value)
            elif func_module.name == "Wins":
                if sub_func.name == "kWindowFrontLeft":
                    self.set("bodycan", "DdmBodyFr04", 'WinPosnStsAtDrvr',value)
                elif sub_func.name == "kWindowFrontRight":
                    self.set("bodycan", "PdmBodyFr01", 'WinPosnStsAtPass', value)
                elif sub_func.name == "kWindowRearLeft":
                    self.set("bodycan", "RldmBodyFr01", 'WinPosnStsAtReLe',value)
                elif sub_func.name == "kWindowRearRight": 
                    self.set("bodycan", "RrdmBodyFr01", 'WinPosnStsAtReRi',value)


    def set_ble_bus_siginal_charge(self,func_module:BleEicCharg,sub_func:Union[BleCharging,BleBatteryInfo],value:Union[int,float]):
        prompt_info = f"---------->设置蓝牙功能模块：{func_module.name}的{sub_func.name}相关的信号值为{value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if func_module.name == "Charging":
                if sub_func.name == "PluggerSts":
                    self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15,"DCChrgnHndlSts", value)
                elif sub_func.name == "ChargSpeed":
                    self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr29, 'ChrgnSpd', value)

            elif func_module.name == "BatteryInfo":
                if sub_func.name == "Current":
                    self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HvBattIDc1', value)


    def set_singal(self,bus: str,msg: str,signal: str,value: Union[str, int, float],wait_time:Union[int,float] = 0):
        prompt_info = f"---------->设置{bus}:{msg}:{signal}值为：{value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            bus = str.lower(bus)
            self.set(bus_name=bus,msg_name=msg,signal_name=signal,sig_value_name=value)

        if wait_time != 0:
            logger.info(f"设置信号之后等待{wait_time}")
            sleep(wait_time)
    
    def check_singal(self,bus: str,msg: str,signal: str,value: Union[str, int, float],timeout:Union[int,float] = 5,do_assert = True,check_time = 1):
        prompt_info = f"---------->检测{bus}:{msg}:{signal}的值是否为：{value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            bus = str.lower(bus)
            self.check(bus_name=bus,msg_name=msg,signal_name=signal,sig_value_name=value,timeout=timeout,do_assert=do_assert,check_time=check_time)


    def check_bms_related_signal(self,type:BMSWakeUpSetType,value:Union[GeneralSts,int,float]):
        if isinstance(value,GeneralSts):
            prompt_info = f"---------->检测BMS相关的{type.name}功能的值是否为：{value.name}"
        else:
            prompt_info = f"---------->检测BMS相关的{type.name}功能的值是否为：{value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if type.name == "ChrgnCurrThd":
                self.ipdu.check(self.ipdu.cem_lin6.BgmCem_Lin6Fr03, 'BMSChrgnCurrWakeUpThd', value)
            elif type.name == "ChrgnCurrEna":
                self.ipdu.check(self.ipdu.cem_lin6.BgmCem_Lin6Fr03, 'BMSChrgnCurrWakeUpEna', value.value)
            elif type.name == "DisChrgnCurrThd":
                self.ipdu.check(self.ipdu.cem_lin6.BgmCem_Lin6Fr03, 'BMSDisChrgnCurrWakeUpThd', value)
            elif type.name == "DisChrgnCurrEna":
                self.ipdu.check(self.ipdu.cem_lin6.BgmCem_Lin6Fr03, 'BMSDisChrgnCurrWakeUpEna', value.value)
            elif type.name == "SocEna":
                self.ipdu.check(self.ipdu.cem_lin6.BgmCem_Lin6Fr03, 'BMSSocWakeUpEna', value.value)
            elif type.name == "SocThd":
                self.ipdu.check(self.ipdu.cem_lin6.BgmCem_Lin6Fr03, 'BMSSocWakeUpThd', value)
            elif type.name == "VolThd":
                self.ipdu.check(self.ipdu.cem_lin6.BgmCem_Lin6Fr03, 'BMSVolWakeUpThd', value)
            elif type.name == "VolEna":
                self.ipdu.check(self.ipdu.cem_lin6.BgmCem_Lin6Fr03, 'BMSVolWakeUpEna', value.value)
        
            
    def get_all_can_channel_info(self):
        '''
        获取所有can通道 名字 索引号
        @return: 返回列表
        '''
        name_dic = self.bus_app.cfg.get("bus")
        can_map = {}
        for name, info in name_dic.items():
            if 'can' in name:
                can_map[info[-1]] = name

        index_list = list(can_map.keys())
        name_list = list(can_map.values())

        return name_list, index_list, can_map

    def get_all_can_channel_index(self):
        '''
        获取所有can 通道的 索引
        @return:
        '''
        name_list, index_list, can_map = self.get_all_can_channel_info()
        # can_index_list = [self.get_can_channel_index(name) for name in can_name_list]
        return index_list

    def get_can_channel_index_by_name(self, bus_name: str):
        '''
        根据通道名字获取通道序号
        @param bus_name:
        @return:
        '''
        name_list, index_list, can_map = self.get_all_can_channel_info()

        us_chn = index_list[name_list.index(bus_name)]
        return us_chn

    def get_can_name_by_index(self, index: int):
        '''
        根据通道序号获取通道名字
        @param index:
        @return:
        '''
        name_list, index_list, can_map = self.get_all_can_channel_info()

        name = can_map.get(index)
        return name

    def recv_mul_can_channel_msg(self, can_chnanel_lis=[0, 4, 7, 9], msg_id=0x7ff, unexpect_msg=[0x02, 0x3e, 0x80],
                                 timeout=2, **kwargs):
        '''
        接收 多路 can，在某个id 段的报文
        @param can_chnanel_lis: can 通道对应的 索引
        @param msg_id: 可以为整数，或者一个元祖（min_id,max_id）
        @param unexpect_msg: 过滤的 报文内容 默认过滤 3e 80
        @param timeout:
        @return:
        '''
        if isinstance(msg_id, (list, tuple)):
            msg_id_min = msg_id[0]
            msg_id_max = msg_id[1]
        else:
            msg_id_min = msg_id
            msg_id_max = msg_id
        dic = {
            # 0: {
            #     0x700: [],
            #     0x701: []
            # }
        }

        tosun_tc1018 = self.bus_app.bus_dict["tosun_tc1018"]
        t = time.time()
        while time.time() - t < timeout:
            msg_info = tosun_tc1018.recv(bus_chn=None, msgid=None)
            if msg_info:
                # (824, 1704889467.191563, 8, [0, 0, 16, 0, 0, 0, 0, 0], 9)
                can_id = msg_info[0]
                can_channel = msg_info[4]
                can_msg = msg_info[3]
                if msg_id_min <= can_id <= msg_id_max:
                    if can_channel in can_chnanel_lis and can_msg[:len(unexpect_msg)] != unexpect_msg:
                        if can_channel in dic:
                            if can_id in dic[can_channel]:
                                dic[can_channel][can_id].append(can_msg)
                            else:
                                dic[can_channel][can_id] = [can_msg]
                        else:
                            dic[can_channel] = {
                                can_id: [can_msg]
                            }
                        msg_string = ' '.join([hex(i)[2:].zfill(2) for i in can_msg])
                        logger.info(f"通道{can_channel}接收到can_id={hex(can_id)}内容为{msg_string}")
        return dic

    def check_bms_related_signal(self,type:BMSWakeUpSetType,value:Union[GeneralSts,int,float]):
        if isinstance(value,GeneralSts):
            prompt_info = f"---------->检测BMS相关的{type.name}功能的值是否为：{value.name}"
        else:
            prompt_info = f"---------->检测BMS相关的{type.name}功能的值是否为：{value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if type.name == "ChrgnCurrThd":
                self.ipdu.check(self.ipdu.cem_lin6.BgmCem_Lin6Fr03, 'BMSChrgnCurrWakeUpThd', value)
            elif type.name == "ChrgnCurrEna":
                self.ipdu.check(self.ipdu.cem_lin6.BgmCem_Lin6Fr03, 'BMSChrgnCurrWakeUpEna', value.value)
            elif type.name == "DisChrgnCurrThd":
                self.ipdu.check(self.ipdu.cem_lin6.BgmCem_Lin6Fr03, 'BMSDisChrgnCurrWakeUpThd', value)
            elif type.name == "DisChrgnCurrEna":
                self.ipdu.check(self.ipdu.cem_lin6.BgmCem_Lin6Fr03, 'BMSDisChrgnCurrWakeUpEna', value.value)
            elif type.name == "SocEna":
                self.ipdu.check(self.ipdu.cem_lin6.BgmCem_Lin6Fr03, 'BMSSocWakeUpEna', value.value)
            elif type.name == "SocThd":
                self.ipdu.check(self.ipdu.cem_lin6.BgmCem_Lin6Fr03, 'BMSSocWakeUpThd', value)
            elif type.name == "VolThd":
                self.ipdu.check(self.ipdu.cem_lin6.BgmCem_Lin6Fr03, 'BMSVolWakeUpThd', value)
            elif type.name == "VolEna":
                self.ipdu.check(self.ipdu.cem_lin6.BgmCem_Lin6Fr03, 'BMSVolWakeUpEna', value.value)


    def set_wti_signal(self,func:WTI_Func,value):
        if func.name == "BatteryLowTelltale":
            logger.info(f"模拟WTI:高压电池电量")
            self.set_singal("propulsioncan", "EcmPropFr04", "DispHvBattLvlOfChrg",value)
        if func.name == "HighVolBattLow":
            logger.info(f"模拟WTI:低电量报警信息")
            self.set_singal("propulsioncan", "EcmPropFr04", "DispHvBattLvlOfChrg",value)
            pass
        if func.name == "SteeringSysWarning":
            logger.info(f"模拟WTI:转向故障信息总线信号")
            self.set_singal("chassiscan1", "PscmChas1Fr03", "SteerErrReq",value)
            pass
        if func.name == "SuspensionFailed":
            logger.info(f"模拟WTI:悬架故障信息总线信号")
            self.set_singal("chassiscan2", "SumChas2Fr05", "SuspFailrStsSuspFailrSts",value)
            pass
        if func.name == "LowBattWarning1":
            logger.info(f"模拟WTI:低压系统故障信息1总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "LowBattWarning2":
            logger.info(f"模拟WTI:低压系统故障信息2总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "LightLevelingMotor":
            logger.info(f"模拟WTI:大灯高度调节电机故障信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "LBFailure":
            logger.info(f"模拟WTI:近光灯故障提示信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "HBFailure":
            logger.info(f"模拟WTI:远光灯故障提示信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "OvertakeLightFailure":
            logger.info(f"模拟WTI:超车灯故障提示信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "ReverseLightFailure":
            logger.info(f"模拟WTI:倒车灯故障提示信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "POFailure":
            logger.info(f"模拟WTI:位置灯故障提示信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "RearFogFailure":
            logger.info(f"模拟WTI:后雾灯故障提示信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "LeftTIFailure":
            logger.info(f"模拟WTI:左转向灯故障提示信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "RightTIFailure":
            logger.info(f"模拟WTI:右转向灯故障提示信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "DriverSeatBeltWarning":
            logger.info(f"模拟WTI:主驾驶安全带报警信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "PassengerSeatBeltWarning":
            logger.info(f"模拟WTI:副驾驶安全带报警信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "SecRowLeftSeatBeltWarning":
            logger.info(f"模拟WTI:二排左安全带报警信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "SecRowMidSeatBeltWarning":
            logger.info(f"模拟WTI:二排中间安全带报警信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "SecRowRightSeatBeltWarning":
            logger.info(f"模拟WTI:二排右安全带报警信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "AirbagFailure":
            logger.info(f"模拟WTI:安全气囊故障信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireFLPressureLow":
            logger.info(f"模拟WTI:左前轮胎胎压低警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireFRPressureLow":
            logger.info(f"模拟WTI:右前轮胎胎压低警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireRLPressureLow":
            logger.info(f"模拟WTI:左后轮胎胎压低警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireRRPressureLow":
            logger.info(f"模拟WTI:右后轮胎胎压低警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireFLPressureHigh":
            logger.info(f"模拟WTI:左前轮胎胎压高警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireFRPressureHigh":
            logger.info(f"模拟WTI:右前轮胎胎压高警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireRLPressureHigh":
            logger.info(f"模拟WTI:左后轮胎胎压高警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireRRPressureHigh":
            logger.info(f"模拟WTI:右后轮胎胎压高警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireFLTempHigh":
            logger.info(f"模拟WTI:左前轮胎温度高警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireFRTempHigh":
            logger.info(f"模拟WTI:右前轮胎温度高警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireRLTempHigh":
            logger.info(f"模拟WTI:左后轮胎温度高警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireRRTempHigh":
            logger.info(f"模拟WTI:右后轮胎温度高警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireFLPressureFastLost":
            logger.info(f"模拟WTI:左前轮胎快速漏气警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireFRPressureFastLost":
            logger.info(f"模拟WTI:右前轮胎快速漏气警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireRLPressureFastLost":
            logger.info(f"模拟WTI:左后轮胎快速漏气警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireRRPressureFastLost":
            logger.info(f"模拟WTI:右后轮胎快速漏气警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireFLSensorBattLow":
            logger.info(f"模拟WTI:左前轮胎传感器低电量警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireFRSensorBattLow":
            logger.info(f"模拟WTI:右前轮胎传感器低电量警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireRLSensorBattLow":
            logger.info(f"模拟WTI:左后轮胎传感器低电量警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireRRSensorBattLow":
            logger.info(f"模拟WTI:右后轮胎传感器低电量警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TirePressureSysFailureFL":
            logger.info(f"模拟WTI:左前胎压监测系统故障信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TirePressureSysFailureFR":
            logger.info(f"模拟WTI:右前胎压监测系统故障信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TirePressureSysFailureRL":
            logger.info(f"模拟WTI:左后胎压监测系统故障信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TirePressureSysFailureRR":
            logger.info(f"模拟WTI:右后胎压监测系统故障信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "ChargingGunTemp":
            logger.info(f"模拟WTI:充电口温度过高信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "ThermalOutOfControl":
            logger.info(f"模拟WTI:热失控报警信息总线信号")
            self.set_singal("propulsioncan", "BecmPropFr23", "HvBattLimnIndcn",value)
            pass
        if func.name == "PowerSysFailure":
            logger.info(f"模拟WTI:动力系统故障信息总线信号")
            self.set_singal("chassiscan2", "EcmChas2Fr31", "DrvPfmncRedn",value)
            pass
        if func.name == "HighVolInterLock_0":
            logger.info(f"模拟WTI:高压互锁状态信息总线信号")
            self.set_singal("propulsioncan", "BecmPropFr08", "HvilFlt",value)
            pass
        if func.name == "HighVolInterLock_1":
            logger.info(f"模拟WTI:高压互锁状态信息总线信号")
            self.set_singal("propulsioncan", "BecmPropFr05", "HVIL1Sts",value)
            pass
        if func.name == "HighVolInterLock_2":
            logger.info(f"模拟WTI:高压互锁状态信息总线信号")
            self.set_singal("propulsioncan", "BecmPropFr05", "HVIL2Sts",value)
            pass
        if func.name == "HighVolInterLock_3":
            logger.info(f"模拟WTI:高压互锁状态信息总线信号")
            self.set_singal("propulsioncan", "BecmPropFr05", "HVIL3Sts",value)
            pass
        if func.name == "ChargeLidOpenSts":
            logger.info(f"模拟WTI:充电口盖状态总线信号")
            self.set_singal("cem_lin2", "PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcActPosn2",value)
            pass
        if func.name == "ChargeLidInfo":
            logger.info(f"模拟WTI:充电口盖信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "ChargeLidFault":
            logger.info(f"模拟WTI:充电口盖异常提示总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "EnergyRegenLimit_1":
            logger.info(f"模拟WTI:能量回收限制信息总线信号")
            self.set_singal("chassiscan2", "EcmChas2Fr31", "DrvPfmncRedn",value)
            pass
        if func.name == "EnergyRegenLimit_2":
            logger.info(f"模拟WTI:能量回收限制信息总线信号")
            self.set_singal("backbonefr", "VddmBackBoneFr20", "EgyRgnLvlAct",value)
            pass
        if func.name == "ShiftGear":
            logger.info(f"模拟WTI:换挡失败信息总线信号")
            self.set_singal("chassiscan1", "EcmChas1Fr09", "GearLvrLockIndcn",value)
            pass
        if func.name == "GearFailure":
            logger.info(f"模拟WTI:换挡器故障信息总线信号")
            self.set_singal("chassiscan1", "EcmChas1Fr09", "GearLvrFaultIndcn",value)
            pass
        if func.name == "BrakingFluid":
            logger.info(f"模拟WTI:制动液位信息总线信号")
            self.set_singal("backbonefr", "BcmVddmBackBoneFr39", "BrkFldLvl",value)
            pass
        if func.name == "EPBWarning1":
            logger.info(f"模拟WTI:EPB警告信息总线信号")
            self.set_singal("backbonefr", "BbmVcuBackBoneFr02", "EpbDrvrDispSec",value)
            # self.set_singal("backbonefr", "BcmVddmBackBoneFr16", "EpbDrvrDisp",value)
            pass
        if func.name == "EPBWarning2":
            logger.info(f"模拟WTI:EPB警告信息总线信号")
            self.set_singal("backbonefr", "BcmVddmBackBoneFr16", "EpbDrvrDisp",value)
            pass
        if func.name == "EPBWarningChime":
            logger.info(f"模拟WTI:释放EPB报警音总线信号")
            self.set_singal("backbonefr", "BcmVddmBackBoneFr39", "EpbLampReqEpbLampReq",value)
            self.set_singal("backbonefr", "BbmBackBoneFr04", "EpbLampReqSecEpbLampReq",value)
            pass
        if func.name == "EPBFailure":
            logger.info(f"模拟WTI:EPB故障信息/驻车系统故障总线信号")
            self.set_singal("backbonefr", "BcmVddmBackBoneFr39", "BrkRelsWarnReq",value)
            pass
        if func.name == "EBDWaring":
            logger.info(f"模拟WTI:EBD警告信息总线信号")
            self.set_singal("backbonefr", "BcmVddmBackBoneFr39", "BrkMsgWarnReq",value)
            pass
        if func.name == "AutoholdWarning":
            logger.info(f"模拟WTI:Autohold警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "NoKey":
            logger.info(f"模拟WTI:无钥匙提醒信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "Starting":
            logger.info(f"模拟WTI:启动相关信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "NotParked":
            logger.info(f"模拟WTI:未驻车提醒信息总线信号")
            self.set_singal("backbonefr", "CemBackBoneFr19", "VehNotParkInfoWarn",value)
            pass
        if func.name == "AntiTheft":
            logger.info(f"模拟WTI:防盗报警信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "Coolant":
            logger.info(f"模拟WTI:液位信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "DoorHood":
            logger.info(f"模拟WTI:前舱盖开报警信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "DoorDrv":
            logger.info(f"模拟WTI:主驾门开报警信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "DoorPass":
            logger.info(f"模拟WTI:副驾门开报警信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "DoorRearLeft":
            logger.info(f"模拟WTI:左后门开报警信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "DoorRearRight":
            logger.info(f"模拟WTI:右后门开报警信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "DoorTail":
            logger.info(f"模拟WTI:尾门开报警信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "PedestrianProtectFailure":
            logger.info(f"模拟WTI:行人保护系统故障信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "PedestrianProtectEnabled":
            logger.info(f"模拟WTI:行人保护系统激活信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "WiperWashingLiquid":
            logger.info(f"模拟WTI:雨刮洗涤液信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "WiperSysFailure":
            logger.info(f"模拟WTI:雨刮系统故障信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "WiperExitRepairPosition":
            logger.info(f"模拟WTI:雨刮退出维修位置提醒总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "WiperSensorFailure":
            logger.info(f"模拟WTI:雨量传感器故障信息总线信号")
            self.set_singal("backbonefr", "CemBackBoneFr19", "RainSnsrActvnErrToHmi",value)

        if func.name == "DrvWindowFailure":
            logger.info(f"模拟WTI:主驾车窗故障信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "PassWindowFailure":
            logger.info(f"模拟WTI:副驾车窗故障信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "RearLeWindowFailure":
            logger.info(f"模拟WTI:后排左车窗故障信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "RearRiWindowFailure":
            logger.info(f"模拟WTI:后排右车窗故障信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "3DModelShowsTailPosition":
            logger.info(f"模拟WTI:3D车模显示电动尾翼位置总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "CarTailWarning":
            logger.info(f"模拟WTI:尾翼报警信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "WirelessChargingRemind":
            logger.info(f"模拟WTI:无线充电状态提示总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "SteerWheelHeatWarning":
            logger.info(f"模拟WTI:方向盘加热故障总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "DriverSeatHeatWarning":
            logger.info(f"模拟WTI:主驾驶座椅加热故障报警总线信号")
            self.set_singal("bodycan", "SmdBodyFr04", "DrvrSeatHeatgAvlSts",value)
            pass
        if func.name == "PassengerSeatHeatWarning":
            logger.info(f"模拟WTI:副驾驶座椅加热故障报警总线信号")
            self.set_singal("bodycan", "SmpBodyFr03", "PassSeatHeatgAvlSts",value)
            pass
        if func.name == "DriverSeatWindWarning":
            logger.info(f"模拟WTI:主驾座椅通风故障报警总线信号")
            self.set_singal("bodycan", "SmdBodyFr04", "DrvrSeatVentAvlSts",value)
            pass
        if func.name == "PassengerSeatWindWarning":
            logger.info(f"模拟WTI:副驾座椅通风故障报警总线信号")
            self.set_singal("bodycan", "SmpBodyFr03", "PassSeatVentAvlSts",value)
            pass
        if func.name == "DriverElectricDoorWarning":
            logger.info(f"模拟WTI:主驾电动门故障报警总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "PassengerElectricDoorWarning":
            logger.info(f"模拟WTI:副驾电动门故障报警总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "SecLeftElectricDoorWarning":
            logger.info(f"模拟WTI:后排左侧电动门故障报警总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "SecRightElectricDoorWarning":
            logger.info(f"模拟WTI:后排右侧电动门故障报警总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "NoPowerOutput":
            logger.info(f"模拟WTI:无动力输出总线信号")
            self.set_singal("propulsioncan", "EcmPropComFr10", 'TrsmParkLockdTrsmParkLockd',1)
            self.set_singal("propulsioncan", "EcmPropFr24", 'GearLvrIndcn_1_EcmPropSignalIPdu24',value)
            pass
        if func.name == "HighBeamOperationFailReminder":
            logger.info(f"模拟WTI:远光开启失败提示总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TailGateUnlockWarning":
            logger.info(f"模拟WTI:尾门解锁故障总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "UnlockReminder":
            logger.info(f"模拟WTI:解闭锁提醒1总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "LockFailedReminder":
            logger.info(f"模拟WTI:解闭锁提醒2总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "CannotUnLockReminder":
            logger.info(f"模拟WTI:解闭锁提醒3总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "CloseDoorReminder":
            logger.info(f"模拟WTI:解闭锁提醒4总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "NoKeyPresent":
            logger.info(f"模拟WTI:解闭锁提醒5总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "KeyDisconnectedReminder":
            logger.info(f"模拟WTI:钥匙断连提醒总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "PEBLEKeyLegacyReminder":
            logger.info(f"模拟WTI:车外按钮锁车-蓝牙钥匙遗留提醒总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "PEUWBKeyLegacyOnDriverReminder":
            logger.info(f"模拟WTI:车外按钮锁车-UWB钥匙遗留在主驾驶提醒总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "PEUWBKeyLegacyOnPassReminder":
            logger.info(f"模拟WTI:车外按钮锁车-UWB钥匙遗留在副驾驶提醒总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "PEUWBKeyLegacyOnReLeReminder":
            logger.info(f"模拟WTI:车外按钮锁车-UWB钥匙遗留在二排左提醒总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "PEUWBKeyLegacyOnReRiReminder":
            logger.info(f"模拟WTI:车外按钮锁车-UWB钥匙遗留在二排右提醒总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "PEUWBKeyLegacyOnTrunkReminder":
            logger.info(f"模拟WTI:车外按钮锁车-UWB钥匙遗留在后备箱提醒总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "NFCBLEKeyLegacyReminder":
            logger.info(f"模拟WTI:NFC锁车-蓝牙钥匙遗留提醒总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "NFCUWBKeyLegacyOnDriverReminder":
            logger.info(f"模拟WTI:NFC锁车-UWB钥匙遗留在主驾驶提醒总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "NFCUWBKeyLegacyOnPassReminder":
            logger.info(f"模拟WTI:NFC锁车-UWB钥匙遗留在副驾驶提醒总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "NFCUWBKeyLegacyOnReLeReminder":
            logger.info(f"模拟WTI:NFC锁车-UWB钥匙遗留在后排左提醒总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "NFCUWBKeyLegacyOnReRiReminder":
            logger.info(f"模拟WTI:NFC锁车-UWB钥匙遗留在后排右提醒总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "NFCUWBKeyLegacyOnTrunkReminder":
            logger.info(f"模拟WTI:NFC锁车-UWB钥匙遗留在后备箱提醒总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "ETCFaultReminder":
            logger.info(f"模拟WTI:ETC故障总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "ETCRemoveReminder":
            logger.info(f"模拟WTI:ETC设备被拆除总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireFLPressureLowLevel2":
            logger.info(f"模拟WTI:左前轮胎胎压低二级警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireFRPressureLowLevel2":
            logger.info(f"模拟WTI:右前轮胎胎压低二级警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireRLPressureLowLevel2":
            logger.info(f"模拟WTI:左后轮胎胎压低二级警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TireRRPressureLowLevel2":
            logger.info(f"模拟WTI:右后轮胎胎压低二级警告信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "TouchShiftActivated":
            logger.info(f"模拟WTI:触摸换挡器总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "WPCWarn":
            logger.info(f"模拟WTI:车内NFC读卡故障总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "BNCMWarn":
            logger.info(f"模拟WTI:数字钥匙模块故障总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "NKRWarn":
            logger.info(f"模拟WTI:车外NFC读卡故障总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "BKAWarn":
            logger.info(f"模拟WTI:数字钥匙天线故障总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "EntityKeyBattLow":
            logger.info(f"模拟WTI:实体钥匙电量低总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "DriverRadarWarning":
            logger.info(f"模拟WTI:门雷达报警，主驾总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "PassengerRadarWarning":
            logger.info(f"模拟WTI:门雷达报警，副驾总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "LeftRearRadarWarning":
            logger.info(f"模拟WTI:门雷达报警，左后总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "RightRearRadarWarning":
            logger.info(f"模拟WTI:门雷达报警，右后总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "ChargingFailedWarning":
            logger.info(f"模拟WTI:充电故障总线信号")
            self.set_singal("backbonefr", "VddmBackBoneFr16", "ChrgnOrDisChrgnStsFb",value)
            pass
        if func.name == "DrvWindowMotorOverheating":
            logger.info(f"模拟WTI:主驾车窗电机过热总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "PassWindowMotorOverheating":
            logger.info(f"模拟WTI:副驾车窗电机过热总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "ReleWindowMotorOverheating":
            logger.info(f"模拟WTI:后排左车窗电机过热总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "ReRiWindowMotorOverheating":
            logger.info(f"模拟WTI:后排右车窗电机过热总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "DrvrMirrorFoldError":
            logger.info(f"模拟WTI:主驾后视镜展开回收故障总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "PassMirrorFoldError":
            logger.info(f"模拟WTI:副驾后视镜展开回收故障总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "DrvrMirrorAdjError":
            logger.info(f"模拟WTI:主驾后视镜镜面调节故障总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "PassMirrorAdjError":
            logger.info(f"模拟WTI:副驾后视镜镜面调节故障总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "FrontVentAdjError":
            logger.info(f"模拟WTI:前排出风口调节故障总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "RearVentAdjError":
            logger.info(f"模拟WTI:后排出风口调节故障总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "CirculationMotorError":
            logger.info(f"模拟WTI:内外循环风门故障总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "FrontModeMotorError":
            logger.info(f"模拟WTI:前排吹风模式故障总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "PM25SystemError":
            logger.info(f"模拟WTI:PM2.5系统故障总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "AQSSystemError":
            logger.info(f"模拟WTI:空气质量管理系统故障总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "ClimateSystemError":
            logger.info(f"模拟WTI:空调系统故障总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "FragSystemError":
            logger.info(f"模拟WTI:香氛系统故障总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "RemoteAuthStart":
            logger.info(f"模拟WTI:无钥匙驾驶已启动总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "LowBattWarning3":
            logger.info(f"模拟WTI:低压系统故障信息3总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "EPedalFunIndcn":
            logger.info(f"模拟WTI:减速和滑行提示信息总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "IPMBattFaultWarn":
            logger.info(f"模拟WTI:备用低压电池系统异常总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "CoolantDriveSys":
            logger.info(f"模拟WTI:液位信息1总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "CoolantHighVolBatt":
            logger.info(f"模拟WTI:液位信息2总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "ETCAuthenticationFailed":
            logger.info(f"模拟WTI:ETC认证失败总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "DoorIceBreakReminder":
            logger.info(f"模拟WTI:车门破冰提醒总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "PEKeyLegacyReminder":
            logger.info(f"模拟WTI:车外按钮锁车-钥匙遗留提醒总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "NFCKeyLegacyReminder":
            logger.info(f"模拟WTI:NFC锁车-钥匙遗留提醒总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "PleaseManualCloseDueToCloseDoorFail":
            logger.info(f"模拟WTI:关门失败-请手动关门总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "OpenCloseDoorReminderDueToLargeSlope":
            logger.info(f"模拟WTI:坡度过大开关门提醒总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "DoorAntiPlayAndThermalProtectionReminder":
            logger.info(f"模拟WTI:电动门防玩和热保护提醒总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "AirGrilleAbnormal":
            logger.info(f"模拟WTI:进气格栅异常总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "WiperSwitchUsePrompt":
            logger.info(f"模拟WTI:雨刮开关使用提示总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "RearFogAndLowBeamOff":
            logger.info(f"模拟WTI:后雾灯与近光灯联动关闭提示总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "LaunchModePrompt_1":
            logger.info(f"模拟WTI:弹射起步提示信息总线信号")
            self.set_singal("chassiscan1", "EcmChas1Fr48", "LnchModIndcnMsg",value)
            pass
        if func.name == "LaunchModePrompt_2":
            logger.info(f"模拟WTI:弹射起步提示信息总线信号")
            self.set_singal("chassiscan1", "EcmChas1Fr25", "LnchModSts",value)
            pass
        if func.name == "ReLeSeatHeatWarning":
            logger.info(f"模拟WTI:后排左座椅加热故障报警总线信号")
            self.set_singal("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecLe",value)
            pass
        if func.name == "ReRiSeatHeatWarning":
            logger.info(f"模拟WTI:后排右座椅加热故障报警总线信号")
            self.set_singal("bodycan", "SmbBodyFr00", "SeatHeatgAvlStsRowSecRi",value)
            pass
        if func.name == "ReLeSeatVentWarning":
            logger.info(f"模拟WTI:后排左座椅通风故障报警总线信号")
            self.set_singal("bodycan", "SmbBodyFr01", "SeatVentAvlStsRowSecLe",value)
            pass
        if func.name == "ReRiSeatVentWarning":
            logger.info(f"模拟WTI:后排右座椅通风故障报警总线信号")
            self.set_singal("bodycan", "SmbBodyFr01", "SeatVentAvlStsRowSecRi",value)
            pass
        if func.name == "VehicleBaselineInconsistent":
            logger.info(f"模拟WTI:整车软件版本未拉齐总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "HVBatteryThermalSts":
            logger.info(f"模拟WTI:高压电池热管理状态提示总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "DrvWirelessChargingRemind":
            logger.info(f"模拟WTI:主驾无线充电故障状态提示总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "ChargingGunConnectSts":
            logger.info(f"模拟WTI:充电枪连接状态")
            self.set_singal("propulsioncan", "BecmPropFr15", "DCChrgnHndlSts",value)
            pass
        if func.name == "PassWirelessChargingRemind":
            logger.info(f"模拟WTI:副驾无线充电故障状态提示总线信号")
            #self.set_singal("", "", "",value)
            pass
        if func.name == "PowerSysFailed":
            logger.info(f"模拟WTI:动力系统故障灯")
            self.set_singal("chassiscan2", "EcmChas2Fr19", "HybErrIndcnReqTelltlSysHybFailr",value)
            pass
        if func.name == "HighVoltBattFailed_1":
            logger.info(f"模拟WTI:动力电池故障灯")
            self.set_singal("chassiscan2", "EcmChas2Fr19", "HybErrIndcnReqTelltlBattTracCutOff",value)
            pass
        if func.name == "HighVoltBattFailed_2":
            logger.info(f"模拟WTI:动力电池故障灯")
            self.set_singal("chassiscan2", "EcmChas2Fr19", "HybErrIndcnReqTelltlBattTracFailr",value)
            pass
        if func.name == "BatteryTempLow":
            logger.info(f"模拟WTI:电池低温指示灯")
            self.set_singal("backbonefr", "VddmBackBoneFr19", "HvBattCellTInfoHvBattTMin",value)
            pass  
        if func.name == "HighVolIsolation":
            logger.info(f"模拟WTI:高压绝缘信息")
            self.set_singal("propulsioncan", "BecmPropFr08", "HvIsoFlt",value)
            pass   
        if func.name == "EPBWork_1":
            logger.info(f"模拟WTI:EPB指示灯")
            self.set_singal("backbonefr", "BcmVddmBackBoneFr39", "EpbLampReqEpbLampReq",value)
            pass
        if func.name == "EPBWork_2":
            logger.info(f"模拟WTI:EPB指示灯")
            self.set_singal("backbonefr", "BbmBackBoneFr04", "EpbLampReqSecEpbLampReq",value)
            pass
        if func.name == "BrakingSysFailedYellow":
            logger.info(f"模拟WTI:EPB制动故障灯黄色")
            self.set_singal("backbonefr", "BcmVddmBackBoneFr39", "BrkSysWarnIndcnReq",0)
            self.set_singal("backbonefr", "BbmBackBoneFr04", "BrkSysWarnIndcnReqSec",0)
            self.set_singal("backbonefr", "BcmVddmBackBoneFr39", "BrkAndAbsWarnIndcnReqBrkWarnIndcnReq",value)
            pass
        if func.name == "BrakingSysFailedRed_1":
            logger.info(f"模拟WTI:EPB制动故障灯黄色")
            self.set_singal("backbonefr", "BcmVddmBackBoneFr39", "BrkFldLvl",value)
            pass
        if func.name == "BrakingSysFailedRed_2":
            logger.info(f"模拟WTI:EPB制动故障灯黄色")
            self.set_singal("backbonefr", "BcmVddmBackBoneFr39", "BrkMsgWarnReq",value)
            pass
        if func.name == "HDCGrey":
            logger.info(f"模拟WTI:HDC陡坡缓降指示灯灰色")
            self.set_singal("backbonefr", "BcmVddmBackBoneFr08", "MsgReqByHillDwnCtrl",value)
            pass
        if func.name == "ABSFailed":
            logger.info(f"模拟WTI:ABS故障指示灯,usagemode出现跳变")
            self.set_singal("backbonefr", "BcmVddmBackBoneFr39", "BrkAndAbsWarnIndcnReqAbsWarnIndcnReq",value)
            pass
       
        if func.name == "ESCFailed":
            logger.info(f"模拟WTI:ESC故障指示灯")
            self.set_singal("backbonefr", "BcmVddmBackBoneFr08", "EscWarnIndcnReqEscWarnIndcnReq",value)
            pass
        
        if func.name == "ESCOff_1":
            logger.info(f"模拟WTI:ESC关闭指示灯")
            self.set_singal("backbonefr", "BcmVddmBackBoneFr39", "DrvModEscOffDrvModEscOff",value)
            pass

        if func.name == "ESCOff_2":
            logger.info(f"模拟WTI:ESC关闭指示灯")
            self.set_singal("backbonefr", "BcmVddmBackBoneFr03", "EscStEscSt",value)
            pass 

        if func.name == "SteeringSysFailedYellow":
            logger.info(f"模拟WTI:转向系统故障指示灯黄色")
            self.set_singal("chassiscan1", "PscmChas1Fr03", "SteerErrReq",value)
            pass

        if func.name == "SuspensionFailed_1":
            logger.info(f"模拟WTI:悬架故障指示灯")
            self.set_singal("chassiscan2", "SumChas2Fr05", "SuspFailrStsTypQf",2)
            self.set_singal("chassiscan2", "SumChas2Fr05", "SuspFailrStsSuspFailrSts",value)
            pass
        
        if func.name == "SuspensionFailed_2":
            logger.info(f"模拟WTI:悬架故障指示灯")
            self.set_singal("chassiscan2", "SumChas2Fr05", "SuspFailrStsTypQf",2)
            self.set_singal("chassiscan2", "SumChas2Fr05", "SuspFailrSts3",value)
            pass

        if func.name == "AutoholdActiveGreen":
            logger.info(f"模拟WTI:Autohold激活指示灯")
            self.set_singal("backbonefr", "BcmVddmBackBoneFr39", "AutHldSoftSwtEnaSts",value)
            # self.set_singal("backbonefr", "BcmVddmBackBoneFr04", "LampReqByVehHld",value)
            self.set_singal("backbonefr", "CemBackBoneFr06", "DoorDrvrStsWithFacQlyDoorSts",2)
            self.set_singal("backbonefr", "CemBackBoneFr06", "DoorDrvrStsWithFacQlyFacQly",3)
            self.set_singal("backbonefr", "AsdmBackBoneFr10", "SmartAutoHldCtrlSts",0)
            self.set_singal("backbonefr", "SrsBackBoneFr05", "BltLockStAtDrvrBltLockSt1",1)
            pass

        if func.name == "AutoholStandbyGrey":
            logger.info(f"模拟WTI:Autohold待命指示灯")
            # self.set_singal("backbonefr", "BcmVddmBackBoneFr39", "AutHldSoftSwtEnaSts",value)
            self.set_singal("backbonefr", "BcmVddmBackBoneFr04", "LampReqByVehHld",value)
            pass
        
        if func.name == "ChargingGunConnectSts":
            logger.info(f"模拟WTI:充电枪连接指示")
            self.set_singal("propulsioncan", "BecmPropFr15", "DCChrgnHndlSts",value)
            pass
        
    def check_windows_position_req(self, pos_drvr: Union[WinPos, None] = None, pos_pass: Union[WinPos, None] = None,
                             pos_lere: Union[WinPos, None] = None, pos_rire: Union[WinPos, None] = None):
        with allure.step("Check BGM 发出的窗户的开关请求"):
            check_list = []
            target_msg = self.ipdu.bodycan.CemBodyFr68
            if pos_drvr is not None:
                logger.info(f"--------->Check BGM发出主驾窗户开关请求为{pos_drvr.name}")
                check_list.append((target_msg, "WinOpenDrvrReq", pos_drvr.value))

            if pos_pass is not None:
                logger.info(f"--------->Check BGM发出副驾窗户开关请求为{pos_pass.name}")
                check_list.append((target_msg, "WinOpenPassReq", pos_pass.value))

            if pos_lere is not None:
                logger.info(f"--------->Check BGM发出左后窗户开关请求为{pos_lere.name}")
                check_list.append((target_msg, "WinOpenReLeReq", pos_lere.value))

            if pos_rire is not None:
                logger.info(f"--------->Check BGM发出右后窗户开关请求为{pos_rire.name}")
                check_list.append((target_msg, "WinOpenReRiReq", pos_rire.value))
    
            self.ipdu.check_multiple_signals(check_list, timeout=2)
            self.ipdu.reset_check_results()
    

    def check_four_windows_position_req(self,pos:WinPos):
        promt_info = f"--------------->同时Check BGM 发出的4个窗户的位置请求是否为：{pos.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.check_windows_position_req(pos_drvr = pos, pos_pass=pos, pos_lere=pos, pos_rire=pos)

    
    def check_windows_short_drop_req(self, pos_drvr: Union[WinShortDropReq, None] = None, pos_pass: Union[WinShortDropReq, None] = None,
                             pos_lere: Union[WinShortDropReq, None] = None, pos_rire: Union[WinShortDropReq, None] = None):
        with allure.step("Check BGM 发出的窗户短降请求"):
            check_list = []
            target_msg = self.ipdu.bodycan.CemBodyFr103
            if pos_drvr is not None:
                logger.info(f"--------->Check BGM发出主驾窗户短降请求为{pos_drvr.name}")
                # self.check("bodycan", "CemBodyFr103", 'ShortDropWinDrvrDoor', pos_drvr.value)
                check_list.append((target_msg, "ShortDropWinDrvrDoor", pos_drvr.value))
            if pos_pass is not None:
                logger.info(f"--------->Check BGM发出副驾窗户短降请求为{pos_pass.name}")
                # self.check("bodycan", "CemBodyFr103", 'ShortDropWinPassDoor', pos_pass.value)
                check_list.append((target_msg, "ShortDropWinPassDoor", pos_pass.value))
            if pos_lere is not None:
                logger.info(f"--------->Check BGM发出左后窗户短降请求为{pos_lere.name}")
                # self.check("bodycan", "CemBodyFr103", 'ShortDropWinLeReDoor', pos_lere.value)
                check_list.append((target_msg, "ShortDropWinLeReDoor", pos_lere.value))
            if pos_rire is not None:
                logger.info(f"--------->Check BGM发出右后窗户短降请求为{pos_rire.name}")
                # self.check("bodycan", "CemBodyFr103", 'ShortDropWinRiReDoor', pos_rire.value)
                check_list.append((target_msg, "ShortDropWinRiReDoor", pos_rire.value))
            
            self.ipdu.check_multiple_signals(check_list, timeout=2)
            self.ipdu.reset_check_results()


    def check_four_windows_short_drop_req(self,pos:WinShortDropReq):
        promt_info = f"--------------->同时Check BGM 发出的4个窗户的短降请求是否为：{pos.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.check_windows_short_drop_req(pos_drvr = pos, pos_pass=pos, pos_lere=pos, pos_rire=pos)

    def set_5_door_lock_status(self, status:CenLockSts):
        logger.info("设置5门锁的状态为{}".format(status.name))
        if status.name == "Lock":
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, "DoorDrvrLockSts", 3)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, "DoorPassLockSts", 3)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, "DoorLeReLockSts", 3)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, "DoorRiReLockSts", 3)
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, "TrOpenerSts", 1)
        elif status.name == "Unlock":
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, "DoorDrvrLockSts", 1)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, "DoorPassLockSts", 1)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, "DoorLeReLockSts", 1)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, "DoorRiReLockSts", 1)
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, "TrOpenerSts", 1)
    
    def set_4_door_lock_status(self, lock_sts:Locksts):
        logger.info(f"同时设置4门锁的状态为{lock_sts.name}")
        self.set_door_lock_sts(drv_lock=lock_sts, pass_lock=lock_sts, rire_lock=lock_sts, lere_lock=lock_sts)
        # if status.name == "Lock":
        #     self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, "DoorDrvrLockSts", 3)
        #     self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, "DoorPassLockSts", 3)
        #     self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, "DoorLeReLockSts", 3)
        #     self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, "DoorRiReLockSts", 3)
        #     self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, "TrOpenerSts", 1)
        # elif status.name == "Unlock":
        #     self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, "DoorDrvrLockSts", 1)
        #     self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, "DoorPassLockSts", 1)
        #     self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, "DoorLeReLockSts", 1)
        #     self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, "DoorRiReLockSts", 1)
        #     self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, "TrOpenerSts", 1)
    
    def check_windows_without_short_drop_req(self, pos_drvr: Union[WinPos, None] = None, pos_pass: Union[WinPos, None] = None,
                             pos_lere: Union[WinPos, None] = None, pos_rire: Union[WinPos, None] = None):
        with allure.step("Check BGM 发出的窗户短降请求"):
            check_list = []
            target_msg = self.ipdu.bodycan.CemBodyFr103
            if pos_drvr is not None:
                logger.info(f"--------->Check BGM发出主驾窗户短降请求为{pos_drvr.name}%")
                # self.check("bodycan", "CemBodyFr103", 'ShortDropWinDrvrDoor', pos_drvr.value)
                check_list.append((target_msg, "ShortDropWinDrvrDoor", pos_drvr.value))
            if pos_pass is not None:
                logger.info(f"--------->Check BGM发出副驾窗户短降请求为{pos_pass.name}")
                # self.check("bodycan", "CemBodyFr103", 'ShortDropWinPassDoor', pos_pass.value)
                check_list.append((target_msg, "ShortDropWinPassDoor", pos_pass.value))
            if pos_lere is not None:
                logger.info(f"--------->Check BGM发出左后窗户短降请求为{pos_lere.name}")
                # self.check("bodycan", "CemBodyFr103", 'ShortDropWinLeReDoor', pos_lere.value)
                check_list.append((target_msg, "ShortDropWinLeReDoor", pos_lere.value))
            if pos_rire is not None:
                logger.info(f"--------->Check BGM发出右后窗户短降请求为{pos_rire.name}")
                # self.check("bodycan", "CemBodyFr103", 'ShortDropWinRiReDoor', pos_rire.value)
                check_list.append((target_msg, "ShortDropWinRiReDoor", pos_rire.value))
            
            result = self.ipdu.check_multiple_signals(check_list, timeout=2,do_assert=False)
            logger.info(f"------------->{result}")
            assert result[0] == False
            self.ipdu.reset_check_results()


    def check_pos_laom_act_sts(self, actn_sts: isOn,pos:GeneralPos, extr_light_sts: ExtrLtgSts):
        promt_info = f"----------------> Check 位置灯的状态是否ActnOfLedPosnLamp:{actn_sts.name},ExtrLtgStsPosLiRe,ExtrLtgStsPosLiFrnt :{extr_light_sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedPosnLamp',
                            actn_sts.value)
            if pos.name == "Rear":
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiRe',
                            extr_light_sts.value)
            if pos.name == "Front":
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsPosLiFrnt',
                            extr_light_sts.value)

    def start_record_trace_log(self, file_name):
        return self.bus_app.start_record_trace_log(file_rename=file_name)

    def stop_record_trace_log(self, is_record_status=True):
        return self.bus_app.stop_record_trace_log(is_record_status=is_record_status)
    
    def check_bus_recv_message(self, bus_name, timeout=5):
        return self.ipdu.check_bus_recv_message(bus_name, timeout=timeout)

    def check_ecu_not_recv_message(self, ecu_name, timeout=5):
        return self.ipdu.check_ecu_not_recv_message(self, ecu_name, timeout=timeout)
    
    def check_RTC_time(self,rtc_time):
        with allure.step("查询RTC唤醒时间"):
            self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'TiLVBattChrgn', rtc_time)


    def set_BMS_wukeup_mode(self,bms_type:BattSnsrType,wakeup_src:BMSWakeUpTrgSrc):
        prompt_info = f"---------->设置BMS补电方式为{bms_type.name},BMS补电激活状态为{wakeup_src.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr05, 'BattSnsrType', bms_type.value)
            logger.info(f"----------------> BMS触发补电")
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr07, 'BMSWakeUpTrgSrc', wakeup_src.value)

    def set_BMS_stop_req(self,low_sts:SocSts,
                         low_soc:Union[float, int, None] = None,
                         low_soh:Union[float, int, None] = None
                         ):
        prompt_info = f"---------->设置BMS采集电池信息"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            logger.info(f"---------->设置BMS采集电池STS为:{low_sts.name}")
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr07, 'BattSocSts', low_sts.value)
            if low_soc is not None:
                logger.info(f"---------->设置BMS采集电池SOC为：{low_soc}")
                self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr05, 'BattSocRaw', low_soc)
            if low_soh is not None:
                logger.info(f"---------->设置BMS采集电池SOH为：{low_soh}")
                self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr07, 'BattSOHLAMRaw', low_soh)
                

    def check_cem_and_vmm_communication_error(self,fault_sts:GeneralFltSts):
        prompt_info = f"---------->Check CEM和VMM通信故障状态是否为{fault_sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr18, 'WiprSysFailrDetdSafe', fault_sts.value)

    
    def set_rain_detect_sts(self,sts:bool,time_wait: Union[float, int] = 0):
        prompt_info = f"---------->设置检测到下雨的状态为{sts}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'RainDetected', sts)
            expectedvalue = self.ipdu.get_recent_signal_raw_value(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'RainDetected')
            logger.info(f"获取实际的雨天状态为:{expectedvalue}")

        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)

    def check_hv_volt_warning(self,LVChrgnFailWarn:Motorola):
        with allure.step(f"检测低压补电失败告警状态{LVChrgnFailWarn.name}"):
            self.check('connectivitycanfd', 'BgmConnectivityFr06', 'LVChrgnFailWarn', LVChrgnFailWarn.value)
            logger.info(f"检测低压补电失败告警状态{LVChrgnFailWarn.name}")

    def check_win_without_pos_req(self, pos_drvr: Union[WinPos, None] = None, pos_pass: Union[WinPos, None] = None,
                             pos_lere: Union[WinPos, None] = None, pos_rire: Union[WinPos, None] = None,timeout:Union[int,float] = 2):
        with allure.step(f"Check 在条件不满足的情况下BGM不发送开窗请求"):
            logger.info(f"Check 在条件不满足的情况下BGM不发送开窗请求")

            if pos_drvr is not None:
                logger.info(f"--------->Check BGM没有发出主驾窗户开关请求")
                ori_data = self.ipdu.check_signal(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq',timeout=timeout)
                value = pos_drvr.value

            if pos_pass is not None:
                logger.info(f"--------->Check BGM没有发出副驾窗户开关请求")
                ori_data = self.ipdu.check_signal(self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq',timeout=timeout)
                value = pos_pass.value

            if pos_lere is not None:
                logger.info(f"--------->Check BGM没有发出左后窗户开关请求")
                ori_data = self.ipdu.check_signal(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq',timeout=timeout)
                value = pos_lere.value

            if pos_rire is not None:
                logger.info(f"--------->Check BGM没有发出右后窗户开关请求")
                ori_data = self.ipdu.check_signal(self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq',timeout=timeout)
                value = pos_rire.value

            logger.info(f"获取{timeout}秒原始数据是:{ori_data}")
            check_result = get_signal_times_interval(ori_data, value)
            logger.info(f"Check 结果是：{check_result}")
            assert check_result[0] == 0

    
    def check_close_win_dueto_rain_sts(self,sts:bool):
        prompt_info = f"---------->BGM是否发送雨天关窗状态信号状态是否为{sts}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr08, 'ClsdDueToRain', sts)


    
    def check_without_close_win_dueto_rain_req(self):
        prompt_info = f"---------->BGM没有发送雨天关窗状态信号到TCAM"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            ori_data = self.ipdu.check_signal(self.ipdu.connectivitycanfd.VgmConnFr08, 'ClsdDueToRain')
            logger.info(f"获取原始数据是:{ori_data}")
            check_result = check_all_value_is(ori_data, 0)
            logger.info(f"Check 结果是：{check_result}")
            assert check_result

    def get_lin_scheduleTable(self, lin_bus):
        return self.ipdu.get_lin_scheduleTable(lin_bus)

    def _jsonpath_query(self, query, data):
        return [match.value for match in ng_parse(query).find(data)]

    def _check_lin_schedule_table(self, lin_bus, check_field=None, check_value=None, need_new_data=False):
        if not self.lin_schedule_data:
            self.lin_schedule_data = self.ipdu.get_lin_scheduleTable(lin_bus)
            logger.info(f"当前lin调度数据：{self.lin_schedule_data}")
        else:
            if need_new_data:
                self.lin_schedule_data = self.ipdu.get_lin_scheduleTable(lin_bus)
                logger.info(f"当前lin调度数据：{self.lin_schedule_data}")
        try:
            matches = self._jsonpath_query(check_field, self.lin_schedule_data)[0]
        except IndexError:
            raise AssertionError('not found selected attr!')
        if isinstance(matches, bool):
            check_value = eval(check_value)

        if isinstance(matches, int):
            check_value = int(check_value)

        if isinstance(matches, float):
            check_value = float(check_value)

        if check_value != matches:
            raise AssertionError("Expected: {}\n\nWas: {}".format(check_value, matches))

    def set_lidar_req(self, Lidar: Union[RelaySts, None] = None):
        with allure.step(f"设置雷达电源请求上电状态"):
            if Lidar is not None:
                logger.info(f"check雷达电源请求上电状态{Lidar.name}")
                self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr05, 'LidarPowerReq',
                              Lidar.value)
    
    def set_tire_config_req(self):
        with allure.step(f"触发胎压配置请求"):
            logger.info(f"触发胎压配置请求")
            self.ipdu.send_pdu("connectivitycanfd", 0x345, [0x00, 0x00, 0x00, 0x00, 0x00, 0x0A, 0x00, 0x00])      
    
    def check_tire_config(self, id: list, config: list, is_id: bool, is_config: bool):
        check_list_1 = []
        check_list_2 = []
        target_msg1 = self.ipdu.connectivitycanfd.BgmConnectivityFr17
        target_msg2 = self.ipdu.connectivitycanfd.BgmConnectivityFr16
        if is_id:
            check_signal_1 = ['FilterIDID1', 'FilterIDID2', 'FilterIDID3', 'FilterIDID4']
            for i in range(len(id)):
                check_list_1.append((target_msg1, check_signal_1[i], id[i]))
                logger.info(f"检查信号为{check_signal_1[i]}， 检查的值为{id[i]}")
        if is_config:
            check_signal_2 = ['TireFilFilSwt', 'TireFilNoiseFlrSwt', 'TireFilRxSwt',  'TireFilPollingMod', 'TireFilSnsrID']
            for j in range(len(config)):
                check_list_2.append((target_msg2, check_signal_2[j], config[j]))
                logger.info(f"检查信号为{check_signal_2[j]}， 检查的值为{config[j]}")
        if is_id:
            self.ipdu.check_multiple_signals(check_list_1, timeout=2)
        if is_config:
            self.ipdu.check_multiple_signals(check_list_2, timeout=2)
        self.ipdu.reset_check_results()

    def check_drl_act_sts(self, actn_sts: isOn, extr_light_sts: ExtrLtgSts):
        promt_info = f"----------------> Check 日行灯的状态是否 ActnOfLedDaytiRunngLamp:{actn_sts.name},日行灯状态是否为 ExtrLtgStsDRL:{extr_light_sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedDaytiRunngLamp', actn_sts.value)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsDRL', extr_light_sts.value)
            
    def check_high_beam_sts(self, hb_actn_sts:isOn, extr_light_sts: ExtrLtgSts,flash_light_sts:ExtrLtgSts):
        promt_info = f"----------------> Check 远光灯激活的状态是否 ActnOfLedHiBeam:{hb_actn_sts.name},外灯状态是否为 ExtrLtgStsHiBeam:{extr_light_sts.name},外部闪光灯状态是否为{flash_light_sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedHiBeam', hb_actn_sts.value)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsHiBeam', extr_light_sts.value)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsFlash', flash_light_sts.value)
            
    def set_drl_fault_sts(self, pos: GeneralPos, fault_sts: LampSts):
        promt_info = f"---------------->设置{pos.name}日行灯故障状态{fault_sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "Right":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr04, 'StsOfLedDaytiRunngLampRi', fault_sts.value)

            elif pos.name == "Left":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLedDaytiRunngLampLe', fault_sts.value)

            elif pos.name == "All":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr04, 'StsOfLedDaytiRunngLampRi', fault_sts.value)
                self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLedDaytiRunngLampLe', fault_sts.value)

    def set_pedal(self,sts:Union[None,YesOrNo] = YesOrNo.Yes):
        prompt_info = f"---------->设置踩刹车踏板"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if sts is not None:
                logger.info(f"刹车踏板状态设为{sts.name}")
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', sts.value)


    def set_child_lock_sts(self,pos:GeneralPos,sts:ChdLockSts):
        prompt_info = f"---------->设置{pos.name}对应儿童锁状态为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if pos.name == "Left":
                self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01,"ChdLockLeftSts",sts.value)
            elif pos.name == "Right":
                self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01,"ChdLockRightSts",sts.value)
    def check_reverse_lamp_act_sts(self, actn_sts: isOn, extr_light_sts: ExtrLtgSts):
        promt_info = f"----------------> Check 倒车灯的状态是否 ActnOfLedRvsgLamp:{actn_sts.name},ExtrLtgStsReverseLi:{extr_light_sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedRvsgLamp',
                            actn_sts.value)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsReverseLi', extr_light_sts.value)


    def set_reverse_lamp_fault_sts(self, pos: GeneralPos, fault_sts: LampSts):
        promt_info = f"---------------->设置{pos.name}倒车灯故障状态{fault_sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "Right":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedRvsgLampRi1', fault_sts.value)

            elif pos.name == "Left":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedRvsgLampLe1', fault_sts.value)

            elif pos.name == "All":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01, 'StsOfLedRvsgLampRi1', fault_sts.value)
                self.ipdu.set(self.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedRvsgLampLe1', fault_sts.value)

    def set_drvrdes_sts(self, drvrdes: DrvrDesDir):
        promt_info = f"----------------> 设置车辆挡位 DrvrDesDirDrvrDesDir:{drvrdes.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr10, 'DrvrDesDirDrvrDesDir',
                            drvrdes.value)
            
    
    def set_accr_pedl_press_act(self, act: isOn):
        promt_info = f"---------------->设置车辆挡位车辆加速踏板踩下:{act.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd',act.value)


    def set_accr_pedl_press_sts(self, sts: isOn):
        promt_info = f"---------------->设置车辆挡位车辆加速踏板踩下状态为:{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdSts',sts.value)

    
    def check_brake_light_act_cycle_sts(self):
        promt_info = f"---------------->查看刹车灯是否循环亮灭,包括激活刹车灯:ActnOfLedStopLampActnOfLedStopLamp和激活中央刹车灯:ActnOfLedStopLampMid)"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.check_event_thread_start(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedStopLampActnOfLedStopLamp',0,1,3)
            self.ipdu.check_event_thread_start(self.ipdu.bodyexposedcanfd.BgmBodyExposedCANFr01, 'ActnOfLedStopLampMid',0,1,3) 
            sleep(3)
            event_times_1 = self.ipdu.check_event_thread_stop('ActnOfLedStopLampActnOfLedStopLamp')
            event_times_2 = self.ipdu.check_event_thread_stop('ActnOfLedStopLampMid')

            logger.info(f"激活刹车灯:ActnOfLedStopLampActnOfLedStopLamp和激活中央刹车灯:ActnOfLedStopLampMid Check结果分别为{event_times_1}和{event_times_2}")
            assert event_times_1 >=3 and event_times_2 >=3
    
    def check_tailgate_without_opener_req(self, timeout=1):
        with allure.step(f"Check 在条件不满足的情况下BGM不发送尾门开关停动作请求"):
            logger.info(f"Check 在条件不满足的情况下BGM不发送尾门开关停动作请求")
            ori_data = self.ipdu.check_signal(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', timeout)
            logger.info(f"获取{timeout}秒内的TrOpenerReqTrOpenerReq原始数据是:{ori_data}")
            check_result = check_all_value_is(ori_data, 0)
            logger.info(f"Check 结果是：{check_result}")
            assert check_result
    
    def check_tailgate_without_opener_rels(self, timeout=1):
        with allure.step(f"Check 在条件不满足的情况下BGM不发送尾门电释放请求"):
            logger.info(f"Check 在条件不满足的情况下BGM不发送尾门电释放请求")
            ori_data = self.ipdu.check_signal(self.ipdu.bodycan.BgmBodyFr01, 'TrRelsReq', timeout)
            logger.info(f"获取{timeout}秒内的尾门电释放请求TrRelsReq原始数据是:{ori_data}")
            # check_result = check_all_value_is(ori_data, DoorRelsReq.Off)
            check_result = check_all_value_is(ori_data, 2)
            logger.info(f"Check 结果是：{check_result}")
            assert check_result

    
    def set_steer_wheel_touch_switch_sts(self,pos:SteerWhlTouchSwtPos,sts:SteerWhlTouchSwtSts):
        promt_info = f"---------------->设置{pos.name}方向盘按键状态为:{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "Left3":
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3',sts.value)
            elif pos.name == "Right3":
                self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3',sts.value)
            if pos.name == "Left2":
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2',sts.value)
            elif pos.name == "Right2":
                self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2',sts.value)
            if pos.name == "Left1":
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2',sts.value)
            elif pos.name == "Right1":
                self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi1SteerWhlTouchSwt2',sts.value)
            elif pos.name == "All":
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3',sts.value)
                self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3',sts.value)
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2',sts.value)
                self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2',sts.value)
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2',sts.value)
                self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi1SteerWhlTouchSwt2',sts.value)

                
    
    def set_cllsnthreat(self, cllsnthreat: CllsnThreat1):
        with allure.step(f"设置子系统的危险级别"):
            self.set('backbonefr', 'AsdmBackBoneFr03', 'CllsnThreat', cllsnthreat.value)
            logger.info(f"设置子系统的危险级别成功")
    
    def set_batturaw(self, BattURaw: int):
        with allure.step(f"设置电池电压"):
            # batturaw1 = (BattURaw - 5) * 40
            #self.set('cem_lin6', 'BmsCem_Lin6Fr05', 'BattURaw', batturaw1)
            self.set('cem_lin6', 'BmsCem_Lin6Fr05', 'BattURaw', BattURaw)
            logger.info(f"设置电池电压成功,设置的电池电压为{BattURaw}V")

    def set_battiraw(self, BattIRaw: int):
        with allure.step(f"设置电池电流"):
            battiraw1 = (BattIRaw + 512) * 64
            self.set('cem_lin6', 'BmsCem_Lin6Fr01', 'BattIRaw', battiraw1)
            logger.info(f"设置电池电流成功,设置的电池电流为 {BattIRaw}A")

    def set_fltelecdcdc(self, fltelecdcdc: BattSnsrHwFltRaw):
        with allure.step(f"设置DCDC的电气故障指示"):
            self.set('backbonefr', 'VddmBackBoneFr21', 'FltElecDcDc', fltelecdcdc.value)
            logger.info(f"设置DCDC的电气故障指示")

    def set_flttdcdc(self, flttdcdc: BattSnsrHwFltRaw):
        with allure.step(f"设置DCDC的温度故障指示"):
            self.set('backbonefr', 'VddmBackBoneFr15', 'FltTDcDc', flttdcdc.value)
            logger.info(f"设置DCDC的温度故障指示")

    def check_pwrlvlelec(self, mai: int, subtype: int):
        with allure.step(f"检查车辆的电功率水平"):
            self.check('backbonefr', 'CemBackBoneFr02', 'VehModMngtGlbSafe1PwrLvlElecMai', mai)
            self.check('backbonefr', 'CemBackBoneFr02', 'VehModMngtGlbSafe1PwrLvlElecSubtyp', subtype)
            logger.info(f"检查车辆的电功率水平无问题，主状态为{mai}, 子状态为{subtype}")

    def set_battsoc_less_15(self):
        with allure.step(f"设置battsoc的状态小于15"):
            flag = 0
            self.set('cem_lin6', 'BmsCem_Lin6Fr05', 'BattSocRaw', 100.0)
            self.set_batturaw(BattURaw=15.0)
            self.set('cem_lin6', 'BmsCem_Lin6Fr01', 'BattIRaw', 1.0)
            self.set('cem_lin6', 'BmsCem_Lin6Fr03', 'BattTRaw', 40.0)
            self.set('cem_lin6', 'BmsCem_Lin6Fr03', 'BattCpEstimdRaw', 80.0)
            logger.info(f"-------->检查BattSoc2Sts是否为1或2")
            timer = 0
            while timer < 600:
                receive_result = self.ipdu.get_recent_signal_raw_value(self.ipdu.connectivitycanfd.BgmConnectivityFr06,
                                                                    'BattSoc2Sts')
                logger.info(f"-------->通过总线上的信号获取BattSoc2Sts值为{receive_result}")
                if (receive_result == 1) | (receive_result) == 2:
                    logger.info("-------->获取到预期的BattSoc2Sts")
                    flag = 1
                    break
                else:
                    sleep(10)
                    timer = timer + 10
            if flag == 0:
                logger.info("-------->获取的实际BattSoc2Sts和期望的不一致")
                assert False
    
    
    def check_hb_fail_flag_sts(self, hb_flag_sts: ExtrLtgSts):
        promt_info = f"----------------> Check 远光灯是否激活是否满足条件 外灯状态是否为 Flash2HighBeamFailFlag:{hb_flag_sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr38, 'Flash2HighBeamFailFlag', hb_flag_sts.value)

    
    def trigger_steer_wheel_button(self,pos:SteerWhlTouchSwtPos,press_type:SteerWhlTouchSwtSts,press_time:Union[int,float] = 0.5):
        promt_info = f"---------------->触发{pos.name}方向盘按键,按压类型为{press_type}，按压持续时间为{press_time}秒"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "Left3":
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3',press_type.value)
                sleep(press_time)
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe3',0)
            elif pos.name == "Right3":
                self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3',press_type.value)
                sleep(press_time)
                self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi3',0)
            if pos.name == "Left2":
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2',press_type.value)
                sleep(press_time)
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2',0)
            elif pos.name == "Right2":
                self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2',press_type.value)
                sleep(press_time)
                self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi2SteerWhlTouchSwt2',0)
            if pos.name == "Left1":
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2',press_type.value)
                sleep(press_time)
                self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2',0)
            elif pos.name == "Right1":
                self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi1SteerWhlTouchSwt2',press_type.value)
                sleep(press_time)
                self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlTouchSwtRi1SteerWhlTouchSwt2',0)


    def check_turn_indicate_lamp_req(self, sts: IndcrSts):
        prompt_info = f"---------->Check 转向指示灯状态是否为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr51, 'IndcrSts', sts.value)


    def send_awakeup_msg(self,bus:str,id:int,payload:str,times:int,interval:int):
        prompt_info = f"---------->在总线{bus}上以时间间隔{interval}ms 循环发送{times}次 ID为：{id}，负载为{payload}的报文"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            while times > 0:
                self.send_pdu(bus,id, payload)
                sleep(interval*0.001)
                times = times -1
    
    def check_key_not_prsnt_msg_to_drvr(self, flag: bool):
         with allure.step(f"检查车辆是否无钥匙启动的HMI状态"):
            self.check('backbonefr', 'CemBackBoneFr14', 'KeyNotPrsntMsgToDrvr', flag)

    def set_strt_msg_to_mod_mngt(self, StrtMsgToModMngt: StrtMsgToModMngt):
         with allure.step(f"设置请求的启动的状态"):
            self.set('backbonefr', 'VddmBackBoneFr15', 'StrtMsgToModMngt', StrtMsgToModMngt.value)

    def check_strt_msg_to_drvrr(self, StrtMsgToDrvrg: StrtMsgToDrvrg):
         with allure.step(f"检查启动相关的信息显示"):
            self.check('backbonefr', 'CemBackBoneFr07', 'StrtMsgToDrvr', StrtMsgToDrvrg.value)

    def check_strtinprogs(self, StrtInProgs: StrtInProgs):
         with allure.step(f"检查启动和关闭动力系统的消息"):
            self.check('bodycan', 'CemBodyFr63', 'StrtInProgs', StrtInProgs.value)

    def set_trsm_park_lockd(self, TrsmParkLockd: TrsmParkLockd):
         with allure.step(f"设置驻车锁定状态"):
            self.set('backbonefr', 'VddmBackBoneFr18', 'TrsmParkLockdTrsmParkLockd', TrsmParkLockd.value)

    def check_veh_not_park_info_warn(self, VehNotParkInfoWarn: VehNotParkInfoWarn):
         with allure.step(f"检查未驻车提示告警"):
            self.check('backbonefr', 'CemBackBoneFr19', 'VehNotParkInfoWarn', VehNotParkInfoWarn.value)

    def set_gearlvrillmnSts(self, GearLvrIllmnSts: isOn):
         with allure.step(f"设置换挡器触摸状态"):
            self.set('propulsioncan', 'EgsmPropFr01', 'GearLvrIllmnSts', GearLvrIllmnSts.value)

    def check_crashunllock_failrSts(self, unlockfail: Union[Unlockfailtohmi, None] = None):
        with allure.step(f"获取总线Crash解锁失败状态"):
            if unlockfail is not None:
                logger.info(f"获取总线Crash解锁失败状态{unlockfail.name}")
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'CrashUnlckFailrSts',
                              unlockfail.value)
    
    def set_battcp_estimd(self, BattCpEstimdRaw: int):
        with allure.step(f"设置估计电池容量"):
            self.set('cem_lin6', 'BmsCem_Lin6Fr03', 'BattCpEstimdRaw', BattCpEstimdRaw)

    def check_egyavldelta(self, delta: int):
        with allure.step(f"检查电池的可用余量"):
            delta1 = delta + 16
            self.check('infocanfd', 'BgmInfoCanFdFr23', 'EgyAvlDelta', delta1)

    def check_egyavlwarn(self, warn: int):
        with allure.step(f"检查电池的发出告警前的可用能量"):
            warn1 = warn + 16
            self.check('infocanfd', 'BgmInfoCanFdFr23', 'EgyAvlToWarn', warn1)

    def check_egylvlelec(self, mai: int, subtype: int):
        with allure.step(f"检查车辆的能量水平"):
            self.check('backbonefr', 'CemBackBoneFr02', 'VehModMngtGlbSafe1EgyLvlElecMai', mai)
            self.check('backbonefr', 'CemBackBoneFr02', 'VehModMngtGlbSafe1EgyLvlElecSubtyp', subtype)
            logger.info(f"检查车辆的能量水平无问题，主状态为{mai}, 子状态为{subtype}")

    def set_battsocraw2_less_value(self, battsocraw2: int, wait_time: int=1000):
        flag = 0
        self.set_battiraw(BattIRaw=-100)
        with allure.step(f"检查battsoc的状态是否小于{battsocraw2}%"):
            timer = 0
            while timer < wait_time:
                receive_result = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.VgmBackBoneFr03,
                                                                    'BattSocRaw2')/10
                logger.info(f"-------->通过总线上的信号获取battsocraw2值为{receive_result}")
                if (receive_result <= battsocraw2):
                    logger.info("-------->获取到预期的battsocraw2")
                    flag = 1
                    break
                else:
                    if receive_result - battsocraw2 < 2:
                        sleep(1)
                        timer = timer + 1
                    else:
                        sleep(10)
                        timer = timer + 10
            if flag == 0:
                logger.info("-------->超时仍未获取到预期的battsocraw2")
                assert False

    def set_battsocraw2_more_value(self, battsocraw2: int, wait_time: int=2000):
        flag = 0
        self.set_battiraw(BattIRaw=100)
        with allure.step(f"检查battsoc的状态是否多于于{battsocraw2}%"):
            timer = 0
            while timer < wait_time:
                receive_result = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.VgmBackBoneFr03,
                                                                    'BattSocRaw2')/10
                logger.info(f"-------->通过总线上的信号获取battsocraw2值为{receive_result}")
                if (receive_result >= battsocraw2):
                    logger.info("-------->获取到预期的battsocraw2")
                    flag = 1
                    break
                else:
                    if battsocraw2 - receive_result < 2:
                        sleep(1)
                        timer = timer + 1
                    else:
                        sleep(10)
                        timer = timer + 10
            if flag == 0:
                logger.info("-------->超时仍未获取到预期的battsocraw2")
                assert False

    def wait_time_and_check_egylvlelec(self, mai_new: int, subtype_new: int, mai_old: int, subtype_old: int, time: int, ):
        timer = 0
        logger.info(f"开始检测未到达时间时是否保持历史值")
        while timer < time - 5:
            self.check_egylvlelec(mai=mai_old, subtype=subtype_old)
            sleep(5)
            timer = timer + 5
        sleep(time - timer)
        logger.info(f"开始检测到达时间时是否变为期望值")
        self.check_egylvlelec(mai=mai_new, subtype=subtype_new)

    def set_crashsts_safests(self, CrashSts: crashsts):
        with allure.step(f"设置crash状态信号"):
            self.set('backbonefr', 'SrsBackBoneFr05', 'CrashStsSafeSts', CrashSts.value)

    def check_egylvlelec_drvinfo(self, info: int):
        with allure.step(f"检查能量通知"):
            self.check('backbonefr', 'CemBackBoneFr18', 'EgyLvlElecDrvInfo', info)
            
    def set_rain_sensor_fault_sts(self,type:RainSensorFaultType,sts:bool):
        promt_info = f"---------------->设置雨量传感器系统故障类型为{type.name}，状态为:{sts}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if sts == True:
                if type.name == "SensorFault":
                    self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'RainSnsrErrRainDetnErr',1)
                    self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'RainSnsrErrRainDetnErrActv',1)

                elif type.name == "CalibrationFault":
                    self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'RainSnsrErrCalErr',1)
                    self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'RainSnsrErrCalErrActv',1)

                elif type.name == "All":
                    self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'RainSnsrErrCalErr',1)
                    self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'RainSnsrErrCalErrActv',1)
                    self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'RainSnsrErrRainDetnErr',1)
                    self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'RainSnsrErrRainDetnErrActv',1)
            else:
                if type.name == "SensorFault":
                    self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'RainSnsrErrRainDetnErr',0)
                    self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'RainSnsrErrRainDetnErrActv',0)

                elif type.name == "CalibrationFault":
                    self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'RainSnsrErrCalErr',0)
                    self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'RainSnsrErrCalErrActv',0)

                elif type.name == "All":
                    self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'RainSnsrErrCalErr',0)
                    self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'RainSnsrErrCalErrActv',0)
                    self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'RainSnsrErrRainDetnErr',0)
                    self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'RainSnsrErrRainDetnErrActv',0)
                
    def set_charging_sts(self, sts: ChargingSts):
        promt_info = f"---------------->设置车辆充电状态为:{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb',sts.value)

    def send_ccp_to_tcam(self, ccp_byte_index: Union[list, int] = [566], ccp_value: Union[list, int] = [0x10]):
        with allure.step(f"模拟BGM给TCAM发送CCP报文"):
            logger.info(f"发送的CCP字节序号为: {ccp_byte_index}, 对应CCP字节的: {ccp_value}")
            self.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
            time.sleep(1)
            if isinstance(ccp_byte_index, int):
                self.mock_bgm_send_ccp(byte_index_to_change=[ccp_byte_index], change_to_value=[ccp_value])
            else:
                self.mock_bgm_send_ccp(byte_index_to_change=ccp_byte_index, change_to_value=ccp_value)
            time.sleep(40)
            self.mock_ccp_flag = False  # 结束send ccp发送线程的flag
            self.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
            time.sleep(1)

    def check_wiper_mode_req(self,req:WiperMode):
        promt_info = f"---------------->检查BGM发出控制雨刮的请求是否为:{req.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.reset_check_results()
            target_msg = self.ipdu.cem_lin1.CemCem_Lin1Fr01
            if req.name == "Off":
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr07,"WipgInfoWipgSpdInfo",0)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",1)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInIntlPosn",0)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInSnglStrokePos",0)
            elif req.name == "Low":
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr07,"WipgInfoWipgSpdInfo",3)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",1)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInIntlPosn",0)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",2)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInSnglStrokePos",0)
            elif req.name == "High":
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr07,"WipgInfoWipgSpdInfo",6)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",2)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInIntlPosn",0)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInSnglStrokePos",0)
            elif req.name == "IntLow":
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr07,"WipgInfoWipgSpdInfo",1)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",1)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInIntlPosn",1)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInSnglStrokePos",0)
            elif req.name == "IntHigh":
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr07,"WipgInfoWipgSpdInfo",2)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",1)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInIntlPosn",1)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInSnglStrokePos",0)
            elif req.name == "SingleWipe":
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",1)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInIntlPosn",0)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInSnglStrokePos",1)
            elif req.name == "Auto":
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr07,"WipgInfoWipgSpdInfo",0)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",1)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInIntlPosn",0)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
                self.ipdu.check(target_msg, "WiprMotFrntLvrCmdSafeLvrInSnglStrokePos",0)
            sleep(1)
            self.ipdu.reset_check_results()

    def set_wpcmodule_sts(self, sts: WpcModule):
        promt_info = f"---------------->设置WPCModule状态{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, "WPCModuleSts", sts.value)


    def check_ahl_act_sts(self, actn_sts: isOn, extr_light_sts: ExtrLtgSts):
        prompt_info = f"---------->Check自动前照灯的状态是否为:ActvnOfAhl:{actn_sts.name},状态是否为:ExtrLtgStsAHL:{extr_light_sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActvnOfAhl', actn_sts.value)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, 'ExtrLtgStsAHL', extr_light_sts.value)

    def set_ahl_fault_sts(self, pos: GeneralPos, fault_sts: LampSts):
        promt_info = f"---------------->设置{pos.name}自动前照灯故障状态{fault_sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "Right":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr04, 'StsOfLvlgRiStsOfLvlgRi', fault_sts.value)

            elif pos.name == "Left":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLvlgLeStsOfLvlgLe', fault_sts.value)

            elif pos.name == "All":
                self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmrBodyExpoFr04, 'StsOfLvlgRiStsOfLvlgRi', fault_sts.value)
                self.ipdu.set(self.ipdu.bodyexposedcanfd.HcmlBodyExpoFr04, 'StsOfLvlgLeStsOfLvlgLe', fault_sts.value)

    def set_pib_sts(self, pib_sts: DiagActLineSts):
        promt_info = f"---------------->设置pib状态{pib_sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr19, 'IndcnToDrvrPostImpctCtrl', pib_sts.value)

    
    def set_wiper_mode(self, mode: WipgAutFrntMod):
        promt_info = f"---------------->模拟反馈雨刮模式为{mode.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, "WipgAutFrntMod", mode.value)

    
    def set_wiper_rain_level(self, level: int):
        promt_info = f"---------------->设置雨量大为{level}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'RainfallAmnt', level)

    
    def set_wiper_ambient_light_intensity(self,qf:Union[int,None]=None,value:Union[int,None]=None):
        promt_info = f"---------------->设置环境光强度{value}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if value is not None:
                self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawTwliBriRaw', value)
            if qf is not None:
                self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawQf', qf)

    
    def set_solar_value(self,left_vlaue:Union[int,None]=None,right_value:Union[int,None]=None):
        promt_info = f"---------------->设置阳光强度"
        with allure.step(promt_info):
            logger.info(promt_info)
            if left_vlaue is not None:
                logger.info(f"设置左边传感器的强度为{left_vlaue}")
                self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'SolarSnsrLeValue', left_vlaue)
            if right_value is not None:
                logger.info(f"设置右边传感器的强度为{right_value}")
                self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, 'SolarSnsrRiValue', right_value)
    
    def check_turn_lamp_always_off(self,pos:GeneralPos,last_time:Union[float,int]):
        promt_info = f"---------------->Check {pos.name}转向灯是否处于关闭状态"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "Left":
                self.check_signal_thread_start("backbonefr","CemBackBoneFr02", "ExtrLtgStsTurnIndrLe", timeout = last_time)
                self.check_signal_thread_start("bodycan", "CemBodyFr03", 'ActvnOfIndcrIndcrOut', timeout = last_time)
                sleep(last_time)
                result_ori_left = self.check_signal_thread_stop("ExtrLtgStsTurnIndrLe")
                result_ori_indcr = self.check_signal_thread_stop("ActvnOfIndcrIndcrOut")
                logger.info(f"result_ori_left:{result_ori_left},result_ori_indcr:{result_ori_indcr}")

                if check_all_value_is(result_ori_left, 0) and check_all_value_is(result_ori_indcr, 0):
                    assert True
                else:
                    logger.info("不是所有的值都是0")
                    assert False
            elif pos.name == "Right":
                self.check_signal_thread_start("backbonefr","CemBackBoneFr02", "ExtrLtgStsTurnIndrRi", timeout = last_time)
                self.check_signal_thread_start("bodycan", "CemBodyFr03", 'ActvnOfIndcrIndcrOut', timeout = last_time)
                sleep(last_time)
                result_ori_right = self.check_signal_thread_stop("ExtrLtgStsTurnIndrRi")
                result_ori_indcr = self.check_signal_thread_stop("ActvnOfIndcrIndcrOut")
                logger.info(f"result_ori_right:{result_ori_right},result_ori_indcr:{result_ori_indcr}")

                if check_all_value_is(result_ori_right, 0) and check_all_value_is(result_ori_indcr, 0):
                    assert True
                else:
                    logger.info("不是所有的值都是0")
                    assert False

            elif pos.name == "All":
                self.check_signal_thread_start("backbonefr","CemBackBoneFr02", "ExtrLtgStsTurnIndrLe", timeout = last_time)
                self.check_signal_thread_start("backbonefr","CemBackBoneFr02", "ExtrLtgStsTurnIndrRi", timeout = last_time)
                self.check_signal_thread_start("bodycan", "CemBodyFr03", 'ActvnOfIndcrIndcrOut', timeout = last_time)
                sleep(last_time)
                result_ori_left = self.check_signal_thread_stop("ExtrLtgStsTurnIndrLe")
                result_ori_right = self.check_signal_thread_stop("ExtrLtgStsTurnIndrRi")
                result_ori_indcr = self.check_signal_thread_stop("ActvnOfIndcrIndcrOut")
                logger.info(f"result_ori_left:{result_ori_left},result_ori_right:{result_ori_right},result_ori_indcr:{result_ori_indcr}")

                if check_all_value_is(result_ori_right, 0) and check_all_value_is(result_ori_left, 0) and check_all_value_is(result_ori_indcr, 0):
                    assert True
                else:
                    logger.info("不是所有的值都是0")
                    assert False

    def check_pnc_valid_last_time(self,
                  bus_name: BusName,
                  msg_id: NMMsgId,
                  pnc_name: Union[BGMPNC, TCAMPNC],
                  last_time: Union[int,float],
                  diff_time:Union[int,float] = 1.0):
        promt_info = f"---------------->检查总线{bus_name}上PNC：{pnc_name.name}置位的持续时间是否为{last_time}(允许{diff_time}秒的偏差)"
        with allure.step(promt_info):
            logger.info(promt_info)   
            self.ipdu.rx_flag_reset_bus(bus_name.value)
            if 'PNC' in pnc_name.value:
                try:
                    pnc_id = int(re.findall(r'PNC(\d+)_', pnc_name.value)[0])
                except (IndexError, TypeError):
                    err_msg= f"{pnc_name}不存在PNC ID"
                    logger.error(err_msg)
                    raise exception_error.IpduError(err_msg)

            recv_value = None
            flag = 0
            duration_time = 0
            recv_time_start = 0
            recv_time_stop = 0
            start_time = time.time()
            end_time = time.time()
            while end_time - start_time < (last_time+1):
                pdu_data = self.recv_pdu(bus_name=bus_name.value, id=msg_id.value)
                logger.info(f"获取的原始数据{pdu_data}")
                if pdu_data:
                    pdu_data = pdu_data[3]
                    recv_value = (pdu_data[pnc_id // 8] >> pnc_id % 8) & 1
                    if recv_value == 1 and flag == 0:
                        flag = 1
                        start_time = time.time()
                        recv_time_start = time.time()
                        logger.info(f"{pnc_name.name} 置位的开始时间 {recv_time_start}")
                    if recv_value == 1 and flag == 1:
                        recv_time_stop = time.time()
                    if recv_value == 0 and flag == 1:
                        flag = 0
                        break
                else:
                    logger.info(f"接收的报文为Null")
                    assert False
                end_time = time.time()

            if recv_time_stop !=0 and recv_time_start !=0:
                logger.info(f"{pnc_name.name} 置位的结束时间 {recv_time_stop}")
                duration_time = float(recv_time_stop - recv_time_start)
                logger.info(f"{pnc_name.name} 置位的持续时间 {duration_time}")

                if duration_time ==0 or abs(duration_time - last_time)>diff_time:
                    if duration_time ==0:
                        logger.info(f"PNC：{pnc_name.name}置位的持续时间超过{last_time}")
                    elif abs(duration_time - last_time)>diff_time:
                        logger.info(f"PNC：{pnc_name.name}置位的持续时间为{duration_time},误差超过{diff_time}s")
                    assert False
            else:
                logger.info(f"没有获取到PNC置位开始时间或者结束时间")
                assert False
  
    def check_keeperreq(self, usagemode:UsageMode):
        with allure.step(f"检查模式维持请求"):
            self.check('infocanfd', 'BgmInfoCanFdDevFr02', 'UsgModKeeperReq', usagemode.value, 0.2)

    def check_keeperreq_act(self, usagemode:UsageMode):
        with allure.step(f"检查模式请求仲裁"):
            self.check('infocanfd', 'BgmInfoCanFdDevFr02', 'UsgModKeeperReqAct', usagemode.value, 0.2)

    def check_carmode_dispd(self, carmoddisp1:CarModDisp1):
        with allure.step(f"检查carmode展示信息"):
            self.check('backbonefr', 'CemBackBoneFr14', 'CarModDispdWdDispd', carmoddisp1.value)

    def check_carmode_dispd_in_time(self,carmode:CarMode, subtype: int, carmoddisp1_old:CarModDisp1, carmoddisp1_new:CarModDisp1, time:int = 10, is_change:bool=True):
        with allure.step(f"检查{time}s内carmode为{carmode.value},carmoddisp为{carmoddisp1_old.value}"):
            timer = 0
            while timer < time - 1:
                self.check_carmode_dispd(carmoddisp1=carmoddisp1_old)
                self.check_car_mode_status(car_mode_main=carmode, car_mode_sub=subtype)
                sleep(1)
                timer = timer + 1
        logger.info(f"开始检测到达时间时是否变为期望值")
        sleep(1)
        if is_change:
            self.check_carmode_dispd(carmoddisp1=carmoddisp1_new)
            self.check_car_mode_status(car_mode_main=carmode, car_mode_sub=subtype)
        else:
            self.check_carmode_dispd(carmoddisp1=carmoddisp1_old)
            self.check_car_mode_status(car_mode_main=carmode, car_mode_sub=subtype)

    def check_key_nfc_vmm_prsnt(self, keyprsnt: Keyprsntsts):
        with allure.step(f"检查寻钥状态"):
            self.check('infocanfd', 'BgmInfoCanFdDevFr03', 'KeyReadStsToVMMNFCNFCKeyPrsnt', keyprsnt.value)

    def check_key_nfc_vmm_prsnt_in_time(self, keyprsnt_old: Keyprsntsts, keyprsnt_new: Keyprsntsts, time:int = 10, is_change:bool=True):
        with allure.step(f"检查{time}s内寻钥状态为{keyprsnt_old.value}"):
            timer = 0
            while timer < time - 1:
                self.check_key_nfc_vmm_prsnt(keyprsnt=keyprsnt_old)
                sleep(1)
                timer = timer + 1
        logger.info(f"开始检测到达时间时是否变为期望值")
        sleep(1)
        if is_change:
            self.check_key_nfc_vmm_prsnt(keyprsnt=keyprsnt_new)
        else:
            self.check_key_nfc_vmm_prsnt(keyprsnt=keyprsnt_old)

    def check_strt_msg_to_drvrr_in_time(self, StrtMsgToDrvrg_old: StrtMsgToDrvrg, StrtMsgToDrvrg_new: StrtMsgToDrvrg, time:int = 10, is_change:bool=True):
        with allure.step(f"检查{time}s内启动相关信息为{StrtMsgToDrvrg_old.value}"):
            timer = 0
            while timer < time - 1:
                self.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg_old)
                sleep(1)
                timer = timer + 1
        logger.info(f"开始检测到达时间时是否变为期望值")
        sleep(1)
        if is_change:
            self.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg_new)
        else:
            self.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg_old)

    def check_key_not_prsnt_msg_to_drvr_in_time(self, flag_old: bool, flag_new: bool, time:int = 10, is_change:bool=True):
        with allure.step(f"检查{time}s内无钥匙状态为{flag_old}"):
            timer = 0
            while timer < time - 1:
                self.check_key_not_prsnt_msg_to_drvr(flag=flag_old)
                sleep(1)
                timer = timer + 1
        logger.info(f"开始检测到达时间时是否变为期望值")
        sleep(1)
        if is_change:
            self.check_key_not_prsnt_msg_to_drvr(flag=flag_new)
        else:
            self.check_key_not_prsnt_msg_to_drvr(flag=flag_old)

    def check_usage_mode_status_in_time(self, usagemode_old: UsageMode, usagemode_new: UsageMode, time:int = 10, is_change:bool=True):
        with allure.step(f"检查{time}s内usagemode为{usagemode_old.value}"):
            timer = 0
            while timer < time - 5:
                self.check_usage_mode_status(usage_mode=usagemode_old)
                sleep(1)
                timer = timer + 1
        logger.info(f"开始检测到达时间时是否变为期望值")
        sleep(5)
        if is_change:
            self.check_usage_mode_status(usage_mode=usagemode_new)
        else:
            self.check_usage_mode_status(usage_mode=usagemode_old)

    def check_drvgcycoff_time(self, TiDrvgCycOff:int, wait_time: int = 0):
        with allure.step(f"检查离开驾驶时间"):
            sleep(wait_time)
            self.check('backbonefr', 'CemBackBoneFr07', 'TiDrvgCycOff', TiDrvgCycOff)
            
    def check_auto_sts(self, sts: CoolgReq, cycle_sts: ClimateCycleReq, wind_pos: SeatPos, wind_mode: AirWindMode, speed_pos: SeatVenPos, speed: SeatVenSpeed):
        promt_info = f"---------------->检查AC、循环模式、吹风模式、风速"
        with allure.step(promt_info):
            logger.info(promt_info)        
            self.check_climate_ac_sts(sts=sts)
            self.check_climate_cycle_req(sts=cycle_sts)
            self.check_climate_windmode_sts_req(pos=wind_pos,mode=wind_mode)
            self.check_windspeed_sts_req(pos=speed_pos,speed=speed)

    def recv_fr_msg_by_id(self, fr_id, send_address: list = [], recv_address: list = [], time_out=3):
        '''
        根据 id 接收 fr 数据 接收单帧报文
        @param fr_id: fr 的id
        @param send_address: 发送的逻辑地址
        @param recv_address: 接收的 逻辑地址
        @param time_out:
        @return:
        '''

        t = time.time()
        while time.time() - t < time_out:
            first_fram_msg = self.recv_pdu_d("backbonefr", fr_id, None, None)
            # logger.info(f"backbonefr 接收{first_fram_msg}")
            if first_fram_msg is None:
                continue
            # f_data = first_fram_msg[3]
            if recv_address and first_fram_msg[3][:2] != recv_address:
                continue
            if send_address and first_fram_msg[3][2:4] != send_address:
                continue
            # logger.info(f"backbonefr>>{first_fram_msg}")
            logger.info(f"backbonefr 接收 msg_id={fr_id}>>{bytes(first_fram_msg[3]).hex().upper()}")
            return first_fram_msg

        logger.error(f"backbonefr 接收id为{fr_id}报文超时，{time_out}未收到报文")
        return None

    def send_fr_msg_by_id(self, fr_id, data:list, **kwargs):
        '''
        发送 单帧 fr 报文
        @param fr_id: id
        @param data:  报文内容
        @param kwargs:
        @return:
        '''

        self.send_pdu_d("backbonefr", fr_id, data, cycle_time=1)
        # logger.info(f"backbonefr 发送id={fr_id} msg={bytes(data).hex().upper()}")

    def recv_fr_msg(self, fr_id_list=[88, 89, 90, 91, 92, 93, 94], fr_response_id=69, send_address=0x0e80,
                    recv_address=0x1601, time_out=20):
        '''
        接收 fr 报文
        @param fr_id_list: 接收id 列表
        @param fr_response_id: 响应id
        @param send_address: 发送的逻辑地址
        @param recv_address: 接收的逻辑地址
        @param time_out:
        @return:
        '''

        # 单帧
        # 开始帧4开头 最多14个字节   ；连续帧5开头 每帧最多16个字节；最后一帧9 开头最多14个字节
        if isinstance(send_address, int):
            send_address_string = hex(send_address)[2:].zfill(4)
            send_address = [int(send_address_string[i:i + 2], 16) for i in range(0, len(send_address_string), 2)]
        elif isinstance(send_address, (list, tuple)):
            send_address = send_address
        elif isinstance(send_address, str):
            if send_address.lower().startswith("0x"):
                send_address_string = send_address[2:].zfill(4)
            else:
                send_address_string = send_address.zfill(4)
            send_address = [int(send_address_string[i:i + 2], 16) for i in range(0, len(send_address_string), 2)]
        else:
            assert 0, "send_address 格式不对"

        if isinstance(recv_address, int):
            recv_address_string = hex(recv_address)[2:].zfill(4)
            recv_address = [int(recv_address_string[i:i + 2], 16) for i in range(0, len(recv_address_string), 2)]
        elif isinstance(recv_address, (list, tuple)):
            recv_address = recv_address
        elif isinstance(recv_address, str):
            if recv_address.lower().startswith("0x"):
                recv_address_string = recv_address[2:].zfill(4)
            else:
                recv_address_string = recv_address.zfill(4)
            recv_address = [int(recv_address_string[i:i + 2], 16) for i in range(0, len(recv_address_string), 2)]
        else:
            assert 0, "recv_address 格式不对"
        # 接收首帧
        fr_id = fr_id_list[0]
        logger.info(f"接收fr id为>>{fr_id}的报文")
        recv_msg_data = []
        first_fram_msg = self.recv_fr_msg_by_id(fr_id, send_address, recv_address, time_out)
        assert first_fram_msg, "未收到报文"
        f_data = first_fram_msg[3]

        # 接收的数据长度
        r_recv_add = f_data[0:2]
        r_send_add = f_data[2:4]
        start_byte = 4
        # 序列号
        fr_seq = f_data[start_byte]
        # 当前帧的数据长度
        current_fram_len = f_data[start_byte + 1]
        # 诊断数据长度
        recv_msg_len = int(bytes(f_data[start_byte + 2:start_byte + 4]).hex(), 16)
        # 当前帧接收的数据
        current_msg = f_data[start_byte + 4:start_byte + 4 + current_fram_len]
        # 判断
        assert fr_seq == 0x40, f"第一帧不是0x40 开头,实际是{hex(fr_seq).upper()}"

        msg_lis = current_msg[:recv_msg_len]
        msg_hex = [hex(i)[2:].zfill(2).upper() for i in msg_lis]
        recv_msg_data.extend(msg_lis)
        # 判断是多帧还是单帧
        if recv_msg_len <= 14:
            # 单帧
            logger.info(f"接收fr 报文为单帧，长度为{recv_msg_len}msg={msg_hex}")
            return recv_msg_data
        else:
            # 多帧 如果
            logger.info(f"接收fr 报文为多帧，总长度为{recv_msg_len}，第一帧为{recv_msg_data}")
            if 14 < recv_msg_len <= 28:
                # 首帧
                # 连续帧 和结束帧是同一帧
                consecutive_frame_head = 0x90
                pass
            elif 28 < recv_msg_len <= 4095:
                consecutive_frame_head = 0x51
            else:
                consecutive_frame_head = 0x51

        # data = [0x0e, 0x80, 0x16, 0x01, 0x83, 0x00, 0x00] + [0] * 15
        data = send_address + recv_address + [0x83, 0x00, 0x00, 0x00]
        msg = self.send_pdu_d("backbonefr", fr_response_id, data, cycle_time=1)
        logger.info(f"backbonefr 发送流控帧id 为{fr_response_id} 数据{bytes(data).hex().upper()}")
        t2 = time.time()
        # 接受最后一帧
        recv_last_frame_flag = False
        if consecutive_frame_head == 0x90:
            while time.time() - t2 < time_out:
                for fr_id in fr_id_list:
                    consecutive_frame_data_list = self.recv_fr_msg_by_id(fr_id, send_address, recv_address, time_out)
                    if consecutive_frame_data_list is None:
                        logger.warning(f"已经接收的报文长度{len(recv_msg_data)}内容为{recv_msg_data}")
                        assert 0, f"backbonefr 接收id为{fr_id}报文超时，{time_out}未收到报文"
                        # continue
                    consecutive_frame_data = consecutive_frame_data_list[3]
                    # 判断连续帧是否连续
                    recv_consecutive_frame_head = consecutive_frame_data[4]
                    if recv_consecutive_frame_head != consecutive_frame_head:
                        log_string = f"id为{fr_id} 接收的连续帧头不连续,本应为{hex(consecutive_frame_head)}实际为{hex(recv_consecutive_frame_head)}"
                        logger.error(log_string)
                        break
                    current_fram_len = consecutive_frame_data[5]
                    logger.info(f"consecutive_frame_head=={hex(consecutive_frame_head)}")
                    # 最后一帧 长度不一样
                    recv_msg_data.extend(consecutive_frame_data[8:8 + current_fram_len])
                    if len(recv_msg_data) >= recv_msg_len:
                        # 返回数据
                        logger.info(f"接收的报文长度{len(recv_msg_data)}内容为{recv_msg_data}")
                        return recv_msg_data
                    else:
                        logger.info(f"接收的报文失败")
                        assert 0, "接收报文失败"
        else:
            # 连续帧头
            while time.time() - t2 < time_out:
                for id_index, fr_id in enumerate(fr_id_list):
                    consecutive_frame_data_list = self.recv_fr_msg_by_id(fr_id, send_address, recv_address, time_out)
                    if consecutive_frame_data_list is None:
                        logger.warning(f"已经接收的报文长度{len(recv_msg_data)}内容为{recv_msg_data}")
                        assert 0, f"backbonefr 接收id为{fr_id}报文超时，{time_out}未收到报文"
                        # continue
                    consecutive_frame_data = consecutive_frame_data_list[3]
                    # 判断连续帧是否连续
                    recv_consecutive_frame_head = consecutive_frame_data[4]
                    if recv_consecutive_frame_head != consecutive_frame_head:
                        log_string = f"id为{fr_id} 接收的连续帧头不连续,本应为{hex(consecutive_frame_head)}实际为{hex(recv_consecutive_frame_head)}"
                        logger.error(log_string)
                        break
                    else:
                        consecutive_frame_head += 1

                    # 到周期重置
                    if consecutive_frame_head == 0x60:
                        consecutive_frame_head = 0x50
                    current_fram_len = consecutive_frame_data[5]

                    logger.info(f"consecutive_frame_head=={hex(consecutive_frame_head)}")
                    if consecutive_frame_head == 0x91:
                        recv_last_frame_flag = True
                        # 最后一帧 长度不一样
                        recv_msg_data.extend(consecutive_frame_data[8:8 + current_fram_len])
                    else:
                        recv_msg_data.extend(consecutive_frame_data[6:6 + current_fram_len])

                    if len(recv_msg_data) >= recv_msg_len:
                        if not recv_last_frame_flag:
                            # 接收 最后一帧 结束帧 9 开头的
                            # next_index = id_index + 1 if id_index + 1 < len(fr_id_list) else 0
                            next_index = 0
                            last_id = fr_id_list[next_index]
                            consecutive_frame_data_list = self.recv_fr_msg_by_id(last_id, send_address, recv_address,
                                                                                 time_out=0.1)
                        # 返回数据
                        logger.info(f"接收的报文长度{len(recv_msg_data)}内容为{recv_msg_data}")
                        return recv_msg_data
                    else:
                        # 判断剩余数据，最后一帧为90 开头
                        left_len = recv_msg_len - len(recv_msg_data)
                        logger.info(f"left_len=={hex(left_len)}")
                        if left_len <= 14:
                            consecutive_frame_head = 0x90
                            logger.info(f"left_len= consecutive_frame_head={hex(consecutive_frame_head)}")

        logger.error(f"已经接收的报文长度{len(recv_msg_data)}内容为{bytes(recv_msg_data).hex().upper()}")
        return []

    def send_fr_msg(self, send_data, send_id=69, recv_id=88, send_address=0x1601, recv_address=0x0e80):
        '''
        发送 fr 报文，根据数据长度 自己判断是多帧还是单帧
        @param send_data:
        @param send_id:
        @param recv_id:
        @param send_address:
        @param recv_address:
        @return:
        '''
        # 单帧 最大字节 26个
        single_frame_len = 26
        if isinstance(send_address, int):
            send_address_string = hex(send_address)[2:].zfill(4)
            send_address = [int(send_address_string[i:i + 2], 16) for i in range(0, len(send_address_string), 2)]
        elif isinstance(send_address, (list, tuple)):
            send_address = send_address
        elif isinstance(send_address, str):
            if send_address.lower().startswith("0x"):
                send_address_string = send_address[2:].zfill(4)
            else:
                send_address_string = send_address.zfill(4)
            send_address = [int(send_address_string[i:i + 2], 16) for i in range(0, len(send_address_string), 2)]
        else:
            assert 0, "send_address 格式不对"

        if isinstance(recv_address, int):
            recv_address_string = hex(recv_address)[2:].zfill(4)
            recv_address = [int(recv_address_string[i:i + 2], 16) for i in range(0, len(recv_address_string), 2)]
        elif isinstance(recv_address, (list, tuple)):
            recv_address = recv_address
        elif isinstance(recv_address, str):
            if recv_address.lower().startswith("0x"):
                recv_address_string = recv_address[2:].zfill(4)
            else:
                recv_address_string = recv_address.zfill(4)
            recv_address = [int(recv_address_string[i:i + 2], 16) for i in range(0, len(recv_address_string), 2)]
        else:
            assert 0, "recv_address 格式不对"

        address = recv_address + send_address
        # 判断是否多帧
        if len(send_data) <= single_frame_len-2:
            # 单帧
            logger.info("backbonefr 发送单帧数据")
            length = [0x40, len(send_data), 0x00, len(send_data)]
            send_msg = address + length + send_data
            self.send_fr_msg_by_id(send_id, send_msg)
        else:
            # 多帧
            logger.info("backbonefr 发送首帧帧数据")
            # 计算数据长度
            data_len_hex = hex(len(send_data))[2:].zfill(4)
            data_len = [int(data_len_hex[i:i + 2], 16) for i in range(0, len(data_len_hex), 2)]
            length = [0x40, single_frame_len-2] + data_len

            # 存放连续帧
            consecutive_frame_list = []
            # 拼接发送数据内容  首帧最多 26个字节
            first_frame = address + length + send_data[:single_frame_len - 2]
            left_msg = send_data[single_frame_len - 2:]

            if single_frame_len-2 < len(send_data) <= single_frame_len*2:
                # 最后一帧包含数据
                length = [0x90, len(left_msg)] + data_len
                last_frame = address + length + left_msg
                consecutive_frame_list.append(last_frame)
            elif single_frame_len*2 < len(send_data) <= 4095:
                # 对数据进行分割
                left_msg_list = [left_msg[i:i + single_frame_len] for i in
                                 range(0, len(left_msg), single_frame_len)]
                last_msg = left_msg_list[-1]

                # 最后一帧 如果小于等14 在9开头，如果大于14 则5开头
                if len(last_msg) <= single_frame_len - 2:
                    # 最后一帧包含数据
                    length = [0x90, len(last_msg)] + data_len
                    last_frame = address + length + last_msg
                    consecutive_data_list = left_msg_list[:-1]
                else:
                    # 最后一帧不包含数据
                    length = [0x90, 0x00] + data_len
                    last_frame = address + length
                    consecutive_data_list = left_msg_list
                # 连续帧头
                consecutive_frame_head = 0x51
                for consecutive_frame_msg in consecutive_data_list:
                    consecutive_frame = address + [consecutive_frame_head] + [
                        len(consecutive_frame_msg)] + consecutive_frame_msg
                    consecutive_frame_list.append(consecutive_frame)
                    consecutive_frame_head += 1
                    if consecutive_frame_head == 0x60:
                        consecutive_frame_head = 0x50
                # 添加最后一帧
                consecutive_frame_list.append(last_frame)
            else:
                pass
            # 发送首帧
            send_count_index = 1
            self.send_fr_msg_by_id(send_id, first_frame)
            logger.info(f"backbonefr {send_count_index}次 发送id={send_id} msg={bytes(first_frame).hex().upper()}")
            # 接收流控帧
            recv_flow_control_frame = self.recv_fr_msg_by_id(recv_id, recv_address, send_address)
            # 判断留空帧
            assert recv_flow_control_frame
            # 发送 连续帧以及最后一帧
            send_id_list = [69, 75, 81]
            # 发送连续帧
            for index, msg in enumerate(consecutive_frame_list):
                self.send_fr_msg_by_id(send_id, msg)
                time.sleep(0.010)
                send_count_index += 1
                logger.info(f"backbonefr {send_count_index}次 发送id={send_id} msg={bytes(msg).hex().upper()}")


    def set_ble_key_prsnt_sts(self,zone:BLEKeyPrsntZone,sts:BLEKeyPrsntSts):
        promt_info = f"---------------->模拟设置蓝牙zone:{zone.name} 的钥匙在位状态为{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)   
            signal_name = "BLEKeyPrsntStsZone" + str(zone.value)
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, signal_name, sts.value)

    
    def telm_set_hv_active_req(self, req: RemHvStrtActvReq, time_wait: Union[int, float] = 0):
        prompt_info = f"---------->APP远程设置充激活请求为{req.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.set(self.ipdu.connectivitycanfd.TcamConnectivityFr12, 'RemHvStrtActvReq', req.value)

    
    def check_no_chrgild_req(self, req: ChrgLidReq):
        promt_info = f"---------------->Check BGM 没有发出{req.name}的控制充电口盖请求"
        with allure.step(promt_info):
            logger.info(promt_info)
            result_ori = self.ipdu.check_signal(self.ipdu.cem_lin2.CemCem_Lin2Fr06, "ChrgLidManvgDCorAcDcReq2")
            logger.info("result_original_1(ChrgLidManvgDCorAcDcReq2) {}".format(result_ori))
            result = check_all_value_is(result_ori, req.value)
            assert result
            self.ipdu.reset_check_results()

 #o_fan.liu           
    def check_steerwheel_direct_req(self, direct: AdjustDirection, sts: bool):
        prompt_info = f"----------> Check BGM 请求的{direct.name}调节方向是否为{sts}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if direct.name == "Forward":
                    self.check("cem_lin4", "CemCem_Lin4Fr06", "SteerAdjSwtFwdSts", sts)
            elif direct.name == "Up":
                    self.check("cem_lin4", "CemCem_Lin4Fr06", "SteerAdjSwtUpSts", sts)
            elif direct.name == "Backward":
                    self.check("cem_lin4", "CemCem_Lin4Fr06", "SteerAdjSwtBackSts", sts)
            elif direct.name == "Down":
                    self.check("cem_lin4", "CemCem_Lin4Fr06", "SteerAdjSwtDwnSts", sts)  
                             

    def check_door_switch_light_keep_sts(self, pos: DoorPos, req: LampSts,last_time:Union[int,float]):
        prompt_info = f"----------> Check BGM 发出的{pos.name}门按键指示灯状态是否一直为{req.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if pos.name == "Dirver":
                self.check_signal_thread_start("infocanfd","BgmInfoCanFdFr22", "StatusOfOuterDoorSwLightDrvrSwLight", timeout = last_time)
                sleep(last_time)
                result_ori_dri = self.check_signal_thread_stop("StatusOfOuterDoorSwLightDrvrSwLight")
                logger.info(f"result_ori_dri:{result_ori_dri}")
                if check_all_value_is(result_ori_dri, req.value):
                    assert True
                else:
                    logger.info(f"不是所有的值都是{req.name}")
                    assert False

            elif pos.name == "Pass":
                self.check_signal_thread_start("infocanfd","BgmInfoCanFdFr22", "StatusOfOuterDoorSwLightPassSwLight", timeout = last_time)
                sleep(last_time)
                result_ori_pass = self.check_signal_thread_stop("StatusOfOuterDoorSwLightPassSwLight")
                logger.info(f"result_ori_pass:{result_ori_pass}")
                if check_all_value_is(result_ori_pass, req.value):
                    assert True
                else:
                    logger.info(f"不是所有的值都是{req.name}")
                    assert False

            elif pos.name == "RearLeft":
                self.check_signal_thread_start("infocanfd","BgmInfoCanFdFr22", "StatusOfOuterDoorSwLightLeReSwLight", timeout = last_time)
                sleep(last_time)
                result_ori_rl = self.check_signal_thread_stop("StatusOfOuterDoorSwLightLeReSwLight")
                logger.info(f"result_ori_rl:{result_ori_rl}")
                if check_all_value_is(result_ori_rl, req.value):
                    assert True
                else:
                    logger.info(f"不是所有的值都是{req.name}")
                    assert False

            elif pos.name == "RearRight":
                self.check_signal_thread_start("infocanfd","BgmInfoCanFdFr22", "StatusOfOuterDoorSwLightRiReSwLight", timeout = last_time)
                sleep(last_time)
                result_ori_rr = self.check_signal_thread_stop("StatusOfOuterDoorSwLightRiReSwLight")
                logger.info(f"result_ori_rr:{result_ori_rr}")
                if check_all_value_is(result_ori_rr, req.value):
                    assert True
                else:
                    logger.info(f"不是所有的值都是{req.name}")
                    assert False

            elif pos.name == "All":
                self.check_signal_thread_start("infocanfd","BgmInfoCanFdFr22", "StatusOfOuterDoorSwLightDrvrSwLight", timeout = last_time)
                self.check_signal_thread_start("infocanfd","BgmInfoCanFdFr22", "StatusOfOuterDoorSwLightPassSwLight", timeout = last_time)
                self.check_signal_thread_start("infocanfd","BgmInfoCanFdFr22", "StatusOfOuterDoorSwLightLeReSwLight", timeout = last_time)
                self.check_signal_thread_start("infocanfd","BgmInfoCanFdFr22", "StatusOfOuterDoorSwLightRiReSwLight", timeout = last_time)
                sleep(last_time)
                result_ori_dri = self.check_signal_thread_stop("StatusOfOuterDoorSwLightDrvrSwLight")
                result_ori_pass = self.check_signal_thread_stop("StatusOfOuterDoorSwLightPassSwLight")
                result_ori_rl = self.check_signal_thread_stop("StatusOfOuterDoorSwLightLeReSwLight")
                result_ori_rr = self.check_signal_thread_stop("StatusOfOuterDoorSwLightRiReSwLight")
                logger.info(f"result_ori_dri:{result_ori_dri},result_ori_pass:{result_ori_pass},result_ori_rl:{result_ori_rl},result_ori_rr:{result_ori_rr}")

                if check_all_value_is(result_ori_dri, req.value) and check_all_value_is(result_ori_pass, req.value) and check_all_value_is(result_ori_rl, req.value) and check_all_value_is(result_ori_rr, req.value):
                    assert True
                else:
                    logger.info(f"不是所有的值都是{req.name}")
                    assert False
    
            # self.check('cem_lin4', 'CemCem_Lin4Fr06', 'SteerAdjSwtFwdSts', sts)
           
    def check_tailgate_upper_req(self, req: isOn):
        with allure.step(f"Check BGM 尾门上部位置请求：{req.name}"):
            logger.info(f"Check BGM 尾门上部位置请求：{req.name}")
            self.check('bodycan', 'CEMBodyFr11', 'TrPosnUpprProgmReq', req.value)

    def set_tailgate_switch_sts(self, sts: FoldHmiReq):
        with allure.step(f"模拟尾门开关闭合状态：{sts.name}"):
            logger.info(f"模拟尾门开关闭合状态：{sts.name}")
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, "SwtTrClsSts", sts.value)
    
    def check_hv_actv_for_vehmod_req(self, onoff: bool):
        with allure.step(f"检查激活高压系统请求状态"):
            self.check('backbonefr', 'CemBackBoneFr03', 'HvActvForVehModReq', onoff)

    def check_hv_actv_for_vehmod_req_in_time(self, onoff_old: bool, onoff_new: bool, time:int = 10, is_change:bool=True):
        with allure.step(f"检查{time}s内激活高压系统请求状态为{onoff_old}"):
            timer = 0
            while timer < time - 1:
                self.check_hv_actv_for_vehmod_req(onoff=onoff_old)
                sleep(1)
                timer = timer + 1
        logger.info(f"开始检测到达时间时是否变为期望值")
        sleep(1)
        if is_change:
            self.check_hv_actv_for_vehmod_req(onoff=onoff_new)
        else:
            self.check_hv_actv_for_vehmod_req(onoff=onoff_old)


    def check_door_lock_req(self, door_pos: DoorPos, req: DoorLockCmd,timeout: Union[float, int] = 1):
        if door_pos.name == "Dirver":
            logger.info(f"Check主驾位门的解闭锁请求是否为{req.name}")
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'DoorDrvrLockCmd', req.value, timeout)
        elif door_pos.name == "Pass":
            logger.info(f"Check副驾位门的解闭锁请求是否为{req.name}")
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'DoorPassLockCmd', req.value, timeout)
        elif door_pos.name == "RearLeft":
            logger.info(f"Check左后门的解闭锁请求是否为{req.name}")
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'DoorLeReLockCmd', req.value, timeout)
        elif door_pos.name == "RearRight":
            logger.info(f"Check右后门的解闭锁请求是否为{req.name}")
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr01, 'DoorRiReLockCmd', req.value, timeout)
        elif door_pos.name == "All":
            logger.info(f"Check所有门的解闭锁请求是否为{req.name}")
            target_msg = self.ipdu.bodycan.CemBodyFr01
            self.ipdu.check_multiple_signals([(target_msg, 'DoorDrvrLockCmd', req.value),
                                              (target_msg, 'DoorPassLockCmd', req.value),
                                              (target_msg, 'DoorLeReLockCmd', req.value),
                                              (target_msg, 'DoorRiReLockCmd', req.value)], 
                                              timeout)


    def check_charge_target_soc_req(self, value:int):
        promt_info = f"--------------->Check BGM 发出的设置目标充电SOC值是否为{value/10}%"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr12, 'LocalBookChrgnTarVal', value)

    
    def recover_all_bus_signal_to_default(self):
        logger.info("停止所有周期性信号发送")
        self.stop_all_cyclic_msgs()
        sleep(1)
        logger.info("开始所有周期性信号发送")
        self.start_all_cyclic_msg()

    

    def check_door_opener_req_and_trigsrc(self, drv_opener: Union[DoorPos, None] = None,
                              pass_opener: Union[DoorPos, None] = None,
                              lere_opener: Union[DoorPos, None] = None,
                              rire_opener: Union[DoorPos, None] = None,
                              tr_opener: Union[DoorPos, None] = None,
                              door_req: DoorOpenerReq = DoorOpenerReq.Idle,
                              door_trigsrc: Union[None, DoorTrigerSource] = None,
                              trunk_trigsrc: Union[None, TailgateTrigerSource] = None,
                              timeout: Union[float, int] = 3
                              ):
        target_msg78 = self.ipdu.bodycan.CemBodyFr78
        target_msg79 = self.ipdu.bodycan.CemBodyFr79
        target_msg02 = self.ipdu.bodycan.CemBodyFr02
        with allure.step(f"Check BGM 发出的电动门的开关请求"):
            if drv_opener is not None:
                if door_trigsrc is not None:
                    logger.info(f"Check主驾位门的开关请求是否为{door_req.name}，触发源是否为{door_trigsrc.name}")
                    self.ipdu.check_multiple_signals([(target_msg78, 'DoorOpenerDrvrReqDoorOpenerReq2', door_req.value),
                                                      (target_msg78, 'DoorOpenerDrvrReqTrigSrc', door_trigsrc.value)],
                                                     timeout=timeout)
                else:
                    logger.info(f"Check主驾位门的开关请求是否为{door_req.name}")
                    self.ipdu.check(target_msg78, 'DoorOpenerDrvrReqDoorOpenerReq2', door_req.value, timeout)

            if pass_opener is not None:

                if door_trigsrc is not None:
                    logger.info(f"Check副驾位门的开关请求是否为{door_req.name}，触发源是否为{door_trigsrc.name}")
                    self.ipdu.check_multiple_signals([(target_msg79, 'DoorOpenerPassReqDoorOpenerReq2', door_req.value),
                                                      (target_msg79, 'DoorOpenerPassReqTrigSrc', door_trigsrc.value)],
                                                     timeout=timeout)
                else:
                    logger.info(f"Check副驾位门的开关请求是否为{door_req.name}")
                    self.ipdu.check(target_msg79, 'DoorOpenerPassReqDoorOpenerReq2', door_req.value, timeout)
            if lere_opener is not None:

                if door_trigsrc is not None:
                    logger.info(f"Check左后门的开关请求是否为{door_req.name}，触发源是否为{door_trigsrc.name}")
                    self.ipdu.check_multiple_signals([(target_msg78, 'DoorOpenerLeReReqDoorOpenerReq2', door_req.value),
                                                      (target_msg78, 'DoorOpenerLeReReqTrigSrc', door_trigsrc.value)],
                                                     timeout=timeout)
                else:
                    logger.info(f"Check左后门的开关请求是否为{door_req.name}")
                    self.ipdu.check(target_msg78, 'DoorOpenerLeReReqDoorOpenerReq2', door_req.value, timeout)
            if rire_opener is not None:

                if door_trigsrc is not None:
                    logger.info(f"Check右后门的开关请求是否为{door_req.name}，触发源是否为{door_trigsrc.name}")
                    self.ipdu.check_multiple_signals([(target_msg79, 'DoorOpenerRiReReqDoorOpenerReq2', door_req.value),
                                                      (target_msg79, 'DoorOpenerRiReReqTrigSrc', door_trigsrc.value)],
                                                     timeout=timeout)
                else:
                    logger.info(f"Check右后门的开关请求是否为{door_req.name}")
                    self.ipdu.check(target_msg79, 'DoorOpenerRiReReqDoorOpenerReq2', door_req.value, timeout)
            if tr_opener is not None:

                if trunk_trigsrc is not None:
                    logger.info(f"Check尾门的开关请求是否为{door_req.name}，触发源是否为{trunk_trigsrc.name}")
                    self.ipdu.check_multiple_signals([(target_msg02, 'TrOpenerReqTrOpenerReq', door_req.value),
                                                      (target_msg02, 'TrOpenerReqTrigSrc', trunk_trigsrc.value)],
                                                     timeout=timeout)
                else:
                    logger.info(f"Check尾门的开关请求是否为{door_req.name}")
                    self.ipdu.check(target_msg02, 'TrOpenerReqTrOpenerReq', door_req.value, timeout)

    def preheat_msg(self, bus_name: str, msg_name: str):
        '''
        预热msg发送, 让其 周期1ms 等待发送, 一般用在发送及时报文
        注意 预热至少要提前2s,只用在PCAN can bus
        '''
        pdu_info = self.ipdu.bus_pdu_dict.get(bus_name)
        msg = pdu_info.get(msg_name)
        msg["pre_send"] = True

    def remove_preheating(self, bus_name: str, msg_name: str):
        '''
        移除 预热msg发送, 让其 恢复周期2s
        注意 只用在PCAN can bus
        '''
        pdu_info = self.ipdu.bus_pdu_dict.get(bus_name)
        msg = pdu_info.get(msg_name)
        msg["pre_send"] = False

    def get_dtc_snapshot_info(self, dtc:str):
        prompt_info = f"---------->Check DTC:{dtc} 的 快照信息"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            dtc_bytes = transferDTCtoBytes(dtc)
            diag_req = [0x19, 0x04] + dtc_bytes + [0x20]
            diag_resp = self.sd_tester.send_request_and_recv_response(diag_req)[1]
            logger.info(f"--------->获取的快照信息如下:{diag_resp}")
            diag_resp_res ="".join(["0" + str(hex(i)).replace("0x","") if len(str(hex(i)).replace("0x","")) == 1 else str(hex(i)).replace("0x","") for i in diag_resp]) 
            return diag_resp_res
        
    def check_tailwing_without_close_or_open_cmd(self,state,timeout=2):
        with allure.step(f"Check 在条件不满足时BGM不能发送cmd信号"):
            result_ori = self.ipdu.check_signal(self.ipdu.cem_lin6.BgmCem_Lin6Fr01, 'ActvReSplrPosnCmd',timeout)
            logger.info(f'获取到的原始数据ActvReSplrPosnCmd为{result_ori}')
            check_result = check_all_value_is(result_ori,state)
            logger.info(f'Check 结果时：{check_result}')
            assert check_result

    def get_key_nfc_vmm_prsnt(self):
        expectedvalue = self.ipdu.get_recent_signal_raw_value(self.ipdu.infocanfd.BgmInfoCanFdDevFr03, 'KeyReadStsToVMMNFCNFCKeyPrsnt')
        logger.info(f"获取的NFC钥匙存在状态为:{expectedvalue}")
        return expectedvalue
    
    def resume_ecu_send(self, bus_name: str, ecu_name: str):
        '''
        继续发送
        @param bus_name:
        @param ecu:
        @return:
        '''
        self.ipdu.resume_ecu_send(bus_name, ecu_name)

    def check_relay_proxyreq(self, poweroutproxy: Union[PowerOutLetReq, None] = None, timeout=2):  
        with allure.step(f"Check 在条件不满足的情况下MPU不发送proxy请求"):
            logger.info(f"Check 在条件不满足的情况下MPU不发送proxy请求")
            ori_data = self.ipdu.check_signal(self.ipdu.infocanfd.BgmInfoCanFdFr21, 'RlyPwrCmdProxyReq', timeout)
            logger.info(f"获取{timeout}秒内的RlyPwrCmdProxyReq原始数据是:{ori_data}")
            check_result = check_all_value_is(ori_data, poweroutproxy.value)
            logger.info(f"Check 结果是：{check_result}")
            assert check_result   
            
    def check_relay_cmd(self, relaytype: Union[RelayType, None] = None,
                            relaysts: Union[RelaySts, None] = None,
                            OnOff: Union[OnOffSafe1, None] = None,
                            poweroutproxy: Union[PowerOutLetReq, None] = None,
                            time_wait: Union[float, int] = None):
            with allure.step(f"Check 继电器使能状态"):
                if relaytype.name == "KL151" :
                    logger.info(f"Check KL151继电器使能状态为{relaysts.name}")
                    self.check_singal("backbonefr", "CemBackBoneFr14", 'RlyPwrDistbnCmd1WdIgnRlyCmd',relaysts.value, check_time=time_wait)
                    
                elif relaytype.name == "KL152":
                    logger.info(f"Check KL152继电器使能状态为{relaysts.name}")
                    self.check_singal("backbonefr", "CemBackBoneFr15", 'RlyPwrDistbnCmd1WdIgnRlyExtCmd',relaysts.value, check_time=time_wait)

                elif relaytype.name == "KL153":
                    logger.info(f"Check KL153继电器使能状态为{relaysts.name}")
                    self.check_singal("adcanfd", "BgmADCANFDFr30", 'IgnRly3Cmd',relaysts.value, check_time=time_wait)
                    
                elif relaytype.name == "climate": 
                    logger.info(f"Check climate继电器使能状态为{relaysts.name}")
                    self.check_singal("bodycan", "CemBodyFr04", 'ClimRlyCmd',relaysts.value, check_time=time_wait)
                    
                elif relaytype.name == "batterysaver":    
                    logger.info(f"Check batterysaver继电器使能状态为{relaysts.name}")
                    self.check_singal("infocanfd", "BgmInfoCanFdFr18", 'RlyPwrDistbnCmd1WdBattSaveCmd',relaysts.value, check_time=time_wait)                           
                            
                elif relaytype.name == "poweroutlet":
                    logger.info(f"Check batterysaver继电器使能状态为{relaysts.name}")
                    self.check_singal("infocanfd", "BgmInfoCanFdFr18", 'RlyPwrCmd',relaysts.value, check_time=time_wait)  
                        
                elif relaytype.name == "crashrelay":
                    logger.info(f"Check crashrelay继电器使能状态为{OnOff.name}")
                    self.check_singal("infocanfd","BgmInfoCanFdFr18", "FuPmpRlyCmd", OnOff.value, check_time=time_wait)
                            
                else:
                    logger.info(f"未获取到期望值")
                    assert False

    def check_Lock_and_unlock_remind(self, lockstsprmt: Union[LockStsPrmt, None] = None, timeout=2):  
        with allure.step(f"Check 总线2s内解闭锁动作提醒状态为{lockstsprmt.name}"):
            logger.info(f"Check 总线2s内解闭锁动作提醒状态为{lockstsprmt.name}")
            ori_data = self.ipdu.check_signal(self.ipdu.infocanfd.BgmInfoCanFdFr21, 'LockSysStsPrmt', timeout)
            logger.info(f"获取{timeout}秒内的LockSysStsPrmt原始数据是:{ori_data}")
            check_result = check_all_value_is(ori_data, lockstsprmt.value)
            
            logger.info(f"Check 结果是：{check_result}")
            assert check_result   
    
    def check_usgmode_deactvn_qly(self, usgmoddeactvnqly: UsgModDeactvnQly):
        with allure.step(f"检查停车时usagemode是否有效的状态值"):
            self.check('backbonefr', 'CemBackBoneFr15', 'UsgModDeactvnQly', usgmoddeactvnqly.value)
            
    def check_alrm_notactived_req(self, timeout=3):
        with allure.step(f"Check 防盗没有被激活"):
            logger.info(f"Check 防盗没有被激活")
            ori_data = self.ipdu.check_signal(self.ipdu.backbonefr.CemBackBoneFr18, 'AlrmStsAlrmSt', timeout)
            logger.info(f"获取{timeout}秒内的CemBackBoneFr18原始数据是:{ori_data}")
            check_result = check_signal_value_exist(ori_data, 2)
            logger.info(f"Check 结果是：{check_result}")
            assert check_result == False
    
    def get_four_tire_pressure_and_temperature(self):
        tire_fl_P = self.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr09, 'LeFrntTireMsgP')
        tire_fl_T = self.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr09, 'LeFrntTireMsgT')
        tire_fr_P = self.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr09, 'RiFrntTireMsgP')
        tire_fr_T = self.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr09, 'RiFrntTireMsgT')
        tire_rl_P = self.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr09, 'LeReTireMsgP')
        tire_rl_T = self.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr09, 'LeReTireMsgT')
        tire_rr_P = self.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr09, 'RiReTireMsgP')
        tire_rr_T = self.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr09, 'RiReTireMsgT')
        logger.info(f"当前的4轮胎压为fl:{tire_fl_P}、fr:{tire_fr_P}、rl:{tire_rl_P}、rr:{tire_rr_P}")
        logger.info(f"当前的4轮胎温为fl:{tire_fl_T}、fr:{tire_fr_T}、rl:{tire_rl_T}、rr:{tire_rr_T}")
        return tire_fl_P, tire_fl_T, tire_fr_P, tire_fr_T, tire_rl_P, tire_rl_T, tire_rr_P, tire_rr_T

    def check_four_tire_pressure_and_temperature(self, tire_fl_P = 0, tire_fl_T = 0, tire_fr_P = 0, tire_fr_T = 0, tire_rl_P = 0, tire_rl_T = 0, tire_rr_P = 0, tire_rr_T = 0):
        with allure.step(f"检查4轮胎压和胎温是否和预期一致"):
            self.check('backbonefr', 'CemBackBoneFr09', 'LeFrntTireMsgP', tire_fl_P)
            self.check('backbonefr', 'CemBackBoneFr09', 'LeFrntTireMsgT', tire_fl_T)
            self.check('backbonefr', 'CemBackBoneFr09', 'RiFrntTireMsgP', tire_fr_P)
            self.check('backbonefr', 'CemBackBoneFr09', 'RiFrntTireMsgT', tire_fr_T)
            self.check('backbonefr', 'CemBackBoneFr09', 'LeReTireMsgP', tire_rl_P)
            self.check('backbonefr', 'CemBackBoneFr09', 'LeReTireMsgT', tire_rl_T)
            self.check('backbonefr', 'CemBackBoneFr09', 'RiReTireMsgP', tire_rr_P)
            self.check('backbonefr', 'CemBackBoneFr09', 'RiReTireMsgT', tire_rr_T)

    def check_right_light_off(self):
        prompt_info = f"---------->检查右转向灯灭"
        with allure.step(prompt_info):
            self.check("backbonefr","CemBackBoneFr06","IndcrDisp",0)
            self.check("backbonefr","CemBackBoneFr02","ExtrLtgStsTurnIndrRi",0)
            self.check("bodyexposedcanfd","CemBodyExpoFr51","ActvnOfIndcrIndcrOut",0)

    def check_left_light_off(self):
        prompt_info = f"---------->检查左转向灯灭"
        with allure.step(prompt_info):
            self.check("backbonefr","CemBackBoneFr06","IndcrDisp",0)
            self.check("backbonefr","CemBackBoneFr02","ExtrLtgStsTurnIndrLe",0)
            self.check("bodyexposedcanfd","CemBodyExpoFr51","ActvnOfIndcrIndcrOut",0)

    def check_turn_right_error(self):
        for i in range(3):
            prompt_info = f"---------->检查 第{i+1}次 右转向灯亮"
            with allure.step(prompt_info):
                self.check("backbonefr","CemBackBoneFr02","ExtrLtgStsTurnIndrRi",2)
                self.check("bodyexposedcanfd","CemBodyExpoFr51","ActvnOfIndcrIndcrOut",2)
            sleep(0.4)
            prompt_info = f"---------->检查 第{i+1}次 右转向灯灭"
            with allure.step(prompt_info):
                self.check("backbonefr","CemBackBoneFr02","ExtrLtgStsTurnIndrRi",0)
                self.check("bodyexposedcanfd","CemBodyExpoFr51","ActvnOfIndcrIndcrOut",0)


    def set_turn_right_wheel(self,wheel="right_old"):
        if wheel == "right_old":
            self.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.NotAvailble)
            sleep(.5)
            self.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Right2,press_type=SteerWhlTouchSwtSts.ShortPress)

        elif wheel == "right_new":
            self.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left1,press_type=SteerWhlTouchSwtSts.NotAvailble)
            sleep(.5)
            self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left1,press_type=SteerWhlTouchSwtSts.ShortPress)

        elif wheel == "left":
            self.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.NotAvailble)
            sleep(.5)
            self.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)

    def check_wheel_light_on_and_light_off(self,direction,num=3):

        #右转向灯亮400ms灭400ms持续3次
        if direction == "right":
            for num in range(3):
                self.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.RiOn)
                self.check_active_indicator_lamp_req(indcr_sts=IndcrSts.RiOn)
                sleep(.4)
                self.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
                self.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)

        elif direction == "left":
            for num in range(3):
                self.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.LeOn)
                self.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeOn)
                sleep(.4)
                self.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
                self.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)


    def set_twilight_sensor_sts(self, OutdBri: Union[OutdBriSts, None] = None,
                            BtnStsOHC: Union[BtnStsSngTyp, None] = None,
                            TwliBriRaw: Union[TwliBriRaw, None] = None):
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawQf', 3)  # SUS光感QF3
        with allure.step(f"设置白天黑夜状态"):
            if OutdBri is not None:
                logger.info(f"设置控制灯光自动开关的输入为{OutdBri.name}")
                self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'OutdBriSts',OutdBri.value)
            if BtnStsOHC is not None:
                logger.info(f"设置开关状态为{BtnStsOHC.name}")
                self.ipdu.set(self.ipdu.cem_lin3.OhcCem_Lin3Fr04, 'BtnStsOHCIntrLiSwtAllOnSts',
                              BtnStsOHC.value)
            if TwliBriRaw is not None:
                logger.info(f"设置黑夜状态为{TwliBriRaw.name}")
                self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'TwliBriRawTwliBriRaw',
                              TwliBriRaw.value)

    def four_domain_restart_send_signal(self, signal_name:str,sig_value_name:Union[str, int, float],time_sleep=0.01):
        self.set(bus_name="connectivitycanfd",msg_name="BgmConnectivityFr22", signal_name=signal_name, sig_value_name=sig_value_name)
        sleep(time_sleep)

    def wakeup_tcam_by_can(self):
        self.preheat_msg(bus_name="connectivitycanfd", msg_name="BgmConnectivityCANNmFr")
        time.sleep(2)
        self.send_pdu(bus_name="connectivitycanfd", msg_id=0x533, data=[0x33,0x50,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF], cycle_time=0.1)
    
    def stop_wakeup_tcam_by_can(self):
        self.stop_send_pdu(bus_name="connectivitycanfd", id=0x533)
        self.remove_preheating(bus_name="connectivitycanfd", msg_name="BgmConnectivityCANNmFr")
        
    def set_brake_pedal_function_safe(self,safe:Union[None,YesOrNo] = YesOrNo.Yes,qf:Union[None,ValueQf] = ValueQf.AccurData,sts:Union[None,YesOrNo] = YesOrNo.Yes, crc_sts:bool = True, ub_flag:bool = True):
        prompt_info = f"---------->设置刹车踏板相关信号"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if sts is not None:
                logger.info(f"刹车踏板安全校验设为{safe.name}")
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlNotPsdSafe', safe.value)
            if qf is not None:
                logger.info(f"刹车踏板QF设为{qf.name}")
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', qf.value)
            if sts is not None:
                logger.info(f"刹车踏板状态设为{sts.name}")
                if crc_sts == False:
                    logger.info("仿真不带crc得刹车踏板状态信号")
                    self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
                    self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', sts.value, ub_flag = ub_flag)
                else:
                    self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
                    self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', sts.value, ub_flag = ub_flag)

    def set_rearview_angle(self, left_horizon: Union[int, None] = None,
                            left_vertical: Union[int, None] = None,
                            right_horizon: Union[int, None] = None,
                            right_vertical: Union[int, None] = None):
        with allure.step(f"设置后视镜角度"):
            if left_horizon is not None:
                logger.info(f"设置主驾后视镜水平角度为{left_horizon}")
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, "MirrPosnToCldAtDrvrMirrPosnAdjCldLeRi", left_horizon)
            if left_vertical is not None:
                logger.info(f"设置主驾后视镜垂直角度为{left_vertical}")
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, "MirrPosnToCldAtDrvrMirrPosnAdjCldUpDwn", left_vertical)
            if right_horizon is not None:
                logger.info(f"设置副驾后视镜水平角度为{right_horizon}")
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, "MirrPosnToCldAtPassMirrPosnAdjCldLeRi", right_horizon)
            if right_vertical is not None:
                logger.info(f"设置副驾后视镜垂直角度为{right_vertical}")
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, "MirrPosnToCldAtPassMirrPosnAdjCldUpDwn", right_vertical)


    def set_aeb_brake_req(self,req:AsySftyHWLReq):
        prompt_info = f"---------->设置AEB紧急刹车请求{req.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr13, 'AsySftyHWLReq', req.value)

    def set_aeb_bkp_brake_req(self,req:AsySftyHWLReq):
        prompt_info = f"---------->设置AEB紧急刹车请求{req.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr04, 'AsySftyHWLReqBkp', req.value)
    
    def set_bluetooth_key_connect_sts(self, key_num:int,type: BlueType, con_sts: ConnSts,key_zone:int=1,key_id: Union[list,None] = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
         0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F]):
        promt_info = f"---------------->设置第{key_num}的蓝牙钥匙类型为{type.name},连接状态{con_sts.name},Key_ID为：{key_id}"
        with allure.step(promt_info):
            logger.info(promt_info)
            KeyConnectSts_sig = 'DigKeyConnectInfo'+str(key_num)+'KeyConnectSts'
            KeyTyp_sig = 'DigKeyConnectInfo'+str(key_num)+'KeyTyp'
            KeyPrsnt_sig = 'DigKeyConnectInfo'+str(key_num)+'KeyPrsntZone'
            if key_num ==1 or key_num ==2:
                self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, KeyTyp_sig, type.value)
                self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, KeyConnectSts_sig,con_sts.value)
                self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, KeyPrsnt_sig,key_zone)
                for i in range(16):
                    KeyIdByte = 'DigKeyConnectInfo'+str(key_num)+'KeyIdByte'+str(i)
                    if key_id == None:
                        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, KeyIdByte,0)
                    else:
                        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, KeyIdByte, key_id[i])
                KeyCon_UB = 'DigKeyConnectInfo'+str(key_num)+'_UB'
                self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, KeyCon_UB,1)
            elif key_num ==3 or key_num ==4:
                self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr19, KeyTyp_sig, type.value)
                self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr19, KeyConnectSts_sig,con_sts.value)
                self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr19, KeyPrsnt_sig,key_zone)
                for i in range(16):
                    KeyIdByte = 'DigKeyConnectInfo'+str(key_num)+'KeyIdByte'+str(i)
                    if key_id == None:
                        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr19, KeyIdByte,0)
                    else:
                        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr19, KeyIdByte, key_id[i])
                KeyCon_UB = 'DigKeyConnectInfo'+str(key_num)+'_UB'
                self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr19, KeyCon_UB,1)
            
    def set_wiper_speed_signal(self, speed: AutWinWipgCmd):
        promt_info = f"---------------->模拟反馈雨刮速度为{speed.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr01, "AutWinWipgCmd", speed.value) 
    
    def check_wiper_rain_sensor(self, rain_sensor: RainSnsrStsToHMI, timeout=5):
        with allure.step(f"Check 雨量传感器激活请求信号值{rain_sensor.name}"):
            logger.info(f"Check 雨量传感器激活请求信号值{rain_sensor.name}")
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, 'RainSnsrStsToHMI', rain_sensor.value, timeout) 
    
    def set_wiper_activation_signal(self, activa: WiprActvFromWMM):
        promt_info = f"---------------->仿真发送雨刮激活信号为{activa.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, "WiprActvFromWMM", activa.value) 
            
    def check_wiper_status_req(self, status_req: WiprActv):
        with allure.step(f"Check 雨刮状态请求{status_req.name}"):
            logger.info(f"Check 雨刮状态请求{status_req.name}")
            self.ipdu.check(self.ipdu.cem_lin1.CemCem_Lin1Fr06, 'WiprActv', status_req.value) 
            
    def set_wiper_Motor_Error_signal(self, Motor_Error: WiprMotErrSafe,timeout=2):
        promt_info = f"---------------->模拟发送雨刮电机错误信号为{Motor_Error.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, "WiprMotErrSafe", Motor_Error.value) 
            
    def set_wiper_position_signal(self, wiper_position: WiprInWipgArFromWMM):
        promt_info = f"---------------->模拟发送雨刮位置信号为{wiper_position.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.cem_lin1.WmmCem_Lin1Fr01, "WiprInWipgArFromWMM", wiper_position.value) 
            
    
    def check_wiper_position_req(self, position_req: WiprInWipgAr):
        with allure.step(f"Check 雨刮位置请求{position_req.name}"):
            logger.info(f"Check 雨刮位置请求{position_req.name}")
            self.ipdu.check(self.ipdu.cem_lin1.CemCem_Lin1Fr06, 'WiprInWipgAr', position_req.value)
    
    def check_keep_power_car_config(self, indcr_sts: IndcrSts, req: MirrFoldCmdTyp, pos: Union[WinPos, None] = None, timeout=1):
        with allure.step("Check BGM 发出的窗户的开关请求、闪光灯请求、后视镜折叠请求"):
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr92, 'MirrOpenClsReq', req.value, timeout=timeout)
            self.check_windows_position_req(pos_drvr=pos, pos_pass=pos, pos_lere=pos, pos_rire=pos)
            self.check_active_indicator_lamp_req(indcr_sts=indcr_sts, timeout=timeout)

    def set_dcdc_battary_act_sts_on_can(self, DcDcActvd: DcDcActvd):
        with allure.step(f"设置高压电池为 {DcDcActvd.name} 状态"):
            self.set('propulsioncan', 'CddIgmPropFr01', 'DcDcActvd', DcDcActvd.value)
            logger.info(f"设置高压电池为 {DcDcActvd.name} 状态成功")

    def set_dispbattegyout(self, DispBattEgyOut: float):
        with allure.step(f"设置显示输出电量为:{DispBattEgyOut}"):
            self.set('chassiscan2', 'EcmChas2Fr16', 'DispBattEgyOut', DispBattEgyOut)
            logger.info(f"设置电量低报警信息为:{DispBattEgyOut}成功")
            
    def __get_message_thread(self):
        protoparse = ProtoParse()
        data = []
        while self.block_flage:
            msg_data = self.recv_pdu("connectivitycanfd", 0x31A)
            if msg_data is not None:
                # 回复流控帧的设计文档 https://jiduauto.feishu.cn/wiki/GA2iwWxvoi0K4TkOpP2cu2qEnmb
                self.ipdu.send_pdu("connectivitycanfd", 0x33A, [48, 1, 5, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA])
                rx_fm = msg_data[3]
                # logger.info("Get frame: {}".format(rx_fm))
                if rx_fm[0] == 0:
                    data_len = rx_fm[1]
                    data = rx_fm[2:data_len + 2]
                    # logger.info("Get single frame: {}".format(data))
                    blockID = protoparse.get_vehicle_mode(bytes(data)).head.blockID
                    logger.info(f'接收到的Block块的ID是：{blockID}')
                    self.block_bytes[blockID] = data.copy()
                    data = []
                    # break
                elif rx_fm[0] < 32:
                    msg_len = rx_fm[1] + (rx_fm[0] - 16) * 256
                    data = rx_fm[2:]
                    msg_len = msg_len - 62
                    # logger.info("Get first frame: {}".format(data))
                    continue
                elif rx_fm[0] >= 32:
                    if msg_len > 63:
                        data = data + rx_fm[1:]
                        msg_len = msg_len - 63
                        # logger.info(f"剩余的msg_len:{msg_len}")
                        # logger.info("Get continue frame: {}".format(data))
                        continue
                    else:
                        data = data + rx_fm[1:1 + msg_len]
                        # logger.info("Get last frame: {}".format(data))
                        blockID = protoparse.get_vehicle_mode(bytes(data)).head.blockID
                        logger.info(f'接收到的Block块的ID是：{blockID}')
                        self.block_bytes[blockID] = data.copy()
                        data = []
                        # break

    def get_ble_bytes_thread_start(self):
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", 0x31A)
        self.block_flage = True
        with allure.step(f'get 报文 0x31A'):
            self.get_msg_thread = threading.Thread(target=self.__get_message_thread)
            self.get_msg_thread.start()
            sleep(1)

    def get_ble_bytes_thread_stop(self):
        self.block_flage = False
        self.get_msg_thread.join()

    def get_block_bytes(self, blockid:BlockName, timeout: Union[int,float] = 5):
        start_time = time.time()
        while time.time() - start_time < timeout:
            bytes_list = self.block_bytes.get(blockid.value, None)
            if bytes_list:
                self.block_bytes[blockid.value] = None
                return bytes_list
            logger.info(f'已经存储的block数据有：{self.block_bytes}')
            sleep(0.3)
    
    def clear_block_bytes(self):
        self.block_bytes = {}
            

    def get_car_mode_status(self):
        logger.info(f"-------->返回CarMode状态")
        receive_result = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1')
        logger.info(f"-------->通过总线上的信号获取CarMode值为{receive_result}")
        return receive_result

    def wait_time_and_check_carmode(self, car_mode_main_new: CarMode, carmode_sub_new: int, car_mode_main_old: CarMode, carmode_sub_old: int, time: int=30):
        timer = 0
        logger.info(f"开始检测未到达时间时是否保持历史值")
        while timer < time - 5:
            self.check_car_mode_status(car_mode_main=car_mode_main_old,car_mode_sub=carmode_sub_old)
            sleep(5)
            timer = timer + 5
        sleep(time - timer)
        logger.info(f"开始检测到达时间时是否变为期望值")
        self.check_car_mode_status(car_mode_main=car_mode_main_new,car_mode_sub=carmode_sub_new)

    def set_driving_preconditions(self, engSt1WdStsEngSt1WdSts:EngSt1WdStsEngSt1WdSts = EngSt1WdStsEngSt1WdSts.EngSt1_Awake,  imobengsts1: ImobSts=ImobSts.ImobMtn, imobengsts2: ImobSts=ImobSts.ImobMtn, imobengsts3: ImobSts=ImobSts.ImobMtn):
        self.set_engine_sts(EngSt1WdStsEngSt1WdSts=engSt1WdStsEngSt1WdSts)
        self.check('infocanfd', 'BgmInfoCanFdDevFr02', 'FOTAStatus', 0)
        self.check('infocanfd', 'BgmInfoCanFdDevFr02', 'StartInhibitSts', 0)
        self.set('backbonefr', 'VddmBackBoneFr08', 'ImobEngSts1', imobengsts1.value)
        self.set('backbonefr', 'VddmBackBoneFr08', 'ImobEngSts2', imobengsts2.value)
        self.set('backbonefr', 'VddmBackBoneFr08', 'ImobEngSts3', imobengsts3.value)
        time.sleep(1)

    def get_designated_time_expected_message(self, channel, recv_id: [int, list, None] = None,
                                             filter_id: [int, list, None] = None, timeout=2):
        '''
        接收一段时间   指定通道的报文，返回接受的报文信息，每次接收前，要清空buffer
        @param channel: 通道，can lin fr
        @param recv_id: 接收指定的id，可以为单个id 或者一个列表包含多个id,默认为None 接收任意id（除去过滤对的id）报文
        @param filter_id: 过滤掉id，接收到该id的报文不算,可以为单个id 或者一个列表包含多个id，默认None 不过滤id
        @param timeout: 接收的一段时间，接收到报文（除去过滤的报文）就退出，接收不到就一直等到超时退出
        @return: [msg1，msg2 ....]/None
        '''
        return self.ipdu.get_designated_time_expected_message(channel,recv_id,filter_id,timeout)


    def get_current_expected_message(self, channel, recv_id: [int, list, None] = None,
                                     filter_id: [int, list, None] = None, timeout=2):
        '''
        接收 指定通道的报文，返回接受的报文信息，每次接收前，要清空buffer
        @param channel: 通道，can lin fr
        @param recv_id: 接收指定的id，可以为单个id 或者一个列表包含多个id,默认为None 接收任意id（除去过滤对的id）报文
        @param filter_id: 过滤掉id，接收到该id的报文不算,可以为单个id 或者一个列表包含多个id，默认None 不过滤id
        @param timeout: 接收的超时时间，接收到报文（除去过滤的报文）就退出，接收不到就一直等到超时退出
        @return: msg/None
        '''
        
        return self.ipdu.get_current_expected_message(channel,recv_id,filter_id,timeout)

    def check_InfoCan_FOTAStatus(self, infocanfotastatus: InfoCanFOTAStatus):
        with allure.step(f"检查InfoCan FOTAStatus状态"):
            return  self.check('infocanfd', 'BgmInfoCanFdDevFr02', 'FOTAStatus',infocanfotastatus)

    def set_keyconnected_and_keytype_sts(self, keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.NoKeyConnected, time_wait:  int=3):
        with allure.step(f"Set 当前第{keyslot.name}的连接状态为{isconnect.name}, 钥匙连接类型为{keyconnecttype.name}"):
            logger.info(f"Set 当前第{keyslot.name}的连接状态为{isconnect}, 钥匙连接类型为{keyconnecttype.name}")
            if keyslot.name == "FirstKey":
                self.set("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo1KeyConnectSts", isconnect.value)
                self.set("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo1KeyTyp", keyconnecttype.value)     
                       
            elif keyslot.name == "SecondKey":
                self.set("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo2KeyConnectSts", isconnect.value)
                self.set("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo2KeyTyp", keyconnecttype.value) 
                 
            elif keyslot.name == "TheThirdKey":
                self.set("connectivitycanfd", "BncmConnectivityFr19", "DigKeyConnectInfo3KeyConnectSts", isconnect.value)
                self.set("connectivitycanfd", "BncmConnectivityFr19", "DigKeyConnectInfo3KeyTyp", keyconnecttype.value)  
                                
            elif keyslot.name == "TheFourthKey": 
                self.set("connectivitycanfd", "BncmConnectivityFr19", "DigKeyConnectInfo4KeyConnectSts", isconnect.value)
                self.set("connectivitycanfd", "BncmConnectivityFr19", "DigKeyConnectInfo4KeyTyp", keyconnecttype.value)   
                
            elif keyslot.name == "All":    
                self.set("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo1KeyConnectSts", isconnect.value)
                self.set("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo1KeyTyp", keyconnecttype.value)
                self.set("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo2KeyConnectSts", isconnect.value)
                self.set("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo2KeyTyp", keyconnecttype.value)    
                self.set("connectivitycanfd", "BncmConnectivityFr19", "DigKeyConnectInfo3KeyConnectSts", isconnect.value)
                self.set("connectivitycanfd", "BncmConnectivityFr19", "DigKeyConnectInfo3KeyTyp", keyconnecttype.value)    
                self.set("connectivitycanfd", "BncmConnectivityFr19", "DigKeyConnectInfo4KeyConnectSts", isconnect.value)
                self.set("connectivitycanfd", "BncmConnectivityFr19", "DigKeyConnectInfo4KeyTyp", keyconnecttype.value)     
                                                                             
            else:
                logger.info(f"No valid key connection")
                assert False

    def check_glove_box_req_and_lock_sts(self, actiontype:ActionType, ison: GloveBoxStatus, time_wait:  int=1):
        promt_info = f"---------------->校验总线手套箱{actiontype.name}状态为{ison.name}"
        with allure.step(promt_info):
            if actiontype.name == "PrivatetLockSts": 
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, 'LockgPrsnlSts', ison.value)
                
            elif actiontype.name == "GloveBoxReq":  
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, 'RmnLockgPrsnlReq', ison.value)  
                            
            else:
                logger.info(f"The request type is not supported")
                assert False
                
        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)

    def check_glove_box_req(self, ison: Union[GloveBoxStatus, None] = None, timeout=2):  
        with allure.step(f"Check 在条件不满足的情况下不发手套箱RmnLockgPrsnlReq请求"):
            logger.info(f"Check 在条件不满足的情况下不发手套箱RmnLockgPrsnlReq请求")
            ori_data = self.ipdu.check_signal(self.ipdu.backbonefr.CemBackBoneFr08, 'RmnLockgPrsnlReq', timeout)
            logger.info(f"获取{timeout}秒内的RmnLockgPrsnlReq原始数据是:{ori_data}")
            check_result = check_all_value_is(ori_data, 0)
            logger.info(f"Check 结果是：{check_result}")
            assert check_result   

    def check_glove_box_private_lock_sts(self, ison: Union[GloveBoxStatus, None] = None, timeout=2):  
        with allure.step(f"Check 在条件不满足的情况下手套箱私锁状态不置位"):
            logger.info(f"Check 在条件不满足的情况下手套箱私锁状态不置位")
            ori_data = self.ipdu.check_signal(self.ipdu.backbonefr.CemBackBoneFr08, 'LockgPrsnlSts', timeout)
            logger.info(f"获取{timeout}秒内的LockgPrsnlSts原始数据是:{ori_data}")
            check_result = check_all_value_is(ori_data, 0)
            logger.info(f"Check 结果是：{check_result}")
            assert check_result   

    def set_brake_pedal_sts(self, sts:Union[None,YesOrNo] = YesOrNo.Yes, time_wait:  int=2):
        prompt_info = f"---------->设置刹车踏板踩下状态为{sts.name}信号"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)  
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', sts.value)  

        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)
        
    def check_keysearch_req(self, key_zone: KeyZone):
        promt_info = f"----------------> Check 寻钥匙请求:{key_zone.value}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'KeyReadReqFromLockg', key_zone.value)
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'KeyReadReqFromSrv', key_zone.value)
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'KeyReadReqFromVMM', key_zone.value)

    def check_ClimaCmd(self, mai: int):
        with allure.step(f"检查空调的能量水平"):
            self.check('bodycan', 'CemBodyFr99', 'ClimaCmd', mai)
            logger.info(f"检查空调的能量水平无问题，主状态为{mai}")

    def wait_time_and_check_ClimaCmd(self, mai_new: int, mai_old: int,  time: int, ):
        timer = 0
        logger.info(f"开始检测未到达时间时是否保持历史值")
        while timer < time - 1:
            self.check_ClimaCmd(mai=mai_old)
            sleep(1)
            timer = timer + 1
        sleep(time - timer)
        logger.info(f"开始检测到达时间时是否变为期望值")
        self.check_ClimaCmd(mai=mai_new)

    def check_seat_heat_climalvl(self, pos: SeatId, level: HeatVentiLvl):
        promt_info = f"---------------->check BGM 转发座椅加热等级请求"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "FrontLeft":
                logger.info(f"BGM转发主驾的座椅加热等级请求是否为{level.name}")
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'TelmSeatDrvHeatClimaLvl', level.value)
            elif pos.name == "FrontRight":
                logger.info(f"BGM转发副驾的座椅加热等级请求是否为{level.name}")
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'TelmSeatPassHeatClimaLvl', level.value)
            elif pos.name == "RearLeft":
                logger.info(f"BGM转发左后的座椅加热等级请求是否为{level.name}")
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr47, 'TelmSeatSecLeHeatClimaLvl', level.value)
            elif pos.name == "RearRow":
                logger.info(f"BGM转发右后的座椅加热等级请求是否为{level.name}")
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr47, 'TelmSeatSecRiHeatClimaLvl', level.value)

    def check_seat_venti_climalvl(self, pos: SeatId, level: HeatVentiLvl):
        promt_info = f"---------------->check BGM 转发座椅通风等级请求"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "FrontLeft":
                logger.info(f"BGM转发主驾的座椅通风等级请求是否为{level.name}")
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'TelmSeatDrvVentnClimaLvl', level.value)
            elif pos.name == "FrontRight":
                logger.info(f"BGM转发主驾的座椅通风等级请求是否为{level.name}")
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr47, 'TelmSeatPassVentnClimaLvl', level.value)
            elif pos.name == "RearLeft":
                logger.info(f"BGM转发主驾的座椅通风等级请求是否为{level.name}")
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr47, 'TelmSeatSecLeVentnClimaLvl', level.value)
            elif pos.name == "RearRow":
                logger.info(f"BGM转发主驾的座椅通风等级请求是否为{level.name}")
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr47, 'TelmSeatSecRiVentnClimaLvl', level.value)

    def check_seat_venti_level_sts(self, pos: SeatId, level: HeatVentiLvl):
        promt_info = f"---------------->check BGM 转发的座椅通风等级请求"
        with allure.step(promt_info):
            logger.info(promt_info)
            if pos.name == "FrontLeft":
                logger.info(f"BGM转发的座椅通风等级请求是否为{level.name}")
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr14, 'DrvrSeatVentnLvlSts', level.value)
            elif pos.name == "FrontRight":
                logger.info(f"BGM转发的座椅通风等级请求是否为{level.name}")
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr14, 'PassSeatVentnLvlSts', level.value)

    def check_lock_status_for_user(self, sts: StsForUsrFb, time_wait:  int=2):
        prompt_info = f"---------->校验总线中央锁状态反馈为{sts.name}信号"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, 'LockgCenStsForUsrFb', sts.value)  


        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)
        
    def set_door_lock_status(self, doorid:DoorId, lock_sts:Locksts, time_wait = 0):
        prompt_info = f"---------->设置当前{doorid.name}侧门锁状态为{lock_sts.name}状态"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if doorid.name == "kDoorFrontLeft":
              self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, "DoorDrvrLockSts", lock_sts.value)
              
            elif doorid.name == "kDoorFrontRight":
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, "DoorPassLockSts", lock_sts.value)
                
            elif doorid.name == "kDoorRearLeft":
                self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, "DoorLeReLockSts", lock_sts.value)
                
            elif doorid.name == "kDoorRearRight":
                self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, "DoorRiReLockSts", lock_sts.value)
                
            elif doorid.name == "kDoorAll":
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, "DoorDrvrLockSts", lock_sts.value)
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, "DoorPassLockSts", lock_sts.value)
                self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, "DoorLeReLockSts", lock_sts.value)
                self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, "DoorRiReLockSts", lock_sts.value)
            else:
                logger.info(f"The request type is not supported")
                assert False
                
        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)                

    def check_lock_unlock_event(self, event:bool,  time_wait = 1):
        prompt_info = f"----------校验总线解闭锁event当前信号跳变状态为{event}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsUpdEve", event)
            
        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)

    def send_signal_and_get_time(self, signal_info_set: list):
        vo_signal_send_info = []
        for signal_info in signal_info_set:
            signal_temp = signal_info
            self.set(signal_temp[2], signal_temp[4], signal_temp[5], int(signal_temp[6]))
            signal_temp.append(time.time())
            vo_signal_send_info.append(signal_temp)
        return vo_signal_send_info
    
    def set_onbd_chrg_handle_sts(self, sts: DCChrgnHndlSts, time_wait: Union[int, float] = 0):
        with allure.step(f"设置交流电充电枪状态为：{sts.name}"):
            logger.info(f"设置交流电充电枪状态为：{sts.name}")
            self.set('propulsioncan', 'CddObcPropFr01', 'OnBdChrgrHndlSts1', sts.value)
        logger.info(f"等待{time_wait}s")
        sleep(time_wait)

    def set_engine_and_check_energy_level(self, engine:Union[EngSt1WdStsEngSt1WdSts, None] = None,
                         mai:Union[int, None] = None):
        prompt_info = f"设置发动机状态为{engine.name},Check车身能量水平EgyLvlElecMai是否为0"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.set('backbonefr', 'VddmBackBoneFr00', 'EngSt1WdStsEngSt1WdSts', engine.value)
            if mai is not None:
                self.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", mai) 

    def check_door_without_open_req(self, drv_opener: Union[DoorOpenerReq, None] = None, 
                                    pass_opener: Union[DoorOpenerReq, None] = None, 
                                    lere_opener: Union[DoorOpenerReq, None] = None, 
                                    rire_opener: Union[DoorOpenerReq, None] = None, 
                                    timeout:Union[int,float] = 2):
        with allure.step(f"Check 在条件不满足的情况下BGM不发送车门动作请求"):
            logger.info(f"Check 在条件不满足的情况下BGM不发送车门动作请求")

            if drv_opener is not None:
                logger.info(f"--------->Check BGM没有发出主驾车门动作请求")
                ori_data = self.ipdu.check_signal(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2',timeout=timeout)
                value = drv_opener.value

            if pass_opener is not None:
                logger.info(f"--------->Check 没有发出副驾车门动作请求")
                ori_data = self.ipdu.check_signal(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqDoorOpenerReq2',timeout=timeout)
                value = pass_opener.value

            if lere_opener is not None:
                logger.info(f"--------->Check BGM没有发出左后车门动作请求")
                ori_data = self.ipdu.check_signal(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqDoorOpenerReq2',timeout=timeout)
                value = lere_opener.value

            if rire_opener is not None:
                logger.info(f"--------->Check BGM没有发出右后车门动作请求")
                ori_data = self.ipdu.check_signal(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2',timeout=timeout)
                value = rire_opener.value
                
            logger.info(f"获取{timeout}秒原始数据是:{ori_data}")
            check_result = get_signal_times_interval(ori_data, value)
            logger.info(f"Check 结果是：{check_result}")
            assert check_result[0] == 0
            
    def check_door_open_pos_and_trigsrc(self, doorpos: Union[DoorPos, None] = None,
                              position: Union[int, None] = None,
                              door_trigsrc: Union[DoorTrigerSource, None] = None,
                              timeout: Union[float, int] = 0
                              ):
        prompt_info = f"Check 当前{doorpos.name}车门发出的指定门开度为{position}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if doorpos.name == "Dirver":
                logger.info(f"--------->Check 主驾门门开度请求为{position}")
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr05, "DoorDrvrTargPercReqFromHmi", position)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr78, "DoorOpenerDrvrReqTrigSrc", door_trigsrc.value)
                
            elif doorpos.name == "Pass":
                logger.info(f"--------->Check 副驾门门开度请求为{position}")
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr05, "DoorPassTargPercReqFromHmi", position)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr79, "DoorOpenerPassReqTrigSrc", door_trigsrc.value)

            elif doorpos.name == "RearLeft":
                logger.info(f"--------->Check 左后门门开度请求为{position}")
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr05, "DoorLeReTargPercReqFromHmi", position)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr78, "DoorOpenerLeReReqTrigSrc", door_trigsrc.value)
                
            elif doorpos.name == "RearRight":
                logger.info(f"--------->Check 右后门开度请求为{position}")
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr05, "DoorRiReTargPercReqFromHmi", position)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr79, "DoorOpenerRiReReqTrigSrc", door_trigsrc.value)

            elif doorpos.name == "All":
                logger.info(f"--------->Check 四门门开度请求为{position}")
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr05, "DoorDrvrTargPercReqFromHmi", position)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr78, "DoorOpenerDrvrReqTrigSrc", door_trigsrc.value)
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr05, "DoorPassTargPercReqFromHmi", position)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr79, "DoorOpenerPassReqTrigSrc", door_trigsrc.value)
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr05, "DoorLeReTargPercReqFromHmi", position)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr78, "DoorOpenerLeReReqTrigSrc", door_trigsrc.value)
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr05, "DoorRiReTargPercReqFromHmi", position)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr79, "DoorOpenerRiReReqTrigSrc", door_trigsrc.value)

            else:
                logger.info(f"The request type is not supported")
                assert False

                
        logger.info(f"--------->等待{timeout}")
        sleep(timeout)  

    def set_child_lock_sts(self, side:Side, childlockstatus:OnOffSafe1, timeout: Union[float, int] = 0):
        prompt_info = f"---------Set {side.name}侧门的儿童锁状态为{childlockstatus.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if side.name == "Left":
                logger.info(f"--------->Set 左后儿童锁状态为{childlockstatus.name}")
                self.set_singal("bodycan", "RldmBodyFr01", "ChdLockLeftSts", childlockstatus.value) 
                
            elif side.name == "Right":
                logger.info(f"--------->Set 右后儿童锁状态为{childlockstatus.name}")
                self.set_singal("bodycan", "RrdmBodyFr01", "ChdLockRightSts", childlockstatus.value) 
                
            elif side.name == "All":
                logger.info(f"--------->Set 两侧儿童锁状态为{childlockstatus.name}")
                self.set_singal("bodycan", "RldmBodyFr01", "ChdLockLeftSts", childlockstatus.value) 
                self.set_singal("bodycan", "RrdmBodyFr01", "ChdLockRightSts", childlockstatus.value) 
            else:
                logger.info(f"The request type is not supported")
                assert False

                
        logger.info(f"--------->等待{timeout}")
        sleep(timeout)  

    def set_door_perc_position(self, doorpos: Union[DoorPos, None] = None,
                              perc_position: Union[str, int] = None,
                              timeout: Union[float, int] = 0
                              ):
        prompt_info = f"Set 当前{doorpos.name}车门开启角度为{perc_position}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if doorpos.name == "Dirver":
                logger.info(f"--------->设置主驾门当前开度为{perc_position}")
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorDrvrPercPosn", perc_position)
            
            elif doorpos.name == "Pass":
                logger.info(f"--------->设置副驾门当前开度为{perc_position}")
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorPassPercPosn", perc_position)


            elif doorpos.name == "RearLeft":
                logger.info(f"--------->设置左后门当前开度为{perc_position}")
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorLeRePercPosn", perc_position)

            elif doorpos.name == "RearRight":
                logger.info(f"--------->设置右后门当前开度为{perc_position}")
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, "DoorRiRePercPosn", perc_position)


            elif doorpos.name == "All":
                logger.info(f"--------->设置四门当前开度为{perc_position}")
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorDrvrPercPosn", perc_position)
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorPassPercPosn", perc_position)
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorLeRePercPosn", perc_position)
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, "DoorRiRePercPosn", perc_position)

            else:
                logger.info(f"The request type is not supported")
                assert False

                
        logger.info(f"--------->等待{timeout}")
        sleep(timeout)       

    def set_fota_JiDUCharging(self, isConnect: bool=False, isPrivate: bool=True):
        if isConnect:
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1)
            if isPrivate:
                self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr02, 'JIDUChgrFlg', 3)
                self.ipdu.set(self.ipdu.connectivitycanfd.BncmBsrmConnectivityFr03, 'ChrgrPileInfo', 1)
            else:
                self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr02, 'JIDUChgrFlg', 2)
                self.ipdu.set(self.ipdu.connectivitycanfd.BncmBsrmConnectivityFr03, 'ChrgrPileInfo', 0)
        else:
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        time.sleep(0.5)
    
    def check_ChrgLidManvgDCorAcDc_CalReq2 (self, Req2: Inact):
        with allure.step(f"检查充电口盖标定请求状态"):
            self.check('cem_lin2', 'CemCem_Lin2Fr06', 'ChrgLidManvgDCorAcDcCalReq2', Req2.value)
            logger.info(f"检查充电口盖标定请求状态，状态为{Req2.name}")

    def set_ChrgLidManvgDCorAcDc_CalRqrdFb(self, CalRqrdFb: bool):
        with allure.step(f"设置充电口盖标定反馈状态 {CalRqrdFb} 状态"):
            self.set('cem_lin2', 'PrldCem_Lin2Fr02', 'ChrgLidManvgDCorAcDcCalRqrdFb', CalRqrdFb)
            logger.info(f"设置充电口盖标定反馈状态 {CalRqrdFb} 状态")

    def set_ChrgLidManvgDCorAcDc_CalActvSts2(self, ActvSts2: Inact):
        with allure.step(f"设置充电口盖标定激活状态 {ActvSts2.name} 状态"):
            self.set('cem_lin2', 'PrldCem_Lin2Fr02', 'ChrgLidManvgDCorAcDcCalActvSts2', ActvSts2.value)
            logger.info(f"设置充电口盖标定激活状态 {ActvSts2.name} 状态")
    
    def set_BrkSysSts_BrkSys_Capability(self, BrkSysCap: BrkSysCap):
        with allure.step(f"设置博世平台的L3状态信号为 {BrkSysCap.name} 状态"):
            self.set('backbonefr', 'BcmVddmBackBoneFr02', 'BrkSysStsBrkSysCapability', BrkSysCap.value)
            logger.info(f"设置博世平台的L3状态信号为 {BrkSysCap.name} 状态成功")

    def check_VMM_BrkgSys_SelfTestFlg(self, SelfTestFlg: bool):
        with allure.step(f"检查自检标志状态"):
            self.check('infocanfd', 'BgmInfoCanFdFr18', 'VMMBrkgSysSelfTestFlg', SelfTestFlg)
            logger.info(f"检查自检标志状态无问题，状态为{SelfTestFlg}")

    def check_PrkgFctTestPndReq_From_VMM(self, ReqSts2: ReqSts2):
        with allure.step(f"检查自检功能触发请求状态"):
            self.check('backbonefr', 'VgmBackBoneFr03', 'PrkgFctTestPndReqFromVMM', ReqSts2.value)
            logger.info(f"检查自检功能触发请求无问题，状态为{ReqSts2.name}")
            
            
    #o_fan.liu edit
    def set_steerwheel_remHeat_sts(self, level: RemSteerWhlHeatgLvlReqLevel, time_wait: Union[float, int] = 0):
        with allure.step(f"设置远程方向盘加热等级为{level.name}"):
            # self.set('bodycan', 'CcmBodyFr61', 'RemSteerWhlHeatgLvlReq', level.value)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr61, "RemSteerWhlHeatgLvlReq", level.value)
            logger.info(f"设置远程方向盘加热等级为{level.name}成功")
            sleep(time_wait)
            
            
    #o_fan.liu edit        
    def check_steerwheel_DesPower_req(self, lev_sts: HeatLevel, DesPwr_sts: DesPwr):   
        with allure.step(f"Check BGM 方向盘加热相关的功率：加热等级{lev_sts.name},预计功率{DesPwr_sts.name}"):
            logger.info(f"Check BGM 方向盘加热相关的功率：加热等级{lev_sts.name},预计功率{DesPwr_sts.name}")
            self.check('backbonefr', 'CemBackBoneFr19', 'SteerWhlHeatgLvlSts', lev_sts.value)
            self.check('bodycan', 'CEMBodyFr11', 'SteerWhlHeatgDesPwr', DesPwr_sts.value)
            
            
    #o_fan.liu edit             
    def set_steerwheel_PwrAllwd(self, PwrAllwd_val: Union[int, float] = 90):    #LF
        logger.info("设置允许功率为{}".format(PwrAllwd_val))  
        with allure.step(f"设置允许功率为{PwrAllwd_val}"):
            # self.set("bodycan", "CcmBodyFr03", 'SteerWhlHeatgPwrAllwd', PwrAllwd_val) 
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, "SteerWhlHeatgPwrAllwd", PwrAllwd_val)
            logger.info(f"设置允许功率为{PwrAllwd_val}")
    
    def set_OnBdChrgrHndlSts1(self, OnBdChrgrHndlSts: OnBdChrgrHndlSts):
        with allure.step(f"设置交流充电枪为 {OnBdChrgrHndlSts.name} 状态"):
            self.set('propulsioncan', 'CddObcPropFr01', 'OnBdChrgrHndlSts1', OnBdChrgrHndlSts.value)
            logger.info(f"设置交流充电枪为 {OnBdChrgrHndlSts.name} 状态")


    def set_blekeyconnected_and_keytype_sts(self, keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.NoKeyConnected, zone=BLEKeyPrsntZone.Zone0, time_wait:  int=3):
        with allure.step(f"Set 当前第{keyslot.name}的连接状态为{isconnect.name}, 钥匙连接类型为{keyconnecttype.name}"):
            logger.info(f"Set 当前第{keyslot.name}的连接状态为{isconnect}, 钥匙连接类型为{keyconnecttype.name}")
            if keyslot.name == "FirstKey":
                self.set("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo1KeyConnectSts", isconnect.value)
                self.set("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo1KeyPrsntZone", zone.value)
                self.set("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo1KeyTyp", keyconnecttype.value)     
                       
            elif keyslot.name == "SecondKey":
                self.set("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo2KeyConnectSts", isconnect.value)
                self.set("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo2KeyPrsntZone", zone.value)
                self.set("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo2KeyTyp", keyconnecttype.value) 
                 
            elif keyslot.name == "TheThirdKey":
                self.set("connectivitycanfd", "BncmConnectivityFr19", "DigKeyConnectInfo3KeyConnectSts", isconnect.value)
                self.set("connectivitycanfd", "BncmConnectivityFr19", "DigKeyConnectInfo3KeyPrsntZone", zone.value)
                self.set("connectivitycanfd", "BncmConnectivityFr19", "DigKeyConnectInfo3KeyTyp", keyconnecttype.value)  
                                
            elif keyslot.name == "TheFourthKey": 
                self.set("connectivitycanfd", "BncmConnectivityFr19", "DigKeyConnectInfo4KeyConnectSts", isconnect.value)
                self.set("connectivitycanfd", "BncmConnectivityFr19", "DigKeyConnectInfo4KeyPrsntZone", zone.value)
                self.set("connectivitycanfd", "BncmConnectivityFr19", "DigKeyConnectInfo4KeyTyp", keyconnecttype.value)   
                
            elif keyslot.name == "All":    
                self.set("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo1KeyConnectSts", isconnect.value)
                self.set("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo1KeyPrsntZone", zone.value)
                self.set("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo1KeyTyp", keyconnecttype.value)
                self.set("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo2KeyConnectSts", isconnect.value)
                self.set("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo2KeyPrsntZone", zone.value)
                self.set("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo2KeyTyp", keyconnecttype.value)    
                self.set("connectivitycanfd", "BncmConnectivityFr19", "DigKeyConnectInfo3KeyConnectSts", isconnect.value)
                self.set("connectivitycanfd", "BncmConnectivityFr19", "DigKeyConnectInfo3KeyPrsntZone", zone.value)
                self.set("connectivitycanfd", "BncmConnectivityFr19", "DigKeyConnectInfo3KeyTyp", keyconnecttype.value)    
                self.set("connectivitycanfd", "BncmConnectivityFr19", "DigKeyConnectInfo4KeyConnectSts", isconnect.value)
                self.set("connectivitycanfd", "BncmConnectivityFr19", "DigKeyConnectInfo4KeyPrsntZone", zone.value)
                self.set("connectivitycanfd", "BncmConnectivityFr19", "DigKeyConnectInfo4KeyTyp", keyconnecttype.value)     
                                                                             
            else:
                logger.info(f"No valid key connection")
                assert False
    
    def check_ChrgHndlStrtEna(self, ChrgHndlStrtEna: ChrgHndlStrtEna):
        with allure.step(f"判断usagemode的充电请求"):
            self.check('backbonefr', 'CemBackBoneFr03', 'ChrgHndlStrtEna', ChrgHndlStrtEna.value)
            logger.info(f"判断usagemode的充电请求,状态为{ChrgHndlStrtEna.name}")

    def set_OnBdChrgrHndlSts1_function_safe(self, OnBdChrgrHndlSts:OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected,ub_flag:bool = True):
        prompt_info = f"---------->设置交流充电枪相关信号"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if OnBdChrgrHndlSts is not None:
                logger.info(f"交流充电枪状态设为{OnBdChrgrHndlSts.name}")
                self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', OnBdChrgrHndlSts.value, ub_flag = ub_flag)

    def set_dc_chrg_handle_sts_function_safe(self, sts:DCChrgnHndlSts = DCChrgnHndlSts.Disconnected, ub_flag:bool = True):
        prompt_info = f"---------->设置直流充电枪相关信号"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if sts is not None:
                logger.info(f"直流充电枪状态设为{sts.name}")
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr29, 'DCChrgnHndlSts', sts.value, ub_flag = ub_flag)

    def set_alm_led_fault(self, alm_num: AlmNum, sts: AlmSts):
        with allure.step(f"==============>制造{alm_num.name}产生LED故障"):
            self.set_singal("CEM_LIN5", f"CemCem_Lin5Fr{alm_num.value + 9}", f"{alm_num.name}FailrStsLEDSts", sts.value)
            sleep(0.1)

    def set_alm_vlt_fault(self, alm_num: AlmNum, sts: AlmSts):
        with allure.step(f"==============>制造{alm_num.name}产生Vlt故障"):
            self.set_singal("CEM_LIN5", f"CemCem_Lin5Fr{alm_num.value + 9}", f"{alm_num.name}FailrStsVltSts", sts.value)
            sleep(0.1)

    def set_alm_tmp_fault(self, alm_num: AlmNum, sts: AlmSts):
        with allure.step(f"==============>制造{alm_num.name}产生Tmp故障"):
            self.set_singal("CEM_LIN5", f"CemCem_Lin5Fr{alm_num.value + 9}", f"{alm_num.name}FailrStsTmpSts", sts.value)
            sleep(0.1)

    def check_alm_flt(self, alm_num: AlmNum, sts: AlmSts):
        with allure.step(f"==============>校验{alm_num.name}Flt的值为{sts.value}"):
            self.check_singal("BackboneFR", "CemBackBoneFr38", f"{alm_num.name}Flt", sts.value)

    def check_courtesy_light_req(self, sts: ReadLampSts):
        with allure.step(f"==============>检验阅读灯状态是否为{sts.name}"):
            self.check_intr_light_read_lamp_req(
                zone=ReadLampZone.FrontLeft, sts=sts
            )
            self.check_intr_light_read_lamp_req(
                zone=ReadLampZone.FrontRight, sts=sts
            )
            self.check_intr_light_read_lamp_req(
                zone=ReadLampZone.RearLeft, sts=sts
            )
            self.check_intr_light_read_lamp_req(
                zone=ReadLampZone.RearRight, sts=sts
            )

    def pause_OHC(self, wait_time):
        with allure.step("==============>暂停OHC接收所有LIN信号"):
            self.pause_ecu_send("cem_lin1", "OHC")
            self.pause_ecu_send("cem_lin2", "OHC")
            self.pause_ecu_send("cem_lin3", "OHC")
            self.pause_ecu_send("cem_lin4", "OHC")
            self.pause_ecu_send("cem_lin5", "OHC")
            self.pause_ecu_send("cem_lin6", "OHC")
        sleep(wait_time)

    def resume_OHC(self, wait_time):
        with allure.step("==============>恢复OHC接收所有LIN信号"):
            self.resume_ecu_send("cem_lin1", "OHC")
            self.resume_ecu_send("cem_lin2", "OHC")
            self.resume_ecu_send("cem_lin3", "OHC")
            self.resume_ecu_send("cem_lin4", "OHC")
            self.resume_ecu_send("cem_lin5", "OHC")
            self.resume_ecu_send("cem_lin6", "OHC")
        sleep(wait_time)

    def set_door_latch_posn(self, doorid: DoorId, latposn:LatPosition,  time_wait = 0):
        prompt_info = f"----------设置{doorid.name}侧门的锁舌位置为{latposn.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if doorid.name == "kDoorFrontLeft":
              self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, "DoorDrvrLatPosn", latposn.value)
              
            elif doorid.name == "kDoorFrontRight":
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, "DoorPassLatPosn", latposn.value)
                
            elif doorid.name == "kDoorRearLeft":
                self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, "DoorLeReLatPosn", latposn.value)
                
            elif doorid.name == "kDoorRearRight":
                self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, "DoorRiReLatPosn", latposn.value)
                
            elif doorid.name == "kDoorAll":
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, "DoorDrvrLatPosn", latposn.value)
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, "DoorPassLatPosn", latposn.value)
                self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, "DoorLeReLatPosn", latposn.value)
                self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, "DoorRiReLatPosn", latposn.value)
                
            else:
                logger.info(f"The request type is not supported")
                assert False

    def set_windows_short_drop_sts(self, doorid: DoorId, shortdropsts:ShortDropSts,  time_wait = 0):
        prompt_info = f"----------设置{doorid.name}当前车窗短降状态为{shortdropsts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if doorid.name == "kDoorFrontLeft":
              self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, "ShortDropWinDrvrSts", shortdropsts.value)
              
            elif doorid.name == "kDoorFrontRight":
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, "ShortDropWinPassSts", shortdropsts.value)
                
            elif doorid.name == "kDoorRearLeft":
                self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, "ShortDropWinReLeSts", shortdropsts.value)
                
            elif doorid.name == "kDoorRearRight":
                self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, "ShortDropWinReRiSts", shortdropsts.value)
                
            elif doorid.name == "kDoorAll":
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, "ShortDropWinDrvrSts", shortdropsts.value)
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, "ShortDropWinPassSts", shortdropsts.value)
                self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, "ShortDropWinReLeSts", shortdropsts.value)
                self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, "ShortDropWinReLeSts", shortdropsts.value)
                
            else:
                logger.info(f"The request type is not supported")
                assert False
    def set_max_ClimaActv_sts(self, sts:isOn):
        prompt_info = f"---------->设置空调相关信号"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if sts is not None:
                logger.info(f"设置空调为{sts.name}")
                self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', sts.value)

    def check_telm_clima_req(self, sts:RemHvStrtActvReq):
        prompt_info = f"--------->Check BGM有没有发出远程实时空调开启请求：{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if sts is not None:
                self.check_singal("bodycan", "CemBodyFr47", "TelmClimaReq", sts.value)

    def check_telm_clima_temp_range(self, sts:Union[float, int] = 16.0):
        prompt_info = f"--------->Check BGM有没有发出温度：{sts}℃"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if sts is not None:   
                self.check_singal("bodycan", "CemBodyFr47", "TelmClimaTSetTempRange", sts)

    def check_telm_clima_cmptmt_spcl(self, sts:ClimateSpcl):
        prompt_info = f"--------->Check BGM有没有发出温度档位：{sts.value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if sts is not None:
                self.check_singal("bodycan", "CemBodyFr47", "TelmClimaTSetHmiCmptmtTSpSpcl", sts.value)
    def set_vehicle_rollover_and_inclination_angles(self, rangetype: RangeType, 
                                                    incln: Union[float, int] = None, 
                                                    roll: Union[float, int] = None, 
                                                    time_wait = 0):
        if rangetype.name == "RoadIncln":
            with allure.step(f'设置车辆倾斜角度：{incln}'):
                logger.info(f'设置车辆倾斜角度：{incln}')
                self.set("backbonefr", "BcmVddmBackBoneFr00", "RoadInclnQly", 1)
                self.set("backbonefr", "BcmVddmBackBoneFr00", "RoadInclnRoadIncln", incln)
                
        elif rangetype.name == "RollAgGlb":
            with allure.step(f'设置车辆翻转角度：{roll}'):
                logger.info(f'设置车辆翻转角度：{roll}')
                self.set("backbonefr", "BcmVddmBackBoneFr13", "RollAgGlbQf", 1)
                self.set("backbonefr", "BcmVddmBackBoneFr13", "RollAgGlbVal", roll)

        else:
            logger.info(f"The request type is not supported")
            assert False
            
        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)  

    def check_child_lock_unlock_req(self, childlockside: RotateDirec, lockreq: LockgCenReq2, time_wait: Union[float, int] = 0):
        if childlockside.name == "Left":
            with allure.step(f'校验左侧儿童锁请求状态为：{lockreq.name}'):
                logger.info(f'校验左侧儿童锁请求状态为：{lockreq.name}')
                self.check("bodycan","CemBodyFr09", 'ChdLockReLeCtrlHmiReq', lockreq.value)
                
        elif childlockside.name == "Right":
            with allure.step(f'校验右侧儿童锁请求状态为：{lockreq.name}'):
                logger.info(f'校验右侧儿童锁请求状态为：{lockreq.name}')
                self.check("bodycan","CemBodyFr09", 'ChdLockReRiCtrlHmiReq', lockreq.value)

        elif childlockside.name == "All":
            with allure.step(f'校验左右两侧儿童锁请求状态为：{lockreq.name}'):
                logger.info(f'校验左右两侧儿童锁请求状态为：{lockreq.name}')
                self.check("bodycan","CemBodyFr09", "ChdLockReLeCtrlHmiReq", lockreq.value)
                self.check("bodycan","CemBodyFr09", "ChdLockReRiCtrlHmiReq", lockreq.value)
        else:
            logger.info(f"The request type is not supported")
            assert False
                
        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)  
        
    def check_WshrFldTankStsToHMI(self,expect_value,sleep_time=0):
        prompt_info = f"---------->设置完开关状态后检查 WshrFldTankStsToHMI 信号值，期望值为：{expect_value}，等待上报时间：{sleep_time}s"
        with allure.step(prompt_info):
            sleep(sleep_time)
            self.check('backbonefr', 'CemBackBoneFr18', 'WshrFldTankStsToHMI', expect_value)

    def check_ApproachUnlockHmi(self,ConfigValue,time_wait: Union[float, int] = 0):
        prompt_info = f"---------->校验近车解锁开关设置项，期望值为：{ConfigValue}，等待上报时间：{time_wait}s"
        with allure.step(prompt_info):
            self.check("connectivitycanfd", "BgmConnectivityFr18", "ApproachUnlockHmi", ConfigValue)

    def check_WalkAwayLockHmi(self,AutoLockOnLeave,time_wait: Union[float, int] = 0):
        prompt_info = f"---------->校验离车落锁开关设置项，期望值为：{AutoLockOnLeave}，等待上报时间：{time_wait}s"
        with allure.step(prompt_info):
            self.check("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", AutoLockOnLeave)
    
    "*********************************************************以下为mock mcu专用接口，请不要插入写入*********************************************************************************"
    
    def cdd_set_usage_mode(self, usage_mode: UsageMode):
        """
        模拟MCU设置使用模式
        @param usage_mode: UsageMode
            ABANDONED = 0
            INACTIVE = 1
            CONVENIENCE = 2
            ACTIVE = 11
            DRIVING = 13
        """
        prompt_info = f"模拟mcu发送给s2s,使用模式UsageMode = {usage_mode.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts',  usage_mode.value)

    def cdd_set_car_mode(self, car_mode: CarMode):
        """
        模拟MCU设置车辆模式
        @param car_mode: CarMode
            NORMAL = 0
            TRANSPORT = 1
            FACTORY = 2
            CRASH = 3
            DYNO = 5
        """
        prompt_info = f"模拟mcu发送给s2s,车辆模式CarMode = {car_mode.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr01, "VehModMngtGlbSafe1CarModSts1", car_mode.value)
    
    def cdd_set_wiper_washer_fluid_low(self, sts: OnOff):
        """
        模拟MCU设置雨刮洗涤液位
        @param sts: OnOff
            Off = 0, 液位不低
            On = 1，液位低
        """
        prompt_info = f"模拟mcu发送给s2s,雨刮洗涤液位低WshrFldTankStsToHMI = {sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WshrFldTankStsToHMI', sts.value)
    
    def cdd_set_rain_sensor_error(self, sts: OnOff):
        """
        模拟MCU设置雨量传感器故障
        @param sts: OnOff
            Off = 0, 无故障
            On = 1，有故障
        """
        prompt_info = f"模拟mcu发送给s2s,雨量传感器故障状态RainSnsrActvnErrToHmi = {sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.set_singal("backbonefr", "CemBackBoneFr19", "RainSnsrActvnErrToHmi", sts.value)
    
    def cdd_set_wiper_sys_fault(self, fault_sts: GeneralFltSts):
        """
        模拟MCU设置雨刮系统故障
        @param fault_sts: GeneralFltSts
            NotVld1 = 0，无效值
            Off = 1，无故障
            On = 2，有故障
            NotVld2 = 3，无效值
        """
        prompt_info = f"模拟mcu发送给s2s, 雨刮内部系统故障WiprSysFailrDetdSafe = {fault_sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'WiprSysFailrDetdSafe', fault_sts.value)
    
    def cdd_set_wiper_position(self, WiprInPrkgPosnLo: Union[OnOff, None] = None, WiprInWipgAr: Union[OnOff, None] = None):
        """
        模拟MCU设置雨刮位置，S2S处理为WiperService::NotifyWiperPosition，通知雨刮位置
            0, 0  --  @value(1)   kWIPING_AREA 刮刷区
            0, 1  --  @value(1)   kWIPING_AREA 刮刷区
            1, 0  --  @value(0)   kPARKED 驻车区
            1, 1  --  last_value
            
        @param WiprInPrkgPosnLo: OnOff, 前挡风玻璃上雨刮操纵杆是否在驻车位置(即最低处)
            Off = 0, 在驻车位置以上(即非最低处)
            On = 1，在驻车位置(即最低处)
            
        @param WiprInWipgAr: OnOff，前挡风玻璃上雨刮器角度
            Off = 0, 角度0(即贴着风挡玻璃)
            On = 1，角度非0（即不贴着风挡玻璃，可能处于维修位置）
        """
        mWiprInWipgAr = WiprInWipgAr.name if WiprInWipgAr is not None else 'last_value'
        mWiprInPrkgPosnLo = WiprInPrkgPosnLo.name if WiprInPrkgPosnLo is not None else 'last_value'
        prompt_info = f"模拟mcu发送给s2s, 雨刮位置WiprInWipgAr = {mWiprInWipgAr}, WiprInPrkgPosnLo = {mWiprInPrkgPosnLo}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if WiprInWipgAr is not None:
                self.set_singal("cem_lin1", "CemCem_Lin1Fr06", 'WiprInWipgAr', WiprInWipgAr.value)
            if WiprInPrkgPosnLo is not None:
                self.set_singal("cem_lin1", "CemCem_Lin1Fr06",  'WiprInPrkgPosnLo', WiprInPrkgPosnLo.value)

    "*********************************************************以上为mock mcu专用接口，请不要插入写入*********************************************************************************"
    
    def set_ChrgLidManvgDCorAcDcOverTrvlFb(self, Fb: bool):
        with allure.step(f"设置充电口盖是否超行程"):
            self.set('cem_lin2', 'PrldCem_Lin2Fr02', 'ChrgLidManvgDCorAcDcOverTrvlFb', Fb)
            logger.info(f"充电口盖是否超行程为{Fb}")

    def set_ChrgLidManvgDCorAcDcBlkFb(self, Fb: bool):
        with allure.step(f"设置充电口盖是否堵塞"):
            self.set('cem_lin2', 'PrldCem_Lin2Fr02', 'ChrgLidManvgDCorAcDcBlkFb', Fb)
            logger.info(f"充电口盖是否堵塞为{Fb}")
    def check_carmode_and_usagemode_sts(self, mode: VehicleMode, 
                                        carmode: Union[CarMode, int] = None,  
                                        usagemode: Union[UsageMode, int] = None,
                                        time_wait: Union[float, int] = 0):
        if mode.name == "CarMode":
            with allure.step(f'校验当前车辆模式为：{carmode.name}'):
                logger.info(f'校验当前车辆模式为：{carmode.name}')
                self.check("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1CarModSts1", carmode.value)
                
        elif mode.name == "UsageMode":
            with allure.step(f'校验当前使用者模式为：{usagemode.name}'):
                logger.info(f'校验当前使用者模式为：{usagemode.name}')
                self.check("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", usagemode.value)

        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait) 


    def check_door_tx(self, drv_tx: Union[Flgsts, None] = None, pass_tx: Union[Flgsts, None] = None,
                          lere_tx: Union[Flgsts, None] = None, rire_tx: Union[Flgsts, None] = None):
        if drv_tx is not None:
            logger.info(f"检查主驾门通讯状态为{drv_tx}")
            self.check("infocanfd","BgmInfoCanFdFr18","FLDoorComFltFlg", drv_tx.value,timeout=1.5)
        if pass_tx is not None:
            logger.info(f"检查副驾门通讯状态为{pass_tx}")
            self.check("infocanfd","BgmInfoCanFdFr18","FRDoorComFltFlg", pass_tx.value,timeout=1.5)
        if lere_tx is not None:
            logger.info(f"检查左后门通讯状态为{lere_tx}")
            self.check("infocanfd","BgmInfoCanFdFr18","RLDoorComFltFlg", lere_tx.value,timeout=1.5)
        if rire_tx is not None:
            logger.info(f"检查右后门通讯状态为{rire_tx}")
            self.check("infocanfd","BgmInfoCanFdFr18","RRDoorComFltFlg", rire_tx.value,timeout=1.5)
            
    def set_fr_gear_pos(self, gear: Gear, time_wait: Union[float, int] = 0):
        prompt_info = f"----------设置backbonefr总线当前挡位处于{gear.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.set("backbonefr","VddmBackBoneFr03", "GearLvrIndcn", gear.value)

        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)  

    def set_door_open_warn_sts(self, side: Side,warn:LcmaIndcn,  time_wait = 0):
        prompt_info = f"----------设置{side.name}侧门的告警状态为{warn.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if side.name == "Left":
                self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", warn.value)
              
            elif side.name == "Right":

                self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", warn.value)
            elif side.name == "All":
                self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", warn.value)
                self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", warn.value)

            else:
                logger.info(f"The request type is not supported")
                assert False
                
        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)     
          
    def check_door_open_resistcmd_sts(self, resistcmd:DoorOpenResistCmd,  time_wait = 0):
        prompt_info = f"----------校验总线当前开门阻力状态为{resistcmd.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr16, "DoorOpenResistCmd", resistcmd.value)

                
        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait) 
        
    def check_without_door_resist_cmd(self, timeout=1.5):
        with allure.step(f"Check 在条件不满足的情况下BGM不发开门阻力使能"):
            logger.info(f"Check 在条件不满足的情况下BGM不发开门阻力使能")
            ori_data = self.ipdu.check_signal(self.ipdu.bodycan.BgmBodyFr16, 'DoorOpenResistCmd', timeout)
            logger.info(f"获取{timeout}秒内的四门开门阻力DoorOpenResistCmd原始数据是:{ori_data}")
            # check_result = check_all_value_is(ori_data, DoorRelsReq.Off)
            check_result = check_all_value_is(ori_data, 0)
            logger.info(f"Check 结果是：{check_result}")
            assert check_result

    def check_ChrgLidManvgDCorAcDc_TqReq2(self, tqreq2: ActTq):
        promt_info = f"---------------->Check BGM 发出的控制充电口盖扭矩请求为{tqreq2.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.check(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcTqReq2', tqreq2.value, timeout=0.3)
            
    def check_static_lighting_mode_en(self, static_lighting_mode_en: StaticLightingModeEn):
        # Check the signal value of StaticLightingModeEn
        with allure.step(f"Check StaticLightingModeEn signal, expected value is {static_lighting_mode_en.value}"):
            self.check("bodyexposedcanfd", "BgmBodyExposedCANFr10", 'StaticLightingModeEn', static_lighting_mode_en.value)
            logger.info(f"StaticLightingModeEn signal check passed, expected value is {static_lighting_mode_en.value}")

    def check_ExtrLtgStsStaticLtgShow(self, ExtrLtgStsStaticLtgShow: ExtrLtgStsStaticLtgShow):
        expected_value = ExtrLtgStsStaticLtgShow.value
        # Check the signal value of StaticLightingModeEn
        with allure.step(f"Check ExtrLtgStsStaticLtgShow signal, expected value is {expected_value}"):
            self.check("backbonefr", "CemBackBoneFr02", "ExtrLtgStsStaticLtgShow", expected_value)
            # 可以在需要时启用以下日志记录，例如调试时
            # logger.info(f"ExtrLtgStsStaticLtgShow signal check passed, expected value is {expected_value}")


    def set_RemClimaHvSts(self,sts:RemoteClimateStatus = RemoteClimateStatus.Invalid):
        prompt_info = f"---------->设置远程上高压：{sts.value}"
        with allure.step(prompt_info):
            self.set("bodycan", "CcmBodyFr22", 'RemClimaHvSts', sts.value)

    def check_TelmSteerWhlHeatgReqLvl(self, level:HeatLevel):
        prompt_info = f"---------->校验方向盘加热等级：{level.name}"
        with allure.step(prompt_info):
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr36, 'TelmSteerWhlHeatgReqLvl', level.value)

    def check_TelmDefrostReq(self, sts:OnOff):
        prompt_info = f"---------->校验远控除霜是否开启：{sts.name}"
        with allure.step(prompt_info):
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr92, 'TelmDefrostReq', sts.value)

    def set_RemClimaDefrstSts(self, sts:OnOff):
        prompt_info = f"---------->设置远程除霜：{sts.name}"
        with allure.step(prompt_info):
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31, 'RemClimaDefrstSts', sts.value)

    def check_HmiDefrstMaxReq(self, sts:OnOff):
        prompt_info = f"---------->校验远控除霜是否开启：{sts.name}"
        with allure.step(prompt_info):
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiDefrstMaxReq', sts.value)
    
    def check_PtInin(self, OnOff: isOn):
        with allure.step(f"检查引脚设置状态"):
            self.check('infocanfd', 'BgmInfoCanFdFr18', 'PtInin', OnOff.value, timeout=0.3)
            logger.info(f"引脚设置状态为{OnOff.name}")

    def check_EngActvnMod1WdReq(self, EngActvnMod1:EngActvnMod1):
        with allure.step(f"检查wakeup信号"):
            self.check('backbonefr', 'CemBackBoneFr03', 'EngActvnMod1WdReq', EngActvnMod1.value, timeout=0.1)
            logger.info(f"wakeup信号状态为{EngActvnMod1.name}")

    def check_IgnRlyCmd(self, OnOff: isOn):
        with allure.step(f"检查IGN继电器状态"):
            self.check('backbonefr', 'CemBackBoneFr14', 'RlyPwrDistbnCmd1WdIgnRlyCmd', OnOff.value, timeout=0.3)
            logger.info(f"IGN继电器状态为{OnOff.name}")

    def check_AI_Inter_actionLamp_Sts(self, AIInteractionLampLeftY, AIInteractionLampRightY):
        with allure.step(f"监测 AI左测指示灯: signal, expected value is AIInteractionLampRightY"):
            self.check_singal("cem_lin2","CemCem_Lin2Fr08",'AIInteractionLampRightY4',AIInteractionLampRightY[0])
            self.check_singal("cem_lin2","CemCem_Lin2Fr08",'AIInteractionLampRightY3',AIInteractionLampRightY[1])
            self.check_singal("cem_lin2","CemCem_Lin2Fr08",'AIInteractionLampRightY2',AIInteractionLampRightY[2])
            self.check_singal("cem_lin2","CemCem_Lin2Fr08",'AIInteractionLampRightY1',AIInteractionLampRightY[3])
        with allure.step(f"监测 AI右测指示灯: signal, expected value is AIInteractionLampLeftY"):
            self.check_singal("cem_lin2","CemCem_Lin2Fr07",'AIInteractionLampLeftY4',AIInteractionLampLeftY[0])
            self.check_singal("cem_lin2","CemCem_Lin2Fr07",'AIInteractionLampLeftY3',AIInteractionLampLeftY[1])
            self.check_singal("cem_lin2","CemCem_Lin2Fr07",'AIInteractionLampLeftY2',AIInteractionLampLeftY[2])
            self.check_singal("cem_lin2","CemCem_Lin2Fr07",'AIInteractionLampLeftY1',AIInteractionLampLeftY[3])

    def set_bncm_key_key_zone(self, zone: Zone, valid: Validity, time_wait: Union[float, int] = 0):
        if zone.name == "Zone0":
            with allure.step(f'仿真发送{zone.name}区域钥匙有效状态:{valid.name}'):
                logger.info(f'仿真发送{zone.name}区域钥匙占位状态:{valid.name}')
                self.set("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone0", valid.value)

        elif zone.name == "Zone1":
            with allure.step(f'仿真发送{zone.name}区域钥匙有效状态:{valid.name}'):
                logger.info(f'仿真发送{zone.name}区域钥匙占位状态:{valid.name}')
                self.set("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone1", valid.value)

        elif zone.name == "Zone2":
            with allure.step(f'仿真发送{zone.name}区域钥匙有效状态:{valid.name}'):
                logger.info(f'仿真发送{zone.name}区域钥匙占位状态:{valid.name}')
                self.set("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone2", valid.value)

        elif zone.name == "Zone3":
            with allure.step(f'仿真发送{zone.name}区域钥匙有效状态:{valid.name}'):
                logger.info(f'仿真发送{zone.name}区域钥匙占位状态:{valid.name}')
                self.set("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone3", valid.value)

        elif zone.name == "Zone4":
            with allure.step(f'仿真发送{zone.name}区域钥匙有效状态:{valid.name}'):
                logger.info(f'仿真发送{zone.name}区域钥匙占位状态:{valid.name}')
                self.set("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone4", valid.value)

        elif zone.name == "Zone5":
            with allure.step(f'仿真发送{zone.name}区域钥匙有效状态:{valid.name}'):
                logger.info(f'仿真发送{zone.name}区域钥匙占位状态:{valid.name}')
                self.set("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone5", valid.value)

        elif zone.name == "Zone6":
            with allure.step(f'仿真发送{zone.name}区域钥匙有效状态:{valid.name}'):
                logger.info(f'仿真发送{zone.name}区域钥匙占位状态:{valid.name}')
                self.set("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone6", valid.value)

        elif zone.name == "Zone7":
            with allure.step(f'仿真发送{zone.name}区域钥匙有效状态:{valid.name}'):
                logger.info(f'仿真发送{zone.name}区域钥匙占位状态:{valid.name}')
                self.set("connectivitycanfd", "BncmConnectivityFr17","BLEKeyPrsntStsZone7", valid.value)

        elif zone.name == "Zone8":
            with allure.step(f'仿真发送{zone.name}区域钥匙有效状态:{valid.name}'):
                logger.info(f'仿真发送{zone.name}区域钥匙占位状态:{valid.name}')
                self.set("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone8", valid.value)

        else:
            logger.error(f"无对应的{zone.name}区域有效钥匙连接")

        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)  

    def set_tailgate_antiPnch_sts(self, sts: bool, time_wait: Union[float, int] = 0):
        prompt_info = f"----------设置尾门防夹状态为{sts}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.set("bodycan","PotBodyFr02", "TrAntiPnch", sts)

        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)  

    def check_driver_prsnt_sts(self, present: NoYesCrit1, time_wait: Union[float, int] = 0):
        prompt_info = f"----------校验驾驶员在位状态为{present.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.set("backbonefr","CemBackBoneFr03", "DrvrPrsntStsDrvrPrsnt", present.value)

        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)

    def check_front_left_alm(self, bright, r, g, b):
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr01",
            signal="OrdinaryAmbientLightFrontLeftBrightness",
            value=bright
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr01",
            signal="OrdinaryAmbientLightFrontLeftRed",
            value=r
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr01",
            signal="OrdinaryAmbientLightFrontLeftGreen",
            value=g
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr01",
            signal="OrdinaryAmbientLightFrontLeftBlue",
            value=b
        )

    def check_front_right_alm(self, bright, r, g, b):
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr04",
            signal="OrdinaryAmbientLightFrontRightBrightness",
            value=bright
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr04",
            signal="OrdinaryAmbientLightFrontRightRed",
            value=r
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr04",
            signal="OrdinaryAmbientLightFrontRightGreen",
            value=g
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr04",
            signal="OrdinaryAmbientLightFrontRightBlue",
            value=b
        )

    def check_rear_left_alm(self, bright, r, g, b):
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr02",
            signal="OrdinaryAmbientLightRearLeftBrightness",
            value=bright
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr02",
            signal="OrdinaryAmbientLightRearLeftRed",
            value=r
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr02",
            signal="OrdinaryAmbientLightRearLeftGreen",
            value=g
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr02",
            signal="OrdinaryAmbientLightRearLeftBlue",
            value=b
        )

    def check_rear_right_alm(self, bright, r, g, b):
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr03",
            signal="OrdinaryAmbientLightRearRightBrightness",
            value=bright
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr03",
            signal="OrdinaryAmbientLightRearRightRed",
            value=r
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr03",
            signal="OrdinaryAmbientLightRearRightGreen",
            value=g
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr03",
            signal="OrdinaryAmbientLightRearRightBlue",
            value=b
        )

    def check_cc_right_alm(self, bright, r, g, b):
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr05",
            signal="OrdinaryAmbientLightCCRightBrightness",
            value=bright
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr05",
            signal="OrdinaryAmbientLightCCRightRed",
            value=r
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr05",
            signal="OrdinaryAmbientLightCCRightGreen",
            value=g
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr05",
            signal="OrdinaryAmbientLightCCRightBlue",
            value=b
        )

    def check_cc_left_alm(self, bright, r, g, b):
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr06",
            signal="OrdinaryAmbientLightCCLeftBrightness",
            value=bright
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr06",
            signal="OrdinaryAmbientLightCCLeftRed",
            value=r
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr06",
            signal="OrdinaryAmbientLightCCLeftGreen",
            value=g
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr06",
            signal="OrdinaryAmbientLightCCLeftBlue",
            value=b
        )

    def check_cc_mid_right_alm(self, bright, r, g, b):
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr09",
            signal="OrdinaryAmbientLightCCMiddleRightBrightness",
            value=bright
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr09",
            signal="OrdinaryAmbientLightCCMiddleRightRed",
            value=r
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr09",
            signal="OrdinaryAmbientLightCCMiddleRightGreen",
            value=g
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr09",
            signal="OrdinaryAmbientLightCCMiddleRightBlue",
            value=b
        )

    def check_cc_mid_left_alm(self, bright, r, g, b):
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr0A",
            signal="OrdinaryAmbientLightCCMiddleLeftBrightness",
            value=bright
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr0A",
            signal="OrdinaryAmbientLightCCMiddleLeftRed",
            value=r
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr0A",
            signal="OrdinaryAmbientLightCCMiddleLeftGreen",
            value=g
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr0A",
            signal="OrdinaryAmbientLightCCMiddleLeftBlue",
            value=b
        )

    def check_twe_left_alm(self, bright, r, g, b):
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr08",
            signal="OrdinaryAmbientLightTweeterLeftBrightness",
            value=bright
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr08",
            signal="OrdinaryAmbientLightTweeterLeftRed",
            value=r
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr08",
            signal="OrdinaryAmbientLightTweeterLeftGreen",
            value=g
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr08",
            signal="OrdinaryAmbientLightTweeterLeftBlue",
            value=b
        )

    def check_twe_right_alm(self, bright, r, g, b):
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr07",
            signal="OrdinaryAmbientLightTweeterRightBrightness",
            value=bright
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr07",
            signal="OrdinaryAmbientLightTweeterRightRed",
            value=r
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr07",
            signal="OrdinaryAmbientLightTweeterRightGreen",
            value=g
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr07",
            signal="OrdinaryAmbientLightTweeterRightBlue",
            value=b
        )

    def check_cc_under_alm(self, bright, r, g, b):
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr0B",
            signal="OrdinaryAmbientLightCCUnderBrightness",
            value=bright
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr0B",
            signal="OrdinaryAmbientLightCCUnderRed",
            value=r
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr0B",
            signal="OrdinaryAmbientLightCCUnderGreen",
            value=g
        )
        self.check_singal(
            bus="cem_lin5",
            msg="CemCem_Lin5Fr0B",
            signal="OrdinaryAmbientLightCCUnderBlue",
            value=b
        )

    def check_mul_alms(self, bright, r, g, b, zone_lst: List[ALMZoneId]):
        for zone in zone_lst:
            if zone.value == 1:
                self.check_front_left_alm(bright, r, g, b)
            elif zone.value == 2:
                self.check_front_right_alm(bright, r, g, b)
            elif zone.value == 3:
                self.check_rear_left_alm(bright, r, g, b)
            elif zone.value == 4:
                self.check_rear_right_alm(bright, r, g, b)
            elif zone.value == 17:
                self.check_twe_left_alm(bright, r, g, b)
            elif zone.value == 18:
                self.check_twe_right_alm(bright, r, g, b)
            elif zone.value == 19:
                self.check_cc_left_alm(bright, r, g, b)
            elif zone.value == 20:
                self.check_cc_right_alm(bright, r, g, b)
            elif zone.value == 29:
                self.check_cc_mid_right_alm(bright, r, g, b)
            elif zone.value == 30:
                self.check_cc_mid_left_alm(bright, r, g, b)
            elif zone.value == 31:
                self.check_cc_under_alm(bright, r, g, b)
            else:
                logger.warning("氛围灯zoneid错误")
                
    def check_goosenecklamp(self, sts: OnOff):
        with allure.step(f"检验鹅颈灯是否为{sts.name}"):
            self.ipdu.check(self.ipdu.cem_lin3.CemCem_Lin3Fr01, "ActvnOfFlGooseneckLamp", sts.value)
            self.ipdu.check(self.ipdu.cem_lin3.CemCem_Lin3Fr01, "ActvnOfFrGooseneckLamp", sts.value)



    #o_fan.liu edit         
    def check_steerwheel_DisAdjMov_req(self, disAdjMov_req: DisAdjMov):
        with allure.step(f"Check BGM 方向盘DisAdjMov信号是否为{disAdjMov_req.name}"):
            logger.info(f"Check BGM 方向盘DisAdjMov信号是否为{disAdjMov_req.name}")
            self.check('cem_lin4', 'CemCem_Lin4Fr02', 'DisAdjMov', disAdjMov_req.value)
    
    def check_VehParkNotActvd(self, Flg1: Flg1):
        with allure.step(f"检查车辆驻车未激活状态是否为{Flg1.name}"):
            self.check('backbonefr', 'CemBackBoneFr08', 'VehParkNotActvd', Flg1.value)

    def set_epbsts_function_safe(self, sts:EpbSts = EpbSts.AllAppld, ub_flag:bool = True):
        prompt_info = f"---------->设置epb相关信号"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if sts is not None:
                logger.info(f"epb相关状态设为{sts.name}")
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', sts.value, ub_flag = ub_flag)

    def set_trsmparklockd_function_safe(self, TrsmParkLockd:TrsmParkLockd = TrsmParkLockd.ParkEngd, ub_flag:bool = True):
        prompt_info = f"---------->设置驻车锁相关信号"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if TrsmParkLockd is not None:
                logger.info(f"驻车锁状态设为{TrsmParkLockd.name}")
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', TrsmParkLockd.value, ub_flag = ub_flag)

    def set_engine_sts_function_safe(self, EngSt1WdStsEngSt1WdSts:EngSt1WdStsEngSt1WdSts = EngSt1WdStsEngSt1WdSts.EngSt1_Ini, ub_flag:bool = True):
        prompt_info = f"---------->设置发动机状态相关信号"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            if EngSt1WdStsEngSt1WdSts is not None:
                logger.info(f"发动机状态设为{EngSt1WdStsEngSt1WdSts.name}")
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', EngSt1WdStsEngSt1WdSts.value, ub_flag = ub_flag)

    def check_RemPrkgSts(self, RemPrkgSts: RemPrkgSts):
        with allure.step(f"检查远程启动状态是否为{RemPrkgSts.name}"):
            self.check('infocanfd', 'BgmInfoCanFdDevFr02', 'PrkgAssiSysRemPrkgSts', RemPrkgSts.value, 0.2)

    def check_PtActvnReq(self, PtActvnReq: PtActvnReq1):
        with allure.step(f"检查启动请求是否为{PtActvnReq.name}"):
            self.check('backbonefr', 'CemBackBoneFr25', 'PtActvnReq1WdPtActvnReq', PtActvnReq.value, 0.2)

    def check_AudWarn(self, AudWarn: bool):
        with allure.step(f"检查非P档离车音频告警是否为{AudWarn}"):
            self.check('backbonefr', 'CemBackBoneFr25', 'AudWarn', AudWarn)

    def check_ProxyKeepLow(self, usage_mode: UsageMode):
        with allure.step(f"检查请求保持的usagemode下限是否为{usage_mode.name}"):
            self.check('infocanfd', 'BgmInfoCanFdDevFr02', 'UsgModProxyKeepLow', usage_mode.value)

    def check_StartInhibitReq(self, StartInhibitReq: isOn):
        with allure.step(f"检查启动禁止请求是否为{StartInhibitReq.name}"):
            self.check('infocanfd', 'BgmInfoCanFdFr18', 'StartInhibitReq', StartInhibitReq.value) 

    def check_walk_away_and_approch_settings(self, keysettingtype:KeySettingType, 
                                             walkaway: Union[KeySettingItem, int] = None, 
                                             approch: Union[EnableDisable, int] = None, 
                                             time_wait: Union[float, int] = 0):
        if keysettingtype.name == "WalkAay":
            prompt_info = f"----------校验总线离车落锁设置项状态{walkaway.name}"
            with allure.step(prompt_info):
                logger.info(prompt_info)
                self.check("connectivitycanfd","BgmConnectivityFr18", "WalkAwayLockHmi", walkaway._value_)

        elif keysettingtype.name == "Approch":
            prompt_info = f"----------校验总线近车解锁设置项状态{approch.name}"
            with allure.step(prompt_info):
                logger.info(prompt_info)
                self.check("connectivitycanfd","BgmConnectivityFr18", "ApproachUnlockHmi", approch.value)
                
        elif keysettingtype.name == "All":
            prompt_info = f"----------校验总线离车落锁设置项状态{walkaway.name},近车解锁设置项为{approch.name}"
            with allure.step(prompt_info):
                logger.info(prompt_info)
                self.check("connectivitycanfd","BgmConnectivityFr18", "WalkAwayLockHmi", walkaway.value)
                self.check("connectivitycanfd","BgmConnectivityFr18", "ApproachUnlockHmi", walkaway.value)
                
        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)  

#zsl edit           
    def set_battery_charger_handle_status(self, soc_value: Union[int, float], ChrgHndlStrtEna: ChrgHndlStrtEna, wait_time: int = 0):
        with allure.step(f"设置高压电池SOC值为{soc_value}"):
            self.set("propulsioncan","EcmPropFr04",'DispHvBattLvlOfChrg', soc_value)
            logger.info(f"高压电池SOC值已设置为{soc_value}")

        # 等待信号上报
        logger.info(f"等待{wait_time}秒以检查ChrgSoftSwCtrlSt信号值...")
        sleep(wait_time)

        # 检查信号值
        with allure.step(f"检查ChrgSoftSwCtrlSt信号值，期望值为{ChrgHndlStrtEna}"):
            self.check("backbonefr", "IHUBackBoneFr08", 'ChrgSoftSwCtrlSt', ChrgHndlStrtEna.value)
            logger.info(f"ChrgSoftSwCtrlSt信号值检查通过，期望值为{ChrgHndlStrtEna}")
            
    def check_handle_status(self, ChrgSoftSwCtrlSt: ChrgSoftSwCtrlSt):
        # 检查信号值
        with allure.step(f"检查ChrgSoftSwCtrlSt信号值，期望值为{ChrgSoftSwCtrlSt}"):
            self.check("backbonefr", "IHUBackBoneFr08", 'ChrgSoftSwCtrlSt', ChrgSoftSwCtrlSt.value)
            logger.info(f"ChrgSoftSwCtrlSt信号值检查通过，期望值为{ChrgSoftSwCtrlSt}")

    def check_static_lighting_mode_en(self, static_lighting_mode_en: StaticLightingModeEn):
        # Check the signal value of StaticLightingModeEn
        with allure.step(f"Check StaticLightingModeEn signal, expected value is {static_lighting_mode_en.value}"):
            self.check("bodyexposedcanfd", "BgmBodyExposedCANFr10", 'StaticLightingModeEn', static_lighting_mode_en.value)
            logger.info(f"StaticLightingModeEn signal check passed, expected value is {static_lighting_mode_en.value}")

    def check_ExtrLtgStsStaticLtgShow(self, ExtrLtgStsStaticLtgShow: ExtrLtgStsStaticLtgShow):
        expected_value = ExtrLtgStsStaticLtgShow.value
        # Check the signal value of StaticLightingModeEn
        with allure.step(f"Check ExtrLtgStsStaticLtgShow signal, expected value is {expected_value}"):
            self.check("backbonefr", "CemBackBoneFr02", "ExtrLtgStsStaticLtgShow", expected_value)
            # 可以在需要时启用以下日志记录，例如调试时
            # logger.info(f"ExtrLtgStsStaticLtgShow signal check passed, expected value is {expected_value}")

    def set_JiDUCharging(self, isDConnect: bool=False,isAConnect: bool=False, isPrivate: bool=True):
        if isDConnect:
            self.set('backbonefr', 'VddmBackBoneFr29', 'DCChrgnHndlSts', 1)
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1)   
        else:
            self.set('backbonefr', 'VddmBackBoneFr29', 'DCChrgnHndlSts', 0)
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        if isAConnect:
            self.set('propulsioncan', 'CddObcPropFr01', 'OnBdChrgrHndlSts1', 3)   
        else:
            self.set('propulsioncan', 'CddObcPropFr01', 'OnBdChrgrHndlSts1', 0)    
        if isPrivate:
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr02, 'JIDUChgrFlg', 2)
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmBsrmConnectivityFr03, 'ChrgrPileInfo', 1)
        else:
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr02, 'JIDUChgrFlg', 3)
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmBsrmConnectivityFr03, 'ChrgrPileInfo', 0)    
        time.sleep(0.5)

    def set_BookCharge_SetResponse(self, BookChargeSetResponse: BookChargeSetResponse):
        expected_value = BookChargeSetResponse.value
        with allure.step(f"set BookChargeSetResponse signal, expected value is {expected_value}"):
            self.set("propulsioncan","EcmPropFr11",'BookChargeSetResponse', expected_value)

    def check_BookChrgnActvdReq_set_BookChrgnStsFb(self, BookChrgnActvdReq, BookChrgnStsFb):
        with allure.step(f"监测 BookChrgnActvdReq: signal, expected value is BookChrgnActvdReq"):
            self.check_singal("backbonefr","VgmBackBoneFr15",'BookChrgnActvdReq',BookChrgnActvdReq,timeout=300)
        with allure.step(f"设置 BookChrgnStsFb: signal, expected value is BookChrgnStsFb"): 
            self.set_singal("chassiscan2","EcmChas2Fr32",'BookChrgnStsFb',BookChrgnStsFb)

    def check_AI_Inter_actionLamp_Sts(self, AIInteractionLampLeftY, AIInteractionLampRightY):
        with allure.step(f"监测 AI左测指示灯: signal, expected value is AIInteractionLampRightY"):
            self.check_singal("cem_lin2","CemCem_Lin2Fr08",'AIInteractionLampRightY4',AIInteractionLampRightY[0])
            self.check_singal("cem_lin2","CemCem_Lin2Fr08",'AIInteractionLampRightY3',AIInteractionLampRightY[1])
            self.check_singal("cem_lin2","CemCem_Lin2Fr08",'AIInteractionLampRightY2',AIInteractionLampRightY[2])
            self.check_singal("cem_lin2","CemCem_Lin2Fr08",'AIInteractionLampRightY1',AIInteractionLampRightY[3])
        with allure.step(f"监测 AI右测指示灯: signal, expected value is AIInteractionLampLeftY"):
            self.check_singal("cem_lin2","CemCem_Lin2Fr07",'AIInteractionLampLeftY4',AIInteractionLampLeftY[0])
            self.check_singal("cem_lin2","CemCem_Lin2Fr07",'AIInteractionLampLeftY3',AIInteractionLampLeftY[1])
            self.check_singal("cem_lin2","CemCem_Lin2Fr07",'AIInteractionLampLeftY2',AIInteractionLampLeftY[2])
            self.check_singal("cem_lin2","CemCem_Lin2Fr07",'AIInteractionLampLeftY1',AIInteractionLampLeftY[3])

    def set_WPCModuleSts(self, sts: WPCModuleSts = WPCModuleSts.Standby):
        with allure.step(f"设置主驾无线充电状态为{sts.name}"):
            self.set_singal(
                bus="ConnectivityCANFD", msg="WpcConnFr02", signal="WPCModuleSts", value=sts.value
            )

    def set_WPCCtrlRes(self, res: WPCCtrlRes = WPCCtrlRes.enabled):
        with allure.step(f"设置主驾无线充电结果为{res.name}"):
            self.set_singal(
                bus="ConnectivityCANFD", msg="WpcConnFr02", signal="WPCCtrlRes", value=res.value
            )

    def set_PhoneForgottenRmn(self, sts: OnOff = OnOff.Off):
        with allure.step(f"设置主驾手机遗忘状态为{sts.name}"):
            self.set_singal(
                bus="ConnectivityCANFD", msg="WpcConnFr02", signal="PhoneForgottenRmn", value=sts.value
            )

    def set_WPCFailureSts(self, sts: WPCFailureSts = WPCFailureSts.NoFailure):
        with allure.step(f"设置主驾无线充电故障状态为{sts.name}"):
            self.set_singal(
                bus="ConnectivityCANFD", msg="WpcConnFr02", signal="WPCFailureSts", value=sts.value
            )

    def set_WPCModuleStsPass(self, sts: WPCModuleSts = WPCModuleSts.Standby):
        with allure.step(f"设置副驾无线充电状态为{sts.name}"):
            self.set_singal(
                bus="ConnectivityCANFD", msg="Wpc3ConnFr01", signal="WPCModuleStsPass", value=sts.value
            )

    def set_WPCCtrlResPass(self, res: WPCCtrlRes = WPCCtrlRes.enabled):
        with allure.step(f"设置主驾无线充电结果为{res.name}"):
            self.set_singal(
                bus="ConnectivityCANFD", msg="Wpc3ConnFr01", signal="WPCCtrlResPass", value=res.value
            )

    def set_PhoneForgottenRmnPass(self, sts: OnOff = OnOff.Off):
        with allure.step(f"设置副驾 手机遗忘状态为{sts.name}"):
            self.set_singal(
                bus="ConnectivityCANFD", msg="Wpc3ConnFr01", signal="PhoneForgottenRmnPass", value=sts.value
            )

    def set_WPCFailureStsPass(self, sts: WPCFailureSts = WPCFailureSts.NoFailure):
        with allure.step(f"设置副驾无线充电故障状态为{sts.name}"):
            self.set_singal(
                bus="ConnectivityCANFD", msg="Wpc3ConnFr01", signal="WPCFailureStsPass", value=sts.value
            )

    def check_wireless_charge_drv(self, sts: OnOff):
        with allure.step(f"检测主驾无线充电状态是否为{sts.name}"):
            self.check_singal(
                "ConnectivityCANFD", "BgmConnectivityFr08", "WirelschrgActvReqFromHmi", sts.value
            )

    def check_wireless_charge_pass(self, sts: OnOff):
        with allure.step(f"检测副驾无线充电状态是否为{sts.name}"):
            self.check_singal(
                "ConnectivityCANFD", "BgmConnectivityFr08", "WirelschrgActvReqFromHmiPass", sts.value
            )
            
    def check_DiagcComActv_sts(self, sts: OnOff,check_time = 1):
        self.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", sts.value,check_time=check_time)

    def set_wiper_lever_status(self,value=0):
        if value == 0:
            with allure.step(f"设置雨刮拨杆信号状态为释放 LeverSwtLeLvrSwt3 信号值为： {value}"):
                self.ipdu.set(self.ipdu.bodycan.StleBodyFr01,'LeverSwtLeLvrSwt3',value)
        elif value == 1:
            with allure.step(f"设置雨刮拨杆短按信号状态为单刮 LeverSwtLeLvrSwt3 信号值为： {value}"):
                self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3',value)
        elif value == 2:
            with allure.step(f"设置雨刮拨杆长按信号状态为洗涤 LeverSwtLeLvrSwt3 信号值为： {value}"):
                self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3',value)

        elif value == 3:
            with allure.step(f"设置雨刮拨杆故障 LeverSwtLeLvrSwt3 信号值为： {value}"):
                self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt3',value)
        else:
            with allure.step(f"传入了不存在的 LeverSwtLeLvrSwt3 信号值为： {value}"):
                pass
                
    
    def check_single_wiper_status(self,value=0):
        if value == 1:
            with allure.step(f"当前收到单刮信号反馈 WiprMotFrntLvrCmdSafeLvrInSnglStrokePos 信号值为： {value}"):
                self.ipdu.check(self.ipdu.cem_lin1.CemCem_Lin1Fr01,"WiprMotFrntLvrCmdSafeLvrInSnglStrokePos",value)
        else:
            with allure.step(f"当前未收到单刮信号反馈 WiprMotFrntLvrCmdSafeLvrInSnglStrokePos 信号值为： {value}"):
                self.ipdu.check(self.ipdu.cem_lin1.CemCem_Lin1Fr01,"WiprMotFrntLvrCmdSafeLvrInSnglStrokePos",value)

    def check_wiper_wash_active_status(self,value=1):
        if value == 2:
            with allure.step(f"当前收到雨刮洗涤激活反馈 ActvnOfWshrFrntSafe 信号值为： {value}"):
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr71,"ActvnOfWshrFrntSafe",value)
        else:
            with allure.step(f"当前未收到雨刮洗涤激活反馈 ActvnOfWshrFrntSafe 信号值为： {value}"):
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr71,"ActvnOfWshrFrntSafe",value)
                
    def set_BookChargingTime_Bluetooth(self, startTime_hour, startTime_min, stopTime_hour, stopTime_min, sleeptime=1):
        '''预约充电时间 蓝牙 开始和结束时间 '''
        self.set_singal("propulsioncan","BecmPropFr32",'BthBookStrtTiChrgnTmrChrgnTmrhour', startTime_hour)
        self.set_singal("propulsioncan","BecmPropFr32",'BthBookStrtTiChrgnTmrChrgnTmrmin', startTime_min)
        self.set_singal("propulsioncan","BecmPropFr32",'BthBookStopTiChrgnTmrChrgnTmrhour', stopTime_hour)
        self.set_singal("propulsioncan","BecmPropFr32",'BthBookStopTiChrgnTmrChrgnTmrmin', stopTime_min)
        sleep(sleeptime)

    def set_BookChargingTime_Remote(self, startTime_hour, startTime_min, stopTime_hour, stopTime_min, sleeptime=1):
        '''预约充电时间 远控 开始和结束时间 '''
        self.set_singal("propulsioncan","BecmPropFr33",'RemoteBookStrtTiChrgnTmrChrgnTmrhour', startTime_hour)
        self.set_singal("propulsioncan","BecmPropFr33",'RemoteBookStrtTiChrgnTmrChrgnTmrmin', startTime_min)
        self.set_singal("propulsioncan","BecmPropFr33",'RemoteBookStopTiChrgnTmrChrgnTmrhour', stopTime_hour)
        self.set_singal("propulsioncan","BecmPropFr33",'RemoteBookStopTiChrgnTmrChrgnTmrmin', stopTime_min)
        sleep(sleeptime)

    def set_JIDUChgrFlg_sts(self, JIDUChgrFlg):
        '''设置充电桩标识 JIDUChgrFlg'''
        self.set_singal("propulsioncan","BecmPropFr02",'JIDUChgrFlg', JIDUChgrFlg)

    def set_BookChrgnStsFb(self, BookChrgnStsFb):
        '''设置预约充电反馈状态'''  
        with allure.step(f"设置 BookChrgnStsFb: signal, expected value is BookChrgnStsFb"): 
            self.set_singal("chassiscan2","EcmChas2Fr32",'BookChrgnStsFb',BookChrgnStsFb)

    def check_BookStopTiAchieved_set_BookChrgnStsFb(self,BookStopTiAchieved, BookChrgnStsFb,timeout=300):
        '''检测充电停止请求，回复充电停止'''
        with allure.step(f"监测 BookStopTiAchieved: signal, expected value is BookStopTiAchieved"):
            self.check_singal("backbonefr","VgmBackBoneFr15",'BookStopTiAchieved',BookStopTiAchieved,timeout=timeout)
        with allure.step(f"设置 BookChrgnStsFb: signal, expected value is BookChrgnStsFb"): 
            self.set_singal("chassiscan2","EcmChas2Fr32",'BookChrgnStsFb',BookChrgnStsFb)

    def check_singal_ub(self,bus: str,msg: str,signal: str,value: Union[str, int, float],timeout:Union[int,float] = 5,do_assert = True,check_time = 1,check_ub=None):
        prompt_info = f"---------->检测{bus}:{msg}:{signal}的值是否为：{value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            bus = str.lower(bus)
            self.check(bus_name=bus,msg_name=msg,signal_name=signal,sig_value_name=value,timeout=timeout,do_assert=do_assert,check_time=check_time,check_ub=check_ub)

    def check_ResvSupChrgThermSwt_sts(self,ResvSupChrgThermSwt, check_ub):
        '''检测SOC统一标定'''
        with allure.step(f"监测 ResvSupChrgThermSwt: signal, expected value is ResvSupChrgThermSwt"):
            self.check_singal_ub("propulsioncan","VcuPropFr02", 'ResvSupChrgThermSwt', ResvSupChrgThermSwt,check_ub=check_ub)

    def check_V2XDchaSwt_sts(self,V2XDchaSwt):
        '''检测放电请求'''
        with allure.step(f"监测 ResvSupChrgThermSwt: signal, expected value is ResvSupChrgThermSwt"):
            self.check_singal("backbonefr","IHUBackBoneFr07", 'V2XDchaSwt', V2XDchaSwt, timeout=0.5)
            
    def set_fota_Discharging(self, isDischarging: bool=False):
        if isDischarging:
            self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 7)  
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 8) #8为放电
        else:
            self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 7)  
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) #非8为不放电
        time.sleep(0.5)
    
    def set_AmbTEstimd_and_qf(self, AmbTEstimd: Union[int, float] = 0.0, qf: HvacTIfQf =HvacTIfQf.SnsrDataOk):
        with allure.step(f"设置环境温度为 {AmbTEstimd} degC, qf为{qf.name}"):
            self.set('bodycan', 'CcmBodyFr28', 'AmbTEstimdAmbTEstimd', AmbTEstimd)
            self.set('bodycan', 'CcmBodyFr28', 'AmbTEstimdQf', qf.value)
            logger.info(f"设置环境温度为 {AmbTEstimd} degC, qf为{qf.name}")
    
    def check_DrvrStrtReq(self, StrtReq: StrtReq):
        with allure.step(f"检查驾驶请求是否为{StrtReq.name}"):
            self.check('infocanfd', 'BgmInfoCanFdDevFr02', 'DrvrStrtReq', StrtReq.value, 0.2)

    def check_can_lin_diag_req_and_send_resp(self,bus_name:BusName,req_id:int,resp_id:int,check_req_data:list=[],send_resp_data:list=[],check_len:Union[int,None] = None ):
        if check_len == None:
            diag_request = self.recv_diag_request_msg(bus_name=bus_name.value,request_id=req_id,response_id=resp_id)[0]
        else:
            diag_request = self.recv_diag_request_msg(bus_name=bus_name.value,request_id=req_id,response_id=resp_id)[0][:check_len]

        logger.info(f"----------> received diag_request is {diag_request}")

        if diag_request == check_req_data:
            logger.info(f"----------> received diag_request same to expected data:{check_req_data}")
            logger.info(f"----------> send diagnostic response {send_resp_data}")
            self.send_diag_request_msg(bus_name=bus_name.value,request_id=resp_id,response_id=req_id,send_msg=send_resp_data)
        else:
            logger.info(f"----------> diag_request is not {check_req_data}")
            assert False
        
        
    def check_TotDstTrvldHiResl_value(self,TotDstTrvldHiResl):
        '''检测BGM里程TotDstTrvldHiResl/m'''
        with allure.step(f"监测 TotDstTrvldHiResl: signal, expected value is TotDstTrvldHiResl"):
            self.check_singal("backbonefr","CemBackBoneFr10", 'TotDstTrvldHiResl', TotDstTrvldHiResl, timeout=0.5)

    def check_BkpOfDstTrvld_value(self,BkpOfDstTrvld):
        '''检测BGM里程BkpOfDstTrvld/km'''
        with allure.step(f"监测 BkpOfDstTrvld: signal, expected value is BkpOfDstTrvld"):
            self.check_singal("backbonefr","DimBackBoneFr04", 'BkpOfDstTrvld', BkpOfDstTrvld, timeout=0.5)

    def get_TotDstTrvldHiResl_value(self):
        '''获取BGM里程TotDstTrvldHiResl/m'''
        expectedvalue = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr10,'TotDstTrvldHiResl')
        logger.info("获取BGM里程TotDstTrvldHiResl/m为: expectedvalue {}".format(expectedvalue))
        return expectedvalue

    def get_BkpOfDstTrvld_value(self):
        '''获取BGM里程BkpOfDstTrvld/km'''
        expectedvalue = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.DimBackBoneFr04,'BkpOfDstTrvld')
        logger.info("获取BGM里程BkpOfDstTrvld/km为: expectedvalue {}".format(expectedvalue))
        return expectedvalue
    def check_afs_act(self,actn_sts: isOn):
        promt_info = f"----------------> Check 自适应前照明系统的状态是否ActvnOfDbl:{actn_sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.check(self.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActvnOfDbl', actn_sts.value)

    def set_trun_beam_pull_up_down(self,gear:TurnPressGear):
        promt_info = f"----------------> 设置转向灯拨杆拨动状态为:{gear.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', gear.value)
            sleep(.3)
            self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeTurnLightSwt1', 0)

    def set_high_beam_pull_in_out(self,gear:HighPressGear,pull_time: Union[float, int] = 0):
        promt_info = f"----------------> 设置远光灯拨杆拨动状态为:{gear.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            if gear.name == "PressOutd":
                self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 0)
                sleep(.5)
                self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 2)
                sleep(.5)
                self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 0)
                sleep(.5)
            if gear.name == "PressInsd":
                self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 0)
                sleep(.5)
                self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 1)
                sleep(pull_time)
            else:
                self.ipdu.set(self.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', gear.value)
                
    def check_flash_lamp_always_on(self,last_time:Union[float,int]=2):
        promt_info = f"---------------->Check 远光灯闪灯是否处于常亮状态"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.check_signal_thread_start("backbonefr","CemBackBoneFr02", "ExtrLtgStsFlash", timeout = last_time)
            self.check_signal_thread_start("bodyexposedcanfd", "CemBodyExpoFr50", 'ActnOfLedHiBeam', timeout = last_time)
            sleep(last_time)
            result_ori_flash = self.check_signal_thread_stop("ExtrLtgStsFlash")
            result_ori_act = self.check_signal_thread_stop("ActnOfLedHiBeam")
            logger.info(f"result_ori_flash:{result_ori_flash},result_ori_act:{result_ori_act}")

            if check_all_value_is(result_ori_flash, 1) and check_all_value_is(result_ori_act, 1):
                assert True
            else:
                logger.info("不是所有的值都是1")
                assert False

    def check_tailgate_lock_status(self,sterm_lock:LockSts2, time_wait: Union[float, int] = 0):
        promt_info = f"----------------> 校验总线尾门锁状态为:{sterm_lock.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, 'TrLockSts', sterm_lock.value)

        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)
        
    def check_SetClsChargeLidTiSts_value(self,SetClsChargeLidTiSts):
        '''充电口盖自动关闭时间SetClsChargeLidTiSts'''
        with allure.step(f"监测 SetClsChargeLidTiSts: signal, expected value is SetClsChargeLidTiSts"):
            self.check_singal("infocanfd","BgmInfoCanFdDevFr02", 'SetClsChargeLidTiSts', SetClsChargeLidTiSts, timeout=0.5)

    def check_chrgild_req_not(self,timeout=30.0 ):
        promt_info = f"--->Check BGM 发出的控制充电口盖请求是否为127"
        with allure.step(promt_info):
            logger.info(promt_info)
            U2 = self.ipdu.get_recent_signal_raw_value(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2',timeout)
            logger.info("BGM电压检测: VehBattUSysU {}".format(U2))
            if U2 ==127:
                logger.info("充电口盖请求为默认值")
                pass
            else:
                logger.info("充电口盖请求不为默认值")
                assert False,"充电口盖请求不为默认值"

    def check_without_chrglid_req(self, req: Union[int, None] = None, timeout=30.0):  
        with allure.step(f"Check 30s内总线充电口盖开关请求状态为{req}"):
            logger.info(f"Check 30s内总线充电口盖开关请求状态为{req}")
            ori_data = self.ipdu.check_signal(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', timeout)
            logger.info(f"获取{timeout}秒内的ChrgLidManvgDCorAcDcReq2原始数据是:{ori_data}")
            check_result = check_all_value_is(ori_data, req)
            logger.info(f"Check 结果是：{check_result}")
            assert check_result

    def check_ChrgLidDCorAcDctSwt_Req(self,Req):
        '''充电口盖开关请求ChrgLidDCorAcDctSwtReq'''
        with allure.step(f"监测 ChrgLidDCorAcDctSwtReq: signal, expected value is ChrgLidDCorAcDctSwtReq"):
            self.check_singal("backbonefr","CemBackBoneFr38", 'ChrgLidDCorAcDctSwtReq', Req, timeout=0.5)    
            
    def check_climate_eco_sts(self, sts: OnOff):
        promt_info = f"---------------->开始查看空调ECO状态信号bodycan:CemBodyFr48:HMIClimaEgySaveReq是否为{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.check("bodycan", "CemBodyFr48", 'HMIClimaEgySaveReq', sts.value)
            
    def set_windows_stauts_signal(self,status:WindowSwitchStatus):
        promt_info = f"----------------> 设置窗户状态:{status.value}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'WinSwtReqFrntLe',status.value)
            
    def set_windows_pass_stauts_signal(self,status:WindowSwitchStatus):
        promt_info = f"----------------> 设置副驾窗户状态:{status.value}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'WinSwtReqFrntRi',status.value)
    
    def set_windows_ReLe_stauts_signal(self,status:WindowSwitchStatus):
        promt_info = f"----------------> 设置左后窗户状态:{status.value}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'WinSwtReqReLe',status.value)

    def set_windows_ReRi_stauts_signal(self,status:WindowSwitchStatus):
        promt_info = f"----------------> 设置右后窗户状态:{status.value}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'WinSwtReqReRi',status.value)

    def set_windows_PDM_pass_stauts_signal(self,status:WindowSwitchStatus):
        promt_info = f"----------------> 设置PDM 副驾窗户状态:{status.value}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinSwtStsAtPass',status.value)

    def set_windows_RLDM_Rele_stauts_signal(self,status:WindowSwitchStatus):
        promt_info = f"----------------> 设置RLDM 左后窗户状态:{status.value}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02,'WinSwtStsAtReLe',status.value)

    def set_windows_RRDM_ReRi_stauts_signal(self,status:WindowSwitchStatus):
        promt_info = f"----------------> 设置RRDM 右后窗户状态:{status.value}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02,'WinSwtStsAtReRi',status.value)

    def set_rcw_req(self,req:RcwReq):
        prompt_info = f"---------->设置后碰撞预警(RCW){req.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr13, 'RcwmLiReq', req.value)
            
    def set_battTraw(self, BattTRaw: int):
        with allure.step(f"设置电池温度"):
            # batturaw1 = (BattURaw - 5) * 40
            #self.set('cem_lin6', 'BmsCem_Lin6Fr05', 'BattURaw', batturaw1)
            self.set('cem_lin6', 'BmsCem_Lin6Fr03', 'BattTRaw', BattTRaw)
            logger.info(f"设置电池温度成功,设置的电池温度为{BattTRaw}V")
    

    def check_without_tailgate_action_req(self,timeout=3):
        prompt_info = f"---------->Check BGM 没有发出尾门控制相关请求"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_signal_always_is("bodycan","CemBodyFr02","TrOpenerReqTrOpenerReq",0,timeout)


    def check_signal_always_is(self,bus:str,msg:str,signal:str,value:Union[int,float],timeout = 3):
        prompt_info = f"---------->Check 总线{bus}->{msg}->{signal}在{timeout}s 内发送值都为{value}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            bus_obj = getattr(self.ipdu, bus)
            msg_signals_obj = getattr(bus_obj, msg)
            ori_data = self.ipdu.check_signal(msg_signals_obj, signal, timeout)
            logger.info(f"获取{timeout}秒内的{signal}原始数据是:{ori_data}")
            check_result = check_all_value_is(ori_data, value)
            logger.info(f"Check 结果是：{check_result}")
            assert check_result

    def set_hzrdLiIndcn_req(self,req:YesOrNo):
        prompt_info = f"---------->设置HzrdLiIndcnReq请求{req.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr39, 'HzrdLiIndcnReq', req.value)
            
    def check_tweeter_sts(self, sts: TweeterSts):
        promt_info = f"---------------->Check 扬声器状态是否为{sts.name}"
        with allure.step(promt_info):
            logger.info(promt_info)
            self.ipdu.check(self.ipdu.cem_lin4.CemCem_Lin4Fr02, 'RiseOrFallControl', sts.value)

    def check_ignition_state(self, sts: OnOffSafe1, time_wait: Union[float, int] = 0):
        prompt_info = f"----------通过总线校验控制点火继电器信号的状态为{sts.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.set("infocanfd","BgmInfoCanFdFr18", "IgnRlyCmdActr", sts.value)

        logger.info(f"--------->等待{time_wait}")
        sleep(time_wait)  
    def set_door_warning_ThermalProtection_sts(self,
                             Drvr: Union[bool, None] = None,
                             Pass: Union[bool, None] = None,
                             LeRe: Union[bool, None] = None,
                             RiRe: Union[bool, None] = None
                             ):
        if Drvr is not None:
            with allure.step(f'设置主驾门热保护故障状态为：{Drvr}'):
                logger.info(f'设置主驾门热保护故障状态为：{Drvr}')
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DtcInfDoorDrvrBoolean1', Drvr)
        if Pass is not None:
            with allure.step(f'设置副驾门热保护故障状态为：{Pass}'):
                logger.info(f'设置副驾门热保护故障状态为：{Pass}')
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DtcInfDoorPassBoolean1', Pass)
        if LeRe is not None:
            with allure.step(f'设置左后门热保护故障状态为：{LeRe}'):
                logger.info(f'设置左后门热保护故障状态为：{LeRe}')
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DtcInfDoorLeReBoolean1', LeRe)
        if RiRe is not None:
            with allure.step(f'设置右后门热保护故障状态为：{RiRe}'):
                logger.info(f'设置右后门热保护故障状态为：{RiRe}')
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DtcInfDoorRiReBoolean1', RiRe)

    def set_door_warning_FaultPlayProtectionActive_sts(self,
                             Drvr: Union[bool, None] = None,
                             Pass: Union[bool, None] = None,
                             LeRe: Union[bool, None] = None,
                             RiRe: Union[bool, None] = None
                             ):
        if Drvr is not None:
            with allure.step(f'设置主驾门防玩激活故障状态为：{Drvr}'):
                logger.info(f'设置主驾门防玩激活故障状态为：{Drvr}')
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DtcInfDoorDrvrBoolean2', Drvr)
        if Pass is not None:
            with allure.step(f'设置副驾门防玩激活故障状态为：{Pass}'):
                logger.info(f'设置副驾门防玩激活故障状态为：{Pass}')
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DtcInfDoorPassBoolean2', Pass)
        if LeRe is not None:
            with allure.step(f'设置左后门防玩激活故障状态为：{LeRe}'):
                logger.info(f'设置左后门防玩激活故障状态为：{LeRe}')
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DtcInfDoorLeReBoolean2', LeRe)
        if RiRe is not None:
            with allure.step(f'设置右后门防玩激活故障状态为：{RiRe}'):
                logger.info(f'设置右后门防玩激活故障状态为：{RiRe}')
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DtcInfDoorRiReBoolean2', RiRe)

    def set_door_warning_RollAngleAbnormal_sts(self,
                             Drvr: Union[bool, None] = None,
                             Pass: Union[bool, None] = None,
                             LeRe: Union[bool, None] = None,
                             RiRe: Union[bool, None] = None
                             ):
        if Drvr is not None:
            with allure.step(f'设置主驾门车辆横摆角度不正常故障状态为：{Drvr}'):
                logger.info(f'设置主驾门车辆横摆角度不正常故障状态为：{Drvr}')
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DtcInfDoorDrvrBoolean3', Drvr)
        if Pass is not None:
            with allure.step(f'设置副驾门车辆横摆角度不正常故障状态为：{Pass}'):
                logger.info(f'设置副驾门车辆横摆角度不正常故障状态为：{Pass}')
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DtcInfDoorPassBoolean3', Pass)
        if LeRe is not None:
            with allure.step(f'设置左后门车辆横摆角度不正常故障状态为：{LeRe}'):
                logger.info(f'设置左后门车辆横摆角度不正常故障状态为：{LeRe}')
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DtcInfDoorLeReBoolean3', LeRe)
        if RiRe is not None:
            with allure.step(f'设置右后门车辆横摆角度不正常故障状态为：{RiRe}'):
                logger.info(f'设置右后门车辆横摆角度不正常故障状态为：{RiRe}')
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DtcInfDoorRiReBoolean3', RiRe)

    def set_door_warning_RoadInclinationAbnormal_sts(self,
                             Drvr: Union[bool, None] = None,
                             Pass: Union[bool, None] = None,
                             LeRe: Union[bool, None] = None,
                             RiRe: Union[bool, None] = None
                             ):
        if Drvr is not None:
            with allure.step(f'设置主驾门道路倾斜角度不正常故障状态为：{Drvr}'):
                logger.info(f'设置主驾门道路倾斜角度不正常故障状态为：{Drvr}')
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DtcInfDoorDrvrBoolean4', Drvr)
        if Pass is not None:
            with allure.step(f'设置副驾门道路倾斜角度不正常故障状态为：{Pass}'):
                logger.info(f'设置副驾门道路倾斜角度不正常故障状态为：{Pass}')
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DtcInfDoorPassBoolean4', Pass)
        if LeRe is not None:
            with allure.step(f'设置左后门道路倾斜角度不正常故障状态为：{LeRe}'):
                logger.info(f'设置左后门道路倾斜角度不正常故障状态为：{LeRe}')
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DtcInfDoorLeReBoolean4', LeRe)
        if RiRe is not None:
            with allure.step(f'设置右后门道路倾斜角度不正常故障状态为：{RiRe}'):
                logger.info(f'设置右后门道路倾斜角度不正常故障状态为：{RiRe}')
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DtcInfDoorRiReBoolean4', RiRe)

    def set_door_warning_HallSensorsError_sts(self,
                             Drvr: Union[bool, None] = None,
                             Pass: Union[bool, None] = None,
                             LeRe: Union[bool, None] = None,
                             RiRe: Union[bool, None] = None
                             ):
        if Drvr is not None:
            with allure.step(f'设置主驾门霍尔传感器故障故障状态为：{Drvr}'):
                logger.info(f'设置主驾门霍尔传感器故障故障状态为：{Drvr}')
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DtcInfDoorDrvrBoolean5', Drvr)
        if Pass is not None:
            with allure.step(f'设置副驾门霍尔传感器故障故障状态为：{Pass}'):
                logger.info(f'设置副驾门霍尔传感器故障故障状态为：{Pass}')
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DtcInfDoorPassBoolean5', Pass)
        if LeRe is not None:
            with allure.step(f'设置左后门霍尔传感器故障故障状态为：{LeRe}'):
                logger.info(f'设置左后门霍尔传感器故障故障状态为：{LeRe}')
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DtcInfDoorLeReBoolean5', LeRe)
        if RiRe is not None:
            with allure.step(f'设置右后门霍尔传感器故障故障状态为：{RiRe}'):
                logger.info(f'设置右后门霍尔传感器故障故障状态为：{RiRe}')
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DtcInfDoorRiReBoolean5', RiRe)

    def check_power_outlet_relay_proxy_req(self, proxy_req: PowerOutLetReq):
        prompt_info = f"----------通过总线校验12V电源服务请求闭合状态为{proxy_req.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_singal("infocanfd","BgmInfoCanFdFr21", "RlyPwrCmdProxyReq", proxy_req.value) 

    def check_battery_save_prxy_req(self, battery_save: OnOff1):
        prompt_info = f"----------通过总线校验节电继电器闭合状态为{battery_save.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.check_singal("infocanfd","BgmInfoCanFdFr21", "BattSaveRlyProxyReq", battery_save.value)

 #o_fan.liu edit             
    def set_tailgate_AntiPinch_sts(self, AntiPinch: bool):    
        with allure.step(f"设置尾门防夹状态为{AntiPinch}"):
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, "TrAntiPnch", AntiPinch)
            logger.info(f"设置尾门防夹状态为{AntiPinch}")

       
    def check_tailgate_Position(self, Position: int):
        with allure.step(f"检查尾门开度是否为{Position}"):
            self.check('bodycan', 'CemBodyFr131', 'TrOpenPosnReqFromHmi', Position)
            logger.info(f"检查尾门开度是否为{Position}")
            
    #o_fan.liu edit             
    def set_tailgate_TrOpenPosn(self, TrOpenPosn: int):    
        with allure.step(f"设置尾门当前位置为{TrOpenPosn}"):
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr03, "TrOpenPosn", TrOpenPosn)
            logger.info(f"设置尾门当前位置为{TrOpenPosn}")

    def set_crash_proxy_req(self, crash_proxy: OnOff1):
        prompt_info = f"----------通过总线设置Crash继电器Proxy请求状态为{crash_proxy.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.set_singal("backbonefr","VddmBackBoneFr00", "RlyCrashForHvsysReq", crash_proxy.value)

    def set_steer_wheel_button_status(self, steer_wheel_button_type: SteerWheelButtonType, steer_wheel_button_status: SteerWheelButtonSts):
        prompt_info = f"----------通过总线设置方向盘按键{steer_wheel_button_type.name}状态为{steer_wheel_button_status.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.set_singal("bodycan", "SwtlBodyFr01", steer_wheel_button_type.name, steer_wheel_button_status.value)

    def set_windows_button_status(self, windows_button_type: WindowsButtonType, windows_button_status: WindowsButtonSts):
        prompt_info = f"----------通过总线设置车窗按键{windows_button_type.name}状态为{windows_button_status.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            msg = None
            if windows_button_type.name in [
                WindowsButtonType.WinSwtReqReLe.name,
                WindowsButtonType.WinSwtReqReRi.name,
                WindowsButtonType.WinSwtReqFrntLe.name,
                WindowsButtonType.WinSwtReqFrntRi.name
            ]:
                msg = "DdmBodyFr07"
            if windows_button_type.name in [
                WindowsButtonType.WinSwtStsAtPass,
                WindowsButtonType.WinSwtStsAtRele,
                WindowsButtonType.WinSwtStsAtReRi
            ]:
                msg = "PdmBodyFr01"
            self.set_singal("bodycan", msg, windows_button_type.name, windows_button_status.value)

    def set_clima_proxy_req(self, clima_proxy: OnOff1):
        prompt_info = f"----------通过总线设置Clima继电器Proxy请求状态为{clima_proxy.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.set_singal("bodycan","CcmBodyFr08", "RlyCrashForClimaReq", clima_proxy.value)

    def set_relay_control_proxy_req(self, proxy_req: OnOff1):
        prompt_info = f"----------设置所有继电器服务请求闭合状态为{proxy_req.name}"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            self.set_singal("bodycan","CcmBodyFr08", "RlyCrashForClimaReq", proxy_req.value)
            self.set_singal("backbonefr","VddmBackBoneFr00", "RlyCrashForHvsysReq", proxy_req.value)
            self.set_singal("adcanfd","BgmADCANFDFr13", 'LidarPowerReq',proxy_req.value)