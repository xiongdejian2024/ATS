from framework.automotive.core.resources import LOCK_SCRIPT, workspace_relative
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :hook_slave.py
@time         :4/11/24 10:23
@author       :dejian.xiong@jiduauto.com
@description  :非分布式进程
"""
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
from framework.automotive.utils.data_type import Domain
from framework.automotive.hook.hook_base import BaseHooks
from framework.automotive.utils.case_info_helper import get_sat_path, back_up_fail_case_log
from framework.automotive.utils.conftest_helper import kill_process, timestamp_to_datetime_full_millis, parent_dir
from framework.automotive.utils.thread_helper import stop_thread


class HookNonDist(BaseHooks):
    def __init__(self):
        super().__init__()

    def pytest_runtest_setup_for_non_dist(self, item: Item):
        self.ecuinfo.case_start = time.time()

    def pytest_runtest_teardown_for_non_dist(self):
        self.ecuinfo.case_end = time.time()

    def pytest_collection_modifyitems_for_non_dist(self, items: List[Item]):
        if self.testplanid:
            try:
                (self.jama_id_mapping,
                 self.ms_failedcases_idlist,
                 self.fail_case_result_description,
                 self.ms_client,
                 self.ms_casesinfo) = self.ms.get_test_plan(
                    testplanid=self.testplanid, execute_type=self.execute_type)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/hook/hook_non_dist.py")
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
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/hook/hook_non_dist.py")
            logger.warning(f"自动化用例 在MS上的优先级分类统计执行异常：{e1.__repr__()}")

        # 配合 ms_failedcases_idlist 只run MS 失败的或没有测试的
        # 将用例名拿出来存入新列表
        if self.ms_failedcases_idlist:
            items = self.ms.collection_failed_case_by_ms(ms_failedcases_idlist=self.ms_failedcases_idlist,
                                                         jama_id_mapping=self.jama_id_mapping, items=items)
        if self.new_ms_cases_info:
            items = self.ms.collection_case_by_ms(ms_case_info=self.new_ms_cases_info, items=items)
        if self.plan_id:
            project_name = self.ms.get_project_name_by_plan_id(self.ms_client, self.plan_id)
            case_info_list = self.database.get_ms_testcase_list(projectName=project_name)
            self.case.add_case_marker(items, case_info_list)

    def pytest_collection_finish_for_non_dist(self, session: Session):
        logger.info(f"收集到的case数量{len(session.items)}")

    def pytest_runtest_makereport_for_non_dist(self, report: TestReport, item: Item, call: CallInfo):
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
                                        # if id_info[2] != "Prepare":
                                        #     logger.info(f"setup阶段，用例{case_id_str} 当前的状态为{id_info[2]}")
                                        if id_info[2] != "Prepare" and self.testresult == "Pass":
                                            logger.info(f"setup阶段，用例{case_id_str} 当前的状态为{id_info[2]},不进行回填")
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
                                                    self.ms_client.set_testcase_status_in_testPlan(
                                                        MSId, MSnodeId, self.testresult, caseId
                                                    )
                                    else:
                                        logger.warning(f"无效的case_id：{case_id_str}, MS测试计划中没有该用例")
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
            logger.info(f"Case 执行结果 {report.outcome}")

            nodeid = report.nodeid
            if report.outcome == "passed":
                self.testresult = "Pass"
            elif report.outcome == "failed":
                self.testresult = "Failure"
            elif report.outcome == "error":
                self.testresult = "Blocking"
            logger.info("用例 {} 执行结果为 ==== {} ====".format(nodeid, self.testresult))
            self.ecuinfo.testresult = self.testresult
            if self.ecuinfo.testresult != "Pass":
                self.ecuinfo.class_case_fail_flag = True
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
                                    # if id_info[2] != "Prepare":
                                    #     logger.info(f"call阶段，用例{case_id_str} 当前的状态为{id_info[2]}")
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
                                                    self.ms_client.set_testcase_status_in_testPlan(
                                                        MSId, MSnodeId, self.testresult, caseId
                                                    )
                                            if self.feed_back.feed_back:
                                                if self.feed_back.repeat_flag:
                                                    self.testresult_dict[case_id_str] = self.feed_back.repeat_info["result"]
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
                                                    self.ms_client.set_testcase_status_in_testPlan(
                                                    MSId, MSnodeId, self.testresult, caseId
                                                )
                                else:
                                    logger.warning(f"无效的case_id：{case_id_str}, MS测试计划中没有该用例")
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
            logger.info(
                f'\n\nUntil now, {passed_amount} cases passed, {failed_amount} cases failed, {skipped_amount} cases skipped, remain {remained_amount} cases to be run!'
            )
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
                        self.database.add_ms_case_run(**case_info)  # 根据添加的用例ID，更新其agent_ip，run_uniq

    def pytest_terminal_summary_for_non_dist(self, terminalreporter: TerminalReporter, exitstatus: ExitCode,
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
        self.bench.generate_env_properties_on_allure(self.env_properties_info)
        self.domain_version_info, link_path, self.report_info = self.report.generate_allure(
            self.env_properties_info,
            self.willow_report_path,
            self.wifi_localhost,
            self.report_info,
            None)

        self.feishu.sync_bench_check_result_to_feishu(
            self.report_info,
            self.is_bench_check,
            self.wifi_localhost,
            link_path)  # 台架环境检查脚本回填飞书多维表格

        self.email.write_report_summary(
            domain_version_info=self.env_properties_info,
            link_path=link_path,
            willow_report_summary_path=self.willow_report_summary_path,
            report_info=self.report_info,
            willow_task_path=self.willow_task_path,
            feed_back=self.feed_back,
            distributed=self.pytest_process
        )
        if self.sec_planId != "":
            try:
                self.ms.sync_current_testResult_to_testplan(self.sec_planId, self.testresult_dict, self.ms_client,
                                                            self.is_onlypass,
                                                            self.version_info,
                                                            self.result_description, self.wifi_localhost)
            except Exception as e1:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/hook/hook_non_dist.py")
                logger.info(f"执行结果同步测试计划{self.sec_planId}失败，异常信息：{e1.__repr__()}")

    def pytest_sessionstart_for_non_dist(self, session: Session):
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

    def pytest_sessionfinish_for_non_dist(self, session: Session, exitstatus: ExitCode):
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

    def pytest_unconfigure_for_non_dist(self, config: Config):
        try:
            # 关闭资源
            kill_process("soa_partner")
            kill_process("IniMap")
            for thread_info in threading.enumerate():
                if thread_info.name != 'MainThread':
                    logger.info(f'stop {thread_info.name}, thread id: {thread_info.native_id}')
                    stop_thread(thread_info)
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
        except Exception as e:
            logger.exception(f'pytest_unconfigure执行出错，错误原因:{str(e)}')
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
