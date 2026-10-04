#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :bench_helper.py
@time         :2/8/24 17:14
@author       :dejian.xiong@jiduauto.com
@description  :
"""
import copy
import json
import os
import re
import threading
import time
from pathlib import Path
from framework.automotive.core.resources import REPOSITORY_ROOT, package_version, clone_command, install_command
from typing import Union, Dict

import pytest
from xat_ecu.legacy.common import exception_error
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.parse_tb_config import ParseTBConfig
from xat_ecu.legacy.common.parse_tc_config import ParseTCConfig
from xat_ecu.legacy.driver.ssh_interface import command_send, close_command, SshClient, ScpClient
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.interface.cd_soc.cd_soc_ssh import CD_SOC_SSH
from xat_ecu.legacy.interface.nuc_app import get_nuc_wifi_ip, setup_vlan, tcam_time_sync, exec_shell
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH

from framework.automotive.utils.artifactory_helper import ArtifactoryHelper
from framework.automotive.utils.conftest_helper import parent_dir, get_bgm_diag_info, get_tcam_diag_info, get_cdc_diag_info, \
    get_acu_diag_info, timestamp_to_datetime_full_millis
from framework.automotive.utils.data_type import Domain, EnvPropertiesInfo, CustomParameters, EcuInfo, BenchStatus, \
    CaseProgress, BenchConfig, HeartBeat, RepoName
from framework.automotive.utils.database_helper import DatabaseHelper

WORKSPACE = Path('/root/willow/distributed')
RETRY_COUNT = 10  # 失败重连次数


class BenchHelper:
    def __init__(self):
        self._case_progress: Union[CaseProgress, None] = None
        self.bgm_diag_info = {}
        self.tcam_diag_info = {}
        self.cdc_diag_info = {}
        self.acu_diag_info = {}
        self.ccu_cd_info = {}
        self.yaml_name = ''
        self.cache_env_path = '/root/env.json'
        self.cache_version_info = {}
        self._bench_status: Dict[str, BenchStatus] = {}
        self._bench_heart_beat_status: Union[None, HeartBeat] = None
        self.task_json = self.get_task_json()

    def get_cache_diag_info(self):
        if os.path.exists(self.cache_env_path):
            with open(self.cache_env_path) as json_obj:
                cache_info = json.load(json_obj)
            self.cache_version_info = cache_info
            return self.cache_version_info

    def set_cache_diag_info(self, diag_info):
        with open(self.cache_env_path, 'w', encoding='utf-8') as json_obj:
            json.dump(diag_info, json_obj, indent=4, ensure_ascii=False)

    def get_tbcfg(self, tbcfg: str):
        if tbcfg == '':
            nuc_wifi_ip = get_nuc_wifi_ip()
            tbs_mapping_path = os.path.join(parent_dir, "bench_config/benches_mapping.yaml")
            tbs_mapping = ParseTBConfig(tbs_mapping_path)
            ip_benchconfig = tbs_mapping.yaml_content.get("ip_benchconfig")
            benchconfig = ip_benchconfig.get(nuc_wifi_ip)
            if benchconfig:
                tbcfg = os.path.join(parent_dir, "bench_config/" + benchconfig)
                self.yaml_name = benchconfig
                logger.info("根据nuc_wifi_ip {} 自动匹配到台架配置为 {}".format(nuc_wifi_ip, tbcfg))
                tbcfg_content = ParseTBConfig(tbcfg).yaml_content
                tbcfg_content['wifi_localhost'] = nuc_wifi_ip
                return tbcfg_content
            else:
                raise exception_error.ConfigError("未获取到 benchconfig")
        else:
            self.yaml_name = tbcfg
            tbcfg = os.path.join(parent_dir, "bench_config/" + tbcfg)
            return ParseTCConfig(tbcfg).yaml_content

    @staticmethod
    def _get_tbcfg_by_ip(ip):
        tbs_mapping_path = os.path.join(parent_dir, "bench_config/benches_mapping.yaml")
        tbs_mapping = ParseTBConfig(tbs_mapping_path)
        ip_benchconfig = tbs_mapping.yaml_content.get("ip_benchconfig")
        benchconfig = ip_benchconfig.get(ip)
        if benchconfig:
            tbcfg = os.path.join(parent_dir, "bench_config/" + benchconfig)
            return ParseTCConfig(tbcfg).yaml_content

    @staticmethod
    def get_tccfg(tccfg: str):
        return ParseTBConfig(tccfg).get_yaml()

    @staticmethod
    def clear_bench_log(coredump_save_days=180, allure_save_days=90, fail_case_log=7):
        """
        删除台架日志：coredump文件默认保存180天内的，allure日志文件默认保存30天内的，失败用例日志默认保留最近7天的
        """
        if os.path.exists("/var/core/"):
            res = os.system(f"find /var/core/ -type f -atime +{coredump_save_days} | xargs rm -rf")
            if res == 0:
                logger.info("成功删除180天以前的coredump文件。")
            else:
                logger.error("删除180天前的coredump文件失败：".format(res))
        else:
            logger.info("coredump 目录 /var/core/不存在，跳过删除coredump文件")

        if os.path.exists("/root/allure_report/"):
            res = os.system(f"find /root/allure_report/ -type d -ctime +{allure_save_days}| xargs rm -rf")
            if res == 0:
                logger.info("成功删除30天以前的allure日志文件。")
            else:
                logger.error("删除30天前的allure日志文件失败：".format(res))
        else:
            logger.info("allure 目录 /root/allure_report/不存在，跳过删除allure报告文件")

        if os.path.exists("/root/fail_case_log/"):
            res = os.system(f"find /root/fail_case_log/ -type d -ctime +{fail_case_log}| xargs rm -rf")
            if res == 0:
                logger.info(f"成功删除{fail_case_log}天以前的失败用例相关日志文件。")
            else:
                logger.error(f"删除{fail_case_log}天以前的失败用例相关日志失败：{res}")
        else:
            logger.info("失败用例日志 目录 /root/fail_case_log/不存在，跳过删除失败用例相关日志")

    @staticmethod
    def get_bench_domain_info(tb_config):
        dp1_bench_dict = {
            'single_bgm': {
                "type": ["BGM"],
                "desc": "当前为单域BGM台架"
            },
            'single_tcam': {
                "type": ["TCAM"],
                "desc": "当前为单域TCAM台架，无法获取obd ip"
            },
            'two_domain': {
                "type": ["BGM", "TCAM"],
                "desc": "当前为两域BGM和TCAM台架"
            },
            'four_domain': {
                "type": ["BGM", "TCAM", "CDC", "ACU"],
                "desc": "当前为四域台架环境，无法使用soa_partner和设置VLAN"
            },
            'bgm_cdc_acu': {
                "type": ["BGM", "CDC", "ACU"],
                "desc": "当前为三域BGM+CDC+ACU台架环境"
            },
            'bgm_tcam_acu': {
                "type": ["BGM", "TCAM", "ACU"],
                "desc": "当前为三域BGM+TCAM+ACU台架环境"
            },
            'bgm_tcam_cdc': {
                "type": ["BGM", "TCAM", "CDC"],
                "desc": "当前为三域BGM+TCAM+CDC台架环境"
            }
        }
        dp2_bench_dict = {
            "ccu_cd": {
                "type": ["CCU_CD"],
                "desc": "当前为CCU CD台架环境"
            },
            "ccu_cd_lcu": {
                "type": ["CCU_CD_LCU"],
                "desc": "当前为CCU CD, LCU台架环境"
            },
            "ccu_cd_ad": {
                "type": ["CCU_CD_AD"],
                "desc": "当前为CCU CD 和 AD台架环境"
            },
            "ccu_cd_ad_lcu": {
                "type": ["CCU_CD_AD_LCU"],
                "desc": "当前为CCU CD, CCU AD, LCU台架环境"
            },
            "lcu_l": {
                "type": ["LCU_L"],
                "desc": "当前为LCU_L"
            },
            "lcu_r": {
                "type": ["LCU_R"],
                "desc": "当前为LCU_R"
            },
        }
        bench_type_dict = {**dp1_bench_dict, **dp2_bench_dict}
        hardwares = tb_config.get('domain')
        if hardwares is None:
            err_msg = 'bench_config中缺少domain参数'
            logger.error(err_msg)
            raise exception_error.ConfigError(err_msg)

        for bench_type, domain_info in bench_type_dict.items():
            if domain_info.get("type") == hardwares:
                logger.info(f'{domain_info.get("desc")}')
                return Domain(**{f"{bench_type}": domain_info})
        else:
            dp2_err_msg = f"{[*list(dp2_bench_dict.keys())]}"
            err_msg = f'domain目前只支持["BGM"]、["TCAM"]、["BGM", "TCAM"]、["BGM", "TCAM", "CDC", "ACU"]、["BGM", "CDC", "ACU"]、["BGM", "TCAM", "ACU"]、["BGM", "TCAM", "CDC"]、{dp2_err_msg}这几种参数'
            logger.error(err_msg)
            raise exception_error.ConfigError(err_msg)

    def parse_get_env_info(
            self,
            domain_info: Domain,
            tb_config,
            tc_config,
            domain_version_info: EnvPropertiesInfo,
            willow_task_path
    ):
        # 单域BGM
        if domain_info.single_bgm:
            bgmssh = BGM_SSH()
            version_info = bgmssh.get_version()
            # self.bgm_diag_info = get_bgm_diag_info(**tc_config)
            version_release = version_info.get('version_release')
            if version_release is None:
                raise exception_error.CmdExecuteError(f"version_release is None")
            domain_version_info.software_version = dict(BGM=version_info.get('build_version'))
            domain_version_info.bootes_version = version_info.get('bootes_version')
            domain_version_info.IDL = version_info.get('jidl_version')
            domain_version_info.JIDLCompiler = version_info.get('bootes_version')
            domain_version_info.bgm_boot_version = self.bgm_diag_info.get('bgm_boot_version')
            domain_version_info.bgm_mcu_version = self.bgm_diag_info.get('bgm_mcu_version')
            domain_version_info.bgm_switch_version = self.bgm_diag_info.get('bgm_switch_version')
            domain_version_info.veh_type = tc_config.get('veh_type')
            domain_version_info.SDB = version_release
            domain_version_info.hardware_version = dict(BGM=self.bgm_diag_info.get('hardware_version'))
        # 单域TCAM
        elif domain_info.single_tcam:
            tcamssh = TCAM_SSH(connect_type='vlan')
            tcam_version_info = tcamssh.get_soa_jidl_name()
            version_release = tcam_version_info.get('build_version')
            if version_release is None:
                raise exception_error.CmdExecuteError(f"version_release is None")
            domain_version_info.IDL = tcam_version_info.get('jidl_version')
            domain_version_info.JIDLCompiler = tcam_version_info.get('bootes_version')
            domain_version_info.SDB = version_release
            self.tcam_diag_info = get_tcam_diag_info(**tc_config)
            domain_version_info.software_version = {'TCAM': tcam_version_info.get('build_version')}
            domain_version_info.hardware_version = dict(TCAM=self.tcam_diag_info.get('hardware_version'))
        # 两域BGM+TCAM
        elif domain_info.two_domain:
            try:
                setup_vlan(tb_config.get('eth_vlan'), tb_config.get('partner_domin', 'acu'))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bench_helper.py")
                err_msg = f'vlan设置出错，原因{str(e)}'
                logger.error(err_msg)
                raise exception_error.SetVlanError(err_msg)
            else:
                bgmssh = BGM_SSH()
                tcamssh = TCAM_SSH(connect_type='obd')
                version_info = bgmssh.get_version()
                self.tcam_diag_info = get_tcam_diag_info(**tc_config)
                version_release = version_info.get('version_release')
                if version_release is None:
                    raise exception_error.CmdExecuteError(f"version_release is None")
                BGM = version_info.get('build_version')
                domain_version_info.bootes_version = version_info.get('bootes_version')
                domain_version_info.bgm_boot_version = self.bgm_diag_info.get('bgm_boot_version')
                domain_version_info.bgm_mcu_version = self.bgm_diag_info.get('bgm_mcu_version')
                domain_version_info.bgm_switch_version = self.bgm_diag_info.get('bgm_switch_version')
                domain_version_info.IDL = version_info.get('jidl_version')
                domain_version_info.JIDLCompiler = version_info.get('bootes_version')
                domain_version_info.veh_type = tc_config.get('veh_type')
                domain_version_info.SDB = version_release
                domain_version_info.hardware_version = dict(
                    BGM=self.bgm_diag_info.get('hardware_version'),
                    TCAM=self.tcam_diag_info.get('hardware_version')
                )
                TCAM = tcamssh.get_soa_jidl_name().get('build_version')
                domain_version_info.software_version = dict(
                    BGM=BGM,
                    TCAM=TCAM
                )
        # 四域
        elif domain_info.four_domain:
            bgmssh = BGM_SSH(connect_type='obd')
            tcamssh = TCAM_SSH(connect_type='obd')
            version_info = bgmssh.get_version()
            self.tcam_diag_info = get_tcam_diag_info(**tc_config)
            self.cdc_diag_info = get_cdc_diag_info(**tc_config)
            self.acu_diag_info = get_acu_diag_info(**tc_config)
            version_release = version_info.get('version_release')
            if version_release is None:
                raise exception_error.CmdExecuteError(f"version_release is None")
            BGM = version_info.get('build_version')
            domain_version_info.bootes_version = version_info.get('bootes_version')
            domain_version_info.IDL = version_info.get('jidl_version')
            domain_version_info.JIDLCompiler = version_info.get('bootes_version')
            domain_version_info.bgm_boot_version = self.bgm_diag_info.get('bgm_boot_version')
            domain_version_info.bgm_mcu_version = self.bgm_diag_info.get('bgm_mcu_version')
            domain_version_info.bgm_switch_version = self.bgm_diag_info.get('bgm_switch_version')
            domain_version_info.SDB = version_release
            domain_version_info.veh_type = tc_config.get('veh_type')
            domain_version_info.hardware_version = dict(
                BGM=self.bgm_diag_info.get('hardware_version'),
                TCAM=self.tcam_diag_info.get('hardware_version'),
                CDC=self.cdc_diag_info.get('hardware_version'),
                ACU=self.acu_diag_info.get('hardware_version')
            )
            TCAM = tcamssh.get_soa_jidl_name().get('build_version')
            ACU = command_send(
                device_name='ACU', connect_type='obd',
                cmd="cat /opt/data/output/acu/version.txt|grep -o '\"software_version\": \"[^\"]*' | cut -d'\"' -f4")
            logger.info(f"ACU: {[ACU]}")
            time.sleep(2)
            ACU = ACU[1]
            CDC = command_send(
                device_name='CDCQ', connect_type='obd',
                cmd='cat /mnt/etc/build.prop | grep sw_part_number')
            logger.info(f"CDC: {[CDC]}")
            CDC = CDC[1].split('=')[1]
            domain_version_info.software_version = dict(
                BGM=BGM,
                TCAM=TCAM,
                ACU=ACU,
                CDC=CDC,
            )
            close_command(device_name='ACU', connect_type='obd')
            close_command(device_name='CDCQ', connect_type='obd')
        # 三域BGM+CDC+ACU
        elif domain_info.bgm_cdc_acu:
            bgmssh = BGM_SSH(connect_type='obd')
            version_info = bgmssh.get_version()
            self.cdc_diag_info = get_cdc_diag_info(**tc_config)
            self.acu_diag_info = get_acu_diag_info(**tc_config)
            version_release = version_info.get('version_release')
            if version_release is None:
                raise exception_error.CmdExecuteError(f"version_release is None")
            BGM = version_info.get('build_version')
            domain_version_info.bootes_version = version_info.get('bootes_version')
            domain_version_info.IDL = version_info.get('jidl_version')
            domain_version_info.JIDLCompiler = version_info.get('bootes_version')
            domain_version_info.bgm_boot_version = self.bgm_diag_info.get('bgm_boot_version')
            domain_version_info.bgm_mcu_version = self.bgm_diag_info.get('bgm_mcu_version')
            domain_version_info.bgm_switch_version = self.bgm_diag_info.get('bgm_switch_version')
            domain_version_info.SDB = version_release
            domain_version_info.veh_type = tc_config.get('veh_type')
            domain_version_info.hardware_version = dict(
                BGM=self.bgm_diag_info.get('hardware_version'),
                CDC=self.cdc_diag_info.get('hardware_version'),
                ACU=self.acu_diag_info.get('hardware_version')
            )
            ACU = command_send(
                device_name='ACU', connect_type='obd',
                cmd="cat /opt/data/output/acu/version.txt|grep -o '\"software_version\": \"[^\"]*' | cut -d'\"' -f4")
            logger.info(f"ACU: {[ACU]}")
            time.sleep(2)
            ACU = ACU[1]
            CDC = command_send(
                device_name='CDCQ', connect_type='obd',
                cmd='cat /mnt/etc/build.prop | grep sw_part_number')
            logger.info(f"CDC: {[CDC]}")
            CDC = CDC[1].split('=')[1]
            domain_version_info.software_version = dict(
                BGM=BGM,
                ACU=ACU,
                CDC=CDC,
            )
            close_command(device_name='ACU', connect_type='obd')
            close_command(device_name='CDCQ', connect_type='obd')
        # 三域BGM+TCAM+ACU
        elif domain_info.bgm_tcam_acu:
            bgmssh = BGM_SSH(connect_type='obd')
            tcamssh = TCAM_SSH(connect_type='obd')
            version_info = bgmssh.get_version()
            self.tcam_diag_info = get_tcam_diag_info(**tc_config)
            self.acu_diag_info = get_acu_diag_info(**tc_config)
            version_release = version_info.get('version_release')
            BGM = version_info.get('build_version')
            domain_version_info.bootes_version = version_info.get('bootes_version')
            domain_version_info.IDL = version_info.get('jidl_version')
            domain_version_info.JIDLCompiler = version_info.get('bootes_version')
            domain_version_info.bgm_boot_version = self.bgm_diag_info.get('bgm_boot_version')
            domain_version_info.bgm_mcu_version = self.bgm_diag_info.get('bgm_mcu_version')
            domain_version_info.bgm_switch_version = self.bgm_diag_info.get('bgm_switch_version')
            domain_version_info.SDB = version_release
            domain_version_info.veh_type = tc_config.get('veh_type')
            domain_version_info.hardware_version = dict(
                BGM=self.bgm_diag_info.get('hardware_version'),
                TCAM=self.tcam_diag_info.get('hardware_version'),
                ACU=self.acu_diag_info.get('hardware_version')
            )
            TCAM = tcamssh.get_soa_jidl_name().get('build_version')
            ACU = command_send(
                device_name='ACU', connect_type='obd',
                cmd="cat /opt/data/output/acu/version.txt|grep -o '\"software_version\": \"[^\"]*' | cut -d'\"' -f4")
            logger.info(f"ACU: {[ACU]}")
            time.sleep(2)
            ACU = ACU[1]
            domain_version_info.software_version = dict(
                BGM=BGM,
                TCAM=TCAM,
                ACU=ACU,
            )
            close_command(device_name='ACU', connect_type='obd')
        # 三域BGM+TCAM+CDC
        elif domain_info.bgm_tcam_cdc:
            bgmssh = BGM_SSH(connect_type='obd')
            tcamssh = TCAM_SSH(connect_type='obd')
            version_info = bgmssh.get_version()
            self.tcam_diag_info = get_tcam_diag_info(**tc_config)
            self.cdc_diag_info = get_cdc_diag_info(**tc_config)
            version_release = version_info.get('version_release')
            BGM = version_info.get('build_version')
            domain_version_info.bootes_version = version_info.get('bootes_version')
            domain_version_info.IDL = version_info.get('jidl_version')
            domain_version_info.JIDLCompiler = version_info.get('bootes_version')
            domain_version_info.bgm_boot_version = self.bgm_diag_info.get('bgm_boot_version')
            domain_version_info.bgm_mcu_version = self.bgm_diag_info.get('bgm_mcu_version')
            domain_version_info.bgm_switch_version = self.bgm_diag_info.get('bgm_switch_version')
            domain_version_info.SDB = version_release
            domain_version_info.veh_type = tc_config.get('veh_type')
            domain_version_info.hardware_version = dict(
                BGM=self.bgm_diag_info.get('hardware_version'),
                TCAM=self.tcam_diag_info.get('hardware_version'),
                CDC=self.cdc_diag_info.get('hardware_version')
            )
            TCAM = tcamssh.get_soa_jidl_name().get('build_version')
            CDC = command_send(
                device_name='CDCQ', connect_type='obd',
                cmd='cat /mnt/etc/build.prop | grep sw_part_number')
            logger.info(f"CDC: {[CDC]}")
            CDC = CDC[1].split('=')[1]
            domain_version_info.software_version = dict(
                BGM=BGM,
                TCAM=TCAM,
                CDC=CDC,
            )
            close_command(device_name='CDCQ', connect_type='obd')
        elif domain_info.ccu_cd:
            pass
        elif domain_info.ccu_cd_ad:
            pass
        elif domain_info.ccu_cd_lcu:
            pass
        elif domain_info.ccu_cd_ad_lcu:
            pass
        elif domain_info.lcu_l:
            pass
        elif domain_info.lcu_r:
            pass
        else:
            raise exception_error.ConfigError(
                'domain目前只支持["BGM"]、["TCAM"]、["BGM", "TCAM"]、["BGM", "TCAM", "CDC", "ACU"]、["BGM", "CDC", "ACU"]、["BGM", "TCAM", "ACU"]、["BGM", "TCAM", "CDC"]这几种参数')
        if willow_task_path and os.path.exists(willow_task_path):
            with open(willow_task_path, 'r') as task_json:
                task = json.load(task_json)
                domain_version_info.software_version = task.get("ecu_ver") if task.get(
                    "ecu_ver") else domain_version_info.software_version
                domain_version_info.bootes_version = task.get("X86") if task.get(
                    "X86") else domain_version_info.bootes_version
                domain_version_info.JIDLCompiler = task.get("JIDLCompiler") if task.get(
                    "JIDLCompiler") else domain_version_info.JIDLCompiler
                domain_version_info.IDL = task.get("idl") if task.get("idl") else domain_version_info.IDL
        return domain_version_info

    def set_env_info(
            self,
            domain_info: Domain,
            tb_config,
            tc_config,
            custom_parameters: CustomParameters
    ):
        dh = DatabaseHelper()
        if domain_info.single_bgm:
            try:
                setup_vlan(tb_config.get('eth_vlan'), tb_config.get('partner_domin', 'acu'))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bench_helper.py")
                err_msg = f'vlan设置出错，原因{str(e)}'
                logger.error(err_msg)
                raise exception_error.SetVlanError(err_msg)
            else:
                # 设置和读取缓存的版本信息
                if not self.cache_version_info:
                    bgmssh = BGM_SSH()
                    version_info = bgmssh.get_version()
                    version_release = version_info.get('version_release')
                    if version_release is None:
                        raise exception_error.CmdExecuteError(f"version_release is None")
                    self.bgm_diag_info = get_bgm_diag_info(**tc_config)
                    self.cache_version_info['diag'] = self.bgm_diag_info
                    self.cache_version_info['ssh'] = version_info
                    self.set_cache_diag_info(self.cache_version_info)
                else:
                    logger.info(f'从{self.cache_env_path}中获取bgm_diag_info')
                    self.bgm_diag_info = self.cache_version_info.get('diag')
                    version_release = self.cache_version_info.get('ssh')
                if custom_parameters.bl_ver:
                    tc_config['bl_ver'] = custom_parameters.bl_ver
                else:
                    try:
                        battery_type = self.bgm_diag_info.get('battery_type')
                        if battery_type:
                            tc_config['bl_ver'] = f'v_{version_release[1:-1].replace(".", "_")}0_{battery_type}'
                        else:
                            tc_config['bl_ver'] = 'v_' + version_release[1:-1].replace('.', '_') + '0'
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bench_helper.py")
                        logger.error(f'自动获取bl_ver参数报错, 原因{str(e)}, 采用配置文件中的bl_ver')
                if custom_parameters.veh_type:
                    tc_config['veh_type'] = custom_parameters.veh_type
                else:
                    if self.bgm_diag_info.get('veh_type'):
                        tc_config['veh_type'] = self.bgm_diag_info.get('veh_type')
                    else:
                        logger.info('自动获取车型失败, 采用配置文件中的veh_type')
                try:
                    utc_time = bgmssh.get_build_date_utc()
                    if utc_time:
                        dh.add_ecu_version_deploy(ecuType='BGM', ecuVersion=version_info.get('build_version'),
                                                  deployTime=timestamp_to_datetime_full_millis(int(utc_time)))
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bench_helper.py")
                    logger.warning(f'get_build_date_utc fail, {str(e)}')
                tc_config['dut_ecu'] = ['BGM']
        # 单域TCAM
        elif domain_info.single_tcam:
            try:
                setup_vlan(tb_config.get('eth_vlan'), tb_config.get('partner_domin', 'acu'))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bench_helper.py")
                err_msg = f'vlan设置出错，原因{str(e)}'
                logger.error(err_msg)
                raise exception_error.SetVlanError(err_msg)
            else:
                # 单域tcam设置成9.1的ip
                res = exec_shell("ifconfig")
                res_str = res["output"]
                iface = tb_config.get('eth_vlan')
                for ip in ['172.16.9.1']:
                    if res_str.find(ip) == -1:
                        if res_str.find(f'eth0.9'):
                            exec_shell(f'ip link delete eth0.9')
                        logger.info(f"配置9.1")
                        exec_shell(f'ip link add link {iface} name eth0.9 type vlan id 9')
                        exec_shell(f'ip addr add {ip}/24 dev eth0.9')
                        exec_shell(f'ip link set dev eth0.9 address 02:00:00:00:10:01')
                        exec_shell(f'ifconfig eth0.9 up')
                tcamssh = TCAM_SSH(connect_type='vlan')
                self.time_sync_thread(tb_config.get('eth_vlan'))
                tcam_version_info = tcamssh.get_soa_jidl_name()
                version_release = tcam_version_info.get('build_version')
                if custom_parameters.bl_ver:
                    tc_config['bl_ver'] = custom_parameters.bl_ver
                else:
                    ver = version_release.split(' ')[0][-3:-1]
                    tc_config['bl_ver'] = f"v_{ver[0]}_{ver[1]}_0"
                if custom_parameters.veh_type:
                    tc_config['veh_type'] = custom_parameters.veh_type
                try:
                    utc_time = tcamssh.get_build_date_utc()
                    if utc_time:
                        dh.add_ecu_version_deploy(ecuType='TCAM', ecuVersion=tcam_version_info.get('build_version'),
                                                  deployTime=timestamp_to_datetime_full_millis(int(utc_time)))
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bench_helper.py")
                    logger.warning(f'get_build_date_utc fail, {str(e)}')
                tc_config['dut_ecu'] = ['TCAM']
                tc_config['sd_tester_cfg']['is_via_gateway'] = False
                tc_config['sd_tester_cfg']['ecu_name'] = "TCAM"
                tc_config['sd_tester_cfg']['server_ip'] = "172.16.9.31"
        # 两域BGM+TCAM
        elif domain_info.two_domain:
            try:
                setup_vlan(tb_config.get('eth_vlan'), tb_config.get('partner_domin', 'acu'))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bench_helper.py")
                err_msg = f'vlan设置出错，原因{str(e)}'
                logger.error(err_msg)
                raise exception_error.SetVlanError(err_msg)
            else:
                # 设置和读取缓存的版本信息
                if not self.cache_version_info:
                    bgmssh = BGM_SSH()
                    version_info = bgmssh.get_version()
                    version_release = version_info.get('version_release')
                    if version_release is None:
                        raise exception_error.CmdExecuteError(f"version_release is None")
                    self.bgm_diag_info = get_bgm_diag_info(**tc_config)
                    self.cache_version_info['diag'] = self.bgm_diag_info
                    self.cache_version_info['ssh'] = version_info
                    self.set_cache_diag_info(self.cache_version_info)
                else:
                    logger.info(f'从{self.cache_env_path}中获取bgm_diag_info')
                    self.bgm_diag_info = self.cache_version_info.get('diag')
                    version_release = self.cache_version_info.get('ssh').get('version_release')
                if version_release is None:
                    raise exception_error.CmdExecuteError(f"version_release is None")
                if custom_parameters.veh_type:
                    tc_config['veh_type'] = custom_parameters.veh_type
                else:
                    if self.bgm_diag_info.get('veh_type'):
                        tc_config['veh_type'] = self.bgm_diag_info.get('veh_type')
                    else:
                        logger.info('自动获取车型失败, 采用配置文件中的veh_type')
                if custom_parameters.bl_ver:
                    tc_config['bl_ver'] = custom_parameters.bl_ver
                else:
                    try:
                        if tc_config['veh_type'] == 'mars1' and self.bgm_diag_info.get('battery_type') == 'mca':
                            tc_config['bl_ver'] = 'v_' + version_release[1:-1].replace('.', '_') + '0' + '_mca'
                        else:
                            tc_config['bl_ver'] = 'v_' + version_release[1:-1].replace('.', '_') + '0'
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bench_helper.py")
                        logger.error(f'自动获取bl_ver参数报错, 原因{str(e)}, 采用配置文件中的bl_ver')
                try:
                    utc_time = bgmssh.get_build_date_utc()
                    if utc_time:
                        dh.add_ecu_version_deploy(ecuType='BGM', ecuVersion=version_info.get('build_version'),
                                                  deployTime=timestamp_to_datetime_full_millis(int(utc_time)))
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bench_helper.py")
                    logger.warning(f'get_build_date_utc fail, {str(e)}')
                tc_config['dut_ecu'] = ['BGM', 'TCAM']
        # 四域
        elif domain_info.four_domain:
            # 设置和读取缓存的版本信息
            if not self.cache_version_info:
                bgmssh = BGM_SSH(connect_type='obd')
                version_info = bgmssh.get_version()
                version_release = version_info.get('version_release')
                if version_release is None:
                    raise exception_error.CmdExecuteError(f"version_release is None")
                self.bgm_diag_info = get_bgm_diag_info(**tc_config)
                self.cache_version_info['diag'] = self.bgm_diag_info
                self.cache_version_info['ssh'] = version_info
                self.set_cache_diag_info(self.cache_version_info)
            else:
                logger.info(f'从{self.cache_env_path}中获取bgm_diag_info')
                self.bgm_diag_info = self.cache_version_info.get('diag')
                version_release = self.cache_version_info.get('ssh').get('version_release')
            if version_release is None:
                raise exception_error.CmdExecuteError(f"version_release is None")
            if custom_parameters.veh_type:
                tc_config['veh_type'] = custom_parameters.veh_type
            else:
                if self.bgm_diag_info.get('veh_type'):
                    tc_config['veh_type'] = self.bgm_diag_info.get('veh_type')
                else:
                    logger.info('自动获取车型失败, 采用配置文件中的veh_type')
            if custom_parameters.bl_ver:
                tc_config['bl_ver'] = custom_parameters.bl_ver
            else:
                try:
                    tc_config['bl_ver'] = 'v_' + version_release[1:-1].replace('.', '_') + '0'
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bench_helper.py")
                    logger.error(f'自动获取bl_ver参数报错, 原因{str(e)}, 采用配置文件中的bl_ver')
            try:
                utc_time = bgmssh.get_build_date_utc()
                if utc_time:
                    dh.add_ecu_version_deploy(ecuType='BGM', ecuVersion=version_info.get('build_version'),
                                              deployTime=timestamp_to_datetime_full_millis(int(utc_time)))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bench_helper.py")
                logger.warning(f'get_build_date_utc fail, {str(e)}')
            tc_config['dut_ecu'] = ['BGM', 'TCAM', 'CDC', 'ACU']
        # 三域BGM+CDC+ACU
        elif domain_info.bgm_cdc_acu:
            # 设置和读取缓存的版本信息
            if not self.cache_version_info:
                bgmssh = BGM_SSH(connect_type='obd')
                version_info = bgmssh.get_version()
                version_release = version_info.get('version_release')
                if version_release is None:
                    raise exception_error.CmdExecuteError(f"version_release is None")
                self.bgm_diag_info = get_bgm_diag_info(**tc_config)
                self.cache_version_info['diag'] = self.bgm_diag_info
                self.cache_version_info['ssh'] = version_info
                self.set_cache_diag_info(self.cache_version_info)
            else:
                logger.info(f'从{self.cache_env_path}中获取bgm_diag_info')
                self.bgm_diag_info = self.cache_version_info.get('diag')
                version_release = self.cache_version_info.get('ssh').get('version_release')
            if version_release is None:
                raise exception_error.CmdExecuteError(f"version_release is None")
            if custom_parameters.veh_type:
                tc_config['veh_type'] = custom_parameters.veh_type
            else:
                if self.bgm_diag_info.get('veh_type'):
                    tc_config['veh_type'] = self.bgm_diag_info.get('veh_type')
                else:
                    logger.info('自动获取车型失败, 采用配置文件中的veh_type')
            if custom_parameters.bl_ver:
                tc_config['bl_ver'] = custom_parameters.bl_ver
            else:
                try:
                    tc_config['bl_ver'] = 'v_' + version_release[1:-1].replace('.', '_') + '0'
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bench_helper.py")
                    logger.error(f'自动获取bl_ver参数报错, 原因{str(e)}, 采用配置文件中的bl_ver')
            try:
                utc_time = bgmssh.get_build_date_utc()
                if utc_time:
                    dh.add_ecu_version_deploy(ecuType='BGM', ecuVersion=version_info.get('build_version'),
                                              deployTime=timestamp_to_datetime_full_millis(int(utc_time)))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bench_helper.py")
                logger.warning(f'get_build_date_utc fail, {str(e)}')
            tc_config['dut_ecu'] = ['BGM', 'CDC', 'ACU']
        # 三域BGM+TCAM+ACU
        elif domain_info.bgm_tcam_acu:
            # 设置和读取缓存的版本信息
            if not self.cache_version_info:
                bgmssh = BGM_SSH(connect_type='obd')
                version_info = bgmssh.get_version()
                version_release = version_info.get('version_release')
                if version_release is None:
                    raise exception_error.CmdExecuteError(f"version_release is None")
                self.bgm_diag_info = get_bgm_diag_info(**tc_config)
                self.cache_version_info['diag'] = self.bgm_diag_info
                self.cache_version_info['ssh'] = version_info
                self.set_cache_diag_info(self.cache_version_info)
            else:
                logger.info(f'从{self.cache_env_path}中获取bgm_diag_info')
                self.bgm_diag_info = self.cache_version_info.get('diag')
                version_release = self.cache_version_info.get('ssh').get('version_release')
            if version_release is None:
                raise exception_error.CmdExecuteError(f"version_release is None")
            if custom_parameters.veh_type:
                tc_config['veh_type'] = custom_parameters.veh_type
            else:
                if self.bgm_diag_info.get('veh_type'):
                    tc_config['veh_type'] = self.bgm_diag_info.get('veh_type')
                else:
                    logger.info('自动获取车型失败, 采用配置文件中的veh_type')
            if custom_parameters.bl_ver:
                tc_config['bl_ver'] = custom_parameters.bl_ver
            else:
                try:
                    tc_config['bl_ver'] = 'v_' + version_release[1:-1].replace('.', '_') + '0'
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bench_helper.py")
                    logger.error(f'自动获取bl_ver参数报错, 原因{str(e)}, 采用配置文件中的bl_ver')
            try:
                utc_time = bgmssh.get_build_date_utc()
                if utc_time:
                    dh.add_ecu_version_deploy(ecuType='BGM', ecuVersion=version_info.get('build_version'),
                                              deployTime=timestamp_to_datetime_full_millis(int(utc_time)))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bench_helper.py")
                logger.warning(f'get_build_date_utc fail, {str(e)}')
            tc_config['dut_ecu'] = ['BGM', 'TCAM', 'ACU']
        # 三域BGM+TCAM+CDC
        elif domain_info.bgm_tcam_cdc:
            # 设置和读取缓存的版本信息
            if not self.cache_version_info:
                bgmssh = BGM_SSH(connect_type='obd')
                version_info = bgmssh.get_version()
                version_release = version_info.get('version_release')
                if version_release is None:
                    raise exception_error.CmdExecuteError(f"version_release is None")
                self.bgm_diag_info = get_bgm_diag_info(**tc_config)
                self.cache_version_info['diag'] = self.bgm_diag_info
                self.cache_version_info['ssh'] = version_info
                self.set_cache_diag_info(self.cache_version_info)
            else:
                logger.info(f'从{self.cache_env_path}中获取bgm_diag_info')
                self.bgm_diag_info = self.cache_version_info.get('diag')
                version_release = self.cache_version_info.get('ssh').get('version_release')
            if version_release is None:
                raise exception_error.CmdExecuteError(f"version_release is None")
            if custom_parameters.veh_type:
                tc_config['veh_type'] = custom_parameters.veh_type
            else:
                if self.bgm_diag_info.get('veh_type'):
                    tc_config['veh_type'] = self.bgm_diag_info.get('veh_type')
                else:
                    logger.info('自动获取车型失败, 采用配置文件中的veh_type')
            if custom_parameters.bl_ver:
                tc_config['bl_ver'] = custom_parameters.bl_ver
            else:
                try:
                    tc_config['bl_ver'] = 'v_' + version_release[1:-1].replace('.', '_') + '0'
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bench_helper.py")
                    logger.error(f'自动获取bl_ver参数报错, 原因{str(e)}, 采用配置文件中的bl_ver')
            try:
                utc_time = bgmssh.get_build_date_utc()
                if utc_time:
                    dh.add_ecu_version_deploy(ecuType='BGM', ecuVersion=version_info.get('build_version'),
                                              deployTime=timestamp_to_datetime_full_millis(int(utc_time)))
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bench_helper.py")
                logger.warning(f'get_build_date_utc fail, {str(e)}')
            tc_config['dut_ecu'] = ['BGM', 'TCAM', 'CDC']
        elif domain_info.ccu_cd:
            # try:
            #     setup_vlan(tb_config.get('eth_vlan'), tb_config.get('partner_domin', 'acu'))
            # except Exception as e:
            #     err_msg = f'vlan设置出错，原因{str(e)}'
            #     logger.error(err_msg)
            #     raise exception_error.SetVlanError(err_msg)
            # else:
            # 设置和读取缓存的版本信息
            if not self.cache_version_info:
                cd_soc_ssh = CD_SOC_SSH()
                version_info = cd_soc_ssh.get_version()
                version_release = version_info.get('version_release')
                if version_release is None:
                    raise exception_error.CmdExecuteError(f"version_release is None")
                # self.bgm_diag_info = get_bgm_diag_info(**tc_config)
                # self.cache_version_info['diag'] = self.bgm_diag_info
                self.cache_version_info['ssh'] = version_info
                self.set_cache_diag_info(self.cache_version_info)
            else:
                logger.info(f'从{self.cache_env_path}中获取ccu_cd版本信息')
                # self.bgm_diag_info = self.cache_version_info.get('diag')
                version_release = self.cache_version_info.get('ssh').get('version_release')
            if version_release is None:
                raise exception_error.CmdExecuteError(f"version_release is None")
            if custom_parameters.veh_type:
                tc_config['veh_type'] = custom_parameters.veh_type
            else:
                if self.ccu_cd_info.get('veh_type'):
                    tc_config['veh_type'] = self.ccu_cd_info.get('veh_type')
                else:
                    logger.info('自动获取车型失败, 采用配置文件中的veh_type')
            if custom_parameters.bl_ver:
                tc_config['bl_ver'] = custom_parameters.bl_ver
            else:
                try:
                    if tc_config['veh_type'] == 'mars1' and self.ccu_cd_info.get('battery_type') == 'mca':
                        tc_config['bl_ver'] = 'v_' + version_release[1:-1].replace('.', '_') + '0' + '_mca'
                    else:
                        tc_config['bl_ver'] = 'v_' + version_release[1:-1].replace('.', '_') + '0'
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bench_helper.py")
                    logger.error(f'自动获取bl_ver参数报错, 原因{str(e)}, 采用配置文件中的bl_ver')
                # try:
                #     utc_time = bgmssh.get_build_date_utc()
                #     if utc_time:
                #         dh.add_ecu_version_deploy(ecuType='BGM', ecuVersion=version_info.get('build_version'),
                #                                   deployTime=timestamp_to_datetime_full_millis(int(utc_time)))
                # except Exception as e:
                #     logger.warning(f'get_build_date_utc fail, {str(e)}')
        elif domain_info.ccu_cd_ad:
            pass
        # 两域BGM+TCAM
        elif domain_info.ccu_cd_lcu:
            pass
        # 四域
        elif domain_info.ccu_cd_ad_lcu:
            pass
        elif domain_info.lcu_l:
            pass
        elif domain_info.lcu_r:
            pass
        else:
            raise exception_error.ConfigError(
                'domain目前只支持["BGM"]、["TCAM"]、["BGM", "TCAM"]、["BGM", "TCAM", "CDC", "ACU"]、["BGM", "CDC", "ACU"]、["BGM", "TCAM", "ACU"]、["BGM", "TCAM", "CDC"]这几种参数')
        return tc_config

    @staticmethod
    def generate_env_properties_on_allure(env_properties: EnvPropertiesInfo):
        environment_path = '../../../report/allure_report/environment.properties'
        environment_path_copy = f'../../../report/allure_report/{env_properties.wifi_localhost}_env.properties'
        if os.path.exists("../../../report/allure_report"):
            with open(environment_path, 'w') as f:
                for key, value in env_properties.__dict__.items():
                    if value:
                        f.write(f'{key}={value}\n')
            with open(environment_path_copy, 'w') as f:
                for key, value in env_properties.__dict__.items():
                    if value:
                        f.write(f'{key}={value}\n')

    def time_sync_thread(self, iface):
        t = threading.Thread(target=self.time_sync, args=(iface, 1800), name='tcam_time_sync')
        t.setDaemon(True)
        t.start()

    @staticmethod
    def time_sync(iface, timeout):
        while True:
            logger.info(f'启动时间同步脚本')
            try:
                tcam_time_sync(iface=iface, timeout=timeout)
            except exception_error.CmdExecuteError:
                logger.info(f'启动失败，继续执行')
                continue
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bench_helper.py")
                logger.error(f"{str(e)}, 启动失败，继续执行")
                continue
            time.sleep(1)

    @staticmethod
    def _get_ecu_simulator_version():
        return package_version('xat-ecu')

    def _get_remote_ecu_simulator_version(self, pip_path, client: SshClient):
        self.print_log(f"开始检查{client.host}台架ecu的版本")
        cmd = pip_path + " show xat-ecu | sed -n 's/^Version: //p'"
        status, output = client.execute(cmd, is_reconnect=False, log_print=True, print_raw_data=True)
        output = '\n'.join(output.split('\r\n')[1:-1])
        self.print_log(f"{client.host}台架ecu的版本检查结束，版本号为{output}")
        self._check_output(client, cmd)
        return output

    @staticmethod
    def _get_sat_framework_version():
        return package_version('xat')

    @staticmethod
    def _get_sdk_interface_version():
        return package_version('xat-ecu')

    @staticmethod
    def _get_sat_commit_or_tag():
        ret = exec_shell(f'git -C {REPOSITORY_ROOT} rev-parse HEAD').get('output')
        return ret.strip()

    @staticmethod
    def _get_bench_yaml_version(yaml_name):
        cmd = f"cd {parent_dir}/bench_config;"
        cmd += rf'git log -1 --pretty=format:"%h~%an~%ad" --date=format:"%Y-%m-%d %H:%M:%S" -- {yaml_name}'
        ret = exec_shell(cmd).get('output').split('~')
        bench_version_info = dict(
            commitId=ret[0],
            lastModifyUser=ret[1],
            lastModifyTime=ret[2]
        )
        return bench_version_info

    def get_framework_version_info(self):
        return dict(
            sdkInterfaceVersion=self._get_sdk_interface_version(),
            satFrameworkVersion=self._get_sat_framework_version(),
            ecuSimulatorVersion=self._get_ecu_simulator_version(),
            satCommitId=self._get_sat_commit_or_tag(),
        )

    def get_bench_version_info(self, bench_ip):
        if self.yaml_name:
            bench_version_info = self._get_bench_yaml_version(self.yaml_name)
            logger.info(bench_version_info)
            return dict(
                yamlName=self.yaml_name,
                benchIp=bench_ip,
                lastModifyTime=bench_version_info.get('lastModifyTime'),
                lastModifyUser=bench_version_info.get('lastModifyUser'),
                commitId=bench_version_info.get('commitId'),
            )

    def deploy_running_env(self, master_bench_config: BenchConfig, slave_bench_config: BenchConfig, ecuinfo: EcuInfo,
                           case_list, vehicle_model, is_willow, workspace, is_flash, running_env, service_ip,
                           service_port):
        # 如果有网线ip则优先使用网线ip
        ip_list = [slave_bench_config.host]
        if slave_bench_config.limited_ip:
            ip_list.append(slave_bench_config.limited_ip)
        port = slave_bench_config.port
        username = slave_bench_config.username
        password = slave_bench_config.password
        for hostname in reversed(ip_list):
            for count in range(1, RETRY_COUNT + 1):
                try:
                    client = SshClient(host=hostname, port=port, username=username, password=password)
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bench_helper.py")
                    logger.warning(f"连接{hostname}:{port}失败，原因是:{str(e)}，当前失败次数为{count}，重连中")
                    continue
                else:
                    logger.info(f"连接{hostname}:{port}成功")
                    break
            else:
                logger.error(f"连接{hostname}:{port} {RETRY_COUNT}次后仍然失败，直接退出")
                continue
            break
        else:
            raise exception_error.CmdExecuteError(f"连接{ip_list}:{port} {RETRY_COUNT}次后仍然失败，直接退出")
        sat = ecuinfo.framework_version.get("satCommitId")
        sat_framework = ecuinfo.framework_version.get("satFrameworkVersion")
        sdk_interface = ecuinfo.framework_version.get("sdkInterfaceVersion")
        ecu_simulator = ecuinfo.framework_version.get("ecuSimulatorVersion")
        path = Path(workspace) / RepoName.sat.value
        for count in range(1, (RETRY_COUNT - 7) + 1):
            try:
                if self._check_env(path, client):
                    self._reset_env(path, client)
                    self._pull_and_checkout(path, sat, client)
                else:
                    self._creat_remote_work_dir(workspace, client)
                    self._git_clone_code(workspace, client)
                    self._pull_and_checkout(path, sat, client)
                self._update_lib_running(path, client, sdk_interface, ecu_simulator, sat_framework)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bench_helper.py")
                logger.error(f"部署环境失败，原因是:{str(e)}，当前失败次数为{count}")
                # 删除sat目录后重试
                self._del_sat_folder(path, client)
                continue
            else:
                break
        else:
            raise exception_error.CmdExecuteError(f"部署环境失败，尝试了{RETRY_COUNT - 7}次仍旧失败")
        logger.info(master_bench_config)
        logger.info(slave_bench_config)
        update_type = self._generate_task_json_on_master(
            slave_ip=hostname,
            workspace=parent_dir,
            report_dir=os.path.join(parent_dir, "../", "report", "allure_report"),
            hostname=master_bench_config.host,
            master_limited_ip=master_bench_config.limited_ip,
            port=master_bench_config.port,
            username=master_bench_config.username,
            password=master_bench_config.password,
            uuid=master_bench_config.distribute_task_id,
            vehicle_model=re.sub(r" +", "_", vehicle_model) if vehicle_model else "",
            service_ip=service_ip,
            service_port=service_port,
            case_list=case_list,
            master_bench_config=master_bench_config,
            slave_bench_config=slave_bench_config,
            running_env=running_env
        )
        self._scp_task_json_to_slave(hostname=hostname, port=port, username=username, password=password,
                                     is_willow=is_willow, workspace=workspace)
        if is_flash:
            # 执行升级
            self._update(workspace=path, client=client, update_type=update_type)
        else:
            logger.info("未指定flashed升级参数，不进行升级")
        return client

    def deploy_env_on_anther_bench(self, bench_config: BenchConfig, ecuinfo: EcuInfo):
        hostname = bench_config.limited_ip if bench_config.limited_ip else bench_config.host
        port = bench_config.port
        username = bench_config.username
        password = bench_config.password
        workdir_username = self._get_workdir_username()
        # 将当前目录的用户名替换成待copy的
        root_path = Path(parent_dir.replace(workdir_username, f"{workdir_username}_copy")).parent
        remote_sat_path = Path(root_path) / RepoName.sat.value
        ecuinfo.cmd = ecuinfo.cmd.replace(workdir_username, f"{workdir_username}_copy")
        # 校验sdk_interface/framework/automotive/ecu_simulator版本是否一致
        client = SshClient(host=hostname, port=port, username=username, password=password)
        sat_framework = ecuinfo.framework_version.get("satFrameworkVersion")
        sdk_interface = ecuinfo.framework_version.get("sdkInterfaceVersion")
        ecu_simulator = ecuinfo.framework_version.get("ecuSimulatorVersion")
        if self._check_env(remote_sat_path, client):
            reset_status = self._reset_env(remote_sat_path, client)
            if not reset_status:
                self._git_clone_code(root_path, client)
        else:
            self._creat_remote_work_dir(root_path, client)
            self._git_clone_code(root_path, client)
        self._update_lib_running(remote_sat_path, client, sdk_interface, ecu_simulator, sat_framework)
        current_repo_list = [REPOSITORY_ROOT]
        # 增量拷贝代码
        for current_repo_path in current_repo_list:
            self._incremental_copy_code(hostname, port, username, password, current_repo_path, workdir_username)
        self._running_pytest(remote_sat_path, client, ecuinfo.cmd)

    def _incremental_copy_code(self, hostname, port, username, password, current_repo_path, workdir_username):
        current_commit = self._get_current_commit(current_repo_path)
        diff_file_list = self._git_diff_commit_file(current_repo_path, current_commit) or []
        if diff_file_list:
            for diff_file in diff_file_list:
                new_diff_file = diff_file.replace(workdir_username, f"{workdir_username}_copy")
                self._scp_diff_commit_file_to_anther_bench(
                    hostname=hostname,
                    port=port,
                    username=username,
                    password=password,
                    remote_sat_path=new_diff_file,
                    file_list=diff_file
                )

    def _check_env(self, path, client: SshClient):
        logger.info('check env')
        self.print_log(f"开始检查台架{client.host}{path}是否存在")
        cmd = f'ls {path}'
        status, output = client.execute(cmd, is_reconnect=False, log_print=True, print_raw_data=True)
        self._check_ls_output(client, cmd)
        self.print_log(f"台架{client.host}检查完成")
        if "No such" in output:
            return
        # 适配台架中文字体
        elif "没有那个文件" in output:
            return False
        else:
            return True

    def _del_sat_folder(self, path, client: SshClient):
        self.print_log(f"开始删除台架{client.host}：{path}仓库代码")
        cmd = f'rm -rf {path}'
        status, output = client.execute(cmd, is_reconnect=False, log_print=True, print_raw_data=True)
        self._check_output(client, cmd)
        self.print_log(f"台架{client.host}sat仓库代码删除结束")

    @staticmethod
    def _get_workdir_username():
        cmd = "pwd |awk -F/ '{print $3}'"
        ret = exec_shell(cmd).get('output')
        if ret:
            username = ret.split('\n')[0]
            return username

    def _reset_env(self, path, client: SshClient):
        self.print_log(f"开始清理台架{client.host}远程工作目录")
        preserve_logs_cmd = (
                "find " + str(
            path) + "/xat/cases/src/xat_cases/legacy -mindepth 2 -maxdepth 2 -type d -name logs -exec bash -c 'cd \"{}\" && "
                    "ls -t1 *.log | tail -n +6 | xargs -r rm -f' \\;")
        client.execute(preserve_logs_cmd, is_reconnect=False, log_print=True, print_raw_data=True, timeout=600)
        reset_cmd = "git reset --hard"
        cmd = f'cd {path};{reset_cmd};git clean -ffdx --exclude=logs'
        status, output = client.execute(cmd, is_reconnect=False, log_print=True, print_raw_data=True, timeout=600)
        self.print_log(f"台架{client.host}远程工作目录清理结束")
        # 有目录但不是git管控
        if '.git' in output:
            return False
        else:
            self._check_output(client, cmd)
            return True

    def _pull_and_checkout(self, path, commit, client: SshClient):
        self.print_log(f"开始更新台架{client.host}sat仓库代码")
        cmd = f'cd {path};git fetch origin;git checkout --detach {commit}'
        client.execute(cmd, is_reconnect=False, log_print=True, print_raw_data=True, timeout=6000)
        self._check_output(client, cmd)
        self.print_log(f"台架{client.host}sat仓库代码更新结束")

    @staticmethod
    def print_log(step):
        logger.info(f"****************{step}****************")

    def _creat_remote_work_dir(self, path, client: SshClient):
        self.print_log(f"开始创建台架{client.host}远程工作目录")
        cmd = f'mkdir -p {path}'
        client.execute(cmd, is_reconnect=False, log_print=True, print_raw_data=True)
        self._check_output(client, cmd)
        self.print_log(f"结束创建台架{client.host}远程工作目录")

    def _git_clone_code(self, path, client: SshClient):
        self.print_log(f"开始进行台架{client.host}仓库代码克隆")
        cmd = clone_command(path)
        client.execute(cmd, timeout=6000, is_reconnect=False, log_print=True, print_raw_data=True)
        self._check_output(client, cmd)
        self.print_log(f"台架{client.host}仓库代码克隆结束")

    def _update_lib_running(self, path, client: SshClient, sdk_interface, ecu_simulator, sat_framework):
        self.print_log(f'开始安装台架{client.host}的 XAT 框架、库与用例')
        cmd = install_command(path)
        client.execute(cmd, timeout=600, is_reconnect=False, log_print=True, print_raw_data=True)
        self._check_output(client, cmd)
        self.print_log(f'台架{client.host}的 XAT 安装结束')

    def _check_output(self, client: SshClient, check_cmd):
        cmd = f"echo $?"
        status, output = client.execute(cmd, is_reconnect=False, log_print=True)
        output = output.split('\r\n')[1:2][0]
        # if output == str(pytest.ExitCode.TESTS_FAILED.value):
        #     return
        # if output == '2':
        #     return
        if output != '0':
            raise exception_error.CmdExecuteError(f"台架{client.host}部署失败，执行命令{check_cmd}返回值为:{output}")

    def _check_ls_output(self, client: SshClient, check_cmd):
        cmd = f"echo $?"
        status, output = client.execute(cmd, is_reconnect=False, log_print=True)
        output = output.split('\r\n')[1:2][0]
        # 2:目录不存在
        if output == '2':
            return

    def _running_pytest(self, workspace, client, cmd):
        self.print_log(f"台架{client.host}开始运行{cmd}")
        cmd = f"cd {workspace};source venv/bin/activate;{cmd}"
        client.execute(cmd, timeout=6000, is_reconnect=False, log_print=True, print_raw_data=True)
        self._check_output(client, cmd)
        self.print_log(f"台架{client.host}开始运行{cmd}运行结束")

    def _update(self, workspace, client, update_type):
        # "update": [
        #     {
        #         "bgm": {
        #             "img_url": "https://repo.jidudev.com/artifactory/BGMSoftware/Release/v2.0.0/6160110200BM/6160110200BM.bin",
        #             "keyinfo": "${XAT_CREDENTIAL_SCAN_582F70F6CEB3A50C1FB1}"
        #         }
        #     },
        #     {
        #         "boot": {
        #             "img_url_boot": "https://repo.jidudev.com/artifactory/BGMSoftware/Release/v2.0.0/6160110200BM/2960110200BB.bin",
        #             "keyinfo_boot": "${XAT_CREDENTIAL_SCAN_12F99C28A710A9E95DB4}"
        #         }
        #     },
        #     {
        #         "tcam": {
        #             "img_url": "",
        #             "keyinfo": ""
        #         }
        #     },
        #     {
        #         "mcu": {
        #             "switch_ver": "",
        #             "switch_ver_b": ""
        #         }
        #     }
        # ]
        update_dict = {
            'bgm': "cd xat/cases/src/xat_cases/legacy/bgm && pytest ecu_flash/test_flash_bgm_distributed.py --bl_ver=v_2_0_0 --disable_lock",
            'tcam': "cd xat/cases/src/xat_cases/legacy/tcam && pytest basetech/ecu_flash/test_flash_tcam_distributed.py --bl_ver=v_2_0_0 --disable_lock",
            'mcu': "cd xat/cases/src/xat_cases/legacy/bgm && pytest mcu/update_mcu/test_update_mcu_distributed.py --bl_ver=v_2_0_0 --disable_lock",
            'sil_bgm': 'docker rm -f autotest && ./deploy_SIL_env.sh bgm "source venv/bin/activate;cd xat/cases/src/xat_cases/legacy/bgm && pytest ecu_flash/test_flash_sil_bgm_distributed.py --disable_partner=true"',
        }

        for domain in update_type:
            cmd = f"{update_dict[domain]}"
            self.print_log(f"开始执行台架{client.host}升级的脚本{cmd}")
            self._running_pytest(workspace=workspace, client=client, cmd=cmd)
            self.print_log(f"台架{client.host}升级脚本执行结束")

    @staticmethod
    def _get_current_commit(path):
        cmd = f'cd {path};git rev-parse HEAD'
        ret = exec_shell(cmd).get('output')
        if ret:
            current_commit = ret.split('\n')[0]
            return current_commit

    @staticmethod
    def _git_diff_commit_file(path, current_commit):
        cmd = f'cd {path};git diff {current_commit} --name-only'
        ret = exec_shell(cmd).get('output')
        if ret:
            diff_commit_file_list = ret.split('\n')[:-1]
            return [f'{path}/{file_path}' for file_path in diff_commit_file_list]

    @staticmethod
    def _scp_diff_commit_file_to_anther_bench(**kwargs):
        hostname = kwargs.get("hostname")
        port = kwargs.get("port")
        username = kwargs.get("username")
        password = kwargs.get("password")
        target_file_list = kwargs.get("file_list")
        remote_sat_path = kwargs.get("remote_sat_path")
        client = BenchHelper.retry_scp(hostname, port, username, password)
        client.put(target_file_list, remote_sat_path)

    @staticmethod
    def retry_scp(hostname, port, username, password):
        for count in range(1, RETRY_COUNT + 1):
            try:
                client = ScpClient(host=hostname, port=port, username=username, password=password)
                client.scp_session.socket_timeout = 600  # 设置文件上传的超时时间
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/bench_helper.py")
                logger.warning(f"连接{hostname}:{port}失败，原因是:{str(e)}，当前失败次数为{count}，重连中")
                continue
            else:
                break
        else:
            raise exception_error.ClientError(f"连接{hostname}:{port} {RETRY_COUNT}次后仍然失败，直接退出")
        return client

    @staticmethod
    def add_running_pytest_task(workspace, host, cmd, distribute_task_id, job_info, willow_feishu_config_info):
        logger.info('running_pytest')
        # cmd = f"cd {workspace}/sat && source venv/bin/activate && {cmd}".replace(';', ' && ')
        dh = DatabaseHelper()
        dh.add_device_test_task(deviceId=host, code=cmd, distibuteTaskId=distribute_task_id, job_info=job_info,
                                willow_feishu_config_info=willow_feishu_config_info)

    def running_pytest_task_by_ssh(self, client: SshClient, cmd, timeout=6000):
        self.print_log(f"台架{client.host}开始运行{cmd}")
        client.execute(cmd, timeout=timeout, is_reconnect=False, log_print=True, print_raw_data=True)
        self._check_output(client, cmd)

    @staticmethod
    def update_running_pytest_task(willow_feishu_config_info):
        logger.info('update device test task allure')
        dh = DatabaseHelper()
        dh.update_device_test_task(willow_feishu_config_info=willow_feishu_config_info)

    def set_status(self, bench_config: BenchConfig, status: BenchStatus, case_progress: CaseProgress = None):
        # 更新台架状态
        self._bench_status[bench_config.host] = status
        if case_progress:
            self._case_progress = case_progress

    def submit_bench_status(self, bench_config: BenchConfig, status: BenchStatus):
        self._bench_status[bench_config.host] = status
        dh = DatabaseHelper()
        while True:
            bench_status = copy.deepcopy(self._bench_status)
            for host, status in bench_status.items():
                if status == BenchStatus.idle:
                    logger.info(
                        f"####################{host} {status} ####################")
                    del self._bench_status[bench_config.host]
                    dh.update_bench_save(agentIp=host, status=status.value)
                elif status == BenchStatus.case_running:
                    # slave端上报用例执行进度
                    if self._case_progress:
                        report_info = dict(
                            totalCaseCount=self._case_progress.total,
                            passCaseCount=self._case_progress.passed,
                            failCaseCount=self._case_progress.failed,
                            errorCaseCount=self._case_progress.error,
                            leftCaseCount=self._case_progress.remain_case,
                            currentCase=self._case_progress.current_case,
                            syncMsFailCount=self._case_progress.sync_ms_fail
                        )
                        logger.debug(report_info)
                        dh.update_test_task(
                            deviceId=host,
                            distibuteTaskId=bench_config.distribute_task_id,
                            totalCaseCount=self._case_progress.total,
                            passCaseCount=self._case_progress.passed,
                            failCaseCount=self._case_progress.failed,
                            errorCaseCount=self._case_progress.error,
                            leftCaseCount=self._case_progress.remain_case,
                            currentCase=self._case_progress.current_case,
                            syncMsFailCount=self._case_progress.sync_ms_fail
                        )
                        dh.update_bench_save(agentIp=host, status=status.value)
                elif status == BenchStatus.stop:
                    del self._bench_status[bench_config.host]
            if not self._bench_status:
                return
            time.sleep(5)

    def _generate_task_json_on_master(self, **kwargs):
        slave_ip = kwargs.get("slave_ip")
        workspace = kwargs.get("workspace")
        report_dir = kwargs.get("report_dir")
        hostname = kwargs.get("hostname")
        master_limited_ip = kwargs.get("master_limited_ip")
        port = kwargs.get("port")
        username = kwargs.get("username")
        password = kwargs.get("password")
        service_ip = kwargs.get("service_ip")
        service_port = kwargs.get("service_port")
        vehicle_model = kwargs.get("vehicle_model")
        uuid = kwargs.get("uuid")
        case_list = kwargs.get("case_list")
        master_bench_config: BenchConfig = kwargs.get("master_bench_config")
        slave_bench_config: BenchConfig = kwargs.get("slave_bench_config")
        running_env = kwargs.get("running_env")
        task_json = {
            "master_config": {
                "workspace": workspace,
                "report_dir": report_dir,
                "limited_ip": master_limited_ip,
                "hostname": hostname,
                "port": port,
                "username": username,
                "password": password,
                "service_ip": service_ip,
                "service_port": service_port
            },
            "case_list": case_list,
            "uuid": uuid,
            "vehicle_model": vehicle_model,
        }
        logger.debug(task_json)
        try:
            return self._add_version_in_task_json(
                slave_ip=slave_ip,
                task_json=task_json,
                master_bench_config=master_bench_config,
                slave_bench_config=slave_bench_config,
                running_env=running_env)
        except Exception as e:
            logger.exception(f"_add_version_in_task_json出现异常：{str(e)}")
            raise e

    @staticmethod
    def _add_version_in_task_json(**kwargs):
        img_url = ''
        keyinfo = ''
        img_url_boot = ''
        keyinfo_boot = ''
        mcu_zip_url = ''
        tcam_img_url = ''
        tcam_keyinfo = ''
        slave_ip = kwargs.get("slave_ip")
        master_bench_config: BenchConfig = kwargs.get("master_bench_config")
        slave_bench_config: BenchConfig = kwargs.get("slave_bench_config")
        task_json = kwargs.get('task_json')
        running_env = kwargs.get('running_env')
        task_json['update'] = []
        task_path = os.path.join(parent_dir, "../", "task.json")
        # 如果存在task.json， 则直接按照task.json进行升级
        if os.path.exists(task_path):
            with open(task_path) as f:
                task_dict = json.load(f)
                img_url = task_dict.get("img_url")
                keyinfo = task_dict.get("keyinfo")
                tcam_img_url = task_dict.get("tcam_img_url")
                tcam_keyinfo = task_dict.get("tcam_keyinfo")
                img_url_boot = task_dict.get("img_url_boot")
                keyinfo_boot = task_dict.get("keyinfo_boot")
                mcu_zip_url = task_dict.get("mcu_zip_url")
                # 如果有task.json并且所有的参数为空，则以master的版本为准
                if not any([img_url, keyinfo, tcam_img_url, tcam_keyinfo, img_url_boot, keyinfo_boot, mcu_zip_url]):
                    master_bgm = master_bench_config.bgm_version
                    master_tcam = master_bench_config.tcam_version[2:]  # tcam版本前面携带一个0
                    slave_bgm = slave_bench_config.bgm_version
                    slave_tcam = slave_bench_config.tcam_version[2:]  # tcam版本前面携带一个0
                    if master_bgm and master_bgm != slave_bgm:
                        sdb_version = master_bgm[-5:-2]
                        bgm_ver = f'v{sdb_version[0]}.{sdb_version[1]}.{sdb_version[2]}'
                        base_img_url = f'https://repo.jidudev.com/artifactory/BGMSoftware/Release/{bgm_ver}/{master_bgm}'
                        img_url = f'{base_img_url}/{master_bgm}.bin'
                        logger.info(f"bgm app包的链接为:{img_url}")
                        keyinfo = ArtifactoryHelper.get_keyinfo(url=img_url.replace('bin', 'keyinfo'))
                        logger.info(f"bgm app包的keyinfo为:{keyinfo}")
                        img_url_boot = ArtifactoryHelper.get_boot_url(url=base_img_url)
                        logger.info(f"bgm boot包的链接为:{img_url_boot}")
                        keyinfo_boot = ArtifactoryHelper.get_keyinfo(url=img_url_boot.replace('bin', 'keyinfo'))
                        logger.info(f"bgm boot包的keyinfo为:{keyinfo_boot}")
                    if master_tcam and master_tcam != slave_tcam:
                        sdb_version = master_tcam[-5:-2]
                        tcam_ver = f'v{sdb_version[0]}.{sdb_version[1]}.{sdb_version[2]}'
                        base_tcam_img_url = f'https://repo.jidudev.com/artifactory/TCAMSoftware/Release/{tcam_ver}/{master_tcam}'
                        tcam_img_url = f'{base_tcam_img_url}/{master_tcam}.bin'
                        logger.info(f"tcam包的链接为:{tcam_img_url}")
                        tcam_keyinfo = ArtifactoryHelper.get_keyinfo(url=tcam_img_url.replace('bin', 'keyinfo'))
                        logger.info(f"tcam包的keyinfo为:{tcam_keyinfo}")
        # 如果不存在task.json， 则直接按照master端的版本号进行升级
        else:
            master_bgm = master_bench_config.bgm_version
            master_tcam = master_bench_config.tcam_version[2:]  # tcam版本前面携带一个0
            slave_bgm = slave_bench_config.bgm_version
            slave_tcam = slave_bench_config.tcam_version[2:]  # tcam版本前面携带一个0
            if master_bgm and master_bgm != slave_bgm:
                sdb_version = master_bgm[-5:-2]
                bgm_ver = f'v{sdb_version[0]}.{sdb_version[1]}.{sdb_version[2]}'
                base_img_url = f'https://repo.jidudev.com/artifactory/BGMSoftware/Release/{bgm_ver}/{master_bgm}'
                img_url = f'{base_img_url}/{master_bgm}.bin'
                logger.info(f"bgm app包的链接为:{img_url}")
                keyinfo = ArtifactoryHelper.get_keyinfo(url=img_url.replace('bin', 'keyinfo'))
                logger.info(f"bgm app包的keyinfo为:{keyinfo}")
                img_url_boot = ArtifactoryHelper.get_boot_url(url=base_img_url)
                logger.info(f"bgm boot包的链接为:{img_url_boot}")
                keyinfo_boot = ArtifactoryHelper.get_keyinfo(url=img_url_boot.replace('bin', 'keyinfo'))
                logger.info(f"bgm boot包的keyinfo为:{keyinfo_boot}")
            if master_tcam and master_tcam != slave_tcam:
                sdb_version = master_tcam[-5:-2]
                tcam_ver = f'v{sdb_version[0]}.{sdb_version[1]}.{sdb_version[2]}'
                base_tcam_img_url = f'https://repo.jidudev.com/artifactory/TCAMSoftware/Release/{tcam_ver}/{master_tcam}'
                tcam_img_url = f'{base_tcam_img_url}/{master_tcam}.bin'
                logger.info(f"tcam包的链接为:{tcam_img_url}")
                tcam_keyinfo = ArtifactoryHelper.get_keyinfo(url=tcam_img_url.replace('bin', 'keyinfo'))
                logger.info(f"tcam包的keyinfo为:{tcam_keyinfo}")
        update_type = set()
        # SIL台架目前只支持sil_bgm，不支持boot
        if running_env == "SIL":
            if 'BGM' in img_url:
                task_json['update'].append(
                    {
                        "bgm": {
                            "img_url": img_url,
                            "keyinfo": keyinfo
                        }
                    }
                )
                update_type.add('sil_bgm')
        else:
            if img_url and keyinfo:
                if 'BGM' in img_url:
                    task_json['update'].append(
                        {
                            "bgm": {
                                "img_url": img_url,
                                "keyinfo": keyinfo
                            }
                        }
                    )
                    update_type.add('bgm')
                elif 'TCAM' in img_url:
                    task_json['update'].append(
                        {
                            "tcam": {
                                "img_url": img_url,
                                "keyinfo": keyinfo
                            }
                        }
                    )
                    update_type.add('tcam')
            if img_url_boot and keyinfo_boot:
                task_json['update'].append(
                    {
                        "boot": {
                            "img_url_boot": img_url_boot,
                            "keyinfo_boot": keyinfo_boot
                        }
                    }
                )
                update_type.add('bgm')
            if tcam_img_url and tcam_keyinfo:
                task_json['update'].append(
                    {
                        "tcam": {
                            "img_url": tcam_img_url,
                            "keyinfo": tcam_keyinfo
                        }
                    }
                )
                update_type.add('tcam')
            if mcu_zip_url:
                task_json['update'].append(
                    {
                        "mcu": {
                            "mcu_zip_url": mcu_zip_url,
                        }
                    }
                )
                update_type.add('mcu')
        with open(Path(parent_dir) / f"{slave_ip}.json", 'w') as task_obj:
            json.dump(task_json, task_obj, indent=4)
        return update_type

    @staticmethod
    def _scp_task_json_to_slave(**kwargs):
        hostname = kwargs.get("hostname")
        port = kwargs.get("port")
        username = kwargs.get("username")
        password = kwargs.get("password")
        is_willow = kwargs.get("is_willow")
        workspace = kwargs.get("workspace")
        client = BenchHelper.retry_scp(hostname, port, username, password)
        client.put(Path(parent_dir) / f"{hostname}.json", Path(workspace) / f"{RepoName.sat.value}" / "task.json")
        if is_willow:
            client = BenchHelper.retry_scp(hostname, port, username, password)
            client.put(Path(parent_dir) / f"../task.json", Path(workspace) / f"{RepoName.sat.value}" / "../task.json")

    @staticmethod
    def get_task_json():
        if os.path.exists(Path(parent_dir) / 'task.json'):
            with open(Path(parent_dir) / 'task.json') as task_obj:
                task_json: dict = json.load(task_obj)
            return task_json

    def set_heartbeat_status(self, status: HeartBeat):
        # 更新台架状态
        self._bench_heart_beat_status = status
        logger.debug(self._bench_heart_beat_status)

    def set_heartbeat_start(self, ip, process, status: HeartBeat, uuid):
        logger.info(f'{ip}-{process}-{uuid}心跳开始')
        self._bench_heart_beat_status = status
        dh = DatabaseHelper()
        while True:
            # logger.debug(self._bench_heart_beat_status)
            if self._bench_heart_beat_status == HeartBeat.online:
                dh.update_heart_beat(deviceId=ip, benchRole=process, masterId=uuid, log_print=False)
                logger.debug(f"发送心跳{ip}-{process}-{uuid}")
            elif self._bench_heart_beat_status == HeartBeat.offline:
                logger.info(f'{ip}-{process}-{uuid}心跳结束')
                return
            time.sleep(5)

    @staticmethod
    def get_sil_bench_type():
        domain_list = []
        cmd = "ps -ef | grep qemu | grep -v grep"
        result = exec_shell(command=cmd)
        output = result.get('output')
        if output:
            if 'bgm' in output:
                domain_list.append('BGM')
            if 'tcam' in output:
                domain_list.append('TCAM')
            if 'cdc' in output:
                domain_list.append('CCU_CD')
            if 'acu' in output:
                domain_list.append('ACU')
            if 'ccu_cd' in output:
                domain_list = ["CCU_CD"]
        logger.info(domain_list)
        return dict(domain=domain_list)
