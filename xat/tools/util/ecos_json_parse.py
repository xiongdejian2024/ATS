# -*- coding: utf-8 -*-
"""
@File        : det_def.py
@Author      : songjian.lin@jiduauto.com
@Time        : 2022/12/26 22:43
@Description :
@Examples    :
"""
import json
import os

from xat_ecu.legacy.common.logger import Logger


def get_json_file_in_dir(dir_path):
    """
    获取目录下的所有的JSON文件
    """
    file_list = []
    if not os.path.exists(dir_path):
        logger.info(f"文件不存在")
        return
    listName = os.listdir(dir_path)
    for fileDirName in listName:
        abspath = os.path.join(dir_path, fileDirName)
        if os.path.isfile(abspath) and abspath.endswith('.json'):
            file_list.append(abspath)
        if os.path.isdir(abspath):
            file_list.extend(get_file_in_dir(abspath))
    return file_list


class test_result:
    """
    所有JSON文件的解析结果
    """
    def __init__(self):
        self.execute_count = 0
        self.fail_count = 0
        self.detail = {}  # key为大项名称,value为字典：包含两个键值对，一个key为fail_count，另一个key为detail：key为小项名称，value为时间列表

    def get_dict_result(self):
        fail_rate = self.fail_count * 100 / self.execute_count
        fail_rate_string = "%.2f" % fail_rate
        return {'整体失败率': fail_rate_string + "%", '失败明细': self.detail}


class signal_json_result:
    """
     单个json文件的解析结果
    """
    def __init__(self):
        self.run_result = "success"
        self.execute_time = ""
        self.detail = {}  # key为大项名称，value为列表，列表中的元素为小项名称

    def get_dict_result(self):
        return {'result': self.run_result, 'detail': self.detail}


def parse_ecos_json(file_path):
    result = signal_json_result()
    with open(file_path, "r", encoding='utf-8') as file_json:
        data = file_json.read()
        json_dict = json.loads(data)
        logger.info(json_dict['content'])
        logger.info(type(json_dict['content']))
        content_dict = eval(json_dict['content'])
        result.execute_time = content_dict['head']['测试时间']
        logger.info(content_dict['head']['测试时间'])
        logger.info(type(content_dict['body']))
        for key in content_dict['body']:
            logger.info(type(content_dict['body'][key]))
            if isinstance(content_dict['body'][key], dict):
                result.run_result = "fail"  # 测试大项执行失败
                logger.info(f"失败大项：{key}")
                result.detail[key] = []
                for sub_key in content_dict['body'][key]:
                    logger.info(f"  失败小项：{sub_key}")
                    result.detail[key].append(sub_key)
        else:
            logger.info(json.dumps(result.get_dict_result(), ensure_ascii=False, indent=4).
                        encode('utf-8').decode('utf-8'))
            return result


if __name__ == '__main__':
    logger = Logger().get_logger("test")
    result = test_result()
    # 后面通过 get_json_file_in_dir()，获取目录下所有的JSON文件
    json_file_list = ['15_37_00.json', '10_05_36.json', '10_05_36-2.json']
    for file_path in json_file_list:
        result_signal_json = parse_ecos_json(file_path)
        result.execute_count += 1
        if result_signal_json.run_result == 'fail':
            result.fail_count += 1
            for key_big in result_signal_json.detail:  # 遍历大项，字典类型
                if key_big not in result.detail:
                    result.detail[key_big] = {"fail_count": 0, "detail": {}}
                result.detail[key_big]["fail_count"] += 1  # 大项的失败次数加1
                for key_second in result_signal_json.detail[key_big]:  # 遍历当前大项下的小项，列表类型
                    if key_second not in result.detail[key_big]["detail"]:
                        result.detail[key_big]["detail"][key_second] = []
                    result.detail[key_big]["detail"][key_second].append(result_signal_json.execute_time)
    else:
        logger.info("======================================================================")
        logger.info(json.dumps(result.get_dict_result(), ensure_ascii=False, indent=4).
                    encode('utf-8').decode('utf-8'))
