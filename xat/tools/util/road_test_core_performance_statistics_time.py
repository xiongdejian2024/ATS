"""
@File        : road_test_core_performance_statistics
@Author      : songjian.lin@jiduauto.com
@Time        : 2023/8/8 13:34
@Description : 路测核心性能的自动化统计（离线分析）
"""
import json
import os
import pathlib
import subprocess
import sys
from datetime import datetime, timedelta

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_ecu.legacy.common.logger import Logger


class indicator:
    def __init__(self, dir_name, time_range=None):
        """
        occurrence_time_range: 发生时间区间
        indicator_type：指标类型，枚举值
        result：结果
        """
        self.occurrence_time_range = time_range
        self.indicator_type = ""
        self.start_time = ""
        self.end_time = ""
        self.hours = 0.0  # 日志文件结束时间与开始时间的“小时差”
        self.seconds = 0.0  # 日志文件结束时间与开始时间的“秒数差”
        self.hours2 = 0.0  # 日志文件结束时间与开始时间的“小时差”
        self.seconds2 = 0.0  # 日志文件结束时间与开始时间的“秒数差”
        self.dir_name = dir_name
        self.fail_count_offline_apn1 = 0
        self.fail_count_offline_apn4 = 0
        self.ICMPTime_list_rmnet_data1 = []
        self.ICMPTime_list_rmnet_data0 = []
        self.total_NetSetupTime_APN1 = 0
        self.total_NetSetupTime_APN4 = 0
        self.file_name = ""
        self.indi_list = {
                           "日志时间同步": {"must": ['vehicle_time:', "202"],
                                      "or": ["set system time", "start ptp4l Succeed", "set rtc time"],
                                      "exclude": [], "data_lines": [], "result": {}}
                          }

    def statistical_indicator_results(self):
        """
        获取每个指标相关的待分析数据
        """
        file_list = get_file_in_dir(self.dir_name)
        curr = ""
        for file_name in file_list:
            self.file_name = file_name
            with open(file_name, 'r', encoding='UTF-8', errors='ignore') as f:
                for line in f.readlines():
                    line = line.strip()
                    if len(line) > 0:  # 行的开头是2023
                        if line.startswith("2023"):
                            curr = convert(line.split('.')[0])
                        if curr == "":
                            continue
                        if curr >= convert(self.occurrence_time_range[0]):
                            if curr <= convert(self.occurrence_time_range[1]):
                                for start, end in self.occurrence_time_range[2]:
                                    if curr >= convert(start):
                                        if curr <= convert(end):
                                            break
                                else:  # 不在排除的时间段内
                                    for key in self.indi_list:
                                        if len(self.indi_list[key]['must']) > 0:
                                            if not all(x in line for x in self.indi_list[key]['must']):
                                                continue
                                        if len(self.indi_list[key]['or']) > 0:
                                            if not any([x in line for x in self.indi_list[key]['or']]):
                                                continue
                                        if len(self.indi_list[key]['exclude']) > 0:
                                            if not all([x not in line for x in self.indi_list[key]['exclude']]):
                                                continue
                                        self.indi_list[key]["data_lines"].append(line)
            for key in self.indi_list:
                self.indicator_type = key
                self.result = self.indi_list[key]["data_lines"]
                self.filter_result()
                self.indi_list = {
                    "日志时间同步": {"must": ['vehicle_time:', "202"],
                               "or": ["set system time", "start ptp4l Succeed", "set rtc time"],
                               "exclude": [], "data_lines": [], "result": {}}
                }

    def filter_result(self):
        if self.indicator_type == '日志时间同步':
            result_dict = {"set system time": [], "start ptp4l Succeed": [], "set rtc time": []}
            for line in self.result:
                if "set system time" in line:
                    current_row_time = line.split(" ")[0] + " " + line.split(" ")[1].split('.')[0]
                    result_dict["set system time"].append(current_row_time)
                if "start ptp4l Succeed" in line:
                    current_row_time = line.split(" ")[0] + " " + line.split(" ")[1].split('.')[0]
                    result_dict["start ptp4l Succeed"].append(current_row_time)
                if "set rtc time" in line:
                    current_row_time = line.split("set rtc time")[1].strip()[:-3]
                    current_row_time = timestamp_to_strtime(int(current_row_time))
                    result_dict["set rtc time"].append(current_row_time)
            else:
                logger.info(f"{self.file_name}"+json.dumps(result_dict, ensure_ascii=False, indent=4).encode('utf-8').decode('utf-8'))


def get_file_in_dir(dir_path):
    """
    获取目录下的所有文件
    """
    file_list = []
    if not os.path.exists(dir_path):
        logger.info(f"文件不存在")
        return
        # 把文件夹下的内容放入列表,便于下一步分析
    listName = os.listdir(dir_path)
    for fileDirName in listName:
        # 拼接成绝对路径
        abspath = os.path.join(dir_path, fileDirName)
        # os.path.isdir()
        if os.path.isfile(abspath):
            file_list.append(abspath)
    return file_list


def convert(my_date_str):
    result = datetime.strptime(my_date_str, "%Y-%m-%d %H:%M:%S")
    return result


def timestamp_to_strtime(timestamp: int):
    """将 10 位整数的秒级时间戳转化成本地普通时间 (字符串格式)
    :param timestamp: 10 位整数的秒级时间戳 (1688091489)
    :return: 返回字符串格式 {str} '2022-06-11 18:19:48'
    """
    timeArry = datetime.fromtimestamp(timestamp)
    strtime = timeArry.strftime('%Y-%m-%d %H:%M:%S')  # .%f 带不带都可
    return strtime


if __name__ == "__main__":
    logger = Logger().get_logger("test")
    occurrence_time_range = ["2021-01-01 00:00:00", "2025-08-11 15:59:00", []]

    indicator0 = indicator(time_range=occurrence_time_range,
                           dir_name=r"D:\soa\sat-develop\tools\util\dir")
    indicator0.statistical_indicator_results()
