# -*- coding: utf-8 -*-
"""
@File        : cdc_flash.py
@Author      : lei.hong@jiduauto.com
@Time        : 2024/06/12 15:00
@Description : 
@Examples    :
"""
import time
import json
import os
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.common.logger import Logger
from xat_ecu.legacy.driver.ssh_interface import ScpClient, SshClient

logger = Logger().get_logger("test")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_uds_data(data):
    if data:
        # data = data_list[0].split(' ')
        if data[0:3] == ['62', 'F1', 'AE']:
            left = data[4:9]
            mid = data[9]
            right = data[10:12]
            if mid == '20':
                return f"{''.join(left)}{chr(int(right[0], 16))}{chr(int(right[1], 16))}"
            else:
                return f"{''.join(left)}{chr(int(mid, 16))}{chr(int(right[0], 16))}{chr(int(right[1], 16))}"

def get_cdc_version():
    config = {
            "dut_ecu": ["CDC"],
            "gateway_ip": "172.16.9.11",
            "sd_tester_cfg": {
                "diag_mode": "doip",
                "is_via_gateway": False,
                "ecu_name": "CDC",
                "dig_bus": "bodycan",
                "server_ip": "172.16.9.11",
            },
            "veh_type": 'mars1',
            "bl_ver": 'v_2_2_0',
            "bus": {}
            }
    try:
        sd_test = Sd_Tester(**config)
        time.sleep(0.5)
        sd_test.diagnostic_client_sim_start()
        time.sleep(0.5)
        sd_test.send_data([0x22, 0xF1, 0xAE])
        data_dict = sd_test.return_udsdata_and_check_and_print_response_result()
        logger.info(f"返回值{data_dict}")
        new_data_dict = []
        for i in data_dict:
            hexadecimal_number_with_prefix = hex(i)  # 转换为16进制，带有"0x"前缀
            hexadecimal_number = hexadecimal_number_with_prefix[2:].zfill(2)
            new_data_dict.append(hexadecimal_number.upper())
        version = get_uds_data(new_data_dict)
        logger.info(f"CDC版本为：{version}")
        return version
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/cdc_flash/cdc_flash.py")
        logger.error(f"获取CDC版本失败: {e}")
        return None
    finally:
        sd_test.stop_tester_present()
        sd_test.diagnostic_client_sim_close()
def get_version_by_url(img_url):
    '''
    根据url 获取版本名称
    @param img_url:
    @return:
    '''
    if isinstance(img_url, str):
        try:
            version = img_url.split('/')[-1].split('.')[0]
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/cdc_flash/cdc_flash.py")
            logger.error(f"根据 url 路径获取版本号失败：{str(e)}")
            version = None
    else:
        version = None
    # '6110110220AE'
    # '613011220AE'
    # '6130110300QF'
    # '6130110220AE'
    # https://repo.jidudev.com/artifactory/CDC/Release/6130110220AE
    return version
def get_willow_task_json(key):
    path = os.path.join(BASE_DIR, "../", "report", "report_summary.json")
    with open(path, 'r') as f:
        data = json.load(f)
    try:
        logger.info(f"task.json {key}的数据为:{data[key]}")
        return str(data[key])
    except KeyError as e:
        logger.error(f"task.json {key}的数据为不存在")
        raise Exception(e)

def cdc_flash(img_url=None, keyinfo=None):
    config = {
            "dut_ecu": ["CDC"],
            "gateway_ip": "172.16.9.11",
            "sd_tester_cfg": {
                "diag_mode": "doip",
                "is_via_gateway": False,
                "ecu_name": "CDC",
                "dig_bus": "bodycan",
                "server_ip": "172.16.9.11",
            },
            "veh_type": 'mars1',
            "bl_ver": 'v_2_2_0',
            "bus": {}
            }
    sd_test = Sd_Tester(**config)
    time.sleep(0.5)
    sd_test.diagnostic_client_sim_start()
    time.sleep(0.5)
    try:
        sd_test.upgrade_ecu_cdc(keyinfo, img_url)
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/cdc_flash/cdc_flash.py")
        logger.error(f"升级失败: {e}")
        assert False, f"升级失败: {e}"
    finally:
        sd_test.stop_tester_present()
        sd_test.diagnostic_client_sim_close()
def replace_profile():
    logger.info("开始替换配置文件")
    client = SshClient(host='172.16.9.11', port=22, username='root', password=__import__("os").environ.get('XAT_CREDENTIAL____CDC_FLASH_CDC_FLASH_PY_PASSWORD', ""))
    client.execute('mount -uw /mnt', is_reconnect=False, log_print=True, print_raw_data=True)
    time.sleep(2)
    scp = ScpClient(host='172.16.9.11', port=22, username='root', password=__import__("os").environ.get('XAT_CREDENTIAL____CDC_FLASH_CDC_FLASH_PY_PASSWORD', ""))
    scp.put(local_path=f"{BASE_DIR}/tools/cdc_flash/cdc_calibration_default_config.json", remote_path='/mnt/etc/cdc_calibrationservice/')
    client.execute('power_ctrl -k Reboot', is_reconnect=False, log_print=True, print_raw_data=True)
    time.sleep(180)
    client.execute('power_ctrl -k Reboot', is_reconnect=False, log_print=True, print_raw_data=True)
    time.sleep(180)
    
    
def main():
    img_url = get_willow_task_json('img_url')
    keyinfo = get_willow_task_json('keyinfo')
    t_version = get_version_by_url(img_url)
    c_version = get_cdc_version()
    if t_version != c_version:
        cdc_flash(img_url, keyinfo)
        # time.sleep(180)
        c_version = get_cdc_version()
        if t_version != c_version:
            logger.error(f"升级失败,当前版本为{c_version},目标版本为{t_version}")
            assert False, f"升级失败,当前版本为{c_version},目标版本为{t_version}"
        else:
            logger.info(f"升级成功,当前版本为{c_version},目标版本为{t_version}")
            replace_profile()
    else:
        logger.info(f"CDC版本与任务中配置一致，不需要升级,current_version:{c_version},target_version:{t_version}")



if __name__ == '__main__':
    main()
    # get_cdc_version()