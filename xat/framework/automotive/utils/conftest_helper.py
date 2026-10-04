# -*- coding: utf-8 -*-
"""
@File        : conftest_helper.py
@Author      : quan.sun@jiduauto.com
@Time        : 2022-11-01 10:30
@Description : 

"""
import json
import subprocess
import threading
import time

from xat_ecu.legacy.interface.nuc_app import exec_shell
from framework.automotive.utils.data_type import VehicleModel
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.common.file_handle import parent_dir as ecu_parent_dir
from pathlib import Path
from framework.automotive.core.resources import XAT_ROOT, AUTOMOTIVE_ROOT, LOCK_SCRIPT, workspace_relative

from xat_ecu.api.call_tracker import ObjExecutor
from xat_ecu.api.interfaces.dp1.sdtest import SdTest

current_path = os.path.dirname(os.path.realpath(__file__))
parent_dir = str(XAT_ROOT)
statics_dir = Path(__file__).resolve().parents[1] / "statics"
soa_partner_path = Path(ecu_parent_dir) / "soa_partner"


def mkdir_folder(log_path="/root/test_case_log"):
    if os.path.exists(log_path):
        res = os.system(f'rm -rf {log_path}/*')
        if res != 0:
            logger.error(f"delete log failed,res:{res}")
    else:
        os.mkdir(log_path)


def convert_version_format(version_name):
    count = 0
    version_name_new = ""
    for x in version_name:
        if x.isnumeric():
            if count < 2:
                version_name_new = version_name_new + x + "."
                count = count + 1
            else:
                version_name_new = version_name_new + x
        else:
            version_name_new = version_name_new + x
    else:
        return version_name_new


def email_str_to_list(email_str: str):
    if email_str and isinstance(email_str, str):
        email_str = email_str.strip()
        email_str_list = email_str.split(";")

        # 去除空格
        email_list = []
        for i in email_str_list:
            email_list.append(i.strip())

        return email_list


def get_bgm_diag_info(**cfg):
    bgm_mcu_version = None
    bgm_boot_version = None
    bgm_switch_version = None
    hardware_version = None
    veh_type = None
    battery_type = None
    cfg = {"dut_ecu": ["BGM"],
           "gateway_ip": "169.254.19.1",
           "veh_type": 'mars1',
           "veh_gen": 'G1.1',
           "bl_ver": 'v_1_4_0',
           "bus":
               {"eth_obd": "",
                "eth_vlan5": "eth0.5",
                "eth_vlan9": "eth0.9",
                "bodycan": 'can0'},
           "sd_tester_cfg":
               {"diag_mode": "doip",
                "is_via_gateway": True,
                "ecu_name": "BGM",
                "dig_bus": "diagnosticcan",
                "server_ip": "169.254.19.1"}
           }
    sd_tester = SdTest(**cfg)
    try:
        bgm_mcu_version = sd_tester.read_bgm_mcu_version()
        bgm_boot_version = sd_tester.read_bgm_boot_version()
        hardware_version = sd_tester.sd_tester.get_hard_version()
        raw_ccp = sd_tester.sd_tester.read_ccp()
        bgm_switch_version = sd_tester.read_bgm_switch_version()
        ccp_data = raw_ccp[1]
        logger.info(f"veh_type ccp data:{ccp_data[949]}")
        logger.info(f"battery_type ccp data:{ccp_data[961]}")
        if ccp_data[949] == 1:
            veh_type = 'mars1'
            logger.info('当前车型为mars1')
        elif ccp_data[949] == 2:
            veh_type = 'venus'
            logger.info('当前车型为venus')
        if ccp_data[961] == 0:
            logger.info('当前是400V平台')
        elif ccp_data[961] == 2:
            battery_type = 'mca'
            logger.info('当前是800V平台')
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/conftest_helper.py")
        logger.error(f"获取bgm诊断信息失败, ERROR: {str(e)}")
    finally:
        with ObjExecutor() as obj:
            for obj_name in obj.start_cache:
                if obj_name == 'SdTest':
                    logger.info("停止sd_tester, 避免对下干扰")
                    sd_tester.stop_sd_tester()
    bgm_diag_info = {
        "bgm_mcu_version": bgm_mcu_version,
        "bgm_boot_version": bgm_boot_version,
        "bgm_switch_version": bgm_switch_version,
        "hardware_version": hardware_version,
        "veh_type": veh_type,
        "battery_type": battery_type
    }
    logger.info(f"获取到bgm 诊断信息 {bgm_diag_info}")
    return bgm_diag_info


