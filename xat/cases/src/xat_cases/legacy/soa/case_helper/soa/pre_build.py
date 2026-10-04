#!/usr/bin/python3
# coding=UTF-8

import os
import sys
import time

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_ecu.legacy.common.logger import logger  as logging
from xat_cases.legacy.soa.case_helper.soa.bootes_log_handler import first_rm
from xat_cases.legacy.soa.case_helper.soa.domain.acu import check_acu_network, get_acu_version, pull_acu_log, rm_acu_log
from xat_cases.legacy.soa.case_helper.soa.domain.bgm import check_bgm_network, pre_bgm, get_bgm_version, pull_log, rm_bgm_log, first_ssh_bgm
from xat_cases.legacy.soa.case_helper.soa.domain.cdca import check_cdca_network, pre_cdca, get_cdca_version, pull_cdca_log, rm_cdca_log
from xat_cases.legacy.soa.case_helper.soa.domain.cdcq import check_cdcq_network, pre_cdcq, pull_cdcq_log, rm_cdcq_log
from xat_cases.legacy.soa.case_helper.soa.domain.tcam import check_tcam_network, get_tcam_version, pull_tcam_log, rm_tcam_log, pre_tcam,reset_tcam_env
from xat_cases.legacy.soa.case_helper.soa.check_doc import *
from xat_cases.legacy.soa.case_helper.codesrc.components.pressure.pre_env_ioe import IoE_start
from xat_cases.legacy.soa.case_helper.soa.pressure_sleep_awake import PressureAwake
from xat_cases.legacy.soa.case_helper.soa.pressure_context import PressureContext
from xat_cases.legacy.soa.case_helper.codesrc.public.utils.disk_manager import DiskCleaner
from xat_cases.legacy.soa.case_helper.codesrc.components.pressure.utils import *

script_path = get_script_path()
config = get_config_info()



def create_dir(path, times, host_ip, bgm_version):
    '''
    创建日志主目录
    '''
    times = int(times) - 1
    now_time = time.strftime('%Y%m%d-%H%M%S', time.localtime())
    now_time = now_time[2:]
    file_name = f"{now_time}-{times}-{bgm_version}-{host_ip}"
    file_path = f"{path}/{file_name}"
    if os.path.exists(file_path) is False:
        os.makedirs(file_path)
    return file_path, file_name


