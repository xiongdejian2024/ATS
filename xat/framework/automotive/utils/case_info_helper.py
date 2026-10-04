#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :case_info_helper.py
@time         :2/18/24 17:19
@author       :dejian.xiong@jiduauto.com
@description  :
"""
import json
import os
import re
from pathlib import Path
from typing import List, Dict, Union

from _pytest.nodes import Item
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.interface.feishu import feishu_api

from framework.automotive.utils.conftest_helper import parent_dir
from framework.automotive.utils.data_type import ReportInfo, VehicleModel, Domain, RunningEnv, CaseStatus

from framework.automotive.utils.data_type import EcuInfo


class CasePriorityStatistics:
    def __init__(self, target, category, total_count, job_owner):
        self.target = target
        self.category = category
        self.job_owner = job_owner
        self.total_count = total_count
        self.P0_count = 0
        self.P1_count = 0
        self.P2_count = 0
        self.P3_count = 0
        self.invalid_count = 0

    def add(self, case_priority):
        if case_priority == "P0":
            self.P0_count = self.P0_count + 1
        elif case_priority == "P1":
            self.P1_count = self.P1_count + 1
        elif case_priority == "P2":
            self.P2_count = self.P2_count + 1
        elif case_priority == "P3":
            self.P3_count = self.P3_count + 1
        else:
            self.invalid_count = self.invalid_count + 1

    def print_statistics_result(self):
        logger.info(
            f"总用例数：{self.total_count}, 等级P0用例：{self.P0_count}条, 等级P1用例：{self.P1_count}条, 等级P2用例："
            f"{self.P2_count}条, 等级P3用例：{self.P3_count}条, 无法匹配用例：{self.invalid_count}条")


class CaseInfoHelper:

    def write_case_priority_statistics(self, items, ms_casesinfo, jama_id_mapping, willow_task_path):
        logger.info("pytest_collection_modifyitems")
        logger.info(willow_task_path)
        if os.path.exists(willow_task_path):
            with open(willow_task_path, "r") as task_json:
                task = json.load(task_json)
                case_type = task.get("case_type", "")
                sheet_name = task.get("sheet_name", "")
                job_owner = task.get("job_owner", "")
                case_statistics = CasePriorityStatistics(sheet_name, case_type, len(items), job_owner)
                for item in items:  # 遍历脚本中获取到的所有的测试用例
                    if "[" in item.name:
                        caseid = item.name.split("[")[1]
                        ids_list = [caseid.split("]")[0]]
                    else:
                        if "_caseid_" in item.name:
                            ids_list = item.name.split("_caseid_")[-1].split('_')
                        else:
                            logger.info(f"没有包含_caseid_：{item.name}")
                            case_statistics.add("invalid")  # 测试用例函数命名没有“_caseid_”
                            ids_list = []
                    for case_id_str in ids_list:
                        if case_id_str.isdigit():
                            if jama_id_mapping is not None:
                                case_id_str = jama_id_mapping.get(str(case_id_str), case_id_str)
                            if ms_casesinfo:
                                id_info = ms_casesinfo.get(case_id_str)
                                if id_info:
                                    priority = id_info[4]
                                    case_statistics.add(priority)  # 对应等级的用例数+1
                                else:
                                    logger.info(f"匹配失败：{item.name}")
                                    case_statistics.add("invalid")  # 映射失败的用例
                        else:
                            logger.info(f"不全是数字：{item.name}")
                            case_statistics.add("invalid")  # 测试用例名称中有非数字
                else:
                    case_statistics.print_statistics_result()
                    self.update_case_priority_statistics(case_statistics)

    @staticmethod
    def update_case_priority_statistics(case_priority: CasePriorityStatistics):
        if "BGM" in case_priority.target:
            group = "BGM"
        elif "TCAM" in case_priority.target:
            group = "TCAM"
        elif "SOA" in case_priority.target:
            group = "SOA"
        elif "VO" in case_priority.target:
            group = "VO"
        else:
            group = "unknown"
        willow_run_result = {"执行类型": case_priority.category, "分组": group,
                             "负责人": case_priority.job_owner.strip(),
                             "总用例数": case_priority.total_count,
                             "对应MS上P0用例": case_priority.P0_count,
                             "对应MS上P1用例": case_priority.P1_count,
                             "对应MS上P2用例": case_priority.P2_count,
                             "对应MS上P3用例": case_priority.P3_count,
                             "不匹配用例": case_priority.invalid_count}
        logger.info("=========================")
        logger.info(f"负责人：{case_priority.job_owner}")
        logger.info(f"执行类型：{case_priority.category}")
        logger.info(f"分组：{group}")
        logger.info("=========================")
        if case_priority.job_owner.strip() != "" and case_priority.category != "" and group != "":
            result, detail = feishu_api.add_priority_feishu_table("用例等级统计", willow_run_result)
            logger.info(f"执行结果{result}，结果说明：{detail}")
        else:
            logger.info("必填字典为空，无法同步用例执行等级统计数据！")

    def case_grouping(self, items: List[Item], job_count: int, veh_type: Union[str, None] = None):
        # case_task = {
        #     'two_domain': {"Venus": [], "Mars_One": []},
        #     'single_tcam': {"Venus": [], "Mars_One": []}
        # }
        case_task: Dict[str, Dict[str, List]] = {key: {} for key in Domain().keys()}
        domain_set = set(case_task.keys())
        case_count = 0
        sil_bgm_case = []
        if veh_type:
            veh_type_set = {veh_type}
        else:
            veh_type_set = set(list(map(lambda v: v.value, VehicleModel)))
        for item in items:
            # node_id = item.nodeid
            marks = {mark.name for mark in item.own_markers}
            # SIL用例单独拿出来分组
            if "sil_bgm" in marks:
                sil_bgm_case.append(item)
                case_count += 1
            else:
                # 取出标签中与定义的域控相同的部分，同时满足说明用例筛选成功
                equal_domains = sorted(domain_set & marks)
                equal_veh_types = sorted(veh_type_set & marks)
                if equal_domains and equal_veh_types:
                    # 取第一个域和第一个车型作为用例添加
                    if not veh_type:
                        veh_type = equal_veh_types[0]
                    if veh_type not in case_task[equal_domains[0]].keys():
                        case_task[equal_domains[0]][veh_type] = [item]
                    else:
                        case_task[equal_domains[0]][veh_type].append(item)
                    veh_type = None
                    case_count += 1
                else:
                    logger.warning(f"{item.nodeid}中不包含{equal_domains}或者{equal_veh_types}, 包含的标签{marks}")
        logger.info(f"总共收集到的case数量为{case_count}")
        # tasks = [
        #     {
        #         'domain': 'two_domain',
        #         'vehicle': 'Venus',
        #         'case_list': [item],
        #     }
        # ]
        tasks = []
        for domain, vehicle_info in case_task.items():
            for vehicle, case_list in vehicle_info.items():
                tasks.append(dict(domain=domain, vehicle=vehicle, case_list=case_list, running_env="HIL"))
        tasks = sorted(tasks, key=lambda d: len(d['case_list']), reverse=True)
        if tasks:
            if len(tasks) < job_count:
                for index, task in enumerate(tasks):
                    if index == 0:
                        continue
                    case_list = self.case_grouping_by_module(task.get('case_list'), 1)[0]
                    tasks[index]['case_list'] = case_list
                remain_job_count = job_count - len(tasks) + 1
                # 数量最多的模块用例按照剩余的job数平均分
                case_list = tasks[0].get('case_list')
                job_num_mapping = self.case_grouping_by_module(case_list, remain_job_count)
                for job_num, case_num in job_num_mapping.items():
                    if job_num == 0:
                        tasks[job_num]['case_list'] = job_num_mapping[job_num]
                    else:
                        tasks.append(dict(
                            domain=tasks[0]["domain"],
                            vehicle=tasks[0]["vehicle"],
                            case_list=job_num_mapping[job_num]
                        ))
            else:
                for index, task in enumerate(tasks):
                    case_list = self.case_grouping_by_module(task.get('case_list'), 1)[0]
                    tasks[index]['case_list'] = case_list
        if sil_bgm_case:
            case_list = self.case_grouping_by_module(sil_bgm_case, 1)[0]
            tasks.append({'domain': 'single_bgm', 'vehicle': '', 'case_list': case_list, 'running_env': "SIL"})
        # 当前只支持SOA单域BGM的用例
        logger.debug(tasks)
        return tasks, case_count

    @staticmethod
    def _case_equal_allocate(modules, task_num):
        sorted_modules = sorted(modules.items(), key=lambda x: x[1], reverse=True)
        tasks = {i: [] for i in range(task_num)}  # 初始化任务列表

        task_cases = {i: 0 for i in range(task_num)}  # 初始化累计case数量

        for module, cases in sorted_modules:
            min_task = min(task_cases, key=task_cases.get)  # 找到累计case数量最少的任务
            tasks[min_task].append((module, cases))  # 将模块分配给累计case数量最少的任务
            task_cases[min_task] += cases  # 更新累计case数量
        logger.info(task_cases)
        return task_cases.values()

    def case_grouping_by_module(self, items: List[Item], job_count=2) -> Dict[int, List[str]]:
        # node_id -> test_lock.py::TestRvcLock::test_unlock_FOTA_UPDATE_caseid_1982245
        node_id_mapping = {}  # {parent_node_id :"case1;case2;xxx;"}
        num = 0
        time = 0
        node_id_num = {}
        node_id_time = {}
        job_num_mapping: Dict[int, List[str]] = {}
        for item in items:
            node_id = item.nodeid
            cost_second = item.costSecond
            parent_node_id = item.parent.nodeid
            if parent_node_id not in node_id_mapping.keys():
                node_id_mapping[parent_node_id] = [node_id]
                num = 1
                time = cost_second
            else:
                num += 1
                time += cost_second
                node_id_mapping[parent_node_id].append(node_id)
            node_id_time[parent_node_id] = [num, time]
        tmp_job_num_mapping, task_cases = self._case_equal_allocate_by_execution_time(node_id_time, job_count,
                                                                                      node_id_mapping)
        before_dict = {}
        # master端检查收集到的用例数与期望是否一致
        # case_list -> [[模块A], [模块B], [模块n]]
        for job_num, case_list in tmp_job_num_mapping.items():
            job_num_mapping[job_num] = []
            for case in case_list:
                job_num_mapping[job_num].extend(case)
            before_dict[job_num] = len(job_num_mapping[job_num])
        if task_cases == before_dict:
            logger.info(f"收集到的用例数与期望一致，收集到数量为{before_dict}，期望数量为{task_cases}")
        else:
            logger.error(f"收集到的用例数与期望不一致，收集到数量为{before_dict}，期望数量为{task_cases}")
        return job_num_mapping

    @staticmethod
    def _case_equal_allocate_for_node_id(modules, task_num, node_id_mapping):
        sorted_modules = sorted(modules.items(), key=lambda x: x[1], reverse=True)
        tasks = {i: [] for i in range(task_num)}  # 初始化任务列表

        task_cases = {i: 0 for i in range(task_num)}  # 初始化累计case数量

        for module, cases in sorted_modules:
            min_task = min(task_cases, key=task_cases.get)  # 找到累计case数量最少的任务
            tasks[min_task].append((module, cases))  # 将模块分配给累计case数量最少的任务
            task_cases[min_task] += cases  # 更新累计case数量
        logger.info(task_cases)
        # tasks.values():
        # [
        #     [('test_case/tcam/remote_control/remote_climate_schdule/test_cock_reserv.py::TestCockReserv', 225)],
        #     [('test_case/tcam/remote_control/remote_climate_schdule/test_battery_heat.py::TestBattHeat', 209)],
        #     [('test_case/tcam/remote_control/basic_remote_control/test_lock.py::TestRvcLock', 165)]
        # ]
        job_num_mapping = {}  # {job1 : "case1;case2;xxx"}
        for job_num, jobs_info in enumerate(list(tasks.values())):
            for node_id, case_num in jobs_info:
                if job_num not in job_num_mapping.keys():
                    job_num_mapping[job_num] = [node_id_mapping[node_id]]
                else:
                    job_num_mapping[job_num].append(node_id_mapping[node_id])
        return job_num_mapping, task_cases

    @staticmethod
    def _case_equal_allocate_by_execution_time(modules, task_num, node_id_mapping):
        # 将modules转换为包含(模块名, (测试用例数, 执行时间))的列表，并按执行时间降序排序
        sorted_modules = sorted(modules.items(), key=lambda x: x[1][1], reverse=True)
        tasks = {i: [] for i in range(task_num)}  # 初始化任务列表
        # 初始化每个任务的累计执行时间
        task_execution_times = {i: 0 for i in range(task_num)}
        task_execution_nums = {i: 0 for i in range(task_num)}
        for module, execution_info in sorted_modules:
            # 找到累计执行时间最少的任务
            execution_time = execution_info[1]
            execution_num = execution_info[0]
            min_task = min(task_execution_times, key=task_execution_times.get)
            # 将模块分配给该任务，并更新累计执行时间
            tasks[min_task].append((module, execution_time))
            task_execution_times[min_task] += execution_time
            task_execution_nums[min_task] += execution_num
        # 记录每个任务的累计执行时间（可选，用于调试）
        logger.info(f"按时间分类的case{task_execution_times}")

        # 构建任务与节点ID的映射（如果仍需要）
        job_num_mapping = {}
        for job_num, jobs_info in enumerate(list(tasks.values())):
            job_node_ids = []
            for node_id, case_num in jobs_info:
                job_node_ids.append(node_id_mapping[node_id])
            job_num_mapping[job_num] = job_node_ids

        return job_num_mapping, task_execution_nums

    @staticmethod
    def select_case_by_name(items: List[Item], case_list: List):
        new_items = {}
        for item in items:
            node_id = item.nodeid
            new_items[node_id] = item
        items.clear()
        if case_list:
            for node_id, item in new_items.items():
                for case in case_list:
                    if node_id == case:
                        items.append(item)
        if len(case_list) == len(items):
            logger.info(f"期望收集到的case数量为{len(case_list)}, 收集到的case数量为{len(items)}, 与实际收到的一致")
        else:
            logger.error(f"期望收集到的case数量为{len(case_list)}, 收集到的case数量为{len(items)}, 与实际收到的不一致")
        return items

    @staticmethod
    def add_case_marker(items: List[Item], case_list):
        for item in items:
            for case_info in case_list:
                apply_car = case_info.get("applyCar")
                apply_scope = case_info.get("applyScope")
                case_tag = case_info.get("caseTag")
                if_automation = case_info.get("ifAutomation")
                case_id = str(case_info.get('caseId'))
                # 单位转换为s
                costSecond = int(case_info.get('costSecond')) // 1000
                case_priority = case_info.get('casePriority')
                if costSecond == 0:
                    # 如无执行记录默认执行时间为15s
                    costSecond = 15
                if case_id in item.nodeid:
                    # 方式apply_car apply_scope case_tag为空的字符串
                    # if apply_car and apply_car != '[]':
                    #     apply_car = json.loads(apply_car)
                    # 给用例增加costSecond字段
                    item.costSecond = costSecond
                    if isinstance(apply_car, list):
                        for car in apply_car:
                            # car = re.sub(r" +", "_", car)
                            item.add_marker(car)
                    if apply_scope:
                        apply_scope = apply_scope.lower()
                        if apply_scope == 'smoke':
                            item.add_marker('full')
                            item.add_marker('sanity')
                        if apply_scope == 'sanity':
                            item.add_marker('full')
                        item.add_marker(apply_scope)
                    # if case_tag and case_tag != '[]':
                    #     case_tag = json.loads(case_tag)
                    if isinstance(case_tag, list):
                        for tag in case_tag:
                            # tag = re.sub(r" +", "_", tag)
                            item.add_marker(tag)
                    if if_automation:
                        item.add_marker(if_automation)
                    if case_priority:
                        item.add_marker(case_priority)
        return items

    @staticmethod
    def parse_allure_json_get_report() -> ReportInfo:
        report_info = ReportInfo(**{
            "total": 0,
            "passed": 0,
            "failed": 0,
            "error": 0,
            "skipped": 0,
            "success_rate": '',
            "duration_str": '',
            'case_list': [],
            'case_fail_list': [],
        })
        report_path = Path(parent_dir) / '../report/allure_report'
        report_files = os.listdir(report_path)
        logger.debug(f"当前的result.json的数量为{len(report_files)}")
        for file in report_files:
            if file.endswith('result.json'):
                with open(Path(report_path) / file) as f:
                    result_json = json.load(f)
                case_result = result_json.get("status").replace('broken', 'error')
                try:
                    case_full_name = result_json.get("fullName")
                    labels = result_json.get("labels", '')
                    parameters = result_json.get("parameters", '')
                    parts = case_full_name.split('.')
                    if len(parts) > 3:
                        # 替换倒数第二个'.'为'::'
                        parts[-2] = parts[-2] + '.py::' + parts[-1]
                        del parts[-1]

                    recombined_string = '/'.join(parts[:-1])
                    final_part = parts[-1].replace('#', '::')
                    m_case_full_name = recombined_string + '/' + final_part if recombined_string else final_part
                    # test_case/bgm/BaseTech/DiagFlash/test_diag_bgm_did::TestDIDBoot::test_caseid_1981700_00
                    if m_case_full_name:
                        parts_ids = m_case_full_name.split('::')
                        if not re.search(r'\d', parts_ids[-1]):
                            name = result_json.get("name")
                            # name = 'CaseID:116178--泛化记忆_Manual_后排开关记忆ON_设置后排温度'
                            match = re.search(r'CaseID:(\d+)--', name)
                            if match:
                                case_id = match.group(1)
                                m_case_full_name += f'[{case_id}]'
                        # repeat标签
                        repeat_info = {'total_num': None, 'count': None}
                        # 提取repeat相关信息
                        for label in labels or []:  # 确保labels不为None
                            if label.get("name", '') == 'tag' and 'repeat' in label.get("value", ''):
                                repeat_info['total_num'] = label["value"].split('(')[-1].strip(')')
                                break

                        for parameter in parameters or []:  # 确保parameters不为None
                            if parameter.get("name", '') == '__pytest_repeat_step_number':
                                repeat_info['count'] = parameter.get("value", '')
                                break
                        # 更新m_case_full_name
                        if repeat_info['total_num'] and repeat_info['count']:
                            m_case_full_name += f'[{int(repeat_info["count"]) + 1}-{repeat_info["total_num"]}]'
                        # logger.info(f"{file}的case_full_name为{m_case_full_name}")
                        report_info.case_list.append(m_case_full_name)
                        if case_result in ['failed', 'error']:
                            report_info.case_fail_list.append(m_case_full_name)                         
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/case_info_helper.py")
                    logger.warning(f"{file}的case_full_name解析失败, 错误信息为{e}")
                if case_result is not None:
                    report_info[case_result] += 1
        total = report_info.passed + report_info.failed + report_info.error
        report_info.total = total
        if total:
            logger.debug(f"通过用例数:{report_info.passed}, 失败用例数:{report_info.failed}, 总用例数:{total}")
            report_info.success_rate = report_info.passed / total
            report_info.success_rate = "{:.2%}".format(report_info.success_rate)
            logger.info('通过率：' + report_info.success_rate)
        else:
            report_info.success_rate = "0%"

        return report_info

    @staticmethod
    def get_duration_time(start_time: float, end_time: float):
        duration = end_time - start_time
        duration = int(duration)
        miniute = duration // 60
        second = duration % 60
        duration_str = 'Cases Run Total Times:  ' + str(miniute) + '分 ' + str(second) + "秒"
        return duration_str

    @staticmethod
    def get_case_id(case_name):
        pattern = r'caseid_(\d+)(?:_(\d+))*'
        match = re.search(pattern, case_name)
        if match:
            # 使用 findall 查找所有匹配的数字组
            numbers = re.findall(r'\d+', match.group())
            return numbers
        return []

    @staticmethod
    def check(current_case_num, target_case_num):
        if current_case_num == target_case_num:
            str_log = f"当前报告中的用例数:{current_case_num}, 收集到的用例数:{target_case_num}, 用例数一致"
            logger.info(str_log)
            res = True
        else:
            str_log = (f"当前报告中的用例数:{current_case_num}, 收集到的用例数:{target_case_num}, 用例数不一致\n"
                        "请在master端日志查看异常用例列表，关键字：数量异常")
            logger.error(str_log)
            res = False
        return res, str_log
    @staticmethod
    def check_case_list(current_case_list, target_case_list):
        current_case_set = set(current_case_list)
        target_case_set = set(target_case_list)
        logger.debug(f"当前报告中的用例列表:{current_case_set}, 收集到的用例列表:{target_case_set}")
        if current_case_set == target_case_set:
            logger.info("当前报告中的用例列表一致")
        elif len(current_case_set) > len(target_case_set):
            diff_cases = current_case_set - target_case_set
            logger.warning("数量异常: 当前报告中的用例列表多于收集到的用例列表, 多的用例是{}".format(diff_cases))
        else:
            diff_cases = target_case_set - current_case_set
            logger.warning("数量异常: 当前报告中的用例列表少于收集到的用例列表, 少的用例是{}".format(diff_cases))
            return diff_cases
    def case_grouping_by_time(self, job_count, items: List[Item], veh_type: Union[str, None] = None):
        # case_task = {
        #     'two_domain': {"Venus": [], "Mars_One": []},
        #     'single_tcam': {"Venus": [], "Mars_One": []}
        # }
        case_task: Dict[str, Dict[str, List]] = {key: {} for key in Domain().keys()}
        domain_set = set(case_task.keys())
        case_count = 0
        sil_bgm_case = []
        if veh_type:
            veh_type_set = {veh_type}
        else:
            veh_type_set = set(list(map(lambda v: v.value, VehicleModel)))
        for item in items:
            # node_id = item.nodeid
            marks = {mark.name for mark in item.own_markers}
            # SIL用例单独拿出来分组
            if "sil_bgm" in marks:
                sil_bgm_case.append(item)
                case_count += 1
            else:
                # 取出标签中与定义的域控相同的部分，同时满足说明用例筛选成功
                equal_domains = sorted(domain_set & marks)
                equal_veh_types = sorted(veh_type_set & marks)
                if equal_domains and equal_veh_types:
                    # 取第一个域和第一个车型作为用例添加
                    if not veh_type:
                        veh_type = equal_veh_types[0]
                    if veh_type not in case_task[equal_domains[0]].keys():
                        case_task[equal_domains[0]][veh_type] = [item]
                    else:
                        case_task[equal_domains[0]][veh_type].append(item)
                    veh_type = None
                    case_count += 1
                else:
                    logger.warning(f"{item.nodeid}中不包含{equal_domains}或者{equal_veh_types}, 包含的标签{marks}")
        logger.info(f"总共收集到的case数量为{case_count}")
        # tasks = [
        #     {
        #         'domain': 'two_domain',
        #         'vehicle': 'Venus',
        #         'case_dict': {
        #               "test_lock.py::TestRvcLock": {
        #                   "class_case_list": [item],
        #                   "class_total_time": 1
        #                   "case_status": 0
        #               }
        #         },
        #         'case_total_time': 1,
        #         'running_env': 'HIL',
        #     }
        # ]
        tasks = []
        bench_time_dict = {}  # 记录每种台架的case耗时
        benches = []
        for domain, vehicle_info in case_task.items():
            for vehicle, case_list in vehicle_info.items():
                case_total_time = 0
                case_total_num = 1
                case_dict = {}
                for item in case_list:
                    case_total_time += item.costSecond
                    case_total_num += 1
                    node_id = item.parent.nodeid
                    if node_id not in case_dict.keys():
                        case_dict[node_id] = {}
                        case_dict[node_id]["class_case_list"] = [item.nodeid]
                        case_dict[node_id]["case_status"] = CaseStatus.not_start.value
                        case_dict[node_id]["class_total_time"] = item.costSecond
                    else:
                        case_dict[node_id]["class_case_list"].append(item.nodeid)
                        case_dict[node_id]["class_total_time"] += item.costSecond
                # case_dict按照class_total_time降序排序
                # case_dict = OrderedDict(sorted(case_dict.items(), key=lambda x: x[1], reverse=True))
                running_env = "HIL"
                tasks.append(dict(
                    domain=domain,
                    vehicle=vehicle,
                    case_total_num=case_total_num,
                    case_total_time=case_total_time,
                    case_dict=case_dict,
                    running_env="HIL"))
                if (domain, running_env) not in bench_time_dict.keys():
                    bench_time_dict[(domain, running_env)] = case_total_time
                else:
                    bench_time_dict[(domain, running_env)] += case_total_time
        tasks = sorted(tasks, key=lambda d: d['case_total_time'], reverse=True)
        if sil_bgm_case:
            case_dict = {}
            case_total_time = 0
            for item in sil_bgm_case:
                node_id = item.nodeid
                if node_id not in case_dict.keys():
                    case_dict[node_id] = {}
                    case_dict[node_id]["class_case_list"] = [item.nodeid]
                    case_dict[node_id]["case_status"] = CaseStatus.not_start.value
                    case_dict[node_id]["class_total_time"] = item.costSecond
                else:
                    case_dict[node_id]["class_case_list"].append(item.nodeid)
                    case_dict[node_id]["class_total_time"] += item.costSecond
                case_total_time += item.costSecond
            running_env = "SIL"
            domain = "single_bgm"
            tasks.append({'domain': domain, 'vehicle': '', 'case_dict': case_dict, 'running_env': running_env})
            bench_time_dict[(domain, running_env)] = case_total_time
        # 当前只支持SOA单域BGM的用例
        logger.debug(tasks)
        # 记录每种台架的耗时
        # benches = {
        #     "two_domain": 300,
        #     "single_tcam": 100
        # }
        logger.info(f"每种台架的case耗时：{bench_time_dict}")
        for (domain, running_env), case_total_time in bench_time_dict.items():
            # 小于2个小时的单独申请一个台架, 大于2个小时的按2个小时的倍数申请，最大不超过job_count
            h2 = 60 * 60 * 2
            if case_total_time < h2:
                bench_count = 1
                benches.append({"domain": domain, "running_env": running_env})
            else:
                target_bench_count = case_total_time // h2
                bench_count = target_bench_count if target_bench_count < job_count else job_count
                for _ in range(bench_count):
                    benches.append({"domain": domain, "running_env": running_env})
            logger.info(f"需要申请{domain} {running_env}台架{bench_count}个")
        return tasks, benches, case_count


class CaseFeedBackHelper:

    def __init__(self):
        self.feed_back = None  # 是否立即回填
        self.case_ids_repeat_info = {}  # 存放所有repeat的用例及其执行结果
        self.repeat_info = {"count": 0, "result": None, "Pass": 0, "Failure": 0, "Blocking": 0}
        self.current_case_id = None  # 正在执行的用例ID
        self.repeat_flag = False

    def __repr__(self):
        return f"立即回填:{self.feed_back}, 是否repeat:{self.repeat_flag},repeat_info:{self.repeat_info}, " \
               f"current_case_id:{self.current_case_id}, case_ids_repeat_info:{self.case_ids_repeat_info}"

    def add(self):
        self.case_ids_repeat_info[self.current_case_id] = self.repeat_info

    def reset(self):
        self.feed_back = None  # 是否立即回填
        self.repeat_info = {"count": 0, "result": None, "Pass": 0, "Failure": 0, "Blocking": 0}
        self.current_case_id = None  # 正在执行的用例ID
        self.repeat_flag = False

    def parse_node_id(self, node_id, result):
        if "_caseid_" in node_id:
            if "[" in node_id:  # test_lin_networkmanagement_caseid_1960053[1-5]
                repeat_info = node_id.split("[")[1]
                repeat_info = repeat_info.split("]")[0]
                self.current_case_id = node_id.split("_caseid_")[1].split("[")[0]
                aa = repeat_info.split("-")
                if len(aa) == 2:  # 仅repeat的情况
                    self.repeat_info["count"] = int(aa[1])  # 当前用例需要repeat的次数
                    self.feed_back = aa[0] == aa[1]  # 当前用例正在repeat的次数
                    self.repeat_flag = True
                    if self.repeat_info["result"] is None:  # 赋初始执行结果
                        self.repeat_info["result"] = result
                    if self.repeat_info["result"] == "Pass":  # 如果上一次结果为PASS，则更新结果
                        self.repeat_info["result"] = result
                    if result == "Pass":
                        self.repeat_info["Pass"] += 1
                    if result == "Failure":
                        self.repeat_info["Failure"] += 1
                    if result == "Blocking":
                        self.repeat_info["Blocking"] += 1
                    if self.feed_back:
                        self.add()
                if len(aa) == 1:
                    self.repeat_flag = False
                    self.feed_back = True
                    self.current_case_id = repeat_info
            else:
                self.current_case_id = node_id.split("_caseid_")[1]  # 最简单的情形：没有参数化，没有repeat
                self.repeat_flag = False
                self.feed_back = True
        else:
            if "[" in node_id:
                caseid = node_id.split("[")[1]
                caseid = caseid.split("]")[0]
                if "-" in caseid:
                    aa = caseid.split("-")
                    if len(aa) == 3:  # 参数化+repeat
                        self.repeat_info["count"] = int(aa[2])  # 当前用例repeat的次数
                        self.feed_back = aa[1] == aa[2]
                        self.current_case_id = aa[0]
                        self.repeat_flag = True
                        if self.repeat_info["result"] is None:  # 赋初始执行结果
                            self.repeat_info["result"] = result
                        if self.repeat_info["result"] == "Pass":  # 如果上一次结果为PASS，则更新结果
                            self.repeat_info["result"] = result
                        if result == "Pass":
                            self.repeat_info["Pass"] += 1
                        if result == "Failure":
                            self.repeat_info["Failure"] += 1
                        if result == "Blocking":
                            self.repeat_info["Blocking"] += 1
                        if self.feed_back:
                            self.add()
                else:  # 仅参数化, 没有repeat
                    self.current_case_id = caseid
                    self.feed_back = True
                    self.repeat_flag = False


def get_sat_path(nodeid):
    if "[" in nodeid:
        append = nodeid.split("[")[1].split("]")[0]
        if "-" in append:
            append_list = append.split("-")
            if len(append_list) == 2:
                return nodeid.split("[")[0]
            if len(append_list) == 3:
                return nodeid.split("[")[0] + "[" + append_list[0] + "]"
        else:
            return nodeid
    else:
        return nodeid


def back_up_fail_case_log(ecu: EcuInfo):
    """ 保存失败用例的日志"""
    if ecu.log_path:
        logger.info(f"失败用例的日志路径：{ecu.log_path}")
    if ecu.bench_uuid:
        logger.info(f"失败用例的UUID：{ecu.bench_uuid}，台架IP:"
                    f"{ecu.tb_config.get('wifi_localhost', None)}, "
                    f"caseid:{ecu.caseid}")
        res = os.system(f'mkdir -p /root/fail_case_log/{ecu.bench_uuid}')
        if res == 0:
            logger.info(f"用例{ecu.caseid}的失败日志存放目录创建成功。")
            if ecu.log_path:
                jet_log_path = ecu.log_path.get('jet_log', None)
                trace_log_path = ecu.log_path.get('trace_log', None)
                partner_log_path = ecu.log_path.get('parter_log', None)
                if jet_log_path:
                    linux_local_file_copy(f'cp -f {jet_log_path} /root/fail_case_log/{ecu.bench_uuid}/jetlog.zip',
                                          f"失败用例{ecu.caseid} 的jetlog")
                if trace_log_path:
                    linux_local_file_copy(f'cp -f {trace_log_path} /root/fail_case_log/{ecu.bench_uuid}/trace.zip',
                                          f"失败用例{ecu.caseid} 的trace日志")
                if partner_log_path:
                    linux_local_file_copy(f'cp -f {partner_log_path} /root/fail_case_log/{ecu.bench_uuid}/partner.zip',
                                          f"失败用例{ecu.caseid} 的partner日志")
            else:
                logger.info(f"用例{ecu.caseid}的失败日志路径获取失败，未设置")
        else:
            logger.error(f"用例{ecu.caseid}的失败日志存放目录创建失败")


def linux_local_file_copy(cmd, result_describe):
    res = os.system(cmd)
    if res == 0:
        logger.info(f"{result_describe}复制成功")
    else:
        logger.error(f"{result_describe}复制失败")
