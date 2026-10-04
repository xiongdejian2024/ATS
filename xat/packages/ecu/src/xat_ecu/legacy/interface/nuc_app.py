# -*- coding: utf-8 -*-
"""
@File        : nuc_app.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022/11/09 09:49
@Description : description about this file
@Examples    : NUC linux common command
"""

import sys
import os
from pathlib import Path

from xat_ecu.legacy.common.logger import *
from xat_ecu.legacy.common import exception_error
from time import sleep
from scapy.all import *
import serial
import serial.tools.list_ports
from serial import SerialException

os.environ["LOGGER"] = "logger"  # 防止 ecu sim logger 多打印
from xat_ecu.legacy.sdk.ethernet.doip_client_sim_odx import Doip_Client_Sim_Odx
from typing import Tuple, Union
from subprocess import Popen
from xat_ecu.legacy.common.file_handle import *

global OBDETH
OBDETH = ""


def convert_data(my_string):
    # OUT1_OPEN = "FE050000FF009835"  # OUT1 OPEN
    # OUT1_CLOSE = "FE0500000000D9C5"  # OUT1 CLOSE
    my_int = int(my_string, 16)
    my_data = my_int.to_bytes((len(my_string) + 1) // 2, byteorder='big')
    return my_data


def jy_dam0800_operation(operation_target, operation_type, port):
    logger.info(f"端口：{operation_target}, 动作：{operation_type}, port:{port}")
    if port is None:
        logger.error("没有找到可用的Jy DAM 继电器，继电器控制失败。")
        return
    try:
        bps = 9600
        # 超时时间,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
        time = 5
        data_dict = {"COM1": {"open": "FE050000FF009835", "close": "FE0500000000D9C5"},
                     "COM2": {"open": "FE050001FF00C9F5", "close": "FE05000100008805"},
                     "COM3": {"open": "FE050002FF0039F5", "close": "FE05000200007805"},
                     "COM4": {"open": "FE050003FF006835", "close": "FE050003000029C5"},
                     "COM5": {"open": "FE050004FF00D9F4", "close": "FE05000400009804"},
                     "COM6": {"open": "FE050005FF008834", "close": "FE0500050000C9C4"},
                     "COM7": {"open": "FE050006FF007834", "close": "FE050006000039C4"},
                     "COM8": {"open": "FE050007FF0029F4", "close": "FE05000700006804"}}

        byte_data = convert_data(data_dict.get(operation_target).get(operation_type))

        # 打开串口，并返回串口对象
        uart = serial.Serial(port, bps, timeout=time)

        # 串口发送一个字符串
        data_len = uart.write(byte_data)
        # print("send len: ", data_len)

        # 串口接收一个字符串
        receive_data = b''
        for i in range(data_len):
            receive_data += uart.read()
        if receive_data == byte_data:
            logger.info(f"=======JYDAM0800 {operation_target} action {operation_type}, success")
        else:
            logger.info(f"=======JYDAM0800 {operation_target} action {operation_type}, fail")
    except SerialException as e1:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/nuc_app.py")
        logger.info(f"=======JYDAM0800 {operation_target} action {operation_type}, success")
    except Exception as result:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/nuc_app.py")
        logger.error("******error******：", result)
    finally:
        # 关闭串口
        uart.close()


def get_jy_dam_port():
    jy_dam_port = None
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) == 0:
        print('无可用串口')
    else:
        for i in range(0, len(port_list)):
            port = str(port_list[i]).split(" - ")
            if "CP2102" in port[1]:
                jy_dam_port = port[0]
                break
        else:
            print("没有可以的jy dam继电器")
    return jy_dam_port


