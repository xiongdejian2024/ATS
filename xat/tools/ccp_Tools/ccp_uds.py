import time
import pytest
import allure


import sys, os
from ccp_get import CCP_GET



project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)


 

# udsoncan.setup_logging()

class Ccp_Uds:
    def __init__(self,ccp):
        self.ccp = ccp
        self.b_cli = BGMDOIP()
        self.b_co = self.b_cli.conn("config/DoIPConfig_mcu.json")

    def send_ccp(self):
        self.b_cli.session_control(3)
        self.b_cli.write_data_by_identifier(0xF106,self.ccp)
        self.b_cli.close()

if __name__ == "__main__":
    #在ccp_tools目录下，执行python3 CCP_UDS
    ccp_get = Ccp_Get()   
    data = ccp_get.run()     #通过ccp.json读取解析后的自定义CCP数据
    ccp_uds  = Ccp_Uds(data)   
    ccp_uds.send_ccp()       #发送诊断命令 22 F106 自定义CCP数据 