# -*- coding: utf-8 -*-
import os
import sys
import time
import typing
import pytest
import allure
import requests
import subprocess
import netifaces
from groot2.cloud.biz.digital_key.manager import DigitalKeyManager
from xat_ecu.legacy.driver.ssh_client import SSHClient
from xat_ecu.api.interfaces.dp1.tsp import Tsp

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

work_path_2 = os.path.join(os.getcwd().split("sat")[0], 'sat', 'ecu_simulator', 'interface')
sys.path.append(work_path_2)

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import S2sBaseClass
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey
from xat_ecu.legacy.common.logger import logger
from xat_ecu.api.common.common import *
from xat_ecu.api.abc_interface import *
from xat_cases.legacy.basetech.case_helper.diag_case_helper.DiagTestBase import *
from xat_ecu.legacy.sdk.sdk_tools import exec_shell
from xat_ecu.legacy.interface.bgm.bgm_ssh import partner_process_check
from tools.feishu.feishu_notice import FeishuAlert
from tools.feishu.feishu_notice import AlertInfo
from xat_ecu.legacy.interface.feishu.feishu_api import feishu_api
from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass_abc import *
from xat_ecu.api.interfaces.dp1.sdtest import SdTest
from xat_ecu.api.interfaces.dp1.ssh import Ssh


