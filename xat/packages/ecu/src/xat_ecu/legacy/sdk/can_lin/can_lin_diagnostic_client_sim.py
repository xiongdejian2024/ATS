# -*- coding: utf-8 -*-
"""
@File        : can_lin_diagnostic_client_sim.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021-03-01 15:28
@Description : simulate diagnostic client behavior using pcan
"""

import os
# from ..driver.ethernet_lib.logger import main
import sys

from xat_ecu.legacy.sdk.driver.lin_lib.lin import Lin
import time
from threading import Thread
from copy import deepcopy
from xat_ecu.legacy.common.logger import *
import can
from time import sleep
from enum import IntEnum
from xat_ecu.legacy.sdk.diagnosis.uds_client_odx import Uds_Client_Odx
from xat_ecu.legacy.sdk.tp.cantp import CanTp
from xat_ecu.legacy.sdk.tp.lintp import Lin_Tp
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding

P2_CLIENT_ENHANCED_TIMEOUT = 5
P2_CLIENT_TIMEOUT = 0.15
P3_CLIENT_MIN = 0.15
S3_CLIENT = 2

# Self definition
TESTER_CLIENT_TIMEOUT = 6000     # Maximum waiting time(pending)

      
class Can_Lin_Diagnostic_Client_Sim():
    """
    Ntester_Sim
    At present, a case
    Parameter solidification, follow-up will be updated
    """

    def __init__(self, ecu_canid, channel, bus_type = "can", bitrate=500000, sec_con={}):
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
        self.ecu_canid = ecu_canid    # can id of ecu, such as 0x644 
        self.lin_nad = ecu_canid & 0xff    # lin ecu node address
        self.res_ecu_canid = self.ecu_canid + 0x80
        self.channel = channel        # channel name, such as 'can0'
        self.bitrate = bitrate 
        # self.p_n_res = p_n_res        # Positive Response or Negative Response,such as True,False
        # self.data_info = data_info    # Positive Response DID date ,such as [0x32,0x45,0x37] type:list     
        #                               #or type:dict (Default is recommended)  
        # self.nrc_code = nrc_code
        # self.dtc_code = dtc_code
        self.all_dtc_code_data = []
        self.bus_type = bus_type
        self.diagnostic_session = 0x01
        self.non_default_diagnostic_session_time = 0
        self.non_default_diagnostic_session_flag = False
        self.seed = [0,0,0,0]
        self.p_data = []
        self.data = []
        self.fc_flag = 0
        self.block_size = 8
        self.st = 20
        self.cycle_tag = True
        self.frame_num = 0
        self.rx_multi_frame_num = 0
        self.i_count = 0
        # self.routine_control_p_data = routine_control_p_data
        self.uds_client = Uds_Client_Odx(self.ecu_canid, sec_con=sec_con)
        self.positive_ack = None
        self.timeout = None
        self.i_ct = 0
        self.message_automatic_sent = None
        self.userdata_print = None

    def run(self):
        """
        要适配 Toomoss , To Do
        """
        if self.bus_type == "can":
            self.rx_bus = can.interface.Bus(bustype='socketcan', channel=self.channel,bitrate=self.bitrate)
            self.rx_bus.set_filters([{"can_id": self.res_ecu_canid, "can_mask": 0xffff}])
            # logger.info(self.res_ecu_canid)
            logger.info(self.res_ecu_canid)
            self.notifier = can.Notifier(self.rx_bus, [self.can_rx_tx_msg])
        elif self.bus_type == "lin":
            self.rx_bus = can.interface.Bus(bustype='socketcan_native', channel=self.channel,bitrate=self.bitrate)
            self.rx_bus.set_filters([{"can_id": 0x3c, "can_mask": 0xfc}])
            self.notifier = can.Notifier(self.rx_bus, [self.lin_rx_tx_msg])

    # def cycle_run(self):
    #     """
    #
    #     """
    #     if self.bus_type == "can":
    #         self.rx_bus = can.interface.Bus(bustype='socketcan', channel=self.channel,bitrate=self.bitrate)
    #
    #         self.rx_bus.set_filters([{"can_id": self.ecu_canid, "can_mask": 0xffff}])
    #         # logger.info(self.ecu_canid)
    #         self.notifier = can.Notifier(self.rx_bus, [self.can_cycle])

    def send_data(self, data:list):
        # data:list   such as [0x10, 0x03]
        self.diagnostic_parameter_reset()
        if self.bus_type == "can":
            udsdata = self.can_tx_msg(data)
            diag_msg_data = CanTp.construct_tx_signal_frames(udsdata)
        elif self.bus_type == "lin":
            udsdata = self.lin_tx_msg(data)
            diag_msg_data = Lin_Tp.construct_tx_signal_frames(self.lin_nad, udsdata)
        self.rx_bus.send(diag_msg_data)
        if data[0] not in [0x36]:
            userdata_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(data)
            logger.info("Raw Data (DoCan/Lin) : [Tx] {}".format(userdata_print))
        elif data[0] in [0x36]:
            logger.info("Considering the performance, the 0x36 service is not displayed")

    def send_data_functional_addressing(self, data, interval_time=P3_CLIENT_MIN):
        # functional addressing
        self.send_data(data)
        sleep(interval_time)

    def send_data_func_cycle(self, data, cycle_time=S3_CLIENT):
        # DIAG_MSG_TYPE
        while self.func_cycle:
            self.send_data(data)
            logger.info("Wait {} seconds to func_cycle".format(cycle_time))
            sleep(cycle_time)

    def send_data_func_cycle_thread(self, data, cycle_time=S3_CLIENT):
        func_msg_cycle = Thread(target=self.send_data_func_cycle,
                                name="Functional_Message_Cycle_DoCan/Lin", args=(data, cycle_time), daemon=True)
        func_msg_cycle.start()

    def check_response(self, timeout=P2_CLIENT_TIMEOUT):
        self.timeout = timeout
        self.i_ct = 0
        wait_pending = 0
        while (self.positive_ack is None) and (self.i_ct < self.timeout) and (wait_pending < TESTER_CLIENT_TIMEOUT):
            sleep(0.001)
            if self.i_ct == 0:
                wait_pending += 2
            self.i_ct += 0.001
        return self.positive_ack

    def retrun_udsdata_and_check_response(self, timeout=P2_CLIENT_TIMEOUT):
        self.timeout = timeout
        self.i_ct = 0
        wait_pending = 0
        while (self.positive_ack is None) and (self.i_ct < self.timeout) and (wait_pending < TESTER_CLIENT_TIMEOUT):
            sleep(0.001)
            if self.i_ct == 0:
                wait_pending += 2
            self.i_ct += 0.001
        return self.positive_ack, self.p_data

    def diagnostic_parameter_reset(self):
        self.positive_ack = None
        self.timeout = P2_CLIENT_TIMEOUT

    def close(self):
        """
        Close Ecu_Sim by stopping notifier and interface_bus 
        """
        try:
            # self.notifier.stop()
            self.func_cycle = False
            sleep(2)
            self.rx_bus.socket.close()
            self.rx_bus.shutdown()
        except AttributeError:
            logger.error('Ecu_Sim close error: {}'.format(self.ecu_canid))

    def can_tx_msg(self , data_info):
        # :data_info : diagnostic data          type: list
        if data_info != [] :
            if len(data_info) <= 7:
                self.data = CanTp.construct_tx_signal_frames(data_info)
                return self.data
            elif len(data_info) > 7:
                self.frame_num = len(data_info) //7
                #logger.info("frame length is {}".format(self.frame_num + 1))
                if self.frame_num > 0 :
                    self.data = CanTp.construct_tx_multi_frames(data_info)
                    return self.data[0]

    def lin_tx_msg(self , data_info):
        # :data_info : diagnostic data          type: list
        if data_info != [] :
            if len(data_info) <= 6:
                self.data = Lin_Tp.construct_tx_signal_frames(self.lin_nad, data_info)
                return self.data
            elif len(data_info) > 6:
                self.frame_num = len(data_info) //6
                #logger.info("frame length is {}".format(self.frame_num + 1))
                if self.frame_num > 0 :
                    self.data = Lin_Tp.construct_tx_multi_frames(data_info)
                    return self.data[0]

    
    # def can_single_cycle(self, data, cycle_time = 2.0):
    #     # :data : diagnostic data          type: list     8
    #     msg = can.Message(arbitration_id = self.ecu_canid, data = data, is_extended_id=False)
    #     while self.cycle_tag:
    #         self.rx_bus.send(msg)
    #         sleep(cycle_time)

    # def can_cycle(self, msg):
    #     pass
    
    def can_rx_tx_msg(self, msg):
        #logger.info("msg is {}".format(msg))
        # length = 8
        
        frame_type = msg.data[0] >> 4
        #logger.info("frame_type is {}".format(frame_type))
        
        can_id_3  = msg.arbitration_id >> 8
        if can_id_3 != 6:
            # logger.info("Unfiltered messages when ECU_sim starts")
            logger.info("Unfiltered messages when ECU_sim starts")
        else:
            userdata_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(msg)
            logger.info("Raw Data (DoCan/Lin) : [Rx] {}".format(userdata_print))
            if frame_type == 0 :                
                length, data = CanTp.deconstruct_rx_signal_frames(msg.data)
                self.p_data = data
                self.rx_data_handing(self.p_data)
                
            elif frame_type == 1 :
                length, data = CanTp.deconstruct_rx_first_frame(msg.data)
                if length <= 7 :
                    # logger.error("data length of rx_first_frame is error, it is less than 8")
                    logger.info("data length of rx_first_frame is error, it is less than 8")

                elif length > 7:
                    self.rx_multi_frame_num = length // 7
                    # logger.info("The number of this multi frame is {}".format(self.frame_num + 1))
                    logger.info("The number of this multi frame is {}".format(self.frame_num + 1))

                flowdata = CanTp.construct_tx_flow_frame(fc_flag = self.fc_flag, block_size = self.block_size, st = self.st)
                msg = can.Message(arbitration_id = self.ecu_canid, data=flowdata, is_extended_id=False)
                self.rx_bus.send(msg)
                self.sid = data[0] - 0x40
                self.p_data = data[1:]

            elif frame_type == 2:
                if self.rx_multi_frame_num > 1 :
                    if self.i_count < 7 :
                        index , data = CanTp.deconstruct_rx_consecutive_frame(msg.data)
                        self.p_data = self.p_data + data
                        self.rx_multi_frame_num -= 1
                        self.i_count += 1
                    elif self.i_count == 7 :
                        index , data = CanTp.deconstruct_rx_consecutive_frame(msg.data)
                        self.p_data = self.p_data + data
                        flowdata = CanTp.construct_tx_flow_frame(fc_flag = self.fc_flag, block_size = self.block_size, st = self.st)
                        msg = can.Message(arbitration_id = self.ecu_canid, data=flowdata, is_extended_id=False)
                        self.rx_bus.send(msg)   
                        self.rx_multi_frame_num -= 1                     
                        self.i_count = 0
                elif self.rx_multi_frame_num == 1:
                    index , data = CanTp.deconstruct_rx_consecutive_frame(msg.data)
                    self.p_data = self.p_data + data
                    self.i_count = 0 
                    self.rx_multi_frame_num = 0
                    logger.info("It is detected that all consecutive frames have been sent")
                    self.rx_data_handing(self.p_data)
                else :
                    self.i_count = 0 
                    self.rx_multi_frame_num = 0
                    # logger.error("The total number of multiple frames exceeded the expectation")
                    logger.info("The total number of multiple frames exceeded the expectation")
                                      
            elif frame_type == 3:
                fc_flag, block_size, st = CanTp.deconstruct_rx_flow_frame(msg.data)
                if fc_flag == 0:
                    # ContinueToSend
                    if block_size == 0:
                        #The BS parameter value zero (0) shall be used to indicate to the sender that 
                        #no more FC frames shall besent during the transmission of the segmented message.
                        bs = self.frame_num
                    else:    
                        self.frame_num = self.frame_num - block_size
                        if self.frame_num <= 0:                
                            bs = self.frame_num + block_size
                        else:
                            bs = block_size   
                    for i in range(bs):
                        #logger.info("i value is {}".format(i))
                        msg = can.Message(arbitration_id = self.ecu_canid, data = self.data[i+1], is_extended_id = False)
                        self.rx_bus.send(msg)
                        if st == 0:
                            sleep(0.005)    # Tentative 5ms
                            # logger.info("Tx Message interval is 5ms")
                            logger.info("Tx Message interval is 5ms")
                        elif st > 0 and st < 0x80 :
                            # SeparationTime (STmin) range: 0 ms – 127 ms 
                            sleep(st/1000)
                            # logger.info("Tx Message interval is {}ms".format(st))  
                            logger.info("Tx Message interval is {}ms".format(st)) 
                        elif st >= 0xF1 and st <= 0xF9:
                            #SeparationTime (STmin) range: 100 μs – 900 μs
                            #However, compass can only send messages at a maximum speed of about 500us, 
                            #so messages are sent at 1ms intervals
                            sleep(0.001)
                            #logger.info("Tx Message interval is 1ms")
                        else:
                            assert False,"This range of Tsmin values is reserved by this part of ISO 15765"
                elif fc_flag == 1:  
                    # logger.info("Wait for a new FlowControl")
                    logger.info("Wait for a new FlowControl")
                elif fc_flag == 2:
                    assert False,"Exceeds the buffer size of the receiving entity"
                else:
                    assert False,"This range of FS values is reserved by this part of ISO 15765"

    def rx_data_handing(self, udsdata):
        self.userdata_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(udsdata)
        logger.info("UDS Data (DoCan/Lin) : [Rx] {}".format(self.userdata_print))
        self.sid = udsdata[0]
        if self.sid == 0x7F:
            self.sid = udsdata[1]
            self.get_sub_data = udsdata[2]
            if self.get_sub_data == 0x78:
                # docan/lin timeout is 5
                self.positive_ack = None
                self.timeout = P2_CLIENT_ENHANCED_TIMEOUT
                self.i_ct = 0
            else:
                self.positive_ack = False
                self.timeout = P2_CLIENT_TIMEOUT
        else:
            self.positive_ack = True
            self.timeout = P2_CLIENT_TIMEOUT
            self.get_sub_data = udsdata[1:]
            self.uds_client.diagnostic_services_return_p_data(self.sid, self.get_sub_data)
            if self.uds_client.p_data:
                self.automatic_send_data = self.uds_client.p_data
                self.message_automatic_sent = True

    def lin_rx_tx_msg(self,msg):
        #logger.info("lin msg is {}".format(msg))
        
        frame_type = msg.data[1] >> 4
        #logger.info("lin frame_type is {}".format(frame_type))
        pid = msg.arbitration_id
        # logger.info("pid is {}".format(pid))
        # logger.info("self.lin_nad is {}".format(self.lin_nad))
        # logger.info("msg.data[0] is {}".format(msg.data[0]))
        
        if  self.lin_nad == msg.data[0]:
        # Screening different Lin ECU
            userdata_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(msg)
            logger.info("Raw Data (DoCan/Lin) : [Rx] {}".format(userdata_print))
            if pid == 0x3d:
                logger.info("Receive lin Diagnosis response")
                length, data = Lin_Tp.deconstruct_rx_signal_frames(msg.data)
                if frame_type == 0:
                    self.rx_data_handing(data)

                elif frame_type == 1:
                    length, data = Lin_Tp.deconstruct_rx_first_frame(msg.data)
                    if length <= 6:
                        logger.error("data length of rx_first_frame is error, it is less than 7")

                    elif length > 6:
                        self.rx_multi_frame_num = length // 6
                        logger.info("The number of this multi frame is {}".format(self.frame_num + 1))
                    self.sid = data[0] - 0x40
                    self.p_data = data[1:]

                elif frame_type == 2:
                    if self.rx_multi_frame_num >= 1:
                        index, data = Lin_Tp.deconstruct_rx_consecutive_frame(msg.data)
                        self.p_data = self.p_data + data
                        self.rx_multi_frame_num -= 1
                        if self.rx_multi_frame_num == 0:
                            logger.info("It is detected that all consecutive frames have been sent")
                            self.rx_data_handing(self.p_data)
                    else:
                        self.i_count = 0
                        self.rx_multi_frame_num = 0
                        logger.error("The total number of multiple frames exceeded the expectation")
                                
if __name__ == "__main__":
    
    A = Can_Lin_Diagnostic_Client_Sim(0x605,"can4")
    A.run()
    A.can_tx_msg([0x10,0x03])
    sleep(1)
    A.can_tx_msg([0x3E,0x80])
    sleep(1)
    print("wan")
            
            
            
        
