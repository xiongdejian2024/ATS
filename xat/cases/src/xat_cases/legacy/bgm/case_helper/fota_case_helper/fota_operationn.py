'''
Author: liu.yang
Date: 2023-02-01 19:05:06
LastEditors: Do not edit
LastEditTime: 2023-07-27 18:44:34
FilePath: /yangliu/sat/xat_cases/legacy/bgm/case_helper/fota_case_helper/fota_operationn.py
'''
import os
import sys

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

work_path_2 = os.path.join(os.getcwd().split("sat")[0], 'sat', 'ecu_simulator', 'interface')
sys.path.append(work_path_2)



from xat_cases.legacy.bgm.case_helper.test_base import TestBase
 
from xat_cases.legacy.bgm.NetworkChannel.test_networkChannel import con_bgm

from xat_ecu.legacy.sdk.bus_app import BusApp
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.logger import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_cases.legacy.bgm.case_helper.diag_case_helper.DiagTestBase import *
current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path, ".."))
sys.path.append(os.path.join(current_path, "../.."))
sys.path.append(os.path.join(current_path, "../../../.."))

from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.case_helper.diag_case_helper.DiagTestBase import *
from xat_ecu.legacy.common.logger import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.interface.tcam.tcam_ssh import *
from xat_cases.legacy.bgm.case_helper.fota_case_helper.fota_constant import *
from xat_ecu.legacy.driver.ssh_interface import *
from func_timeout import func_set_timeout

def clear_bgm_env():
    # 清bgm环境
    logger.info("======================= clear bgm env =======================")
    command_send(device_name='BGM', cmd='''rm -rf /log/*;rm /update/state-backup.pb;rm /update/state.pb;rm /update/update_agent_persist.json;sync;ps -ef|grep -E "ua|install|fota|obt|arb|jetlog"|grep app|awk -F " " '{print $2}'|xargs kill -9;sync
''')
    time.sleep(1.5)
    
def reset_fota_env():
    # 清fota环境
    logger.info("======================= clear fota env =======================")
    command_send(device_name='BGM', cmd='''rm /update/state-backup.pb;rm /update/state.pb;rm /update/update_agent_persist.json;sync;ps -ef|grep -E "ua|install|fota|obt|arb|jetlog"|grep app|awk -F " " '{print $2}'|xargs kill -9;sync
''')
    time.sleep(20)
    
def clear_fota_cache():
    logger.info("======================= clear fota cache =======================")
    command_send(device_name='BGM', cmd='''rm /update/state-backup.pb;rm /update/state.pb;rm /update/update_agent_persist.json
''')
    time.sleep(1.5)
    
    
def reset_sh():
    # 偷懒清环境方式，正式压测环境禁止使用
    BGM_SSH().type_commands("/update/reset.sh")
    time.sleep(10)

def clear_tcam_log():
    # 清tcam log
    TCAM_SSH().type_commands("rm -rf /mnt/sdcard/log/*")
    logger.info("======================= clear tcam log =======================")

