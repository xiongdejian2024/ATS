#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :data_type.py
@time         :2/7/24 15:06
@author       :dejian.xiong@jiduauto.com
@description  :定义框架中用到的数据类型
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Union


@dataclass
class BaseData:
    def get(self, key, value=None):
        if hasattr(self, key):
            return getattr(self, key)
        return value

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def to_dict(self):
        return self.__dict__


@dataclass
class ReportInfo(BaseData):
    total: Union[str, int] = ''
    passed: Union[str, int] = ''
    failed: Union[str, int] = ''
    error: Union[str, int] = ''
    skipped: Union[str, int] = ''
    success_rate: str = ''
    duration_str: str = ''
    case_list: list = field(default_factory=list)
    case_fail_list: list = field(default_factory=list)
    num_check: list = field(default_factory=list)


@dataclass
class CaseProgress(BaseData):
    total: int = 0
    passed: int = 0
    failed: int = 0
    error: int = 0
    skipped: int = 0
    current_case: str = ''
    remain_case: int = 0
    sync_ms_fail: int = 0


@dataclass
class SoftwareVersion(BaseData):
    BGM: str = ''
    TCAM: str = ''
    ACU: str = ''
    CDC: str = ''


@dataclass
class HardwareVersion(SoftwareVersion):
    pass


@dataclass
class Domain(BaseData):
    single_bgm: Union[str, None] = None
    single_tcam: Union[str, None] = None
    two_domain: Union[str, None] = None
    four_domain: Union[str, None] = None
    bgm_cdc_acu: Union[str, None] = None
    bgm_tcam_acu: Union[str, None] = None
    bgm_tcam_cdc: Union[str, None] = None
    ccu_cd: Union[str, None] = None
    ccu_cd_lcu: Union[str, None] = None
    ccu_cd_ad: Union[str, None] = None
    ccu_cd_ad_lcu: Union[str, None] = None
    lcu_l: Union[str, None] = None
    lcu_r: Union[str, None] = None


@dataclass
class EnvPropertiesInfo(BaseData):
    software_version: Union[SoftwareVersion, None] = None
    hardware_version: Union[HardwareVersion, None] = None
    sdk_version: str = ''
    bgm_boot_version: str = ''
    bgm_mcu_version: str = ''
    bgm_switch_version: str = ''
    IDL: str = ''
    bootes_version: str = ''
    JIDLCompiler: str = ''
    wifi_localhost: str = ''
    veh_type: str = ''
    SDB: str = ''


@dataclass
class FrameworkVersion(BaseData):
    sdkInterfaceVersion: str = ''
    satFrameworkVersion: str = ''
    ecuSimulatorVersion: str = ''
    satCommitId: str = ''


@dataclass
class EcuInfo(BaseData):
    logpath: str = ''
    loglevel: str = ''
    record_log: str = ''
    trace_log: str = ''
    sdb_version: str = ''
    release_version: str = ''
    testresult: str = ''
    disable_env: bool = False
    case_start: float = 0.0  # 用例开始时间
    case_end: float = 0.0  # 用例结束时间
    testname: str = ''  # 用例名称
    cmd: str = ''  # 执行的原始命令
    tb_config: dict = field(default=dict)
    tc_config: dict = field(default=dict)
    domain: Union[Domain, None] = None
    env_properties_info: Union[EnvPropertiesInfo, None] = None
    framework_version: Union[FrameworkVersion, None] = None
    benchEcuId: Union[int, None] = None
    benchVersionId: Union[int, None] = None
    frameworkVersionId: Union[int, None] = None
    caseid = None
    bench_uuid = None
    log_path = {}
    class_uuid = None
    class_bgm_log = {}
    class_case_fail_flag = False


@dataclass
class CustomParameters(BaseData):
    """
    自定义参数
    """
    veh_type: str = ""
    bl_ver: str = ""


@dataclass
class PytestProcess(BaseData):
    Master: Union[bool, None] = None
    Slave: Union[bool, None] = None
    NonDist: Union[bool, None] = None


@dataclass
class RunningEnv(BaseData):
    HIL: Union[bool, None] = None
    SIL: Union[bool, None] = None


class BenchStatus(Enum):
    offline = 0  # 设备离线
    stop = 1  # 环境部署完成
    env_deploy = 3  # 环境部署中
    case_running = 4  # 用例运行中
    idle = 5  # 任务结束


class HeartBeat(Enum):
    online = 1
    offline = 0


@dataclass
class BenchConfig(BaseData):
    host: str  # 无线wifi
    limited_ip: str = ''  # 有线ip
    port: int = 22
    username: str = 'root'
    password: str = __import__("os").environ.get('XAT_CREDENTIAL_PYTEST___UTILS_DATA_TYPE_PY_PASSWORD', "")
    distribute_task_id: str = ''
    bgm_version: str = ''
    tcam_version: str = ''
    cdc_version: str = ''
    acu_version: str = ''


class SlaveTaskStatus(Enum):
    unable_run = -1
    not_start = 0
    running = 1
    finish = 2
    exit = 3


class VehicleModel(Enum):
    MarsOne = 'MarsOne'
    Venus = 'Venus'
    MarsOneMCA = 'MarsOneMCA'
    MarsOneICA = 'MarsOneICA'
    Venus_800V = 'Venus800v'


class RepoName(Enum):
    sat = 'ATS'
    sat_framework = 'xat/framework/automotive'
    sdk_interface = 'xat/packages/ecu/src/xat_ecu/api'


class BenchLockStatus(Enum):
    not_exist = -1
    idle = 0
    busy = 1


class CaseStatus(Enum):
    not_start = 0
    running = 1
    finished = 2


class TaskTarget(Enum):
    apply_case = 0
    update_case_status = 1


class ReportStatus(Enum):
    not_start = 0
    finished = 1


class PytestSlaveStatus(Enum):
    pytest_sessionstart = "pytest_sessionstart"
    pytest_collection_modifyitems = "pytest_collection_modifyitems"
    pytest_collection_finish = "pytest_collection_finish"
    pytest_runtestloop = "pytest_runtestloop"
    pytest_runtest_makereport = "pytest_runtest_makereport"
    pytest_terminal_summary = "pytest_terminal_summary"
    pytest_sessionfinish = "pytest_sessionfinish"
    pytest_unconfigure = "pytest_unconfigure"
    slave_offline = "slave_offline"
    handle_stop_task = "handle_stop_task"
    handle_start_task = "handle_start_task"
    list_all_tasks = "list_all_tasks"
    list_all_slave_status = "list_all_slave_status"
