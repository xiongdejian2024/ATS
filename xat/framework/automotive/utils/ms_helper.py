#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :ms_helper.py
@time         :2/8/24 16:53
@author       :dejian.xiong@jiduauto.com
@description  :封装ms相关的操作
"""
from typing import Tuple
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common import exception_error
from xat_ecu.legacy.interface.ms.ms_lib import meterSphere_client


class MsHelper:
    @staticmethod
    def get_test_plan(testplanid, execute_type) -> Tuple:
        """
        获取测试计划
        :param testplanid: 测试计划id
        :param execute_type: 执行类型
        :return: ms上失败用例id
        """
        ms_failedcases_idlist = []
        ms_client = meterSphere_client()
        logger.info("开始获取测试计划 {} MS case info ".format(testplanid))
        if ms_client.signin_flag:
            (
                ms_casesinfo,
                jama_id_mapping,
                fail_case_result_description,
            ) = ms_client.get_customnum_mappings_from_planid(testplanid)
            logger.debug(ms_casesinfo)
            if ms_casesinfo:  # 类型为字典，value的格式：(ms_id, nodeId, status, caseId)
                logger.info(
                    "获取测试计划 {} MS case info 成功, 计划cases数量: {}".format(
                        testplanid, len(ms_casesinfo)
                    )
                )
                if execute_type == "fn":
                    for idstr, plan_caseinfo in ms_casesinfo.items():
                        if plan_caseinfo[2] in ["Failure", "Prepare"]:
                            ms_failedcases_idlist.append(idstr)
                if execute_type == "n":
                    for idstr, plan_caseinfo in ms_casesinfo.items():
                        if plan_caseinfo[2] in ["Prepare"]:
                            ms_failedcases_idlist.append(idstr)
            else:
                err_msg = f"获取测试计划 {ms_casesinfo} MS case info 失败！！！"
                logger.error(err_msg)
                raise exception_error.ConfigError(err_msg)
            return jama_id_mapping, ms_failedcases_idlist, fail_case_result_description, ms_client, ms_casesinfo
        else:
            err_msg = "未登入 MS"
            logger.error(err_msg)
            raise exception_error.ConfigError(err_msg)

    @staticmethod
    def collection_failed_case_by_ms(ms_failedcases_idlist, jama_id_mapping, items):
        if ms_failedcases_idlist:
            if jama_id_mapping:
                for i in range(len(ms_failedcases_idlist)):
                    if ms_failedcases_idlist[i] in jama_id_mapping.values():
                        for key, value in jama_id_mapping.items():
                            if ms_failedcases_idlist[i] == value:
                                # ms_failedcases_idlist[i] = key
                                ms_failedcases_idlist.append(key)
                                break
            new_itemsdict = {}
            for item in items:
                new_itemsdict[item.name] = item

            items.clear()

            for item_name in new_itemsdict:
                for idstr in ms_failedcases_idlist:
                    if idstr in item_name and len(idstr) > 0:
                        items.append(new_itemsdict[item_name])
                        break
        return items

    @staticmethod
    def collection_case_by_ms(ms_case_info, items):
        if ms_case_info:
            new_itemsdict = {}
            for item in items:
                new_itemsdict[item.name] = item

            items.clear()

            for item_name in new_itemsdict:
                for case_id, case_info in ms_case_info.items():
                    if case_id and case_id in item_name:
                        items.append(new_itemsdict[item_name])
                        break
        return items

    @staticmethod
    def sync_current_testResult_to_testplan(planid, testresult_dict, ms_client, is_onlypass, version_info,
                                            result_description, wifi_localhost):
        """
        同步执行结果到测试计划，如果用例已有测试结果，则当前结果不覆盖已有结果

        :params planid: 待同步测试结果的测试计划ID
        :params testresult_dict: 待同步的测试结果
        :params ms_client: MS同步对象
        :params is_onlypass: 是否仅同步执行成功的测试结果
        :params version_info: 版本信息
        :params result_description: 结果描述
        :params wifi_localhost: 上位机IP地址
        """
        if ms_client is None:
            ms_client = meterSphere_client()
        if ms_client.signin_flag:
            (
                ms_casesinfo,
                jama_id_mapping,
                fail_case_result_description,
            ) = ms_client.get_customnum_mappings_from_planid(planid)
            if ms_casesinfo:  # 类型为字典，value的格式：(ms_id, nodeId, status, caseId)
                logger.info("获取测试计划 {} MS case info 成功, 计划cases数量: {}".format(planid, len(ms_casesinfo)))
                logger.info(f"待同步的结果：")
                logger.info(f"{testresult_dict}")
                for case_id_str in testresult_dict:
                    if jama_id_mapping is not None:
                        case_id_str = jama_id_mapping.get(str(case_id_str), case_id_str)
                        id_info = ms_casesinfo.get(case_id_str)
                        if id_info:
                            MSId = id_info[0]
                            MSnodeId = id_info[1]
                            caseId = id_info[3]
                            if id_info[2] in ["Prepare", "Skip"]:  # 只有未执行、跳过状态的用例更新最新的状态
                                result = testresult_dict[case_id_str]
                                if is_onlypass:  # 用例执行成功的同步测试结果
                                    # 只有pass才更新测试计划
                                    if result == "Pass":
                                        if version_info and result_description:
                                            ms_client.set_testcase_status_in_testPlan_new(planid, caseId, result,
                                                                                          wifi_localhost, version_info,
                                                                                          result_description)
                                        else:
                                            ms_client.set_testcase_status_in_testPlan(MSId, MSnodeId, "Pass", caseId)
                                else:

                                    if version_info and result_description:
                                        ms_client.set_testcase_status_in_testPlan_new(planid, caseId, result,
                                                                                      wifi_localhost, version_info,
                                                                                      result_description)
                                    else:
                                        ms_client.set_testcase_status_in_testPlan(MSId, MSnodeId, result, caseId)
                        else:
                            logger.warning(f"同步测试计划时，无效的case_id：{case_id_str}")
            else:
                logger.error("获取测试计划 {} MS case info 失败！！！".format(planid))
        else:
            logger.info("未登入 MS")

    @staticmethod
    def get_project_name_by_plan_id(ms_client: meterSphere_client, plan_id):
        if ms_client:
            return ms_client.get_projectname_by_testPlan(plan_id)
        else:
            ms_client = meterSphere_client()
            return ms_client.get_projectname_by_testPlan(plan_id)

