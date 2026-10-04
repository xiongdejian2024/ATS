 # -*- coding: utf-8 -*-
"""
@File        : test_uds_bgm_app.py
@Author      : o_wenyu.liang_ext@jiduauto.com
@Time        : 2022/11/17
@Description :

"""
import time
import pytest
import allure
import sys, os


project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

work_path_2 = os.path.join(os.getcwd().split("sat")[0], 'sat','ecu_simulator','interface')
sys.path.append(work_path_2)

work_path_3 = os.path.join(os.getcwd().split("sat")[0], 'sat','ecu_simulator','driver')
sys.path.append(work_path_3)



from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.case_helper.fota_case_helper.tsp_helper import Tsp_Helper
from xat_cases.legacy.bgm.case_helper.fota_case_helper.fota_operationn import *
 

from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.sdk.ecu_simulator_app import Ecu_Sim_App
from xat_ecu.legacy.interface.nuc_app import get_obd_ip
from xat_ecu.legacy.driver.ssh_client import SSHClient
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH
from xat_ecu.legacy.common.logmanagment.logmanager import *
from xat_cases.legacy.bgm.case_helper.diag_case_helper.DiagTestBase import *



# from ecu_simulator.sdk.get_obd_ip import get_announcement_ip


class Test(TestBase):
    def before_class(self, ecu):
        super().before_class(self,ecu)
    
        self.diagtest = DiagTestBase(self.ipdu,self.busapp)
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
 
    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        super().after_class(self, ecu)
    
    def test_bgm_log(self):
        self.diagtest.Get_Bgm_Log()
        
    def test_tcam_log(self):
        self.diagtest.Get_Tcam_Log()
        
    def test_L7(self):
        Constant = self.diagtest.Get_L7_Constant()
        logger.info("Constant={}".format(Constant))

    def test_Tcam_L7(self):
        Constant = self.diagtest.Get_Tcam_L7_Constant()
        logger.info("Constant={}".format(Constant))
        
    def test_version(self):
        self.diagtest.Get_BGM_Version()
        
    def test_Flash_Bgm(self):
        keyinfo = __import__("os").environ['XAT_CREDENTIAL_SCAN_6CAEDBEE8144A73014AE']
        file_url = "https://repo.jidudev.com/artifactory/BGMSoftware/Release/v1.1.0/6160110110AY/6160110110AY.bin"
        self.diagtest.Flash_Bgm(keyinfo,file_url)
        # self.diagtest.Flash()
        
    def test_Flash_Tcam(self):
        keyinfo = __import__("os").environ['XAT_CREDENTIAL_SCAN_02405C5118017C9C29B4']
        file_url = "https://repo.jidudev.com/artifactory/TCAMSoftware/Release/v1.1.0/6110110110AO/6110110110AO.bin"
        self.diagtest.Flash_Tcam(keyinfo,file_url)
        
    def test_clear_tcam_log(self):
        self.diagtest.Clear_TCAM_Log()
    
#pytest uds/test_tcam.py::Test::test_Flash_Tcam
