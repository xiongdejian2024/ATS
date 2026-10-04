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

from openpyxl import Workbook

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_ecu.legacy.common.logger import Logger


class indicator:
    def __init__(self, dir_name, time_range=None, apn_dict=None):
        """
        occurrence_time_range: 发生时间区间
        indicator_type：指标类型，枚举值
        result：结果
        """
        if apn_dict is None:
            apn_dict = {"APN1": "rmnet_data0", "APN4": "rmnet_data1"}
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
        self.global_APN1 = apn_dict.get("APN1")
        self.global_APN4 = apn_dict.get("APN4")

        self.indi_list = {"平均网络延时": {"must": ['CellPingSts.cpp:192', "2023"], "or": [f"interfacename:{self.global_APN1}",  f"interfacename:{self.global_APN4}"],
                                     "exclude": [], "data_lines": [], "result": {}},
                               "pingfail": {"must": ['CellPingSts.cpp:164', 'ApnIndex', "2023"], "or": [], "exclude": [],
                                            "data_lines": [], "result":{}},
                               "蜂窝断网": {"must": ['AbnormalEvent', "Write log", "2023"], "or": [], "exclude": ["sleep", "wakeup", "reboot"],
                                        "data_lines": [], "result": {}},
                               "蜂窝重连": {"must": ['DailupSetup', "2023", "Write log"], "or": [], "exclude": ["reboot"],
                                        "data_lines": [], "result": {}},
                               "蜂窝断网恢复时长": {"must": ['DailupSetup', "2023", "Write log"], "or": [], "exclude": [],
                                            "data_lines": [], "result": {}},
                               "蜂窝在线时长": {"must": ['DailupSetup', "2023", "Write log"], "or": [], "exclude": [],
                                          "data_lines": [], "result": {}},
                               "休眠&唤醒时间戳": {"must": ['BROADCAST_TOPIC_ID_EVERY_MODULE', "2023"], "or": [], "exclude": [],
                                            "data_lines": [], "result": {}},
                               "上电&下电时间": {"must": ["2023"], "or": ["POWER_OFF", "Mip Init Start"], "exclude": [],
                                           "data_lines": [], "result": {}},
                               "mqtt断连": {"must": ["2023"], "or": ["MqttConnectEventReport", "MqttDisconnectEventReport"],
                                          "exclude": [], "data_lines": [], "result": {}},
                               "上传&下载速率": {"must": [], "or": ["DownCurrentRateAverage",
                                                                         "UploadCurrentRateAverage"], "exclude": [],
                                           "data_lines": [], "result": {}},
                               "IPA失效": {"must": ['Write log', "2023"], "or": ["IPAFailure", "IPARecover"], "exclude": [],
                                         "data_lines": [], "result": {}},
                               "modem crash": {"must": ['Write log', "modem_crash", "2023"], "or": [], "exclude": [],
                                               "data_lines": [], "result": {}},
                               "5G & 4G占网比": {"must": ['NetStatusMonitor.cpp:269', "APN1", "2023"], "or": [], "exclude": [],
                                              "data_lines": [], "result": {}},
                               "车辆运动轨迹": {"must": ['gnss_service.cpp:201 GNSSInfo', "2023"], "or": [], "exclude": [],
                                          "data_lines": [], "result": {}},
                               "日志时间同步": {"must": ['vehicle_time:', "2023"],
                                          "or": ["set system time", "start ptp4l Succeed", "set rtc time"],
                                          "exclude": [], "data_lines": [], "result": {}}
                          }
        self.workbook = Workbook()

    def statistical_indicator_results(self):
        """
        获取每个指标相关的待分析数据
        """
        file_list = get_file_in_dir(self.dir_name)
        curr = ""
        for file_name in file_list:
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
        else:
            self.start_time = self.occurrence_time_range[0]
            self.end_time = self.occurrence_time_range[1]
            self.hours = round((convert(self.end_time) - convert(self.start_time)).seconds / 3600, 2) + \
                         round((convert(self.end_time) - convert(self.start_time)).days * 24, 2)
            self.seconds = (convert(self.end_time) - convert(self.start_time)).seconds + \
                           round((convert(self.end_time) - convert(self.start_time)).days * 24 * 3600, 2)
            for start, end in self.occurrence_time_range[2]:
                self.hours2 += (round((convert(end) - convert(start)).seconds / 3600, 2) +
                                round((convert(end) - convert(start)).days * 24, 2))
            for start, end in self.occurrence_time_range[2]:
                self.seconds2 += ((convert(end) - convert(start)).seconds +
                                  round((convert(end) - convert(start)).days * 24 * 3600, 2))
            self.hours -= self.hours2
            self.seconds -= self.seconds2
            for key in self.indi_list:
                self.indi_list[key]["data_lines"].sort()  # 重新排序
        """
        生成每个指标的统计结果
        """
        for key in self.indi_list:
            self.indicator_type = key
            self.result = self.indi_list[key]["data_lines"]
            self.filter_result()
        else:
            try:
                if self.indi_list["蜂窝重连"]["result"]["蜂窝重连次数-APN1"] > 0:
                    self.indi_list["蜂窝重连"]["result"]["蜂窝重连平均恢复时长-APN1"] = round(self.total_NetSetupTime_APN1 / self.indi_list["蜂窝重连"]["result"]["蜂窝重连次数-APN1"] * 0.001, 2)
                else:
                    self.indi_list["蜂窝重连"]["result"]["蜂窝重连平均恢复时长-APN1"] = 0

                if self.indi_list["蜂窝重连"]["result"]["蜂窝重连次数-APN4"] > 0:
                    self.indi_list["蜂窝重连"]["result"]["蜂窝重连平均恢复时长-APN4"] = round(self.total_NetSetupTime_APN4 / self.indi_list["蜂窝重连"]["result"]["蜂窝重连次数-APN4"] * 0.001, 2)
                else:
                    self.indi_list["蜂窝重连"]["result"]["蜂窝重连平均恢复时长-APN4"] = 0
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/util/road_test_core_performance_statistics.py")
                print(e)

        """
        打印执行结果
        """
        logger.info(f"开始时间：{self.occurrence_time_range[0]}")
        logger.info(f"结束时间：{self.occurrence_time_range[1]}")
        logger.info(f"排除时间范围：{self.occurrence_time_range[2]}")
        logger.info(f"小时数：{self.hours}")
        logger.info(f"总秒数：{self.seconds}")
        for index, key in enumerate(self.indi_list, 1):
            logger.info(f"{index}:"+json.dumps(self.indi_list[key]["result"], ensure_ascii=False, indent=4).
                   encode('utf-8').decode('utf-8'))

    def filter_result(self):
        if self.indicator_type == '平均网络延时':
            ICMPTime_list_rmnet_data1 = []
            ICMPTime_list_rmnet_data0 = []
            for line in self.result:
                if len(line) > 0:
                    current_row_time = line.split(" ")[0] + " " + line.split(" ")[1].split('.')[0]
                    ICMPTime = int(line.split("ICMPTime=")[1].split(",")[0])
                    if convert(current_row_time) > convert(self.occurrence_time_range[0]):
                        if convert(current_row_time) < convert(self.occurrence_time_range[1]):
                            if self.global_APN1 in line:
                                ICMPTime_list_rmnet_data0.append(ICMPTime)
                            if self.global_APN4 in line:
                                ICMPTime_list_rmnet_data1.append(ICMPTime)
            if len(ICMPTime_list_rmnet_data0) > 0:
                self.indi_list[self.indicator_type]["result"][f"IMCPTime平均延时-{self.global_APN1}"] = \
                    sum(ICMPTime_list_rmnet_data0) // len(ICMPTime_list_rmnet_data0)
            if len(ICMPTime_list_rmnet_data1) > 0:
                self.indi_list[self.indicator_type]["result"][f"IMCPTime平均延时-{self.global_APN4}"] = \
                    sum(ICMPTime_list_rmnet_data1) // len(ICMPTime_list_rmnet_data1)
            self.indi_list[self.indicator_type]["result"]["开始时间"] = self.occurrence_time_range[0]
            self.indi_list[self.indicator_type]["result"]["结束时间"] = self.occurrence_time_range[1]
            self.ICMPTime_list_rmnet_data0 = ICMPTime_list_rmnet_data0
            self.ICMPTime_list_rmnet_data1 = ICMPTime_list_rmnet_data1
        elif self.indicator_type == 'pingfail':
            last_three_list_apn1 = []
            last_three_list_apn4 = []
            pingfail_result_ApnIndex1 = []
            pingfail_result_ApnIndex1_total = 0
            pingfail_result_ApnIndex1_total_nq_2 = 0
            pingfail_result_ApnIndex4 = []
            pingfail_result_ApnIndex4_total = 0
            pingfail_result_ApnIndex4_total_nq_2 = 0
            base_time_apn1 = ""
            base_time_apn4 = ""
            count_apn1 = 0
            count_apn4 = 0

            for line in self.result:
                if len(line) > 0:
                    current_row_time = line.split(" ")[0] + " " + line.split(" ")[1]
                    ApnIndex = int(line.split("ApnIndex:")[1].split(",")[0])
                    Count = int(line.split("Count:")[1])
                    if "ApnIndex:1" in line:
                        if base_time_apn1 == "":
                            base_time_apn1 = current_row_time.strip()
                            count_apn1 = Count
                        else:
                            if count_apn1 >= Count:
                                if count_apn1 >= 3:
                                    pingfail_result_ApnIndex1.append((base_time_apn1,
                                                                      f"ApnIndex:{ApnIndex},Count:{count_apn1}"))
                                    pingfail_result_ApnIndex1_total += count_apn1
                                else:
                                    pingfail_result_ApnIndex1_total_nq_2 += count_apn1
                            base_time_apn1 = current_row_time.strip()
                            count_apn1 = Count

                    if "ApnIndex:4" in line:
                        if base_time_apn4 == "":
                            base_time_apn4 = current_row_time.strip()
                            count_apn4 = Count
                        else:
                            if count_apn4 >= Count:
                                if count_apn4 >= 3:
                                    pingfail_result_ApnIndex4.append((base_time_apn4,
                                                                      f"ApnIndex:{ApnIndex},Count:{count_apn4}"))
                                    pingfail_result_ApnIndex4_total += count_apn4
                                else:
                                    pingfail_result_ApnIndex4_total_nq_2 += count_apn4
                            base_time_apn4 = current_row_time.strip()
                            count_apn4 = Count
            else:
                if count_apn1 >= 3:
                    pingfail_result_ApnIndex1.append((base_time_apn1,
                                                      f"ApnIndex:1,Count:{count_apn1}"))
                    pingfail_result_ApnIndex1_total += count_apn1
                else:
                    pingfail_result_ApnIndex1_total_nq_2 += count_apn1

                if count_apn4 >= 3:
                    pingfail_result_ApnIndex4.append((base_time_apn4,
                                                      f"ApnIndex:4,Count:{count_apn4}"))
                    pingfail_result_ApnIndex4_total += count_apn4
                else:
                    pingfail_result_ApnIndex4_total_nq_2 += count_apn4

                logger.info("连续3次pingfail导致的断网结果")
                logger.info(f"apn1: {self.fail_count_offline_apn1}")
                logger.info(f"apn4: {self.fail_count_offline_apn4}")
                pingfail_result_ApnIndex1_total += pingfail_result_ApnIndex1_total_nq_2
                pingfail_result_ApnIndex4_total += pingfail_result_ApnIndex4_total_nq_2
            self.indi_list[self.indicator_type]["result"]["pingfail次数-ApnIndex1"] = pingfail_result_ApnIndex1_total
            self.indi_list[self.indicator_type]["result"][
                "pingfail占比-ApnIndex1"] = pingfail_result_ApnIndex1_total / len(self.ICMPTime_list_rmnet_data0)
            self.indi_list[self.indicator_type]["result"]["pingfail次数-ApnIndex4"] = pingfail_result_ApnIndex4_total
            self.indi_list[self.indicator_type]["result"][
                "pingfail占比-ApnIndex4"] = pingfail_result_ApnIndex4_total / len(self.ICMPTime_list_rmnet_data1)
            self.indi_list[self.indicator_type]["result"]["pingfail概率-ApnIndex1"] = f"{round(len(pingfail_result_ApnIndex1)/self.hours,2)}次每小时"
            self.indi_list[self.indicator_type]["result"]["pingfail概率-ApnIndex4"] = f"{round(len(pingfail_result_ApnIndex4) / self.hours, 2)}次每小时"
            self.indi_list[self.indicator_type]["result"]["pingfail时间戳ApnIndex1"] = pingfail_result_ApnIndex1
            self.indi_list[self.indicator_type]["result"]["pingfail时间戳ApnIndex4"] = pingfail_result_ApnIndex4
        elif self.indicator_type == "蜂窝断网":
            network = []
            for line in self.result:
                if len(line) > 0:
                    if line.startswith("2023"):
                        current_row_time = line.split(" ")[0] + " " + line.split(" ")[1]
                        content = line.split("Write log")[1].strip()
                        network.append((current_row_time.strip(), eval(content)))
            else:
                fail_count = len(network)
            self.indi_list[self.indicator_type]["result"]["蜂窝断网次数"] = fail_count
            self.indi_list[self.indicator_type]["result"]["蜂窝断网概率"] = f"{round(fail_count/self.hours,2)}次每小时"
            self.indi_list[self.indicator_type]["result"]["蜂窝断网时间戳"] = network
        elif self.indicator_type == "蜂窝重连":
            network_APN1 = []
            network_APN4 = []
            for line in self.result:
                if len(line) > 0:
                    if line.startswith("2023"):
                        # logger.info(f"蜂窝重连：{line}")
                        current_row_time = line.split(" ")[0] + " " + line.split(" ")[1]
                        content = line.split("Write log")[1].strip()
                        ct_dict = eval(content)
                        if ct_dict.get('SwitchStatus') == 0 or ct_dict.get('TriggerResult') in ['wakeup', 'sleep'] \
                                or ct_dict.get('DailupResult') != 1:
                            continue
                        else:
                            if '"APN_Index":1' in line:
                                network_APN1.append((current_row_time.strip(), eval(content)))
                            if '"APN_Index":4' in line:
                                network_APN4.append((current_row_time.strip(), eval(content)))
            else:
                apn1_count1 = 0
                apn1_count2 = 0
                apn1_count3 = 0
                for ins in network_APN1:
                    if ins[1].get("NetSetupTime") <= 5000:
                        apn1_count1 += 1
                    elif ins[1].get("NetSetupTime") <= 30000:
                        apn1_count2 += 1
                    else:
                        apn1_count3 += 1
                else:
                    if len(network_APN1) > 0:
                        apn1_count1 = f"{round(apn1_count1 / len(network_APN1), 4) * 100}%"
                        apn1_count2 = f"{round(apn1_count2 / len(network_APN1), 4) * 100}%"
                        apn1_count3 = f"{round(apn1_count3 / len(network_APN1), 4) * 100}%"

                apn4_count1 = 0
                apn4_count2 = 0
                apn4_count3 = 0
                for ins in network_APN4:
                    if ins[1].get("NetSetupTime") <= 5000:
                        apn4_count1 += 1
                    elif ins[1].get("NetSetupTime") <= 30000:
                        apn4_count2 += 1
                    else:
                        apn4_count3 += 1
                else:
                    if len(network_APN4) > 0:
                        apn4_count1 = f"{round(apn4_count1 / len(network_APN4), 4) * 100}%"
                        apn4_count2 = f"{round(apn4_count2 / len(network_APN4), 4) * 100}%"
                        apn4_count3 = f"{round(apn4_count3 / len(network_APN4), 4) * 100}%"

            self.indi_list[self.indicator_type]["result"]["蜂窝重连次数-APN1"] = len(network_APN1)
            self.indi_list[self.indicator_type]["result"]["蜂窝重连次数分布-APN1"] = {"0-5秒占比": apn1_count1,
                                                                              "5秒到30秒占比": apn1_count2,
                                                                              "超过30秒占比": apn1_count3}
            self.indi_list[self.indicator_type]["result"]["蜂窝重连时间戳-APN1"] = network_APN1

            self.indi_list[self.indicator_type]["result"]["蜂窝重连次数-APN4"] = len(network_APN4)
            self.indi_list[self.indicator_type]["result"]["蜂窝重连次数分布-APN4"] = {"0-5秒占比": apn4_count1,
                                                                              "5秒到30秒占比": apn4_count2,
                                                                              "超过30秒占比": apn4_count3}
            self.indi_list[self.indicator_type]["result"]["蜂窝重连时间戳-APN4"] = network_APN4
        elif self.indicator_type == "蜂窝断网恢复时长":
            network_APN1 = []
            network_APN4 = []
            total_NetSetupTime_APN1 = 0
            total_NetSetupTime_APN4 = 0
            for line in self.result:
                if len(line) > 0:
                    if line.startswith("2023"):
                        # logger.info(f"蜂窝断网恢复时长：{line}")
                        current_row_time = line.split(" ")[0] + " " + line.split(" ")[1]
                        content = line.split("Write log")[1].strip()
                        ct_dict = eval(content)
                        if ct_dict.get('SwitchStatus') == 1 and ct_dict.get('TriggerResult') not in ['wakeup', 'sleep']:
                            # logger.info(f"有效的数据：{content}")
                            if ct_dict.get("APN_Index") == 1:
                                network_APN1.append((current_row_time.strip(), ct_dict.get("NetSetupTime")))
                                total_NetSetupTime_APN1 += ct_dict.get("NetSetupTime")
                            if ct_dict.get("APN_Index") == 4:
                                network_APN4.append((current_row_time.strip(), ct_dict.get("NetSetupTime")))
                                total_NetSetupTime_APN4 += ct_dict.get("NetSetupTime")
                            continue
            self.total_NetSetupTime_APN1 = total_NetSetupTime_APN1
            self.total_NetSetupTime_APN4 = total_NetSetupTime_APN4
            self.indi_list[self.indicator_type]["result"]["断网恢复时长-APN1"] = f"{total_NetSetupTime_APN1 // 1000}秒"
            self.indi_list[self.indicator_type]["result"]["蜂窝网络在线线率-APN1"] = \
                f"{(1-round((total_NetSetupTime_APN1 // 1000)/self.seconds, 4))*100}%"
            self.indi_list[self.indicator_type]["result"]["断网恢复时长-APN4"] = f"{total_NetSetupTime_APN4 // 1000}秒"
            self.indi_list[self.indicator_type]["result"]["蜂窝网络在线线率-APN4"] = \
                f"{(1 - round((total_NetSetupTime_APN4 // 1000) / self.seconds, 4)) * 100}%"
        elif self.indicator_type == "蜂窝在线时长":
            network = []
            total_NetSetupTime = 0
            for line in self.result:
                if len(line) > 0:
                    if line.startswith("2023"):
                        current_row_time = line.split(" ")[0] + " " + line.split(" ")[1]
                        content = line.split("Write log")[1].strip()
                        ct_dict = eval(content)
                        if ct_dict.get('SwitchStatus') == 1 and ct_dict.get('TriggerResult') not in ['wakeup', 'sleep']:
                            # logger.info(f"有效的数据：{content}")
                            network.append((current_row_time.strip(), ct_dict.get("NetSetupTime")))
                            total_NetSetupTime += ct_dict.get("NetSetupTime")
                            continue
            else:
                online_time_second = self.seconds - total_NetSetupTime//1000
            self.indi_list[self.indicator_type]["result"]["蜂窝在线总时长"] = f"{online_time_second}秒"
        elif self.indicator_type == "休眠&唤醒时间戳":
            network = []
            wake_up_count = 0
            sleep_count = 0
            for line in self.result:
                if len(line) > 0:
                    if line.startswith("2023"):
                        if "power" in line:
                            if "SLEEP" in line:
                                sleep_count += 1
                                current_row_time = line.split(" ")[0] + " " + line.split(" ")[1]
                                network.append((current_row_time, "SLEEP"))
                            elif "WAKEUP" in line:
                                wake_up_count += 1
                                current_row_time = line.split(" ")[0] + " " + line.split(" ")[1]
                                network.append((current_row_time, "WAKEUP"))
            self.indi_list[self.indicator_type]["result"]["唤醒次数"] = wake_up_count
            self.indi_list[self.indicator_type]["result"]["休眠次数"] = sleep_count
            self.indi_list[self.indicator_type]["result"]["休眠唤醒时间戳"] = network
        elif self.indicator_type == "上电&下电时间":
            network = []
            mip_init_start_count = 0
            power_off_count = 0
            for line in self.result:
                if len(line) > 0:
                    if line.startswith("2023"):
                        if "power" in line:
                            if "Mip Init Start" in line:
                                mip_init_start_count += 1
                                current_row_time = line.split(" ")[0] + " " + line.split(" ")[1]
                                network.append((current_row_time, "Mip Init Start"))
                            elif "POWER_OFF" in line:
                                power_off_count += 1
                                current_row_time = line.split(" ")[0] + " " + line.split(" ")[1]
                                network.append((current_row_time, "POWER_OFF"))
            # else:
            #     logger.info(f"{self.indicator_type}:上电次数:{mip_init_start_count}，下电次数：{power_off_count}")
            self.indi_list[self.indicator_type]["result"]["上电次数"] = mip_init_start_count
            self.indi_list[self.indicator_type]["result"]["下电次数"] = power_off_count
            self.indi_list[self.indicator_type]["result"]["上电下电时间戳"] = network
        elif self.indicator_type == "mqtt断连":
            network = []
            mqtt_disconnect_count = 0  # mqtt断连次数
            mqtt_disconnect_total_time = 0  # mqtt 断连总时长,单位秒
            mqtt_connect_total_time = 0  # mqtt 连接总时长,单位秒
            mqtt_disconnect_happen_time = ""
            mqtt_connect_happen_time = ""
            first_flag = ""
            for line in self.result:
                if len(line) > 0:
                    if line.startswith("2023"):
                        current_row_time = line.split(" ")[0] + " " + line.split(" ")[1]
                        if "MqttConnectEventReport" in line:
                            content = line.split("MqttConnectEventReport")[1].strip()
                            # logger.info(content)
                        elif "MqttDisconnectEventReport" in line:
                            content = line.split("MqttDisconnectEventReport")[1].strip()
                        ct_dict = eval(content)

                        if ct_dict.get('logtype') == "MQTTDisconnect":
                            mqtt_disconnect_count += 1  # mqtt断连次数
                            if len(first_flag) == 0:
                                first_flag = "MQTTDisconnect"
                                online_time = (convert(ct_dict.get("time").split(".")[0])-convert(self.start_time)).seconds
                                mqtt_connect_total_time += online_time
                            else:
                                online_time = (convert(ct_dict.get("time").split(".")[0]) - convert(mqtt_connect_happen_time)).seconds
                                mqtt_connect_total_time += online_time
                            mqtt_disconnect_happen_time = ct_dict.get("time").split(".")[0]
                            network.append((current_row_time, {"logtype": "MQTTDisconnect",
                                                               "time": ct_dict.get("time")}))
                        if ct_dict.get('logtype') == "MqttConnect":
                            if len(first_flag) == 0:
                                first_flag = "MqttConnect"
                                offline_time = (convert(ct_dict.get("time").split(".")[0])-convert(self.start_time)).seconds
                                mqtt_disconnect_total_time += offline_time
                            else:
                                offline_time = (convert(ct_dict.get("time").split(".")[0]) - convert(mqtt_disconnect_happen_time)).seconds
                                mqtt_disconnect_total_time += offline_time
                            mqtt_connect_happen_time = ct_dict.get("time").split(".")[0]
                            network.append((current_row_time, {"logtype": "MqttConnect",
                                                               "time": ct_dict.get("time")}))
            else:
                if len(mqtt_connect_happen_time) > 0 and len(mqtt_disconnect_happen_time) > 0:
                    if (convert(mqtt_connect_happen_time) - convert(mqtt_disconnect_happen_time)).seconds > 0:
                        online_time = (convert(self.end_time) - convert(mqtt_connect_happen_time)).seconds
                        mqtt_connect_total_time += online_time
                    else:
                        offline_time = (convert(self.end_time) - convert(mqtt_disconnect_happen_time)).seconds
                        mqtt_disconnect_total_time += offline_time
                total_seconds = (convert(self.end_time) - convert(self.start_time)).seconds

                self.indi_list[self.indicator_type]["result"]["mqtt统计总时长"] = f"{total_seconds}秒"
                self.indi_list[self.indicator_type]["result"]["mqtt在线时长"] = f"{mqtt_connect_total_time}秒"
                self.indi_list[self.indicator_type]["result"]["mqtt断连时长"] = f"{mqtt_disconnect_total_time}秒"
                self.indi_list[self.indicator_type]["result"]["mqtt断连次数"] = mqtt_disconnect_count
                self.indi_list[self.indicator_type]["result"]["mqtt断连连接时间点"] = network
        elif self.indicator_type == "上传&下载速率":
            network = []
            down_total_rate = 0
            up_total_rate = 0
            for line in self.result:
                if len(line) > 0:
                    if not line.startswith("2023"):
                        try:
                            ct_dict = eval(line.strip())
                            if ct_dict.get('APN_Index') == 4:
                                network.append((ct_dict.get('time'), {"down": ct_dict.get('DownCurrentRateAverage'),
                                                "upload": ct_dict.get('UploadCurrentRateAverage')}))
                                down_total_rate += ct_dict.get('DownCurrentRateAverage')
                                up_total_rate += ct_dict.get('UploadCurrentRateAverage')
                                continue
                        except Exception as e:
                            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/util/road_test_core_performance_statistics.py")
                            continue
            else:
                down_average_rate = 0 if len(network) == 0 else round(down_total_rate*8/len(network)/1024/1024, 2)
                up_average_rate = 0 if len(network) == 0 else round(up_total_rate*8/len(network)/1024/1024, 2)
                network.sort(key=lambda x: convert(x[0]))
                self.workbook = Workbook()
                self.workbook.create_sheet(self.indicator_type)
                sheet = self.workbook[self.indicator_type]
                sheet.cell(row=1, column=1).value = "时间戳"
                sheet.cell(row=1, column=2).value = "下载速率"
                sheet.cell(row=1, column=3).value = "上传速率"
                for i in range(len(network)):
                    sheet.cell(row=i+2, column=1).value = network[i][0]
                    sheet.cell(row=i+2, column=2).value = network[i][1].get("down")
                    sheet.cell(row=i+2, column=3).value = network[i][1].get("upload")

                sheet.cell(row=2, column=2).value = 2

                self.workbook.save(f"{self.indicator_type}.xlsx")
            self.indi_list[self.indicator_type]["result"]["下载速率"] = f"{down_average_rate}Mb/S"
            self.indi_list[self.indicator_type]["result"]["上传速率"] = f"{up_average_rate}Mb/S"
        elif self.indicator_type == "IPA失效":
            network = []
            ipa_count = 0
            IPAFailure_time = ""
            IPARecover_time = ""
            for line in self.result:
                if len(line) > 0:
                    if line.startswith("2023"):
                        current_row_time = line.split(".")[0]
                        content = line.split("Write log")[1].strip()
                        ct_dict = eval(content)
                        # logger.info(f"Event:{ct_dict.get('Event')};")
                        if ct_dict.get('Event') == "IPAFailure" and len(IPAFailure_time) == 0:
                            logger.info(f"更新失效时间")
                            logger.info(json.dumps(ct_dict, ensure_ascii=False, indent=4).encode('utf-8').decode('utf-8'))
                            IPAFailure_time = current_row_time
                            network.append((current_row_time, "IPAFailure"))
                        if ct_dict.get('Event') == "IPARecover":
                            if len(IPAFailure_time) > 0:
                                logger.info("更新生效时间：")
                                logger.info(json.dumps(ct_dict, ensure_ascii=False, indent=4).encode('utf-8').decode('utf-8'))
                                IPARecover_time = current_row_time
                                network.append((current_row_time, "IPARecover"))
                                # aa = convert(IPARecover_time)-convert(IPAFailure_time)
                                # # logger.info(f"时间差秒数：{aa.seconds}")
                                if (convert(IPARecover_time)-convert(IPAFailure_time)) >= timedelta(seconds=30):
                                    ipa_count += 1
                                else:
                                    IPAFailure_time = ""
                                    IPARecover_time = ""
            self.indi_list[self.indicator_type]["result"]["IPA失效次数"] = ipa_count
            self.indi_list[self.indicator_type]["result"]["IPA失效时间戳"] = network
        elif self.indicator_type == "modem crash":
            network = []
            modem_crash_count = 0
            for line in self.result:
                if len(line) > 0:
                    if line.startswith("2023"):
                        current_row_time = line.split(" ")[0] + " " + line.split(" ")[1]
                        content = line.split("Write log")[1].strip()
                        ct_dict = eval(content)
                        if ct_dict.get('Event') == "modem_crash":
                            network.append((current_row_time, "modem_crash"))
                            modem_crash_count += 1
            self.indi_list[self.indicator_type]["result"]["modem_crash次数"] = modem_crash_count
            self.indi_list[self.indicator_type]["result"]["modem_crash概率"] = \
                f"{round(modem_crash_count/self.hours, 2)}次每小时"
            self.indi_list[self.indicator_type]["result"]["modem_crash时间戳"] = network
        elif self.indicator_type == "5G & 4G占网比":
            network = []
            total_num = 0
            SA_num = 0
            LTE_num = 0
            NSA_num = 0
            for line in self.result:
                if len(line) > 0:
                    if line.startswith("2023"):
                        nettype = line.split("nettype:")[1].split(" ")[0].strip()
                        total_num = total_num + 1
                        if nettype == "SA":
                            SA_num = SA_num + 1
                        elif nettype == "LTE":
                            LTE_num = LTE_num + 1
                        elif nettype == "NSA":
                            NSA_num += 1
            else:
                network.append(("total", total_num))
                network.append(("SA", SA_num))
                network.append(("LTE", LTE_num))
                # logger.info(f"{self.indicator_type}: 占网比：{round((SA_num+LTE_num)/total_num,4)*100}%")
            self.indi_list[self.indicator_type]["result"]["total"] = total_num
            self.indi_list[self.indicator_type]["result"]["SA"] = SA_num
            self.indi_list[self.indicator_type]["result"]["LTE"] = LTE_num
            self.indi_list[self.indicator_type]["result"]["NSA"] = NSA_num
            self.indi_list[self.indicator_type]["result"]["5G & 4G占网比"] = f"{round((SA_num+LTE_num+NSA_num)/total_num,4)*100}%"
        elif self.indicator_type == "车辆运动轨迹":
            network = []
            for line in self.result:
                if len(line) > 0:
                    if line.startswith("2023"):
                        current_row_time = line.split(" ")[0] + " " + line.split(" ")[1]
                        content = line.split("GNSSInfo:")[1].strip()
                        result_dict = eval(content)
                        longitude = result_dict.get("longitude")
                        latitude = result_dict.get("latitude")
                        network.append((current_row_time, longitude, latitude))
            else:
                self.workbook = Workbook()
                self.workbook.create_sheet(self.indicator_type)
                sheet = self.workbook[self.indicator_type]
                ws = self.workbook[self.workbook.sheetnames[1]]
                ws.column_dimensions['A'].width = 11.0
                sheet.cell(row=1, column=1).value = "时间戳"
                sheet.cell(row=1, column=2).value = "longitude"
                sheet.cell(row=1, column=3).value = "latitude"
                for i in range(len(network)):
                    sheet.cell(row=i + 2, column=1).value = network[i][0]
                    sheet.cell(row=i + 2, column=2).value = network[i][1]
                    sheet.cell(row=i + 2, column=3).value = network[i][2]
                self.workbook.save(f"{self.indicator_type}.xlsx")
        elif self.indicator_type == '日志时间同步':
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
                logger.info(f"日志时间同步:{result_dict['set system time']}")
                logger.info(f"日志时间同步:{result_dict['start ptp4l Succeed']}")
                logger.info(f"日志时间同步:{result_dict['set rtc time']}")


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


