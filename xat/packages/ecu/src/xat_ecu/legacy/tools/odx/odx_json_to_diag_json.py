# -*- coding: utf-8 -*-
"""
@File        : odx_json_to_diag_json.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021-08-25 09:21
@Description :
"""

import sys
import os
from xat_ecu.legacy.common.logger import *
from xat_ecu.legacy.sdk.diagnosis.uds_data import *
import json


class Uds_Complete_Data_Ecu:
    def __init__(self):
        # self.uds_data = Uds_Data()
        # self.uds_data_ecu = Uds_Data_Ecu()
        pass


    # def get_request_service_id_and_diag_name_dict(self):
    #     uds_data_request_dict = self.uds_data.get_request_service_id_and_diag_name_dict()
    #     uds_data_ecu_request_dict = self.uds_data_ecu.get_request_service_id_and_diag_name_dict()
    #     uds_data_request_dict.update(uds_data_ecu_request_dict)
    #     return uds_data_request_dict
    #
    # def get_pos_response_service_id_and_diag_name_dict(self):
    #     uds_data_pos_response_dict = self.uds_data.get_pos_response_service_id_and_diag_name_dict()
    #     uds_data_ecu_pos_response_dict = self.uds_data_ecu.get_pos_response_service_id_and_diag_name_dict()
    #     uds_data_pos_response_dict.update(uds_data_ecu_pos_response_dict)
    #     return uds_data_pos_response_dict
    #
    # def get_neg_response_service_id_and_diag_name_dict(self):
    #     uds_data_neg_response_dict = self.uds_data.get_neg_response_service_id_and_diag_name_dict()
    #     uds_data_ecu_neg_response_dict = self.uds_data_ecu.get_neg_response_service_id_and_diag_name_dict()
    #     uds_data_neg_response_dict.update(uds_data_ecu_neg_response_dict)
    #     return uds_data_neg_response_dict

    # def get_request_struct_and_diag_name_dict(self):
    #     uds_data_request_dict = self.uds_data.get_request_diag_struct_and_diag_name_dict_form_param()
    #     uds_data_ecu_request_dict = self.uds_data_ecu.get_request_diag_struct_and_diag_name_dict_form_param()
    #     uds_data_request_dict.update(uds_data_ecu_request_dict)
    #     return uds_data_request_dict
    #
    # def get_pos_response_struct_and_diag_name_dict(self):
    #     uds_data_pos_response_dict = self.uds_data.get_pos_response_diag_struct_and_diag_name_dict_form_param()
    #     uds_data_ecu_pos_response_dict = self.uds_data_ecu.get_pos_response_diag_struct_and_diag_name_dict_form_param()
    #     uds_data_pos_response_dict.update(uds_data_ecu_pos_response_dict)
    #     return uds_data_pos_response_dict
    #
    # def get_neg_response_struct_and_diag_name_dict(self):
    #     uds_data_neg_response_dict = self.uds_data.get_neg_response_diag_struct_and_diag_name_dict_form_param()
    #     uds_data_ecu_neg_response_dict = self.uds_data_ecu.get_neg_response_diag_struct_and_diag_name_dict_form_param()
    #     uds_data_neg_response_dict.update(uds_data_ecu_neg_response_dict)
    #     return uds_data_neg_response_dict

