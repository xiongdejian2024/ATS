# -*- coding: utf-8 -*-
"""
@File        : lintp.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021-02-18 11:01
@Description : lintp ---- Assemble the data according to the requirements of lin diagnosis
"""


# Lin Diagnosis TP
class Lin_Tp: 
      
    @staticmethod    
    def construct_tx_signal_frames(lin_nad,data):
        msg_length = len(data)   # msg_length <= 6
        signal = [msg_length]
        
        while len(data) > 0:
            signal.append(data.pop(0))
        # add "FF"
        ff_length = 6 - msg_length 
        signal = signal + [0xFF]*ff_length
        
        # add lin node address
        signal = [lin_nad] + signal
        return signal
    
    @staticmethod     
    def construct_tx_multi_frames(lin_nad,data):
        msg_length = len(data)   # msg_length <= 4095 and msg_length >6
        first_header = 0x1000 | msg_length
        first = [(first_header >> 8)]
        first.append(first_header & 0xff)

        while len(first) < 7 and len(data) > 0:
            first.append(data.pop(0))
        tx_frames = [[lin_nad] + first]

        idx = 0
        for i in range(msg_length//6):
            idx += 1
            consecutive_frame = [0x20 | idx]
            while len(consecutive_frame) < 7 and len(data) > 0:
                consecutive_frame.append(data.pop(0))
            consecutive_frame = [lin_nad] + consecutive_frame
            tx_frames.append(consecutive_frame)
            if idx == 0xF:
                idx = -1
        # add "FF"
        ff_length = 8 - len(tx_frames[-1])
        consecutive_frame_last = tx_frames[-1] + [0xFF]*ff_length
        tx_frames[-1] = consecutive_frame_last
        return tx_frames

    @staticmethod 
    def deconstruct_rx_signal_frames(msg):
        lin_nad = msg[0]
        length = 0xf & msg[1]
        data = msg[2:]
        return length, data
    
    @staticmethod     
    def deconstruct_rx_first_frame(msg):
        length = ((0xf & msg[1]) << 8) | msg[2]
        lin_nad = msg[0]
        data = msg[3:]
        return length, data

    @staticmethod 
    def deconstruct_rx_consecutive_frame(msg):
        lin_nad = msg[0]
        index = msg[1] & 0xf
        data = msg[2:]
        return index, data

