# -*- coding: utf-8 -*-
"""
@File        : uds_client_odx.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021-11-30 11:05
@Description :
"""

import sys
import os

from xat_ecu.legacy.sdk.driver.lin_lib.lin import Lin
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
from xat_ecu.legacy.sdk.diagnosis.aes_128_cbc import Aes128
from typing import Tuple, Union
from xat_ecu.legacy.sdk.diagnosis.uds_securitycal import SecurityAlgorithm


class Diagnostic_Sid(IntEnum):
    DIAGNOSTICSESSIONCONTROL = 0X10
    ECURESET = 0X11
    CLEARDIAGNOSTICINFORMATION = 0X14
    READDTCINFORMATION = 0X19
    READDATABYIDENTIFIER = 0X22
    SECURITYACCESS = 0X27
    COMMUNICATIONCONTROL = 0X28
    WRITEDATABYIDENTIFIER = 0X2E
    INPUTOUTPUTCONTROLBYIDENTIFIER = 0X2F
    ROUTINECONTROL = 0X31
    REQUESTDOWNLOAD = 0X34
    TRANSFERDATA = 0X36
    REQUESTTRANSFEREXIT = 0X37
    REQUESTFILETRANSFER = 0x38
    TESTERPRESENT = 0X3E
    CONTROLDTCSETTINGS =0X85
    

def crc8(data, div=0x11D):
    '''
    **CRC8 algorithm used is defined by SAE (refer to SAE-J1850), using the division
    polynomial x8+x4+x3+x2+1    div = 0x11D
    :data is list , such as [0x11,0x22]
    '''
    t_crc = 0xFF
    i = 0
    while i < len(data):
        t_crc ^= data[i]
        b = 0
        while b < 8:
            if (t_crc & 0x80) != 0:
                t_crc <<= 1
                t_crc ^= div
            else:
                t_crc <<= 1
            b += 1
        i += 1
    t_crc ^= 0xFF
    return t_crc	