def get_tcam_diag_info(**cfg):
    hardware_version = None
    sd_tester = SdTest(**cfg)
    sd_tester.update_serverdoipid(doipid=0x1011, ecu='TCAM')
    try:
        hardware_version = sd_tester.sd_tester.get_hard_version()
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/conftest_helper.py")
        logger.error(f"获取tcam诊断信息失败, ERROR: {str(e)}")
    finally:
        with ObjExecutor() as obj:
            for obj_name in obj.start_cache:
                if obj_name == 'SdTest':
                    logger.info("停止sd_tester, 避免对下干扰")
                    sd_tester.stop_sd_tester()
    tcam_diag_info = {
        "hardware_version": hardware_version
    }
    logger.info(f"获取到bgm 诊断信息 {tcam_diag_info}")
    return tcam_diag_info


def get_cdc_diag_info(**cfg):
    hardware_version = None
    sd_tester = SdTest(**cfg)
    sd_tester.update_serverdoipid(doipid=0x1201, ecu='CDC')
    try:
        hardware_version = sd_tester.sd_tester.get_hard_version()
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/conftest_helper.py")
        logger.error(f"获取acu诊断信息失败, ERROR: {str(e)}")
    finally:
        with ObjExecutor() as obj:
            for obj_name in obj.start_cache:
                if obj_name == 'SdTest':
                    logger.info("停止sd_tester, 避免对下干扰")
                    sd_tester.stop_sd_tester()
    cdc_diag_info = {
        "hardware_version": hardware_version,
    }
    logger.info(f"获取到cdc 诊断信息 {cdc_diag_info}")
    return cdc_diag_info


def get_acu_diag_info(**cfg):
    hardware_version = None
    sd_tester = SdTest(**cfg)
    sd_tester.update_serverdoipid(doipid=0x1401, ecu='BGM')
    try:
        hardware_version = sd_tester.sd_tester.get_hard_version()
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/conftest_helper.py")
        logger.error(f"获取acu诊断信息失败, ERROR: {str(e)}")
    finally:
        with ObjExecutor() as obj:
            for obj_name in obj.start_cache:
                if obj_name == 'SdTest':
                    logger.info("停止sd_tester, 避免对下干扰")
                    sd_tester.stop_sd_tester()
    acu_diag_info = {
        "hardware_version": hardware_version,
    }
    logger.info(f"获取到acu 诊断信息 {acu_diag_info}")
    return acu_diag_info


def change_bgm_vehicle_model(vehicle_model: VehicleModel, **cfg):
    if vehicle_model == VehicleModel.MarsOne.value:
        ccp_dict = {950: 1, 962: 0}
    elif vehicle_model == VehicleModel.MarsOneMCA.value:
        ccp_dict = {950: 1, 962: 2}
    elif vehicle_model == VehicleModel.MarsOneICA.value:
        ccp_dict = {950: 1, 962: 0}
    elif vehicle_model == VehicleModel.Venus.value:
        ccp_dict = {950: 2, 962: 0}
    elif vehicle_model == VehicleModel.Venus_800V.value:
        ccp_dict = {950: 2, 962: 2}
    else:
        return
    if os.path.exists('tmp_config.json'):
        with open('tmp_config.json', 'r') as f:
            config = json.load(f)
        if config == ccp_dict:
            logger.info("车型和平台配置与预期一致")
            return
    sd_tester = SdTest(**cfg)
    try:
        raw_ccp = sd_tester.read_ccp()
        ccp_data = raw_ccp[1]
        if ccp_data[950 - 1] == ccp_dict[950] and ccp_data[962 - 1] == ccp_dict[962]:
            logger.info("当前车型和平台已经是所需的车型和平台")
            with open('tmp_config.json', 'w') as f:
                json.dump(ccp_dict, f)
            return
        else:
            sd_tester.write_multi_ccp(ccp_dict)
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/conftest_helper.py")
        logger.error(f"获取ccp失败, ERROR: {str(e)}")
    else:
        sd_tester.reboot_bgm_by_diag_hardreset()
        with open('tmp_config.json', 'w') as f:
            json.dump(ccp_dict, f)
    finally:
        with ObjExecutor() as obj:
            for obj_name in obj.start_cache:
                if obj_name == 'SdTest':
                    logger.info("停止sd_tester, 避免对下干扰")
                    sd_tester.stop_sd_tester()


