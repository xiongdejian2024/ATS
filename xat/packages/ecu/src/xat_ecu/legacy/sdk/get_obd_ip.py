# -*- coding: utf-8 -*-
"""
@File        : get_obd_ip.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022/12/27 09:49
@Description : description about this file
@Examples    : 
"""

import sys
import os
import time

from xat_ecu.legacy.common.logger import *
from time import sleep
from scapy.all import *
from xat_ecu.legacy.sdk.ethernet import doip_client_sim_odx
import subprocess
from subprocess import Popen

global OBD_ETH
OBD_ETH = ""
global OBD_ETH_IP
OBD_ETH_IP = ""


def request_vid(obd_nuc_ip="169.254.1.200"):
    if obd_nuc_ip:
        doip_client = doip_client_sim_odx.Doip_Client_Sim_Odx(obd_nuc_ip=obd_nuc_ip)
    else:
        doip_client = doip_client_sim_odx.Doip_Client_Sim_Odx(obd_nuc_ip="169.254.1.200")
    doip_client.vid_request()


def get_obd_iface():
    global OBD_ETH
    global OBD_ETH_IP
    if OBD_ETH == "":
        # res = os.popen("ifconfig")
        # # res_str = res.buffer.read().decode('utf-8')  # 有时获取不到消息
        # res_str = res.read()  # 某些电脑报编码错误
        # res.close()
        p = Popen(["ifconfig"], stdout=subprocess.PIPE)  # 还是有时获取不到值
        res_str = p.stdout.read().decode()

        # res = p.communicate()  # 目前会导致下一次获取不到值
        # res_str = res[0].decode(encoding="utf-8")

        # logger.info("res_str:{}".format(res_str))

        res_list = res_str.split("\n")

        data = ""
        obd_iface = ""
        for i in res_list:
            if "inet 169.254" in i:
                obd_iface = data.split(":")[0]
                if obd_iface:
                    OBD_ETH = obd_iface
                    logger.info(f"上位机 OBD 网卡名 is {OBD_ETH}")

                i_list = i.split()
                for j in i_list:
                    if "169.254" in j:
                        OBD_ETH_IP = j  # 上位机 OBD IP
                        logger.info(f"上位机 OBD IP is {OBD_ETH_IP}")
                        break
            data = i
    return OBD_ETH, OBD_ETH_IP


def get_announcement_ip(obd_eth=None, obd_nuc_ip=None, auto=True):
    if auto:
        obd_iface, obd_nuc_ip = get_obd_iface()
        # print("obd_iface is {}".format(obd_iface))
        # logger.info("INFO -- obd_iface is {}".format(obd_iface))
        logger.info(f"obd接口是：{obd_iface}")
        # request_vid(obd_nuc_ip)
        # pack = sniff(iface=obd_iface, filter='dst port 13400', count=1, timeout=10)
        sniffer = AsyncSniffer(iface=obd_iface, filter='udp port 13400', timeout=10)
        sniffer.start()
        sleep(0.5)
        request_vid(obd_nuc_ip)
        sleep(1)
        pack = sniffer.stop()
    else:  # obd_eth 和 obd_nuc_ip 需要传正确的值
        # request_vid(obd_nuc_ip)
        # pack = sniff(iface=obd_eth, filter='dst port 13400', count=1, timeout=10)   阻塞型
        # 非阻塞型
        sniffer = AsyncSniffer(iface=obd_eth, filter='udp port 13400', timeout=10)
        sniffer.start()
        sleep(0.5)
        request_vid(obd_nuc_ip)
        sleep(1)
        pack = sniffer.stop()

    if pack:
        for packet in pack:
            if "169.254" in packet['IP'].src:
                # logger.info(packet.show())
                if list(packet['Raw'].load)[:4] == [0x02, 0xFD, 0x00, 0x04]:
                    # logger.info("get_announcement_ip is {}".format(packet['IP'].src))
                    logger.info(f"获取到OBD网关IP是：{packet['IP'].src}")
                    return packet['IP'].src
            else:
                # logger.error("obd ip not match , ip {}".format(packet['IP'].src))
                logger.warning("获取到obd的网关ip不匹配，得到 {}".format(packet['IP'].src))
    else:
        # logger.warning("not got announcement_ip")
        logger.warning("没有发现OBD网关IP")


if __name__ == "__main__":
    # logger = Logger().get_logger("test")
    get_announcement_ip()
