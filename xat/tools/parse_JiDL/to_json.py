#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_

"""
@Time: 2022/9/20 15:37
@Author: lei.tao
@File: to_json.py
@Software: PyCharm
@Description: parse jidl to json
@Example:
没有输入或输入为空：{}
没有输出：{"out": null}
输出为空：{"out": "None"}
"""
import json
import os
import re
import sys


current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path.split("sat")[0], "sat"))
soa_partner_path = os.path.join(current_path.split("sat")[0], "sat/xat_ecu/legacy/soa_partner/")


def get_method_in_out_arg(o_file, method):
    model = get_type_mode(o_file, "interface")
    arg_ = []
    for method_model in model.split(";"):
        if method in method_model:
            if "return" in method_model:
                arg_.append("return")
            if "param[in]" in method_model:
                arg_.append("arg_in")
            elif "param[out]" in method_model:
                arg_.append("arg_out")
            else:
                arg_.append(False)

    return arg_


def get_type_mode(o_file, _type):
    """
    获取type定义类型的内容模块
    """
    arg = parse_arg_type(_type)
    mod_list = get_service_data(o_file).split("};")
    s_mod_list = []
    for i in range(len(mod_list)):
        if (arg + '{') in mod_list[i]:
            s_mod_list.append(mod_list[i])
        elif (arg + ' ') in mod_list[i]:
            s_mod_list.append(mod_list[i])
        elif arg in mod_list[i]:
            s_mod_list.append(mod_list[i])
    if not s_mod_list:
        for i in range(len(mod_list)):
            if arg in mod_list[i]:
                s_mod_list.append(mod_list[i])
    if 'const string' in s_mod_list[0]:
        data = []
        for line in s_mod_list[0].split('\n'):
            if 'const string' in line:
                if arg in line:
                    return line
            else:
                data.append(line)
        return "\n".join(data)
    elif 'typedef' in s_mod_list[0]:
        data = []
        for line in s_mod_list[0].split('\n'):
            if 'typedef' in line:
                if arg in line:
                    return line
            else:
                data.append(line)

        return "\n".join(data)
    else:
        return s_mod_list[0]


def get_mode_method(mode):
    for i in range(len(mode.split('\n'))):
        mode.split('\n')[i].replace('\t', ' ')
        if '{' in mode.split('\n')[i]:
            if mode.split('\n')[i].split('{')[0] == "":
                if len(mode.split('\n')[i - 1].strip().split(' ')) == 1:
                    if mode.split('\n')[i + 1].strip().split(' ')[0] == "enum":
                        return "enum"
                    elif mode.split('\n')[i + 1].strip().split(' ')[0] == "struct":
                        return "struct"
                else:
                    if mode.split('\n')[i - 1].strip().split(' ')[0] == "enum":
                        return "enum"
                    elif mode.split('\n')[i - 1].strip().split(' ')[0] == "struct":
                        return "struct"
            else:
                if mode.split('\n')[i].strip().split(' ')[0] == "enum":
                    return "enum"
                elif mode.split('\n')[i].strip().split(' ')[0] == "struct":
                    return "struct"


def get_enum_value(o_file, _type):
    arg_list = []
    arg = parse_arg_type(_type)
    model = get_type_mode(o_file, arg)

    for line in model.split('\n'):
        # if "@value" in line and "\t" in line:
        #     arg_list.append(line.split(',')[0].split('\t'))
        line = line.replace("\t", " ")
        if "@value" in line and " " in line:
            arg_list.append(line.split(',')[0].split(' '))

    arg_list_ = [i for i in arg_list[0] if i != ""]

    if "sequence" in _type:
        return list(arg_list_[-2][-2])
    else:
        return int(arg_list_[-2][-2])


