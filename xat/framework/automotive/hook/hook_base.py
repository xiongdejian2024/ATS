from framework.automotive.core.resources import LOCK_SCRIPT, workspace_relative
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :hook_class.py
@time         :2/7/24 14:41
@author       :dejian.xiong@jiduauto.com
@description  :定义各种钩子实现
"""
import os
import json
import shlex
import sys
import time
from queue import Queue
from typing import Union

from xat_ecu.legacy.interface.nuc_app import get_nuc_wifi_ip
from pytest import Parser, Config

from xat_ecu.legacy.common.logger import Logger
from framework.automotive.communication.client import DistClient

from framework.automotive.utils.bench_helper import BenchHelper
from framework.automotive.utils.case_info_helper import CaseInfoHelper, CaseFeedBackHelper
from framework.automotive.utils.new_relay_helper import jy_dam0800_check_and_repair_new
from framework.automotive.utils.conftest_helper import parent_dir, change_bgm_vehicle_model, record_top_thread

from framework.automotive.utils.data_type import EnvPropertiesInfo, EcuInfo, ReportInfo, CustomParameters, \
    PytestProcess, Domain, CaseProgress, BenchStatus, BenchConfig, HeartBeat, VehicleModel, BenchLockStatus, RunningEnv
from framework.automotive.utils.database_helper import DatabaseHelper
from framework.automotive.utils.email_helper import EmailHelper
from framework.automotive.utils.feishu_helper import FeishuHelper
from framework.automotive.utils.ms_helper import MsHelper
from framework.automotive.utils.partner_helper import PartnerHelper
from framework.automotive.utils.report_helper import ReportHelper
from framework.automotive.utils.thread_helper import ThreadPoolManager
from framework.automotive.utils.willow_helper import WillowHelper, WillowConfigForFeishu, get_version_from_url
from framework.automotive.utils.tasks_helper import JobInfo, TaskHelper
from framework.automotive.utils.conftest_helper import bench_resource_collect_thread


class BaseHooks:
    def __init__(self):
        self.disable_env = None
        self.is_flash = True
        self.result_description = None
        self.version_info = None
        self.ms_client = None
        self.disable_partner = None
        self.testplanid = None
        self.errfarmatcase_list = []
        self.testresult = "Pass"
        self.testresult_dict = {}
        self.is_deploy_soapartner = None
        self.fail_case_result_description = None
        self.ms_casesinfo = None
        self.new_ms_cases_info = None
        self.wifi_localhost = None
        self.jama_id_mapping = None
        self.is_onlypass = None
        self.is_disable_partner = None
        self.plan_id = None
        self.sec_planId = None
        self.is_willow = False
        self.willow_task_path = None
        self.willow_report_summary_path = None
        self.willow_report_path = None
        self.running_env: RunningEnv = RunningEnv(**{})
        self.pytest_process: PytestProcess = PytestProcess(**{})
        self.ms_failedcases_idlist = []
        self.report_to_willow = None
        self.willow_feishu_config_info = WillowConfigForFeishu(version_num='', case_type='', job_type='', job_owner='',
                                                               fail_case_sheet_name='', fail_case_document_id='',
                                                               feishu_rule_key='')
        self.report_info: ReportInfo = ReportInfo(**{})
        self.case_progress: CaseProgress = CaseProgress(**{})
        self.ecuinfo: EcuInfo = EcuInfo(**{})
        self.env_properties_info: EnvPropertiesInfo = EnvPropertiesInfo(**{})
        self.custom_parameters: CustomParameters = CustomParameters(**{})
        self.ms = MsHelper()
        self.feishu = FeishuHelper()
        self.partner = PartnerHelper()
        self.willow = WillowHelper()
        self.bench = BenchHelper()
        self.report = ReportHelper()
        self.email = EmailHelper()
        self.case = CaseInfoHelper()
        self.feed_back = CaseFeedBackHelper()
        self.database = DatabaseHelper()
        self.start_time = time.time()
        self.tasks = ThreadPoolManager()
        self.is_bench_check = False
        self.sync_ms_fail_num = 0
        self.job_info = JobInfo()  # 分布式执行时，计划执行总用例数
        self.sync_ms_result = True
        self.slave_client: Union[DistClient, None] = None
        self.slave_queue = Queue()

    def pytest_addoption(self, parser: Parser):
        parser.addoption(
            "--tbcfg", action="store", default='', help="testbed config YAML file"
        )
        parser.addoption(
            "--tccfg",
            action="store",
            default='config/latest_config.yaml',
            help="testcase config YAML file",
        )
        parser.addoption(
            "--logpath", action="store", default='./logs', help="path of log folder"
        )
        parser.addoption(
            "--loglevel",
            action="store",
            default='INFO',
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            help="Default log level, pcan be DEBUG/INFO/WARNING/ERROR/CRITICAL",
        )
        parser.addoption(
            "--file_loglevel",
            action="store",
            default='DEBUG',
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            help="Default file log level, pcan be DEBUG/INFO/WARNING/ERROR/CRITICAL",
        )
        parser.addoption(
            "--sdb_ver", action="store", default='default', help="arxml version"
        )
        parser.addoption("--soa_ver", action="store", default='default', help="soa version")
        parser.addoption(
            "--veh_type",
            action="store",
            default='',
            help="车型参数，设定时会覆盖配置文件中的车型参数信息，一般配合--bl_ver使用，实现自定义车型的数据库版本，"
                 "详见ecu_simulator/config下"
        )
        parser.addoption(
            "--bl_ver",
            action="store",
            default='',
            help="数据库版本，例如v_2_0_0，详见ecu_simulator/config下，指定时会加载对应版本的数据库"
        )
        parser.addoption(
            "--testplan", action="store", default='', help="test plan ID on MS"
        )
        parser.addoption(
            "--sec_planId", action="store", default='', help="test plan ID on MS"
        )
        parser.addoption(
            "--onlypass",
            choices=['true', 'false'],
            default=False,
            help="前提需要有testplan才生效, 为 'true' 时, test plan 只更新pass结果",
        )
        parser.addoption(
            "--disable_partner",
            action="store",
            choices=['true', 'false'],
            default=False,
            help="默认不禁用soa partner更新检查，用户可以设置true禁用soa partner更新",
        )
        parser.addoption(
            "--disable_env",
            action="store",
            choices=['true', 'false'],
            default=False,
            help="默认不禁用获取环境信息，用户可以设置true禁用获取环境信息",
        )
        parser.addoption(
            "--execute_type",
            action="store",
            choices=['fn', 'n'],
            default='',
            help="fn ---- test plan 只收集执行失败的和没有测试的用例，需要配合testplan一起使用"
                 "n  ---- test plan 只收集执行没有测试的用例，需要配合testplan一起使用"
        )
        parser.addoption(
            "--record_log",
            action="store",
            choices=['true', 'false'],
            default=True,
            help="为true时，自动录制jetlog日志，为false不录制，默认为录制",
        )
        parser.addoption(
            "--trace_log",
            action="store",
            choices=['true', 'false'],
            default=True,
            help="为true时,自动录制总线报文，为false不录制，默认为录制",
        )
        parser.addoption(
            "--version_info",
            action="store",
            default='',
            help="被测版本",
        )
        parser.addoption(
            "--result_description",
            action="store",
            default='',
            help="结果说明",
        )
        parser.addoption(
            "--sdb_version",
            action="store",
            default='',
            help="数据库版本例如v1.3.0，主要是应用在升级上，需要跟--release_version配套使用",
        )
        parser.addoption(
            "--release_version",
            action="store",
            default='',
            help="释放版本例如AQ,AH等，主要是应用在升级上，需要跟--sdb_version配套使用",
        )
        parser.addoption(
            "--task_id",
            action="store",
            default='',
            help="FOTA task id",
        )
        parser.addoption(
            "--soft_id",
            action="store",
            default='',
            help="FOTA soft id, for bridge",
        )
        parser.addoption(
            "--e2e_info",
            action="store",
            default='',
            help="FOTA e2e info",
        )
        parser.addoption(
            "--fota_tcam_version",
            action="store",
            default='',
            help="FOTA TCAM被测版本",
        )
        parser.addoption(
            "--report_to_willow",
            choices=['BGM', 'TCAM', 'CDC', 'ACU'],
            action="store",
            help="上传报告到willow平台，当前字段只能在willow上执行，参数类型是BGM,TCAM,CDC,ACU"
        )
        parser.addoption(
            "--distributed",
            action="store",
            choices=['true', 'false', 'None'],
            default=None,
            help="是否分布式执行case，为True时表示master端，为False表示slave端，不填则是非分布式执行"
        )
        parser.addoption(
            "--plan_id",
            action="store",
            default="",
            help="计划ID，该id与测试计划有差别，不进行回填，可与-m一起使用，参数为ms标签，由于目前ms上的标签部分是有空格字符的，"
                 "例如Mars One，如果使用-m指定了，需要加下划线，否则会出问题，也就是Mars One改成Mars_One，中间多个空格只加一个下划线"
        )
        parser.addoption(
            "--bench_count",
            action="store",
            type=int,
            default=None,
            help="分布式申请的任务数量，默认为3个"
        )
        parser.addoption(
            "--ip",
            action="store",
            type=str,
            default=None,
            help="非分布式运行时，可指定台架ip运行"
        )
        parser.addoption(
            "--disable_lock",
            action="store_true",
            help="是否跳过台架分布式锁",
        )
        parser.addoption(
            "--is_flash",
            choices=['true', 'false'],
            default=True,
            help="分布式是否跳过台架升级",
        )
        parser.addoption(
            "--by_platform",
            choices=['true', 'false'],
            default=True,
            help="分布式的通讯方式，默认true数据平台，可选false实时双端通讯",
        )
        parser.addoption(
            "--dist_id",
            type=str,
            default=None,
            help="分布式运行的唯一id",
        )

    def pytest_configure(self, config: Config):
        if config.getoption("--help") or config.getoption("-h"):
            return
        logger = self._init_args(config)
        # 获取命令行原始打印
        cmd = shlex.join(sys.argv[1:])
        if cmd == "-s bgm_tools/test_check_prenv.py --disable_env=true --record_log=false --trace_log=false":
            self.is_bench_check = True
        logger.info(self.is_bench_check)
        self.ecuinfo.cmd = cmd
        # 分布式master进程
        if self.pytest_process.Master:
            self._master_process_start(logger)
        # 分布式slave进程
        elif self.pytest_process.Slave:
            self._slave_process_start(logger)
        # 非分布式进程
        elif self.pytest_process.NonDist:
            self._nondist_process_start(logger)

        self.willow_feishu_config_info.wifi_localhost = self.wifi_localhost
        bench_resource_collect_thread()

    def _slave_process_start(self, logger):
        # 分布式SIL环境
        if self.running_env.SIL:
            self.tccfg = self.bench.get_tccfg(self.tccfg)
            self.tbcfg = {"bus": {}}  # 防止启动总线报错
            self.wifi_localhost = os.environ["HOST_IP"] if os.environ["HOST_IP"] else '127.0.0.1'
            if self.by_platform:
                bench_config = BenchConfig(
                    **{"host": self.wifi_localhost, "distribute_task_id": self.bench.task_json.get('uuid')})
                self.willow_feishu_config_info.distibute_task_id = self.bench.task_json.get('uuid')
                self.tasks.add_task(f'{self.wifi_localhost}_ed', self.bench.submit_bench_status, bench_config,
                                    BenchStatus.case_running)
                self.tasks.add_task(f'heartbeat', self.bench.set_heartbeat_start, self.wifi_localhost, 'slave',
                                    HeartBeat.online, self.bench.task_json.get('uuid'))
            bench_type = self.bench.get_sil_bench_type()
            version = self.bench.get_framework_version_info()
            # 更新自动化版本信息到数据库中
            self.ecuinfo.framework_version = version
            framework_version_id = self.database.update_ms_framework_version_info(**version)
            self.ecuinfo.frameworkVersionId = framework_version_id
            self.custom_parameters.veh_type = self.veh_type
            self.custom_parameters.bl_ver = self.bl_ver
            domain_info: Domain = self.bench.get_bench_domain_info(bench_type)
            if self.disable_env is True:
                self.cache_info = self.bench.get_cache_diag_info()
            if self.disable_partner is False:
                logger.info("获取 soa partner 版本信息")
                if self.disable_env is True:
                    try:
                        soa_name = self.cache_info.get('ssh').get('soa_name')
                    except AttributeError:
                        soa_name = self.partner.get_soa_name_on_sil(domain_info)
                else:
                    soa_name = self.partner.get_soa_name_on_sil(domain_info)
                bootesflag = False if "apus" in soa_name else True
                logger.info(f"bootesflag is {bootesflag},soa_name is {soa_name}")

                # 是否需要部署soa partner
                self.is_deploy_soapartner = self.partner.check_soa_partner(soa_name)
                if self.is_deploy_soapartner:
                    self.partner.deploy_soapartner(soa_name)
            else:
                logger.info(f'--disable_partner配置为{self.disable_partner}, 不部署soa partner')
            self.ecuinfo.tb_config = self.tbcfg
            self.ecuinfo.tc_config = self.tccfg
            logger.info(domain_info)
            self.ecuinfo.domain = domain_info
        else:
            if os.system(f"bash \"{LOCK_SCRIPT}\" -t") != 0:
                os._exit(1)
            if not self.by_platform:
                server_ip = self.bench.task_json.get('master_config').get('service_ip')
                server_port = self.bench.task_json.get('master_config').get('service_port')
                logger.info(f"server_ip:{server_ip},server_port:{server_port}")
                if server_ip and server_port:
                    self.slave_client = DistClient(ip=server_ip, port=server_port, queue=self.slave_queue)
                    self.slave_client.setName("slave_client")
                    self.slave_client.setDaemon(True)
                    self.slave_client.start()
            self.bench.clear_bench_log()
            self.tbcfg = self.bench.get_tbcfg(self.tbcfg)
            self.tccfg = self.bench.get_tccfg(self.tccfg)
            self.wifi_localhost = self.tbcfg.get("wifi_localhost")
            if self.by_platform:
                bench_config = BenchConfig(
                    **{"host": self.wifi_localhost, "distribute_task_id": self.bench.task_json.get('uuid')})
                self.willow_feishu_config_info.distibute_task_id = self.bench.task_json.get('uuid')
                self.tasks.add_task(f'{self.wifi_localhost}_ed', self.bench.submit_bench_status, bench_config,
                                    BenchStatus.case_running)
                self.tasks.add_task(f'heartbeat', self.bench.set_heartbeat_start, self.wifi_localhost, 'slave',
                                    HeartBeat.online, self.bench.task_json.get('uuid'))
            version = self.bench.get_framework_version_info()
            # 更新自动化版本信息到数据库中
            self.ecuinfo.framework_version = version
            framework_version_id = self.database.update_ms_framework_version_info(**version)
            self.ecuinfo.frameworkVersionId = framework_version_id
            self.custom_parameters.veh_type = self.veh_type
            self.custom_parameters.bl_ver = self.bl_ver
            if self.disable_env is True:
                self.cache_info = self.bench.get_cache_diag_info()
            if self.disable_env is False and self.is_willow:
                bench_version_info = self.bench.get_bench_version_info(self.wifi_localhost)
                # 更新ms_bench_version表
                self.ecuinfo.benchVersionId = self.database.update_ms_bench_version_info(**bench_version_info)
            domain_info: Domain = self.bench.get_bench_domain_info(self.tbcfg)
            if "power_control_type" in self.tbcfg:
                if self.tbcfg.get("power_control_type") == "jydam0800":
                    logger.info("执行台架jydam0800继电器状态检查")
                    jy_dam0800_check_and_repair_new(domain_info)
            if self.by_platform:
                change_bgm_vehicle_model(self.bench.task_json.get('vehicle_model'))
            # 是否部署partner
            if self.disable_partner is False:
                logger.info("获取 soa partner 版本信息")
                if self.disable_env is True:
                    try:
                        soa_name = self.cache_info.get('ssh').get('soa_name')
                    except AttributeError:
                        soa_name = self.partner.get_soa_name(domain_info)
                else:
                    soa_name = self.partner.get_soa_name(domain_info)
                bootesflag = False if "apus" in soa_name else True
                logger.info(f"bootesflag is {bootesflag},soa_name is {soa_name}")

                # 是否需要部署soa partner
                self.is_deploy_soapartner = self.partner.check_soa_partner(soa_name)
                if self.is_deploy_soapartner:
                    self.partner.deploy_soapartner(soa_name)
            else:
                logger.info(f'--disable_partner配置为{self.disable_partner}, 不部署soa partner')
            self.bench.set_env_info(domain_info, self.tbcfg, self.tccfg, self.custom_parameters)
            # 是否获取环境信息
            if self.disable_env is False:
                env_properties_info = self.bench.parse_get_env_info(
                    domain_info, self.tbcfg, self.tccfg, self.env_properties_info, self.willow_task_path)
                logger.info(f"domain version info is {env_properties_info}")
                self.ecuinfo.env_properties_info = env_properties_info
                if self.is_willow:
                    self.willow_feishu_config_info = self.willow.get_willow_config_for_feishu(
                        env_properties_info, self.willow_task_path)
            else:
                logger.info(f'--disable_env配置为{self.disable_env}, 通过缓存文件获取环境参数')
            self.env_properties_info.wifi_localhost = self.wifi_localhost
            self.ecuinfo.tb_config = self.tbcfg
            self.ecuinfo.tc_config = self.tccfg
            self.env_properties_info.sdk_version = self.ecuinfo.framework_version
            logger.info(domain_info)
            self.ecuinfo.domain = domain_info

    def _nondist_process_start(self, logger):
        # SIL
        if self.running_env.SIL:
            # self.tbcfg = self.bench.get_tbcfg(self.tbcfg)
            self.tccfg = self.bench.get_tccfg(self.tccfg)
            self.tbcfg = {"bus": {}}  # 防止启动总线报错
            bench_type = self.bench.get_sil_bench_type()
            domain_info: Domain = self.bench.get_bench_domain_info(bench_type)
            # setup_vlan(self.tbcfg.get('eth_vlan'), self.tbcfg.get('partner_domin', 'acu'))
            if self.disable_env is True:
                self.cache_info = self.bench.get_cache_diag_info()
            if self.disable_partner is False:
                logger.info("获取 soa partner 版本信息")
                if self.disable_env is True:
                    try:
                        soa_name = self.cache_info.get('ssh').get('soa_name')
                    except AttributeError:
                        soa_name = self.partner.get_soa_name_on_sil(domain_info)
                else:
                    soa_name = self.partner.get_soa_name_on_sil(domain_info)
                bootesflag = False if "apus" in soa_name else True
                logger.info(f"bootesflag is {bootesflag},soa_name is {soa_name}")

                # 是否需要部署soa partner
                self.is_deploy_soapartner = self.partner.check_soa_partner(soa_name)
                if self.is_deploy_soapartner:
                    self.partner.deploy_soapartner(soa_name)
            else:
                logger.info(f'--disable_partner配置为{self.disable_partner}, 不部署soa partner')
            self.ecuinfo.tb_config = self.tbcfg
            self.ecuinfo.tc_config = self.tccfg
            logger.info(domain_info)
            self.ecuinfo.domain = domain_info
            self.wifi_localhost = os.environ["HOST_IP"] if os.environ["HOST_IP"] else '127.0.0.1'
        # HIL
        else:
            self.tbcfg = self.bench.get_tbcfg(self.tbcfg)
            self.tccfg = self.bench.get_tccfg(self.tccfg)
            self.wifi_localhost = self.tbcfg.get("wifi_localhost")
            # 获取工作目录
            workspace = workspace_relative(os.getcwd())
            # 生成slave端的执行命令
            self.ecuinfo.cmd = f"cd {workspace};pytest {self.ecuinfo.cmd}"
            logger.info(self.ecuinfo.cmd)
            # 跳过分布式锁
            if not self.disable_lock:
                # 指定ip
                if self.ip:
                    data = self.database.get_query_lock_status(ip_addr=self.ip)
                    # -1代表无此台架，0代表台架空闲，1代表台架占用中，直接退出
                    if data == BenchLockStatus.not_exist.value:
                        logger.info(f"指定的台架不存在，直接退出")
                        os._exit(1)
                    elif data == BenchLockStatus.busy.value:
                        logger.info(f"指定的台架被分布式锁占用，直接退出")
                        os._exit(1)
                    else:
                        p_data = self.database.get_query_account_info(ip_addr=self.ip)
                        bench_config = BenchConfig(**{
                            'host': self.ip,
                            'username': p_data.get('userName'),
                            'password': p_data.get('password')
                        })
                        # 如果指定的ip与当前台架不一致，则远程到指定台架运行
                        if self.ip != self.wifi_localhost:
                            version = self.bench.get_framework_version_info()
                            self.ecuinfo.framework_version = version
                            self.bench.deploy_env_on_anther_bench(bench_config, self.ecuinfo)
                            os._exit(1)
                        # 直接加锁占用
                        else:
                            if os.system(f"bash \"{LOCK_SCRIPT}\" -t") != 0:
                                os._exit(1)
                # 如果不指定ip
                else:
                    # 判断当前台架是否被分布式锁占用
                    data = self.database.get_query_lock_status(ip_addr=self.wifi_localhost)
                    # 如果为分布式锁住，直接退出
                    if data == BenchLockStatus.busy.value:
                        logger.info(f"当前台架被分布式锁占用，直接退出")
                        os._exit(1)
                    # 如果不被分布式锁占用，则等待设备锁
                    else:
                        if os.system(f"bash \"{LOCK_SCRIPT}\" -t") != 0:
                            os._exit(1)
            version = self.bench.get_framework_version_info()
            # 更新自动化版本信息到数据库中
            self.ecuinfo.framework_version = version
            if self.disable_env is False and self.is_willow:
                framework_version_id = self.database.update_ms_framework_version_info(**version)
                self.ecuinfo.frameworkVersionId = framework_version_id
            self.custom_parameters.veh_type = self.veh_type
            self.custom_parameters.bl_ver = self.bl_ver
            self.bench.clear_bench_log()
            self.wifi_localhost = get_nuc_wifi_ip()
            if self.disable_env is True:
                self.cache_info = self.bench.get_cache_diag_info()
            if self.disable_env is False and self.is_willow:
                bench_version_info = self.bench.get_bench_version_info(self.wifi_localhost)
                # 更新ms_bench_version表
                self.ecuinfo.benchVersionId = self.database.update_ms_bench_version_info(**bench_version_info)
            domain_info: Domain = self.bench.get_bench_domain_info(self.tbcfg)
            if "power_control_type" in self.tbcfg:
                if self.tbcfg.get("power_control_type") == "jydam0800":
                    logger.info("执行台架jydam0800继电器状态检查")
                    jy_dam0800_check_and_repair_new(domain_info)
            # 是否部署partner
            if self.disable_partner is False:
                logger.info("获取 soa partner 版本信息")
                if self.disable_env is True:
                    try:
                        soa_name = self.cache_info.get('ssh').get('soa_name')
                    except AttributeError:
                        soa_name = self.partner.get_soa_name(domain_info)
                else:
                    soa_name = self.partner.get_soa_name(domain_info)
                bootesflag = False if "apus" in soa_name else True
                logger.info(f"bootesflag is {bootesflag},soa_name is {soa_name}")

                # 是否需要部署soa partner
                self.is_deploy_soapartner = self.partner.check_soa_partner(soa_name)
                if self.is_deploy_soapartner:
                    self.partner.deploy_soapartner(soa_name)
            else:
                logger.info(f'--disable_partner配置为{self.disable_partner}, 不部署soa partner')
            self.bench.set_env_info(domain_info, self.tbcfg, self.tccfg, self.custom_parameters)
            # 是否获取环境信息
            if self.disable_env is False:
                env_properties_info = self.bench.parse_get_env_info(
                    domain_info, self.tbcfg, self.tccfg, self.env_properties_info, self.willow_task_path)
                logger.info(f"domain version info is {env_properties_info}")
                self.ecuinfo.env_properties_info = env_properties_info
                if self.is_willow:
                    self.willow_feishu_config_info = self.willow.get_willow_config_for_feishu(
                        env_properties_info, self.willow_task_path)
            else:
                logger.info(f'--disable_env配置为{self.disable_env}, 通过缓存文件获取环境参数')
            self.env_properties_info.wifi_localhost = self.wifi_localhost
            self.env_properties_info.sdk_version = self.ecuinfo.framework_version
            self.ecuinfo.tb_config = self.tbcfg
            self.ecuinfo.tc_config = self.tccfg
            logger.info(domain_info)
            self.ecuinfo.domain = domain_info

    def _master_process_start(self, logger):
        self.tbcfg = self.bench.get_tbcfg(self.tbcfg)
        self.wifi_localhost = self.tbcfg.get("wifi_localhost")
        bench_group = self.database.get_query_benchgroup(ip_addr=self.wifi_localhost)
        if bench_group:
            if bench_group in ['NA', 'None', 'Loan']:
                logger.error("当前台架分组为NA、None或Loan，不执行分布式")
                os._exit(1)
        else:
            logger.error(f"当前台架分组不存在或{self.wifi_localhost}无线ip不存在，不执行分布式")
            os._exit(1)
        version = self.bench.get_framework_version_info()
        # 将slave端的distributed参数替换成false
        self.ecuinfo.cmd = self.ecuinfo.cmd.replace('--distributed=true', '--distributed=false')
        # 获取工作目录
        workspace = workspace_relative(os.getcwd())
        # 生成slave端的执行命令
        self.ecuinfo.cmd = f"cd {workspace};pytest {self.ecuinfo.cmd}"
        logger.info(self.ecuinfo.cmd)
        # 更新自动化版本信息到数据库中
        self.ecuinfo.framework_version = version
        self.database.update_ms_framework_version_info(**version)
        self.bench.clear_bench_log()
        self.ecuinfo.domain = self.bench.get_bench_domain_info(self.tbcfg)
        if self.is_willow:
            with open(self.willow_task_path, "r") as task_json:
                task = json.load(task_json)
            bgm_url = task.get("img_url", '')
            bgm_boot_url = task.get("img_url_boot", '')
            tcam_url = task.get("tcam_img_url", '')
            if bgm_url:
                sdb, bgm_ver = get_version_from_url(bgm_url)
                self.env_properties_info.SDB = sdb
            else:
                bgm_ver = None
            if bgm_boot_url:
                boot_ver = get_version_from_url(bgm_boot_url)[1]
                self.env_properties_info.bgm_boot_version = boot_ver
            if tcam_url:
                tcam_ver = get_version_from_url(tcam_url)[1]
            else:
                tcam_ver = None
            self.env_properties_info.software_version = dict(
                BGM=bgm_ver,
                TCAM=tcam_ver,
            )
            self.env_properties_info.sdk_version = self.ecuinfo.framework_version
            self.env_properties_info.wifi_localhost = self.wifi_localhost

    def _init_args(self, config):
        log_path = config.getoption("--logpath")
        log_level = config.getoption("--loglevel")
        file_log_level = config.getoption("--file_loglevel")

        # Initlalize logger which will be used for all project scripts
        # from ecu_simulator.common.logger import Logger
        logger = Logger(log_path=log_path, log_level=log_level, file_log_level=file_log_level).get_logger('test')
        logger.info(f"log_path is {log_path}")
        logger.info(f"log_level is {log_level}")
        logger.info(f"file_log_level is {file_log_level}")
        if config.getoption("--is_flash") == 'true':
            self.is_flash = True
        if config.getoption("--is_flash") == 'false':
            self.is_flash = False
        if config.getoption("--onlypass") == 'true':
            self.is_onlypass = True
        elif config.getoption("--onlypass") == 'false':
            self.is_onlypass = False
        else:
            self.is_onlypass = config.getoption("--onlypass")
        logger.info(f"is_onlypass is {self.is_onlypass}")
        if config.getoption("--disable_partner") == 'true':
            self.disable_partner = True
        elif config.getoption("--disable_partner") == 'false':
            self.disable_partner = False
        else:
            self.disable_partner = config.getoption("--disable_partner")
        logger.info(f"disable_partner is {self.disable_partner}")
        if config.getoption("--disable_env") == 'true':
            self.disable_env = True
        elif config.getoption("--disable_env") == 'false':
            self.disable_env = False
        else:
            self.disable_env = config.getoption("--disable_env")
        logger.info(f"disable_env is {self.disable_env}")
        if config.getoption("--distributed") == 'true':
            self.pytest_process.Master = True
            logger.info(f"is_flash is {self.is_flash}")
        elif config.getoption("--distributed") == 'false':
            self.pytest_process.Slave = True
            logger.info(f"is_flash is {self.is_flash}")
        elif config.getoption("--distributed") is None:
            self.pytest_process.NonDist = True
        logger.info(f"distributed is {self.pytest_process}")
        if "container" in os.environ.values():
            self.running_env.SIL = True
            logger.info(f"当前运行环境为SIL")
        else:
            self.running_env.HIL = True
            logger.info(f"当前运行环境为HIL")
        self.testplanid = config.getoption("--testplan")
        logger.info(f"testplanid is {self.testplanid}")
        self.sec_planId = config.getoption("--sec_planId")
        logger.info(f"sec_planId is {self.sec_planId}")
        self.execute_type = config.getoption("--execute_type")
        logger.info(f"execute_type is {self.execute_type}")
        self.version_info = config.getoption("--version_info")
        logger.info(f"version_info is {self.version_info}")
        self.result_description = config.getoption("--result_description")
        logger.info(f"result_description is {self.result_description}")
        self.tbcfg = config.getoption("--tbcfg")
        logger.info(f"tbcfg is {self.tbcfg}")
        self.tccfg = config.getoption("--tccfg")
        logger.info(f"tccfg is {self.tccfg}")
        self.report_to_willow = config.getoption('--report_to_willow')
        logger.info(f"report_to_willow is {self.report_to_willow}")
        self.raw_veh_type = config.getoption('--veh_type')
        if self.raw_veh_type == VehicleModel.MarsOne.value:
            self.veh_type = 'mars1'
        elif self.raw_veh_type == VehicleModel.Venus.value:
            self.veh_type = 'venus'
        elif self.raw_veh_type == VehicleModel.MarsOneICA.value:
            self.veh_type = 'mars1'
        elif self.raw_veh_type == VehicleModel.MarsOneMCA.value:
            self.veh_type = 'mars1'
        elif self.raw_veh_type == VehicleModel.Venus_800V.value:
            self.veh_type = 'venus'
        else:
            self.veh_type = None
        logger.info(f"veh_type is {self.veh_type}")
        self.bl_ver = config.getoption('--bl_ver')
        logger.info(f"bl_ver is {self.bl_ver}")
        self.plan_id = config.getoption('--plan_id')
        logger.info(f"plan_id is {self.plan_id}")
        self.soft_id = config.getoption('--soft_id')
        logger.info(f"soft_id is {self.soft_id}")
        self.bench_count = config.getoption('--bench_count')
        if self.bench_count:
            logger.info(f"bench_count is {self.bench_count}")
        self.ip = config.getoption('ip')
        if self.ip:
            logger.info(f"指定运行的台架ip is {self.ip}")
        self.disable_lock = config.getoption("--disable_lock")
        if self.disable_lock:
            logger.info(f"disable_lock is {self.disable_lock}")
        if config.getoption("--by_platform") == 'true':
            self.by_platform = True
            logger.info(f"分布式的通讯方式为数据平台")
        elif config.getoption("--by_platform") == 'false':
            self.by_platform = False
            logger.info(f"分布式的通讯方式为实时双端通讯")
        else:
            self.by_platform = config.getoption("--by_platform")
        (
            self.is_willow,
            self.willow_task_path,
            self.willow_report_summary_path,
            self.willow_report_path,
            self.time_now_year_month
        ) = self.willow.check_is_willow()
        if self.is_willow:
            logger.info(f"willow is {self.is_willow}")
        if self.willow_task_path:
            logger.info(f"willow_task_path is {self.willow_task_path}")
        if self.willow_report_summary_path:
            logger.info(f"willow_report_summary_path is {self.willow_report_summary_path}")
        if self.willow_report_path:
            logger.info(f"willow_report_path is {self.willow_report_path}")
        return logger
