# -*- coding: utf-8 -*-
"""
@File        : uds_server_odx.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022-02-07 23:59
@Description : 
"""

from termios import TIOCSERSETMULTI
import time
import errno
import subprocess
import threading
from threading import Thread
from copy import deepcopy
from webbrowser import get
import can
from time import sleep
from enum import IntEnum
from random import randint
from xat_ecu.legacy.sdk.diagnosis.aes_128_cbc import Aes128
from xat_ecu.legacy.sdk.diagnosis.uds_securitycal import SecurityAlgorithm
from xat_ecu.legacy.common.data_type_handing import *
from xat_ecu.legacy.sdk.diagnosis.aes_128_cbc import bcc_check
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common import exception_error
from xat_ecu.legacy.common.error_code import StatusCode
from xat_ecu.legacy.common.exception_error import error_check
from xat_ecu.legacy.utils.utils import struct_pretty


@staticmethod
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


class Diagnostic_Sid(IntEnum):
    DIAGNOSTICSESSIONCONTROL = 0x10
    ECURESET = 0x11
    CLEARDIAGNOSTICINFORMATION = 0x14
    READDTCINFORMATION = 0x19
    READDATABYIDENTIFIER = 0x22
    SECURITYACCESS = 0x27
    COMMUNICATIONCONTROL = 0x28
    WRITEDATABYIDENTIFIER = 0x2E
    INPUTOUTPUTCONTROLBYIDENTIFIER = 0x2F
    ROUTINECONTROL = 0x31
    REQUESTDOWNLOAD = 0x34
    TRANSFERDATA = 0x36
    REQUESTTRANSFEREXIT = 0x37
    REQUESTFILETRANSFER = 0x38
    TESTERPRESENT = 0x3E
    CONTROLDTCSETTINGS = 0x85
    TESTSINGALFRAME = 0x98
    TESTMULITFRAME = 0x99


class MockUdsResponseDataInfo:
    SID_10 = dict()
    SID_11 = dict()
    SID_27 = dict()
    SID_34: Union[list, dict] = None
    SID_36 = dict()
    SID_37 = None