class NucApp:
    def __init__(self, tb_cfg={}):
        self.eth_obd = None
        self.tb_cfg = tb_cfg
        self.eth_obd_nuc_ip = self.tb_cfg.get("eth_obd")
        self.eth_obd = self.tb_cfg.get("bus").get("eth_obd")
        self.power_control_type = self.tb_cfg.get("power_control_type", None)
        if self.power_control_type:
            if self.power_control_type == "jydam0800":
                self.jydam0800_port = get_jy_dam_port()
        else:
            self.usbrelay_map = self.tb_cfg.get("usbrelay")
            self.usbrelay_name = self.get_usbrelay_name()

    # ----------------------------  Simple call    ----------------------------------------

    def bgm_power_off(self):
        if self.power_control_type:
            if self.power_control_type == "jydam0800":
                jy_dam0800_operation(self.tb_cfg.get("jydam0800").get("BGM_P"), "open", self.jydam0800_port)
            else:
                self.usbrelay_cmd_open("BGM_P")
        else:
            self.usbrelay_cmd_open("BGM_P")

    def bgm_power_on(self):
        if self.power_control_type:
            if self.power_control_type == "jydam0800":
                jy_dam0800_operation(self.tb_cfg.get("jydam0800").get("BGM_P"), "close", self.jydam0800_port)
            else:
                self.usbrelay_cmd_close("BGM_P")
        else:
            self.usbrelay_cmd_close("BGM_P")

    def tcam_power_off(self):
        if self.power_control_type:
            if self.power_control_type == "jydam0800":
                jy_dam0800_operation(self.tb_cfg.get("jydam0800").get("TCAM_P"), "open", self.jydam0800_port)
            else:
                self.usbrelay_cmd_open("TCAM_P")
        else:
            self.usbrelay_cmd_open("TCAM_P")

    def tcam_power_on(self):
        if self.power_control_type:
            if self.power_control_type == "jydam0800":
                jy_dam0800_operation(self.tb_cfg.get("jydam0800").get("TCAM_P"), "close", self.jydam0800_port)
            else:
                self.usbrelay_cmd_close("TCAM_P")
        else:
            self.usbrelay_cmd_close("TCAM_P")

    def cdc_power_off(self):
        if self.power_control_type:
            if self.power_control_type == "jydam0800":
                jy_dam0800_operation(self.tb_cfg.get("jydam0800").get("CDC_P"), "open", self.jydam0800_port)
            else:
                self.usbrelay_cmd_open("CDC_P")
        else:
            self.usbrelay_cmd_open("CDC_P")

    def cdc_power_on(self):
        if self.power_control_type:
            if self.power_control_type == "jydam0800":
                jy_dam0800_operation(self.tb_cfg.get("jydam0800").get("CDC_P"), "close", self.jydam0800_port)
            else:
                self.usbrelay_cmd_close("CDC_P")
        else:
            self.usbrelay_cmd_close("CDC_P")

    def acu_power_off(self):
        if self.power_control_type:
            if self.power_control_type == "jydam0800":
                jy_dam0800_operation(self.tb_cfg.get("jydam0800").get("ACU_P"), "open", self.jydam0800_port)
            else:
                self.usbrelay_cmd_open("ACU_P")
        else:
            self.usbrelay_cmd_open("ACU_P")

    def acu_power_on(self):
        if self.power_control_type:
            if self.power_control_type == "jydam0800":
                jy_dam0800_operation(self.tb_cfg.get("jydam0800").get("ACU_P"), "close", self.jydam0800_port)
            else:
                self.usbrelay_cmd_close("ACU_P")
        else:
            self.usbrelay_cmd_close("ACU_P")

    def pcan_power_off(self):
        if self.power_control_type:
            if self.power_control_type == "jydam0800":
                jy_dam0800_operation(self.tb_cfg.get("jydam0800").get("PCAN_P"), "open", self.jydam0800_port)
            else:
                self.usbrelay_cmd_open("PCAN_P")
        else:
            self.usbrelay_cmd_open("PCAN_P")

    def pcan_power_on(self):
        if self.power_control_type:
            if self.power_control_type == "jydam0800":
                jy_dam0800_operation(self.tb_cfg.get("jydam0800").get("PCAN_P"), "close", self.jydam0800_port)
            else:
                self.usbrelay_cmd_close("PCAN_P")
        else:
            self.usbrelay_cmd_close("PCAN_P")

    def toomoss_power_off(self):
        if self.power_control_type:
            if self.power_control_type == "jydam0800":
                jy_dam0800_operation(self.tb_cfg.get("jydam0800").get("Toomoss_P"), "open", self.jydam0800_port)
            else:
                self.usbrelay_cmd_open("Toomoss_P")
        else:
            self.usbrelay_cmd_open("Toomoss_P")

    def toomoss_power_on(self):
        if self.power_control_type:
            if self.power_control_type == "jydam0800":
                jy_dam0800_operation(self.tb_cfg.get("jydam0800").get("Toomoss_P"), "close", self.jydam0800_port)
            else:
                self.usbrelay_cmd_close("Toomoss_P")
        else:
            self.usbrelay_cmd_close("Toomoss_P")

    def bgm_diag_line_up(self):
        if self.power_control_type:
            if self.power_control_type == "jydam0800":
                jy_dam0800_operation(self.tb_cfg.get("jydam0800").get("BGM_D"), "open", self.jydam0800_port)
            else:
                self.usbrelay_cmd_open("BGM_D")
        else:
            self.usbrelay_cmd_open("BGM_D")

    def bgm_diag_line_down(self):
        if self.power_control_type:
            if self.power_control_type == "jydam0800":
                jy_dam0800_operation(self.tb_cfg.get("jydam0800").get("BGM_D"), "close", self.jydam0800_port)
            else:
                self.usbrelay_cmd_close("BGM_D")
        else:
            self.usbrelay_cmd_close("BGM_D")

    def tcam_kl15_up(self):
        if self.power_control_type:
            if self.power_control_type == "jydam0800":
                jy_dam0800_operation(self.tb_cfg.get("jydam0800").get("TCAM_KL15"), "open", self.jydam0800_port)
            else:
                self.usbrelay_cmd_open("TCAM_KL15")
        else:
            self.usbrelay_cmd_open("TCAM_KL15")

    def tcam_kl15_down(self):
        if self.power_control_type:
            if self.power_control_type == "jydam0800":
                jy_dam0800_operation(self.tb_cfg.get("jydam0800").get("TCAM_KL15"), "close", self.jydam0800_port)
            else:
                self.usbrelay_cmd_close("TCAM_KL15")
        else:
            self.usbrelay_cmd_close("TCAM_KL15")

    # ----------------------------  Door and Door Switch Status ----------------------------------------
    def drvr_door_open(self):
        self.usbrelay_cmd_close("DrvrDoorOpenSts")

    def drvr_door_close(self):
        self.usbrelay_cmd_open("DrvrDoorOpenSts")

    def pass_door_open(self):
        self.usbrelay_cmd_close("PassDoorOpenSts")

    def pass_door_close(self):
        self.usbrelay_cmd_open("PassDoorOpenSts")

    def lere_door_open(self):
        self.usbrelay_cmd_close("LeReDoorOpenSts")

    def lere_door_close(self):
        self.usbrelay_cmd_open("LeReDoorOpenSts")

    def rire_door_open(self):
        self.usbrelay_cmd_close("RiReDoorOpenSts")

    def rire_door_close(self):
        self.usbrelay_cmd_open("RiReDoorOpenSts")

    def trunk_door_open(self):
        self.usbrelay_cmd_close("TrunkDoorOpenSts")

    def trunk_door_close(self):
        self.usbrelay_cmd_open("TrunkDoorOpenSts")

    def set_four_door_close(self):
        self.drvr_door_close()
        self.pass_door_close()
        self.lere_door_close()
        self.rire_door_close()

    def drvr_door_outswitch_pressed(self):
        self.usbrelay_cmd_close("DrvrDoorOutSwitch")

    def drvr_door_outswitch_unpressed(self):
        self.usbrelay_cmd_open("DrvrDoorOutSwitch")

    def pass_door_outswitch_pressed(self):
        self.usbrelay_cmd_close("PassDoorOutSwitch")

    def pass_door_outswitch_unpressed(self):
        self.usbrelay_cmd_open("PassDoorOutSwitch")

    def lere_door_outswitch_pressed(self):
        self.usbrelay_cmd_close("LeReDoorOutSwitch")

    def lere_door_outswitch_unpressed(self):
        self.usbrelay_cmd_open("LeReDoorOutSwitch")

    def rire_door_outswitch_pressed(self):
        self.usbrelay_cmd_close("RiReDoorOutSwitch")

    def rire_door_outswitch_unpressed(self):
        self.usbrelay_cmd_open("RiReDoorOutSwitch")

    def trunk_door_outswitch_pressed(self):
        self.usbrelay_cmd_open("TrunkDoorOutSwtich")

    def trunk_door_outswitch_unpressed(self):
        self.usbrelay_cmd_close("TrunkDoorOutSwtich")

    def driver_seat_present(self):
        self.usbrelay_cmd_open("DrvrSeatPresent")

    def driver_seat_notpresent(self):
        self.usbrelay_cmd_close("DrvrSeatPresent")

    def brake_down(self):
        self.usbrelay_cmd_open("Brake")

    def brake_up(self):
        self.usbrelay_cmd_close("Brake")

    def release_door_switch(self):
        self.drvr_door_outswitch_unpressed()
        self.pass_door_outswitch_unpressed()
        self.lere_door_outswitch_unpressed()
        self.rire_door_outswitch_unpressed()

    def init_bgm_HW(self):
        self.bgm_power_on()
        self.bgm_diag_line_up()
        self.set_four_door_close()
        self.trunk_door_close()
        self.release_door_switch()
        self.trunk_door_outswitch_unpressed()
        self.driver_seat_notpresent()
        self.brake_up()

    # -------------------------------------------------------------------------------------------------------------

    # -----------------------------    Flexible call   ------------------------------------------
    def get_usbrelay_name(self):
        results = exec_shell("usbrelay")
        results_str = results["output"]
        result = re.search(r"(\w*)_1=", results_str)
        if result:
            usbrelay_name = result.group(1)
        else:
            usbrelay_name = None
        return usbrelay_name

    def usbrelay_cmd(self, num: Union[int, str], on_off: int):
        # on_off:    0 ---- on        1 ---- off
        if self.usbrelay_name or self.usbrelay_name == "":
            if isinstance(num, int):
                usbrelay_cmd = "usbrelay {}_{}={}".format(
                    self.usbrelay_name, num, on_off
                )
            elif isinstance(num, str):
                usbrelay_cmd = "usbrelay {}={}".format(num, on_off)
            res = exec_shell(usbrelay_cmd)["error"]
            if res == "":
                logger.info("usbrelay cmd success")
            else:
                logger.error("usbrelay cmd res is {}, ----- run failed".format(res))
        else:
            logger.error("No usbrelay is found, and the cmd does not run")

    def usbrelay_cmd_close(self, ur):
        usbrelay_port = None
        if self.usbrelay_map:
            usbrelay_port = self.usbrelay_map.get(ur)
        if usbrelay_port:
            self.usbrelay_cmd(usbrelay_port, 0)
            logger.info(
                "==============  usbrelay_cmd: {} NC   =============================".format(
                    ur
                )
            )

    def usbrelay_cmd_open(self, ur):
        usbrelay_port = None
        if self.usbrelay_map:
            usbrelay_port = self.usbrelay_map.get(ur)
        if usbrelay_port:
            self.usbrelay_cmd(usbrelay_port, 1)
            logger.info(
                "==============  usbrelay_cmd: {} NO   =============================".format(
                    ur
                )
            )

    def get_announcement_ip(self):
        retry_times = 20
        while retry_times > 0:
            if self.eth_obd:
                # request_vid(self.eth_obd_nuc_ip)
                # pack = sniff(iface=self.eth_obd, filter='port 13400', count=1, timeout=10)
                sniffer = AsyncSniffer(
                    iface=self.eth_obd, filter='udp port 13400', timeout=10
                )
                sniffer.start()
                sleep(0.5)
                request_vid(self.eth_obd_nuc_ip)
                sleep(1)
                try:
                    pack = sniffer.stop()
                except Scapy_Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/nuc_app.py")
                    logger.error(f'{str(e)}, retry times: {retry_times}')
                    retry_times -= 1
                    continue
            else:
                obd_iface = get_obd_iface()
                logger.info("INFO -- obd_iface is {}".format(obd_iface))
                # request_vid(self.eth_obd_nuc_ip)
                # pack = sniff(iface=obd_iface, filter='port 13400', count=1, timeout=10)
                sniffer = AsyncSniffer(iface=obd_iface, filter='udp port 13400', timeout=10)
                sniffer.start()
                sleep(0.5)
                request_vid(self.eth_obd_nuc_ip)
                sleep(1)
                try:
                    pack = sniffer.stop()
                except Scapy_Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/nuc_app.py")
                    retry_times -= 1
                    logger.error(f'{str(e)}, retry times: {retry_times}')
                    continue

                # pack = sniff(iface=obd_iface, filter='port 13400', count=1, timeout=10, prn=printnow)
            # wrpcap('xxx.pcap', pack)
            # pcaps = rdpcap("xxx.pcap")
            if pack:
                for packet in pack:
                    if "169.254" in packet['IP'].src:
                        # logger.info(packet.show())
                        if list(packet['Raw'].load)[:4] == [0x02, 0xFD, 0x00, 0x04]:
                            logger.info(
                                "get_announcement_ip is {}".format(packet['IP'].src)
                            )
                            return packet['IP'].src
                    else:
                        logger.error("obd ip not match , ip {}".format(packet['IP'].src))
                retry_times -= 1
                logger.error(f'not got announcement_ip, retry times: {retry_times}')
            else:
                retry_times -= 1
                logger.warning(f"not got announcement_ip, retry times: {retry_times}")
                continue
        logger.warning('obd ip获取异常请检查环境')

    # -------------------------------------------------------------------------------------------------------------------

    def start_nuc_odb_tcpdump(self, save_path: str="./nuc_log") -> Path:
        """
        功能说明：
            抓取上位机odb网卡的网络数据包
        参数说明：
            param: save_path 指定需要保存的路径，默认存放在/root/nuc_log下 
        异常说明：无
        返回值：Path  抓包文件存放路径
        """
        odb_iface = get_obd_iface()
        return self.start_nuc_tcpdump(odb_iface, save_path)

    def start_nuc_tcpdump(self, interface: str="any", save_path: str="./nuc_log") -> Path:
        """
        功能说明：
            抓取上位机网络数据包
        参数说明：
            param: interface 指定需要抓取的网卡名称，默认抓取所有网口
            param: save_path 指定需要保存的路径，默认存放在/root/nuc_log下
        异常说明：无
        返回值：Path  抓包文件存放路径
        """
        floder = Path(save_path)
        if not floder.exists():
            floder.mkdir(parents=True)
        file_name = f"{time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime())}.pcap"
        save_path = Path(save_path, file_name)
        cmd = f"tcpdump -i {interface} -w {save_path}"
        logger.info(f"开始抓取NUC {interface} 网卡的网络数据包，文件存放路径：{save_path}")
        thread = threading.Thread(target=lambda: subprocess.call(cmd, shell=True))
        thread.setDaemon(True)
        thread.start()
        return str(save_path)

    def stop_nuc_tcpdump(self, time_wait: int=2) -> None:
        """
        功能说明：
            停止抓取上位机网络数据包
        参数说明：
            param: time_wait 为防止用例结束有的包丢失所设置的等待时间，默认2秒
        异常说明：无
        返回值：None
        """
        time.sleep(time_wait)
        exec_shell("killall tcpdump")
        logger.info("已停止nuc网络数据抓包")

    def check_nuc_tcpdump(self,
                        pcap_file: str,
                        target_ip: str,
                        interval: int,
                        data_to_check: str=None,
                        count: int=None) -> bool:
        """
        功能说明：
            用于检查目标IP地址是否每interval秒内都至少响应一次，并检查数据包内容是否包含特定数据
        参数说明：
            param: pcap_file 抓包后的pcap文件
            param: target_ip 目标ip
            param: interval 监测周期，多少秒内出现一次
            param: data_to_check 需要监测到的数据，不传时只监测目标ip出现频率
        异常说明：无
        返回值：True/False
        """
        packets = rdpcap(pcap_file)
        last_response_time = None
        appear_count = 0
        for packet in packets:
            if IP in packet and packet[IP].src == target_ip:
                current_time = packet.time
                if last_response_time is None:
                    last_response_time = current_time
                if data_to_check:
                    if packet.haslayer(Raw):
                        packet_data = packet[Raw].load.decode('utf-8', errors='ignore')
                        if data_to_check in packet_data:
                            time_diff = current_time - last_response_time
                            last_response_time = current_time
                            appear_count += 1
                            if time_diff > interval: 
                                return False
                else:
                    time_diff = current_time - last_response_time
                    last_response_time = current_time
                    appear_count += 1
                    if time_diff > interval: 
                        return False
        if count is not None:
            if appear_count != count:
                logger.warning(f"与预期想得到得响应次数不符合， 预期响应{count}， 实际响应{appear_count}")
                return False
        return True if last_response_time else False


