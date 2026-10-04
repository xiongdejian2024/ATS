# -*- coding: utf-8 -*-
"""
@File        : ecu_can_lin_doip_simulator.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021-03-01 23:59
@Description : (Ecu_Sim)simulate the ecu behavior using pcan
"""
import copy
import math

from sdk.driver.lin_lib.lin import Lin
import time
import errno
import subprocess
import threading
from threading import Thread
from copy import deepcopy
from xat_ecu.legacy.common.logger import *
import can
from time import sleep
from enum import IntEnum
from xat_ecu.legacy.sdk.tp.cantp import CanTp
from xat_ecu.legacy.sdk.tp.flexraytp import FlexRayTp
from xat_ecu.legacy.sdk.tp.lintp import Lin_Tp
from xat_ecu.legacy.sdk.diagnosis.uds_server_odx import Uds_Server_Odx
from xat_ecu.legacy.common import exception_error
from xat_ecu.legacy.common.error_code import StatusCode
from xat_ecu.legacy.common.exception_error import error_check
from xat_ecu.legacy.common.error_callback import error_callback
from xat_ecu.legacy.utils.utils import struct_pretty


daig_func_list = []
daig_func_list_fr = []


class Ecu_Sim(Uds_Server_Odx):
    """
    Ecu_Sim
    At present, a case
    Parameter solidification, follow-up will be updated
    """

    def __init__(
        self,
        tosun_obj=None,
        bus_name=None,
        ecu="TCAM",
        ecu_canid=None,
        channel="can0",
        res_ecu_canid=None,
        lin_nad=None,
        bus_type="can",
        bitrate=500000,
        p_n_res=True,
        data_info=[],
        nrc_code=0x22,
        dtc_code=[],
        routine_control_p_data={},
        snapshot_data=None,
        extended_data=None,
        # block_size=8,
        # st=20,
        block_size=0,
        st=0,
        sec_con={},
        mock_uds_data=None
    ):
        """
        Initialize a SocketCan object.
        :param ecu_canid: can id of ecu,such as '0x644'     type : int
        :param channel: channel interface, such as 'can0', 'can1'    type : str
        :param bitrate: bitrate of socket can, default is 500000
        :param p_n_res: Positive Response or Negative Response,such as Ture,False   type:bool
        :param data_info : Response date ,such as [0x32,0x45,0x37]         type:list or dict
        :param dtc_code : such as  {'C16A904': [86, 169, 4, 15] ,'C16AA04': [86, 170, 4, 15]}      type : dict
                            [86, 169, 4, 15] is DTC code and  status Of DTC
                            DTC code ,such as 'B150111'
        :param routine_control_p_data : routine control positive data (include rid , routine_type , rsr)  ,      type:dict
                            such as  {"08BA": { 1 : [0x00] , 3 : [0x02]}}
                            rid: "08BA" is  HV PowerDown
                            routine_type:  are Fixed
                                        1  ---- "start routine"
                                        2  ---- "stop rountine"
                                        3  ---- "rountine results"
                            rsr: [0x00],[0x02],[0xA0,0x01] Specific ECU may have different implementation
        """
        # threading.Thread.__init__(self)
        self.mock_uds_data = mock_uds_data
        self.tosun_obj = tosun_obj
        self.bus_name = bus_name
        self.ecu = ecu
        self.ecu_canid = ecu_canid  # can id of ecu, such as '0x644'
        self.lin_nad = lin_nad  # lin ecu node address
        self.res_ecu_canid = res_ecu_canid
        self.channel = channel  # channel name, such as 'can0'
        self.bitrate = bitrate
        self.p_n_res = (
            p_n_res  # Positive Response or Negative Response,such as True,False
        )
        self.data_info = (
            data_info  # Positive Response DID date ,such as [0x32,0x45,0x37] type:list
        )
        # or type:dict (Default is recommended)
        self.nrc_code = nrc_code
        self.dtc_code = dtc_code
        self.all_dtc_code_data = []
        self.bus_type = bus_type
        if self.bus_type == "canfd":
            self.is_fd = True
        else:
            self.is_fd = False
        self.diagnostic_session = 0x01
        self.non_default_diagnostic_session_time = 0
        self.non_default_diagnostic_session_flag = False
        self.seed = [0, 0, 0, 0]
        self.p_data = []
        self.routine_control_p_data = routine_control_p_data
        self.mock_uds_data = mock_uds_data
        self.block_size = block_size
        self.st = st
        self.frame_num = 0
        self.rx_multi_frame_num = 0
        self.i_count = 0
        super().__init__(self.ecu, sec_con=sec_con, mock_uds_data=self.mock_uds_data)

    def run(self):
        """ """
        if self.bus_type == "fr":
            global daig_func_list_fr
            if daig_func_list_fr:
                daig_func_list_fr.append(self.flex_rx_tx_mg)
            else:
                daig_func_list_fr.append(self.flex_rx_tx_mg)
                self.tosun_obj.register_diagfr_callback(self.diag_callback_fr)
        else:
            global daig_func_list
            if daig_func_list:
                daig_func_list.append(self.can_rx_tx_msg)
            else:
                daig_func_list.append(self.can_rx_tx_msg)
                self.tosun_obj.register_diagcan_callback(self.diag_callback)

    def diag_callback(self, msg):
        # To Do 暂时如此设计
        for func in daig_func_list:
            func(msg)

    def diag_callback_fr(self, msg):
        # To Do 暂时如此设计
        for func in daig_func_list_fr:
            func(msg)

    def close(self):
        """
        Close Ecu_Sim 
        """
        global daig_func_list
        global daig_func_list_fr
        if self.flex_rx_tx_mg in daig_func_list_fr:
            daig_func_list_fr.remove(self.flex_rx_tx_mg)

        if self.can_rx_tx_msg in daig_func_list:
            daig_func_list.remove(self.can_rx_tx_msg)

        self.tosun_obj.unregister_diagcan_callback()
        self.tosun_obj.unregister_diagfr_callback()

    def send_fr_message_by_uds(self, data):
        self.tosun_obj.fr_send(
            slot_id=self.res_ecu_canid,
            cyclecode=1,
            data=data,
            dlc=len(data)
        )
        logger.debug(f"发送flexray诊断数据: {bytes(data).hex()}")

    def flex_rx_tx_mg(self, msg):
        if self.mock_uds_data.no_reply:
            logger.info(f"flexray设置的诊断回复模式为不回复。")
            return
        try:
            if msg.FSlotId in [0x7f, self.ecu_canid]:
                return
            length = msg.FActualPayloadLength
            _raw_data = list(msg.FData[:length])
            logger.debug(f"接收到的诊断数据:{bytes(_raw_data).hex()}")

            self.non_default_diagnostic_session_time = 0
            raw_data_obj = FlexRayTp.construct_parse_frames_data(bytes(_raw_data))
            ta = list(raw_data_obj.TargetAddress)
            sa = list(raw_data_obj.SourceAddress)
            header = sa + ta
            if int(raw_data_obj.TargetAddress.hex(), 16) != self.ecu_canid:
                logger.debug(f"当前的ecu: {hex(self.ecu_canid)}, 接收到的ecu: 0x{raw_data_obj.TargetAddress.hex()} 不匹配直接返回。")
                return
            frame_type = raw_data_obj.FrameType.C_PCIType
            raw_data = raw_data_obj.RawData
            effective_length = 0
            max_len = 0
            if raw_data_obj.MessageInfo.get("EffectiveLength"):
                effective_length = raw_data_obj.MessageInfo.EffectiveLength
                max_len = raw_data_obj.MessageInfo.MaximumLoad

            bfs = 0xffff
            if self.mock_uds_data.BFS:
                for block, block_size in self.mock_uds_data.BFS.items():
                    bfs = block_size
                    if bfs < max_len and all([bfs, max_len]):
                        block_number = math.ceil(bfs/max_len)
                    else:
                        pass

            if max_len < effective_length:
                with error_check(StatusCode.DOCAN_LEN_ERR, exception_error.DOCANError):
                    raise

            if frame_type == 4 and max_len > effective_length:
                self.sid = raw_data[0]
                self.get_sub_data = list(raw_data[1:])
                data = FlexRayTp.construct_tx_flow_frame()
                self.send_fr_message_by_uds(header + data)
            elif frame_type == 4 and max_len == effective_length:
                self.sid = raw_data[0]
                self.get_sub_data = list(raw_data[1:])
                if self.p_n_res:
                    self.diagnostic_services_p_data(self.sid, self.get_sub_data)
                    logger.debug(f"当前的p_data:{bytes(self.p_data).hex()}")
                    if self.p_data != []:
                        if len(self.p_data) <= 14:
                            self.data = FlexRayTp.construct_tx_signal_frames(self.p_data)
                            self.send_fr_message_by_uds(header + self.data)
                        else:
                            self.data = FlexRayTp.construct_tx_multi_frames(self.p_data)
                            self.send_fr_message_by_uds(header + self.data.pop(0))
                else:
                    self.diagnostic_services_n_data()
                    logger.debug(f"消极响应的数据:{bytes(self.n_data).hex()}")
                    data = FlexRayTp.construct_tx_signal_frames(self.n_data)
                    self.send_fr_message_by_uds(header + data)
            elif frame_type == 5:
                self.get_sub_data += list(raw_data[1:])
            elif frame_type == 7:
                self.sid = raw_data[0]
                self.get_sub_data = list(raw_data[1:])
                data = FlexRayTp.construct_tx_flow_frame()
                self.send_fr_message_by_uds(header + data)
            elif frame_type == 8:
                for single_data in self.data:
                    time.sleep(0.01)
                    self.send_fr_message_by_uds(header + single_data)
            elif frame_type == 9:
                self.get_sub_data += list(raw_data[1:])
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/can_lin/ecu_can_lin_simulator.py")
            logger.warning(f"ecu mock错误，得到:{e}")

    def can_rx_tx_msg(self, msg):
        if self.mock_uds_data.no_reply:
            logger.info(f"can设置的诊断回复模式为不回复。")
            return

        if msg.FIdentifier not in [0x7FF, self.ecu_canid]:
            return

        length = msg.FDLC
        # length = DLC_DATA_BYTE_CNT[length]
        data_raw = msg.FData[:length]
        # logger.info(f"{hex(self.ecu_canid)},收到：{data_raw.hex()}")
        frame_type = data_raw[0] >> 4
        # logger.info("frame_type is {}".format(frame_type))

        can_id_3 = msg.FIdentifier >> 8
        length, data = CanTp.deconstruct_rx_signal_frames(data_raw)
        # logger.info(msg.FIdentifier)
        if can_id_3 not in [6, 7]:
            # logger.info("Unfiltered messages when ECU_sim starts")
            pass

        # length, data = CanTp.deconstruct_rx_signal_frames(data_raw)

        elif msg.FIdentifier == 0x7FF and (list(data)[1] >> 7) == 1:
            pass
            # logger.info(msg.FIdentifier)
        else:
            # logger.info(msg.FIdentifier)
            self.non_default_diagnostic_session_time = 0
            if frame_type == 0:
                # print('frame_type == 0')
                # logger.info(list(data))
                length, data = CanTp.deconstruct_rx_signal_frames(data_raw)
                if (list(data)[0:2]) == [62, 128]:
                    pass
                self.sid = data[0]
                # print('list(data)=',list(data))
                self.get_sub_data = data[1:length]
                # print('self.get_sub_data=',list(self.get_sub_data))
                # print('list(msg,data)',list(data))
                # print('data=',data)
                # print('length',length)
                # print('data=',data)
                # print('self.sid',self.sid)
                # print('self.get_sub_data = data[1:length]=',self.get_sub_data)
                if self.p_n_res:
                    self.diagnostic_services_p_data(self.sid, self.get_sub_data)
                    if self.p_data != []:
                        if len(self.p_data) <= 7:
                            # print('len(self.p_data) <= 7')
                            self.data = CanTp.construct_tx_signal_frames(self.p_data)
                            # logger.info(self.data)
                            self.tosun_obj.can_send(self.bus_name, self.data, self.res_ecu_canid, cycle_time=0)
                        elif len(self.p_data) > 7:
                            # print('len(self.p_data) > 7')
                            self.frame_num = len(self.p_data) // 7
                            # logger.info("frame length is {}".format(self.frame_num + 1))
                            if self.frame_num > 0:
                                self.data = CanTp.construct_tx_multi_frames(self.p_data)
                                # logger.info(self.data)
                                self.tosun_obj.can_send(self.bus_name, self.data[0], self.res_ecu_canid, cycle_time=0)
                else:
                    self.diagnostic_services_n_data()
                    self.data = CanTp.construct_tx_signal_frames(self.n_data)
                    logger.debug(f"当前发送的数据：{bytes(self.data).hex()}")
                    self.tosun_obj.can_send(self.bus_name, self.data, self.res_ecu_canid, cycle_time=0)

            elif frame_type == 1:
                # print('frame_type == 1')
                # The flow frame uses the default value temporarily
                length, data = CanTp.deconstruct_rx_first_frame(data_raw)
                self.length = length
                self.sid = data[0]
                self.get_sub_data = data[1:]
                if length <= 7:
                    # logger.error(
                    #     "data length of rx_first_frame is error, it is less than 8"
                    # )
                    with error_check(StatusCode.DOCAN_SINGLE_FRAME_LEN_ERR, exception_error.DOCANError, error_callback, data, length):
                        raise
                elif length > 7:
                    self.rx_multi_frame_num = length // 7
                    # logger.info(
                    #     "The number of this multi frame is {}".format(
                    #         self.frame_num + 1
                    #     )
                    # )
                    logger.info(
                        "多帧数量为 {} 帧".format(
                            self.frame_num + 1
                        )
                    )
                self.data = CanTp.construct_tx_flow_frame(
                    block_size=self.block_size, st=self.st
                )
                self.tosun_obj.can_send(self.bus_name, self.data, self.res_ecu_canid, cycle_time=0)

            elif frame_type == 2:
                # print('frame_type == 2')
                # Temporary fixed use (block_size = 8)
                if self.rx_multi_frame_num > 1:
                    if self.i_count < (self.block_size - 1):
                        # index , data = CanTp.deconstruct_rx_consecutive_frame(data_raw)
                        self.rx_multi_frame_num -= 1
                        self.i_count += 1
                        index, data = CanTp.deconstruct_rx_consecutive_frame(data_raw)
                        self.get_sub_data += data
                    elif self.i_count == (self.block_size - 1):
                        self.data = CanTp.construct_tx_flow_frame(
                            block_size=self.block_size, st=self.st
                        )
                        self.tosun_obj.can_send(self.bus_name, self.data, self.res_ecu_canid, cycle_time=0)
                        self.rx_multi_frame_num -= 1
                        self.i_count = 0
                        index, data = CanTp.deconstruct_rx_consecutive_frame(data_raw)
                        self.get_sub_data += data
                    elif self.block_size == 0:
                        # 不用再发流控帧
                        self.rx_multi_frame_num -= 1
                        index, data = CanTp.deconstruct_rx_consecutive_frame(data_raw)
                        self.get_sub_data += data
                elif self.rx_multi_frame_num == 1:
                    self.i_count = 0
                    self.rx_multi_frame_num = 0
                    index, data = CanTp.deconstruct_rx_consecutive_frame(data_raw)
                    self.get_sub_data += data
                    # logger.info(
                    #     "It is detected that all consecutive frames have been sent"
                    # )
                    logger.info("检测到所有连续帧都已发送")
                    if self.p_n_res:
                        self.get_sub_data = self.get_sub_data[0 : self.length - 1]
                        self.diagnostic_services_p_data(self.sid, self.get_sub_data)
                        if self.p_data != []:
                            if len(self.p_data) <= 7:
                                self.data = CanTp.construct_tx_signal_frames(
                                    self.p_data
                                )
                                # logger.info(self.data)

                                # 0x36 最后回复前加个 7F 36 78
                                if self.sid == 0x36:
                                    data_78 = CanTp.construct_tx_signal_frames(
                                        [0x7F, 0x36, 0x78]
                                    )

                                    self.tosun_obj.can_send(self.bus_name, data_78, self.res_ecu_canid, cycle_time=0)
                                    sleep(0.01)  # 模拟数据处理时间

                                self.tosun_obj.can_send(self.bus_name, self.data, self.res_ecu_canid, cycle_time=0)
                            elif len(self.p_data) > 7:
                                self.frame_num = len(self.p_data) // 7
                                # logger.info("frame length is {}".format(self.frame_num + 1))
                                if self.frame_num > 0:
                                    self.data = CanTp.construct_tx_multi_frames(
                                        self.p_data
                                    )
                                    # logger.info(self.data)
                                    self.tosun_obj.can_send(self.bus_name, self.data, self.res_ecu_canid, cycle_time=0)
                    else:
                        self.diagnostic_services_n_data()
                        self.data = CanTp.construct_tx_signal_frames(self.n_data)
                        logger.info(self.data)
                        self.tosun_obj.can_send(self.bus_name, self.data, self.res_ecu_canid, cycle_time=0)
                else:
                    self.i_count = 0
                    self.rx_multi_frame_num = 0
                    # logger.error(
                    #     "The total number of multiple frames exceeded the expectation"
                    # )
                    with error_check(None, exception_error.DOCANError):
                        raise AssertionError(f"多个帧的总数超出预期")

            elif frame_type == 3:
                fc_flag, block_size, st = CanTp.deconstruct_rx_flow_frame(data_raw)
                if fc_flag == 0:
                    # ContinueToSend
                    if block_size == 0:
                        # The BS parameter value zero (0) shall be used to indicate to the sender that
                        # no more FC frames shall besent during the transmission of the segmented message.
                        bs = self.frame_num
                    else:
                        self.frame_num = self.frame_num - block_size
                        if self.frame_num <= 0:
                            bs = self.frame_num + block_size
                        else:
                            bs = block_size
                    for i in range(bs):
                        # logger.info("i value is {}".format(i))
                        self.tosun_obj.can_send(self.bus_name, self.data[i + 1], self.res_ecu_canid, cycle_time=0)
                        if st == 0:
                            sleep(0.005)  # Tentative 5ms
                            # logger.info("Tx Message interval is 5ms")
                            logger.info("发送消息间隔 5ms")
                        elif st > 0 and st < 0x80:
                            # SeparationTime (STmin) range: 0 ms – 127 ms
                            sleep(st / 1000)
                            # logger.info("Tx Message interval is {}ms".format(st))
                            logger.info("发送消息间隔 {}ms".format(st))
                        elif st >= 0xF1 and st <= 0xF9:
                            # SeparationTime (STmin) range: 100 μs – 900 μs
                            # However, compass can only send messages at a maximum speed of about 500us,
                            # so messages are sent at 1ms intervals
                            sleep(0.001)
                            # logger.info("Tx Message interval is 1ms")
                        else:
                            with error_check(None, exception_error.DOCANError):
                                raise AssertionError("此Tsmin值范围由ISO 15765的此部分保留")
                            # assert (
                            #     False
                            # ), "This range of Tsmin values is reserved by this part of ISO 15765"
                elif fc_flag == 1:
                    # logger.info("Wait for a new FlowControl")
                    logger.info("等待一个新的流控帧")
                elif fc_flag == 2:
                    with error_check(None, exception_error.DOCANError):
                        raise AssertionError("超过接收实体的缓冲区大小")
                    # assert False, "Exceeds the buffer size of the receiving entity"
                else:
                    with error_check(None, exception_error.DOCANError):
                        raise AssertionError("此FS值范围由ISO 15765的此部分保留")
                    # assert (
                    #     False
                    # ), "This range of FS values is reserved by this part of ISO 15765"

    # def lin_rx_tx_msg(self, msg):
    #     # logger.info("lin msg is {}".format(msg))

    #     frame_type = data[1] >> 4
    #     # logger.info("lin frame_type is {}".format(frame_type))
    #     pid = msg.FIdentifier
    #     # logger.info("pid is {}".format(pid))
    #     # logger.info("self.lin_nad is {}".format(self.lin_nad))
    #     # logger.info("data[0] is {}".format(data[0]))
    #     self.non_default_diagnostic_session_time = 0
    #     if self.lin_nad == data[0]:
    #         # Screening different Lin ECU
    #         if pid == 0x3C:
    #             logger.info("lin Diagnosis resquest")
    #             if frame_type == 0:
    #                 length, data = Lin_Tp.deconstruct_rx_signal_frames(data_raw)
    #                 self.sid = data[0]
    #                 self.get_sub_data = data[1:length]
    #                 if self.p_n_res:
    #                     self.diagnostic_services_p_data(self.sid, self.get_sub_data)
    #                     if self.p_data != []:
    #                         if len(self.p_data) <= 6:
    #                             self.data = Lin_Tp.construct_tx_signal_frames(
    #                                 self.lin_nad, self.p_data
    #                             )
    #                             logger.info(self.data)
    #                             msg = can.Message(
    #                                 arbitration_id=0x7D,
    #                                 data=self.data,
    #                                 is_extended_id=False,
    #                             )
    #                             self.rx_bus.send(msg)
    #                             self.frame_num = 0
    #                         elif len(self.p_data) > 6:
    #                             self.frame_num = len(self.p_data) // 6
    #                             self.i = 0
    #                             # logger.info("frame length is {}".format(self.frame_num + 1))
    #                             self.data = Lin_Tp.construct_tx_multi_frames(
    #                                 self.lin_nad, self.p_data
    #                             )
    #                             # logger.info(self.data)
    #                             msg = can.Message(
    #                                 arbitration_id=0x7D,
    #                                 data=self.data[self.i],
    #                                 is_extended_id=False,
    #                             )
    #                             self.rx_bus.send(msg)
    #                 else:
    #                     self.diagnostic_services_n_data()
    #                     self.data = Lin_Tp.construct_tx_signal_frames(
    #                         self.lin_nad, self.n_data
    #                     )
    #                     logger.info(self.data)
    #                     msg = can.Message(
    #                         arbitration_id=0x7D, data=self.data, is_extended_id=False
    #                     )
    #                     self.rx_bus.send(msg)

    #             elif frame_type == 1:
    #                 # If there is a requirement to be added
    #                 # length, data = Lin_Tp.deconstruct_rx_first_frame(data)
    #                 pass

    #             elif frame_type == 2:
    #                 # If there is a requirement to be added
    #                 pass

    #         if pid == 0x3D:
    #             if self.frame_num > 0:
    #                 self.i = self.i + 1
    #                 self.frame_num = self.frame_num - 1
    #                 # logger.info("self.i value is {}".format(self.i))
    #                 msg = can.Message(
    #                     arbitration_id=0x7D,
    #                     data=self.data[self.i],
    #                     is_extended_id=False,
    #                 )
    #                 self.rx_bus.send(msg)

    #             elif self.frame_num == 0:
    #                 logger.info("lin msg send finished")
