# -*- coding: utf-8 -*-
"""
@File        : uds_data.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021-08-03 17:59
@Description : ODX Parser
"""

import sys
import os
from xat_ecu.legacy.common.logger import *
import json
from typing import Tuple, Union
import copy

# logger = Logger(log_level="INFO").get_logger('test')
# logger.info('Pytest configure completed')

class Uds_Data:
    def __init__(self, dlc_sd_udsservices_path="/root/quansun_pycharm/compass/xat_ecu/legacy/sdk/odx_json/dlc_sd_udsservices_dignostic_data.json"):
        with open(dlc_sd_udsservices_path, "r") as f:
            self.diag_data = json.load(f)
        f.close()

        # deal with json
        json_dict = {}
        odx = self.diag_data["ODX"]
        diag_layer_container = odx["DIAG-LAYER-CONTAINER"]
        ecu_shared_datas = diag_layer_container["ECU-SHARED-DATAS"]
        ecu_shared_data = ecu_shared_datas["ECU-SHARED-DATA"]

        funct_classs = ecu_shared_data["FUNCT-CLASSS"]
        diag_data_dictionary_spec = ecu_shared_data["DIAG-DATA-DICTIONARY-SPEC"]
        diag_comms = ecu_shared_data["DIAG-COMMS"]
        requests = ecu_shared_data["REQUESTS"]
        pos_responses = ecu_shared_data["POS-RESPONSES"]
        neg_responses = ecu_shared_data["NEG-RESPONSES"]
        global_neg_responses = ecu_shared_data["GLOBAL-NEG-RESPONSES"]
        state_charts = ecu_shared_data["STATE-CHARTS"]
        additional_audiences = ecu_shared_data["ADDITIONAL-AUDIENCES"]

        self.funct_class = funct_classs["FUNCT-CLASS"]  # funct_class is list
        self.diag_service = diag_comms["DIAG-SERVICE"]  # diag_service is list
        self.request = requests["REQUEST"]  # request is list
        self.pos_response = pos_responses["POS-RESPONSE"]  # pos_response is list
        self.neg_response = neg_responses["NEG-RESPONSE"]  # neg_response is list
        self.dtc_dop = diag_data_dictionary_spec["DTC-DOPS"]["DTC-DOP"]
        self.data_object_prop = diag_data_dictionary_spec["DATA-OBJECT-PROPS"]["DATA-OBJECT-PROP"]
        self.structure = diag_data_dictionary_spec["STRUCTURES"]["STRUCTURE"]
        self.end_of_pdu_field = diag_data_dictionary_spec["END-OF-PDU-FIELDS"]["END-OF-PDU-FIELD"]
        self.mux = diag_data_dictionary_spec["MUXS"]["MUX"]
        self.unit = diag_data_dictionary_spec["UNIT-SPEC"]["UNITS"]["UNIT"]
        self.table = diag_data_dictionary_spec["TABLES"]["TABLE"]

        self.diag_service_name = [diag_service.get("SHORT-NAME") for diag_service in self.diag_service]

    def get_value(self, data: Union[list, dict], assert_value, key_data, fixed_key="SHORT-NAME"):
        if isinstance(data, dict):
            if data.get(fixed_key) == assert_value:
                return data.get(key_data)
        elif isinstance(data, list):
            for i in data:
                if isinstance(i, dict):
                    if i.get(fixed_key) == assert_value:
                        return i.get(key_data)
                else:
                    logger.error("ODX data does not meet expectations, please check the Layer 2 data input")
        else:
            logger.error("ODX data does not meet expectations, please check the Layer 1 data input")

    def get_param(self, data):
        param = data.get("PARAMS").get("PARAM")
        return param

    def get_diag_service(self, diag_service_name):
        if diag_service_name in self.diag_service_name:
            for diag_service in self.diag_service:
                if diag_service_name == diag_service.get("SHORT-NAME"):
                    return diag_service
        else:
            logger.error("Not found diag service {}".format(diag_service_name))
            return False

    def get_diag_struct(self, diag_service_name):
        diag_service = self.get_diag_service(diag_service_name)
        diag_service_struct = self.get_param(diag_service)
        return diag_service_struct


    def get_diag_service_addressing(self, diag_service_name):
        diag_service = self.get_diag_service(diag_service_name)
        if diag_service:
            return diag_service.get("@ADDRESSING")
        else:
            logger.error("Not found diag service {}".format(diag_service_name))
            return False

    def get_diag_service_transmission_mode(self, diag_service_name):
        diag_service = self.get_diag_service(diag_service_name)
        if diag_service:
            return diag_service.get("@TRANSMISSION-MODE")
        else:
            logger.error("Not found diag service {}".format(diag_service_name))
            return False

    def get_param_from_structure(self, structure):
        param = structure.get("PARAMS").get("PARAM")
        return param

    def get_dop_from_key_dop(self, key_dop_ref):
        for dop in self.data_object_prop:
            if key_dop_ref == dop.get("@ID"):
                return dop
            elif key_dop_ref == dop.get("SHORT-NAME"):
                return dop
        if isinstance(self.dtc_dop, dict):
            if key_dop_ref == self.dtc_dop.get("SHORT-NAME"):
                return self.dtc_dop
        elif isinstance(self.dtc_dop, list):
            for dtc_dop in self.dtc_dop:
                if key_dop_ref == dtc_dop.get("SHORT-NAME"):
                    return dtc_dop
        for structure in self.structure:
            if key_dop_ref == structure.get("SHORT-NAME"):
                return structure

    def get_structure_from_structure_ref(self, structure_ref):
        for structure in self.structure:
            if structure_ref == structure.get("@ID"):
                return structure
            elif structure_ref == structure.get("SHORT-NAME"):
                return structure

    def get_dop_compu_method_form_dop(self, dop):
        return dop.get("COMPU-METHOD").get("CATEGORY")

    def get_dop_bit_length_form_dop(self, dop):
        return int(dop.get("DIAG-CODED-TYPE").get("BIT-LENGTH"))

    def get_dop_diag_coded_type_type_form_dop(self, dop):
        return dop.get("DIAG-CODED-TYPE").get("@xsi:type")

    def get_dop_diag_coded_type_form_dop(self, dop):
        return dop.get("DIAG-CODED-TYPE")

    def get_dop_display_radix_form_dop(self, dop):
        return dop.get("PHYSICAL-TYPE").get("@DISPLAY-RADIX")

    def get_dop_physical_type_form_dop(self, dop):
        base_data_type = dop.get("PHYSICAL-TYPE").get("@BASE-DATA-TYPE")
        if "@DISPLAY-RADIX" in dop.get("PHYSICAL-TYPE"):
            display_radix = self.get_dop_display_radix_form_dop(dop)
            return [base_data_type, display_radix]
        else:
            return base_data_type

    def get_dop_compu_method_from_key_dop(self, key_dop_ref):
        dop = self.get_dop_from_key_dop(key_dop_ref)
        return self.get_dop_compu_method_form_dop(dop)

    def get_dop_bit_length_from_key_dop(self, key_dop_ref):
        dop = self.get_dop_from_key_dop(key_dop_ref)
        return self.get_dop_bit_length_form_dop(dop)

    def get_dop_diag_coded_type_type_from_key_dop(self, key_dop_ref):
        dop = self.get_dop_from_key_dop(key_dop_ref)
        return self.get_dop_diag_coded_type_type_form_dop(dop)

    def get_dop_display_radix_from_key_dop(self, key_dop_ref):
        dop = self.get_dop_from_key_dop(key_dop_ref)
        return self.get_dop_display_radix_form_dop(dop)

    def get_dop_physical_type_from_key_dop(self, key_dop_ref):
        dop = self.get_dop_from_key_dop(key_dop_ref)
        return self.get_dop_physical_type_form_dop(dop)

    def get_dop_diag_coded_type_from_key_dop(self, key_dop_ref):
        dop = self.get_dop_from_key_dop(key_dop_ref)
        return self.get_dop_diag_coded_type_form_dop(dop)

    def get_request_service_id_and_diag_name_dict(self):
        request_service_id_and_diag_name_dict = {}
        for req in self.request:
            diag_name = req.get("SHORT-NAME")
            param = self.get_param(req)
            serivce_id_str = self.get_value(param, "SID_RQ", "CODED-VALUE")
            serivce_id = int(serivce_id_str)
            request_service_id_and_diag_name_dict[diag_name] = serivce_id
        return request_service_id_and_diag_name_dict

    def get_pos_response_service_id_and_diag_name_dict(self):
        pos_response_service_id_and_diag_name_dict = {}
        for pos in self.pos_response:
            diag_name = pos.get("SHORT-NAME")
            param = self.get_param(pos)
            serivce_id_str = self.get_value(param, "SID_PR", "CODED-VALUE")
            serivce_id = int(serivce_id_str)
            pos_response_service_id_and_diag_name_dict[diag_name] = serivce_id
        return pos_response_service_id_and_diag_name_dict

    def get_neg_response_service_id_and_diag_name_dict(self):
        neg_response_service_id_and_diag_name_dict = {}
        for neg in self.neg_response:
            diag_name = neg.get("SHORT-NAME")
            param = self.get_param(neg)
            serivce_id_str = self.get_value(param, "SIDRQ_NR", "CODED-VALUE")
            serivce_id = int(serivce_id_str)
            neg_response_service_id_and_diag_name_dict[diag_name] = serivce_id
        return neg_response_service_id_and_diag_name_dict

    def get_table_row_and_key_dop_ref_form_param_dict(self, param_dict: dict):
        table_row = None
        key_dop_ref = None
        if "TABLE-SNREF" in param_dict:
            table_snref_dict = param_dict.get("TABLE-SNREF")
            table_snref = table_snref_dict.get("@SHORT-NAME")
            for table_name in self.table:
                if table_snref == table_name.get("SHORT-NAME"):
                    table_row = table_name.get("TABLE-ROW")
                    key_dop_ref = table_name.get("KEY-DOP-REF").get("@ID-REF")
                    return table_row, key_dop_ref
        elif "TABLE-REF" in param_dict:
            table_ref_dict = param_dict.get("TABLE-REF")
            table_ref = table_ref_dict.get("@ID-REF")
            for table_name in self.table:
                if table_ref == table_name.get("@ID"):
                    table_row = table_name.get("TABLE-ROW")
                    key_dop_ref = table_name.get("KEY-DOP-REF").get("@ID-REF")
                    return table_row, key_dop_ref

    def get_structure_ref_form_table_row_ref(self, table_row_ref):
        key_dict = {}
        for table in self.table:
            if "TABLE-ROW" in table:
                table_rows = table.get("TABLE-ROW")
                if isinstance(table_rows, list):
                    for table_row in table_rows:
                        if table_row_ref == table_row.get("@ID"):
                            if "KEY" in table_row:
                                name = table_row.get("SHORT-NAME")
                                key = int(table_row.get("KEY"))
                                key_dict[name] = key
                                key_dop_ref = table.get("KEY-DOP-REF").get("@ID-REF")
                                return key_dict, key_dop_ref
                            else:
                                logger.error("table error , please check ODX , table_row_ref is {}".format(table_row_ref))

    def get_table_row_from_table_struct(self, param_dict: dict, param: list):
        if "TABLE-KEY-SNREF" in param_dict:
            table_key_snref_dict = param_dict.get("TABLE-KEY-SNREF")
            table_key_snref = table_key_snref_dict.get("@SHORT-NAME")
            for data in param:
                if data.get("SHORT-NAME") == table_key_snref:
                    table_snref_dict = data.get("TABLE-SNREF")
                    table_snref = table_snref_dict.get("@SHORT-NAME")
                    for table_name in self.table:
                        if table_snref == table_name.get("SHORT-NAME"):
                            table_row = table_name.get("TABLE-ROW")
                            return table_row
        elif "TABLE-KEY-REF" in param_dict:
            table_key_ref_dict = param_dict.get("TABLE-KEY-REF")
            table_key_ref = table_key_ref_dict.get("@ID-REF")
            for data in param:
                if data.get("@ID") == table_key_ref:
                    table_ref_dict = data.get("TABLE-REF")
                    table_ref = table_ref_dict.get("@ID-REF")
                    for table_name in self.table:
                        if table_ref == table_name.get("@ID"):
                            table_row = table_name.get("TABLE-ROW")
                            return table_row

    def get_key_dict_from_table_row(self, table_row: list):
        key_dict = {}
        if isinstance(table_row, list):
            for table in table_row:
                # if len(table.get("KEY")) > 10:
                if "memoryAddress" in table.get("KEY"):
                    key_dict.setdefault(table.get("SHORT-NAME"), table.get("KEY"))
                else:
                    key_dict.setdefault(table.get("SHORT-NAME"), int(table.get("KEY")))
        elif isinstance(table_row, dict):
            key_dict.setdefault(table_row.get("SHORT-NAME"), int(table_row.get("KEY")))
        else:
            logger.error("table_row error , please check ODX , table_row is {}".format(table_row))
        return key_dict

    def get_structure_ref_dict_from_table_row(self, table_row):
        structure_ref_dict = {}
        if isinstance(table_row, list):
            for table in table_row:
                if "STRUCTURE-REF" in table:
                    structure_ref_dict.setdefault(table.get("SHORT-NAME"), table.get("STRUCTURE-REF").get("@ID-REF"))
                else:
                    structure_ref_dict.setdefault(table.get("SHORT-NAME"))
        elif isinstance(table_row, dict):
            if "STRUCTURE-REF" in table_row:
                structure_ref_dict.setdefault(table_row.get("SHORT-NAME"), table_row.get("STRUCTURE-REF").get("@ID-REF"))
            else:
                structure_ref_dict.setdefault(table_row.get("SHORT-NAME"))
        else:
            logger.error("table_row error , please check ODX")
        return structure_ref_dict

    def get_key_length_form_key_dop_ref(self, key_dop_ref):
        dop_bit_length = self.get_dop_bit_length_from_key_dop(key_dop_ref)
        remainder = dop_bit_length % 8
        key_length = dop_bit_length // 8
        if remainder == 0:
            return dop_bit_length
        else:
            logger.error("table key dop_bit_length error , please check ODX, key_dop_ref is {}".format(key_dop_ref))

    # def get_key_dict_from_param_dict(self, param_dict):
    #     logger.info(param_dict)
    #     table_row = self.get_table_row_form_param_dict(param_dict)
    #     key_dict = self.get_key_dict_from_table_row(table_row)
    #     return key_dict

    def get_data_type_struct_from_diag_coded_type(self, diag_coded_type):
        if diag_coded_type.get("@xsi:type") == "STANDARD-LENGTH-TYPE":
            length = int(diag_coded_type.get("BIT-LENGTH"))/8
            if isinstance(length, int) == False:
                length_bit = int(diag_coded_type.get("BIT-LENGTH"))
                return length_bit
            else:
                return [length]
        elif diag_coded_type.get("@xsi:type") == "MIN-MAX-LENGTH":
            max_length = diag_coded_type.get("MAX-LENGTH")
            min_length = diag_coded_type.get("MIN-LENGTH")
            return [min_length, max_length]

    def get_structure_param_struct_from_structure_ref(self, structure_ref):
        structure = self.get_structure_from_structure_ref(structure_ref)
        # byte_size = structure.get("BYTE-SIZE")
        structure_param = self.get_param_from_structure(structure)
        structure_param_structs = []
        if isinstance(structure_param, dict):
            if structure_param.get("@xsi:type") == "VALUE":
                value_struct = self.get_value_struct_form_param(structure_param)
                return value_struct
        elif isinstance(structure_param, list):
            for structure_data in structure_param:
                if structure_data.get("@xsi:type") == "VALUE":
                    structure_param_struct = self.get_value_struct_form_param(structure_data)
                elif structure_data.get("@xsi:type") == "TABLE-KEY":
                    structure_param_struct = self.get_table_key_struct_form_param(structure_data)
                elif structure_data.get("@xsi:type") == "TABLE-STRUCT":
                    structure_param_struct = self.get_table_struct_struct_form_param(structure_data, structure_param)
                elif structure_data.get("@xsi:type") == "RESERVED":
                    structure_param_struct = self.get_reserved_struct_form_param(structure_data)
                else:
                    logger.error("Exceed expectations , please check ODX")
                structure_param_structs.append(structure_param_struct)
            return structure_param_structs

    def get_mux_struct_from_mux(self, mux: dict):
        mux_byte_position = int(mux.get("BYTE-POSITION"))
        case = mux.get("CASES").get("CASE")
        switch_key = mux.get("SWITCH-KEY")
        switch_key_byte_position = int(switch_key.get("BYTE-POSITION"))
        switch_key_data_object_prop_ref = switch_key.get("DATA-OBJECT-PROP-REF").get("@ID-REF")
        mux_case_struct = {}
        if isinstance(case, dict):
            case_name = case.get("SHORT-NAME")
            case_struct_ref = case.get("STRUCTURE-REF").get("@ID-REF")
            case_struct = self.get_structure_param_struct_from_structure_ref(case_struct_ref)
            mux_case_struct[case_name] = case_struct
            mux_struct = [[mux_byte_position, switch_key_byte_position], mux_case_struct]
        elif isinstance(case, list):
            for case_single in case:
                case_name = case_single.get("SHORT-NAME")
                case_struct_ref = case_single.get("STRUCTURE-REF").get("@ID-REF")
                case_struct = self.get_structure_param_struct_from_structure_ref(case_struct_ref)
                mux_case_struct[case_name] = case_struct
            mux_struct = [[mux_byte_position, switch_key_byte_position], mux_case_struct]
        return mux_struct

    def get_struct_name_and_struct_dict_from_struct(self):
        struct_name_and_struct_dict = {}
        for struct in self.structure:
            struct_name = struct.get("SHORT-NAME")
            struct_name_and_struct_dict[struct_name] = struct
        return struct_name_and_struct_dict

    def get_struct_id_and_struct_dict_from_struct(self):
        struct_id_and_struct_dict = {}
        for struct in self.structure:
            struct_id = struct.get("@ID")
            struct_id_and_struct_dict[struct_id] = struct
        return struct_id_and_struct_dict
    
    def get_mux_name_and_mux_dict_from_mux(self):
        mux_name_and_mux_dict = {}
        for mux in self.mux:
            mux_name = mux.get("SHORT-NAME")
            mux_name_and_mux_dict[mux_name] = mux
        return mux_name_and_mux_dict
    
    def get_mux_id_and_mux_dict_from_mux(self):
        mux_id_and_mux_dict = {}
        for mux in self.mux:
            mux_id = mux.get("@ID")
            mux_id_and_mux_dict[mux_id] = mux
        return mux_id_and_mux_dict

    def get_end_of_pdu_field_name_and_end_of_pdu_field_dict_from_end_of_pdu_field(self):
        end_of_pdu_field_name_and_end_of_pdu_field_dict = {}
        for end_of_pdu_field in self.end_of_pdu_field:
            end_of_pdu_field_name = end_of_pdu_field.get("SHORT-NAME")
            end_of_pdu_field_name_and_end_of_pdu_field_dict[end_of_pdu_field_name] = end_of_pdu_field
        return end_of_pdu_field_name_and_end_of_pdu_field_dict
    
    def get_end_of_pdu_field_id_and_end_of_pdu_field_dict_from_end_of_pdu_field(self):
        end_of_pdu_field_id_and_end_of_pdu_field_dict = {}
        for end_of_pdu_field in self.end_of_pdu_field:
            end_of_pdu_field_id = end_of_pdu_field.get("@ID")
            end_of_pdu_field_id_and_end_of_pdu_field_dict[end_of_pdu_field_id] = end_of_pdu_field
        return end_of_pdu_field_id_and_end_of_pdu_field_dict

    def get_struct_ref_form_end_of_pdu_field_dict(self, end_of_pdu_field_dict):
        struct_ref = end_of_pdu_field_dict.get("BASIC-STRUCTURE-REF").get("@ID-REF")
        return struct_ref

    def get_table_key_struct_form_param(self, param: dict):
        if param.get("@xsi:type") == "TABLE-KEY":
            byte_position = int(param.get("BYTE-POSITION"))
            if "TABLE-ROW-REF" in param:
                table_row_ref = param.get("TABLE-ROW-REF").get("@ID-REF")
                key_dict, key_dop_ref = self.get_structure_ref_form_table_row_ref(table_row_ref)
                key_length = self.get_key_length_form_key_dop_ref(key_dop_ref)
                table_key_struct = [byte_position, key_length, key_dict]
                return table_key_struct
            else:
                table_row, key_dop_ref = self.get_table_row_and_key_dop_ref_form_param_dict(param)
                key_length = self.get_key_length_form_key_dop_ref(key_dop_ref)
                key_dict = self.get_key_dict_from_table_row(table_row)
                table_key_struct = [byte_position, key_length, key_dict]
                return table_key_struct
        else:
            logger.error("param data error , please check ODX , param is {}".format(param))

    def get_table_struct_struct_form_param(self, param: dict, params: list):
        if param.get("@xsi:type") == "TABLE-STRUCT":
            table_row = self.get_table_row_from_table_struct(param, params)
            structure_ref_dict = self.get_structure_ref_dict_from_table_row(table_row)
            for structure_ref_key in structure_ref_dict.keys():
                structure_ref = structure_ref_dict[structure_ref_key]
                if structure_ref:
                    structure_param_struct = self.get_structure_param_struct_from_structure_ref(structure_ref)
                    structure_ref_dict[structure_ref_key] = structure_param_struct
            table_struct_struct = structure_ref_dict
            return table_struct_struct
        else:
            logger.error("param data error , please check ODX , param is {}".format(param))

    def get_reserved_struct_form_param(self, param: dict):
        if param.get("@xsi:type") == "RESERVED":
            byte_position = param.get("BYTE-POSITION")
            bit_position = param.get("BIT-POSITION")
            param_position = [byte_position, bit_position]
            length = param.get("BIT-LENGTH")
            physical_type = None
            compu_method = None
            reserved_struct = [param_position, length, physical_type, compu_method]
            return reserved_struct
        else:
            logger.error("param data error , please check ODX , param is {}".format(param))


    def get_value_struct_form_param(self, param: dict):
        if param.get("@xsi:type") == "VALUE":
            if "DOP-REF" in param:
                dop_ref = param.get("DOP-REF").get("@ID-REF")
                struct_id_and_struct_dict = self.get_struct_id_and_struct_dict_from_struct()
                end_of_pdu_field_id_and_end_of_pdu_field_dict = self.get_end_of_pdu_field_id_and_end_of_pdu_field_dict_from_end_of_pdu_field()
                mux_id_and_mux_dic = self.get_mux_id_and_mux_dict_from_mux()
                if dop_ref in struct_id_and_struct_dict:
                    value_struct = self.get_structure_param_struct_from_structure_ref(dop_ref)
                elif dop_ref in end_of_pdu_field_id_and_end_of_pdu_field_dict:
                    end_of_pdu_field = end_of_pdu_field_id_and_end_of_pdu_field_dict[dop_ref]
                    struct_ref = self.get_struct_ref_form_end_of_pdu_field_dict(end_of_pdu_field)
                    value_struct = self.get_structure_param_struct_from_structure_ref(struct_ref)
                elif dop_ref in mux_id_and_mux_dic:
                    mux = mux_id_and_mux_dic[dop_ref]
                    param_position = int(param.get("BYTE-POSITION"))
                    mux_sturt = self.get_mux_struct_from_mux(mux)
                    value_struct = [param_position, mux_sturt]
                else:
                    diag_coded_type = self.get_dop_diag_coded_type_from_key_dop(dop_ref)
                    if diag_coded_type:
                        byte_position = int(param.get("BYTE-POSITION"))
                        physical_type = self.get_dop_physical_type_from_key_dop(dop_ref)
                        if "BIT-POSITION" in param:
                            bit_position = param.get("BIT-POSITION")
                            param_position = [byte_position, bit_position]
                        else:
                            param_position = byte_position
                        compu_method = self.get_dop_compu_method_from_key_dop(dop_ref)
                        # "INTERNAL-CONSTR"   To Do
                        # "UNIT-REF"   To Do
                        length = self.get_data_type_struct_from_diag_coded_type(diag_coded_type)
                    else:
                        logger.error("diag_coded_type param error , please check ODX , param is {}".format(param))
                    value_struct = [param_position, length, physical_type, compu_method]
                return value_struct
            elif param.get("@xsi:type") == "RESERVED":
                byte_position = param.get("BYTE-POSITION")
                bit_position = param.get("BIT-POSITION")
                param_position = [byte_position, bit_position]
                length = param.get("BIT-LENGTH")
                physical_type = None
                compu_method = None
                value_struct = [param_position, length, physical_type, compu_method]
                return value_struct
            elif "DOP-SNREF" in param:
                dop_ref = param.get("DOP-SNREF").get("@SHORT-NAME")
                struct_name_and_struct_dict = self.get_struct_name_and_struct_dict_from_struct()
                end_of_pdu_field_name_and_end_of_pdu_field_dict = self.get_end_of_pdu_field_name_and_end_of_pdu_field_dict_from_end_of_pdu_field()
                mux_name_and_mux_dic = self.get_mux_name_and_mux_dict_from_mux()
                if dop_ref in struct_name_and_struct_dict:
                    value_struct = self.get_structure_param_struct_from_structure_ref(dop_ref)
                elif dop_ref in end_of_pdu_field_name_and_end_of_pdu_field_dict:
                    end_of_pdu_field = end_of_pdu_field_name_and_end_of_pdu_field_dict[dop_ref]
                    struct_ref = self.get_struct_ref_form_end_of_pdu_field_dict(end_of_pdu_field)
                    value_struct = self.get_structure_param_struct_from_structure_ref(struct_ref)
                elif dop_ref in mux_name_and_mux_dic:
                    mux = mux_name_and_mux_dic[dop_ref]
                    param_position = int(param.get("BYTE-POSITION"))
                    mux_sturt = self.get_mux_struct_from_mux(mux)
                    value_struct = [param_position, mux_sturt]
                else:
                    diag_coded_type = self.get_dop_diag_coded_type_from_key_dop(dop_ref)
                    if diag_coded_type:
                        byte_position = int(param.get("BYTE-POSITION"))
                        physical_type = self.get_dop_physical_type_from_key_dop(dop_ref)
                        if "BIT-POSITION" in param:
                            bit_position = param.get("BIT-POSITION")
                            param_position = [byte_position, bit_position]
                        else:
                            param_position = byte_position
                        compu_method = self.get_dop_compu_method_from_key_dop(dop_ref)
                        # "INTERNAL-CONSTR"   To Do
                        # "UNIT-REF"   To Do
                        length = self.get_data_type_struct_from_diag_coded_type(diag_coded_type)
                    else:
                        logger.error("diag_coded_type param error , please check ODX , param is {}".format(param))
                    value_struct = [param_position, length, physical_type, compu_method]
                return value_struct
        else:
            logger.error("param data error , please check ODX , param is {}".format(param))

    def get_diag_struct_and_diag_name_dict_from_param(self, param):
        diag_struct = []
        if isinstance(param, dict):
            diag_coded_type = None
            if param.get("@xsi:type") == "CODED-CONST":
                byte_position = int(param.get("BYTE-POSITION"))
                coded_value = int(param.get("CODED-VALUE"))
                diag_struct.append(coded_value)
                diag_coded_type = param.get("DIAG-CODED-TYPE")
                if diag_coded_type:
                    length = self.get_data_type_struct_from_diag_coded_type(diag_coded_type)
                else:
                    logger.error("diag_coded_type data error , please check ODX")
            else:
                logger.error("Exceed expectations , please check ODX")
            return diag_struct
        elif isinstance(param, list):
            for data in param:
                diag_coded_type = None
                if data.get("@xsi:type") == "CODED-CONST":
                    byte_position = int(data.get("BYTE-POSITION"))
                    coded_value = int(data.get("CODED-VALUE"))
                    diag_struct.append(coded_value)
                    diag_coded_type = data.get("DIAG-CODED-TYPE")
                    if diag_coded_type:
                        length = self.get_data_type_struct_from_diag_coded_type(diag_coded_type)
                    else:
                        logger.error("diag_coded_type data error , please check ODX")
                elif data.get("@xsi:type") == "TABLE-KEY":
                    table_key_struct = self.get_table_key_struct_form_param(data)
                    diag_struct.append(table_key_struct)
                elif data.get("@xsi:type") == "TABLE-STRUCT":
                    table_struct_struct = self.get_table_struct_struct_form_param(data, param)
                    diag_struct.append(table_struct_struct)
                elif data.get("@xsi:type") == "VALUE":
                    value_struct = self.get_value_struct_form_param(data)
                    diag_struct.append(value_struct)
                elif data.get("@xsi:type") == "MATCHING-REQUEST-PARAM":
                    logger.error("uds_data.py Code not overwritten MATCHING-REQUEST-PARAM")
                elif data.get("@xsi:type") == "RESERVED":
                    logger.warning("uds_data.py Code not overwritten LENGTH-KEY")
                elif data.get("@xsi:type") == "LENGTH-KEY":
                    logger.warning("uds_data.py Code not overwritten LENGTH-KEY")
                elif data.get("@xsi:type") == "PHYS-CONST":
                    logger.warning("uds_data.py Code not overwritten PHYS-CONST")
                elif data.get("@xsi:type") == "TABLE-ENTRY":
                    logger.warning("uds_data.py Code not overwritten TABLE-ENTRY")
                else:
                    logger.error("Exceed expectations , please check ODX")
        return diag_struct

    def get_request_diag_struct_and_diag_name_dict_form_param(self):
        request_diag_struct_and_diag_name_dict = {}
        for req in self.request:
            diag_name = req.get("SHORT-NAME")
            param = self.get_param(req)
            diag_struct = self.get_diag_struct_and_diag_name_dict_from_param(param)
            request_diag_struct_and_diag_name_dict[diag_name] = diag_struct
        return request_diag_struct_and_diag_name_dict

    def get_pos_response_diag_struct_and_diag_name_dict_form_param(self):
        pos_response_diag_struct_and_diag_name_dict = {}
        for pos in self.pos_response:
            diag_name = pos.get("SHORT-NAME")
            param = self.get_param(pos)
            diag_struct = self.get_diag_struct_and_diag_name_dict_from_param(param)
            pos_response_diag_struct_and_diag_name_dict[diag_name] = diag_struct
        return pos_response_diag_struct_and_diag_name_dict

    def get_neg_response_diag_struct_and_diag_name_dict_form_param(self):
        neg_response_diag_struct_and_diag_name_dict = {}
        for neg in self.neg_response:
            diag_name = neg.get("SHORT-NAME")
            param = self.get_param(neg)
            diag_struct = self.get_diag_struct_and_diag_name_dict_from_param(param)
            neg_response_diag_struct_and_diag_name_dict[diag_name] = diag_struct
        return neg_response_diag_struct_and_diag_name_dict

