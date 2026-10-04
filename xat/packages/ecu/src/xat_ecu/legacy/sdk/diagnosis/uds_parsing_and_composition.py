# -*- coding: utf-8 -*-
"""
@File        : uds_parsing_and_composition.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021-08-23 09:59
@Description : 
"""

import sys
import os
from typing import Tuple, Union
from xat_ecu.legacy.sdk.diagnosis import *
from xat_ecu.legacy.sdk.diagnosis.uds_const import *
from xat_ecu.legacy.common.logger import *
from xat_ecu.legacy.sdk.diagnosis.uds_data import *


def get_key_from_value(service_dict: dict, service_value: int):
    service_list = []
    for service_key in service_dict.keys():
        if service_dict.get(service_key) == service_value:
            service_list.append(service_key)
    return service_list

def intlist_to_int(intlist:list):
    byte_data = bytes(intlist)
    int_data = int.from_bytes(byte_data, byteorder="big", signed=False)
    return int_data

def raw_data_to_physical_value(raw_data:list, service_struct:list):
    param_data = []
    service_struct_length = len(service_struct)
    if service_struct_length == 1:
        return param_data
    elif service_struct_length > 1:
        for i in range(1, service_struct_length):
            if isinstance(service_struct[i], int):
                value_raw = raw_data[i]
                value_struct = service_struct[i]
                if value_raw != value_struct:
                    break
            elif isinstance(service_struct[i], list):
                if isinstance(service_struct[i][0], int):
                    byte_start = service_struct[i][0]
                    byte_length = service_struct[i][1]
                    byte_end = byte_start + byte_length
                    value_raw = raw_data[byte_start: byte_end]
                    if isinstance(service_struct[i][2], dict):
                        value = intlist_to_int(value_raw)
                        value_key = get_key_from_value(service_struct[i][2], value)
                        param_data.append(value_key)
                    elif (service_struct[i][2] == "A_UNICODE2STRING" and
                          service_struct[i][3] == "IDENTICAL"):
                        value_byte = bytes(value_raw)
                        value = value_byte.decode(encoding="utf-8")
                        param_data.append(value)
                    else:
                        logger.error("=============  To Do  ===============")
                        break
                else:
                    logger.error(" ================ TO DO =================")
                    break
            return param_data

# To Do
class UdsParsingComposition:
    def __init__(self):
        pass

    # DIAG-SERVICE
    def sessions_start(self, message_type: Union[str, int], subfunction):
        # :message_type  such as "REQUEST", "POS-RESPONSE", "NEG-RESPONSE",  0,  1,  2
        # "REQUEST" ----  0
        # "POS-RESPONSE" ----  1
        # "NEG-RESPONSE" ----  2
        self.message_type = message_type

    # def rq_sessions_start(self, subfunction):
    #     SUBFUNCTION = subfunction
    #     return [Diagnostic_Sid.DIAGNOSTICSESSIONCONTROL, subfunction]
    #
    # def pr_sessions_start(self, subfunction):
    #     return [Diagnostic_Sid.DIAGNOSTICSESSIONCONTROL, subfunction]
    #
    # def nr_sessions_start(self, subfunction):
    #     return [Diagnostic_Sid.DIAGNOSTICSESSIONCONTROL, subfunction]

    def uds_parsing(self, uds_data: list):
        if len(uds_data) >= 1:
            if ValidService.has_value(uds_data[0]):
                # Resquest
                pass
            elif ValidResponse.has_value(uds_data[0]):
                # Response
                if uds_data[0] == ValidResponse.NegativeResponse:
                    # NEG-RESPONSE
                    pass
                elif ValidService.has_value(uds_data[0]):
                    # POS - RESPONSE
                    pass
                else:
                    logger.error("The received data is abnormal and the service does not support it")
        else:
            logger.error("The data received is faulty")


