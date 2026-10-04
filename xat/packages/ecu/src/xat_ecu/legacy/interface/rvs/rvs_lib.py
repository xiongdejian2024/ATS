# -*- coding: utf-8 -*-
"""
@File        : rvs_lib.py
@Author      : songjian.lin@jiduatuo.com
@Time        : 2024-03-06 15:06
@Description :
@Examples    :
"""
import datetime
import json
import os
import sys
import time

current_path = os.path.dirname(os.path.realpath(__file__))
from xat_ecu.legacy.common.constant import RVSConstant
from xat_ecu.legacy.common.logger import logger, Logger
import requests
import base64


class ES_client:
    def __init__(
            self,
            username=RVSConstant.RVS_USERNAME,
            password=RVSConstant.RVS_PASSWORD,
            server_name='https://log.jidustaging.com',
    ):
        self.username = base64.b64decode(username.encode()).decode()
        self.password = base64.b64decode(password.encode()).decode()
        self.server_name = server_name
        self.sid = None
        self.signin_flag = None
        self.query_id = None
        try:
            self.signin()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/rvs/rvs_lib.py")
            logger.error("登入 ES 失败: {}".format(e))

    def signin(self, path="/internal/security/login"):
        """
        登录 es 系统，获取 response Headers信息
        """
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-length': '53',
            'content-type': 'application/json',
            'cookie': 'jidu_device_id=76ffc892-3dfc-436a-9e41-8284a0d69f6d',
            'kbn-version': '7.9.3',
            'origin': 'https://log.jidustaging.com',
            'referer': r'https://log.jidustaging.com/login?msg=LOGGED_OUT',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            }
        data = {
            'username': self.username,
            'password': self.password
        }
        url = self.server_name + path
        self.sid = None
        self.signin_flag = None
        response = requests.post(url, json.dumps(data), headers=headers, timeout=5)
        resp_header = response.headers
        set_cookie = resp_header.get("set-cookie")
        # logger.info(f"resp_header:{resp_header}")
        if set_cookie:
            set_cookie_list = set_cookie.split(";")
        else:
            set_cookie_list = []
        for value in set_cookie_list:
            if "sid=" in value:
                self.sid = value.replace("sid=", "")
                # logger.info(f"获取到的sid为：{self.sid}，sid初始化成功！")
                self.signin_flag = True
                # logger.info("登录ES成功")
                break
        else:
            logger.info("登录ES失败")

    def query_newest_in_es(self, filter_list=None, rvs_db="jidulogapp-staging-vidb-report-data"):
        """
        根据过滤条件查询数据, 查询日期为当天

        @param filter_list: 查询条件列表
        @param rvs_db: 查询数据库
        """
        result_dict = {}
        filters_list = []
        if filter_list is not None:
            for filter1 in filter_list:
                filters_list.append({"multi_match": {"type": "best_fields", "query": f"{filter1}", "lenient": True}})

        if self.signin_flag:
            headers = {
                'Content-Type': "application/json; charset=utf-8",
                'accept-encoding': "gzip, deflate, br",
                'accept-language': "zh-CN,zh;q=0.9",
                'content-length': '85',
                'content-type': 'application/json',
                'cookie': f"jidu_device_id=76ffc892-3dfc-436a-9e41-8284a0d69f6d; sid={self.sid}",
                'kbn-version': '7.9.3',
                'origin': 'https://log.jidustaging.com',
                'referer': r'https://log.jidustaging.com/app/discover',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/86.0.4240.198 Safari/537.36',
            }
            today = datetime.datetime.now()
            today_str = today.strftime("%Y-%m-%d")
            yesterday = today - datetime.timedelta(days=1)
            yesterday_str = yesterday.strftime("%Y-%m-%d")

            data = {"params": {"ignoreThrottled": "true", "index": rvs_db,
                               "body": {"version": "true", "size": 300,
                                        "sort": [{"@timestamp": {"order": "desc", "unmapped_type": "boolean"}}],
                                        "aggs": {"2": {
                                            "date_histogram": {"field": "@timestamp", "fixed_interval": "30m",
                                                               "time_zone": "Asia/Shanghai", "min_doc_count": 1}}},
                                        "stored_fields": ["*"], "script_fields": {},
                                        "docvalue_fields": [{"field": "@timestamp", "format": "date_time"},
                                                            {"field": "filebeat_time", "format": "date_time"}],
                                        "_source": {"excludes": []}, "query": {"bool": {"must": [], "filter": [{
                                       "bool": {
                                           "filter": filters_list}},
                                       {
                                           "range": {
                                               "@timestamp": {
                                                   "gte": f"{yesterday_str}T16:00:00.000Z",
                                                   "lte": f"{today_str}T15:59:59.999Z",
                                                   "format": "strict_date_optional_time"}}}],
                                                                                        "should": [], "must_not": []}},
                                        "highlight": {"pre_tags": ["@kibana-highlighted-field@"],
                                                      "post_tags": ["@/kibana-highlighted-field@"], "fields": {"*": {}},
                                                      "fragment_size": 2147483647}}, "rest_total_hits_as_int": "true",
                               "ignore_unavailable": "true", "ignore_throttled": "true", "preference": 1709691870696,
                               "timeout": "30000ms"}}
            path = f"/internal/search/es"
            url = self.server_name + path
            response = requests.post(url, json.dumps(data), headers=headers, timeout=30)
            resp_header = response.headers
            set_cookie = resp_header.get("set-cookie")
            # logger.info(f"resp_header:{resp_header}")
            set_cookie_list = []
            if set_cookie:
                set_cookie_list = set_cookie.split(";")
            for value in set_cookie_list:
                if "sid=" in value:
                    self.sid = value.replace("sid=", "")
                    # logger.info(f"获取到的sid为：{self.sid}，sid更新成功！")
                    resp_body = json.loads(str(response.content, 'utf-8'))
                    time.sleep(2)
                    self.query_id = resp_body.get('id', None)
                    if self.query_id is None:
                        try:
                            record_count = resp_body.get("rawResponse").get("hits").get("total")
                            # logger.info(f"查询结果条数：{record_count}")
                            if record_count > 0:
                                result_dict = resp_body.get("rawResponse").get("hits").get("hits")[0]
                                logger.info(json.dumps(result_dict, ensure_ascii=False, indent=4))
                        except Exception as e:
                            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/rvs/rvs_lib.py")
                            logger.info(e)
                    else:
                        # logger.info(f"首次获取到的查询ID为{self.query_id}")
                        data = {"id": self.query_id}
                        response = requests.post(url, json.dumps(data), headers=headers, timeout=30)
                        resp_body = json.loads(str(response.content, 'utf-8'))
                        # logger.info("再次查询的结果：{}".format(resp_body.get("rawResponse").get("hits").get("total")))
                        try:
                            record_count = resp_body.get("rawResponse").get("hits").get("total")
                            # logger.info(f"查询结果条数：{record_count}")
                            if record_count > 0:
                                result_dict = resp_body.get("rawResponse").get("hits").get("hits")[0]
                                logger.info(json.dumps(result_dict, ensure_ascii=False, indent=4))
                        except Exception as e:
                            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/rvs/rvs_lib.py")
                            logger.info(e)
                    break

            return result_dict.get("_source").get("message")


def get_rvs_data(condition: list, rvs_db="jidulogapp-staging-vidb-report-data", retry_count=5):
    """
    根据查询条件查询rvs数据，数据类型列表，列表中的数据为字符串

    @param condition： 查询条件列表
    @param rvs_db: 查询数据库
    @param retry_count：查询失败最多重试次数
    """
    client = ES_client()
    result_dict = ""
    query_count = 1
    while query_count < retry_count:
        query_count += 1
        try:
            result_dict = client.query_newest_in_es(condition, rvs_db)
        except AttributeError:
            print("1")
            result_dict = client.query_newest_in_es(condition, rvs_db)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/rvs/rvs_lib.py")
            logger.info(type(e))
            result_dict = client.query_newest_in_es(condition, rvs_db)
        finally:
            if "##JIDU##" in result_dict:
                result_dict = result_dict.split("##JIDU##")[0]
                return eval(result_dict)
            else:
                return result_dict


if __name__ == '__main__':
    logger = Logger().get_logger("test")
    condition_list = ["51e5701381e5f796e7887e9bea1e87b9", "10103"]
    result = get_rvs_data(condition_list)
    logger.info(result)
    logger.info(result.get("createTimeMillis"))
