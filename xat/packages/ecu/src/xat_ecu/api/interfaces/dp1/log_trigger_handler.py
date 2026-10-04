#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**********************
@File    : log_trigger_handler.py

**********************

------------------------------------------------------------------
@Time    : 2024/10/24 19:22
@Author  : jiewen.deng
Language: Python 3.9
------------------------------------------------------------------
Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.
"""
import ast
import copy
import random
import string
import re
import time
import io
import json
import uuid
import six
import pytz

import requests
from jsonpath_ng import parse as ng_parse
from collections import defaultdict
from xat_ecu.api.interfaces.dp1.configfile_utils import *
from dateutil import parser
# from ecu_simulator.common.data_type_handing import DataTypeHanding, int_to_4_bytes_list
# from ecu_simulator.common.logger import logger
# from ecu_simulator.sdk.tcp_framework.tcp_communicate import SocketClient
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.api.config_center.configfile_utils import *
from xat_ecu.legacy.sdk.tcp_framework.tcp_communicate import *
from xat_ecu.legacy.driver.ssh_interface import command_send
from collections import defaultdict
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding, int_to_4_bytes_list
from xat_ecu.api.abc_interface import *

CONFIGMASTER_SERVICE_CLIENT = "ConfigMasterService_client"


class SingleMeta(type):

    def __init__(cls, *args, **kwargs):
        cls._instance = None
        super(SingleMeta, cls).__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SingleMeta, cls).__call__(*args, **kwargs)
        return cls._instance


log_bgm_config_data = [
    {
        "proname": "remoteLog.t2v.logcfg",
        "value": {
            "ecuName": "BGM",
            "upload_enable": True,
            "ecuLogConfig": [
                {
                    "vlog_type_id": 1,
                    "vlog_level": "Info",
                    "vlog_logfile_size": 10,
                    "vlog_upload_interval": 65535,
                    "expired_time": 4070908800
                },
                {
                    "vlog_type_id": 4,
                    "vlog_level": "Info",
                    "vlog_logfile_size": 7,
                    "vlog_upload_interval": 65535,
                    "expired_time": 4070908800
                },
            ],
            "localTriggerUploadConfig": [
                {
                    "triggerType": 1,
                    "isUploadLog": True,
                    "logTimeScope": 0,
                    "logType": None,
                },
                {
                    "triggerType": 2,
                    "isUploadLog": True,
                    "logTimeScope": 0,
                    "logType": None,
                },
                {
                    "triggerType": 3,
                    "isUploadLog": True,
                    "logTimeScope": 0,
                    "logType": None,
                },
                {
                    "triggerType": 4,
                    "isUploadLog": True,
                    "logTimeScope": 0,
                    "logType": None,
                },
                {
                    "triggerType": 5,
                    "isUploadLog": True,
                    "logTimeScope": 0,
                    "logType": None,
                },
                {
                    "triggerType": 6,
                    "isUploadLog": True,
                    "logTimeScope": 0,
                    "logType": None,
                }
            ]
        }
    }
]

log_tcam_config_data = [
    {
        "proname": "remoteLog.t2v.logcfg",
        "value": {
            "ecuName": "TCAM",
            "upload_enable": True,
            "ecuLogConfig": [
                {
                    "vlog_type_id": 1,
                    "vlog_level": "Info",
                    "vlog_logfile_size": 20,
                    "vlog_upload_interval": 65535,
                    "expired_time": 4070908800
                },
                {
                    "vlog_type_id": 4,
                    "vlog_level": "Debug",
                    "vlog_logfile_size": 5,
                    "vlog_upload_interval": 65535,
                    "expired_time": 4070908800
                },
                {
                    "vlog_type_id": 100,
                    "vlog_level": "Debug",
                    "vlog_logfile_size": 2,
                    "vlog_upload_interval": 65535,
                    "expired_time": 4070908800
                },
                {
                    "vlog_type_id": 101,
                    "vlog_level": "Debug",
                    "vlog_logfile_size": 2,
                    "vlog_upload_interval": 65535,
                    "expired_time": 4070908800
                },
                {
                    "vlog_type_id": 102,
                    "vlog_level": "Debug",
                    "vlog_logfile_size": 2,
                    "vlog_upload_interval": 65535,
                    "expired_time": 4070908800
                }
            ],
            "localTriggerUploadConfig": [
                {
                    "triggerType": 1,
                    "isUploadLog": True,
                    "logTimeScope": 0,
                    "logType": [],
                },
                {
                    "triggerType": 2,
                    "isUploadLog": True,
                    "logTimeScope": 0,
                    "logType": [],
                },
                {
                    "triggerType": 3,
                    "isUploadLog": True,
                    "logTimeScope": 0,
                    "logType": [],
                },
                {
                    "triggerType": 4,
                    "isUploadLog": True,
                    "logTimeScope": 0,
                    "logType": [],
                }
            ]
        }
    }
]

network_config_data = [
    {
        "proname": "FunctionSwitch",
        "value": 1
    },
    {
        "proname": "NetResourceDetailFileConfig",
        "value": [
            {
                "key": "FileCreatInterval",
                "value": 800,
                "comment": "file creat interval time(s)"
            },
            {
                "key": "FileCount",
                "value": 6,
                "comment": "file count"
            },
            {
                "key": "FileCompression",
                "value": 0,
                "comment": "Compression"
            }
        ]
    }
]

log_monitor_config_data = [
    {
        "proname": "monitor_agent.t2v.logcfg",
        "value": {
            "data_channel_config": {},
            "pers_file_size": 25,  # 每个文件最大大小,单位 KB
            "wait_sys_time_sync": 30,  # 30S后默认时间同步
            "handle_data_config": [
                {
                    "data_type": 20,
                    "upload_data_interval": 30,
                    "upload_data_retry_count": 3,
                    "data_queue_max_size": 300,
                    "data_pers_file_max_size": 250,
                    "persist_file_path": "/data/monitor_agent",
                    "persist_data_interval": 180,
                    "prod_uri": "https://metric-collector.jiducar.com",
                    "stagging_uri": "https://acu-monitor-staging.jiduapp.cn",
                    "post_api": "/api/acu-monitor/api/v3/monitor/metricpush",
                    "upload_to_tsp": False,
                    "payload_compression": True
                },
                {
                    "data_type": 21,
                    "upload_data_interval": 0,
                    "upload_data_retry_count": 3,
                    "data_queue_max_size": 300,
                    "data_pers_file_max_size": 250,
                    "persist_file_path": "/data/monitor_agent",
                    "persist_data_interval": 180,
                    "prod_uri": "https://metric-collector.jiducar.com",
                    "stagging_uri": "https://acu-monitor-staging.jiduapp.cn",
                    "post_api": "/api/acu-monitor/api/v3/monitor/metricpush",
                    "upload_to_tsp": True,
                    "coredump_upload_enabled": True,
                    "wait_sys_time_sync": 30,
                    "receive_data_max_size": 10000
                }
            ]
        }
    }
]


@six.add_metaclass(SingleMeta)
class LogTriggerHandler(object):

    def __init__(self, mix):
        self.mix = mix
        self.socket = None
        self.soa = self.mix.soa
        self.ssh = self.mix.ssh
        self.io = self.mix.io
        self.log_manage = self.mix.log_manage
        self.tsp = self.mix.tsp
        self.serial = self.mix.serial
        self.bus_comm = self.mix.bus_comm
        self.diag_mock = self.mix.diag_mock
        self.sd_tester = self.mix.sd_tester

        self.bgm_log_local_config_data = copy.deepcopy(log_bgm_config_data)
        self.bgm_log_vehicle_config_data = None
        self.tcam_log_local_config_data = copy.deepcopy(log_tcam_config_data)
        self.tcam_log_vehicle_config_data = None
        self.network_local_config_data = copy.deepcopy(network_config_data)
        self.network_vehile_config_data = None
        self.log_monitor_local_config_data = copy.deepcopy(log_monitor_config_data)
        self.log_monitor_vehicle_config_data = None

    # ################ djw   ######################################################
    def start_socket(self):
        try:
            self.socket = SocketClient("172.16.5.21",
                                       random.randint(1000, 9999),
                                       "172.16.5.31", 5678)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/log_trigger_handler.py")
            logger.warning(f"启动socket 报错：{e}")

    def stop_socket(self):
        if self.socket:
            try:
                self.socket.tcp_client.close()
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/log_trigger_handler.py")
                logger.warning(f"关闭socket报错：{e}")

    def start_v2t_monitor(self, only_start_bgm=False):
        """
        启动v2t模拟器启动
        :return:
        """
        if only_start_bgm:
            self.ssh.bgm_ssh.type_commands(
                "rm -rf /data/persistent/config_*;rm -rf /data/config_service/remoteLog/*;shutdown -r")
            time.sleep(20)
        else:
            self.ssh.bgm_ssh.type_commands(
                "rm -rf /data/persistent/config_*;rm -rf /data/config_service/remoteLog/*;shutdown -r")
            self.ssh.tcam_ssh.type_commands(
                "rm -rf /mnt/sdcard/persistent2/config_*;rm -rf /mnt/sdcard/persistent/config_service/remoteLog/*")
            self.ssh.tcam_ssh.type_commands("mv /mnt/sdcard/jiduEM.sh /oemdata/bin/;reboot")
            logger.info("tcam 重启中 等待300秒")
            time.sleep(300)

    def stop_v2t_monitor(self):
        """
        关闭模拟器，回复环境至正常
        :return:
        """
        time_out = 60
        while time_out:
            self.ssh.tcam_ssh.type_commands("mv /oemdata/bin/jiduEM.sh /mnt/sdcard/")
            data = self.ssh.tcam_ssh.type_commands("ls /oemdata/bin/")
            if "jiduEM.sh.bak" in data:
                self.ssh.tcam_ssh.type_commands("mv /oemdata/bin/jiduEM.sh.bak /oemdata/bin/jiduEM_bak.sh")
            if "jiduEM.sh_backup" in data:
                self.ssh.tcam_ssh.type_commands("mv /oemdata/bin/jiduEM.sh_backup /oemdata/bin/jiduEM.sh_backup")
            if "jiduEM.sh" not in data:
                logger.info("配置文件清除成功")
                self.ssh.tcam_ssh.type_commands("reboot")
                break
            else:
                time_out -= 1
                time.sleep(2)
                logger.info("等待清除配置文件")
        time.sleep(300)

    def trigger_config_to_get_keywords(self,
                                       domain="BGM",
                                       trigger_type=1,
                                       log_type="RLog",
                                       update_field="$[0].value.upload_enable",
                                       new_value=None,
                                       keywords="Recv a upload event, but upload_enable is false, event is webuser",
                                       source=1,
                                       tach_upload_source=1,
                                       event=None,
                                       only_trigger=False,
                                       time_out=10 * 60):
        """

        :param domain:
        :param trigger_type: trigger_type:1,v2t模拟器触发方式；trigger_type:2，立即上传；trigger_type:3，远程上传
        :param log_type:
        :param update_field:
        :param new_value:
        :param keywords:
        :param source:1：模拟器发送数据；2：模拟tcam，server方式配置下发
        :param tach_upload_source: 触发上传source参数
        :param event: event参数
        :param only_trigger: 只做触发
        :param time_out:
        :return:
        """
        try:
            if not only_trigger:
                self.log_manage.log_manage.check_log_by_keywords_start_thread(
                    log_type=log_type,
                    keywords=keywords,
                    unexpect_keywords=None,
                    log_print=None,
                    device_name=domain,
                    timeout=time_out
                )
                time.sleep(5)
            if trigger_type == 1:
                if not isinstance(update_field, list):
                    update_field_list = [update_field]
                else:
                    update_field_list = update_field
                if not isinstance(new_value, list):
                    new_value_list = [new_value]
                else:
                    new_value_list = new_value
                if len(update_field_list) != len(new_value_list):
                    logger.warning(f"需要改变得字段和值个数不相等，请仔细检查...")
                    raise
                for i, update_field in enumerate(update_field_list):
                    config_type = "bgm_rlog" if domain == "BGM" else "tcam_rlog"
                    self.update_config_data(config_type=config_type, update_field=update_field,
                                            new_value=new_value_list[i])
                inner_type = 'bgm_remote' if domain == "BGM" else "tcam_remote"
                self.config_trigger_to_valid(inner_type, source=source)
            elif trigger_type == 2:
                if domain == "BGM":
                    partner_key = "RemoteLogManagerService_client_BGM_RemoteLogManagerService"
                else:
                    partner_key = "RemoteLogManagerService_client_TCAM_RemoteLogManagerService"
                self.send_soa_request(partner_key,
                                                              "ReqUploadLog",
                                                              {"triggerSourceInfo": {"source": tach_upload_source,
                                                                                     "event": event,
                                                                                     "request_id": str(uuid.uuid4()),
                                                                                     "ctrlParam": "wsxcdefvgthjuu"}})
            elif trigger_type == 3:
                if domain == "BGM":
                    partner_key = "V2TRoutingForwarder_client_V2TLogBGMForwarder"
                else:
                    partner_key = "V2TRoutingForwarder_client_V2TLogTCAMForwarder"
                entries = self.get_tcam_log_files(1)
                payload = json.dumps({"request_id": str(uuid.uuid4()), "event": event, "entries": entries})
                ascii_list = [ord(char) for char in payload]
                method_name = "CallVehicleApi",
                soa_parameters = {"api": 'UploadFilesRequest',
                                  'payload': ascii_list,
                                  'traceId': f"123456"}
                self.send_soa_request(partner_key, method_name, soa_parameters, timeout=5)
        finally:
            if not only_trigger:
                ret, jet_log_msg = self.log_manage.log_manage.check_log_by_keywords_stop_thread()
                if ret:
                    logger.info(f"过滤到：{keywords}")
                else:
                    raise

    def check_file_size_by_type(self, check_all_size, allow_offset=30, check_dir_path="", time_out=60, domain="BGM"):
        """
        超时时间内，校验文件的总大小根据类型
        :param check_all_size: 需要检查类型文件总大小,单位字节
        :param allow_offset: 允许最大文件大小的偏差，单位字节
        :param check_dir_path: 检查的文件路径目录
        :param time_out: 需要检查的一段时间
        :param domain:
        :return:
        """
        start_time = int(time.time())

        data_dict = {"event_data": {}, "metric_data": {}}
        while time.time() - start_time < time_out:
            file_info = self.get_work_tree_by_path(domain=domain, path=check_dir_path)
            for file_list in file_info:
                result = re.findall(f".*event_data_(\d+).log.*", file_list[2])
                if result:
                    data_dict["event_data"][file_list[2]] = file_list[1]

                result = re.findall(f".*metric_data_(\d+).log.*", file_list[2])
                if result:
                    data_dict["metric_data"][file_list[2]] = file_list[1]

            event_max_size = sum([i for i in data_dict["event_data"].values()])
            logger.info(f"event_max_size is:{event_max_size}")
            if event_max_size - check_all_size > allow_offset:
                logger.warning(f"event 类型文件总大小：{event_max_size} 大于检查大小：{check_all_size}")
                raise

            metric_max_size = sum([i for i in data_dict["metric_data"].values()])
            logger.info(f"metric_max_size is:{metric_max_size}")
            if metric_max_size - check_all_size > allow_offset:
                logger.warning(f"metric 类型文件总大小：{metric_max_size} 大于检查大小：{check_all_size}")
                raise
            time.sleep(5)

    def check_file_size_by_time(self, check_max_size, allow_offset=30, time_after=None, check_dir_path="", time_out=300,
                                domain="BGM"):
        """
        超时时间内，校验文件的最大大小
        :param time_after: 从某个时间后开始计算文件大小
        :param check_max_size: 需要检查最大文件的大小,单位字节
        :param allow_offset: 允许最大文件大小的偏差，单位字节
        :param check_dir_path: 检查的文件路径目录
        :param time_out: 需要检查的一段时间
        :param domain:
        :return:
        """
        start_time = int(time.time())

        metric_data_max_count = 0
        event_data_max_count = 0

        current_event_max_count = 0
        current_metric_max_count = 0
        if not time_after:
            check_time_start = int(time.time())
        else:
            check_time_start = time_after
        logger.info(f"开始计算文件有效的起始时间是：{check_time_start}")
        while time.time() - start_time < time_out:
            file_info = self.get_work_tree_by_path(domain=domain, path=check_dir_path)

            for file_list in file_info:
                if file_list[0] + 8 * 60 * 60 >= check_time_start:
                    logger.info(
                        f"文件时间：{file_list[0] + 8 * 60 * 60}，开始计算文件有效的起始时间是：{check_time_start}")
                    result = re.findall(f".*event_data_(\d+).log.*", file_list[2])
                    if result:
                        if int(result[0]) > event_data_max_count:
                            event_data_max_count = int(result[0])

                    result = re.findall(f".*metric_data_(\d+).log.*", file_list[2])
                    if result:
                        if int(result[0]) > metric_data_max_count:
                            metric_data_max_count = int(result[0])

            if event_data_max_count:
                logger.info(
                    f"current_event_max_count:{current_event_max_count};event_data_max_count:{event_data_max_count}")
                if current_event_max_count == 0 and event_data_max_count != 0:
                    current_event_max_count = copy.deepcopy(event_data_max_count)
                elif current_event_max_count != 0 and event_data_max_count != current_event_max_count:
                    for file_list in file_info:
                        if str(file_list[2]).endswith(f"event_data_{current_event_max_count}.log"):
                            if abs(check_max_size - file_list[1]) <= allow_offset:
                                logger.info(f"{file_list[2]}:的大小：{file_list[1]} 小于,允许的：{check_max_size}")
                                return

            if metric_data_max_count:
                logger.info(
                    f"metric_data_max_count:{metric_data_max_count};current_metric_max_count:{current_metric_max_count}")
                if current_metric_max_count == 0 and metric_data_max_count != 0:
                    current_metric_max_count = copy.deepcopy(metric_data_max_count)
                elif current_metric_max_count != 0 and metric_data_max_count != current_metric_max_count:
                    for file_list in file_info:
                        if str(file_list[2]).endswith(f"metric_data_{current_metric_max_count}.log"):
                            if abs(check_max_size - file_list[1]) <= allow_offset:
                                logger.info(f"{file_list[2]}:的大小：{file_list[1]} 小于,允许的：{check_max_size}")
                                return

            time.sleep(5)
        logger.warning(f"超时时间内，没有检查到文件按照规定大小生成。")
        raise

    def check_monitor_payload_compression(self, domain="BGM", check_compression_status=True, time_out=300):
        if check_compression_status:
            keywords = "compressed data size:"
            # keywords = "compressed data size: ***%d, origin data size: ***%d"
        else:
            keywords = "upload data directly, not compress"
        self.log_manage.log_manage.check_log_by_keywords_start_thread(
            log_type="monitor_a:",
            keywords=keywords,
            unexpect_keywords=None,
            log_print=None,
            device_name=domain,
            timeout=time_out
        )
        time.sleep(5)
        ret, jet_log_msg = self.log_manage.log_manage.check_log_by_keywords_stop_thread()
        if ret:
            logger.info(f"过滤到：{keywords}")

    def check_dir_new_file_compression(self,
                                       domain="BGM",
                                       check_dir="/log/net_resource_manager_tmp",
                                       check_compression=True
                                       ):
        """
        判断目录下最新文件是否为压缩文件
        :param domain:
        :param check_dir: 需要检查最新文件所在的目录
        :param check_compression: 需要检查最新文件是否压缩
        :return:
        """
        file_info = self.get_work_tree_by_path(domain=domain, path=check_dir)
        logger.info(f"path:{check_dir},has file:{file_info}")
        if not file_info:
            logger.warning(f"{check_dir}目录下没有发现有文件")
            raise
        new_file_time = 0
        new_file = None
        for i in file_info:
            if i[0] > new_file_time:
                new_file_time = i[0]
        for i in file_info:
            if i[0] == new_file_time:
                new_file = i[2]
                break
        if domain == "BGM":
            result = self.ssh.bgm_ssh.type_commands(f"file -i {new_file}")
        else:
            result = self.ssh.tcam_ssh.type_commands(f"file -i {new_file}")
        if check_compression:
            if "charset=binary" not in result:
                raise
        else:
            if "charset=us-ascii" not in result:
                raise

    def verify_time_synchronization_and_log(self, device_name, now_local, expected_log_fragment):
        # # 当前时间
        # now_local = datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")
        # logger.info(f"{now_local}时开始执行用例")
        # time.sleep(5)
        log_command = "/app/bin/zstdcat /log/jetlog_messages | grep 'vehicle_time:' | grep -E 'set system time|time is|set rtc time|Set UTC Time to MCU succeed|VehicleTimeInfo|ptp4l'"
        string0 = self.ssh.type_commands(device_name, log_command)
        # 验证是否存在更新RTC时间的日志
        assert 'set rtc time' in string0 and expected_log_fragment in string0, f"No match update rtc time or {expected_log_fragment}"
        # 获取设置系统时间的信息
        string1 = self.ssh.type_commands(DeviceName.BGM,
                                         "/app/bin/zstdcat /log/jetlog_messages | grep 'vehicle_time:' | grep 'set system time' | tail -1")
        pattern1 = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3})\s+\d+\s+\d+\s+.*: (\d+)'  # 提取时间和日期
        match1 = re.search(pattern1, string1)
        if match1:
            init_time = parser.parse(match1.group(1))
            default_time = parser.parse("2021-01-01 08:00:00.0")  # 东八区时间
            assert abs(init_time - default_time).seconds <= 8, f'BGM{init_time}时开始set system time'
        else:
            logger.info(f"No match found for set system time")
        logger.info(f'BGM{init_time}时开始set system time')
        set_sys_time_ms = match1.group(2)
        set_sys_time_s = int(set_sys_time_ms) / 1000
        set_sys_time = parser.parse(
            datetime.datetime.fromtimestamp(set_sys_time_s).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        logger.info(f"设置BGM系统时间为：{set_sys_time}")
        assert (set_sys_time - parser.parse(
            now_local)).seconds < 30, f'本次获取到的log非本次执行的记录{parser.parse(now_local)}脚本开始执行'
        # 获取ptp4l启动成功的时间
        string2 = self.ssh.type_commands(DeviceName.BGM,
                                         "/app/bin/zstdcat /log/jetlog_messages | grep 'vehicle_time:' | grep 'start ptp4l Succeed' |tail -1")
        pattern2 = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3})\s+'
        match2 = re.search(pattern2, string2)
        if match2:
            bgm_sys_time = parser.parse(match2.group(1))
            logger.info(f"BGM系统时间为：{bgm_sys_time}")
            assert abs(bgm_sys_time - set_sys_time).seconds < 0.01, f'BGM系统时间为：{bgm_sys_time}'
        else:
            raise ValueError("No match found for start ptp4l Succeed")

    def check_path_file_max_file(self,
                                 domain="BGM",
                                 check_path="/log/net_resource_manager",
                                 check_max_count=5
                                 ):
        """
        检查某个路径下文件数最大值
        :param domain:
        :param check_path:
        :param check_max_count:
        :return:
        """
        retry_times = 2
        while retry_times:
            file_info = self.get_work_tree_by_path(domain=domain, path=check_path)
            logger.info(f"目录文件：{file_info}")
            if len(file_info) > check_max_count:
                logger.warning(f"路径：{check_path}下文件有：{len(file_info)}个，期望最大：{check_max_count}")
                retry_times -= 1
                continue

    def check_net_resource_manager_create_file_by_time(self,
                                                       domain="BGM",
                                                       check_create_path="/log/net_resource_manager",
                                                       check_create_time=60,
                                                       offset_time=2
                                                       ):
        """
        检查目录文件新增
        :param domain:
        :param check_create_path:
        :param check_create_time:
        :return:
        """
        start_file_info = self.get_work_tree_by_path(domain=domain, path=check_create_path)
        logger.info(f"等待前文件：{[i[2] for i in start_file_info]}")
        logger.info(f"等待：{check_create_time} S中...;检查目录是否新产生文件。")
        time.sleep(int(check_create_time) + offset_time)
        end_file_info = self.get_work_tree_by_path(domain=domain, path=check_create_path)
        logger.info(f"等待后文件：{[i[2] for i in end_file_info]}")
        add_file = set([i[2] for i in end_file_info]) - set([i[2] for i in start_file_info])
        logger.info(f"文件差异为：{add_file}")
        if len(add_file) != 1:
            raise

    def check_net_resource_manager_tmp_dir_change_status(self,
                                                         domain="BGM",
                                                         check_path='/log/net_resource_manager_tmp',
                                                         check_time=10 * 60,
                                                         check_status="no_change"
                                                         ):
        """
        检查net_resource_manager_tmp目录下不发生变化
        :param domain: BGM/TCAM
        :param check_path: 检查路径
        :param check_time: 检查10分钟不发生变化
        :param check_status: 检查状态是否发生变化，check_status：不发生变化；change:发声变化
        :return:
        """
        start_file_info = self.get_work_tree_by_path(domain=domain, path=check_path)
        logger.info(f"等待前文件：{start_file_info}")
        logger.info(f"等待：{check_time} S中...;检查目录：{check_path}不发生变化。")
        time.sleep(int(check_time))
        end_file_info = self.get_work_tree_by_path(domain=domain, path=check_path)
        logger.info(f"等待后文件：{end_file_info}")

        if not start_file_info:
            if check_status == "no_change":
                if end_file_info:
                    logger.warning(f"开始没有发现：{check_path} 有文件，之后发现有：{end_file_info}")
                    raise
            else:
                if not end_file_info:
                    logger.warning(f"开始没有发现：{check_path} 有文件，之后也没有：{end_file_info}")
                    raise

        if check_status == "no_change":
            if len(start_file_info) != len(end_file_info):
                logger.warning(f"检查时间前长度：{len(start_file_info)}，不等于检查后长度：{len(end_file_info)}")
                raise
        if check_status == "no_change":
            for s_info in start_file_info:
                flag = False
                for d_info in end_file_info:
                    if s_info[2] == d_info[2]:
                        if s_info[0] != d_info[0]:
                            logger.warning(f"文件：{s_info[2]}，前后修改时间不等：{s_info[0]}->{d_info[0]}")
                            raise
                        if s_info[1] != d_info[1]:
                            logger.warning(f"文件：{s_info[2]}，前后文件大小不等：{s_info[1]}->{d_info[1]}")
                            raise
                        flag = True
                        break
                if not flag:
                    logger.warning(f"等待时间：{check_time}后，没有发现文件：{s_info[2]}")
                    raise
        else:
            flag = False
            for s_info in start_file_info:
                for d_info in end_file_info:
                    if s_info[2] == d_info[2]:
                        if s_info[0] != d_info[0]:
                            logger.warning(f"文件：{s_info[2]}，前后修改时间不等：{s_info[0]}->{d_info[0]}")
                            flag = True
                            break
                        if s_info[1] != d_info[1]:
                            logger.warning(f"文件：{s_info[2]}，前后文件大小不等：{s_info[1]}->{d_info[1]}")
                            flag = True
                            break
                        logger.info(f"文件：{s_info[2]}，没有发生改变")
                        break

                if flag:
                    logger.info(f"已经发现文件有变化...")
                    return
            if not flag:
                logger.warning(f"发现文件没有变化。")
                raise

    def get_tree_dir_data(self, domain, timeout):
        """
        触发类似云平台获取目录树，并解析日志中获取的文件，
        :param domain:
        :param timeout:
        :return: [(修改时间, 大小，文件名),....]
        """
        self.log_manage.log_manage.check_log_by_keywords_start_thread(
            log_type="RLog",
            keywords='server response: {"code":0,"data":null,"msg":"OK"}',
            unexpect_keywords=None,
            log_print=None,
            device_name=domain,
            timeout=timeout
        )
        time.sleep(10)
        self.remote_dir_check_trigger(domain)
        logger.info("已经发送目录树结构获取指令。")
        ret, vehicle_log = self.log_manage.log_manage.check_log_by_keywords_stop_thread()
        logger.info(f"vehicle_log={vehicle_log}")
        assert ret, f"超时{timeout}秒日志未上传结束"

    def _int_to_4_bytes_list(self, int_data):
        # such as    386 ---->> [0x01, 0x82]
        bytes_list = (
                [(int_data >> 24) & 0xFF]
                + [(int_data >> 16) & 0xFF]
                + [(int_data >> 8) & 0xFF]
                + [int_data & 0xFF]
        )
        return bytes_list

    def recover_v2t_to_normal_env(self):
        """
        恢复v2t模拟器环境到正常环境
        :return:
        """
        time_out = 60
        while time_out:
            self.ssh.tcam_ssh.type_commands("mv /oemdata/bin/jiduEM.sh /mnt/sdcard/")
            data = self.ssh.tcam_ssh.type_commands("ls /oemdata/bin/")
            if "jiduEM.sh.bak" in data:
                self.ssh.tcam_ssh.type_commands("mv /oemdata/bin/jiduEM.sh.bak /oemdata/bin/jiduEM_bak.sh")

            if "jiduEM.sh_backup" in data:
                self.ssh.tcam_ssh.type_commands("mv /oemdata/bin/jiduEM.sh_backup /oemdata/bin/jiduEM_bak.sh")
            if "jiduEM.sh" not in data:
                logger.info("配置文件清除成功")
                self.ssh.tcam_ssh.type_commands("reboot")
                break
            else:
                time_out -= 1
                time.sleep(2)
                logger.info("等待清除配置文件")
        time.sleep(180)

    def v2t_simulator_Configuration(self, domain, appname, confname, value):
        """
        V2T模拟器发送请求
        :param domain:
        :param appname:
        :param confname:
        :param value:
        :return:
        """
        pb_ver = "V1"
        name = "MarsOne"
        year = "2024"
        action = 0
        conftype = 0
        pushtype = 1
        SyncStrategy = 3

        logger.info(f"配置文件内容为:{value}")
        # 模拟云端下发配置文件
        cmd = ConfigMasterV2TCmd(pb_ver, name, year, domain, appname, confname, action, conftype, pushtype,
                                 SyncStrategy, value, True)
        payload = cmd.return_v2t_cmd_bytes()
        logger.info(f"发送的master数据指令{payload}")
        logger.info(f"master字节长度{len(payload) / 2}")
        cloudcmd = VehicleCloudCmd(pb_bytes=DataTypeHanding.to_bytes(payload))
        cloud_payload = cloudcmd.return_cmd_bytes()
        logger.info(f"发送的车云数据指令{cloud_payload}")
        logger.info(f"云端v2t指令字节长度{len(cloud_payload) / 2}")
        ck_data = DataTypeHanding.hexstr_to_inlist("12345678") + int_to_4_bytes_list(
            int(len(cloud_payload) / 2)) + DataTypeHanding.hexstr_to_inlist(cloud_payload)
        cloud_cmd = DataTypeHanding.intlist_to_hexstr(ck_data)
        logger.info(f"发送的数据{cloud_cmd}")
        logger.info(f"组包后新字节长度{len(cloud_cmd) / 2}")
        logger.info(f"转换后的字节数组{ck_data}")

        self.socket.send_data_to_server(ck_data)
        self.socket.listen_data_from_server()
        time.sleep(10)
        revc_data = self.socket.received_data
        while True:
            if "12345678" == revc_data[:8]:
                logger.info(f"接收到的字节串{revc_data}")
                logger.info(revc_data[8:16])
                data_len = DataTypeHanding.to_int(DataTypeHanding.hexstr_to_inlist(revc_data[8:16]))
                data = revc_data[16:(16 + data_len * 2)]
                logger.info(f"接收的data为{data}")
                report_data = VehicleCloudInvoke()
                report_data.ParseFromString(DataTypeHanding.to_bytes(data))
                logger.info(f"接收到云端的header信息{report_data.header}")
                logger.info(f"接收到云端的body信息{report_data.body}")
                interface = report_data.header.reqTarget.api

                if "checkConfigVersion" in interface:
                    resp_data = NotifyData()
                    resp_data.ParseFromString(DataTypeHanding.to_bytes(DataTypeHanding.to_hexstr(report_data.body)))
                    logger.info(f'车端主动上报的应用信息{resp_data.Detail}')
                    for i in resp_data.Detail:
                        if domain == i.Domain and appname == i.AppName:
                            for j in i.StatusData:
                                if j.StageType == "RT_MASTER_RECEIVED":
                                    assert j.StatusType == 'ST_SUCCESS'
                                elif j.StageType == "RT_CONFIG_SERVER_RECEIVED":
                                    assert j.StatusType == 'ST_SUCCESS'

                elif "configStatusReport" in interface:
                    resp_data = ConfigStatusReport()
                    resp_data.ParseFromString(DataTypeHanding.to_bytes(DataTypeHanding.to_hexstr(report_data.body)))
                    logger.info(f'车端接收到配置后上报的信息{resp_data}')
                    for i in resp_data.Data:
                        if domain == i.Domain and appname == i.AppName:
                            for j in i.StatusData:
                                if j.StageType == "RT_MASTER_RECEIVED":
                                    assert j.StatusType == 'ST_SUCCESS'
                                elif j.StageType == "RT_CONFIG_SERVER_RECEIVED":
                                    assert j.StatusMessage == 'ok'
                                    assert j.StatusType == 'ST_SUCCESS'

                elif "syncServiceEvent" in interface:
                    event = ServiceEventReq()
                    event.ParseFromString(DataTypeHanding.to_bytes(DataTypeHanding.to_hexstr(report_data.body)))
                    logger.info(f'接收到车端的event信息{event.events}')

                elif "TspAppConfigSet" in interface:
                    resp = ConfSyncDataResp()
                    resp.ParseFromString(DataTypeHanding.to_bytes(DataTypeHanding.to_hexstr(report_data.body)))
                    logger.info(f'接收到车端的响应信息{resp.Details}')
                    for i in resp.Details:
                        assert i.Status == 1
                        assert i.StatusMessage == "success"
                revc_data = revc_data[(16 + data_len * 2):]
            else:
                break
        self.soa.ck_s2s_event(CONFIGMASTER_SERVICE_CLIENT, "ConfigDataNotify",
                              {"ecuName": domain, "info": {"ecuName": domain}})
        time.sleep(10)

    def remote_upload_file_trigger(self, only_upload_new_file_count=None, customize_file_list=[], domain="BGM"):
        """
        远程上传文件接口
        :param only_upload_new_file_count: 上传最新的几个文件，如:only_upload_new_file_count=2
        :param customize_file_list: 自定义上传文件列表，列表里面的zst文件
        :param domain:
        :return:
        """

        if customize_file_list:
            if not isinstance(customize_file_list, list):
                entries = [customize_file_list]
            else:
                entries = customize_file_list
        else:
            if domain == "BGM":
                entries = self.get_bgm_log_files(only_upload_new_file_count)
            else:
                entries = self.get_tcam_log_files(only_upload_new_file_count)

        payload = json.dumps({"request_id": str(uuid.uuid4()), "event": "remote_fetch", "entries": entries})
        ascii_list = [ord(char) for char in payload]
        service = "V2TRoutingForwarder_client_V2TLogBGMForwarder" if domain.upper() == "BGM" else "V2TRoutingForwarder_client_V2TLogTCAMForwarder"
        var = self.send_soa_request(service,
                                                    "CallVehicleApi",
                                                    {"api": 'UploadFilesRequest',
                                                     'payload': ascii_list,
                                                     'traceId': f"123456"},
                                                    timeout=10)["out"]
        return entries

    def remote_dir_check_trigger(self, domain="BGM"):
        """
        远程目录检查触发
        :param domain:
        :return:
        """
        payload = json.dumps({"request_id": str(uuid.uuid4())})
        ascii_list = [ord(char) for char in payload]
        if domain == "BGM":
            service = "V2TRoutingForwarder_client_V2TLogBGMForwarder"
        else:
            service = "V2TRoutingForwarder_client_V2TLogTCAMForwarder"
        var = self.send_soa_request(service,
                                                "CallVehicleApi",
                                                {
                                                    "api": 'DirectoryTreeRequest',
                                                    'payload': ascii_list,
                                                    'traceId': f"123456"})

    def check_work_tree_equal_upload_data(self,
                                          domain="BGM",
                                          log_path=f"/log/",
                                          time_out=10 * 60,
                                          allow_time_offset=30,
                                          allow_size_offset=5*1024,
                                          do_assert=True):
        """
        检查本地目录和远程触发获取目录的值是否一致
        :param domain:
        :param log_path:
        :param time_out:
        :param do_assert: 默认为true ，执行失败则会报错，为false 时候则有返回值
        :param allow_time_offset: 允许对比的文件时间偏差
        :param allow_size_offset: 允许对比的文件大小偏差
        :return: 0/1 0 表示失败，1 表示成功
        """
        if not isinstance(log_path, list):
            log_path = [log_path]

        parse_data0 = []
        for i in log_path:
            _d = self.get_work_tree_by_path(i, domain)
            if _d:
                parse_data0 += _d
        if domain.upper() == "TCAM":
            self.log_manage.log_manage.device_name = "TCAM"
        else:
            self.log_manage.log_manage.device_name = "BGM"
        self.log_manage.log_manage.check_log_by_keywords_start_thread(
            log_type="RLog",
            keywords='server response: {"code":0,"data":null,"msg":"OK"}',
            unexpect_keywords=None,
            log_print=None,
            device_name=domain,
            timeout=time_out
        )
        time.sleep(5)
        self.remote_dir_check_trigger(domain=domain)
        ret, jet_log_msg = self.log_manage.log_manage.check_log_by_keywords_stop_thread()
        with open("test_jetlog.txt", "w", encoding="utf-8") as f:
            f.write(jet_log_msg)
        parse_data = self.get_work_tree_by_log(log_data=jet_log_msg, domain=domain)
        logger.info(f"parse_data:{parse_data}")
        parse_data1 = []
        for i in log_path:
            _d = self.get_work_tree_by_path(i, domain)
            if _d:
                parse_data1 += _d

        fail_flag = False
        for index, value in enumerate(parse_data):
            flag = False
            inner_count = None
            for i, j in enumerate(parse_data1):
                if value[2] == j[2]:
                    if str(value[2]).endswith("current"):
                        logger.info(f"发现current文件：{value[2]}，跳过不匹配...")
                        flag = True
                        inner_count = j
                        break
                    if value[0] != j[0]:
                        if abs(value[0] - j[0]) > allow_time_offset:
                            logger.warning(f"文件比对不匹配{value}-----|{j}")
                            fail_flag = True
                        else:
                            logger.info(f"文件修改时间不匹配，但是在误差范围内{value}-----|{j}")
                    if value[1] != j[1]:
                        if abs(value[1] - j[1]) > allow_size_offset:
                            logger.warning(f"文件比对不匹配{value}-----|{j}")
                            fail_flag = True
                        else:
                            logger.info(f"文件大小不匹配，但是在误差范围内{value}-----|{j}")
                    flag = True
                    inner_count = j
                    logger.info(f"---文件{value[2]}的修改时间和文件大小比对成功---")
                    break
            if not flag:
                for z, w in enumerate(parse_data0):
                    if value[2] == w[2]:
                        if value[0] != w[0]:
                            if abs(value[0] - w[0]) > allow_time_offset:
                                logger.warning(f"文件比对不匹配{value}-----|{w}")
                                fail_flag = True
                            else:
                                logger.info(f"文件修改时间不匹配，但是在误差范围内{value}-----|{j}")
                        if value[1] != w[1]:
                            if abs(value[1] - w[1]) > allow_size_offset:
                                logger.warning(f"文件比对不匹配{value}-----|{w}")
                                fail_flag = True
                            else:
                                logger.info(f"文件大小不匹配，但是在误差范围内{value}-----|{j}")
                        flag = True
                        logger.info(f"---文件{value[2]}的修改时间和文件大小比对成功---")
                        break
                if not flag:
                    logger.error(f"{value}不在parse_data1中,也不在parse_data0中")
                    fail_flag = True
            if inner_count:
                parse_data1.remove(inner_count)
        logger.info(f"还未对比的本地文件有:{parse_data1}")

        if fail_flag:
            if do_assert:
                assert False
            return 0
        return 1

    def __get_tree_data(self, data, path="", result=[]):
        for info in data:
            if not info.get("children"):
                if info["modified_time"]:
                    result.append((int(info["modified_time"]), info["size"], path + info["name"]))
            else:
                if path and not str(info["name"]).startswith("/"):
                    path = path + info["name"]
                    path = path if path.endswith('/') else path + "/"
                else:
                    path = info["name"]
                self.__get_tree_data(info["children"], path)
                path_list = [i for i in path.split('/') if i]
                if len(path_list) >= 2:
                    path = '/' + "/".join(path_list[:-1]) + "/"
        return result

    def get_work_tree_by_log(self, log_data, domain="BGM"):
        """

        :param log_data:
        :param domain:
        :return: [('1729744880', '/log/jetlog_messages1_20210101080001_0c668e94b70845d2bedabdc85b2970a5.zst', 10286171), ('1729763033', '/log/jetlog_s2s2_20241024174142_cfab0bf5e6a049738c449cf0b8ced5df.zst', 39638), ('1729762902', '/log/jetlog_messages5_20241024163418_ff8aec0ed9564a4ca419c53bf9d00b77.zst', 8659736), ('1729753856', '/log/jetlog_messages3_20241024140711_13f74f7a229f427ca38f85d85e0a9093.zst', 10290179), ('1729759778', '/log/jetlog_bts2_20241024140726_a7500c292f1f4008bde24d63d1f53f5b.zst', 10284617), ('1729763033', '/log/jetlog_bts4_20241024174142_63e2a783921e4817806183af25e02433.zst', 171429), ('1729750041', '/log/net_resource_manager/net_resource_detail_3_20241024061720_58b14e34-7d1a-4274-8a21-6a587cebe7a0.zst', 10322), ('1729759864', '/log/net_resource_manager/net_resource_detail_5_20241024090104_32c749de-5ceb-45a8-b612-3e0be96f6ffb.zst', 10934), ('1729746441', '/log/net_resource_manager/net_resource_detail_2_20241024051720_f3aa7593-6ed3-439c-a385-5af0d8b00c7c.zst', 10056), ('1729742841', '/log/net_resource_manager/net_resource_detail_1_20241024041720_986f9aa6-ef1b-4e0a-ae3e-653aa1e6be3a.zst', 11977), ('1729756264', '/log/net_resource_manager/net_resource_detail_4_20241024080104_d916c76b-2e7f-434f-a819-6b0717b88de3.zst', 19992), ('1729753769', '/log/net_resource_manager/coredump/core_220AD.vehInfoServer.1575', 19718144), ('1729762277', '/log/net_resource_manager/coredump/core_220AD.vehInfoServer.1580', 19718144), ('1729739958', '/log/net_resource_manager/coredump/core_220AE.em2.431', 293380096), ('1729741043', '/log/net_resource_manager/coredump/core_220AE.vehInfoServer.1598', 19718144), ('1729750031', '/log/net_resource_manager/coredump/jetlog_messages2_20241024124120_6438b454195b42698428c012c8ce4b87.zst', 10288199), ('1729762946', '/log/net_resource_manager/coredump/jetlog_messages6_20241024174142_1480f1b309e84d44a97dbf6767f73862.zst', 1039219), ('', '/log/net_resource_manager/coredump/syslogs', -1), ('', '/log/net_resource_manager/coredump/nids', -1), ('', '/log/net_resource_manager/coredump/net_resource_manager_tmp', -1), ('1729762990', '/log/net_resource_manager/coredump/jetlog_messages7_20241024174226_9e51a0e4e8854f1b8218933eea8ed2ec.zst', 1029828), ('', '/log/net_resource_manager/coredump/jetcrash', -1), ('1729762902', '/log/net_resource_manager/coredump/jetlog_s2s1_20210101080002_849e3ca582fa4963bb164814a1b00735.zst', 6341586), ('1729763038', '/log/net_resource_manager/coredump/jetlog_messages9_20241024174354_a933fb807fcf43899eb358999872ab3c.zst', 94662), ('1729762902', '/log/net_resource_manager/coredump/jetlog_bts3_20241024164938_306a5c3775e24b57a503369fc85ae77d.zst', 3813365), ('1729758857', '/log/net_resource_manager/coredump/jetlog_messages4_20241024151056_4fe881e8e3f34274b2afba8f84643cf6.zst', 10287928), ('1729750046', '/log/net_resource_manager/coredump/jetlog_bts1_20210101080002_0b9263e6f92f423bb49e9b0cee998f3d.zst', 10281766), ('1729763034', '/log/net_resource_manager/coredump/jetlog_messages8_20241024174310_6e248caeb10b4fdfbd3c2de795fe566d.zst', 1035108)]
        """
        re_data = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3} \d+ \d+ \w RLog: \d+: \[V2TForwarder.cpp:\d+\]:|\n)\s*"
        temp = re.split(re_data, log_data, flags=re.I)
        dir_dict = {}
        if temp:
            result = ""
            for i in temp:
                if domain == 'TCAM':
                    match_data2 = re.findall(r"V2TForwarder.cpp:\d+", i)
                    match_data3 = re.findall(r"RLog", i)
                    if not (match_data2 or match_data3):
                        result += i
                elif domain == 'BGM':
                    match_data = re.findall(r"\d{4}-\d{2}-\d{2}", i)
                    if not match_data:
                        result += i
            result = result.replace("\n", "")
            start_count = result.index('{"entities"')
            result = result[start_count:]
            re_count = None
            if not result.endswith("}"):
                for index, value in enumerate(result[::-1]):
                    if value == "}":
                        re_count = index
                        break
            if re_count:
                result = result[:-re_count]
            with open("test222.txt", "w", encoding="utf-8") as f:
                f.write(result)
            dir_dict = json.loads(result)
        return self.__get_tree_data(dir_dict["entities"])

    def datetime_to_timestamp(self, date, short=False):
        try:
            st = time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S'))
        except ValueError:
            raise ValueError('Please input right date type "%Y-%m-%d %H:%M:%S"!')
        return st * 1000 if short else st

    def get_work_tree_by_path(self, path, domain="BGM"):
        if domain.upper() == "BGM":
            cmd = f"find {path} " + r"-type f -exec stat --format '%y %s %n' {} \;"
            result = self.ssh.bgm_ssh.type_commands(cmd)
            temp = re.findall(r".*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).* \+0000 (\d+) (.*)", result)
            if temp:
                rs = []
                for info in temp:
                    rs.append((int(self.datetime_to_timestamp(info[0]))+8*60*60, int(info[1]), info[2]))
                return rs
        elif domain.upper() == "TCAM":
            # cmd = f"find {path} " + "-type f -exec ls --full-time {} \;"
            cmd = f"find {path} " + "-type f -exec stat -c '%y %s %n' {} \;"
            result = self.ssh.tcam_ssh.type_commands(cmd)
            # temp = re.findall(r".*root/s+(\d+)\s(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \+0000 (.*)", result)
            temp = re.findall(r".*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\.\d+\s(\d+) (.*)", result)
            if temp:
                rs = []
                for info in temp:
                    rs.append((int(self.datetime_to_timestamp(info[0]))+8*60*60, int(info[1]), info[2]))
                return rs
        else:
            logger.warning(f"domain error:{domain}")
            return

    def get_bgm_log_files(self, new_file_count=None, path_log="/log/"):
        """
        获取bgm最新的几个文件，不传则获取所有文件
        :param new_file_count:
        :param path_log:
        :return:
        """
        cmd = f"find {path_log} " + r"-type f -exec stat --format '%y %s %n' {} \;"
        log_data = self.ssh.bgm_ssh.type_commands(cmd)
        # result = re.findall(f"{path_log}.*\w\d+_\d+_.*\.\w+", log_data, re.I)
        result = re.findall(f"{path_log}.*", log_data, re.I)
        result_dict = defaultdict(dict)
        if result:
            return_result = []
            for i in result:
                match_data = re.findall(f"{path_log}(.+?\w)(\d+)_\d+_", i, re.I)
                if match_data:
                    if match_data[0][0] not in result_dict:
                        result_dict[match_data[0][0]] = {int(match_data[0][1]): i}
                    else:
                        result_dict[match_data[0][0]][int(match_data[0][1])] = i
                else:
                    sp_data = re.findall(f".*({path_log}.*)", i, re.I)
                    if sp_data:
                        valide_data_flag = True
                        for j in ["syslogs", "nids"]:
                            if j in sp_data[0]:
                                valide_data_flag = False
                                break
                        if valide_data_flag:
                            return_result.append(sp_data[0])

            for k, v in result_dict.items():
                sorted_d_by_value = sorted(v, key=lambda x: x, reverse=True)
                logger.info(f"k is:{k}, sorted_d_by_value is:{sorted_d_by_value}")
                if new_file_count:
                    for count in range(int(new_file_count)):
                        try:
                            return_result.append(v[sorted_d_by_value[count]])
                        except Exception as e:
                            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/log_trigger_handler.py")
                            logger.info(e)
                else:
                    for i in sorted_d_by_value:
                        return_result.append(v[i])
            logger.info(return_result)
            return return_result

    def get_tcam_log_files(self, new_file_count=None, log_path="/mnt/sdcard/log/"):
        """
        获取tcam最新的几个文件，不传则获取所有文件
        :param new_file_count:
        :param log_path:
        :return:
        """
        # cmd = f"find {log_path} " + "-type f -exec ls --full-time {} \;"
        cmd = f"find {log_path} " + "-type f -exec stat -c '%y %s %n' {} \;"
        log_data = self.ssh.tcam_ssh.type_commands(cmd)
        result = re.findall(f"{log_path}\w.*", log_data, re.I)
        result_dict = defaultdict(dict)
        if result:
            for i in result:
                if "mcu_log_" in i:
                    result1 = re.findall(f"{log_path}(.*.+?_\d+_)(\d+).*", i, re.I)
                else:
                    result1 = re.findall(
                        f"{log_path}(.+?[A-Za-z])_?(\d+)_\d+_.*|{log_path}(.+?)_\d+-.*_(\d+)\.|_.*|{log_path}(.*.+?_)(\d+)_.*",
                        i, re.I)
                if result1:
                    if not any(result1[0]):
                        continue
                    result1 = [j for j in result1[0] if j]
                    if result1[0] not in result_dict:
                        result_dict[result1[0]] = {int(result1[1]): i}
                    else:
                        result_dict[result1[0]][int(result1[1])] = i

        return_result = []
        for k, v in result_dict.items():
            sorted_d_by_value = sorted(v, key=lambda x: x, reverse=True)
            logger.info(f"k is:{k}, sorted_d_by_value is:{sorted_d_by_value}")
            if new_file_count:
                for count in range(int(new_file_count)):
                    try:
                        return_result.append(v[sorted_d_by_value[count]])
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/log_trigger_handler.py")
                        logger.info(e)
            else:
                for i in sorted_d_by_value:
                    return_result.append(v[i])
        logger.info(f"return_result is:{return_result}")
        return return_result

    def config_trigger_to_valid(self, trigger_type='bgm_remote', own_data=None, source=1):
        """
        使用V2T模拟器配置触发不同类型的配置数据
        :param trigger_type:
        :param own_data:
        :param source:1:V2T模拟器，2：单域TCAM-soapatenner方式
        :return:
        """
        if own_data:
            own_data[0]["value"] = json.dumps(own_data[0]["value"])
            if source == 2:
                value = json.dumps(own_data).replace("\n", "").replace(" ", "")
            else:
                value = json.dumps(own_data).replace("\n", "").replace(" ", "").encode("utf-8")
        if trigger_type == "bgm_remote":
            if not own_data:
                temp_data = copy.deepcopy(self.bgm_log_local_config_data)
                temp_data[0]["value"] = json.dumps(temp_data[0]["value"])
                value = json.dumps(temp_data).replace("\n", "").replace(" ", "").encode("utf-8")
            self.v2t_simulator_Configuration("BGM", "remoteLog", confname="bgm_log_cfg", value=value)
            self.ssh.bgm_ssh.type_commands(
                "ls -alt /data/remote_log;cat /data/remote_log/remote_log_config.json;ls -alt /data/config_service/remoteLog")
        elif trigger_type == "tcam_remote":
            if not own_data:
                temp_data = copy.deepcopy(self.tcam_log_local_config_data)
                temp_data[0]["value"] = json.dumps(temp_data[0]["value"])
                value = json.dumps(temp_data).replace("\n", "").replace(" ", "").encode("utf-8")
            if source == 2:
                if not own_data:
                    temp_data = copy.deepcopy(self.tcam_log_local_config_data)
                    temp_data[0]["value"] = json.dumps(temp_data[0]["value"])
                    value = json.dumps(temp_data).replace("\n", "").replace(" ", "")
                self.soa.send_config_data_and_feedback_result(config_data=value, app_name="remoteLog",
                                                              file_name="tcam_log_cfg",
                                                              publish_id=int(time.time()))
            else:
                self.v2t_simulator_Configuration("TCAM", "remoteLog", confname="tcam_log_cfg", value=value)
            self.ssh.tcam_ssh.type_commands(
                f"ls -alt /mnt/sdcard/persistent/config_service/remoteLog/;cat /oemdata/remote_log/remote_log_config.json;ls -alt /oemdata/remote_log")
        elif trigger_type == "bgm_network":
            if not own_data:
                temp_data = copy.deepcopy(self.network_local_config_data)
                value = json.dumps(temp_data).replace("\n", "").replace(" ", "").encode("utf-8")
            self.v2t_simulator_Configuration("BGM", "net_resource_manager", confname="key_value_tab_config",
                                             value=value)
            self.ssh.bgm_ssh.type_commands(f"ls -alt /data/config_service")
        elif trigger_type == "bgm_monitor":
            if not own_data:
                temp_data = copy.deepcopy(self.log_monitor_local_config_data)
                temp_data[0]["value"] = json.dumps(
                    temp_data[0]["value"])
                value = json.dumps(temp_data).replace("\n", "").replace(" ", "").encode(
                    "utf-8")
            self.v2t_simulator_Configuration("BGM", "monitor_agent", confname="bgm_monitor_agent_cfg", value=value)
            self.ssh.bgm_ssh.type_commands(f"ls -alt /data/config_service")
        else:
            raise Exception("域名错误")

        logger.info(f"已经触发配置下发")
        time.sleep(3)

    def get_vehicle_config_data(self, config_type="bgm_rlog"):
        """
        获取车机端app应用的json文件，目前只支持BGM和TCAM
        :param config_type:
        :return:
        """
        if config_type == "bgm_rlog":
            result = self.ssh.bgm_ssh.type_commands("cat /data/remote_log/remote_log_config.json")
            data = result.replace("\n", "").replace(" ", "")
            self.bgm_log_vehicle_config_data = json.loads(data)
        elif config_type == "tcam_rlog":
            result = self.ssh.tcam_ssh.type_commands("cat /oemdata/remote_log/remote_log_config.json")
            data = result.replace("\n", "").replace(" ", "")
            self.tcam_log_vehicle_config_data = json.loads(data)
        elif config_type == "agent_monitor":
            result = self.ssh.bgm_ssh.type_commands(
                "cat /data/config_service/monitor_agent/bgm_monitor_agent_cfg_pointer")
            data = result.replace("\n", "").replace(" ", "")
            if "A" in data:
                result = self.ssh.bgm_ssh.type_commands(
                    "cat /data/config_service/monitor_agent/bgm_monitor_agent_cfg_A")
                data = result.replace("\n", "").replace(" ", "")
            else:
                result = self.ssh.bgm_ssh.type_commands(
                    "cat /data/config_service/monitor_agent/bgm_monitor_agent_cfg_B")
                data = result.replace("\n", "").replace(" ", "")
            self.log_monitor_vehicle_config_data = json.loads(data)

    def check_vehicle_config_data(self, config_type="bgm_rlog", check_field=None, expect_value=None):
        """
        检查车辆数据
        :param config_type:
        :param check_field:
        :param expect_value:
        :return:
        """
        if config_type == "bgm_rlog":
            match_check_data = self.bgm_log_vehicle_config_data
        elif config_type == "tcam_rlog":
            match_check_data = self.tcam_log_vehicle_config_data
        try:
            matches = [match.value for match in ng_parse(check_field).find(match_check_data)][0]
        except IndexError:
            raise AssertionError('not found selected attr!')
        if isinstance(matches, bool):
            check_value = eval(expect_value)

        if isinstance(matches, int):
            check_value = int(expect_value)

        if isinstance(matches, float):
            check_value = float(expect_value)

        if check_value != matches:
            raise AssertionError("Expected: {}\n\nWas: {}".format(check_value, matches))

    def update_config_data(self, config_type="bgm_rlog", update_field=None, new_value=None):
        """
        更新车辆数据
        :param config_type:
        :param update_field:
        :param new_value:
        :return:
        """
        if config_type == "bgm_rlog":
            ng_parse(update_field).update(self.bgm_log_local_config_data, new_value)
            logger.info(f"更新配置后数据是：{self.bgm_log_local_config_data}")
        elif config_type == "tcam_rlog":
            ng_parse(update_field).update(self.tcam_log_local_config_data, new_value)
            logger.info(f"更新配置后数据是：{self.tcam_log_local_config_data}")
        elif config_type == "network":
            ng_parse(update_field).update(self.network_local_config_data, new_value)
            logger.info(f"更新配置后数据是：{self.network_local_config_data}")
        elif config_type == "agent_monitor":
            ng_parse(update_field).update(self.log_monitor_local_config_data, new_value)
            logger.info(f"更新配置后数据是：{self.log_monitor_local_config_data}")

    def check_app_logleve_valid(self, log_type=None, expect_log_flag=" D ", unexpect_log_flag=None, device_name='TCAM', check_time=20,
                                time_out=600):
        # 检查日志等级
        self.log_manage.log_manage.check_log_by_keywords_start_thread(
            log_type=log_type if log_type else expect_log_flag,
            keywords=unexpect_log_flag if unexpect_log_flag else expect_log_flag,
            unexpect_keywords=None,
            log_print=None,
            device_name=device_name,
            timeout=time_out
        )
        sleep(check_time)

        logger.info(f"等待:{check_time}秒，获取日志。。。")
        ret, vehicle_log = self.log_manage.log_manage.check_log_by_keywords_stop_thread()
        logger.info(f"vehicle_log=\n{vehicle_log}")
        match_data = re.findall(f".*\d+\s(.+?) \w+: .*", vehicle_log)
        if match_data:
            logger.info(f"匹配到日志：{match_data}")
            if unexpect_log_flag:
                logger.warning(f"期望不得到：{unexpect_log_flag}，但是匹配到：{match_data[0]}")
                assert False
        else:
            if not unexpect_log_flag:
                logger.warning(f"超时时间内没有获取到相应等级的数据")
                assert False

    def check_app_log_size_valid(self, device_name="BGM", log_path="/log/", log_file_size=1024 * 1024,
                                 allow_offest=24 * 1024, time_out=600):
        start_time = time.time()
        first_file = None
        current_file_size = 0
        while time.time() - start_time < time_out:
            # 检查日志文件大小
            if device_name == "BGM":
                ret_msg = self.ssh.bgm_ssh.type_commands(f"ls -alt --full-time {log_path}")
                logger.info(f"ret_msg={ret_msg}")
                match_data = re.findall(".*root\s\s?(\d+)\s\d+-\d+-\d+.*(jetlog_messages\d.*.zst).*", ret_msg)
            else:
                ret_msg = self.ssh.tcam_ssh.type_commands(f"ls -alt --full-time {log_path}")
                logger.info(f"ret_msg={ret_msg}")
                match_data = re.findall(".*root\s+(\d+)\s\d+-\d+-\d+.*(jetlog_messages\d.*.zst).*", ret_msg)

            if match_data:
                logger.info(f"匹配到日志文件大小：{match_data}")
                if first_file is None:
                    first_file = match_data[0][1]
                    current_file_size = int(match_data[0][0])
                else:
                    if match_data[0][1] != first_file:
                        if match_data[0][1] != match_data[1][1]:
                            if abs(log_file_size - int(match_data[1][0])) > allow_offest:
                                logger.error(f"日志文件{first_file}的大小为{match_data[1][0]}，超过允许范围{allow_offest}")
                                assert False
                            current_file_size = int(match_data[2][0])
                        else:
                            if abs(log_file_size - int(match_data[2][0])) > allow_offest:
                                logger.error(f"日志文件{first_file}的大小为{match_data[1][0]}，超过允许范围{allow_offest}")
                                assert False
                            current_file_size = int(match_data[2][0])
            time.sleep(20)
        if abs(log_file_size - current_file_size) > allow_offest:
            logger.error(f"在规定时间内，日志文件{first_file}的大小为{current_file_size}，误差超过允许范围{allow_offest}")
            assert False

    def check_app_cycle_valid(self, log_type="RLog", device_name="TCAM", time_out=10 * 60):
        self.log_manage.log_manage.check_log_by_keywords_start_thread(
            log_type=log_type,
            keywords='jetlog over time meetting',
            unexpect_keywords=None,
            log_print=None,
            device_name=device_name,
            timeout=time_out
        )

        sleep(5)
        ret, vehicle_log = self.log_manage.log_manage.check_log_by_keywords_stop_thread()
        logger.info(f"vehicle_log:\n{vehicle_log}")
        match_data = re.findall(r".*(\d{4}-\d+-\d+ \d+:\d+:\d+).*jetlog over time meetting.*", vehicle_log)
        if not match_data:
            logger.warning(f"没有匹配到期望的值：jetlog over time meetting")
            raise AssertionError(f"没有匹配到期望的值：jetlog over time meetting")
        logger.info(f"jetlog over time meetting：{match_data};转化为时间戳：{self.datetime_to_timestamp(match_data[0])}")

        self.log_manage.log_manage.check_log_by_keywords_start_thread(
            log_type=log_type,
            keywords='jetlog over time remain',
            unexpect_keywords=None,
            log_print=None,
            device_name=device_name,
            timeout=time_out
        )
        sleep(5)
        ret, vehicle_log = self.log_manage.log_manage.check_log_by_keywords_stop_thread()
        logger.info(f"vehicle_log:\n{vehicle_log}")
        match_data = re.findall(r".*(\d+-\d+-\d+ \d+:\d+:\d+).*jetlog over time remain.*", vehicle_log)
        if not match_data:
            logger.warning(f"没有匹配到期望的值：jetlog over time remain")
            raise AssertionError(f"没有匹配到期望的值：jetlog over time remain")
        logger.info(f"jetlog over time remain:匹配到日志：{match_data}")

    # ################ djw  end  ######################################################

    # ################ ltg ######################################################

    #  解析车端日志
    def parse_vehicle_log_get_check_data(self, vel_log, **kwargs):
        '''
        解析 车端日志 提取校验内容
        @param vel_log: 获取的 车端日志
        @return: {}，{}
        '''

        def extract_json_or_return_line(line):
            start_index = line.find('{')
            end_index = line.rfind('}')
            if start_index != -1 and end_index != -1 and start_index < end_index:
                try:
                    json_content = line[start_index:end_index + 1]
                    return json.loads(json_content)
                except json.JSONDecodeError:
                    return line
            return line

        if not vel_log.strip():
            assert 0, f"内容为空={vel_log}"
        filter_vel_log_data = {}
        # 上传文件的 信息
        upload_file_info = {}
        object_key_string_map_name = {}
        # keywords=["trigger source", 'UploadFileList', 'utimestamp: Log-upload-timestamp:', '[UPLOADER]FileInfo', '[UPLOADER]Success']
        lines = vel_log.splitlines()
        for line in lines:
            if not line.strip():
                continue
            # 判断 触发源 trigger source:{"source":1,"event":"webuser","request_id":"1837022287480750080","ctrlParam":""}
            if "trigger source" in line:
                logger.info(f"line>>>{line}")
                # 触发
                trigger = extract_json_or_return_line(line.strip())
                logger.info(f"触发源信息={trigger}")
                # print(type(trigger),trigger)
                filter_vel_log_data["trigger_source"] = trigger
            elif "resp_str =" in line:
                # 远程拉取
                remote_fetch = extract_json_or_return_line(line.strip())
                filter_vel_log_data["remote_fetch"] = remote_fetch
                logger.info(f"触发源信息={remote_fetch}")
            elif "remote_config_service" in line and "ecu log config" in line:
                logger.info(f"line>>>{line}")
                # 配置下发  [remote_config_service.cpp:276]:ecu log config: 1, level: 3, size: 1, interval: 180, expire time: 1730109567
                data_dic = {item.split(':')[0].strip(): item.split(':')[1].strip() for item in line.split(",") if
                            item.strip()}
                if "remote_config_service" in filter_vel_log_data:
                    filter_vel_log_data["remote_config_service"]["ecu_log_config"].append(data_dic)
                else:
                    filter_vel_log_data["remote_config_service"] = {}
                    filter_vel_log_data["remote_config_service"]["ecu_log_config"] = [data_dic]
                logger.info(f"remote_config_service ={data_dic}")

            elif "triggerSourceInfo" in line:
                logger.info(f"line>>>{line}")
                # error   触发 上传
                # [log_file_manager.cpp:381]:triggerSourceInfo.eventerr_log_monitor
                # triggerSourceInfo.eventcoredump_monitor
                logger.info(f"lin={line}")
                name = line.split("triggerSourceInfo.")[-1].strip()
                filter_vel_log_data[name] = name
                logger.info(f"触发源信息=eventerr_log_monitor")
            # elif 'param:{"error_type"' in line:
            #     # param:{"error_type":"coredump","param":{"err_id":"68fc8678a5194928847bc536031ee83a","file-path":"","log-type":1,"name":""},"type":1}
            #     msg_dict = extract_json_or_return_line(line.strip())
            #     logger.info(line)
            #     error_type = msg_dict.get("error_type","")
            #     filter_vel_log_data[error_type] = error_type
            #     # triggerSourceInfo.eventcoredump_monitor

            elif ":UploadFileList:" in line:
                #  上传的 文件都有哪些
                # [jetlog_file.cpp:731]:UploadFileList: {"event":"webuser","files":["/log/jetlog_messages1_20210101080001_f078e1916e294fb2beb212b30b744d43.zst","/log/jetlog_messages2_20240920120107_6ae7217cdafd4335af633466d75d9acc.zst","/log/jetlog_messages3_20240920133443_107472e0ae9142a2a6aa99f0b1c27e6d.zst","/log/jetlog_bts1_20210101080002_62984e1379674a9f84a1da874d8f1202.zst","/log/jetlog_bts2_20240920132738_b58968e2e9044db89a903ba191068fa0.zst","/log/jetlog_s2s1_20210101080002_9cf0d07ca872450bbef51ccb5b40973e.zst"],"is_finish":false,"request_id":"1837022287480750080","trigger_source":"CLOUD"}
                UploadFileList = extract_json_or_return_line(line.strip())
                if "jetlog_file.cpp" in line:
                    logger.info(f"上传的 jetlog 信息={UploadFileList}")
                    if 'jetlog_upload_list' in filter_vel_log_data:
                        filter_vel_log_data["jetlog_upload_list"].append(UploadFileList)
                    else:
                        filter_vel_log_data["jetlog_upload_list"] = [UploadFileList]
                elif "coredump_file" in line:
                    logger.info(f"上传的 coredump 信息={UploadFileList}")
                    if 'coredump_upload_list' in filter_vel_log_data:
                        filter_vel_log_data["coredump_upload_list"].append(UploadFileList)
                    else:
                        filter_vel_log_data["coredump_upload_list"] = [UploadFileList]
            elif '[UPLOADER]FileInfo' in line:
                logger.info(f"line>>>{line}")
                pattern = r'FileInfo:{file=(.*?),size=(\d+),.*?modify_time:(\d+)'
                match = re.search(pattern, line)
                # 如果找到匹配项，则提取文件名称和大小
                if match:
                    file_name = match.group(1)
                    file_size = match.group(2)
                    modify_time = match.group(3)
                    logger.info(f"文件名称: {file_name}")
                    logger.info(f"文件大小: {file_size}")
                    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(modify_time)))
                    logger.info(f"修改时间: {modify_time},{otherStyleTime}")
                    upload_file_info[file_name] = {
                        "filename": file_name,
                        # "modified_at": otherStyleTime,
                    }
                else:
                    logger.info("未找到文件名称和大小")
            elif "[UPLOADER]Update start upload" in line:
                # 判断 开始上传的文件
                # 2024-09-20 14:53:44.311 2123 2166 I RLog: 12176: [UPLOADER]Update start upload /log/jetlog_messages1_20210101080001_f078e1916e294fb2beb212b30b744d43.zst:{object_key:staging/bgm/tracelog/b681a02a-daee-477b-a532-331b0b0ca37b,offset:2096050,inode:21}
                logger.info(f"line>>>{line}")
                pattern = r'Update start upload (.*?)\:{(.*?)}'
                match = re.search(pattern, line)
                if match:
                    filename = match.group(1).strip()
                    object_key = match.group(2).strip()

                    logger.info(f"upload_file_name={filename}")
                    logger.info(f"object_key={object_key}")
                    object_key_value = object_key.split(',')[0].split(":")[-1].strip()
                    upload_file_info[filename]["object_key"] = object_key_value
                    object_key_string_map_name[object_key] = filename
            elif "[UPLOADER]RECORD:{object_key:" in line:
                # 2024-09-20 14:53:44.850 2123 2166 I RLog: 12200: [UPLOADER]RECORD:{object_key:staging/bgm/tracelog/b681a02a-daee-477b-a532-331b0b0ca37b,offset:2096050,inode:21},file_offset:2096050,upload_size:524288
                object_key = line.split("[UPLOADER]RECORD:{")[-1].split("}")[0].strip()
                #
                line_string_list = line.split(' ')
                upload_time_string = ' '.join(line_string_list[:2])
                filename = object_key_string_map_name.get(object_key)

                if filename and not upload_file_info[filename].get("upload_at"):
                    logger.info(f"object_key_string={object_key}  upload_time_string={upload_time_string}")
                    # 只取第一个
                    upload_file_info[filename]["__vehicle_upload_time"] = upload_time_string

            elif "[UPLOADER]Success(" in line:
                logger.info(f"line>>>{line}")
                # [UPLOADER]Success(1) file=/log/jetlog_messages1_20210101080001_f078e1916e294fb2beb212b30b744d43.zst @10495764->10495764
                pattern = r'Success\((\d+)\) file=(.*?)@(\d+)->(\d+)'
                match = re.search(pattern, line)
                up_load_typ = match.group(1)
                file_name = match.group(2).strip()
                size1 = int(match.group(3).strip())
                size2 = int(match.group(4).strip())
                logger.info(f'up_load_typ {up_load_typ, file_name, size1, size2}')
                upload_time_string = line.split('.')[0]
                timestamp = int(time.mktime(time.strptime(upload_time_string, '%Y-%m-%d %H:%M:%S')))
                logger.info(f'timestamp {timestamp, upload_time_string}')
                upload_file_info[file_name]["upload_at"] = timestamp
                upload_file_info[file_name]["size"] = size2
                upload_file_info[file_name]["__duplicated"] = int(up_load_typ)
                upload_file_info[file_name]["__upload_ok"] = int(up_load_typ)

                modified_at = ""  # upload_file_info[file_name].get('modified_at')
                string = f"车端上传成功 >>> {file_name}  upload_at={timestamp, upload_time_string}，size={size2} modified_at={modified_at}"
                with allure.step(string):
                    logger.info(string)

                # 已经有的 "文件名"、"日志修改时间"  "文件大小"，"上传时间"
                if up_load_typ == '1':
                    # 老文件断点续传，根据VID，检查"文件名"、"日志修改时间"、"上传时间"、"文件大小"
                    # upload_file_info[file_name]
                    pass
                else:
                    # 新文件，根据文件名，检查"文件名"、"车端上传时间"、"日志修改时间"、"上传时间"、"文件大小"、"触发源"、"事件类型"、"车型"、"域控版本"
                    info_dict_list = filter_vel_log_data.get('jetlog_upload_list')
                    if info_dict_list:
                        info_dict = info_dict_list[0]
                        upload_file_info[file_name]["__trigger_source"] = info_dict["trigger_source"]
                        upload_file_info[file_name]["__event"] = info_dict["event"]
                        upload_file_info[file_name]["__vehicle_type"] = ""
                    info_dict_list = filter_vel_log_data.get('remote_fetch')
                    if info_dict_list:
                        upload_file_info[file_name]["__trigger_source"] = "remote_fetch"
                        upload_file_info[file_name]["__event"] = info_dict_list["event"]

                    # upload_file_info[file_name]["__vehicle_version"] = ""
                    # upload_file_info[file_name]["__vehicle_vid"] = ""
            elif "upload NG:" in line:
                # 上传失败  [uploader_proxy.cpp:311]:upload NG: /mnt/sdcard/log/backup/3/mcu_log_20241012035241_0_20241027170818_CPFILE.txt
                # uploadFileResult = -1
                logger.info(f"line>>>{line}")
                file_name = line.split("upload NG:")[-1].strip()
                if upload_file_info.get(file_name):
                    upload_file_info[file_name]["__upload_ok"] = -1
                else:
                    upload_file_info[file_name] = {}
                    upload_file_info[file_name]["__upload_ok"] = -1

                string = f"车端上传 NG >>> {file_name} "
                with allure.step(string):
                    logger.info(string)

            elif "upload OK:" in line:
                # uploader_proxy.cpp:304]:result: 0 upload OK: /mnt/sdcard/log/UDS_2_20241029-072354.dlt
                logger.info(f"line>>>{line}")
                pattern = r'result\: (\d+) upload OK\: (.*)'
                match = re.search(pattern, line)
                if match:
                    result = int(match.group(1).strip())
                    file_name = match.group(2).strip()
                    upload_file_info[file_name]["__upload_ok"] = result

        logger.info(f"upload_file_info={len(upload_file_info)}  {upload_file_info}")
        logger.info(f"filter_vel_log_data={len(upload_file_info)}  {filter_vel_log_data}")

        return filter_vel_log_data, upload_file_info

    # 校验车端日志和 云端日志
    def check_vehicle_log_and_upload_log(self, check_data_dict: dict, **kwargs):
        '''
        校验车端日志和上传的日志 是否一致

        @param check_data_dict:
            {
            '/log/jetlog_bts1930_20241023132739_8bc6e1c3b418465abcf5964ebc48efe3.zst': {'Client-Version': '6160110220AD',
                                                                             '__duplicated': 0,
                                                                             '__event': 'CNAfME6YmxSgjrPpHSpn',
                                                                             '__trigger_source': 'CLOUD',
                                                                             '__vehicle_type': '',
                                                                             'ecu': 'bgm',
                                                                             '__vehicle_upload_time': '2024-10-23 13:31:48.677',
                                                                             'filename': '/log/jetlog_bts1930_20241023132739_8bc6e1c3b418465abcf5964ebc48efe3.zst',
                                                                             'modified_at': '2024-10-23 13:31:44',
                                                                             'object_key': 'staging/bgm/tracelog/16b44f7f-fece-4d23-92ab-205a0596b97e',
                                                                             'size': 275671,
                                                                             'upload_at': 1729661509,
                                                                             'vid': '23aa03d499a848b4a2191074f9064b2f'},
            '/log/jetlog_messages1442_20241023131244_a0367384b4ff47c993d5c2d1b4252d58.zst': {'Client-Version': '6160110220AD',
                                                                                  '__duplicated': 0,
                                                                                  '__event': 'CNAfME6YmxSgjrPpHSpn',
                                                                                  '__trigger_source': 'CLOUD',
                                                                                  '__vehicle_type': '',
                                                                                  'ecu': 'bgm',
                                                                                  '__vehicle_upload_time': '2024-10-23 13:31:34.991',
                                                                                  'filename': '/log/jetlog_messages1442_20241023131244_a0367384b4ff47c993d5c2d1b4252d58.zst',
                                                                                  'modified_at': '2024-10-23 13:22:04',
                                                                                  'object_key': 'staging/bgm/tracelog/4935408d-b5f6-44bf-ae62-3dc1bf7b3c8f',
                                                                                  'size': 1035337,
                                                                                  'upload_at': 1729661498,
                                                                                  'vid': '23aa03d499a848b4a2191074f9064b2f'}
            }
        @param kwargs:
        @return:
        '''

        url = kwargs.get("url", 'https://logservice.jidustaging.com/api/search/common')
        headers = kwargs.get("headers", {
            'Content-Type': 'application/json',
            'Cookie': 'jidu_device_id=d5725be5-2a5b-41fd-9637-8e12501abf2c'
        })
        index = kwargs.get("index", 'jidulogapp-staging-vehicle-log-serverlog')
        vid = kwargs.get("vid", '95595be57f093f19e042da6be5c03227')
        fuzzy_query = kwargs.get("fuzzy_query", [])
        service_name = kwargs.get("service_name", "vehicle-log")
        begin_time = kwargs.get("begin_time", time.time() - 30 * 60)
        end_time = kwargs.get("end_time", time.time())
        size = kwargs.get("size", 20)

        data = {
            "index": index,
            "service_name": service_name,
            "fuzzy_query": [vid] + fuzzy_query,
            "begin": int(begin_time),
            "end": int(end_time),
            "from": 0,
            "size": size
        }

        count = 0
        start_time = time.time()
        req_timeout = 10 * 60
        upload_ng = 0
        object_key_list = set()
        object_name_list = []
        logger.info(f"check_data_dict=={check_data_dict}")
        check_data_dict_d = copy.deepcopy(check_data_dict)
        for k, info_dic in check_data_dict_d.items():
            if info_dic.get("object_key"):
                object_key_list.add(info_dic.get("object_key"))
                object_name_list.append(k)

            if info_dic.get("__upload_ok") == -1:
                # 上传失败的 去掉
                check_data_dict.pop(k)
                string = f"{k}车端上传失败，跳过校验"
                with allure.step(string):
                    logger.info(string)
                upload_ng += 1
            elif info_dic.get("__upload_ok") == 3:
                check_data_dict.pop(k)
                string = f"{k} 车端已经完全上传过 result=3  不需要上传，跳过校验"
                with allure.step(string):
                    logger.info(string)

        string = f"文件个数为为{len(object_name_list)} object_key 个数为{len(object_key_list)}"
        assert len(object_key_list) == len(object_name_list), "object_key 不唯一"
        with allure.step(string):
            logger.info(string)
        if len(check_data_dict) == 0:
            if upload_ng:
                ss = f"存在车端上传失败的{upload_ng}文件 需要关注！！！！"
                with allure.step(ss):
                    logger.info(ss)
                assert 0, ss
            with allure.step(f"没有需要校验的文件/文件已经上传过"):
                logger.info(f"没有需要校验的文件")
            return
        try:
            while time.time() - start_time < req_timeout:
                # if not end_time:
                data['begin'] = int(time.time() - 80 * 60)
                data['end'] = int(time.time())
                response = requests.post(url, headers=headers, json=data, timeout=5)
                logger.info(f"查询参数={data}")
                logger.info(f"查询TCAM上报到车云的远控结果集为: response={response.text}")
                if response.json()["code"] == 0:
                    res = response.json()["data"]
                    if res["total"] <= 0:
                        continue
                    info = res['entries']
                    for rec_msg in info:
                        message = rec_msg['message']
                        if "produce message" in message:
                            message_dict_string = message.split('produce message:')[-1].replace("false",
                                                                                                'False').strip()
                            dictionary = ast.literal_eval(message_dict_string)
                            # 拼接路径
                            name = os.path.join(dictionary["directory"], dictionary["filename"])
                            dictionary["filename"] = name
                            # 进行时间转换
                            dictionary["upload_at"] = int(
                                time.mktime(time.strptime(dictionary["upload_at"], '%Y-%m-%d %H:%M:%S')))
                            logger.info(f'dictionary={dictionary}')
                            check_data_dict2 = copy.deepcopy(check_data_dict)
                            logger.info(
                                f'需要校验的个数={len(check_data_dict2)} 已经校验成功{count} 个 check_data_dict2={check_data_dict2}')
                            for check_key, check_info_value in check_data_dict2.items():
                                if check_key != name:
                                    # logger.info(f"获取到的文件名字是{name} ")
                                    continue
                                if check_info_value.get("check_flag", None):
                                    # 校验通过的 ，
                                    # logger.info(f" {name} 已经校验通过")
                                    continue

                                logger.info(f"校验{check_key} 日志相关信息")
                                # 遍历 所有 key  value
                                flag = False
                                for key, info_value in check_info_value.items():
                                    if key.startswith("__"):
                                        continue
                                    elif key == "upload_at":
                                        if abs(dictionary.get(key) - info_value) < 30:
                                            continue
                                        else:
                                            log_string = f"name={name}  对应的{key} 不一致 本应为{info_value}实际为{dictionary.get(key)} 则跳过"
                                            logger.error(log_string)
                                            break
                                    elif dictionary.get(key) != info_value:
                                        flag = False
                                        log_string = f"name={name}  对应的{key} 不一致 本应为{info_value}实际为{dictionary.get(key)} 则跳过"
                                        logger.error(log_string)
                                        break
                                    else:
                                        log_string = f"name={name}  对应的{key} 一致 本应为{info_value}实际为{dictionary.get(key)}"
                                        logger.info(log_string)
                                        flag = True
                                if flag:
                                    # 如果 都匹配 则 下次不校验
                                    check_data_dict[check_key]["check_flag"] = 1
                                    # 校验通过的
                                    count += 1

                                    log_string = f"总共{len(check_data_dict)}个文件，校验成功{count}个，当前{check_key} 校验成功 还有{len(check_data_dict) - count}个需要校验"
                                    with allure.step(log_string):
                                        logger.info(log_string + f"check_data_dict={check_data_dict}")
                                    if count == len(check_data_dict):
                                        with allure.step(f"总共校验{len(check_data_dict)}，都校验成功"):
                                            logger.info(f"总共校验{len(check_data_dict)}，都校验成功")
                                        if upload_ng:
                                            ss = f"存在车端上传失败{upload_ng}的 需要关注！！！！"
                                            with allure.step(ss):
                                                logger.info(ss)
                                        return
                                    break
                        logger.info('===============================================================')
                else:
                    logger.error("TCAM云端日志查询失败")
                time.sleep(30)
        except requests.exceptions.RequestException as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/log_trigger_handler.py")
            logger.error("请求失败: {}".format(e))
        # 校验是否匹配
        num = 0
        for name, item in check_data_dict.items():
            if item.get("check_flag"):
                with allure.step(f"{name}云端和车端校验成功"):
                    logger.info(f"校验成功=》{item}")
            else:
                num += 1
                with allure.step(f"异常 {name} 云端和车端校验不匹配"):
                    logger.info(f"校验失败=》云端和车端校验不匹配 {item}")

        with allure.step(f"存在{num}个校验失败"):
            assert 0, f"存在校验失败的{check_data_dict} "

    def check_vehicle_and_trigger_event(self, filter_vel_log_dict, **kwargs):
        '''

        @param kwargs:
        @return:
        '''
        soa_parameters = kwargs.get("soa_parameters", {})  # 需要根据情况填
        method_name = kwargs.get("method_name", "ReqUploadLog")  # 需要根据情况填

        if soa_parameters:
            send_event = ""
            vehicle_event = ""
            logger.info("校验 event事件")
            if method_name == "ReqUploadLog":
                send_event = soa_parameters.get("triggerSourceInfo", {}).get("event")
                # filter_vel_log_dict= {'trigger_source': {'source': 2, 'event': 'local_voice', 'request_id': 'd0HFtg6TpYw89eDZDxLr',
                #                     'ctrlParam': '123'}
                vehicle_event = filter_vel_log_dict.get("trigger_source", {}).get("event")
                string = f"下发的 event为{send_event}，车端收到的为{vehicle_event}"
                with allure.step(string):
                    logger.info(string)
                assert send_event == vehicle_event, string
            elif method_name == "CallVehicleApi":
                vehicle_event = filter_vel_log_dict.get("remote_fetch", {}).get("event")
                ascii_list = soa_parameters.get("payload", {})
                ss = ''.join([chr(char) for char in ascii_list])
                send_event = json.loads(ss).get("event")
            else:
                pass

            string = f"下发的 event为{send_event}，车端收到的为{vehicle_event}"
            with allure.step(string):
                logger.info(string)
            assert send_event == vehicle_event, string

    def add_check_info(self, check_data_dict, vid, device_name=DeviceName.BGM):
        '''
        增加 vid 版本号
        @param check_data_dict: 原来的数据
        @param device_name:
        @param vid: vid 码
        @return:
        '''
        version = self.getVersion(device_name)
        new_add_dict = {
            'vid': vid,
            "Client-Version": version,
            'ecu': device_name.name.lower(),
        }
        for key, info_dic in check_data_dict.items():
            if info_dic.get("__duplicated"):
                info_dic.update(new_add_dict)
            else:
                info_dic.update(new_add_dict)

        return check_data_dict

    def getVersion(self, device_name: DeviceName):
        '''
        获取版本号
        @param device_name:
        @return:
        '''
        if device_name == DeviceName.BGM:
            version_info = self.ssh.bgm_ssh.get_version()
            version = version_info.get("build_version", "").replace(" ", "")
            # 6160110220AE
            return version
        elif device_name == DeviceName.TCAM:
            # {'sys.build.version.release': '016110110220 AD', 'sys.build.version.swpn': '6110110220',
            #  'sys.build.version.ver': 'AD', 'sys.build.version.diagpn': '', 'sys.build.version.diagver': '',
            #  'sys.build.date': '', 'sys.build.date.utc': '1729690413', 'sys.build.variant': '',
            #  'sys.build.band': 'JIDU', 'sys.build.device': 'MARS1', 'sys.build.arch': 'ARM',
            #  'sys.build.fingerprint': 'JIDU/MARS1//ARM/:ece8c4784b2a', 'sys.build.carina.version': 'Carina2.2.2.1',
            #  'sys.build.jidl.id': '69a038b', 'sys.build.jidl.version': 'refs/tags/JIDL_RELEASE_2.2REL_3',
            #  'sys.build.neu.build.project': 'GEEA2.0_JIDU_CN', 'sys.build.neu.build.version': '2.203',
            #  'sys.build.neu.build.date': '2024-10-17 18', 'sys.build.neu.build.chipset': 'Linksci-T02L',
            #  'sys.build.neu.build.firmware': 'SA515M_T02L-GA-ACN_R2.1_V.B.4.22_20241014',
            #  'sys.build.neu.build.compiler': 'SA515M_T02L-GA-ACN_R2.1_V.B.4.20_20240909'}

            cmd = "cat /oemapp/etc/build.prop"
            version_info = self.ssh.type_commands(device_name, cmd)
            version_info_dict = {item.split('=')[0].strip(): item.split('=')[1].strip() for item in
                                 version_info.split("\n") if item.strip()}
            # 6110110220AD
            version = version_info_dict.get("sys.build.version.swpn", "") + version_info_dict.get(
                "sys.build.version.ver", "")
            return version

    # 检查当前是否有日志在上传
    def check_vehicle_log_is_uploading(self, device_name=DeviceName.BGM, timeout=10 * 60):
        '''
        检查日志是否有在上传， 如果有则 等带上传结束，若果超过timeout 未结束则报错
        @param device_name:
        @param timeout:
        @return:
        '''

        logger.info(f"检查当前是否有日志在上传")
        self.log_manage.log_manage.check_log_by_keywords_start_thread(
            log_type="RLog",
            keywords="[UPLOADER]RECORD",
            unexpect_keywords=None,
            log_print=None,
            device_name=device_name.name,
            timeout=20
        )
        ret, jet_log_msg = self.log_manage.log_manage.check_log_by_keywords_stop_thread()
        if ret:
            logger.info(f"当前有日志在上传{jet_log_msg}")
            logger.info(f"当前有日志在上传 延时{timeout}秒 等待日志上传完成")
            self.log_manage.log_manage.check_log_by_keywords_start_thread(
                log_type="RLog",
                keywords="Upload ==>> WaitUpload",
                unexpect_keywords=None,
                log_print=None,
                device_name=device_name.name,
                timeout=timeout
            )
            ret, jet_log_msg = self.log_manage.log_manage.check_log_by_keywords_stop_thread()

            assert ret, f"超时{timeout}秒日志未上传结束"

    # 获取 触发上传的车端日志
    def trigger_vehicle_log_upload_and_get_log(self, device_name=DeviceName.BGM, timeout=10 * 60, **kwargs):
        '''
        触发日志上传，并获取上传的相关日志
        @param device_name: 设备名称
        @param timeout: 超时时间
        @param kwargs:
        @return:
        '''
        error_conditions = kwargs.get("error_conditions", False)  # 需要根据情况填
        # soa 服务参数
        partner_key = kwargs.get("partner_key", "RemoteLogManagerService_client_BGM_RemoteLogManagerService")  # 需要根据情况填
        method_name = kwargs.get("method_name", "ReqUploadLog")  # 需要根据情况填
        args = kwargs.get("soa_parameters", {})  # 需要根据情况填
        ck_info = kwargs.get("ck_info", {'out': 0})  # 默认 不需要填
        soa_timeout = kwargs.get("soa_timeout", 1)  # 默认 不需要填
        cycle_time = kwargs.get("cycle_time", 0.2)  # 默认 不需要填
        is_async = kwargs.get("is_async", False)  # 默认 不需要填
        fuzz_match = kwargs.get("fuzz_match", True)  # 默认 不需要填

        self.log_manage.log_manage.check_log_by_keywords_start_thread(
            log_type="RLog",
            keywords="Upload ==>> WaitUpload",
            unexpect_keywords=None,
            log_print=None,
            device_name=device_name.name,
            timeout=timeout
        )
        # 延时一段时间等ssh 启动
        time.sleep(10)
        # 触发 日志上传
        self.send_soa_request(partner_key, method_name, args)

        if error_conditions:
            time.sleep(10)
            logger.info("执行异常场景")
            self.ssh.set_airplane_mode(sts=isOn.On)
            time.sleep(3 * 60)
            # 关闭飞行模式
            self.ssh.set_airplane_mode(sts=isOn.Off)
            interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
            if 'rmnet_data1' not in interface:
               logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
            time.sleep(2)

        logger.info("等待日志上传")
        ret, vehicle_log = self.log_manage.log_manage.check_log_by_keywords_stop_thread()
        logger.info(f"vehicle_log={vehicle_log}")
        assert ret, f"超时{timeout}秒日志未上传结束"
        return vehicle_log

    # 校验触发的 上传 ************************************
    def trigger_updatelog_check(self, vid, device_name=DeviceName.BGM, timeout=10 * 60, **kwargs):
        '''
        配置触发上传 校验
        @param vid:
        @param device_name:
        @param timeout:
        @param kwargs:
        @return:
        '''
        # 检查环境
        self.check_vehicle_log_is_uploading(device_name=device_name, timeout=timeout)
        # 触发日志上传，获取日志
        vehicle_log_msg = self.trigger_vehicle_log_upload_and_get_log(device_name=device_name, timeout=timeout,
                                                                      **kwargs)
        # 解析日志
        filter_vel_log_dict, check_data_dict = self.parse_vehicle_log_get_check_data(vehicle_log_msg)
        # 补充校验内容
        self.add_check_info(check_data_dict, vid=vid, device_name=device_name)
        # 对上传数据进行校验
        self.check_vehicle_log_and_upload_log(check_data_dict, vid=vid)
        # 校验event
        self.check_vehicle_and_trigger_event(filter_vel_log_dict, **kwargs)

    # 获取 远程拉取的车端日志
    def get_remote_fetch_upload_log(self, device_name=DeviceName.BGM, timeout=10 * 60, **kwargs):
        '''
        获取通过 远程连接 拉取的日志  对应的车端上传日志
        @param kwargs:
        @return:
        '''
        error_conditions = kwargs.get("error_conditions", False)  # 需要根据情况填
        partner_key = kwargs.get("partner_key", "V2TRoutingForwarder_client_V2TLogBGMForwarder")  # 需要根据情况填
        method_name = kwargs.get("method_name", "CallVehicleApi")  # 需要根据情况填
        args = kwargs.get("soa_parameters", {})  # 需要根据情况填
        ck_info = kwargs.get("ck_info", {'out': 0})  # 默认 不需要填
        soa_timeout = kwargs.get("soa_timeout", 1)  # 默认 不需要填
        cycle_time = kwargs.get("cycle_time", 0.2)  # 默认 不需要填
        is_async = kwargs.get("is_async", False)  # 默认 不需要填
        fuzz_match = kwargs.get("fuzz_match", True)  # 默认 不需要填

        self.log_manage.log_manage.check_log_by_keywords_start_thread(
            log_type="RLog",
            keywords="Upload ==>> WaitUpload",
            unexpect_keywords=None,
            log_print=None,
            device_name=device_name.name,
            timeout=timeout
        )
        sleep(5)
        self.send_soa_request(partner_key, method_name, args, timeout=5)
        logger.info("等待日志上传")
        if error_conditions:
            time.sleep(10)
            logger.info("执行异常场景")
            self.ssh.set_airplane_mode(sts=isOn.On)
            time.sleep(3 * 60)
            # 关闭飞行模式
            self.ssh.set_airplane_mode(sts=isOn.Off)
            interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
            if 'rmnet_data1' not in interface:
               logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
            time.sleep(2)

        ret, vehicle_log = self.log_manage.log_manage.check_log_by_keywords_stop_thread()
        logger.info(f"vehicle_log={vehicle_log}")
        assert ret, f"超时{timeout}秒日志未上传结束"
        return vehicle_log

    # 校验 远程拉取 ************************************
    def check_remote_fetch(self, vid, device_name=DeviceName.BGM, timeout=10 * 60, **kwargs):
        '''
        校验 远程拉取的
        @param vid:
        @param device_name:
        @param timeout:
        @param kwargs:
        @return:
        '''
        self.check_vehicle_log_is_uploading(device_name=device_name, timeout=timeout)
        # 远程拉取
        vehicle_log_msg = self.get_remote_fetch_upload_log(device_name, timeout, **kwargs)
        # 解析日志
        filter_vel_log_dict, check_data_dict = self.parse_vehicle_log_get_check_data(vehicle_log_msg)
        # 补充校验内容
        self.add_check_info(check_data_dict, vid=vid, device_name=device_name)
        # 对上传数据进行校验
        self.check_vehicle_log_and_upload_log(check_data_dict, vid=vid)
        # 校验event
        self.check_vehicle_and_trigger_event(filter_vel_log_dict, **kwargs)

    # 校验 远程配置 ************************************
    def check_remote_config(self, vid, device_name=DeviceName.BGM, timeout=15 * 60, **kwargs):
        '''
        校验 远程配置
        @param device_name:
        @param timeout:
        @param kwargs:
        @return:
        '''
        error_conditions = kwargs.get("error_conditions", False)  # 需要根据情况填
        upload_interval = kwargs.get("upload_interval", 3 * 60)  # 上传周期
        # 检查是否有上传
        self.check_vehicle_log_is_uploading(device_name=device_name, timeout=timeout)
        # 检查 倒计时
        self.log_manage.log_manage.check_log_by_keywords_start_thread(
            log_type="RLog",
            keywords="jetlog over time remain(s):",
            unexpect_keywords=None,
            log_print=None,
            device_name=device_name.name,
            timeout=30
        )
        # 延时一段时间等ssh 启动
        time.sleep(10)
        logger.info("周期倒计时")
        ret, vehicle_log = self.log_manage.log_manage.check_log_by_keywords_stop_thread()
        logger.info(f"vehicle_log={vehicle_log}")
        assert ret, f"超时{timeout}秒日志未上传结束"
        # 开始监听日志
        self.log_manage.log_manage.check_log_by_keywords_start_thread(
            log_type="RLog",
            keywords="Upload ==>> WaitUpload",
            unexpect_keywords=None,
            log_print=None,
            device_name=device_name.name,
            timeout=timeout
        )
        if error_conditions:
            t = upload_interval + 30
            logger.info(f"执行异常场景，延时一段时间{t}秒")
            time.sleep(t)
            self.ssh.set_airplane_mode(sts=isOn.On)
            time.sleep(3 * 60)
            # 关闭飞行模式
            self.ssh.set_airplane_mode(sts=isOn.Off)
            interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
            if 'rmnet_data1' not in interface:
               logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
            time.sleep(2)

        logger.info("等待日志上传")
        ret, vehicle_log = self.log_manage.log_manage.check_log_by_keywords_stop_thread()
        logger.info(f"vehicle_log={vehicle_log}")
        assert ret, f"超时{timeout}秒日志未上传结束"
        # 解析日志
        # filter_vel_log_dict, check_data_dict = self.parse_vehicle_log_get_check_data(vehicle_log)
        # # 补充校验内容
        # self.add_check_info(check_data_dict, vid=vid, device_name=device_name)
        # # 对上传数据进行校验
        # self.check_vehicle_log_and_upload_log(check_data_dict, vid=vid)
        self.parse_log_and_check(vehicle_log, vid, device_name)

    def make_error(self, device_name=DeviceName.BGM, **kwargs):
        '''
        制造异常 去触发日志上传
        @param device_name:
        @param kwargs:
        @return:
        '''
        if device_name == DeviceName.BGM:
            cmd = """cat /app/etc/bgm_app_env.sh"""
            string = self.ssh.type_commands(device_name, cmd)

            lis = [item.strip() for item in string.split("\n") if item.strip() and item.startswith("export")]
            cmd = ';'.join(lis)
            logger.info(f"cmd={cmd}")
            ret_msg = self.ssh.type_commands(device_name, cmd)
            cmd = " cd /app/bin; ./monitor_client_test"
            self.ssh.type_commands(device_name, cmd, timeout=30)
        else:
            cmd = """cat /oemapp/jiduEM.sh"""
            string = self.ssh.type_commands(device_name, cmd)
            lis = [item.strip() for item in string.split("\n") if item.strip() and item.startswith("export")]
            cmd = ';'.join(lis)
            logger.info(f"cmd={cmd}")
            ret_msg = self.ssh.type_commands(device_name, cmd)
            cmd = " cd /oemapp/bin/; ./monitor_client_test"
            self.ssh.type_commands(device_name, cmd, timeout=30)

        # kill 进程
        cmd = "\x03"
        logger.info(f"停止 error cmd={cmd}")
        try:
            self.ssh.type_commands(device_name, cmd, timeout=5)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/log_trigger_handler.py")
            logger.error(f"停止 error 失败 {str(e)}！！")
        return 1, ""

    def kill_pid_to_create_coredump(self, device_name=DeviceName.BGM, **kwargs):
        '''
        kill 进程 让bgm/TCAM   产生coredump 文件
        @param device_name:
        @param kwargs:
        @return:
        '''
        process_name = kwargs.get("process_name", "vehInfoServer")  # kill的进程名字
        logger.info(f"kill {device_name.name} {process_name} 进程 制造 coredump")

        def judge_coredump(device_name, old_files_name_list, new_files_name_list):

            if new_files_name_list is None:
                log_string = f"{device_name.name} 执行kill后 未产生 coredump 文件 "
                with allure.step(log_string):
                    logger.info(log_string)
                return 0, log_string
            if old_files_name_list is not None:
                if new_files_name_list != old_files_name_list:
                    new_lis = [item for item in new_files_name_list if
                               item not in old_files_name_list]
                    log_string = f"{device_name.name} 执行kill后 产生coredump 文件{new_lis}"
                    with allure.step(log_string):
                        logger.info(log_string)
                    return 1, log_string
                else:
                    log_string = f"{device_name.name} 执行kill后 未产生新的 coredump 文件 "
                    with allure.step(log_string):
                        logger.info(log_string)
                    return 0, log_string

        def kill_process(device_name, process_name="vehInfoServer"):
            # top | grep em2
            # cmd = f"top -n 10 | grep {process_name}"
            if device_name == DeviceName.BGM:
                pid_ind = 3
            else:
                pid_ind = 0
            cmd = f"ps -elf |grep -v grep | grep {process_name}"
            string = self.ssh.type_commands(device_name, cmd, timeout=120)
            logger.info(f"string={string}")
            pid_string = [item for item in string.split("\n") if process_name in item][0]

            pid = [item.strip() for item in pid_string.split(" ") if item.strip()][pid_ind]
            logger.info(f"pid={pid}")
            # pid = 3346
            kil_cmd = f"kill -6 {pid}"
            self.ssh.type_commands(device_name, kil_cmd)
            sleep(5)  # 让 coredump 文件产生，防止 误判
            # 看 进程是否起来
            string2 = self.ssh.type_commands(device_name, cmd, timeout=120)
            logger.info(f"string2={string2}")
            pid_string = [item for item in string2.split("\n") if process_name in item][0]
            pid2 = [item.strip() for item in pid_string.split(" ") if item.strip()][pid_ind]

            log_info = f"{process_name}原来进程{pid}重启后进程号{pid2}"
            logger.info(log_info)
            if int(pid2) > int(pid):
                return 1, log_info
            return 0, log_info

        try:
            #  干掉进程 制造 coredump
            if device_name == DeviceName.BGM:
                # 先判断 原来的coredump 文件
                old_files_name_list = self.ssh.get_bgm_coredump_names()
                ret, log_info = kill_process(device_name, process_name)
                if not ret:
                    return ret, log_info
                new_files_name_list = self.ssh.get_bgm_coredump_names()
                return judge_coredump(device_name, old_files_name_list, new_files_name_list)
            elif device_name == DeviceName.TCAM:
                old_files_name_list = self.get_tcam_coredump_names()
                ret, log_info = kill_process(device_name, process_name)
                if not ret:
                    return ret, log_info
                new_files_name_list = self.get_tcam_coredump_names()

                return judge_coredump(device_name, old_files_name_list, new_files_name_list)
            else:
                pass
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/log_trigger_handler.py")
            logger.error(f"{str(e)}")
            return 0, str(e)

    def get_tcam_coredump_names(self):
        '''
        获取tcam coredump  文件名字
        @return: 【】
        '''
        cmd = " ls /mnt/sdcard/"
        ret_msg = self.ssh.type_commands(DeviceName.TCAM, cmd)
        if "coredump" not in ret_msg:
            return []
        cmd = " find /mnt/sdcard/coredump -type f -exec stat -c '%y %s %n' {} \;"
        ret_msg = self.ssh.type_commands(DeviceName.TCAM, cmd)
        logger.info(f"ret_msg={ret_msg}")
        if ret_msg:
            # coredump = [item.strip() for item in ret_msg.split("\n").replace(" ", '') if item.strip()]
            coredump_list = [item.strip() for item in ret_msg.split("\n") if item.strip()]
            coredump = [item.split('/')[-1] for item in coredump_list]

            logger.info(f"coredump={coredump}")
            return coredump
        return []

    def get_exception_trigger_vehicle_log(self, device_name=DeviceName.BGM, timeout=600, **kwargs):
        '''
        获取 coredump 或者 error 引起的日志上传 相关日志
        @param device_name:
        @param timeout:
        @param kwargs:
        @return:
        '''
        error_conditions = kwargs.get("error_conditions", False)  # 是否断网
        exception_type = kwargs.get("exception_type", "coredump")  # 判断是coredump 还是error
        self.log_manage.log_manage.check_log_by_keywords_start_thread(
            log_type="RLog",
            keywords="Upload ==>> WaitUpload",
            unexpect_keywords=None,
            log_print=None,
            device_name=device_name.name,
            timeout=timeout
        )
        # 延时一段时间等ssh 启动
        time.sleep(10)
        # 判断是那种 异常触发
        if exception_type == "coredump":
            ret_code, ret_msg = self.kill_pid_to_create_coredump(device_name, **kwargs)
        else:
            # 制造 error
            ret_code, ret_msg = self.make_error(device_name, **kwargs)
        logger.info("等待日志上传")
        if ret_code:
            # 构造断网异常
            if error_conditions:
                t = 30
                logger.info(f"执行异常场景，延时一段时间{t}秒")
                time.sleep(t)
                self.ssh.set_airplane_mode(sts=isOn.On)
                time.sleep(3 * 60)
            # 关闭飞行模式
            self.ssh.set_airplane_mode(sts=isOn.Off)
            interface = self.ssh.type_commands(DeviceName.TCAM, 'ifconfig')
            if 'rmnet_data1' not in interface:
               logger.info('rmnet_data1不存在，再次关闭飞行模式')
            self.ssh.set_airplane_mode(isOn.Off)
            time.sleep(2)

        ret, vehicle_log = self.log_manage.log_manage.check_log_by_keywords_stop_thread()
        logger.info(f"vehicle_log={vehicle_log}")
        assert ret_code, ret_msg
        assert ret, f"超时{timeout}秒日志未上传结束"
        return vehicle_log

    def check_exception_trigger(self, vid, device_name=DeviceName.BGM, timeout=600, **kwargs):
        '''
        配置触发上传 校验
        @param vid:
        @param device_name:
        @param timeout:
        @param kwargs:
        @return:
        '''
        # 检查环境
        self.check_vehicle_log_is_uploading(device_name=device_name, timeout=timeout)
        # 触发日志上传，获取日志
        vehicle_log_msg = self.get_exception_trigger_vehicle_log(device_name=device_name, timeout=timeout,
                                                                 **kwargs)
        self.parse_log_and_check(vehicle_log_msg, vid, device_name)
        # 解析日志
        # filter_vel_log_dict, check_data_dict = self.parse_vehicle_log_get_check_data(vehicle_log_msg)
        # # 补充校验内容
        # self.add_check_info(check_data_dict, vid=vid, device_name=device_name)
        # # 对上传数据进行校验
        # self.check_vehicle_log_and_upload_log(check_data_dict, vid=vid)
        # 校验event
        # self.check_vehicle_and_trigger_event(filter_vel_log_dict, **kwargs)

    def parse_log_and_check(self, vehicle_log_msg, vid, device_name=DeviceName.BGM):
        '''
        解析日志 校验日志
        @param vehicle_log_msg:
        @param vid:
        @param device_name:
        @return:
        '''

        # 解析日志
        filter_vel_log_dict, check_data_dict = self.parse_vehicle_log_get_check_data(vehicle_log_msg)
        # 补充校验内容
        self.add_check_info(check_data_dict, vid=vid, device_name=device_name)
        # 对上传数据进行校验
        self.check_vehicle_log_and_upload_log(check_data_dict, vid=vid)

    def send_soa_request(self, partner_key, method_name, args, timeout=10, **kwargs):
        try:
            # self.soa.send_request_and_ck_resp(partner_key, method_name, args, timeout=timeout)
            timeout= 10 if timeout<10 else timeout
            ret = self.soa.send_request_and_return_resp(partner_key, method_name, args, timeout=timeout)
            string = "发送soa 服务 成功"
            with allure.step(string):
                logger.info(string)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/api/interfaces/dp1/log_trigger_handler.py")
            string = "发送soa 服务 失败 !!!!!!!!!!!!"
            with allure.step(string):
                logger.error(string)
            ret = {"out": ""}
        return ret

    # ################ ltg  end ######################################################

    # ################ hl   ######################################################
    def get_log_timestamp(self, log_data):
        result = log_data
        temp = re.findall(r".*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})(.*)", result)
        if temp:
            rs = []
            for info in temp:
                rs.append((int(self.datetime_to_timestamp(info[0])) + 8 * 60 * 60, info[1]))
            return rs

    # 删除日志
    def delete_device_old_log(self, device_name=DeviceName.BGM):
        exclude_bts_file = ''
        exclude_messages_file = ''
        exclude_s2s_file = ''
        if device_name == DeviceName.BGM:
            commands = 'ls /log'
            ret_msg = self.ssh.type_commands(DeviceName.BGM, commands=commands, timeout=30)
            string_list = [item.split(' ') for item in ret_msg.replace('\t', ' ').split('\n')]
        elif device_name == DeviceName.TCAM:
            commands = 'ls /mnt/sdcard/log'
            ret_msg = self.ssh.type_commands(DeviceName.TCAM, commands=commands, timeout=30)
            cleaned_content = re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', ret_msg)
            # 将制表符替换为空格
            cleaned_content = cleaned_content.replace('\t', ' ')
            string_list = [filter(None, re.split(r'\s+', line)) for line in cleaned_content.split('\n')]
        data_lis = []
        for item_lis in string_list:
            lis = [item.strip() for item in item_lis if item.strip()]
            if lis:
                data_lis.extend(lis)
        # jetlog_messages217_20241024200228_96a6d466a6234c83ab59744acdc1c18a.zst
        messages_dic = {int(item.split("_")[1][len("messages"):]): item for item in data_lis if
                        item.startswith('jetlog_messages') and item != "jetlog_messages"}
        if messages_dic:
            max_messages = max(list(messages_dic.keys()))
            logger.info(f"jetlog_messages 共{len(messages_dic)}个 最大文件 为{messages_dic.get(max_messages)}")
            exclude_messages_file = messages_dic.get(max_messages, '')

        bts_dic = {int(item.split("_")[1][len("bts"):]): item for item in data_lis if
                   item.startswith('jetlog_bts') and item != "jetlog_bts"}
        if bts_dic:
            max_bts = max(list(bts_dic.keys()))
            logger.info(f"jetlog_bts 共{len(bts_dic)}个 最大文件 为{bts_dic.get(max_bts)}")
            exclude_bts_file = bts_dic.get(max_bts, '')

        s2s_dic = {int(item.split("_")[1][len("s2s"):]): item for item in data_lis if
                   item.startswith('jetlog_s2s') and item != "jetlog_s2s"}
        if s2s_dic:
            max_s2s = max(list(s2s_dic.keys()))
            logger.info(f"jetlog_s2s 共{len(s2s_dic)}个 最大文件 为{s2s_dic.get(max_s2s)}")
            exclude_s2s_file = s2s_dic.get(max_s2s, '')
        excludes = []
        if exclude_bts_file:
            excludes.append(f'! -name "{exclude_bts_file}"')
        if exclude_messages_file:
            excludes.append(f'! -name "{exclude_messages_file}"')
        if exclude_s2s_file:
            excludes.append(f' ! -name "{exclude_s2s_file}"')
        if device_name == DeviceName.BGM:
            commands = f'find /log -type f -name "jetlog_*.zst" {" ".join(excludes)} -exec rm -f {{}} \\;'
        elif device_name == DeviceName.TCAM:
            commands = f'find /mnt/sdcard/log -type f -name "jetlog_*.zst" {" ".join(excludes)} -exec rm -f {{}} \\;'
        logger.info(f"remove_log={commands}")
        self.ssh.type_commands(device_name, commands=commands, timeout=60)

    # 拉取异常场景的日志    # 拉取异常场景的日志
    def get_upload2waitupload_log(self, device_name=DeviceName.BGM, timeout=600, **kwargs):

        self.log_manage.log_manage.check_log_by_keywords_start_thread(
            log_type="RLog",
            keywords="Upload ==>> WaitUpload",
            unexpect_keywords=None,
            log_print=None,
            device_name=device_name.name,
            timeout=timeout
        )
        ret, jet_log_msg = self.log_manage.log_manage.check_log_by_keywords_stop_thread()
        # assert ret, "check_log_by_keywords_stop_thread failed"
        if device_name == DeviceName.BGM:
            ret_log = self.ssh.bgm_ssh.type_commands('/app/bin/zstdcat /log/jetlog_messages* -n | grep RLog')
        else:
            ret_log = self.ssh.tcam_ssh.type_commands(
                '/oemapp/bin/zstdcat /mnt/sdcard/log/jetlog_messages* -n |grep RLog')

        logger.info(f"获取的车端日志{'*' * 100}")
        logger.info(f"ret_log={ret_log}")
        logger.info(f"获取的车端日志end {'*' * 100}")
        pattern = '(.*?)Upload ==>> WaitUpload'  # 要匹配的模式，这里是所有的'a'
        # strig = 'banana'
        matches = re.findall(pattern, ret_log)
        if len(matches) == 1:
            return ret_log
        elif len(matches) > 1:
            # msg = ret_log.split(matches[-2])[-1]
            msg2 = ret_log.split(matches[0])
            msg = "".join(msg2[1:])
            logger.info(f"处理后的车端日志{'*' * 100}")
            logger.info(f"ret_log=\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n{msg}\n\n\n\n\n\n\n\n\n\n\n\n")
            logger.info(f"处理后的车端日志 end {'*' * 100}")
            return msg
        else:
            assert 0, "未匹配到 Upload ==>> WaitUpload 数据"

    # 拉取异常场景的日志    # 拉取异常场景的日志
    def check_upload2waite(self, trigger_mode=1, device_name=DeviceName.BGM, timeout=600,
                           **kwargs):
        """
        从指定设备获取断电异常日志。

        Args:
            trigger_mode (int, optional): 触发模式，默认为1。
                1表示远程拉取目录；
                2表示配置下发；
                3表示触发
                4 coredum
                5 error
            device_name (DeviceName, optional): 设备名称，默认为DeviceName.BGM。
            timeout:查询日志超时时间，默认为30s

        Returns:
            str: 从设备获取的异常日志内容。

        Raises:
            ValueError: 如果设备名称无效，将抛出ValueError异常。
        """
        # 删除日志
        self.delete_device_old_log(device_name)
        # 触发上传
        # 监测'WaitUpload ==>> Upload'后开始制造异常
        self.log_manage.log_manage.device_name = device_name.name
        self.log_manage.log_manage.check_log_by_keywords_start_thread(
            log_type="RLog",
            keywords="WaitUpload ==>> Upload",
            unexpect_keywords=None,
            log_print=None,
            device_name=device_name.name,
            timeout=timeout
        )
        # 1 远程拉取目录
        if trigger_mode == 1:
            self.remote_upload_file_trigger(domain=device_name.value)
        # 2 配置下发
        elif trigger_mode == 2:
            if device_name == DeviceName.BGM:
                trigger_type = 'bgm_remote'
                source = 1
            elif device_name == DeviceName.TCAM:
                trigger_type = 'tcam_remote'
                source = 2
            self.config_trigger_to_valid(trigger_type=trigger_type, source=source)
        # 3 触发（coredump、error）
        elif trigger_mode == 3:
            if device_name == DeviceName.BGM:
                partner_key = 'RemoteLogManagerService_client_BGM_RemoteLogManagerService'
            elif device_name == DeviceName.TCAM:
                partner_key = 'RemoteLogManagerService_client_TCAM_RemoteLogManagerService'
            method_name = 'ReqUploadLog'
            soa_parameters = kwargs.get("soa_parameters", {})
            ck_info = {'out': 0}  # 默认 不需要填
            soa_timeout = 1  # 默认 不需要填
            cycle_time = 0.2  # 默认 不需要填
            is_async = False  # 默认 不需要填
            fuzz_match = True  # 默认 不需要填
            self.send_soa_request(partner_key, method_name, soa_parameters)
        elif trigger_mode == 4:
            ret_code, ret_msg = self.kill_pid_to_create_coredump(device_name, **kwargs)
            if not ret_code:
                self.log_manage.log_manage.check_log_by_keywords_stop_thread()
                assert 0, "产生coredump失败"
        elif trigger_mode == 5:
            self.make_error(device_name)
        ret, jet_log_msg = self.log_manage.log_manage.check_log_by_keywords_stop_thread()
        logger.info(f"jet_log_msg={jet_log_msg}")
        assert ret, "未触发上传日志，未检查到关键字WaitUpload ==>> Upload  "

    def vehicle_power_off_exception_log_fetcher(self, trigger_mode=1, device_name=DeviceName.BGM, timeout=600,
                                                **kwargs):
        """
        从指定设备获取断电异常日志。

        Args:
            trigger_mode (int, optional): 触发模式，默认为1。
                1表示远程拉取目录；
                2表示配置下发；
                3表示触发（coredump、error）。
            device_name (DeviceName, optional): 设备名称，默认为DeviceName.BGM。
            timeout:查询日志超时时间，默认为30s

        Returns:
            str: 从设备获取的异常日志内容。

        Raises:
            ValueError: 如果设备名称无效，将抛出ValueError异常。
        """
        self.check_upload2waite(trigger_mode, device_name, timeout=60)
        # 触发断电异常
        if device_name == DeviceName.BGM:
            self.io.io_reset_bgm(10)
            time.sleep(20)
        elif device_name == DeviceName.TCAM:
            self.io.tcam_power_off()
            time.sleep(30)
            self.io.tcam_power_on()
            logger.info("tcam 重启等待5分钟")
            time.sleep(5 * 60)
        else:
            raise ValueError(f"Invalid ECU name: {device_name}. Please use 'bgm' or 'tcam'.")
        log = self.get_upload2waitupload_log(device_name, timeout)
        with open("log_exception_test.txt", "w", encoding="utf-8") as f:
            f.write(log)
        return log

    def vehicle_reset_1181_exception_log_fetcher(self, trigger_mode=1, device_name=DeviceName.BGM, timeout=600,
                                                 **kwargs):
        """
        从指定设备获取诊断复位异常日志。

        Args:
            trigger_mode (int, optional): 触发模式，默认为1。
                1表示远程拉取目录；
                2表示配置下发；
                3表示触发（coredump、error）。
            device_name (DeviceName, optional): 设备名称，默认为DeviceName.BGM。
            timeout:查询日志超时时间，默认为30s

        Returns:
            str: 从设备获取的异常日志内容。

        Raises:
            ValueError: 如果设备名称无效，将抛出ValueError异常。
        """
        self.check_upload2waite(trigger_mode, device_name, timeout=60)
        # 触发诊断复位
        if device_name == DeviceName.BGM:
            self.sd_tester.update_serverdoipid(0X1FFF)
            self.sd_tester.send_data([0x11, 0x81])
            time.sleep(30)
        elif device_name == DeviceName.TCAM:
            self.sd_tester.update_serverdoipid(0X1011)
            self.sd_tester.send_request_and_recv_response([0x10, 0x03], recv=[0x50, 0x03])
            self.sd_tester.send_request_and_recv_response([0x11, 0x03], recv=[0x51, 0x03])
            time.sleep(4 * 60)
        log = self.get_upload2waitupload_log(device_name, timeout)
        with open("log_exception_test.txt", "w", encoding="utf-8") as f:
            f.write(log)
        return log

    def vehicle_network_sleep_exception_log_fetcher(self, trigger_mode=1, device_name=DeviceName.BGM, timeout=600,
                                                    **kwargs):
        """
        从指定设备获取休眠唤醒中断开异常日志。

        Args:
            trigger_mode (int, optional): 触发模式，默认为1。
                1表示远程拉取目录；
                2表示配置下发；
                3表示触发（coredump、error）。
            device_name (DeviceName, optional): 设备名称，默认为DeviceName.BGM。
            timeout:查询日志超时时间，默认为30s

        Returns:
            str: 从设备获取的异常日志内容。

        Raises:
            ValueError: 如果设备名称无效，将抛出ValueError异常。
        """
        self.check_upload2waite(trigger_mode, device_name, timeout=60)
        # 休眠唤醒
        self.mix.network_sleep()
        self.mix.set_tcam_bgm_to_wakeup()
        self.mix.chk_tcam_ping()
        self.mix.chk_bgm_ping()
        log = self.get_upload2waitupload_log(device_name, timeout)
        with open("log_exception_test.txt", "w", encoding="utf-8") as f:
            f.write(log)
        return log

    # ################ hl  end  ######################################################
