# -*- coding: utf-8 -*-
"""
@File        : change_bgm_env.py
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/9/6 10:26
@Description :

"""

import os
import sys
import time
import datetime
import json
import operator
import threading
import time
from socket import *

from time import sleep


from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.bus_app import BusApp
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.config.path import CONFIG_DIR_PATH
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.ecu_sim.parse_tb_config import ParseTBConfig


def rese_bgm(nucapp):
    '''
    重启BGM
    @param nucapp:
    @return:
    '''
    if nucapp:
        # 重启
        time.sleep(3)
        nucapp.bgm_power_off()
        time.sleep(2)
        nucapp.bgm_power_on()
        logger.info(f"bgm重启延时{25}s")
        time.sleep(25)
    else:
        try:
            tb_path = os.path.join(CONFIG_DIR_PATH, "willow_bgm_flash_config.yaml")
            tb_config = ParseTBConfig(tb_path)
            sd_tc_config = tb_config.yaml_content

            sd_tester = Sd_Tester(**sd_tc_config)
            sd_tester.diagnostic_client_sim_start()
            sleep(0.5)
            sd_tester.update_serverdoipid(0x1002)
            sleep(0.5)
            sd_tester.send_data([0x11, 0x81])
            time.sleep(0.5)
            sd_tester.diagnostic_client_sim_close()
            logger.info(f"bgm重启延时{25}s")
            time.sleep(25)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/bgm/bgm_env/change_bgm_env.py")
            sd_tester.diagnostic_client_sim_close()
            logger.warning(f"重启失败==》》{str(e)}")
            assert 0, "修改成功bgm 配置成功，重启失败，可能无法生效"


def ssh_cmd(ssh_obj, cmd, repeat_times=3):
    """
    ssh执行指定指令,可配置重试次数
    @param ssh_obj: ssh对象
    @param cmd: 指令
    @param repeat_times: 如果上一个指令未执行成功，则重复执行次数
    """
    while repeat_times:
        ssh_obj.type_commands(cmd)
        if ssh_obj.type_commands("echo $?") != '0':  # 表示上一条指令未执行成功
            repeat_times -= 1
            sleep(1)
        else:
            break
    else:
        assert False, "指令执行失败"


def ssh_cp_file_to_bgm(ssh_obj, local_file, bgm_path, repeat_times=3):
    """
    复制本地文件至bgm中,可配置重试次数
    @param ssh_obj: ssh对象
    @param local_file: 本地文件
    @param bgm_path: 复制到bgm的路径
    @param repeat_times: 如果上一个指令未执行成功，则重复执行次数
    """
    while repeat_times:
        ssh_obj.scp_local_file_to_bgm(local_file, bgm_path=bgm_path)
        if ssh_obj.type_commands("echo $?") != '0':
            logger.info("复制文件失败重试一次")
            repeat_times -= 1
        else:
            break
    else:
        assert False, "文件复制失败"


