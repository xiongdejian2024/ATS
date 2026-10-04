"""
@File: ms_lib.py
@Time: 2022/11/16 14:00
@Author: songjian.lin
@Software: PyCharm
@Description: python 与 测试管理平台MeterSphere交互相关方法
@Examples:
"""
import json
import requests


def send_result_to_soa_platform(case_result, path="/s2sAutoTestResult/insert"):
    """
    pytest 执行的S2S自动化测试结果同步到 SOA测试平台
    """
    headers = {'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ' \
                             '(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
               'Content-Type': 'application/json;charset=utf-8', 'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9', 'Host': '10.80.51.28:8887'}
    data = {'bgmVersion': case_result.bgmVersion, 'jamaId': case_result.jamaId,
            'interfaceName': case_result.interfaceName, 'serviceName': case_result.serviceName,
            'functionName': case_result.functionName, 'functionType': case_result.functionType,
            'functionParameter': case_result.functionParameter, 'expectResult': case_result.expectResult,
            'realResult': str(case_result.realResult), 'autoCaseResult': case_result.autoCaseResult,
            'testcaseId': case_result.testcaseId, 'testcaseDescription': case_result.testcaseDescription,
            'jiraLink': case_result.jiraLink, 'updateTime': case_result.updateTime}
    url = "http://10.80.51.28:8887" + path
    response = requests.post(url, json.dumps(data), headers=headers)
    # resp_body = json.loads(str(response.content, 'utf-8'))
    # print("***************获取响应结果********************")
    # print(resp_body)
    # print("***************获取响应结果********************")
    # result = resp_body.get("msg")


class CaseResult:
    def __init__(self, bgmVersion, jamaId, interfaceName, serviceName,  functionName,
                 functionType, functionParameter, expectResult, realResult, autoCaseResult,
                 testcaseId, testcaseDescription, jiraLink, jidlVersion, updateTime="", uniq_id="", domain="BGM"):
        self.bgmVersion = bgmVersion
        self.jidlVersion = jidlVersion
        self.jamaId = jamaId
        self.interfaceName = interfaceName
        self.serviceName = serviceName
        self.functionName = functionName
        self.functionType = functionType
        self.functionParameter = functionParameter
        self.expectResult = expectResult
        self.realResult = realResult
        self.autoCaseResult = autoCaseResult
        self.testcaseId = testcaseId
        self.testcaseDescription = testcaseDescription  # 描述该自动化测试用例的测试概要信息
        self.jiraLink = jiraLink
        self.uniq_id = uniq_id
        self.updateTime = updateTime
        self.domain = domain

    def get_api_request_dict(self):
        """
        格式转换：SOA 测试平台数据格式  to API网站数据格式
        @return:
        """
        request_dict = {'origin_case_id': self.uniq_id, 'jidl_version': self.jidlVersion,
                        'bgm_version': self.bgmVersion, 'testcase_id': self.testcaseId,
                        'testcase_description': self.testcaseDescription, 'interface_name': self.interfaceName,
                        'service_name': self.serviceName, 'function_name': self.functionName,
                        'function_type': self.functionType, 'jama_id': self.jamaId,
                        'function_parameter': self.functionParameter, 'expect_result': self.expectResult,
                        'real_result': self.realResult, 'auto_case_result': self.autoCaseResult,
                        'jira_link': self.jiraLink, 'update_time': self.updateTime, 'domain': self.domain}
        # print("即将上传的测试数据：")
        # print(json.dumps(request_dict, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False))
        return request_dict


if __name__ == '__main__':
    testcase = CaseResult(bgmVersion='CD', jamaId="", interfaceName="获取座椅通风等级", serviceName='SeatService',
                          functionName='GetVentingLevel', functionType='method', functionParameter='{"name":1}',
                          expectResult='out:topPosition=4', realResult='out:topPosition=3', autoCaseResult='FAIL',
                          testcaseId='case004', testcaseDescription='测试用例描述信息', jiraLink='', jidlVersion='')
    send_result_to_soa_platform(testcase)
