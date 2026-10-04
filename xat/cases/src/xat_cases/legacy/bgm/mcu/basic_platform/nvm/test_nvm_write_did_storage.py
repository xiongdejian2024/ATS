# -*- coding: utf-8 -*-
"""
@File        : test_nvm_write_did_storage.py
@Author      : huajie.yang@jiduauto.com
@Time        : 2024/02/24 
@Description : Test NVM storage functionality
"""

import os
import sys
from time import sleep
import pytest

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
sys.path.append(os.path.join(os.getcwd(), "../../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *

@pytest.mark.smoke
class TestNvmWriteDid(TestABCBase):
    def before_class(self, ecu):
        self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )

    def before_each_func(self, ecu):
        pass

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")

    def reset_bgm(self):
        self.sd_tester.update_serverdoipid(0x1FFF)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(25)
        self.sd_tester.update_serverdoipid(0x1002)


    def resume_dafult_data(self):
        
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        logger.info("写入fota状态")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0xF1, 0x53, 0x00],do_assert=True)
        sleep(1)
        self.sd_tester.send_request_and_recv_response([0x2E, 0xF0, 0xF5, 0x28, 0x0A, 0X03, 0X05, 0X03, 0x02],do_assert=True)
        sleep(1)
        self.sd_tester.send_request_and_recv_response([0x2E, 0x45, 0x32, 0x00],do_assert=True)
        sleep(1)
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0x34, 0x78], do_assert=True
        )
        sleep(1)
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0x31, 0x78], do_assert=True
        )
        self.sd_tester.send_request_and_recv_response([0x2E, 0x45, 0x30, 0x00],do_assert=True)
        sleep(1)
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0x33, 0x5D], do_assert=True
        )
        sleep(1)
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0x35, 0x4B], do_assert=True
        )
        sleep(1)
        self.sd_tester.send_request_and_recv_response([0x2E, 0x42, 0xE9, 0x00],do_assert=True)
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x41, 0x09, 0x00], do_assert=True
        )
        sleep(1)
        self.sd_tester.send_request_and_recv_response([0x2E, 0x43, 0x13, 0x01],do_assert=True)
        
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x45, 0xA4, 0x07], do_assert=True
        )
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x42, 0x97, 0x78], do_assert=True
        )

    def test_caseid_1987730(self):
        '''写入多个DID后bgm重启检查DID是否存储'''
        try:
            self.resume_dafult_data()
            self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
            self.sd_tester.send_request_and_recv_response(
                [0x2E, 0xF1, 0x53, 0x04],do_assert=False)       
            logger.info("写入电源管理值")
            self.sd_tester.send_request_and_recv_response([0x2E, 0xF0, 0xF5, 0x27, 0x0A, 0X03, 0X05, 0X03, 0x02],do_assert=False)
            logger.info("写入内灯亮度值")
            
            logger.info("4532休眠超时充电使能")
            self.sd_tester.send_request_and_recv_response([0x2E, 0x45, 0x32, 0x01],do_assert=False)
            
            self.sd_tester.send_request_and_recv_response(
                [0x2E, 0x45, 0x34, 0xA0], do_assert=False
            )
            self.sd_tester.send_request_and_recv_response(
                [0x2E, 0x45, 0x31, 0xA0], do_assert=False
            )
            logger.info("DID4530写入值")
            self.sd_tester.send_request_and_recv_response([0x2E, 0x45, 0x30, 0x01],do_assert=False)
            
            self.sd_tester.send_request_and_recv_response(
                [0x2E, 0x45, 0x33, 0x7F], do_assert=False
            )
            self.sd_tester.send_request_and_recv_response(
                [0x2E, 0x45, 0x35, 0x7F], do_assert=False
            )
            self.sd_tester.send_request_and_recv_response([0x2E, 0x42, 0xE9, 0x01],do_assert=False)
            self.sd_tester.send_request_and_recv_response(
                [0x2E, 0x41, 0x09,0x0F], do_assert=False
            )
            self.sd_tester.send_request_and_recv_response([0x2E, 0x43, 0x13, 0x02],do_assert=False)

            self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
            self.sd_tester.send_request_and_recv_response(
                [0x2E, 0x45, 0xA4, 0x07], do_assert=False
            )
            
            logger.info("写入nfc解锁持续时间的值")
            self.sd_tester.send_request_and_recv_response(
                [0x2E, 0x42, 0x97,0xFF], do_assert=False
            )
            
            sleep(10)
            logger.info("------------->重启bgm")
            self.reset_bgm()
            self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
            ret_code1, local_date1 = self.sd_tester.send_request_and_recv_response(
                [0x22, 0xF1, 0x53],recv=[0x62, 0xF1, 0x53, 0x04],
                do_assert=False,
            )
            
            ret_code5, read_date5 = self.sd_tester.send_request_and_recv_response([0x22, 0xF0, 0xF5],
                                                                                recv=[0x62, 0xF0, 0xF5, 0x27, 0x0A, 0X03, 0X05, 0X03, 0x02],do_assert=False)
            ret_code12, read_date12 = self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0x32],
                                                        recv=[0x62, 0x45, 0x32, 0x01],do_assert=False)                                                                     
            ret_code6, read_date6 = self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0x34],recv=[0x62, 0x45, 0x34, 0xA0] ,do_assert=False
            )    
            ret_code7, read_date7 = self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0x31],recv=[0x62, 0x45, 0x31, 0xA0] ,do_assert=False
            )    
            ret_code13, read_date13 = self.sd_tester.send_request_and_recv_response([0x2E, 0x45, 0x30, 0x01],do_assert=False)                                      

            ret_code8, read_date8 = self.sd_tester.send_request_and_recv_response(
                [0x22, 0x45, 0x33],recv=[0x62, 0x45, 0x33, 0x7F],do_assert=False
            )
            ret_code9, read_date9 = self.sd_tester.send_request_and_recv_response(
                [0x22, 0x45, 0x35],recv=[0x62, 0x45, 0x35, 0x7F],do_assert=False
            )
            ret_code10, local_date10 = self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0xE9],recv=[0x62, 0x42, 0xE9, 0x01],do_assert=False)
            ret_code11, local_date11 = self.sd_tester.send_request_and_recv_response(
                [0x22, 0x41, 0x09],recv=[0x62, 0x41, 0x09,0x0F], do_assert=False
            )
            logger.info(f'4313驱动数量')
            ret_code4, read_date4 = self.sd_tester.send_request_and_recv_response([0x22, 0x43, 0x13],recv=[0x62, 0x43, 0x13, 0x02],do_assert=False)
            
            self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L11)
            ret_code2, read_date2 = self.sd_tester.send_request_and_recv_response(
                [0x22, 0x42, 0x97],
                recv=[0x62, 0x42, 0x97, 0xFF],
                do_assert=False,
            )
            logger.info(f'读取雨量传感器值')
            ret_code3, read_date3 = self.sd_tester.send_request_and_recv_response(
                [0x22, 0x45, 0xA4], recv=[0x62, 0x45, 0xA4, 0x07],do_assert=False
            )
            
            storage_list=[(ret_code1,local_date1),(ret_code2,read_date2),(ret_code3, read_date3),(ret_code4, read_date4),(ret_code5, read_date5),
                        (ret_code6, read_date6),(ret_code7, read_date7),(ret_code8, read_date8),(ret_code9, read_date9),(ret_code10, local_date10),
                        (ret_code11, local_date11),(ret_code12, read_date12),(ret_code13, read_date13)]
            a=0
            for i in storage_list:
                if i[0]== False:
                    logger.info(f'存储失败的DID为{bytes(i[1]).hex()}')
                    a+=1
        except Exception as e:
            logger.info(f'write did error{str(e)}')
            a=1
        self.resume_dafult_data()
        assert not a,f'有{a}个存储失败的DID'



    # def test_caseid_003(self):
        # write_vin_list1 = [random.randint(0, 255) for _ in range(17)]
        # logger.info("随机写入vin码")
        # self.sd_tester.send_request_and_recv_response(
        #     [0x2E, 0xF1, 0x90], write_vin_list1, do_assert=False
        # )
        # write_tpmsid_list = [random.randint(0, 255) for _ in range(16)]
        # logger.info("随机写入TPMS ID")
        # self.sd_tester.send_request_and_recv_response(
        #     [0x2E, 0x28, 0x1F], write_tpmsid_list, do_assert=False
        # )  
        # write_immokey_list = [random.randint(0, 255) for _ in range(32)]
        # logger.info("写入认证密钥")
        # self.sd_tester.send_request_and_recv_response(
        #     [0x2E, 0x40, 0xDE], write_immokey_list, do_assert=False
        # )
        # self.sd_tester.send_request_and_recv_response(
        #     [0x2E, 0x40, 0xDF], write_immokey_list, do_assert=False
        # )
        # self.sd_tester.send_request_and_recv_response(
        #     [0x2E, 0x40, 0xE0], write_immokey_list, do_assert=False
        # )  
        # write_power_list = [random.randint(0, 100) for _ in range(5)]
        # self.sd_tester.send_request_and_recv_response(
        #     [0x2E, 0x46, 0x00], write_power_list, do_assert=False
        # )  
        # write_408F_list = [random.randint(0, 255) for _ in range(16)]
        # self.sd_tester.send_request_and_recv_response(
        #     [0x2E, 0x40, 0x8F], write_408F_list, do_assert=False
        # )



