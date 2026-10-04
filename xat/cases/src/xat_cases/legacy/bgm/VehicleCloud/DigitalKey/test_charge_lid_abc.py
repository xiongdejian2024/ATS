#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_charge_lid_abc.py
@Time         :2024/03/15 10:50:21
@Author       :hui.zhao@jiduauto.com
@Description  :数字钥匙充电盖相关
"""

from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass_abc import *
from xat_ecu.api.abc_interface import *

@allure.feature("互联服务")
@allure.story("数字钥匙和账号/其他/充电桩蓝牙充电口盖控制")
class TestDigitalKeyChargePileOpenChargeLid(TestDigitalKeyBase):
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.telm_set_chrglid_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.telm_set_hv_active_req(req=RemHvStrtActvReq.On)
    
    def after_each_func(self, ecu):
        super().after_each_func(ecu)


    @allure.title("充电桩蓝牙充电口盖控制_Success_INACTIVE+P档+整车解锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111987?projectId=46')
    @pytest.mark.smoke
    def test_caseid_111987(self):
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.dk.send_charge_pile_open_charge_lid_cmd()
        self.bus_comm.check_chrgild_req(ChrgLidReq.Open)
        self.bus_comm.check_chrgild_req(ChrgLidReq.Idle)

    @allure.title("充电桩蓝牙充电口盖控制_Success_INACTIVE+N档+整车上锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111990?projectId=46')
    @pytest.mark.smoke
    def test_caseid_111990(self):
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        sleep(1)
        self.bus_comm.dk.send_charge_pile_open_charge_lid_cmd()
        self.bus_comm.check_chrgild_req(ChrgLidReq.Open)
        self.bus_comm.check_chrgild_req(ChrgLidReq.Idle)


    @allure.title("充电桩蓝牙充电口盖控制_Success_AVTIVE+N档+主驾未占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111986?projectId=46')
    @pytest.mark.full
    def test_caseid_111986(self):
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        sleep(1)
        self.bus_comm.dk.send_charge_pile_open_charge_lid_cmd()
        self.bus_comm.check_chrgild_req(ChrgLidReq.Open)
        self.bus_comm.check_chrgild_req(ChrgLidReq.Idle)

   
    @allure.title("充电桩蓝牙充电口盖控制_Success_CONVENIENCE+P档+主驾未占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111989?projectId=46')
    @pytest.mark.smoke
    def test_caseid_111989(self):
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.dk.send_charge_pile_open_charge_lid_cmd()
        self.bus_comm.check_chrgild_req(ChrgLidReq.Open)
        self.bus_comm.check_chrgild_req(ChrgLidReq.Idle)

    @allure.title("充电桩蓝牙充电口盖控制_Fail_CONVENIENCE+P档+主驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111988?projectId=46')
    @pytest.mark.full
    def test_caseid_111988(self):
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.io.driver_seat_present()
        self.bus_comm.dk.send_charge_pile_open_charge_lid_cmd()
        self.bus_comm.check_no_chrgild_req(req=ChrgLidReq.Idle)

    @allure.title("充电桩蓝牙充电口盖控制_Fail_ACTIVE+R档+主驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111983?projectId=46')
    @pytest.mark.full
    def test_caseid_111983(self):
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.io.driver_seat_present()
        self.bus_comm.dk.send_charge_pile_open_charge_lid_cmd()
        self.bus_comm.check_no_chrgild_req(req=ChrgLidReq.Idle)

    @allure.title("充电桩蓝牙充电口盖控制_Fail_ACTIVE+D档+主驾未占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111984?projectId=46')
    @pytest.mark.full
    def test_caseid_111984(self):
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.bus_comm.dk.send_charge_pile_open_charge_lid_cmd()
        self.bus_comm.check_no_chrgild_req(req=ChrgLidReq.Idle)

    @allure.title("充电桩蓝牙充电口盖控制_Fail_CONVENIENCE+R档+主驾未占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111982?projectId=46')
    @pytest.mark.full
    def test_caseid_111982(self):
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.bus_comm.dk.send_charge_pile_open_charge_lid_cmd()
        self.bus_comm.check_no_chrgild_req(req=ChrgLidReq.Idle)

    @allure.title("充电桩蓝牙充电口盖控制_Fail_INACTIVE+P档+主驾未占座+Action=0x0")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111985?projectId=46')
    @pytest.mark.full
    def test_caseid_111985(self):
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.dk.send_charge_pile_open_charge_lid_cmd(action=0)
        self.bus_comm.check_no_chrgild_req(req=ChrgLidReq.Idle)

    @allure.title("直流电充电桩蓝牙充电口盖控制_Success_充电枪未连接")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1990919?projectId=46')
    @pytest.mark.smoke
    @pytest.mark.v210
    def test_caseid_1990919(self):
        self.sd_tester.write_multi_ccp({973:2})
        self.sd_tester.reset_bgm()
        self.bus_comm.set_onbd_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.dk.send_rke_chargelidgate(op=-1)
        self.bus_comm.dk.ck_rke_resp(12,0, "PreConditionOK", exec_type=2)
        self.bus_comm.set_chrglid_pos(0)
        self.bus_comm.dk.ck_rke_resp(12,0, "Success", exec_type=3)

    @allure.title("直流电充电桩蓝牙充电口盖控制_Fail_充电枪连接")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1990918?projectId=46')
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_caseid_1990918(self):
        self.sd_tester.write_multi_ccp({973:2})
        self.sd_tester.reset_bgm()
        self.bus_comm.set_onbd_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.dk.send_rke_chargelidgate(op=-1)
        self.bus_comm.dk.ck_rke_resp(12,1, "PluggerConnected", exec_type=3)

    @allure.title("交流电充电桩蓝牙充电口盖控制_Success_充电枪未连接")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1990917?projectId=46')
    @pytest.mark.smoke
    @pytest.mark.v210
    def test_caseid_1990917(self):
        self.sd_tester.write_multi_ccp({973:2})
        self.sd_tester.reset_bgm()
        self.bus_comm.set_onbd_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.dk.send_rke_chargelidgate(op=-1)
        self.bus_comm.dk.ck_rke_resp(12,0, "PreConditionOK", exec_type=2)
        self.bus_comm.set_chrglid_pos(0)
        self.bus_comm.dk.ck_rke_resp(12,0, "Success", exec_type=3)

    @allure.title("交流电充电桩蓝牙充电口盖控制_Fail_充电枪连接")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1990916?projectId=46')
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_caseid_1990916(self):
        self.sd_tester.write_multi_ccp({973:2}) 
        self.sd_tester.check_ccp_value({973:2})
        self.sd_tester.reset_bgm()
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait=3)
        self.bus_comm.set_onbd_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.dk.send_rke_chargelidgate(op=-1)
        self.bus_comm.dk.ck_rke_resp(12,1, "PluggerConnected", exec_type=3)

    @allure.title("重启后功能充电口盖启动对应用例")
    @pytest.mark.full
    def test_caseid_1985388(self):
        logger.info("------------------>复位BGM")
        self.io.bgm_power_off()
        time.sleep(2)
        self.io.bgm_power_on()
        time.sleep(15)
        logger.info("------------------>复位BGM结束")
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        sleep(1)
        self.bus_comm.dk.send_charge_pile_open_charge_lid_cmd()
        self.bus_comm.check_chrgild_req(ChrgLidReq.Open)
        self.bus_comm.check_chrgild_req(ChrgLidReq.Idle)
