#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :request_helper.py
@time         :4/15/24 09:54
@author       :dejian.xiong@jiduauto.com
@description  :
"""
import json
import re
import time
from typing import Dict

import requests
from xat_ecu.legacy.common import exception_error
from xat_ecu.legacy.common.logger import logger


class DatabaseHelper:
    def __init__(self, base_url='http://10.80.51.28:8887/'):
        """
        初始化DatabaseHelper对象，设置base_url和headers属性。

        Args:
            base_url (str, optional): 数据库的基本URL地址。默认为'http://10.80.51.28:8887/'。

        Attributes:
            base_url (str): 数据库的基本URL地址。
            headers (dict): HTTP请求头信息。

        """
        self.base_url = base_url
        self.headers = {'Connection': 'keep-alive',
                        'Content-Type': 'application/json;charset=utf-8', 'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.9'}

    def _post(self, url, query, do_assert=False, timeout=65):
        """
        向指定URL发送POST请求并返回响应结果。

        Args:
            url (str): 请求的URL地址。
            query (dict): 请求的查询参数，以字典形式传入。
            do_assert (bool, optional): 是否进行断言。默认为False。
            timeout (int, optional): 请求超时时间。默认为30秒。

        Returns:
            Any: 请求返回的结果，如果请求成功则返回解析后的JSON数据，否则返回None。

        Raises:
            CmdExecuteError: 当do_assert为True且请求失败时，抛出此异常。

        """

        url = f"{self.base_url}{url}"
        data = json.dumps(query)
        start_time = time.time()
        while time.time() - start_time <= timeout * 3:
            try:
                response = requests.post(url=url, data=data, headers=self.headers, timeout=timeout)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/database_helper.py")
                time.sleep(1)
                err_msg = f"请求url:{url}失败，原因{str(e)}"
                logger.error(err_msg)
                time.sleep(0.5)
                continue
            else:
                res_json = response.json()
                if res_json:
                    if res_json.get("msg") == "success":
                        return res_json.get("data")
                    elif res_json.get("msg") == "更新成功":
                        return res_json.get("data")
                    else:
                        # 数据异常
                        err_msg = f"请求url:{url}失败，返回值为:{res_json}，参数为{query}，返回默认值"
                        logger.debug(err_msg)
                        return {'id': -1}
                err_msg = f"请求url:{url}失败，返回值为:{res_json}，2s后继续请求"
                time.sleep(2)
                logger.error(err_msg)
                if do_assert:
                    raise exception_error.CmdExecuteError(err_msg)
        else:
            err_msg = f"请求url:{url}失败并超时"
            logger.error(err_msg)
            if do_assert:
                raise exception_error.CmdExecuteError(err_msg)
    
    def _get(self, url, do_assert=False, timeout=65):
        """
        发送GET请求获取数据。
        
        Args:
            url (str): 请求的URL。
            do_assert (bool, optional): 是否在失败时抛出异常。默认为False。
            timeout (int, optional): 请求超时时间。默认为65秒。
        
        Returns:
            dict: 返回请求成功后的JSON数据中的"data"字段，若请求失败或数据异常则返回{'id': -1}。
        
        Raises:
            CmdExecuteError: 在do_assert为True且请求失败时抛出异常。
        
        """
        url = f"{self.base_url}{url}"
        start_time = time.time()
        while time.time() - start_time <= timeout * 3:
            try:
                response = requests.get(url=url, headers=self.headers, timeout=timeout)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/database_helper.py")
                time.sleep(1)
                err_msg = f"请求url:{url}失败，原因{str(e)}"
                logger.error(err_msg)
                time.sleep(0.5)
                continue
            else:
                res_json = response.json()
                if res_json:
                    if res_json.get("msg") == "success":
                        return res_json.get("data")
                    else:
                        # 数据异常
                        err_msg = f"请求url:{url}失败，返回值为:{res_json}，返回默认值"
                        logger.warning(err_msg)
                        return {'id': -1}
                err_msg = f"请求url:{url}失败，返回值为:{res_json}，2s后继续请求"
                time.sleep(2)
                logger.error(err_msg)
                if do_assert:
                    raise exception_error.CmdExecuteError(err_msg)
        else:
            err_msg = f"请求url:{url}失败并超时"
            logger.error(err_msg)
            if do_assert:
                raise exception_error.CmdExecuteError(err_msg)

    def get_ms_testcase_list(self, url="mstestcase/list", **kwargs):
        """
        获取测试用例列表。

        Args:
            url (str, optional): 获取测试用例列表的接口URL。默认为 "mstestcase/list"。
            **kwargs:
                - projectName (str): 项目名称。
                - caseId (str): 测试用例ID。
                - applyCar (str): 应用车辆。
                - caseTag (str): 测试用例标签。
                - casePriority (str): 测试用例优先级。
                - do_assert (bool): 是否执行断言。

        Returns:
            dict: 包含测试用例列表信息的字典。

        """
        projectName = kwargs.get("projectName")
        caseId = kwargs.get("caseId")
        applyCar = kwargs.get("applyCar")
        caseTag = kwargs.get("caseTag")
        casePriority = kwargs.get("casePriority")
        do_assert = kwargs.get("do_assert", True)  # 默认为True， 如果接口出现问题直接抛出异常
        query = dict(
            projectName=projectName,
            caseId=caseId,
            applyCar=applyCar,
            caseTag=caseTag,
            casePriority=casePriority
        )
        data = self._post(url=url, query=query, do_assert=do_assert)
        logger.debug(f"获取testcase_list成功 对应的参数:{query}，对应的接口:{url}")
        return data

    def update_ms_bench_version_info(self, url="msbenchversioninfo/addOrUpdate", **kwargs):
        """
        更新bench_version_info信息。

        Args:
            url (str, optional): 更新bench_version_info的接口URL。默认为 "msbenchversioninfo/addOrUpdate"。
            **kwargs:
                - yamlName (str): YAML配置文件名。
                - benchIp (str): Bench环境的IP地址。
                - commitId (str): 版本控制系统的提交ID。
                - lastModifyTime (str): 最后一次修改时间。
                - lastModifyUser (str): 最后一次修改的用户。
                - do_assert (bool): 是否执行断言。

        Returns:
            int: 更新成功后返回的ID。

        """
        yamlName = kwargs.get("yamlName")
        benchIp = kwargs.get("benchIp")
        commitId = kwargs.get("commitId")
        lastModifyTime = kwargs.get("lastModifyTime")
        lastModifyUser = kwargs.get("lastModifyUser")
        do_assert = kwargs.get("do_assert")
        query = dict(
            yamlName=yamlName,
            benchIp=benchIp,
            commitId=commitId,
            lastModifyTime=lastModifyTime,
            lastModifyUser=lastModifyUser,
        )
        data = self._post(url=url, query=query, do_assert=do_assert)
        bench_version_id = data.get('id')
        logger.info(f"更新bench_version_info成功 返回的id为{bench_version_id} 对应的参数:{query}，对应的接口:{url}")
        return bench_version_id

    def update_ms_framework_version_info(self, url="msframeworkversioninfo/addOrUpdate", **kwargs):
        """
        更新framework_version_info信息。

        Args:
            url (str, optional): 更新framework_version_info的接口URL。默认为 "msframeworkversioninfo/addOrUpdate"。
            **kwargs:
                - sdkInterfaceVersion (str): SDK接口版本号。
                - satFrameworkVersion (str): SAT框架版本号。
                - ecuSimulatorVersion (str): ECU模拟器版本号。
                - satCommitId (str): SAT代码库的提交ID。
                - do_assert (bool): 是否在更新过程中执行断言。

        Returns:
            int: 更新成功后返回的ID。

        """
        sdkInterfaceVersion = kwargs.get("sdkInterfaceVersion")
        satFrameworkVersion = kwargs.get("satFrameworkVersion")
        ecuSimulatorVersion = kwargs.get("ecuSimulatorVersion")
        satCommitId = kwargs.get("satCommitId")
        do_assert = kwargs.get("do_assert")
        query = dict(
            sdkInterfaceVersion=sdkInterfaceVersion,
            satFrameworkVersion=satFrameworkVersion,
            ecuSimulatorVersion=ecuSimulatorVersion,
            satCommitId=satCommitId
        )
        data = self._post(url=url, query=query, do_assert=do_assert)
        framework_version_id = data.get('id')
        logger.info(
            f"更新framework_version_info成功 返回的id为{framework_version_id} 对应的参数:{query}，对应的接口:{url}")
        return framework_version_id

    def update_ms_bench_ecu_info(self, url="msbenchecuinfo/addOrUpdate", **kwargs):
        """
        添加ms_bench_ecu_info信息。

        Args:
            url (str, optional): 更新bench_ecu_info的接口url。Defaults to "msbenchecuinfo/addOrUpdate".
            **kwargs:
                - caseId (str): 测试用例的唯一标识符。
                - costSecond (float): 测试用例运行所花费的时间（以秒为单位）。
                - runResult (str): 测试用例的运行结果。
                - scriptPath (str): 测试用例执行脚本的文件路径。
                - benchEcu (str): 用于测试的电子控制单元（ECU）的标识符或相关信息。
                - benchVersion (str): 测试环境的版本信息。
                - frameworkVersion (str): 测试框架的版本信息。
                - do_assert (bool): 一个布尔值，指示是否在测试失败时进行断言（即是否抛出异常）。

        Returns:
            Any: 添加成功后返回的数据，可能是响应对象或其他相关信息。

        """
        bgmBootVersion = kwargs.get("bgmBootVersion")
        softwareVersion = kwargs.get("softwareVersion")
        hardwareVersion = kwargs.get("hardwareVersion")
        bgmMcuVersion = kwargs.get("bgmMcuVersion")
        bgmSwitchVersion = kwargs.get("bgmSwitchVersion")
        idlVersion = kwargs.get("idlVersion")
        jidlVersion = kwargs.get("jidlVersion")
        bootesVersion = kwargs.get("bootesVersion")
        sdbVersion = kwargs.get("sdbVersion")
        carType = kwargs.get("carType")
        do_assert = kwargs.get("do_assert")
        query = dict(
            bgmBootVersion=bgmBootVersion,
            softwareVersion=softwareVersion,
            hardwareVersion=hardwareVersion,
            bgmMcuVersion=bgmMcuVersion,
            bgmSwitchVersion=bgmSwitchVersion,
            idlVersion=idlVersion,
            jidlVersion=jidlVersion,
            bootesVersion=bootesVersion,
            sdbVersion=sdbVersion,
            carType=carType,
        )
        data = self._post(url=url, query=query, do_assert=do_assert)
        bench_ecu_id = data.get('id')
        logger.info(f"更新bench_ecu_info成功 返回的id为{bench_ecu_id} 对应的参数:{query}，对应的接口:{url}")
        return bench_ecu_id

    def add_ms_case_run(self, url="mscaserun/add", **kwargs):
        """
        添加ms_case_run信息。

        Args:
            url (str, optional): 添加ms_case_run的接口url。Defaults to "mscaserun/add".
            **kwargs:
                - caseId (str): 测试用例的唯一标识符。
                - costSecond (float): 测试用例运行所花费的时间（以秒为单位）。
                - startTime (float): 测试用例运行的开始时间（以秒为单位）。
                - endTime (float): 测试用例运行的结束时间（以秒为单位）。
                - runResult (str): 测试用例的运行结果。
                - scriptPath (str): 测试用例执行脚本的文件路径。
                - benchEcu (str): 用于测试的电子控制单元（ECU）的标识符或相关信息。
                - benchVersion (str): 测试环境的版本信息。
                - frameworkVersion (str): 测试框架的版本信息。
                - do_assert (bool): 一个布尔值，指示是否在测试失败时进行断言（即是否抛出异常）。

        Returns:
            Any: 添加成功后返回的数据，可能是响应对象或其他相关信息。

        """
        caseId = kwargs.get("caseId")
        costSecond = kwargs.get("costSecond")
        startTime = kwargs.get("startTime")
        endTime = kwargs.get("endTime")
        runResult = kwargs.get("runResult")
        scriptPath = kwargs.get("scriptPath")
        benchEcu = kwargs.get("benchEcu")
        benchVersion = kwargs.get("benchVersion")
        frameworkVersion = kwargs.get("frameworkVersion")
        do_assert = kwargs.get("do_assert")
        runUnique = kwargs.get("runUnique")
        agentIp = kwargs.get("agentIp")
        classUnique = kwargs.get("classUnique")
        msTestplanId = kwargs.get("msTestplanId")
        query = dict(
            caseId=caseId,
            costSecond=costSecond,
            startTime=startTime,
            endTime=endTime,
            runResult=runResult,
            scriptPath=scriptPath,
            benchEcu=benchEcu,
            benchVersion=benchVersion,
            frameworkVersion=frameworkVersion,
            agentIp=agentIp,
            classUnique=classUnique
        )

        if runUnique is not None:
            query['runUnique'] = runUnique
        if msTestplanId is not None:
            query['msTestplanId'] = msTestplanId

        data = self._post(url=url, query=query, do_assert=do_assert)
        logger.info(f"添加ms_case_run成功 返回数据为: {data} 对应的参数:{query}，对应的接口:{url}")
        return data

    def add_ecu_version_deploy(self, url="ecuversiondeploy/add", **kwargs):
        """
        添加ms_case_run信息。

        Args:
            url (str, optional): 添加add_ecu_version_deploy的接口url。Defaults to "ecuversiondeploy/add".
            **kwargs:
                - ecuType (str): ecu名称。
                - ecuVersion (float): ecu版本。
                - deployTime (float): 编译时间。

        Returns:
            Any: 添加成功后返回的数据，可能是响应对象或其他相关信息。

        """
        ecuType = kwargs.get("ecuType")
        ecuVersion = kwargs.get("ecuVersion")
        deployTime = kwargs.get("deployTime")
        do_assert = kwargs.get("do_assert")
        query = dict(
            ecuType=ecuType,
            ecuVersion=ecuVersion,
            deployTime=deployTime
        )
        data = self._post(url=url, query=query, do_assert=do_assert)
        logger.info(f"添加ecu_version_deploy成功 返回数据为: {data} 对应的参数:{query}，对应的接口:{url}")
        return data

    def add_device_test_task(self, url="deviceTestTask/add", **kwargs):
        """
        写入任务

        Args:
            url (str, optional): 添加device_test_task的接口url。Defaults to "deviceTestTask/add".
            **kwargs:
                - deviceId (str): 台架ip。
                - code (str): 任务命令。
                - distibuteTaskId (str): 任务id。

        Returns:
            Any: 添加成功后返回的数据，可能是响应对象或其他相关信息。

        """
        deviceId = kwargs.get("deviceId")
        code = kwargs.get("code")
        distibuteTaskId = kwargs.get("distibuteTaskId")
        do_assert = kwargs.get("do_assert")
        job_info = kwargs.get('job_info')
        document_id = kwargs.get('willow_feishu_config_info').fail_case_document_id
        table_name = kwargs.get('willow_feishu_config_info').fail_case_sheet_name
        query = dict(
            deviceId=deviceId,
            distibuteTaskId=distibuteTaskId,
            code=code,
            jobName=job_info.job_name,
            jobId=job_info.job_id,
            planTotalCaseNum=job_info.plan_total_case_num,
            documentId=document_id,
            tableName=table_name
        )
        if job_info.testplan_id is not None:
            query["msTestplanId"] = job_info.testplan_id
        data = self._post(url=url, query=query, do_assert=do_assert)
        logger.info(f"添加add_device_test_task成功 返回数据为: {data} 对应的参数:{query}，对应的接口:{url}")
        return data

    def update_device_test_task(self, url="deviceTestTask/updateAllure", **kwargs):
        """
        更新设备任务信息生成的allure报告

        Args:
            url (str, optional): 添加device_test_task的接口url。Defaults to "deviceTestTask/add".
            **kwargs:
                - deviceId (str): 台架ip。
                - code (str): 任务命令。
                - distibuteTaskId (str): 任务id。

        Returns:
            Any: 添加成功后返回的数据，可能是响应对象或其他相关信息。

        """
        wifi_localhost = kwargs.get('willow_feishu_config_info').wifi_localhost
        distribute_task_id = kwargs.get('willow_feishu_config_info').distibute_task_id
        allure_report = kwargs.get('willow_feishu_config_info').allure_report

        query = dict(
            deviceId=wifi_localhost,
            distibuteTaskId=distribute_task_id,
            allureReport=allure_report
        )

        data = self._post(url=url, query=query)
        logger.info(f"update_device_test_task 的allure报告成功 返回数据为: {data} 对应的参数:{query}，对应的接口:{url}")
        return data

    def update_bench_save(self, url="bench/save", **kwargs):
        """
        更改台架状态的接口，状态包括空闲、环境部署中、用例运行中等

        Args:
            url (str, optional): 更新bench_save的接口url。Defaults to "bench/save".
            **kwargs:
                - agentIp (str): 台架ip。
                - status (int): 状态。

        Returns:
            Any: 添加成功后返回的数据，可能是响应对象或其他相关信息。

        """
        agentIp = kwargs.get("agentIp")
        status = kwargs.get("status")
        do_assert = kwargs.get("do_assert")
        query = dict(
            agentIp=agentIp,
            status=status,
        )
        data = self._post(url=url, query=query, do_assert=do_assert)
        logger.debug(f"更新update_bench_save成功 返回数据为: {data} 对应的参数:{query}，对应的接口:{url}")
        return data

    def update_test_task(self, url="testTask/update", **kwargs):
        """
        用例进度更新接口

        Args:
            url (str, optional): 更新test_task的接口url。Defaults to "testTask/update".
            **kwargs:
                - deviceId (str): 台架ip。
                - distibuteTaskId (str): 分布式任务id。
                - totalCaseCount (int): 用例总数。
                - passCaseCount (int): 用例通过数。
                - failCaseCount (int): 失败用例数。
                - errorCaseCount (int): 错误用例数。
                - leftCaseCount (int): 剩余用例数。
                - currentCase (str): 当前执行case。

        Returns:
            Any: 添加成功后返回的数据，可能是响应对象或其他相关信息。

        """
        deviceId = kwargs.get("deviceId")
        distibuteTaskId = kwargs.get("distibuteTaskId")
        totalCaseCount = kwargs.get("totalCaseCount")
        passCaseCount = kwargs.get("passCaseCount")
        failCaseCount = kwargs.get("failCaseCount")
        errorCaseCount = kwargs.get("errorCaseCount")
        leftCaseCount = kwargs.get("leftCaseCount")
        currentCase = kwargs.get("currentCase")
        do_assert = kwargs.get("do_assert")
        sync_ms_result = kwargs.get("syncMsFailCount")
        query = dict(
            deviceId=deviceId,
            distibuteTaskId=distibuteTaskId,
            totalCaseCount=totalCaseCount,
            passCaseCount=passCaseCount,
            failCaseCount=failCaseCount,
            errorCaseCount=errorCaseCount,
            leftCaseCount=leftCaseCount,
            currentCase=currentCase,
            syncMsFailCount=sync_ms_result
        )
        data = self._post(url=url, query=query, do_assert=do_assert)
        logger.debug(f"更新update_test_task成功 返回数据为: {data} 对应的参数:{query}，对应的接口:{url}")
        return data

    def get_test_task(self, url="testTask/query", **kwargs):
        """
        用例进度查询接口

        Args:
            url (str, optional): 获取test_task的接口url。Defaults to "testTask/query".
            **kwargs:
                - deviceId (str): 台架ip。
                - distibuteTaskId (str): 分布式任务id。
                - log_print (bool): 是否打印日志。

        Returns:
            Any: 添加成功后返回的数据，可能是响应对象或其他相关信息。

        """
        deviceId = kwargs.get("deviceId")
        distibuteTaskId = kwargs.get("distibuteTaskId")
        do_assert = kwargs.get("do_assert")
        log_print = logger.info if kwargs.get("log_print", True) else logger.debug
        query = dict(
            deviceId=deviceId,
            distibuteTaskId=distibuteTaskId,
        )
        data = self._post(url=url, query=query, do_assert=do_assert)
        log_print(f"获取get_test_task成功 返回数据为: {data} 对应的参数:{query}，对应的接口:{url}")
        return data

    def get_device_test_task_query_status(self, url="deviceTestTask/queryStatus", **kwargs):
        """
        用例进度查询接口

        Args:
            url (str, optional): 获取device_test_task_query_status的接口url。Defaults to "deviceTestTask/queryStatus".
            **kwargs:
                - deviceId (str): 台架ip。
                - distibuteTaskId (str): 分布式任务id。
                - log_print (bool): 是否打印日志。

        Returns:
            Any: 添加成功后返回的数据，可能是响应对象或其他相关信息。

        """
        deviceId = kwargs.get("deviceId")
        distibuteTaskId = kwargs.get("distibuteTaskId")
        do_assert = kwargs.get("do_assert")
        log_print = logger.info if kwargs.get("log_print", True) else logger.debug
        query = dict(
            deviceId=deviceId,
            distibuteTaskId=distibuteTaskId,
        )
        data = self._post(url=url, query=query, do_assert=do_assert)
        log_print(f"获取get_device_test_task_query_status成功 返回数据为: {data} 对应的参数:{query}，对应的接口:{url}")
        return data

    def get_available_bench(self, url="distributeTask/getAvaiableBench", **kwargs) -> Dict:
        """
        获取空闲台架信息

        Args:
            url (str, optional): 获取device_test_task_query_status的接口url。Defaults to "distributeTask/getAvaiableBench".
            **kwargs:
                - ipAddr (str): 台架ip。
                - excludeIpAddr (list): 排除的ip地址。
                - lockDirMaster (str): master锁目录。
                - lockDirSlave (str): slave锁目录。
                - single_bgm (int): single_bgm数量。
                - single_Tcam (int): single_Tcam数量。
                - two_domain (int): two_domain数量。
                - four_domain (int): four_domain数量。
                - bgmVersion (str): 期望bgm的版本。
                - tcamVersion (str): 期望tcam的版本。
                - log_print (bool): 是否打印日志。
                - do_assert (bool): 是否抛出异常。

        Returns:
                {
                    "msg": "success",
                    "data": {
                        "masterId": "M-320e33b9-b457-4e6b-bb31-620197fd8c16",
                        "singalTcam": [
                        ],
                        "doubleDomain": [
                            {
                                "cdcVersion": null,
                                "bgmVersion": "6160110200AY",
                                "userName": "",
                                "password": "",
                                "bgmVersion": "6160110200AY",
                                "slaveId": "S-8bb93208-6028-480d-846c-318614553207",
                                "acuVersion": null,
                                "deviceId": "172.18.128.185",
                                "limitedIp": "172.18.163.185",
                                "tcamVersion": "016110110200AT"
                            },
                            {
                                "cdcVersion": null,
                                "bgmVersion": "6160110200AY",
                                "userName": "",
                                "password": "",
                                "slaveId": "S-a6611775-f21b-4b65-9a3b-293bbb6ee413",
                                "acuVersion": null,
                                "deviceId": "172.18.128.186",
                                "limitedIp": "172.18.163.186",
                                "tcamVersion": "016110110200AT"
                            }
                        ],
                        "singalBgm": [
                        ],
                        "deviceId": "172.18.128.184",
                        "userName": "",
                        "password": "",
                        "fourDomain": [
                        ]
                    },
                    "status": 1
                }
        """
        ipAddr = kwargs.get("ipAddr")
        excludeIpAddr = kwargs.get("excludeIpAddr", [])
        lockDirMaster = kwargs.get("lockDirMaster")
        lockDirSlave = kwargs.get("lockDirSlave")
        singalBgm = kwargs.get("single_bgm", 0)
        singalTcam = kwargs.get("single_tcam", 0)
        doubleDomain = kwargs.get("two_domain", 0)
        fourDomain = kwargs.get("four_domain", 0)
        SIL = kwargs.get("SIL", 0)
        bgmVersion = kwargs.get("bgmVersion", '')
        tcamVersion = kwargs.get("tcamVersion", '')
        do_assert = kwargs.get("do_assert")
        log_print = logger.info if kwargs.get("log_print", True) else logger.debug
        query = dict(
            ipAddr=ipAddr,
            excludeIpAddr=excludeIpAddr,
            lockDirMaster=lockDirMaster,
            lockDirSlave=lockDirSlave,
            singalBgm=singalBgm,
            singalTcam=singalTcam,
            doubleDomain=doubleDomain,
            fourDomain=fourDomain,
            bgmVersion=bgmVersion,
            tcamVersion=tcamVersion,
            do_assert=do_assert
        )
        data: Dict = self._post(url=url, query=query, do_assert=do_assert)
        log_print(f"获取get_available_bench成功 返回数据为: {data} 对应的参数:{query}，对应的接口:{url}")
        bench_infos = []
        if singalBgm:
            for bench_info in data.get('singalBgm'):
                bench_info['domain'] = 'singalBgm'
                bench_infos.append(bench_info)
        if singalTcam:
            for bench_info in data.get('singalTcam'):
                bench_info['domain'] = 'singalTcam'
                bench_infos.append(bench_info)
        if doubleDomain:
            for bench_info in data.get('doubleDomain'):
                bench_info['domain'] = 'doubleDomain'
                bench_infos.append(bench_info)
        if fourDomain:
            for bench_info in data.get('fourDomain'):
                bench_info['domain'] = 'fourDomain'
                bench_infos.append(bench_info)
        if SIL:
            for bench_info in data.get('SIL'):
                bench_info['domain'] = 'SIL'
                bench_infos.append(bench_info)
        p_data = dict(
            master_id=data.get('masterId'),
            device_id=data.get('deviceId'),
            limited_ip=data.get('limitedIp'),
            master_username=data.get('userName'),
            master_password=data.get('password'),
            bgm_version=data.get('bgmVersion'),
            tcam_version=data.get('tcamVersion'),
            cdc_version=data.get('cdcVersion'),
            acu_version=data.get('acuVersion'),
            bench_type_list=data.get('benchTypeList'),
            bench_infos=bench_infos
        )
        return p_data

    def update_heart_beat(self, url="distributeTask/heartBeatUpdate", **kwargs):
        """
        更新心跳

        Args:
            url (str, optional): 更新update_heart_beat的接口url。Defaults to "distributeTask/heartBeatUpdate".
            **kwargs:
                - deviceId (str): 台架ip。
                - benchRole (str): 角色（master或者slave）。
                - masterId (str): 对应master的唯一标志符。

        Returns:
            Any: 添加成功后返回的数据，可能是响应对象或其他相关信息。

        """
        deviceId = kwargs.get("deviceId")
        benchRole = kwargs.get("benchRole")
        masterId = kwargs.get("masterId")
        do_assert = kwargs.get("do_assert")
        log_print = logger.info if kwargs.get("log_print", True) else logger.debug
        query = dict(
            deviceId=deviceId,
            benchRole=benchRole,
            masterId=masterId
        )
        data = self._post(url=url, query=query, do_assert=do_assert)
        log_print(f"获取update_heart_beat成功 返回数据为: {data} 对应的参数:{query}，对应的接口:{url}")
        return data

    def get_query_lock_status(self, url="distributeTask/queryLockStatus/", **kwargs):
        """
        获取分布式锁状态

        Args:
            url (str, optional): 获取query_lock_status的接口url。Defaults to "distributeTask/queryLockStatus/".
            **kwargs:
                - ip_addr (str): 台架ip。

        Returns:
            返回值：{"status":1,"msg":"success","data":-1} # -1代表无此台架，0代表台架空闲，1代表台架占用中

        """
        ip_addr = kwargs.get("ip_addr")
        do_assert = kwargs.get("do_assert")
        log_print = logger.info if kwargs.get("log_print", True) else logger.debug
        query = dict(
            ipAddr=ip_addr
        )
        data = self._post(url=url, query=query, do_assert=do_assert)
        log_print(f"获取get_query_lock_status成功 返回数据为: {data} 对应的参数:{query}，对应的接口:{url}")
        return data

    def get_query_account_info(self, url="distributeTask/queryAccountInfo/", **kwargs):
        """
        通过ip获取用户名和密码

        Args:
            url (str, optional): 获取query_account_info的接口url。Defaults to "distributeTask/queryAccountInfo/".
            **kwargs:
                - ip_addr (str): 台架ip。

        Returns:
            返回值：{"status":1,"msg":"success","data":-1} # -1代表无此台架，0代表台架空闲，1代表台架占用中

        """
        ip_addr = kwargs.get("ip_addr")
        do_assert = kwargs.get("do_assert")
        log_print = logger.info if kwargs.get("log_print", True) else logger.debug
        query = dict(
            ipAddr=ip_addr
        )
        data = self._post(url=url, query=query, do_assert=do_assert)
        log_print(f"获取get_query_account_info成功 返回数据为: {data} 对应的参数:{query}，对应的接口:{url}")
        return data
    def get_query_benchgroup(self, url="distributeBenchInfo/queryBenchGroup/", **kwargs):
        """
        获取benchgroup

        Args:
            url (str, optional): 请求的url地址，默认为"distributeBenchInfo/queryBenchGroup/"。
            **kwargs: 其他可选参数，包括：
                ip_addr (str): 目标IP地址,必须为台架的无线地址。
                do_assert (bool): 是否进行断言操作
                log_print (bool): 是否打印日志

        Returns:
            data: 台架的分组名称。当没有设置分组或者无线IP不存在，返回为空字符串。

        """
        ip_addr = kwargs.get("ip_addr")
        url = url + ip_addr
        do_assert = kwargs.get("do_assert")
        log_print = logger.info if kwargs.get("log_print", True) else logger.debug
        data = self._get(url=url, do_assert=do_assert)
        log_print(f"获取{ip_addr}台架的get_query_benchgroup成功 返回数据为: {data} ,对应的接口:{url}")
        return data
def get_ms_testcase_module(case):
    """
    根据测试用例路径获取对应模块名称
    
    Args:
        case (str): 测试用例路径
    
    Returns:
        str: 测试用例对应的模块名称
    
    """
    pattern_number = r'\[(\d+)\]|caseid_(\d+)'
    case_parts = case.split('/')
    if len(case) >= 3:
        project_part = case_parts[1]
        if project_part == 'bgm':
            projectName = 'BGM_ComponentTest'
        elif project_part == 'tcam':
            projectName = 'TCAM_ComponentTest'
        elif project_part == 'soa':
            projectName = 'SOA平台测试'
        else:
            logger.warning(f"未知的项目部分：{project_part}")
            return None
        match = re.search(pattern_number, case_parts[-1])
        if match:
            if match.group(1):
                caseId = match.group(1)
            elif match.group(2):
                caseId = match.group(2)
        else:
            logger.warning(f"无法解析caseId，case为{case}")
            return None
        if projectName and caseId:
            dh = DatabaseHelper()
            case_info = dh.get_ms_testcase_list(projectName=projectName, caseId=caseId)
            if case_info:
                moudles = case_info[0].get('nodePath','').split('/')
                moudles = [moudle for moudle in moudles if moudle]
                if len(moudles) >=3:
                    return moudles[2]
                else:
                    return moudles[-1]
    else:
        logger.warning(f"无法解析caseId，case为{case}")
        return None
def get_ms_testcase_top_module(case_list, top_number=3):
    """
    从给定的测试用例列表中提取出前top_number个最常用的模块名称
    
    Args:
        case_list (list): 测试用例列表，每个元素都是一个字符串表示的测试用例路径
        top_number (int): 需要返回的前top_number个模块名称,默认为3
        
    Returns:
        list: 包含前top_number个模块名称的列表
    
    """
    module_dict = {}
    for case in case_list:
        module = get_ms_testcase_module(case)
        if module:
            if module not in module_dict:
                module_dict[module] = 1
            else:
                module_dict[module] += 1
    if module_dict:
        top_keys = [item[0] for item in sorted(module_dict.items(), key=lambda item: item[1], reverse=True)[:top_number]]
        return top_keys
    return []

if __name__ == '__main__':
    # dh = DatabaseHelper()
    # print(dh.get_available_bench(ipAddr='172.18.163.144'))
    # dh.get_device_test_task_query_status(deviceId='172.18.128.78', distibuteTaskId='M-835ca82e-bb37-4257-bad6-508d4f43f5c0')
    get_ms_testcase_module('test_case/tcam/basetech/diagnostics/test_diag_tcam_full.py::TestUdSService::test_caseid_1990206[7-50]')
    # dh.get_query_lock_status(ip_addr='172.18.128.231')
    # dh.get_available_bench(
    #     ipAddr='172.18.128.231', 
    #     excludeIpAddr=[], 
    #     lockDirMaster='/root/lei_test/sat',
    #     lockDirSlave='/root/autotest', 
    #     two_domain=1)