def change_bgm_config(nucapp=None, **kwargs):
    '''
    修改bgm的配置文件
    @param nucapp: 传参 则使用继电器重启，不传则诊断重启
    @param kwargs:
    @param s2s_path: 推送指定路径的s2s.json到bgm路径下
    @param bgm_inter_enable: 是否修改配置，使能域内服务跨域调用
    @return:
    '''
    debug_path = kwargs.get("debug_path", None)
    bgm_app_env_path = kwargs.get("bgm_app_env_path", None)
    s2s_path = kwargs.get("s2s_path", None)
    bgm_inter_enable = kwargs.get("bgm_inter_enable", None)  # 是否使能bgm内部服务的跨域调用，使能则置True

    config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')

    bgm_ssh = BGM_SSH()
    # 切换 启动模式
    cmd = "cat /sys/power/sys_resumed"
    ret = bgm_ssh.type_commands(commands=cmd, output=False, root_permission=True, ).strip()
    if ret and int(ret[0]) == 1: # 返回"1"则代表STD启动
        bgm_ssh.type_commands("/app/bin/swdl -nw 10 1")  # 切换冷启

    # 复制文件夹，因为debug.sh已经将配置路径从/app/etc改成/data/app/etc
    ssh_cmd(bgm_ssh, "cp /app/etc/ /data/app/ -r")


    # 删除计数文件，否则计数到20 debug 文件会丢失
    bgm_ssh.delete_debug_script_executed_count()

    if debug_path is None:
        debug_path = os.path.join(config_dir, 'debug.sh')
    ssh_cp_file_to_bgm(bgm_ssh, local_file=debug_path, bgm_path="/data/")

    if bgm_app_env_path is None:
        bgm_app_env_path = os.path.join(config_dir, 'bgm_app_env.sh')
    ssh_cp_file_to_bgm(bgm_ssh, local_file=bgm_app_env_path, bgm_path="/data/app/etc/")

    if s2s_path is None:
        s2s_path = os.path.join(config_dir, 's2s.json')
    ssh_cp_file_to_bgm(bgm_ssh, local_file=s2s_path, bgm_path="/data/app/etc/")

    if bgm_inter_enable:
        # process_config_json = os.path.join(config_dir, 'process_config.json')
        service_monitor_json = os.path.join(config_dir, 'service_monitor.json')
        # bgm_ssh.scp_bgm_file_to_local("/data/etc/process_config.json", process_config_json)
        bgm_ssh.scp_bgm_file_to_local("/app/etc/service_monitor.json", service_monitor_json)

        # 根据bgm配置文件使能域内RKECtrlService和BGM_InterCommService        
        with open(service_monitor_json, 'r') as file:
            data = json.load(file)
        for service in data['service_list']:
            if service['service_id'] == 'RKECtrlService':
                service['service_addr_tcp'] = ["tcp://172.16.5.1:25011"]
                break
        for service in data['service_list']:
            if service['service_id'] == 'BGM_InterCommService':
                service['service_addr_tcp'] = ["tcp://172.16.5.1:25014"]
                break
        with open(service_monitor_json, 'w') as file:
            file.write(json.dumps(data))
        
        # ssh_cp_file_to_bgm(bgm_ssh, local_file=process_config_json, bgm_path="/data/app/etc/")
        ssh_cp_file_to_bgm(bgm_ssh, local_file=service_monitor_json, bgm_path="/data/app/etc/")
    
    cdm = "sync"
    bgm_ssh.type_commands(cdm)

    rese_bgm(nucapp)


def recover_bgm_config(nucapp=None, **kwargs):
    '''
    恢复bgm的配置文件
    @param nucapp: 传参 则使用继电器重启，不传则诊断重启
    @param kwargs:
    @return:
    '''

    bgm_ssh = BGM_SSH()
    # 切换 启动模式
    cmd = "ls /data/"
    ret = bgm_ssh.type_commands(cmd)
    name_List = ret.split()
    logger.warning(f"name_List=》》{name_List}")
    if "debug.sh" in name_List:
        # 删除debug.sh 文件
        cdm = "rm -rf /data/debug.sh"
        bgm_ssh.type_commands(cdm)

        # cdm = "rm -rf /data/app/etc"
        # bgm_ssh.type_commands(cdm)

        cmd = "cat /sys/power/sys_resumed"
        ret = bgm_ssh.type_commands(commands=cmd, output=False, root_permission=True, ).strip()
        logger.info(f"执行指令{cmd}》》》{ret}")
        if ret and int(ret[0]) == 0:
            cdm = " /app/bin/swdl -nw 10 0"
            bgm_ssh.type_commands(cdm)

        cdm = "sync"
        bgm_ssh.type_commands(cdm)

        rese_bgm(nucapp)


def mock_mcu_listen_pdu(pdu_id, pdu_length, pdu_data: list, result, timeout_second=10):
    """
    Mock MCU给MPU发送TCP报文
    @param pdu_id:
    @param pdu_length:
    @param pdu_data: 类型为列表，长度等于pdu_length
    @param result
    @param timeout_second
    @return:
    """
    if len(pdu_data) == pdu_length:
        HOST = '172.16.5.21'
        PORT = 30501
        PORT2 = 30500
        ADDRESS = (HOST, PORT)
        ADDRESS2 = (HOST, PORT2)
        tcpServerSocket = socket(AF_INET, SOCK_STREAM)
        tcpServerSocket2 = socket(AF_INET, SOCK_STREAM)
        tcpServerSocket.bind(ADDRESS)
        tcpServerSocket2.bind(ADDRESS2)
        tcpServerSocket2.listen(50)
        tcpServerSocket.listen(50)
        try:
            logger.info('服务器正在运行，等待客户端连接...')
            client_socket2, client_address2 = tcpServerSocket2.accept()

            before_thread = threading.Thread(target=mock_mcu_listen_result, args=(client_socket2, pdu_id, pdu_length,
                                                                                  pdu_data, result, timeout_second))
            before_thread.setDaemon(True)
            before_thread.start()
            logger.info('客户端{}已连接！'.format(client_address2))
            try:
                try:
                    logger.info('服务器正在运行，等待客户端连接...')
                    client_socket, client_address = tcpServerSocket.accept()
                    logger.info('客户端2{}已连接！'.format(client_address))
                    time.sleep(timeout_second)
                    client_socket.close()
                finally:
                    tcpServerSocket.close()
            finally:
                client_socket2.close()
        finally:
            tcpServerSocket2.close()
    else:
        logger.info("入参格式错误：pdu_data: 类型为列表，长度等于pdu_length")