if __name__=="__main__":
    # work path: compass/

    # sa_uds_data = Uds_Data()
    sa_uds_data = Uds_Data_Ecu()
    sa_request_struct_and_diag_name_dict = sa_uds_data.get_request_diag_struct_and_diag_name_dict_form_param()
    sa_pos_response_struct_and_diag_name_dict = sa_uds_data.get_pos_response_diag_struct_and_diag_name_dict_form_param()
    sa_neg_response_struct_and_diag_name_dict = sa_uds_data.get_neg_response_diag_struct_and_diag_name_dict_form_param()
    sa_uds_data_dict = {"REQUESTS": sa_request_struct_and_diag_name_dict,
                        "POS-RESPONSES": sa_pos_response_struct_and_diag_name_dict,
                        "NEG-RESPONSES": sa_neg_response_struct_and_diag_name_dict}

    sa_diag_path = "./xat_ecu/legacy/sdk/odx_json/diag_json/sa_diag_struct.json"
    with open(sa_diag_path, "w", encoding='utf-8') as f:
        json.dump(sa_uds_data_dict, f, indent=4)
    f.close()
    logger.info("{} File created successfully".format(sa_diag_path))

    sa_request_diag_name_and_id_dict = {}
    sa_pos_response_diag_name_and_id_dict = {}
    sa_neg_response_diag_name_and_id_dict = {}
    for request in sa_request_struct_and_diag_name_dict.keys():
        sa_request_diag_name_and_id_dict[request] = sa_request_struct_and_diag_name_dict.get(request)[0]
    for pos_response in sa_pos_response_struct_and_diag_name_dict.keys():
        sa_pos_response_diag_name_and_id_dict[pos_response] = \
            sa_pos_response_struct_and_diag_name_dict.get(pos_response)[0]
    for neg_response in sa_neg_response_struct_and_diag_name_dict.keys():
        sa_neg_response_diag_name_and_id_dict[neg_response] = \
            sa_neg_response_struct_and_diag_name_dict.get(neg_response)[1]
    sa_uds_service_id_dict = {"REQUESTS": sa_request_diag_name_and_id_dict,
                              "POS-RESPONSES": sa_pos_response_diag_name_and_id_dict,
                              "NEG-RESPONSES": sa_neg_response_diag_name_and_id_dict}
    sa_diag_service_id_path = "./xat_ecu/legacy/sdk/odx_json/diag_json/sa_diag_service_id.json"
    with open(sa_diag_service_id_path, "w", encoding='utf-8') as f:
        json.dump(sa_uds_service_id_dict, f, indent=4)
    f.close()
    logger.info("{} File created successfully".format(sa_diag_service_id_path))

    sa_request_diag_name_and_did_dict = {}
    sa_pos_response_diag_name_and_did_dict = {}
    sa_neg_response_diag_name_and_did_dict = {}
    sa_request_diag_name_and_did_dict["RQ_ODX_ECU_Variant_Version_Number_Read"] = \
        sa_request_struct_and_diag_name_dict.get("RQ_ODX_ECU_Variant_Version_Number_Read")[1][2]
    sa_request_diag_name_and_did_dict["RQ_ECU_Identification_Read"] = \
        sa_request_struct_and_diag_name_dict.get("RQ_ECU_Identification_Read")[1][2]
    sa_request_diag_name_and_did_dict["RQ_Stored_Data_Read"] = \
        sa_request_struct_and_diag_name_dict.get("RQ_Stored_Data_Read")[1][2]
    sa_request_diag_name_and_did_dict["RQ_ECU_Identification_Write"] = \
        sa_request_struct_and_diag_name_dict.get("RQ_ECU_Identification_Write")[1][2]
    sa_request_diag_name_and_did_dict["RQ_Stored_Data_Write"] = \
        sa_request_struct_and_diag_name_dict.get("RQ_Stored_Data_Write")[1][2]
    sa_pos_response_diag_name_and_did_dict["PR_ECU_Diagnostic_Database_Version_Read"] = \
        sa_pos_response_struct_and_diag_name_dict.get("PR_ECU_Diagnostic_Database_Version_Read")[1][2]
    sa_pos_response_diag_name_and_did_dict["PR_ECU_Identification_Read"] = \
        sa_pos_response_struct_and_diag_name_dict.get("PR_ECU_Identification_Read")[1][2]
    sa_pos_response_diag_name_and_did_dict["PR_Stored_Data_Read"] = \
        sa_pos_response_struct_and_diag_name_dict.get("PR_Stored_Data_Read")[1][2]
    sa_pos_response_diag_name_and_did_dict["PR_ECU_Identification_Write"] = \
        sa_pos_response_struct_and_diag_name_dict.get("PR_ECU_Identification_Write")[1][2]
    sa_pos_response_diag_name_and_did_dict["PR_Stored_Data_Write"] = \
        sa_pos_response_struct_and_diag_name_dict.get("PR_Stored_Data_Write")[1][2]
    sa_uds_did_dict = {"REQUESTS": sa_request_diag_name_and_did_dict,
                              "POS-RESPONSES": sa_pos_response_diag_name_and_did_dict,
                              "NEG-RESPONSES": sa_neg_response_diag_name_and_did_dict}
    sa_diag_did_path = "./xat_ecu/legacy/sdk/odx_json/diag_json/sa_diag_did.json"
    with open(sa_diag_did_path, "w", encoding='utf-8') as f:
        json.dump(sa_uds_did_dict, f, indent=4)
    f.close()
    logger.info("{} File created successfully".format(sa_diag_did_path))