class Uds_Data_Ecu(Uds_Data):
    def __init__(self, odx_json_path="/root/quansun_pycharm/compass/xat_ecu/legacy/sdk/odx_json/sa_dignostic_data.json"):
        super().__init__()

        with open(odx_json_path, "r") as f:
            self.diag_data = json.load(f)
        f.close()

        # deal with json
        json_dict = {}
        odx = self.diag_data["ODX"]
        diag_layer_container = odx["DIAG-LAYER-CONTAINER"]
        base_variants = diag_layer_container["BASE-VARIANTS"]
        base_variant = base_variants["BASE-VARIANT"]

        funct_classs = base_variant["FUNCT-CLASSS"]
        diag_data_dictionary_spec = base_variant["DIAG-DATA-DICTIONARY-SPEC"]
        diag_comms = base_variant["DIAG-COMMS"]
        requests = base_variant["REQUESTS"]
        pos_responses = base_variant["POS-RESPONSES"]
        neg_responses = base_variant["NEG-RESPONSES"]
        comparam_refs = base_variant["COMPARAM-REFS"]
        parent_refs = base_variant["PARENT-REFS"]
        additional_audiences = base_variant["ADDITIONAL-AUDIENCES"]

        self.funct_class += funct_classs["FUNCT-CLASS"]  # funct_class is list
        self.diag_service += diag_comms["DIAG-SERVICE"]  # diag_service is list
        self.request += requests["REQUEST"]  # request is list
        self.pos_response += pos_responses["POS-RESPONSE"]  # pos_response is list
        self.neg_response += neg_responses["NEG-RESPONSE"]  # neg_response is list

        self.dtc_dop = [self.dtc_dop, diag_data_dictionary_spec["DTC-DOPS"]["DTC-DOP"]]
        self.data_object_prop += diag_data_dictionary_spec["DATA-OBJECT-PROPS"]["DATA-OBJECT-PROP"]
        self.structure += diag_data_dictionary_spec["STRUCTURES"]["STRUCTURE"]
        if "END-OF-PDU-FIELDS" in diag_data_dictionary_spec:
            self.dict_or_list(diag_data_dictionary_spec["END-OF-PDU-FIELDS"]["END-OF-PDU-FIELD"], self.end_of_pdu_field)
        if "MUXS" in diag_data_dictionary_spec:
            self.dict_or_list(diag_data_dictionary_spec["MUXS"]["MUX"], self.mux)
        if "UNIT-SPEC" in diag_data_dictionary_spec:
            self.dict_or_list(diag_data_dictionary_spec["UNIT-SPEC"]["UNITS"]["UNIT"], self.unit)
        if "TABLES" in diag_data_dictionary_spec:
            self.dict_or_list(diag_data_dictionary_spec["TABLES"]["TABLE"], self.table)
        self.diag_service_name = [diag_service.get("SHORT-NAME") for diag_service in self.diag_service]

    def dict_or_list(self, data, param: list):
        if isinstance(data, dict):
            param.append(data)
        elif isinstance(data, list):
            param += data
        else:
            logger.error("data error,data is {}".format(data))

class Uds_Handle_Data:
    def __init__(self):
        with open("./xat_ecu/legacy/sdk/odx_json/diag_json/sa_diag_struct.json", "r") as sa_diag:
            self.diag_data = json.load(sa_diag)
        sa_diag.close()

        with open("./xat_ecu/legacy/sdk/odx_json/diag_json/sa_diag_service_id.json", "r") as service_id:
            self.service_id = json.load(service_id)
        service_id.close()




