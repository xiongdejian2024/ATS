#!/usr/bin/python3
# coding=UTF-8

import os
# import logging
import subprocess
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

from xat_cases.legacy.soa.case_helper.codesrc.components.pressure.pre_env_ioe import IoE_start
from xat_cases.legacy.soa.case_helper.codesrc.components.pressure.wechat import send_in_message, send_out_message, send_wechat_file
from xat_cases.legacy.soa.case_helper.codesrc.public.utils.report import WechatTools
from xat_ecu.legacy.common.logger import logger  as logging
from xat_cases.legacy.soa.case_helper.soa.domain.bgm import *
from xat_cases.legacy.soa.case_helper.soa.domain.cdcq import rm_cdcq_log, config_cdcq
from xat_cases.legacy.soa.case_helper.soa.domain.cdca import rm_cdca_log, check_cdca_is_on
from xat_cases.legacy.soa.case_helper.soa.domain.tcam import rm_tcam_log, check_tcam_is_on
from xat_cases.legacy.soa.case_helper.soa.domain.acu import rm_acu_log
from xat_cases.legacy.soa.case_helper.soa.poweroff_strategy import PoweroffStrategy
from xat_cases.legacy.soa.case_helper.codesrc.components.pressure.utils import hand_usbrelay_on,hand_usbrelay_off

def report_file(script_path, file_path, file_name, index):
    time.sleep(20)
    logging.info(f'开始出报告')

    try:
        _analyse_json(script_path, file_path)
        _analyse_csv(script_path, file_path, index)
    except Exception as e:
        logging.info(f'解析 failed：  {e}')
    # 执行序号加到文档路径中
    doc_path = f'{file_path}/{file_name}-{index}.docx'
    logging.info(f'生成的文档路径：{doc_path}')
    logging.info(doc_path)
    try:
        WechatTools.send(doc_path)
    except Exception as e:
        logging.info(f"发送企业微信 failed{e}")
    return doc_path


def report_message(version, cdca_version, tcam_version, acu_version, index, host_ip, wiki_url, end_flag=False):
    try:
        if end_flag:
            send_out_message(version, cdca_version, tcam_version, acu_version, index, host_ip, wiki_url)
        else:
            send_in_message(version, cdca_version, tcam_version, acu_version, index, host_ip, wiki_url)
    except Exception as e:
        logging.info(f"发送企业微信 failed{e}")


def _analyse_json(script_path, file_path):
    '''
    json转csv
    '''
    try:
        os.chdir(file_path)
        cmd = f'python3 {script_path}/bootes_log_parser.py -p {file_path} --json2csv'
        logging.info(f'cmd222====={cmd}')
        os.system(cmd)
        logging.info(f'csv转换 success')
    except Exception as e:
        logging.info(f'json转csv failed{e}')
        logging.debug(f'json转csv failed{e}')
        return False
    return True


def _analyse_csv(path, file_path, ret):
    '''
    csv转docx
    '''
    try:
        os.chdir(file_path)
        cmd = f'python3 {path}/bootes_log_parser.py -p {file_path} -t {ret}  --csv2docx'
        logging.info(f'csv转docx==={cmd}')
        os.system(cmd)
        logging.info(f'docx转换 success')
    except Exception as e:
        logging.info(f'csv转docx{e}')
        logging.debug(f'csv转docx{e}')
        return False
    return True


def log_once_to_json(path, all_path):
    '''
    子进程转json
    '''
    # try:
    #     p = subprocess.Popen(
    #         f'python3  {path}/bootes_log_parser.py -p {all_path} -t presure show', shell=True)
    # except Exception as e:
    #     logging.debug(f'log to json  failed {e}')
    try:
        cmd = f'python3  {path}/log_analyzer.py --log_path {all_path} --meta_path {all_path} --meta_json {path}/module/meta.json --meta_data --is_bootes'
        p = subprocess.Popen(cmd, shell=True)
        p.wait()
    except Exception as e:
        logging.debug(f'log to json  failed {e}')


def rm_log(bgm_uname, bgm_addr, bgm_pwd, cdca_addr, tcam_pwd, acu_name, acu_pwd, index,item=None):
    '''
    获取日志后清理日志
    '''
    logging.info("开始清理bgm日志")
    rm_bgm_log(bgm_uname, bgm_pwd, bgm_addr, index, item)
    logging.info("开始清理cdcq日志")
    rm_cdcq_log(bgm_addr, bgm_pwd, index,item)
    logging.info("开始清理tcam日志")
    rm_tcam_log(bgm_addr, tcam_pwd, index,item)
    logging.info("开始清理cdca日志")
    rm_cdca_log(cdca_addr, index,item)
    logging.info("开始清理acu日志")
    rm_acu_log(bgm_addr, bgm_pwd, acu_pwd, acu_name, index,item)



def first_rm(bgm_uname, bgm_addr, bgm_pwd, cdca_addr, tcam_pwd, acu_name, acu_pwd, tc_config, ipdu, nucapp=None):
    """
    第一次清理日志方法,tcam弃用adb方式，更换为ssh方式，
    tcam登录判断暂时不需要，之前加入判断是因为tcam上电时间周期太长，上电后立即连接可能会连不上
    """
    logging.info("开始进行第一次日志清理")
    item = {
      "poweroff": [
        "bgm",
        "cdc",
        "tcam",
        "acu"
      ],

      "times": 1,
      "space": 6
    }
    logging.info(f"cdca的IP地址为: {cdca_addr}")
    res_cdca = check_cdca_is_on(cdca_addr)
    if res_cdca == 0:
        logging.info("cdca号已查询到")
        index = 0
        rm_log(bgm_uname, bgm_addr, bgm_pwd, cdca_addr, tcam_pwd, acu_name, acu_pwd, index,item)
        
        logging.info("第一次 清完日志 四域上下电")
        ltg= PoweroffStrategy(item,tc_config=tc_config,nucapp=nucapp)
        logging.info("四域开始重启")
        ltg.sd_reboot_domian(ipdu)
        time.sleep(180)
        
    else:
        logging.info(f'Adb -s cdca_devices shell Failed，重新上电尝试重连')
        ltg= PoweroffStrategy(item,tc_config,nucapp=nucapp)
        ltg.sd_reboot_domian(ipdu)
        time.sleep(180)
        from soa_lib.interface.nuc_app import get_obd_ip
        logging.info("重新上下电后重新回去bgm的ip")
        bgm_addr = get_obd_ip()
        cdca_addr = f"{bgm_addr}:1313"
        IoE_start(bgm_addr, bgm_uname, bgm_pwd, force_flag=True)
        first_rm(bgm_uname, bgm_addr, bgm_pwd, cdca_addr, tcam_pwd, acu_name, acu_pwd, tc_config, nucapp)


if __name__ == '__main__':
    all_path = "/root/TestDev/pressure_log/240327-195931-1-bootes1.4.1r703-172.18.128.138/6"
    #log_once_to_json("/root/TestDev/sat/soa_lib/codesrc/components/log_analyzer", all_path)
    docx_path = report_file("/root/TestDev/sat/soa_lib/codesrc/components/pressure", "/root/TestDev/pressure_log/240331-195931-1-bootes1.4.1r703-172.18.128.138", "240331-195931-1-bootes1.4.1r703-172.18.128.138", "四域依次休眠唤醒4次")
    logging.info(f'docx_path ===== {docx_path}')