# 获取参数类型
def get_arg(o_file, _arg):
    _type = parse_arg_type(_arg)
    if _type == "bool":
        return False
    elif _type == "float":
        return 0.0
    elif _type == "void":
        return None
    elif _type == "double":
        return 1579881600000
    elif _type.startswith("int") or _type.startswith("uint"):
        if "sequence" in str(_arg):
            return [0]
        else:
            return 0
    elif _type == "string":
        return ""
    else:
        # 获取type定义类型的模块
        mode = get_type_mode(o_file, _type)
        arg_list1 = []
        arg_list2 = []
        arg_list3 = []
        arg_list5 = []
        arg_list6 = []
        arg_list7 = []
        arg_list8 = []
        arg_list9 = []
        if "enum" == get_mode_method(mode):
            return get_enum_value(o_file, _type)

        if "struct" == get_mode_method(mode):
            for line in mode.split('\n'):
                line = line.replace('\t', ' ')
                if ";" in line and " " in line:
                    arg_list = [i for i in line.split(' ') if i != ""]
                    arg_list1.append({arg_list[-1].strip(';'): arg_list[-2]})

    if arg_list1:
        for arg1 in arg_list1:
            for k, vs in arg1.items():
                v = parse_arg_type(vs)
                if v == "bool":
                    arg_list2.append({k: False})
                elif v == "string":
                    arg_list2.append({k: ""})
                elif v == "double":
                    arg_list2.append({k: 1579881600000})
                elif v == "float":
                    arg_list2.append({k: 0.0})
                elif v.startswith("int") or v.startswith("uint"):
                    arg_list2.append({k: 0})
                else:
                    mode1 = get_type_mode(o_file, v)
                    if "enum" == get_mode_method(mode1):
                        arg_list2.append({k: get_enum_value(o_file, v)})
                    if "struct" == get_mode_method(mode1):
                        for line in mode1.split('\n'):
                            line = line.replace('\t', ' ')
                            if ";" in line and " " in line:
                                arg_list4 = [i for i in line.split(' ') if i != ""]
                                arg_list3.append({arg_list4[-1].strip(';'): arg_list4[-2]})

    if not arg_list3:
        return arg_list2
    else:
        for arg2 in arg_list3:
            for key, vals in arg2.items():
                val = parse_arg_type(vals)
                if val == "bool":
                    arg_list5.append({key: False})
                elif val == "string":
                    arg_list5.append({key: ""})
                elif val == "double":
                    arg_list5.append({key: 1579881600000})
                elif val == "float":
                    arg_list5.append({key: 0.0})
                elif val.startswith("int") or val.startswith("uint"):
                    arg_list5.append({key: 0})
                else:
                    mode2 = get_type_mode(o_file, val)
                    if "enum" == get_mode_method(mode2):
                        arg_list5.append({key: get_enum_value(o_file, val)})
                    if "struct" == get_mode_method(mode2):
                        for line in mode2.split('\n'):
                            line = line.replace('\t', ' ')
                            if ";" in line and " " in line:
                                arg_list_ = [i for i in line.split(' ') if i != ""]
                                arg_list6.append({arg_list_[-1].strip(';'): arg_list_[-2]})

    if not arg_list6:
        arg_list2.extend(arg_list5)
        return arg_list2
    else:
        for arg3 in arg_list6:
            for key1, vals1 in arg3.items():
                val1 = parse_arg_type(vals1)
                if val1 == "bool":
                    arg_list7.append({key1: False})
                elif val1 == "double":
                    arg_list7.append({key1: 1579881600000})
                elif val1 == "string":
                    arg_list7.append({key1: ""})
                elif val1 == "float":
                    arg_list7.append({key1: 0.0})
                elif val1.startswith("int") or val1.startswith("uint"):
                    arg_list7.append({key1: 0})
                else:
                    mode3 = get_type_mode(o_file, val1)
                    if "enum" == get_mode_method(mode3):
                        arg_list7.append({key1: get_enum_value(o_file, val1)})
                    if "struct" == get_mode_method(mode3):

                        for line in mode3.split('\n'):
                            line = line.replace('\t', ' ')
                            if ";" in line and " " in line:
                                arg_list_1 = [i for i in line.split(' ') if i != ""]
                                arg_list8.append({arg_list_1[-1].strip(';'): arg_list_1[-2]})

    if not arg_list8:
        arg_list5.extend(arg_list7)
        arg_list2.extend(arg_list5)
        return arg_list2
    else:
        for arg4 in arg_list8:
            for key4, vals4 in arg4.items():
                val4 = parse_arg_type(vals4)
                if val4 == "bool":
                    arg_list9.append({key4: False})
                elif val4 == "double":
                    arg_list9.append({key4: 1579881600000})
                elif val4 == "string":
                    arg_list9.append({key4: ""})
                elif val4 == "float":
                    arg_list9.append({key4: 0.0})
                elif val4.startswith("int") or val4.startswith("uint"):
                    arg_list9.append({key4: 0})
                else:
                    mode4 = get_type_mode(o_file, val4)
                    if "enum" == get_mode_method(mode4):
                        arg_list9.append({key4: get_enum_value(o_file, val4)})

        arg_list7.extend(arg_list9)
        arg_list5.extend(arg_list7)
        arg_list2.extend(arg_list5)
        return arg_list2