def request_vid(obd_nuc_ip="169.254.1.200"):
    if obd_nuc_ip:
        doip_client = Doip_Client_Sim_Odx(obd_nuc_ip=obd_nuc_ip)
    else:
        doip_client = Doip_Client_Sim_Odx(obd_nuc_ip="169.254.1.200")
    doip_client.vid_request()


def get_obd_iface():
    global OBDETH
    if os.name == "nt":
        logger.info("操作系统是windows")
        res = exec_shell("ipconfig")
        sleep(0.5)
        res_str = res["output"]
        res_list = res_str.split("\n")

        data = ""
        obd_iface = ""
        for i in res_list:
            if "169.254" in i:
                data = res_list[res_list.index(i) - 4]
                regular = re.findall(r" (.+?):", data)
        obd_iface = "".join(regular)
        return obd_iface
    else:
        logger.info("操作系统是linux")
        if OBDETH == "":
            # res = os.popen("ifconfig")
            # # res_str = res.buffer.read().decode('utf-8')  # 有时获取不到消息
            # res_str = res.read()  # 某些电脑报编码错误
            # res.close()
            p = Popen(["ifconfig"], stdout=subprocess.PIPE)  # 还是有时获取不到值
            res_str = p.stdout.read().decode()

            # res = p.communicate()  # 目前会导致下一次获取不到值
            # res_str = res[0].decode(encoding="utf-8")

            logger.debug("res_str:{}".format(res_str))

            res_list = res_str.split("\n")

            data = ""
            obd_iface = ""
            for i in res_list:
                if "inet 169.254" in i:
                    obd_iface = data.split(":")[0]
                data = i
            if obd_iface:
                OBDETH = obd_iface
        return OBDETH


