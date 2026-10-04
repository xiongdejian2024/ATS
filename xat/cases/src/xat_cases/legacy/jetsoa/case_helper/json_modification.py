# -*- coding: utf-8 -*-
"""
@File        : Json_Modification.py
@Author      : jingjing.wang@jiduauto.com
@Time        : 2024/07/24 15:30
@Description :
@Examples    :
"""
import io
import json
from jsonpath_ng import parse as ng_parse
from xat_ecu.legacy.common.logger import logger


class JsonModification:
    
    def __init__(self, json_path) -> None:
        self.json_path = json_path
        self.raw_json_data = self.init_json_data()
    
    def init_json_data(self):
        with open(self.json_path, 'rb') as f:
            return json.load(f)

    def recover_json_data(self):
        try:
            with io.open(self.json_path, 'w', encoding='utf-8') as out:
                json.dump(
                    self.raw_json_data,
                    out,
                    indent=4,
                    ensure_ascii=False,
                    separators=(
                        ',',
                        ': '))
                out.write('\n')
        except FileNotFoundError as e:
            logger.warning(f"{e}")
            raise e
        except Exception as e:
            logger.warning(f"写入文件报错，{e}")
            raise e
        
    def update_json_data(self, update_field=None, new_value=None, new_path=None, own_data=None):
        """
        更新剧本文件字段值
        :param update_field: 更新字段的查找路径，如:$.data.list[0].treeList[0].nodeList[1].conditionExpressionList[0].extras.rightValue
        :param new_value: 更新字段的值，如：new_value=5
        :param new_path: 生成新的剧本文件路径，默认不传
        :param own_data: 自己改变后的dict数据，这个数据会直接更新到json文件里面
        :return:
        """

        with open(self.json_path, 'rb') as f:
            json_data = json.load(f)

        if own_data:
            json_data = own_data
        else:
            ng_parse(update_field).update(json_data, new_value)
        try:
            to_path = new_path if new_path else self.json_path
            with io.open(to_path, 'w', encoding='utf-8') as out:
                json.dump(
                    json_data,
                    out,
                    indent=4,
                    ensure_ascii=False,
                    separators=(
                        ',',
                        ': '))
                out.write('\n')
        except FileNotFoundError as e:
            logger.warning(f"{e}")
            raise e
        except Exception as e:
            logger.warning(f"写入文件报错，{e}")
            raise e