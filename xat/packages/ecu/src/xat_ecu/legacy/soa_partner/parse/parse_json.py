import json
import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
soa_partner_path = os.path.join(current_path.split("ecu_simulator")[0], "ecu_simulator/soa_partner/")
from tools.parse_JiDL.to_json import *


def write_client_module_header(file_handler, port=16789):
    """
    客户端头部格式定义
    """
    file_handler.write("from threading import Thread" + "\n")
    file_handler.write("import time" + "\n")
    file_handler.write("import socket" + "\n")
    file_handler.write("import json" + "\n")
    # file_handler.write("import logging" + "\n")

    file_handler.write("\n")
    file_handler.write("DEFAULT_PORT = {}".format(port) + "\n")
    file_handler.write("BUFFER_SIZE = 1024 * 1000" + "\n")
    file_handler.write("MESSAGE_LENGTH_BYTES_FMT = '%08x'" + "\n")
    file_handler.write("MESSAGE_LENGTH_BYTES = 4")
    file_handler.write("\n\n\n")


def write_client_class_header(file_handler, service_name, name="Client"):
    file_handler.write("class "+service_name + name + ":\n")
    file_handler.write("\n")
    file_handler.write("    def __init__(self):" + "\n")
    file_handler.write("        self.stop_loop = False" + "\n")
    file_handler.write("        self.running = False" + "\n")
    file_handler.write("        self.tcp_socket_list = []" + "\n")
    file_handler.write("        self.resp_list = []" + "\n")
    file_handler.write("\n")
    base_content_stop(file_handler)
    base_content_listen(file_handler, service_name, name)


def base_content_send_data_to(file_handler):
    file_handler.write("def send_data_to(conn, data):" + "\n")
    file_handler.write("    byte_len = MESSAGE_LENGTH_BYTES_FMT % len(json.dumps(data))" + "\n")
    file_handler.write("    conn.sendall(bytes(byte_len + json.dumps(data), encoding='utf-8'))" + "\n")
    file_handler.write("\n")
    file_handler.write("\n")


def base_content_recv_data_from(file_handler):
    file_handler.write("def recv_data_from(conn):" + "\n")
    file_handler.write("    recv_data = b''" + "\n")
    file_handler.write("    msg_len_bcd = conn.recv(MESSAGE_LENGTH_BYTES * 2)" + "\n")
    file_handler.write("    msg_len = int(msg_len_bcd.decode('utf-8'), 16)" + "\n")
    file_handler.write("    while msg_len > len(recv_data):" + "\n")
    file_handler.write("        data = conn.recv(BUFFER_SIZE)" + "\n")
    file_handler.write("        recv_data += data" + "\n")
    file_handler.write("    return recv_data" + "\n")
    file_handler.write("\n")
    file_handler.write("\n")


def base_content_stop(file_handler):
    file_handler.write("    def stop_handler(self):" + "\n")
    file_handler.write("        self.running = False" + "\n")
    file_handler.write("        for tcp_socket in self.tcp_socket_list:" + "\n")
    file_handler.write("            tcp_socket.close()" + "\n")
    file_handler.write("        self.tcp_socket_list.clear()" + "\n")
    file_handler.write("\n")


