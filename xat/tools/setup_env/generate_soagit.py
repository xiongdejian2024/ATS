# -*- coding: utf-8 -*-
"""
@File        : generate_soagit.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022/09/26 18:00 PM
@Description : description about this file
@Examples    : example of how to use it
"""

from cmath import log
import os
import sys

import socket
import netifaces

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path, ".."))
sys.path.append(os.path.join(current_path, "../.."))
sys.path.append(os.path.join(current_path, "../../.."))
import subprocess
from subprocess import Popen
from xat_ecu.legacy.common.file_handle import *
from xat_ecu.legacy.common.logger import *
from xat_ecu.legacy.common.file_handle import FileHandle
from time import sleep
import json

bootes_flag = True
artifactory_base_path = 'https://repo.jidudev.com/artifactory/SOASDK/SoaAutoTestPackages'
ARTIFACTORY_USERNAME = "sunquan_onwner"
ARTIFACTORY_PASSWORD = __import__("os").environ.get('XAT_CREDENTIAL____SETUP_ENV_GENERATE_SOAGIT_PY_ARTIFACTORY_PASSWORD', "")
soazip_name = 'soa.zip'
ignore_ip = '172.18.128.5'


def update_soagit(JIDLCompiler, X86_value, idl):
    # update soagit
    if bootes_flag:
        update_soagit_cmd = os.path.join(parent_dir, "tools/setup_env/update_soagit_bootes.sh")
    else:
        update_soagit_cmd = os.path.join(parent_dir, "tools/setup_env/update_soagit.sh")
    update_soagit_cmd = update_soagit_cmd + " " + JIDLCompiler + " " + X86_value + " " + idl
    logger.info("update_soagit cmd: {}".format(update_soagit_cmd))
    res = os.system(update_soagit_cmd)
    if res == 0:
        logger.info("update_soagit_cmd success")
    else:
        logger.error("update_soagit_cmd res is {}, ----- run failed".format(res))


def makezipmv_soa(soa_path):
    # make soa, zip soa, mv soa
    if bootes_flag:
        makezipmv_soa_cmd = os.path.join(parent_dir, "tools/setup_env/makezipmv_soa_bootes.sh")
    else:
        makezipmv_soa_cmd = os.path.join(parent_dir, "tools/setup_env/makezipmv_soa.sh")
    logger.info("makezipmv_soa cmd: {}".format(makezipmv_soa_cmd))
    makezipmv_soa_cmd = makezipmv_soa_cmd + " " + soa_path

    retry = 0
    retry_max = 1
    while retry <= retry_max:
        res = os.system(makezipmv_soa_cmd)
        if res == 0:
            retry = 100
            logger.info("makezipmv_soa_cmd success")
        else:
            retry += 1
            if retry > retry_max:
                logger.error("makezipmv_soa_cmd res is {}, ----- run failed".format(res))
                raise RecursionError("makezipmv_soa_cmd run failed")
            else:
                logger.warning("makezipmv_soa_cmd res is {}, ----- run failed , retry {} ... ".format(res, retry))


def get_soa_name():
    # get soa path
    if os.path.exists("/root/soagit/task.json"):
        with open("../task.json", "r") as f:
            task = json.load(f)

            JIDLCompiler = task.get("JIDLCompiler")
            logger.info("JIDLCompiler: {}".format(JIDLCompiler))

            X86_value = task.get("X86")
            logger.info("X86: {}".format(X86_value))
            if "apus" in X86_value:
                global bootes_flag
                bootes_flag = False

            idl = task.get("idl")
            logger.info("idl: {}".format(idl))
            soa_name = "SOA_" + JIDLCompiler + X86_value + idl
            soa_name = soa_name.replace(".", "_")
        return soa_name, JIDLCompiler, X86_value, idl