class Uds_Client_Odx:
    def __init__(self, ecu="BGM", sec_con={}):
        self.return_data = []
        # self.return_p_n = None
        self.fl_id = None
        self.max_bl = None
        self.nrc = None
        self.sec_con = sec_con
        self.uds_security_cal = SecurityAlgorithm(ecu, sec_con=self.sec_con)

    def update_security_constant(self, ecu):
        self.uds_security_cal.update_security_constant(ecu)

    def diagnostic_services_return_p_data(self, sid, get_sub_data):
        sid = sid - 0x40
        self.return_data = [sid] + list(get_sub_data)
        # if sid == Diagnostic_Sid.READDATABYIDENTIFIER:
        #     self.read_data_by_identifier_p_data(get_sub_data)
        # if sid == Diagnostic_Sid.DIAGNOSTICSESSIONCONTROL:
        #     self.diagnostic_session_control_p_data(get_sub_data)
        # elif sid == Diagnostic_Sid.TESTERPRESENT:
        #     self.tester_present_p_data(get_sub_data)    
        # elif sid == Diagnostic_Sid.WRITEDATABYIDENTIFIER:
        #     self.write_data_by_identifier_p_data(get_sub_data)
        # elif sid == Diagnostic_Sid.ECURESET:
        #     self.ecu_reset(get_sub_data)
        # elif sid == Diagnostic_Sid.READDTCINFORMATION:
        #     self.read_dtc_information(get_sub_data)
        # elif sid == Diagnostic_Sid.CLEARDIAGNOSTICINFORMATION:
        #     self.clear_diagnostic_information(get_sub_data)
        if sid == Diagnostic_Sid.SECURITYACCESS:
            self.security_access_p_data(get_sub_data)
        elif sid == Diagnostic_Sid.REQUESTDOWNLOAD:
            self.requestdownload(get_sub_data)  
        # elif sid == Diagnostic_Sid.ROUTINECONTROL:
        #     self.routine_control(get_sub_data)    
        else:
            self.p_data = None
            
    def requestdownload(self, get_sub_data):
        self.fl_id = get_sub_data[0]
        max_bl_length = self.fl_id >> 4
        if max_bl_length == len(get_sub_data[1:]):
            self.max_bl = int.from_bytes(get_sub_data[1:], "big")
        else:
            logger.error("the length of max_bl is error" )

    def read_data_by_identifier_p_data(self,get_sub_data):
        # SID is 0x22
        sid = Diagnostic_Sid.READDATABYIDENTIFIER
        sub_id = [get_sub_data[0],get_sub_data[1]]
        if isinstance(self.data_info,dict):
            data_key = ((hex((sub_id[0] << 8)+sub_id[1]))[2:]).upper()
            if len(data_key) < 4 :
                data_key = "0"*(4 - len(data_key)) + data_key
            if isinstance(self.data_info[data_key], str):
                self.p_data = [sid + 0x40] + sub_id +  list(bytes(self.data_info[data_key],"ascii"))
            elif isinstance(self.data_info[data_key], list):
                self.p_data = [sid + 0x40] + sub_id +  self.data_info[data_key]
        elif isinstance(self.data_info,list):
            self.p_data = [sid + 0x40] + sub_id + self.data_info
        # logger.info(self.p_data)
        
    def diagnostic_session_control_p_data(self,get_sub_data):
        # SID is 0x10
        sid = Diagnostic_Sid.DIAGNOSTICSESSIONCONTROL
        sub_id = get_sub_data[0]
        
        # Timing P2server value is provided in 1ms resolution  (0x32)
        # Timing P2*server value is provided in 10ms resolution  (0xC8)
        self.p_data = [sid + 0x40] + [sub_id] + [0x00,0x32,0x00,0xC8]
        self.diagnostic_session = sid
        if sid != 0x01:
            if self.non_default_diagnostic_session_flag:
                self.non_default_diagnostic_session_time = 0
            else:
                self.non_default_diagnostic_session = Thread(target=self.non_default_diagnostic_session_5s)
                self.non_default_diagnostic_session.start()
                self.non_default_diagnostic_session_flag = True
                logger.info("enter non default diagnostic session")
        else :
            self.non_default_diagnostic_session_time = 5
            logger.info("enter default diagnostic session")
        
    def non_default_diagnostic_session_5s(self):
        while self.non_default_diagnostic_session_time < 5:
            sleep(0.1)
            self.non_default_diagnostic_session_time += 0.1
        self.diagnostic_session = 0x10
        self.non_default_diagnostic_session_flag = False
        self.non_default_diagnostic_session_time = 0
        logger.info("exit non default diagnostic session")
    
    def tester_present_p_data(self,get_sub_data):
        # SID is 0x3E
        sid = Diagnostic_Sid.TESTERPRESENT
        sub_id = get_sub_data[0]
        if sub_id == 0x80:
            self.non_default_diagnostic_session_time = 0
            logger.info("receive keeping session")
        else:
            self.p_data = [sid + 0x40] + [sub_id]

    def get_securityaccessLevel(self, sub_id):
        if sub_id in [0x01,0x02]:
            securityaccessLevel = 0x01
            return securityaccessLevel
        elif sub_id in [0x03,0x04]:
            securityaccessLevel = 0x02
            return securityaccessLevel
        elif sub_id in [0x05,0x06]:
            securityaccessLevel = 0x03
            return securityaccessLevel
        elif sub_id in [0x07,0x08]:
            securityaccessLevel = 0x04
            return securityaccessLevel
        elif sub_id in [0x09,0x0A]:
            securityaccessLevel = 0x05
            return securityaccessLevel
        elif sub_id in [0x11,0x12]:
            securityaccessLevel = 0x06
            return securityaccessLevel
        elif sub_id in [0x19,0x1A]:
            securityaccessLevel = 0x07
            return securityaccessLevel
        elif sub_id in [0x5F,0x60]:
            securityaccessLevel = 0x08
            return securityaccessLevel

    def security_access_p_data(self, get_sub_data):
        # SID is 0x27
        sid = Diagnostic_Sid.SECURITYACCESS
        sub_id = get_sub_data[0]
        if sub_id in [0x01,0x03,0x05,0x07,0x09,0x11,0x19,0x5F]:
            if sub_id in [0x07,0x09]:
                self.seed = get_sub_data[1:17]
            else:
                self.seed = get_sub_data[1:4]
            candidateSecurityAccessLevel = self.get_securityaccessLevel(sub_id)
            calculatedKey = self.uds_security_cal.get_calculated_key(candidateSecurityAccessLevel, self.seed)
            calculatedKey = list(calculatedKey)
            self.p_data = [sid] + [sub_id + 0x01] + calculatedKey
        elif sub_id in [0x02,0x04,0x06,0x08,0x0A,0x1A,0x60]:
            candidateSecurityAccessLevel = self.get_securityaccessLevel(sub_id)
            self.p_data = None
            
    def crc8(self, data):
        t_crc = 0xFF
        i = 0
        SEED_LENGTH = 6
        while i < SEED_LENGTH:
            t_crc ^= data[i]
            b = 0
            while b < 8:
                if (t_crc & 0x80) != 0:
                    t_crc <<= 1
                    t_crc ^= 0x11D
                else:
                    t_crc <<= 1
                b += 1
            i += 1
        return ~t_crc

    def write_data_by_identifier_p_data(self,get_sub_data):
        # SID is 0x2E
        # self.data_info is dict
        # The specific relationship between did and non_default_diagnostic_session  will be updated later
        sid = Diagnostic_Sid.WRITEDATABYIDENTIFIER
        if self.non_default_diagnostic_session:
            sub_id = [get_sub_data[0],get_sub_data[1]]
            data_key = ((hex((sub_id[0] << 8)+sub_id[1]))[2:]).upper()
            if len(data_key) < 4 :
                data_key = "0"*(4 - len(data_key)) + data_key
            data = get_sub_data[2:]
            self.data_info[data_key] = data
            self.p_data = [sid + 0x40] + sub_id
        else:
            self.p_data = [0x7F,sid,0x22]     # Negative response
            logger.error("ECU is not in non_default_diagnostic_session ; NRC (0x22) :conditions Not Correct")
            
    def ecu_reset(self,get_sub_data):
        # SID is 0x11
        sid = Diagnostic_Sid.ECURESET
        sub_id = get_sub_data[0]
        self.p_data = [sid + 0x40] + [sub_id]
        
    def read_dtc_information(self,get_sub_data):
        # SID is 0x19
        dtc_status_availability_mask = [0x0F]
        sid = Diagnostic_Sid.READDTCINFORMATION
        sub_id = get_sub_data[0]
        self.all_dtc_code_data = []  
        if sub_id == 0x0A :
            for dtc_code_data in self.dtc_code.values():
                self.all_dtc_code_data = self.all_dtc_code_data + dtc_code_data
            self.p_data = [sid + 0x40] + [sub_id] + dtc_status_availability_mask + self.all_dtc_code_data
        elif sub_id == 0x01 :
            # provisional  dtc_status_availability_mask is 0x0F
            # DTCFormatIdentifier is ISO15031-6DTCFormat (0x00)
            dtc_format_identifier = [0x00]
            dtc_status_mask = get_sub_data[1]
            i = 0
            for dtc_code_data in self.dtc_code.values():
                if (dtc_code_data[-1:] & 0x0F & dtc_status_mask) :
                    i += 1
            dtc_count_h = i >> 8
            dtc_count_l = i & 0xFF
            dtc_count = [dtc_count_h] + [dtc_count_l]
            self.p_data = [sid + 0x40] + [sub_id] + dtc_status_availability_mask + dtc_format_identifier + dtc_count 
        elif sub_id == 0x02 :
            # provisional  dtc_status_availability_mask is 0x0F
            dtc_status_mask = get_sub_data[1]
            dtc_and_status_record = []
            for dtc_code_data in self.dtc_code.values():
                if (dtc_code_data[-1] & 0x0F & dtc_status_mask) :
                    dtc_and_status_record = dtc_and_status_record + dtc_code_data
            self.p_data = [sid + 0x40] + [sub_id] + dtc_status_availability_mask + dtc_and_status_record
    
    def clear_diagnostic_information(self,get_sub_data):
        # SID is 0x14
        sid = Diagnostic_Sid.CLEARDIAGNOSTICINFORMATION
        sub_id = list(get_sub_data)
        if sub_id == [0xFF, 0xFF, 0xFF] :
            self.p_data = [sid + 0x40]
        else:
            self.p_data = [0x7F, 0x14, 0x31]
            logger.error("{} is request out range".format(sub_id))
            
    def routine_control(self,get_sub_data):
        # SID is 0x31
        sid = Diagnostic_Sid.ROUTINECONTROL
        routine_type = get_sub_data[0]
        rid = list(get_sub_data[1:3])

        data_key = ((hex((rid[0] << 8)+rid[1]))[2:]).upper()
        if len(data_key) < 4 :
            data_key = "0"*(4 - len(data_key)) + data_key
        rid_keys = self.routine_control_p_data.keys()
        if data_key in rid_keys:
            routine_type_keys = self.routine_control_p_data[data_key].keys()
            if routine_type in routine_type_keys :
                self.p_data = [sid + 0x40] + [routine_type] + rid + self.routine_control_p_data[data_key][routine_type]
            else :
                self.p_data = [sid + 0x40] + [routine_type] + rid
        else :
            self.p_data = [sid + 0x40] + [routine_type] + rid
                    
            
                
            
            

            
            
                    
            
            
        


            

        
            

            
    
            
        
            
            
        