class DiagStruct:
    def __init__(self):
        self.uds_data = Uds_Handle_Data()
        self.diag_data = self.uds_data.diag_data
        self.requests_service_id_dict = self.diag_data.get("REQUESTS")
        self.pos_responses_service_id_dict = self.diag_data.get("POS-RESPONSES")
        self.neg_response_service_id_dict = self.diag_data.get("NEG-RESPONSES")

        self.service_id_dict = self.uds_data.service_id

    def physical_to_raw(self, data, data_struct):
        '''
        :data    type:str    such as:"DefaultSession"
        :data_struct     type:list
        such as
        [
            1,
            8,
            {
                "DefaultSession": 1,
                "ProgrammingSession": 2,
                "ExtendedSession": 3
            }
        ]
        '''
        byte_length = data_struct[1] // 8
        if (data_struct[1] % 8) != 0:
            raise ValueError("Bit length is not a multiple of 8")
        if isinstance(data_struct[2], dict) and len(data_struct) == 3:
            data_value = data_struct[2].get(data)
            data_byte = data_value.to_bytes(byte_length, byteorder='big')
            data_list = list(data_byte)
        elif data_struct[2] =="A_UNICODE2STRING" and data_struct[3]=="IDENTICAL":
            data_byte = bytes(data, encoding="utf8")
            data_list = list(data_byte)
        else:
            raise ValueError("=======================  TO DO  ===============================")
        return data_list

    def composition_data(self, message_type, diag_service, param_data=[]):
        '''
        :message_type      type: str or int
            such as "REQUEST", "POS-RESPONSE", "NEG-RESPONSE",  0,  1,  2
            "REQUEST" ----  0
            "POS-RESPONSE" ----  1
            "NEG-RESPONSE" ----  2

        :diag_service      type: str
            such as   "RQ_FaultMemory_ReadNumber", "RQ_FaultMemory_ReadAllIdentified"...

        :param_data    type: list
            such as   [[0xF1, 0x00]]   Follow up data need to be fully supplemented
            such as   ["Vehicle_Configuration"]
        '''
        raw_data = []
        if message_type == "REQUEST" or message_type == 0 or message_type == "POS-RESPONSE" or message_type == 1:
            data_struct_list = self.requests_service_id_dict.get(diag_service)
            length = len(param_data)
            struct_num = 0
            diag_service_id = data_struct_list[struct_num]
            raw_data.append(diag_service_id)
            if diag_service_id is None:
                raise ValueError("diag_service is non-existent")
            struct_num += 1
            if isinstance(data_struct_list[struct_num], int):
                raw_data.append(data_struct_list[struct_num])
                struct_num += 1
            if length <= (len(data_struct_list) - struct_num):
                for data in param_data:
                    if isinstance(data, list):
                        raw_data += data
                        struct_num += 1
                    if isinstance(data_struct_list[struct_num], int):
                        raw_data.append(data_struct_list[struct_num])
                        struct_num += 1
                    elif isinstance(data_struct_list[struct_num], list):
                        data_list = self.physical_to_raw(data, data_struct_list[struct_num])
                        raw_data += data_list
                    elif isinstance(data_struct_list[struct_num], dict):
                        data_dict_value = data_struct_list[struct_num].get(data_struct_list[struct_num-1])
                        data_list = self.physical_to_raw(data, data_dict_value)
                        raw_data += data_list
            else:
                raise ValueError("Input param_data error")
        # elif message_type == "POS-RESPONSE" or message_type == 1:
        #     data_struct_list = self.requests_service_id_dict.get(diag_service)
        #     length = len(param_data)
        #     struct_num = 0
        #     diag_service_id = data_struct_list[struct_num]
        #     raw_data.append(diag_service_id)
        #     if diag_service_id is None:
        #         raise ValueError("diag_service is non-existent")
        #     struct_num += 1
        #     if isinstance(data_struct_list[struct_num], int):
        #         raw_data.append(data_struct_list[struct_num])
        #         struct_num += 1
        #     if length == (len(data_struct_list) - struct_num):
        #         for data in param_data:
        #             if isinstance(data, list):
        #                 raw_data += data
        #                 struct_num += 1
        #             else:
        #                 data_list = self.physical_to_raw(data, data_struct_list[struct_num])
        #                 raw_data += data_list
        #     else:
        #         raise ValueError("Input param_data error")
        elif message_type == "NEG-RESPONSE" or message_type == 2:
            raw_data.append(ValidResponse.NegativeResponse)
            data_struct_list = self.requests_service_id_dict.get(diag_service)
            diag_service_id = data_struct_list[1]
            raw_data.append(diag_service_id)
            if diag_service_id is None:
                raise ValueError("diag_service is non-existent")
            if isinstance(param_data[0], list):
                raw_data += param_data
            elif isinstance(param_data[0], str):
                nrc = NegativeResponseCode.getattr(param_data[0])
                raw_data.append(nrc)
        return raw_data

    def parsing_data(self, raw_data: list):
        '''
        :raw_data    type: list    such as [10, 03]  UDS data
        '''
        length = len(raw_data)
        if length >= 1:
            if ValidService.has_value(raw_data[0]):
                # Resquest
                message_type = "Resquest"
                sid = raw_data[0]
                service_list = get_key_from_value(self.service_id_dict.get("REQUESTS"), sid)
                for service in service_list:
                    service_struct = self.requests_service_id_dict.get(service)
                    param_data = raw_data_to_physical_value(raw_data, service_struct)
                    if param_data is not None:
                        break
                return [message_type, service, param_data]
            elif ValidResponse.has_value(raw_data[0]):
                # Response
                if raw_data[0] == ValidResponse.NegativeResponse:
                    # NEG-RESPONSE
                    message_type = "NEG-RESPONSE"
                    for diag in self.neg_response_service_id_dict.keys():
                        if raw_data[1] == self.neg_response_service_id_dict.get(diag)[1]:
                            diag_service = diag
                            break
                    param_struct = self.neg_response_service_id_dict.get(diag_service)[2]
                    nrc = NegativeResponseCode.return_key(raw_data[2])
                    return [message_type, diag_service, nrc]
                else:
                    # POS - RESPONSE
                    message_type = "POS-RESPONSE"
                    sid = raw_data[0]
                    service_list = get_key_from_value(self.service_id_dict.get("POS-RESPONSE"), sid)
                    for service in service_list:
                        service_struct = self.requests_service_id_dict.get(service)
                        param_data = raw_data_to_physical_value(raw_data, service_struct)
                        if param_data is not None:
                            break
                    return [message_type, service, param_data]
            else:
                logger.error("The received data is abnormal and the service does not support it; "
                             "data is {}".format(raw_data))
        else:
            logger.error("The data received is faulty, the data is {}".format(raw_data))

    def requests_struct(self, uds_data_raw_input=[]):
        '''
        :uds_data_dict_input    such as ["RQ_Sessions_Start","DefaultSession"]
        Display status
            {"RQ_Sessions_Start":
                {
                "SERVICE-ID":0x10,
                "SUBFUNCTION":0x01
                }
            }
        :uds_data_list_input     such as   [0x10, 0x01]
        '''

        if uds_data_raw_input:
            sid = uds_data_raw_input[0]
            diag_name_list = get_key_from_value(self.requests_service_id_dict, sid)
            if len(diag_name_list) == 1:
                pass
            elif len(diag_name_list) >= 1:
                subid = uds_data_raw_input[1]
                # if subid
            elif diag_name_list == []:
                logger.error("Diagnostic service received out of test")