def get_nuc_wifi_ip():
    # 操作系统是linux
    res = exec_shell("ifconfig")
    res_str = res["output"]
    res_list = res_str.split("\n")

    data = ""
    nuc_wifi_ip = ""
    for i in res_list:
        if data:
            result = re.search(r"inet(.+)netmask", i)
            if result:
                nuc_wifi_ip = result.group(1).strip()
                logger.info("获取到的nuc_wifi_ip is {}".format(nuc_wifi_ip))
                return nuc_wifi_ip
            else:
                logger.error("获取 nuc_wifi_ip 错误， result is {}".format(result))
        if "wl" in i:
            data = i
            logger.info("匹配到的wifi信息为 {}".format(data))
    return nuc_wifi_ip


def get_obd_ip(obd_eth=None, obd_nuc_ip=None):
    retry_times = 20
    while retry_times > 0:
        if obd_eth:
            # request_vid(obd_nuc_ip)
            # pack = sniff(iface=obd_eth, filter='port 13400', count=1, timeout=10)   阻塞型
            # 非阻塞型
            sniffer = AsyncSniffer(iface=obd_eth, filter='udp port 13400', timeout=10)
            sniffer.start()
            sleep(0.5)
            request_vid(obd_nuc_ip)
            sleep(1)
            try:
                pack = sniffer.stop()
            except Scapy_Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/nuc_app.py")
                retry_times -= 1
                logger.error(f'{str(e)}, retry times:{retry_times}')
                continue
        else:
            obd_iface = get_obd_iface()
            logger.info("INFO -- obd_iface is {}".format(obd_iface))
            # request_vid(obd_nuc_ip)
            # pack = sniff(iface=obd_iface, filter='port 13400', count=1, timeout=10)
            sniffer = AsyncSniffer(iface=obd_iface, filter='udp port 13400', timeout=10)
            sniffer.start()
            sleep(0.5)
            request_vid(obd_nuc_ip)
            sleep(1)
            try:
                pack = sniffer.stop()
            except Scapy_Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/nuc_app.py")
                retry_times -= 1
                logger.error(f'{str(e)}, retry times:{retry_times}')
                continue

        if pack:
            for packet in pack:
                if "169.254" in packet['IP'].src:
                    # logger.info(packet.show())
                    if list(packet['Raw'].load)[:4] == [0x02, 0xFD, 0x00, 0x04]:
                        logger.info("get_announcement_ip is {}".format(packet['IP'].src))
                        return packet['IP'].src
                else:
                    logger.error("obd ip not match , ip {}".format(packet['IP'].src))
            retry_times -= 1
            logger.warning(f"not got announcement_ip, retry times:{retry_times}")
        else:
            retry_times -= 1
            logger.warning(f"not got announcement_ip, retry times:{retry_times}")
            continue
    logger.warning('obd ip获取异常请检查环境')


