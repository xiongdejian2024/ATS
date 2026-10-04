#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: test_em.py
@Time: 2022/10/19 12:00
@Author: lei.tao
@Software: PyCharm
@Description: EM测试用例
@Examples:
"""
import json
import os
import sys
import time

import allure
import pytest

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
# from ecu_simulator.driver.ssh_client import SSHClient, SSHFailException
# from ecu_simulator.common.logger import logger
# from test_case.tcam.case_helper.test_base import TestBase
# from ecu_simulator.interface.tcam.tcam_ssh import TCAM_SSH
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *

# def con_tcam(cmd=None):
#     try:
#         conn = SSHClient(hostname="172.16.5.31", port=22, username="root", password="oelinux123")
#         stdout, stderr = conn.exec_cmd(cmd)
#         return stdout
#     except SSHFailException as e:
#         print(f'The server connect failed with error {e}')
#         raise SSHFailException
#     finally:
#         conn.close()

@allure.feature("架构基础")
@allure.story("EM")
class Test_EM(TestABCBase):

    def before_class(self, ecu):
        super().before_class(self, ecu)
        global ip
        ip = self.tc_config.get('gateway_ip')
        self.process_list = [
                                "/usr/bin/qrtr-filter",
                                "/usr/bin/port_bridge",
                                "/usr/bin/qrtr-ns",
                                "/usr/bin/inotifywait --exclude /data/vendor/tzstorage -m -e modify -e close_write -e attrib -e create -e delete -e move -r /systemrw /data",
                                "/usr/bin/ssreq_server",
                                "/usr/bin/writeback /run/tmp/systemrw_write_back 60",
                                "/usr/bin/writeback /run/tmp/data_write_back 60",
                                "/usr/bin/qseecomd",
                                "/usr/bin/qseecomd",
                                "/usr/bin/qwesd",
                                "/usr/bin/netmgrd",
                                "/usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only",
                                "/usr/bin/ipacm",
                                "/usr/bin/QCMAP_ConnectionManager",
                                "/oemapp/etc/data/mobileap_cfg.xml d",
                                "/usr/bin/qti",
                                "/oemapp/bin/dlt-daemon -c",
                                "/oemapp/etc/dlt.conf",
                                "/usr/bin/location_hal_daemon",
                                "/usr/bin/scsi_usb_mode",
                                "/usr/bin/adpl",
                                "/usr/bin/atfwd_daemon",
                                "/usr/bin/qmi_shutdown_modem",
                                "/usr/bin/pdmappersvc",
                                "/usr/bin/syslog_manager",
                                "/oemapp/bin/jetlogd",
                                "/oemapp/bin/service_monitor -c ",
                                "/oemapp/etc/bootes/service_monitor.json",
                                "/oemapp/bin/em2",
                                "/usr/bin/tsens_service",
                                "{sh} /bin/busybox.nosuid /bin/sh /oemapp/bin/renice_neu_process.sh",
                                "{sh} /bin/busybox.nosuid /bin/sh /oemapp/bin/traffic_control_vlan.sh",
                                "{sh} /bin/busybox.nosuid /bin/sh /oemapp/bin/traffic_control_vlan.sh",
                                "/usr/bin/diagrebootapp",
                                "/usr/bin/fibo_at",
                                "/usr/bin/power_manager_daemon",
                                "/usr/bin/ipacmdiag",
                                "/usr/bin/ethpwrmgr",
                                "/oemapp/bin/CellNetworkManager",
                                "/oemapp/bin/ptp4l -i eth0 -m -f /oemapp/bin/gptp/automotive-slave.cfg",
                                "/oemapp/bin/phc2sys -s /dev/ptp0 -w -m -S 3 -O 0 --transportSpecific=1",
                                "/oemapp/bin/xcall_service",
                                "/oemapp/bin/prop",
                                "/oemapp/bin/network_manager",
                                "/oemapp/bin/CertificateMgr",
                                "/oemapp/bin/gb32960_service",
                                "/oemapp/bin/v2trouter",
                                "/oemapp/bin/rvc",
                                "/oemapp/bin/ua_server_app",
                                "/oemapp/bin/rtc",
                                "/usr/bin/fibo-call-path",
                                "/usr/sbin/sshd -f /etc/ssh/sshd_config -h /oemdata/ssh_rsa",
                                "/oemapp/bin/gnss_location",
                                "/oemapp/bin/misc",
                                "/oemapp/bin/vehicle_data_mining_engine",
                                "/oemapp/bin/gnss_service",
                                "/oemapp/bin/config_service",
                                "/oemapp/bin/monitor_agent",                                                                                                                                                                                                                                                            
                                "/usr/bin/dnsmasq --conf-file=/etc/data/dnsmasq.conf --dhcp-leasefile=/var/run/data/dnsmasq.leases --addn-hosts=/etc/data/hosts --pid-file=/var/run/data/dnsmasq.pid --interface=bridge0 --except-interface=lo -z --dhcp-range=bridge0,192.168.225.20,192.168.225.60,255.255.255.0,43200",
                                "/oemapp/bin/remote_log",
                                "/usr/bin/loc_launcher",
                                "RpcService mode=260",
                                "ParaService mode=260",
                                "TeeMgrService mode=260",
                                "RouteCtrlService mode=260",
                                "Uds mode=260",
                                "NeuDiag mode=260",
                                "Xcall mode=260",
                                "StorageService mode=260",
                                "RMS mode=260"
                                ]


    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        self.io.tcam_kl15_up()
        super().after_class(self, ecu)

    @pytest.mark.smoke
    @allure.title("EM normal startup test")
    def test_caseid_101610(self):
        data = self.ssh.tcam_ssh.exec("ps aux | grep /oemapp/bin/em2 | grep -v grep", ip)
        print(data)
        if data != "":
            allure.attach("进程em2启动成功")
        else:
            allure.attach("进程em2启动失败")

        assert data != "",f"进程em2启动失败"

    @pytest.mark.smoke
    @allure.title("EM startup sequence test")
    def test_caseid_101608(self):
        info = self.ssh.tcam_ssh.exec(f"cat /oemapp/etc/app_info.json", ip)
        pid_list = []
        data = json.loads(info)
        logger.info(f"app_info中的内容:{data}")
        for x in data:
            if x.get("session") == "default":
                data = x.get("apps")
                for i in range(len(data)):
                    pid = self.ssh.tcam_ssh.exec(f"ps aux | grep /oemapp/bin/{data[i]['name']} " + "| grep -v grep", ip).split(" ")[0]
                    with allure.step(f"查看进程{data[i]['name']}的pid"):
                        if pid:
                            allure.attach(f"进程{data[i]['name']}的pid为{pid}")
                            pid_list.append(pid)
                        else:
                            allure.attach(f"进程{data[i]['name']}没有启动")
        logger.info(f"app_info中的需要check的进程列表:{pid_list}")

        with allure.step(f"查看各进程pid是否配置越靠前, PID越小:"):
            for j in range(len(pid_list)-1):
                if pid_list[j] < pid_list[j + 1]:
                    allure.attach(f"app_info.json配置中{pid_list[j]}的PID小于{pid_list[j + 1]}的PID")

                assert int(pid_list[j]) < int(pid_list[j+1]), f"app_info.json中配置越靠前,PID不是越小"
            allure.attach("app_info.json中配置越靠前,PID越小")

    @pytest.mark.sanity
    @allure.title("EM_SM monitoring test_autostart")
    def test_caseid_101609(self):
        dict = {}
        info = self.ssh.tcam_ssh.exec(f"cat /oemapp/etc/app_info.json", ip)
        data = json.loads(info)
        logger.info(f"app_info中的内容:{data}")
        for x in data:
            if x.get("session") == "default":
                data = x.get("apps")
                for i in range(len(data)):
                    pid = self.ssh.tcam_ssh.exec(f"ps aux | grep {data[i]['name']} " + "| grep -v grep", ip).strip().split(" ")[0]
                    #pid = self.ssh.tcam_ssh.exec(f"ps aux | grep /oemapp/bin/{data[i]['name']} " + "| grep -v grep", ip).split(" ")[0]
                    logger.info(f"pid:{pid}")
                    with allure.step(f"查看进程{data[i]['name']}的pid"):
                        if pid:
                            allure.attach(f"进程{data[i]['name']}的pid为{pid}")
                            dict[pid] = data[i]['name']
                        else:
                            allure.attach(f"进程{data[i]['name']}没有启动")
        logger.info(f"app_info中的需要测试重新拉起的进程列表:{dict}")

        with allure.step(f"判断进程异常挂掉后，EM能否自动拉起进程"):
            for key, value in dict.items():
                try:
                    with allure.step(f"查看进程{value}是否kill"):
                        outmsg = self.ssh.tcam_ssh.exec(f"kill -9 {key}", ip)
                        assert outmsg == "", f"kill -9 {key} 指令异常报错"
                    time.sleep(10)
                    with allure.step(f"查看进程{value}是否被重新拉起"):
                        #autostart_pid = self.ssh.tcam_ssh.exec(f"ps aux | grep /oemapp/bin/{value} " + "| grep -v grep", ip).strip().split(" ")[0]
                        autostart_pid = self.ssh.tcam_ssh.exec(f"ps aux | grep {value} " + "| grep -v grep", ip).strip().split(" ")[0]
                        logger.info(f"进程kill前的pid：{key}，重新拉起后的pid:{autostart_pid}")
                        assert autostart_pid != "" and autostart_pid != key, f"进程{value}没有被重新拉起"
                except Exception as e:
                    logger.error(f"进程{value}自动拉起测试失败: {e}")
                    continue

    @pytest.mark.sanity
    @allure.title("EM startup broadcast")
    def test_caseid_1899271(self):
        with allure.step("TCAM上下电"):
            self.io.tcam_power_off()
            time.sleep(30)
            self.io.tcam_power_on()
            time.sleep(240)

        with allure.step("进入到TCAM查看启动后的广播日志: startup mode: default"):
            data = self.ssh.tcam_ssh.exec("/oemapp/bin/zstdcat /mnt/sdcard/log/jetlog_messages| grep 'startup mode: default'", ip)
            logger.info(f"启动后广播日志为: {data}")
            if "startup mode: default" in data:
                allure.attach("日志中可以搜到startup mode: default 广播")
            else:
                allure.attach("日志中搜不到startup mode: default 广播")
        assert "startup mode: default" in data, f"日志中搜不到startup mode: default 广播"

    @pytest.mark.sanity
    @allure.title("EM Suspend broadcast")
    def test_caseid_1912497(self):
        """
        EM2联调模块进程检查: https://wiki.jiduauto.com/pages/viewpage.action?pageId=310997218
        进程"diagd_iautosar", "gnss_location", "ptp4l", "phc2sys"不需要集成
        进程"jetlogd"暂不处理
        """
        failed = []
        with allure.step("TCAM上电后, 一段时间断开KL15"):
            self.mix.network_sleep()
            self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_CONNCANFD)

        with allure.step("进入到TCAM查看日志(休眠广播): Suspend"):
            data = self.ssh.tcam_ssh.exec("/oemapp/bin/zstdcat /mnt/sdcard/log/jetlog_messages| grep 'change mode to'", ip)
            logger.info(f"休眠后日志广播为: {data}")
            if "change mode to: suspend" in data:
                allure.attach("日志中可以搜到休眠后change mode to: suspend 广播")
            else:
                allure.attach("日志中搜不到休眠后change mode to: suspend 广播")
                failed.append("日志中搜不到休眠后change mode to: suspend 广播")
        with allure.step("查询业务模块的收到休眠广播"):
            mode = ["CertificateMgr", "config_service", "rtc", "misc", "v2trouter", "prop", "gb32960_service", 
                    "xcall_service", "rvc", "gnss_service", "ua_server_app","vehicle_data_mining_engine"]
            for i in mode:
                with allure.step(f"查询业务模块{i}收到的休眠广播"):
                    data1 = self.ssh.tcam_ssh.exec(f"/oemapp/bin/zstdcat /mnt/sdcard/log/jetlog_messages| grep 'Suspend res(1: 0k)' | grep {i}", ip)
                    logger.info(f"休眠后日志广播为: {data1}")
                    if data1:
                        allure.attach(f"日志中可以搜到休眠后业务模块{i}的广播")
                    else:
                        allure.attach(f"日志中搜不到休眠后业务模块{i}的广播")
                        failed.append(f"日志中搜不到休眠后业务模块{i}的广播")
        assert len(failed) == 0

    @pytest.mark.sanity
    @allure.title("EM Resume broadcast")
    def test_caseid_1912554(self):
        """
        EM2联调模块进程检查: https://wiki.jiduauto.com/pages/viewpage.action?pageId=310997218
        进程"diagd_iautosar", "gnss_location", "ptp4l", "phc2sys"不需要集成
        进程"jetlogd"暂不处理
        """
        failed = []
        with allure.step("连接KL15唤醒"):
            # os.system("usbrelay _8=0")
            self.mix.network_sleep()
            self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_CONNCANFD)

            # time.sleep(5)

        with allure.step("进入到TCAM查看唤醒后的广播日志: Resume"):
            data = self.ssh.tcam_ssh.exec("/oemapp/bin/zstdcat /mnt/sdcard/log/jetlog_messages| grep 'change mode to'", ip)
            logger.info(f"唤醒后日志广播为: {data}")
            if "change mode to: default" in data:
                allure.attach("日志中可以搜到唤醒后change mode to: default 广播")
            else:
                allure.attach("日志中搜不到唤醒后change mode to: default 广播")
                failed.append("日志中搜不到唤醒后change mode to: default 广播")
        with allure.step("查询业务模块的收到唤醒广播"):
            mode = ["CertificateMgr", "config_service", "rtc", "misc", "v2trouter", "prop", "gb32960_service", 
                    "xcall_service", "rvc", "gnss_service", "ua_server_app","vehicle_data_mining_engine"]
            for i in mode:
                with allure.step(f"查询业务模块{i}收到的唤醒广播"):
                    data1 = self.ssh.tcam_ssh.exec(f"/oemapp/bin/zstdcat /mnt/sdcard/log/jetlog_messages| grep 'Resume res(1: 0k)' | grep {i}", ip)
                    logger.info(f"唤醒后日志广播为: {data1}")
                    if data1:
                        allure.attach(f"日志中可以搜到唤醒后业务模块{i}的广播")
                    else:
                        allure.attach(f"日志中搜不到唤醒后业务模块{i}的广播")
                        failed.append(f"日志中搜不到唤醒后业务模块{i}的广播")
        assert len(failed) == 0

    @pytest.mark.sanity
    @allure.title("TCAM正常运行查看TCAM进程运行情况")
    def test_caseid_1986123(self):
        self.mix.check_tcam_process_status(proecess_list=self.process_list, cmd="ps -ef|grep -E 'usr|app|oem|mode=260'")

    @pytest.mark.full
    @allure.title("TCAM重启后查看TCAM进程能否正常运行")
    def test_caseid_1986124(self):
        self.io.tcam_power_off()
        time.sleep(30)
        self.io.tcam_power_on()
        time.sleep(240)
        self.mix.check_tcam_process_status(proecess_list=self.process_list, cmd="ps -ef|grep -E 'usr|app|oem|mode=260'")


if __name__ == '__main__':
    pytest.main()

# pytest basetech/EM/test_em.py