if __name__=="__main__":
    a = DiagStruct()
    # printb = a.parsing_data([0x7F, 0x10, 0x22])
    printb = a.composition_data(0, "RQ_Upload_Download_RequestDownload", [0x11])
    print(printb)
    print("1111111111111_____--end__________")

    # uds_data = Uds_Handle_Data()
    # diag_data = uds_data.diag_data
    # requests_service_id_dict = diag_data.get("REQUESTS")
    # pos_responses_service_id_dict = diag_data.get("POS-RESPONSES")
    # neg_response_service_id_dict = diag_data.get("NEG-RESPONSES")

    # @classmethod
    # def requests_struct(cls, uds_data_physical_input=[], uds_data_raw_input=[]):
    #     '''
    #     :uds_data_dict_input    such as ["RQ_Sessions_Start","DefaultSession"]
    #     Display status
    #         {"RQ_Sessions_Start":
    #             {
    #             "SERVICE-ID":0x10,
    #             "SUBFUNCTION":0x01
    #             }
    #         }
    #     :uds_data_list_input     such as   [0x10, 0x01]
    #     '''
    #
    #     if uds_data_physical_input:
    #         service_id = cls.requests_service_id_dict.get(uds_data_physical_input[0])
    #         uds_data_display = {uds_data_physical_input[0]:
    #                                 {
    #                                     "SERVICE-ID": service_id,
    #                                     "SUBFUNCTION": uds_data_physical_input[1]
    #                                 }}
    #         return_data = [service_id, uds_data_physical_input[1]]
    #         return  return_data
    #     elif uds_data_raw_input:
    #         sid = uds_data_raw_input[0]
    #         diag_name_list = get_key_from_value(cls.requests_service_id_dict, sid)
    #         if len(diag_name_list) == 1:
    #             pass
    #         elif len(diag_name_list) >= 1:
    #             subid = uds_data_raw_input[1]
    #             # if subid
    #         elif diag_name_list == []:
    #             logger.error("Diagnostic service received out of test")