def setup_vlan(iface='enx207bd2765e50', domin="acu"):
    """
    配置台架环境的vlan
    :param iface: 台架网卡名称
    :param domin: 网卡连接的以太网线所在域控，默认acu
    :return:
    """

    def os_cmd(cmd):
        logger.info(cmd)
        # os.system(cmd)
        exec_shell(cmd)

    if iface is None:
        logger.info("Error: 当前台架未配置radmoon网卡名")
        return
    res = exec_shell("ifconfig")
    domin_map = {"acu": 21, "tcam": 31, "cdcq": 11}
    if domin not in domin_map:
        logger.error("配置信息partner_domin不正确，应当为acu/tcam/cdc")
        raise Exception("配置信息partner_domin不正确，应当为acu/tcam/cdc")
    domin_id = domin_map[domin]
    res_str = res["output"]
    if res_str.find(iface) == -1:
        logger.error(f"Error: 当前台架无{iface}的网卡")
        raise Exception(f"Error: 当前台架无{iface}的网卡")
    for ip in ['172.16.9.222', f'172.16.21.{domin_id}', f'172.16.22.{domin_id}', f'172.16.5.{domin_id}']:
        if res_str.find(ip) == -1:
            vlan = ip.split('.')[2]
            if res_str.find(f'eth0.{vlan}') and vlan != 9:
                os_cmd(f'ip link delete eth0.{vlan}')
            logger.info(f"配置{vlan}.{domin_id}")
            os_cmd(f'ip link add link {iface} name eth0.{vlan} type vlan id {vlan}')
            os_cmd(f'ip addr add {ip}/24 dev eth0.{vlan}')
            os_cmd(f'ip link set dev eth0.{vlan} address 02:00:00:00:10:{domin_id}')
            os_cmd(f'ifconfig eth0.{vlan} up')