def mock_mcu_listen_result(m_sock, pdu_id, pdu_length, pdu_data: list, result: dict, timeout_second):
    """
    Mock MCU监听MPU发送过来的TCP报文
    @param m_sock:
    @param pdu_id:
    @param pdu_length:
    @param pdu_data: 类型为列表，长度等于pdu_length
    @param result 抓取结果
    @param timeout_second: 超时时间，单位秒
    @return:
    """
    time_start = time.time()
    listen_flag = True
    while listen_flag:
        data = m_sock.recv(1024 * 101)
        list_data = list(data)
        my_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        time_now = time.time()
        listen_flag = (time_now-time_start) < timeout_second
        expected_result = []
        expected_result.extend(convert_int_to_list(pdu_id, 4))
        expected_result.extend(convert_int_to_list(pdu_length, 4))
        expected_result.extend(pdu_data)
        if operator.eq(list_data, expected_result):
            logger.info(list_data)
            result[my_time] = list_data


def mock_mcu_send_pdu(pdu_id, pdu_length, pdu_data: list):
    """
    Mock MCU给MPU发送TCP报文
    @param pdu_id:
    @param pdu_length:
    @param pdu_data: 类型为列表，长度等于pdu_length
    @return:
    """
    if len(pdu_data) == pdu_length:
        HOST = '172.16.5.21'
        PORT = 30501
        PORT2 = 30500
        ADDRESS = (HOST, PORT)
        ADDRESS2 = (HOST, PORT2)
        # 创建监听socket
        tcpServerSocket = socket(AF_INET, SOCK_STREAM)
        tcpServerSocket2 = socket(AF_INET, SOCK_STREAM)
        # 绑定IP地址和固定端口
        tcpServerSocket.bind(ADDRESS)
        tcpServerSocket2.bind(ADDRESS2)
        # logger.info("服务器启动，监听端口{}...".format(ADDRESS[1]))
        # logger.info("服务器启动，监听端口{}...".format(ADDRESS2[1]))
        tcpServerSocket2.listen(50)
        tcpServerSocket.listen(50)
        try:
            logger.info('服务器正在运行，等待客户端连接...')
            client_socket2, client_address2 = tcpServerSocket2.accept()
            # before_thread = threading.Thread(target=mock_mcu_listen_result, args=(client_socket2, 21, 1, [0x05]))
            # before_thread.setDaemon(True)
            # before_thread.start()
            logger.info('客户端{}已连接！'.format(client_address2))
            try:
                try:
                    logger.info('服务器正在运行，等待客户端连接...')
                    client_socket, client_address = tcpServerSocket.accept()
                    logger.info('客户端2{}已连接！'.format(client_address))
                    time.sleep(10)
                    try:
                        data1 = []
                        data1.extend(convert_int_to_list(str(pdu_id), 4))
                        data1.extend(convert_int_to_list(str(pdu_length), 4))
                        data1.extend(pdu_data)
                        client_socket.send(bytes(data1))
                        logger.info('发送消息 {} 至 {}'.format(data1, client_address))
                    finally:
                        client_socket.close()
                finally:
                    tcpServerSocket.close()
            finally:
                client_socket2.close()
        finally:
            tcpServerSocket2.close()
    else:
        logger.info("入参格式错误：pdu_data: 类型为列表，长度等于pdu_length")


def convert_int_to_list(input_str, length):
    a = int(input_str)
    if 0 <= a <= 2147483647:
        result = hex(a)[2::].upper()
        first = []
        for _ in range(length):
            first.append(0)
        index = len(result)
        i = len(first)
        while True:
            if index - 2 >= 0:
                first[i - 1] = int(result[index - 2:index], 16)
            elif index - 2 == -1:
                first[i - 1] = int(result[index - 1:index], 16)
            else:
                break
            i -= 1
            index -= 2
        return first


if __name__ == '__main__':
    recover_bgm_config()
    # change_bgm_config()
