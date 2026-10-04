"""
@File        : test_ccp_dtc.py
@Author      : O_jingyuan.chen@external.jiduauto.com
@Time        : 2024/04/15 15:12
@Description : ccp_dtc用例

"""

import pytest
import allure
from xat_cases.legacy.bgm.mcu.case_helper.test_abc_base import TestABCBase 
from xat_ecu.api.common.common import *

@allure.feature("诊断DTC")
@allure.story("CarConfig DTC")
class TestCarConfig_DTC(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.ccp=self.sd_tester.sd_tester.make_ccp_according_id_and_data('1','A3')
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf106,SESSION.EXTENDED,UnLock.L5,f'{self.ccp}','6ef106',check_method=Check_Method.response,recover=False)


    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除的历史故障")

    def after_class(self, ecu):
        super().after_class(self, ecu)


    #BGM_MCU
    @pytest.mark.sanity
    @allure.title('Valid Configuration State_DTC(E30056)_test')
    def test_caseid_1982519(self):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.write_ccp({1:0xa4})
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56,0x50])
        self.mix.set_dtc_precontion()
        time.sleep(7)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56,0x2f])
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf106,SESSION.EMPTY,UnLock.L5,f'{self.ccp}','6ef106',check_method=Check_Method.response,recover=False)
        self.mix.set_dtc_precontion()
        time.sleep(7)
        dtc_data=self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56])[10:12]
        dtc_data_int = int(dtc_data, 16)
        dtc_data_binary = bin(dtc_data_int)[2:].zfill(8) 
        bit0 = dtc_data_binary[-1]
        bit3 = dtc_data_binary[-4]
        logger.info(f'{bit0}{bit3}') 
        assert bit0 == '0' and bit3 == '1' ,f'dtc的故障掩码为{dtc_data}，不是历史故障'
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x14,0xff,0xff,0xff],'54')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56,0x00])
        self.sd_tester.reset_0x1181()
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        time.sleep(7)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56,0x00])

    #BGM_MCU
    @pytest.mark.full
    @allure.title('Valid Configuration State_DTC(E30056)_566_test')
    def test_caseid_1987020(self):
        self.sd_tester.write_ccp({566:0x00})
        self.mix.set_dtc_precontion()
        time.sleep(7)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56,0x2f])
        hex_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 16, 17, 18, 19, 20, 23, 24, 25]
        for hex in hex_list:
            logger.info(f'此刻566写入的值是{hex}')
            self.sd_tester.write_ccp({566:hex})
            self.mix.set_dtc_precontion()
            time.sleep(7)
            dtc_data=self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56])[10:12]
            dtc_data_int = int(dtc_data, 16)
            dtc_data_binary = bin(dtc_data_int)[2:].zfill(8) 
            bit0 = dtc_data_binary[-1]
            bit3 = dtc_data_binary[-4]
            logger.info(f'{bit0}{bit3}') 
            assert bit0 == '0' and bit3 == '1' ,f'dtc的故障掩码为{dtc_data}，不是历史故障'

    #BGM_MCU
    @pytest.mark.full
    @allure.title('Valid Configuration State_DTC(E30056)_962_test')
    def test_caseid_1987021(self):
        self.sd_tester.write_ccp({962:0x01})
        self.mix.set_dtc_precontion()
        time.sleep(7)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56,0x2f])
        hex_list = [0, 2]
        for hex in hex_list:
            logger.info(f'此刻962写入的值是{hex}')
            self.sd_tester.write_ccp({962:hex})
            self.mix.set_dtc_precontion()
            time.sleep(7)
            dtc_data=self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56])[10:12]
            dtc_data_int = int(dtc_data, 16)
            dtc_data_binary = bin(dtc_data_int)[2:].zfill(8) 
            bit0 = dtc_data_binary[-1]
            bit3 = dtc_data_binary[-4]
            logger.info(f'{bit0}{bit3}') 
            assert bit0 == '0' and bit3 == '1' ,f'dtc的故障掩码为{dtc_data}，不是历史故障'

    #BGM_MCU
    @pytest.mark.full
    @allure.title('Valid Configuration State_DTC(E30056)_1327_test')
    def test_caseid_1987022(self):
        self.sd_tester.write_ccp({1327:0x00})
        self.mix.set_dtc_precontion()
        time.sleep(7)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56,0x2f])
        hex_list = [1, 2]
        for hex in hex_list:
            logger.info(f'此刻1327写入的值是{hex}')
            self.sd_tester.write_ccp({1327:hex})
            self.mix.set_dtc_precontion()
            dtc_data=self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56])[10:12]
            dtc_data_int = int(dtc_data, 16)
            dtc_data_binary = bin(dtc_data_int)[2:].zfill(8) 
            bit0 = dtc_data_binary[-1]
            bit3 = dtc_data_binary[-4]
            logger.info(f'{bit0}{bit3}') 
            assert bit0 == '0' and bit3 == '1' ,f'dtc的故障掩码为{dtc_data}，不是历史故障'

    #BGM_MCU
    @pytest.mark.full
    @allure.title('Valid Configuration State_DTC(E30056)_1328_test')
    def test_caseid_1987023(self):
        self.sd_tester.write_ccp({1328:0x00})
        self.mix.set_dtc_precontion()
        time.sleep(7)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56,0x2f])
        hex_list = [1, 2]
        for hex in hex_list:
            logger.info(f'此刻1328写入的值是{hex}')
            self.sd_tester.write_ccp({1328:hex})
            self.mix.set_dtc_precontion()
            dtc_data=self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56])[10:12]
            dtc_data_int = int(dtc_data, 16)
            dtc_data_binary = bin(dtc_data_int)[2:].zfill(8) 
            bit0 = dtc_data_binary[-1]
            bit3 = dtc_data_binary[-4]
            logger.info(f'{bit0}{bit3}') 
            assert bit0 == '0' and bit3 == '1' ,f'dtc的故障掩码为{dtc_data}，不是历史故障'

    #BGM_MCU
    @pytest.mark.full
    @allure.title('Valid Configuration State_DTC(E30056)_1334_test')
    def test_caseid_1987024(self):
        self.sd_tester.write_ccp({1334:0x00})
        self.mix.set_dtc_precontion()
        time.sleep(7)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56,0x2f])
        hex_list = [1, 2]
        for hex in hex_list:
            logger.info(f'此刻1334写入的值是{hex}')
            self.sd_tester.write_ccp({1334:hex})
            self.mix.set_dtc_precontion()
            dtc_data=self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56])[10:12]
            dtc_data_int = int(dtc_data, 16)
            dtc_data_binary = bin(dtc_data_int)[2:].zfill(8) 
            bit0 = dtc_data_binary[-1]
            bit3 = dtc_data_binary[-4]
            logger.info(f'{bit0}{bit3}') 
            assert bit0 == '0' and bit3 == '1' ,f'dtc的故障掩码为{dtc_data}，不是历史故障'

    #BGM_MCU
    @pytest.mark.full
    @allure.title('Valid Configuration State_DTC(E30056)_1439_test')
    def test_caseid_1987025(self):
        self.sd_tester.write_ccp({1439:0x00})
        self.mix.set_dtc_precontion()
        time.sleep(7)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56,0x2f])
        hex_list = [1, 2]
        for hex in hex_list:
            logger.info(f'此刻1439写入的值是{hex}')
            self.sd_tester.write_ccp({1439:hex})
            self.mix.set_dtc_precontion()
            dtc_data=self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56])[10:12]
            dtc_data_int = int(dtc_data, 16)
            dtc_data_binary = bin(dtc_data_int)[2:].zfill(8) 
            bit0 = dtc_data_binary[-1]
            bit3 = dtc_data_binary[-4]
            logger.info(f'{bit0}{bit3}') 
            assert bit0 == '0' and bit3 == '1' ,f'dtc的故障掩码为{dtc_data}，不是历史故障'

    #BGM_MCU
    @pytest.mark.full
    @allure.title('Valid Configuration State_DTC(E30056)_964_test')
    def test_caseid_1987026(self):
        self.sd_tester.write_ccp({964:0x02})
        self.mix.set_dtc_precontion()
        time.sleep(7)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56,0x2f])
        hex_list = [0, 1]
        for hex in hex_list:
            logger.info(f'此刻964写入的值是{hex}')
            self.sd_tester.write_ccp({964:hex})
            self.mix.set_dtc_precontion()
            dtc_data=self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56])[10:12]
            dtc_data_int = int(dtc_data, 16)
            dtc_data_binary = bin(dtc_data_int)[2:].zfill(8) 
            bit0 = dtc_data_binary[-1]
            bit3 = dtc_data_binary[-4]
            logger.info(f'{bit0}{bit3}') 
            assert bit0 == '0' and bit3 == '1' ,f'dtc的故障掩码为{dtc_data}，不是历史故障'

    #BGM_MCU
    @pytest.mark.full
    @allure.title('Valid Configuration State_DTC(E30056)_965_test')
    def test_caseid_1987027(self):
        self.sd_tester.write_ccp({965:0x02})
        self.mix.set_dtc_precontion()
        time.sleep(7)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56,0x2f])
        hex_list = [0, 1]
        for hex in hex_list:
            logger.info(f'此刻965写入的值是{hex}')
            self.sd_tester.write_ccp({965:hex})
            self.mix.set_dtc_precontion()
            dtc_data=self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56])[10:12]
            dtc_data_int = int(dtc_data, 16)
            dtc_data_binary = bin(dtc_data_int)[2:].zfill(8) 
            bit0 = dtc_data_binary[-1]
            bit3 = dtc_data_binary[-4]
            logger.info(f'{bit0}{bit3}') 
            assert bit0 == '0' and bit3 == '1' ,f'dtc的故障掩码为{dtc_data}，不是历史故障'

    #BGM_MCU
    @pytest.mark.full
    @allure.title('Valid Configuration State_DTC(E30056)_968_test')
    def test_caseid_1989025(self):
        self.sd_tester.write_ccp({968:0x02})
        self.mix.set_dtc_precontion()
        time.sleep(7)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56,0x2f])
        hex_list = [0, 1]
        for hex in hex_list:
            logger.info(f'此刻968写入的值是{hex}')
            self.sd_tester.write_ccp({968:hex})
            self.mix.set_dtc_precontion()
            dtc_data=self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56])[10:12]
            dtc_data_int = int(dtc_data, 16)
            dtc_data_binary = bin(dtc_data_int)[2:].zfill(8) 
            bit0 = dtc_data_binary[-1]
            bit3 = dtc_data_binary[-4]
            logger.info(f'{bit0}{bit3}') 
            assert bit0 == '0' and bit3 == '1' ,f'dtc的故障掩码为{dtc_data}，不是历史故障'

    #BGM_MCU
    @pytest.mark.full
    @allure.title('Valid Configuration State_DTC(E30056)_970_test')
    def test_caseid_1989026(self):
        self.sd_tester.write_ccp({970:0x02})
        self.mix.set_dtc_precontion()
        time.sleep(7)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56,0x2f])
        hex_list = [0, 1]
        for hex in hex_list:
            logger.info(f'此刻970写入的值是{hex}')
            self.sd_tester.write_ccp({970:hex})
            self.mix.set_dtc_precontion()
            dtc_data=self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x04,0xe3,0x00,0x56,0x20],[0x59,0x04,0xe3,0x00,0x56])[10:12]
            dtc_data_int = int(dtc_data, 16)
            dtc_data_binary = bin(dtc_data_int)[2:].zfill(8) 
            bit0 = dtc_data_binary[-1]
            bit3 = dtc_data_binary[-4]
            logger.info(f'{bit0}{bit3}') 
            assert bit0 == '0' and bit3 == '1' ,f'dtc的故障掩码为{dtc_data}，不是历史故障'

#pytest BaseTech/diag_dtc/test_ccp_dtc.py::TestCarConfig_DTC::test_caseid_1987028