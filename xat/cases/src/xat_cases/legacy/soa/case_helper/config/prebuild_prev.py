# -*- coding: utf-8 -*-
"""
@File        : 
@Author      : 
@Time        : 2023/05/10 15:00 PM
@Description : Test s2s interface about bonnet function
"""
import os
from xat_ecu.legacy.common.logger import logger


def download_file_from_soasdk(file_name, localpath='/root/test_data'):
    '''
    下载文件
    :param localpath:
    :param file_name:
    :return:
    '''
    if not os.path.exists(localpath):
        os.makedirs(localpath)
    file_path = os.path.join(localpath, file_name)
    if os.path.isfile(file_path):
        pass
    else:
        cmd = __import__("os").environ['XAT_CREDENTIAL_SCAN_6EC87DFBCE6034433ECD']
        os.system(cmd)


def change_bgm_config(bgm_ssh, sd_tester):
    '''
    修改bgm的配置文件
    @return:
    '''
    download_file_from_soasdk("1.1Udp_unvlan_revise_mac_revise_ip.pcap")
    # 切换 启动模式
    cmd = "cat /sys/power/sys_resumed"
    ret = bgm_ssh.type_commands(commands=cmd, output=False, root_permission=True, ).strip()
    logger.info(f"执行指令{cmd}》》》{ret}")
    if ret and int(ret[0]) == 1:
        cdm = " /app/bin/swdl -nw 10 1"
        bgm_ssh.type_commands(cdm)
    # 移动文件件
    cdm = "cp /app/etc/ /data/app/ -r"
    bgm_ssh.type_commands(cdm)
    cdm = "rm /data/debug_script_executed_count"
    bgm_ssh.type_commands(cdm)
    local_path = os.path.join(os.getcwd(), 'case_helper/config/debug.sh')
    logger.info(f"local_path=====》》{local_path} ")
    bgm_ssh.scp_local_file_to_bgm(local_path, bgm_path="/data/")
    local_path = os.path.join(os.getcwd(), 'case_helper/config/bgm_app_env.sh')
    bgm_ssh.scp_local_file_to_bgm(local_path, bgm_path="/data/app/etc/")
    local_path = os.path.join(os.getcwd(), 'case_helper/config/s2s.json')
    bgm_ssh.scp_local_file_to_bgm(local_path, bgm_path="/data/app/etc/")

    # 校验下是否修改成功
    # 判断是否有debug.sh 文件
    cmd = "ls /data/"
    ret = bgm_ssh.type_commands(cmd)
    if "debug.sh" not in ret:
        assert 0, "debug.sh 未上传成功"
    cmd = "cat /data/app/etc/bgm_app_env.sh"
    ret = bgm_ssh.type_commands(cmd)
    if "export ENV_CONFIG_PATH=/data/app/etc/" not in ret:
        assert 0, "bgm_app_env.sh 未修改成功"
    cmd = "cat /data/app/etc/s2s.json"
    ret = bgm_ssh.type_commands(cmd)
    if "169.254.93.253" not in ret:
        assert 0, "s2s.json 未修改成功"
    sd_tester.send_data([0x11, 0x81])


def recover_bgm_config(bgm_ssh, sd_tester):
    '''
    恢复 bgm 配置
    @return:
    '''
    # 切换 启动模式
    cmd = "cat /sys/power/sys_resumed"
    ret = bgm_ssh.type_commands(commands=cmd, output=False, root_permission=True, ).strip()
    logger.info(f"执行指令{cmd}》》》{ret}")
    if ret and int(ret[0]) == 0:
        cdm = " /app/bin/swdl -nw 10 0"
        bgm_ssh.type_commands(cdm)
    # 删除debug.sh 文件
    cdm = "rm -rf /data/debug.sh"
    bgm_ssh.type_commands(cdm)
    # 校验下是否修改成功
    # 判断是否有debug.sh 文件
    cmd = "ls /data/"
    ret = bgm_ssh.type_commands(cmd)
    if "debug.sh" in ret:
        assert 0, "debug.sh 未删除成功"
    sd_tester.send_data([0x11, 0x81])
