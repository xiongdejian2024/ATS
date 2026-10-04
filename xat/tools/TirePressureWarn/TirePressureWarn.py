#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**********************
@File    : TirePressureWarn.py

**********************

------------------------------------------------------------------
@Time    : 2024/10/18 13:03
@Author  : jiewen.deng
Language: Python 3.9
------------------------------------------------------------------
Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.
"""
from loguru import logger
from collections import defaultdict
from xat_ecu.legacy.interface.feishu.feishu_api import feishu_api


class TirePressureWarn(object):

    def __init__(self):
        pass


if __name__ == "__main__":
    feishu = feishu_api()
    feishu.get_bitable_app_access_token(document_id="GmxwwTxXtiGSCAkVyMVcj49lnuf")
    if feishu.app_access_token:
        table_id = feishu.get_table_id_by_table_name("胎压告警原始数据模版")
        # table_id = feishu.get_table_id_by_table_name("9月30-10月6 胎压告警原始数据")
        # table_id = feishu.get_table_id_by_table_name("9月23-9月29 胎压告警原始数据")
        # table_id = feishu.get_table_id_by_table_name("9月16-9月22-胎压告警原始数据")
        if table_id:
            logger.info(table_id)
            res = feishu.get_records_in_table(table_id)
            record_list_0 = []
            data_list_0 = []
            record_list_1 = []
            data_list_1 = []
            error_dict = {}

            for i in res:
                print(i)
                try:
                    if not all([i["fields"].get("告警解除时间"), i["fields"].get("告警发生时间")]):
                        record_list_0.append(i["record_id"])
                        data_list_0.append({"是否误报": 0})
                        # feishu.update_record_in_table(table_id, i["record_id"], {"是否误报": 0})
                    elif i["fields"]["告警解除时间"] - i["fields"]["告警发生时间"] <= 10*60:
                        if i["fields"]["告警解除时间"] < i["fields"]["告警发生时间"]:
                            record_list_0.append(i["record_id"])
                            data_list_0.append({"是否误报": 0})
                        else:
                            record_list_1.append(i["record_id"])
                            data_list_1.append({"是否误报": 1})
                            if i["fields"]["VIN"] not in error_dict:
                                error_dict[i["fields"]["VIN"]] = {i["fields"]["WTI 中文名"].strip(): [[i["fields"]["告警发生时间"], i["fields"]["告警解除时间"], i["record_id"]]]}
                            else:
                                if i["fields"]["WTI 中文名"].strip() not in error_dict[i["fields"]["VIN"]]:
                                    error_dict[i["fields"]["VIN"]][i["fields"]["WTI 中文名"].strip()] = [[i["fields"]["告警发生时间"], i["fields"]["告警解除时间"], i["record_id"]]]
                                else:
                                    error_dict[i["fields"]["VIN"]][i["fields"]["WTI 中文名"].strip()].append([i["fields"]["告警发生时间"], i["fields"]["告警解除时间"], i["record_id"]])

                        # print(i["fields"]["VIN"], i["fields"]["告警发生时间"], i["fields"]["告警解除时间"])
                        # feishu.update_record_in_table(table_id, i["record_id"], {"是否误报": 1})
                    else:
                        record_list_0.append(i["record_id"])
                        data_list_0.append({"是否误报": 0})
                        # feishu.update_record_in_table(table_id, i["record_id"], {"是否误报": 0})
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/TirePressureWarn/TirePressureWarn.py")
                    print(e)
                    print(i)
                    print('==========')

            remove_record_dict = {}
            for k, v in error_dict.items():
                if "胎压低报警二级提醒 TPMS Low Pressure Warning" in v:
                    if "胎压低报警一级报警 TPMS Low Pressure Warning" in v:
                        for i in v["胎压低报警二级提醒 TPMS Low Pressure Warning"]:
                            for j in v["胎压低报警一级报警 TPMS Low Pressure Warning"]:
                                if j[0] == i[1]:
                                    # for i_d, value in enumerate(record_list_1):
                                    #     if value == j[2]:
                                    index = record_list_1.index(j[2])
                                    remove_record_dict[index] = j[2]

            for k, v in remove_record_dict.items():
                print(f"一级和二级误报时间冲突的记录有：{v}")
                try:
                    record_list_1.remove(v)
                    data_list_1.pop()
                    record_list_0.append(v)
                    data_list_0.append({"是否误报": 0})
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/TirePressureWarn/TirePressureWarn.py")
                    print(f"操作失败：{e}")
            print(f"len(record_list_0) is:{len(record_list_0)}")
            print(f"len(data_list_0) is:{len(data_list_0)}")
            print(f"len(record_list_1) is:{len(record_list_1)}")
            print(f"len(data_list_1) is:{len(data_list_1)}")

            if len(record_list_0) > 100:
                count = len(record_list_0)//100 + 1 if len(record_list_0)//100 else len(record_list_0)//100
            else:
                count = 1
            for i in range(count):
                # print(f"record_list_0 is:{record_list_0}\ndata_list_0 is:{data_list_0}")
                # open("aaa.txt", "")
                result = feishu.batch_update_record_in_table(table_id, record_list_0[:100], data_list_0[:100])
                print(f"执行结果为：{result}")
                record_list_0 = record_list_0[100:]
                data_list_0 = data_list_0[100:]

            if len(record_list_1) > 100:
                count = len(record_list_1) // 100 + 1 if len(record_list_1) // 100 else len(record_list_1) // 100
            else:
                count = 1
            for i in range(count):
                # print(f"record_list_1 is:{record_list_1}\ndata_list_1 is:{data_list_1}")
                feishu.batch_update_record_in_table(table_id, record_list_1[:100], data_list_1[:100])
                record_list_0 = record_list_1[100:]
                data_list_0 = data_list_1[100:]