def candump_check(check_cmd):
    pi = subprocess.Popen(check_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
    stdout = pi.stdout.read()
    return stdout


def convert(my_date_str):
    # 将字符串按逗号分割，取第一个部分作为日期时间字符串
    my_date_str = my_date_str.split('",')[0]
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

    # all
    # exclude_period =[]
    # occurrence_time_range = ["2023-09-11 10:40:33", "2023-09-11 15:40:34", exclude_period]

    # 静态城区
    # exclude_period =[("2023-09-10 11:08:33", "2023-09-10 11:28:34"), ("2023-09-10 11:40:33", "2023-09-10 11:45:34"), 
    #                  ("2023-09-10 11:55:33", "2023-09-10 12:45:34"), ("2023-09-10 13:00:33", "2023-09-10 13:55:34"),
    #                  ("2023-09-10 14:11:33", "2023-09-10 15:20:34")]
    # occurrence_time_range = ["2023-09-10 10:58:33", "2023-09-10 16:00:34", exclude_period]

    # 动态城区
    # exclude_period =[("2023-09-10 10:58:33", "2023-09-10 11:08:34"), ("2023-09-10 11:28:33", "2023-09-10 11:40:34"), 
    #                  ("2023-09-10 11:45:33", "2023-09-10 11:55:34"), ("2023-09-10 12:45:33", "2023-09-10 13:00:34"),
    #                  ("2023-09-10 13:55:33", "2023-09-10 14:11:34")]
    # occurrence_time_range = ["2023-09-10 10:40:33", "2023-09-10 15:20:34", exclude_period]

    # 静态郊区
    # exclude_period = [("2023-09-11 11:08:33", "2023-09-11 11:33:34"), ("2023-09-11 11:43:33", "2023-09-11 11:54:34"), 
    #                   ("2023-09-11 12:30:33", "2023-09-11 12:50:34"), ("2023-09-11 13:00:33", "2023-09-11 14:07:34"),
    #                   ("2023-09-11 14:20:33", "2023-09-11 14:32:34"), ("2023-09-11 14:42:33", "2023-09-11 15:24:34")]
    # occurrence_time_range = ["2023-09-11 11:03:33", "2023-09-11 15:40:34", exclude_period]

    # 动态郊区
    exclude_period = [("2023-09-11 11:03:33", "2023-09-11 11:08:34"), ("2023-09-11 11:33:33", "2023-09-11 11:43:34"), 
                      ("2023-09-11 11:54:33", "2023-09-11 12:30:34"), ("2023-09-11 12:50:33", "2023-09-11 13:00:34"),
                      ("2023-09-11 14:07:33", "2023-09-11 14:20:34"), ("2023-09-11 14:32:33", "2023-09-11 14:42:34"),
                      ("2023-09-11 15:07:33", "2023-09-11 15:17:34")]
    occurrence_time_range = ["2023-09-11 10:40:33", "2023-09-11 15:24:34", exclude_period]

    # 地下室
    # exclude_period = []
    # occurrence_time_range = ["2023-09-11 15:07:33", "2023-09-11 15:17:34", exclude_period]

    indicator0 = indicator(time_range=occurrence_time_range,
                           dir_name=r"D:\sat-develop\tools\util_fin\dir",
                           apn_dict={"APN1": "rmnet_data0", "APN4": "rmnet_data1"})
    indicator0.statistical_indicator_results()