def printnow(packet):
    logger.info(packet)
    # logger.info("get_announcement_ip is {}".format(packet['IP'].src))


def exec_shell(command):
    '''
    输入指令，获取返回结果
    @param command:
    @return:
    '''
    process = None
    try:
        # 执行命令
        logger.info(f"开始执行cmd={command}")
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        # 等待命令执行完成
        stdout, stderr = process.communicate()
        # 将输出和错误信息解码为字符串
        output = stdout.decode(encoding="utf-8")
        error = stderr.decode(encoding="utf-8")
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/nuc_app.py")
        output = ""
        error = str(e)
    finally:
        if process:
            process.terminate()
            process.kill()
    # 返回命令的输出和错误信息
    logger.info(f"执行cmd={command} 结束")
    result = {"output": output, "error": error}
    logger.debug(result)
    return result


def get_willow_file_path(**kwargs):
    '''
    获取 最近的 willow 文件
    @return:
    '''
    if not ("willow" in current_path.lower() or "testdev" in current_path.lower()):
        return None
    save_num = kwargs.get("save_num", 20)
    # 存放 willow_log 的路径
    willow_log_path = kwargs.get("willow_log_path", "/root/autotest/willow/")
    willow_log_filename_len = kwargs.get("willow_log_filename_len", 36)
    # 查找文件
    cmd = f"cd {willow_log_path};ls -lrt"
    result = exec_shell(cmd)
    data = result["output"]
    error = result["error"]
    try:
        if data:
            output_lis = data.split("\n")
            name_list = [na.split(' ')[-1] for na in output_lis[1:]]
            name_list = [i for i in name_list if i.strip()]
            name_list.reverse()
            logger.info(f"len={len(name_list)} name_list={name_list}")
            # 需要保留的 日志
            save_log_list = []
            for namestr in name_list:
                if "distributed" in namestr:
                    save_log_list.append(namestr)
                if namestr.endswith('zip'):
                    continue
                if len(save_log_list) >= save_num:
                    break
                save_log_list.append(namestr)
            logger.info(f"删除多余文件保留最近修改的{save_num}个文件==》{save_log_list}")
            # 删除 文件
            for del_name in name_list:
                if del_name in save_log_list:
                    continue
                path = os.path.join(willow_log_path, del_name)
                logger.info(f"删除的文件为 path={path}")
                cmd = f"rm -rf {path}"
                # os.system(cmd)
                exec_shell(cmd)
            # 返回最新文件
            if "testdev" in current_path.lower():
                willow_file_lis = [
                    namestr
                    for namestr in name_list
                    if len(namestr) == willow_log_filename_len
                ]
                path = os.path.join(willow_log_path, willow_file_lis[0])
                logger.info(f"获取到最新的文件夹path为{path}")
                return path
            # 返回当前路径
            if "willow" in current_path.lower():
                path = os.path.dirname(current_path)
                logger.info(f"获取当前willow运行路径{path}")
                return path
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/nuc_app.py")
        logger.error(f"未找到最新 willow 文件 {str(e)}")
    logger.error(f"未找到最新 willow 文件{error}")
    return None