def base_content_listen(file_handler, service_name, name):
    file_handler.write("    def start_handler(self, connect_info, handler):" + "\n")
    file_handler.write("        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)" + "\n")
    file_handler.write("        conn.connect(connect_info)" + "\n")
    file_handler.write("        thread = Thread(target=handler, args=(conn, ))" + "\n")
    file_handler.write("        thread.setDaemon(True)" + "\n")
    file_handler.write("        thread.start()" + "\n")
    file_handler.write("        return conn" + "\n")
    file_handler.write("\n")

    if name == "Client":
        file_handler.write("    def send_method_request(self, conn, method_name, args, is_async=False):" + "\n")
        file_handler.write("        req = {" + "\n")
        file_handler.write("            \"action\": \"request\"," + "\n")
        file_handler.write("            \"function\": f\"{method_name}{is_async and 'Async' or ''}\"," + "\n")
        file_handler.write("            \"args\": json.dumps(args)" + "\n")
        file_handler.write("        }" + "\n")
        file_handler.write("        conn.sendall(bytes(json.dumps(req), encoding='utf-8'))" + "\n")
        file_handler.write("        time.sleep(1)" + "\n")
        file_handler.write("\n")
    else:
        file_handler.write("    def send_event_notify(self, conn, event_name, args):" + "\n")
        file_handler.write("        event = {" + "\n")
        file_handler.write("            \"action\": \"event\"," + "\n")
        file_handler.write("            \"function\": f\"Update{event_name}Event\"," + "\n")
        file_handler.write("            \"args\": json.dumps(args)" + "\n")
        file_handler.write("        }" + "\n")
        file_handler.write("        conn.sendall(bytes(json.dumps(event), encoding='utf-8'))" + "\n")
        file_handler.write("        print(\"发布事件通知：{}\".format(event))" + "\n")
        file_handler.write("\n")

    file_handler.write("    def method_run_init(self, service_name, port=16789):" + "\n")
    file_handler.write("        self.running = True" + "\n")
    # file_handler.write("        self.func_type = method_type\n")
    file_handler.write("        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n")
    file_handler.write("        tcp_socket.connect(('127.0.0.1', port))\n")
    file_handler.write("        req = {\n")
    file_handler.write("            \"action\": \"request\",\n")
    file_handler.write("            \"function\": \"get_current_service_list\",\n")
    file_handler.write("            \"args\": None\n")
    file_handler.write("        }\n")
    file_handler.write("        send_data_to(tcp_socket, req)\n")
    file_handler.write("        recv_data = recv_data_from(tcp_socket)\n")
    file_handler.write("        resp1 = json.loads(recv_data.decode(\"utf-8\"))\n")
    file_handler.write("        result = json.loads(resp1['result'])\n")
    #file_handler.write("        print(\"get_current_service_list: {}\".format(result.keys()))\n")

    file_handler.write("        req = {\n")
    file_handler.write("            \"action\": \"request\",\n")
    file_handler.write("            \"function\": \"running_service\",\n")
    file_handler.write("            \"args\": None\n")
    file_handler.write("        }\n")
    file_handler.write("        send_data_to(tcp_socket, req)\n")
    file_handler.write("        recv_data = recv_data_from(tcp_socket)\n")
    file_handler.write("        resp1 = json.loads(recv_data.decode(\"utf-8\"))\n")
    file_handler.write("        result = json.loads(resp1['result'])\n")
    #file_handler.write("        print(\"running_service: {}\".format(result.keys()))\n")

    file_handler.write("        req = {\n")
    file_handler.write("            \"action\": \"request\",\n")
    file_handler.write("            \"function\": \"start_config\",\n")
    file_handler.write("            \"args\": json.dumps({\n")
    file_handler.write("                 service_name: {\n")
    file_handler.write("                     \"role\": \"{}\",\n".format(name.lower()))
    file_handler.write("                     \"name\": \"{}\".format(service_name)\n")
    file_handler.write("                  }\n")
    file_handler.write("            })\n")
    file_handler.write("        }\n")
    file_handler.write("        send_data_to(tcp_socket, req)\n")
    file_handler.write("        recv_data = recv_data_from(tcp_socket)\n")
    file_handler.write("        resp1 = json.loads(recv_data.decode(\"utf-8\"))\n")
    file_handler.write("        result = json.loads(resp1['result'])\n")
    #file_handler.write("        print(\"get_current_service_list: {}\".format(result.keys()))\n")

    file_handler.write("        tcp_socket.close()\n")
    file_handler.write("        time.sleep(1)\n")
    file_handler.write("        window_conn = self.start_handler(\n")
    file_handler.write("            tuple(result[service_name+'_{}']), self.window_handler)\n".format(name.lower()))
    file_handler.write("        self.tcp_socket_list.append(window_conn)\n")
    file_handler.write("        time.sleep(1)\n")
    file_handler.write("        return window_conn\n")
    file_handler.write("\n")


def base_content_client_handler(file_handler):
    file_handler.write("    def window_handler(self, conn):" + "\n")
    file_handler.write("        conn.settimeout(600)" + "\n")
    file_handler.write("        while self.running:" + "\n")
    file_handler.write("            try:" + "\n")
    file_handler.write("                recv_data = conn.recv(BUFFER_SIZE)" + "\n")
    file_handler.write("                if len(recv_data) == 0:" + "\n")
    file_handler.write("                    break" + "\n")
    file_handler.write("                response = json.loads(recv_data.decode(\"utf-8\"))" + "\n")
    file_handler.write("                print(\"收到服务端响应：{}\".format(response))" + "\n")
    file_handler.write("                if response not in self.resp_list:" + "\n")
    file_handler.write("                    self.resp_list.append(response)" + "\n")
    file_handler.write("            except OSError as e:" + "\n")
    file_handler.write("                print(e.__repr__())" + "\n")
    file_handler.write("                print(\"remote end is closed\")" + "\n")
    file_handler.write("                break" + "\n")
    file_handler.write("            except Exception as e:" + "\n")
    file_handler.write("                print(e.__repr__())" + "\n")
    file_handler.write("                continue" + "\n")
    file_handler.write("\n")
    file_handler.write("\n")


