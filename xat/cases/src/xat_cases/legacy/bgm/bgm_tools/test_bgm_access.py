# -*- coding: utf-8 -*-
"""
@File        : test_flash_bgm
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/3/1 13:34
@Description :

"""
import time
import pytest
import allure
import sys, os
import json

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

work_path_2 = os.path.join(os.getcwd().split("sat")[0], 'sat', 'ecu_simulator', 'interface')
sys.path.append(work_path_2)


sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from xat_cases.legacy.bgm.case_helper.test_base import TestBase
import pytest
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_ecu.legacy.sdk.get_obd_ip import get_announcement_ip
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_cases.legacy.bgm.case_helper.diag_case_helper.DiagTestBase import *

# @pytest.mark.repeat(10)
class Test_Check_Env(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)

        self.sd_tester = Sd_Tester(**self.tc_config)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.diagnostic_client_sim_start()
        self.sd_tester.tester_present()

        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文

        self.sd_test_tb_config = self.tc_config
        self.bgm_cmd = BGM_SSH()
        self.b_cli = DiagTestBase(self.ipdu, self.busapp,self.tc_config)
        sleep(1)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # Code Location

    def after_each_func(self, ecu):
        # Code Location
        super().after_each_func(ecu)

    def after_class(self, ecu):
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        # Code Location
        self.sd_tester.stop_tester_present()
        super().after_class(self, ecu)

    def reboot_bgm(self):
        self.sd_tester.send_data([0x11, 0x81])
        # self.bgm_power_off_and_on()
    
    def stop_test_to_reserve_even(self):
        logger.info("停止测试，保留环境,停止test present 打印")
        self.sd_tester.stop_tester_present()
        sleep(3*24*3600)
    
    # @pytest.mark.access_2
    # def test_debug(self):
    #     self.sd_tester.diagnostic_session_check()
    #     sleep(1)
    #     self.sd_tester.send_data([0x10, 0x01])
    #     sleep(1)
    #     self.sd_tester.diagnostic_session_check()
    #     sleep(10)
    
    @pytest.mark.access
    def test_announce_msg_time_caseid_0000001(self):
        self.reboot_bgm()
        bgm_power_reset_time = time.time()
        self.b_cli.catch_announcenent()
        time_receive_anno_msg = time.time()
        time_interval = float(time_receive_anno_msg) - float(bgm_power_reset_time)
        logger.info("在{}内获取车辆公告".format(time_interval))
        if time_interval < 15 :
            assert True
        else:
            logger.error("15s 内未获取车辆公告，测试停止，保留环境")
            self.stop_test_to_reserve_even()
        sleep(15)
            

    @pytest.mark.access
    def test_time_sync_caseid_0000002(self):
        #获取时间同步时间
        logger.info("self.bl_ver:{}".format(self.bl_ver))
        if self.bl_ver == "v_1_3_0":
            cmd = r"ls -1 /log/jetlog_messages* | sort -t'_' -k2 -n | tail -2 | xargs -I{} /app/bin/zstdcat {} | sed -n 's/.*,\([0-9]\+\),-;PM: hibernation: hibernation exit.*/\1/p' | tail -n 1"
            time_start = self.bgm_cmd.type_commands(cmd)
            
            
            
            cmd = r"ls -1 /log/jetlog_messages* | sort -t'_' -k2 -n | tail -2 | xargs -I{} /app/bin/zstdcat {} | sed -n 's/.*,\([0-9]\+\),-;VehicleTime.*/\1/p' | tail -n 1"
            time_sync = self.bgm_cmd.type_commands(cmd)
            
        else:
            cmd = r"/app/bin/zstdcat /log/jetlog_messages | sed -n 's/.*,\([0-9]\+\),-;PM: hibernation: hibernation exit.*/\1/p'"
            time_start = self.bgm_cmd.type_commands(cmd)
            cmd = r"/app/bin/zstdcat /log/jetlog_messages | sed -n 's/.*,\([0-9]\+\),-;VehicleTime.*/\1/p'"
            time_sync = self.bgm_cmd.type_commands(cmd)

        if "\n" in time_start:
                time_start = time_start.split("\n")
                time_start = time_start[-1]
        if "\n" in time_sync:
                time_sync = time_sync.split("\n")
                time_sync = time_sync[-1]
        logger.info("time_start:{}".format(time_start))
        logger.info("time_sync:{}".format(time_sync))
        
        time_interval = (int(time_sync) - int(time_start))/1000000
        logger.info("从启动的到时间同步的时间间隔是 {}".format(time_interval))
        if int(time_interval)>10:
            logger.error("从启动的到时间同步的时间间隔是大于10s")
            self.stop_test_to_reserve_even()
            assert False
        else:
            assert True
        sleep(2)

    @pytest.mark.access
    def test_sys_resumed_caseid_0000003(self):
        cmd = "cat /sys/power/sys_resumed"
        data = self.bgm_cmd.type_commands(cmd)
        logger.info("sys_resumed是 {}".format(data))
        if int(data) == 0:
            logger.info("cat /sys/power/sys_resumed 为0")
            self.stop_test_to_reserve_even()
            assert False
        else:
            assert True
        sleep(2)


    @pytest.mark.access
    def test_get_coredump_caseid_0000004(self):
        #4.出现core.sys_to_s2d_then.xxx或者core.exec_s2d.sh.xxx的coredump；
        cmd = r"ls /log/coredump"
        data = self.bgm_cmd.type_commands(cmd)
        logger.info("BGM coredump 文件是 {}".format(data))
        if data.find("core.sys_to_s2d_then") != -1 or data.find("core.exec_s2d") != -1:
            logger.info("出现sys_to_s2d 或者 exec_s2d.sh coredump 文件")
            self.stop_test_to_reserve_even()
            assert False
        else:
            assert True
        sleep(2)


    @pytest.mark.access
    def test_read_ReadSysfsResume_caseid_0000005(self):
        # 5.log搜索“ReadSysfsResumedTime”，时间大于6000；
        if self.bl_ver == "v_1_3_0":
            cmd = r"ls -1 /log/jetlog_messages* | sort -t'_' -k2 -n | tail -2 | xargs -I{} /app/bin/zstdcat {} | sed -n 's/.*ReadSysfsResumedTime : \([0-9]\+\).*/\1/p' | tail -n 1"
        else:
            cmd = r"/app/bin/zstdcat /log/jetlog_messages | sed -n 's/.*ReadSysfsResumedTime : \([0-9]\+\).*/\1/p'"
        data = self.bgm_cmd.type_commands(cmd)
        if "\n" in data:
            data = data.split("\n")
            data = data[-1]
        logger.info("ReadSysfsResumedTime 是 {}".format(data))
        if int(data)>6000:
            logger.error("ReadSysfsResumedTime，时间大于6000")
            self.stop_test_to_reserve_even()
            assert False
        else:
            assert True
        sleep(2)
    
    @pytest.mark.access
    def test_read_S2SServiceResume_caseid_0000006(self):
        #6.log搜索“S2SService Resume time”，如果时间大于2000；
        if self.bl_ver == "v_1_3_0":
            cmd = r"ls -1 /log/jetlog_messages* | sort -t'_' -k2 -n | tail -2 | xargs -I{} /app/bin/zstdcat {} | sed -n 's/.*S2SService Resume time:\([0-9]\+\).*/\1/p' | tail -n 1"
        else:
            cmd = r"/app/bin/zstdcat /log/jetlog_messages | sed -n 's/.*S2SService Resume time:\([0-9]\+\).*/\1/p'"
        data = self.bgm_cmd.type_commands(cmd)
        if "\n" in data:
            data = data.split("\n")
            data = data[-1]
        logger.info("S2SService Resume time 是 {}".format(data))
        if int(data)>2000:
            logger.error("S2SService Resume time 时间大于2000")
            self.stop_test_to_reserve_even()
            assert False
        else:
            assert True
        sleep(2)
        
    
    @pytest.mark.access
    def test_read_syslogd_phy_monitor_caseid_0000007(self):
        #7. syslogd和phy_monitor
            # cmd: top -b -n 1 | grep syslogd 返回空
            # cmd: top -b -n 1 | grep phy_monitor 返回空

        # cmd_1 = r"top -b -n 1 | grep syslogd"
        # data = self.bgm_cmd.type_commands(cmd_1)
        # logger.info("top -b -n 1 | grep syslogd 返回值是 {}".format(data))
        # if len(data)<2:
        #     logger.error("top -b -n 1 | grep syslogd 返回值是空")
        #     self.stop_test_to_reserve_even()
        #     assert False
        # else:
        #     assert True
            
        cmd_2 = r"top -b -n 1 | grep phy_monitor"
        data = self.bgm_cmd.type_commands(cmd_2)
        logger.info("top -b -n 1 | grep phy_monitor 返回值是 {}".format(data))
        if len(data)<2:
            logger.error("top -b -n 1 | grep phy_monitor 返回值是空")
            self.stop_test_to_reserve_even()
            assert False
        else:
            assert True
            
        sleep(2)
        

    @pytest.mark.access
    def test_read_valnip_caseid_0000008(self):
        #9. ifconfig
            # cmd: ifconfig eth0.5 | grep inet | grep -v inet6 | awk '{print $2}' 不为 172.16.5.1
            # cmd: ifconfig eth0.9 | grep inet | grep -v inet6 | awk '{print $2}' 不为 172.16.9.1
            # cmd: ifconfig eth0.10 | grep inet | grep -v inet6 | awk '{print $2}' 不为 169.254.19.1
            # cmd: ifconfig eth0.11 | grep inet | grep -v inet6 | awk '{print $2}' 不为 172.16.11.1
            # cmd: ifconfig eth0.32 | grep inet | grep -v inet6 | awk '{print $2}' 不为 172.16.32.1

        cmd_1 = r"ifconfig eth0.5 | grep inet | grep -v inet6 | awk '{print $2}'"
        cmd_2 = r"ifconfig eth0.9 | grep inet | grep -v inet6 | awk '{print $2}'"
        cmd_3 = r"ifconfig eth0.10 | grep inet | grep -v inet6 | awk '{print $2}'"
        cmd_4 = r"ifconfig eth0.11 | grep inet | grep -v inet6 | awk '{print $2}'"
        cmd_5 = r"ifconfig eth0.32 | grep inet | grep -v inet6 | awk '{print $2}'"
        
        data_1 = self.bgm_cmd.type_commands(cmd_1)
        logger.info("获取Vlan 5 网卡IP返回值是 {}".format(data_1))
        sleep(1)
        
        data_2 = self.bgm_cmd.type_commands(cmd_2)
        logger.info("获取Vlan 9 网卡IP返回值是 {}".format(data_2))
        sleep(1)
        
        data_3 = self.bgm_cmd.type_commands(cmd_3)
        logger.info("获取Vlan 10 网卡IP返回值是 {}".format(data_3))
        sleep(1)
        
        data_4 = self.bgm_cmd.type_commands(cmd_4)
        logger.info("获取Vlan 11 网卡IP返回值是 {}".format(data_4))
        sleep(1)
        
        data_5 = self.bgm_cmd.type_commands(cmd_5)
        logger.info("获取Vlan 32 网卡IP返回值是 {}".format(data_5))
        sleep(1)
        
        if data_1 != "172.16.5.1" or data_2 != "172.16.9.1" or data_3 != "169.254.19.1" or data_4 != "172.16.11.1" or data_5 != "172.16.32.1":
            logger.error("有Vlan的IP地址不正确")
            self.stop_test_to_reserve_even()
            assert False
        else:
            assert True     
        sleep(2)
        
    
    @pytest.mark.access
    def test_read_lsblk_caseid_00000010(self):
        """
        10. lsblk
            cmd: lsblk | grep p6 | awk '{print $7}' 不为 /data
            cmd: lsblk | grep p7 | awk '{print $7}' 不为 /update
            cmd: lsblk | grep p8 | awk '{print $7}' 不为 /log
            A面单独检查：
            cmd: lsblk | grep p2 | awk '{print $7}' 不为 /
            cmd: lsblk | grep p4 | awk '{print $7}' 不为 /app
            B面单独检查：
            cmd: lsblk | grep p3 | awk '{print $7}' 不为 /
            cmd: lsblk | grep p5 | awk '{print $7}' 不为 /app
        """

        cmd_1 = r"lsblk | grep p6 | awk '{print $7}'"
        data_1 = self.bgm_cmd.type_commands(cmd_1)
        print("----------------->1")
        logger.info("{} 返回值是 {}".format(cmd_1,data_1))
        print("----------------->2")
        sleep(2)
        if str.strip(data_1) != r"/data":
            logger.error("{} 返回值不为 /data".format(cmd_1))
            self.stop_test_to_reserve_even()
            assert False
        else:
            assert True
            
        cmd_2 = r"lsblk | grep p7 | awk '{print $7}'"
        data_2 = self.bgm_cmd.type_commands(cmd_2)
        logger.info("{} 返回值是 {}".format(cmd_2,data_2))
        if str.strip(data_2) != r"/update":
            logger.error("{} 返回值不为 /update".format(cmd_2))
            self.stop_test_to_reserve_even()
            assert False
        else:
            assert True
        
        cmd_3 = r"lsblk | grep p8 | awk '{print $7}'"
        data_3 = self.bgm_cmd.type_commands(cmd_3)
        logger.info("{} 返回值是 {}".format(cmd_3,data_3))
        if str.strip(data_3) != r"/log":
            logger.error("lsblk | grep p8 | awk '{print $7}' 不为 /log")
            self.stop_test_to_reserve_even()
            assert False
        else:
            assert True
        
        cmd_4 = r"/app/bin/swdl -nr 8"
        data_4 = self.bgm_cmd.type_commands(cmd_4)

        if str.strip(data_4) == "A":
            cmd_5 = r"lsblk | grep p2 | awk '{print $7}'"
            cmd_6 = r"lsblk | grep p4 | awk '{print $7}'"
        elif str.strip(data_4) == "B":
            cmd_5 = r"lsblk | grep p3 | awk '{print $7}'"
            cmd_6 = r"lsblk | grep p5 | awk '{print $7}'"
        else:
            logger.error("'/app/bin/swdl -nr 8'返回值错误，没有读取A/B面信息")
            assert False
            
        data_5 = self.bgm_cmd.type_commands(cmd_5)
        logger.info("{} 返回值是 {}".format(cmd_5,data_5))
        if str.strip(data_5) != r"/":
            logger.error("{} 返回值不为 /".format(cmd_5))
            self.stop_test_to_reserve_even()
            assert False
        else:
            assert True
        
        data_6 = self.bgm_cmd.type_commands(cmd_6)
        logger.info("{} 返回值是 {}".format(cmd_6,data_6))
        if str.strip(data_6) != r"/app":
            logger.error("{} 返回值不为 /app".format(cmd_6))
            self.stop_test_to_reserve_even()
            assert False
        else:
            assert True
        sleep(2)
        

if __name__ == "__main__":
    from datetime import datetime
    print(datetime.now())