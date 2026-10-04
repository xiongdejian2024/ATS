#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :feishu_task.py
@Time         :2024/7/25 11:48
@Author       :dejian.xiong@jiduauto.com
@Description  :
"""
import json
import os
import sys
import re
from datetime import datetime, timedelta
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from xat_ecu.legacy.common.logger import Logger
from xat_ecu.legacy.interface.feishu.feishu_api import feishu_api
from xat_ecu.legacy.interface.ms.ms_lib import meterSphere_client
from framework.automotive.utils.artifactory_helper import ArtifactoryHelper
from framework.automotive.utils.feishu_helper import send_error_msg

logger = Logger().get_logger("test")
# 根据不同的基线匹配不同的动态标签
MARK_DICT = {
    '2.0.0': ' and not v110only and not v140only and not stress_test and not v210 and Automated',
    '2.1.0': ' and not v110only and not v140only and not v200only and not stress_test and Automated',
    '2.2.0': ' and not v210only and not v110only and not v140only and not v200only and not stress_test and Automated',
    '3.0.0': ' and not v210only and not v110only and not v140only and not v200only and not stress_test and Automated',
    'default': ' and not stress_test and Automated'
}


def get_willow_json_params():
    with open(os.path.join(BASE_DIR, "../", "task.json")) as f:
        task_obj = json.load(f)
    return task_obj


def parse_overall_requirements_return_ruler(feishu: feishu_api, task_des, table_name='总体需求'):
    table_id = feishu.get_table_id_by_table_name(table_name)
    overall_requirements_data = feishu.get_records_in_table(table_id)
    willow_ruler = ''
    logger.info(f"获取到表格{table_name}的数据为{overall_requirements_data}")
    for index, requirement in enumerate(overall_requirements_data):
        if requirement['fields']['任务描述'] == task_des:
            if requirement['fields']['任务分类'] != "集中化CICD":
                logger.error(f"任务描述为{task_des}不为集中化CICD任务，不触发")
                raise Exception(f"任务描述为{task_des}不为集中化CICD任务，不触发")
            trigger_mode = requirement['fields']['触发方式']
            if get_willow_task_json("run_immediately") == "否":
                if trigger_mode == 'Willow流水线触发':
                    weekday_number = datetime.now().weekday()
                    willow_trigger_rule = requirement['fields']['时间']
                    if willow_trigger_rule:
                        if willow_trigger_rule[weekday_number] == "0":
                            raise Exception(f"流水线触发规则为{willow_trigger_rule}，当前为周{weekday_number + 1}，不触发")
                if get_willow_task_json("executor") == 'system':
                    if requirement['fields']['生效'] == '否':
                        raise Exception(f"任务描述为{task_des}未生效，不触发")
                    # 需要判断一下流水线触发时间和规则的时间：1，每天、每隔触发；2，每周触发的需要判断当前时间
                    if  trigger_mode in ('每日', '每隔'):
                        logger.info('流水线正常触发流程')
                    elif trigger_mode == '每周':
                        now = datetime.now()
                        # 如果第二天中午12点之前出包，也触发
                        if now.hour < 12:
                            now -= timedelta(days=1)
                        weekday_number = str(now.weekday() + 1)
                        willow_trigger_rule = requirement['fields']['时间']
                        if willow_trigger_rule:
                            parts = willow_trigger_rule.split('/')
                            unique_numbers = set()
                            for part in parts:
                                number = part.split('-')[0]
                                unique_numbers.add(number)
                            if weekday_number not in unique_numbers:
                                raise Exception(f"流水线触发规则为{willow_trigger_rule}，当前为周{weekday_number}，不触发")
            willow_ruler = requirement['fields']['Willow'][0]["text"]
            feishu_ruler = requirement['fields']['飞书'][0]["text"]
            if willow_ruler:
                return willow_ruler, trigger_mode, feishu_ruler
            else:
                logger.error(f"没有找到任务描述为{task_des}的任务")
                send_error_msg(task_des, f"没有找到任务描述为{task_des}的任务")
                raise Exception(f"没有找到任务描述为{task_des}的任务")
def update_task_info(feishu: feishu_api, key, task_des, data_name, data, table_name='总体需求'):
    logger.info(f"更新表格{table_name}中任务描述为{task_des}的数据{data_name}为{data}")
    table_id = feishu.get_table_id_by_table_name(table_name)
    willow_ruler_data = feishu.get_records_in_table(table_id)
    logger.info(f"获取到表格{table_name}的数据为{willow_ruler_data}")
    for index, ruler_data in enumerate(willow_ruler_data):
        ruler_data_fields = ruler_data['fields']
        if ruler_data_fields[key] == task_des:
            records_id = ruler_data['record_id']
            break
    feishu.update_record_in_table(
        table_id=table_id,
        record_id=records_id,
        data={data_name: data}
        )          

def parse_willow_rulers(feishu: feishu_api, trigger_mode, ruler, table_name='Willow规则'):
    table_id = feishu.get_table_id_by_table_name(table_name)
    willow_ruler_data = feishu.get_records_in_table(table_id)
    logger.info(f"获取到表格{table_name}的数据为{willow_ruler_data}")
    for index, ruler_data in enumerate(willow_ruler_data):
        ruler_data_fields = ruler_data['fields']
        if ruler_data_fields['规则名'] == ruler:
            plan_id = ruler_data_fields['测试计划ID']
            code_version = format_code_version(ruler_data_fields['自动化版本'])
            case_mark = ruler_data_fields['用例筛选']
            test_scope = ruler_data_fields['测试范围']
            if test_scope and set(test_scope) != {'P0', 'P1', 'P2', 'P3'}:
                or_conditions = ' or '.join(test_scope)
                case_mark = case_mark + f' and ({or_conditions})'
            project_name = ruler_data_fields['项目']
            # ecu = ruler_data_fields['ECU']
            target_version_dicts = get_target_version(ruler_data_fields['目标版本'])
            if len(target_version_dicts) == 1:
                for k , v in target_version_dicts.items():
                    ecu = k
                    target_baseline = v[0]
                    target_version = v[1]
                case_mark += next((MARK_DICT[version] for version in MARK_DICT if version in target_baseline), MARK_DICT['default'])
                if get_willow_task_json("executor") == 'system':
                    task_img_url = get_willow_task_json("img_url")
                    if target_baseline.lower() not in task_img_url or target_version not in task_img_url or ecu.upper() not in task_img_url:
                        logger.error(f"任务中{target_baseline}和{target_version}的版本不匹配，当前触发的版本为{task_img_url}")
                        raise Exception(f"任务中{target_baseline}和{target_version}的版本不匹配，当前触发的版本为{task_img_url}")
                test_plan = get_test_plans(project_name, target_baseline, target_version, ruler)
            elif len(target_version_dicts) == 2:
                test_plans = []
                img_match = []
                for k , v in target_version_dicts.items():
                    ecu = k
                    target_baseline = v[0]
                    target_version = v[1]
                    if get_willow_task_json("executor") == 'system':
                        task_img_url = get_willow_task_json("img_url")
                        if target_baseline.lower() not in task_img_url or target_version not in task_img_url or ecu.upper() not in task_img_url:
                            logger.error(f"任务中{target_baseline}和{target_version}的版本不匹配，当前触发的版本为{task_img_url}")
                            img_match.append(False)
                        else:
                            img_match.append(True)
                            # raise Exception(f"任务中{target_baseline}和{target_version}的版本不匹配，当前触发的版本为{task_img_url}")
                    # test_plan = get_test_plans(ecu.upper(), target_baseline, target_version)
                    test_plans.append(get_test_plans(project_name, target_baseline, target_version, ruler))
                target_baseline_bgm = target_version_dicts['bgm'][0]
                target_baseline_tcam = target_version_dicts['tcam'][0]
                if target_baseline_bgm == target_baseline_tcam:
                    case_mark += next((MARK_DICT[version] for version in MARK_DICT if version in target_baseline), MARK_DICT['default'])
                else:
                    case_mark += MARK_DICT['default']
                    logger.warning(f"bgm和tcam的基线版本不一致，将不动态更新mark")
                if get_willow_task_json("executor") == 'system':
                    if not img_match[0] and not img_match[1]:
                        logger.error(f"任务中{target_version_dicts}的版本均不匹配，当前触发的版本为{task_img_url}")
                        raise Exception(f"任务中{target_version_dicts}的版本均不匹配，当前触发的版本为{task_img_url}")
                if test_plans[0] == test_plans[1]:
                    test_plan = test_plans[0]
                else:
                    test_plan = None
            else:
                logger.error(f"目标版本格式错误:{target_version_dicts},当前仅支持最多两域")
                send_error_msg(task_des, f"目标版本格式错误{target_version_dicts}，当前仅支持最多两域")
                raise Exception(f"目标版本格式错误{target_version_dicts}，当前仅支持最多两域")
            if '周提测' in ruler:
                if test_plan:
                    # 如果获取了测试计划，则使用获取到的测试计划
                    plan_id = test_plan
                elif plan_id:
                # 周提测，则使用表格中默认填写的plan_id
                    logger.info(f"使用表格中默认填写的plan_id: {plan_id}")
                    send_error_msg(task_des, f"MS未匹配到{project_name}项目的{target_version_dicts}版本的测试计划，将使用Sdata中填写的plan_id: {plan_id}", willow_url=willow_url, msg_color='yellow')
                else:
                    logger.error(f"没有找到{project_name}项目下的{target_version_dicts}版本的plan_id，无法执行")
                    send_error_msg(task_des, f"未匹配到{project_name}项目下的{target_version_dicts}版本的测试计划，无法执行")
                    raise Exception(f"没有找到{project_name}项目下的{target_version_dicts}版本的plan_id，无法执行")
            else:
                try:
                    # 非周提测，则创建一个新的测试计划
                    test_plan = creat_testplan_and_add_case(project_name)
                    plan_id = test_plan
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/feishu/feishu_task.py")
                    logger.error(f"非周提测任务根据参数project:{project_name}、版本信息：{target_version_dicts}，创建测试计划失败:{e},将使用Sdata中填写的plan_id: {plan_id}")
                    send_error_msg(task_des, f"非周提测任务根据参数project:{project_name}、版本信息：{target_version_dicts}，创建测试计划失败:{e},将使用Sdata中填写的plan_id: {plan_id}", willow_url=willow_url, msg_color='yellow')
                    if not plan_id:
                        logger.error(f"没有找到{project_name}项目下的{target_version_dicts}版本的plan_id，无法执行")
                        send_error_msg(task_des, f"未匹配到{project_name}项目下的{target_version_dicts}版本的测试计划，无法执行")
                        raise Exception(f"没有找到{project_name}项目下的{target_version_dicts}版本的plan_id，无法执行")
            return plan_id, test_plan, code_version, case_mark, target_version_dicts
    else:
        logger.error(f"没有找到{table_name}为{ruler}的任务")
        send_error_msg(task_des, f"没有找到{table_name}为{ruler}的willow规则")
        raise Exception(f"没有找到{table_name}为{ruler}的任务")
def parse_cdc_mcu_willow_rulers(feishu: feishu_api, trigger_mode, ruler, table_name='Willow规则'):
    table_id = feishu.get_table_id_by_table_name(table_name)
    willow_ruler_data = feishu.get_records_in_table(table_id)
    logger.info(f"获取到表格{table_name}的数据为{willow_ruler_data}")
    for index, ruler_data in enumerate(willow_ruler_data):
        ruler_data_fields = ruler_data['fields']
        if ruler_data_fields['规则名'] == ruler:
            plan_id = ruler_data_fields['测试计划ID']
            target_version_dicts = get_target_version(ruler_data_fields['目标版本'])
            project_name = ruler_data_fields['项目']
            if len(target_version_dicts) == 1:
                for k , v in target_version_dicts.items():
                    ecu = k
                    target_baseline = v[0]
                    target_version = v[1]
            else:
                logger.error(f"目标版本格式错误:{target_version_dicts},当前仅支持CDCMCU")
                send_error_msg(task_des, f"目标版本格式错误{target_version_dicts}，当前仅支持CDCMCU")
                raise Exception(f"目标版本格式错误{target_version_dicts}，当前仅支持CDCMCU")
            test_plan = get_test_plans(project_name, target_baseline, target_version, '先按照周提测流程来走')
            if test_plan:
                plan_id = test_plan
            elif plan_id:
                logger.info(f"使用表格中默认填写的plan_id: {plan_id}")
                send_error_msg(task_des, f"MS未匹配到{project_name}项目的{target_version_dicts}版本的测试计划，将使用Sdata中填写的plan_id: {plan_id}", willow_url=willow_url, msg_color='yellow')
            else:
                logger.error(f"没有找到{project_name}项目下的{target_version_dicts}版本的plan_id，无法执行")
                send_error_msg(task_des, f"未匹配到{project_name}项目下的{target_version_dicts}版本的测试计划，无法执行")
                raise Exception(f"没有找到{project_name}项目下的{target_version_dicts}版本的plan_id，无法执行")
            code_version = format_code_version(ruler_data_fields['自动化版本'])
            case_mark = ruler_data_fields['用例筛选']
            test_scope = ruler_data_fields['测试范围']
            if test_scope and set(test_scope) != {'P0', 'P1', 'P2', 'P3'}:
                or_conditions = ' or '.join(test_scope)
                case_mark = case_mark + f' and ({or_conditions})'
            project_name = ruler_data_fields['项目']
            return plan_id, plan_id, code_version, case_mark, target_version_dicts
    else:
        logger.error(f"没有找到{table_name}为{ruler}的任务")
        send_error_msg(task_des, f"没有找到{table_name}为{ruler}的willow规则")
        raise Exception(f"没有找到{table_name}为{ruler}的任务")
def parse_feishu_rulers(feishu: feishu_api, ruler, table_name='飞书规则'):
    table_id = feishu.get_table_id_by_table_name(table_name)
    feishu_ruler_data = feishu.get_records_in_table(table_id)
    logger.info(f"获取到表格{table_name}的数据为{feishu_ruler_data}")
    for index, ruler_data in enumerate(feishu_ruler_data):
        ruler_data_fields = ruler_data['fields']
        if ruler_data_fields['规则名'] == ruler:
            fail_case_document_id = ruler_data_fields['文档ID']
            fail_case_sheet_name = ruler_data_fields['表格名称']
            feishu_rule_key = ruler_data_fields['字段规则']
            return fail_case_document_id, fail_case_sheet_name, feishu_rule_key
    else:
        logger.error(f"没有找到{table_name}为{ruler}的飞书规则")
        send_error_msg(task_des, f"没有找到{table_name}为{ruler}的飞书规则")
        raise Exception(f"没有找到{table_name}为{ruler}的飞书规则")

def generate_update_url(ecu, target_baseline, target_version):
    if ecu == 'bgm':
        baseline_url = f'https://repo.jidudev.com/artifactory/BGMSoftware/Release/{target_baseline}'
        bgm_package_list = ArtifactoryHelper.get_url_list(baseline_url)
        logger.info(f"bgm app包列表为:{bgm_package_list}")
        for package_name in bgm_package_list:
            if package_name.endswith(f"{target_version}"):
                base_img_url = f'{baseline_url}/{package_name}'
                img_url = f'{base_img_url}/{package_name}.bin'
                logger.info(f"bgm app包的链接为:{img_url}")
                keyinfo = ArtifactoryHelper.get_keyinfo(url=img_url.replace('bin', 'keyinfo'))
                logger.info(f"bgm app包的keyinfo为:{keyinfo}")
                img_url_boot = ArtifactoryHelper.get_boot_url(url=base_img_url)
                logger.info(f"bgm boot包的链接为:{img_url_boot}")
                keyinfo_boot = ArtifactoryHelper.get_keyinfo(url=img_url_boot.replace('bin', 'keyinfo'))
                logger.info(f"bgm boot包的keyinfo为:{keyinfo_boot}")
                return img_url, keyinfo, img_url_boot, keyinfo_boot
    elif ecu == 'tcam':
        baseline_url = f'https://repo.jidudev.com/artifactory/TCAMSoftware/Release/{target_baseline}'
        tcam_package_list = ArtifactoryHelper.get_url_list(baseline_url)
        logger.info(f"tcam app包列表为:{tcam_package_list}")
        for package_name in tcam_package_list:
            if package_name.endswith(f"{target_version}"):
                base_img_url = f'{baseline_url}/{package_name}'
                img_url = f'{base_img_url}/{package_name}.bin'
                logger.info(f"tcam app包的链接为:{img_url}")
                keyinfo = ArtifactoryHelper.get_keyinfo(url=img_url.replace('bin', 'keyinfo'))
                logger.info(f"tcam app包的keyinfo为:{keyinfo}")
                # tcam_img_url
                # tcam_keyinfo = task_dict.get("tcam_keyinfo
                return img_url, keyinfo
    elif ecu == 'cdc-mcu':
        baseline_url = f'https://repo.jidudev.com/artifactory/CDC/Release'
        
        cdc_package_list = ArtifactoryHelper.get_url_list(baseline_url)
        parts = target_baseline[1:].split('.')
        base_line = ''
        for part in parts:
            base_line += part
        logger.info(f"CDC-muc app包列表为:{cdc_package_list}")
        for package_name in cdc_package_list:
            if package_name.endswith(f"{base_line}{target_version}"):
                base_img_url = f'{baseline_url}/{package_name}'
                img_url = f'{base_img_url}/{package_name}.bin'
                logger.info(f"cdc app包的链接为:{img_url}")
                keyinfo = ArtifactoryHelper.get_bin_keyinfo(url=img_url)
                logger.info(f"cdc app包的keyinfo为:{keyinfo}")
                # tcam_img_url
                # tcam_keyinfo = task_dict.get("tcam_keyinfo
                return img_url, keyinfo
    else:
        logger.error(f"不支持的获取{ecu}的版本url")
        raise Exception(f"不支持的获取{ecu}的版本url")
                


def generate_summery_json(plan_id, test_plan, code_version, case_mark, target_version_dicts, 
                          fail_case_document_id, fail_case_sheet_name, feishu_rule_key):
    # tasks = get_willow_json_params()
    tasks = {}
    tasks['plan_id'] = plan_id if plan_id else ''
    tasks['test_plan'] = test_plan if test_plan else ''
    tasks['case_mark'] = case_mark if case_mark else ''
    tasks["fail_case_document_id"] = fail_case_document_id if fail_case_document_id else ''
    tasks["fail_case_sheet_name"] = fail_case_sheet_name if fail_case_sheet_name else ''
    tasks['feishu_rule_key'] = feishu_rule_key if feishu_rule_key else ''
    if isinstance(code_version, tuple):
        tasks['code_version'] = code_version[1]
        tasks[
            'inputTestScriptGit '] = f'-b {code_version[0]} ${XAT_CREDENTIAL_URL_3}'
    else:
        tasks['code_version'] = code_version
    if 'bgm' in target_version_dicts:
        img_url, keyinfo, img_url_boot, keyinfo_boot = generate_update_url("bgm", target_version_dicts["bgm"][0].lower(), target_version_dicts["bgm"][1].upper())
        tasks['img_url'] = img_url
        tasks['keyinfo'] = keyinfo
        tasks['img_url_boot'] = img_url_boot
        tasks['keyinfo_boot'] = keyinfo_boot
    if 'tcam' in target_version_dicts:
        img_url, keyinfo = generate_update_url("tcam", target_version_dicts["tcam"][0].lower(), target_version_dicts["tcam"][1].upper())
        tasks['tcam_img_url'] = img_url
        tasks['tcam_keyinfo'] = keyinfo
    if 'cdc-mcu' in target_version_dicts:
        img_url, keyinfo = generate_update_url("cdc-mcu", target_version_dicts["cdc-mcu"][0].lower(), target_version_dicts["cdc-mcu"][1].upper())
        tasks['img_url'] = img_url
        tasks['keyinfo'] = keyinfo
    # else:
    #     logger.warning(f"不支持的获取{target_version_dicts}的版本url，将不获取")
    os.makedirs(os.path.join(BASE_DIR, "../", "report"), exist_ok=True)
    with open(os.path.join(BASE_DIR, "../", "report", "report_summary.json"), 'w') as f:
        json.dump(tasks, f)
def get_willow_task_json(key):
    path = os.path.join(BASE_DIR, "../", "task.json")
    with open(path, 'r') as f:
        data = json.load(f)
    try:
        logger.info(f"task.json {key}的数据为:{data[key]}")
        return str(data[key])
    except KeyError as e:
        logger.error(f"task.json {key}的数据为不存在")
        raise Exception(e)
    # return str(data['willow_flow_result_id'])
    

def format_code_version(code_version):
    if code_version == 'New_Release':
        return ''
    if code_version == 'New_Daily':
        return 'new'
    if '_' in code_version:
        version_list = code_version.split('_')
        if len(version_list) == 4:
            return f'{version_list[0]}', f'{version_list[1]} {version_list[2]} {version_list[3]}'
def get_target_version(input_str):
    """
    智能处理单个字符串或逗号分隔的字符串，通过下划线分割并提取信息。
    
    :param input_str: 输入的字符串，可以是单个'模块名_版本号_类型'或逗号分隔的多个此类字符串
    :return: 一个包含多个元组的列表，每个元组包含模块名、版本号和类型
    """
    if ',' in input_str or '，' in input_str:
        parts = re.split(r'[,，]', input_str)
    else:
        parts = [input_str]
    # 初始化一个空列表来存储提取的信息
    extracted_info = {}
    for part in parts:
        # 去除可能的空白字符（如空格、换行符等）
        part = part.strip()
        subparts = part.split('_')
        if len(subparts) >= 3:
            ecu = subparts[0]
            baseline = subparts[1]
            vesion = subparts[2]
            extracted_info[ecu] = [baseline, vesion]
        else:
            logger.error(f"提取版本信息错误，版本信息{part}不符合规则")
            send_error_msg(task_des, f"提取版本信息错误，版本信息{part}不符合规则")
            raise Exception(f"提取版本信息错误，版本信息{part}不符合规则")
    # 输出: {'bgm': ['v2.2.0', 'AL'], 'tcam': ['v2.1.0', 'AD']}
    return extracted_info
def get_test_plans(project_name, target_baseline, target_version, ruler):
    if '周提测' in ruler:
        test_tpye = '版本提测'
    else:
        test_tpye = '脚本稳定性'
    ms_client = meterSphere_client()
    test_plans = ms_client.get_testplan_id_by_condition(project_name, target_baseline, target_version, test_tpye)
    for test_plan in test_plans:
        if test_plan:
            logger.info(f"找到{project_name}项目下的{target_baseline}基线下的{target_version}版本的回填TestPlanID为{test_plan}")
            return test_plan
def creat_testplan_and_add_case(project_name):
    """
    根据传入的项目名称、目标版本字典和测试类型，创建测试计划并添加测试用例。
    
    Args:
        project_name (str): 项目名称。
        target_version_dicts (dict): 目标版本字典，包含基线版本和测试版本。
        test_tpye (str, optional): 测试类型，默认为'脚本稳定性'。
    
    Returns:
        int: 创建的测试计划的ID。
    
    Raises:
        Exception: 如果目标版本字典不符合规则（如版本数量不符合预期，或基线版本不同），则抛出异常。
    """
    now = datetime.now()
    # 格式化时间为YYYYMMDDHHmm格式
    timestamp = now.strftime('%Y%m%d%H%M')
    name = project_name + '_脚本稳定性_' + timestamp
    ms_clinet = meterSphere_client()
    plan_id = ms_clinet.creat_new_testplan(project_name=project_name, testplan_name=name)
    ids = ms_clinet.get_testcases_from_project_by_condition(project_name, ex_con=['未规划用例', '历史用例'])
    ms_clinet.add_testcase_to_testplan(plan_id, ids, project_name)
    time.sleep(2)
    if plan_id:
        ms_clinet.change_testplan_status(project_name=project_name, planId=plan_id, status='已归档')
    else:
        raise Exception(f"创建测试计划失败")
    return plan_id
    
def main():
    global task_des
    if len(sys.argv) == 2:
        task_des = sys.argv[1]
    else:
        task_des = "Test_cicd"
    willow_flow_id = get_willow_task_json("willow_flow_id")
    global willow_url 
    willow_url = f"https://willow.jiduprod.com/flow/flow_history?flowID={willow_flow_id}"
    source_feishu = feishu_api()
    source_feishu.get_app_access_token()
    source_feishu.get_user_access_token()
    document_id = 'U7OUwlovWiddnwkZDTwcINsrnRe'
    requirements_table_name = '总体需求'
    willow_rulers_table_name = 'Willow规则'
    feishu_rulers_table_name = '飞书规则'
    source_feishu.get_bitable_app_access_token(document_id=document_id)
    # 获取需求
    try:
        willow_ruler, trigger_mode, feishu_ruler = parse_overall_requirements_return_ruler(source_feishu, task_des, requirements_table_name)
        logger.info(f"willow规则:{willow_ruler}, 触发方式为:{trigger_mode}")
        if 'CDC_MCU' in task_des:
            plan_id, test_plan, code_version, case_mark, target_version_dicts = parse_cdc_mcu_willow_rulers(source_feishu, trigger_mode, willow_ruler, 
                                                                                                           willow_rulers_table_name)
            fail_case_document_id, fail_case_sheet_name, feishu_rule_key = '', '', ''
        else:
            # 获取willow规则
            plan_id, test_plan, code_version, case_mark, target_version_dicts = parse_willow_rulers(source_feishu, trigger_mode, willow_ruler, 
                                                                                                            willow_rulers_table_name)
            # 获取飞书规则
            fail_case_document_id, fail_case_sheet_name, feishu_rule_key = parse_feishu_rulers(source_feishu, feishu_ruler, feishu_rulers_table_name)
        # 生成汇总json
        generate_summery_json(plan_id, test_plan, code_version, case_mark, target_version_dicts, 
                              fail_case_document_id, fail_case_sheet_name, feishu_rule_key)
    except Exception as e:
        # logger.error(f"解析任务失败:{e}")
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/feishu/feishu_task.py")
        update_task_info(source_feishu, "任务描述", task_des, "执行状态", "获取任务失败")
        raise Exception(f"解析任务失败:{e}")
    else:
        logger.info("解析任务成功")
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ts = int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S"))) * 1000
        update_task_info(source_feishu, "任务描述", task_des, "开始时间", ts)
        update_task_info(source_feishu, "任务描述", task_des, "执行状态", "进行中")
        update_task_info(source_feishu, "规则名", willow_ruler, "flow_result_id", get_willow_task_json("willow_flow_result_id"), willow_rulers_table_name)
        


if __name__ == '__main__':
    main()
