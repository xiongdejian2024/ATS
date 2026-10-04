# -*- coding: utf-8 -*-
"""
@File        : someip_metrics_generator.py
@Description : description about this file
@Examples    : example of how to use it
"""

from pyexcel_xls import get_data
import sys
from pathlib import Path
import json
import argparse
import os

struct_mapping = {
    "uint32": "I",
    "double": "d",
    "float": "f",
    "uint64": "q",
    "boolean": "?",
    "uint8": "B",
}


def _write_content_to_json_file(data_type_dict, service_interface_dict, json_file_path):
    data_type_file = Path(json_file_path).joinpath("data_type.json").as_posix()
    service_interface_file = Path(json_file_path).joinpath("service_interface.json").as_posix()
    with open(data_type_file, "w") as f:
        f.write(json.dumps(data_type_dict, sort_keys=True,
                           indent=2, separators=(",", ":")))
    with open(service_interface_file, "w") as f:
        f.write(json.dumps(service_interface_dict, sort_keys=True,
                           indent=2, separators=(",", ":")))


def parser_metrics_from_excel(file_path: str = "", output_path: str = "") -> None:
    # Read excel file for someip
    book = get_data(file_path)
    data_types = book.get("Datatypes")
    service_interface = book.get("ServiceInterfaces")
    data_type_dict = _parser_datatype(data_types)
    service_interface_dict = _parser_services_interface(service_interface)
    _write_content_to_json_file(data_type_dict, service_interface_dict, output_path)


def _parser_datatype(data_types: dict) -> dict:
    result = []
    mapping_list = []
    finally_result = []
    keyword = [key.strip() for key in data_types[0]]
    for raw in data_types[2:]:
        result.append(dict(zip(keyword, raw)))
    data_type_name = ''
    member_type = ''
    member_name = ''
    data_type_reference = ''
    value_table = ''
    finally_result = []
    for raw_w in result:
        tmp = {
            "members": []
        }
        if raw_w.get('DatatypeName'):
            struct_name = raw_w.get('DatatypeName').strip()
            struct_type = raw_w.get('Enum/Typedef/Union/Struct').strip()
            member_name = raw_w.get('MemberName').strip()
            member_type = raw_w.get('DatatypeReference').strip()
            tmp['struct_name'] = struct_name
            tmp['struct_type'] = struct_type
            tmp['members'].append({
                "member_name": member_name,
                "member_type": member_type
            })
            finally_result.append(tmp)
        elif len(tmp) <= 0:
            raise ValueError("Please help check Datatype sheets, it seems the format is bad")
        else:
            finally_result[-1]['members'].append({
                "member_name": raw_w.get('MemberName').strip(),
                "member_type": raw_w.get('DatatypeReference').strip()
            })

    datatype_dict = {}
    for template in finally_result:
        if template.get('struct_name') not in datatype_dict:
            datatype_dict[template.get('struct_name')] = {"members": template.get('members'),
                                                          "type": template.get('struct_type')}
    return datatype_dict


def _parser_services_interface(service_interface: dict) -> dict:
    result = []
    mapping_list = []
    keyword = [key.strip() for key in service_interface[1]]
    for raw in service_interface[2:]:
        result.append(dict(zip(keyword, raw)))
    service_id = ''
    interface_version = ''
    target_ecu = ''
    group_id = ''
    method_id = ''
    direct = ''
    finally_result = []
    null_list = ['', 'NA', 'N/A', 'None']
    for raw_w in result:
        tmp = {}
        # get service_id, interface_version,target_ecu
        if raw_w.get("ServiceInterfaceID") not in null_list:
            service_id = raw_w.get("ServiceInterfaceID")
            interface_version = raw_w.get('ServiceInterfaceVersion')
            target_ecu = raw_w.get('ServiceProviderECU')
            continue  # continue the loop, did not do below logic
        else:
            tmp["service_id"] = service_id
            tmp["interface_version"] = interface_version
            tmp["target_ecu"] = target_ecu

        # get method or eventgroup
        if raw_w.get('Method/Event/Field') not in null_list:
            if raw_w.get('Method/Event/Field') == "Method":
                group_id = ''
                method_id = raw_w.get("Method/Event ID")
            else:
                method_id = ''
                group_id = raw_w.get('Eventgroup (EventgroupName@EventgroupID)').split("@")[-1]
            data_struct = raw_w.get('DatatypeReference'), raw_w.get('ParameterName')
            # data_param_name = raw_w.get('ParameterName')
            direct = raw_w.get('ParameterDirection\n(IN/OUT)')
            tmp['group_id'] = group_id
            # tmp['data_param_name'] = data_param_name
            tmp['method_id'] = method_id
            tmp['data_struct'] = [data_struct]
            tmp['direct'] = direct
            finally_result.append(tmp)
        else:
            # Verify if direct is the same with last direct
            direct = raw_w.get('ParameterDirection\n(IN/OUT)')
            data_struct = raw_w.get('DatatypeReference'), raw_w.get('ParameterName')
            if len(finally_result) and raw_w.get('ParameterDirection\n(IN/OUT)') == finally_result[-1].get("direct"):
                finally_result[-1]['data_struct'].append(data_struct)
            else:
                tmp['group_id'] = group_id
                tmp['method_id'] = method_id
                tmp['data_struct'] = [data_struct]
                # tmp['data_param_name'] = data_param_name
                tmp['direct'] = direct
                finally_result.append(tmp)

    print(finally_result)
    service_interface = {}
    for template in finally_result:
        key = 'method_' + template.get('service_id') + '_' + template.get('method_id') if template.get(
            'method_id') else 'group_' + template.get('service_id') + '_' + template.get('group_id')
        if key not in service_interface:
            tem_value = {}
            if template.get('direct') == "IN":
                # tem_value['IN'] = [template.get('data_struct'),template.get('data_param_name')]
                tem_value['IN'] = template.get('data_struct')
            else:
                # tem_value['OUT'] = [template.get('data_struct'),template.get('data_param_name')]
                tem_value['OUT'] = template.get('data_struct')

            service_interface[key] = tem_value
        else:
            if template.get('direct') not in service_interface[key]:
                service_interface[key][template.get('direct')] = template.get('data_struct')
    return service_interface


if __name__ == "__main__":
    path_tail = "compass/tools/scripts_generator"
    scripts_path = Path(os.getcwd()).as_posix()
    input_file_path = Path(os.getcwd()).joinpath("../../sdk/interface/someip/data/SOMEIP_Services.xlsm").as_posix()
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-input_path', help='the original file from DA, support excel file only till now', default=input_file_path)
    argparser.add_argument(
        '-output_path', help='the path for json file after generator finished',
        default="../../sdk/interface/someip/constants")
    args = argparser.parse_args()
    assert scripts_path.endswith(path_tail), "Before running this script:\ncd {}".format(path_tail)
    parser_metrics_from_excel(args.input_path, args.output_path)