def add_soazip(soa_name, JIDLCompiler, X86_value, idl):
    # add soazip
    soazip_rootpath = "/root/soazip/"
    exist_soas = FileHandle.get_subdir_names_from_dir(soazip_rootpath)
    if soa_name is None:
        logger.error("task.json is non-existent, soa_name is None , can not compile")
        raise RuntimeError("task.json is non-existent")
    elif soa_name in exist_soas:
        logger.info("Same SOA version, no need to compile")
    else:
        logger.info("SOA version is different, start to update and compile ...")

        logger.info("删除 SOA out文件夹")
        soa_outdir_path = os.path.join(parent_dir, "ecu_simulator/soa_partner/BootesRelease/out/")
        rm_soa_cmd = "rm -rf " + soa_outdir_path
        res = os.system(rm_soa_cmd)

        update_soagit(JIDLCompiler, X86_value, idl)
        soazip_dir_path = os.path.join(soazip_rootpath, soa_name)
        os.makedirs(soazip_dir_path)
        with open("/root/soazip/soazipconf.json", "r+") as f:
            soazipconf = json.load(f)
            f.seek(0)
            f.truncate()
            soazipconf[soa_name] = "Installing"
            json.dump(soazipconf, f, indent=4)

        soazip_path = os.path.join(soazip_dir_path, "soa.zip")
        makezipmv_soa(soazip_path)
        logger.info("====>>>>  compile fished, soazip_dir_path is {}".format(soazip_path))
        if not check_ip_exist(ignore_ip):
            upload_soazip_to_artifactory(soa_name, soazip_name)
            upload_soazip_config_to_artifactory()
        with open("/root/soazip/soazipconf.json", "r+") as f:
            soazipconf = json.load(f)

            f.seek(0)
            f.truncate()

            soazipconf["new_version"] = soa_name
            soazipconf[soa_name] = "Finish"
            json.dump(soazipconf, f, indent=4)
        logger.info("====  Write soazip config finished  ======")


def upload_soazip_to_artifactory(soa_name, soazip_name):
    logger.info("upload to artifactory")
    cmd = f'curl -u {ARTIFACTORY_USERNAME}:{ARTIFACTORY_PASSWORD} -X PUT "{artifactory_base_path}/{soa_name}/{soazip_name}" -T /root/soazip/{soa_name}/{soazip_name}'
    res = os.system(cmd)
    if res == 0:
        logger.info(f"====>>>>  upload fished, artifactory path is {artifactory_base_path}/{soa_name}/{soazip_name}")
    else:
        logger.error(f"upload {artifactory_base_path}/{soa_name}/{soazip_name} failed")
        raise Exception(f"upload {artifactory_base_path}/{soa_name}/{soazip_name} failed")


def upload_soazip_config_to_artifactory():
    logger.info("upload soazip config to artifactory")
    cmd = f'curl -u {ARTIFACTORY_USERNAME}:{ARTIFACTORY_PASSWORD} -X PUT "{artifactory_base_path}/soazipconf.json" -T /root/soazip/soazipconf.json'
    res = os.system(cmd)
    if res == 0:
        logger.info(f"====>>>>  upload fished, artifactory path is {artifactory_base_path}/soazipconf.json")
    else:
        logger.error(f"upload {artifactory_base_path}/soazipconf.json failed")
        raise Exception(f"upload {artifactory_base_path}/soazipconf.json failed")


def get_ip_addresses():
    ip_addresses = []
    # 获取所有网络接口
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        # 获取接口的IP地址信息
        addresses = netifaces.ifaddresses(interface)
        for family, addresses in addresses.items():
            # 获取IPv4和IPv6地址
            if family in (socket.AF_INET, socket.AF_INET6):
                for address_info in addresses:
                    ip = address_info.get('addr')
                    if ip and ip != '127.0.0.1':
                        ip_addresses.append(ip)
    return ip_addresses


def check_ip_exist(ignore_ip):
    if isinstance(ignore_ip, str):
        ignore_ip = [ignore_ip]
    ip_addresses_list = get_ip_addresses()
    for ip in ignore_ip:
        if ip in ip_addresses_list:
            return True


if __name__ == "__main__":
    # work dir: sat/
    # cmd: python3 tools/setup_env/generate_soagit.py
    logger = Logger().get_logger("test")

    soa_name, JIDLCompiler, X86_value, idl = get_soa_name()
    add_soazip(soa_name, JIDLCompiler, X86_value, idl)