def parse_arg_type(_type):
    """
    解析参数的类型, 带sequence的返回<>中的实际类型，
    """
    if "sequence" in _type:
        p = re.compile(r'<(.*?)>', re.S)
        arg1 = re.findall(p, _type.strip())[0]
        return arg1

    else:
        return _type


def get_arg_type(o_file, _type):
    arg_list = []
    mode = get_type_mode(o_file, _type)

    if "enum" == get_mode_method(mode):
        return get_enum_value(o_file, _type)

    else:
        for line in mode.split('\n'):
            # if ";" in line and "\t" in line:
            #     if ";" in line.split('\t')[1].strip():
            #         arg_list3 = [i for i in line.split('\t') if i != ""]
            #         arg_list.append({"arg": arg_list3[-1].strip(';'), "type": arg_list3[0].strip()})
            #     if " " in line.split('\t')[-1].strip():
            #         arg_list3 = [i for i in line.split(' ') if i != ""]
            #         arg_list.append({"arg": arg_list3[1][:-1], "type": arg_list3[0][1:]})
            #     else:
            #         arg_list3 = [i for i in line.split('\t') if i != ""]
            #         arg_list.append({"arg": arg_list3[-1].strip(';'), "type": arg_list3[-2].strip()})
            line = line.replace('\t', ' ')
            if ";" in line:
                arg_list3 = [i for i in line.split(' ') if i != ""]
                arg_list.append({"arg": arg_list3[-1].strip(';'), "type": arg_list3[-2].strip()})

        arg_list2 = []
        for item in arg_list:
            if item['type'] == "bool":
                arg_list2.append({"arg": item['arg'], "type": item['type']})
            elif item['type'] == "string":
                arg_list2.append({"arg": item['arg'], "type": item['type']})
            elif "int" in str(item['type']):
                arg_list2.append({"arg": item['arg'], "type": item['type']})
            elif item['type'] == "float":
                arg_list2.append({"arg": item['arg'], "type": item['type']})
            elif item['type'] == "void":
                arg_list2.append({"arg": item['arg'], "type": item['type']})
            else:
                mode1 = get_type_mode(o_file, item['type'])

                if "enum" == get_mode_method(mode1):
                    arg_list2.append({"arg": item['arg'], "type": item['type']})
                if "typedef" in mode1:
                    line = mode1.replace('\t', ' ')
                    arg_list3 = [i for i in line.split(' ') if i != ""]
                    arg_list2.append({"arg": item['arg'], "type": arg_list3[-2]})
                if "struct" == get_mode_method(mode1):
                    for line in mode1.split('\n'):

                        line = line.replace('\t', ' ')
                        if ";" in line and " " in line:
                            arg_list3 = [i for i in line.split(' ') if i != ""]
                            arg_list2.append({"arg": arg_list3[-1].strip(';'), "type": arg_list3[-2]})

        return arg_list2


# 获取函数的类型
def get_arg_out_value(o_file, _arg):
    """
    return: 返回参数类型的value
    """
    _type = parse_arg_type(_arg)
    if "void" in _type:
        return {"out": "None"}
    elif "int" in str(_type):
        return {"out": 0}
    elif "bool" in _type:
        return {"out": False}
    elif "string" in _type:
        return {"out": ""}
    elif "float" in _type:
        return {"out": 0.0}
    else:
        type_json = get_arg_type(o_file, _type)
        model = get_type_mode(o_file, _type)
        _value = []
        if "enum" == get_mode_method(model):
            return {"out": type_json}
        elif "typedef" in model:
            return {"out": get_arg(o_file, model.split(' ')[-2])}
        else:
            # for _args in type_json:
            # _value.append({_args['arg']: get_arg(o_file, _args['type'])})
            _value.append(get_arg(o_file, _type))
            return _value


