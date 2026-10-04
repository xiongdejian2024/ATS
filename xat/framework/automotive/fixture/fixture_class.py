#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :fixture_class.py.py
@time         :2/7/24 14:46
@author       :dejian.xiong@jiduauto.com
@description  :
"""
import os

from pytest import FixtureRequest
from xat_ecu.legacy.common import exception_error
from xat_ecu.legacy.common.logger import logger

from framework.automotive.fixture.fixture_base import FixtureBase
from framework.automotive.utils.data_type import EcuInfo


class Fixtures(FixtureBase):
    def __init__(self):
        ecuinfo = {}
        self.ecuinfo: EcuInfo = EcuInfo(**ecuinfo)

    def ecu(self, request: FixtureRequest):
        logpath = request.config.getoption("--logpath")
        loglevel = request.config.getoption("--loglevel")
        record_log = request.config.getoption("--record_log")
        if record_log == 'true':
            record_log = True
        if record_log == 'false':
            record_log = False
        trace_log = request.config.getoption("--trace_log")
        if trace_log == 'true':
            trace_log = True
        if trace_log == 'false':
            trace_log = False
        sdb_version = request.config.getoption("--sdb_version")
        release_version = request.config.getoption("--release_version")
        disable_env = request.config.getoption("--disable_env")

        fota_task_id = request.config.getoption("--task_id")
        fota_soft_id = request.config.getoption("--soft_id")
        e2e_info = request.config.getoption("--e2e_info")
        fota_tcam_version = request.config.getoption("--fota_tcam_version")

        logger.info('Test session start')
        # logger.info('Test parameter: logpath: %s' % logpath)
        # logger.info('Test parameter: loglevel: %s' % loglevel)
        # logger.info('Test parameter: record_log: %s' % record_log)
        # logger.info('Test parameter: trace_log: %s' % trace_log)

        d = {}
        d.update({'logpath': logpath})
        d.update({'loglevel': loglevel})
        d.update({'record_log': record_log})
        d.update({'trace_log': trace_log})
        d.update({'sdb_version': sdb_version})
        d.update({'release_version': release_version})
        d.update({'disable_env': disable_env})

        d.update({"task_id": fota_task_id})
        d.update({"soft_id": fota_soft_id})
        d.update({"e2e_info": e2e_info})
        d.update({"fota_tcam_version": fota_tcam_version})

        for key, value in d.items():
            setattr(self.ecuinfo, key, value)

        return self.ecuinfo

    def case_function_hook(self, request: FixtureRequest, ecu):
        """
        automatically call `before_each_func(self,ecu)` and
        `after_each_func(self,ecu)` once call for each function
        """
        testname = request.node.name
        self.ecuinfo.testname = testname
        FixtureBase.case_function_hook(request, ecu)

    def case_class_hook(self, request: FixtureRequest, ecu):
        """
        automatically call `before_class(self, ecu)` and
        `after_class(self, ecu)` once call for each class
        """
        FixtureBase.case_class_hook(request, ecu)

    def case_module_hook(self, request: FixtureRequest, ecu):
        """
        automatically call `before_module(ecu)` and
        `after_module(ecu)`
        once call for each module
        """
        FixtureBase.case_module_hook(request, ecu)

    def session_teardown(self):
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

    def case_session(self, request: FixtureRequest):

        '''
        once call for each session
        To finally process the allure report
        '''
        logger.info("session开始执行")
        # 防止之前报告数据没有清楚的影响，开始测试前，再删一次
        del_result = os.system("find ../../../report/allure_report -mindepth 1 -delete")
        if del_result == 0:
            logger.info("测试前 Del allure raw report data OK")
        else:
            err_msg = f"测试前 Del allure raw report data res is {del_result}, ----- run failed"
            logger.error(err_msg)
            raise exception_error.AllureError(err_msg)

        request.addfinalizer(self.session_teardown)
