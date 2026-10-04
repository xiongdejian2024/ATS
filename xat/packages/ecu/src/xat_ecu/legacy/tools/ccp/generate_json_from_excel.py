"""
@File        : generate_json_from_excel.py
@Author      : wenyu.liang_ext@jiduauto.com
@Time        : 2023/04/24 
@Description :
@Examples    :
"""
import json
import os
import sys
import argparse

current_path = os.path.dirname(os.path.realpath(__file__))
import importlib
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.file_handle import FileHandle
from xat_ecu.legacy.config.path import CONFIG_DIR_PATH
import xlrd

class Generate_Json_From_Excel:
    def __init__(self,ccp_xlsx_path,veh_type,bl_ver):
       self.veh_type = veh_type
       self.bl_ver = bl_ver
       self.ccp_xlsx_path = ''
       self.ccp_json_path = ''
       self.version_path = ''
       self.ccp_xlsx_path = ccp_xlsx_path
       
    def generate(self):
        #
        self.version_path = "../sdk/data/{}/ccp/{}".format(self.veh_type, self.bl_ver)
        self.version_path = os.path.join(CONFIG_DIR_PATH ,self.version_path)

        # self.ccp_xlsx_path = "../sdk/data/{}/ccp/{}/ccp.xlsx".format(self.veh_type, self.bl_ver)
        # self.ccp_xlsx_path = os.path.join(CONFIG_DIR_PATH ,self.ccp_xlsx_path)
        
        self.ccp_json_path = "../sdk/data/{}/ccp/{}/ccp.json".format(self.veh_type, self.bl_ver)
        self.ccp_json_path = os.path.join(CONFIG_DIR_PATH ,self.ccp_json_path)
         
        if os.path.exists(self.version_path):
            logger.info('文件夹存在,无需生成文件夹')
            pass
        else:
            logger.info('文件夹不存在,生成对应版本{}文件夹'.format(self.bl_ver))
            os.mkdir(self.version_path)
        
        Excel_data = xlrd.open_workbook(self.ccp_xlsx_path)

        ccp_content = []  # 存放数据
            
        #根据ccp的excel文件生成对应的ccp的json文件以及内容字典
        #打开Excel文件
        #读取第一个工作表
        table = Excel_data.sheets()[0]
        # 统计行数
        rows = table.nrows
       
        for i in range(1, rows):
                values = table.row_values(i)
                ccp_content.append(
                    (
                        {
                                "字节序号": str(int(values[0])),
                                "参数类型": values[1],
                                "CCP英文描述":values[2],
                                "CCP中文描述":values[3],
                                "CCP取值":values[4],
                                "相关ECU":values[5],
                                "MarsOne_Useful": values[6],
                                "原车CCP值": values[7],
                                "原车CCP解析": values[8],
                                "待写入CCP值":values[9]
                        }
                    )
                )
        
        js = json.dumps(ccp_content, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ':'))
        with open(self.ccp_json_path, "w+", encoding='utf-8') as jsFile :
            jsFile.write(js)
        logger.info('Excel表对应Json文件创建成功'.format(self.bl_ver))
        
#work dir:/tools
#python3 ccp/generate_json_from_excel.py --ccp_xlsx_path='/root/wenyu.liang/ecu-simulator/xat_ecu/legacy/sdk/data/mars1/ccp/v_1_0_0/ccp.xlsx' --veh_type='mars1' --bl_ver='v_1_0_0'

if __name__ == '__main__':
    
    # parser = argparse.ArgumentParser(description='命令行中传入三个参数:按顺序分别是ccp文件路径,车辆类型，版本号')

    parser = argparse.ArgumentParser()
    parser.add_argument('--ccp_xlsx_path', type=str, help='ccp的excel文件的绝对路径')
    parser.add_argument('--veh_type', type=str, help='车辆类型')
    parser.add_argument('--bl_ver', type=str, help='车辆版本号')

    args = parser.parse_args()
    demo = Generate_Json_From_Excel(ccp_xlsx_path=args.ccp_xlsx_path,veh_type=args.veh_type,bl_ver=args.bl_ver)
    demo.generate()