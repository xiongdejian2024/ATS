#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_

"""
@Time: 2022/9/9 13:23  
@Author: lei.tao
@File: to_new_excel.py
@Software: PyCharm
@Description: 
@Example:
test_template, summary, VehicleBaseDataUpload(删除)
"""
import os,sys

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)


import openpyxl
from xat_ecu.legacy.common.logger import logger
from tools.jama.upload import upload
from tools.jama.update import update


expect_list = ['诊断仲裁']


def to_new_excel(old_file, new_file):

    wb = openpyxl.load_workbook(old_file)
    n_row = 1
    header = []
    for sn in wb.sheetnames:

        if sn in expect_list:
            sheet = wb[sn]
            logger.info(f'{sn} in list')

            # 插入header
            if not header:
                logger.info(f'{sn} for header')
                for c in range(1, sheet.max_column + 1):
                    val = sheet.cell(1, c).value
                    if val:
                        header.append(val)

            # 插入case
            for r in range(2, sheet.max_row + 1):  # 从第二行开始
                # 去除首个单元格为空的行
                if sheet.cell(r, 1).value is None:
                    logger.info(f'{sn} row: {r}, colum: {1} skipped')
                    continue
                if isinstance(sheet.cell(r, 1).value, str):
                    if sheet.cell(r, 1).value.strip() == "":
                        logger.info(f'{sn} row: {r}, colum: {1} skipped')
                        continue
                n_row += 1
                for c in range(1, sheet.max_column + 1):
                    sheet.cell(r, c)

            # 插入一空白列jama_id
            if "jama_id" not in header:
                sheet.insert_cols(1, 1)
                sheet.cell(1, 1, value="jama_id")

            # 用例存在jama_id的更新，不存在的插入
            for a in range(2, sheet.max_row + 1):

                if sheet.cell(a, 1).value is None:
                    case_id = sheet.cell(a, 3).value
                    if case_id:
                        jama_id = upload(old_file, sn, case_id)
                        print(case_id)
                        sheet.cell(a, 1, value=jama_id)
                    else:
                        break

                else:
                    jama_id = sheet.cell(a, 1).value
                    print(jama_id)
                    case_id = sheet.cell(a, 3).value
                    if case_id:
                        update(old_file, sn, jama_id)
                    else:
                        break

    wb.save(filename=new_file)


if __name__ == '__main__':

    to_new_excel("SOA_BGM_测试2.xlsx", "SOA_BGM_测试1.xlsx")
