#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: test_networkChannel.py
@Time: 2022/10/11 10:08
@Author: lei.tao
@Software: PyCharm
@Description: 网络通道定义测试用例
@Examples:
"""
import base64
import os
import subprocess
import sys
import time
import tempfile
import allure
import pytest

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_ecu.legacy.common.constant import BGM_CONSTANT
from xat_ecu.legacy.driver.adb_client import Adb, ADBFailException
from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.bgm.case_helper.test_base import TestBase


def con_bgm(cmd):
    """
    针对一些特殊命令, 通过python获取不到值时, 需要用到sshpass命令来获取
    但是子进程产生一些数据, 他们会被buffer起来, 当buffer满了, 会写到子进程的标准输出和标准错误输出,
    这些东西通过管道发送给父进程。当管道满了之后, 子进程就停止写入, 于是就卡住了, 及时取走管道的输出就不会出现阻塞了
    此处采取的是临时文件接收子进程输出, 由于临时文件是建立在磁盘上的, 没有size的限制,
    并且文件被close后, 相应的磁盘上的空间也会被释放掉
    """
    global out_temp
    try:
        # 得到一个临时文件对象,  调用close后, 此文件从磁盘删除
        out_temp = tempfile.TemporaryFile(mode='w+')
        # 获取临时文件的文件号
        fileno = out_temp.fileno()
        usr = base64.b64decode(BGM_CONSTANT.BGM_USERNAME.encode()).decode()
        pwd = base64.b64decode(BGM_CONSTANT.BGM_PASSWORD.encode()).decode()
        command = f"sshpass -p {pwd} ssh {usr}@{ip} \"bash --login -c '{cmd}'\""

        conn = subprocess.Popen(command, shell=True, stdout=fileno, stderr=fileno)
        conn.wait()
        # 从临时文件读出shell命令的输出结果
        out_temp.seek(0)
        rt = out_temp.read()
    except Exception as e:
        logger.error(e)

    # return conn[0].decode()
    finally:
        if out_temp:
            out_temp.close()

    return rt.strip()


def con_tcam(cmd=None):
    try:
        conn = Adb()
        res = conn.shell(cmd)
        return res

    except ADBFailException as e:
        logger.error(f'The server connect failed with error {e}')
        raise ADBFailException


@pytest.mark.full_other
@allure.feature("互联服务")
@allure.story("移动网络")
class Test_NetworkChannel(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        global ip, device
        ip = self.tc_config.get('gateway_ip')
        device = self.tc_config.get('eth_vlan')

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)

    # @pytest.mark.smoke
    @pytest.mark.full_other
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1196143?projectId=46"
    )
    @allure.title("DataIsolation_TCAM_Vlan5_BGM_Vlan5用例")
    def test01_caseid_1196143(self):
        case_failed = []

        with allure.step(f"查看vlan5通道的网络"):
            bgm = con_bgm(cmd=f"ping -I eth0.5 172.16.5.31 -c 4")
            with allure.step("vlan5 ping 5.31的网络结果:"):
                allure.attach(bgm)
                if "100% packet loss" not in bgm:
                    allure.attach(f"bgm vlan5通道可以ping通172.16.5.31")
                else:
                    allure.attach(f"bgm vlan5通道不可以ping通172.16.5.31")
                    case_failed.append("bgm vlan5通道不可以ping通172.16.5.31")

        assert (
            len(case_failed) == 0
        ), f"NetworkChannelDefinition_DataIsolation_TCAM_Vlan5_BGM_Vlan5用例执行失败"

    # @pytest.mark.smoke
    @pytest.mark.full_other
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1196144?projectId=46"
    )
    @allure.title("DataIsolation_TCAM_Vlan9_BGM_Vlan9用例")
    def test02_caseid_1196144(self):
        case_failed = []

        with allure.step(f"查看vlan9通道的网络"):
            bgm = con_bgm(cmd=f"ping -I eth0.9 172.16.9.31 -c 4")
            with allure.step("vlan9 ping 9.31的网络结果:"):
                allure.attach(bgm)
                if "100% packet loss" not in bgm:
                    allure.attach(f"bgm vlan9通道可以ping通172.16.9.31")
                else:
                    allure.attach(f"bgm vlan9通道不可以ping通172.16.9.31")
                    case_failed.append("bgm vlan9通道不可以ping通172.16.9.31")

        assert (
            len(case_failed) == 0
        ), f"NetworkChannelDefinition_DataIsolation_TCAM_Vlan9_BGM_Vlan9用例执行失败"

    """
    vlan 11端口已删除
    @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1196145?projectId=46")
    @allure.title("DataIsolation_TCAM_Vlan11_BGM_Vlan11用例")
    def test03_caseid_1196145(self):
        case_failed = []

        with allure.step(f"查看vlan11通道的网络"):
            bgm = con_bgm(cmd=f"ping -I eth0.11 172.16.11.31 -c 4")
            print(bgm)
            if "4 packets transmitted, 4 received" in bgm:
                allure.attach(f"bgm vlan11通道可以ping通172.16.11.31")
            else:
                allure.attach(f"bgm vlan11通道不可以ping通172.16.11.31")
                case_failed.append("bgm vlan11通道不可以ping通172.16.11.31")

            data = con_bgm(cmd=f"ping -I eth0.9 172.16.11.31 -c 4")
            print(data)
            if "4 packets transmitted, 4 received" in data:
                allure.attach(f"bgm vlan9通道可以ping通172.16.11.31")
                case_failed.append("bgm vlan9通道可以ping通172.16.11.31")
            else:
                allure.attach(f"bgm vlan9通道不可以ping通172.16.11.31")

        assert len(case_failed) == 0, f"NetworkChannelDefinition_DataIsolation_TCAM_Vlan11_BGM_Vlan11用例执行失败"
    """

    # @pytest.mark.smoke
    @pytest.mark.full_other
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1196146?projectId=46"
    )
    @allure.title("DataIsolation_TCAM_Vlan32_BGM_Vlan32用例")
    def test04_caseid_1196146(self):
        case_failed = []

        with allure.step(f"查看vlan32通道的网络"):
            bgm = con_bgm(cmd=f"ping -I eth0.32 172.16.32.31 -c 4")
            with allure.step("vlan32 ping 32.31的网络结果:"):
                allure.attach(bgm)
                if "100% packet loss" not in bgm:
                    allure.attach(f"bgm vlan32通道可以ping通172.16.32.31")
                else:
                    allure.attach(f"bgm vlan32通道不可以ping通172.16.32.31")
                    case_failed.append("bgm vlan32通道不可以ping通172.16.32.31")

            # data = con_bgm(cmd=f"ping -I eth0.5 172.16.32.31 -c 4")
            # with allure.step("vlan5 ping 32.31的网络结果:"):
            #     allure.attach(data)
            #     if "100% packet loss" not in data:
            #         allure.attach(f"bgm vlan5通道可以ping通172.16.32.31")
            #         case_failed.append("bgm vlan5通道可以ping通172.16.32.31")
            #     else:
            #         allure.attach(f"bgm vlan5通道不可以ping通172.16.32.31")

        assert (
            len(case_failed) == 0
        ), f"NetworkChannelDefinition_DataIsolation_TCAM_Vlan32_BGM_Vlan32用例执行失败"

    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1196147?projectId=46"
    )
    @allure.title("DataIsolation_TCAM_BGM_APN4用例校验")
    def test05_caseid_1196147(self):
        data = con_bgm(cmd="ping -I eth0.32 211.95.34.35 -c 4")
        with allure.step("查看数据走APN4的网络结果:"):
            allure.attach(data)
            if "4 packets transmitted, 4 received" in data:
                allure.attach(f"数据走APN4(eth0.32)")
            else:
                allure.attach(f"数据不走APN4(eth0.32)")
        assert "4 packets transmitted, 4 received" in data

    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1196151?projectId=46"
    )
    @allure.title("DataIsolation_TCAM_BGM_APN1用例校验")
    def test06_caseid_1196151(self):
        data = con_bgm(cmd="ping baidu.com -c 4")
        with allure.step("查看数据走APN1的网络结果:"):
            allure.attach(data)
            if "4 packets transmitted, 4 received" in data:
                allure.attach(f"数据走APN1(eth0.5)")
            else:
                allure.attach(f"数据不走APN1(eth0.5)")
        assert "4 packets transmitted, 4 received" in data

    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1196149?projectId=46"
    )
    @allure.title("DataIsolation_TCAM_BGM_APN3用例校验")
    def test07_caseid_1196149(self):
        with allure.step("PC端设置IP 172.16.31.23"):
            os.system(
                f" ip link add link {device} name eth0.31 type vlan id 31;\
                         ip addr add 172.16.31.23/24 dev eth0.31;\
                         ifconfig eth0.31 up;\
                         ifconfig eth0.31 hw ether 02:00:00:00:10:23"
            )
            time.sleep(0.1)
        with allure.step("PC端ping baidu.com查看数据是否走APN3"):
            conn = subprocess.Popen(
                f"ping baidu.com -c 4",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ).communicate()
            with allure.step("查看数据走APN3的网络结果:"):
                allure.attach(conn[0].decode())

                if "已发送 4 个包， 已接收 4 个包" in conn[0].decode():
                    allure.attach(f"测试用例DataIsolation_ACU_TCAM_BGM_APN3执行成功")
                else:
                    allure.attach(f"测试用例DataIsolation_ACU_TCAM_BGM_APN3执行失败")

        os.system(f"vconfig rem eth0.31")
        assert (
            "已发送 4 个包， 已接收 4 个包" in conn[0].decode()
        ), f"测试用例DataIsolation_ACU_TCAM_BGM_APN3执行失败"

    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1196150?projectId=46"
    )
    @allure.title("DataIsolation_TCAM_BGM_APN2用例校验")
    def test08_caseid_1196150(self):
        with allure.step("PC端设置IP 172.16.30.13"):
            os.system(
                f" ip link add link {device} name eth0.30 type vlan id 30;\
                         ip addr add 172.16.30.13/24 dev eth0.30;\
                         ifconfig eth0.30 up;\
                         ifconfig eth0.30 hw ether 02:00:00:00:10:13"
            )
            time.sleep(0.1)
        with allure.step("PC端ping baidu.com查看数据是否走APN2"):
            conn = subprocess.Popen(
                f"ping baidu.com -c 4",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ).communicate()
            with allure.step("查看数据走APN2的网络结果:"):
                allure.attach(conn[0].decode())

                if "已发送 4 个包， 已接收 4 个包" in conn[0].decode():
                    allure.attach(f"测试用例DataIsolation_ACU_TCAM_BGM_APN2执行成功")
                else:
                    allure.attach(f"测试用例DataIsolation_ACU_TCAM_BGM_APN2执行失败")

        os.system(f"vconfig rem eth0.30")
        assert (
            "已发送 4 个包， 已接收 4 个包" in conn[0].decode()
        ), f"测试用例DataIsolation_ACU_TCAM_BGM_APN2执行失败"

    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1196148?projectId=46"
    )
    @allure.title("DataIsolation_PC_Vlan10_BGM_Vlan10用例校验")
    def test09_caseid_1196148(self):
        with allure.step("PC端ping 172.16.5.1"):
            conn = subprocess.Popen(
                f"ping 172.16.5.1 -c 4",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ).communicate()
            with allure.step("查看vlan10的网络结果:"):
                allure.attach(conn[0].decode())
                if "已发送 4 个包， 已接收 4 个包" in conn[0].decode():
                    allure.attach(f"测试用例DataIsolation_PC_Vlan10_BGM_Vlan10执行成功")
                else:
                    allure.attach(f"测试用例DataIsolation_PC_Vlan10_BGM_Vlan10执行失败")

            assert (
                "已发送 4 个包， 已接收 4 个包" in conn[0].decode()
            ), f"测试用例DataIsolation_PC_Vlan10_BGM_Vlan10执行失败"


if __name__ == '__main__':
    pytest.main()
