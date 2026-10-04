#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :tasks_helper.py
@time         :5/15/24 14:11
@author       :dejian.xiong@jiduauto.com
@description  :定义框架各种task，供异步调用
"""
import os.path
import time
import uuid

from xat_ecu.legacy.common.logger import logger
from pathlib import Path

from xat_ecu.legacy.interface.nuc_app import exec_shell
from framework.automotive.utils.bench_helper import BenchHelper
from framework.automotive.utils.conftest_helper import parent_dir
from framework.automotive.core.resources import AUTOMOTIVE_ROOT
from framework.automotive.utils.data_type import SlaveTaskStatus, BenchConfig, EcuInfo, BenchStatus, HeartBeat
from framework.automotive.utils.database_helper import DatabaseHelper
from framework.automotive.utils.thread_helper import ThreadPoolManager

RETRY_COUNT = 3


class TaskHelper:

    @staticmethod
    def pytest_distribute_execute(wifi_localhost, veh_type, domain,
                                  case_list, ecuinfo: EcuInfo, task: ThreadPoolManager, is_willow, is_flash,
                                  job_info, willow_feishu_config_info, running_env='HIL'):
        database = DatabaseHelper()
        bench = BenchHelper()
        failed_bech_list = []
        retry_times = 0
        if is_willow:
            workspace = Path('/root/autotest/willow/distributed')
        else:
            workspace = Path('/root/distributed')
        # 申请空闲台架
        logger.debug(f"当前运行的环境为{running_env}")
        while True:
            # SIL申请两域台架
            if running_env == 'SIL':
                domain = 'SIL'
            data = database.get_available_bench(
                ipAddr=wifi_localhost,
                excludeIpAddr=failed_bech_list,
                log_print=False,
                lockDirMaster=parent_dir,
                lockDirSlave=str(workspace),
                **{domain: 1}
            )
            time.sleep(5)
            bench_list = data.get('bench_type_list')
            logger.info(f"当前台架池台架类型:{bench_list}")
            if domain not in bench_list:
                logger.error(f"当前台架池:{bench_list}没有{domain}台架，无法执行相关用例")
                return
            bench_infos = data.get('bench_infos')
            if bench_infos:
                if retry_times > RETRY_COUNT:
                    logger.error(f"台架异常，已超过重试次数{RETRY_COUNT}次，任务结束")
                    return
                # 如果申请到台架，部署台架环境
                master_config = BenchConfig(
                    **{
                        'host': data.get('device_id'),
                        'limited_ip': data.get('limited_ip'),
                        'username': data.get('master_username'),
                        'password': data.get('master_password'),
                        'bgm_version': data.get('bgm_version'),
                        'tcam_version': data.get('tcam_version'),
                        'cdc_version': data.get('cdc_version'),
                        'acu_version': data.get('acu_version'),
                        'distribute_task_id': data.get('master_id')
                    }
                )
                # for bech_info in bench_infos:
                slave_config = BenchConfig(
                    **{
                        'host': bench_infos[0].get('deviceId'),
                        'limited_ip': bench_infos[0].get('limitedIp'),
                        'username': bench_infos[0].get('userName'),
                        'password': bench_infos[0].get('password'),
                        'bgm_version': bench_infos[0].get('bgmVersion'),
                        'tcam_version': bench_infos[0].get('tcamVersion'),
                        'cdc_version': bench_infos[0].get('cdcVersion'),
                        'acu_version': bench_infos[0].get('acuVersion'),
                        'distribute_task_id': data.get('master_id')
                    }
                )
                if slave_config.host in failed_bech_list:
                    logger.error(f"当前台架{slave_config.host}环境异常，跳过")
                    continue
                logger.info(f"当前分配任务:{job_info.job_id}, 给{slave_config.host} {domain}台架运行")
                task.add_task(f'{slave_config.host}_env_deploy', bench.submit_bench_status, slave_config,
                              BenchStatus.env_deploy)
                task.add_task(f'heartbeat_{master_config.distribute_task_id}', bench.set_heartbeat_start,
                              wifi_localhost, 'master',
                              HeartBeat.online, master_config.distribute_task_id)
                try:
                    bench.deploy_running_env(master_bench_config=master_config,
                                             slave_bench_config=slave_config,
                                             ecuinfo=ecuinfo,
                                             case_list=case_list,
                                             vehicle_model=veh_type, is_willow=is_willow, workspace=workspace,
                                             is_flash=is_flash, running_env=running_env, service_ip='', service_port='')
                except Exception as e:
                    # 出现异常时将台架状态设置为空闲
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/tasks_helper.py")
                    bench.set_status(slave_config, BenchStatus.idle)
                    # 心跳结束
                    bench.set_heartbeat_status(HeartBeat.offline)
                    # raise e
                    logger.error(f"当前台架{slave_config.host}部署环境异常，错误原因：{e}")
                    failed_bech_list.append(slave_config.host)
                    retry_times += 1
                    continue
                else:
                    bench.set_status(slave_config, BenchStatus.stop)
                # willow_feishu_config_info.distibute_task_id = master_config.distribute_task_id
                # 添加pytest任务到server端
                if running_env == 'SIL':
                    cmd = f'cd {workspace}/sat && ./deploy_SIL_env.sh bgm "cd {workspace}/sat && source venv/bin/activate && {ecuinfo.cmd}"'.replace(
                        ';', ' && ')
                else:
                    cmd = f"cd {workspace}/sat && source venv/bin/activate && {ecuinfo.cmd}".replace(';', ' && ')
                bench.add_running_pytest_task(host=slave_config.host, cmd=cmd,
                                              distribute_task_id=master_config.distribute_task_id, workspace=workspace,
                                              job_info=job_info, willow_feishu_config_info=willow_feishu_config_info)
                # 监控case运行
                retry_times += 1
                while True:
                    data = database.get_test_task(
                        deviceId=slave_config.host,
                        distibuteTaskId=master_config.distribute_task_id,
                        log_print=False
                    )
                    if data:
                        total = data[0].get('totalCaseCount')
                        passed = data[0].get('passCaseCount')
                        error = data[0].get('errorCaseCount')
                        failed = data[0].get('failCaseCount')
                        skipped = data[0].get('skipCaseCount')
                        remained = data[0].get('leftCaseCount')
                        current = data[0].get('currentCase')
                        logger.info(
                            f'台架{slave_config.host}用例进度 total:{total}, pass:{passed}, failed:{failed}, error: {error}, skipped:{skipped}, remained:{remained}, current: {current}'
                        )
                    # 获取任务的状态
                    device_data = database.get_device_test_task_query_status(
                        deviceId=slave_config.host,
                        distibuteTaskId=master_config.distribute_task_id,
                        log_print=False
                    )
                    if device_data:
                        # logger.info(f"{slave_config.host}任务状态#########：{device_data}")
                        if device_data.get('status') == SlaveTaskStatus.finish.value:
                            if data and data[0].get('leftCaseCount', 0) > 0:
                                logger.error(f"{slave_config.host}任务异常中断,错误原因：{device_data.get('errMsg')}")
                                bench.set_heartbeat_status(HeartBeat.offline)
                                time.sleep(6)
                                failed_bech_list.append(slave_config.host)
                                break
                            if device_data.get('errMsg') is None:
                                logger.info(f"{slave_config.host}任务已正常完成")
                                bench.set_heartbeat_status(HeartBeat.offline)
                                time.sleep(6)
                                return
                            else:
                                logger.error(f"{slave_config.host}任务异常中断,错误原因：{device_data.get('errMsg')}")
                                bench.set_heartbeat_status(HeartBeat.offline)
                                time.sleep(6)
                                failed_bech_list.append(slave_config.host)
                                break
                        elif device_data.get('status') == SlaveTaskStatus.unable_run.value:
                            logger.info(f"{slave_config.host}任务无法运行")
                            bench.set_heartbeat_status(HeartBeat.offline)
                            time.sleep(6)
                            failed_bech_list.append(slave_config.host)
                            break
                        elif device_data.get('status') == SlaveTaskStatus.not_start.value:
                            logger.info(f"{slave_config.host}任务未开始运行")
                        elif device_data.get('status') == SlaveTaskStatus.running.value:
                            if not data:
                                logger.info(f"{slave_config.host}任务运行中")
                    time.sleep(5)
            else:
                logger.warning(f"当前没有空闲的{domain}台架，等待1min后继续申请")
                time.sleep(60)

    @staticmethod
    def pytest_distribute_execute_by_socket(
            wifi_localhost=None,
            is_willow=None,
            running_env='HIL',
            ecuinfo: EcuInfo = None,
            job_info=None,
            veh_type=None,
            is_flash=None,
            domain=None,
            service_ip=None,
            service_port=None,
            task: ThreadPoolManager = None
    ):
        database = DatabaseHelper()
        bench = BenchHelper()
        failed_bech_list = []
        retry_times = 0
        if is_willow:
            workspace = Path('/root/autotest/willow/distributed')
        else:
            workspace = Path('/root/distributed')
        # 申请空闲台架
        logger.debug(f"当前运行的环境为{running_env}")
        while True:
            # SIL申请两域台架
            if running_env == 'SIL':
                domain = 'SIL'
            data = database.get_available_bench(
                ipAddr=wifi_localhost,
                log_print=False,
                lockDirMaster=parent_dir,
                lockDirSlave=str(workspace),
                **{domain: 1}
            )
            time.sleep(5)
            bench_list = data.get('bench_type_list')
            logger.info(f"当前台架池台架类型:{bench_list}")
            if domain not in bench_list:
                logger.error(f"当前台架池:{bench_list}没有{domain}台架，无法执行相关用例")
                return
            bench_infos = data.get('bench_infos')
            if bench_infos:
                if retry_times > RETRY_COUNT:
                    logger.error(f"台架异常，已超过重试次数{RETRY_COUNT}次，任务结束")
                    return
                # 如果申请到台架，部署台架环境
                master_config = BenchConfig(
                    **{
                        'host': data.get('device_id'),
                        'limited_ip': data.get('limited_ip'),
                        'username': data.get('master_username'),
                        'password': data.get('master_password'),
                        'bgm_version': data.get('bgm_version'),
                        'tcam_version': data.get('tcam_version'),
                        'cdc_version': data.get('cdc_version'),
                        'acu_version': data.get('acu_version'),
                        'distribute_task_id': data.get('master_id')
                    }
                )
                slave_config = BenchConfig(
                    **{
                        'host': bench_infos[0].get('deviceId'),
                        'limited_ip': bench_infos[0].get('limitedIp'),
                        'username': bench_infos[0].get('userName'),
                        'password': bench_infos[0].get('password'),
                        'bgm_version': bench_infos[0].get('bgmVersion'),
                        'tcam_version': bench_infos[0].get('tcamVersion'),
                        'cdc_version': bench_infos[0].get('cdcVersion'),
                        'acu_version': bench_infos[0].get('acuVersion'),
                        'distribute_task_id': data.get('master_id')
                    }
                )
                if slave_config.host in failed_bech_list:
                    logger.error(f"当前台架{slave_config.host}环境异常，跳过")
                    continue
                logger.info(f"当前分配任务:{job_info.job_id}, 给{slave_config.host} {domain}台架运行")
                task.add_task(f'heartbeat_{master_config.distribute_task_id}', bench.set_heartbeat_start,
                              wifi_localhost, 'master',
                              HeartBeat.online, master_config.distribute_task_id)
                try:
                    client = bench.deploy_running_env(
                        master_bench_config=master_config,
                        slave_bench_config=slave_config,
                        ecuinfo=ecuinfo,
                        case_list=[],
                        vehicle_model=veh_type,
                        is_willow=is_willow,
                        workspace=workspace,
                        is_flash=is_flash,
                        running_env=running_env,
                        service_ip=service_ip,
                        service_port=service_port,
                    )
                except Exception as e:
                    logger.exception(f"当前台架{slave_config.host}部署环境异常，错误原因：{e}")
                    failed_bech_list.append(slave_config.host)
                    retry_times += 1
                    continue
                else:
                    logger.info("部署环境成功")
                    # 添加pytest任务到server端
                    dist_id = uuid.uuid4()  # 分布式任务id
                    host_ip = slave_config.limited_ip if slave_config.limited_ip else slave_config.host
                    if running_env == 'SIL':
                        cmd = f'cd {workspace}/sat && ./deploy_SIL_env.sh bgm "cd {workspace}/sat && source venv/bin/activate && {ecuinfo.cmd}"'.replace(
                            ';', ' && ')
                    else:
                        raw_cmd = ecuinfo.cmd.replace(';', ' && ').replace('pytest',
                                                                           f'rm -f nohup.out && mkdir -p logs && nohup pytest --dist_id={dist_id}')
                        cmd = f"cd {workspace}/sat && source venv/bin/activate && {raw_cmd} > logs/slave_{dist_id}_{host_ip}.log 2>&1 &"
                    bench.running_pytest_task_by_ssh(
                        client=client,
                        cmd=cmd,
                        timeout=5
                    )
                    while True:
                        grep_pytest_cmd = f'ps -ef | grep dist_id={dist_id} | grep -v grep' + "| awk '{print $2}'"
                        status, ret = client.execute(grep_pytest_cmd, is_reconnected=True)
                        pytest_process = ret.split('\r\n')[1:-1]
                        if pytest_process:
                            if "[1]+  " in pytest_process[0]:
                                if "[1]+  Exit 1" in pytest_process[0]:
                                    logger.info(f"{host_ip}任务运行完成, 返回值为1")
                                elif "[1]+  Done" in pytest_process[0]:
                                    logger.info(f"{host_ip}任务运行完成, 返回值为0")
                                bench.set_heartbeat_status(HeartBeat.offline)
                                break
                            # 如果是数字
                            elif pytest_process[0].isdigit():
                                logger.debug(f"{host_ip}任务运行中，进程号为{pytest_process[0]}")
                            else:
                                logger.info(f"{host_ip}任务运行失败或者被killed，返回值为{pytest_process[0]}")
                        else:
                            bench.set_heartbeat_status(HeartBeat.offline)
                            break
                        time.sleep(5)
                    bench.set_heartbeat_status(HeartBeat.offline)
                    break
            else:
                logger.warning(f"当前没有空闲的{domain}台架，等待1min后继续申请")
                time.sleep(60)

    @staticmethod
    def record_top():
        script_path = os.path.join(AUTOMOTIVE_ROOT, 'scripts', 'record_top.sh')
        exec_shell(f'{script_path}')


class JobInfo:
    """
    任务信息：描述通过分布式执行的任务的基础信息
    """

    def __init__(self):
        self.job_name = ""
        self.job_id = ""
        self.plan_total_case_num = 0
        self.testplan_id = None
