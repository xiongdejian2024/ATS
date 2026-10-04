import json
import os
import sys
import threading
import time
from collections import defaultdict
from datetime import datetime
import copy

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_ecu.legacy.driver.ssh_client import SSHClient
from xat_ecu.legacy.common.logger import logger, Logger

file_analysis_result = defaultdict(dict)
full_result = defaultdict(dict)


class pid_info:
    def __int__(self):
        self.pid = 0
        self.start = 0
        self.end = 0
        self.rows = 0
        self.result = 0


class analysis:
    def __init__(self, floder):
        current_path = os.path.abspath(os.curdir)
        for file_name in os.listdir(floder):
            row = 0
            with open(os.path.join(current_path, "file_path", file_name), 'r') as f:
                pidInfo = pid_info()
                while True:
                    line = f.readline()
                    if line.startswith("2023-"):
                        row = row+1
                        current_pid, current_row_num = self.row_analysis(line)
                        if row == 1:  # 初始化
                            pidInfo.pid = current_pid
                            pidInfo.start = current_row_num
                            pidInfo.end = current_row_num
                            pidInfo.rows = 1
                        elif pidInfo.pid == current_pid:
                            pidInfo.end = current_row_num
                            pidInfo.rows = pidInfo.rows+1
                        elif pidInfo.pid != current_pid:
                            # logger.info("pid:{},start:{},end:{},row:{},result:{}".
                            #       format(pidInfo.pid, pidInfo.start, pidInfo.end, pidInfo.rows,
                            #              "Success" if (float(pidInfo.end)-float(pidInfo.start)+1) == float(pidInfo.rows)
                            #              else "Fail"))
                            if str(pidInfo.pid) in file_analysis_result:
                                file_analysis_result[str(pidInfo.pid)]["end"] = pidInfo.end
                                file_analysis_result[str(pidInfo.pid)]["row_count"] += pidInfo.rows
                                ss = float(file_analysis_result[str(pidInfo.pid)]["start"])
                                ee = float(pidInfo.end)
                                rr = file_analysis_result[str(pidInfo.pid)]["row_count"]
                                file_analysis_result[str(pidInfo.pid)]["result"] = "Success" if (ee-ss) == rr-1 \
                                    else "False"
                            else:
                                result = "Success" \
                                    if (float(pidInfo.end)-float(pidInfo.start)+1) == float(pidInfo.rows) else "Fail"
                                file_analysis_result[str(pidInfo.pid)] = {"start": pidInfo.start, "end": pidInfo.end,
                                                                          "row_count": pidInfo.rows, "result": result}

                            pidInfo.pid = current_pid
                            pidInfo.start = current_row_num
                            pidInfo.end = current_row_num
                            pidInfo.rows = 1
                        if row == 10000:
                            break
                logger.info("当前日志分析结果：")
                logger.info(json.dumps(file_analysis_result, ensure_ascii=False, indent=4))
            full_result[file_name] = file_analysis_result
        logger.info("所有日志分析结果：")
        logger.info(json.dumps(full_result, ensure_ascii=False, indent=4))

    def row_analysis(self, row_str):
        row_array = row_str.split(" ")
        # print("{}:{}".format(row_array[2], row_array[6]))
        return row_array[2], row_array[6][0:-1]


if __name__ == "__main__":
    logger = Logger().get_logger("test")
    # 在log_file_analysis 目录下创建子目录file_path，并将待分析的日志文件放在该目录下
    ana = analysis("file_path")

