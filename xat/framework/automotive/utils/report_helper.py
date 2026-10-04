#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :report_helper.py
@time         :2/18/24 17:25
@author       :dejian.xiong@jiduauto.com
@description  :
"""
import json
import os
import time
from pathlib import Path
from threading import Thread
import traceback

import requests

from xat_ecu.legacy.common import exception_error
from xat_ecu.legacy.common.file_handle import FileHandle
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.time_handle import get_time_str_now

from framework.automotive.utils.bench_helper import BenchHelper
from framework.automotive.utils.data_type import EnvPropertiesInfo
from framework.automotive.utils.conftest_helper import current_path, parent_dir
from framework.automotive.utils.feishu_helper import FeishuHelper


class ReportHelper:
    def generate_allure(
            self,
            domain_version_info,
            willow_report_path,
            wifi_localhost="localhost",
            report_info={},
            willow_feishu_config_info=None
    ):
        if os.path.exists("../../../report/allure_report"):
            try:
                time.sleep(2)  # wait raw allure report ok   用线程运行时可能需要
                link_path = None

                nowtime = get_time_str_now()
                allure_report_generate_path = "/root/allure_report/" + nowtime
                FileHandle.makedirs(allure_report_generate_path)

                # generate allure report html
                exe_result = os.system(
                    "/opt/allure-2.19.0/bin/allure generate --clean ../../../report/allure_report -o "
                    + allure_report_generate_path
                )

                if exe_result == 0:
                    logger.info("allure generate report OK")
                    link_path = "http://" + wifi_localhost + ":8080/" + nowtime
                    logger.info("Allure Report Local Link: {}".format(link_path))
                    if willow_feishu_config_info:
                        try:
                            # 根据distibute_task_id、wifi_localhost更新allure_report
                            willow_feishu_config_info.allure_report = link_path
                            bench = BenchHelper()
                            bench.update_running_pytest_task(willow_feishu_config_info=willow_feishu_config_info)

                            if willow_feishu_config_info:
                                # 将最终的报告链接更新到失败用例回填表的每一条记录
                                FeishuHelper.update_fail_case_table_allure_report(willow_feishu_config_info, link_path)
                        except Exception as e:
                            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/report_helper.py")
                            logger.info(f"失败用例信息，更新 allure报告 字段的值时出现异常")
                            logger.info(traceback.format_exc())

                    # 新 ---- 在固定本地仓库运行，原始数据都得删除
                    # if is_willow:
                    if "testdev" in current_path.lower():
                        res = os.system(
                            "cp -rf ../../../report/allure_report {}".format(
                                willow_report_path
                            )
                        )
                        if res == 0:
                            logger.info("cp report/allure_report success")
                        else:
                            err_msg = f"cp report/allure_report res is {res}, ----- run failed"
                            logger.error(err_msg)
                            raise exception_error.AllureError(err_msg)
                else:
                    err_msg = f"allure generate report Failed, res: {exe_result}"
                    logger.error(err_msg)
                    raise exception_error.AllureError(err_msg)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/report_helper.py")
                err_msg = f"generate_allure error: {str(e)}"
                logger.error(err_msg)
                raise exception_error.AllureError(err_msg)
            else:
                return domain_version_info, link_path, report_info
        else:
            logger.error(f"不存在../../../report/allure_report该路径")

    def generate_allure_thread_start(
            self,
            is_willow=False,
            wifi_localhost="localhost",
            report_info={},
            willow_report_summary_path=None,
    ):
        allure_thread = Thread(
            target=self.generate_allure,
            name="generate_allure_thread",
            args=(
                is_willow,
                wifi_localhost,
                report_info,
                willow_report_summary_path,
                None
            ),
        )
        allure_thread.start()

    @staticmethod
    def upload_report_file_to_server():
        if os.path.exists(Path(parent_dir) / 'task.json'):
            with open(Path(parent_dir) / 'task.json') as task_obj:
                task_json: dict = json.load(task_obj)
                hostname = task_json.get('master_config').get('hostname')
                limited_ip = task_json.get('master_config').get('limited_ip')
                port = task_json.get('master_config').get('port')
                username = task_json.get('master_config').get('username')
                password = task_json.get('master_config').get('password')
                master_report_dir = task_json.get('master_config').get('report_dir')
                # client = BenchHelper.retry_scp(hostname=hostname, port=port, username=username, password=password)
                ip_list = [hostname]
                if limited_ip:
                    ip_list.append(limited_ip)
                for hostname in reversed(ip_list):
                    try:
                        client = BenchHelper.retry_scp(hostname=hostname, port=port, username=username,
                                                       password=password)
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/report_helper.py")
                        logger.warning(f"连接{hostname}:{port} 10次后仍然失败，继续尝试下一个IP")
                        continue
                    else:
                        logger.info(f"上传报告成功连接master {hostname}:{port}")
                        break
                else:
                    raise exception_error.CmdExecuteError(f"连接{ip_list}:{port} 10次后仍然失败，直接退出")
                report_path = Path(parent_dir) / '../report/allure_report'
                report_files = os.listdir(report_path)
                logger.info(f'{report_path}路径下文件个数为{len(report_files)}')
                client.put([os.path.join(report_path, file) for file in report_files], master_report_dir)

    def generate_env_properties_on_master(self, env_properties: EnvPropertiesInfo):
        # environment_path = '../../../report/allure_report/environment.properties'
        # environment_path_copy = f'../../../report/allure_report/{env_properties.wifi_localhost}_env.properties'
        merge_json_data = {
            "distribute": 'True'
        }
        report_path = Path(parent_dir) / '../report/allure_report'
        report_files = os.listdir(report_path)
        try:
            merged_content = merge_properties_files(report_files, report_path)
            env_properties.software_version = dict(
                BGM=merged_content.get('software_version_bgm', None),
                TCAM=merged_content.get('software_version_tcam', None),
            )
            env_properties.hardware_version = dict(
                BGM=merged_content.get('hardware_version_bgm', None),
                TCAM=merged_content.get('hardware_version_tcam', None),
            )
            env_properties.bgm_boot_version = merged_content.get('bgm_boot_version', None)
            env_properties.bgm_mcu_version = merged_content.get('bgm_mcu_version', None)
            env_properties.bgm_switch_version = merged_content.get('bgm_switch_version', None)
            env_properties.IDL = merged_content.get('IDL', None)
            env_properties.bootes_version = merged_content.get('bootes_version', None)
            env_properties.JIDLCompiler = merged_content.get('JIDLCompiler', None)
            env_properties.veh_type = merged_content.get('veh_type', None)
            env_properties.SDB = merged_content.get('SDB', None)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/report_helper.py")
            logger.error(f"分布式合并slave端properties_files错误，错误原因: {str(e)}")
        for file in report_files:
            # 解析link_report_json中的数据
            if file.endswith('_link_report.json'):
                with open(Path(report_path) / file) as f:
                    link_report_json = json.load(f)
                    logger.debug(link_report_json)
                    name = file.split('_link_report')[0]
                    merge_json_data[f"{name}"] = f'{link_report_json["link"]}'
        if report_path.exists():
            with open(report_path / 'environment.properties', 'w', encoding='utf-8') as f:
                for key, value in env_properties.__dict__.items():
                    if value:
                        f.write(f'{key}={value}\n')
                for key, value in merge_json_data.items():
                    if value:
                        f.write(f'{key}={value}\n')
            # with open(environment_path_copy, 'w') as f:
            #     for key, value in env_properties.__dict__.items():
            #         if value:
            #             f.write(f'{key}={value}\n')
            #     for key, value in merge_json_data.items():
            #         if value:
            #             f.write(f'{key}={value}\n')

    @staticmethod
    def upload_report_file_by_http(last_check_time, retry_times=3):
        if os.path.exists(Path(parent_dir) / 'task.json'):
            with open(Path(parent_dir) / 'task.json') as task_obj:
                task_json: dict = json.load(task_obj)
                service_ip = task_json.get('master_config').get('service_ip')
                service_port = task_json.get('master_config').get('service_port')
                server_url = f"http://{service_ip}:{service_port}/upload"
                report_path = Path(parent_dir) / '../report/allure_report'
                report_files = os.listdir(report_path)
                for file in report_files:
                    report_file_path = os.path.join(report_path, file)
                    file_mtime = os.path.getmtime(report_file_path)
                    if file_mtime > last_check_time or file.endswith('_env.properties'):
                        logger.debug(f'上传{file}到/root/willow/distributed/report/allure_report上')
                        for _ in range(retry_times):
                            with open(report_file_path, 'rb') as f:
                                files = {'file': f}
                                try:
                                    requests.post(url=server_url, files=files, timeout=30)
                                except requests.exceptions.ConnectionError as e:
                                    logger.error(f"{report_file_path}文件上传失败， 失败原因: {str(e)}")
                                    continue
                                else:
                                    logger.debug(f'{report_file_path}文件上传成功')
                                    break


def merge_properties_files(file_list, report_path):
    merged_data = {
        'software_version_bgm': [],
        'software_version_tcam': [],
        'hardware_version_bgm': [],
        'hardware_version_tcam': [],
        'bgm_boot_version': [],
        'bgm_mcu_version': [],
        'bgm_switch_version': [],
        'IDL': [],
        'bootes_version': [],
        'JIDLCompiler': [],
        'veh_type': [],
        'SDB': []
    }
    for file_path in file_list:
        if file_path.endswith('_env.properties'):
            data = parse_properties_file(Path(report_path) / file_path)
            for key, value in data.items():
                if key == 'software_version':
                    merged_data['software_version_bgm'].append(value.get('BGM', ''))
                    merged_data['software_version_tcam'].append(value.get('TCAM', ''))
                elif key == 'hardware_version':
                    merged_data['hardware_version_bgm'].append(value.get('BGM', ''))
                    merged_data['hardware_version_tcam'].append(value.get('TCAM', ''))
                elif key in ['sdk_version', 'wifi_localhost']:
                    continue
                else:
                    merged_data[key].append(value)
    for key, value in merged_data.items():
        # print(len(set(value)))
        if len(set(value)) == 1:
            merged_data[key] = value[0]
        else:
            merged_data[key] = None
    return merged_data


def parse_properties_file(filename):
    system_info = {}
    with open(filename) as file:
        for line in file:
            line = line.strip()
            line = line.replace("'", '"')
            line = line.replace('None', '"None"')
            if '=' in line:
                key, value_str = line.split('=', 1)
                if value_str.startswith('{') and value_str.endswith('}'):
                    start_index = value_str.find('{')
                    end_index = value_str.find('}')
                    if start_index != -1 and end_index != -1 and start_index < end_index:
                        try:
                            json_content = value_str[start_index:end_index + 1]
                            value = json.loads(json_content)
                        except json.JSONDecodeError:
                            value = value_str
                else:
                    value = value_str
                system_info[key] = value
            else:
                logger.warning(f"Ignoring line without '=': {line}")
    return system_info


if __name__ == '__main__':
    ReportHelper.upload_report_file_to_server()
