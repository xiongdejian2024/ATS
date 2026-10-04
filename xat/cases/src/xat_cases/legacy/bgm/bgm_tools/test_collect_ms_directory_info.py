import os
import sys
import re
from time import sleep
import pytest
import allure
import openpyxl


sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from xat_ecu.legacy.interface.ms.ms_lib import *
from xat_ecu.legacy.interface.ms.ms_to_jama import *

class MS_Client(meterSphere_client):
    def get_testcase_id_from_ms():
        pass

class CollectCaseInfo(Upload):
    def get_caseid_and_tag(self,nodeIds, projectid):
        case_info = []
        res = self.client.get_testcases_from_nodeIds(nodeIds, projectid)
        for i in range(len(res)) :
            try:
                if "Not Applicable" in str(res[i].get('fields')):
                    print(f"--------------------> 'case_id': {res[i].get('num')} Not need automatical <----------------------------------------")
                    pass
                else:
                    case_info.append({'id': res[i].get('id'), 'case_id': res[i].get('num'),'jama_id': res[i].get('customNum'), 'nodeid': res[i].get('nodeId'), 'functionModule': res[i].get('nodePath'), 'tags': res[i].get('tags')})
            except Exception as e:
                print(f"'case_id': {res[i].get('num')} Error: ------------->{str(e)}")
                pass
        return case_info

    def get_ms_directory_info(self,nodeIds, projectid,directory_level):
        directory_ctrl = []
        directory_fota = []
        directory_mcu = []
        directory_basetech = []
        directory_cloud = []
        res = self.client.get_testcases_from_nodeIds(nodeIds, projectid)
        for i in range(len(res)) :
            try:
                if "Not Applicable" in str(res[i].get('fields')):
                    pass
                else:
                    directory_name = res[i].get('nodePath')
                    if directory_level == 1:
                        index = directory_name.find('/', directory_name.find('/') + 1)
                        directory_name = directory_name[:index+1]

                    elif directory_level == 2:
                        print(directory_name)
                        index = directory_name.find('/', directory_name.find('/', directory_name.find('/') + 1) + 1)
                        directory_name = directory_name[:index+1]
                    
                    elif directory_level == 3:
                        index = directory_name.find('/', directory_name.find('/', directory_name.find('/', directory_name.find('/') + 1) + 1) + 1)
                        directory_name = directory_name[:index+1]

                    if 'BGM车控车设' in str(directory_name) and directory_name not in directory_ctrl:
                        directory_ctrl.append(directory_name)
                    elif 'BGM FOTA用例' in  str(directory_name) and directory_name not in directory_fota:
                        directory_fota.append(directory_name)
                    elif 'BGM车云用例' in str(directory_name) and directory_name not in directory_cloud:
                        directory_cloud.append(directory_name)
                    elif str(directory_name).startswith('/BGM BaseTech') and directory_name not in directory_basetech:
                        directory_basetech.append(directory_name)
                    elif str(directory_name).startswith('/BGM_MCU') and directory_name not in directory_mcu:
                        directory_mcu.append(directory_name)
            except Exception as e:
                print(f"'case_id': {res[i].get('num')} Error: ------------->{str(e)}")
                pass
        print(directory_ctrl)
        print("------------------------------>")
        print(directory_fota)
        print("------------------------------>")
        print(directory_basetech)
        print("------------------------------>")
        print(directory_mcu)
        print("------------------------------>")
        print(directory_cloud)

if __name__ == "__main__":
    case_info = CollectCaseInfo()
    nodeIds = ["28c4aecb-b8b4-4df5-82f1-38a5bddefb40"]
    projectid = "1fbbeb47-6cc7-48bd-aafc-24349853e9d8" 
    # directory_info_list = case_info.get_ms_directory_info([], projectid,1)
    # print(directory_info_list)
    # level1_name = ['/BGM车控车设', '/BGM FOTA用例', '/BGM车云用例', '/BGM BaseTech', '/BGM_MCU', '/BGM性能稳定性', '/BGM实车功能点检']
    case_info.get_ms_directory_info([], projectid,2)
    # case_info.get_ms_directory_info([], projectid,3)
    # print(directory_info_list)
    