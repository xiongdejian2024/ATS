import json
import math
import os
import sys
from datetime import datetime

import paramiko
import yaml

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path.split("sat")[0], "sat"))
from xat_ecu.legacy.common.logger import logger, Logger


def exec_cmd_indirect_on_ecu(local, des, cmd_str):
    """
    SSH嵌套登录后，执行linux指令：
    先SSH到local，然后再通过local机SSH到des主机上，并在des主机上执行命令字符串
    返回值：在在des主机上执行命令字符串的结果
    """
    vm = paramiko.SSHClient()
    vm.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        logger.info("开始连接BGM.....")
        vm.connect(local.ip, username=local.username, password=local.password, timeout=5)
    except Exception:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/monitor/exec_cmd_on_ecu_indirect.py")
        logger.info(f"BGM直连失败，请检查环境信息！！！")
        return False, f"BGM直连失败，请检查环境信息！！！"
    if vm.get_transport().is_active():
        vm_transport = vm.get_transport()
        des_addr = (des.ip, des.port)
        local_addr = (local.ip, local.port)
        try:
            logger.info(f"开始通过BGM连接ecu：{des.ip}")
            vm_channel = vm_transport.open_channel("direct-tcpip", des_addr, local_addr)
        except Exception:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/monitor/exec_cmd_on_ecu_indirect.py")
            logger.info(f"ECU桥接失败，请检查环境信息！！！")
            return False, "ECU桥接失败，请检查环境信息！！！"
        j_host = paramiko.SSHClient()
        j_host.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        j_host.connect(des.ip, username=des.username, password=des.password, sock=vm_channel)
        if j_host.get_transport().is_active():
            try:
                stdin, stdout, stderr = j_host.exec_command(cmd_str)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/monitor/exec_cmd_on_ecu_indirect.py")
                logger.info("远程执行命令失败：{}".format(e.__str__()))
                return False, "连接跳板机失败 ！！！"
            res = stdout.read()
            logger.info("命令执行结果-stdout：{}".format(res))
            logger.info("命令执行结果-stderr：{}".format(stderr.read()))
            j_host.close()
            vm.close()
            print(res.decode('UTF-8'))
            return True, res.decode('UTF-8')
        else:
            j_host.close()
            vm.close()
            logger.info("连接跳板机失败，但是连接目标主机失败 ！！！")
            return False, "连接跳板机失败，但是连接目标主机失败 ！！！"
    else:
        vm.close()
        logger.info("连接跳板机失败 ！！！")
        return False, "连接跳板机失败 ！！！"


class machine_info:
    """
    台架SSH登录信息：IP、端口、账户、密码
    """
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password


def dict_to_json(dict_obj):
    return json.dumps(dict_obj, ensure_ascii=False, sort_keys=False, indent=4)


def now_time():
    dt = datetime.utcnow()
    dt_str = dt.strftime('%Y-%m-%d %H:%M:%S')
    return dt_str


if __name__ == "__main__":
    logger = Logger().get_logger("test")

    bgm_client = machine_info('169.254.1.1', 22, "root", "mars1bgm")
    tcam_client = machine_info('172.16.5.31', 22, "root", "oelinux123")

    exec_cmd_indirect_on_ecu(bgm_client, tcam_client, sys.argv[1])