class TestBenchEnv(TestBase):

    def before_class(self, ecu) -> None:
        super().before_class(self, ecu)
        self.alert_info = {}
        self.tsp = Tsp(**self.tc_config)
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        self.config = self.parser_ecu(self, ecu)
        logger.info(f"获取到的配置文件是：{self.config}")

    def before_each_func(self, ecu) -> None:
        super().before_each_func(ecu)

    def after_each_func(self, ecu) -> None:
        time.sleep(1)
        super().after_each_func(ecu)

    def after_class(self, ecu) -> None:
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文

        output = exec_shell(f"pwd").get("output", "")
        alarm_description = AlertInfo(self.config.get("wifi_localhost"), self.alert_info)
        alarm = FeishuAlert(alarm_description)
        if str(output).startswith("/root/autotools/bench_check"):
            alarm.post_to_robot()
        else:
            alarm.post_to_robot(True)
        super().after_class(self, ecu)

    def parser_ecu(self, ecu) -> typing.Dict[str, typing.Any]:
        eths = []
        can_channels = []
        can_devices = set()
        lin_channels = []
        lin_devices = set()
        fr_channels = []
        fr_devices = set()
        config: dict = ecu.tc_config
        bus = config.get("bus")
        eths.append([bus.get("eth_obd"), config.get("eth_obd")])
        if bus.get("eth_vlan5"):
            eths.append([bus.get("eth_vlan5"), "172.16.5.21"])
        for bus_name, devices in bus.items():
            if "can" in bus_name:
                can_channels.append(bus_name)
                can_devices.add(devices[0])
            elif "cem" in bus_name:
                lin_channels.append(bus_name)
                lin_devices.add(devices[0])
            elif "fr" in bus_name:
                fr_channels.append(bus_name)
                fr_devices.add(devices[0])
        for key, value in ecu.domain.__dict__.items():
            if value is not None:
                domain = key
                dut_ecu = value.get("type")
                break
        domain = domain if domain in ["four_domain", "two_domain", "single_tcam", "single_bgm"] else "nonsupport"
        return {
            "domain": domain,
            "dut_ecu": dut_ecu,
            "eths": eths,
            "wifi_localhost": config.get("wifi_localhost"),
            "tel": config.get("tel"),
            "can_channels": can_channels,
            "can_devices": can_devices,
            "lin_channels": lin_channels,
            "lin_devices": lin_devices,
            "fr_channels": fr_channels,
            "fr_devices": fr_devices,
            "vid": config.get("vid"),
            "vin": config.get("vin"),
            "bncm_key": config.get("BNCM_KEY"),
            "serials": config.get("serial")
        }

    def ping_31(self, ip: str) -> bool:
        output = exec_shell(f"ping {ip} -c 1").get("output", "")
        return True if "已接收 1 个包" in output or "1 received" in output else False

    def check_disk_health(self) -> bool:
        perft = 0
        disk_device_proc = subprocess.Popen("df -h | awk '{print $5, $6}'", shell=True, stdout=subprocess.PIPE)
        disk_device_out, _ = disk_device_proc.communicate()
        for info in disk_device_out.decode().split("\n"):
            if info:
                if info.split(" ")[1] == "/":
                    perft = int(info.split(" ")[0].split("%")[0])
        return perft
        # result = subprocess.run(['df', '-h'], stdout=subprocess.PIPE)
        # logger.info("当前磁盘使用情况：")
        # logger.info(result.stdout.decode())
        #
        # disk_device_cmd = "lsblk -o NAME | grep -E 'nvme[0-9]' | head -n 1"
        # disk_device_proc = subprocess.Popen(disk_device_cmd, shell=True, stdout=subprocess.PIPE)
        # disk_device_out, _ = disk_device_proc.communicate()
        # disk_device = disk_device_out.decode("utf-8").strip()
        # disk_device = f"/dev/{disk_device}"
        # logger.info(f"当前检测磁盘为：{disk_device}")
        # check_smartmontools_cmd = "dpkg -l | grep smartmontools"
        # proc = subprocess.Popen(check_smartmontools_cmd, shell=True, stdout=subprocess.PIPE)
        # out, _ = proc.communicate()
        # if b"smartmontools" not in out:
        #     logger.info("未安装磁盘检查工具，现在开始安装 smartmontools")
        #     install_smartmontools_cmd = "apt-get install smartmontools -y"
        #     subprocess.run(install_smartmontools_cmd, shell=True)
        #
        # command = f"smartctl -H {disk_device}"
        # result = subprocess.run(command, shell=True, capture_output=True, text=True)
        # if result.returncode == 0:
        #     output = result.stdout
        #     logger.info(output.strip())
        #     return True if "PASSED" in output else False
        # else:
        #     logger.error(result.stderr)
        #     return False

    def check_mem_health(self) -> bool:
        check_memtester_cmd = "which memtester"
        proc = subprocess.Popen(check_memtester_cmd, shell=True, stdout=subprocess.PIPE)
        out, _ = proc.communicate()
        if not out.strip():
            logger.info("未安装内存检查工具，现在开始安装 memtester")
            install_memtester_cmd = "apt-get install memtester -y"
            subprocess.run(install_memtester_cmd, shell=True)

        command = "memtester 100M 1"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(result.stdout)
            return True
        else:
            logger.error(result.stderr)
            return False

    def check_cpu_health(self) -> bool:
        check_mpstat_cmd = "which mpstat"
        proc = subprocess.Popen(check_mpstat_cmd, shell=True, stdout=subprocess.PIPE)
        out, _ = proc.communicate()
        if not out.strip():
            logger.info("未安装CPU检查工具，现在开始安装 mpstat")
            install_mpstat_cmd = "apt-get install sysstat -y"
            subprocess.run(install_mpstat_cmd, shell=True)

        command = "mpstat"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(result.stdout)
            return True
        else:
            logger.error(result.stderr)
            return False

    @allure.title("检查磁盘健康")
    def test_disk(self) -> None:
        """
        检测磁盘是否健康，若磁盘不健康可能会导致运行慢，数据丢失等问题
        """
        result = self.check_disk_health()
        if result < 95:
            with allure.step("磁盘状态健康"):
                logger.info("磁盘状态健康")
        else:
            with allure.step("磁盘状态不健康"):
                logger.error("磁盘状态不健康")
            self.alert_info['磁盘检测'] = "PASS" if result < 95 else f"磁盘状态不健康，占用空间：{result}%"
        assert result < 95, "磁盘状态不健康"

    @allure.title("检查内存健康性")
    def test_mem(self) -> None:
        """
        检测内存是否健康，若内存不健康可能会导致运行慢，卡死等问题
        """
        result = self.check_mem_health()
        if result:
            with allure.step("内存状态健康"):
                logger.info("内存状态健康")
            with allure.step("内存状态不健康"):
                logger.error("内存状态不健康")
        self.alert_info['内存'] = "PASS" if result else "内存状态不健康"
        assert result, "内存状态不健康"

    @allure.title("检查CPU健康性")
    def test_cpu(self) -> None:
        """
        检测CPU是否健康，若CPU不健康可能会导致运行慢，卡死等问题
        """
        result = self.check_cpu_health()
        if result:
            with allure.step("CPU状态健康"):
                logger.info("CPU状态健康")
        else:
            with allure.step("CPU状态不健康"):
                logger.error("CPU状态不健康")
        self.alert_info['CPU'] = "PASS" if result else "CPU状态不健康"
        assert result, "CPU状态不健康"

    @allure.title("检查固定USB串口是否配置")
    def test_fixed_usb_serial(self) -> None:
        """
        检查USB串口是否固定配置，以下是对应关系
        32路继电器  USB_DO
        8路采集器   USB_DI
        Pwm        USB_PWM
        Bgm        USB_BGM
        Tcam       USB_TCAM
        若USB串口未配置会导致使用对应USB功能时所操纵的并不是该USB

        若串口配置但未启用请尝试执行如下命令后重启nuc：
        sudo udevadm control --reload-rules
        sudo service udev restart
        """
        if self.config.get("domain") == "single_tcam":
            pytest.skip("当前是tcam单域台架环境，跳过检查")
        serials = self.config.get("serials")
        if serials is None:
            pytest.skip("serials 为空，跳过检查")
        err_list = []
        usb_configs = {
            "USB_DO": "32路继电器",
            "USB_DI": "8路采集器",
            "USB_PWM": "Pwm",
            "USB_BGM": "Bgm",
            "USB_TCAM": "Tcam"
        }
        output = exec_shell("cat /etc/udev/rules.d/99-usb-serial.rules")  # 查看串口固定配置文件
        active_usb = exec_shell("ls /dev/").get("output").split("\n")
        if output.get("output"):
            for serial in serials:
                devices = usb_configs.get(serial)
                if serial in output.get("output"):  # 查看是否设置了对应串口
                    if serial in active_usb:  # 查看对应串口状态是否正常
                        with allure.step(f"{devices} 已固定为 {serial} 并启用"):
                            logger.info(f"{devices} 已固定为 {serial} 并启用")
                    else:
                        with allure.step(f"{devices} 已固定为 {serial} 但并未启用"):
                            logger.error(f"{devices} 已固定为 {serial} 但并未启用")
                            err_list.append(f"{devices} 已固定为 {serial} 但并未启用")
                else:
                    with allure.step(f"{devices} 未固定USB配置"):
                        logger.error(f"{devices} 未固定USB配置")
                        err_list.append(f"{devices} 未固定USB配置")
        else:
            result = output.get("error")  # 查看串口设置文件，一般可能是还未配置导致无法查看
            with allure.step(result):
                logger.error(result)
                err_list.append(result)
        error_info = "\n".join(err_list)
        self.alert_info['固定USB串口'] = error_info if error_info else "PASS"
        assert not error_info, error_info

    @allure.title("检查网卡配置")
    def test_nic_config(self) -> None:
        """
        检查网卡是否配置，未配置网卡时请根据手顺配置对应网卡
        检查网卡是否被激活, 当网卡没有被激活时使用 sudo ip link set 网卡名 up ，如sudo ip link set enp114s0 up
        """
        if self.config.get("domain") != "two_domain":
            pytest.skip("当前是非双域台架环境，跳过检查")
        err_list = []
        for infos in self.config.get("eths"):
            eth_name, eth_ip = infos
            output = exec_shell(f"ip addr show {eth_name}")
            eth_info = output.get("output")
            if eth_info:
                if eth_ip in eth_info:
                    result = f"已配置{eth_name} {eth_ip}网卡"
                    with allure.step(result):
                        logger.info(result)
                        logger.info(f"网卡配置信息：{eth_info}")
                else:
                    result = f"未配置{eth_name} {eth_ip}网卡或未被激活"
                    with allure.step(result):
                        logger.error(result)
                        err_list.append(result)
            else:
                result = f"未配置{eth_name} 网卡，请检查 /etc/netplan/01-network-manager-all.yaml是否配置或bench_config 中yaml文件网卡名称是否是您期望的网卡名"
                with allure.step(result):
                    err_list.append(result)
                    logger.error(result)
                    continue

            output = exec_shell(f"ip link show {eth_name}")
            eth_info = output.get("output")
            if eth_info:
                if "state UP" in eth_info:
                    result = f"{eth_name}网卡当前为激活状态"
                    with allure.step(result):
                        logger.info(f"网卡激活信息：{eth_info}")
                else:
                    result = f"{eth_name}网卡当前为未激活状态"
                    with allure.step(result):
                        logger.error(result)
                        err_list.append(result)
            else:
                result = output.get("error")
                with allure.step(result):
                    err_list.append(result)
                    logger.error(result)
        error_info = "\n".join(err_list)
        self.alert_info['网卡配置'] = error_info if error_info else "PASS"
        assert not error_info, error_info

    def get_local_network_ip(self):
        interfaces = netifaces.interfaces()
        network_info = []

        for interface in interfaces:
            addrs = netifaces.ifaddresses(interface)
            ip_info = addrs.get(netifaces.AF_INET)

            if ip_info is not None:
                ip = ip_info[0]['addr']
                netmask = ip_info[0]['netmask']
                network_info.append({'interface': interface, 'ip': ip, 'netmask': netmask})

        return [i.get('ip') for i in network_info]

    @allure.title("检查台架nuc能否登录")
    def test_ssh_login(self) -> None:
        """
        检查台架ssh密码和飞书里面IP是否对应
        """
        feishu = feishu_api()
        feishu.get_app_access_token()
        feishu.get_user_access_token()
        feishu.get_bitable_app_access_token(document_id="Nm6awGREhiWGPkkux9EcGYsjndd")
        table_id = feishu.get_table_id_by_table_name("标准台架信息汇总")
        message_info = feishu.get_all_records_in_table(table_id)
        root_passwd = None

        for info in message_info:
            if info['fields']['WifiIP地址'] == self.config.get("wifi_localhost"):
                root_passwd = info['fields']['root密码']
        err_list = []
        if not root_passwd:
            err_list.append(f"飞书台架信息中没有发现root的密码，请仔细检查")

        ssh_obj = None
        try:
            ssh_obj = SSHClient(hostname=self.config.get("wifi_localhost"), password=root_passwd)
        except Exception as e:
            err_list.append("ssh登录错误：" + str(e))
        finally:
            if ssh_obj:
                ssh_obj.close()
        error_info = "\n".join(err_list)
        self.alert_info['SSH登录检查'] = error_info if error_info else "PASS"
        assert not error_info, error_info

    @allure.title("检查有线IP")
    def test_wired_ip(self) -> None:
        """
        检查网卡有线IP和飞书里面IP是否对应
        """
        if self.config.get("domain") == "single_tcam":
            pytest.skip("当前单域TCAM，跳过检查")

        local_ip_list = self.get_local_network_ip()
        logger.info(f"local ip list is:{local_ip_list}")
        feishu = feishu_api()
        feishu.get_app_access_token()
        feishu.get_user_access_token()
        feishu.get_bitable_app_access_token(document_id="Nm6awGREhiWGPkkux9EcGYsjndd")
        table_id = feishu.get_table_id_by_table_name("标准台架信息汇总")
        message_info = feishu.get_all_records_in_table(table_id)
        wired_ip = None

        for info in message_info:
            if info['fields']['WifiIP地址'] == self.config.get("wifi_localhost"):
                wired_ip = info['fields']['有线IP地址']

        err_list = []
        if not wired_ip:
            err_list.append(f"飞书台架信息表没有发现有线IP的配置，请仔细核对飞书台架表有线IP")
        elif wired_ip not in local_ip_list:
            info = "|".join(local_ip_list)
            err_list.append(f"台架信息表配置的有线ip:{wired_ip},没有在当前NUC发现（{info}）")
        error_info = "\n".join(err_list)
        self.alert_info['台架有线IP检查'] = error_info if error_info else "PASS"
        assert not error_info, error_info

    @allure.title("检查BGM电源控制")
    def test_check_domain(self) -> None:
        """
        检查域控电源控制，通过ping网关来判断电源控制是否可用
        """
        if self.config.get("domain") != "two_domain":
            pytest.skip("当前是非双域台架环境，跳过检查")
        # if self.config.get("domain") == "single_tcam":
        #     pytest.skip("当前是tcam单域台架环境，跳过检查")
        err_list = []
        domains = self.config.get("dut_ecu")
        domain_dict = {
            "BGM": {
                "power_on": self.nucapp.bgm_power_on,
                "power_on_sleep_time": 60,
                "power_off": self.nucapp.bgm_power_off,
                "power_off_sleep_time": 10,
                "ip": " 172.16.5.1"
            },
            "TCAM": {
                "power_on": self.nucapp.tcam_power_on,
                "power_on_sleep_time": 200,
                "power_off": self.nucapp.tcam_power_off,
                "power_off_sleep_time": 10,
                "ip": " 172.16.5.31"
            },
            "CDC": {
                "power_on": self.nucapp.cdc_power_on,
                "power_on_sleep_time": 60,
                "power_off": self.nucapp.cdc_power_off,
                "power_off_sleep_time": 10,
                "ip": "172.16.5.11"
            },
            "ACU": {
                "power_on": self.nucapp.acu_power_on,
                "power_on_sleep_time": 60,
                "power_off": self.nucapp.acu_power_off,
                "power_off_sleep_time": 10,
                "ip": "172.16.5.21"
            }
        }

        def ctrl_power_and_ping(err_list: typing.List[str],
                                domain: str,
                                domain_dict: typing.Dict[str, object]) -> None:
            if domain == "TCAM":
                self.nucapp.tcam_kl15_down()

            domain_dict.get("power_off")()
            time.sleep(30)
            time.sleep(domain_dict.get("power_off_sleep_time"))
            for _ in range(10):
                if not self.ping_31(ip=domain_dict.get("ip")):
                    with allure.step(f'关闭{domain}电源不能ping通{domain}，符合预期'):
                        break
            else:
                error = f"关闭{domain}电源仍可以ping通{domain}，不符合预期，关闭电源失败"
                with allure.step(error):
                    logger.error(error)
                    err_list.append(error)
            if domain == "TCAM":
                self.nucapp.tcam_kl15_up()
                time.sleep(10)

            domain_dict.get("power_on")()
            time.sleep(domain_dict.get("power_on_sleep_time"))
            for _ in range(10):
                if self.ping_31(ip=domain_dict.get("ip")):
                    with allure.step(f'打开{domain}电源可以ping通{domain}，符合预期'):
                        break
            else:
                error = f"打开{domain}电源仍不能ping通{domain}"
                with allure.step(error):
                    logger.error(error)
                    err_list.append(error)

        self.init_real_device()
        for domain in domains:
            # if domain in ['BGM', 'TCAM']:
            if domain in ['BGM']:
                ctrl_power_and_ping(err_list, domain, domain_dict.get(domain))
        error_info = "\n".join(err_list)
        self.alert_info['域控电源检查'] = error_info if error_info else "PASS"
        assert not error_info, error_info

    def init_real_device(self):
        try:
            self.nucapp.bgm_power_on()
        except Exception as e:
            logger.warning(f"bgm_power_on com error:{e}")

        # 不对TCAM串口初始化，耗时很长
        # try:
        #     self.nucapp.tcam_power_on()
        # except Exception as e:
        #     logger.warning(f"tcam_power_on com error:{e}")
        try:
            self.nucapp.bgm_diag_line_up()
        except Exception as e:
            logger.warning(f"bgm_diag_line_up com error:{e}")
        try:
            self.nucapp.pcan_power_on()()
        except Exception as e:
            logger.warning(f"pcan_power_on com error:{e}")
        try:
            self.nucapp.cdc_power_on()
        except Exception as e:
            logger.warning(f"cdc_power_on com error:{e}")
        try:
            self.nucapp.acu_power_on()
        except Exception as e:
            logger.warning(f"acu_power_on com error:{e}")
        try:
            self.nucapp.toomoss_power_on()
        except Exception as e:
            logger.warning(f"toomoss_power_on com error:{e}")
        try:
            self.nucapp.tcam_kl15_up()
        except Exception as e:
            logger.warning(f"tcam_kl15_up com error:{e}")

    @allure.title("检查 CAN 通道")
    def test_can_channel(self) -> None:
        """
        检查CAN通道，当通道异常时，您可尝试插拔设备
        """
        self.ipdu.set_vehspd(0)
        # todo - 使用can报文 533#3350FFFFFFFFFFFF保持TCAM
        self.ipdu.send_pdu('connectivitycanfd', 0x533, [0x33, 0x50, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff], cycle_time=0.5)
        time.sleep(7)
        ms_info = self.tsp.check_rvc_lock_control(1)
        # if ms_info is None:
        #     self.alert_info['CAN总线'] = f"调用tsp接口失败返回：{ms_info.get('msg')}"
        #     assert False

        err_list = []
        for can_channel in self.config.get("can_channels"):
            if can_channel in ["bodyalmcanfd1", "bodyalmcanfd2", "diagnosticcan"]:
                continue
            logger.info(f"{can_channel} 开始初始化通道")
            is_active = self.ipdu.check_bus_recv_message(can_channel)
            if is_active:
                with allure.step(f"{can_channel} 初始化通道成功"):
                    logger.info(f"{can_channel} 初始化通道成功")
            else:
                with allure.step(f"{can_channel} 初始化通道失败！！！"):
                    logger.error(f"{can_channel} 初始化通道失败！！！")
                    err_list.append(f"{can_channel} 初始化通道失败！！！")
        error_info = "\n".join(err_list)
        self.alert_info['CAN总线'] = error_info if error_info else "PASS"
        assert not error_info, error_info

    def set(self,
            bus_name: str,
            msg_name: str,
            signal_name: str,
            sig_value_name: Union[str, int, float],
            ub_flag=True,
            cycle_time=None):
        bus_obj = getattr(self.ipdu, bus_name)
        msg_signals_obj = getattr(bus_obj, msg_name)
        return self.ipdu.set(msg_signals_obj, signal_name, sig_value_name, ub_flag=ub_flag, cycle_time=cycle_time)

    @allure.title("检查 LIN 通道")
    def test_lin_channel(self) -> None:
        """
        检查LIN通道，当通道异常时，您可尝试插拔设备
        """
        if self.config.get("domain") == "single_tcam":
            pytest.skip("当前是tcam单域台架环境，跳过检查")
        err_list = []
        self.set('backbonefr', 'BcmVddmBackBoneFr00', 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        sd_test = None
        try:
            sd_test = Sd_Tester(**self.tc_config)
            sd_test.diagnostic_client_sim_start()
            time.sleep(0.5)
            sd_test.tester_present()
            sd_test.update_serverdoipid(0x1002)
            try:
                sd_test.change_usage_mode(13)
            except Exception as e:
                err_list.append(f"诊断切换为驾驶模式报错：{e}")
            time.sleep(5)
            for lin_channel in self.config.get("lin_channels"):
                is_active = self.ipdu.check_bus_recv_message(lin_channel)
                if is_active:
                    with allure.step(f"{lin_channel} 成功接收到信号"):
                        logger.info(f"{lin_channel} 成功接收到信号")
                else:
                    with allure.step(f"{lin_channel} 总线无信号！！！"):
                        logger.error(f"{lin_channel} 总线无信号！！！")
                        err_list.append(f"{lin_channel} 总线无信号！！！")
        finally:
            if sd_test:
                sd_test.change_usage_mode(1)
                sd_test.stop_tester_present()
                sd_test.diagnostic_client_sim_close()
        error_info = "\n".join(err_list)
        self.alert_info['LIN总线'] = error_info if error_info else "PASS"
        assert not error_info, error_info

    @allure.title("检查 FLEXRAY 通道")
    def test_fr_channel(self) -> None:
        """
        检查FLEXRAY通道，当通道异常时，您可尝试插拔设备
        """
        if self.config.get("domain") == "single_tcam":
            pytest.skip("当前是tcam单域台架环境，跳过检查")
        err_list = []
        self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        # self.set(self.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00', 'VehMtnSt2_StandStillVal3')
        time.sleep(1)
        signal = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.BcmVddmBackBoneFr00,
                                                       'VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00')
        if signal == 3:
            result = f"flexray 通道发送报文成功，期望接收信号值为3，实际接收信号值为{signal}"
            logger.info(result)
        else:
            result = f"flexray 通道发送报文异常，期望接收信号值为3，实际接收信号值为{signal}"
            logger.error(result)
            err_list.append(result)
        with allure.step(result):
            pass

        self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval1()
        # self.set(self.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00', 'VehMtnSt2_StandStillVal3')
        time.sleep(1)
        signal = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.BcmVddmBackBoneFr00,
                                                       'VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00')
        if signal == 1:
            result = f"flexray 通道发送报文成功，期望接收信号值为1，实际接收信号值为{signal}"
            logger.info(result)
        else:
            result = f"flexray 通道发送报文异常，期望接收信号值为1，实际接收信号值为{signal}"
            logger.error(result)
            err_list.append(result)
        with allure.step(result):
            pass
        error_info = "\n".join(err_list)
        self.alert_info['flexray总线'] = error_info if error_info else "PASS"
        assert not error_info, error_info

    @allure.title("检查 IO 通道")
    def test_io_channel(self) -> None:
        '''
        检查IO通道, 当通道接收不到值的时候原因是xxx,
        当通道接收信号与预期不符时可能对业务并无影响，请人工查看是否对您的用例会造成影响
        '''
        if self.config.get("domain") == "single_tcam":
            pytest.skip("当前是tcam单域台架环境，跳过检查")
        err_list = []
        io_dict = {
            "关闭左前门": {
                "set_io": self.io.drvr_door_close,
                "check_io": {
                    "sig_value": 2,
                    "msg_signals_obj": self.ipdu.bodycan.CemBodyFr02,
                    "signal_name": "DoorDrvrSts_2_CemBodySignalIPdu02",
                    "do_assert": False,
                    "timeout": 5}
            },
            "打开左前门": {
                "set_io": self.io.drvr_door_open,
                "check_io": {
                    "sig_value": 1,
                    "msg_signals_obj": self.ipdu.bodycan.CemBodyFr02,
                    "signal_name": "DoorDrvrSts_2_CemBodySignalIPdu02",
                    "do_assert": False,
                    "timeout": 5}
            },
            "关闭 右前门": {
                "set_io": self.io.pass_door_close,
                "check_io": {
                    "sig_value": 2,
                    "msg_signals_obj": self.ipdu.bodycan.CEMBodyFr11,
                    "signal_name": "DoorPassSts_2_CEMBodySignalIPdu11",
                    "do_assert": False,
                    "timeout": 5}
            },
            "打开右前门": {
                "set_io": self.io.pass_door_open,
                "check_io": {
                    "sig_value": 1,
                    "msg_signals_obj": self.ipdu.bodycan.CEMBodyFr11,
                    "signal_name": "DoorPassSts_2_CEMBodySignalIPdu11",
                    "do_assert": False,
                    "timeout": 5}
            },
            "关闭左后门": {
                "set_io": self.io.lere_door_close,
                "check_io": {
                    "sig_value": 2,
                    "msg_signals_obj": self.ipdu.bodycan.CemBodyFr02,
                    "signal_name": "DoorLeReSts_1_CemBodySignalIPdu02",
                    "do_assert": False,
                    "timeout": 5}
            },
            "打开左后门": {
                "set_io": self.io.lere_door_open,
                "check_io": {
                    "sig_value": 1,
                    "msg_signals_obj": self.ipdu.bodycan.CemBodyFr02,
                    "signal_name": "DoorLeReSts_1_CemBodySignalIPdu02",
                    "do_assert": False,
                    "timeout": 5}
            },
            "关闭右后门": {
                "set_io": self.io.rire_door_close,
                "check_io": {
                    "sig_value": 2,
                    "msg_signals_obj": self.ipdu.bodycan.CEMBodyFr11,
                    "signal_name": "DoorRiReSts_1_CEMBodySignalIPdu11",
                    "do_assert": False,
                    "timeout": 5}
            },
            "打开右后门": {
                "set_io": self.io.rire_door_open,
                "check_io": {
                    "sig_value": 1,
                    "msg_signals_obj": self.ipdu.bodycan.CEMBodyFr11,
                    "signal_name": "DoorRiReSts_1_CEMBodySignalIPdu11",
                    "do_assert": False,
                    "timeout": 5}
            },
            "关闭后备箱": {
                "set_io": self.io.trunk_door_close,
                "check_io": {
                    "sig_value": 2,
                    "msg_signals_obj": self.ipdu.bodycan.CEMBodyFr11,
                    "signal_name": "TrSts_2_CEMBodySignalIPdu11",
                    "do_assert": False,
                    "timeout": 5}
            },
            "打开后备箱": {
                "set_io": self.io.trunk_door_open,
                "check_io": {
                    "sig_value": 1,
                    "msg_signals_obj": self.ipdu.bodycan.CEMBodyFr11,
                    "signal_name": "TrSts_2_CEMBodySignalIPdu11",
                    "do_assert": False,
                    "timeout": 5}
            },
            "关闭引擎盖": {
                "set_io": self.io.hood_door1_close,
                "check_io": {
                    "sig_value": 2,
                    "msg_signals_obj": self.ipdu.backbonefr.CemBackBoneFr06,
                    "signal_name": "HoodSts",
                    "do_assert": False,
                    "timeout": 5}
            },
            "打开引擎盖": {
                "set_io": self.io.hood_door1_open,
                "check_io": {
                    "sig_value": 1,
                    "msg_signals_obj": self.ipdu.backbonefr.CemBackBoneFr06,
                    "signal_name": "HoodSts",
                    "do_assert": False,
                    "timeout": 5}
            },
            # "关闭打开充电口": {
            #     "set_io": self.io.charge_lid_open,
            #     "check_io": {
            #         "sig_value": 1,
            #         "msg_signals_obj": self.ipdu.backbonefr.CemBackBoneFr09,
            #         "signal_name": "ChrgLidRearSts_0_CEMBackBoneSignalIpdu09",
            #         "do_assert": False,
            #         "timeout": 5}
            # },
            # "打开打开充电口": {
            #     "set_io": self.io.charge_lid_close,
            #     "check_io": {
            #         "sig_value": 2,
            #         "msg_signals_obj": self.ipdu.backbonefr.CemBackBoneFr09,
            #         "signal_name": "ChrgLidRearSts_0_CEMBackBoneSignalIpdu09",
            #         "do_assert": False,
            #         "timeout": 5}
            # },
            "关闭危险灯": {
                "set_io": self.io.hazard_light_open,
                "check_io": {
                    "sig_value": 1,
                    "msg_signals_obj": self.ipdu.backbonefr.CemBackBoneFr04,
                    "signal_name": "SwtLiHzrdWarn",
                    "do_assert": False,
                    "timeout": 5}
            },
            "打开危险灯": {
                "set_io": self.io.hazard_light_close,
                "check_io": {
                    "sig_value": 0,
                    "msg_signals_obj": self.ipdu.backbonefr.CemBackBoneFr04,
                    "signal_name": "SwtLiHzrdWarn",
                    "do_assert": False,
                    "timeout": 5}
            },
            "关闭驾驶员占位传感器": {
                "set_io": self.io.driver_seat_present,
                "check_io": {
                    "sig_value": 2,
                    "msg_signals_obj": self.ipdu.backbonefr.CemBackBoneFr12,
                    "signal_name": "DrvrSeatSts",
                    "do_assert": False,
                    "timeout": 5}
            },
            "打开驾驶员占位传感器": {
                "set_io": self.io.driver_seat_notpresent,
                "check_io": {
                    "sig_value": 1,
                    "msg_signals_obj": self.ipdu.backbonefr.CemBackBoneFr12,
                    "signal_name": "DrvrSeatSts",
                    "do_assert": False,
                    "timeout": 5}
            },
            # "关闭刹车踏板开关": {
            #     "set_io": self.io.brake_down,
            #     "check_io": {
            #         "sig_value": 0,
            #         "msg_signals_obj": self.ipdu.backbonefr.BcmVddmBackBoneFr00,
            #         "signal_name": "BrkPedlPsdBrkPedlPsd",
            #         "do_assert": False,
            #         "timeout": 5}
            # },
            # "打开刹车踏板开关": {
            #     "set_io": self.io.brake_up,
            #     "check_io": {
            #         "sig_value": 1,
            #         "msg_signals_obj": self.ipdu.backbonefr.BcmVddmBackBoneFr00,
            #         "signal_name": "BrkPedlPsdBrkPedlPsd",
            #         "do_assert": False,
            #         "timeout": 5}
            # },
            # "关闭外部尾门解锁": {
            #     "set_io": self.io.trunk_door_outswitch_pressed,
            #     "check_io": {
            #         "sig_value": 0,
            #         "msg_signals_obj": self.ipdu.backbonefr.CemBackBoneFr25,
            #         "signal_name": "TrSts",
            #         "do_assert": False,
            #         "timeout": 5}
            # },
            # "打开外部尾门解锁": {
            #     "set_io": self.io.trunk_door_outswitch_unpressed,
            #     "check_io": {
            #         "sig_value": 1,
            #         "msg_signals_obj": self.ipdu.backbonefr.CemBackBoneFr25,
            #         "signal_name": "TrSts",
            #         "do_assert": False,
            #         "timeout": 5}
            # },
        }
        for io_name, io_info in io_dict.items():
            if io_name == "关闭引擎盖":
                self.io.hood_door2_open()

            logger.info(io_name)
            io_info.get("set_io")()
            time.sleep(0.3)
            check_io_info = io_info.get("check_io")
            _, realvalue, expectedvalue = self.ipdu.check(
                msg_signals_obj=check_io_info.get("msg_signals_obj"),
                signal_name=check_io_info.get("signal_name"),
                sig_value_name=check_io_info.get("sig_value"),
                do_assert=check_io_info.get("do_assert"),
                timeout=check_io_info.get("timeout")
            )
            if realvalue == expectedvalue:
                result = f"{io_name} 设置后状态正常 期望是{expectedvalue}实际是{realvalue}"
                with allure.step(result):
                    logger.info(result)
            else:
                result = f"{io_name} 设置后状态异常 期望是{expectedvalue}实际是{realvalue}"
                with allure.step(result):
                    logger.error(result)
                    err_list.append(result)
        error_info = "\n".join(err_list)
        self.alert_info['IO检测'] = error_info if error_info else "PASS"
        assert not error_info, f"{error_info}\n通过接收can信号判断，结果为None时请先检查can总线，若预期值与实际不符时请检查台架手动控制Io的按钮状态"

    @allure.title("检查 soa_partner")
    def test_soapartner(self) -> None:
        """
        用于检查soa_partner是否能正常启动，只有当环境中没有ACU时才可启动
        """
        if self.config.get("domain") != "two_domain":
            pytest.skip("当前是非双域台架环境，跳过检查")
        if self.config.get("domain") == "single_tcam":
            pytest.skip("当前是tcam单域台架环境，跳过检查")
        partner_process_check()
        self.soa_partner = None
        try:
            self.soa_partner = S2sBaseClass([("BlueToothService", "client")])
        except Exception as error:
            with allure.step(f"soa_partner启动失败"):
                self.alert_info['soa_partner'] = "soa_partner启动失败"
                assert False, f"soa_partner启动失败!!! 异常：{error}"
        else:
            with allure.step(f"soa_partner启动成功"):
                self.alert_info['soa_partner'] = "PASS"
                assert True
        finally:
            if self.soa_partner:
                self.soa_partner.stop_operators()
            partner_process_check()

    @allure.title("检查 tsp")
    def test_tsp(self) -> None:
        """
        检查tsp
        """
        tel = self.config.get("tel")
        url = 'https://api.jidustaging.com/api/user-c-server/v1/login/sms_login'
        "获取远控操作token"
        headers = {
            "Content-Type": "application/json",
            "client": "4"
        }
        data = {
            "countryCode": "86",
            "tel": tel,
            "captcha": "6825",
            "captchaKey": __import__("os").environ['XAT_CREDENTIAL_SCAN_7CD10D93116DEE020DFC']
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            logger.info(response.json()['data']['token'])
            with allure.step(f"请求{url}成功"):
                self.alert_info['tsp'] = "PASS"
        except Exception:
            with allure.step(f"请求{url}失败"):
                self.alert_info['tsp'] = f"请求{url}失败"
                assert False, f"请求{url}失败"

    @allure.title("检查 BNCM KEY 状态")
    def test_bncm_key(self) -> None:
        """
        检查bncm key 状态是否正常, 若发生异常则是bncm key错误，
        可能是key未写入或写入了错误的key，若是错误写入请记录错误写入的key并尽快恢复
        """
        if self.config.get("domain") == "single_tcam":
            pytest.skip("单域tcam不检查")
        sdtest = SdTest()
        try:
            is_write = sdtest.send_request_and_recv_response([0x22, 0xD9, 0X04])[0]
        finally:
            sdtest.stop_sd_tester()
        if is_write:
            with allure.step("已写入 bncm key"):
                logger.info("已写入 bncm key")
        else:
            with allure.step("bncm key 未写入，请尝试写入bncm key, 写入时请妥善保存bncm key"):
                logger.error("bncm key 未写入，请尝试写入bncm key, 写入时请妥善保存bncm key")
                self.alert_info['bncm key'] = "bncm key 未写入，请尝试写入bncm key, 写入时请妥善保存bncm key"
                assert False, "bncm key 未写入，请尝试写入bncm key, 写入时请妥善保存bncm key"

        dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        try:
            dk.send_nfc_cmd()
            self.alert_info['bncm key'] = "PASS"
            with allure.step("bncm key 状态正常"):
                logger.info("bncm key 状态正常")
                self.alert_info['bncm key'] = "PASS"
                assert True
        except Exception as e:
            with allure.step(
                    "bncm key 状态异常, 可能是key未写入或写入了错误的key，若是错误写入请记录错误写入的key并尽快恢复"):
                error = "bncm key 状态异常, 可能是key未写入或写入了错误的key，若是错误写入请记录错误写入的key并尽快恢复"
                self.alert_info['bncm key'] = error
                assert False, error

    @allure.title("检查ECU活跃状态")
    def test_ecu_is_active(self) -> None:
        """
        通过诊断检查ECU是否活跃
        """
        if self.config.get("domain") == "single_tcam":
            self.tc_config["sd_tester_cfg"]["ecu_name"] = "TCAM"
            self.tc_config["sd_tester_cfg"]["server_ip"] = "172.16.9.31"

        err_list = []
        domains = self.config.get("dut_ecu")
        self.sd_test = Sd_Tester(**self.tc_config)
        self.sd_test.diagnostic_client_sim_start()
        time.sleep(1)
        if self.config.get("domain") == "single_tcam":
            self.sd_test.update_serverdoipid(0x1011, ecu="TCAM")

        ecu_state = self.sd_test.all_ecu_is_active()
        self.sd_test.diagnostic_client_sim_close()
        for domain in domains:
            domain_state = ecu_state.get(domain).get("active")
            if domain_state is True:
                with allure.step(f"{domain} 当前状态为跃状态"):
                    logger.info(f"{domain} 当前状态为跃状态")
            else:
                with allure.step(f"{domain} 当前状态为非活跃状态"):
                    logger.error(f"{domain} 当前状态为非活跃状态")
                    err_list.append(f"{domain} 当前状态为非活跃状态")
        error_info = "\n".join(err_list)
        self.alert_info['ECU'] = error_info if error_info else "PASS"
        assert not error_info, error_info

    @allure.title("检查BGM是否写入车云依赖证书")
    def test_bgm_dependency_certificate(self) -> None:
        """
        检查BGM是否写入车云依赖证书
        """
        if self.config.get("domain") == "single_tcam":
            pytest.skip("单域tcam不检查")
        ssh = Ssh(domain=self.config.get("domain"))
        ssh.type_commands(DeviceName.BGM, "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib", timeout=3)
        ssh.type_commands(DeviceName.BGM, "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib/soa", timeout=3)
        ssh.type_commands(DeviceName.BGM, "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib/proxy", timeout=3)
        ssh.type_commands(DeviceName.BGM, "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/service/em", timeout=3)
        ssh.type_commands(DeviceName.BGM, "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/service/prop", timeout=3)
        ssh.type_commands(DeviceName.BGM, "export ENV_APP_PATH=/app/", timeout=3)
        ssh.type_commands(DeviceName.BGM, "export ENV_APP_INFO=/app/etc/AppInfo.json", timeout=3)
        ssh.type_commands(DeviceName.BGM, "export ENV_CONFIG_PATH=/app/etc/", timeout=3)
        ssh.type_commands(DeviceName.BGM, "export ENV_SOA_CONFIG_PATH=/app/etc/soaconfig/", timeout=3)
        ssh.type_commands(DeviceName.BGM, "export UDSDOIP_CONFIG_PATH=/app/bin/udsconfig/", timeout=3)
        ssh.type_commands(DeviceName.BGM, "export UDSDOIP_DATA_PATH=/data/uds/", timeout=3)
        ssh.type_commands(DeviceName.BGM, "export BOOTES_HOME_DIR=/app/etc", timeout=3)
        result = ssh.type_commands(DeviceName.BGM, "/app/bin/ts_security -m test1 -d 0123456", timeout=5)
        dependency_certificate = result.split("\n")[2]
        if dependency_certificate:
            with allure.step(f"已配置BGM车云证书{dependency_certificate}"):
                logger.info(f"已配置BGM车云证书{dependency_certificate}")
                self.alert_info['BGM车云证书'] = "PASS"
                assert True
        else:
            with allure.step("未配置BGM车云证书"):
                logger.error("未配置BGM车云证书")
                self.alert_info['BGM车云证书'] = "未配置BGM车云证书"
                assert not False, "未配置BGM车云证书"

    @allure.title("检查通过安全级")
    def test_security_constant(self) -> None:
        """
        检查是否能通过安全级锁
        """
        if self.config.get("domain") == "single_tcam":
            pytest.skip("单域tcam不检查")
        err_list = []
        try:
            diag = DiagTestBase(self.ipdu, self.busapp, self.tc_config)
            diag.connect(0x1001)
        except:
            self.alert_info['诊断安全级'] = "初始化诊断类失败"
            assert not False, "初始化诊断类失败"

        def security_access_level(level: int) -> None:
            try:
                diag.security_access_level(level)
                with allure.step(f"通过安全访问L{level}"):
                    logger.info(f"通过安全访问L{level}成功")
            except Exception as e:
                with allure.step(f"通过安全访问L{level}失败，请检查安全常数"):
                    err_list.append(f"通过安全访问L{level}失败，请检查安全常数")
                    logger.error(f"通过安全访问L{level}失败，请检查安全常数")

        with allure.step("进入默认会话"):
            diag.session_control(1)
        with allure.step("进入扩展会话"):
            diag.session_control(3)
            security_access_level(7)
        with allure.step("进入boot"):
            diag.enter_boot()
        with allure.step("进入默认会话"):
            diag.session_control(1)
        with allure.step("进入扩展会话"):
            diag.session_control(3)
            for level in [3, 5]:  # 11也需要检查，用的不多，暂时忽略
                security_access_level(level)
        with allure.step("进入编程会话"):
            diag.session_control(2)
            security_access_level(1)
        with allure.step(f"退出boot，关闭诊断服务"):
            try:
                diag.exit_boot()
                diag.close()
            except Exception as e:
                err_list.append("退出编程会话，关闭诊断服务失败")
        error_info = "\n".join(err_list)
        self.alert_info['诊断安全级'] = error_info if error_info else "PASS"
        assert not error_info, error_info

    @allure.title("检查实际vid是否与配置表中一致")
    def test_vid(self):
        """
        检查vid是否与配置表中一致，若不一致请修改yaml配置文件
        """
        if self.config.get("domain") == "single_tcam":
            pytest.skip("单域tcam不检查")
        yaml_vid = self.config.get("vid")
        diag = DiagTestBase(self.ipdu, self.busapp, self.tc_config)
        diag.connect(0x1001)
        diag.init_boot_per()
        with allure.step("进入默认会话"):
            diag.session_control(1)
        with allure.step("进入扩展会话"):
            diag.session_control(3)
        with allure.step("通过安全访问L5"):
            diag.security_access_level(5)
        with allure.step("读取VID测试"):
            diag.read_data_by_identifier(0xB163)
            vid = diag.get_payload()[6:]
            diag.close()
        if yaml_vid == vid:
            with allure.step("yaml配置文件vid号与实际vid号一致"):
                logger.info("yaml配置文件vid号与实际vid号一致")
                self.alert_info['vid'] = "PASS"
                assert True
        else:
            if vid == "ffffffffffffffffffffffffffffffff":
                error = f"未安装生成vid需要的证书，请通过诊断仪重新设置vin和vid"
                logger.error(error)
                self.alert_info['vid'] = error
                # self.sd_tester = SdTest(**self.tc_config)
                # self.sd_tester.start_sd_tester()
                # time.sleep(1)
                # try:
                #     self.sd_tester.write_did_and_check(TA.BGM_SOC, 0xb163, SESSION.EXTENDED, UnLock.L7, yaml_vid,
                #                                        '62b163' + yaml_vid, check_method=Check_Method.reset,
                #                                        recover=False)
                # finally:
                #     self.sd_tester.stop_sd_tester()
                # logger.info(f"已经恢复台架VID为：{yaml_vid}")
            else:
                error = f"yaml配置文件中vid号与台架实际vid号: {vid} 不一致，请修改yaml文件中的vid号"
                logger.error(error)
                self.alert_info['vid'] = error
            with allure.step(error):
                logger.error(error)

    @allure.title("检查实际vin是否与配置表中一致")
    def test_vin(self):
        """
        检查vin是否与配置表中一致，若不一致请修改yaml配置文件
        """
        if self.config.get("domain") == "single_tcam":
            pytest.skip("单域tcam不检查")
        yaml_vin = self.config.get("vin")
        diag = DiagTestBase(self.ipdu, self.busapp, self.tc_config)
        diag.connect(0x1002)
        diag.init_boot_per()
        with allure.step("进入默认会话"):
            diag.session_control(1)
        with allure.step("读取VIN码测试"):
            diag.read_data_by_identifier(0xF190)
            hex_string = diag.get_payload()[6:]
            diag.close()
            vin = ""
            for i in range(0, len(hex_string), 2):
                vin += chr(int(hex_string[i:i + 2], 16))
            logger.info(f"读取到的vin号是{vin}")

        if yaml_vin == vin:
            with allure.step("yaml配置文件vin号与实际vin号一致"):
                logger.info("yaml配置文件vin号与实际vin号一致")
                self.alert_info['vin'] = "PASS"
                assert True
        else:
            error = f"yaml配置文件中vin号与台架实际vin号: {vin} 不一致，请修改yaml文件中的vin号"
            with allure.step(error):
                logger.error(error)
                self.alert_info['vin'] = error
                assert not False, error


class TestBenchEnv2(TestABCBase):

    def before_class(self, ecu):
        self.TestDigitalKeyBase = TestDigitalKeyBase()
        self.config = self.parser_ecu(self, ecu)
        self.alert_info = {}
        self.nucapp = None
        try:
            self.nucapp = NucApp(ecu.tc_config)
        except Exception as e:
            logger.error(f'NucApp初始化异常，原因:{str(e)}')
            raise exception_error.NucAppError(f'NucApp初始化异常，原因:{str(e)}')
        sleep(1)

    def before_each_func(self, ecu):
        pass

    def after_each_func(self, ecu):
        sleep(1)

    def after_class(self, ecu):
        # 如果有ECALL没有挂断，则挂断ECALL
        try:
            self.soa.update(["CallService_client"])
            sleep(2)
            self.soa.hang_up_call_sos(ReqSrc=eCallReqSource.kCDC)
        except Exception as e:
            logger.error(e)
        output = exec_shell(f"pwd").get("output", "")
        alarm_description = AlertInfo(self.tc_config.get("wifi_localhost"), self.alert_info)
        alarm = FeishuAlert(alarm_description)
        if str(output).startswith("/root/autotools/bench_check"):
            alarm.post_to_robot()
        else:
            alarm.post_to_robot(True)

    def parser_ecu(self, ecu) -> typing.Dict[str, typing.Any]:
        eths = []
        can_channels = []
        can_devices = set()
        lin_channels = []
        lin_devices = set()
        fr_channels = []
        fr_devices = set()
        config: dict = ecu.tc_config
        bus = config.get("bus")
        eths.append([bus.get("eth_obd"), config.get("eth_obd")])
        if bus.get("eth_vlan5"):
            eths.append([bus.get("eth_vlan5"), "172.16.5.21"])
        for bus_name, devices in bus.items():
            if "can" in bus_name:
                can_channels.append(bus_name)
                can_devices.add(devices[0])
            elif "cem" in bus_name:
                lin_channels.append(bus_name)
                lin_devices.add(devices[0])
            elif "fr" in bus_name:
                fr_channels.append(bus_name)
                fr_devices.add(devices[0])
        for key, value in ecu.domain.__dict__.items():
            if value is not None:
                domain = key
                dut_ecu = value.get("type")
                break
        domain = domain if domain in ["four_domain", "two_domain", "single_tcam", "single_bgm"] else "nonsupport"
        return {
            "domain": domain,
            "dut_ecu": dut_ecu,
            "eths": eths,
            "wifi_localhost": config.get("wifi_localhost"),
            "tel": config.get("tel"),
            "can_channels": can_channels,
            "can_devices": can_devices,
            "lin_channels": lin_channels,
            "lin_devices": lin_devices,
            "fr_channels": fr_channels,
            "fr_devices": fr_devices,
            "vid": config.get("vid"),
            "vin": config.get("vin"),
            "uid": config.get("uid"),
            "bncm_key": config.get("BNCM_KEY"),
            "serials": config.get("serial")
        }

    def tcam_domain(self):
        ms_info = self.tsp.check_rvc_lock_control(1)
        if ms_info['code'] != 0:
            self.alert_info['车主绑定'] = ms_info['msg']
        else:
            self.alert_info['车主绑定'] = "PASS"

        ms_info = self.tsp.check_error_rvc_lock_control(1)
        if ms_info['code'] != 600004 and ms_info['msg'] != '没有指令下发权限':
            self.alert_info['车主绑定'] = ms_info['msg']
        else:
            self.alert_info['车主绑定'] = "PASS"

    def two_domain(self):
        error_message = ""
        try:
            self.TestDigitalKeyBase.uid = self.tc_config.get('uid') if self.tc_config.get('uid') != None else self.tsp.get_uid()
        except Exception as e:
            error_message = (f"通过台架配置文件电话号码：{self.config.get('tel')},调用平台接口获取uid失败，请检查配置文件电话号码是否绑定，"
                             f"绑定台架需要提供：staging环境车辆vin:{self.config.get('vin')},tel:{self.config.get('tel')}然后@yuxue.jia进行绑定。")
            self.alert_info['车主绑定'] = error_message
            raise AssertionError(f"{e}")

        self.TestDigitalKeyBase.tsp_dk = DigitalKeyManager(vid=self.config.get('vid'),
                                                           tel=self.config.get('tel'),
                                                           user_agent="jiduapp/0.9.3 (iOS; 16.0; apple; jdcomiphone; iPhone 12; NULL; BF983636-D3F2-4805-90B4-77C3DC75D433; aVBob25l)")
        sleep(2)
        try:
            bind_message = self.TestDigitalKeyBase.mock_pes_sign(self.config.get('vid'), True)
            logger.info(f"bind_message {bind_message}")
            if bind_message.get("code") == 0:
                self.alert_info['车主绑定'] = "PASS"
            else:
                logger.warning(bind_message.get("msg"))
                error_message = (
                    f"通过台架配置文件电话号码：{self.config.get('tel')},调用平台接口获取uid失败，请检查配置文件电话号码是否绑定，"
                    f"绑定台架需要提供：staging环境车辆vin和tel然后@yuxue.jia进行绑定。")
                self.alert_info['车主绑定'] = error_message
        except Exception as e:
            logger.info(f"车主绑定失败：{str(e)}")
            error_message = (
                f"通过台架配置文件电话号码：{self.config.get('tel')},调用平台接口获取uid失败，请检查配置文件电话号码是否绑定，"
                f"绑定台架需要提供：staging环境车辆vin和tel然后@yuxue.jia进行绑定。")
            self.alert_info['车主绑定'] = error_message
        assert True if not error_message else False, error_message

    @allure.title("检查车主绑定")
    def test_owner_binding(self) -> None:
        if self.config.get("domain") not in ["single_tcam", "two_domain"]:
            pytest.skip(f"域控为:{self.config.get('domain')},跳过不检查。")
        if self.config.get("domain") == "single_tcam":
            self.tcam_domain()
        elif self.config.get("domain") == "two_domain":
            self.two_domain()


if __name__ == "__main__":
    pytest.main()