def change_veh_type(vehicle_model: VehicleModel):
    veh_type = ''
    if vehicle_model == VehicleModel.MarsOne.value:
        veh_type = 'mars1'
    elif vehicle_model == VehicleModel.MarsOneMCA.value:
        veh_type = 'mars1'
    elif vehicle_model == VehicleModel.MarsOneICA.value:
        veh_type = 'mars1'
    elif vehicle_model == VehicleModel.Venus.value:
        veh_type = 'venus'
    elif vehicle_model == VehicleModel.Venus_800V.value:
        veh_type = 'venus'
    return veh_type


def change_bl_ver(vehicle_model: VehicleModel):
    bl_ver = ''
    if vehicle_model == VehicleModel.MarsOne.value:
        bl_ver = ''
    elif vehicle_model == VehicleModel.MarsOneMCA.value:
        bl_ver = '_mca'
    elif vehicle_model == VehicleModel.MarsOneICA.value:
        bl_ver = ''
    elif vehicle_model == VehicleModel.Venus.value:
        bl_ver = ''
    elif vehicle_model == VehicleModel.Venus_800V.value:
        bl_ver = '_mca'
    return bl_ver


def kill_process(name):
    """
    检查上位机上是否有其它未关闭的进程在运行，如果有，则重载进程
    """
    check_cmd = f"ps -ef | grep {name} | grep -v grep"
    pi = subprocess.Popen(
        check_cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding='utf-8',
    )
    stdout = pi.stdout.read()
    if stdout:
        logger.info(f"结束{name}进程")
        logger.debug("命令执行结果：\n{}".format(stdout))
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
            stdout = pi.stdout.read()
            if stdout:
                logger.info("error: {}".format(stdout))
                logger.info("process kill fail")
                time.sleep(1)
                return False
            else:
                logger.info(f"{name} process kill success")
                time.sleep(1)
                return True


def check_process(name):
    """
    检查上位机上是否正常运行
    """
    check_cmd = f"ps -ef | grep {name} | grep -v grep"
    pi = subprocess.Popen(
        check_cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding='utf-8',
    )
    stdout = pi.stdout.read()
    if stdout:
        logger.info(f"{name}进程存在")
        return True
    else:
        logger.error(f"未检查到{name}进程")
        return False


def record_top():
    """
    pytest执行期间监控top命令，并将监控结果记录到文件中
    """
    script_path = os.path.join(AUTOMOTIVE_ROOT, 'scripts', 'record_top.sh')
    exec_shell(f'chmod 777 {script_path};{script_path}')


def record_vmstat():
    """
    pytest执行期间监控vmstat命令，并将监控结果记录到文件中
    """
    script_path = os.path.join(AUTOMOTIVE_ROOT, 'scripts', 'record_vm_stat.sh')
    exec_shell(f'chmod 777 {script_path};{script_path}')


def bench_resource_collect_thread():
    threads = [
        threading.Thread(target=record_top, name='record_top'),
        threading.Thread(target=record_vmstat, name='record_vmstat'),
    ]
    for t in threads:
        t.setDaemon(True)
        t.start()


def check_process_thread(name):
    t = threading.Thread(target=check_process, args=(name,), name='check_process')
    t.setDaemon(True)
    t.start()


def record_top_thread():
    t = threading.Thread(target=record_top, name='record_top')
    t.setDaemon(True)
    t.start()


def timestamp_to_datetime_full_millis(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp)
    formatted_dt = dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    return formatted_dt
