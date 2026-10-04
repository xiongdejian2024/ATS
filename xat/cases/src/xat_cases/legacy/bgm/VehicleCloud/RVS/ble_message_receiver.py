
from ctypes import *
import time
import threading
from xat_ecu.legacy.common.logger import *
import os
import subprocess


class BLETP(threading.Thread):
    def __init__(self, pdu): 
        threading.Thread.__init__(self)
        self.pdu = pdu
        self.pdu.preheat_msg("connectivitycanfd", "BncmToBgmCanTpFrame")
        logger.info("Start preheating!!!")
        self.fc = [48,0,5,0xAA,0xAA,0xAA,0xAA,0xAA]
        self.msg_list = []

    def run(self):
        self.msg_list = self.get_bletp(timeout=5)
    
    def get_result(self):
        threading.Thread.join(self)
        try:
            return self.msg_list
        except Exception:
            return None

    def stop(self):
        self.pdu.remove_preheating("connectivitycanfd", "BncmToBgmCanTpFrame")
        
    def get_bletp(self, msg_id=0x31A, timeout=5):
        msg_len = 0
        msg_list = []
        start= time.time()
        data = []
        self.pdu.rx_flag_reset_msg("connectivitycanfd", msg_id)
        logger.info("Start to recv can message")
        while time.time() - start < timeout:
            self.pdu.rx_flag_reset_msg("connectivitycanfd", msg_id)
            rx_data = self.pdu.recv_pdu("connectivitycanfd", msg_id, timeout=1)
            if rx_data != None:
                rx_fm = rx_data[3]
            else:
                continue
            logger.info("Get frame:   {}".format(rx_fm))
            if rx_fm[0] == 0:
                data_len = rx_fm[1]
                data = rx_fm[2:data_len+2]
                msg_list.append(data)
                logger.info("Get single frame: {}".format(data))
                data = []
                continue
            elif rx_fm[0] < 32:
                self.pdu.send_pdu("connectivitycanfd", 0x33A, self.fc)
                msg_len = rx_fm[1]+(rx_fm[0]-16)*256
                data = rx_fm[2:]
                msg_len = msg_len - 62
                logger.info("Get first frame: {}".format(data))                
                continue
            elif rx_fm[0] >= 32:
                if msg_len > 63:
                    data = data + rx_fm[1:]
                    msg_len = msg_len - 63
                    logger.info("Get continue frame: {}".format(data)) 
                    continue
                else:
                    data = data + rx_fm[1:1+msg_len]
                    msg_list.append(data)
                    logger.info("Get last frame: {}".format(data)) 
                    data = []
                    continue
        logger.info("Get CANTP list: {}".format(msg_list))
        return msg_list