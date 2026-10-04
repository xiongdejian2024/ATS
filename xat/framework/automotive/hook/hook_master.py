#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :hook_master.py
@time         :4/11/24 10:23
@author       :dejian.xiong@jiduauto.com
@description  :分布式master进程
"""
import json
import os
import threading
import time
import traceback
import uuid
from typing import List

from _pytest.config import Config, ExitCode
from _pytest.main import Session
from _pytest.nodes import Item
from xat_ecu.legacy.common import exception_error
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.interface.nuc_app import exec_shell
from framework.automotive.communication.message_protocol import message_protocol_dict
from framework.automotive.communication.server import find_free_port

from framework.automotive.hook.hook_base import BaseHooks
from framework.automotive.utils.conftest_helper import kill_process
from framework.automotive.utils.data_type import ReportInfo, CaseStatus, PytestSlaveStatus
from framework.automotive.utils.tasks_helper import TaskHelper
from framework.automotive.utils.thread_helper import stop_thread
from framework.automotive.utils.feishu_helper import send_error_msg, insert_tl_test_data_to_feishu
from framework.automotive.communication.server import DistServer
from framework.automotive.utils.database_helper import get_ms_testcase_top_module


class HookMaster(BaseHooks):
    def __init__(self):
        super().__init__()
        self.exception_threads_dict = {}  # 记录异常线程
        self.task_group_list = []  # 任务组列表
        self.master_lock = threading.Lock()
        self.add_new_task = []  # 新增任务列表，可通过api或者提前按照用例分配
        self.message_protocol_dict = message_protocol_dict  # 消息协议字典
        self.pytest_slave_status_dict = {}  # 记录slave运行的状态进度

    def _handle_msgs(self, message):
        if isinstance(message, dict):
            title = message.get('title')
            if self.message_protocol_dict.get(title):
                return self.message_protocol_dict[title](self, message)

    def pytest_sessionstart_for_master(self, session):
        logger.info("session开始执行")
        # 防止之前报告数据没有清楚的影响，开始测试前，再删一次
        del_result = os.system("find ../../../report/allure_report -mindepth 1 -delete")
        if del_result == 0:
            logger.info("测试前删除allure_report数据成功")
        else:
            err_msg = f"测试前删除allure_report数据失败，命令行返回值为{del_result}"
            logger.error(err_msg)
            raise exception_error.AllureError(err_msg)

    def pytest_sessionfinish_for_master(self, session: Session, exitstatus: ExitCode):
        logger.info("session结束执行")

    def pytest_collection_modifyitems_for_master(self, items: List[Item]):
        if self.testplanid:
            try:
                (self.jama_id_mapping,
                 self.ms_failedcases_idlist,
                 self.fail_case_result_description,
                 self.ms_client,
                 self.ms_casesinfo) = self.ms.get_test_plan(
                    testplanid=self.testplanid, execute_type=self.execute_type)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/hook/hook_master.py")
                logger.warning(f"获取回填测试计划信息失败：{e.__repr__()}")
        if self.plan_id:
            self.new_ms_cases_info = self.ms.get_test_plan(testplanid=self.plan_id, execute_type=self.execute_type)[
                -1]
        try:
            self.case.write_case_priority_statistics(items, self.ms_casesinfo, self.jama_id_mapping,
                                                     self.willow_task_path)
            logger.info("当前自动化用例 在MS上的优先级分类统计成功")
        except Exception as e1:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/hook/hook_master.py")
            logger.warning(f"自动化用例 在MS上的优先级分类统计执行异常：{e1.__repr__()}")

        # 配合 ms_failedcases_idlist 只run MS 失败的或没有测试的
        # 将用例名拿出来存入新列表
        if self.ms_failedcases_idlist:
            items = self.ms.collection_failed_case_by_ms(ms_failedcases_idlist=self.ms_failedcases_idlist,
                                                         jama_id_mapping=self.jama_id_mapping, items=items)
        if self.new_ms_cases_info:
            items[:] = self.ms.collection_case_by_ms(ms_case_info=self.new_ms_cases_info, items=items)
        if self.plan_id:
            project_name = self.ms.get_project_name_by_plan_id(self.ms_client, self.plan_id)
            case_info_list = self.database.get_ms_testcase_list(projectName=project_name)
            items[:] = self.case.add_case_marker(items, case_info_list)
        return items

    def pytest_collection_finish_for_master(self, session: Session):
        # -m参数收集在pytest_collection_modifyitems之后,pytest_collection_finish之前运行
        job_count = self.bench_count if self.bench_count else 3
        self.job_info.job_id = ""
        self.job_info.testplan_id = self.testplanid  # 用例回填MS时的测试计划
        willow_flow_id = ""
        if self.is_willow:
            with open(self.willow_task_path, "r") as task_json:
                task = json.load(task_json)
                self.job_info.job_name = task.get("task_desc", "")
                self.job_info.job_id = task.get("job_id", "")
                willow_flow_id = task.get("willow_flow_id", "")
                self.willow_feishu_config_info.job_id = task.get("job_id", "")
                self.willow_feishu_config_info.fail_case_sheet_name = task.get("fail_case_sheet_name", "")
                self.willow_feishu_config_info.fail_case_document_id = task.get("fail_case_document_id", "")
        else:
            self.job_info.job_id = str(uuid.uuid4())
        if self.by_platform:
            case_count, case_list_all = self._distribute_task_run_by_platform(job_count, session, willow_flow_id)
        else:
            case_count, case_list_all = self._distribute_task_run_by_socket(job_count, session, willow_flow_id)
        session.items.clear()
        report_info: ReportInfo = self.case.parse_allure_json_get_report()
        # 检查用例数量是否与预期一致
        res, str_log = self.case.check(report_info.total, case_count)
        diff_case_list = self.case.check_case_list(report_info.case_list, case_list_all)
        report_info.num_check.append(res)
        report_info.num_check.append(str_log)
        report_info.duration_str = self.case.get_duration_time(self.start_time, time.time())
        self.report.generate_env_properties_on_master(self.env_properties_info)
        self.domain_version_info, link_path, self.report_info = self.report.generate_allure(
            None,
            self.willow_report_path,
            self.wifi_localhost,
            report_info,
            self.willow_feishu_config_info)
        self.email.write_report_summary(
            domain_version_info=self.env_properties_info,
            willow_report_summary_path=self.willow_report_summary_path,
            link_path=link_path,
            report_info=self.report_info,
            willow_task_path=self.willow_task_path,
            feed_back='',
            distributed=self.pytest_process
        )
        try:
            if self.job_info.job_name:
                if report_info.case_fail_list:
                    case_fail_top_three = get_ms_testcase_top_module(report_info.case_fail_list)
                else:
                    case_fail_top_three = []
                if diff_case_list:
                    case_prepare_top_three = get_ms_testcase_top_module(diff_case_list)
                else:
                    case_prepare_top_three = []
                insert_tl_test_data_to_feishu(
                   test_task_name=self.job_info.job_name,
                   test_software_version=[self.env_properties_info.software_version.get('BGM'), 
                                          self.env_properties_info.software_version.get('TCAM')],
                   start_time=self.start_time,
                   end_time=time.time(),
                   total_case_num=int(case_count),
                   current_case_num=int(report_info.total),
                   case_fail_top_three=case_fail_top_three,
                   case_prepare_top_three=case_prepare_top_three,
                   max_hour=round((time.time() - self.start_time) / 3600, 2),
                   allure_report=link_path,   
                )
            else:
                logger.info("没有获取到任务名称，不进行插入飞书")
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/hook/hook_master.py")
            logger.warning(f"脚本稳定性数据插入飞书失败，错误信息：{e}")
            

    def _distribute_task_run_by_platform(self, job_count, session, willow_flow_id):
        tasks, case_count = self.case.case_grouping(session.items, job_count=job_count, veh_type=self.raw_veh_type)
        case_list_all = []
        if case_count:
            self.job_info.plan_total_case_num = case_count
            bench_config_list = []  # 记录
            for index, task in enumerate(tasks):
                vehicle = task.get('vehicle')
                domain = task.get('domain')
                running_env = task.get('running_env')
                case_list = task.get('case_list')
                case_list_all.extend(case_list)
                if len(case_list) == 0:
                    logger.warning(f'第{index}个任务：{task} 用例为空，跳过执行')
                    continue
                self.tasks.add_task(f'pytest_distribute_execute_{index}', TaskHelper.pytest_distribute_execute,
                                    self.wifi_localhost, vehicle, domain, case_list,
                                    self.ecuinfo, self.tasks, self.is_willow, self.is_flash,
                                    self.job_info, self.willow_feishu_config_info, running_env)
                bench_config_list.append(f'pytest_distribute_execute_{index}')
            while True:
                for index in range(len(bench_config_list) - 1, -1, -1):
                    task_result = self.tasks.get_task(f'{bench_config_list[index]}')
                    if task_result.done():
                        try:
                            task_result.result()
                        except Exception as e:
                            logger.exception(f'{bench_config_list[index]}执行任务出错, 原因是:{str(e)}')
                            self.exception_threads_dict[bench_config_list[index]] = traceback.format_exc()
                        del bench_config_list[index]
                if not bench_config_list:
                    break
                time.sleep(5)
                logger.debug(bench_config_list)
        else:
            if self.job_info.job_name:
                send_error_msg(
                    self.job_info.job_name,
                    f'测试计划:{self.plan_id},收集到的用例数量为{case_count}',
                    master_ip=self.wifi_localhost,
                    willow_url=f"https://willow.jiduprod.com/flow/flow_history?flowID={willow_flow_id}")
            logger.info(f'收集到的用例数量为{case_count}')
        return case_count, case_list_all

    def _distribute_task_run_by_socket(self, job_count, session: Session, willow_flow_id):
        case_list_all = []
        service_port = find_free_port()
        cmd = "curl https://ip.jiduauto.com | awk '{print $NF}'"
        bench_ip = exec_shell(cmd).get('output')
        service_ip = bench_ip.replace('\n', '') if bench_ip else self.wifi_localhost
        self.server = DistServer(service_ip=service_ip, service_port=service_port)
        self.server.setDaemon(True)
        self.server.start()
        if self.server.is_alive():
            logger.info(f'服务器启动成功, ip为{service_ip}端口号为:{service_port}')
        else:
            logger.error(f'服务器启动失败, ip为{service_ip}端口号为:{service_port}')
            return
        self.server.set_callback(self._handle_msgs)
        tasks, benches, case_count = self.case.case_grouping_by_time(job_count, session.items,
                                                                     veh_type=self.raw_veh_type)
        self.task_group_list = tasks
        for item in tasks:
            case_dict = item.get('case_dict')
            for key, value in case_dict.items():
                class_case_list = value['class_case_list']
                case_list_all.extend(class_case_list)
        if case_count:
            self.job_info.plan_total_case_num = case_count
            bench_config_list = []  # 记录
            self.add_new_task.extend(benches)
            while True:
                if self.add_new_task:
                    for index, bench in enumerate(benches):
                        domain = bench.get('domain')
                        running_env = bench.get('running_env')
                        task_name = f'pytest_task_{uuid.uuid4()}_{domain}_{running_env}'
                        self.tasks.add_task(
                            task_name,
                            TaskHelper.pytest_distribute_execute_by_socket,
                            self.wifi_localhost,
                            self.is_willow,
                            running_env,
                            self.ecuinfo,
                            self.job_info,
                            self.raw_veh_type,
                            self.is_flash,
                            domain,
                            service_ip,
                            service_port,
                            self.tasks
                        )
                        bench_config_list.append(task_name)
                    self.add_new_task.clear()
                for index in range(len(bench_config_list) - 1, -1, -1):
                    task_result = self.tasks.get_task(f'{bench_config_list[index]}')
                    if task_result.done():
                        logger.info(f'{bench_config_list[index]}执行任务完成')
                        try:
                            task_result.result()
                        except Exception as e:
                            logger.exception(f'{bench_config_list[index]}执行任务出错, 原因是:{str(e)}')
                            self.exception_threads_dict[bench_config_list[index]] = traceback.format_exc()
                        del bench_config_list[index]
                # 台架任务结束，并且task_group_list中的任务状态都置位时
                if not bench_config_list:
                    logger.info(f"台架上所有的任务分配已经结束")
                    break
                if self._check_task_group_status(task_group_list=self.task_group_list):
                    logger.info('所有任务执行完成，检查pytest的运行状态')
                    if self.pytest_slave_status_dict:
                        if self._check_pytest_slave_status(self.pytest_slave_status_dict):
                            logger.info('所有任务执行完成，pytest进程也结束')
                            break
                time.sleep(5)
        else:
            if self.job_info.job_name:
                send_error_msg(
                    self.job_info.job_name,
                    f'测试计划:{self.plan_id},收集到的用例数量为{case_count}',
                    master_ip=self.wifi_localhost,
                    willow_url=f"https://willow.jiduprod.com/flow/flow_history?flowID={willow_flow_id}")
            logger.info(f'收集到的用例数量为{case_count}')
        return case_count, case_list_all

    def pytest_unconfigure_for_master(self, config: Config):
        logger.info(self.tasks.tasks)
        if self.exception_threads_dict:
            for task, exception_info in self.exception_threads_dict.items():
                logger.error(f'线程任务{task}出现异常:{exception_info}')
        if not self.tasks.all_tasks_done():
            self.tasks.shutdown(wait=False)
        else:
            self.tasks.shutdown(wait=True)
        for thread_info in threading.enumerate():
            if thread_info.name != 'MainThread' or 'ThreadPoolExecutor' in thread_info.name:
                logger.info(f'stop {thread_info.name}, thread id: {thread_info.native_id}')
                stop_thread(thread_info)
        kill_process("top")
        kill_process("vmstat")

    @staticmethod
    def _check_task_group_status(task_group_list):
        for task in task_group_list:
            for node_id, node_info in task.get('case_dict').items():
                if node_info.get('case_status') != CaseStatus.finished.value:
                    return False
        return True

    @staticmethod
    def _check_pytest_slave_status(pytest_slave_status_dict):
        for client_ip, status in pytest_slave_status_dict.items():
            if status != PytestSlaveStatus.pytest_terminal_summary.value:
                logger.debug(f"{client_ip}当前为{status}")
                return False
        return True
