# -*- coding: utf-8 -*-
"""
@File        : cantp.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2023-06-11 10:02
@Description : cantp ---- Assemble the data according to the requirements of can diagnosis
"""


DEFAULT_VALUE = 0x00     # 不够8 bytes 填 默认值
# Can Diagnosis TP
class CanTp:
       
    @staticmethod    
    def construct_tx_signal_frames(data):
        msg_length = len(data)   # msg_length <= 7
        signal = [msg_length]
        
        while len(data) > 0:
            signal.append(data.pop(0))
        # 不够8 bytes 填 默认值
        aa_length = 7 - msg_length 
        signal = signal + [DEFAULT_VALUE]*aa_length
        return signal
    
    @staticmethod     
    def construct_tx_multi_frames(data):
        msg_length = len(data)   # msg_length <= 4095 and msg_length >7
        first_header = 0x1000 | msg_length
        first = [(first_header >> 8)]
        first.append(first_header & 0xff)

        while len(first) < 8 and len(data) > 0:
            first.append(data.pop(0))
        tx_frames = [first]

        idx = 0
        for i in range(msg_length//7):
            idx += 1
            consecutive_frame = [0x20 | idx]
            while len(consecutive_frame) < 8 and len(data) > 0:
                consecutive_frame.append(data.pop(0))
            tx_frames.append(consecutive_frame)
            if idx == 0xF:
                idx = -1
        # add "AA"
        aa_length = 8 - len(tx_frames[-1])
        consecutive_frame_last = tx_frames[-1] + [DEFAULT_VALUE]*aa_length
        tx_frames[-1] = consecutive_frame_last
        return tx_frames

    @staticmethod 
    def construct_tx_flow_frame(fc_flag=0, block_size=8, st=20):
        tx_flow_control_frame = [0x30 | fc_flag]
        tx_flow_control_frame.append(block_size)
        tx_flow_control_frame.append(st)
        aa_length = 5
        tx_flow_control_frame = tx_flow_control_frame + [DEFAULT_VALUE]*aa_length
        return tx_flow_control_frame
    
    @staticmethod 
    def deconstruct_rx_signal_frames(msg):
        # msg is Message.data
        #frame_type = msg[0] >> 4
        length = 0xf & msg[0]
        data = msg[1:]
        return length, data
    
    @staticmethod     
    def deconstruct_rx_first_frame(msg):
        # msg is Message.data
        #frame_type = msg[0] >> 4
        length = ((0xf & msg[0]) << 8) | msg[1]
        data = msg[2:]
        return length, data

    @staticmethod 
    def deconstruct_rx_consecutive_frame(msg):
        #frame_type = msg[0] >> 4
        index = msg[0] & 0xf
        data = msg[1:]
        return index, data

    @staticmethod 
    def deconstruct_rx_flow_frame(msg):
        #frame_type = ((0xf << 4) & msg[0]) >> 4
        fc_flag = msg[0] & 0xf
        block_size = msg[1]
        st = msg[2]
        return fc_flag, block_size, st

    