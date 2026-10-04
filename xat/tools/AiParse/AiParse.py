#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**********************
@File    : AiParse.py

**********************

------------------------------------------------------------------
@Time    : 2024/7/30 13:36
@Author  : jiewen.deng
Language: Python 3.9
------------------------------------------------------------------
Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.
"""
import argparse
import copy
import json
import os
import re
import sys
import time

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

import pandas as pd
from loguru import logger
# import win32com.client as win32
from openpyxl import load_workbook
import xlrd
import os
from datetime import datetime
from xat_ecu.legacy.interface.feishu.feishu_api import feishu_api


class RexcelHandle(object):
    def __init__(self, file_path):
        self.wb = xlrd.open_workbook(file_path)
        self.ws = self.wb.sheets()[0]

    @property
    def get_nrows(self):
        return self.ws.nrows

    @property
    def get_ncols(self):
        return self.ws.ncols

    def get_row_values(self,row_value):
        return [self.get_cell_type_filter_value(row_value,y) for y,x in enumerate(self.ws.row_values(row_value))]

    def get_col_values(self,col_value):
        return [self.get_cell_type_filter_value(y,col_value) for y,x in enumerate(self.ws.col_values(col_value))]

    def get_cell_value(self,x,y):
        return self.ws.cell(x,y).value

    def get_cell_type_filter_value(self, x, y):
        cell = self.get_cell_value(x,y)
        ctype = self.ws.cell(x,y).ctype
        if ctype == 2 and cell % 1 == 0:
            cell = int(cell)
        elif ctype == 3:
            date = datetime(*xlrd.xldate_as_tuple(cell, 0))
            cell = date.strftime('%Y/%m/%d %H:%M:%S')
        elif ctype == 4:
            cell = True if cell == 1 else False
        return cell


def is_chinese_char(char):
    if '\u4e00' <= char <= '\u9fff':
        return True
    return False


class AiParse(object):

    def __init__(self, path):
        self.path = path
        self.excel_obj = RexcelHandle(path)

    def parse_excel_data_to_feishu(self):
        single_meta_user_dict = {}
        col_0_list = self.excel_obj.get_col_values(0)[1:]
        col_10_list = self.excel_obj.get_col_values(10)[1:]
        col_4_list = self.excel_obj.get_col_values(4)[1:]
        col_5_list = self.excel_obj.get_col_values(5)[1:]
        col_6_list = self.excel_obj.get_col_values(6)[1:]
        col_7_list = self.excel_obj.get_col_values(7)[1:]
        col_8_list = self.excel_obj.get_col_values(8)[1:]
        col_9_list = self.excel_obj.get_col_values(9)[1:]
        for index, value in enumerate(col_0_list):
            if value in user_list:
                accept_info = json.loads(col_10_list[index])

                user_id = feishu.get_user_open_id(name=value)
                if user_id is None:
                    logger.warning(f"not found feishu people:{value}")
                    continue
                # logger.info(f"获取到的用户id是：{user_id}")
                raw_data = {"用户名": value,
                            "人员": [{'id': user_id}],
                            "采纳行数": int(col_4_list[index]),
                            "推荐行数": int(col_5_list[index]),
                            "采纳率": str(col_6_list[index]),
                            "是否为活跃用户": col_7_list[index],
                            "采纳次数": int(col_8_list[index]),
                            "推荐次数": int(col_9_list[index]),
                            }

                raw_data1 = {}
                for single in accept_info:
                    if is_chinese_char(single['name']):
                        if str(single['name']).endswith("建议"):
                            raw_data1[single['name']] = single['suggestion']
                        elif str(single['name']).endswith("接受"):
                            raw_data1[single['name']] = single['accepted']
                        else:
                            raw_data1[single['name'] + "建议"] = single['suggestion']
                            raw_data1[single['name'] + "接受"] = single['accepted']
                    # feishu.update_record_in_table(table_id, result[1], {single['name']: message})
                raw_data.update(raw_data1)
                # print(f"accept_info:{accept_info}")

                if value not in single_meta_user_dict:
                    single_meta_user_dict[value] = raw_data
                else:
                    for k, v in single_meta_user_dict[value].items():
                        if k in ["采纳行数", "推荐行数", "采纳次数", "推荐次数"]:
                            single_meta_user_dict[value][k] = single_meta_user_dict[value][k] + raw_data[k]
                        if k == "采纳率":
                            if single_meta_user_dict[value]['推荐行数'] == 0:
                                single_meta_user_dict[value]['采纳率'] = '0%'
                            else:
                                single_meta_user_dict[value]['采纳率'] = str(round(
                                    (int(single_meta_user_dict[value]['采纳行数']) / int(
                                        single_meta_user_dict[value]['推荐行数']))*100, 2)) + "%"
                        if str(k).endswith("接受") or str(k).endswith("建议"):
                            if k in raw_data:
                                single_meta_user_dict[value][k] = single_meta_user_dict[value][k] + + raw_data[k]

        for write_data in single_meta_user_dict.values():
            result = feishu.add_record_in_table(table_id, write_data)
            logger.info(f"write user data is:{write_data}")
            logger.info(f"add result is:{result}")
            logger.info("==========================")
            time.sleep(0.1)

    def extraction_data(self, data_path):
        wb = load_workbook(data_path)
        all_sheet_name = wb.sheetnames
        useful_sheet = [i for i in all_sheet_name if i not in ['hidden']]
        single_meta_user_dict = {}
        for i in range(len(useful_sheet)):
            data_i = pd.read_excel(data_path, sheet_name=useful_sheet[i])
            for index, value in enumerate(data_i["用户名"]):
                if value in user_list:
                    accept_info = json.loads(data_i["分功能次数"][index])

                    user_id = feishu.get_user_open_id(name=value)
                    if user_id is None:
                        logger.warning(f"not found feishu people:{value}")
                        continue
                    # logger.info(f"获取到的用户id是：{user_id}")
                    raw_data = {"用户名": value,
                                "人员": [{'id': user_id}],
                                "采纳行数": int(data_i["采纳行数"][index]),
                                "推荐行数": int(data_i["推荐行数"][index]),
                                "采纳率": str(data_i["采纳率"][index]),
                                "是否为活跃用户": data_i["是否为活跃用户"][index],
                                "采纳次数": int(data_i["采纳次数"][index]),
                                "推荐次数": int(data_i["推荐次数"][index]),
                                }

                    raw_data1 = {}
                    for single in accept_info:
                        if is_chinese_char(single['name']):
                            raw_data1[single['name']+"建议"] = single['suggestion']
                            raw_data1[single['name']+"接受"] = single['accepted']
                        # feishu.update_record_in_table(table_id, result[1], {single['name']: message})
                    raw_data.update(raw_data1)
                    # print(f"accept_info:{accept_info}")

                    # print(f"raw_data:{raw_data}")
                    # print("======================")

                    if value not in single_meta_user_dict:
                        single_meta_user_dict[value] = raw_data
                    else:
                        for k, v in single_meta_user_dict[value].items():
                            if k in ["采纳行数", "推荐行数", "采纳次数", "推荐次数"]:
                                single_meta_user_dict[value][k] = single_meta_user_dict[value][k] + raw_data[k]
                            if k == "采纳率":
                                if single_meta_user_dict[value]['推荐行数'] == 0:
                                    single_meta_user_dict[value]['采纳率'] = '0%'
                                else:
                                    single_meta_user_dict[value]['采纳率'] = str(round(int(single_meta_user_dict[value]['采纳行数'])/int(single_meta_user_dict[value]['推荐行数']), 2)) + "%"
                            if str(k).endswith("接受") or str(k).endswith("建议"):
                                if k in raw_data:
                                    single_meta_user_dict[value][k] = single_meta_user_dict[value][k] + + raw_data[k]

        for write_data in single_meta_user_dict.values():
            # result = feishu.add_record_in_table(table_id, write_data)
            logger.info(f"write user data is:{write_data}")
            # logger.info(f"add result is:{result}")
            logger.info("==========================")
            time.sleep(0.1)


def parse_xls_to_xlsx(file_path, out_file_path):
    # excel = win32.gencache.EnsureDispatch("Excel.Application")
    # wb = excel.Workbooks.Open(os.path.abspath(file_path))
    # wb.SaveAs(os.path.abspath(out_file_path), FileFormat=51)
    # wb.Close()
    # excel.Application.Quit()

    data = pd.read_excel(file_path)
    data.to_excel(out_file_path, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-fp', '--file_path', type=str, default="用户数据详情.xls", help="指定用户AI数据路径")
    args = parser.parse_args()
    if not args.file_path:
        raise AssertionError(f"not found user ai data path.")

    src_file_path = args.file_path

    # logger.info(f"found user ai data path:{src_file_path}")
    # outfile = os.path.join(os.getcwd(), "autotest.xlsx")
    # if os.path.exists(outfile):
    #     os.remove(outfile)
    # parse_xls_to_xlsx(src_file_path, outfile)

    soa_user = """
        quan.sun,quan.sun@jiduauto.com
        dejian.xiong,dejian.xiong@jiduauto.com
        songjian.lin,songjian.lin@jiduauto.com
        jiewen.deng,jiewen.deng@jiduauto.com
        lei.hong,lei.hong@jiduauto.com
        lei.song, lei.song@jiduauto.com
        taiping.zong, taiping.zong@jiduauto.com
        yunpeng.zhou, yunpeng.zhou@jiduauto.com
        linfeng.xu, linfeng.xu@jiduauto.com
        O_liangliang.chen, o_liangliang.chen@external.jiduauto.com
        zhongchen.wang,zhongchen.wang@jiduauto.com
        renyue.dai, renyue.dai@jiduauto.com
        liu.yang, liu.yang@jiduauto.com
        lijian.wang, lijian.wang@jiduauto.com
        O_zhuangzhuang.huang, o_zhuangzhuang.huang@external.jiduauto.com
        junxing.pang, junxing.pang@jiduauto.com
        haoran.jia, haoran.jia@jiduauto.com
        lei.an, lei.an@jiduauto.com
        jinzhi.lv, jinzhi.lv@jiduauto.com
        O_jingyuan.chen, o_jingyuan.chen@external.jiduauto.com
        O_huajie.yang, o_huajie.yang@external.jiduauto.com
        xiaoqiang.hu,  xiaoqiang.hu@jiduauto.com
        jiabin.zhu,  jiabin.zhu@jiduauto.com
        jingjing.wang, jingjing.wang@jiduauto.com
        qingxia.ai, qingxia.ai@jiduauto.com
        lei.tao, lei.tao@jiduauto.com
        gang.liu, gang.liu@jiduauto.com
        chi.han, chi.han@jiduauto.com
        tao.cheng_ext, tao.cheng_ext@external.jiduauto.com
        jishu.duan_ext, jishu.duan_ext@external.jiduauto.com
        O_daidi.liang01, o_daidi.liang01@external.jiduauto.com
        qian.feng,qian.feng@jiduauto.com
        jianwen.wang,jianwen.wang@jiduauto.com
        heng.wang,heng.wang@jiduauto.com
        xiangyue.li,xiangyue.li@jiduauto.com
        O_guojing.yang,o_guojing.yang@external.jiduauto.com
        O_fan.liu,o_fan.liu@external.jiduauto.com
        shulin.zheng,shulin.zheng@jiduauto.com
        yucheng.zhu,yucheng.zhu@jiduauto.com
        mingyue.xing,mingyue.xing@jiduauto.com
        lijian.wang,lijian.wang@jiduauto.com
        hui.zhao,hui.zhao@jiduauto.com
        tanggeng.li,tanggeng.li@jiduauto.com
        zhipeng.zhou,zhipeng.zhou@jiduauto.com
        dongfang.ding@jiduauto.com
    """

    user_name = [i.strip() for i in soa_user.split('\n') if i.strip()]
    user_list = []
    for user in user_name:
        if len(user.split(',')) == 1:
            user_list.append(user.split('@')[0])
        elif len(user.split(',')) == 2:
            user_list.append(user.split(',')[0])
        else:
            raise AssertionError(f"输入的格式不对：{user}")

    feishu = feishu_api()
    feishu.get_app_access_token()
    feishu.get_user_access_token()
    feishu.get_bitable_app_access_token(document_id="RtQsw2wsTiyYaNkwTqScGQJpnre")
    table_id = feishu.get_table_id_by_table_name("使用数据")

    ai_obj = AiParse(src_file_path)
    # ai_obj.extraction_data(src_file_path)
    ai_obj.parse_excel_data_to_feishu()
