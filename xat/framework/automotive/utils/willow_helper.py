#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :willow_helper.py
@time         :2/8/24 17:09
@author       :dejian.xiong@jiduauto.com
@description  :
"""
import json
import os
import re
import threading
import time
from typing import Dict

import requests
from xat_ecu.legacy.common import exception_error
from xat_ecu.legacy.common.file_handle import FileHandle
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.time_handle import get_time_str_year_month
from xat_ecu.legacy.interface.nuc_app import exec_shell


from framework.automotive.utils.conftest_helper import convert_version_format, parent_dir


class WillowHelper:
    def __init__(self):
        self.slave_run_url = 'https://willow.jiduprod.com/api/willow-service/flow/flow/{}/run/'
        self.headers = {
            'Authorization': __import__("os").environ.get('XAT_CREDENTIAL_PYTEST___UTILS_WILLOW_HELPER_PY_AUTHORIZATION', "")
        }

    def get_willow_file_path(self, **kwargs):
        '''
        获取 最近的 willow 文件
        @return:
        '''
        if not ("willow" in parent_dir.lower() or "testdev" in parent_dir.lower()):
            return None
        save_num = kwargs.get("save_num", 20)
        # 存放 willow_log 的路径
        willow_log_path = kwargs.get("willow_log_path", "/root/autotest/willow/")
        willow_log_filename_len = kwargs.get("willow_log_filename_len", 36)
        # 查找文件
        cmd = f"cd {willow_log_path};ls -lrt"
        result = exec_shell(cmd)
        data = result["output"]
        error = result["error"]
        try:
            if data:
                output_lis = data.split("\n")
                name_list = [na.split(' ')[-1] for na in output_lis[1:]]
                name_list = [i for i in name_list if i.strip()]
                name_list.reverse()
                logger.info(f"len={len(name_list)} name_list={name_list}")
                # 需要保留的 日志
                save_log_list = []
                for namestr in name_list:
                    if namestr.endswith('zip'):
                        continue
                    if len(save_log_list) >= save_num:
                        break
                    save_log_list.append(namestr)
                save_log_list.append('distributed')
                logger.info(f"删除多余文件保留最近修改的{save_num}个文件==》{save_log_list}")
                # 删除 文件
                for del_name in name_list:
                    if del_name in save_log_list:
                        continue
                    path = os.path.join(willow_log_path, del_name)
                    logger.info(f"删除的文件为 path={path}")
                    cmd = f"rm -rf {path}"
                    # os.system(cmd)
                    exec_shell(cmd)
                # 返回最新文件
                logger.info(f"current_path:{parent_dir}")
                if "testdev" in parent_dir.lower():
                    willow_file_lis = [
                        namestr
                        for namestr in name_list
                        if len(namestr) == willow_log_filename_len
                    ]
                    path = os.path.join(willow_log_path, willow_file_lis[0])
                    logger.info(f"获取到最新的文件夹path为{path}")
                    return path
                # 返回当前路径
                if "willow" in parent_dir.lower():
                    path = os.path.dirname(parent_dir)
                    logger.info(f"获取当前willow运行路径{path}")
                    return path
        except Exception as e:
            logger.exception(f"未找到最新 willow 文件 {str(e)}")
        logger.info(f"未找到最新 willow 文件{error}")
        return None

    def check_is_willow(self):
        # 新 ---- willow任务直接使用固定的 仓库测试，不拉代码，避免因网络原因导致代码拉不下来；
        result = None
        willow_task_path = ""
        willow_report_path = ""
        willow_report_summary_path = ""
        time_now_year_month = get_time_str_year_month()

        willow_path = self.get_willow_file_path()
        if willow_path:
            willow_task_path = os.path.join(willow_path, "task.json")
            willow_report_path = os.path.join(willow_path, "report")
            willow_report_summary_path = os.path.join(
                willow_report_path, "report_summary.json"
            )
            if os.path.exists(willow_task_path):
                result = True
                FileHandle.makedirs(willow_report_path)
                os.system("touch {}".format(willow_report_summary_path))
                with open(willow_task_path, "r") as f:
                    task = json.load(f)
                    start = task.get("start")
                    if start == False:
                        raise RuntimeError(
                            "The previous process is abnormal,  don't need to run"
                        )

        return (
            result,
            willow_task_path,
            willow_report_summary_path,
            willow_report_path,
            time_now_year_month,
        )

    def get_willow_config_for_feishu(self, domain_version_info, willow_task_path):
        with open(willow_task_path, "r") as task_json:
            task = json.load(task_json)
            job_type = task.get("job_type", "")
            case_type = task.get("case_type", "")
            sheet_name = task.get("sheet_name", "")
            job_owner = task.get("job_owner", "")
            fail_case_sheet_name = task.get("fail_case_sheet_name", "")
            fail_case_document_id = task.get("fail_case_document_id", "")
            feishu_rule_key = task.get("feishu_rule_key")
            try:
                if isinstance(domain_version_info.get("software_version"), dict):
                    feishu_version_bgm = domain_version_info.get("software_version").get("BGM", "")
                else:
                    feishu_version_bgm = domain_version_info.get("software_version")
                if feishu_version_bgm:
                    feishu_version_list_bgm = feishu_version_bgm.split(" ")
                    feishu_version_bgm = "V" + feishu_version_list_bgm[0][-3:] + " " + feishu_version_list_bgm[1]
                    feishu_version_bgm = convert_version_format(feishu_version_bgm)
            except Exception as e1:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/willow_helper.py")
                logger.warning(f"BGM 版本获取时异常：{e1.__repr__()}")
                feishu_version_bgm = ""

            try:
                if isinstance(domain_version_info.get("software_version"), dict):
                    feishu_version_tcam = domain_version_info.get("software_version").get("TCAM", "")
                else:
                    feishu_version_tcam = domain_version_info.get("software_version")
                if feishu_version_tcam:
                    feishu_version_tcam = "V" + feishu_version_tcam.replace("6110110", "")
                    feishu_version_tcam = feishu_version_tcam[:4] + " " + feishu_version_tcam[4:]
                    feishu_version_tcam = convert_version_format(feishu_version_tcam)
            except Exception as e2:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/willow_helper.py")
                logger.warning(f"TCAM 版本获取时异常：{e2.__repr__()}")
                feishu_version_tcam = ""

            version_num = feishu_version_bgm if "BGM" in sheet_name else feishu_version_tcam
            if "SOA" in sheet_name:
                if "BGM" in job_type:
                    version_num = feishu_version_bgm
                elif "TCAM" in job_type:
                    version_num = feishu_version_tcam
                else:
                    version_num = feishu_version_bgm
            version_num = re.sub(r'\s+', ' ', version_num)  # 合并版本号中间的多个空格

            return WillowConfigForFeishu(version_num, case_type, job_type, job_owner,
                                         fail_case_sheet_name, fail_case_document_id, 
                                         feishu_rule_key)

    @staticmethod
    def write_report_summary_json(willow_task_path: str, willow_config: dict):
        with open(willow_task_path, "r") as task_json:
            report_summary = json.load(task_json)
            report_summary['upload_to_willow_config'] = willow_config
        with open(willow_task_path, "w") as task_json:
            json.dump(report_summary, task_json)

    def _run_willow_job(self, flow_id, data):
        ret = requests.post(
            url=self.slave_run_url.format(flow_id),
            headers=self.headers,
            data=data
        )
        ret_json = ret.json()
        if ret_json:
            logger.info(ret_json)
            if ret_json.get('code') == 200:
                flow_result_id = ret_json.get('data').get('flow_result_id')
                logger.info(f'获取云端任务:{flow_result_id}')
                return flow_result_id
            else:
                err_msg = f"云端任务启动失败, code: {ret_json.get('code')}"
                logger.error(err_msg)
                raise exception_error.WillowError(err_msg)
        else:
            err_msg = f"云端任务启动失败, ret_json: {ret_json}"
            logger.error(err_msg)
            raise exception_error.WillowError(err_msg)

    def _get_willow_job_detail(self, flow_id):
        url = f'https://willow.jiduprod.com/api/willow-service/flow/flow/{flow_id}/'
        ret = requests.get(url=url, headers=self.headers)
        ret_json = ret.json()
        if ret_json:
            if ret_json.get('code') == 200:
                logger.info(f'请求{url}成功')
                return ret_json
            else:
                error_msg = f"请求{url}失败，返回值{ret_json}"
                logger.error(error_msg)
                raise exception_error.WillowError(error_msg)
        else:
            error_msg = f"请求{url}失败，返回值{ret_json}"
            logger.error(error_msg)
            raise exception_error.WillowError(error_msg)

    def _update_willow_job(self, flow_id, update_data):
        url = f'https://willow.jiduprod.com/api/willow-service/flow/flow/{flow_id}/'
        ret = requests.put(url, data=update_data, headers=self.headers)
        ret_json = ret.json()
        if ret_json:
            if ret_json.get('code') == 200:
                logger.info(f'请求{url}成功')
                return ret_json
            else:
                error_msg = f"请求{url}失败，返回值{ret_json}"
                logger.error(error_msg)
                raise exception_error.WillowError(error_msg)
        else:
            error_msg = f"请求{url}失败，返回值{ret_json}"
            logger.error(error_msg)
            raise exception_error.WillowError(error_msg)

    @staticmethod
    def _sync_master_job_to_slave(master_update_data: Dict, slave_update_data: Dict):
        # 同步第一行最后一列的数据，也就是0，-1
        # 同步插件任务
        notice = master_update_data["notice"]
        # 同步超时时间
        expiry_time = master_update_data["stages"][0]["parallelTasks"][0]["serialTasks"][-1]["expiry_time"]
        # 同步代码仓库
        git = master_update_data["stages"][0]["parallelTasks"][0]["serialTasks"][-1]["input_test_script_git"]
        # 同步代码分支
        branch = master_update_data["stages"][0]["parallelTasks"][0]["serialTasks"][-1]["input_test_script_version"]

        slave_update_data["notice"] = notice
        slave_update_data["stages"][0]["parallelTasks"][0]["serialTasks"][-1]["expiry_time"] = expiry_time
        slave_update_data["stages"][0]["parallelTasks"][0]["serialTasks"][-1]["input_test_script_git"] = git
        slave_update_data["stages"][0]["parallelTasks"][0]["serialTasks"][-1]["input_test_script_version"] = branch
        return slave_update_data

    def run_and_check_willow_job(self, willow_task_path, case_mapping: Dict, master_ip, master_port):
        with open(willow_task_path, "r") as task_json:
            task = json.load(task_json)
            input_test_script_cmd: str = task.get("inputTestScriptCMD")
            executor: str = task.get("executor")
            flow_id: str = task.get("flow_id")
            job_id: str = task.get("job_id")
            input_test_script_cmd = input_test_script_cmd.replace('--distributed=true', '--distributed=false')
            input_test_script_cmd = re.sub(r'\n+', ';', input_test_script_cmd)
        remark = executor
        flow_result_id_list = []
        for job_num, case_list in case_mapping.items():
            # slave_data = self._get_willow_job_detail(flow_id)
            # master_data = self._get_willow_job_detail(job_id)
            data = {
                'remark': remark,
                'cmd': input_test_script_cmd,
                'case_list': case_list,
                'master_report_path': willow_task_path,
                'master_ip': master_ip,
                'master_port': master_port,
            }
            # slave_update_data = self._sync_master_job_to_slave(master_data, slave_data)
            # self._update_willow_job(flow_id, slave_update_data)
            flow_result_id = self._run_willow_job(flow_id, data)
            time.sleep(2)
            flow_result_id_list.append(flow_result_id)
        self._check_willow_job_status(flow_id, flow_result_id_list)

    @staticmethod
    def _check_willow_job_status(flow_id, flow_result_id_list, timeout=60 * 60 * 24):
        start_time = time.time()
        while time.time() - start_time <= timeout:
            logger.info(f"当前有{len(flow_result_id_list)}个任务在执行")
            for index in range(len(flow_result_id_list) - 1, -1, -1):
                flow_result_id = flow_result_id_list[index]
                job_history = f'https://willow.jiduprod.com/flow/flow_history?flowID={flow_id}&flowHistoryTab=SonTask&pageNum=1&id={flow_result_id}'
                url = f'https://willow.jiduprod.com/api/willow-service/flow/results/{flow_result_id}/'
                ret = requests.get(url=url)
                ret_json = ret.json()
                logger.debug(ret_json)
                if ret_json:
                    if ret_json.get('code') == 200:
                        status = ret_json.get('data').get('status')
                        if status == 'IN PROGRESS':
                            logger.info(f'slave端任务正在执行中, job链接：{job_history}')
                            time.sleep(1)
                            continue
                        elif status == 'FAIL':
                            logger.error(f'任务执行失败, job链接：{job_history}')
                            del flow_result_id_list[index]
                        elif status == 'SUCCESS':
                            logger.info(f'任务执行成功, job链接：{job_history}')
                            del flow_result_id_list[index]
                        elif status == 'ABORT':
                            logger.info(f'任务已取消, job链接：{job_history}')
                            del flow_result_id_list[index]
                        del ret_json['data']['exec_param']['case_list']
                        logger.info(ret_json)
                    else:
                        logger.info(ret_json)
            if not flow_result_id_list:
                logger.info('所有任务已执行完毕')
                break
            time.sleep(30)
        if time.time() - start_time > timeout:
            logger.error('任务超时退出')
            return False

    @staticmethod
    def get_case_list(willow_task_path):
        with open(willow_task_path, "r") as task_json:
            task = json.load(task_json)
            case_list = task.get("case_list")
        return case_list

    def async_check_master_status(self, willow_task_path):
        with open(willow_task_path, "r") as task_json:
            task = json.load(task_json)
            master_ip = task.get("master_ip")
            master_port = task.get("master_port")
            if master_ip and master_port:
                t = threading.Thread(target=self._check_master_status, args=(master_ip, master_port))
                t.setDaemon(True)
                t.start()

    @staticmethod
    def _check_master_status(master_ip, master_port):
        url = f'http://{master_ip}:{master_port}/'
        logger.info(f"开始监控master:{url}是否退出")
        while True:
            try:
                ret = requests.get(url=url)
                ret_json = ret.json()
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/willow_helper.py")
                logger.error(fr"请求出现异常，{str(e)}，master端已退出，释放slave端资源")
                os._exit(1)
            else:
                if ret_json:
                    if ret_json.get("code") == 200:
                        time.sleep(5)
                        logger.info(f"master:{url} is online")
                        continue
                logger.error(fr"master端已退出，释放slave端资源，ret_json为{ret_json}")
                os._exit(1)


class WillowConfigForFeishu:
    def __init__(self, version_num, case_type, job_type, job_owner, fail_case_sheet_name, fail_case_document_id, feishu_rule_key):
        self.version_num = version_num
        self.case_type = case_type
        self.job_type = job_type
        self.job_owner = job_owner
        self.fail_case_sheet_name = fail_case_sheet_name
        self.fail_case_document_id = fail_case_document_id
        self.feishu_rule_key = feishu_rule_key
        self.ms_path = None
        self.sat_path = None
        self.caseid = None
        self.maintainer = None
        self.caseUnique = None
        self.job_id = None
        self.wifi_localhost = None
        self.allure_report = None  # 分布式任务结束后生成的allure报告
        self.distibute_task_id = None  # 分布式任务ID

    def reset(self):
        self.ms_path = None
        self.sat_path = None
        self.caseid = None

    def to_string(self):
        logger.info("========================willow_config_for_feishu==============")
        logger.info(f"当前上传飞书的配置字段为：版本号：{self.version_num}, 执行类型：{self.case_type}, "
                    f"JOB类型：{self.job_type}, 负责人：{self.job_owner}, 飞书文档ID：{self.fail_case_document_id},"
                    f"飞书数据表名称：{self.fail_case_sheet_name},"
                    f"飞书内容规则：{self.feishu_rule_key}")
        logger.info(f"失败用例信息：MS路径{self.ms_path}, 脚本路径：{self.sat_path}，用例ID: {self.caseid}")
        logger.info("========================willow_config_for_feishu==============")
        
def get_version_from_url(img_url):
    # 匹配版本号
    sdb_match = re.search(r"/Release/(v\d+\.\d+\.\d+)/", img_url)
    if sdb_match:
        sdb = sdb_match.group(1)
    # 匹配文件名（也就是URL的最后一部分，假设不包含路径分隔符）
    ver_match = re.search(r"/([^/]+)\.bin$", img_url)
    if ver_match:
        ver = ver_match.group(1)
        if re.search(r'\d', ver):  # 确保ver包含数字
            # 找到第一个非数字字符的位置
            first_non_digit = next((i for i, char in enumerate(ver) if not char.isdigit()), None)
            if first_non_digit is not None:
                # 在第一个非数字字符前插入空格（如果它不是第一个字符）
                if first_non_digit > 0:
                    ver = ver[:first_non_digit] + ' ' + ver[first_non_digit:]
    return sdb, ver