def refresh_version_debug(task_id, BGM_HWPN, TCAM_HWPN):
    if BGM_HWPN and TCAM_HWPN:
        logger.info("========================================================")
        logger.info("Current domain controller: BGM && TCAM")
        logger.info("========================================================")
        BGM_SSH().type_commands(f'echo -n "{VERSION_DEBUG_1}" > /update/version_debug.json')
        time.sleep(0.2)
        BGM_SSH().type_commands(f'echo -n "{BGM_HWPN}" >> /update/version_debug.json')
        time.sleep(0.2)
        BGM_SSH().type_commands(f'echo -n "{VERSION_DEBUG_2}" >> /update/version_debug.json')
        time.sleep(0.2)
        BGM_SSH().type_commands(f'echo -n "{TCAM_HWPN}" >> /update/version_debug.json')
        time.sleep(0.2)
        BGM_SSH().type_commands(f'echo -n "{VERSION_DEBUG_3}" >> /update/version_debug.json')
        time.sleep(0.2)
        BGM_SSH().type_commands(f'echo -n "{task_id}" >> /update/version_debug.json')
        time.sleep(0.2)
        BGM_SSH().type_commands(f'echo -n "{VERSION_DEBUG_BACK}" >> /update/version_debug.json')
        time.sleep(0.2)
    elif BGM_HWPN:
        logger.info("========================================================")
        logger.info("Current domain controller: BGM ")
        logger.info("========================================================")
        BGM_SSH().type_commands(f'echo -n "{VERSION_DEBUG_1}" > /update/version_debug.json')
        time.sleep(0.2)
        BGM_SSH().type_commands(f'echo -n "{BGM_HWPN}" >> /update/version_debug.json')
        time.sleep(0.2)
        BGM_SSH().type_commands(f'echo -n "{VERSION_DEBUG_4}" >> /update/version_debug.json')
        time.sleep(0.2)
        BGM_SSH().type_commands(f'echo -n "{task_id}" >> /update/version_debug.json')
        time.sleep(0.2)
        BGM_SSH().type_commands(f'echo -n "{VERSION_DEBUG_BACK}" >> /update/version_debug.json')
        time.sleep(0.2)       
    elif TCAM_HWPN:
        logger.info("========================================================")
        logger.info("Current domain controller: TCAM ")
        logger.info("========================================================")
        BGM_SSH().type_commands(f'echo -n "{VERSION_DEBUG_1}" > /update/version_debug.json')
        time.sleep(0.2)        
        BGM_SSH().type_commands(f'echo -n "{TCAM_HWPN}" >> /update/version_debug.json')
        time.sleep(0.2)
        BGM_SSH().type_commands(f'echo -n "{VERSION_DEBUG_3}" >> /update/version_debug.json')
        time.sleep(0.2)
        BGM_SSH().type_commands(f'echo -n "{task_id}" >> /update/version_debug.json')
        time.sleep(0.2)
        BGM_SSH().type_commands(f'echo -n "{VERSION_DEBUG_BACK}" >> /update/version_debug.json')
        time.sleep(0.2)        
    else:
        logger.error("no ecu need fota ？")

def refresh_version_debug_cdc(task_id):
        logger.info("========================================================")
        logger.info("Current domain controller: CDC ")
        logger.info("========================================================")
        BGM_SSH().type_commands(f'echo -n "{VERSION_DEBUG_1}" > /update/version_debug.json')
        time.sleep(0.2)
        BGM_SSH().type_commands(f'echo -n "6608010818  F" >> /update/version_debug.json')
        time.sleep(0.2)
        BGM_SSH().type_commands(f'echo -n "{VERSION_DEBUG_2_CDC}" >> /update/version_debug.json')
        time.sleep(0.2)
        BGM_SSH().type_commands(f'echo -n "{task_id}" >> /update/version_debug.json')
        time.sleep(0.2)
        BGM_SSH().type_commands(f'echo -n "{VERSION_DEBUG_BACK}" >> /update/version_debug.json')
        time.sleep(0.2)   

def refresh_ua_skip(allow_same_version_flash=False):
    BGM_SSH().type_commands(f'echo "[" > /update/ua_skip')
    if allow_same_version_flash:
        BGM_SSH().type_commands(f'echo -n "{UA_SKIP_allow_same_version_flash}" >> /update/ua_skip')
    BGM_SSH().type_commands(f'echo "]" >> /update/ua_skip')

def refresh_version_debug_pro(task_id):
    BGM_SSH().type_commands(f'echo "{VERSION_DEBUG_FRONT_PRO}" > version_debug.json')
    BGM_SSH().type_commands(f'echo "{task_id}" >> version_debug.json')
    BGM_SSH().type_commands(f'echo "{VERSION_DEBUG_BACK_PRO}" >> version_debug.json')

def clear_tcam_env():
    # 清tcam环境
    TCAM_SSH().type_commands("rm /mnt/sdcard/Update/update_agent_persist.json")
    logger.info("======================= clear tcam env =======================")

def clear_bgm_log():
    # 清bgm log
    BGM_SSH().type_commands("rm -rf /log/*")
    logger.info("======================= clear bgm log =======================")
    time.sleep(5)

def get_bgm_log(log_path):
    # 取bgm log
    logger.info("======================= get bgm log =======================")
    BGM_SSH().get_log(log_path)

def get_tcam_log(log_path):
    # 取tcam log
    logger.info("======================= get tcam log =======================")
    TCAM_SSH().get_log(log_path,"/mnt/sdcard/log/jetlog_mess*")

def reboot_bgm():
    # 重启bgm
    logger.info("======================= reboot bgm, wait 30s =======================")
    # command_send(device_name='BGM', cmd='sudo -s')
    # command_send(device_name='BGM', cmd='bgm@Axzfr778')
    command_send(device_name='BGM', cmd="cp /app/etc/reboot.sh /tmp/jiduer && chmod +x /tmp/jiduer/reboot.sh && runuser -l powerMgr -c '/tmp/jiduer/reboot.sh'")
    time.sleep(30)

