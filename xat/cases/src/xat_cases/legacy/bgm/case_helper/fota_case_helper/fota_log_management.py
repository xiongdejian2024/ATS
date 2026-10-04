'''
Author: liu.yang
Date: 2023-02-01 19:05:06
LastEditors: Do not edit
LastEditTime: 2023-07-04 18:07:18
FilePath: /yangliu_tmp/sat/xat_cases/legacy/bgm/case_helper/fota_case_helper/fota_log_management.py
'''
import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path, ".."))
sys.path.append(os.path.join(current_path, "../.."))
sys.path.append(os.path.join(current_path, "../../.."))

from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.tsp.tsp_fota import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.interface.tcam.tcam_ssh import *
from xat_ecu.legacy.interface.nuc_app import *
from fota_constant import *
# from fota_cahce import *
class Fota_log_management:
            
    def __monitor_log_by_tail(
        self,
        grep: str,
        expect_targets_list: List[str],
        unexpect_targets_list: List[str],
        failed_msg: str,
        succ_msg: str,
        log_path: str = "/log/jetlog_messages",
        tail_num: int = 100,
        debug: bool = False,
        tail_timeout: int = 3,
    ):
        time.sleep(3)
        cmd = f"echo bgm@Axzfr778 | sudo -S /app/bin/zstdcat /log/jetlog_messages|grep -E ' fota:|UpdateNotifyEOLCaliInfoEvent:'|tail -n 100000"
        stdout = BGM_SSH().type_commands(cmd,root_permission=False)
        content = stdout
        for target in expect_targets_list:
            if target in content:
                logger.info(f"## hit expected target: {target}")
                return succ_msg
            
        for target in unexpect_targets_list:
            if target in content:
                logger.info(f"## hit unexpected target: {target}")
                return failed_msg

        
        # actual_fufil_targets_count = 0
        # for target in expect_targets_list:
        #     if target in content:
        #         logger.info(f"found expected target: {target}")
        #         actual_fufil_targets_count += 1
        # if actual_fufil_targets_count == len(expect_targets_list):
        #     return succ_msg

        return ""
    
    def monitor_jetlog_messages_by_tail(
        self,
        grep: str,
        expect_targets_list: List[str],
        unexpect_targets_list: List[str],
        failed_msg: str,
        succ_msg: str,
        tail_num: int = 100,
        debug: bool = False,
        max_retry_times: int = 100,
        retry_interval: int = 3,  # 重试间隔(单位: 秒)
    ):
        retry_times = 0
        while retry_times < max_retry_times:
            try:
                # ret = self.__monitor_log_by_tail(
                #     grep=grep,
                #     expect_targets_list=expect_targets_list,
                #     unexpect_targets_list=unexpect_targets_list,
                #     failed_msg=failed_msg,
                #     succ_msg=succ_msg,
                #     log_path="/log/jetlog_messages1",
                #     tail_num=tail_num,
                #     debug=debug,
                # )
                # # logger.info("===================log1")
                # if ret == succ_msg or ret == failed_msg:
                #     return ret               
                ret = self.__monitor_log_by_tail(
                    grep=grep,
                    expect_targets_list=expect_targets_list,
                    unexpect_targets_list=unexpect_targets_list,
                    failed_msg=failed_msg,
                    succ_msg=succ_msg,
                    log_path="/log/jetlog_messages",
                    tail_num=tail_num,
                    debug=debug,
                )
                # logger.info("===================log")
                if ret == succ_msg or ret == failed_msg:
                    return ret
                retry_times += 1
                time.sleep(retry_interval)
            except Exception as e:
                logger.exception(e)
        return failed_msg

    def monitor_jetlog_messages_by_tail_bool(
        self,
        expect_targets_list: List[str],
        unexpect_targets_list: List[str],
    ):
        try:
            ret = self.monitor_jetlog_messages_by_tail(
                grep="/fota/",
                expect_targets_list=expect_targets_list,
                unexpect_targets_list=unexpect_targets_list,
                failed_msg="fail",
                succ_msg="success",
                tail_num=100000,
                max_retry_times=50,
                retry_interval=30,  # 重试间隔(单位: 秒))
            )
            if ret == "fail":
                return False
            if ret == "success":
                return True
        except Exception as e:
            logger.exception(e)

if __name__ == '__main__':
    succ_msg = "FOTA start download"
    failed_msg="FOTA start download Failed"
    fota = Fota_log_management()
    result = fota.__monitor_log_by_tail_tmp(
        expect_targets_list=['a'
        ],
        unexpect_targets_list=['b']
        )
    if result == True:
        print(1)
    else:
        print(2)   


    # result1 = fota.monitor_jetlog_messages_by_tail_bool(
    #             expect_targets_list=[
    #             'check_ota_task => collect_version'],
    #             unexpect_targets_list=['"taskId":0']
    #     )
    # if result1 == True:
    #     print(11)
    # else:
    #     print(22) 