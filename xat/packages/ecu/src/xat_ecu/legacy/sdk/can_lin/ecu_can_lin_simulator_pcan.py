# -*- coding: utf-8 -*-
"""
@File        : ecu_can_lin_doip_simulator.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021-03-01 23:59
@Description : (Ecu_Sim)simulate the ecu behavior using pcan
"""
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
from xat_ecu.legacy.sdk.tp.lintp import Lin_Tp
from xat_ecu.legacy.sdk.diagnosis.uds_server_odx import Uds_Server_Odx


class Ecu_Sim(Uds_Server_Odx):
    """
    Ecu_Sim
    At present, a case
    Parameter solidification, follow-up will be updated
    """

    def __init__(
        self,
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
        self.block_size = block_size
        self.st = st
        self.frame_num = 0
        self.rx_multi_frame_num = 0
        self.i_count = 0
        super().__init__(self.ecu, sec_con=sec_con)

    def run(self):
        """ """
        if self.bus_type in ["can", "canfd"]:
            if self.bus_type == "can":
                self.rx_bus = can.interface.Bus(
                    bustype='socketcan', channel=self.channel, bitrate=self.bitrate
                )
            else:
                self.rx_bus = can.interface.Bus(
                    bustype='socketcan',
                    channel=self.channel,
                    bitrate=self.bitrate,
                    fd=True,
                )
            self.rx_bus.set_filters(
                [
                    {"can_id": self.ecu_canid, "can_mask": 0xFFFF},
                    {"can_id": 0x7FF, "can_mask": 0xFFFF},
                ]
            )
            # logger.info(self.ecu_canid)
            self.notifier = can.Notifier(self.rx_bus, [self.can_rx_tx_msg])
        elif self.bus_type == "lin":
            # # BUG can.exceptions.CanInterfaceNotImplementedError: Unknown interface type "socketcan_native"    目前像是 接口没有了或没有接Lin dgou   To Do
            # self.rx_bus = can.interface.Bus(bustype='socketcan_native', channel=self.channel, bitrate=self.bitrate)

            # self.rx_bus.set_filters([{"can_id": 0x3c, "can_mask": 0xfc}])
            # self.notifier = can.Notifier(self.rx_bus, [self.lin_rx_tx_msg])
            pass

    def close(self):
        """
        Close Ecu_Sim by stopping notifier and interface_bus
        """
        try:
            self.notifier.stop()
            self.rx_bus.socket.close()
            self.rx_bus.shutdown()
        except AttributeError:
            logger.error(
                'Ecu_Sim close error: ecu {}    channel {}'.format(
                    self.ecu, self.channel
                )
            )

    def can_rx_tx_msg(self, msg):
        # logger.info("msg is {}".format(msg))

        frame_type = msg.data[0] >> 4
        # logger.info("frame_type is {}".format(frame_type))

        can_id_3 = msg.arbitration_id >> 8
        length, data = CanTp.deconstruct_rx_signal_frames(msg.data)
        # logger.info(msg.arbitration_id)
        if can_id_3 not in [6, 7]:
            # logger.info("Unfiltered messages when ECU_sim starts")
            pass

        # length, data = CanTp.deconstruct_rx_signal_frames(msg.data)

        elif msg.arbitration_id == 0x7FF and (list(data)[1] >> 7) == 1:
            pass
            # logger.info(msg.arbitration_id)
        else:
            # logger.info(msg.arbitration_id)
            self.non_default_diagnostic_session_time = 0
            if frame_type == 0:
                # print('frame_type == 0')
                # logger.info(list(msg.data))
                length, data = CanTp.deconstruct_rx_signal_frames(msg.data)
                if (list(data)[0:2]) == [62, 128]:
                    pass
                self.sid = data[0]
                # print('list(data)=',list(data))
                self.get_sub_data = data[1:length]
                # print('self.get_sub_data=',list(self.get_sub_data))
                # print('list(msg,data)',list(msg.data))
                # print('msg.data=',msg.data)
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
                            msg = can.Message(
                                arbitration_id=self.res_ecu_canid,
                                data=self.data,
                                is_fd=self.is_fd,
                                bitrate_switch=self.is_fd,
                                is_extended_id=False,
                            )
                            self.rx_bus.send(msg)
                        elif len(self.p_data) > 7:
                            # print('len(self.p_data) > 7')
                            self.frame_num = len(self.p_data) // 7
                            # logger.info("frame length is {}".format(self.frame_num + 1))
                            if self.frame_num > 0:
                                self.data = CanTp.construct_tx_multi_frames(self.p_data)
                                # logger.info(self.data)
                                msg = can.Message(
                                    arbitration_id=self.res_ecu_canid,
                                    data=self.data[0],
                                    is_fd=self.is_fd,
                                    bitrate_switch=self.is_fd,
                                    is_extended_id=False,
                                )
                                self.rx_bus.send(msg)
                else:
                    self.diagnostic_services_n_data()
                    self.data = CanTp.construct_tx_signal_frames(self.n_data)
                    logger.info(self.data)
                    msg = can.Message(
                        arbitration_id=self.res_ecu_canid,
                        data=self.data,
                        is_fd=self.is_fd,
                        bitrate_switch=self.is_fd,
                        is_extended_id=False,
                    )
                    self.rx_bus.send(msg)

            elif frame_type == 1:
                # print('frame_type == 1')
                # The flow frame uses the default value temporarily
                length, data = CanTp.deconstruct_rx_first_frame(msg.data)
                self.length = length
                self.sid = data[0]
                self.get_sub_data = data[1:]
                if length <= 7:
                    logger.error(
                        "data length of rx_first_frame is error, it is less than 8"
                    )
                elif length > 7:
                    self.rx_multi_frame_num = length // 7
                    logger.info(
                        "The number of this multi frame is {}".format(
                            self.frame_num + 1
                        )
                    )
                self.data = CanTp.construct_tx_flow_frame(
                    block_size=self.block_size, st=self.st
                )
                msg = can.Message(
                    arbitration_id=self.res_ecu_canid,
                    data=self.data,
                    is_fd=self.is_fd,
                    bitrate_switch=self.is_fd,
                    is_extended_id=False,
                )
                self.rx_bus.send(msg)

            elif frame_type == 2:
                # print('frame_type == 2')
                # Temporary fixed use (block_size = 8)
                if self.rx_multi_frame_num > 1:
                    if self.i_count < (self.block_size - 1):
                        # index , data = CanTp.deconstruct_rx_consecutive_frame(msg.data)
                        self.rx_multi_frame_num -= 1
                        self.i_count += 1
                        index, data = CanTp.deconstruct_rx_consecutive_frame(msg.data)
                        self.get_sub_data += data
                    elif self.i_count == (self.block_size - 1):
                        self.data = CanTp.construct_tx_flow_frame(
                            block_size=self.block_size, st=self.st
                        )
                        msg = can.Message(
                            arbitration_id=self.res_ecu_canid,
                            data=self.data,
                            is_fd=self.is_fd,
                            bitrate_switch=self.is_fd,
                            is_extended_id=False,
                        )
                        self.rx_bus.send(msg)
                        self.rx_multi_frame_num -= 1
                        self.i_count = 0
                        index, data = CanTp.deconstruct_rx_consecutive_frame(msg.data)
                        self.get_sub_data += data
                    elif self.block_size == 0:
                        # 不用再发流控帧
                        self.rx_multi_frame_num -= 1
                        index, data = CanTp.deconstruct_rx_consecutive_frame(msg.data)
                        self.get_sub_data += data
                elif self.rx_multi_frame_num == 1:
                    self.i_count = 0
                    self.rx_multi_frame_num = 0
                    index, data = CanTp.deconstruct_rx_consecutive_frame(msg.data)
                    self.get_sub_data += data
                    logger.info(
                        "It is detected that all consecutive frames have been sent"
                    )

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

                                    msg = can.Message(
                                        arbitration_id=self.res_ecu_canid,
                                        data=data_78,
                                        is_fd=self.is_fd,
                                        bitrate_switch=self.is_fd,
                                        is_extended_id=False,
                                    )
                                    self.rx_bus.send(msg)
                                    sleep(0.01)  # 模拟数据处理时间

                                msg = can.Message(
                                    arbitration_id=self.res_ecu_canid,
                                    data=self.data,
                                    is_fd=self.is_fd,
                                    bitrate_switch=self.is_fd,
                                    is_extended_id=False,
                                )
                                self.rx_bus.send(msg)
                            elif len(self.p_data) > 7:
                                self.frame_num = len(self.p_data) // 7
                                # logger.info("frame length is {}".format(self.frame_num + 1))
                                if self.frame_num > 0:
                                    self.data = CanTp.construct_tx_multi_frames(
                                        self.p_data
                                    )
                                    # logger.info(self.data)
                                    msg = can.Message(
                                        arbitration_id=self.res_ecu_canid,
                                        data=self.data[0],
                                        is_fd=self.is_fd,
                                        bitrate_switch=self.is_fd,
                                        is_extended_id=False,
                                    )
                                    self.rx_bus.send(msg)
                    else:
                        self.diagnostic_services_n_data()
                        self.data = CanTp.construct_tx_signal_frames(self.n_data)
                        logger.info(self.data)
                        msg = can.Message(
                            arbitration_id=self.res_ecu_canid,
                            data=self.data,
                            is_fd=self.is_fd,
                            bitrate_switch=self.is_fd,
                            is_extended_id=False,
                        )
                        self.rx_bus.send(msg)
                else:
                    self.i_count = 0
                    self.rx_multi_frame_num = 0
                    logger.error(
                        "The total number of multiple frames exceeded the expectation"
                    )

            elif frame_type == 3:
                fc_flag, block_size, st = CanTp.deconstruct_rx_flow_frame(msg.data)
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
                        msg = can.Message(
                            arbitration_id=self.res_ecu_canid,
                            data=self.data[i + 1],
                            is_fd=self.is_fd,
                            bitrate_switch=self.is_fd,
                            is_extended_id=False,
                        )
                        self.rx_bus.send(msg)
                        if st == 0:
                            sleep(0.005)  # Tentative 5ms
                            logger.info("Tx Message interval is 5ms")
                        elif st > 0 and st < 0x80:
                            # SeparationTime (STmin) range: 0 ms – 127 ms
                            sleep(st / 1000)
                            logger.info("Tx Message interval is {}ms".format(st))
                        elif st >= 0xF1 and st <= 0xF9:
                            # SeparationTime (STmin) range: 100 μs – 900 μs
                            # However, compass can only send messages at a maximum speed of about 500us,
                            # so messages are sent at 1ms intervals
                            sleep(0.001)
                            # logger.info("Tx Message interval is 1ms")
                        else:
                            assert (
                                False
                            ), "This range of Tsmin values is reserved by this part of ISO 15765"
                elif fc_flag == 1:
                    logger.info("Wait for a new FlowControl")
                elif fc_flag == 2:
                    assert False, "Exceeds the buffer size of the receiving entity"
                else:
                    assert (
                        False
                    ), "This range of FS values is reserved by this part of ISO 15765"

    def lin_rx_tx_msg(self, msg):
        # logger.info("lin msg is {}".format(msg))

        frame_type = msg.data[1] >> 4
        # logger.info("lin frame_type is {}".format(frame_type))
        pid = msg.arbitration_id
        # logger.info("pid is {}".format(pid))
        # logger.info("self.lin_nad is {}".format(self.lin_nad))
        # logger.info("msg.data[0] is {}".format(msg.data[0]))
        self.non_default_diagnostic_session_time = 0
        if self.lin_nad == msg.data[0]:
            # Screening different Lin ECU
            if pid == 0x3C:
                logger.info("lin Diagnosis resquest")
                if frame_type == 0:
                    length, data = Lin_Tp.deconstruct_rx_signal_frames(msg.data)
                    self.sid = data[0]
                    self.get_sub_data = data[1:length]
                    if self.p_n_res:
                        self.diagnostic_services_p_data(self.sid, self.get_sub_data)
                        if self.p_data != []:
                            if len(self.p_data) <= 6:
                                self.data = Lin_Tp.construct_tx_signal_frames(
                                    self.lin_nad, self.p_data
                                )
                                logger.info(self.data)
                                msg = can.Message(
                                    arbitration_id=0x7D,
                                    data=self.data,
                                    is_extended_id=False,
                                )
                                self.rx_bus.send(msg)
                                self.frame_num = 0
                            elif len(self.p_data) > 6:
                                self.frame_num = len(self.p_data) // 6
                                self.i = 0
                                # logger.info("frame length is {}".format(self.frame_num + 1))
                                self.data = Lin_Tp.construct_tx_multi_frames(
                                    self.lin_nad, self.p_data
                                )
                                # logger.info(self.data)
                                msg = can.Message(
                                    arbitration_id=0x7D,
                                    data=self.data[self.i],
                                    is_extended_id=False,
                                )
                                self.rx_bus.send(msg)
                    else:
                        self.diagnostic_services_n_data()
                        self.data = Lin_Tp.construct_tx_signal_frames(
                            self.lin_nad, self.n_data
                        )
                        logger.info(self.data)
                        msg = can.Message(
                            arbitration_id=0x7D, data=self.data, is_extended_id=False
                        )
                        self.rx_bus.send(msg)

                elif frame_type == 1:
                    # If there is a requirement to be added
                    # length, data = Lin_Tp.deconstruct_rx_first_frame(msg.data)
                    pass

                elif frame_type == 2:
                    # If there is a requirement to be added
                    pass

            if pid == 0x3D:
                if self.frame_num > 0:
                    self.i = self.i + 1
                    self.frame_num = self.frame_num - 1
                    # logger.info("self.i value is {}".format(self.i))
                    msg = can.Message(
                        arbitration_id=0x7D,
                        data=self.data[self.i],
                        is_extended_id=False,
                    )
                    self.rx_bus.send(msg)

                elif self.frame_num == 0:
                    logger.info("lin msg send finished")