def base_content_server_handler(file_handler):
    file_handler.write("    def window_handler(self, conn):" + "\n")
    file_handler.write("        conn.settimeout(600)" + "\n")
    file_handler.write("        while self.running:" + "\n")
    file_handler.write("            try:" + "\n")
    file_handler.write("                recv_data = conn.recv(BUFFER_SIZE)" + "\n")
    file_handler.write("                if len(recv_data) == 0:" + "\n")
    file_handler.write("                    break" + "\n")
    file_handler.write("                req_info = json.loads(recv_data.decode(\"utf-8\"))" + "\n")
    file_handler.write("                print(\"收到方法请求：{}\".format(req_info))" + "\n")
    file_handler.write("                method_all_response(conn, req_info[\"function\"])" + "\n")
    file_handler.write("            except OSError as e:" + "\n")
    file_handler.write("                print(e.__repr__())" + "\n")
    file_handler.write("                print(\"remote end is closed\")" + "\n")
    file_handler.write("                break" + "\n")
    file_handler.write("            except Exception as e:" + "\n")
    file_handler.write("                print(e.__repr__())" + "\n")
    file_handler.write("                continue" + "\n")
    file_handler.write("\n")
    file_handler.write("\n")


def write_method_response(file_handler, function_detail):
    file_handler.write("def method_{}_response(conn, param={}):\n".format(function_detail.name,
                                                                          function_detail.arg_out))
    file_handler.write("    if param is None:" + "\n")
    file_handler.write("        args = \"\"" + "\n")
    file_handler.write("    else:" + "\n")
    file_handler.write("        args = param" + "\n")
    file_handler.write("    resp = {" + "\n")
    file_handler.write("        \"action\": \"response\"," + "\n")
    file_handler.write("        \"function\": f\""+function_detail.name+"\"," + "\n")
    file_handler.write("        \"result\": json.dumps(args)" + "\n")
    file_handler.write("    }" + "\n")
    file_handler.write("    print(\"方法返回结果：{}\".format(json.dumps(resp)))" + "\n")
    file_handler.write("    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))\n")
    file_handler.write("\n")
    file_handler.write("\n")


def write_all_method_response(file_handler, method_list):
    file_handler.write("def method_all_response(conn, method_name):\n")
    for method_detail in method_list:
        file_handler.write("    if method_name == \"{}\":\n".format(method_detail.name))
        file_handler.write("        method_{}_response(conn, {})\n".format(method_detail.name, method_detail.arg_out))
    file_handler.write("\n")
    file_handler.write("\n")


def write_all_event_notify(file_handler, event_list):
    file_handler.write("def event_all_notify(conn, event_name):\n")
    for method_detail in event_list:
        file_handler.write("    if method_name == \"{}\":\n".format(method_detail.name))
        file_handler.write(
            "        method_{}_response(conn, {})\n".format(method_detail.name, method_detail.arg_out))
    file_handler.write("\n")
    file_handler.write("\n")


def write_signal_event_notify(file_handler, event_list):
    for event_detail in event_list:
        file_handler.write("def event_{}_notify(conn, param={}):\n".format(event_detail.name, event_detail.arg_in))
        file_handler.write("    if param is None:" + "\n")
        file_handler.write("        args = \"\"" + "\n")
        file_handler.write("    else:" + "\n")
        file_handler.write("        args = {key: value for pa in param for key, value in pa.items()}" + "\n")
        file_handler.write("    event = {\n")
        file_handler.write("        \"action\": \"event\",\n")
        file_handler.write("        \"function\": f\"Update{}Event\",\n".format(event_detail.name))
        file_handler.write("         \"args\": json.dumps(args)\n")
        file_handler.write("    }\n")
        file_handler.write("    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))\n")
        file_handler.write("    print(\"下发事件通知：{}\".format(event))\n")
        file_handler.write("\n")
        file_handler.write("\n")


def write_all_event_notify(file_handler, event_list):
    file_handler.write("def event_all_notify(conn):\n")
    for event_detail in event_list:
        file_handler.write("    event_{}_notify(conn, args={})\n".format(event_detail.name, event_detail.arg_in))
        file_handler.write("    time.sleep(1)\n")
    file_handler.write("\n")
    file_handler.write("\n")


