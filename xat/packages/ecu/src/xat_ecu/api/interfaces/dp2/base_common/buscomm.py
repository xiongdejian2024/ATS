#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :buscomm.py
@Time         :2023/12/26 10:00
@Author       :quan.sun@jiduauto.com
@Description  :整车通信能力实现接口
"""
from typing import Union, List, Tuple

from xat_ecu import reporting as allure
from xat_ecu.legacy.common.logger import logger
from xat_ecu.api.interfaces.dp2.interface import CommonBusComm
from xat_ecu.api.constants.common import BusName, NMMsgId, BGMPNC, TCAMPNC, FrameType, NMSts


class BusComm(CommonBusComm):
    def set(self,
            bus_name: str,
            msg_name: str,
            signal_name: str,
            sig_value_name: Union[str, int, float],
            ub_flag=True,
            cycle_time=None):
        bus_obj = getattr(self.ipdu, bus_name)
        msg_signals_obj = getattr(bus_obj, msg_name)
        return self.ipdu.set(msg_signals_obj, signal_name, sig_value_name, ub_flag=ub_flag, cycle_time=cycle_time)

    def check(self,
              bus_name: str,
              msg_name: str,
              signal_name: str,
              sig_value_name: Union[str, int],
              timeout: Union[float, int] = 5,
              do_assert=True,
              check_time=1):
        bus_obj = getattr(self.ipdu, bus_name)
        msg_signals_obj = getattr(bus_obj, msg_name)
        return self.ipdu.check(msg_signals_obj,
                               signal_name,
                               sig_value_name,
                               timeout,
                               do_assert=do_assert,
                               check_time=check_time)

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

    def recv_pdu_d(self, bus_name, msg_id: Union[str, int], tosun_tc1018, bus_chn, timeout=5):
        """
        目前适配了同星的 can和fr

        :param bus_name: 总线名称 sucn as "bodycan"
        :param msg_id: can ID 或 FR slot_id
        :param timeout: to do 暂无效
        :returns: (msg_id, time_stamp, length, data)
        :raises keyError:
        """
        if bus_name == "backbonefr":
            Msg = self.bus_app.bus_dict["tosun_tc1034"].recv(msgid=msg_id)
        else:
            # Msg = self.bus_app.bus_dict["tosun_tc1018"].recv()
            Msg = tosun_tc1018.recv(bus_chn=bus_chn, msgid=msg_id)

        return Msg

    def clear_recv_pdu_d_buffer(self, bus_name: str, timeout: float = 0.1):
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

    def resume_ecu_send(self, bus_name: str):
        '''
        @param bus_name:
        @return:
        '''
        self.ipdu.resume_ecu_send(bus_name)

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

    def start_record_trace_log(self, file_name):
        return self.bus_app.start_record_trace_log(file_rename=file_name)

    def stop_record_trace_log(self, is_record_status=True):
        return self.bus_app.stop_record_trace_log(is_record_status=is_record_status)
