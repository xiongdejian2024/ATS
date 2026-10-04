"""
@File         :test_licheng_abc.py
@Time         :2024/10/28 19:07:31
@Author       :shulin.zheng@jiduauto.com
@Description  :Test SOA for HighVoltageService
"""
import os
import sys
import pytest
import allure
from time import sleep
from datetime import datetime, timedelta

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.legacy.driver.ssh_interface import command_send
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.common.data_handle import *

@allure.feature("车控车设")
@allure.story("高压里程续航功能")
@pytest.mark.test1018
class TestHVdischarge(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["DrivingAssistService_client"])
        self.bus_comm.set_vehspd_gear(vehspd=0, gear=Gear.Park)
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)
        self.sd_tester.write_single_ccp(950, 1)
        sleep(2)

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
            pass

    @allure.title("车辆行驶里程_车速可信_TotDstTrvldHiResl算法验证")
    @pytest.mark.sanity
    @pytest.mark.test1128
    def test_caseid_1995684(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_and_qf(vehspd=0.0, veh_qf= VehSpdQf.AccurData)
        A = self.bus_comm.get_TotDstTrvldHiResl_value()
        A1 = self.bus_comm.get_BkpOfDstTrvld_value()
        self.bus_comm.set_vehspd_and_qf(vehspd=10.0, veh_qf= VehSpdQf.AccurData)
        sleep(300)
        self.bus_comm.set_vehspd_and_qf(vehspd=0.0, veh_qf= VehSpdQf.AccurData)
        B = self.bus_comm.get_TotDstTrvldHiResl_value()
        B1 = self.bus_comm.get_BkpOfDstTrvld_value()
        assert abs(B-(A+300*10*1.02))<=10,"里程计算错误"
        assert B1==A1+3,"备份里程计算错误"

    @allure.title("车辆行驶里程_车速可信_TotDstTrvldHiResl算法验证(1.02系数)")
    @pytest.mark.sanity
    @pytest.mark.fota
    def test_caseid_1995685(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_and_qf(vehspd=0.0, veh_qf= VehSpdQf.AccurData)
        A = self.bus_comm.get_TotDstTrvldHiResl_value()
        A1 = self.bus_comm.get_BkpOfDstTrvld_value()
        self.bus_comm.set_vehspd_and_qf(vehspd=10.0, veh_qf= VehSpdQf.AccurData)
        sleep(300)
        B = self.bus_comm.get_TotDstTrvldHiResl_value()
        B1 = self.bus_comm.get_BkpOfDstTrvld_value()
        assert abs((B-A)/10/300-1.02)*100<2,"里程计算错误"
        assert abs((B1-A1)-10*300*1.02/1000)<2,"备份里程计算错误"

    @allure.title("车辆行驶里程_车速不可信1_反向场景")
    @pytest.mark.sanity
    @pytest.mark.test1128
    def test_caseid_1995686(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_and_qf(vehspd=0.0, veh_qf= VehSpdQf.AccurData)
        A = self.bus_comm.get_TotDstTrvldHiResl_value()
        A1 = self.bus_comm.get_BkpOfDstTrvld_value()
        self.bus_comm.set_vehspd_and_qf(vehspd=10.0, veh_qf= VehSpdQf.TmpUndefdData)
        sleep(300)
        self.bus_comm.set_vehspd_and_qf(vehspd=0.0, veh_qf= VehSpdQf.AccurData)
        B = self.bus_comm.get_TotDstTrvldHiResl_value()
        B1 = self.bus_comm.get_BkpOfDstTrvld_value()
        assert B==A,"里程计算错误"
        assert B1==A1,"备份里程计算错误"

    @allure.title("车辆行驶里程_车速可信_反向场景E2E不正确_VehSpdLgtChks不变化")
    @pytest.mark.sanity
    @pytest.mark.test1128
    def test_caseid_1995687(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_and_qf(vehspd=0.0, veh_qf= VehSpdQf.AccurData)
        A = self.bus_comm.get_TotDstTrvldHiResl_value()
        A1 = self.bus_comm.get_BkpOfDstTrvld_value()
        self.bus_comm.set_vehspd_and_qf(vehspd=10.0, veh_qf= VehSpdQf.AccurData)
        self.bus_comm.ipdu.set_no_cntr(self.bus_comm.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgt')
        self.bus_comm.ipdu.set_no_crc(self.bus_comm.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgt')
        sleep(300)
        self.bus_comm.set_vehspd_and_qf(vehspd=0.0, veh_qf= VehSpdQf.AccurData)
        self.bus_comm.ipdu.restore_cntr(self.bus_comm.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgt')
        self.bus_comm.ipdu.restore_crc(self.bus_comm.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgt')
        B = self.bus_comm.get_TotDstTrvldHiResl_value()
        B1 = self.bus_comm.get_BkpOfDstTrvld_value()
        assert B==A,"里程计算错误"
        assert B1==A1,"备份里程计算错误"

    @allure.title("638234_行驶里程_行驶里程计算_存储NVM（诊断）")
    @pytest.mark.sanity
    @pytest.mark.test1128
    def test_caseid_1995688(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_and_qf(vehspd=0.0, veh_qf= VehSpdQf.AccurData)
        A = self.bus_comm.get_TotDstTrvldHiResl_value()
        A1 = self.bus_comm.get_BkpOfDstTrvld_value()
        self.bus_comm.set_vehspd_and_qf(vehspd=10.0, veh_qf= VehSpdQf.AccurData)
        sleep(300)
        self.bus_comm.set_vehspd_and_qf(vehspd=0.0, veh_qf= VehSpdQf.AccurData)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        B = self.bus_comm.get_TotDstTrvldHiResl_value()
        B1 = self.bus_comm.get_BkpOfDstTrvld_value()
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        C = self.bus_comm.get_TotDstTrvldHiResl_value()
        C1 = self.bus_comm.get_BkpOfDstTrvld_value()
        assert B == C,  '里程诊断TotDstTrvldHiResl数值存储异常'
        assert B1 == C1,  '里程诊断BkpOfDstTrvld数值存储异常'

    @allure.title("车辆行驶里程_NVM存储_里程累加_大于10km")
    @pytest.mark.sanity
    @pytest.mark.test1128
    def test_caseid_1995689(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_and_qf(vehspd=0.0, veh_qf= VehSpdQf.AccurData)
        A = self.bus_comm.get_TotDstTrvldHiResl_value()
        A1 = self.bus_comm.get_BkpOfDstTrvld_value()
        self.bus_comm.set_vehspd_and_qf(vehspd=50.0, veh_qf= VehSpdQf.AccurData)
        sleep(250)
        self.bus_comm.set_vehspd_and_qf(vehspd=0.0, veh_qf= VehSpdQf.AccurData)
        B = self.bus_comm.get_TotDstTrvldHiResl_value()
        B1 = self.bus_comm.get_BkpOfDstTrvld_value()
        assert abs(B-(A+250*50*1.02))<=10,"里程计算错误"
        assert abs(B1-(A1+12))<=1,"备份里程计算错误"
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        C = self.bus_comm.get_TotDstTrvldHiResl_value()
        C1 = self.bus_comm.get_BkpOfDstTrvld_value()
        assert C == A+10000,  '里程诊断TotDstTrvldHiResl数值存储异常'
        assert C1 == A1+10,  '里程诊断BkpOfDstTrvld数值存储异常'

    @allure.title("车辆行驶里程_诊断读写_ 总里程>255km,写入更大里程")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_caseid_1995695(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"):    
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x01,0x00],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x01,0x00])
            self.bus_comm.check_TotDstTrvldHiResl_value(256000)
            self.bus_comm.check_BkpOfDstTrvld_value(256)
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x01,0x01],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x01,0x01])
            self.bus_comm.check_TotDstTrvldHiResl_value(257000)
            self.bus_comm.check_BkpOfDstTrvld_value(257)

    @allure.title("车辆行驶里程_诊断读写_ 总里程>255km,写255")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_caseid_1995696(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"):    
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x01,0x01],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x01,0x01])
            self.bus_comm.check_TotDstTrvldHiResl_value(257000)
            self.bus_comm.check_BkpOfDstTrvld_value(257)
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0xFF],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x00,0xFF])
            self.bus_comm.check_TotDstTrvldHiResl_value(255000)
            self.bus_comm.check_BkpOfDstTrvld_value(255)

    @allure.title("车辆行驶里程_诊断读写_ 总里程>255km,写10")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_caseid_1995728(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"):    
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x01,0x01],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x01,0x01])
            self.bus_comm.check_TotDstTrvldHiResl_value(257000)
            self.bus_comm.check_BkpOfDstTrvld_value(257)
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0x0A],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x01,0x01])
            self.bus_comm.check_TotDstTrvldHiResl_value(257000)
            self.bus_comm.check_BkpOfDstTrvld_value(257)

    @allure.title("车辆行驶里程_诊断读写_ 总里程>255km,写小于10")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_caseid_1995729(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"):    
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x01,0x01],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x01,0x01])
            self.bus_comm.check_TotDstTrvldHiResl_value(257000)
            self.bus_comm.check_BkpOfDstTrvld_value(257)
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0x08],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x01,0x01])
            self.bus_comm.check_TotDstTrvldHiResl_value(257000)
            self.bus_comm.check_BkpOfDstTrvld_value(257)

    @allure.title("车辆行驶里程_诊断读写_ 总里程=255km,写入10")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_caseid_1995732(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"):    
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0xFF],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x00,0xFF])
            self.bus_comm.check_TotDstTrvldHiResl_value(255000)
            self.bus_comm.check_BkpOfDstTrvld_value(255)
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0x0A],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x00,0xFF])
            self.bus_comm.check_TotDstTrvldHiResl_value(255000)
            self.bus_comm.check_BkpOfDstTrvld_value(255)

    @allure.title("车辆行驶里程_诊断读写_ 总里程=255km,写入100")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_caseid_1995730(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"):    
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0xFF],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x00,0xFF])
            self.bus_comm.check_TotDstTrvldHiResl_value(255000)
            self.bus_comm.check_BkpOfDstTrvld_value(255)
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0x64],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x00,0x64])
            self.bus_comm.check_TotDstTrvldHiResl_value(100000)
            self.bus_comm.check_BkpOfDstTrvld_value(100)

    @allure.title("车辆行驶里程_诊断读写_ 总里程=255km,写大于255")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_caseid_1995697(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"):    
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0xFF],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x00,0xFF])
            self.bus_comm.check_TotDstTrvldHiResl_value(255000)
            self.bus_comm.check_BkpOfDstTrvld_value(255)
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x01,0x2C],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x01,0x2C])
            self.bus_comm.check_TotDstTrvldHiResl_value(300000)
            self.bus_comm.check_BkpOfDstTrvld_value(300)

    @allure.title("车辆行驶里程_诊断读写_ 总里程=255km,写小于10")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_caseid_1995733(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"):    
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0xFF],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x00,0xFF])
            self.bus_comm.check_TotDstTrvldHiResl_value(255000)
            self.bus_comm.check_BkpOfDstTrvld_value(255)
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0x05],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x00,0xFF])
            self.bus_comm.check_TotDstTrvldHiResl_value(255000)
            self.bus_comm.check_BkpOfDstTrvld_value(255)

    @allure.title("车辆行驶里程_诊断读写_ 总里程<255km,写入10")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_caseid_1995737(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"):    
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0xC8],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x00,0xC8])
            self.bus_comm.check_TotDstTrvldHiResl_value(200000)
            self.bus_comm.check_BkpOfDstTrvld_value(200)
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0x0A],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x00,0xC8])
            self.bus_comm.check_TotDstTrvldHiResl_value(200000)
            self.bus_comm.check_BkpOfDstTrvld_value(200)

    @allure.title("车辆行驶里程_诊断读写_ 总里程<255km,写入100")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_caseid_1995736(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"):    
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0xC8],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x00,0xC8])
            self.bus_comm.check_TotDstTrvldHiResl_value(200000)
            self.bus_comm.check_BkpOfDstTrvld_value(200)
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0x64],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x00,0x64])
            self.bus_comm.check_TotDstTrvldHiResl_value(100000)
            self.bus_comm.check_BkpOfDstTrvld_value(100)

    @allure.title("车辆行驶里程_诊断读写_ 总里程<255km,写入255")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_caseid_1995735(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"):    
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0x64],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x00,0x64])
            self.bus_comm.check_TotDstTrvldHiResl_value(100000)
            self.bus_comm.check_BkpOfDstTrvld_value(100)
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0xFF],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x00,0xFF])
            self.bus_comm.check_TotDstTrvldHiResl_value(255000)
            self.bus_comm.check_BkpOfDstTrvld_value(255)

    @allure.title("车辆行驶里程_诊断读写_ 总里程<255km,写大于255")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_caseid_1995734(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"):    
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0x64],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x00,0x64])
            self.bus_comm.check_TotDstTrvldHiResl_value(100000)
            self.bus_comm.check_BkpOfDstTrvld_value(100)
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x01,0x2C],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x01,0x2C])
            self.bus_comm.check_TotDstTrvldHiResl_value(300000)
            self.bus_comm.check_BkpOfDstTrvld_value(300)

    @allure.title("车辆行驶里程_诊断读写_ 总里程<255km,写小于10")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.V_1_4
    def test_caseid_1995738(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"):    
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0xC8],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x00,0xC8])
            self.bus_comm.check_TotDstTrvldHiResl_value(200000)
            self.bus_comm.check_BkpOfDstTrvld_value(200)
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0x05],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x00,0xC8])
            self.bus_comm.check_TotDstTrvldHiResl_value(200000)
            self.bus_comm.check_BkpOfDstTrvld_value(200)

    @allure.title("车辆行驶里程_CDC里程同步_大于BGM里程同步(恢复默认值00)")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.test1128
    def test_caseid_1995694(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"):    
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0x00],recv=[0x6E,0xDD,0x01])
            sleep(2)
            self.sd_tester.send_request_and_recv_response([0x22,0xDD,0x01],recv=[0x62,0xDD,0x01,0x00,0x00,0x00])
            self.bus_comm.check_TotDstTrvldHiResl_value(0)
            self.bus_comm.check_BkpOfDstTrvld_value(0)
            self.soa.set_Distance_cdc(1500)
            sleep(5)
            self.bus_comm.check_TotDstTrvldHiResl_value(1500)
            self.bus_comm.check_BkpOfDstTrvld_value(1)

    @allure.title("车辆行驶里程_CDC里程同步_小于10km BGM里程同步")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.test1128
    def test_caseid_1995693(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"): 
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0x09],recv=[0x6E,0xDD,0x01])
            sleep(2) 
            A = self.bus_comm.get_TotDstTrvldHiResl_value()
            logger.info("总里程: TotDstTrvldHiResl {}".format(A))
            A1 = self.bus_comm.get_BkpOfDstTrvld_value()
            if A1 < 10:
                logger.info("BGM里程小于10km")
                self.soa.set_Distance_cdc(10000)
                sleep(5)
                self.bus_comm.check_TotDstTrvldHiResl_value(10000)
                self.bus_comm.check_BkpOfDstTrvld_value(10)
            else:
                logger.info("BGM里程超过10km")
                assert False,"重新设置BGM里程"

    @allure.title("车辆行驶里程_CDC里程同步_大于10km不同步")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.test1128
    def test_caseid_1995692(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"): 
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0x0B],recv=[0x6E,0xDD,0x01])
            sleep(2) 
            A = self.bus_comm.get_TotDstTrvldHiResl_value()
            logger.info("总里程: TotDstTrvldHiResl {}".format(A))
            A1 = self.bus_comm.get_BkpOfDstTrvld_value()
            if A1 < 10:
                logger.info("BGM里程小于10km")
                assert False,"重新设置BGM里程"
            else:
                logger.info("BGM里程超过10km")
                self.soa.set_Distance_cdc(1000000000)
                sleep(5)
                self.bus_comm.check_TotDstTrvldHiResl_value(11000)
                self.bus_comm.check_BkpOfDstTrvld_value(11)
                
    @allure.title("车辆行驶里程_CDC里程同步_大于BGM里程同步最大值（2000000km）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.test1128
    def test_caseid_1999119(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"):
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0x00],recv=[0x6E,0xDD,0x01])
            sleep(2)    
            A = self.bus_comm.get_TotDstTrvldHiResl_value()
            logger.info("总里程: TotDstTrvldHiResl {}".format(A))
            A1 = self.bus_comm.get_BkpOfDstTrvld_value()
            if A1 < 10:
                logger.info("BGM里程小于10km")
                self.soa.set_Distance_cdc(2000000000)
                sleep(5)
                self.bus_comm.check_TotDstTrvldHiResl_value(2000000000)
                self.bus_comm.check_BkpOfDstTrvld_value(2000000)
            else:
                logger.info("BGM里程超过10km")
                assert False,"重新设置BGM里程"

    @allure.title("车辆行驶里程_CDC里程同步_大于BGM里程同步中间值（1000000km）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.test1128
    def test_caseid_1999120(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"): 
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0x00],recv=[0x6E,0xDD,0x01])
            sleep(2) 
            A = self.bus_comm.get_TotDstTrvldHiResl_value()
            logger.info("总里程: TotDstTrvldHiResl {}".format(A))
            A1 = self.bus_comm.get_BkpOfDstTrvld_value()
            if A1 < 10:
                logger.info("BGM里程小于10km")
                self.soa.set_Distance_cdc(1000000000)
                sleep(5)
                self.bus_comm.check_TotDstTrvldHiResl_value(1000000000)
                self.bus_comm.check_BkpOfDstTrvld_value(1000000)
            else:
                logger.info("BGM里程超过10km")
                assert False,"重新设置BGM里程"
    
    @allure.title("车辆行驶里程_CDC里程同步_大于BGM里程同步最大值（4294000km）")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.test1128
    def test_caseid_1998911(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"): 
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0x00],recv=[0x6E,0xDD,0x01])
            sleep(2) 
            A = self.bus_comm.get_TotDstTrvldHiResl_value()
            logger.info("总里程: TotDstTrvldHiResl {}".format(A))
            A1 = self.bus_comm.get_BkpOfDstTrvld_value()
            if A1 < 10:
                logger.info("BGM里程小于10km")
                self.soa.set_Distance_cdc(4294000000)
                sleep(5)
                self.bus_comm.check_TotDstTrvldHiResl_value(2000000000)
                self.bus_comm.check_BkpOfDstTrvld_value(2000000)
            else:
                logger.info("BGM里程超过10km")
                assert False,"重新设置BGM里程"

    @allure.title(" 车辆行驶里程_CDC里程同步_等于10km BGM里程不同步2")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.test1128
    def test_caseid_1995824(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"): 
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0x0A],recv=[0x6E,0xDD,0x01])
            sleep(2) 
            A = self.bus_comm.get_TotDstTrvldHiResl_value()
            logger.info("总里程: TotDstTrvldHiResl {}".format(A))
            A1 = self.bus_comm.get_BkpOfDstTrvld_value()
            if A1 < 10:
                logger.info("BGM里程小于10km")
                assert False,"重新设置BGM里程"
            else:
                logger.info("BGM里程超过10km")
                self.soa.set_Distance_cdc(1000000000)
                sleep(5)
                self.bus_comm.check_TotDstTrvldHiResl_value(10000)
                self.bus_comm.check_BkpOfDstTrvld_value(10)

    @allure.title(" 车辆行驶里程_CDC里程同步_等于10km BGM里程不同步")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.test1128
    def test_caseid_1995823(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"): 
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0x0A],recv=[0x6E,0xDD,0x01])
            sleep(2) 
            A = self.bus_comm.get_TotDstTrvldHiResl_value()
            logger.info("总里程: TotDstTrvldHiResl {}".format(A))
            A1 = self.bus_comm.get_BkpOfDstTrvld_value()
            if A1 < 10:
                logger.info("BGM里程小于10km")
                assert False,"重新设置BGM里程"
            else:
                logger.info("BGM里程超过10km")
                self.soa.set_Distance_cdc(1000)
                sleep(5)
                self.bus_comm.check_TotDstTrvldHiResl_value(10000)
                self.bus_comm.check_BkpOfDstTrvld_value(10)
    
    @allure.title(" 车辆行驶里程_CDC里程同步_小于10km BGM里程不同步2")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.test1128
    def test_caseid_1995822(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"): 
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0x09],recv=[0x6E,0xDD,0x01])
            sleep(2) 
            A = self.bus_comm.get_TotDstTrvldHiResl_value()
            logger.info("总里程: TotDstTrvldHiResl {}".format(A))
            A1 = self.bus_comm.get_BkpOfDstTrvld_value()
            if A1 < 10:
                logger.info("BGM里程小于10km")
                self.soa.set_Distance_cdc(1000)
                sleep(5)
                self.bus_comm.check_TotDstTrvldHiResl_value(9000)
                self.bus_comm.check_BkpOfDstTrvld_value(9)
            else:
                logger.info("BGM里程超过10km")
                assert False,"重新设置BGM里程"

    @allure.title(" 车辆行驶里程_CDC里程同步_持续时间小于5S不同步")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.test1128
    def test_caseid_1995739(self):
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])    
        with allure.step("安全验证"):
            self.sd_tester.security_access_level(UnLock.L5)
        with allure.step("设置总里程"): 
            self.sd_tester.send_request_and_recv_response([0x2E,0xDD,0x01,0x00,0x00,0x09],recv=[0x6E,0xDD,0x01])
            sleep(2) 
            A = self.bus_comm.get_TotDstTrvldHiResl_value()
            logger.info("总里程: TotDstTrvldHiResl {}".format(A))
            A1 = self.bus_comm.get_BkpOfDstTrvld_value()
            if A1 < 10:
                logger.info("BGM里程小于10km")
                self.soa.set_Distance_cdc(20000)
                sleep(4)
                self.soa.set_Distance_cdc(1000)
                self.bus_comm.check_TotDstTrvldHiResl_value(9000)
                self.bus_comm.check_BkpOfDstTrvld_value(9)
            else:
                logger.info("BGM里程超过10km")
                assert False,"重新设置BGM里程"
            
    @allure.title("638234_行驶里程_行驶里程计算_存储NVM（诊断）")
    @pytest.mark.sanity
    @pytest.mark.nvm
    def test_caseid_1994582(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_and_qf(vehspd=0.0, veh_qf= VehSpdQf.AccurData)
        A = self.bus_comm.get_TotDstTrvldHiResl_value()
        A1 = self.bus_comm.get_BkpOfDstTrvld_value()
        self.bus_comm.set_vehspd_and_qf(vehspd=10.0, veh_qf= VehSpdQf.AccurData)
        sleep(300)
        self.bus_comm.set_vehspd_and_qf(vehspd=0.0, veh_qf= VehSpdQf.AccurData)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        B = self.bus_comm.get_TotDstTrvldHiResl_value()
        B1 = self.bus_comm.get_BkpOfDstTrvld_value()
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        C = self.bus_comm.get_TotDstTrvldHiResl_value()
        C1 = self.bus_comm.get_BkpOfDstTrvld_value()
        assert B == C,  '里程诊断TotDstTrvldHiResl数值存储异常'
        assert B1 == C1,  '里程诊断BkpOfDstTrvld数值存储异常'

    @allure.title("638234_行驶里程_行驶里程计算_存储NVM（上下电）")
    @pytest.mark.sanity
    @pytest.mark.nvm
    def test_caseid_1994583(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_and_qf(vehspd=0.0, veh_qf= VehSpdQf.AccurData)
        A = self.bus_comm.get_TotDstTrvldHiResl_value()
        A1 = self.bus_comm.get_BkpOfDstTrvld_value()
        self.bus_comm.set_vehspd_and_qf(vehspd=10.0, veh_qf= VehSpdQf.AccurData)
        sleep(300)
        self.bus_comm.set_vehspd_and_qf(vehspd=0.0, veh_qf= VehSpdQf.AccurData)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        B = self.bus_comm.get_TotDstTrvldHiResl_value()
        B1 = self.bus_comm.get_BkpOfDstTrvld_value()
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        C = self.bus_comm.get_TotDstTrvldHiResl_value()
        C1 = self.bus_comm.get_BkpOfDstTrvld_value()
        assert B == C,  '里程上下电TotDstTrvldHiResl数值存储异常'
        assert B1 == C1,  '里程上下电BkpOfDstTrvld数值存储异常'

    @allure.title("638234_行驶里程_行驶里程计算_存储NVM（休眠）")
    @pytest.mark.sanity
    @pytest.mark.nvm
    def test_caseid_1994581(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_and_qf(vehspd=0.0, veh_qf= VehSpdQf.AccurData)
        A = self.bus_comm.get_TotDstTrvldHiResl_value()
        A1 = self.bus_comm.get_BkpOfDstTrvld_value()
        self.bus_comm.set_vehspd_and_qf(vehspd=10.0, veh_qf= VehSpdQf.AccurData)
        sleep(300)
        self.bus_comm.set_vehspd_and_qf(vehspd=0.0, veh_qf= VehSpdQf.AccurData)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        B = self.bus_comm.get_TotDstTrvldHiResl_value()
        B1 = self.bus_comm.get_BkpOfDstTrvld_value()
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        C = self.bus_comm.get_TotDstTrvldHiResl_value()
        C1 = self.bus_comm.get_BkpOfDstTrvld_value()
        assert B == C,  '里程休眠TotDstTrvldHiResl数值存储异常'
        assert B1 == C1,  '里程休眠BkpOfDstTrvld数值存储异常'