# -*- coding: utf-8 -*-

"""
@Time    : 2024/07/01 17:26 下午
@Author  : songjian.lin
@Email   : songjian.lin@jiduauto.com
"""

import xmltodict
import json

from xat_ecu.legacy.common.logger import logger, Logger


def xml_to_json(xml_str: str):
    xml_parse = xmltodict.parse(xml_str)
    json_str = json.dumps(xml_parse, indent=4)
    return json_str


def json_to_xml(obj_dict: dict):
    # 使用 pretty=True 选项来输出格式化的 XML
    xml_str = xmltodict.unparse(obj_dict, pretty=True)
    return xml_str


def create_canoe_run_xml(canoe_vxt_module_file):
    """根据canoe的模版文件生成对应的xml文件"""
    with open(canoe_vxt_module_file, 'r') as f:
        xml_file = f.read()
        json_str1 = xml_to_json(xml_file)
        python_dict = json.loads(json_str1)
        for i in python_dict['testmodule']['testgroup']:
            if i['@title'] == 'Main Test':
                for j in i:
                    if j == 'capltestcase':
                        i.get(j).append({'@name': 'test_110004', '@title': 'test_110004', '@ident': 'TC-0004'})
                        break
        with open(XML_path[:-4] + '.xml', 'w') as new_file:
            new_file.write(json_to_xml(python_dict))


def parse_canoe_report_xml(canoe_report_xml):
    """解析canoe执行完成后生产的xml报告"""
    with open(canoe_report_xml, 'r') as f:
        xml_file = f.read()
        json_str1 = xml_to_json(xml_file)
        logger.info(json_str1)
        python_dict = json.loads(json_str1)
        if "testmodule" in python_dict:
            if "testgroup" in python_dict.get("testmodule"):
                for testcase in python_dict.get("testmodule").get("testgroup"):
                    if isinstance(testcase.get('testcase'), dict):
                        logger.info(f"{testcase.get('testcase').get('ident')}")
                        logger.info(f"{testcase.get('testcase').get('verdict').get('@result')}")
                        logger.info("----------------------------")
                    if isinstance(testcase.get('testcase'), list):
                        for case in testcase.get('testcase'):
                            logger.info(f"{case.get('ident')}")
                            logger.info(f"{case.get('description')}")
                            logger.info(f"{case.get('verdict').get('@result')}")
                            logger.info("----------------------------")


if __name__ == "__main__":
    logger = Logger().get_logger("test")

    # 读取canoe输入文件，并基于MS标签用例生成模板文件
    XML_path = "./CANoeDemo.vxt"
    create_canoe_run_xml(XML_path)

    # 解析canoe执行完成后生产的xml报告
    XML_path = "./CANoeDemo_report.xml"
    parse_canoe_report_xml(XML_path)