def get_service_data(o_file):
    with open(o_file, 'r', encoding='utf-8') as f:
        data = f.read()
        service_data = []
        for line in data.split('\n'):
            line = line.replace("\t", " ")
            if "*" not in line and "//" not in line:
                service_data.append(line)
            if "//" in line:
                service_data.append(line.split("//")[0])
            if "@value" in line:
                if line not in service_data:
                    service_data.append(line.split("/")[0])
    service_data = [i for i in service_data if i != ""]

    return "".join("\n".join(service_data).split('service ')[1:]).split('interface')[0]


def get_interface_data(o_file):
    with open(o_file, 'r', encoding='utf-8') as f:
        data = f.read()
        service_data = []
        for line in data.split('\n'):
            if "*" not in line and "//" not in line:
                service_data.append(line)
            if "//" in line:
                service_data.append(line.split("//")[0])
            if "@value" in line:
                if line not in service_data:
                    service_data.append(line.split("/")[0])
    service_data = [i for i in service_data if i != ""]

    return "".join("\n".join(service_data).split('service ')[1:]).split('interface')[-1]


def get_method_type(o_file, method):
    """
    return: method or event
    """
    _line = []
    _list = get_interface_data(o_file).split(");")
    for j in range(len(_list)):
        line = [i for i in _list[j].split("\n") if i != " " and i != "" and "*" not in i]
        if line:
            if line[-1].split("(")[0].replace("\t", " ").split(" ")[-1] == method:

                _line.append(line[-2])
                if "method" in line[-2]:
                    return "method"
                elif "event" in line[-2]:
                    return "event"
                else:
                    if "method" in line[-3]:
                        return "method"
                    elif "event" in line[-3]:
                        return "event"


