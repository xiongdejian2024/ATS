# -*- coding: utf-8 -*-

"""
@Time    : 2022/6/19 13:26 下午
@Author  : songjian.lin
@Email   : songjian.lin@jiduauto.com
"""
import os
import uuid

import allure

from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.time_handle import get_time_str_year_month_day
from xat_ecu.legacy.interface.baidu_bos.bos_api import BosApi
from xat_ecu.legacy.interface.youzi.youzi import YouZiClient
from framework.automotive.utils.data_type import EcuInfo


def get_class_begin_bgm_log(ssh, ecu: EcuInfo):
    s2s_log_cmd = "ls -lrt /log/ | grep 'jetlog_s2s ->' | awk '{print $11}'"
    s2s_log = ssh.type_commands(s2s_log_cmd)
    if s2s_log:
        s2s_log = s2s_log.replace("/log/", "")
    logger.info(f"当前的s2slog为{s2s_log}")
    messages_log_cmd = "ls -lrt /log/ | grep 'jetlog_messages ->' | awk '{print $11}'"
    messages_log = ssh.type_commands(messages_log_cmd)
    logger.info(f"当前的messages_log为{messages_log}")
    if messages_log:
        messages_log = messages_log.replace("/log/", "")
    bts_log_cmd = "ls -lrt /log/  | grep 'jetlog_bts ->' | awk '{print $11}'"
    bts_log = ssh.type_commands(bts_log_cmd)
    logger.info(f"当前的bts_log为{bts_log}")
    if bts_log:
        bts_log = bts_log.replace("/log/", "")
    ecu.class_bgm_log["s2s_log"] = s2s_log
    ecu.class_bgm_log["messages_log"] = messages_log
    ecu.class_bgm_log["bts_log"] = bts_log


def get_class_after_bgm_log(ssh, ecu: EcuInfo):
    """如果当前类里面的用例执行失败，则拷贝类执行期间所有的log到上位机"""
    logger.info(f"class_uniq: {ecu.class_uuid}")
    if ecu.class_case_fail_flag:
        res = os.system(f'mkdir -p /root/fail_case_log/{ecu.class_uuid}')
        if res == 0:
            logger.info("===================================================================")
            s2s_log_cmd = "ls -lrt /log/ | grep 'jetlog_s2s' |grep -v 'jetlog_s2s ->'|grep -v grep| awk '{print $9}'"
            s2s_log_list = ssh.type_commands(s2s_log_cmd).split("\n")
            for s2s_log in s2s_log_list:
                # logger.info(s2s_log)
                if s2s_log:
                    s2s_log = s2s_log.replace("/log/", "")
                    if compare_bgm_log(s2s_log, ecu.class_bgm_log["s2s_log"], "jetlog_s2s"):
                        ssh.scp_bgm_file_to_local(f"/log/{s2s_log}", f"/root/fail_case_log/{ecu.class_uuid}/{s2s_log}")
                        logger.info(f"jetlog_s2s newer：{s2s_log}")
            logger.info("===================================================================")
            msg_log_cmd = "ls -lrt /log/ | grep 'jetlog_messages' " \
                          "|grep -v 'jetlog_messages ->'|grep -v grep| awk '{print $9}'"
            messages_log_list = ssh.type_commands(msg_log_cmd).split("\n")
            for messages_log in messages_log_list:
                logger.info(messages_log)
                if messages_log:
                    messages_log = messages_log.replace("/log/", "")
                    if compare_bgm_log(messages_log, ecu.class_bgm_log["messages_log"], "jetlog_messages"):
                        ssh.scp_bgm_file_to_local(f"/log/{messages_log}",
                                                  f"/root/fail_case_log/{ecu.class_uuid}/{messages_log}")
                        logger.info(f"jetlog_messages newer：{messages_log}")

            logger.info("===================================================================")
            bts_log_cmd = "ls -lrt /log/ | grep 'jetlog_bts' |grep -v 'jetlog_bts ->'|grep -v grep| awk '{print $9}'"
            bts_log_list = ssh.type_commands(bts_log_cmd).split("\n")
            for bts_log in bts_log_list:
                logger.info(bts_log)
                if bts_log:
                    bts_log = bts_log.replace("/log/", "")
                    if compare_bgm_log(bts_log, ecu.class_bgm_log["bts_log"], "jetlog_bts"):
                        ssh.scp_bgm_file_to_local(f"/log/{bts_log}", f"/root/fail_case_log/{ecu.class_uuid}/{bts_log}")
                        logger.info(f"bts_log newer：{bts_log}")
            u = uuid.uuid4()
            bgm_log_zip = f"/root/fail_case_log/{ecu.class_uuid}/bgm_log_{u}.zip"
            res = os.system(
                f"cd /root/fail_case_log/{ecu.class_uuid};zip -r bgm_log_{u}.zip ./*")
            if res == 0:
                logger.info("bgm日志压缩成功")
            else:
                logger.error(f"bgm日志压缩失败 命令行返回值: {res}")
            if os.path.exists(bgm_log_zip):
                # allure.attach.file(bgm_log_zip, 'bgm日志', 'application/zip', 'zip')
                bos_client = BosApi()
                try:
                    remote_link = bos_client.put_and_get_url(
                        file_path=bgm_log_zip,
                        target_path=f'SOA/allure_report/{get_time_str_year_month_day()}')
                except Exception as e:
                    logger.exception(f"bgm日志上传bos失败: {e}")
                    allure.attach.file(bgm_log_zip, 'bgm日志', 'application/zip', 'zip')
                else:
                    allure.attach(remote_link, 'bgm日志', allure.attachment_type.URI_LIST)
                return bgm_log_zip
    else:
        logger.info("释放 class文件的BGM 日志创建失败")


def compare_bgm_log(curr_file_name, base_name, index_name):
    try:
        curr_num = curr_file_name.replace(index_name, "").split("_")[0]
        base_num = base_name.replace(index_name, "").split("_")[0]

        if int(curr_num) >= int(base_num):
            return True
        else:
            return False
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bgm_helper.py")
        logger.info(f"当前文件名：{curr_file_name}， 基础文件{base_name}， 前缀：{index_name}")
        return False