# ============================    环境类    ======================================
def partner_process_check():
    """
    检查上位机上是否有其它未关闭的soa_partner进程在运行，如果有，则杀死进程
    """
    check_cmd = f"ps -ef | grep soa_partner | grep -v grep"
    pi = subprocess.Popen(
        check_cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding='utf-8',
    )
    stdout = pi.stdout.read()
    if stdout:
        logger.info("命令执行结果：\n{}".format(stdout))
        stdout = stdout.split('\n')
        pid_list = []
        for s in stdout:
            if s:
                s = ' '.join(s.split())  # 合并连续的空格
                s = s.split(' ')
                pid_list.append(s[1])
        if len(pid_list):
            kill_pid_str = ''
            for pid in pid_list:
                kill_pid_str += pid
                kill_pid_str += ' '
            check_cmd = f"kill -9 {kill_pid_str}"
            pi = subprocess.Popen(
                check_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                encoding='utf-8',
            )
            time.sleep(1)
            stdout = pi.stdout.read()
            if stdout:
                logger.info("error: {}".format(stdout))
                logger.info("process kill fail")
                time.sleep(1)
                return False
            else:
                logger.info("process kill success")
                time.sleep(1)
                return True
    else:
        # logger.info("没有残留的soa partner 进程")
        return True


