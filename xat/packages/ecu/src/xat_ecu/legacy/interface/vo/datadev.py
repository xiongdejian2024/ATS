#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: data_vo.py
@Time: 2024/5/28 14:03
@Author: lei.hong
@Software: vscode
@Description: vo需求埋点数据查询
@Examples: 
"""
import time
import csv
import datetime
import requests
import base64
from xat_ecu.legacy.interface.vo import data_request
from xat_ecu.legacy.common.logger import logger, Logger
from xat_ecu.legacy.interface.vo.get_token import get_passport_b_token
from xat_ecu.legacy.interface.feishu.feishu_api import feishu_api
from xat_ecu.legacy.common.exception_error import ExecutionFailError, NoDataError
from xat_ecu.legacy.common.constant import DataConstant


class DataDev:
    """查询流程埋点数据"""

    def __init__(self,
                 user_name=base64.b64decode(DataConstant.DATA_USERNAME).decode(),
                 password=base64.b64decode(DataConstant.DATA_PASSWORD).decode(),
                 server_name=DataConstant.DATA_URL):
        """
        初始化函数，用于创建类的实例。
        
        Args:
            user_name (str, optional): 用户名，默认为base64解码后的DataConstant.DATA_USERNAME。
            password (str, optional): 密码，默认为base64解码后的DataConstant.DATA_PASSWORD。
            server_name (str, optional): 服务器名称，默认为DataConstant.DATA_URL。
        
        Returns:
            None
        """
        self.server_name = server_name
        self.date = None
        self.hour = None
        self.signalname = None
        self.httpheadervid = None
        self.sigvalue = None
        self.sql = None
        self.submit_id = None
        self.runid = 0
        self.next_runid = 0
        self.code = None
        self.data = None
        self.user_name = user_name
        self.password = password
        self.validate_status = None
        self.has_result = None
        self.is_end = False
        self.status = None
        self.total_size = 0

    def _post(self, url, data=None):
        """
        发送POST请求执行SQL语句，并返回执行结果。
        
        Args:
            url (str): 请求的URL地址。
            data (dict, optional): 请求的POST数据，默认为None。
        
        Returns:
            None: 如果请求失败，则返回None。
        
        Raises:
            NoDataError: 当获取data数据为空时触发。
            ExecutionFailError: 当SQL执行失败时触发。
        """
        try:
            run = data_request.DataRequest().post(url,
                                                  headers={
                                                      "username": self.user_name,
                                                      "access_token": get_passport_b_token("349a9e1ac04c44ad",
                                                                                           "904cae9755114eea8c19589e8ce7a215",
                                                                                           self.user_name,
                                                                                           self.password)},
                                                  data=data,
                                                  timeout=60)
            logger.debug(f"执行sql语句返回结果{run}")
            # print(f"执行sql语句返回结果{run}")
            self.code = run.get("code")
            if not self.code:
                data = run.get("data")
                if not data:
                    raise NoDataError("获取data数据为空")
                else:
                    self.data = data
            else:
                raise ExecutionFailError(f"sql执行失败,code:{self.code},submitId={self.submit_id}")
        except requests.exceptions.RequestException as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/vo/datadev.py")
            logger.info(f"sql post failed: {e}")
            return None

    def validate_sql(self, table_name="ods.ods_data_jade_ee_signal_qa_staging_h", dt=None, hr=None, ver=None, vid=None,
                     num=None, signal_name=None, signal_value=None, limit=100000, sql=None):
        """
        校验SQL语句
        
        Args:
            date (str, optional): 日期，格式为'YYYY-MM-DD'. 默认为None.
            hour (str, optional): 小时，格式为'HH'. 默认为None.
            signalname (str, optional): 信号名称. 默认为None.
            httpheadervid (str, optional): HTTP头版本号. 默认为None.
            sigvalue (str, optional): 信号值. 默认为None.
            limit (int, optional): 查询结果限制数量. 默认为100000.
            sql (str, optional): 待校验的SQL语句. 默认为None.
        
        Returns:
            None
        
        Raises:
            无
        
        注意：
        - 如果提供了sql参数，则直接使用该sql进行校验；
        """
        if sql:
            self.sql = sql
            start_index = sql.find("signalname=") + len("signalname='")
            end_index = sql.find("'", start_index)
            self.signalname = sql[start_index:end_index]
        else:
            str_and = ""
            list_and = {"hr": hr,
                        "httpheadervehicleversion": ver,
                        "messagenum": num,
                        "httpheadervid": vid,
                        "signalname": signal_name,
                        "sigvalue": signal_value,
                        }

            for i in list_and:
                if list_and[i] is not None:
                    str_and += " and {}='{}'".format(i, list_and[i])
            self.sql = "SELECT * from {table} WHERE dt='{dt}'{str_and} LIMIT {limit};".format(table=table_name, dt=dt,
                                                                                              str_and=str_and,
                                                                                              limit=limit)
        url = f"{self.server_name}/data-studio/editor/sqlexecute/validate"
        data = {"submitSource": "0",
                "sql": self.sql,
                "engine": "1",
                "queryScriptId": "2898",
                "submitId": self.submit_id,
                "execAccount": f"{self.user_name}"
                }
        logger.info(f"校验sql语句{self.sql}")
        self._post(url, data=data)
        self.submit_id = self.data.get("submitId")
        self.validate_status = self.data.get("validateStatus")

    def run_sql(self):
        """
        执行sql语句
        """
        url = f"{self.server_name}/data-studio/editor/sqlexecute/run"
        data = {"submitSource": "0",
                "sql": self.sql,
                "engine": "1",
                "queryScriptId": "2898",
                "submitId": self.submit_id,
                "execAccount": f"{self.user_name}"
                }
        logger.info(f"执行sql语句{self.sql}")
        self._post(url, data=data)

    def get_log(self):
        """
        获取执行日志
        """
        url = f"{self.server_name}/data-studio/editor/sqlexecute/log"
        data = {"submitId": self.submit_id,
                "runId": self.runid,
                "offset": "0"
                }
        self._post(url, data=data)
        self.runid = self.data.get("runId")
        self.has_result = self.data.get("hasResult")
        self.is_end = self.data.get("isEnd")
        self.status = self.data.get("status")

    def get_result(self):
        """
        获取执行结果
        """
        url = f"{self.server_name}/data-studio/editor/sqlexecute/result"
        data = {"pageIndex": 1,
                "pageSize": 500,
                "submitId": self.submit_id,
                "runId": self.runid,
                }
        self._post(url, data=data)
        self.has_result = self.data.get("hasResult")
        self.total_size = self.data.get("totalSize")
        logger.info(f"获取到{self.total_size}条结果")

    def download_result(self):
        """
        下载SQL执行结果到本地文件。

        Args:
            该函数没有显式传入参数，因为它依赖于类的属性，如self.server_name, self.submit_id, self.runid, self.user_name, self.password。

        Returns:
            str: 保存下载结果的本地文件名（包括.csv扩展名）。

        Raises:
            ValueError: 如果返回的content不是有效的bytes数据，则会引发此异常。
        """
        url = f"{self.server_name}/data-studio/editor/sqlexecute/downloadResult"
        download_file_name = f"{self.submit_id}-{self.runid}-result"
        data = {"format": "csv",
                "downloadFileName": download_file_name,
                "encoding": "UTF-8",
                "submitId": self.submit_id,
                "runId": self.runid,
                }
        headers = {
            "username": self.user_name,
            "access_token": get_passport_b_token("349a9e1ac04c44ad",
                                                 "904cae9755114eea8c19589e8ce7a215",
                                                 self.user_name,
                                                 self.password)
        }
        content = data_request.DataRequest().post(url, headers=headers, data=data, timeout=120)
        # 确保content是有效的bytes数据
        if not isinstance(content, bytes):
            raise ValueError("content不是有效的bytes数据")
        with open(f'{download_file_name}.csv', 'wb') as f:
            f.write(content)
        return f'{download_file_name}.csv'


def validate_result(table_name="ods.ods_data_jade_ee_signal_qa_staging_h", dt=None, hr=None, ver=None, vid=None,
                    num=None, limit=100000, document_id: str = "AmTTwCN0miv6g8kjbLhcE3MWnHf", sheet_ids: list = None,
                    length: int = 200, timeout: int = 600, wait_interval: int = 3, is_override: bool = True):
    """
        校验飞书表格中指定的信号值是否满足预期，并更新表格中的校验结果。

        Args:
            table_name (str, optional): 待校验的表格名称。默认为 "ods.ods_data_jade_ee_signal_qa_staging_h"。
            dt (str, optional): 日期字符串，格式为'YYYY-MM-DD'。校验时使用的日期。默认为None。
            hr (str, optional): 小时字符串，格式为'HH'。校验时使用的小时。默认为None。
            ver (str, optional): httpheadervehicleversion。校验时使用的版本号。默认为None。
            vid (str, optional): httpheadervid。校验时使用的vid值。默认为None。
            num (int, optional): messagenum。默认为None。
            limit (int, optional): SQL查询结果返回的最大行数。默认为100000。
            document_id (str, optional): 飞书表格的文档ID。默认为 "AmTTwCN0miv6g8kjbLhcE3MWnHf"。
            sheet_ids (list, optional): 待校验的表格ID列表。默认为None。
            length (int, optional): 表格中每页显示的行数。默认为200。
            timeout (int, optional): 等待日志查询操作超时的最大时间，单位为秒。默认为600秒。
            wait_interval (int, optional): 每次查询日志结果的等待时间间隔，单位为秒。默认为3秒。
            is_override (bool, optional): 是否覆盖已存在的校验结果。默认为True。

        Returns:
            None

        Raises:
            AssertionError: 当日志查询操作超时时抛出此异常。
        """

    # 获取飞书表格中内容
    feishu = feishu_api()
    feishu.get_app_access_token()
    feishu.get_user_access_token()
    feishu.get_bitable_app_access_token(document_id=document_id)
    token = feishu.app_access_token
    feishu.get_spreadsheets_info(spreadsheet_token=token)

    if sheet_ids is None:
        sheet_ids = feishu.sheet_ids
    for sheet_id in sheet_ids:
        index = 2
        values = feishu.get_spreadsheets_signal_value(spreadsheet_token=token, sheet_id=sheet_id, end=f"M{length}")
        for value in values:
            if value[0] is None or (not is_override and value[-1] is not None):
                continue
            # 获取sql执行语句的入参和校验值
            signal_name = value[0]
            node_name = value[4]
            signal_value = str(value[5])
            expection_value = str(value[6])
            # 开始执行sql语句进行校验
            Data = DataDev()
            Data.validate_sql(table_name=table_name, dt=dt, hr=hr, ver=ver, vid=vid, num=num,
                              signal_name=signal_name, signal_value=signal_value, limit=limit)
            Data.run_sql()
            start_time = time.time()
            flag = True
            while flag:
                elapsed_time = time.time() - start_time
                if elapsed_time >= timeout:
                    assert False, "日志查询操作超时"
                Data.get_log()
                time.sleep(wait_interval)
                if Data.has_result == 1 and Data.status == 2:
                    flag = False
            time.sleep(wait_interval)
            Data.get_result()
            # 回填前再次飞书获取token
            feishu = feishu_api()
            feishu.get_app_access_token()
            feishu.get_user_access_token()
            feishu.get_bitable_app_access_token(document_id=document_id)
            token = feishu.app_access_token
            if Data.has_result == 1 and Data.total_size > 0:
                if node_name.upper() == "BGM":
                    # 回填结果为pass
                    feishu.update_spreadsheets_value(spreadsheet_token=token, sheet_id=sheet_id, start=f"M{index}",
                                                     value=[[
                                                         f"PASS-BGM-{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]])
                else:
                    rows = Data.data["rowData"]
                    for row in rows:
                        if row[8] == signal_name:
                            # 校验结果
                            if row[10] == expection_value:
                                # 回填结果为pass
                                feishu.update_spreadsheets_value(spreadsheet_token=token, sheet_id=sheet_id,
                                                                 start=f"M{index}", value=[
                                        [f"PASS-{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]])
                                break
                            else:
                                # 回填结果为fail
                                feishu.update_spreadsheets_value(spreadsheet_token=token, sheet_id=sheet_id,
                                                                 start=f"M{index}", value=[[
                                        f"FAIL-查询到的value:{row[10]} {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]])
                                break
            else:
                # 回填结果为fail
                feishu.update_spreadsheets_value(spreadsheet_token=token, sheet_id=sheet_id, start=f"M{index}", value=[
                    [f"FAIL-SQL查询为空-{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]])

            index += 1


# 一次性验证全部结果
def validate_result_all(table_name="ods.ods_data_jade_ee_signal_qa_staging_h", dt=None, hr=None, ver=None, vid=None,
                        num=None, limit=100000, document_id: str = "AmTTwCN0miv6g8kjbLhcE3MWnHf",
                        sheet_ids: list = None,
                        length: int = 200, timeout: int = 600, wait_interval: int = 3, is_override: bool = True):
    """
        一次性校验飞书表格中指定的信号值是否满足预期，并更新表格中的校验结果。

        Args:
            table_name (str, optional): 待校验的表格名称。默认为 "ods.ods_data_jade_ee_signal_qa_staging_h"。
            dt (str, optional): 日期字符串，格式为'YYYY-MM-DD'。校验时使用的日期。默认为None。
            hr (str, optional): 小时字符串，格式为'HH'。校验时使用的小时。默认为None。
            ver (str, optional): httpheadervehicleversion。校验时使用的版本号。默认为None。
            vid (str, optional): httpheadervid。校验时使用的vid值。默认为None。
            num (int, optional): messagenum。默认为None。
            limit (int, optional): SQL查询结果返回的最大行数。默认为100000。
            document_id (str, optional): 飞书表格的文档ID。默认为 "AmTTwCN0miv6g8kjbLhcE3MWnHf"。
            sheet_ids (list, optional): 待校验的表格ID列表。默认为None。
            length (int, optional): 表格中每页显示的行数。默认为200。
            timeout (int, optional): 等待日志查询操作超时的最大时间，单位为秒。默认为600秒。
            wait_interval (int, optional): 每次查询日志结果的等待时间间隔，单位为秒。默认为3秒。
            is_override (bool, optional): 是否覆盖已存在的校验结果。默认为True。

        Returns:
            None

        Raises:
            AssertionError: 当日志查询操作超时时抛出此异常。
        """
    data = DataDev()
    data.validate_sql(table_name=table_name, dt=dt, hr=hr, ver=ver, vid=vid, num=num, limit=limit)
    data.run_sql()
    start_time = time.time()
    flag = True
    while flag:
        elapsed_time = time.time() - start_time
        if elapsed_time >= timeout:
            assert False, "日志查询操作超时"
        data.get_log()
        time.sleep(wait_interval)
        if data.has_result == 1 and data.status == 2:
            flag = False
    time.sleep(wait_interval)
    data.get_result()
    if data.has_result == 1 and data.total_size > 0:
        download_file_name = data.download_result()
        # if True:
        # 获取飞书表格中内容
        feishu = feishu_api()
        feishu.get_app_access_token()
        feishu.get_user_access_token()
        feishu.get_bitable_app_access_token(document_id=document_id)
        token = feishu.app_access_token
        feishu.get_spreadsheets_info(spreadsheet_token=token)
        if sheet_ids is None:
            sheet_ids = feishu.sheet_ids
        for sheet_id in sheet_ids:
            index = 2
            values = feishu.get_spreadsheets_signal_value(spreadsheet_token=token, sheet_id=sheet_id, end=f"M{length}")
            for value in values:
                # logger.info(f"#################################value: {value}")
                if value[0] is None or (not is_override and value[-1] is not None):
                    continue
                # 获取sql执行语句的入参和校验值
                signal_name = value[0]
                node_name = value[4]
                exception_value = str(value[6])
                found = False
                with open(download_file_name, 'r', newline='') as file:
                    reader = csv.DictReader(file)
                    rows = reader
                    for row in rows:
                        if row['signalname'] == signal_name:
                            # 校验结果
                            found = True
                            if node_name.upper() == "BGM":
                                feishu.update_spreadsheets_value(spreadsheet_token=token, sheet_id=sheet_id,
                                                                 start=f"M{index}",
                                                                 value=[[
                                                                     f"PASS-BGM-{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]])
                                index += 1
                                break
                            if row['sigvalue'] == exception_value:
                                # 回填结果为pass
                                feishu.update_spreadsheets_value(spreadsheet_token=token, sheet_id=sheet_id,
                                                                 start=f"M{index}", value=[
                                        [f"PASS-{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]])
                                index += 1
                                break
                            else:
                                # 回填结果为fail
                                feishu.update_spreadsheets_value(spreadsheet_token=token, sheet_id=sheet_id,
                                                                 start=f"M{index}", value=[[
                                        f"FAIL-查询到的value:{row['sigvalue']} {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]])
                                index += 1
                                break

                    if not found:
                        # 回填结果为fail
                        feishu.update_spreadsheets_value(spreadsheet_token=token, sheet_id=sheet_id,
                                                         start=f"M{index}", value=[
                                [f"FAIL-SQL查询为空-{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]])

                        index += 1
            # 回填下一张表格前再次飞书获取token
            feishu = feishu_api()
            feishu.get_app_access_token()
            feishu.get_user_access_token()
            feishu.get_bitable_app_access_token(document_id=document_id)
            token = feishu.app_access_token


# 调试用
if __name__ == "__main__":
    # 打印log示例
    logger = Logger().get_logger("test")
    validate_result_all(dt="2024-07-01", hr="15", vid="a598ecf7c03d7fa94d355e2175120cb7",
                        sheet_ids=["iK64lP", '3wbvCP'],
                        is_override=True)

#