def to_json_file(o_file, output_file):
    """
    return json file：
          "service_name": {
             'class_name': {
                'method_name1': {
                    "args_in": "",
                    "args_out": ""
                    },
                'method_name2': {
                    "args_in": "",
                    "args_out": ""
                    }
                }
            }
         }
    """
    result = []
    class_name = []
    method_name = []
    line_list = []
    service_name = os.path.splitext(o_file)[0].split('/')[-1]
    mod_list = get_interface_data(o_file).split("};")
    class_name.append(mod_list[-3].split("\n")[0].split(" ")[1])
    for line in mod_list[-3].split("\n"):
        if ");" in line:
            method_name.append(line.split("(")[0].replace("\t", " ").split(" ")[-1])
            if "\t" in line:
                line = line.replace("\t", " ")
                line_list.append(line)
            else:
                line_list.append(line)

    class_list = []
    method_list = []
    for x in range(len(class_name)):
        for j in range(len(method_name)):
            for line in line_list:
                value = {}
                if line.split("(")[0].split(" ")[-1] == method_name[j]:
                    in_list = []
                    # 抽取函数名的()中内容判定是否有输入
                    p = re.compile(r'[(](.*?)[)]', re.S)
                    p0 = 0
                    if ");" in line:
                        p0 = re.findall(p, line.strip())[0]

                    # 只有输入
                    if p0 and "event" == get_method_type(o_file, method_name[j]):
                        if "," in p0:
                            in_list = p0.split(",")
                        else:
                            in_list.append(p0)
                        out_value = {"out": None}
                        arg = []
                        for p1 in in_list:
                            if p1.split(' ')[0]:
                                in_value = p1.split(' ')[0]
                            else:
                                in_value = p1.split(' ')[-2]

                            if "void" in in_value:
                                arg.append({p1.split(' ')[-1]: "None"})

                            elif "int" in in_value:
                                arg.append({p1.split(' ')[-1]: 0})

                            elif "bool" in in_value:
                                arg.append({p1.split(' ')[-1]: False})

                            elif "string" in in_value:
                                arg.append({p1.split(' ')[-1]: ""})

                            elif "float" in in_value:
                                arg.append({p1.split(' ')[-1]: 0.0})

                            else:
                                type_json = get_arg_type(o_file, in_value)
                                model = get_type_mode(o_file, in_value)
                                if "enum" == get_mode_method(model):
                                    arg.append({p1.split(' ')[-1]: type_json})
                                elif "typedef" in model:
                                    arg_type = [i for i in model.split(' ') if i != ""][-2]
                                    arg.append({p1.split(' ')[-1]: get_arg(o_file, arg_type)})
                                else:
                                    # for _arg in type_json:
                                    arg.append(get_arg(o_file, in_value))

                        value = {
                            'type': get_method_type(o_file, method_name[j]),
                            'arg_in': arg,
                            'arg_out': out_value
                        }

                    # 输入输出都有
                    elif p0 and "method" == get_method_type(o_file, method_name[j]):
                        if "," in p0:
                            in_list = p0.split(",")
                        else:
                            in_list.append(p0)

                        out_value = line.split("(")[0].split(" ")[-2]

                        arg = []
                        for p1 in in_list:
                            if p1.split(' ')[0]:
                                in_value = p1.split(' ')[0]
                            else:
                                in_value = p1.split(' ')[-2]

                            if "void" in in_value:
                                arg.append({p1.split(' ')[-1]: "None"})

                            elif "int" in in_value:
                                arg.append({p1.split(' ')[-1]: 0})

                            elif "bool" in in_value:
                                arg.append({p1.split(' ')[-1]: False})

                            elif "string" in in_value:
                                arg.append({p1.split(' ')[-1]: ""})

                            elif "float" in in_value:
                                arg.append({p1.split(' ')[-1]: 0.0})

                            else:
                                type_json = get_arg_type(o_file, in_value)
                                model = get_type_mode(o_file, in_value)
                                if "enum" == get_mode_method(model):
                                    arg.append({p1.split(' ')[-1]: type_json})
                                elif "typedef" in model:
                                    arg_type = [i for i in model.split(' ') if i != ""][-2]
                                    arg.append({p1.split(' ')[-1]: get_arg(o_file, arg_type)})
                                else:
                                    # for _arg in type_json:
                                    arg.append(get_arg(o_file, in_value))

                        value = {
                            'type': get_method_type(o_file, method_name[j]),
                            'arg_in': arg,
                            'arg_out': get_arg_out_value(o_file, out_value)
                        }

                    # 只有输出
                    elif not p0 and "method" == get_method_type(o_file, method_name[j]):
                        out = [i for i in line.split("(")[0].split(" ") if i != ""]
                        out_value = out[-2]

                        value = {
                            'type': get_method_type(o_file, method_name[j]),
                            'arg_in': {},
                            'arg_out': get_arg_out_value(o_file, out_value)
                        }

                    # 输入输出都为空
                    elif not p0 and "event" == get_method_type(o_file, method_name[j]):
                        value = {
                            'type': get_method_type(o_file, method_name[j]),
                            'arg_in': {},
                            'arg_out': {"out": None}
                        }

                    method_list.append({method_name[j]: value})

        class_list.append({class_name[x]: method_list})

    result.append({service_name: class_list})

    with open(f"{output_file}.json", "w", encoding="utf-8") as fd:
        fd.write(json.dumps(result[0], ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': ')))

    return result[0]


def batch_convert_to_json():
    """
    批量将jidl文件转换成json文件
    """
    print(soa_partner_path)
    jidl_path = os.path.join(soa_partner_path, 'idl/')
    json_path = os.path.join(soa_partner_path, 'json/')

    dir_list = os.listdir(jidl_path)
    print(dir_list)
    for i in range(0, len(dir_list)):
        # 构造路径
        path = os.path.join(jidl_path, dir_list[i])
        print("文件夹: {}".format(path))
        if os.path.isdir(path):
            for file_name in os.listdir(path):
                if os.path.splitext(path + file_name)[-1] != '.jidl':
                    continue
                print(os.path.splitext(path + '/' + file_name)[0])
                try:
                    to_json_file(os.path.join(path, file_name), json_path + file_name.split('.')[0])
                except Exception:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/parse_JiDL/to_json.py")
                    continue


if __name__ == '__main__':
    batch_convert_to_json()

