#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: test_dm.py
@Time: 2022/10/08 16:00
@Author: lei.tao
@Software: PyCharm
@Description: DM测试用例
@Examples:
"""
import os
import re
import sys

import allure
import pytest

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.bgm.case_helper.test_base import TestBase


@allure.feature('BGM BaseTech/软件平台/数据存储')
class Test_DM(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        global ip
        ip = self.tc_config.get('gateway_ip')

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)


    @pytest.mark.full
    @allure.title("folder_readonly_001")
    def test_caseid_109630(self):
        case_failed = []
        for i in ['/home']:
            with allure.step(f"在{i}目录下新建文件test.txt"):
                data = BGM_SSH(ip).type_commands(
                    f"touch {i}/test.txt; ls {i}/test.txt", root_permission=False
                )
            with allure.step(f"查询{i}目录下新建的文件是否存在"):
                logger.info(f"查询到{i}目录下新建的文件为: {data}")
                allure.attach(f"查询的结果为: {data}")
            if "cannot touch" in data:
                allure.attach("{}文件夹的属性为Read-only".format(i))
            else:
                allure.attach("{}文件夹的属性不是为Read-only".format(i))
                if i not in case_failed:
                    case_failed.append(i)
        assert len(case_failed) == 0, "folder_readonly用例执行失败"


    @pytest.mark.full
    @allure.title("folder_readonly_002")
    def test_caseid_109631(self):
        case_failed = []
        for i in ['/app']:
            with allure.step(f"在{i}目录下新建文件test.txt"):
                data = BGM_SSH(ip).type_commands(
                    f"touch {i}/test.txt; ls {i}/test.txt", root_permission=False
                )
            with allure.step(f"查询{i}目录下新建的文件是否存在"):
                logger.info(f"查询到{i}目录下新建的文件为: {data}")
                allure.attach(f"查询的结果为: {data}")
            if "cannot touch" in data:
                allure.attach("{}文件夹的属性为Read-only".format(i))
            else:
                allure.attach("{}文件夹的属性不是为Read-only".format(i))
                if i not in case_failed:
                    case_failed.append(i)
        assert len(case_failed) == 0, "folder_readonly用例执行失败"


    @pytest.mark.full
    @allure.title("folder_readonly_003")
    def test_caseid_109636(self):
        case_failed = []
        for i in ['/bin']:
            with allure.step(f"在{i}目录下新建文件test.txt"):
                data = BGM_SSH(ip).type_commands(
                    f"touch {i}/test.txt; ls {i}/test.txt", root_permission=False
                )
            with allure.step(f"查询{i}目录下新建的文件是否存在"):
                logger.info(f"查询到{i}目录下新建的文件为: {data}")
                allure.attach(f"查询的结果为: {data}")
            if "cannot touch" in data:
                allure.attach("{}文件夹的属性为Read-only".format(i))
            else:
                allure.attach("{}文件夹的属性不是为Read-only".format(i))
                if i not in case_failed:
                    case_failed.append(i)
        assert len(case_failed) == 0, "folder_readonly用例执行失败"


    @pytest.mark.full
    @allure.title("folder_readonly_004")
    def test_caseid_109635(self):
        case_failed = []
        for i in ['/boot']:
            with allure.step(f"在{i}目录下新建文件test.txt"):
                data = BGM_SSH(ip).type_commands(
                    f"touch {i}/test.txt; ls {i}/test.txt", root_permission=False
                )
            with allure.step(f"查询{i}目录下新建的文件是否存在"):
                logger.info(f"查询到{i}目录下新建的文件为: {data}")
                allure.attach(f"查询的结果为: {data}")
            if "cannot touch" in data:
                allure.attach("{}文件夹的属性为Read-only".format(i))
            else:
                allure.attach("{}文件夹的属性不是为Read-only".format(i))
                if i not in case_failed:
                    case_failed.append(i)
        assert len(case_failed) == 0, "folder_readonly用例执行失败"

    
    @pytest.mark.full
    @allure.title("folder_readonly_005")
    def test_caseid_109637(self):
        case_failed = []
        for i in ['/etc']:
            with allure.step(f"在{i}目录下新建文件test.txt"):
                data = BGM_SSH(ip).type_commands(
                    f"touch {i}/test.txt; ls {i}/test.txt", root_permission=False
                )
            with allure.step(f"查询{i}目录下新建的文件是否存在"):
                logger.info(f"查询到{i}目录下新建的文件为: {data}")
                allure.attach(f"查询的结果为: {data}")
            if "cannot touch" in data:
                allure.attach("{}文件夹的属性为Read-only".format(i))
            else:
                allure.attach("{}文件夹的属性不是为Read-only".format(i))
                if i not in case_failed:
                    case_failed.append(i)
        assert len(case_failed) == 0, "folder_readonly用例执行失败"


    @pytest.mark.full
    @allure.title("folder_readonly_006")
    def test_caseid_109629(self):
        case_failed = []
        for i in ['/lib']:
            with allure.step(f"在{i}目录下新建文件test.txt"):
                data = BGM_SSH(ip).type_commands(
                    f"touch {i}/test.txt; ls {i}/test.txt", root_permission=False
                )
            with allure.step(f"查询{i}目录下新建的文件是否存在"):
                logger.info(f"查询到{i}目录下新建的文件为: {data}")
                allure.attach(f"查询的结果为: {data}")
            if "cannot touch" in data:
                allure.attach("{}文件夹的属性为Read-only".format(i))
            else:
                allure.attach("{}文件夹的属性不是为Read-only".format(i))
                if i not in case_failed:
                    case_failed.append(i)
        assert len(case_failed) == 0, "folder_readonly用例执行失败"


    @pytest.mark.full
    @allure.title("folder_readonly_007")
    def test_caseid_109638(self):
        case_failed = []
        for i in ['/usr']:
            with allure.step(f"在{i}目录下新建文件test.txt"):
                data = BGM_SSH(ip).type_commands(
                    f"touch {i}/test.txt; ls {i}/test.txt", root_permission=False
                )
            with allure.step(f"查询{i}目录下新建的文件是否存在"):
                logger.info(f"查询到{i}目录下新建的文件为: {data}")
                allure.attach(f"查询的结果为: {data}")
            if "cannot touch" in data:
                allure.attach("{}文件夹的属性为Read-only".format(i))
            else:
                allure.attach("{}文件夹的属性不是为Read-only".format(i))
                if i not in case_failed:
                    case_failed.append(i)
        assert len(case_failed) == 0, "folder_readonly用例执行失败"


    @pytest.mark.full
    @allure.title("folder_readonly_008")
    def test_caseid_109639(self):
        case_failed = []
        for i in ['/var']:
            with allure.step(f"在{i}目录下新建文件test.txt"):
                data = BGM_SSH(ip).type_commands(
                    f"touch {i}/test.txt; ls {i}/test.txt", root_permission=False
                )
            with allure.step(f"查询{i}目录下新建的文件是否存在"):
                logger.info(f"查询到{i}目录下新建的文件为: {data}")
                allure.attach(f"查询的结果为: {data}")
            if "cannot touch" in data:
                allure.attach("{}文件夹的属性为Read-only".format(i))
            else:
                allure.attach("{}文件夹的属性不是为Read-only".format(i))
                if i not in case_failed:
                    case_failed.append(i)
        assert len(case_failed) == 0, "folder_readonly用例执行失败"


    @pytest.mark.full
    @allure.title("folder_readonly_009")
    def test_caseid_109632(self):
        case_failed = []
        for i in ['/srv']:
            with allure.step(f"在{i}目录下新建文件test.txt"):
                data = BGM_SSH(ip).type_commands(
                    f"touch {i}/test.txt; ls {i}/test.txt", root_permission=False
                )
            with allure.step(f"查询{i}目录下新建的文件是否存在"):
                logger.info(f"查询到{i}目录下新建的文件为: {data}")
                allure.attach(f"查询的结果为: {data}")
            if "cannot touch" in data:
                allure.attach("{}文件夹的属性为Read-only".format(i))
            else:
                allure.attach("{}文件夹的属性不是为Read-only".format(i))
                if i not in case_failed:
                    case_failed.append(i)
        assert len(case_failed) == 0, "folder_readonly用例执行失败"


    @pytest.mark.full
    @allure.title("folder_readonly_010")
    def test_caseid_109633(self):
        case_failed = []
        for i in ['/sbin']:
            with allure.step(f"在{i}目录下新建文件test.txt"):
                data = BGM_SSH(ip).type_commands(
                    f"touch {i}/test.txt; ls {i}/test.txt", root_permission=False
                )
            with allure.step(f"查询{i}目录下新建的文件是否存在"):
                logger.info(f"查询到{i}目录下新建的文件为: {data}")
                allure.attach(f"查询的结果为: {data}")
            if "cannot touch" in data:
                allure.attach("{}文件夹的属性为Read-only".format(i))
            else:
                allure.attach("{}文件夹的属性不是为Read-only".format(i))
                if i not in case_failed:
                    case_failed.append(i)
        assert len(case_failed) == 0, "folder_readonly用例执行失败"


    @pytest.mark.full
    @allure.title("folder_readonly_011")
    def test_caseid_109634(self):
        case_failed = []
        for i in ['/media']:
            with allure.step(f"在{i}目录下新建文件test.txt"):
                data = BGM_SSH(ip).type_commands(
                    f"touch {i}/test.txt; ls {i}/test.txt", root_permission=False
                )
            with allure.step(f"查询{i}目录下新建的文件是否存在"):
                logger.info(f"查询到{i}目录下新建的文件为: {data}")
                allure.attach(f"查询的结果为: {data}")
            if "cannot touch" in data:
                allure.attach("{}文件夹的属性为Read-only".format(i))
            else:
                allure.attach("{}文件夹的属性不是为Read-only".format(i))
                if i not in case_failed:
                    case_failed.append(i)
        assert len(case_failed) == 0, "folder_readonly用例执行失败"


    @pytest.mark.full
    @allure.title("folder_readonly_012")
    def test_caseid_109628(self):
        case_failed = []
        for i in ['/lost+found']:
            with allure.step(f"在{i}目录下新建文件test.txt"):
                data = BGM_SSH(ip).type_commands(
                    f"touch {i}/test.txt; ls {i}/test.txt", root_permission=False
                )
            with allure.step(f"查询{i}目录下新建的文件是否存在"):
                logger.info(f"查询到{i}目录下新建的文件为: {data}")
                allure.attach(f"查询的结果为: {data}")
            if "cannot touch" in data:
                allure.attach("{}文件夹的属性为Read-only".format(i))
            else:
                allure.attach("{}文件夹的属性不是为Read-only".format(i))
                if i not in case_failed:
                    case_failed.append(i)
        assert len(case_failed) == 0, "folder_readonly用例执行失败"


if __name__ == '__main__':
    pytest.main()
