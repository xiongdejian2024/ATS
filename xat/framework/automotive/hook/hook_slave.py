from framework.automotive.core.resources import LOCK_SCRIPT, workspace_relative
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :hook_slave.py
@time         :4/11/24 10:23
@author       :dejian.xiong@jiduauto.com
@description  :分布式slave进程
"""
import copy
import json
import os
import threading
import time
from typing import List

import allure
from _pytest.config import ExitCode, Config
from _pytest.main import Session
from _pytest.nodes import Item
from _pytest.reports import TestReport
from _pytest.runner import CallInfo
from _pytest.terminal import TerminalReporter
from xat_ecu.legacy.common import exception_error
from xat_ecu.legacy.common.logger import logger

from framework.automotive.hook.hook_base import BaseHooks
from framework.automotive.utils.data_type import Domain, CaseStatus, SlaveTaskStatus, TaskTarget, PytestSlaveStatus
from framework.automotive.utils.case_info_helper import get_sat_path, back_up_fail_case_log
from framework.automotive.utils.conftest_helper import kill_process, timestamp_to_datetime_full_millis, parent_dir, \
    change_bgm_vehicle_model, change_veh_type, change_bl_ver
from framework.automotive.utils.data_type import BenchStatus, BenchConfig, HeartBeat
from framework.automotive.utils.thread_helper import stop_thread
from framework.automotive.utils.feishu_helper import send_error_msg


class HookSlave(BaseHooks):
    def __init__(self):
        super().__init__()
        self.collected_case_list = []
        self.collected_class_list = []

    def pytest_runtest_setup_for_slave(self, item: Item):
        self.ecuinfo.case_start = time.time()

    def pytest_runtest_teardown_for_slave(self):
        self.ecuinfo.case_end = time.time()

    def _run_class_test(self, session: Session, message):
        items = session.items
        new_items = []
        for item in items:
            for nodeid in message.get("class_case_list"):
                if item.nodeid == nodeid:
                    if nodeid not in self.collected_case_list:
                        self.collected_case_list.append(item.parent.nodeid)
                        new_items.append(item)
                    else:
                        logger.warning(f"当前测试项已存在于列表中，跳过该测试项：{item.nodeid}")
                        return
        logger.info(f"执行的用例为{new_items}")
        for index in range(len(new_items)):
            current_item = new_items[index]
            next_item = new_items[index + 1] if index < len(new_items) - 1 else None
            session.config.hook.pytest_runtest_protocol(item=current_item, nextitem=next_item)

    def pytest_runtestloop(self, session: Session):
        if not self.by_platform:
            while True:
                # 接收master的信息，如果是用例信息则执行用例，如果是结束信息则退出循环
                for key, value in self.ecuinfo.domain.items():
                    if value:
                        domain = key
                        break
                else:
                    err_msg = 'domain参数获取为None，环境识别失败停止运行'
                    logger.error(err_msg)
                    raise exception_error.ConfigError(err_msg)
                running_env = "HIL" if self.running_env.HIL else "SIL"
                self.slave_client.send_event(data={
                    "title": PytestSlaveStatus.pytest_runtestloop.value,
                    "domain": domain,
                    "running_env": running_env,
                    "data": TaskTarget.apply_case.value
                })
                try:
                    message = self.slave_queue.get(timeout=3 * 60)
                except Exception as e:
                    logger.exception(f"任务接收超时，异常原因是{e}")
                    if not self.slave_client.sio.connected:
                        logger.error(f"master断开连接")
                        return
                else:
                    if message.get("slave_task_status") == SlaveTaskStatus.finish.value:
                        logger.info(f"master端任务已经分配完成")
                        return True
                    elif message.get("slave_task_status") == SlaveTaskStatus.exit.value:
                        logger.info(f"任务被暂停结束")
                        return True
                    vehicle_model = message.get("vehicle")
                    # 更新用例状态为running
                    self.slave_client.send_event(data={
                        "title": PytestSlaveStatus.pytest_runtestloop.value,
                        "domain": domain,
                        "running_env": running_env,
                        "vehicle_model": vehicle_model,
                        "class_name": message.get("class_name"),
                        "task_status": CaseStatus.running.value,
                        "data": TaskTarget.update_case_status.value
                    })
                    # 判断车型是否匹配，如果不匹配先修改车型
                    change_bgm_vehicle_model(vehicle_model)
                    tmp_tcconfig = copy.deepcopy(self.ecuinfo.tc_config)
                    self.ecuinfo.tc_config['veh_type'] = change_veh_type(vehicle_model)  # 更新ecu变量信息
                    target_vehicle_model = change_bl_ver(vehicle_model)
                    # 如果不包含mca
                    if self.ecuinfo.tc_config['bl_ver'].count(target_vehicle_model) != 1:
                        self.ecuinfo.tc_config[
                            'bl_ver'] = f"{self.ecuinfo.tc_config['bl_ver']}{change_bl_ver(vehicle_model)}"  # 更新ecu变量信息
                    # 修改ecuinfo中的变量
                    current_time = time.time()
                    self._run_class_test(session, message)  # 执行类级别的用例
                    self.ecuinfo.tc_config = tmp_tcconfig
                    self.report.upload_report_file_by_http(current_time)
                    # 更新用例状态为finished
                    self.slave_client.send_event(data={
                        "title": PytestSlaveStatus.pytest_runtestloop.value,
                        "domain": domain,
                        "running_env": running_env,
                        "vehicle_model": vehicle_model,
                        "class_name": message.get("class_name"),
                        "task_status": CaseStatus.finished.value,
                        "data": TaskTarget.update_case_status.value
                    })

    def pytest_collection_modifyitems_for_slave(self, items: List[Item]):
        if self.testplanid:
            try:
                (self.jama_id_mapping,
                 self.ms_failedcases_idlist,
                 self.fail_case_result_description,
                 self.ms_client,
                 self.ms_casesinfo) = self.ms.get_test_plan(
                    testplanid=self.testplanid, execute_type=self.execute_type)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/hook/hook_slave.py")
                logger.warning(f"获取回填测试计划信息失败：{e.__repr__()}")
        if self.plan_id:
            self.new_ms_cases_info = self.ms.get_test_plan(testplanid=self.plan_id, execute_type=self.execute_type)[
                -1]
        logger.info('pytest_collection_modifyitems')
        try:
            self.case.write_case_priority_statistics(items, self.ms_casesinfo, self.jama_id_mapping,
                                                     self.willow_task_path)
            logger.info("当前自动化用例 在MS上的优先级分类统计成功")
        except Exception as e1:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/hook/hook_slave.py")
            logger.warning(f"自动化用例 在MS上的优先级分类统计执行异常：{e1.__repr__()}")

        # 配合 ms_failedcases_idlist 只run MS 失败的或没有测试的
        # 将用例名拿出来存入新列表
        if self.ms_failedcases_idlist:
            items[:] = self.ms.collection_failed_case_by_ms(ms_failedcases_idlist=self.ms_failedcases_idlist,
                                                            jama_id_mapping=self.jama_id_mapping, items=items)
        if self.new_ms_cases_info:
            items[:] = self.ms.collection_case_by_ms(ms_case_info=self.new_ms_cases_info, items=items)
        if self.plan_id:
            project_name = self.ms.get_project_name_by_plan_id(self.ms_client, self.plan_id)
            case_info_list = self.database.get_ms_testcase_list(projectName=project_name)
            items[:] = self.case.add_case_marker(items, case_info_list)
        if self.by_platform:
            case_list = self.bench.task_json.get('case_list')
            if case_list:
                items[:] = self.case.select_case_by_name(items, case_list)
        else:
            self.slave_client.send_event(data={
                "title": PytestSlaveStatus.pytest_collection_modifyitems.value,
                "msg": "用例修改完成"
            })

    def pytest_collection_finish_for_slave(self, session: Session):
        # 通过task path获取需要执行的case 应用场景为分布式执行
        logger.info(f"收集到的case数量{len(session.items)}")
        if not self.by_platform:
            self.slave_client.send_event(data={
                "title": PytestSlaveStatus.pytest_collection_finish.value,
                "msg": "用例收集完成"
            })
        if len(session.items) == 0:
            if self.is_willow:
                with open(self.willow_task_path, "r") as task_json:
                    task = json.load(task_json)
                    task_desc = task.get("task_desc", "")
                    willow_flow_id = task.get("willow_flow_id", "")
                if task_desc:
                    send_error_msg(
                        task_desc,
                        "Slave节点任务收集到的case数量为0",
                        slave_ip=self.wifi_localhost,
                        willow_url=f"https://willow.jiduprod.com/flow/flow_history?flowID={willow_flow_id}")

    def pytest_runtest_makereport_for_slave(self, report: TestReport, item: Item, call: CallInfo):
        """
        每个测试用例执行后，制作测试报告
        :param report:测试报告对象
        :param item:测试用例对象
        :param call:测试用例的测试步骤
                 执行完常规钩子函数返回的report报告有个属性叫report.when
                先执行when='setup' 返回setup 的执行结果
                然后执行when='call' 返回call 的执行结果
                最后执行when='teardown'返回teardown 的执行结果
        :return:
        """
        # 获取调用结果的测试报告，返回一个report对象, report对象的属性包括when（steup, call, teardown三个值）、nodeid(测试用例的名字)、
        if self.is_willow:
            self.willow_feishu_config_info.sat_path = get_sat_path(report.nodeid)
            self.willow_feishu_config_info.caseUnique = None
        if report.when == "setup":
            logger.info("before func 执行结果 {}".format(report.outcome))
            nodeid = report.nodeid
            item.session.results[item.nodeid] = report
            if report.outcome != "passed":
                self.ecuinfo.class_case_fail_flag = True
                if report.outcome == "failed":
                    self.testresult = "Failure"
                elif report.outcome == "error":
                    self.testresult = "Blocking"
                    logger.info(f"用例 {report.nodeid}  before func 执行结果为 ==== {self.testresult} ====")
                self.ecuinfo.testresult = self.testresult
                try:
                    self.feed_back.parse_node_id(nodeid, self.testresult)
                    logger.info(self.feed_back.__repr__())
                    case_id_str_list = self.feed_back.current_case_id.split("_")
                    # 回填飞书表格失败用例信息
                    for case_id_str in case_id_str_list:
                        if self.is_willow:
                            self.willow_feishu_config_info.caseid = case_id_str  # 赋初始值
                        if case_id_str.isdigit():
                            if self.jama_id_mapping is not None:
                                case_id_str = self.jama_id_mapping.get(
                                    str(case_id_str), case_id_str
                                )
                            logger.info("case_id is {}".format(case_id_str))
                            if self.is_willow:
                                self.willow_feishu_config_info.caseid = str(case_id_str)  # 再次赋值
                            if (
                                    self.testresult_dict.get(case_id_str) is None
                                    or self.testresult_dict.get(case_id_str) == "Pass"
                            ):
                                if self.ms_casesinfo:
                                    id_info = self.ms_casesinfo.get(case_id_str)
                                    if id_info:
                                        self.willow_feishu_config_info.caseUnique = id_info[3]
                                if self.is_willow:
                                    self.feishu.sync_fail_case_result_to_feishu(
                                        self.willow_task_path,
                                        self.willow_feishu_config_info,
                                        self.ecuinfo)  # 执行结果同步到飞书多维表格-setup阶段
                                if self.ms_casesinfo:
                                    id_info = self.ms_casesinfo.get(case_id_str)
                                    if id_info:
                                        MSId = id_info[0]
                                        MSnodeId = id_info[1]
                                        caseId = id_info[3]
                                        if id_info[2] != "Prepare" and self.testresult == "Pass":
                                            logger.info(
                                                f"setup阶段，用例{case_id_str} 当前的状态为{id_info[2]},不进行回填")
                                        else:
                                            if not self.is_onlypass and self.feed_back.feed_back:  # 立即回填
                                                if self.feed_back.repeat_flag:  # 当前用例repeat
                                                    self.testresult = self.feed_back.repeat_info["result"]
                                                if self.version_info and self.result_description:
                                                    self.ms_client.set_testcase_status_in_testPlan_new(
                                                        self.testplanid,
                                                        caseId,
                                                        self.testresult,
                                                        self.wifi_localhost,
                                                        self.version_info,
                                                        self.result_description)
                                                else:
                                                    self.sync_ms_result = self.ms_client.set_testcase_status_in_testPlan(
                                                        MSId, MSnodeId, self.testresult, caseId
                                                    )
                                    else:
                                        logger.warning(f"无效的case_id：{case_id_str}, MS上没有对应的测试用例")
                                        if nodeid not in self.errfarmatcase_list:
                                            self.errfarmatcase_list.append(nodeid)
                            else:
                                logger.info("MS已更新了结果(Failure/Blocking); 不需要再更新MS")
                        else:
                            logger.warning("自动化测试case name {} 不符合规范".format(nodeid))
                            if nodeid not in self.errfarmatcase_list:
                                self.errfarmatcase_list.append(nodeid)
                        if self.feed_back.feed_back:
                            if self.feed_back.repeat_flag:
                                self.feed_back.reset()
                                self.testresult_dict[case_id_str] = self.feed_back.repeat_info["result"]
                            else:
                                self.testresult_dict[case_id_str] = self.testresult
                except Exception as e:
                    logger.exception(f"setup阶段,飞书回填报错,原因:{str(e)}")
        if report.when == "call":
            logger.info("Case 执行结果 {}".format(report.outcome))

            nodeid = report.nodeid
            if report.outcome == "passed":
                self.testresult = "Pass"
            elif report.outcome == "failed":
                self.testresult = "Failure"
            elif report.outcome == "error":
                self.testresult = "Blocking"
            self.ecuinfo.testresult = self.testresult
            if self.ecuinfo.testresult != "Pass":
                self.ecuinfo.class_case_fail_flag = True
            logger.info("用例 {} 执行结果为 ==== {} ====".format(nodeid, self.testresult))
            item_result = item.session.results.get(item.nodeid)
            if item_result and item_result.outcome == 'passed':
                item.session.results[item.nodeid] = report
            try:
                self.feed_back.parse_node_id(nodeid, self.testresult)
                logger.info(self.feed_back.__repr__())

                case_id_str_list = self.feed_back.current_case_id.split("_")
                for case_id_str in case_id_str_list:
                    if self.is_willow:
                        self.willow_feishu_config_info.caseid = case_id_str  # 赋初始值
                    if case_id_str.isdigit():
                        if self.jama_id_mapping is not None:
                            case_id_str = self.jama_id_mapping.get(str(case_id_str), case_id_str)
                        if report.outcome != "passed":
                            logger.info("增加失败描述信息")
                            if self.jama_id_mapping is not None:
                                case_id_str = self.jama_id_mapping.get(
                                    str(case_id_str), case_id_str
                                )
                            if self.fail_case_result_description is not None:
                                logger.info(case_id_str)
                                logger.info(self.fail_case_result_description)
                                case_fail_info = self.fail_case_result_description.get(
                                    str(case_id_str), None
                                )
                                logger.info(case_fail_info)
                                if case_fail_info:
                                    logger.info("定制allure报告，增加上次分析结果")
                                    allure.dynamic.description(
                                        f"结果说明：{case_fail_info.get('resultDescribe', '无')}\n"
                                        f"Jira缺陷：{case_fail_info.get('jiraIssue', '无')}"
                                    )
                        if (
                                self.testresult_dict.get(case_id_str) is None
                                or self.testresult_dict.get(case_id_str) == "Pass"
                        ):
                            if self.is_willow:
                                if self.feed_back.feed_back:
                                    if self.testresult != "Pass":
                                        if self.ms_casesinfo:
                                            id_info = self.ms_casesinfo.get(case_id_str)
                                            if id_info:
                                                self.willow_feishu_config_info.caseUnique = id_info[3]
                                        self.feishu.sync_fail_case_result_to_feishu(
                                            self.willow_task_path,
                                            self.willow_feishu_config_info,
                                            self.ecuinfo)  # 执行结果同步到飞书多维表格-call阶段

                            if self.ms_casesinfo:
                                id_info = self.ms_casesinfo.get(case_id_str)
                                if id_info:
                                    MSId = id_info[0]
                                    MSnodeId = id_info[1]
                                    caseId = id_info[3]
                                    if id_info[2] != "Prepare" and self.testresult == "Pass":
                                        logger.info(f"setup阶段，用例{case_id_str} 当前的状态为{id_info[2]},不进行回填")
                                    else:
                                        if self.is_onlypass:
                                            # 只有pass才更新测试计划
                                            if self.testresult == "Pass" and self.feed_back.feed_back:
                                                if self.feed_back.repeat_flag:  # 当前用例有repeat
                                                    if self.feed_back.repeat_info["result"] is not None:
                                                        self.testresult = self.feed_back.repeat_info["result"]
                                                if self.version_info and self.result_description:
                                                    self.ms_client.set_testcase_status_in_testPlan_new(
                                                        self.testplanid,
                                                        caseId,
                                                        self.testresult,
                                                        self.wifi_localhost,
                                                        self.version_info,
                                                        self.result_description)
                                                else:
                                                    self.sync_ms_result = self.ms_client.set_testcase_status_in_testPlan(
                                                        MSId, MSnodeId, self.testresult, caseId
                                                    )
                                            if self.feed_back.feed_back:
                                                if self.feed_back.repeat_flag:
                                                    self.testresult_dict[case_id_str] = self.feed_back.repeat_info[
                                                        "result"]
                                                    self.feed_back.reset()
                                                else:
                                                    self.testresult_dict[case_id_str] = self.testresult
                                        else:
                                            if self.feed_back.feed_back:
                                                if self.feed_back.repeat_flag:
                                                    if self.feed_back.repeat_info["result"] is not None:
                                                        self.testresult = self.feed_back.repeat_info["result"]
                                                if self.version_info and self.result_description:
                                                    self.ms_client.set_testcase_status_in_testPlan_new(
                                                        self.testplanid, caseId,
                                                        self.testresult,
                                                        self.wifi_localhost,
                                                        self.version_info,
                                                        self.result_description)
                                                else:
                                                    self.sync_ms_result = self.ms_client.set_testcase_status_in_testPlan(
                                                        MSId, MSnodeId, self.testresult, caseId
                                                    )
                                else:
                                    logger.warning(f"无效的case_id：{case_id_str}，MS测试计划找不到该用例")
                                    if nodeid not in self.errfarmatcase_list:
                                        self.errfarmatcase_list.append(nodeid)
                        else:
                            logger.info("MS已更新了结果(Failure/Blocking); 不需要再更新MS")
                        if self.feed_back.feed_back:
                            if self.feed_back.repeat_flag:
                                self.testresult_dict[case_id_str] = self.feed_back.repeat_info["result"]
                                self.feed_back.reset()
                                logger.info(self.feed_back.repeat_info)
                            else:
                                self.testresult_dict[case_id_str] = self.testresult
                    else:
                        logger.warning("自动化测试case name {} 不符合规范".format(nodeid))
                        if nodeid not in self.errfarmatcase_list:
                            self.errfarmatcase_list.append(nodeid)
                item.session.results[item.nodeid] = report
            except Exception as e:
                logger.exception(f"call阶段,飞书回填报错,原因:{str(e)}")
        if report.when == "teardown":
            self.ecuinfo.testresult = self.testresult
            item_result = item.session.results.get(item.nodeid)
            if item_result and item_result.outcome == 'passed':
                item.session.results[item.nodeid] = report
            try:
                # 将用例的日志保存到对应的台架/root/fail_case_log/{bench_uuid}
                back_up_fail_case_log(self.ecuinfo)
            except Exception as e:
                logger.exception(f"{self.ecuinfo.caseid}的bench_uuid、log_path获取异常，无法存储日志, {str(e)}")
            passed_amount = sum(1 for r in item.session.results.values() if r.passed)
            failed_amount = sum(1 for r in item.session.results.values() if r.failed)
            skipped_amount = sum(1 for r in item.session.results.values() if r.skipped)
            total = item.session.testscollected
            remained_amount = total - len(item.session.results)
            if self.by_platform:
                print_info = f'\n\nUntil now, {passed_amount} cases passed, {failed_amount} cases failed, {skipped_amount} cases skipped, remain {remained_amount} cases to be run!'
                logger.info(print_info)
                self.case_progress.passed = passed_amount
                self.case_progress.failed = failed_amount
                self.case_progress.skipped = skipped_amount
                self.case_progress.total = total
                self.case_progress.remain_case = remained_amount
                self.case_progress.current_case = report.nodeid
                if not self.sync_ms_result:
                    self.sync_ms_fail_num += 1
                self.case_progress.sync_ms_fail = self.sync_ms_fail_num
                bench_config = BenchConfig(**{'host': self.env_properties_info.wifi_localhost})
                self.bench.set_status(bench_config, BenchStatus.case_running, case_progress=self.case_progress)
                if self.disable_env is False and self.is_willow:
                    case_id_list = self.case.get_case_id(self.ecuinfo.testname)
                    if case_id_list:
                        for caseId in case_id_list:
                            startTime = self.ecuinfo.case_start
                            endTime = self.ecuinfo.case_end
                            startTime = timestamp_to_datetime_full_millis(startTime)
                            endTime = timestamp_to_datetime_full_millis(endTime)
                            case_info = dict(
                                caseId=caseId,
                                endTime=endTime,
                                startTime=startTime,
                                runResult=self.testresult,
                                scriptPath=item.nodeid,
                                benchEcu=self.ecuinfo.benchEcuId,
                                benchVersion=self.ecuinfo.benchVersionId,
                                frameworkVersion=self.ecuinfo.frameworkVersionId,
                                agentIp=self.ecuinfo.tb_config.get('wifi_localhost', None),
                                runUnique=str(self.ecuinfo.bench_uuid),
                                classUnique=str(self.ecuinfo.class_uuid),
                                msTestplanId=self.testplanid
                            )
                            self.database.add_ms_case_run(**case_info)
            else:
                total = len(self.collected_case_list)
                remained_amount = total - passed_amount - failed_amount - skipped_amount
                print_info = f'Until now, {passed_amount} cases passed, {failed_amount} cases failed, {skipped_amount} cases skipped, remain {remained_amount} cases to be run!' \
                             f'用例{item.nodeid}已执行'
                logger.info(print_info)
                data = {
                    "title": PytestSlaveStatus.pytest_runtest_makereport.value,
                    "msg": f"makereport完成",
                    "data": print_info
                }
                self.slave_client.send_event(data=data)

    def pytest_terminal_summary_for_slave(self, terminalreporter: TerminalReporter, exitstatus: ExitCode,
                                          config: Config):
        '''收集测试结果'''
        passed = len(
            [i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown']
        )
        failed = len(
            [i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown']
        )
        error = len(
            [i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown']
        )
        skipped = len(
            [i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown']
        )
        total = passed + failed + error
        if total:
            success_rate = passed / total
            success_rate = "{:.2%}".format(success_rate)
            logger.info('通过率：' + success_rate)
        else:
            success_rate = "0%"

        # terminalreporter._sessionstarttime 会话开始时间
        duration = time.time() - terminalreporter._sessionstarttime
        duration = int(duration)
        miniute = duration // 60
        second = duration % 60
        duration_str = 'Cases Run Total Times:  ' + str(miniute) + '分 ' + str(second) + "秒"
        # logger.info(duration_str)

        self.report_info.total = total
        self.report_info.passed = passed
        self.report_info.failed = failed
        self.report_info.error = error
        self.report_info.skipped = skipped
        self.report_info.success_rate = success_rate
        self.report_info.duration_str = duration_str

        # 确保 report_info 已被写入
        # 末尾 pytest_terminal_summary 比 case_session 后执行
        # allure的环境属性里面增加各个版本信息
        last_check_time = time.time()
        self.bench.generate_env_properties_on_allure(self.env_properties_info)
        self.domain_version_info, link_path, self.report_info = self.report.generate_allure(
            self.env_properties_info,
            self.willow_report_path,
            self.wifi_localhost,
            self.report_info,
            self.willow_feishu_config_info)
        if self.is_willow:
            self.willow_report_summary_path = '/root/autotest/willow/distributed/report/report_summary.json'
            self.willow_task_path = '/root/autotest/willow/distributed/task.json'
        self.email.write_report_summary(
            domain_version_info=self.env_properties_info,
            link_path=link_path,
            willow_report_summary_path=self.willow_report_summary_path,
            report_info=self.report_info,
            willow_task_path=self.willow_task_path,
            feed_back=self.feed_back,
            distributed=self.pytest_process
        )
        if self.by_platform:
            try:
                self.report.upload_report_file_to_server()
            except exception_error.ClientError:
                # todo:报告上传异常
                pass
        else:
            if self.slave_client.sio.connected:
                self.report.upload_report_file_by_http(last_check_time=last_check_time)
        if self.sec_planId != "":
            try:
                self.ms.sync_current_testResult_to_testplan(self.sec_planId, self.testresult_dict, self.ms_client,
                                                            self.is_onlypass,
                                                            self.version_info,
                                                            self.result_description, self.wifi_localhost)
            except Exception as e1:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/hook/hook_slave.py")
                logger.info(f"执行结果同步测试计划{self.sec_planId}失败，异常信息：{e1.__repr__()}")
        if not self.by_platform:
            self.slave_client.send_event(data={
                "title": PytestSlaveStatus.pytest_terminal_summary.value,
                "msg": "生成并上传报告成功"
            })

    def pytest_sessionstart_for_slave(self, session: Session):
        if not self.by_platform:
            self.slave_client.send_event(data={
                "title": PytestSlaveStatus.pytest_sessionstart.value,
                "msg": "session开始执行"
            })
        logger.info("session开始执行")
        # 防止之前报告数据没有清楚的影响，开始测试前，再删一次
        del_result = os.system("find ../../../report/allure_report -mindepth 1 -delete")
        if del_result == 0:
            logger.info("测试前 Del allure raw report data OK")
        else:
            err_msg = f"测试前 Del allure raw report data res is {del_result}, ----- run failed"
            logger.error(err_msg)
            raise exception_error.AllureError(err_msg)
        session.results = dict()
        # 修改对应车型的ccp文件

        if self.disable_env is False and self.is_willow:
            env_info = dict(
                bgmBootVersion=self.env_properties_info.bgm_boot_version,
                softwareVersion=str(self.env_properties_info.software_version),
                hardwareVersion=str(self.env_properties_info.hardware_version),
                bgmMcuVersion=self.env_properties_info.bgm_mcu_version,
                bgmSwitchVersion=self.env_properties_info.bgm_switch_version,
                idlVersion=self.env_properties_info.IDL,
                jidlVersion=self.env_properties_info.JIDLCompiler,
                bootesVersion=self.env_properties_info.bootes_version,
                sdbVersion=self.env_properties_info.SDB,
                carType=self.env_properties_info.veh_type,
            )
            self.ecuinfo.benchEcuId = self.database.update_ms_bench_ecu_info(**env_info)

    def pytest_sessionfinish_for_slave(self, session: Session, exitstatus: ExitCode):
        if self.running_env.HIL and self.disable_env is False:
            try:
                logger.info("结束后再次获取版本信息")
                domain_info: Domain = self.bench.get_bench_domain_info(self.tbcfg)
                self.bench.parse_get_env_info(
                    domain_info, self.tbcfg, self.tccfg, self.env_properties_info, self.willow_task_path)
            except Exception as e:
                logger.exception(f"获取版本信息失败，错误原因：{str(e)}")
        if os.path.exists("./libTSH.so"):
            os.system("rm -rf ./libASCLog.so")
            os.system("rm -rf ./libTSCANApiOnLinux.so")
            os.system("rm -rf ./libbinlog.so")
            res = os.system("rm -rf ./libTSH.so")
            if res == 0:
                logger.info("rm libTSH.so success")
            else:
                err_msg = f"rm libTSH.so   res is {res}, ----- run failed"
                logger.error(err_msg)
                raise exception_error.CmdExecuteError(err_msg)
        if not self.by_platform:
            self.slave_client.send_event(data={
                "title": PytestSlaveStatus.pytest_sessionfinish.value,
                "msg": "session结束执行",
                "exitcode": exitstatus
            })

    def pytest_unconfigure_for_slave(self, config: Config):
        try:
            # 关闭资源
            kill_process("soa_partner")
            kill_process("IniMap")
            kill_process("ptp4l")
            kill_process("top")
            kill_process("vmstat")
            if self.is_willow and self.report_to_willow:
                test_ecu_info = []
                try:
                    for ecu, version in self.env_properties_info.software_version.items():
                        if ecu == self.report_to_willow:
                            test_ecu_info.append({"ecu": ecu, "version": version})
                except AttributeError:
                    logger.error(f'未获取到软件版本信息，upload_to_willow_config字段信息写入失败')
                else:
                    with open(self.willow_task_path, "r") as task_json:
                        task = json.load(task_json)
                        job_type = task.get('job_type')
                        case_type = task.get('case_type')
                    if job_type or case_type:
                        upload_to_willow_config = {
                            "is_uploaded_needed": True,  # 是否需要上传报告
                            "test_ecu_info": test_ecu_info,  # 被测件信息
                            "task_name": f"{job_type}_{case_type}"
                        }
                    else:
                        upload_to_willow_config = {
                            "is_uploaded_needed": True,  # 是否需要上传报告
                            "test_ecu_info": test_ecu_info
                        }
                    self.willow.write_report_summary_json(self.willow_report_summary_path, upload_to_willow_config)
                    logger.info(f"report_summary.json中写入upload_to_willow_config字段信息成功")
            if self.by_platform:
                bench_config = BenchConfig(**{'host': self.env_properties_info.wifi_localhost})
                # self.bench.set_status(bench_config, BenchStatus.idle)
                self.bench.set_heartbeat_status(HeartBeat.offline)
                if not self.tasks.all_tasks_done():
                    self.tasks.shutdown(wait=False)
                else:
                    self.tasks.shutdown(wait=True)
                self.tasks.shutdown()
                for thread_info in threading.enumerate():
                    if thread_info.name != 'MainThread':
                        logger.info(f'stop {thread_info.name}, thread id: {thread_info.native_id}')
                        stop_thread(thread_info)
        except Exception as e:
            logger.exception(f"pytest_unconfigure执行出错，错误原因:{str(e)}")
        finally:
            # 释放锁
            res = os.system(f"bash \"{LOCK_SCRIPT}\" -rt")
            if res == 0:
                logger.info("释放资源锁 success")
            else:
                err_msg = f"释放资源锁 res is {res}, ----- run failed"
                logger.error(err_msg)
                raise exception_error.CmdExecuteError(err_msg)

            logger.info("pytest执行结束")