class Uds_Server_Odx:
    def __init__(self, ecu, sec_con={}, mock_uds_data=MockUdsResponseDataInfo):
        self.mock_uds_data = mock_uds_data
        self.non_default_diagnostic_session_flag = None
        self.non_default_diagnostic_session_time = 5
        self.ecu = ecu
        self.f186 = 0x01
        self.sec_con = sec_con

    def diagnostic_services_n_data(self):
        self.n_data = [0x7F] + [self.sid] + self.nrc_code
        # logger.info(self.n_data)

    # def unified_reply_logic_data(self, sid, data_key=None):
    #     """
    #     肯定响应和否定响应的逻辑都在其中；
    #     有数据，按照数据回复，没有，则使用默认回复；
    #     目前只适配了0x22服务
    #     """
    #     if self.data_info and isinstance(self.data_info, dict):
    #         data_value = self.data_info.get(data_key, None)
    #         if isinstance(data_value, list):
    #             data = data_value
    #             return data
    #         elif isinstance(data_value, dict):
    #             # such as {"NRC" : 0x22}
    #             data = data_value.get("NRC")
    #             if data is None:
    #                 data = 0x22
    #             return [0x7F, sid, data]
    #     logger.info("没有预设值，这边使用默认值 0")
    #     data = [0x00]
    #     return data
    
    def diagnostic_services_p_data(self, sid, get_sub_data):
        if sid == Diagnostic_Sid.READDATABYIDENTIFIER:
            self.read_data_by_identifier_p_data(get_sub_data)
        elif sid == Diagnostic_Sid.DIAGNOSTICSESSIONCONTROL:
            self.diagnostic_session_control_p_data(get_sub_data)
        elif sid == Diagnostic_Sid.TESTERPRESENT:
            self.tester_present_p_data(get_sub_data)
        elif sid == Diagnostic_Sid.SECURITYACCESS:
            self.security_access_p_data(get_sub_data)
        elif sid == Diagnostic_Sid.WRITEDATABYIDENTIFIER:
            self.write_data_by_identifier_p_data(get_sub_data)
        elif sid == Diagnostic_Sid.ECURESET:
            self.ecu_reset(get_sub_data)
        elif sid == Diagnostic_Sid.COMMUNICATIONCONTROL:
            self.communication_control(get_sub_data)
        elif sid == Diagnostic_Sid.CONTROLDTCSETTINGS:
            self.control_dtc_settings(get_sub_data)
        elif sid == Diagnostic_Sid.READDTCINFORMATION:
            self.read_dtc_information(get_sub_data)
        elif sid == Diagnostic_Sid.CLEARDIAGNOSTICINFORMATION:
            self.clear_diagnostic_information(get_sub_data)
        elif sid == Diagnostic_Sid.ROUTINECONTROL:
            self.routine_control(get_sub_data)
        elif sid == Diagnostic_Sid.REQUESTDOWNLOAD:
            self.request_download(get_sub_data)
        elif sid == Diagnostic_Sid.TRANSFERDATA:
            self.transfer_data(get_sub_data)
        elif sid == Diagnostic_Sid.REQUESTTRANSFEREXIT:
            self.request_transfer_exit(get_sub_data)
        elif sid == Diagnostic_Sid.REQUESTFILETRANSFER:
            self.request_file_transfer(get_sub_data)
        elif sid == Diagnostic_Sid.TESTSINGALFRAME:
            self.test_singal_frame(get_sub_data)
        elif sid == Diagnostic_Sid.TESTMULITFRAME:
            self.test_multi_frame(get_sub_data)
        elif sid == Diagnostic_Sid.INPUTOUTPUTCONTROLBYIDENTIFIER:
            self.input_output_control(get_sub_data)
        else:
            # serviceNotSupported (NRC is 0x11)
            self.p_data = [0x7F, sid, 0x11]
            logger.error("{} serviceNotSupported".format(sid))

    def input_output_control(self, get_sub_data):
        # SID is 0x2F
        sid = Diagnostic_Sid.INPUTOUTPUTCONTROLBYIDENTIFIER
        sub_id = get_sub_data[0]
        # self.p_data = [sid + 0x40] + [sub_id]
        # 目前强行 回复 7f 2f 33
        self.p_data = [0x7F, 0x2F, 0x33]

    def communication_control(self, get_sub_data):
        # SID is 0x28
        sid = Diagnostic_Sid.COMMUNICATIONCONTROL
        sub_id = get_sub_data[0]
        self.p_data = [sid + 0x40] + [sub_id]

    def control_dtc_settings(self, get_sub_data):
        # SID is 0x28
        sid = Diagnostic_Sid.CONTROLDTCSETTINGS
        sub_id = get_sub_data[0]
        self.p_data = [sid + 0x40] + [sub_id]

    def read_data_by_identifier_p_data(self, get_sub_data):
        # SID is 0x22
        sid = Diagnostic_Sid.READDATABYIDENTIFIER
        sub_id = [get_sub_data[0], get_sub_data[1]]

        # 以下为以前逻辑，考虑太细，逻辑过于复杂，建议用上者统一逻辑 unified_reply_logic_data, 目前暂保持现状
        if self.data_info and isinstance(self.data_info, dict):
            data_key = ((hex((sub_id[0] << 8) + sub_id[1]))[2:]).upper()
            if len(data_key) < 4:
                data_key = "0" * (4 - len(data_key)) + data_key
            if self.data_info.get(data_key, None) is None:
                if sub_id == [0xF1, 0xAA]:
                    data = [0x61, 0x60, 0x11, 0x00, 0x50, 0x20, 0x65, 0x65]
                elif sub_id == [0xF1, 0xAE]:
                    data = [0x01, 0x61, 0x60, 0x11, 0x00, 0x50, 0x20, 0x65, 0x65]
                elif sub_id == [0xF1, 0x86]:
                    data = [self.f186]
                else:
                    data = [0x00]
                self.p_data = [sid + 0x40] + sub_id + data
                logger.warning("DID {} 没有获取到更新数据且没有给默认数据，此为固定回复".format(data_key))
            else:
                data_value = self.data_info[data_key]
                if data_value:
                    if isinstance(data_value, dict):
                        # such as {"NRC" : 0x22}
                        if data_value.get("NRC"):
                            if data_value.get("NRC") == "no_reply":
                                self.p_data = []
                            else:
                                with error_check(StatusCode.DOIP_MOCK_DATA_TYPE_ERR, exception_error.DOIPError):
                                    self.p_data = [0x7F] + [sid] + [data_value["NRC"]]
                                    if not isinstance(data_value["NRC"], int):
                                        raise TypeError(f"类型错误")
                        elif data_value.get("F1AE"):
                            sw_num = len(data_value.get("F1AE"))
                            data = []
                            for s in data_value.get("F1AE"):
                                datax = str_to_bcd5_ascii3_list(s)
                                data += datax
                            data = [sw_num] + data
                            self.p_data = [sid + 0x40] + sub_id + data
                        else:
                            logger.error("yaml config data error")
                    elif isinstance(data_value, str):
                        if sub_id in [[0xF1, 0xAA], [0xF1, 0xAB], [0xF1, 0xA0]]:
                            data = str_to_bcd5_ascii3_list(data_value)
                        elif sub_id == [0xF1, 0xAE]:
                            data = str_to_bcd5_ascii3_list(data_value)
                            data = [0x01] + data
                        elif sub_id == [0xF1, 0x8C]:
                            if len(data_value) == 8:
                                b = binascii.a2b_hex(data_value)
                                b_list = list(b)
                                data = b_list
                            else:
                                logger.error("yaml config data error")
                        elif sub_id == [0xED, 0x20]:  # 这个目前可以随意填  such as  "default"
                            s1 = self.data_info.get("F1AA")
                            s2 = self.data_info.get("F1AB")
                            s3 = self.data_info.get("F18C")
                            with error_check(StatusCode.DOIP_MOCK_DATA_TYPE_ERR, exception_error.DOIPError):
                                data1 = str_to_bcd5_ascii3_list(s1)
                                data2 = str_to_bcd5_ascii3_list(s2)
                                data3 = str_to_bcd5_ascii3_list(s3)
                            data = (
                                [0xF1, 0xAA]
                                + data1
                                + [0xF1, 0xAB]
                                + data2
                                + [0xF1, 0x8C]
                                + data3
                            )
                        else:
                            a_list = list(bytes(data_value, "ascii"))
                            data = a_list
                        self.p_data = [sid + 0x40] + sub_id + data
                    elif isinstance(data_value, list):
                        data = data_value
                        self.p_data = [sid + 0x40] + sub_id + data
                else:
                    logger.error("yaml config data error")
        elif self.data_info and isinstance(self.data_info, list):
            self.p_data = [sid + 0x40] + sub_id + self.data_info
        elif self.data_info is None:
            # 做了一些默认
            if sub_id == [0xF1, 0xAA]:
                data = [0x61, 0x60, 0x11, 0x00, 0x50, 0x20, 0x65, 0x65]
            elif sub_id == [0xF1, 0xAE]:
                data = [0x01, 0x61, 0x60, 0x11, 0x00, 0x50, 0x20, 0x65, 0x65]
            elif sub_id == [0xF1, 0x86]:
                data = [self.f186]
            else:
                data = [0x00]
            self.p_data = [sid + 0x40] + sub_id + data
            logger.warning("ECU 没有获取到更新数据且没有给默认数据，此为固定回复")

    def diagnostic_session_control_p_data(self, get_sub_data):
        # SID is 0x10
        sid = Diagnostic_Sid.DIAGNOSTICSESSIONCONTROL
        sub_id = get_sub_data[0]

        # Timing P2server value is provided in 1ms resolution  (0x32)
        # Timing P2*server value is provided in 10ms resolution  (0x1F4)??
        self.p_data = [sid + 0x40] + [sub_id] + [0x00, 0x32, 0x01, 0xF4]
        self.diagnostic_session = sub_id
        if sub_id not in [0x01, 0x81]:
            if sub_id in [0x02, 0x82]:
                self.f186 = 0x02
            elif sub_id in [0x03, 0x83]:
                self.f186 = 0x03

            if self.non_default_diagnostic_session_flag:
                self.non_default_diagnostic_session_time = 0
            else:
                self.non_default_diagnostic_session = Thread(
                    target=self.non_default_diagnostic_session_5s
                )
                self.non_default_diagnostic_session.start()
                logger.info("enter non default diagnostic session")
        else:
            self.f186 = 0x01

            self.non_default_diagnostic_session_flag = False
            self.non_default_diagnostic_session_time = 5
            logger.info("enter default diagnostic session")

        mock_data = self.mock_uds_data.SID_10.get(sub_id)
        if isinstance(mock_data, list):
            self.p_data = [sid + 0x40] + [sub_id] + mock_data

        if isinstance(mock_data, dict):
            if mock_data.get("NRC"):
                if mock_data.get("NRC") == "no_reply":
                    self.p_data = []
                else:
                    with error_check(StatusCode.DOIP_MOCK_DATA_TYPE_ERR, exception_error.DOIPError):
                        self.p_data = [0x7F] + [sid] + [mock_data["NRC"]]
                        if not isinstance(mock_data["NRC"], int):
                            raise TypeError(f"类型错误")

    def non_default_diagnostic_session_5s(self):
        self.non_default_diagnostic_session_flag = True
        self.non_default_diagnostic_session_time = 0
        while self.non_default_diagnostic_session_time < 5:
            sleep(0.01)
            self.non_default_diagnostic_session_time += 0.01
        self.diagnostic_session = 0x01
        self.f186 = 0x01
        self.non_default_diagnostic_session_flag = False
        # logger.info("exit non default diagnostic session")
        logger.info("退出非默认诊断会话")

    def tester_present_p_data(self, get_sub_data):
        # SID is 0x3E
        sid = Diagnostic_Sid.TESTERPRESENT
        sub_id = get_sub_data[0]
        if sub_id == 0x80:
            if self.non_default_diagnostic_session_flag:
                self.non_default_diagnostic_session_time = 0
            # logger.debug("receive keeping session")
            logger.debug("接收到保持会话请求")
            self.p_data = [sid + 0x40] + [sub_id]
        else:
            self.p_data = [sid + 0x40] + [sub_id]

    def get_securityaccessLevel(self, sub_id):
        if sub_id in [0x01, 0x02]:
            securityaccessLevel = 0x01
            return securityaccessLevel
        elif sub_id in [0x03, 0x04]:
            securityaccessLevel = 0x02
            return securityaccessLevel
        elif sub_id in [0x05, 0x06]:
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
        elif sub_id in [0x19, 0x1A]:
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
            if sub_id in [0x07]:
                random64 = os.urandom(16)
                self.seed = list(random64)
            else:
                random3 = os.urandom(3)
                self.seed = list(random3)
                self.seed = [0xA9, 0x19, 0xCE]
            self.p_data = [sid + 0x40] + [sub_id] + self.seed
        elif sub_id in [0x02,0x04,0x06,0x08,0x0A,0x12,0x1A,0x60]:
            if sub_id in [0x08]:
                get_calculatedKey = list(get_sub_data[1:65])
            else:
                get_calculatedKey = list(get_sub_data[1:4])
    
            self.seed.reverse()
            candidateSecurityAccessLevel = self.get_securityaccessLevel(sub_id)
            self.uds_security_cal = SecurityAlgorithm(self.ecu, sec_con=self.sec_con)
            calculatedKey = self.uds_security_cal.get_calculated_key(
                candidateSecurityAccessLevel, self.seed
            )
            calculatedKey = list(calculatedKey)
            logger.info(
                "seed is {0} , calculatedKey is {1}".format(self.seed, calculatedKey)
            )
            if get_calculatedKey == calculatedKey:
                self.p_data = [sid + 0x40] + [sub_id]
            else:
                self.p_data = [sid + 0x40] + [sub_id]
                logger.warning("Force simulation to pass security level")

        mock_data = self.mock_uds_data.SID_27.get(sub_id)
        if isinstance(mock_data, list):
            self.p_data = [sid + 0x40] + [sub_id] + mock_data
        elif isinstance(mock_data, dict):
            if mock_data.get("NRC"):
                if mock_data.get("NRC") == "no_reply":
                    self.p_data = []
                else:
                    with error_check(StatusCode.DOIP_MOCK_DATA_TYPE_ERR, exception_error.DOIPError):
                        self.p_data = [0x7F] + [sid] + [mock_data.get("NRC")]
                        if not isinstance(mock_data["NRC"], int):
                            raise TypeError(f"类型错误")

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

    def write_data_by_identifier_p_data(self, get_sub_data):
        # SID is 0x2E
        # self.data_info is dict
        # The specific relationship between did and non_default_diagnostic_session  will be updated later
        sid = Diagnostic_Sid.WRITEDATABYIDENTIFIER
        sub_id = [get_sub_data[0], get_sub_data[1]]
        if self.non_default_diagnostic_session_flag:
            sub_id = [get_sub_data[0], get_sub_data[1]]
            data_key = ((hex((sub_id[0] << 8) + sub_id[1]))[2:]).upper()
            if len(data_key) < 4:
                data_key = "0" * (4 - len(data_key)) + data_key
            data = get_sub_data[2:]
            if isinstance(self.data_info, dict):
                self.data_info[data_key] = data
            self.p_data = [sid + 0x40] + sub_id
        else:
            with error_check(StatusCode.DOIP_SESSION_ERR, exception_error.DOIPError):
                self.p_data = [0x7F, sid, 0x22]  # Negative response
                logger.warning(f"当前会话等级错误")
            # logger.error(
            #     "ECU is not in non_default_diagnostic_session ; NRC (0x22) :conditions Not Correct"
            # )

    def ecu_reset(self, get_sub_data):
        # SID is 0x11
        sid = Diagnostic_Sid.ECURESET
        sub_id = get_sub_data[0]
        self.p_data = [sid + 0x40] + [sub_id]

        mock_data = self.mock_uds_data.SID_11.get(sub_id)
        if isinstance(mock_data, list):
            self.p_data = [sid + 0x40] + mock_data
        elif isinstance(mock_data, dict):
            if mock_data.get("NRC"):
                if mock_data.get("NRC") == "no_reply":
                    self.p_data = []
                else:
                    with error_check(StatusCode.DOIP_MOCK_DATA_TYPE_ERR, exception_error.DOIPError):
                        self.p_data = [0x7F] + [sid] + [mock_data.get("NRC")]
                        if not isinstance(mock_data["NRC"], int):
                            raise TypeError(f"类型错误")
            else:
                logger.error("yaml config data error")

    def read_dtc_information(self, get_sub_data):
        # SID is 0x19
        dtc_status_availability_mask = [0x0F]
        sid = Diagnostic_Sid.READDTCINFORMATION
        sub_id = get_sub_data[0]
        self.all_dtc_code_data = []
        if sub_id == 0x0A:
            if isinstance(self.dtc_code, dict):
                for dtc_code_data in self.dtc_code.values():
                    if isinstance(dtc_code_data, list):
                        self.all_dtc_code_data = self.all_dtc_code_data + dtc_code_data
                    else:
                        logger.warning("预置的 dtc码 格式有误")
            self.p_data = (
                [sid + 0x40]
                + [sub_id]
                + dtc_status_availability_mask
                + self.all_dtc_code_data
            )
        elif sub_id == 0x01:
            # provisional  dtc_status_availability_mask is 0x0F
            # DTCFormatIdentifier is ISO15031-6DTCFormat (0x00)
            dtc_format_identifier = [0x00]
            dtc_status_mask = get_sub_data[1]
            i = 0
            if isinstance(self.dtc_code, dict):
                for dtc_code_data in self.dtc_code.values():
                    if isinstance(dtc_code_data, list):
                        if dtc_code_data[-1:] & 0x0F & dtc_status_mask:
                            i += 1
                    else:
                        logger.warning("预置的 dtc码 格式有误")
            dtc_count_h = i >> 8
            dtc_count_l = i & 0xFF
            dtc_count = [dtc_count_h] + [dtc_count_l]
            self.p_data = (
                [sid + 0x40]
                + [sub_id]
                + dtc_status_availability_mask
                + dtc_format_identifier
                + dtc_count
            )
        elif sub_id == 0x02:
            # provisional  dtc_status_availability_mask is 0x0F
            dtc_status_mask = get_sub_data[1]
            dtc_and_status_record = []
            if isinstance(self.dtc_code, dict):
                for dtc_code_data in self.dtc_code.values():
                    if isinstance(dtc_code_data, list):
                        if dtc_code_data[-1] & 0x0F & dtc_status_mask:
                            dtc_and_status_record = dtc_and_status_record + dtc_code_data
                    else:
                        logger.warning("预置的 dtc码 格式有误")
            self.p_data = (
                [sid + 0x40]
                + [sub_id]
                + dtc_status_availability_mask
                + dtc_and_status_record
            )

    def clear_diagnostic_information(self, get_sub_data):
        # SID is 0x14
        sid = Diagnostic_Sid.CLEARDIAGNOSTICINFORMATION
        sub_id = list(get_sub_data)
        if sub_id == [0xFF, 0xFF, 0xFF]:
            self.p_data = [sid + 0x40]
        else:
            self.p_data = [0x7F, 0x14, 0x31]
            # logger.warning("{} is request out range".format(sub_id))
            logger.warning("{} 请求超出范围".format(sub_id))

    def routine_control(self, get_sub_data):
        # SID is 0x31
        sid = Diagnostic_Sid.ROUTINECONTROL
        routine_type = get_sub_data[0]
        rid = list(get_sub_data[1:3])

        data_key = ((hex((rid[0] << 8) + rid[1]))[2:]).upper()
        if len(data_key) < 4:
            data_key = "0" * (4 - len(data_key)) + data_key
        if self.ecu == 'ETCM' and data_key == 'A7A0':
            self.routine_control_specified_for_etcm_a7a0(get_sub_data)
            return
        if isinstance(self.routine_control_p_data, dict):
            rid_keys = self.routine_control_p_data.keys()
            if data_key in rid_keys:
                routine_type_keys = self.routine_control_p_data[data_key].keys()
                if routine_type in routine_type_keys:
                    if isinstance(self.routine_control_p_data[data_key][routine_type], dict):
                        if self.routine_control_p_data[data_key][routine_type].get("NRC") == "no_reply":
                            self.p_data = []
                        else:
                            self.p_data = [0x7F, sid, self.routine_control_p_data[data_key][routine_type]["NRC"]]
                    elif isinstance(self.routine_control_p_data[data_key][routine_type], list):
                        self.p_data = (
                            [sid + 0x40]
                            + [routine_type]
                            + rid
                            + self.routine_control_p_data[data_key][routine_type]
                        )
                    else:
                        logger.warning("没有预置的routine_control格式不符合规范，使用默认回复")
                        self.p_data = [sid + 0x40] + [routine_type] + rid
                else:
                    self.p_data = [sid + 0x40] + [routine_type] + rid
            else:
                logger.warning("没有预置的routine_control格式不符合规范，使用默认回复")
                add_list = []
                if routine_type in [0x00, 0x01]:
                    if rid == [0x40, 0x00]:
                        add_list = [0x10, 0x01]
                    elif rid == [0x42, 0x89]:
                        add_list = [0x10, 0x01]
                    elif rid == [0xA1, 0x00]:
                        add_list = [0x10, 0x00]
                    elif rid == [0xA1, 0x01]:
                        add_list = [0x10, 0x00]
                    elif rid == [0xA1, 0x02]:
                        add_list = [0x01]
                    elif rid == [0x02, 0x06]:
                        add_list = [0x10, 0x01]
                    elif rid == [0x02, 0x12]:
                        add_list = [0x10, 0x00]
                    elif rid == [0x03, 0x01]:
                        add_list = [0x01]
                    elif rid == [0xFF, 0x00]:
                        add_list = [0x10]
                    elif rid == [0x02, 0x08]:
                        add_list = [0x10]
                    elif rid == [0x02, 0x05]:
                        add_list = [0x10, 0x00, 0x00, 0x00, 0x00]
                self.p_data = [sid + 0x40] + [routine_type] + rid + add_list
        else:
            logger.warning("预置的routine_control格式不符合规范，使用默认回复")
            add_list = []
            if routine_type in [0x00, 0x01]:
                if rid == [0x40, 0x00]:
                    add_list = [0x10, 0x01]
                elif rid == [0x42, 0x89]:
                    add_list = [0x10, 0x01]
                elif rid == [0xA1, 0x00]:
                    add_list = [0x10, 0x00]
                elif rid == [0xA1, 0x01]:
                    add_list = [0x10, 0x00]
                elif rid == [0xA1, 0x02]:
                    add_list = [0x01]
                elif rid == [0x02, 0x06]:
                    add_list = [0x10, 0x01]
                elif rid == [0x02, 0x12]:
                    add_list = [0x10, 0x00]
                elif rid == [0x03, 0x01]:
                    add_list = [0x01]
                elif rid == [0xFF, 0x00]:
                    add_list = [0x10]
                elif rid == [0x02, 0x08]:
                    add_list = [0x10]
                elif rid == [0x02, 0x05]:
                    add_list = [0x10, 0x00, 0x00, 0x00, 0x00]
            self.p_data = [sid + 0x40] + [routine_type] + rid + add_list

    def request_download(self, get_sub_data):
        # SID is 0x34
        # LengthFormatIdentifier
        # MaxNumberOfBlockLength
        sid = Diagnostic_Sid.REQUESTDOWNLOAD

        # 包比较大的 一般doip
        # length_format_identifier = [0x40]
        # Mmx_number_of_block_length = [0x00, 0x01, 0x90, 0x00]

        # 包较小的 一般doip
        length_format_identifier = [0x20]
        Mmx_number_of_block_length = [0x0F, 0xA2]
        self.p_data = (
            [sid + 0x40] + length_format_identifier + Mmx_number_of_block_length
        )

        if self.mock_uds_data.SID_34 and isinstance(self.mock_uds_data.SID_34, dict):
            if self.mock_uds_data.SID_34.get("NRC"):
                if self.mock_uds_data.SID_34.get("NRC") == "no_reply":
                    self.p_data = []
                else:
                    with error_check(StatusCode.DOIP_MOCK_DATA_TYPE_ERR, exception_error.DOIPError):
                        self.p_data = [0x7F] + [sid] + [self.mock_uds_data.SID_34.get("NRC")]
                        if not isinstance(self.mock_uds_data.SID_34["NRC"], int):
                            raise TypeError(f"类型错误")
            else:
                logger.error("yaml config data error")
        elif isinstance(self.mock_uds_data.SID_34, list):
            self.p_data = [sid + 0x40] + self.mock_uds_data.SID_34

    def transfer_data(self, get_sub_data):
        # SID is 0x36
        # bsc is Block Sequence Counter
        sid = Diagnostic_Sid.TRANSFERDATA
        bsc = get_sub_data[0]
        self.p_data = [sid + 0x40] + [bsc]

        if self.mock_uds_data.SID_36.get(bsc):
            if self.mock_uds_data.SID_36.get(bsc) == "no_reply":
                self.p_data = []
            else:
                with error_check(StatusCode.DOIP_MOCK_DATA_TYPE_ERR, exception_error.DOIPError):
                    self.p_data = [0x7F] + [sid] + [self.mock_uds_data.SID_36.get(bsc)]
                    if not isinstance(self.mock_uds_data.SID_36["NRC"], int):
                        raise TypeError(f"类型错误")

    def request_transfer_exit(self, get_sub_data):
        # SID is 0x37
        sid = Diagnostic_Sid.REQUESTTRANSFEREXIT
        self.p_data = [sid + 0x40]

        if isinstance(self.mock_uds_data.SID_37, dict):
            if not self.mock_uds_data.SID_37:
                self.p_data = [sid + 0x40]
            elif self.mock_uds_data.SID_37.get("NRC"):
                if self.mock_uds_data.SID_37.get("NRC") == "no_reply":
                    self.p_data = []
                else:
                    with error_check(StatusCode.DOIP_MOCK_DATA_TYPE_ERR, exception_error.DOIPError):
                        self.p_data = [0x7F] + [sid] + [self.mock_uds_data.SID_37["NRC"]]
                        if not isinstance(self.mock_uds_data.SID_37["NRC"], int):
                            raise TypeError(f"类型错误")
            else:
                logger.error("yaml config data error")

    def request_file_transfer(self, get_sub_data):
        # SID is 0x38
        # modeOfOperation
        # lengthFormatIdentifier
        # MaxNumberOfBlockLength
        # dataFormatIdentifier
        sid = Diagnostic_Sid.REQUESTFILETRANSFER
        mode_of_operation = get_sub_data[0]
        length_format_identifier = [0x04]
        Mmx_number_of_block_length = [0x00, 0x01, 0x90, 0x00]
        data_format_identifier = [0x00]
        self.p_data = (
            [sid + 0x40]
            + [mode_of_operation]
            + length_format_identifier
            + Mmx_number_of_block_length
            + data_format_identifier
        )

    def routine_control_specified_for_etcm_a7a0(self, get_sub_data):
        """
        针对ETCM的RID0xA7A0自定义响应内容
        :param get_sub_data: [01 A7 A0 33 01......]
        :return:
        """
        st = get_sub_data[3]
        sn = get_sub_data[4]
        ctl = get_sub_data[5]
        length = get_sub_data[6]
        data = get_sub_data[7:-1]
        bcc = get_sub_data[-1]
        if st != 0x33:
            raise ValueError("ST字段不符合要求：{}".format(st))
        elif ctl != 0x80:
            raise ValueError("ctl字段不符合要求：{}".format(ctl))
        # elif bcc_check(get_sub_data[4: -1]) != bcc:
        #     raise ValueError("请求指令BCC校验异常{}".format(get_sub_data))
        self.p_data = [0x71, get_sub_data[0], 0xA7, 0xA0, 0x33]
        res_data = [sn, 0x80, 0x0]
        if data == bytearray([0xAE, 0x01, 0xF0]):  # 自定义退出指令
            res_data += [0xBE, 0x00]
        elif data == bytearray([0xA2]):  # 设备握手指令 # todo
            res_data += [0xB2, 0x00, 0x02, 0x00, 0x09]
        elif data[0] in [0xA3, 0xAC, 0xBC]:  # 0xA3: PICC通道，0xBC：ESAM通道
            cmd_type = data[0]
            data_encrypt_type = data[1]  # 数据类型：0-明文数据，1-加密数据，当前全是明文
            cmd_length = data[2] + data[3] << 8
            cmd_data = data[4:]
            if cmd_data[0:5] == bytearray(
                [0x00, 0xA4, 0x00, 0x00, 0x02]
            ):  # SELECT FILE
                res_data += (
                    [cmd_type + 0x10, 0x0, 0x0, 0xC, 0x0]
                    + [0x6F, 0x08, 0x84, 0x01, 0x22, 0xA5, 0x03, 0x88, 0x01, 0x22]
                    + [0x90, 0x00]
                )  # DDF
            elif cmd_data[0:5] == bytearray([0x00, 0x84, 0x00, 0x00, 0x04]):  # 获取随机数
                res_data += [cmd_type + 0x10, 0x0, 0x0, 0x6, 0x0]
                for i in range(4):
                    res_data += [randint(0, 255)]
                res_data += [0x90, 0x00]
            elif cmd_data[0:5] == bytearray([0x00, 0xB0, 0x81, 0x00, 0x3B]) or cmd_data[
                0:5
            ] == bytearray([0x00, 0xB0, 0x95, 0x00, 0x2B]):
                # READ BINARY
                res_data += (
                    [cmd_type + 0x10, 0x0, 0x0, 0x16, 0x0]
                    + [
                        0x11,
                        0x22,
                        0x33,
                        0x44,
                        0x55,
                        0x66,
                        0x77,
                        0x88,
                        0x99,
                        0xAA,
                        0x31,
                        0x32,
                        0x33,
                        0x34,
                        0x35,
                        0x36,
                        0x37,
                        0x38,
                        0x39,
                        0x30,
                    ]
                    + [0x90, 0x00]
                )  # DDF
            elif cmd_data[0:2] == bytearray([0x00, 0xD6]) or cmd_data[0:2] == bytearray(
                [0x04, 0xD6]
            ):  # 写文件指令
                res_data += [cmd_type + 0x10, 0x0, 0x0, 0x2, 0x0, 0x90, 0x00]
            else:
                raise ValueError("请求命令{}, 当前无法响应".format(data))
        res_data[2] = len(res_data) - 3
        self.p_data += res_data + [bcc_check(res_data)]

    def test_singal_frame(self, get_sub_data):
        # SID is 0x98
        # print('get_sub_data=',list(get_sub_data))
        # for i in list(get_sub_data):
        #     print('i.hex()=',hex(i))
        sid = Diagnostic_Sid.TESTSINGALFRAME
        self.p_data = [sid + 0x40]

    def test_multi_frame(self, get_sub_data):
        # SID is 0x99
        sid = Diagnostic_Sid.TESTMULITFRAME
        self.p_data = [sid + 0x40]