def write_method_request(file_handler, function_detail):
    file_handler.write("def method_{}_request(conn, param={}, is_async=False):\n".format(function_detail.name,
                                                                                         function_detail.arg_in))
    file_handler.write("    if param is None:" + "\n")
    file_handler.write("        args = \"\"" + "\n")
    file_handler.write("    else:" + "\n")
    file_handler.write("        args = {key: value for pa in param for key, value in pa.items()}" + "\n")
    file_handler.write("    req = {" + "\n")
    file_handler.write("        \"action\": \"request\"," + "\n")
    file_handler.write("        \"function\": f\""+function_detail.name+"{is_async and 'Async' or ''}\"," + "\n")
    file_handler.write("        \"args\": json.dumps(args)" + "\n")
    file_handler.write("    }" + "\n")
    file_handler.write("    print(\"执行方法请求：{}\".format(req))" + "\n")
    file_handler.write("    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))\n")
    file_handler.write("\n")
    file_handler.write("\n")


def write_all_method_request(file_handler, method_list):
    file_handler.write("def method_all_request(conn):\n")
    for method_detail in method_list:
        file_handler.write("    method_{}_request(conn, {})\n".format(method_detail.name, method_detail.arg_in))
        file_handler.write("    time.sleep(1)\n")
    file_handler.write("\n")
    file_handler.write("\n")


def base_content_demo_test(file_handler, service_name, role="Client"):
    file_handler.write("if __name__ == \"__main__\":\n")
    file_handler.write("    {} = {}{}()\n".format(role.lower(), service_name, role))
    file_handler.write("    window_conn = {}.method_run_init(\"{}\")\n".format(role.lower(), service_name))
    if role == "Client":
        file_handler.write("    method_all_request(window_conn)\n")
    else:
        file_handler.write("    event_all_notify(window_conn)\n")
    file_handler.write("    time.sleep(10)\n")
    file_handler.write("    {}.stop_handler()\n".format(role.lower()))
    file_handler.write("    resp = {}.resp_list\n".format(role.lower()))
    file_handler.write("    print(\"方法响应结果：{}\".format(resp))\n")


class function_detail_info:
    """
    函数信息类：method、event
    """
    def __init__(self, name, arg_in, arg_out, func_type):
        self.name = name
        self.arg_in = arg_in
        self.arg_out = arg_out
        self.func_type = func_type


def get_lower_case_name(text):
    """
        将参数名的驼峰形式转为下划线形式
        @text params:
        @return:
    """
    lst = []
    for index, char in enumerate(text):
        if char.isupper() and index != 0:
            lst.append("_")
        lst.append(char)

    return "".join(lst).lower()


def batch_convert_to_client_server():
    """
    批量将json文件转换成client和server脚本
    """
    print("#############################################################################")
    path = os.path.join(soa_partner_path, 'json/')
    output_path = os.path.join(soa_partner_path, 'output/')
    path = "../json"
    for file_name in os.listdir(path):
        function_method_list = []
        function_event_list = []
        print("***********************{}*****************".format(os.path.join(path + "/" + file_name)))
        try:
            short_name = file_name.split('.')[0]
            with open("../json/" + file_name, 'r', encoding='utf-8') as fw:
                injson = json.load(fw)
                functions_info = injson[short_name][0]
                for key in functions_info.keys():
                    functions_info = functions_info[key]
                    break
                for function_info in functions_info:
                    for key, value in function_info.items():
                        function = function_detail_info(key, value["arg_in"], value["arg_out"], value["type"])
                        if value["type"] == 'method':
                            function_method_list.append(function)
                        else:
                            function_event_list.append(function)
            # 创建对应的客户端python文件
            with open(output_path + short_name + "_client.py", "w", encoding='utf-8') as file:
                write_client_module_header(file)
                for function_one in function_method_list:
                    write_method_request(file, function_one)
                write_all_method_request(file, function_method_list)
                base_content_send_data_to(file)
                base_content_recv_data_from(file)
                write_client_class_header(file, short_name)
                base_content_client_handler(file)
                base_content_demo_test(file, short_name)
            # 创建对应的服务端python文件
            with open(output_path + short_name + "_server.py", "w", encoding='utf-8') as file:
                write_client_module_header(file, 6789)
                for function_one in function_method_list:
                    write_method_response(file, function_one)
                write_signal_event_notify(file, function_event_list)
                write_all_event_notify(file, function_event_list)
                write_all_method_response(file, function_method_list)
                base_content_send_data_to(file)
                base_content_recv_data_from(file)
                write_client_class_header(file, short_name, "Server")
                base_content_server_handler(file)
                base_content_demo_test(file, short_name, "Server")
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/parse/parse_json.py")
            print("异常信息：{}".format(e.__str__()))
            continue


if __name__ == "__main__":
    batch_convert_to_client_server()