def defunc_process_check():
    """
    检查上位机上是否有其它未关闭的defunc进程在运行，如果有，则重载进程
    """
    check_cmd = f"ps -ef | grep defunc | grep -v grep"
    pi = subprocess.Popen(
        check_cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding='utf-8',
    )
    stdout = pi.stdout.read()
    if stdout:
        logger.info("命令执行结果：\n{}".format(stdout))
        stdout = stdout.split('\n')
        pid_list = []
        for s in stdout:
            if s:
                s = ' '.join(s.split())  # 合并连续的空格
                s = s.split(' ')
                pid_list.append(s[1])
        if len(pid_list):
            kill_pid_str = ''
            for pid in pid_list:
                kill_pid_str += pid
                kill_pid_str += ' '
            check_cmd = f"kill -HUP {kill_pid_str}"
            pi = subprocess.Popen(
                check_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                encoding='utf-8',
            )
            time.sleep(1)
            stdout = pi.stdout.read()
            if stdout:
                logger.info("error: {}".format(stdout))
                logger.info("process kill fail")
                time.sleep(1)
                return False
            else:
                logger.info("process kill success")
                time.sleep(1)
                return True
    else:
        # logger.info("没有残留的 僵尸 进程")
        return True

def process_check(key_str: str):
    """
    检查上位机上是否有其它未关闭的key_str相关的进程在运行，如果有，则重载进程
    """
    check_cmd = f"ps -ef | grep {key_str} | grep -v grep"
    pi = subprocess.Popen(
        check_cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding='utf-8',
    )
    stdout = pi.stdout.read()
    if stdout:
        logger.info("命令执行结果：\n{}".format(stdout))
        stdout = stdout.split('\n')
        pid_list = []
        for s in stdout:
            if s:
                s = ' '.join(s.split())  # 合并连续的空格
                s = s.split(' ')
                pid_list.append(s[1])
        if len(pid_list):
            kill_pid_str = ''
            for pid in pid_list:
                kill_pid_str += pid
                kill_pid_str += ' '
            check_cmd = f"kill -HUP {kill_pid_str}"
            pi = subprocess.Popen(
                check_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                encoding='utf-8',
            )
            time.sleep(1)
            stdout = pi.stdout.read()
            if stdout:
                logger.info("error: {}".format(stdout))
                logger.info("process kill fail")
                time.sleep(1)
                return False
            else:
                logger.info("process kill success")
                time.sleep(1)
                return True
    else:
        # logger.info("没有残留的 {key_str} 进程")
        return True

def jetsoa_env_check():
    """
    检查上位机上是否有其它未关闭的jetsoa_env相关的进程在运行，如果有，则重载进程
    :return:
    """
    process_check("export")


def tcam_time_sync(iface='enp89s0', timeout=5):
    """
    TCAM单域时间同步
    :param iface: 网卡
    :param timeout: 命令执行时间，超时之后会kill掉
    :return:
    """
    command = f"ptp4l -i {iface} -m -f {Path(parent_dir) / 'interface/automotive-master.cfg'} -S"
    process = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)

    start_time = time.time()
    while time.time() - start_time < timeout:
        # 检查命令的状态
        if process.poll() is None:
            # 执行其他操作，或者等待一段时间
            time.sleep(1)
        else:
            break

    # 检查返回状态码
    if not process.returncode:
        logger.info("命令执行成功")
        process.terminate()
        exec_shell("ps -ef  | grep ptp4l | grep -v grep | awk '{print $2}' | xargs kill -9")
    else:
        err_msg = f"命令执行失败，原因是:{process.stderr.read().decode()}"
        logger.error(err_msg)
        raise exception_error.CmdExecuteError(err_msg)


if __name__ == "__main__":
    # work dir: sat/
    # cmd: python3  ecu_simulator/interface/nuc_app.py

    logger = Logger().get_logger("test")
    # nucapp = NucApp()
    # nucapp.bgm_power_off()
    # sleep(2)
    # nucapp.bgm_power_on()
    # sleep(5)
    # nucapp.get_announcement_ip()
    # get_obd_ip(obd_eth="enx000ec629a465")
    # get_obd_ip()
    # defunc_process_check()
    tcam_time_sync()
    # jy_dam_port1 = get_jy_dam_port()
    #
    # if sys.argv[2] == "1":
    #     action = "open"
    # else:
    #     action = "close"
    #
    # jy_dam0800_operation(f"COM" + sys.argv[1], action, jy_dam_port1)
