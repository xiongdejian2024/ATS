#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : test_diag_basetech_didfunc.py
@time         : 2024/4/19 14:19
@author       : o_jingyuan.chen@external.jiduauto.com
@description  : 
'''''

import pytest
import allure
from xat_cases.legacy.basetech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature('BGM BaseTech/诊断功能')
class TestDIDFunc(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self,ecu)
        logger.info("before_class")
            
    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        logger.info("after_class")
        super().after_class(self, ecu)

    # @pytest.mark.full
    # @allure.story('DID功能测试')
    # @allure.title('F13F_子节点未回复')
    # def test_caseid_1986964(self):
    #     with allure.step(f"设置测试ECU的CCP值全有效"):
    #         self.sd_tester.write_multi_ccp({1305:0x02,1550:0x02,1343:0x02,1358:0x02,1306:0x02,1530:0x02,1327:0x02,1328:0x02,1391:0x02,1308:0x02,1455:0x02,1304:0x02,1322:0x02,1413:0x02,1532:0x02,1531:0x02})
    #     with allure.step(f"获取F13F的SN数据"):
    #         self.sn = self.sd_tester.send_request_and_recv_response([0x22,0xF1,0x3F],recv=f'62f13f{"ff"*288}')
    #         logger.info(f'获取到的SN真实值:{self.sn}')

    @pytest.mark.sanity
    @allure.story('DID功能测试')
    @allure.title('F13F_CCP值无效_在CCP变量中')
    def test_caseid_1986966(self):
        # self.bus_comm.recover_all_bus_signal_to_default()
        with allure.step(f"设置测试ECU的CCP值全无效"):
            self.sd_tester.write_multi_ccp({1305:0x01,1550:0x01,1343:0x01,1358:0x01,1306:0x01,1530:0x01,1327:0x01,1328:0x01,1391:0x01,1308:0x01,1455:0x01,1304:0x01,1322:0x01,1413:0x01,1532:0x01,1531:0x01})
        with allure.step(f"获取F13F的SN数据"):
            self.sn = self.sd_tester.send_request_and_recv_response([0x22,0xF1,0x3F],recv='62 F1 3F 18 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')
            logger.info(f'获取到的SN真实值:{self.sn}')

    @pytest.mark.full
    @allure.story('DID功能测试')
    @allure.title('F13F_CCP值无效_不在CCP变量中')
    def test_caseid_1986965(self):
        with allure.step(f"设置测试ECU的CCP值全无效"):
            self.sd_tester.write_multi_ccp({1305:0x03,1550:0x03,1343:0x03,1358:0x03,1306:0x03,1530:0x03,1327:0x03,1328:0x03,1391:0x03,1308:0x03,1455:0x03,1304:0x03,1322:0x03,1413:0x03,1532:0x03,1531:0x03})
        with allure.step(f"获取F13F的SN数据"):
            self.sn = self.sd_tester.send_request_and_recv_response([0x22,0xF1,0x3F],recv='62 F1 3F 18 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')
            logger.info(f'获取到的SN真实值:{self.sn}')

    @pytest.mark.smoke
    @allure.story('DID功能测试')
    @allure.title('F13F_CCP值有效')
    def test_caseid_1986967(self):
        with allure.step(f"设置测试ECU的CCP值全有效"):
            self.sd_tester.write_multi_ccp({1305:0x02,1550:0x02,1343:0x02,1358:0x02,1306:0x02,1530:0x02,1327:0x02,1328:0x02,1391:0x02,1308:0x02,1455:0x02,1304:0x02,1322:0x02,1413:0x02,1532:0x02,1531:0x02})
        with allure.step(f"模拟ASWMSN信号"):
            self.bus_comm.set('cem_lin4','AswmCem_Lin4SerNrFr01','ASWMSerNoNr1',0x00)
            self.bus_comm.set('cem_lin4','AswmCem_Lin4SerNrFr01','ASWMSerNoNr2',0xbc)
            self.bus_comm.set('cem_lin4','AswmCem_Lin4SerNrFr01','ASWMSerNoNr3',0x61)
            self.bus_comm.set('cem_lin4','AswmCem_Lin4SerNrFr01','ASWMSerNoNr4',0x4e)
        with allure.step(f"模拟HODSN信号"):
            self.bus_comm.set('cem_lin4','HodDim_Lin1SerNrFr01', 'HODSerNoNr1',0x01)
            self.bus_comm.set('cem_lin4','HodDim_Lin1SerNrFr01', 'HODSerNoNr2',0xbc)
            self.bus_comm.set('cem_lin4','HodDim_Lin1SerNrFr01', 'HODSerNoNr3',0x61)
            self.bus_comm.set('cem_lin4','HodDim_Lin1SerNrFr01', 'HODSerNoNr4',0x4e)
        with allure.step(f"模拟OHCSN信号"):
            self.bus_comm.set('cem_lin3','OhcCem_Lin3SerNrFr01', 'OHCSerNoNr1',0x03)
            self.bus_comm.set('cem_lin3','OhcCem_Lin3SerNrFr01', 'OHCSerNoNr2',0xbc)
            self.bus_comm.set('cem_lin3','OhcCem_Lin3SerNrFr01', 'OHCSerNoNr3',0x61)
            self.bus_comm.set('cem_lin3','OhcCem_Lin3SerNrFr01', 'OHCSerNoNr4',0x4e)
        with allure.step(f"模拟RLSMSN信号"):
            self.bus_comm.set('cem_lin1','RlsmCem_SerNrLin1Fr01', 'RLSMSerNoNr1',0x06)
            self.bus_comm.set('cem_lin1','RlsmCem_SerNrLin1Fr01', 'RLSMSerNoNr2',0xbc)
            self.bus_comm.set('cem_lin1','RlsmCem_SerNrLin1Fr01', 'RLSMSerNoNr3',0x61)
            self.bus_comm.set('cem_lin1','RlsmCem_SerNrLin1Fr01', 'RLSMSerNoNr4',0x4e)
        with allure.step(f"模拟TLSMSN信号"):
            self.bus_comm.set('cem_lin4','TlcmCem_Lin4SerNrFr01', 'TLCMSerNoNr1',0x02)
            self.bus_comm.set('cem_lin4','TlcmCem_Lin4SerNrFr01', 'TLCMSerNoNr2',0xbc)
            self.bus_comm.set('cem_lin4','TlcmCem_Lin4SerNrFr01', 'TLCMSerNoNr3',0x61)
            self.bus_comm.set('cem_lin4','TlcmCem_Lin4SerNrFr01', 'TLCMSerNoNr4',0x4e)
        with allure.step(f"模拟FCSISN信号"):
            self.bus_comm.set('cem_lin2','FcsiEcm_Lin4SerNrFr01', 'FCSISerNoNr1',0x0a)
            self.bus_comm.set('cem_lin2','FcsiEcm_Lin4SerNrFr01', 'FCSISerNoNr2',0xbc)
            self.bus_comm.set('cem_lin2','FcsiEcm_Lin4SerNrFr01', 'FCSISerNoNr3',0x61)
            self.bus_comm.set('cem_lin2','FcsiEcm_Lin4SerNrFr01', 'FCSISerNoNr4',0x4e)
        with allure.step(f"模拟AIILLSN信号"):
            self.bus_comm.set('cem_lin2','AiillEcm_Lin4SerNrFr01', 'AIILLSerNoNr1',0x0b)
            self.bus_comm.set('cem_lin2','AiillEcm_Lin4SerNrFr01', 'AIILLSerNoNr2',0xbc)
            self.bus_comm.set('cem_lin2','AiillEcm_Lin4SerNrFr01', 'AIILLSerNoNr3',0x61)
            self.bus_comm.set('cem_lin2','AiillEcm_Lin4SerNrFr01', 'AIILLSerNoNr4',0x4e)
        with allure.step(f"模拟AIILRSN信号"):
            self.bus_comm.set('cem_lin2','AiilrEcm_Lin4SerNrFr01', 'AIILRSerNoNr1',0x0c)
            self.bus_comm.set('cem_lin2','AiilrEcm_Lin4SerNrFr01', 'AIILRSerNoNr2',0xbc)
            self.bus_comm.set('cem_lin2','AiilrEcm_Lin4SerNrFr01', 'AIILRSerNoNr3',0x61)
            self.bus_comm.set('cem_lin2','AiilrEcm_Lin4SerNrFr01', 'AIILRSerNoNr4',0x4e)
        with allure.step(f"模拟WMMSN信号"):
            self.bus_comm.set('cem_lin1','WmmCem_Lin1SerNrFr01', 'WMMSerNoNr1',0x09)
            self.bus_comm.set('cem_lin1','WmmCem_Lin1SerNrFr01', 'WMMSerNoNr2',0xbc)
            self.bus_comm.set('cem_lin1','WmmCem_Lin1SerNrFr01', 'WMMSerNoNr3',0x61)
            self.bus_comm.set('cem_lin1','WmmCem_Lin1SerNrFr01', 'WMMSerNoNr4',0x4e)
        with allure.step(f"模拟BMSSN信号"):
            self.bus_comm.set('cem_lin6','BmsCem_Lin6SerNrFr01', 'NrSerlBMSNr1',0x07)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6SerNrFr01', 'NrSerlBMSNr2',0xbc)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6SerNrFr01', 'NrSerlBMSNr3',0x61)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6SerNrFr01', 'NrSerlBMSNr4',0x4e)
        with allure.step(f"模拟AWMSN信号"):
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','AWMSerNoNr1',0x11)
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01', 'AWMSerNoNr2',0xbc)
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01', 'AWMSerNoNr3',0x61)
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01', 'AWMSerNoNr4',0x4e)
        with allure.step(f"模拟PRLDSN信号"):
            self.bus_comm.set('cem_lin2','PrldCem_Lin2SerNoFr01', 'PRLDSerNoNr1',0x0d)
            self.bus_comm.set('cem_lin2','PrldCem_Lin2SerNoFr01', 'PRLDSerNoNr2',0xbc)
            self.bus_comm.set('cem_lin2','PrldCem_Lin2SerNoFr01', 'PRLDSerNoNr3',0x61)
            self.bus_comm.set('cem_lin2','PrldCem_Lin2SerNoFr01', 'PRLDSerNoNr4',0x4e)
        with allure.step(f"模拟IRMMSN信号"):
            self.bus_comm.set('cem_lin1','IrmmCem_Lin1SerNrFr01', 'SerNoIRMMNr1',0x08)
            self.bus_comm.set('cem_lin1','IrmmCem_Lin1SerNrFr01', 'SerNoIRMMNr2',0xbc)
            self.bus_comm.set('cem_lin1','IrmmCem_Lin1SerNrFr01', 'SerNoIRMMNr3',0x61)
            self.bus_comm.set('cem_lin1','IrmmCem_Lin1SerNrFr01', 'SerNoIRMMNr4',0x4e)
        with allure.step(f"模拟DSGLSN信号"):
            self.bus_comm.set('cem_lin3','DsglCem_Lin3SerNrFr01', 'DSGLSerNoNr1',0x04)
            self.bus_comm.set('cem_lin3','DsglCem_Lin3SerNrFr01', 'DSGLSerNoNr2',0xbc)
            self.bus_comm.set('cem_lin3','DsglCem_Lin3SerNrFr01', 'DSGLSerNoNr3',0x61)
            self.bus_comm.set('cem_lin3','DsglCem_Lin3SerNrFr01', 'DSGLSerNoNr4',0x4e)
        with allure.step(f"模拟PSGLSN信号"):
            self.bus_comm.set('cem_lin3','PsglCem_Lin3SerNrFr01', 'PSGLSerNoNr1',0x05)
            self.bus_comm.set('cem_lin3','PsglCem_Lin3SerNrFr01', 'PSGLSerNoNr2',0xbc)
            self.bus_comm.set('cem_lin3','PsglCem_Lin3SerNrFr01', 'PSGLSerNoNr3',0x61)
            self.bus_comm.set('cem_lin3','PsglCem_Lin3SerNrFr01', 'PSGLSerNoNr4',0x4e)
        with allure.step(f"获取F13F的SN数据"):
            self.sn = self.sd_tester.send_request_and_recv_response([0x22,0xF1,0x3F],recv='62 F1 3F 18 00 00 00 00 00 00 00 00 00 bc 61 4e 00 00 00 00 00 00 00 00 01 bc 61 4e 00 00 00 00 00 00 00 00 03 bc 61 4e 00 00 00 00 00 00 00 00 06 bc 61 4e 00 00 00 00 00 00 00 00 02 bc 61 4e 00 00 00 00 00 00 00 00 0a bc 61 4e 00 00 00 00 00 00 00 00 0b bc 61 4e 00 00 00 00 00 00 00 00 0c bc 61 4e 00 00 00 00 00 00 00 00 09 bc 61 4e 00 00 00 00 00 00 00 00 07 bc 61 4e 00 00 00 00 00 00 00 00 11 bc 61 4e 00 00 00 00 00 00 00 00 0d bc 61 4e ff ff ff ff ff ff ff ff ff ff ff ff 00 00 00 00 00 00 00 00 08 bc 61 4e 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 04 bc 61 4e 00 00 00 00 00 00 00 00 05 bc 61 4e')
            logger.info(f'获取到的SN真实值:{self.sn}')


    # @pytest.mark.full
    # @allure.story('DID功能测试')
    # @allure.title('F1BB_子节点未回复')
    # def test_caseid_1986959(self):
    #     with allure.step(f"设置测试ECU的CCP值全有效"):
    #         self.sd_tester.write_multi_ccp({1305:0x02,1550:0x02,1343:0x02,1358:0x02,1306:0x02,1530:0x02,1327:0x02,1328:0x02,1391:0x02,1308:0x02,1455:0x02,1304:0x02,1322:0x02,1413:0x02,1532:0x02,1531:0x02})
    #     with allure.step(f"获取F1BB的SN数据"):
    #         self.pn = self.sd_tester.send_request_and_recv_response([0x22,0xF1,0xBB],recv=f'62f1bb{"ff"*216}')
    #         logger.info(f'获取到的PN真实值:{self.pn}')

    @pytest.mark.smoke
    @allure.story('DID功能测试')
    @allure.title('F1BB_CCP值有效_版本后缀1个字母')
    def test_caseid_1986963(self):
        with allure.step(f"设置测试ECU的CCP值全有效"):
            self.sd_tester.write_multi_ccp({1305:0x02,1550:0x02,1343:0x02,1358:0x02,1306:0x02,1530:0x02,1327:0x02,1328:0x02,1391:0x02,1308:0x02,1455:0x02,1304:0x02,1322:0x02,1413:0x02,1532:0x02,1531:0x02})
        with allure.step(f"模拟ASWMPN信号"):
            self.bus_comm.set('cem_lin4','AswmCem_Lin4PartNrFr05','ASWMPartNo10CmplNr1',0x01)
            self.bus_comm.set('cem_lin4','AswmCem_Lin4PartNrFr05','ASWMPartNo10CmplNr2',0x23)
            self.bus_comm.set('cem_lin4','AswmCem_Lin4PartNrFr05','ASWMPartNo10CmplNr3',0x45)
            self.bus_comm.set('cem_lin4','AswmCem_Lin4PartNrFr05','ASWMPartNo10CmplNr4',0x67)
            self.bus_comm.set('cem_lin4','AswmCem_Lin4PartNrFr05','ASWMPartNo10CmplNr5',0x89)
            self.bus_comm.set('cem_lin4','AswmCem_Lin4PartNrFr05','ASWMPartNo10CmplEndSgn1',0x20)
            self.bus_comm.set('cem_lin4','AswmCem_Lin4PartNrFr05','ASWMPartNo10CmplEndSgn2',0x20)
            self.bus_comm.set('cem_lin4','AswmCem_Lin4PartNrFr05','ASWMPartNo10CmplEndSgn3',0x41)
        with allure.step(f"模拟HODPN信号"):
            self.bus_comm.set('cem_lin4','HodDim_Lin1PartNrFr02', 'HODPartNo10CmplEndSgn1',0x20)
            self.bus_comm.set('cem_lin4','HodDim_Lin1PartNrFr02', 'HODPartNo10CmplEndSgn2',0x20)
            self.bus_comm.set('cem_lin4','HodDim_Lin1PartNrFr02', 'HODPartNo10CmplEndSgn3',0x41)
            self.bus_comm.set('cem_lin4','HodDim_Lin1PartNrFr02', 'HODPartNo10CmplNr1',0x01)
            self.bus_comm.set('cem_lin4','HodDim_Lin1PartNrFr02', 'HODPartNo10CmplNr2',0xbc)
            self.bus_comm.set('cem_lin4','HodDim_Lin1PartNrFr02', 'HODPartNo10CmplNr3',0x61)
            self.bus_comm.set('cem_lin4','HodDim_Lin1PartNrFr02', 'HODPartNo10CmplNr4',0x4e)
            self.bus_comm.set('cem_lin4','HodDim_Lin1PartNrFr02', 'HODPartNo10CmplNr5',0x89)
        with allure.step(f"模拟OHCPN信号"):
            self.bus_comm.set('cem_lin3','OhcCem_Lin3PartNrFr04', 'OHCPartNo10CmplNr1',0x03)
            self.bus_comm.set('cem_lin3','OhcCem_Lin3PartNrFr04', 'OHCPartNo10CmplNr2',0xbc)
            self.bus_comm.set('cem_lin3','OhcCem_Lin3PartNrFr04', 'OHCPartNo10CmplNr3',0x61)
            self.bus_comm.set('cem_lin3','OhcCem_Lin3PartNrFr04', 'OHCPartNo10CmplNr4',0x4e)
            self.bus_comm.set('cem_lin3','OhcCem_Lin3PartNrFr04', 'OHCPartNo10CmplNr5',0x89)
            self.bus_comm.set('cem_lin3','OhcCem_Lin3PartNrFr04', 'OHCPartNo10CmplEndSgn1',0x20)
            self.bus_comm.set('cem_lin3','OhcCem_Lin3PartNrFr04', 'OHCPartNo10CmplEndSgn2',0x20)
            self.bus_comm.set('cem_lin3','OhcCem_Lin3PartNrFr04', 'OHCPartNo10CmplEndSgn3',0x41)
        with allure.step(f"模拟RLSMPN信号"):
            self.bus_comm.set('cem_lin1','RlsmCem_Lin1PartNrFr02', 'RLSMPartNo10EndSgn1',0x20)
            self.bus_comm.set('cem_lin1','RlsmCem_Lin1PartNrFr02', 'RLSMPartNo10EndSgn2',0x20)
            self.bus_comm.set('cem_lin1','RlsmCem_Lin1PartNrFr02', 'RLSMPartNo10EndSgn3',0x41)
            self.bus_comm.set('cem_lin1','RlsmCem_Lin1PartNrFr02', 'RLSMPartNo10Nr1',0x06)
            self.bus_comm.set('cem_lin1','RlsmCem_Lin1PartNrFr02', 'RLSMPartNo10Nr2',0xbc)
            self.bus_comm.set('cem_lin1','RlsmCem_Lin1PartNrFr02', 'RLSMPartNo10Nr3',0x61)
            self.bus_comm.set('cem_lin1','RlsmCem_Lin1PartNrFr02', 'RLSMPartNo10Nr4',0x4e)
            self.bus_comm.set('cem_lin1','RlsmCem_Lin1PartNrFr02', 'RLSMPartNo10Nr5',0x89)
        with allure.step(f"模拟TLSMPN信号"):
            self.bus_comm.set('cem_lin4','TlcmCem_Lin4PartNrFr01', 'TLCMPartNo10CmplNr1',0x02)
            self.bus_comm.set('cem_lin4','TlcmCem_Lin4PartNrFr01', 'TLCMPartNo10CmplNr2',0xbc)
            self.bus_comm.set('cem_lin4','TlcmCem_Lin4PartNrFr01', 'TLCMPartNo10CmplNr3',0x61)
            self.bus_comm.set('cem_lin4','TlcmCem_Lin4PartNrFr01', 'TLCMPartNo10CmplNr4',0x4e)
            self.bus_comm.set('cem_lin4','TlcmCem_Lin4PartNrFr01', 'TLCMPartNo10CmplNr5',0x89)
            self.bus_comm.set('cem_lin4','TlcmCem_Lin4PartNrFr01', 'TLCMPartNo10CmplEndSgn1',0x20)
            self.bus_comm.set('cem_lin4','TlcmCem_Lin4PartNrFr01', 'TLCMPartNo10CmplEndSgn2',0x20)
            self.bus_comm.set('cem_lin4','TlcmCem_Lin4PartNrFr01', 'TLCMPartNo10CmplEndSgn3',0x41)
        with allure.step(f"模拟FCSIPN信号"):
            self.bus_comm.set('cem_lin2','FcsiEcm_Lin4PartNrFr04', 'FCSIPartNo10CmplNr1',0x0a)
            self.bus_comm.set('cem_lin2','FcsiEcm_Lin4PartNrFr04', 'FCSIPartNo10CmplNr2',0xbc)
            self.bus_comm.set('cem_lin2','FcsiEcm_Lin4PartNrFr04', 'FCSIPartNo10CmplNr3',0x61)
            self.bus_comm.set('cem_lin2','FcsiEcm_Lin4PartNrFr04', 'FCSIPartNo10CmplNr4',0x4e)
            self.bus_comm.set('cem_lin2','FcsiEcm_Lin4PartNrFr04', 'FCSIPartNo10CmplNr5',0x89)
            self.bus_comm.set('cem_lin2','FcsiEcm_Lin4PartNrFr04', 'FCSIPartNo10CmplEndSgn1',0x20)
            self.bus_comm.set('cem_lin2','FcsiEcm_Lin4PartNrFr04', 'FCSIPartNo10CmplEndSgn2',0x20)
            self.bus_comm.set('cem_lin2','FcsiEcm_Lin4PartNrFr04', 'FCSIPartNo10CmplEndSgn3',0x41)
        with allure.step(f"模拟AIILLPN信号"):
            self.bus_comm.set('cem_lin2','AiillEcm_Lin4PartNrFr01', 'AIILLPartNo10CmplNr1',0x0b)
            self.bus_comm.set('cem_lin2','AiillEcm_Lin4PartNrFr01', 'AIILLPartNo10CmplNr2',0xbc)
            self.bus_comm.set('cem_lin2','AiillEcm_Lin4PartNrFr01', 'AIILLPartNo10CmplNr3',0x61)
            self.bus_comm.set('cem_lin2','AiillEcm_Lin4PartNrFr01', 'AIILLPartNo10CmplNr4',0x4e)
            self.bus_comm.set('cem_lin2','AiillEcm_Lin4PartNrFr01', 'AIILLPartNo10CmplNr5',0x89)
            self.bus_comm.set('cem_lin2','AiillEcm_Lin4PartNrFr01', 'AIILLPartNo10CmplEndSgn1',0x20)
            self.bus_comm.set('cem_lin2','AiillEcm_Lin4PartNrFr01', 'AIILLPartNo10CmplEndSgn2',0x20)
            self.bus_comm.set('cem_lin2','AiillEcm_Lin4PartNrFr01', 'AIILLPartNo10CmplEndSgn3',0x41)
        with allure.step(f"模拟AIILRPN信号"):
            self.bus_comm.set('cem_lin2','AiilrEcm_Lin4PartNrFr01', 'AIILRPartNo10CmplNr1',0x0c)
            self.bus_comm.set('cem_lin2','AiilrEcm_Lin4PartNrFr01', 'AIILRPartNo10CmplNr2',0xbc)
            self.bus_comm.set('cem_lin2','AiilrEcm_Lin4PartNrFr01', 'AIILRPartNo10CmplNr3',0x61)
            self.bus_comm.set('cem_lin2','AiilrEcm_Lin4PartNrFr01', 'AIILRPartNo10CmplNr4',0x4e)
            self.bus_comm.set('cem_lin2','AiilrEcm_Lin4PartNrFr01', 'AIILRPartNo10CmplNr5',0x89)
            self.bus_comm.set('cem_lin2','AiilrEcm_Lin4PartNrFr01', 'AIILRPartNo10CmplEndSgn1',0x20)
            self.bus_comm.set('cem_lin2','AiilrEcm_Lin4PartNrFr01', 'AIILRPartNo10CmplEndSgn2',0x20)
            self.bus_comm.set('cem_lin2','AiilrEcm_Lin4PartNrFr01', 'AIILRPartNo10CmplEndSgn3',0x41)
        with allure.step(f"模拟WMMPN信号"):
            self.bus_comm.set('cem_lin1','WmmCem_Lin1PartNrFr02', 'WMMPartNo10EndSgn1',0x20)
            self.bus_comm.set('cem_lin1','WmmCem_Lin1PartNrFr02', 'WMMPartNo10EndSgn2',0x20)
            self.bus_comm.set('cem_lin1','WmmCem_Lin1PartNrFr02', 'WMMPartNo10EndSgn3',0x41)
            self.bus_comm.set('cem_lin1','WmmCem_Lin1PartNrFr02', 'WMMPartNo10Nr1',0x09)
            self.bus_comm.set('cem_lin1','WmmCem_Lin1PartNrFr02', 'WMMPartNo10Nr2',0xbc)
            self.bus_comm.set('cem_lin1','WmmCem_Lin1PartNrFr02', 'WMMPartNo10Nr3',0x61)
            self.bus_comm.set('cem_lin1','WmmCem_Lin1PartNrFr02', 'WMMPartNo10Nr4',0x4e)
            self.bus_comm.set('cem_lin1','WmmCem_Lin1PartNrFr02', 'WMMPartNo10Nr5',0x89)
        with allure.step(f"模拟BMSPN1信号"):
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr05', 'PartNo10ApplBMSNr1',0x07)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr05', 'PartNo10ApplBMSNr2',0xbc)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr05', 'PartNo10ApplBMSNr3',0x61)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr05', 'PartNo10ApplBMSNr4',0x4e)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr05', 'PartNo10ApplBMSNr5',0x89)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr05', 'PartNo10ApplBMSEndSgn1',0x20)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr05', 'PartNo10ApplBMSEndSgn2',0x20)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr05', 'PartNo10ApplBMSEndSgn3',0x41)
        with allure.step(f"模拟BMSPN2信号"):
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr06', 'PartNo10ApplDiagBMSEndSgn1',0x20)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr06', 'PartNo10ApplDiagBMSEndSgn2',0x20)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr06', 'PartNo10ApplDiagBMSEndSgn3',0x41)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr06', 'PartNo10ApplDiagBMSNr1',0x07)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr06', 'PartNo10ApplDiagBMSNr2',0xbc)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr06', 'PartNo10ApplDiagBMSNr3',0x61)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr06', 'PartNo10ApplDiagBMSNr4',0x4e)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr06', 'PartNo10ApplDiagBMSNr5',0x89)
        with allure.step(f"模拟BMSPN3有效信号"):
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr07', 'PartNo10BMSEndSgn1',0x20)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr07', 'PartNo10BMSEndSgn2',0x20)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr07', 'PartNo10BMSEndSgn3',0x41)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr07', 'PartNo10BMSNr1',0x07)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr07', 'PartNo10BMSNr2',0xbc)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr07', 'PartNo10BMSNr3',0x61)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr07', 'PartNo10BMSNr4',0x4e)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr07', 'PartNo10BMSNr5',0x89)
        with allure.step(f"模拟BMSPN4信号"):
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr08', 'PartNo10HwBMSEndSgn1',0x20)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr08', 'PartNo10HwBMSEndSgn2',0x20)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr08', 'PartNo10HwBMSEndSgn3',0x41)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr08', 'PartNo10HwBMSNr1',0x07)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr08', 'PartNo10HwBMSNr2',0xbc)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr08', 'PartNo10HwBMSNr3',0x61)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr08', 'PartNo10HwBMSNr4',0x4e)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr08', 'PartNo10HwBMSNr5',0x89)
        with allure.step(f"模拟AWMPN信号"):
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr02', 'AWMPartNo10CmplEndSgn1',0x20)
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr02', 'AWMPartNo10CmplEndSgn2',0x20)
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr02', 'AWMPartNo10CmplEndSgn3',0x41)
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr02', 'AWMPartNo10CmplNr1',0x11)
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr02', 'AWMPartNo10CmplNr2',0xbc)
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr02', 'AWMPartNo10CmplNr3',0x61)
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr02', 'AWMPartNo10CmplNr4',0x4e)
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr02', 'AWMPartNo10CmplNr5',0x89)
        with allure.step(f"模拟PRLDPN信号"):
            self.bus_comm.set('cem_lin2','PrldCem_Lin2PartNoFr01', 'PRLDPartNo10CmplNr1',0x0d)
            self.bus_comm.set('cem_lin2','PrldCem_Lin2PartNoFr01', 'PRLDPartNo10CmplNr2',0xbc)
            self.bus_comm.set('cem_lin2','PrldCem_Lin2PartNoFr01', 'PRLDPartNo10CmplNr3',0x61)
            self.bus_comm.set('cem_lin2','PrldCem_Lin2PartNoFr01', 'PRLDPartNo10CmplNr4',0x4e)
            self.bus_comm.set('cem_lin2','PrldCem_Lin2PartNoFr01', 'PRLDPartNo10CmplNr5',0x89)
            self.bus_comm.set('cem_lin2','PrldCem_Lin2PartNoFr01', 'PRLDPartNo10CmplEndSgn1',0x20)
            self.bus_comm.set('cem_lin2','PrldCem_Lin2PartNoFr01', 'PRLDPartNo10CmplEndSgn2',0x20)
            self.bus_comm.set('cem_lin2','PrldCem_Lin2PartNoFr01', 'PRLDPartNo10CmplEndSgn3',0x41)
        with allure.step(f"模拟IRMMPN信号"):
            self.bus_comm.set('cem_lin1','IrmmCem_Lin1PartNrFr02', 'PartNo10IRMMEndSgn1',0x20)
            self.bus_comm.set('cem_lin1','IrmmCem_Lin1PartNrFr02', 'PartNo10IRMMEndSgn2',0x20)
            self.bus_comm.set('cem_lin1','IrmmCem_Lin1PartNrFr02', 'PartNo10IRMMEndSgn3',0x41)
            self.bus_comm.set('cem_lin1','IrmmCem_Lin1PartNrFr02', 'PartNo10IRMMNr1',0x08)
            self.bus_comm.set('cem_lin1','IrmmCem_Lin1PartNrFr02', 'PartNo10IRMMNr2',0xbc)
            self.bus_comm.set('cem_lin1','IrmmCem_Lin1PartNrFr02', 'PartNo10IRMMNr3',0x61)
            self.bus_comm.set('cem_lin1','IrmmCem_Lin1PartNrFr02', 'PartNo10IRMMNr4',0x4e)
            self.bus_comm.set('cem_lin1','IrmmCem_Lin1PartNrFr02', 'PartNo10IRMMNr4',0x89)
        with allure.step(f"模拟DSGLPN信号"):
            self.bus_comm.set('cem_lin3','DsglCem_Lin3PartNrFr01', 'DSGLPartNo10CmplNr1',0x04)
            self.bus_comm.set('cem_lin3','DsglCem_Lin3PartNrFr01', 'DSGLPartNo10CmplNr2',0xbc)
            self.bus_comm.set('cem_lin3','DsglCem_Lin3PartNrFr01', 'DSGLPartNo10CmplNr3',0x61)
            self.bus_comm.set('cem_lin3','DsglCem_Lin3PartNrFr01', 'DSGLPartNo10CmplNr4',0x4e)
            self.bus_comm.set('cem_lin3','DsglCem_Lin3PartNrFr01', 'DSGLPartNo10CmplNr5',0x89)
            self.bus_comm.set('cem_lin3','DsglCem_Lin3PartNrFr01', 'DSGLPartNo10CmplEndSgn1',0x20)
            self.bus_comm.set('cem_lin3','DsglCem_Lin3PartNrFr01', 'DSGLPartNo10CmplEndSgn2',0x20)
            self.bus_comm.set('cem_lin3','DsglCem_Lin3PartNrFr01', 'DSGLPartNo10CmplEndSgn3',0x41)
        with allure.step(f"模拟PSGLpN信号"):
            self.bus_comm.set('cem_lin3','PsglCem_Lin3PartNrFr01', 'PSGLPartNo10CmplNr1',0x05)
            self.bus_comm.set('cem_lin3','PsglCem_Lin3PartNrFr01', 'PSGLPartNo10CmplNr2',0xbc)
            self.bus_comm.set('cem_lin3','PsglCem_Lin3PartNrFr01', 'PSGLPartNo10CmplNr3',0x61)
            self.bus_comm.set('cem_lin3','PsglCem_Lin3PartNrFr01', 'PSGLPartNo10CmplNr4',0x4e)
            self.bus_comm.set('cem_lin3','PsglCem_Lin3PartNrFr01', 'PSGLPartNo10CmplNr5',0x89)
            self.bus_comm.set('cem_lin3','PsglCem_Lin3PartNrFr01', 'PSGLPartNo10CmplEndSgn1',0x20)
            self.bus_comm.set('cem_lin3','PsglCem_Lin3PartNrFr01', 'PSGLPartNo10CmplEndSgn2',0x20)
            self.bus_comm.set('cem_lin3','PsglCem_Lin3PartNrFr01', 'PSGLPartNo10CmplEndSgn3',0x41)
        with allure.step(f"获取F13F的SN数据"):
            self.pn = self.sd_tester.send_request_and_recv_response([0x22,0xF1,0xBB],recv='62F1BB1B012345678920204101BC614E8920204103BC614E8920204106BC614E8920204102BC614E892020410ABC614E892020410BBC614E892020410CBC614E8920204109BC614E8920204107BC614E8920204107BC614E8920204107BC614E8920204107BC614E8920204111BC614E892020410DBC614E89202041FFFFFFFFFFFFFFFF08BC6189002020410000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004bc614e8920204105bc614e89202041')
            logger.info(f'获取到的PN真实值:{self.pn}')

    @pytest.mark.smoke
    @allure.story('DID功能测试')
    @allure.title('F1BB_CCP值有效_版本后缀2个字母')
    def test_caseid_1986962(self):
        with allure.step(f"设置测试ECU的CCP值全有效"):
            self.sd_tester.write_multi_ccp({1305:0x02,1550:0x02,1343:0x02,1358:0x02,1306:0x02,1530:0x02,1327:0x02,1328:0x02,1391:0x02,1308:0x02,1455:0x02,1304:0x02,1322:0x02,1413:0x02,1532:0x02,1531:0x02})
        with allure.step(f"模拟ASWMPN信号"):
            self.bus_comm.set('cem_lin4','AswmCem_Lin4PartNrFr05','ASWMPartNo10CmplNr1',0x01)
            self.bus_comm.set('cem_lin4','AswmCem_Lin4PartNrFr05','ASWMPartNo10CmplNr2',0x23)
            self.bus_comm.set('cem_lin4','AswmCem_Lin4PartNrFr05','ASWMPartNo10CmplNr3',0x45)
            self.bus_comm.set('cem_lin4','AswmCem_Lin4PartNrFr05','ASWMPartNo10CmplNr4',0x67)
            self.bus_comm.set('cem_lin4','AswmCem_Lin4PartNrFr05','ASWMPartNo10CmplNr5',0x89)
            self.bus_comm.set('cem_lin4','AswmCem_Lin4PartNrFr05','ASWMPartNo10CmplEndSgn1',0x20)
            self.bus_comm.set('cem_lin4','AswmCem_Lin4PartNrFr05','ASWMPartNo10CmplEndSgn2',0x42)
            self.bus_comm.set('cem_lin4','AswmCem_Lin4PartNrFr05','ASWMPartNo10CmplEndSgn3',0x41)
        with allure.step(f"模拟HODPN信号"):
            self.bus_comm.set('cem_lin4','HodDim_Lin1PartNrFr02', 'HODPartNo10CmplEndSgn1',0x20)
            self.bus_comm.set('cem_lin4','HodDim_Lin1PartNrFr02', 'HODPartNo10CmplEndSgn2',0x42)
            self.bus_comm.set('cem_lin4','HodDim_Lin1PartNrFr02', 'HODPartNo10CmplEndSgn3',0x41)
            self.bus_comm.set('cem_lin4','HodDim_Lin1PartNrFr02', 'HODPartNo10CmplNr1',0x01)
            self.bus_comm.set('cem_lin4','HodDim_Lin1PartNrFr02', 'HODPartNo10CmplNr2',0xbc)
            self.bus_comm.set('cem_lin4','HodDim_Lin1PartNrFr02', 'HODPartNo10CmplNr3',0x61)
            self.bus_comm.set('cem_lin4','HodDim_Lin1PartNrFr02', 'HODPartNo10CmplNr4',0x4e)
            self.bus_comm.set('cem_lin4','HodDim_Lin1PartNrFr02', 'HODPartNo10CmplNr5',0x89)
        with allure.step(f"模拟OHCPN信号"):
            self.bus_comm.set('cem_lin3','OhcCem_Lin3PartNrFr04', 'OHCPartNo10CmplNr1',0x03)
            self.bus_comm.set('cem_lin3','OhcCem_Lin3PartNrFr04', 'OHCPartNo10CmplNr2',0xbc)
            self.bus_comm.set('cem_lin3','OhcCem_Lin3PartNrFr04', 'OHCPartNo10CmplNr3',0x61)
            self.bus_comm.set('cem_lin3','OhcCem_Lin3PartNrFr04', 'OHCPartNo10CmplNr4',0x4e)
            self.bus_comm.set('cem_lin3','OhcCem_Lin3PartNrFr04', 'OHCPartNo10CmplNr5',0x89)
            self.bus_comm.set('cem_lin3','OhcCem_Lin3PartNrFr04', 'OHCPartNo10CmplEndSgn1',0x20)
            self.bus_comm.set('cem_lin3','OhcCem_Lin3PartNrFr04', 'OHCPartNo10CmplEndSgn2',0x42)
            self.bus_comm.set('cem_lin3','OhcCem_Lin3PartNrFr04', 'OHCPartNo10CmplEndSgn3',0x41)
        with allure.step(f"模拟RLSMPN信号"):
            self.bus_comm.set('cem_lin1','RlsmCem_Lin1PartNrFr02', 'RLSMPartNo10EndSgn1',0x20)
            self.bus_comm.set('cem_lin1','RlsmCem_Lin1PartNrFr02', 'RLSMPartNo10EndSgn2',0x42)
            self.bus_comm.set('cem_lin1','RlsmCem_Lin1PartNrFr02', 'RLSMPartNo10EndSgn3',0x41)
            self.bus_comm.set('cem_lin1','RlsmCem_Lin1PartNrFr02', 'RLSMPartNo10Nr1',0x06)
            self.bus_comm.set('cem_lin1','RlsmCem_Lin1PartNrFr02', 'RLSMPartNo10Nr2',0xbc)
            self.bus_comm.set('cem_lin1','RlsmCem_Lin1PartNrFr02', 'RLSMPartNo10Nr3',0x61)
            self.bus_comm.set('cem_lin1','RlsmCem_Lin1PartNrFr02', 'RLSMPartNo10Nr4',0x4e)
            self.bus_comm.set('cem_lin1','RlsmCem_Lin1PartNrFr02', 'RLSMPartNo10Nr5',0x89)
        with allure.step(f"模拟TLSMPN信号"):
            self.bus_comm.set('cem_lin4','TlcmCem_Lin4PartNrFr01', 'TLCMPartNo10CmplNr1',0x02)
            self.bus_comm.set('cem_lin4','TlcmCem_Lin4PartNrFr01', 'TLCMPartNo10CmplNr2',0xbc)
            self.bus_comm.set('cem_lin4','TlcmCem_Lin4PartNrFr01', 'TLCMPartNo10CmplNr3',0x61)
            self.bus_comm.set('cem_lin4','TlcmCem_Lin4PartNrFr01', 'TLCMPartNo10CmplNr4',0x4e)
            self.bus_comm.set('cem_lin4','TlcmCem_Lin4PartNrFr01', 'TLCMPartNo10CmplNr5',0x89)
            self.bus_comm.set('cem_lin4','TlcmCem_Lin4PartNrFr01', 'TLCMPartNo10CmplEndSgn1',0x20)
            self.bus_comm.set('cem_lin4','TlcmCem_Lin4PartNrFr01', 'TLCMPartNo10CmplEndSgn2',0x42)
            self.bus_comm.set('cem_lin4','TlcmCem_Lin4PartNrFr01', 'TLCMPartNo10CmplEndSgn3',0x41)
        with allure.step(f"模拟FCSIPN信号"):
            self.bus_comm.set('cem_lin2','FcsiEcm_Lin4PartNrFr04', 'FCSIPartNo10CmplNr1',0x0a)
            self.bus_comm.set('cem_lin2','FcsiEcm_Lin4PartNrFr04', 'FCSIPartNo10CmplNr2',0xbc)
            self.bus_comm.set('cem_lin2','FcsiEcm_Lin4PartNrFr04', 'FCSIPartNo10CmplNr3',0x61)
            self.bus_comm.set('cem_lin2','FcsiEcm_Lin4PartNrFr04', 'FCSIPartNo10CmplNr4',0x4e)
            self.bus_comm.set('cem_lin2','FcsiEcm_Lin4PartNrFr04', 'FCSIPartNo10CmplNr5',0x89)
            self.bus_comm.set('cem_lin2','FcsiEcm_Lin4PartNrFr04', 'FCSIPartNo10CmplEndSgn1',0x20)
            self.bus_comm.set('cem_lin2','FcsiEcm_Lin4PartNrFr04', 'FCSIPartNo10CmplEndSgn2',0x42)
            self.bus_comm.set('cem_lin2','FcsiEcm_Lin4PartNrFr04', 'FCSIPartNo10CmplEndSgn3',0x41)
        with allure.step(f"模拟AIILLPN信号"):
            self.bus_comm.set('cem_lin2','AiillEcm_Lin4PartNrFr01', 'AIILLPartNo10CmplNr1',0x0b)
            self.bus_comm.set('cem_lin2','AiillEcm_Lin4PartNrFr01', 'AIILLPartNo10CmplNr2',0xbc)
            self.bus_comm.set('cem_lin2','AiillEcm_Lin4PartNrFr01', 'AIILLPartNo10CmplNr3',0x61)
            self.bus_comm.set('cem_lin2','AiillEcm_Lin4PartNrFr01', 'AIILLPartNo10CmplNr4',0x4e)
            self.bus_comm.set('cem_lin2','AiillEcm_Lin4PartNrFr01', 'AIILLPartNo10CmplNr5',0x89)
            self.bus_comm.set('cem_lin2','AiillEcm_Lin4PartNrFr01', 'AIILLPartNo10CmplEndSgn1',0x20)
            self.bus_comm.set('cem_lin2','AiillEcm_Lin4PartNrFr01', 'AIILLPartNo10CmplEndSgn2',0x42)
            self.bus_comm.set('cem_lin2','AiillEcm_Lin4PartNrFr01', 'AIILLPartNo10CmplEndSgn3',0x41)
        with allure.step(f"模拟AIILRPN信号"):
            self.bus_comm.set('cem_lin2','AiilrEcm_Lin4PartNrFr01', 'AIILRPartNo10CmplNr1',0x0c)
            self.bus_comm.set('cem_lin2','AiilrEcm_Lin4PartNrFr01', 'AIILRPartNo10CmplNr2',0xbc)
            self.bus_comm.set('cem_lin2','AiilrEcm_Lin4PartNrFr01', 'AIILRPartNo10CmplNr3',0x61)
            self.bus_comm.set('cem_lin2','AiilrEcm_Lin4PartNrFr01', 'AIILRPartNo10CmplNr4',0x4e)
            self.bus_comm.set('cem_lin2','AiilrEcm_Lin4PartNrFr01', 'AIILRPartNo10CmplNr5',0x89)
            self.bus_comm.set('cem_lin2','AiilrEcm_Lin4PartNrFr01', 'AIILRPartNo10CmplEndSgn1',0x20)
            self.bus_comm.set('cem_lin2','AiilrEcm_Lin4PartNrFr01', 'AIILRPartNo10CmplEndSgn2',0x42)
            self.bus_comm.set('cem_lin2','AiilrEcm_Lin4PartNrFr01', 'AIILRPartNo10CmplEndSgn3',0x41)
        with allure.step(f"模拟WMMPN信号"):
            self.bus_comm.set('cem_lin1','WmmCem_Lin1PartNrFr02', 'WMMPartNo10EndSgn1',0x20)
            self.bus_comm.set('cem_lin1','WmmCem_Lin1PartNrFr02', 'WMMPartNo10EndSgn2',0x42)
            self.bus_comm.set('cem_lin1','WmmCem_Lin1PartNrFr02', 'WMMPartNo10EndSgn3',0x41)
            self.bus_comm.set('cem_lin1','WmmCem_Lin1PartNrFr02', 'WMMPartNo10Nr1',0x09)
            self.bus_comm.set('cem_lin1','WmmCem_Lin1PartNrFr02', 'WMMPartNo10Nr2',0xbc)
            self.bus_comm.set('cem_lin1','WmmCem_Lin1PartNrFr02', 'WMMPartNo10Nr3',0x61)
            self.bus_comm.set('cem_lin1','WmmCem_Lin1PartNrFr02', 'WMMPartNo10Nr4',0x4e)
            self.bus_comm.set('cem_lin1','WmmCem_Lin1PartNrFr02', 'WMMPartNo10Nr5',0x89)
        with allure.step(f"模拟BMSPN1信号"):
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr05', 'PartNo10ApplBMSNr1',0x07)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr05', 'PartNo10ApplBMSNr2',0xbc)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr05', 'PartNo10ApplBMSNr3',0x61)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr05', 'PartNo10ApplBMSNr4',0x4e)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr05', 'PartNo10ApplBMSNr5',0x89)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr05', 'PartNo10ApplBMSEndSgn1',0x20)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr05', 'PartNo10ApplBMSEndSgn2',0x42)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr05', 'PartNo10ApplBMSEndSgn3',0x41)
        with allure.step(f"模拟BMSPN2信号"):
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr06', 'PartNo10ApplDiagBMSEndSgn1',0x20)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr06', 'PartNo10ApplDiagBMSEndSgn2',0x42)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr06', 'PartNo10ApplDiagBMSEndSgn3',0x41)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr06', 'PartNo10ApplDiagBMSNr1',0x07)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr06', 'PartNo10ApplDiagBMSNr2',0xbc)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr06', 'PartNo10ApplDiagBMSNr3',0x61)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr06', 'PartNo10ApplDiagBMSNr4',0x4e)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr06', 'PartNo10ApplDiagBMSNr5',0x89)
        with allure.step(f"模拟BMSPN3有效信号"):
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr07', 'PartNo10BMSEndSgn1',0x20)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr07', 'PartNo10BMSEndSgn2',0x42)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr07', 'PartNo10BMSEndSgn3',0x41)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr07', 'PartNo10BMSNr1',0x07)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr07', 'PartNo10BMSNr2',0xbc)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr07', 'PartNo10BMSNr3',0x61)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr07', 'PartNo10BMSNr4',0x4e)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr07', 'PartNo10BMSNr5',0x89)
        with allure.step(f"模拟BMSPN4信号"):
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr08', 'PartNo10HwBMSEndSgn1',0x20)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr08', 'PartNo10HwBMSEndSgn2',0x42)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr08', 'PartNo10HwBMSEndSgn3',0x41)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr08', 'PartNo10HwBMSNr1',0x07)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr08', 'PartNo10HwBMSNr2',0xbc)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr08', 'PartNo10HwBMSNr3',0x61)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr08', 'PartNo10HwBMSNr4',0x4e)
            self.bus_comm.set('cem_lin6','BmsCem_Lin6PartNrFr08', 'PartNo10HwBMSNr5',0x89)
        with allure.step(f"模拟AWMPN信号"):
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr02', 'AWMPartNo10CmplEndSgn1',0x20)
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr02', 'AWMPartNo10CmplEndSgn2',0x42)
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr02', 'AWMPartNo10CmplEndSgn3',0x41)
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr02', 'AWMPartNo10CmplNr1',0x11)
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr02', 'AWMPartNo10CmplNr2',0xbc)
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr02', 'AWMPartNo10CmplNr3',0x61)
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr02', 'AWMPartNo10CmplNr4',0x4e)
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr02', 'AWMPartNo10CmplNr5',0x89)
        with allure.step(f"模拟PRLDPN信号"):
            self.bus_comm.set('cem_lin2','PrldCem_Lin2PartNoFr01', 'PRLDPartNo10CmplNr1',0x0d)
            self.bus_comm.set('cem_lin2','PrldCem_Lin2PartNoFr01', 'PRLDPartNo10CmplNr2',0xbc)
            self.bus_comm.set('cem_lin2','PrldCem_Lin2PartNoFr01', 'PRLDPartNo10CmplNr3',0x61)
            self.bus_comm.set('cem_lin2','PrldCem_Lin2PartNoFr01', 'PRLDPartNo10CmplNr4',0x4e)
            self.bus_comm.set('cem_lin2','PrldCem_Lin2PartNoFr01', 'PRLDPartNo10CmplNr5',0x89)
            self.bus_comm.set('cem_lin2','PrldCem_Lin2PartNoFr01', 'PRLDPartNo10CmplEndSgn1',0x20)
            self.bus_comm.set('cem_lin2','PrldCem_Lin2PartNoFr01', 'PRLDPartNo10CmplEndSgn2',0x42)
            self.bus_comm.set('cem_lin2','PrldCem_Lin2PartNoFr01', 'PRLDPartNo10CmplEndSgn3',0x41)
        with allure.step(f"模拟IRMMPN信号"):
            self.bus_comm.set('cem_lin1','IrmmCem_Lin1PartNrFr02', 'PartNo10IRMMEndSgn1',0x20)
            self.bus_comm.set('cem_lin1','IrmmCem_Lin1PartNrFr02', 'PartNo10IRMMEndSgn2',0x42)
            self.bus_comm.set('cem_lin1','IrmmCem_Lin1PartNrFr02', 'PartNo10IRMMEndSgn3',0x41)
            self.bus_comm.set('cem_lin1','IrmmCem_Lin1PartNrFr02', 'PartNo10IRMMNr1',0x08)
            self.bus_comm.set('cem_lin1','IrmmCem_Lin1PartNrFr02', 'PartNo10IRMMNr2',0xbc)
            self.bus_comm.set('cem_lin1','IrmmCem_Lin1PartNrFr02', 'PartNo10IRMMNr3',0x61)
            self.bus_comm.set('cem_lin1','IrmmCem_Lin1PartNrFr02', 'PartNo10IRMMNr4',0x4e)
            self.bus_comm.set('cem_lin1','IrmmCem_Lin1PartNrFr02', 'PartNo10IRMMNr4',0x89)
        with allure.step(f"模拟DSGLPN信号"):
            self.bus_comm.set('cem_lin3','DsglCem_Lin3PartNrFr01', 'DSGLPartNo10CmplNr1',0x04)
            self.bus_comm.set('cem_lin3','DsglCem_Lin3PartNrFr01', 'DSGLPartNo10CmplNr2',0xbc)
            self.bus_comm.set('cem_lin3','DsglCem_Lin3PartNrFr01', 'DSGLPartNo10CmplNr3',0x61)
            self.bus_comm.set('cem_lin3','DsglCem_Lin3PartNrFr01', 'DSGLPartNo10CmplNr4',0x4e)
            self.bus_comm.set('cem_lin3','DsglCem_Lin3PartNrFr01', 'DSGLPartNo10CmplNr5',0x89)
            self.bus_comm.set('cem_lin3','DsglCem_Lin3PartNrFr01', 'DSGLPartNo10CmplEndSgn1',0x20)
            self.bus_comm.set('cem_lin3','DsglCem_Lin3PartNrFr01', 'DSGLPartNo10CmplEndSgn2',0x42)
            self.bus_comm.set('cem_lin3','DsglCem_Lin3PartNrFr01', 'DSGLPartNo10CmplEndSgn3',0x41)
        with allure.step(f"模拟PSGLpN信号"):
            self.bus_comm.set('cem_lin3','PsglCem_Lin3PartNrFr01', 'PSGLPartNo10CmplNr1',0x05)
            self.bus_comm.set('cem_lin3','PsglCem_Lin3PartNrFr01', 'PSGLPartNo10CmplNr2',0xbc)
            self.bus_comm.set('cem_lin3','PsglCem_Lin3PartNrFr01', 'PSGLPartNo10CmplNr3',0x61)
            self.bus_comm.set('cem_lin3','PsglCem_Lin3PartNrFr01', 'PSGLPartNo10CmplNr4',0x4e)
            self.bus_comm.set('cem_lin3','PsglCem_Lin3PartNrFr01', 'PSGLPartNo10CmplNr5',0x89)
            self.bus_comm.set('cem_lin3','PsglCem_Lin3PartNrFr01', 'PSGLPartNo10CmplEndSgn1',0x20)
            self.bus_comm.set('cem_lin3','PsglCem_Lin3PartNrFr01', 'PSGLPartNo10CmplEndSgn2',0x42)
            self.bus_comm.set('cem_lin3','PsglCem_Lin3PartNrFr01', 'PSGLPartNo10CmplEndSgn3',0x41)
        with allure.step(f"获取F1BB的SN数据"):
            self.pn = self.sd_tester.send_request_and_recv_response([0x22,0xF1,0xBB],recv='62 F1 BB 1B 01 23 45 67 89 20 42 41 01 BC 61 4E 89 20 42 41 03 BC 61 4E 89 20 42 41 06 BC 61 4E 89 20 42 41 02 BC 61 4E 89 20 42 41 0A BC 61 4E 89 20 42 41 0B BC 61 4E 89 20 42 41 0C BC 61 4E 89 20 42 41 09 BC 61 4E 89 20 42 41 07 BC 61 4E 89 20 42 41 07 BC 61 4E 89 20 42 41 07 BC 61 4E 89 20 42 41 07 BC 61 4E 89 20 42 41 11 BC 61 4E 89 20 42 41 0D BC 61 4E 89 20 42 41 FF FF FF FF FF FF FF FF 08 BC 61 89 00 20 42 41 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 04 bc 61 4e 89 20 42 41 05 bc 61 4e 89 20 42 41')
            logger.info(f'获取到的PN真实值:{self.pn}')

    @pytest.mark.sanity
    @allure.story('DID功能测试')
    @allure.title('F1BB_CCP值无效_在CCP变量中')
    def test_caseid_1986961(self):
        with allure.step(f"设置测试ECU的CCP值全无效"):
            self.sd_tester.write_multi_ccp({1305:0x01,1550:0x01,1343:0x01,1358:0x01,1306:0x01,1530:0x01,1327:0x01,1328:0x01,1391:0x01,1308:0x01,1455:0x01,1304:0x01,1322:0x01,1413:0x01,1532:0x01,1531:0x01})
        with allure.step(f"获取F1BB的SN数据"):
            self.pn = self.sd_tester.send_request_and_recv_response([0x22,0xF1,0xBB],recv='62 F1 BB 1B 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')
            logger.info(f'获取到的SN真实值:{self.pn}')

    @pytest.mark.full
    @allure.story('DID功能测试')
    @allure.title('F1BB_CCP值无效_不在CCP变量中')
    def test_caseid_1986960(self):
        with allure.step(f"设置测试ECU的CCP值全无效"):
            self.sd_tester.write_multi_ccp({1305:0x03,1550:0x03,1343:0x03,1358:0x03,1306:0x03,1530:0x03,1327:0x03,1328:0x03,1391:0x03,1308:0x03,1455:0x03,1304:0x03,1322:0x03,1413:0x03,1532:0x03,1531:0x03})
        with allure.step(f"获取F1BB的SN数据"):
            self.pn = self.sd_tester.send_request_and_recv_response([0x22,0xF1,0xBB],recv='62 F1 BB 1B 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')
            logger.info(f'获取到的PN真实值:{self.pn}')


    # @pytest.mark.full
    # @allure.story('DID功能测试')
    # @allure.title('Snapshot DID_E30056')
    # def test_caseid_1986(self):
    #     with allure.step(f"读取快照组信息"):
    #         self.tdistance=self.sd_tester.read_did_and_check(TA.BGM_MCU,0xdd01,SESSION.EMPTY,'62dd01')
    #         self.vbv=self.sd_tester.read_did_and_check(TA.BGM_MCU,0xdd02,SESSION.EMPTY,'62dd02')
    #     with allure.step(f"置为当前DTC"):
    #         self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
    #         self.sd_tester.write_ccp({1:0xa4})
    #         self.sd_tester.change_usage_mode(UsageMode.CONVENIENCE)
    #         sleep(5)
    #         self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x22,0x42,0x9e],[0x62,0x42,0x9e,0x00])
    #         self.elpower=self.sd_tester.read_did_and_check(TA.BGM_MCU,0xdd0c,SESSION.EMPTY,'62dd0c0f')
    #         self.time=self.sd_tester.read_did_and_check(TA.BGM_MCU,0xdd00,SESSION.EMPTY,'62dd00')
    #         self.snapdid=self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],'5904e300562f2005')
    #         logger.info(f'快照信息为：{self.snapdid}')
    #         self.sd_tester.reset_0x1181()
    #         self.time=self.sd_tester.read_did_and_check(TA.BGM_MCU,0xdd00,SESSION.EMPTY,'62dd00')
    #         self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
    #         sleep(5)
    #         self.time=self.sd_tester.read_did_and_check(TA.BGM_MCU,0xdd00,SESSION.EMPTY,'62dd00')
    #         self.snapdid=self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],'5904e300562f2005')
    #     with allure.step(f"置为历史DTC"):
    #         self.sd_tester.write_ccp({1:0xa3})
    #         self.sd_tester.change_usage_mode(UsageMode.CONVENIENCE)
    #         time.sleep(5)
    #         self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56,0x2c])
    #         self.sd_tester.reset_0x1181()
    #         self.sd_tester.change_usage_mode(UsageMode.CONVENIENCE)
    #         sleep(5)
    #         self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56,0x00])


    # @pytest.mark.full
    # @allure.story('DID功能测试')
    # @allure.title('Snapshot DID_D11587')
    # def test_caseid_198700001(self):
    #     self.mix.set_dtc_precontion()
    #     self.bus_comm.pause_ecu_send('backbonefr','ACU')
    #     time.sleep(5)
    #     self.sd_tester.send_data_and_check(0x1002,0x1904D1158720,'5904d115872',diagnostic_action="检查故障是否制造成功")
    #     self.bus_comm.resume_all_bus_send()
    #     time.sleep(5)
    #     self.sd_tester.send_data_and_check(0x1002,0x1904D1158720,'5904d115872',diagnostic_action="检查是否有存历史故障")
#pytest BaseTech/Diagnostics/test_diag_basetech_didfunc.py::TestDIDFunc::test_caseid_198700001           
#pytest BaseTech/Diagnostics/test_diag_basetech_didfunc.py::TestDIDFunc::test_caseid_1986