@func_set_timeout(30)    
def reboot_tcam():
    # 重启tcam
    TCAM_SSH().type_commands("reboot;exit")
    logger.info("reboot tcam,wait 10s...")
    # time.sleep(10)

def copy_packet():
    # 工厂灌包
    command_send(device_name='BGM', cmd='sudo -s')
    command_send(device_name='BGM', cmd='bgm@Axzfr778')
    command_send(device_name='BGM', cmd="cp /update/factory_bak/* /update/factory")
    time.sleep(5)
    BGM_SSH().type_commands("sync")
    time.sleep(0.5)
    logger.info("======================= copy factory_bak >> factory =======================")
    
def rebuild_bgm_log():
    # 重新生成bgm log
    BGM_SSH().type_commands("ps -ef|grep -E 'jetlogd'|grep app|awk -F " " '{print $2}'|xargs kill -9")
    time.sleep(10)
    logger.info("rebuild log")

def clear_cdc_env():
    os.system("/root/script/auto_tools/clear_cdc_env.sh")

def clear_acu_env():
    os.system("/root/script/auto_tools/clear_acu_env.sh")
    
def switch_to_4G():
    TCAM_SSH().type_commands('''cat /dev/smd8 & echo -en "at+gtact=2\r\n" > /dev/smd8''')
    logger.info("======================= download by 4G =======================")

def switch_to_5G():
    TCAM_SSH().type_commands('''cat /dev/smd8 & echo -en "at+gtact=14\r\n" > /dev/smd8''')
    logger.info("======================= download by 5G =======================")

def turn_on_airplane_mode():
    command_send(device_name='TCAM', cmd='''echo -en "at+cfun=0\\r\\n" > /dev/smd8''')
    logger.info("======================= turn on airplane mode =======================")
    time.sleep(2)
    
def turn_off_airplane_mode():
    command_send(device_name='TCAM', cmd='''echo -en "at+cfun=1\\r\\n" > /dev/smd8''')
    logger.info("======================= turn off airplane mode =======================")
    time.sleep(2)
    
def get_bgm_version():
    bgm_version = BGM_SSH().get_version().get('build_version')
    logger.info(f"======================= BGM version is {bgm_version} =======================")
    return bgm_version

def get_tcam_version():
    tcam_version = TCAM_SSH().get_version()
    logger.info(f"======================= TCAM version is {tcam_version} =======================")
    return tcam_version

def refresh_skip_debug(debug_list):
    if not debug_list:
        BGM_SSH().type_commands(f'echo -n "{SKIP_DEBUG_MUST_USED_IN_TWO_DOMAIN_FRONT}" > /update/skip_debug')
        BGM_SSH().type_commands(f'echo -n "{SKIP_DEBUG_MUST_USED_IN_TWO_DOMAIN_BACK}" >> /update/skip_debug')
        time.sleep(0.5)
        command_send(device_name='BGM', cmd='''rm /update/state-backup.pb;rm /update/state.pb;rm /update/update_agent_persist.json;sync;ps -ef|grep -E "ua|install|fota|obt|arb|jetlog"|grep app|awk -F " " '{print $2}'|xargs kill -9;sync''')    
        time.sleep(10)
    else:
        BGM_SSH().type_commands(f'echo -n "{SKIP_DEBUG_MUST_USED_IN_TWO_DOMAIN_FRONT}" > /update/skip_debug')
        for debug_word in debug_list:
            BGM_SSH().type_commands(f"echo -n ''',\n''' >> /update/skip_debug")    
            BGM_SSH().type_commands(f'echo -n \\" >> /update/skip_debug')    
            BGM_SSH().type_commands(f'echo -n {debug_word} >> /update/skip_debug')   
            BGM_SSH().type_commands(f'echo -n \\" >> /update/skip_debug')    
        BGM_SSH().type_commands(f'echo -n "{SKIP_DEBUG_MUST_USED_IN_TWO_DOMAIN_BACK}" >> /update/skip_debug')
        time.sleep(0.5)
        command_send(device_name='BGM', cmd='''rm /update/state-backup.pb;rm /update/state.pb;rm /update/update_agent_persist.json;sync;ps -ef|grep -E "ua|install|fota|obt|arb|jetlog"|grep app|awk -F " " '{print $2}'|xargs kill -9;sync''')    
        time.sleep(20)
        

if __name__ == '__main__':
    # pass
    # turn_on_airplane_mode()
    # turn_off_airplane_mode()
    refresh_version_debug_cdc(123)