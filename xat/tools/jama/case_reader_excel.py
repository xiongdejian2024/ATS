# -*- coding: utf-8 -*-
"""
@File        : case_reader_excel.py
@Author      : jinhui.zhao@jiduauto.com
@Time        : 2022/7/12 20:02
@Description : 
@Examples    :
"""

import openpyxl
from xat_ecu.legacy.common.logger import logger

MANDATORY_FIELDS = ['Function Category', 'QA Owner', 'Case_ID', 'Name', 'Preconditions', 'TestSteps', 'ExpectResults']


class CaseFmtException(Exception):
    """This is the base class for all exceptions raised by the JamaClient"""

    def __init__(self, message):
        super(CaseFmtException, self).__init__(message)


class Case:
    def __init__(self, row_num, header: list, values: list):
        self.Case_ID = None
        self.row_num = None
        self.construct_case(row_num, header, values)
        self.check_case_validation(header)

    def construct_case(self, row_num, header, values):
        setattr(self, "row_num", row_num)
        if len(header) == len(values):
            for i in range(len(header)):
                setattr(self, header[i], values[i])

    def check_case_validation(self, header):
        row_info = self.row_num
        error_str = ""
        for h in header:
            if not getattr(self, h) and h in MANDATORY_FIELDS:
                error_str += f'{h} is empty\n'
        # if error_str != "":
        #     raise CaseFmtException(f'row: {row_info} case format error:\n{error_str}')


class CaseParser(object):

    def __init__(self, case_f):
        try:
            self.case_f = case_f
            self.workbook = openpyxl.load_workbook(case_f)
            self.sheets = self.workbook.sheetnames
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/jama/case_reader_excel.py")
            logger.error(str(e))

    def max_row(self, sheet_name):
        return self.workbook.get_sheet_by_name(sheet_name).max_row

    def max_column(self, sheet_name):
        return self.workbook.get_sheet_by_name(sheet_name).max_column

    def get_sheet_header(self, sheet_name):
        sheet = self.workbook[sheet_name]
        header = []
        for c in range(1, sheet.max_column + 1):
            value = sheet.cell(1, c).value
            if value:
                header.append(value)
        return header

    def parse_sheet(self, sheet_name):
        sheet = self.workbook[sheet_name]
        header = self.get_sheet_header(sheet_name)
        logger.info(header)
        case = []
        for r in range(2, sheet.max_row + 1):
            case_data = []
            for c in range(1, len(header) + 1):
                value = sheet.cell(r, c).value
                case_data.append(value)
            case.append(Case(r, header, case_data))
        return case

    def add_col(self, sheet_name, col, col_num):
        """
        col: 在第几行前插入
        col_num: 插入的行数
        """
        sheet = self.workbook[sheet_name]
        sheet.insert_cols(col, col_num)
        self.workbook.save(self.case_f)

    def insert_data(self, sheet_name, data, row, col):
        sheet = self.workbook[sheet_name]
        sheet.cell(row, col).value = data
        self.workbook.save(self.case_f)

    def create_sheet(self, sheet_name):
        self.workbook.create_sheet(sheet_name)
        self.workbook.save(self.case_f)


if __name__ == "__main__":
    case_file = "jama_id.xlsx"
    sheet = "jama"
    o_case = CaseParser(case_file)
    o_case.create_sheet("111")
    print(CaseParser("ffff.xlsx").sheets)
    cases = CaseParser("ffff.xlsx").parse_sheet("OuterRearViewService")
    print(len(cases))
    o_case.add_col(sheet, 1, 2)
    o_case.insert_data(sheet, "jama_id", 1, 1)
    o_case.insert_data(sheet, "Case_ID", 1, 2)
    for cs in cases:
        logger.info(f'row: {cs.row_num}, case_id: {cs.Case_ID}')

