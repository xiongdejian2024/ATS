# -*- coding: utf-8 -*-
"""
@File        : xmindparser_tool.py
@Author      : quan.sun@jiduauto.com
@Time        : 2022/04/11 12:18
@Description :
@Examples    :
"""

from xmindparser import xmind_to_dict
import openpyxl
from xat_ecu.legacy.common.logger import logger


class XmindParseTool:
    def __init__(self, xmindfilepath, case_file_path):
        self.xmindfilepath = xmindfilepath
        self.case_file_path = case_file_path

    def get_sheetlist_from_xmind(self):
        # 调用python中xmind_to_dict方法,将xmind转成字典
        self.sheets = xmind_to_dict(self.xmindfilepath)  # sheets是一个list，可包含多sheet页；
        # print(self.sheets)
        for sheet in self.sheets:
            self.my_list = sheet['topic']['topics']  # 字典的值sheet['topic']['topics']是一个list
            # print(self.my_list)
        return self.my_list

    def get_title_and_topics_from_casedict(self, casedict: dict):
        if isinstance(casedict, dict):
            title = casedict.get("title")
            topics = casedict.get("topics")
            return title, topics
        else:
            logger.error("casedict is not dict")

    def get_cases_data(self, sheetlist):
        rowdatas = []
        for sheet in sheetlist:
            title1, topics1 = self.get_title_and_topics_from_casedict(sheet)
            i = 0
            if isinstance(topics1, list):
                for topic_dict in topics1:
                    rowdata = []
                    i += 1
                    title1_1 = "{}_{:0>4d}".format(title1, i)
                    rowdata.append(title1_1)
                    topics = topic_dict
                    while topics:
                        title, topics = self.get_title_and_topics_from_casedict(topics)
                        # Later, there is only one dict in a list
                        if isinstance(topics, list):
                            topics = topics[0]
                        # print(title)
                        rowdata.append(title)
                    rowdatas.append(rowdata)
            else:
                logger.warning("Some cases are incomplete")
        return rowdatas

    def write_data_into_excel(self):
        testfile = openpyxl.load_workbook(self.case_file_path)
        sheet_all_names = testfile.sheetnames
        for sh_name in sheet_all_names:
            sh = testfile[sh_name]

            # check row 1 value
            # row1 = sh[1]
            # row1_list = [cell.value for cell in row1]
            # logger.info(row1_list)
            # row1_list ----------- ['Case_ID', 'Name', 'Preconditions', 'Test Steps', 'Expect Results',
            # 'Test Platform','Test Execution Mode', 'TestCase Priority', 'Tags', 'Verifies(DPMS/CR/Issue)',
            # 'Test Level', 'Automatable']

            casedict = self.get_sheetlist_from_xmind()
            excel_datas = self.get_cases_data(casedict)
            # print(excel_datas)
            for data in excel_datas:
                sh.append(data)
        testfile.save("/home/sun/quansun/sat/tools/case_tools/SOA_Fota.xlsx")
        testfile.close()



if __name__ == "__main__":

    xmindtool = XmindParseTool("/home/sun/quansun/sat/tools/case_tools/SOA_Fota.xmind", "/home/sun/quansun/sat/tools/case_tools/Case_Template.xlsx")
    xmindtool.write_data_into_excel()