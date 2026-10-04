#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_

"""
@File: ms_to_jama.py
@Time: 2023/06/13 11:07
@Author: lei.tao
@Software: PyCharm
@Description: 测试用例的需求覆盖率统计，检索用例的需求ID
@Examples:
"""

from ms_to_jama import *

class Coverage_statistics(object):
    def __init__(self) -> None:
        user = "ldap_soa_jama"
        passWord = __import__("os").environ.get('XAT_CREDENTIAL_ECU__INTERFACE_MS_REQUIREMENT_ID_STATISTICS_PY_PASSWORD', "")
        logger.info("登录MS!!")
        self.client = meterSphere_client(user, passWord)
        self.require_id = {"no_id": 0}
        
    def statistics_bgm(self, nodeIds, projectid):
        data = self.client.get_testcases_from_nodeIds(nodeIds, projectid)
        for i in range(len(data)):
            import ast
            flag = False
            Fields = ast.literal_eval(data[i]['customFields'].replace("null","None"))
            # logger.info(Fields)
            for j in Fields:
                if "需求ID" in dict(j).values():
                    try:
                        if j['value']:
                            flag = True
                            if "," in j['value']:
                                for a in [b for b in j['value'].split(",") if b != '']:
                                    if a not in self.require_id:
                                        self.require_id.update({a:1})
                                    else:
                                        self.require_id[a] += 1         
                            elif "，" in j['value']:
                                for a in [b for b in j['value'].split("，") if b != '']:
                                    if a not in self.require_id:
                                        self.require_id.update({a:1})
                                    else:
                                        self.require_id[a] += 1      
                            else:
                                if j['value'] not in self.require_id:
                                    self.require_id.update({j['value']:1})
                                else:
                                    self.require_id[j['value']] += 1
                    except Exception:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ms/requirement_id_statistics.py")
                        flag == False
                    finally:
                        break
                else:
                    continue   
            if flag == False:
                self.require_id['no_id'] += 1
                
        return self.require_id
                    
                    
if __name__ == '__main__':
    ss = Coverage_statistics()
    bgm_projectId = "6e14e1c5-aa15-4a44-b392-bdac2a4cc131"
    tcam_projectId = "f1d8bad3-4417-4e02-8b8d-28e583cd2e80"
    soa_projectId = "b325be5e-f19d-4937-8662-1b72458c9c0c"
    # nodeIds为空默认获取所有的测试用例
    result = ss.statistics_bgm(nodeIds=[], projectid=bgm_projectId)
    logger.info(f"BGM_MS中所有用例覆盖率统计{result}")
