#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : test_ccp.py
@time         : 2023/12/25
@author       : o_jingyuan.chen@external.jiduauto.com
@description  : 
'''

import pytest
import allure
from xat_cases.legacy.basetech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.ecu_sim.parse_tb_config import ParseTBConfig

@allure.feature("BGM BaseTech/车辆配置")
@allure.story("CCP")
class TestBasetechccp(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        with allure.step('加载bgm_ccp文件'):
            self.bgmcli = BGM_SSH()
            version_info = self.bgmcli.get_version()
            version_num = version_info.get('build_version')[7:10]
            absolute_path = os.path.abspath('./config/bgm_ccp.yaml')
            tb_path = os.path.join(absolute_path)
            tb_config = ParseTBConfig(tb_path)
            self.ccp_tb_config = tb_config.yaml_content
            if version_num not in self.ccp_tb_config.keys():
                logger.info(f'{version_num}不在bgm_ccp.yaml文件中,需要更新')
            else:
                self.json_data = self.ccp_tb_config[version_num]['ccp_json']   
        self.ccp=self.sd_tester.sd_tester.make_ccp_according_id_and_data('1','A3')
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf106,SESSION.EXTENDED,UnLock.L5,f'{self.ccp}','6ef106',check_method=Check_Method.response,recover=False)
        super().after_class(self, ecu)


    #BGM_MCU
    @pytest.mark.smoke
    @allure.title('CarCfg_data storage_复位测试')
    def test_caseid_1982464(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf106,SESSION.EXTENDED,UnLock.L5,f'{self.ccp}','6ef106',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_ccp({181:0x02})
        ccp2=self.sd_tester.read_did_and_check(TA.BGM_MCU,0xf106,SESSION.EMPTY,'62f106',check_length=3122)
        self.sd_tester.reset_0x1181()
        ccp1=self.sd_tester.read_did_and_check(TA.BGM_MCU,0xf106,SESSION.EMPTY,'62f106',check_length=3122)
        assert int(ccp1[3118:],16) == int(ccp2[3118:],16)

    #BGM_MCU
    @pytest.mark.smoke
    @allure.title('CarCfg_data storage_断电重启测试')
    def test_caseid_1982463(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf106,SESSION.EXTENDED,UnLock.L5,f'{self.ccp}','6ef106',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_ccp({181:0x02})
        ccp2=self.sd_tester.read_did_and_check(TA.BGM_MCU,0xf106,SESSION.EMPTY,'62f106',check_length=3122)
        self.io.io_reset_bgm(times=10)
        ccp1=self.sd_tester.read_did_and_check(TA.BGM_MCU,0xf106,SESSION.EMPTY,'62f106',check_length=3122)
        assert int(ccp1[3118:],16) == int(ccp2[3118:],16)

    #BGM_MCU
    @pytest.mark.smoke
    @allure.title('OperationCycle_BackboneFR_test')
    def test_caseid_1982494(self):
        self.mix.check_ccp_data_resp(CheckType.IN_TIME,'backbonefr',0x80104,15)
        self.mix.check_ccp_data_resp(CheckType.IN_TIME,'backbonefr',0x270508)

    #BGM_MCU
    @pytest.mark.smoke
    @allure.title('OperationCycle_BackboneFR_usagmode_test')
    def test_caseid_1982493(self):
        self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3')
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.mix.check_ccp_data_resp(CheckType.IN_ALL,'backbonefr', 0x80104,15)
        self.mix.check_ccp_data_resp(CheckType.IN_ALL,'backbonefr', 0x270508)
        self.sd_tester.change_usage_mode(UsageMode.ABANDONED)

    #BGM_MCU
    @pytest.mark.full
    @allure.title('OperationCycle_BackboneFR_丢帧test')
    def test_caseid_1982492(self):
        self.mix.check_ccp_data_resp(CheckType.IS_COMPLETE,'backbonefr', 0x80104,15)
        self.mix.check_ccp_data_resp(CheckType.IS_COMPLETE,'backbonefr', 0x270508)

    #BGM_MCU
    @pytest.mark.smoke
    @allure.title('OperationCycle_bodycan_test')
    def test_caseid_1982512(self):
        self.mix.check_ccp_data_resp(CheckType.IN_TIME,'bodycan',0x340)
        self.mix.check_ccp_data_resp(CheckType.IN_TIME,'bodycan',0x132)

    #BGM_MCU
    @pytest.mark.smoke
    @allure.title('OperationCycle_bodycan_usagmode_test')
    def test_caseid_1982511(self):
        self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3')
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.mix.check_ccp_data_resp(CheckType.IN_ALL,'bodycan',0x340)
        self.mix.check_ccp_data_resp(CheckType.IN_ALL,'bodycan',0x132)
        self.sd_tester.change_usage_mode(UsageMode.ABANDONED)
                
    #BGM_MCU
    @pytest.mark.full
    @allure.title('OperationCycle_bodycan_丢帧test')
    def test_caseid_1982510(self):
        self.mix.check_ccp_data_resp(CheckType.IS_COMPLETE,'bodycan',0x340)
        self.mix.check_ccp_data_resp(CheckType.IS_COMPLETE,'bodycan',0x132)

    #BGM_MCU
    @pytest.mark.smoke
    @allure.title('OperationCycle_bodyexposedcanfd_test')
    def test_caseid_1982509(self):
        self.mix.check_ccp_data_resp(CheckType.IN_TIME,'bodyexposedcanfd',0x180)
        self.mix.check_ccp_data_resp(CheckType.IN_TIME,'bodyexposedcanfd',0x183)

    #BGM_MCU
    @pytest.mark.smoke
    @allure.title('OperationCycle_bodyexposedcanfd_usagmode_test')
    def test_caseid_1982508(self):
        self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3')
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.mix.check_ccp_data_resp(CheckType.IN_ALL,'bodyexposedcanfd',0x180)
        self.mix.check_ccp_data_resp(CheckType.IN_ALL,'bodyexposedcanfd',0x183)
        self.sd_tester.change_usage_mode(UsageMode.ABANDONED)

    #BGM_MCU
    @pytest.mark.full
    @allure.title('OperationCycle_bodyexposedcanfd_丢帧test')
    def test_caseid_1982507(self):
        self.mix.check_ccp_data_resp(CheckType.IS_COMPLETE,'bodyexposedcanfd',0x180)
        self.mix.check_ccp_data_resp(CheckType.IS_COMPLETE,'bodyexposedcanfd',0x183)


    #BGM_MCU
    @pytest.mark.smoke
    @allure.title('OperationCycle_connectivitycanfd_test')
    def test_caseid_1982506(self):
        self.mix.check_ccp_data_resp(CheckType.IN_TIME,'connectivitycanfd',0x330)
        self.mix.check_ccp_data_resp(CheckType.IN_TIME,'connectivitycanfd',0x400)
        
    #BGM_MCU
    @pytest.mark.smoke
    @allure.title('OperationCycle_connectivitycanfd_usagmode_test')
    def test_caseid_1982505(self):
        self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3')
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)        
        self.mix.check_ccp_data_resp(CheckType.IN_ALL,'connectivitycanfd',0x330)
        self.mix.check_ccp_data_resp(CheckType.IN_ALL,'connectivitycanfd',0x400)
        self.sd_tester.change_usage_mode(UsageMode.ABANDONED)

    #BGM_MCU
    @pytest.mark.full
    @allure.title('OperationCycle_connectivitycanfd_丢帧test')
    def test_caseid_1982504(self):
        self.mix.check_ccp_data_resp(CheckType.IS_COMPLETE,'connectivitycanfd',0x330)
        self.mix.check_ccp_data_resp(CheckType.IS_COMPLETE,'connectivitycanfd',0x400)

    #BGM_MCU
    @pytest.mark.smoke
    @allure.title('OperationCycle_passivesafetycan_test')
    def test_caseid_1982503(self):
        self.mix.check_ccp_data_resp(CheckType.IN_TIME,'passivesafetycan',0x30d)
        self.mix.check_ccp_data_resp(CheckType.IN_TIME,'passivesafetycan',0x2eb)

    #BGM_MCU
    @pytest.mark.smoke
    @allure.title('OperationCycle_passivesafetycan_usagmode_test')
    def test_caseid_1982502(self):
        self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3')
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)        
        self.mix.check_ccp_data_resp(CheckType.IN_ALL,'passivesafetycan',0x30d)
        self.mix.check_ccp_data_resp(CheckType.IN_ALL,'passivesafetycan',0x2eb)
        self.sd_tester.change_usage_mode(UsageMode.ABANDONED)

    #BGM_MCU
    @pytest.mark.full
    @allure.title('OperationCycle_passivesafetycan_丢帧test')
    def test_caseid_1982501(self):
        self.mix.check_ccp_data_resp(CheckType.IS_COMPLETE,'passivesafetycan',0x30d)
        self.mix.check_ccp_data_resp(CheckType.IS_COMPLETE,'passivesafetycan',0x2eb)

    #BGM_MCU
    @pytest.mark.sanity
    @allure.title('Parameter 遍历写入test_CCP#(1-504)_Useful Value')
    def test_caseid_1982515(self):
        self.mix.cycle_write_ccp(self.json_data,1,504,'bodycan',0x340)

    #BGM_MCU
    @pytest.mark.sanity
    @allure.title('Parameter 遍历写入test_CCP#(1301-1554)_Useful Value')
    def test_caseid_1982513(self):
        self.mix.cycle_write_ccp(self.json_data,1301,1554,'backbonefr',0x260040)

    #BGM_MCU
    @pytest.mark.sanity
    @allure.title('Parameter 遍历写入test_CCP#(505-999)_Useful Value')
    def test_caseid_1982514(self):
        self.mix.cycle_write_ccp(self.json_data,505,999,'bodycan',0x132)

    #BGM_MCU
    @pytest.mark.smoke
    @allure.title('Valid Configuration State_DID(E103)_test_10个无效值读出')
    def test_caseid_1982518(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf106,SESSION.EXTENDED,UnLock.L5,f'{self.ccp}','6ef106',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_ccp({1:0xa2,2:0x02,3:0x01,6:0x01,8:0x02,9:0x01,10:0x01,13:0x01,19:0x07,22:0x01})
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xe103,SESSION.EMPTY,'62e1030a',check_length=68)

    #BGM_MCU
    @pytest.mark.smoke
    @allure.title('Valid Configuration State_DID(E103)_test_最大个数无效值读出')
    def test_caseid_1982517(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf106,SESSION.EMPTY,UnLock.L5,f'{"ff" * 1556}eaf1',f'62f106{"ff" * 1556}eaf1',check_method=Check_Method.read,recover=False)
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xe103,SESSION.EMPTY,'62e103f1',check_length=68)

    #BGM_MCU
    @pytest.mark.full
    @allure.title('Valid Configuration State_DID(E103)_test_有效值误读')
    def test_caseid_1982516(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf106,SESSION.EXTENDED,UnLock.L5,f'{self.ccp}','6ef106',check_method=Check_Method.response,recover=False)
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xe103,SESSION.EMPTY,'62e10300',check_length=68)
        self.sd_tester.write_ccp({3:0x80,9:0xa3,177:0x81,181:0x02,183:0x84,189:0x02,460:0x82,524:0x01,564:0x01,636:0x02,950:0x02,958:0x02,959:0x00,960:0x02,961:0x02,1306:0x02,1309:0x02,1310:0x02,1312:0x01,1329:0x02,1333:0x01,1381:0x01,1395:0x02,1473:0x02,1530:0x02,1531:0x02,1532:0x02,1533:0x01,1534:0x01,1535:0x02,1536:0x02})
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xe103,SESSION.EMPTY,'62e10300',check_length=68)
        self.sd_tester.write_ccp({958:0x00,959:0x00,960:0x00,961:0x00})
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xe103,SESSION.EMPTY,'62e10300',check_length=68)
        hex_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 16, 17, 18, 19, 20, 23, 24, 25]
        for hex in hex_list:
            logger.info(f'此刻566写入的值是{hex}')
            self.sd_tester.write_ccp({566:hex})
            self.sd_tester.read_did_and_check(TA.BGM_MCU,0xe103,SESSION.EMPTY,'62e10300',check_length=68)

    #BGM_MCU
    @pytest.mark.smoke
    @allure.title('Valid Configuration State_test')
    def test_caseid_1982521(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf106,SESSION.EXTENDED,UnLock.L5,f'{self.ccp}','6ef106',check_method=Check_Method.response,recover=False)
        self.mix.set_dtc_precontion()
        self.sd_tester.clear_all_dtc_and_check(TA.BGM_MCU,SESSION.EMPTY,UnLock.L0,'54')
        time.sleep(7)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56,0x00])
        self.sd_tester.change_usage_mode(UsageMode.ABANDONED)

    #BGM_MCU
    @pytest.mark.smoke
    @allure.title('Valid Configuration State_错误CRC_test')
    def test_caseid_1982520(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf106,SESSION.EXTENDED,UnLock.L5,f'{self.ccp}','6ef106',check_method=Check_Method.response,recover=False)
        ccp1=self.sd_tester.read_did_and_check(TA.BGM_MCU,0xf106,SESSION.EMPTY,'62f106',check_length=3122)
        self.ccp1 = self.ccp[:-4] + '0000'
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf106,SESSION.EMPTY,UnLock.L5,f'{self.ccp1}','7f2e31',check_method=Check_Method.response,recover=False)
        ccp2=self.sd_tester.read_did_and_check(TA.BGM_MCU,0xf106,SESSION.EMPTY,'62f106',check_length=3122)
        assert int(ccp1[3118:],16) == int(ccp2[3118:],16)
        self.mix.set_dtc_precontion()
        self.sd_tester.clear_all_dtc_and_check(TA.BGM_MCU,SESSION.EMPTY,UnLock.L0,'54')
        time.sleep(7)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56,0x00])
        self.sd_tester.change_usage_mode(UsageMode.ABANDONED)


#pytest BaseTech/CarConfiguration/test_ccp.py::TestBasetechccp::test_caseid_1982515 --disable_partner='true'



        
