#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: smoke_runner.py
@Time: 2022/5/31 16:00
@Author: lei.tao
@Software: PyCharm
@Description: 冒烟测试用例
@Examples:
"""
import allure
import base64
import os
import sys
import pytest

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_ecu.legacy.common.constant import BGM_CONSTANT
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_ecu.legacy.driver.serial_client import get_device_name, BaseSerial
from xat_ecu.legacy.driver.ssh_client import SSHClient, SSHFailException
from xat_ecu.legacy.common.logger import logger


def con(process=None):
    """
    :param process : 进程
    """
    logger.debug(f"检查进程{process}")
    # with allure.step(f"获取串口可用的端口:"):
    #     port = get_device_name()
    #     allure.attach(port)
    # with allure.step(f"开始连接端口，查看进程 {process}"):
    #     com = BaseSerial(port, baudrate=115200, timeout=0.1)
    #     com.send("ps -ef | grep " + process + " | grep -v grep | awk '{print $2}'", timeout=1)
    # with allure.step(f"查看进程{process}的结果:"):
    #     msg = com.receive_data().split('\r\n')[-2]
    # logger.info("串口输出的内容为: {}".format(msg))
    # time.sleep(1)
    # if msg.isdigit():
    #     with allure.step(f"查看进程 {process} 是否启动"):
    #         allure.attach("{0}".format("启动成功"), f"进程 {process}")
    #     with allure.step(f"查看进程 {process} 的PID"):
    #         allure.attach("{0}".format(msg), f"进程 {process} 的PID")
    # else:
    #     with allure.step(f"查看进程 {process} 是否启动"):
    #         allure.attach("{0}".format("启动失败"), f"进程 {process}")
    # assert msg.isdigit() == True, f"【BGM】进程{process}启动失败"
    # com.close()
    try:
        conn = SSHClient(
            hostname=ip,
            port=base64.b64decode(BGM_CONSTANT.BGM_PORT.encode()).decode(),
            username=base64.b64decode(BGM_CONSTANT.BGM_USERNAME.encode()).decode(),
            password=base64.b64decode(BGM_CONSTANT.BGM_PASSWORD.encode()).decode(),
        )
        stdout1, stderr1 = conn.exec_cmd(f"ps -ef | grep {process}")

        with allure.step(f"查看进程 {process}"):
            allure.attach("{0}".format(stdout1), f"进程 {process} 的stdout")
            allure.attach("{0}".format(stderr1), f"进程 {process} 的stderr")

        stdout2, stderr2 = conn.exec_cmd(
            "ps -ef | grep " + process + " | grep -v grep | awk '{print $2}'"
        )
        if stdout2 != "":
            with allure.step(f"查看进程 {process} 是否启动"):
                allure.attach("{0}".format("启动成功"), f"进程 {process}")
            with allure.step(f"查看进程 {process} 的PID"):
                allure.attach("{0}".format(stdout2), f"进程 {process} 的PID")

        elif stdout2 == "":
            with allure.step(f"查看进程 {process} 是否启动"):
                allure.attach("{0}".format("启动失败"), f"进程 {process}")

        assert stdout2 != "", f"【BGM】进程{process}启动失败"

    except SSHFailException as e:
        print(f'The server connect failed with error {e}')
        raise SSHFailException


# @pytest.mark.smoke
@pytest.mark.full
@allure.feature("架构基础")
@allure.story("PM EM")
class Test_process(TestBase):
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

    @allure.title("校验进程：s2s_service")
    def test01_caseid_1196466(self):
        """
        校验进程：s2s_service 是否正常启动
        """
        con(process="s2s_service")

    @allure.title("校验进程：jetlogd")
    def test02_caseid_1196467(self):
        """
        校验进程：jetlogd 是否正常启动
        """
        con(process="jetlogd")

    @allure.title("校验进程：remote_vehicle_status")
    def test03_caseid_1196468(self):
        """
        校验进程：remote_vehicle_status 是否正常启动
        """
        con(process="remote_vehicle_status")

    @allure.title("校验进程：diagd_iautosar")
    def test04_caseid_1196469(self):
        """
        校验进程：diagd_iautosar 是否正常启动
        """
        con(process="diagd_iautosar")

    @allure.title("校验进程：prop")
    def test05_caseid_1196470(self):
        """
        校验进程：prop 是否正常启动
        """
        con(process="prop")

    @allure.title("校验进程：powerMgr")
    def test06_caseid_1196481(self):
        """
        校验进程：powerMgr 是否正常启动
        """
        con(process="powerMgr")

    @allure.title("校验进程：network_manager")
    def test07_caseid_1196482(self):
        """
        校验进程：network_manager 是否正常启动
        """
        con(process="network_manager")

    @allure.title("校验进程：fota")
    def test08_caseid_1196483(self):
        """
        校验进程：fota 是否正常启动
        """
        con(process="fota")

    @allure.title("校验进程：EM2")
    def test9_caseid_1196484(self):
        """
        校验进程：EM2 是否正常启动
        """
        con(process="/app/bin/em2")

    @allure.title("校验进程：ua_server_app")
    def test10_caseid_1196485(self):
        """
        校验进程：ua_server_app 是否正常启动
        """
        con(process="ua_server_app")

    @allure.title("校验进程：arbitrateMgr")
    def test11_caseid_1196486(self):
        """
        校验进程：arbitrateMgr 是否正常启动
        """
        con(process="arbitrateMgr")

    @allure.title("校验进程：certificate_service")
    def test12_caseid_1196487(self):
        """
        校验进程：certificate_service 是否正常启动
        """
        con(process="certificate_service")


if __name__ == '__main__':
    pytest.main()