def run_log(path):
    """
    程序运行日志输出
    """
    logger = logging.getLogger()
    logger.setLevel(level=logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    log_path = os.path.join(path, 'Run.log')
    logging.info(f'日志输出路径====={log_path}')
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(level=logging.DEBUG)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def process_pcap():
    """
        发包函数
        1、根据跳板机的网卡执行相应的播包命令
    """
    logging.info('开始发包')
    pcap_path = os.path.join(script_path, 'conf', '1.1Udp_unvlan_revise_mac_revise_ip.pcap')
    #os.system(f"ip a | grep -2 'inet 169.254.1.200' | head -n 1 | awk '{{logging.info $2}}' | sed 's/:$//'  |xargs -I {{}} sudo tcpreplay -i {{}} -l 10000 {pcap_path} &")
    pcap = PcapManager(pcap_path, config['relay_ip'])
    pcap.send(config['pcap_length'])


def stop_replay():
    '''
    结束发包
    '''
    # cmd = "ps -ef|grep tcpreplay|grep -v grep|awk '{logging.info $2}'|xargs kill -9"
    # os.system(cmd)
    logging.info('结束发包')


def pre_process(bgm_uname, bgm_addr, bgm_pwd, cdca_addr, config, tc_config, ipdu, nucapp):
    first_rm(bgm_uname, bgm_addr, bgm_pwd, cdca_addr, config['tcam_pwd'], config['acu_name'], config['acu_pwd'], tc_config, ipdu, nucapp)
    logging.info('有上下电需要重新获取bgm的ip')


def post_process():
    stop_replay()

    
def init_disk():
    """
    初始化磁盘检测，低于10G清除之前的文件
    """
    pressure_log_path = f"{os.path.join(os.path.abspath(os.path.join(script_path, '../../../../..')), 'pressure_log')}"
    disk_cleaner = DiskCleaner(pressure_log_path, config['threshold_gb'])
    disk_cleaner.clean_if_needed()


def init_pre(nucapp=None):
    """
    初始化环境准备
    """
    logging.info("刷机后进行一次bgm上下电；暂时避免车辆公告发不出来问题")
    hand_usbrelay_off("bgm",nucapp)
    time.sleep(1)
    hand_usbrelay_on("bgm",nucapp)
    time.sleep(20)
    bgm_addr = get_obd_ip()
    logging.info(f'BGM_ADDR====={bgm_addr}')
    cdca_addr = f"{bgm_addr}:1313"
    bgm_uname = config['bgm_uname']
    bgm_pwd = config['bgm_pwd']
    IoE_start(bgm_addr, bgm_uname, bgm_pwd, force_flag=True)
    pre_bgm(bgm_uname, bgm_addr, bgm_pwd)
    pre_cdcq(bgm_addr)
    pre_cdca(bgm_addr, cdca_addr, bgm_uname, bgm_pwd,nucapp)
    pre_tcam(bgm_addr, config['tcam_pwd'])
    logging.info('<pre_env>  Finish')

def reset_env():
    bgm_addr = get_obd_ip()
    logging.info(f'BGM_ADDR====={bgm_addr}')
    cdca_addr = f"{bgm_addr}:1313"
    bgm_uname = config['bgm_uname']
    bgm_pwd = config['bgm_pwd']
    IoE_start(bgm_addr, bgm_uname, bgm_pwd, force_flag=True)
    #恢复环境
    reset_tcam_env(bgm_addr, config['tcam_pwd'])
    logging.info('<reset_env>  Finish')

    

def start_pre(data=None,nucapp=None,tc_config=None, ipdu=None, sd=False):
    bgm_addr = get_obd_ip()
    logging.info(f'BGM_ADDR====={bgm_addr}')
    if data:
        config['strategy']=data
    cdca_addr = f"{bgm_addr}:1313"
    bgm_uname = config['bgm_uname']
    bgm_pwd = config['bgm_pwd']
    logging.info("第一次连接bgm")
    IoE_start(bgm_addr, bgm_uname, bgm_pwd, force_flag=True)

    bgm_version = get_bgm_version(bgm_uname, bgm_addr, bgm_pwd)
    cdca_version = get_cdca_version(cdca_addr)
    tcam_version = get_tcam_version(bgm_addr, config['tcam_pwd'])
    acu_version = get_acu_version(bgm_addr, config['acu_name'], config['acu_pwd'])
    pressure_log_path = f"{os.path.join(os.path.abspath(os.path.join(script_path, '../../../../..')), 'pressure_log')}"
    file_path, file_name = create_dir(pressure_log_path, config['times'], get_host_ip(), bgm_version)
    logging.info(f'==============={file_path}======{file_name}============================')

    logging.info('=======================压测开始==========================')
    logging.info(f'bgm_version=========={bgm_version}')
    logging.info(f'cdc_version=========={cdca_version}')
    logging.info(f'tcam_version=========={tcam_version}')
    logging.info(f'acu_version=========={acu_version}')
    logging.info(f'配置信息：{config}')
    import multiprocessing
    process1 = multiprocessing.Process(target=process_pcap)
    process1.daemon = True
    process1.start()
    
    pre_process(bgm_uname, bgm_addr, bgm_pwd, cdca_addr, config, tc_config, ipdu, nucapp)
    bgm_addr = get_obd_ip()
    logging.info(f'BGM_ADDR====={bgm_addr}')
    cdca_addr = f"{bgm_addr}:1313"
    IoE_start(bgm_addr, bgm_uname, bgm_pwd, force_flag=True)
    pressure = PressureContext(config, bgm_addr, cdca_addr, script_path, file_path, file_name,
                               bgm_version, cdca_version, tcam_version, acu_version, tc_config, nucapp)
    pressure.run(ipdu, sd)
    post_process()
    logging.info('=======================压测结束==========================')
    
    # 解析数据
    logging.info("校验是否有coredump:")
    ret,msg=read_doc(file_path)
    logging.info(msg)
    logging.info("校验进程连接目标服务的时间:")
    flag,event = check_timeout_process(file_path)
    logging.info(event)
    return all([ret, flag]),f"最大超时时间为: {event}, 异常错误: {msg}"


def start_awake(data=None, tc_config=None, ipdu=None, nucapp=None):
    bgm_addr = get_obd_ip()
    logging.info(f'BGM_ADDR====={bgm_addr}')
    if data:
        config['strategy']=data
    cdca_addr = f"{bgm_addr}:1313"
    bgm_uname = config['bgm_uname']
    bgm_pwd = config['bgm_pwd']
    IoE_start(bgm_addr, bgm_uname, bgm_pwd, force_flag=True)
    bgm_version = get_bgm_version(bgm_uname, bgm_addr, bgm_pwd)
    cdca_version = get_cdca_version(cdca_addr)
    tcam_version = get_tcam_version(bgm_addr, config['tcam_pwd'])
    acu_version = get_acu_version(bgm_addr, config['acu_name'], config['acu_pwd'])
    pressure_log_path = f"{os.path.join(os.path.abspath(os.path.join(script_path, '../../../../..')), 'pressure_log')}"
    file_path, file_name = create_dir(pressure_log_path, config['times'], get_host_ip(), bgm_version)
    
    logging.info(f'==============={file_path}======{file_name}============================')
    logging.info('=======================压测开始==========================')
    logging.info(f'bgm_version=========={bgm_version}')
    logging.info(f'cdc_version=========={cdca_version}')
    logging.info(f'tcam_version=========={tcam_version}')
    logging.info(f'acu_version=========={acu_version}')
    logging.info(f'配置信息：{config}')
    import multiprocessing
    process1 = multiprocessing.Process(target=process_pcap)
    process1.daemon = True
    process1.start()
    
    pre_process(bgm_uname, bgm_addr, bgm_pwd, cdca_addr, config, tc_config, ipdu, nucapp)
    bgm_addr = get_obd_ip()
    cdca_addr = f"{bgm_addr}:1313"
    pressure = PressureAwake(config, bgm_addr, cdca_addr, script_path, file_path, file_name,
                               bgm_version, cdca_version, tcam_version, acu_version, tc_config=tc_config, ipdu=ipdu, nucapp=nucapp)
    pressure.run()
    post_process()
    logging.info('=======================压测结束==========================')
    
    # 解析数据
    logging.info("校验是否有coredump:")
    ret,msg=read_doc(file_path)
    logging.info(msg)
    logging.info("校验进程连接目标服务的时间:")
    flag,event = check_timeout_process(file_path)
    logging.info(event)
    logging.info("休眠唤醒场景需要校验Method/Event事件调用:")
    state,str=chech_event(file_path)
    logging.info(f"Method/Event事件调用次数{str}")
    return all([ret, flag]),f"最大超时时间为: {event}\n 异常错误: {msg}\n 校验Method/Event事件调用{str}"


def before(data, tc_config, ipdu, nucapp):
    bgm_addr = get_obd_ip()
    logging.info(f'BGM_ADDR====={bgm_addr}')
    if data:
        config['strategy']=data
    cdca_addr = f"{bgm_addr}:1313"
    bgm_uname = config['bgm_uname']
    bgm_pwd = config['bgm_pwd']
    IoE_start(bgm_addr, bgm_uname, bgm_pwd, force_flag=True)
    bgm_version = get_bgm_version(bgm_uname, bgm_addr, bgm_pwd)
    cdca_version = get_cdca_version(cdca_addr)
    tcam_version = get_tcam_version(bgm_addr, config['tcam_pwd'])
    acu_version = get_acu_version(bgm_addr, config['acu_name'], config['acu_pwd'])
    pressure_log_path = f"{os.path.join(os.path.abspath(os.path.join(script_path, '../../../../..')), 'pressure_log')}"
    file_path, file_name = create_dir(pressure_log_path, config['times'], get_host_ip(), bgm_version)
    logging.info(f'==============={file_path}======{file_name}============================')
    logging.info('=======================压测开始==========================')
    logging.info(f'bgm_version=========={bgm_version}')
    logging.info(f'cdc_version=========={cdca_version}')
    logging.info(f'tcam_version=========={tcam_version}')
    logging.info(f'acu_version=========={acu_version}')
    logging.info(f'配置信息：{config}')
    import multiprocessing
    process1 = multiprocessing.Process(target=process_pcap)
    process1.daemon = True
    process1.start()
    
    pre_process(bgm_uname, bgm_addr, bgm_pwd, cdca_addr, config, tc_config, ipdu, nucapp)
    bgm_addr = get_obd_ip()
    cdca_addr = f"{bgm_addr}:1313"
    IoE_start(bgm_addr, bgm_uname, bgm_pwd, force_flag=True)

    return config, bgm_addr, cdca_addr, file_path, file_name, bgm_version, cdca_version, tcam_version, acu_version

def after(nucapp, tc_config, config, bgm_addr, cdca_addr, file_path, file_name, bgm_version, cdca_version, tcam_version, acu_version):
    import multiprocessing
    process1 = multiprocessing.Process(target=process_pcap)
    process1.daemon = True
    process1.start()
    pressure = PressureContext(config, bgm_addr, cdca_addr, script_path, file_path, file_name,
                            bgm_version, cdca_version, tcam_version, acu_version, tc_config, nucapp)
    pressure.run()
    post_process()
    logging.info('=======================压测结束==========================')
    
    # 解析数据
    ret,msg=read_doc(file_path)
    logging.info("校验进程连接目标服务的时间:")
    flag,event = check_timeout_process(file_path)
    logging.info(event)
    return all([ret, flag]),f"最大超时时间为: {event}, 异常错误: {msg}"
